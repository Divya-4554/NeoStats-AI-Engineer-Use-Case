# models/embeddings.py

from config.config import settings
from typing import List

# Explicit OpenAI import to avoid Streamlit errors
try:
    from langchain.embeddings.openai import OpenAIEmbeddings
except Exception:
    OpenAIEmbeddings = None

def get_embeddings_client():
    provider = settings.PROVIDER.lower()
    if provider == "openai":
        if OpenAIEmbeddings is None:
            raise RuntimeError(
                "OpenAIEmbeddings not available. Ensure `langchain` and `openai` packages are installed."
            )
        return OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
    elif provider == "groq":
        raise NotImplementedError("Groq embeddings not implemented in this template.")
    elif provider in ("google", "gemini"):
        raise NotImplementedError("Google embeddings not implemented in this template.")
    else:
        raise RuntimeError(f"Unsupported provider for embeddings: {provider}")

def embed_texts(texts: List[str]) -> List[List[float]]:
    client = get_embeddings_client()
    try:
        return client.embed_documents(texts)
    except Exception:
        if hasattr(client, "embed"):
            return client.embed(texts)
        raise
