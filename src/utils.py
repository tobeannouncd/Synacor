def from_bin(filename):
    memory = []

    with open(filename, 'rb') as f:
        word = f.read(2)
        while word:
            memory.append(int.from_bytes(word, 'little'))
            word = f.read(2)

    return memory
