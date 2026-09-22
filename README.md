# Resume Reviewer 🦙

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Ollama Engine](https://img.shields.io/badge/Ollama-qwen2.5--3b-black)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An AI-powered CLI application that analyzes resume PDFs locally using Ollama (`qwen2.5:3b`) and generates structured, actionable feedback exported as a formatted PDF.

---

## 📌 Features

- **Local PDF Discovery**: Automatically detects all `.pdf` files in the project root directory.
- **Interactive CLI**: Simple terminal prompt to select which resume you want to analyze.
- **Privacy-First**: Runs 100% locally via Ollama with no external API calls or data sharing.
- **Structured Evaluation**: Generates detailed professional feedback formatted in Portuguese.
- **PDF Report Export**: Exports the generated review directly to `output.pdf`.

---

## 📊 Review Structure

The generated evaluation is organized into four core sections:

1. **General Impression and Positioning**
2. **Strengths**
3. **Opportunities for Improvement**
4. **Practical Recommendations**

---

## 💻 System Requirements

| Requirement | Specification |
| :--- | :--- |
| **CPU / GPU** | AVX2-compatible CPU or Apple Silicon (M1/M2/M3) |
| **Memory** | Minimum 6 GB VRAM |
| **Disk Space** | 3 GB free disk space |
| **Python** | Python 3.9 or newer |
| **Ollama** | Installed and running with `qwen2.5:3b` model |

---

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
\- Place one or more resume PDF files in the same folder as project.py.<br>
\- Ensure Ollama is running in the background.<br>
\- Start the application:<br>

```bash
python project.py
```
\- Enter the number corresponding to the resume you wish to review.
<br>

>[!NOTE]
>The report will be saved as output.pdf in the project directory. Running the program again will overwrite the existing output.pdf.

<br>

📁 Project Structure
```Plaintext
.
├── project.py         # Main CLI application logic & PDF processing
├── requirements.txt   # Required Python dependencies
└── output.pdf         # Generated review PDF (created upon execution)
```
## ⚠️ Limitations
- Single Page Processing: Only the first page of the selected PDF is extracted and analyzed.
- Text Layer Required: Scanned image-only PDFs without an embedded text layer are not supported.
- Local LLM Reliance: Quality depends entirely on the local Ollama model's generation capabilities.
- Advisory Nature: Generated reviews are AI-assisted recommendations and should be reviewed before taking professional decisions.
