import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv(override=True)

def _get_client() -> TavilyClient:
    """Initialise the Tavily client."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key or api_key == "your_key_here":
        raise ValueError("TAVILY_API_KEY not set in environment variables.")
    return TavilyClient(api_key=api_key)


def search(query: str, max_results: int = 5) -> str:
    """
    Search Tavily for the given query and return a flattened string of the
    top results (content trimmed to 2000 characters to stay within LLM token
    budgets).

    Returns:
        A multi-line string of search-result content, or a fallback message.
    """
    try:
        client = _get_client()
        results = client.search(query=query, max_results=max_results)
        hits = results.get("results", [])
        if not hits:
            return "No results found."

        pieces = []
        for hit in hits:
            title = hit.get("title", "")
            content = hit.get("content", "")
            url = hit.get("url", "")
            pieces.append(f"[{title}] ({url})\n{content}")

        combined = "\n\n".join(pieces)
        # Trim to avoid token overflow but allow enough room for API docs & code
        return combined[:10000]

    except Exception as exc:
        return f"Tavily search error: {exc}"
