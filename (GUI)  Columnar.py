# https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
# https://crypto.interactive-maths.com/columnar-transposition-cipher.html#encrypt
# romeoromeowhereartthou
# romoeromoewheerarthtouXXX
# 01243
# tomato
# 421053
# The tomato is a plant in the nightshade family
# 1111111111
# ARESA SXOST HEYLO IIAIE XPENG DLLTA HTFAX TENHM WX, kw = potato


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

def rotate_columns(columns):
    new = []
    for i in range(len(columns[0])):
        new.append("".join([column[i] for column in columns]))
    return new

def clear_weight(frame):
    columns, rows = frame.grid_size()
    for c in range(columns):
        frame.grid_columnconfigure(c, weight=0)
    for r in range(rows):
        frame.grid_columnconfigure(r, weight=0)

def invert_key(key):
    return [key.index(c) for c in range(len(key))]

def on_change_answer(event):
    print(event.keysym)
    for key in ("BackSpace",):
        if key == event.keysym:
            return "break"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg=BG)

        # Widgets
        st_kwargs = {"width":60, "height":10, "spacing2":10}
        st_kwargs.update(style())
        self.enter = tkst.ScrolledText(self, **st_kwargs)
        self.output = tkst.ScrolledText(self, **st_kwargs)

        self.under_enter_frame = tk.Frame(self, bg=BG)
        lbl_strings = ("Create range length n: ", "Enter string as key: ")
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
                command=btn_cmds[r], **style(13)).grid(row=r, column=2)
        self.key_display = tk.Label(self.under_enter_frame, **style(15))
        self.set_key((0,))
        btn_strings = ("encipher", "decipher")
        for r in range(2):
            tk.Button(
                self.under_enter_frame, text=btn_strings[r],
                command=lambda r=r: self.update_grid(key=self.key, mode=btn_strings[r]), **style(15)).grid(
                    row=r, column=3)
        options_frame = tk.Frame(self, bg=BG)
        column_sep_font_size = 12
        tk.Label(options_frame, text="Answer column separator: '", **style(column_sep_font_size)).grid(row=0, column=0)
        self.sep_entry = tk.Entry(options_frame, width=3, **style(column_sep_font_size))
        tk.Label(options_frame, text="'", **style(column_sep_font_size)).grid(row=0, column=2, sticky="W")
        self.scroll_canvas = tk.Canvas(width=500, bg=BG)
        self.grid_frame = tk.Frame(self, bg=BG)
        self.scrollbar = tk.Scrollbar(
            self, orient="horizontal", command=self.scroll_canvas.xview())
        self.scroll_canvas.configure(xscrollcommand=self.scrollbar.set)

        # Grid
        self.enter.grid(row=0, column=0)
        self.output.grid(row=3, column=0)

        self.under_enter_frame.grid(row=1, column=0, sticky="W", padx=50)
        self.skip_slider.grid(row=0, column=1)
        self.key_entry.grid(row=1, column=1)
        self.key_display.grid(row=0, column=3, rowspan=2, sticky="NS")

        self.sep_entry.grid(row=0, column=1, sticky="W")
        options_frame.grid(row=2, column=0)
        
        self.scroll_canvas.grid(row=0, column=1, rowspan=4, sticky="NESW")

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
        self.output.bind("<Key>", on_change_answer)

        # Testing
        self.enter.insert(0.0, "ARESA SXOST HEYLO IIAIE XPENG DLLTA HTFAX TENHM WX")
        self.key_entry.insert(0, "314052")
        self.set_key_from_string()

        self.mainloop()

    def on_frame_config(self, event):
        self.scroll_canvas.configure(
            scrollregion=self.scroll_canvas.bbox("all"))

    def set_key(self, value):
        self.key = list(value)
        self.display_key()

    def display_key(self):
        self.key_display.config(text="Key:\n'{}'".format(
            "".join(map(str, self.key))))

    def set_key_from_range(self):
        self.set_key(list(range(self.column_amount.get())))

    def set_key_from_string(self):
        string = self.key_entry.get()
        ordered = sorted(string)
        new_key = []
        for i in range(len(string)):
            index = ordered.index(string[i])
            index += new_key.count(index)
            new_key.append(index)
        self.set_key(new_key)

    def update_grid(self, event=None, key=None, mode="encipher"):
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
        if mode == "decipher":
            print(text)
            self.columns = []
            column_length = len(text) // len(key)
            print(column_length)
            for i in range(0, len(text), column_length):
                self.columns.append(text[i: i + column_length])
        elif mode == "encipher":
            self.columns = letters
        else:
            raise

        self.display_grid(mode)   ###################

    def display_grid(self, mode):
        if mode == "decipher":
            def get_nth_column(column):
                return self.columns[self.key[column]]
        else:
            def get_nth_column(column):
                return self.columns[column]
        
        # Delete current
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        # print("Columns:", self.columns)
        self.display_top_frames()   ###################

        inverted_key = invert_key(self.key)
        for column in range(len(self.columns)):
            # inverted_key_value = inverted_key[column]
            this_column = get_nth_column(column)
            for row in range(len(self.columns[column])):
                text = this_column[row].upper()
                tk.Label(
                    self.grid_frame, text=text, **style()
                    ).grid(row=row + 2, column=column)
        clear_weight(self.grid_frame)
        for column in range(len(self.columns)):
            self.grid_frame.grid_columnconfigure(column, weight=1)
        if mode == "decipher":
            to_write = rotate_columns(["".join(self.columns[self.key[n]]).upper() for n in range(len(self.columns))])
        else:
            print(self.columns)
            print(["".join(self.columns[n]).upper() for n in inverted_key])
            to_write = ["".join(self.columns[n]).upper() for n in inverted_key]
        print(to_write)
        column_sep = self.sep_entry.get().replace("\\n", "\n").replace("\\t", "\t")
        print("sep:", column_sep, column_sep == "\\n")
        self.write_output(column_sep.join(to_write))
            

    def display_top_frames(self):
        for column in range(len(self.columns)):
            MoveBtn(self, self.key[column], master=self.grid_frame).grid(row=0, column=column)   ###################

    def write_output(self, *values, end="\n"):
        # print(values)
        to_write = end.join(values)
        self.output.delete("1.0", "end")
        self.output.insert("end", to_write)

class MoveBtn(tk.Frame):
    # ◀▶
    def __init__(self, parent, index, master=None):
        super().__init__(master=master, bg=BG)    ###################
        self.parent = parent
        self.index = index
        tk.Button(self, text=index, command=lambda: print("Index:", self.index), **style(20)).grid(row=0, column=0, columnspan=2)
        string = "◀▶"
        for c in range(2):
            tk.Button(self, text=string[c], command=lambda c=c: self.move((-1) ** (1 - c)), **style(9)).grid(row=1, column=c)  ###################

    def move(self, offset):
        # print(offset)
        current_pos = self.parent.key.index(self.index)
        new_pos = (current_pos + offset) % len(self.parent.key)
        # print("Index of {} in key: {}".format(self.index, self.parent.key.index(self.index)))
        # print("Switching", self.index, new_pos)
        self.parent.key[current_pos], self.parent.key[new_pos] = self.parent.key[new_pos], self.parent.key[current_pos]
        self.parent.display_key()
        self.parent.update_grid(key=self.parent.key)


if __name__ == "__main__":
    app = App()
