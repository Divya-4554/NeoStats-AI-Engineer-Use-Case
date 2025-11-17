import streamlit as st

from models.embeddings import get_embeddings
from models.llm import get_chat_model
from utils.retrieve import retrieve_docs
from utils.web_search import web_search

# --------------------------------------------------
# Page Title
# --------------------------------------------------
st.title("NeoStats AI Engineer Assistant")

# --------------------------------------------------
# Local Dummy Documents (RAG Corpus)
# --------------------------------------------------
docs = [
    "NeoStats provides AI-powered analytics for IT and engineering teams.",
    "Streamlit allows fast deployment of AI, ML, and data applications.",
    "RAG integrates local documents with LLMs to provide contextual answers."
]

# Compute embeddings once
doc_embeddings = get_embeddings(docs)

# --------------------------------------------------
# UI Elements
# --------------------------------------------------
mode = st.radio("Response Mode", ["Concise", "Detailed"])
query = st.text_input("Enter your question:")

# Load Dummy LLM Model (from models/llm.py)
llm = get_chat_model()

# --------------------------------------------------
# Ask Button Logic
# --------------------------------------------------
if st.button("Ask"):

    if not query.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:
        # Step 1: Retrieve relevant local documents (RAG)
        top_docs = retrieve_docs(query, docs, doc_embeddings)

        if top_docs:
            context = "\n".join(top_docs)
        else:
            # Step 2: Fallback → Web Search Tool
            web_results = web_search(query)
            if web_results:
                context = "\n".join(web_results)
            else:
                context = "No relevant document or web result found."

        # Step 3: LLM generates final response
        prompt = f"User Query: {query}\nContext:\n{context}"
        final_response = llm(prompt, mode)

        # Output
        st.write(final_response)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
