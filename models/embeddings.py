from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  # store key in config/config.py

def get_embeddings(text_list):
    """
    Generates embeddings for a list of text documents.
    Returns a list of embedding vectors.
    """
    embeddings = []
    for text in text_list:
        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",  # or use "text-embedding-3-large"
                input=text
            )
            embeddings.append(response.data[0].embedding)
        except Exception as e:
            print(f"Error generating embedding: {e}")
            embeddings.append(None)
    return embeddings
