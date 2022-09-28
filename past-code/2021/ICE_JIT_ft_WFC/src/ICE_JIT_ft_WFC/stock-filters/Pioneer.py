#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ToriiBuilder as T
import BridgeBuilder as B
import LanternBuilder as L
from MaterialChecker import *
from road_builder import *
from Cityscape import *
from field_builder import *
from Laying import *
import numpy as np


class Pioneer:
    """
    -1 = 已经勘探，未被占用土地
    -2 = 已被别人占用建筑土地
    -3 = 生活区
    0 = 不可用土地（原始）
    1 = 可用土地（原始）
    2 = 水
    5 = 河流
    10 = 原始边界（属于可用土地）
    3 = 可用土地(勘探后)
    4 = 不可用土地(勘探后)
    13 = 勘探后边界（属于可用土地）
    """

    def __init__(self, level, height_map, area_with_border, mergeArea_meanHeight, s_x, s_z, gravity_pos):
        self.limit_num = 5
        # begin_time = time()
        self.height_limit = 5
        self.level = level
        self.pos = [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1],
                    [-1, 1]]  # search in the 4 directions of the cell S-W-N-E
        self.s_x = s_x
        self.s_z = s_z
        self.gates_x = []
        self.gates_z = []
        self.bridges = []
        self.x1 = 0
        self.x2 = 0
        self.z1 = 0
        self.z2 = 0
        self.area_with_border = np.copy(area_with_border)
        self.mergeArea_meanHeight = mergeArea_meanHeight
        self.give_to_next_area_with_border = np.copy(area_with_border)
        self.height_for_bridge = np.copy(height_map.height_map)
        self.shape = self.area_with_border.shape
        self.mean_height = 0
        # print self.area_with_border
        self.height_map = height_map
        self.gravity_pos = gravity_pos
        self.gravity_height = height_map.getHeight(gravity_pos[0], gravity_pos[1])
        self.width = 0
        self.height = 0
        self.real_measure = 0  # 实际可用面积
        self.done_flag = False
        self.bridge_pos = []
        self.utilization = self.findAreaToLevelling()
        self.material_dict = Material_Checker(level, height_map, s_x, s_z, self.x1, self.z1, self.x2,
                                              self.z2)  # Material checking
        self.fence_id = self.material_dict["fence_id"]
        self.floor_id = self.material_dict["floor_id"]
        # end_time = time()
        # run_time = end_time - begin_time
        # print "Pioneer's runtime: %.2f s" % run_time

    def give_to_next(self):
        return self.give_to_next_area_with_border

    def findAreaToLevelling(self):
        direction_l = [(-1, -1), (1, -1), (1, 1), (-1, 1), (0, -1), (1, 0), (0, 1), (-1, 0)]
        pos_l = []
        show_path = 0
        for i in range(len(direction_l)):
            self.done_flag = False
            x, z = self.gravity_pos
            while not self.done_flag:
                x += direction_l[i][0]
                z += direction_l[i][1]
                # print "start check x:", x, " z:", z, " = ", self.getValueFromArea(x, z)
                if show_path == 1:
                    p_x = x + self.s_x
                    p_z = z + self.s_z
                    setBlock(self.level, p_x, self.height_map.getHeight(x, z), p_z, 26)
                if self.getValueFromArea(x, z) <= -1:
                    x -= direction_l[i][0]
                    z -= direction_l[i][1]
                    self.done_flag = True
                elif self.getValueFromArea(x, z) != 1:
                    p_height = self.height_map.getHeight(x, z)
                    j = 0
                    while j < self.limit_num:
                        x += direction_l[i][0]
                        z += direction_l[i][1]
                        j += 1
                        if abs(self.height_map.getHeight(x, z) - p_height) > self.height_limit:
                            self.done_flag = True
                            break
                        if self.getValueFromArea(x, z) == 1:
                            break
                    if j >= self.limit_num or self.done_flag:
                        x -= j * direction_l[i][0]
                        z -= j * direction_l[i][1]
                        # print "True x:", x, "True z", z
                        self.done_flag = True
            pos_l.append((x, z))
            if show_path == 1:
                p_x = x + self.s_x
                p_z = z + self.s_z
                setBlock(self.level, p_x, self.height_map.getHeight(x, z), p_z, 45)
        # print pos_l
        self.x1 = min(pos_l[0][0], pos_l[3][0], pos_l[7][0])
        self.x2 = max(pos_l[1][0], pos_l[2][0], pos_l[5][0])
        self.z1 = min(pos_l[0][1], pos_l[1][1], pos_l[4][1])
        self.z2 = max(pos_l[2][1], pos_l[3][1], pos_l[6][1])
        # print self.x1, self.x2
        # print self.z1, self.z2
        count_num = 0
        self.width = self.z2 - self.z1 + 1
        self.height = self.x2 - self.x1 + 1
        backup_land = []
        # print self.area_with_border
        for x in range(self.x1, self.x2 + 1):
            for z in range(self.z1, self.z2 + 1):
                # print self.area_with_border[x, z]
                if self.area_with_border[x, z] == 0:
                    backup_land.append((x, z))
                    continue
                elif self.area_with_border[x, z] == 2 or self.area_with_border[x, z] <= -1 or \
                        self.area_with_border[x, z] == 5:
                    continue
                # print x, z
                if not abs(self.mergeArea_meanHeight[x, z] - self.gravity_height) > self.height_limit:
                    self.area_with_border[x, z] = 3
                    self.mean_height += self.height_map.getHeight(x, z)
                    count_num += 1
                else:
                    self.area_with_border[x, z] = 4
                    backup_land.append((x, z))

        self.calculateMeanHeight(count_num)
        for one in backup_land:
            if abs(self.height_map.getHeight(one[0], one[1]) - self.mean_height) <= self.height_limit:
                self.area_with_border[one[0], one[1]] = 3
                count_num += 1
        self.real_measure = count_num
        # print self.area_with_border
        for x in range(self.x1, self.x2 + 1):
            for z in range(self.z1, self.z2 + 1):
                if self.area_with_border[x, z] == 3 and self.isBorder(x, z):
                    self.area_with_border[x, z] = 13

        for x in range(self.x1, self.x2 + 1):
            for z in range(self.z1, self.z2 + 1):
                if self.area_with_border[x, z] == 3 or self.area_with_border[x, z] == 13:
                    self.height_for_bridge[x, z] = self.mean_height
                    self.give_to_next_area_with_border[x, z] = -2
                else:
                    self.give_to_next_area_with_border[x, z] = -1

        return float(count_num) / float(self.width * self.height)

    def isBorder(self, x, z):
        if x == self.x1 or x == self.x2 or z == self.z1 or z == self.z2:
            return True
        res = False
        for i in range(8):
            p_x = self.pos[i][0] + x
            p_z = self.pos[i][1] + z
            if 0 <= p_x < self.shape[0] and 0 <= p_z < self.shape[1]:
                if self.area_with_border[p_x, p_z] != 3 and self.area_with_border[p_x, p_z] != 13:
                    return True
            else:
                return True
        return res

    def getValueFromArea(self, x, z):
        shape = self.area_with_border.shape
        if 0 <= x < shape[0] and 0 <= z < shape[1]:
            return self.area_with_border[x, z]
        else:
            return -1

    def getAreaMap(self):
        return self.area_with_border

    def getWidthAndHeight(self):
        return self.width, self.height

    def calculateMeanHeight(self, c):
        if c == 0:
            self.mean_height = self.height_map.getHeight(self.gravity_pos[0], self.gravity_pos[1])
        else:
            self.mean_height = self.mean_height / c

    def get_mean_height(self):
        return self.mean_height

    def getUtilization(self):
        return self.utilization

    def getBridge(self):
        return self.bridges

    def levelling(self):
        # plt.imshow(self.area_with_border, cmap='gray')
        # plt.show()
        for x in range(self.shape[0]):
            for z in range(self.shape[1]):
                p_x = x + self.s_x
                p_z = z + self.s_z
                if self.area_with_border[x, z] == 3:
                    origin_h = self.height_map.getHeight(x, z)
                    if get_block(self.level, p_x, origin_h + 1, p_z)[0] == 17:
                        continue
                    setBlock(self.level, p_x, self.mean_height, p_z, self.floor_id[0], self.floor_id[1])
                    if self.mean_height < origin_h:
                        for i in range(self.mean_height + 1, origin_h + 3):
                            setBlock(self.level, p_x, i, p_z, 0)
                    elif self.mean_height > origin_h:
                        for i in range(origin_h, self.mean_height):
                            setBlock(self.level, p_x, i, p_z, 3)
                        setBlock(self.level, p_x, self.mean_height + 1, p_z, 0)
                        setBlock(self.level, p_x, self.mean_height + 2, p_z, 0)
                    else:
                        setBlock(self.level, p_x, self.mean_height + 1, p_z, 0)
                        setBlock(self.level, p_x, self.mean_height + 2, p_z, 0)
                elif self.area_with_border[x, z] == 13:
                    f_height = self.mean_height
                    for i in range(8):
                        h_x = self.pos[i][0] + x
                        h_z = self.pos[i][1] + z
                        if 0 <= h_x < self.shape[0] and 0 <= h_z < self.shape[1]:
                            if self.area_with_border[h_x, h_z] == 2:
                                h_p = self.height_map.getHeight(h_x, h_z)
                                if h_p > f_height:
                                    f_height = h_p - 1
                    for i in range(self.mean_height - 3, f_height + 10):
                        if i == f_height + 2:
                            setBlock(self.level, p_x, i, p_z, self.fence_id[2])
                        elif i > f_height + 2:
                            setBlock(self.level, p_x, i, p_z, 0)
                        else:
                            setBlock(self.level, p_x, i, p_z, self.fence_id[0], self.fence_id[1])

        # for one in self.gates_z:
        #     x = one[0]
        #     z = one[1]
        #     T.ToriiBuilder(self.level, x + self.s_x, self.mean_height,
        #                    z + self.s_z, 0)
        # for one in self.gates_x:
        #     x = one[0]
        #     z = one[1]
        #     T.ToriiBuilder(self.level, x + self.s_x, self.mean_height,
        #                    z + self.s_z, 1)
        self.paving()

    def get_road_len(self, r_x, width, right_list, d=1, river_check=0):
        road_length = []
        road_continue_flag = False
        road_start_len = (0, 0)
        for z in range(self.z1, self.z2 + d):
            river_flag = False
            flag = True
            for i in range(width):
                v = self.getValueFromArea(r_x + i, z)
                if v == 5:
                    river_flag = True
                if v not in right_list:
                    flag = False
                    break
            if river_flag and river_check == 1:
                self.bridge_pos.append((r_x, z, 6))
            if flag:
                if not road_continue_flag:
                    road_continue_flag = True
                    road_start_len = (z, 0)
            else:
                if road_continue_flag:
                    road_continue_flag = False
                    road_start_len = (road_start_len[0], z - road_start_len[0])
                    road_length.append(road_start_len)

        return road_length

    def paving(self):
        p_z = self.s_z
        river = 0
        road_width = 12
        field_flag = False
        if self.material_dict["is_desert"]:
            # print "need river"
            river = 1
            road_width = 16
        for r_x in range(0, self.height / 2 - 23):
            if r_x % 30 == 0:
                r_x_1 = self.x1 + r_x
                r_x_2 = self.x2 - r_x
                road_length = self.get_road_len(r_x_1 + 1, 6, [3], river_check=1)
                # road from bottom
                for one_len in road_length:
                    Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                           (r_x_1 + 1, 1, one_len[0]),
                           (r_x_1 + 1 + 6, 20, one_len[0] + one_len[1]),
                           self.mean_height, (43, 5, 3, 0, 0), False)
                    road = Road_Builder(self.level, r_x_1 + 1 + self.s_x, self.mean_height + 1, p_z + one_len[0],
                                        one_len[1], 1, 6, 0, 0)
                    road.build()
                    if r_x == 0 and one_len[1] >= 27:
                        n = np.random.randint(0, 3)
                        f = field(self.level, r_x_1 + 1 + self.s_x, self.mean_height, p_z + one_len[0], 10, 10, 1,
                                  n)
                        f.build()
                        n = np.random.randint(0, 3)
                        f = field(self.level, r_x_1 + 1 + self.s_x, self.mean_height, p_z + one_len[0] + 9, 10, 10,
                                  2, n)
                        f.build()
                        n = np.random.randint(0, 3)
                        f = field(self.level, r_x_1 + 1 + self.s_x, self.mean_height, p_z + one_len[0] + 18, 10,
                                  10, 3, n)
                        f.build()
                        field_flag = True
                # under the road
                if r_x_1 - self.x1 > 0:
                    road_length = self.get_road_len(r_x_1 - 8, 9, [3])
                    for one_len in road_length:
                        # print one_len
                        Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                               (r_x_1 - 8, 1, one_len[0]+1),
                               (r_x_1 - 8 + 9, 20, one_len[0] + 1 + one_len[1] - 2),
                               self.mean_height, (43, 5, 3, 0, 0), False)
                        c = Cityspace(self.level, one_len[1]-2, r_x_1 - 8 + self.s_x, self.mean_height + 1,
                                      p_z + one_len[0]+1, 1,
                                      self.material_dict["tree_ID"][0], self.material_dict["tree_ID"][1],
                                      self.material_dict["wood_ID"][0], self.material_dict["wood_ID"][1],
                                      self.material_dict["roof_ID"])
                        c.build()
                        for j in range(0, one_len[1]-3):
                            if j % 10 == 0:
                                L.LanternBuilder(self.level, r_x_1 + self.s_x + 1, p_z + one_len[0] + 1 + j,
                                                 self.mean_height, 0)
                # above the road
                road_length = self.get_road_len(r_x_1 + 7, 9, [3])
                num_a = 0
                for one_len in road_length:
                    # print one_len
                    if r_x_1+19 < self.x1 + self.height / 2 - 17:
                        # print r_x_1 + 7
                        if field_flag and num_a == 0:
                            one_len = (one_len[0] + 27, one_len[1]-27)
                        num_a += 1
                        Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                               (r_x_1 + 7, 1, one_len[0] + 1),
                               (r_x_1 + 7 + 9, 20, one_len[0] + 1 + one_len[1] - 2),
                               self.mean_height, (43, 5, 3, 0, 0), False)
                        c = Cityspace(self.level, one_len[1] - 2, r_x_1 + 7 + self.s_x, self.mean_height + 1,
                                      p_z + one_len[0] + 1, 0,
                                      self.material_dict["tree_ID"][0], self.material_dict["tree_ID"][1],
                                      self.material_dict["wood_ID"][0], self.material_dict["wood_ID"][1],
                                      self.material_dict["roof_ID"])
                        c.build()
                        for j in range(0, one_len[1]-3):
                            if j % 10 == 0:
                                L.LanternBuilder(self.level, r_x_1 + 4 + self.s_x, p_z + one_len[0] + 1 + j,
                                                 self.mean_height, 0)


                # road from up
                road_length = self.get_road_len(r_x_2-6, 6, [3], river_check=1)
                for one_len in road_length:
                    # print one_len
                    Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                           (r_x_2 - 6, 1, one_len[0]),
                           (r_x_2 - 6 + 6, 20, one_len[0] + one_len[1]),
                           self.mean_height, (43, 5, 3, 0, 0), False)
                    road = Road_Builder(self.level, r_x_2 - 6 + self.s_x, self.mean_height + 1, p_z + one_len[0],
                                        one_len[1], 1, 6,
                                        0, 0)
                    road.build()
                # above the road
                road_length = self.get_road_len(r_x_2, 9, [3])
                for one_len in road_length:
                    if r_x_2 + 11 < self.x2:
                        Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                               (r_x_2, 1, one_len[0] + 1),
                               (r_x_2 + 9, 20, one_len[0] + 1 + one_len[1] - 2),
                               self.mean_height, (43, 5, 3, 0, 0), False)
                        c = Cityspace(self.level, one_len[1] - 2, r_x_2 + self.s_x, self.mean_height + 1,
                                      p_z + one_len[0] + 1,
                                      0,
                                      self.material_dict["tree_ID"][0], self.material_dict["tree_ID"][1],
                                      self.material_dict["wood_ID"][0], self.material_dict["wood_ID"][1],
                                      self.material_dict["roof_ID"])
                        c.build()
                        for j in range(0, one_len[1]-3):
                            if j % 10 == 0:
                                L.LanternBuilder(self.level, r_x_2 + self.s_x - 2, p_z + one_len[0] + 1 + j,
                                                 self.mean_height, 0)
                # under the road
                road_length = self.get_road_len(r_x_2 - 15, 9, [3])
                for one_len in road_length:
                    if r_x_2 - 18 > self.x1 + self.height / 2 + 17:
                        Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                               (r_x_2 - 15, 1, one_len[0] + 1),
                               (r_x_2 - 15 + 9, 20, one_len[0] + 1 + one_len[1] - 2),
                               self.mean_height, (43, 5, 3, 0, 0), False)
                        c = Cityspace(self.level, one_len[1] - 2, r_x_2 - 15 + self.s_x, self.mean_height + 1,
                                      p_z + one_len[0] + 1, 1,
                                      self.material_dict["tree_ID"][0], self.material_dict["tree_ID"][1],
                                      self.material_dict["wood_ID"][0], self.material_dict["wood_ID"][1],
                                      self.material_dict["roof_ID"])
                        c.build()
                        for j in range(0, one_len[1]-3):
                            if j % 10 == 0:
                                L.LanternBuilder(self.level, r_x_2 - 6 + self.s_x, p_z + one_len[0] + 1 + j,
                                                 self.mean_height, 0)

        #中间大路及其两侧
        i = 0
        road_length = self.get_road_len(self.x1 + self.height / 2 - road_width/2 + 1, road_width, (3, 13, 2), 2, river_check=1)
        # print "road_length", road_length
        for one_len in road_length:
            if i == 0:
                one_len = (one_len[0] + 1, one_len[1] - 1)
                if river == 0:
                    Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                           (self.x1 + self.height / 2 - 3, 1, self.z1),
                           (self.x1 + self.height / 2 + 4, 4, one_len[0]+1),
                           self.mean_height, (43, 5, 3, 0, 0), False)
                else:
                    Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                           (self.x1 + self.height / 2 - 7, 1, self.z1),
                           (self.x1 + self.height / 2 - 3, 4, one_len[0] + 1),
                           self.mean_height, (43, 5, 3, 0, 0), False)
                    Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                           (self.x1 + self.height / 2 + 5, 1, self.z1),
                           (self.x1 + self.height / 2 + 9, 4, one_len[0] + 1),
                           self.mean_height, (43, 5, 3, 0, 0), False)
                T.ToriiBuilder(self.level, self.x1 + self.height / 2 + self.s_x + 1, self.mean_height+1,
                               one_len[0] + p_z - 1, 1)
            if i == len(road_length)-1:
                one_len = (one_len[0], one_len[1]-1)
                if river == 0:
                    Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                           (self.x1 + self.height / 2 - 3, 1, one_len[0] + one_len[1]),
                           (self.x1 + self.height / 2 + 4, 4, self.z2 + 1),
                           self.mean_height, (43, 5, 3, 0, 0), False)
                else:
                    Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                           (self.x1 + self.height / 2 - 7, 1, one_len[0] + one_len[1]),
                           (self.x1 + self.height / 2 - 3, 4, self.z2 + 1),
                           self.mean_height, (43, 5, 3, 0, 0), False)
                    Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                           (self.x1 + self.height / 2 + 5, 1, one_len[0] + one_len[1]),
                           (self.x1 + self.height / 2 + 9, 4, self.z2 + 1),
                           self.mean_height, (43, 5, 3, 0, 0), False)
                T.ToriiBuilder(self.level, self.x1 + self.height / 2 + self.s_x + 1, self.mean_height+1,
                               one_len[0] + one_len[1] + p_z, 1)
            Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                   (self.x1 + self.height / 2 - road_width / 2 + 1, 1, one_len[0]),
                   (self.x1 + self.height / 2 - road_width / 2 + 1 + road_width, 20, one_len[0] + one_len[1]),
                   self.mean_height - 1, (43, 5, 3, 0, 0), False)
            road = Road_Builder(self.level, self.x1 + self.height / 2 + self.s_x - road_width/2 + 1, self.mean_height + 1,
                                p_z + one_len[0],
                                one_len[1], 1, road_width, 0, river)
            road.build()
            if river == 1 and one_len[1] >= 6:
                B.BridgeBuilder(self.level, self.x1 + self.height / 2 + self.s_x - road_width / 2 + 7,
                                self.mean_height + 2, p_z + one_len[0] + one_len[1] / 2 - 2, 4, 3, 0)
            i += 1
        road_length = self.get_road_len(self.x1 + self.height / 2 - road_width/2-8, 9, (3, 13, 2), 2)
        for one_len in road_length:
            if self.x1 + self.height / 2 > 14:
                Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                       (self.x1 + self.height / 2 - road_width/2-8, 1, one_len[0] + 1),
                       (self.x1 + self.height / 2 - road_width/2-8+9, 20, one_len[0] + 1 + one_len[1] - 2),
                       self.mean_height, (43, 5, 3, 0, 0), False)
                c = Cityspace(self.level, one_len[1]-2, self.x1 + self.height / 2 + self.s_x - road_width/2-8,
                              self.mean_height + 1,
                              p_z + one_len[0] + 1,
                              1,
                              self.material_dict["tree_ID"][0], self.material_dict["tree_ID"][1],
                              self.material_dict["wood_ID"][0], self.material_dict["wood_ID"][1],
                              self.material_dict["roof_ID"])
                c.build()
                for j in range(0, one_len[1]-3):
                    if j % 10 == 0:
                        L.LanternBuilder(self.level, self.x1 + self.height / 2 + self.s_x - road_width/2 + 1, p_z + one_len[0] + 1 + j,
                                         self.mean_height, 0)
        road_length = self.get_road_len(self.x1 + self.height / 2 + road_width/2 + 1, 9, (3, 13, 2), 2)
        for one_len in road_length:
            if self.x1 + self.height / 2 + 17 < self.x2:
                Laying(self.level, self.height_map, (self.s_x, 0, self.s_z),
                       (self.x1 + self.height / 2 + road_width/2 + 1, 1, one_len[0] + 1),
                       (self.x1 + self.height / 2 + road_width/2 + 1 + 9, 20, one_len[0] + 1 + one_len[1] - 2),
                       self.mean_height, (43, 5, 3, 0, 0), False)
                c = Cityspace(self.level, one_len[1]-2, self.x1 + self.height / 2 + self.s_x + road_width/2 + 1,
                              self.mean_height + 1, p_z + one_len[0] + 1,
                              0,
                              self.material_dict["tree_ID"][0], self.material_dict["tree_ID"][1],
                              self.material_dict["wood_ID"][0], self.material_dict["wood_ID"][1],
                              self.material_dict["roof_ID"])
                c.build()
                for j in range(0, one_len[1]-3):
                    if j % 10 == 0:
                        L.LanternBuilder(self.level, self.x1 + self.height / 2 + self.s_x + road_width/2 + 1 - 3, p_z + one_len[0] + 1 + j,
                                         self.mean_height, 0)

    def build_bridge(self):
        # print "bridge_pos", self.bridge_pos
        while len(self.bridge_pos) > 0:
            one_b = self.bridge_pos.pop(0)
            if one_b[2] == -1:
                print "-1", one_b
            else:
                x = one_b[0]
                z = one_b[1]
                w = one_b[2]
                over_border = False
                landfall = False
                j1 = 0
                while True:
                    j1 += 1
                    if z+j1 >= self.area_with_border.shape[1]:
                        over_border = True
                        break
                    num = w/2
                    for i in range(w):
                        if self.area_with_border[x + i, z + j1] == 5 or abs(self.height_for_bridge[x + i, z + j1] - self.mean_height) >= 3:
                            break
                        landfall = True
                    if landfall:
                        break
                if over_border:
                    continue
                over_border = False
                landfall = False
                j2 = 0
                while True:
                    j2 += 1
                    if z - j2 <= 0:
                        over_border = True
                        break
                    for i in range(w):
                        if self.area_with_border[x + i, z - j2] == 5 or abs(self.height_for_bridge[x + i, z - j2] - self.mean_height)>=3:
                            break
                        landfall = True
                    if landfall:
                        break
                if over_border:
                    continue
                j = j1 + j2
                if 2 < j:
                    # print "j", j
                    # print "x, z", x, z
                    B.BridgeBuilder(self.level, x + self.s_x, self.mean_height+2, z + self.s_z - j2, w, j, 1)
                    for o in range(z - j2, z + j1+1):
                        a = (x, o, w)
                        if a in self.bridge_pos:
                            self.bridge_pos.remove(a)

    def secure_area(self, c_x, c_z, x_len, z_len):
        for i in [1, -1]:
            for j in range(1, x_len+1):
                if self.getValueFromArea(c_x + j*i, c_z) <= -2:
                    return False
            for j in range(1, z_len+1):
                if self.getValueFromArea(c_x, c_z + j*i) <= -2:
                    return False
        return True

    def find_water(self, c_x, c_z, x_len, z_len):
        for x in range(c_x-x_len, c_x+x_len):
            for z in range(c_z-z_len, c_z+z_len):
                if self.getValueFromArea(x, z) == 5:
                    self.bridge_pos.append((x, z, -1))
                    return True
        return False

    def define_living_area(self):
        for x in range(self.x1, self.x2 + 1):
            for z in range(self.z1, self.z2 + 1):
                if self.area_with_border[x, z] == -2:
                    self.give_to_next_area_with_border[x, z] = -3
        # east_road_length = self.height - 2
        # p_x = self.x1 + self.s_x
        # for r_z in range(0, self.width / 2 - 25):
        #     if r_z % 40 == 0:
        #         r_z_1 = self.z1 + r_z + self.s_z
        #         r_z_2 = self.z2 - r_z + self.s_z
        #         road = Road_Builder(self.level, p_x, self.mean_height, r_z_1 + 1, east_road_length, 1, 5, 1, 0)
        #         road.build()
        #         road = Road_Builder(self.level, p_x, self.mean_height, r_z_2 - 5, east_road_length, 1, 5, 1, 0)
        #         road.build()
        # road = Road_Builder(self.level, p_x, self.mean_height, self.z1 + self.width / 2 + self.s_z - 5,
        #                     east_road_length, 1,
        #                     10, 1, 0)
        # road.build()

        # road_length = self.height
        # p_x = self.x1 + self.s_x
        # for r_z in range(self.z1, self.z2-5):
        #     if r_z % 20 == 0 or self.z2 - r_z == 0:
        #         p_z = r_z + self.s_z
        #         road = Road_Builder(self.level, p_x, self.mean_height, p_z, road_length, 1, 5, 1, 0)
        #         road.build()
        # for j in range(le / 10):
        #     if abs(z + j*10 - self.width / 2 - self.z1) > 5:
        #         L.LanternBuilder(self.level, p_x + 5, p_z + j * 10, self.mean_height + 1, 0)
        #         L.LanternBuilder(self.level, p_x - 5, p_z + j * 10, self.mean_height + 1, 0)
        # x = self.x1
        # z = self.width / 2 + self.z1
        # p_x = x + self.s_x
        # p_z = z + self.s_z
        # le = self.gates_z[1][0] - x + 1
        # road = Road_Builder(self.level, p_x+5, self.mean_height, p_z - 5, le, 1, 10, 1, 0)
        # road.build()
        # for j in range(le / 10):
        #     if abs(x - 5 + j * 10 - self.height / 2 - self.x1) > 5:
        #         L.LanternBuilder(self.level, p_x - 5 + j * 10, p_z - 5, self.mean_height + 1, 0)
        #         L.LanternBuilder(self.level, p_x - 5 + j * 10, p_z, self.mean_height + 1, 0)

        # start_end_x = [0, 0]
        # river_started = False
        # if self.gates_z.index(one) == 0:
        #     # print "check river -1"
        #     while x >= 0:
        #         if self.area_with_border[x, z] == 2:
        #             if not river_started:
        #                 # print "river_started!", x, z
        #                 river_started = True
        #                 start_end_x[1] = x
        #         else:
        #             if river_started:
        #                 start_end_x[0] = x
        #                 break
        #         x -= 1
        #     if river_started:
        #         # print "river found build bridge:", start_end_x
        #         B.BridgeBuilder(self.level, start_end_x[0] + self.s_x,
        #                         self.height_map.getHeight(start_end_x[0], z) + 2,
        #                         z + self.s_z - 2, 4,
        #                         abs(start_end_x[0] - start_end_x[1]), 0)
        #         self.bridges.append({"start_end_x": (start_end_x[0], start_end_x[1]), "direction": 0})
        # else:
        #     # print "check river +1"
        #     while x < self.shape[0]:
        #         if self.area_with_border[x, z] == 2:
        #             if not river_started:
        #                 # print "river_started!", x, z
        #                 river_started = True
        #                 start_end_x[0] = x
        #         else:
        #             if river_started:
        #                 start_end_x[0] = x
        #                 break
        #         x += 1
        #     if river_started:
        #         # print "found:", start_end_x
        #         B.BridgeBuilder(self.level, start_end_x[0] + self.s_x,
        #                         self.height_map.getHeight(start_end_x[0], z) + 2,
        #                         z + self.s_z - 2, 4,
        #                         abs(start_end_x[0] - start_end_x[1]), 0)
        #         self.bridges.append({"start_end_x": (start_end_x[0], start_end_x[1]), "direction": 0})
