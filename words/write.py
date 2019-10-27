def of_len(length):
    return [word for word in lines if len(word) == length]

def write_length(length):
    with open(r"plain\\" + str(length) + ".txt", "w") as file:
        to_write = of_len(length + 1)
        if to_write == []:
            return False
        print(to_write[:10])
        file.writelines(to_write)
        return True
    
if __name__ == "__main__":
    lines = [line for line in open(r"plain\all.txt").readlines()]
    length = 2
    while write_length(length):
        length += 1
    print(length)
