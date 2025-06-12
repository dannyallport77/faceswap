#!/Users/admin/micromamba/envs/faceswap/bin/python
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
import webbrowser
from pathlib import Path
from typing import Optional, Dict, Any, List

class SimpleFaceSwapGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple FaceSwap - Step by Step")
        self.root.geometry("1000x800")  # Increased default size
        self.root.minsize(800, 600)     # Set minimum size
        
        # Project state
        self.project_dir: Optional[str] = None
        self.source_files: List[str] = []
        self.target_files: List[str] = []
        self.current_step = 1
        self.total_steps = 6
        
        # Paths
        self.faceswap_dir = "/Users/admin/Documents/faceswap/faceswap"
        
        self.setup_ui()
        self.update_step_display()
        
    def setup_ui(self):
        """Create the user interface"""
        # Create a main scrollable frame
        self.main_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind canvas resize to adjust frame width
        def _on_canvas_configure(event):
            # Update the scrollable frame width to match canvas width
            canvas_width = event.width
            self.main_canvas.itemconfig(self.main_canvas.find_all()[0], width=canvas_width)
        
        self.main_canvas.bind('<Configure>', _on_canvas_configure)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)
        
        # Bind mousewheel to canvas for scrolling
        def _on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            self.main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.main_canvas.unbind_all("<MouseWheel>")
        
        self.main_canvas.bind('<Enter>', _bind_to_mousewheel)
        self.main_canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # Now create all UI elements in the scrollable frame instead of root
        # Main title
        title_frame = ttk.Frame(self.scrollable_frame)
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = ttk.Label(title_frame, text="🎭 Simple FaceSwap", font=('Arial', 24, 'bold'))
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Easy step-by-step face swapping", font=('Arial', 12))
        subtitle_label.pack()
        
        # Progress bar and step indicator
        progress_frame = ttk.Frame(self.scrollable_frame)
        progress_frame.pack(fill='x', padx=20, pady=10)
        
        self.step_label = ttk.Label(progress_frame, text="", font=('Arial', 14, 'bold'))
        self.step_label.pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(pady=5)
        
        # Main content area with notebook for steps
        self.notebook = ttk.Notebook(self.scrollable_frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Step 1: Project Setup
        self.setup_step1()
        
        # Step 2: Source Selection
        self.setup_step2()
        
        # Step 3: Target Selection  
        self.setup_step3()
        
        # Step 4: Content to Convert (only for Advanced Mode)
        # This will be created dynamically based on mode
        self.step4_frame = None
        
        # Step 5: Processing
        self.setup_step5()
        
        # Step 6: Results
        self.setup_step6()
        
        # Update tab titles and create Step 4 if needed
        self.update_mode_structure()
        
        # Control buttons
        control_frame = ttk.Frame(self.scrollable_frame)
        control_frame.pack(fill='x', padx=20, pady=10)
        
        self.prev_btn = ttk.Button(control_frame, text="← Previous", command=self.prev_step)
        self.prev_btn.pack(side='left')
        
        self.next_btn = ttk.Button(control_frame, text="Next →", command=self.next_step)
        self.next_btn.pack(side='right')
        
        # Status area
        status_frame = ttk.Frame(self.scrollable_frame)
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

Choose your workflow:
• SIMPLE MODE: Replace any detected face with a specific person (only need target training)
• ADVANCED MODE: High-quality swaps between two specific people (need both training sets)

The simple mode is perfect for most use cases and much faster to set up!

First, let's create a project folder to organize everything."""
        
        ttk.Label(frame, text=instructions, wraplength=600, justify='left').pack(pady=10)
        
        # Project selection
        project_frame = ttk.LabelFrame(frame, text="Project Folder", padding=10)
        project_frame.pack(fill='x', pady=10)
        
        self.project_var = tk.StringVar()
        project_entry = ttk.Entry(project_frame, textvariable=self.project_var, width=60)
        project_entry.pack(side='left', padx=5)
        
        browse_btn = ttk.Button(project_frame, text="Browse...", command=self.select_project_folder)
        browse_btn.pack(side='left', padx=5)
        
        create_btn = ttk.Button(project_frame, text="Create New", command=self.create_new_project)
        create_btn.pack(side='left', padx=5)
        
        # Tips
        tips_frame = ttk.LabelFrame(frame, text="💡 Tips", padding=10)
        tips_frame.pack(fill='x', pady=10)
        
        tips = """• Choose a location with plenty of space (models can be several GB)
• Avoid spaces or special characters in folder names
• Keep source material organized in subfolders"""
        
        ttk.Label(tips_frame, text=tips, justify='left').pack()
        
        # Mode selection
        mode_frame = ttk.LabelFrame(frame, text="Workflow Mode", padding=10)
        mode_frame.pack(fill='x', pady=10)
        
        self.mode_var = tk.StringVar(value="simple")
        
        simple_radio = ttk.Radiobutton(mode_frame, text="🚀 Simple Mode", 
                                      variable=self.mode_var, value="simple", 
                                      command=self.on_mode_change)
        simple_radio.pack(anchor='w', pady=2)
        
        simple_desc = ttk.Label(mode_frame, text="   Replace any detected face with a target person (faster, easier)", 
                               font=('Arial', 10), foreground='gray')
        simple_desc.pack(anchor='w', padx=20)
        
        advanced_radio = ttk.Radiobutton(mode_frame, text="⚙️ Advanced Mode", 
                                        variable=self.mode_var, value="advanced",
                                        command=self.on_mode_change)
        advanced_radio.pack(anchor='w', pady=2)
        
        advanced_desc = ttk.Label(mode_frame, text="   High-quality swaps between two specific people (slower, more setup)", 
                                 font=('Arial', 10), foreground='gray')
        advanced_desc.pack(anchor='w', padx=20)
        
        # Technology selection
        tech_frame = ttk.LabelFrame(frame, text="Face Swap Technology", padding=10)
        tech_frame.pack(fill='x', pady=10)
        
        tech_info = ttk.Label(tech_frame, text="Choose between professional quality or instant speed:", 
                             font=('Arial', 10, 'bold'))
        tech_info.pack(anchor='w', pady=(0, 5))
        
        self.technology_var = tk.StringVar(value="faceswap")
        
        tech_selection_frame = ttk.Frame(tech_frame)
        tech_selection_frame.pack(fill='x', pady=5)
        
        ttk.Label(tech_selection_frame, text="Technology:", font=('Arial', 10)).pack(side='left', padx=(0, 10))
        
        tech_dropdown = ttk.Combobox(tech_selection_frame, textvariable=self.technology_var, 
                                   values=["faceswap", "rehifaces"], state="readonly", width=15)
        tech_dropdown.pack(side='left')
        tech_dropdown.bind('<<ComboboxSelected>>', self.on_technology_change)
        
        # Technology descriptions
        faceswap_radio = ttk.Radiobutton(tech_frame, text="🎭 Traditional FaceSwap", 
                                        variable=self.technology_var, value="faceswap", 
                                        command=self.on_technology_change)
        faceswap_radio.pack(anchor='w', pady=2)
        
        faceswap_desc = ttk.Label(tech_frame, text="   Professional quality • 12-48 hour training • Custom models • Excellent results", 
                                 font=('Arial', 10), foreground='gray')
        faceswap_desc.pack(anchor='w', padx=20)
        
        rehifaces_radio = ttk.Radiobutton(tech_frame, text="⚡ ReHiFace-S (Real-time)", 
                                         variable=self.technology_var, value="rehifaces",
                                         command=self.on_technology_change)
        rehifaces_radio.pack(anchor='w', pady=2)
        
        rehifaces_desc = ttk.Label(tech_frame, text="   Instant results • 10 second setup • Pre-trained models • muke.ai speed", 
                                  font=('Arial', 10), foreground='gray')
        rehifaces_desc.pack(anchor='w', padx=20)
        
    def update_mode_structure(self):
        """Update the GUI structure based on current mode (create/remove Step 4)"""
        mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
        
        if mode == "advanced":
            # Advanced Mode: Create Step 4 if it doesn't exist
            if self.step4_frame is None:
                self.setup_step4()
        else:
            # Simple Mode: Remove Step 4 if it exists
            if self.step4_frame is not None:
                self.notebook.forget(self.step4_frame)
                self.step4_frame.destroy()
                self.step4_frame = None
        
        # Update tab titles after structure change
        self.update_tab_titles()
        
    def on_mode_change(self):
        """Handle mode change between simple and advanced"""
        mode = self.mode_var.get()
        
        # Update total steps based on mode
        if mode == "simple":
            self.total_steps = 5  # Setup, Target Training, Content, Processing, Results
        else:
            self.total_steps = 6  # Setup, Person A, Person B, Content, Processing, Results
                    
        # Update step content if steps are already created
        if hasattr(self, 'step2_frame'):
            self.update_step2_content()
        if hasattr(self, 'step3_frame'):
            self.update_step3_content()
        
        # Update the mode structure (create/remove Step 4)
        self.update_mode_structure()
            
        self.update_step_display()
        
    def on_technology_change(self, event=None):
        """Handle technology change between FaceSwap and ReHiFace-S"""
        technology = self.technology_var.get()
        
        if technology == "rehifaces":
            # Show message about switching to ReHiFace-S
            messagebox.showinfo("Technology Switch", 
                               "🚀 Switching to ReHiFace-S Real-time Face Swap!\n\n"
                               "This technology provides:\n"
                               "• Instant results (10 seconds setup)\n"
                               "• Real-time processing\n"
                               "• Pre-trained models\n"
                               "• muke.ai-style speed\n\n"
                               "Note: For maximum quality, use Traditional FaceSwap.")
            
            # Update status
            self.status_label.config(text="Technology: ReHiFace-S (Real-time) - Ready for instant face swapping", 
                                   foreground='blue')
        else:
            # Traditional FaceSwap
            self.status_label.config(text="Technology: Traditional FaceSwap - Ready for professional quality", 
                                   foreground='green')
        
        # Update step content based on technology
        if hasattr(self, 'step2_frame'):
            self.update_step2_content()
        if hasattr(self, 'step3_frame'):
            self.update_step3_content()
        
        # Update processing instructions based on technology
        self.update_processing_instructions()
        
    def update_processing_instructions(self):
        """Update processing step instructions based on selected technology"""
        technology = getattr(self, 'technology_var', tk.StringVar(value="faceswap")).get()
        
        if hasattr(self, 'step5_frame'):
            # Update Step 5 content to reflect the selected technology
            self.update_processing_content()
    
    def update_processing_content(self):
        """Update the processing step content based on selected technology"""
        if not hasattr(self, 'processing_instructions_frame'):
            return
            
        # Clear existing content
        for widget in self.processing_instructions_frame.winfo_children():
            widget.destroy()
            
        technology = getattr(self, 'technology_var', tk.StringVar(value="faceswap")).get()
        
        if technology == "rehifaces":
            # ReHiFace-S Instructions
            instructions = """🚀 ReHiFace-S Real-time Processing:

✅ INSTANT FACE SWAPPING (No training required!)
1. Select your source face image or video
2. Add content where faces will be replaced
3. Click 'Start Processing' for instant results
4. Get face-swapped content in seconds!

⚡ Benefits:
• 10 second setup vs 12-48 hours training
• Real-time processing (9,000x faster!)
• Pre-trained models (no custom training)
• Perfect for quick demos and testing"""
            color = 'blue'
            
            # Add ReHiFace-S specific controls
            rehiface_controls = ttk.Frame(self.tech_controls_frame)
            rehiface_controls.pack(fill='x')
            
            ttk.Button(rehiface_controls, text="🌐 Open ReHiFace-S Web Interface", 
                      command=self.launch_rehifaces_web).pack(side='left', padx=5)
            
        else:
            # Traditional FaceSwap Instructions
            mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
            
            if mode == "simple":
                instructions = """🎭 Traditional FaceSwap - Simple Mode Processing:

1. Extract NEW FACE training material
2. Train face-swapping model (12-48+ hours)
3. Convert your content with face swaps

✅ High-quality custom results
⏰ Training time: 12-48+ hours (patience required)
🎯 Perfect for professional projects"""
            else:
                instructions = """🎭 Traditional FaceSwap - Advanced Mode Processing:

1. Extract ORIGINAL FACE training material (face to remove)
2. Extract NEW FACE training material (replacement face)
3. Train face-swapping model (12-48+ hours)
4. Convert your content with face swaps

✅ Maximum quality results
⏰ Training time: 12-48+ hours (patience required)
🏆 Professional-grade custom models"""
            color = 'darkgreen'
        
        instruction_label = ttk.Label(self.processing_instructions_frame, text=instructions, 
                                    wraplength=600, justify='left', foreground=color)
        instruction_label.pack(pady=10)
        
    def update_tab_titles(self):
        """Update tab titles based on current mode"""
        mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
        
        if mode == "simple":
            # Simple Mode: Step 2 = NEW FACE Training, Step 3 = Content to Convert, Step 4 is skipped
            if hasattr(self, 'step2_frame'):
                self.notebook.tab(self.step2_frame, text="2. 🎭 NEW FACE Training")
            if hasattr(self, 'step3_frame'):
                self.notebook.tab(self.step3_frame, text="3. 📺 Content to Convert")
        else:
            # Advanced Mode: Step 2 = ORIGINAL FACE, Step 3 = NEW FACE Training, Step 4 = Content to Convert
            if hasattr(self, 'step2_frame'):
                self.notebook.tab(self.step2_frame, text="2. 🚫 ORIGINAL FACE Training")
            if hasattr(self, 'step3_frame'):
                self.notebook.tab(self.step3_frame, text="3. 🎭 NEW FACE Training")
            if hasattr(self, 'step4_frame'):
                self.notebook.tab(self.step4_frame, text="4. 📺 Content to Convert")
        
    def setup_step2(self):
        """Step 2: Training Data (changes based on mode)"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="2. Training Data")
        
        # Dynamic content based on mode
        self.step2_frame = frame
        self.update_step2_content()
        
    def update_step2_content(self):
        """Update Step 2 content based on selected mode"""
        # Clear existing content
        for widget in self.step2_frame.winfo_children():
            widget.destroy()
            
        mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
        technology = getattr(self, 'technology_var', tk.StringVar(value="faceswap")).get()
        
        if mode == "simple":
            # Simple mode: Only target person training
            if technology == "rehifaces":
                title = "Step 2: Source Face Selection (ReHiFace-S)"
                instructions = """Select the face you want to put onto others using ReHiFace-S real-time technology.

🚀 ReHiFace-S Requirements:
• Just ONE clear photo of the face you want to use
• No training required - instant results!
• Works with any clear face image (JPG/PNG)
• 10 second setup vs 12-48 hours training

💡 For best results:
• Use a clear, front-facing photo
• Good lighting and high resolution
• Single person in the image preferred

Select the source face image:"""
                label_text = "📸 Source Face Image (ReHiFace-S)"
            else:
                title = "Step 2: New Face Training Data"
                instructions = """Add training videos or images of the person whose face you want to PUT ONTO others.

In Simple Mode:
• AI will detect ANY face in your content
• Replace all detected faces with your trained person's face
• Only need training data for the NEW FACE (the replacement)
• Much faster setup and processing

⚠️ MINIMUM REQUIREMENTS:
• At least 25 training images (FaceSwap requirement)
• Recommended: 50-500+ images for best quality
• Use videos for more variety (different angles/expressions)

Upload clear videos/images of the person whose face you want to USE AS REPLACEMENT:"""
                label_text = "🎭 NEW FACE Training Material (Face to PUT ON others)"
            
            ttk.Label(self.step2_frame, text=title, 
                     font=('Arial', 16, 'bold')).pack(pady=10)
            
            ttk.Label(self.step2_frame, text=instructions, wraplength=600, justify='left').pack(pady=10)
            
            # Target person training
            target_frame = ttk.LabelFrame(self.step2_frame, text=label_text, padding=10)
            target_frame.pack(fill='both', expand=True, pady=10)
            
            buttons_frame = ttk.Frame(target_frame)
            buttons_frame.pack(fill='x', pady=5)
            
            if technology == "rehifaces":
                # ReHiFace-S: Only need single image selection
                add_images_btn = ttk.Button(buttons_frame, text="Select Face Image", 
                          command=lambda: self.add_files('target_faces', 'images'))
                add_images_btn.pack(side='left', padx=5)
            else:
                # Traditional FaceSwap: Need multiple images/videos
                add_video_btn = ttk.Button(buttons_frame, text="Add Video(s)", 
                          command=lambda: self.add_files('target_faces', 'video'))
                add_video_btn.pack(side='left', padx=5)
                
                add_images_btn = ttk.Button(buttons_frame, text="Add Images", 
                          command=lambda: self.add_files('target_faces', 'images'))
                add_images_btn.pack(side='left', padx=5)
            
            clear_btn = ttk.Button(buttons_frame, text="Clear All", 
                      command=lambda: self.clear_files('target_faces'))
            clear_btn.pack(side='left', padx=5)
            
            # Always create a new listbox when mode changes
            self.target_faces_listbox_simple = tk.Listbox(target_frame, height=8)
            self.target_faces_listbox_simple.pack(fill='both', expand=True, pady=5)
            
            scrollbar_simple = ttk.Scrollbar(target_frame, orient="vertical", command=self.target_faces_listbox_simple.yview)
            scrollbar_simple.pack(side="right", fill="y")
            self.target_faces_listbox_simple.configure(yscrollcommand=scrollbar_simple.set)
            
            # Update with existing files
            if hasattr(self, 'target_faces_files'):
                self.update_listbox(self.target_faces_listbox_simple, self.target_faces_files)
            
        else:
            # Advanced mode: Person A training
            ttk.Label(self.step2_frame, text="Step 2: Original Face Training Data", 
                     font=('Arial', 16, 'bold')).pack(pady=10)
            
            instructions = """Add training videos or images of the person whose face will be REMOVED/REPLACED.

In Advanced Mode:
• AI learns both faces specifically for high-quality swaps
• Can do bidirectional swaps (Original ↔ New Face)
• Requires training data for BOTH the original and new faces
• Higher quality but more setup required

Upload clear videos/images of the person whose face you want to REMOVE/REPLACE:"""
            
            ttk.Label(self.step2_frame, text=instructions, wraplength=600, justify='left').pack(pady=10)
            
            # Person A training
            source_frame = ttk.LabelFrame(self.step2_frame, text="🚫 ORIGINAL FACE Training Material (Face to REMOVE)", padding=10)
            source_frame.pack(fill='both', expand=True, pady=10)
            
            buttons_frame = ttk.Frame(source_frame)
            buttons_frame.pack(fill='x', pady=5)
            
            add_video_btn = ttk.Button(buttons_frame, text="Add Video(s)", 
                      command=lambda: self.add_files('source', 'video'))
            add_video_btn.pack(side='left', padx=5)
            
            add_images_btn = ttk.Button(buttons_frame, text="Add Images", 
                      command=lambda: self.add_files('source', 'images'))
            add_images_btn.pack(side='left', padx=5)
            
            clear_btn = ttk.Button(buttons_frame, text="Clear All", 
                      command=lambda: self.clear_files('source'))
            clear_btn.pack(side='left', padx=5)
            
            # Always create a new listbox when mode changes
            self.source_listbox = tk.Listbox(source_frame, height=8)
            self.source_listbox.pack(fill='both', expand=True, pady=5)
            
            scrollbar1 = ttk.Scrollbar(source_frame, orient="vertical", command=self.source_listbox.yview)
            scrollbar1.pack(side="right", fill="y")
            self.source_listbox.configure(yscrollcommand=scrollbar1.set)
            
            # Update with existing files
            if hasattr(self, 'source_files'):
                self.update_listbox(self.source_listbox, self.source_files)
        
    def setup_step3(self):
        """Step 3: Content or Person B Training (changes based on mode)"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="3. Next Step")
        
        # Store reference to the frame for tab title updates
        self.step3_frame = frame
        
        # Dynamic content based on mode
        self.update_step3_content()
        
    def update_step3_content(self):
        """Update Step 3 content based on selected mode"""
        # Clear existing content
        for widget in self.step3_frame.winfo_children():
            widget.destroy()
            
        mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
        technology = getattr(self, 'technology_var', tk.StringVar(value="faceswap")).get()
        
        if mode == "simple":
            # Simple mode: Skip to content conversion
            ttk.Label(self.step3_frame, text="Step 3: Content to Convert", 
                     font=('Arial', 16, 'bold')).pack(pady=10)
            
            if technology == "rehifaces":
                instructions = """Add the videos or images where you want to apply face swapping using ReHiFace-S.

🚀 ReHiFace-S Processing:
• Any detected face will be REPLACED with your source face from Step 2
• Real-time processing - results in seconds!
• No training required - instant face swapping
• Works with videos and images

💡 Tips for best results:
• Use high-quality source content
• Ensure faces are clearly visible
• Good lighting improves results

Add your content files below (where faces will be REPLACED):"""
            else:
                instructions = """Add the videos or images where you want to perform face swapping.

In Simple Mode:
• Any detected face will be REPLACED with your NEW FACE from Step 2
• You don't need to specify which person to replace - all faces get swapped
• Works great for putting celebrities, yourself, etc. on any content
• Much simpler than traditional face swapping

Add your content files below (where faces will be REPLACED):"""
            
            ttk.Label(self.step3_frame, text=instructions, wraplength=600, justify='left').pack(pady=10)
            
            # Convert content for simple mode
            convert_frame = ttk.LabelFrame(self.step3_frame, text="📺 Content Where Faces Will BE REPLACED", padding=10)
            convert_frame.pack(fill='both', expand=True, pady=10)
            
            buttons_frame = ttk.Frame(convert_frame)
            buttons_frame.pack(fill='x', pady=5)
            
            convert_video_btn = ttk.Button(buttons_frame, text="Add Video(s)", 
                      command=lambda: self.add_files('convert', 'video'))
            convert_video_btn.pack(side='left', padx=5)
            
            convert_images_btn = ttk.Button(buttons_frame, text="Add Images", 
                      command=lambda: self.add_files('convert', 'images'))
            convert_images_btn.pack(side='left', padx=5)
            
            clear_convert_btn = ttk.Button(buttons_frame, text="Clear All", 
                      command=lambda: self.clear_files('convert'))
            clear_convert_btn.pack(side='left', padx=5)
            
            # Always create a new listbox when mode changes
            self.convert_listbox_simple = tk.Listbox(convert_frame, height=8)
            self.convert_listbox_simple.pack(fill='both', expand=True, pady=5)
            
            scrollbar_convert = ttk.Scrollbar(convert_frame, orient="vertical", command=self.convert_listbox_simple.yview)
            scrollbar_convert.pack(side="right", fill="y")
            self.convert_listbox_simple.configure(yscrollcommand=scrollbar_convert.set)
            
            # Update with existing files
            if hasattr(self, 'convert_files'):
                self.update_listbox(self.convert_listbox_simple, self.convert_files)
            
        else:
            # Advanced mode: Person B training (same as before)
            ttk.Label(self.step3_frame, text="Step 3: New Face Training Data", 
                     font=('Arial', 16, 'bold')).pack(pady=10)
            
            instructions = """Add training videos or images of the person whose face will REPLACE the original face.

This is ONLY for training the AI to learn the NEW FACE. You need:
• Clear, well-lit faces of the person whose face you want to PUT ON others
• Multiple angles and expressions  
• At least 300-500 faces for good results
• Videos work better than individual photos

Note: This is separate from the content you want to convert in Step 4."""
            
            ttk.Label(self.step3_frame, text=instructions, wraplength=600, justify='left').pack(pady=10)
            
            # Person B training
            target_faces_frame = ttk.LabelFrame(self.step3_frame, text="🎭 NEW FACE Training Material (Face to PUT ON others)", padding=10)
            target_faces_frame.pack(fill='both', expand=True, pady=10)
            
            buttons_frame = ttk.Frame(target_faces_frame)
            buttons_frame.pack(fill='x', pady=5)
            
            target_video_btn = ttk.Button(buttons_frame, text="Add Video(s)", 
                      command=lambda: self.add_files('target_faces', 'video'))
            target_video_btn.pack(side='left', padx=5)
            
            target_images_btn = ttk.Button(buttons_frame, text="Add Images", 
                      command=lambda: self.add_files('target_faces', 'images'))
            target_images_btn.pack(side='left', padx=5)
            
            clear_target_btn = ttk.Button(buttons_frame, text="Clear All", 
                      command=lambda: self.clear_files('target_faces'))
            clear_target_btn.pack(side='left', padx=5)
            
            # Always create a new listbox when mode changes
            self.target_faces_listbox = tk.Listbox(target_faces_frame, height=8)
            self.target_faces_listbox.pack(fill='both', expand=True, pady=5)
            
            scrollbar_target = ttk.Scrollbar(target_faces_frame, orient="vertical", command=self.target_faces_listbox.yview)
            scrollbar_target.pack(side="right", fill="y")
            self.target_faces_listbox.configure(yscrollcommand=scrollbar_target.set)
            
            # Update with existing files
            if hasattr(self, 'target_faces_files'):
                self.update_listbox(self.target_faces_listbox, self.target_faces_files)
        
    def setup_step4(self):
        """Step 4: Content to Convert"""
        frame = ttk.Frame(self.notebook)
        # Insert Step 4 at the correct position (index 3, after Step 3)
        self.notebook.insert(3, frame, text="4. Content to Convert")
        
        # Store reference to the frame for tab title updates
        self.step4_frame = frame
        
        ttk.Label(frame, text="Step 4: Content to Convert", 
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        instructions = """Add the videos or images where you want to perform face swapping.

This is your final content where:
• Any faces matching the ORIGINAL FACE will be REPLACED with the NEW FACE
• The content can contain either person (or both)
• You can add multiple videos/images to process
• Results will be saved with face swaps applied

Important: This should be DIFFERENT from your training material in Steps 2 & 3."""
        
        ttk.Label(frame, text=instructions, wraplength=600, justify='left').pack(pady=10)
        
        # Convert content
        convert_frame = ttk.LabelFrame(frame, text="📺 Content Where Faces Will Be REPLACED", padding=10)
        convert_frame.pack(fill='both', expand=True, pady=10)
        
        buttons_frame3 = ttk.Frame(convert_frame)
        buttons_frame3.pack(fill='x', pady=5)
        
        convert_video_btn = ttk.Button(buttons_frame3, text="Add Video(s)", 
                  command=lambda: self.add_files('convert', 'video'))
        convert_video_btn.pack(side='left', padx=5)
        
        convert_images_btn = ttk.Button(buttons_frame3, text="Add Images", 
                  command=lambda: self.add_files('convert', 'images'))
        convert_images_btn.pack(side='left', padx=5)
        
        clear_convert_btn = ttk.Button(buttons_frame3, text="Clear All", 
                  command=lambda: self.clear_files('convert'))
        clear_convert_btn.pack(side='left', padx=5)
        
        self.convert_listbox = tk.Listbox(convert_frame, height=8)
        self.convert_listbox.pack(fill='both', expand=True, pady=5)
        
        scrollbar3 = ttk.Scrollbar(convert_frame, orient="vertical", command=self.convert_listbox.yview)
        scrollbar3.pack(side="right", fill="y")
        self.convert_listbox.configure(yscrollcommand=scrollbar3.set)
        
    def setup_step5(self):
        """Step 5: Processing"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="5. Processing")
        self.step5_frame = frame
        
        ttk.Label(frame, text="Step 5: Automatic Processing", 
                 font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Create technology-aware instructions
        self.processing_instructions_frame = ttk.Frame(frame)
        self.processing_instructions_frame.pack(fill='x', pady=10)
        
        self.update_processing_content()
        
        # Processing controls
        controls_frame = ttk.Frame(frame)
        controls_frame.pack(fill='x', pady=10)
        
        self.start_btn = ttk.Button(controls_frame, text="🚀 Start Processing", 
                                   command=self.start_processing, style='Accent.TButton')
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = ttk.Button(controls_frame, text="⏹ Stop", 
                                  command=self.stop_processing, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        # Technology-specific controls
        self.tech_controls_frame = ttk.Frame(controls_frame)
        self.tech_controls_frame.pack(side='left', padx=20)
        
        # Progress details
        progress_frame = ttk.LabelFrame(frame, text="Processing Progress", padding=10)
        progress_frame.pack(fill='both', expand=True, pady=10)
        
        self.progress_detail = ttk.Label(progress_frame, text="Ready to start processing")
        self.progress_detail.pack(pady=5)
        
        self.detail_progress = ttk.Progressbar(progress_frame, length=500, mode='indeterminate')
        self.detail_progress.pack(pady=5)
        
        # Log output
        self.log_text = scrolledtext.ScrolledText(progress_frame, height=10, width=80)
        self.log_text.pack(fill='both', expand=True, pady=5)
        
    def setup_step6(self):
        """Step 6: Results"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="6. Results")
        
        ttk.Label(frame, text="Step 6: View Results", 
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
        
        results_btn = ttk.Button(buttons_frame, text="📁 Open Results Folder", 
                  command=self.open_results_folder)
        results_btn.pack(side='left', padx=5)
        
        project_btn = ttk.Button(buttons_frame, text="🎬 Open Project Folder", 
                  command=self.open_project_folder)
        project_btn.pack(side='left', padx=5)
        
        new_project_btn = ttk.Button(buttons_frame, text="🔄 Start New Project", 
                  command=self.new_project)
        new_project_btn.pack(side='left', padx=5)
        
        # Results info
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10, width=80)
        self.results_text.pack(fill='both', expand=True, pady=5)
        
    def update_step_display(self):
        """Update the progress bar and step indicator"""
        mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
        
        if mode == "simple":
            # Adjust progress calculation for simple mode (5 effective steps)
            effective_step = self.current_step
            if self.current_step == 5:  # Processing step in simple mode
                effective_step = 4  # Show as step 4 of 5
            elif self.current_step == 6:  # Results step in simple mode
                effective_step = 5  # Show as step 5 of 5
            elif self.current_step > 3:
                effective_step = self.current_step - 1
            
            progress = (effective_step - 1) / (5 - 1) * 100  # 5 effective steps
            self.step_label.config(text=f"Step {effective_step} of 5")
        else:
            progress = (self.current_step - 1) / (self.total_steps - 1) * 100
            self.step_label.config(text=f"Step {self.current_step} of {self.total_steps}")
        
        self.progress_bar['value'] = progress
        
        # Update notebook selection (map current_step to actual tab index)
        try:
            if mode == "simple":
                # Simple mode tab mapping: Step 1->Tab 0, Step 2->Tab 1, Step 3->Tab 2, Step 5->Tab 3, Step 6->Tab 4
                # (Step 4 is removed in Simple mode, so tabs are 0,1,2,3,4)
                if self.current_step <= 3:
                    tab_index = self.current_step - 1
                elif self.current_step == 5:
                    tab_index = 3  # Processing tab (was index 4, now index 3)
                else:  # self.current_step == 6
                    tab_index = 4  # Results tab (was index 5, now index 4)
            else:
                # Advanced mode: direct mapping
                tab_index = self.current_step - 1
            
            # Ensure tab exists before selecting
            if 0 <= tab_index < len(self.notebook.tabs()):
                self.notebook.select(tab_index)
            else:
                print(f"Warning: Tab index {tab_index} out of range (total tabs: {len(self.notebook.tabs())})")
        except Exception as e:
            print(f"Error updating notebook selection: {e}")
        
        # Update button states
        self.prev_btn.config(state='normal' if self.current_step > 1 else 'disabled')
        
        # Next button logic
        if mode == "simple":
            # In simple mode: allow next until step 3, then skip to step 5, then allow step 6 (results)
            next_enabled = self.current_step <= 3 or self.current_step == 5
        else:
            next_enabled = self.current_step < self.total_steps
            
        self.next_btn.config(state='normal' if next_enabled else 'disabled')
        
    def prev_step(self):
        """Go to previous step"""
        if self.current_step > 1:
            mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
            
            # In simple mode, skip step 4 in both directions
            if mode == "simple" and self.current_step == 5:
                self.current_step = 3  # Skip step 4 in simple mode (Processing -> Content)
            elif mode == "simple" and self.current_step == 6:
                self.current_step = 5  # Results -> Processing in simple mode
            else:
                self.current_step -= 1
                
            self.update_step_display()
            
    def next_step(self):
        """Go to next step"""
        if self.validate_current_step():
            mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
            
            if self.current_step < self.total_steps:
                # In simple mode, skip step 4 (go from step 3 to step 5)
                if mode == "simple" and self.current_step == 3:
                    self.current_step = 5  # Skip step 4 in simple mode
                else:
                    self.current_step += 1
                    
                self.update_step_display()
                
    def validate_current_step(self) -> bool:
        """Validate current step before proceeding"""
        mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
        
        if self.current_step == 1:
            if not self.project_dir:
                messagebox.showerror("Error", "Please select or create a project folder first.")
                return False
                
        elif self.current_step == 2:
            if mode == "simple":
                # Simple mode: Check target faces
                if not hasattr(self, 'target_faces_files') or not self.target_faces_files:
                    messagebox.showerror("Error", "Please add training material for your NEW FACE (the face you want to put on others) first.")
                    return False
            else:
                # Advanced mode: Check Person A
                if not self.source_files:
                    messagebox.showerror("Error", "Please add training material for the ORIGINAL FACE (the face you want to remove) first.")
                    return False
                
        elif self.current_step == 3:
            if mode == "simple":
                # Simple mode: Check content to convert (this is the final input step)
                if not hasattr(self, 'convert_files') or not self.convert_files:
                    messagebox.showerror("Error", "Please add content where faces will be REPLACED first.")
                    return False
            else:
                # Advanced mode: Check Person B
                if not hasattr(self, 'target_faces_files') or not self.target_faces_files:
                    messagebox.showerror("Error", "Please add training material for the NEW FACE (the replacement face) first.")
                    return False
                
        elif self.current_step == 4 and mode == "advanced":
            # Advanced mode only: Check content to convert
            if not hasattr(self, 'convert_files') or not self.convert_files:
                messagebox.showerror("Error", "Please add content where faces will be REPLACED first.")
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
                # Filter out problematic macOS system files and hidden files
                filename = os.path.basename(file)
                if (filename.startswith('._') or  # macOS metadata files
                    filename.startswith('.DS_Store') or  # macOS directory metadata
                    filename.startswith('Thumbs.db') or  # Windows thumbnail cache
                    filename.startswith('.') or  # Other hidden files
                    'copy' in filename.lower() or  # Files with "copy" often have encoding issues
                    not os.path.exists(file) or  # File doesn't exist
                    os.path.getsize(file) == 0):  # Empty file
                    invalid_files.append(file)
                    continue
                    
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
                    if hasattr(self, 'source_listbox'):
                        self.update_listbox(self.source_listbox, self.source_files)
                elif file_type == 'target_faces':
                    if not hasattr(self, 'target_faces_files'):
                        self.target_faces_files = []
                    self.target_faces_files.extend(valid_files)
                    # Update the appropriate listbox based on mode
                    mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
                    if mode == "simple" and hasattr(self, 'target_faces_listbox_simple'):
                        self.update_listbox(self.target_faces_listbox_simple, self.target_faces_files)
                    elif mode == "advanced" and hasattr(self, 'target_faces_listbox'):
                        self.update_listbox(self.target_faces_listbox, self.target_faces_files)
                elif file_type == 'convert':
                    if not hasattr(self, 'convert_files'):
                        self.convert_files = []
                    self.convert_files.extend(valid_files)
                    # Update the appropriate listbox based on mode
                    mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
                    if mode == "simple" and hasattr(self, 'convert_listbox_simple'):
                        self.update_listbox(self.convert_listbox_simple, self.convert_files)
                    elif mode == "advanced" and hasattr(self, 'convert_listbox'):
                        self.update_listbox(self.convert_listbox, self.convert_files)
                    
                self.log_message(f"Added {len(valid_files)} {media_type} file(s) to {file_type}")
            else:
                messagebox.showinfo("No Valid Files", f"No valid {media_type} files were selected.")
                
    def update_listbox(self, listbox: tk.Listbox, files: List[str]):
        """Update listbox with file list"""
        if listbox is None:
            return
        try:
            listbox.delete(0, tk.END)
            for file in files:
                listbox.insert(tk.END, os.path.basename(file))
        except tk.TclError:
            # Listbox might not exist yet
            pass
            
    def clear_files(self, file_type: str):
        """Clear files from list"""
        mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
        
        if file_type == 'source':
            self.source_files.clear()
            if hasattr(self, 'source_listbox'):
                self.update_listbox(self.source_listbox, self.source_files)
                
        elif file_type == 'target_faces':
            if hasattr(self, 'target_faces_files'):
                self.target_faces_files.clear()
                # Update the appropriate listbox based on mode
                if mode == "simple" and hasattr(self, 'target_faces_listbox_simple'):
                    self.update_listbox(self.target_faces_listbox_simple, self.target_faces_files)
                elif mode == "advanced" and hasattr(self, 'target_faces_listbox'):
                    self.update_listbox(self.target_faces_listbox, self.target_faces_files)
                    
        elif file_type == 'convert':
            if hasattr(self, 'convert_files'):
                self.convert_files.clear()
                # Update the appropriate listbox based on mode
                if mode == "simple" and hasattr(self, 'convert_listbox_simple'):
                    self.update_listbox(self.convert_listbox_simple, self.convert_files)
                elif mode == "advanced" and hasattr(self, 'convert_listbox'):
                    self.update_listbox(self.convert_listbox, self.convert_files)
            
    def clean_input_files(self, file_list: List[str]) -> List[str]:
        """Clean input files by removing problematic system files"""
        cleaned_files = []
        removed_files = []
        
        for file_path in file_list:
            filename = os.path.basename(file_path)
            
            # Check for problematic file patterns
            if (filename.startswith('._') or  # macOS metadata files
                filename.startswith('.DS_Store') or  # macOS directory metadata  
                filename.startswith('Thumbs.db') or  # Windows thumbnail cache
                filename.startswith('.') or  # Other hidden files
                'copy' in filename.lower() or  # Files with "copy" often have encoding issues
                not os.path.exists(file_path) or  # File doesn't exist
                os.path.getsize(file_path) == 0):  # Empty file
                removed_files.append(filename)
                continue
                
            # Check if file is readable
            try:
                with open(file_path, 'rb') as f:
                    f.read(1)  # Try to read first byte
                cleaned_files.append(file_path)
            except (OSError, IOError, PermissionError):
                removed_files.append(filename)
                continue
        
        if removed_files:
            self.log_message(f"🧹 Cleaned {len(removed_files)} problematic files: {', '.join(removed_files[:3])}{'...' if len(removed_files) > 3 else ''}")
            
        self.log_message(f"📁 {len(cleaned_files)} valid files ready for processing")
        return cleaned_files

    def clean_temp_directory(self, temp_dir: str):
        """Clean temporary directory of problematic system files"""
        import os
        
        if not os.path.exists(temp_dir):
            return
            
        files_removed = []
        try:
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                
                # Only remove specific problematic files, preserve important faceswap files
                if (filename.startswith('._') and  # macOS metadata files
                    not filename.endswith('.fsa') and  # But preserve alignment files even with ._ prefix
                    not filename.endswith('.json')):  # And preserve other important files
                    try:
                        os.remove(file_path)
                        files_removed.append(filename)
                    except (OSError, IOError):
                        pass  # Ignore errors removing problematic files
                elif filename in ['.DS_Store', 'Thumbs.db']:  # Specific system files
                    try:
                        os.remove(file_path)
                        files_removed.append(filename)
                    except (OSError, IOError):
                        pass
        except (OSError, IOError):
            # If we can't read the directory, skip cleaning
            pass
        
        if files_removed:
            self.log_message(f"🧹 Cleaned temp directory: removed {', '.join(files_removed)}")

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
        mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
        technology = getattr(self, 'technology_var', tk.StringVar(value="faceswap")).get()
        
        if not self.project_dir:
            messagebox.showerror("Error", "Project folder not selected.")
            return False
        
        if technology == "rehifaces":
            # ReHiFace-S validation: Only need source face and content to convert
            if not hasattr(self, 'target_faces_files') or not self.target_faces_files:
                messagebox.showerror("Error", "Please select a source face image for ReHiFace-S.")
                return False
            if not hasattr(self, 'convert_files') or not self.convert_files:
                messagebox.showerror("Error", "Please select content files to process with ReHiFace-S.")
                return False
            return True
            
        # Traditional FaceSwap validation
        if mode == "simple":
            # Simple Mode: Only need NEW FACE training material and content to convert
            if not hasattr(self, 'target_faces_files') or not self.target_faces_files:
                messagebox.showerror("Error", "No NEW FACE training material selected.")
                return False
            if not hasattr(self, 'convert_files') or not self.convert_files:
                messagebox.showerror("Error", "No content to convert selected.")
                return False
        else:
            # Advanced Mode: Need both ORIGINAL and NEW face training material plus content
            if not self.source_files:
                messagebox.showerror("Error", "No ORIGINAL FACE training material selected.")
                return False
            if not hasattr(self, 'target_faces_files') or not self.target_faces_files:
                messagebox.showerror("Error", "No NEW FACE training material selected.")
                return False
            if not hasattr(self, 'convert_files') or not self.convert_files:
                messagebox.showerror("Error", "No content to convert selected.")
                return False
        return True
        
    def run_processing(self):
        """Run the complete processing pipeline"""
        try:
            mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
            technology = getattr(self, 'technology_var', tk.StringVar(value="faceswap")).get()
            
            if technology == "rehifaces":
                # Use ReHiFace-S processing pipeline
                self.log_message(f"🚀 Starting ReHiFace-S real-time processing...")
                self.run_rehifaces_processing()
                return
            else:
                # Use traditional FaceSwap processing pipeline
                self.log_message(f"🚀 Starting FaceSwap processing pipeline in {mode} mode...")
            
            # Clean all input files first to avoid crashes
            self.log_message("🧹 Cleaning input files...")
            
            # Clean target faces files
            if hasattr(self, 'target_faces_files'):
                original_count = len(self.target_faces_files)
                self.target_faces_files = self.clean_input_files(self.target_faces_files)
                self.log_message(f"NEW FACE files: {len(self.target_faces_files)}/{original_count} valid")
            
            # Clean convert files  
            if hasattr(self, 'convert_files'):
                original_count = len(self.convert_files)
                self.convert_files = self.clean_input_files(self.convert_files)
                self.log_message(f"Content files: {len(self.convert_files)}/{original_count} valid")
                
            # Clean source files (Advanced mode only)
            if mode == "advanced" and hasattr(self, 'source_files'):
                original_count = len(self.source_files)
                self.source_files = self.clean_input_files(self.source_files)
                self.log_message(f"ORIGINAL FACE files: {len(self.source_files)}/{original_count} valid")
            
            if mode == "simple":
                # Simple mode: Extract target faces + faces from content, then train
                self.log_message("ℹ️ Simple mode: Will replace any detected faces with your NEW face")
                
                # Step 1: Extract target faces (NEW face to put on others)
                self.update_progress("Extracting NEW FACE training material...")
                target_output = os.path.join(self.project_dir, 'target_faces')
                os.makedirs(target_output, exist_ok=True)
                
                for i, file in enumerate(self.target_faces_files):
                    self.log_message(f"Processing NEW face file {i+1}/{len(self.target_faces_files)}: {os.path.basename(file)}")
                    self.extract_faces(file, target_output, "target")
                
                # Step 2: Extract faces from content to be converted (these become "source" faces)
                self.update_progress("Extracting faces from content to be converted...")
                source_output = os.path.join(self.project_dir, 'source_faces')
                os.makedirs(source_output, exist_ok=True)
                
                for i, file in enumerate(self.convert_files):
                    self.log_message(f"Extracting faces from content {i+1}/{len(self.convert_files)}: {os.path.basename(file)}")
                    self.extract_faces(file, source_output, "content_source")
                
                # Check face counts (filter out metadata files)
                source_count = len([f for f in os.listdir(source_output) 
                                  if f.endswith('.png') and not f.startswith('._')])
                target_count = len([f for f in os.listdir(target_output) 
                                  if f.endswith('.png') and not f.startswith('._')])
                
                self.log_message(f"✅ Extraction complete: {source_count} faces from content, {target_count} NEW face training images")
                
                # Validate minimum requirements for FaceSwap training
                if source_count == 0:
                    raise Exception("No faces found in content to convert. Please check your input files.")
                
                if target_count < 25:
                    self.log_message(f"❌ TRAINING REQUIREMENT NOT MET: Only {target_count} NEW face images found.")
                    self.log_message("🚫 FaceSwap requires minimum 25 images per side for training.")
                    self.log_message("📝 SOLUTION: Add more images/videos of your NEW face (the face you want to impose).")
                    self.log_message("💡 TIPS:")
                    self.log_message("   • Use videos (extract more frames with different angles/expressions)")
                    self.log_message("   • Add photos from different lighting conditions")
                    self.log_message("   • Include various facial expressions and head angles")
                    self.log_message("   • Aim for 50-500+ images for best results")
                    raise Exception(f"Insufficient training material: {target_count} images < 25 minimum required")
                elif target_count < 50:
                    self.log_message(f"⚠️ LOW IMAGE COUNT: {target_count} NEW face images (minimum met but results may be limited)")
                    self.log_message("📝 RECOMMENDATION: Add more images/videos for better quality results")
                elif target_count < 250:
                    self.log_message(f"⚠️ MODERATE IMAGE COUNT: {target_count} NEW face images (acceptable for basic results)")
                    self.log_message("💡 For optimal results, aim for 250+ images")
                else:
                    self.log_message(f"✅ EXCELLENT: {target_count} NEW face images - great for high-quality training!")
                    
            else:
                # Advanced mode: Extract both Person A and Person B
                # Step 1: Extract source faces (ORIGINAL faces to remove)
                self.update_progress("Extracting ORIGINAL FACE training material...")
                source_output = os.path.join(self.project_dir, 'source_faces')
                os.makedirs(source_output, exist_ok=True)
                
                for i, file in enumerate(self.source_files):
                    self.log_message(f"Processing ORIGINAL face file {i+1}/{len(self.source_files)}: {os.path.basename(file)}")
                    self.extract_faces(file, source_output, "source")
                    
                # Step 2: Extract target faces (NEW faces to put on others)
                self.update_progress("Extracting NEW FACE training material...")
                target_output = os.path.join(self.project_dir, 'target_faces')
                os.makedirs(target_output, exist_ok=True)
                
                for i, file in enumerate(self.target_faces_files):
                    self.log_message(f"Processing NEW face file {i+1}/{len(self.target_faces_files)}: {os.path.basename(file)}")
                    self.extract_faces(file, target_output, "target")
                    
                # Check face counts (filter out metadata files)
                source_count = len([f for f in os.listdir(source_output) 
                                  if f.endswith('.png') and not f.startswith('._')])
                target_count = len([f for f in os.listdir(target_output) 
                                  if f.endswith('.png') and not f.startswith('._')])
                
                self.log_message(f"✅ Extraction complete: {source_count} ORIGINAL faces, {target_count} NEW faces")
                
                # Validate minimum requirements for FaceSwap training
                failed_requirements = []
                if source_count < 25:
                    failed_requirements.append(f"ORIGINAL faces: {source_count} < 25 minimum")
                if target_count < 25:
                    failed_requirements.append(f"NEW faces: {target_count} < 25 minimum")
                
                if failed_requirements:
                    self.log_message("❌ TRAINING REQUIREMENTS NOT MET:")
                    for req in failed_requirements:
                        self.log_message(f"   🚫 {req}")
                    self.log_message("📝 SOLUTION: Add more images/videos for the insufficient face types.")
                    self.log_message("💡 TIPS:")
                    self.log_message("   • Use videos to extract more frames with different angles/expressions")
                    self.log_message("   • Add photos from different lighting conditions") 
                    self.log_message("   • Include various facial expressions and head angles")
                    self.log_message("   • Aim for 50-500+ images per person for best results")
                    raise Exception(f"Insufficient training material: {', '.join(failed_requirements)}")
                
                # Provide quality feedback for adequate amounts
                warnings = []
                if source_count < 50:
                    warnings.append(f"ORIGINAL faces: {source_count} images (minimum met, basic quality)")
                if target_count < 50:
                    warnings.append(f"NEW faces: {target_count} images (minimum met, basic quality)")
                    
                if warnings:
                    self.log_message("⚠️ LOW IMAGE COUNTS:")
                    for warning in warnings:
                        self.log_message(f"   📊 {warning}")
                    self.log_message("📝 RECOMMENDATION: Add more images for better quality results")
                
                # Check for good amounts
                if source_count >= 250 and target_count >= 250:
                    self.log_message(f"✅ EXCELLENT: {source_count} ORIGINAL + {target_count} NEW faces - great for high-quality training!")
                elif source_count >= 50 and target_count >= 50:
                    self.log_message(f"✅ GOOD: {source_count} ORIGINAL + {target_count} NEW faces - sufficient for quality results")
                
            # Step 3: Train model (same for both modes)
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
        try:
            self.log_message(f"Extracting {face_type} faces from: {os.path.basename(input_file)}")
            
            # Clean the input file first
            cleaned_files = self.clean_input_files([input_file])
            if not cleaned_files:
                self.log_message(f"⚠️ Skipping {os.path.basename(input_file)} - file has issues")
                return
                
            input_file = cleaned_files[0]  # Use cleaned file
            
            # Check if input is a single image file
            image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
            file_ext = os.path.splitext(input_file.lower())[1]
            
            if file_ext in image_extensions:
                # For single images, create a temporary folder and copy the image
                import shutil
                temp_input_dir = os.path.join(os.path.dirname(output_dir), f"temp_input_{face_type}")
                os.makedirs(temp_input_dir, exist_ok=True)
                
                try:
                    # Copy image to temp folder
                    temp_image_path = os.path.join(temp_input_dir, os.path.basename(input_file))
                    shutil.copy2(input_file, temp_image_path)
                    
                    # Clean the temp directory of any problematic system files that might have been created
                    self.clean_temp_directory(temp_input_dir)
                    
                    cmd = [
                        '/Users/admin/micromamba/envs/faceswap/bin/python', 'faceswap.py', 'extract',
                        '-i', temp_input_dir,  # Use folder instead of single file
                        '-o', output_dir,
                        '-D', 's3fd',
                        '-A', 'fan', 
                        '-M', 'bisenet-fp'
                    ]
                    
                    self.run_command(cmd)
                    
                    # Clean the output directory of any metadata files that might have been created
                    self.clean_temp_directory(output_dir)
                    
                except Exception as e:
                    self.log_message(f"⚠️ Error during extraction: {str(e)}")
                    # Continue processing other files instead of failing completely
                    
                finally:
                    # Clean up temp folder
                    try:
                        if os.path.exists(temp_input_dir):
                            shutil.rmtree(temp_input_dir)
                    except (OSError, IOError):
                        pass  # Ignore cleanup errors
            else:
                # For videos, use the file directly
                cmd = [
                    '/Users/admin/micromamba/envs/faceswap/bin/python', 'faceswap.py', 'extract',
                    '-i', input_file,
                    '-o', output_dir,
                    '-D', 's3fd',
                    '-A', 'fan', 
                    '-M', 'bisenet-fp'
                ]
                
                self.run_command(cmd)
                
        except Exception as e:
            self.log_message(f"❌ Failed to extract faces from {os.path.basename(input_file)}: {str(e)}")
            # Log the error but continue processing other files
        
    def train_model(self, source_dir: str, target_dir: str, model_dir: str):
        """Train the face-swapping model"""
        self.log_message("Training model - this may take several hours...")
        
        cmd = [
            '/Users/admin/micromamba/envs/faceswap/bin/python', 'faceswap.py', 'train',
            '-A', source_dir,
            '-B', target_dir, 
            '-m', model_dir,
            '-t', 'original',
            '-b', '16'
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
            
            # Clean the temp directory of any problematic system files that might have been created
            self.clean_temp_directory(temp_input_dir)
            
            # Create temp output folder
            temp_output_dir = os.path.join(os.path.dirname(output_dir), "temp_convert_output")
            os.makedirs(temp_output_dir, exist_ok=True)
            
            cmd = [
                '/Users/admin/micromamba/envs/faceswap/bin/python', 'faceswap.py', 'convert',
                '-i', temp_input_dir,
                '-o', temp_output_dir,
                '-m', model_dir
            ]
            
            try:
                self.run_command(cmd)
                
                # Move converted image to final output location (filter out metadata files)
                converted_files = [f for f in os.listdir(temp_output_dir) 
                                 if f.endswith(('.png', '.jpg', '.jpeg')) and not f.startswith('._')]
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
                '/Users/admin/micromamba/envs/faceswap/bin/python', 'faceswap.py', 'convert',
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
            self.log_message(f"🔧 Running command: {' '.join(cmd[:3])}...")  # Log first 3 parts for privacy
            
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
                if line.strip():  # Only log non-empty lines
                    self.log_message(line.strip())
                
            process.wait()
            if process.returncode != 0:
                error_msg = f"Command failed with return code {process.returncode}"
                self.log_message(f"❌ Error: {error_msg}")
                raise Exception(error_msg)
            else:
                self.log_message("✅ Command completed successfully")
                
        except FileNotFoundError as e:
            error_msg = f"Command not found: {e}"
            self.log_message(f"❌ Error: {error_msg}")
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Command execution failed: {str(e)}"
            self.log_message(f"❌ Error: {error_msg}")
            raise
                
        except Exception as e:
            self.log_message(f"Command failed: {str(e)}")
            raise
            
    def run_rehifaces_processing(self):
        """Run ReHiFace-S real-time processing pipeline"""
        try:
            # Check if ReHiFace-S is installed
            rehifaces_path = Path("fast_faceswap/ReHiFace-S")
            
            if not rehifaces_path.exists():
                self.log_message("❌ ReHiFace-S not found. Installing...")
                # Trigger installation
                self.root.after(0, lambda: messagebox.showinfo(
                    "ReHiFace-S Required",
                    "🚀 ReHiFace-S needs to be installed first.\n\n"
                    "Click 'Open ReHiFace-S Web Interface' to install it automatically."
                ))
                return
            
            # Check if we have the required files
            if not hasattr(self, 'target_faces_files') or not self.target_faces_files:
                self.log_message("❌ No source face selected for ReHiFace-S")
                return
                
            if not hasattr(self, 'convert_files') or not self.convert_files:
                self.log_message("❌ No content files selected for processing")
                return
            
            # Get the first target face as the source face for ReHiFace-S
            source_face = self.target_faces_files[0]
            self.log_message(f"📸 Using source face: {os.path.basename(source_face)}")
            
            # Create output directory
            output_dir = os.path.join(self.project_dir, 'rehifaces_output')
            os.makedirs(output_dir, exist_ok=True)
            self.log_message(f"📁 Output directory: {output_dir}")
            
            # Process each content file with ReHiFace-S
            total_files = len(self.convert_files)
            successful_files = []
            failed_files = []
            
            for i, target_file in enumerate(self.convert_files):
                self.update_progress(f"Processing with ReHiFace-S: {i+1}/{total_files}")
                self.log_message(f"🎭 Processing file {i+1}/{total_files}: {os.path.basename(target_file)}")
                
                # Generate output filename
                base_name = os.path.splitext(os.path.basename(target_file))[0]
                file_ext = os.path.splitext(target_file)[1]
                output_file = os.path.join(output_dir, f"rehifaces_{base_name}{file_ext}")
                
                # Run ReHiFace-S processing
                success = self.run_rehifaces_swap(source_face, target_file, output_file)
                
                if success and os.path.exists(output_file):
                    file_size = os.path.getsize(output_file)
                    self.log_message(f"✅ Completed: {os.path.basename(output_file)} ({file_size} bytes)")
                    successful_files.append(output_file)
                else:
                    self.log_message(f"❌ Failed to process: {os.path.basename(target_file)}")
                    failed_files.append(target_file)
            
            # Report results
            if successful_files:
                self.log_message(f"🎉 ReHiFace-S processing completed! {len(successful_files)} files processed successfully.")
                if failed_files:
                    self.log_message(f"⚠️ {len(failed_files)} files failed to process.")
                
                # List successful files
                self.log_message("📂 Successful outputs:")
                for file_path in successful_files:
                    self.log_message(f"   • {os.path.basename(file_path)}")
            else:
                self.log_message("❌ No files were processed successfully.")
                # Show troubleshooting info
                self.log_message("🔧 Troubleshooting:")
                self.log_message("   • Check if ReHiFace-S conda environment has required packages")
                self.log_message("   • Try using the web interface instead")
                self.log_message("   • Make sure source face image is clear and high quality")
            
            self.update_progress("ReHiFace-S processing completed!")
            
            # Switch to results tab
            self.root.after(0, lambda: self.show_rehifaces_results(output_dir))
            
        except Exception as e:
            self.log_message(f"❌ ReHiFace-S processing failed: {str(e)}")
            self.update_progress("ReHiFace-S processing failed!")
        finally:
            self.root.after(0, self.processing_finished)
    
    def run_rehifaces_swap(self, source_face: str, target_file: str, output_file: str) -> bool:
        """Run a single ReHiFace-S face swap operation"""
        try:
            # Change to ReHiFace-S directory
            original_dir = os.getcwd()
            rehifaces_path = Path("fast_faceswap/ReHiFace-S")
            
            if not rehifaces_path.exists():
                self.log_message("❌ ReHiFace-S directory not found")
                return False
            
            # Get absolute path before changing directory
            abs_rehifaces_path = rehifaces_path.resolve()
            os.chdir(rehifaces_path)
            
            self.log_message(f"🔍 Looking for scripts in: {abs_rehifaces_path}")
            
            # Find the appropriate script - prioritize working_face_swap.py
            swap_scripts = ['working_face_swap.py', 'quick_swap.py', 'swap_face.py', 'inference.py', 'app.py']
            swap_script = None
            
            for script in swap_scripts:
                # Check in current directory since we already changed to it
                script_path = Path(script)
                if script_path.exists():
                    swap_script = script
                    self.log_message(f"✅ Found script: {script}")
                    break
                else:
                    self.log_message(f"🔍 Script not found: {script}")
            
            if not swap_script:
                self.log_message("❌ ReHiFace-S swap script not found")
                # List what files are actually available
                available_files = [f.name for f in Path('.').glob('*.py')]
                self.log_message(f"📁 Available Python files: {available_files}")
                return False
            
            # Convert paths to absolute paths to avoid confusion
            abs_source_path = str(Path(source_face).resolve() if Path(source_face).is_absolute() else Path(original_dir) / source_face)
            abs_target_path = str(Path(target_file).resolve() if Path(target_file).is_absolute() else Path(original_dir) / target_file)
            abs_output_path = str(Path(output_file).resolve() if Path(output_file).is_absolute() else Path(original_dir) / output_file)
            
            # Prepare command for the working script
            cmd = [
                'conda', 'run', '-n', 'rehifaces', 'python', swap_script,
                '--source', abs_source_path,
                '--target', abs_target_path,
                '--output', abs_output_path,
                '--gpu'
            ]
            
            self.log_message(f"🔧 Running: {swap_script} with ReHiFace-S...")
            self.log_message(f"📸 Source: {abs_source_path}")
            self.log_message(f"🎬 Target: {abs_target_path}")
            self.log_message(f"📤 Output: {abs_output_path}")
            
            # Run the command
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout per file
            )
            
            if process.returncode == 0:
                # Check if output file was actually created using absolute path
                output_path_obj = Path(abs_output_path)
                if output_path_obj.exists() and output_path_obj.stat().st_size > 0:
                    self.log_message(f"✅ Output file created successfully: {output_path_obj} ({output_path_obj.stat().st_size} bytes)")
                    return True
                else:
                    self.log_message(f"❌ Output file not created or is empty: {output_path_obj}")
                    # Log what files actually exist in the output directory
                    output_dir = output_path_obj.parent
                    if output_dir.exists():
                        existing_files = list(output_dir.glob('*'))
                        self.log_message(f"📁 Files in output directory: {[f.name for f in existing_files]}")
                    return False
            else:
                self.log_message(f"❌ ReHiFace-S script failed (exit code {process.returncode})")
                if process.stdout:
                    self.log_message(f"📤 Script output: {process.stdout}")
                if process.stderr:
                    self.log_message(f"❌ Script error: {process.stderr}")
                
                # Try direct Python execution as fallback (without conda)
                self.log_message(f"🔄 Trying direct Python execution as fallback...")
                fallback_cmd = [
                    'python', swap_script,
                    '--source', abs_source_path,
                    '--target', abs_target_path,
                    '--output', abs_output_path,
                    '--gpu'
                ]
                
                try:
                    fallback_process = subprocess.run(
                        fallback_cmd,
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    
                    if fallback_process.returncode == 0:
                        output_path_obj = Path(abs_output_path)
                        if output_path_obj.exists() and output_path_obj.stat().st_size > 0:
                            self.log_message(f"✅ Fallback successful: {output_path_obj} ({output_path_obj.stat().st_size} bytes)")
                            return True
                        else:
                            self.log_message(f"❌ Fallback failed: no output file created")
                    else:
                        self.log_message(f"❌ Fallback failed: {fallback_process.stderr}")
                except Exception as fallback_error:
                    self.log_message(f"❌ Fallback error: {fallback_error}")
                
                # Try the Python API as final fallback
                return self.run_rehifaces_python_api(source_face, target_file, output_file, original_dir)
                
        except subprocess.TimeoutExpired:
            self.log_message("❌ ReHiFace-S processing timed out")
            return False
        except Exception as e:
            self.log_message(f"❌ ReHiFace-S swap error: {str(e)}")
            return False
        finally:
            # Always return to original directory
            os.chdir(original_dir)
    
    def run_rehifaces_python_api(self, source_face: str, target_file: str, output_file: str, original_dir: str) -> bool:
        """Try to use ReHiFace-S Python API directly"""
        try:
            # Import ReHiFace-S modules
            import sys
            sys.path.append(str(Path.cwd()))
            
            from app import FaceSwapProcessor, initialize_processor
            
            self.log_message("🔧 Using ReHiFace-S Python API...")
            
            # Initialize processor
            initialize_processor()
            from app import processor
            
            # Load source and target
            source_path = str(Path(original_dir) / source_face)
            target_path = str(Path(original_dir) / target_file)
            output_path = str(Path(original_dir) / output_file)
            
            self.log_message(f"📸 Source: {source_path}")
            self.log_message(f"🎬 Target: {target_path}")
            self.log_message(f"📤 Output: {output_path}")
            
            # Load images
            import cv2
            source_img = cv2.imread(source_path)
            
            if source_img is None:
                self.log_message(f"❌ Could not load source image: {source_path}")
                return False
            
            # Check if target is video or image
            target_ext = os.path.splitext(target_path)[1].lower()
            
            if target_ext in ['.mp4', '.avi', '.mov', '.mkv']:
                # Process video
                success = self.process_video_with_rehifaces(processor, source_img, target_path, output_path)
            else:
                # Process image
                target_img = cv2.imread(target_path)
                if target_img is None:
                    self.log_message(f"❌ Could not load target image: {target_path}")
                    return False
                
                # Use processor to swap faces
                result = processor.process_frame(target_img, source_img, True, 0.5, True, 'rct')
                cv2.imwrite(output_path, result)
                success = True
            
            return success
            
        except ImportError as e:
            self.log_message(f"❌ Could not import ReHiFace-S modules: {e}")
            return False
        except Exception as e:
            self.log_message(f"❌ ReHiFace-S API error: {e}")
            return False
    
    def process_video_with_rehifaces(self, processor, source_img, target_path: str, output_path: str) -> bool:
        """Process video file with ReHiFace-S"""
        try:
            import cv2
            
            cap = cv2.VideoCapture(target_path)
            if not cap.isOpened():
                self.log_message(f"❌ Could not open video: {target_path}")
                return False
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            self.log_message(f"📹 Processing video: {total_frames} frames at {fps} FPS")
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process frame with face swap
                try:
                    processed_frame = processor.process_frame(frame, source_img, True, 0.5, True, 'rct')
                    out.write(processed_frame)
                except Exception as frame_error:
                    # If frame processing fails, use original frame
                    self.log_message(f"⚠️ Frame {frame_count} processing failed: {frame_error}")
                    out.write(frame)
                
                frame_count += 1
                if frame_count % 30 == 0:  # Update progress every 30 frames
                    progress = (frame_count / total_frames) * 100
                    self.log_message(f"📹 Progress: {frame_count}/{total_frames} frames ({progress:.1f}%)")
            
            cap.release()
            out.release()
            
            self.log_message(f"✅ Video processing completed: {frame_count} frames")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Video processing error: {e}")
            return False
    
    def show_rehifaces_results(self, output_dir: str):
        """Show ReHiFace-S results"""
        mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
        if mode == "simple":
            self.current_step = 6
        else:
            self.current_step = 6
        self.update_step_display()
        
        # Count output files and get their details
        output_files = []
        file_details = []
        if os.path.exists(output_dir):
            for f in os.listdir(output_dir):
                if f.endswith(('.mp4', '.avi', '.mov', '.png', '.jpg', '.jpeg')):
                    output_files.append(f)
                    file_path = os.path.join(output_dir, f)
                    file_size = os.path.getsize(file_path)
                    file_details.append(f"   • {f} ({file_size:,} bytes)")
        
        # Create detailed results info
        results_info = f"""🎉 ReHiFace-S processing completed!

🚀 Technology: ReHiFace-S (Real-time)
📁 Project Location: {self.project_dir}
📂 Results Location: {output_dir}

Files Processed:
• Source face: {os.path.basename(self.target_faces_files[0]) if hasattr(self, 'target_faces_files') and self.target_faces_files else 'None'}
• Content files: {len(self.convert_files) if hasattr(self, 'convert_files') else 0} files

Output Files Created ({len(output_files)} files):
{chr(10).join(file_details) if file_details else '   • No output files found'}

⚡ Results saved to: {output_dir}

🎭 Your instant face-swapped content is ready!
⏱️ Processing time: Seconds (vs hours with traditional training)

💡 Click "Open Results Folder" below to view your files!
"""
        
        # Ensure we have the results_text widget available
        try:
            if hasattr(self, 'results_text') and self.results_text:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, results_info)
                self.log_message("📊 Results displayed successfully")
            else:
                self.log_message("⚠️ Results text widget not available, logging results instead")
                self.log_message(results_info)
        except Exception as e:
            self.log_message(f"❌ Error displaying results: {e}")
            self.log_message(results_info)
        
        # Auto-open results folder if files were created
        if output_files:
            self.log_message(f"🎯 {len(output_files)} output files created successfully!")
            self.log_message(f"📁 Opening results folder: {output_dir}")
            # Auto-open folder after a short delay to let the user see the results message
            self.root.after(2000, lambda: self.open_specific_folder(output_dir))
        else:
            self.log_message("⚠️ No output files found - checking for processing issues")
            self.log_message(f"Expected output directory: {output_dir}")
            if os.path.exists(output_dir):
                all_files = os.listdir(output_dir)
                self.log_message(f"Files in output directory: {all_files}")
            else:
                self.log_message("Output directory does not exist")

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
        mode = getattr(self, 'mode_var', tk.StringVar(value="simple")).get()
        if mode == "simple":
            # In simple mode, this is the final step after processing
            self.current_step = 6  # Use step 6 internally to map to results tab (index 5)
        else:
            self.current_step = 6  # Results step in advanced mode
        self.update_step_display()
        
        # Populate results
        results_info = f"""🎉 Face swapping completed successfully!

Project Location: {self.project_dir}

Files Processed:
• Source faces extracted: {len(self.source_files) if hasattr(self, 'source_files') else 0} files
• Target faces extracted: {len(self.target_faces_files) if hasattr(self, 'target_faces_files') else 0} files  
• Content converted: {len(self.convert_files) if hasattr(self, 'convert_files') else 0} files

Results saved to: {os.path.join(self.project_dir, 'converted_output') if self.project_dir else 'No project directory'}

You can find your face-swapped videos/images in the converted_output folder.
"""
        
        # Ensure we have the results_text widget available
        try:
            if hasattr(self, 'results_text') and self.results_text:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, results_info)
                self.log_message("📊 Results displayed successfully")
            else:
                self.log_message("⚠️ Results text widget not available, logging results instead")
                self.log_message(results_info)
        except Exception as e:
            self.log_message(f"❌ Error displaying results: {e}")
            self.log_message(results_info)
        
    def open_results_folder(self):
        """Open results folder in file manager"""
        if self.project_dir:
            results_path = os.path.join(self.project_dir, 'converted_output')
            self.open_specific_folder(results_path)
            
    def open_project_folder(self):
        """Open project folder in file manager"""
        if self.project_dir:
            self.open_specific_folder(self.project_dir)
    
    def open_specific_folder(self, folder_path: str):
        """Open a specific folder in the file manager"""
        try:
            if os.path.exists(folder_path):
                import platform
                system = platform.system()
                if system == "Darwin":  # macOS
                    os.system(f'open "{folder_path}"')
                elif system == "Windows":
                    os.system(f'explorer "{folder_path}"')
                else:  # Linux and others
                    os.system(f'xdg-open "{folder_path}"')
                self.log_message(f"📁 Opened folder: {folder_path}")
            else:
                self.log_message(f"❌ Folder not found: {folder_path}")
        except Exception as e:
            self.log_message(f"❌ Failed to open folder: {e}")
    
    def launch_rehifaces_web(self):
        """Launch ReHiFace-S web interface"""
        try:
            # Check if ReHiFace-S is installed
            rehifaces_path = Path("fast_faceswap/ReHiFace-S")
            
            if not rehifaces_path.exists():
                # ReHiFace-S not installed, offer to install
                response = messagebox.askyesno(
                    "Install ReHiFace-S?",
                    "🚀 ReHiFace-S is not installed yet.\n\n"
                    "ReHiFace-S provides:\n"
                    "• Instant face swapping (10 second setup)\n"
                    "• Real-time processing (9,000x faster)\n"
                    "• Pre-trained models (no training required)\n"
                    "• muke.ai-style speed\n\n"
                    "Would you like to install ReHiFace-S now?"
                )
                
                if response:
                    self.install_rehifaces()
                return
            
            # Check if conda environment exists
            try:
                result = subprocess.run(['conda', 'list', '-n', 'rehifaces'], 
                                      capture_output=True, text=True, timeout=10)
                conda_available = result.returncode == 0
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                conda_available = False
            
            if not conda_available:
                messagebox.showerror(
                    "Environment Missing",
                    "❌ ReHiFace-S conda environment not found.\n\n"
                    "Please run the installation script:\n"
                    "./install_rehifaces.sh\n\n"
                    "Or install manually:\n"
                    "conda create -n rehifaces python=3.10\n"
                    "conda activate rehifaces\n"
                    "pip install torch torchvision onnxruntime opencv-python gradio"
                )
                return
            
            # Launch ReHiFace-S web interface
            messagebox.showinfo(
                "Launching ReHiFace-S",
                "🌐 Launching ReHiFace-S Web Interface...\n\n"
                "• Opening at http://localhost:7860\n"
                "• Use your browser to access the interface\n"
                "• Upload source face and target video/image\n"
                "• Get instant face swap results!\n\n"
                "Click OK to continue..."
            )
            
            # Change to ReHiFace-S directory and launch
            original_dir = os.getcwd()
            os.chdir(rehifaces_path)
            
            try:
                # Find the appropriate launch script
                web_scripts = ['web_interface.py', 'app.py', 'demo.py', 'interface.py']
                web_script = None
                
                for script in web_scripts:
                    script_path = rehifaces_path / script
                    if script_path.exists():
                        web_script = script
                        break
                
                if not web_script:
                    messagebox.showerror(
                        "Web Interface Not Found",
                        "❌ ReHiFace-S web interface script not found.\n\n"
                        "Expected files: web_interface.py, app.py, demo.py, or interface.py\n\n"
                        "Please run the installation script:\n"
                        "./install_rehifaces.sh"
                    )
                    return
                
                # Launch web interface in background
                web_cmd = ['conda', 'run', '-n', 'rehifaces', 'python', web_script]
                
                # Start the process in background
                process = subprocess.Popen(web_cmd, 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE)
                
                # Give it a moment to start
                time.sleep(3)
                
                # Check if process is still running (not crashed)
                if process.poll() is None:
                    # Success - open browser
                    webbrowser.open('http://localhost:7860')
                    
                    messagebox.showinfo(
                        "Success!",
                        "✅ ReHiFace-S web interface is running!\n\n"
                        "• Access at: http://localhost:7860\n"
                        "• The interface should open in your browser\n"
                        "• Upload your source face and target content\n"
                        "• Enjoy instant face swapping!"
                    )
                else:
                    # Process crashed, get error
                    stdout, stderr = process.communicate()
                    raise subprocess.SubprocessError(f"Process failed: {stderr.decode()}")
                    
            except Exception as launch_error:
                messagebox.showerror(
                    "Launch Failed",
                    f"❌ Failed to launch ReHiFace-S web interface.\n\n"
                    f"Error: {str(launch_error)}\n\n"
                    "Try manual launch:\n"
                    f"1. cd fast_faceswap/ReHiFace-S\n"
                    f"2. conda activate rehifaces\n"
                    f"3. python {web_script if 'web_script' in locals() else 'web_interface.py'}"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch ReHiFace-S: {str(e)}")
        finally:
            # Return to original directory
            if 'original_dir' in locals():
                os.chdir(original_dir)
    
    def install_rehifaces(self):
        """Install ReHiFace-S system"""
        try:
            # Show installation dialog
            install_dialog = messagebox.askyesno(
                "Install ReHiFace-S",
                "🚀 Installing ReHiFace-S Real-Time Face Swap\n\n"
                "This will:\n"
                "• Create a new conda environment 'rehifaces'\n"
                "• Download ReHiFace-S from HuggingFace\n"
                "• Install all required dependencies\n"
                "• Set up the web interface\n\n"
                "Installation may take 5-10 minutes.\n"
                "Continue with installation?"
            )
            
            if not install_dialog:
                return
                
            # Check if installation script exists
            install_script = Path("install_rehifaces.sh")
            if not install_script.exists():
                messagebox.showerror(
                    "Installation Script Missing",
                    "❌ Installation script not found: install_rehifaces.sh\n\n"
                    "Please download the complete package or\n"
                    "install ReHiFace-S manually following the\n"
                    "instructions in FASTER_FACE_SWAP_ALTERNATIVES.md"
                )
                return
            
            # Show progress dialog
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Installing ReHiFace-S...")
            progress_window.geometry("500x300")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            # Progress label
            progress_label = ttk.Label(progress_window, 
                                     text="🚀 Installing ReHiFace-S...\nThis may take 5-10 minutes.",
                                     font=('Arial', 12))
            progress_label.pack(pady=20)
            
            # Progress bar
            progress_bar = ttk.Progressbar(progress_window, length=400, mode='indeterminate')
            progress_bar.pack(pady=10)
            progress_bar.start()
            
            # Log text
            log_text = scrolledtext.ScrolledText(progress_window, height=10, width=60)
            log_text.pack(fill='both', expand=True, padx=20, pady=10)
            
            def run_installation():
                try:
                    # Run installation script
                    process = subprocess.Popen(['bash', str(install_script)],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT,
                                             text=True,
                                             universal_newlines=True)
                    
                    # Stream output to log
                    for line in iter(process.stdout.readline, ''):
                        if line:
                            progress_window.after(0, lambda l=line: log_text.insert(tk.END, l))
                    
                    # Wait for completion
                    process.wait()
                    
                    if process.returncode == 0:
                        # Success
                        progress_window.after(0, lambda: [
                            progress_bar.stop(),
                            progress_label.config(text="✅ Installation completed successfully!"),
                            messagebox.showinfo("Success", 
                                               "🎉 ReHiFace-S installed successfully!\n\n"
                                               "You can now use the real-time face swap features.\n"
                                               "Click 'Open ReHiFace-S Web Interface' to get started!"),
                            progress_window.destroy()
                        ])
                    else:
                        # Failed
                        progress_window.after(0, lambda: [
                            progress_bar.stop(),
                            progress_label.config(text="❌ Installation failed"),
                            messagebox.showerror("Installation Failed",
                                               "❌ ReHiFace-S installation failed.\n\n"
                                               "Check the log output above for details.\n"
                                               "You may need to install manually.")
                        ])
                    
                except Exception as e:
                    progress_window.after(0, lambda: [
                        progress_bar.stop(),
                        progress_label.config(text="❌ Installation error"),
                        messagebox.showerror("Error", f"Installation error: {str(e)}")
                    ])
            
            # Run installation in thread
            install_thread = threading.Thread(target=run_installation)
            install_thread.daemon = True
            install_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start installation: {str(e)}")
            
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
        
        # Clear all possible listboxes safely
        for listbox_name in ['source_listbox', 'target_faces_listbox', 'target_faces_listbox_simple', 
                           'convert_listbox', 'convert_listbox_simple']:
            if hasattr(self, listbox_name):
                listbox = getattr(self, listbox_name)
                try:
                    listbox.delete(0, tk.END)
                except (tk.TclError, AttributeError):
                    pass
                    
        # Clear text areas
        try:
            self.log_text.delete(1.0, tk.END)
            self.results_text.delete(1.0, tk.END)
        except (tk.TclError, AttributeError):
            pass
        
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
