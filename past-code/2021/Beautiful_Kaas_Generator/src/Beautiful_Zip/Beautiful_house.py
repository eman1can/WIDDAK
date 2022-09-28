import utilityFunctions as utilityFunctions
from pymclevel import biome_types, schematic, MCSchematic, box as bx
from Beautiful_Pallete import Pallete
import random
import math

#from scematic import MCSchematic, extractSchematicFrom


# Information visible in mcedit, can be used for user-input
inputs = (
	("Canal House Generator", "label"),
	("Creator: Koen and Sem", "label"),
    ("length (x)", (8, 0, 256)),
    ("height (y)", (4, 0, 256)),
    ("length (z)", (8, 0, 256)),
    ("offset (x)", (0, -256, 256)),
    ("offset (y)", (3, 0, 256)),
    ("offset (z)", (0, -256, 256)),
    ("door location (N=0, W=1, S=2, E=3)", (0, 0, 3)),
    ("number of floors", (2, 1, 10)),
    ("facade type (small stairs=0, large stairs=1, bell=2", (0, 0, 2))
)


def small_stairs_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center

    y = base_y+height_y+1
    for x in range(base_x, x_center):
        utilityFunctions.setBlock(level, (pallete.quartz_stair,0), x, y, base_z)
        y += 1

    y = base_y+height_y+1
    for x in range(base_x + length_x - 1, x_west, -1):
        utilityFunctions.setBlock(level, (pallete.quartz_stair,1), x, y, base_z)
        y += 1

    if length_x % 2 != 0: # Building has an uneven with
        utilityFunctions.setBlock(level, pallete.quartz_slab, x_center, y, base_z)

def large_stairs_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center
    y_r = base_y+height_y+1
    for x in range(base_x, x_center):
        utilityFunctions.setBlock(level, pallete.wall, x, y_r, base_z)
        utilityFunctions.setBlock(level, pallete.quartz_slab, x, y_r+1, base_z)
        y_r += 1
    y_r = base_y+height_y+1
    for x in range(base_x + length_x - 1, x_west, -1):
        utilityFunctions.setBlock(level, pallete.wall, x, y_r, base_z)
        utilityFunctions.setBlock(level, pallete.quartz_slab, x, y_r+1, base_z)
        y_r += 1

    if length_x%2 != 0: # Building has an uneven with. Random chance to place another block in the middle on top
        extra_top = random.randint(0, 1)
        if extra_top:
            utilityFunctions.setBlock(level, pallete.wall, x_center, y_r, base_z)
            utilityFunctions.setBlock(level, pallete.quartz_slab, x_center, y_r+1, base_z)
        else:
            utilityFunctions.setBlock(level, pallete.quartz_slab, x_center, y_r, base_z)

def clock_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center
    y = base_y+height_y+1
    facade_height = int(y + length_x*0.7)
    side_parts = length_x // 3
    middle_part = (length_x // 3) + (length_x % 3)
    for x in range(side_parts, middle_part + side_parts):
        for y_r in range(y, facade_height):
            utilityFunctions.setBlock(level, pallete.wall, x, y_r, base_z)
    utilityFunctions.setBlock(level, (pallete.quartz_stair,0), side_parts, facade_height-1, base_z)
    utilityFunctions.setBlock(level, (pallete.quartz_stair,1), length_x-side_parts-1, facade_height-1, base_z)

    for x in range(side_parts, x_center):
        y = facade_height
        y_r = facade_height + (x-side_parts) * 0.5
        while y < y_r:
            if y_r-y > 0.5:
                utilityFunctions.setBlock(level, pallete.wall, x, y, base_z)
            else:
                utilityFunctions.setBlock(level, pallete.quartz_slab, x, y, base_z)
            y += 1
        y_r += 0.5

    y_r = facade_height
    for x in range(length_x-side_parts-1, x_center-1, -1):
        y = facade_height
        y_r = facade_height + ((length_x-side_parts-1)-x) * 0.5
        while y < y_r:
            if y_r-y > 0.5:
                utilityFunctions.setBlock(level, pallete.wall, x, y, base_z)
            else:
                utilityFunctions.setBlock(level, pallete.quartz_slab, x, y, base_z)
            y += 1
        y_r += 0.5

def facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z, facade_type):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center

    # Heightening the facade and replacing blocks with facade type...
    y_r = base_y+height_y+1
    for x in range(base_x, x_center):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, pallete.wall, x, y, base_z)
        y_r += 1

    if length_x % 2 != 0:
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, pallete.wall, x_center, y, base_z)

    y_r = base_y+height_y+1
    for x in range(base_x + length_x - 1, x_west, -1):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, pallete.wall, x, y, base_z)
        y_r += 1


    # Roof types. Roof type 0 is just doing nothing: small staircase facade.
    if facade_type == 0: # Small staircase facade
        small_stairs_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z)

    elif facade_type == 1: # Large staircase facade
        pass
        large_stairs_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z)

    elif facade_type == 2: # Lit. translation: clock/neck type facade
        small_stairs_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z) # Side of facade
        clock_facade(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z) # Center of facade

    # Place windows in facade
    for y in range(base_y+height_y, y_r-2):
        utilityFunctions.setBlock(level, pallete.window, x_center, y, base_z)

    for y in range(base_y+height_y, y_r-2):
        utilityFunctions.setBlock(level, pallete.window, x_west, y, base_z)

def ground_floor_windows(level, pallete, width, height):
    z = 0
    if width <= 6:
        for x in [1,width-4]:
            for y in range(2, height):
                utilityFunctions.setBlock(level, pallete.window, x, y, z)#DONE
    elif width <= 8:
        #width = 7 or 8
        for x in [1,width-2]:
            for y in range(2, height):
                utilityFunctions.setBlock(level, pallete.window, x, y, z)
    else:
        #width = 9 or 10
        for x in [1, 2, width - 3, width-2]:
            for y in range(2, height):
                utilityFunctions.setBlock(level, pallete.window, x, y, z)

def other_floor_windows(level, pallete, width, height, offset):
    z = 0
    if width <= 6:
        for x in [1,width-2]:
            for y in range(offset + 2, offset + height):
                utilityFunctions.setBlock(level, pallete.window, x, y, z)#DONE
    elif width == 7:
        for x in [1, 3, width-2]:
            for y in range(offset + 2, offset + height):
                utilityFunctions.setBlock(level, pallete.window, x, y, z)#DONE
    elif width == 8:
        #width = 7 or 8
        for x in [1, 2, width-3, width-2]:
            for y in range(offset + 2, offset + height):
                utilityFunctions.setBlock(level, pallete.window, x, y, z)
    else:
        #width = 9 or 10
        for x in [1, 2, 4, width - 5, width - 3, width-2]:
            for y in range(offset + 2, offset + height):
                utilityFunctions.setBlock(level, pallete.window, x, y, z)

def windows(level, pallete, length_x, height_y, no_floors, window_width, door_x):
    x_center = length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center

    window_max_height = height_y-2 # window height is depending on floor height

    for window_x in range(1, x_center+1, window_width+1):
        for i in range(window_x, min(window_x+window_width, x_center+1)):
            if i == door_x-1 or i == door_x+1:
                pass

            #elif i == door_x: # If on same place as the window
            else:
                for j in range(2, 1+window_max_height+1):
                    utilityFunctions.setBlock(level, pallete.window, i, j, 0)

    for window_x in range(length_x-2, x_west, -(window_width+1)):
        for i in range(window_x, window_x-min(window_width, window_x-x_west), -1):
            if i == door_x-1 or i == door_x+1:
                pass

            else:
                for j in range(2, 1+window_max_height+1):
                    utilityFunctions.setBlock(level, pallete.window, i, j, 0)

    for j in range(3, 1+window_max_height+1):
        utilityFunctions.setBlock(level, pallete.door_window, door_x, j, 0)


    y_r = 1 + height_y + 1
    for floors in range(1, no_floors): # Windows on higher floors
        for window_x in range(1, x_center+1, window_width+1):
            for i in range(window_x, min(window_x+window_width, x_center+1)):
                for j in range(window_max_height):
                    utilityFunctions.setBlock(level, pallete.window, i, y_r+j, 0)

        for window_x in range(length_x-2, x_west, -(window_width+1)):
            for i in range(window_x, window_x-min(window_width, window_x-x_west), -1):
                for j in range(window_max_height):
                    utilityFunctions.setBlock(level, pallete.window, i, y_r+j, 0)

        y_r += height_y

def build_roof(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z):
    x_center = base_x + length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center

    for z in range(base_z, base_z + length_z):
        y = base_y+height_y
        for x in range(base_x, x_center):
            utilityFunctions.setBlock(level, (pallete.roof_stair,0), x, y, z)
            y += 1
        adjust = 0
        if length_x % 2 != 0:
            adjust = 1
            utilityFunctions.setBlock(level, pallete.roof_block, x_center, y - 1, z)

        y = base_y+height_y
        for x in range(base_x + length_x - 1, x_west, -1):
            utilityFunctions.setBlock(level, (pallete.roof_stair,1), x, y, z)
            y += 1

    y_r = base_y+height_y
    for x in range(base_x, x_center):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, pallete.roof_block, x, y, base_z)
            utilityFunctions.setBlock(level, pallete.roof_block, x, y, base_z + length_z - 1)
        y_r += 1

    if length_x % 2 != 0:
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, pallete.roof_block, x_center, y, base_z)
            utilityFunctions.setBlock(level, pallete.roof_block, x_center, y, base_z + length_z - 1)

    y_r = base_y+height_y
    for x in range(base_x + length_x - 1, x_west, -1):
        for y in range(base_y+height_y, y_r):
            utilityFunctions.setBlock(level, pallete.roof_block, x, y, base_z)
            utilityFunctions.setBlock(level, pallete.roof_block, x, y, base_z + length_z - 1)
        y_r += 1

    return y_r-1

def build_floor(level, pallete, length_x, height_y, length_z, base_x, base_y, base_z, stair_loc, top_offset, ladder):
    x = base_x#z-directional wall
    for z in range(base_z + 1, base_z + length_z - 1):
        for y in range(base_y, base_y + height_y + top_offset):
            utilityFunctions.setBlock(level, pallete.wall, x, y, z)

    z = base_z
    for x in range (base_x + 1, base_x + length_x - 1):#x-directional wall
        for y in range(base_y, base_y + height_y + top_offset):
            utilityFunctions.setBlock(level, pallete.wall, x, y, z)

    #Other walls:
    x = base_x + length_x - 1#z-directional wall
    for z in range(base_z + 1, base_z + length_z - 1):
        for y in range(base_y, base_y + height_y + top_offset):
            utilityFunctions.setBlock(level, pallete.wall, x, y, z)

    z = base_z + length_z - 1
    for x in range (base_x + 1, base_x + length_x - 1):#x-directional wall
        for y in range(base_y, base_y + height_y + top_offset):
            utilityFunctions.setBlock(level, pallete.wall, x, y, z)

    #Corner Pillars:
    for y in range(base_y, base_y+height_y + top_offset):
         utilityFunctions.setBlock(level, pallete.pillar, base_x, y, base_z)
         utilityFunctions.setBlock(level, pallete.pillar, base_x, y, base_z + length_z - 1)
         utilityFunctions.setBlock(level, pallete.pillar, base_x + length_x - 1, y, base_z)
         utilityFunctions.setBlock(level, pallete.pillar, base_x + length_x - 1, y, base_z + length_z - 1)

    y_ceiling = base_y + height_y - 1

    if ladder:
        x_ladd = length_x - 2 if stair_loc == 2 else 1
        z_ladd = length_z - 2
        for y in range(base_y, base_y+ height_y):
            utilityFunctions.setBlock(level, (pallete.ladder, 2), x_ladd, y, z_ladd)

        for x in range(1, length_x - 1):
            for z in range(1, length_z - 2):
                utilityFunctions.setBlock(level, pallete.floor, x, y_ceiling, z)
            if (x != x_ladd and level.blockAt(x, y, z_ladd) == 0):
                utilityFunctions.setBlock(level, pallete.floor, x, y_ceiling, z_ladd)


    #end if ladder
    else:
        if stair_loc == 0:
            #stair on west side, grow to south side
            start_x = base_x + 1
            start_z = base_z + length_z - height_y - 2

            for i in range(height_y):
                utilityFunctions.setBlock(level, (pallete.stair, 2), start_x, base_y+i, start_z+i)
                if i < height_y - 1:
                    utilityFunctions.setBlock(level, (pallete.stair, 7), start_x, base_y+i, start_z+i+1)
                else:#one extra floor block for more convenient walking
                    utilityFunctions.setBlock(level, pallete.floor, start_x, base_y+i, start_z+i+1)

            for z in range(base_z + 1, start_z):
                utilityFunctions.setBlock(level, pallete.floor, base_x + 1, y_ceiling, z)
            for x in range (base_x + 2, base_x + length_x - 1):
                for z in range(base_z + 1, base_z + length_z - 1):
                    utilityFunctions.setBlock(level, pallete.floor, x, y_ceiling, z)
        #end if stair_loc
        elif stair_loc == 2:
            #stair on east side grow to north side
            start_x = base_x + length_x - 2
            start_z = base_z + height_y + 1
            utilityFunctions.setBlock(level, (pallete.stair,1), start_x, base_y, start_z)

            for i in range(height_y):
                utilityFunctions.setBlock(level, (pallete.stair,3), start_x, base_y+i, start_z-i)
                if i < height_y - 1:
                    utilityFunctions.setBlockIfEmpty(level, (pallete.stair,6), start_x, base_y+i, start_z-i-1)
                else:#one extra floor block for more convenient walking
                    utilityFunctions.setBlockIfEmpty(level, pallete.floor, start_x, base_y+i, start_z-i-1)

            for z in range(start_z + 1, base_z + length_z - 1):
                utilityFunctions.setBlock(level, pallete.floor, base_x + length_x - 2, y_ceiling, z)
            for x in range (base_x + 1, base_x + length_x - 2):
                for z in range(base_z + 1, base_z + length_z - 1):
                    utilityFunctions.setBlock(level, pallete.floor, x, y_ceiling, z)
        #end if stair_loc
    #end if stairs

# Function to detect walls that we can put stuff against. For some rooms, we definitely want the furniture against a wall (kitchen)
def analyse_walls(level, length_x, height_y, length_z, build_height, min_x, max_x, min_z, max_z):
    build_options = []
    if min_x == 1: # I guess this never happens, but just for completeness
        build_options.append('west')
    if max_x == length_x-1:
        build_options.append('east')
    if max_z == length_z-1:
        build_options.append('north')
    if min_z == 1:
        build_options.append('south')

    if build_options: # We can build against a wall, which is our preference
        chosen_wall = random.choice(build_options)

    else: # We cannot build against a wall, so improvise
        chosen_wall = random.choice(['north', 'south', 'east', 'west']) # We'll just build in a direction, but not against a wall

    return chosen_wall

def build_library(level, pallete, length_x, height_y, length_z, build_height, min_x, max_x, min_z, max_z): # TODO: don't place anything when near a staircase. These are in the range of height of the floor (height_y) + 4, either from front or back. Maybe even a little more space.
    chosen_wall = random.choice(['north', 'south', 'east', 'west']) # For a library, we don't care where the bookshelfs are

    x_center = length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center

    if chosen_wall == 'north' or chosen_wall == 'south':
        z = min_z
        for x in range(min_x, max_x):
            for y in range(build_height, build_height+(height_y-2)):
                utilityFunctions.setBlock(level, pallete.bookshelf, x, y, z)

            if x == min_x or x == max_x-1:
                utilityFunctions.setBlock(level, pallete.torch, x, build_height+(height_y-2), z)

        z = max_z-1
        for x in range(min_x, max_x):
            for y in range(build_height, build_height+(height_y-2)):
                utilityFunctions.setBlock(level, pallete.bookshelf, x, y, z)

            if x == min_x or x == max_x-1:
                utilityFunctions.setBlock(level, pallete.torch, x, build_height+(height_y-2), z)

        for stair_z in range (min_z+2, max_z-2): # Place benches (for reading)
            if (max_x-min_x)%2 == 0:
                utilityFunctions.setBlock(level, (pallete.int_stair, 1), x_center, build_height, stair_z)
                utilityFunctions.setBlock(level, (pallete.int_stair, 0), x_west, build_height, stair_z)
            else:
                if max_x-min_x < 3:
                    utilityFunctions.setBlock(level, (pallete.int_stair, 1), x_center, build_height, stair_z)
                else:
                    utilityFunctions.setBlock(level, (pallete.int_stair, 0), x_center-1, build_height, stair_z)
                    utilityFunctions.setBlock(level, pallete.int_wood, x_center, build_height, stair_z)
                    if stair_z == min_z+2 or stair_z == max_z-3:
                        utilityFunctions.setBlock(level, pallete.torch, x_center, build_height+1, stair_z)
                    utilityFunctions.setBlock(level, (pallete.int_stair, 1), x_center+1, build_height, stair_z)


    elif chosen_wall == 'west' or chosen_wall == 'east':
        x = min_x
        left_part = False
        go = True
        while go:
            if left_part:
                if x+1 >= max_x:
                    go = False
                    for z in range(min_z, max_z):
                        for y in range(build_height, build_height+(height_y-2)):
                            utilityFunctions.setBlock(level, pallete.bookshelf, x, y, z)

                        if z == min_z or z == max_z-1:
                            utilityFunctions.setBlock(level, pallete.torch, x, build_height+(height_y-2), z)
                    break
                for z in range(min_z+1, max_z-1):
                    utilityFunctions.setBlock(level, (pallete.int_stair, 1), x, build_height, z)

                x += 2
                if x >= max_x:
                    go = False
                    break

                for z in range(min_z, max_z):
                    for y in range(build_height, build_height+(height_y-2)):
                        utilityFunctions.setBlock(level, pallete.bookshelf, x, y, z)

                    if z == min_z or z == max_z-1:
                        utilityFunctions.setBlock(level, pallete.torch, x, build_height+(height_y-2), z)

                x += 1
                if x >= max_x:
                    go = False

            else:
                for z in range(min_z, max_z):
                    for y in range(build_height, build_height+(height_y-2)):
                        utilityFunctions.setBlock(level, pallete.bookshelf, x, y, z)

                    if z == min_z or z == max_z-1:
                        utilityFunctions.setBlock(level, pallete.torch, x, build_height+(height_y-2), z)

                x += 2
                if x >= max_x:
                    go = False
                    break

                for z in range(min_z+1, max_z-1):
                    utilityFunctions.setBlock(level, (pallete.int_stair, 0), x, build_height, z)

                x += 1
                if x >= max_x:
                    go = False
            left_part = not left_part

def build_dining(level, pallete, length_x, height_y, length_z, build_height, min_x, max_x, min_z, max_z, no_floors):
    x_center = length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center
    z_center = length_z/2

    if max_x > length_x - 3:
        x_west = x_center

    table_length_z = min((max_z-min_z), no_floors)
    table_start_z = int(z_center-math.ceil(table_length_z/2.0))

    for z in range(table_start_z, table_start_z+table_length_z):
        if z >= min_z and z < max_z:
            utilityFunctions.setBlock(level, pallete.int_fence, x_west, build_height, z)
            utilityFunctions.setBlock(level, pallete.int_slab, x_west, build_height+1, z)
            if x_west-1 >= min_x:
                utilityFunctions.setBlock(level, (pallete.int_stair, 1), x_west-1, build_height, z)
            if x_west+1 < max_x:
                utilityFunctions.setBlock(level, (pallete.int_stair, 0), x_west+1, build_height, z)

def build_kitchen(level, pallete, length_x, height_y, length_z, build_height, min_x, max_x, min_z, max_z, no_floors):
    chosen_wall = analyse_walls(level, length_x, height_y, length_z, build_height, min_x, max_x, min_z, max_z)

    if chosen_wall == 'north':
        z = max_z-1
        for x in range(min_x, max_x):
            kitchen_unit = random.choice([pallete.furnace, pallete.cauldron, pallete.chest, pallete.crafting_table])
            if kitchen_unit == pallete.cauldron:
                utilityFunctions.setBlock(level, (pallete.cauldron, random.randint(0,1)), x, build_height, z)
            elif kitchen_unit == pallete.crafting_table:
                utilityFunctions.setBlock(level, pallete.crafting_table, x, build_height, z)
            else:
                utilityFunctions.setBlock(level, (kitchen_unit, 2), x, build_height, z)
        max_z-=2

    elif chosen_wall == 'south':
        z = min_z
        for x in range(min_x, max_x):
            kitchen_unit = random.choice([pallete.furnace, pallete.cauldron, pallete.chest, pallete.crafting_table])
            if kitchen_unit == pallete.cauldron:
                utilityFunctions.setBlock(level, (pallete.cauldron, random.randint(0,1)), x, build_height, z)
            elif kitchen_unit == pallete.crafting_table:
                utilityFunctions.setBlock(level, pallete.crafting_table, x, build_height, z)
            else:
                utilityFunctions.setBlock(level, (kitchen_unit, 3), x, build_height, z)
        min_z+=2

    elif chosen_wall == 'west':
        x = min_x
        for z in range(min_z, max_z):
            kitchen_unit = random.choice([pallete.furnace, pallete.cauldron, pallete.chest, pallete.crafting_table])
            if kitchen_unit == pallete.cauldron:
                utilityFunctions.setBlock(level, (pallete.cauldron, random.randint(0,1)), x, build_height, z)
            elif kitchen_unit == pallete.crafting_table:
                utilityFunctions.setBlock(level, pallete.crafting_table, x, build_height, z)
            else:
                utilityFunctions.setBlock(level, (kitchen_unit, 5), x, build_height, z)
        min_x+=2

    elif chosen_wall == 'east':
        x = max_x-1
        for z in range(min_z, max_z):
            kitchen_unit = random.choice([pallete.furnace, pallete.cauldron, pallete.chest, pallete.crafting_table])
            if kitchen_unit == pallete.cauldron:
                utilityFunctions.setBlock(level, (pallete.cauldron, random.randint(0,1)), x, build_height, z)
            elif kitchen_unit == pallete.crafting_table:
                utilityFunctions.setBlock(level, pallete.crafting_table, x, build_height, z)
            else:
                utilityFunctions.setBlock(level, (kitchen_unit, 4), x, build_height, z)
        max_x-=2

    build_dining(level, pallete, length_x, height_y, length_z, build_height, min_x, max_x, min_z, max_z, no_floors)

# Builds a bedroom. I could use a bedroom. I'm tired. Excuse me for this spaghetti. Can't come up with anything better right now.
def build_bedroom(level, pallete, length_x, height_y, length_z, build_height, min_x, max_x, min_z, max_z):
    chosen_wall = analyse_walls(level, length_x, height_y, length_z, build_height, min_x, max_x, min_z, max_z)

    x_center = length_x/2
    x_west = x_center - 1 if length_x % 2 == 0 else x_center

    beds_r = random.random()
    if beds_r < 0.2 or length_x == 5: # Small house...
        no_beds = 1
    elif beds_r < 0.85: # Pretty high chance for two beds
        no_beds = 2
    else:
        no_beds = 3 # Jerry's easter egg

    if chosen_wall == 'north':
        if length_x % 2 == 0: # It just looks too nice to have two beds in a building with even length_x
            utilityFunctions.setBlock(level, (pallete.bed,8), x_center, build_height, max_z-1)
            utilityFunctions.setBlock(level, (pallete.bed,8), x_west, build_height, max_z-1)
            utilityFunctions.setBlock(level, (pallete.bed,0), x_center, build_height, max_z-2)
            utilityFunctions.setBlock(level, (pallete.bed,0), x_west, build_height, max_z-2)
            if x_center+1 < max_x:
                if random.randint(0,1):
                    utilityFunctions.setBlock(level, pallete.int_wood, x_center+1, build_height, max_z-1)
                    utilityFunctions.setBlock(level, pallete.torch, x_center+1, build_height+1, max_z-1)
                else:
                    utilityFunctions.setBlock(level, (pallete.chest, 2), x_center+1, build_height, max_z-1)

            if x_west-1 >= min_x:
                if random.randint(0,1):
                    utilityFunctions.setBlock(level, pallete.int_wood, x_west-1, build_height, max_z-1)
                    utilityFunctions.setBlock(level, pallete.torch, x_west-1, build_height+1, max_z-1)
                else:
                    utilityFunctions.setBlock(level, (pallete.chest, 2), x_west-1, build_height, max_z-1)


        else:
            if no_beds == 1:
                utilityFunctions.setBlock(level, (pallete.bed,8), x_center, build_height, max_z-1)
                utilityFunctions.setBlock(level, (pallete.bed,0), x_center, build_height, max_z-2)
                if x_center+1 < max_x:
                    if random.randint(0,1):
                        utilityFunctions.setBlock(level, pallete.int_wood, x_center+1, build_height, max_z-1)
                        utilityFunctions.setBlock(level, pallete.torch, x_center+1, build_height+1, max_z-1)
                    else:
                        utilityFunctions.setBlock(level, (pallete.chest, 2), x_center+1, build_height, max_z-1)

                if x_west-1 >= min_x:
                    if random.randint(0,1):
                        utilityFunctions.setBlock(level, pallete.int_wood, x_west-1, build_height, max_z-1)
                        utilityFunctions.setBlock(level, pallete.torch, x_west-1, build_height+1, max_z-1)
                    else:
                        utilityFunctions.setBlock(level, (pallete.chest, 2), x_west-1, build_height, max_z-1)


            else:
                if no_beds == 2:
                    utilityFunctions.setBlock(level, pallete.int_wood, x_center, build_height, max_z-1)
                    utilityFunctions.setBlock(level, pallete.torch, x_center, build_height+1, max_z-1)
                else:
                    utilityFunctions.setBlock(level, (pallete.bed,8), x_center, build_height, max_z-1)
                    utilityFunctions.setBlock(level, (pallete.bed,0), x_center, build_height, max_z-2)

                utilityFunctions.setBlock(level, (pallete.bed,8), x_center-1, build_height, max_z-1)
                utilityFunctions.setBlock(level, (pallete.bed,0), x_center-1, build_height, max_z-2)
                utilityFunctions.setBlock(level, (pallete.bed,8), x_center+1, build_height, max_z-1)
                utilityFunctions.setBlock(level, (pallete.bed,0), x_center+1, build_height, max_z-2)

                if x_center+2 < max_x:
                    if random.randint(0,1):
                        utilityFunctions.setBlock(level, pallete.int_wood, x_center+2, build_height, max_z-1)
                        utilityFunctions.setBlock(level, pallete.torch, x_center+2, build_height+1, max_z-1)
                    else:
                        utilityFunctions.setBlock(level, (pallete.chest, 2), x_center+2, build_height, max_z-1)

                if x_center-2 >= min_x:
                    if random.randint(0,1):
                        utilityFunctions.setBlock(level, pallete.int_wood, x_center-2, build_height, max_z-1)
                        utilityFunctions.setBlock(level, pallete.torch, x_center-2, build_height+1, max_z-1)
                    else:
                        utilityFunctions.setBlock(level, (pallete.chest, 2), x_center-2, build_height, max_z-1)


    else:
        if length_x % 2 == 0: # It just looks too nice to have two beds in a building with even length_x
            utilityFunctions.setBlock(level, (pallete.bed,10), x_center, build_height, min_z)
            utilityFunctions.setBlock(level, (pallete.bed,10), x_west, build_height, min_z)
            utilityFunctions.setBlock(level, (pallete.bed,2), x_center, build_height, min_z+1)
            utilityFunctions.setBlock(level, (pallete.bed,2), x_west, build_height, min_z+1)

            if x_center+1 < max_x:
                if random.randint(0,1):
                    utilityFunctions.setBlock(level, pallete.int_wood, x_center+1, build_height, min_z)
                    utilityFunctions.setBlock(level, pallete.torch, x_center+1, build_height+1, min_z)
                else:
                    utilityFunctions.setBlock(level, (pallete.chest, 3), x_center+1, build_height, min_z)

            if x_west-1 >= min_x:
                if random.randint(0,1):
                    utilityFunctions.setBlock(level, pallete.int_wood, x_west-1, build_height, min_z)
                    utilityFunctions.setBlock(level, pallete.torch, x_west-1, build_height+1, min_z)
                else:
                    utilityFunctions.setBlock(level, (pallete.chest, 3), x_west-1, build_height, min_z)

        else:
            if no_beds == 1:
                utilityFunctions.setBlock(level, (pallete.bed,10), x_center, build_height, min_z)
                utilityFunctions.setBlock(level, (pallete.bed,2), x_center, build_height, min_z+1)

                if x_center+1 < max_x:
                    if random.randint(0,1):
                        utilityFunctions.setBlock(level, pallete.int_wood, x_center+1, build_height, min_z)
                        utilityFunctions.setBlock(level, pallete.torch, x_center+1, build_height+1, min_z)
                    else:
                        utilityFunctions.setBlock(level, (pallete.chest, 3), x_center+1, build_height, min_z)

                if x_west-1 >= min_x:
                    if random.randint(0,1):
                        utilityFunctions.setBlock(level, pallete.int_wood, x_west-1, build_height, min_z)
                        utilityFunctions.setBlock(level, pallete.torch, x_west-1, build_height+1, min_z)
                    else:
                        utilityFunctions.setBlock(level, (pallete.chest, 3), x_west-1, build_height, min_z)

            else:
                if no_beds == 2:
                    utilityFunctions.setBlock(level, pallete.int_wood, x_center, build_height, min_z)
                    utilityFunctions.setBlock(level, pallete.torch, x_center, build_height+1, min_z)
                else:
                    utilityFunctions.setBlock(level, (pallete.bed,10), x_center, build_height, min_z)
                    utilityFunctions.setBlock(level, (pallete.bed,2), x_center, build_height, min_z+1)

                utilityFunctions.setBlock(level, (pallete.bed,10), x_center-1, build_height, min_z)
                utilityFunctions.setBlock(level, (pallete.bed,2), x_center-1, build_height, min_z+1)
                utilityFunctions.setBlock(level, (pallete.bed,10), x_center+1, build_height, min_z)
                utilityFunctions.setBlock(level, (pallete.bed,2), x_center+1, build_height, min_z+1)

                if x_center+2 < max_x:
                    if random.randint(0,1):
                        utilityFunctions.setBlock(level, pallete.int_wood, x_center+2, build_height, min_z)
                        utilityFunctions.setBlock(level, pallete.torch, x_center+2, build_height+1, min_z)
                    else:
                        utilityFunctions.setBlock(level, (pallete.chest, 3), x_center+2, build_height, min_z)

                if x_center-2 >= min_x:
                    if random.randint(0,1):
                        utilityFunctions.setBlock(level, pallete.int_wood, x_center-2, build_height, min_z)
                        utilityFunctions.setBlock(level, pallete.torch, x_center-2, build_height+1, min_z)
                    else:
                        utilityFunctions.setBlock(level, (pallete.chest, 3), x_center-2, build_height, min_z)

def build_interior(level, pallete, length_x, height_y, length_z, no_floors):
    built_interiors = []
    mandatory_interiors = ['kitchen', 'bedroom']
    optional_interiors = ['bedroom', 'library'] # TODO: Add more?

    current_floor = 0
    while current_floor < no_floors+1:
        if current_floor == 0: # Hardcode kitchen on the bottom floor
            current_building_interior = 'kitchen'
        else:
            if current_floor == no_floors and 'bedroom' not in built_interiors: # We're on the last floor, and there's no bedroom yet!
                current_building_interior = 'bedroom'
            else: # There's already a bedroom, or we're not on the last floor yet
                current_building_interior = random.choice(optional_interiors)

        build_height = 1+(current_floor*height_y)
        stair_loc = current_floor%2

        if current_floor == 0:
            min_x = 2
            max_x = length_x-1
            min_z = 2
            max_z = length_z-1
        elif current_floor == no_floors:
            min_x = 3
            max_x = length_x-3
            min_z = 2
            max_z = length_z-1
        else:
            min_x = 2
            max_x = length_x-2
            min_z = 1
            max_z = length_z-1
            if stair_loc == 0:
                min_z+=1
            else:
                max_z-=1

        if current_building_interior == 'bedroom':
            build_bedroom(level, pallete, length_x, height_y, length_z, build_height, min_x, max_x, min_z, max_z)
        elif current_building_interior == 'kitchen':
            build_kitchen(level, pallete, length_x, height_y, length_z, build_height, min_x, max_x, min_z, max_z, no_floors+1)
        elif current_building_interior == 'library':
            build_library(level, pallete, length_x, height_y, length_z, build_height, min_x, max_x, min_z, max_z)
        else:
            build_bedroom(level, pallete, length_x, height_y, length_z, build_height, min_x, max_x, min_z, max_z)

        current_floor += 1


# Start of the Generation script
#  @ level: Minecraft world
#  @ box: selected box by mcedit
#  @ options: user defined inputs from mcedit
def build_house(length_x, height_y, length_z, rotations, no_floors, facade_type):
    base_x = 0
    base_y = 1
    base_z = 0

    tot_height = no_floors*height_y + 2*length_x + 1 #/ 2 box too large is not really an issue...
    level = MCSchematic((length_x, tot_height, length_z))#working object
    box = bx.BoundingBox((0,0,0),(length_x, tot_height, length_z))

    pallete = Pallete()

    window_type_1 = random.randint(0, 1) == 1
    ladder = length_z < height_y + 4

    #Walls:
    temp_base_y = base_y
    stair_loc = 0
    for i in range(no_floors):
        if i == no_floors - 1:#top most floor
            build_floor(level, pallete, length_x, height_y, length_z, base_x, temp_base_y, base_z, stair_loc, 1, ladder)
        else:#middel floors
            build_floor(level, pallete, length_x, height_y, length_z, base_x, temp_base_y, base_z, stair_loc, 0, ladder)
        stair_loc += 2
        stair_loc %= 4
        temp_base_y += height_y
    temp_base_y -= height_y - 1

    #floor:
    for x in range (0, length_x):
        for z in range(0, length_z):
            utilityFunctions.setBlock(level, pallete.floor, x, 0, z)

    #roof:
    y_r = build_roof(level, pallete, length_x, height_y, length_z, base_x, temp_base_y, base_z)
    facade(level, pallete, length_x, height_y, length_z, base_x, temp_base_y, base_z, facade_type)

    #door:

    door_z = 0

    if window_type_1:
        if length_x%2 == 0:
            door_loc = random.randint(0, 1)
            if door_loc:
                door_x = base_x + 1
            else:
                door_x = length_x - 2
        else:
            door_x = random.randrange(base_x + 1, base_x+length_x - 1, 2)

    else:
        door_x = math.floor(length_x / 2) if length_x > 6 else length_x - 2

        if length_x % 2 == 0 and length_x > 6:
            rng = random.randint(0,1)
            door_x -= rng

    door_rot = 1 if rotations % 2 == 0 else 3



    #windows:
    if window_type_1:
        w1ndow = not bool((length_x-1)%2) # Determine is windows are divisible by 2, for windows of 1 wide
        w2ndow = not bool((length_x-1)%3) # Determine is windows are divisible by 3, for windows of 2 wide
        if w1ndow and w2ndow:
            wide_windows = random.randint(0, 1)
            if wide_windows:
                n_windows = length_x//2
                window_width = 1
            else:
                n_windows = length_x//3
                window_width = 2

        elif w1ndow and not w2ndow: # Windows can only be one wide
            n_windows = length_x//2
            window_width = 1

        elif w2ndow and not w1ndow: # Windows can only be two wide
            n_windows = length_x//3
            window_width = 2

        else: # Other cases: windows can be neither, we have to improvise :)
            n_windows = length_x//2
            window_width = 1
        windows(level, pallete, length_x, height_y, no_floors, window_width, door_x)

    else:
        ground_floor_windows(level, pallete, length_x, height_y)
        for i in range(1, no_floors):
            offset = height_y * i
            other_floor_windows(level, pallete, length_x, height_y, offset)
    #'''
    #source for door and bed rotations: https://github.com/abrightmoore/ProceduralSettlementsInMinecraft/blob/master/House.py

    utilityFunctions.setBlock(level, (pallete.door, door_rot), door_x, base_y, door_z)
    utilityFunctions.setBlock(level, (pallete.door, door_rot + 8), door_x, base_y + 1, door_z)

    build_interior(level, pallete, length_x, height_y, length_z, no_floors)

    return level, box, [door_x, door_z]

def place_house(og_level, length_x, height_y, length_z, base, rotations, no_floors, facade_type):
    scheme, box, door_coords = build_house(length_x, height_y, length_z, rotations, no_floors, facade_type)

    if rotations % 2 == 0:
        rot_box = bx.BoundingBox((0,0,0),(box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz))
    else:
        rot_box = bx.BoundingBox((0,0,0),(box.maxz-box.minz,box.maxy-box.miny,box.maxx-box.minx))

    for _ in range(rotations):
        scheme.rotateLeft()

    og_level.copyBlocksFrom(scheme, rot_box, base)

    #transform from scheme coords to global coords
    door_coords[0] += base[0]#x
    door_coords[1] += base[2]#z

    return door_coords

def perform(level, box, options):
    height_y = options["height (y)"]
    length_z = options["length (z)"]
    length_x = options["length (x)"]
    base_x = options["offset (x)"]
    base_y = options["offset (y)"]
    base_z = options["offset (z)"]
    rotations = options["door location (N=0, W=1, S=2, E=3)"]
    no_floors = options["number of floors"]
    facade_type = options["facade type (small stairs=0, large stairs=1, bell=2, flat=3)"]

    place_house(level, length_x, height_y, length_z, (base_x, base_y, base_z), rotations, no_floors, facade_type)

	#TODO: windows, roof and facade top (different styles)

	# while loop over windows: every 2 blocks, set as window if not door_x
	# potentially, we could change the height of the windows on ground floor for smaller houses
	# Also, we could generate houses with more width and windows of 2 meters wide
	# If you google for "grachtenpanden minecraft", you'll see some nice examples or inspiration
	# (or demotivation, wow those look nice... How do we even build such a thing?)

	# Roofs: a few different styles, I've written them down on a paper. Those are
	# a few basics. Again, look at "grachtenpanden minecraft for some inspiration".
	# A lot of stuff is done with slabs and stairs that have been rotated upside
	# down. How do we rotate in this program, anyway?

	# Roof: Just use the staircase builder, but wihout the 'meat' of the staircase,
	# that is, wihout the 'support'. Just use the stair blocks from minecraft. The
	# rear of the buildings can be staircases.


    # #door_x = 0
    # #door_z = 0
    # if x_door == 1:
    #     #door in x section
    #     door_z = random.randint(base_z+2, base_z+depth_z-2)
    #     door_x = random.randint(0, 1)
    #     if door_x == 0:
    #         door_x = base_x
    #     else:
    #         door_x = base_x+width_x
    # else:
    #     #door in z section
    #     door_x = random.randint(base_x+2, base_x+width_x-2)
    #     door_z = random.randint(0, 1)
    #     if door_z == 0:
    #         door_z = base_z
    #     else:
    #         door_z = base_z+depth_z
