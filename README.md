# LLMs-Full HTML Generator

This repository provides a Python script to generate `llms-full.html` files—a way to make website and project documentation more accessible to Large Language Models (LLMs).

## Overview

`llms-full.html` is an HTML file that aggregates complete documentation (including code examples) into one file for easy ingestion by LLMs. It complements traditional standards like `sitemap.xml` and `robots.txt` by focusing on content accessibility for AI models.

### Key Features

- **Comprehensive Content:** Combines full documentation and code.
- **AI-Friendly Format:** Uses HTML to keep the content simple and structured, with generated summaries for easier AI ingestion.
- **Efficient Processing:** Consolidates all relevant content to help overcome LLM context limitations.
- **OpenRouter Summarization:** Uses the OpenRouter chat completions API to summarize file content.

## Repository Structure
- **README.md:** Project overview and usage instructions.
- **src/**
  - **utils.py:** Shared utility functions and constants.
  - **generate_llms_html.py:** Generates `llms-full.html` from a given directory.

## Usage Examples

### Prerequisites

- Python 3.9+
- An OpenRouter API key provided via one of:
  - Environment variable `OPENROUTER_API_KEY`
  - Fallback file `~/.api-openrouter` containing the key as a single line

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url> ; cd llms-full-html
   ```
2. Create a virtual environment using `uv`:
   ```bash
   python -m uv venv .venv
   ```
3. Ensure tooling inside the venv:
   ```bash
   .venv/Scripts/python.exe -m ensurepip ; .venv/Scripts/python.exe -m pip install uv
   ```
4. Install dependencies (runtime):
   ```bash
   .venv/Scripts/python.exe -m uv pip install -r requirements.txt
   ```
   For development and tests (fully pinned dev stack):
   ```bash
   .venv/Scripts/python.exe -m uv pip install -r requirements-dev.txt
   ```

### Generate `llms-full.html`

```bash
.venv/Scripts/python.exe src/generate_llms_html.py
```

### Notes on Authentication

The tool will first look for `OPENROUTER_API_KEY` in the environment. If not set, it falls back to reading `~/.api-openrouter`. Without a key, summaries will be skipped (returning None).

## License

This repository is licensed under the MIT-0 License.