from app.services.search_from_db.search_pinecone import query_from_retriever
from fastapi import APIRouter

router = APIRouter()

@router.get('/query')
async def query_db(query: str):
    return await query_from_retriever(query)