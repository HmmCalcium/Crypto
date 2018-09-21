alphabet = "abcdefghijklmnopqrstuvwxyz"
def pos(letter1,letter2):
    return alphabet[(alphabet.index(letter1)+alphabet.index(letter2))%len(alphabet)]

while 1:
    text = input("Enter plaintext (just letters) ").lower()
    key = " "*(len(text)+1)
    while len(key) not in range(1,len(text)):
        key = input("Enter a key (if it is shorter than the text it will be repeated) ")
    answer = ""
    for x in range(0,len(text)):
        if text[x] in alphabet:
            answer += pos(text[x],key[x%len(key)])
        else:
            answer += text[x]
    print(answer)
