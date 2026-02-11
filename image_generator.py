"""
image_generator.py

Generates background images for brochures using PIL/Pillow.
Creates gradient backgrounds with subtle patterns.
"""

import os
from pathlib import Path
from typing import Dict, Any
from PIL import Image, ImageDraw, ImageFont
import random

BusinessProfile = Dict[str, Any]


def _generate_gradient_background(width: int, height: int, colors: tuple) -> Image.Image:
    """Create a gradient background image."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Simple linear gradient
    for y in range(height):
        ratio = y / height
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img


def _add_pattern_overlay(img: Image.Image, pattern_type: str = 'dots') -> Image.Image:
    """Add very subtle, light pattern overlay to the image."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    if pattern_type == 'dots':
        # Very subtle white dot pattern for light backgrounds
        for x in range(0, img.width, 50):
            for y in range(0, img.height, 50):
                draw.ellipse([x-1.5, y-1.5, x+1.5, y+1.5], fill=(255, 255, 255, 15))
    elif pattern_type == 'lines':
        # Very subtle white line pattern
        for x in range(0, img.width, 80):
            draw.line([(x, 0), (x, img.height)], fill=(255, 255, 255, 12), width=1)
    elif pattern_type == 'sparkle':
        # Light sparkle effect
        for _ in range(30):
            x = random.randint(0, img.width)
            y = random.randint(0, img.height)
            size = random.randint(2, 4)
            draw.ellipse([x-size, y-size, x+size, y+size], fill=(255, 255, 255, 20))
    
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')


def _get_color_scheme(audience: str) -> tuple:
    """Return light, bright color scheme based on audience type."""
    schemes = {
        'customers': ((250, 252, 255), (200, 230, 255)),  # Very light blue to soft blue
        'investors': ((255, 252, 245), (255, 240, 220)),  # Very light cream to soft peach
        'partners': ((245, 255, 245), (220, 255, 220)),   # Very light green to soft green
    }
    return schemes.get(audience, ((250, 250, 250), (240, 240, 240)))  # Very light gray


def generate_brochure_background(profile: BusinessProfile, audience: str) -> str:
    """
    Generate a background image for a brochure.
    Returns the path to the saved image file.
    """
    # Standard brochure size (A4 ratio, 1200x1697 for web)
    width, height = 1200, 1697
    
    # Get color scheme based on audience
    colors = _get_color_scheme(audience)
    
    # Generate gradient background with lighter colors
    img = _generate_gradient_background(width, height, colors)
    
    # Add very subtle light pattern (sparkle for extra brightness)
    img = _add_pattern_overlay(img, pattern_type='sparkle')
    
    # Brighten the image slightly for extra lightness
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)  # 10% brighter
    
    # Save the image
    output_dir = Path('static/images')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f'brochure_bg_{audience}.jpg'
    filepath = output_dir / filename
    img.save(filepath, 'JPEG', quality=85)
    
    return str(filepath)


if __name__ == '__main__':
    # Test generation
    test_profile = {
        "company_positioning": "Test company",
        "core_offerings": ["Service 1", "Service 2"],
        "target_audience": ["Audience 1"],
        "unique_value_propositions": ["Value 1"],
        "brand_tone_signals": ["Professional"],
    }
    
    for audience in ['customers', 'investors', 'partners']:
        path = generate_brochure_background(test_profile, audience)
        print(f"Generated: {path}")
