# models/embeddings.py

def get_embeddings(text_list):
    """
    Returns dummy embeddings for testing without any API.
    Each text becomes a simple numeric vector based on ASCII sum.
    """
    embeddings = []
    for text in text_list:
        embeddings.append([sum(ord(c) for c in text)])  # simple numeric vector
    return embeddings
