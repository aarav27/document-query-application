from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str
    category_ids: list[int] | None = None