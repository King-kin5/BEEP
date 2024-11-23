import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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
        self.bind("<KeyRelease>", self._highlight_syntax)

    def set_language(self, language):
        """Set the language for syntax highlighting."""
        self.lexer = LANGUAGES[language]()

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
