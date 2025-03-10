
"""
Asset Generator - Creates necessary assets for the AI CEO Mobile App
"""
import os
import shutil
import random
import math
from PIL import Image, ImageDraw

def ensure_dir(directory):
    """Ensure directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_tv_static(filename, width=500, height=500):
    """Generate a TV static image"""
    img = Image.new('RGB', (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw random noise
    for x in range(width):
        for y in range(height):
            # More white than black for TV static look
            if random.random() > 0.5:
                brightness = random.randint(100, 255)
                draw.point((x, y), fill=(brightness, brightness, brightness))
    
    img.save(filename)
    print(f"Generated {filename}")

def generate_simple_logo(filename, text="AI CEO", width=300, height=100):
    """Generate a simple logo with text"""
    img = Image.new('RGBA', (width, height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw background rectangle
    draw.rectangle([(0, 0), (width, height)], fill=(10, 30, 60, 200), outline=(0, 150, 255, 255))
    
    # We can't use fonts easily here, so just draw some lines to represent text
    line_length = len(text) * 15
    center_x = width // 2
    center_y = height // 2
    
    # Draw horizontal line for text
    draw.line([(center_x - line_length//2, center_y), 
               (center_x + line_length//2, center_y)], 
              fill=(0, 200, 255, 255), width=10)
    
    # Draw some decorative elements
    for i in range(5):
        x1 = random.randint(10, width-10)
        y1 = random.randint(10, height-10)
        size = random.randint(5, 15)
        draw.ellipse([(x1-size, y1-size), (x1+size, y1+size)], 
                    fill=(0, 255, 200, 150))
    
    img.save(filename)
    print(f"Generated {filename}")

def generate_circle_icon(filename, size=100, color=(255, 0, 100)):
    """Generate a simple circular icon"""
    img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw the circle
    draw.ellipse([(0, 0), (size, size)], fill=color)
    
    # Add some decorative elements
    for i in range(3):
        angle = i * 2 * math.pi / 3
        x = size//2 + int(size//3 * math.cos(angle))
        y = size//2 + int(size//3 * math.sin(angle))
        dot_size = size // 10
        draw.ellipse([(x-dot_size, y-dot_size), (x+dot_size, y+dot_size)], 
                    fill=(255, 255, 255, 200))
    
    img.save(filename)
    print(f"Generated {filename}")

def main():
    """Main function to generate all assets"""
    print("Generating assets for AI CEO Mobile App...")
    
    # Ensure assets directory exists
    assets_dir = "assets"
    ensure_dir(assets_dir)
    
    # Generate TV static image if it doesn't exist
    tv_static_path = os.path.join(assets_dir, "tv_static.png")
    if not os.path.exists(tv_static_path):
        generate_tv_static(tv_static_path)
    
    # Generate app logo if it doesn't exist
    logo_path = os.path.join(assets_dir, "app_logo.png")
    if not os.path.exists(logo_path):
        generate_simple_logo(logo_path)
    
    # Generate profile icon if it doesn't exist
    profile_icon_path = os.path.join(assets_dir, "profile_icon.png")
    if not os.path.exists(profile_icon_path):
        generate_circle_icon(profile_icon_path)
    
    # Copy existing assets if available
    source_files = [
        "tv_static.svg", 
        "tv_frame.svg", 
        "static_noise.wav",
        "adtv_logo.svg"
    ]
    
    for file in source_files:
        dest_path = os.path.join(assets_dir, file)
        if not os.path.exists(dest_path) and os.path.exists(file):
            shutil.copy(file, dest_path)
            print(f"Copied {file} to assets directory")
    
    print("Asset generation complete!")

if __name__ == "__main__":
    main()
