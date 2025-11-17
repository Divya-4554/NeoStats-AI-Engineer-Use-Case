import streamlit as st
from models.llm import get_chat_model
from models.embeddings import get_vector_store
from utils.rag_pipeline import rag_answer

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="NeoStats AI Engineer Assistant", layout="wide")

# -----------------------------
# INIT SESSION STATE
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "Concise"

# -----------------------------
# HEADER
# -----------------------------
st.title("🤖 NeoStats AI Engineer Assistant")

# -----------------------------
# RESPONSE MODE TOGGLE
# -----------------------------
col1, col2 = st.columns([4, 2])
with col2:
    st.session_state.mode = st.radio(
        "Response Mode",
        ["Concise", "Detailed"],
        horizontal=True
    )

# -----------------------------
# CLEAR CHAT HISTORY
# -----------------------------
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.experimental_rerun()

# -----------------------------
# CHAT DISPLAY AREA
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# USER INPUT BOX (ChatGPT Style)
# -----------------------------
query = st.chat_input("Enter your question...")

# -----------------------------
# PROCESS USER INPUT
# -----------------------------
if query:
    # append user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Load model + vector store
    llm = get_chat_model()
    vector_store = get_vector_store()

    # Generate RAG response
    answer = rag_answer(query, llm=llm, vector_store=vector_store, mode=st.session_state.mode)

    # append bot message
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # display bot message
    with st.chat_message("assistant"):
        st.markdown(answer)

