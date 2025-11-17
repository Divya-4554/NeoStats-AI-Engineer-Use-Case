import sys, os
sys.path.insert(0, os.path.dirname(__file__))  # ensure repo root is in Python path

import streamlit as st
from models.llm import get_chat_model
from models.embeddings import get_embeddings
from models.rag import run_rag_pipeline

# Initialize models
chat_model = get_chat_model()
embeddings_model = get_embeddings()

# Streamlit page config
st.set_page_config(
    page_title="NeoStats AI Engineer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    page = st.radio("Go to:", ["Chat", "Instructions"])
    if page == "Chat":
        st.divider()
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.experimental_rerun()

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Instructions page
if page == "Instructions":
    st.title("NeoStats AI Assistant Instructions")
    st.markdown("""
    ## Setup
    This app uses a dummy AI assistant for testing purposes.
    
    Later, you can replace the models in the `models/` folder with your real LangChain + API keys.
    
    ### Usage
    1. Go to the **Chat** page.
    2. Type your question.
    3. Receive a simulated AI answer.
    
    ### Notes
    - The chat history is saved per session.
    - Clear chat history anytime using the sidebar button.
    """)

# Chat page
if page == "Chat":
    st.title("🤖 NeoStats AI Chat")
    
    # Display existing messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.markdown(content)
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Save user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate bot response
        with st.chat_message("assistant"):
            with st.spinner("Generating answer..."):
                response = run_rag_pipeline(prompt, chat_model, embeddings_model)
                st.markdown(response)
        
        # Save bot response
        st.session_state.messages.append({"role": "assistant", "content": response})

