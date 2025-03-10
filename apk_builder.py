
"""
AI CEO APK Builder - Simplified build process for mobile APK
"""
import os
import subprocess
import sys

def generate_assets():
    """Generate necessary assets for the APK"""
    print("Generating assets for APK...")
    
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    try:
        # Try to use the dedicated asset generator if it exists
        if os.path.exists('generate_assets.py'):
            subprocess.run(['python', 'generate_assets.py'], check=True)
            return True
        else:
            # Otherwise, create minimal required assets
            try:
                from PIL import Image, ImageDraw
                
                # Generate a static TV image
                img = Image.new('RGB', (300, 300), color=(0, 0, 0))
                draw = ImageDraw.Draw(img)
                
                # Draw random noise for static effect
                for x in range(300):
                    for y in range(300):
                        if random.random() > 0.5:
                            brightness = random.randint(100, 255)
                            draw.point((x, y), fill=(brightness, brightness, brightness))
                
                img.save('assets/tv_static.png')
                print("Generated TV static image")
                
                # Generate a simple app icon
                icon = Image.new('RGB', (192, 192), color=(10, 30, 60))
                draw = ImageDraw.Draw(icon)
                draw.rectangle([(20, 20), (172, 172)], fill=(0, 150, 255))
                draw.ellipse([(50, 50), (142, 142)], fill=(255, 255, 255))
                draw.text((70, 80), "AI CEO", fill=(0, 0, 0))
                
                icon.save('assets/app_icon.png')
                print("Generated app icon")
                
                return True
            except ImportError:
                print("PIL not available, skipping asset generation")
                # Copy any existing SVG files
                for file in ['tv_static.svg', 'tv_frame.svg', 'adtv_logo.svg']:
                    if os.path.exists(file):
                        import shutil
                        shutil.copy(file, os.path.join('assets', file))
                return True
    except Exception as e:
        print(f"Error generating assets: {e}")
        return False

def build_apk():
    """Build the APK using buildozer"""
    print("Starting APK build process...")
    
    # Verify mobile_preview.py exists
    if not os.path.exists('mobile_preview.py'):
        print("Error: mobile_preview.py not found!")
        return False
    
    # Generate assets
    generate_assets()
    
    # Run buildozer
    try:
        subprocess.run(['buildozer', 'android', 'debug'], check=True)
        
        # Check if build was successful
        if os.path.exists('bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk'):
            print("APK build completed successfully!")
            print("The APK file is available at: bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk")
            return True
        else:
            print("APK file not found after build. Check buildozer logs for errors.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error building APK: {e}")
        # Try to show the error from buildozer log
        try:
            import glob
            log_files = glob.glob('.buildozer/logs/buildozer-*.log')
            if log_files:
                latest_log = max(log_files, key=os.path.getctime)
                print(f"Last 20 lines from {latest_log}:")
                with open(latest_log, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-20:]:
                        print(line.strip())
        except Exception:
            pass
        return False
    except FileNotFoundError:
        print("Error: buildozer not found! Installing buildozer...")
        try:
            subprocess.run(['pip', 'install', 'buildozer'], check=True)
            print("Buildozer installed, now building APK...")
            return build_apk()  # Recursive call now that buildozer is installed
        except subprocess.CalledProcessError as e:
            print(f"Error installing buildozer: {e}")
            return False

if __name__ == "__main__":
    build_apk()
