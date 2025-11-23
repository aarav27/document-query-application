from http.client import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.s3 import s3_client, create_s3_document_key, AWS_S3_BUCKET
from app.core.tasks import extract_pdf_text
from app.models import document_model
from app.schemas import document_schema

async def get_documents(db: AsyncSession):
    result = await db.execute(select(document_model.Document))
    return result.scalars().all()

async def post_document(document: document_schema.DocumentCreate, db: AsyncSession):
    # 1. Adds document record to Postgres
    new_document = document_model.Document(
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

async def put_document_extract_text(document_id: int, db: AsyncSession):
    db_result = await db.execute(select(document_model.Document).where(document_model.Document.id == document_id))
    document = db_result.scalar_one_or_none()
    if not document or not document.s3_document_key:
        return {"status": "Document not found"}

    extracted_text = extract_pdf_text(document.s3_document_key)
    document.extracted_text = extracted_text
    db.add(document)
    await db.commit()
    await db.refresh(document)
    
    return {"status": "Success", "extracted_text": extracted_text}

async def delete_document(document_id: int, db: AsyncSession):
    document = await db.get(document_model.Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.delete(document)
    await db.commit()
    return {"ok": True}