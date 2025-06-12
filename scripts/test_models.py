#!/usr/bin/env python3
"""
Test FaceSwap Model Loading

This script tests that the downloaded models can be properly loaded
by FaceSwap's extraction plugins.
"""

import os
import sys
import logging

# Setup logging to suppress info messages during testing
logging.basicConfig(level=logging.WARNING)

def test_model_loading():
    """Test loading key models"""
    print("Testing FaceSwap Model Loading")
    print("=" * 40)
    
    tests = []
    
    # Test S3FD detector
    try:
        from plugins.extract.detect.s3fd import Detect as S3FDDetect
        detector = S3FDDetect()
        print("✅ S3FD face detector - Model loaded successfully")
        tests.append(("S3FD Detector", True))
    except Exception as e:
        print(f"❌ S3FD face detector - Failed: {str(e)}")
        tests.append(("S3FD Detector", False))
    
    # Test U-Net DFL mask
    try:
        from plugins.extract.mask.unet_dfl import Mask as UNetMask
        masker = UNetMask()
        print("✅ U-Net DFL mask - Model loaded successfully")
        tests.append(("U-Net DFL Mask", True))
    except Exception as e:
        print(f"❌ U-Net DFL mask - Failed: {str(e)}")
        tests.append(("U-Net DFL Mask", False))
    
    # Test BiSeNet mask
    try:
        from plugins.extract.mask.bisenet_fp import Mask as BiSeNetMask
        masker = BiSeNetMask()
        print("✅ BiSeNet-FP mask - Model loaded successfully")
        tests.append(("BiSeNet-FP Mask", True))
    except Exception as e:
        print(f"❌ BiSeNet-FP mask - Failed: {str(e)}")
        tests.append(("BiSeNet-FP Mask", False))
    
    # Test FAN alignment
    try:
        from plugins.extract.align.fan import Align as FANAlign
        aligner = FANAlign()
        print("✅ FAN 2D aligner - Model loaded successfully")
        tests.append(("FAN 2D Aligner", True))
    except Exception as e:
        print(f"❌ FAN 2D aligner - Failed: {str(e)}")
        tests.append(("FAN 2D Aligner", False))
    
    print("\n" + "=" * 40)
    print("Test Summary:")
    success_count = sum(1 for _, success in tests if success)
    total_count = len(tests)
    print(f"Passed: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 All models loaded successfully!")
        print("Your FaceSwap installation is ready for extraction.")
    else:
        print("⚠️  Some models failed to load.")
        print("This might be due to missing dependencies or model issues.")
    
    return success_count == total_count

def main():
    """Main test function"""
    # Check if we're in the right directory
    if not os.path.exists('faceswap.py'):
        print("Error: Please run this script from the faceswap directory.")
        print("Current directory:", os.getcwd())
        sys.exit(1)
    
    # Check if models exist
    cache_dir = ".fs_cache"
    if not os.path.exists(cache_dir) or not os.listdir(cache_dir):
        print("Error: No models found in cache directory.")
        print("Please run download_models.py first to download the models.")
        sys.exit(1)
    
    success = test_model_loading()
    
    if success:
        print("\n🚀 Next Steps:")
        print("1. Launch FaceSwap GUI: python faceswap.py gui")
        print("2. Or use command line: python faceswap.py extract -h")
        print("3. Check model_summary.py for detailed usage instructions")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
