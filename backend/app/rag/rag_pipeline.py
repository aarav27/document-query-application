import logging
from typing import List, Optional, Dict, Tuple
from qdrant_client.models import Filter, FieldCondition, Fusion, FusionQuery, MatchValue, Prefetch, SparseVector

from app.rag.vector_stores import get_vector_store, VectorStore
from app.rag.models import get_llm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def qna_pipeline(query: str, category_ids: Optional[List[int]] = None, k: int = 3) -> Tuple[str, List[Dict]]:
    # 1. Process query
    processed_query = process_query(query)
    
    # 2. Retrieve documents using hybrid search
    documents = retrieval(query=processed_query, category_ids=category_ids, k=k)
    if not documents:
        return "The provided sources do not contain any information about this subject.", []
    
    # 3. Augment context from documents
    context = augmentation(documents)
    
    # 4. Generate answer using LLM
    response = generation(processed_query, context)
    if "don't have sufficient information to answer" in response:
        documents = []
    return response, documents


def process_query(query: str) -> str:
    return " ".join(query.strip().split())

def retrieval(query: str, category_ids: Optional[List[int]] = None, k: int = 3, score_threshold: float = 0.0) -> List[str]:
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
                filter=query_filter,
                limit=k*2,
            ),
            Prefetch(
                query=SparseVector(**sparse_query_vector.as_object()),
                using="sparse",
                filter=query_filter,
                limit=k*2,
            ),
        ],
        query=FusionQuery(fusion=Fusion.RRF),
        limit=k,
        search_params={
            "hnsw_ef": 100,
        }
    )

    # Aggregate scores for each document ID level
    document_chunks = {}
    for scored_point in search_result.points:
        metadata = scored_point.payload
        document_id = metadata.get("document_id")
        if document_id not in document_chunks:
            document_chunks[document_id] = []
        document_chunks[document_id].append({
            "document_id": document_id,
            "document_name": metadata.get("document_name", "Unknown"),
            "category_name": metadata.get("category_name", "Unknown"),
            "description": metadata.get("description", ""),
            "chunk_id": metadata.get("chunk_id", ""),
            "chunk_content": metadata.get("chunk_content", ""),
            "score": scored_point.score
        })
    
    # Keep the highest score for each document across all its chunks
    documents = []
    for _, chunks in document_chunks.items():
        best_chunk = max(chunks, key=lambda x: x["score"])
        documents.append(best_chunk)
    documents.sort(key=lambda x: x["score"], reverse=True)
    return documents[:k]

def augmentation(documents: List[Dict]) -> str:
    
    context_sections = []
    source_index = 1
    
    for doc in documents: 
        document_name = doc.get("document_name", "Unknown")
        category_name = doc.get("category_name", "Unknown")
        description = doc.get("description", "")
        chunk_id = doc.get("chunk_id", "Unknown")
        score = doc.get("score", "Unknown Score")
        chunk_content = doc.get("chunk_content", "")

        logger.info("Document")
        logger.info(document_name)
        logger.info(score)
        logger.info(chunk_content)

        
        # Format source section
        section = f"""[Source {source_index}]
Category Name: {category_name}
Document Name: {document_name}
Document Description: {description}
Chunk Number: {chunk_id}
Chunk Relevance Score: {score:.2%}
Chunk Content:
{chunk_content}"""

        context_sections.append(section)
        source_index += 1

    # Join all sections with separator
    full_context = "\n\n" + "="*80 + "\n\n".join(context_sections)
    return full_context


def generation(query: str, context: str) -> str:

    # prompt = (
    #     "You are a helpful assistant that answers questions using ONLY the provided sources.\n"
    #     "Instructions:\n"
    #     "1. Answer questions using ONLY information explicitly stated in the sources.\n"
    #     "2. If the answer is NOT in the sources, respond with exactly: \"I don't have sufficient information to answer based on the sources\"\n"
    #     "3. Do NOT use any prior knowledge or data.\n"
    #     "4. Do NOT infer, guess, or extrapolate beyond what is in the sources.\n"
    #     "5. Be concise and direct in your answer.\n"
    # )
    
    messages = [
        {
            "role": "system",
            "content": (
                "You answer questions using ONLY the provided sources.\n"
                "Do NOT use prior knowledge.\n"
                "Do NOT infer or guess.\n"
                "Some sources may be more relevant than others to answer the user's question/query\n"
                "If the answer is not explicitly contained in the sources, respond with exactly: \"I don't have sufficient information to answer\"\n"
            )
        },
        {
            "role": "user",
            "content": f"Sources:\n{context}\n\nQuestion: {query}"
        }
    ]

    try:
        logger.info("Calling LLM for answer generation")
        llm_pipeline = get_llm()
        
        output = llm_pipeline(messages)
        if isinstance(output, list) and len(output) > 0:
            response = output[0].get('generated_text', '')
        else:
            response = str(output)
        
        logger.info(f"Generated response ({len(response)} chars)")
        return response
        
    except Exception as e:
        logger.error(f"LLM generation failed: {e}", exc_info=True)
        return f"Error generating response"