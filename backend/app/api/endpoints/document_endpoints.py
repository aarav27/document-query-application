from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.s3 import s3_client, AWS_S3_BUCKET, generate_s3_document_key
from app.rag import document_pipeline
from app.services import document_service
from app.schemas import document_schema

document_router = APIRouter()

@document_router.get(
    "/",
    summary="Get all documents",
    response_model=list[document_schema.Document]
)
async def read_documents_all(db: AsyncSession = Depends(get_db)):
    return await document_service.get_documents_all(db)

@document_router.get(
    "/{document_id}",
    summary="Get document by ID",
    response_model=document_schema.Document
)
async def read_document_by_id(document_id: int, db: AsyncSession = Depends(get_db)):
    return await document_service.get_document_by_id(document_id, db)

@document_router.post(
    "/",
    summary="Create new document",
    response_model=document_schema.Document
)
async def create_document(document: document_schema.DocumentCreate, db: AsyncSession = Depends(get_db)):
    # TODO: Add Transactional Outboxing
    new_document = await document_service.post_document(document, db)
    document_pipeline.ingest_document_vectordb(new_document, document.category_name)
    return new_document

@document_router.delete(
    "/{document_id}",
    summary="Delete document",
    response_model=dict
)
async def delete_document(document_id: int, db: AsyncSession = Depends(get_db)):
    # TODO: Add Transactional Outboxing
    delete_message = await document_service.delete_document(document_id, db)
    document_pipeline.delete_document_vectordb(document_id)
    return delete_message

@document_router.post(
    "/upload-url",
    summary="Generate upload presigned URL for document",
    response_model=dict
)
async def generate_upload_url(upload_request : document_schema.DocumentUploadRequest):
    s3_document_key = generate_s3_document_key(upload_request.name)
    upload_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": AWS_S3_BUCKET,
            "Key": s3_document_key,
            "ContentType": "application/pdf",
        },
        ExpiresIn=3600,
    )
    return {"upload_url": upload_url, "s3_document_key": s3_document_key}
    
@document_router.post(
    "/download-url",
    summary="Generate download presigned URL for document",
    response_model=str
)
async def generate_download_url(download_request: document_schema.DocumentDownloadRequest):
    download_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": AWS_S3_BUCKET, 
            "Key": download_request.s3_document_key,
            "ResponseContentType": "application/pdf",
            "ResponseContentDisposition": f'inline; filename="{download_request.name}"'},
        ExpiresIn=3600,
        
    )
    return download_url