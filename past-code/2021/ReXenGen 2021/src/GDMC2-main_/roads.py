import numpy as np
import maths
import math
import main
import map
import schematic
import interfaceUtils as minecraft
import random

from PIL import Image
from collections import Counter

alreadyGenerated = []


######################## Lanes materials presets #######################


standard_modern_lane_composition = {
    "road_surface": {
        "black_concrete": 3,
        "coal_block": 1,
        "black_concrete_powder": 2,
    },
    "median_strip": {"stone": 1},
    "structure": {"stone": 3, "andesite": 1},
    "central_lines": {"yellow_concrete": 3, "yellow_concrete_powder": 1},
    "external_lines": {"white_concrete": 3, "white_concrete_powder": 1},
    "lines": {"white_concrete": 3, "white_concrete_powder": 1},
}


######################### Additional functions #########################


def cleanLanes(lanes):
    cleanLanes = {}
    for lane in lanes:
        for xyz in lanes[lane]:
            if (round(xyz[0]), round(xyz[1]), round(xyz[2]),) not in [
                cleanLanes[i][j]
                for __, i in enumerate(cleanLanes)
                for j in range(len(cleanLanes[i]))
            ]:
                if cleanLanes.get(lane) == None:
                    cleanLanes[lane] = []
                cleanLanes[lane].append(
                    (round(xyz[0]), round(xyz[1]), round(xyz[2]))
                )
    return cleanLanes


############################ Lanes functions ###########################

housesCoordinates = []


def singleLaneLeft(XYZ, blocks=standard_modern_lane_composition):
    """Left side."""

    factor = 8
    distance = 2

    roadMarkings = maths.curveSurface(
        np.array(XYZ),
        distance + 1,
        resolution=0,
        pixelPerfect=True,
        factor=1,
        start=2,
    )
    roadMarkings = cleanLanes(roadMarkings)

    roadSurface = maths.curveSurface(
        np.array(XYZ),
        distance,
        resolution=0,
        pixelPerfect=False,
        factor=factor,
    )
    roadSurface = cleanLanes(roadSurface)

    walkway = maths.curveSurface(
        np.array(XYZ),
        distance + 3,
        resolution=0,
        pixelPerfect=False,
        factor=4,
        start=3,
    )
    walkway = cleanLanes(walkway)

    houses = maths.curveSurface(
        np.array(XYZ),
        distance + 14,
        resolution=0,
        pixelPerfect=False,
        factor=1,
        start=distance + 13,
    )
    houses = cleanLanes(houses)

    road_surface = blocks.get("road_surface")
    structure = blocks.get("structure")

    for lane in roadSurface:
        for xyz in roadSurface[lane]:
            main.fillBlock(
                "air", (xyz[0], xyz[1], xyz[2], xyz[0], xyz[1] + 4, xyz[2])
            )
            main.setBlock(
                random.choices(
                    list(structure.keys()),
                    weights=structure.values(),
                    k=1,
                )[0],
                (xyz[0], xyz[1] - 1, xyz[2]),
            )
            main.setBlock(
                random.choices(
                    list(road_surface.keys()),
                    weights=road_surface.values(),
                    k=1,
                )[0],
                xyz,
            )
            alreadyGenerated.append((xyz[0], xyz[2]))

    lines = blocks.get("lines")
    for lane in roadMarkings:
        for xyz in roadMarkings[lane]:
            if lane == -1:
                main.setBlock(
                    random.choices(
                        list(structure.keys()),
                        weights=structure.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] - 1, xyz[2]),
                )
                main.setBlock(
                    random.choices(
                        list(lines.keys()),
                        weights=lines.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1], xyz[2]),
                )

    for lane in walkway:
        for xyz in walkway[lane]:
            if lane <= -1:
                counterSegments = 0
                main.fillBlock(
                    "air",
                    (xyz[0], xyz[1] + 1, xyz[2], xyz[0], xyz[1] + 4, xyz[2]),
                )
                main.fillBlock(
                    random.choices(
                        list(structure.keys()),
                        weights=structure.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] + 1, xyz[2], xyz[0], xyz[1] - 1, xyz[2]),
                )
                alreadyGenerated.append((xyz[0], xyz[2]))

    counterSegments = 0
    for lane in houses:
        for xyz in houses[lane]:
            if lane <= -1:
                counterSegments += 1
                if counterSegments % 10 == 0:
                    housesCoordinates.append((xyz[0], xyz[1], xyz[2]))


def singleLaneRight(XYZ, blocks=standard_modern_lane_composition):
    """Right side."""

    factor = 8
    distance = 2

    roadMarkings = maths.curveSurface(
        np.array(XYZ),
        distance + 1,
        resolution=0,
        pixelPerfect=True,
        factor=1,
        start=2,
    )
    roadMarkings = cleanLanes(roadMarkings)

    roadSurface = maths.curveSurface(
        np.array(XYZ),
        distance,
        resolution=0,
        pixelPerfect=False,
        factor=factor,
    )
    roadSurface = cleanLanes(roadSurface)

    walkway = maths.curveSurface(
        np.array(XYZ),
        distance + 3,
        resolution=0,
        pixelPerfect=False,
        factor=4,
        start=3,
    )
    walkway = cleanLanes(walkway)

    houses = maths.curveSurface(
        np.array(XYZ),
        distance + 14,
        resolution=0,
        pixelPerfect=False,
        factor=1,
        start=distance + 13,
    )
    houses = cleanLanes(houses)

    road_surface = blocks.get("road_surface")
    structure = blocks.get("structure")
    central_lines = blocks.get("central_lines")

    for lane in roadSurface:
        for xyz in roadSurface[lane]:
            main.fillBlock(
                "air", (xyz[0], xyz[1], xyz[2], xyz[0], xyz[1] + 4, xyz[2])
            )
            main.setBlock(
                random.choices(
                    list(structure.keys()),
                    weights=structure.values(),
                    k=1,
                )[0],
                (xyz[0], xyz[1] - 1, xyz[2]),
            )
            main.setBlock(
                random.choices(
                    list(road_surface.keys()),
                    weights=road_surface.values(),
                    k=1,
                )[0],
                xyz,
            )
            alreadyGenerated.append((xyz[0], xyz[2]))

    lines = blocks.get("lines")
    counterSegments = 0
    for lane in roadMarkings:
        for xyz in roadMarkings[lane]:
            if lane == 1:
                main.setBlock(
                    random.choices(
                        list(structure.keys()),
                        weights=structure.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] - 1, xyz[2]),
                )
                main.setBlock(
                    random.choices(
                        list(lines.keys()),
                        weights=lines.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1], xyz[2]),
                )

            if lane == -1:  # Central Lane.
                counterSegments += 1
                if counterSegments % 4 != 0:
                    main.setBlock(
                        random.choices(
                            list(structure.keys()),
                            weights=structure.values(),
                            k=1,
                        )[0],
                        (xyz[0], xyz[1] - 1, xyz[2]),
                    )
                    main.setBlock(
                        random.choices(
                            list(central_lines.keys()),
                            weights=central_lines.values(),
                            k=1,
                        )[0],
                        (xyz[0], xyz[1], xyz[2]),
                    )
                else:
                    main.setBlock(
                        random.choices(
                            list(structure.keys()),
                            weights=structure.values(),
                            k=1,
                        )[0],
                        (xyz[0], xyz[1] - 1, xyz[2]),
                    )
                    main.setBlock(
                        random.choices(
                            list(road_surface.keys()),
                            weights=road_surface.values(),
                            k=1,
                        )[0],
                        (xyz[0], xyz[1], xyz[2]),
                    )

    for lane in walkway:
        for xyz in walkway[lane]:
            if lane >= 1:
                main.fillBlock(
                    "air",
                    (xyz[0], xyz[1] + 1, xyz[2], xyz[0], xyz[1] + 4, xyz[2]),
                )
                main.fillBlock(
                    random.choices(
                        list(structure.keys()),
                        weights=structure.values(),
                        k=1,
                    )[0],
                    (xyz[0], xyz[1] + 1, xyz[2], xyz[0], xyz[1] - 1, xyz[2]),
                )
                alreadyGenerated.append((xyz[0], xyz[2]))

    counterSegments = 0
    for lane in houses:
        for xyz in houses[lane]:
            if lane >= 1:
                counterSegments += 1
                if counterSegments % 10 == 0:
                    housesCoordinates.append((xyz[0], xyz[1], xyz[2]))


############################ Roads Generator ###########################


class RoadCurve:
    def __init__(self, roadData, XYZ):
        print("road, first input:", XYZ)
        """Create points that forms the lanes depending of the roadData."""
        self.roadData = roadData
        self.XYZ = XYZ

        # Find the offset, where the lanes is.
        self.lanesXYZ = {}
        for __, i in enumerate(self.roadData["lanes"]):
            laneCenterDistance = self.roadData["lanes"][i]["centerDistance"]
            self.lanesXYZ[i] = maths.curveSurface(
                np.array(XYZ),
                abs(laneCenterDistance),
                resolution=0,
                pixelPerfect=True,
                factor=1,
                start=abs(laneCenterDistance) - 1,
                returnLine=False,
            )
            # We only take the desired side.
            if laneCenterDistance == 0:
                self.lanesXYZ[i] = self.lanesXYZ[i][0]
            if laneCenterDistance > 0:
                self.lanesXYZ[i] = self.lanesXYZ[i][1]
            if laneCenterDistance < 0:
                self.lanesXYZ[i] = self.lanesXYZ[i][-1]

    def setLanes(self, lanes=[]):
        """Generate the lanes depending of the function name."""
        for __, i in enumerate(self.roadData["lanes"]):
            if i in lanes or lanes == []:
                self.roadData["lanes"][i]["type"](np.array(self.lanesXYZ[i]))

    def getLanes(self, lanes=[]):
        """Return the points that forms the lanes."""
        lanesDict = {}
        for __, i in enumerate(self.roadData["lanes"]):
            if i in lanes or lanes == []:
                lanesDict[i] = self.lanesXYZ[i]
        return lanesDict


def intersection(
    roadsData, centerPoint, mainRoads, sideRoads
):  # TODO: Refactoring. Error with y in curve.
    """
    [summary]

    [extended_summary]

    Args:
        roadsData (dict): standard_modern_lanes_agencement
        centerPoint (tuple): (x, y, z)
        mainRoads (list): {0:((x, y, z), (x, y, z)), 1:((x, y, z), (x, y, z))}
        sideRoads ([type]): {0:[(x, y, z), 1:(x, y, z), -1:(x, y, z), 2:(x, y, z)}
    """
    # Save all the lanes.
    lanes = {}

    # Set the side roads.
    for i in roadsData["sideRoads"]:
        sideRoad = RoadCurve(
            roadsData["sideRoads"].get(i), (sideRoads.get(i), centerPoint)
        )
        sideRoad.setLanes()
        lanes[sideRoads[i]] = sideRoad.getLanes()

    # Set the main roads.
    for i in roadsData["mainRoads"]:
        mainLanes = []
        mainRoad = RoadCurve(
            roadsData["mainRoads"].get(i), (mainRoads.get(i)[0], centerPoint)
        )
        mainRoad.setLanes()
        lanes[mainRoads[i][0]] = mainRoad.getLanes()
        mainLanes.append(mainRoad.getLanes())
        # We don't want to inverse the orientation of the main road.
        mainRoad = RoadCurve(
            roadsData["mainRoads"].get(i), (centerPoint, mainRoads.get(i)[1])
        )
        mainRoad.setLanes()
        # But we want to save it like the others.
        mainRoad = RoadCurve(
            roadsData["mainRoads"].get(i),
            (
                mainRoads.get(i)[1],
                centerPoint,
            ),
        )
        lanes[mainRoads[i][1]] = mainRoad.getLanes()
        mainLanes.append(mainRoad.getLanes())

        # # Compute the curve of the main road.
        # center = ()
        # for j in list(mainRoad.getLanes().keys()):

        #     line0 = (mainLanes[0][j][0], mainLanes[0][j][1])
        #     line1 = (mainLanes[1][j][0], mainLanes[1][j][1])

        #     intersectionPointsTemp, center = maths.curveCornerIntersectionLine(
        #         line0, line1, 70, angleAdaptation=False, center=center
        #     )

        #     y = 205
        #     intersectionPoints = []
        #     [
        #         intersectionPoints.append((round(xz[0]), y, round(xz[1])))
        #         for xz in intersectionPointsTemp
        #         if (round(xz[0]), y, round(xz[1])) not in intersectionPoints
        #     ]
        #     print(intersectionPointsTemp, center)

        #     singleLane2(
        #         intersectionPoints, blocks=standard_modern_lane_composition
        #     )

    # Sort all the points in rotation order.
    points = []
    points.extend([xyz[i] for xyz in mainRoads.values() for i in range(2)])
    points.extend([xyz for xyz in sideRoads.values()])
    points = maths.sortRotation(points)

    # Compute the curve between each road.
    for i in range(len(points)):
        line0 = (
            lanes[points[i]][max(lanes[points[i]])][0],
            lanes[points[i]][max(lanes[points[i]])][1],
        )
        line1 = (
            lanes[points[i - 1]][min(lanes[points[-1]])][0],
            lanes[points[i - 1]][min(lanes[points[-1]])][1],
        )

        # Compute the curve.
        intersectionPointsTemp = maths.curveCornerIntersectionLine(
            line0, line1, 10, angleAdaptation=False
        )[0]

        y = centerPoint[1]  # Not the real y here
        intersectionPoints = []
        [
            intersectionPoints.append((round(xz[0]), y, round(xz[1])))
            for xz in intersectionPointsTemp
            if (round(xz[0]), y, round(xz[1])) not in intersectionPoints
        ]
        diffAlt = abs(line0[0][1] - line1[0][1])
        maxAlt = max(line0[0][1], line1[0][1])
        print(diffAlt, maxAlt, len(intersectionPoints))
        if diffAlt != 0:
            step = len(intersectionPoints) // diffAlt
        else:
            step = 1
        for i in range(len(intersectionPoints)):
            print(i)
            intersectionPoints[i] = (
                intersectionPoints[i][0],
                maxAlt - (i // step),
                intersectionPoints[i][2],
            )

        singleLaneRight(
            intersectionPoints, blocks=standard_modern_lane_composition
        )

        # # Generate the curve.
        # for key, value in lanes.items():
        #     for __, value1 in value.items():
        #         if intersectionPoints[0] in value1:
        #             # Key found.
        #             for __, j in enumerate(mainRoads):
        #                 if key in mainRoads[j]:
        #                     curveRoad = RoadCurve(
        #                         roadsData["mainRoads"][j], intersectionPoints
        #                     )
        #                     curveRoad.setLanes(
        #                         [max(roadsData["mainRoads"][j]["lanes"])]
        #                     )
        #             # for __, j in enumerate(sideRoads):
        #             #     print(sideRoads[j])
        #             #     if key == sideRoads[j]:
        #             #         print(
        #             #             roadsData["sideRoads"][j], intersectionPoints
        #             #         )
        #             #         curveRoad = Road(
        #             #             roadsData["sideRoads"][j], intersectionPoints
        #             #         )
        #             #         curveRoad.setLanes(
        #             #             [min(roadsData["sideRoads"][j]["lanes"])]
        #             #         )


############################# Lanes Preset #############################


standard_modern_lane_agencement = {
    "lanes": {
        -1: {"type": singleLaneLeft, "centerDistance": -3},
        1: {"type": singleLaneRight, "centerDistance": 3},
    },
}


standard_modern_lanes_agencement = {
    "mainRoads": {
        0: {
            "lanes": {
                -1: {"type": singleLaneLeft, "centerDistance": -5},
                0: {"type": singleLaneLeft, "centerDistance": 0},
                1: {"type": singleLaneRight, "centerDistance": 5},
            }
        },
        1: {
            "lanes": {
                -1: {"type": singleLaneRight, "centerDistance": -5},
                0: {"type": singleLaneRight, "centerDistance": 0},
                1: {"type": singleLaneRight, "centerDistance": 5},
            }
        },
    },
    "sideRoads": {
        0: {
            "lanes": {
                -1: {"type": singleLaneLeft, "centerDistance": -5},
                1: {"type": singleLaneLeft, "centerDistance": 0},
                2: {"type": singleLaneLeft, "centerDistance": 5},
            }
        },
        1: {
            "lanes": {
                -1: {"type": singleLaneLeft, "centerDistance": -5},
                1: {"type": singleLaneLeft, "centerDistance": 0},
                2: {"type": singleLaneLeft, "centerDistance": 5},
            }
        },
    },
}


if __name__ == "__main__":
    debug = False

    # Find the area.
    area = minecraft.requestBuildArea()
    area = map.areaCoordinates(
        (area["xFrom"], area["zFrom"]), (area["xTo"], area["zTo"])
    )
    print("area:", area)

    # Generate data to work with.
    map.heightmap(
        area[0],
        area[1],
        mapName="heightmap.png",
        biomeName="heightmap_biome.png",
    )
    map.blur("heightmap_biome.png", name="heightmap_biome.png", factor=11)
    map.sobel("heightmap.png")
    map.blur("heightmap_biome.png", name="heightmap_medianBlur.png", factor=11)
    pixel_graph_row, pixel_graph_col, pixel_graph_data, coordinates = map.skel(
        "heightmap_medianBlur.png", "heightmap_skeletonize.png"
    )
    lines, intersections, center = map.parseGraph(
        pixel_graph_row, pixel_graph_col
    )

    if debug:
        print(center)
        print(lines)
        print(intersections)

    # Colorization

    # Lines
    path = "heightmap_skeletonize_color.png"
    im = Image.open("heightmap_skeletonize.png")
    width, height = im.size
    # img = Image.new(mode="RGB", size=(width, height))
    img = Image.open("heightmap_sobel.png")
    for i in range(len(lines)):
        r, g, b = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        for j in range(len(lines[i])):
            img.putpixel(
                (
                    int(coordinates[lines[i][j]][0]),
                    int(coordinates[lines[i][j]][1]),
                ),
                (r + j, g + j, b + j),
            )
    img.save(path, "PNG")

    # Centers
    img = Image.open(path)
    for i in range(len(center)):
        if debug:
            print(coordinates[center[i]])
        img.putpixel(
            (int(coordinates[center[i]][0]), int(coordinates[center[i]][1])),
            (255, 255, 0),
        )
    img.save(path, "PNG")

    # Intersections
    for i in range(len(intersections)):
        intersection = []
        for j in range(len(intersections[i])):
            intersection.append(coordinates[intersections[i][j]])
        if debug:
            print(intersection)

        img = Image.open(path)
        for i in range(len(intersection)):
            img.putpixel(
                (int(intersection[i][0]), int(intersection[i][1])),
                (255, 0, 255),
            )
        img.save(path, "PNG")

    # Generation
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            xz = map.irlToMc(area[0], coordinates[lines[i][j]])
            lines[i][j] = xz

    # Simplification
    from simplification.cutil import simplify_coords

    for i in range(len(lines)):
        if debug:
            print(lines[i])
        lines[i] = simplify_coords(lines[i], 1.0)

    for i in range(len(lines)):
        for j in range(len(lines[i])):
            xyz = map.findGround(area[0], lines[i][j])
            lines[i][j] = xyz

    for i in range(len(lines)):  # HERE --------------------------------------
        road = RoadCurve(standard_modern_lane_agencement, lines[i])
        road.setLanes()
        # print(road.getLanes(), "LANES ***********")

    # i = 5
    # road = RoadCurve(standard_modern_lane_agencement, lines[i])
    # road.setLanes()
    rejected = []
    accepted = []
    # print(housesCoordinates)
    for i in range(len(housesCoordinates)):
        pos = housesCoordinates[i]
        # print(pos, "pos0")
        base = map.findGround(area[0], pos)
        if base != None:
            # print(pos, "pos1")
            pos1 = (
                pos[0] - random.randint(3, 6),
                base[1],
                pos[2] - random.randint(3, 6),
            )
            pos2 = (
                pos[0] + random.randint(3, 6),
                base[1],
                pos[2] + random.randint(3, 6),
            )
            pos3 = (
                pos1[0],
                base[1],
                pos2[2],
            )
            pos4 = (
                pos2[0],
                base[1],
                pos1[2],
            )
            # print(pos1, pos2, pos3, pos4, "pos")
            Ypos1 = map.findGround(area[0], pos1)
            Ypos2 = map.findGround(area[0], pos2)
            Ypos3 = map.findGround(area[0], pos3)
            Ypos4 = map.findGround(area[0], pos4)

            if (
                Ypos1 != None
                and Ypos2 != None
                and Ypos3 != None
                and Ypos4 != None
            ):

                pos2 = (
                    pos2[0],
                    max(Ypos1[1], Ypos2[1], base[1], Ypos3[1], Ypos4[1]),
                    pos2[2],
                )
                pos1 = (
                    pos1[0],
                    max(Ypos1[1], Ypos2[1], base[1], Ypos3[1], Ypos4[1]),
                    pos1[2],
                )
                if (
                    (pos1[0], pos1[2]) not in alreadyGenerated
                    and (
                        pos2[0],
                        pos2[2],
                    )
                    not in alreadyGenerated
                    and (pos1[0], pos2[2]) not in alreadyGenerated
                    and (pos2[0], pos1[2])
                ):  # HERE, remove print and find why house gen on self

                    for xi in range(
                        -5,
                        (max(pos1[0], pos2[0]) - min(pos1[0], pos2[0])) + 5,
                    ):
                        for yi in range(
                            -5,
                            (max(pos1[2], pos2[2]) - min(pos1[2], pos2[2]))
                            + 5,
                        ):
                            alreadyGenerated.append(
                                (
                                    min(pos1[0], pos2[0]) + xi,
                                    min(pos1[2], pos2[2]) + yi,
                                )
                            )

                    door = ["south", "north", "east", "west"]
                    cb = random.randint(0, 3)
                    schematic.house(
                        pos1,
                        pos2,
                        door[cb],
                        random.randint(0, 1),
                        min(Ypos1[1], Ypos2[1], base[1], Ypos3[1], Ypos4[1]),
                    )
                    accepted.append(
                        (
                            pos1[0],
                            pos1[2],
                            pos2[0],
                            pos2[2],
                        )
                    )
                else:
                    rejected.append(
                        (
                            pos1[0],
                            pos1[2],
                            pos2[0],
                            pos2[2],
                        )
                    )

#     standard_modern_lane_agencement,
#     (
#         (70, 70 + 15, -20),
#         (160, 68 + 15, -128),
#         (235, 64 + 15, -215),
#     ),
# )

# roadTest.setLanes()


# intersection(
#     standard_modern_lanes_agencement,
#     (150, 140, -150),
#     {
#         0: ((200, 140, -80), (100, 140, -115)),
#         1: ((120, 140, -80), (200, 140, -150)),
#     },
#     {0: (50, 140, -200), 1: (150, 140, -200), 2: (175, 140, -175)},
# )

# intersection(
#     standard_modern_lanes_agencement,
#     (300, 130, 100),
#     {
#         0: ((300, 130, 0), (300, 130, 200)),
#         1: ((250, 130, 150), (350, 130, -50)),
#     },
#     {0: (400, 130, 200), 1: (250, 130, 50)},
# )


# roadTest = Road(
#     standard_modern_lane_agencement,
#     (
#         (70, 70 + 15, -20),
#         (160, 68 + 15, -128),
#         (235, 64 + 15, -215),
#     ),
# )

# roadTest.setLanes()