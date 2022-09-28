from numpy import *
import random
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from functions import *

class field:

    def __init__(self, level, start_x, start_y, start_z, size_x, size_z, field_type, letter_type):
            self.level = level
            self.start_x = start_x
            self.start_y = start_y
            self.start_z = start_z
            self.size_x = size_x
            self.size_z = size_z
            self.field_type = field_type
            self.letter_type = letter_type

    def build(self):
        lv = self.level
        x = self.start_x
        y = self.start_y
        z = self.start_z
        s_x = self.size_x
        s_z = self.size_z
        l_type = self.letter_type

        plant = [141,142,59]
        l_ID = [91,95,9]
        l_data = [1,11,0]
        r = random.randint(0,8)
        s = random.randint(0,2)

        if self.field_type is 0:
            for i in range(s_x):
                for j in range(s_z):
                    setBlock(lv, x+i, y, z+j, 2, 0)
                    setBlock(lv, x+i, y+1, z+j, 85, 0)
            for i in range(1, s_x-1):
                for j in range(1, s_z-1):
                    setBlock(lv, x+i, y, z+j, 60, 7)
                    #your favorite plants
                    setBlock(lv, x+i, y+1, z+j, plant[s], 7) 
                setBlock(lv, x+s_x/2, y+1, z-1, 0, 0)
            setBlock(lv, x+1, y, z+1, 9, 0)#water
            setBlock(lv, x+1, y, z+s_z-2, 9, 0)
            setBlock(lv, x+s_x-2, y, z+1, 9, 0)
            setBlock(lv, x+s_x-2, y, z+s_z-2, 9, 0)
            setBlock(lv, x+1, y+1, z+1, 0, 0)#air
            setBlock(lv, x+1, y+1, z+s_z-2, 0, 0)
            setBlock(lv, x+s_x-2, y+1, z+1, 0, 0)
            setBlock(lv, x+s_x-2, y+1, z+s_z-2, 0, 0)
            setBlock(lv, x, y+1, z+s_z/2, 0, 0)#air
            setBlock(lv, x+s_x-1, y+1, z+s_z/2, 0, 0)#air
            if s_z>9:
                setBlock(lv, x+s_x/2, y, z+s_z/2, 9, 0)#water
                setBlock(lv, x+s_x/2, y+1, z+s_z/2, 0, 0)#air

        elif self.field_type is 1:#I
            letter = [[0,0,0,0,0,0,0],[0,1,1,1,1,1,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,0,0,1,0,0,0],[0,1,1,1,1,1,0],[0,0,0,0,0,0,0]]
            for i in range(9):
                for j in range(9):
                    setBlock(lv, x+i, y, z+j, 2, 0)
                    setBlock(lv, x+i, y+1, z+j, 85, 0)
            for i in range(7):
                for j in range(7):
                    setBlock(lv, x+i+1, y, z+j+1, 60, 7)
                    if letter[j][i]==0:
                        setBlock(lv, x+i+1, y+1, z+j+1, 38, r)
                    elif letter[j][i]==1:
                        if l_type==2:
                            setBlock(lv, x+i+1, y-1, z+j+1, 89, 0) #glowstone
                            setBlock(lv, x+i+1, y, z+j+1, l_ID[l_type], l_data[l_type]) #letter
                            setBlock(lv, x+i+1, y+1, z+j+1, 0, 0) #air
                        else:
                            setBlock(lv, x+i+1, y, z+j+1, 89, 0) #glowstone
                            setBlock(lv, x+i+1, y+1, z+j+1, l_ID[l_type], l_data[l_type]) #letter
                setBlock(lv, x+9/2, y+1, z-1, 0, 0)
            setBlock(lv, x+1, y, z+1, 9, 0)#water
            setBlock(lv, x+1, y, z+7, 9, 0)
            setBlock(lv, x+7, y, z+1, 9, 0)
            setBlock(lv, x+7, y, z+7, 9, 0)
            setBlock(lv, x+1, y+1, z+1, 0, 0)#air
            setBlock(lv, x+1, y+1, z+7, 0, 0)
            setBlock(lv, x+7, y+1, z+1, 0, 0)
            setBlock(lv, x+7, y+1, z+7, 0, 0)
            setBlock(lv, x, y+1, z+s_z/2, 0, 0)#air
            setBlock(lv, x+s_x-1, y+1, z+s_z/2, 0, 0)#air
        elif self.field_type is 2:#C
            letter = [[0,0,0,0,0,0,0],[0,0,1,1,1,0,0],[0,1,0,0,0,1,0],[0,1,0,0,0,0,0],[0,1,0,0,0,1,0],[0,0,1,1,1,0,0],[0,0,0,0,0,0,0]]
            for i in range(9):
                for j in range(9):
                    setBlock(lv, x+i, y, z+j, 2, 0)
                    setBlock(lv, x+i, y+1, z+j, 85, 0)
            for i in range(7):
                for j in range(7):
                    setBlock(lv, x+i+1, y, z+j+1, 60, 7)
                    if letter[j][i]==0:
                        setBlock(lv, x+i+1, y+1, z+j+1, 38, r)
                    elif letter[j][i]==1:
                        if l_type==2:
                            setBlock(lv, x+i+1, y-1, z+j+1, 89, 0) #glowstone
                            setBlock(lv, x+i+1, y, z+j+1, l_ID[l_type], l_data[l_type]) #letter
                            setBlock(lv, x+i+1, y+1, z+j+1, 0, 0) #air
                        else:
                            setBlock(lv, x+i+1, y, z+j+1, 89, 0) #glowstone
                            setBlock(lv, x+i+1, y+1, z+j+1, l_ID[l_type], l_data[l_type]) #letter
                setBlock(lv, x+9/2, y+1, z-1, 0, 0)
            setBlock(lv, x+1, y, z+1, 9, 0)#water
            setBlock(lv, x+1, y, z+7, 9, 0)
            setBlock(lv, x+7, y, z+1, 9, 0)
            setBlock(lv, x+7, y, z+7, 9, 0)
            setBlock(lv, x+1, y+1, z+1, 0, 0)#air
            setBlock(lv, x+1, y+1, z+7, 0, 0)
            setBlock(lv, x+7, y+1, z+1, 0, 0)
            setBlock(lv, x+7, y+1, z+7, 0, 0)
            setBlock(lv, x, y+1, z+s_z/2, 0, 0)#air
            setBlock(lv, x+s_x-1, y+1, z+s_z/2, 0, 0)#air
        elif self.field_type is 3:#E
            letter = [[0,0,0,0,0,0,0],[0,1,1,1,1,1,0],[0,1,0,0,0,0,0],[0,1,1,1,1,1,0],[0,1,0,0,0,0,0],[0,1,1,1,1,1,0],[0,0,0,0,0,0,0]]
            for i in range(9):
                for j in range(9):
                    setBlock(lv, x+i, y, z+j, 2, 0)
                    setBlock(lv, x+i, y+1, z+j, 85, 0)
            for i in range(7):
                for j in range(7):
                    setBlock(lv, x+i+1, y, z+j+1, 60, 7)
                    if letter[j][i]==0:
                        setBlock(lv, x+i+1, y+1, z+j+1, 38, r)
                    elif letter[j][i]==1:
                        if l_type==2:
                            setBlock(lv, x+i+1, y-1, z+j+1, 89, 0) #glowstone
                            setBlock(lv, x+i+1, y, z+j+1, l_ID[l_type], l_data[l_type]) #letter
                            setBlock(lv, x+i+1, y+1, z+j+1, 0, 0) #air
                        else:
                            setBlock(lv, x+i+1, y, z+j+1, 89, 0) #glowstone
                            setBlock(lv, x+i+1, y+1, z+j+1, l_ID[l_type], l_data[l_type]) #letter
                setBlock(lv, x+9/2, y+1, z-1, 0, 0)
            setBlock(lv, x+1, y, z+1, 9, 0)#water
            setBlock(lv, x+1, y, z+7, 9, 0)
            setBlock(lv, x+7, y, z+1, 9, 0)
            setBlock(lv, x+7, y, z+7, 9, 0)
            setBlock(lv, x+1, y+1, z+1, 0, 0)#air
            setBlock(lv, x+1, y+1, z+7, 0, 0)
            setBlock(lv, x+7, y+1, z+1, 0, 0)
            setBlock(lv, x+7, y+1, z+7, 0, 0)
            setBlock(lv, x, y+1, z+s_z/2, 0, 0)#air
            setBlock(lv, x+s_x-1, y+1, z+s_z/2, 0, 0)#air
    
        elif self.field_type is 4:#suger
            y-=1
            for i in range(s_x):
                for j in range(s_z):
                    if i%2==0:
                        #your favorite plants
                        setBlock(lv, x+i, y, z+j, 12, 0) 
                        setBlock(lv, x+i, y+1, z+j, 83, 0) 
                        setBlock(lv, x+i, y+2, z+j, 83, 0) 
                        setBlock(lv, x+i, y+3, z+j, 83, 0) 
                    else:
                        setBlock(lv, x+i, y, z+j, 9, 0)
                        setBlock(lv, x+i, y+1, z+j, 0, 0)
                setBlock(lv, x+s_x/2, y+3, z-1, 0, 0)
            for j in range(1, s_z-1):
                setBlock(lv, x+1, y+1, z+j, 0, 0)
                setBlock(lv, x+s_x-2, y+1, z+j, 0, 0)
