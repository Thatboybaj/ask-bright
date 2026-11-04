"""
STEP 1 OF RAG: build the search index.

What it does:
  1. Reads every .md file in /knowledge (including knowledge/site/)
  2. Splits each file into small "chunks" (one per section)
  3. Turns each chunk into an embedding (a list of numbers that captures meaning)
  4. Saves everything to index.json

Only NEW or CHANGED chunks are sent to Gemini. Unchanged chunks reuse the
embedding already saved in index.json. That keeps runs fast and inside the
free-tier limit (100 embeddings per minute).

    python scripts/build_index.py
"""

import hashlib
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # reads GOOGLE_API_KEY from your .env file

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = ROOT / "knowledge"
INDEX_FILE = ROOT / "index.json"
EMBED_MODEL = os.getenv("EMBED_MODEL", "gemini-embedding-001")
BATCH_SIZE = 90        # stay under the free tier's 100 embeddings per minute
PAUSE_SECONDS = 62     # wait between batches so the per-minute limit resets


def read_front_matter(text: str) -> tuple[dict, str]:
    """Pull the title/url block (between --- lines) off the top of a file."""
    meta = {}
    if text.startswith("---"):
        _, header, body = text.split("---", 2)
        for line in header.strip().splitlines():
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
        return meta, body.strip()
    return meta, text


def split_into_chunks(body: str) -> list[str]:
    """Split on '## ' headings so each chunk is one focused section."""
    chunks, current = [], []
    for line in body.splitlines():
        if line.startswith("## ") and current:
            chunks.append("\n".join(current).strip())
            current = []
        current.append(line)
    if current:
        chunks.append("\n".join(current).strip())
    return [c for c in chunks if c]


def fingerprint(text: str) -> str:
    """A short ID that changes whenever the text changes."""
    return hashlib.sha256(f"{EMBED_MODEL}\n{text}".encode()).hexdigest()[:16]


def load_cache() -> dict[str, list[float]]:
    """Embeddings from the previous index.json, keyed by fingerprint."""
    if not INDEX_FILE.exists():
        return {}
    try:
        old = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {r["hash"]: r["embedding"] for r in old if "hash" in r and "embedding" in r}


def main() -> None:
    records = []

    # rglob = also look inside subfolders, like knowledge/site/
    for path in sorted(KNOWLEDGE_DIR.rglob("*.md")):
        meta, body = read_front_matter(path.read_text(encoding="utf-8"))
        title = meta.get("title", path.stem)
        for i, chunk in enumerate(split_into_chunks(body)):
            text = f"{title}\n{chunk}"  # title keeps each chunk tied to its project
            records.append({
                "id": f"{path.stem}-{i}",
                "source": path.stem,
                "title": title,
                "url": meta.get("url", ""),
                "text": text,
                "hash": fingerprint(text),
            })

    cache = load_cache()
    todo = []
    for r in records:
        if r["hash"] in cache:
            r["embedding"] = cache[r["hash"]]  # unchanged: reuse
        else:
            todo.append(r)                     # new or edited: embed

    print(f"{len(records)} chunks: {len(records) - len(todo)} unchanged, {len(todo)} to embed")

    if todo:
        client = genai.Client()  # uses GOOGLE_API_KEY automatically
        for n, start in enumerate(range(0, len(todo), BATCH_SIZE)):
            if n > 0:
                print(f"  waiting {PAUSE_SECONDS}s for the rate limit to reset...")
                time.sleep(PAUSE_SECONDS)
            batch = todo[start:start + BATCH_SIZE]
            result = client.models.embed_content(
                model=EMBED_MODEL,
                contents=[r["text"] for r in batch],
                config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
            )
            for record, emb in zip(batch, result.embeddings):
                record["embedding"] = emb.values
            print(f"  embedded {start + len(batch)}/{len(todo)}")

    # Chunks from deleted files simply aren't in `records`, so they drop out.
    INDEX_FILE.write_text(json.dumps(records), encoding="utf-8")
    print(f"Saved {INDEX_FILE.name} ({len(records)} chunks)")


if __name__ == "__main__":
    main()