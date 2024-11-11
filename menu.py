import tkinter as tk
from theme import *  # Assuming you have theme-related functions
from file import new_file, open_file, save_file
from ai import AIFeatures  # Assuming you have AI features defined here
from insert import insert_image

# Function to create menus
def create_menus(root, menu_bar, text_widget, default_font, update_status_bar, editor):
    # File Menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=lambda: new_file(text_widget, root))
    file_menu.add_command(label="Open", command=lambda: open_file(text_widget, root))
    file_menu.add_command(label="Save", command=lambda: save_file(text_widget, root))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    # Edit Menu
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Cut", command=lambda: text_widget.event_generate("<<Cut>>"))
    edit_menu.add_command(label="Copy", command=lambda: text_widget.event_generate("<<Copy>>"))
    edit_menu.add_command(label="Paste", command=lambda: text_widget.event_generate("<<Paste>>"))

    # Insert Menu
    insert_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Insert", menu=insert_menu)
    insert_menu.add_command(label="Insert Image", command=lambda: insert_image(editor))

    # Format Menu
    format_menu = tk.Menu(menu_bar, tearoff=0, bg="white", fg="black", activebackground="#f0f0f0")
    menu_bar.add_cascade(label="Format", menu=format_menu)
    
    # Font submenu
    font_sizes = list(range(8, 39, 2))
    font_menu = tk.Menu(format_menu, tearoff=0, bg="white", fg="black", activebackground="#f0f0f0")
    format_menu.add_cascade(label="Font Size", menu=font_menu)
    
    for size in font_sizes:
        font_menu.add_command(
            label=str(size),
            command=lambda s=size: text_widget.configure(font=(default_font.actual()["family"], s))
        )
    
    # Theme Menu
    theme_menu = tk.Menu(menu_bar, tearoff=0, bg="white", fg="black", activebackground="#f0f0f0")
    menu_bar.add_cascade(label="Themes", menu=theme_menu)
    theme_menu.add_command(label="Light Mode", command=lambda: apply_light_theme(root, text_widget, menu_bar, file_menu, theme_menu))
    theme_menu.add_command(label="Dark Mode", command=lambda: apply_dark_theme(root, text_widget, menu_bar, file_menu, theme_menu))
    # Add other theme commands as needed...

    # View Menu
    view_menu = tk.Menu(menu_bar, tearoff=0, bg="white", fg="black", activebackground="#f0f0f0")
    menu_bar.add_cascade(label="View", menu=view_menu)
    
    # Word Wrap toggle
    wrap_var = tk.BooleanVar()
    view_menu.add_checkbutton(
        label="Word Wrap",
        variable=wrap_var,
        command=lambda: text_widget.configure(wrap="word" if wrap_var.get() else "none")
    )

    # AI Features Menu
    ai_menu = tk.Menu(menu_bar, tearoff=0, bg="white", fg="black", activebackground="#f0f0f0")
    menu_bar.add_cascade(label="AI Features", menu=ai_menu)
    
    ai_menu.add_command(label="Check Grammar", command=lambda: check_grammar(text_widget))
    ai_menu.add_command(label="Get Context Suggestions", command=lambda: get_context_suggestions(text_widget))
    ai_menu.add_command(label="Autocomplete Current Word", command=lambda: autocomplete_current_word(text_widget))

def check_grammar(text_widget):
    """Function to check grammar and style."""
    text = text_widget.get("1.0", tk.END)
    suggestions = AIFeatures.get_grammar_suggestions(text)
    display_suggestions(suggestions, text_widget)

def get_context_suggestions(text_widget):
    """Function to get context-aware suggestions."""
    cursor_position = text_widget.index(tk.INSERT)
    text = text_widget.get("1.0", tk.END)
    suggestions = AIFeatures.get_context_suggestions(text, cursor_position)
    display_suggestions(suggestions, text_widget)

def autocomplete_current_word(text_widget):
    """Function to autocomplete the current word."""
    cursor_position = text_widget.index(tk.INSERT)
    current_text = text_widget.get("1.0", tk.END)
    word_start = text_widget.search(r'\W', current_text[:cursor_position], stopindex=tk.END, backwards=True)
    if not word_start:
        word_start = "1.0"
    current_word = current_text[word_start:cursor_position].strip()
    
    suggestions = AIFeatures.get_smart_autocomplete(current_word, current_text)
    display_suggestions(suggestions, text_widget)

def display_suggestions(suggestions, text_widget):
    """Display suggestions in the text widget or a popup."""
    if suggestions:
        suggestion_text = "\n".join(suggestions)
        tk.messagebox.showinfo("Suggestions", suggestion_text)
    else:
        tk .messagebox.showinfo("Suggestions", "No suggestions found.")