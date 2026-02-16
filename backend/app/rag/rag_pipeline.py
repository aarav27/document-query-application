import logging
from typing import List, Optional

from app.rag.document_pipeline import chroma_db
from app.rag.models import get_phi_llm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def qna_pipeline(query: str, category_ids: list[int] | None = None):
    processed_query = process_query(query)
    documents, scores = retrieval(processed_query, category_ids)
    logging.info(scores)
    context = augmentation(documents)
    response = generation(processed_query, context)
    return response, documents, scores

def process_query(query):
    return query.lower().strip().replace("\n", " ")

def retrieval(query: str, category_ids: Optional[List[int]] = None, k: int = 3):
    filter_dict = None
    if category_ids:
        filter_dict = {"category_id": {"$in": category_ids}}

    results = chroma_db.similarity_search_with_score(
        query,
        k,
        filter=filter_dict
    )

    documents, scores = zip(*results)
    return documents, scores

# TODO: Add category name to metadata
def augmentation(documents):
    if not documents:
        return ""

    context_sections = []
    for i, doc in enumerate(documents):
        content = doc.page_content if hasattr(doc, "page_content") else str(doc)
        metadata = getattr(doc, "metadata", {})

        document_name = metadata.get("document_name", "Unknown")
        description = metadata.get("description", "")
        chunk_id = metadata.get("chunk_id", "Unknown")

        section = f"""
            [Source {i+1}]
            Document Name: {document_name}
            Chunk ID: {chunk_id}
            Description: {description}

            Content Chunk:
            {content}
            """

        context_sections.append(section)

    full_context = "\n\n---\n\n".join(context_sections)
    return full_context


def generation(query, context):
    llm_prompt = f"""
        You are a helpful assistant that answers **only from retrieved knowledge**.
        Retrieved information is the **only source of truth**.

        ## Core Rules
        - **Never guess, infer, or rely on prior knowledge.**
        - **Never fill gaps** with reasoning or external knowledge.
        - Make **no logical leaps** — even if a connection seems obvious.
        - Treat each retrieved context as **independent**; combine only if they reference the same entity by name.
        - Treat entities as related **only if the relationship is explicitly stated**.
        - **Do not infer, assume, or deduce** compatibility, membership, or relationships between entities or components.
        - Some document chunks given may be more relevant than others to answer the user's question/query

        ## Answering & Formatting
        - Provide concise and factual answers **without speculation or synthesis**.
        - Avoid boilerplate introductions and justifications.
        - **If the context does not explicitly answer the question, state that the information is unavailable.**
        - Do not include references, footnotes or citations unless explicitly requested.
        - Use Markdown formatting to improve readability.
        - Use MathJax for mathematical or scientific notation: $...$ for inline, $$...$$ for block; avoid other delimiters.

        ## Process
        1. Retrieve context before answering; use short, focused queries.
        2. For multi-part questions, handle each part separately while applying all rules.
        3. If the user's question conflicts with retrieved data, trust the data and note the discrepancy.
        4. If sources conflict, do not merge or reinterpret — report the discrepancy.
        5. If coverage is incomplete or unclear, explicitly state that the information is missing.

        ## Final Reinforcement
        Always prefer **accuracy over completeness**.
        If uncertain, clearly state that the information is missing.
        
        ## Question/Query
        A user wants to know about {query}. Shorten this user query to its core meaning. 
        Then use the extracted passages from our knowledge base (below) to form the best answer you can. 
        Context/Knowledge Base: {context}
    """

    llm_pipeline = get_phi_llm()
    response = llm_pipeline(llm_prompt)
    return response


