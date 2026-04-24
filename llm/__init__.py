import os
from llm.ollama_client import OllamaClient
from llm.gemini_client import GeminiClient
from llm.groq_client import GroqClient

def get_llm(force_provider: str = None):
    """Dynamically return the LLM client based on LLM_PROVIDER env var, or force one."""
    provider = force_provider if force_provider else os.getenv("LLM_PROVIDER", "ollama").lower()
    
    if provider == "groq":
        return GroqClient()
    elif provider == "gemini":
        return GeminiClient()
    return OllamaClient()
