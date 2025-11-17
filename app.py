import streamlit as st
from models.llm import get_chat_model
from model.embeddings import get_vector_store

# Initialize LLM and Vector Store
chat_model = get_chat_model()
vector_store = get_vector_store()

st.title("NeoStats AI Engineer Assistant")

response_mode = st.radio("Response Mode", ["Concise", "Detailed"])
user_query = st.text_input("Enter your question:")

chat_history = st.session_state.get("chat_history", [])

if user_query:
    # Embed Query & Search
    docs = vector_store.similarity_search(user_query, k=2)

    # Prepare context
    context = "\n".join([d.page_content for d in docs]) if docs else "No relevant document found."

    prompt = f"Response Mode: {response_mode}.\nUser Query: {user_query}.\nContext: {context}.\nAnswer:"    

    # LLM Response
    answer = chat_model.predict(prompt)

    # Save to history
    chat_history.append(("You", user_query))
    chat_history.append(("Assistant", answer))
    st.session_state.chat_history = chat_history

# Display chat history
st.subheader("Chat History")
for speaker, msg in chat_history:
    st.write(f"**{speaker}:** {msg}")
