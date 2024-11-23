import tkinter as tk
from tkinter import font, messagebox
from text import  * 
from theme import *  # Assuming you have theme-related functions
from file import new_file, open_file, save_file
from ai import AIFeatures  # Assuming you have AI features defined here
from insert import *
from pygments import lex
from pygments.lexers import PythonLexer, HtmlLexer, JavaLexer, JavascriptLexer, CLexer, GoLexer
from pygments.token import Token

# Supported languages and their corresponding lexers
LANGUAGES = {
    "Python": PythonLexer,
    "Java": JavaLexer,
    "Go": GoLexer,
    "HTML": HtmlLexer,
    "JavaScript": JavascriptLexer,
    "C": CLexer,
}

class SyntaxHighlightingText(tk.Text):
    def __init__(self, parent, lexer=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.lexer = lexer
        self.setup_tags()
        self.bind("<KeyRelease>", self._highlight_syntax)

    def set_language(self, language):
        """Set the language for syntax highlighting."""
        self.lexer = LANGUAGES[language]()
        self._highlight_syntax()  # Highlight the current text with the new lexer

    def _highlight_syntax(self, event=None):
        """Highlight syntax in the text widget."""
        if not self.lexer:
            return

        self.mark_set("range_start", "1.0")
        data = self.get("1.0", "end-1c")
        for token, content in lex(data, self.lexer):
            start = self.index("range_start")
            end = f"{start}+{len(content)}c"
            self.mark_set("range_start", end)

            # Apply tags based on token type
            if token in Token.Keyword:
                self.tag_add("keyword", start, end)
            elif token in Token.String:
                self.tag_add("string", start, end)
            elif token in Token.Comment:
                self.tag_add("comment", start, end)
            elif token in Token.Name.Function:
                self.tag_add("function", start, end)

    def setup_tags(self):
        """Define syntax highlighting tags."""
        self.tag_configure("keyword", foreground="blue")
        self.tag_configure("string", foreground="green")
        self.tag_configure("comment", foreground="grey")
        self.tag_configure("function", foreground="purple")











def create_menus(root, menu_bar, text_widget, default_font, update_status_bar, editor):
    # File Menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # New file - Ctrl+N
    file_menu.add_command(label="📄 New", 
                         command=lambda: new_file(text_widget, root),
                         accelerator="Ctrl+N")
    root.bind('<Control-n>', lambda event: new_file(text_widget, root))

    # Open - Ctrl+O
    file_menu.add_command(label="📂 Open", 
                         command=lambda: open_file(text_widget, root),
                         accelerator="Ctrl+O")
    root.bind('<Control-o>', lambda event: open_file(text_widget, root))

    # Save - Ctrl+S
    file_menu.add_command(label="💾 Save",
                         command=lambda: save_file(text_widget, root),
                         accelerator="Ctrl+S")
    root.bind('<Control-s>', lambda event: save_file(text_widget, root))

    # Save As - Ctrl+Shift+S
    file_menu.add_command(label="💾 Save As...",
                         command=lambda: save_as_file(text_widget, root),
                         accelerator="Ctrl+Shift+S")
    root.bind('<Control-Shift-S>', lambda event: save_as_file(text_widget, root))

    file_menu.add_separator()

    # Print - Ctrl+P
    file_menu.add_command(label="🖨️ Print",
                         command=lambda: print_file(text_widget, root),
                         accelerator="Ctrl+P")
    root.bind('<Control-p>', lambda event: print_file(text_widget, root))

    file_menu.add_separator()

    # Exit - Alt+F4
    file_menu.add_command(label="🚪 Exit",
                         command=root.quit,
                         accelerator="Alt+F4")
    
    # Language Menu
    # Language menu
    language_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Language", menu=language_menu)

    for lang in LANGUAGES.keys():
        language_menu.add_command(
            label=lang,
            command=lambda l=lang: text_widget.set_language(l)
        )

    # Edit Menu
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="✂️ Cut", command=lambda: text_widget.event_generate("<<Cut>>"), accelerator="Ctrl+X")
    edit_menu.add_command(label="📋 Copy", command=lambda: text_widget.event_generate("<<Copy>>"), accelerator="Ctrl+C")
    edit_menu.add_command(label="📌 Paste", command=lambda: text_widget.event_generate("<<Paste>>"), accelerator="Ctrl+V")
   
    # Insert Menu
    insert_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Insert", menu=insert_menu)
    insert_menu.add_command(label="🖼️ Insert Image", command=lambda: insert_image(editor))

    # Options Menu
    options_menu = tk.Menu(menu_bar, tearoff=0, bg="white", fg="black", activebackground="#f0f0f0")
    menu_bar.add_cascade(label="Options", menu=options_menu)
    
    # Font Size submenu
    font_sizes = list(range(8, 39, 2))
    font_size_menu = tk.Menu(options_menu, tearoff=0, bg="white", fg="black", activebackground="#f0f0f0")
    options_menu.add_cascade(label="📏 Font Size", menu=font_size_menu)
    
    for size in font_sizes:
        font_size_menu.add_command(
            label=str(size),
            command=lambda s=size: text_widget.configure(font=(default_font.actual()["family"], s))
        )
    
    # Font Family submenu
    font_family_menu = tk.Menu(options_menu, tearoff=0, bg="white", fg="black", activebackground="#f0f0f0")
    options_menu.add_cascade(label="🔤 Font Family", menu=font_family_menu)
    
    available_fonts = font.families()
    for family in available_fonts:
        font_family_menu.add_command(
            label=family,
            command=lambda f=family: text_widget.configure(font=(f, default_font.actual()["size"]))
        )

        # Text Alignment submenu
    align_menu = tk.Menu(options_menu, tearoff=0)
    options_menu.add_cascade(label="🖊️ Alignment", menu=align_menu)
    align_menu.add_command(label="Align Left", command=lambda: align_text("left", text_widget))
    align_menu.add_command(label="Align Center", command=lambda: align_text("center", text_widget))
    align_menu.add_command(label="Align Right", command=lambda: align_text("right", text_widget))
    align_menu.add_command(label="Justify", command=lambda: align_text("justify", text_widget))

    #Create Table 
     # Add Table submenu
    table_menu = tk.Menu(options_menu, tearoff=0, bg="white", fg="black", activebackground="#f0f0f0")
    options_menu.add_cascade(label="Create Table", menu=table_menu)
    table_menu.add_command(label="Insert Table", command=lambda: insert_table(root,text_widget))

    # Line and Paragraph Spacing submenu
    spacing_menu = tk.Menu(options_menu, tearoff=0)
    options_menu.add_cascade(label="📏 Line & Paragraph Spacing", menu=spacing_menu)
    spacing_menu.add_command(label="Single Spacing", command=lambda: set_spacing(text_widget, 1))
    spacing_menu.add_command(label="1.5 Spacing", command=lambda: set_spacing(text_widget, 1.5))
    spacing_menu.add_command(label="Double Spacing", command=lambda: set_spacing(text_widget, 2))

    # Superscript and Subscript
    options_menu.add_command(label="⁺ Superscript", command=lambda: apply_superscript(text_widget))
    options_menu.add_command(label="₋ Subscript", command=lambda: apply_subscript(text_widget))

    # Clear Formatting
    options_menu.add_command(label="❌ Clear Formatting", command=lambda: clear_formatting(text_widget))

    #Adding Bullets and Numbered Lists
    options_menu.add_command(label="Bulleted List", command=lambda: add_bullets(text_widget))
    options_menu.add_command(label="Numbered List", command=lambda: add_numbered_list(text_widget))
    
    # Theme submen
    theme_menu = tk.Menu(options_menu, tearoff=0, bg="white", fg="black", activebackground="#f0f0f0")
    options_menu.add_cascade(label="🎨 Theme", menu=theme_menu)
    
    # Add all theme options
    theme_commands = {
        "☀️ Light Mode": lambda: apply_light_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "🌙 Dark Mode": lambda: apply_dark_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "🌿 Mint Lavender": lambda: mint_lavender_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "🍑 Peach Slate": lambda: peach_slate_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "💗 Soft Pink Charcoal": lambda: soft_pink_charcoal_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "🌊 Deep Blue Neon": lambda: deep_blue_neon_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "🌑 Ebony Coral": lambda: ebony_coral_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "⚡ True Black Electric": lambda: true_black_electric_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "🫒 Olive Cream": lambda: olive_cream_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "📜 Sepia Sand": lambda: sepia_sand_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "🔥 Burnt Orange Tan": lambda: burnt_orange_tan_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "💜 Bright Purple White": lambda: bright_purple_white_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "💠 Aqua Yellow": lambda: aqua_yellow_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "💎 Ruby Soft Pink": lambda: ruby_soft_pink_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "🔷 Steel Blue Gray": lambda: steel_blue_gray_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "🌱 Sage Mint": lambda: sage_mint_theme(root, text_widget, menu_bar, file_menu, theme_menu),
        "🌫️ Charcoal Slate Blue": lambda: charcoal_slate_blue_theme(root, text_widget, menu_bar, file_menu, theme_menu)
    }
    
    for theme_name, theme_command in theme_commands.items():
        theme_menu.add_command(label=theme_name, command=theme_command)

    # View Menu
    view_menu = tk.Menu(menu_bar, tearoff=0, bg="white", fg="black", activebackground="#f0f0f0")
    menu_bar.add_cascade(label="View", menu=view_menu)
    
    # Word Wrap toggle
    wrap_var = tk.BooleanVar()
    view_menu.add_checkbutton(
        label="↩️ Word Wrap",
        variable=wrap_var,
        command=lambda: text_widget.configure(wrap="word" if wrap_var.get() else "none")
    )

    # AI Features Menu
    ai_menu = tk.Menu(menu_bar, tearoff=0, bg="white", fg="black", activebackground="#f0f0f0")
    menu_bar.add_cascade(label="🤖 AI Features", menu=ai_menu)
    
    ai_menu.add_command(label="📝 Check Grammar", command=lambda: check_grammar(text_widget))
    ai_menu.add_command(label="💡 Get Context Suggestions", command=lambda: get_context_suggestions(text_widget))
    ai_menu.add_command(label="✨ Autocomplete Current Word", command=lambda: autocomplete_current_word(text_widget))































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
        messagebox.showinfo("Suggestions", suggestion_text)
    else:
        messagebox.showinfo("Suggestions", "No suggestions found.")

def save_as_file(text_widget, root):
    """Function to implement Save As functionality"""
    from tkinter import filedialog
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"),
                                                     ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            text = text_widget.get(1.0, tk.END)
            file.write(text)

def print_file(text_widget, root):
    """Function to handle print functionality"""
    try:
        from tkinter import filedialog
        import tempfile
        import os
        import platform
        
        # Create a temporary file
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        temp_path = temp.name
        
        # Write the content to the temporary file
        with open(temp_path, 'w') as file:
            text = text_widget.get(1.0, tk.END)
            file.write(text)
        
        # Open the print dialog based on the operating system
        if platform.system() == 'Windows':
            os.startfile(temp_path, 'print')
        elif platform.system() == 'Darwin':  # macOS
            os.system(f'lpr {temp_path}')
        else:  # Linux
            os.system(f'lpr {temp_path}')
            
    except Exception as e:
        messagebox.showerror("Print Error", f"Could not print the file: {str(e)}")