import os
import logging
from datetime import datetime
from csgui import display_summary, show_file_selection_gui

def is_selected_file(file_name: str, selected_types: list) -> bool:
    """Checks if a file should be included based on its extension and user selection."""
    _, extension = os.path.splitext(file_name)
    return extension.lower() in selected_types

def append_files_to_project(directory: str = '.', selected_types: list = None, excluded_files: set = None):
    """Appends selected text-based files from the project to a single output file."""
    output_dir = '.codestract'
    os.makedirs(output_dir, exist_ok=True)

    if excluded_files is None:
        excluded_files = {'main.py'}
    else:
        excluded_files.update({'main.py'})

    total_chars = 0
    file_count = 0
    total_file_size = 0
    skipped_dirs = []
    skipped_files = []

    start_time = datetime.now()
    timestamp = start_time.strftime("%Y%m%d_%H%M%S")
    output_file_name = f"project_export_{timestamp}.txt"
    output_file_path = os.path.join(output_dir, output_file_name)

    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            for root, dirs, files in os.walk(directory):
                # Skip directories named '.env' or '.venv'
                dirs[:] = [d for d in dirs if d not in {'.env', '.venv'}]

                # Capture skipped directories
                skipped_dirs.extend([os.path.join(root, d) for d in set(dirs) - set(os.listdir(root))])

                for file in files:
                    file_path = os.path.join(root, file)
                    if file not in excluded_files and is_selected_file(file, selected_types):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as infile:
                                contents = infile.read()
                                outfile.write(f'# File: {file_path}\n\n')
                                outfile.write(contents)
                                outfile.write("\n\n")
                                total_chars += len(contents)
                                file_count += 1
                                total_file_size += os.path.getsize(file_path)
                        except Exception as e:
                            logging.error(f"Error reading file {file_path}: {e}")
                            skipped_files.append(file_path)
                    else:
                        skipped_files.append(file_path)

            end_time = datetime.now()
            execution_time = end_time - start_time

            summary = (f'Summary:\n'
                       f'- Total characters: {total_chars}\n'
                       f'- Total files processed: {file_count}\n'
                       f'- Total file size: {total_file_size} bytes\n'
                       f'- Skipped directories: {len(skipped_dirs)}\n'
                       f'- Skipped files: {len(skipped_files)}\n'
                       f'- Execution time: {execution_time}\n')

            outfile.write('-' * 40 + '\n')
            outfile.write(summary)
            outfile.write('-' * 40 + '\n')

            logging.info(summary)

            if skipped_dirs:
                logging.info("Skipped directories:")
                for directory in skipped_dirs:
                    logging.info(directory)
            if skipped_files:
                logging.info("Skipped files:")
                for file in skipped_files:
                    logging.info(file)

            # Display the summary in a GUI popup
            display_summary(summary, skipped_files)

        return True
    except Exception as e:
        logging.error(f"Failed to write to {output_file_path}: {e}")
        return False

def setup_logging(log_file_name='logfile.log'):
    """Sets up logging configuration."""
    output_dir = '.codestract'
    os.makedirs(output_dir, exist_ok=True)
    log_file_path = os.path.join(output_dir, log_file_name)

    # Setup logging to file and console
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # Create handlers
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_file_path)
    # Create formatter and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    # Add handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

def main():
    setup_logging()
    
    def start_export(selected_types):
        if append_files_to_project(selected_types=selected_types):
            logging.info("Code base exported successfully.")
        else:
            logging.error("Failed to export code base.")

    show_file_selection_gui(start_export)

if __name__ == "__main__":
    main()
