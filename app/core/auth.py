from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key: str = Security(api_key_header)) -> str:
    """Dependency that checks if the provided API key is valid."""
    
    # Split the comma-separated string from config into a list of valid keys
    valid_keys = [k.strip() for k in settings.VALID_API_KEYS.split(",")]
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key. Please provide 'X-API-Key' in the header."
        )
        
    if api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key."
        )
        
    return api_key