from __future__ import division

from math import ceil, sqrt
from random import randint, random
from typing import List

from numpy.random import choice
from utilityFunctions import raytrace

from generation import Generator
from generation.road_generator import Bridge
from pymclevel import MCLevel, BoundingBox, MCInfdevOldLevel
from pymclevel.block_fill import fillBlocks
from terrain import HeightMap
from terrain.maps import Maps
from utils import TransformBox, Point2D, Direction, Materials, cardinal_directions, Point3D, manhattan, euclidean, \
    clear_tree_at, product, array, place_torch

displayName = "Bridge generator test filter"

inputs = (("type", ("Bridge", "Stair")), ("Creator: Charlie", "label"))


def perform(level, box, options):
    # type: (MCLevel, BoundingBox, dict) -> None
    box = TransformBox(box)
    print("Selected zone: {}".format(box))
    maps = Maps(level, box)
    assert box.width > 3 and box.length > 3

    if box.width > box.length:
        x1, x2 = 0, box.width - 1
        z1, z2 = randint(1, box.length - 2), randint(1, box.length - 2)
    else:
        x1, x2 = randint(1, box.width - 2), randint(1, box.width - 2)
        z1, z2 = 0, box.length - 1

    p1, p2 = Point2D(x1, z1), Point2D(x2, z2)
    if options["type"] == "Bridge":
        h = maps.height_map.box_height(box, use_relative_coords=False)
        bridge = Bridge(p1, Point2D(box.minx, box.minz))
        bridge += p2
        bridge.generate(level, h)
    else:
        stair = RampStairs(p1, p2, maps.height_map)
        stair.translate(box.minx, 0, box.minz)
        h = maps.height_map.box_height(stair._box, use_relative_coords=False)
        print("Generating ramp stairs: {}".format(stair))
        stair.generate(level, h)


class RampStairs(Generator):
    RAMP_WIDTH = 2  # ramp stair width
    RAMP_LENGTH = 3  # ramp stair min length

    def __init__(self, p1, p2, height_map):
        # type: (Point2D, Point2D, HeightMap) -> None
        y1, y2 = height_map.fluid_height(p1), height_map.fluid_height(p2)
        if y2 < y1:
            p1, p2, y1, y2 = p2, p1, y2, y1
        self.__direction = Direction(dx=p2.x - p1.x, dz=p2.z - p1.z)
        self.__entry3d = Point3D(p1.x, y1, p1.z) + self.__direction.asPoint2D
        self.__exit3d = Point3D(p2.x, y2, p2.z) - self.__direction.asPoint2D
        dy = abs(height_map.fluid_height(p2) - height_map.fluid_height(p1))
        width = abs(p1.x - p2.x) + 1
        length = abs(p1.z - p2.z) + 1
        size = max(width, length)
        self.__ramp_length = max(self.RAMP_LENGTH, int(ceil(dy * (self.RAMP_WIDTH + 1) / size)))
        self.__ramp_count = int(ceil(dy / self.__ramp_length)) + 1
        extended_ramp_length = self.__ramp_length + 2 * self.RAMP_WIDTH

        # build smaller box to contain origin and destination
        box = TransformBox((p1.x, y1, p1.z), (1, 1, 1))
        box = box.union(TransformBox((p2.x, y2, p2.z), (1, 1, 1)))

        # extend box to be larger than the longer ramp length
        if box.length < min(box.width, extended_ramp_length):
            box = box.expand(0, 0, (1+extended_ramp_length-box.length)//2)
        elif box.width < min(box.length, extended_ramp_length):
            box = box.expand((1+extended_ramp_length-box.width)//2, 0, 0)

        # extend box from min height to max height
        box = TransformBox((box.minx, 0, box.minz), (box.width, 256, box.length))

        Generator.__init__(self, box, p1)
        self.__height = height_map.box_height(self._box, True, True)
        self.__stored_edge_cost = {}

    def __generate_stairs(self, level, p1, p2, height):
        # type: (MCInfdevOldLevel, Point3D, Point3D, array) -> None
        assert p1.x == p2.x or p1.z == p2.z
        if p2.y < p1.y:
            p2, p1 = p1, p2
        stair_dir = Direction(dx=p2.x - p1.x, dz=p2.z - p1.z)
        # Compute building positions
        if p1.x == p2.x:
            if p1.z < p2.z:
                z_list = range(p1.z + 1, p2.z - 1)
            else:
                z_list = range(p1.z - 2, p2.z, -1)
            l = len(z_list)
            x_list = [p1.x - self.RAMP_WIDTH // 2] * l
            width, length = self.RAMP_WIDTH, 1
        else:
            if p1.x < p2.x:
                x_list = range(p1.x + 1, p2.x - 1)
            else:
                x_list = range(p1.x - 2, p2.x, -1)
            l = len(x_list)
            z_list = [p1.z - self.RAMP_WIDTH // 2] * l
            width, length = 1, self.RAMP_WIDTH
        y_list = [p1.y * (1 - _ / l) + p2.y * (_ / l) for _ in range(l)] + [p2.y]
        material_def = Materials["Stone Bricks"]
        for _ in range(l):
            x, z = x_list[_], z_list[_]
            y, y1 = int(round(y_list[_])), int(round(y_list[_ + 1]))
            if y < y1:
                material = Materials["Stone Brick Stairs (Bottom, {})".format(stair_dir)]
                material_opp = Materials["Stone Brick Stairs (Top, {})".format(-stair_dir)]
            else:
                material = material_def
                material_opp = None
            box = TransformBox((x, y1, z), (width, 1, length))
            clear_tree_at(level, box=BoundingBox((x - 5, 0, z - 5), (11, 256, 11)), point=Point2D(x, z))
            fillBlocks(level, box.translate(dy=2).expand(0, 1, 0), Materials[0])
            fillBlocks(level, box, material)
            y0 = min(self.__heightAt(Point2D(x, z), True, height) for x, _, z in box.positions)
            if abs(y0 - y) >= 3:
                if material_opp is not None:
                    fillBlocks(level, box.translate(dy=-1), material_opp, [Materials[0]])
            else:
                fillBlocks(level, BoundingBox((box.minx, y0, box.minz), (width, 1+y-y0, length)), material_def, [Materials[0]])

        e, w = self.RAMP_WIDTH // 2, self.RAMP_WIDTH
        y = min(p1.y, min(self.__heightAt(Point2D(p1.x+dx, p1.z+dz), True, height) for dx, dz in product(range(-e, w-e), range(-e, w-e))))
        box = TransformBox((p1.x - e, y, p1.z - e), (w, 1+p1.y-y, w))
        fillBlocks(level, box.translate(dy=2).expand(0, 1, 0), Materials[0])
        fillBlocks(level, box, Materials["Stone Bricks"])
        clear_tree_at(level, box, Point2D(box.minx, box.minz))
        # place_torch(level, randint(box.minx, box.maxx-1), box.maxy, randint(box.minz, box.maxz-1))
        if euclidean(p1, p2) > self.RAMP_WIDTH:
            place_torch(level, randint(box.minx, box.maxx-1), box.maxy, randint(box.minz, box.maxz-1))

        y = min(p2.y, min(self.__heightAt(Point2D(p2.x+dx, p2.z+dz), True, height) for dx, dz in product(range(-e, w-e), range(-e, w-e))))
        box = TransformBox((p2.x - e, y, p2.z - e), (w, 1+p2.y-y, w))
        fillBlocks(level, box.translate(dy=2).expand(0, 1, 0), Materials[0])
        fillBlocks(level, box, Materials["Stone Bricks"])
        clear_tree_at(level, box, Point2D(box.minx, box.minz))

    def __heightAt(self, pos, cast_to_int=False, height_map=None):
        # type: (Point2D, bool, array) -> int or float
        if height_map is None:
            height_map = self.__height
        f = height_map[pos.x - self.origin.x, pos.z - self.origin.z]
        if cast_to_int:
            return int(round(f))
        else:
            return f

    def __edge_cost(self, edge_begin, edge_end):
        # type: (Point3D, Point3D) -> float
        str_beg, str_end = str(edge_begin), str(edge_end)
        if str_beg in self.__stored_edge_cost and str_end in self.__stored_edge_cost[str_beg]:
            return self.__stored_edge_cost[str_beg][str_end]
        else:
            def pos_cost(x, y, z):
                h = self.__heightAt(Point2D(x, z))
                if 0 <= (y - h) <= 2:
                    return 1
                else:
                    return (1 + abs(y-h)) ** 2
            edge_points = raytrace(edge_begin.coords, edge_end.coords)
            v = sum(pos_cost(x, y, z) for x, y, z in edge_points)
            if str_beg not in self.__stored_edge_cost:
                self.__stored_edge_cost[str_beg] = {}
            self.__stored_edge_cost[str_beg][str_end] = v
            return v

    def __edge_interest(self, edge_begin, edge_end):
        distance_gain = max(euclidean(edge_begin, self.exit) - euclidean(edge_end, self.exit), abs(edge_end.y - edge_begin.y), 0)
        weight = self.__edge_cost(edge_begin, edge_end)
        return distance_gain / sqrt(weight)
        # return 1 + random()

    def __solution_cost(self, solution):
        # type: (List[Point3D]) -> float
        """
        Cost of the last computed solution (ramp_points), measure of quality
        Approximately represents the average difference btwn path height and altitude
        """
        res = sum(self.__edge_cost(edge[0], edge[1]) for edge in zip(solution[:-1], solution[1:]))
        if solution[-1] != self.exit:
            # additional penalty if path does not reach the exit
            res += self.__edge_cost(solution[-1], self.exit) + manhattan(solution[-1], self.exit)
        return sqrt(res) / manhattan(solution[0], self.exit)

    def __steepness(self, point, direction, margin=3):
        values = []
        h0 = self.__heightAt(point)
        for m in range(1, margin+1):
            if (point + direction.asPoint2D * m).coords in self._box:
                hm = self.__heightAt(point + direction.asPoint2D * m)
                values.append((hm - h0) / m)
            if (point - direction.asPoint2D * m).coords in self._box:
                hm1 = self.__heightAt(point - direction.asPoint2D * m)
                values.append((h0 - hm1) / m)
        return abs(sum(values) / len(values))

    def generate(self, level, height_map=None, palette=None):
        from time import time

        # print(self._box.size)
        # print(height_map.shape)
        self.__height = self.__height.astype(float)
        mrg = self.RAMP_WIDTH // 2
        for x, z in product(range(mrg, self.width - mrg), range(mrg, self.length - mrg)):
            self.__height[x, z] = self.__height[(x - mrg):(x + mrg + 1), (z - mrg):(z + mrg + 1)].mean()

        def terminate():
            # type: () -> bool
            """
            Ending condition for the solution search: ends after some max time or time since last improving solution
            """
            return (time() - t0) > 20 or (t1 > t0 and (time() - t1) > 5)

        def close_to_exit(pos):
            # type: (Point3D) -> bool
            ex, ey, ez = self.exit.coords
            px, py, pz = pos.coords
            if ex != px and ez != pz:
                # Not close enough
                return False
            elif max(abs(ex-px), abs(ez-pz)) < (abs(ey-py) + self.RAMP_WIDTH):
                # too much height difference
                return False
            else:
                return self.__solution_cost([pos, self.exit]) < 1

        def buildRandomSolution(edge_interest):
            _ramp_points = [self.__entry3d]  # type: List[Point3D]

            # Add an edge while exit is not reached
            while _ramp_points[-1] != self.exit:
                cur_p = _ramp_points[-1]

                # Compute directions to extend to
                if len(_ramp_points) == 1:
                    valid_directions = [self.__direction, self.__direction.rotate(), -self.__direction.rotate()]
                else:
                    prev_p = _ramp_points[-2]  # previous point
                    prev_d = Direction(dx=cur_p.x - prev_p.x, dz=cur_p.z - prev_p.z)  # previous direction
                    valid_directions = set(cardinal_directions())
                    for d in {-prev_d, -self.__direction}:
                        valid_directions.remove(d)  # cannot go back
                    if manhattan(cur_p, prev_p) <= self.RAMP_WIDTH:
                        valid_directions.remove(prev_d)  # avoids repeated baby steps

                # Explore all those directions
                next_p, next_cost = None, None
                while valid_directions:
                    cur_d = valid_directions.pop()  # type: Direction
                    if self.__steepness(cur_p, cur_d, self.RAMP_WIDTH) >= 2:
                        # steep direction, add a step to turn left or right
                        next_point_list = [cur_p + cur_d.asPoint2D * self.RAMP_WIDTH]
                    else:
                        # Compute random extensions in that direction
                        min_length = self.RAMP_LENGTH + self.RAMP_WIDTH
                        max_length = 1 + self.__ramp_length + self.RAMP_WIDTH
                        next_point_list = [cur_p + cur_d.asPoint2D * min_length]
                        while len(next_point_list) <= max_length - min_length and next_point_list[-1].coords in self._box:
                            p = next_point_list[-1] + cur_d.asPoint2D  # one step ahead
                            e = abs((p - cur_p).dot(cur_d.asPoint2D)) - self.RAMP_WIDTH  # max ramp height from cur_p to p
                            if p.x == self.exit.x and p.z == self.exit.z and cur_p.y-e <= self.exit.y <= cur_p.y+e:
                                return _ramp_points + [self.exit]
                            else:
                                h = self.__heightAt(p, True) if p.coords in self._box else cur_p.y  # altitude at that point
                                if cur_p.y < self.exit.y:
                                    y = max(min(h, cur_p.y + e), cur_p.y)  # forbids going down while below target height
                                else:
                                    y = max(min(h, cur_p.y + e), cur_p.y - e)  # constrained altitude
                                next_point_list.append(Point3D(p.x, y, p.z))

                    if next_point_list[-1].coords not in self._box:
                        next_point_list.pop(-1)

                    if self.exit in next_point_list:
                        return _ramp_points + [self.exit]
                    elif any(close_to_exit(_) for _ in next_point_list):
                        next_p = next(_ for _ in next_point_list if close_to_exit(_))
                        return _ramp_points + [next_p, self.exit]
                    elif next_point_list:
                        weights = [edge_interest(cur_p, _) for _ in next_point_list]
                        if sum(weights) == 0:
                            continue
                        index = choice(range(len(weights)), p=map(lambda _: _ / sum(weights), weights))
                        # index = argmax(weights)
                        if next_p is None or weights[index] > next_cost:
                            next_p, next_cost = next_point_list[index], weights[index]
                if next_p is not None:
                    _ramp_points.append(next_p)
                else:
                    break

            return _ramp_points

        # function init
        t0 = t1 = time()
        best_ramp = []
        best_cost = -1
        explored_solutions = 0
        while not terminate():
            edge_func = (lambda _: 1) if ((time() - t0) > 10 and best_ramp is None) else self.__edge_interest
            ramp_points = buildRandomSolution(edge_func)
            explored_solutions += 1
            c = self.__solution_cost(ramp_points)
            if ramp_points[-1] == self.exit and (not best_ramp or c < best_cost):
                print("Cost decreased to {}".format(c))
                best_cost = c
                best_ramp = ramp_points
                t1 = time()

        print("Explored {} solutions in {} seconds".format(explored_solutions, time()-t0))
        for p1, p2 in zip(best_ramp[:-1], best_ramp[1:]):
            print("Building stairs from {} to {}".format(p1, p2))
            self.__generate_stairs(level, p1, p2, height_map)

    def translate(self, dx=0, dy=0, dz=0):
        Generator.translate(self, dx, dy, dz)
        self.__entry3d += Point3D(dx, dy, dz)
        self.__exit3d += Point3D(dx, dy, dz)

    def __str__(self):
        return "stairs from {} to {}, oriented {}".format(self.__entry3d, self.__exit3d, self.__direction)

    @property
    def exit(self):
        return self.__exit3d
