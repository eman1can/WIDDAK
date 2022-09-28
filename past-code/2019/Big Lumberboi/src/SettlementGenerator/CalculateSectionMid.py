from collections import deque
from Classes import Point
from Common import getMatrix

def calculateSectionMid(surface, section):
	surfaceInfo = newSurfaceInfo(surface, section)

	# Layer -1
	setOutsideSectionAsComplete(surface, section, surfaceInfo)

	# Layer 0
	findFirstLayerAlongBorder(surfaceInfo)
	for x in range(1, surfaceInfo.xLength - 1):
		for z in range(1, surfaceInfo.zLength - 1):
			findLayer(surfaceInfo, x, z, 0)

	# Layer 1+
	layer = 1
	finished = False
	while not finished:
		finished = True
		for x in range(0 + layer, surfaceInfo.xLength - layer):
			for z in range(0 + layer, surfaceInfo.zLength - layer):
				if isPartOfLayer(surfaceInfo, x, z, layer):
					findLayer(surfaceInfo, x, z, layer)
					finished = False
		layer += 1

	setSectionMid(section, surfaceInfo)
	updateSurfacePoints(surface, section, surfaceInfo)

def newSurfaceInfo(surface, section):
	xStart = section.points[0].x
	xEnd = section.points[0].x
	zStart = section.points[0].z
	zEnd = section.points[0].z
	for point in section.points:
		if point.x < xStart:
			xStart = point.x
		elif point.x > xEnd:
			xEnd = point.x
		if point.z < zStart:
			zStart = point.z
		elif point.z > zEnd:
			zEnd = point.z
	return SurfaceInfo(xStart, zStart, xEnd + 1, zEnd + 1)

def setOutsideSectionAsComplete(surface, section, surfaceInfo):
	for x in range(surfaceInfo.xLength):
		for z in range(surfaceInfo.zLength):
			if section.id != surface.surfaceMap[x + surfaceInfo.xStart][z + surfaceInfo.zStart].sectionId:
				surfaceInfo.surfaceMap[x][z].isComplete = True
				surfaceInfo.surfaceMap[x][z].layer = -1

def findFirstLayerAlongBorder(surfaceInfo):
	zTop = surfaceInfo.zLength - 1
	for x in range(surfaceInfo.xLength):
		if not surfaceInfo.surfaceMap[x][0].isComplete:
			surfaceInfo.surfaceMap[x][0].isComplete = True
			surfaceInfo.surfaceMap[x][0].layer = 0
		if not surfaceInfo.surfaceMap[x][zTop].isComplete:
			surfaceInfo.surfaceMap[x][zTop].isComplete = True
			surfaceInfo.surfaceMap[x][zTop].layer = 0

	xTop = surfaceInfo.xLength - 1
	for z in range(1, surfaceInfo.zLength - 1):
		if not surfaceInfo.surfaceMap[0][z].isComplete:
			surfaceInfo.surfaceMap[0][z].isComplete = True
			surfaceInfo.surfaceMap[0][z].layer = 0
		if not surfaceInfo.surfaceMap[xTop][z].isComplete:
			surfaceInfo.surfaceMap[xTop][z].isComplete = True
			surfaceInfo.surfaceMap[xTop][z].layer = 0

# A more simple function to find out whether the given point is part of the layer.
def isPartOfLayer(surfaceInfo, x, z, layer):
	return not surfaceInfo.surfaceMap[x][z].isComplete and surfaceInfo.surfaceMap[x + 1][z].layer == layer - 1

def findLayer(surfaceInfo, x, z, layer):
	queue = deque()
	queue.append(Point(x, z))
	while queue:
		point = queue.popleft()
		if addPointToLayer(surfaceInfo, point.x, point.z, layer):
			addNeighborPointsToQueue(surfaceInfo, point.x, point.z, layer, queue)

def addPointToLayer(surfaceInfo, x, z, layer):
	for xNeighbor in [x - 1, x, x + 1]:
		for zNeighbor in [z - 1, z, z + 1]:
			if xNeighbor == x and zNeighbor == z:
				continue
			if surfaceInfo.surfaceMap[xNeighbor][zNeighbor].layer == layer - 1:
				surfaceInfo.surfaceMap[x][z].layer = layer
				surfaceInfo.surfaceMap[x][z].isComplete = True
				return True

def addNeighborPointsToQueue(surfaceInfo, x, z, layer, queue):
	for xNeighbor in [x - 1, x, x + 1]:
		for zNeighbor in [z - 1, z, z + 1]:
			if xNeighbor == x and zNeighbor == z:
				continue
			if not surfaceInfo.surfaceMap[xNeighbor][zNeighbor].isComplete and surfaceInfo.surfaceMap[xNeighbor][zNeighbor].isCheckedByLayer != layer:
				surfaceInfo.surfaceMap[xNeighbor][zNeighbor].isCheckedByLayer = layer
				queue.append(Point(xNeighbor, zNeighbor))

def setSectionMid(section, surfaceInfo):
	xMid = 0
	zMid = 0
	layer = -2
	for x in range(surfaceInfo.xLength):
		for z in range(surfaceInfo.zLength):
			if layer < surfaceInfo.surfaceMap[x][z].layer:
				xMid = x
				zMid = z
				layer = surfaceInfo.surfaceMap[x][z].layer
	section.xMid = xMid + surfaceInfo.xStart
	section.zMid = zMid + surfaceInfo.zStart
	section.layerDepth = layer + 1

def updateSurfacePoints(surface, section, surfaceInfo):
	for x in range(surfaceInfo.xLength):
		for z in range(surfaceInfo.zLength):
			if section.id == surface.surfaceMap[surfaceInfo.xStart + x][surfaceInfo.zStart + z].sectionId:
				surface.surfaceMap[surfaceInfo.xStart + x][surfaceInfo.zStart + z].layer = surfaceInfo.surfaceMap[x][z].layer

class SurfaceInfo:

	def __init__(self, xStart, zStart, xEnd, zEnd):
		self.xStart = xStart
		self.zStart = zStart
		self.xEnd = xEnd
		self.zEnd = zEnd
		self.xLength = xEnd - xStart
		self.zLength = zEnd - zStart
		self.surfaceMap = self.getNewSurfaceMap()

	def getNewSurfaceMap(self):
		surfaceMap = []
		for _ in range(self.xLength):
			row = []
			for _ in range(self.zLength):
				row.append(PointInfo())
			surfaceMap.append(row)
		return surfaceMap

class PointInfo:

	def __init__(self):
		self.layer = -2 # -2 is for uncompleted points, -1 is for outside the section, 0+ is for the actual layers
		self.isComplete = False
		self.isCheckedByLayer = -1