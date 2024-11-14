from tkinter import filedialog, messagebox
from insert import *  # Import the insert_image function
from PIL import Image
from fpdf import FPDF
from docx import Document
from docx.shared import Inches
import os
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from fpdf import FPDF

            
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
        filetypes=[("Word documents", "*.docx"), ("PDF files", "*.pdf"), ("All files", "*.*")]
    )
    
    if file_path:
        try:
            if file_path.endswith(".docx"):
                # Save as DOCX
                doc = Document()
                
                # Insert blank paragraphs as invisible placeholders
                doc.add_paragraph()  # First blank placeholder
                doc.add_paragraph()  # Second blank placeholder
                
                # Get text content from the widget
                text_content = text_widget.get("1.0", tk.END).splitlines()
                
                # Add each line from the text widget as a paragraph
                for line in text_content:
                    if line.strip():  # Skip empty lines
                        doc.add_paragraph(line)
                
                # Save images if any
                # ... (existing image handling code here) ...

                doc.save(file_path)
                root.title(f"Beep (Text Editor) - {file_path}")
            
            elif file_path.endswith(".pdf"):
                # Save as PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                
                # Add blank lines for invisible placeholders
                pdf.cell(0, 10, "", ln=True)  # First blank placeholder
                pdf.cell(0, 10, "", ln=True)  # Second blank placeholder
                
                # Add text content from the widget
                text_content = text_widget.get("1.0", tk.END).splitlines()
                for line in text_content:
                    pdf.cell(0, 10, line, ln=True)
                
                # Save images if any
                # ... (existing image handling code here) ...

                pdf.output(file_path)
                root.title(f"Beep (Text Editor) - {file_path}")

            messagebox.showinfo("Success", f"File saved successfully as {file_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {str(e)}")

def open_file(text_widget, root):
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Word documents", "*.docx"),
            ("PDF files", "*.pdf"),
            ("All files", "*.*")
        ]
    )
    if file_path:
        try:
            if file_path.endswith(".docx"):
                doc = Document(file_path)
                text_widget.delete(1.0, "end")

                # Insert blank lines for invisible placeholders at the start
                text_widget.insert(tk.END, "\n\n")  # Two blank lines as placeholders
                
                # Load the rest of the document content
                for para in doc.paragraphs:
                    if para.text.strip():  # Avoid adding additional blank lines
                        text_widget.insert(tk.END, para.text + "\n")

                root.title(f"Beep (Text Editor) - {file_path}")
                messagebox.showinfo("Success", "Word document opened successfully!")

            elif file_path.endswith(".pdf"):
                doc = fitz.open(file_path)
                text_widget.delete(1.0, "end")

                # Add two blank lines for placeholders
                text_widget.insert(tk.END, "\n\n")

                for page_num in range(doc.page_count):
                    page = doc[page_num]
                    text = page.get_text()
                    text_widget.insert(tk.END, text + "\n")

                root.title(f"Beep (Text Editor) - {file_path}")
                messagebox.showinfo("Success", "PDF file opened successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {str(e)}")
