import logging
from typing import List, Optional

from app.rag.vector_stores import get_chroma_client
from app.rag.models import get_llm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def qna_pipeline(query: str, category_ids: list[int] | None = None):
    processed_query = process_query(query)
    documents, scores = retrieval(processed_query, category_ids)
    sources = create_sources(documents, scores)
    if not documents:
        return "The provided sources do not contain any information about this subject.", sources
    context = augmentation(documents)
    response = generation(processed_query, context)
    return response, sources

def process_query(query):
    return query.strip()

def retrieval(query: str, category_ids: Optional[List[int]] = None, k: int = 3, score_threshold: float = 0.3):
    filter_dict = None
    if category_ids:
        filter_dict = {"category_id": {"$in": category_ids}}
    chroma_db = get_chroma_client()
    results = chroma_db.similarity_search_with_relevance_scores(query, k, filter=filter_dict)
    relevant_results = [(doc, score) for doc, score in results if score >= score_threshold]
    if not relevant_results:
        return [], []
    documents, scores = zip(*relevant_results)
    return documents, scores

def create_sources(documents, scores):
    
    source_score_map = {}
    for doc, score in zip(documents, scores):
        metadata = getattr(doc, "metadata", {})
        document_id = metadata.get("document_id", "")
        if document_id not in source_score_map:
            source_score_map[document_id] = (doc, score)
        elif score > source_score_map[document_id][1]:
            source_score_map[document_id] = (doc, score)

    sources = []
    for document_id, (doc, highest_score) in source_score_map.items():
        metadata = getattr(doc, "metadata", {})
        sources.append({
            "document_id": document_id,
            "document_name": metadata.get("document_name", ""),
            "category_name": metadata.get("category_name", ""),
            "score": highest_score
        })
    return sources

def augmentation(documents):
    if not documents:
        return ""

    context_sections = []
    source_index = 1
    for doc in documents:
        content = doc.page_content if hasattr(doc, "page_content") else str(doc)
        metadata = getattr(doc, "metadata", {})

        chunk_id = metadata.get("chunk_id")
        document_name = metadata.get("document_name", "Unknown")
        description = metadata.get("description", "")
        category_name = metadata.get("category_name", "Unknown")
        chunk_id = metadata.get("chunk_id", "Unknown")

        section = f"""
            [Source {source_index}]
            Category Name: {category_name}
            Document Name: {document_name}
            Document Description: {description}
            Document Chunk Number: {chunk_id}
            Content Chunk:
            {content}
            """

        context_sections.append(section)
        source_index += 1

    full_context = "\n\n---\n\n".join(context_sections)
    return full_context


def generation(query, context):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that answers only from retrieved knowledge. "
                "Retrieved information is the only source of truth. "
                "Never guess, infer, or rely on prior knowledge."
                "Never fill gaps with reasoning or external knowledge."
                "Most important: If context coverage is incomplete or unclear, explicitly state that the information is missing."
            )
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {query}"
        }
    ]

    llm_pipeline = get_llm()
    output = llm_pipeline(messages)
    response = output[0]['generated_text']
    return response


