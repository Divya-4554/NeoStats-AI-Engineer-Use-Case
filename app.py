# app.py

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))  # ensures repo root is in Python path

import streamlit as st
from models.llm import get_chat_model
from models.embeddings import get_embeddings as embeddings
from models.rag import run_rag_pipeline

# Streamlit page setup
st.set_page_config(page_title="NeoStats AI Assistant", layout="wide")
st.title("NeoStats AI Engineer Assistant")
st.write("Ask questions about your system/network/data, and the AI assistant will respond.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    with st.chat_message(role):
        st.markdown(content)

# User input
if prompt := st.chat_input("Enter your question:"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            chat_model = get_chat_model()
            embeddings_model = embeddings()  # call alias function
            answer = run_rag_pipeline(prompt, chat_model, embeddings_model)
            st.markdown(answer)
            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})

# Sidebar for clearing chat
with st.sidebar:
    st.title("Navigation")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()
