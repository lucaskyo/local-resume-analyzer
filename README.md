# Resume Reviewer 🦙

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Ollama Engine](https://img.shields.io/badge/Ollama-qwen2.5--3b-black)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An AI-powered **Human Resources recruiting assistant** that uses Ollama (`qwen2.5:3b`) to compare resume PDFs with job descriptions and generate structured feedback exported as portuguese formatted PDF. It supports recruiters and HR professionals during resume screening, profile positioning and interview preparation.

> [!NOTE]  
> The tool is designed to make the initial recruiting analysis faster and more consistent. It does not replace the professional judgment of the recruiter or the final hiring decision.

---

## 📌 Features

- **Local PDF Discovery**: Automatically detects resume `.pdf` files in the `resumes` folder and job `.pdf` files in the `positions` folder.
- **Interactive CLI**: Simple terminal prompt to select which resume you want to analyze.
- **Privacy-First**: Runs 100% locally via Ollama with no external API calls or data sharing.
- **PDF Report Export**: Saves each generated review in the `output` folder.

## 📊 Review Structure

1. **Compatibility with the Position** 
2. **General Impression and Positioning**
3. **Strengths for the Position**
4. **Interview Questions**


## 💻 System Requirements

| Requirement | Specification |
| :--- | :--- |
| **CPU** | AVX2-compatible x86_64 CPU or Apple Silicon (M1/M2/M3) |
| **GPU** | Minimum 6 GB VRAM (Modern Architecture with Tensor Cores recommended for optimal inference speeds) |
| **Disk Space** | 4 GB free disk space |
| **Python** | Python 3.9 or newer |
| **Ollama** | Installed and running with `qwen2.5:3b` model |


## 🚀 Quick Start Guide

### 1 - Install & Pull Model

\- Download and install [Ollama](https://ollama.com/), then pull the required model:

```bash
ollama pull qwen2.5:3b
```
### 2 - Install Dependencies
\- Clone this repository and install the Python packages:

```bash
pip install -r requirements.txt
```
### 3 - Usage
\- Place one or more resume PDF files in the `resumes` folder.<br>
\- Place one or more job description PDF files in the `positions` folder.<br>
\- Ensure Ollama is running in the background.<br>
\- Start the application:<br>

```bash
python main.py
```
\- Enter the number corresponding to the resume you wish to review and then the number corresponding to the job description.
<br>


<br>

## 📁 Project Structure
```Plaintext
.
├── resumes/           # Resume PDF files
├── positions/         # Job description PDF files
├── output/            # Generated review PDFs
├── main.py         # Main CLI application logic & PDF processing
├── requirements.txt   # Required Python dependencies
└── README.md          # Project documentation
```
## ⚠️ Important Considerations
- Text Layer Required: Scanned image-only PDFs without an embedded text layer are not supported.
- Local LLM Reliance: Quality depends entirely on the local Ollama model's generation capabilities.
- Advisory Nature: Generated reviews are AI-assisted recommendations and should be reviewed before taking professional decisions.
