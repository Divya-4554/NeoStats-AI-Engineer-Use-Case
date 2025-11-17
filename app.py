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

# Precompute dummy embeddings
doc_embeddings = get_embeddings(docs)

# UI
mode = st.radio("Response Mode", ["Concise", "Detailed"])
query = st.text_input("Enter your question:")

def generate_answer(query, context, mode):
    """
    Clean Answer Generator — NO API required.
    """

    # 1. Handle greetings / casual messages
    smalltalk = ["hi", "hello", "hey", "hii", "yo", "hola"]
    if query.lower().strip() in smalltalk:
        return "Hi! How can I help you today? 😊"

    # 2. If nothing found at all
    if not context or context.strip() == "":
        return "I couldn't find any relevant information. Please try another question."

    # 3. Concise Mode
    if mode == "Concise":
        return f"{context[:250]}..."

    # 4. Detailed Mode
    return (
        f"### Detailed Answer\n"
        f"**Your Question:** {query}\n\n"
        f"**Relevant Information Found:**\n{context}\n\n"
        f"**Explanation:**\n"
        f"This answer is generated using a simple RAG pipeline. "
        f"Relevant documents (or fallback web search results) "
        f"were used to form the final response."
    )


if st.button("Ask"):
    try:
        # Retrieve top docs using embeddings
        top_docs = retrieve_docs(query, docs, doc_embeddings)

        if top_docs:
            context = "\n".join(top_docs)
        else:
            # If local docs fail → fallback to dummy web search
            web_results = web_search(query)
            context = "\n".join(web_results)

        final_answer = generate_answer(query, context, mode)
        st.write(final_answer)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
