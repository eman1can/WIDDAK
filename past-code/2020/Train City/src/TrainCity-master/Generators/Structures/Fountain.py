import logging
import toolbox as toolbox
import utility as utility

FOUNTAIN_HEIGHT = 15

def generateFountain(matrix, h_min, h_max, x_min, x_max, z_min, z_max):
	logger = logging.getLogger("fountain")
	logger.info("Preparation for Fountain generation")

	fountain_material = toolbox.getBlockID("double_stone_slab")

	x_center = (x_min + x_max) / 2
	z_center = (z_min + z_max) / 2
	if (h_min + FOUNTAIN_HEIGHT < h_max): h_max = h_min + FOUNTAIN_HEIGHT
	generateStructure(matrix, logger, fountain_material, h_min, h_max, x_center, z_center)

	f = toolbox.dotdict()
	f.type = "fountain"
	f.lotArea = toolbox.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})
	f.buildArea = toolbox.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_center - 6, "x_max": x_center + 7, "z_min": z_center - 6, "z_max": z_center + 7})
	f.orientation = "S"
	f.entranceLot = (f.lotArea.x_min, f.lotArea.z_min)
	return f

def generateStructure(matrix, logger, material, h_min, h_max, x_center, z_center):
	water = toolbox.getBlockID("water")
	border = toolbox.getBlockID("lapis_block")

	h_first_floor = h_min + (h_max - h_min) / 3
	h_second_floor = h_min + (h_max - h_min) / 3 * 2

	# water
	matrix.setValue(h_max, x_center, z_center, water)
	for h in range(h_second_floor, h_max + 1):
		matrix.setValue(h, x_center - 1, z_center, water)
		matrix.setValue(h, x_center + 1, z_center, water)
		matrix.setValue(h, x_center, z_center - 1, water)
		matrix.setValue(h, x_center, z_center + 1, water)
	for h in range(h_first_floor, h_second_floor + 1):
		matrix.setValue(h, x_center - 2, z_center, water)
		matrix.setValue(h, x_center + 2, z_center, water)
		matrix.setValue(h, x_center, z_center - 2, water)
		matrix.setValue(h, x_center, z_center + 2, water)
	for h in range(h_min + 1, h_first_floor + 1):
		matrix.setValue(h, x_center - 3, z_center - 2, water)
		matrix.setValue(h, x_center - 3, z_center + 2, water)
		matrix.setValue(h, x_center + 3, z_center - 2, water)
		matrix.setValue(h, x_center + 3, z_center + 2, water)
		matrix.setValue(h, x_center - 2, z_center - 3, water)
		matrix.setValue(h, x_center + 2, z_center - 3, water)
		matrix.setValue(h, x_center - 2, z_center + 3, water)
		matrix.setValue(h, x_center + 2, z_center + 3, water)
	for i in range(-2, 3):
		for j in range(-2, 3):
			matrix.setValue(h_first_floor, x_center + i, z_center + j, water)

	for i in range(-5, 6):
		for j in range(-5, 6):
			matrix.setValue(h_min + 1, x_center + i, z_center + j, water)

	# central base
	logger.info("Fountain central base height : {}".format(h_max))
	for h in range(h_min, h_max):
		matrix.setValue(h, x_center, z_center, material)

	# basin
	for x in range(x_center - 6, x_center + 7):
		matrix.setValue(h_min + 1, x, z_center - 6, border)
		matrix.setValue(h_min + 1, x, z_center + 6, border)
	for z in range(z_center - 6, z_center + 7):
		matrix.setValue(h_min + 1, x_center - 6, z, border)
		matrix.setValue(h_min + 1, x_center + 6, z, border)
	for x in range(x_center - 4, x_center + 5):
		matrix.setValue(h_min, x, z_center - 4, border)
		matrix.setValue(h_min, x, z_center + 4, border)
	for z in range(z_center - 4, z_center + 5):
		matrix.setValue(h_min, x_center - 4, z, border)
		matrix.setValue(h_min, x_center + 4, z, border)
	for x in range(x_center - 8, x_center + 9):
		matrix.setValue(h_min, x, z_center - 8, border)
		matrix.setValue(h_min, x, z_center + 8, border)
	for z in range(z_center - 8, z_center + 9):
		matrix.setValue(h_min, x_center - 8, z, border)
		matrix.setValue(h_min, x_center + 8, z, border)

	# first floor
	logger.info("Fountain first floor height : {}".format(h_first_floor))
	for h in range(h_min, h_first_floor):
		for i in range(-2, 3):
			for j in range(-2, 3):
				matrix.setValue(h, x_center + i, z_center + j, material)
	def generateFirstFloorLine(x):
		matrix.setValue(h_first_floor, x, z_center - 3, border)
		matrix.setValue(h_first_floor, x, z_center - 1, border)
		matrix.setValue(h_first_floor, x, z_center, border)
		matrix.setValue(h_first_floor, x, z_center + 1, border)
		matrix.setValue(h_first_floor, x, z_center + 3, border)
	generateFirstFloorLine(x_center - 3)
	generateFirstFloorLine(x_center + 3)
	matrix.setValue(h_first_floor, x_center - 1, z_center - 3, border)
	matrix.setValue(h_first_floor, x_center, z_center - 3, border)
	matrix.setValue(h_first_floor, x_center + 1, z_center - 3, border)
	matrix.setValue(h_first_floor, x_center - 1, z_center + 3, border)
	matrix.setValue(h_first_floor, x_center, z_center + 3, border)
	matrix.setValue(h_first_floor, x_center + 1, z_center + 3, border)

	# second floor
	logger.info("Fountain second floor height : {}".format(h_second_floor))
	for h in range(h_first_floor, h_second_floor):
		for i in range(-1, 2):
			for j in range(-1, 2):
				matrix.setValue(h, x_center + i, z_center + j, material)
	matrix.setValue(h_second_floor, x_center - 1, z_center - 1, border)
	matrix.setValue(h_second_floor, x_center - 1, z_center + 1, border)
	matrix.setValue(h_second_floor, x_center + 1, z_center - 1, border)
	matrix.setValue(h_second_floor, x_center + 1, z_center + 1, border)
