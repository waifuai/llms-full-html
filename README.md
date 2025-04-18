# LLMs-Full HTML Generator

This repository provides a Python script to generate `llms-full.html` files—a way to make website and project documentation more accessible to Large Language Models (LLMs).

## Overview

`llms-full.html` is an HTML file that aggregates complete documentation (including code examples) into one file for easy ingestion by LLMs. It complements traditional standards like `sitemap.xml` and `robots.txt` by focusing on content accessibility for AI models.

### Key Features

- **Comprehensive Content:** Combines full documentation and code.
- **AI-Friendly Format:** Uses HTML to keep the content simple and structured, with generated summaries for easier AI ingestion.
- **Efficient Processing:** Consolidates all relevant content to help overcome LLM context limitations.
- **Gemini Summarization:** Leverages the Gemini API to generate concise summaries of file content.

## Repository Structure
- **README.md:** Project overview and usage instructions.
- **src/**
  - **utils.py:** Shared utility functions and constants.
  - **generate_llms_html.py:** Generates `llms-full.html` from a given directory.

## Usage Examples

### Prerequisites

- Python 3.7+
- A Gemini API key. Store this key in a file named `.api-gemini` in your home directory (`~/.api-gemini`).

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd llms-full-html
   ```
2. Create a virtual environment using `uv`:
   ```bash
   python -m uv venv .venv
   ```
3. Activate the virtual environment:
   ```bash
   source .venv/Scripts/activate
   ```
4. Install dependencies:
   ```bash
   .venv/Scripts/python.exe -m uv pip install -e .[test] google-generativeai
   ```

### Generate `llms-full.html`
```bash
.venv/Scripts/python.exe -m python src/generate_llms_html.py
```

## License

This repository is licensed under the MIT-0 License.