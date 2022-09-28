#!/usr/bin/python
# -*- coding: UTF-8 -*-
from functions import *
import wfc
from Prototypes import Prototypes
# displayName = "WFC"


dict_4_WFC = {}

dict_4_WFC['minecraft:air'] = (0, 0)
dict_4_WFC['minecraft:jungle_log[axis=y,]'] = (17, 3)
dict_4_WFC['minecraft:jungle_planks'] = (5, 3)
dict_4_WFC['minecraft:glass'] = (20, 0)

dict_4_WFC['minecraft:oak_door[hinge=right,half=lower,powered=false,facing=east,open=false,]'] = (64, 0)
dict_4_WFC['minecraft:oak_door[hinge=right,half=upper,powered=false,facing=east,open=false,]'] = (64, 8)

dict_4_WFC['minecraft:oak_door[hinge=right,half=lower,powered=false,facing=south,open=false,]'] = (64, 1)
dict_4_WFC['minecraft:oak_door[hinge=right,half=upper,powered=false,facing=south,open=false,]'] = (64, 8)

dict_4_WFC['minecraft:oak_door[hinge=right,half=lower,powered=false,facing=west,open=false,]'] = (64, 2)
dict_4_WFC['minecraft:oak_door[hinge=right,half=upper,powered=false,facing=west,open=false,]'] = (64, 8)

dict_4_WFC['minecraft:oak_door[hinge=right,half=lower,powered=false,facing=north,open=false,]'] = (64, 3)
dict_4_WFC['minecraft:oak_door[hinge=right,half=upper,powered=false,facing=north,open=false,]'] = (64, 8)

dict_4_WFC['minecraft:yellow_carpet'] = (171, 4)
dict_4_WFC['minecraft:green_carpet'] = (171, 13)
dict_4_WFC['minecraft:lantern[waterlogged=false,hanging=true,]'] = (89, 0)
dict_4_WFC['minecraft:stone_brick_slab[waterlogged=false,type=bottom,]'] = (44, 5)
dict_4_WFC['minecraft:stone_bricks'] = (43, 5)

dict_4_WFC['minecraft:oak_planks'] = (5, 0)
dict_4_WFC['minecraft:oak_stairs[half=bottom,waterlogged=false,shape=straight,facing=south,]'] = (53, 2)
dict_4_WFC['minecraft:oak_stairs[half=bottom,waterlogged=false,shape=straight,facing=east,]'] = (53, 0)

dict_4_WFC['minecraft:jungle_fence[east=false,waterlogged=false,south=false,north=false,west=false,]'] = (190, 0)
dict_4_WFC['minecraft:oak_stairs[half=bottom,waterlogged=false,shape=straight,facing=north,]'] = (53, 3)
dict_4_WFC['minecraft:oak_stairs[half=bottom,waterlogged=false,shape=straight,facing=west,]'] = (53, 1)
dict_4_WFC['minecraft:spruce_pressure_plate[powered=false,]'] = (72, 0)
# dict_4_WFC[''] = (, )
# dict_4_WFC[''] = (, )
# dict_4_WFC[''] = (, )
# dict_4_WFC[''] = (, )
# dict_4_WFC[''] = (, )

unseen_blocks = []


def build(level, xside, yside, zside, minx, miny, minz):
    prototypes = Prototypes(level=None)
    bd = prototypes.read("./stock-filters/prototypes_stone_27.txt")
    w = wfc.WFC(xside, yside, zside, bd, AUTO=0)
    r = False
    while r == False:
        r = w.run(level=None, visualize=False)
        print(r)

    # print wfc.finalwave
    # print wfc.wave
    w.setBuilding(0, 0, 0)
    for one in wfc.blocks:
        if dict_4_WFC.has_key(one[3]):
            id = dict_4_WFC[one[3]]
            setBlock(level, one[0] + minx, one[1] + miny, one[2] + minz, id[0], id[1])
        else:
            if one[3] not in unseen_blocks:
                unseen_blocks.append(one[3])

    for one in unseen_blocks:
        print one


# def perform(level, box, options):
#     """map_R1
#     start_x = 140, start_z = 30
#     width(x) = 256, depth(z) = 256
#     map_R2
#     start_x = 3, start_z = -6
#     width(x) = 256, depth(z) = 256
#     map_R3
#     start_x = -346, start_z = -66
#     width(x) = 256, depth(z) = 256
#     """
#     (width, height, depth) = getBoxSize(box)
#     start_x = box.minx
#     start_z = box.minz
#     end_x = box.maxx
#     end_z = box.maxz
#
#     build(level, 10, 10, 10, start_x, box.miny+2, start_z)