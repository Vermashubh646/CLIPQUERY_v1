from app.main import app
from fastapi.testclient import TestClient
from app.core.config import settings

client = TestClient(app)
client.headers.update({"X-API-Key": settings.VALID_API_KEYS})

def test_status_endpoint_not_found():
    """Smoke Test 1: Querying a fake Job ID should correctly return a 404 error."""
    response = client.get("/api/videos/get_status/fake-job-id-123")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Job ID not found"}


def test_search_requires_user_id():
    """Smoke Test 2: Not providing user_id along with query for querying db should return error."""

    payload={"query":"A smiling old man"}
    response = client.post("/api/search/query", json=payload)
    
    # 422 Unprocessable Entity
    assert response.status_code == 422
    assert "user_id" in response.text

def test_upload_rejects_non_video_file():
    """Smoke Test 3: Uploading a non video file should return error."""

    fake_file_content = b"Hello, I am a secret text file trying to sneak in."
    files = {
       "file": ("sneaky.txt", fake_file_content, "text/plain")
    }
    
    response = client.post("/api/videos/upload?USER_ID=123&public_listing=false", files=files)
    
    assert response.status_code == 400
    assert "Video Format Error" in response.text


def test_missing_api_key():
    """Smoke Test 4: Querying a fake Job ID without api key should correctly return a 401 error."""
    response = client.get("/api/videos/get_status/fake-job-id-123", headers={"X-API-Key":""})
    
    assert response.status_code == 401
    assert "Missing API Key" in response.text

def test_auth_invalid_key():
    """Smoke Test 5: Querying a fake Job ID with wrong api key should correctly return a 401 error."""
    response = client.get("/api/videos/get_status/fake-job-id-123", headers={"X-API-Key":"sdf15df"})
    
    assert response.status_code == 401
    assert "Invalid API Key" in response.text