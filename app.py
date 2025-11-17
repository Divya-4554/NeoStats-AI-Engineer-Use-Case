# app.py

import streamlit as st
from models.llm import get_chat_model
from models.embeddings import get_embeddings
from typing import List

# ------------------------------
# Dummy RAG documents
# ------------------------------
DOCS = {
    "doc1": "NeoStats AI helps analyze system and network data efficiently.",
    "doc2": "The chatbot can retrieve knowledge from local documents and answer intelligently."
}

# ------------------------------
# Dummy RAG retrieval function
# ------------------------------
def retrieve_from_docs(query: str, top_k: int = 1) -> List[str]:
    """
    Returns top_k document chunks containing the query word.
    Dummy implementation: returns first top_k docs containing any word from query.
    """
    results = []
    for doc in DOCS.values():
        if any(word.lower() in doc.lower() for word in query.split()):
            results.append(doc)
        if len(results) >= top_k:
            break
    if not results:
        results = ["No relevant document found."]  # fallback
    return results

# ------------------------------
# Chat response
# ------------------------------
def get_chat_response(chat_model, embeddings_model, query: str, mode: str = "Concise") -> str:
    """
    Generates a response using dummy logic and retrieved documents.
    """
    retrieved_docs = retrieve_from_docs(query)
    doc_text = " ".join(retrieved_docs)

    # Dummy embeddings vector print
    vec = embeddings_model.embed_documents([query])
    st.write("Embeddings vector (dummy):", vec)

    # Dummy response logic
    if mode == "Concise":
        response = f"Concise answer: {doc_text[:60]}..."
    else:
        response = f"Detailed answer:\n{doc_text}\n\nFurther explanation based on your question: {query}"

    return response

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="NeoStats AI Assistant", layout="wide")
st.title("NeoStats AI Engineer Assistant")
st.write("Ask questions about your system/network/data, and the AI assistant will respond.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Response mode selector
mode = st.radio("Response Mode", ["Concise", "Detailed"], index=0)

# User input
query = st.text_input("Enter your question:")

if query:
    chat_model = get_chat_model()
    embeddings_model = get_embeddings()

    # Get response
    response = get_chat_response(chat_model, embeddings_model, query, mode)

    # Display messages
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "assistant", "content": response})

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Clear chat
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.experimental_rerun()
