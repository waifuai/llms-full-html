# LLMs-Full HTML Generator

This repository provides a Python script to generate `llms-full.html` files—a way to make website and project documentation more accessible to Large Language Models (LLMs).

## Overview

`llms-full.html` is an HTML file that aggregates complete documentation (including code examples) into one file for easy ingestion by LLMs. It complements traditional standards like `sitemap.xml` and `robots.txt` by focusing on content accessibility for AI models.

### Key Features
- **Comprehensive Content:** Combines full documentation and code.
- **AI-Friendly Format:** Uses HTML to keep the content simple and structured.
- **Efficient Processing:** Consolidates all relevant content to help overcome LLM context limitations.

## Repository Structure

- **README.md:** Project overview and usage instructions.
- **src/**
  - **utils.py:** Shared utility functions and constants.
  - **generate_llms_html.py:** Generates `llms-full.html` from a given directory.

## Usage Examples

### Generate `llms-full.html`
```bash
python generate_llms_html.py
```

## License

This repository is licensed under the MIT-0 License.