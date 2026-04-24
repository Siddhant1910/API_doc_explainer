import os
import random
from dotenv import load_dotenv
from google import genai
from llm.base import LLMClient

load_dotenv(override=True)


class GeminiClient(LLMClient):
    """LLM client backed by Google Gemini API (google-genai SDK)."""

    def __init__(self, model: str = "gemini-2.5-flash"):
        keys_env = os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY")
        if not keys_env:
            raise ValueError("GEMINI_API_KEYS or GEMINI_API_KEY not set in environment variables.")
        
        self.api_keys = [k.strip() for k in keys_env.split(",") if k.strip()]
        self.model_name = model

    def generate(self, prompt: str) -> str:
        """Call Gemini and return the generated text. Retries on other keys if quota exceeded."""
        available_keys = list(self.api_keys)
        random.shuffle(available_keys)
        
        last_error = ""
        for key in available_keys:
            client = genai.Client(api_key=key)
            try:
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=genai.types.GenerateContentConfig(
                        response_mime_type="application/json",
                    )
                )
                return response.text
            except Exception as e:
                err_msg = str(e)
                last_error = err_msg
                # If quota exceeded or 503 Unavailable, try the next key
                if "RESOURCE_EXHAUSTED" in err_msg or "429" in err_msg or "503" in err_msg:
                    continue
                # If other error, break and return it
                return f"Gemini API Error: {err_msg}"
                
        return "Gemini API Quota Exceeded. Please wait a minute and try again."
