import time
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from numpy import *
from random import randint, choice


class Structure:
	def __init__(self, map, structures, x1, y1, x2, y2, height, entry_distance, reserved_space, direction, cat, materials, modify_terrain, start_time):
		# cat - short for 'category' (house, plaza, farm...)

		self.cat = cat
		self.map = map
		self.modify_terrain = modify_terrain

		self.direction = direction
		self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

		self.height = height
		self.large = self.height > 6
		self.entry_distance = entry_distance
		self.reserved_space = reserved_space

		if self.cat == 'farm':
			self.entry_distance = 2
			self.reserved_space = 1

		self.materials = materials

		self.center_x, self.center_y = int(round((self.x2+self.x1)/2)), int(round((self.y2+self.y1)/2))
		self.door_x, self.door_y = self.center_x, self.center_y

		# self.structures = structures
		self.structures = structures + map.buffer

		self.has_distance_data = False

		if self.direction == 'w':
			self.door_x = self.x1
		elif self.direction == 'e':
			self.door_x = self.x2 - 1
		elif self.direction == 'n':
			self.door_y = self.y1
		elif self.direction == 's':
			self.door_y = self.y2 - 1

		exit_space_sides = 1
		exit_space_ahead = 2
		front_space = 3

		self.exit_x1, self.exit_y1, self.exit_x2, self.exit_y2 = self.get_exit_space(exit_space_sides, exit_space_ahead)
		self.front_x1, self.front_y1, self.front_x2, self.front_y2 = self.get_exit_space(exit_space_sides, front_space)
		self.outer_x1, self.outer_y1, self.outer_x2, self.outer_y2 = max(0,self.x1-self.reserved_space), max(0,self.y1-self.reserved_space), min(self.map.w,self.x2+self.reserved_space), min(self.map.h,self.y2+self.reserved_space)

		if not self.map.fits_inside(self.front_x1, self.front_y1, self.front_x2, self.front_y2):
			self.front_x1, self.front_y1 = self.exit_x1, self.exit_y1
			self.front_x2, self.front_y2 = self.exit_x2, self.exit_y2

		# self.altitude = self.map.altitudes[self.door_x, self.door_y]
		self.altitude = self.map.altitudes[max(0,min(self.map.w-1,self.door_x)), max(0,min(self.map.h-1,self.door_y))]

		self.other_entry_points = []
		if self.cat == "plaza":
			for point in [(self.center_x, self.y1), (self.center_x, self.y2-1), (self.x1, self.center_y), (self.x2-1, self.center_y)]:
				if point[0] != self.door_x or point[1] != self.door_y:
					self.other_entry_points.append(point)

		self.templates = self.get_templates()


	def get_templates(self):
		map = self.map
		entry_distance = self.entry_distance
		reserved_space = self.reserved_space
		templates = []

		padding = 1

		extent_neighbour = 8
		extent_plaza = 6
		extent_corner = 10
		margin_corner = 4


		if self.cat == 'plaza':

			template_west = (max(0,self.x1-entry_distance-reserved_space-extent_neighbour), self.y1+padding, max(0,self.x1-entry_distance-reserved_space), self.y2-padding, 'e', 'house')
			template_east = (min(map.w,self.x2+entry_distance+reserved_space), self.y1+padding, min(map.w,self.x2+entry_distance+reserved_space+extent_neighbour), self.y2-padding, 'w', 'house')
			template_north = (self.x1+padding, max(0,self.y1-entry_distance-reserved_space-extent_neighbour), self.x2-padding, max(0,self.y1-entry_distance-reserved_space), 's', 'house')
			template_south = (self.x1+padding, min(map.h,self.y2+entry_distance+reserved_space), self.x2-padding, min(map.h,self.y2+entry_distance+reserved_space+extent_neighbour), 'n', 'house')

			# to prioritize buildings near plazas (wells), requirements are added twice (could be handled with a score modifier instead)

			templates.append(template_west)
			templates.append(template_east)
			templates.append(template_north)
			templates.append(template_south)

			templates.append(template_west)
			templates.append(template_east)
			templates.append(template_north)
			templates.append(template_south)


		elif self.cat == 'house':

			if self.direction == 's':
				template_left_area = (max(0,self.x1-reserved_space-extent_neighbour), self.y1+padding, max(0,self.x1-reserved_space), self.y2-padding, 'sw', 'house')
				template_right_area = (min(map.w,self.x2+reserved_space), self.y1+padding, min(map.w,self.x2+reserved_space+extent_neighbour), self.y2-padding, 'se', 'house')
				templates.append(template_left_area)
				templates.append(template_right_area)

				if self.large:
					template_plaza = (self.x1+padding, min(map.h,self.y2+entry_distance+reserved_space), self.x2-padding, min(map.h,self.y2+entry_distance+reserved_space+extent_plaza), 'n', 'plaza')
					templates.append(template_plaza)

				else:
					template_ahead = (self.x1+padding, min(map.h,self.y2+entry_distance+reserved_space), self.x2-padding, min(map.h,self.y2+entry_distance+reserved_space+extent_neighbour), 'n', 'house')
					templates.append(template_ahead)

					template_corner_left = (max(0,self.x1-reserved_space-extent_corner), min(map.h,self.y2+entry_distance-margin_corner), max(0,self.x1-reserved_space), min(map.h,self.y2+entry_distance+margin_corner), 'e', 'house')
					template_corner_right = (min(map.w,self.x2+reserved_space), min(map.h,self.y2+entry_distance-margin_corner), min(map.w,self.x2+reserved_space+extent_corner), min(map.h,self.y2+entry_distance+margin_corner), 'w', 'house')
					templates.append(template_corner_left)
					templates.append(template_corner_right)


			elif self.direction == 'n':
				template_left_area = (max(0,self.x1-reserved_space-extent_neighbour), self.y1+padding, max(0,self.x1-reserved_space), self.y2-padding, 'nw', 'house')
				template_right_area = (min(map.w,self.x2+reserved_space), self.y1+padding, min(map.w,self.x2+reserved_space+extent_neighbour), self.y2-padding, 'ne', 'house')
				templates.append(template_left_area)
				templates.append(template_right_area)

				if self.large:
					template_plaza = (self.x1+padding, max(0,self.y1-entry_distance-reserved_space), self.x2-padding, max(0,self.y1-entry_distance-reserved_space-extent_plaza), 's', 'plaza')
					templates.append(template_plaza)

				else:
					template_ahead = (self.x1+padding, max(0,self.y1-entry_distance-reserved_space), self.x2-padding, max(0,self.y1-entry_distance-reserved_space-extent_neighbour), 's', 'house')
					templates.append(template_ahead)

					template_corner_left = (max(0,self.x1-reserved_space-extent_corner), max(0,self.y1-entry_distance-margin_corner), max(0,self.x1-reserved_space), max(0,self.y1-entry_distance+margin_corner), 'e', 'house')
					template_corner_right = (min(map.w,self.x2+reserved_space), max(0,self.y1-entry_distance-margin_corner), min(map.w,self.x2+reserved_space+extent_corner), max(0,self.y1-entry_distance+margin_corner), 'w', 'house')
					templates.append(template_corner_left)
					templates.append(template_corner_right)


			elif self.direction == 'w':
				template_left_area = (self.x1+padding, max(0,self.y1-reserved_space-extent_neighbour), self.x2-padding, max(0,self.y1-reserved_space), 'wn', 'house')
				template_right_area = (self.x1+padding, min(map.h,self.y2+reserved_space), self.x2-padding, min(map.h,self.y2+reserved_space+extent_neighbour), 'ws', 'house')
				templates.append(template_left_area)
				templates.append(template_right_area)

				if self.large:
					template_plaza = (max(0,self.x1-reserved_space-entry_distance-extent_plaza), self.y1+padding, max(0,self.x1-entry_distance-reserved_space), self.y2-padding, 'e', 'plaza')
					templates.append(template_plaza)

				else:
					template_ahead = (max(0,self.x1-entry_distance-reserved_space), self.y1+padding, max(0,self.x1-entry_distance-reserved_space-extent_neighbour), self.y2-padding, 'e', 'house')
					templates.append(template_ahead)

					template_corner_left = (max(0,self.x1-entry_distance-margin_corner), max(0,self.y1-reserved_space-extent_corner), max(0,self.x1-entry_distance+margin_corner), max(0,self.y1-reserved_space), 's', 'house')
					template_corner_right = (max(0,self.x1-entry_distance-margin_corner), min(map.h,self.y2+reserved_space), max(0,self.x1-entry_distance+margin_corner), min(map.h,self.y2+reserved_space+extent_corner), 'n', 'house')
					templates.append(template_corner_left)
					templates.append(template_corner_right)


			elif self.direction == 'e':
				template_left_area = (self.x1+padding, max(0,self.y1-reserved_space-extent_neighbour), self.x2-padding, max(0,self.y1-reserved_space), 'en', 'house')
				template_right_area = (self.x1+padding, min(map.h,self.y2+reserved_space), self.x2-padding, min(map.h,self.y2+reserved_space+extent_neighbour), 'es', 'house')
				templates.append(template_left_area)
				templates.append(template_right_area)

				if self.large:
					template_plaza = (min(map.w,self.x2+entry_distance+reserved_space), self.y1+padding, min(map.w,self.x2+entry_distance+reserved_space+extent_plaza), self.y2-padding, 'w', 'plaza')
					templates.append(template_plaza)

				else:
					template_ahead = (min(map.w,self.x2+entry_distance+reserved_space), self.y1+padding, min(map.w,self.x2+entry_distance+reserved_space+extent_neighbour), self.y2-padding, 'w', 'house')
					templates.append(template_ahead)

					template_corner_left = (min(map.w,self.x2+entry_distance-margin_corner), max(0,self.y1-reserved_space-extent_corner), min(map.w,self.x2+entry_distance+margin_corner), max(0,self.y1-reserved_space), 's', 'house')
					template_corner_right = (min(map.w,self.x2+entry_distance-margin_corner), min(map.h,self.y2+reserved_space), min(map.w,self.x2+entry_distance+margin_corner), min(map.h,self.y2+reserved_space+extent_corner), 'n', 'house')
					templates.append(template_corner_left)
					templates.append(template_corner_right)


		return templates


	def count_template_matches(self):
		matches = 0
		# can go over 1 if overlaps with multiple templates (this is intentional)

		for structure in self.structures:
			for template in structure.templates:
				x1, y1, x2, y2, directions, cat = template
				if cat == self.cat and self.direction in directions:

					# if house, the door must fit inside template
					if self.map.box_collision(x1, y1, x2, y2, self.x1, self.y1, self.x2, self.y2) and (self.cat != 'house' or self.map.box_collision(x1-1,y1-1,x2+1,y2+1, self.door_x, self.door_y, self.door_x+1, self.door_y+1)):

						intersection = float( max(0, min(x2, self.x2) - max(x1, self.x1)) * max(0, min(y2, self.y2) - max(y1, self.y1)) )
						overlap = intersection / float(((x2-x1)*(y2-y1)) + ((self.x2-self.x1)*(self.y2-self.y1)) - intersection)

						matches += overlap

		return matches


	def fits_inside(self):
		if self.map.fits_inside(self.x1, self.y1, self.x2, self.y2) and self.map.fits_inside(self.exit_x1, self.exit_y1, self.exit_x2, self.exit_y2):
			entry_point = self.get_entry_point()
			if self.map.fits_inside(entry_point[0], entry_point[1], entry_point[0]+1, entry_point[1]+1):
				return True
		return False


	def collides(self, x1, y1, x2, y2):
		collider_blocks = set([8, 9, 10, 11, 79, self.materials['wall'][0], self.materials['floor'][0], self.materials['plaza'][0]])
		return self.map.collides(x1, y1, x2, y2, collider_blocks)


	def collides_structures(self, x1, y1, x2, y2):
		for structure in self.structures:
			if self.map.box_collision(x1, y1, x2, y2, structure.x1, structure.y1, structure.x2, structure.y2):
				return True
		return False


	def collides_terrain_or_structures(self, x1, y1, x2, y2):
		return self.collides_structures(x1, y1, x2, y2) or self.collides(x1, y2, x2, y2)


	def collides_road(self, x1, y1, x2, y2):
		collider_blocks = set([self.materials['road'][0], self.materials['farm'][0]])
		return self.map.collides(x1, y1, x2, y2, collider_blocks)


	def get_entry_point(self):
		if self.direction == 's':
			return self.door_x, self.door_y + self.entry_distance
		elif self.direction == 'n':
			return self.door_x, self.door_y - self.entry_distance
		elif self.direction == 'e':
			return self.door_x + self.entry_distance, self.door_y
		elif self.direction == 'w':
			return self.door_x - self.entry_distance, self.door_y


	def get_other_entry_points(self):
		adjusted_entry_points = []

		for point in self.other_entry_points:
			if self.center_x == point[0] and self.center_y > point[1]:
				adjusted_entry_points.append((point[0], point[1] - self.entry_distance))
			elif self.center_x == point[0] and self.center_y < point[1]:
				adjusted_entry_points.append((point[0], point[1] +  self.entry_distance))
			elif self.center_y == point[1] and self.center_x > point[0]:
				adjusted_entry_points.append((point[0] -  self.entry_distance, point[1]))
			elif self.center_y == point[1] and self.center_x < point[0]:
				adjusted_entry_points.append((point[0] +  self.entry_distance, point[1]))

		return [point for point in adjusted_entry_points if self.map.fits_inside(point[0], point[1], point[0]+1, point[1]+1)]


	def get_entry_path_default(self):
		path = []
		if self.direction == 's':
			for y in xrange(self.door_y, self.door_y + self.entry_distance + 1):
				path.append((self.door_x, y))
		elif self.direction == 'n':
			for y in xrange(self.door_y, self.door_y - self.entry_distance - 1, -1):
				path.append((self.door_x, y))
		elif self.direction == 'e':
			for x in xrange(self.door_x, self.door_x + self.entry_distance + 1):
				path.append((x, self.door_y))
		elif self.direction == 'w':
			for x in xrange(self.door_x, self.door_x - self.entry_distance - 1, -1):
				path.append((x, self.door_y))
		return path


	def get_entry_path(self, entry_point):
		path = []
		if self.center_x == entry_point[0] and self.center_y > entry_point[1]:
			for y in xrange(0, self.entry_distance + 1):
				path.append((entry_point[0], entry_point[1] + y))
		elif self.center_x == entry_point[0] and self.center_y < entry_point[1]:
			for y in xrange(0, self.entry_distance + 1):
				path.append((entry_point[0], entry_point[1] - y))
		elif self.center_y == entry_point[1] and self.center_x > entry_point[0]:
			for x in xrange(0, self.entry_distance + 1):
				path.append((entry_point[0] + x, entry_point[1]))
		elif self.center_y == entry_point[1] and self.center_x < entry_point[0]:
			for x in xrange(0, self.entry_distance + 1):
				path.append((entry_point[0] - x, entry_point[1]))
		return path


	def update_distance_data(self):
		pointA = self.get_entry_point()

		pointB = self.get_entry_point()
		source = self
		shortest_point_distance = (self.map.w + self.map.h)

		for structure in self.structures:
			if structure != self and structure.cat != 'farm':
				structure_entry_points = structure.get_other_entry_points()
				structure_entry_points.append(structure.get_entry_point())

				for structure_point in structure_entry_points:
					topdown_distance = self.map.get_distance(pointA[0], pointA[1], structure_point[0], structure_point[1])
					altitude_difference = abs(self.map.altitudes[pointA[0],pointA[1]] - self.map.altitudes[structure_point[0],structure_point[1]])

					point_distance = topdown_distance * (1 + altitude_difference)

					if point_distance < shortest_point_distance:
						pointB = structure_point
						source = structure
						shortest_point_distance = point_distance

		self.has_distance_data = True
		self.distance_data = (shortest_point_distance, pointA, pointB, source)

		return self.distance_data


	def get_distance_of_farm(self):
		pointA = self.get_entry_point()
		shortest_point_distance = (self.map.w + self.map.h)

		for structure in self.structures:
			if structure != self and structure.cat != 'farm':
				structure_entry_points = structure.get_other_entry_points()
				structure_entry_points.append(structure.get_entry_point())

				for structure_point in structure_entry_points:
					topdown_distance = self.map.get_distance(pointA[0], pointA[1], structure_point[0], structure_point[1])
					altitude_difference = abs(self.map.altitudes[pointA[0],pointA[1]] - self.map.altitudes[structure_point[0],structure_point[1]])
					point_distance = topdown_distance * (1 + altitude_difference)

					if point_distance < shortest_point_distance:
						shortest_point_distance = point_distance

		return shortest_point_distance


	def get_exit_space(self, space_sides, space_ahead):
		if self.direction == 's':
			exit_x1 = self.door_x - space_sides
			exit_x2 = self.door_x + space_sides + 1
			exit_y1 = self.door_y
			exit_y2 = self.door_y + space_ahead + 1
		elif self.direction == 'n':
			exit_x1 = self.door_x - space_sides
			exit_x2 = self.door_x + space_sides + 1
			exit_y1 = self.door_y - space_ahead
			exit_y2 = self.door_y + 1
		elif self.direction == 'w':
			exit_x1 = self.door_x - space_ahead
			exit_x2 = self.door_x + 1
			exit_y1 = self.door_y - space_sides
			exit_y2 = self.door_y + space_sides + 1
		elif self.direction == 'e':
			exit_x1 = self.door_x
			exit_x2 = self.door_x + space_ahead + 1
			exit_y1 = self.door_y - space_sides
			exit_y2 = self.door_y + space_sides + 1

		return exit_x1, exit_y1, exit_x2, exit_y2


	def doesnt_block_entrance(self):
		for structure in self.structures:
			if structure != self:
				if self.map.box_collision(self.x1, self.y1, self.x2, self.y2, structure.front_x1, structure.front_y1, structure.front_x2, structure.front_y2):
					return False
		return True


	def can_exit_smoothly(self):
		return self.map.altitude_difference(self.exit_x1, self.exit_y1, self.exit_x2, self.exit_y2) == 0 and not self.collides(self.front_x1, self.front_y1, self.front_x2, self.front_y2)


	def acceptable(self):
		outer_x1, outer_y1, outer_x2, outer_y2 = self.outer_x1, self.outer_y1, self.outer_x2, self.outer_y2
		return self.fits_inside() and (self.cat == 'farm' or self.can_exit_smoothly()) and not self.collides_structures(outer_x1, outer_y1, outer_x2, outer_y2) and not self.collides(outer_x1, outer_y1, outer_x2, outer_y2) and not self.collides_road(max(0,self.x1-1), max(0,self.y1-1), min(self.map.w,self.x2+1), min(self.map.h,self.y2+1))


	def get_symmetries(self, space, categories):
		symmetry_front = False
		symmetry_left = False
		symmetry_right = False
		symmetry_back = False

		for structure in self.structures:
			if self != structure and (categories == None or structure.cat in categories):

				if self.y2 == structure.y2 and self.map.box_distance(self.x1, self.y1, self.x2, self.y2, structure.x1, structure.y1, structure.x2, structure.y2) <= space:
					symmetry_front = True
				if self.x1 == structure.x1 and self.map.box_distance(self.x1, self.y1, self.x2, self.y2, structure.x1, structure.y1, structure.x2, structure.y2) <= space:
					symmetry_left = True
				if self.x2 == structure.x2 and self.map.box_distance(self.x1, self.y1, self.x2, self.y2, structure.x1, structure.y1, structure.x2, structure.y2) <= space:
					symmetry_right = True
				if self.y1 == structure.y1 and self.map.box_distance(self.x1, self.y1, self.x2, self.y2, structure.x1, structure.y1, structure.x2, structure.y2) <= space:
					symmetry_back = True

			if symmetry_front and symmetry_left and symmetry_right and symmetry_back:
				break

		return (symmetry_front, symmetry_left, symmetry_right, symmetry_back)


	def count_symmetries(self, categories):
		space = max(1 + self.reserved_space, 1 + ((self.entry_distance * 2) -1))
		symmetries = self.get_symmetries(space, categories)

		symmetries_number = 0
		for symmetry in symmetries:
			if symmetry:
				symmetries_number += 1

		return symmetries_number


	def has_neighbour_side(self, cat, across_street, similar_directions, can_block):
		distance_nearest = self.reserved_space
		distance_across_road = self.entry_distance + 2

		if across_street:
			distance = max(distance_nearest, distance_across_road)
		else:
			distance = distance_nearest

		padding = 1
		if self.direction == "n" or self.direction == "s":
			neighbouring_space1 = (self.x1-distance-1, self.y1+padding, self.x1-1, self.y2-padding)
			neighbouring_space2 = (self.x2+1, self.y1+padding, self.x2+distance+1, self.y2-padding)
			# directions_similar = set([self.direction, "w", "e"])
			directions_similar = set(['n', 's', 'w', 'e'])
		elif self.direction == "w" or self.direction == "e":
			neighbouring_space1 = (self.x1+padding, self.y1-distance-1, self.x2-padding, self.y1-1)
			neighbouring_space2 = (self.x1+padding, self.y2+1, self.x2-padding, self.y2+distance+1)
			# directions_similar = set([self.direction, "n", "s"])
			directions_similar = set(['n', 's', 'w', 'e'])

		for structure in self.structures:
			if structure != self and (structure.cat == cat or cat == None) and (structure.direction == self.direction or (similar_directions and structure.direction in directions_similar)):

				wont_lock_neighbour_side1 = True
				wont_lock_neighbour_side2 = True

				if not can_block:
					structure_distance = max(distance_nearest, distance_across_road)

					if structure.direction == "n" or structure.direction == "s":
						structure_space1 = (structure.x1-structure_distance-1, structure.y1, structure.x1-1, structure.y2)
						structure_space2 = (structure.x2+1, structure.y1, structure.x2+structure_distance+1, structure.y2)
					elif structure.direction == "w" or structure.direction == "e":
						structure_space1 = (structure.x1, structure.y1-structure_distance-1, structure.x2, structure.y1-1)
						structure_space2 = (structure.x1, structure.y2+1, structure.x2, structure.y2+structure_distance+1)

					for other_structure in list(self.structures) + [self]:
						if other_structure != structure and other_structure.cat != 'plaza':
							if self.map.box_collision(other_structure.x1, other_structure.y1, other_structure.x2, other_structure.y2, structure_space1[0], structure_space1[1], structure_space1[2], structure_space1[3]):
								wont_lock_neighbour_side1 = False
								break
					for other_structure in list(self.structures) + [self]:
						if other_structure != structure and other_structure.cat != 'plaza':
							if self.map.box_collision(other_structure.x1, other_structure.y1, other_structure.x2, other_structure.y2, structure_space2[0], structure_space2[1], structure_space2[2], structure_space2[3]):
								wont_lock_neighbour_side2 = False
								break

				if wont_lock_neighbour_side1 or wont_lock_neighbour_side2:
					for neighbouring_space in (neighbouring_space1, neighbouring_space2):
						if self.map.box_collision(structure.x1, structure.y1, structure.x2, structure.y2, neighbouring_space[0], neighbouring_space[1], neighbouring_space[2], neighbouring_space[3]):
							return True

		return False


	def in_front_of_road(self):
		entry_point = self.get_entry_point()
		# if self.map.blocks[entry_point[0], entry_point[1]] == self.materials['road'][0]:
		if self.map.blocks[entry_point[0], entry_point[1]] == self.materials['road'][0] or self.map.blocks[entry_point[0], entry_point[1]] == self.materials['farm'][0]:
			return True
		return False


	def get_score(self, labels_instead_of_scores):
		outer_x1, outer_y1, outer_x2, outer_y2 = self.outer_x1, self.outer_y1, self.outer_x2, self.outer_y2
		altitude_lowest, altitude_highest = self.map.get_edge_altitudes(outer_x1, outer_y1, outer_x2, outer_y2, 2)
		altitude_difference = max(abs(self.altitude - altitude_highest), abs(self.altitude - altitude_lowest))

		# scores currently have no fixed value format (e.g. distance/altitude scores are negative integers, other scores may be floats, 0 or 1, etc.)

		scores = []

		if self.cat == 'house':
			scores = [
						("altitude difference",			-1 * altitude_difference ),
						("template matches",			self.count_template_matches() ),
					]

		elif self.cat == 'plaza':
			scores = [
						("altitude difference",			-1 * altitude_difference ),
						("template matches",			self.count_template_matches() ),
					]

		elif self.cat == 'farm':
			scores = [
						("altitude difference",			-1 * altitude_difference ),
						("has neighbour",				int(self.has_neighbour_side('house', False, True, True)) ),
						("in front of road",			int(self.in_front_of_road()) ),
						("distance",					int(-1 * self.get_distance_of_farm()) ),
						("symmetries",					self.count_symmetries(None) ),
						("has neighbour",				int(self.has_neighbour_side('farm', False, True, True)) ),
					]

		if labels_instead_of_scores:
			return [score[0] for score in scores]
		else:
			return [score[1] for score in scores]


	def generate(self):
		map = self.map

		if self.modify_terrain:
			# outer coordinates
			outer_x1, outer_y1, outer_x2, outer_y2 = self.outer_x1, self.outer_y1, self.outer_x2, self.outer_y2

			# clear space
			for x in range(outer_x1, outer_x2):
				for y in range(outer_y1, outer_y2):
					# map.clear_space(x, y, self.altitude+1)
					# map.altitudes[x,y] = min(map.altitudes[x,y], self.altitude)

					map.drop_blocks_to_level(x, y, self.altitude)
					map.altitudes[x,y] = min(map.altitudes[x,y], self.altitude)

			# clear surrounding hills
			area_margin = 2
			max_clear_area = 20
			map.clear_surrounding_hills(outer_x1, outer_y1, outer_x2, outer_y2, area_margin, self.altitude, max_clear_area)
			map.clear_surrounding_hills(self.exit_x1, self.exit_y2, self.exit_x2, self.exit_y2, area_margin, self.altitude, max_clear_area)

		# generate foundation
		if self.cat == 'house':
			map.fill(self.x1, self.y1, self.altitude, self.x2, self.y2, self.altitude+1, self.materials['floor'])
		elif self.cat == 'plaza':
			map.fill(self.x1, self.y1, self.altitude, self.x2, self.y2, self.altitude+1, self.materials['plaza'])
		elif self.cat == 'farm':
			map.fill(self.x1, self.y1, self.altitude, self.x2, self.y2, self.altitude+1, self.materials['farm'])

		# generate building
		if self.cat == 'house':
			map.fill(self.x1, self.y1, self.altitude+1, self.x2, self.y2, self.altitude+self.height, self.materials['wall'])
			map.fill(self.x1+1, self.y1+1, self.altitude+1, self.x2-1, self.y2-1, self.altitude+self.height-1, (0,0))

		# generate door
		if self.cat == 'house':
			map.fill_block(self.door_x, self.door_y, self.altitude+1, (0,0))
			map.fill_block(self.door_x, self.door_y, self.altitude+2, (0,0))


	def generate_details(self, tree_area, tree_probabilities, plank_conversion, log_conversion, wood_source):
		map = self.map

		# clear space

		# for x in range(self.x1, self.x2):
			# for y in range(self.y1, self.y2):
				# map.clear_space(x, y, self.altitude+1)

		if self.cat == 'plaza' or self.cat == 'farm':
			for x in range(self.x1, self.x2):
				for y in range(self.y1, self.y2):
					map.clear_space(x, y, self.altitude+1)


		# buildings
		if self.cat == 'house':

			if wood_source in log_conversion.keys() and wood_source in plank_conversion.keys():
				wood_beam = log_conversion[wood_source]
				wood_floor = plank_conversion[wood_source]
				wood_wall = plank_conversion[wood_source]
				wood_roof = plank_conversion[wood_source]
			else:
				wood_beam = (17, 0)
				wood_floor = (5, 0)
				wood_wall = (5, 0)
				wood_roof = (5, 0)

			wooden_building_chance = 50 + max(30, tree_area * 1000)
			wooden_building = not self.large and (randint(0, 100) <= wooden_building_chance)

			if wooden_building:
				floor_material = wood_floor
				wall_material = wood_wall
				wall_under_roof_material = wood_wall
				beam_material = wood_beam
				roof_material = wood_roof
				window_material = (20, 0)

			else:
				floor_material = wood_floor
				wall_material = (4, 0)
				wall_under_roof_material = (4, 0)
				beam_material = wood_beam
				roof_material = wood_roof
				window_material = (20, 0)


			# walls

			map.fill(self.x1, self.y1, self.altitude, self.x2, self.y2, self.altitude+1, floor_material)
			map.fill(self.x1, self.y1, self.altitude+1, self.x2, self.y2, self.altitude+self.height, wall_material)
			map.fill(self.x1+1, self.y1+1, self.altitude+1, self.x2-1, self.y2-1, self.altitude+self.height, (0,0))

			for y_step in xrange(self.altitude+1, self.altitude+self.height):
			# for y_step in xrange(self.altitude, self.altitude+self.height):
				map.fill_block(self.x1, self.y1, y_step, beam_material)
				map.fill_block(self.x1, self.y2-1, y_step, beam_material)
				map.fill_block(self.x2-1, self.y1, y_step, beam_material)
				map.fill_block(self.x2-1, self.y2-1, y_step, beam_material)


			# beam underneath rooftops

			for x in xrange(self.x1, self.x2):
				map.fill(x, self.y1, self.altitude+self.height, x+1, self.y1+1, self.altitude+self.height+1, beam_material)
				map.fill(x, self.y2-1, self.altitude+self.height, x+1, self.y2, self.altitude+self.height+1, beam_material)

			for y in xrange(self.y1, self.y2):
				map.fill(self.x1, y, self.altitude+self.height, self.x1+1, y+1, self.altitude+self.height+1, beam_material)
				map.fill(self.x2-1, y, self.altitude+self.height, self.x2, y+1, self.altitude+self.height+1, beam_material)


			# rooftops (make sure it doesn't cross box ceiling?)

			if self.direction == 'e' or self.direction == 'w':
				i = 0
				for x in xrange(self.x1-1, self.center_x):
					if x >= 0:
						map.fill(x, max(0,self.y1-1), self.altitude+self.height+i, x+1, min(map.h,self.y2+1), self.altitude+self.height+i+1, roof_material)
						map.fill(x, max(0,self.y1), self.altitude+self.height+1, x+1, min(map.h,self.y2), self.altitude+self.height+i, wall_under_roof_material)
					i += 1
				i = 0
				for x in xrange(self.x2, self.center_x-1, -1):
					if x < map.w:
						map.fill(x, max(0,self.y1-1), self.altitude+self.height+i, x+1, min(map.h,self.y2+1), self.altitude+self.height+i+1, roof_material)
						map.fill(x, max(0,self.y1), self.altitude+self.height+1, x+1, min(map.h,self.y2), self.altitude+self.height+i, wall_under_roof_material)
					i += 1

			elif self.direction == 'n' or self.direction == 's':
				i = 0
				for y in xrange(self.y1-1, self.center_y):
					if y >= 0:
						map.fill(max(0,self.x1-1), y, self.altitude+self.height+i, min(map.w,self.x2+1), y+1, self.altitude+self.height+i+1, roof_material)
						map.fill(max(0,self.x1), y, self.altitude+self.height+1, min(map.w,self.x2), y+1, self.altitude+self.height+i, wall_under_roof_material)
					i += 1
				i = 0
				for y in xrange(self.y2, self.center_y-1, -1):
					if y < map.h:
						map.fill(max(0,self.x1-1), y, self.altitude+self.height+i, min(map.w,self.x2+1), y+1, self.altitude+self.height+i+1, roof_material)
						map.fill(max(0,self.x1), y, self.altitude+self.height+1, min(map.w,self.x2), y+1, self.altitude+self.height+i, wall_under_roof_material)
					i += 1


			# door opening

			map.fill_block(self.door_x, self.door_y, self.altitude+1, (0,0))
			map.fill_block(self.door_x, self.door_y, self.altitude+2, (0,0))


			# door frame and torches

			map.fill_block(self.door_x, self.door_y, self.altitude+3, beam_material)

			if  self.direction == 'n':
				for y_step in xrange(self.altitude+1, self.altitude+4):
					map.fill_block(self.door_x+1, self.door_y, y_step, beam_material)
					map.fill_block(self.door_x-1, self.door_y, y_step, beam_material)

				map.fill_block(self.door_x+1, self.door_y-1, self.altitude+2, (50,4))
				map.fill_block(self.door_x-1, self.door_y-1, self.altitude+2, (50,4))

			elif self.direction == 's':
				for y_step in xrange(self.altitude+1, self.altitude+4):
					map.fill_block(self.door_x+1, self.door_y, y_step, beam_material)
					map.fill_block(self.door_x-1, self.door_y, y_step, beam_material)

				map.fill_block(self.door_x+1, self.door_y+1, self.altitude+2, (50,3))
				map.fill_block(self.door_x-1, self.door_y+1, self.altitude+2, (50,3))

			elif self.direction == 'e':
				for y_step in xrange(self.altitude+1, self.altitude+4):
					map.fill_block(self.door_x, self.door_y-1, y_step, beam_material)
					map.fill_block(self.door_x, self.door_y+1, y_step, beam_material)

				map.fill_block(self.door_x+1, self.door_y-1, self.altitude+2, (50,1))
				map.fill_block(self.door_x+1, self.door_y+1, self.altitude+2, (50,1))

			elif self.direction == 'w':
				for y_step in xrange(self.altitude+1, self.altitude+4):
					map.fill_block(self.door_x, self.door_y-1, y_step, beam_material)
					map.fill_block(self.door_x, self.door_y+1, y_step, beam_material)

				map.fill_block(self.door_x-1, self.door_y-1, self.altitude+2, (50,2))
				map.fill_block(self.door_x-1, self.door_y+1, self.altitude+2, (50,2))


			# torches on sides of buildings (including torches placed on wooden beams... this is probably against OSHA)
			# (make sure they don't extend beyond map/box boundaries!)

			if self.x1-1 >= 0:
				map.fill_block(self.x1-1, self.y1, self.altitude+4, (50,2))
			if self.x1-1 >= 0 and self.y2-1 >= 0:
				map.fill_block(self.x1-1, self.y2-1, self.altitude+4, (50,2))

			if self.x2 < map.w:
				map.fill_block(self.x2, self.y1, self.altitude+4, (50,1))
			if self.x2 < map.w and self.y2-1 < map.h:
				map.fill_block(self.x2, self.y2-1, self.altitude+4, (50,1))

			if self.y1-1 >= 0:
				map.fill_block(self.x1, self.y1-1, self.altitude+4, (50,4))
			if self.y1-1 >= 0 and self.x2-1 < map.w:
				map.fill_block(self.x2-1, self.y1-1, self.altitude+4, (50,4))

			if self.y2 < map.h:
				map.fill_block(self.x1, self.y2, self.altitude+4, (50,3))
			if self.y2 < map.h and self.x2-1 < map.w:
				map.fill_block(self.x2-1, self.y2, self.altitude+4, (50,3))


			# windows (assuming building w/h are odd)
			# prevent windows from being generated if there are blocks outside?

			windows = []
			window_padding = 1

			for i, x in enumerate(range(self.center_x+3, self.x2-2)):
				if i % (1+window_padding) == 0:
					if (x > 0 and x < map.w):
						windows.append((x, self.y2-1))
						windows.append((x, self.y1))

			for i, x in enumerate(range(self.center_x-3, self.x1+1, -1)):
				if i % (1+window_padding) == 0:
					if (x > 0 and x < map.w):
						windows.append((x, self.y2-1))
						windows.append((x, self.y1))

			for i, y in enumerate(range(self.center_y+3, self.y2-2)):
				if i % (1+window_padding) == 0:
					if (y > 0 and y < map.h):
						windows.append((self.x2-1,y))
						windows.append((self.x1,y))

			for i, y in enumerate(range(self.center_y-3, self.y1+1, -1)):
				if i % (1+window_padding) == 0:
					if (y > 0 and y < map.h):
						windows.append((self.x2-1,y))
						windows.append((self.x1,y))


			if self.direction != 'w':
				windows.append((self.x1, self.center_y))
			if self.direction != 'e':
				windows.append((self.x2-1, self.center_y))
			if self.direction != 'n':
				windows.append((self.center_x, self.y1))
			if self.direction != 's':
				windows.append((self.center_x, self.y2-1))

			for x, y in windows:
				window_blocked = False
				for x2 in xrange(max(0,x-1), min(map.w,x+1)):
					for y2 in xrange(max(0,y-1), min(map.h,y+1)):
						if map.altitudes[x2,y2] > self.altitude:
							window_blocked = True

				if not window_blocked:
					# for y_step in xrange(self.altitude+1, self.altitude+self.height):
						# map.fill_block(x, y, y_step, beam_material)

					map.fill_block(x, y, self.altitude+2, window_material)
					map.fill_block(x, y, self.altitude+3, window_material)


			# support for uneven terrain
			for x, y in [(self.x1+1,self.y1+1), (self.x1+1,self.y2-2), (self.x2-2,self.y1+1), (self.x2-2,self.y2-2)]:
				for y_step in xrange(map.altitudes[x,y], self.altitude):
					# map.fill_block(x, y, y_step, floor_material)
					map.fill_block(x, y, y_step, beam_material)


		# generate well
		well_xr = 2
		well_yr = 2
		well_x1, well_x2, well_y1, well_y2 = self.center_x-well_xr, self.center_x+well_xr+1, self.center_y-well_yr, self.center_y+well_yr+1

		if self.cat == 'plaza':
			map.fill(well_x1, well_y1, self.altitude+1, well_x2, well_y2, self.altitude+2, (98, 1))
			map.fill(well_x1+1, well_y1+1, self.altitude+1, well_x2-1, well_y2-1, self.altitude+2, (8, 0))

			# support for uneven terrain
			for x in xrange(self.x1, self.x2):
				for y in xrange(self.y1, self.y2):
					for y_step in xrange(map.altitudes[x,y], self.altitude+1):
						map.fill_block(x, y, y_step, self.materials['plaza'])


		if self.cat == 'farm':

			if wood_source in log_conversion.keys():
				wood_beam = log_conversion[wood_source]
			else:
				wood_beam = (17, 0)

			crops_block = choice([(59, 7), (59, 7), (141,7), (142,7)])

			map.fill(self.x1, self.y1, self.altitude+1, self.x2, self.y2, self.altitude+2, wood_beam)
			map.fill(self.x1+1, self.y1+1, self.altitude+1, self.x2-1, self.y2-1, self.altitude+2, self.materials['farm'])
			map.fill(self.x1+1, self.y1+1, self.altitude+2, self.x2-1, self.y2-1, self.altitude+3, crops_block)

			if self.direction == 'n' or self.direction == 's':
				for x in xrange(self.x1+1, self.x2-1):
					if x % 3 == 0:
						map.fill(x, self.y1+1, self.altitude+1, x+1, self.y2-1, self.altitude+2, (8, 0))
						map.fill(x, self.y1+1, self.altitude+2, x+1, self.y2-1, self.altitude+3, (0, 0))

			if self.direction == 'e' or self.direction == 'w':
				for y in xrange(self.y1+1, self.y2-1):
					if y % 3 == 0:
						map.fill(self.x1+1, y, self.altitude+1, self.x2-1, y+1, self.altitude+2, (8, 0))
						map.fill(self.x1+1, y, self.altitude+2, self.x2-1, y+1, self.altitude+3, (0, 0))

			# support for uneven terrain
			for x in xrange(self.x1, self.x2):
				for y in xrange(self.y1, self.y2):
					for y_step in xrange(map.altitudes[x,y], self.altitude+1):
						map.fill_block(x, y, y_step, wood_beam)
