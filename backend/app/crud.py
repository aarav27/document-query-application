from http.client import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from .s3 import s3_client, create_s3_document_key, AWS_S3_BUCKET

async def get_documents(db: AsyncSession):
    result = await db.execute(select(models.Document))
    return result.scalars().all()

async def post_document(document: schemas.DocumentCreate, db: AsyncSession):
    # 1. Adds document record to Postgres
    new_document = models.Document(
        name=document.name,
        description=document.description,
        category_id=document.category_id,
    )
    db.add(new_document)
    await db.commit()
    await db.refresh(new_document)

    # 2. Create S3 document key and updates document record
    s3_document_key = create_s3_document_key(new_document.id, document.name)
    new_document.s3_document_key = s3_document_key
    db.add(new_document)
    await db.commit()
    await db.refresh(new_document)

    # 3. Generates S3 presigned upload URL
    upload_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": AWS_S3_BUCKET, "Key": s3_document_key},
        ExpiresIn=3600,
    )

    return {**new_document.__dict__, "upload_url": upload_url}

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

async def post_category(category: schemas.CategoryCreate, db: AsyncSession):
    new_category = models.Category(
        name=category.name
    )
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

async def delete_category(category_id: int, db: AsyncSession):
    category = await db.get(models.Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(category)
    await db.commit()
    return {"ok": True}