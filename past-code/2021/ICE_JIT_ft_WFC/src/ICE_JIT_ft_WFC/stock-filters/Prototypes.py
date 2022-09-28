
import numpy as np
class Prototypes:
    def __init__(self,PList=None,size=0,level=None):
        self.PList =PList
        if PList:
            self.n = len(PList)
        self.level =level
        self.size = size
        self.limitList = []

    def read(self, fn="prototypes.txt"):
        f = open(fn)
        data = f.read().splitlines()
        self.size = int(data[0])
        self.PStep = int(data[1])
        self.n = int(data[2])

        self.IDtoName ={}
        NametoID ={}
        index = -1
        self.PList = []
        bsize = self.size*self.size*self.size
        
        rc = 0
        for i in range(self.n):
            blockList= [[[0 for _ in range(self.size)] for _ in range(self.size)] for _ in range(self.size)] #Block ID list shape[y][z][x]
            for block in data[3+i*bsize:3+bsize+i*bsize]:
                _data = block.split(" ")
                # print(_data)
                _x = int(_data[0])
                _y = int(_data[1])
                _z = int(_data[2])
                if _data[3] not in NametoID :
                    index +=1
                    self.IDtoName[index] = _data[3]
                    NametoID[_data[3]] = index
                blockList[_y][_z][_x]= NametoID[_data[3]]

            prototype = Prototype(self.size,blocks=blockList)
            self.PList.append(prototype)
            self.limit = []
            self.limit.append(len(self.PList)-1)
            for k in range(3):
                flag=1
                temp=self.rotate(prototype.blocks[0])
                for kk in range(1,self.size):
                    temp=np.append(temp,self.rotate(prototype.blocks[kk]))
                temp=np.reshape(temp,(self.size,self.size,self.size))
                prototype = Prototype(self.size,blocks=temp)
                for pl in self.PList:
                    if np.allclose(pl.blocks,temp):
                        flag=0
                        # print("allclose")
                        break
                if flag:
                    # print("flag")
                    rc +=1
                    self.PList.append(prototype)
                    self.limit.append(len(self.PList)-1)
                    self.n+=1
            if len(self.limit) == 4:
                self.limitList.append(self.limit)

        # print(self.limitList)
        # print("retate: %d" % rc)
        # print(PList)
        # print(len(PList))
        # print(IDtoName)
        # print(NametoID)
        return self.size, self.PStep, self.IDtoName, NametoID, self.PList

    def rotate(self,matrix):
        l = self.size
        temp = np.zeros(shape=(l,l))
        for i in range(l):
            for j in range(l):
                k = l - 1 - j
                temp[k][i] = matrix[i][j]

        return temp

    def show(self,x,y,z,undo = 10,num = 10):
        if num ==0:
            num = self.n
        if num > self.n:
            print("n must less than %d" % self.n)
            return False
        
        space = 0
        for prototype in self.PList[:num]:
            for _y in range(self.size):
                for _z in range(self.size):
                    for _x in range(self.size):
                        self.level.setBlock(_x+x+space,_y+y,_z+z,self.IDtoName[prototype.blocks[_y][_z][_x]])
            space+=(self.size+1)

        self.level.flush()
        if undo:
            import time
            time.sleep(undo)
            print("undo")
            self.level.undo()

    # def write(self,pos,N,num):

class Prototype:
    def __init__(self,N,blocks=None,level=None):
        self.N = N
        try:
            if blocks ==None:
                self.blocks = np.zeros([self.N,self.N,self.N],dtype=int)
                print("empty blocks")
            else:
                self.blocks = blocks
                self.N =N
                self.isFloor = False
        except:
            self.blocks = blocks    
            self.N =N
            self.isFloor = False

        
if __name__ == "__main__":
    from Level import *
    level = Level(USE_BATCHING=2000)
    area = level.getBuildArea()
    x_start = area[0]
    z_start = area[1]
    x_size = area[2]
    z_size = area[3]
    x_end = x_start + x_size
    z_end = z_start + z_size
    x_center = int((x_start + x_end) /2)
    z_center = int((z_start + z_end) /2)

    prototypes = Prototypes(level=level)
    prototypes.read("prototypes.txt")
    # prototypes.show(3,4,7,num=30,undo=120)