
#!/bin/bash

echo "===================================================="
echo "        AI CEO SYSTEM - COMPLETE APK BUILD          "
echo "===================================================="

# Step 1: Install required dependencies
echo "[1/6] Installing dependencies..."
pip install --upgrade pip
pip install buildozer cython pillow flask requests

# Step 2: Generate configuration if not exists
echo "[2/6] Setting up configuration..."
if [ ! -f "ai_ceo_config.json" ]; then
    python -c "import json; print(json.dumps({
        'theme': 'default',
        'debug_mode': False,
        'token_balance': {'BBGT': 500, '918T': 20},
        'trial_expiry': $(date +%s) + 10800
    }, indent=4))" > ai_ceo_config.json
    echo "Created default configuration"
fi

# Step 3: Generate assets
echo "[3/6] Generating assets..."
# Create assets directory if it doesn't exist
mkdir -p assets
mkdir -p bin

# Run asset generation if it exists
if [ -f "generate_assets.py" ]; then
    python generate_assets.py
else
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
echo "[4/6] Verifying mobile_preview.py..."
python -m py_compile mobile_preview.py
if [ $? -ne 0 ]; then
    echo "Error in mobile_preview.py - please fix before building APK"
    exit 1
fi

# Step 5: Ensure build_apk.sh is executable
echo "[5/6] Setting up build script..."
chmod +x build_apk.sh

# Step 6: Build the APK
echo "[6/6] Building APK..."
./build_apk.sh

# Check if build was successful
if [ -f "bin/aiceosystem-0.1-arm64-v8a_armeabi-v7a-debug.apk" ]; then
    echo "===================================================="
    echo "Build completed successfully!"
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
