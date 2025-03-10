
#!/bin/bash

echo "===================================================="
echo "        AI CEO SYSTEM - COMPLETE APK BUILD          "
echo "                VERSION 1.0.0 RELEASE               "
echo "===================================================="

# Step 1: Install required dependencies
echo "[1/7] Installing dependencies..."
pip install --upgrade pip
pip install buildozer cython pillow flask requests

# Step 2: Generate configuration if not exists
echo "[2/7] Setting up configuration..."
if [ ! -f "ai_ceo_config.json" ]; then
    python -c "import json; print(json.dumps({
        'theme': 'default',
        'debug_mode': False,
        'token_balance': {'BBGT': 500, '918T': 20},
        'trial_expiry': $(date +%s) + 10800,
        'active_subscriptions': {},
        'version': '1.0.0'
    }, indent=4))" > ai_ceo_config.json
    echo "Created default configuration"
fi

# Step 3: Generate assets
echo "[3/7] Generating assets..."
mkdir -p assets
mkdir -p bin

if [ -f "generate_assets.py" ]; then
    python generate_assets.py
else
    echo "Asset generation script not found, copying default assets"
    # Copy existing SVG files to assets
    for file in tv_static.svg tv_frame.svg adtv_logo.svg; do
        if [ -f "$file" ]; then
            cp -n "$file" assets/
            echo "Copied $file to assets/"
        fi
    done
    
    # Copy audio files to assets
    for file in static_noise.wav; do
        if [ -f "$file" ]; then
            cp -n "$file" assets/
            echo "Copied $file to assets/"
        fi
    done
fi

# Step 4: Verify mobile_preview.py has no errors
echo "[4/7] Verifying mobile_preview.py..."
python -m py_compile mobile_preview.py
if [ $? -ne 0 ]; then
    echo "Error in mobile_preview.py - please fix before building APK"
    exit 1
fi

# Step 5: Update buildozer.spec with production settings
echo "[5/7] Updating buildozer.spec..."
# Ensure correct version is set
sed -i "s/version = .*/version = 1.0.0/" buildozer.spec 2>/dev/null || \
sed -i "" "s/version = .*/version = 1.0.0/" buildozer.spec

# Step 6: Ensure build_apk.sh is executable
echo "[6/7] Setting up build script..."
chmod +x build_apk.sh

# Step 7: Build the APK
echo "[7/7] Building production APK..."
./build_apk.sh

# Check if build was successful
if [ -f "bin/aiceosystem-1.0.0-arm64-v8a_armeabi-v7a-release.apk" ]; then
    echo "===================================================="
    echo "Build completed successfully!"
    echo "The release APK file is available at:"
    echo "bin/aiceosystem-1.0.0-arm64-v8a_armeabi-v7a-release.apk"
    echo "Download it using the Files tab in Replit."
    echo "===================================================="
elif [ -f "bin/aiceosystem-1.0.0-arm64-v8a_armeabi-v7a-debug.apk" ]; then
    echo "===================================================="
    echo "Build completed successfully!"
    echo "The debug APK file is available at:"
    echo "bin/aiceosystem-1.0.0-arm64-v8a_armeabi-v7a-debug.apk"
    echo "Download it using the Files tab in Replit."
    echo "===================================================="
elif [ -f "bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk" ]; then
    echo "===================================================="
    echo "Build completed with old version number!"
    echo "The APK file is available at:"
    echo "bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk"
    echo "Download it using the Files tab in Replit."
    echo "===================================================="
else
    echo "===================================================="
    echo "Build process completed but APK was not generated."
    echo "Check the logs above for errors."
    echo "===================================================="
fi
