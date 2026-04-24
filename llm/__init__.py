import os
from llm.ollama_client import OllamaClient
from llm.gemini_client import GeminiClient
from llm.groq_client import GroqClient

def get_llm(force_provider: str = None):
    """Dynamically return the LLM client based on LLM_PROVIDER env var, or force one."""
    env_provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    
    # If the user explicitly sets LLM_PROVIDER=ollama in .env, force ALL agents to use Ollama
    # to allow 100% local execution. Otherwise, respect the hardcoded provider for load balancing.
    if env_provider == "ollama":
        provider = "ollama"
    else:
        provider = force_provider if force_provider else env_provider
        
    if provider == "groq":
        return GroqClient()
    elif provider == "gemini":
        return GeminiClient()
    return OllamaClient()
