from tkinter import filedialog,messagebox, ttk
from PIL import Image, ImageTk
import tkinter as tk
from draggable import DraggableResizableTable
def insert_image(text_editor):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        # Insert the image into the text widget
        original_img = Image.open(file_path)  # Open the original image
        display_img = original_img.resize((200, 150))  # Resize for display
        photo = ImageTk.PhotoImage(display_img)

        img_label = tk.Label(text_editor.text, image=photo)
        img_label.image = original_img  # Keep a reference to the original image for saving
        img_label.photo = photo  # Keep a reference to the PhotoImage to avoid garbage collection
        text_editor.text.window_create(tk.INSERT, window=img_label)  # Insert the image



def insert_table(root, text_widget):
    def create_table():
        rows = int(row_entry.get())
        cols = int(col_entry.get())
        table = DraggableResizableTable(root, rows, cols, bg="white")
        table.place(x=50, y=50)

        if not hasattr(text_widget, "tables"):
            text_widget.tables = []
        text_widget.tables.append(table)

    table_dialog = tk.Toplevel()
    table_dialog.title("Insert Table")
    tk.Label(table_dialog, text="Rows:").grid(row=0, column=0, padx=10, pady=5)
    row_entry = tk.Entry(table_dialog)
    row_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Label(table_dialog, text="Columns:").grid(row=1, column=0, padx=10, pady=5)
    col_entry = tk.Entry(table_dialog)
    col_entry.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(table_dialog, text="Create Table", command=create_table).grid(row=2, column=0, columnspan=2, pady=10)