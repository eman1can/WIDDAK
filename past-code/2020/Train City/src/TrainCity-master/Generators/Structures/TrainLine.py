import logging
import toolbox as toolbox
import utility as utility

## TO-DO LIST :
## - rail alone under CHECK
## - corner too low CHECK ?
## - path erases ladder CHECK
## - path erases corner pillars CHECK
## - generatePath generates infinte ladder under station CHECK
## - station on water CHECK
## - powered rails CHECK
## - multiple station generation CHECK
## - ideal station generation location CHECK
## - lightning CHECK
## - chest with minecart
## - sign with station name

STATION_FLATNESS = 5
HEIGHT_FROM_GROUND = 10
SMOOTHING_RANGE = 5
SPACE_BETWEEN_PILLARS = 8

class RailNode:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		self.next = None
		self.prev = None

class RailNetwork:
	def __init__(self):
		self.starting_rail = None
		self.size = 0
		self.logger = logging.getLogger("trainLine")

	def browseList(self):
		r = self.starting_rail
		if r == None:
			self.logger.error("Rail network empty")
			return
		for i in range(self.size * 2):
			self.logger.debug("{}, {}, {}".format(r.x, r.y, r.z))
			r = r.next

	def browseListBackwards(self):
		r = self.starting_rail
		if r == None:
			self.logger.error("Rail network empty")
			return
		for i in range(self.size * 2):
			self.logger.debug("{}, {}, {}".format(r.x, r.y, r.z))
			r = r.prev

	def insertNodeAtEnd(self, new_rail):
		if self.starting_rail == None:
			self.starting_rail = new_rail
			self.starting_rail.prev = new_rail
			self.starting_rail.next = new_rail
		else:
			new_rail.prev = self.starting_rail.prev
			new_rail.next = self.starting_rail
			self.starting_rail.prev.next = new_rail
			self.starting_rail.prev = new_rail
		self.size += 1

	def insertNewNodeAtEnd(self, x, y, z):
		new_rail = RailNode(x, y, z)
		self.insertNodeAtEnd(new_rail)

	def isNetworkContinuous(self):
		def isOneOrLessDifferencial(x, y):
			return ((x - y == 0) or (x - y == 1) or (x - y == -1))

		r = self.starting_rail
		if r == None:
			return False
		for i in range(self.size):
			if r.next == None or not isOneOrLessDifferencial(r.y, r.next.y):
				return False
			r = r.next
		return True

	def smoothNetwork(self, smoothing_range):
		def railNeighboursHeightMean(base_rail):
			if base_rail == None:
				return -1
			height_sum = base_rail.y
			nb_neighbours = 1
			r = base_rail
			for i in range(smoothing_range):
				r = r.prev
				height_sum += r.y
				nb_neighbours += 1
			r = base_rail
			for i in range(smoothing_range):
				r = r.next
				height_sum += r.y
				nb_neighbours += 1
			return int(round(1.0 * height_sum / nb_neighbours))

		r = self.starting_rail
		tmp_heights = []
		for i in range(self.size):
			tmp_heights.append(railNeighboursHeightMean(r))
			r = r.next

		r = self.starting_rail
		for i in range(self.size):
			r.y = tmp_heights[i]
			r = r.next


def generateTrainLine(matrix, wood_material, nb_stations, height_map, simple_height_map, h_min, h_max, x_min, x_max, z_min, z_max):
	logger = logging.getLogger("trainLine")
	logger.info("Preparation for Train Line generation")
	stations = []

	## Create train line height map
	logger.info("Creating Train Line rail network")
	rail_network = createRailNetwork(simple_height_map, x_min, x_max, z_min, z_max)
	logger.info("Creating Train Line smoothed height map")
	train_line_height_map = createTrainLineHeightMap(rail_network, simple_height_map, h_max, x_min, x_max, z_min, z_max)

	if train_line_height_map == -1:
		logger.error("Train Line height map smoothing failed")
		return
	wooden_materials_kit = utility.wood_IDs[wood_material] # wood_material instead of "urban" for an adaptative wooden rail network
	logger.info("Generating Train Line rails")
	(pillar_coordinates, stations_coordinates) = generateRails(logger, matrix, wooden_materials_kit, nb_stations, height_map, simple_height_map, train_line_height_map, x_min, x_max, z_min, z_max)
	logger.info("Clearing Train Line")
	clearAboveRailNetwork(matrix, train_line_height_map, h_max, x_min, x_max, z_min, z_max)

	for i in range(0, len(stations_coordinates)):
		s = toolbox.dotdict()
		s.type = "trainLine"
		s.lotArea = toolbox.dotdict({"y_min": h_min, "y_max": h_max, "x_min": stations_coordinates[i][0] - 2, "x_max": stations_coordinates[i][0] + 2, "z_min": stations_coordinates[i][1] - 2, "z_max": stations_coordinates[i][1] + 2})
		s.buildArea = toolbox.dotdict({"y_min": h_min, "y_max": h_max, "x_min": stations_coordinates[i][0], "x_max": stations_coordinates[i][0], "z_min": stations_coordinates[i][1], "z_max": stations_coordinates[i][1]})
		s.orientation = "S"
		s.entranceLot = (s.lotArea.x_min + 1, s.lotArea.z_min)
		stations.append(s)
		logger.info("Generating station {}".format(i + 1))
		generateStation(matrix, wooden_materials_kit, simple_height_map, train_line_height_map, stations_coordinates[i][0], stations_coordinates[i][1], stations_coordinates[i][2])

	logger.info("Train Line generaton successful")
	return (pillar_coordinates, stations)

def generateStation(matrix, wooden_materials_kit, simple_height_map, train_line_height_map, x, z, direction):
	floor_material = wooden_materials_kit["planks"]
	fence_material = wooden_materials_kit["fence"]
	roof_material = wooden_materials_kit["slab"]
	air = toolbox.getBlockID("air", 0)

	initial_position = train_line_height_map[x][z] + HEIGHT_FROM_GROUND

	if direction == 1:
		# base
		matrix.setValue(initial_position + 1, x, z, toolbox.getBlockID("golden_rail", toolbox.Orientation.HORIZONTAL - 1))
		for y in range(simple_height_map[x][z - 1] + 1, initial_position + 1):
			matrix.setValue(y, x, z - 1, toolbox.getBlockID("ladder", 2))
		for y in range(simple_height_map[x][z + 1] + 1, initial_position + 1):
			matrix.setValue(y, x, z + 1, toolbox.getBlockID("ladder", 3))
		for i in range(-1, 2):
			matrix.setValue(initial_position + 1, x + i, z - 1, air)
			matrix.setValue(initial_position + 1, x + i, z + 1, air)
		for i in range(-2, 3):
			matrix.setValue(initial_position, x + i, z - 2, floor_material)
			matrix.setValue(initial_position + 1, x + i, z - 2, fence_material)
			matrix.setValue(initial_position, x + i, z + 2, floor_material)
			matrix.setValue(initial_position + 1, x + i, z + 2, fence_material)

	elif direction == 0:
		# base
		matrix.setValue(initial_position + 1, x, z, toolbox.getBlockID("golden_rail", toolbox.Orientation.VERTICAL - 1))
		for y in range(simple_height_map[x][z - 1] + 1, initial_position + 1):
			matrix.setValue(y, x - 1, z, toolbox.getBlockID("ladder", 4))
		for y in range(simple_height_map[x][z + 1] + 1, initial_position + 1):
			matrix.setValue(y, x + 1, z, toolbox.getBlockID("ladder", 5))
		for i in range(-1, 2):
			matrix.setValue(initial_position + 1, x - 1, z + i, air)
			matrix.setValue(initial_position + 1, x + 1, z + i, air)
		for i in range(-2, 3):
			matrix.setValue(initial_position, x - 2, z + i, floor_material)
			matrix.setValue(initial_position + 1, x - 2, z + i, fence_material)
			matrix.setValue(initial_position, x + 2, z + i, floor_material)
			matrix.setValue(initial_position + 1, x + 2, z + i, fence_material)

	# roof
	for i in range(0, 3):
		matrix.setValue(initial_position + 1 + i, x - 2, z - 2, fence_material)
		matrix.setValue(initial_position + 1 + i, x + 2, z - 2, fence_material)
		matrix.setValue(initial_position + 1 + i, x - 2, z + 2, fence_material)
		matrix.setValue(initial_position + 1 + i, x + 2, z + 2, fence_material)
	for i in range(-2, 3):
		for j in range(-2, 3):
			matrix.setValue(initial_position + 4, x + i, z + j, roof_material)
	for i in range(-1, 2):
		for j in range(-1, 2):
			matrix.setValue(initial_position + 4, x + i, z + j, floor_material)


def clearAboveBlock(matrix, h_min, h_max, x, z):
	for y in range(h_min + HEIGHT_FROM_GROUND + 2, h_max):
		matrix.setValue(y, x, z, toolbox.getBlockID("air", 0))

def clearAboveRail(matrix, h_min, h_max, x, z, direction):
	if direction == 1:
		clearAboveBlock(matrix, h_min + 1, h_max, x, z - 1)
		clearAboveBlock(matrix, h_min, h_max, x, z)
		clearAboveBlock(matrix, h_min + 1, h_max, x, z + 1)
	elif direction == 0:
		clearAboveBlock(matrix, h_min + 1, h_max, x - 1, z)
		clearAboveBlock(matrix, h_min, h_max, x, z)
		clearAboveBlock(matrix, h_min + 1, h_max, x + 1, z)

def clearAboveRailNetwork(matrix, train_line_height_map, h_max, x_min, x_max, z_min, z_max):
	for x in range(x_min + 1, x_max):
		clearAboveRail(matrix, train_line_height_map[x][z_min], h_max, x, z_min, 1)
		clearAboveRail(matrix, train_line_height_map[x][z_max], h_max, x, z_max, 1)
	for z in range(z_min + 1, z_max):
		clearAboveRail(matrix, train_line_height_map[x_min][z], h_max, x_min, z, 0)
		clearAboveRail(matrix, train_line_height_map[x_max][z], h_max, x_max, z, 0)

def isFlat(train_line_height_map, x, z, direction):
	y = train_line_height_map[x][z]
	if direction == 1:
		return y == train_line_height_map[x + 1][z]
	return y == train_line_height_map[x][z + 1]

def isAloneUnder(train_line_height_map, x, z, direction):
	y = train_line_height_map[x][z]
	if direction == 1:
		return y == train_line_height_map[x - 1][z] - 1 and y == train_line_height_map[x + 1][z] - 1
	return y == train_line_height_map[x][z - 1] - 1 and y == train_line_height_map[x][z + 1] - 1

def createRailNetwork(simple_height_map, x_min, x_max, z_min, z_max):
	## Init rail network
	rail_network = RailNetwork()
	# x_min, z_min -> x_max, z_min
	for x in range(x_min, x_max):
		rail_network.insertNewNodeAtEnd(x, simple_height_map[x][z_min], z_min)
	# x_max, z_min -> x_max, z_max
	for z in range(z_min, z_max):
		rail_network.insertNewNodeAtEnd(x_max, simple_height_map[x_max][z], z)
	# x_max, z_max -> x_min, z_max
	for x in range(x_max, x_min, -1):
		rail_network.insertNewNodeAtEnd(x, simple_height_map[x][z_max], z_max)
	# x_min, z_max -> x_min, z_min
	for z in range(z_max, z_min, -1):
		rail_network.insertNewNodeAtEnd(x_min, simple_height_map[x_min][z], z)

	## Smooth rail network
	iteration = 0
	while not rail_network.isNetworkContinuous():
		iteration += 1
		rail_network.smoothNetwork(SMOOTHING_RANGE)

	return rail_network

def createTrainLineHeightMap(rail_network, simple_height_map, h_max, x_min, x_max, z_min, z_max):
	train_line_height_map = [row[:] for row in simple_height_map] # copy the simple height map

	r = rail_network.starting_rail
	# x_min, z_min -> x_max, z_min
	for x in range(x_min, x_max):
		train_line_height_map[x][z_min] = r.y
		r = r.next
	# x_max, z_min -> x_max, z_max
	for z in range(z_min, z_max):
		train_line_height_map[x_max][z] = r.y
		r = r.next
	# x_max, z_max -> x_min, z_max
	for x in range(x_max, x_min, -1):
		train_line_height_map[x][z_max] = r.y
		r = r.next
	# x_min, z_max -> x_min, z_min
	for z in range(z_max, z_min, -1):
		train_line_height_map[x_min][z] = r.y
		r = r.next

	## Check for disturbances for rail continuity
	for x in range(x_min + 1, x_max):
		if isAloneUnder(train_line_height_map, x, z_min, 1):
			train_line_height_map[x][z_min] += 1
		if isAloneUnder(train_line_height_map, x, z_max, 1):
			train_line_height_map[x][z_max] += 1
	for z in range(z_min + 1, z_max):
		if isAloneUnder(train_line_height_map, x_min, z, 0):
			train_line_height_map[x_min][z] += 1
		if isAloneUnder(train_line_height_map, x_max, z, 0):
			train_line_height_map[x_max][z] += 1
	return train_line_height_map

def generatePillar(matrix, pillar_material, simple_height_map, train_line_height_map, x, z, direction):
	h = train_line_height_map[x][z] + HEIGHT_FROM_GROUND
	matrix.setValue(h - 4, x + 1, z, toolbox.getBlockID("torch", 1))
	matrix.setValue(h - 4, x - 1, z, toolbox.getBlockID("torch", 2))
	matrix.setValue(h - 4, x, z + 1, toolbox.getBlockID("torch", 3))
	matrix.setValue(h - 4, x, z - 1, toolbox.getBlockID("torch", 4))
	for y in range(simple_height_map[x][z] + 1, h - 2):
		matrix.setValue(y, x, z, pillar_material)
	if direction == 1:
		matrix.setValue(h + 2, x, z - 1, toolbox.getBlockID("torch", 5))
		matrix.setValue(h + 2, x, z + 1, toolbox.getBlockID("torch", 5))
	elif direction == 0:
		matrix.setValue(h + 2, x - 1, z, toolbox.getBlockID("torch", 5))
		matrix.setValue(h + 2, x + 1, z, toolbox.getBlockID("torch", 5))

def isGoldenRail(rail_orientation):
	return (rail_orientation == toolbox.Orientation.NORTH - 1 or
			rail_orientation == toolbox.Orientation.SOUTH - 1 or
			rail_orientation == toolbox.Orientation.WEST - 1 or
			rail_orientation == toolbox.Orientation.EAST - 1)

def generateRail(matrix, y, x, z, path_material, fence_material, rail_orientation, generateAround = True):
	# Generate the path
	matrix.setValue(y - 2, x, z, path_material)
	matrix.setValue(y - 1, x, z, path_material)
	matrix.setValue(y, x, z, path_material)
	if generateAround:
		(x_modifier, z_modifier) = (1, 0) # default
		if ((rail_orientation == toolbox.Orientation.VERTICAL - 1) or
			(rail_orientation == toolbox.Orientation.WEST - 1) or
			(rail_orientation == toolbox.Orientation.EAST - 1)):
			(x_modifier, z_modifier) = (1, 0)
		elif ((rail_orientation == toolbox.Orientation.HORIZONTAL - 1) or
			(rail_orientation == toolbox.Orientation.NORTH - 1) or
			(rail_orientation == toolbox.Orientation.SOUTH - 1)):
			(x_modifier, z_modifier) = (0, 1)
		matrix.setValue(y - 1, x - x_modifier, z - z_modifier, path_material)
		matrix.setValue(y, x - x_modifier, z - z_modifier, path_material)
		matrix.setValue(y + 1, x - x_modifier, z - z_modifier, fence_material)
		matrix.setValue(y - 1, x + x_modifier, z + z_modifier, path_material)
		matrix.setValue(y, x + x_modifier, z + z_modifier, path_material)
		matrix.setValue(y + 1, x + x_modifier, z + z_modifier, fence_material)
	# Generate the rail
	if isGoldenRail(rail_orientation):
		matrix.setValue(y + 1, x, z, toolbox.getBlockID("golden_rail", rail_orientation))
		if generateAround:
			matrix.setValue(y, x, z, toolbox.getBlockID("redstone_block"))
	else:
		matrix.setValue(y + 1, x, z, toolbox.getBlockID("rail", rail_orientation))

def generateRailWithDifferential(matrix, wooden_materials_kit, train_line_height_map, x, z, rail_orientation):
	path_material = wooden_materials_kit["planks"]
	fence_material = wooden_materials_kit["fence"]
	if (rail_orientation == toolbox.Orientation.HORIZONTAL - 1):
		if train_line_height_map[x][z] == train_line_height_map[x + 1][z] - 1: rail_orientation = toolbox.Orientation.NORTH - 1
		elif train_line_height_map[x][z] == train_line_height_map[x - 1][z] - 1: rail_orientation = toolbox.Orientation.SOUTH - 1
	elif (rail_orientation == toolbox.Orientation.VERTICAL - 1):
		if train_line_height_map[x][z] == train_line_height_map[x][z + 1] - 1: rail_orientation = toolbox.Orientation.EAST - 1
		elif train_line_height_map[x][z] == train_line_height_map[x][z - 1] - 1: rail_orientation = toolbox.Orientation.WEST - 1
	generateRail(matrix, train_line_height_map[x][z] + HEIGHT_FROM_GROUND, x, z, path_material, fence_material, rail_orientation)

## Happen when the corner rail smoothed not enough
def generateSpecialCorner(logger, matrix, simple_height_map, train_line_height_map, y, x, z, x_modifier, z_modifier, path_material, fence_material, pillar_material, rail_orientation):
	logger.info("Generating special train line rail corner")
	rail_orientations = (toolbox.Orientation.NORTH_WEST - 1, toolbox.Orientation.SOUTH_EAST - 1, toolbox.Orientation.HORIZONTAL - 1, toolbox.Orientation.EAST - 1, toolbox.Orientation.SOUTH - 1, toolbox.Orientation.VERTICAL - 1) #default
	if rail_orientation == toolbox.Orientation.NORTH_EAST - 1:
		rail_orientations = (toolbox.Orientation.NORTH_WEST - 1, toolbox.Orientation.SOUTH_EAST - 1, toolbox.Orientation.HORIZONTAL - 1, toolbox.Orientation.EAST - 1, toolbox.Orientation.SOUTH - 1, toolbox.Orientation.VERTICAL - 1)
	elif rail_orientation == toolbox.Orientation.NORTH_WEST - 1:
		rail_orientations = (toolbox.Orientation.SOUTH_WEST - 1, toolbox.Orientation.NORTH_EAST - 1, toolbox.Orientation.VERTICAL - 1, toolbox.Orientation.NORTH - 1, toolbox.Orientation.EAST - 1, toolbox.Orientation.HORIZONTAL - 1)
	elif rail_orientation == toolbox.Orientation.SOUTH_WEST - 1:
		rail_orientations = (toolbox.Orientation.NORTH_WEST - 1, toolbox.Orientation.SOUTH_EAST - 1, toolbox.Orientation.HORIZONTAL - 1, toolbox.Orientation.EAST - 1, toolbox.Orientation.SOUTH - 1, toolbox.Orientation.VERTICAL - 1)
	elif rail_orientation == toolbox.Orientation.SOUTH_EAST - 1:
		rail_orientations = (toolbox.Orientation.SOUTH_WEST - 1, toolbox.Orientation.NORTH_EAST - 1, toolbox.Orientation.VERTICAL - 1, toolbox.Orientation.NORTH - 1, toolbox.Orientation.EAST - 1, toolbox.Orientation.HORIZONTAL - 1)

	generateRail(matrix, y + 1, x, z, path_material, fence_material, rail_orientations[1], False)
	generateRail(matrix, y + 1, x, z + z_modifier, path_material, fence_material, rail_orientations[2], False)
	generateRail(matrix, y + 1, x, z + 2 * z_modifier, path_material, fence_material, rail_orientations[0], False)
	generateRail(matrix, y, x + x_modifier, z + 2 * z_modifier, path_material, fence_material, rail_orientations[3], False)
	generateRail(matrix, y, x + 2 * x_modifier, z + 2 * z_modifier, path_material, fence_material, rail_orientation, False)
	generateRail(matrix, y - 1, x + 2 * x_modifier, z + z_modifier, path_material, fence_material, rail_orientations[4], False)
	generateRail(matrix, y - 1, x + 2 * x_modifier, z, path_material, fence_material, rail_orientations[1], False)
	generateRail(matrix, y - 1, x + x_modifier, z, path_material, fence_material, rail_orientations[5], False)
	generateRail(matrix, y - 1, x, z, path_material, fence_material, rail_orientations[0], False)
	matrix.setValue(y, x + x_modifier, z + z_modifier, toolbox.getBlockID("redstone_block"))
	matrix.setValue(y + 1, x + x_modifier, z + z_modifier, path_material)
	train_line_height_map[x][z] -= 1

def generateCorner(logger, matrix, simple_height_map, train_line_height_map, x, z, x_modifier, z_modifier, path_material, fence_material, pillar_material, rail_orientation):
	y = train_line_height_map[x][z] + HEIGHT_FROM_GROUND
	if (train_line_height_map[x][z] == train_line_height_map[x - x_modifier][z] - 1):
		if (train_line_height_map[x][z] != train_line_height_map[x][z - z_modifier] + 1):
			train_line_height_map[x][z] += 1
			y += 1
		else:
			generateSpecialCorner(logger, matrix, simple_height_map, train_line_height_map, y, x, z, x_modifier, z_modifier, path_material, fence_material, pillar_material, rail_orientation)
			return
	elif (train_line_height_map[x][z] == train_line_height_map[x][z - z_modifier] - 1):
		if (train_line_height_map[x][z] != train_line_height_map[x - x_modifier][z] + 1):
			train_line_height_map[x][z] += 1
			y += 1
		else:
			generateSpecialCorner(logger, matrix, simple_height_map, train_line_height_map, y, x, z, x_modifier, z_modifier, path_material, fence_material, pillar_material, rail_orientation)
			return
	generateRail(matrix, y, x, z, path_material, fence_material, rail_orientation, False)
	matrix.setValue(y, x + x_modifier, z, path_material)
	matrix.setValue(y + 1, x + x_modifier, z, fence_material)
	matrix.setValue(y, x, z + z_modifier, path_material)
	matrix.setValue(y + 1, x, z + z_modifier, fence_material)
	matrix.setValue(y, x + x_modifier, z + z_modifier, path_material)
	matrix.setValue(y + 1, x + x_modifier, z + z_modifier, fence_material)
	matrix.setValue(y + 2, x + x_modifier, z + z_modifier, toolbox.getBlockID("torch", 5))
	#generatePillar(matrix, pillar_material, simple_height_map, train_line_height_map, x, z, -1)

def generateCorners(logger, matrix, wooden_materials_kit, simple_height_map, train_line_height_map, x_min, x_max, z_min, z_max):
	## Generates the edges turning rails
	path_material = wooden_materials_kit["planks"]
	fence_material = wooden_materials_kit["fence"]
	pillar_material = wooden_materials_kit["log"]

	# x_min, z_min
	generateCorner(logger, matrix, simple_height_map, train_line_height_map, x_min, z_min, -1, -1, path_material, fence_material, pillar_material, toolbox.Orientation.NORTH_EAST - 1)
	# x_min, z_max
	generateCorner(logger, matrix, simple_height_map, train_line_height_map, x_min, z_max, -1, 1, path_material, fence_material, pillar_material, toolbox.Orientation.NORTH_WEST - 1)
	# x_max, z_min
	generateCorner(logger, matrix, simple_height_map, train_line_height_map, x_max, z_min, 1, -1, path_material, fence_material, pillar_material, toolbox.Orientation.SOUTH_EAST - 1)
	# x_max, z_max
	generateCorner(logger, matrix, simple_height_map, train_line_height_map, x_max, z_max, 1, 1, path_material, fence_material, pillar_material, toolbox.Orientation.SOUTH_WEST - 1)

def generateRails(logger, matrix, wooden_materials_kit, nb_stations, height_map, simple_height_map, train_line_height_map, x_min, x_max, z_min, z_max):
	pillar_coordinates = []
	nb_pillars = 0
	pillar_material = wooden_materials_kit["log"]
	stations_coordinates = []
	flatness_score1 = flatness_score2 = flatness_score3 = flatness_score4 = 0
	nb_stations1 = nb_stations2 = nb_stations3 = nb_stations4 = 0
	if nb_stations == 2:
		nb_stations1 = 1
		nb_stations2 = 1
	elif nb_stations == 4:
		nb_stations1 = 1
		nb_stations2 = 1
		nb_stations3 = 1
		nb_stations4 = 1

	generateCorners(logger, matrix, wooden_materials_kit, simple_height_map, train_line_height_map, x_min, x_max, z_min, z_max)

	rail_orientation = toolbox.Orientation.HORIZONTAL - 1
	for x in range(x_min + 1, x_max):
		station_orientation = 1
		flatness_score1 = flatness_score1 + 1 if isFlat(train_line_height_map, x, z_min, 1) else 0
		flatness_score2 = flatness_score2 + 1 if isFlat(train_line_height_map, x, z_max, 1) else 0
		if (x % SPACE_BETWEEN_PILLARS == 0):
			generatePillar(matrix, pillar_material, simple_height_map, train_line_height_map, x, z_min, 1)
			pillar_coordinates.append((x, z_min))
			generatePillar(matrix, pillar_material, simple_height_map, train_line_height_map, x, z_max, 1)
			pillar_coordinates.append((x, z_max))
			nb_pillars += 2
			if nb_stations > 0:
				if nb_stations1 > 0 and flatness_score1 >= STATION_FLATNESS and height_map[x][z_min] != -1:
					station_x = x
					station_z = z_min
					stations_coordinates.append((station_x, station_z, station_orientation))
					flatness_score1 = 0
					nb_stations1 -= 1
					nb_stations -= 1
				elif nb_stations2 > 0 and flatness_score2 >= STATION_FLATNESS and height_map[x][z_max] != -1:
					station_x = x
					station_z = z_max
					stations_coordinates.append((station_x, station_z, station_orientation))
					flatness_score2 = 0
					nb_stations2 -= 1
					nb_stations -= 1
		generateRailWithDifferential(matrix, wooden_materials_kit, train_line_height_map, x, z_min, rail_orientation)
		generateRailWithDifferential(matrix, wooden_materials_kit, train_line_height_map, x, z_max, rail_orientation)

	if nb_stations1 > 0 or nb_stations2 > 0:
		nb_stations3 += 1
		nb_stations4 += 1
	rail_orientation = toolbox.Orientation.VERTICAL - 1
	for z in range(z_min + 1, z_max):
		station_orientation = 0
		flatness_score3 = flatness_score3 + 1 if isFlat(train_line_height_map, x_min, z, 0) else 0
		flatness_score4 = flatness_score4 + 1 if isFlat(train_line_height_map, x_max, z, 0) else 0
		if (z % SPACE_BETWEEN_PILLARS == 0):
			generatePillar(matrix, pillar_material, simple_height_map, train_line_height_map, x_min, z, 0)
			pillar_coordinates.append((x_min, z))
			generatePillar(matrix, pillar_material, simple_height_map, train_line_height_map, x_max, z, 0)
			pillar_coordinates.append((x_max, z))
			nb_pillars += 2
			if nb_stations > 0:
				if nb_stations3 > 0 and flatness_score3 >= STATION_FLATNESS and height_map[x_min][z] != -1:
					station_x = x_min
					station_z = z
					stations_coordinates.append((station_x, station_z, station_orientation))
					flatness_score3 = 0
					nb_stations3 -= 1
					nb_stations -= 1
				elif nb_stations4 > 0 and flatness_score4 >= STATION_FLATNESS and height_map[x_max][z] != -1:
					station_x = x_max
					station_z = z
					stations_coordinates.append((station_x, station_z, station_orientation))
					flatness_score4 = 0
					nb_stations4 -= 1
					nb_stations -= 1
		generateRailWithDifferential(matrix, wooden_materials_kit, train_line_height_map, x_min, z, rail_orientation)
		generateRailWithDifferential(matrix, wooden_materials_kit, train_line_height_map, x_max, z, rail_orientation)


	return (pillar_coordinates, stations_coordinates)
