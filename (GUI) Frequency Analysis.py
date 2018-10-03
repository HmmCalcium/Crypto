#Alex Scorza September 2018
#https://www.karamasoft.com/ultimatespell/samples/longtext/longtext.aspx
#The hardware gremlin has arrived
import tkinter as tk
import tkinter.scrolledtext as tkst
from re import match

font = ("Consolas",10)
bg = "white"
style = {"bg":bg,"font":font}

alphabet = "abcdefghijklmnopqrstuvwxyz"
mono = "etaoinshrdlcumwfgypbvkjxqz" #Most to least frequent
di = ["th","he","an","in","er","on","re","ed","nd","ha","at","en"]
tri = ["the","and","tha","ent","ion","tio","for","nce","has","nce","tis","oft","men"]

changed = list(mono) #Has to swap letters, must me mutable

conversions = lambda: [alphabet[x]+" -> "+changed[x] for x in range(26)] #Call to update whenever
letter = lambda x: match(r"[a-zA-z]",x) != None #Is letter
keep = lambda arr1,arr2: "".join([x for x in arr1 if x in arr2])

def set_to_letter(string): #Widget to disable
    if string == "":
        return ""
    string = string[-1]
    if string[0].lower() not in alphabet:
        string = ""
    return string.lower()

def amount(string): #Dictionary with numbers of each letter
    amount = [0]*26
    for el in string:
        if el.lower() in alphabet:
            amount[alphabet.index(el.lower())] += 1
    return amount

def assign(arr): #Dictionary with each letter's frequency
    new = [""]*26
    for i in range(26):
        hi = arr.index(max(arr))
        new[hi] = mono[i]
        arr[hi] = -1 #Won't be reused but deleting will cause index error
    return new

def encipher(text):
    answer = ""
    for el in text:
        if el == "\n":
            answer += el
        elif el in alphabet:
            answer += changed[alphabet.index(el)]
        elif answer in alphabet.upper():
            answer += changed[alphabet.index(el.lower())].upper()
        else:
            answer += el
    return answer

def decipher(text):
    answer = ""
    for el in text:
        answer += alphabet[changed.index(el)]
    return answer

def compare(search): #Set to int array
    search = search.lower()
    numbers = [] #Answer
    done = [] #Leters that have already appeared
    for x in range(len(search)):
        if search[x] in done:
            numbers += [done.index(search[x])]
        else:
            numbers += [x]
        done.append(search[x])
    return("".join([str(x) for x in numbers]))

def find_matches(text,word): #Find matches of word to words in the text
    result = []
    find = compare(word)
    text = keep(text,alphabet+alphabet.upper()+" ").split()
    for x in text:
        if compare(x) == find and not x in result: #No duplicates
            result += [x]
    return sorted(result)

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
        self.decrypt = tk.Button(self.buttons,text = "Monographs",**style,width = btn_width,height = btn_height,command = lambda: self.set_change(self.enter.get("1.0","end")))
        self.decrypt.grid(row = 0,column = 1,sticky = "EW")
        self.find = tk.Button(self.buttons,text = "Digraphs",**style,width = btn_width,height = btn_height,command = lambda: print("Coming soon!"))
        self.find.grid(row = 1,column = 0,sticky = "EW")
        self.find = tk.Button(self.buttons,text = "Trigraphs",**style,width = btn_width,height = btn_height,command = lambda: print("Coming soon!"))
        self.find.grid(row = 1,column = 1,sticky = "EW")
        
        tk.Label(**style,text = "Enter two letters below to switch them").grid(row = 4,column = 1,columnspan = 2,sticky = "EW")
        tk.Message(text = """'Decrypt': Find letter frequencies and attempt to decrypt (start with this)
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

        self.select = tk.Button(text = "Selecting/Test Feature",command = lambda: self.highlight(self.enter,"2.6","2.11"))
        self.select.grid(row = 3,column = 4)
        ##self.enter.tag_configure("warning",background = "yellow")
        ##self.enter.insert("1.0","Lorem ipsum dolor sit amet")
        ##self.enter.tag_add("warning","1.6","1.11")

    def highlight(self,widget,index1,index2):
        widget.tag_configure("selected",background = "yellow")
        widget.tag_add("selected",index1,index2)
        lines = widget.get("1.0","end").split("\n")
        print(lines)
        for i in range(len(lines)):
            print(lines[i])
            lines[i] = tuple(keep(lines[i],alphabet+alphabet.upper()+" ").split())
        print(lines)
        
    def get_select(self,event):
        widget = event.widget
        index = widget.curselection()
        if len(index) == 1:
            val = widget.get(index).lower()
            ##print(self.word_search.get()[0],encipher(val)[0])
            for i in range(len(val)):
                self.switch(self.word_search.get()[i],encipher(val)[i])
            self.decrypt_current()
            
    def decrypt_current(self):
        self.set_answer(encipher(self.enter.get("1.0","end")))
    
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
