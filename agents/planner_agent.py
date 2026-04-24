"""
Planner Agent — takes the classified intent dict and returns an ordered
list of pipeline steps to execute.
"""
# The planner acts as the "brain's secretary", deciding which tools and 
# generation steps are necessary based on the detected intent.

import json
import re
from llm import get_llm

_PLANNER_PROMPT = """\
You are a planning agent for an API Documentation Explainer system.

Given the following intent, produce an ordered list of pipeline steps.
Choose from these available step names:
  - search_tavily       : fetch live API documentation via Tavily search
  - generate_summary    : summarise the API's purpose
  - generate_endpoints  : extract key endpoints
  - generate_code       : produce code examples (Python, JS, cURL)
  - generate_demo       : produce a request/response demo
  - recommend_apis      : suggest relevant APIs for a use-case
  - compare_apis        : produce a side-by-side comparison
  - judge_output        : run the LLM-as-Judge evaluation

Return ONLY a valid JSON array of step name strings (no markdown, no explanation).
Example: ["search_tavily", "generate_summary", "generate_code", "judge_output"]

Intent: {intent}
"""


def planner_agent(intent: dict) -> list:
    """
    Return an ordered list of pipeline step strings for the given intent.
    Falls back to a sensible default if parsing fails.
    """
    # 1. Initialize LLM
    llm = get_llm("groq")
    
    # 2. Format request
    prompt = _PLANNER_PROMPT.format(intent=json.dumps(intent))
    
    # 3. Call model
    raw = llm.generate(prompt).strip()

    # 4. Cleanup and parse JSON
    raw = re.sub(r"```json\s*|```", "", raw).strip()

    try:
        steps = json.loads(raw)
        if isinstance(steps, list):
            return steps
    except json.JSONDecodeError:
        # If parsing fails, the pipeline won't break; we use a safe default
        pass

    # Default plan for "explain_api"
    return [
        "search_tavily",
        "generate_summary",
        "generate_endpoints",
        "generate_code",
        "generate_demo",
        "judge_output",
    ]
