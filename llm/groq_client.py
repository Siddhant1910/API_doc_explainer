import os
from dotenv import load_dotenv
from groq import Groq
from llm.base import LLMClient

load_dotenv(override=True)


class GroqClient(LLMClient):
    """LLM client backed by Groq API."""

    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment variables.")
        
        self.client = Groq(api_key=api_key)
        self.model_name = model

    def generate(self, prompt: str) -> str:
        """Call Groq and return the generated text."""
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model_name,
                response_format={"type": "json_object"},
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Groq API Error: {str(e)}"
