#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functions import *

# displayName = "roof"


class RoofBuilder:
    """two directions 0&1  two types(room & tower) width must be 9"""

    def __init__(self, level, start_x, start_z, depth, surface, direction, roof_type, tree_ID,tree_data,wood_ID,wood_data, roof_ID):
        self.level = level
        self.start_x = start_x
        self.start_z = start_z
        self.depth = depth
        self.surface = surface
        self.direction = direction
        self.roof_type = roof_type
        self.tree_ID = tree_ID
        self.tree_data = tree_data
        self.wood_ID = wood_ID
        self.wood_data = wood_data
        self.roof_ID = roof_ID
        self.width = 9

    def build(self):
        lv = self.level
        x = self.start_x
        z = self.start_z
        s = self.surface
        w = self.width
        d = self.depth
        t_ID = self.tree_ID
        t_data = self.tree_data
        w_ID = self.wood_ID
        w_data = self.wood_data
        r_ID = self.roof_ID
        lw = 4
        if self.roof_type is 0:  # room's roof
            if self.direction is 0:
                for i in range(1, w / 2):
                    for j in range(i):
                        setBlock(lv, x + i, s + j, z, w_ID, w_data)
                        setBlock(lv, x + w - i - 1, s + j, z, w_ID, w_data)
                        setBlock(lv, x + i, s + j, z + d - 1, w_ID, w_data)
                        setBlock(lv, x + w - i - 1, s + j, z + d - 1, w_ID, w_data)
                for i in range(3):
                    setBlock(lv, x + w / 2, s + i, z, t_ID,t_data)
                    setBlock(lv, x + w / 2, s + i, z + d - 1, t_ID,t_data)  # Triangles on both sides
                for i in range(0, d + 2):
                    setBlock(lv, x - 1, s - 2, z - 1 + i, 53, 4)
                    setBlock(lv, x + w, s - 2, z - 1 + i, 53, 4)  # Wooden Stairs (Oak)

                    setBlock(lv, x - 2, s - 2, z - 1 + i, r_ID[1], r_ID[2] + 8)
                    setBlock(lv, x + w + 1, s - 2, z - 1 + i, r_ID[1], r_ID[2] + 8)  # Stone Brick Slab
                    setBlock(lv, x + w - 4, s + 3, z - 1 + i, r_ID[1], r_ID[2])
                    setBlock(lv, x + 3, s + 3, z - 1 + i, r_ID[1], r_ID[2])  # Stone Brick Slab Top

                    setBlock(lv, x + 4, s + 3, z - 1 + i, r_ID[3], r_ID[4])  # Stone Brick Slab (Double)
                    if r_ID[0] == 109:
                        setBlock(lv, x + 4, s + 4, z - 1 + i, 139, 0)  # Cobblestone Wall

                    setBlock(lv, x + w - 3, s + 2, z - 1 + i, r_ID[0], 1)
                    setBlock(lv, x + w - 2, s + 1, z - 1 + i, r_ID[0], 1)
                    setBlock(lv, x + w - 1, s, z - 1 + i, r_ID[0], 1)
                    setBlock(lv, x + 2, s + 2, z - 1 + i, r_ID[0], 0)
                    setBlock(lv, x + 1, s + 1, z - 1 + i, r_ID[0], 0)
                    setBlock(lv, x, s, z - 1 + i, r_ID[0], 0)
                    setBlock(lv, x - 1, s - 1, z - 1 + i, r_ID[0], 0)
                    setBlock(lv, x + w, s - 1, z - 1 + i, r_ID[0], 1)  # Stone Brick Stairs
                setBlock(lv, x - 1, s - 2, z - 1, 126, 8)
                setBlock(lv, x + w, s - 2, z - 1, 126, 8)
                setBlock(lv, x - 1, s - 2, z + d, 126, 8)
                setBlock(lv, x + w, s - 2, z + d, 126, 8)  # Oak-Wood Slabs at four corners
            else:
                for i in range(1, w / 2):
                    for j in range(i):
                        setBlock(lv, x, s + j, z + i, w_ID, w_data)
                        setBlock(lv, x, s + j, z + w - i - 1, w_ID, w_data)
                        setBlock(lv, x + d - 1, s + j, z + i, w_ID, w_data)
                        setBlock(lv, x + d - 1, s + j, z + w - i - 1, w_ID, w_data)
                for i in range(3):
                    setBlock(lv, x, s + i, z + w / 2, t_ID,t_data)
                    setBlock(lv, x + d - 1, s + i, z + w / 2, t_ID,t_data)  # Triangles on both sides
                for i in range(0, d + 2):
                    setBlock(lv, x - 1 + i, s - 2, z - 1, 53, 4)
                    setBlock(lv, x - 1 + i, s - 2, z + w, 53, 4)  # Wooden Stairs (Oak)

                    setBlock(lv, x - 1 + i, s - 2, z - 2, r_ID[1], r_ID[2] + 8)
                    setBlock(lv, x - 1 + i, s - 2, z + w + 1, r_ID[1], r_ID[2] + 8)  # Stone Brick Slab
                    setBlock(lv, x - 1 + i, s + 3, z + w - 4, r_ID[1], r_ID[2])
                    setBlock(lv, x - 1 + i, s + 3, z + 3, r_ID[1], r_ID[2])  # Stone Brick Slab Top

                    setBlock(lv, x - 1 + i, s + 3, z + 4, r_ID[3], r_ID[4])  # Stone Brick Slab (Double)
                    if r_ID[0] == 109:
                        setBlock(lv, x - 1 + i, s + 4, z + 4, 139, 0)  # Cobblestone Wall

                    setBlock(lv, x - 1 + i, s + 2, z + w - 3, r_ID[0], 3)
                    setBlock(lv, x - 1 + i, s + 1, z + w - 2, r_ID[0], 3)
                    setBlock(lv, x - 1 + i, s, z + w - 1, r_ID[0], 3)
                    setBlock(lv, x - 1 + i, s + 2, z + 2, r_ID[0], 2)
                    setBlock(lv, x - 1 + i, s + 1, z + 1, r_ID[0], 2)
                    setBlock(lv, x - 1 + i, s, z, r_ID[0], 2)
                    setBlock(lv, x - 1 + i, s - 1, z - 1, r_ID[0], 2)
                    setBlock(lv, x - 1 + i, s - 1, z + w, r_ID[0], 3)  # Stone Brick Stairs
                setBlock(lv, x - 1, s - 2, z - 1, 126, 8)
                setBlock(lv, x - 1, s - 2, z + w, 126, 8)
                setBlock(lv, x + d, s - 2, z - 1, 126, 8)
                setBlock(lv, x + d, s - 2, z + w, 126, 8)  # Oak-Wood Slabs at four corners
        elif self.roof_type is 1:  # tower's roof
            d = d-1
            for i in range(0, 4):
                for j in range(x-4+i, x + d + 4-i-1):    # left
                    if i > 0:
                        if j < (d-1)/2 + x:
                            setBlock(lv, j, s - 1, z - 5 + i, 53, 4)
                        elif j > (d-1)/2 + x:
                            setBlock(lv, j, s - 1, z - 5 + i, 53, 5)
                        else:
                            setBlock(lv, j, s - 1, z - 5 + i, r_ID[1], r_ID[2] + 5)
                    if i is 0:
                        if j == x-4+i or j == x + d + 4-i-2:
                            setBlock(lv, j, s, z - 5 + i, r_ID[1], r_ID[2])
                        else:
                            setBlock(lv, j, s-1, z - 5 + i, r_ID[1], r_ID[2]+8)
                    elif i is 1:
                        setBlock(lv, j, s, z - 5 + i, r_ID[1], r_ID[2])
                    elif i is 2:
                        setBlock(lv, j, s, z - 5 + i, r_ID[3], r_ID[4])
                    else:
                        setBlock(lv, j, s, z - 5 + i, r_ID[1], r_ID[2] + 8)
            for i in range(0, 4):
                for j in range(x-4+i, x + d + 4-i-1):  # right
                    if i > 0:
                        if j < (d-1)/2 + x:
                            setBlock(lv, j, s-1, z + d + 3 - i, 53, 4)
                        elif j > (d-1)/2 + x:
                            setBlock(lv, j, s-1, z + d + 3 - i, 53, 5)
                        else:
                            setBlock(lv, j, s-1, z + d + 3 - i, r_ID[1], r_ID[2] + 5)
                    if i is 0:
                        if j == x-4+i or j == x + d + 4-i-2:
                            setBlock(lv, j, s, z + d + 3 - i, r_ID[1], r_ID[2])
                        else:
                            setBlock(lv, j, s-1, z + d + 3 - i, r_ID[1], r_ID[2] + 8)
                    elif i is 1:
                        setBlock(lv, j, s, z + d + 3 - i, r_ID[1], r_ID[2])
                    elif i is 2:
                        setBlock(lv, j, s, z + d + 3 - i, r_ID[3], r_ID[4])
                    else:
                        setBlock(lv, j, s, z + d + 3 - i, r_ID[1], r_ID[2] + 8)
            for i in range(0, 4):
                for j in range(z-5+i, z + d + 4 - i):  # under
                    if i > 0:
                        if j == z-5+i or j == z + d + 4 - i -1:
                            setBlock(lv, x - 5 + i, s - 1, j, r_ID[1], r_ID[2] + 5)
                        else:
                            if j > (d-1)/2 + z:
                                setBlock(lv, x - 5 + i, s-1, j, 53, 7)
                            elif j < (d-1)/2 + z:
                                setBlock(lv, x - 5 + i, s - 1, j, 53, 6)
                            else:
                                setBlock(lv, x - 5 + i, s - 1, j, r_ID[1], r_ID[2] + 5)
                    if i is 0:
                        if j == z-5+i or j == z + d + 4 - i - 1:
                            setBlock(lv, x - 5 + i, s, j, r_ID[1], r_ID[2] + 8)

                        elif j == z-5+i+1 or j == z + d + 4 - i - 2:
                            setBlock(lv, x - 5 + i, s - 1 + 1, j, r_ID[1], r_ID[2])
                        else:
                            setBlock(lv, x - 5 + i, s - 1, j, r_ID[1], r_ID[2] + 8)
                    elif i is 1:
                        if j == z - 5 + i or j == z + d + 4 - i - 1:
                            setBlock(lv, x - 5 + i, s - 1, j, 189)
                            setBlock(lv, x - 5 + i, s - 2, j, 89)
                        setBlock(lv, x - 5 + i, s, j, r_ID[1], r_ID[2])
                    elif i is 2:
                        setBlock(lv, x - 5 + i, s, j, r_ID[3], r_ID[4])
                    else:
                        setBlock(lv, x - 5 + i, s, j, r_ID[1], r_ID[2] + 8)
            for i in range(0, 4):
                for j in range(z-4+i-1, z + d + 3 - i+1):  # up
                    if i > 0:
                        if j == z-4+i-1 or j == z + d + 3 - i:
                            setBlock(lv, x + d + 3 - i, s-1, j, r_ID[1], r_ID[2] + 5)
                        else:
                            if j < (d-1)/2 + z:
                                setBlock(lv, x + d + 3 - i, s - 1, j, 53, 6)
                            elif j > (d-1)/2 + z:
                                setBlock(lv, x + d + 3 - i, s - 1, j, 53, 7)
                            else:
                                setBlock(lv, x + d + 3 - i, s-1, j, r_ID[1], r_ID[2] + 5)
                    if i is 0:
                        if j == z-4+i-1 or j == z + d + 3 - i:
                            setBlock(lv, x + d + 3 - i, s, j, r_ID[1], r_ID[2] + 8)
                        elif j == z-4+i or j == z + d + 3 - i - 1:
                            setBlock(lv, x + d + 3 - i, s, j, r_ID[1], r_ID[2])
                        else:
                            setBlock(lv, x + d + 3 - i, s - 1, j, r_ID[1], r_ID[2] + 8)
                    elif i is 1:
                        if j == z - 4 + i - 1 or j == z + d + 3 - i:
                            setBlock(lv, x + d + 3 - i, s - 1, j, 189)
                            setBlock(lv, x + d + 3 - i, s - 2, j, 89)
                        setBlock(lv, x + d + 3 - i, s, j, r_ID[1], r_ID[2])
                    elif i is 2:
                        setBlock(lv, x + d + 3 - i, s, j, r_ID[3], r_ID[4])
                    else:
                        setBlock(lv, x + d + 3 - i, s, j, r_ID[1], r_ID[2] + 8)
            if d <= 5:
                for i in range(d+1):
                    for j in range(d+1):
                        setBlock(lv, x+3-i, s+1, z-1+j, r_ID[1], r_ID[2])
                for i in range(d-1):
                    for j in range(d-1):
                        setBlock(lv, x+2-i, s+1, z+j, r_ID[3], r_ID[4])
                s -= 1
                for i in range(12):
                    stairs = [r_ID[0], 114]
                    if i == 0 or i == 1:
                        setBlock(lv, x, s + 3 + i, z + 1, stairs[i], 4)
                        setBlock(lv, x + 2, s + 3 + i, z + 1, stairs[i], 5)
                        setBlock(lv, x + 1, s + 3 + i, z, stairs[i], 6)
                        setBlock(lv, x + 1, s + 3 + i, z + 2, stairs[i], 7)
                    else:
                        setBlock(lv, x + 1, s + 3 + i, z, r_ID[1], r_ID[2])
                        setBlock(lv, x + 1, s + 3 + i, z + 2, r_ID[1], r_ID[2])
                        setBlock(lv, x, s + 3 + i, z + 1, r_ID[1], r_ID[2])
                        setBlock(lv, x + 2, s + 3 + i, z + 1, r_ID[1], r_ID[2])
                    if i % 2 == 0:
                        setBlock(lv, x+1, s + 3 + i, z+1, r_ID[3], r_ID[4])
                    else:
                        setBlock(lv, x+1, s + 3 + i, z+1, 89, 0)
                for i in range(3):
                    setBlock(lv, x + 1, s + 15 + i, z + 1, 145)
                setBlock(lv, x + 1, s + 18, z + 1, 139)
                setBlock(lv, x + 1, s + 19, z + 1, 113)
                setBlock(lv, x + 1, s + 20, z + 1, 139)
                setBlock(lv, x + 1, s + 21, z + 1, 76, 5)
        elif self.roof_type is 2:  # little house roof
            if self.direction is 0:
                for i in range(1, lw / 2):
                    for j in range(i):
                        setBlock(lv, x + i, s + j, z, w_ID, w_data)
                        setBlock(lv, x + lw - i - 1, s + j, z, w_ID, w_data)
                        setBlock(lv, x + i, s + j, z + d - 1, w_ID, w_data)
                        setBlock(lv, x + lw - i - 1, s + j, z + d - 1, w_ID, w_data)
                for i in range(0, d + 2):
                    setBlock(lv, x + lw - 2, s + 1, z - 1 + i, r_ID[0], 1)
                    setBlock(lv, x + lw - 1, s, z - 1 + i, r_ID[0], 1)
                    setBlock(lv, x + 1, s + 1, z - 1 + i, r_ID[0], 0)
                    setBlock(lv, x, s, z - 1 + i, r_ID[0], 0)
                    setBlock(lv, x - 1, s - 1, z - 1 + i, r_ID[0], 0)
                    setBlock(lv, x + lw, s - 1, z - 1 + i, r_ID[0], 1)  # Stone Brick Stairs
            else:
                for i in range(1, lw / 2):
                    for j in range(i):
                        setBlock(lv, x, s + j, z + i, w_ID, w_data)
                        setBlock(lv, x, s + j, z + lw - i - 1, w_ID, w_data)
                        setBlock(lv, x + d - 1, s + j, z + i, w_ID, w_data)
                        setBlock(lv, x + d - 1, s + j, z + lw - i - 1, w_ID, w_data)
                for i in range(0, d + 2):
                    setBlock(lv, x - 1 + i, s + 1, z + lw - 2, r_ID[0], 3)
                    setBlock(lv, x - 1 + i, s, z + lw - 1, r_ID[0], 3)
                    setBlock(lv, x - 1 + i, s + 1, z + 1, r_ID[0], 2)
                    setBlock(lv, x - 1 + i, s, z, r_ID[0], 2)
                    setBlock(lv, x - 1 + i, s - 1, z - 1, r_ID[0], 2)
                    setBlock(lv, x - 1 + i, s - 1, z + lw, r_ID[0], 3)  # Stone Brick Stairs
# def perform(level, box, options):
#     (width, height, depth) = getBoxSize(box)
#     surface = box.miny
#     start_x = box.minx
#     start_z = box.minz
#     print 'width(x) = %d, depth(z) = %d' % (width, depth)
#     print 'start_x = %d, start_z = %d' % (start_x, start_z)
#     print 'surface = %d' % surface
#
#     roof_builder = RoofBuilder(level, start_x, start_z, depth, box.maxy, 0, 1)
#     roof_builder.run()
#
#     for i in range(box.minx, box.maxx):
#         for j in range(box.minz, box.maxz):
#             id = level.blockAt(i, surface, j)
#             data = level.blockDataAt(i, surface, j)
#             print "id = %d   data=%d " % (id, data)
#             setBlock(level, box.minx-1, surface, j, id, data)