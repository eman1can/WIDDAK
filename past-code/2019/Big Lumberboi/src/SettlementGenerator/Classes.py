from Common import getMatrix

class Surface:

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
		for x in range(self.xLength):
			row = []
			for z in range(self.zLength):
				row.append(SurfacePoint())
			surfaceMap.append(row)
		return surfaceMap

	def toSimpleSurfaceX(self, simpleSurface, x):
		return (self.xStart - simpleSurface.xStart + x) / 3

	def toSimpleSurfaceZ(self, simpleSurface, z):
		return (self.zStart - simpleSurface.zStart + z) / 3

	def toRealX(self, x):
		return self.xStart + x

	def toRealZ(self, z):
		return self.zStart + z

class SurfacePoint:

	def __init__(self):
		self.height = 0
		self.steepness = 0
		self.isWater = False
		self.sectionId = -1
		self.layer = -1
		self.isOccupied = False
		self.houseId = -1
		self.biomeId = -1

class SimpleSurface:

	def __init__(self, xStart, zStart, xEnd, zEnd):
		self.xStart = xStart + (3 - xStart % 3) % 3
		self.zStart = zStart + (3 - zStart % 3) % 3
		self.xEnd = xEnd - xEnd % 3
		self.zEnd = zEnd - zEnd % 3
		self.xRealLength = self.xEnd - self.xStart
		self.zRealLength = self.zEnd - self.zStart
		self.xLength = self.xRealLength / 3
		self.zLength = self.zRealLength / 3
		self.surfaceMap = self.getNewSurfaceMap()

	def getNewSurfaceMap(self):
		surfaceMap = []
		for x in range(self.xLength):
			row = []
			for z in range(self.zLength):
				row.append(SurfaceArea())
			surfaceMap.append(row)
		return surfaceMap

	def toSurfaceX(self, surface, x):
		return self.xStart - surface.xStart + x * 3 + 1

	def toSurfaceZ(self, surface, z):
		return self.zStart - surface.zStart + z * 3 + 1

	def toRealX(self, x):
		return self.xStart + x * 3 + 1

	def toRealZ(self, z):
		return self.zStart + z * 3 + 1

class SurfaceArea:

	def __init__(self):
		self.height = 0
		self.isWater = False
		self.houseId = -1

class Section:

	def __init__(self, id):
		self.id = id
		self.points = []
		self.size = 0
		self.layerDepth = 0
		self.averageHeight = 0
		self.xMid = 0
		self.zMid = 0
		self.pathConnectionPoints = []
		self.isWater = False
		self.exitPoints = []
		self.name = ""

class Point:

	def __init__(self, x, z):
		self.x = x
		self.z = z

class Node:

	def __init__(self, id, data):
		self.id = id
		self.data = data

class Edge:

	def __init__(self, cost, nodeId1, nodeId2):
		self.cost = cost
		self.nodeId1 = nodeId1
		self.nodeId2 = nodeId2

	def __eq__(self, other):
		return self.cost == other.cost

	def __lt__(self, other):
		return self.cost < other.cost

class Property:

	def __init__(self, xStart, zStart, xEnd, zEnd, height):
		self.xStart = xStart
		self.zStart = zStart
		self.xEnd = xEnd
		self.zEnd = zEnd
		self.xLength = xEnd - xStart
		self.zLength = zEnd - zStart
		self.height = height
		self.doorDirection = ""
		self.xPathwayStart = 0
		self.zPathwayStart = 0
		self.xPathwayEnd = 0
		self.zPathwayEnd = 0

class Bridge:

	def __init__(self, bridgePoints, biomeId):
		self.bridgePoints = bridgePoints
		self.biomeId = biomeId

class Blueprint:

	def __init__(self, point, blockRegister, baseHeight, base = None, buildFoundation = False):
		self.point = point
		self.blockRegister = blockRegister
		self.baseHeight = baseHeight
		self.base = base
		self.buildFoundation = buildFoundation

class Base:
	
	def __init__(self, xStart, zStart, xLength, zLength):
		self.xStart = xStart
		self.zStart = zStart
		self.xLength = xLength
		self.zLength = zLength