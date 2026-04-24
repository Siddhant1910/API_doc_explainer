"""
app.py — Streamlit entry point for the API Documentation Explainer Agent.
"""
import streamlit as st
from dotenv import load_dotenv

# ── Environment ────────────────────────────────────────────────────────────
load_dotenv(override=True)

# ── Page Config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="API Explainer · Vibe AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Import pipeline (after env load) ──────────────────────────────────────
from utils.helpers import run_pipeline  # noqa: E402

# ══════════════════════════════════════════════════════════════════════════
# Global CSS
# ══════════════════════════════════════════════════════════════════════════
LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&family=Crimson+Pro:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Root ──────────────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background: #F8FAFC !important;
    font-family: 'Atkinson Hyperlegible', sans-serif !important;
    color: #1E293B !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] {
    background: #1E293B !important;
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { 
    color: #ffffff !important; 
    font-family: 'Crimson Pro', serif !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Crimson Pro', serif !important;
    color: #1E293B !important;
}

/* ── Accent colours ────────────────────────────────────────────────────── */
:root {
    --accent: #2563EB;
    --ai:     #475569;
    --text:   #1E293B;
    --muted:  #64748B;
    --border: #CBD5E1;
    --surface:#FFFFFF;
}

/* ── Main heading ───────────────────────────────────────────────────────── */
.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    font-family: 'Crimson Pro', serif;
    color: #0F172A;
    margin-bottom: 0.25rem;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 0.5rem;
}
.hero-sub { color: var(--muted); font-size: 1.1rem; margin-bottom: 2rem; font-family: 'Atkinson Hyperlegible', sans-serif; }

/* ── Chips ──────────────────────────────────────────────────────────────── */
.chip-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 1.5rem; }
.chip {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 4px;
    border: 1px solid var(--accent);
    color: var(--accent);
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
    background: var(--surface);
}
.chip:hover { background: var(--accent); color: #fff; box-shadow: 2px 2px 0px rgba(37,99,235,0.2); }

/* ── Cards ──────────────────────────────────────────────────────────────── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    transition: box-shadow 0.2s, transform 0.2s;
    font-family: 'Atkinson Hyperlegible', sans-serif;
    line-height: 1.6;
}
.card:hover { box-shadow: 0 4px 6px rgba(0,0,0,0.08); transform: translateY(-1px); }

/* ── Endpoint badges ────────────────────────────────────────────────────── */
.endpoint-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 0.5rem 0 1rem; }
.badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    padding: 4px 10px;
    border-radius: 4px;
    font-weight: 600;
    white-space: nowrap;
    border: 1px solid currentColor;
}
.badge-get    { background: #F8FAFC; color: #15803d; }
.badge-post   { background: #F8FAFC; color: #1d4ed8; }
.badge-put    { background: #F8FAFC; color: #92400e; }
.badge-delete { background: #F8FAFC; color: #991b1b; }
.badge-patch  { background: #F8FAFC; color: #7c3aed; }
.badge-other  { background: #F8FAFC; color: #475569; }

/* ── Judge score pill ───────────────────────────────────────────────────── */
.score-pill {
    display: inline-block;
    padding: 6px 22px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    border: 1px solid currentColor;
}
.score-green  { background: #f0fdf4; color: #15803d; }
.score-amber  { background: #fefce8; color: #92400e; }
.score-red    { background: #fef2f2; color: #991b1b; }

/* ── Custom Alert Cards ─────────────────────────────────────────────────── */
.alert-card {
    padding: 1.25rem 1.5rem;
    border-radius: 6px;
    margin-bottom: 1rem;
    font-family: 'Atkinson Hyperlegible', sans-serif;
    line-height: 1.6;
    border-left: 4px solid;
    color: #1E293B !important;
}
.alert-info { background: #eff6ff; border-color: #3b82f6; }
.alert-warning { background: #fffbeb; border-color: #f59e0b; }
.alert-success { background: #f0fdf4; border-color: #22c55e; }

.alert-card * { color: #1E293B !important; }
.alert-card code { background: rgba(0,0,0,0.05); padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }

/* ── Custom Metric Cards ────────────────────────────────────────────────── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1rem;
}
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1rem;
    text-align: center;
}
.metric-label { font-size: 0.85rem; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.metric-val { font-size: 2rem; font-family: 'Crimson Pro', serif; font-weight: 700; color: #1E293B; margin-top: 0.25rem; }

/* ── Verdict quote ──────────────────────────────────────────────────────── */
.verdict-quote {
    font-style: italic;
    font-family: 'Crimson Pro', serif;
    font-size: 1.15rem;
    color: var(--muted);
    border-left: 3px solid var(--accent);
    padding-left: 1.25rem;
    margin-top: 1rem;
    background: #f8fafc;
    padding: 1rem 1.25rem;
    border-radius: 0 6px 6px 0;
}

/* Streamlit specific overrides */
.stTextInput input { border-radius: 6px !important; border: 1px solid var(--border) !important; font-family: 'Atkinson Hyperlegible', sans-serif !important; padding: 0.75rem 1rem !important;}
.stButton button { border-radius: 6px !important; font-family: 'Atkinson Hyperlegible', sans-serif !important; font-weight: 600 !important; padding: 0.5rem 1.5rem !important;}
[data-testid="stExpander"] * { color: #1E293B; }
[data-testid="stExpander"] { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; }
</style>
"""

DARK_CSS = """
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: #0F172A !important;
}
[data-testid="stSidebar"] {
    background: #0B0F19 !important;
    border-right: 1px solid #1E293B;
}
.card { background: #1E293B !important; border-color: #334155 !important; }
:root {
    --text:   #F8FAFC;
    --muted:  #94A3B8;
    --border: #334155;
    --surface:#1E293B;
}
h1, h2, h3, h4, h5, h6, p, label, div { color: #F8FAFC !important; }
.hero-title { color: #F8FAFC !important; border-bottom: 2px solid #334155 !important; }
.stTextInput input { background: #0B0F19 !important; color: #F8FAFC !important; border-color: #334155 !important; }
.chip { background: #1E293B; }
.badge { background: #0F172A; }
</style>
"""

# ══════════════════════════════════════════════════════════════════════════
# Sidebar
# ══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚡ API Explainer")
    st.markdown("*Powered by Agentic AI*")
    st.divider()

    dark_mode = st.checkbox("🌑 Dark Mode", value=False, key="dark_mode")
    show_logs = st.checkbox("🔬 Show Agent Reasoning", value=False, key="show_logs")

    st.divider()
    st.markdown("**About**")
    st.caption(
        "Paste an API name, URL, or describe a use-case. "
        "The AI agent will explain, generate code, and evaluate its own output."
    )
    st.divider()
    st.markdown("**Agent Pipeline**")
    for step in ["🔍 Intent", "📋 Planner", "🌐 Tavily", "⚙️ Generator", "⚖️ Judge"]:
        st.caption(step)

# ── CSS injection ──────────────────────────────────────────────────────────
st.markdown(LIGHT_CSS, unsafe_allow_html=True)
if dark_mode:
    st.markdown(DARK_CSS, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# Hero header
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<h1 class="hero-title">API Documentation Explainer</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Understand any API in under 5 minutes · '
    'Agentic · Tavily-powered · LLM-as-Judge</p>',
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════
# Input section
# ══════════════════════════════════════════════════════════════════════════
# Session state for text input pre-fill
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

user_input = st.text_input(
    label="Your query",
    value=st.session_state.user_input,
    placeholder="Paste API URL, name, or describe your use-case…",
    label_visibility="collapsed",
    key="main_input",
)

run_btn = st.button("Explain →", type="primary", use_container_width=False, key="run_btn")

# ══════════════════════════════════════════════════════════════════════════
# Pipeline execution
# ══════════════════════════════════════════════════════════════════════════
if run_btn and user_input.strip():
    status_placeholder = st.empty()

    with st.spinner("🤖 Agent pipeline running…"):
        # Live status updates
        status_msgs = []

        def update_status(msg: str):
            status_msgs.append(msg)
            status_placeholder.info("\n\n".join(status_msgs))

        update_status("🔍 Detecting intent…")
        output, evaluation, steps_log = run_pipeline(user_input.strip())
        update_status("✅ Pipeline complete!")

    status_placeholder.empty()

    # Store results in session state so the page can re-render without re-running
    st.session_state["result_output"] = output
    st.session_state["result_eval"] = evaluation
    st.session_state["result_logs"] = steps_log
    st.session_state["result_query"] = user_input.strip()

elif run_btn and not user_input.strip():
    st.warning("Please enter an API name, URL, or use-case before running.")

# ══════════════════════════════════════════════════════════════════════════
# Results rendering
# ══════════════════════════════════════════════════════════════════════════
if "result_output" in st.session_state:
    output: dict = st.session_state["result_output"]
    evaluation: dict = st.session_state["result_eval"]
    steps_log: list = st.session_state["result_logs"]

    st.divider()

    # ── Agent reasoning log ────────────────────────────────────────────
    if show_logs:
        with st.expander("🧠 Agent Reasoning Log", expanded=False):
            for line in steps_log:
                st.write(line)

    # 1. API Name & Fit Analysis
    api_name = output.get("api_name", "API Name")
    st.markdown(f"### 📄 {api_name} - Fit Analysis")
    st.markdown(
        f'<div class="card">{output.get("api_fit_analysis", "Analysis not available.")}</div>',
        unsafe_allow_html=True,
    )

    # 2. API Comparison Table
    if output.get("api_comparison_table") and output["api_comparison_table"] != "N/A":
        st.markdown("### 📊 API Comparison Table")
        st.markdown(output["api_comparison_table"])

    # 3. Authentication
    if output.get("authentication") and output["authentication"] != "N/A":
        st.markdown("### 🔐 Authentication (Step-by-Step)")
        st.markdown(f'<div class="alert-card alert-info">{output["authentication"]}</div>', unsafe_allow_html=True)

    # 4. Endpoint Playground
    playground = output.get("endpoint_playground")
    if playground and isinstance(playground, dict) and playground.get("url") != "N/A":
        st.markdown("### 🛝 Endpoint Playground")
        st.markdown(f"**URL:** `{playground.get('url', 'N/A')}`")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Parameters**")
            st.markdown(playground.get("params", "N/A"))
            st.markdown("**Example Request**")
            st.code(playground.get("example_request", ""), language="bash")
        with col2:
            st.markdown("**Sample JSON Response**")
            st.code(playground.get("sample_json_response", ""), language="json")
            st.markdown("**Field Explanation**")
            st.markdown(playground.get("field_explanation", "N/A"))

    # 5. Code Workbench
    if output.get("code") and any(output.get("code", {}).values()):
        st.markdown("### 💻 Code Workbench")
        code = output.get("code", {})
        tab_py, tab_js = st.tabs(["Python", "JavaScript"])
        with tab_py:
            st.code(code.get("python", "# No Python code generated"), language="python")
        with tab_js:
            st.code(code.get("javascript", "// No JavaScript code generated"), language="javascript")

    # 6. Location Data Guide
    if output.get("location_data_guide") and output["location_data_guide"] != "N/A":
        st.markdown("### 📍 How to Get Data for User's Location")
        st.markdown(f'<div class="card">{output["location_data_guide"]}</div>', unsafe_allow_html=True)

    # 7. Limitations & Gotchas
    if output.get("limitations_and_gotchas") and output["limitations_and_gotchas"] != "N/A":
        st.markdown("### ⚠️ Limitations & Gotchas")
        st.markdown(f'<div class="alert-card alert-warning">{output["limitations_and_gotchas"]}</div>', unsafe_allow_html=True)

    # 8. Final Recommendation
    if output.get("final_recommendation") and output["final_recommendation"] != "N/A":
        st.markdown("### 🎯 Final Recommendation")
        st.markdown(f'<div class="alert-card alert-success">{output["final_recommendation"]}</div>', unsafe_allow_html=True)

    # 7I — LLM-as-Judge Panel (Moved to bottom expander)
    with st.expander("⚖️ View AI Quality Evaluation", expanded=False):
        overall = evaluation.get("overall", 5)
        score_class = (
            "score-green" if overall >= 8
            else "score-amber" if overall >= 5
            else "score-red"
        )
        st.markdown(
            f'<div class="score-pill {score_class}" style="margin-bottom:1.5rem;">Overall Score: {overall}/10</div>',
            unsafe_allow_html=True,
        )

        metrics = {
            "Accuracy": evaluation.get("accuracy", 5),
            "Completeness": evaluation.get("completeness", 5),
            "Clarity": evaluation.get("clarity", 5),
            "Code Usability": evaluation.get("code_usability", 5),
        }
        
        metrics_html = '<div class="metric-grid">'
        for label, score in metrics.items():
            metrics_html += f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-val">{score}/10</div></div>'
        metrics_html += '</div>'
        
        st.markdown(metrics_html, unsafe_allow_html=True)

        verdict = evaluation.get("verdict", "")
        if verdict:
            st.markdown(
                f'<div class="verdict-quote">"{verdict}"</div>',
                unsafe_allow_html=True,
            )

elif not run_btn:
    # Placeholder state — show a friendly empty state
    st.markdown(
        """
        <div style="text-align:center; padding: 3rem; color: #64748B;">
            <div style="font-size:3rem;">🚀</div>
            <p>Enter an API name, URL, or use-case above and click <strong>Explain →</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
