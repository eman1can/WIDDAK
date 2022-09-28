#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functions import *


class MooreNeighbor:
    def __init__(self, height_map, x, y, z, one_x_area, one_z_area, threshold=0):
        self.checked_list = []
        self.uncheck_list = []
        self.threshold = threshold
        self.height_map = height_map
        self.start_x = x
        self.start_y = y
        self.start_z = z
        self.one_x_area = one_x_area
        self.one_z_area = one_z_area
        self.pos = [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1],
                    [-1, 1]]  # search in the 4 directions of the cell S-W-N-E
        # self.stoppingSign = 0
        self.uncheck_list.append((x, y, z))
        while len(self.uncheck_list) > 0:
            (c_x, c_y, c_z) = self.uncheck_list.pop(0)
            self.checkStep(c_x, c_y, c_z)

    def checkStep(self, x, y, z):
        for i in range(8):
            p_x = self.pos[i][0] + x
            p_z = self.pos[i][1] + z  # search in the 4 directions of the cell S-W-N-E
            if p_x < self.one_x_area[0] or p_x >= self.one_x_area[1] or p_z < self.one_z_area[0] or p_z >= \
                    self.one_z_area[1]:
                continue
            p_y = self.height_map.getHeight(p_x, p_z)
            if abs(p_y - self.start_y) <= self.threshold:
                if (p_x, p_y, p_z) not in self.checked_list and (p_x, p_y, p_z) not in self.uncheck_list:
                    self.uncheck_list.append((p_x, p_y, p_z))
        self.checked_list.append((x, y, z))

    def getResult(self):
        return self.checked_list

# p = MooreNeighbor(1, 1, 1, 1)
# print p.getResult()
