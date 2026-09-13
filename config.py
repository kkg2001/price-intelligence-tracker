import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key: str
    groq_model : str = "openai/gpt-oss-120b"

    database_file: str = "price_intelligence.db"
    vector_db_dir: str = "chroma_db"
    knowledge_file: str = "data/product_knowledge.csv"
    api_url: str = "http://127.0.0.1.8000"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

def get_secret_from_docker():
    secret_path = "/run/secrets/groq_api_key"
    if os.path.exists(secret_path):
        with open(secret_path,"r",encoding = "utf-8") as file:
            return file.read().strip()
    return None

def get_settings():
    docker_secret=get_secret_from_docker()
    if docker_secret:
        return Settings(groq_api_key=docker_secret)
    return Settings()

settings = get_settings()

