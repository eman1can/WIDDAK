#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functions import *


class LanternBuilder:
    """LanternBuilder 3x3"""

    def __init__(self, level, start_x, start_z, surface, lantern_type=0):
        self.level = level
        self.start_x = start_x
        self.start_z = start_z
        self.surface = surface
        self.lantern_type = lantern_type
        self.build()

    def build(self):
        lv = self.level
        x = self.start_x
        z = self.start_z
        s = self.surface
        if self.lantern_type is 0:
            setBlock(lv, x + 1, s + 3, z + 1, 44, 3)
            setBlock(lv, x + 1, s, z + 1, 43, 3)
            setBlock(lv, x + 1, s + 1, z + 1, 139, 0)
            setBlock(lv, x + 1, s + 2, z + 1, 89, 0)
            setBlock(lv, x + 1, s + 2, z, 96, 4)
            setBlock(lv, x, s + 2, z + 1, 96, 6)
            setBlock(lv, x + 2, s + 2, z + 1, 96, 7)
            setBlock(lv, x + 1, s + 2, z + 2, 96, 5)
        else:
            setBlock(lv, x, s, z, 44, 3)
            setBlock(lv, x + 2, s, z, 44, 3)
            setBlock(lv, x, s, z + 2, 44, 3)
            setBlock(lv, x + 2, s, z + 2, 44, 3)
            for one in [s, s+4]:
                setBlock(lv, x + 1, one, z + 1, 43, 3)
                setBlock(lv, x + 1, one, z, 67, 2)
                setBlock(lv, x + 2, one, z + 1, 67, 1)
                setBlock(lv, x, one, z + 1, 67, 0)
                setBlock(lv, x + 1, one, z + 2, 67, 3)
            setBlock(lv, x + 1, s + 5, z + 1, 44, 3)
            setBlock(lv, x + 1, s + 1, z + 1, 43, 3)
            setBlock(lv, x + 1, s + 2, z + 1, 139, 0)
            setBlock(lv, x + 1, s + 3, z + 1, 89, 0)
            setBlock(lv, x + 1, s + 3, z, 96, 4)
            setBlock(lv, x, s + 3, z + 1, 96, 6)
            setBlock(lv, x + 2, s + 3, z + 1, 96, 7)
            setBlock(lv, x + 1, s + 3, z + 2, 96, 5)
