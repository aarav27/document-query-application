import fitz
from langchain_community.vectorstores import Chroma
# from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pymupdf4llm
from app.core.s3 import s3_client, AWS_S3_BUCKET
from app.models.document_model import Document as DocumentModel

vectordb = Chroma(
    persist_directory="./chroma_db",
    # embedding_function = OpenAIEmbeddings()
)

# @celery_client.task
def ingest_document_vectordb(new_document: DocumentModel):

    # 1. Download PDF from S3
    file = s3_client.get_object(Bucket=AWS_S3_BUCKET, Key=new_document.s3_document_key)
    file_bytes = file["Body"].read()

    # 2. Extract text as markdown
    pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
    markdown_text = pymupdf4llm.to_markdown(pdf_doc)

    # 3. Create chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    chunks = splitter.split_text(markdown_text)

    # 4. Add chunks to vector DB
    vectordb.add_texts(
        texts=chunks,
        metadatas=[
            {
                "category_id": new_document.category_id,
                "document_id": new_document.id,
                "document_name": new_document.name,
                "description": new_document.description,
                "s3_document_key": new_document.s3_document_key,
                "chunk_id": i+1
            }
            for i in range(len(chunks))
        ]
    )
    vectordb.persist()

def delete_document_vectordb(document_id: int):
    vectordb.delete(
        where={
            "document_id": document_id
        }
    )
    vectordb.persist()