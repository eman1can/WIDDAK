from pymclevel import alphaMaterials, BoundingBox
import toolbox as toolbox
import random
import math
import os
import RNG
import logging
from SpacePartitioning import binarySpacePartitioning, quadtreeSpacePartitioning
import House
import Building
import Path
import Bridge
import Tower
import Farm
import RollerCoaster
import TrainLine
import Fountain
from Earthworks import prepareLot
import TreeGestion
import time

displayName = "Train City"

inputs = (
	("University of Tsukuba - Adrien CELERIER - GDMC", "label"),
	("Generation", True),
	("Settlement type", ("City",
						"Village",
						"City Center",
						"Amusement Park",
						"Test",
						)),
	("allow Train Line", True),
	("Train Line Style", ("Urban", "Country"),)
)

# change to INFO if you want a verbose log!
for handler in logging.root.handlers[:]:
   logging.root.removeHandler(handler)
logging.basicConfig(filename="log", level=logging.INFO, filemode='w')

# remove INFO logs from pymclevel
#logging.getLogger("pymclevel").setLevel(logging.WARNING)

# Uncomment this to log to stdout as well!
#logging.getLogger().addHandler(logging.StreamHandler())

def perform(level, box, options):
	logging.info("BoundingBox coordinates: ({},{}),({},{}),({},{})".format(box.miny, box.maxy, box.minx, box.maxx, box.minz, box.maxz))

	# ==== PREPARATION =====
	logging.info("Options : {}".format(options))
	logging.info("Preparation")
	(width, height, depth) = toolbox.getBoxSize(box)
	logging.info("Selection box dimensions {}, {}, {}".format(width,height,depth))
	world = toolbox.generateMatrix(level, box, width,depth,height)
	world_space = toolbox.dotdict({"y_min": 0, "y_max": height-1, "x_min": 0, "x_max": width-1, "z_min": 0, "z_max": depth-1})
	logging.info("Generating simple height map")
	simple_height_map = toolbox.getSimpleHeightMap(level,box) #no height = -1 when water like block
	logging.info("Saving and erasing the trees")
	tree_list = TreeGestion.prepareMap(world, simple_height_map) #get a list of all trees and erase them, so we can put some of them back after
	logging.info("Generating normal height map")
	height_map = toolbox.getHeightMap(level,box)
	logging.info("Preparing settlement deck card")
	cityDeck = toolbox.generateCityDeck(options["Settlement type"], width, depth)
	logging.info("Setting the settlement type")
	tree_counter = TreeGestion.countTreeSpecies(tree_list)
	logging.info("Counting the occurrence of the different tree species in the area")
	wood_material = TreeGestion.selectWoodFromTreeCounter(tree_counter)

	# ==== PARTITIONING OF NEIGHBOURHOODS ====
	logging.info("Partitioning of the map, getting city center and neighbourhoods")
	(center, neighbourhoods) = generateCenterAndNeighbourhood(world_space, height_map)
	all_buildings = []

	# ====  GENERATING CITY CENTER ====
	logging.info("Generating city center")
	minimum_h = 50
	minimum_w = 25
	mininum_d = 25

	iterate = 100
	minimum_lots = 6
	available_lots = 0
	maximum_tries = 50
	current_try = 0
	threshold = 20
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
				cond1 = toolbox.hasValidGroundBlocks(x_min, x_max,z_min,z_max, height_map)
				if cond1 == False: failed_conditions.append(1)
				cond2 = toolbox.hasMinimumSize(y_min, y_max, x_min, x_max,z_min,z_max, minimum_h, minimum_w, mininum_d)
				if cond2 == False: failed_conditions.append(2)
				cond3 = toolbox.hasAcceptableSteepness(x_min, x_max, z_min, z_max, height_map, toolbox.getScoreArea_type4, threshold)
				if cond3 == False: failed_conditions.append(3)
				if cond1 and cond2 and cond3:
					score = toolbox.getScoreArea_type4(height_map, x_min, x_max, z_min, z_max)
					valid_partitioning.append((score, p))
					logging.info("Passed the 3 conditions!")
				else:
					logging.info("Failed Conditions {}".format(failed_conditions))

			partitioning_list.extend(valid_partitioning)
			logging.info("Generated a partition with {} valid lots and {} invalids ones".format(len(valid_partitioning), len(partitioning)-len(valid_partitioning)))

		# sort partitions by steepness
		partitioning_list = sorted(partitioning_list)
		final_partitioning = toolbox.getNonIntersectingPartitions(partitioning_list)

		available_lots = len(final_partitioning)
		logging.info("Current partitioning with most available_lots: {}, current threshold {}".format(available_lots, threshold))

		threshold += 2
		current_try += 1

	logging.info("Final lots ({}) for the City Centre {}: ".format(len(final_partitioning), center))
	for (score, partition) in final_partitioning:
		logging.info("\t{}".format(partition))

	#for (score, partition) in final_partitioning:
	#	#building = generateBuilding(world, partition, height_map, simple_height_map)
	#	wood_material = TreeGestion.selectWoodFromTreeCounter(tree_counter)
	#	logging.info("Wood material used : {}".format(wood_material))
	#	building = generateStructureFromDeck(world, score, partition, height_map, simple_height_map, wood_material, cityDeck, "center")
	#	all_buildings.append(building)

	l = len(final_partitioning)
	fountain = generateFountain(world, final_partitioning[0][1], height_map, simple_height_map)
	all_buildings.append(fountain)
	for i in range(1, l):
		wood_material = TreeGestion.selectWoodFromTreeCounter(tree_counter)
		logging.info("Wood material used : {}".format(wood_material))
		score = i / (l * 1.0) # turns the result to float
		building = generateStructureFromDeck(world, score, final_partitioning[i][1], height_map, simple_height_map, wood_material, cityDeck, "center")
		all_buildings.append(building)

	# ==== GENERATING NEIGHBOURHOODS ====
	logging.info("Generating neighbourhoods")
	minimum_h = 10
	minimum_w = 16
	mininum_d = 16

	iterate = 100
	maximum_tries = 80
	current_try = 0
	minimum_lots = 50
	available_lots = 0
	threshold = 50
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
					(y_min, y_max, x_min, x_max, z_min, z_max) = (p[0], p[1], p[2], p[3], p[4], p[5])
					failed_conditions = []
					cond1 = toolbox.hasValidGroundBlocks(x_min, x_max,z_min,z_max, height_map)
					if cond1 == False: failed_conditions.append(1)
					cond2 = toolbox.hasMinimumSize(y_min, y_max, x_min, x_max,z_min,z_max, minimum_h, minimum_w, mininum_d)
					if cond2 == False: failed_conditions.append(2)
					cond3 = toolbox.hasAcceptableSteepness(x_min, x_max, z_min, z_max, height_map, toolbox.getScoreArea_type4, threshold)
					if cond3 == False: failed_conditions.append(3)
					if cond1 and cond2 and cond3:
						score = toolbox.getScoreArea_type4(height_map, x_min, x_max, z_min, z_max)
						valid_partitioning.append((score, p))
						logging.info("Passed the 3 conditions!")
					else:
						logging.info("Failed Conditions {}".format(failed_conditions))

				partitioning_list.extend(valid_partitioning)
				logging.info("Generated a partition with {} valid lots and {} invalids ones".format(len(valid_partitioning), len(partitioning)-len(valid_partitioning)))

		temp_partitioning_list.extend(partitioning_list)

		# sort partitions by steepness
		temp_partitioning_list = sorted(temp_partitioning_list)
		final_partitioning = toolbox.getNonIntersectingPartitions(temp_partitioning_list)

		available_lots = len(final_partitioning)
		logging.info("Current neighbourhood partitioning with most available_lots: {}, current threshold {}".format(available_lots, threshold))

		threshold += 2
		current_try += 1

	logging.info("Final lots ({})for the neighbourhood {}: ".format(len(final_partitioning), neigh))
	for (score, partition) in final_partitioning:
		logging.info("\t{}".format(partition))

	logging.info("Building in the neighbourhood")

	#for (score, partition) in final_partitioning:
	#	wood_material = TreeGestion.selectWoodFromTreeCounter(tree_counter)
	#	logging.info("Wood material used : {}".format(wood_material))
	#	building = generateStructureFromDeck(world, score, partition, height_map, simple_height_map, wood_material, cityDeck, "neighbourhood")
	#	all_buildings.append(building)

	l = len(final_partitioning)
	for i in range(l):
		wood_material = TreeGestion.selectWoodFromTreeCounter(tree_counter)
		logging.info("Wood material used : {}".format(wood_material))
		score = i / (l * 1.0) # turns the result to float
		building = generateStructureFromDeck(world, score, final_partitioning[i][1], height_map, simple_height_map, wood_material, cityDeck, "neighbourhood")
		all_buildings.append(building)

	#n = 0
	#for i in xrange(0, int(len(final_partitioning) * 0.50) + 1):
	#	house = generateHouse(world, final_partitioning[i], height_map, simple_height_map)
	#	all_buildings.append(house)
	#	logging.info("House number : {} built on lot number {}".format(n + 1, i + 1))
	#	n += 1
	#n = 0
	#for i in xrange(int(len(final_partitioning) * 0.50) + 1, int(len(final_partitioning) * 0.70) + 1):
	#	# generate either a regular farm or a smiley farm
	#	farm = generateFarm(world, final_partitioning[i], height_map, simple_height_map) if (RNG.randint(0, 2) == 0) else generateFarm(world, final_partitioning[i], height_map, simple_height_map, "smiley")
	#	all_buildings.append(farm)
	#	logging.info("Farm number : {} built on lot number {}".format(n + 1, i + 1))
	#	n += 1
	#n = 0
	#m = 0
	#for i in xrange(int(len(final_partitioning)*0.70)+1, len(final_partitioning)):
	#	RollerCoaster = generateRollerCoaster(world, final_partitioning[i], height_map, simple_height_map)
	#	if RollerCoaster.type == "tower":
	#		all_buildings.append(RollerCoaster)
	#		logging.info("Tower number : {} built on lot number {}".format(n + 1, i + 1))
	#		n += 1
	#	else:
	#		logging.info("RollerCoaster number : {} built on lot number {}".format(m + 1, i + 1))
	#		m += 1

	# ==== GENERATE THE TrainLine NETWORK ====
	if options["allow Train Line"] == True:
		wood_material = "urban" if options["Train Line Style"] == "Urban" else TreeGestion.selectWoodFromTreeCounter(tree_counter)

		stations = generateTrainLine(world, center, height_map, simple_height_map, wood_material, cityDeck.getNbStations())
		for station in stations:
			all_buildings.append(station)

	# ==== GENERATE PATH MAP  ====
	# generate a path map that gives the cost of moving to each neighbouring cell
	logging.info("Generating path map and simple path map")
	pathMap = toolbox.getPathMap(height_map, width, depth)
	simple_pathMap = toolbox.getPathMap(simple_height_map, width, depth) #not affected by water

	# ==== CONNECTING BUILDINGS WITH ROADS  ====
	logging.info("Calling MST on {} buildings".format(len(all_buildings)))
	MST = toolbox.getMST_Manhattan(all_buildings)

	for m in MST:
		p1 = m[1]
		p2 = m[2]
		if p1.type == "farm" or p2.type == "farm":
			pavement_Type = "Grass"
			bridge_Type = "Wood"
		else:
			pavement_Type = "Stone"
			bridge_Type = "Stone"

		try:
			logging.info("Trying to find a path between {} and {}, finding potential bridges".format(p1.entranceLot, p2.entranceLot))
			simple_path = toolbox.simpleAStar(p1.entranceLot, p2.entranceLot, simple_pathMap, simple_height_map) #water and height are not important
			list_end_points = toolbox.findBridgeEndPoints(world, simple_path, simple_height_map)

			if list_end_points != []:
				for i in xrange(0,len(list_end_points),2):
					logging.info("Found water between {} and {}. Trying to generating a {} bridge...".format(list_end_points[i], list_end_points[i+1], bridge_Type))
					Bridge.generateBridge(world, simple_height_map, list_end_points[i], list_end_points[i+1], bridge_Type)
				list_end_points.insert(0, p1.entranceLot)
				list_end_points.append(p2.entranceLot)
				for i in xrange(0,len(list_end_points),2):
					path = toolbox.aStar(list_end_points[i], list_end_points[i+1], pathMap, height_map)
					logging.info("Connecting end points of the bridge(s), Generating {} road between {} and {}".format(pavement_Type, list_end_points[i], list_end_points[i+1]))
					Path.generatePath(world, path, height_map, pavement_Type)
			else:
				logging.info("No potential bridge found, Generating road between {} and {}".format(list_end_points[i], list_end_points[i+1]))
				Path.generatePath(world, simple_path, height_map, pavement_Type)

		except:
			logging.info("Bridge found but is not buildable, Trying to find a path between {} and {} avoiding water".format(p1.entranceLot, p2.entranceLot))
			path = toolbox.aStar(p1.entranceLot, p2.entranceLot, pathMap, height_map)
			if path != None:
				logging.info("Path found, Generating {} road between {} and {}".format(pavement_Type, p1.entranceLot, p2.entranceLot))
				Path.generatePath(world, path, height_map, pavement_Type)
			else:
				logging.info("Couldnt find path between {} and {}. Generating a straight road".format(p1.entranceLot, p2.entranceLot))
				#Path.generatePath_StraightLine(world, p1.entranceLot[1], p1.entranceLot[2], p2.entranceLot[1], p2.entranceLot[2], height_map, pavement_Type)

	# ==== PUT BACK UNTOUCHED TREES ====
	logging.info("Putting back untouched trees")
	TreeGestion.putBackTrees(world, height_map, tree_list) #put back the trees that are not cut buy the building and are not in unwanted places

	# ==== UPDATE WORLD ====
	if options["Generation"] == True:
		logging.info("Generating the world")
		world.updateWorld()
	else:
		logging.info("Generation set to false, stops here")

def generateCenterAndNeighbourhood(space, height_map):
	neighbourhoods = []
	logging.info("Generating Neighbourhood Partitioning...")
	center = toolbox.getSubsection(space.y_min, space.y_max, space.x_min, space.x_max, space.z_min, space.z_max, 0.6)
	logging.info("Generated city center: {}".format(center))
	partitions = toolbox.subtractPartition((space.y_min, space.y_max, space.x_min, space.x_max, space.z_min, space.z_max), center)
	for p in partitions:
		neighbourhoods.append(p)
		logging.info("Generated neighbourhood: {}".format(p))
	return (center, neighbourhoods)

def generateBuilding(matrix, p, height_map, simple_height_map):
	logging.info("Generating a building in lot {}".format(p))
	h = prepareLot(matrix, p, height_map, (43, 8))
	building = Building.generateBuilding(matrix, h, p[1],p[2],p[3], p[4], p[5])
	toolbox.updateHeightMap(height_map, p[2]+1, p[3]-1, p[4]+1, p[5]-1, -1)
	toolbox.updateHeightMap(simple_height_map, p[2]+1, p[3]-1, p[4]+1, p[5]-1, -1)
	return building

def generateHouse(matrix, p, height_map, simple_height_map, wood_material):
	logging.info("Generating a house in lot {}".format(p))
	h = prepareLot(matrix, p, height_map, None)
	house = House.generateHouse(matrix, wood_material, h, p[1], p[2], p[3], p[4], p[5])
	toolbox.updateHeightMap(height_map, p[2]+1, p[3]-1, p[4]+1, p[5]-1, -1)
	toolbox.updateHeightMap(simple_height_map, p[2]+1, p[3]-1, p[4]+1, p[5]-1, -1)
	return house

def generateFarm(matrix, p, height_map, simple_height_map, wood_material, farmType = None):
	logging.info("Generating a farm in lot {}".format(p))
	h = prepareLot(matrix, p, height_map, None)
	farm = Farm.generateFarm(matrix, wood_material, h, p[1], p[2], p[3], p[4], p[5], farmType)
	toolbox.updateHeightMap(height_map, p[2] + 1, p[3] - 2, p[4] + 1, p[5] - 2, -1)
	return farm

def generateRollerCoaster(matrix, p, height_map, simple_height_map, wood_material):
	logging.info("Trying to generate a RollerCoaster in lot {}".format(p))
	structure = RollerCoaster.generateRollerCoaster(matrix, wood_material, height_map, p[1], p[2], p[3], p[4], p[5])
	if structure == False:
		logging.info("Generating RollerCoaster failed, Generating Tower instead")
		structure = generateTower(matrix, p, height_map, simple_height_map)
	return structure

def generateTower(matrix, p, height_map, simple_height_map):
	logging.info("Generating a tower in lot {}".format(p))
	tower = Tower.generateTower(matrix, p[2], p[3], p[4], p[5], height_map)
	toolbox.updateHeightMap(height_map, tower.buildArea.x_min, tower.buildArea.x_max, tower.buildArea.z_min, tower.buildArea.z_max, -1)
	toolbox.updateHeightMap(simple_height_map, tower.buildArea.x_min, tower.buildArea.x_max, tower.buildArea.z_min, tower.buildArea.z_max, -1)
	return tower

def generateTrainLine(matrix, center, height_map, simple_height_map, wood_material, nb_stations):
	train_line_partition = (center[0], center[1], center[2] - 2, center[3] + 2, center[4] - 2, center[5] + 2)
	(pillar_coordinates, stations) = TrainLine.generateTrainLine(matrix, wood_material, nb_stations, height_map, simple_height_map, train_line_partition[0], train_line_partition[1], train_line_partition[2], train_line_partition[3], train_line_partition[4], train_line_partition[5])
	for (x, z) in pillar_coordinates:
		toolbox.updateHeightMap(height_map, x, x, z, z, -1)
		toolbox.updateHeightMap(simple_height_map, x, x, z, z, -1)
	return stations

def generateFountain(matrix, p, height_map, simple_height_map):
	logging.info("Generating a fountain in lot {}".format(p))
	h = prepareLot(matrix, p, height_map, (43, 8))
	building = Fountain.generateFountain(matrix, h, p[1], p[2], p[3], p[4], p[5])
	toolbox.updateHeightMap(height_map, p[2] + 1, p[3] - 1, p[4] + 1, p[5] - 1, -1)
	toolbox.updateHeightMap(simple_height_map, p[2] + 1, p[3] - 1, p[4] + 1, p[5] - 1, -1)
	return building

def generateStructureFromDeck(world, score, partition, height_map, simple_height_map, wood_material, cityDeck, deck_type = "neighbourhood"):
	structure_type = cityDeck.popDeck(deck_type)
	size = cityDeck.getSize()[0] if deck_type == "center" else cityDeck.getSize()[1]
	while abs(toolbox.getStructureScore(structure_type) - score) > 0.3 and size > 0:
		logging.info("Structure of type : {} has a score too high ({} > 0.3).".format(structure_type, abs(toolbox.structure_scores[structure_type] - score)))
		logging.info("Picking a new card")
		cityDeck.putBackToDeck(deck_type, structure_type)
		structure_type = cityDeck.popDeck(deck_type)
		size -= 1
	logging.info("Generating a {} with lot score = {}".format(structure_type, score))
	if   structure_type == "house" :			return generateHouse(world, partition, height_map, simple_height_map, wood_material)
	elif structure_type == "building" :			return generateBuilding(world, partition, height_map, simple_height_map)
	elif structure_type == "fountain" :			return generateFountain(world, partition, height_map, simple_height_map)
	elif structure_type == "farm" :				return generateFarm(world, partition, height_map, simple_height_map, wood_material)
	elif structure_type == "slope structure" :	return generateRollerCoaster(world, partition, height_map, simple_height_map, wood_material)
	else:
		logging.info("Unable to find {} type of building from the settlement deck".format(structure_type))
		return None
