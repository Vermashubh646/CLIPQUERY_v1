from app.services.search_from_db.search_pinecone import query_from_retriever
from app.schemas.models import SearchQuery, ClipResult, SearchResponse
from fastapi import APIRouter

router = APIRouter()

@router.post('/query', response_model=SearchResponse)
async def query_db(search_query: SearchQuery):
    docs = await query_from_retriever(search_query.query, search_query.user_id, search_query.max_results)
    results = [
        ClipResult(
            video_name=doc.metadata.get("video_name", ""),
            start_time=doc.metadata.get("start_time", 0.0),
            end_time=doc.metadata.get("end_time", 0.0),
            narrative=doc.page_content,
            video_url=doc.metadata.get("video_url", ""),
            score=doc.metadata.get("score", 0.0),
        )
        for doc in docs
    ]
    return SearchResponse(results=results)