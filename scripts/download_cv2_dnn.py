#!/usr/bin/env python3
"""
Download CV2-DNN Model for FaceSwap

This script downloads the OpenCV DNN model separately since it had an issue
with the main download script.
"""

import os
import sys
import logging
from lib.utils import GetModel

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Download CV2-DNN model"""
    print("Downloading CV2-DNN (OpenCV DNN detector)")
    
    # Check if we're in the right directory
    if not os.path.exists('faceswap.py'):
        print("\nError: Please run this script from the faceswap directory.")
        print("Current directory:", os.getcwd())
        sys.exit(1)
    
    try:
        # Download CV2-DNN model with correct parameters
        print("\nDownloading: CV2-DNN (OpenCV DNN detector)")
        model = GetModel(['resnet_ssd_v1.caffemodel', 'resnet_ssd_v1.prototxt'], 4)
        print(f"✓ Downloaded to: {model.model_path}")
        
        print("\n✓ CV2-DNN model download completed!")
        print("You can now use the CV2-DNN detector in FaceSwap's extract pipeline.")
        
    except Exception as e:
        print(f"✗ Failed to download CV2-DNN model: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
