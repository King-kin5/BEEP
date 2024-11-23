# main.py
import tkinter as tk
from tkinter import ttk, font, filedialog, messagebox
from file import open_file, new_file, save_file
from theme import *  # Assuming you have theme-related functions
from textEditor import create_text_widget  # Assuming this is a function that creates a text widget
from menu import create_menus
from insert import *  # Import insert_image if needed
from program import *

class TextEditor:
    def __init__(self):
        print("Initializing TextEditor...")
        self.root = tk.Tk()
        self.root.title("Beep (Text Editor)")
        self.root.geometry("1024x768")
        
        # Initialize image paths storage
        self.image_paths = []
        
        # Set up font
        self.default_font = font.Font(
            family="Segoe UI" if "Segoe UI" in font.families() else "Helvetica",
            size=11
        )
        
        # Configure style for modern look
        self.style = ttk.Style()
        self.style.configure("Flat.TFrame", background="white")

        # Main container for text widget and scrollbars
        self.main_container = ttk.Frame(self.root, style="Flat.TFrame")
        self.main_container.pack(fill="both", expand=True)
        
        # Create the text widget
        self.text = create_text_widget(self.main_container, self.default_font)

        # Setup scrollbars
        self.setup_scrollbars()
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", anchor="w", padding=(5, 2))
        self.status_bar.pack(side="bottom", fill="x")
        
        # Create menus
        self.create_all_menus()

        # Bind events
        self.bind_events()
        print("Initialization complete.")
    
    def setup_scrollbars(self):
        """Set up vertical and horizontal scrollbars"""
        # Vertical scrollbar
        self.y_scrollbar = ttk.Scrollbar(
            self.main_container,
            orient="vertical",
            command=self.text.yview
        )
        self.y_scrollbar.pack(side="right", fill="y")
        
        # Horizontal scrollbar
        self.x_scrollbar = ttk.Scrollbar(
            self.root,
            orient="horizontal",
            command=self.text.xview
        )
        self.x_scrollbar.pack(side="bottom", fill="x")
        
        # Configure text widget scrolling
        self.text.configure(
            yscrollcommand=self.y_scrollbar.set,
            xscrollcommand=self.x_scrollbar.set
        )
    
    def update_status_bar(self, event=None):
        """Update status bar with cursor position"""
        cursor_pos = self.text.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        self.status_bar.config(text=f"Line: {line}, Column: {int(col) + 1}")
    
    def create_all_menus(self):
        """Create the menu bar"""
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        create_menus(
            self.root,
            self.menu_bar,
            self.text,
            self.default_font,
            self.update_status_bar,  # Pass the callback function
            self  # Pass the instance of TextEditor
        )
    
    def bind_events(self):
        """Bind keyboard shortcuts and cursor movement for the status bar"""
        self.root.bind('<Control-n>', lambda e: new_file(self.text, self.root))
        self.root.bind('<Control-o>', lambda e: open_file(self.text, self.root))
        self.root.bind('<Control-s>', lambda e: save_file(self.text, self.root))
        
        # Bind cursor movement to update status bar
        self.text.bind('<KeyRelease>', self.update_status_bar)
        self.text.bind('<Button-1>', self.update_status_bar)
    
    def run(self):
        """Run the main Tkinter loop"""
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting application...")
    editor = TextEditor()
    editor.run()
