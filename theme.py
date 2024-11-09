# theme.py

# Light Theme (Default)
def apply_light_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="white")
    text.config(bg="white", fg="black", insertbackground="black")
    menu_bar.config(bg="white", fg="black")
    file_menu.config(bg="white", fg="black", activebackground="#d9d9d9", activeforeground="black")
    theme_menu.config(bg="white", fg="black", activebackground="#d9d9d9", activeforeground="black")

# Dark Theme
def apply_dark_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#1c1c1c")
    text.config(bg="#1c1c1c", fg="#00ff00", insertbackground="#00ff00")
    menu_bar.config(bg="#1c1c1c", fg="#00ff00")
    file_menu.config(bg="#1c1c1c", fg="#00ff00", activebackground="#333333", activeforeground="#00ff00")
    theme_menu.config(bg="#1c1c1c", fg="#00ff00", activebackground="#333333", activeforeground="#00ff00")

# theme.py

# Soft Pastel Themes
def mint_lavender_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#e0f7fa")
    text.config(bg="#e0f7fa", fg="#5e548e", insertbackground="#0d47a1")
    menu_bar.config(bg="#e0f7fa", fg="#5e548e")
    file_menu.config(bg="#e0f7fa", fg="#5e548e", activebackground="#b2ebf2", activeforeground="#0d47a1")
    theme_menu.config(bg="#e0f7fa", fg="#5e548e", activebackground="#b2ebf2", activeforeground="#0d47a1")

def peach_slate_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#ffe0b2")
    text.config(bg="#ffe0b2", fg="#37474f", insertbackground="#ff5722")
    menu_bar.config(bg="#ffe0b2", fg="#37474f")
    file_menu.config(bg="#ffe0b2", fg="#37474f", activebackground="#ffe0b2", activeforeground="#ff5722")
    theme_menu.config(bg="#ffe0b2", fg="#37474f", activebackground="#ffe0b2", activeforeground="#ff5722")

def soft_pink_charcoal_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#f8bbd0")
    text.config(bg="#f8bbd0", fg="#212121", insertbackground="#880e4f")
    menu_bar.config(bg="#f8bbd0", fg="#212121")
    file_menu.config(bg="#f8bbd0", fg="#212121", activebackground="#f8bbd0", activeforeground="#880e4f")
    theme_menu.config(bg="#f8bbd0", fg="#212121", activebackground="#f8bbd0", activeforeground="#880e4f")

# High Contrast Dark Themes
def deep_blue_neon_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#001f3f")
    text.config(bg="#001f3f", fg="#39ff14", insertbackground="#00e5ff")
    menu_bar.config(bg="#001f3f", fg="#39ff14")
    file_menu.config(bg="#001f3f", fg="#39ff14", activebackground="#001f3f", activeforeground="#00e5ff")
    theme_menu.config(bg="#001f3f", fg="#39ff14", activebackground="#001f3f", activeforeground="#00e5ff")

def ebony_coral_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#2c2c2c")
    text.config(bg="#2c2c2c", fg="#ff6f61", insertbackground="#e91e63")
    menu_bar.config(bg="#2c2c2c", fg="#ff6f61")
    file_menu.config(bg="#2c2c2c", fg="#ff6f61", activebackground="#2c2c2c", activeforeground="#e91e63")
    theme_menu.config(bg="#2c2c2c", fg="#ff6f61", activebackground="#2c2c2c", activeforeground="#e91e63")

def true_black_electric_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#000000")
    text.config(bg="#000000", fg="#00b0ff", insertbackground="#ffeb3b")
    menu_bar.config(bg="#000000", fg="#00b0ff")
    file_menu.config(bg="#000000", fg="#00b0ff", activebackground="#000000", activeforeground="#ffeb3b")
    theme_menu.config(bg="#000000", fg="#00b0ff", activebackground="#000000", activeforeground="#ffeb3b")

# Earthy Tones
def olive_cream_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#3e4e50")
    text.config(bg="#3e4e50", fg="#ffe4b5", insertbackground="#ff7043")
    menu_bar.config(bg="#3e4e50", fg="#ffe4b5")
    file_menu.config(bg="#3e4e50", fg="#ffe4b5", activebackground="#3e4e50", activeforeground="#ff7043")
    theme_menu.config(bg="#3e4e50", fg="#ffe4b5", activebackground="#3e4e50", activeforeground="#ff7043")

def sepia_sand_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#704214")
    text.config(bg="#704214", fg="#f5deb3", insertbackground="#ffb74d")
    menu_bar.config(bg="#704214", fg="#f5deb3")
    file_menu.config(bg="#704214", fg="#f5deb3", activebackground="#704214", activeforeground="#ffb74d")
    theme_menu.config(bg="#704214", fg="#f5deb3", activebackground="#704214", activeforeground="#ffb74d")

def burnt_orange_tan_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#8b4513")
    text.config(bg="#8b4513", fg="#ffefd5", insertbackground="#d2691e")
    menu_bar.config(bg="#8b4513", fg="#ffefd5")
    file_menu.config(bg="#8b4513", fg="#ffefd5", activebackground="#8b4513", activeforeground="#d2691e")
    theme_menu.config(bg="#8b4513", fg="#ffefd5", activebackground="#8b4513", activeforeground="#d2691e")

# Bright Color Pops
def bright_purple_white_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#800080")
    text.config(bg="#800080", fg="#ffffff", insertbackground="#f4a261")
    menu_bar.config(bg="#800080", fg="#ffffff")
    file_menu.config(bg="#800080", fg="#ffffff", activebackground="#800080", activeforeground="#f4a261")
    theme_menu.config(bg="#800080", fg="#ffffff", activebackground="#800080", activeforeground="#f4a261")

def aqua_yellow_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#00ced1")
    text.config(bg="#00ced1", fg="#fffacd", insertbackground="#ff4500")
    menu_bar.config(bg="#00ced1", fg="#fffacd")
    file_menu.config(bg="#00ced1", fg="#fffacd", activebackground="#00ced1", activeforeground="#ff4500")
    theme_menu.config(bg="#00ced1", fg="#fffacd", activebackground="#00ced1", activeforeground="#ff4500")

def ruby_soft_pink_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#990000")
    text.config(bg="#990000", fg="#ffe4e1", insertbackground="#ffd700")
    menu_bar.config(bg="#990000", fg="#ffe4e1")
    file_menu.config(bg="#990000", fg="#ffe4e1", activebackground="#990000", activeforeground="#ffd700")
    theme_menu.config(bg="#990000", fg="#ffe4e1", activebackground="#990000", activeforeground="#ffd700")

# Cool & Professional Themes
def steel_blue_gray_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#4682b4")
    text.config(bg="#4682b4", fg="#e0e0e0", insertbackground="#ffffff")
    menu_bar.config(bg="#4682b4", fg="#e0e0e0")
    file_menu.config(bg="#4682b4", fg="#e0e0e0", activebackground="#4682b4", activeforeground="#ffffff")
    theme_menu.config(bg="#4682b4", fg="#e0e0e0", activebackground="#4682b4", activeforeground="#ffffff")

def sage_mint_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#b2beb5")
    text.config(bg="#b2beb5", fg="#f5fffa", insertbackground="#4f7942")
    menu_bar.config(bg="#b2beb5", fg="#4f7942")
    file_menu.config(bg="#b2beb5", fg="#4f7942", activebackground="#b2beb5", activeforeground="#4f7942")
    theme_menu.config(bg="#b2beb5", fg="#4f7942", activebackground="#b2beb5", activeforeground="#4f7942")

def charcoal_slate_blue_theme(root, text, menu_bar, file_menu, theme_menu):
    root.config(bg="#36454f")
    text.config(bg="#36454f", fg="#c0c5ce", insertbackground="#6a5acd")
    menu_bar.config(bg="#36454f", fg="#c0c5ce")
    file_menu.config(bg="#36454f", fg="#c0c5ce", activebackground="#36454f", activeforeground="#6a5acd")
    theme_menu.config(bg="#36454f", fg="#c0c5ce", activebackground="#36454f", activeforeground="#6a5acd")