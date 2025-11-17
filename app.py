# app.py
import streamlit as st
from models.embeddings import get_embeddings
from utils.retrieve import retrieve_docs
from utils.web_search import web_search

st.title("NeoStats AI Engineer Assistant")

# Dummy local documents
docs = [
    "NeoStats provides AI-powered analytics for IT teams.",
    "Streamlit allows fast deployment of ML and AI apps.",
    "RAG integrates local documents with LLMs for better responses."
]

# Compute dummy embeddings
doc_embeddings = get_embeddings(docs)

# Response mode
mode = st.radio("Response Mode", ["Concise", "Detailed"])

# User input
query = st.text_input("Enter your question:")

if st.button("Ask"):
    try:
        # Retrieve relevant docs
        top_docs = retrieve_docs(query, docs, doc_embeddings)

        if top_docs:
            context = "\n".join(top_docs)
            response = f"Based on retrieved documents:\n{context}"
        else:
            # Fallback to mock web search
            web_results = web_search(query)
            context = "\n".join(web_results)
            response = f"Based on web search results:\n{context}"

        # Adjust response based on mode
        if mode == "Concise":
            response += "\n\n[Concise Answer Mode]"
        else:
            response += "\n\n[Detailed Answer Mode]"

        st.write(response)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
