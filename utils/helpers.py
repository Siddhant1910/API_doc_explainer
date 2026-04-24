"""
Pipeline Orchestrator — runs all five agents in order and returns a
comprehensive result tuple.
"""
from agents.intent_agent import intent_agent
from agents.planner_agent import planner_agent
from agents.tool_agent import tool_agent
from agents.generator_agent import generator_agent
from agents.judge_agent import judge_agent


def run_pipeline(user_input: str) -> tuple[dict, dict, list]:
    """
    Execute the full agentic pipeline for `user_input`.

    Returns:
        (output, evaluation, steps_log)

        output      – structured API explanation dict from generator_agent
        evaluation  – quality scores dict from judge_agent
        steps_log   – list of human-readable status messages for the UI
    """
    steps_log = []

    # ── Step 1: Intent Detection ───────────────────────────────────────────
    steps_log.append("🔍 Detecting intent…")
    intent = intent_agent(user_input)
    steps_log.append(f"✅ Intent: {intent.get('intent', 'unknown')}")

    # ── Step 2: Planning ──────────────────────────────────────────────────
    steps_log.append("📋 Planning steps…")
    plan = planner_agent(intent)
    steps_log.append(f"✅ Plan: {', '.join(plan)}")

    # ── Step 3: Tavily Search ─────────────────────────────────────────────
    steps_log.append("🌐 Searching Tavily…")
    query = intent.get("input", user_input)
    tavily_result = tool_agent(query)
    chars = len(tavily_result)
    steps_log.append(f"✅ Tavily returned {chars} characters.")

    # ── Step 4: Generate Output ───────────────────────────────────────────
    steps_log.append("⚙️ Generating structured output…")
    output = generator_agent(tavily_result, intent)
    steps_log.append("✅ Output generated.")

    # ── Step 5: Judge Evaluation ──────────────────────────────────────────
    steps_log.append("⚖️ Evaluating output quality…")
    evaluation = judge_agent(output)
    overall = evaluation.get("overall", "?")
    steps_log.append(f"✅ Judge score: {overall}/10")

    return output, evaluation, steps_log
