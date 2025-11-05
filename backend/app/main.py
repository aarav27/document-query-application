from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas, crud
from .database import engine, Base, get_db
from .s3 import s3_client, AWS_S3_BUCKET

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Documents
@app.get("/documents", response_model=list[schemas.Document])
async def read_documents(db: AsyncSession = Depends(get_db)):
    return await crud.get_documents(db)

@app.post("/documents", response_model=schemas.Document)
async def create_document(document: schemas.DocumentCreate, db: AsyncSession = Depends(get_db)):
    return await crud.post_document(document, db)

@app.delete("/documents/{document_id}", response_model=dict)
async def delete_document(document_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_document(document_id, db)


# Categories
@app.get("/categories", response_model=list[schemas.Category])
async def read_categories(db: AsyncSession = Depends(get_db)):
    return await crud.get_categories(db)

@app.post("/categories", response_model=schemas.Category)
async def create_category(category: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.post_category(category, db)


# S3 Presigned URLs  
@app.post("/upload-url")
async def generate_upload_url(filename: str):
    upload_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": AWS_S3_BUCKET, "Key": filename},
        ExpiresIn=60,
    )
    return {"upload_url": upload_url, "file_key": filename}

@app.get("/download-url")
async def generate_download_url(filename: str):
    download_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": AWS_S3_BUCKET, "Key": filename},
        ExpiresIn=60,
    )
    return {"download_url": download_url, "file_key": filename}