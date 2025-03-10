
#!/bin/bash

# Complete APK Builder Script for AI CEO Mobile App
# This script handles all steps of the APK building process

set -e  # Exit on error

# Print colored output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}===============================================${NC}"
echo -e "${BLUE}     AI CEO MOBILE APP - COMPLETE APK BUILDER  ${NC}"
echo -e "${BLUE}===============================================${NC}"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Install dependencies
echo -e "\n${YELLOW}Step 1: Installing dependencies${NC}"
echo -e "=============================="

# Upgrade pip
echo -e "Upgrading pip..."
pip install --upgrade pip

# Install required Python packages
echo -e "Installing required Python packages..."
pip install buildozer cython pillow kivy==2.3.1

# Skip system package installation as dependencies are managed by replit.nix
echo -e "${GREEN}Using Replit-provided dependencies${NC}"

echo -e "${GREEN}Dependencies installed successfully!${NC}"

# Step 2: Create and configure necessary files
echo -e "\n${YELLOW}Step 2: Setting up project files${NC}"
echo -e "============================="

# Create directories
echo -e "Creating necessary directories..."
mkdir -p assets bin

# Check if required files exist
if [ ! -f "mobile_preview.py" ]; then
    echo -e "${RED}Error: mobile_preview.py not found.${NC}"
    echo -e "This file is required for building the APK."
    exit 1
fi

if [ ! -f "theme_manager.py" ]; then
    echo -e "${YELLOW}Warning: theme_manager.py not found. Creating default theme manager...${NC}"
    cat > theme_manager.py << 'EOF'
"""
Theme Manager for AI CEO Mobile App
Provides consistent styling across the application
"""

class ThemeManager:
    """Theme manager for providing consistent colors and styles"""
    
    def __init__(self):
        """Initialize theme manager with default theme"""
        self.current_theme = "default"
        self.themes = {
            "default": {
                "primary_color": (0, 0.6, 1, 1),
                "background_color": (0.08, 0.08, 0.15, 1),
                "secondary_color": (0.1, 0.3, 0.5, 1),
                "emergency_color": (0.8, 0, 0, 1),
                "success_color": (0.2, 0.8, 0.2, 1),
                "warning_color": (0.9, 0.7, 0.1, 1),
                "text_color": (1, 1, 1, 1),
                "text_secondary_color": (0.7, 0.7, 0.7, 1),
                "button_color": (0.1, 0.6, 0.9, 1),
                "button_secondary_color": (0.4, 0.4, 0.4, 1)
            }
        }
    
    def get_theme_color(self, color_type):
        """Get color for the current theme"""
        if color_type in self.themes[self.current_theme]:
            return self.themes[self.current_theme][color_type]
        return (1, 1, 1, 1)  # Default to white if color not found

# Create a singleton instance
theme_manager = ThemeManager()
EOF
    echo -e "${GREEN}Created default theme_manager.py${NC}"
fi

# Verify mobile_preview.py
echo -e "Verifying mobile_preview.py..."
if python -m py_compile mobile_preview.py; then
    echo -e "${GREEN}mobile_preview.py verified successfully${NC}"
else
    echo -e "${RED}Error in mobile_preview.py - please fix before building APK${NC}"
    exit 1
fi

echo -e "${GREEN}Project files set up successfully!${NC}"

# Step 3: Configure buildozer
echo -e "\n${YELLOW}Step 3: Configuring buildozer${NC}"
echo -e "==========================="

# Initialize buildozer if spec file doesn't exist
if [ ! -f "buildozer.spec" ]; then
    echo -e "Creating buildozer.spec..."
    buildozer init
    echo -e "${GREEN}Created default buildozer.spec${NC}"
fi

# Update important settings in buildozer.spec
echo -e "Updating buildozer.spec..."

# Set output directory
sed -i 's/# bin_dir = \.\//bin_dir = \.\/bin/g' buildozer.spec

# Set package name
sed -i 's/package.name = myapp/package.name = aiceosystem/g' buildozer.spec

# Set app name
sed -i 's/title = My Application/title = AI CEO System/g' buildozer.spec

# Set source.dir to include the current directory
sed -i 's/source.dir = ./source.dir = ./g' buildozer.spec

# Set requirements
sed -i 's/requirements = python3,kivy/requirements = python3,kivy==2.3.1,pillow/g' buildozer.spec

# Set permissions
sed -i 's/# android.permissions =/android.permissions = INTERNET,ACCESS_NETWORK_STATE/g' buildozer.spec

# Set orientation
sed -i 's/orientation = landscape/orientation = portrait/g' buildozer.spec

echo -e "${GREEN}Buildozer configured successfully!${NC}"

# Step 4: Build APK
echo -e "\n${YELLOW}Step 4: Building APK${NC}"
echo -e "===================="

echo -e "${BLUE}Starting APK build process...${NC}"
echo -e "This may take several minutes. Please be patient."

# Run buildozer
if buildozer android debug; then
    echo -e "${GREEN}Buildozer command completed successfully!${NC}"
else
    echo -e "${RED}Buildozer command failed. Checking for partial output...${NC}"
fi

# Check for APK file
apk_files=$(find bin -name "*.apk" 2>/dev/null || echo "")
if [ -n "$apk_files" ]; then
    echo -e "${GREEN}APK build successful!${NC}"
    echo -e "APK file(s) found:"
    for apk in $apk_files; do
        echo -e "  - ${BLUE}$apk${NC}"
    done
    echo -e "\nYou can download the APK using the Files tab in Replit."
else
    echo -e "${RED}No APK file found in the bin directory.${NC}"
    echo -e "The build process may have failed. Check the logs for errors."
    
    # Look for common errors in the buildozer.log
    if [ -f ".buildozer/logs/buildozer.log" ]; then
        echo -e "\n${YELLOW}Checking build logs for common errors...${NC}"
        
        if grep -q "NDK is missing" .buildozer/logs/buildozer.log; then
            echo -e "${RED}Error: Android NDK is missing.${NC}"
            echo -e "This is a common issue with Android builds on cloud environments."
        fi
        
        if grep -q "Unable to find any valuable Cutbuffer provider" .buildozer/logs/buildozer.log; then
            echo -e "${YELLOW}Warning: Clipboard functionality may be limited.${NC}"
            echo -e "This is not critical and can be ignored."
        fi
        
        if grep -q "buildozer.buildozer.TargetException" .buildozer/logs/buildozer.log; then
            echo -e "${RED}Error: Target exception occurred.${NC}"
            echo -e "This might be due to an environment configuration issue."
        fi
    fi
fi

# Final message
echo -e "\n${BLUE}===============================================${NC}"
echo -e "${BLUE}     AI CEO MOBILE APP - BUILD PROCESS COMPLETE  ${NC}"
echo -e "${BLUE}===============================================${NC}"

if [ -n "$apk_files" ]; then
    echo -e "${GREEN}Build completed successfully!${NC}"
    echo -e "You can download the APK from the bin directory."
else
    echo -e "${RED}Build did not produce an APK file.${NC}"
    echo -e "Please check the logs for errors and try again."
fi

echo -e "\nThank you for using the AI CEO Mobile App Builder!"
