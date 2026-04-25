"""
Generator Agent — transforms raw Tavily search results + intent into a
richly structured output dict containing summary, endpoints, code, demo,
and optional recommendations.
"""
# This is the "creative" part of the pipeline. It synthesizes raw facts
# into a developer-friendly documentation format.

import json
import re
from llm import get_llm

_BASE_PROMPT = """\
You are an expert API Documentation writer and software architect.

The user's original query is: "{user_query}"
The system classified intent is: {intent_type}

API Documentation Context (from search):
---
{tavily_result}
---

INSTRUCTIONS:
Your job is to convert the context into a practical integration guide or comparison based on the user's intent.
Output must be structured, developer-focused, and immediately usable.
You MUST return ONLY a valid JSON object matching the exact schema below. Do not include markdown fences.

CRITICAL RULES:
- NO vague explanations
- ALWAYS optimize for real-world usage
- Output valid JSON only.

EXPECTED JSON SCHEMA:
{json_schema}
"""

_SCHEMA_EXPLAIN = """
{
  "api_name": "Name of the API",
  "api_fit_analysis": "Detailed technical analysis of what this API does. (Section 1)",
  "authentication": "Step-by-step authentication guide.",
  "endpoint_playground": {
    "url": "https://api.example.com/v1/endpoint",
    "params": "List of parameters",
    "example_request": "cURL or similar example request",
    "sample_json_response": "Raw JSON sample response",
    "field_explanation": "Explanation of the response fields"
  },
  "code": {
    "python": "// Comprehensive properly formatted Python code example with error handling",
    "javascript": "// Comprehensive properly formatted JavaScript code example with error handling"
  },
  "limitations_and_gotchas": "Limitations & Gotchas (Section 7)",
  "final_recommendation": "Final Recommendation (Section 8)"
}
"""

_SCHEMA_COMPARE = """
{
  "api_name": "Names of the APIs being compared",
  "api_fit_analysis": "Detailed technical analysis contrasting the APIs.",
  "api_comparison_table": "Must be a raw Markdown string containing a table (e.g. '| API | Pricing | Features |...\\n|---|---|---|'). DO NOT output a JSON array. ALWAYS include a 'Pricing' column.",
  "code": {
    "python": "// Comprehensive properly formatted Python code example comparing both if applicable",
    "javascript": "// Comprehensive properly formatted JavaScript code example"
  }
}
"""

_SCHEMA_RECOMMEND = """
{
  "api_name": "Top Recommended APIs",
  "api_fit_analysis": "Overview of the recommended APIs for the use-case.",
  "api_comparison_table": "Must be a raw Markdown string containing a table (e.g. '| API | Pricing | Features |...\\n|---|---|---|'). DO NOT output a JSON array. ALWAYS include a 'Pricing' column.",
  "code": {
    "python": "// Example Python code snippet for the top recommended API",
    "javascript": "// Example JavaScript code snippet for the top recommended API"
  },
  "final_recommendation": "Final Recommendation - which API should they choose and why?"
}
"""


def generator_agent(tavily_result: str, intent: dict) -> dict:
    """
    Generate structured API explanation output.
    Returns a dict on success; returns an error dict on failure.
    """
    llm = get_llm("gemini")  # Use Gemini for large-context generation
    
    intent_type = intent.get("intent", "explain_api")
    if intent_type == "compare_api":
        schema = _SCHEMA_COMPARE
    elif intent_type == "recommend_api":
        schema = _SCHEMA_RECOMMEND
    else:
        schema = _SCHEMA_EXPLAIN
        
    # Trim context to avoid token overflow on LLMs (Safe for 8k contexts)
    tavily_trimmed = tavily_result[:12000] if isinstance(tavily_result, str) else str(tavily_result)[:12000]

    prompt = _BASE_PROMPT.format(
        user_query=intent.get("input", "N/A"),
        intent_type=intent_type,
        tavily_result=tavily_trimmed,
        json_schema=schema
    )

    
    raw = llm.generate(prompt).strip()

    # Strip markdown fences if the model wraps output in them
    raw = re.sub(r"```json\s*|```", "", raw).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "api_name": "API Quota Exceeded or Error",
            "api_fit_analysis": raw[:500],
            "api_comparison_table": "N/A",
            "authentication": "N/A",
            "endpoint_playground": {
                "url": "N/A",
                "params": "N/A",
                "example_request": "N/A",
                "sample_json_response": "N/A",
                "field_explanation": "N/A"
            },
            "code": {"python": "", "javascript": ""},
            "location_data_guide": "N/A",
            "limitations_and_gotchas": "N/A",
            "final_recommendation": "N/A"
        }
