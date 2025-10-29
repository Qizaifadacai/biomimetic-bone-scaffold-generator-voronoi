#!/bin/bash

# 🚀 Quick Start Script
# Biomimetic Bone Scaffold Generator

echo "🦴 Biomimetic Bone Scaffold Generator - Quick Start"
echo "=================================================="
echo ""

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.7 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Check if requirements are installed
echo "Checking dependencies..."
MISSING_DEPS=0

for package in numpy scipy matplotlib; do
    if ! python3 -c "import $package" 2>/dev/null; then
        echo "❌ Missing: $package"
        MISSING_DEPS=1
    else
        echo "✅ Found: $package"
    fi
done

echo ""

if [ $MISSING_DEPS -eq 1 ]; then
    echo "📦 Installing missing dependencies..."
    echo ""
    pip3 install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Installation failed. Please install manually:"
        echo "   pip3 install -r requirements.txt"
        exit 1
    fi
    
    echo ""
    echo "✅ All dependencies installed successfully!"
    echo ""
fi

# Run the demo
echo "🎬 Launching Interactive Demo..."
echo ""
echo "📝 Tips:"
echo "  • Enter numerical values in the text boxes"
echo "  • Press Enter to confirm"
echo "  • Click 'Generate Scaffold' to create"
echo "  • Click 'Save Visuals' to export images"
echo ""
echo "⏳ Starting in 3 seconds..."
sleep 3

python3 新版本演示.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Failed to launch. Possible issues:"
    echo "  1. Missing main module: 支持梯度的Voronoi支架生成器.py"
    echo "  2. Display environment not available"
    echo "  3. Dependency errors"
    echo ""
    echo "Try running manually:"
    echo "  python3 新版本演示.py"
fi
