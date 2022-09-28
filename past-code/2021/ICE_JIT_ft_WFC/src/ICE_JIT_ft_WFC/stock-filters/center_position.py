#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
from matplotlib import pyplot as plt

def CenterPosition(norm_arr, filter_size):
    #ave_array = np.arange(size*size).reshape((size, size))
    min_n = 100000000000000
    min_posX = 0
    min_posZ = 0

    print(norm_arr.shape)
    nX, nY = norm_arr.shape

    half_size = filter_size / 2

    #最小平均勾配地点の検出
    for filter_x in range(0 + half_size, nX - half_size):
        for filter_y in range(0 + half_size, nY - half_size):
            #[x][y]
            sum_n = norm_arr[filter_x-half_size: filter_x+half_size, filter_y-half_size: filter_y+half_size].sum()

            if min_n > sum_n:
                min_n = sum_n
                min_posX = filter_x
                min_posZ = filter_y
        # print(min_n, min_posX, min_posZ)
        

    print min_posX,min_posZ
    print norm_arr[min_posX, min_posZ]

    return (min_posX, min_posZ)

# n = np.load('../height_map_norm.npy')
# map = np.load('../height_map.npy')
#
# CenterPosition(n, 300)
# plt.imshow(map, cmap='gray')
# plt.show()

