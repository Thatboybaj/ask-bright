"""
Sync case studies from the live portfolio site into knowledge/site/.

What it does:
  1. Reads the site's sitemap.xml (Framer creates one automatically)
  2. Picks every case study page (URLs under /work/<name>)
  3. Downloads each page and keeps only the real content
     (drops menus, footers, buttons and Framer's duplicated mobile/tablet copies)
  4. Rewrites knowledge/site/ FROM SCRATCH, so deleted case studies disappear too

Then run build_index.py to re-embed everything.

    python scripts/sync_site.py
"""

import re
import shutil
import urllib.request
import xml.etree.ElementTree as ET
import ssl
import certifi
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

SITE = "https://brightajiboye.com"
CASE_STUDY_PATH = re.compile(r"^/work/[^/]+/?$")  # /work/sable-records, not /work
EXTRA_PAGES = ["/info"]  # other pages worth knowing about (add or remove freely)
TITLE_SUFFIX = " - Bright Ajiboye"

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "knowledge" / "site"
HEADERS = {"User-Agent": "AskBrightSync/1.0"}


SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30, context=SSL_CONTEXT) as res:
        return res.read().decode("utf-8", errors="ignore")

def page_urls() -> list[str]:
    """Case study URLs from the sitemap, plus EXTRA_PAGES."""
    xml = fetch(f"{SITE}/sitemap.xml")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text.strip() for loc in ET.fromstring(xml).findall(".//s:loc", ns)]
    paths = {re.sub(r"^https?://[^/]+", "", u) or "/" for u in urls}
    picked = sorted(p for p in paths if CASE_STUDY_PATH.match(p))
    picked += [p for p in EXTRA_PAGES if p in paths]
    return [SITE + p for p in picked]


def extract(html: str) -> tuple[str, list[str]]:
    """Return (title, lines) where lines are Markdown-ish text in page order."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "nav", "header", "footer"]):
        tag.decompose()

    title = (soup.title.string or "").strip() if soup.title else ""
    title = title.removesuffix(TITLE_SUFFIX).strip()

    lines, seen = [], set()
    for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
        # skip elements nested inside another element we already take
        if el.find_parent(["p", "li", "h1", "h2", "h3", "h4"]):
            continue
        text = " ".join(el.get_text(" ", strip=True).split())
        if not text or text in seen:  # Framer repeats content per breakpoint
            continue
        seen.add(text)
        if el.name == "h1":
            lines.append(f"# {text}")
        elif el.name in ("h3", "h4"):
            lines.append(f"## {text}")  # section headings → chunk boundaries
        else:
            lines.append(text)
    return title, lines


def main() -> None:
    urls = page_urls()
    print(f"Found {len(urls)} pages")
    pages = []
    for url in urls:
        title, lines = extract(fetch(url))
        pages.append((url, title or url.rsplit("/", 1)[-1], lines))
        print(f"  {url}  ({len(lines)} lines)")

    # Lines that appear on most pages are site chrome ("Book a Call", "© 2026"…)
    counts = Counter(line for _, _, lines in pages for line in set(lines))
    # Headings are never boilerplate: every case study has "## Overview" etc.
    boilerplate = {
        l for l, n in counts.items()
        if len(pages) > 2 and n > len(pages) / 2 and not l.startswith("#")
    }

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)  # start fresh so removed pages vanish
    OUT_DIR.mkdir(parents=True)

    for url, title, lines in pages:
        body = [l for l in lines if l not in boilerplate and len(l) > 2]
        slug = url.rstrip("/").rsplit("/", 1)[-1]
        content = f"---\ntitle: {title}\nurl: {url}\n---\n\n" + "\n\n".join(body) + "\n"
        (OUT_DIR / f"{slug}.md").write_text(content, encoding="utf-8")

    print(f"Wrote {len(pages)} files to knowledge/site/ (removed {len(boilerplate)} boilerplate lines)")


if __name__ == "__main__":
    main()
