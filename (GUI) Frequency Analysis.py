"""
Alex Scorza September 2018
http://www.randomtextgenerator.com/
https://www.blindtextgenerator.com/lorem-ipsum

Made for the cipher challenge but feel free to use all you lovely people.
This program decrypts substitution ciphers by finding the frequencies of letters.
You can switch words once it's done and search for words.
It returns the answer keeping punctuation, spaces and which letters are capitals.

Upcoming features: Suggestions
"""

import tkinter as tk
import tkinter.scrolledtext as tkst
import re
from warnings import warn

#Change these depending on state
WIP = True
NEW_RELEASE = False


title = "Frequency Analysis"
if WIP:
    title += " (FEATURE CURRENTLY BEING ADDED - WILL NOT WORK PROPERLY)"
if NEW_RELEASE:
    title += " (FEATURE HAS JUST BEEN ADDED - MAY BE BUGGY STILL)"

font = ("Consolas", 10)
bg = "white"
style = {"bg":bg, "font":font}
lb_colours = ("black", "#2bb516")

alphabet = "abcdefghijklmnopqrstuvwxyz" #Doesn't need to be a tuple
mono = "etaoinshrdlcumwfgypbvkjxqz" #Doesn't need to be a tuple
##alphabet = mono[:]
di = ("th", "he", "an", "in", "er", "on", "re", "ed", "nd", "ha", "at", "en")
tri = ("the", "and", "tha", "ent", "ion", "tio", "for", "nce", "has", "nce", "tis", "oft", "men")

co_nums = ("mono", "di", "tri")

changed = list(alphabet)  #Has to swap letters, must me mutable, this is default if no letters are entered

conversions = lambda: [alphabet[x]+" -> "+changed[x] for x in range(26)] #Call to update whenever
letter = lambda x: re.match(r"^[a-zA-z]$", x) is not  None  # Is letter
keep = lambda arr1, arr2: "".join([x for x in arr1 if x in arr2])
order_changed = lambda: None

def add_spaces(num):
    num = str(num) + "%"
    num = " "*(5 - len(num)) + num
    return num

def order_rating(array):
    score = 0
    for i in range(len(array)-1):
        cmp1 = array[i]
        cmp2 = array[(i+1)%len(array)]
        if cmp1 != cmp2:
            if cmp1 > cmp2:
                score -= 1
            else:
                score += 1
##            print(cmp1, cmp2)
    return int(100*score/(len(array)-1))

def regex_pos(find, string, mode): #'find' can be string or regexp. mode = 0: string, 1: regexp
    if find  ==  "":
        return []
    else:
        if mode == 0:
            return [(x, x+len(find)) for x in range(len(string)) if string[x:x+len(find)] == find] #Index string positions
        else:
            return [x.span() for x in re.compile(find).finditer(string)]
            #Index positions were regexp matches - span() is start() and end() in a tuple

def get(scrolled_text):
        return scrolled_text.get("1.0", "end")

def is_regex(string): #If vaild regexp
    try:
        re.match(string, "Any Old String")
        return True
    except:
        return False

def find_pos(line_list, regex, mode): #line_list example: ("hello there", "howdy parter")
    result = []
    for line_num in range(len(line_list)):
        for letter_pos in regex_pos(regex, line_list[line_num], mode): #example of letter_pos: (3, 6), starting and finishing index
            result +=  (("{}.{}".format(line_num+1, letter_pos[0]), "{}.{}".format(line_num+1, letter_pos[1])), )
    return tuple(result)

def set_to_letter(string):
    if string == "":
        return "" #Else, next line will cause error
    string = string[-1] #When you type another letter, set to last for ease of use
    if string[0].lower() not in alphabet:
        string = "" #Only allowed if letter
    return string.lower()

def order_dict(dictionary):
##    print("dict:", dictionary)
    #order_dict({'he': 2, 'el': 1, 'll': 1, 'lo': 1, 'ot': 1, 'th': 1, 'er': 1, 're': 1, 'ef': 1, 'fr': 1, 'ri': 1, 'ie': 1, 'en': 1, 'nd': 1})
    new = []
    for x in range(len(dictionary)):
        hi = max(tuple(dictionary.values()))
        for k, v in dictionary.items():
            if v == hi:
                new.append(k)
                del dictionary[k]
                break
    return new


def amount(string, group_size = 1): #Dictionary with numbers of each letter
##    tally = [0]*len(var_value) #[0, 0, 0, 0, 0, 0...]
    string = keep(string.lower(), alphabet)
    iterable = [string[i:i+group_size] for i in range(1+len(string)-group_size)]
##    print("iterable:", iterable)
    amounts = {}
    for el in iterable:
##        if el.lower() in var_value:
##            tally[var_value.index(el.lower())] +=  1
            if el in amounts.keys():
                amounts[el] +=  1
            else:
                amounts[el] = 1
    return amounts            

def _assign(arr, group_size = 1): #Dictionary with each letter's frequency
    new = [""]*26
    for i in range(26):
        hi = arr.index(max(arr)) #position of highest number
        new[hi] = mono[i] #Set highest to highest remaining in most frequent letters
        arr[hi] = -1 #Won't be reused but deleting will reduce list lenght and cause index error
    return new

def assign(arr, group_size = 1):
    selected_var = co_nums[group_size-1]
    var_value = globals()[selected_var]
    ordered = order_dict(arr)
##    print("ordered:", ordered)
    overlay = [""]*26
    for x in range(len(var_value[:len(ordered)])):
        for letter, i in zip(ordered[x], range(len(ordered[x]))):
##            print(var_value[x])
##            print(letter, var_value[x])
##            print(new_changed[alphabet.index(letter)], mono[x])
            
            selected_val = var_value[x][i]
##            print(selected_val)
            if letter not in overlay:
                overlay[alphabet.index(letter)], overlay[alphabet.index(selected_val)] = selected_val, letter
##            new_changed[alphabet.index(selected_val)] = letter
##    print("new changed", new_changed)
##    remaining_letters = [letter for letter in alphabet if letter not in new_changed]
####    print("remaining:", remaining_letters)
##    for letter in alphabet[len(new_changed):]:
##        if letter not in new_changed:
##            new_changed.append(letter)
##        else:
##            new_changed.append(remaining_letters.pop(0))
####    print("filled, len:", new_changed, len(new_changed))
##    print("new changed 2:", new_changed)

    new_changed = changed[:]
    for i in range(len(alphabet)):
        if overlay[i] != "":
            new_changed[i] = overlay[i]
    print(overlay)
    set1 = set(alphabet)
    set2 = set(new_changed)
##    print(alphabet, len(set1), changed, len(set2), set1 == set2, set2 - set1)
    return new_changed

def encipher(text):
    answer = ""
    for el in text:
        if el in alphabet:
            answer +=  changed[alphabet.index(el)]
        elif el in alphabet.upper():
            answer +=  changed[alphabet.index(el.lower())].upper()
        else:
            answer +=  el
    return answer

def decipher(text):
    answer = ""
    for el in text:
        if el in alphabet:
            answer +=  alphabet[changed.index(el)]
        elif el in alphabet.upper():
            answer +=  alphabet[changed.index(el.lower())].upper()
        else:
            answer +=  el
    return answer

def compare(search):
    """Allows you to find if one word can be enciphered to another with substitution.
    This makes a word into a tuple of integers - if a letter has not appeared, 
    it adds its position to numbers. Else, the position of the first
    appearance of that letter: "morning" -> (0, 1, 2, 3, 4, 3, 6) - 'n' appears twice"""
    search = keep(search.lower(), alphabet)
    numbers = [] #Answer
    done = [] #Leters that have already appeared
    for x in range(len(search)):
        if search[x] in done:
            numbers +=  [done.index(search[x])]
        else:
            numbers +=  [x]
        done.append(search[x])
    return tuple(numbers)

def find_matches(text, word): #Find matches of word to words in the text
    result = []
    find = compare(word)
    text = text.replace("\n", " ") #Remove newlines and put a space -> one line
    text = keep(text, alphabet+alphabet.upper()+" ").split()
    for x in text:
        if compare(x) == find and not x in result: #No duplicates
            result +=  [x] #If not already there, add
    return sorted(result) #Makes it easier to navigate

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg = bg)
        self.title(title)
        
        self.enter = tkst.ScrolledText(width = 70, height = 12, **style) #12 + 12 + (button height * 2) = 26
        self.enter.grid(row = 0, column = 0, columnspan = 3, sticky = "EW")
        self.answer = tkst.ScrolledText(width = 70, height = 12, **style)
        self.answer.grid(row = 2, column = 0, columnspan = 3, sticky = "EW")

        self.buttons = tk.Frame(self)
        self.buttons.grid(row = 1, column = 0, columnspan = 3, sticky = "EW")

        btn_width = 35
        btn_height = 1
        make_command = lambda size: lambda: self.set_change(get(self.enter), size)
        self.decrypt_c = tk.Button(self.buttons, text = "Decrypt Using Current", **style, width = btn_width, height = btn_height, command = self.decrypt_current)
        self.decrypt_c.grid(row = 0, column = 0, sticky = "EW")
        self.decrypt = tk.Button(self.buttons, text = "Monographs", **style, width = btn_width, height = btn_height, command = make_command(1))
        self.decrypt.grid(row = 0, column = 1, sticky = "EW")
        self.find = tk.Button(self.buttons, text = "Digraphs", **style, width = btn_width, height = btn_height, command = make_command(2))
        self.find.grid(row = 1, column = 0, sticky = "EW")
        self.find = tk.Button(self.buttons, text = "Trigraphs", **style, width = btn_width, height = btn_height, command = make_command(3))
        self.find.grid(row = 1, column = 1, sticky = "EW")
##        tk.Message(text = """Made by Alex Scorza. This project is my own work, but feel free to use and modify it!""", 
##                   **style, justify = "center", fg = "#464647", width = 200
##                   ).grid(row = 4, column = 0, rowspan = 3)
        self.stats_frame = tk.Frame()
        self.stats_frame.grid(row = 4, column = 0, rowspan = 3)
        tk.Label(self.stats_frame, **style, text = "Order rating (-100 to 100):", justify = "center").grid(row = 0, column = 0)
        self.order_lbl = tk.Label(self.stats_frame, **style, text = " 100%")
        self.order_lbl.grid(row = 0, column = 1)
        
        self.switch_frame = tk.Frame(bg = bg)
        self.switch_frame.grid(row = 4, column = 1)
        tk.Label(self.switch_frame, **style, text = "Enter two letters below to switch them").grid(row = 0, column = 0, columnspan = 2, sticky = "EW")
        self.mark_as_correct = tk.BooleanVar(self, value=True)
        tk.Checkbutton(self.switch_frame, **style, text = "Mark new letter as correct", variable = self.mark_as_correct).grid(row = 1, column = 0, columnspan = 2)
        self.letter_var1 = tk.StringVar(self)
        self.letter_var2 = tk.StringVar(self)
        self.letter_var1.trace("w", self.check_letter1)
        self.letter_var2.trace("w", self.check_letter2)
        self.letter_entry1 = tk.Entry(self.switch_frame, **style, textvariable = self.letter_var1, width = 2, justify = "center")
        self.letter_entry1.grid(row = 2, column = 0)
        self.letter_entry1.bind("<Return>", self.return_letter1)
        self.letter_entry2 = tk.Entry(self.switch_frame, **style, textvariable = self.letter_var2, width = 2, justify = "center")
        self.letter_entry2.grid(row = 2, column = 1)
        self.letter_entry2.bind("<Return>", self.return_letter2)
        self.switch_btn = tk.Button(self.switch_frame, text = "Switch", **style, state = "disabled", command = lambda: self.switch(self.letter_var1.get(), self.letter_var2.get()))
        self.switch_btn.grid(row = 3, column = 0, columnspan = 2)
        
        self.converts = tk.Listbox(self, width = 10, **style, fg = lb_colours[0], selectmode = "multiple")
        self.converts.grid(row = 0, column = 3, rowspan = 3, sticky = "NS")
        self.converts.bind("<<ListboxSelect>>", self.on_conversion_select)
        self.converts.bind("<FocusOut>", lambda event: self.converts.selection_clear(0, "end"))
        self.popup_menu = tk.Menu(self, tearoff = 0)
        self.popup_menu.add_command(label = "Toggle Marking", command = self.toggle_marked)
        self.popup_menu.add_command(label = "Select All", command = self.select_all)
        self.converts.bind("<Button-3>", self.popup)
        self.marked = [0]*26

        tk.Label(text = "Enter a word: ", **style).grid(row = 0, column = 4, sticky = "NEW", columnspan = 2)
        self.word_search = tk.StringVar(self)
        word_entry = tk.Entry(width = 17, textvariable = self.word_search, **style)
        word_entry.grid(row = 0, column = 4, sticky = "N", pady = 30)
        tk.Button(text = "→", **style, width = 2, command = lambda: self.set_letters(find_matches(get(self.enter), self.word_search.get()), self.possible)).grid(row = 0, column = 5, sticky = "NE", pady = 26)
        ###
        self.possible = tk.Listbox(height = 22)
        self.possible.grid(row = 0, rowspan = 5, column = 4, sticky = "NS", pady = 64)
        self.scrollbar = tk.Scrollbar(self, command = self.possible.yview)
        self.scrollbar.grid(row = 0, rowspan = 5, column = 5, sticky = "NSW", pady = 64)
        self.possible.config(yscrollcommand = self.scrollbar.set)
        ###
        self.possible.bind("<<ListboxSelect>>", lambda event: self.get_select(event))
        
        self.set_letters(conversions(), self.converts)

        find_frame = tk.Frame(self, bg = bg)
        self.word_option = tk.BooleanVar(find_frame, value = 0) #Needs to be accessible in self.match_finder
        word_options = ("Enter a string to match", "Enter a regexp to match")
        instruct = tk.Label(find_frame, text = word_options[0], **style)
        instruct.grid(row = 0, column = 0, columnspan = 2)
        tk.Checkbutton(find_frame, text = "Use regular expressions?", **style, variable = self.word_option, command = lambda: [instruct.config(text = word_options[self.word_option.get()]), self.match_finder()]).grid(row = 5, column = 0, columnspan = 2)
        self.to_find = tk.StringVar(self)
        self.ctrlf = tk.Entry(find_frame, **style, textvariable = self.to_find, width = 20)
        self.ctrlf.grid(row = 1, column = 0, columnspan = 2, sticky = "W", padx = 30)
        tk.Button(find_frame, text = "→", command = self.match_finder, **style, width = 2).grid(row = 1, column = 0, columnspan = 2, sticky = "E")
        self.match_num = tk.Label(find_frame, **style, text = "Matches: 0")
        self.match_num.grid(row = 3, column = 0, columnspan = 2)
        self.find_in = tk.IntVar(self, value = 0) #0 = entry, 1 = answer, 'self': accessible in class
        tk.Radiobutton(find_frame, text = "In Entry", variable = self.find_in, **style, value = 0, command = self.match_finder).grid(row = 4, column = 0)
        tk.Radiobutton(find_frame, text = "In Answer", variable = self.find_in, **style, value = 1, command = self.match_finder).grid(row = 4, column = 1)        
        find_frame.grid(row = 4, column = 3, columnspan = 2)

        self.mainloop()

    def set_mark(self, index, colour_index):
        if colour_index == "invert":
            colour_index = 1-self.marked[index]
        self.marked[index] = colour_index
        self.converts.itemconfig(index, fg = lb_colours[colour_index])

    def toggle_marked(self):
        for sel in self.converts.curselection():
##5            print(alphabet[sel])
            self.set_mark(sel, "invert")
        self.converts.selection_clear(0, "end")
    
    def select_all(self):
        self.converts.selection_set(0, "end")
    
    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def match_finder(self, *args):
        try:
            if self.find_in.get() == 0:
                self.highlight_words(self.answer, encipher(self.to_find.get()))
                self.highlight_words(self.enter, self.to_find.get())
            else:
                self.highlight_words(self.answer, self.to_find.get())
                self.highlight_words(self.enter, decipher(self.to_find.get()))
            self.ctrlf.config(fg = "black")
        except Exception as error: #Invalid regex
            self.ctrlf.config(fg = "red")
##            print(error)
        
    def highlight_words(self, widget, word): #Find all points to highlight and highlight them
        widget.tag_delete("selected")
        widget.tag_configure("selected", background = "yellow")
        positions = find_pos(get(widget).split("\n"), word, self.word_option.get())
        #'self.word_option.get()' is whether is looks for string (0/False) or regexp (1/True)
        for pos in positions:
            self.highlight(widget, *pos)
        self.match_num.config(text = "Matches: "+str(len(positions)))
        
    def highlight(self, widget, index1 = "1.0", index2 = "1.0"): #Highlight between two points
        widget.tag_add("selected", index1, index2)
        
    def get_select(self, event): #Activate when listbox item selected
        widget = event.widget
        index = widget.curselection()
        if len(index) == 1:
            val = widget.get(index).lower()
            for i in range(len(val)):
                self.switch(self.word_search.get()[i], encipher(val)[i])
            self.decrypt_current()

    def on_conversion_select(self, event):
        return
        widget = event.widget
        index = int(widget.curselection()[0])
        value = widget.get(index)
        print(index, value)
        self.letter_var1.set(value[0])
            
    def decrypt_current(self):
        self.set_answer(encipher(get(self.enter)))
        self.enter.tag_delete("selected")
        self.answer.tag_delete("selected")
    
    def set_letters(self, arr, listbox):
        listbox.delete(0, "end")
        for x in arr:
            listbox.insert("end", x)

    def set_answer(self, value):
        self.answer.delete("1.0", "end")
        self.answer.insert("end", value)
    
    def set_change(self, plain_txt, group_size):
        global changed
        tallied = amount(plain_txt, group_size)
##        print("TALLIED:", len(tallied))
##        print(alphabet, changed)
        self.reset_changed()
        changed = assign(tallied, group_size)
        self.order_lbl.config(text = add_spaces(order_rating(changed)))
##        print(tallied)
##        print(changed)
        self.set_answer(encipher(plain_txt))
        self.set_letters(conversions(), self.converts)

    def return_letter1(self, event):
        if self.letter_var1.get() == "":
            return
##        print("enter")
        self.letter_entry2.focus()

    def return_letter2(self, event):
        if self.letter_var2.get() == "":
            return
        self.switch_btn.invoke()
    
    def check_letter1(self, *args):
        self.letter_var1.set(set_to_letter(self.letter_var1.get()))
        if self.check_both():
            pass

    def check_letter2(self, *args):
        self.letter_var2.set(set_to_letter(self.letter_var2.get()))
        self.check_both()

    def check_both(self):
        vals = (self.letter_var1.get(), self.letter_var2.get())
        if "" in vals or len(set(vals)) == 1: #None empty and no duplicates
            self.switch_btn.config(state = "disabled")
            return False
        else:
            self.switch_btn.config(state = "normal")
            return True
    
    def reset_changed(self):
        changed = list(alphabet)  #Has to swap letters, must me mutable, this is default if no letters are entered
        self.decrypt_current()


    def switch(self, char1, char2): #Switch two letters in changed
        char2_index = changed.index(char2)
        changed[changed.index(char1)] = changed[changed.index(char2)]
        changed[char2_index] = char1
        self.set_letters(conversions(), self.converts)
        self.letter_var1.set("")
        self.letter_var2.set("")
        self.decrypt_current() #After switching, decrypt with new

class Graph(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Window")
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.canvas = tk.Canvas(self, width = 600, height = 300)
        self.canvas.grid(row = 0, column = 0, sticky = "NESW")
##        self.canvas.bind("<Configure>", self.on_resize)
        self.t_screen = turtle.TurtleScreen(self.canvas)
        self.t_screen.delay(0)
##        self.t_screen.tracer(0, 0)
        self.t = turtle.RawTurtle(self.t_screen)
        self.t.setpos(100, 100)
##        self.t_screen.update()
        self.canvas.addtag_all("all")
        self.mainloop()

    def on_resize(self, event):
        change_scale_x = event.width/self.canvas.width
        change_scale_y = event.height/self.canvas.height
        self.canvas.width = event.width
        self.canvas.height = event.height
        self.canvas.config(width = self.canvas.width, height = self.canvas.height)
        self.scale("all",0,0,change_scale_x, change_scale_y)        
    
if __name__ == "__main__":
    app = Main()
