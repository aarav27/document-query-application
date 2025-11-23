from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services import category_service
from app.schemas import category_schema

category_router = APIRouter()

@category_router.get(
    "/",
    summary="Get all categories",
    response_model=list[category_schema.Category])
async def read_categories(db: AsyncSession = Depends(get_db)):
    return await category_service.get_categories(db)

@category_router.post(
    "/",
    summary="Create new category",
    response_model=category_schema.Category)
async def create_category(category: category_schema.CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await category_service.post_category(category, db)

@category_router.delete(
    "/{category_id}",
    summary="Delete category",
    response_model=dict)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    return await category_service.delete_category(category_id, db)