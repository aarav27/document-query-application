from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

categories = [
    {"category": "Legal", "document_ids": [1, 2]},
    {"category": "Projects", "document_ids": [3]},
    {"category": "Research Papers", "document_ids": [4, 5]}
]

documents = [
    {"id": 1, "name": "Contract 1", "description": "A", "category": "Legal"},
    {"id": 2, "name": "Contract 2", "description": "B", "category": "Legal"},
    {"id": 3, "name": "New Project", "description": "C", "category": "Projects"},
    {"id": 4, "name": "New Study", "description": "D", "category": "Research Papers"},
    {"id": 5, "name": "Old Study", "description": "E", "category": "Research Papers"},
]

@app.get("/documents")
def get_documents():
    return documents

@app.get("/categories")
def get_categories():
    return categories