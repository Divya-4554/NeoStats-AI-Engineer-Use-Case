# utils/retrieve.py
import numpy as np

def cosine_similarity_manual(a, b):
    """Manual cosine similarity without sklearn."""
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)

    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_docs(query, docs, doc_embeddings, top_k=3):
    """Retrieve most relevant documents using manual cosine similarity."""
    try:
        query_emb = [sum(ord(c) for c in query) * len(query)]

        similarities = [
            cosine_similarity_manual(query_emb, emb)
            for emb in doc_embeddings
        ]

        top_indices = np.argsort(similarities)[-top_k:][::-1]

        top_docs = [docs[i] for i in top_indices]
        return top_docs

    except Exception as e:
        print("Error in retrieve_docs:", e)
        return []
