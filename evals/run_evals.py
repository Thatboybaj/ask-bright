"""
Retrieval eval: does search find the RIGHT case study for each question?

For each test question we check whether the top result comes from the file we
expected. For questions with expected_source = null, the correct behaviour is
to find NOTHING relevant (so the bot says "I don't know").

Run:  python evals/run_evals.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(ROOT / ".env")

from ask_bright.retrieval import search  # noqa: E402

cases = json.loads((ROOT / "evals" / "questions.json").read_text())
passed = 0

for case in cases:
    results = search(case["question"], top_k=1)
    got = results[0]["source"] if results else None
    score = results[0]["score"] if results else 0
    ok = got == case["expected_source"]
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  [{score:.2f}]  {case['question']}  -> got {got}, expected {case['expected_source']}")

print(f"\nRetrieval accuracy: {passed}/{len(cases)} ({passed / len(cases):.0%})")
