from http.client import HTTPException
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

async def delete_document(document_id: int, db: AsyncSession):
    document = await db.get(models.Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.delete(document)
    await db.commit()
    return {"ok": True}


async def get_categories(db: AsyncSession):
    result = await db.execute(select(models.Category))
    return result.scalars().all()