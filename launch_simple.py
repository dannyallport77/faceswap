#!/usr/bin/env python3
"""
Simple FaceSwap Launcher

A quick launcher for the simplified FaceSwap GUI that handles environment setup
and provides easy access to the step-by-step face swapping tool.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def check_faceswap():
    """Check if FaceSwap is properly installed"""
    faceswap_dir = "/Users/admin/Documents/faceswap/faceswap"
    
    if not os.path.exists(faceswap_dir):
        return False, f"FaceSwap directory not found: {faceswap_dir}"
    
    if not os.path.exists(os.path.join(faceswap_dir, "faceswap.py")):
        return False, f"faceswap.py not found in {faceswap_dir}"
        
    return True, "FaceSwap found and ready"

def activate_conda_env():
    """Activate conda environment if available"""
    try:
        # Check if conda environment exists
        result = subprocess.run(['conda', 'env', 'list'], capture_output=True, text=True)
        if 'faceswap' in result.stdout:
            return True, "Conda environment 'faceswap' detected"
        else:
            return False, "Conda environment 'faceswap' not found"
    except FileNotFoundError:
        return False, "Conda not found"

def launch_simple_gui():
    """Launch the simple GUI"""
    try:
        faceswap_dir = "/Users/admin/Documents/faceswap/faceswap"
        simple_gui_path = os.path.join(faceswap_dir, "simple_gui.py")
        
        # Try to run with conda environment first
        try:
            subprocess.run(['conda', 'run', '-n', 'faceswap', 'python', simple_gui_path], 
                         cwd=faceswap_dir, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to system python
            subprocess.run(['python', simple_gui_path], cwd=faceswap_dir, check=True)
            
    except Exception as e:
        messagebox.showerror("Launch Error", f"Failed to launch Simple FaceSwap GUI:\n{str(e)}")

def create_launcher_gui():
    """Create a simple launcher interface"""
    root = tk.Tk()
    root.title("Simple FaceSwap Launcher")
    root.geometry("500x400")
    
    # Title
    title_label = tk.Label(root, text="🎭 Simple FaceSwap", font=('Arial', 24, 'bold'))
    title_label.pack(pady=20)
    
    subtitle_label = tk.Label(root, text="Easy Face Swapping Tool", font=('Arial', 14))
    subtitle_label.pack(pady=5)
    
    # Status frame
    status_frame = tk.Frame(root)
    status_frame.pack(pady=20, padx=20, fill='x')
    
    tk.Label(status_frame, text="System Status:", font=('Arial', 12, 'bold')).pack(anchor='w')
    
    # Check dependencies
    deps_ok = check_dependencies()
    deps_status = "✅ Dependencies OK" if deps_ok else "❌ Missing dependencies"
    tk.Label(status_frame, text=f"• {deps_status}").pack(anchor='w')
    
    # Check FaceSwap
    fs_ok, fs_msg = check_faceswap()
    fs_status = f"✅ {fs_msg}" if fs_ok else f"❌ {fs_msg}"
    tk.Label(status_frame, text=f"• {fs_status}").pack(anchor='w')
    
    # Check conda
    conda_ok, conda_msg = activate_conda_env()
    conda_status = f"✅ {conda_msg}" if conda_ok else f"⚠️ {conda_msg}"
    tk.Label(status_frame, text=f"• {conda_status}").pack(anchor='w')
    
    # Instructions
    instructions = """
How to use Simple FaceSwap:

1. Click 'Launch Simple GUI' below
2. Create a new project or select existing folder
3. Add source material (Person A - face to replace)
4. Add target material (Person B - replacement face)
5. Add content to convert (videos/images for face swapping)
6. Click 'Start Processing' and wait for completion
7. View results in the converted_output folder

The tool will automatically:
• Extract faces from your material
• Train a custom face-swapping model
• Apply face swaps to your content
"""
    
    instructions_label = tk.Label(root, text=instructions, justify='left', wraplength=450)
    instructions_label.pack(pady=10, padx=20)
    
    # Launch button
    launch_button = tk.Button(root, text="🚀 Launch Simple GUI", 
                             command=lambda: [root.destroy(), launch_simple_gui()],
                             font=('Arial', 14, 'bold'),
                             bg='#4CAF50', fg='white',
                             relief='raised', bd=3)
    launch_button.pack(pady=20)
    
    # Additional buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    def open_full_gui():
        """Launch the full FaceSwap GUI"""
        try:
            faceswap_dir = "/Users/admin/Documents/faceswap/faceswap"
            subprocess.run(['conda', 'run', '-n', 'faceswap', 'python', 'faceswap.py', 'gui'], 
                         cwd=faceswap_dir)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch full GUI: {str(e)}")
    
    def open_demo_folder():
        """Open the demo project folder"""
        demo_path = "/Users/admin/faceswap_demo"
        if os.path.exists(demo_path):
            os.system(f'open "{demo_path}"')
        else:
            messagebox.showinfo("Info", "Demo folder not found. Create a project first using the Simple GUI.")
    
    tk.Button(button_frame, text="Full GUI", command=open_full_gui).pack(side='left', padx=5)
    tk.Button(button_frame, text="Demo Folder", command=open_demo_folder).pack(side='left', padx=5)
    
    # Warning if issues
    if not (deps_ok and fs_ok):
        warning_label = tk.Label(root, text="⚠️ Please resolve the issues above before launching", 
                               fg='red', font=('Arial', 10, 'bold'))
        warning_label.pack(pady=5)
        launch_button.config(state='disabled')
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == '--direct':
        # Direct launch of simple GUI
        launch_simple_gui()
    else:
        # Show launcher
        create_launcher_gui()

if __name__ == "__main__":
    main()
