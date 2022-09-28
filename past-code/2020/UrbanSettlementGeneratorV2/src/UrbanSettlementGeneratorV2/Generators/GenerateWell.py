import random
import math
import RNG
import logging
import utilityFunctions as utilityFunctions
import BlocksInfo as BlocksInfo
from GenerateObject import *

WELL_AREA_SIZE = 12
WELL_ENTRANCE_SIZE = 4

def generateWell(matrix, h_min, h_max, x_min, x_max, z_min, z_max, biome) :
    well = utilityFunctions.dotdict()
    well.type = "well"
    well.lotArea = utilityFunctions.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})

    utilityFunctions.cleanProperty(matrix, h_min+1, h_max, x_min, x_max, z_min, z_max)

    (h_min, h_max, x_min, x_max, z_min, z_max) = getWellAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max)

    well.buildArea = utilityFunctions.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})
    well.orientation = getOrientation()

    logging.info("Generating well at area {}".format(well.lotArea))
    logging.info("Construction area {}".format(well.buildArea))

    picked_wood = 'oak'
    fence = BlocksInfo.IRON_BAR_ID
    slab = BlocksInfo.getSlabId(biome, picked_wood, "Lower")
    wall = BlocksInfo.getWellWallId(biome)
    structure_bloc = BlocksInfo.getStructureBlockId(biome, picked_wood)
    pillar = BlocksInfo.getHousePillarId(wall, picked_wood)
    stairs = BlocksInfo.getStairsId(biome, picked_wood)[0]
    pavement_block = BlocksInfo.getPavmentId(biome)

    setGround(matrix, h_min - 1, x_min, x_max, z_min, z_max, structure_bloc)
    generateWall(matrix, h_min, x_min, x_max, z_min, z_max, wall, fence)
    generateCenterPart(matrix, h_min, x_min + 3, x_max - 3, z_min + 3, z_max - 3, slab, structure_bloc, pillar, fence, stairs, wall)

    if well.orientation == "N" :
        generateEntrance(matrix, h_min, x_min + WELL_ENTRANCE_SIZE, x_max - WELL_ENTRANCE_SIZE, z_min, z_min, wall)
        generateBucket(matrix, h_min + 4, x_min + (WELL_AREA_SIZE / 2), z_min + (WELL_AREA_SIZE / 2), 1)
        well.entranceLot = (well.lotArea.y_min + 1, well.buildArea.x_min + (WELL_AREA_SIZE / 2), well.lotArea.z_min)
        door_x = x_min + WELL_ENTRANCE_SIZE
        # entrance path
        for z in range(well.lotArea.z_min, well.buildArea.z_min):
            for i in range(1, WELL_ENTRANCE_SIZE - 1) :
                matrix.setValue(well.lotArea.y_min, door_x + i, z, pavement_block)

    elif well.orientation == "S" :
        generateEntrance(matrix, h_min, x_min + WELL_ENTRANCE_SIZE, x_max - WELL_ENTRANCE_SIZE, z_max, z_max, wall)
        generateBucket(matrix, h_min + 4, x_max - (WELL_AREA_SIZE / 2), z_max - (WELL_AREA_SIZE / 2), 1)
        well.entranceLot = (well.lotArea.y_min + 1, well.buildArea.x_min + (WELL_AREA_SIZE / 2), well.lotArea.z_max)
        door_x = x_min + WELL_ENTRANCE_SIZE
        # entrance path
        for z in range(well.buildArea.z_max + 1, well.lotArea.z_max):
            for i in range(1, WELL_ENTRANCE_SIZE - 1) :
                matrix.setValue(well.lotArea.y_min, door_x + i, z, pavement_block)

    elif well.orientation == "E" :
        generateEntrance(matrix, h_min, x_max, x_max, z_min + WELL_ENTRANCE_SIZE, z_max - WELL_ENTRANCE_SIZE, wall)
        generateBucket(matrix, h_min + 4, x_max - (WELL_AREA_SIZE / 2), z_min + (WELL_AREA_SIZE / 2), 1)
        well.entranceLot = (well.lotArea.y_min + 1, well.lotArea.x_max, well.buildArea.z_min + (WELL_AREA_SIZE / 2))
        door_z = z_min + WELL_ENTRANCE_SIZE
        # entrance path
        for x in range(well.buildArea.x_max + 1, well.lotArea.x_max):
            for i in range(1, WELL_ENTRANCE_SIZE - 1):
                matrix.setValue(well.lotArea.y_min, x, door_z + i, pavement_block)

    else :
        generateEntrance(matrix, h_min, x_min, x_min, z_min + WELL_ENTRANCE_SIZE, z_max - WELL_ENTRANCE_SIZE, wall)
        generateBucket(matrix, h_min + 4, x_min + (WELL_AREA_SIZE / 2), z_max - (WELL_AREA_SIZE / 2), 1)
        well.entranceLot = (well.lotArea.y_min + 1, well.lotArea.x_min, well.buildArea.z_min + (WELL_AREA_SIZE / 2))
        door_z = z_min + WELL_ENTRANCE_SIZE
        # entrance path
        for x in range(well.lotArea.x_min, well.buildArea.x_min):
            for i in range(1, WELL_ENTRANCE_SIZE - 1) :
                matrix.setValue(well.lotArea.y_min, x, door_z + i, pavement_block)

    return well

def getWellAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max):
    remainder_x = x_max - x_min - WELL_AREA_SIZE
    x_min = x_min + (remainder_x / 2)
    x_max = x_max - (remainder_x / 2) - (remainder_x % 2) - 1
    remainder_z = z_max - z_min - WELL_AREA_SIZE
    z_min = z_min + (remainder_z / 2)
    z_max = z_max - (remainder_z / 2) - (remainder_z % 2) - 1
    return (h_min + 1, h_max, x_min, x_max, z_min, z_max)

def getOrientation():
    orientation = ["N", "E", "S", "W"]
    return orientation[random.randint(0, len(orientation) - 1)]

def setGround(matrix, h, x_min, x_max, z_min, z_max, ground_id) :
    for x in range(x_min, x_max + 1) :
        for z in range(z_min, z_max + 1) :
            matrix.setValue(h, x, z, ground_id)

def generateWall(matrix, h, x_min, x_max, z_min, z_max, wall_id, fence_id) :
    for x in range(x_min, x_max + 1) :
        for z in range(z_min, z_max + 1) :
            if x == x_min or x == x_max or z == z_min or z == z_max :
                matrix.setValue(h, x, z, wall_id)
                if (x == x_min or x == x_max) and (z == z_min or z == z_max) :
                    matrix.setValue(h + 1, x, z, wall_id)
                    generateStreetLight(matrix, h + 1, x, z, 0)
                else :
                    matrix.setValue(h + 1, x, z, fence_id)

def generateCenterPart(matrix, h, x_min, x_max, z_min, z_max, slab_id, structure_id, pillar_id, fence_id, stair_id, wall_id) :
    for x in range(x_min, x_max + 1) :
        for z in range(z_min, z_max + 1) :
            if z == z_min or z == z_max :
                if x < x_max - 1 and x > x_min + 1 :
                    matrix.setValue(h, x, z, (stair_id, 2 if z == z_min else 3))
                elif x == x_min + 1 or x == x_max - 1 :
                    matrix.setValue(h, x, z, slab_id)

            elif x == x_min or x == x_max:
                if z < z_max - 1 and z > z_min + 1 :
                    matrix.setValue(h, x, z, (stair_id, 0 if x == x_min else 1))
                elif z == z_max - 1 or z == z_min + 1 :
                    matrix.setValue(h, x, z, slab_id)

            elif x == x_min + 1 or x == x_max - 1 or z == z_max - 1 or z == z_min + 1 :
                matrix.setValue(h, x, z, structure_id)
                if (x == x_min + 1 or x == x_max - 1) and (z == z_min + 1 or z == z_max - 1) :
                    for i in range(1, 4) :
                        matrix.setValue(h + i, x, z, fence_id)
                    else :
                        matrix.setValue(h + i + 1, x, z, pillar_id)
                else :
                    matrix.setValue(h + 4, x, z, wall_id)

            else :
                matrix.setValue(h + 4, x, z, wall_id)
                x_shifting = -1 if x - x_min < 3 else 1
                z_shifting = -1 if z - z_min < 3 else 1
                for i in range(1, 6) :
                    matrix.setValue(h - i, x, z, BlocksInfo.AIR_ID)
                    matrix.setValue(h - i, x + x_shifting, z, structure_id)
                    matrix.setValue(h - i, x, z + z_shifting, structure_id)
                else :
                    matrix.setValue(h - i - 1, x, z, BlocksInfo.WATER_ID)
                    matrix.setValue(h - i - 2, x, z, structure_id)
                    matrix.setValue(h - i - 1, x + x_shifting, z, structure_id)
                    matrix.setValue(h - i - 1, x, z + z_shifting, structure_id)

def generateEntrance(matrix, h, x_min, x_max, z_min, z_max, wall_id):
    for x in range(x_min, x_max + 1):
        for z in range(z_min, z_max + 1) :
            matrix.setValue(h, x, z, BlocksInfo.AIR_ID)
            matrix.setValue(h + 1, x, z, BlocksInfo.AIR_ID)
    if x_min == x_max :
        matrix.setValue(h + 1, x_max, z_min - 1, wall_id)
        matrix.setValue(h + 1, x_max, z_max + 1, wall_id)
    elif z_min == z_max :
        matrix.setValue(h + 1, x_min - 1, z_max, wall_id)
        matrix.setValue(h + 1, x_max + 1, z_max, wall_id)
