
#!/bin/bash

# APK Builder Script for AI CEO Mobile App
# This script builds an Android APK for the AI CEO Mobile App

set -e  # Exit on error

# Print colored output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== AI CEO Mobile App - APK Builder ===${NC}"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install required dependencies
echo -e "${YELLOW}Installing required dependencies...${NC}"
pip install --upgrade pip
pip install buildozer cython pillow

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python_version=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "Python version: ${GREEN}$python_version${NC}"

# Create directories if they don't exist
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p assets
mkdir -p bin

# Generate assets if needed
echo -e "${YELLOW}Generating assets...${NC}"
if [ -f "generate_assets.py" ]; then
    python generate_assets.py
else
    echo -e "${RED}Warning: generate_assets.py not found${NC}"
fi

# Configure app
echo -e "${YELLOW}Configuring app...${NC}"
if [ -f "app_configurator.py" ]; then
    python app_configurator.py
else
    echo -e "${RED}Warning: app_configurator.py not found${NC}"
fi

# Make sure mobile_preview.py has no errors
echo -e "${YELLOW}Verifying mobile_preview.py...${NC}"
if python -m py_compile mobile_preview.py; then
    echo -e "${GREEN}mobile_preview.py verified successfully${NC}"
else
    echo -e "${RED}Error in mobile_preview.py - please fix before building APK${NC}"
    exit 1
fi

# Configure theme
echo -e "${YELLOW}Configuring app theme...${NC}"
if [ -f "theme_manager.py" ]; then
    echo -e "${GREEN}Theme manager found${NC}"
else
    echo -e "${YELLOW}Creating theme manager...${NC}"
    if [ -f "create_theme_manager.py" ]; then
        python create_theme_manager.py
    fi
fi

# Update buildozer.spec if needed
echo -e "${YELLOW}Updating buildozer.spec...${NC}"
if ! [ -f "buildozer.spec" ]; then
    echo -e "${YELLOW}Creating default buildozer.spec...${NC}"
    buildozer init
fi

# Set output directory in buildozer.spec
echo -e "${YELLOW}Setting output directory to bin/...${NC}"
sed -i 's/# bin_dir = \.\//bin_dir = \.\/bin/g' buildozer.spec

# Run buildozer to create APK
echo -e "${BLUE}Building APK...${NC}"
buildozer -v android debug

# Check if build was successful
if [ -d "bin" ]; then
    apk_count=$(find bin -name "*.apk" | wc -l)
    if [ "$apk_count" -gt 0 ]; then
        apk_file=$(find bin -name "*.apk" | head -1)
        echo -e "${GREEN}APK build process completed successfully!${NC}"
        echo -e "The APK file is available at: ${BLUE}$apk_file${NC}"
        echo -e "You can download it using the Files tab in Replit."
    else
        echo -e "${RED}APK build failed. No APK file found in bin directory.${NC}"
        echo -e "Check the logs for errors."
    fi
else
    echo -e "${RED}APK build failed. bin directory not found.${NC}"
    echo -e "Check the logs for errors."
fi

echo -e "${BLUE}=== Build process completed ===${NC}"
