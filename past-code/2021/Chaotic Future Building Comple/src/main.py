from functools import reduce
from random import choice, randint, random, randrange
from time import perf_counter

import cv2
import numpy as np

import interfaceUtils
from blockRegistry import (getFurnitureRandomClutter, getSimpleRandomClutter)
from mapUtils import (calcGoodHeightmap, cv2SizedWindow, distanceToCenter,
                      fractalnoise, imshowLabels, listWhere, minecraft_colors,
                      noise, normalize, normalizeUInt8)
from worldLoader import WorldSlice

# wow lets go

# step 1 - discovery

# TODO travelling agents / building spot

# stencil = cv2.imread("gdmcStencil.png")
# stencil = cv2.cvtColor(stencil, cv2.COLOR_RGB2GRAY)
# stencil = np.flip(stencil, axis=0)
# w = stencil.shape[0]
# h = stencil.shape[1]
# cv2.imshow("stencil", stencil)
# cv2.waitKey(1000)
# cv2.destroyAllWindows()


time0 = perf_counter()

## basic setup ##
# for testing
AROUND_PLAYER = False

w = 96
h = 103
if AROUND_PLAYER:
    interfaceUtils.runCommand(f"execute at @p run setbuildarea ~-{int(w/2)} 0 ~-{int(h/2)} ~{int(w/2)} 256 ~{int(h/2)}")

# 2D build area
x1, y1, z1, x2, y2, z2 = interfaceUtils.requestBuildArea()
w = min(abs(x2 - x1), 196)
h = min(abs(z2 - z1), 196)
centerX = (x1 + x2) // 2
centerZ = (z1 + z2) // 2
area = (centerX - w//2, centerZ - h//2, w, h)
x1 = area[0]
z1 = area[1]
x2 = area[0] + area[2]
z2 = area[1] + area[3]

# step 2 - analysis

interfaceUtils.setBuffering(True)
def recalcSlice():
    global worldSlice, hmTrees, hmOceanFloor, heightmap

    worldSlice = WorldSlice(x1, z1, x2, z2, ["MOTION_BLOCKING_NO_LEAVES", "WORLD_SURFACE", "OCEAN_FLOOR"])

    hmTrees = worldSlice.heightmaps["WORLD_SURFACE"]
    hmOceanFloor = worldSlice.heightmaps["OCEAN_FLOOR"]

    heightmap = calcGoodHeightmap(worldSlice)
    heightmap = heightmap.astype(np.uint8)

recalcSlice()

# step 3 - construction
rng = np.random.default_rng()

# basic bounds of the settlement
maxHeight = 150
minHeight = heightmap.min() - 8
shape2d = (area[2], area[3])
shape3d = (area[2], maxHeight-minHeight, area[3])


## Ground Prep ##
# use noise to determine the basic shape of the city
largenoise = normalize(fractalnoise(shape2d, -5, -2))
distToCenter = distanceToCenter(shape2d)
cutoff = np.percentile(largenoise, 70) #random.randint(50, 75))
endheight = int(np.median(heightmap) - 4)

# forbiddenMap =  np.zeros(shape2d, dtype=np.uint8)
# forbiddenMap = (stencil > 128).astype(np.uint8)
forbiddenMap = ((largenoise > cutoff) | (distToCenter > 0.45)).astype(np.uint8) 

flattenedHM = cv2.medianBlur(heightmap, 5)
difference = (flattenedHM.astype(int) - heightmap)

fill = np.where((difference > 0) & (difference < 6))
bridge = np.where((difference > 0) & (difference >= 6))
cut = np.where(difference < 0)

strctElmt = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
chasm = cv2.erode(forbiddenMap, strctElmt)
pave = np.where((forbiddenMap > 0) & (chasm == 0))

TERRAFORM = True

# input("wait...")

if TERRAFORM:
    strctElmt = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
    forbMapEroded = cv2.erode(forbiddenMap.astype(np.uint8), strctElmt)
    cutTrees = np.where((hmTrees > heightmap) & (~forbiddenMap))

    # cut trees
    for p in zip(*cutTrees):
        for y in range(hmTrees[p] - 1, heightmap[p] - 1, -1):
            interfaceUtils.setBlock(p[0] + area[0], y, p[1] + area[1], "air")
    # fill
    for p in zip(*fill):
        for y in range(heightmap[p], flattenedHM[p]):
            interfaceUtils.setBlock(p[0] + area[0], y, p[1] + area[1], "dirt")
    # bridge
    for p in zip(*bridge):
        interfaceUtils.setBlock(p[0] + area[0], flattenedHM[p] - 1, p[1] + area[1], "light_gray_concrete")
    # cut
    for p in zip(*cut):
        for y in range(heightmap[p] - 1, flattenedHM[p] - 1, -1):
            interfaceUtils.setBlock(p[0] + area[0], y, p[1] + area[1], "air")
    # pave
    for p in zip(*pave):
        axis = choice(["x", "z"])
        interfaceUtils.setBlock(p[0] + area[0], flattenedHM[p]-1, p[1] + area[1], f"polished_basalt[axis={axis}]")

    # chasm
    # TODO line walls of chasm
    # for p in zip(*np.where(chasm > 0)):
    #     for y in range(flattenedHM[p] + 1, endheight, -1):
    #         interfaceUtils.setBlock(area[0] + p[0], y, area[1] + p[1], "air")

    interfaceUtils.sendBlocks()

    # player teleport
    # cmd = f"tp @p {elevatorPos[0] + area[0]} {flattenedHM[elevatorPos]+1} {elevatorPos[1] + area[1]}"
    # print(f"command: {cmd}")
    # print(interfaceUtils.runCommand(cmd))

recalcSlice()

# input("wait...")

originalHeightmap = np.array(heightmap)

## Drop Boxes Algorithm ##

boxSidesShort = [7, 8, 9, 10, 11]
boxSidesLong = [14,16]

boxes = []

buildingsOnlyHeightmap = np.zeros(shape2d, dtype=np.uint8)
modifiedHeightmap = heightmap[:]

borderMap = np.zeros(shape2d, dtype=np.uint8)
cv2.rectangle(borderMap, (0, 0), (area[3]-1, area[2]-1), (1), 3)

# block cache is 0 or one of these labels...

# cache labels
lcPlatform = 1
lcBuilding = 2
lcBuildingFoundation = 3
lcPillar = 4
lcStairs = 5
lcKeepFree = 6
lcDoorstep = 7
lcDoor = 8
lcNoAccessFoundation = 9

blockCache = np.zeros(shape3d, dtype=np.uint8)

# box ids map 
# 3d map describing ground floors of boxes
# value is id of box
boxIDMap = np.zeros(shape3d, dtype=int)

maxBoxWidth = (area[2] - 3, area[3] - 3)

BUILD = True
COLOR = False
USE_PROXIMITY_HEURISTICS = False

buildingsPerSquareMeter = 0.014

buildingCount = int((w * h) * buildingsPerSquareMeter)

boxID = 0
# place n boxes
for i in range(buildingCount):
    # determine box size first
    # dim1 = randint(7,11)
    # dim2 = randint(7,11) * randint(1,2)
    dim1 = choice(boxSidesShort)
    dim2 = choice(choice([boxSidesShort,boxSidesLong]))

    # randomly flip long/short
    if random() < 0.5:
        tmp = dim1
        dim2 = dim1
        dim1 = tmp

    # box size
    sx = min(dim1, maxBoxWidth[0])
    sz = min(dim2, maxBoxWidth[1])
    sy = randint(1, 1) * 6 # 1, 2 or 3 floors high 
    
    # round heightmap down up to 2 blocks to ensure we only build in 3-high 'floors'
    heightmap = heightmap - heightmap%3

    # center offset of box
    offset = (int(sx/2), int(sz/2))
    
    # gap between neighboring buildings
    gap = randrange(1,3)
    if random() < .8:
        gap = 0

    # use the footprint of the box as a dilation kernel to find valid places to build
    strctFootprint = cv2.getStructuringElement(cv2.MORPH_RECT, (sz + 2*gap, sx + 2*gap))
    anchor = (offset[1] + gap, offset[0] + gap)

    dilatedBuildingsHeightmap = cv2.dilate(buildingsOnlyHeightmap, strctFootprint, anchor=anchor)
    dilatedBorderMap = cv2.dilate(borderMap, strctFootprint, anchor=anchor)
    dilatedHeightmap = cv2.dilate(heightmap, strctFootprint, anchor=anchor)
    dilatedForbiddenMap = cv2.dilate(forbiddenMap, strctFootprint, anchor=anchor)

    # rank building positions by their y value
    # TODO how do I build right now, why is there sometimes no space?
    desiredBuildPosMap = (dilatedBuildingsHeightmap == buildingsOnlyHeightmap) * (dilatedForbiddenMap == 0) * (dilatedBorderMap == 0)
    if USE_PROXIMITY_HEURISTICS:
        desiredBuildPosMap = desiredBuildPosMap * (255-dilatedHeightmap)

    maxi = desiredBuildPosMap.max()
    if maxi == 0:
        print("No space found to build!!! just skipping this step and going on as if nothing happened....")
        continue

    # get valid building positions as list
    buildPositions = listWhere(desiredBuildPosMap == maxi)

    lastBoxPos = (boxes[-1][0], boxes[-1][1], boxes[-1][2]) if len(boxes) > 0 else (int(area[2]/2), 0, int(area[3]/2))
    # helper function to build close to last placed box
    distSquared = lambda p1: (p1[0] - lastBoxPos[0])**2 + (dilatedHeightmap[p1] - lastBoxPos[2])**2 * 100 + (p1[1] - lastBoxPos[2])**2

    if len(buildPositions) > 0:
        if USE_PROXIMITY_HEURISTICS or random() < 0.5:
            p = reduce(lambda a,b : a if distSquared(a) < distSquared(b) else b, buildPositions)
        else:
            p = choice(buildPositions)
    else:
        # no valid positions are found
        print("WARNING: This point should never be reached")
        continue
    
    # dx, dz is the position of the box
    dx = p[0]
    dz = p[1]

    # cx, cz is the position of the corner of the box (lowest x, lowest z)
    cx = p[0] - offset[0]
    cz = p[1] - offset[1]
    
    # y position is sampled at dx, dz
    # since we did the dilation with the right kernel, it is guranteed that we 
    # can build here without obstructions (unless we didn't find any)
    y = dilatedHeightmap[dx, dz]

    # randomly turn it into a platform (only in the lower half of the settlement)
    # if random() < .2 and y - minHeight < maxHeight/2 :
    #     y = y + sy - 1
    #     sy = 1

    # check if we ran out of vertical space
    if y + sy >= maxHeight:
        continue

    # remember box for later
    boxes.append([dx, y, dz, sx, sy, sz, cx, cz]) # local space! center pos

    # x,y,z are corner pos
    x = area[0] + cx
    z = area[1] + cz

    print(f"build cube at {(x, y, z)}")

    # build pillars to support the box
    for rx in range(2):
        for rz in range(2):
            xx = cx + (sx - 1) * rx
            zz = cz + (sz - 1) * rz
            yFloor = hmOceanFloor[xx, zz]
            for yy in range(yFloor, y):
                if BUILD:
                    interfaceUtils.setBlock(area[0] + xx, yy, area[1] + zz, "gray_concrete")

            # update block cache
            blockCache[xx, (yFloor-minHeight):(y-minHeight), zz] = lcPillar

    # build the box
    if BUILD:
        col = None if COLOR else "gray_concrete"
        # interfaceUtils.buildHollowCube(x, y, z, sx, sy, sz, None if COLOR else "gray_concrete")
        interfaceUtils.buildWireCube(x, y-1, z, sx, sy, sz, col)
        # interfaceUtils.buildHollowCube(x, y+sy-1, z, sx, 1, sz, col)
        # interfaceUtils.buildHollowCube(x, y, z, sx, 1, sz, col)

    # update heightmaps
    bheight = y + sy
    heightmap[cx:cx+sx, cz:cz+sz] = bheight
    hmOceanFloor[cx:cx+sx, cz:cz+sz] = bheight
    buildingsOnlyHeightmap[cx:cx+sx, cz:cz+sz] = bheight

    modifiedHeightmap[cx:cx+sx, cz:cz+sz] = y - 2

    # update block cache and id map
    dy = y - minHeight
    # mark as obstructed
    blockCache[cx:cx+sx, dy-1:dy, cz:cz+sz] = lcPlatform # sneaky 'below' platform
    blockCache[cx:cx+sx, dy:dy+1, cz:cz+sz] = lcBuildingFoundation # roof -> platform
    blockCache[cx:cx+sx, dy+1:dy+sy-1, cz:cz+sz] = lcBuilding
    blockCache[cx:cx+sx, dy+sy-1:dy+sy, cz:cz+sz] = lcPlatform # roof -> platform
    # remember box with id
    boxIDMap[cx:cx+sx, dy:dy+sy, cz:cz+sz] = boxID    # only floor -> [cx:cx+sx, y+sy-minHeight-1, cz:cz+sz]

    boxID += 1

    # visualization
    
    img = buildingsOnlyHeightmap + dilatedBuildingsHeightmap
    img[cx, cz] = 230
    img[cx+sx, cz] = 230
    img[cx, cz+sz] = 230
    img[cx+sx, cz+sz] = 230
    img[dx, dz] = 230
    img = cv2.resize(img, (img.shape[1] * 4, img.shape[0] * 4), interpolation=cv2.INTER_NEAREST)
    cv2.imshow("img", img)
    # cv2.waitKey(0 if i == 0 else 1)
    cv2.waitKey(1)

interfaceUtils.sendBlocks()

# clear some extra land
for pos in zip(*np.where(modifiedHeightmap < originalHeightmap)):
    for y in range(originalHeightmap[pos], modifiedHeightmap[pos], -1):
        interfaceUtils.setBlock(area[0] + pos[0], y, area[1] + pos[1], "air")


# 2nd pass -> traversability

# interfaceUtils.setBuffering(False)

# debug / visualization windows
cv2SizedWindow("slices", shape2d)
# cv2SizedWindow("lastLayer", shape2d)
cv2SizedWindow("bCache", shape2d)
cv2SizedWindow("hMap", shape2d)

## Slices Bottom -> Top ##

dilSize = 10 # dilation size used to connect platforms
walkwayWidth = 4 # minimum width of the walkways

# create some structuring elements (kernels)
kSize = dilSize * 2 + 1
strctBigCirc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kSize,kSize))
strctCross = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
strctRect = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))

traversible = (blockCache == 0)

pass1Heightmap = heightmap # remember old heightmap
heightmap = np.array(originalHeightmap) # and start with the original

lastLayer = np.zeros((3, area[2], area[3]), np.uint8)
lastLayerY = -1

stairs = np.zeros(shape2d, dtype=np.uint8)
platformCache = np.zeros(shape3d, dtype=np.uint8)

for i in range(maxHeight - minHeight):
    # pathway maps
    if i > 0 and i < maxHeight - minHeight - 1:
        free = traversible[:,i,:] & traversible[:,i+1,:]
        blocked = ~free
        ground = ~traversible[:,i-1,:] & free
        y = minHeight + i

        # platforms
        platform0 = ground.astype(np.uint8)

        padWidth = dilSize + 1
        platform1 = np.pad(platform0, (padWidth, padWidth), mode='constant') 
        platform1 = cv2.dilate(platform1, strctBigCirc)
        platform1 = cv2.erode(platform1, strctCross, iterations=dilSize)
        platform1 = platform1[padWidth:-padWidth, padWidth:-padWidth]

        platform2 = np.where(pass1Heightmap != y, platform0, 0) 
        platform2 = cv2.dilate(platform2, strctCross, iterations=walkwayWidth)

        floor = cv2.bitwise_or(platform1, platform2)

        # TODO
        # get rid of 1-wide artifacts
        # platform = cv2.filter2D(...)

        # TODO visualize

        platformCache[:,i,:] = floor[:,:]

        # calc space under platform
        diffToHM = np.maximum(0, y - heightmap - 1) * floor
        diffToHM = cv2.bitwise_and(diffToHM, 0b01111111) # fix underflows

        # prep platform for build and update blockCache
        floor = (free & ~ground) * floor
        blockCache[:,i-1,:] = np.where(floor > 0, lcPlatform, blockCache[:,i-1,:])
        
        # update heightmap according to last 2 layers of block cache
        heightmap = np.where(blockCache[:,i-1,:] > 0, y-1, heightmap)
        heightmap = np.where(blockCache[:,i,:] > 0, y, heightmap)

        cv2.imshow("hMap", heightmap) 

        # visualize
        r = blocked.astype(np.uint8) * 128 + normalizeUInt8(blockCache[:,i,:]) // 2
        g = ground.astype(np.uint8) * 255 
        b = floor.astype(np.uint8) * int(255 / walkwayWidth)
        # b = (originalHeightmap > i + minHeight).astype(np.uint8) * 255

        bgr = cv2.merge((b, g, r))

        # show boxes
        for b in filter(lambda box: box[1] == y, boxes):
            bgr[b[0], b[2], :] = (130, 250, 250)


        cv2.imshow("slices", bgr)
        # llimg = cv2.cvtColor(np.transpose(lastLayer, [1,2,0]) * 255, cv2.COLOR_RGB2BGR)
        # cv2.imshow("lastLayer", llimg)
        # cv2.waitKey(0 if i==1 else 1)
        # cv2.waitKey(0)
        cv2.waitKey(1)

        # build layer if necessary
        if floor.max() > 0:
            buildPositions = np.where(floor > 0)
            foundation = np.where(diffToHM > 1, 0, diffToHM)
            y = minHeight + i
            for p in zip(*buildPositions):
                x = area[0] + p[0]
                z = area[1] + p[1]
                for yy in range(y-foundation[p]-1, y):
                    if BUILD:
                        interfaceUtils.setBlock(x, yy, z, "gray_concrete")

            # TODO I think I can remove this?
            lastLayerY = y # TODO kindaweird
            lastLayer[0,:,:] = blocked.astype(np.uint8)
            lastLayer[1,:,:] = ground.astype(np.uint8)
            lastLayer[2,:,:] = floor
        interfaceUtils.sendBlocks()

cv2.destroyAllWindows()


# TODO could probably rewrite this without the for loop
def traversibilityCheck(array, i, n):
    # check traversability
    for k in range(0, n):
        if i <= maxHeight - minHeight - 1 - k:
            array *= np.isin(blockCache[:,i+k,:], [0, lcKeepFree, lcDoor])

    return array

cv2SizedWindow("stairs", shape2d)
cv2SizedWindow("outline", shape2d)
cv2SizedWindow("labels", shape2d)

# funky kernel
strctBranch = np.array([[0,0,1,0,0],[0,0,0,0,0],[1,0,0,0,1],[0,0,0,0,0],[0,0,1,0,0]], dtype=np.uint8)

## Slices Top -> Bottom ##

for i in range(maxHeight - minHeight - 1, 0, -1):
    y = minHeight + i

    # stairs move operation
    stairsCount, stairsLabels = cv2.connectedComponents(stairs, connectivity=4)
    stairsLabels = stairsLabels.astype(np.uint8)
    stairsLabelsCandidates = stairsLabels
    stairsLabelsCandidates = cv2.erode(stairsLabelsCandidates, strctCross)
    stairsLabelsCandidates = cv2.dilate(stairsLabelsCandidates, strctBranch)
    stairsLabelsCandidates *= (blockCache[:,i,:] == 0)
    stairsLabelsCandidates = cv2.dilate(stairsLabelsCandidates, strctCross)
    stairsLabelsCandidates *= (cv2.dilate(stairsLabels, strctCross) - stairsLabels) > 0
    
    # check traversability
    stairsLabelsCandidates = traversibilityCheck(stairsLabelsCandidates, i, 5)

    stairsLabelsCandidatesAlt = stairsLabelsCandidates
    stairsLabelsCandidates = np.where((blockCache[:,i,:] == 0) & (blockCache[:,i-1,:] == 0), stairsLabelsCandidates, 0)
    
    blockCacheWalls = np.isin(blockCache[:,i,:], [lcPlatform, lcBuilding, lcBuildingFoundation]).astype(np.uint8)
    blockCacheWalls = cv2.dilate(blockCacheWalls, strctCross, iterations=1)
    stairsLabelsCandidatesPreferred = (blockCacheWalls != 0) * stairsLabelsCandidates

    blockCacheWalls = (blockCache[:,i,:] != 0).astype(np.uint8)
    blockCacheWalls = cv2.dilate(blockCacheWalls, strctCross, iterations=2)
    stairsLabelsCandidatesSlightlyLessPreferred = (blockCacheWalls != 0) * stairsLabelsCandidates

    stairs *= 0

    for j in range(1, stairsCount):
        buildPositions = listWhere(stairsLabelsCandidatesPreferred == j)
        lvl = 1
        if len(buildPositions) == 0:
            buildPositions = listWhere(stairsLabelsCandidatesSlightlyLessPreferred == j)
            lvl = 2
        if len(buildPositions) == 0:
            buildPositions = listWhere(stairsLabelsCandidates == j)
            lvl = 3
        if len(buildPositions) == 0:
            buildPositions = listWhere(stairsLabelsCandidatesAlt == j)
            lvl = 4
        if len(buildPositions) > 0:
            pos = buildPositions[randrange(len(buildPositions))]
            flippedPos = np.flip(pos) # opencv / numpy coordinate disagreemets
            stairs = cv2.rectangle(stairs, tuple(flippedPos - 1), tuple(flippedPos + 1), lvl, -1)

            # build support pillar
            if i % 3 == 0:
                yFloor = hmOceanFloor[tuple(pos)]
                for yy in range(yFloor, y):
                    if BUILD:
                        interfaceUtils.setBlock(area[0] + pos[0], yy, area[1] + pos[1], "gray_concrete")

                # update block cache
                blockCache[pos[0], (yFloor-minHeight):(y-minHeight), pos[1]] = lcPillar

    # new staircase spawns
    if i+1 > maxHeight - minHeight - 1:
        floor = np.zeros(shape2d, dtype=np.uint8)
    else:
        floor = platformCache[:,i+1,:] 
        floor = traversibilityCheck(floor, i+1, 2) # TODO keep an eye on this, maye last arg needs to be 3

    platformCount, labels = cv2.connectedComponents(floor, connectivity=4)
    # print(f"platformCount={platformCount}, labels={labels}, stats={stats}, centroids={centroids}")
    
    stairstepShape = (3,3)
    strctElmt = cv2.getStructuringElement(cv2.MORPH_RECT, stairstepShape)

    # find if platform already connects to stairs
    overlaps = np.where(cv2.dilate(stairs, strctCross) > 0, labels, 0)

    labels = labels.astype(np.uint8)
    labels = cv2.dilate(labels, strctElmt)
    outline = cv2.dilate(labels, strctCross) - labels
    outline = outline * (blockCache[:,i,:] == 0)
    
    outline = traversibilityCheck(outline, i, 3)
    
    cv2.imshow("stairs", normalizeUInt8(stairs))
    cv2.imshow("outline", normalizeUInt8(outline))
    imshowLabels("labels", labels)

    # cv2.waitKey(1 if labels.max() == 0 else 0)
    cv2.waitKey(1)

    for j in range(1,platformCount):
        if not j in overlaps:
            buildPositions = listWhere(outline == j)
            if len(buildPositions) > 0:
                pos = buildPositions[randrange(len(buildPositions))]
                pos = np.flip(pos)

                print(f"start stairs at {pos[0] + area[0]}, {pos[1] + area[1]}")
                stairs = cv2.rectangle(stairs, tuple(pos - 1), tuple(pos + 1), 1, -1)

    blockCache[:,i,:] = np.where((stairs > 0) & (blockCache[:,i,:] == 0), lcStairs, blockCache[:,i,:])
            
    # build stairs
    buildPositions = np.where(stairs > 0)
    for p in zip(*buildPositions):
        x = area[0] + p[0]
        z = area[1] + p[1]
        blockID = "gray_concrete" if stairs[tuple(p)] == 1 else "cyan_terracotta"
        if BUILD:
            interfaceUtils.setBlock(x, y, z, blockID)
    interfaceUtils.sendBlocks()

    cv2.waitKey(1)
        

cv2.destroyAllWindows()
interfaceUtils.sendBlocks()


# mark spaces as 'keep free'
for i in range(maxHeight - minHeight - 2):
    walkSpace = np.isin(blockCache[:,i,:], [lcPlatform, lcStairs])
    for k in range(1,3):
        blockCache[:,i+k,:] = np.where(walkSpace & (blockCache[:,i+k,:] == 0), lcKeepFree, blockCache[:,i+k,:])

cv2SizedWindow("railings", shape2d)
cv2SizedWindow("bCache", shape2d)
cv2SizedWindow("layer", shape2d)
cv2SizedWindow("grate_direction", shape2d)

## Pseudo-CA Bottom -> Top
# labels:
lGround = 1
lTopsoil = 2
# lPaved = 3
lPlatform = 4
lIndoorFeet = 5
lOutdoorFeet = 6
lIndoorHead = 7
lOutdoorHead = 8
lIndoorAir = 9
lIndoorFloor = 10
lRailingFloor = 11
lRailingFeet = 12
lRailingHead = 13
lWall = 14
lLamp = 15
lPlatformCovered = 16
lDoorstep = 17
lClear = 18
lIndoorAir2 = 19
lIndoorCeiling = 20
lLampSocket = 21
lGrateSide = 22
lSlabCover = 23

airLayers = [lIndoorHead, lOutdoorHead, lIndoorAir, lRailingHead, lIndoorFeet, lOutdoorFeet, lClear]

# magicPattern = np.array([[0,0,0,1],[0,1,0,0],[0,0,1,0],[1,0,0,0]], dtype=np.uint8)
magicPattern = np.array([[1,0,0,0,0,0],
                         [0,0,0,0,1,0],
                         [0,1,0,0,0,0],
                         [0,0,0,1,0,0],
                         [0,0,0,0,0,1],
                         [0,0,1,0,0,0]], dtype=np.uint8)
magicPatternTiled = np.tile(magicPattern, np.array(shape2d)//np.array(np.shape(magicPattern)) + 1)[tuple(map(slice, shape2d))]

# lampPattern = np.array([[0,0,1,0,0],[0,0,0,0,0],[1,0,0,0,1],[0,0,0,0,0],[0,0,1,0,0],], dtype=np.uint8)
lampPattern = np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,0],], dtype=np.uint8)
lampPatternTiled = np.tile(lampPattern, np.array(shape2d)//np.array(np.shape(lampPattern)) + 1)[tuple(map(slice, shape2d))]


def buildByCondition(condition, y, blockID):
    buildPositions = np.where(condition)
    for p in zip(*buildPositions):
        x = area[0] + p[0]
        z = area[1] + p[1]
        if BUILD:
            interfaceUtils.setBlock(x, y, z, blockID)
    interfaceUtils.sendBlocks()

CARDINALS = ["east", "south", "north", "west"]

def buildByConditionRotated(condition, rotation, y, blockID, additionalState=""):
    buildPositions = np.where(condition)
    for p in zip(*buildPositions):
        x = area[0] + p[0]
        z = area[1] + p[1]
        r = int(rotation[p]) % 4
        card = CARDINALS[r]
        bID = f"{blockID}[facing={card}{additionalState}]"
        if BUILD:
            interfaceUtils.setBlock(x, y, z, bID)
    interfaceUtils.sendBlocks()

layer = np.ones(shape2d, dtype=np.uint8) * 0

hmNew = np.minimum(originalHeightmap, hmOceanFloor)

# simplify block cache
origKeepFree = (blockCache == lcKeepFree)
blockCache = np.where(blockCache == lcKeepFree, 0, blockCache)
# TODO I could have a sort of 'category cache' here to simplify some checks later

# input("wait...")

numberOfLamps = 0
layerCache = np.zeros(shape3d, dtype=np.uint8)

for i in range(0, maxHeight - minHeight - 1):
    y = minHeight + i

    prevLayer = layer
    bCache = blockCache[:,i,:]
    bCachePlus1 = blockCache[:,i+1,:]

    bCachePlus4 = blockCache[:,i+4,:] if i+4 < maxHeight - minHeight else np.ones(shape2d, dtype=np.uint8) * 0

    rndNoise = noise(shape2d, shape2d)

    layer = np.zeros(shape2d)

    layer = np.where((bCache == lcPlatform) & (bCachePlus1 == 0), lPlatform, layer)
    layer = np.where((bCache == lcPlatform) & (bCachePlus1 != 0), lPlatformCovered, layer)

    layer = np.where((prevLayer == lPlatform) & (bCache == 0), lOutdoorFeet, layer)
    layer = np.where((prevLayer == lOutdoorFeet) & (bCache == 0), lOutdoorHead, layer)

    # layer = np.where(bCache == lcBuildingFoundation, lIndoorFloor, layer)
    # layer = np.where(prevLayer == lIndoorFloor, lIndoorFeet, layer)
    # layer = np.where((bCache == lcPlatform) & (bCachePlus1 == lcBuildingFoundation) & (bCachePlus1 == 0), lIndoorFloor, layer)
    # layer = np.where((bCache == lcBuildingFoundation) & (bCachePlus1 == 0), lIndoorFeet, layer)
    # TODO this is not always true, e.g. for pillars and staircases
    indoors = cv2.erode(((prevLayer == lPlatformCovered) & (bCache == lcBuildingFoundation)).astype(np.uint8), strctCross)
    layer = np.where(indoors > 0, lIndoorFeet, layer)
    layer = np.where(prevLayer == lIndoorFeet, lIndoorHead, layer)
    layer = np.where(prevLayer == lIndoorHead, lIndoorAir, layer)

    layer = np.where((prevLayer == lIndoorAir), lIndoorAir2, layer)

    layer = np.where((prevLayer == lIndoorAir2) & (lampPatternTiled > 0), lLamp, layer)
    layer = np.where((prevLayer == lIndoorAir2) & (layer != lLamp), lIndoorCeiling, layer)

    layer = np.where(bCache == lcDoorstep, lDoorstep, layer)

    building = (np.isin(bCache, [lcBuilding, lcBuildingFoundation, lcDoor, lcDoorstep])).astype(np.uint8)
    walls = building - cv2.erode(building, strctRect)
    layer = np.where((walls > 0) & np.isin(bCache, [lcBuilding, lcBuildingFoundation]), lWall, layer)

    # floor = np.isin(layer, [lIndoorFloor, lPlatform]).astype(np.uint8)
    # floor = (bCache == lcPlatform).astype(np.uint8)
    floor = (layer == lPlatform).astype(np.uint8)
    railing = cv2.dilate(floor, strctRect) - floor
    obstructed = (bCachePlus1 != 0) & (bCache != 0)
    obstructed = obstructed.astype(np.uint8)
    # obstructed = cv2.dilate(obstructed.astype(np.uint8), strctRect)
    railing = railing * (1-obstructed)

    layer = np.where((railing > 0) & (~origKeepFree[:,i,:]), lRailingFloor, layer)
    layer = np.where((prevLayer == lRailingFloor) & (bCache == 0) & (~origKeepFree[:,i,:]), lRailingFeet, layer)
    layer = np.where((prevLayer == lRailingFeet) & (bCache == 0) & (~origKeepFree[:,i,:]), lRailingHead, layer)

    layer = np.where((magicPatternTiled > 0) & (prevLayer == lRailingFloor) & (~origKeepFree[:,i,:]), lLamp, layer)

    # dilatedFloor = cv2.dilate((layer == lIndoorFloor).astype(np.uint8), strctRect)
    outFeetDilated = cv2.dilate((layer == lOutdoorFeet).astype(np.uint8), strctCross)
    lampPotential = (layer == lWall) & (outFeetDilated > 0)
    layer = np.where((lampPotential > 0) & (magicPatternTiled > 0), lLamp, layer)
    # layer = np.where((lampPotential), lLamp, layer)

    # TODO maybe modify block cache to fit labels

    # lamp covers
    isLamp = (layer == lLamp).astype(np.uint8)
    lampDilated = cv2.dilate(isLamp, strctCross)
    grateDirection = cv2.filter2D(isLamp, cv2.CV_16S, np.array([[0,1,0],[2,0,3],[0,4,0]])) - 1
    imshowLabels("grate_direction", grateDirection)
    layer = np.where((lampDilated > 0) & np.isin(layer, airLayers + [0]) & (bCache == 0), lGrateSide, layer)

    layer = np.where((prevLayer == lLamp) & np.isin(layer, airLayers + [0]) & (bCache == 0), lSlabCover, layer)
    
    cv2.imshow("railings", railing * 255) 
    # cv2.imshow("bCache", (normalize(bCache) * 255).astype(np.uint8)) 
    imshowLabels("bCache", bCache)
    imshowLabels("layer", layer)
    # cv2.waitKey(0 if i==1 else 1)
    cv2.waitKey(1)

    numberOfLamps += np.count_nonzero(layer == lLamp)
    layerCache[:,i,:] = layer

    # build
    if BUILD:
        buildByCondition((layer == lTopsoil) & (rndNoise < 0.05), y, "blackstone")
        buildByCondition(layer == lPlatform, y, "blue_terracotta")
        buildByCondition(layer == lPlatformCovered, y, "cyan_terracotta")
        # buildByCondition((layer == lPlatform) & (y+1 != pass1Heightmap), y, "blue_terracotta")
        # buildByCondition((layer == lPlatform) & (y+1 == pass1Heightmap), y, "grass_block")
        buildByCondition((layer == lOutdoorFeet) & (rndNoise < 0.25) , y, "gray_carpet")
        # buildByCondition((layer == lIndoorFeet) & (rndNoise < 0.25), y, "white_carpet")
        # buildByCondition(layer == lOutdoorHead, y, "air")
        # buildByCondition(layer == lIndoorAir, y, "air")
        # buildByCondition(layer == lRailingHead, y, "air")
        buildByCondition(layer == lIndoorFloor, y, "gray_concrete")
        buildByCondition(layer == lRailingFloor, y, "crimson_slab[type=top]")
        buildByCondition(layer == lRailingFeet, y, "polished_blackstone_wall")
        buildByCondition(layer == lWall, y, "gray_concrete")
        buildByCondition(layer == lLamp, y, "sea_lantern")
        buildByCondition((layer == lLamp) & (prevLayer == lIndoorAir2), y-1, "crimson_trapdoor[half=top,open=false]")
        buildByCondition(layer == lIndoorCeiling, y, "polished_blackstone_slab[type=top]")
        buildByCondition(layer == lLampSocket, y, "polished_blackstone")
        buildByCondition(layer == lDoorstep, y, "polished_blackstone")
        buildByCondition(np.isin(layer, [lIndoorHead, lOutdoorHead, lIndoorAir, lRailingHead]), y, "air")
        buildByCondition((layer == lIndoorFeet) & (rndNoise >= 0.25), y, "air")
        buildByCondition((layer == lOutdoorFeet) & (rndNoise >= 0.25) , y, "air")
        buildByCondition((layer == lClear), y, "air")
        buildByConditionRotated(layer == lGrateSide, grateDirection, y, "crimson_trapdoor", ",open=true,half=bottom")
        buildByCondition((layer == lSlabCover), y, "crimson_slab")

interfaceUtils.sendBlocks()
cv2.destroyAllWindows()


## Decoration / Interiors ##

cv2SizedWindow("buildings", shape2d)
cv2SizedWindow("doorspace", shape2d)
cv2SizedWindow("walkspace", shape2d)

failedHouses = 0
succeededHouses = 0

for i in range(1, maxHeight - minHeight):
    y = minHeight + i
    buildings = (blockCache[:,i,:] == lcBuildingFoundation).astype(np.uint8)
    imshowLabels("buildings", buildings)

    labelCount, buildingsLabels, _, centroids = cv2.connectedComponentsWithStats(buildings, connectivity=4)
    buildingsLabels = buildingsLabels.astype(np.uint8)

    # the first operation gets rid of the corners
    wallsLabels = cv2.dilate(cv2.erode(buildingsLabels, strctCross), strctCross) - cv2.erode(buildingsLabels, strctCross)
    # surroundingLabels = cv2.dilate(buildingsLabels, strctCross) - buildingsLabels
    # lets start with the door
    walkSpace = (np.isin(blockCache[:,i-1,:], [lcPlatform, lcStairs]) | (y <= flattenedHM)).astype(np.uint8)
    walkSpace = traversibilityCheck(walkSpace, i, 2)
    accesible = cv2.dilate(walkSpace, strctCross)
    doorPotential = np.where(accesible > 0, wallsLabels, 0)

    peoplePotential = cv2.erode(buildings, strctCross) * buildingsLabels

    # another representation
    furniture = np.zeros(shape2d, dtype=np.uint8)
    distToEdge = cv2.distanceTransform(buildings, cv2.DIST_L1, 3)
    blockedByDoors = np.zeros(shape2d, dtype=np.uint8)

    imshowLabels("doorspace", doorPotential)
    imshowLabels("walkspace", walkSpace)

    rndNoise = noise(shape2d, shape2d)

    # DOORS & people
    for j in range(1, labelCount):
        exitPositions = listWhere(doorPotential == j)
        peoplePositions = listWhere(peoplePotential == j)

        if len(exitPositions) > 0:
            succeededHouses += 1
            pos = exitPositions[randrange(len(exitPositions))]
            blockCache[pos[0], i-1, pos[1]] = lcDoorstep
            blockCache[pos[0], i:i+2, pos[1]] = lcDoor
            blockedByDoors[pos[0], pos[1]] = 1
            if BUILD:
                # TODO let door face in correct direction
                interfaceUtils.setBlock(area[0] + pos[0], y, area[1] + pos[1], "acacia_door[half=lower]")
                interfaceUtils.setBlock(area[0] + pos[0], y+1, area[1] + pos[1], "acacia_door[half=upper]")

            
            if len(peoplePositions) > 0:
                # for _ in range(randint(1,4)):
                p = choice(peoplePositions)
                interfaceUtils.runCommand(f"summon villager {area[0] + p[0]} {y+1} {area[1] + p[1]}")
        else:
            failedHouses += 1
            centroid = centroids[j]
            print(f"House didn't find exit!!! at {area[0] + centroid[0]} {y} {area[1] + centroid[1]}")
            # TODO do something better
            continue

    strctElmt = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
    blockedByDoors = cv2.dilate(blockedByDoors, strctElmt)

    if BUILD:
        # clear some space
        for k in range(2):
            if y+k < maxHeight:
                # clearable = np.isin(layerCache[:,i+k,:], [lGrateSide]) | ((y+k <= flattenedHM) & (layerCache[:,i+k,:] == 0))
                clearable = (layerCache[:,i+k,:] == lGrateSide) | ((y+k <= flattenedHM) & (blockCache[:,i+k,:] == 0))

                clearSpace = np.where((blockedByDoors > 0) & clearable)
                
                for p in zip(*clearSpace):
                    interfaceUtils.setBlock(area[0] + p[0], y+k, area[1] + p[1], "air")

        # clutter
        for cpos in zip(*np.where((distToEdge == 2) & (blockedByDoors == 0) & (rndNoise > .2))):
            # blocked[cpos[0], cpos[1]] = 1
            blockID = getSimpleRandomClutter()
            if random() > 0.5:
                interfaceUtils.setBlock(area[0] + cpos[0], y, area[1] + cpos[1], blockID)
            else:
                furnID = getFurnitureRandomClutter()
                interfaceUtils.setBlock(area[0] + cpos[0], y, area[1] + cpos[1], furnID)
                interfaceUtils.setBlock(area[0] + cpos[0], y+1, area[1] + cpos[1], blockID)
        
        
    # beds        
    for j in range(1, labelCount):
        bedPositions = listWhere((distToEdge == 3) & (blockedByDoors == 0) & (buildingsLabels == j))

        if len(bedPositions) > 0:
            cpos = choice(bedPositions)
            # blocked[cpos[0], cpos[1]] = 1
            dir = randrange(4)
            # CARDINALS = ["east", "south", "north", "west"]
            card = CARDINALS[dir]
            deltaX = [1,0,0,-1][dir]
            deltaZ = [0,1,-1,0][dir]
            col = choice(minecraft_colors)
            blockID1 = f"{col}_bed[facing={card},part=foot]"
            blockID2 = f"{col}_bed[facing={card},part=head]"

            if BUILD:
                interfaceUtils.setBlock(area[0] + cpos[0], y, area[1] + cpos[1], blockID1)
                interfaceUtils.setBlock(area[0] + cpos[0] + deltaX, y, area[1] + cpos[1] + deltaZ, blockID2)

 
    # cv2.waitKey(0 if buildingsLabels.max() > 0 else 1)
    cv2.waitKey(1)

cv2.destroyAllWindows()
interfaceUtils.sendBlocks()

secs = int(perf_counter() - time0)

print(f"number of lamps in the settlement: {numberOfLamps}")
print(f"buildings with doors: {succeededHouses} buildings without doors: {failedHouses}")

print(f"Took {secs//60} min {secs%60} sec")

DEBUG_CONSOLE = False

while True and DEBUG_CONSOLE:
    cmd = input(">")
    if cmd in ["q", "exit", "quit"]:
        break

    args = cmd.split(" ")
    if args[0] == "lc":
        x = int(args[1]) - area[0]
        y = int(args[2]) - minHeight
        z = int(args[3]) - area[1]
        print(layerCache[x, y, z])
    elif args[0] == "bc":
        x = int(args[1]) - area[0]
        y = int(args[2]) - minHeight
        z = int(args[3]) - area[1]
        print(blockCache[x, y, z])

