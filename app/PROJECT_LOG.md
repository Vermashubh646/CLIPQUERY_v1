# ClipQuery - Development Log

> **Note for new LLM sessions:** This file tracks all the features implemented, bugs fixed, and architectural choices made in this specific branch of development. Refer to this to understand the current state of the backend before suggesting changes.
> 
> **CRUCIAL AGENT INSTRUCTION:** The user is actively learning and building their backend skills. **DO NOT** just write full code files or "throw code" at them. They strictly prefer to be given logic explanations and coding "challenges" where you outline *what* needs to be done (e.g., "Write a function that does HTTP 401 on failure"), so they can write the actual Python syntax themselves. Only provide exact code snippets when introducing a brand new library or complex framework concept (like FastAPI Dependency Injection or Pytest clients). Start completely new tasks with a planning artifact!

## ✅ Accomplished Features
The following features from `MUST_HAVES.txt` and the mentor's schedule have been fully implemented and verified:

1. **CORS Middleware (Point 2)**
   - Added `CORSMiddleware` to `main.py`.
   - Allowed origins are securely loaded from `settings.CORS_ALLOWED_ORIGINS` via environment variables.

2. **Global Error Handling (Point 3)**
   - Created custom Python exceptions: `VideoFormatError`, `ProcessingError`, `StorageError`, `VectorDBError`.
   - Built a FastAPI global exception handler in `core/handlers.py` to intercept these errors and return clean JSON responses (preventing raw stack traces in production).

3. **Fixed Upload Endpoint Bugs (Point 8)**
   - Implemented a fast 50MB file size limit reader (`check_size_limit`).
   - Implemented `startswith("video/")` MIME type validation blocking text/executable files.
   - Guarded temporary file saving with `try/finally` blocks ensuring `os.remove()` and `shutil.rmtree()` always clean up dropped uploads.

4. **User-Scoped Search Architecture (Point 9)**
   - Refactored the architecture mentally to be a Multi-Tenant Master DB.
   - Piped `user_id` and `public_listing` via LangChain `RunnableLambda(lambda x: x['key'])` through the complex orchestrator into Pinecone Document metadata.
   - Updated the `SearchQuery` Pydantic model to require `user_id`.
   - Overhauled `search_pinecone.py` to use a dynamic factory that injects a MongoDB-style `$or` metadata filter into the LangChain Retriever, ensuring users only retrieve videos they own OR videos marked public.

5. **Basic Smoke Tests (Buffer Day Schedule)**
   - Validated the endpoints by writing automated HTTP tests using `pytest` and FastAPI's `TestClient` in `tests/test_api.py`.
   - Tested the `404 Not Found` for fake Job IDs, the `422 Unprocessable` for missing `user_id` in search, and the `400 Bad Request` for non-video file uploads.

6. **API Key Authentication (Point 6)**
   - Configured `VALID_API_KEYS` inside `core/config.py`.
   - Generated a FastAPI Security Dependency (`APIKeyHeader`) in `core/auth.py` that intercepts the `X-API-Key` header, validating it against the configured string list.
   - Locked the global router (`app/api/v1/router.py`) using `Depends(get_api_key)`.
   - Added tests ensuring `401 Unauthorized` for missing or invalid keys.
   - This automatically integrated a security padlock into the `/docs` Swagger UI.

7. **Background Tasks & Job Tracking (Day 2 Schedule)**
   - Explored `ingest.py` and confirmed `BackgroundTasks` was already flawlessly implemented to return immediate HTTP responses while processing video sequentially.
   - Mapped out the `jobs` in-memory dictionary tracking `processing` -> `completed` -> `failed` states.
   - Verified the `GET /api/videos/get_status/{job_id}` endpoint.

---

## 🚧 Currently Working On (Day 3 / Point 10)
**Structured Logging + Requirements Finalization**
- We are actively replacing `print()` statements with the `loguru` library.
- **Next steps**: 
  - Build a FastAPI Middleware (`@app.middleware`) to generate UUIDs for every incoming request.
  - Bind these Request IDs to `loguru` so we can trace specific user requests cleanly in production.
  - Finalize `requirements.txt`.
