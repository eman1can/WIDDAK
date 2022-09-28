import toolbox
import logging

# Perform earthworks on a given lot, returns the height to start construction
def prepareLot(matrix, p, height_map, block):

	areaScore = toolbox.getScoreArea_type4(height_map, p[2],p[3], p[4], p[5])
	logging.info("Preparing lot {} with score {}".format(p, areaScore))

	if areaScore != 0:
		terrain_height = flattenPartition(matrix, p[2],p[3], p[4], p[5], height_map, block)
		logging.info("Terrain was flattened at height {}".format(terrain_height))
		toolbox.updateHeightMap(height_map, p[2], p[3], p[4], p[5], terrain_height)
		h = matrix.getMatrixY(terrain_height)
	else:
		heightCounts = toolbox.getHeightCounts(height_map, p[2],p[3], p[4], p[5])
		terrain_height = max(heightCounts, key=heightCounts.get)
		logging.info("No changes in terrain were necessary, terrain at height {}".format(terrain_height))
		toolbox.updateHeightMap(height_map, p[2], p[3], p[4], p[5], terrain_height)
		# update the ground with the most occured block
		if block == None:
			block = toolbox.getMostOcurredGroundBlock(matrix, height_map, p[2],p[3], p[4], p[5])
			if block == (3, 0):
				block = (2, 0)
		for x in range(p[2], p[3]+1):
			for z in range(p[4], p[5]+1):
				matrix.setValue(terrain_height, x, z, block)
		h = matrix.getMatrixY(terrain_height)


	logging.info("Index of height {} in selection box matrix: {}".format(terrain_height, h))

	return h

# Given the map matrix, a partition (x_min, x_max, z_min, z_max) and a
# height_map, perform earthworks on this lot by the flattening
# returns the height in which construction should start
def flattenPartition(matrix, x_min, x_max, z_min, z_max, height_map, deep_block):

	heightCounts = toolbox.getHeightCounts(height_map, x_min, x_max, z_min, z_max)
	most_ocurred_height = max(heightCounts, key=heightCounts.get)

	logging.info("Flattening {}".format((x_min, x_max, z_min, z_max)))

	top_block = deep_block
	if deep_block == None:
		top_block = deep_block = toolbox.getMostOcurredGroundBlock(matrix, height_map, x_min, x_max, z_min, z_max)
	if deep_block == (3, 0):
		top_block = (2, 0)
	elif deep_block == (2, 0):
		deep_block = (3, 0)
	logging.info("Most occurred ground block: {}".format(deep_block))
	logging.info("Flattening at height {}".format(most_ocurred_height))

	for x in range(x_min, x_max+1):
		for z in range(z_min,z_max+1):
			if height_map[x][z] == -1:
				logging.warning("Flattening invalid area. Position ", x, z, " of height_map is -1. Cannot do earthworks.")
				continue

			matrix_height = matrix.getMatrixY(height_map[x][z])
			desired_matrix_height = matrix.getMatrixY(most_ocurred_height)

			if desired_matrix_height > matrix_height:
				for y in range(matrix_height, desired_matrix_height):
					matrix.setValue(y,x,z, deep_block)
			else:
				#update every block between top height and the desired height
				# when bringing the ground to a lower level, this will have the
				# effect of e.g. erasing trees that were on top of that block
				# this may cause some things to be unproperly erased
				# (e.g. a branch of a tree coming from an nearby block)
				# but this is probably the best/less complex solution for this
				for y in range(matrix.height-1, desired_matrix_height, -1):
					matrix.setValue(y,x,z, 0)
			matrix.setValue(desired_matrix_height, x, z, top_block)

	return most_ocurred_height
