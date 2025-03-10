
"""
APK Builder for AI CEO Mobile App
Builds Android APK for the application
"""

import os
import subprocess
import sys
import time
import shutil
from app_configurator import app_configurator

class APKBuilder:
    """Builds Android APK for the application"""
    
    def __init__(self, debug=True):
        """Initialize the APK builder"""
        self.debug = debug
        self.buildozer_spec = "buildozer.spec"
        self.output_dir = "bin"
        self.build_status = {
            "status": "not_started",
            "progress": 0,
            "message": "Build not started",
            "output_file": None
        }
    
    def log(self, message):
        """Log a message if debug is enabled"""
        if self.debug:
            print(f"[APK Builder] {message}")
    
    def check_buildozer_installed(self):
        """Check if buildozer is installed"""
        try:
            result = subprocess.run(
                ["buildozer", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                self.log(f"Buildozer is installed: {result.stdout.strip()}")
                return True
            else:
                self.log("Buildozer is not installed")
                return False
        except FileNotFoundError:
            self.log("Buildozer not found in PATH")
            return False
    
    def install_buildozer(self):
        """Install buildozer if not already installed"""
        self.log("Installing buildozer...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "buildozer"],
                check=True
            )
            self.log("Buildozer installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Failed to install buildozer: {str(e)}")
            return False
    
    def check_dependencies(self):
        """Check and install necessary dependencies"""
        # Check if buildozer is installed
        if not self.check_buildozer_installed():
            if not self.install_buildozer():
                self.log("Failed to install buildozer")
                return False
        
        # Check if buildozer spec exists
        if not os.path.exists(self.buildozer_spec):
            self.log(f"Buildozer spec file not found: {self.buildozer_spec}")
            self.log("Creating default buildozer spec...")
            try:
                subprocess.run(
                    ["buildozer", "init"],
                    check=True
                )
                self.log("Default buildozer spec created")
            except subprocess.CalledProcessError as e:
                self.log(f"Failed to create buildozer spec: {str(e)}")
                return False
        
        # Configure app using AppConfigurator
        app_configurator.configure_for_apk()
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        return True
    
    def clean_build(self):
        """Clean previous build files"""
        self.log("Cleaning previous build files...")
        try:
            if os.path.exists(".buildozer"):
                self.log("Removing .buildozer directory...")
                shutil.rmtree(".buildozer")
            
            self.log("Running buildozer clean...")
            subprocess.run(
                ["buildozer", "clean"],
                check=True
            )
            
            self.log("Clean completed successfully")
            return True
        except (subprocess.CalledProcessError, OSError) as e:
            self.log(f"Failed to clean build files: {str(e)}")
            return False
    
    def build_apk(self, clean=False):
        """Build the Android APK"""
        # Reset status
        self.build_status = {
            "status": "preparing",
            "progress": 5,
            "message": "Preparing build environment",
            "output_file": None
        }
        
        # Check dependencies
        if not self.check_dependencies():
            self.build_status.update({
                "status": "failed",
                "message": "Failed to prepare build environment"
            })
            return False
        
        # Clean if requested
        if clean:
            self.build_status["message"] = "Cleaning previous build files"
            if not self.clean_build():
                self.build_status.update({
                    "status": "failed",
                    "message": "Failed to clean build files"
                })
                return False
        
        # Start build
        self.build_status.update({
            "status": "building",
            "progress": 10,
            "message": "Building APK..."
        })
        
        self.log("Building APK...")
        try:
            # Run buildozer to create APK
            process = subprocess.Popen(
                ["buildozer", "android", "debug"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor output
            for line in process.stdout:
                line = line.strip()
                self.log(line)
                
                # Update progress based on output
                if "Gradle build done" in line:
                    self.build_status.update({
                        "progress": 90,
                        "message": "Gradle build completed"
                    })
                elif "Packaging" in line:
                    self.build_status.update({
                        "progress": 80,
                        "message": "Packaging APK"
                    })
                elif "Android SDK found" in line:
                    self.build_status.update({
                        "progress": 20,
                        "message": "Android SDK found"
                    })
                elif "Compiling" in line:
                    self.build_status.update({
                        "progress": 50,
                        "message": "Compiling sources"
                    })
            
            # Wait for process to complete
            process.wait()
            
            # Check if build was successful
            if process.returncode == 0:
                self.log("APK build completed successfully")
                
                # Find the APK file
                apk_files = [f for f in os.listdir(self.output_dir) if f.endswith(".apk")]
                if apk_files:
                    apk_path = os.path.join(self.output_dir, apk_files[0])
                    self.build_status.update({
                        "status": "success",
                        "progress": 100,
                        "message": "APK build completed successfully",
                        "output_file": apk_path
                    })
                    self.log(f"APK file: {apk_path}")
                    return True
                else:
                    self.build_status.update({
                        "status": "failed",
                        "progress": 90,
                        "message": "APK build completed but no APK file found"
                    })
                    self.log("No APK file found in the bin directory")
                    return False
            else:
                self.build_status.update({
                    "status": "failed",
                    "progress": 0,
                    "message": "APK build failed"
                })
                self.log("APK build failed")
                return False
                
        except Exception as e:
            self.build_status.update({
                "status": "failed",
                "message": f"Build error: {str(e)}"
            })
            self.log(f"Build error: {str(e)}")
            return False
    
    def get_build_status(self):
        """Get the current build status"""
        return self.build_status
        
    def generate_release_apk(self):
        """Generate a release APK"""
        self.log("Generating release APK...")
        # Clean and build
        if not self.clean_build():
            return False
        return self.build_apk(clean=True)

# Create instance for direct use
apk_builder = APKBuilder()

if __name__ == "__main__":
    # If run directly, build the APK
    if apk_builder.build_apk():
        print("APK build successful!")
        print(f"APK file: {apk_builder.build_status['output_file']}")
    else:
        print("APK build failed")
        print(f"Error: {apk_builder.build_status['message']}")
