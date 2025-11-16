# utils/web_search.py
import requests
from config.config import settings

SERPAPI_BASE = "https://serpapi.com/search.json"

def serpapi_search(query: str, num_results: int = 3):
    key = settings.SERPAPI_API_KEY
    if not key:
        raise RuntimeError("SERPAPI_API_KEY not set. Add it to .env to enable live web search.")
    params = {
        "q": query,
        "num": num_results,
        "api_key": key
    }
    try:
        resp = requests.get(SERPAPI_BASE, params=params, timeout=10)
        resp.raise_for_status()
        j = resp.json()
        results = []
        for r in j.get("organic_results", [])[:num_results]:
            title = r.get("title")
            snippet = r.get("snippet") or r.get("snippet_highlighted_words")
            link = r.get("link")
            results.append({"title": title, "snippet": snippet, "link": link})
        return results
    except Exception as e:
        raise RuntimeError(f"SerpAPI search failed: {e}")
