#!/bin/bash

# Quick Start Script for Biomimetic Bone Scaffold Generator
# Author: Siqi (Qizaifadacai)

echo "🦴 Biomimetic Bone Scaffold Generator"
echo "======================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.7+"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"
echo ""

# Check dependencies
echo "Checking dependencies..."
if python3 -c "import numpy, scipy, matplotlib" 2>/dev/null; then
    echo "✅ All dependencies installed"
else
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo ""
echo "🚀 Launching demo..."
echo ""

python3 demo.py
