#!/usr/bin/env python3
"""
Thumbnail Generator for YouTube Automation
Generates eye-catching US-style thumbnails with text overlay
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO
import textwrap
import sys
import json
import os

def generate_thumbnail(title, output_path='/tmp/thumbnail.jpg'):
    """
    Generate a YouTube thumbnail with the given title
    
    Args:
        title: Video title text (max 60 chars)
        output_path: Where to save the thumbnail
    
    Returns:
        dict with thumbnail_path
    """
    # Truncate title to 60 chars
    title = title[:60]
    
    # Download background image
    background_url = "https://source.unsplash.com/1280x720/?technology,modern"
    try:
        response = requests.get(background_url, timeout=10)
        img = Image.open(BytesIO(response.content))
    except Exception as e:
        # Fallback: create a solid color background
        print(f"Warning: Could not download background: {e}", file=sys.stderr)
        img = Image.new('RGB', (1280, 720), color=(30, 30, 30))
    
    # Resize to YouTube thumbnail size
    img = img.resize((1280, 720), Image.Resampling.LANCZOS)
    
    # Apply slight blur for background
    blurred = img.filter(ImageFilter.GaussianBlur(3))
    
    # Create dark gradient overlay for text readability
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    for i in range(720):
        alpha = int(100 + (i / 720) * 80)  # Gradient from semi-transparent to more opaque
        draw_overlay.rectangle([(0, i), (1280, i+1)], fill=(0, 0, 0, alpha))
    
    img = Image.alpha_composite(blurred.convert('RGBA'), overlay)
    
    # Add text
    draw = ImageDraw.Draw(img)
    
    # Try to load a bold font (common on most systems)
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except Exception:
        try:
            # Alternative font path for different systems
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 90)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        except Exception:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    
    # Word wrap title for better display
    wrapped_title = textwrap.fill(title, width=20)
    
    # Add title with shadow effect (US style - bold and eye-catching)
    for offset in [(2,2), (-2,2), (2,-2), (-2,-2)]:
        draw.multiline_text(
            (640 + offset[0], 300 + offset[1]), 
            wrapped_title, 
            font=title_font, 
            fill='black', 
            anchor='mm',
            align='center'
        )
    
    # Main title in white
    draw.multiline_text(
        (640, 300), 
        wrapped_title, 
        font=title_font, 
        fill='white', 
        anchor='mm',
        align='center'
    )
    
    # Add engaging subtitle
    subtitle = "WATCH NOW!"
    draw.text(
        (640, 500), 
        subtitle, 
        font=subtitle_font, 
        fill='#FF0000',  # YouTube red
        anchor='mm'
    )
    
    # Add accent elements (modern US YouTube style)
    draw.rectangle([(40, 600), (240, 620)], fill='#FF0000')  # Red accent bar
    
    # Save thumbnail
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.convert('RGB').save(output_path, 'JPEG', quality=95, optimize=True)
    
    return {'thumbnail_path': output_path}

if __name__ == '__main__':
    # Read title from command line argument or stdin
    if len(sys.argv) > 1:
        title = sys.argv[1]
    else:
        # Read from stdin (for n8n integration)
        try:
            input_data = json.loads(sys.stdin.read())
            title = input_data.get('topic', input_data.get('title', 'Default Title'))
        except:
            title = "Default Title"
    
    # Generate thumbnail
    result = generate_thumbnail(title)
    
    # Output result as JSON for n8n
    print(json.dumps(result))
