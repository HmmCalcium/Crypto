#Alex Scorza
alphabet = "abcdefghijklmnopqrstuvwxyz"
changed = "".join([alphabet[25-i] for i in range(26)])
userIn = input("Enter the text to encode\n> ")
answer = ""
for i in range(len(userIn)):
    if userIn[i] in alphabet:
        answer += changed[alphabet.index(userIn[i])]
    elif userIn[i] in alphabet.upper():
        answer += changed[alphabet.index(userIn[i].lower())].upper()
    else:
        answer += userIn[i]
print(answer)
