"""
Alex Scorza September 2018
http://www.randomtextgenerator.com/

Made for the cipher challenge but feel free to use all you lovely people.
This program decrypts substitution ciphers by finding the frequencies of letters.
You can switch words once it's done and search for words.
It returns the answer keeping punctuation, spaces and which letters are capitals.

Upcoming features:
-digraphs
-trigraphs
-highlighting words from entry to encoded in answer and vice versa
-decode/encode singe words
"""

import tkinter as tk
import tkinter.scrolledtext as tkst
import re
from warnings import warn

font = ("Consolas",10)
bg = "white"
style = {"bg":bg,"font":font}

alphabet = "abcdefghijklmnopqrstuvwxyz" #Doesn't need to be a tuple
mono = "etaoinshrdlcumwfgypbvkjxqz" #Doesn't need to be a tuple
di = ("th","he","an","in","er","on","re","ed","nd","ha","at","en")
tri = ("the","and","tha","ent","ion","tio","for","nce","has","nce","tis","oft","men")

changed = list(mono) #Has to swap letters, must me mutable, this is default if no letters are entered

conversions = lambda: [alphabet[x]+" -> "+changed[x] for x in range(26)] #Call to update whenever
letter = lambda x: re.match(r"^[a-zA-z]$",x) != None #Is letter
keep = lambda arr1,arr2: "".join([x for x in arr1 if x in arr2])
def regex_pos(regex,string):
    if regex == "":
        return []
    else:
        return [x.span() for x in re.compile(regex).finditer(string)]

def get(scrolled_text):
        return scrolled_text.get("1.0","end")

def _find_pos(line_list,find): #Find row and column of words: (0,10) would become "1.10"
    result = [] #2D
    for line_num in range(len(line_list)):
        for letter_pos in range(len(line_list[line_num])):
            if line_list[line_num][letter_pos:letter_pos+len(find)] == find:
                result += (("{}.{}".format(line_num+1,letter_pos),"{}.{}".format(line_num+1,letter_pos+len(find))),)
    return result

def find_pos(line_list,regex): #line_list example: ("hello there","howdy parter")
    result = []
    for line_num in range(len(line_list)):
        for letter_pos in regex_pos(regex,line_list[line_num]): #example of letter_pos: (3,6), starting and finishing index
            result += (("{}.{}".format(line_num+1,letter_pos[0]),"{}.{}".format(line_num+1,letter_pos[1])),)
    return tuple(result)

def set_to_letter(string):
    if string == "": 
        return "" #Else, next line will cause error
    string = string[-1] #When you type another letter, set to last for ease of use
    if string[0].lower() not in alphabet:
        string = "" #Only allowed if letter
    return string.lower()

def amount(string): #Dictionary with numbers of each letter
    amount = [0]*26 #26*zero appearances
    for el in string:
        if el.lower() in alphabet:
            amount[alphabet.index(el.lower())] += 1
    return amount

def assign(arr): #Dictionary with each letter's frequency
    new = [""]*26
    for i in range(26):
        hi = arr.index(max(arr)) #position of highest number
        new[hi] = mono[i] #Set highest to highest remaining in most frequent letters
        arr[hi] = -1 #Won't be reused but deleting will cause index error
    return new

def encipher(text): #Impure - required 'changed'
    answer = ""
    for el in text:
        if el == "\n":
            answer += el
        elif el in alphabet:
            answer += changed[alphabet.index(el)]
        elif el in alphabet.upper():
            answer += changed[alphabet.index(el.lower())].upper()
        else:
            answer += el
    return answer

def decipher(text):
    answer = ""
    for el in text:
        answer += alphabet[changed.index(el)]
    return answer

def compare(search): #Allows you to find if one word can be enciphered to another with substitution
    #This makes a word into a tuple of integers - if a letter has not appeared,
    #it adds its position to numbers. Else, the position of the first
    #appearance of that letter: "morning" -> (0,1,2,3,4,3,6) - 'n' appears twice
    search = keep(search.lower(),alphabet)
    numbers = [] #Answer
    done = [] #Leters that have already appeared
    for x in range(len(search)):
        if search[x] in done:
            numbers += [done.index(search[x])]
        else:
            numbers += [x]
        done.append(search[x])
    return tuple(numbers)

def find_matches(text,word): #Find matches of word to words in the text
    result = []
    find = compare(word)
    text = text.replace("\n"," ") #Remove newlines and put a space -> one line
    text = keep(text,alphabet+alphabet.upper()+" ").split()
    for x in text:
        if compare(x) == find and not x in result: #No duplicates
            result += [x] #If not already there, add
    return sorted(result) #Makes it easier to navigate

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config(bg = bg)
        
        self.enter = tkst.ScrolledText(width = 66,height = 12,**style) #12 + 12 + (button height * 2) = 26
        self.enter.grid(row = 0,column = 0,columnspan = 3,sticky = "EW")
        self.answer = tkst.ScrolledText(width = 66,height = 12,**style)
        self.answer.grid(row = 2,column = 0,columnspan = 3,sticky = "EW")

        self.buttons = tk.Frame(self)
        self.buttons.grid(row = 1,column = 0,columnspan = 3,sticky = "EW")

        btn_width = 33
        btn_height = 1
        self.decrypt_c = tk.Button(self.buttons,text = "Decrypt Using Current",**style,width = btn_width,height=btn_height,command = self.decrypt_current)
        self.decrypt_c.grid(row = 0,column = 0,sticky = "EW")
        self.decrypt = tk.Button(self.buttons,text = "Monographs",**style,width = btn_width,height = btn_height,command = lambda: self.set_change(get(self.enter)))
        self.decrypt.grid(row = 0,column = 1,sticky = "EW")
        self.find = tk.Button(self.buttons,text = "Digraphs",**style,width = btn_width,height = btn_height,command = lambda: print("Coming soon!"))
        self.find.grid(row = 1,column = 0,sticky = "EW")
        self.find = tk.Button(self.buttons,text = "Trigraphs",**style,width = btn_width,height = btn_height,command = lambda: print("Coming soon!"))
        self.find.grid(row = 1,column = 1,sticky = "EW")
        
        tk.Label(**style,text = "Enter two letters below to switch them").grid(row = 4,column = 1,columnspan = 2,sticky = "EW")
        tk.Message(text = """'Monographs': Find letter frequencies and attempt to decrypt (start with this)
                            'Decrypt using current': Decrypt using current conversion (list box,left)""",
                   **style,justify = "center",fg = "#464647"
                   ).grid(row = 4,column = 0,rowspan = 3)
        
        self.letter_var1 = tk.StringVar(self)
        self.letter_var2 = tk.StringVar(self)
        self.letter_var1.trace("w",self.check_letter1)
        self.letter_var2.trace("w",self.check_letter2)
        tk.Entry(**style,textvariable = self.letter_var1,width = 2,justify = "center").grid(row = 5,column = 1)
        tk.Entry(**style,textvariable = self.letter_var2,width = 2,justify = "center").grid(row = 5,column = 2)
        self.switch_btn = tk.Button(text = "Switch",**style,state = "disabled",command = lambda: self.switch(self.letter_var1.get(),self.letter_var2.get()))
        self.switch_btn.grid(row = 6,column = 1,columnspan = 2)
        
        self.converts = tk.Listbox(self,width = 10,**style)
        self.converts.grid(row = 0,column = 3,rowspan = 3,sticky = "NS")

        tk.Label(text = "Enter a word to find: ",**style).grid(row = 0,column = 4,sticky = "NEW",columnspan = 2)
        self.word_search = tk.StringVar(self)
        word_entry = tk.Entry(width = 17,textvariable = self.word_search,**style)
        word_entry.grid(row = 0,column = 4,sticky = "N",pady = 30)
        tk.Button(text = "→",**style,width = 2,command = lambda: self.set_letters(find_matches(self.enter.get("1.0","end"),self.word_search.get()),self.possible)).grid(row = 0,column = 5,sticky = "NE",pady = 26)
        
        self.possible = tk.Listbox()
        self.possible.grid(row = 0,rowspan = 5,column = 4,sticky = "NS",pady = 60)
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row = 0,rowspan = 4,column = 5,sticky = "NSW",pady = 60)
        self.possible.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.possible.yview)
        self.possible.bind("<<ListboxSelect>>",lambda event: self.get_select(event))
        
        self.set_letters(conversions(),self.converts)

        tk.Label(text = "Enter regex to match",**style).grid(row = 4,column = 4)
        self.to_find = tk.StringVar(self)
        self.to_find.trace("w",self.trace_finder)        
        self.ctrlf = tk.Entry(**style,textvariable = self.to_find)
        self.ctrlf.grid(row = 5,column = 4)
        self.match_num = tk.Label(**style,text = "Matches: 0")
        self.match_num.grid(row = 6,column = 4)

        self.find_in = tk.IntVar(self,value = 0) #0 = entry, 1 = answer
        
    def trace_finder(self,*args):
        try:
            if self.find_in.get() == 0:
                self.highlight_words(self.answer,encipher(self.to_find.get()))
                self.highlight_words(self.enter,self.to_find.get())
            else:
                self.highlight_words(self.answer,self.to_find.get())
                self.highlight_words(self.enter,decipher(self.to_find.get()))
            self.ctrlf.config(fg = "black")
        except Exception as error: #Invalid regex
            self.ctrlf.config(fg = "red")
            print(error)
    
    def highlight_words(self,widget,word): #Find all points to highlight and highlight them
        widget.tag_delete("selected")
        widget.tag_configure("selected",background = "yellow")
        positions = find_pos(get(widget).split("\n"),word)
        for pos in positions:
            self.highlight(widget,*pos)
        self.match_num.config(text = "Matches: "+str(len(positions)))
        
    def highlight(self,widget,index1 = "1.0",index2 = "1.0"): #Highlight between two points
        widget.tag_add("selected",index1,index2)
        
    def get_select(self,event): #Activate when listbox item selected
        widget = event.widget
        index = widget.curselection()
        if len(index) == 1:
            val = widget.get(index).lower()
##            print(self.word_search.get()[0],encipher(val)[0])
            for i in range(len(val)):
                self.switch(self.word_search.get()[i],encipher(val)[i])
            self.decrypt_current()
            
    def decrypt_current(self):
        self.set_answer(encipher(get(self.enter)))
    
    def set_letters(self,arr,listbox):
        listbox.delete(0,"end")
        for x in arr:
            listbox.insert("end",x)

    def set_answer(self,value):
        self.answer.delete("1.0","end")
        self.answer.insert("end",value)
    
    def set_change(self,plain_txt):
        global changed
        changed = assign(amount(plain_txt))
        self.set_answer(encipher(plain_txt))
        self.set_letters(conversions(),self.converts)
        
    def check_letter1(self,*args):
        self.letter_var1.set(set_to_letter(self.letter_var1.get()))
        self.check_both()

    def check_letter2(self,*args):
        self.letter_var2.set(set_to_letter(self.letter_var2.get()))
        self.check_both()

    def check_both(self):
        vals = (self.letter_var1.get(),self.letter_var2.get())
        if "" in vals and len(set(vals)) == 2: #None empty and no duplicates
            self.switch_btn.config(state = "disabled")
        else:
            self.switch_btn.config(state = "normal")
    
    def switch(self,char1,char2): #Switch two letters in changed
        char2_index = changed.index(char2)
        changed[changed.index(char1)] = changed[changed.index(char2)]
        changed[char2_index] = char1
        self.set_letters(conversions(),self.converts)
        self.decrypt_current()
    
if __name__ == "__main__":
    app = Main()
