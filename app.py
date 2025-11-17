# app.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from models.llm import get_chat_model
from models.embeddings import get_embeddings
# from models.rag import run_rag_pipeline   # keep this if you implement RAG

# Streamlit page setup
st.set_page_config(page_title="NeoStats AI Assistant", layout="wide")
st.title("NeoStats AI Engineer Assistant")
st.write("Ask questions about your system/network/data, and the AI assistant will respond.")

# User input
user_question = st.text_input("Enter your question:")

if user_question:
    with st.spinner("Generating answer..."):
        chat_model = get_chat_model()           # LLM model
        embeddings_model = get_embeddings()     # dummy embeddings
        # For now, you can just show the embeddings length as a test
        vector = embeddings_model.embed_documents([user_question])
        st.subheader("Embeddings vector (dummy):")
        st.write(vector)
        # If you implement RAG later, use run_rag_pipeline here
