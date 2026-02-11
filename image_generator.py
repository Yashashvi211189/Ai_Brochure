"""
image_generator.py

Generates creative, visually-rich background images for brochures using PIL/Pillow.
Creates Pinterest/Canva-style backgrounds with gradients, shapes, and patterns.
"""

import os
from pathlib import Path
from typing import Dict, Any
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFilter, ImageEnhance
import random
import math

BusinessProfile = Dict[str, Any]


def _generate_creative_gradient(width: int, height: int, colors: tuple, style: str = 'diagonal') -> Image.Image:
    """Create creative gradient backgrounds with different styles."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    if style == 'diagonal':
        # Diagonal gradient
        for y in range(height):
            for x in range(width):
                ratio = (x + y) / (width + height)
                r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
                g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
                b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
                draw.point((x, y), fill=(r, g, b))
    elif style == 'radial':
        # Radial gradient from center
        center_x, center_y = width // 2, height // 2
        max_dist = math.sqrt(center_x**2 + center_y**2)
        for y in range(height):
            for x in range(width):
                dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                ratio = min(dist / max_dist, 1.0)
                r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
                g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
                b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
                draw.point((x, y), fill=(r, g, b))
    else:
        # Linear gradient
        for y in range(height):
            ratio = y / height
            r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
            g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
            b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img


def _add_creative_shapes(img: Image.Image, audience: str) -> Image.Image:
    """Add creative shapes and patterns like Canva/Pinterest style."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    width, height = img.size
    
    # Add geometric shapes
    if audience == 'customers':
        # Circles and curves for customers
        for _ in range(8):
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(50, 150)
            alpha = random.randint(5, 15)
            draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                        fill=(255, 255, 255, alpha), outline=None)
    elif audience == 'investors':
        # Rectangles and lines for investors
        for _ in range(6):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = x1 + random.randint(100, 300)
            y2 = y1 + random.randint(100, 300)
            alpha = random.randint(8, 18)
            draw.rectangle([x1, y1, x2, y2], 
                           fill=(255, 255, 255, alpha), outline=None)
    else:  # partners
        # Triangles and polygons for partners
        for _ in range(5):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(80, 200)
            points = [
                (x, y - size),
                (x - size, y + size),
                (x + size, y + size)
            ]
            alpha = random.randint(10, 20)
            draw.polygon(points, fill=(255, 255, 255, alpha), outline=None)
    
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')


def _add_pattern_overlay(img: Image.Image, pattern_type: str = 'dots') -> Image.Image:
    """Add creative pattern overlays."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    if pattern_type == 'dots':
        # Creative dot pattern
        for x in range(0, img.width, 60):
            for y in range(0, img.height, 60):
                size = random.randint(2, 5)
                alpha = random.randint(10, 25)
                draw.ellipse([x-size, y-size, x+size, y+size], fill=(255, 255, 255, alpha))
    elif pattern_type == 'waves':
        # Wave pattern
        for y in range(0, img.height, 40):
            for x in range(0, img.width, 1):
                wave_y = y + int(10 * math.sin(x / 20))
                if 0 <= wave_y < img.height:
                    draw.point((x, wave_y), fill=(255, 255, 255, 15))
    elif pattern_type == 'grid':
        # Grid pattern
        for x in range(0, img.width, 80):
            draw.line([(x, 0), (x, img.height)], fill=(255, 255, 255, 12), width=1)
        for y in range(0, img.height, 80):
            draw.line([(0, y), (img.width, y)], fill=(255, 255, 255, 12), width=1)
    
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')


def _get_creative_color_scheme(audience: str) -> tuple:
    """Return creative, vibrant color schemes inspired by Pinterest/Canva."""
    schemes = {
        'customers': (
            (255, 245, 238),  # Soft peach
            (255, 223, 186),  # Warm coral
        ),
        'investors': (
            (240, 248, 255),  # Light blue
            (176, 224, 230),  # Powder blue
        ),
        'partners': (
            (245, 255, 250),  # Mint cream
            (152, 251, 152),  # Pale green
        ),
    }
    return schemes.get(audience, ((250, 250, 250), (240, 240, 240)))


def generate_brochure_background(profile: BusinessProfile, audience: str) -> str:
    """
    Generate a creative, visually-rich background image for a brochure.
    Returns the path to the saved image file.
    """
    # Standard brochure size (A4 ratio, 1200x1697 for web)
    width, height = 1200, 1697
    
    # Get creative color scheme
    colors = _get_creative_color_scheme(audience)
    
    # Generate creative gradient (diagonal for visual interest)
    img = _generate_creative_gradient(width, height, colors, style='diagonal')
    
    # Add creative shapes
    img = _add_creative_shapes(img, audience)
    
    # Add pattern overlay
    pattern_types = ['dots', 'waves', 'grid']
    pattern = random.choice(pattern_types)
    img = _add_pattern_overlay(img, pattern_type=pattern)
    
    # Apply blur for dreamy effect
    img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # Enhance brightness and saturation for vibrancy
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.15)  # 15% brighter
    
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.1)  # 10% more saturated
    
    # Save the image
    output_dir = Path('static/images')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f'brochure_bg_{audience}.jpg'
    filepath = output_dir / filename
    img.save(filepath, 'JPEG', quality=90)
    
    return str(filepath)


if __name__ == '__main__':
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
