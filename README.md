# API Documentation Explainer Agent

> An agentic AI web app that understands, explains, and evaluates any API in under 5 minutes.

[![Live Demo](https://img.shields.io/badge/Live-Railway-blueviolet)](https://your-railway-url.railway.app)

---

## 📌 Overview

The **API Documentation Explainer Agent** is a production-grade agentic system that:

- **Explains** any API (by URL, name, or use-case) with deep technical detail.
- **Compares** multiple APIs side-by-side with contrastive analysis.
- **Generates** ready-to-use code examples in Python, JavaScript, and cURL.
- **Recommends** the best APIs for specific problems.
- **Evaluates** its own output quality using an **LLM-as-Judge**.

---

## 🏗️ Architecture

The system uses a **Multi-Provider Load Balancing** architecture to ensure maximum speed and reliability:

```
User Input
    │
    ▼
Intent Agent (Groq)    ← ultra-fast classification
    │
    ▼
Planner Agent (Groq)   ← builds execution steps
    │
    ▼
Tool Agent (Tavily)    ← fetches live data via Web Search
    │
    ▼
Generator Agent (Gemini) ← high-context JSON generation (w/ Multi-Key Rotation)
    │
    ▼
Judge Agent (Groq)     ← critical evaluation & scoring
    │
    ▼
Streamlit UI           ← Premium CSS, Crimson Pro typography, Custom HTML Cards
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/api-doc-explainer.git
cd api-doc-explainer
```

### 2. Configure environment

Create a `.env` file and fill in your keys:

```
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here
GEMINI_API_KEYS=key1,key2,key3 # Supports automatic rotation & retry
TAVILY_API_KEY=your_key_here
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run locally

```bash
streamlit run app.py
```

---

## 🔀 Smart Load Balancing

| Agent | Provider | Model | Rationale |
|-------|----------|-------|-----------|
| **Intent / Planner** | Groq | `llama-3.3-70b` | Near-instant response (<500ms) |
| **Generator** | Gemini | `gemini-2.5-flash` | Superior 1M+ context window & instruction following |
| **Judge** | Groq | `llama-3.3-70b` | Objective, fast scoring |

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

---

## 🚀 Deployment (Railway)

1. Push to GitHub
2. Create a new Railway project → connect your repo
3. Add environment variables: `LLM_PROVIDER`, `GROQ_API_KEY`, `GEMINI_API_KEYS`, `TAVILY_API_KEY`
4. Railway auto-detects the `Procfile` and deploys

---

## 📁 Project Structure

```
api-doc-explainer/
├── app.py                 ← Streamlit entry point (Premium UI)
├── agents/
│   ├── intent_agent.py    ← Intent classification (Groq)
│   ├── planner_agent.py   ← Step planning (Groq)
│   ├── tool_agent.py      ← Tavily search wrapper
│   ├── generator_agent.py ← JSON generation (Gemini)
│   └── judge_agent.py     ← Evaluation (Groq)
├── llm/
│   ├── base.py            ← Abstract LLMClient
│   ├── groq_client.py     ← Groq backend (Lightning speed)
│   ├── gemini_client.py   ← Gemini backend (Multi-key support)
│   └── ollama_client.py   ← Local fallback
├── tools/
│   └── tavily_tool.py     ← Tavily search wrapper
├── utils/
│   └── helpers.py         ← Pipeline orchestrator
├── tests/
│   └── test_agents.py     ← Unit + integration tests
├── Procfile               ← Railway deployment
├── requirements.txt
└── .env
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit + Custom HTML/CSS Cards |
| **Typography** | Crimson Pro & Atkinson Hyperlegible |
| **Inference ⚡** | **Groq** (llama-3.3-70b-versatile) |
| **Reasoning 🧠** | **Google Gemini 2.5 Flash** |
| **Search tool** | Tavily Search API |
| **Deployment** | Railway |
