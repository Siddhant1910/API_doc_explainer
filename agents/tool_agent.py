"""
Tool Agent — wraps the Tavily search tool and returns trimmed results.
"""
# This agent is responsible for external retrieval. 
# It fetches real-time data from the web using Tavily.

from tools import tavily_tool

# Limit character count to avoid blowing up the LLM's context window
_MAX_CHARS = 2000


def tool_agent(query: str) -> str:
    """
    Search Tavily for `query` and return the result string.
    Trims to _MAX_CHARS to prevent LLM token overflow.
    """
    # Simply delegates the heavy lifting to the Tavily wrapper in tools/
    result = tavily_tool.search(query)
    return result[:_MAX_CHARS]
