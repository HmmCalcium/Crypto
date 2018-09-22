#Alex Scorza
alphabet = "abcdefghijklmnopqrstuvwxyz"

while 1:
    text = input("Enter some text to encode\n> ")
    func_text = input("(With x as letter number, auto does %26) enter and expression\n> ")
    #i.e (5*x)+8
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
        
