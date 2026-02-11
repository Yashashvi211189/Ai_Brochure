"""
analyzer.py

Takes the content blocks from `scraper.py` and turns them into a compact,
structured view of the business using a token-efficient LLM call.
"""

import json
from textwrap import shorten
from typing import List, Dict, Any

# Note: in the original version this module called the OpenAI API.
# For local/offline use and interview demos, we now run fully locally
# and infer a simple profile directly from the scraped content.


ContentBlock = Dict[str, Any]
BusinessProfile = Dict[str, Any]


def _build_compact_context(blocks: List[ContentBlock], max_chars: int = 3500) -> str:
    """
    Turn the blocks into a compact, line-based context string.
    We keep it short to avoid wasting tokens.
    """
    lines = []
    for block in blocks:
        if block["type"] == "heading":
            level = block["level"] or 1
            prefix = "#" * min(level, 6)
            lines.append(f"{prefix} {block['text']}")
        else:
            lines.append(block["text"])

    full = "\n".join(lines)
    # Hard cap length; we want to be deterministic about token usage.
    # textwrap.shorten keeps sentence-ish boundaries when possible.
    return shorten(full, width=max_chars, placeholder="\n...[truncated]...")


def _offline_profile_from_blocks(blocks: List[ContentBlock]) -> BusinessProfile:
    """
    Very small heuristic that mimics what the LLM would return.
    This keeps the rest of the pipeline unchanged, but removes
    the dependency on any external API.
    """
    compact = _build_compact_context(blocks, max_chars=2000).lower()

    # Crude keyword-based guesses; good enough for a demo and easy to explain.
    offerings: List[str] = []
    if "hosting" in compact or "infrastructure" in compact:
        offerings.append("Managed infrastructure and hosting")
    if "ml ops" in compact or "ml ops" in compact.replace("mlops", "ml ops"):
        offerings.append("ML Ops tooling")
    if "deployment" in compact or "deploy" in compact:
        offerings.append("Model deployment and monitoring")
    if not offerings:
        offerings.append("Software products and related services")

    audience: List[str] = []
    if "enterprise" in compact or "enterprises" in compact:
        audience.append("Enterprise technology teams")
    if "saas" in compact:
        audience.append("B2B SaaS companies")
    if "startup" in compact or "founder" in compact:
        audience.append("High-growth startups")
    if not audience:
        audience.append("Modern businesses looking to use technology more effectively")

    value_props: List[str] = []
    if "faster" in compact or "weeks instead of months" in compact:
        value_props.append("Faster time-to-value compared to in-house builds")
    if "secure" in compact or "security" in compact:
        value_props.append("Security and compliance handled by specialists")
    if "scal" in compact:
        value_props.append("Scales with demand without manual capacity planning")
    if not value_props:
        value_props.append("Focused on reliable delivery and practical outcomes")

    tone_signals: List[str] = []
    if "pragmatic" in compact or "practical" in compact:
        tone_signals.append("Pragmatic and down-to-earth")
    if "partner" in compact or "with you" in compact:
        tone_signals.append("Partnership-oriented and supportive")
    if not tone_signals:
        tone_signals.extend(["Professional", "Confident"])

    positioning = (
        "The company provides pragmatic technology solutions for teams that want the "
        "benefits of modern tooling without running complex infrastructure themselves."
    )

    return {
        "company_positioning": positioning,
        "core_offerings": offerings,
        "target_audience": audience,
        "unique_value_propositions": value_props,
        "brand_tone_signals": tone_signals,
    }


def analyze_business(blocks: List[ContentBlock]) -> BusinessProfile:
    """
    Main entry point: from content blocks to a structured business profile dict.
    """
    if not blocks:
        raise ValueError("No content blocks provided for analysis.")

    # In the stubbed version we skip the remote LLM call and rely on a small,
    # deterministic heuristic that still produces a structured profile.
    return _offline_profile_from_blocks(blocks)


if __name__ == "__main__":
    # Tiny sanity check with fake blocks.
    demo_blocks = [
        {"type": "heading", "level": 1, "text": "Acme AI Cloud"},
        {
            "type": "paragraph",
            "level": None,
            "text": "Acme provides scalable AI infrastructure for enterprises.",
        },
    ]
    print("Running demo analysis (requires OPENAI_API_KEY)...")
    result = analyze_business(demo_blocks)
    print(json.dumps(result, indent=2))

