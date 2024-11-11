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




def save_file(text_widget, root, editor):
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
            doc.add_paragraph(text_widget.get("1.0", tk.END).strip())
            
            # Add images to the document
            if editor.image_paths:
                doc.add_paragraph("\nImages:\n")
                for img_path in editor.image_paths:
                    doc.add_picture(img_path, width=Inches(2))
                    doc.add_paragraph(img_path)  # Store image path below the image

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

            # Clear existing image paths
            text_widget.image_paths = []  

            # Read text content from the document
            for paragraph in doc.paragraphs:
                if paragraph.text.strip() == "Images:":
                    break
                text_widget.insert(tk.END, paragraph.text + "\n")

            # Read image paths
            for paragraph in doc.paragraphs:
                if paragraph.text.strip() and paragraph.text.strip() != "Images:":
                    img_path = paragraph.text.strip()
                    text_widget.image_paths.append(img_path)

                    # Insert the image into the text widget
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