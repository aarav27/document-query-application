
from http.client import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import category_model
from app.schemas import category_schema

async def get_categories(db: AsyncSession):
    result = await db.execute(select(category_model.Category))
    return result.scalars().all()

async def post_category(category: category_schema.CategoryCreate, db: AsyncSession):
    new_category = category_model.Category(
        name=category.name
    )
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

async def delete_category(category_id: int, db: AsyncSession):
    category = await db.get(category_model.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(category)
    await db.commit()
    return {"ok": True}