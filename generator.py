"""
generator.py

Takes a structured business profile and produces simple, markdown brochures
for different audiences. This stubbed version does not call any external LLM;
it just formats the profile into human-readable copy.
"""

from typing import Dict, Any

BusinessProfile = Dict[str, Any]
BrochureSet = Dict[str, str]


def _format_brochure_common_intro(profile: BusinessProfile) -> str:
    """Shared intro text for all audiences so things stay consistent."""
    positioning = profile.get("company_positioning", "").strip()
    offerings = profile.get("core_offerings") or []
    audience = profile.get("target_audience") or []

    lines = []
    if positioning:
        lines.append(positioning)
    if offerings:
        lines.append("")
        lines.append("**What we offer**")
        for item in offerings:
            lines.append(f"- {item}")
    if audience:
        lines.append("")
        lines.append("**Who we work with**")
        for item in audience:
            lines.append(f"- {item}")
    return "\n".join(lines).strip()


def _brochure_for_customers(profile: BusinessProfile) -> str:
    uvps = profile.get("unique_value_propositions") or []
    intro = _format_brochure_common_intro(profile)

    lines = ["## Why teams choose us", ""]
    for v in uvps:
        lines.append(f"- {v}")

    body = "\n".join(lines).strip()
    return f"{intro}\n\n{body}".strip()


def _brochure_for_investors(profile: BusinessProfile) -> str:
    uvps = profile.get("unique_value_propositions") or []
    audience = profile.get("target_audience") or []

    lines = ["## Market and focus", ""]
    if audience:
        lines.append("We focus on:")
        for item in audience:
            lines.append(f"- {item}")
        lines.append("")

    if uvps:
        lines.append("## Why we win")
        lines.append("")
        for v in uvps:
            lines.append(f"- {v}")

    return "\n".join(lines).strip()


def _brochure_for_partners(profile: BusinessProfile) -> str:
    tone = profile.get("brand_tone_signals") or []
    offerings = profile.get("core_offerings") or []

    lines = ["## How we like to partner", ""]
    if tone:
        lines.append("We aim to be:")
        for t in tone:
            lines.append(f"- {t}")
        lines.append("")

    if offerings:
        lines.append("We look for partners who complement these capabilities:")
        for item in offerings:
            lines.append(f"- {item}")

    return "\n".join(lines).strip()


def generate_brochures(profile: BusinessProfile) -> BrochureSet:
    """
    Main entry: from business profile dict to three brochures.
    This is deterministic and offline, which is handy for demos/tests.
    """
    return {
        "customers": _brochure_for_customers(profile),
        "investors": _brochure_for_investors(profile),
        "partners": _brochure_for_partners(profile),
    }


if __name__ == "__main__":
    # Small self-test with a fake profile.
    sample_profile: BusinessProfile = {
        "company_positioning": "Platform for AI-native SaaS companies.",
        "core_offerings": ["Managed AI infrastructure", "Model deployment tooling"],
        "target_audience": ["Technical founders", "Growth-stage SaaS teams"],
        "unique_value_propositions": [
            "Minutes from prototype to production",
            "Usage-based pricing aligned with growth",
        ],
        "brand_tone_signals": ["Pragmatic", "Supportive", "Forward-looking"],
    }
    print("Generating demo brochures (requires OPENAI_API_KEY)...")
    result = generate_brochures(sample_profile)
    for audience, text in result.items():
        print(f"\n=== {audience.upper()} ===\n{text}\n")

