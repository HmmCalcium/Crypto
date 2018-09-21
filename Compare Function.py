words = ["ifmmp", "uifsf", "ipx", "bsf", "zpv", "epjoh", "upebz","aoxxizzyy"]
def compare(search):
    numbers = []
    done = []
    x = 0
    while x < len(search):
        if search[x] in done:
            numbers.append(done.index(search[x]))
        else:
            numbers.append(x)
        done.append(search[x])
        x += 1
    for x in range(1,len(numbers)):
        numbers[0] = str(numbers[0])+str(numbers[x])
    return(numbers[0])


for x in range(0, len(words)):
    if compare("committee") == compare(words[x]):
        print(words[x])
