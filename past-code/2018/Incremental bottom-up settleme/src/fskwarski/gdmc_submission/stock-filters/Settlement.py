import time
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

from SettlementGenerator import Generator
from SettlementMap import Map


# lots of spaces to align checkboxes
inputs = (
			("Incremental Bottom-Up Settlement Generation", "label"),
			("Seed                          ", 10),
			("Number of structures  ", 50),
			("Generate fences                                             ", True),
			("Allow terrain to be modified                             ", True),
			("Allow roads across rough terrain                      ", False),
			# ("Plan ahead (slow)                                           ", False),

			("Note: Selection area should reach below the ground and above the trees. Generation may take a while, esp. clearing trees (check console for progress).", "label"),
	)


def perform(level, box, options):
	start_time = time.time()

	wood_blocks = set([17, 162, 99, 100])
	leaf_blocks = set([18, 161, 106])
	decorative_blocks = set([6, 30, 31, 32, 37, 38, 39, 40, 50, 51, 55, 59, 63, 78, 81, 104, 105, 111, 141, 142, 175, 207])
	impassable_blocks = set([8, 9, 10, 11, 79])

	plank_conversion = {
						(17,0): (5,0),
						(17,1): (5,1),
						(17,2): (5,2),
						(17,3): (5,3),
						(162,0): (5,4),
						(162,1): (5,5),
						(99,0): (5,1), # mushrooms converted into wood
						(100,1): (5,3), # mushrooms converted into wood
					}

	log_conversion = {
						(17,0): (17,0),
						(17,1): (17,1),
						(17,2): (17,2),
						(17,3): (17,3),
						(162,0): (162,0),
						(162,1): (162,1),
						(99,0): (17,1),
						(100,1): (17,3),
					}

	fence_conversion = {
						(17,0): (85,0),
						(17,1): (189,0),
						(17,2): (188,0),
						(17,3): (190,0),
						(162,0): (191,0),
						(162,1): (192,0),
						(99,0): (189,0),
						(100,1): (190,0),
					}

	# the following are only used initially for filling map during generation, then mostly overriden during final step
	materials = {
					'wall': (4,0),
					'floor': (5,0),
					'road': (98,0),
					'plaza': (43,5),
					'farm': (60,0),
				}

	sizes_big_w, sizes_big_h = [13, 15], [11, 13]
	sizes_w, sizes_h = [9, 11], [7, 9]
	sizes_plaza_w, sizes_plaza_h = [7, 9], [7, 9]
	sizes_farm_w, sizes_farm_h = [11, 13, 15], [5, 7, 9]

	entry_distance = 3
	reserved_space = 4
	road_distance = 1


	# use_buffer = options['Plan ahead (slow)                                           ']
	use_buffer = False

	add_fences = options['Generate fences                                             ']
	roads_can_cross_corners = options['Allow roads across rough terrain                      ']
	modify_terrain = options['Allow terrain to be modified                             ']
	modify_terrain_roads = modify_terrain
	seed = options['Seed                          ']
	number_of_structures = options['Number of structures  ']


	# max_attempts: number of positions considered when placing each structure (higher value = better layouts but slower generation, lower value = opposite)
	max_attempts = 5000


	print("\nStep 1: generate heightmap")

	map = Map(level, box, impassable_blocks, wood_blocks, leaf_blocks, decorative_blocks, False, False, roads_can_cross_corners, start_time)


	print("\nStep 2: generate structures")

	generator = Generator(level, box, options, map, materials, seed, start_time)

	sequence = []
	for i in xrange(number_of_structures):
		category = i % 9

		if category == 0:
			sequence.append((choice(sizes_big_w), choice(sizes_big_h), 7, entry_distance, reserved_space, road_distance, 'house'))
		elif category == 1:
			sequence.append((choice(sizes_plaza_w), choice(sizes_plaza_h), 5, entry_distance, reserved_space, road_distance, 'plaza'))
		elif category >= 2 and category <= 5:
			sequence.append((choice(sizes_w), choice(sizes_h), 5, entry_distance, reserved_space, road_distance, 'house'))
		elif category >= 6:
			sequence.append((choice(sizes_farm_w), choice(sizes_farm_h), 5, entry_distance, reserved_space, road_distance, 'farm'))

	# generator.add_sequence(sequence[:2], max_attempts, modify_terrain, modify_terrain_roads, use_buffer, start_time)
	generator.add_sequence(sequence, max_attempts, modify_terrain, modify_terrain_roads, use_buffer, start_time)


	print("\nStep 3: postprocessing")

	# expand roads

	blocks_copy = copy(map.blocks)
	blocks_updated = copy(map.blocks)
	reserved_materials = set([materials['wall'][0], materials['floor'][0], materials['farm'][0], materials['plaza'][0]])

	for x in xrange(1, map.w-1):
		for y in xrange(1, map.h-1):
			if map.blocks[x,y] == materials['road'][0]:
				for x2 in xrange(x-1, x+2):
					for y2 in xrange(y-1, y+2):
						if map.altitudes[x2,y2] == map.altitudes[x,y] and not map.blocks[x2,y2] in reserved_materials:
							map.fill_block(x2, y2, map.altitudes[x,y], materials['road'])
							map.clear_space(x2, y2, map.altitudes[x,y]+1)
							map.blocks[x2,y2] = blocks_copy[x2,y2]
							blocks_updated[x2,y2] = materials['road'][0]

	# determine materials

	print("")
	print("Tree area: %f" % map.tree_area)
	print("")
	for k, v in map.tree_probabilities.items():
		print("  %-20s %f" % (k, v))

	tree_keys = sorted(map.tree_probabilities.keys(), key=lambda k: map.tree_probabilities[k], reverse=True)
	if len(tree_keys) > 0:
		wood_source = tree_keys[0]
	else:
		wood_source = (5,0)

	print("\nTree keys: %s" % (tree_keys,))


	# add fences (if applicable)

	if add_fences:
		print("  Adding fences...")
		map.place_fences(blocks_updated, reserved_materials, impassable_blocks, materials, fence_conversion, wood_source)


	# everything associated with clearing trees starts here

	print("  Clearing trees...")

	tree_points = []
	for x in xrange(0, map.w):
		for y in xrange(0, map.h):
			if map.trees[x,y] != None:
				tree_points.append((x,y))

	# get a table of nearest tree coordinates for every point
	# this is used to approximate which tree the surrounding leaves belong to, though the approach isn't perfectly accurate)
	# it also doesn't extend beyond selection box, meaning that trees around it may get cut in half, etc.

	nearest_tree_table = empty((map.w,map.h), object)
	if len(tree_points) > 0:
		for x in xrange(0, map.w):
			for y in xrange(0, map.h):
				nearest_tree_table[x,y] = (x,y)
				if map.trees[x,y] == None:
					for d in xrange(1, max(map.w,map.h)):
						points = []

						for i in xrange(0, d+1):
							x1 = x - d + i;
							y1 = y - i;
							if x1 >= 0 and y1 >= 0 and x1 < map.w and y1 < map.h and map.trees[x1,y1] != None:
								points.append((x1,y1))
							x2 = x + d - i;
							y2 = y + i;
							if x2 >= 0 and y2 >= 0 and x2 < map.w and y2 < map.h and map.trees[x2,y2] != None:
								points.append((x2,y2))

						for i in xrange(1, d):
							x1 = x - i;
							y1 = y + d - i;
							if x1 >= 0 and y1 >= 0 and x1 < map.w and y1 < map.h and map.trees[x1,y1] != None:
								points.append((x1,y1))
							x2 = x + d - i;
							y2 = y - i;
							if x2 >= 0 and y2 >= 0 and x2 < map.w and y2 < map.h and map.trees[x2,y2] != None:
								points.append((x2,y2))

						if points:
							ordered_points = sorted(points, key=lambda position: map.get_distance(position[0], position[1], x, y))
							nearest_tree_table[x,y] = ordered_points[0]
							break

	# actually clear trees

	for x in xrange(0, map.w):
		for y in xrange(0, map.h):
			if map.trees[x,y] != None:
				tree_near_settlement = False
				distance = 8

				for x2 in xrange(max(0,x-distance), min(map.w,x+distance)):
					for y2 in xrange(max(0,y-distance), min(map.h,y+distance)):

						if map.blocks[x2,y2] in reserved_materials or map.blocks[x2,y2] == materials['road'][0]:
							tree_near_settlement = True

					if tree_near_settlement:
						break

				if tree_near_settlement:
					map.clear_tree(x, y, nearest_tree_table)


	# generate final versions of buildings

	print("  Generating buildings...")

	for structure in generator.structures:
		structure.generate_details(map.tree_area, map.tree_probabilities, plank_conversion, log_conversion, wood_source)


	print("\nDone (total time elapsed: %i s)." % (time.time() - start_time,))