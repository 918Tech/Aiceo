
"""
AI CEO APK Builder - Production-ready APK build process
Version 1.0.0
"""
import os
import subprocess
import sys
import json
import time
import random

# Configuration Constants
APK_VERSION = "1.0.0"
DEBUG_MODE = False  # Set to False for production build

def log(message, error=False):
    """Log a message with timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    if error:
        print(f"[{timestamp}] ERROR: {message}", file=sys.stderr)
    else:
        print(f"[{timestamp}] {message}")

def run_command(command, capture_output=False, check=True):
    """Run a shell command with better error handling"""
    try:
        log(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, capture_output=capture_output, check=check, text=True)
        return result
    except subprocess.CalledProcessError as e:
        log(f"Command failed with exit code {e.returncode}", error=True)
        if capture_output and e.stderr:
            log(f"Error output: {e.stderr}", error=True)
        if check:
            raise
        return e

def check_dependencies():
    """Check if all required dependencies are installed"""
    log("Checking dependencies...")
    
    required_packages = {
        "buildozer": "buildozer",
        "pillow": "PIL",
        "cython": "Cython",
        "flask": "flask",
        "requests": "requests"
    }
    
    missing_packages = []
    
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        log(f"Missing dependencies: {', '.join(missing_packages)}")
        log("Installing missing dependencies...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                          check=True, capture_output=True)
            
            for package in missing_packages:
                log(f"Installing {package}...")
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              check=True, capture_output=True)
                
            log("All dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            log(f"Failed to install dependencies: {e}", error=True)
            return False
    else:
        log("All dependencies are satisfied")
        return True

def update_config_version():
    """Update the app configuration with the current version"""
    config_file = "ai_ceo_config.json"
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            config['version'] = APK_VERSION
            config['production_build'] = True
            config['debug_mode'] = DEBUG_MODE
            config['build_timestamp'] = int(time.time())
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
                
            log(f"Updated config version to {APK_VERSION}")
            return True
        except Exception as e:
            log(f"Error updating config: {e}", error=True)
            return False
    else:
        log("Config file not found, creating a new one")
        try:
            config = {
                'version': APK_VERSION,
                'production_build': True,
                'debug_mode': DEBUG_MODE,
                'build_timestamp': int(time.time()),
                'theme': 'default',
                'token_balance': {'BBGT': 500, '918T': 20},
                'active_subscriptions': {},
                'trial_expiry': int(time.time()) + (3 * 60 * 60)
            }
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
                
            log(f"Created new config with version {APK_VERSION}")
            return True
        except Exception as e:
            log(f"Error creating config: {e}", error=True)
            return False

def generate_assets():
    """Generate necessary assets for the APK"""
    log("Generating assets for APK...")
    
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    try:
        # Try to use the dedicated asset generator if it exists
        if os.path.exists('generate_assets.py'):
            result = run_command([sys.executable, 'generate_assets.py'], capture_output=True)
            log(result.stdout)
            return True
        else:
            # Otherwise, use the basic asset generation in this file
            log("Asset generator not found, using basic asset generation")
            return _generate_basic_assets()
    except Exception as e:
        log(f"Error generating assets: {e}", error=True)
        return False

def _generate_basic_assets():
    """Generate basic assets if the asset generator is not available"""
    try:
        from PIL import Image, ImageDraw
        import random
        
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
        log("Generated TV static image")
        
        # Generate a simple app icon
        icon = Image.new('RGB', (192, 192), color=(10, 30, 60))
        draw = ImageDraw.Draw(icon)
        draw.rectangle([(20, 20), (172, 172)], fill=(0, 150, 255))
        draw.ellipse([(50, 50), (142, 142)], fill=(255, 255, 255))
        
        icon.save('assets/app_icon.png')
        log("Generated app icon")
        
        return True
    except ImportError:
        log("PIL not available, copying existing SVG files")
        # Copy any existing SVG files
        for file in ['tv_static.svg', 'tv_frame.svg', 'adtv_logo.svg']:
            if os.path.exists(file):
                import shutil
                shutil.copy(file, os.path.join('assets', file))
        return True
    except Exception as e:
        log(f"Error in basic asset generation: {e}", error=True)
        return False

def verify_files():
    """Verify all required files exist"""
    log("Verifying required files...")
    
    required_files = [
        'mobile_preview.py',
        'buildozer.spec'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        log(f"Missing required files: {', '.join(missing_files)}", error=True)
        return False
    
    # Verify mobile_preview.py can be compiled
    try:
        import py_compile
        py_compile.compile('mobile_preview.py')
        log("mobile_preview.py compiled successfully")
    except Exception as e:
        log(f"Error compiling mobile_preview.py: {e}", error=True)
        return False
    
    return True

def update_buildozer_spec():
    """Update buildozer.spec with production settings"""
    log("Updating buildozer.spec for production...")
    
    try:
        with open('buildozer.spec', 'r') as f:
            lines = f.readlines()
        
        updated_lines = []
        for line in lines:
            # Update version
            if line.strip().startswith('version ='):
                updated_lines.append(f'version = {APK_VERSION}\n')
            # Ensure directory paths are set
            elif line.strip().startswith('# bin_dir ='):
                updated_lines.append('bin_dir = ./bin\n')
            else:
                updated_lines.append(line)
        
        with open('buildozer.spec', 'w') as f:
            f.writelines(updated_lines)
            
        log("buildozer.spec updated successfully")
        return True
    except Exception as e:
        log(f"Error updating buildozer.spec: {e}", error=True)
        return False

def build_apk(build_mode='debug'):
    """Build the APK using buildozer"""
    log(f"Building APK in {build_mode} mode...")
    
    # Ensure bin directory exists
    if not os.path.exists('bin'):
        os.makedirs('bin')
    
    # Run buildozer
    try:
        run_command(['buildozer', 'android', build_mode])
        
        # Determine expected APK filename
        if build_mode == 'release':
            apk_path = f'bin/aiceosystem-{APK_VERSION}-arm64-v8a_armeabi-v7a-release.apk'
        else:
            apk_path = f'bin/aiceosystem-{APK_VERSION}-arm64-v8a_armeabi-v7a-debug.apk'
        
        # Check if old version filename exists if the expected one doesn't
        if not os.path.exists(apk_path):
            old_version_path = f'bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk'
            if os.path.exists(old_version_path):
                apk_path = old_version_path
        
        # Check if build was successful
        if os.path.exists(apk_path):
            apk_size = os.path.getsize(apk_path) / (1024 * 1024)  # Size in MB
            log(f"APK build completed successfully!")
            log(f"APK file: {apk_path}")
            log(f"APK size: {apk_size:.2f} MB")
            return True
        else:
            log("APK file not found after build", error=True)
            
            # Try to show the error from buildozer log
            import glob
            log_files = glob.glob('.buildozer/logs/buildozer-*.log')
            if log_files:
                latest_log = max(log_files, key=os.path.getctime)
                log(f"Showing last 20 lines from {latest_log}:")
                with open(latest_log, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-20:]:
                        log(line.strip())
            
            return False
    except Exception as e:
        log(f"Error building APK: {e}", error=True)
        return False

def main():
    """Main execution function"""
    log("Starting AI CEO APK Builder v1.0.0")
    
    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser(description='AI CEO APK Builder')
    parser.add_argument('--mode', choices=['debug', 'release'], default='debug',
                      help='Build mode (debug or release)')
    parser.add_argument('--debug', action='store_true',
                      help='Enable debug output')
    
    args = parser.parse_args()
    
    # Set debug mode based on arguments
    global DEBUG_MODE
    DEBUG_MODE = args.debug
    
    build_mode = args.mode
    log(f"Build mode: {build_mode}")
    log(f"Debug mode: {'Enabled' if DEBUG_MODE else 'Disabled'}")
    
    # Build process steps
    steps = [
        ("Check dependencies", check_dependencies),
        ("Update config version", update_config_version),
        ("Verify required files", verify_files),
        ("Update buildozer.spec", update_buildozer_spec),
        ("Generate assets", generate_assets),
        ("Build APK", lambda: build_apk(build_mode))
    ]
    
    # Execute build steps
    for step_name, step_func in steps:
        log(f"Step: {step_name}")
        success = step_func()
        if not success:
            log(f"Build failed at step: {step_name}", error=True)
            return 1
    
    log("AI CEO APK build completed successfully")
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
