from langchain_community.vectorstores import Chroma
from app.rag.embeddings import get_sentence_transformers
vectordb = Chroma(
    persist_directory="./chroma_db",
    embedding_function=get_sentence_transformers()
)