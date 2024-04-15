# Codestract — Export codebase context for LLMs

<br>

<div>
<img src="Codestract.png" alt="codestract-main" width="500"/>
</div>
<br>

Codestract is a powerful command-line tool designed to extract and consolidate text-based files from your codebase into a single context file. This tool is particularly useful for developers working with Large Language Models (LLMs), as it allows them to efficiently prepare their codebase for analysis or fine-tuning by the LLM.

## Features

- **Recursive Directory Traversal**: Codestract can traverse through all subdirectories within a specified directory, ensuring that no file is left behind.
- **File Exclusion**: Automatically excludes certain files like `main.py` and output files from processing, allowing you to customize the exclusion list.
- **Image File Filtering**: Filters out files with image extensions such as `.jpg`, `.png`, etc., to focus solely on text-based files.
- **Timestamp-based Output Files**: Each time the script is run, a new output file with a timestamp is generated and saved in the `context-out` folder, ensuring that your context files are organized and easy to reference.
- **Project Structure Summary**: Codestract generates a summary of the project structure, including directories and files, and inserts it at the top of each exported context file.
- **Encoding Support**: The script supports different file encodings, ensuring compatibility with a wide range of files.
- **Command-line Arguments and Configuration**: Codestract can be customized through command-line arguments and configuration files, allowing you to specify various options such as the directory, output directory, excluded files, file encoding, and logging settings.
- **Logging**: The script provides detailed logging to both the console and a log file, making it easier to monitor and debug the execution process.

## Requirements

- **Python**: Python 3.8+ is required to run the script.

## Getting Started

### Prerequisites

Ensure that Python 3.8 or higher is installed on your system:

```bash
sudo apt-get install python3
```

### Installation

Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/yourusername/codestract.git
cd codestract
```

### Usage

To use the script, run the following command in your terminal. It will start the process of scanning for files and appending their contents to the specified output file.

```bash
python3 main.py
```

You can also pass various command-line arguments to customize the behavior of the script:

```
usage: main.py [-h] [-d DIRECTORY] [-o OUTPUT_DIR] [-c CONFIG] [-e ENCODING] [--log-file LOG_FILE] [--log-level LOG_LEVEL]

Code context exporting script.

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        The directory to search for files.
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        The path of the output directory.
  -c CONFIG, --config CONFIG
                        The path of the configuration file.
  -e ENCODING, --encoding ENCODING
                        The encoding to use for reading and writing files.
  --log-file LOG_FILE   The path of the log file.
  --log-level LOG_LEVEL
                        The log level (e.g., DEBUG, INFO, WARNING, ERROR).
```

Alternatively, you can create a configuration file and specify its path using the `-c` or `--config` argument.

## Roadmap

Future improvements include:

- **GUI Implementation**: To enhance user interaction and provide a more user-friendly experience.
- **Support for Additional File Types**: Expand the types of files that can be processed, allowing for a more comprehensive codebase context extraction.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
