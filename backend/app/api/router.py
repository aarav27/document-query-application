from app.api.endpoints import document_endpoints
from fastapi import APIRouter

from app.api.endpoints import category_endpoints

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