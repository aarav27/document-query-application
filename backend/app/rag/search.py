from app.rag.document_pipeline import vectordb

def semantic_search(query, category_ids: list[int] | None = None):
    search_kwargs={
        "k": 5,
        "fetch_k": 20
    }
    if category_ids is not None:
        search_kwargs["filter"] = {
            "category_id": {"$in": category_ids}
        }
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs=search_kwargs,
    )
    vectordb_docs = retriever.invoke(query)
    document_ids = [
        doc.metadata["document_id"]
        for doc in vectordb_docs
    ]
    return document_ids