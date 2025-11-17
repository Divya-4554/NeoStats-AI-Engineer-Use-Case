import streamlit as st
from models.embeddings import get_embeddings
from utils.retrieve import retrieve_docs
from utils.web_search import web_search

st.set_page_config(page_title="NeoStats AI Engineer Assistant", layout="centered")
st.title("NeoStats AI Engineer Assistant")

# ---------- Local documents ----------
# Replace these with real .txt files loaded dynamically if you want later.
docs = [
    "NeoStats provides AI-powered analytics for IT and engineering teams.",
    "Streamlit allows fast deployment of AI, ML, and data applications.",
    "RAG integrates local documents with LLMs to provide contextual answers."
]

# Compute dummy embeddings once (no external API required)
doc_embeddings = get_embeddings(docs)

# UI
mode = st.radio("Response Mode", ["Concise", "Detailed"])
query = st.text_input("Enter your question:")

def generate_answer(query, context, mode):
    """
    Clean Answer Generator — NO API required.
    Provides small-talk handling and concise/detailed outputs using context.
    """
    # small-talk
    if query and query.lower().strip() in ["hi", "hello", "hey", "hii", "hola", "yo"]:
        return "Hi! How can I help you today? 😊"

    # nothing found
    if not context or context.strip() == "":
        return "I couldn't find any relevant information. Try a different question or upload documents."

    # concise
    if mode == "Concise":
        # Prefer an actual short answer derived from the most relevant sentence(s)
        snippet = context.strip().replace("\n", " ")
        return snippet[:250] + ("..." if len(snippet) > 250 else "")

    # detailed
    return (
        f"### Detailed Answer\n\n"
        f"**Question:** {query}\n\n"
        f"**Relevant Information Used:**\n{context}\n\n"
        f"**Explanation:**\nThis response was generated using a retrieval-augmented pipeline: the app retrieved relevant documents (or web results) and used them as context to form this answer."
    )


if st.button("Ask"):
    try:
        if not query or query.strip() == "":
            st.warning("Please enter a question.")
        else:
            # Retrieve local documents (RAG)
            top_docs = retrieve_docs(query, docs, doc_embeddings, top_k=3, similarity_threshold=0.35)

            if top_docs:
                context = "\n\n".join(top_docs)
            else:
                # Fallback to mock web search
                web_results = web_search(query)
                context = "\n\n".join(web_results)

            final_answer = generate_answer(query, context, mode)
            st.markdown(final_answer)
    except Exception as e:
        st.error(f"Something went wrong: {e}")
