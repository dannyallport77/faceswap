# FaceSwap macOS Installer

Complete installation package for FaceSwap with Simple GUI on macOS (Intel and Apple Silicon).

## 📦 Installation Options

### Option 1: Command Line Installer (Recommended)
```bash
# Download and run the installer
curl -O https://raw.githubusercontent.com/dannyallport77/faceswap/main/install_macos.sh
chmod +x install_macos.sh
./install_macos.sh
```

### Option 2: GUI Installer
```bash
# Download and run the graphical installer
curl -O https://raw.githubusercontent.com/dannyallport77/faceswap/main/installer_gui.py
python3 installer_gui.py
```

### Option 3: Manual Installation
1. Clone the repository
2. Run the installer script from the project directory

## 🚀 What Gets Installed

### Core Components
- **FaceSwap Application**: Complete face-swapping software with Simple GUI
- **Python Environment**: Conda environment with all required dependencies
- **Pre-trained Models**: AI models for face detection, alignment, and masking (~800MB)
- **System Dependencies**: Required system packages via Homebrew

### User Interface
- **Simple GUI**: Easy-to-use step-by-step interface
- **Original GUI**: Advanced interface with full control
- **Command Line**: Full CLI access for power users

### Integration
- **Application Launcher**: macOS app bundle in Applications folder
- **Command Line Shortcuts**: Terminal aliases for easy access
- **Documentation**: Complete guides and tutorials

## 📋 System Requirements

### Supported Systems
- **macOS**: 10.15 (Catalina) or later
- **Architecture**: Intel (x86_64) and Apple Silicon (ARM64)
- **Memory**: 4GB RAM minimum, 8GB+ recommended
- **Storage**: 4GB free space minimum, 8GB+ recommended

### Dependencies (Auto-installed)
- **Homebrew**: Package manager for macOS
- **Conda/Miniforge**: Python environment manager
- **Git**: Version control system
- **Python 3.10**: Programming language runtime
- **System Libraries**: cmake, pkg-config, etc.

## 🔧 Installation Process

### Automatic Steps
1. **System Check**: Verify macOS version and architecture
2. **Homebrew**: Install or update package manager
3. **System Packages**: Install Git, CMake, Python, etc.
4. **Conda Environment**: Create isolated Python environment
5. **Python Dependencies**: Install TensorFlow, OpenCV, etc.
6. **FaceSwap Code**: Clone/update repository
7. **AI Models**: Download pre-trained models
8. **Integration**: Create launchers and shortcuts

### Apple Silicon Optimizations
- **TensorFlow Metal**: GPU acceleration for M1/M2/M3 chips
- **Optimized Dependencies**: Apple Silicon native packages
- **Performance Tuning**: Metal GPU support enabled

### Intel Mac Support
- **Standard TensorFlow**: CPU/GPU support
- **Legacy Compatibility**: Works with older Intel Macs
- **Performance**: Optimized for Intel architecture

## 🎯 Post-Installation

### Quick Start
1. **GUI Application**: Launch "FaceSwap Simple GUI" from Applications
2. **Command Line**: Use `faceswap-gui` in Terminal
3. **Documentation**: Read guides in installation folder

### Command Line Shortcuts
```bash
# Launch Simple GUI
faceswap-gui

# Launch original CLI
faceswap-cli --help

# View installed models
faceswap-models

# Activate environment
faceswap-env
```

### Application Locations
- **FaceSwap Files**: `~/Documents/faceswap/faceswap/`
- **App Launcher**: `/Applications/FaceSwap Simple GUI.app`
- **Documentation**: In FaceSwap directory
- **Models**: `~/Documents/faceswap/faceswap/.fs_cache/`

## 📚 Documentation Included

### User Guides
- **SIMPLE_GUI_README.md**: Complete Simple GUI tutorial
- **WORKFLOW_GUIDE.md**: Step-by-step face-swapping guide
- **TOOLTIPS_GUIDE.md**: Interface help reference
- **FIX_SUMMARY.md**: Troubleshooting and solutions

### Technical Documentation
- **README.md**: Main project documentation
- **INSTALL.md**: Installation details
- **USAGE.md**: Advanced usage instructions

## 🛠 Troubleshooting

### Common Issues
1. **Permission Errors**: Don't run installer as root/sudo
2. **Network Issues**: Ensure stable internet connection
3. **Disk Space**: Free up space if installation fails
4. **Architecture**: Installer auto-detects Intel vs Apple Silicon

### Getting Help
- Check the log output for specific error messages
- Review documentation files in installation directory
- Ensure system meets minimum requirements
- Try running installer again if network issues occur

## 🗑 Uninstallation

### Complete Removal
```bash
# Run the uninstaller
./uninstall_macos.sh
```

### What Gets Removed
- FaceSwap application files
- Conda environment
- Application launcher
- Command line aliases
- Cache and temporary files

### What Stays
- Personal projects and face-swapped content
- Homebrew installation (shared with other apps)
- Conda installation (shared with other environments)

## 🔒 Security & Privacy

### Data Handling
- **No Data Collection**: Installer doesn't send any personal data
- **Local Processing**: All face-swapping happens on your Mac
- **Open Source**: Complete source code available for review

### Permissions
- **File System**: Access to installation directories only
- **Network**: Only for downloading components during installation
- **Camera/Microphone**: Not used by installer

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the documentation files
3. Check the project's GitHub repository
4. Look for similar issues in the project's issue tracker

## 📄 License

This installer and FaceSwap software are provided under their respective open source licenses. See LICENSE files for details.
