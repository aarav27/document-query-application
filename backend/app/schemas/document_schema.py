from pydantic import BaseModel
from typing import Optional

class DocumentBase(BaseModel):
    name: str
    description: str

class DocumentCreate(DocumentBase):
    category_id: int

class Document(DocumentBase):
    id: int
    category_id: Optional[int]
    s3_document_key: Optional[str] = None
    extracted_text: Optional[str] = None

    class Config:
        orm_mode = True

class DocumentUpload(DocumentBase):
    id: int
    category_id: int
    upload_url: str