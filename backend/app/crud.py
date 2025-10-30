from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def get_documents(db: AsyncSession):
    result = await db.execute(select(models.Document))
    return result.scalars().all()

async def post_document(document: schemas.DocumentCreate, db: AsyncSession):
    new_document = models.Document(
        name=document.name,
        description=document.description,
        category_id=document.category_id,
    )

    db.add(new_document)
    await db.commit()
    await db.refresh(new_document)
    return new_document

async def get_categories(db: AsyncSession):
    result = await db.execute(select(models.Category))
    return result.scalars().all()