"""
STEP 2 OF RAG: search the index.

Turns the user's question into an embedding, compares it with every chunk
in index.json, and returns the closest matches.
"""

import json
import math
import os
from functools import lru_cache
from pathlib import Path

from google import genai
from google.genai import types

INDEX_FILE = Path(__file__).resolve().parent.parent / "index.json"
EMBED_MODEL = os.getenv("EMBED_MODEL", "gemini-embedding-001")
MIN_SCORE = 0.67  # below this, a chunk is treated as "not relevant"


@lru_cache(maxsize=1)
def load_index() -> list[dict]:
    """Load index.json once and keep it in memory."""
    return json.loads(INDEX_FILE.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    return genai.Client()


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """How similar two embeddings are: 1.0 = same meaning, 0 = unrelated."""
    dot = sum(x * y for x, y in zip(a, b))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm if norm else 0.0


def embed_query(question: str) -> list[float]:
    result = get_client().models.embed_content(
        model=EMBED_MODEL,
        contents=question,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    return result.embeddings[0].values


def rank(query_vector: list[float], top_k: int = 4) -> list[dict]:
    """Score every chunk and return the best matches (no API call)."""
    scored = [
        {**{k: v for k, v in rec.items() if k != "embedding"},
         "score": round(cosine_similarity(query_vector, rec["embedding"]), 3)}
        for rec in load_index()
    ]
    scored.sort(key=lambda r: r["score"], reverse=True)
    return [r for r in scored[:top_k] if r["score"] >= MIN_SCORE]


def search(question: str, top_k: int = 8) -> list[dict]:
    return rank(embed_query(question), top_k)
