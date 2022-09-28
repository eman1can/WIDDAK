#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from functions import *
from roofBuilder import *


class House_Builder:

    #door is 0->front 1->back

    def __init__(self, level, start_x, start_y, start_z, door, width, direction, tree_ID,tree_data,wood_ID,wood_data,roof_ID):
        self.level = level
        self.start_x = start_x
        self.start_y = start_y
        self.start_z = start_z
        self.door = door
        self.width = width
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
        width = self.width
        di = self.direction
        t_ID =self.tree_ID
        t_data =self.tree_data
        w_ID = self.wood_ID
        w_data = self.wood_data
        r_ID = self.roof_ID
        w = 9
        size = int((width-1)/8)
        d = size*8+1


        def wallX(x,y,z,door):
            if di==0:
                """
                if self.wall_type is 0:
                    for j in range(9): #line_W
                        setBlock(lv, x, y, z + j, 4, 0)#stone
                        if(j==0 or j==3 or j==5 or j==8):
                            for k in range(1,5): #line_H
                                setBlock(lv,x,y+k,z+j,17,1)#black
                        else:
                            if(door==1):
                                if(j==4):
                                    setBlock(lv,x,y,z+j,196,0)#door
                                    setBlock(lv,x,y+1,z+j,196,7)#door
                                else:
                                    for k in range(1,5): #line_H
                                        if k==3:
                                            setBlock(lv,x,y+k,z+j,17,1)#black
                                        else:
                                            setBlock(lv,x,y+k,z+j,12,0)#white
                                for k in range(2,5): #line_H
                                    if k==2:
                                        setBlock(lv,x,y+k,z+j,17,1)#black
                                    else:
                                        setBlock(lv,x,y+k,z+j,12,0)#white
                                setBlock(lv, x, y+1, z+1, 85, 0)
                                setBlock(lv, x, y+1, z+2, 85, 0)
                                setBlock(lv, x, y+1, z+6, 85, 0)
                                setBlock(lv, x, y+1, z+7, 85, 0)
                            else:
                                for k in range(1,5): #line_H
                                    if k==2:
                                        setBlock(lv,x,y+k,z+j,17,1)#black
                                    else:
                                        setBlock(lv,x,y+k,z+j,12,0)#white
                if self.wall_type is 1:
                """
                for j in range(9): #line_W
                    setBlock(lv, x, y, z + j, 4, 0)#stone
                    if(j==0 or j==3 or j==5 or j==8):
                        for k in range(1,5): #line_H
                            setBlock(lv,x,y+k,z+j,t_ID,t_data)#black
                    else:
                        if(door==1):
                            if(j==4):
                                setBlock(lv,x,y,z+j,196,0)#door
                                setBlock(lv,x,y+1,z+j,196,8)#door
                            else:
                                for k in range(1,5): #line_H
                                    if k==3:
                                        setBlock(lv,x,y+k,z+j,t_ID,t_data)#black
                                    else:
                                        setBlock(lv,x,y+k,z+j,w_ID,w_data)#white
                            for k in range(2,5): #line_H
                                if k==2:
                                    setBlock(lv,x,y+k,z+j,t_ID,t_data)#black
                                else:
                                    setBlock(lv,x,y+k,z+j,w_ID,w_data)#white
                            setBlock(lv, x, y+1, z+1, 85, 0)
                            setBlock(lv, x, y+1, z+2, 85, 0)
                            setBlock(lv, x, y+1, z+6, 85, 0)
                            setBlock(lv, x, y+1, z+7, 85, 0)
                        else:
                            for k in range(1,5): #line_H
                                if k==2:
                                    setBlock(lv,x,y+k,z+j,t_ID,t_data)#black
                                else:
                                    setBlock(lv,x,y+k,z+j,w_ID,w_data)#white
            elif di==1: 
                """ 
                if self.wall_type is 0:
                    for j in range(9): #line_W
                        setBlock(lv, x+j, y, z, 4, 0)#stone
                        if(j==0 or j==3 or j==5 or j==8):
                            for k in range(1,5): #line_H
                                setBlock(lv,x+j,y+k,z,17,1)#black
                        else:
                            if(door==1):
                                if(j==4):
                                    setBlock(lv,x+j,y,z,196,1)#door
                                    setBlock(lv,x+j,y+1,z,196,9)#door
                                else:
                                    for k in range(1,5): #line_H
                                        if k==3:
                                            setBlock(lv,x+j,y+k,z,17,1)#black
                                        else:
                                            setBlock(lv,x+j,y+k,z,12,0)#white
                                for k in range(2,5): #line_H
                                    if k==2:
                                        setBlock(lv,x+j,y+k,z,17,1)#black
                                    else:
                                        setBlock(lv,x+j,y+k,z,12,0)#white
                                setBlock(lv, x, y+1, z+1, 85, 0)
                                setBlock(lv, x, y+1, z+2, 85, 0)
                                setBlock(lv, x, y+1, z+6, 85, 0)
                                setBlock(lv, x, y+1, z+7, 85, 0)
                            else:
                                for k in range(1,5): #line_H
                                    if k==2:
                                        setBlock(lv,x+j,y+k,z,17,1)#black
                                    else:
                                        setBlock(lv,x+j,y+k,z,12,0)#white
                if self.wall_type is 1:
                """
                for j in range(9): #line_W
                    setBlock(lv, x+j, y, z, 4, 0)#stone
                    if(j==0 or j==3 or j==5 or j==8):
                        for k in range(1,5): #line_H
                            setBlock(lv,x+j,y+k,z,t_ID,t_data)#black
                    else:
                        if(door==1):
                            if(j==4):
                                setBlock(lv,x+j,y,z,196,1)#door
                                setBlock(lv,x+j,y+1,z,196,9)#door
                            else:
                                for k in range(1,5): #line_H
                                    if k==3:
                                        setBlock(lv,x+j,y+k,z,t_ID,t_data)#black
                                    else:
                                        setBlock(lv,x+j,y+k,z,w_ID,w_data)#white
                            for k in range(2,5): #line_H
                                if k==2:
                                    setBlock(lv,x+j,y+k,z,t_ID,t_data)#black
                                else:
                                    setBlock(lv,x+j,y+k,z,w_ID,w_data)#white
                            setBlock(lv, x+1, y+1, z, 85, 0)
                            setBlock(lv, x+2, y+1, z, 85, 0)
                            setBlock(lv, x+6, y+1, z, 85, 0)
                            setBlock(lv, x+7, y+1, z, 85, 0)
                        else:
                            for k in range(1,5): #line_H
                                if k==2:
                                    setBlock(lv,x+j,y+k,z,t_ID,t_data)#black
                                else:
                                    setBlock(lv,x+j,y+k,z,w_ID,w_data)#white

        def wallZ(x,y,z):
            if di==0:
                """
                if self.wall_type is 0:
                    for j in range(8): #line_W
                        setBlock(lv, x + j, y, z, 4, 0)#rstone
                        if(j==0 or j==4 or j==8):
                            for k in range(1,5): #line_H
                                setBlock(lv, x + j, y + k, z, 17,1)#black
                        else:
                            for k in range(1,5): #line_H
                                if k==2:
                                    setBlock(lv, x + j, y + k, z, 17,1)#black
                                else:
                                    setBlock(lv, x + j, y + k, z, 12,0)#white         
                if self.wall_type is 1:
                """
                for j in range(9): #line_W
                    setBlock(lv, x + j, y, z, 4, 0)#rstone
                    if(j==0 or j==4 or j==8):
                        for k in range(1,5): #line_H
                            setBlock(lv, x + j, y + k, z, t_ID, t_data)#black
                    else:
                        for k in range(1,5): #line_H
                            if k==2:
                                setBlock(lv, x + j, y + k, z, t_ID, t_data)#black
                            else:
                                setBlock(lv, x + j, y + k, z, w_ID,w_data)#white
            if di==1:  
                """ 
                if self.wall_type is 0:
                    for j in range(8): #line_W
                        setBlock(lv, x, y, z+j, 4, 0)#rstone
                        if(j==0 or j==4 or j==8):
                            for k in range(1,5): #line_H
                                setBlock(lv, x, y + k, z+j, 17,1)#black
                        else:
                            for k in range(1,5): #line_H
                                if k==2:
                                    setBlock(lv, x, y + k, z+j, 17,1)#black
                                else:
                                    setBlock(lv, x, y + k, z+j, 12,0)#white         
                if self.wall_type is 1:
                """
                for j in range(9): #line_W
                    setBlock(lv, x, y, z+j, 4, 0)#rstone
                    if(j==0 or j==4 or j==8):
                        for k in range(1,5): #line_H
                            setBlock(lv, x, y + k, z+j, t_ID, t_data)#black
                    else:
                        for k in range(1,5): #line_H
                            if k==2:
                                setBlock(lv, x, y + k, z+j, t_ID, t_data)#black
                            else:
                                setBlock(lv, x, y + k, z+j, w_ID,w_data)#white


        def floor(x,y,z,door): #must fix
            if di==0:
                if door==0:
                    for j in range(0,7):
                        for i in range(1,4):
                            setBlock(lv, x+i, y-1, z+j+1, 4, 0)
                        setBlock(lv, x+4, y, z+j+1, 126, 0)
                        for i in range(5,8):
                            setBlock(lv, x+i, y, z+j+1, 5, 0)
                    setBlock(lv, x+7, y+1, z+1, 58, 0)
                    setBlock(lv, x+7, y+1, z+random.randint(2,6), 54, 4)
                    setBlock(lv, x+7, y+1, z+7, 50, 5)
                    setBlock(lv, x+1, y, z+1, 50, 5)
                    setBlock(lv, x+1, y, z+7, 50, 5)
                    setBlock(lv, x+3, y, z+7, 61, 2)
                if door==1:
                    for j in range(0,7):
                        for i in range(5,8):
                            setBlock(lv, x+i, y-1, z+j+1, 4, 0)
                        setBlock(lv, x+4, y, z+j+1, 126, 0)
                        for i in range(1,4):
                            setBlock(lv, x+i, y, z+j+1, 5, 0)
                    setBlock(lv, x+1, y+1, z+1, 58, 0)
                    setBlock(lv, x+1, y+1, z+random.randint(2,6), 54, 4)
                    setBlock(lv, x+1, y+1, z+7, 50, 5)
                    setBlock(lv, x+7, y, z+1, 50, 5)
                    setBlock(lv, x+7, y, z+7, 50, 5)
                    setBlock(lv, x+5, y, z+7, 61, 4)
            elif di==1:
                if door==0:
                    for j in range(0,7):
                        for i in range(1,4):
                            setBlock(lv, x+j+1, y-1, z+i, 4, 0)
                        setBlock(lv, x+j+1, y, z+4, 126, 0)
                        for i in range(5,8):
                            setBlock(lv, x+j+1, y, z+i, 5, 0)
                    setBlock(lv, x+1, y+1, z+7, 58, 0)
                    setBlock(lv, x+random.randint(2,6), y+1, z+7, 54, 4)
                    setBlock(lv, x+7, y+1, z+7, 50, 5)
                    setBlock(lv, x+1, y, z+1, 50, 5)
                    setBlock(lv, x+7, y, z+1, 50, 5)
                    setBlock(lv, x+7, y, z+3, 61, 2)
                if door==1:
                    for j in range(0,7):
                        for i in range(5,8):
                            setBlock(lv, x+j+1, y-1, z+i, 4, 0)
                        setBlock(lv, x+j+1, y, z+4, 126, 0)
                        for i in range(1,4):
                            setBlock(lv, x+j+1, y, z+i, 5, 0)
                    setBlock(lv, x+1, y+1, z+1, 58, 0)
                    setBlock(lv, x+random.randint(2,6), y+1, z+1, 54, 4)
                    setBlock(lv, x+7, y+1, z+1, 50, 5)
                    setBlock(lv, x+1, y, z+7, 50, 5)
                    setBlock(lv, x+7, y, z+7, 50, 5)
                    setBlock(lv, x+7, y, z+5, 61, 4)


        if di==0:
            for i in range(w):
                    for j in range(6):
                        for k in range(d):
                            setBlock(lv,x+i,y+j,z+k,0,0)
            wallZ(x,y,z) #x,z
            for q in range(size):
                wallZ(x,y,z+q*8+8) #x,z
                if door==0:
                    wallX(x,y,z+q*8,1) #x,z,door
                    wallX(x+8,y,z+q*8,0) #x,z,door
                elif door==1:
                    wallX(x,y,z+q*8,0) #x,z,door
                    wallX(x+8,y,z+q*8,1) #x,z,door
                floor(x,y,z+q*8,door)
                setBlock(lv,x-1,y+1,z+q*8,50,2)
                setBlock(lv,x-1,y+1,z+q*8+3,50,2)
                setBlock(lv,x-1,y+1,z+q*8+5,50,2)
                setBlock(lv,x-1,y+1,z+q*8+8,50,2)
                setBlock(lv,x+9,y+1,z+q*8,50,1)
                setBlock(lv,x+9,y+1,z+q*8+3,50,1)
                setBlock(lv,x+9,y+1,z+q*8+5,50,1)
                setBlock(lv,x+9,y+1,z+q*8+8,50,1)
        elif di==1:
            for i in range(w):
                    for j in range(6):
                        for k in range(d):
                            setBlock(lv,x+k,y+j,z+i,0,0)  
            wallZ(x,y,z) #x,z
            for q in range(size):
                wallZ(x+q*8+8,y,z) #x,z

                if door==0:
                    wallX(x+q*8,y,z,1) #x,z,door
                    wallX(x+q*8,y,z+8,0) #x,z,door
                elif door==1:
                    wallX(x+q*8,y,z,0) #x,z,door
                    wallX(x+q*8,y,z+8,1) #x,z,door
                floor(x+q*8,y,z,door)
                setBlock(lv,x+q*8,y+1,z-1,50,4)
                setBlock(lv,x+q*8+3,y+1,z-1,50,4)
                setBlock(lv,x+q*8+5,y+1,z-1,50,4)
                setBlock(lv,x+q*8+8,y+1,z-1,50,4)
                setBlock(lv,x+q*8,y+1,z+9,50,3)
                setBlock(lv,x+q*8+3,y+1,z+9,50,3)
                setBlock(lv,x+q*8+5,y+1,z+9,50,3)
                setBlock(lv,x+q*8+8,y+1,z+9,50,3)

        roof = RoofBuilder(lv, x, z, d, y+5, di, 0, t_ID,t_data,w_ID,w_data, r_ID)
        roof.build()