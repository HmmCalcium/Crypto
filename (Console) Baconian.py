#Alex Scorza September 2018
from re import match
from warnings import warn

alphabet = "abcdefghijklmnopqrstuvwxyz" #Not a dictionary to work both ways more easily
bacon = ["aaaaa", "aaaab", "aaaba", "aaabb", "aabaa", "aabab", "aabba", "aabbb", #A-H
         "abaaa", "abaaa", "abaab", "ababa", "ababb", "abbaa", "abbab", "abbba", "abbbb",#I-Q, I is the same as J
         "baaaa", "baaab", "baaba", "baabb", "baabb", "babaa", "babab", "babba", "babbb"] #R-Z, U is the same as W

is_bacon = lambda x: match(r"^([abAB]{5})+$",x) != None #No spaces/punctuation

def only(arr1,arr2): #Remove each character of arr1 unless in arr2
    answer = ""
    for x in arr1:
        if x in arr2:
            answer += x
    return answer

def encode(text):
    if not text.isalpha():
        warn("Should be plain text")
    
    answer = ""
    for x in range(len(text)):
        if text[x] in alphabet+alphabet.upper():
            answer += bacon[alphabet.index(text[x].lower())]
    return answer.upper()

def decode(baconian): #letters, no spaces/punctuation
    if not is_bacon(baconian):
        warn("Use letters only, nothing else")
    
    answer = ""
    baconian = only(baconian.upper(),"AB")
    baconian = only(baconian,alphabet.upper())
    for x in range(0,len(baconian),5): #First letter of each group of 5 letters
        answer += alphabet[bacon.index(baconian[x:x+5].lower())]
    return answer

if __name__ == "__main__":
    while 1:
        choice = ""
        while choice not in ("1","2"):
            choice = input("You can 1)Decode or 2)Encode\n> ")
        print("\n")
        if choice == "1":
            print(decode(input("Enter baconian (must be letters only - no spaces or punctuation, not case sensetive)\n> ")))
        else: #choice == "2"
            print(encode(input("Enter plain text (preferably letters only, not case sensetive)\n> ")))
        print("\n")
