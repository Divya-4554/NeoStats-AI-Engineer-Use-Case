# app.py

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))  # Ensure repo root is in path

import streamlit as st
from models.llm import get_chat_model
from models.embeddings import get_embeddings
from models.rag import run_rag_pipeline

# Streamlit page setup
st.set_page_config(page_title="NeoStats AI Assistant", layout="wide")
st.title("NeoStats AI Engineer Assistant")
st.write("Ask questions about your system/network/data, and the AI assistant will respond.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Enter your question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            chat_model = get_chat_model()
            embeddings_model = get_embeddings()  # fixed alias
            answer = run_rag_pipeline(prompt, chat_model, embeddings_model)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# Sidebar to clear chat
with st.sidebar:
    st.title("Navigation")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()
