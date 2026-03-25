from fastapi import APIRouter, Depends
from app.api.v1.endpoints import ingest,search
from app.core.auth import get_api_key

api_router = APIRouter(dependencies=[Depends(get_api_key)])

api_router.include_router(
    ingest.router,
    prefix="/videos",
    tags=["Videos"]
)

api_router.include_router(
    search.router,
    prefix="/search",
    tags=["Search"]
)
