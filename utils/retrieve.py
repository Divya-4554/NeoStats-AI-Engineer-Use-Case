import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def retrieve_docs(query, docs, doc_embeddings, top_k=3, query_embedding=None):
    """
    Retrieve top_k most relevant documents to a query.
    """
    try:
        if query_embedding is None:
            from models.embeddings import get_embeddings
            query_embedding = get_embeddings([query])[0]

        sims = cosine_similarity([query_embedding], doc_embeddings)[0]
        top_indices = sims.argsort()[-top_k:][::-1]
        top_docs = [docs[i] for i in top_indices]
        return top_docs
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return []

