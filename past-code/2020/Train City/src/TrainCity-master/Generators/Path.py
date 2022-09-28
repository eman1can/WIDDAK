import logging
import toolbox as toolbox
import utility as utility

IDs = utility.IDs
air_like = [IDs["air"], IDs["water"], IDs["log"], IDs["leaves"], IDs["web"], IDs["tallgrass"], IDs["deadbush"],  IDs["yellow_flower"], IDs["flower"], IDs["brown_mushroom"], IDs["red_mushroom"], IDs["wheat"], IDs["cactus"], IDs["reeds"], IDs["oak_fence"], IDs["melon_block"], IDs["pumpkin_stem"], IDs["melon_stem"], IDs["vine"], IDs["oak_fence_gate"], IDs["waterlily"], IDs["carrots"], IDs["potatoes"], IDs["leaves2"], IDs["log2"], IDs["double_plant"], IDs["snow"], IDs["ice"]]
ground_like = [IDs["stone"], IDs["grass"], IDs["dirt"]]
water_like = [IDs["flowing_water"], IDs["water"], IDs["flowing_lava"], IDs["lava"]]
light_pillar_like = [IDs["oak_fence"],  IDs["cobblestone_wall"], IDs["redstone_lamp"], IDs["daylight_detector_inverted"]]

def generatePath_StraightLine(matrix, x_p1, z_p1, x_p2, z_p2, height_map, pavement_Type):
	if pavement_Type == "Grass":
		pavement_Block = toolbox.getBlockID("grass_path")
		light_Pillar = toolbox.getBlockID("oak_fence")
	elif pavement_Type == "Stone":
		pavement_Block = toolbox.getBlockID("stone", 6)
		light_Pillar = toolbox.getBlockID("cobblestone_wall")

	for x in toolbox.twoway_range(x_p1, x_p2):
		h = height_map[x][z_p1]
		h = matrix.getMatrixY(h)
		matrix.setValue(h, x, z_p1, pavement_Block)

	for z in toolbox.twoway_range(z_p1, z_p2):
		h = height_map[x_p2][z]
		h = matrix.getMatrixY(h)
		matrix.setValue(h, x_p2, z, pavement_Block)
		matrix.setValue(h + 1, x_p2, z, toolbox.getBlockID("air"))

def generatePath(matrix, path, height_map, pavement_Type):
	air = toolbox.getBlockID("air")
	if pavement_Type == "Grass":
		pavement_Block = toolbox.getBlockID("grass_path")
		baseBlock = toolbox.getBlockID("dirt")
		light_Pillar = toolbox.getBlockID("oak_fence")
	elif pavement_Type == "Stone":
		pavement_Block = toolbox.getBlockID("stone", 6)
		baseBlock = toolbox.getBlockID("stone")
		light_Pillar = toolbox.getBlockID("cobblestone_wall")

	def fillUnderneath(matrix, y, x, z):
		if y < 0: return
		block = matrix.getValue(y, x, z)
		if type(block) == tuple: block = block[0]
		if block in air_like or block in water_like:
			matrix.setValue(y, x, z, baseBlock)
			fillUnderneath(matrix, y - 1, x, z)

	def fillAbove(matrix, y, x, z, up_to):
		if up_to < 0 or y >= matrix.height: return
		block = matrix.getValue(y, x, z)
		if type(block) == tuple: block = block[0]
		if block in air_like:
			matrix.setValue(y, x, z, air)
		fillAbove(matrix, y + 1, x, z, up_to-1)

	def getOrientation(x1, z1, x2, z2):
		if x1 < x2:   return "E"
		elif x1 > x2: return "W"
		elif z1 < z2: return "S"
		elif z1 > z2: return "N"
		else: return None

	def generateLight(matrix, block_section, path, height_map): #generate a light by using the center of mass if it is possible
		(x, z) = computeCenterOfMass(block_section)

		if height_map[x][z] != -1 and matrix.getValue(height_map[x][z] + 1, x, z) not in light_pillar_like+[65] and matrix.getValue(height_map[x][z] - 1, x, z) not in air_like: #validity of the center of mass
			if isNeighborLight(matrix,height_map, x, z) != True:
				buildLight(matrix, height_map[x][z], x, z)
		else:
			(x, z) = findPos(matrix, x, z, path, height_map)
			if (x, z) != (-1, -1):
				if isNeighborLight(matrix,height_map, x, z) != True:
					buildLight(matrix, height_map[x][z], x, z)
			else:
				return False

	def buildLight(matrix, h, x, z): #put the light at the position given
		logging.info("Generating light at point {}, {}, {}".format(h+1, x, z))
		try:
			matrix.setValue(h + 1, x, z, light_Pillar)
			matrix.setValue(h + 2, x, z, light_Pillar)
			matrix.setValue(h + 3, x, z, toolbox.getBlockID("redstone_lamp"))
			matrix.setEntity(h + 4, x, z, toolbox.getBlockID("daylight_detector_inverted", 15), "daylight_detector")
		except:
			logging.info("Error when generating light at position : {}, {}, {}".format(h+1, x, z))

	def computeCenterOfMass(block_section): #compute the center of gravity to have a general idea of where a light could be put
		x = 0
		z = 0
		for i in range(0, len(block_section)):
			x += block_section[i][0]
			z += block_section[i][1]
		x = int(round(x / len(block_section)))
		z = int(round(z / len(block_section)))
		return (x, z)

	def findPos(matrix, x, z, path, height_map): #try to find a position next to the one given that is suitable for building a light
		for neighbor_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
			new_position = (x + neighbor_position[0], z + neighbor_position[1])
			try:
				if height_map[new_position[0]][new_position[1]] != -1 and matrix.getValue(height_map[new_position[0]][new_position[1]]+1,new_position[0],new_position[1]) not in light_pillar_like+[65] and matrix.getValue(height_map[new_position[0]][new_position[1]]-1,new_position[0],new_position[1]) not in air_like:
					return new_position
			except:
				continue
		return (-1, -1)

	def isNeighborLight(matrix,height_map, x, z): #return True if a light is neighbor to the position x, y
		for neighbor_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
			new_position = (x + neighbor_position[0], z + neighbor_position[1])
			try:
				if matrix.getValue(height_map[new_position[0]][new_position[1]] + 1, new_position[0], new_position[1]) in light_pillar_like:
					return True
			except:
				continue

	for i in range(0, len(path) - 1):

		block = path[i]
		x = block[0]
		z = block[1]
		h = height_map[x][z]

		next_block = path[i + 1]
		next_h = height_map[next_block[0]][next_block[1]]

		if i != 0:
			previous_block = path[i - 1]
			previous_h = height_map[previous_block[0]][previous_block[1]]


		logging.info("Generating road at point ({}, {}, {})".format(h, x, z))
		(b, d) = toolbox.getBlockFullValue(matrix, h, x, z)
		if (b, d) != toolbox.getBlockID("stone", 6):
			matrix.setValue(h, x, z, pavement_Block)
			fillUnderneath(matrix, h - 1, x, z)
			fillAbove(matrix, h + 1, x, z, 5)
			# check if we are moving in the x axis (so to add a new pavement
			# on the z-1, z+1 block)
			if x != next_block[0]:

				# if that side block is walkable
				if z - 1 >= 0 and height_map[x][z - 1] != -1 and h-height_map[x][z - 1] in [0, 1]:
					matrix.setValue(h, x, z - 1, pavement_Block)
					height_map[x][z - 1] = h
					# try to fill with earth underneath if it's empty
					#logging.info("Filling underneath at height {}".format(h-1))
					fillUnderneath(matrix, h - 1, x, z - 1)
					# fill upwards with air to remove any obstacles
					fillAbove(matrix, h + 1, x, z - 1, 5)

				# if the opposite side block is walkable
				if z + 1 < matrix.depth and height_map[x][z + 1] != -1 and h-height_map[x][z + 1] in [0, 1]:
					matrix.setValue(h, x, z + 1, pavement_Block)
					height_map[x][z + 1] = h
					#logging.info("Filling underneath at height {}".format(h-1))
					fillUnderneath(matrix, h - 1, x, z + 1)
					fillAbove(matrix, h + 1, x, z + 1, 5)

			elif z != next_block[1]:
				# check if we are moving in the z axis (so add a new pavement
				# on the x-1 block) and if that side block is walkable
				if x-1 >= 0 and height_map[x - 1][z] != -1 and h - height_map[x - 1][z] in [0, 1]:
					matrix.setValue(h, x - 1, z, pavement_Block)
					height_map[x - 1][z] = h
					#logging.info("Filling underneath at height {}".format(h-1))
					fillUnderneath(matrix, h - 1, x - 1, z)
					fillAbove(matrix, h + 1, x - 1, z, 5)


				if x + 1 < matrix.width and height_map[x + 1][z] != -1 and h - height_map[x + 1][z] in [0, 1]:
					matrix.setValue(h, x + 1, z, pavement_Block)
					height_map[x + 1][z] = h
					#logging.info("Filling underneath at height {}".format(h-1))
					fillUnderneath(matrix, h - 1, x + 1, z)
					fillAbove(matrix, h + 1, x + 1, z, 5)

		else:
			logging.info("Stone path at point ({}, {}, {}) already existing, going forward".format(h, x, z))

	# another iteration over the path to generate ladders and lights
	# this is to guarantee that fillAbove or any other
	# manipulations of the environment around the path
	# will erase the ladder blocks or the lights
	block_section = path[0:20] # Block section of 20 blocks to find the right place to put lights
	isPut = generateLight(matrix, block_section, path, height_map)
	if isPut == False: #Failed to find a good position with the center of mass, build it next to or on the path
		try:
			(xl, zl) = findPos(matrix, path[10][0], path[10][1], path, height_map)
		except:
			#not enough block left in the path, so take the position of half of what remains
			(xl, zl) = findPos(matrix, path[int(((i-len(path)-1)/2))][0], path[int(((i-len(path)-1)/2))][1], path, height_map)
		if (xl, zl) != (-1, -1):
			if isNeighborLight(matrix,height_map, xl, zl) != True:
				buildLight(matrix, height_map[xl][zl], xl, zl)
		else:
			if isNeighborLight(matrix,height_map, path[10][0], path[10][1]) != True:
				buildLight(matrix, height_map[path[10][0]][path[10][1]], path[10][0], path[10][1])
	for i in range(0, len(path) - 1):

		block = path[i]
		x = block[0]
		z = block[1]
		h = height_map[x][z]

		next_block = path[i + 1]
		next_h = height_map[next_block[0]][next_block[1]]

		orientation = getOrientation(x, z, next_block[0], next_block[1])
		if abs(h - next_h) > 1:
			if h < next_h:
				if orientation == "N":   ladder_subID = 3
				elif orientation == "S": ladder_subID = 2
				elif orientation == "E": ladder_subID = 4
				elif orientation == "W": ladder_subID = 5
				for ladder_h in range(h + 1, next_h + 1):
					matrix.setValue(ladder_h, x, z, toolbox.getBlockID("ladder", ladder_subID))
					# make sure that the ladders in which the stairs are attached
					# are pathblock and not dirt, etc
					(b, d) = toolbox.getBlockFullValue(matrix, ladder_h, next_block[0], next_block[1])
					if (b, d) != toolbox.getBlockID("ladder", 6):
						matrix.setValue(ladder_h, next_block[0], next_block[1], (pavement_Block))
				block = matrix.getValue(next_h + 1, x, z)
				if type(block) == tuple: block = block[0]
				if block in air_like:
					matrix.setValue(next_h + 1, x, z, air)
				block = matrix.getValue(next_h + 2, x, z)
				if type(block) == tuple: block = block[0]
				if block in air_like:
					matrix.setValue(next_h + 2, x, z, air)

			elif h > next_h:
				if orientation == "N":   ladder_subID = 2
				elif orientation == "S": ladder_subID = 3
				elif orientation == "E": ladder_subID = 5
				elif orientation == "W": ladder_subID = 4
				for ladder_h in range(next_h+1, h+1):
					matrix.setValue(ladder_h, next_block[0], next_block[1], toolbox.getBlockID("ladder", ladder_subID))
					# make sure that the ladders in which the stairs are attached
					# are pathblock and not dirt, etc
					(b, d) = toolbox.getBlockFullValue(matrix, h, x, z)
					if (b, d) != toolbox.getBlockID("ladder", 6):
						matrix.setValue(ladder_h, x, z, (pavement_Block))
				block = matrix.getValue(h + 1, x, z)
				if type(block) == tuple: block = block[0]
				if block in air_like:
					matrix.setValue(h + 1, x, z, air)
				block = matrix.getValue(h + 2, x, z)
				if type(block) == tuple: block = block[0]
				if block in air_like:
					matrix.setValue(h + 2, x, z, air)

		#build next light and update the blocksection
		if type(block) == type(block_section[len(block_section) - 1]) and block == block_section[len(block_section) - 1]:
			isPut = generateLight(matrix, block_section, path, height_map)
			if isPut == False: #Failed to find a good position with the center of mass, build it next to or on the path
				try:
					(xl, zl) = findPos(matrix, path[i + 10][0], path[i + 10][1], path, height_map)
				except:
					#not enogh block left in the path, so take the position of half of what remains
					(xl, zl) = findPos(matrix, path[i + int(((i - len(path) - 1) / 2))][0], path[i + int(((i - len(path) - 1) / 2))][1], path, height_map)
				if (xl, zl) != (-1, -1):
					if isNeighborLight(matrix,height_map, xl, zl) != True:
						buildLight(matrix, height_map[xl][zl], xl, zl)
				else:
					if isNeighborLight(matrix,height_map, path[i + 10][0], path[i + 10][1]) != True:
						buildLight(matrix, height_map[path[i + 10][0]][path[i + 10][1]], path[i + 10][0], path[i + 10][1])
			try:
				block_section = path[i:i + 20]
			except:
				block_section = path[i:len(path)]
