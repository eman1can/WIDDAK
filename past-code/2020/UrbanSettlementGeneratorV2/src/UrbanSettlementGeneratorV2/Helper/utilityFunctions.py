import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from collections import defaultdict
from AStar import aStar
from Matrix import Matrix
import RNG
import BlocksInfo as BlocksInfo
from copy import deepcopy
import sys

air_like = [0, 4, 5, 6, 17, 18, 20, 23, 26, 29, 30, 31, 32, 35, 37, 38, 39, 40, 44, 46, 47, 48, 50, 53, 54, 55, 58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 78, 81, 83, 85, 86, 93, 94, 95, 96, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 117, 118, 126, 128, 131, 132, 134, 135, 136, 139, 140, 141, 142, 145, 146, 160, 161, 162, 163, 164, 170, 171, 175, 176, 177, 180, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 207]
ground_like = [1, 2, 3, 12, 13, 16, 79, 80, 82, 110, 159, 174]
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

# Given an x an z coordinate, this will go from box.miny to maxy and return the first block under a block considered as an air block
def findTerrain2(level, x, z, miny, maxy, air_like_id):
	blocks = []
	if air_like_id is None :
		air_like_id = air_like

	for y in xrange(maxy-1, miny-1, -1):
		if level.blockAt(x, y, z) in air_like_id:
			continue
		elif level.blockAt(x, y, z) in water_like:
			return -1
		else:
			return y
	return -1

# Given an x an z coordinate, this will go from box.miny to maxy and return the first block under a block considered as an air block
def findTerrain3(level, x, z, miny, maxy, air_like_id):
	blocks = []
	if air_like_id is None :
		air_like_id = air_like

	for y in xrange(maxy-1, miny-1, -1):
		if level.blockAt(x, y, z) in air_like_id:
			continue
		else:
			return y
	return -1

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

	p1 = (outer[0], outer[1], outer[2], inner[2], outer[4], inner[5])
	p2 = (outer[0], outer[1], inner[2], outer[3], outer[4], inner[4])
	p3 = (outer[0], outer[1], inner[3], outer[3], inner[4], outer[5])
	p4 = (outer[0], outer[1], outer[2], inner[3], inner[5], outer[5])

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

	for x in range(x_min, x_max):
		for z in range(z_min, z_max):
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
def hasAcceptableSteepness(x_min, x_max,z_min,z_max, height_map, scoring_function, threshold = 5):
	initial_value = height_map[x_min][z_min]
	score = scoring_function(height_map, x_min, x_max, z_min , z_max , initial_value)
	if score > threshold:
		return False
	return True

# given a box selection, returns a 2d matrix where each element is
# the height of the first non-block air in that x, z position
def getHeightMap(level, box, air_like_id, consider_water) :
	logging.info("Calculating height map...")
	terrain = [[0 for z in range(box.minz,box.maxz)] for x in range(box.minx,box.maxx)]

	for d, z in zip(range(box.minz,box.maxz), range(0, box.maxz-box.minz)):
		for w, x in zip(range(box.minx,box.maxx), range(0, box.maxx-box.minx)):
			if consider_water :
				terrain[x][z] = findTerrain3(level, w, d, box.miny, box.maxy, air_like_id)
			else:
				terrain[x][z] = findTerrain2(level, w, d, box.miny, box.maxy, air_like_id)

	#print("Terrain Map: ")
	#for x in range(0, box.maxx-box.minx):
	#	print(terrain[x])
	return terrain

def getPathMap(height_map, width, depth):
	pathMap = []

	print(width, depth)
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


def getScoreArea_type1(height_map, min_x, max_x, min_z, max_z, initial_value=None):
	if initial_value == None:
		initial_value = height_map[min_x][min_z]

	ocurred_values = []
	value = 0
	for x in range(min_x, max_x+1):
		for z in range(min_z, max_z+1):
			difference = initial_value - height_map[x][z]
			if difference not in ocurred_values:
				ocurred_values.append(difference)
  	return len(ocurred_values)

def getScoreArea_type2(height_map, min_x, max_x, min_z, max_z, initial_value=None):
	if initial_value == None:
		initial_value = height_map[min_x][min_z]

	value = 0
	for x in range(min_x, max_x+1):
		for z in range(min_z, max_z+1):
			value += abs(initial_value - height_map[x][z])
  	return value

def getScoreArea_type3(height_map, min_x, max_x, min_z, max_z, initial_value=None):
	if initial_value == None:
		initial_value = height_map[min_x][min_z]

	value = 0
	for x in range(min_x, max_x+1):
		for z in range(min_z, max_z+1):

			value += (abs(initial_value - height_map[x][z]))**2
  	return value

def getHeightCounts(matrix, min_x, max_x, min_z, max_z):
	flood_values = {}
	for x in range(min_x, max_x+1):
		for z in range(min_z, max_z+1):
			value = matrix[x][z]
			if not value == -1 :
				if value not in flood_values.keys():
					flood_values[value] = 1
				else:
					flood_values[value] += 1
	return flood_values

def getMostOcurredGroundBlock(matrix, height_map, min_x, max_x, min_z, max_z):
	block_values = {}
	for x in range(min_x, max_x+1):
		for z in range(min_z, max_z+1):
			groundBlock = matrix.getValue(height_map[x][z], x, z)
			if not type(groundBlock) == tuple:
				groundBlock = (groundBlock, 0)
			else :
				groundBlock = (groundBlock[0], 0)
			if groundBlock not in block_values.keys():
				if groundBlock == (179, 0) :
					block_values[BlocksInfo.RED_SAND_ID] = block_values[BlocksInfo.RED_SAND_ID] + 1 if BlocksInfo.RED_SAND_ID in block_values.keys() else  1
				elif groundBlock == (24, 0) :
					block_values[BlocksInfo.SAND_ID] = block_values[BlocksInfo.SAND_ID] + 1 if BlocksInfo.SAND_ID in block_values.keys() else 1
				elif groundBlock == (159, 0) :
					block_values[BlocksInfo.TERRACOTTA_ID] = block_values[BlocksInfo.TERRACOTTA_ID] + 1 if BlocksInfo.TERRACOTTA_ID in block_values.keys() else 1
				else :
					block_values[groundBlock] = 1
			else:
				block_values[groundBlock] += 1
	selected_key = BlocksInfo.GRASS_ID
	max_value = 0
	for key in block_values.keys():
		tmp_value = block_values[key]
		if  tmp_value > max_value :
			max_value = tmp_value
			selected_key = key
	return selected_key


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
    return not (p2[0] >= p1[1] or p2[1] <= p1[0] or p2[3] <= p1[2] or p2[2] >= p1[3])

# returns whether or not 2 partitions are colliding, must be in the format
# (x_min, x_max, z_min, z_max)
def intersectPartitions(p1, p2):
    return not (p2[2] >= p1[3] or p2[3] <= p1[2] or p2[5] <= p1[4] or p2[4] >= p1[5])

def getNonIntersectingPartitions(partitioning):
	cleaned_partitioning = []
	for score, partition in partitioning:
		intersect = False
		for valid_partition in cleaned_partitioning:
			if intersectPartitions(partition, valid_partition):
				intersect = True
				break
		if intersect == False:
			cleaned_partitioning.append(partition)
	return cleaned_partitioning

def fusionIntersectingPartitions(partitioning, height_map):
	cleaned_partitioning = []
	for score, partition in partitioning:
		intersect = False
		for valid_score, valid_partition in cleaned_partitioning:
			if intersectPartitions(partition, valid_partition) :
				if abs(score - valid_score) < 6 :
					x_min = partition[2] if valid_partition[2] > partition[2] else valid_partition[2]
					x_max = partition[3] if valid_partition[3] < partition[3] else valid_partition[3]
					z_min = partition[4] if valid_partition[4] > partition[4] else valid_partition[4]
					z_max = partition[5] if valid_partition[5] < partition[5] else valid_partition[5]
					valid_partition = (valid_partition[0], valid_partition[1], x_min, x_max, z_min, z_max)
					heights = getHeightCounts(height_map, valid_partition[2], valid_partition[3], valid_partition[4], valid_partition[5])
					valid_score = max(heights, key=heights.get)
				intersect = True
		if not intersect :
			cleaned_partitioning.append((score, partition))

	final_partitioning = []
	for valid_score, valid_partition in cleaned_partitioning:
		final_partitioning.append(valid_partition)
	return final_partitioning

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

def getMST_Manhattan(buildings, pathMap, height_map):
	MST = []
	vertices = []
	partitions = deepcopy(buildings)

	selected_vertex = partitions[RNG.randint(0, len(partitions)-1)]
	logging.info("Initial selected partition: {}".format(selected_vertex))
	vertices.append(selected_vertex)
	partitions.remove(selected_vertex)

	while len(partitions) > 0:

		edges = []
		for v in vertices:
			logging.info("v: {}".format(v))
			for p in partitions:
				logging.info("\tp: {}".format(p))
				p1 = v.entranceLot
				p2 = p.entranceLot
				distance = getManhattanDistance((p1[1],p1[2]), (p2[1],p2[2]))
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
	return range(start, stop+1, 1) if (start <= stop) else range(start, stop-1, -1)

def updateHeightMap(height_map, x_min, x_max, z_min, z_max, height):
	for x in range(x_min, x_max+1):
		for z in range(z_min, z_max+1):
			height_map[x][z] = height

def cleanProperty(matrix, h_min, h_max, x_min, x_max, z_min, z_max):
	for h in range(h_min, h_max):
		for x in range(x_min, x_max+1):
			for z in range(z_min, z_max+1):
				matrix.setValue(h,x,z, BlocksInfo.AIR_ID)

def saveTreesInArea(matrix, height_map, new_height, x_min, x_max, z_min, z_max) :
	saved_trees = {}
	for x in range(x_min, x_max + 1) :
		for z in range(z_min, z_max + 1):
			y = height_map[x][z] + 1
			value = matrix.getValue(y, x, z)
			if value in BlocksInfo.LOGS_ID :
				(x_min_tree, x_max_tree, z_min_tree, z_max_tree) = locateWholeTrunk(matrix, y, x, z)
				blocks_to_save = deleteTree(matrix, y, x_min_tree, x_max_tree, z_min_tree, z_max_tree)
				saved_trees[(y, x, z)] = blocks_to_save
	for x in range(x_min, x_max + 1) :
		for z in range(z_min, z_max + 1):
			y = height_map[x][z] + 1
			if y < new_height :
				for tmp_y in range(y, new_height) :
					value = matrix.getValue(tmp_y, x, z)
					if value in BlocksInfo.LEAVES_ID or value in BlocksInfo.LOGS_ID:
						locateAndDeleteTreeFromLeaves(matrix, tmp_y, x, z)
	return saved_trees

def repositionateTrees(matrix, saved_trees, new_height, x_min, x_max, z_min, z_max) :
	for key in saved_trees.keys():
		tree = saved_trees[key]
		height_shifting = (new_height - key[0]) + 1
		if treeInArea(matrix, tree, height_shifting, x_min, x_max, z_min, z_max) :
			for block in tree :
				matrix.setValue(block[0] + height_shifting, block[1], block[2], block[3])

def treeInArea(matrix, tree, height_shifting, x_min, x_max, z_min, z_max):
	for block in tree :
		y = block[0]
		x = block[1]
		z = block[2]
		if x < x_min or x > x_max or z < z_min or z > z_max :
			value = getBlockAndBlockData(matrix, y + height_shifting, x, z)
			if not value == BlocksInfo.AIR_ID :
				return False
	return True

def cleanProperty2(matrix, h_min, h_max, x_min, x_max, z_min, z_max):
	cleanTreeInProperty(matrix, h_min, x_min, x_max, z_min, z_max)
	for h in range(h_min, h_max):
		for x in range(x_min, x_max + 1):
			for z in range(z_min, z_max + 1):
				value = matrix.getValue(h, x, z)
				if type(value) == tuple :
					value = value[0]
				if value in BlocksInfo.LEAVES_ID :
					locateAndDeleteTreeFromLeaves(matrix, h, x, z)
				else :
					matrix.setValue(h,x,z, BlocksInfo.AIR_ID)

def cleanTreeInProperty(matrix, h_min, x_min, x_max, z_min, z_max):
	for x in range(x_min, x_max + 1) :
		for z in range(z_min, z_max + 1) :
			value = matrix.getValue(h_min, x, z)
			if type(value) == tuple :
				value = value[0]
			if value in BlocksInfo.LOGS_ID :
				(x_min_tree, x_max_tree, z_min_tree, z_max_tree) = locateWholeTrunk(matrix, h_min, x, z)
				deleteTree(matrix, h_min, x_min_tree, x_max_tree, z_min_tree, z_max_tree)

def locateWholeTrunk(matrix, h, x, z):
	x_min_tree = x
	x_max_tree = x
	z_min_tree = z
	z_max_tree = z
	x_min = x - 1 if x - 1 > 0 else 0
	x_max = x + 1 if x + 1 < matrix.width else matrix.width - 1
	z_min = z - 1 if z - 1 > 0 else 0
	z_max = z + 1 if z + 1 < matrix.depth else matrix.depth - 1
	cpt = 0
	block_to_verify = []
	for prox_x in range(x_min, x_max + 1, 2) :
		block_to_verify.append((prox_x, z))
	for prox_z in range(z_min, z_max + 1, 2) :
		block_to_verify.append((x, prox_z))
	while cpt < len(block_to_verify) :
		block = block_to_verify[cpt]
		cur_x = block[0]
		cur_z = block[1]
		value = matrix.getValue(h, cur_x, cur_z)
		if type(value) == tuple :
			value = value[0]
		if value in BlocksInfo.LOGS_ID :
			x_min_tree = prox_x if prox_x < x_min_tree else x_min_tree
			x_max_tree = prox_x if prox_x > x_max_tree else x_max_tree
			z_min_tree = prox_z if prox_z < z_min_tree else z_min_tree
			z_max_tree = prox_z if prox_z > z_max_tree else z_max_tree
			if (cur_x == x - 1 or cur_x == x + 1) and (cur_x, z_min) not in block_to_verify and cur_z == z :
				block_to_verify.append((cur_x, z_min))
				block_to_verify.append((cur_x, z_max))
			elif (cur_z == z - 1 or cur_z == z + 1) and (x_min, cur_z) not in block_to_verify and cur_x == x :
				block_to_verify.append((x_min, cur_z))
				block_to_verify.append((x_max, cur_z))
		cpt += 1
	return (x_min_tree, x_max_tree, z_min_tree, z_max_tree)

def locateAndDeleteTreeFromLeaves(matrix, leaves_h, leaves_x, leaves_z) :
	targeted_leaves = getBlockAndBlockData(matrix, leaves_h, leaves_x, leaves_z)
	modulo = 4 if targeted_leaves[0] == 18 else 2
	if targeted_leaves[0] in BlocksInfo.LEAVES_ID :
		targeted_leaves = (targeted_leaves[0], targeted_leaves[1] % modulo)
		targeted_logs = BlocksInfo.getLogIdFromLeaves(targeted_leaves)
	elif targeted_leaves[0] in BlocksInfo.LOGS_ID :
		targeted_logs = targeted_leaves
		targeted_leaves = BlocksInfo.getBushId('None', BlocksInfo.getWoodName(targeted_logs))
	tree_blocks = []
	index = 0
	scan_size = 10
	find = False
	block_to_verify = [(leaves_h, leaves_x, leaves_z)]
	logging.info("searching for trees with leaves at {}".format((leaves_h, leaves_x, leaves_z)))
	x_min = leaves_x - scan_size
	x_max = leaves_x + scan_size
	z_min = leaves_z - scan_size
	z_max = leaves_z + scan_size
	while index < len(block_to_verify) and not find :
		block = block_to_verify[index]
		y = block[0]
		x = block[1]
		z = block[2]
		value = getBlockAndBlockData(matrix, y, x, z)
		if value[0] == targeted_leaves[0] and value[1] % modulo == targeted_leaves[1]:
			if x <= x_max and x >= x_min :
				if x - 1 >= 0 and (y, x - 1, z) not in block_to_verify :
					block_to_verify.append((y, x - 1, z))
				if x + 1 < matrix.width and (y, x + 1, z) not in block_to_verify :
					block_to_verify.append((y, x + 1, z))
			if z <= z_max and z >= z_min :
				if z - 1 >= 0 and (y, x, z - 1) not in block_to_verify :
					block_to_verify.append((y, x, z - 1))
				if z + 1 < matrix.depth and (y, x, z + 1) not in block_to_verify :
					block_to_verify.append((y, x, z + 1 if z + 1 < matrix.depth else matrix.depth - 1))
			if (y - 1, x, z) not in block_to_verify :
				block_to_verify.append((y - 1, x, z))
			if (y + 1, x, z) not in block_to_verify :
				block_to_verify.append((y + 1, x, z))
		elif value == targeted_logs :
			logging.info("find log {} at {}".format(value, (y, x, z)))
			possible_trunk_base = [(y, x, z)]
			cpt = 0
			while not find and cpt < len(possible_trunk_base):
				block = possible_trunk_base[cpt]
				y = block[0]
				x = block[1]
				z = block[2]
				value = getBlockAndBlockData(matrix, y, x, z)
				if value == targeted_logs :
					next_value = getBlockAndBlockData(matrix, y - 1, x, z)
					possible_trunk_base.append((y - 1, x, z))
					if next_value[0] in ground_like :
						logging.info("find trunk base at {}".format((x, y, z)))
						(x_min_tree, x_max_tree, z_min_tree, z_max_tree) = locateWholeTrunk(matrix, y, x, z)
						tree_blocks.extend(deleteTree(matrix, y, x_min_tree, x_max_tree, z_min_tree, z_max_tree))
						find = True
					elif not next_value == targeted_logs :
						for tmp_y in range(y - 1, y + 1, 1) :
							if x + 1 < matrix.width and (tmp_y, x + 1, z) not in possible_trunk_base :
								possible_trunk_base.append((tmp_y, x + 1, z))
							if x - 1 >= 0 and (tmp_y, x - 1, z) not in possible_trunk_base :
								possible_trunk_base.append((tmp_y, x - 1, z))
							if z + 1 < matrix.depth and (tmp_y, x, z + 1) not in possible_trunk_base :
								possible_trunk_base.append((tmp_y, x, z + 1))
							if z - 1 >= 0 and (tmp_y, x, z - 1) not in possible_trunk_base :
								possible_trunk_base.append((tmp_y, x, z - 1))
							if x + 1 < matrix.width and z - 1 >= 0 and (tmp_y, x + 1, z - 1) not in possible_trunk_base :
								possible_trunk_base.append((tmp_y, x + 1, z - 1))
							if x - 1 >= 0 and z + 1 < matrix.depth and (tmp_y, x - 1, z + 1) not in possible_trunk_base :
								possible_trunk_base.append((tmp_y, x - 1, z + 1))
							if x + 1 < matrix.width and z + 1 < matrix.depth and (tmp_y, x + 1, z + 1) not in possible_trunk_base :
								possible_trunk_base.append((tmp_y, x + 1, z + 1))
							if x - 1 >= 0 and z - 1 >= 0 and (tmp_y, x - 1, z - 1) not in possible_trunk_base :
								possible_trunk_base.append((tmp_y, x - 1, z - 1))
				cpt += 1
		index += 1
	logging.info("tree with leaf at {} deleted".format((leaves_h, leaves_x, leaves_z)))
	return tree_blocks

#Delete the tree whose trunk is located in the given range of coordinates
def deleteTree(matrix, h, x_min, x_max, z_min, z_max):
	tree_type = getBlockAndBlockData(matrix, h, x_min, z_min)
	targeted_leaves = BlocksInfo.getBushId('None', BlocksInfo.getWoodName(tree_type))
	modulo = 4 if targeted_leaves[0] == 18 else 2
	tree_blocks = []
	if tree_type == BlocksInfo.getWoodId('acacia') :
		logging.info("deleting acacia tree")
		block_to_verify = [(h, x_min, z_min)]
		while len(block_to_verify) > 0 :
			block = block_to_verify.pop(0)
			y = block[0]
			x = block[1]
			z = block[2]
			value = getBlockAndBlockData(matrix, y, x, z)
			if value == tree_type :
				matrix.setValue(y, x, z, BlocksInfo.AIR_ID)
				tree_blocks.append((y, x, z, tree_type))
				block_to_verify.extend(getAllBlockAround(matrix, y, y + 1, x, z, "Cross"))
				block_to_verify.append((y + 1, x, z))
			elif value[0] == targeted_leaves[0] and value[1] % modulo == targeted_leaves[1] :
				matrix.setValue(y, x, z, BlocksInfo.AIR_ID)
				tree_blocks.append((y, x, z, targeted_leaves))
				block_to_verify.extend(getAllBlockAround(matrix, y, y, x, z, "Cross"))

	elif tree_type == BlocksInfo.getWoodId('dark_oak') :
		logging.info("deleting dark oak tree")
		scan_size = 4
		block_to_verify = []
		for x in range(x_min, x_max + 1) :
			for z in range(z_min, z_max + 1) :
				block_to_verify.append((h, x, z))
		trunk_blocks = []
		branch_blocks = []
		max_y = h
		while len(block_to_verify) > 0 :
			block = block_to_verify.pop(0)
			y = block[0]
			x = block[1]
			z = block[2]
			value = getBlockAndBlockData(matrix, y, x, z)
			if value == tree_type :
				matrix.setValue(y, x, z, BlocksInfo.AIR_ID)
				trunk_blocks.append((y, x, z))
				tree_blocks.append((y, x, z, tree_type))
				block_to_verify.extend(getAllBlockAround(matrix, y, y, x, z, "Circle"))
				block_to_verify.append((y + 1, x, z))
				if y > max_y :
					max_y = y
		top_blocks = []
		for block in trunk_blocks :
			if block[0] == max_y :
				top_blocks.append(block)

		for block in top_blocks :
			next = True
			tmp_y = max_y + 1
			x = block[1]
			z = block[2]
			while next :
				next = False
				value = getBlockAndBlockData(matrix, tmp_y, x, z)
				if value[0] == targeted_leaves[0] and value[1] % modulo == targeted_leaves[1] :
					matrix.setValue(tmp_y, x, z, BlocksInfo.AIR_ID)
					trunk_blocks.append((tmp_y, x, z))
					tree_blocks.append((tmp_y, x, z, targeted_leaves))
					next = True
				tmp_y += 1

		for block in trunk_blocks :
			y = block[0]
			x = block[1]
			z = block[2]
			tmp_scan_size = scan_size
			tree_blocks.extend(deleteLeaves(matrix, y, x, z, tree_type, tmp_scan_size, "E"))
			tree_blocks.extend(deleteLeaves(matrix, y, x, z, tree_type, tmp_scan_size, "W"))
			tree_blocks.extend(deleteLeaves(matrix, y, x, z, tree_type, tmp_scan_size, "S"))
			tree_blocks.extend(deleteLeaves(matrix, y, x, z, tree_type, tmp_scan_size, "N"))

	elif tree_type == BlocksInfo.getWoodId('oak') :
		logging.info("deleting oak tree")
		block_to_verify = [(h, x_min, z_min)]
		trunk_blocks = []
		branch = False
		while len(block_to_verify) > 0 :
			block = block_to_verify.pop(0)
			y = block[0]
			x = block[1]
			z = block[2]
			value = getBlockAndBlockData(matrix, y, x, z)
			if x == x_min and x == x_max and z == z_min and z == z_max :
				if value == tree_type or value[0] == targeted_leaves[0] and value[1] % modulo == targeted_leaves[1] and not (y, x, z) in trunk_blocks:
					trunk_blocks.append((y, x, z))
					block_to_verify.extend(getAllBlockAround(matrix, y, y, x, z, "Circle"))
					block_to_verify.append((y + 1, x, z))
			else :
				if getLogRealId(value, tree_type) == tree_type:
					branch = True

		if not branch :
			scan_size = 2
			for block in trunk_blocks :
				y = block[0]
				x = block[1]
				z = block[2]
				tree_blocks.append((y, x, z, getBlockAndBlockData(matrix, y, x, z)))
				matrix.setValue(y, x, z, BlocksInfo.AIR_ID)
				if x - 1 >= 0 :
					tree_blocks.extend(deleteLeaves(matrix, y, x, z, tree_type, scan_size, "W"))
				if x + 1 < matrix.width :
					tree_blocks.extend(deleteLeaves(matrix, y, x, z, tree_type, scan_size, "E"))
				if z + 1 < matrix.depth :
					tree_blocks.extend(deleteLeaves(matrix, y, x, z, tree_type, scan_size, "S"))
				if z - 1 >= 0 :
					tree_blocks.extend(deleteLeaves(matrix, y, x, z, tree_type, scan_size, "N"))
		else :
			# we will delete all the tree adjacent oak tree since it's to hard to delete a big oak properly
			block_to_verify.extend(trunk_blocks)
			while len(block_to_verify) > 0 :
				block = block_to_verify.pop(0)
				y = block[0]
				x = block[1]
				z = block[2]
				value = getBlockAndBlockData(matrix, y, x, z)
				if (value[0] == targeted_leaves[0] and value[1] % modulo == targeted_leaves[1]) or getLogRealId(value, tree_type) == tree_type:
					matrix.setValue(y, x, z, BlocksInfo.AIR_ID)
					tree_blocks.append((y, x, z, value))
					block_to_verify.extend(getAllBlockAround(matrix, y - 1, y + 1, x, z, "Circle"))
					block_to_verify.append((y + 1, x, z))
					block_to_verify.append((y - 1, x, z))
				else :
					clearVine(matrix, y, x, z)

	elif tree_type == BlocksInfo.getWoodId('jungle') and not x_min == x_max and not z_min == z_max :
		logging.info("deleting size 2 jungle tree")
		scan_size = 5
		block_to_verify = []
		for x in range(x_min, x_max + 1) :
			for z in range(z_min, z_max + 1) :
				block_to_verify.append((h, x, z))
		trunk_blocks = []
		branch_blocks = []
		max_y = h
		while len(block_to_verify) > 0 :
			block = block_to_verify.pop(0)
			y = block[0]
			x = block[1]
			z = block[2]
			value = getBlockAndBlockData(matrix, y, x, z)
			if x >= x_min and x <= x_max and z >= z_min and z <= z_max :
				if value == tree_type :
					matrix.setValue(y, x, z, BlocksInfo.AIR_ID)
					trunk_blocks.append((y, x, z, getDirections(x, z, x_min, x_max, z_min, z_max)))
					tree_blocks.append((y, x, z, tree_type))
					block_to_verify.extend(getAllBlockAround(matrix, y, y, x, z, "Circle"))
					block_to_verify.append((y + 1, x, z))
				elif value[0] == targeted_leaves[0] and value[1] % modulo == targeted_leaves[1] :
					matrix.setValue(y, x, z, BlocksInfo.AIR_ID)
					trunk_blocks.append((y, x, z, getDirections(x, z, x_min, x_max, z_min, z_max)))
					tree_blocks.append((y, x, z, targeted_leaves))
					block_to_verify.append((y + 1, x, z))
					if y > max_y :
						max_y = y
			else :
				if getLogRealId(value, tree_type) == tree_type :
					matrix.setValue(y, x, z,  BlocksInfo.AIR_ID)
					branch_blocks.append((y, x, z))
					tree_blocks.append((y, x, z, value))
					block_to_verify.extend(getAllBlockAround(matrix, y, y + 1, x, z, "Circle"))
					block_to_verify.append((y + 1, x, z))

		for block in trunk_blocks :
			for direction in block[3] :
				if block[0] >= max_y - 2 :
					tree_blocks.extend(deleteLeaves(matrix, block[0], block[1], block[2], tree_type, scan_size, direction))
				else :
					if direction == "N" and block[2] - 1 >= 0 :
						clearVine(matrix, block[0], block[1], block[2] - 1)
					elif direction == "S" and block[2] + 1 < matrix.depth :
						clearVine(matrix, block[0], block[1], block[2] + 1)
					elif direction == "E" and block[1] + 1 < matrix.width :
						clearVine(matrix, block[0], block[1] + 1, block[2])
					elif direction == "W" and block[1] - 1 >= 0 :
						clearVine(matrix, block[0], block[1] - 1, block[2])

		scan_size = 4
		branch_at_height = {}
		for block in branch_blocks :
			y = block[0]
			x = block[1]
			z = block[2]
			block_to_verify.extend(getAllBlockAround(matrix, y, y, x, z, "Cross"))
			if y not in branch_at_height.keys() :
				branch_at_height[y] = (y, x, z, calculate_distance(x_min, x_max, z_min, z_max, x, z))
			else :
				dist = calculate_distance(x_min, x_max, z_min, z_max, x, z)
				if dist > branch_at_height[y][3] :
					branch_at_height[y] = (y, x, z, dist)
		while len(block_to_verify) > 0 :
			block = block_to_verify.pop(0)
			y = block[0]
			x = block[1]
			z = block[2]
			value = getBlockAndBlockData(matrix, y, x, z)
			if value[0] == targeted_leaves[0] and value[1] % modulo == targeted_leaves[1] :
				matrix.setValue(y, x, z, BlocksInfo.AIR_ID)
				tree_blocks.append((y, x, z, value))
				cpt = 0
				while y - cpt not in branch_at_height.keys() and y - cpt > 0:
					cpt += 1
				scan_ref = branch_at_height[y - cpt]
				if x + 1 <= scan_ref[1] + scan_size :
					block_to_verify.append((y, x + 1 if x + 1 < matrix.width else matrix.width - 1, z))
				if x - 1 >= scan_ref[1] - scan_size :
					block_to_verify.append((y, x - 1 if x - 1 >= 0 else 0, z))
				if z + 1 <= scan_ref[2] + scan_size :
					block_to_verify.append((y, x, z + 1 if z + 1 < matrix.depth else matrix.depth - 1))
				if z - 1 >= scan_ref[2] - scan_size :
					block_to_verify.append((y, x, z - 1 if z - 1 >= 0 else 0))
				block_to_verify.append((y + 1, x, z))
			else :
				clearVine(matrix, y, x, z)

	else :
		logging.info("deleting birch or spruce or simple jungle tree with log id {}".format(tree_type))
		scan_size = 3 if tree_type == BlocksInfo.getWoodId('spruce') else 2
		(h_min, h_max) = h, h
		finish = False
		while not finish :
			finish = True
			value1 = getBlockAndBlockData(matrix, h_min - 1, x_min, z_min)
			value2 = getBlockAndBlockData(matrix, h_max + 1, x_min, z_min)
			if value1 == tree_type :
				h_min -= 1
				finish = False
			if (value2[0] == tree_type[0] and value2[1] == tree_type[1]) or (value2[0] == targeted_leaves[0] and value2[1] % modulo == targeted_leaves[1]):
				h_max += 1
				finish = False

		for y in range(h_min, h_max + 1) :
			for x in range(x_min, x_max + 1) :
				for z in range(z_min, z_max + 1):
					tree_blocks.append((y, x, z, getBlockAndBlockData(matrix, y, x, z)))
					matrix.setValue(y, x, z, BlocksInfo.AIR_ID)
					if x == x_max and x + 1 < matrix.width :
						if not clearVine(matrix, y, x + 1, z) :
							tree_blocks.extend(deleteLeaves(matrix, y, x, z, tree_type, scan_size, "E"))
					if x == x_min and x - 1 >= 0 :
						if not clearVine(matrix, y, x - 1, z):
							tree_blocks.extend(deleteLeaves(matrix, y, x, z, tree_type, scan_size, "W"))
					if z == z_min and z - 1 >= 0:
						if not clearVine(matrix, y, x, z - 1) :
							tree_blocks.extend(deleteLeaves(matrix, y, x, z, tree_type, scan_size, "N"))
					if z == z_max and z + 1 < matrix.depth :
						if not clearVine(matrix, y, x, z + 1) :
							tree_blocks.extend(deleteLeaves(matrix, y, x, z, tree_type, scan_size, "S"))
	return tree_blocks

def getAllBlockAround(matrix, y_min, y_max, x, z, type) :
	blocks = []
	x_plus = x + 1 < matrix.width
	x_minus = x - 1 >= 0
	z_plus = z + 1 < matrix.depth
	z_minus = z - 1 >= 0

	for prox_y in range(y_min, y_max + 1) :
		if x_plus :
			blocks.append((prox_y, x + 1, z))
		if x_minus :
			blocks.append((prox_y, x - 1, z))
		if z_plus :
			blocks.append((prox_y, x, z + 1))
		if z_minus :
			blocks.append((prox_y, x, z - 1))
		if type == "Circle" :
			if z_plus :
				if x_plus :
					blocks.append((prox_y, x + 1, z + 1))
				if x_minus :
					blocks.append((prox_y, x - 1, z + 1))
			if z_minus :
				if x_plus :
					blocks.append((prox_y, x + 1, z - 1))
				if x_minus :
					blocks.append((prox_y, x - 1, z - 1))
	return blocks

def calculate_distance(x_min, x_max, z_min, z_max, x, z) :
	if x >= x_max :
		x_dist = x - x_max
	elif x <= x_min :
		x_dist = x_min - x
	if z >= z_max :
		z_dist = z - z_max
	elif z <= z_min :
		z_dist = z_min - z
	return x_dist + z_dist

def getDirections(x, z, x_min, x_max, z_min, z_max) :
	directions = []
	if x == x_max :
		directions.append("E")
	if x == x_min :
		directions.append("W")
	if z == z_min :
		directions.append("N")
	if z == z_max :
		directions.append("S")
	return directions

def getLogRealId(value, tree_type):
	if value[0] == tree_type[0] :
		sub_value = value[1]
		sub_value = sub_value - 8 if sub_value >= 8 else sub_value
		sub_value = sub_value - 4 if sub_value >= 4 else sub_value
		return (value[0], sub_value)
	return value

def clearVine(matrix, h, x, z):
	logging.info("y = {}, x = {}, z = {} and width = {}, height = {} and depth = {}".format(h, x, z, matrix.width, matrix.height, matrix.depth))
	value = matrix.getValue(h, x, z)
	if type(value) == tuple :
		value = value[0]
	if value == BlocksInfo.VINES_ID or value == BlocksInfo.COCOA_ID :
		matrix.setValue(h, x, z, BlocksInfo.AIR_ID)
		return True
	return False

def deleteLeaves(matrix, trunk_h, trunk_x, trunk_z, tree_type, searching_area_size, direction):
	targeted_leaves = BlocksInfo.getBushId('None', BlocksInfo.getWoodName(tree_type))
	modulo = 4 if targeted_leaves[0] == 18 else 2
	block_to_verify = []
	if direction == "N" :
		block_to_verify.append((trunk_h, trunk_x, trunk_z - 1))
	elif direction == "S" :
		block_to_verify.append((trunk_h, trunk_x, trunk_z + 1))
	elif direction == "E" :
		block_to_verify.append((trunk_h, trunk_x + 1, trunk_z))
	elif direction == "W" :
		block_to_verify.append((trunk_h, trunk_x -1, trunk_z))
	found_leaves = []
	logging.info("###### {}".format(direction))
	while len(block_to_verify) > 0 :
		block = block_to_verify.pop(0)
		logging.info("number of block to verify {}".format(len(block_to_verify)))
		y = block[0]
		x = block[1]
		z = block[2]
		value = getBlockAndBlockData(matrix, y, x, z)
		if value[0] == targeted_leaves[0] and value[1] % modulo == targeted_leaves[1]:
			matrix.setValue(y, x, z, BlocksInfo.AIR_ID)
			found_leaves.append((y, x, z, value))
			if x + 1 <= trunk_x + searching_area_size and (direction == "S" or direction == "N" or direction == "E") :
				block_to_verify.append((y, x + 1 if x + 1 < matrix.width else matrix.width - 1, z))
			if x - 1 >= trunk_x - searching_area_size and (direction == "S" or direction == "N" or direction == "W") :
				block_to_verify.append((y, x - 1 if x - 1 > 0 else 0, z))
			if z + 1 <= trunk_z + searching_area_size and (direction == "S" or direction == "E" or direction == "W") :
				block_to_verify.append((y, x, z + 1 if z + 1 < matrix.depth else matrix.depth - 1))
			if z - 1 >= trunk_z - searching_area_size and (direction == "N" or direction == "E" or direction == "W"):
				block_to_verify.append((y, x, z - 1 if z - 1 > 0 else 0))
		else :
			clearVine(matrix, y, x, z)
	return found_leaves

def getBlockAndBlockData(matrix, y, x, z) :
	if matrix.isChanged(y, x, z) :
		value = matrix.getValue(y, x, z)
		if not type(value) == tuple :
			value = (value, 0)
		return value
	else :
		y = matrix.getWorldY(y)
		x = matrix.getWorldX(x)
		z = matrix.getWorldZ(z)
		return (matrix.level.blockAt(x, y, z), matrix.level.blockDataAt(x, y, z))

def selectRandomWood(usable_wood) :
	selected = RNG.randint(0, 100)
	current = 0
	for key in usable_wood.keys():
		 current += usable_wood[key]
		 if current >= selected :
			 return BlocksInfo.getWoodName(key)
	logging.info("Error in select random Wood no result obtained !")
	return None

# algorithm to randomly find flat areas given a height map
def getAreasSameHeight(box,terrain):
	validAreas = []

	for i in range(0, 1000):
		random_x = RNG.randint(0, box.maxx-box.minx)
		random_z = RNG.randint(0,box.maxz-box.minz)
		size_x = 15
		size_z = 15
		if checkSameHeight(terrain, 0, box.maxx-box.minx, 0,box.maxz-box.minz, random_x, random_z, size_x, size_z):
			newValidArea = (random_x, random_x+size_x-1, random_z, random_z+size_z-1)
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
