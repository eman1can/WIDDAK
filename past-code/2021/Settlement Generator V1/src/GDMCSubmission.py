# Although there are three options that can be changed in the MCEdit GUI, I strongly recommend keeping them at their default values

import random
from numpy import zeros
import itertools
from pymclevel import alphaMaterials, TAG_Int, TAG_String, TAG_List, TAG_Compound, TileEntity
from pymclevel.level import extractHeights
from pymclevel import level, MCSchematic, BoundingBox, TileEntity
from mcInterface import MCLevelAdapter
import numpy as np
import math
from PIL import Image
from pymclevel.box import Vector
from datetime import datetime

am = alphaMaterials

# Naturally occuring materials
blocks = [
    am.Grass,
    am.Dirt,
    am.Stone,
    am.Bedrock,
    am.Sand,
    am.Gravel,
    am.GoldOre,
    am.IronOre,
    am.CoalOre,
    am.LapisLazuliOre,
    am.DiamondOre,
    am.RedstoneOre,
    am.RedstoneOreGlowing,
    am.Netherrack,
    am.SoulSand,
    am.Clay,
    am.Glowstone,
    am.Water,
    am.WaterActive,
    am.HardenedClay,
    am[159, 0], # The different colored Terracotta blocks
    am[159, 1],
    am[159, 4],
    am[159, 8],
    am[159, 12],
    am[159, 14],
    am[12, 1] # Red sand
]
blocktypes = [b.ID for b in blocks]

def naturalBlockmask():
    blockmask = zeros((256,), dtype='bool')
    blockmask[blocktypes] = True
    return blockmask

# Naturally occuring materials without water
blocksWithoutWater = [
    am.Grass,
    am.Dirt,
    am.Stone,
    am.Bedrock,
    am.Sand,
    am.Gravel,
    am.GoldOre,
    am.IronOre,
    am.CoalOre,
    am.LapisLazuliOre,
    am.DiamondOre,
    am.RedstoneOre,
    am.RedstoneOreGlowing,
    am.Netherrack,
    am.SoulSand,
    am.Clay,
    am.Glowstone,
    am.StainedClay,
    am.HardenedClay,
    am[159, 0], # The different colored Terracotta blocks
    am[159, 1],
    am[159, 4],
    am[159, 8],
    am[159, 12],
    am[159, 14],
    am[12, 1] # Red sand
]
blocktypesWithoutWater = [b.ID for b in blocksWithoutWater]

def naturalBlockmaskWithoutWater():
    blockmask = zeros((256,), dtype='bool')
    blockmask[blocktypesWithoutWater] = True
    return blockmask

syllables = [
    "ba",
    "be",
    "bi",
    "bo",
    "bu",
    "ca",
    "ce",
    "ci",
    "co",
    "cu",
    "da",
    "de",
    "di",
    "do",
    "du",
    "du",
    "fe",
    "fi",
    "fo",
    "ba",
    "be",
    "bi",
    "bo",
    "bu",
    "ca",
    "ce",
    "ci",
    "co",
    "cu",
    "da",
    "de",
    "di",
    "do",
    "du",
    "fa",
    "fe",
    "fi",
    "fo",
    "fu",
    "ga",
    "ge",
    "gi",
    "go",
    "gu",
    "ha",
    "he",
    "hi",
    "ho",
    "hu",
    "ja",
    "je",
    "ji",
    "jo",
    "ju",
    "ka",
    "ke",
    "ki",
    "ko",
    "ku",
    "la",
    "le",
    "li",
    "lo",
    "lu",
    "ma",
    "me",
    "mi",
    "mo",
    "mu",
    "na",
    "ne",
    "ni",
    "no",
    "nu",
    "pa",
    "pe",
    "pi",
    "po",
    "pu",
    "qa",
    "qe",
    "qi",
    "qo",
    "qu",
    "ra",
    "re",
    "ri",
    "ro",
    "ru",
    "sa",
    "se",
    "si",
    "so",
    "su",
    "ta",
    "te",
    "ti",
    "to",
    "tu",
    "va",
    "ve",
    "vi",
    "vo",
    "vu",
    "wa",
    "we",
    "wi",
    "wo",
    "wu",
    "xa",
    "xe",
    "xi",
    "xo",
    "xu",
    "ya",
    "ye",
    "yi",
    "yo",
    "yu",
    "za",
    "ze",
    "zi",
    "zo",
    "zu"
]

def getName():
    output = ""
    for i in xrange(3):
        output += syllables[random.randint(0, len(syllables)-1)]
    return output.capitalize()

def crestPatternGenerator(name):
    seed = 0
    for i in xrange(len(name)):
        seed += math.pow(ord(name[i]), i+1)
    random.seed(seed)
    pattern = []
    for i in xrange(3):
        pattern.append([])
        for j in xrange(2):
            pattern[i].append(random.randint(0, 15))
    random.seed(datetime.now())
    return pattern

class Person:
    def __init__(self, family, generation, firstName, parent1=None, parent2=None, lastName=None):
        self.family = family
        self.generation = generation
        self.spouse = None
        self.children = []
        self.parent1 = parent1
        self.parent2 = parent2
        self.firstName = firstName
        if lastName:
            self.lastName = lastName
        else:
            self.lastName = parent1.lastName
    
    def __str__(self):
        output = ""
        output += self.firstName + " " + self.lastName
        return output
    
    def getParents(self):
        output = "Parent 1: "
        output += "Unknown" if (self.parent1 == None) else str(self.parent1)
        output += ", Parent 2: "
        output += "Unknown" if (self.parent2 == None) else str(self.parent2)
        return output
    
    def marry(self, otherPerson):
        # Both people become eachothers spouses
        self.spouse = otherPerson
        otherPerson.spouse = self
        # The person who gets asked takes the last name of the person who asks
        otherPerson.lastName = self.lastName
        # The person who got asked gets removed from their old familt and added to the family of the person who asked them
        otherPerson.family.members[otherPerson.generation].remove(otherPerson)
        otherPerson.family = self.family
        self.family.members[otherPerson.generation].append(otherPerson)

class Family:
    def __init__(self, generations, manualGenerations=False):
        self.lastName = getName()
        self.members = []
        if not manualGenerations:
            for i in xrange(generations):
                self.members.append([])
                for j in xrange(int(math.pow(2, i))):
                    parent = self.members[i-1][random.randint(0, len(self.members[i-1])-1)] if i > 0 else None
                    self.members[i].append(Person(self, i, getName(), parent1=parent, parent2=None, lastName=self.lastName))
        else:
            self.members.append([])
            self.members[0].append(Person(self, 0, getName(), None, None, lastName=self.lastName))
            self.members[0].append(Person(self, 0, getName(), None, None, lastName=self.lastName))

    def getCurrentGeneration(self):
        output = " --- The " + str(self.lastName) + " Family --- \n"
        for j in xrange(len(self.members[len(self.members)-1])):
            output += str(self.members[len(self.members)-1][j]) + ", " + self.members[len(self.members)-1][j].getParents() + ", Spouse: " + str(self.members[len(self.members)-1][j].spouse) + "\n"
        return output
    
    def getCurrentGenerationCount(self):
        return len(self.members[len(self.members)-1])

    def __str__(self):
        output = " --- The " + str(self.lastName) + " Family --- \n"
        for i in xrange(len(self.members)):
            output += " - Generation " + str(i) + " - \n"
            for j in xrange(len(self.members[i])):
                output += str(self.members[i][j]) + ", " + self.members[i][j].getParents() + ", Spouse: " + str(self.members[i][j].spouse) + "\n"
        return output

class Settlement:
    def __init__(self, families, generations):
        # Create the number of families specified
        self.families = []
        for i in xrange(families):
            self.families.append(Family(generations, True))
        # Simulate the number of generations specified
        for g in xrange(generations):
            # Get the size of the family that is the biggest at the current generation
            biggestFamilySize = 0
            for i in xrange(len(self.families)):
                biggestFamilySize = max(biggestFamilySize, len(self.families[i].members[g]))
            # For the ith person in each family
            for i in xrange(biggestFamilySize):
                # For family j
                for j in xrange(len(self.families)):
                    # Until they get rejected 10 times
                    rejectCount = 10
                    while len(self.families[j].members[g]) > i and self.families[j].members[g][i].spouse == None and rejectCount > 0:
                        # Pick a random family (and keep picking until you pick one that still has people in it)
                        spouseFamilyIndex = random.randint(0, len(self.families)-1)
                        while len(self.families[spouseFamilyIndex].members[g]) < 1:
                            spouseFamilyIndex = random.randint(0, len(self.families)-1)
                        # If that family has more than one member
                        if len(self.families[spouseFamilyIndex].members[g]) > 1:
                            # Pick a random member of that family
                            spouseIndex = random.randint(0, len(self.families[spouseFamilyIndex].members[g])-1)
                            # If their family isn't yours and they are single
                            if spouseFamilyIndex != j and self.families[spouseFamilyIndex].members[g][spouseIndex].spouse == None:
                                # Get married to that person
                                self.families[j].members[g][i].marry(self.families[spouseFamilyIndex].members[g][spouseIndex])
                            else:
                                # Otherwise, get rejected
                                rejectCount -= 1
                        # If the family that you picked only has one person
                        elif len(self.families[spouseFamilyIndex].members[g]) == 1:
                            # If the family isn't yours
                            if spouseFamilyIndex != j and self.families[spouseFamilyIndex].members[g][0].spouse == None:
                                # Marry that person
                                self.families[j].members[g][i].marry(self.families[spouseFamilyIndex].members[g][0])
                            else:
                                # Otherwise, get rejected
                                rejectCount -= 1
            # For every family, make a space for the new generation
            for i in xrange(len(self.families)):
                self.families[i].members.append([])
                # For every member of the current generation
                for j in xrange(len(self.families[i].members[g])):
                    # If you currently have a spouse and no children
                    if self.families[i].members[g][j].spouse != None and len(self.families[i].members[g][j].children) == 0:
                        # Have between 1 and 3 children
                        for k in xrange(random.randint(1,3)):
                            child = Person(self.families[i], len(self.families[i].members)-1, getName(), self.families[i].members[g][j], self.families[i].members[g][j].spouse)
                            self.families[i].members[len(self.families[i].members)-1].append(child)
                            # And make sure that it is registered as a child for both parents
                            self.families[i].members[g][j].children.append(child)
                            self.families[i].members[g][j].spouse.children.append(child)
    
    def getCurrentGeneration(self):
        output = ""
        currentGenCount = 0
        for i in xrange(len(self.families)):
            output += "\n"
            output += self.families[i].getCurrentGeneration()
            currentGenCount += self.families[i].getCurrentGenerationCount()
        output += "Total Population: " + str(currentGenCount)
        return output
    
    def __str__(self):
        output = ""
        for i in xrange(len(self.families)):
            output += "\n"
            output += str(self.families[i])
        return output

# A bunch of constants in arrays used to convert minecrafts different ways of representing direction into a usable standard
doorOffsetX = [1, 0, -1, 0]
doorOffsetZ = [0, -1, 0, 1]
doorOrientation = [3, 0, 1, 2]
turnCountToBannerRotation = [5, 2, 4, 3]
upsideDownStairDirection = [6, 4, 7, 5]
trapdoorLadderDirections = [[5, 6], [2, 5], [4, 7], [3, 4]]
ladderDirections = [[2, 2], [3, 3], [4, 4], [5, 5], [2, 3], [3, 2], [4, 5], [5, 4]]
# A collection of all of the offsets for the streetlights from a given path coordinate
streetLightOffsets = [[[[2,-2],[-2,2]], [[0,-2],[0,2]], [[-2,-2],[2,2]]], [[[-2,0],[2,0]], [[0,0],[0,0]], [[-2,0],[2,0]]], [[[-2,-2],[2,2]], [[0,-2],[0,2]], [[2,-2],[-2,2]]]]

# The possible actions that the AStar pathfinding can take
actions = [[1, 1], [-1, -1], [1, -1], [-1, 1], [0, 1], [0, -1], [1, 0], [-1, 0]]
# AStar node class
class Node:
    def __init__(self, x, z, parent, action, g, h):
        self.x = x
        self.z = z
        self.action = action
        self.parent = parent
        self.g = g
        self.h = h

# A 2D vector class mostly used in the Poisson Disc Distribution algorithm
class Vec2:
        def __init__(self, x, y, isFromUniqueStructure=False):
            self.isFromUniqueStructure = isFromUniqueStructure
            self.x = x
            self.y = y
        
        def multiply(self, m):
            self.x = self.x * m
            self.y = self.y * m
        
        def add(self, a):
            self.x = self.x + a.x
            self.y = self.y + a.y

# The inputs that can be entered in the MCEdit GUI and their defaults
inputs = (
    ("Cristopher Yates", "label"),
    ("Poisson Distribution", "label"),
    ("Radius: ", 28),
    ("Families: ", 48),
    ("Generations: ", 3),
)

chunks = None
boundingBox = None
chunks = []

def perform(level, box, options):

    print("X: " + str(box.maxx - box.minx) + ", Z: " + str(box.maxz - box.minz))

    # If the selected area is too big
    tooBig = False
    center = None
    initialBox = None
    if (box.maxx - box.minx) > 256 or (box.maxz - box.minz) > 256:
        print("Too big!")
        tooBig = True
        # Pick a location to build the settlement
        halfXSize = (box.maxx - box.minx)/2
        halfZSize = (box.maxz - box.minz)/2
        center = [halfXSize + box.minx, halfZSize + box.minz]
        settlementPlacementOffset = Vec2(-1 * random.randint(128, halfXSize - 128), random.randint(128, halfZSize - 128))
        settlementPlacementOffset.x += center[0]
        settlementPlacementOffset.y += center[1]
        # Place the settlement at the chosen location
        initialBox = box
        box = BoundingBox((settlementPlacementOffset.x - 128, box.miny, settlementPlacementOffset.y - 128), (256, box.maxy, 256))
        



    # Generate the families for the settlement
    settlement = Settlement(options["Families: "], options["Generations: "])

    print("Calculating HeightMap...")
    horizontalHeightmapParts = []
    horizontalHeightmapPartsWithoutWater = []

    # All of the code between these two "lines" is adapted slightly / comes from the built in MCEdit filter: topsoil.py 

    ##############################################################################

    #compute a truth table that we can index to find out whether a block
    # is naturally occuring and should be considered in a heightmap
    blockmask = naturalBlockmask()
    blockmaskWithoutWater = naturalBlockmaskWithoutWater()

    currentX = None

    #iterate through the slices of each chunk in the selection box
    for chunk, slices, point in level.getChunkSlices(box):
        # slicing the block array is straightforward. blocks will contain only
        # the area of interest in this chunk.

        blocks = chunk.Blocks[slices]

        # use indexing to look up whether or not each block in blocks is
        # naturally-occuring. these blocks will "count" for column height.
        maskedBlocks = blockmask[blocks]
        maskedBlocksWithoutWater = blockmaskWithoutWater[blocks]

    ##############################################################################

        heightmap = extractHeights(maskedBlocks)
        heightmapWithoutWater = extractHeights(maskedBlocksWithoutWater)
        if currentX != chunk.chunkPosition[0]:
            currentX = chunk.chunkPosition[0]
            horizontalHeightmapParts.append(heightmap)
            horizontalHeightmapPartsWithoutWater.append(heightmapWithoutWater)
        else:
            horizontalHeightmapParts[len(horizontalHeightmapParts)-1] = np.hstack((horizontalHeightmapParts[len(horizontalHeightmapParts)-1], heightmap))
            horizontalHeightmapPartsWithoutWater[len(horizontalHeightmapPartsWithoutWater)-1] = np.hstack((horizontalHeightmapPartsWithoutWater[len(horizontalHeightmapPartsWithoutWater)-1], heightmapWithoutWater))
    
    completeHeightmap = horizontalHeightmapParts[0]
    completeHeightmapWithoutWater = horizontalHeightmapPartsWithoutWater[0]
    for i in range(1, len(horizontalHeightmapParts)):
        completeHeightmap = np.vstack((completeHeightmap, horizontalHeightmapParts[i]))
        completeHeightmapWithoutWater = np.vstack((completeHeightmapWithoutWater, horizontalHeightmapPartsWithoutWater[i]))
    print("Finished Calculating HeightMap!")


    # Get the direction that all of the flags will be facing
    flagDir = random.randint(0,3)

    # Initialize the pathfinding grid and the list of door/entrance positions
    pathfindingGrid = np.zeros([abs(box.maxx - box.minx), abs(box.maxz - box.minz)])
    doorPositions = []

    


    print("Calculating Distribution")

    width = box.maxx - box.minx
    height = box.maxz - box.minz

    r = options["Radius: "]
    k = 30
    grid = []
    w = r / math.sqrt(2)
    active = []

    # Set Up Grid
    cols = math.floor(width / w)
    rows = math.floor(height / w)
    for i in range(int(cols * rows)):
        grid.append(None)


    # Placing Unique Structures

    # Nether Temple
    gridPos = [15, 15]
    placeNetherTemple(level, box, 0, completeHeightmap, completeHeightmapWithoutWater, pathfindingGrid, gridPos, doorPositions)
    for i in xrange(int((gridPos[0] + 11)/w)+1):
        for j in xrange(int((gridPos[1] + 15)/w)+1):
            grid[int(i + j * cols)] = Vec2(int((gridPos[0] - 11)) + (w*i), int((gridPos[1] - 15)) + (w * j), True)
            print(str(grid[int(i + j * cols)].x) + ", " + str(grid[int(i + j * cols)].y))
    
    # Cemetary
    cemetaryBox = BoundingBox((box.minx + 4, box.miny + 3, box.maxz - 80), (76, box.maxy-3, 76))
    cemetaryHeight = generateCemetary(level, cemetaryBox, settlement, completeHeightmap, completeHeightmapWithoutWater, [4, box.maxz - 80 - box.minz])
    for i in xrange(int((80)/w)+1):
        for j in xrange(int((80)/w)+1):
            grid[int((i) + (cols - 1 - j) * cols)] = Vec2(int(w/3) + (w*i), box.maxz - box.minz - (int(w/3) + (w * j)), True)
    doorPositions.append([80, box.maxz - box.minz - 40])
    # Cemetary Gate
    placeCemetaryGateSchematic(level, Vector(box.minx + 77, cemetaryHeight+4, box.maxz - 42))

    # Farm Building
    gridPos = [240, 240]
    placeFarmBuilding(level, box, 2, completeHeightmap, completeHeightmapWithoutWater, pathfindingGrid, gridPos, doorPositions)


    # Set first Point
    x = ((width) / 2.0)
    y = ((height) / 2.0)
    i = math.floor(x / w)
    j = math.floor(y / w)
    firstPos = Vec2(x, y)
    firstPosIndex = int(i + j * cols)
    grid[firstPosIndex] = firstPos
    active.append(firstPos)

    # Populate the rest of the Points
    while len(active) > 0:
        randIndex = random.randint(0, len(active)-1)
        pos = active[randIndex]
        found = False
        # K times
        for n in range(k):
            # Get a new point between r and 2r from the currently selected active point
            a = random.uniform(0, 2 * math.pi)
            sample = Vec2(math.cos(a), math.sin(a))
            m = random.uniform(r, 2 * r)
            sample.multiply(m)
            sample.add(pos)
            # Get its appropriate grid coordinates
            col = math.floor((sample.x) / w)
            row = math.floor((sample.y) / w)
            # If it's not off the out of bounds and there's no point in that grid spot already
            if col < cols - 1 and col > -1  + 1 and row < rows - 1 and row > -1 + 1 and not grid[int(col + row * cols)]:
                ok = True
                # In a 3x3 area centered on the point
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        # If there's a point in one of those grid positions and it's too close to the point we are trying to place
                        if (col+i) + (row+j) * cols > -1 and (col+i) + (row+j) * cols < len(grid):
                            neighbor = grid[int((col+i) + (row+j) * cols)]
                            if neighbor:
                                diffX = sample.x - neighbor.x
                                diffY = sample.y - neighbor.y
                                d = (diffX * diffX) + (diffY * diffY)
                                if d < (r * r):
                                    # The point will not be placed on the grid
                                    ok = False
                # Otherwise place the point on the grid
                if ok:
                    found = True
                    grid[int(col + row * cols)] = sample
                    active.append(sample)
                    break
        # After K point placing attempts, pop the currently selected active point from the active list 
        if not found:
            active.pop(randIndex)


    # Initialize the index of the person that we are giving a house at 0
    personCounter = 0
    # Initialize the list of people who are in the current generation as empty
    alivePeople = []
    # Add all of the people from the current generation to the alive people list
    for i in xrange(len(settlement.families)):
        for j in range(len(settlement.families[i].members[len(settlement.families[i].members)-1])):
            alivePeople.append(settlement.families[i].members[len(settlement.families[i].members)-1][j])
    # Randomimze the order of the list
    random.shuffle(alivePeople)
    for i in xrange(len(grid)):
        # If the current house position is the one at the middle of the settlment, place the "lore shrine" there instead of a house
        if i == firstPosIndex:
            dest = [int(math.floor(box.minx + grid[i].x)), int(math.floor(box.minz + grid[i].y))]
            placeLoreShrine(level, box, completeHeightmap, completeHeightmapWithoutWater, pathfindingGrid, grid[i], dest)
        # Otherwise, if the position on the grid is not from a unique structure place a house there
        elif grid[i] and not grid[i].isFromUniqueStructure:
            person = alivePeople[personCounter]
            turnCount = random.randint(0, 3)
            dest = [int(math.floor(box.minx + grid[i].x))+1, int(math.floor(box.minz + grid[i].y))+1]
            # Pick a random house and place it in the spot specified, and have it be inhabited by the next person in the alivePeople list
            houseIndex = random.randint(0,3)
            housePlacingFunctions[houseIndex](level, box, turnCount, completeHeightmap, completeHeightmapWithoutWater, pathfindingGrid, grid[i], dest, doorPositions, flagDir, person)
            personCounter += 1


    # Store some images of the heightmap and the pathfinding grid for no discernible reason
    im = Image.fromarray(np.array(completeHeightmap))
    im.convert('RGB').save("heightmap.jpeg")
    im = Image.fromarray(np.array(pathfindingGrid))
    im.convert('RGB').save("pathfinding.jpeg")


    # Paths
    
    # Initialize a 2D array to keep track of where to place path blocks
    pathBlocks = np.zeros([abs(box.maxx - box.minx), abs(box.maxz - box.minz)])

    # Keep track of the door position that is furthest to the north-east
    northEastPos = [0, 256]

    # For each door/entrance position in the list
    for i in xrange(len(doorPositions)):
        # Check if the position is the furthest to the north-east
        if (doorPositions[i][0] + (256-doorPositions[i][1])) > (northEastPos[0] + (256-northEastPos[1])):
            # If so store the postion
            northEastPos = doorPositions[i]
        # Get the height at that position
        startY = completeHeightmap[doorPositions[i][0], doorPositions[i][1]]
        dists = []
        # For each door/entrance position in the list that comes after position i
        for j in xrange(i, len(doorPositions)):
            if i != j:
                # Get the height at that position
                goalY = completeHeightmap[doorPositions[j][0], doorPositions[j][1]]
                # Make a list with the differences in position for the 3 dimensions
                deltas = [doorPositions[i][0] - doorPositions[j][0], startY - goalY, doorPositions[i][1] - doorPositions[j][1]]
                # Get the squared distance from the first position to the second and append it to the list of distances
                distSquared = (deltas[0] * deltas[0]) + (deltas[1] * deltas[1]) + (deltas[2] * deltas[2])
                dists.append(distSquared)
                print("The distance from house " + str(i) + " to house " + str(j) + " is " + str(distSquared))
        # Disregard the rest of this if there were no distances added to the list
        if len(dists) == 0:
            continue
        # Get the index in the doorPositions list of the closest other door/entrance position
        minIndex = dists.index(min(dists)) + i + 1
        print("Connecting house " + str(i) + " with house " + str(minIndex))
        print("Positions: (" + str(doorPositions[i][0]) + ", " + str(doorPositions[i][1]) + ") and (" + str(doorPositions[minIndex][0]) + ", " + str(doorPositions[minIndex][1]) + ")")
        # Find the path from position "i" to position "minIndex"
        path = aStar(level, box, [int(doorPositions[i][0]), int(doorPositions[i][1])], [int(doorPositions[minIndex][0]), int(doorPositions[minIndex][1])], pathfindingGrid, completeHeightmap)
        # For every block in the path
        for k in xrange(len(path)):
            # Add that block to the array of path blocks
            pathBlocks[path[k][0], path[k][1]] = 1
            # If it's not at the beginning, or the end, every eighth block
            if k != 0 and k + 1 != len(path) and k % 8 == 0:
                # Place street lights on either side of the path
                xDiff = path[k+1][0] - path[k][0]
                zDiff = path[k+1][1] - path[k][1]
                pos = streetLightOffsets[xDiff+1][zDiff+1][0]
                if pos[0] == 0 and pos[1] == 0:
                    break
                height = completeHeightmap[pos[0] + path[k][0], pos[1] + path[k][1]]
                dest = Vector(pos[0] + box.minx + path[k][0], height-1, pos[1] + box.minz + path[k][1])
                # Only if they wouldn't intersect with a building
                if pathfindingGrid[pos[0] + path[k][0], pos[1] + path[k][1]] != 255:
                    placeStreetLightSchematic(level, dest)
                    pathfindingGrid[pos[0], pos[1]] = 255
                pos = streetLightOffsets[xDiff+1][zDiff+1][1]
                height = completeHeightmap[pos[0] + path[k][0], pos[1] + path[k][1]]
                dest = Vector(pos[0] + box.minx + path[k][0], height-1, pos[1] + box.minz + path[k][1])
                # Only if they wouldn't intersect with a building: the sequel
                if pathfindingGrid[pos[0] + path[k][0], pos[1] + path[k][1]] != 255:
                    placeStreetLightSchematic(level, dest)
                    pathfindingGrid[pos[0], pos[1]] = 255
    for i in xrange(abs(box.maxx - box.minx)):
        for j in xrange(abs(box.maxz - box.minz)):
            if pathBlocks[i, j] == 1:
                # Get the block below the one that is being replaced
                blockBelowReplaced = level.blockAt(box.minx + i, completeHeightmap[i][j]-2, box.minz + j)
                # Set the block that the this segment of the path will be made of to Stone Bricks if it's over water, and Path block otherwise
                pathBlock = 98 if (blockBelowReplaced == 8 or blockBelowReplaced == 9) else 208
                level.setBlockAt(box.minx + i, completeHeightmap[i][j]-1, box.minz + j, pathBlock)
                level.setBlockDataAt(box.minx + i, completeHeightmap[i][j]-1, box.minz + j, 0)
                # Do the same for a 3x3 area centered on that block
                for k in xrange(8):
                    blockBelowReplaced = level.blockAt(box.minx + i + actions[k][0], completeHeightmap[i + actions[k][0]][j + actions[k][1]]-2, box.minz + j + actions[k][1])
                    pathBlock = 98 if (blockBelowReplaced == 8 or blockBelowReplaced == 9) else 208
                    level.setBlockAt(box.minx + i + actions[k][0], completeHeightmap[i + actions[k][0]][j + actions[k][1]]-1, box.minz + j + actions[k][1], pathBlock)
                    level.setBlockDataAt(box.minx + i + actions[k][0], completeHeightmap[i + actions[k][0]][j + actions[k][1]]-1, box.minz + j + actions[k][1], 0)
    print("Blocks Placed!")
    print(str(personCounter) + " Houses in total")

    # Place the path from the center of the map to the settlement if need be
    if tooBig:
        # Calculate the bounding box for the area where the path will be made
        anotherBox = BoundingBox(((northEastPos[0]+box.minx)-1, box.miny, center[1]-1), (center[0]-(northEastPos[0]+box.minx)+2, box.maxy, (northEastPos[1]+box.minz)-center[1]+2))
        print("Min Point: X: " + str(anotherBox.minx) + ", Z: " + str(anotherBox.minz))
        print("Size: X: " + str(anotherBox.maxx - anotherBox.minx) + ", Z: " + str(anotherBox.maxz - anotherBox.minz))
        # Reset some stuff used earlier
        currentX = None
        horizontalHeightmapParts = []

        # The following section is derived from the built in MCEdit filter: topsoil.py 

        ##############################################################################

        #iterate through the slices of each chunk in the selection box
        for chunk, slices, point in level.getChunkSlices(anotherBox):
            # slicing the block array is straightforward. blocks will contain only
            # the area of interest in this chunk.

            blocks = chunk.Blocks[slices]

            # use indexing to look up whether or not each block in blocks is
            # naturally-occuring. these blocks will "count" for column height.
            maskedBlocks = blockmask[blocks]

        ##############################################################################

        # Construct the heightmap from slices of chunks
            heightmap = extractHeights(maskedBlocks)
            if currentX != chunk.chunkPosition[0]:
                currentX = chunk.chunkPosition[0]
                horizontalHeightmapParts.append(heightmap)
            else:
                horizontalHeightmapParts[len(horizontalHeightmapParts)-1] = np.hstack((horizontalHeightmapParts[len(horizontalHeightmapParts)-1], heightmap))

        completeHeightmap = horizontalHeightmapParts[0]
        for i in range(1, len(horizontalHeightmapParts)):
            completeHeightmap = np.vstack((completeHeightmap, horizontalHeightmapParts[i]))
        print("Finished Calculating HeightMap!")
        
        # Find the path from the center of the initial selection to the north-east point of the settlement
        pathfindingGrid = np.zeros([abs(anotherBox.maxx - anotherBox.minx), abs(anotherBox.maxz - anotherBox.minz)])
        newStart = [anotherBox.maxx-anotherBox.minx-2, 1]
        newGoal = [1, anotherBox.maxz-anotherBox.minz-2]
        path = aStar(level, anotherBox, newStart, newGoal, pathfindingGrid, completeHeightmap)
        # For every block in the path (except the last few) place blocks on the ground in a 3x3 centered around it
        for i in xrange(1, len(path)-5):
            for x in xrange(-1, 2):
                for y in xrange(-1, 2):
                    blockBelowReplaced = level.blockAt(anotherBox.minx + path[i][0] + x, completeHeightmap[path[i][0] + x, path[i][1] + y]-2, anotherBox.minz + path[i][1] + y)
                    pathBlock = 98 if (blockBelowReplaced == 8 or blockBelowReplaced == 9) else 208
                    level.setBlockAt(anotherBox.minx + path[i][0] + x, completeHeightmap[path[i][0] + x, path[i][1] + y]-1, anotherBox.minz + path[i][1] + y, pathBlock)
                    level.setBlockDataAt(anotherBox.minx + path[i][0] + x, completeHeightmap[path[i][0] + x, path[i][1] + y]-1, anotherBox.minz + path[i][1] + y, 0)
    


# The AStar pathfinding algorithm
def aStar(level, box, start, goal, pathfindingGrid, completeHeightmap):
    
    # Functions to estimate the cost using a heuristic, and determine if an action is legal
    def estimateCost(x, z, goal):
        return (abs(x-goal[0]) + abs(z-goal[1])) * 100
    def isLegalAction(x, z, action, pathfindingGrid):
        if not (x + action[0] < 0 or x + action[0] >= len(pathfindingGrid) or z + action[1] < 0 or z + action[1] >= len(pathfindingGrid[0]) or pathfindingGrid[x, z] == 255):
            return True
    
    # Initialize a bunch of stuff
    inProgress = True
    path = []
    openList = [Node(start[0], start[1], None, None, 0, 0)]
    openListGArray = [[0 for i in xrange(len(pathfindingGrid[0]))] for j in xrange(len(pathfindingGrid))]
    closed = [[False for i in xrange(len(pathfindingGrid[0]))] for j in xrange(len(pathfindingGrid))]

    while inProgress:
        
        print("Open: " + str(len(openList)))
        # If the openlist is empty, stop trying to find a path
        if len(openList) == 0:
            inProgress = False
            return path
                
        # Find and pop th enode with the lowest F value
        minF = openList[0].g + openList[0].h
        minFIndex = 0
        for i in xrange(1, len(openList)):
            if openList[i].g + openList[i].h < minF:
                minF = openList[i].g + openList[i].h
                minFIndex = i
            # Using H as a tiebreaker if needed
            elif openList[i].g + openList[i].h == minF and openList[minFIndex].h > openList[i].h:
                    minFIndex = i
        node = openList.pop(minFIndex)
        # Add that node to the closed list
        closed[node.x][node.z] = True
        # If the popped node is the goal node, stop the search and return the path
        if goal[0] == node.x and goal[1] == node.z:
            inProgress = False
            while node.parent != None:
                path.append([node.x, node.z])
                node = node.parent
            return path

        # For all eight surrounding nodes on the grid
        for i in xrange(8):
            a = actions[i]
            # If the action to get to it is legal
            if not isLegalAction(node.x, node.z, a, pathfindingGrid):
                continue
            # And the node isn't in the closed list already
            s = [node.x + a[0], node.z + a[1]]
            if closed[s[0]][s[1]]:
                continue
            # And it's G value is grater than any G values already stored for that position in the "openListGArray"
            newG = node.g + 100 + (40 * (a[0] and a[1]))
            if openListGArray[s[0]][s[1]] and openListGArray[s[0]][s[1]] < newG:
                continue
            # Append the node to the open list
            openListGArray[s[0]][s[1]] = newG
            heuristic = estimateCost(s[0], s[1], goal)
            openList.append(Node(s[0], s[1], node, a, newG, heuristic))

    

def placeHouse1(level, box, turnCount, completeHeightmap, completeHeightmapWithoutWater, pathfindingGrid, gridPos, dest, doorPositions, flagDir, resident):
    print("Turn Count: " + str(turnCount))
    footprint = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]])
    footprint = np.rot90(footprint, k=turnCount*3, axes=(0, 1))
    # Place some barriers on the pathfinding grid
    if turnCount % 2 == 0:
        xRange = [-9, 10]
        zRange = [-7, 8]
    else: 
        xRange = [-7, 8]
        zRange = [-9, 10]
    highestPointUnderStructure = 0
    for x in xrange(xRange[0], xRange[1]):
        for y in xrange(zRange[0], zRange[1]):
            if footprint[x + abs(xRange[0]), y + abs(zRange[0])] == 1:
                pathfindingGrid[int(gridPos.x) + x, int(gridPos.y) + y] = 255
                highestPointUnderStructure = max(highestPointUnderStructure, completeHeightmap[int(gridPos.x) + x, int(gridPos.y) + y])
    # Place the actual house
    placeHouse1Schematic(level, Vector(dest[0], highestPointUnderStructure, dest[1]), turnCount)

    # Append a point from the entrance of the house to the list of "doorPositions"
    doorPos = [int(gridPos.x + (doorOffsetX[turnCount] * 10)), int(gridPos.y + (doorOffsetZ[turnCount] * 10))]
    doorPositions.append(doorPos)
    otherOffset = [doorPos[0] + box.minx - (doorOffsetX[turnCount]*3), doorPos[1] + box.minz - (doorOffsetZ[turnCount]*3)]

    # Pillar to connect to the ground
    pillarToGround(level, box, completeHeightmapWithoutWater, highestPointUnderStructure, 6, 3, gridPos, [0, 0], footprint, [xRange[0], zRange[0]], True)

    # Ladder to the ground
    ladderHeight = highestPointUnderStructure - 1
    while (ladderHeight >= completeHeightmap[doorPos[0], doorPos[1]]):
        level.setBlockAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, 65)
        level.setBlockDataAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, trapdoorLadderDirections[turnCount][0])
        if (level.blockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount]) == 0):
            level.setBlockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], 96)
            level.setBlockDataAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], trapdoorLadderDirections[turnCount][1])
        ladderHeight = ladderHeight - 1


    # Randomize the color of the beds and the carpets next to them
    prevTurn = (turnCount - 1) % 4
    bedColor = random.randint(0, 15)
    bedHeight = highestPointUnderStructure+6
    bedPos = [dest[0]-1 + (doorOffsetX[turnCount] * 4), dest[1]-1 + (doorOffsetZ[turnCount] * 4)]
    placeBed(level, bedPos[0] + (doorOffsetX[prevTurn] * 3), bedHeight, bedPos[1] + (doorOffsetZ[prevTurn] * 3), bedColor, prevTurn)
    placeBed(level, bedPos[0] + (doorOffsetX[prevTurn] * 3) + (doorOffsetX[turnCount]), bedHeight, bedPos[1] + (doorOffsetZ[prevTurn] * 3) + (doorOffsetZ[turnCount]), bedColor, prevTurn)
    level.setBlockDataAt(bedPos[0] + (doorOffsetX[prevTurn] * 3) - (doorOffsetX[turnCount]), bedHeight, bedPos[1] + (doorOffsetZ[prevTurn] * 3) - (doorOffsetZ[turnCount]), bedColor)
    level.setBlockDataAt(bedPos[0] + (doorOffsetX[prevTurn] * 4) - (doorOffsetX[turnCount]), bedHeight, bedPos[1] + (doorOffsetZ[prevTurn] * 4) - (doorOffsetZ[turnCount]), bedColor)
    # Place the banner over the fireplace
    pattern = crestPatternGenerator(resident.lastName)
    banner(level, dest[0]-1 - (doorOffsetX[turnCount]*(4)), highestPointUnderStructure+6, dest[1]-1 - (doorOffsetZ[turnCount]*(4)), pattern, turnCountToBannerRotation[turnCount])
    # Place the flag on top of the building
    nextTurn = (turnCount + 1) % 4
    flag(level, dest[0]-1 + (doorOffsetX[turnCount]*(9)) + (doorOffsetX[nextTurn]*(2)), highestPointUnderStructure+12, dest[1]-1 + (doorOffsetZ[turnCount]*(9)) + (doorOffsetZ[nextTurn]*(2)), flagDir, pattern)
    # Randomize the flowers in the flower beds
    for j in xrange(3):
        flowerIndex = random.randint(0, 10)
        level.setBlockAt(otherOffset[0] + (doorOffsetZ[turnCount]*(3+j)), highestPointUnderStructure+1, otherOffset[1] + (doorOffsetX[turnCount]*(3+j)), 38)
        level.setBlockDataAt(otherOffset[0] + (doorOffsetZ[turnCount]*(3+j)), highestPointUnderStructure+1, otherOffset[1] + (doorOffsetX[turnCount]*(3+j)), flowerIndex)
        flowerIndex = random.randint(0, 10)
        level.setBlockAt(otherOffset[0] - (doorOffsetZ[turnCount]*(3+j)), highestPointUnderStructure+1, otherOffset[1] - (doorOffsetX[turnCount]*(3+j)), 38)
        level.setBlockDataAt(otherOffset[0] - (doorOffsetZ[turnCount]*(3+j)), highestPointUnderStructure+1, otherOffset[1] - (doorOffsetX[turnCount]*(3+j)), flowerIndex)
        flowerIndex = random.randint(0, 10)
        level.setBlockAt(otherOffset[0] + (doorOffsetZ[turnCount]*(3+j)), highestPointUnderStructure+7, otherOffset[1] + (doorOffsetX[turnCount]*(3+j)), 38)
        level.setBlockDataAt(otherOffset[0] + (doorOffsetZ[turnCount]*(3+j)), highestPointUnderStructure+7, otherOffset[1] + (doorOffsetX[turnCount]*(3+j)), flowerIndex)
        flowerIndex = random.randint(0, 10)
        level.setBlockAt(otherOffset[0] - (doorOffsetZ[turnCount]*(3+j)), highestPointUnderStructure+7, otherOffset[1] - (doorOffsetX[turnCount]*(3+j)), 38)
        level.setBlockDataAt(otherOffset[0] - (doorOffsetZ[turnCount]*(3+j)), highestPointUnderStructure+7, otherOffset[1] - (doorOffsetX[turnCount]*(3+j)), flowerIndex)

def placeHouse2(level, box, turnCount, completeHeightmap, completeHeightmapWithoutWater, pathfindingGrid, gridPos, dest, doorPositions, flagDir, resident):
    print("Turn Count: " + str(turnCount))
    footprint = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]])
    footprint = np.rot90(footprint, k=turnCount*3, axes=(0, 1))
    # Place some barriers on the pathfinding grid
    highestPointUnderStructure = 0
    for x in xrange(-8, 9):
        for y in xrange(-8, 9):
            if footprint[x + 8, y + 8] == 1:
                pathfindingGrid[int(gridPos.x) + x, int(gridPos.y) + y] = 255
                highestPointUnderStructure = max(highestPointUnderStructure, completeHeightmap[int(gridPos.x) + x, int(gridPos.y) + y])
    # Place the actual house
    placeHouse2Schematic(level, Vector(dest[0], highestPointUnderStructure, dest[1]), turnCount)

    # Append a point from the entrance of the house to the list of "doorPositions"
    doorPos = [int(math.floor(gridPos.x) + (doorOffsetX[turnCount] * 9)), int(math.floor(gridPos.y) + (doorOffsetZ[turnCount] * 9))]
    doorPositions.append(doorPos)

    # Pillar to connect to the ground
    pillarToGround(level, box, completeHeightmapWithoutWater, highestPointUnderStructure, 6, 3, gridPos, [0, 0], footprint, [-8, -8], True)

    # Ladder to the ground
    ladderHeight = highestPointUnderStructure - 1
    while (ladderHeight >= completeHeightmap[doorPos[0], doorPos[1]]):
        level.setBlockAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, 65)
        level.setBlockDataAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, trapdoorLadderDirections[turnCount][0])
        if (level.blockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount]) == 0):
            level.setBlockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], 96)
            level.setBlockDataAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], trapdoorLadderDirections[turnCount][1])
        ladderHeight = ladderHeight - 1
    
    # Place the banners over the fireplace
    nextTurn = (turnCount + 1) % 4
    pattern = crestPatternGenerator(resident.lastName)
    bannerHeight = highestPointUnderStructure+5
    bannerPos = [dest[0]-1 + (doorOffsetX[turnCount] * -4), dest[1]-1 + (doorOffsetZ[turnCount] * -4)]
    banner(level, bannerPos[0], bannerHeight, bannerPos[1], pattern, turnCountToBannerRotation[turnCount])
    banner(level, bannerPos[0] - (doorOffsetX[nextTurn]), bannerHeight, bannerPos[1] - (doorOffsetZ[nextTurn]), pattern, turnCountToBannerRotation[turnCount])
    banner(level, bannerPos[0] + (doorOffsetX[nextTurn]), bannerHeight, bannerPos[1] + (doorOffsetZ[nextTurn]), pattern, turnCountToBannerRotation[turnCount])
    # Randomize the color of the bed and the carpets surrounding it
    bedColor = random.randint(0, 15)
    bedPos = [dest[0]-1 + (doorOffsetX[turnCount] * 4), dest[1]-1 + (doorOffsetZ[turnCount] * 4)]
    bedHeight = highestPointUnderStructure+5
    placeBed(level, bedPos[0], bedHeight, bedPos[1], bedColor, turnCount)
    level.setBlockDataAt(bedPos[0] + (doorOffsetX[nextTurn]), bedHeight, bedPos[1] + (doorOffsetZ[nextTurn]), bedColor)
    level.setBlockDataAt(bedPos[0] - (doorOffsetX[nextTurn]), bedHeight, bedPos[1] - (doorOffsetZ[nextTurn]), bedColor)
    level.setBlockDataAt(bedPos[0] + (doorOffsetX[nextTurn]) + (doorOffsetX[turnCount]), bedHeight, bedPos[1] + (doorOffsetZ[nextTurn]) + (doorOffsetZ[turnCount]), bedColor)
    level.setBlockDataAt(bedPos[0] - (doorOffsetX[nextTurn]) + (doorOffsetX[turnCount]), bedHeight, bedPos[1] - (doorOffsetZ[nextTurn]) + (doorOffsetZ[turnCount]), bedColor)
    # Place the flag at the top of the house
    flag(level, dest[0]-1 + (doorOffsetX[turnCount] * 5), highestPointUnderStructure+10, dest[1]-1 + (doorOffsetZ[turnCount] * 5), flagDir, pattern)
    # Correct door placement for the fridge
    if turnCount % 2 == 1:
        topVal = 9 if (turnCount == 3) else 8
        bottomVal = 1 if (turnCount == 3) else 3
        level.setBlockDataAt(int(gridPos.x + (doorOffsetX[turnCount] * -4) + (doorOffsetX[nextTurn] * 3)) + box.minx, highestPointUnderStructure+2, int(gridPos.y + (doorOffsetZ[turnCount] * -4) + (doorOffsetZ[nextTurn] * 3)) + box.minz, topVal)
        level.setBlockDataAt(int(gridPos.x + (doorOffsetX[turnCount] * -4) + (doorOffsetX[nextTurn] * 3)) + box.minx, highestPointUnderStructure+1, int(gridPos.y + (doorOffsetZ[turnCount] * -4) + (doorOffsetZ[nextTurn] * 3)) + box.minz, bottomVal)

def placeHouse3(level, box, turnCount, completeHeightmap, completeHeightmapWithoutWater, pathfindingGrid, gridPos, dest, doorPositions, flagDir, resident):
    print("Turn Count: " + str(turnCount))
    footprint = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0]]
    footprint = np.rot90(footprint, k=turnCount*3, axes=(0, 1))
    # Place some barriers on the pathfinding grid
    highestPointUnderStructure = 0
    for x in xrange(-6, 7):
        for y in xrange(-6, 7):
            if footprint[x + 6, y + 6] == 1:
                pathfindingGrid[int(gridPos.x) + x, int(gridPos.y) + y] = 255
                highestPointUnderStructure = max(highestPointUnderStructure, completeHeightmap[int(gridPos.x) + x, int(gridPos.y) + y])
    # Place the actual house
    placeHouse3Schematic(level, Vector(dest[0], highestPointUnderStructure, dest[1]), turnCount)

    # Append a point from the entrance of the house to the list of "doorPositions"
    doorPos = [int(math.floor(gridPos.x) + (doorOffsetX[turnCount] * 7)), int(math.floor(gridPos.y) + (doorOffsetZ[turnCount] * 7))]
    doorPositions.append(doorPos)

    # Pillar to connect to the ground
    pillarToGround(level, box, completeHeightmapWithoutWater, highestPointUnderStructure, 6, 3, gridPos, [0, 0], footprint, [-6, -6], True)

    # Ladder to the ground
    ladderHeight = highestPointUnderStructure - 1
    while (ladderHeight >= completeHeightmap[doorPos[0], doorPos[1]]):
        level.setBlockAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, 65)
        level.setBlockDataAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, trapdoorLadderDirections[turnCount][0])
        if (level.blockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount]) == 0):
            level.setBlockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], 96)
            level.setBlockDataAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], trapdoorLadderDirections[turnCount][1])
        ladderHeight = ladderHeight - 1

    # Place the flag at the top of the house
    pattern = crestPatternGenerator(resident.lastName)
    flag(level, dest[0]-1 + (doorOffsetX[turnCount] * 4), highestPointUnderStructure+15, dest[1]-1 + (doorOffsetZ[turnCount] * 4), flagDir, pattern)
    # Place the banners over the fireplace
    bannerHeight = highestPointUnderStructure+9
    bannerPos = [dest[0]-1 + (doorOffsetX[turnCount] * -2), dest[1]-1 + (doorOffsetZ[turnCount] * -2)]
    banner(level, bannerPos[0], bannerHeight, bannerPos[1], pattern, turnCountToBannerRotation[turnCount])
    # Randomize the color of the bed and the carpets surrounding it
    nextTurn = (turnCount + 1) % 4
    prevTurn = (turnCount - 1) % 4
    bedColor = random.randint(0, 15)
    bedHeight = highestPointUnderStructure+5
    bedPos = [dest[0]-1 + (doorOffsetX[turnCount] * 2), dest[1]-1 + (doorOffsetZ[turnCount] * 2)]
    placeBed(level, bedPos[0] + (doorOffsetX[prevTurn] * 3), bedHeight, bedPos[1] + (doorOffsetZ[prevTurn] * 3), bedColor, prevTurn)
    level.setBlockDataAt(bedPos[0] + (doorOffsetX[prevTurn] * 3) - (doorOffsetX[turnCount]), bedHeight, bedPos[1] + (doorOffsetZ[prevTurn] * 3) - (doorOffsetZ[turnCount]), bedColor)
    level.setBlockDataAt(bedPos[0] + (doorOffsetX[prevTurn] * 3) + (doorOffsetX[turnCount]), bedHeight, bedPos[1] + (doorOffsetZ[prevTurn] * 3) + (doorOffsetZ[turnCount]), bedColor)
    # Randomize the flowers in the flower beds
    otherOffset = [doorPos[0] + box.minx - (doorOffsetX[turnCount]*2), doorPos[1] + box.minz - (doorOffsetZ[turnCount]*2)]
    for j in xrange(2):
        flowerIndex = random.randint(0, 10)
        level.setBlockAt(otherOffset[0] + (doorOffsetZ[turnCount]*(2+j)), highestPointUnderStructure+5, otherOffset[1] + (doorOffsetX[turnCount]*(2+j)), 38)
        level.setBlockDataAt(otherOffset[0] + (doorOffsetZ[turnCount]*(2+j)), highestPointUnderStructure+5, otherOffset[1] + (doorOffsetX[turnCount]*(2+j)), flowerIndex)
        flowerIndex = random.randint(0, 10)
        level.setBlockAt(otherOffset[0] - (doorOffsetZ[turnCount]*(2+j)), highestPointUnderStructure+5, otherOffset[1] - (doorOffsetX[turnCount]*(2+j)), 38)
        level.setBlockDataAt(otherOffset[0] - (doorOffsetZ[turnCount]*(2+j)), highestPointUnderStructure+5, otherOffset[1] - (doorOffsetX[turnCount]*(2+j)), flowerIndex)

def placeHouse4(level, box, turnCount, completeHeightmap, completeHeightmapWithoutWater, pathfindingGrid, gridPos, dest, doorPositions, flagDir, resident):
    print("Turn Count: " + str(turnCount))
    footprint = [[0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    footprint = np.rot90(footprint, k=turnCount*3, axes=(0, 1))
    # Place some barriers on the pathfinding grid
    highestPointUnderStructure = 0
    for x in xrange(-6, 7):
        for y in xrange(-6, 7):
            if footprint[x + 6, y + 6] == 1:
                pathfindingGrid[int(gridPos.x) + x, int(gridPos.y) + y] = 255
                highestPointUnderStructure = max(highestPointUnderStructure, completeHeightmap[int(gridPos.x) + x, int(gridPos.y) + y])
    # Place the actual house
    placeHouse4Schematic(level, Vector(dest[0], highestPointUnderStructure, dest[1]), turnCount)

    # Append a point from the entrance of the house to the list of "doorPositions"
    prevTurn = (turnCount - 1) % 4
    nextTurn = (turnCount + 1) % 4
    doorPos = [int(math.floor(gridPos.x) + (doorOffsetX[turnCount] * 8) - (doorOffsetX[prevTurn] * 3)), int(math.floor(gridPos.y) + (doorOffsetZ[turnCount] * 8) - (doorOffsetZ[prevTurn] * 3))]
    doorPositions.append(doorPos)

    # Pillar to connect to the ground
    pillarToGround(level, box, completeHeightmapWithoutWater, highestPointUnderStructure, 6, 3, gridPos, [0, 0], footprint, [-6, -6], True)

    # Ladder to the ground
    ladderHeight = highestPointUnderStructure - 1
    while (ladderHeight >= completeHeightmap[doorPos[0], doorPos[1]]):
        level.setBlockAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, 65)
        level.setBlockDataAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, trapdoorLadderDirections[turnCount][0])
        if (level.blockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount]) == 0):
            level.setBlockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], 96)
            level.setBlockDataAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], trapdoorLadderDirections[turnCount][1])
        ladderHeight = ladderHeight - 1

    # Place the flag at the top of the house
    pattern = crestPatternGenerator(resident.lastName)
    flag(level, dest[0]-1 + (doorOffsetX[turnCount] * -3), highestPointUnderStructure+13, dest[1]-1 + (doorOffsetZ[turnCount] * -3), flagDir, pattern)
    # Place the banner
    bannerHeight = highestPointUnderStructure+8
    bannerPos = [dest[0]-1 + (doorOffsetX[turnCount] * -3) + (doorOffsetX[prevTurn] * 6), dest[1]-1 + (doorOffsetZ[turnCount] * -3) + (doorOffsetZ[prevTurn] * 6)]
    banner(level, bannerPos[0], bannerHeight, bannerPos[1], pattern, turnCountToBannerRotation[nextTurn])
    # Randomize the color of the bed and the carpets surrounding it
    bedColor = random.randint(0, 15)
    bedHeight = highestPointUnderStructure+5
    bedPos = [dest[0]-1 + (doorOffsetX[turnCount] * -3), dest[1]-1 + (doorOffsetZ[turnCount] * -3)]
    placeBed(level, bedPos[0] + (doorOffsetX[prevTurn] * -5), bedHeight, bedPos[1] + (doorOffsetZ[prevTurn] * -5), bedColor, nextTurn)
    level.setBlockDataAt(bedPos[0] + (doorOffsetX[prevTurn] * -5) - (doorOffsetX[turnCount]), bedHeight, bedPos[1] + (doorOffsetZ[prevTurn] * -5) - (doorOffsetZ[turnCount]), bedColor)
    level.setBlockDataAt(bedPos[0] + (doorOffsetX[prevTurn] * -5) + (doorOffsetX[turnCount]), bedHeight, bedPos[1] + (doorOffsetZ[prevTurn] * -5) + (doorOffsetZ[turnCount]), bedColor)

# This is basically just here so we can select a house placing function using an index
housePlacingFunctions = {
    0: placeHouse1,
    1: placeHouse2,
    2: placeHouse3,
    3: placeHouse4
}

def placeFarmBuilding(level, box, turnCount, completeHeightmap, completeHeightmapWithoutWater, pathfindingGrid, gridPos, doorPositions):
    print("Turn Count: " + str(turnCount))
    footprint = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]]
    footprint = np.rot90(footprint, k=turnCount*3, axes=(0, 1))
    # Place some barriers on the pathfinding grid
    if turnCount % 2 == 0:
        xRange = [-8, 9]
        zRange = [-9, 10]
    else: 
        xRange = [-9, 10]
        zRange = [-8, 9]
    highestPointUnderStructure = 0
    for x in xrange(xRange[0], xRange[1]):
        for y in xrange(zRange[0], zRange[1]):
            pathfindingGrid[int(gridPos[0]) + x, int(gridPos[1]) + y] = 255
            highestPointUnderStructure = max(highestPointUnderStructure, completeHeightmap[int(gridPos[0]) + x, int(gridPos[1]) + y])

    # Place the actual building
    placeFarmBuildingSchematic(level, Vector(gridPos[0] + box.minx - doorOffsetX[turnCount], highestPointUnderStructure, gridPos[1] + box.minz - doorOffsetZ[turnCount]), turnCount)

    # Append a point from the entrance of the house to the list of "doorPositions"
    prevTurn = (turnCount - 1) % 4
    doorPos = [int(math.floor(gridPos[0]) + (doorOffsetX[turnCount] * 9)), int(math.floor(gridPos[1]) + (doorOffsetZ[turnCount] * 9))]
    doorPositions.append(doorPos)

    # Pillar to connect to the ground
    pillarToGround(level, box, completeHeightmapWithoutWater, highestPointUnderStructure, 6, 3, Vec2(gridPos[0], gridPos[1]), [0, 0], footprint, [-6, -6], True)

    # Ladder to the ground
    ladderHeight = highestPointUnderStructure - 1
    while (ladderHeight >= completeHeightmap[doorPos[0], doorPos[1]]):
        level.setBlockAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, 65)
        level.setBlockDataAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, trapdoorLadderDirections[turnCount][0])
        if (level.blockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount]) == 0):
            level.setBlockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], 96)
            level.setBlockDataAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], trapdoorLadderDirections[turnCount][1])
        ladderHeight = ladderHeight - 1

def placeNetherTemple(level, box, turnCount, completeHeightmap, completeHeightmapWithoutWater, pathfindingGrid, gridPos, doorPositions):
    print("Turn Count: " + str(turnCount))
    footprint = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    footprint = footprint = np.rot90(footprint, k=turnCount*3, axes=(0, 1))
    # Place some barriers on the pathfinding grid
    if turnCount % 2 == 0:
        xRange = [-14, 15]
        zRange = [-11, 12]
    else: 
        xRange = [-11, 12]
        zRange = [-14, 15]
    highestPointUnderStructure = 0
    for x in xrange(xRange[0], xRange[1]):
        for y in xrange(zRange[0], zRange[1]):
            if footprint[x + abs(xRange[0]), y + abs(zRange[0])] == 1:
                pathfindingGrid[int(gridPos[0]) + x, int(gridPos[1]) + y] = 255
                highestPointUnderStructure = max(highestPointUnderStructure, completeHeightmap[int(gridPos[0]) + x, int(gridPos[1]) + y])
    # Place the actual structure
    placeNetherTempleSchematic(level, Vector(gridPos[0] + box.minx+1, highestPointUnderStructure, gridPos[1] + box.minz+1), turnCount)
    # Append a point from the entrance of the structure to the list of "doorPositions"
    doorPos = [int(gridPos[0] + (doorOffsetX[turnCount]) * 15), int(gridPos[1] + (doorOffsetZ[turnCount] * 15))]
    doorPositions.append(doorPos)
    # Pillar to connect to the ground
    pillarToGround(level, box, completeHeightmapWithoutWater, highestPointUnderStructure, 10, 6, Vec2(gridPos[0], gridPos[1]), [0, 0], footprint, [xRange[0], zRange[0]], True)
    # Ladder to the ground
    ladderHeight = highestPointUnderStructure - 1
    while (ladderHeight >= completeHeightmap[doorPos[0], doorPos[1]]):
        level.setBlockAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, 65)
        level.setBlockDataAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, trapdoorLadderDirections[turnCount][0])
        if (level.blockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minx - doorOffsetZ[turnCount]) == 0):
            level.setBlockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], 96)
            level.setBlockDataAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], trapdoorLadderDirections[turnCount][1])
        ladderHeight = ladderHeight - 1

def placeLoreShrine(level, box, completeHeightmap, completeHeightmapWithoutWater, pathfindingGrid, gridPos, dest):
    # Place some barriers on the pathfinding grid
    highestPointUnderStructure = 0
    for x in xrange(-3, 4):
        for y in xrange(-3, 4):
            pathfindingGrid[int(gridPos.x) + x, int(gridPos.y) + y] = 255
            highestPointUnderStructure = max(highestPointUnderStructure, completeHeightmap[int(gridPos.x) + x, int(gridPos.y) + y])
    # Place the actual house
    placeLoreShrineSchematic(level, Vector(dest[0], highestPointUnderStructure, dest[1]))
    # Pillar to connect to the ground
    for x in xrange(-3, 4):
        for z in xrange(-3, 4):
            yThatIsBeingChecked = highestPointUnderStructure - 1
            while (yThatIsBeingChecked >= completeHeightmapWithoutWater[int(gridPos.x) + x, int(gridPos.y) + z]):
                level.setBlockAt(int(gridPos.x) + x + box.minx, yThatIsBeingChecked, int(gridPos.y) + z + box.minz, 4)
                level.setBlockDataAt(int(gridPos.x) + x + box.minx, yThatIsBeingChecked, int(gridPos.y) + z + box.minz, 0)
                yThatIsBeingChecked = yThatIsBeingChecked - 1



# All of the "placeXYZSchematic" functions are basically just there to account for the offsets of each individual structure

def placeHouse1Schematic(level, destination, dir):
    filename = "./stock-filters/GDMCSchematics/house_01.schematic"
    schematic = MCSchematic(shape=(15,18,14),filename=filename)
    for i in xrange(dir):
        schematic.rotateLeft()
    offset = None
    if dir % 2 == 1:
        offset = Vector(-8, 0, -10)
    else:
        offset = Vector(-10, 0, -8)
    level.copyBlocksFrom(schematic, schematic.bounds, destination + offset)

def placeHouse2Schematic(level, destination, dir):
    filename = "./stock-filters/GDMCSchematics/house_02.schematic"
    schematic = MCSchematic(shape=(15,18,14),filename=filename)
    for i in xrange(dir):
        schematic.rotateLeft()
    offset = Vector(-9, 0, -9)
    level.copyBlocksFrom(schematic, schematic.bounds, destination + offset)

def placeHouse3Schematic(level, destination, dir):
    filename = "./stock-filters/GDMCSchematics/house_03.schematic"
    schematic = MCSchematic(shape=(15,18,14),filename=filename)
    for i in xrange(dir):
        schematic.rotateLeft()
    offset = Vector(-7, 0, -7)
    level.copyBlocksFrom(schematic, schematic.bounds, destination + offset)

def placeHouse4Schematic(level, destination, dir):
    filename = "./stock-filters/GDMCSchematics/backsmithBuilding.schematic"
    schematic = MCSchematic(shape=(17,13,17),filename=filename)
    for i in xrange(dir):
        schematic.rotateLeft()
    offset = Vector(-9, 0, -9)
    level.copyBlocksFrom(schematic, schematic.bounds, destination + offset)

def placeFarmBuildingSchematic(level, destination, dir):
    filename = "./stock-filters/GDMCSchematics/farmBuilding.schematic"
    schematic = MCSchematic(shape=(19,13,19),filename=filename)
    for i in xrange(dir):
        schematic.rotateLeft()
    offset = Vector(-9, 0, -9)
    level.copyBlocksFrom(schematic, schematic.bounds, destination + offset)

def placeNetherTempleSchematic(level, destination, dir):
    filename = "./stock-filters/GDMCSchematics/netherTemple.schematic"
    schematic = MCSchematic(shape=(23,14,29),filename=filename)
    for i in xrange(dir):
        schematic.rotateLeft()
    offset = None
    if dir % 2 == 1:
        offset = Vector(-12, 0, -15)
    else:
        offset = Vector(-15, 0, -12)
    level.copyBlocksFrom(schematic, schematic.bounds, destination + offset)

def placeLoreShrineSchematic(level, destination):
    filename = "./stock-filters/GDMCSchematics/loreShrine.schematic"
    schematic = MCSchematic(shape=(7,7,7),filename=filename)
    offset = Vector(-3, 0, -3)
    level.copyBlocksFrom(schematic, schematic.bounds, destination + offset)

def placeStreetLightSchematic(level, destination):
    filename = "./stock-filters/GDMCSchematics/streetLight.schematic"
    schematic = MCSchematic(shape=(1,6,1),filename=filename)
    level.copyBlocksFrom(schematic, schematic.bounds, destination)



def flag(level, x, y, z, flagDir, pattern):
    print("Flag")
    print("X: " + str(x) + ", Y: " + str(y) + ", Z: " + str(z))
    # Place some fences to act as the flag pole
    level.setBlockAt(x, y, z, 188)
    level.setBlockAt(x, y+1, z, 188)
    # Build the flag in the direction specified with the pattern
    flagX = 1 if flagDir > 1 else -1
    flagZ = 1 if flagDir % 2 else -1
    for i in xrange(3):
        for j in xrange(2):
            level.setBlockAt(x + (flagX*i), y + 2 + j, z + (flagZ*i), 35)
            level.setBlockDataAt(x + (flagX*i), y + 2 + j, z + (flagZ*i), 15 - pattern[i][j])

def banner(level, x, y, z, pattern, direction):
    # Create the new Tile Entity
    level.setBlockAt(x, y, z, 177)
    level.setBlockDataAt(x, y, z, direction)
    banner = TileEntity.Create("minecraft:banner")
    TileEntity.setpos(banner, (x, y, z))
    # Set the pattern
    banner["Base"] = TAG_Int(pattern[1][1])
    patterns = [TAG_Compound({}), TAG_Compound({}), TAG_Compound({}), TAG_Compound({}), TAG_Compound({})]
    patterns[0]["Pattern"] = TAG_String(u'vh')
    patterns[0]["Color"] = TAG_Int(pattern[1][0])
    patterns[1]["Pattern"] = TAG_String(u'tl')
    patterns[1]["Color"] = TAG_Int(pattern[0][0])
    patterns[2]["Pattern"] = TAG_String(u'tr')
    patterns[2]["Color"] = TAG_Int(pattern[0][1])
    patterns[3]["Pattern"] = TAG_String(u'bl')
    patterns[3]["Color"] = TAG_Int(pattern[2][0])
    patterns[4]["Pattern"] = TAG_String(u'br')
    patterns[4]["Color"] = TAG_Int(pattern[2][1])
    banner["Patterns"] = TAG_List(patterns)
    # Add the Tile Entity to the chunk
    chunk = level.getChunk(math.floor((x)/16), math.floor((z)/16))
    chunk.TileEntities.append(banner)

def placeBed(level, x, y, z, color, direction):
    # The top part of the bed
    level.setBlockAt(x, y, z, 26)
    level.setBlockDataAt(x, y, z, 3-direction)
    bedTop = TileEntity.Create("minecraft:bed")
    TileEntity.setpos(bedTop, (x, y, z))
    bedTop["color"] = TAG_Int(color)
    # The bottom part of the bed
    level.setBlockAt(x + (doorOffsetX[direction]), y, z + (doorOffsetZ[direction]), 26)
    level.setBlockDataAt(x + (doorOffsetX[direction]), y, z + (doorOffsetZ[direction]), 11-direction)
    bedBottom = TileEntity.Create("minecraft:bed")
    TileEntity.setpos(bedBottom, (x + (doorOffsetX[direction]), y, z + (doorOffsetZ[direction])))
    bedBottom["color"] = TAG_Int(color)
    # Add the Tile Entities to the chunk
    chunk = level.getChunk(math.floor((x)/16), math.floor((z)/16))
    chunk.TileEntities.append(bedTop)
    chunk.TileEntities.append(bedBottom)


def generateCemetary(level, box, mainSettlement, completeHeightmap, completeHeightmapWithoutWater, offset):
    global chunks
    global boundingBox
    chunks = []
    boundingBox = box
    generations = 3
    settlement = mainSettlement

    # Get the highest point under the structure
    highestPoint = 0
    for x in xrange(box.minx, box.maxx):
        for z in xrange(box.minz, box.maxz):
            highestPoint = max(highestPoint, completeHeightmap[x + offset[0] - box.minx, z + offset[1] - box.minz])

    y = highestPoint + 3
    for x in xrange(box.minx, box.maxx):
        for z in xrange(box.minz, box.maxz):
            # Bottom of the cemetary structure
            level.setBlockAt(x, y-2, z, 98)
            level.setBlockDataAt(x, y-2, z, 0)
            if x == box.minx or x == box.maxx-1 or z == box.minz or z == box.maxz-1:
                # Walls / fence
                level.setBlockAt(x, y-1, z, 98)
                level.setBlockDataAt(x, y-1, z, 0)
                level.setBlockAt(x, y, z, 98)
                level.setBlockDataAt(x, y, z, 0)
                level.setBlockAt(x, y+1, z, 139)
                level.setBlockDataAt(x, y+1, z, 0)
                level.setBlockAt(x, y+2, z, 101)
                level.setBlockDataAt(x, y+2, z, 0)
                level.setBlockAt(x, y+3, z, 101)
                level.setBlockDataAt(x, y+3, z, 0)
            else:
                # Grass / dirt
                level.setBlockAt(x, y-1, z, 3)
                level.setBlockAt(x, y, z, 2)
                level.setBlockDataAt(x, y, z, 0)
                level.setBlockAt(x, y+1, z, 0)
                level.setBlockAt(x, y+2, z, 0)
                level.setBlockAt(x, y+3, z, 0)
                level.setBlockAt(x, y+4, z, 0)        

    # Corner posts
    for i in xrange(5):
        level.setBlockAt(box.minx, y+i, box.minz, 98)
        level.setBlockAt(box.maxx-1, y+i, box.minz, 98)
        level.setBlockAt(box.maxx-1, y+i, box.maxz-1, 98)
        level.setBlockAt(box.minx, y+i, box.maxz-1, 98)
    
    # Pillars to the ground
    pillarToGround(level, box, completeHeightmapWithoutWater, highestPoint+1, 11, 7, Vec2(10, 10), [4, 176], [], [], False)
    pillarToGround(level, box, completeHeightmapWithoutWater, highestPoint+1, 11, 7, Vec2(65, 10), [4, 176], [], [], False)
    pillarToGround(level, box, completeHeightmapWithoutWater, highestPoint+1, 11, 7, Vec2(10, 65), [4, 176], [], [], False)
    pillarToGround(level, box, completeHeightmapWithoutWater, highestPoint+1, 11, 7, Vec2(65, 65), [4, 176], [], [], False)

    # Ladder to the ground
    ladderHeight = highestPoint + 3
    turnCount = 0
    doorPos = [76, 40]
    while (ladderHeight >= completeHeightmap[doorPos[0] + offset[0], doorPos[1] + offset[1]]):
        level.setBlockAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, 65)
        level.setBlockDataAt(doorPos[0] + box.minx, ladderHeight, doorPos[1] + box.minz, trapdoorLadderDirections[turnCount][0])
        if (level.blockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount]) == 0):
            level.setBlockAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], 96)
            level.setBlockDataAt(doorPos[0] + box.minx - doorOffsetX[turnCount], ladderHeight, doorPos[1] + box.minz - doorOffsetZ[turnCount], trapdoorLadderDirections[turnCount][1])
        ladderHeight = ladderHeight - 1

    # Get a list of all dead people
    allDeadPeople = []
    for i in xrange(generations):
        for j in xrange(len(settlement.families)):
            for k in xrange(len(settlement.families[j].members[i])):
                allDeadPeople.append(settlement.families[j].members[i][k])

    # Place a tombstone for each dead person (that can fit in the cemetary)
    personCounter = 0
    for i in xrange(1, int((box.maxx - box.minx)/4) - 1):
        for j in xrange(1, int((box.maxz - box.minz)/4)):
            if personCounter < len(allDeadPeople):
                tombstone(level, box.minx + (i*4), y, box.minz + (j*4), allDeadPeople[personCounter])
                personCounter += 1
    print(settlement.getCurrentGeneration())
    print(str(personCounter) + " people in the cemetary")
    return highestPoint
 
def tombstone(level, x, y, z, person):
    # Place the blocks for the tombstone
    level.setBlockAt(x, y, z, 98)
    level.setBlockAt(x, y+1, z, 98)
    level.setBlockAt(x, y+2, z, 98)
    level.setBlockAt(x, y+3, z, 98)
    level.setBlockAt(x, y+4, z, 50)
    level.setBlockDataAt(x, y+4, z, 5)
    level.setBlockAt(x+1, y+1, z, 109)
    level.setBlockDataAt(x+1, y+1, z, 1)
    # Place the sign
    level.setBlockAt(x+2, y+1, z, 68)
    level.setBlockDataAt(x+2, y+1, z, 5)
    sign = TileEntity.Create("minecraft:sign")
    TileEntity.setpos(sign, (x+2, y+1, z))
    parentText = "Parents unknown" if (person.parent1 == None) else ("Child of " + person.parent1.firstName)
    childText = "No known children" if (len(person.children) == 0) else ("Parent of " + person.children[0].firstName)
    sign["Text1"] = TAG_String(u'{"text":"Here lies"}')
    sign["Text2"] = TAG_String(u'{"text":"' + person.firstName + " " + person.lastName + '"}')
    sign["Text3"] = TAG_String(u'{"text":"' + childText + '"}')
    sign["Text4"] = TAG_String(u'{"text":"' + parentText + '"}')
    chunk = level.getChunk(math.floor((x+2)/16), math.floor((z)/16))
    chunk.TileEntities.append(sign)
    # Place the banner
    level.setBlockAt(x+1, y+3, z, 177)
    level.setBlockDataAt(x+1, y+3, z, 5)
    banner = TileEntity.Create("minecraft:banner")
    TileEntity.setpos(banner, (x+1, y+3, z))
    pattern = crestPatternGenerator(person.lastName)
    banner["Base"] = TAG_Int(pattern[1][1])
    patterns = [TAG_Compound({}), TAG_Compound({}), TAG_Compound({}), TAG_Compound({}), TAG_Compound({})]
    patterns[0]["Pattern"] = TAG_String(u'vh')
    patterns[0]["Color"] = TAG_Int(pattern[1][0])
    patterns[1]["Pattern"] = TAG_String(u'tl')
    patterns[1]["Color"] = TAG_Int(pattern[0][0])
    patterns[2]["Pattern"] = TAG_String(u'tr')
    patterns[2]["Color"] = TAG_Int(pattern[0][1])
    patterns[3]["Pattern"] = TAG_String(u'bl')
    patterns[3]["Color"] = TAG_Int(pattern[2][0])
    patterns[4]["Pattern"] = TAG_String(u'br')
    patterns[4]["Color"] = TAG_Int(pattern[2][1])
    banner["Patterns"] = TAG_List(patterns)
    chunk = level.getChunk(math.floor((x+1)/16), math.floor((z)/16))
    chunk.TileEntities.append(banner)
    # Reseed the randomness of the program
    random.seed(datetime.now())

def placeCemetaryGateSchematic(level, destination):
    filename = "./stock-filters/GDMCSchematics/cemetaryGate.schematic"
    schematic = MCSchematic(shape=(3,5,6),filename=filename)
    level.copyBlocksFrom(schematic, schematic.bounds, destination)


def pillarToGround(level, box, completeHeightmapWithoutWater, highestPointUnderStructure, topWidth, mainWidth, gridPos, offset, footprint, footprintOffset, footprintNeeded):
    # Pillar to connect to the ground
    for x in xrange((mainWidth * -1 + 1), mainWidth):
        for z in xrange((mainWidth * -1 + 1), mainWidth):
            yThatIsBeingChecked = highestPointUnderStructure - 1
            while (yThatIsBeingChecked >= completeHeightmapWithoutWater[int(gridPos.x) + x + offset[0], int(gridPos.y) + z + offset[1]]):
                level.setBlockAt(int(gridPos.x) + x + box.minx, yThatIsBeingChecked, int(gridPos.y) + z + box.minz, 4)
                level.setBlockDataAt(int(gridPos.x) + x + box.minx, yThatIsBeingChecked, int(gridPos.y) + z + box.minz, 0)
                yThatIsBeingChecked = yThatIsBeingChecked - 1
    pillarTopThingHeight = 1
    # Fancy top part that decreases in size as it goes down
    for radius in xrange(topWidth, mainWidth, -1):
        for x in xrange((radius * -1) + 1, radius):
            for z in xrange((radius * -1) + 1, radius):
                fitsInFootprint = not footprintNeeded or footprint[x + abs(footprintOffset[0]), z + abs(footprintOffset[1])] == 1
                if (completeHeightmapWithoutWater[int(gridPos.x) + x + offset[0], int(gridPos.y) + z + offset[1]] <= highestPointUnderStructure - pillarTopThingHeight and (fitsInFootprint)):
                    level.setBlockAt(int(gridPos.x) + x + box.minx, highestPointUnderStructure - pillarTopThingHeight, int(gridPos.y) + z + box.minz, 4)
                    level.setBlockDataAt(int(gridPos.x) + x + box.minx, highestPointUnderStructure - pillarTopThingHeight, int(gridPos.y) + z + box.minz, 0)
        pillarTopThingHeight = pillarTopThingHeight + 1