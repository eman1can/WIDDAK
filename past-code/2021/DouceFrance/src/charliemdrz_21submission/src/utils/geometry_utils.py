from enum import Enum
from typing import Iterable

from interfaceUtils import requestBuildArea
from utils.pymclevel.box import BoundingBox
from utils.misc_objects_functions import argmax


class Point:

    """
    Minecraft main coordinates are x, z, while y represents y
    I choose to set y as an optional coordinate so that you can work with 2D points by just ignoring the 3rd coord
    """

    def __init__(self, x, z, y=0):
        self._x = x if x % 1 else int(x)
        self._z = z if z % 1 else int(z)
        self._y = y if y % 1 else int(y)

    def __str__(self):
        res = "(x:{}".format(self._x)
        res += "; y:{}".format(self._y) if self._y else ""
        res += "; z:{})".format(self._z)
        return res

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return all(_ == 0 for _ in (self - other).coords)

    def __add__(self, other):
        assert isinstance(other, Point)
        return Point(self._x + other._x, self._z + other._z, self._y + other._y)

    def __neg__(self):
        return Point(-self._x, -self._z, -self._y)

    def __sub__(self, other):
        assert isinstance(other, Point)
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, Point):
            return Point(self.x * other.x, self.z * other.z, self.y * other.y)
        return Point(self._x * other, self._z * other, self._y * other)

    def __abs__(self):
        return Point(abs(self.x), abs(self.z), abs(self.y))

    def __truediv__(self, other):
        return Point(self.x // other, self.z // other)

    def __floordiv__(self, other):
        return Point(self.x // other, self.z // other)

    def __hash__(self):
        return hash(self.coords)

    def dot(self, other):
        assert isinstance(other, Point)
        mult = self * other
        return sum(mult.coords)

    @property
    def coords(self):
        return self.x, self.y, self.z

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def norm(self):
        from math import sqrt
        return sqrt(self.dot(self))

    @property
    def toInt(self):
        return Point(int(round(self.x)), int(round(self.z)))


def euclidean(p1: Point, p2: Point) -> float:
    return (p1 - p2).norm


def manhattan(p1: Point, p2: Point) -> float:
    return sum(abs(p2 - p1).coords)


class Direction(Enum):
    """
    Custom direction class
    """

    East = Point(1, 0, 0)
    West = Point(-1, 0, 0)
    South = Point(0, 1, 0)
    North = Point(0, -1, 0)
    Top = Point(0, 0, 1)
    Bottom = Point(0, 0, -1)

    @staticmethod
    def of(dx=0, dy=0, dz=0):
        """
        Given a 3D vector, return the closer cardinal direction
        """
        if isinstance(dx, Point):
            return Direction.of(dx.x, dx.y, dx.z)
        assert not (dx == 0 and dy == 0 and dz == 0)  # assert that at least one coordinate is not null
        # keep only one non null coordinate
        import numpy as np
        kept_dir = argmax([abs(dx), abs(dy), abs(dz)])
        if kept_dir == 0:
            dy = dz = 0
        elif kept_dir == 1:
            dx = dz = 0
        else:
            dx = dy = 0

        # each direction is set to -1 or 1
        dir_x = int(dx / abs(dx)) if dx else 0  # 1, 0, or -1
        dir_y = int(dy / abs(dy)) if dy else 0
        dir_z = int(dz / abs(dz)) if dz else 0
        assert abs(dir_x) + abs(dir_y) + abs(dir_z) == 1  # safety check that the direction is valid
        point_dir = Point(dir_x, dir_z, dir_y)
        for direction in Direction:
            if direction.value == point_dir:
                return direction

    def __eq__(self, other):
        if isinstance(other, Direction):
            return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)
        return False

    def __str__(self):
        # known_dirs = {'0 0 1': 'South', '0 1 0': 'Top', '1 0 0': 'East', '0 0 -1': 'North',
        #               '0 -1 0': 'Bottom', '-1 0 0': 'West'}
        # key = ' '.join(map(str, self.value.coords))
        # name = known_dirs[key] if key in known_dirs else "Unknown"
        # return "{} Direction".format(self.name)
        return self.name

    def __hash__(self):
        return hash(str(self))

    def __neg__(self):
        return Direction.of(-self.value)

    def __abs__(self):
        return Direction.of(abs(self.value))

    def rotate(self):
        """
        Rotates direction anti-normally, East.rotate() == South
        Returns anti-normal rotation of self
        -------

        """
        return Direction.of(dx=-self.value.z, dz=self.value.x)

    @property
    def x(self):
        return self.value.x

    @property
    def y(self):
        return self.value.y

    @property
    def z(self):
        return self.value.z

    @classmethod
    def from_string(cls, dir_str):
        str_to_coord = {value.lower(): key for key, value in Direction.__known_dirs.items()}  # reversed dict
        x, y, z = list(map(int, str_to_coord[dir_str].split(' ')))
        return Direction.of(x, y, z)


def cardinal_directions(as_points: bool = True) -> Iterable[Direction or Point]:
    directions = [Direction.East, Direction.South, Direction.West, Direction.North]
    if as_points:
        directions = list(map(lambda d: d.value, directions))
    from random import shuffle
    shuffle(directions)
    return iter(directions)


def all_directions(as_points: bool = True) -> Iterable[Direction or Point]:
    directions = [_ for _ in Direction]
    if as_points:
        directions = list(map(lambda d: d.value, directions))
    from random import shuffle
    shuffle(directions)
    return iter(directions)


class BuildArea:
    def __init__(self, build_area_json=None):
        if build_area_json is None:
            build_area_json = requestBuildArea()
        XFROM, XTO, ZFROM, ZTO = 'xFrom', 'xTo', 'zFrom', 'zTo'

        for (key1, key2, tag) in {(XFROM, XTO, 'X'), (ZFROM, ZTO, 'Z')}:
            if build_area_json[key1] == build_area_json[key2]:
                raise ValueError("lower {} and upper {} bounds must be different !".format(tag, tag))
            elif build_area_json[key1] > build_area_json[key2]:
                build_area_json[key1], build_area_json[key2] = build_area_json[key2], build_area_json[key1]

        self.__origin: Point = Point(build_area_json[XFROM], build_area_json[ZFROM])
        self.__destination: Point = Point(build_area_json[XTO], build_area_json[ZTO]) + Point(1, 1)
        self.__shape: Point = abs(self.__destination - self.__origin)

    def __contains__(self, item):
        assert isinstance(item, Point)
        return (self.x <= item.x < self.__destination.x) and (self.z <= item.z < self.__destination.z)

    @property
    def x(self):
        return self.__origin.x

    @property
    def z(self):
        return self.__origin.z

    @property
    def origin(self):
        return Point(self.x, self.z)

    @property
    def width(self):
        return self.__shape.x

    @property
    def length(self):
        return self.__shape.z

    @property
    def rect(self):
        return self.x, self.z, self.width, self.length

    def __str__(self):
        return f"build area of size {self.__shape} starting in {self.origin}"


class TransformBox(BoundingBox):
    """
    Adds class methods to the BoundingBox to transform the box's shape and position
    """

    def translate(self, dx=0, dy=0, dz=0, inplace=False):
        if isinstance(dx, Direction):
            return self.translate(dx.x, dx.y, dx.z, inplace)
        if inplace:
            self._origin += (dx, dy, dz)
            return self
        else:
            return TransformBox(self.origin + (dx, dy, dz), self.size)

    def split(self, dx=None, dy=None, dz=None):
        assert (dx is not None) ^ (dy is not None) ^ (dz is not None)
        if dx is not None:
            b0 = TransformBox(self.origin, (dx, self.height, self.length))
            b1 = TransformBox((self.origin + (dx, 0, 0)), (self.size - (dx, 0, 0)))
        elif dy is not None:
            b0 = TransformBox(self.origin, (self.width, dy, self.length))
            b1 = TransformBox((self.origin + (0, dy, 0)), (self.size - (0, dy, 0)))
        else:
            b0 = TransformBox(self.origin, (self.width, self.height, dz))
            b1 = TransformBox((self.origin + (0, 0, dz)), (self.size - (0, 0, dz)))
        return [b0, b1]

    def expand(self, dx_or_dir, dy=None, dz=None, inplace=False):
        # if isinstance(dx_or_dir, Direction):
        if isinstance(dx_or_dir, Direction):
            direction = dx_or_dir
            dpos = (min(direction.x, 0), min(direction.y, 0), min(direction.z, 0))
            dsize = (abs(direction.x), abs(direction.y), abs(direction.z))
            expanded_box = TransformBox(self.origin + dpos, self.size + dsize)
        else:
            expanded_box = TransformBox(BoundingBox.expand(self, dx_or_dir, dy, dz))
        return self.copy_from(expanded_box) if inplace else expanded_box

    def enlarge(self, direction, reverse=False, inplace=False):
        # type: (Direction, bool, bool) -> TransformBox
        """
        For example, TransformBox((0, 0, 0), (1, 1, 1)).expand(East) -> TransformBox((-1, 0, 0), (3, 1, 1))
        """
        copy_box = TransformBox(self.origin, self.size)
        dx, dz = 1 - abs(direction.x), 1 - abs(direction.z)
        if reverse:
            dx, dz = -dx, -dz
        copy_box = copy_box.expand(dx, 0, dz)
        if inplace:
            self.copy_from(copy_box)
        else:
            return copy_box

    def copy_from(self, other):
        self._origin = other.origin
        self._size = other.size
        return self

    def __sub__(self, other):
        # type: (TransformBox) -> TransformBox
        """
        exclusion operator, only works if self is an extension of other in a single direction
        should work well with self.expand(Direction), eg box.expand(South) - box -> southern extension of box
        """
        same_coords = [self.minx == other.minx, self.maxx == other.maxx, self.minz == other.minz,
                       self.maxz == other.maxz]
        assert sum(same_coords) == 3  # only one of the 4 bool should be False
        if not same_coords[0]:  # supposedly self.minx < other.minx
            return self.split(dx=1)[0]
        elif not same_coords[1]:  # supposedly self.minx < other.minx
            return self.split(dx=self.width - 1)[1]
        elif not same_coords[2]:  # supposedly self.minx < other.minx
            return self.split(dz=1)[0]
        else:  # supposedly self.minx < other.minx
            return self.split(dz=self.length - 1)[1]

    def closest_border(self, px, z=None, relative_coords=False):
        """Gets the border point of self closer to the input point"""
        if z is not None:
            return self.closest_border(Point(px, z), None, relative_coords)

        if relative_coords:
            px = Point(px.x + self.minx, px.z + self.minz)

        if self.is_lateral(px.x, px.z):
            return px - Point(self.minx, self.minz) if relative_coords else px

        xm, zm = (self.minx + self.maxx) // 2, (self.minz + self.maxz) // 2
        corners = [Point(self.minx, zm), Point(self.maxx-1, zm), Point(xm, self.minz), Point(xm, self.maxz-1)]
        distance = [euclidean(px, _) for _ in corners]
        from numpy import argmin
        i = argmin(distance)
        if i == 0:
            return Point(0, px.z - self.minz) if relative_coords else Point(self.minx, px.z)
        elif i == 1:
            return Point(self.width - 1, px.z - self.minz) if relative_coords else Point(self.maxx - 1, px.z)
        elif i == 2:
            return Point(px.x - self.minx, 0) if relative_coords else Point(px.x, self.minz)
        else:
            return Point(px.x - self.minx, self.length - 1) if relative_coords else Point(px.x, self.maxz - 1)

    def is_corner(self, new_gate_pos):
        return self.is_lateral(new_gate_pos.x) and self.is_lateral(None, new_gate_pos.z)

    def is_lateral(self, x=None, z=None):
        assert x is not None or z is not None
        if x is None:
            return z == self.minz or z == self.maxz - 1
        if z is None:
            return x == self.minx or x == self.maxx - 1
        else:
            return self.is_lateral(x, None) or self.is_lateral(None, z)


    @property
    def surface(self):
        return self.width * self.length


if __name__ == '__main__':
    print(Direction.East, Direction.East.value, Direction.East.name)
    print(list(all_directions(False)))
