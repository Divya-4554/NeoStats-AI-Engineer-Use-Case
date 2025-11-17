import requests

def web_search(query, api_key):
    """
    Perform a simple web search and return top results.
    """
    try:
        url = f"https://api.serpapi.com/search.json?q={query}&api_key={api_key}"
        resp = requests.get(url).json()
        results = []
        for r in resp.get("organic_results", [])[:3]:
            title = r.get("title")
            snippet = r.get("snippet")
            link = r.get("link")
            results.append(f"{title}\n{snippet}\n{link}")
        return results
    except Exception as e:
        print(f"Web search error: {e}")
        return ["No web results found."]
