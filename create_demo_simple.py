#!/usr/bin/env python3
"""
Simple FaceSwap Demo Setup

Creates a demo project with sample instructions and shows the workflow
without requiring actual video files.
"""

import os
import sys
from pathlib import Path

def create_demo_with_instructions():
    """Create a demo project with detailed instructions"""
    
    # Create demo project
    demo_path = Path.home() / "faceswap_demo_simple"
    demo_path.mkdir(exist_ok=True)
    
    # Create folder structure
    folders = [
        "01_source_material",
        "02_target_material", 
        "03_content_to_convert",
        "04_extracted_faces",
        "05_trained_model",
        "06_final_results"
    ]
    
    for folder in folders:
        (demo_path / folder).mkdir(exist_ok=True)
    
    # Create detailed instructions
    instructions = """# Simple FaceSwap Demo Project

Welcome to your Simple FaceSwap demo project! Follow these steps to swap faces.

## 📁 Folder Structure

### 01_source_material/
Put videos or images of **Person A** (the face you want to REPLACE)
- Example: Videos of Actor A, Celebrity A, or Person A
- Tip: 30-60 seconds of video OR 50-100 clear photos

### 02_target_material/  
Put videos or images of **Person B** (the REPLACEMENT face)
- Example: Videos of Actor B, Celebrity B, or Person B
- Tip: 30-60 seconds of video OR 50-100 clear photos

### 03_content_to_convert/
Put the videos or images where you want to perform the face swap
- Example: Movie scene with Person A that you want to replace with Person B
- This is your final output content

### 04_extracted_faces/ 
(Created automatically) - Extracted face images from your source material

### 05_trained_model/
(Created automatically) - Your custom trained face-swapping model

### 06_final_results/
(Created automatically) - Your final face-swapped videos/images

## 🚀 How to Use Simple FaceSwap

### Step 1: Prepare Your Material
1. Find good quality videos/images of both people
2. Place Person A material in `01_source_material/`
3. Place Person B material in `02_target_material/`
4. Place content to convert in `03_content_to_convert/`

### Step 2: Launch Simple GUI
Run: `python launch_simple.py` from the FaceSwap directory

### Step 3: Follow the GUI Steps
1. **Project Setup**: Select this demo folder as your project
2. **Source Files**: Add files from `01_source_material/`
3. **Target Files**: 
   - Training Material: Add files from `02_target_material/`
   - Content to Convert: Add files from `03_content_to_convert/`
4. **Processing**: Click "Start Processing" and wait (can take hours)
5. **Results**: Find your face-swapped content in `06_final_results/`

## ⚡ Quick Test Example

### Sample Workflow:
1. **Get test videos**:
   - Download a short video of Person A (5-10 seconds)
   - Download a short video of Person B (5-10 seconds)  
   - Download target content with Person A (what you want to convert)

2. **Place in folders**:
   ```
   01_source_material/person_a_video.mp4
   02_target_material/person_b_video.mp4
   03_content_to_convert/scene_with_person_a.mp4
   ```

3. **Run Simple FaceSwap**:
   - Launch the GUI
   - Point to this project folder
   - Add the files from each folder
   - Start processing
   - Wait for completion

4. **Results**:
   - Check `06_final_results/` for your face-swapped video
   - Person A's face should now look like Person B

## 💡 Tips for Success

### Source Material Quality:
- **Clear, well-lit faces** are crucial
- **Multiple angles** help the model learn better
- **Similar lighting conditions** between source and target
- **No obstructions** (sunglasses, hands covering face)

### Hardware Requirements:
- **GPU recommended** for faster training (hours vs days)
- **8GB+ RAM** for processing larger videos
- **Several GB storage** for extracted faces and models

### Realistic Expectations:
- **Training takes time**: 12-48+ hours is normal
- **Quality varies**: Better source material = better results
- **First attempt**: May not be perfect, can retrain with more data

## 🔧 Troubleshooting

### Common Issues:
- **"No state file found"**: Need to complete training first
- **Poor quality swaps**: Use better source material
- **Training too slow**: Reduce batch size or use GPU
- **Out of memory**: Process smaller videos or reduce resolution

### Getting Help:
- Check the terminal output for detailed error messages
- Refer to SIMPLE_GUI_README.md for more details
- Try the full FaceSwap GUI for advanced options

## 📋 Checklist

Before starting, make sure you have:
- [ ] Good quality source material (Person A)
- [ ] Good quality target material (Person B)  
- [ ] Content to convert (videos/images with Person A)
- [ ] Enough storage space (5-10GB+ free)
- [ ] Time to wait for training (hours)
- [ ] FaceSwap environment activated

---

**Remember**: Face swapping is an art and science. Good results require:
1. **Quality source material**
2. **Patience during training** 
3. **Experimentation with settings**
4. **Realistic expectations**

Start with short videos and simple scenarios before attempting complex swaps!
"""

    # Write instructions
    readme_path = demo_path / "README.md"
    with open(readme_path, 'w') as f:
        f.write(instructions)
    
    # Create placeholder files with instructions
    placeholders = {
        "01_source_material/PLACE_PERSON_A_FILES_HERE.txt": 
            "Place videos or images of Person A (face to be replaced) in this folder.\n\nGood formats: .mp4, .mov, .avi, .jpg, .png\nTip: 30-60 seconds of video OR 50-100 photos",
        
        "02_target_material/PLACE_PERSON_B_FILES_HERE.txt":
            "Place videos or images of Person B (replacement face) in this folder.\n\nGood formats: .mp4, .mov, .avi, .jpg, .png\nTip: 30-60 seconds of video OR 50-100 photos",
        
        "03_content_to_convert/PLACE_CONTENT_TO_CONVERT_HERE.txt":
            "Place the videos or images where you want to swap Person A's face with Person B's face.\n\nThis is your target content - the final output will have Person B's face on Person A's body.",
        
        "04_extracted_faces/README.txt":
            "This folder will contain extracted face images after running the extraction process.\nDo not manually add files here - they are generated automatically.",
        
        "05_trained_model/README.txt":
            "This folder will contain your trained face-swapping model.\nThe model learns how to convert Person A's face to Person B's face.\nTraining can take 12-48+ hours.",
        
        "06_final_results/README.txt":
            "This folder will contain your final face-swapped videos and images.\nAfter processing, check here for the converted content with face swaps applied."
    }
    
    for file_path, content in placeholders.items():
        full_path = demo_path / file_path
        with open(full_path, 'w') as f:
            f.write(content)
    
    print(f"✅ Demo project created at: {demo_path}")
    print("\n📋 Next steps:")
    print("1. Add your source material to the numbered folders")
    print("2. Run: python launch_simple.py")
    print("3. Select this demo folder as your project")
    print("4. Follow the step-by-step GUI")
    print(f"\n📖 Read the full instructions: {readme_path}")
    
    return str(demo_path)

if __name__ == "__main__":
    create_demo_with_instructions()
