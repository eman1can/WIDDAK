from pymclevel import alphaMaterials, BoundingBox
import utilityFunctions as utilityFunctions
import random
import math
import os
import RNG
import logging
from SpacePartitioning import binarySpacePartitioning, quadtreeSpacePartitioning
import GenerateHouse
import GenerateBuilding
import GenerateGreenhouse
import GenerateWell
import BlocksInfo as BlocksInfo
from Earthworks import prepareLot, prepareArea
import GeneratePath
import EnvironmentAnalyzer

# change to INFO if you want a verbose log!
logging.basicConfig(filename="log", level=logging.WARNING, filemode='w')

# remove INFO logs from pymclevel
#logging.getLogger("pymclevel").setLevel(logging.WARNING)

# Uncomment this to log to stdout as well!
#logging.getLogger().addHandler(logging.StreamHandler())

def perform(level, box, options):

	logging.info("BoundingBox coordinates: ({},{}),({},{}),({},{})".format(box.miny, box.maxy, box.minx, box.maxx, box.minz, box.maxz))

	# ==== PREPARATION =====
	(width, height, depth) = utilityFunctions.getBoxSize(box)
	logging.info("Selection box dimensions {}, {}, {}".format(width,height,depth))
	world = utilityFunctions.generateMatrix(level, box, width,depth,height)
	world_space = utilityFunctions.dotdict({"y_min": 0, "y_max": height-1, "x_min": 0, "x_max": width-1, "z_min": 0, "z_max": depth-1})
	height_map = utilityFunctions.getHeightMap(level,box, None, False)

	# === Wood quantity and Biome analyzer === #
	air_like = [0, 4, 5, 6, 20, 23, 29, 30, 35, 37, 38, 39, 40, 44, 46, 47, 50, 59, 66, 83, 85, 86, 95, 102, 104, 105, 107, 126, 141, 142, 160, 175]
	wood_height_map = utilityFunctions.getHeightMap(level, box, air_like, True)
	(usable_wood, biome) = EnvironmentAnalyzer.determinate_usable_wood(level, wood_height_map, box.minx, box.maxx, box.minz, box.maxz)

	# ===  City stats === #
	biome_with_well = ['Desert', 'Badlands']
	APARTMENT_SIZE = 2
	HOUSE_SIZE = 4
	GREENHOUSE_CAPACITY = 15
	inhabitants = 0
	greenhouse_count = 0
	well_count = 0

	# ==== PARTITIONING OF THE SELECTION IN AREA IN ORDER TO FLATTEN ====
	# Work in progress do not use
	#earthwork_height_map = utilityFunctions.getHeightMap(level,box, None, True)
	#area_partitioning_and_flattening(world_space, earthwork_height_map, world, biome)

	# ==== PARTITIONING OF NEIGHBOURHOODS ====
	(center, neighbourhoods) = generateCenterAndNeighbourhood(world_space, height_map)
	all_buildings = []

	# ====  GENERATING CITY CENTER ====
	minimum_h = 50
	minimum_w = 25
	mininum_d = 25

	iterate = 100
	minimum_lots = 6
	available_lots = 0
	maximum_tries = 50
	current_try = 0
	threshold = 1
	partitioning_list = []
	temp_partitioning_list = []

	# run the partitioning algorithm for iterate times to get different partitionings of the same area
	logging.info("Generating {} different partitionings for the the City Centre {}".format(iterate, center))
	while available_lots < minimum_lots and current_try < maximum_tries:

		for i in range(iterate):

			# generate a partitioning through some algorithm
			if RNG.random() < 0.5:
				partitioning = binarySpacePartitioning(center[0], center[1], center[2], center[3], center[4], center[5], [])
			else:
				partitioning = quadtreeSpacePartitioning(center[0], center[1], center[2], center[3], center[4], center[5], [])

			# remove invalid partitions from the partitioning
			valid_partitioning = []
			for p in partitioning:
				(y_min, y_max, x_min, x_max, z_min, z_max) = (p[0], p[1], p[2],p[3], p[4], p[5])
				failed_conditions = []
				cond1 = utilityFunctions.hasValidGroundBlocks(x_min, x_max,z_min,z_max, height_map)
				if cond1 == False: failed_conditions.append(1)
				cond2 = utilityFunctions.hasMinimumSize(y_min, y_max, x_min, x_max,z_min,z_max, minimum_h, minimum_w, mininum_d)
				if cond2 == False: failed_conditions.append(2)
				cond3 = utilityFunctions.hasAcceptableSteepness(x_min, x_max,z_min,z_max, height_map, utilityFunctions.getScoreArea_type1, threshold)
				if cond3 == False: failed_conditions.append(3)
				if cond1 and cond2 and cond3:
					score = utilityFunctions.getScoreArea_type1(height_map, x_min, x_max, z_min, z_max)
					valid_partitioning.append((score, p))
				else:
					logging.info("Failed Conditions {}".format(failed_conditions))

			partitioning_list.extend(valid_partitioning)
			logging.info("Generated a partition with {} valid lots and {} invalids ones".format(len(valid_partitioning), len(partitioning)-len(valid_partitioning)))

		# order partitions by steepness
		partitioning_list = sorted(partitioning_list)
		final_partitioning = utilityFunctions.getNonIntersectingPartitions(partitioning_list)

		available_lots = len(final_partitioning)
		logging.info("Current partitioning with most available_lots: {}, current threshold {}".format(available_lots, threshold))

		threshold += 1
		current_try += 1

	logging.info("Final lots ({}) for the City Centre {}: ".format(len(final_partitioning), center))
	for p in final_partitioning:
		logging.info("\t{}".format(p))

	for partition in final_partitioning:
		building, apartments_inhabitants = generateBuilding(world, partition, height_map, usable_wood, biome)
		inhabitants += apartments_inhabitants
		all_buildings.append(building)

	# ==== GENERATING NEIGHBOURHOODS ====

	minimum_h = 10
	minimum_w = 16
	mininum_d = 16

	iterate = 100
	maximum_tries = 50
	current_try = 0
	minimum_lots = 20
	available_lots = 0
	threshold = 1
	partitioning_list = []
	final_partitioning = []

	while available_lots < minimum_lots and current_try < maximum_tries:
		partitioning_list = []
		for i in range(iterate):
			for neigh in neighbourhoods:
				logging.info("Generating {} different partitionings for the neighbourhood {}".format(iterate, neigh))

				if RNG.random() < 0.5:
					partitioning = binarySpacePartitioning(neigh[0], neigh[1], neigh[2], neigh[3], neigh[4], neigh[5], [])
				else:
					partitioning = quadtreeSpacePartitioning(neigh[0], neigh[1], neigh[2], neigh[3], neigh[4], neigh[5], [])

				valid_partitioning = []
				for p in partitioning:
					(y_min, y_max, x_min, x_max, z_min, z_max) = (p[0], p[1], p[2],p[3], p[4], p[5])
					failed_conditions = []
					cond1 = utilityFunctions.hasValidGroundBlocks(x_min, x_max,z_min,z_max, height_map)
					if cond1 == False: failed_conditions.append(1)
					cond2 = utilityFunctions.hasMinimumSize(y_min, y_max, x_min, x_max,z_min,z_max, minimum_h, minimum_w, mininum_d)
					if cond2 == False: failed_conditions.append(2)
					cond3 = utilityFunctions.hasAcceptableSteepness(x_min, x_max,z_min,z_max, height_map, utilityFunctions.getScoreArea_type1, threshold)
					if cond3 == False: failed_conditions.append(3)
					if cond1 and cond2 and cond3:
						score = utilityFunctions.getScoreArea_type1(height_map, x_min, x_max, z_min, z_max)
						valid_partitioning.append((score, p))
						logging.info("Passed the 3 conditions!")
					else:
						logging.info("Failed Conditions {}".format(failed_conditions))

				partitioning_list.extend(valid_partitioning)
				logging.info("Generated a partition with {} valid lots and {} invalids ones".format(len(valid_partitioning), len(partitioning)-len(valid_partitioning)))

		temp_partitioning_list.extend(partitioning_list)
		# order partitions by steepness
		temp_partitioning_list = sorted(temp_partitioning_list)
		final_partitioning = utilityFunctions.getNonIntersectingPartitions(temp_partitioning_list)

		available_lots = len(final_partitioning)
		logging.info("Current neighbourhood partitioning with most available_lots: {}, current threshold {}".format(available_lots, threshold))

		threshold += 1
		current_try += 1

		logging.info("Final lots ({})for the neighbourhood {}: ".format(len(final_partitioning), neigh))
		for p in final_partitioning:
			logging.info("\t{}".format(p))

	for partition in final_partitioning:
		if well_count < 1 and biome in biome_with_well :
			well = generateWell(world, partition, height_map, biome)
			well_count += 1
			all_buildings.append(well)
		elif greenhouse_count * GREENHOUSE_CAPACITY < inhabitants :
			greenhouse = generateGreenhouse(world, partition, height_map, usable_wood, biome)
			greenhouse_count += 1
			all_buildings.append(greenhouse)
		else :
			house = generateHouse(world, partition, height_map, usable_wood, biome)
			inhabitants += RNG.randint(1, HOUSE_SIZE)
			all_buildings.append(house)

	# ==== GENERATE PATH MAP  ====
 	# generate a path map that gives the cost of moving to each neighbouring cell
	pathMap = utilityFunctions.getPathMap(height_map, width, depth)

	# ==== CONNECTING BUILDINGS WITH ROADS  ====
	logging.info("Calling MST on {} buildings".format(len(all_buildings)))
	MST = utilityFunctions.getMST_Manhattan(all_buildings, pathMap, height_map)

	pavementBlockID = BlocksInfo.getPavmentId(biome)
	for m in MST:
		p1 = m[1]
		p2 = m[2]
		logging.info("Pavement with distance {} between {} and {}".format(m[0], p1.entranceLot, p2.entranceLot))

	 	path = utilityFunctions.aStar(p1.entranceLot, p2.entranceLot, pathMap, height_map)
	 	if path != None:
	 		logging.info("Found path between {} and {}. Generating road...".format(p1.entranceLot, p2.entranceLot))
		 	GeneratePath.generatPath(world, path, height_map, pavementBlockID)
		else:
			logging.info("Couldnt find path between {} and {}. Generating a straight road between them...".format(p1.entranceLot, p2.entranceLot))
	 		GeneratePath.generatPath_StraightLine(world, p1.entranceLot[1], p1.entranceLot[2], p2.entranceLot[1], p2.entranceLot[2], height_map, pavementBlockID)

	# ==== UPDATE WORLD ====
	world.updateWorld()

def area_partitioning_and_flattening(space, height_map, matrix, biome):
	minimum_h = 10
	minimum_w = 40
	mininum_d = 40

	iterate = 100
	maximum_tries = 50
	current_try = 0
	minimum_lots = 100 #origin = 20
	available_lots = 0
	threshold = 10
	partitioning_list = []
	final_partitioning = []

	while available_lots < minimum_lots and current_try < maximum_tries:
		partitioning_list = []
		for i in range(iterate):

			# generate a partitioning through some algorithm
			if RNG.random() < 0.5:
				partitioning = binarySpacePartitioning(space.y_min, space.y_max, space.x_min, space.x_max, space.z_min, space.z_max, [])
			else:
				partitioning = quadtreeSpacePartitioning(space.y_min, space.y_max, space.x_min, space.x_max, space.z_min, space.z_max, [])

			# remove invalid partitions from the partitioning
			valid_partitioning = []
			for p in partitioning:
				(y_min, y_max, x_min, x_max, z_min, z_max) = (p[0], p[1], p[2],p[3], p[4], p[5])
				failed_conditions = []
				#cond2 = utilityFunctions.hasMinimumSize(y_min, y_max, x_min, x_max,z_min,z_max, minimum_h, minimum_w, mininum_d)
				#if cond2 == False: failed_conditions.append(2)
				cond3 = utilityFunctions.hasAcceptableSteepness(x_min, x_max,z_min,z_max, height_map, utilityFunctions.getScoreArea_type1, threshold)
				if cond3 == False: failed_conditions.append(3)
				if cond3:
					heightCounts = utilityFunctions.getHeightCounts(height_map, x_min, x_max, z_min, z_max)
					score =  max(heightCounts, key=heightCounts.get)
					valid_partitioning.append((score, p))
				else:
					logging.info("Failed Conditions {}".format(failed_conditions))

			partitioning_list.extend(valid_partitioning)
			logging.info("Generated a partition with {} valid area and {} invalids ones".format(len(valid_partitioning), len(partitioning)-len(valid_partitioning)))

		# order partitions by steepness
		partitioning_list = sorted(partitioning_list)
		final_partitioning = utilityFunctions.fusionIntersectingPartitions(partitioning_list, height_map)

		available_lots = len(final_partitioning)
		logging.info("Current partitioning with most available_lots: {}, current threshold {}".format(available_lots, threshold))

		threshold = threshold + 1 if threshold < 20 else 20
		current_try += 1

	for partition in final_partitioning :
		prepareArea(matrix, partition, height_map, biome)

def generateCenterAndNeighbourhood(space, height_map):
	neighbourhoods = []
	logging.info("Generating Neighbourhood Partitioning...")
	center = utilityFunctions.getSubsection(space.y_min, space.y_max, space.x_min, space.x_max, space.z_min, space.z_max, 0.6)
	logging.info("Generated city center: {}".format(center))
	partitions = utilityFunctions.subtractPartition((space.y_min, space.y_max, space.x_min, space.x_max, space.z_min, space.z_max), center)
	for p in partitions:
		neighbourhoods.append(p)
		logging.info("Generated neighbourhood: {}".format(p))
	return (center, neighbourhoods)

def generateBuilding(matrix, p, height_map, usable_wood, biome):
	h = prepareLot(matrix, p, height_map, biome)
	building = GenerateBuilding.generateBuilding(matrix, h, p[1],p[2],p[3], p[4], p[5], usable_wood, biome)
	utilityFunctions.updateHeightMap(height_map, p[2]+1, p[3]-2, p[4]+1, p[5]-2, -1)
	return building

def generateGreenhouse(matrix, p, height_map, usable_wood, biome):
	h = prepareLot(matrix, p, height_map, biome)
	greenhouse = GenerateGreenhouse.generateGreenhouse(matrix, h, p[1], p[2], p[3], p[4], p[5], usable_wood, biome)
	utilityFunctions.updateHeightMap(height_map, p[2]+3, p[3]-3, p[4]+2, p[5]-2, -1)
	return greenhouse

def generateWell(matrix, p, height_map, biome):
	h = prepareLot(matrix, p, height_map, biome)
	well = GenerateWell.generateWell(matrix, h, p[1], p[2], p[3], p[4], p[5], biome)
	utilityFunctions.updateHeightMap(height_map, p[2] + 1, p[3] - 2, p[4] + 1, p[5]-2, -1)
	return well

def generateHouse(matrix, p, height_map, usable_wood, biome):
	logging.info("Generating a house in lot {}".format(p))
	logging.info("Terrain before flattening: ")
	for x in range (p[2], p[3]):
		line = ""
		for z in range(p[4], p[5]):
			line += str(height_map[x][z])+" "
		logging.info(line)

	h = prepareLot(matrix, p, height_map, biome)

	logging.info("Terrain after flattening: ")
	for x in range (p[2], p[3]):
		line = ""
		for z in range(p[4], p[5]):
			line += str(height_map[x][z])+" "
		logging.info(line)
	house = GenerateHouse.generateHouse(matrix, h, p[1],p[2],p[3], p[4], p[5], biome, usable_wood)

	utilityFunctions.updateHeightMap(height_map, p[2]+1, p[3]-1, p[4]+1, p[5]-1, -1)

	logging.info("Terrain after construction: ")
	for x in range (p[2], p[3]):
		line = ""
		for z in range(p[4], p[5]):
			line += str(height_map[x][z])+" "
		logging.info(line)

	return house
