# Simple FaceSwap GUI

A user-friendly, step-by-step interface for FaceSwap that makes face swapping easy for beginners.

## Features

🎯 **Step-by-Step Guidance**: Clear instructions for each phase of the process
🚀 **Automated Pipeline**: Handles extraction, training, and conversion automatically  
📁 **Project Management**: Organized folder structure for all your face swap projects
💻 **Progress Monitoring**: Real-time progress updates and detailed logging
🎬 **Multiple Formats**: Supports videos and images for both input and output
🔧 **Smart File Handling**: Automatically detects and handles different file types
⚡ **Mixed Media Support**: Process videos and images together seamlessly

## Quick Start

### Option 1: Use the Launcher (Recommended)
```bash
cd /Users/admin/Documents/faceswap/faceswap
python launch_simple.py
```

### Option 2: Direct Launch
```bash
cd /Users/admin/Documents/faceswap/faceswap
conda activate faceswap
python simple_gui.py
```

## How It Works

### Step 1: Project Setup
- Create a new project folder or select an existing one
- The tool automatically creates organized subfolders

### Step 2: Source Material (Person A)
- Add videos or images of the person whose face will be **replaced**
- Supports multiple files for better training quality

### Step 3: Target Material
- **Training Material (Person B)**: Add videos/images of the replacement face
- **Content to Convert**: Add the videos/images where you want to perform face swaps

### Step 4: Automated Processing
The tool automatically handles:
1. **Face Extraction**: Extracts faces from all source and target material
2. **Model Training**: Trains a custom face-swapping model (12-48+ hours)
3. **Face Conversion**: Applies face swaps to your content

### Step 5: Results
- View your face-swapped content in the `converted_output` folder
- Access all project files and intermediate results

## Project Structure

After creating a project, you'll have this organized structure:
```
MyProject/
├── source_faces/          # Extracted faces from Person A
├── target_faces/          # Extracted faces from Person B  
├── trained_model/         # Your custom face-swap model
├── converted_output/      # Final face-swapped results
├── source_material/       # Original source files
└── target_material/       # Original target files
```

## Requirements

- **Source Material**: Videos or images of Person A (face to be replaced)
- **Target Material**: Videos or images of Person B (replacement face)  
- **Content to Convert**: Videos or images for face swapping
- **Storage Space**: Several GB for models and processed content
- **Time**: Training can take 12-48+ hours depending on hardware

## Tips for Best Results

### Source Material Quality
- **Clear, well-lit faces** are essential
- **Multiple angles and expressions** improve model quality
- **At least 300-500 faces** for good results
- **Videos work better** than individual photos

### Hardware Considerations
- **GPU highly recommended** for training (Metal on Apple Silicon)
- **Plenty of RAM** (8GB+ recommended)
- **Fast storage** helps with large datasets

### Training Tips
- **Don't rush training** - let the model train thoroughly
- **Monitor preview window** to see model improvement
- **Save frequently** - training can be resumed if interrupted

## Troubleshooting

### Common Issues

**"No state file found" Error**
- This means you need to complete training first
- The Convert step requires a trained model with a state file

**"Input file is not a valid video" Error**
- ✅ FIXED: The GUI now automatically handles both images and videos
- Images are processed using temporary folders to work with FaceSwap's extraction

**Training Takes Too Long**
- Use fewer but higher quality extracted faces
- Reduce batch size in training settings
- Consider using a simpler model architecture

**Poor Quality Results**
- Extract more diverse faces (different angles, lighting)
- Train for more iterations
- Use higher resolution source material
- Adjust mask settings

**GUI Won't Launch**
- Make sure conda environment is activated: `conda activate faceswap`
- Check that all dependencies are installed
- Try launching from the launcher: `python launch_simple.py`

### Performance Tips

1. **Start Small**: Test with shorter videos first
2. **Quality over Quantity**: 500 good faces beat 2000 poor ones
3. **Similar Conditions**: Use source material with similar lighting/angles
4. **Monitor Progress**: Watch the preview to see model improvement

## Advanced Usage

### Command Line Alternative
The simple GUI generates these commands behind the scenes:

```bash
# Extract faces
python faceswap.py extract -i input_video.mp4 -o faces_folder

# Train model  
python faceswap.py train -A person_a_faces -B person_b_faces -m model_folder

# Convert with face swap
python faceswap.py convert -i input_video.mp4 -o output_video.mp4 -m model_folder
```

### Configuration
The simple GUI uses these recommended settings:
- **Detector**: S3FD (best balance of speed/accuracy)
- **Aligner**: FAN (Face Alignment Network)
- **Masker**: BiSeNet-FP (best for detailed face parsing)
- **Trainer**: Original (most stable for beginners)

## Support

For issues with the Simple GUI itself, check the terminal output for error messages.
For general FaceSwap issues, refer to the main [USAGE.md](USAGE.md) and [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md).

---

**Remember**: Face swapping requires patience! The extraction and training phases are crucial for good results. Don't skip the training step - it's what creates the "brain" that knows how to swap faces.
