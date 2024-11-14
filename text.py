# Helper functions for formatting options
from tkinter import messagebox
import tkinter as tk

def align_text(alignment, text_widget):
    """Align text to left, center, right, or justify."""
    text_widget.tag_configure("align", justify=alignment)
    text_widget.tag_add("align", "1.0", "end")

def set_spacing(text_widget, spacing):
    """Set line spacing for the text."""
    text_widget.configure(spacing1=spacing * 10, spacing3=spacing * 10)

def apply_superscript(text_widget):
    """Apply superscript to selected text."""
    try:
        selected_text = text_widget.selection_get()
        text_widget.tag_configure("superscript", offset=5)
        text_widget.tag_add("superscript", "sel.first", "sel.last")
    except tk.TclError:
        messagebox.showinfo("Error", "Please select text to apply superscript.")

def apply_subscript(text_widget):
    """Apply subscript to selected text."""
    try:
        selected_text = text_widget.selection_get()
        text_widget.tag_configure("subscript", offset=-5)
        text_widget.tag_add("subscript", "sel.first", "sel.last")
    except tk.TclError:
        messagebox.showinfo("Error", "Please select text to apply subscript.")

def clear_formatting(text_widget):
    """Clear all formatting from the selected text."""
    try:
        text_widget.tag_remove("superscript", "1.0", "end")
        text_widget.tag_remove("subscript", "1.0", "end")
        text_widget.tag_remove("align", "1.0", "end")
        text_widget.configure(spacing1=0, spacing3=0)
    except tk.TclError:
        messagebox.showinfo("Error", "No formatting found to clear.")



    #Adding Bullets and Numbered Lists    

def add_bullets(text_widget):
    selected_text = text_widget.get("sel.first", "sel.last").splitlines()
    for i, line in enumerate(selected_text):
        text_widget.insert(f"sel.first + {i} lines linestart", "• ")
        
def add_numbered_list(text_widget):
    selected_text = text_widget.get("sel.first", "sel.last").splitlines()
    for i, line in enumerate(selected_text, 1):
        text_widget.insert(f"sel.first + {i - 1} lines linestart", f"{i}. ")     