import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

def get_open_ai_embeddings():
    return OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=OPEN_AI_KEY
    )