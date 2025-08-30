from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/ai_core"
    VECTOR_EMBEDDING_MODEL: str = "text-embedding-3-large"
    LLM_MODEL: str = "gpt-4o-mini"
    ENV: str = "dev"

    class Config:
        env_file = ".env"

settings = Settings()
