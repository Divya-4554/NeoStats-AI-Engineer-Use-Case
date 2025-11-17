# app.py

import sys
import os
sys.path.append(os.path.dirname(__file__))  # ensures repo root is in path

import streamlit as st
from models.llm import get_chat_model
from models.embeddings import get_embeddings
from models.rag import run_rag_pipeline

# Page setup
st.set_page_config(page_title="NeoStats AI Assistant", layout="wide")
st.title("NeoStats AI Engineer Assistant")
st.write("Ask questions about your system/network/data, and the AI assistant will respond.")

# User input
user_question = st.text_input("Enter your question:")

if user_question:
    with st.spinner("Generating answer..."):
        chat_model = get_chat_model()
        embeddings_model = get_embeddings()
        answer = run_rag_pipeline(user_question, chat_model, embeddings_model)
        st.subheader("Answer:")
        st.write(answer)

