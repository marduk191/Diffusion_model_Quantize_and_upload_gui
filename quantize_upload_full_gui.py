import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import subprocess
import threading
from pathlib import Path
import sys

class ModelQuantizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Model Quantizer & Uploader")
        self.root.geometry("800x700")
        
        # Variables
        self.fname = tk.StringVar(value="chroma-unlocked-v47-detail-calibrated_sma_v3b")
        self.author = tk.StringVar(value="marduk191")
        self.reponame = tk.StringVar(value="marduk191/Chroma_quants")
        self.basepath = tk.StringVar(value=os.getcwd())
        self.venv_path = tk.StringVar(value=r"I:\AI\ComfyUI\venv\Scripts\activate")
        
        self.setup_gui()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Input fields
        ttk.Label(main_frame, text="File Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(main_frame, textvariable=self.fname, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(main_frame, text="Author:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(main_frame, textvariable=self.author, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)
        
        ttk.Label(main_frame, text="Repository:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(main_frame, textvariable=self.reponame, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)
        
        # Path selection
        ttk.Label(main_frame, text="Base Path:").grid(row=3, column=0, sticky=tk.W, pady=2)
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)
        path_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(path_frame, textvariable=self.basepath, width=40).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(path_frame, text="Browse", command=self.browse_basepath).grid(row=0, column=1, padx=(5, 0))
        
        ttk.Label(main_frame, text="Venv Path:").grid(row=4, column=0, sticky=tk.W, pady=2)
        venv_frame = ttk.Frame(main_frame)
        venv_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)
        venv_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(venv_frame, textvariable=self.venv_path, width=40).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(venv_frame, text="Browse", command=self.browse_venv).grid(row=0, column=1, padx=(5, 0))
        
        # Upload option
        ttk.Label(main_frame, text="Upload to HuggingFace:").grid(row=5, column=0, sticky=tk.W, pady=(10, 2))
        self.enable_upload = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Enable automatic upload after quantization", variable=self.enable_upload).grid(row=5, column=1, sticky=tk.W, pady=(10, 2))
        
        # Quantization options
        ttk.Label(main_frame, text="Quantization Types:").grid(row=6, column=0, sticky=(tk.W, tk.N), pady=(10, 2))
        
        quant_frame = ttk.LabelFrame(main_frame, text="Select Quantizations", padding="5")
        quant_frame.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=(10, 2))
        
        self.quant_vars = {}
        # Organized quantization types by category
        quant_types = [
            # Standard formats (enabled by default)
            ("F32", False), ("F16", False), ("BF16", True),
            ("Q8_0", True), ("Q6_K", False),
            
            # Q5 variants
            ("Q5_K_M", False), ("Q5_K_S", False), ("Q5_K", False),
            ("Q5_1", False), ("Q5_0", True),
            
            # Q4 variants
            ("Q4_K_M", False), ("Q4_K_S", False), ("Q4_K", False),
            ("Q4_1", False), ("Q4_0", True),
            ("Q4_0_8_8", False), ("Q4_0_4_8", False), ("Q4_0_4_4", False),
            
            # Q3 variants
            ("Q3_K_L", False), ("Q3_K_M", False), ("Q3_K_S", False), ("Q3_K", False),
            
            # Q2 variants
            ("Q2_K_S", False), ("Q2_K", False),
            
            # IQ variants (intelligent quantization)
            ("IQ4_NL", False), ("IQ4_XS", False),
            ("IQ3_XS", False), ("IQ3_M", False), ("IQ3_S", False), ("IQ3_XXS", False),
            ("IQ2_M", False), ("IQ2_S", False), ("IQ2_XS", False), ("IQ2_XXS", False),
            ("IQ1_M", False), ("IQ1_S", False),
            
            # TQ variants (ternary quantization)
            ("TQ2_0", False), ("TQ1_0", False),
            
            # Custom formats
            ("fp8_scaled_stochastic", True)
        ]
        
        # Create scrollable frame for quantization options
        canvas = tk.Canvas(quant_frame, height=200)
        scrollbar = ttk.Scrollbar(quant_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add quantization checkboxes in a grid
        cols = 4  # Number of columns
        for i, (qtype, default) in enumerate(quant_types):
            var = tk.BooleanVar(value=default)
            self.quant_vars[qtype] = var
            row = i // cols
            col = i % cols
            ttk.Checkbutton(scrollable_frame, text=qtype, variable=var).grid(
                row=row, column=col, sticky=tk.W, padx=5, pady=2
            )
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add select/deselect all buttons
        button_frame_quant = ttk.Frame(quant_frame)
        button_frame_quant.pack(fill="x", pady=5)
        
        ttk.Button(button_frame_quant, text="Select All", 
                  command=self.select_all_quants).pack(side="left", padx=2)
        ttk.Button(button_frame_quant, text="Deselect All", 
                  command=self.deselect_all_quants).pack(side="left", padx=2)
        ttk.Button(button_frame_quant, text="Select Common", 
                  command=self.select_common_quants).pack(side="left", padx=2)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=(20, 10))
        
        ttk.Button(button_frame, text="Start Processing", command=self.start_processing).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Stop", command=self.stop_processing).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Log output
        ttk.Label(main_frame, text="Log Output:").grid(row=9, column=0, sticky=(tk.W, tk.N), pady=(10, 2))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=80)
        self.log_text.grid(row=9, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(9, weight=1)
        
        # Processing control
        self.is_processing = False
        self.process_thread = None
        
    def select_all_quants(self):
        """Select all quantization types"""
        for var in self.quant_vars.values():
            var.set(True)
    
    def deselect_all_quants(self):
        """Deselect all quantization types"""
        for var in self.quant_vars.values():
            var.set(False)
    
    def select_common_quants(self):
        """Select commonly used quantization types"""
        common_types = ["BF16", "Q8_0", "Q5_0", "Q4_0", "Q4_K_M", "Q5_K_M"]
        
        # First deselect all
        self.deselect_all_quants()
        
        # Then select common ones
        for qtype, var in self.quant_vars.items():
            if qtype in common_types:
                var.set(True)
    
    def browse_basepath(self):
        path = filedialog.askdirectory(title="Select Base Path")
        if path:
            self.basepath.set(path)
    
    def browse_venv(self):
        path = filedialog.askopenfilename(
            title="Select Virtual Environment Activation Script",
            filetypes=[("Batch files", "*.bat"), ("All files", "*.*")]
        )
        if path:
            self.venv_path.set(path)
    
    def log_message(self, message):
        """Add message to log with timestamp"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def start_processing(self):
        if self.is_processing:
            messagebox.showwarning("Warning", "Processing is already in progress!")
            return
        
        # Validate inputs
        if not self.fname.get().strip():
            messagebox.showerror("Error", "File name is required!")
            return
        
        if not self.author.get().strip():
            messagebox.showerror("Error", "Author name is required!")
            return
        
        if not self.reponame.get().strip():
            messagebox.showerror("Error", "Repository name is required!")
            return
        
        # Check if any quantization is selected
        if not any(var.get() for var in self.quant_vars.values()):
            messagebox.showerror("Error", "Please select at least one quantization type!")
            return
        
        self.is_processing = True
        self.progress.start()
        self.log_message("Starting processing...")
        
        # Start processing in separate thread
        self.process_thread = threading.Thread(target=self.run_processing)
        self.process_thread.daemon = True
        self.process_thread.start()
    
    def stop_processing(self):
        self.is_processing = False
        self.progress.stop()
        self.log_message("Processing stopped by user.")
    
    def run_command(self, command, shell=True):
        """Run a command and return success status"""
        try:
            self.log_message(f"Running: {command}")
            result = subprocess.run(command, shell=shell, capture_output=True, text=True, timeout=300)
            
            if result.stdout:
                self.log_message(f"Output: {result.stdout}")
            if result.stderr:
                self.log_message(f"Error: {result.stderr}")
            
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            self.log_message("Command timed out!")
            return False
        except Exception as e:
            self.log_message(f"Exception running command: {str(e)}")
            return False
    
    def run_processing(self):
        try:
            fname = self.fname.get().strip()
            author = self.author.get().strip()
            reponame = self.reponame.get().strip()
            basepath = Path(self.basepath.get().strip())
            
            # Setup paths
            input_path = basepath / "in" / f"{fname}.safetensors"
            output_dir = basepath / "out" / fname
            output_base = output_dir / fname
            tools_dir = basepath / "tools"
            
            self.log_message(f"Input file: {input_path}")
            self.log_message(f"Output directory: {output_dir}")
            
            # Check if input file exists
            if not input_path.exists():
                self.log_message(f"Error: Input file not found: {input_path}")
                return
            
            # Create output directory
            output_dir.mkdir(parents=True, exist_ok=True)
            self.log_message(f"Created output directory: {output_dir}")
            
            # Change to tools directory
            original_cwd = os.getcwd()
            if tools_dir.exists():
                os.chdir(tools_dir)
                self.log_message(f"Changed to tools directory: {tools_dir}")
            else:
                self.log_message(f"Warning: Tools directory not found: {tools_dir}")
            
            # Process each selected quantization
            mvers = "BF16"  # Base version for quantization
            
            try:
                for qtype, var in self.quant_vars.items():
                    if not var.get() or not self.is_processing:
                        continue
                    
                    self.log_message(f"\n--- Processing {qtype} ---")
                    
                    if qtype == "BF16":
                        # Convert to GGUF BF16
                        output_file = f"{output_base}-{qtype}-{author}.gguf"
                        cmd = f'python convert.py --src "{input_path}" --dst "{output_file}"'
                        
                        if self.run_command(cmd):
                            self.log_message(f"Successfully created {qtype} version")
                            # Upload
                            if self.enable_upload.get():
                                upload_cmd = f'huggingface-cli upload {reponame} "{output_file}" ./{fname}/"{fname}-{qtype}-{author}.gguf" --commit-message "uploaded {fname}-{qtype}-{author}.gguf"'
                                if self.run_command(upload_cmd):
                                    self.log_message(f"Successfully uploaded {qtype} version")
                                else:
                                    self.log_message(f"Failed to upload {qtype} version")
                            else:
                                self.log_message(f"Upload skipped for {qtype} version (upload disabled)")
                        else:
                            self.log_message(f"Failed to create {qtype} version")
                    
                    elif qtype == "fp8_scaled_stochastic":
                        # FP8 scaled conversion
                        output_file = f"{output_base}-{qtype}-{author}.safetensors"
                        cmd = f'python convert_fp8_scaled_stochastic.py --input "{input_path}" --output "{output_file}"'
                        
                        if self.run_command(cmd):
                            self.log_message(f"Successfully created {qtype} version")
                            # Upload
                            if self.enable_upload.get():
                                upload_cmd = f'huggingface-cli upload {reponame} "{output_file}" ./{fname}/"{fname}-{qtype}-{author}.safetensors" --commit-message "uploaded {fname}-{qtype}-{author}.safetensors"'
                                if self.run_command(upload_cmd):
                                    self.log_message(f"Successfully uploaded {qtype} version")
                                else:
                                    self.log_message(f"Failed to upload {qtype} version")
                            else:
                                self.log_message(f"Upload skipped for {qtype} version (upload disabled)")
                        else:
                            self.log_message(f"Failed to create {qtype} version")
                    
                    else:
                        # All other quantization types using llama-quantize
                        # For F32, F16 formats, use the original file as base
                        if qtype in ["F32", "F16"]:
                            # These might need special handling or conversion
                            base_file = f"{output_base}-BF16-{author}.gguf"  # Use BF16 as base
                        else:
                            base_file = f"{output_base}-{mvers}-{author}.gguf"
                        
                        output_file = f"{output_base}-{qtype}-{author}.gguf"
                        
                        # Check if base file exists
                        if not Path(base_file).exists():
                            self.log_message(f"Warning: Base file not found for {qtype}: {base_file}")
                            self.log_message(f"Skipping {qtype} quantization")
                            continue
                        
                        cmd = f'llama-quantize.exe "{base_file}" "{output_file}" {qtype}'
                        
                        if self.run_command(cmd):
                            self.log_message(f"Successfully created {qtype} version")
                            # Upload
                            if self.enable_upload.get():
                                upload_cmd = f'huggingface-cli upload {reponame} "{output_file}" ./{fname}/"{fname}-{qtype}-{author}.gguf" --commit-message "uploaded {fname}-{qtype}-{author}.gguf"'
                                if self.run_command(upload_cmd):
                                    self.log_message(f"Successfully uploaded {qtype} version")
                                else:
                                    self.log_message(f"Failed to upload {qtype} version")
                            else:
                                self.log_message(f"Upload skipped for {qtype} version (upload disabled)")
                        else:
                            self.log_message(f"Failed to create {qtype} version")
            
            finally:
                # Restore original working directory
                os.chdir(original_cwd)
            
            if self.is_processing:
                self.log_message("\n=== Processing completed! ===")
            
        except Exception as e:
            self.log_message(f"Error during processing: {str(e)}")
        
        finally:
            self.is_processing = False
            self.progress.stop()

def main():
    root = tk.Tk()
    app = ModelQuantizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
