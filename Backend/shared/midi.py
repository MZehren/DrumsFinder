import functools

class HeaderChunk:
    
    def __init__(self, chunk = None):
        if chunk:
            self.header_length = int(chunk[4:8].encode('hex'),16)
            self.format = int(chunk[8:10].encode('hex'),16)
            self.n = int(chunk[10:12].encode('hex'),16)
            self.division = int(chunk[12:14].encode('hex'),16)
        else:
            self.header_length = 0
            self.format = 0
            self.n = 0
            self.division = 0
        
    def __str__(self):
        return "header_length : " + str(self.header_length) + "\nformat : " + str(self.format) + "\nn : " + str(self.n) + "\ndivision : " + str(self.division)

class TrackEvent:
    v_time = 0
    event = 0
    
    def __init__(self, chunk):
        v_time = int(chunk[4:8].encode('hex'),16)
    
class Chunk:
    id = 0
    length = 0
    data = 0
    
    def __init__(self, file):
        self.id = file.read(4)
        self.length = int(file.read(4).encode('hex'),16)
        if self.length:
            self.data = file.read(self.length)
    
    def __str__(self):
        return "id : " + str(self.id) + "\nlength : " + str(self.length) + "\ndata : " + str(self.data) + "\n"
    
    def getData(self):
        if self.id == "MThd":
            return self.getDataAsHeader()
        elif self.id =="MTrk":
            return self.getDataAsTrackEvents()
        
        
    def getDataAsHeader(self):
        format = int(self.data[0:2].encode('hex'),16)
        tracks = int(self.data[2:4].encode('hex'),16)
        division = int(self.data[4:6].encode('hex'),16)
        
        return format, tracks, division
    
    def getDataAsTrackEvents(self):
        for n in range(0, len(self.data), 4):
            delta_time = 
        
        return [(int(self.data[n:n+2].encode('hex'),16), int(self.data[n+2:n+4].encode('hex'),16)) for n in range(0, len(self.data), 4)]
    
class Midi:
       
    def __init__(self, path):
        self.read(path)
    
    def __str__(self):
        return "todo"
       
    def read(self, path):
        with open(path, 'rb') as file:
            while True:
                chunk = Chunk(file)
                if not chunk.data:
                    break
                
                print chunk.getData()
                
    def write(self, path):
        print "Not Implemented yet"
        

midi = Midi("../samples/tabs/LegionsOfTheSerpant.mid")
print midi