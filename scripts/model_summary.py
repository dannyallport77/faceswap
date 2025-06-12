#!/usr/bin/env python3
"""
FaceSwap Model Summary

This script shows what models have been downloaded and provides guidance
on how to use them in FaceSwap.
"""

import os
import sys

def format_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

def main():
    cache_dir = "/Users/admin/Documents/faceswap/faceswap/.fs_cache"
    
    print("=" * 60)
    print("FaceSwap Pre-trained Models Summary")
    print("=" * 60)
    
    if not os.path.exists(cache_dir):
        print("❌ No models cache directory found.")
        sys.exit(1)
    
    model_info = {
        # Face Detection Models
        "s3fd_keras_v2.h5": {
            "type": "Face Detection",
            "name": "S3FD",
            "description": "Recommended face detector - good balance of speed and accuracy",
            "plugin": "s3fd"
        },
        "mtcnn_det_v2.1.h5": {
            "type": "Face Detection", 
            "name": "MTCNN Stage 1",
            "description": "Multi-task CNN detector - part of 3-stage cascade",
            "plugin": "mtcnn"
        },
        "mtcnn_det_v2.2.h5": {
            "type": "Face Detection",
            "name": "MTCNN Stage 2", 
            "description": "Multi-task CNN detector - part of 3-stage cascade",
            "plugin": "mtcnn"
        },
        "mtcnn_det_v2.3.h5": {
            "type": "Face Detection",
            "name": "MTCNN Stage 3",
            "description": "Multi-task CNN detector - part of 3-stage cascade", 
            "plugin": "mtcnn"
        },
        "resnet_ssd_v1.caffemodel": {
            "type": "Face Detection",
            "name": "CV2-DNN Model",
            "description": "OpenCV DNN face detector - CPU only",
            "plugin": "cv2_dnn"
        },
        "resnet_ssd_v1.prototxt": {
            "type": "Face Detection",
            "name": "CV2-DNN Config",
            "description": "OpenCV DNN network configuration",
            "plugin": "cv2_dnn"
        },
        
        # Face Masking Models
        "DFL_256_sigmoid_v1.h5": {
            "type": "Face Masking",
            "name": "U-Net DFL",
            "description": "DeepFaceLab mask - good general purpose mask",
            "plugin": "unet_dfl"
        },
        "bisnet_face_parsing_v1.h5": {
            "type": "Face Masking",
            "name": "BiSeNet-FP (Original)",
            "description": "Face parsing mask - original CelebAMask-HQ weights",
            "plugin": "bisenet_fp"
        },
        "bisnet_face_parsing_v2.h5": {
            "type": "Face Masking", 
            "name": "BiSeNet-FP (FaceSwap)",
            "description": "Face parsing mask - FaceSwap optimized weights",
            "plugin": "bisenet_fp"
        },
        "Nirkin_300_softmax_v1.h5": {
            "type": "Face Masking",
            "name": "VGG Clear/Obstructed",
            "description": "VGG-based mask for clear or obstructed faces",
            "plugin": "vgg_clear/vgg_obstructed"
        },
        
        # Face Alignment Models  
        "face-alignment-network_2d4_keras_v2.h5": {
            "type": "Face Alignment",
            "name": "FAN 2D",
            "description": "Face Alignment Network for landmark detection",
            "plugin": "fan"
        }
    }
    
    # Group models by type
    detection_models = []
    masking_models = []
    alignment_models = []
    other_models = []
    
    total_size = 0
    
    for filename in os.listdir(cache_dir):
        if filename.startswith('.'):
            continue
            
        filepath = os.path.join(cache_dir, filename)
        if not os.path.isfile(filepath):
            continue
            
        size = os.path.getsize(filepath)
        total_size += size
        size_str = format_size(size)
        
        if filename in model_info:
            info = model_info[filename]
            model_entry = f"  📁 {filename} ({size_str})\n     {info['name']} - {info['description']}\n     Plugin: {info['plugin']}\n"
            
            if info['type'] == 'Face Detection':
                detection_models.append(model_entry)
            elif info['type'] == 'Face Masking':
                masking_models.append(model_entry)
            elif info['type'] == 'Face Alignment':
                alignment_models.append(model_entry)
        else:
            other_models.append(f"  📁 {filename} ({size_str})\n")
    
    print(f"\n🎯 Face Detection Models:")
    print("   Used to find and locate faces in images/videos")
    for model in detection_models:
        print(model)
    
    print(f"🎭 Face Masking Models:")
    print("   Used to create masks for better face swapping")
    for model in masking_models:
        print(model)
        
    print(f"🎯 Face Alignment Models:")
    print("   Used to detect facial landmarks for alignment")
    for model in alignment_models:
        print(model)
    
    if other_models:
        print(f"📦 Other Models:")
        for model in other_models:
            print(model)
    
    print("=" * 60)
    model_count = len([f for f in os.listdir(cache_dir) if not f.startswith('.') and os.path.isfile(os.path.join(cache_dir, f))])
    print(f"Total models: {model_count}")
    print(f"Total size: {format_size(total_size)}")
    print("=" * 60)
    
    print("\n🚀 How to Use These Models:")
    print("\n1. **Face Detection** - Choose one detector:")
    print("   • S3FD: Recommended for most use cases")
    print("   • MTCNN: Good for small faces, slower but more accurate")
    print("   • CV2-DNN: CPU-only option, fastest but less accurate")
    
    print("\n2. **Face Masking** - Choose one mask:")
    print("   • U-Net DFL: Good general purpose mask")
    print("   • BiSeNet-FP: Best for detailed face parsing")
    print("   • VGG Clear: Good for clear, unobstructed faces")
    
    print("\n3. **Using in GUI:**")
    print("   • Go to Extract tab")
    print("   • Select your input folder/video")
    print("   • Select output folder")
    print("   • Choose plugins from dropdowns")
    print("   • Click 'Extract'")
    
    print("\n4. **Using Command Line:**")
    print("   python faceswap.py extract -i input_folder -o output_folder")
    print("   python faceswap.py extract -i input_video.mp4 -o output_folder")
    
    print("\n💡 The models are automatically loaded when you select the corresponding plugin!")
    print("   No need to manually specify model paths.")

if __name__ == "__main__":
    main()
