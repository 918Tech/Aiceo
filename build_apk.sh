
#!/bin/bash
echo "Setting up environment for APK building..."

# Install required dependencies
pip install --upgrade pip
pip install buildozer cython

# Create directories if they don't exist
mkdir -p assets
mkdir -p bin

# Make sure mobile_preview.py has no errors
echo "Verifying mobile_preview.py..."
python -m py_compile mobile_preview.py
if [ $? -ne 0 ]; then
    echo "Error in mobile_preview.py - please fix before building APK"
    exit 1
fi

# Run buildozer to create APK
echo "Building APK..."
buildozer android debug

# Check if build was successful
if [ -f "bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk" ]; then
    echo "APK build process completed successfully!"
    echo "The APK file is available at: bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk"
    echo "You can download it using the Files tab in Replit."
else
    echo "APK build failed. Check the logs for errors."
fi
