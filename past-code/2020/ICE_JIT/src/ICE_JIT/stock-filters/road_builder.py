#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functions import *


class Road_Builder:
    # if road_type is 1(sand&river), depth is only 16

    def __init__(self, level, start_x, start_y, start_z, width, height, depth, direction, road_type):
        self.level = level
        self.start_x = start_x
        self.start_y = start_y
        self.start_z = start_z
        self.width = width
        self.height = height
        self.depth = depth
        self.direction = direction
        self.road_type = road_type

    def build(self):
        lv = self.level
        x = self.start_x
        y = self.start_y
        z = self.start_z
        w = self.width
        h = self.height
        d = self.depth
        y= y-1
        maxy = y
        
        if self.road_type is 0: #sand only
            if self.direction is 0:
                for i in range(w):
                    for j in range(d): 
                        setBlock(lv, x+j, y, z+i, 12, 0)
                        setBlock(lv, x+j, y-1, z+i, 17, 1)
                        for k in range(y+1, maxy):
                            setBlock(lv, x+j, k, z+i, 0, 0)
            if self.direction is 1:
                for i in range(w):
                    for j in range(d): 
                        setBlock(lv, x+i, y, z+j, 12, 0)
                        setBlock(lv, x+i, y-1, z+j, 17, 1)
                        for k in range(y+1, maxy):
                            setBlock(lv, x+i, k, z+j, 0, 0)

        elif self.road_type is 1: #sand + river
            if self.direction is 0:
                for i in range(w):
                    #sand
                    for j in range(4): #0~3
                        setBlock(lv, x+j, y, z+i, 12, 0)
                        setBlock(lv, x+j, y-1, z+i, 17, 1)
                        for k in range(y+1, maxy):
                            setBlock(lv, x+j, k, z+i, 0, 0)
                    for j in range(12,16): #12~15
                        setBlock(lv, x+j, y, z+i, 12, 0)
                        setBlock(lv, x+j, y-1, z+i, 17, 1)
                        for k in range(y+1, maxy):
                            setBlock(lv, x+j, k, z+i, 0, 0)
                    #stone
                    for j in range(4,12): #4~11
                        if (j==4 or j==11):
                            for k in range(4):
                                setBlock(lv, x+j, y-k, z+i, 1, 0)
                        else:
                            setBlock(lv, x+j, y-k, z+i, 0, 0)
                            for k in range(2):
                                setBlock(lv, x+j, y-1-k, z+i, 9, 0)
                            setBlock(lv, x+j, y-3, z+i, 1, 0)
                        for k in range(y+1, maxy):
                            setBlock(lv, x+j, k, z+i, 0, 0)
                    
            if self.direction is 1:
                for i in range(w):
                    #sand
                    for j in range(4): #0~3
                        setBlock(lv, x+i, y, z+j, 12, 0)
                        setBlock(lv, x+i, y-1, z+j, 17, 1)
                        for k in range(y+1, maxy):
                            setBlock(lv, x+i, k, z+j, 0, 0)
                    for j in range(12,16): #12~15
                        setBlock(lv, x+i, y, z+j, 12, 0)
                        setBlock(lv, x+i, y-1, z+j, 17, 1)
                        for k in range(y+1, maxy):
                            setBlock(lv, x+i, k, z+j, 0, 0)
                    #stone
                    for j in range(4,12): #4~11
                        if (j==4 or j==11):
                            for k in range(4):
                                setBlock(lv, x+i, y-k, z+j, 1, 0)
                        else:
                            setBlock(lv, x+i, y-k, z+j, 0, 0)
                            for k in range(2):
                                setBlock(lv, x+i, y-1-k, z+j, 9, 0)
                            setBlock(lv, x+i, y-3, z+j, 1, 0)
                        for k in range(y+1, maxy):
                            setBlock(lv, x+i, k, z+j, 0, 0)