import utilityFunctions
import logging
import BlocksInfo as BlocksInfo

# Perform earthworks on a given lot, returns the height to start construction
def prepareLot(matrix, p, height_map, biome):

	areaScore = utilityFunctions.getScoreArea_type1(height_map, p[2],p[3], p[4], p[5], height_map[p[2]][p[4]])
	logging.info("Preparing lot {} with score {}".format(p, areaScore))

	if areaScore != 0:
		terrain_height = flattenPartition(matrix, p[2],p[3], p[4], p[5], height_map, biome)
		logging.info("Terrain was flattened at height {}".format(terrain_height))
		utilityFunctions.updateHeightMap(height_map, p[2], p[3], p[4], p[5], terrain_height)
		h = matrix.getMatrixY(terrain_height)
	else:
		heightCounts = utilityFunctions.getHeightCounts(height_map, p[2],p[3], p[4], p[5])
		terrain_height = max(heightCounts, key=heightCounts.get)
		logging.info("No changes in terrain were necessary, terrain at height {}".format(terrain_height))
		utilityFunctions.updateHeightMap(height_map, p[2], p[3], p[4], p[5], terrain_height)
		# update the ground with the grass block
		for x in range(x_min, x_max):
			for z in range(z_min,z_max):
				matrix.setValue(terrain_height, x, z, ground)
		h = matrix.getMatrixY(terrain_height)


	logging.info("Index of height {} in selection box matrix: {}".format(terrain_height, h))

	return h

def prepareArea(matrix, p, height_map, biome):
	terrain_height = flattenPartition(matrix, p[2],p[3], p[4], p[5], height_map, biome, 6)
	logging.info("Terrain was flattened at height {}".format(terrain_height))
	utilityFunctions.updateHeightMap(height_map, p[2], p[3], p[4], p[5], terrain_height)

# Given the map matrix, a partition (x_min, x_max, z_min, z_max) and a
# height_map, perform earthworks on this lot by the flattening
# returns the height in which construction should start
def flattenPartition(matrix, x_min, x_max, z_min, z_max, height_map, biome, shifting = 12):
	x_min_height_count = x_min - shifting if x_min - shifting >= 0 else 0
	x_max_height_count = x_max + shifting if x_max + shifting < matrix.width else matrix.width - 1
	z_min_height_count = z_min - shifting if z_min - shifting >= 0 else 0
	z_max_height_count = z_max + shifting if z_max + shifting < matrix.depth else matrix.depth - 1
	heightCounts = utilityFunctions.getHeightCounts(height_map, x_min_height_count, x_max_height_count, z_min_height_count, z_max_height_count)

	average_height = max(heightCounts, key=heightCounts.get)
	#count = 0
	#for key in heightCounts.keys() :
	#	value = heightCounts[key]
	#	if value > round((x_max_height_count - x_min_height_count) * (z_max_height_count - z_min_height_count) * 0.01) :
	#		average_height += key * value
	#		count += value
	#average_height = average_height / count

	logging.info("Flattening {}".format((x_min, x_max, z_min, z_max)))

	base_block = utilityFunctions.getMostOcurredGroundBlock(matrix, height_map, x_min, x_max, z_min, z_max)
	if base_block == BlocksInfo.SAND_ID and biome == 'Badlands' :
		base_block = BlocksInfo.RED_SAND_ID
	elif base_block == BlocksInfo.DIRT_ID and biome == 'Taiga' :
		base_block = BlocksInfo.PODZOL_ID

	if base_block == BlocksInfo.TERRACOTTA_ID :
		 #Temporary need change
		 underground_block = BlocksInfo.TERRACOTTA_ID
	else :
		underground_block = BlocksInfo.getUndergroundBlockId(base_block)
	logging.info("Most occurred ground block: {}".format(base_block))
	logging.info("Flattening at height {}".format(average_height))

	saved_trees = utilityFunctions.saveTreesInArea(matrix, height_map, average_height, x_min, x_max, z_min, z_max)

	for x in range(x_min, x_max):
		for z in range(z_min,z_max):
			if height_map[x][z] == average_height:
				# Equal height! No flattening needed
				# but lets use the base block just in case
				matrix.setValue(height_map[x][z], x, z, base_block)
			if height_map[x][z] != average_height:

				if height_map[x][z] == -1:
					logging.warning("Flattening invalid area. Position ", x, z, " of height_map is -1. Cannot do earthworks.")
					continue

				matrix_height = matrix.getMatrixY(height_map[x][z])
				desired_matrix_height = matrix.getMatrixY(average_height)

				if desired_matrix_height > matrix_height:
					for y in range(matrix_height, desired_matrix_height):
						matrix.setValue(y,x,z, underground_block)
					matrix.setValue(desired_matrix_height, x, z, base_block)
				else:
					for y in range(matrix.height-1, desired_matrix_height, -1):
						value = utilityFunctions.getBlockAndBlockData(matrix, y, x, z)
						if type(value) == tuple :
							value = value[0]
						if not value in BlocksInfo.LEAVES_ID :
							matrix.setValue(y, x, z, BlocksInfo.AIR_ID)
					matrix.setValue(desired_matrix_height,x,z, base_block)

	utilityFunctions.repositionateTrees(matrix, saved_trees, average_height, x_min, x_max, z_min, z_max)

	return average_height
