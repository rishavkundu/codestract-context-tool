"""
Summary panel widget for displaying file selection summary and export controls.
"""

from typing import Set

from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual import work
from textual.containers import ScrollableContainer
from textual.widgets import Label, Static

from ...exporter import export_selected_files
from .file_preview import FilePreview


class SummaryPanel(ScrollableContainer):
    """A container widget for the summary panel and export controls."""

    DEFAULT_CSS = """
    SummaryPanel {
        width: 100%;
        padding: 0 1;
        scrollbar-size: 1 1;
        scrollbar-gutter: stable;
        overflow-x: hidden;
    }

    SummaryPanel:focus {
        scrollbar-color: $accent;
        scrollbar-background: $background;
    }

    SummaryPanel > Static {
        width: 100%;
    }

    #selection-count {
        height: 0;
    }

    #spacing {
        height: 0;
    }

    #shortcuts-legend {
        margin-top: 0;
    }

    #export-summary {
        margin-top: 0;
    }

    Panel {
        border: solid #20403F;
        width: 100%;
    }
    """

    def __init__(self) -> None:
        """Initialize the summary panel."""
        super().__init__(id="summary-container")
        self.selected_files: Set[str] = set()

    def compose(self):
        """Create child widgets for the panel."""
        yield Label("", id="selection-count")
        yield FilePreview("", id="file-preview")
        yield Label("", id="spacing")
        yield Static(self._create_shortcuts_panel(), id="shortcuts-legend")
        yield Label("", id="export-summary")

    def _create_shortcuts_panel(self) -> Panel:
        """Create a panel displaying keyboard shortcuts."""
        table = Table(
            show_header=False,
            show_edge=False,
            padding=(0, 0),
            box=None,
            expand=True,
        )

        shortcuts = [
            ("q", "Quit"),
            ("e", "Export Files"),
            ("space", "Toggle Selection"),
            ("enter", "Expand/Collapse"),
            ("f", "Show/Hide Files"),
            ("/", "Search"),
        ]

        for key, action in shortcuts:
            table.add_row(
                Text(key, style="cyan bold"),
                Text("→", style="dim"),
                Text(action),
            )

        return Panel(
            table,
            title="[bold white]Keyboard Shortcuts[/]",
            title_align="left",
            padding=(0, 1),
        )

    def update_selection_count(self, selected_files: Set[str]) -> None:
        """Update the selection count display."""
        self.selected_files = selected_files
        count = len(selected_files)
        count_label = self.query_one("#selection-count", Label)
        count_label.update(f"{count} files selected")

    @work(thread=True)
    def update_preview(self) -> None:
        """Update the file preview asynchronously in a background thread."""
        preview = self.query_one(FilePreview)
        preview.update_preview(self.selected_files)

    @work(thread=True)
    def handle_export(self) -> None:
        """Handle the export action."""
        if not self.selected_files:
            self.show_export_error()
            return

        summary = export_selected_files(self.selected_files)
        self.show_export_summary(summary)

    def show_export_error(self) -> None:
        """Show export error message."""
        summary_label = self.query_one("#export-summary", Label)
        summary_label.update(
            Panel(
                "[red]❌ No files selected for export[/]",
                title="Export Error",
                title_align="left",
                padding=(0, 1),
            )
        )

    def show_export_summary(self, summary: str) -> None:
        """Show export summary message."""
        summary_label = self.query_one("#export-summary", Label)
        summary_label.update(
            Panel(
                summary,
                title="Export Summary",
                title_align="left",
                padding=(0, 1),
            )
        )
