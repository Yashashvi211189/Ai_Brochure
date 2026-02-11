"""
generator.py

Takes a structured business profile and produces creative, visually-rich brochures
for different audiences with detailed content and engaging copy.
"""

from typing import Dict, Any

BusinessProfile = Dict[str, Any]
BrochureSet = Dict[str, str]


def _brochure_for_customers(profile: BusinessProfile) -> str:
    """Create a creative, engaging brochure for customers."""
    positioning = profile.get("company_positioning", "Innovative solutions for modern businesses").strip()
    offerings = profile.get("core_offerings") or ["Quality products and services"]
    audience = profile.get("target_audience") or ["Forward-thinking companies"]
    uvps = profile.get("unique_value_propositions") or ["Excellence in delivery"]
    tone = profile.get("brand_tone_signals") or ["Professional"]
    
    lines = []
    
    # Hero section
    lines.append("## 🚀 Transform Your Business Today")
    lines.append("")
    lines.append(f"**{positioning}**")
    lines.append("")
    
    # What we offer - creative section
    lines.append("### ✨ What Sets Us Apart")
    lines.append("")
    for i, offering in enumerate(offerings[:4], 1):
        lines.append(f"**{i}. {offering}**")
        lines.append("")
    
    # Who we work with
    if audience:
        lines.append("### 👥 Perfect For")
        lines.append("")
        for item in audience[:3]:
            lines.append(f"✓ {item}")
        lines.append("")
    
    # Value propositions - creative format
    if uvps:
        lines.append("### 💎 Why Choose Us")
        lines.append("")
        for v in uvps[:4]:
            lines.append(f"**→ {v}**")
        lines.append("")
    
    # Call to action
    lines.append("### 🎯 Ready to Get Started?")
    lines.append("")
    lines.append("Join hundreds of satisfied customers who trust us to deliver exceptional results.")
    
    return "\n".join(lines).strip()


def _brochure_for_investors(profile: BusinessProfile) -> str:
    """Create a compelling investment-focused brochure."""
    positioning = profile.get("company_positioning", "A high-growth technology company").strip()
    offerings = profile.get("core_offerings") or ["Scalable solutions"]
    audience = profile.get("target_audience") or ["Enterprise clients"]
    uvps = profile.get("unique_value_propositions") or ["Strong market position"]
    
    lines = []
    
    # Investment pitch
    lines.append("## 💼 Investment Opportunity")
    lines.append("")
    lines.append(f"**{positioning}**")
    lines.append("")
    
    # Market opportunity
    lines.append("### 📈 Market Position")
    lines.append("")
    if audience:
        lines.append("**Target Market:**")
        for item in audience[:3]:
            lines.append(f"• {item}")
        lines.append("")
    
    # Competitive advantages
    if uvps:
        lines.append("### 🏆 Competitive Advantages")
        lines.append("")
        for v in uvps[:5]:
            lines.append(f"**✓ {v}**")
        lines.append("")
    
    # Product portfolio
    if offerings:
        lines.append("### 🎯 Product Portfolio")
        lines.append("")
        for offering in offerings[:4]:
            lines.append(f"• **{offering}**")
        lines.append("")
    
    # Growth potential
    lines.append("### 📊 Growth Potential")
    lines.append("")
    lines.append("• Scalable business model")
    lines.append("• Strong customer retention")
    lines.append("• Expanding market opportunity")
    lines.append("• Proven track record")
    
    return "\n".join(lines).strip()


def _brochure_for_partners(profile: BusinessProfile) -> str:
    """Create a partnership-focused brochure."""
    positioning = profile.get("company_positioning", "Building strategic partnerships").strip()
    offerings = profile.get("core_offerings") or ["Quality solutions"]
    tone = profile.get("brand_tone_signals") or ["Collaborative", "Trustworthy"]
    uvps = profile.get("unique_value_propositions") or ["Mutual success"]
    
    lines = []
    
    # Partnership vision
    lines.append("## 🤝 Let's Build Something Great Together")
    lines.append("")
    lines.append(f"**{positioning}**")
    lines.append("")
    
    # Our values
    if tone:
        lines.append("### 💫 Our Partnership Values")
        lines.append("")
        for t in tone[:4]:
            lines.append(f"**✨ {t}**")
        lines.append("")
    
    # What we bring
    if offerings:
        lines.append("### 🎁 What We Bring to the Table")
        lines.append("")
        for offering in offerings[:4]:
            lines.append(f"• **{offering}**")
        lines.append("")
    
    # Partnership benefits
    if uvps:
        lines.append("### 🌟 Partnership Benefits")
        lines.append("")
        for v in uvps[:4]:
            lines.append(f"**→ {v}**")
        lines.append("")
    
    # Call to action
    lines.append("### 🚀 Ready to Partner?")
    lines.append("")
    lines.append("Let's explore how we can create mutual value and drive success together.")
    
    return "\n".join(lines).strip()


def generate_brochures(profile: BusinessProfile) -> BrochureSet:
    """
    Main entry: from business profile dict to three creative brochures.
    """
    return {
        "customers": _brochure_for_customers(profile),
        "investors": _brochure_for_investors(profile),
        "partners": _brochure_for_partners(profile),
    }


if __name__ == "__main__":
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
    print("Generating creative brochures...")
    result = generate_brochures(sample_profile)
    for audience, text in result.items():
        print(f"\n=== {audience.upper()} ===\n{text}\n")
