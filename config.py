def save(name, value, file, mode):
    file = open(file, mode)
    write = str(name) + ":" + str(value)
    file.write(write)
    file.write("\n")
    file.close()


def read_until(file, character):
    data = ''
    byte = ''
    while byte != character:
        data += byte
        byte = file.read(1)
    return data


def load(name, file, border):
    file = open(file, "r")
    for i in range(border):
        ru = read_until(file, ":")
        if ru == name:
            ru = read_until(file, "\n")
            file.close()
            return ru
        else:
            read_until(file, "\n")
    file.close()
    return None
