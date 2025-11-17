# utils/web_search.py
"""
Mock web search function for demo purposes (no external API).
Returns a small list of textual search results for the given query.
"""

def web_search(query):
    if not query or query.strip() == "":
        return ["No query provided for web search."]
    # Provide three mock results using the query (clear and formatted)
    return [
        f"Mock result 1 for '{query}': summary of a likely web article related to \"{query}\".",
        f"Mock result 2 for '{query}': another short snippet that could help answer the question.",
        f"Mock result 3 for '{query}': further context and a possible link/reference placeholder."
    ]
