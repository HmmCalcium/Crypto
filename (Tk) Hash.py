#Alex Scorza September 2018
from hashlib import *
import tkinter as tk


style = {"bg":"white", "font":("consolas",10)}

funcs = {"md5": (lambda x: md5(bytes(x,"UTF-8")).hexdigest()),
         "sha1": (lambda x: sha1(bytes(x,"UTF-8")).hexdigest()),
         "sha224": (lambda x: sha224(bytes(x,"UTF-8")).hexdigest()),
         "sha384": (lambda x: sha384(bytes(x,"UTF-8")).hexdigest()),
         "sha512": (lambda x: sha512(bytes(x,"UTF-8")).hexdigest()),
         "Python Default": (lambda x: hash(x))}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.text = tk.StringVar(self)
        self.enter = tk.Entry(self, textvariable = self.text, **style)
        self.enter.grid(row = 0, column = 0, columnspan = 3, sticky = "EW")
        for x in funcs:
            index = list(funcs.keys()).index(x)
            tk.Button(self, height = 2, text = x, command = lambda x = x: [self.answer.delete("1.0","end"),self.answer.insert("end",self._encode(x))], **style).grid(
                sticky = "EW", row = 1+(index // 3), column = index % 3)
        self.answer = tk.Text(height = 2,**style)
        self.answer.grid(row = 3, column = 0, columnspan = 3)
        
    def _encode(self,func):
        return funcs[func](self.text.get())

if __name__ == "__main__": 
    App()
