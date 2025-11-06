from pydantic import BaseModel
from typing import List, Optional

class DocumentBase(BaseModel):
    name: str
    description: str

class DocumentCreate(DocumentBase):
    category_id: int

class Document(DocumentBase):
    id: int
    category_id: int
    s3_document_key: Optional[str] = None

    class Config:
        orm_mode = True

class DocumentUpload (DocumentBase):
    id: int
    category_id: int
    upload_url: str


class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True