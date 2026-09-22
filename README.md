# ReelReads AI Agent — Book Concierge & Literary Platform

**ReelReads AI Agent** is an autonomous, agent-first book concierge and literary analysis application powered by Google Agent Development Kit (**ADK**) and **Gemini**.


### Check video recording of the working demo
reelreads_demo.webm file in the root location , download the file and play.


It combines real-time book discovery, grounded RAG Q&A, custom AI cover art generation, and personalized reading progress tracking into a sleek dark-mode web application.

![ReelReads AI Agent Demo](demo.gif)

---

## ✨ Features & Capabilities

- **🤖 Book Concierge Agent**: Live book search, metadata retrieval, ratings, and author information powered by the **Open Library API**.
- **🧠 Literary Research Agent**: Deep grounded thematic analysis, plot breakdowns, and character arcs powered by **Vertex AI RAG Engine**.
- **🎨 Cover Creation Agent**: Original custom book cover posters generated on demand using **Gemini Image Studio** (`gemini-3.1-flash-lite-image`).
- **📚 Reading List Agent**: Shelf tracking ("want_to_read", "currently_reading", "read") with reading page percentages stored in **Cloud Firestore**.
- **🧠 Preference Memory Bank**: Stores reading pace, favorite genres, and authors across sessions using **Vertex AI Memory Bank**.
- **📊 Reading Velocity Sandbox**: Computes estimated completion dates, reading pace, and reading velocity metrics.
- **🎴 Rich A2UI Interface**: Structured cards and carousels for visual book discovery and shelf rendering.

---

## 🏗️ Architecture

```text
+-------------------------------------------------------------+
|                  ReelReads AI Web Application              |
|                 (FastAPI + Static Dark Frontend)            |
+------------------------------+------------------------------+
                               | /api/chat
                               v
+-------------------------------------------------------------+
|              ADK Root Agent (app/agent.py)                  |
+----------+-------------------+------------------+-----------+
           |                   |                  |
           v                   v                  v
    [Open Library API]  [Vertex AI RAG]   [Gemini Image Studio]
    Live Book Search    Grounded Q&A      Custom Cover Art
```

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
- Python 3.11+
- Virtual environment set up with dependencies in `pyproject.toml`

### 2. Installation
```bash
git clone https://github.com/cszhu/build-with-gemini.git
cd reelreads-ai
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3. Run Application Locally
```bash
python -m uvicorn app.fast_api_app:app --host 0.0.0.0 --port 8000
```
Open your browser and navigate to:
`http://localhost:8000/static/index.html`

---

## 🧪 Testing

Run the automated pytest test suite:
```bash
pytest tests/test_reelreads.py
```

---

## ☁️ Deployment

### Deploy Agent to Agent Platform
```bash
agents-cli deploy --project qwiklabs-gcp-01-2eb132f631d3 --region us-east1
```

### Deploy Frontend to Cloud Run
```bash
gcloud run deploy reelreads-ai-frontend \
  --source . \
  --region us-east1 \
  --allow-unauthenticated
```

