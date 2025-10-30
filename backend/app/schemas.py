from pydantic import BaseModel
from typing import List

class DocumentBase(BaseModel):
    name: str
    description: str

class DocumentCreate(DocumentBase):
    category_id: int

class Document(DocumentBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True