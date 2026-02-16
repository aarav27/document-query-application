from fastapi import APIRouter

from app.rag.rag_pipeline import qna_pipeline
from app.schemas import search_schema

rag_router = APIRouter()

@rag_router.post(
    "/qna",
    summary="Perform RAG query",
    response_model=dict
)
async def rag_endpoint(search_request : search_schema.SearchRequest):
    response, documents, scores = qna_pipeline(search_request.query, search_request.category_ids)
    sources = []
    document_id_set = set()
    for doc, score in zip(documents, scores):
        metadata = getattr(doc, "metadata", {})
        document_id = metadata.get("document_id", "")
        if document_id in document_id_set:
            continue
        document_name = metadata.get("document_name", "")
        sources.append({
            "document_name": document_name,
            "document_id": document_id,
            "score": score
        })
    return {"response": response, "sources": sources}
