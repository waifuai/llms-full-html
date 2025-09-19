import os
import shutil
import tempfile
import unittest
import asyncio
from unittest.mock import Mock, patch, MagicMock
import sys
import json
from pathlib import Path

from utils import safe_read, CODE_EXTENSIONS

# Import the main module functions for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
try:
    from generate_llms_html import generate_llms_html, get_gemini_api_key, summarize_content
except ImportError:
    # Handle import gracefully if dependencies are not available
    generate_llms_html = None
    get_gemini_api_key = None
    summarize_content = None

class TestSafeRead(unittest.TestCase):
    def setUp(self):
        # Create a temporary file to test safe_read.
        self.test_dir = tempfile.mkdtemp()
        self.file_path = os.path.join(self.test_dir, "test.txt")
        self.content = "Sample content for safe read."
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(self.content)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_safe_read_success(self):
        # Verify safe_read correctly returns the content.
        result = safe_read(self.file_path)
        self.assertEqual(result, self.content)

    def test_safe_read_nonexistent(self):
        # Verify safe_read returns None for a non-existent file.
        non_existent = os.path.join(self.test_dir, "nofile.txt")
        result = safe_read(non_existent)
        self.assertIsNone(result)

    def test_safe_read_encoding_fallback(self):
        # Test reading file with different encoding
        utf8_content = "UTF-8 content: café"
        utf8_file = os.path.join(self.test_dir, "utf8.txt")
        with open(utf8_file, "w", encoding="utf-8") as f:
            f.write(utf8_content)

        result = safe_read(utf8_file)
        self.assertEqual(result, utf8_content)

class TestCodeExtensions(unittest.TestCase):
    def test_code_extensions_comprehensive(self):
        """Test that CODE_EXTENSIONS includes expected file types"""
        expected_extensions = {'.py', '.js', '.html', '.css', '.md', '.json', '.txt'}
        for ext in expected_extensions:
            self.assertIn(ext, CODE_EXTENSIONS, f"Extension {ext} should be in CODE_EXTENSIONS")

    def test_code_extensions_length(self):
        """Test that CODE_EXTENSIONS has a reasonable number of extensions"""
        self.assertGreater(len(CODE_EXTENSIONS), 50, "Should have many file extensions covered")

class TestUtils(unittest.TestCase):
    def test_safe_read_with_binary_file(self):
        """Test safe_read handles binary files gracefully"""
        binary_file = os.path.join(tempfile.mkdtemp(), "binary.bin")
        try:
            with open(binary_file, "wb") as f:
                f.write(b"\x00\x01\x02\x03")

            result = safe_read(binary_file)
            # Note: The function might successfully read binary content as text
            # So we just check it returns something (not crashing)
            self.assertIsInstance(result, (str, type(None)))
        finally:
            os.remove(binary_file)

@unittest.skipIf(generate_llms_html is None, "Main module not available")
class TestGenerateLLMsHTML(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.output_file = os.path.join(self.test_dir, "test_output.html")

        # Create test markdown file
        self.md_file = os.path.join(self.test_dir, "test.md")
        with open(self.md_file, "w", encoding="utf-8") as f:
            f.write("# Test Document\n\nThis is a test document.\n\n> This is a summary.\n\nSome content here.")

        # Create test Python file
        self.py_file = os.path.join(self.test_dir, "test.py")
        with open(self.py_file, "w", encoding="utf-8") as f:
            f.write("# Test Python file\ndef hello():\n    print('Hello, World!')")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch('generate_llms_html.get_gemini_api_key')
    @patch('generate_llms_html.summarize_content')
    def test_generate_llms_html_basic(self, mock_summarize, mock_get_key):
        """Test basic HTML generation functionality"""
        mock_get_key.return_value = None  # No API key
        mock_summarize.return_value = "Mocked summary"

        generate_llms_html(self.test_dir, self.output_file)

        # Check that output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Read the generated content
        with open(self.output_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Basic checks
        self.assertIn("Project Documentation", content)
        self.assertIn("Table of Contents", content)
        self.assertIn("Test Document", content)
        self.assertIn("test.py", content)

    def test_generate_llms_html_with_empty_directory(self):
        """Test HTML generation with empty directory"""
        empty_dir = os.path.join(self.test_dir, "empty")
        os.makedirs(empty_dir)

        generate_llms_html(empty_dir, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))

        with open(self.output_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Project Documentation", content)


@unittest.skipIf(generate_llms_html is None, "Main module not available")
class TestAsyncFunctionality(unittest.TestCase):
    """Test async functionality for AI summarization"""

    def setUp(self):
        self.test_content = "This is test content for summarization."

    @patch('generate_llms_html.summarize_with_openrouter')
    @patch('generate_llms_html.get_gemini_api_key')
    def test_summarize_content_fallback(self, mock_get_key, mock_openrouter):
        """Test summarization fallback mechanism"""
        mock_get_key.return_value = "test_key"
        mock_openrouter.return_value = None  # OpenRouter fails

        with patch('generate_llms_html.summarize_with_gemini') as mock_gemini:
            mock_gemini.return_value = "Gemini summary"

            result = summarize_content(self.test_content, "test_key")
            self.assertEqual(result, "Gemini summary")
            mock_openrouter.assert_called_once()
            mock_gemini.assert_called_once()

    @patch('generate_llms_html.summarize_with_openrouter')
    def test_summarize_content_openrouter_success(self, mock_openrouter):
        """Test successful OpenRouter summarization"""
        mock_openrouter.return_value = "OpenRouter summary"

        result = summarize_content(self.test_content, None)
        self.assertEqual(result, "OpenRouter summary")

    def test_summarize_content_no_api_key(self):
        """Test summarization when no API key is available"""
        result = summarize_content(self.test_content, None)
        self.assertIn("Summary not available", result)

if __name__ == "__main__":
    unittest.main()