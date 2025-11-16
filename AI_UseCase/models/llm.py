# models/llm.py

from config.config import settings, validate_for_provider

def get_chat_model():
    provider = settings.PROVIDER.lower()

    if provider == "openai":
        try:
            from langchain_openai import ChatOpenAI
        except Exception as e:
            raise RuntimeError("ChatOpenAI is not available. Install `langchain-openai`.") from e

        validate_for_provider()
        return ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            api_key=settings.OPENAI_API_KEY
        )

    elif provider == "groq":
        try:
            from langchain_groq import ChatGroq
        except Exception as e:
            raise RuntimeError("ChatGroq is not available. Install `langchain-groq`.") from e

        if not settings.GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY missing for Groq provider.")

        return ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE
        )

    elif provider in ("google", "gemini", "google-genai"):
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except Exception as e:
            raise RuntimeError("ChatGoogleGenerativeAI not importable. Install `langchain-google-genai`.") from e

        if not settings.GOOGLE_API_KEY:
            raise RuntimeError("GOOGLE_API_KEY missing for Google Gemini provider.")

        return ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            google_api_key=settings.GOOGLE_API_KEY
        )

    else:
        raise RuntimeError(f"Unsupported PROVIDER: {provider}")
