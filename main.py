import os
import logging
from datetime import datetime

def is_image_file(file_name: str) -> bool:
    # Checks if a file is an image file based on its extension.
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg'}
    _, extension = os.path.splitext(file_name)
    return extension.lower() in image_extensions

def append_files_to_project(directory: str = '.', output_file: str = 'project_context_export.txt', excluded_files: set = None):
    output_dir = '.codestract'
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, output_file)

    if excluded_files is None:
        excluded_files = {output_file, 'main.py'}
    else:
        excluded_files.update({output_file, 'main.py'})

    total_chars = 0
    file_count = 0
    total_file_size = 0
    skipped_dirs = []
    skipped_files = []

    start_time = datetime.now()

    try:
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            for root, dirs, files in os.walk(directory):
                # Skip directories named '.env' or '.venv'
                dirs[:] = [d for d in dirs if d not in {'.env', '.venv'}]
                skipped_dirs.extend([os.path.join(root, d) for d in set(dirs) - set(os.listdir(root))])

                for file in files:
                    if file not in excluded_files and not is_image_file(file):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            contents = infile.read()
                            outfile.write(f'# File: {file_path}\n\n')
                            outfile.write(contents)
                            outfile.write("\n\n")
                            total_chars += len(contents)
                            file_count += 1
                            total_file_size += os.path.getsize(file_path)
                    else:
                        skipped_files.append(os.path.join(root, file))

            end_time = datetime.now()
            execution_time = end_time - start_time

            summary = f'Summary:\n'
            summary += f'- Total characters: {total_chars}\n'
            summary += f'- Total files processed: {file_count}\n'
            summary += f'- Total file size: {total_file_size} bytes\n'
            summary += f'- Skipped directories: {len(skipped_dirs)}\n'
            summary += f'- Skipped files: {len(skipped_files)}\n'
            summary += f'- Execution time: {execution_time}\n'

            outfile.write(summary)
            logging.info(summary)
            print(summary)

            if skipped_dirs:
                logging.info("Skipped directories:")
                for directory in skipped_dirs:
                    logging.info(directory)
            if skipped_files:
                logging.info("Skipped files:")
                for file in skipped_files:
                    logging.info(file)

        return True
    except Exception as e:
        logging.error(f"Failed to write to {output_file_path}: {e}")
        return False

def setup_logging(log_file_name='logfile.log'):
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
    if append_files_to_project():
        logging.info("Code base exported successfully.")
        print("Code base exported successfully.")
    else:
        logging.error("Failed to export code base.")
        print("Failed to export code base.")

if __name__ == "__main__":
    main()
