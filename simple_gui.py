#!/usr/bin/env python3
"""
Simple FaceSwap GUI - Step-by-Step Face Swapping

A simplified interface that guides users through the complete face-swapping workflow:
1. Select source faces (Person A - to be replaced)
2. Select target faces (Person B - replacement face)
3. Extract faces automatically
4. Train model automatically
5. Convert target video/images

This GUI handles all the complexity behind the scenes with clear progress indicators.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import threading
import subprocess
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List

class SimpleFaceSwapGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple FaceSwap - Step by Step")
        self.root.geometry("800x700")
        
        # Project state
        self.project_dir: Optional[str] = None
        self.source_files: List[str] = []
        self.target_files: List[str] = []
        self.current_step = 1
        self.total_steps = 5
        
        # Paths
        self.faceswap_dir = "/Users/admin/Documents/faceswap/faceswap"
        
        self.setup_ui()
        self.update_step_display()
        
    def setup_ui(self):
        """Create the user interface"""
        # Main title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = ttk.Label(title_frame, text="🎭 Simple FaceSwap", font=('Arial', 24, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Easy step-by-step face swapping", font=('Arial', 12))
        subtitle_label.pack()
        
        # Progress bar and step indicator
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(fill='x', padx=20, pady=10)
        
        self.step_label = ttk.Label(progress_frame, text="", font=('Arial', 14, 'bold'))
        self.step_label.pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(pady=5)
        
        # Main content area with notebook for steps
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Step 1: Project Setup
        self.setup_step1()
        
        # Step 2: Source Selection
        self.setup_step2()
        
        # Step 3: Target Selection  
        self.setup_step3()
        
        # Step 4: Processing
        self.setup_step4()
        
        # Step 5: Results
        self.setup_step5()
        
        # Control buttons
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill='x', padx=20, pady=10)
        
        self.prev_btn = ttk.Button(control_frame, text="← Previous", command=self.prev_step)
        self.prev_btn.pack(side='left')
        
        self.next_btn = ttk.Button(control_frame, text="Next →", command=self.next_step)
        self.next_btn.pack(side='right')
        
        # Status area
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill='x', padx=20, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready to start", foreground='green')
        self.status_label.pack()
        
    def setup_step1(self):
        """Step 1: Project Setup"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="1. Setup Project")
        
        # Instructions
        ttk.Label(frame, text="Step 1: Create or Select Project", 
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        instructions = """Welcome to Simple FaceSwap! This tool will guide you through swapping faces between people.

You'll need:
• Videos or images of Person A (source - face to be replaced)
• Videos or images of Person B (target - replacement face)  
• A video or image where you want to swap Person A's face with Person B's face

First, let's create a project folder to organize everything."""
        
        ttk.Label(frame, text=instructions, wraplength=600, justify='left').pack(pady=10)
        
        # Project selection
        project_frame = ttk.LabelFrame(frame, text="Project Folder", padding=10)
        project_frame.pack(fill='x', pady=10)
        
        self.project_var = tk.StringVar()
        project_entry = ttk.Entry(project_frame, textvariable=self.project_var, width=60)
        project_entry.pack(side='left', padx=5)
        
        ttk.Button(project_frame, text="Browse...", 
                  command=self.select_project_folder).pack(side='left', padx=5)
        
        ttk.Button(project_frame, text="Create New", 
                  command=self.create_new_project).pack(side='left', padx=5)
        
        # Tips
        tips_frame = ttk.LabelFrame(frame, text="💡 Tips", padding=10)
        tips_frame.pack(fill='x', pady=10)
        
        tips = """• Choose a location with plenty of space (models can be several GB)
• Avoid spaces or special characters in folder names
• Keep source material organized in subfolders"""
        
        ttk.Label(tips_frame, text=tips, justify='left').pack()
        
    def setup_step2(self):
        """Step 2: Source Selection"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="2. Source Files")
        
        ttk.Label(frame, text="Step 2: Select Source Material (Person A)", 
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        instructions = """Select videos or images of Person A (the person whose face will be REPLACED).

Tips for good source material:
• Clear, well-lit faces
• Multiple angles and expressions
• At least 300-500 faces for good results
• Videos work better than individual photos"""
        
        ttk.Label(frame, text=instructions, wraplength=600, justify='left').pack(pady=10)
        
        # Source file selection
        source_frame = ttk.LabelFrame(frame, text="Source Files (Person A)", padding=10)
        source_frame.pack(fill='both', expand=True, pady=10)
        
        buttons_frame = ttk.Frame(source_frame)
        buttons_frame.pack(fill='x', pady=5)
        
        ttk.Button(buttons_frame, text="Add Video(s)", 
                  command=lambda: self.add_files('source', 'video')).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Add Images", 
                  command=lambda: self.add_files('source', 'images')).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Clear All", 
                  command=lambda: self.clear_files('source')).pack(side='left', padx=5)
        
        self.source_listbox = tk.Listbox(source_frame, height=8)
        self.source_listbox.pack(fill='both', expand=True, pady=5)
        
        scrollbar1 = ttk.Scrollbar(source_frame, orient="vertical", command=self.source_listbox.yview)
        scrollbar1.pack(side="right", fill="y")
        self.source_listbox.configure(yscrollcommand=scrollbar1.set)
        
    def setup_step3(self):
        """Step 3: Target Selection"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="3. Target Files")
        
        ttk.Label(frame, text="Step 3: Select Target Material", 
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        instructions = """Now select your target material:

1. Training Images/Videos (Person B): Face that will REPLACE Person A
2. Content to Convert: The video/images where you want to perform the face swap"""
        
        ttk.Label(frame, text=instructions, wraplength=600, justify='left').pack(pady=10)
        
        # Target faces (Person B)
        target_faces_frame = ttk.LabelFrame(frame, text="Training Material (Person B)", padding=10)
        target_faces_frame.pack(fill='x', pady=5)
        
        buttons_frame2 = ttk.Frame(target_faces_frame)
        buttons_frame2.pack(fill='x', pady=5)
        
        ttk.Button(buttons_frame2, text="Add Video(s)", 
                  command=lambda: self.add_files('target_faces', 'video')).pack(side='left', padx=5)
        ttk.Button(buttons_frame2, text="Add Images", 
                  command=lambda: self.add_files('target_faces', 'images')).pack(side='left', padx=5)
        
        self.target_faces_listbox = tk.Listbox(target_faces_frame, height=4)
        self.target_faces_listbox.pack(fill='x', pady=5)
        
        # Convert content
        convert_frame = ttk.LabelFrame(frame, text="Content to Convert", padding=10)
        convert_frame.pack(fill='x', pady=5)
        
        buttons_frame3 = ttk.Frame(convert_frame)
        buttons_frame3.pack(fill='x', pady=5)
        
        ttk.Button(buttons_frame3, text="Add Video(s)", 
                  command=lambda: self.add_files('convert', 'video')).pack(side='left', padx=5)
        ttk.Button(buttons_frame3, text="Add Images", 
                  command=lambda: self.add_files('convert', 'images')).pack(side='left', padx=5)
        
        self.convert_listbox = tk.Listbox(convert_frame, height=4)
        self.convert_listbox.pack(fill='x', pady=5)
        
    def setup_step4(self):
        """Step 4: Processing"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="4. Processing")
        
        ttk.Label(frame, text="Step 4: Automatic Processing", 
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        instructions = """Click 'Start Processing' to begin the automatic face-swapping process:

1. Extract faces from source material (Person A)
2. Extract faces from target material (Person B)  
3. Train face-swapping model (this may take several hours)
4. Convert your content with face swaps

You can monitor progress below. Training can take 12-48+ hours depending on your hardware."""
        
        ttk.Label(frame, text=instructions, wraplength=600, justify='left').pack(pady=10)
        
        # Processing controls
        controls_frame = ttk.Frame(frame)
        controls_frame.pack(fill='x', pady=10)
        
        self.start_btn = ttk.Button(controls_frame, text="🚀 Start Processing", 
                                   command=self.start_processing, style='Accent.TButton')
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = ttk.Button(controls_frame, text="⏹ Stop", 
                                  command=self.stop_processing, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        # Progress details
        progress_frame = ttk.LabelFrame(frame, text="Processing Progress", padding=10)
        progress_frame.pack(fill='both', expand=True, pady=10)
        
        self.progress_detail = ttk.Label(progress_frame, text="Ready to start processing")
        self.progress_detail.pack(pady=5)
        
        self.detail_progress = ttk.Progressbar(progress_frame, length=500, mode='indeterminate')
        self.detail_progress.pack(pady=5)
        
        # Log output
        self.log_text = scrolledtext.ScrolledText(progress_frame, height=15, width=80)
        self.log_text.pack(fill='both', expand=True, pady=5)
        
    def setup_step5(self):
        """Step 5: Results"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="5. Results")
        
        ttk.Label(frame, text="Step 5: View Results", 
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        instructions = """Processing complete! Your face-swapped content is ready.

Results are saved in your project folder under 'converted_output'.
You can also view training progress and model information below."""
        
        ttk.Label(frame, text=instructions, wraplength=600, justify='left').pack(pady=10)
        
        # Results controls
        results_frame = ttk.LabelFrame(frame, text="Results", padding=10)
        results_frame.pack(fill='both', expand=True, pady=10)
        
        buttons_frame = ttk.Frame(results_frame)
        buttons_frame.pack(fill='x', pady=5)
        
        ttk.Button(buttons_frame, text="📁 Open Results Folder", 
                  command=self.open_results_folder).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="🎬 Open Project Folder", 
                  command=self.open_project_folder).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="🔄 Start New Project", 
                  command=self.new_project).pack(side='left', padx=5)
        
        # Results info
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.results_text.pack(fill='both', expand=True, pady=5)
        
    def update_step_display(self):
        """Update the progress bar and step indicator"""
        progress = (self.current_step - 1) / (self.total_steps - 1) * 100
        self.progress_bar['value'] = progress
        self.step_label.config(text=f"Step {self.current_step} of {self.total_steps}")
        
        # Update notebook selection
        self.notebook.select(self.current_step - 1)
        
        # Update button states
        self.prev_btn.config(state='normal' if self.current_step > 1 else 'disabled')
        self.next_btn.config(state='normal' if self.current_step < self.total_steps else 'disabled')
        
    def prev_step(self):
        """Go to previous step"""
        if self.current_step > 1:
            self.current_step -= 1
            self.update_step_display()
            
    def next_step(self):
        """Go to next step"""
        if self.validate_current_step():
            if self.current_step < self.total_steps:
                self.current_step += 1
                self.update_step_display()
                
    def validate_current_step(self) -> bool:
        """Validate current step before proceeding"""
        if self.current_step == 1:
            if not self.project_dir:
                messagebox.showerror("Error", "Please select or create a project folder first.")
                return False
                
        elif self.current_step == 2:
            if not self.source_files:
                messagebox.showerror("Error", "Please add source material (Person A) first.")
                return False
                
        elif self.current_step == 3:
            if not hasattr(self, 'target_faces_files') or not self.target_faces_files:
                messagebox.showerror("Error", "Please add training material (Person B) first.")
                return False
            if not hasattr(self, 'convert_files') or not self.convert_files:
                messagebox.showerror("Error", "Please add content to convert first.")
                return False
                
        return True
        
    def select_project_folder(self):
        """Select existing project folder"""
        folder = filedialog.askdirectory(title="Select Project Folder")
        if folder:
            self.project_dir = folder
            self.project_var.set(folder)
            self.status_label.config(text=f"Project: {folder}", foreground='green')
            
    def create_new_project(self):
        """Create new project folder"""
        folder = filedialog.askdirectory(title="Select Location for New Project")
        if folder:
            project_name = simpledialog.askstring("Project Name", "Enter project name:")
            if project_name:
                project_path = os.path.join(folder, project_name)
                try:
                    os.makedirs(project_path, exist_ok=True)
                    
                    # Create subfolders
                    subfolders = ['source_faces', 'target_faces', 'trained_model', 'converted_output', 'source_material', 'target_material']
                    for subfolder in subfolders:
                        os.makedirs(os.path.join(project_path, subfolder), exist_ok=True)
                    
                    self.project_dir = project_path
                    self.project_var.set(project_path)
                    self.status_label.config(text=f"Created project: {project_path}", foreground='green')
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create project: {str(e)}")
                    
    def add_files(self, file_type: str, media_type: str):
        """Add files to the appropriate list"""
        if not self.project_dir:
            messagebox.showerror("Error", "Please select a project folder first.")
            return
            
        if media_type == 'video':
            filetypes = [("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv")]
            files = filedialog.askopenfilenames(title=f"Select {media_type} files", filetypes=filetypes)
        else:
            filetypes = [("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
            files = filedialog.askopenfilenames(title=f"Select {media_type} files", filetypes=filetypes)
            
        if files:
            # Validate file types
            valid_files = []
            invalid_files = []
            
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}
            image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
            
            for file in files:
                file_ext = os.path.splitext(file.lower())[1]
                if media_type == 'video' and file_ext in video_extensions:
                    valid_files.append(file)
                elif media_type == 'images' and file_ext in image_extensions:
                    valid_files.append(file)
                else:
                    invalid_files.append(file)
            
            if invalid_files:
                invalid_names = [os.path.basename(f) for f in invalid_files]
                messagebox.showwarning("Invalid Files", 
                    f"The following files have invalid formats and were skipped:\n" + 
                    "\n".join(invalid_names))
            
            if valid_files:
                if file_type == 'source':
                    self.source_files.extend(valid_files)
                    self.update_listbox(self.source_listbox, self.source_files)
                elif file_type == 'target_faces':
                    if not hasattr(self, 'target_faces_files'):
                        self.target_faces_files = []
                    self.target_faces_files.extend(valid_files)
                    self.update_listbox(self.target_faces_listbox, self.target_faces_files)
                elif file_type == 'convert':
                    if not hasattr(self, 'convert_files'):
                        self.convert_files = []
                    self.convert_files.extend(valid_files)
                    self.update_listbox(self.convert_listbox, self.convert_files)
                    
                self.log_message(f"Added {len(valid_files)} {media_type} file(s) to {file_type}")
            else:
                messagebox.showinfo("No Valid Files", f"No valid {media_type} files were selected.")
                
    def update_listbox(self, listbox: tk.Listbox, files: List[str]):
        """Update listbox with file list"""
        listbox.delete(0, tk.END)
        for file in files:
            listbox.insert(tk.END, os.path.basename(file))
            
    def clear_files(self, file_type: str):
        """Clear files from list"""
        if file_type == 'source':
            self.source_files.clear()
            self.update_listbox(self.source_listbox, self.source_files)
            
    def start_processing(self):
        """Start the automated processing"""
        if not self.validate_all_inputs():
            return
            
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.detail_progress.start()
        
        # Start processing in background thread
        self.processing_thread = threading.Thread(target=self.run_processing)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        
    def validate_all_inputs(self) -> bool:
        """Validate all inputs before processing"""
        if not self.project_dir:
            messagebox.showerror("Error", "Project folder not selected.")
            return False
        if not self.source_files:
            messagebox.showerror("Error", "No source files selected.")
            return False
        if not hasattr(self, 'target_faces_files') or not self.target_faces_files:
            messagebox.showerror("Error", "No target face files selected.")
            return False
        if not hasattr(self, 'convert_files') or not self.convert_files:
            messagebox.showerror("Error", "No files to convert selected.")
            return False
        return True
        
    def run_processing(self):
        """Run the complete processing pipeline"""
        try:
            self.log_message("🚀 Starting FaceSwap processing pipeline...")
            
            # Step 1: Extract source faces
            self.update_progress("Extracting source faces (Person A)...")
            source_output = os.path.join(self.project_dir, 'source_faces')
            os.makedirs(source_output, exist_ok=True)
            
            for i, file in enumerate(self.source_files):
                self.log_message(f"Processing source file {i+1}/{len(self.source_files)}: {os.path.basename(file)}")
                self.extract_faces(file, source_output, "source")
                
            # Step 2: Extract target faces  
            self.update_progress("Extracting target faces (Person B)...")
            target_output = os.path.join(self.project_dir, 'target_faces')
            os.makedirs(target_output, exist_ok=True)
            
            for i, file in enumerate(self.target_faces_files):
                self.log_message(f"Processing target file {i+1}/{len(self.target_faces_files)}: {os.path.basename(file)}")
                self.extract_faces(file, target_output, "target")
                
            # Check if we have enough faces
            source_count = len([f for f in os.listdir(source_output) if f.endswith('.png')])
            target_count = len([f for f in os.listdir(target_output) if f.endswith('.png')])
            
            self.log_message(f"✅ Extraction complete: {source_count} source faces, {target_count} target faces")
            
            if source_count < 50:
                self.log_message("⚠️ Warning: Less than 50 source faces found. Results may be poor.")
            if target_count < 50:
                self.log_message("⚠️ Warning: Less than 50 target faces found. Results may be poor.")
                
            # Step 3: Train model
            self.update_progress("Training face-swapping model (this may take hours)...")
            model_dir = os.path.join(self.project_dir, 'trained_model')
            os.makedirs(model_dir, exist_ok=True)
            self.train_model(source_output, target_output, model_dir)
            
            # Step 4: Convert files
            self.update_progress("Converting files with face swaps...")
            output_dir = os.path.join(self.project_dir, 'converted_output')
            os.makedirs(output_dir, exist_ok=True)
            
            for i, file in enumerate(self.convert_files):
                self.log_message(f"Converting file {i+1}/{len(self.convert_files)}: {os.path.basename(file)}")
                self.convert_file(file, output_dir, model_dir)
                
            self.log_message("✅ Processing completed successfully!")
            self.update_progress("Processing completed!")
            
            # Switch to results tab
            self.root.after(0, lambda: self.show_results())
            
        except Exception as e:
            self.log_message(f"❌ Error during processing: {str(e)}")
            self.update_progress("Processing failed!")
            
            # Provide helpful error information
            if "not a valid video" in str(e):
                self.log_message("💡 Tip: Make sure image files are in a folder, not processed individually as videos")
            elif "No such file or directory" in str(e):
                self.log_message("💡 Tip: Check that all file paths are correct and files exist")
            elif "state file" in str(e):
                self.log_message("💡 Tip: Training needs to complete successfully before conversion")
                
        finally:
            self.root.after(0, self.processing_finished)
            
    def extract_faces(self, input_file: str, output_dir: str, face_type: str):
        """Extract faces from input file"""
        self.log_message(f"Extracting {face_type} faces from: {os.path.basename(input_file)}")
        
        # Check if input is a single image file
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        file_ext = os.path.splitext(input_file.lower())[1]
        
        if file_ext in image_extensions:
            # For single images, create a temporary folder and copy the image
            import shutil
            temp_input_dir = os.path.join(os.path.dirname(output_dir), f"temp_input_{face_type}")
            os.makedirs(temp_input_dir, exist_ok=True)
            
            # Copy image to temp folder
            temp_image_path = os.path.join(temp_input_dir, os.path.basename(input_file))
            shutil.copy2(input_file, temp_image_path)
            
            cmd = [
                'python', 'faceswap.py', 'extract',
                '-i', temp_input_dir,  # Use folder instead of single file
                '-o', output_dir,
                '-D', 's3fd',
                '-A', 'fan', 
                '-M', 'bisenet-fp'
            ]
            
            try:
                self.run_command(cmd)
            finally:
                # Clean up temp folder
                import shutil
                if os.path.exists(temp_input_dir):
                    shutil.rmtree(temp_input_dir)
        else:
            # For videos, use the file directly
            cmd = [
                'python', 'faceswap.py', 'extract',
                '-i', input_file,
                '-o', output_dir,
                '-D', 's3fd',
                '-A', 'fan', 
                '-M', 'bisenet-fp'
            ]
            
            self.run_command(cmd)
        
    def train_model(self, source_dir: str, target_dir: str, model_dir: str):
        """Train the face-swapping model"""
        self.log_message("Training model - this may take several hours...")
        
        cmd = [
            'python', 'faceswap.py', 'train',
            '-A', source_dir,
            '-B', target_dir, 
            '-m', model_dir,
            '-t', 'original',
            '-bs', '16'
        ]
        
        self.run_command(cmd)
        
    def convert_file(self, input_file: str, output_dir: str, model_dir: str):
        """Convert file with face swap"""
        self.log_message(f"Converting: {os.path.basename(input_file)}")
        
        # Check if input is a single image file
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}
        file_ext = os.path.splitext(input_file.lower())[1]
        
        if file_ext in image_extensions:
            # For images, create temp input folder and specify output image
            import shutil
            temp_input_dir = os.path.join(os.path.dirname(output_dir), "temp_convert_input")
            os.makedirs(temp_input_dir, exist_ok=True)
            
            # Copy image to temp folder
            temp_image_path = os.path.join(temp_input_dir, os.path.basename(input_file))
            shutil.copy2(input_file, temp_image_path)
            
            # Create temp output folder
            temp_output_dir = os.path.join(os.path.dirname(output_dir), "temp_convert_output")
            os.makedirs(temp_output_dir, exist_ok=True)
            
            cmd = [
                'python', 'faceswap.py', 'convert',
                '-i', temp_input_dir,
                '-o', temp_output_dir,
                '-m', model_dir
            ]
            
            try:
                self.run_command(cmd)
                
                # Move converted image to final output location
                converted_files = [f for f in os.listdir(temp_output_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
                if converted_files:
                    src_path = os.path.join(temp_output_dir, converted_files[0])
                    base_name = os.path.splitext(os.path.basename(input_file))[0]
                    dst_path = os.path.join(output_dir, f"swapped_{base_name}.png")
                    shutil.move(src_path, dst_path)
                    self.log_message(f"✅ Converted image saved: {os.path.basename(dst_path)}")
                    
            finally:
                # Clean up temp folders
                if os.path.exists(temp_input_dir):
                    shutil.rmtree(temp_input_dir)
                if os.path.exists(temp_output_dir):
                    shutil.rmtree(temp_output_dir)
                    
        elif file_ext in video_extensions:
            # For videos, use direct file conversion
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(output_dir, f"swapped_{base_name}.mp4")
            
            cmd = [
                'python', 'faceswap.py', 'convert',
                '-i', input_file,
                '-o', output_file,
                '-m', model_dir
            ]
            
            self.run_command(cmd)
            self.log_message(f"✅ Converted video saved: {os.path.basename(output_file)}")
            
        else:
            self.log_message(f"⚠️ Unsupported file format: {file_ext}")
            raise Exception(f"Unsupported file format: {file_ext}")
        
    def run_command(self, cmd: List[str]):
        """Run a command and capture output"""
        try:
            process = subprocess.Popen(
                cmd,
                cwd=self.faceswap_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            for line in process.stdout:
                self.log_message(line.strip())
                
            process.wait()
            if process.returncode != 0:
                raise Exception(f"Command failed with return code {process.returncode}")
                
        except Exception as e:
            self.log_message(f"Command failed: {str(e)}")
            raise
            
    def update_progress(self, message: str):
        """Update progress message"""
        self.root.after(0, lambda: self.progress_detail.config(text=message))
        
    def log_message(self, message: str):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.root.after(0, lambda: self.log_text.insert(tk.END, formatted_message))
        self.root.after(0, lambda: self.log_text.see(tk.END))
        
    def processing_finished(self):
        """Called when processing is complete"""
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.detail_progress.stop()
        
    def stop_processing(self):
        """Stop the processing"""
        # Implementation for stopping would go here
        self.log_message("⏹ Processing stopped by user")
        self.processing_finished()
        
    def show_results(self):
        """Switch to results tab and populate"""
        self.current_step = 5
        self.update_step_display()
        
        # Populate results
        results_info = f"""🎉 Face swapping completed successfully!

Project Location: {self.project_dir}

Files Processed:
• Source faces extracted: {len(self.source_files)} files
• Target faces extracted: {len(self.target_faces_files)} files  
• Content converted: {len(self.convert_files)} files

Results saved to: {os.path.join(self.project_dir, 'converted_output')}

You can find your face-swapped videos/images in the converted_output folder.
"""
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, results_info)
        
    def open_results_folder(self):
        """Open results folder in file manager"""
        if self.project_dir:
            results_path = os.path.join(self.project_dir, 'converted_output')
            os.system(f'open "{results_path}"')
            
    def open_project_folder(self):
        """Open project folder in file manager"""
        if self.project_dir:
            os.system(f'open "{self.project_dir}"')
            
    def new_project(self):
        """Start a new project"""
        self.project_dir = None
        self.source_files.clear()
        if hasattr(self, 'target_faces_files'):
            self.target_faces_files.clear()
        if hasattr(self, 'convert_files'):
            self.convert_files.clear()
        
        self.current_step = 1
        self.update_step_display()
        
        # Clear UI elements
        self.project_var.set("")
        self.source_listbox.delete(0, tk.END)
        self.target_faces_listbox.delete(0, tk.END)
        self.convert_listbox.delete(0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.results_text.delete(1.0, tk.END)
        
        self.status_label.config(text="Ready for new project", foreground='green')
        
    def run(self):
        """Start the GUI"""
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.root.mainloop()

def main():
    """Main entry point"""
    # Check if FaceSwap is available
    faceswap_dir = "/Users/admin/Documents/faceswap/faceswap"
    if not os.path.exists(os.path.join(faceswap_dir, "faceswap.py")):
        messagebox.showerror("Error", f"FaceSwap not found at {faceswap_dir}")
        return
        
    app = SimpleFaceSwapGUI()
    app.run()

if __name__ == "__main__":
    main()
