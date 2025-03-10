
"""
App Configuration Helper for AI CEO Mobile App
Configures the application for different platforms and environments
"""

import os
import json
import shutil

class AppConfigurator:
    """Configures the application for different platforms and environments"""
    
    def __init__(self, config_file="app_config.json", debug=False):
        """Initialize the app configurator"""
        self.config_file = config_file
        self.debug = debug
        
        # Default configuration
        self.config = {
            "app_name": "AI CEO System",
            "package_name": "com.aiceo.management",
            "version": "1.0.0",
            "orientation": "portrait",
            "icon": "assets/app_logo.png",
            "splash": "assets/app_logo.png",
            "platforms": {
                "android": {
                    "min_sdk_version": 21,
                    "target_sdk_version": 33,
                    "build_mode": "debug"
                },
                "ios": {
                    "deployment_target": "12.0",
                    "build_mode": "debug"
                },
                "web": {
                    "enabled": True,
                    "port": 5000
                }
            },
            "modules": {
                "kivy": True,
                "kivymd": False,
                "camera": False,
                "maps": False,
                "notifications": True,
                "biometrics": False
            },
            "theme": {
                "primary_color": "#0088cc",
                "accent_color": "#ff9900",
                "background_color": "#101020",
                "text_color": "#ffffff",
                "dark_mode": True
            }
        }
        
        # Load existing configuration if available
        self.load_config()
    
    def load_config(self):
        """Load configuration from file if it exists"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
                if self.debug:
                    print(f"Configuration loaded from {self.config_file}")
            except Exception as e:
                if self.debug:
                    print(f"Error loading configuration: {str(e)}")
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            if self.debug:
                print(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            if self.debug:
                print(f"Error saving configuration: {str(e)}")
            return False
    
    def update_buildozer_spec(self, spec_file="buildozer.spec"):
        """Update buildozer.spec file with current configuration"""
        if not os.path.exists(spec_file):
            if self.debug:
                print(f"Buildozer spec file not found: {spec_file}")
            return False
        
        try:
            # Read the existing spec file
            with open(spec_file, 'r') as f:
                spec_content = f.readlines()
            
            # Update configuration values
            new_spec = []
            for line in spec_content:
                # App title
                if line.startswith("title ="):
                    new_spec.append(f"title = {self.config['app_name']}\n")
                # Package name
                elif line.startswith("package.name ="):
                    new_spec.append(f"package.name = {self.config['package_name']}\n")
                # App version
                elif line.startswith("version ="):
                    new_spec.append(f"version = {self.config['version']}\n")
                # Orientation
                elif line.startswith("orientation ="):
                    new_spec.append(f"orientation = {self.config['orientation']}\n")
                # Android SDK versions
                elif line.startswith("android.api ="):
                    new_spec.append(f"android.api = {self.config['platforms']['android']['target_sdk_version']}\n")
                elif line.startswith("android.minapi ="):
                    new_spec.append(f"android.minapi = {self.config['platforms']['android']['min_sdk_version']}\n")
                # Keep the line unchanged
                else:
                    new_spec.append(line)
            
            # Write the updated spec file
            with open(spec_file, 'w') as f:
                f.writelines(new_spec)
            
            if self.debug:
                print(f"Buildozer spec file updated: {spec_file}")
            return True
        
        except Exception as e:
            if self.debug:
                print(f"Error updating buildozer spec: {str(e)}")
            return False
    
    def ensure_icons_and_splash(self):
        """Ensure that icon and splash screen files exist"""
        # Check if icon file exists
        icon_path = self.config["icon"]
        if not os.path.exists(icon_path):
            if self.debug:
                print(f"Icon file not found: {icon_path}")
            
            # Create default icon directory if it doesn't exist
            os.makedirs(os.path.dirname(icon_path), exist_ok=True)
            
            # Copy default icon if available or create a simple one
            default_icon = "assets/app_logo.png"
            if os.path.exists(default_icon):
                shutil.copy(default_icon, icon_path)
                if self.debug:
                    print(f"Copied default icon to {icon_path}")
        
        # Check if splash screen file exists
        splash_path = self.config["splash"]
        if not os.path.exists(splash_path):
            if self.debug:
                print(f"Splash screen file not found: {splash_path}")
            
            # Create default splash directory if it doesn't exist
            os.makedirs(os.path.dirname(splash_path), exist_ok=True)
            
            # Copy default splash if available or create a simple one
            default_splash = "assets/app_logo.png"
            if os.path.exists(default_splash):
                shutil.copy(default_splash, splash_path)
                if self.debug:
                    print(f"Copied default splash to {splash_path}")
        
        return True
    
    def configure_for_apk(self):
        """Configure the app for Android APK building"""
        # Ensure all necessary directories exist
        os.makedirs("assets", exist_ok=True)
        os.makedirs("bin", exist_ok=True)
        
        # Ensure icon and splash images exist
        self.ensure_icons_and_splash()
        
        # Update buildozer spec
        self.update_buildozer_spec()
        
        # Update app configuration for Android
        self.config["platforms"]["android"]["build_mode"] = "debug"
        self.save_config()
        
        if self.debug:
            print("App configured for APK building")
        
        return True
    
    def get_required_packages(self):
        """Get a list of required packages based on the configuration"""
        packages = ["kivy==2.3.1"]
        
        if self.config["modules"]["kivymd"]:
            packages.append("kivymd==1.1.1")
        
        if self.config["modules"]["camera"]:
            packages.append("kivy-garden.xcamera")
        
        if self.config["modules"]["maps"]:
            packages.append("kivy-garden.mapview")
        
        return packages
    
    def get_permissions(self):
        """Get a list of required Android permissions based on the configuration"""
        permissions = ["INTERNET", "ACCESS_NETWORK_STATE"]
        
        if self.config["modules"]["camera"]:
            permissions.extend(["CAMERA", "WRITE_EXTERNAL_STORAGE"])
        
        if self.config["modules"]["maps"]:
            permissions.extend(["ACCESS_FINE_LOCATION", "ACCESS_COARSE_LOCATION"])
        
        if self.config["modules"]["notifications"]:
            permissions.extend(["VIBRATE", "RECEIVE_BOOT_COMPLETED"])
        
        if self.config["modules"]["biometrics"]:
            permissions.append("USE_BIOMETRIC")
        
        return permissions

# Instantiate for direct use
app_configurator = AppConfigurator(debug=True)

if __name__ == "__main__":
    # If run directly, perform full configuration
    app_configurator.configure_for_apk()
    print("App configuration complete!")
    print(f"Required packages: {', '.join(app_configurator.get_required_packages())}")
    print(f"Required permissions: {', '.join(app_configurator.get_permissions())}")
