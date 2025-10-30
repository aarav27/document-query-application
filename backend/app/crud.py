from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def get_documents(db: AsyncSession):
    result = await db.execute(select(models.Document))
    return result.scalars().all()

async def get_categories(db: AsyncSession):
    result = await db.execute(select(models.Category))
    return result.scalars().all()