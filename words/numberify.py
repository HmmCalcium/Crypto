def numberify(text):
    numbers = [] # Answer
    done = [] # Leters that have already appeared
    for x in range(len(text)):
        if text[x] in done:
            numbers +=  [done.index(text[x])]
        else:
            numbers +=  [x]
        done.append(text[x])
    return " ".join(map(str, numbers))

if __name__ == "__main__":
    import os
    os.chdir(r"plain")
    files = ([(file, open(file, "r").readlines()) for file in os.listdir()])
    os.chdir(r"..\numerical")
    print(os.listdir())
    for name, file in files:
        print(name, file)
        numbers = []
        for line in file:
            numbers.append(numberify(line.rstrip("\n")) + "\n")
##        numbers[-1] = numbers[-1][:-1]
        print(numbers[-10:])
        with open(name, "w") as new_file:
            new_file.writelines(numbers)
    input("Completed")
        
            
