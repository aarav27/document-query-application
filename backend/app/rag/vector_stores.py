from langchain_chroma import Chroma
from langchain_elasticsearch import ElasticsearchStore
from app.rag.embeddings import get_sentence_transformers
from dotenv import load_dotenv
import os

load_dotenv()
ES_URL = os.getenv("ES_LOCAL_URL")
ES_LOCAL_API_KEY = os.getenv("ES_LOCAL_API_KEY")

chroma_dev_db = Chroma(
    collection_name="DocQuery_ChromaDB",
    persist_directory="./chroma_db",
    embedding_function=get_sentence_transformers(),
    collection_metadata={"hnsw:space": "cosine"}
)

chroma_test_db = Chroma(
    collection_name="DocQuery_test",
    persist_directory="./chroma_db_test",
    embedding_function=get_sentence_transformers(),
    collection_metadata={"hnsw:space": "cosine"}
)

elasticsearch_store_dev = ElasticsearchStore(
    index_name="docquery_elasticsearch",
    embedding=get_sentence_transformers(),
    es_url=ES_URL,
    es_api_key=ES_LOCAL_API_KEY,
    strategy=ElasticsearchStore.ApproxRetrievalStrategy(
        hybrid=True,
        rrf={"rank_constant": 60, "window_size": 50}
    ),
)

# elasticsearch_store_test = ElasticsearchStore(
#     index_name="docquery_elasticsearch_test",
#     embedding=get_sentence_transformers(),
#     es_url=ES_URL,
#     es_api_key=ES_LOCAL_API_KEY,
#     strategy=ElasticsearchStore.ApproxRetrievalStrategy(
#         hybrid=True,
#         rrf={"rank_constant": 60, "window_size": 50}
#     ),
# )

def get_vector_store():
    return elasticsearch_store_dev
