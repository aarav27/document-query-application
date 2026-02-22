import logging
from typing import List, Optional

from app.rag.document_pipeline import chroma_db
from app.rag.models import get_llm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def qna_pipeline(query: str, category_ids: list[int] | None = None):
    processed_query = process_query(query)
    documents, scores = retrieval(processed_query, category_ids)
    context = augmentation(documents)
    response = generation(processed_query, context)
    return response, documents, scores

def process_query(query):
    return query.strip()

def retrieval(query: str, category_ids: Optional[List[int]] = None, k: int = 3):
    filter_dict = None
    if category_ids:
        filter_dict = {"category_id": {"$in": category_ids}}
    results = chroma_db.similarity_search_with_relevance_scores(query, k, filter=filter_dict)
    documents, scores = zip(*results)
    return documents, scores

# TODO: Add category name to metadata
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
        chunk_id = metadata.get("chunk_id", "Unknown")

        section = f"""
            [Source {source_index}]
            Document Name: {document_name}
            Chunk ID: {chunk_id}
            Description: {description}
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
                "If the answer is not in the context, say so clearly."
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


