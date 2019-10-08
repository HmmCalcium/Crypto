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


def clear_weight(frame):
    columns, rows = frame.grid_size()
    for c in range(columns):
        frame.grid_columnconfigure(c, weight=0)
    for r in range(rows):
        frame.grid_columnconfigure(r, weight=0)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg=BG)

        # Widgets
        self.enter = tkst.ScrolledText(
            self, width=60, height=10, spacing2=10, **style())

        self.under_enter_frame = tk.Frame(self, bg=BG)
        lbl_strings = ("Create range 1 to n: ", "Enter string as key: ")
        for r in range(2):
            tk.Label(
                self.under_enter_frame, text=lbl_strings[r], **style(13)
                ).grid(row=r, column=0)
        self.column_amount = tk.IntVar(self, value=1)
        self.skip_slider = tk.Scale(
            self.under_enter_frame, variable=self.column_amount, from_=1,
            to=10, orient="horizontal", relief="flat", sliderrelief="flat",
            tickinterval=9, **style(13))
        self.key_entry = tk.Entry(self.under_enter_frame, width=10, **style())
        btn_cmds = (self.set_key_from_range, self.set_key_from_string)
        for r in range(2):
            tk.Button(
                self.under_enter_frame, text="Create Key",
                **style(13), command=btn_cmds[r]).grid(row=r, column=2)
        self.key_display = tk.Label(self.under_enter_frame, **style(15))
        self.set_key("1")
        btn_strings = ("encrypt", "decrypt")
        for r in range(2):
            tk.Button(
                self.under_enter_frame, text=btn_strings[r],
                command=getattr(self, btn_strings[r]), **style(15)).grid(
                    row=r, column=3)

        self.scroll_canvas = tk.Canvas(width=300, bg="red")
        self.grid_frame = tk.Frame(self, bg=BG)
        self.scrollbar = tk.Scrollbar(
            self, orient="horizontal", command=self.scroll_canvas.xview())
        self.scroll_canvas.configure(xscrollcommand=self.scrollbar.set)

        # Grid
        self.enter.grid(row=0, column=0)

        self.under_enter_frame.grid(row=1, column=0, sticky="W", padx=50)
        self.skip_slider.grid(row=0, column=1)
        self.key_entry.grid(row=1, column=1)
        self.key_display.grid(row=0, column=3, rowspan=2, sticky="NS")

        self.scroll_canvas.grid(row=0, column=1, sticky="NESW")

        self.update_idletasks()
        width = self.scroll_canvas.winfo_width()
        height = self.scroll_canvas.winfo_height()
        self.scroll_canvas.create_window(
            (width / 2, height / 2), window=self.grid_frame,
            height=height, width=width)

        # Weights
        for r in range(2):
            self.under_enter_frame.grid_rowconfigure(r, minsize=100)
        self.under_enter_frame.grid_columnconfigure(3, minsize=200)

        # Binding
        self.grid_frame.bind("<Configure>", self.on_frame_config)

        self.mainloop()

    def encrypt(self):
        self.update_grid(key=self.key)

    def decrypt(self):
        ...

    def on_frame_config(self, event):
        self.scroll_canvas.configure(
            scrollregion=self.scroll_canvas.bbox("all"))

    def set_key(self, value):
        self.key = list(value)
        self.key_display.config(text="Key:\n'{}'".format(
            "".join(map(str, self.key))))

    def set_key_from_range(self):
        self.set_key(list(range(self.column_amount.get())))

    def set_key_from_string(self):
        enumerated = tuple(enumerate(self.key_entry.get()))
        print(enumerated)
        ordered = sorted(enumerated, key=lambda el: el[1])
        print(ordered)
        nums = [el[0] for el in ordered]
        print(nums)
        self.set_key(nums)

    def reordered_columns(self):
        new = []
        print(self.key)
        print(self.columns)

    def update_grid(self, event=None, key=None):
        assert key is not None
        columns = len(key)
        text = self.enter.get("1.0", "end").replace("\n", "").replace(" ", "")
        fill_len = (columns - (len(text) % columns)) % columns
        text += "X" * fill_len

        letters = [[] for _ in range(columns)]
        reordered_letters = letters[:]
        for c in range(columns):
            for r in range(c, len(text), columns):
                letters[c].append(text[r])
        print(letters)

        for c in range(len(self.key)):
            reordered_letters[c] = letters[self.key[c]]
        self.columns = reordered_letters

        self.display_grid()

    def display_grid(self):
        # Delete current
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        for column in range(len(self.columns)):
            tk.Label(
                    self.grid_frame, text=str(self.key[column]) + "\n", **style(20)
                    ).grid(row=0, column=column)
            for row in range(len(self.columns[column])):
                tk.Label(
                    self.grid_frame, text=self.columns[column][row], **style()
                    ).grid(row=row + 2, column=column)
        clear_weight(self.grid_frame)
        for column in range(len(self.columns)):
            self.grid_frame.grid_columnconfigure(column, weight=1)


if __name__ == "__main__":
    app = App()
