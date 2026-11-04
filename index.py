"""
The web API. Vercel finds the FastAPI `app` in this file and serves it.

Endpoints:
  GET  /           -> the test chat page (public/index.html)
  GET  /api/health -> quick "is it alive?" check
  POST /api/chat   -> send {"message": "...", "session_id": "..."}; get the answer
"""

import os
import uuid

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

load_dotenv()

from google.adk.runners import InMemoryRunner  # noqa: E402
from google.genai import types  # noqa: E402

from ask_bright.agent import root_agent  # noqa: E402

APP_NAME = "ask_bright"
runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)

app = FastAPI(title="Ask Bright")

# CORS = which websites may call this API from the browser.
# Set ALLOWED_ORIGINS on Vercel to your real domain, e.g. https://brightajiboye.com
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    session_id: str
    sources: list[dict]


@app.get("/")
def home():
    return FileResponse(os.path.join(os.path.dirname(__file__), "public", "index.html"))


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    user_id = "visitor"
    session_id = req.session_id or str(uuid.uuid4())

    # Reuse the conversation if we still have it, otherwise start a new one.
    # (On Vercel, memory resets between cold starts, so this is "best effort".)
    session = await runner.session_service.get_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id
    )
    if session is None:
        await runner.session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

    message = types.Content(role="user", parts=[types.Part(text=req.message)])
    answer, sources = "", []

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=message
        ):
            # Collect the sources the tool returned, so the UI can show links
            for resp in event.get_function_responses() or []:
                for r in (resp.response or {}).get("results", []):
                    if r["title"] not in [s["title"] for s in sources]:
                        sources.append({"title": r["title"], "url": r["url"]})
            if event.is_final_response() and event.content and event.content.parts:
                answer = "".join(p.text or "" for p in event.content.parts)
    except Exception as exc:  # show a clean error instead of crashing
        raise HTTPException(status_code=500, detail=f"Agent error: {exc}") from exc

    return ChatResponse(answer=answer.strip(), session_id=session_id, sources=sources)
