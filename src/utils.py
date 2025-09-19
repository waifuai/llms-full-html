"""
Utility Functions Module

This module provides common utility functions and constants used across the LLMs HTML
generator project. It contains helper functions for safe file reading with encoding
fallback and defines comprehensive file extension constants for identifying different
types of code and text files.

Key components:
- safe_read(): Robust file reading function with UTF-8/Latin-1 encoding fallback
- CODE_EXTENSIONS: Comprehensive tuple of file extensions for various programming
  languages, markup formats, and text files supported by the project

These utilities are used by the main HTML generation module to process different
file types and handle encoding issues gracefully.
"""
import os

# Common file extensions for code and text files.
CODE_EXTENSIONS = (
    '.py', '.txt', '.java', '.c', '.cpp', '.h', '.hpp', '.js', '.jsx', '.ts', '.tsx',
    '.html', '.htm', '.css', '.scss', '.less', '.sh', '.bash', '.go', '.rb', '.php',
    '.sql', '.xml', '.json', '.yaml', '.yml', '.ini', '.toml', '.md', '.markdown',
    '.swift', '.kt', '.dart', '.scala', '.groovy', '.perl', '.lua', '.r', '.m',
    '.asm', '.s', '.f', '.for', '.f90', '.f95', '.f03', '.pas', '.ada', '.v',
    '.vhdl', '.csproj', '.sln', '.vb', '.vbs', '.pl', '.tcl', '.coffee', '.hs', '.erl',
    '.rs', '.jl', '.clj', '.lisp', '.scm', '.edn', '.mat', '.m', '.cmake', '.gradle',
    '.dockerfile', '.gitignore', '.env', '.config', '.tf', '.tfvars', '.proto',
    '.ps1', '.bat',
)

def safe_read(filepath):
    """
    Safely read the content of a file by trying UTF-8 and falling back to Latin-1 encoding.

    Args:
        filepath (str): The path to the file.

    Returns:
        str or None: The file content if successful; otherwise, None.
    """
    for encoding in ('utf-8', 'latin-1'):
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return None
    print(f"Skipping file due to encoding issues: {filepath}")
    return None