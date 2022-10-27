"""### Provides various small functions for the average workflow."""

from itertools import product
from typing import Union

import cv2
import numpy as np
from glm import ivec2, ivec3
from matplotlib import pyplot as plt

from . import lookup
from .vector_util import Rect, Box

__all__ = ['isSequence',
           'invertDirection', 'directionToRotation', 'directionToVector',
           'axisToVector']

__author__ = "Blinkenlights"
__version__ = "v5.1"
__year__ = 2022


def isSequence(sequence):
    """**Determine whether sequence is a sequence**."""
    try:
        _ = sequence[0:-1]
        return True
    except TypeError:
        return False


def normalizePolygonCoordinates(polygon: Union[Rect, Box]):
    """**Return set of coordinates where (x1, y1, z1) <= (x2, y2, z2)**."""
    x1, x2 = polygon.x1, polygon.x2
    z1, z2 = polygon.z1, polygon.z2

    if x1 > x2:
        x1, x2 = x2, x1
    if z1 > z2:
        z1, z2 = z2, z1

    if isinstance(polygon, Rect):
        y1, y2 = 0, 255
    else:
        y1, y2 = polygon.y1, polygon.y2
        if y1 > y2:
            y1, y2 = y2, y1
    return Box.from_corners(x1, y1, z1, x2, y2, z2)


def index2slot(sx, sy, ox, oy):
    """**Return slot number of an inventory correlating to a 2d index**."""
    if not (0 <= sx < ox and 0 <= sy < oy):
        raise ValueError(f"{sx, sy} is not within (0, 0) and {ox, oy}!")
    return sx + sy * ox


def identifyObtrusiveness(blockStr):
    """**Return the perceived obtrusiveness of a given block**.

    Returns a numeric weight from 0 (invisible) to 4 (opaque)
    """
    if blockStr in lookup.INVISIBLE:
        return 0
    if blockStr in lookup.FILTERING:
        return 1
    if blockStr in lookup.UNOBTRUSIVE:
        return 2
    if blockStr in lookup.OBTRUSIVE:
        return 3
    return 4


# ========================================================= converters
# The 'data types' commonly used in this package are:
#
# axis: 'x', 'y', 'z'
# direction: 'up', 'down', 'north', 'south', 'east', 'west'
# rotation: 0 - 15 (22.5° clockwise turns starting at north)
# vector: any multiple of (1, 1, 1) e.g. (0, 1, -4)
# =========================================================


def invertDirection(direction):
    """**Return the inverted direction of direction**."""
    if isSequence(direction):
        return [lookup.INVERTDIRECTION[n] for n in direction]
    return lookup.INVERTDIRECTION[direction]


def directionToRotation(direction):
    """**Convert a direction to a rotation**.

    If a sequence is provided, the average is returned.
    """
    reference = {'north': 0, 'east': 4, 'south': 8, 'west': 12}
    if len(direction) == 1:
        rotation = reference[lookup.INVERTDIRECTION[direction[0]]]
    else:
        rotation = 0
        for direction in direction:
            rotation += reference[lookup.INVERTDIRECTION[direction]]
        rotation //= 2

        if rotation == 6 and 'north' not in direction:
            rotation = 14
        if rotation % 4 != 2:
            rotation = reference[direction[0]]
    return rotation


def directionToVector(direction):
    """**Convert a direction to a vector**."""
    return lookup.DIRECTION2VECTOR[direction]


def axisToVector(axis):
    """**Convert an axis to a vector**."""
    return lookup.AXIS2VECTOR[axis]
