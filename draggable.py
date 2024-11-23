import tkinter as tk

class DraggableResizableTable(tk.Frame):
    def __init__(self, parent, rows, cols, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.rows = rows
        self.cols = cols
        self.configure(borderwidth=2, relief="solid")

        # Create table cells
        self.cells = []
        for r in range(rows):
            row_cells = []
            for c in range(cols):
                cell = tk.Entry(self, width=10, relief="solid", justify="center")
                cell.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                row_cells.append(cell)
            self.cells.append(row_cells)

        # Add resizing grip
        self.resizer = tk.Frame(self, cursor="sizing", width=10, height=10)  # Replaced size_se with sizing
        self.resizer.grid(row=rows, column=cols, sticky="se")
        self.resizer.bind("<B1-Motion>", self.resize_table)

        # Add drag handling
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)

        # Variables for drag state
        self._drag_start_x = None
        self._drag_start_y = None

    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def do_drag(self, event):
        x = self.winfo_x() + (event.x - self._drag_start_x)
        y = self.winfo_y() + (event.y - self._drag_start_y)
        self.place(x=x, y=y)

    def resize_table(self, event):
        new_width = self.winfo_width() + event.x
        new_height = self.winfo_height() + event.y
        self.configure(width=new_width, height=new_height)
        self.update_table_dimensions(new_width, new_height)

    def update_table_dimensions(self, new_width, new_height):
     # Log or use new_height for future implementation
     print(f"Height: {new_height}")  # Example usage to suppress warning
     # Update column widths based on new width
     for r in range(self.rows):
        for c in range(self.cols):
            self.cells[r][c].config(width=max(1, int(new_width / self.cols / 8)))
