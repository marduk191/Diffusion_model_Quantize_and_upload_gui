# Model Quantizer & Uploader GUI

A Python GUI application for quantizing AI models and automatically uploading them to Hugging Face repositories. This tool converts models from SafeTensors format to various GGUF quantization formats with a user-friendly interface.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)

## Features

### 🎯 **Multiple Quantization Formats**
Support for 40+ quantization formats including:
- **Standard formats**: F32, F16, BF16, Q8_0, Q6_K
- **Q5 variants**: Q5_0, Q5_1, Q5_K, Q5_K_S, Q5_K_M
- **Q4 variants**: Q4_0, Q4_1, Q4_K, Q4_K_S, Q4_K_M, Q4_0_4_4, Q4_0_4_8, Q4_0_8_8
- **Q3 variants**: Q3_K, Q3_K_S, Q3_K_M, Q3_K_L
- **Q2 variants**: Q2_K, Q2_K_S
- **Intelligent Quantization (IQ)**: IQ1_S, IQ1_M, IQ2_XXS through IQ4_XS
- **Ternary Quantization (TQ)**: TQ1_0, TQ2_0
- **Special formats**: fp8_scaled_stochastic

### 🖥️ **User-Friendly GUI**
- Clean, intuitive tkinter interface
- Scrollable quantization selection panel
- Real-time progress monitoring
- Comprehensive logging output
- Quick selection buttons (Select All, Deselect All, Select Common)

### ⚡ **Smart Processing**
- Multi-threaded processing (GUI remains responsive)
- Selective quantization (choose only what you need)
- Upload control (enable/disable automatic uploads)
- Error handling and validation
- Progress tracking with stop functionality

### 🚀 **Automated Workflow**
- Batch processing of multiple quantization formats
- Automatic Hugging Face repository uploads
- Organized output file structure
- Commit messages for version tracking

## Screenshots

### Main Interface
```
┌─────────────────────────────────────────────┐
│  Model Quantizer & Uploader                 │
├─────────────────────────────────────────────┤
│  File Name: [model-name________________]    │
│  Author:    [your-name________________]     │
│  Repository:[username/repo-name_______]     │
│  Base Path: [/path/to/models__________] [📁] │
│  Venv Path: [/path/to/venv____________] [📁] │
│                                             │
│  ☑ Enable automatic upload after quantization │
│                                             │
│  ┌── Select Quantizations ─────────────────┐ │
│  │ ☑BF16   ☐F32    ☑Q8_0   ☐Q6_K        │ │
│  │ ☑Q5_0   ☐Q5_1   ☐Q5_K   ☐Q5_K_S      │ │
│  │ ☑Q4_0   ☐Q4_1   ☐Q4_K   ☐Q4_K_S      │ │
│  │ ☐IQ4_XS ☐IQ3_M  ☐IQ2_S  ☐TQ1_0  ... │ │
│  │ [Select All] [Deselect All] [Common]   │ │
│  └─────────────────────────────────────────┘ │
│                                             │
│  [Start Processing] [Stop] [Clear Log]     │
│  ████████████████████████████████████████  │
│                                             │
│  Log Output:                                │
│  ┌─────────────────────────────────────────┐ │
│  │ Starting processing...                  │ │
│  │ --- Processing BF16 ---                 │ │
│  │ Successfully created BF16 version       │ │
│  │ Successfully uploaded BF16 version      │ │
│  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

## Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)
- Required tools in your `tools/` directory:
  - `convert.py` - Model conversion script
  - `llama-quantize.exe` - GGUF quantization tool
  - `convert_fp8_scaled_stochastic.py` - FP8 conversion script
- Hugging Face CLI configured with authentication

### Setup
1. Clone this repository:
```bash
git clone https://github.com/your-username/model-quantizer-gui.git
cd model-quantizer-gui
```

2. Install dependencies:
```bash
pip install tkinter  # If not already available
```

3. Set up your directory structure:
```
project_root/
├── quantizer_gui.py
├── tools/
│   ├── convert.py
│   ├── llama-quantize.exe
│   └── convert_fp8_scaled_stochastic.py
├── in/
│   └── chroma/
│       └── detailed/
│           └── your-model.safetensors
└── out/
    └── (generated output folders)
```

4. Configure Hugging Face CLI:
```bash
huggingface-cli login
```

## Usage

### Quick Start
1. Run the application:
```bash
python quantizer_gui.py
```

2. Configure your settings:
   - **File Name**: Name of your model file (without extension)
   - **Author**: Your name/username for file naming
   - **Repository**: Target Hugging Face repository (username/repo-name)
   - **Base Path**: Directory containing your project structure
   - **Venv Path**: Path to your Python virtual environment activation script

3. Select quantization formats:
   - Use checkboxes to select desired formats
   - Use "Select Common" for most popular formats
   - Use "Select All" to process all available formats

4. Choose upload option:
   - ✅ **Enabled**: Quantize and upload automatically
   - ❌ **Disabled**: Quantize only (no upload)

5. Click "Start Processing" and monitor the log output

### Advanced Usage

#### Selective Processing
You can run specific quantization types by unchecking unwanted formats. This is useful for:
- Testing new formats
- Re-running failed quantizations
- Processing only high-priority formats

#### Offline Mode
Disable uploads to work offline or test quantizations:
- Uncheck "Enable automatic upload after quantization"
- All files will be saved locally in `out/model-name/`
- Upload manually later using Hugging Face CLI

#### Batch Processing
Process multiple models by:
1. Changing the file name
2. Keeping other settings
3. Running processing again

## Directory Structure

### Input Structure
```
project_root/
├── in/
│   └── chroma/
│       └── detailed/
│           └── your-model.safetensors
```

### Output Structure
```
project_root/
├── out/
│   └── your-model/
│       ├── your-model-BF16-author.gguf
│       ├── your-model-Q8_0-author.gguf
│       ├── your-model-Q5_0-author.gguf
│       ├── your-model-Q4_0-author.gguf
│       └── your-model-fp8_scaled_stochastic-author.safetensors
```

## Quantization Format Guide

| Format | Description | Use Case | File Size |
|--------|-------------|----------|-----------|
| **F32** | 32-bit float | Maximum quality, huge files | 100% |
| **F16** | 16-bit float | High quality, large files | 50% |
| **BF16** | Brain float 16 | Good quality, manageable size | 50% |
| **Q8_0** | 8-bit quantization | Excellent quality/size balance | 25% |
| **Q5_K_M** | 5-bit K-quant medium | Good quality, smaller size | 20% |
| **Q4_K_M** | 4-bit K-quant medium | Decent quality, small size | 15% |
| **Q4_0** | 4-bit standard | Basic quality, very small | 12% |
| **IQ4_XS** | Intelligent 4-bit | Better than Q4_0, similar size | 12% |
| **Q2_K** | 2-bit K-quant | Minimal quality, tiny files | 8% |

### Recommended Formats
For most users, these formats provide the best balance:
- **Q8_0**: Near-original quality
- **Q5_K_M**: Excellent balance
- **Q4_K_M**: Good for limited storage
- **Q4_0**: Maximum compression

## Troubleshooting

### Common Issues

**"Input file not found"**
- Check that your model file exists in `in/chroma/detailed/`
- Verify the file name matches exactly (case-sensitive)
- Ensure the file has `.safetensors` extension

**"Base file not found for quantization"**
- Make sure BF16 conversion completed successfully first
- Check that `convert.py` is working properly
- Verify the tools directory contains all required scripts

**"Upload failed"**
- Confirm Hugging Face CLI is logged in: `huggingface-cli whoami`
- Check repository exists and you have write access
- Verify internet connection

**"Command timed out"**
- Large models may take longer than 5 minutes
- Increase timeout in the code if needed
- Check system resources (RAM/CPU)

### Performance Tips
- **RAM Usage**: Large models require significant RAM for quantization
- **Storage**: Ensure enough disk space for all output formats
- **CPU**: Multi-core CPUs will process quantizations faster
- **Selection**: Only select needed formats to save time

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Original batch script by marduk191
- GGUF quantization tools from the llama.cpp project
- Hugging Face for model hosting and CLI tools
- Python tkinter for the GUI framework

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/your-username/model-quantizer-gui/issues) page
2. Create a new issue with detailed information
3. Include log output and error messages

---

**⭐ Star this repository if you find it helpful!**