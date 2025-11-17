"""
LLM Loader — returns Groq LLM if key exists, else returns dummy.
"""

import os

try:
    from groq import Groq
except:
    Groq = None


def get_chat_model():
    api_key = os.getenv("GROQ_API_KEY")

    if api_key and Groq:
        client = Groq(api_key=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)

        def chat(prompt):
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            return response.choices[0].message["content"]

        return chat

    # Dummy fallback
    def dummy(prompt):
        return "Dummy LLM response (no API key provided)."

    return dummy
