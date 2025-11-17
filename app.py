import sys
import os

# Fix Python path so Streamlit can find models folder
repo_root = os.path.dirname(os.path.abspath(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import streamlit as st

# Import models after fixing path
from models.llm import get_chat_model
from models.embeddings import get_embeddings
from models.rag import run_rag_pipeline

# Streamlit UI
st.set_page_config(page_title="NeoStats AI Assistant", layout="wide")
st.title("NeoStats AI Engineer Assistant")
st.write("Ask questions about your system/network/data, and the AI assistant will respond.")

chat_model = get_chat_model()
embeddings_model = get_embeddings()

user_question = st.text_input("Enter your question:")

if user_question:
    with st.spinner("Generating answer..."):
        answer = run_rag_pipeline(user_question, chat_model, embeddings_model)
        st.subheader("Answer:")
        st.write(answer)
