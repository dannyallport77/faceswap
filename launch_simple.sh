#!/bin/bash
# Simple FaceSwap Desktop Launcher
# Double-click this file to launch the Simple FaceSwap GUI

echo "🎭 Starting Simple FaceSwap..."

# Navigate to FaceSwap directory
cd "/Users/admin/Documents/faceswap/faceswap"

# Activate conda environment and launch
conda activate faceswap
python launch_simple.py

echo "Simple FaceSwap closed."
read -p "Press Enter to close this window..."
