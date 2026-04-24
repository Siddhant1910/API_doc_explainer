"""
Intent Agent — classifies the user's input into one of three intents:
  - explain_api   : user provided an API URL or name
  - recommend_api : user described a use-case / problem
  - compare_api   : user wants to compare multiple APIs
"""
# This agent uses an LLM to understand what the user wants to do.
# It returns a structured JSON so the pipeline knows which steps to take next.
import json
import re
from llm import get_llm

_INTENT_PROMPT = """\
You are an intent classification agent for an API Documentation Explainer system.

Classify the following user input into EXACTLY one of these three intents:
  - "explain_api"   → The user has given an API URL or API name (e.g. "Stripe API", "https://api.openai.com")
  - "recommend_api" → The user has described a problem or use-case and wants API suggestions (e.g. "I need an API for weather data")
  - "compare_api"   → The user explicitly wants to compare two or more APIs

Return ONLY a valid JSON object with this exact shape (no markdown, no explanation):
{{
  "intent": "<one of the three intents above>",
  "input": "<the original user input, unchanged>"
}}

User input: {user_input}
"""


def intent_agent(user_input: str) -> dict:
    """
    Classify user_input and return a dict like:
        {"intent": "explain_api", "input": "Stripe API"}
    Falls back to "explain_api" if the LLM output cannot be parsed.
    """
    # Initialize the LLM client
    llm = get_llm("groq")
    
    # Format the prompt with the user's input
    prompt = _INTENT_PROMPT.format(user_input=user_input)
    
    # Generate the classification response
    raw = llm.generate(prompt).strip()

    # Strip markdown fences if the model wraps output
    raw = re.sub(r"```json\s*|```", "", raw).strip()

    try:
        result = json.loads(raw)
        if result.get("intent") not in ("explain_api", "recommend_api", "compare_api"):
            result["intent"] = "explain_api"
        return result
    except json.JSONDecodeError:
        return {"intent": "explain_api", "input": user_input}
