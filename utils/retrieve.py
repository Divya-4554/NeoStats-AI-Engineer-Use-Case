import numpy as np

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def retrieve_docs(query, docs, embeddings):
    query_emb = [sum(ord(c) for c in query)]

    scored = []
    for idx, emb in enumerate(embeddings):
        sim = cosine_similarity(query_emb, emb)
        scored.append((sim, docs[idx]))

    scored.sort(reverse=True)

    top = [doc for sim, doc in scored[:2] if sim > 0]
    return top
