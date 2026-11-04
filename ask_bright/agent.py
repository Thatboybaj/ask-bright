"""
The ADK agent: the "brain" of Ask Bright.

It has ONE tool, search_portfolio. When a visitor asks something, Gemini
decides to call the tool, reads the matching chunks, and answers from them.
That pattern (retrieve, then generate) is called RAG.
"""

import os

from google.adk.agents import Agent

from google.genai import types

from .retrieval import search

MODEL = os.getenv("CHAT_MODEL", "gemini-3.8-flash")


def search_portfolio(query: str) -> dict:
    """Search Bright's case studies, services and background.

    Args:
        query: What to look for, e.g. "Framer CMS projects" or "certifications".

    Returns:
        A dict with a list of matching passages, each with its title, url and text.
    """
    results = search(query)
    if not results:
        return {"status": "no_results", "results": []}
    return {
        "status": "ok",
        "results": [
            {"title": r["title"], "url": r["url"], "text": r["text"]}
            for r in results
        ],
    }


INSTRUCTION = """
You are "Ask Bright", an assistant on Bright Ajiboye's portfolio website.
Visitors are potential clients and recruiters.

Rules:
1. ALWAYS call search_portfolio before answering a question about Bright,
   his projects, skills, services or background.
2. Answer ONLY from what the tool returns. Never invent projects, clients,
   numbers or skills.
3. If the tool finds nothing relevant, say you don't have that information
   and suggest contacting Bright via brightajiboye.com.
4. Keep answers short: 2-4 sentences, friendly and professional.
5. End with "Sources:" and the title of each passage you used.
6. Politely decline questions unrelated to Bright's work.
"""

# ADK looks for a variable called root_agent. Don't rename it.
# Retry automatically when Google's servers are busy (429/500/503),
# waiting a little longer between each attempt.
RETRY = types.GenerateContentConfig(
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            attempts=5,
            initial_delay=1.0,
            http_status_codes=[429, 500, 503],
        )
    )
)

# ADK looks for a variable called root_agent. Don't rename it.
root_agent = Agent(
    name="ask_bright",
    model=MODEL,
    description="Answers questions about Bright's web design and development work.",
    instruction=INSTRUCTION,
    tools=[search_portfolio],
    generate_content_config=RETRY,
)