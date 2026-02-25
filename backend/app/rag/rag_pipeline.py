import logging
from typing import List, Optional

from app.rag.vector_stores import get_vector_store
from app.rag.models import get_llm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def qna_pipeline(query: str, category_ids: list[int] | None = None):
    processed_query = process_query(query)
    documents = retrieval(processed_query, category_ids)
    sources = create_sources(documents)
    if not documents:
        return "The provided sources do not contain any information about this subject.", sources
    context = augmentation(documents)
    response = generation(processed_query, context)
    if "don't have sufficient information to answer" in response:
        sources = []
    return response, sources

def process_query(query):
    return query.strip()

def retrieval(query: str, category_ids: Optional[List[int]] = None, k: int = 3, score_threshold: float = -100):
    filter_dict = None
    if category_ids:
        filter_dict = {"category_id": {"$in": category_ids}}
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k, filter=filter_dict)
    documents = results
    # relevant_results = [(doc, score) for doc, score in results if score >= score_threshold]
    # if not relevant_results:
    #     return [], []
    # documents, scores = zip(*relevant_results)
    return documents

def create_sources(documents):
    sources = []
    doc_set = set()
    for doc in documents:
        metadata = getattr(doc, "metadata", {})
        document_id = metadata.get("document_id", "")
        if document_id not in doc_set:
            sources.append({
                "document_id": document_id,
                "document_name": metadata.get("document_name", ""),
                "category_name": metadata.get("category_name", ""),
                "score": 0.5
            })
    return sources
    # source_score_map = {}
    # for doc, score in zip(documents, scores):
    #     metadata = getattr(doc, "metadata", {})
    #     document_id = metadata.get("document_id", "")
    #     if document_id not in source_score_map:
    #         source_score_map[document_id] = (doc, score)
    #     elif score > source_score_map[document_id][1]:
    #         source_score_map[document_id] = (doc, score)

    # sources = []
    # for document_id, (doc, highest_score) in source_score_map.items():
    #     metadata = getattr(doc, "metadata", {})
    #     sources.append({
    #         "document_id": document_id,
    #         "document_name": metadata.get("document_name", ""),
    #         "category_name": metadata.get("category_name", ""),
    #         "score": highest_score
    #     })
    # return sources

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
                "You answer questions using ONLY the provided sources.\n"
                "Do NOT use prior knowledge.\n"
                "Do NOT infer or guess.\n"
                "If the answer is not explicitly contained in the sources, respond with exactly: \"I don't have sufficient information to answer\" and do not explain why and do not mention the sources."
            )
        },
        {
            "role": "user",
            "content": f"Sources:\n{context}\n\nQuestion: {query}"
        }
    ]

    llm_pipeline = get_llm()
    output = llm_pipeline(messages)
    response = output[0]['generated_text']
    return response


