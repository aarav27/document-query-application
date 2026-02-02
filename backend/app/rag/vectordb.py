from langchain_community.vectorstores import Chroma
from app.rag.embeddings import get_open_ai_embeddings
vectordb = Chroma(
    persist_directory="./chroma_db",
    embedding_function=get_open_ai_embeddings()
)