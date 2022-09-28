#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functions import *
import numpy as np
from time import *


class BorderAreaFinder:
    def __init__(self, area_map):
        begin_time = time()
        self.area_map = np.copy(area_map)
        self.shape = self.area_map.shape
        self.pos = [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1],
                    [-1, 1]]  # search in the 4 directions of the cell S-W-N-E
        self.checked_list = []
        self.uncheck_list = []
        self.border_blocks = []
        self.group_of_border_blocks = []
        self.scanBorders()
        self.groupBorders()
        end_time = time()
        run_time = end_time - begin_time
        print "BorderAreaFinder's runtime: %.2f s" % run_time

    def getAllBorders(self):
        return self.group_of_border_blocks

    def getAllAreaBordersInOrder(self):
        group_measure = []
        for one_g in self.group_of_border_blocks:
            min_x_p = one_g[0][0]
            min_z_p = one_g[0][1]
            max_x_p = one_g[0][0]
            max_z_p = one_g[0][1]
            for i in range(1, len(one_g)):
                if one_g[i][0] < min_x_p:
                    min_x_p = one_g[i][0]
                elif one_g[i][0] > max_x_p:
                    max_x_p = one_g[i][0]
                if one_g[i][1] < min_z_p:
                    min_z_p = one_g[i][1]
                elif one_g[i][1] > max_z_p:
                    max_z_p = one_g[i][1]
            group_measure.append((max_x_p - min_x_p) * (max_z_p - min_z_p))
        sorted_group_measure = sorted(group_measure, reverse=True)
        # print sorted_group_measure
        new_group = []
        for one in sorted_group_measure:
            new_group.append(self.group_of_border_blocks[group_measure.index(one)])

        return new_group

    def scanBorders(self):
        for x in range(self.shape[0]):
            for z in range(self.shape[1]):
                if self.area_map[x, z] == 1 and self.is_border(x, z):
                    self.area_map[x, z] = 10
                    self.border_blocks.append((x, z))

    def is_border(self, x, z):
        if x in [0, self.shape[0]-1] or z in [0, self.shape[1]-1]:
            return True
        res = False
        for i in range(8):
            p_x = self.pos[i][0] + x
            p_z = self.pos[i][1] + z  # search in the 4 directions of the cell S-W-N-E
            if 0 <= p_x < self.shape[0] and 0 <= p_z < self.shape[1]:
                if self.area_map[p_x, p_z] == 0 or self.area_map[p_x, p_z] == 2 or self.area_map[p_x, p_z] == 5:
                    return True
        return res

    def groupBorders(self):
        while len(self.border_blocks) > 0:
            first_border_block = self.border_blocks[0]
            self.checked_list = []
            self.uncheck_list = []
            a = self.getConnectionPoint(first_border_block[0], first_border_block[1])
            self.group_of_border_blocks.append(a)

    def getAreaMap(self):
        return self.area_map

    def getConnectionPoint(self, x, z):
        self.uncheck_list.append((x, z))
        while len(self.uncheck_list) > 0:
            (c_x, c_z) = self.uncheck_list.pop(0)
            self.checkStep(c_x, c_z)
        return self.checked_list

    def checkStep(self, x, z):
        for i in range(8):
            p_x = self.pos[i][0] + x
            p_z = self.pos[i][1] + z  # search in the 4 directions of the cell S-W-N-E
            if 0 <= p_x < self.shape[0] and 0 <= p_z < self.shape[1]:
                p_y = self.area_map[p_x, p_z]
                if p_y == 10:
                    if (p_x, p_z) not in self.checked_list and (p_x, p_z) not in self.uncheck_list:
                        self.uncheck_list.append((p_x, p_z))
        self.checked_list.append((x, z))
        self.border_blocks.remove((x, z))
