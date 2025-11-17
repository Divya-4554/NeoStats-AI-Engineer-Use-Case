# app.py

import sys
import os
sys.path.append(os.path.dirname(__file__))  # ensures repo root is in Python path

import streamlit as st

# Import from models folder
from models.llm import get_chat_model
from models.embeddings import get_embeddings
from models.rag import run_rag_pipeline

# Streamlit page configuration
st.set_page_config(page_title="NeoStats AI Engineer Assistant", layout="wide")

# Page title and instructions
st.title("NeoStats AI Engineer Assistant")
st.write("Ask questions about your system/network/data, and the AI assistant will respond.")

# User input
user_question = st.text_input("Enter your question:")

# Generate and display answer
if user_question:
    with st.spinner("Generating answer..."):
        # Initialize chat model and embeddings
        chat_model = get_chat_model()
        embeddings_model = get_embeddings()

        # Run RAG pipeline
        answer = run_rag_pipeline(user_question, chat_model, embeddings_model)

        # Display result
        st.subheader("Answer:")
        st.write(answer)
