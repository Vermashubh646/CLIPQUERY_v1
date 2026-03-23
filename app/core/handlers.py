from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from .exceptions import VideoFormatError, ProcessingError, StorageError, VectorDBError


def register_exception_handlers(app: FastAPI):
    
    @app.exception_handler(VideoFormatError)
    async def video_format_error_handler(request: Request, exc: VideoFormatError):
        return JSONResponse(
            status_code=400,
            content={"detail": f"Video Format Error: {str(exc)}"},
        )
    
    @app.exception_handler(ProcessingError)
    async def processing_error_handler(request: Request, exc: ProcessingError):
        return JSONResponse(
            status_code=400,
            content={"detail": f"Video Processing Error: {str(exc)}"},
        )
    
    @app.exception_handler(StorageError)
    async def storage_error_handler(request: Request, exc: StorageError):
        return JSONResponse(
            status_code=400,
            content={"detail": f"Storage Error: {str(exc)}"},
        )
    
    @app.exception_handler(VectorDBError)
    async def vector_DB_error_handler(request: Request, exc: VectorDBError):
        return JSONResponse(
            status_code=400,
            content={"detail": f"Vector DB Error: {str(exc)}"},
        )