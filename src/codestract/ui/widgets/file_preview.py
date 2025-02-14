"""
File preview widget for displaying selected files and their statistics.
"""

import os
from typing import Dict, Set

from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual.widgets import Static

from ...exporter import calculate_file_stats


class FilePreview(Static):
    """A widget to display file preview and statistics."""

    DEFAULT_CSS = """
    FilePreview {
        height: auto;
        margin: 0;
        width: 100%;
    }

    FilePreview Panel {
        width: 100%;
    }

    FilePreview Table {
        width: 100%;
        padding: 0;
    }
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.files_info: Dict[str, dict] = {}

    def update_preview(self, files: Set[str]) -> None:
        """Update the preview with selected files info."""
        if not files:
            self.update(Panel("[dim]No files selected[/]", padding=(0, 1)))
            return

        self.files_info = calculate_file_stats(files)
        self._render_preview(files)

    def _render_preview(self, files: Set[str]) -> None:
        """Render the preview content using Rich components."""
        total_chars = sum(info["chars"] for info in self.files_info.values())
        total_lines = sum(info["lines"] for info in self.files_info.values())
        total_size = sum(info["size"] for info in self.files_info.values())

        # Create statistics table
        stats_table = Table(
            show_header=False,
            show_edge=False,
            padding=(0, 1),
            box=None,
            expand=True,
        )

        # Add statistics in a clean, aligned format
        stats_table.add_row(
            Text("Total Files:", style="dim"),
            Text(str(len(files)), style="cyan bold"),
            Text("Total Lines:", style="dim"),
            Text(f"{total_lines:,}", style="cyan bold"),
        )

        stats_table.add_row(
            Text("Total Characters:", style="dim"),
            Text(f"{total_chars:,}", style="cyan bold"),
            Text("Total Size:", style="dim"),
            Text(self._format_size(total_size), style="cyan bold"),
        )

        # Create files table
        files_table = Table(
            show_header=False,
            show_edge=False,
            padding=(0, 0),
            box=None,
            expand=True,
        )

        # Add file listings
        for file_path in sorted(files):
            info = self.files_info[file_path]
            rel_path = os.path.relpath(file_path)

            files_table.add_row(
                Text("•", style="dim"),
                Text(" " + rel_path, style="cyan"),
                Text(f"{info['lines']:,} lines", style="dim"),
                Text(f"{info['chars']:,} chars", style="dim"),
                Text(self._format_size(info["size"]), style="dim"),
            )

        # Combine all components into panels
        content = Group(
            Panel(
                stats_table,
                title="[bold white]File Statistics[/]",
                title_align="left",
                padding=(0, 1),
            ),
            Panel(
                files_table,
                title="[bold white]Selected Files[/]",
                title_align="left",
                padding=(0, 1),
            ),
        )
        self.update(content)

    def _format_size(self, size_in_bytes: int) -> str:
        """Format file size in human-readable format."""
        units = ["B", "KB", "MB", "GB", "TB"]
        size = float(size_in_bytes)
        unit_index = 0

        while size >= 1024.0 and unit_index < len(units) - 1:
            size /= 1024.0
            unit_index += 1

        return f"{size:,.1f} {units[unit_index]}"
