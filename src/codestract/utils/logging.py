"""
Logging configuration for the application.
"""

import logging
import os
from datetime import datetime


def setup_logging() -> None:
    """
    Configure logging for the application.

    Sets up logging to both console and a file in the current directory.
    The log file is named with a timestamp for each session.
    """
    # Create .codestract directory if it doesn't exist
    output_dir = "."
    os.makedirs(output_dir, exist_ok=True)

    # Create a timestamped log file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(output_dir, f"codestract_{timestamp}.log")

    # Configure logging format
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Set up root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear any existing handlers
    logger.handlers.clear()

    # Create and configure file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    logger.addHandler(file_handler)

    # Create and configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    logger.addHandler(console_handler)

    # Log initial message
    logging.info("Logging initialized")
