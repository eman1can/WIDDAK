# coding=utf-8
"""
Function used to compute sociability
"""

from __future__ import division

from typing import List

import numpy as np
from numba import njit

from building_seeding import Parcel
from building_seeding.building_encyclopedia import BUILDING_ENCYCLOPEDIA
from building_seeding.interest.math_function import attraction_repulsion
from utils import Point, euclidean, X_ARRAY, Z_ARRAY


def local_sociability(x, z, building_type, scenario, settlement_seeds: List[Parcel]):
    if not settlement_seeds:
        return 0

    _sociability = 0
    social_score = -1

    for settlement_seed in settlement_seeds:

        neighbor_type, neighbor_position = settlement_seed.building_type, settlement_seed.center
        distance_to_building = euclidean(Point(x, z), neighbor_position)
        lambda_min, lambda_0, lambda_max = BUILDING_ENCYCLOPEDIA[scenario]["Sociability"][
            building_type.name + "-" + neighbor_type.name]

        social_score = attraction_repulsion(distance_to_building, lambda_min, lambda_0, lambda_max)

        if social_score == -1:
            return -1

        _sociability += social_score

    return _sociability / len(settlement_seeds)


def sociability(building_type, scenario, settlement_seeds, size):
    sociability_all = np.zeros(size)
    unreachable = np.full(size, False)

    for seed in settlement_seeds:
        neighbor_type, pos = seed.building_type, seed.center
        lambdas = BUILDING_ENCYCLOPEDIA[scenario]["Sociability"][building_type.name + "-" + neighbor_type.name]
        sociability_one = sociability_one_seed(*lambdas, pos.x, pos.z, size)
        unreachable |= (sociability_one == -1)
        sociability_all += sociability_one

    sociability_all /= len(settlement_seeds)
    sociability_all[unreachable] = -1
    return sociability_all


@njit()
def sociability_one_seed(l0, l1, l2, x, z, size):
    X = np.full(size, x)
    Z = np.full(size, z)
    D = np.sqrt((X - X_ARRAY) ** 2 + (Z - Z_ARRAY) ** 2)
    # return np.vectorize(lambda d: attraction_repulsion(d, l0, l1, l2))(D)
    return attraction_repulsion(D, l0, l1, l2)
