import streamlit as st
from models.embeddings import get_embeddings
from utils.retrieve import retrieve_docs
from utils.web_search import web_search
from config.config import SERPAPI_KEY

# Dummy local docs for example
docs = [
    "NeoStats provides AI-powered analytics for IT teams.",
    "Streamlit allows fast deployment of ML and AI apps.",
    "RAG integrates local documents with LLMs for better responses."
]
doc_embeddings = get_embeddings(docs)

st.title("NeoStats AI Engineer Assistant")

mode = st.radio("Response Mode", ["Concise", "Detailed"])
query = st.text_input("Enter your question:")

if st.button("Ask"):
    try:
        # Retrieve relevant docs
        top_docs = retrieve_docs(query, docs, doc_embeddings)

        if top_docs:
            context = "\n".join(top_docs)
            prompt = f"Answer the following question based on context:\n{context}\nQuestion: {query}"
        else:
            # fallback to web search
            web_results = web_search(query, SERPAPI_KEY)
            context = "\n".join(web_results)
            prompt = f"Answer the following question based on web search:\n{context}\nQuestion: {query}"

        if mode == "Concise":
            prompt += "\nProvide a short summary (2-3 sentences)."
        else:
            prompt += "\nProvide a detailed answer with examples."

        # Call your LLM (OpenAI / Gemini / Groq)
        from models.llm import get_chat_model
        response = get_chat_model(prompt)  # implement in llm.py

        st.write(response)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
