from qdrant_client import QdrantClient
from qdrant_client.models import Distance, SparseVectorParams, VectorParams
from fastembed import TextEmbedding, SparseTextEmbedding
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "docquery_qdrant"
EMBEDDING_DIM = 384
DENSE_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
BM25_EMBEDDING_MODEL = "Qdrant/bm25"

_vector_store = None
_client = None

class VectorStore:
    def __init__(self, client, collection_name):
        self.client = client
        self.collection_name = collection_name
        self.dense_embedding_model = TextEmbedding(DENSE_EMBEDDING_MODEL)
        self.bm25_embedding_model = SparseTextEmbedding(BM25_EMBEDDING_MODEL)


def get_client() -> QdrantClient:
    global _client
    if _client is None:
        if QDRANT_API_KEY:
            _client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        else:
            _client = QdrantClient(url=QDRANT_URL)
    return _client

def initialize_collection(client: QdrantClient, collection_name: str = COLLECTION_NAME) -> None:
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
        logger.error(f"Failed to create collection: {e}")
        raise

def delete_collection(collection_name: str = COLLECTION_NAME) -> None:
    client = get_client()
    try:
        client.delete_collection(collection_name=collection_name)
        logger.info(f"Deleted collection: {collection_name}")
    except Exception as e:
        logger.error(f"Failed to delete collection {collection_name}: {e}")
        raise

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        client = get_client()
        initialize_collection(client, COLLECTION_NAME)
        _vector_store = VectorStore(client, COLLECTION_NAME)
    return _vector_store