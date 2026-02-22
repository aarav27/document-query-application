import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pymupdf4llm
from app.core.s3 import s3_client, AWS_S3_BUCKET
from app.models import document_model
from app.rag.vector_stores import chroma_db

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

# @celery_client.task
def ingest_document_vectordb(new_document: document_model.Document, category_name: str):

    # 1. Download PDF from S3
    file = s3_client.get_object(Bucket=AWS_S3_BUCKET, Key=new_document.s3_document_key)
    file_bytes = file["Body"].read()

    # 2. Extract text as markdown
    pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
    markdown_text = pymupdf4llm.to_markdown(pdf_doc)

    # 3. Create chunks
    chunks = splitter.split_text(markdown_text)

    # 4. Add chunks to vector DB
    chroma_db.add_texts(
        texts=chunks,
        metadatas=[
            {   
                "document_id": new_document.id,
                "document_name": new_document.name,
                "description": new_document.description,
                "category_name": category_name,
                "chunk_id": i+1
            }
            for i in range(len(chunks))
        ]
    )

def delete_document_vectordb(document_id: int):
    chroma_db.delete(
        where={
            "document_id": document_id
        }
    )