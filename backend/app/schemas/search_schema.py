from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str
    category_id: int | None = None