import random
import RNG
import logging
import toolbox as toolbox
import utility as utility

PLANT_SPECIES_NUMBER = 3

def generateFarm(matrix, wood_material, h_min, h_max, x_min, x_max, z_min, z_max, farmType):
	logger = logging.getLogger("farm")

	farm = toolbox.dotdict()
	farm.type = "farm"
	farm.lotArea = toolbox.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})

	toolbox.cleanProperty(matrix, h_min + 1, h_max, x_min, x_max, z_min, z_max)

	(h_min, h_max, x_min, x_max, z_min, z_max) = getFarmAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max, farmType)
	farm.buildArea = toolbox.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})

	logger.info("Generating Farm at area {}".format(farm.lotArea))
	logger.info("Construction area {}".format(farm.buildArea))

	farm.orientation = getOrientation(matrix, farm.lotArea)

	## Generates the farm
	wooden_materials_kit = utility.wood_IDs[wood_material]
	if farmType == None:
		generateBasicPattern(matrix, wooden_materials_kit, h_min, x_min, x_max, z_min, z_max)
	elif farmType == "smiley":
		generateSmileyPattern(matrix, wooden_materials_kit, h_min, x_min, x_max, z_min, z_max)

	#create door and entrance path
	if farm.orientation == "S":
		door_x = x_max - 2
		door_z = z_max - 1
		farm.entranceLot = (door_x, farm.lotArea.z_max)
		generateEntrance(matrix, wooden_materials_kit, 0, h_min, door_x, door_z, door_z + 1, farm.lotArea.z_max + 1)

	elif farm.orientation == "N":
		door_x = x_min + 2
		door_z = z_min + 1
		farm.entranceLot = (door_x, farm.lotArea.z_min)
		generateEntrance(matrix, wooden_materials_kit, 2, h_min, door_x, door_z, farm.lotArea.z_min, door_z)

	elif farm.orientation == "W":
		door_x = x_min + 1
		door_z = z_max - 2
		farm.entranceLot = (farm.lotArea.x_min, door_z)
		generateEntrance(matrix, wooden_materials_kit, 1, h_min, door_x, door_z, farm.lotArea.x_min, door_x)

	elif farm.orientation == "E":
		door_x = x_max - 1
		door_z = z_min + 2
		farm.entranceLot = (farm.lotArea.x_max, door_z)
		generateEntrance(matrix, wooden_materials_kit, 3, h_min, door_x, door_z, door_x + 1, farm.lotArea.x_max + 1)

	return farm

def getFarmAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max, farmType):
	farm_size_x = farm_size_z = 0
	if farmType == None:
		farm_size_x = RNG.randint(11, 16)
		farm_size_z = RNG.randint(11, 16)
	elif farmType == "smiley":
		farm_size_x = farm_size_z = 16

	if x_max-x_min > farm_size_x:
		x_mid = x_min + (x_max - x_min) / 2
		x_min = x_mid - farm_size_x / 2
		x_max = x_mid + farm_size_x / 2

	if z_max-z_min > farm_size_z:
		z_mid = z_min + (z_max - z_min) / 2
		z_min = z_mid - farm_size_z / 2
		z_max = z_mid + farm_size_z / 2

	farm_size_h = (farm_size_x + farm_size_z) / 2
	if h_max - h_min > 19 or h_max - h_min > farm_size_h:
		h_max = h_min + ((farm_size_x + farm_size_z) / 2)

	return (h_min, h_max, x_min, x_max, z_min, z_max)

def generateEntrance(matrix, wooden_materials_kit, orientation, h_min, door_x, door_z, min_bound, max_bound):
	grass_pathID = toolbox.getBlockID("grass_path")
	if orientation % 2 == 0:
		for z in range(min_bound, max_bound):
			matrix.setValue(h_min, door_x, z, grass_pathID)
			matrix.setValue(h_min, door_x - 1, z, grass_pathID)
			matrix.setValue(h_min, door_x + 1, z, grass_pathID)
	else:
		for x in range(min_bound, max_bound):
			matrix.setValue(h_min, x, door_z, grass_pathID)
			matrix.setValue(h_min, x, door_z - 1, grass_pathID)
			matrix.setValue(h_min, x, door_z + 1, grass_pathID)
	matrix.setValue(h_min + 1, door_x, door_z, (wooden_materials_kit["fence_gate"][0], orientation))

def generateBasicPattern(matrix, wooden_materials_kit, h, x_min, x_max, z_min, z_max, plant = None):

	## FENCES
	generateFences(matrix, wooden_materials_kit, h, x_min + 1, x_max - 1, z_min + 1, z_max - 1)

	## GROUND & CULTURES
	if plant == None:
		# select one random plant for this farm
		plants = [toolbox.getBlockID("wheat"), toolbox.getBlockID("carrots"), toolbox.getBlockID("potatoes")]
		plant = plants[RNG.randint(0, PLANT_SPECIES_NUMBER - 1)]
	# fill field with dirt and the corresponding plant
	farmlandID = toolbox.getBlockID("farmland")
	for x in range(x_min + 3, x_max - 2):
		for z in range(z_min + 3, z_max - 2):
			matrix.setValue(h, x, z, farmlandID)
			matrix.setValue(h + 1, x, z, plant)

	## WATER
	waterID = toolbox.getBlockID("water")
	for x in range(x_min + 2, x_max - 1):
		matrix.setValue(h, x, z_max - 2, waterID)
		matrix.setValue(h, x, z_min + 2, waterID)
	for z in range(z_min + 2, z_max - 1):
		matrix.setValue(h, x_max - 2, z, waterID)
		matrix.setValue(h, x_min + 2, z, waterID)

def generateSmileyPattern(matrix, wooden_materials_kit, h, x_min, x_max, z_min, z_max):

	## FENCES
	generateFences(matrix, wooden_materials_kit, h, x_min + 1, x_max - 1, z_min + 1, z_max - 1)

	## GROUND
	farmlandID = toolbox.getBlockID("farmland")
	carrotsID = toolbox.getBlockID("carrots")
	# fill field with dirt and carrots
	for x in range(x_min + 3, x_max - 2):
		for z in range(z_min + 3, z_max - 2):
			matrix.setValue(h, x, z, farmlandID)
			matrix.setValue(h + 1, x, z, CARROT_ID)

	## SMILEY
	wheatID = toolbox.getBlockID("wheat")
	waterID = toolbox.getBlockID("water")
	# eyes
	def generateEye(x, z):
		matrix.setValue(h + 1, x, z, wheatID)
		matrix.setValue(h + 1, x, z + 1, wheatID)
		matrix.setValue(h + 1, x + 1, z, wheatID)
		matrix.setValue(h, x + 1, z + 1, waterID)
		matrix.setValue(h + 1, x + 1, z + 1, toolbox.getBlockID("air"))
	# left eye
	generateEye(x_min + 5, z_min + 5)
	# right eye
	generateEye(x_max - 6, z_min + 5)
	# mouth
	for x in range(x_min + 6, x_max - 5):
		matrix.setValue(h + 1, x, z_max - 4, wheatID)
	matrix.setValue(h + 1, x_min + 5, z_max - 5, wheatID)
	matrix.setValue(h + 1, x_max - 5, z_max - 5, wheatID)
	matrix.setValue(h + 1, x_min + 4, z_max - 6, wheatID)
	matrix.setValue(h + 1, x_max - 4, z_max - 6, wheatID)

	## WATER
	for x in range(x_min + 2, x_max - 1):
		matrix.setValue(h, x, z_max - 2, waterID)
		matrix.setValue(h, x, z_min + 2, waterID)
	for z in range(z_min + 2, z_max - 1):
		matrix.setValue(h, x_max - 2, z, waterID)
		matrix.setValue(h, x_min + 2, z, waterID)


def generateFences(matrix, wooden_materials_kit, h, x_min, x_max, z_min, z_max):
	oak_logID = wooden_materials_kit["log"]
	oak_fenceID = wooden_materials_kit["fence"]
	torchID = toolbox.getBlockID("torch", 5)
	for x in range(x_min, x_max + 1):
		matrix.setValue(h, x, z_max, oak_logID)
		matrix.setValue(h, x, z_min, oak_logID)
		matrix.setValue(h + 1, x, z_max, oak_fenceID)
		matrix.setValue(h + 1, x, z_min, oak_fenceID)
	for z in range(z_min, z_max + 1):
		matrix.setValue(h, x_max, z, oak_logID)
		matrix.setValue(h, x_min, z, oak_logID)
		matrix.setValue(h + 1, x_max, z, oak_fenceID)
		matrix.setValue(h + 1, x_min, z, oak_fenceID)
	matrix.setValue(h + 2, x_min, z_max, torchID)
	matrix.setValue(h + 2, x_min, z_min, torchID)
	matrix.setValue(h + 2, x_max, z_max, torchID)
	matrix.setValue(h + 2, x_max, z_min, torchID)

def getOrientation(matrix, area):
	x_mid = matrix.width/2
	z_mid = matrix.depth/2

	bx_mid = area.x_min + (area.x_max-area.x_min)/2
	bz_mid = area.z_min + (area.z_max-area.z_min)/2

	if bx_mid <= x_mid:
		if bz_mid <= z_mid:
			# return SOUTH, EAST
			return RNG.choice(["S", "E"])
		elif bz_mid > z_mid:
			# return NORTH, EAST
			return RNG.choice(["N", "E"])

	elif bx_mid > x_mid:
		if bz_mid <= z_mid:
			# return SOUTH, WEST
			return RNG.choice(["S", "W"])
		elif bz_mid > z_mid:
			# return NORTH, WEST
			return RNG.choice(["N", "W"])
	return None
