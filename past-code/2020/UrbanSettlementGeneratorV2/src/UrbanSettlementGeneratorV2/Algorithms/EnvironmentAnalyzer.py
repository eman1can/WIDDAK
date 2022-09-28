import random
import math
import RNG
import logging
import utilityFunctions as utilityFunctions
import BlocksInfo as BlocksInfo
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox, level

GROUND_ID = [1, 2, 3, 12, 13, 16, 79, 80, 82, 110, 159, 174]
PLANT_ID = [31, 32, 81, 78, 99, 100, 106, 111, 127]
NO_SUB_ID = [99, 100, 106, 127] #block with useless sub_id info
FLUID_ID = [9]

found_wood = {(17, 0): 0, (17, 1): 0, (17, 2): 0, (17, 3): 0, (162, 0): 0, (162, 1): 0}
found_blocks = {}
found_plants = {}

def determinate_usable_wood(level, height_map, x_min, x_max, z_min, z_max) :
    usable_wood = {}
    total_found = 0
    total_ground = 0
    total_water = 0
    biome = ''
    for z in range(z_min, z_max):
        for x in range(x_min, x_max):
            y = height_map[x - x_min][z - z_min]
            block = level.blockAt(x, y, z)
            while not block in GROUND_ID and not block in FLUID_ID :
                if block in BlocksInfo.LOGS_ID :
                    sub_id = level.blockDataAt(x, y, z)
                    if (block == 17 and sub_id > 3) or (block == 162 and sub_id > 1) :
                        sub_id = 0
                    found_wood[(block, sub_id)] += 1
                    total_found += 1
                elif block in PLANT_ID :
                    if block in NO_SUB_ID :
                        block_id = block
                    else :
                        block_id = (block, level.blockDataAt(x, y, z))
                    addToDictionary(found_plants, block_id)
                y = y - 1
                block = level.blockAt(x, y, z)
            if block in GROUND_ID :
                block_id = (level.blockAt(x, y, z), level.blockDataAt(x, y, z))
                addToDictionary(found_blocks, block_id)
                total_ground += 1
            elif block in FLUID_ID :
                total_water += 1
                total_ground += 1

    logging.info("---------------------------------------------")
    logging.info("found wood : oak : {}, spruce {}, birch {}, jungle {}, acacia {}, dark_oak {}".format(found_wood[(17, 0)], found_wood[(17, 1)], found_wood[(17, 2)], found_wood[(17, 3)], found_wood[(162, 0)], found_wood[(162, 1)]))
    logging.info("---------------------------------------------")
    logging.info("block found : {}".format(found_blocks))
    logging.info("---------------------------------------------")
    logging.info("plantes trouves : {}".format(found_plants))
    logging.info("---------------------------------------------")

    if total_found > 0 :
        for key in found_wood.keys():
            percentage = int(round(float(found_wood[key]) / total_found * 100))
            if found_wood[key] > 0 :
                usable_wood[key] = percentage
    else :
        """ Todo add a behavior if no wood """
        usable_wood[(17, 0)] = 100

    biome = identifyBiome(total_ground, total_water, total_found)

    logging.info("usable wood = {}".format(usable_wood))
    logging.info("We are in a {}".format(biome))
    return usable_wood, biome

def identifyBiome(total_ground, total_water, total_found):
    terracotta_count = badlandsTerracottaCount()
    logging.info("Water percentage = {}".format(total_water / float(total_ground)))
    if found_blocks.has_key(BlocksInfo.SAND_ID) or found_blocks.has_key(BlocksInfo.RED_SAND_ID) or terracotta_count > 0:
        red_sand = (found_blocks[BlocksInfo.RED_SAND_ID] if found_blocks.has_key(BlocksInfo.RED_SAND_ID) else 0) + terracotta_count
        sand =  found_blocks[BlocksInfo.SAND_ID] if found_blocks.has_key(BlocksInfo.SAND_ID) else 0
        #logging.info("Sand percentage = {}".format((red_sand + sand) / float(total_ground)))
        if (red_sand + sand) / float(total_ground) > 0.45 :
            ##logging.info("red Sand {} and Sand {}".format(red_sand, sand))
            if red_sand > sand :
                return 'Badlands'
            else :
                if found_plants.has_key(BlocksInfo.DEAD_BUSH_ID) or found_plants.has_key((BlocksInfo.CACTUS_ID, 0)) :
                    return 'Desert'
                elif total_water / float(total_ground) > 0.3 :
                    return 'Beach'
                else :
                    return 'Desert'
    if found_plants.has_key(BlocksInfo.SNOW_ID) :
        if found_blocks.has_key(BlocksInfo.STONE_ID) :
            if found_blocks[BlocksInfo.STONE_ID] / float(total_ground) > 0.22 :
                logging.info("Stone percentage = {}".format(found_blocks[BlocksInfo.STONE_ID] / float(total_ground)))
                return 'Mountains'
        if found_blocks.has_key(BlocksInfo.GRAVEL_ID) :
            if found_blocks[BlocksInfo.GRAVEL_ID] / float(total_ground) > 0.22 :
                return 'Mountains'
        if found_plants[BlocksInfo.SNOW_ID] / float(total_ground) > 0.08 :
            return 'Snowy_zone'
    elif found_blocks.has_key(BlocksInfo.MYCELIUM_ID) :
        if found_blocks[BlocksInfo.MYCELIUM_ID] / float(total_ground) > 0.45 :
            return 'Mushroom_fields'
    if total_water / float(total_ground) > 0.7 :
        return 'Ocean'
    elif found_blocks.has_key(BlocksInfo.STONE_ID) :
        if found_blocks[BlocksInfo.STONE_ID] / float(total_ground) > 0.25 :
            return 'Mountains'
    if found_blocks.has_key(BlocksInfo.ICE_ID) :
        if found_blocks[BlocksInfo.ICE_ID] / float(total_water) > 0.5 :
            return 'Snowy_zone'
    if total_found > 0 :
        if float(found_wood[(162, 1)]) / total_found > 0.5:
            return 'Dark_forest'
        elif float(found_wood[(17, 3)]) / total_found > 0.5 :
            return 'Jungle'
        elif float(found_wood[(162, 0)]) / total_found > 0.3 :
            return 'Savanna'
        elif float(found_wood[(17, 0)] + found_wood[(17, 2)] + found_wood[(17, 1)]) / total_found > 0.7 and not found_plants.has_key(BlocksInfo.VINES_ID) :
            logging.info("base with wood")
            return 'Base'
    #This part is just in order to return something
    if found_plants.has_key(BlocksInfo.VINES_ID) :
        if found_plants.has_key(BlocksInfo.LILY_PAD_ID) or found_plants.has_key(BlocksInfo.RED_MUSHROOM_ID) or found_plants.has_key(BlocksInfo.BROWN_MUSHROOM_ID):
            return 'Swamp'
        elif found_plants.has_key(BlocksInfo.COCOA_ID) :
            return 'Jungle'
    elif found_blocks.has_key(BlocksInfo.COAL_ORE_ID) :
            return 'Mountains'
    elif found_blocks.has_key(MYCELIUM_ID) :
        return 'Mushroom_fields'
    elif found_plants.has_key(BlocksInfo.LILY_PAD_ID) :
        return 'Swamp'
    elif found_plants.has_key(BlocksInfo.COCOA_ID):
        return 'Jungle'
    elif found_plants.has_key(BlocksInfo.SNOW_ID) :
        return 'Snowy_zone'
    elif (found_plants.has_key(BlocksInfo.RED_MUSHROOM_ID) or found_plants.has_key(BlocksInfo.BROWN_MUSHROOM_ID)) and found_wood[(162, 1)] > 0 :
        return 'Dark_forest'
    return 'Base'

def addToDictionary(dictionary, key):
    if dictionary.has_key(key):
        dictionary[key] += 1
    else :
        dictionary[key] = 1

def badlandsTerracottaCount():
    terracotta_count = 0
    for i in range(0, len(BlocksInfo.BADLANDS_TERRACOTTA_ID)):
        terracotta_count += found_blocks[BlocksInfo.BADLANDS_TERRACOTTA_ID[i]] if found_blocks.has_key(BlocksInfo.BADLANDS_TERRACOTTA_ID[i]) else 0
    return terracotta_count
