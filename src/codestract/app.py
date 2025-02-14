"""
Codestract - A CLI tool for extracting and combining code files.
"""

import os
import sys

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import DirectoryTree, Header

from .ui.widgets.file_tree_panel import FileTreePanel
from .ui.widgets.summary_panel import SummaryPanel
from .utils.file_utils import is_text_file
from .utils.logging import setup_logging


class FileExportApp(App):
    """Main terminal app for interactively selecting and exporting files."""

    TITLE = "Codestract"
    SUB_TITLE = "Select files to generate contextfile"

    CSS_PATH = "styles/app.css"

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("e", "export", "Export Files", show=True),
        Binding("space", "toggle_file", "Toggle Selection", show=True),
        Binding("f", "toggle_files", "Show/Hide Files", show=True),
        Binding("/", "search", "Search", show=True),
    ]

    DEFAULT_CSS = """
    Screen {
        background: $surface;
    }
    """

    def __init__(self, start_path: str | None = None) -> None:
        """Initialize the application with an optional starting path."""
        super().__init__()
        self.start_path = start_path or os.getcwd()
        setup_logging()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=False)
        yield FileTreePanel(self.start_path)
        yield SummaryPanel()

    def on_mount(self) -> None:
        """Handle app mount event."""
        tree_panel = self.query_one(FileTreePanel)
        tree = tree_panel.get_tree()
        tree.focus()
        tree_panel.refresh_tree_icons()

    @on(DirectoryTree.FileSelected)
    def handle_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle file selection in the directory tree."""
        file_path = str(event.path)
        if not os.path.isfile(file_path) or not is_text_file(file_path):
            return

        tree_panel = self.query_one(FileTreePanel)
        summary_panel = self.query_one(SummaryPanel)

        if file_path in tree_panel.selected_files:
            tree_panel.selected_files.remove(file_path)
        else:
            tree_panel.selected_files.add(file_path)

        tree_panel.refresh_tree_icons()
        summary_panel.update_selection_count(tree_panel.selected_files)
        summary_panel.update_preview()

    @on(DirectoryTree.NodeExpanded)
    def handle_directory_expanded(self, _: DirectoryTree.NodeExpanded) -> None:
        """Handle directory expansion by refreshing icons for newly visible nodes."""
        tree_panel = self.query_one(FileTreePanel)
        tree_panel.refresh_tree_icons()

    def action_toggle_file(self) -> None:
        """Toggle selection of the currently focused file."""
        tree_panel = self.query_one(FileTreePanel)
        tree = tree_panel.get_tree()
        if (
            tree.cursor_node
            and hasattr(tree.cursor_node, "data")
            and tree.cursor_node.data
        ):
            tree.select_node(tree.cursor_node)

    def action_export(self) -> None:
        """Export selected files."""
        summary_panel = self.query_one(SummaryPanel)
        summary_panel.handle_export()


def main() -> None:
    """Entry point for the application."""
    if len(sys.argv) > 1:
        start_path = sys.argv[1]
    else:
        start_path = os.getcwd()

    app = FileExportApp(start_path)
    app.run()


if __name__ == "__main__":
    main()
