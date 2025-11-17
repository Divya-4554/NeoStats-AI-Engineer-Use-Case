# models/embeddings.py
"""
Dummy embedding generator — no external API required.
Produces simple numeric vectors that work with the manual cosine similarity.
"""

def get_embeddings(text_list):
    """
    Returns a list of 1-D numeric embeddings for each text item.
    Designed to be deterministic and somewhat discriminative for simple corpora.
    """
    embeddings = []
    for text in text_list:
        # a slightly richer numeric transform: sum of ordinals times length and number of words
        if not text:
            embeddings.append([0.0])
            continue
        ascii_sum = sum(ord(c) for c in text)
        length = max(1, len(text))
        words = max(1, len(text.split()))
        val = float(ascii_sum * length) / words
        embeddings.append([val])
    return embeddings
