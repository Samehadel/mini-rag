from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE_MB: int
    FILE_DEFAULT_CHUNCK_SIZE: int

    MONGODB_URL: str
    MONGODB_DATABASE: str

    # LLM Config
    GENERATION_PROVIDER: str
    EMBEDDING_PROVIDER: str
    EMBDDING_SIZE: int
    
    GENERATION_MODEL_ID: str
    EMBEDDING_MODEL_ID: str

    OPENAI_API_KEY: str
    COHERE_API_KEY: str

    # Vector DB Config
    VECTOR_DB_PROVIDER: str
    QDRANT_DB_PATH: str
    DISTANCE_METHOD: str
    
    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()