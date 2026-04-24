from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Abstract base class for all LLM backends."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Send a prompt and return the generated text response."""
        pass
