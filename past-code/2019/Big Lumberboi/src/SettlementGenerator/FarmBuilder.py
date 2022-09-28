from random import randint

from BiomeMaterials import get_biome_materials
from Classes import Point
from Common import setBlock
from RemoveTree import removeTree
from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float

def buildFarm(level, surface, prop):
	if prop.height > 90:
		return
	getMaterials(surface, prop)
	if randint(0, 9) < 6:
		buildPatch(level, surface, prop)
	else:
		buildAnimalPen(level, surface, prop)

def buildPatch(level, surface, prop):
	buildField(level, surface, prop)
	buildSides(level, surface, prop)

def clearFarmProperty(level, surface, prop):
	for x in range(prop.xStart, prop.xEnd):
		for z in range(prop.zStart, prop.zEnd):
			for y in range(prop.height + 2, prop.height + 4):
				removeTree(level, x + surface.xStart, y, z + surface.zStart)
				setBlock(level, surface, x, y, z, 0)

def buildField(level, surface, prop):
	y = prop.height + 1
	for x in range(prop.xStart + 1, prop.xEnd - 1):
		for z in range(prop.zStart + 1, prop.zEnd - 1):
			setBlock(level, surface, x, y, z, 60)
			setBlock(level, surface, x, y + 1, z, 59, 7)

	setBlock(level, surface, prop.xStart + prop.xLength / 2, y, prop.zStart + prop.zLength / 2, 9)
	setBlock(level, surface, prop.xStart + prop.xLength / 2, y + 1, prop.zStart + prop.zLength / 2, 0)

def buildSides(level, surface, prop):
	# Corners
	y = prop.height + 1
	for p in [(prop.xStart, prop.zStart), (prop.xStart, prop.zEnd - 1), (prop.xEnd - 1, prop.zStart), (prop.xEnd - 1, prop.zEnd - 1)]:
		setBlock(level, surface, p[0], y, p[1], materials["wood"]["default"])
		setBlock(level, surface, p[0], y + 1, p[1], materials["wood"]["default"])
		setBlock(level, surface, p[0], y + 2, p[1], materials["torch"]["default"])

	buildNorthSide(level, surface, prop)
	buildEastSide(level, surface, prop)
	buildSouthSide(level, surface, prop)
	buildWestSide(level, surface, prop)

def buildNorthSide(level, surface, prop):
	y = prop.height + 1
	if prop.doorDirection == "NORTH":
		setBlock(level, surface, prop.xStart + 1, y, prop.zStart, materials["wood_planks"]["default"])
		setBlock(level, surface, prop.xStart + 1, y + 1, prop.zStart, materials["fence"]["default"])
		setBlock(level, surface, prop.xEnd - 2, y, prop.zStart, materials["wood_planks"]["default"])
		setBlock(level, surface, prop.xEnd - 2, y + 1, prop.zStart, materials["fence"]["default"])
		for x in range(prop.xStart + 2, prop.xEnd - 2):
			if isSurfaceBlock(level, x + surface.xStart, y, prop.zStart - 1 + surface.zStart):
				setBlock(level, surface, x, y, prop.zStart, materials["wood_planks"]["default"])
			else:
				setBlock(level, surface, x, y, prop.zStart, materials["wood_planks"]["directions"]["south"]["bottom"])
	else:
		for x in range(prop.xStart + 1, prop.xEnd - 1):
			setBlock(level, surface, x, y, prop.zStart, materials["wood_planks"]["default"])
			setBlock(level, surface, x, y + 1, prop.zStart, materials["fence"]["default"])

def buildEastSide(level, surface, prop):
	y = prop.height + 1
	if prop.doorDirection == "EAST":
		setBlock(level, surface, prop.xEnd - 1, y, prop.zStart + 1, materials["wood_planks"]["default"])
		setBlock(level, surface, prop.xEnd - 1, y + 1, prop.zStart + 1, materials["fence"]["default"])
		setBlock(level, surface, prop.xEnd - 1, y, prop.zEnd - 2, materials["wood_planks"]["default"])
		setBlock(level, surface, prop.xEnd - 1, y + 1, prop.zEnd - 2, materials["fence"]["default"])
		for z in range(prop.zStart + 2, prop.zEnd - 2):
			if isSurfaceBlock(level, prop.xEnd + surface.xStart, y, z + surface.zStart):
				setBlock(level, surface, prop.xEnd - 1, y, z, materials["wood_planks"]["default"])
			else:
				setBlock(level, surface, prop.xEnd - 1, y, z, materials["wood_planks"]["directions"]["west"]["bottom"])
	else:
		for z in range(prop.zStart + 1, prop.zEnd - 1):
			setBlock(level, surface, prop.xEnd - 1, y, z, materials["wood_planks"]["default"])
			setBlock(level, surface, prop.xEnd - 1, y + 1, z, materials["fence"]["default"])

def buildSouthSide(level, surface, prop):
	y = prop.height + 1
	if prop.doorDirection == "SOUTH":
		setBlock(level, surface, prop.xStart + 1, y, prop.zEnd - 1, materials["wood_planks"]["default"])
		setBlock(level, surface, prop.xStart + 1, y + 1, prop.zEnd - 1, materials["fence"]["default"])
		setBlock(level, surface, prop.xEnd - 2, y, prop.zEnd - 1, materials["wood_planks"]["default"])
		setBlock(level, surface, prop.xEnd - 2, y + 1, prop.zEnd - 1, materials["fence"]["default"])
		for x in range(prop.xStart + 2, prop.xEnd - 2):
			if isSurfaceBlock(level, x + surface.xStart, y, prop.zEnd + surface.zStart):
				setBlock(level, surface, x, y, prop.zEnd - 1, materials["wood_planks"]["default"])
			else:
				setBlock(level, surface, x, y, prop.zEnd - 1, materials["wood_planks"]["directions"]["north"]["bottom"])
	else:
		for x in range(prop.xStart + 1, prop.xEnd - 1):
			setBlock(level, surface, x, y, prop.zEnd - 1, materials["wood_planks"]["default"])
			setBlock(level, surface, x, y + 1, prop.zEnd - 1, materials["fence"]["default"])

def buildWestSide(level, surface, prop):
	y = prop.height + 1
	if prop.doorDirection == "WEST":
		setBlock(level, surface, prop.xStart, y, prop.zStart + 1, materials["wood_planks"]["default"])
		setBlock(level, surface, prop.xStart, y + 1, prop.zStart + 1, materials["fence"]["default"])
		setBlock(level, surface, prop.xStart, y, prop.zEnd - 2, materials["wood_planks"]["default"])
		setBlock(level, surface, prop.xStart, y + 1, prop.zEnd - 2, materials["fence"]["default"])
		for z in range(prop.zStart + 2, prop.zEnd - 2):
			if isSurfaceBlock(level, prop.xStart - 1 + surface.xStart, y, z + surface.zStart):
				setBlock(level, surface, prop.xStart, y, z, materials["wood_planks"]["default"])
			else:
				setBlock(level, surface, prop.xStart, y, z, materials["wood_planks"]["directions"]["east"]["bottom"])
	else:
		for z in range(prop.zStart + 1, prop.zEnd - 1):
			setBlock(level, surface, prop.xStart, y, z, materials["wood_planks"]["default"])
			setBlock(level, surface, prop.xStart, y + 1, z, materials["fence"]["default"])

aboveSurfaceBlocks = [0, 6, 17, 18, 31, 32, 37, 38, 39, 40, 59, 78, 81, 83, 99, 100, 103, 104, 105, 106, 111, 141, 142, 161, 162, 175]
def isSurfaceBlock(level, x, y, z):
	for block in aboveSurfaceBlocks:
		if level.blockAt(x, y, z) == block:
			return False
	return True

def getMaterials(surface, prop):
	biomeId = surface.surfaceMap[prop.xStart][prop.zStart].biomeId

	global materials
	materials = get_biome_materials(biomeId)

def buildAnimalPen(level, surface, prop):
	# Grass
	y = prop.height + 1
	for x in range(prop.xStart + 1, prop.xEnd - 1):
		for z in range(prop.zStart + 1, prop.zEnd - 1):
			setBlock(level, surface, x, y, z, 2)

	# Fence
	for x in range(prop.xStart, prop.xEnd):
		setBlock(level, surface, x, y, prop.zStart, 4)
		setBlock(level, surface, x, y + 1, prop.zStart, materials["fence"]["default"])
		setBlock(level, surface, x, y, prop.zEnd - 1, 4)
		setBlock(level, surface, x, y + 1, prop.zEnd - 1, materials["fence"]["default"])
	for z in range(prop.zStart + 1, prop.zEnd - 1):
		setBlock(level, surface, prop.xStart, y, z, 4)
		setBlock(level, surface, prop.xStart, y + 1, z, materials["fence"]["default"])
		setBlock(level, surface, prop.xEnd - 1, y, z, 4)
		setBlock(level, surface, prop.xEnd - 1, y + 1, z, materials["fence"]["default"])

	# Torches
	setBlock(level, surface, prop.xStart, y + 2, prop.zStart, 50, 5)
	setBlock(level, surface, prop.xStart, y + 2, prop.zEnd - 1, 50, 5)
	setBlock(level, surface, prop.xEnd - 1, y + 2, prop.zStart, 50, 5)
	setBlock(level, surface, prop.xEnd - 1, y + 2, prop.zEnd - 1, 50, 5)

	# Gate
	if prop.doorDirection == "NORTH":
		x = prop.xStart + prop.xLength / 2
		setBlock(level, surface, x, y + 1, prop.zStart, 107, 0)
		if isSurfaceBlock(level, x + surface.xStart, y, prop.zStart - 1 + surface.zStart):
			setBlock(level, surface, x, y, prop.zStart, 4)
		else:
			setBlock(level, surface, x, y, prop.zStart, 67, 2)
	if prop.doorDirection == "EAST":
		z = prop.zStart + prop.zLength / 2
		setBlock(level, surface, prop.xEnd - 1, y + 1, z, 107, 1)
		if isSurfaceBlock(level, prop.xEnd + surface.xStart, y, z + surface.zStart):
			setBlock(level, surface, prop.xEnd - 1, y, z, 4)
		else:
			setBlock(level, surface, prop.xEnd - 1, y, z, 67, 1)
	if prop.doorDirection == "SOUTH":
		x = prop.xStart + prop.xLength / 2
		setBlock(level, surface, x, y + 1, prop.zEnd - 1, 107, 2)
		if isSurfaceBlock(level, x + surface.xStart, y, prop.zEnd + surface.zStart):
			setBlock(level, surface, x, y, prop.zEnd - 1, 4)
		else:
			setBlock(level, surface, x, y, prop.zEnd - 1, 67, 3)
	if prop.doorDirection == "WEST":
		z = prop.zStart + prop.zLength / 2
		setBlock(level, surface, prop.xStart, y + 1, z, 107, 3)
		if isSurfaceBlock(level, prop.xStart - 1 + surface.xStart, y, z + surface.zStart):
			setBlock(level, surface, prop.xStart, y, z, 4)
		else:
			setBlock(level, surface, prop.xStart, y, z, 67, 0)

	# Animals
	amount = (prop.xLength * prop.zLength) / 12
	kind = None
	a = randint(0, 12)
	if a < 1:
		kind = "HORSE"
	elif a < 4:
		kind = "CHICKEN"
	elif a < 7:
		kind = "PIG"
	elif a < 10:
		kind = "COW"
	else:
		kind = "SHEEP"

	points = []
	for _ in range(amount):
		points.append(getRandomPoint(surface, prop, points))

	if kind == "HORSE":
		for p in points:
			placeHorse(level, p.x + surface.xStart, y + 1, p.z + surface.zStart)
	elif kind == "CHICKEN":
		for p in points:
			placeChicken(level, p.x + surface.xStart, y + 1, p.z + surface.zStart)
	elif kind == "PIG":
		for p in points:
			placePig(level, p.x + surface.xStart, y + 1, p.z + surface.zStart)
	elif kind == "COW":
		for p in points:
			placeCow(level, p.x + surface.xStart, y + 1, p.z + surface.zStart)
	elif kind == "SHEEP":
		for p in points:
			placeSheep(level, p.x + surface.xStart, y + 1, p.z + surface.zStart)

def getRandomPoint(surface, prop, points):
	x = randint(prop.xStart + 1, prop.xEnd - 2)
	z = randint(prop.zStart + 1, prop.zEnd - 2)
	p = Point(x, z)
	while contain(points, p):
		x = randint(prop.xStart + 1, prop.xEnd - 2)
		z = randint(prop.zStart + 1, prop.zEnd - 2)
		p = Point(x, z)
	return p

def contain(points, point):
	for p in points:
		if p.x == point.x and p.z == point.z:
			return True
	return False

def placeHorse(level, x, y, z):
    horse = TAG_Compound()
    horse["id"] = TAG_String("horse")
    horse["Pos"] = TAG_List([TAG_Double(x + 0.5), TAG_Double(y), TAG_Double(z + 0.5)])

    chunk = level.getChunk(x / 16, z / 16)
    chunk.Entities.append(horse)
    chunk.dirty = True

def placeChicken(level, x, y, z):
    chicken = TAG_Compound()
    chicken["id"] = TAG_String("chicken")
    chicken["Pos"] = TAG_List([TAG_Double(x + 0.5), TAG_Double(y), TAG_Double(z + 0.5)])

    chunk = level.getChunk(x / 16, z / 16)
    chunk.Entities.append(chicken)
    chunk.dirty = True

def placePig(level, x, y, z):
    pig = TAG_Compound()
    pig["id"] = TAG_String("pig")
    pig["Pos"] = TAG_List([TAG_Double(x + 0.5), TAG_Double(y), TAG_Double(z + 0.5)])

    chunk = level.getChunk(x / 16, z / 16)
    chunk.Entities.append(pig)
    chunk.dirty = True

def placeCow(level, x, y, z):
    cow = TAG_Compound()
    cow["id"] = TAG_String("cow")
    cow["Pos"] = TAG_List([TAG_Double(x + 0.5), TAG_Double(y), TAG_Double(z + 0.5)])

    chunk = level.getChunk(x / 16, z / 16)
    chunk.Entities.append(cow)
    chunk.dirty = True

def placeSheep(level, x, y, z):
    sheep = TAG_Compound()
    sheep["id"] = TAG_String("sheep")
    sheep["Pos"] = TAG_List([TAG_Double(x + 0.5), TAG_Double(y), TAG_Double(z + 0.5)])

    chunk = level.getChunk(x / 16, z / 16)
    chunk.Entities.append(sheep)
    chunk.dirty = True