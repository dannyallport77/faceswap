# Simple FaceSwap GUI - Tooltips Guide

This document lists all the tooltips available in the Simple FaceSwap GUI to help users understand each interface element.

## Main Interface Elements

### Progress Indicators
- **Step Label**: Shows your current step in the face-swapping process
- **Progress Bar**: Visual indicator of your overall progress through all steps
- **Notebook Tabs**: Click on tabs to navigate between different steps of the face-swapping process

### Navigation Controls
- **Previous Button**: Go back to the previous step in the workflow
- **Next Button**: Proceed to the next step (validates current step first)
- **Status Label**: Shows the current status of your project and any important messages

## Step 1: Project Setup

### Project Folder Section
- **Project Frame**: Your project folder will store all extracted faces, trained models, and converted results
- **Project Entry Field**: Path to your project folder - this will be created or selected using the buttons
- **Browse Button**: Select an existing folder to use as your project directory
- **Create New Button**: Create a new project folder with all necessary subdirectories automatically

## Step 2: Person A Training Data

### Training Material Section
- **Person A Frame**: Add videos or images containing Person A's face for training the AI model
- **Add Video(s) Button**: Add video files (.mp4, .avi, .mov, .mkv, .wmv) containing Person A's face for training
- **Add Images Button**: Add image files (.jpg, .png, .bmp, .tiff) containing Person A's face for training
- **Clear All Button**: Remove all Person A training files from the list
- **Person A Listbox**: Training material for Person A. The AI will learn this person's face to recognize it in other content.

## Step 3: Person B Training Data

### Training Material Section
- **Person B Frame**: Add videos/images of Person B - the face that will REPLACE Person A
- **Add Video(s) Button**: Add videos containing Person B's face for training the model
- **Add Images Button**: Add images containing Person B's face for training the model
- **Clear All Button**: Remove all Person B training files from the list
- **Person B Listbox**: Training material for Person B. The AI will learn this person's face to use as replacement.

## Step 4: Content to Convert

### Content Selection Section
- **Convert Frame**: Add the videos/images where you want to perform the face swap
- **Add Video(s) Button**: Add videos where Person A's face should be swapped with Person B's
- **Add Images Button**: Add images where Person A's face should be swapped with Person B's
- **Clear All Button**: Remove all content files from the list
- **Convert Listbox**: These files will have Person A's face replaced with Person B's face

## Step 5: Processing

### Processing Controls
- **Start Processing Button**: Begin the automated face-swapping process. This will extract faces, train the model, and convert your content.
- **Stop Button**: Stop the current processing operation (active during processing)

### Progress Monitoring
- **Progress Frame**: Monitor the progress of face extraction, model training, and content conversion
- **Progress Detail Label**: Shows which step is currently being processed
- **Detail Progress Bar**: Visual indicator showing that processing is active
- **Log Text Area**: Detailed log output showing the progress of extraction, training, and conversion operations

## Step 6: Results

### Results Section
- **Results Frame**: Access your completed face-swapped content and project information
- **Open Results Folder Button**: Open the folder containing your face-swapped videos and images
- **Open Project Folder Button**: Open the main project folder showing all extracted faces, models, and results
- **Start New Project Button**: Clear all current settings and start a fresh face-swapping project
- **Results Text Area**: Summary of your completed project including file counts and output locations

## Understanding the Workflow

### Training vs. Content:
- **Steps 2 & 3**: Training data teaches the AI what each person's face looks like
- **Step 4**: Content to convert is where the actual face swapping happens
- **Key**: Training data and content can be the same files, but serve different purposes

### Example:
1. **Step 2**: Add Tom Cruise movies (AI learns Tom's face)
2. **Step 3**: Add Nicolas Cage movies (AI learns Nicolas's face)
3. **Step 4**: Add Mission Impossible scene (Tom gets replaced with Nicolas)

## Tips for Best Results

1. **Hover over any interface element** to see its tooltip with helpful information
2. **Training Data Quality**: Use clear, well-lit faces with multiple angles and expressions
3. **Face Count**: Aim for 300-500 faces from each person for optimal results
4. **Processing Time**: Model training can take 12-48+ hours depending on your hardware
5. **File Organization**: The GUI automatically organizes all files in your project folder

## Troubleshooting

If tooltips are not appearing:
1. Make sure you're hovering over the correct interface element
2. Wait a moment - tooltips appear after a brief delay
3. Try moving your mouse away and back to the element
4. Ensure the GUI window has focus

For more detailed help, see the main documentation files:
- `SIMPLE_GUI_README.md` - Complete usage guide
- `WORKFLOW_GUIDE.md` - Step-by-step instructions
- `WORKFLOW_CLARIFICATION.md` - Explains the new 6-step design
- `FIX_SUMMARY.md` - Common issues and solutions
