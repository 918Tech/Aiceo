
#!/bin/bash
echo "Setting up environment for APK building..."

# Install required dependencies
pip install --upgrade pip
pip install buildozer
pip install cython

# Create assets directory if it doesn't exist
mkdir -p assets

# Run buildozer to create APK
echo "Building APK..."
buildozer android debug

echo "APK build process completed!"
echo "The APK file should be available in the bin/ directory if build was successful."
