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

records = [
    {"document_name": "New Contract", "category": "Legal"},
    {"document_name": "New Project", "category": "Projects"},
    {"document_name": "New Study", "category": "Research Papers"},
]

@app.get("/records")
def get_records():
    return records