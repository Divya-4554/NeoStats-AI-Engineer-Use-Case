def run_rag_pipeline(question, chat_model, embeddings_model):
    """Dummy RAG pipeline: returns the chat model response"""
    return chat_model.invoke([{"content": question}]).content
