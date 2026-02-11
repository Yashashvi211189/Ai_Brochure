"""
image_analyzer.py

Extracts business information from uploaded images.
Uses basic image analysis and heuristics to infer company details.
"""

from PIL import Image
from typing import List, Dict, Any
import os

ContentBlock = Dict[str, Any]


def _extract_text_from_image_metadata(image_path: str) -> List[str]:
    """Extract any text metadata from image."""
    # In a real implementation, you'd use OCR here (like pytesseract)
    # For the stubbed version, we'll use filename and basic heuristics
    filename = os.path.basename(image_path).lower()
    
    # Extract potential keywords from filename
    keywords = []
    common_terms = [
        'company', 'business', 'startup', 'enterprise', 'tech', 'ai', 'cloud',
        'software', 'service', 'solutions', 'platform', 'app', 'digital'
    ]
    
    for term in common_terms:
        if term in filename:
            keywords.append(term)
    
    return keywords


def _analyze_image_content(image_path: str) -> Dict[str, Any]:
    """Analyze image to extract visual cues."""
    try:
        img = Image.open(image_path)
        width, height = img.size
        
        # Basic color analysis
        colors = img.getcolors(maxcolors=256*256*256)
        if colors:
            # Get dominant colors
            dominant_colors = sorted(colors, key=lambda x: x[0], reverse=True)[:5]
            color_info = {
                'dominant_colors': len(dominant_colors),
                'is_bright': sum(c[1][0] + c[1][1] + c[1][2] for c in dominant_colors[:3]) / 3 > 400,
                'is_dark': sum(c[1][0] + c[1][1] + c[1][2] for c in dominant_colors[:3]) / 3 < 200,
            }
        else:
            color_info = {'is_bright': True, 'is_dark': False}
        
        return {
            'dimensions': (width, height),
            'aspect_ratio': width / height if height > 0 else 1,
            'is_landscape': width > height,
            'is_portrait': height > width,
            **color_info
        }
    except Exception:
        return {}


def analyze_image(image_path: str) -> List[ContentBlock]:
    """
    Convert an image into content blocks that can be processed by the analyzer.
    This is a simplified version - in production you'd use OCR or vision models.
    """
    blocks: List[ContentBlock] = []
    
    # Extract from filename
    filename = os.path.basename(image_path)
    name_without_ext = os.path.splitext(filename)[0]
    
    # Create a heading from filename
    if name_without_ext:
        blocks.append({
            "type": "heading",
            "level": 1,
            "text": name_without_ext.replace('_', ' ').replace('-', ' ').title()
        })
    
    # Analyze image properties
    img_info = _analyze_image_content(image_path)
    
    # Create content based on image characteristics
    if img_info.get('is_bright'):
        blocks.append({
            "type": "paragraph",
            "level": None,
            "text": "The company presents a modern, bright brand identity suggesting innovation and clarity."
        })
    
    if img_info.get('is_landscape'):
        blocks.append({
            "type": "paragraph",
            "level": None,
            "text": "The visual style emphasizes breadth and comprehensive solutions."
        })
    
    # Extract keywords from filename
    keywords = _extract_text_from_image_metadata(image_path)
    if keywords:
        blocks.append({
            "type": "paragraph",
            "level": None,
            "text": f"The company operates in the {', '.join(keywords)} space, focusing on delivering value to clients."
        })
    
    # Default content if nothing extracted
    if not blocks:
        blocks.append({
            "type": "heading",
            "level": 1,
            "text": "Company Overview"
        })
        blocks.append({
            "type": "paragraph",
            "level": None,
            "text": "A forward-thinking company dedicated to delivering exceptional products and services to its customers."
        })
    
    return blocks


if __name__ == '__main__':
    # Test with a sample image path
    test_path = "data/sample.jpg"
    if os.path.exists(test_path):
        blocks = analyze_image(test_path)
        for block in blocks:
            print(block)
