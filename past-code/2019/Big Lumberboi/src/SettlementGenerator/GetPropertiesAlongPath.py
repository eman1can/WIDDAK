import math
from Classes import Property
from Common import isWithinBorder
from GetRectangle import getRectangle

gap = 8
def getPropertiesAlongPath(surface, path, minSize, maxSize, distanceFromPath):
	minSize += 2
	maxSize += 2
	properties = []
	for i, point in enumerate(path):
		if i % gap != 0:
			continue
		for p in [(point.x + distanceFromPath, point.z, "WEST"), (point.x - distanceFromPath, point.z, "EAST"), (point.x, point.z + distanceFromPath, "NORTH"), (point.x, point.z - distanceFromPath, "SOUTH")]:
			x = p[0]
			z = p[1]
			doorDirection = p[2]
			if not isWithinBorder(surface, x, z) or surface.surfaceMap[x][z].isOccupied or surface.surfaceMap[x][z].isWater or isGreatHeightDifference(surface, point.x, point.z, x, z):
				continue
			prop = getProperty(surface, x, z, minSize, maxSize)
			if prop:
				prop.doorDirection = doorDirection
				setPathwayStart(prop)
				setPathwayEnd(path, i, prop)
				properties.append(prop)
				occupyArea(surface, prop.xStart, prop.zStart, prop.xEnd, prop.zEnd)

	# Decreases the size again to decrease the compactness of the properties
	for p in properties:
		decreaseProperty(surface, p)

	return properties

def isGreatHeightDifference(surface, x1, z1, x2, z2):
	height1 = surface.surfaceMap[x1][z1].height
	height2 = surface.surfaceMap[x2][z2].height
	return abs(height1 - height2) > 3

def getProperty(surface, x, z, minSize, maxSize):
	rec = getRectangle(surface, x, z, 1, maxSize)
	if rec.xLength >= minSize and rec.zLength >= minSize:
		height = surface.surfaceMap[x][z].height
		return Property(rec.xStart, rec.zStart, rec.xEnd, rec.zEnd, height)
	return None

def setPathwayStart(prop):
	if prop.doorDirection == "NORTH":
		prop.xPathwayStart = prop.xStart + prop.xLength / 2
		prop.zPathwayStart = prop.zStart
	elif prop.doorDirection == "EAST":
		prop.xPathwayStart = prop.xEnd - 1
		prop.zPathwayStart = prop.zStart + prop.zLength / 2
	elif prop.doorDirection == "SOUTH":
		prop.xPathwayStart = prop.xStart + prop.xLength / 2
		prop.zPathwayStart = prop.zEnd - 1
	elif prop.doorDirection == "WEST":
		prop.xPathwayStart = prop.xStart
		prop.zPathwayStart = prop.zStart + prop.zLength / 2

def occupyArea(surface, xStart, zStart, xEnd, zEnd):
	for x in range(xStart, xEnd):
		for z in range(zStart, zEnd):
			surface.surfaceMap[x][z].isOccupied = True

def setPathwayEnd(path, pathwayEndIndex, prop):
	i = pathwayEndIndex
	pathLength = len(path)
	distance = getDistance(prop.xPathwayStart, prop.zPathwayStart, path[i].x, path[i].z)
	step = 0
	if i + 1 < pathLength and getDistance(prop.xPathwayStart, prop.zPathwayStart, path[i + 1].x, path[i + 1].z) < distance:
		step = 1
	elif i - 1 >= 0 and getDistance(prop.xPathwayStart, prop.zPathwayStart, path[i - 1].x, path[i - 1].z) < distance:
		step = -1
	else:
		prop.xPathwayEnd = path[i].x
		prop.zPathwayEnd = path[i].z
		return

	pathwayEndIsFound = False
	distance = getDistance(prop.xPathwayStart, prop.zPathwayStart, path[i + step].x, path[i + step].z)
	nextDistance = 0
	i += step * 2
	while i >= 0 and i < pathLength and not pathwayEndIsFound:
		nextDistance = getDistance(prop.xPathwayStart, prop.zPathwayStart, path[i].x, path[i].z)
		if nextDistance >= distance:
			pathwayEndIsFound = True
		else:
			distance = nextDistance
			i += step
	prop.xPathwayEnd = path[i - step].x
	prop.zPathwayEnd = path[i - step].z

sqrtOfTwo = math.sqrt(2)
def getDistance(x1, z1, x2, z2):
	shortest = 0
	longest = 0
	horizontalDist = abs(x1 - x2)
	verticalDist = abs(z1 - z2)
	if horizontalDist < verticalDist:
		shortest = horizontalDist
		longest = verticalDist
	else:
		shortest = verticalDist
		longest = horizontalDist
	return shortest * sqrtOfTwo + longest - shortest

def decreaseProperty(surface, prop):
	# Deoccupy outer area
	for x in range(prop.xStart, prop.xEnd):
		surface.surfaceMap[x][prop.zStart].isOccupied = False
		surface.surfaceMap[x][prop.zEnd - 1].isOccupied = False
	for z in range(prop.zStart + 1, prop.zEnd - 1):
		surface.surfaceMap[prop.xStart][z].isOccupied = False
		surface.surfaceMap[prop.xEnd - 1][z].isOccupied = False

	# Decrease property
	prop.xStart += 1
	prop.xEnd -= 1
	prop.xLength -= 2
	prop.zStart += 1
	prop.zEnd -= 1
	prop.zLength -= 2