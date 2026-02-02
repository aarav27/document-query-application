import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

def get_sentence_transformers():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )