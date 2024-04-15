# Codestract | Export project & provide LLMs context on your code.

Codestract is a tool designed to identify and collect text files from specified directories, excluding image files and other specified exclusions. This functionality facilitates efficient file management and data aggregation, making it an essential tool for developers who need to organize and analyze their project files effectively.
  
## About the Project

Codestract simplifies the process of collecting and aggregating text-based file contents from various subdirectories while filtering out image files based on their extensions. It is aimed at developers who require a quick method to gather file data without manually selecting each file.

## Requirements

- **Python**: Python 3.8+ is required to run the script.

## Features

- **File Exclusion**: Automatically excludes certain files like `main.py` and output files from processing.

- **Image File Filtering**: Filters out files with image extensions such as `.jpg`, `.png`, etc.

- **Recursive Directory Traversal**: Capable of traversing through all subdirectories within a specified directory.
  
### Prerequisites
Ensure that Python 3.8 or higher is installed on your system:

```bash

sudo apt-get install python3

```

### Installation
Clone the repository and navigate into the project directory:

```bash

git clone https://github.com/yourusername/your-repository.git

cd your-repository

```
### Usage
To use the script, run the following command in your terminal. It will start the process of scanning for files and appending their contents to the specified output file.

```bash

python3 main.py

```


## Roadmap

Future improvements include:

- **GUI Implementation**: To enhance user interaction.

- **Support for Additional File Types**: Expand the types of files that can be processed.
