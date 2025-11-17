import streamlit as st
from models.embeddings import get_embeddings
from utils.retrieve import retrieve_docs
from utils.web_search import web_search

st.title("NeoStats AI Engineer Assistant")

# Dummy local documents
docs = [
    "NeoStats provides AI-powered analytics for IT and engineering teams.",
    "Streamlit allows fast deployment of AI, ML, and data applications.",
    "RAG integrates local documents with LLMs to provide contextual answers."
]

# Compute dummy embeddings once
doc_embeddings = get_embeddings(docs)

# UI
mode = st.radio("Response Mode", ["Concise", "Detailed"])
query = st.text_input("Enter your question:")

def generate_answer(query, context, mode):
    """Dummy LLM-style answer (no API needed)."""
    if mode == "Concise":
        return (
            f"Short Answer:\n{context[:150]}...\n\n"
            f"(Concise Mode)"
        )
    else:
        return (
            f"Detailed Answer\n\n"
            f"User Query: {query}\n\n"
            f"Relevant Information:\n{context}\n\n"
            f"Explanation:\n"
            f"This answer is generated using a RAG pipeline where retrieved documents "
            f"or web search results are used as context.\n\n"
            f"(Detailed Mode)"
        )

if st.button("Ask"):
    try:
        # RAG Retrieval
        top_docs = retrieve_docs(query, docs, doc_embeddings)

        if top_docs:
            context = "\n".join(top_docs)
        else:
            # Web Search Fallback
            web_results = web_search(query)
            context = "\n".join(web_results)

        final_response = generate_answer(query, context, mode)
        st.write(final_response)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
