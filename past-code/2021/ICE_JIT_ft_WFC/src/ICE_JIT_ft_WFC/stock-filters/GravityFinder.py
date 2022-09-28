# coding=utf-8
import decimal as d
from time import *


class GravityFinder:
    """
                @brief      获取多边形的重心点
                @param      points  The points
                @return     The center of gravity point.
    """
    def __init__(self, points):
        self.points = points

    def get_gravity_point2(self):
        sum_x = 0
        sum_y = 0
        le = len(self.points)
        for p in self.points:
            sum_x += p[0]
            sum_y += p[1]
        return [int(sum_x/le), int(sum_y/le)]

    def get_gravity_point(self):
        points = self.points
        if len(points) <= 2:
            return list()

        area = d.Decimal(0.0)
        x, y = d.Decimal(0.0), d.Decimal(0.0)
        for i in range(len(points)):
            lng = d.Decimal(points[i][0])
            lat = d.Decimal(points[i][1])
            nextlng = d.Decimal(points[i-1][0])
            nextlat = d.Decimal(points[i-1][1])

            tmp_area = (nextlng*lat - nextlat*lng)/d.Decimal(2.0)
            area += tmp_area
            x += tmp_area*(lng+nextlng)/d.Decimal(3.0)
            y += tmp_area*(lat+nextlat)/d.Decimal(3.0)
        x = x/area
        y = y/area
        return [int(x), int(y)]
