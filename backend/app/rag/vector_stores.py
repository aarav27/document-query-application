from langchain_chroma import Chroma
from app.rag.embeddings import get_sentence_transformers

dev_client = Chroma(
    collection_name="DocQuery_ChromaDB",
    persist_directory="./chroma_db",
    embedding_function=get_sentence_transformers(),
    collection_metadata={"hnsw:space": "cosine"}
)

test_client = Chroma(
    collection_name="DocQuery_test",
    persist_directory="./chroma_db_test",
    embedding_function=get_sentence_transformers(),
    collection_metadata={"hnsw:space": "cosine"}
)

def get_chroma_client(env: str = "test"):
    if env.lower() == "test":
        return test_client
    return dev_client
