from pydantic import BaseModel
from typing import Optional

class DocumentBase(BaseModel):
    name: str
    description: str
    category_id: int
    s3_document_key: str

class DocumentCreate(DocumentBase):
    category_name: str

class DocumentDownloadRequest(BaseModel):
    name: str
    s3_document_key: str

class DocumentUploadRequest(BaseModel):
    name: str

class Document(DocumentBase):
    id: int
    class Config:
        orm_mode = True