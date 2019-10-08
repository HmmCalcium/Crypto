# https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter

import tkinter as tk
import tkinter.scrolledtext as tkst

FG = "black"
BG = "white"
FONT = "consolas"
FSIZE = 15


def style(size=FSIZE):
    kwargs = {"fg": FG, "bg": BG}
    if size != 0:
        kwargs["font"] = (FONT, size)
    return kwargs


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Widgets
        self.enter = tkst.ScrolledText(
            self, width=100, height=10, spacing2=10, **style())

        self.under_enter_frame = tk.Frame(self)
        self.skip_length = tk.IntVar(self, value=1)
        self.skip_slider = tk.Scale(
            self.under_enter_frame, variable=self.skip_length, from_=1, to=10,
            orient="horizontal", relief="flat", sliderrelief="flat",
            tickinterval=9, command=self.update_grid, **style(13))
        self.key_entry = tk.Entry(self.under_enter_frame, width=10, **style())

        self.scroll_canvas = tk.Canvas(height=300, bg="red")
        self.grid_frame = tk.Frame(self)
        self.scrollbar = tk.Scrollbar(self, orient="horizontal", command=self.scroll_canvas.xview())
        self.scroll_canvas.configure(xscrollcommand=self.scrollbar.set)

        # Grid
        self.enter.grid(row=0, column=0)

        self.under_enter_frame.grid(row=1, column=0)
        self.skip_slider.grid(row=0, column=0)
        self.key_entry.grid(row=1, column=0)

        self.scroll_canvas.grid(row=0, column=1, sticky="NESW")
        
        self.update_idletasks()
        width = self.scroll_canvas.winfo_width()
        height = self.scroll_canvas.winfo_height()
        self.scroll_canvas.create_window(
            (width / 2, height / 2), window=self.grid_frame,
            height=height, width=width)

        # Binding
        self.grid_frame.bind("<Configure>", self.on_frame_config)

        self.mainloop()

    def on_frame_config(self, event):
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))

    def clear_weight(self, frame):
        columns, rows = frame.grid_size()
        for c in range(columns):
            frame.grid_columnconfigure(c, weight=0)
        for r in range(rows):
            frame.grid_columnconfigure(r, weight=0)

    def update_grid(self, event=None):
        columns = self.skip_length.get()
        text = self.enter.get("1.0", "end").replace("\n", "").replace(" ", "")
        fill_len = (columns - (len(text) % columns)) % columns
        text += "X" * fill_len

        # Delete current
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        letters = [[] for _ in range(columns)]
        for c in range(columns):
            for r in range(c, len(text), columns):
                letters[c].append(text[r])
        for column in range(len(letters)):
            for row in range(len(letters[column])):
                tk.Label(
                    self.grid_frame, text=letters[column][row], **style()
                    ).grid(row=row, column=column)
        self.clear_weight(self.grid_frame)
        for column in range(len(letters)):
            self.grid_frame.grid_columnconfigure(column, weight=1)


if __name__ == "__main__":
    app = App()
