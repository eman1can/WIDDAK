import random
import math
import RNG
import logging
from pymclevel import alphaMaterials, BoundingBox
import utilityFunctions as utilityFunctions
import BlocksInfo as BlocksInfo
from GenerateCarpet import generateCarpet
from GenerateObject import *

GREENHOUSE_WIDTH = 10
GREENHOUSE_DEPTH = 12
GREENHOUSE_HEIGHT = 5

def generateGreenhouse(matrix, h_min, h_max, x_min, x_max, z_min, z_max, usable_wood, biome):
    greenhouse = utilityFunctions.dotdict()
    greenhouse.type = "greenhouse"
    greenhouse.lotArea = utilityFunctions.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})

    (h_min, h_max, x_min, x_max, z_min, z_max) = getGreenHouseAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max)

    greenhouse.buildArea = utilityFunctions.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})
    greenhouse.orientation = getOrientation()
    door_z = greenhouse.buildArea.z_min
    door_x = greenhouse.buildArea.x_min + GREENHOUSE_WIDTH / 2
    greenhouse.entranceLot = ( greenhouse.lotArea.y_min + 1, door_x, greenhouse.lotArea.z_min)

    logging.info("Generating greenhouse at area {}".format(greenhouse.lotArea))
    logging.info("Construction area {}".format(greenhouse.buildArea))
    utilityFunctions.cleanProperty2(matrix, greenhouse.lotArea.y_min + 1, greenhouse.lotArea.y_max, x_min - 1, x_max + 1, z_min - 1, z_max + 1)
    utilityFunctions.cleanProperty2(matrix, h_min + 1, h_max, door_x - 1, door_x + 1, greenhouse.lotArea.z_min + 1, z_min - 1)

    picked_wood = utilityFunctions.selectRandomWood(usable_wood)
    foundation = BlocksInfo.getGreenhouseFundationId(biome, picked_wood)
    ground = BlocksInfo.getGreenhouseGroundId(biome)
    used_glass = BlocksInfo.getGreenhouseGlassId(biome)
    pavement_block = BlocksInfo.getPavmentId(biome)

    generateGroundAndCropse(matrix, greenhouse.buildArea.y_min,greenhouse.buildArea.x_min, greenhouse.buildArea.x_max, greenhouse.buildArea.z_min, greenhouse.buildArea.z_max, foundation, ground)
    generateGlassDome(matrix, greenhouse.buildArea.y_min + 1, greenhouse.buildArea.y_min + GREENHOUSE_HEIGHT, greenhouse.buildArea.x_min, greenhouse.buildArea.x_max, greenhouse.buildArea.z_min, greenhouse.buildArea.z_max, used_glass)
    generateFront(matrix, greenhouse.buildArea.y_min + 1, greenhouse.buildArea.y_min + GREENHOUSE_HEIGHT, greenhouse.buildArea.x_min, greenhouse.buildArea.x_max, greenhouse.buildArea.z_min, greenhouse.buildArea.z_max, used_glass)

    # entrance path
    for z in range(greenhouse.lotArea.z_min, door_z):
        matrix.setValue(h_min, door_x, z, pavement_block)
        matrix.setValue(h_min, door_x - 1, z, pavement_block)

    return greenhouse

def generateFront(matrix, h_min, h_max, x_min, x_max, z_min, z_max, used_glass):
    for x in range(x_min, x_max + 1):
        for y in range(h_min, h_max + 1):
            if x < x_min + 2 and y - h_min < 2 + (x - x_min):
                addGlass(matrix, y, x, z_min, z_max, used_glass)
            elif x > x_max - 2 and y - h_min < 2 + (x_max - x):
                addGlass(matrix, y, x, z_min, z_max, used_glass)
            elif x == x_min + 2 or x == x_max - 2 :
                if y - h_min < 3 :
                    addGlassSinglePossibility(matrix, y, x, z_min, z_max, BlocksInfo.GLASS_ID)
                elif y - h_min == 3 :
                    addGlass(matrix, y, x, z_min, z_max, used_glass)
            elif x > x_min + 2 and x < x_max - 2:
                if y == h_max :
                    addGlass(matrix, y, x, z_min, z_max, used_glass)
                elif y == h_max - 1 :
                    addGlassSinglePossibility(matrix, y, x, z_min, z_max, BlocksInfo.GLASS_ID)

def addGlass(matrix, y, x, z_min, z_max, glass) :
    matrix.setValue(y, x, z_min, glass[random.randint(0, len(glass) - 1)])
    matrix.setValue(y, x, z_max, glass[random.randint(0, len(glass) - 1)])

def addGlassSinglePossibility(matrix, y, x, z_min, z_max, glass) :
    matrix.setValue(y, x, z_min, glass)
    matrix.setValue(y, x, z_max, glass)

def generateGlassDome(matrix, h_min, h_max, x_min, x_max, z_min, z_max, used_glass):
    for x in range(x_min, x_max+1):
        for y in range(h_min, h_max+1):
            for z in range(z_min+1, z_max):
                if y - h_min == 1 + (x - x_min) or y - h_min == 1 + (x_max - x) :
                    matrix.setValue(y, x, z, used_glass[random.randint(0, len(used_glass) - 1)])
                elif (x == x_min or x == x_max) and y == h_min :
                    matrix.setValue(y, x, z, used_glass[random.randint(0, len(used_glass) - 1)])
                elif x > x_min + 3 and x < x_max - 3 and y == h_max :
                    matrix.setValue(y, x, z, used_glass[random.randint(0, len(used_glass) - 1)])


def generateGroundAndCropse(matrix, h_min, x_min, x_max, z_min, z_max, foundation, ground):
    used_cropse = BlocksInfo.CROPS_ID[RNG.randint(0, len(BlocksInfo.CROPS_ID) - 1)]
    for x in range(x_min, x_max+1):
        for z in range(z_min, z_max+1):
            if x == x_min or x == x_max :
                matrix.setValue(h_min, x, z, foundation)
            elif z == z_min or z == z_max :
                if (x > x_min and x < x_min + 2) or (x < x_max and x > x_max - 2) :
                    matrix.setValue(h_min, x, z, foundation)
                elif x == x_min + 2 or x == x_max - 2 :
                    matrix.setValue(h_min, x, z, BlocksInfo.SEA_LANTERN_ID)
                else :
                    matrix.setValue(h_min, x, z, ground)
            elif x == x_min + 1 or x == x_max - 1 :
                if z == z_min + 3 or z == z_max - 3 :
                    addWaterSource(matrix, h_min, x, z, "W" if x == x_min + 1 else "E")
                else :
                    addFarmlandAndCrops(matrix, h_min, x, z, used_cropse)
            elif x == x_min + 2 or x == x_max - 2 :
                addFarmlandAndCrops(matrix, h_min, x, z, used_cropse)
            elif x == x_min + 3 or x == x_max - 3 :
                matrix.setValue(h_min, x, z, ground)
            else :
                addFarmlandAndCrops(matrix, h_min, x, z, used_cropse)

def addFarmlandAndCrops(matrix, h, x, z, used_cropse) :
    matrix.setValue(h, x, z, BlocksInfo.FARMLAND_ID)
    matrix.setValue(h + 1, x, z, used_cropse)

def addWaterSource(matrix, h, x, z, direction) :
    matrix.setValue(h, x, z, BlocksInfo.WATER_ID)
    #Put a dirt bloc under the water source and a trapdoor above
    matrix.setValue(h - 1, x, z, BlocksInfo.DIRT_ID)
    if direction == "E" :
        matrix.setValue(h + 1, x, z, (BlocksInfo.TRAPDOOR_ID, 2))
    elif direction == "W" :
        matrix.setValue(h + 1, x, z, (BlocksInfo.TRAPDOOR_ID, 3))
    elif direction == "S" :
        matrix.setValue(h + 1, x, z, (BlocksInfo.TRAPDOOR_ID, 0))
    else :
        matrix.setValue(h + 1, x, z, (BlocksInfo.TRAPDOOR_ID, 1))

def getGreenHouseAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max):
    remainder_x = x_max - x_min - GREENHOUSE_WIDTH
    x_min = x_min + (remainder_x / 2)
    x_max = x_max - (remainder_x / 2) - (remainder_x % 2) - 1
    remainder_z = z_max - z_min - GREENHOUSE_DEPTH
    z_min = z_min + (remainder_z / 2)
    z_max = z_max - (remainder_z / 2) - (remainder_z % 2) -1
    assert x_max - x_min == GREENHOUSE_WIDTH - 1
    assert z_max - z_min == GREENHOUSE_DEPTH - 1

    return (h_min, h_max, x_min, x_max, z_min, z_max)

def getOrientation():
    return "N"
