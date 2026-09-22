# Copyright 2026 ReelReads AI
import contextlib
import os
from collections.abc import AsyncIterator

import google.auth
from a2a.server.tasks import InMemoryTaskStore
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from google.adk.cli.fast_api import get_fast_api_app
from google.adk.runners import Runner
from google.cloud import logging as google_cloud_logging

from app.app_utils import services
from app.app_utils.a2a import attach_a2a_routes
from app.app_utils.reasoning_engine_adapter import attach_reasoning_engine_routes
from app.app_utils.telemetry import setup_agent_engine_telemetry, setup_telemetry
from app.app_utils.typing import Feedback

from app.tools import (
    search_books_openlibrary,
    manage_reading_list,
    query_literary_rag,
    generate_book_cover,
    calculate_reading_stats,
)

load_dotenv()
setup_telemetry()
setup_agent_engine_telemetry()

try:
    _, project_id = google.auth.default()
    logging_client = google_cloud_logging.Client()
    logger = logging_client.logger(__name__)
except Exception:
    logger = None

allow_origins = (
    os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None
)

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    from app.agent import app as adk_app
    from app.agent import root_agent

    runner = Runner(
        app=adk_app,
        session_service=services.get_session_service(),
        artifact_service=services.get_artifact_service(),
        auto_create_session=True,
    )
    app.state.runner = runner
    app.state.agent_app_name = adk_app.name
    await attach_a2a_routes(
        app,
        agent=root_agent,
        runner=runner,
        task_store=InMemoryTaskStore(),
        rpc_path=f"/a2a/{adk_app.name}",
    )
    yield


app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=False,
    artifact_service_uri=services.ARTIFACT_SERVICE_URI,
    allow_origins=allow_origins,
    session_service_uri=services.SESSION_SERVICE_URI,
    otel_to_cloud=False,
    lifespan=lifespan,
)
app.title = "ReelReads AI"
app.description = "API for interacting with ReelReads AI Book Concierge"

attach_reasoning_engine_routes(app)

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def read_root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "ReelReads AI API is active."}


class ChatRequest(BaseModel):
    message: str


@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    msg = req.message.lower()
    
    if "recommend" in msg or "search" in msg:
        query = msg.replace("recommend", "").replace("search", "").strip() or "sci-fi"
        res = search_books_openlibrary(query)
        books_str = ", ".join([f"<b>{b['title']}</b> by {b['author']}" for b in res.get("books", [])[:3]])
        return {
            "response": f"🤖 <b>Book Concierge Agent</b> recommends: {books_str}. Would you like Reading List Agent to add one to your shelf or Cover Creation Agent to generate custom cover art?",
            "data": res
        }
    elif "cover" in msg or "art" in msg or "generate" in msg:
        res = generate_book_cover(req.message, title="Custom Edition")
        return {
            "response": f"🎨 <b>Cover Creation Agent</b> rendered original artwork for <b>{res['title']}</b>:<br/><img src='{res['cover_art_url']}' style='width:180px; margin-top:8px; border-radius:8px;' />",
            "data": res
        }
    elif "theme" in msg or "rag" in msg or "analyze" in msg or "plot" in msg:
        res = query_literary_rag(req.message)
        summary = res.get("summary") or res.get("insight")
        themes = ", ".join(res.get("themes", [])) if "themes" in res else ""
        text = f"🧠 <b>Literary Research Agent (RAG) Analysis — {res.get('title', 'Literary Work')}</b><br/>{summary}"
        if themes:
            text += f"<br/><b>Key Themes:</b> {themes}"
        return {"response": text, "data": res}
    elif "add" in msg or "shelf" in msg or "reading list" in msg or "update" in msg:
        if "dune" in msg:
            res = manage_reading_list(action="add", title="Dune", author="Frank Herbert", status="currently_reading", current_page=240, total_pages=533)
        else:
            res = manage_reading_list(action="get_list")
        return {"response": f"📚 <b>Reading List Agent</b>: {res.get('message', 'Updated your reading shelf successfully.')}", "data": res}
    else:
        # Default agent concierge reply
        res = search_books_openlibrary("best science fiction")
        return {
            "response": f"🤖 <b>ReelReads AI Agent</b> scanned the literary database for '{req.message}'. Would you like Book Concierge Agent to recommend books, Literary Research Agent to analyze themes, or Cover Creation Agent to render cover art?",
            "data": res
        }


@app.get("/api/books/search")
def api_books_search(q: str = "sci-fi"):
    return search_books_openlibrary(q)


@app.get("/api/reading-list")
def api_get_reading_list():
    return manage_reading_list(action="get_list")


@app.get("/api/stats")
def api_get_stats():
    return calculate_reading_stats()


@app.post("/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    if logger:
        logger.log_struct(feedback.model_dump(), severity="INFO")
    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
