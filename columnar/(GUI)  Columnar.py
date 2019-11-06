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
import os
import subprocess
import sys

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
FG = "black"
BG = "white"
FONT = "consolas"
FSIZE = 13

def plaintext(text):
    return "".join([char for char in text.upper() if char in ALPHABET])

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

        self.mode = "encipher"

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
        self.sep_entry.insert("end", "\\n")
        tk.Label(options_frame, text="'", **style(column_sep_font_size)).grid(row=0, column=2, sticky="W")
        right_frame = tk.Frame(self, bg=BG)
        self.scroll_canvas = tk.Canvas(right_frame, width=500, bg=BG)
        self.grid_frame = tk.Frame(self, bg=BG)
        self.scrollbar = tk.Scrollbar(
            right_frame, orient="vertical", command=self.scroll_canvas.xview())
        self.scroll_canvas.configure(xscrollcommand=self.scrollbar.set)
        code_frame = tk.Frame(right_frame, bg=BG)
        tk.Label(code_frame, text="File List:", **style(FSIZE)).grid(row=0, column=0, sticky="NESW")
        tk.Label(code_frame, text="Code:", **style(FSIZE)).grid(row=0, column=1, columnspan=3, sticky="NESW")
        self.file_list = tk.Listbox(code_frame, **style(8))
        self.code_entry = tkst.ScrolledText(code_frame, width=50, height=20, **style(10))
        btn_text = ("Save", "Chdir")
        btn_cmd = ()
        self.run_btn = tk.Button(code_frame, text="Run", state="disabled", command=self.run_code, **style(11))
        for c in range(2):
            tk.Button(code_frame, text=btn_text[c], **style(11)).grid(row=2, column=c + 2, sticky="NESW")

        # Grid
        self.enter.grid(row=0, column=0, sticky="EW")
        self.output.grid(row=3, column=0, sticky="EW")
        self.under_enter_frame.grid(row=1, column=0, sticky="W", padx=10)
        self.skip_slider.grid(row=0, column=1)
        self.key_entry.grid(row=1, column=1)
        self.key_display.grid(row=0, column=3, rowspan=2, sticky="NS")
        self.sep_entry.grid(row=0, column=1, sticky="W")
        options_frame.grid(row=2, column=0)
        right_frame.grid(row=0, column=1, rowspan=4)
        self.scroll_canvas.grid(row=0, column=0, sticky="NS", pady=20)
        self.scrollbar.grid(row=0, column=1, sticky="NS", pady=20)
        code_frame.grid(row=1, column=0, sticky = "NESW")
        self.file_list.grid(row=1, column=0, rowspan=2, sticky="NS")
        self.code_entry.grid(row=1, column=1, columnspan=3)
        self.run_btn.grid(row=2, column=1, sticky="NESW")

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
        self.file_list.bind("<<ListboxSelect>>", self.load_code)

        # Initialise
        self.directory = os.path.dirname(__file__) + "\\code"
        os.chdir(self.directory)
        self.initiate_test()
        self.new_directory()

        self.mainloop()

    def new_directory(self, directory=None):
        if directory is not None:
            os.chdir(directory)
        print(os.listdir())
        for filename in [name for name in os.listdir() if not name.startswith("_")]:
            self.file_list.insert("end", filename)

    def load_code(self, event):
        lbox = event.widget
        selection = lbox.curselection()
        if len(selection) == 0:
            return
        selection = lbox.get(selection[0])
        self.code_file = CodeFile(selection, self)
        self.run_btn.config(state="normal")

    def run_code(self):
        self.code_file.run()
        print(os.getcwd())
        file = open("..\\output.txt", "r")
        text = file.read()
        file.close()
        self.output.delete("1.0", "end")
        self.output.insert("end", text)

    def initiate_test(self):
        self.enter.insert(0.0, "ARESA SXOST HEYLO IIAIE XPENG DLLTA HTFAX TENHM WX")
        self.key_entry.insert(0, "314052")
        self.set_key_from_string()

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

    def update_grid(self, event=None, key=None, mode=None):
        if mode is None:
            mode = self.mode
        self.mode = mode
        assert key is not None
        columns = len(key)
        text = self.text
        fill_len = (columns - (len(text) % columns)) % columns
        text += "X" * fill_len
        letters = [[] for _ in range(columns)]
        reordered_letters = letters[:]
        for c in range(columns):
            for r in range(c, len(text), columns):
                letters[c].append(text[r])
        if self.mode == "decipher":
            self.columns = []
            column_length = len(text) // len(key)
            for i in range(0, len(text), column_length):
                self.columns.append(text[i: i + column_length])
        elif self.mode == "encipher":
            self.columns = letters
        else:
            raise

        self.display_grid(self.mode)   ###################

    def display_grid(self, mode):
        if self.mode == "decipher":
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
                text = this_column[row]
                tk.Label(
                    self.grid_frame, text=text, **style()
                    ).grid(row=row + 2, column=column)
        clear_weight(self.grid_frame)
        for column in range(len(self.columns)):
            self.grid_frame.grid_columnconfigure(column, weight=1)
        if self.mode == "decipher":
            to_write = rotate_columns(["".join(self.columns[self.key[n]]) for n in range(len(self.columns))])
        else:
            to_write = ["".join(self.columns[n]) for n in inverted_key]
        column_sep = self.column_sep
        self.write_output(column_sep.join(to_write))
            

    def display_top_frames(self):
        for column in range(len(self.columns)):
            MoveBtn(self, self.key[column], master=self.grid_frame).grid(row=0, column=column)   ###################

    def write_output(self, *values, end="\n"):
        # print(values)
        to_write = end.join(values)
        self.output.delete("1.0", "end")
        self.output.insert("end", to_write)

    @property
    def column_sep(self):
        return self.sep_entry.get().replace("\\n", "\n").replace("\\t", "\t")
    
    @property
    def text(self):
        return plaintext(self.enter.get("1.0", "end").replace("\n", ""))
        
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


class CodeFile:
    def __init__(self, name, parent):
        self.parent = parent
        self.name = name
        self.path = os.path.dirname(__file__) + "\\code\\"  + name
        self.load()

    def save(self):
        self.code = self.parent.code_entry.get("1.0", "end")
        print(self.code)
        with open(self.path, "w") as file:
            file.write(self.code)

    def load(self):
        self.code = open(self.path, "r").read()
        self.parent.code_entry.delete("1.0", "end")
        self.parent.code_entry.insert("end", self.code)
    
    def run(self):
        args = (self.parent.text, self.parent.sep_entry.get(), self.parent.key)
        command = 'py "{}"'.format(self.path) + (' "{}"' * len(args)).format(*args)
        print(command)
        os.system(command)
        

class CodeRun:
    def create_file(code, name):
        ...

for method in dir(CodeRun):
    if not (method.startswith("__") and method.endswith("__")):
        setattr(CodeRun, method, staticmethod(getattr(CodeRun, method)))

if __name__ == "__main__":
    app = App()
