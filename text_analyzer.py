"""
text_analyzer.py

Processes raw text/ideas and converts them into structured content blocks.
"""

from typing import List, Dict, Any

ContentBlock = Dict[str, Any]


def analyze_text(text: str) -> List[ContentBlock]:
    """
    Convert raw text/idea input into content blocks.
    Tries to intelligently parse the text into headings and paragraphs.
    """
    blocks: List[ContentBlock] = []
    
    if not text or not text.strip():
        # Default content for empty input
        blocks.append({
            "type": "heading",
            "level": 1,
            "text": "Company Overview"
        })
        blocks.append({
            "type": "paragraph",
            "level": None,
            "text": "A company focused on delivering value and innovation to customers."
        })
        return blocks
    
    lines = text.strip().split('\n')
    current_heading = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Detect headings (lines that are short and end without punctuation, or start with #)
        if line.startswith('#'):
            # Markdown-style heading
            level = len(line) - len(line.lstrip('#'))
            heading_text = line.lstrip('#').strip()
            if heading_text:
                blocks.append({
                    "type": "heading",
                    "level": min(level, 6),
                    "text": heading_text
                })
        elif line.isupper() and len(line) < 100 and not line.endswith(('.', '!', '?')):
            # Likely a heading (all caps, short, no ending punctuation)
            blocks.append({
                "type": "heading",
                "level": 2,
                "text": line.title()
            })
        elif len(line) < 80 and not line.endswith(('.', '!', '?', ',')):
            # Short line without punctuation - might be a heading
            blocks.append({
                "type": "heading",
                "level": 2,
                "text": line
            })
        else:
            # Regular paragraph
            blocks.append({
                "type": "paragraph",
                "level": None,
                "text": line
            })
    
    # If no blocks were created, treat entire text as a paragraph
    if not blocks:
        blocks.append({
            "type": "heading",
            "level": 1,
            "text": "Company Description"
        })
        blocks.append({
            "type": "paragraph",
            "level": None,
            "text": text.strip()
        })
    
    return blocks


if __name__ == '__main__':
    # Test
    sample_text = """
    Tech Startup
    We build AI-powered solutions for enterprises
    Our platform helps companies automate workflows
    Focus on machine learning and cloud infrastructure
    """
    
    blocks = analyze_text(sample_text)
    for block in blocks:
        print(block)
