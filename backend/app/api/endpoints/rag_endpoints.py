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
    # TODO: fix scoring to take max score of a document ID for whole document, later we will use document and page
    for doc, score in zip(documents, scores):
        metadata = getattr(doc, "metadata", {})
        document_id = metadata.get("document_id", "")
        if document_id not in document_id_set:
            document_name = metadata.get("document_name", "")
            sources.append({
                "document_name": document_name,
                "document_id": document_id,
                "score": score
            })
            document_id_set.add(document_id)
    return {"response": response, "sources": sources}
