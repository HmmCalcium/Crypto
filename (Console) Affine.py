#Alex Scorza September 2018
alphabet = "abcdefghijklmnopqrstuvwxyz"
from math import *

while 1:
    text = input("Enter some text to encode\n> ")
    func_text = input("(With x as letter number, auto does %26, done 'from math import *', trig expects answers in radians) enter and expression\n> ")
    #i.e sin(deg(5*x)+8
    func = lambda x: eval(func_text)
    answer = ""
    for x in text:
        if x in alphabet:
            answer += alphabet[func(alphabet.index(x))%26]
        elif x in alphabet.upper():
            answer += alphabet[func(alphabet.index(x.lower()))%26].upper()
        else:
            answer += x
    print(answer)
    print("\n"*2)
        
