"""
Utility functions for file filtering operations.
"""

import os


def is_text_file(file_path: str) -> bool:
    """
    Check if a file is a text file.

    Args:
        file_path (str): Path to the file to check

    Returns:
        bool: True if the file is a text file, False otherwise
    """
    # Common binary file extensions to ignore
    BINARY_EXTENSIONS = {
        ".gif",
        ".jpg",
        ".jpeg",
        ".png",
        ".ico",
        ".pdf",
        ".pyc",
        ".exe",
        ".dll",
        ".so",
        ".dylib",
        ".zip",
        ".tar",
        ".gz",
        ".rar",
        ".7z",
        ".db",
        ".sqlite",
        ".bin",
        ".dat",
    }
    # Git-specific files to ignore
    GIT_FILES = {".git/index", ".git/HEAD", ".git/COMMIT_EDITMSG"}

    ext = os.path.splitext(file_path)[1].lower()
    base = os.path.basename(file_path)

    if ext in BINARY_EXTENSIONS or base in GIT_FILES:
        return False

    try:
        with open(file_path, "tr") as f:
            f.read(1024)  # Try reading first 1KB
            return True
    except UnicodeDecodeError:
        return False
