def open_level(file):
    datei = open(file, "r")
    size_spawn_music_lifes = []
    for i in range(6):
        byte = ""
        text = ""
        while byte != "\t" and byte != "\n":
            text += byte
            byte = datei.read(1)
        size_spawn_music_lifes.append(text)
    size = [int(size_spawn_music_lifes[3]), int(size_spawn_music_lifes[4])]
    spawn_x = int(size_spawn_music_lifes[1])
    spawn_y = int(size_spawn_music_lifes[2])
    music = size_spawn_music_lifes[0]
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
    return [array, size, spawn_x, spawn_y, music, int(size_spawn_music_lifes[5])]


def save_level(array, file, size, spawn_x, spawn_y, music, lifes):
    datei = open(file, "w")
    text = music + "\n" +\
        str(spawn_x) + "\t" +\
        str(spawn_y) + "\n" +\
        str(size[0]) + "\t" +\
        str(size[1]) + "\n" +\
        str(lifes) + "\n"
    datei.write(text)
    for i in array:
        for ii in i:
            datei.write(str(ii))
            datei.write(";")
    datei.write("\n")
    datei.close()
