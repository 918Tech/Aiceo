
"""
AI CEO APK Builder - Simplified build process for mobile APK
"""
import os
import subprocess
import sys

def build_apk():
    """Build the APK using buildozer"""
    print("Starting APK build process...")
    
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # Verify mobile_preview.py exists
    if not os.path.exists('mobile_preview.py'):
        print("Error: mobile_preview.py not found!")
        return False
    
    # Run buildozer
    try:
        subprocess.run(['buildozer', 'android', 'debug'], check=True)
        print("APK build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building APK: {e}")
        return False
    except FileNotFoundError:
        print("Error: buildozer not found! Installing buildozer...")
        try:
            subprocess.run(['pip', 'install', 'buildozer'], check=True)
            print("Buildozer installed, now building APK...")
            subprocess.run(['buildozer', 'android', 'debug'], check=True)
            print("APK build completed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing buildozer or building APK: {e}")
            return False

if __name__ == "__main__":
    build_apk()
