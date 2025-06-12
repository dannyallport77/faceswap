# FaceSwap Complete Workflow Guide

## Overview
FaceSwap requires three main steps to swap faces between people:

1. **EXTRACT** - Extract faces from videos/images
2. **TRAIN** - Train a model to learn face mappings
3. **CONVERT** - Apply the trained model to swap faces

## Step 1: Extract Faces

### What you need:
- Source material (Person A): Video or images of the person whose face you want to replace
- Target material (Person B): Video or images of the person whose face will be the replacement

### GUI Method:
1. Open FaceSwap GUI: `python faceswap.py gui`
2. Go to **Extract** tab
3. **Input Dir/Video**: Select folder with Person A's images or a video file
4. **Output Dir**: Create a folder for extracted faces (e.g., `person_a_faces`)
5. **Detector**: Choose `s3fd` (recommended)
6. **Aligner**: Choose `fan`
7. **Masker**: Choose `bisenet-fp` 
8. Click **Extract**

Repeat for Person B into a different output folder (e.g., `person_b_faces`).

### Command Line Method:
```bash
# Extract Person A faces
python faceswap.py extract -i /path/to/person_a_video.mp4 -o /path/to/person_a_faces

# Extract Person B faces  
python faceswap.py extract -i /path/to/person_b_video.mp4 -o /path/to/person_b_faces
```

## Step 2: Train the Model

### What you need:
- Two folders of extracted faces from Step 1
- Time and computational power (training can take hours/days)

### GUI Method:
1. Go to **Train** tab
2. **Input A**: Select Person A's extracted faces folder
3. **Input B**: Select Person B's extracted faces folder  
4. **Model Dir**: Create a new folder for your model (e.g., `my_faceswap_model`)
5. **Trainer**: Choose `original` (recommended for beginners)
6. **Config**: Use default settings or adjust as needed
7. Click **Train**

### Command Line Method:
```bash
python faceswap.py train -A /path/to/person_a_faces -B /path/to/person_b_faces -m /path/to/model_folder
```

### Training Notes:
- Training creates a `*_state.json` file in your model folder
- Training can take 12-48+ hours depending on your hardware
- You can stop and resume training anytime
- Monitor the preview window to see progress
- Save iterations every 10,000-25,000 iterations

## Step 3: Convert (Face Swap)

### What you need:
- A trained model (with state file from Step 2)
- Source video/images to convert
- The faces folder used for training

### GUI Method:
1. Go to **Convert** tab
2. **Input Dir/Video**: Select video/images to convert
3. **Output Dir**: Select where to save converted results
4. **Alignments**: Select the alignments file from extraction
5. **Model Dir**: Select your trained model folder (must contain state file)
6. **Writer**: Choose output format (e.g., `opencv` for video)
7. **Config**: Adjust settings as needed
8. Click **Convert**

### Command Line Method:
```bash
python faceswap.py convert -i /path/to/input_video.mp4 -o /path/to/output_video.mp4 -m /path/to/trained_model
```

## Common Issues and Solutions

### "0 state files found" Error
**Problem**: Trying to convert without training a model first
**Solution**: Complete the training step first

### Poor Quality Results
**Solutions**:
- Extract more diverse faces (different angles, lighting)
- Train for more iterations
- Adjust mask settings
- Use higher resolution source material

### Training Takes Too Long
**Solutions**:
- Use fewer extracted faces (keep best quality ones)
- Reduce batch size in training config
- Use a simpler model architecture

## File Structure After Each Step

```
project_folder/
├── person_a_faces/          # Step 1 output
│   ├── 00001.png
│   ├── 00002.png
│   └── alignments.fsa
├── person_b_faces/          # Step 1 output  
│   ├── 00001.png
│   ├── 00002.png
│   └── alignments.fsa
├── my_model/               # Step 2 output
│   ├── original_state.json  # ← This file is required for convert!
│   ├── original_model.h5
│   └── preview_images/
└── converted_output/       # Step 3 output
    ├── converted_video.mp4
    └── converted_images/
```

## Quick Start Example

1. **Prepare source material**:
   ```bash
   mkdir -p ~/faceswap_project/{person_a_video,person_b_video,person_a_faces,person_b_faces,my_model,converted_output}
   ```

2. **Extract faces** (replace with your actual video paths):
   ```bash
   cd /Users/admin/Documents/faceswap/faceswap
   python faceswap.py extract -i ~/faceswap_project/person_a_video/video.mp4 -o ~/faceswap_project/person_a_faces
   python faceswap.py extract -i ~/faceswap_project/person_b_video/video.mp4 -o ~/faceswap_project/person_b_faces
   ```

3. **Train model**:
   ```bash
   python faceswap.py train -A ~/faceswap_project/person_a_faces -B ~/faceswap_project/person_b_faces -m ~/faceswap_project/my_model
   ```

4. **Convert** (after training completes):
   ```bash
   python faceswap.py convert -i ~/faceswap_project/person_a_video/video.mp4 -o ~/faceswap_project/converted_output/result.mp4 -m ~/faceswap_project/my_model
   ```

## Tips for Success

1. **Quality over quantity**: 500 good face images beat 2000 poor ones
2. **Similar conditions**: Use source material with similar lighting and angles
3. **Face size**: Faces should be at least 256x256 pixels
4. **Training time**: Don't rush - let the model train thoroughly
5. **Experiment**: Try different settings to find what works best for your material

---

**Remember**: The state file error means you need to train a model first!
