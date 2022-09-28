import time
from math import (
    sqrt,
    tan,
    sin,
    cos,
    pi,
    ceil,
    floor,
    acos,
    atan,
    asin,
    degrees,
    radians,
    log,
    atan2,
    acos,
    asin,
)
from random import *
from numpy import *
import random

from setup import getBlock, fill, in_BuildingPlot
import setup

url = "http://localhost:9000/command"
USE_BATCHING = False


def setBlock(block, x, y, z):
    if USE_BATCHING:
        setup.placeBlockBatched(x, y, z, block, 100)
    else:
        setup.setBlock(x, y, z, block)


def cutinterior(pos1, pos2, doorpos):
    if doorpos[0][0] > doorpos[1][0]:
        temp = doorpos[0][0]
        doorpos[0][0] = doorpos[1][0]
        doorpos[1][0] = temp
    if doorpos[0][2] > doorpos[1][2]:
        temp = doorpos[0][2]
        doorpos[0][2] = doorpos[1][2]
        doorpos[1][2] = temp
    length = pos2[0] - pos1[0] + 1
    width = pos2[2] - pos1[2] + 1
    typelist = {}
    for x in range(length):
        typelist[x + pos1[0]] = {}
        for z in range(width):
            if x not in range(1, length - 1) or z not in range(1, width - 1):
                typelist[x + pos1[0]][z + pos1[2]] = "white"
            else:
                typelist[x + pos1[0]][z + pos1[2]] = "gray"
    for door in doorpos:
        typelist[door[0]][door[2]] = "brown"
        estate = door
    finish = False
    d, d1 = 0, 0
    while not finish:
        if (d1 == 0 or d1 == 1) and d < 2:
            for x in range(-1, 2, 2):
                try:
                    if typelist[estate[0] + x][estate[2]] == "gray":
                        typelist[estate[0] + x][estate[2]] = "blue"
                        estate = [estate[0] + x, 0, estate[2]]
                        if d1 == 0:
                            direc = x
                        enter, d, d1 = "x", d + 1, 2
                except:
                    pass
        if (d1 == 0 or d1 == 2) and d < 2:
            for z in range(-1, 2, 2):
                try:
                    if typelist[estate[0]][estate[2] + z] == "gray":
                        typelist[estate[0]][estate[2] + z] = "blue"
                        estate = [estate[0], 0, estate[2] + z]
                        if d1 == 0:
                            direc = z
                        enter, d, d1 = "z", d + 1, 1
                except:
                    pass
        if d == len(doorpos):
            finish = True
    walldoor = False
    for xpos in typelist:
        for zpos in typelist[xpos]:
            if typelist[xpos][zpos] == "blue":
                for x in range(-1, 2, 2):
                    if typelist[xpos + x][zpos] == "white":
                        walldoor = True
                        estate = [xpos, 0, zpos]
                for z in range(-1, 2, 2):
                    if typelist[xpos][zpos + z] == "white":
                        walldoor = True
                        estate = [xpos, 0, zpos]
                typelist[xpos][zpos] = "gray"
    if walldoor:
        for doors in doorpos:
            if enter == "x":
                estate = [doors[0], doors[1], doors[2] + direc]
                for z in range(-1, 2, 2):
                    try:
                        if typelist[estate[0]][estate[2] + z] == "white":
                            estate[2] += z
                            nowhite = estate
                    except:
                        pass
            if enter == "z":
                estate = [doors[0] + direc, doors[1], doors[2]]
                for x in range(-1, 2, 2):
                    try:
                        if typelist[estate[0] + x][estate[2]] == "white":
                            estate[0] += x
                            nowhite = estate
                    except:
                        pass
    else:
        estate = [doorpos[1][0], doorpos[1][1], doorpos[1][2]]
        walltest = ""
        while walltest != "white":
            if enter == "x" and length < 10:
                estate[0] = estate[0] + 1
                walltest, nowithe = (
                    typelist[estate[0]][estate[2] + direc],
                    estate,
                )
            elif enter == "x" and length > 10:
                walltest = "white"
                estate = [doorpos[1][0], doorpos[1][1], doorpos[1][2] + direc]
            if enter == "z" and width < 10:
                estate[2] = estate[2] + 1
                walltest, nowhite = (
                    typelist[estate[0] + direc][estate[2]],
                    estate,
                )
            elif enter == "z" and length > 10:
                walltest = "white"
                estate = [doorpos[1][0] + direc, doorpos[1][1], doorpos[1][2]]
    finish = False
    while not finish:
        if enter == "x":
            if length <= 10:
                typeb = False
                while not typeb:
                    for x in range(-1, 2, 2):
                        try:
                            if typelist[estate[0] + x][estate[2]] == "gray":
                                (
                                    typelist[estate[0] + x][estate[2]],
                                    typelist[estate[0] + x][estate[2] + direc],
                                ) = ("blue", "blue")
                                estate = [estate[0] + x, 0, estate[2]]
                            elif (
                                typelist[estate[0] + x][estate[2]] == "white"
                                and estate[0] + x != nowhite[0]
                            ):
                                typeb = True
                        except:
                            pass
            else:
                coorl, executed, estate2 = (
                    length // 2,
                    0,
                    [doorpos[0][0], doorpos[0][1], doorpos[0][2] + direc],
                )
                while executed < coorl:
                    for x in range(-1, 2, 2):
                        try:
                            if typelist[estate[0] + x][estate[2]] == "gray":
                                (
                                    typelist[estate[0] + x][estate[2]],
                                    typelist[estate[0] + x][estate[2] + direc],
                                    typelist[estate[0] + x][
                                        estate[2] + 2 * direc
                                    ],
                                ) = ("blue", "blue", "blue")
                                try:
                                    if (
                                        typelist[estate2[0] - x][estate2[2]]
                                        == "gray"
                                    ):
                                        (
                                            typelist[estate2[0] - x][
                                                estate2[2]
                                            ],
                                            typelist[estate2[0] - x][
                                                estate2[2] + direc
                                            ],
                                            typelist[estate2[0] - x][
                                                estate2[2] + 2 * direc
                                            ],
                                        ) = ("blue", "blue", "blue")
                                except:
                                    pass
                                estate, estate2 = [
                                    estate[0] + x,
                                    0,
                                    estate[2],
                                ], [estate2[0] - x, 0, estate2[2]]
                                executed += 2
                            if typelist[estate[0] + x][estate[2]] == "white":
                                temp = estate
                                estate, estate2 = estate2, temp
                        except:
                            pass
            estate = [doorpos[0][0], 0, doorpos[0][2] + direc]
            walltest = ""
            while walltest != "white":
                estate[0] = estate[0] + 1
                walltest = typelist[estate[0]][estate[2]]
            estate[0] -= 1
            while typelist[estate[0]][estate[2]] != "white":
                if typelist[estate[0]][estate[2]] == "gray":
                    typelist[estate[0]][estate[2]] = "orange"
                    tested = False
                    for x in range(-1, 2, 2):
                        if typelist[estate[0] + x][estate[2]] == "white":
                            (
                                typelist[estate[0]][estate[2] + direc],
                                typelist[estate[0]][estate[2] + 2 * direc],
                            ) = ("orange", "orange")
                            tested = True
                        elif not tested:
                            (
                                typelist[estate[0]][estate[2] + direc],
                                typelist[estate[0]][estate[2] + 2 * direc],
                            ) = ("blue", "blue")
                estate[0] -= 1

        elif enter == "z":
            if width <= 10:
                typeb = False
                while not typeb:
                    for z in range(-1, 2, 2):
                        try:
                            if typelist[estate[0]][estate[2] + z] == "gray":
                                (
                                    typelist[estate[0]][estate[2] + z],
                                    typelist[estate[0] + direc][estate[2] + z],
                                ) = ("blue", "blue")
                                estate = [estate[0], 0, estate[2] + z]
                            elif (
                                typelist[estate[0]][estate[2] + z] == "white"
                                and estate[2] + z != nowhite[2]
                            ):
                                typeb = True
                        except:
                            pass
            else:
                coorw, executed, estate2 = (
                    width // 2,
                    0,
                    [doorpos[0][0] + direc, doorpos[0][1], doorpos[0][2]],
                )
                while executed < coorw:
                    for z in range(-1, 2, 2):
                        try:
                            if typelist[estate[0]][estate[2] + z] == "gray":
                                (
                                    typelist[estate[0]][estate[2] + z],
                                    typelist[estate[0] + direc][estate[2] + z],
                                    typelist[estate[0] + 2 * direc][
                                        estate[2] + z
                                    ],
                                ) = ("blue", "blue", "blue")
                                try:
                                    if (
                                        typelist[estate2[0]][estate2[2] - z]
                                        == "gray"
                                    ):
                                        (
                                            typelist[estate2[0]][
                                                estate2[2] - z
                                            ],
                                            typelist[estate2[0] + direc][
                                                estate2[2] - z
                                            ],
                                            typelist[estate2[0] + 2 * direc][
                                                estate2[2] - z
                                            ],
                                        ) = ("blue", "blue", "blue")
                                except:
                                    pass
                                estate, estate2 = [
                                    estate[0],
                                    0,
                                    estate[2] + z,
                                ], [estate2[0], 0, estate2[2] - z]
                                executed += 2
                            if typelist[estate[0]][estate[2] + z] == "white":
                                temp = estate
                                estate, estate2 = estate2, temp
                        except:
                            pass
            estate = [doorpos[0][0] + direc, 0, doorpos[0][2]]
            walltest = ""
            while walltest != "white":
                estate[2] = estate[2] + 1
                walltest = typelist[estate[0]][estate[2]]
            estate[2] -= 1
            while typelist[estate[0]][estate[2]] != "white":
                if typelist[estate[0]][estate[2]] == "gray":
                    typelist[estate[0]][estate[2]] = "orange"
                    tested = False
                    for z in range(-1, 2, 2):
                        if typelist[estate[0]][estate[2] + z] == "white":
                            (
                                typelist[estate[0] + direc][estate[2]],
                                typelist[estate[0] + 2 * direc][estate[2]],
                            ) = ("orange", "orange")
                            tested = True
                        elif not tested:
                            (
                                typelist[estate[0] + direc][estate[2]],
                                typelist[estate[0] + 2 * direc][estate[2]],
                            ) = ("blue", "blue")
                estate[2] -= 1
        finish = True
    return typelist


def colorinterior(typelist):
    for x in range(pos1[0], pos2[0] + 1):
        for z in range(pos1[2], pos2[2] + 1):
            color = typelist[x][z] + "_wool"
            setBlock(color, x, 3, z)


pos1 = (67, 3, 25)
pos2 = (67 + 12, 3, 37)
typel = cutinterior(pos1, pos2, [[79, 4, 27], [79, 4, 28]])
colorinterior(typel)


def house(pos1, pos2, door, varwall, base):

    mat = [
        "oak_log",
        "oak_planks",
        "oak_stairs",
        "white_terracotta",
        "stone",
        "stone_stairs",
        "oak_door",
        "stone_stairs",
        "glass_pane",
        "spruce_stairs",
        "spruce_planks",
        "spruce_slab",
        "oak_slab",
    ]
    # -------- Foundations --------#
    avpos = [pos1[0], pos1[1], pos1[2], pos2[0], pos2[1], pos2[2]]
    avpos2 = [
        pos1[0] - 2,
        pos1[1],
        pos1[2] - 2,
        pos2[0] + 2,
        base,
        pos2[2] + 2,
    ]
    fill(mat[4], avpos2)
    avpos2 = [
        pos1[0] + 1,
        pos1[1],
        pos1[2] + 1,
        pos2[0] - 1,
        pos2[1],
        pos2[2] - 1,
    ]
    fill(mat[1], avpos2)

    # -------- Walls --------#
    xlen = pos2[0] - pos1[0]
    zlen = pos2[2] - pos1[2]
    if varwall == 1:
        mat[1], mat[3] = mat[3], mat[1]

    # type 1
    avpos[1], avpos[4] = avpos[1] + 1, avpos[4] + 1
    fill(mat[0], avpos)
    avpos[1], avpos[4] = avpos[1] + 1, avpos[4] + 3
    fill(mat[1], avpos)
    avpos[0], avpos[1], avpos[2], avpos[3], avpos[5] = (
        avpos[0] + 1,
        avpos[1] - 1,
        avpos[2] + 1,
        avpos[3] - 1,
        avpos[5] - 1,
    )
    fill("air", avpos)
    avpos3 = [pos1[0], pos1[1] + 4, pos1[2], pos2[0], pos2[1] + 4, pos2[2]]
    fill(mat[1], avpos3)

    # -------- Windows & Door --------#
    middle1 = int(ceil((abs(pos1[0] - pos2[0]) + 1) / 2))
    middle2 = int(ceil((abs(pos1[2] - pos2[2]) + 1) / 2))

    # step 1
    y = pos1[1]
    x1, x2 = pos1[0], pos2[0]
    for x in range(0, middle1 + 1, 4):
        if middle1 - x >= 4:
            z = pos1[2]
            # Face 1
            temppos = [x1 + x + 1, y + 2, z, x1 + x + 2, y + 3, z]
            fill(mat[8], temppos)
            temppos = [x2 - x - 1, y + 2, z, x2 - x - 2, y + 3, z]
            fill(mat[8], temppos)

            z = pos2[2]
            # Face 2
            temppos = [x1 + x + 1, y + 2, z, x1 + x + 2, y + 3, z]
            fill(mat[8], temppos)
            temppos = [x2 - x - 1, y + 2, z, x2 - x - 2, y + 3, z]
            fill(mat[8], temppos)

        elif middle1 - x >= 1:
            z = pos1[2]
            # Face 1
            temppos = [x1 + middle1 - 1, y + 2, z, x1 + middle1 - 1, y + 3, z]
            fill(mat[8], temppos)
            temppos = [x2 - middle1 + 1, y + 2, z, x2 - middle1 + 1, y + 3, z]
            fill(mat[8], temppos)

            z = pos2[2]
            # Face 2
            temppos = [x1 + middle1 - 1, y + 2, z, x1 + middle1 - 1, y + 3, z]
            fill(mat[8], temppos)
            temppos = [x2 - middle1 + 1, y + 2, z, x2 - middle1 + 1, y + 3, z]
            fill(mat[8], temppos)

    # step 2
    y = pos1[1]
    z1, z2 = pos1[2], pos2[2]
    for z in range(0, middle2 + 1, 4):
        if middle2 - z >= 4:
            x = pos1[0]
            # Face 1
            temppos = [x, y + 2, z1 + z + 1, x, y + 3, z1 + z + 2]
            fill(mat[8], temppos)
            temppos = [x, y + 2, z2 - z - 1, x, y + 3, z2 - z - 2]
            fill(mat[8], temppos)

            x = pos2[0]
            # Face 2
            temppos = [x, y + 2, z1 + z + 1, x, y + 3, z1 + z + 2]
            fill(mat[8], temppos)
            temppos = [x, y + 2, z2 - z - 1, x, y + 3, z2 - z - 2]
            fill(mat[8], temppos)

        elif middle2 - z >= 1:
            x = pos1[0]
            # Face 1
            temppos = [x, y + 2, z1 + middle2 - 1, x, y + 3, z1 + middle2 - 1]
            fill(mat[8], temppos)
            temppos = [x, y + 2, z2 - middle2 + 1, x, y + 3, z2 - middle2 + 1]
            fill(mat[8], temppos)

            x = pos2[0]
            # Face 2
            temppos = [x, y + 2, z1 + middle2 - 1, x, y + 3, z1 + middle2 - 1]
            fill(mat[8], temppos)
            temppos = [x, y + 2, z2 - middle2 + 1, x, y + 3, z2 - middle2 + 1]
            fill(mat[8], temppos)

    # step 3
    y = pos1[1] + 1
    if door == "north" or door == "south":
        if door == "north":
            z = pos1[2]
        if door == "south":
            z = pos2[2]
        posdoor = []
        for block in range(pos1[0] + 1, pos2[0]):
            tempblock = getBlock(block, y + 1, z)
            if tempblock == mat[8]:
                temppos = [block, y + 1, z]
                posdoor.append(temppos)
        a = len(posdoor) - 1
        b = random.randint(0, a)
        locdoor = posdoor[b][0]
        checka, checkb = getBlock(locdoor - 1, y + 1, z), getBlock(
            locdoor + 1, y + 1, z
        )
        if checka != mat[8] and checkb != mat[8]:
            if door == "south":
                setBlock("oak_door[hinge=left,facing=south]", locdoor, y, z)
                setBlock(
                    "oak_door[half=upper,hinge=left,facing=south]",
                    locdoor,
                    y + 1,
                    z,
                )
            if door == "north":
                setBlock("oak_door[hinge=left,facing=north]", locdoor, y, z)
                setBlock(
                    "oak_door[half=upper,hinge=left,facing=north]",
                    locdoor,
                    y + 1,
                    z,
                )
            setBlock(mat[1], locdoor, y + 2, z)
            doorpos = [[locdoor, y, z]]
        else:
            wood = (locdoor, y + 2, z, locdoor, y + 2, z)
            if door == "south":
                if checka == mat[8]:
                    setBlock(
                        "oak_door[hinge=left,facing=south]", locdoor, y, z
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=left,facing=south]",
                        locdoor,
                        y + 1,
                        z,
                    )
                    setBlock(
                        "oak_door[hinge=right,facing=south]", locdoor - 1, y, z
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=right,facing=south]",
                        locdoor - 1,
                        y + 1,
                        z,
                    )
                    wood = (locdoor, y + 2, z, locdoor - 1, y + 2, z)
                    doorpos = [[locdoor, y, z], [locdoor - 1, y, z]]
                if checkb == mat[8]:
                    setBlock(
                        "oak_door[hinge=right,facing=south]", locdoor, y, z
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=right,facing=south]",
                        locdoor,
                        y + 1,
                        z,
                    )
                    setBlock(
                        "oak_door[hinge=left,facing=south]", locdoor + 1, y, z
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=left,facing=south]",
                        locdoor + 1,
                        y + 1,
                        z,
                    )
                    wood = (locdoor, y + 2, z, locdoor + 1, y + 2, z)
                    doorpos = [[locdoor, y, z], [locdoor + 1, y, z]]
            if door == "north":
                if checka == mat[8]:
                    setBlock(
                        "oak_door[hinge=right,facing=north]", locdoor, y, z
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=right,facing=north]",
                        locdoor,
                        y + 1,
                        z,
                    )
                    setBlock(
                        "oak_door[hinge=left,facing=north]", locdoor - 1, y, z
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=left,facing=north]",
                        locdoor - 1,
                        y + 1,
                        z,
                    )
                    wood = (locdoor, y + 2, z, locdoor - 1, y + 2, z)
                    doorpos = [[locdoor, y, z], [locdoor - 1, y, z]]
                if checkb == mat[8]:
                    setBlock(
                        "oak_door[hinge=left,facing=north]", locdoor, y, z
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=left,facing=north]",
                        locdoor,
                        y + 1,
                        z,
                    )
                    setBlock(
                        "oak_door[hinge=right,facing=north]", locdoor + 1, y, z
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=right,facing=north]",
                        locdoor + 1,
                        y + 1,
                        z,
                    )
                    wood = (locdoor, y + 2, z, locdoor + 1, y + 2, z)
                    doorpos = [[locdoor, y, z], [locdoor + 1, y, z]]
            fill(mat[1], wood)

    if door == "east" or door == "west":
        if door == "west":
            x = pos1[0]
        if door == "east":
            x = pos2[0]
        posdoor = []
        for block in range(pos1[2] + 1, pos2[2]):
            tempblock = getBlock(x, y + 1, block)
            if tempblock == mat[8]:
                temppos = [x, y + 1, block]
                posdoor.append(temppos)
        a = len(posdoor) - 1
        b = random.randint(0, a)
        locdoor = posdoor[b][2]
        checka, checkb = getBlock(x, y + 1, locdoor - 1), getBlock(
            x, y + 1, locdoor + 1
        )
        if checka != mat[8] and checkb != mat[8]:
            if door == "west":
                setBlock("oak_door[hinge=left,facing=west]", x, y, locdoor)
                setBlock(
                    "oak_door[half=upper,hinge=left,facing=west]",
                    x,
                    y + 1,
                    locdoor,
                )
            if door == "east":
                setBlock("oak_door[hinge=left,facing=east]", x, y, locdoor)
                setBlock(
                    "oak_door[half=upper,hinge=left,facing=east]",
                    x,
                    y + 1,
                    locdoor,
                )
            setBlock(mat[1], x, y + 2, locdoor)
            doorpos = [[x, y, locdoor]]
        else:
            wood = (x, y + 2, locdoor, x, y + 2, locdoor)
            if door == "west":
                if checka == mat[8]:
                    setBlock("oak_door[hinge=left,facing=west]", x, y, locdoor)
                    setBlock(
                        "oak_door[half=upper,hinge=left,facing=west]",
                        x,
                        y + 1,
                        locdoor,
                    )
                    setBlock(
                        "oak_door[hinge=right,facing=west]", x, y, locdoor - 1
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=right,facing=west]",
                        x,
                        y + 1,
                        locdoor - 1,
                    )
                    wood = (x, y + 2, locdoor, x, y + 2, locdoor - 1)
                    doorpos = [[x, y, locdoor], [x, y, locdoor - 1]]
                if checkb == mat[8]:
                    setBlock(
                        "oak_door[hinge=right,facing=west]", x, y, locdoor
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=right,facing=west]",
                        x,
                        y + 1,
                        locdoor,
                    )
                    setBlock(
                        "oak_door[hinge=left,facing=west]", x, y, locdoor + 1
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=left,facing=west]",
                        x,
                        y + 1,
                        locdoor + 1,
                    )
                    wood = (x, y + 2, locdoor, x, y + 2, locdoor + 1)
                    doorpos = [[x, y, locdoor], [x, y, locdoor + 1]]
            if door == "east":
                if checka == mat[8]:
                    setBlock(
                        "oak_door[hinge=right,facing=east]", x, y, locdoor
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=right,facing=east]",
                        x,
                        y + 1,
                        locdoor,
                    )
                    setBlock(
                        "oak_door[hinge=left,facing=east]", x, y, locdoor - 1
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=left,facing=east]",
                        x,
                        y + 1,
                        locdoor - 1,
                    )
                    wood = (x, y + 2, locdoor, x, y + 2, locdoor - 1)
                    doorpos = [[x, y, locdoor], [x, y, locdoor - 1]]
                if checkb == mat[8]:
                    setBlock("oak_door[hinge=left,facing=east]", x, y, locdoor)
                    setBlock(
                        "oak_door[half=upper,hinge=left,facing=east]",
                        x,
                        y + 1,
                        locdoor,
                    )
                    setBlock(
                        "oak_door[hinge=right,facing=east]", x, y, locdoor + 1
                    )
                    setBlock(
                        "oak_door[half=upper,hinge=right,facing=east]",
                        x,
                        y + 1,
                        locdoor + 1,
                    )
                    wood = (x, y + 2, locdoor, x, y + 2, locdoor + 1)
                    doorpos = [[x, y, locdoor], [x, y, locdoor + 1]]
            fill(mat[1], wood)

    # -------- roof --------#

    # step 1
    rooftype = random.randint(1, 5)
    rooftype = 4
    if rooftype <= 3:
        if rooftype <= 2:
            if door == "north" or door == "south":
                direction = "z"
            if door == "east" or door == "west":
                direction = "x"
        if rooftype == 3:
            if door == "north" or door == "south":
                direction = "x"
            if door == "east" or door == "west":
                direction = "z"
    elif rooftype >= 4:
        if (door == "north" or door == "south") and xlen <= 9:
            form, direction = "mono-pitched", "x"
        elif (door == "north" or door == "south") and xlen > 9:
            form, direction = "saltbox", "x"
        if (door == "east" or door == "west") and zlen <= 9:
            form, direction = "mono-pitched", "z"
        elif (door == "east" or door == "west") and zlen > 9:
            form, direction = "saltbox", "z"

    # step 2

    # type 1
    if rooftype <= 3:
        if direction == "x":
            z3, z4 = pos1[2] - 1, pos2[2] + 1
            y = pos1[1] + 4
            for x in range(middle1 + 1):
                roofline = [
                    pos1[0] + x - 1,
                    y + x,
                    z3,
                    pos1[0] + x - 1,
                    y + x,
                    z4,
                ]
                roofline2 = [
                    pos2[0] - x + 1,
                    y + x,
                    z3,
                    pos2[0] - x + 1,
                    y + x,
                    z4,
                ]
                roofline3 = [pos1[0] + x, y + x, z3, pos1[0] + x, y + x, z4]
                roofline4 = [pos2[0] - x, y + x, z3, pos2[0] - x, y + x, z4]
                stairs = mat[2] + "[facing=east]"
                fill(stairs, roofline)
                if x != middle1:
                    stairs = mat[2] + "[facing=west,half=top]"
                    fill(stairs, roofline3)
                stairs = mat[2] + "[facing=west]"
                fill(stairs, roofline2)
                if x != middle1:
                    stairs = mat[2] + "[facing=east,half=top]"
                    fill(stairs, roofline4)
                if roofline != roofline2:
                    roofwall = [
                        pos1[0] + x,
                        y + x,
                        pos1[2],
                        pos2[0] - x,
                        y + x,
                        pos1[2],
                    ]
                    fill(mat[1], roofwall)
                    roofwall[2], roofwall[5] = pos2[2], pos2[2]
                    fill(mat[1], roofwall)
                if roofline == roofline2:
                    if varwall == 1:
                        mat[1], mat[3] = mat[3], mat[1]
                    fill(mat[12], roofline)
                    roofline[1], roofline[4] = roofline[1] - 1, roofline[4] - 1
                    fill(mat[1], roofline)
                    if varwall == 1:
                        mat[1], mat[3] = mat[3], mat[1]
            y = pos1[1] + 5
            for x in range(middle1):
                roofline = [
                    pos1[0] + x,
                    y + x,
                    pos1[2],
                    pos1[0] + x,
                    y + x,
                    pos2[2],
                ]
                roofline2 = [
                    pos2[0] - x,
                    y + x,
                    pos1[2],
                    pos2[0] - x,
                    y + x,
                    pos2[2],
                ]
                stairs = mat[9] + "[facing=east]"
                fill(stairs, roofline)
                stairs = mat[9] + "[facing=west]"
                fill(stairs, roofline2)
                if roofline == roofline2:
                    fill(mat[11], roofline)
                    roofline[1], roofline[4] = roofline[1] - 1, roofline[4] - 1
                    fill(mat[10], roofline)

        if direction == "z":
            x3, x4 = pos1[0] - 1, pos2[0] + 1
            y = pos1[1] + 4
            for z in range(middle2 + 1):
                roofline = [
                    x3,
                    y + z,
                    pos1[2] + z - 1,
                    x4,
                    y + z,
                    pos1[2] + z - 1,
                ]
                roofline2 = [
                    x3,
                    y + z,
                    pos2[2] - z + 1,
                    x4,
                    y + z,
                    pos2[2] - z + 1,
                ]
                roofline3 = [x3, y + z, pos1[2] + z, x4, y + z, pos1[2] + z]
                roofline4 = [x3, y + z, pos2[2] - z, x4, y + z, pos2[2] - z]
                stairs = mat[2] + "[facing=south]"
                fill(stairs, roofline)
                if z != middle2:
                    stairs = mat[2] + "[facing=north,half=top]"
                    fill(stairs, roofline3)
                stairs = mat[2] + "[facing=north]"
                fill(stairs, roofline2)
                if z != middle2:
                    stairs = mat[2] + "[facing=south,half=top]"
                    fill(stairs, roofline4)
                if roofline != roofline2:
                    roofwall = [
                        pos1[0],
                        y + z,
                        pos1[2] + z,
                        pos1[0],
                        y + z,
                        pos2[2] - z,
                    ]
                    fill(mat[1], roofwall)
                    roofwall[0], roofwall[3] = pos2[0], pos2[0]
                    fill(mat[1], roofwall)
                if roofline == roofline2:
                    if varwall == 1:
                        mat[1], mat[3] = mat[3], mat[1]
                    fill(mat[12], roofline)
                    roofline[1], roofline[4] = roofline[1] - 1, roofline[4] - 1
                    fill(mat[1], roofline)
                    if varwall == 1:
                        mat[1], mat[3] = mat[3], mat[1]
            y = pos1[1] + 5
            for z in range(middle2):
                roofline = [
                    pos1[0],
                    y + z,
                    pos1[2] + z,
                    pos2[0],
                    y + z,
                    pos1[2] + z,
                ]
                roofline2 = [
                    pos1[0],
                    y + z,
                    pos2[2] - z,
                    pos2[0],
                    y + z,
                    pos2[2] - z,
                ]
                stairs = mat[9] + "[facing=south]"
                fill(stairs, roofline)
                stairs = mat[9] + "[facing=north]"
                fill(stairs, roofline2)
                if roofline == roofline2:
                    fill(mat[11], roofline)
                    roofline[1], roofline[4] = roofline[1] - 1, roofline[4] - 1
                    fill(mat[10], roofline)

    # type 2
    if rooftype >= 4:
        alea = random.randint(1, 2)
        if form == "mono-pitched":
            if direction == "x":
                if alea == 1:
                    z3, z4 = pos1[2] - 1, pos2[2] + 1
                    y = pos1[1] + 4
                    for x in range(xlen + 3):
                        if x != 0 and x != xlen + 2:
                            if x % 2 == 0:
                                roofline = [
                                    pos1[0] + x - 1,
                                    y + x / 2,
                                    z3,
                                    pos1[0] + x - 1,
                                    y + x / 2,
                                    z4,
                                ]
                                roofline2 = [
                                    pos1[0] + x - 1,
                                    y + x / 2 - 1,
                                    z3,
                                    pos1[0] + x - 1,
                                    y + x / 2 - 1,
                                    z4,
                                ]
                                type1, type2 = (
                                    mat[12] + "[type=bottom]",
                                    mat[12] + "[type=top]",
                                )
                                fill(type1, roofline)
                                fill(type2, roofline2)
                                roofwall = [
                                    pos1[0] + x - 1,
                                    y + x / 2 - 1,
                                    z3 + 1,
                                    pos1[0] + x - 1,
                                    y,
                                    z3 + 1,
                                ]
                                fill(mat[1], roofwall)
                                roofwall[2], roofwall[5] = z4 - 1, z4 - 1
                                fill(mat[1], roofwall)
                            else:
                                if varwall == 1:
                                    mat[1], mat[3] = mat[3], mat[1]
                                roofline = [
                                    pos1[0] + x - 1,
                                    y + x / 2,
                                    z3,
                                    pos1[0] + x - 1,
                                    y + x / 2,
                                    z4,
                                ]
                                fill(mat[1], roofline)
                                if varwall == 1:
                                    mat[1], mat[3] = mat[3], mat[1]
                                roofwall = [
                                    pos1[0] + x - 1,
                                    y + x / 2 - 1,
                                    z3 + 1,
                                    pos1[0] + x - 1,
                                    y,
                                    z3 + 1,
                                ]
                                fill(mat[1], roofwall)
                                roofwall[2], roofwall[5] = z4 - 1, z4 - 1
                                fill(mat[1], roofwall)
                        else:
                            if x == 0:
                                roofline, type1 = [
                                    pos1[0] + x - 1,
                                    y + x / 2,
                                    z3,
                                    pos1[0] + x - 1,
                                    y + x / 2,
                                    z4,
                                ], mat[12] + "[type=bottom]"
                                fill(type1, roofline)
                            else:
                                if x % 2 == 0:
                                    roofline, type1 = [
                                        pos1[0] + x - 1,
                                        y + x / 2 - 1,
                                        z3,
                                        pos1[0] + x - 1,
                                        y + x / 2 - 1,
                                        z4,
                                    ], mat[12] + "[type=top]"
                                    fill(type1, roofline)
                                else:
                                    roofline, type1 = [
                                        pos1[0] + x - 1,
                                        y + x / 2,
                                        z3,
                                        pos1[0] + x - 1,
                                        y + x / 2,
                                        z4,
                                    ], mat[12] + "[type=bottom]"
                                    fill(type1, roofline)
                    z1, z2 = pos1[2], pos2[2]
                    if varwall == 1:
                        mat[1], mat[3] = mat[3], mat[1]
                        fill(mat[1], [pos1[0], y, z1, pos1[0], y, z4])
                        mat[1], mat[3] = mat[3], mat[1]
                    wallpos = [
                        pos2[0],
                        y,
                        z1,
                        pos2[0],
                        y + round((xlen + 1) / 2) - 1,
                        z2,
                    ]
                    fill(mat[1], wallpos)
                    if xlen > 7:
                        for z in range(0, middle2 + 1, 4):
                            if middle2 - z >= 4:
                                x = pos2[0]
                                temppos = [
                                    x,
                                    y + 2,
                                    z1 + z + 1,
                                    x,
                                    y + 3,
                                    z1 + z + 2,
                                ]
                                fill(mat[8], temppos)
                                temppos = [
                                    x,
                                    y + 2,
                                    z2 - z - 1,
                                    x,
                                    y + 3,
                                    z2 - z - 2,
                                ]
                                fill(mat[8], temppos)
                            elif middle2 - z >= 1:
                                x = pos2[0]
                                temppos = [
                                    x,
                                    y + 2,
                                    z1 + middle2 - 1,
                                    x,
                                    y + 3,
                                    z1 + middle2 - 1,
                                ]
                                fill(mat[8], temppos)
                                temppos = [
                                    x,
                                    y + 2,
                                    z2 - middle2 + 1,
                                    x,
                                    y + 3,
                                    z2 - middle2 + 1,
                                ]
                                fill(mat[8], temppos)
                elif alea == 2:
                    z3, z4 = pos1[2] - 1, pos2[2] + 1
                    y = pos1[1] + 4
                    for x in range(xlen + 3):
                        if x != 0 and x != xlen + 2:
                            if x % 2 == 0:
                                roofline = [
                                    pos2[0] - x + 1,
                                    y + x / 2,
                                    z3,
                                    pos2[0] - x + 1,
                                    y + x / 2,
                                    z4,
                                ]
                                roofline2 = [
                                    pos2[0] - x + 1,
                                    y + x / 2 - 1,
                                    z3,
                                    pos2[0] - x + 1,
                                    y + x / 2 - 1,
                                    z4,
                                ]
                                type1, type2 = (
                                    mat[12] + "[type=bottom]",
                                    mat[12] + "[type=top]",
                                )
                                fill(type1, roofline)
                                fill(type2, roofline2)
                                roofwall = [
                                    pos2[0] - x + 1,
                                    y + x / 2 - 1,
                                    z3 + 1,
                                    pos2[0] - x + 1,
                                    y,
                                    z3 + 1,
                                ]
                                fill(mat[1], roofwall)
                                roofwall[2], roofwall[5] = z4 - 1, z4 - 1
                                fill(mat[1], roofwall)
                            else:
                                if varwall == 1:
                                    mat[1], mat[3] = mat[3], mat[1]
                                roofline = [
                                    pos2[0] - x + 1,
                                    y + x / 2,
                                    z3,
                                    pos2[0] - x + 1,
                                    y + x / 2,
                                    z4,
                                ]
                                fill(mat[1], roofline)
                                if varwall == 1:
                                    mat[1], mat[3] = mat[3], mat[1]
                                roofwall = [
                                    pos2[0] - x + 1,
                                    y + x / 2 - 1,
                                    z3 + 1,
                                    pos2[0] - x + 1,
                                    y,
                                    z3 + 1,
                                ]
                                fill(mat[1], roofwall)
                                roofwall[2], roofwall[5] = z4 - 1, z4 - 1
                                fill(mat[1], roofwall)
                        else:
                            if x == 0:
                                roofline, type1 = [
                                    pos2[0] - x + 1,
                                    y + x / 2,
                                    z3,
                                    pos2[0] - x + 1,
                                    y + x / 2,
                                    z4,
                                ], mat[12] + "[type=bottom]"
                                fill(type1, roofline)
                            else:
                                if x % 2 == 0:
                                    roofline, type1 = [
                                        pos2[0] - x + 1,
                                        y + x / 2 - 1,
                                        z3,
                                        pos2[0] - x + 1,
                                        y + x / 2 - 1,
                                        z4,
                                    ], mat[12] + "[type=top]"
                                    fill(type1, roofline)
                                else:
                                    roofline, type1 = [
                                        pos2[0] - x + 1,
                                        y + x / 2,
                                        z3,
                                        pos2[0] - x + 1,
                                        y + x / 2,
                                        z4,
                                    ], mat[12] + "[type=bottom]"
                                    fill(type1, roofline)
                    z1, z2 = pos1[2], pos2[2]
                    if varwall == 1:
                        mat[1], mat[3] = mat[3], mat[1]
                        fill(mat[1], [pos2[0], y, z1, pos2[0], y, z4])
                        mat[1], mat[3] = mat[3], mat[1]
                    wallpos = [
                        pos1[0],
                        y,
                        z1,
                        pos1[0],
                        y + round((xlen + 1) / 2) - 1,
                        z2,
                    ]
                    fill(mat[1], wallpos)
                    if xlen > 7:
                        for z in range(0, middle2 + 1, 4):
                            if middle2 - z >= 4:
                                x = pos1[0]
                                temppos = [
                                    x,
                                    y + 2,
                                    z1 + z + 1,
                                    x,
                                    y + 3,
                                    z1 + z + 2,
                                ]
                                fill(mat[8], temppos)
                                temppos = [
                                    x,
                                    y + 2,
                                    z2 - z - 1,
                                    x,
                                    y + 3,
                                    z2 - z - 2,
                                ]
                                fill(mat[8], temppos)
                            elif middle2 - z >= 1:
                                x = pos1[0]
                                temppos = [
                                    x,
                                    y + 2,
                                    z1 + middle2 - 1,
                                    x,
                                    y + 3,
                                    z1 + middle2 - 1,
                                ]
                                fill(mat[8], temppos)
                                temppos = [
                                    x,
                                    y + 2,
                                    z2 - middle2 + 1,
                                    x,
                                    y + 3,
                                    z2 - middle2 + 1,
                                ]
                                fill(mat[8], temppos)

            if direction == "z":
                if alea == 1:
                    x3, x4 = pos1[0] - 1, pos2[0] + 1
                    y = pos1[1] + 4
                    for z in range(zlen + 3):
                        if z != 0 and z != zlen + 2:
                            if z % 2 == 0:
                                roofline = [
                                    x3,
                                    y + z / 2,
                                    pos1[2] + z - 1,
                                    x4,
                                    y + z / 2,
                                    pos1[2] + z - 1,
                                ]
                                roofline2 = [
                                    x3,
                                    y + z / 2 - 1,
                                    pos1[2] + z - 1,
                                    x4,
                                    y + z / 2 - 1,
                                    pos1[2] + z - 1,
                                ]
                                type1, type2 = (
                                    mat[12] + "[type=bottom]",
                                    mat[12] + "[type=top]",
                                )
                                fill(type1, roofline)
                                fill(type2, roofline2)
                                roofwall = [
                                    x3 + 1,
                                    y + z / 2 - 1,
                                    pos1[2] + z - 1,
                                    x3 + 1,
                                    y,
                                    pos1[2] + z - 1,
                                ]
                                fill(mat[1], roofwall)
                                roofwall[0], roofwall[3] = x4 - 1, x4 - 1
                                fill(mat[1], roofwall)
                            else:
                                if varwall == 1:
                                    mat[1], mat[3] = mat[3], mat[1]
                                roofline = [
                                    x3,
                                    y + z / 2,
                                    pos1[2] + z - 1,
                                    x4,
                                    y + z / 2,
                                    pos1[2] + z - 1,
                                ]
                                fill(mat[1], roofline)
                                if varwall == 1:
                                    mat[1], mat[3] = mat[3], mat[1]
                                roofwall = [
                                    x3 + 1,
                                    y + z / 2 - 1,
                                    pos1[2] + z - 1,
                                    x3 + 1,
                                    y,
                                    pos1[2] + z - 1,
                                ]
                                fill(mat[1], roofwall)
                                roofwall[0], roofwall[3] = x4 - 1, x4 - 1
                                fill(mat[1], roofwall)
                        else:
                            if z == 0:
                                roofline, type1 = [
                                    x3,
                                    y + z / 2,
                                    pos1[2] + z - 1,
                                    x4,
                                    y + z / 2,
                                    pos1[2] + z - 1,
                                ], mat[12] + "[type=bottom]"
                                fill(type1, roofline)
                            else:
                                if z % 2 == 0:
                                    roofline, type1 = [
                                        x3,
                                        y + z / 2 - 1,
                                        pos1[2] + z - 1,
                                        x4,
                                        y + z / 2 - 1,
                                        pos1[2] + z - 1,
                                    ], mat[12] + "[type=top]"
                                    fill(type1, roofline)
                                else:
                                    roofline, type1 = [
                                        x3,
                                        y + z / 2,
                                        pos1[2] + z - 1,
                                        x4,
                                        y + z / 2,
                                        pos1[2] + z - 1,
                                    ], mat[12] + "[type=bottom]"
                                    fill(type1, roofline)
                    x1, x2 = pos1[0], pos2[0]
                    if varwall == 1:
                        mat[1], mat[3] = mat[3], mat[1]
                        fill(mat[1], [x3, y, pos1[2], x4, y, pos1[2]])
                        mat[1], mat[3] = mat[3], mat[1]
                    wallpos = [
                        x1,
                        y,
                        pos2[2],
                        x2,
                        y + round((zlen + 1) / 2) - 1,
                        pos2[2],
                    ]
                    fill(mat[1], wallpos)
                    if zlen > 7:
                        for x in range(0, middle1 + 1, 4):
                            if middle1 - x >= 4:
                                z = pos2[2]
                                temppos = [
                                    x1 + x + 1,
                                    y + 2,
                                    z,
                                    x1 + x + 2,
                                    y + 3,
                                    z,
                                ]
                                fill(mat[8], temppos)
                                temppos = [
                                    x2 - x - 1,
                                    y + 2,
                                    z,
                                    x2 - x - 2,
                                    y + 3,
                                    z,
                                ]
                                fill(mat[8], temppos)
                            elif middle1 - x >= 1:
                                z = pos2[2]
                                temppos = [
                                    x1 + middle1 - 1,
                                    y + 2,
                                    z,
                                    x1 + middle1 - 1,
                                    y + 3,
                                    z,
                                ]
                                fill(mat[8], temppos)
                                temppos = [
                                    x2 - middle1 + 1,
                                    y + 2,
                                    z,
                                    x2 - middle1 + 1,
                                    y + 3,
                                    z,
                                ]
                                fill(mat[8], temppos)
                elif alea == 2:
                    x3, x4 = pos1[0] - 1, pos2[0] + 1
                    y = pos1[1] + 4
                    for z in range(zlen + 3):
                        if z != 0 and z != zlen + 2:
                            if z % 2 == 0:
                                roofline = [
                                    x3,
                                    y + z / 2,
                                    pos2[2] - z + 1,
                                    x4,
                                    y + z / 2,
                                    pos2[2] - z + 1,
                                ]
                                roofline2 = [
                                    x3,
                                    y + z / 2 - 1,
                                    pos2[2] - z + 1,
                                    x4,
                                    y + z / 2 - 1,
                                    pos2[2] - z + 1,
                                ]
                                type1, type2 = (
                                    mat[12] + "[type=bottom]",
                                    mat[12] + "[type=top]",
                                )
                                fill(type1, roofline)
                                fill(type2, roofline2)
                                roofwall = [
                                    x3 + 1,
                                    y + z / 2 - 1,
                                    pos2[2] - z + 1,
                                    x3 + 1,
                                    y,
                                    pos2[2] - z + 1,
                                ]
                                fill(mat[1], roofwall)
                                roofwall[0], roofwall[3] = x4 - 1, x4 - 1
                                fill(mat[1], roofwall)
                            else:
                                if varwall == 1:
                                    mat[1], mat[3] = mat[3], mat[1]
                                roofline = [
                                    x3,
                                    y + z / 2,
                                    pos2[2] - z + 1,
                                    x4,
                                    y + z / 2,
                                    pos2[2] - z + 1,
                                ]
                                fill(mat[1], roofline)
                                if varwall == 1:
                                    mat[1], mat[3] = mat[3], mat[1]
                                roofwall = [
                                    x3 + 1,
                                    y + z / 2 - 1,
                                    pos2[2] - z + 1,
                                    x3 + 1,
                                    y,
                                    pos2[2] - z + 1,
                                ]
                                fill(mat[1], roofwall)
                                roofwall[0], roofwall[3] = x4 - 1, x4 - 1
                                fill(mat[1], roofwall)
                        else:
                            if z == 0:
                                roofline, type1 = [
                                    x3,
                                    y + z / 2,
                                    pos2[2] - z + 1,
                                    x4,
                                    y + z / 2,
                                    pos2[2] - z + 1,
                                ], mat[12] + "[type=bottom]"
                                fill(type1, roofline)
                            else:
                                if z % 2 == 0:
                                    roofline, type1 = [
                                        x3,
                                        y + z / 2 - 1,
                                        pos2[2] - z + 1,
                                        x4,
                                        y + z / 2 - 1,
                                        pos2[2] - z + 1,
                                    ], mat[12] + "[type=top]"
                                    fill(type1, roofline)
                                else:
                                    roofline, type1 = [
                                        x3,
                                        y + z / 2,
                                        pos2[2] - z + 1,
                                        x4,
                                        y + z / 2,
                                        pos2[2] - z + 1,
                                    ], mat[12] + "[type=bottom]"
                                    fill(type1, roofline)
                    x1, x2 = pos1[0], pos2[0]
                    if varwall == 1:
                        mat[1], mat[3] = mat[3], mat[1]
                        fill(mat[1], [x3, y, pos2[2], x4, y, pos2[2]])
                        mat[1], mat[3] = mat[3], mat[1]
                    wallpos = [
                        x1,
                        y,
                        pos1[2],
                        x2,
                        y + round((zlen + 1) / 2) - 1,
                        pos1[2],
                    ]
                    fill(mat[1], wallpos)
                    if zlen > 7:
                        for x in range(0, middle1 + 1, 4):
                            if middle1 - x >= 4:
                                z = pos1[2]
                                temppos = [
                                    x1 + x + 1,
                                    y + 2,
                                    z,
                                    x1 + x + 2,
                                    y + 3,
                                    z,
                                ]
                                fill(mat[8], temppos)
                                temppos = [
                                    x2 - x - 1,
                                    y + 2,
                                    z,
                                    x2 - x - 2,
                                    y + 3,
                                    z,
                                ]
                                fill(mat[8], temppos)
                            elif middle1 - x >= 1:
                                z = pos1[2]
                                temppos = [
                                    x1 + middle1 - 1,
                                    y + 2,
                                    z,
                                    x1 + middle1 - 1,
                                    y + 3,
                                    z,
                                ]
                                fill(mat[8], temppos)
                                temppos = [
                                    x2 - middle1 + 1,
                                    y + 2,
                                    z,
                                    x2 - middle1 + 1,
                                    y + 3,
                                    z,
                                ]
                                fill(mat[8], temppos)

        # type 3
        elif form == "saltbox":
            if direction == "x":
                line1, line2 = pos1[0], pos2[0]
                z3, z4, y = pos1[2] - 1, pos2[2] + 1, pos1[1] + 5
                while line1 < line2:
                    if alea == 1:
                        roofline = [line1, y, z3, line1, y, z4]
                        roofline2 = [line1, y - 1, z3, line1, y - 1, z4]
                        roofline3 = [line1, y, z3 + 1, line1, y, z4 - 1]
                        stairs, stairs2 = (
                            mat[2] + "[facing=east]",
                            mat[9] + "[facing=east]",
                        )
                        fill(stairs, roofline)
                        fill(stairs2, roofline3)
                        if line1 != line2:
                            stairs = mat[2] + "[facing=west,half=top]"
                            fill(stairs, roofline2)
                        roofwall = [
                            line1,
                            y - 1,
                            z3 + 1,
                            line1,
                            pos1[1] + 4,
                            z3 + 1,
                        ]
                        fill(mat[1], roofwall)
                        roofwall[2], roofwall[5] = z4 - 1, z4 - 1
                        fill(mat[1], roofwall)
                        if line1 < line2:
                            roofline = [line2, y, z3, line2, y, z4]
                            roofline2 = [line2, y - 1, z3, line2, y - 1, z4]
                            roofline3 = [line2, y, z3 + 1, line2, y, z4 - 1]
                            type1, type2, type3 = (
                                mat[12] + "[type=bottom]",
                                mat[12] + "[type=top]",
                                mat[11] + "[type=bottom]",
                            )
                            fill(type1, roofline)
                            fill(type2, roofline2)
                            fill(type3, roofline3)
                            roofwall = [
                                line2,
                                y - 1,
                                z3 + 1,
                                line2,
                                pos1[1] + 4,
                                z3 + 1,
                            ]
                            fill(mat[1], roofwall)
                            roofwall[2], roofwall[5] = z4 - 1, z4 - 1
                            fill(mat[1], roofwall)
                        if line1 < line2 - 1:
                            roofline = [line2 - 1, y, z3, line2 - 1, y, z4]
                            roofline2 = [
                                line2 - 1,
                                y,
                                z3 + 1,
                                line2 - 1,
                                y,
                                z4 - 1,
                            ]
                            if varwall == 1:
                                mat[1], mat[3] = mat[3], mat[1]
                            fill(mat[1], roofline)
                            fill(mat[10], roofline2)
                            if varwall == 1:
                                mat[1], mat[3] = mat[3], mat[1]
                            roofwall = [
                                line2 - 1,
                                y - 1,
                                z3 + 1,
                                line2 - 1,
                                pos1[1] + 4,
                                z3 + 1,
                            ]
                            fill(mat[1], roofwall)
                            roofwall[2], roofwall[5] = z4 - 1, z4 - 1
                            fill(mat[1], roofwall)
                        line1, line2, y = line1 + 1, line2 - 2, y + 1
                    elif alea == 2:
                        roofline = [line2, y, z3, line2, y, z4]
                        roofline2 = [line2, y - 1, z3, line2, y - 1, z4]
                        roofline3 = [line2, y, z3 + 1, line2, y, z4 - 1]
                        stairs, stairs2 = (
                            mat[2] + "[facing=west]",
                            mat[9] + "[facing=west]",
                        )
                        fill(stairs, roofline)
                        fill(stairs2, roofline3)
                        if line1 != line2:
                            stairs = mat[2] + "[facing=east,half=top]"
                            fill(stairs, roofline2)
                        roofwall = [
                            line2,
                            y - 1,
                            z3 + 1,
                            line2,
                            pos1[1] + 4,
                            z3 + 1,
                        ]
                        fill(mat[1], roofwall)
                        roofwall[2], roofwall[5] = z4 - 1, z4 - 1
                        fill(mat[1], roofwall)
                        if line1 < line2:
                            roofline = [line1, y, z3, line1, y, z4]
                            roofline2 = [line1, y - 1, z3, line1, y - 1, z4]
                            roofline3 = [line1, y, z3 + 1, line1, y, z4 - 1]
                            type1, type2, type3 = (
                                mat[12] + "[type=bottom]",
                                mat[12] + "[type=top]",
                                mat[11] + "[type=bottom]",
                            )
                            fill(type1, roofline)
                            fill(type2, roofline2)
                            fill(type3, roofline3)
                            roofwall = [
                                line1,
                                y - 1,
                                z3 + 1,
                                line1,
                                pos1[1] + 4,
                                z3 + 1,
                            ]
                            fill(mat[1], roofwall)
                            roofwall[2], roofwall[5] = z4 - 1, z4 - 1
                            fill(mat[1], roofwall)
                        if line1 < line2 - 1:
                            roofline = [line1 + 1, y, z3, line1 + 1, y, z4]
                            roofline2 = [
                                line1 + 1,
                                y,
                                z3 + 1,
                                line1 + 1,
                                y,
                                z4 - 1,
                            ]
                            if varwall == 1:
                                mat[1], mat[3] = mat[3], mat[1]
                            fill(mat[1], roofline)
                            fill(mat[10], roofline2)
                            if varwall == 1:
                                mat[1], mat[3] = mat[3], mat[1]
                            roofwall = [
                                line1 + 1,
                                y - 1,
                                z3 + 1,
                                line1 + 1,
                                pos1[1] + 4,
                                z3 + 1,
                            ]
                            fill(mat[1], roofwall)
                            roofwall[2], roofwall[5] = z4 - 1, z4 - 1
                            fill(mat[1], roofwall)
                        line1, line2, y = line1 + 2, line2 - 1, y + 1
                if alea == 1:
                    roofline = [
                        pos1[0] - 1,
                        pos1[1] + 4,
                        z3,
                        pos1[0] - 1,
                        pos1[1] + 4,
                        z4,
                    ]
                    fill(mat[2] + "[facing=east]", roofline)
                    roofline = [
                        pos2[0] + 1,
                        pos1[1] + 4,
                        z3,
                        pos2[0] + 1,
                        pos1[1] + 4,
                        z4,
                    ]
                    fill(mat[12] + "[type=top]", roofline)
                    roofline = [
                        pos2[0],
                        pos1[1] + 4,
                        z3 + 1,
                        pos2[0],
                        pos1[1] + 4,
                        z4 - 1,
                    ]
                    fill(mat[1], roofline)
                elif alea == 2:
                    roofline = [
                        pos2[0] + 1,
                        pos1[1] + 4,
                        z3,
                        pos2[0] + 1,
                        pos1[1] + 4,
                        z4,
                    ]
                    fill(mat[2] + "[facing=west]", roofline)
                    roofline = [
                        pos1[0] - 1,
                        pos1[1] + 4,
                        z3,
                        pos1[0] - 1,
                        pos1[1] + 4,
                        z4,
                    ]
                    fill(mat[12] + "[type=top]", roofline)
                    roofline = [
                        pos1[0],
                        pos1[1] + 4,
                        z3 + 1,
                        pos1[0],
                        pos1[1] + 4,
                        z4 - 1,
                    ]
                    fill(mat[1], roofline)
                if line1 - 2 == line2 or line2 + 2 == line1:
                    if alea == 1:
                        roofline = [line2 + 1, y - 1, z3, line2 + 1, y - 1, z4]
                        roofline2 = [
                            line2 + 1,
                            y - 1,
                            z3 + 1,
                            line2 + 1,
                            y - 1,
                            z4 - 1,
                        ]
                        fill(mat[12] + "[type=bottom]", roofline)
                        fill(mat[11] + "[type=bottom]", roofline2)
                    elif alea == 2:
                        roofline = [line1 - 1, y - 1, z3, line1 - 1, y - 1, z4]
                        roofline2 = [
                            line1 - 1,
                            y - 1,
                            z3 + 1,
                            line1 - 1,
                            y - 1,
                            z4 - 1,
                        ]
                        fill(mat[12] + "[type=bottom]", roofline)
                        fill(mat[11] + "[type=bottom]", roofline2)
                if line1 == line2:
                    roofline = [line1, y - 1, z3, line1, y - 1, z4]
                    roofline2 = [line1, y, z3, line1, y, z4]
                    roofline3 = [line1, y, z3 + 1, line1, y, z4 - 1]
                    if varwall == 1:
                        mat[1], mat[3] = mat[3], mat[1]
                    fill(mat[1], roofline)
                    if varwall == 1:
                        mat[1], mat[3] = mat[3], mat[1]
                    fill(mat[12] + "[type=bottom]", roofline2)
                    fill(mat[11] + "[type=bottom]", roofline3)
                    roofwall = [
                        line1,
                        y - 1,
                        z3 + 1,
                        line1,
                        pos1[1] + 4,
                        z3 + 1,
                    ]
                    fill(mat[1], roofwall)
                    roofwall[2], roofwall[5] = z4 - 1, z4 - 1
                    fill(mat[1], roofwall)

            elif direction == "z":
                line1, line2 = pos1[2], pos2[2]
                x3, x4, y = pos1[0] - 1, pos2[0] + 1, pos1[1] + 5
                while line1 < line2:
                    if alea == 1:
                        roofline = [x3, y, line1, x4, y, line1]
                        roofline2 = [x3, y - 1, line1, x4, y - 1, line1]
                        roofline3 = [x3 + 1, y, line1, x4 - 1, y, line1]
                        stairs, stairs2 = (
                            mat[2] + "[facing=south]",
                            mat[9] + "[facing=south]",
                        )
                        fill(stairs, roofline)
                        fill(stairs2, roofline3)
                        if line1 != line2:
                            stairs = mat[2] + "[facing=north,half=top]"
                            fill(stairs, roofline2)
                        roofwall = [
                            x3 + 1,
                            y - 1,
                            line1,
                            x3 + 1,
                            pos1[1] + 4,
                            line1,
                        ]
                        fill(mat[1], roofwall)
                        roofwall[0], roofwall[3] = x4 - 1, x4 - 1
                        fill(mat[1], roofwall)
                        if line1 < line2:
                            roofline = [x3, y, line2, x4, y, line2]
                            roofline2 = [x3, y - 1, line2, x4, y - 1, line2]
                            roofline3 = [x3 + 1, y, line2, x4 - 1, y, line2]
                            type1, type2, type3 = (
                                mat[12] + "[type=bottom]",
                                mat[12] + "[type=top]",
                                mat[11] + "[type=bottom]",
                            )
                            fill(type1, roofline)
                            fill(type2, roofline2)
                            fill(type3, roofline3)
                            roofwall = [
                                x3 + 1,
                                y - 1,
                                line2,
                                x3 + 1,
                                pos1[1] + 4,
                                line2,
                            ]
                            fill(mat[1], roofwall)
                            roofwall[0], roofwall[3] = x4 - 1, x4 - 1
                            fill(mat[1], roofwall)
                        if line1 < line2 - 1:
                            roofline = [x3, y, line2 - 1, x4, y, line2 - 1]
                            roofline2 = [
                                x3 + 1,
                                y,
                                line2 - 1,
                                x4 - 1,
                                y,
                                line2 - 1,
                            ]
                            if varwall == 1:
                                mat[1], mat[3] = mat[3], mat[1]
                            fill(mat[1], roofline)
                            fill(mat[10], roofline2)
                            if varwall == 1:
                                mat[1], mat[3] = mat[3], mat[1]
                            roofwall = [
                                x3 + 1,
                                y - 1,
                                line2 - 1,
                                x3 + 1,
                                pos1[1] + 4,
                                line2 - 1,
                            ]
                            fill(mat[1], roofwall)
                            roofwall[0], roofwall[3] = x4 - 1, x4 - 1
                            fill(mat[1], roofwall)
                        line1, line2, y = line1 + 1, line2 - 2, y + 1
                    elif alea == 2:
                        roofline = [x3, y, line2, x4, y, line2]
                        roofline2 = [x3, y - 1, line2, x4, y - 1, line2]
                        roofline3 = [x3 + 1, y, line2, x4 - 1, y, line2]
                        stairs, stairs2 = (
                            mat[2] + "[facing=north]",
                            mat[9] + "[facing=north]",
                        )
                        fill(stairs, roofline)
                        fill(stairs2, roofline3)
                        if line1 != line2:
                            stairs = mat[2] + "[facing=south,half=top]"
                            fill(stairs, roofline2)
                        roofwall = [
                            x3 + 1,
                            y - 1,
                            line2,
                            x3 + 1,
                            pos1[1] + 4,
                            line2,
                        ]
                        fill(mat[1], roofwall)
                        roofwall[0], roofwall[3] = x4 - 1, x4 - 1
                        fill(mat[1], roofwall)
                        if line1 < line2:
                            roofline = [x3, y, line1, x4, y, line1]
                            roofline2 = [x3, y - 1, line1, x4, y - 1, line1]
                            roofline3 = [x3 + 1, y, line1, x4 - 1, y, line1]
                            type1, type2, type3 = (
                                mat[12] + "[type=bottom]",
                                mat[12] + "[type=top]",
                                mat[11] + "[type=bottom]",
                            )
                            fill(type1, roofline)
                            fill(type2, roofline2)
                            fill(type3, roofline3)
                            roofwall = [
                                x3 + 1,
                                y - 1,
                                line1,
                                x3 + 1,
                                pos1[1] + 4,
                                line1,
                            ]
                            fill(mat[1], roofwall)
                            roofwall[0], roofwall[3] = x4 - 1, x4 - 1
                            fill(mat[1], roofwall)
                        if line1 < line2 - 1:
                            roofline = [x3, y, line1 + 1, x4, y, line1 + 1]
                            roofline2 = [
                                x3 + 1,
                                y,
                                line1 + 1,
                                x4 - 1,
                                y,
                                line1 + 1,
                            ]
                            if varwall == 1:
                                mat[1], mat[3] = mat[3], mat[1]
                            fill(mat[1], roofline)
                            fill(mat[10], roofline2)
                            if varwall == 1:
                                mat[1], mat[3] = mat[3], mat[1]
                            roofwall = [
                                x3 + 1,
                                y - 1,
                                line1 + 1,
                                x3 + 1,
                                pos1[1] + 4,
                                line1 + 1,
                            ]
                            fill(mat[1], roofwall)
                            roofwall[0], roofwall[3] = x4 - 1, x4 - 1
                            fill(mat[1], roofwall)
                        line1, line2, y = line1 + 2, line2 - 1, y + 1
                if alea == 1:
                    roofline = [
                        x3,
                        pos1[1] + 4,
                        pos1[2] - 1,
                        x4,
                        pos1[1] + 4,
                        pos1[2] - 1,
                    ]
                    fill(mat[2] + "[facing=south]", roofline)
                    roofline = [
                        x3,
                        pos1[1] + 4,
                        pos2[2] + 1,
                        x4,
                        pos1[1] + 4,
                        pos2[2] + 1,
                    ]
                    fill(mat[12] + "[type=top]", roofline)
                    roofline = [
                        x3 + 1,
                        pos1[1] + 4,
                        pos2[2],
                        x4 - 1,
                        pos1[1] + 4,
                        pos2[2],
                    ]
                    fill(mat[1], roofline)
                elif alea == 2:
                    roofline = [
                        x3,
                        pos1[1] + 4,
                        pos2[2] + 1,
                        x4,
                        pos1[1] + 4,
                        pos2[2] + 1,
                    ]
                    fill(mat[2] + "[facing=north]", roofline)
                    roofline = [
                        x3,
                        pos1[1] + 4,
                        pos1[2] - 1,
                        x4,
                        pos1[1] + 4,
                        pos1[2] - 1,
                    ]
                    fill(mat[12] + "[type=top]", roofline)
                    roofline = [
                        x3 + 1,
                        pos1[1] + 4,
                        pos1[2],
                        x4 - 1,
                        pos1[1] + 4,
                        pos1[2],
                    ]
                    fill(mat[1], roofline)
                if line1 - 2 == line2 or line2 + 2 == line1:
                    if alea == 1:
                        roofline = [x3, y - 1, line2 + 1, x4, y - 1, line2 + 1]
                        roofline2 = [
                            x3 + 1,
                            y - 1,
                            line2 + 1,
                            x4 - 1,
                            y - 1,
                            line2 + 1,
                        ]
                        fill(mat[12] + "[type=bottom]", roofline)
                        fill(mat[11] + "[type=bottom]", roofline2)
                    elif alea == 2:
                        roofline = [x3, y - 1, line1 + 1, x4, y - 1, line1 + 1]
                        roofline2 = [
                            x3 + 1,
                            y - 1,
                            line1 + 1,
                            x4 - 1,
                            y - 1,
                            line1 + 1,
                        ]
                        fill(mat[12] + "[type=bottom]", roofline)
                        fill(mat[11] + "[type=bottom]", roofline2)
                if line1 == line2:
                    roofline = [x3, y - 1, line1, x4, y - 1, line1]
                    roofline2 = [x3, y, line1, x4, y, line1]
                    roofline3 = [x3 + 1, y, line1, x4 - 1, y, line1]
                    if varwall == 1:
                        mat[1], mat[3] = mat[3], mat[1]
                    fill(mat[1], roofline)
                    if varwall == 1:
                        mat[1], mat[3] = mat[3], mat[1]
                    fill(mat[12] + "[type=bottom]", roofline2)
                    fill(mat[11] + "[type=bottom]", roofline3)
                    roofwall = [
                        x3 + 1,
                        y - 1,
                        line1,
                        x3 + 1,
                        pos1[1] + 4,
                        line1,
                    ]
                    fill(mat[1], roofwall)
                    roofwall[0], roofwall[3] = x4 - 1, x4 - 1
                    fill(mat[1], roofwall)

    # -------- fireplace --------#

    isfireplace = 0
    if (pos2[0] - pos1[0]) > 7 and (pos2[2] - pos1[2]) > 7:
        isfireplace = random.randint(1, 5)
    if isfireplace > 2 and form != "mono-pitched":
        if door == "north":
            var = random.randint(1, 2)
            if var == 1:
                xp = pos1[0] + 2
            else:
                xp = pos2[0] - 2
            FPpos = [xp, pos1[1] + 1, pos2[2] - 2]
        elif door == "south":
            var = random.randint(1, 2)
            if var == 1:
                xp = pos1[0] + 2
            else:
                xp = pos2[0] - 2
            FPpos = [xp, pos1[1] + 1, pos1[2] + 2]
        elif door == "east":
            var = random.randint(1, 2)
            if var == 1:
                zp = pos1[2] + 2
            else:
                zp = pos2[2] - 2
            FPpos = [pos1[0] + 2, pos1[1] + 1, zp]
        else:
            var = random.randint(1, 2)
            if var == 1:
                zp = pos1[2] + 2
            else:
                zp = pos2[2] - 2
            FPpos = [pos2[0] - 2, pos1[1] + 1, zp]

        fill(
            "minecraft:iron_bars",
            [
                FPpos[0] - 1,
                FPpos[1],
                FPpos[2] - 1,
                FPpos[0] + 1,
                FPpos[1],
                FPpos[2] + 1,
            ],
        )
        setBlock("minecraft:campfire", FPpos[0], FPpos[1], FPpos[2])
        fill(
            "minecraft:cobblestone",
            [
                FPpos[0] - 1,
                FPpos[1] - 1,
                FPpos[2] - 1,
                FPpos[0] + 1,
                FPpos[1] - 1,
                FPpos[2] + 1,
            ],
        )
        setBlock("minecraft:hay_block", FPpos[0], FPpos[1] - 1, FPpos[2])
        fill(
            "minecraft:cobblestone_stairs[half=top,facing=east]",
            [
                FPpos[0] - 1,
                FPpos[1] + 2,
                FPpos[2] - 1,
                FPpos[0] - 1,
                FPpos[1] + 2,
                FPpos[2] + 1,
            ],
        )
        fill(
            "minecraft:cobblestone_stairs[half=top,facing=west]",
            [
                FPpos[0] + 1,
                FPpos[1] + 2,
                FPpos[2] - 1,
                FPpos[0] + 1,
                FPpos[1] + 2,
                FPpos[2] + 1,
            ],
        )
        setBlock(
            "minecraft:cobblestone_stairs[half=top,facing=north]",
            FPpos[0],
            FPpos[1] + 2,
            FPpos[2] + 1,
        )
        setBlock(
            "minecraft:cobblestone_stairs[half=top,facing=south]",
            FPpos[0],
            FPpos[1] + 2,
            FPpos[2] - 1,
        )
        for x in range(-2, 3, 4):
            if getBlock(FPpos[0] + x, FPpos[1] + 1, FPpos[2]) != "air":
                fill(
                    "minecraft:cobblestone",
                    [
                        FPpos[0] + x / 2,
                        FPpos[1],
                        FPpos[2],
                        FPpos[0] + x / 2,
                        FPpos[1] + 3,
                        FPpos[2],
                    ],
                )
                fill(
                    mat[1],
                    [
                        FPpos[0] + x,
                        FPpos[1] + 1,
                        FPpos[2] + 1,
                        FPpos[0] + x,
                        FPpos[1] + 2,
                        FPpos[2] - 1,
                    ],
                )
        for z in range(-2, 3, 4):
            if getBlock(FPpos[0], FPpos[1] + 1, FPpos[2] + z) != "air":
                fill(
                    "minecraft:cobblestone",
                    [
                        FPpos[0],
                        FPpos[1],
                        FPpos[2] + z / 2,
                        FPpos[0],
                        FPpos[1] + 3,
                        FPpos[2] + z / 2,
                    ],
                )
                fill(
                    mat[1],
                    [
                        FPpos[0] + 1,
                        FPpos[1] + 1,
                        FPpos[2] + z,
                        FPpos[0] - 1,
                        FPpos[1] + 2,
                        FPpos[2] + z,
                    ],
                )
        y = FPpos[1] + 3
        while (
            getBlock(FPpos[0], y, FPpos[2]) == "air"
            or getBlock(FPpos[0], y, FPpos[2]) == mat[1]
        ):
            fill(
                "minecraft:cobblestone",
                [FPpos[0] - 1, y, FPpos[2], FPpos[0] - 1, y + 1, FPpos[2]],
            )
            fill(
                "minecraft:cobblestone",
                [FPpos[0] + 1, y, FPpos[2], FPpos[0] + 1, y + 1, FPpos[2]],
            )
            fill(
                "minecraft:cobblestone",
                [FPpos[0], y, FPpos[2] - 1, FPpos[0], y + 1, FPpos[2] - 1],
            )
            fill(
                "minecraft:cobblestone",
                [FPpos[0], y, FPpos[2] + 1, FPpos[0], y + 1, FPpos[2] + 1],
            )
            y += 1
        fill(
            "minecraft:air",
            [
                FPpos[0],
                FPpos[1] + 1,
                FPpos[2],
                FPpos[0],
                FPpos[1] + 15,
                FPpos[2],
            ],
        )
        xy = []
        for x in range(-1, 2, 2):
            ybis = y
            while getBlock(FPpos[0] + x, ybis, FPpos[2]) != "air":
                setBlock("minecraft:cobblestone", FPpos[0] + x, ybis, FPpos[2])
                ybis += 1
            fill(
                "minecraft:cobblestone",
                [
                    FPpos[0] + x,
                    ybis,
                    FPpos[2],
                    FPpos[0] + x,
                    ybis + 1,
                    FPpos[2],
                ],
            )
            xy.append(ybis + 2)
        if xy[0] - 2 == xy[1]:
            setBlock(
                "minecraft:cobblestone_stairs[facing=west]",
                FPpos[0] - 1,
                xy[0],
                FPpos[2],
            )
            setBlock(
                "minecraft:cobblestone_stairs[facing=west]",
                FPpos[0] + 1,
                xy[1],
                FPpos[2],
            )
            setBlock(
                "minecraft:cobblestone_stairs[facing=west]",
                FPpos[0],
                xy[1] + 1,
                FPpos[2] - 1,
            )
            setBlock(
                "minecraft:cobblestone_stairs[facing=west]",
                FPpos[0],
                xy[1] + 1,
                FPpos[2] + 1,
            )
        elif xy[0] + 2 == xy[1]:
            setBlock(
                "minecraft:cobblestone_stairs[facing=east]",
                FPpos[0] - 1,
                xy[0],
                FPpos[2],
            )
            setBlock(
                "minecraft:cobblestone_stairs[facing=east]",
                FPpos[0] + 1,
                xy[1],
                FPpos[2],
            )
            setBlock(
                "minecraft:cobblestone_stairs[facing=east]",
                FPpos[0],
                xy[0] + 1,
                FPpos[2] - 1,
            )
            setBlock(
                "minecraft:cobblestone_stairs[facing=east]",
                FPpos[0],
                xy[0] + 1,
                FPpos[2] + 1,
            )
        zy = []
        for z in range(-1, 2, 2):
            ybis = y
            while getBlock(FPpos[0], ybis, FPpos[2] + z) != "air":
                setBlock("minecraft:cobblestone", FPpos[0], ybis, FPpos[2] + z)
                ybis += 1
            fill(
                "minecraft:cobblestone",
                [
                    FPpos[0],
                    ybis,
                    FPpos[2] + z,
                    FPpos[0],
                    ybis + 1,
                    FPpos[2] + z,
                ],
            )
            zy.append(ybis + 2)
        if zy[0] - 2 == zy[1]:
            setBlock(
                "minecraft:cobblestone_stairs[facing=north]",
                FPpos[0],
                zy[0],
                FPpos[2] - 1,
            )
            setBlock(
                "minecraft:cobblestone_stairs[facing=north]",
                FPpos[0],
                zy[1],
                FPpos[2] + 1,
            )
            setBlock(
                "minecraft:cobblestone_stairs[facing=north]",
                FPpos[0] - 1,
                zy[1] + 1,
                FPpos[2],
            )
            setBlock(
                "minecraft:cobblestone_stairs[facing=north]",
                FPpos[0] + 1,
                zy[1] + 1,
                FPpos[2],
            )
        elif zy[0] + 2 == zy[1]:
            setBlock(
                "minecraft:cobblestone_stairs[facing=south]",
                FPpos[0],
                zy[0],
                FPpos[2] - 1,
            )
            setBlock(
                "minecraft:cobblestone_stairs[facing=south]",
                FPpos[0],
                zy[1],
                FPpos[2] + 1,
            )
            setBlock(
                "minecraft:cobblestone_stairs[facing=south]",
                FPpos[0] - 1,
                zy[0] + 1,
                FPpos[2],
            )
            setBlock(
                "minecraft:cobblestone_stairs[facing=south]",
                FPpos[0] + 1,
                zy[0] + 1,
                FPpos[2],
            )
        if zy[0] - 1 == zy[1] or zy[0] + 1 == zy[1]:
            setBlock(
                "minecraft:cobblestone_slab",
                FPpos[0] - 1,
                round((zy[0] + zy[1]) / 2) - 1,
                FPpos[2],
            )
            setBlock(
                "minecraft:cobblestone_slab",
                FPpos[0] + 1,
                round((zy[0] + zy[1]) / 2) - 1,
                FPpos[2],
            )
        elif xy[0] - 1 == xy[1] or xy[0] + 1 == xy[1]:
            setBlock(
                "minecraft:cobblestone_slab",
                FPpos[0],
                round((xy[0] + xy[1]) / 2) - 1,
                FPpos[2] - 1,
            )
            setBlock(
                "minecraft:cobblestone_slab",
                FPpos[0],
                round((xy[0] + xy[1]) / 2) - 1,
                FPpos[2] + 1,
            )

    # -------- interior --------#

    # interior(pos1,pos2,doorpos)


if __name__ == "__main__":
    pos1 = [260, 3, 180]
    pos2 = [269, 3, 189]
    door = ["south", "north", "east", "west"]
    cb = random.randint(0, 3)
    mat = [
        "oak_log",
        "oak_planks",
        "oak_stairs",
        "white_terracotta",
        "stone",
        "stone_stairs",
        "oak_door",
        "stone_stairs",
        "glass_pane",
        "spruce_stairs",
        "spruce_planks",
        "spruce_slab",
        "oak_slab",
    ]
    pos = [
        pos1[0] - 2,
        pos1[1],
        pos1[2] - 2,
        pos2[0] + 2,
        pos2[1] + 20,
        pos2[2] + 2,
    ]
    fill("air", pos)
    pos = [pos1[0], pos1[1], pos1[2], pos2[0], pos2[1], pos2[2]]
    # house(pos1,pos2,mat,door[cb],1)
    for elt in range(10):
        house([pos[0], pos[1], pos[2]], [pos[3], pos[4], pos[5]], "south", 1)
        pos = [
            pos1[0],
            pos1[1],
            pos1[2] + 1 * 15,
            pos2[0],
            pos2[1],
            pos2[2] + 1 * 15,
        ]
        house([pos[0], pos[1], pos[2]], [pos[3], pos[4], pos[5]], "south", 1)
        pos = [
            pos1[0],
            pos1[1],
            pos1[2] + 2 * 15,
            pos2[0],
            pos2[1],
            pos2[2] + 2 * 15,
        ]
        house([pos[0], pos[1], pos[2]], [pos[3], pos[4], pos[5]], "south", 1)
        pos = [
            pos1[0],
            pos1[1],
            pos1[2] + 3 * 15,
            pos2[0],
            pos2[1],
            pos2[2] + 3 * 15,
        ]
        house([pos[0], pos[1], pos[2]], [pos[3], pos[4], pos[5]], "south", 1)
        pos = [
            pos1[0],
            pos1[1],
            pos1[2] + 4 * 15,
            pos2[0],
            pos2[1],
            pos2[2] + 4 * 15,
        ]
        house([pos[0], pos[1], pos[2]], [pos[3], pos[4], pos[5]], "south", 1)
        pos = [
            pos1[0],
            pos1[1],
            pos1[2] + 5 * 15,
            pos2[0],
            pos2[1],
            pos2[2] + 5 * 15,
        ]
        house([pos[0], pos[1], pos[2]], [pos[3], pos[4], pos[5]], "south", 1)
        pos = [
            pos1[0],
            pos1[1],
            pos1[2] + 6 * 15,
            pos2[0],
            pos2[1],
            pos2[2] + 6 * 15,
        ]
        house([pos[0], pos[1], pos[2]], [pos[3], pos[4], pos[5]], "south", 1)
        pos = [
            pos1[0],
            pos1[1],
            pos1[2] + 7 * 15,
            pos2[0],
            pos2[1],
            pos2[2] + 7 * 15,
        ]
        house([pos[0], pos[1], pos[2]], [pos[3], pos[4], pos[5]], "south", 1)
        pos = [
            pos1[0],
            pos1[1],
            pos1[2] + 8 * 15,
            pos2[0],
            pos2[1],
            pos2[2] + 8 * 15,
        ]
        house([pos[0], pos[1], pos[2]], [pos[3], pos[4], pos[5]], "south", 1)
        pos = [
            pos1[0],
            pos1[1],
            pos1[2] + 9 * 15,
            pos2[0],
            pos2[1],
            pos2[2] + 9 * 15,
        ]
        house([pos[0], pos[1], pos[2]], [pos[3], pos[4], pos[5]], "south", 1)
        pos = [
            pos1[0],
            pos1[1],
            pos1[2] + 10 * 15,
            pos2[0],
            pos2[1],
            pos2[2] + 10 * 15,
        ]
        house([pos[0], pos[1], pos[2]], [pos[3], pos[4], pos[5]], "south", 1)
        pos = [
            pos1[0],
            pos1[1],
            pos1[2] + 11 * 15,
            pos2[0],
            pos2[1],
            pos2[2] + 11 * 15,
        ]
        house([pos[0], pos[1], pos[2]], [pos[3], pos[4], pos[5]], "south", 1)
        pos1[0], pos2[0] = pos1[0] + 15, pos2[0] + 15
