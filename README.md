# Codestract — A lightweight CLI contextfile tool

A lightweight CLI tool for exporting and combining code files into a single context file, perfect for working with Large Language Models (LLMs).

<div align="center">
  <img src="image.webp" alt="codestract-main" width="1280"/>
</div>

## Features

- **Interactive File Selection**: Navigate and select files using an intuitive terminal interface
- **Smart File Filtering**: Automatically identifies and filters non-text files
- **Organized Output**: Generates descriptive context files with clear file separators and metadata
- **Project Statistics**: Shows real-time statistics about selected files
- **Native Experience**: Uses platform-native keyboard shortcuts and navigation patterns

## Installation

### Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/codestract.git
cd codestract

# Install dependencies
pip install -r requirements.txt

# Run locally
python -m codestract [directory_path]
```

### Global Installation

Install the tool globally to use `codestract` from any directory:

```bash
# Clone and install globally
git clone https://github.com/yourusername/codestract.git
cd codestract
pip install -e .

# Now you can run from anywhere
codestract [directory_path]
```

To uninstall:

```bash
pip uninstall codestract
```

## Usage

1. Navigate the file tree using arrow keys
2. Press `Space` to toggle file selection
3. Use `Enter` to expand/collapse directories
4. Press `e` to export selected files
5. Press `q` to quit

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Toggle Selection |
| `Enter` | Expand/Collapse |
| `e` | Export Files |
| `f` | Show/Hide Files |
| `/` | Search |
| `q` | Quit |

## Output

Generated context files are saved in your current directory with:

- Intuitive naming: `{directory_name}_context_{timestamp}.txt`
- File metadata and statistics
- Clear file separators
- Project summary

## Requirements

- Python 3.8+
- Terminal with Unicode support
- For macOS: iTerm2, Kitty, or WezTerm recommended for best experience

## License

[MIT License](LICENSE)
