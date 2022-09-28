# coding=utf-8
"""
Function used to compute accessibility
"""

from __future__ import division

import numpy as np


def extendability(size, parcel_size):

    extendability_map = np.zeros(size)

    map_width = size[0]
    map_length = size[1]

    extendability_map[0:parcel_size, :] = -1
    extendability_map[map_width-parcel_size:map_width, :] = -1
    extendability_map[:, parcel_size] = -1
    extendability_map[:, map_length-parcel_size:map_length] = -1

    return extendability_map
