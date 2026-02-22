from langchain_chroma import Chroma
from app.rag.embeddings import get_sentence_transformers

chroma_db = Chroma(
    collection_name="DocQuery_ChromaDB",
    persist_directory="./chroma_db",
    embedding_function=get_sentence_transformers(),
    collection_metadata={"hnsw:space": "cosine"}
)