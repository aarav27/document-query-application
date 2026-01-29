import numpy as np
from sentence_transformers import SentenceTransformer
from app.rag.vector_db import vectordb

def semantic_search(query, documents, top_k=5, similarity_threshold=0.2):

    model = SentenceTransformer('all-MiniLM-L6-v2')
    documents_text = [doc.extracted_text for doc in documents]
    document_embeddings = model.encode(documents_text)

    query_embedding = model.encode([query])
    similarities = np.dot(query_embedding, document_embeddings.T).flatten()
    top_indices = similarities.argsort()[-top_k:][::-1]

    search_results = []
    for index in top_indices:
        if similarities[index] >= similarity_threshold:
            search_results.append(documents[index])
    return search_results

def semantic_search_vb(query):
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,
            "fetch_k": 20
        }
    )
    docs = retriever.invoke(query)
    return docs