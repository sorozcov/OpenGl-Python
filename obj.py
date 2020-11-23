# Carga un archivo OBJ

class Obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.fileLines = file.read().splitlines()

        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        self.parseObject()

    def read(self):
        for line in self.fileLines:
            if line:
                try:
                    prefix, value = line.split(' ', 1)
                except:
                    continue

                if prefix == 'v': # vertices
                    self.vertices.append(list(map(float,value.split(' '))))
                elif prefix == 'vn':
                    self.normals.append(list(map(float,value.split(' '))))
                elif prefix == 'vt':
                    self.texcoords.append(list(map(float,value.split(' '))))
                elif prefix == 'f':
                    self.faces.append([list(map(int,vert.split('/'))) for vert in value.split(' ')])

    #Parse obj file properties to my class obj
    def parseObject(self):
        for line in self.fileLines:
            try:
                splitLine = line.split(None,1)
                type= splitLine[0]
                
                values=[]
                if(type[0]=='v'):

                    values=[float(val) for val in splitLine[1].split()]
                else:
                    
                    for f in splitLine[1].split():
                        if(len(f)!=0):
                            values.append([(int(val) if val!='' else 0) for val in f.split("/")])
                            
    
                    
                #You can also do list(map(float, splitLine[1])) parses completely to float
                #Now we save them in our object properties
                
                #Vertex Indexes
               
                if(type=='v'):
                    
                    self.vertices.append(values)
                #Vertex Normal Indexes    
                elif(type=='vn'):
                    self.normals.append(values)
                #Vertex Texture Indexes    
                elif(type=='vt'):
                    self.texcoords.append(values)
                elif(type=='f'):
                    
                    self.faces.append(values)
            except:
                #Manage error if needed but most likely is just a line with another info not needed right now
                pass




