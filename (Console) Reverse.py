#Alex Scorza
alphabet = "abcdefghijklmnopqrstuvwxyz"
while 1:
    userIn = input("Enter text to reverse\n> ")
    keep = "x" #placeholder so avoid IndexError
    punc = {}
    final = []
    
    while not keep[0] in ("y","n"):
        keep = input("Keep the positions of punctuation, spaces and capital letters?\n> ")
        
    if keep[0] == "n":
        for x in range(len(userIn)):
            final.append(userIn[-(x+1)])
            
    else:
        for x in range(0,len(userIn)):
            if not userIn[x].lower() in alphabet: #if letter
                punc[x] = userIn[x]
            else:
                final.insert(0,userIn[x].lower())
    for x in punc:
        final.insert(x,punc[x]) #Insert punctuation
    if keep[0] == "y":
        for x in range(len(userIn)):
            if userIn[x] in alphabet.upper():
                final[x] = final[x].upper()
    print("".join(final))
