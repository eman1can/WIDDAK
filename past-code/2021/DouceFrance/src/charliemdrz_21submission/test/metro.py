# coding=utf-8
from __future__ import division

from typing import Dict, Set, List, Iterable

import numpy as np

from pymclevel.block_copy import copyBlocksFrom
from pymclevel.block_fill import fillBlocks
from terrain import Maps
from utils import *

# TODO: stations -> génération des quais + entrée ?
# TODO: jingles ? noms de stations ?

all_but_rails = [_ for _ in Materials if ("Rail" not in str(_) and "Redstone" not in str(_))]


def hermit_curve(p0, q0, p1, q1):
    # type: (Point2D, Point2D, Point2D, Point2D) -> Iterable[Point2D]

    def hermit(t):
        hp0 = (1 - t) ** 2 * (1 + 2 * t)

        hp1 = t ** 2 * (3 - 2 * t)

        hq0 = t * (1 - t) ** 2

        hq1 = -(t ** 2) * (1 - t)

        return ((p0 * hp0) + (p1 * hp1) + (q0 * hq0) + (q1 * hq1)).toInt

    distance = int(manhattan(p0, p1))
    curve = {hermit(i / distance).toInt for i in range(distance + 1)}
    ordered_curve = sorted(curve, key=lambda pt: euclidean(p0, pt))
    return ordered_curve


def place_accelerator(level, p1, p2, y=None):
    assert euclidean(p1, p2) == 1
    assert isinstance(p1, Point3D) or (isinstance(p1, Point2D) and y is not None)
    if isinstance(p1, Point3D):
        y = p1.y
    direction_str = axis_dir(Direction.from_point(p2 - p1))
    setMaterial(level, p1.x, y + 1, p1.z, Materials["Detector Rail (Unpowered, {})".format(direction_str)])
    setMaterial(level, p1.x, y, p1.z, Materials["Cobblestone"])
    setMaterial(level, p2.x, y + 1, p2.z, Materials["Powered Rail (Unpowered, {})".format(direction_str)])
    setMaterial(level, p2.x, y, p2.z, Materials["Cobblestone"])


class RailElement(object):
    def __init__(self, origin, destination):
        assert isinstance(origin, Point2D)
        assert isinstance(destination, Point2D)
        self._connectors = [origin, destination]  # type: List[Point2D]

    def generate(self, level, height):
        pass

    def other_end(self, end):
        assert end in self._connectors
        if end == self._connectors[0]:
            return self._connectors[1]
        else:
            return self._connectors[0]

    @property
    def width(self):
        return 1 + abs(self._connectors[0].x - self._connectors[1].x)

    @property
    def length(self):
        return 1 + abs(self._connectors[0].z - self._connectors[1].z)

    @property
    def isStraight(self):
        return self.width == 1 or self.length == 1

    @property
    def minx(self):
        return min(_.x for _ in self._connectors)

    @property
    def minz(self):
        return min(_.z for _ in self._connectors)


class RailConnector(Point2D):
    CAPACITY = 2

    def __init__(self, position):
        Point2D.__init__(self, position.x, position.z)
        self.__neighbours = {}  # type: Dict[Direction, RailElement]
        self.__x_orientation = False  # type: bool

    def branch(self, new_edge):
        assert not self.is_full
        other_conn = new_edge.other_end(self)
        railway_vector = other_conn - self
        edge_dir = Direction(dx=railway_vector.x, dz=railway_vector.z)

        if self.__neighbours:
            old_edge = self.__neighbours.values()[0]
            if old_edge.isStraight:
                edge_dir = -self.__neighbours.keys()[0]
            elif new_edge.isStraight:
                self.__neighbours.clear()
                self.__neighbours[-edge_dir] = old_edge
        self.__neighbours[edge_dir] = new_edge
        self.__compute_orientation()

    def other_end(self, end):
        l = list(self.__neighbours.values())
        assert end in l
        if end is l[0]:
            return l[1]
        else:
            return l[0]

    @property
    def is_full(self):
        return len(self.__neighbours) == self.CAPACITY

    @property
    def nodes(self):
        dp = Point2D(1, 0) if self.__x_orientation else Point2D(0, 1)
        return self - dp, self + dp

    def __compute_orientation(self):
        if North in self.__neighbours.keys() or South in self.__neighbours.keys():
            self.__x_orientation = True
        elif East in self.__neighbours.keys() or West in self.__neighbours.keys():
            self.__x_orientation = False
        # neighbours = self.__neighbours.values()
        # if len(neighbours) > 0 and neighbours[0].isStraight:
        #     line = neighbours[0]
        # elif len(neighbours) > 1 and neighbours[1].isStraight:
        #     line = neighbours[1]
        # else:
        #     line = None
        #
        # if line:
        #     self.__x_orientation = (line.width == 1)

    def direction(self, neighbour):
        assert neighbour in self.__neighbours.values()
        return [_ for (_, value) in self.__neighbours.items() if value == neighbour][0]

    def getNodes(self, direction):
        # type: (Direction) -> (Point2D, Point2D)
        return self - direction.rotate().asPoint2D, self + direction.rotate().asPoint2D


class RailWay(RailElement):
    DIST_BTWN_LIGHTS = 6

    def __init__(self, connector1, connector2):
        # type: (RailConnector, RailConnector) -> None
        assert isinstance(connector1, RailConnector)
        assert isinstance(connector2, RailConnector)
        RailElement.__init__(self, connector1, connector2)
        self._connectors = [connector1, connector2]  # type: List[RailConnector]
        self._tracks = []  # type: List[Rails]

    def generate(self, level, height):
        # get rails
        d0, d1 = self._connectors[0].direction(self), self._connectors[1].direction(self)
        p0, q0 = self._connectors[0].getNodes(d0)
        p1, q1 = self._connectors[1].getNodes(d1)
        # todo: clear the way first ? then gen tracks, then gen lights and decorations (?)
        # generate tracks
        self._tracks.append(Rails(p0, d0, q1, d1, not self._connectors[1].other_end(self).isStraight))
        self._tracks.append(Rails(p1, d1, q0, d0, not self._connectors[0].other_end(self).isStraight))
        map(lambda way: way.generate(level, height), self._tracks)

        # generate lights, clear the way
        lights = []
        distance = manhattan(self._connectors[0], self._connectors[1])
        p0, p1 = self._connectors[0], self._connectors[1]
        q0, q1 = d0.asPoint2D * (distance // 2), d1.asPoint2D * (-distance // 2)
        for curve_p in hermit_curve(p0, q0, p1, q1):
            x, z = curve_p.x, curve_p.z
            # if there are no lights or all lights are far enough and the position is unoccupied, place torch
            underground = level.blockAt(x, height + 3, z) in ground_blocks_ID
            if lights == [] or euclidean(curve_p, lights[-1]) > self.DIST_BTWN_LIGHTS:
                lights.append(curve_p)
                if underground:
                    setMaterial(level, x, height + 3, z, Materials["Sea Lantern"])
                elif level.blockAt(x, height + 1, z) == 0:
                    setMaterial(level, x, height + 1, z, Materials["Oak Fence"])
                    setMaterial(level, x, height + 2, z, Materials["Torch (Up)"])
                    if level.blockAt(x, height, z) == 0:
                        setMaterial(level, x, height, z, Materials["Oak Wood Planks"])
            if not underground:
                clear_tree_at(level, BoundingBox((x - 5, 0, z - 5), (11, 255, 11)), curve_p)


class Rails(RailElement):
    DIST_BTWN_ACCELERATION = 16

    def __init__(self, connector1, direction1, connector2, direction2, links_to_curve):
        RailElement.__init__(self, connector1, connector2)
        self.__in = Point2D(connector1.x, connector1.z)  # type: Point2D
        self.__out = Point2D(connector2.x, connector2.z)  # type: Point2D
        self.__in_dir = direction1  # type: Direction
        self.__out_dir = direction2  # type: Direction
        self.__late_acceleration = links_to_curve

    def generate(self, level, height):
        if self.isStraight:
            self.__gen_straight_rail(level, height)
        else:
            self.__gen_spline_rail(level, height)

    def __gen_straight_rail(self, level, height):
        origin = (self.minx, height, self.minz)
        size = (self.width, 1, self.length)
        box = TransformBox(origin, size)
        fillBlocks(box, Materials["Cobblestone"])
        box.translate(dy=1, inplace=True)
        tunnel_box = box.expand(1, 0, 0) if self.length > self.width else box.expand(0, 0, 1)
        tunnel_box.expand(Top, inplace=True)

        fillBlocks(tunnel_box, Materials["Air"])
        material = Materials["Rail (North/South)"] if (self.width == 1) else Materials["Rail (East/West)"]
        fillBlocks(box, material, [Materials["Air"]])

        tunnel_box.translate(dy=1)
        fillBlocks(tunnel_box, Materials["Stone"], [Materials["Sand"], Materials["Gravel"]])

        accelerator_count = max(self.width, self.length) // self.DIST_BTWN_ACCELERATION
        for count in range(max(accelerator_count, 1)):
            position = self.__in_dir.asPoint2D * self.DIST_BTWN_ACCELERATION * count
            place_accelerator(level, self.__in + position, self.__in + position + self.__in_dir.asPoint2D, height)
        if self.__late_acceleration:
            place_accelerator(level, self.__out + self.__out_dir.asPoint2D, self.__out, height)

    def __gen_spline_rail(self, level, height):
        # todo: generate accelerators where possible ?
        n_points = int(manhattan(self.__in, self.__out))
        p0, p1 = self.__in, self.__out  # interpolation targets
        q0, q1 = self.__in_dir.asPoint2D * (n_points / 2), self.__out_dir.asPoint2D * (
                -n_points / 2)  # osculation targets
        accelerators = []

        def find_missing_point(_p1, _p2):
            distance = euclidean(_p1, _p2)
            direction = self.__in_dir
            for _ in range(4):
                new_point = _p1 + direction.asPoint2D
                if euclidean(new_point, _p2) < distance:
                    return new_point
                else:
                    direction = direction.rotate()

        def find_rail_block(dir1, dir2):
            if dir1 == dir2 or dir1 == -dir2:
                dir_str = axis_dir(dir1)
                if accelerators == [] or all(manhattan(a, cur_p) > self.DIST_BTWN_ACCELERATION for a in accelerators):
                    accelerators.append(cur_p)
                    return Materials["Powered Rail (Powered, {})".format(dir_str)]
                else:
                    return Materials["Rail ({})".format(dir_str)]
            else:
                rail_direction = dir1.asPoint2D + dir2.asPoint2D
                rail_x_dir = "East" if rail_direction.x == 1 else "West"
                rail_z_dir = "South" if rail_direction.z == 1 else "North"
                return Materials["Rail (Curved, {}/{})".format(rail_z_dir, rail_x_dir)]

        def build_rail_block(x, y, z, block):
            box = TransformBox((x - 1, y + 1, z - 1), (3, 2, 3))
            fillBlocks(box, Materials["Air"], all_but_rails)
            box.translate(dy=1, inplace=True)
            fillBlocks(box, Materials["Stone"], [Materials["Sand"]])
            setMaterial(level, x, y, z, b)
            if level.blockAt(int(x), int(y) + 1, int(z)) == 0:
                setMaterial(level, x, y + 1, z, block)
            if block.stringID == 'golden_rail':
                normal_direction = in_dir.rotate()
                setMaterial(level, x + normal_direction.x, y, z + normal_direction.z, Materials["Cobblestone"])
                setMaterial(level, x + normal_direction.x, y + 1, z + normal_direction.z,
                            Materials["Redstone Torch (Up)"])

        curve = list(hermit_curve(p0, q0, p1, q1))
        # curve = [self.__in]
        # for spline_index in range(n_points+1):
        #     spline_param = spline_index / n_points
        #     curve_point = hermit(p0, q0, p1, q1, spline_param).toInt
        #     if not curve_point == curve[-1]:
        #         curve.append(curve_point)
        b = Materials["Cobblestone"]

        in_dir = self.__in_dir
        while curve:
            cur_p = curve[0]

            if len(curve) > 1:
                nxt_p = curve[1]
                if euclidean(cur_p, nxt_p) > 1:
                    nxt_p = find_missing_point(cur_p, nxt_p)
                    curve.insert(1, nxt_p)
                nxt_dir = Direction(dx=(nxt_p.x - cur_p.x), dz=(nxt_p.z - cur_p.z))
            else:
                nxt_dir = self.__out_dir

            rail_block = find_rail_block(in_dir, nxt_dir)
            build_rail_block(cur_p.x, height, cur_p.z, rail_block)
            in_dir = -nxt_dir
            curve.remove(cur_p)

    @property
    def isStraight(self):
        x_straight = self.length == 1 and (self.__in_dir.x * self.__out_dir.x == -1)
        z_straight = self.width == 1 and (self.__in_dir.z * self.__out_dir.z == -1)
        return x_straight or z_straight

    @property
    def direction(self):
        return self.__in_dir

    @property
    def entry(self):
        return self.__in

    @property
    def exit(self):
        return self.__out


def axis_dir(direction):
    if direction == North or direction == South:
        return "North/South"
    elif direction == East or direction == West:
        return "East/West"
    raise ValueError


class TrainStation(RailWay):

    def __init__(self, connector1, connector2):
        super(TrainStation, self).__init__(connector1, connector2)
        origin = (min(connector1.x, connector2.x), 0, min(connector1.z, connector2.z))
        self._structure_box = TransformBox(origin, (self.width, 1, self.length))  # type: TransformBox

    def generate(self, level, height):
        super(TrainStation, self).generate(level, height)
        center = Point3D(self.minx + (self.width - 1) // 2, height, self.minz + (self.length - 1) // 2)
        self.__generate_metro_station(level, center)
        for track in self._tracks:
            stop_block = center - (track.direction.asPoint2D * 3) - track.direction.rotate().asPoint2D
            # stop_block = track.entry + track.direction.asPoint2D * ((euclidean(track.entry, track.exit) - 6)//2)
            place_accelerator(level, stop_block, stop_block + track.direction.asPoint2D)

            # block palette
            powr_block = Materials["Powered Rail (Powered, {})".format(axis_dir(track.direction))]
            rail_block = Materials["Rail ({})".format(axis_dir(track.direction))]
            ston_block = Materials["Stone"]
            dust_block = Materials["Redstone Dust (Power 0)"]
            rptr_block = Materials["Redstone Repeater (Unpowered, Delay 4, {})".format(-track.direction)]
            trch_block = Materials["Redstone Torch ({})".format(track.direction)]

            # blocks used for each level
            level0 = [rail_block] + 3 * [powr_block] + [rail_block]
            levelm2 = [dust_block, dust_block, rptr_block, ston_block, trch_block]

            # generation
            x, y, z = stop_block.x, height + 1, stop_block.z
            dx, dz = track.direction.x, track.direction.z
            for index in range(5):
                setMaterial(level, x + dx * index, y - 3, z + dz * index, ston_block)  # red stone mechanism support
                setMaterial(level, x + dx * index, y - 2, z + dz * index, levelm2[index])  # red stone mechanism
                setMaterial(level, x + dx * (index + 2), y, z + dz * (index + 2), level0[index])  # stop&go rails

    def __generate_metro_station(self, level, center):
        # type: (MCLevel, Point3D) -> None
        """
        Generates a metro station in the style of Paris Metropolitain.
        The generation code is written for a station where the rails go in the X direction (East/West).
        When the rails are in the North/South direction, the X station is generated in a schematic, rotated, then placed
        in the actual level
        """
        box = self._structure_box = TransformBox((center.x - 5, center.y + 1, center.z - 5), (11, 6, 11))

        def generate_x_station(__level, __box):

            # Station walls and ceiling
            fillBlocks(__box, Materials["Block of Quartz"])
            fillBlocks(__box.expand(-1, -1, -1), Materials["Air"])

            # Platform
            platform_box = __box.expand(-1, 0, -1).split(dy=1)[0]
            fillBlocks(platform_box, Materials["Stone"])
            platform_edge_box = platform_box.split(dz=2)[1].split(dz=1)[0]
            fillBlocks(platform_edge_box, Materials["Stone Brick Stairs (Bottom, North)"])
            fillBlocks(platform_edge_box.translate(dz=4), Materials["Stone Brick Stairs (Bottom, South)"])

            # Ceiling
            ceiling_box = platform_edge_box.translate(dy=5, dz=2)
            fillBlocks(ceiling_box.translate(dy=-1, dz=-4), Materials["Stone Brick Stairs (Top, North)"])
            fillBlocks(ceiling_box.translate(dy=-1, dz=4), Materials["Stone Brick Stairs (Top, South)"])
            fillBlocks(ceiling_box.translate(dz=-3), Materials["Stone Bricks"])
            fillBlocks(ceiling_box.translate(dz=-2), Materials["Stone Brick Stairs (Top, North)"])
            fillBlocks(ceiling_box.translate(dz=-1), Materials["Stone Brick Slab (Top)"])
            fillBlocks(ceiling_box.translate(dz=0), Materials["Chiseled Stone Bricks"])
            fillBlocks(ceiling_box.translate(dz=1), Materials["Stone Brick Slab (Top)"])
            fillBlocks(ceiling_box.translate(dz=2), Materials["Stone Brick Stairs (Top, South)"])
            fillBlocks(ceiling_box.translate(dz=3), Materials["Stone Bricks"])

            # Rails
            rail_box = __box.expand(0, 0, -4).split(dy=2)[0]
            fillBlocks(__box.expand(0, 0, -4).split(dy=2)[0], Materials.Air)
            rail_box = rail_box.split(dy=1)[0]
            fillBlocks(rail_box.translate(dy=-1), Materials["Cobblestone"])
            fillBlocks(rail_box, Materials["Rail (East/West)"])
            fillBlocks(rail_box.expand(0, 0, -1), Materials["Standing Sign (South)"])

            for x in [__box.minx + 3, __box.minx + 7]:
                setMaterial(__level, x, __box.miny + 3, __box.minz + 5, Materials["Sea Lantern"])
                setMaterial(__level, x, __box.miny + 4, __box.minz + 5, Materials["Oak Fence"])

        if self.width < self.length:
            from pymclevel import MCSchematic
            schematic = MCSchematic(box.size + (0, 1, 0))
            schem_box = TransformBox((0, 1, 0), box.size)
            generate_x_station(schematic, schem_box)
            schematic.rotateLeft()
            copyBlocksFrom(level, schematic, sourceBox=schem_box.expand(Bottom),
                           destinationPoint=box.origin - (0, 1, 0))
            sign_box = BoundingBox((box.minx + 5, box.miny, box.minz), (1, 1, box.length))
            fillBlocks(sign_box, Materials.Air)
            fillBlocks(sign_box, Materials["Standing Sign (East)"])
        else:
            generate_x_station(level, box)


class RailroadNet:
    def __init__(self, maps):
        self.__maps = maps  # type: Maps
        self.__limits = maps.box
        self.__elements = set()  # type: Set[RailWay]
        self.__connectors = {}  # type: Dict[Point2D, RailConnector]
        # self.__network = {}  # type: Dict[RailConnector, List[RailElement]] # adjacency list graph

    def add_edge(self, p1, p2, is_station=False):
        # type: (Point2D, Point2D, bool) -> None

        for p in [p1, p2]:
            if p not in self.__connectors:
                self.__connectors[p] = RailConnector(p)
        c1, c2 = self.__connectors[p1], self.__connectors[p2]
        new_edge = TrainStation(c1, c2) if is_station else RailWay(c1, c2)

        c1.branch(new_edge)
        c2.branch(new_edge)
        self.__elements.add(new_edge)

    def generate(self, level):
        box_height = self.__maps.height_map.box_height(self.__limits, use_relative_coords=False)
        metro_y = int(np.percentile(box_height, 50))
        for rail in self.__elements:
            rail.generate(level, metro_y)


displayName = "Metro test"

inputs = ()


def perform(level, box, options):
    # type: (MCLevel, BoundingBox, object) -> None
    print(options)
    maps = Maps(level, TransformBox(box))
    metro = RailroadNet(maps)
    x0, z0, w, l = box.minx, box.minz, box.width, box.length
    # nodes = [Point2D(x0 + w//10, z0), Point2D(x0 + w//10, z0 + l//2), Point2D(x0 + w//2, z0 + l*9//10),
    #          Point2D(x0 + w, z0 + l*9//10)]
    # for p1, p2 in zip(nodes[:-1], nodes[1:]):
    #     metro.add_edge(p1, p2)
    nodes = [Point2D(x0 + w // 10, z0 + l * 3 // 10), Point2D(x0 + w // 10, z0 + l * 7 // 10),
             Point2D(x0 + w * 3 // 10, z0 + l * 9 // 10),
             Point2D(x0 + w * 7 // 10, z0 + l * 9 // 10), Point2D(x0 + w * 9 // 10, z0 + l * 7 // 10),
             Point2D(x0 + w * 9 // 10, z0 + l * 3 // 10), Point2D(x0 + w * 7 // 10, z0 + l // 10),
             Point2D(x0 + w * 3 // 10, z0 + l // 10)]
    for p1, p2 in zip(nodes, nodes[1:] + [nodes[0]]):
        is_station = (p1 == nodes[0]) or (p1 == nodes[2])
        metro.add_edge(p1, p2, is_station)
    metro.generate(level)
