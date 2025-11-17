# utils/retrieve.py
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def retrieve_docs(query, docs, doc_embeddings, top_k=3):
    """
    Retrieve top_k most relevant documents to a query using dummy embeddings.
    """
    try:
        # Convert query to dummy embedding
        query_embedding = [sum(ord(c) for c in query)]
        # Compute cosine similarity
        sims = cosine_similarity([query_embedding], doc_embeddings)[0]
        top_indices = sims.argsort()[-top_k:][::-1]
        top_docs = [docs[i] for i in top_indices]
        return top_docs
    except Exception as e:
        print(f"Error in retrieve_docs: {e}")
        return []
