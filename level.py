def open_level(file):
    datei = open(file, "r")
    size_spawn = []
    for i in range(4):
        byte = ""
        text = ""
        while byte != "\t" and byte != "\n":
            text += byte
            byte = datei.read(1)
        size_spawn.append(int(text))
    size = (size_spawn[2], size_spawn[3])
    spawn_x = size_spawn[0]
    spawn_y = size_spawn[1]
    array = []
    tmp_array = []
    text = ""
    count = 0
    while True:
        byte = datei.read(1)
        if byte == ";":
            tmp_array.append(int(text))
            text = ""
            count += 1
            if count >= size[0]:
                count = 0
                array.append(tmp_array)
                tmp_array = []
        else:
            text += byte
        if byte == "\n":
            break
    return array, size, spawn_x, spawn_y


def save_level(array, file, size, spawn_x, spawn_y):
    datei = open(file, "w")
    text = str(spawn_x) + "\t" + str(spawn_y) + "\n" + str(size[0]) + "\t" + str(size[1]) + "\n"
    datei.write(text)
    for i in array:
        for ii in i:
            datei.write(str(ii))
            datei.write(";")
    datei.write("\n")
    datei.close()
