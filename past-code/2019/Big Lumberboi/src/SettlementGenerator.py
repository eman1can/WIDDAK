import heapq

from BiomeFinder import findBiomes
from Biomes import getBiomeDict
from Classes import Point
from Classes import Surface
from Common import getEuclideanDistance
from Common import setBlock
from FarmBuilder import buildFarm
from FarmBuilder import clearFarmProperty
from GetPath import getPath
from GetPropertiesAlongPath import getPropertiesAlongPath
from HouseBuilder import clearHouseProperty
from PathManager import getPathsBetweenSections
from PathManager import getPathsInSections
from RemoveTree import removeTree
from RoadBuilder import buildTestRoad
from StructureBuilder import buildStructure
from SurfaceManager import calculateHeightMapAdv
from SurfaceManager import calculateSectionMid
from SurfaceManager import calculateSections
from SurfaceManager import calculateSteepnessMap
from SurfaceManager import calculateWaterPlacement

def perform(level, box, options):
	surface = Surface(box.minx, box.minz, box.maxx, box.maxz)
	calculateHeightMapAdv(level, surface)
	calculateSteepnessMap(surface)
	calculateWaterPlacement(level, surface)
	findBiomes(level, surface)

	sections = calculateSections(surface, 1, 15)
	calculateSectionMids(surface, sections)

	smallLandSections = []
	mediumLandSections = []
	bigLandSections = []
	waterSections = []

	arrangeSections(sections, waterSections, bigLandSections, mediumLandSections, smallLandSections)

	averageSurfaceHeight = calculateAverageSurfaceHeight(surface)
	calculateAverageSectionHeights(surface, sections)

	towerSections = getTowerSections(surface, averageSurfaceHeight, bigLandSections, mediumLandSections, smallLandSections)

	habitatSections = getHabitatSections(towerSections, mediumLandSections, bigLandSections)

	paths = getPathsInSections(surface, bigLandSections)
	paths.extend(getPathsBetweenSections(surface, habitatSections))

	buildPaths(level, surface, paths)

	properties = getProperties(surface, paths)
	clearHouseProperties(level, surface, properties)
	buildHouseProperties(level, surface, properties)

	farmProperties = getFarmProperties(surface, paths)
	clearFarmProperties(level, surface, farmProperties)
	buildFarmProperties(level, surface, farmProperties)

	buildTowers(level, surface, towerSections)

def calculateSectionMids(surface, sections):
	for section in sections:
		calculateSectionMid(surface, section)

def arrangeSections(sections, waterSections, bigLandSections, mediumLandSections, smallLandSections):
	for section in sections:
		if section.layerDepth < 2:
			continue
		if section.isWater:
			waterSections.append(section)
			continue
		if len(section.points) < 250:
			smallLandSections.append(section)
			continue
		if len(section.points) < 1000:
			mediumLandSections.append(section)
			continue
		bigLandSections.append(section)

def calculateAverageSurfaceHeight(surface):
	cumulativeHeight = 0
	for x in range(surface.xLength):
		for z in range(surface.zLength):
			cumulativeHeight += surface.surfaceMap[x][z].height
	return cumulativeHeight / (surface.xLength * surface.zLength)

def calculateAverageSectionHeights(surface, sections):
	for section in sections:
		section.averageHeight = calculateAverageSectionHeight(surface, section)

def calculateAverageSectionHeight(surface, section):
	cumulativeHeight = 0
	for point in section.points:
		x = point.x
		z = point.z
		cumulativeHeight += surface.surfaceMap[x][z].height
	return cumulativeHeight / len(section.points)

def heapifySectionsByAverageHeight(sections):
	heap = []
	for section in sections:
		heapq.heappush(heap, (-section.averageHeight, section))
	return heap

def getTowerSections(surface, averageSurfaceHeight, bigLandSections, mediumLandSections, smallLandSections):
	maxAmount = (surface.xLength * surface.zLength) / 25000 + 1
	sectionHeap = heapifySectionsByAverageHeight(smallLandSections)
	towerSections = []
	for i, element in enumerate(sectionHeap):
		if i >= maxAmount:
			break
		section = element[1]
		averageSectionHeight = section.averageHeight
		if averageSectionHeight < averageSurfaceHeight:
			break
		sectionMid = Point(section.xMid, section.zMid)
		if tooCloseToOtherTowers(surface, sectionMid, towerSections) or tooCloseToBiggerHigherSections(surface, sectionMid, averageSectionHeight, bigLandSections, mediumLandSections):
			continue
		towerSections.append(section)
	return towerSections

def tooCloseToOtherTowers(surface, sectionMid, towerSections):
	for towerSection in towerSections:
		towerSectionMid = Point(towerSection.xMid, towerSection.zMid)
		distance = getEuclideanDistance(surface, towerSectionMid, sectionMid)
		if distance < 100:
			return True
	return False

def tooCloseToBiggerHigherSections(surface, sectionMid, averageSectionHeight, bigLandSections, mediumLandSections):
	biggerSections = []
	biggerSections.extend(bigLandSections)
	biggerSections.extend(mediumLandSections)
	for s in biggerSections:
		if s.averageHeight < averageSectionHeight + 10:
			continue
		for p in s.points:
			if surface.surfaceMap[p.x][p.z].layer != 0:
				continue
			distance = getEuclideanDistance(surface, p, sectionMid)
			if distance < 30:
				return True
	return False

def getHabitatSections(towerSections, mediumLandSections, bigLandSections):
	habitatSections = []
	habitatSections.extend(towerSections)
	habitatSections.extend(mediumLandSections)
	habitatSections.extend(bigLandSections)
	return habitatSections

def buildPaths(level, surface, paths):
	for path in paths:
		buildTestRoad(level, surface, path)

def buildTowers(level, surface, towerSections):
	for section in towerSections:
		height = surface.surfaceMap[section.xMid][section.zMid].height
		biomeId = surface.surfaceMap[section.xMid][section.zMid].biomeId
		biome = getBiomeDict()[biomeId]
		buildStructure(level, Point(surface.xStart + section.xMid - 5, surface.zStart + section.zMid - 5), height, 'tower', 'north', biome)

def getProperties(surface, paths):
	properties = []
	for path in paths:
		properties.extend(getPropertiesAlongPath(surface, path, 7, 11, 7))
	return properties

def clearHouseProperties(level, surface, houseProperties):
	for p in houseProperties:
		clearHouseProperty(level, surface, p)

def buildHouseProperties(level, surface, properties):
	for p in properties:
		biomeId = surface.surfaceMap[p.xStart][p.zStart].biomeId
		biome = getBiomeDict()[biomeId]
		point = Point(surface.xStart + p.xStart, surface.zStart + p.zStart)
		buildStructure(level, point, p.height, 'house', 'north', biome, prop=p)
		buildPathway(level, surface, p.xPathwayStart, p.zPathwayStart, p.xPathwayEnd, p.zPathwayEnd)

def getFarmProperties(surface, paths):
	farmProperties = []
	for path in paths:
		farmProperties.extend(getPropertiesAlongPath(surface, path, 7, 11, 16))
	return farmProperties

def clearFarmProperties(level, surface, farmProperties):
	for p in farmProperties:
		clearFarmProperty(level, surface, p)

def buildFarmProperties(level, surface, farmProperties):
	for p in farmProperties:
		buildFarm(level, surface, p)

def buildPathway(level, surface, xStart, zStart, xEnd, zEnd):
	path = getPath(surface, xStart, zStart, xEnd, zEnd)
	for p in path:
		height = surface.surfaceMap[p.x][p.z].height
		setBlock(level, surface, p.x, height + 1, p.z, 0)
		setBlock(level, surface, p.x, height + 2, p.z, 0)
		if not surface.surfaceMap[p.x][p.z].isOccupied:
			setBlock(level, surface, p.x, height, p.z, 4)