def vernam(plain, key):
    # assuming equal length
    result = ""
    for pchar, kchar in zip(plain, key):
        result += chr(ord(pchar) ^ ord(kchar))
    return result

if __name__ == "__main__":
    plain = input("Enter plain text > ")
    key = input("Enter a key > ")
    while len(key) < len(plain):
        print("Key was {} letter{}, must be at least {} letter{}".format(
            len(key), "" if len(key) == 1 else "s",
            len(plain), "" if len(plain) == 1 else "s"))
        key = input("Enter a key > ")
    if len(key) > len(plain):
        print("Removing {} letters from end of key".format(len(plain) - len(key)))
    print(vernam(plain, key))
    
