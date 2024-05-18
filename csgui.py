import os
import tkinter as tk
from tkinter import ttk, messagebox

def display_summary(summary: str, skipped_files: list):
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Create the summary message
    message = summary + "\n\nSkipped files:\n" + "\n".join(skipped_files)
    
    # Show the summary in a popup window
    messagebox.showinfo("Export Summary", message)
    root.destroy()

def get_file_types(directory: str = '.'):
    file_types = set()
    for root, _, files in os.walk(directory):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext:
                file_types.add(ext.lower())
    return sorted(file_types)

def show_file_selection_gui(start_export_callback):
    root = tk.Tk()
    root.title("Select File Types to Export")
    root.configure(bg='#080808')

    # Grouping file types by category
    categories = {
        "Web Development": [".js", ".html", ".css", ".php", ".jsx", ".tsx", ".vue"],
        "General Purpose": [".py", ".java", ".cpp", ".c", ".cs", ".rb", ".swift", ".go", ".ts", ".sh"],
        "Data": [".sql", ".xml", ".json", ".yaml", ".r", ".jl"],
        "Documentation": [".md"],
        "Mobile": [".kt", ".dart"],
        "Functional": [".hs", ".clj", ".ex", ".scala", ".rkt", ".scm", ".lisp", ".erl", ".fs"],
        "Scripting": [".pl", ".lua", ".tcl"],
        "System Programming": [".rs", ".asm"],
        "Scientific": [".m", ".f"],
        "Other": [".vb", ".groovy", ".nim", ".lean", ".vhdl", ".v", ".pro", ".ml"]
    }

    # Sort categories and file types
    categories = {k: sorted(v) for k, v in sorted(categories.items())}

    # Dictionary to hold the selected file types
    selected_file_types = {ext: tk.BooleanVar(value=False) for exts in categories.values() for ext in exts}

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Instructions
    instructions = ttk.Label(frame, text="Select file types to export:")
    instructions.grid(row=0, column=0, columnspan=3, pady=(0, 10))

    # Create a search bar
    search_var = tk.StringVar()
    search_bar = ttk.Entry(frame, textvariable=search_var)
    search_bar.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))
    
    def update_checkbuttons(*args):
        search_term = search_var.get().lower()
        for checkbox, ext in checkbuttons.items():
            checkbox.grid_remove()
            if search_term in ext:
                checkbox.grid()

    search_var.trace_add("write", update_checkbuttons)

    # Create checkboxes in multiple columns
    checkbuttons = {}
    row_offset = 2
    col = 0
    for category, exts in categories.items():
        ttk.Label(frame, text=category, font=('Arial', 10, 'bold')).grid(row=row_offset, column=col, sticky=tk.W, pady=(10, 0))
        row_offset += 1
        for ext in exts:
            checkbox = ttk.Checkbutton(frame, text=ext, variable=selected_file_types[ext])
            checkbox.grid(row=row_offset, column=col, sticky=tk.W)
            checkbuttons[checkbox] = ext
            row_offset += 1
        row_offset = 2 if col < 2 else row_offset + len(exts) + 2
        col = (col + 1) % 3

    def on_export():
        selected = [ext for ext, var in selected_file_types.items() if var.get()]
        root.destroy()
        start_export_callback(selected)

    ttk.Button(frame, text="Export", command=on_export).grid(row=row_offset + 2, column=1, pady=(20, 0), sticky=tk.EW)

    root.mainloop()
