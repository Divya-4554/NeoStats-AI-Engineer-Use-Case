# models/embeddings.py

def get_embeddings(text_list):
    """
    Dummy embeddings without API.
    More meaningful than single sum → improves retrieval.
    """
    embeddings = []
    for text in text_list:
        emb = sum(ord(c) for c in text) * len(text)
        embeddings.append([emb])  # 1D vector
    return embeddings
