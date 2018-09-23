#Alex Scorza
alphabet = "abcdefghijklmnopqrstuvwxyz"
changedAlphabet = []
answer = []
while 1:
    print("Please type in the right shift (any number):")
    print("(To decode, set the shift to the shift used to encode, times -1).")
    shift = int(input(""))

    print("Please type the text that you would like to decode/encode:")
    text = input("")
    shift = shift % 26
    #This accounts for negative numbers and numbers out of the range -25 to 25, i.e 27 would be converted to 1.
    i = 0
    for x in range(0,26):
        if shift + i > 25: #If the number is above 26, it will have an error as 'alphabet' only has 26 items.
            changedAlphabet.append(alphabet[(i + shift) - 26])
        else:
            changedAlphabet.append(alphabet[i + shift])
        i = i + 1
    print(alphabet)
    print("".join(changedAlphabet))

    textPos = 0
    #'textPos' is the character of 'text' that is being checked.
    #'i' is the item of the list that is being compared to letter 'textPos' of 'text'.
    for x in range (0,len(text)):
        i = 0
        if text[textPos] in alphabet:
            while not text[textPos] == alphabet[i]:
                i = i + 1
            answer.append(changedAlphabet[i])
        else: #This is for characters that are not letters and can't be decoded or encoded.
            answer.append(text[textPos])
        textPos = textPos + 1

    final = ""
    i = 0
    for x in range(0,len(text)):
        final = (final + answer[i])
        i = i + 1
    print(final)
    print("\n"*2)
