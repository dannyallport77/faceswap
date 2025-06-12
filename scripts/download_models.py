#!/usr/bin/env python3
"""
Download Pre-trained Models for FaceSwap

This script downloads commonly used pre-trained models for FaceSwap's extract pipeline:
- Face Detection Models (S3FD, MTCNN, CV2-DNN)
- Face Masking Models (U-Net DFL, BiSeNet-FP, VGG Clear, VGG Obstructed)

The models are automatically downloaded from the deepfakes-models GitHub repository
and cached in the .fs_cache directory for use by FaceSwap.
"""

import os
import sys
import logging
from lib.utils import GetModel

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def download_detection_models():
    """Download face detection models"""
    print("\n=== Downloading Face Detection Models ===")
    
    detection_models = [
        {
            'name': 'S3FD (Recommended face detector)',
            'git_id': 11,
            'filename': 's3fd_keras_v2.h5'
        },
        {
            'name': 'MTCNN (Multi-task CNN detector)', 
            'git_id': 2,
            'filename': ['mtcnn_det_v2.1.h5', 'mtcnn_det_v2.2.h5', 'mtcnn_det_v2.3.h5']
        },
        {
            'name': 'CV2-DNN (OpenCV DNN detector)',
            'git_id': 12, 
            'filename': ['opencv_face_detector_uint8_v1.pb', 'opencv_face_detector_v1.pbtxt']
        }
    ]
    
    for model_info in detection_models:
        try:
            print(f"\nDownloading: {model_info['name']}")
            model = GetModel(model_info['filename'], model_info['git_id'])
            print(f"✓ Downloaded to: {model.model_path}")
        except Exception as e:
            print(f"✗ Failed to download {model_info['name']}: {str(e)}")

def download_mask_models():
    """Download face masking models"""
    print("\n=== Downloading Face Masking Models ===")
    
    mask_models = [
        {
            'name': 'U-Net DFL (Deep Face Lab mask)',
            'git_id': 6,
            'filename': 'DFL_256_sigmoid_v1.h5'
        },
        {
            'name': 'BiSeNet-FP (Face parsing mask)',
            'git_id': 14,
            'filename': 'bisnet_face_parsing_v1.h5'  # Default version
        },
        {
            'name': 'VGG Clear (Clear face mask)',
            'git_id': 8,
            'filename': 'Nirkin_300_softmax_v1.h5'
        },
        {
            'name': 'VGG Obstructed (Obstructed face mask)',
            'git_id': 9,
            'filename': 'Nirkin_300_softmax_v1.h5'
        }
    ]
    
    for model_info in mask_models:
        try:
            print(f"\nDownloading: {model_info['name']}")
            model = GetModel(model_info['filename'], model_info['git_id'])
            print(f"✓ Downloaded to: {model.model_path}")
        except Exception as e:
            print(f"✗ Failed to download {model_info['name']}: {str(e)}")

def download_additional_models():
    """Download additional commonly used models"""
    print("\n=== Downloading Additional Models ===")
    
    additional_models = [
        {
            'name': 'BiSeNet-FP (Faceswap weights)',
            'git_id': 14,
            'filename': 'bisnet_face_parsing_v2.h5'  # Faceswap version
        }
    ]
    
    for model_info in additional_models:
        try:
            print(f"\nDownloading: {model_info['name']}")
            model = GetModel(model_info['filename'], model_info['git_id'])
            print(f"✓ Downloaded to: {model.model_path}")
        except Exception as e:
            print(f"✗ Failed to download {model_info['name']}: {str(e)}")

def main():
    """Main function to download all models"""
    print("FaceSwap Model Downloader")
    print("=" * 50)
    print("This will download pre-trained models for face detection and masking.")
    print("Models are downloaded from: https://github.com/deepfakes-models/faceswap-models")
    print("Models will be cached in the .fs_cache directory.")
    
    # Check if we're in the right directory
    if not os.path.exists('faceswap.py'):
        print("\nError: Please run this script from the faceswap directory.")
        print("Current directory:", os.getcwd())
        sys.exit(1)
    
    try:
        download_detection_models()
        download_mask_models() 
        download_additional_models()
        
        print("\n" + "=" * 50)
        print("✓ Model download completed!")
        print("\nYou can now use these models in FaceSwap's extract pipeline.")
        print("The models are cached and will be automatically used when you run extract.")
        
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
