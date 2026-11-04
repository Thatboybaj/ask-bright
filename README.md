# Ask Bright

An AI assistant that answers questions about my web design and development work, grounded in my own case studies. Built with **Google ADK**, **Gemini**, and **retrieval-augmented generation (RAG)**, deployed on **Vercel**.

**Live demo:** https://YOUR-PROJECT.vercel.app

---

## What it does

Visitors to my portfolio can ask things like *"Has Bright built custom code components?"* and get a short answer drawn only from my real project write-ups, with links to the sources it used. If the answer isn't in my case studies, the assistant says so instead of making something up.

## How it works

```
Visitor question
      │
      ▼
FastAPI  /api/chat  ──►  ADK agent (Gemini)
                              │  decides to call the tool
                              ▼
                      search_portfolio(query)
                              │  embed query → cosine similarity
                              ▼
                      index.json (pre-embedded case-study chunks)
                              │  top matches
                              ▼
                      Gemini writes the answer from those passages
      │
      ▼
Answer + source links
```

1. **Indexing (offline).** `scripts/build_index.py` splits each Markdown case study into section-sized chunks and embeds them with `gemini-embedding-001`. The vectors are saved to `index.json`.
2. **Retrieval (per request).** The question is embedded and compared against every chunk with cosine similarity. Chunks below a relevance threshold are dropped.
3. **Generation.** An ADK agent with one tool, `search_portfolio`, retrieves passages and answers only from them, citing its sources.

## Design decisions

| Decision | Why |
|---|---|
| JSON file instead of a vector database | Under 50 chunks, a brute-force search in plain Python is fast and removes an external dependency. A vector DB is the next step if the knowledge base grows. |
| Chunking by `##` section | Case studies are already structured by topic, so section boundaries keep each chunk focused and meaningful. |
| Title prepended to every chunk | Keeps project context attached to small chunks so retrieval knows which project a detail belongs to. |
| Relevance threshold (`MIN_SCORE`) | Lets the agent refuse out-of-scope questions instead of answering from weak matches. |
| Retrieval exposed as an agent tool | The model decides when to search and can search more than once for multi-part questions. |
| Separate `RETRIEVAL_DOCUMENT` / `RETRIEVAL_QUERY` task types | Gemini embeddings are tuned differently for stored text and for questions, which improves matching. |

## Evaluation

`evals/run_evals.py` runs 15 test questions and checks whether retrieval returns the correct case study, including two questions that should return **nothing** (out-of-scope).

```
Retrieval accuracy: XX/15 (XX%)
```

## Run it locally

Requires Python 3.10+ and a free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

```bash
git clone https://github.com/YOUR-USERNAME/ask-bright.git
cd ask-bright
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # then paste your GOOGLE_API_KEY into .env
python scripts/build_index.py     # builds index.json
uvicorn index:app --reload        # open http://localhost:8000
```

Test the agent on its own with ADK's developer UI:

```bash
adk web
```

## Project structure

```
ask_bright/
  agent.py         ADK agent, system instructions, search tool
  retrieval.py     Embedding search over index.json
knowledge/         Case studies in Markdown (the source of truth)
scripts/
  build_index.py   Chunks + embeds knowledge/ into index.json
evals/             Test questions and retrieval eval script
public/index.html  Chat UI
index.py           FastAPI app (Vercel entrypoint)
```

## Tech stack

Python · Google ADK · Gemini 2.5 Flash · Gemini Embeddings · FastAPI · Vercel

## Next steps

- Stream responses token by token
- Embed as a Framer code component on my portfolio
- Add a lead-capture tool so visitors can send a project brief
- Grow the eval set and track answer quality, not just retrieval

---

Built by [Bright Ajiboye](https://brightajiboye.com) · [LinkedIn](https://www.linkedin.com/in/bright-ajiboye/)
