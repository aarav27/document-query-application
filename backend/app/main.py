from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, crud
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

@app.post("/documents", response_model=schemas.DocumentUpload)
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


@app.get("/download-url/{document_key}")
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