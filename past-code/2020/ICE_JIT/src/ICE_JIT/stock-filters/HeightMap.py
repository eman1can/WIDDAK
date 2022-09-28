#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
from matplotlib import pyplot as plt
from time import *


class HeightMap:
    def __init__(self, level, start_x, start_z, end_x, end_z):
        begin_time = time()
        self.level = level
        self.s_x = start_x
        self.s_z = start_z
        self.e_x = end_x
        self.e_z = end_z
        self.water_blocks = []
        self.aboveSurfaceBlocks = [0, 6, 17, 18, 31, 32, 37, 38, 39, 40, 59, 78, 81, 83, 99,
                                   100, 103, 104, 105, 106, 111, 141, 142, 161, 162, 175]
        self.n = self.e_x - self.s_x - 1
        self.height_map = np.zeros((self.e_x - self.s_x, self.e_z - self.s_z), dtype=np.int)
        self.height_map2 = np.zeros((self.e_x - self.s_x, self.e_z - self.s_z), dtype=np.int)
        self.height_map_gradient_X = None
        self.height_map_gradient_Z = None
        self.height_map_norm = None
        self.shape = self.height_map.shape
        self.calculate()
        self.calculate_gradient()

        end_time = time()
        run_time = end_time - begin_time
        print "HeightMap's runtime: %.2f s" % run_time
        # plt.imshow(self.height_map_gradient_X, cmap='gray')
        # plt.show()
        # plt.imshow(self.height_map_gradient_Z, cmap='gray')
        # plt.show()
        # print self.height_map
        # print self.height_map_gradient_X
        # print self.height_map_gradient_Z
        # print self.height_map_norm

    def showMap(self):
        print self.height_map2
        print "be careful! X axis reversed!"
        plt.imshow(self.height_map2, cmap='gray')
        plt.show()

    def getShape(self):
        return self.shape

    def getHeightMap(self):
        return self.height_map

    def getWaterBlocks(self):
        return self.water_blocks

    def getHeight_map_gradient_X(self):
        return self.height_map_gradient_X

    def getHeight_map_gradient_Z(self):
        return self.height_map_gradient_Z

    def get_height_map_norm(self):
        return self.height_map_norm

    def calculate(self):
        for x in range(0, self.e_x - self.s_x):
            for z in range(0, self.e_z - self.s_z):
                height = self.calculateSurfacePointHeight(self.level, x + self.s_x, z + self.s_z)
                block_id = self.level.blockAt(x + self.s_x, height, z + self.s_z)
                if block_id == 8 or block_id == 9:
                    self.water_blocks.append((x, z))
                self.height_map[x, z] = height
                self.height_map2[self.n - x, z] = height

    def calculateSurfacePointHeight(self, level, x, z):
        heightIsFound = False
        y = 128
        while not heightIsFound:
            if self.isSurfaceBlock(level, x, y, z):
                heightIsFound = True
            else:
                y -= 1
        return y

    def isSurfaceBlock(self, level, x, y, z):
        # print level.blockAt(x, y, z)
        for block in self.aboveSurfaceBlocks:
            if level.blockAt(x, y, z) == block:
                return False
        return True

    def calculate_gradient(self):
        res = np.gradient(self.height_map)
        self.height_map_gradient_X = res[0]
        self.height_map_gradient_Z = res[1]
        self.height_map_norm = np.sqrt(res[0]**2 + res[1]**2)

    def getHeight(self, x, z):
        if 0 <= x < self.shape[0] and 0 <= z < self.shape[1]:
            return self.height_map[x, z]
        else:
            return 128

    def getNorm(self, x, z):
        if 0 <= x < self.shape[0] and 0 <= z < self.shape[1]:
            return self.height_map_norm[x, z]
        else:
            return 128

