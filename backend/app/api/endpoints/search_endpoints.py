from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.rag.search import hybrid_search
from app.schemas import document_schema, search_schema
from app.services.document_service import get_documents_by_ids

search_router = APIRouter()

@search_router.post(
    "/",
    summary="Perform document search given a search query",
    response_model=list[document_schema.Document]
)
async def document_search(search_request : search_schema.SearchRequest, db: AsyncSession = Depends(get_db)):
    document_ids : list[int] = hybrid_search(search_request.query, search_request.category_ids)
    documents = await get_documents_by_ids(document_ids, db)
    return documents
    
