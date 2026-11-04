"""
STEP 1 OF RAG: build the search index.

What it does:
  1. Reads every .md file in /knowledge
  2. Splits each file into small "chunks" (one per section)
  3. Turns each chunk into an embedding (a list of numbers that captures meaning)
  4. Saves everything to index.json

Run it whenever you edit the knowledge files:
    python scripts/build_index.py
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # reads GOOGLE_API_KEY from your .env file

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = ROOT / "knowledge"
INDEX_FILE = ROOT / "index.json"
EMBED_MODEL = os.getenv("EMBED_MODEL", "gemini-embedding-001")


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


def main() -> None:
    client = genai.Client()  # uses GOOGLE_API_KEY automatically
    records = []

    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        meta, body = read_front_matter(path.read_text(encoding="utf-8"))
        title = meta.get("title", path.stem)
        for i, chunk in enumerate(split_into_chunks(body)):
            # Prefix the title so every chunk knows which project it belongs to
            records.append({
                "id": f"{path.stem}-{i}",
                "source": path.stem,
                "title": title,
                "url": meta.get("url", ""),
                "text": f"{title}\n{chunk}",
            })

    print(f"Embedding {len(records)} chunks from {KNOWLEDGE_DIR.name}/ ...")
    result = client.models.embed_content(
        model=EMBED_MODEL,
        contents=[r["text"] for r in records],
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )
    for record, emb in zip(records, result.embeddings):
        record["embedding"] = emb.values

    INDEX_FILE.write_text(json.dumps(records), encoding="utf-8")
    print(f"Saved {INDEX_FILE.name} ({len(records)} chunks)")


if __name__ == "__main__":
    main()
