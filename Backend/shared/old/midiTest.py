import functools

#hand made midi parser, It should be better to use midiPython instead
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

#Express n as binary bits string with separator'
def tobits(n, _group=8, _sep='_', _pad=False):
    bits = '{0:b}'.format(n)[::-1]
    if _pad:
        bits = '{0:0{1}b}'.format(n,
                                  ((_group+len(bits)-1)//_group)*_group)[::-1]
        answer = _sep.join(bits[i:i+_group]
                                 for i in range(0, len(bits), _group))[::-1]
        answer = '0'*(len(_sep)-1) + answer
    else:
        answer = _sep.join(bits[i:i+_group]
                           for i in range(0, len(bits), _group))[::-1]
    return answer

#return the value and the number of bytes read
def getVariableLengthValue(data):
    
    i = 0
    MSB = 1
    realValue = ''
    
    while MSB:
        byte = int(data[i].encode('hex'),16)
        MSB = byte >> 7 & 1
        realValue += tobits(byte & 127, _group=7, _sep='', _pad=True )
        i += 1
    
    return int(realValue, 2), i
    
    
    
class Chunk:
    id = 0
    length = 0
    data = 0
    
    def __init__(self, file):
        self.id = file.read(4)
        if not self.id:
            return
        
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

        delta_time, n = getVariableLengthValue(self.data)
        
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
        

midi = Midi("../samples/tabs/sample.mid")
print midi