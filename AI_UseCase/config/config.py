# config/config.py
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    PROVIDER: str = os.getenv("PROVIDER", "openai").lower()
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.05"))
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "800"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "100"))

settings = Settings()

def validate_for_provider():
    p = settings.PROVIDER
    if p == "openai" and not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required when PROVIDER=openai")
    if p == "groq" and not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is required when PROVIDER=groq")
    if p in ("google", "gemini") and not settings.GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is required when PROVIDER=google")
