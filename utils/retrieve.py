# utils/retrieve.py
import numpy as np

def cosine_similarity_manual(a, b):
    """Compute cosine similarity between two 1-D vectors (lists/ndarrays)."""
    a = np.array(a, dtype=float).ravel()
    b = np.array(b, dtype=float).ravel()
    if a.size == 0 or b.size == 0:
        return 0.0
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    if a_norm == 0 or b_norm == 0:
        return 0.0
    return float(np.dot(a, b) / (a_norm * b_norm))


def retrieve_docs(query, docs, doc_embeddings, top_k=3, similarity_threshold=0.3):
    """
    Retrieve top_k most relevant documents for a query.
    - query: user query string
    - docs: list of document strings (same order as doc_embeddings)
    - doc_embeddings: list of numeric vectors (e.g., returned by get_embeddings)
    - top_k: number of docs to return (max)
    - similarity_threshold: minimum cosine similarity to consider a doc relevant
    Returns: list of top documents (strings). Returns [] if none pass threshold.
    """
    try:
        # Handle edge cases
        if not query or not docs or not doc_embeddings:
            return []

        # Create dummy embedding for query, same transform as models/embeddings.get_embeddings
        ascii_sum = sum(ord(c) for c in query)
        length = max(1, len(query))
        words = max(1, len(query.split()))
        query_emb = [float(ascii_sum * length) / words]

        # compute similarities
        similarities = [cosine_similarity_manual(query_emb, emb) for emb in doc_embeddings]

        # If best similarity below threshold, return empty to trigger fallback
        if len(similarities) == 0 or max(similarities) < similarity_threshold:
            return []

        # pick top_k indices (highest similarity)
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        top_docs = [docs[int(i)] for i in top_indices]
        return top_docs

    except Exception as e:
        print("Error in retrieve_docs:", e)
        return []
