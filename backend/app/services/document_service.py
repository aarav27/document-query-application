from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import document_model
from app.schemas import document_schema

async def get_documents_all(db: AsyncSession):
    db_result = await db.execute(select(document_model.Document))
    return db_result.scalars().all()

async def get_documents_by_ids(ids: list[int], db: AsyncSession):
    db_result = await db.execute(
        select(document_model.Document)
        .where(document_model.Document.id.in_(ids)))
    return db_result.scalars().all()

async def get_documents_by_category_id(category_id, db: AsyncSession):
    db_result = await db.execute(
        select(document_model.Document)
        .where(document_model.Document.category_id == category_id))
    return db_result.scalars().all()

async def post_document(document: document_schema.DocumentCreate, db: AsyncSession):
    new_document = document_model.Document(
        name=document.name,
        description=document.description,
        category_id=document.category_id,
        s3_document_key=document.s3_document_key
    )
    db.add(new_document)
    await db.commit()
    await db.refresh(new_document)
    return new_document

async def delete_document(document_id: int, db: AsyncSession):
    document = await db.get(document_model.Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.delete(document)
    await db.commit()
    return {"ok": True}