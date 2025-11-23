from fastapi import APIRouter

from app.api.endpoints import category, document

api_router = APIRouter(prefix="")

api_router.include_router(
    document.document_router,
    prefix="/documents",
    tags=["Documents"],
)
api_router.include_router(
    category.category_router,
    prefix="/categories",
    tags=["Categories"],
)