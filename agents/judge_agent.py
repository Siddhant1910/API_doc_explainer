"""
Judge Agent — LLM-as-a-Judge that evaluates the generated output on four
criteria and returns structured scores + a verdict.
"""
# This agent performs self-correction and quality control.
# It ensures the output is accurate and usable before showing it to the user.

import json
import re
from llm import get_llm

_JUDGE_PROMPT = """\
You are an impartial AI quality evaluator (LLM-as-a-Judge).

Evaluate the following API documentation output on four criteria.
Score each criterion from 1 (poor) to 10 (excellent).

Output to evaluate:
---
{output_json}
---

Scoring criteria:
  1. Accuracy      – Is the information factually correct and trustworthy?
  2. Completeness  – Does it cover the key aspects (summary, endpoints, auth, code)?
  3. Clarity       – Is the explanation clear and easy to understand?
  4. Code Usability – Are the code snippets correct and immediately usable?

Return ONLY a valid JSON object (no markdown, no explanation):
{{
  "accuracy": <int 1-10>,
  "completeness": <int 1-10>,
  "clarity": <int 1-10>,
  "code_usability": <int 1-10>,
  "overall": <int — simple average of the four scores, rounded>,
  "verdict": "<One or two sentence qualitative verdict>"
}}
"""


def _clamp(value, lo: int = 1, hi: int = 10) -> int:
    """Ensure a score value is an integer clamped between lo and hi."""
    try:
        return max(lo, min(hi, int(value)))
    except (TypeError, ValueError):
        return 5


def judge_agent(generated_output: dict) -> dict:
    """
    Evaluate generated_output and return a structured scores dict.
    All four criteria scores are guaranteed to be integers in [1, 10].
    """
    # 1. Initialize LLM
    llm = get_llm("groq")  # Reverted to Groq due to API quotas
    
    # 2. Serialise the output for the prompt (trim large fields to save tokens)
    try:
        output_str = json.dumps(generated_output, indent=2)[:1500]
    except Exception:
        output_str = str(generated_output)[:1500]

    # 3. Create evaluation prompt
    prompt = _JUDGE_PROMPT.format(output_json=output_str)
    raw = llm.generate(prompt).strip()

    # 4. Cleanup response
    raw = re.sub(r"```json\s*|```", "", raw).strip()

    try:
        # 5. Parse and post-process scores
        result = json.loads(raw)
        
        # Validate and clamp all scores to ensure they stay in [1, 10]
        accuracy = _clamp(result.get("accuracy", 5))
        completeness = _clamp(result.get("completeness", 5))
        clarity = _clamp(result.get("clarity", 5))
        code_usability = _clamp(result.get("code_usability", 5))
        
        # Calculate derived overall score
        overall = round((accuracy + completeness + clarity + code_usability) / 4)
        verdict = str(result.get("verdict", "Evaluation incomplete."))

        return {
            "accuracy": accuracy,
            "completeness": completeness,
            "clarity": clarity,
            "code_usability": code_usability,
            "overall": overall,
            "verdict": verdict,
        }
    except json.JSONDecodeError:
        # Fail-safe evaluation response
        return {
            "accuracy": 5,
            "completeness": 5,
            "clarity": 5,
            "code_usability": 5,
            "overall": 5,
            "verdict": "Could not parse judge response.",
        }
