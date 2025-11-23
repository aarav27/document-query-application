from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.s3 import s3_client, AWS_S3_BUCKET
from app.services import document_service
from app.schemas import document_schema

document_router = APIRouter()

@document_router.get(
    "/",
    summary="Get all documents",
    response_model=list[document_schema.Document]
)
async def read_documents(db: AsyncSession = Depends(get_db)):
    return await document_service.get_documents(db)

@document_router.post(
    "/",
    summary="Create new document",
    response_model=document_schema.DocumentUpload
)
async def create_document(document: document_schema.DocumentCreate, db: AsyncSession = Depends(get_db)):
    return await document_service.post_document(document, db)

@document_router.put(
    "/{document_id}/extract",
    summary="Update extracted_text in document",
    response_model=dict
)
async def extract_text_document(document_id: int, db: AsyncSession = Depends(get_db)):
    return await document_service.put_document_extract_text(document_id, db)

@document_router.delete(
    "/{document_id}",
    summary="Delete document",
    response_model=dict
)
async def delete_document(document_id: int, db: AsyncSession = Depends(get_db)):
    return await document_service.delete_document(document_id, db)

@document_router.get(
    "/download-url/{document_key}",
    summary="Generate presigned URL for document",
    response_model=dict
)
async def generate_download_url(document_key: str, document_name: str):
    download_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": AWS_S3_BUCKET, 
            "Key": document_key,
            "ResponseContentDisposition": f'inline; filename="{document_name}.pdf"'},
        ExpiresIn=3600,
        
    )
    return {"download_url": download_url}