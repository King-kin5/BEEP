from tkinter import filedialog, messagebox
from insert import *  # Import the insert_image function
from PIL import Image
from fpdf import FPDF
from docx import Document
from docx.shared import Inches
import os
from tkinter import filedialog, messagebox


            
def new_file(text_widget, root):
    if messagebox.askokcancel("New File", "Create new file? Unsaved changes will be lost."):
        text_widget.delete(1.0, "end")
        root.title("Beep (Text Editor) - New File")
        # Clear image paths
        text_widget.image_paths = []  # Clear existing image paths

def save_file(text_widget, root):
    documents_path = os.path.expanduser("~/Documents")
    file_path = filedialog.asksaveasfilename(
        initialdir=documents_path,
        defaultextension=".docx",
        filetypes=[("Word documents", "*.docx"), ("All files", "*.*")]
    )
    
    if file_path:
        try:
            doc = Document()
            # Add text content
            text_content = text_widget.get("1.0", tk.END).strip()
            doc.add_paragraph(text_content)

            # Save images
            image_counter = 0  # Counter for image naming
            for img_label in text_widget.winfo_children():
                if isinstance(img_label, tk.Label) and img_label.image:
                    # Save the original image to a specific directory
                    original_image = img_label.image  # This is the PIL Image object
                    img_path = f"image_{image_counter}.png"  # You can customize the naming
                    original_image.save(img_path)  # Save the original image
                    doc.add_paragraph(img_path)  # Add the image path to the document
                    image_counter += 1

            # Save the document
            doc.save(file_path)
            root.title(f"Beep (Text Editor) - {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")

def open_file(text_widget, root):
    file_path = filedialog.askopenfilename(
        defaultextension=".docx",
        filetypes=[
            ("Word documents", "*.docx"),
            ("All files", "*.*")
        ]
    )
    if file_path:
        try:
            doc = Document(file_path)
            text_widget.delete(1.0, "end")

            # Read text content and image paths from the document
            for paragraph in doc.paragraphs:
                text = paragraph.text.strip()
                if text and not text.startswith("image_"):  # Assuming image paths start with "image_"
                    text_widget.insert(tk.END, text + "\n")
                elif text.startswith("image_"):
                    img_path = text
                    if os.path.exists(img_path):  # Check if the image file exists
                        original_img = Image.open(img_path)
                        display_img = original_img.resize((200, 150))  # Resize for display
                        photo = ImageTk.PhotoImage(display_img)

                        img_label = tk.Label(text_widget, image=photo)
                        img_label.image = photo  # Keep a reference
                        text_widget.window_create(tk.END, window=img_label)  # Append image at the end

            root.title(f"Beep (Text Editor) - {file_path}")
            messagebox.showinfo("Success", "File opened successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {str(e)}")