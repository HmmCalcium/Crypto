#Alex Scorza April 2018
alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"
morseITU = [".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--..", #Letters
     ".----","..---","...--",".....","-....","--...","---..","----.","----"] #Numbers
def split(string): #Splits string into words but keeps punctuation
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890.-"
    answer = [""]
    for x in range(0,len(string)):
        if not string[x].lower() in alphabet:
            answer.append(string[x])
        else:
            if len(answer) > 1:
                if answer[-1][0].lower() not in alphabet:
                    answer.append("")
            answer[-1] += string[x]
    base = 0
    for x in range(0,len(answer)):
        if x+1 > len(answer):
            break
        if answer[base] != " " and answer[x] == " ":
            base = x
            while answer[x+1] == " ":
                del answer[x+1]
                answer[base] += " "
    return answer

def toMorse(string,letterSpace,wordSpace):
    answer = ""
    for letter in string.lower():#Don't use fullstops or capital letters!!!!
        if letter in alphabet:
            answer += morseITU[alphabet.index(letter)] + " "*letterSpace
        elif letter == " ":
            answer += " "*wordSpace
        else:
            answer += " "*letterSpace
    while answer[-1] == " ":
        answer = answer[:-1]
    return answer

def fromMorse(string,letterSpace):#Wordspace is irrelevant - it just checks if the no. of spaces != letterSpace
    answer = ""
    sep = split(string)
    for x in range(0,len(sep)):
        if sep[x] in morseITU:
            sep[x] = alphabet[morseITU.index(sep[x])]
    for x in range(0,len(sep)):
        if sep[x][0] == " ":
            if len(sep[x]) == letterSpace:
                sep[x] = ""
            else:
                sep[x] = " "
    for x in sep[1:]:
        sep[0] += x
    return sep[0]

##print(toMorse("Hello there",2,5))
##print(fromMorse(toMorse("Hello there",2,5),2))
while 1:
    mode = ""
    while mode not in ("1","2"):
        mode = input("You can: 1) Do morse code to text or 2) Do text to morse code\n(Don't enter fullstops or dashes!)\n> ")
    if mode == "1":
        print(fromMorse(input("Enter morse code (use '.' and '-')"),int(input("What's the spacing in between letters?\n> "))))
    else:
        print(toMorse(input("Enter normal text (avoid using fullstops and dashes)\n> "), int(input("How much space do you want between letters?\n> ")),int(input("How much spacing do you want between words?\n> "))))
