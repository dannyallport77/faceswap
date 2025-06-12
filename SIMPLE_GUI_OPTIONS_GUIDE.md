# FaceSwap Simple GUI - How to Select Different Options 🎛️

## Overview
The FaceSwap Simple GUI provides two main modes for different user skill levels:

- **🟢 Simple Mode**: Streamlined 5-step process for beginners
- **🔶 Advanced Mode**: Full 6-step process with more control

## Mode Selection

### 1. Choosing Your Mode
At the top of the interface, you'll see a **Mode Selection** dropdown:

```
Mode: [Simple ▼] or [Advanced ▼]
```

**Click the dropdown** to switch between:
- **Simple**: Recommended for beginners
- **Advanced**: For experienced users who want full control

When you change modes, the interface automatically updates to show the appropriate steps.

---

## Simple Mode (5 Steps) 🟢

### Step 1: 📁 Project Setup
- **Project Directory**: Click "Browse" to select where your project files will be stored
- **Model Name**: Enter a name for your AI model (e.g., "person_swap_project")

### Step 2: 🎭 NEW FACE Training
- **Add Videos**: Click to select video files containing the NEW face you want to use
- **Add Images**: Click to select image files containing the NEW face
- **Clear All**: Remove all selected files

### Step 3: 📺 Content to Convert  
- **Add Video(s)**: Select videos where faces will be replaced
- **Add Images**: Select images where faces will be replaced
- **Clear All**: Remove all selected content

### Step 4: ⚙️ Processing (Auto-configured)
Simple mode automatically sets optimal settings.

### Step 5: 📊 Results
View your completed face swaps and training progress.

---

## Advanced Mode (6 Steps) 🔶

### Step 1: 📁 Project Setup
Same as Simple Mode.

### Step 2: 🚫 ORIGINAL FACE Training
- **Add Videos**: Select videos containing the ORIGINAL face (to be removed)
- **Add Images**: Select images containing the ORIGINAL face
- **Clear All**: Remove all selected files

### Step 3: 🎭 NEW FACE Training  
- **Add Videos**: Select videos containing the NEW face (to replace with)
- **Add Images**: Select images containing the NEW face
- **Clear All**: Remove all selected files

### Step 4: 📺 Content to Convert
- **Add Video(s)**: Select videos where faces will be replaced
- **Add Images**: Select images where faces will be replaced  
- **Clear All**: Remove all selected content

### Step 5: ⚙️ Processing
Advanced settings for fine-tuning (detector, aligner, etc.)

### Step 6: 📊 Results
View your completed face swaps and training progress.

---

## Navigation Controls

### Step Navigation
- **Next Step**: Click to advance to the next step
- **Previous Step**: Click to go back to the previous step
- **Tab Selection**: Click directly on any tab (1, 2, 3, etc.) to jump to that step

### File Selection Options

#### Adding Files
1. **Add Videos**: Opens file browser filtered for video files (.mp4, .avi, .mov, etc.)
2. **Add Images**: Opens file browser filtered for image files (.jpg, .png, .bmp, etc.)
3. **Multiple Selection**: Hold `Cmd` (Mac) or `Ctrl` (Windows) to select multiple files

#### Managing Files
- **Clear All**: Removes all files from the current category
- **Individual Removal**: Select a file in the list and press `Delete` key
- **File List**: Scroll through your selected files in the listbox

---

## Detector & Processing Options (Advanced Mode)

When you reach the Processing step in Advanced Mode, you can select:

### Face Detectors
- **S3FD**: Best balance of speed and accuracy (recommended)
- **MTCNN**: Highest accuracy, slower processing
- **CV2-DNN**: Fastest, CPU-only, lower accuracy

### Face Aligners  
- **FAN**: Default aligner, good for most cases
- **CV2-DNN**: Alternative aligner option

### Masking Options
- **U-Net DFL**: General purpose mask (recommended)
- **BiSeNet-FP**: High-quality segmentation
- **VGG**: For clear, unobstructed faces

---

## Tips for Selecting Options

### ✅ Best Practices

1. **Start with Simple Mode** if you're new to face swapping
2. **Use high-quality source material** (good lighting, clear faces)
3. **Select multiple angles** of the same person for better results
4. **Match video quality** between source and target content

### ⚠️ Common Mistakes

1. **Don't mix different people** in the same training category
2. **Avoid blurry or low-resolution images**
3. **Don't use heavily makeup or filtered photos**
4. **Ensure faces are clearly visible** (not obscured)

### 🎯 File Selection Guidelines

**For Training Data:**
- 📹 **Videos**: 30 seconds to 5 minutes of clear face footage
- 🖼️ **Images**: 50-200 high-quality photos minimum
- 🎭 **Face Quality**: Well-lit, different angles, various expressions

**For Content to Convert:**
- 📺 **Target Videos**: Any length, good lighting preferred
- 🖼️ **Target Images**: High resolution for best results

---

## Validation and Error Checking

The GUI automatically validates your selections:

- ✅ **Green checkmarks**: Valid selections
- ❌ **Red warnings**: Missing or invalid files
- ⚠️ **Yellow alerts**: Recommendations for better results

### Required Fields
Each step requires specific files before you can proceed:
- **Step 2**: At least one source of NEW face training data
- **Step 3**: At least one piece of content to convert
- **Step 4**: Configuration validation

---

## Quick Start Example

### Simple Mode Workflow:
1. **Select "Simple" mode** from dropdown
2. **Step 1**: Choose project folder and name your model
3. **Step 2**: Add videos/images of the NEW face you want to use
4. **Step 3**: Add videos/images where faces should be replaced
5. **Step 4**: Click "Start Processing" (auto-configured)
6. **Step 5**: Review results

### Advanced Mode Workflow:
1. **Select "Advanced" mode** from dropdown  
2. **Step 1**: Set up project directory and model name
3. **Step 2**: Add ORIGINAL face training material (face to remove)
4. **Step 3**: Add NEW face training material (replacement face)
5. **Step 4**: Add content where swapping will occur
6. **Step 5**: Configure detector, aligner, and mask settings
7. **Step 6**: Review results and training progress

---

## Troubleshooting Selection Issues

### Files Not Appearing
- Check file formats are supported
- Ensure files aren't corrupted
- Verify file permissions

### Can't Proceed to Next Step  
- Ensure all required files are selected
- Check for validation errors (red text)
- Verify project directory has write permissions

### Mode Switch Problems
- Save your current progress first
- Some settings may reset when switching modes
- File selections are preserved across mode changes

---

This guide covers all the selection options available in the FaceSwap Simple GUI. The interface is designed to guide you through the process step-by-step, with validation and helpful hints along the way!
