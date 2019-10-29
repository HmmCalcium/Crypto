#Alex Scorza
def numberify(search):
    numbers=[] # Answer
    done=[] # Letters that have already appeared
    for x in range(len(search)):
        if search[x] in done:
            numbers +=  [done.index(search[x])]
        else:
            numbers +=  [x]
        done.append(search[x])
    return " ".join(map(str, numbers))


if __name__ == "__main__":
    words = ["ifmmp", "uifsf", "ipx", "bsf", "zpv", "epjoh", "upebz","aoxxizzyy"]
    comparison = numberify("committee")
    for x in range(0, len(words)):
        if comparison == numberify(words[x]):
            print(words[x])
