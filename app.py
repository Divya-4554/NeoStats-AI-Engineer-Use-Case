import streamlit as st
from models.embeddings import get_embeddings
from models.llm import get_chat_model
from utils.retrieve import retrieve_docs
from utils.web_search import web_search

# --------------------------------------------------
# APP TITLE
# --------------------------------------------------
st.title("NeoStats AI Engineer Assistant")

# --------------------------------------------------
# Initialize Chat History
# --------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# --------------------------------------------------
# Dummy Local RAG Documents
# --------------------------------------------------
docs = [
    "NeoStats provides AI-powered analytics for IT and engineering teams.",
    "Streamlit allows fast deployment of AI, ML, and data applications.",
    "RAG integrates local documents with LLMs to provide contextual answers."
]

# Precompute embeddings
doc_embeddings = get_embeddings(docs)

# --------------------------------------------------
# UI Controls
# --------------------------------------------------
mode = st.radio("Response Mode", ["Concise", "Detailed"])
query = st.text_input("Enter your question:")

# Load Dummy LLM
llm = get_chat_model()

# --------------------------------------------------
# Clear Chat Button
# --------------------------------------------------
if st.button("Clear Chat"):
    st.session_state.history = []
    st.experimental_rerun()

# --------------------------------------------------
# Ask Button Logic
# --------------------------------------------------
if st.button("Ask"):

    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:
        # Step 1: RAG Retrieval
        top_docs = retrieve_docs(query, docs, doc_embeddings)

        if top_docs:
            context = "\n".join(top_docs)
        else:
            # Step 2: Fallback to Web Search
            web_results = web_search(query)
            context = "\n".join(web_results) if web_results else "No relevant information found."

        # Step 3: LLM Response
        prompt = f"User Query: {query}\nContext:\n{context}"
        final_response = llm(prompt, mode)

        # Store in chat history
        st.session_state.history.append({"user": query, "bot": final_response})

    except Exception as e:
        st.error(f"Something went wrong: {e}")

# --------------------------------------------------
# Chat History Display
# --------------------------------------------------
st.subheader("Chat History")

if st.session_state.history:
    for chat in st.session_state.history:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**Assistant:** {chat['bot']}")
        st.markdown("---")
else:
    st.write("Start asking questions to build chat history.")
