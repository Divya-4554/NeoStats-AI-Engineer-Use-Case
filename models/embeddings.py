# models/embeddings.py
from typing import List

# Dummy embeddings class for testing without API key
class DummyEmbeddings:
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Return a simple numeric vector for each text
        return [[float(len(t))] for t in texts]

def get_embeddings_client():
    """Return dummy embeddings client for testing."""
    print("⚠️ Using DummyEmbeddings because no API key is provided.")
    return DummyEmbeddings()

# Alias for app.py
def get_embeddings():
    return get_embeddings_client()
