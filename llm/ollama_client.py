import os
from dotenv import load_dotenv
import ollama
from llm.base import LLMClient

load_dotenv(override=True)


class OllamaClient(LLMClient):
    """LLM client backed by a local Ollama instance."""

    def __init__(self, model: str | None = None):
        # Use provided model, or read from env, or default to a safe value
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2:3b")

    def generate(self, prompt: str) -> str:
        """Call Ollama and return the generated text."""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                format="json"
            )
            return response["message"]["content"]
        except Exception as e:
            return f'{{ "summary": "Ollama Error ({self.model}): {str(e)}" }}'
