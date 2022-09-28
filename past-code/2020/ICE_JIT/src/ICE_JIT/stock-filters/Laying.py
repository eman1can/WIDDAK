#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functions import *


class Laying:
    def __init__(self, level, height_map, real_start_pos, start_pos, end_pos, surface, block_id, have_surface):
        self.lv = level
        self.rs_pos = real_start_pos
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.surface = surface
        self.height_map = height_map
        self.block_id = block_id
        self.have_surface = have_surface
        self.work()

    def work(self):
        for x in range(self.start_pos[0], self.end_pos[0]):
            for z in range(self.start_pos[2], self.end_pos[2]):
                p_x = x + self.rs_pos[0]
                p_z = z + self.rs_pos[2]
                real_h = self.height_map.getHeight(x, z)
                # print "real_h", real_h
                # print "self.surface", self.surface
                if self.have_surface:
                    for p_y in range(real_h, self.surface):
                        # print "p_y", p_y
                        setBlock(self.lv, p_x, p_y, p_z, self.block_id[2], self.block_id[3])

                    setBlock(self.lv, p_x, self.surface, p_z, self.block_id[0], self.block_id[1])

                for y in range(self.start_pos[1], self.end_pos[1]):
                    setBlock(self.lv, p_x, y + self.surface, p_z, self.block_id[4])


