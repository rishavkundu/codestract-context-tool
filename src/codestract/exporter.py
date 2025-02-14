"""
Module for handling file export operations in Codestract.
"""

import logging
import os
from datetime import datetime
from typing import Dict, Set


def calculate_file_stats(files: Set[str]) -> Dict[str, Dict[str, int]]:
    """
    Calculate statistics for the given files.

    Args:
        files: Set of file paths to analyze

    Returns:
        Dictionary mapping file paths to their statistics (chars, lines, size)
    """
    stats: Dict[str, Dict[str, int]] = {}

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                stats[file_path] = {
                    "chars": len(content),
                    "lines": len(content.splitlines()),
                    "size": os.path.getsize(file_path),
                }
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            stats[file_path] = {"chars": 0, "lines": 0, "size": 0}

    return stats


def export_selected_files(selected_files: Set[str]) -> str:
    """
    Export selected files by concatenating their contents into a single file.

    Args:
        selected_files: Set of file paths to export

    Returns:
        A formatted summary string of the export operation
    """
    if not selected_files:
        return "[red]No files selected for export[/]"

    # Generate a descriptive filename based on the current directory and timestamp
    current_dir = os.path.basename(os.getcwd())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_name = f"{current_dir}_context_{timestamp}.txt"

    # Calculate stats before export
    stats = calculate_file_stats(selected_files)
    total_chars = sum(info["chars"] for info in stats.values())
    total_lines = sum(info["lines"] for info in stats.values())
    total_size = sum(info["size"] for info in stats.values())
    skipped_files = []

    try:
        with open(output_file_name, "w", encoding="utf-8") as outfile:
            # Write header with statistics
            outfile.write("# Codebase Export\n")
            outfile.write(f"# Generated: {datetime.now().isoformat()}\n")
            outfile.write(f"# Files: {len(selected_files)}\n")
            outfile.write(f"# Total Lines: {total_lines:,}\n")
            outfile.write(f"# Total Characters: {total_chars:,}\n")
            outfile.write(f"# Total Size: {total_size:,} bytes\n\n")

            for file_path in sorted(selected_files):
                if not os.path.isfile(file_path):
                    skipped_files.append(file_path)
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        contents = infile.read()
                        file_stats = stats[file_path]

                        # Write file separator and metadata
                        outfile.write(f"{'=' * 80}\n")
                        outfile.write(f"# File: {file_path}\n")
                        outfile.write(f"# Lines: {file_stats['lines']:,}\n")
                        outfile.write(f"# Characters: {file_stats['chars']:,}\n")
                        outfile.write(f"# Size: {file_stats['size']:,} bytes\n")
                        outfile.write(f"{'=' * 80}\n\n")

                        # Write file contents
                        outfile.write(contents)
                        outfile.write("\n\n")

                except Exception as e:
                    logging.error(f"Error reading file {file_path}: {e}")
                    skipped_files.append(file_path)

            # Write summary
            summary = (
                f"\n{'=' * 80}\n"
                f"Export Summary\n"
                f"{'=' * 80}\n"
                f"📊 Statistics:\n"
                f"• Files processed: {len(selected_files) - len(skipped_files)}\n"
                f"• Total lines: {total_lines:,}\n"
                f"• Total characters: {total_chars:,}\n"
                f"• Total size: {total_size:,} bytes\n"
                f"• Output file: {output_file_name}\n"
            )

            if skipped_files:
                summary += "\n❌ Skipped files:\n"
                for file in skipped_files:
                    summary += f"• {file}\n"

            outfile.write(summary)
            logging.info(f"Export completed: {output_file_name}")

            # Return a colorized version for the UI
            return f"[green]✅ Export successful![/]\n{summary}"

    except Exception as e:
        error_msg = f"[red]❌ Export failed: {str(e)}[/]"
        logging.error(error_msg)
        return error_msg
