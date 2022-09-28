#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from functions import *
from roofBuilder import *

class Little_House_Builder:

    #door is 0->front 1->back

    def __init__(self, level, start_x, start_y, start_z, door, direction, tree_ID,tree_data,wood_ID,wood_data,roof_ID):
        self.level = level
        self.start_x = start_x
        self.start_y = start_y
        self.start_z = start_z
        self.door = door
        self.direction = direction
        self.tree_ID = tree_ID
        self.tree_data = tree_data
        self.wood_ID = wood_ID
        self.wood_data = wood_data
        self.roof_ID = roof_ID

    def build(self):
        lv = self.level
        x = self.start_x
        y = self.start_y
        z = self.start_z
        door = self.door
        di = self.direction
        t_ID = self.tree_ID
        t_data = self.tree_data
        w_ID = self.wood_ID
        w_data = self.wood_data
        r_ID = self.roof_ID

    
        def wallX(x,z,door):
            if di==0:
                if door==0:
                    for j in range(5):
                        for i in range(3):
                            setBlock(lv, x, y+i, z+j, w_ID, w_data)
                if door==1:
                    for j in range(5):
                        for i in range(3):
                            setBlock(lv, x, y+i, z+j, w_ID, w_data)
                    setBlock(lv, x, y, z+2, 196, 0)
                    setBlock(lv, x, y+1, z+2, 196, 8)
            elif di==1:
                if door==0:
                    for j in range(5):
                        for i in range(3):
                            setBlock(lv, x+j, y+i, z, w_ID, w_data)
                if door==1:
                    for j in range(5):
                        for i in range(3):
                            setBlock(lv, x+j, y+i, z, w_ID, w_data)
                    setBlock(lv, x+2, y, z, 196, 1)
                    setBlock(lv, x+2, y+1, z, 196, 9)
        def wallZ(x,z,window):
            if di==0:
                if window==0:
                    for j in range(4):
                        for i in range(3):
                            setBlock(lv, x+j, y+i, z, w_ID, w_data)
                if window==1:
                    for j in range(4):
                        for i in range(3):
                            setBlock(lv, x+j, y+i, z, w_ID, w_data)
                    setBlock(lv, x+1, y+1, z, 85, 0)#window
                    setBlock(lv, x+2, y+1, z, 85, 0)#window
            elif di==1:
                if window==0:
                    for j in range(4):
                        for i in range(3):
                            setBlock(lv, x, y+i, z+j, w_ID, w_data)
                if window==1:
                    for j in range(4):
                        for i in range(3):
                            setBlock(lv, x, y+i, z+j, w_ID, w_data)
                    setBlock(lv, x, y+1, z+1, 85, 0)#window
                    setBlock(lv, x, y+1, z+2, 85, 0)#window
        def floor(x,z,door):
            if di==0:
                for i in range(5):
                    for j in range(4):
                        setBlock(lv, x+j, y-1, z+i, w_ID, w_data)
                if door==0:
                    setBlock(lv, x+2, y, z+1, 54, 4)
                elif door==1:
                    setBlock(lv, x+1, y, z+1, 54, 5)
            elif di==1:
                for i in range(5):
                    for j in range(4):
                        setBlock(lv, x+i, y-1, z+j, w_ID, w_data)
                if door==0:
                    setBlock(lv, x+1, y, z+2, 54, 5)
                elif door==1:
                    setBlock(lv, x+1, y, z+1, 54, 5)



        if di==0:
            for i in range(4):
                for j in range(5):
                    for k in range(5):
                        setBlock(lv,x+i,y+j,z+k,0,0)
            wallZ(x,z,0) #x,z
            wallZ(x,z+4,1) #x,z
            if door==0:
                wallX(x,z,1) #x,z,door
                wallX(x+3,z,0) #x,z,door
            elif door==1:
                wallX(x,z,0) #x,z,door
                wallX(x+3,z,1) #x,z,door
        elif di==1:
            for i in range(4):
                for j in range(5):
                    for k in range(5):
                        setBlock(lv,x+k,y+j,z+i,0,0)
            wallZ(x,z,0) #x,z
            wallZ(x+4,z,1) #x,z
            if door==0:
                wallX(x,z,1) #x,z,door
                wallX(x,z+3,0) #x,z,door
            elif door==1:
                wallX(x,z,0) #x,z,door
                wallX(x,z+3,1) #x,z,door
        floor(x,z,door)
        roof = RoofBuilder(lv, x, z, 5, y+3, di, 2, t_ID,t_data,w_ID,w_data, r_ID)
        roof.build()