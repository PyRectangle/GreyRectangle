import threading
import gzip


class Region(threading.Thread):
    def __init__(self, level, number, x, y):
        threading.Thread.__init__(self)
        self.x = x
        self.y = y
        self.file = level.folder + "/region" + str(number) + "/" + str(x) + "-" + str(y) + ".rgn"
        self.loaded = False
        self.loading = False
    
    def run(self):
        self.load()

    def load(self):
        self.loading = True
        self.region = []
        file = gzip.open(self.file)
        string = list(file.read().decode())
        file.close()
        blocks = []
        count = 0
        madeData = False
        for char in string:
            number = ord(char)
            if number == 1000000:
                data = 0
                dataCount = 0
                while data != 1114111:
                    dataCount += 1
                    data = ord(string[count + dataCount])
                    if data != 1114111:
                        blocks[-1][1].append(data)
                madeData = True
            elif not madeData:
                blocks.append([number, []])
            if number == 1114111:
                madeData = False
            count += 1
        x = 0
        row = []
        for block in blocks:
            row.append(block)
            if x >= 15:
                self.region.append(row)
                x = -1
                row = []
            x += 1
        self.loaded = True
        self.loading = False

    def close(self):
        for i in range(len(self.region) - 1):
            del self.region[0]
        del self.region
        self.loaded = False
    
    def save(self):
        if self.loaded:
            file = gzip.open(self.file, "w")
            for line in self.region:
                for block in line:
                    file.write(chr(block[0]).encode())
                    if block[1] != None:
                        file.write(chr(1000000).encode())
                        for i in block[1]:
                            file.write(chr(i).encode())
                        file.write(chr(1114111).encode())
            file.close()
