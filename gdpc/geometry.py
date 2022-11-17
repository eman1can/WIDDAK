"""Provides tools for creating multidimensional shapes"""

__all__ = ['placeLine', 'placeJointedLine',
           'placeFromList', 'getDimension',
           'line2d', 'line3d', 'lineSequence']

__author__ = "Blinkenlights"
__version__ = "v5.1"
__year__ = 2022

from typing import List, Optional, Sequence, Union

import numpy as np
from glm import ivec3

from amulet.api.block import Block

from . import lookup
from .interface import Interface, getGlobalInterface
from .vector_util import Box, Rect

gi = getGlobalInterface()


def getDimension(one: ivec3, two: ivec3):
    """ Get the occupied dimensions of two corner points """
    return 3 - (np.subtract(one, two) == 0).sum()


def getFlatSides(one: ivec3, two: ivec3):
    """ Get which sides are flat from two corner points"""
    return np.subtract(one, two) == 0


def placeFromList(plist: Sequence[ivec3], block: Block, replace: Optional[Union[str, List[str]]] = None, itf: Interface = gi):
    """ Place a block at a list of different points """
    for point in plist:
        itf.place(block, point, replace)


def placeRect(rect: Rect, y: int, block: Block, replace: Optional[Union[str, List[str]]] = None, width: Union[str, int] = 'fill', itf: Interface = gi):
    """ Place a 2d rectangle at a specified y height, and either filled or a specified block width """
    if width == 'fill':
        for x, z in rect:
            itf.place(block, ivec3(x, y, z), replace)
    else:
        for x, z in rect:
            if x - rect.x1 < width or z - rect.z1 < width or rect.x2 - x <= width or rect.z2 - z <= width:
                itf.place(block, ivec3(x, y, z), replace)


def placeBox(box: Box, block: Block, replace: Optional[Union[str, List[str]]] = None, width: Union[str, int] = 'fill', itf: Interface = gi):
    """ Place a 3d cube either filled or with a specified block width """
    if width == 'fill':
        for x, y, z in box:
            itf.place(block, ivec3(x, y, z), replace)
    else:
        for x, y, z in box:
            if x - box.x1 <= width or y - box.y1 <= width or z - box.z1 <= width or box.x2 - x <= width or box.y2 - y <= width or box.z2 - z <= width:
                itf.place(block, ivec3(x, y, z), replace)


def placeCheckeredBox(box: Box, first: Block, second: Block = Block('minecraft:air'), replace: Optional[Union[str, List[str]]] = None, itf: Interface = gi):
    for point in box:
        itf.place(first if sum(point) % 2 == 0 else second, ivec3(*point), replace, itf)


def placeLine(start: ivec3, end: ivec3, block: Block, replace: Optional[Union[str, List[str]]] = None, itf: Interface = gi):
    """ Draw a line from point to point efficiently """
    dim = getDimension(start, end)
    if dim == 0:
        return itf.place(block, start, replace)
    elif dim == 1:
        return placeBox(Box(start, end - start), block, replace)
    elif dim == 2 or dim == 3:
        return placeFromList(line3d(start, end), block, replace, itf)


def placeJointedLine(points: Sequence[ivec3], blocks: Block, replace=None, interface=gi):
    """ Place a line that runs from point to point """
    return placeFromList(lineSequence(points), blocks, replace, interface)


# def placePolygon(points, blocks, replace=None, filled=False, interface=gi):
#     """**Place a polygon that runs from line to line and may be filled**."""
#     polygon = set()
#     polygon.update(lineSequence(points))
#     polygon.update(line3d(*points[0], *points[-1]))
#     dimension, _ = getDimension(*getShapeBoundaries(polygon))
#     if filled and dimension == 2:
#         polygon.update(fill2d(polygon))
#     elif filled and dimension == 3:
#         raise ValueError(f'{lookup.TCOLORS["red"]}Cannot fill 3D polygons!')
#     placeFromList(polygon, blocks, replace, interface)


# TODO: Cylinder
# TODO: Horizontal Cylinder
# TODO: 2D Polygon
# TODO: 3D Polygon
# TODO: Commented Out Functions
# TODO: Corner Pillars (gdcp)
# TODO: Checkered Box (gdcp)
# TODO: Striped Box (gdcp)
# TODO: Striped Box (gdcp)

# ========================================================= calculations


# def getShapeBoundaries(points):
#     """**Return the smallest and largest values used in a shape**."""
#     points = np.array(points)
#     dimension = len(points[0])
#     if dimension == 2:
#         minx, miny = points.min(axis=0)
#         maxx, maxy = points.max(axis=0)
#         return minx, miny, maxx, maxy
#     elif dimension == 3:
#         minx, miny, minz = points.min(axis=0)
#         maxx, maxy, maxz = points.max(axis=0)
#         return minx, miny, minz, maxx, maxy, maxz
#     raise ValueError(f'{lookup.TCOLORS["red"]}{dimension}D '
#                      'shapes are not supported!')


# def padDimension(points, value=0, axis='z'):
#     """**Pad a list of 2D points with a value in the appropriate position**.
#
#     May also be used to replace all values in an axis.
#     """
#     if axis == 'x':
#         return [(value, i[-2], i[-1]) for i in points]
#     elif axis == 'y':
#         return [(i[0], value, i[-1]) for i in points]
#     elif axis == 'z':
#         return [(i[0], i[1], value) for i in points]
#     raise ValueError(f'{lookup.TCOLORS["red"]}{axis} is not a valid axis '
#                      'to pad with!')
#
#
# def cutDimension(points, axis='z'):
#     """**Cut the appropriate axis from a list of points**."""
#     try:
#         if axis == 'x':
#             return [(i[0:]) for i in points]
#         elif axis == 'y':
#             dimension = len(points[0])
#             if dimension == 2:
#                 return [(i[:-1]) for i in points]
#             elif dimension == 3:
#                 return [(i[0], i[-1]) for i in points]
#         elif axis == 'z':
#             return [(i[:-1]) for i in points]
#     except IndexError:
#         pass
#     raise ValueError(f'{lookup.TCOLORS["red"]}{axis} is not a valid axis '
#                      f'to cut from this set!\n{points}')


# def translate(points, amount, axis='y'):
#     """**Return a clone of the points translateed by amount in axis**."""
#     points = set(points)
#     vx, vy, vz = lookup.AXIS2VECTOR[axis]
#     clone = [(x + amount * vx, y + amount * vy, z + amount * vz)
#              for x, y, z in points]
#     return clone


# def repeat(points, times, axis='y', step=1):
#     """**Return points with duplicates shifted along the appropriate axis**."""
#     clone = set(points)
#     for n in range(1, times + 2):
#         clone.update(translate(points, step * n, axis))
#     return clone


# def fill2d(points):
#     """**Return all filling within the shape of points**."""
#     points = list(points)
#     filling = []
#     minx, miny = np.array(points).min()
#     maxx, maxy = np.array(points).max()
#     cx, cy = minx + (maxx - minx) // 2, miny + (maxy - miny) // 2
#
#     def fill(x, y):
#         if (x, y) in points:
#             return
#         elif not (minx <= x <= maxx and miny <= y <= maxy):
#             raise ValueError(f'{lookup.TCOLORS["red"]}Aborted filling '
#                              'open-sided shape!')
#         points.append((x, y))
#         filling.append((x, y))
#         fill(x + 1, y)
#         fill(x - 1, y)
#         fill(x, y + 1)
#         fill(x, y - 1)
#
#     fill(cx, cy)
#     return filling
#
#
# def fill3d(points):
#     """**Return all filling within the shape of points**."""
#     points = list(points)
#     filling = []
#     minx, miny, minz = np.array(points).min(axis=0)
#     maxx, maxy, maxz = np.array(points).max(axis=0)
#     cx, cy, cz = (minx + (maxx - minx) // 2,
#                   miny + (maxy - miny) // 2,
#                   minz + (maxz - minz) // 2)
#
#     def fill(x, y, z):
#         if (x, y, z) in points:
#             return
#         elif not (minx <= x <= maxx
#                   and miny <= y <= maxy
#                   and minz <= z <= maxz):
#             raise ValueError(f'{lookup.TCOLORS["red"]}Aborted filling '
#                              'open-sided 3D shape!')
#         points.append((x, y, z))
#         filling.append((x, y, z))
#         fill(x + 1, y, z)
#         fill(x - 1, y, z)
#         fill(x, y + 1, z)
#         fill(x, y - 1, z)
#         fill(x, y, z + 1)
#         fill(x, y, z - 1)
#
#     fill(cx, cy, cz)
#     return filling


def line2d(s: ivec3, e: ivec3) -> Sequence[ivec3]:
    """**Return coordinates for a 2D line from point to point**.

    From
    https://www.codegrepper.com/code-examples/python/line+algorithm+in+python
    """
    dx = e.x - s.x
    dz = e.z - s.z
    is_steep = abs(dz) > abs(dx)
    if abs(dz) > abs(dx):
        x1, z1 = s.z, s.x
        x2, z2 = e.z, e.x
    else:
        x1, z1 = s.x, s.z
        x2, z2 = e.x, e.z
    # Swap start and end points if necessary
    if x1 > x2:
        x1, x2 = x2, x1
        z1, z2 = z2, z1

    dx = x2 - x1
    dz = z2 - z1

    # Calculate error
    error = int(dx / 2.0)
    zstep = 1 if z1 < z2 else -1

    # Iterate over bounding box generating points between start and end
    z = z1
    points = set()
    for x in range(x1, x2 + 1):
        coord = ivec3(z, s.y, x) if is_steep else ivec3(x, s.y, z)
        points.add(coord)
        error -= abs(dz)
        if error < 0:
            z += zstep
            error += dx

    return list(points)


def line3d(s: ivec3, e: ivec3) -> Sequence[ivec3]:
    """**Return coordinates for a 3D line from point to point**.

    With 'inspiration' from
    https://www.geeksforgeeks.org/bresenhams-algorithm-for-3-d-line-drawing/
    """

    def if_greater_pos_else_neg(a, b):
        return 1 if a > b else -1

    def bresenham_line_next_point(p: ivec3, xs, ys, zs, dx, dy, dz, p1, p2):
        x = p.x + xs
        y = p.y
        z = p.z
        if p1 >= 0:
            y = p.y + ys
            p1 -= 2 * dx
        if p2 >= 0:
            z = p.z + zs
            p2 -= 2 * dx
        p1 += 2 * dy
        p2 += 2 * dz
        return ivec3(x, y, z), p1, p2

    points = set()
    points.add((s.x, s.y, s.z))
    dx = abs(e.x - s.x)
    dy = abs(e.y - s.y)
    dz = abs(e.z - s.z)
    xs = if_greater_pos_else_neg(e.x, s.x)
    ys = if_greater_pos_else_neg(e.y, s.y)
    zs = if_greater_pos_else_neg(e.z, s.z)

    # Driving axis is X-axis"
    curr = s
    if dx >= dy and dx >= dz:
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while curr.x != e.x:
            curr, p1, p2 = bresenham_line_next_point(curr,
                                                     xs, ys, zs,
                                                     dx, dy, dz,
                                                     p1, p2)
            points.add(curr)

    # Driving axis is Y-axis"
    elif dy >= dx and dy >= dz:
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while curr.y != e.y:
            curr, p1, p2 = bresenham_line_next_point(curr,
                                                           ys, xs, zs,
                                                           dy, dx, dz,
                                                           p1, p2)
            points.add(curr)

    # Driving axis is Z-axis"
    else:
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while curr.z != e.z:
            curr, p1, p2 = bresenham_line_next_point(curr,
                                                     zs, xs, ys,
                                                     dz, dx, dy,
                                                     p1, p2)
            points.add(curr)

    return list(points)


def lineSequence(points) -> Sequence[ivec3]:
    """**Return all points connecting points in sequence**."""
    last = points[0]
    dimension = len(last)
    toPlace = set()
    for point in points[0:]:
        if dimension == 2:
            toPlace.update(line2d(last, point))
        elif dimension == 3:
            toPlace.update(line3d(last, point))
        else:
            raise ValueError(f'{lookup.TCOLORS["red"]}{dimension}D lineSequence not supported!')
        last = point
    return list(toPlace)


# def circle(x1, y1, x2, y2, filled=False):
#     """**Return the points of a circle with a given centre and diameter**.
#
#     With 'inspiration' from:
#     https://www.geeksforgeeks.org/bresenhams-circle-drawing-algorithm/
#     """
#     toolbox.normalizeCoordinates(x1, y1, x2, y2)
#
#     diameter = min(x2 - x1, y2 - y1)
#     e = diameter % 2  # for even centers
#     cx, cy = x1 + diameter // 2, y1 + diameter // 2
#     points = set()
#
#     def eightPoints(x, y):
#         points.add((cx + e + x, cy + e + y))
#         points.add((cx - 0 - x, cy + e + y))
#         points.add((cx + e + x, cy - 0 - y))
#         points.add((cx - 0 - x, cy - 0 - y))
#         points.add((cx + e + y, cy + e + x))
#         points.add((cx - 0 - y, cy + e + x))
#         points.add((cx + e + y, cy - 0 - x))
#         points.add((cx - 0 - y, cy - 0 - x))
#
#     r = diameter // 2
#     x, y = 0, r
#     d = 3 - 2 * r
#     eightPoints(x, y)
#     while y >= x:
#         # for each pixel we will
#         # draw all eight pixels
#
#         x += 1
#
#         # check for decision parameter
#         # and correspondingly
#         # update d, x, y
#         if d > 0:
#             y -= 1
#             d = d + 4 * (x - y) + 10
#         else:
#             d = d + 4 * x + 6
#         eightPoints(x, y)
#
#     if filled:
#         return points, fill2d(points)
#     return points
#
#
# def ellipse(x1, y1, x2, y2, filled=False):
#     """**Return the points of an ellipse with a given centre and size**.
#
#     Modified version 'inspired' by chandan_jnu from
#     https://www.geeksforgeeks.org/midpoint-ellipse-drawing-algorithm/
#     """
#     toolbox.normalizeCoordinates(x1, y1, x2, y2)
#
#     dx, dy = x2 - x1, y2 - y1
#     ex, ey = dx % 2, dy % 2
#     if dx == dy:
#         return circle(x1, y1, x2, y2, filled)
#     cx, cy = x1 + dx / 2, y1 + dy / 2
#     points = set()
#     filledpoints = set()
#
#     def fourpoints(x, y):
#         points.add((cx + x, cy + y))
#         points.add((cx - x, cy + y))
#         points.add((cx + x, cy - y))
#         points.add((cx - x, cy - y))
#
#         if filled:
#             filledpoints.update(line2d(cx + ex, cy + ey, cx + x, cy + y))
#             filledpoints.update(line2d(cx, cy + ey, cx - x, cy + y))
#             filledpoints.update(line2d(cx + ex, cy, cx + x, cy - y))
#             filledpoints.update(line2d(cx, cy, cx - x, cy - y))
#
#     rx, ry = dx / 2, dy / 2
#
#     x = 0
#     y = ry
#
#     # Initial decision parameter of region 1
#     d1 = ((ry * ry) - (rx * rx * ry) + (0.25 * rx * rx))
#     dx = 2 * ry * ry * x
#     dy = 2 * rx * rx * y
#
#     # For region 1
#     while dx < dy:
#
#         fourpoints(x, y)
#
#         # Checking and updating value of
#         # decision parameter based on algorithm
#         if d1 < 0:
#             x += 1
#             dx = dx + (2 * ry * ry)
#             d1 = d1 + dx + (ry * ry)
#         else:
#             x += 1
#             y -= 1
#             dx = dx + (2 * ry * ry)
#             dy = dy - (2 * rx * rx)
#             d1 = d1 + dx - dy + (ry * ry)
#
#     # Decision parameter of region 2
#     d2 = (((ry * ry) * ((x + 0.5) * (x + 0.5)))
#           + ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry))
#
#     # Plotting points of region 2
#     while y >= 0:
#
#         fourpoints(x, y)
#
#         # Checking and updating parameter
#         # value based on algorithm
#         if d2 > 0:
#             y -= 1
#             dy = dy - (2 * rx * rx)
#             d2 = d2 + (rx * rx) - dy
#         else:
#             y -= 1
#             x += 1
#             dx = dx + (2 * ry * ry)
#             dy = dy - (2 * rx * rx)
#             d2 = d2 + dx - dy + (rx * rx)
#
#     if filled:
#         return points, fill2d(points)
#     return points
