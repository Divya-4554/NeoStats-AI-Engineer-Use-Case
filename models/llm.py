import os
import streamlit as st
from groq import Groq

def get_chat_model():
    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        return lambda prompt: "Dummy LLM response (no API key provided)."

    client = Groq(api_key=api_key)

    def chat(prompt):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        return response.choices[0].message["content"]

    return chat
