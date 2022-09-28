#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functions import *
import numpy as np
import MooreNeighborhood as M
from time import *


class FlatFinder:
    def __init__(self, level, height_map, area_size=20, threshold=3):
        begin_time = time()
        self.level = level
        self.height_limit = 2
        self.unFill_list = []
        self.height_map = height_map
        self.h_shape = self.height_map.getShape()
        self.waters = self.height_map.getWaterBlocks()
        self.threshold = threshold
        self.area_size = area_size
        self.gap_num = area_size/10
        self.area_list_x = []
        self.area_list_z = []
        self.candidate_Points_list = []
        self.candidate_Areas_list = []
        self.checked_list = []
        self.uncheck_list = []
        self.mergeArea = np.zeros(self.h_shape, dtype=np.int)
        self.mergeArea_meanHeight = np.zeros(self.h_shape, dtype=np.int)
        self.pos = [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1],
                    [-1, 1]]  # search in the 4 directions of the cell S-W-N-E
        self.splitArea()
        self.calculateCandidatePoints()
        self.calculateCandidateAreas()
        self.mergeAllArea()
        self.find_river()

        end_time = time()
        run_time = end_time - begin_time
        print "FlatFinder's runtime: %.2f s" % run_time

    def splitArea(self):
        area_number_x = self.h_shape[0] / self.area_size
        remainder_x = self.h_shape[0] % self.area_size
        area_number_z = self.h_shape[1] / self.area_size
        remainder_z = self.h_shape[1] % self.area_size
        for i in range(area_number_x-1):
            self.area_list_x.append((self.area_size*i, self.area_size*(i+1)))
        if area_number_x == 0:
            self.area_list_x.append(
                (0, self.area_size * area_number_x + remainder_x))
        else:
            self.area_list_x.append(
                (self.area_size * (area_number_x - 1), self.area_size * area_number_x + remainder_x))
        for i in range(area_number_z-1):
            self.area_list_z.append((self.area_size*i, self.area_size*(i+1)))
        if area_number_z == 0:
            self.area_list_z.append(
                (0, self.area_size * area_number_z + remainder_z))
        else:
            self.area_list_z.append(
                (self.area_size * (area_number_z - 1), self.area_size * area_number_z + remainder_z))
        # print self.area_list_x
        # print self.area_list_z

    def calculateCandidatePoints(self):
        for one_x_area in self.area_list_x:
            for one_z_area in self.area_list_z:
                self.candidate_Points_list.append(self.calculateOneCandidatePoint(one_x_area, one_z_area))

    def calculateCandidateAreas(self):
        area_index = 0
        for one_x_area in self.area_list_x:
            for one_z_area in self.area_list_z:
                self.candidate_Areas_list.append(self.calculateOneCandidateArea(one_x_area, one_z_area, area_index))
                area_index += 1

    def calculateOneCandidatePoint(self, one_x_area, one_z_area):
        one_candidate_point = one_x_area[0], one_z_area[0]
        min_norm = 128
        for x in range(0 + self.gap_num, one_x_area[1] - one_x_area[0] - self.gap_num):
            for z in range(0 + self.gap_num, one_z_area[1] - one_z_area[0] - self.gap_num):
                index_xz = one_x_area[0] + x, one_z_area[0] + z
                if index_xz in self.waters:
                    continue
                mean_norm = self.calculate_point_mean_norm(index_xz)
                # print mean_norm
                if mean_norm == 0:
                    return index_xz
                if mean_norm < min_norm:
                    min_norm = mean_norm
                    one_candidate_point = index_xz
        # print min_norm
        # print one_candidate_point
        return one_candidate_point

    def calculateOneCandidateArea(self, one_x_area, one_z_area, area_index):
        point = self.candidate_Points_list[area_index]
        height = self.height_map.getHeight(point[0], point[1])
        # print point, height
        m = M.MooreNeighbor(self.height_map, point[0], height, point[1], one_x_area, one_z_area, self.threshold)
        return m.getResult()

    def calculate_point_mean_norm(self, index_xz):
        norm_list = []
        for i in range(index_xz[0] - self.gap_num, index_xz[0] + self.gap_num):
            for j in range(index_xz[1] - self.gap_num, index_xz[1] + self.gap_num):
                norm_list.append(self.height_map.getNorm(i, j))
        mean_norm = np.mean(norm_list)
        return mean_norm

    def getCandidatePoints(self):
        return self.candidate_Points_list

    def getCandidateAreas(self):
        return self.candidate_Areas_list

    def getMergeArea(self):
        return self.mergeArea

    def mergeAllArea(self):
        for one in self.candidate_Areas_list:
            mean_h = 0
            c_num = 0
            for one_area in one:
                mean_h += self.height_map.getHeight(one_area[0], one_area[2])
                c_num += 1
                if (one_area[0], one_area[2]) not in self.waters:
                    self.mergeArea[one_area[0], one_area[2]] = 1
                else:
                    self.mergeArea[one_area[0], one_area[2]] = 2         # waters_blocks = 2
            if c_num > 0:
                mean_h = mean_h/c_num
                for one_area in one:
                    self.mergeArea_meanHeight[one_area[0], one_area[2]] = mean_h
        # print self.mergeArea_meanHeight
        # self.mergeSmallArea()
        # gradient_x, gradient_z = np.gradient(self.mergeArea)
        # print gradient_x
        # print gradient_z

    # def mergeSmallArea(self):
    #     for x in range(self.h_shape[0]):
    #         for z in range(self.h_shape[1]):
    #             if self.mergeArea[x, z] == 0 and (x, z) not in self.unFill_list:
    #                 small_area = self.getConnectionPoint(x, z)
    #                 self.canBeFilled(x, z, small_area)

    # def canBeFilled(self, x, z, small_area):
    #     if len(small_area) <= 200:
    #         for x, z in small_area:
    #             self.mergeArea[x, z] = 1
    #     else:
    #         for one in small_area:
    #             self.unFill_list.append(one)

    def getMeanHeight(self, m_area):
        h = 0
        count_num = 0
        for one in m_area:
            h += self.height_map.getHeight(one[0], one[1]) - 60
            count_num += 1
        return h/count_num + 60

    def getConnectionPoint(self, x, z):
        checked_list2 = []
        self.uncheck_list.append((x, z))
        while len(self.uncheck_list) > 0:
            (c_x, c_z) = self.uncheck_list.pop(0)
            self.checkStep(c_x, c_z, checked_list2)
        return checked_list2

    def checkStep(self, x, z, checked_list2):
        for i in range(8):
            p_x = self.pos[i][0] + x
            p_z = self.pos[i][1] + z  # search in the 4 directions of the cell S-W-N-E
            if 0 <= p_x < self.h_shape[0] and 0 <= p_z < self.h_shape[1]:
                p_y = self.mergeArea[p_x, p_z]
                if p_y == 2:
                    if (p_x, p_z) not in self.checked_list and (p_x, p_z) not in self.uncheck_list:
                        self.uncheck_list.append((p_x, p_z))
        self.checked_list.append((x, z))
        checked_list2.append((x, z))

    def find_river(self):
        waters = []
        for x in range(self.h_shape[0]):
            for z in range(self.h_shape[1]):
                if (x, z) not in self.checked_list and self.mergeArea[x, z] == 2:
                    waters.append(self.getConnectionPoint(x, z))
        print "Waters' area:", len(waters)
        for one_area in waters:
            if len(one_area) >= 200:
                for one in one_area:
                    self.mergeArea[one[0], one[1]] = 5

