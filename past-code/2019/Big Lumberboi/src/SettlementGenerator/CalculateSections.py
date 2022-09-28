from collections import deque
from Classes import Point
from Classes import Section
from Common import getMatrix

def calculateSections(surface, allowedSteepness = 0, minSize = 1):
	sections = []
	isChecked = getMatrix(surface.xLength, surface.zLength, False) #A matrix that keeps track of which points are checked

	id = 0
	for x in range(surface.xLength):
		for z in range(surface.zLength):
			if isChecked[x][z]:
				continue
			if surface.surfaceMap[x][z].steepness <= allowedSteepness:
				section = calculateSection(id, Point(x, z), surface, isChecked, allowedSteepness)
				if section.size >= minSize:
					registerIdsOnSurface(surface, section)
					sections.append(section)
					id += 1
			isChecked[x][z] = True
	return sections

def registerIdsOnSurface(surface, section):
	for point in section.points:
		surface.surfaceMap[point.x][point.z].sectionId = section.id

def calculateSection(id, startPoint, surface, isChecked, allowedSteepness):
	section = Section(id)
	section.isWater = surface.surfaceMap[startPoint.x][startPoint.z].isWater
	pointsToCheck = deque()
	pointsToCheck.append(startPoint)
	isChecked[startPoint.x][startPoint.z] = True
	while pointsToCheck:
		nextPoint = pointsToCheck.popleft()
		x = nextPoint.x
		z = nextPoint.z
		if surface.surfaceMap[x][z].isWater == section.isWater and (surface.surfaceMap[x][z].steepness <= allowedSteepness or section.isWater):
			section.points.append(nextPoint)
			pointsToCheck.extend(getNeighboursToCheck(nextPoint, surface, isChecked))
		else:
			isChecked[x][z] = False
	section.size = len(section.points)
	return section

def getNeighboursToCheck(point, surface, isChecked):
	neighboursToCheck = []
	x = point.x
	z = point.z
	if (x + 1) < surface.xLength and not isChecked[x + 1][z]:
		isChecked[x + 1][z] = True
		neighboursToCheck.append(Point(x + 1, z))
	if (z + 1) < surface.zLength and not isChecked[x][z + 1]:
		isChecked[x][z + 1] = True
		neighboursToCheck.append(Point(x, z + 1))
	if (x - 1) >= 0 and not isChecked[x - 1][z]:
		isChecked[x - 1][z] = True
		neighboursToCheck.append(Point(x - 1, z))
	if (z - 1) >= 0 and not isChecked[x][z - 1]:
		isChecked[x][z - 1] = True
		neighboursToCheck.append(Point(x, z - 1))
	return neighboursToCheck