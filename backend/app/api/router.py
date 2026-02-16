from fastapi import APIRouter
from app.api.endpoints import document_endpoints, category_endpoints, search_endpoints, rag_endpoints

api_router = APIRouter(prefix="")

api_router.include_router(
    document_endpoints.document_router,
    prefix="/documents",
    tags=["Documents"],
)
api_router.include_router(
    category_endpoints.category_router,
    prefix="/categories",
    tags=["Categories"],
)
api_router.include_router(
    search_endpoints.search_router,
    prefix="/search",
    tags=["Document Search"],
)
api_router.include_router(
    rag_endpoints.rag_router,
    prefix="/rag",
    tags=["RAG"],
)