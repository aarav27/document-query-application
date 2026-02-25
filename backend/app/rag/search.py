from typing import List, Optional
from app.rag.vector_stores import get_vector_store

def hybrid_search(query, category_ids: Optional[List[int]] = None):
    search_kwargs={
        "k": 5,
        "fetch_k": 20
    }
    if category_ids is not None:
        search_kwargs["filter"] = {
            "category_id": {"$in": category_ids}
        }
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs=search_kwargs,
    )
    vectordb_docs = retriever.invoke(query)

    document_ids = set()
    for doc in vectordb_docs:
        doc_id = doc.metadata["document_id"]
        if doc.metadata["document_id"] not in document_ids:
            document_ids.add(doc_id)
    return list(document_ids)