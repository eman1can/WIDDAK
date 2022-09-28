#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from functions import *
from roofBuilder import *

class Store_Builder:

    #door is 0->front 1->back

    def __init__(self, level, start_x, start_y, start_z, door, direction,tree_ID,tree_data,wood_ID,wood_data,roof_ID):
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
        t_ID =self.tree_ID
        t_data =self.tree_data
        w_ID = self.wood_ID
        w_data = self.wood_data
        r_ID = self.roof_ID
        d = 10
        w = 9


        def wallX(x,y,z,door):
            if di==0:
                for j in range(10): #line_W
                    setBlock(lv, x, y, z + j, 4, 0)#stone
                    if(j==0 or j==3 or j==6 or j==9):
                        for k in range(1,5): #line_H
                            setBlock(lv,x,y+k,z+j,t_ID,t_data)#black
                    else:
                        if(door==1):
                            if(j==1 or j==4 or j==7):
                                setBlock(lv,x,y,z+j,196,0)#door
                                setBlock(lv,x,y+1,z+j,196,8)#door
                            if(j==2 or j==5 or j==8):
                                setBlock(lv,x,y,z+j,196,7)#door
                                setBlock(lv,x,y+1,z+j,196,10)#door
                            else:
                                for k in range(2,6): #line_H
                                    if k==3:
                                        setBlock(lv,x,y+k,z+j,t_ID,t_data)#black
                                    else:
                                        setBlock(lv,x,y+k,z+j,w_ID,w_data)#red
                            for k in range(2,6): #line_H
                                if k==3:
                                    setBlock(lv,x,y+k,z+j,t_ID,t_data)#black
                                else:
                                    setBlock(lv,x,y+k,z+j,w_ID,w_data)#red
                        else:
                            for k in range(1,6): #line_H
                                if k==2:
                                    setBlock(lv,x,y+k,z+j,t_ID,t_data)#black
                                else:
                                    setBlock(lv,x,y+k,z+j,w_ID,w_data)#red
            elif di==1:
                for j in range(10): #line_W
                    setBlock(lv, x+j, y, z, 4, 0)#stone
                    if(j==0 or j==3 or j==6 or j==9):
                        for k in range(1,5): #line_H
                            setBlock(lv,x+j,y+k,z,t_ID,t_data)#black
                    else:
                        if(door==1):
                            if(j==1 or j==4 or j==7):
                                setBlock(lv,x+j,y,z,196,1)#door
                                setBlock(lv,x+j,y+1,z,196,9)#door
                            if(j==2 or j==5 or j==8):
                                setBlock(lv,x+j,y,z,196,4)#door
                                setBlock(lv,x+j,y+1,z,196,12)#door
                            else:
                                for k in range(2,6): #line_H
                                    if k==3:
                                        setBlock(lv,x+j,y+k,z,t_ID,t_data)#black
                                    else:
                                        setBlock(lv,x+j,y+k,z,w_ID,w_data)#red
                            for k in range(2,6): #line_H
                                if k==3:
                                    setBlock(lv,x+j,y+k,z,t_ID,t_data)#black
                                else:
                                    setBlock(lv,x+j,y+k,z,w_ID,w_data)#red
                        else:
                            for k in range(1,6): #line_H
                                if k==2:
                                    setBlock(lv,x+j,y+k,z,t_ID,t_data)#black
                                else:
                                    setBlock(lv,x+j,y+k,z,w_ID,w_data)#red

        def wallZ(x,y,z):
            if di==0:
                for j in range(9): #line_W
                    setBlock(lv, x + j, y, z, 4, 0)#rstone
                    if(j==0 or j==4 or j==8):
                        for k in range(1,6): #line_H
                            setBlock(lv, x + j, y + k, z, t_ID, t_data)#black
                    else:
                        for k in range(1,6): #line_H
                            if k==3:
                                setBlock(lv, x + j, y + k, z, t_ID, t_data)#black
                            else:
                                setBlock(lv, x + j, y + k, z, w_ID,w_data)#white
            elif di==1:   
                for j in range(9): #line_W
                    setBlock(lv, x, y, z+j, 4, 0)#rstone
                    if(j==0 or j==4 or j==8):
                        for k in range(1,6): #line_H
                            setBlock(lv, x, y + k, z+j, t_ID, t_data)#black
                    else:
                        for k in range(1,6): #line_H
                            if k==3:
                                setBlock(lv, x, y + k, z+j, t_ID, t_data)#black
                            else:
                                setBlock(lv, x, y + k, z+j, w_ID,w_data)#white

        def floor(x,y,z,door):
            if di==0:
                if door==0:
                    for i in range(0,8):
                        for j in range(1,9):
                            if i==0 or i==1:
                                setBlock(lv, x+i, y-1, z+j, 1, 0)#floor
                            elif i==2:
                                setBlock(lv, x+i, y, z+j, 126, 0)
                            elif i==7:
                                setBlock(lv, x+i, y+1, z+j, 47, 0)
                                setBlock(lv, x+i, y+2, z+j, 47, 0)
                                setBlock(lv, x+i, y+3, z+j, 54, 0)
                                setBlock(lv, x+i, y+4, z+j, 54, 0)
                            else:
                                setBlock(lv, x+i, y, z+j, 5, 0)#floor
                elif door==1:
                    for i in range(0,8):
                        for j in range(1,9):
                            if i==8 or i==7:
                                setBlock(lv, x+i, y-1, z+j, 1, 0)#floor
                            elif i==6:
                                setBlock(lv, x+i, y, z+j, 126, 0)
                            elif i==1:
                                setBlock(lv, x+i, y+1, z+j, 47, 0)
                                setBlock(lv, x+i, y+2, z+j, 47, 0)
                                setBlock(lv, x+i, y+3, z+j, 54, 0)
                                setBlock(lv, x+i, y+4, z+j, 54, 0)
                            else:
                                setBlock(lv, x+i, y, z+j, 5, 0)#floor
                setBlock(lv,x+1,y+5,z+1,89,0)#glowStone
                setBlock(lv,x+1,y+2,z+1,89,0)#glowStone
                setBlock(lv,x+7,y+5,z+1,89,0)#glowStone
                setBlock(lv,x+1,y+5,z+8,89,0)#glowStone
                setBlock(lv,x+1,y+2,z+8,89,0)#glowStone
                setBlock(lv,x+7,y+5,z+8,89,0)#glowStone
            elif di==1:
                if door==0:
                    for i in range(0,8):
                        for j in range(1,9):
                            if i==0 or i==1:
                                setBlock(lv, x+j, y-1, z+i, 1, 0)#floor
                            elif i==2:
                                setBlock(lv, x+j, y, z+i, 126, 0)#floor
                            elif i==7:
                                setBlock(lv, x+j, y+1, z+i, 47, 0)
                                setBlock(lv, x+j, y+2, z+i, 47, 0)
                                setBlock(lv, x+j, y+3, z+i, 54, 0)
                                setBlock(lv, x+j, y+4, z+i, 54, 0)
                            else:
                                setBlock(lv, x+j, y, z+i, 5, 0)#floor
                elif door==1:
                    for i in range(0,8): 
                        for j in range(1,9):
                            if i==8 or i==7:
                                setBlock(lv, x+j, y-1, z+i, 1, 0)#floor
                            elif i==6:
                                setBlock(lv, x+j, y, z+i, 126, 0)
                            elif i==1:
                                setBlock(lv, x+j, y+1, z+i, 47, 0)
                                setBlock(lv, x+j, y+2, z+i, 47, 0)
                                setBlock(lv, x+j, y+3, z+i, 54, 0)
                                setBlock(lv, x+j, y+4, z+i, 54, 0)
                            else:
                                setBlock(lv, x+j, y, z+i, 5, 0)#floor
                setBlock(lv,x+1,y+5,z+1,89,0)#glowStone
                setBlock(lv,x+1,y+2,z+1,89,0)#glowStone
                setBlock(lv,x+1,y+5,z+7,89,0)#glowStone
                setBlock(lv,x+8,y+5,z+1,89,0)#glowStone
                setBlock(lv,x+8,y+2,z+1,89,0)#glowStone
                setBlock(lv,x+8,y+5,z+7,89,0)#glowStone
        
        if di==0:
            for i in range(w):
                for j in range(6):
                    for k in range(d):
                        setBlock(lv,x+i,y+j,z+k,0,0)
            wallZ(x,y,z) #x,z
            wallZ(x,y,z+9) #x,z
            if door==0:
                wallX(x,y,z,1) #x,z,door
                wallX(x+8,y,z,0) #x,z,door
            elif door==1:
                wallX(x,y,z,0) #x,z,door
                wallX(x+8,y,z,1) #x,z,door
            setBlock(lv,x-1,y+2,z,50,2)
            setBlock(lv,x-1,y+2,z+3,50,2)
            setBlock(lv,x-1,y+2,z+6,50,2)
            setBlock(lv,x-1,y+2,z+9,50,2)
            setBlock(lv,x+9,y+2,z,50,1)
            setBlock(lv,x+9,y+2,z+3,50,1)
            setBlock(lv,x+9,y+2,z+6,50,1)
            setBlock(lv,x+9,y+2,z+9,50,1)
        elif di==1:
            for i in range(w):
                for j in range(6):
                    for k in range(d):
                        setBlock(lv,x+k,y+j,z+i,0,0) 
            wallZ(x,y,z) #x,z
            wallZ(x+9,y,z) #x,z
            if door==0:
                wallX(x,y,z,1) #x,z,door
                wallX(x,y,z+8,0) #x,z,door
            elif door==1:
                wallX(x,y,z,0) #x,z,door
                wallX(x,y,z+8,1) #x,z,door
            setBlock(lv,x,y+2,z-1,50,4)
            setBlock(lv,x+3,y+2,z-1,50,4)
            setBlock(lv,x+6,y+2,z-1,50,4)
            setBlock(lv,x+9,y+2,z-1,50,4)
            setBlock(lv,x,y+2,z+9,50,3)
            setBlock(lv,x+3,y+2,z+9,50,3)
            setBlock(lv,x+6,y+2,z+9,50,3)
            setBlock(lv,x+9,y+2,z+9,50,3)
        floor(x,y,z,door)

        roof = RoofBuilder(lv, x, z, d, y+6, di, 0, t_ID,t_data,w_ID,w_data,r_ID)
        roof.build()
        