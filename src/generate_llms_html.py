import os
import re
import html
import sys
from utils import safe_read
from google import genai
import httpx

GEMINI_MODEL = "gemini-2.5-pro"
_GENAI_CLIENT = None  # module-level cache

def _get_client(api_key: str):
    global _GENAI_CLIENT
    if _GENAI_CLIENT is not None:
        return _GENAI_CLIENT
    # Create client with short HTTP timeout to avoid blocking generation
    # google-genai honors httpx client options via client params
    try:
        _GENAI_CLIENT = genai.Client(
            api_key=api_key,
            http_client=httpx.Client(timeout=httpx.Timeout(10.0, connect=5.0, read=10.0, write=10.0)),
        )
    except Exception:
        # Fallback without custom http client if construction fails
        _GENAI_CLIENT = genai.Client(api_key=api_key)
    return _GENAI_CLIENT

def get_gemini_api_key(filepath="~/.api-gemini"):
    """Resolve API key from env or fallback file."""
    # Prefer env vars
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if api_key:
        return api_key.strip()

    # Fallback to key file
    try:
        expanded_filepath = os.path.expanduser(filepath)
        with open(expanded_filepath, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Warning: API key not found. Set GEMINI_API_KEY/GOOGLE_API_KEY or create {filepath}")
        return None
    except Exception as e:
        print(f"Error reading API key file: {e}")
        return None

def summarize_content(content, api_key):
    """Summarize content using Google GenAI SDK, with network-safe fallbacks."""
    if not api_key:
        return "Summary not available: API key not found."

    prompt = (
        "Provide a concise, factual summary of the following content. "
        "Focus on purpose, key features, and important details. "
        "Limit to 3-6 bullet points if possible.\n\n"
    ) + content

    try:
        client = _get_client(api_key)
        resp = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        # google-genai returns text via resp.text; keep a defensive fallback
        if hasattr(resp, "text") and resp.text:
            return resp.text
        if hasattr(resp, "candidates") and resp.candidates:
            for cand in resp.candidates:
                if getattr(cand, "content", None) and getattr(cand.content, "parts", None):
                    parts = cand.content.parts
                    texts = [getattr(p, "text", "") for p in parts if getattr(p, "text", None)]
                    if texts:
                        return "".join(texts)
        return "Summary generation failed: Empty response."
    except (httpx.TimeoutException, httpx.HTTPError) as net_err:
        print(f"Network issue while generating summary: {net_err}")
        return "Summary skipped due to network timeout."
    except KeyboardInterrupt:
        # Ensure generation still completes even if user interrupts
        return "Summary skipped due to interruption."
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Summary skipped due to API error."

def generate_llms_html(directory, output_file="llms-full.html"):
    """
    Generates an HTML file from a directory structure, including Markdown files and other text files,
    with clickable links for easy navigation.

    Args:
        directory (str): The root directory to process.
        output_file (str): The output file name (default: "llms-full.html").
    """
    markdown_files = []
    other_text_files = []

    # Categorize files
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filename.endswith(".md"):
                markdown_files.append(filepath)
            elif filename.endswith((".txt", ".py", ".js", ".html", ".sh", ".rs", ".toml")):
                other_text_files.append(filepath)

    # Sort files for consistent output
    markdown_files.sort()
    other_text_files.sort()

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
        h1, h2 { color: #333; }
        h2 { border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-top: 30px; }
        pre { background-color: #f4f4f4; padding: 10px; border: 1px solid #ddd; overflow-x: auto; }
        code { font-family: monospace; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Project Documentation</h1>
    <nav>
        <h2>Table of Contents</h2>
        <ol>
    """

    toc_entries = []
    content_sections = []

    api_key = get_gemini_api_key()

    # Process Markdown Files
    markdown_section_id = 'markdown-files'
    html_content += f"<li><a href='#{markdown_section_id}'>Markdown Files</a></li>"
    content_sections.append(f"<h2 id='{markdown_section_id}'>Markdown Files</h2>")
    content_sections.append("<p>Comprehensive documentation of the project in Markdown format.</p>")
    content_sections.append(f"<p><a href='#top'>Back to Table of Contents</a></p>")

    for filepath in markdown_files:
        content = safe_read(filepath)
        if content is None:
            continue

        # Extract title or derive from filename
        title_match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else os.path.basename(filepath).replace(".md", "").replace("_", " ").title()
        section_id = title.lower().replace(" ", "-")
        toc_entries.append(f"<li><a href='#{section_id}'>{title}</a></li>")
        content_sections.append(f"<h2 id='{section_id}'>{title}</h2>")
        content_sections.append(f"<p><a href='#top'>Back to Table of Contents</a></p>")


        # Extract summary if available or generate using Gemini
        summary_match = re.search(r"^>\s+(.+)", content, re.MULTILINE)
        if summary_match:
            summary = summary_match.group(1).strip()
            content_sections.append(f"<p>Summary: {summary}</p>")
        else:
            # Generate summary using Gemini
            summary = summarize_content(content, api_key)
            content_sections.append(f"<p>Generated Summary: {summary}</p>")


        # Remove title and summary if already written
        content_to_write = content
        if title_match:
            content_to_write = content_to_write.replace(title_match.group(0), "", 1)
        if summary_match:
            content_to_write = content_to_write.replace(summary_match.group(0), "", 1)
        content_sections.append(f"<pre><code>{html.escape(content_to_write.strip())}</code></pre>")

    # Process Other Text Files
    code_section_id = 'code-files'
    html_content += f"<li><a href='#{code_section_id}'>Code and Other Files</a></li>"
    content_sections.append(f"<h2 id='{code_section_id}'>Code and Other Files</h2>")
    content_sections.append("<p>Code snippets, scripts, and other relevant text files.</p>")
    content_sections.append(f"<p><a href='#top'>Back to Table of Contents</a></p>")

    for filepath in other_text_files:
        content = safe_read(filepath)
        if content is None:
            continue

        title = os.path.basename(filepath)
        section_id = title.lower().replace(" ", "-")
        toc_entries.append(f"<li><a href='#{section_id}'>{title}</a></li>")
        content_sections.append(f"<h2 id='{section_id}'>{title}</h2>")
        content_sections.append(f"<p><a href='#top'>Back to Table of Contents</a></p>")

        # Generate summary using Gemini
        summary = summarize_content(content, api_key)
        content_sections.append(f"<p>Generated Summary: {summary}</p>")

        content_sections.append("<pre><code>{}</code></pre>".format(html.escape(content.strip())))

    html_content += "".join(toc_entries)
    html_content += """
        </ol>
    </nav>
    <main>
    """
    html_content += "".join(content_sections)
    html_content += """
    </main>
</body>
</html>
    """

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(html_content)

    print(f"Successfully generated {output_file} from {directory}")

def main():
    root_directory = "."
    generate_llms_html(root_directory)

if __name__ == "__main__":
    main()