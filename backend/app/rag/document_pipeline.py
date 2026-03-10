import fitz
import hashlib
import pymupdf4llm
from typing import Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue

from app.core.s3 import s3_client, AWS_S3_BUCKET
from app.models import document_model
from app.rag.vector_stores import get_vector_store, VectorStore

# Text chunking configuration
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

def ingest_document_vectordb(new_document: document_model.Document, category_name: str, category_id: Optional[int] = None) -> None:

    # 1. Download PDF from S3
    file = s3_client.get_object(Bucket=AWS_S3_BUCKET, Key=new_document.s3_document_key)
    file_bytes = file["Body"].read()

    # 2. Extract text as markdown for better structure preservation
    pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
    markdown_text = pymupdf4llm.to_markdown(pdf_doc)

    # 3. Split text into overlapping chunks
    chunks = splitter.split_text(markdown_text)

    if not chunks:
        return {"message": "No chunks extracted from document"}

    # 4. Ingest document and (dense and sparse) embeddings into vector store
    vector_store: VectorStore = get_vector_store()
    client = vector_store.client

    dense_model = vector_store.dense_embedding_model
    sparse_model = vector_store.bm25_embedding_model
    dense_vectors = list(dense_model.passage_embed(chunks))
    sparse_vectors = list(sparse_model.passage_embed(chunks))
    
    points = []
    for i, chunk in enumerate(chunks):
        
        metadata = {
            "document_id": new_document.id,
            "document_name": new_document.name,
            "description": new_document.description,
            "category_name": category_name,
            "category_id": category_id,
            "chunk_id": i,
            "total_chunks": len(chunks),
            "chunk_content": chunk
        }
        
        point = PointStruct(
            id=int(str(new_document.id) + str(i).zfill(6)),
            vector={
                "dense": dense_vectors[i].tolist(),
                "sparse": sparse_vectors[i].as_object()
            },
            payload=metadata
        )
        points.append(point)
    
    client.upsert(
        collection_name=vector_store.collection_name,
        points=points
    )


def delete_document_vectordb(document_id: int) -> None:
    vector_store = get_vector_store()
    client = vector_store.client
    collection_name = vector_store.collection_name 

    try:
        client.delete(
            collection_name=collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id)
                    )
                ]
            )
        )
        
    except:
        return