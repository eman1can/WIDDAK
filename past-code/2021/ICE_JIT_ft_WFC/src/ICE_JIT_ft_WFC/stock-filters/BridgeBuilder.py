#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functions import *


class BridgeBuilder:
    """BridgeBuilder weight x length, 0x, 1z"""

    def __init__(self, level, start_x, start_y, start_z, weight, length, direction=0):
        self.level = level
        self.start_x = start_x
        self.start_z = start_z
        self.surface = start_y
        self.weight = weight
        self.length = length
        self.direction = direction
        self.build()

    def build(self):
        lv = self.level
        x = self.start_x
        z = self.start_z
        s = self.surface
        w = self.weight-1
        le = self.length
        if self.direction is 0:
            for i in range(le + 1):
                if i % 5 == 0 or i == le:
                    j = s
                    while get_block(lv, x + i, j, z) == (0, 0) or \
                            get_block(lv, x + i, j, z) == (8, 0) or \
                            get_block(lv, x + i, j, z) == (9, 0):
                        setBlock(lv, x + i, j, z, 17, 1)
                        setBlock(lv, x + i, j, z + w, 17, 1)
                        j -= 1
                for k in range(w+1):
                    if k is 0 or k is w:
                        setBlock(lv, x + i, s+1, z + k, 192, 0)
                    if i == 0:
                        setBlock(lv, x + i - 1, s, z + k, 134, 0)
                        setBlock(lv, x + i - 2, s - 1, z + k, 134, 0)
                    elif i == le:
                        setBlock(lv, x + i + 1, s, z + k, 134, 1)
                        setBlock(lv, x + i + 2, s - 1, z + k, 134, 1)
                    setBlock(lv, x + i, s, z + k, 125, 1)
        elif self.direction is 1:
            for i in range(le + 1):
                if i % 5 is 0:
                    j = s
                    while get_block(lv, x, j, z + i) == (0, 0) or \
                            get_block(lv, x, j, z + i) == (8, 0) or \
                            get_block(lv, x, j, z + i) == (9, 0):
                        setBlock(lv, x, j, z + i, 17, 1)
                        setBlock(lv, x + w, j, z + i, 17, 1)
                        j -= 1
                for k in range(w+1):
                    if k is 0 or k is w:
                        setBlock(lv, x + k, s+1, z + i, 192, 0)
                        setBlock(lv, x + k, s + 2, z + i, 50, 5)
                    if i == 0:
                        setBlock(lv, x + k, s, z + i - 1, 134, 2)
                        setBlock(lv, x + k, s-1, z + i - 2, 134, 2)
                    elif i == le:
                        setBlock(lv, x + k, s, z + i + 1, 134, 3)
                        setBlock(lv, x + k, s - 1, z + i + 2, 134, 3)
                    setBlock(lv, x + k, s, z + i, 125, 1)
