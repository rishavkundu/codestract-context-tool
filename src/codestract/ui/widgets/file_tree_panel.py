"""
File tree panel widget for displaying and managing the directory structure.
"""

import os
from typing import Set

from rich.text import Text
from textual.containers import Container
from textual.widgets import DirectoryTree, Label
from textual.widgets.tree import TreeNode

from ...utils.constants import ICONS
from ...utils.file_utils import is_text_file


class FileTreePanel(Container):
    """A container widget for the file tree and its header."""

    def __init__(self, start_path: str) -> None:
        """Initialize the file tree panel."""
        super().__init__(id="tree-container")
        self.start_path = start_path
        self.selected_files: Set[str] = set()

    def compose(self):
        """Create child widgets for the panel."""
        yield Label(
            f"{ICONS['folder']} Project Files (Space: Toggle)",
            id="tree-header",
        )
        yield DirectoryTree(
            self.start_path,
            id="file-tree",
        )

    def refresh_tree_icons(self) -> None:
        """Refresh the file tree icons."""
        tree = self.query_one(DirectoryTree)
        root = tree.root
        if root:
            self._update_node_icons(root)

    def _update_node_icons(self, node: TreeNode) -> None:
        """Update icons for a node and its children recursively."""
        if hasattr(node, "data") and node.data:
            path = str(node.data.path)
            is_selected = path in self.selected_files
            is_text = is_text_file(path) if os.path.isfile(path) else True

            # Show different styling for non-text files
            if not is_text and os.path.isfile(path):
                name = os.path.basename(path)
                node.label = Text.from_markup(f"[dim]⊘ {name}[/]")
            else:
                name = os.path.basename(path)
                # Only show checkbox for selected items
                prefix = ICONS["selected"] + " " if is_selected else ""
                node.label = Text.from_markup(f"{prefix}{name}")

            # Recursively update children
            for child in node.children:
                self._update_node_icons(child)

    def select_all_in_node(self, node: TreeNode) -> None:
        """Recursively select all files in a node and its children."""
        if hasattr(node, "data") and node.data:
            path = str(node.data.path)
            if os.path.isfile(path) and is_text_file(path):
                self.selected_files.add(path)
            for child in node.children:
                self.select_all_in_node(child)

    def get_tree(self) -> DirectoryTree:
        """Get the DirectoryTree widget."""
        return self.query_one(DirectoryTree)
