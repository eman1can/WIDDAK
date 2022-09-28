#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functions import *
import ToriiBuilder as T


class MountainPath:
    def __init__(self, level, real_start_pos, start_pos, end_pos, height_map, one_area, tori=0):
        self.level = level
        self.height_map = height_map
        self.h = self.height_map.getHeight(start_pos[0], start_pos[1])
        self.tori = tori
        self.direction = (0, 0)
        self.real_start_pos = real_start_pos
        self.pos = [[-1, 0], [-1, -1], [0, -1], [1, -1],
                    [1, 0],  [1, 1],   [0, 1],  [-1, 1]]  # search in the 4 directions of the cell S-W-N-E
        self.one_area = one_area
        self.start_pos = start_pos
        # print start_pos
        self.end_pos = end_pos
        # print end_pos
        self.res_paths = []
        self.block_id = 43

    def find_goal(self):
        sh = self.one_area.shape
        foundflag = False
        for i in range(8):
            p_x = self.start_pos[0]
            p_z = self.start_pos[1]
            n_x = self.pos[i][0] + p_x
            n_z = self.pos[i][1] + p_z
            while 0 <= n_x < sh[0] and 0 <= n_z < sh[1]:
                # print n_x, n_z
                if self.one_area[n_x, n_z] == -1:
                    self.end_pos = (n_x, n_z)
                    self.direction = self.pos[i]
                    foundflag = True
                    break
                n_x += self.pos[i][0]
                n_z += self.pos[i][1]
            if foundflag:
                break
        return self.end_pos


    def scan_path(self):
        p_x = self.start_pos[0]
        p_z = self.start_pos[1]
        p_h = self.get_height_from_map(p_x, p_z)
        self.res_paths.append((p_x, p_z))
        x_offset, z_offset = self.get_offset(p_x, p_z)
        while not (x_offset == 0 and z_offset == 0):
            h_difference1 = []
            h2 = []
            action1 = []
            for i in range(8):
                n_x = self.pos[i][0] + p_x
                n_z = self.pos[i][1] + p_z
                if (n_x, n_z) in self.res_paths:
                    continue
                h_difference = abs(self.get_height_from_map(n_x, n_z) - p_h)
                h2.append(h_difference)
                if h_difference >= 3:
                    continue
                if x_offset == self.pos[i][0] and z_offset == self.pos[i][1]:
                    if h_difference <= 1:
                        h_difference1 = []
                        action1 = []
                        h_difference1.append(h_difference)
                        action1.append((n_x, n_z))
                        break
                else:
                    h_difference1.append(h_difference)
                    action1.append((n_x, n_z))
            # print "p_x, p_z", p_x, p_z
            # print "offset ", x_offset, z_offset
            # print self.res_paths
            # print h_difference1
            # print h2
            if len(h_difference1) > 0:
                p_x, p_z = action1[h_difference1.index(min(h_difference1))]
                self.res_paths.append((p_x, p_z))
                p_h = self.get_height_from_map(p_x, p_z)
                x_offset, z_offset = self.get_offset(p_x, p_z)
            else:
                # print "path break"
                break
        self.paving()

    def paving(self):
        xx = 0
        zz = 0
        i = 0
        for one in self.res_paths:
            p_x = one[0] + self.real_start_pos[0]
            p_z = one[1] + self.real_start_pos[1]
            p_y = self.height_map.getHeight(one[0], one[1])
            # for i in range(1, 11):
            #     setBlock(self.level, p_x, p_y + i, p_z, 0)
            setBlock(self.level, p_x, p_y, p_z, 89)
            for i in range(8):
                n_x = self.pos[i][0] + p_x - self.real_start_pos[0]
                n_z = self.pos[i][1] + p_z - self.real_start_pos[1]
                if (n_x, n_z) not in self.res_paths and self.get_height_from_map(n_x, n_z) < 500:
                    setBlock(self.level, n_x + self.real_start_pos[0], p_y, n_z + self.real_start_pos[1], self.block_id)
            if i == 0:
                xx = one[0]
                zz = one[1]
            elif abs(one[0] - xx) >= 5:
                xx = one[0]
                zz = one[1]
                if self.tori == 1:
                    T.ToriiBuilder(self.level, p_x, p_y, p_z, 0)
            elif abs(one[1] - zz) >= 5:
                xx = one[0]
                zz = one[1]
                if self.tori == 1:
                    T.ToriiBuilder(self.level, p_x, p_y, p_z, 1)
            i += 1

    def get_height_from_map(self, p_x, p_z):
        if 0 <= p_x < self.height_map.shape[0] and 0 <= p_z < self.height_map.shape[1]:
            return self.height_map.getHeight(p_x, p_z)
        else:
            return 500

    def get_offset(self, p_x, p_z):
        x_offset = 0
        z_offset = 0
        end_x = self.end_pos[0]
        end_z = self.end_pos[1]
        if p_x < end_x:
            x_offset = 1
        elif p_x > end_x:
            x_offset = -1
        if p_z < end_z:
            z_offset = 1
        elif p_z > end_z:
            z_offset = -1
        return x_offset, z_offset
