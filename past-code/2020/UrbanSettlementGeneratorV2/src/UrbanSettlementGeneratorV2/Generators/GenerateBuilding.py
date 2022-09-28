import random
import math
import RNG
import logging
from pymclevel import alphaMaterials, BoundingBox
import utilityFunctions as utilityFunctions
import BlocksInfo as BlocksInfo
from GenerateObject import *
from GenerateCarpet import generateCarpet
from GenerateBalcony import generateBalcony

def generateBuilding(matrix, h_min, h_max, x_min, x_max, z_min, z_max, usable_wood, biome):

	building = utilityFunctions.dotdict()
	building.type = "building"

	building.area = utilityFunctions.dotdict({"y_min": h_min, "y_max": h_max, "x_min": x_min, "x_max": x_max, "z_min": z_min, "z_max": z_max})

	(h_min, h_max, x_min, x_max, z_min, z_max) = getBuildingAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max)
	building.constructionArea = (h_min, h_max, x_min, x_max, z_min, z_max)

	logging.info("Generating building at area {}".format(building.area))
	logging.info("Construction area {}".format(building.constructionArea))
	utilityFunctions.cleanProperty2(matrix, building.area.y_min + 1, building.area.y_max, x_min - 1, x_max + 1, z_min - 3 if z_min - 3 > building.area.z_min else building.area.z_min, z_max + 1)

	picked_wood = utilityFunctions.selectRandomWood(usable_wood)
	wall = (159, random.randint(0,15))
	ceiling = wall
	floor = wall
	pavement_block = BlocksInfo.getPavmentId(biome)
	slab = BlocksInfo.getSlabId(biome, picked_wood, "Upper")
	stairs = BlocksInfo.getStairsId(biome, picked_wood)
	fence = BlocksInfo.getFenceId(biome, picked_wood)
	structureBloc = BlocksInfo.getStructureBlockId(biome, picked_wood)

	floor_size = 8
	max_height = h_max-h_min
	if max_height > 32:
		h_max = h_min+random.randint(32, 80 if max_height > 80 else max_height)

	while (h_max-h_min) % floor_size != 0:
		h_max -= 1

	building.orientation = getOrientation()

	if building.orientation == "S":
		door_x = RNG.randint(x_min+1, x_max-1)
		door_z = z_max
		utilityFunctions.cleanProperty2(matrix, h_min + 1, h_max, door_x - 1, door_x + 1, z_max + 1, building.area.z_max - 1)
		generateBuildingWalls(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall)
		generateFloorsDivision(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall)
		generateDoor(matrix, h_min+1, door_x, door_z, (64,9), (64,3))
		building.entranceLot = (h_min+1, door_x, building.area.z_max)
		for z in range(door_z+1, building.area.z_max):
			matrix.setValue(h_min,door_x,z, pavement_block)
			matrix.setValue(h_min,door_x-1,z, pavement_block)
			matrix.setValue(h_min,door_x+1,z, pavement_block)
		# determine which floor have two apartment instead of one
		double_apartment_floor = pickDoubleapartmentFloor(h_min, h_max, floor_size)
		# apartment windows
		generateBuildingWindows_AlongZ(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, double_apartment_floor)
		# corridor windows
		generateBuildingWindows_AlongZ(matrix, h_min, h_max, floor_size, x_min, x_max, z_max, [])
		generateCorridorInterior(matrix, h_min, h_max, floor_size, x_min, x_max, z_max-6, z_max, fence)
		generateFloorPlan(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall, double_apartment_floor)

		generateStairs(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall)
		generateRoof(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, biome, usable_wood, wall, stairs)
		generateApartmentInterior(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max-6, double_apartment_floor, usable_wood, biome, fence)
		generateBalconySouth(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, building.area.z_min, building.orientation, double_apartment_floor, wall, slab, stairs, fence, structureBloc)

		inhabitants = RNG.randint(1, 2) * (h_max / floor_size) + len(double_apartment_floor)
	return (building, inhabitants)

def getBuildingAreaInsideLot(h_min, h_max, x_min, x_max, z_min, z_max):
	building_size_x = random.randint(15, 18)
	if x_max-x_min > building_size_x:
		x_mid = x_min + (x_max-x_min)/2
		x_min = x_mid - building_size_x/2
		x_max = x_mid + building_size_x/2

	building_size_z = random.randint(15, 18)
	if z_max-z_min > building_size_z:
		z_mid = z_min + (z_max-z_min)/2
		z_min = z_mid - building_size_z/2
		z_max = z_mid + building_size_z/2

	return (h_min, h_max, x_min, x_max, z_min, z_max)

def pickDoubleapartmentFloor(h_min, h_max, floor_size):
	floor_number = (h_max - h_min) / floor_size
	picked_number = random.randint(0, floor_number - 1)
	double_apartment_floor = []
	floors = []
	for i in range(1, floor_number) :
		floors.append(i)
	#logging.info("################")
	#logging.info("picking {} floors out of {}".format(picked_number, floor_number))
	while picked_number > 0 :
		picked_floor = floors[random.randint(0, len(floors)-1)]
		double_apartment_floor.append(picked_floor * floor_size + h_min)
		floors.remove(picked_floor)
		picked_number -= 1

	return double_apartment_floor

def generateStairs(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall):
	cur_floor = h_min
	floor = 0
	while cur_floor < h_max:
		step = cur_floor+floor_size-1
		if floor % 2 == 0:
			x = x_max-2
			z = z_max-2
			for x1 in range(x, x-3, -1):
				#removes the floor blocks
				matrix.setValue(step+1, x1, z, (0, 0))
				matrix.setValue(step+1, x1, z-1, (0, 0))
				#removes the carpet blocks
				matrix.setValue(step+2, x1, z, (0, 0))
				matrix.setValue(step+2, x1, z-1, (0, 0))

			while step > cur_floor:
				matrix.setValue(step, x, z, (109, 0))
				matrix.setValue(step, x, z-1, (109, 0))
				for h in range(cur_floor+1, step):
					matrix.setValue(h, x, z, (98, 0))
					matrix.setValue(h, x, z-1, (98, 0))

				step -= 1
				x -= 1
		if floor % 2 == 1:
			x = x_min+2
			z = z_max-2
			for x1 in range(x, x+3):
				#removes the floor blocks
				matrix.setValue(step+1, x1, z, (0, 0))
				matrix.setValue(step+1, x1, z-1, (0, 0))
				#removes the carpet blocks
				matrix.setValue(step+2, x1, z, (0, 0))
				matrix.setValue(step+2, x1, z-1, (0, 0))
			while step > cur_floor:
				matrix.setValue(step, x, z, (109, 1))
				matrix.setValue(step, x, z-1, (109, 1))
				for h in range(cur_floor+1, step):
					matrix.setValue(h, x, z, (98, 0))
					matrix.setValue(h, x, z-1, (98, 0))
				step -= 1
				x += 1

		floor += 1
		cur_floor += floor_size

def generateRoof(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, biome, usable_wood, wall, stairs):
	floor = (h_max - h_min) / floor_size
	for x in range(x_min, x_max + 1) :
		for z in range(z_min, z_max + 1):
			if x == x_min or x == x_max or z == z_max or z == z_min :
				matrix.setValue(h_max + 1, x, z, BlocksInfo.IRON_BAR_ID)
	generateStreetLight(matrix, h_max, x_min + 1, z_min + 1)
	generateStreetLight(matrix, h_max, x_max - 1, z_min + 1)
	local_size = 5
	z_min_local = z_max - (local_size - 1)
	if floor % 2 == 0 :
		x_max_local = x_min + (local_size - 1)
		generateStreetLight(matrix, h_max, x_max - 1, z_max - 1)
		generateBuildingWalls(matrix, h_max + 1, h_max + local_size, floor_size, x_min, x_max_local, z_min_local, z_max, wall)
		generateFloorsDivision(matrix, h_max + local_size, h_max + local_size, local_size, x_min, x_max_local, z_min_local, z_max, wall)
		generateDoor(matrix, h_max + 1, x_min + 1, z_min_local, (197,9), (197,1))
		generateDoor(matrix, h_max + 1, x_max_local, z_max -1, (197,8), (197,2))
		generateAntenna(matrix, h_max + local_size, x_max_local - (x_max_local - x_min) / 2, z_max - (z_max - z_min_local) / 2)
		generateLantern(matrix,  h_max + 2, x_max_local - 1, z_min_local, "S")
		generateLantern(matrix, h_max + 2, x_max_local, z_min_local + 1, "W")
		fillWithTable(matrix, h_max, x_min + 2, x_max_local, z_min + 3, z_min_local - 3, stairs)
		fillWithGarden(matrix, h_max, x_max_local + 2, x_max - 3, z_min + 3, z_max - 3, biome, usable_wood)
	else :
		x_min_local = x_max - (local_size - 1)
		generateStreetLight(matrix, h_max, x_min + 1, z_max - 1)
		generateBuildingWalls(matrix, h_max + 1, h_max + local_size, floor_size, x_min_local, x_max, z_min_local, z_max, wall)
		generateFloorsDivision(matrix, h_max + local_size, h_max + local_size, local_size, x_min_local, x_max, z_min_local, z_max, wall)
		generateDoor(matrix, h_max + 1, x_max - 1, z_min_local, (197,9), (197,1))
		generateDoor(matrix, h_max + 1, x_min_local, z_max - 1, (197,8), (197,0))
		generateAntenna(matrix, h_max + local_size, x_max - (x_max - x_min_local) / 2, z_max - (z_max - z_min_local) / 2)
		generateLantern(matrix,  h_max + 2, x_min_local + 1, z_min_local, "S")
		generateLantern(matrix, h_max + 2, x_min_local, z_min_local + 1, "E")
		fillWithTable(matrix, h_max, x_min_local, x_max - 2, z_min + 3, z_min_local - 3, stairs)
		fillWithGarden(matrix, h_max, x_min + 3, x_min_local - 2, z_min + 3, z_max - 3, biome, usable_wood)

def fillWithTable(matrix, h, x_min, x_max, z_min, z_max, stairs_id):
	for x in range(x_min, x_max + 1, 2):
		for z in range(z_max - 1, z_min - 1, -4):
			if z - 1 >= z_min :
				generateCentralTableSouth(matrix, h, x, z, stairs_id[0])

def fillWithGarden(matrix, h, x_min, x_max, z_min, z_max, biome, usable_wood):
	flowers_id = BlocksInfo.getFlowerId(biome)
	flower_ground_id = BlocksInfo.getPlantGroundId(biome)
	bush_id = BlocksInfo.getBushId(biome, utilityFunctions.selectRandomWood(usable_wood))
	for x in range(x_min, x_max + 1, 5):
		for z in range(z_max, z_min + 1, -5):
			if z - 5 >= z_min and x + 5 <= x_max:
				generateBushCorner(matrix, h, x, z, 0, bush_id)
				generateBushCorner(matrix, h, x, z - 5, 1, bush_id)
				generateBushCorner(matrix, h, x + 5, z - 5, 2, bush_id)
				generateBushCorner(matrix, h, x + 5, z, 3, bush_id)
				generateFlowerTray(matrix, h, x + 2, z - 2, flowers_id, flower_ground_id)

def generateFloorPlan(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall, double_apartment_floor):
	cur_floor = h_min
	z_wall = z_max-6

	while cur_floor < h_max:
		if cur_floor == h_min :
			x_mid = x_max - (x_max - x_min) / 2
			for h in range(cur_floor, cur_floor+floor_size):
				# generating separating wall between the entrance and the apartment
				for z in range(z_min+1, z_wall):
					matrix.setValue(h, x_mid, z, wall)
				# generating front wall of the apartment
				for x in range(x_mid, x_max):
					matrix.setValue(h, x, z_wall, wall)
			bonus = 1 if (x_mid - x_min) / 2 < 4 else 0
			generateDoor(matrix, cur_floor+1, x_mid + (x_mid - x_min) / 2 + bonus, z_wall, (197,8), (197,3))

		else :
			# generating separating wall between hall and apartments
			for h in range(cur_floor, cur_floor+floor_size):
				for x in range(x_min, x_max):
					matrix.setValue(h, x, z_wall, wall)
			if cur_floor in double_apartment_floor :
				# generating separating wall between the two apartments
				x_mid = x_max - (x_max - x_min) / 2
				for h in range(cur_floor, cur_floor+floor_size):
					for z in range(z_min+1, z_wall):
						matrix.setValue(h, x_mid, z, wall)
				# generating door to both apartment
				bonus = 1 if (x_mid - x_min) / 2 < 4 else 0
				generateDoor(matrix, cur_floor+1, x_mid + (x_mid - x_min) / 2 + bonus, z_wall, (197,8), (197,3))
				generateDoor(matrix, cur_floor+1, x_mid - (x_mid - x_min) / 2, z_wall, (197,9), (197,3))
			else :
				# generating door to the apartment
				x_door = x_max - ((x_max-x_min)/2)
				generateDoor(matrix, cur_floor+1, x_door, z_wall, (197,9), (197,3))

		cur_floor += floor_size

def generateApartmentInterior(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, double_apartment_floor, usable_wood, biome, fence_id):
	cur_floor = h_min
	floor = 0
	x_mid = x_max - int((x_max - x_min)/2)
	z_mid = z_max - int((z_max - z_min)/2)

	while cur_floor < h_max:
		cur_floor_ceiling = cur_floor+floor_size
		if cur_floor == h_min :
			#hall
			generateFurnitureHall(matrix, cur_floor, floor_size, x_min, x_mid, z_min, z_max, usable_wood, biome, fence_id)
			#apartment on the left side of the floor
			picked_wood = utilityFunctions.selectRandomWood(usable_wood)
			generateFurnitureSmallApartment(matrix, cur_floor, floor_size, x_mid, x_max, z_min, z_max, 2, fence_id, biome, picked_wood)
		elif cur_floor in double_apartment_floor :
			#first apartment
			picked_wood = utilityFunctions.selectRandomWood(usable_wood)
			generateFurnitureSmallApartment(matrix, cur_floor, floor_size, x_min, x_mid, z_min, z_max, 1, fence_id, biome, picked_wood)
			#second apartment
			picked_wood = utilityFunctions.selectRandomWood(usable_wood)
			generateFurnitureSmallApartment(matrix, cur_floor, floor_size, x_mid, x_max, z_min, z_max, 2, fence_id, biome, picked_wood)
		else :
			picked_wood = utilityFunctions.selectRandomWood(usable_wood)
			stairs_id = BlocksInfo.getStairsId(biome, picked_wood)[0]
			generateCarpet(matrix.matrix, cur_floor+1, x_min+1, x_max, z_min+1, z_max)
			generateBed(matrix, cur_floor, x_max, z_min)
			generateCentralTable(matrix, cur_floor, x_mid, z_mid, stairs_id)
			generateBookshelf(matrix, cur_floor, x_max, z_max)
			generateCouch(matrix, cur_floor, x_min, z_max, stairs_id)

			x_mid = x_min + (x_max-x_min)/2
			z_mid = z_min + (z_max-z_min)/2
			generateChandelier(matrix, cur_floor_ceiling, x_mid-5, z_mid, fence_id, 2)
			generateChandelier(matrix, cur_floor_ceiling, x_mid+5, z_mid, fence_id, 2)

		cur_floor += floor_size

def generateFurnitureSmallApartment(matrix, h, floor_size, x_min, x_max, z_min, z_max, position, fence_id, biome, picked_wood):
	x_mid = x_max - (x_max - x_min) / 2
	z_mid = z_max - (z_max - z_min) / 2
	bonus = -1 if position == 2 and (x_max - x_min % 2) == 0 else 0
	generateCarpet(matrix.matrix, h + 1, x_min + 1, x_max, z_min + 1, z_max)
	generateChandelier(matrix, h + floor_size, x_mid + bonus, z_mid, fence_id, 2)
	generateCouch(matrix, h, x_min, z_max, BlocksInfo.getStairsId(biome, picked_wood)[0])
	generateBedSouth(matrix, h, x_min + 1 if position == 1 else x_max - 1, z_min + 1)
	generateCentralTableSouth(matrix, h, x_mid + bonus, z_mid, BlocksInfo.getStairsId(biome, picked_wood)[0])
	generateBookshelfEast(matrix, h, x_max, z_max)

def generateFurnitureHall(matrix, h_min, floor_size, x_min, x_max, z_min, z_max, usable_wood, biome, fence_id):
	grounds = [(47, 0), (45, 0)]
	x_mid = x_max - (x_max - x_min) / 2
	z_mid = z_max - (z_max - z_min) / 2
	plant_ground_id = BlocksInfo.getPlantGroundId(biome)
	ground_id = grounds[random.randint(0, len(grounds) - 1)]
	plant_id = BlocksInfo.getPlantsId(biome, utilityFunctions.selectRandomWood(usable_wood))
	generateCarpet(matrix.matrix, h_min + 1, x_min + 1, x_max, z_min + 1, z_max + 1)
	generateChandelier(matrix, h_min + floor_size, x_mid, z_mid, fence_id, 2)
	generatePlant(matrix, h_min, x_min + 2, z_max - 1, plant_id, plant_ground_id)
	generatePlant(matrix, h_min, x_max - 2, z_max - 1, plant_id, plant_ground_id)
	next_blank = 2
	for z in range(z_max - 3, z_min + 1, -1) :
		if next_blank == 0 :
			next_blank = 3
			generatePotWithPlant(matrix, h_min, x_mid, z, (47, 0), ground_id)
			if (x_max - x_min - 1) % 2 == 0 :
				generatePotWithPlant(matrix, h_min, x_mid - 1, z, (47, 0), ground_id)
		else :
			next_blank -= 1
			generateMailbox(matrix, h_min, x_min + 1, z, "E")
			generateMailbox(matrix, h_min, x_max - 1, z, "W")


def generateBalconySouth(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, area_z_min, orientation, double_apartment_floor, wall, slab_id, stairs_id, fence_id, structureBloc_id):
	cur_floor = h_min + floor_size
	while cur_floor < h_max:
		x_mid = x_max - (x_max - x_min) / 2
		if cur_floor in double_apartment_floor :
			x_max_quarter = (x_mid - x_min) / 2
			if random.randint(0, 100) < 50 :
				quarter = x_mid - x_max_quarter
				generateLamp(matrix, cur_floor + 3, quarter, z_min, orientation)
				generateDoor(matrix, cur_floor+1, quarter, z_min, (64,8), (64,3))
				generateBalcony(matrix, cur_floor,quarter - 2, quarter + 2, z_min - 1, area_z_min, orientation, stairs_id[0], fence_id, structureBloc_id, slab_id, wall)
			if random.randint(0, 100) < 50 :
				x_max_quarter += 1 if x_max_quarter < 4 else 0
				quarter = x_mid + x_max_quarter
				generateLamp(matrix, cur_floor + 3, quarter, z_min, orientation)
				generateDoor(matrix, cur_floor+1, quarter, z_min, (64,8), (64,3))
				generateBalcony(matrix, cur_floor, quarter - 2, quarter + 2, z_min - 1, area_z_min, orientation, stairs_id[0], fence_id, structureBloc_id, slab_id, wall)
		else :
			if random.randint(0,100) < 75 :
				generateLamp(matrix, cur_floor + 3, x_mid, z_min, orientation)
				generateDoor(matrix, cur_floor + 1, x_mid, z_min, (64,8), (64,3))
				generateBalcony(matrix, cur_floor, x_min + 2, x_max - 2, z_min - 1, area_z_min, orientation, stairs_id[0], fence_id, structureBloc_id, slab_id, wall)
		cur_floor += floor_size

def generateLamp(matrix, h, x, z, orientation):
	matrix.setValue(h, x, z, (123, 0))
	if orientation == "N" :
		matrix.setValue(h, x, z - 1, (69, 4))
	elif orientation == "S" :
		matrix.setValue(h, x, z + 1, (69, 3))
	elif orientation == "W" :
		matrix.setValue(h, x + 1, z, (69, 2))
	elif orientation == "E" :
		matrix.setValue(h, x - 1, z, (69, 1))

def generateCorridorInterior(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, fence_id):
	cur_floor = h_min
	floor = 0
	x_mid = x_max - int((x_max - x_min)/2)
	z_mid = z_max - int((z_max - z_min)/2)

	while cur_floor < h_max:
		cur_floor_ceiling = cur_floor+floor_size

		x_mid = x_min + (x_max-x_min)/2
		z_mid = z_min + (z_max-z_min)/2
		generateChandelier(matrix, cur_floor_ceiling, x_mid, z_mid, fence_id, 1)

		# corridor's carpet
		for x in range(x_min+1, x_max):
			for z in range(z_min+1, z_max):
				matrix.setValue(cur_floor+1,x,z, (171, 12))

		cur_floor += floor_size

def generateBuildingWalls(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall):

	# walls along x axis
	for x in range(x_min, x_max+1):
		for y in range(h_min, h_max):
			matrix.setValue(y,x,z_max, wall)
			matrix.setValue(y,x,z_min, wall)

	# walls along z axis
	for z in range(z_min, z_max+1):
		for y in range(h_min, h_max):
			matrix.setValue(y,x_max,z, wall)
			matrix.setValue(y,x_min,z, wall)

def generateFloorsDivision(matrix, h_min, h_max, floor_size, x_min, x_max, z_min, z_max, wall):
	# floors division
	cur_floor = h_min
	while cur_floor <= h_max:
		for x in range(x_min, x_max+1):
			for z in range(z_min, z_max+1):
				matrix.setValue(cur_floor,x,z, wall)

		cur_floor += floor_size

def getOrientation():
	return "S"

def generateDoor(matrix, y, x, z, door_up, door_down):
	matrix.setValue(y+1, x, z, door_up)
	matrix.setValue(y, x, z, door_down)

def constructWindows(matrix, h, x, x_shifting, z, window_id):
	matrix.setValue(h, x + x_shifting, z, window_id)
	matrix.setValue(h - 1, x + x_shifting, z, window_id)
	matrix.setValue(h, x - x_shifting, z, window_id)
	matrix.setValue(h - 1, x - x_shifting, z, window_id)

def generateBuildingWindows_AlongZ(matrix, h_min, h_max, floor_size, x_min, x_max, z, double_apartment_floor):
	x_window_size = x_max-random.randint(x_min+2, x_max-2)

	# windows
	cur_floor = h_min
	while cur_floor < h_max:
		window_h = cur_floor + 1 + int(math.ceil(floor_size/2))
		if cur_floor in double_apartment_floor or cur_floor == h_min:
			x_mid = x_max - (x_max - x_min)/2
			shifting = 1
			while x_mid + shifting + 1 < x_max and x_mid - shifting - 1 > x_min :
				constructWindows(matrix, window_h, x_mid, shifting, z, (20,0))
				constructWindows(matrix, window_h, x_mid, shifting + 1, z, (20,0))
				if shifting == 1 and x_mid + shifting + 2 < x_max and x_mid - shifting - 2 > x_min :
					constructWindows(matrix, window_h, x_mid, shifting + 2, z, (20,0))
					shifting += 1
				shifting += 3
		else :
			for x in range(x_min+2, x_max-1, 3):
				# apartment windows
				matrix.setValue(window_h, x, z, (20,0))
				matrix.setValue(window_h-1, x, z, (20,0))
				matrix.setValue(window_h, x+1, z, (20,0))
				matrix.setValue(window_h-1, x+1, z, (20,0))

		cur_floor += floor_size
