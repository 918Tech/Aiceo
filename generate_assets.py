
"""
AI CEO System - Asset Generator
Generates necessary assets for the mobile app
"""
import os
import sys
import random
import math
from PIL import Image, ImageDraw, ImageFont

def ensure_directories():
    """Ensure all necessary directories exist"""
    directories = ['assets', 'bin']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def generate_logo(output_path="assets/app_logo.png"):
    """Generate the AI CEO app logo"""
    width, height = 512, 512
    
    # Create base image with dark blue background
    img = Image.new('RGBA', (width, height), (10, 30, 60, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw outer ring
    draw.ellipse([(40, 40), (width-40, height-40)], outline=(0, 150, 255, 255), width=20)
    
    # Draw inner logo shape
    draw.rectangle([(width//4, height//4), (width*3//4, height*3//4)], fill=(0, 100, 200, 255))
    
    # Try to add text (if font available)
    try:
        # Try to use a system font
        font_path = None
        system_fonts = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',  # Linux
            '/System/Library/Fonts/Helvetica.ttc',  # macOS
            'C:\\Windows\\Fonts\\Arial.ttf'  # Windows
        ]
        
        for path in system_fonts:
            if os.path.exists(path):
                font_path = path
                break
        
        if font_path:
            font_large = ImageFont.truetype(font_path, 80)
            font_small = ImageFont.truetype(font_path, 40)
            
            # Draw text - can use .text() with align parameter on Pillow 8.0.0+
            draw.text((width//2, height//2-50), "AI CEO", fill=(255, 255, 255, 255), 
                      font=font_large, anchor="mm")
            draw.text((width//2, height//2+40), "SYSTEM", fill=(200, 200, 200, 255), 
                      font=font_small, anchor="mm")
        else:
            # If no font found, draw a simple placeholder
            draw.rectangle([(width//3, height//2-30), (width*2//3, height//2+30)], fill=(255, 255, 255, 255))
    except Exception as e:
        print(f"Warning: Could not add text to logo: {e}")
    
    # Save the image
    img.save(output_path)
    print(f"Generated logo: {output_path}")
    
    # Create smaller version for app icon
    icon_size = 192
    icon = img.resize((icon_size, icon_size), Image.LANCZOS)
    icon.save("assets/app_icon.png")
    print("Generated app icon: assets/app_icon.png")
    
    return True

def generate_tv_static(output_path="assets/tv_static.png"):
    """Generate a TV static image"""
    width, height = 512, 512
    
    # Create base image
    img = Image.new('RGB', (width, height), (0, 0, 0))
    pixels = img.load()
    
    # Draw random noise
    for y in range(height):
        for x in range(width):
            # Random grayscale value for static effect
            brightness = random.randint(0, 255)
            pixels[x, y] = (brightness, brightness, brightness)
    
    # Save the image
    img.save(output_path)
    print(f"Generated TV static: {output_path}")
    return True

def generate_tv_frame(output_path="assets/tv_frame.png"):
    """Generate a TV frame image"""
    width, height = 600, 500
    frame_width = 40
    
    # Create base image with transparency
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw outer frame
    draw.rectangle([(0, 0), (width, height)], fill=(30, 30, 30, 255))
    
    # Draw inner cutout (TV screen area)
    draw.rectangle([(frame_width, frame_width), 
                    (width-frame_width, height-frame_width)], 
                   fill=(0, 0, 0, 0))
    
    # Draw some details on the frame
    # Control panel at bottom
    control_panel_height = 60
    draw.rectangle([(width//3, height-frame_width-control_panel_height), 
                    (width*2//3, height-frame_width)], 
                   fill=(50, 50, 50, 255))
    
    # Control buttons
    button_size = 15
    button_y = height - frame_width - control_panel_height//2
    for i in range(3):
        button_x = width//3 + 30 + (i * 40)
        draw.ellipse([(button_x-button_size//2, button_y-button_size//2), 
                      (button_x+button_size//2, button_y+button_size//2)], 
                     fill=(80, 80, 80, 255))
    
    # Volume slider
    slider_width = 80
    slider_height = 10
    slider_x = width//3 + 160
    slider_y = button_y
    draw.rectangle([(slider_x, slider_y-slider_height//2), 
                    (slider_x+slider_width, slider_y+slider_height//2)], 
                   fill=(80, 80, 80, 255))
    
    # Slider knob
    knob_size = 20
    knob_x = slider_x + slider_width * 0.7
    draw.ellipse([(knob_x-knob_size//2, slider_y-knob_size//2), 
                  (knob_x+knob_size//2, slider_y+knob_size//2)], 
                 fill=(150, 150, 150, 255))
    
    # Add highlight to top edge of frame
    for i in range(frame_width//2):
        alpha = 100 - (i * 2)
        if alpha > 0:
            draw.line([(i, i), (width-i, i)], fill=(255, 255, 255, alpha), width=1)
    
    # Save the image
    img.save(output_path)
    print(f"Generated TV frame: {output_path}")
    return True

def generate_profile_icon(output_path="assets/profile_icon.png"):
    """Generate a simple profile icon"""
    size = 128
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw circle background
    draw.ellipse([(0, 0), (size, size)], fill=(100, 100, 200, 255))
    
    # Draw simplified person silhouette
    # Head
    head_size = size // 3
    head_top = size // 5
    draw.ellipse([(size//2-head_size//2, head_top), 
                  (size//2+head_size//2, head_top+head_size)], 
                 fill=(240, 240, 240, 255))
    
    # Body
    body_width = size // 2
    body_top = head_top + head_size - 5
    draw.ellipse([(size//2-body_width//2, body_top), 
                  (size//2+body_width//2, size-10)], 
                 fill=(240, 240, 240, 255))
    
    # Save the image
    img.save(output_path)
    print(f"Generated profile icon: {output_path}")
    return True

def generate_all_assets():
    """Generate all required assets"""
    ensure_directories()
    
    # Check if PIL is available
    try:
        from PIL import Image, ImageDraw, ImageFont
        print("Generating assets using PIL...")
        
        # Generate all assets
        generate_logo()
        generate_tv_static()
        generate_tv_frame()
        generate_profile_icon()
        
        print("All assets generated successfully!")
        return True
    except ImportError:
        print("PIL not available, skipping asset generation")
        copy_default_assets()
        return False

def copy_default_assets():
    """Copy any existing default assets if PIL not available"""
    assets_to_copy = {
        'tv_static.svg': 'assets/tv_static.svg',
        'tv_frame.svg': 'assets/tv_frame.svg',
        'adtv_logo.svg': 'assets/adtv_logo.svg',
        'static_noise.wav': 'assets/static_noise.wav'
    }
    
    copied = False
    for src, dest in assets_to_copy.items():
        if os.path.exists(src) and not os.path.exists(dest):
            import shutil
            try:
                shutil.copy(src, dest)
                print(f"Copied {src} to {dest}")
                copied = True
            except Exception as e:
                print(f"Error copying {src}: {e}")
    
    if not copied:
        print("No default assets found to copy")

if __name__ == "__main__":
    generate_all_assets()
