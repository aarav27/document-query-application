from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.rag.search import semantic_search
from app.schemas import document_schema, search_schema
from app.services.document_service import get_documents, get_documents_all

search_router = APIRouter()

@search_router.post(
    "/",
    summary="Perform document search given a search query",
    response_model=list[document_schema.Document]
)
async def document_search(search_request : search_schema.SearchRequest, db: AsyncSession = Depends(get_db)):
    if search_request.category_id is None:
         documents : list[document_schema.Document] = await get_documents_all(db)
    else:
        documents : list[document_schema.Document] = await get_documents(search_request.category_id, db)
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found")
    return semantic_search(search_request.query, documents)
