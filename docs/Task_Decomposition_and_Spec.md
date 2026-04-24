# Task Decomposition & System Specification

## 1. System Overview
The **API Documentation Explainer Agent** is a modular AI system built to understand user queries about APIs, retrieve live documentation from the web, generate structured technical guides, and evaluate its own output.

## 2. Task Decomposition (Agentic Workflow)

The system's workload is broken down into five distinct, specialized agentic tasks:

### Task 1: Intent Classification (`intent_agent.py`)
- **Objective**: Determine exactly what the user wants to do.
- **Execution**: Uses a fast LLM (Groq Llama-3) to classify the input into one of three intents: `explain_api`, `compare_api`, or `recommend_api`.
- **Output**: A structured JSON specifying the intent type.

### Task 2: Execution Planning (`planner_agent.py`)
- **Objective**: Create a step-by-step reasoning plan.
- **Execution**: Takes the intent and generates a logical sequence of actions (e.g., "1. Identify target API, 2. Search for auth methods, 3. Draft code snippet").
- **Output**: A list of string-based reasoning steps.

### Task 3: Knowledge Retrieval (`tool_agent.py`)
- **Objective**: Fetch the most accurate, live documentation.
- **Execution**: Utilizes the **Tavily Search API** to scour the web for official documentation, GitHub repos, and developer guides based on the user's query.
- **Output**: A concatenated string of relevant markdown/text data from the web.

### Task 4: Content Generation (`generator_agent.py`)
- **Objective**: Synthesize the retrieved data into a structured output.
- **Execution**: Uses a high-context LLM (Gemini 2.5 Flash) to parse the raw web data and map it perfectly to a strict JSON schema depending on the intent (Explain, Compare, or Recommend).
- **Output**: A heavily structured JSON containing summaries, endpoint details, and functional code (Python/JS).

### Task 5: Output Evaluation (`judge_agent.py`)
- **Objective**: Perform quality assurance on the generated guide.
- **Execution**: Implements an **LLM-as-a-Judge** pattern. A separate, objective LLM reviews the generator's JSON output, scoring it from 1-10 on Accuracy, Clarity, and Code Quality.
- **Output**: A JSON scorecard with feedback and an overall rating.

---

## 3. Technical Specification

### 3.1 Core Technologies
- **Frontend**: Streamlit Community Cloud (with custom HTML/CSS cards for a premium UI)
- **Primary LLM (Speed)**: Groq API (`llama-3.3-70b-versatile`)
- **Secondary LLM (Context)**: Google Gemini API (`gemini-2.5-flash`)
- **Local Fallback**: Ollama (`llama3.1` / `llama3.2`)
- **Search Tool**: Tavily Search API

### 3.2 Load Balancing Strategy
The architecture uses provider-specific routing:
- **Groq** handles lightweight, fast tasks: Intent, Planning, and Judging.
- **Gemini** handles heavy lifting: processing 10k+ tokens of web search data and generating massive JSON schemas.
- **Ollama** can be toggled via `LLM_PROVIDER=ollama` to run the entire pipeline 100% locally on user hardware.

### 3.3 UI Specifications
- **Dynamic Interface**: The UI morphs based on the Intent. If the intent is `compare_api`, it renders markdown tables. If it's `explain_api`, it renders interactive Endpoint Playgrounds.
- **Transparency**: A sidebar logs the exact thought process and pipeline execution steps of the agent, giving the user insight into the AI's reasoning.
