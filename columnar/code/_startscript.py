import os
import sys
os.chdir(os.path.dirname(__file__))

def output(value): #Output final string to be output
    with open(r"..\output.txt", "w") as file:
        file.write(value)
        
def to_plaintext(text): #i.e. "Hello there!" to "HELLOTHERE"
    return "".join([char for char in text.upper() if char in ALPHABET])

def split_text(text):
    split = []
    for i in range(0, len(text), len(KEY)):
        split.append(text[i:i+len(KEY)])
    return split

def add_separators(text):
    return SEP.join(split_text(text))

TEXT, SEP, KEY = sys.argv[1:]
#TEXT: Enciphered text entered when 'run' was clicked
#SEP: Separator between each column when 'run' was clicked
#KEY: Entered key when 'run' was clicked
KEY = eval(KEY) #i.e. from string "[3, 1, 4, 0, 5, 2]" to list [3, 1, 4, 0, 5, 2]
SEP = {"\\n": "\n", "\\t": "\t"}.get(SEP, SEP)
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"






