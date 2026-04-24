"""
Unit and integration tests for the API Documentation Explainer Agent.

Run with:
    python -m pytest tests/ -v
"""
import json
from unittest.mock import patch, MagicMock

import pytest

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Helpers
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_SAMPLE_OUTPUT = {
    "api_name": "Stripe API",
    "api_fit_analysis": "Stripe is a payment processing API.",
    "api_comparison_table": "| API | Fees |\n|---|---|",
    "authentication": "Bearer Token",
    "endpoint_playground": {
        "url": "https://api.stripe.com/v1/charges",
        "params": "amount, currency",
        "example_request": "curl ...",
        "sample_json_response": "{}",
        "field_explanation": "id: charge id"
    },
    "code": {
        "python": "import requests",
        "javascript": "fetch()"
    },
    "location_data_guide": "N/A",
    "limitations_and_gotchas": "Rate limits apply",
    "final_recommendation": "Use Stripe"
}

_SAMPLE_JUDGE = {
    "accuracy": 8,
    "completeness": 7,
    "clarity": 9,
    "code_usability": 8,
    "overall": 8,
    "verdict": "Strong output.",
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8.2 — Intent Agent Tests
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestIntentAgent:

    @patch("agents.intent_agent.get_llm")
    def test_url_returns_explain_api(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = json.dumps(
            {"intent": "explain_api", "input": "https://api.stripe.com"}
        )
        mock_get_llm.return_value = mock_llm

        from agents.intent_agent import intent_agent
        result = intent_agent("https://api.stripe.com")

        assert result["intent"] == "explain_api"
        assert "input" in result

    @patch("agents.intent_agent.get_llm")
    def test_use_case_returns_recommend_api(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = json.dumps(
            {"intent": "recommend_api", "input": "I need a weather API"}
        )
        mock_get_llm.return_value = mock_llm

        from agents.intent_agent import intent_agent
        result = intent_agent("I need a weather API")
        assert result["intent"] == "recommend_api"

    @patch("agents.intent_agent.get_llm")
    def test_invalid_json_falls_back(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = "not json at all"
        mock_get_llm.return_value = mock_llm

        from agents.intent_agent import intent_agent
        result = intent_agent("something")
        # Should not raise; should fallback to explain_api
        assert result["intent"] == "explain_api"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8.3 — Judge Agent Tests
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestJudgeAgent:

    @patch("agents.judge_agent.get_llm")
    def test_all_scores_are_integers_in_range(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = json.dumps(_SAMPLE_JUDGE)
        mock_get_llm.return_value = mock_llm

        from agents.judge_agent import judge_agent
        result = judge_agent(_SAMPLE_OUTPUT)

        for key in ("accuracy", "completeness", "clarity", "code_usability", "overall"):
            assert isinstance(result[key], int), f"{key} should be an int"
            assert 1 <= result[key] <= 10, f"{key} should be in [1, 10]"

    @patch("agents.judge_agent.get_llm")
    def test_verdict_is_string(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.generate.return_value = json.dumps(_SAMPLE_JUDGE)
        mock_get_llm.return_value = mock_llm

        from agents.judge_agent import judge_agent
        result = judge_agent(_SAMPLE_OUTPUT)
        assert isinstance(result["verdict"], str)

    @patch("agents.judge_agent.get_llm")
    def test_out_of_range_scores_are_clamped(self, mock_get_llm):
        """Scores outside [1,10] should be clamped."""
        bad_judge = {**_SAMPLE_JUDGE, "accuracy": 15, "clarity": -3}
        mock_llm = MagicMock()
        mock_llm.generate.return_value = json.dumps(bad_judge)
        mock_get_llm.return_value = mock_llm

        from agents.judge_agent import judge_agent
        result = judge_agent(_SAMPLE_OUTPUT)
        assert result["accuracy"] == 10
        assert result["clarity"] == 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8.4 — Tavily Tool Tests
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestTavilyTool:

    @patch("tools.tavily_tool.TavilyClient")
    @patch.dict("os.environ", {"TAVILY_API_KEY": "fake_key"})
    def test_returns_string(self, MockClient):
        # Reset cached client so the mock is used
        import tools.tavily_tool as tt
        tt._client = None

        mock_instance = MagicMock()
        MockClient.return_value = mock_instance
        mock_instance.search.return_value = {
            "results": [
                {"title": "Stripe Docs", "content": "Stripe is a payment API.", "url": "https://stripe.com"}
            ]
        }

        from tools.tavily_tool import search
        result = search("Stripe payment API documentation")
        assert isinstance(result, str)
        assert len(result) > 0

    @patch("tools.tavily_tool.TavilyClient")
    @patch.dict("os.environ", {"TAVILY_API_KEY": "fake_key"})
    def test_no_results_fallback(self, MockClient):
        import tools.tavily_tool as tt
        tt._client = None

        mock_instance = MagicMock()
        MockClient.return_value = mock_instance
        mock_instance.search.return_value = {"results": []}

        from tools.tavily_tool import search
        result = search("something obscure")
        assert result == "No results found."


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8.5 — Integration Test: run_pipeline
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TestPipeline:

    @patch("agents.judge_agent.get_llm")
    @patch("agents.generator_agent.get_llm")
    @patch("agents.planner_agent.get_llm")
    @patch("agents.intent_agent.get_llm")
    @patch("tools.tavily_tool.TavilyClient")
    @patch.dict("os.environ", {"TAVILY_API_KEY": "fake_key", "LLM_PROVIDER": "gemini", "GEMINI_API_KEY": "fake"})
    def test_run_pipeline_returns_required_keys(
        self,
        MockTavily,
        mock_intent_llm,
        mock_planner_llm,
        mock_gen_llm,
        mock_judge_llm,
    ):
        import tools.tavily_tool as tt
        tt._client = None

        # Mock Tavily
        mock_tavily_instance = MagicMock()
        MockTavily.return_value = mock_tavily_instance
        mock_tavily_instance.search.return_value = {
            "results": [{"title": "OpenAI", "content": "OpenAI API docs.", "url": "https://openai.com"}]
        }

        # Mock intent LLM
        intent_mock = MagicMock()
        intent_mock.generate.return_value = json.dumps({"intent": "explain_api", "input": "OpenAI API"})
        mock_intent_llm.return_value = intent_mock

        # Mock planner LLM
        planner_mock = MagicMock()
        planner_mock.generate.return_value = json.dumps(
            ["search_tavily", "generate_summary", "generate_code", "judge_output"]
        )
        mock_planner_llm.return_value = planner_mock

        # Mock generator LLM
        gen_mock = MagicMock()
        gen_mock.generate.return_value = json.dumps(_SAMPLE_OUTPUT)
        mock_gen_llm.return_value = gen_mock

        # Mock judge LLM
        judge_mock = MagicMock()
        judge_mock.generate.return_value = json.dumps(_SAMPLE_JUDGE)
        mock_judge_llm.return_value = judge_mock

        from utils.helpers import run_pipeline
        output, evaluation, steps_log = run_pipeline("OpenAI API")

        required_output_keys = {"api_name", "api_fit_analysis", "api_comparison_table", "authentication", "endpoint_playground", "code", "location_data_guide", "limitations_and_gotchas", "final_recommendation"}
        required_eval_keys = {"accuracy", "completeness", "clarity", "code_usability", "overall", "verdict"}

        assert required_output_keys.issubset(output.keys()), "Missing output keys"
        assert required_eval_keys.issubset(evaluation.keys()), "Missing evaluation keys"
        assert isinstance(steps_log, list)
        assert len(steps_log) > 0
