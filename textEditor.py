# textEditor.py
import tkinter as tk

def create_text_widget(container, default_font):
    text = tk.Text(
        container,
        wrap="none",
        undo=True,
        font=default_font,
        bg="white",
        fg="black",
        insertbackground="black",
        selectbackground="#0078d7",
        selectforeground="white",
        spacing1=2,
        spacing2=2,
        spacing3=2,
        relief="flat",
        padx=10,
        pady=5
    )
    text.pack(side="left", fill="both", expand=True)
    
    # Configure search highlighting
    text.tag_configure("search", background="yellow")
    
    return text

