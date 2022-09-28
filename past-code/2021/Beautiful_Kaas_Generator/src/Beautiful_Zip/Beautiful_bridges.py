import utilityFunctions as utilityFunctions
from pymclevel import biome_types
from pymclevel.box import BoundingBox

import random
import math
import numpy as np

from Beautiful_meta_analysis import get_height_map


# Information visible in mcedit, can be used for user-input
inputs = (
	("Bridge Generator", "label"),
	("Creator: Elin", "label"),
    # ("length (x)", (7, 0, 128)),
    # ("height (y)", (5, 0, 128)),
    # ("length (z)", (12, 0, 128)),
    # ("offset (x)", (0, -256, 256)),
    # ("offset (y)", (4, 0, 256)),
    # ("offset (z)", (0, -256, 256)),
    # ("door location (W=0, N=1, E=2, S=3)", (0, 0, 3)),
    # ("number of floors", (2, 1, 5)),
    ("bridge type (all stairs=0, half stairs=1, flat=2)", (0, 0, 2))
)

# def east_west_roof(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z):
#     z_center = base_z + length_z/2
#     z_south = z_center - 1 if length_z % 2 == 0 else z_center
#     for x in range(base_x, base_x + length_x):
#         y = base_y+height_y
#         for z in range(base_z, z_center):
#             utilityFunctions.setBlock(level, (67,2), x, y, z)
#             y += 1
#         adjust = 0
#         if length_z % 2 != 0:
#             adjust = 1
#             utilityFunctions.setBlock(level, (4,0), x, y - 1, z_center)

#         y = base_y+height_y
#         for z in range(base_z + length_z - 1, z_south, -1):
#             utilityFunctions.setBlock(level, (67,3), x, y, z)
#             y += 1

#     y_r = base_y+height_y

#     for z in range(base_z, z_center):
#         for y in range(base_y+height_y, y_r):
#             utilityFunctions.setBlock(level, (4,0), base_x, y, z)
#             utilityFunctions.setBlock(level, (4,0), base_x + length_x - 1, y, z)
#         y_r += 1
#     adjust = 0
#     if length_z % 2 != 0:
#         adjust = 1
#         for y in range(base_y+height_y, y_r - 1):
#             utilityFunctions.setBlock(level, (4,0), base_x, y, z_center)
#             utilityFunctions.setBlock(level, (4,0), base_x + length_x - 1, y, z_center)

#     y_r = base_y+height_y
#     for z in range(base_z + length_z - 1, z_south, -1):
#         for y in range(base_y+height_y, y_r):
#             utilityFunctions.setBlock(level, (4,0), base_x, y, z)
#             utilityFunctions.setBlock(level, (4,0), base_x + length_x - 1, y, z)
#         y_r += 1


# def small_stairs_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z):
#     x_center = base_x + length_x/2
#     x_west = x_center - 1 if length_x % 2 == 0 else x_center

#     y = base_y+height_y+1
#     for x in range(base_x, x_center):
#         utilityFunctions.setBlock(level, (67,0), x, y, base_z)
#         y += 1

#     y = base_y+height_y+1
#     for x in range(base_x + length_x - 1, x_west, -1):
#         utilityFunctions.setBlock(level, (67,1), x, y, base_z)
#         y += 1

#     if length_x % 2 != 0: # Building has an uneven with. Random chance to place another block in the middle on top
#         extra_top = random.randint(0, 1)
#         if extra_top:
#             utilityFunctions.setBlock(level, (44,0), x_center, y, base_z)

# def large_stairs_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z):
#     x_center = base_x + length_x/2
#     x_west = x_center - 1 if length_x % 2 == 0 else x_center
#     y_r = base_y+height_y+1
#     for x in range(base_x, x_center):
#         utilityFunctions.setBlock(level, (4,0), x, y_r, base_z)
#         y_r += 1
#     y_r = base_y+height_y+1
#     for x in range(base_x + length_x - 1, x_west, -1):
#         utilityFunctions.setBlock(level, (4,0), x, y_r, base_z)
#         y_r += 1

#     if length_x%2 != 0: # Building has an uneven with. Random chance to place another block in the middle on top
#         extra_top = random.randint(0, 1)
#         if extra_top:
#             utilityFunctions.setBlock(level, (4,0), x_center, y_r, base_z)


# def facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z, facade_type):
#     x_center = base_x + length_x/2
#     x_west = x_center - 1 if length_x % 2 == 0 else x_center
#     # Heightening the facade...
#     for x in range(0, length_x):
#         utilityFunctions.setBlock(level, (4,0), x, base_y+height_y, base_z)

#     y_r = base_y+height_y
#     for x in range(base_x, x_center):
#         utilityFunctions.setBlock(level, (4,0), x, y_r, base_z)
#         y_r += 1

#     if length_x % 2 != 0:
#         utilityFunctions.setBlock(level, (4,0), x_center, y_r-1, base_z)
#         utilityFunctions.setBlock(level, (4,0), x_center, y_r, base_z)

#     y_r = base_y+height_y
#     for x in range(base_x + length_x - 1, x_west, -1):
#         utilityFunctions.setBlock(level, (4,0), x, y_r, base_z)
#         y_r += 1

#     # Roof types. Roof type 0 is just doing nothing: small staircase facade.
#     if facade_type == 0: # Small staircase facade
#         small_stairs_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z)

#     elif facade_type == 1: # Large staircase facade
#         large_stairs_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z)

#     elif facade_type == 2: # Lit. translation: clock/neck type facade
#         small_stairs_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z) # Side of facade
#         clock_facade(level, box, length_x, height_y, length_z, base_x, base_y, base_z) # Center of facade


# def north_south_roof(level, box, length_x, height_y, length_z, base_x, base_y, base_z, facade_type):
#     x_center = base_x + length_x/2
#     x_west = x_center - 1 if length_x % 2 == 0 else x_center

#     for z in range(base_z, base_z + length_z):
#         y = base_y+height_y
#         for x in range(base_x, x_center):
#             utilityFunctions.setBlock(level, (67,0), x, y, z)
#             y += 1
#         adjust = 0
#         if length_x % 2 != 0:
#             adjust = 1
#             utilityFunctions.setBlock(level, (4,0), x_center, y - 1, z)

#         y = base_y+height_y
#         for x in range(base_x + length_x - 1, x_west, -1):
#             utilityFunctions.setBlock(level, (67,1), x, y, z)
#             y += 1

#     y_r = base_y+height_y
#     for x in range(base_x, x_center):
#         for y in range(base_y+height_y, y_r):
#             utilityFunctions.setBlock(level, (4,0), x, y, base_z)
#             utilityFunctions.setBlock(level, (4,0), x, y, base_z + length_z - 1)
#         y_r += 1
#     adjust = 0
#     if length_x % 2 != 0:
#         adjust = 1
#         for y in range(base_y+height_y, y_r):
#             utilityFunctions.setBlock(level, (4,0), x_center, y, base_z)
#             utilityFunctions.setBlock(level, (4,0), x_center, y, base_z + length_z - 1)

#     y_r = base_y+height_y
#     for x in range(base_x + length_x - 1, x_west, -1):
#         for y in range(base_y+height_y, y_r):
#             utilityFunctions.setBlock(level, (4,0), x, y, base_z)
#             utilityFunctions.setBlock(level, (4,0), x, y, base_z + length_z - 1)
#         y_r += 1

#     return y_r-1


# def build_floor(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z, front_side, stair_loc, top_offset):
#     wall_block = (20,0)
#     #Walls of the house:
#     x = base_x#z-directional wall
#     for z in range(base_z + 1, base_z + length_z - 1):
#         for y in range(base_y, base_y + height_y + top_offset):
#             utilityFunctions.setBlock(level, wall_block, x, y, z)

#     z = base_z
#     for x in range (base_x + 1, base_x + length_x - 1):#x-directional wall
#         for y in range(base_y, base_y + height_y + top_offset):
#             utilityFunctions.setBlock(level, wall_block, x, y, z)

#     #Other walls:
#     x = base_x + length_x - 1#z-directional wall
#     for z in range(base_z + 1, base_z + length_z - 1):
#         for y in range(base_y, base_y + height_y + top_offset):
#             utilityFunctions.setBlock(level, wall_block, x, y, z)

#     z = base_z + length_z - 1
#     for x in range (base_x + 1, base_x + length_x - 1):#x-directional wall
#         for y in range(base_y, base_y + height_y + top_offset):
#             utilityFunctions.setBlock(level, wall_block, x, y, z)


#     if stair_loc == 0:
#         #stair on west side, grow to south side
#         start_x = base_x + 1
#         start_z = base_z + length_z - height_y - 2

#         for i in range(height_y):
#             utilityFunctions.setBlock(level, (67,2), start_x, base_y+i, start_z+i)
#             if i < height_y - 1:
#                 utilityFunctions.setBlock(level, (67,7), start_x, base_y+i, start_z+i+1)
#             else:#one extra floor block for more convenient walking
#                 utilityFunctions.setBlock(level, (1,0), start_x, base_y+i, start_z+i+1)

#         y_ceiling = base_y + height_y - 1

#         for z in range(base_z + 1, start_z):
#             utilityFunctions.setBlock(level, (1,0), base_x + 1, y_ceiling, z)
#         for x in range (base_x + 2, base_x + length_x - 1):
#             for z in range(base_z + 1, base_z + length_z - 1):
#                 utilityFunctions.setBlock(level, (1,0), x, y_ceiling, z)
#     #elif stair_loc == 1:
#         #stair on north side grow to west side
#     elif stair_loc == 2:
#         #stair on east side grow to north side
#         start_x = base_x + length_x - 2
#         start_z = base_z + height_y + 1
#         utilityFunctions.setBlock(level, (67,1), start_x, base_y, start_z)

#         for i in range(height_y):
#             utilityFunctions.setBlock(level, (67,3), start_x, base_y+i, start_z-i)
#             if i < height_y - 1:
#                 utilityFunctions.setBlockIfEmpty(level, (67,6), start_x, base_y+i, start_z-i-1)
#             else:#one extra floor block for more convenient walking
#                 utilityFunctions.setBlockIfEmpty(level, (1,0), start_x, base_y+i, start_z-i-1)

#         y_ceiling = base_y + height_y - 1

#         for z in range(start_z + 1, base_z + length_z - 1):
#             utilityFunctions.setBlock(level, (1,0), base_x + length_x - 2, y_ceiling, z)
#         for x in range (base_x + 1, base_x + length_x - 2):
#             for z in range(base_z + 1, base_z + length_z - 1):
#                 utilityFunctions.setBlock(level, (1,0), x, y_ceiling, z)
#     #else: #if stair_loc == 3:
#         #stair on south side grow to east side

# # Start of the Generation script
# #  @ level: Minecraft world
# #  @ box: selected box by mcedit
# #  @ options: user defined inputs from mcedit
# def build_house(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z, door_loc, no_floors, facade_type):
#     #Walls:
#     temp_base_y = base_y
#     stair_loc = 0
#     for i in range(no_floors):
#         if i == no_floors - 1:
#             build_floor(level, box, options, length_x, height_y, length_z, base_x, temp_base_y, base_z, 1, stair_loc, 1)
#         else:
#             build_floor(level, box, options, length_x, height_y, length_z, base_x, temp_base_y, base_z, 1, stair_loc, 0)
#         stair_loc += 2
#         stair_loc %= 4
#         temp_base_y += height_y
#     temp_base_y -= height_y - 1

#     #floor:
#     for x in range (base_x + 1, base_x + length_x - 1):
#         for z in range(base_z + 1, base_z + length_z - 1):
#             utilityFunctions.setBlock(level, (1,0), x, base_y-1, z)

def build_halfstair_bridge(level, box, y_base, bridge_material):
    xdif = box.maxx - box.minx 
    zdif = box.maxz - box.minz 

    if xdif > zdif:
        for z in range(box.minz, box.maxz): 
            step = 0
            for x in range(box.minx, box.maxx):
                if step < 3:
                    step += 1
                elif step > 3:
                    step -= 1
                else:
                    None

                y = y_base + step
                utilityFunctions.setBlock(level, (1,0), x, y, z)

    else:
        for x in range(box.minx, box.maxx):
            step = 0
            for z in range(box.minz, box.maxz): 
                if step < 3:
                    step += 1
                elif step > 3:
                    step -= 1
                else:
                    None

                y = y_base + step
                utilityFunctions.setBlock(level, (1,0), x, y, z)


def build_flat_bridge(level, box, y_base, bridge_material):
    for x in range(box.minx, box.maxx):
        for z in range(box.minz, box.maxz):
            utilityFunctions.setBlock(level, bridge_material, x, y_base, z)


def fillup_fundering(level, box, height_map, y_base, horizontal):
    '''Fill underneath start and ending steps '''

    if horizontal:
        start_step = height_map[0, :]
        highest_in_startstep = max(start_step) + y_base

        for count, z in enumerate(range(box.minz, box.maxz)):
            block_height = start_step[count]

        for positions in start_steps:
            # fill up with stone / dirt
            None

        end_step = height_map[-1, :]
        highest_in_endstep = max(end_step) + y_base

        for positions in start_steps:
            # fill up with stone / dirt
            None
    else:
        start_step = height_map[:, 0]
        end_step = height_map[:, -1]
        
        highest_in_startstep = max(start_step) + y_base

        for positions in start_steps:
            # fill up with stone / dirt
            None

        end_step = height_map[-1, :]
        highest_in_endstep = max(end_step) + y_base

        for positions in start_steps:
            # fill up with stone / dirt
            None

    highest_in_endstep = max(end_step) + y_base


def find_direction(box):
    """Find out in the bridge should be build in long or wide form"""
    xdif = box.maxx - box.minx 
    zdif = box.maxz - box.minz 

    # is horizontal?
    if xdif > zdif:
        return True
    else:
        return False

def build_bridge(level, box, bridge_type):
    horizontal = find_direction(box)
    bridge_material = (1,0)

    #x = width, z = length
    print(box.width)
    print(box.length)

    # get at which height the bridge should be built + how high in should be
    height_map = get_height_map(level, box)
    ymax_ratio = np.max(height_map)
    ymax_overal = box.maxy
    y_base = ymax_overal - ymax_ratio

    fillup_fundering(level, box, height_map, y_base, horizontal)

    if bridge_type == 0:
        build_flat_bridge(level, box, y_base, bridge_material)
    elif bridge_type == 1:
        build_halfstair_bridge(level, box, y_base, bridge_material)







    # # height_map = get_height_map(level, box)
    # highest_val = box.maxy
    # # bridge_material = get_col_pal().bridge
    # bridge_material = (1, 0)
    # y_base = highest_val


    # elif bridge_type == 2:
    #     build_flat_bridge(level, box, y_base, bridge_material)




def perform(level, box, options):
    #'''
    # height_y = options["height (y)"]
    # length_z = options["length (z)"]
    # length_x = options["length (x)"]
    # base_x = options["offset (x)"]
    # base_y = options["offset (y)"]
    # base_z = options["offset (z)"]
    # door_loc = options["door location (W=0, N=1, E=2, S=3)"]
    # no_floors = options["number of floors"]
    bridge_type = options["bridge type (all stairs=0, half stairs=1, flat=2)"]
    #'''

    #build_floor(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z, 1, 2)
    # build_house(level, box, options, length_x, height_y, length_z, base_x, base_y, base_z, door_loc, no_floors, facade_type)
    build_bridge(level, box, bridge_type)

