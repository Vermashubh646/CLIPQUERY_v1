import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logger import custom_logger
from app.core.handlers import register_exception_handlers


app = FastAPI(title="ClipQuery Backend")

# ── CORS ─────────────────────────────────────────────────────
# Allows frontends / external clients on other origins to call
# this API.  Origins are configured via CORS_ALLOWED_ORIGINS
# in .env (defaults to ["*"] for local dev).
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Human readable
@app.get('/')
def home():
    return {"message": "Welcome to ClipQuery API"}

# Machine readable (for Nginx/Docker to ping)
@app.get('/health')
def health_check():
    return {
        "status": "healthy",
        "api_version": "1.0"
    }



@app.middleware('http')
async def log_requests(request: Request, call_next):
    request_id = uuid.uuid4().hex

    with custom_logger.contextualize(request_id = request_id):
        custom_logger.info(f"Incoming Request: {request.method} {request.url.path}")
        response = await call_next(request)
        custom_logger.info(f"Outgoing Response: Status {response.status_code}")
        return response


# Attach all routes
app.include_router(api_router, prefix="/api")

register_exception_handlers(app)



