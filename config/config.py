# config/config.py
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

@dataclass
class Settings:
    PROVIDER: str = os.getenv("PROVIDER", "openai")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))

settings = Settings()

def validate_for_provider():
    p = settings.PROVIDER.lower()
    if p == "openai" and not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required when PROVIDER=openai")
    if p == "groq" and not settings.GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is required when PROVIDER=groq")
    if p in ("google", "gemini") and not settings.GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is required when PROVIDER=google")
