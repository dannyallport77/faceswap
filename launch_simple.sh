#!/bin/bash
# Simple FaceSwap Desktop Launcher
# Double-click this file to launch the Simple FaceSwap GUI

echo "🎭 Starting Simple FaceSwap..."

# Navigate to FaceSwap directory
cd "/Users/admin/Documents/faceswap/faceswap"

# Activate conda environment and launch
conda activate faceswap
/Users/admin/micromamba/envs/faceswap/bin/python simple_gui.py

echo "Simple FaceSwap closed."
read -p "Press Enter to close this window..."
