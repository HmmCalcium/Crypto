#Alex Scorza
mode = "1"
alphabet = "abcdefghijklmnopqrstuvwxyz"

def order(word): #Converts a word to numbers depending on the order of the
    wordList = list(word.lower()) #letters - zebra becomes [4,2,1,3,0] as
    wordList = [alphabet.index(x) for x in wordList] #the order goes as
    values = ["" for x in wordList] #["a","b","e","r","z"]
    for x in range(0,len(wordList)):
        item = wordList.index(max(wordList))
        values[item] = len(wordList)-x-1
        wordList[item] = -1
    return values

def array(string,strLen): #Acts differently depending on
    if mode != "1":
        strLen = int(len(string)/strLen)
    stringConc = string #whether it's encrypting or decrypting
    stringConc += "X"*((strLen-(len(string)%strLen))%strLen) #Adds enough X's to have a length
    split = [] #that's a multiple of strLen
    for x in range(0,len(stringConc),strLen):
        split.append(stringConc[x:x+strLen])
    if mode == "1":
        return column(split,len(split[0]))
    else:
        return split

def column(lst,length):
    columns = []
    for x in range(0,length):
        columns += [""]
        for row in lst:
            columns[-1] += row[x]
    return columns

def stripall(string): #only keeps letters
    answer = ""
    for x in string.lower():
        if x in alphabet:
            answer += x
    return answer
    
while 1:
    answer = []
    plainText = stripall(input("Enter some plaintext\n> "))
    key = input("Enter a key\n> ")
    mode = input("You can 1)encrypt or 2)decrypt\n> ")
    nums = order(key)
    arrayed = array(plainText,len(key))
    if mode == "1":
        for i in range(len(nums)):
            answer += [arrayed[nums.index(i)]]
    else: #Will always do something
        for i in nums: #Put them in the correct order
            answer += [arrayed[i]]
        answer = column(answer,int(len(plainText)/len(key)))
    print("".join(answer))
