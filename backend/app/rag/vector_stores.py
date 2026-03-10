from qdrant_client import QdrantClient
from qdrant_client.models import Distance, SparseVectorParams, VectorParams
from fastembed import TextEmbedding, SparseTextEmbedding
from dotenv import load_dotenv
import os
import logging

load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "docquery_qdrant"
EMBEDDING_DIM = 384
DENSE_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
BM25_EMBEDDING_MODEL = "Qdrant/bm25"

_qdrant_client = None

class VectorStore:
    def __init__(self, client, collection_name):
        self.client = client
        self.collection_name = collection_name
        self.dense_embedding_model = TextEmbedding(DENSE_EMBEDDING_MODEL)
        self.bm25_embedding_model = SparseTextEmbedding(BM25_EMBEDDING_MODEL)


def get_client() -> QdrantClient:
    global _qdrant_client
    
    if _qdrant_client is not None:
        return _qdrant_client
    
    try:
        if QDRANT_API_KEY:
            _qdrant_client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY
            )
        else:
            _qdrant_client = QdrantClient(url=QDRANT_URL)
        return _qdrant_client
        
    except Exception as e:
        logging.error(f"Failed to connect to Qdrant: {e}")
        raise

def initialize_collection(collection_name: str = COLLECTION_NAME) -> None:
    client = get_client()
    
    try:
        client.get_collection(collection_name)
        return
    except Exception as e:
        logger.info(f"Collection doesn't exist, creating: {collection_name}")
    
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config={
                "dense": VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE)
            },
            sparse_vectors_config={
                "sparse": SparseVectorParams()
            }
        )
    except Exception as e:
        logging.error(f"Failed to create collection: {e}")
        raise

def delete_collection(collection_name: str = COLLECTION_NAME) -> None:
    client = get_client()
    try:
        client.delete_collection(collection_name=collection_name)
        logging.info(f"Deleted collection: {collection_name}")
    except Exception as e:
        logging.error(f"Failed to delete collection {collection_name}: {e}")
        raise

def get_vector_store():
    client = get_client()
    initialize_collection(COLLECTION_NAME)
    return VectorStore(client, COLLECTION_NAME)