from tkinter import filedialog,messagebox, ttk
from PIL import Image, ImageTk
import tkinter as tk
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