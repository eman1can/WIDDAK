import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from collections import defaultdict
from AStar import aStar
from AStar import simpleAStar
from Matrix import Matrix
from cityDeck import CityDeck
import RNG
from copy import deepcopy
import sys
from operator import itemgetter
from collections import Counter
import utility as utility


air_like = [0, 6, 17, 18, 30, 31, 32, 37, 38, 39, 40, 59, 81, 83, 85, 104, 105, 106, 107, 111, 141, 142, 161, 162, 175, 78, 79, 99]
ground_like = [1, 2, 3]
water_like = [8, 9, 10, 11]

# These are a few helpful functions we hope you find useful to use

# sets the block to the given blocktype at the designated x y z coordinate
# *params*
# level : the minecraft world level
# (block, data) : a tuple with block = the block id and data being a subtype
# x,y,z : the coordinate to set
def setBlock(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
    	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)

# sets the block to the given blocktype at the designated x y z coordinate IF the block is empty (air)
# *params*
# level : the minecraft world level
# (block, data) : a tuple with block = the block id and data being a subtype
# x,y,z : the coordinate to set
def setBlockIfEmpty(level, (block, data), x, y, z):
    tempBlock = level.blockAt((int)(x),(int)(y),(int)(z))
    if tempBlock == 0:
		setBlock(level, (block, data), (int)(x),(int)(y),(int)(z))

# sets every block to the given blocktype from the given x y z coordinate all the way down to ymin if the block is empty
# *params*
# level : the minecraft world level
# (block, data) : a tuple with block = the block id and data being a subtype
# x,y,z : the coordinate to set
# ymin: the minium y in which the iteration ceases
def setBlockToGround(level, (block, data), x, y, z, ymin):
    for iterY in xrange(ymin, (int)(y)):
    	setBlockIfEmpty(level, (block, data), (int)(x),(int)(iterY),(int)(z))


# Given an x an z coordinate, this will drill down a y column from box.maxy until box.miny and return a list of blocks
def drillDown(level, x, z, miny, maxy):
	blocks = []
	for y in xrange(maxy, miny, -1):
		blocks.append(level.blockAt(x, y, z))
		# print level.blockAt(x,y,z)
	return blocks

# Given an x an z coordinate, this will go from box.miny to maxy and return the first block under an air block
def findTerrain_old(level, x, z, miny, maxy):
	blocks = []
	for y in xrange(miny, maxy):
		#print("y: ", y, " block: ", level.blockAt(x, y, z))
		if level.blockAt(x, y, z) == 0:
			return y-1
		# print level.blockAt(x,y,z)
	return -1



# returns a 2d matrix representing tree trunk locations on an x-z coordinate basis (bird's eye view) in the given box
# *params*
# level: the minecraft world level
# box: the selected subspace of the world
def treeMap(level, box):
	# Creates a 2d array containing z rows, each of x items, all set to 0
	w = abs(box.maxz - box.minz)
	h = abs(box.maxx - box.minx)
	treeMap = zeros((w,h))

	countx = box.minx
	countz = box.minz
	# iterate over the x dimenison of the mapping
	for x in range(h):
		# iterate over the z dimension of the mapping
		countz = box.minz
		for z in range(w):
			# drillDown at this location and get all the blocks in the y-column
			column = drillDown(level, countx, countz, box.miny, box.maxy)
			for block in column:
				# check if any block in this column is a wooden trunk block. If so, there is at this x-z coordinate
				if block == 17:
					treeMap[z][x] = 17
			print treeMap[z][x] ,
			countz += 1
		print ''
		countx += 1
	return treeMap


# returns the box size dimensions in x y and z
def getBoxSize(box):
	return (box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz)

# returns an array of blocks after raytracing from (x1,y1,z1) to (x2,y2,z2)
# this uses Bresenham 3d algorithm, taken from a modified version written by Bob Pendleton
def raytrace((x1, y1, z1), (x2, y2, z2)):
	output = []

	x2 -= 1
	y2 -= 1
	z2 -= 1

	i = 0
	dx = 0
	dy = 0
	dz = 0
	l = 0
	m = 0
	n = 0
	x_inc = 0
	y_inc = 0
	z_inc = 0
	err_1 = 0
	err_2 = 0
	dx2 = 0
	dy2 = 0
	dz2 = 0
	point = [x1,y1,z1]

	dx = x2 - x1
	dy = y2 - y1;
	dz = z2 - z1;
	x_inc = -1  if dx < 0 else 1
	l = abs(dx)
	y_inc = -1 if dy < 0 else 1
	m = abs(dy)
	z_inc = -1 if dz < 0 else 1
	n = abs(dz)
	dx2 = l << 1
	dy2 = m << 1
	dz2 = n << 1

	if l >= m and l >= n:
		err_1 = dy2 - l
		err_2 = dz2 - l
		for i in range(l):
			np = (point[0], point[1], point[2])
			output.append(np)
			if err_1 > 0:
				point[1] += y_inc
				err_1 -= dx2

			if err_2 > 0:
				point[2] += z_inc
				err_2 -= dx2

			err_1 += dy2
			err_2 += dz2
			point[0] += x_inc

	elif m >= l and m >= n:
		err_1 = dx2 - m
		err_2 = dz2 - m
		for i in range(m):
			np = (point[0], point[1], point[2])
			output.append(np)
			if err_1 > 0:
				point[0] += x_inc
				err_1 -= dy2

			if err_2 > 0:
				point[2] += z_inc
				err_2 -= dy2

			err_1 += dx2
			err_2 += dz2
			point[1] += y_inc

	else:
		err_1 = dy2 - n
		err_2 = dx2 - n
		for i in range(n):
			np = (point[0], point[1], point[2])
			output.append(np)
			if err_1 > 0:
				point[1] += y_inc
				err_1 -= dz2

			if err_2 > 0:
				point[0] += x_inc
				err_2 -= dz2

			err_1 += dy2
			err_2 += dx2
			point[2] += z_inc

	np = (point[0], point[1], point[2])
	output.append(np)
	return output

# Given an x an z coordinate, this will drill down a y column from box.maxy until box.miny and return a list of blocks
def drillDown(level,box):
	(width, height, depth) = getBoxSize(box)
	blocks = []
	for y in xrange(maxy, miny, -1):
		blocks.append(level.blockAt(x, y, z))
		# print level.blockAt(x,y,z)
	return blocks

# Given an x an z coordinate, this will go from box.miny to maxy and return the first block under an air block
def findTerrain(level, x, z, miny, maxy):


	blocks = []
	for y in xrange(maxy-1, miny-1, -1):
		#print("y: ", y, " block: ", level.blockAt(x, y, z))
		if level.blockAt(x, y, z) in air_like:
			continue
		elif level.blockAt(x, y, z) in water_like:
			return -1
		else:
			return y
		#elif level.blockAt(x, y, z) in ground_like:
		#	return y
		# print level.blockAt(x,y,z)
	return -1

def findSimpleTerrain(level, x, z, miny, maxy):
	blocks = []
	for y in xrange(maxy-1, miny-1, -1):
		#print("y: ", y, " block: ", level.blockAt(x, y, z))
		if level.blockAt(x, y, z) in air_like:
			continue
		else:
			return y
	return -1


# class that allows easy indexing of dicts
class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    #__getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    def __getattr__(self, attr):
        if attr.startswith('__'):
            raise AttributeError
        return self.get(attr, None)

# generate and return 3d matrix as in the format matrix[h][w][d]
def generateMatrix(level, box, width, depth, height):
	matrix = Matrix(level, box, height, width, depth)
	return matrix

# generate and return a settlement in the form of a deck composed with a specific number of buildings
def generateCityDeck(type, width, height):
	return CityDeck(type, width, height)

# get a subsection of a give arean partition based on the percentage
def getSubsection(y_min, y_max, x_min, x_max, z_min, z_max, percentage=0.8):

	width = x_max - x_min
	x_mid = x_min + int(width/2)

	subsection_x_size = int(width*percentage)
	subsection_x_mid = int(subsection_x_size/2)
	subsection_x_min = x_mid - subsection_x_mid
	subsection_x_max = x_mid + subsection_x_mid

	depth = z_max - z_min
	z_mid = z_min + int(depth/2)

	subsection_z_size = int(depth*percentage)
	subsection_z_mid = int(subsection_z_size/2)

	subsection_z_min = z_mid - subsection_z_mid
	subsection_z_max = z_mid + subsection_z_mid

	return (y_min, y_max, subsection_x_min, subsection_x_max, subsection_z_min, subsection_z_max)

# remove inner partition from outer and return 4 partitions as the result
def subtractPartition(outer, inner):

	p1 = (outer[0], outer[1], outer[2], inner[2] - 5, outer[4], inner[5] + 5)
	p2 = (outer[0], outer[1], inner[2] - 5, outer[3], outer[4], inner[4] - 5)
	p3 = (outer[0], outer[1], inner[3] + 5, outer[3], inner[4] - 5, outer[5])
	p4 = (outer[0], outer[1], outer[2], inner[3] + 5, inner[5] + 5, outer[5])

	return (p1,p2,p3,p4)

def getEuclidianDistancePartitions(p1, p2):

	p1_center = (p1[0] + int((p1[1]-p1[0])*0.5), p1[2] + int((p1[3]-p1[2])*0.5))
	p2_center = (p2[0] + int((p2[1]-p2[0])*0.5), p2[2] + int((p2[3]-p2[2])*0.5))
	euclidian_distance = getEuclidianDistance(p1_center,p2_center)
	return euclidian_distance

def getEuclidianDistance(p1,p2):
	distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))
	return distance

def getManhattanDistance(p1,p2):
	distance = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
	return distance


# Given a partition and height map, return true if there's no water
# or other unwalkable block inside that partition
def hasValidGroundBlocks(x_min, x_max,z_min,z_max, height_map):

	for x in range(x_min, x_max+1):
		for z in range(z_min, z_max+1):
			if height_map[x][z] == -1:
				return False
	return True

# Return true if a partition has the minimum size specified
def hasMinimumSize(y_min, y_max, x_min, x_max,z_min,z_max, minimum_h=4, minimum_w=16, minimum_d=16):

	if y_max-y_min < minimum_h or x_max-x_min < minimum_w or z_max-z_min < minimum_d:
		return False
	return True

# Return true if a given partition has an acceptable steepness
# according to the a scoring function and a threshold
def hasAcceptableSteepness(x_min, x_max, z_min, z_max, height_map, scoring_function, threshold = 5):
	score = scoring_function(height_map, x_min, x_max, z_min , z_max)
	if score > threshold:
		return False
	return True

# given a box selection, returns a 2d matrix where each element is
# the height of the first non-block air in that x, z position
def getHeightMap(level, box):
	logging.info("Calculating height map...")
	terrain = [[0 for z in range(box.minz,box.maxz)] for x in range(box.minx,box.maxx)]

	for d, z in zip(range(box.minz,box.maxz), range(0, box.maxz-box.minz)):
		for w, x in zip(range(box.minx,box.maxx), range(0, box.maxx-box.minx)):
			terrain[x][z] = findTerrain(level, w, d, box.miny, box.maxy)

	#print("Terrain Map: ")
	#for x in range(0, box.maxx-box.minx):
	#	print(terrain[x])
	return terrain

def getSimpleHeightMap(level,box):
	logging.info("Calculating simple height map...")
	terrain = [[0 for z in range(box.minz,box.maxz)] for x in range(box.minx,box.maxx)]

	for d, z in zip(range(box.minz,box.maxz), range(0, box.maxz-box.minz)):
		for w, x in zip(range(box.minx,box.maxx), range(0, box.maxx-box.minx)):
			terrain[x][z] = findSimpleTerrain(level, w, d, box.miny, box.maxy)

	return terrain

def getPathMap(height_map, width, depth):
	pathMap = []

	for x in range(width):
		pathMap.append([])
		for z in range(depth):
			pathMap[x].append(dotdict())

	threshold = 50
	for x in range(width):
		for z in range(depth):

			#left
			if x-1 < 0:
				pathMap[x][z].left = -1
			else:
				pathMap[x][z].left = abs(height_map[x-1][z] - height_map[x][z])
				if pathMap[x][z].left > threshold or height_map[x-1][z] == -1:
					pathMap[x][z].left = -1


			#right
			if x+1 >= width:
				pathMap[x][z].right = -1
			else:
				pathMap[x][z].right = abs(height_map[x][z] - height_map[x+1][z])
				if pathMap[x][z].right > threshold or height_map[x+1][z] == -1:
					pathMap[x][z].right = -1

			#down
			if z-1 < 0:
				pathMap[x][z].down = -1
			else:
				pathMap[x][z].down = abs(height_map[x][z] - height_map[x][z-1])
				if pathMap[x][z].down > threshold or height_map[x][z-1] == -1:
					pathMap[x][z].down = -1

			#up
			if z+1 >= depth:
				pathMap[x][z].up = -1
			else:
				pathMap[x][z].up = abs(height_map[x][z+1] - height_map[x][z])
				if pathMap[x][z].up > threshold or height_map[x][z+1] == -1:
					pathMap[x][z].up = -1

	return pathMap


def getScoreArea_type1(height_map, min_x, max_x, min_z, max_z):
	initial_value = height_map[min_x][min_z]

	ocurred_values = []
	value = 0
	for x in range(min_x, max_x+1):
		for z in range(min_z, max_z+1):
			difference = initial_value - height_map[x][z]
			if difference not in ocurred_values:
				ocurred_values.append(difference)
  	return len(ocurred_values)

def getScoreArea_type2(height_map, min_x, max_x, min_z, max_z):
	initial_value = height_map[min_x][min_z]

	value = 0
	for x in range(min_x, max_x+1):
		for z in range(min_z, max_z+1):
			value += abs(initial_value - height_map[x][z])
  	return value

def getScoreArea_type3(height_map, min_x, max_x, min_z, max_z):
	initial_value = height_map[min_x][min_z]

	value = 0
	for x in range(min_x, max_x+1):
		for z in range(min_z, max_z+1):
			value += (abs(initial_value - height_map[x][z]))**2
  	return value

def getScoreArea_type4(height_map, min_x, max_x, min_z, max_z):
	area_surface = (max_x-min_x)*(max_z-min_z)
	list_height = []
	for x in range(min_x, max_x+1):
		for z in range(min_z, max_z+1):
			list_height.append(height_map[x][z])

	list_height_nb_occurence = []
	for h in set(list_height):
		nb_occurence = list_height.count(h)
		list_height_nb_occurence.append((h, nb_occurence))
	height_mode = max(list_height_nb_occurence,key=itemgetter(1))[0]

	list_cost_per_height = []
	for h, nb in list_height_nb_occurence:
		list_cost_per_height.append((h, nb, (abs(h-height_mode))))

	score = 0
	for h, nb, c in list_cost_per_height:
		score += c
	return score

def getHeightCounts(matrix, min_x, max_x, min_z, max_z):
	flood_values = {}
	for x in range(min_x, max_x+1):
		for z in range(min_z, max_z+1):
			value = matrix[x][z]
			if value not in flood_values.keys():
				flood_values[value] = 1
			else:
				flood_values[value] += 1
	return flood_values

def getMostOcurredGroundBlock(matrix, height_map, min_x, max_x, min_z, max_z):
	block_values = []
	for x in range(min_x, max_x+1):
		block_values.append(getBlockFullValue(matrix, height_map[x][max_z], x, max_z))
		block_values.append(getBlockFullValue(matrix, height_map[x][min_z], x, min_z))
	for z in range(min_z+1, max_z):
		block_values.append(getBlockFullValue(matrix, height_map[max_x][z], max_x, z))
		block_values.append(getBlockFullValue(matrix, height_map[min_x][z], min_x, z))

	return mostOccured(block_values)


# receives a list of areas in the format (x_min, x_max, z_min, z_max)
# returns the same list minus any overlaping areas
def removeOverlaping(areas):
	if len(areas) == 0: return areas

	# get the first area from the list as a valid area
	validAreas = areas[:1]
	areas = areas[1:]

	for i in range(len(areas)):
		current_area = areas[0]
		for index, a in enumerate(validAreas):
			if intersectRect(current_area, a):
				break
		else:
			validAreas.append(current_area)
		areas = areas[1:]

	return validAreas

# returns whether or not 2 partitions are colliding, must be in the format
# (x_min, x_max, z_min, z_max)
def intersectRect(p1, p2):
    return not (p2[0] > p1[1] or p2[1] < p1[0] or p2[3] < p1[2] or p2[2] > p1[3])

# returns whether or not 2 partitions are colliding, must be in the format
# (y_min, y_max, x_min, x_max, z_min, z_max)
def intersectPartitions(p1, p2):
    return not (p2[2] > p1[3] or p2[3] < p1[2] or p2[5] < p1[4] or p2[4] > p1[5])

def getNonIntersectingPartitions(partitioning):
	cleaned_partitioning = []
	for (score, partition) in partitioning:
		intersect = False
		for (score, valid_partition) in cleaned_partitioning:
			if intersectPartitions(partition, valid_partition):
				intersect = True
				break
		if intersect == False:
			cleaned_partitioning.append((score, partition))
	return cleaned_partitioning

# update the minecraft world given a matrix with h,w,d dimensions, and each element in the
# (x, y) format, where x is the ID of the block and y the subtype
def updateWorld(level, box, matrix, height, width, depth):
	for y, h in zip(range(box.miny,box.maxy), range(0,height)):
		for x, w in zip(range(box.minx,box.maxx), range(0,width)):
			for z, d in zip(range(box.minz,box.maxz), range(0,depth)):
				if matrix.isChanged(h,w,d):
					try:
						block = matrix.getValue(h,w,d)
						setBlock(level, (block[0], block[1]), x, y, z)
					except:
						block = matrix.getValue(h,w,d)
						setBlock(level, (block, 0), x, y, z)

def getCentralPoint(x_min, x_max, z_min, z_max):
	x_mid = x_max - int((x_max - x_min)/2)
	z_mid = z_max - int((z_max - z_min)/2)
	return (x_mid, z_mid)



def getMST_Manhattan(buildings):
	MST = []
	vertices = []
	partitions = deepcopy(buildings)

	selected_vertex = partitions[RNG.randint(0, len(partitions)-1)]
	logging.error("Initial selected partition: {}".format(selected_vertex))
	vertices.append(selected_vertex)
	partitions.remove(selected_vertex)

	while len(partitions) > 0:

		edges = []
		for v in vertices:
			logging.error("v: {}".format(v))
			for p in partitions:
				logging.error("\tp: {}".format(p))
				p1 = v.entranceLot
				p2 = p.entranceLot
				distance = getManhattanDistance((p1[0],p1[1]), (p2[0],p2[1]))
				edges.append((distance, v, p))

		edges = sorted(edges)
		if len(edges) > 0:
			MST.append((edges[0][0], edges[0][1], edges[0][2]))
		partitions.remove(edges[0][2])
		vertices.append(edges[0][2])
	return MST


#print a matrix given its h,w,d dimensions
def printMatrix(matrix, height, width, depth):
	for h in range(0,height):
		print("matrix at height: ", h)
		for x in range(0,width):
			print(matrix[h][x])

def twoway_range(start, stop):
	return range(start, stop + 1, 1) if (start <= stop) else range(start, stop - 1, -1)

def updateHeightMap(height_map, x_min, x_max, z_min, z_max, height):
	for x in range(x_min, x_max + 1):
		for z in range(z_min, z_max + 1):
			#print("updating height at {}, {}, {}, {}".format(x_min, x_max, z_min, z_max))
			height_map[x][z] = height

def cleanProperty(matrix, h_min, h_max, x_min, x_max, z_min, z_max):
	for h in range(h_min, h_max):
		for x in range(x_min, x_max + 1):
			for z in range(z_min, z_max + 1):
				matrix.setValue(h, x, z, getBlockID("air"))

# algorithm to randomly find flat areas given a height map
def getAreasSameHeight(box,terrain):
	validAreas = []

	for i in range(0, 1000):
		random_x = RNG.randint(0, box.maxx - box.minx)
		random_z = RNG.randint(0, box.maxz - box.minz)
		size_x = 15
		size_z = 15
		if checkSameHeight(terrain, 0, box.maxx - box.minx, 0,box.maxz - box.minz, random_x, random_z, size_x, size_z):
			newValidArea = (random_x, random_x + size_x-1, random_z, random_z + size_z - 1)
			if newValidArea not in validAreas:
				validAreas.append(newValidArea)

	print("Valid areas found:")
	validAreas = removeOverlaping(validAreas)
	for a in validAreas:
		print(a)

	return validAreas

def checkSameHeight(terrain, minx, maxx, minz, maxz, random_x, random_z, mininum_w, mininum_d):
	if random_x + mininum_w > maxx or random_z + mininum_d > maxz or terrain[random_x][random_z] == -1:
		return False

	initial_value = terrain[random_x][random_z]

	for x in range(random_x, random_x + mininum_w):
		for z in range(random_z, random_z + mininum_d):
			#print("Checking x, z: ", x, z)
			if terrain[x][z] != initial_value:
				return False

	return True

def checkSlopeTerrain(p, height_map):
	score = getScoreArea_type1(height_map, p[2], p[3], p[4], p[5])
	return score >= 10

def getHighestPoint(height_map, x_min, x_max, z_min, z_max):
	highestPoint = (x_min, z_min)
	for x in range(x_min, x_max):
		for z in range(z_min, z_max):
			if height_map[x][z] > height_map[highestPoint[0]][highestPoint[1]]:
				highestPoint = (x, z)
	return highestPoint

def findBridgeEndPoints(matrix, path, height_map): #find if bridges are needed on a path, if so, return the end points of them
	inWater = False
	list_bridge_end_points = []
	for i in range(1, len(path)):

		block = path[i]
		before_b = path[i-1]

		if inWater == False and matrix.getValue(height_map[block[0]][block[1]], block[0], block[1]) in water_like:
			list_bridge_end_points.append((before_b[0], before_b[1]))
			inWater = True
		if inWater == True and matrix.getValue(height_map[block[0]][block[1]], block[0], block[1]) not in water_like:
			list_bridge_end_points.append((block[0], block[1]))
			inWater = False

	return list_bridge_end_points

def getBlockFullValue(matrix, h, w, d):
	if isinstance(matrix.getValue(h, w, d),tuple):
		return matrix.getValue(h, w, d)
	else:
		x = matrix.getWorldX(w)
		y = matrix.getWorldY(h)
		z = matrix.getWorldZ(d)
		block = matrix.level.blockAt(x,y,z)
		data = matrix.level.blockDataAt(x,y,z)
		return (block, data)

def mostOccured(l):
    occurence_count = Counter(l)
    return occurence_count.most_common(1)[0][0]

## Score for each structure type to help generating it on an appropriate terrain
structure_scores = {
	"house" : 0.4,
	"farm" : 0.2,
	"building" : 0.5,
	"fountain" : 0.8,
	"slope structure" : 1
}
def getStructureScore(name):
	return structure_scores[name]

def getBlockID(name, secondaryID = 0):
	return utility.getBlockID(name, secondaryID)

## Set of blocks for each wood type :
# 0 -> planks
# 1 -> log
# 2 -> slab
# 3 -> stairs
# 4 -> door
# 5 -> fence
# 6 -> fence_gate
def createWoodenMaterialsKit(planks, log, slab, stairs, door, fence, fence_gate):
	return {
		"planks" : planks,
		"log" : log,
		"slab" : slab,
		"stairs" : stairs,
		"door" : door,
		"fence" : fence,
		"fence_gate" : fence_gate
	}

wood_IDs = {
	"oak" :			createWoodenMaterialsKit(getBlockID("planks", 0), getBlockID("log", 0), getBlockID("wooden_slab", 0), getBlockID("oak_stairs", 0), getBlockID("wooden_door", 0), getBlockID("oak_fence", 0), getBlockID("oak_fence_gate", 0)),
	"spruce" :		createWoodenMaterialsKit(getBlockID("planks", 1), getBlockID("log", 1), getBlockID("wooden_slab", 1), getBlockID("spruce_stairs", 0), getBlockID("spruce_door", 0), getBlockID("spruce_fence", 0), getBlockID("spruce_fence_gate", 0)),
	"birch" :		createWoodenMaterialsKit(getBlockID("planks", 2), getBlockID("stone", 6), getBlockID("wooden_slab", 2), getBlockID("birch_stairs", 0), getBlockID("birch_door", 0), getBlockID("birch_fence", 0), getBlockID("birch_fence_gate", 0)),
	"jungle" :		createWoodenMaterialsKit(getBlockID("planks", 3), getBlockID("log", 3), getBlockID("wooden_slab", 3), getBlockID("jungle_stairs", 0), getBlockID("jungle_door", 0), getBlockID("jungle_fence", 0), getBlockID("jungle_fence_gate", 0)),
	"dark_oak" :	createWoodenMaterialsKit(getBlockID("planks", 4), getBlockID("log2", 1), getBlockID("wooden_slab", 4), getBlockID("acacia_stairs", 0), getBlockID("acacia_door", 0), getBlockID("acacia_fence", 0), getBlockID("acacia_fence_gate", 0)),
	"acacia" :		createWoodenMaterialsKit(getBlockID("planks", 5), getBlockID("log2", 0), getBlockID("wooden_slab", 5), getBlockID("dark_oak_stairs", 0), getBlockID("dark_oak_door", 0), getBlockID("dark_oak_fence", 0), getBlockID("dark_oak_fence_gate", 0)),
	"urban" :		createWoodenMaterialsKit(getBlockID("double_stone_slab", 5), getBlockID("double_stone_slab", 5), getBlockID("stone_slab", 5), getBlockID("stone_brick_stairs", 0), getBlockID("iron_door", 0), getBlockID("cobblestone_wall", 0), getBlockID("dark_oak_fence_gate", 0))
}


## Rail orientation goes from 0 to 9 included (2, 3, 4, 5 -> slopes) (6, 7, 8, 9 -> turns)
#Orientation = Enum("Orientation", "VERTICAL HORIZONTAL NORTH SOUTH WEST EAST NORTH_EAST SOUTH_EAST SOUTH_WEST NORTH_WEST")
class Orientation:
	VERTICAL = 1
	HORIZONTAL = 2
	NORTH = 3
	SOUTH = 4
	WEST = 5
	EAST = 6
	NORTH_EAST = 7
	SOUTH_EAST = 8
	SOUTH_WEST = 9
	NORTH_WEST = 10
