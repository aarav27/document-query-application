from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas, crud
from .database import engine, Base, get_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/documents", response_model=list[schemas.Document])
async def read_documents(db: AsyncSession = Depends(get_db)):
    return await crud.get_documents(db)

@app.get("/categories", response_model=list[schemas.Category])
async def read_categories(db: AsyncSession = Depends(get_db)):
    return await crud.get_categories(db)