"""
main.py

CLI entry point wiring together:
- scraper.scrape_html
- analyzer.analyze_business
- generator.generate_brochures

Intended usage:
    python main.py --html ./data/company.html --output ./output
"""

import argparse
from pathlib import Path

from scraper import scrape_html
from analyzer import analyze_business
from generator import generate_brochures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Local AI-powered website brochure generator."
    )
    parser.add_argument(
        "--html",
        type=str,
        default="./data/company.html",
        help="Path to the local HTML file to analyze.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./output",
        help="Directory where brochure files will be written.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    html_path = Path(args.html)
    output_dir = Path(args.output)

    # Ensure output directory exists so writes are straightforward.
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1) Scrape and clean the HTML.
    content_blocks = scrape_html(str(html_path))

    # 2) Analyze the business profile using the LLM.
    profile = analyze_business(content_blocks)

    # 3) Generate brochures for different audiences.
    brochures = generate_brochures(profile)

    # 4) Persist brochures as separate markdown files for easy sharing.
    outputs = {
        "customers": output_dir / "brochure_customers.md",
        "investors": output_dir / "brochure_investors.md",
        "partners": output_dir / "brochure_partners.md",
    }

    for audience, path in outputs.items():
        text = brochures.get(audience, "").strip()
        if not text:
            # Avoid writing empty files; this also signals issues when testing.
            continue

        header = f"# {audience.capitalize()} Brochure\n\n"
        path.write_text(header + text + "\n", encoding="utf-8")

    print(f"Brochures written to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()

