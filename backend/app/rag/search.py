from typing import List, Optional, Dict
from app.rag.vector_stores import get_vector_store, VectorStore
from qdrant_client.models import Filter, FieldCondition, Fusion, FusionQuery, MatchValue, Prefetch, SparseVector

def hybrid_search(query: str, category_ids: Optional[List[int]] = None, k: int = 5, with_scores: bool = False) -> List[str]:
    
    vector_store: VectorStore = get_vector_store()
    client = vector_store.client
    
    # Filter based on category IDs
    query_filter = None
    if category_ids:
        query_filter = Filter(
            must=[FieldCondition(
                key="category_id", 
                match=MatchValue(value=category_ids)
            )]
        )
    
    # Create dense and sparse vectors for hybrid search
    dense_query_vector = next(vector_store.dense_embedding_model.query_embed(query))
    sparse_query_vector = next(vector_store.bm25_embedding_model.query_embed(query))

    # Perform hybrid search: semantic + BM25 with RRF ranking
    search_result = client.query_points(
        collection_name=vector_store.collection_name,
        prefetch=[
            Prefetch(
                query=dense_query_vector,
                using="dense",
                limit=k*2,
            ),
            Prefetch(
                query=SparseVector(**sparse_query_vector.as_object()),
                using="sparse",
                limit=k*2,
            ),
        ],
        query=FusionQuery(fusion=Fusion.RRF),
        query_filter=query_filter,
        limit=k,
        search_params={
            "hnsw_ef": 100,
        }
    )

    # Aggregate scores for each document ID level
    document_chunks: Dict[int, List[float]] = {}
    for scored_point in search_result.points:
        metadata = scored_point.payload
        document_id = metadata.get("document_id")
        if document_id not in document_chunks:
            document_chunks[document_id] = []
        document_chunks[document_id].append(scored_point.score)
    
    # Keep the highest score for each document across all its chunks
    document_scores = [
        {
            "document_id": document_id,
            "score": max(scores)
        }
        for document_id, scores in document_chunks.items()
    ]
    document_scores.sort(key=lambda x: x["score"], reverse=True)
    if with_scores:
        return document_scores
    return [doc["document_id"] for doc in document_scores]