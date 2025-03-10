
#!/bin/bash

echo "Setting up environment for production APK building..."

# Install required dependencies
pip install --upgrade pip
pip install buildozer cython pillow requests flask 

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
if [ ! -f "assets/tv_static.png" ] || [ ! -f "assets/tv_frame.png" ]; then
    echo "Generating assets..."
    if [ -f "generate_assets.py" ]; then
        python generate_assets.py
    else
        echo "Copying default assets..."
        cp -n tv_static.svg assets/ 2>/dev/null || :
        cp -n tv_frame.svg assets/ 2>/dev/null || :
        cp -n adtv_logo.svg assets/ 2>/dev/null || :
        cp -n static_noise.wav assets/ 2>/dev/null || :
    fi
fi

# Determine build type based on environment variable or argument
BUILD_TYPE=${1:-"debug"}
if [ "$BUILD_TYPE" == "release" ]; then
    echo "Building RELEASE APK..."
    # For release build, check if keystore exists
    if [ ! -f "aiceo.keystore" ]; then
        echo "No keystore found. Creating keystore for signing the release APK..."
        keytool -genkeypair -v -keystore aiceo.keystore -alias aiceo \
        -keyalg RSA -keysize 2048 -validity 10000 \
        -dname "CN=AI CEO System, OU=918 Technologies, O=918 Technologies LLC, L=Tulsa, ST=Oklahoma, C=US" \
        -storepass aiceopassword -keypass aiceopassword 2>/dev/null || \
        echo "Could not create keystore. Using debug build instead."
        BUILD_TYPE="debug"
    fi
fi

# Run buildozer to create APK
echo "Building APK with buildozer..."
if [ "$BUILD_TYPE" == "release" ]; then
    buildozer -v android release
else
    buildozer -v android debug
fi

# Check if build was successful
APK_PATH=""
if [ "$BUILD_TYPE" == "release" ] && [ -f "bin/aiceosystem-1.0.0-arm64-v8a_armeabi-v7a-release.apk" ]; then
    APK_PATH="bin/aiceosystem-1.0.0-arm64-v8a_armeabi-v7a-release.apk"
elif [ -f "bin/aiceosystem-1.0.0-arm64-v8a_armeabi-v7a-debug.apk" ]; then
    APK_PATH="bin/aiceosystem-1.0.0-arm64-v8a_armeabi-v7a-debug.apk"
elif [ -f "bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk" ]; then
    APK_PATH="bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk"
fi

if [ ! -z "$APK_PATH" ]; then
    echo "APK build process completed successfully!"
    echo "The APK file is available at: $APK_PATH"
    echo "You can download it using the Files tab in Replit."
    
    # Calculate file size for user information
    if [ -f "$APK_PATH" ]; then
        filesize=$(stat -c%s "$APK_PATH" 2>/dev/null || stat -f%z "$APK_PATH" 2>/dev/null || echo "Unknown")
        if [ "$filesize" != "Unknown" ]; then
            echo "APK Size: $(($filesize / 1024 / 1024)) MB"
        fi
        
        # Generate a QR code for easy download
        echo "To download via QR code, share the following URL:"
        echo "https://aiceosystem-${REPL_ID}.${REPL_OWNER}.repl.co/download/$APK_PATH"
    fi
else
    echo "APK build failed. Check the buildozer.log file for errors."
    
    # Display the last few lines of the buildozer log to help diagnose issues
    LATEST_LOG=$(find .buildozer/logs -name "buildozer-*.log" -type f -printf "%T@ %p\n" 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2)
    if [ -n "$LATEST_LOG" ] && [ -f "$LATEST_LOG" ]; then
        echo "Last 20 lines of buildozer log:"
        tail -n 20 "$LATEST_LOG"
    fi
fi
