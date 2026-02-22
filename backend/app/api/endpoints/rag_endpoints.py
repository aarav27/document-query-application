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
    response, sources = qna_pipeline(search_request.query, search_request.category_ids)
    return {"response": response, "sources": sources}
