
#!/bin/bash

echo "Setting up environment for APK building..."

# Install required dependencies
pip install --upgrade pip
pip install buildozer cython 

# Create required directories if they don't exist
mkdir -p assets
mkdir -p bin

# Make sure all required files exist for assets
if [ ! -d "assets" ]; then
    echo "Creating assets directory..."
    mkdir -p assets
fi

# Check for required files
if [ ! -f "mobile_preview.py" ]; then
    echo "Error: mobile_preview.py not found!"
    exit 1
fi

# Verify buildozer.spec exists
if [ ! -f "buildozer.spec" ]; then
    echo "Error: buildozer.spec not found!"
    exit 1
fi

# Make sure mobile_preview.py has no errors
echo "Verifying mobile_preview.py..."
python -m py_compile mobile_preview.py
if [ $? -ne 0 ]; then
    echo "Error in mobile_preview.py - please fix before building APK"
    exit 1
fi

# Create assets if needed
if [ ! -f "assets/tv_static.png" ]; then
    echo "Copying default assets..."
    cp -n tv_static.svg assets/ 2>/dev/null || :
    cp -n tv_frame.svg assets/ 2>/dev/null || :
    cp -n adtv_logo.svg assets/ 2>/dev/null || :
    cp -n static_noise.wav assets/ 2>/dev/null || :
fi

# Run buildozer to create APK
echo "Building APK..."
buildozer -v android debug

# Check if build was successful
if [ -f "bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk" ]; then
    echo "APK build process completed successfully!"
    echo "The APK file is available at: bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk"
    echo "You can download it using the Files tab in Replit."
    
    # Calculate file size for user information
    filesize=$(stat -c%s "bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk")
    echo "APK Size: $(($filesize / 1024 / 1024)) MB"
else
    echo "APK build failed. Check the buildozer.log file for errors."
    
    # Display the last few lines of the buildozer log to help diagnose issues
    if [ -f ".buildozer/logs/buildozer-$(date +%Y-%m-%d).log" ]; then
        echo "Last 20 lines of buildozer log:"
        tail -n 20 .buildozer/logs/buildozer-$(date +%Y-%m-%d).log
    fi
fi
