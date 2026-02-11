"""
scraper.py

Responsible for:
- Loading a local HTML file.
- Removing obvious noise (scripts, navbars, footers, cookie banners, etc.).
- Returning a simple list of content blocks: headings + associated text.
"""

from pathlib import Path
from typing import List, Dict, Any

from bs4 import BeautifulSoup, Tag


ContentBlock = Dict[str, Any]


def load_html(path: str) -> BeautifulSoup:
    """Read HTML from disk and return a BeautifulSoup object."""
    html_path = Path(path)
    if not html_path.is_file():
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    text = html_path.read_text(encoding="utf-8", errors="ignore")
    # lxml parser is usually faster and more forgiving than html.parser
    return BeautifulSoup(text, "lxml")


def _remove_obvious_noise(soup: BeautifulSoup) -> None:
    """
    Strip script/style tags and obvious layout noise.
    We do this in-place to keep the rest of the code straightforward.
    """
    # Kill script/style outright
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Common structural wrappers that are rarely core content
    for tag_name in ["nav", "footer", "form", "aside"]:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Heuristic removal based on id/class patterns
    noise_keywords = [
        "cookie",
        "banner",
        "consent",
        "gdpr",
        "newsletter",
        "signup",
        "subscribe",
        "modal",
        "popup",
        "promo",
        "advert",
        "ads",
        "legal",
        "terms",
        "privacy",
    ]

    for tag in soup.find_all(True):  # all tags
        id_str = (tag.get("id") or "").lower()
        class_str = " ".join(c.lower() for c in tag.get("class", []))
        combined = f"{id_str} {class_str}"

        if any(keyword in combined for keyword in noise_keywords):
            # If this wrapper is clearly decoration, drop it entirely
            tag.decompose()


def _pick_main_container(soup: BeautifulSoup) -> Tag:
    """
    Try to select the main content container.
    Prefer <main>, then a large <div>, otherwise fall back to <body>.
    """
    main = soup.find("main")
    if main:
        return main

    body = soup.body
    if not body:
        # Degenerate pages: just use the top-level soup
        return soup

    # Naive heuristic: the largest div by text length inside body
    candidate = body
    max_len = len(body.get_text(strip=True))

    for div in body.find_all("div"):
        text_len = len(div.get_text(strip=True))
        if text_len > max_len:
            max_len = text_len
            candidate = div

    return candidate


def _is_meaningful_text(text: str) -> bool:
    """Filter out very short or noisy text fragments."""
    stripped = text.strip()
    if not stripped:
        return False
    # Skip tiny fragments like "OK", "Learn more", etc.
    if len(stripped) < 25:
        return False
    # Skip clear boilerplate phrases
    lower = stripped.lower()
    boilerplate_phrases = [
        "all rights reserved",
        "terms of use",
        "privacy policy",
        "cookie policy",
    ]
    if any(phrase in lower for phrase in boilerplate_phrases):
        return False
    return True


def extract_content_blocks(soup: BeautifulSoup) -> List[ContentBlock]:
    """
    Return a flat list of content blocks with a very simple structure:
    - type: "heading" or "paragraph"
    - level: for headings, 1–6 (for non-headings, None)
    - text: clean text

    We walk the main container in document order so the analyzer
    can infer structure without us doing heavy DOM reasoning.
    """
    _remove_obvious_noise(soup)
    root = _pick_main_container(soup)

    blocks: List[ContentBlock] = []

    for element in root.descendants:
        if not isinstance(element, Tag):
            continue

        # Headings
        if element.name in {f"h{i}" for i in range(1, 7)}:
            text = element.get_text(separator=" ", strip=True)
            if not _is_meaningful_text(text):
                continue
            level = int(element.name[1])
            blocks.append(
                {
                    "type": "heading",
                    "level": level,
                    "text": text,
                }
            )
            continue

        # Paragraph-like nodes
        if element.name in {"p", "li"}:
            text = element.get_text(separator=" ", strip=True)
            if not _is_meaningful_text(text):
                continue
            blocks.append(
                {
                    "type": "paragraph",
                    "level": None,
                    "text": text,
                }
            )

    return blocks


def scrape_html(path: str) -> List[ContentBlock]:
    """Public entry point: from HTML path to cleaned content blocks."""
    soup = load_html(path)
    return extract_content_blocks(soup)


if __name__ == "__main__":
    # Small manual test; kept simple on purpose.
    example_path = "./data/company.html"
    blocks = scrape_html(example_path)
    print(f"Extracted {len(blocks)} content blocks from {example_path}.")
    for b in blocks[:10]:
        print(b)

