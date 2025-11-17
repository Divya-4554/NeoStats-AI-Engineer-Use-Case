import streamlit as st
from groq import Groq
import os
import json

# -----------------------------
# Load API Key
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("Missing GROQ_API_KEY. Add it in Streamlit → Settings → Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="NeoStats AI Engineer Assistant", layout="wide")

st.title("NeoStats AI Engineer Assistant")

st.write("Ask questions about your system, network, or data. The AI will respond intelligently.")

# MODE SELECTION
response_mode = st.radio("Response Mode", ["Concise", "Detailed"])

# -----------------------------
# Session State for Chat History
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Chat Completion Function
# -----------------------------
def get_llm_response(user_query, mode):
    """Send a query to Groq LLM and return the answer."""
    try:
        messages = [
            {"role": "system", "content": f"You are a helpful AI Engineer Assistant. Reply in {mode} mode."},
        ]

        # Add previous conversation history
        for h in st.session_state.chat_history:
            messages.append({"role": "user", "content": h["user"]})
            messages.append({"role": "assistant", "content": h["assistant"]})

        # Add latest query
        messages.append({"role": "user", "content": user_query})

        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
            temperature=0.2
        )

        answer = response.choices[0].message.content
        return answer

    except Exception as e:
        return f"Something went wrong: {str(e)}"


# -----------------------------
# Input Box
# -----------------------------
user_query = st.text_input("Enter your question:")

if st.button("Submit"):
    if user_query.strip() == "":
        st.warning("Please enter a message.")
    else:
        # Get model response
        answer = get_llm_response(user_query, response_mode)

        # Save history
        st.session_state.chat_history.append({
            "user": user_query,
            "assistant": answer
        })

# -----------------------------
# Chat History Display
# -----------------------------
if st.session_state.chat_history:
    st.subheader("Chat History")
    for h in st.session_state.chat_history:
        st.markdown(f"**You:** {h['user']}")
        st.markdown(f"**Assistant:** {h['assistant']}")
        st.markdown("---")
