from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    GROQ_API_KEY: SecretStr
    PINECONE_API_KEY: SecretStr
    HUGGINGFACEHUB_ACCESS_TOKEN: SecretStr
    AWS_ACCESS_KEY_ID: SecretStr
    AWS_SECRET_ACCESS_KEY: SecretStr
    AWS_REGION: str         
    S3_BUCKET_NAME: str
    CORS_ALLOWED_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"                

settings = Settings() #type:ignore      