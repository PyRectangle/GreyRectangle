class Config():
    def __init__(self):
        self.FILE = "config/config.txt"
        
    def save(self, name, value, mode):
        variable = str(name) + ":" + str(value)

        file = open(self.FILE, mode)
        
        file.write(variable)
        file.write("\n")
        
        file.close()
    
    
    def read_until(self, file, character):
        data = ''
        byte = ''
        
        while byte != character:
            data += byte
            byte = file.read(1)
        
        return data
    
    
    def load(self, name, border):
        file = open(self.FILE, "r")
        
        for i in range(border):
            variable = self.read_until(file, ":")
            if variable == name:
                variable = self.read_until(file, "\n")
                
                file.close()
            
                return variable
            else:
                self.read_until(file, "\n")
        
        file.close()
        
        return None
