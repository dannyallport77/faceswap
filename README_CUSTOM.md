# FaceSwap Custom - Enhanced Face Swapping Tool

This is a customized version of FaceSwap with enhanced features, simplified GUI, and Apple Silicon optimization.

## 🎯 Key Enhancements

### ✨ Simple GUI
- **Step-by-step interface** for beginners
- **Automated pipeline** handling extraction, training, and conversion
- **Mixed media support** (videos + images)
- **Real-time progress monitoring**
- **Project management** with organized folders

### 🚀 Apple Silicon Optimization
- **Metal GPU acceleration** support
- **Optimized dependencies** for M1/M2 Macs
- **Pre-configured environment** setup
- **Performance optimizations** for Apple hardware

### 📦 Enhanced Features
- **Automated model downloading** with verification
- **Comprehensive documentation** and guides
- **Error handling** with helpful troubleshooting
- **Demo projects** with examples
- **File type validation** and smart handling

## 🚀 Quick Start

### Simple GUI (Recommended)
```bash
cd /Users/admin/Documents/faceswap/faceswap
python launch_simple.py
```

### Traditional Interface
```bash
conda activate faceswap
python faceswap.py gui
```

## 📖 Documentation

- **[Simple GUI Guide](SIMPLE_GUI_README.md)** - Step-by-step face swapping
- **[Complete Workflow](WORKFLOW_GUIDE.md)** - Detailed process explanation
- **[Model Information](MODEL_DOWNLOAD_COMPLETE.md)** - Pre-trained models guide
- **[Fix Summary](FIX_SUMMARY.md)** - Recent improvements and fixes

## 🛠 Setup

### Prerequisites
- macOS with Apple Silicon (M1/M2) or Intel
- 8GB+ RAM recommended
- 10GB+ free storage space
- Conda or Python 3.10+

### Installation
```bash
# Clone this repository
git clone <your-repo-url>
cd faceswap

# Set up environment
conda env create -f requirements/requirements_apple_silicon.yml
conda activate faceswap

# Install dependencies
python setup.py

# Download pre-trained models
python scripts/download_models.py

# Launch Simple GUI
python launch_simple.py
```

## 🎭 How It Works

### Simple Workflow
1. **Project Setup** - Create organized project folder
2. **Add Source Material** - Videos/images of Person A (to be replaced)
3. **Add Target Material** - Videos/images of Person B (replacement face)
4. **Automated Processing** - Extract → Train → Convert
5. **View Results** - Face-swapped content ready

### Traditional Workflow
1. **Extract** faces from source material
2. **Train** custom face-swapping model
3. **Convert** content with face swaps

## 🔧 Features

### Smart File Handling
- ✅ Mixed video and image support
- ✅ Automatic file type detection
- ✅ Batch processing capabilities
- ✅ Temporary file management

### Enhanced GUI
- ✅ Step-by-step guidance
- ✅ Progress monitoring
- ✅ Error handling with tips
- ✅ Project organization

### Apple Silicon Optimization
- ✅ Metal GPU acceleration
- ✅ Optimized TensorFlow
- ✅ Memory management
- ✅ Performance tuning

## 📊 Supported Formats

### Input Formats
- **Videos**: .mp4, .avi, .mov, .mkv, .wmv
- **Images**: .jpg, .jpeg, .png, .bmp, .tiff

### Output Formats
- **Videos**: .mp4 (H.264)
- **Images**: .png, .jpg

## 🎯 System Requirements

### Minimum
- macOS 10.15+
- 4GB RAM
- 5GB storage space
- Any Mac (Intel or Apple Silicon)

### Recommended
- macOS 12.0+ with Apple Silicon
- 8GB+ RAM
- 10GB+ storage space
- GPU acceleration (Metal/CUDA)

## 🛠 Troubleshooting

### Common Issues

**"No state file found"**
- Complete training before attempting conversion
- Check that model folder contains `*_state.json`

**"Input file is not a valid video"**
- ✅ Fixed in this version with smart file handling
- Use Simple GUI for automatic file type detection

**Training too slow**
- Ensure GPU acceleration is enabled
- Reduce batch size in settings
- Use fewer but higher quality faces

**Poor results**
- Use more diverse training material
- Train for more iterations
- Ensure good lighting in source material

## 📈 Performance Tips

1. **Use GPU acceleration** (Metal on Apple Silicon)
2. **Quality over quantity** for training faces
3. **Similar lighting conditions** between source and target
4. **Monitor training progress** via preview window

## 🔄 Updates and Fixes

### Recent Improvements
- ✅ Fixed image processing errors
- ✅ Enhanced Simple GUI with validation
- ✅ Apple Silicon optimization
- ✅ Comprehensive documentation
- ✅ Automated model management

### Version History
- **v1.2** - Simple GUI with mixed media support
- **v1.1** - Apple Silicon optimization
- **v1.0** - Initial custom version

## 🤝 Contributing

This is a customized version of the original FaceSwap project. For contributions:

1. Fork this repository
2. Create feature branch
3. Test on Apple Silicon
4. Submit pull request

## 📄 License

Based on the original FaceSwap project license. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Original [FaceSwap project](https://github.com/deepfakes/faceswap)
- FaceSwap community and contributors
- Apple Silicon optimization community

## 📞 Support

For issues specific to this custom version:
- Check the documentation files in this repository
- Review the troubleshooting guides
- Test with the Simple GUI for better error handling

For general FaceSwap questions:
- Refer to the [original project documentation](https://github.com/deepfakes/faceswap)

---

**Note**: This is a customized version optimized for ease of use and Apple Silicon performance. It includes additional features not found in the original FaceSwap project.
