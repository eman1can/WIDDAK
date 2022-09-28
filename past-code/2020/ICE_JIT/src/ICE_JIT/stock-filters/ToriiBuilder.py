#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functions import *


class ToriiBuilder:
    """ToriiBuilder 1x8"""

    def __init__(self, level, start_x, surface, start_z, direction=0):
        self.level = level
        self.start_x = start_x
        self.start_z = start_z
        self.surface = surface
        self.direction = direction
        self.build()

    def build(self):
        lv = self.level
        x = self.start_x
        z = self.start_z
        s = self.surface
        d = self.direction
        if d is 0:
            setBlock(lv, x, s, z + 3, 251, 15)
            setBlock(lv, x, s, z - 4, 251, 15)
            for i in range(12):
                setBlock(lv, x, s + 9, z - 6 + i, 251, 14)
            for i in range(10):
                setBlock(lv, x, s + 7, z - 5 + i, 251, 14)
                setBlock(lv, x, s + 10, z - 5 + i, 126, 1)
            setBlock(lv, x, s + 10, z - 6, 134, 3)
            setBlock(lv, x, s + 10, z + 5, 134, 2)
            setBlock(lv, x, s + 10, z - 7, 134, 6)
            setBlock(lv, x, s + 10, z + 6, 134, 7)
            for y in range(s+1, s + 9):
                setBlock(lv, x, y, z + 3, 251, 14)
                setBlock(lv, x, y, z - 4, 251, 14)
        elif d is 1:
            setBlock(lv, x + 3, s, z, 251, 15)
            setBlock(lv, x - 4, s, z, 251, 15)
            for i in range(12):
                setBlock(lv, x - 6 + i, s + 9, z, 251, 14)
            for i in range(10):
                setBlock(lv, x - 5 + i, s + 7, z, 251, 14)
                setBlock(lv, x - 5 + i, s + 10, z, 126, 1)
            setBlock(lv, x - 6, s + 10, z, 134, 1)
            setBlock(lv, x + 5, s + 10, z, 134, 0)
            setBlock(lv, x - 7, s + 10, z, 134, 4)
            setBlock(lv, x + 6, s + 10, z, 134, 5)
            for y in range(s + 1, s + 9):
                setBlock(lv, x + 3, y, z, 251, 14)
                setBlock(lv, x - 4, y, z, 251, 14)



