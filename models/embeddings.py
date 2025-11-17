# models/embeddings.py

from config.config import settings
from typing import List

try:
    from langchain.embeddings import OpenAIEmbeddings
except Exception:
    OpenAIEmbeddings = None

def get_embeddings_client():
    provider = settings.PROVIDER
    if provider == "openai":
        if OpenAIEmbeddings is None:
            raise RuntimeError("OpenAIEmbeddings not available. Install langchain-openai.")
        return OpenAIEmbeddings(model=settings.EMBEDDING_MODEL, openai_api_key=settings.OPENAI_API_KEY)
    elif provider in ("groq", "google", "gemini"):
        raise NotImplementedError(f"{provider} embeddings not implemented")
    else:
        raise RuntimeError(f"Unsupported provider for embeddings: {provider}")

# Add this wrapper so app.py import works
def get_embeddings():
    """Alias for get_embeddings_client for backward compatibility."""
    return get_embeddings_client()

def embed_texts(texts: List[str]) -> List[List[float]]:
    client = get_embeddings_client()
    try:
        return client.embed_documents(texts)
    except Exception:
        if hasattr(client, "embed"):
            return client.embed(texts)
        raise
