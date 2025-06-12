#!/usr/bin/env python3
"""
Quick Start Demo Setup for FaceSwap
Creates a test project structure to demonstrate the workflow
"""

import os
import sys

def create_demo_structure():
    """Create a demo project structure"""
    base_path = os.path.expanduser("~/faceswap_demo")
    
    folders = [
        "source_videos",
        "person_a_faces", 
        "person_b_faces",
        "trained_model",
        "converted_output"
    ]
    
    print(f"Creating demo project structure at: {base_path}")
    
    # Create base directory
    os.makedirs(base_path, exist_ok=True)
    
    # Create subfolders
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"✓ Created: {folder_path}")
    
    # Create README with instructions
    readme_content = """# FaceSwap Demo Project

## Folder Structure:
- `source_videos/` - Put your source videos/images here
- `person_a_faces/` - Extracted faces from Person A (will be replaced)
- `person_b_faces/` - Extracted faces from Person B (replacement face)
- `trained_model/` - Your trained model will be saved here
- `converted_output/` - Final face-swapped results

## Workflow:
1. Place source videos in `source_videos/`
2. Extract faces using FaceSwap GUI or command line
3. Train model using the extracted faces
4. Convert videos using the trained model

## Next Steps:
1. Get 2 videos (or image sets) of different people
2. Place them in source_videos/
3. Follow the workflow guide to extract, train, and convert

See WORKFLOW_GUIDE.md for detailed instructions.
"""
    
    readme_path = os.path.join(base_path, "README.md")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✓ Created: {readme_path}")
    print(f"\n🎉 Demo project structure created at: {base_path}")
    print("\nTo get started:")
    print("1. Add videos/images to the source_videos folder")
    print("2. Use FaceSwap GUI to extract faces")
    print("3. Train a model") 
    print("4. Convert your videos")

if __name__ == "__main__":
    create_demo_structure()
