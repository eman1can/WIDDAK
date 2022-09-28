import time
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *


def get_block(level, x, y, z):
	return level.blockAt(x,y,z)


def set_block(level, (block, data), x, y, z):
	level.setBlockAt((int)(x),(int)(y),(int)(z), block)
	level.setBlockDataAt((int)(x),(int)(y),(int)(z), data)


def get_block_tuple(level, x, y, z):
	return (level.blockAt(x,y,z), level.blockDataAt(x,y,z))


def restricted_flood_fill(array, xsize, ysize, start_node, replace_value, max_steps):
	steps = 0
	source_value = array[start_node[0], start_node[1]]
	stack = set(((start_node[0], start_node[1]),))
	if replace_value == source_value:
		return steps
	while stack:
		x, y = stack.pop()
		if array[x, y] == source_value:
			array[x, y] = replace_value
			steps += 1
			if steps == max_steps:
				return steps
			else:
				if x > 0:
					stack.add((x - 1, y))
				if x < (xsize - 1):
					stack.add((x + 1, y))
				if y > 0:
					stack.add((x, y - 1))
				if y < (ysize - 1):
					stack.add((x, y + 1))
	return steps


class Map:
	def __init__(self, level, box, impassable_blocks, wood_blocks, leaf_blocks, decorative_blocks, clear_decorations, clear_trees, roads_can_cross_corners, start_time):
		self.level = level
		self.box = box

		self.x, self.y = box.minx, box.minz
		self.w, self.h = box.maxx-box.minx, box.maxz-box.minz

		self.impassable_blocks = impassable_blocks
		self.wood_blocks = wood_blocks
		self.leaf_blocks = leaf_blocks
		self.decorative_blocks = decorative_blocks

		self.setup(start_time, clear_decorations, clear_trees)
		self.tree_area, self.tree_probabilities = self.get_tree_data()
		self.collect_positions()

		self.roads_can_cross_corners = roads_can_cross_corners
		self.setup_grid(self.roads_can_cross_corners, self.impassable_blocks)
		self.buffer = []


	def setup(self, start_time, clear_decorations, clear_trees):
		print("  Generating heightmap...")

		self.blocks = zeros((self.w, self.h)).astype(int)
		self.altitudes = zeros((self.w, self.h)).astype(int)
		self.trees = empty((self.w,self.h), object)

		box = self.box
		level = self.level

		for x in xrange(box.minx, box.maxx):
			for z in xrange(box.minz, box.maxz):
				for y in xrange(box.maxy, box.miny, -1):

					block = get_block(level, x, y, z)
					if block != 0:
						if block in self.wood_blocks or block in self.leaf_blocks or (clear_decorations and block in self.decorative_blocks):
							block_data = get_block_tuple(level, x, y, z)
							if block_data != None and block_data[0] in self.wood_blocks:
								self.trees[x-self.x,z-self.y] = block_data

							if clear_trees:
								set_block(level, (0, 0), x, y, z)
								if get_block(level, x, y+1, z) in self.decorative_blocks:
									set_block(level, (0, 0), x, y+1, z)
						elif not block in self.decorative_blocks:
							self.altitudes[x-self.x,z-self.y] = int(y)
							self.blocks[x-self.x,z-self.y] = int(block)
							break

		print("  Done. (time elapsed: %i s)" % (time.time() - start_time))


	def get_tree_data(self):
		tree_frequency = {}
		tree_probabilities = {}
		for x in xrange(0, self.w):
			for y in xrange(0, self.h):
				value = self.trees[x,y]
				if value != None:
					if value not in tree_frequency.keys():
						tree_frequency[value] = 0
					tree_frequency[value] += 1
		tree_total = sum(tree_frequency.values())
		for k, v in tree_frequency.items():
			tree_probabilities[k] = float(v) / float(tree_total)
		tree_area = float(tree_total) / float(self.w * self.h)
		return tree_area, tree_probabilities


	def clear_tree(self, x, y, nearest_tree_table):
		if x >= 0 and x < self.w and y >= 0 and y < self.h and self.trees[x,y] != None:

			distance = 4

			for x2 in xrange(max(0,x-distance), min(self.w,x+distance+1)):
				for y2 in xrange(max(0,y-distance), min(self.h,y+distance+1)):

					for y_step in range(self.altitudes[x2,y2]+1, self.box.maxy):
						block = get_block(self.level, self.x+x2, y_step, self.y+y2)
						if (block in self.wood_blocks or block in self.leaf_blocks) and nearest_tree_table[x2,y2] == (x, y):
							set_block(self.level, (0,0), self.x+x2, y_step, self.y+y2)
							if get_block(self.level, self.x+x2, y_step+1, self.y+y2) in self.decorative_blocks:
								set_block(self.level, (0, 0), self.x+x2, y_step+1, self.y+y2)

			self.trees[x,y] = None

			self.clear_tree(x-1, y, nearest_tree_table)
			self.clear_tree(x+1, y, nearest_tree_table)
			self.clear_tree(x, y-1, nearest_tree_table)
			self.clear_tree(x, y+1, nearest_tree_table)
			self.clear_tree(x-1, y-1, nearest_tree_table)
			self.clear_tree(x-1, y+1, nearest_tree_table)
			self.clear_tree(x+1, y-1, nearest_tree_table)
			self.clear_tree(x+1, y+1, nearest_tree_table)


	def collect_positions(self):
		self.positions = set()
		for x in xrange(self.w):
			for y in xrange(self.h):
				# self.positions.add((x,y))
				if not self.blocks[x,y] in self.impassable_blocks:
					self.positions.add((x,y))


	def setup_grid(self, roads_can_cross_corners, impassable_blocks):
		grid = zeros((self.w, self.h)).astype(int)
		corners = zeros((self.w, self.h)).astype(int)

		# prevent roads from crossing water, lava and ice
		for x in xrange(1, self.w-1):
			for y in xrange(1, self.h-1):
				if self.blocks[x,y] in impassable_blocks:
					grid[x,y] = 1
					grid[x-1,y] = 1
					grid[x+1,y] = 1
					grid[x,y-1] = 1
					grid[x,y+1] = 1
					grid[x-1,y-1] = 1
					grid[x+1,y-1] = 1
					grid[x-1,y+1] = 1
					grid[x+1,y+1] = 1

		# prevent roads from climbing up slopes at corners
		for x in xrange(0, self.w-2):
			for y in xrange(0, self.h-2):
				x1, x2, y1, y2 = x, x+1, y, y+1
				corner = False
				if self.altitudes[x1,y1] != self.altitudes[x2,y1] and self.altitudes[x1,y1] != self.altitudes[x1,y2]:
					corner = True
				elif self.altitudes[x2,y1] != self.altitudes[x1,y1] and self.altitudes[x2,y1] != self.altitudes[x2,y2]:
					corner = True
				elif self.altitudes[x1,y2] != self.altitudes[x1,y1] and self.altitudes[x1,y2] != self.altitudes[x2,y2]:
					corner = True
				elif self.altitudes[x2,y2] != self.altitudes[x2,y1] and self.altitudes[x2,y2] != self.altitudes[x1,y2]:
					corner = True
				if corner:
					corners[x1,y1] = 1
					corners[x2,y1] = 1
					corners[x1,y2] = 1
					corners[x2,y2] = 1
					if not roads_can_cross_corners:
						grid[x1,y1] = 1
						grid[x2,y1] = 1
						grid[x1,y2] = 1
						grid[x2,y2] = 1

		self.grid = grid
		self.corners = corners


	def update_grid_for_structure(self, structure, road_distance):
		for x in xrange(max(0,structure.x1-road_distance), min(self.w,structure.x2+road_distance)):
			for y in xrange(max(0,structure.y1-road_distance), min(self.h,structure.y2+road_distance)):
				self.grid[x,y] = 1
		entry_path = structure.get_entry_path_default()
		for x, y in entry_path:
			self.grid[x,y] = 0


	def update_entire_grid(self, structures, road_distance):
		self.setup_grid(self.roads_can_cross_corners, self.impassable_blocks)
		for structure in structures:
			self.update_grid_for_structure(structure, road_distance)


	def fits_inside(self, x1, y1, x2, y2):
		if x1 >= 0 and x2 <= self.w and y1 >= 0 and y2 <= self.h:
			return True
		return False


	def get_distance(self, x1, y1, x2, y2):
		return sqrt( (x2 - x1)**2 + (y2 - y1)**2 )


	def box_collision(self, a_x1, a_y1, a_x2, a_y2, b_x1, b_y1, b_x2, b_y2):
		return not (b_x1 > a_x2 or b_x2 < a_x1 or b_y1 > a_y2 or b_y2 < a_y1)


	def box_distance(self, x1, y1, x1b, y1b, x2, y2, x2b, y2b):
		left = x2b < x1
		right = x1b < x2
		bottom = y2b < y1
		top = y1b < y2
		if top and left:
			return self.get_distance(x1, y1b, x2b, y2)
		elif left and bottom:
			return self.get_distance(x1, y1, x2b, y2b)
		elif bottom and right:
			return self.get_distance(x1b, y1, x2, y2b)
		elif right and top:
			return self.get_distance(x1b, y1b, x2, y2)
		elif left:
			return x1 - x2b
		elif right:
			return x2 - x1b
		elif bottom:
			return y1 - y2b
		elif top:
			return y2 - y1b
		else:
			return 0


	def get_altitudes(self, x1, y1, x2, y2):
		altitudes = set()
		for x in range(x1, x2):
			for y in range(y1, y2):
				altitudes.add(self.altitudes[x,y])
		return min(altitudes), max(altitudes)


	def get_edge_altitudes(self, x1, y1, x2, y2, margin):
		# fails if x1=x2 or y1=y2
		altitudes = set()
		for x in range(x1, x2):
			for y in range(y1, y1+margin):
				altitudes.add(self.altitudes[x,y])
			for y in range(y2-margin, y2):
				altitudes.add(self.altitudes[x,y])
		for y in range(y1, y2):
			for x in range(x1, x1+margin):
				altitudes.add(self.altitudes[x,y])
			for x in range(x2-margin, x2):
				altitudes.add(self.altitudes[x,y])

		return min(altitudes), max(altitudes)


	def altitude_difference(self, x1, y1, x2, y2):
		altitude_lowest, altitude_highest = self.get_altitudes(x1, y1, x2, y2)
		return altitude_highest - altitude_lowest


	def collides(self, x1, y1, x2, y2, collider_blocks):
		for x in range(x1, x2):
			for y in range(y1, y2):
				if self.blocks[x,y] in collider_blocks:
					return True
		return False


	def clear_space(self, x, y, z):
		for y_step in range(z, self.box.maxy):
			set_block(self.level, (0,0), self.x+x, y_step, self.y+y)


	def clear_space_relative_to_surface(self, x, y, z):
		for y_step in range(self.altitudes[x,y]+z, self.box.maxy):
			set_block(self.level, (0,0), self.x+x, y_step, self.y+y)


	def drop_blocks_to_level(self, x, y, z):
		if z >= self.altitudes[x,y]:
			return None
		else:
			top_blocks = []
			for y_step in range(self.altitudes[x,y], self.box.maxy):
				block = get_block_tuple(self.level, self.x+x, y_step, self.y+y)
				if block != (0, 0):
					top_blocks.append(block)
				else:
					break

			self.clear_space(x, y, z)

			for y_step in range(z, self.box.maxy):
				if top_blocks:
					block = top_blocks.pop(0)
					set_block(self.level, block, self.x+x, y_step, self.y+y)
				else:
					break


	def clear_surrounding_hills(self, x1, y1, x2, y2, area_margin, altitude, max_size):
		area_x1, area_y1, area_x2, area_y2 = max(0,x1-area_margin), max(0,y1-area_margin), min(self.w,x2+area_margin), min(self.h,y2+area_margin)

		max_difference = 1

		hill_points = set()
		for x in range(area_x1, area_x2):
			for y in range(area_y1, y1):
				if self.altitudes[x,y] > altitude and self.altitudes[x,y] <= altitude + max_difference:
					hill_points.add((x,y))
			for y in range(y2, area_y2):
				if self.altitudes[x,y] > altitude and self.altitudes[x,y] <= altitude + max_difference:
					hill_points.add((x,y))
		for y in range(area_y1, area_y2):
			for x in range(area_x1, x1):
				if self.altitudes[x,y] > altitude and self.altitudes[x,y] <= altitude + max_difference:
					hill_points.add((x,y))
			for x in range(x2, area_x2):
				if self.altitudes[x,y] > altitude and self.altitudes[x,y] <= altitude + max_difference:
					hill_points.add((x,y))

		altitudes_copy = copy(self.altitudes)

		while hill_points:
			x, y = hill_points.pop()
			if altitudes_copy[x,y] > altitude and altitudes_copy[x,y] <= altitude + max_difference:
				altitudes_current = copy(altitudes_copy)
				steps = restricted_flood_fill(altitudes_copy, self.w, self.h, (x,y), altitude, max_size)
				if steps == max_size:
					altitudes_copy = altitudes_current

		altitude_differences = 0
		for x in range(0, self.w):
			for y in range(0, self.h):
				if self.altitudes[x,y] != altitudes_copy[x,y]:
					altitude_differences += 1;
					self.drop_blocks_to_level(x, y, altitudes_copy[x,y])
					self.altitudes[x,y] = altitudes_copy[x,y]
		if altitude_differences > 0:
			print(" :Cleared up some hills (%i altitude differences)." % (altitude_differences))


	def place_fences(self, blocks_updated, reserved_materials, impassable_blocks, materials, fence_conversion, wood_source):

		# brace yourselves: horrible, horrible code ahead

		map = self
		fence_map = zeros((map.w, map.h)).astype(int)

		if wood_source in fence_conversion.keys():
			fence_block = fence_conversion[wood_source]
		else:
			fence_block = (85,0)

		for x in xrange(1, map.w-1):
			for y in xrange(1, map.h-1):
				if blocks_updated[x,y] not in reserved_materials and not blocks_updated[x,y] in impassable_blocks:

					near_road = False
					road_altitude = -999
					for position_d in [(-2,0,'e'), (0,-2,'w'), (0,2,'n'), (2,0,'s'), (-2,-2,'s'), (-2,2,'e'), (2,2,'n'), (2,-2,'w')]:
						if x+position_d[0] > 0 and y+position_d[1] > 0 and x+position_d[0] < map.w and y+position_d[1] < map.h and blocks_updated[x+position_d[0], y+position_d[1]] == materials['road'][0]:
							near_road = True
							road_altitude = map.altitudes[x+position_d[0], y+position_d[1]]
							fence_direction = position_d[2]
							break

					if near_road and road_altitude <= map.altitudes[x,y]:
						clear_space = True
						for x2 in xrange(max(0,x-1), min(map.w,x+2)):
							for y2 in xrange(max(0,y-1), min(map.h,y+2)):
								if blocks_updated[x2,y2] == materials['road'][0] or blocks_updated[x2,y2] in reserved_materials:
									clear_space = False
									break
							if not clear_space:
								break

						if clear_space:
							faces_away = True
							x_d, y_d = 0, 0

							if fence_direction == 'n':
								increment_x, increment_y = 0, -1
							elif fence_direction == 's':
								increment_x, increment_y = 0, 1
							elif fence_direction == 'e':
								increment_x, increment_y = 1, 0
							elif fence_direction == 'w':
								increment_x, increment_y = -1, 0

							for i in xrange(10):
								x_d += increment_x
								y_d += increment_y

								if x+x_d <= 0 or x+x_d >= map.w or y+y_d <= 0 or y+y_d >= map.h:
									faces_away = True
									break
								elif map.altitudes[x+x_d,y+y_d] <= map.altitudes[x,y] - 2:
									faces_away = True
									break
								elif map.blocks[x+x_d,y+y_d] in reserved_materials or map.blocks[x+x_d,y+y_d] == materials['road'][0]:
									faces_away = False
									break

							if faces_away:
								fence_map[x,y] = map.altitudes[x,y]


		for x in xrange(1, map.w-1):
			for y in xrange(1, map.h-1):
				if fence_map[x,y] != 0:

					acceptable = True
					alt = fence_map[x,y]

					if fence_map[x-1,y] == alt and fence_map[max(0,x-2),y] == alt:
						acceptable = True
						map.fill_block(x, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x-1, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(max(0,x-2), y, map.altitudes[x,y]+1, fence_block)

					elif fence_map[x+1,y] == alt and fence_map[min(map.w,x+2),y] == alt:
						acceptable = True
						map.fill_block(x, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x+1, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(min(map.w,x+2), y, map.altitudes[x,y]+1, fence_block)

					elif fence_map[x-1,y] == alt and fence_map[x+1,y] == alt:
						acceptable = True
						map.fill_block(x, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x-1, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x+1, y, map.altitudes[x,y]+1, fence_block)

					elif fence_map[x,y-1] == alt and fence_map[x,max(0,y-2)] == alt:
						acceptable = True
						map.fill_block(x, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x, y-1, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x, max(0,y-2), map.altitudes[x,y]+1, fence_block)

					elif fence_map[x,y+1] == alt and fence_map[x,min(map.h,y+2)] == alt:
						acceptable = True
						map.fill_block(x, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x, y+1, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x, min(map.h,y+2), map.altitudes[x,y]+1, fence_block)

					elif fence_map[x,y-1] == alt and fence_map[x,y+1] == alt:
						acceptable = True
						map.fill_block(x, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x, y-1, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x, y+1, map.altitudes[x,y]+1, fence_block)

					elif fence_map[x-1,y] == alt and fence_map[x,y-1] == alt:
						acceptable = True
						map.fill_block(x, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x-1, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x, y-1, map.altitudes[x,y]+1, fence_block)

					elif fence_map[x-1,y] == alt and fence_map[x,y+1] == alt:
						acceptable = True
						map.fill_block(x, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x-1, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x, y+1, map.altitudes[x,y]+1, fence_block)

					elif fence_map[x+1,y] == alt and fence_map[x,y-1] == alt:
						acceptable = True
						map.fill_block(x, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x+1, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x, y-1, map.altitudes[x,y]+1, fence_block)

					elif fence_map[x+1,y] == alt and fence_map[x,y+1] == alt:
						acceptable = True
						map.fill_block(x, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x+1, y, map.altitudes[x,y]+1, fence_block)
						map.fill_block(x, y+1, map.altitudes[x,y]+1, fence_block)


	def complete_path(self, points, road_material):
		for x, y in points:
			self.fill_block_relative_to_surface(x, y, 0, road_material)
			self.clear_space_relative_to_surface(x, y, 1)


	def fill_block_relative_to_surface(self, x, y, z, material):
		set_block(self.level, material, self.x+x, self.altitudes[x,y]+z, self.y+y)
		self.blocks[x,y] = material[0] # only if it's the same or higher than altitude?
		if material[0] == 0:
			self.positions.discard((x,y))


	def fill_block(self, x, y, z, material):
		set_block(self.level, material, self.x+x, z, self.y+y)
		if material[0] != 0:
			self.blocks[x,y] = material[0]
			self.positions.discard((x,y))


	def fill(self, x1, y1, z1, x2, y2, z2, material):
		for x in range(x1, x2):
			for y in range(y1, y2):
				for z in range(z1, z2):
					set_block(self.level, material, self.x+x, z, self.y+y)
					if material[0] != 0:
						self.blocks[x,y] = material[0]
						self.positions.discard((x,y))