from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    LLM_PROVIDER: str
    
    OPENAI_API_KEY: str
    OPENAI_GENERATION_MODEL: str
    OPENAI_EMBEDDING_MODEL: str

    # Cohere settings (optional)
    COHERE_API_KEY: str | None = None
    COHERE_GENERATION_MODEL: str | None = None
    COHERE_EMBEDDING_MODEL: str | None = None

    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE_MB: int
    FILE_DEFAULT_CHUNCK_SIZE: int

    MONGODB_URL: str
    MONGODB_DATABASE: str
    
    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()