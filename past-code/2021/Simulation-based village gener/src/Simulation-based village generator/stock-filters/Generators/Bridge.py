import logging
import toolbox as toolbox
air_like = [0, 6, 17, 18, 30, 31, 32, 37, 38, 39, 40, 59, 81, 83, 85, 104, 105, 106, 107, 111, 141, 142, 161, 162, 175, 78, 79, 99]
water_like = [8, 9, 10, 11]

def generateBridge(matrix, height_map, p1, p2, bridge_Type): #generate a bridge between p1 and p2
	logger = logging.getLogger("bridge")

	if bridge_Type == "Wood":
		bridge_Middle_Bottom = toolbox.getBlockID("wooden_slab", 5)
		bridge_Middle_Top = toolbox.getBlockID("wooden_slab", 13)
		bridge_Middle_Double = toolbox.getBlockID("double_wooden_slab", 5)
		bridge_Side_Bottom = toolbox.getBlockID("stone_slab", 2)
		bridge_Side_Top = toolbox.getBlockID("stone_slab", 10)
		bridge_Side_Double = toolbox.getBlockID("double_stone_slab", 10)
		bridge_Base = toolbox.getBlockID("grass_path")
		pillar_Base = toolbox.getBlockID("log")
		pillar = toolbox.getBlockID("oak_fence")

	elif bridge_Type == "Stone":
		bridge_Middle_Bottom = toolbox.getBlockID("stone_slab", 5)
		bridge_Middle_Top = toolbox.getBlockID("stone_slab", 13)
		bridge_Middle_Double = toolbox.getBlockID("double_wooden_slab", 5)
		bridge_Side_Bottom = toolbox.getBlockID("stone_slab")
		bridge_Side_Top = toolbox.getBlockID("stone_slab", 8)
		bridge_Side_Double = toolbox.getBlockID("double_wooden_slab")
		bridge_Base = toolbox.getBlockID("stone", 6)
		pillar_Base = toolbox.getBlockID("cobblestone")
		pillar = toolbox.getBlockID("cobblestone_wall")

	def getPathBridge(matrix, p1, p2): #find a path to link p1 to p2
		path_bridge = []
		actual_point = p1
		path_bridge.append(actual_point)
		while actual_point != p2:
			if actual_point[0] < p2[0]:
				actual_point = (actual_point[0] + 1, actual_point[1])
				path_bridge.append(actual_point)
			if actual_point[0] > p2[0]:
				actual_point = (actual_point[0] - 1, actual_point[1])
				path_bridge.append(actual_point)
			if actual_point[1] < p2[1]:
				actual_point = (actual_point[0], actual_point[1] + 1)
				path_bridge.append(actual_point)
			if actual_point[1] > p2[1]:
				actual_point = (actual_point[0], actual_point[1] - 1)
				path_bridge.append(actual_point)
		return path_bridge

	def buildBridge(matrix, path_bridge, h_bridge, h_start, normal_bridge):
		#check if the bridge is more x or z axis
		if abs(path_bridge[0][0] - path_bridge[len(path_bridge)-1][0]) >= abs(path_bridge[0][1] - path_bridge[len(path_bridge)-1][1]):
			x_val = 0
			z_val = 1
		else:
			x_val = 1
			z_val = 0

		#build cross in the middle of the bridge
		matrix.setValue(h_bridge, middlepoint[0], middlepoint[1], bridge_Middle_Double)
		matrix.setValue(h_bridge, middlepoint[0]+x_val, middlepoint[1]+z_val, bridge_Middle_Double)
		matrix.setValue(h_bridge, middlepoint[0]-x_val, middlepoint[1]-z_val, bridge_Middle_Double)
		buildPillar(matrix, h_bridge-1, middlepoint)

		#_______________________main path of the bridge______________________________
		is_half_block = True
		h_actual = h_start
		#start of the bridge
		matrix.setValue(h_actual, path_bridge[0][0], path_bridge[0][1], bridge_Middle_Bottom)
		fillUnder(matrix, h_actual, path_bridge[0][0], path_bridge[0][1])
		matrix.setValue(h_actual, path_bridge[1][0], path_bridge[1][1], bridge_Middle_Double)
		fillUnder(matrix, h_actual, path_bridge[1][0], path_bridge[1][1])

		for i in range(2, len(path_bridge)-1):
			#the bridge goes up
			if h_actual != h_bridge:
				if is_half_block == True: #check if we need to put a full block or 2 slabs
					matrix.setValue(h_actual, path_bridge[i][0], path_bridge[i][1], bridge_Middle_Top)
					matrix.setValue(h_actual+1, path_bridge[i][0], path_bridge[i][1], bridge_Middle_Bottom)
					h_actual += 1
				else:
					matrix.setValue(h_actual, path_bridge[i][0], path_bridge[i][1], bridge_Middle_Double)
				is_half_block = not is_half_block

			#max height reached
			else:
				matrix.setValue(h_bridge, path_bridge[i][0], path_bridge[i][1], bridge_Middle_Double)

		#_______________________extend the bridge on both sides______________________________
		is_half_block = True
		h_actual = h_start
		barrierPut = False
		#start of the bridge
		setIfCorrect(matrix, h_actual, path_bridge[0][0]-x_val, path_bridge[0][1]-z_val, bridge_Side_Bottom)
		fillUnder(matrix, h_actual, path_bridge[0][0]-x_val, path_bridge[0][1]-z_val)
		setIfCorrect(matrix, h_actual, path_bridge[0][0]+x_val, path_bridge[0][1]+z_val, bridge_Side_Bottom)
		fillUnder(matrix, h_actual, path_bridge[0][0]+x_val, path_bridge[0][1]+z_val)
		setIfCorrect(matrix, h_actual, path_bridge[1][0]-x_val, path_bridge[1][1]-z_val, bridge_Side_Double)
		fillUnder(matrix, h_actual, path_bridge[1][0]-x_val, path_bridge[1][1]-z_val)
		setIfCorrect(matrix, h_actual, path_bridge[1][0]+x_val, path_bridge[1][1]+z_val, bridge_Side_Double)
		fillUnder(matrix, h_actual, path_bridge[1][0]+x_val, path_bridge[1][1]+z_val)

		for i in range(2, len(path_bridge)-1):
			#the bridge goes up
			if h_actual != h_bridge:
				if is_half_block == True: #check if we need to put a full block or 2 slabs
					setIfCorrect(matrix, h_actual+1, path_bridge[i][0]-x_val, path_bridge[i][1]-z_val, bridge_Side_Bottom)
					setIfCorrect(matrix, h_actual, path_bridge[i][0]-x_val, path_bridge[i][1]-z_val, bridge_Side_Top)
					setIfCorrect(matrix, h_actual+1, path_bridge[i][0]+x_val, path_bridge[i][1]+z_val, bridge_Side_Bottom)
					setIfCorrect(matrix, h_actual, path_bridge[i][0]+x_val, path_bridge[i][1]+z_val, bridge_Side_Top)
					h_actual += 1
				else:
					setIfCorrect(matrix, h_actual, path_bridge[i][0]-x_val, path_bridge[i][1]-z_val, bridge_Side_Double)
					setIfCorrect(matrix, h_actual, path_bridge[i][0]+x_val, path_bridge[i][1]+z_val, bridge_Side_Double)
				is_half_block = not is_half_block

			#max height reached
			else:
				setIfCorrect(matrix, h_bridge, path_bridge[i][0]-x_val, path_bridge[i][1]-z_val, bridge_Side_Double)
				setIfCorrect(matrix, h_bridge, path_bridge[i][0]+x_val, path_bridge[i][1]+z_val, bridge_Side_Double)
				#Build the barrier and light when the direction is fixed if the bridge is normal
				if normal_bridge == True and barrierPut == False and len(path_bridge) - i >= 2:
					if path_bridge[i-1][0] != path_bridge[i][0] != path_bridge[i+1][0]:
						buildBarrierX(matrix, h_bridge, path_bridge[i:len(path_bridge)])
						barrierPut = True
					if path_bridge[i-1][1] != path_bridge[i][1] != path_bridge[i+1][1]:
						buildBarrierZ(matrix, h_bridge, path_bridge[i:len(path_bridge)])
						barrierPut = True

	def fillUnder(matrix, h, x, z): #put blocks under the position if there is air
		(b, d) = toolbox.getBlockFullValue(matrix, h, x, z)
		if (b, d) == bridge_Middle_Top:
			matrix.setValue(h, x, z, bridge_Middle_Double)
		elif (b, d) == bridge_Side_Top:
			matrix.setValue(h, x, z, bridge_Side_Double)
		h -= 1
		while matrix.getValue(h, x, z) in air_like+water_like:
			matrix.setValue(h, x, z, bridge_Side_Double)
			h -= 1

	def cleanAbove(matrix, h, x, z): #erase block above the block selected
		h += 1
		while matrix.getValue(h, x, z) not in air_like:
			matrix.setValue(h, x, z, 0)
			h += 1

	def setIfCorrect(matrix, h, x, z, i): #put block only if the position given is correct
		(b,d) = toolbox.getBlockFullValue(matrix, h-1, x, z)
		if matrix.getValue(h, x, z) in air_like and (b,d) not in [bridge_Side_Double,bridge_Side_Top,bridge_Side_Bottom,bridge_Middle_Double,bridge_Middle_Top,bridge_Middle_Bottom]:
			matrix.setValue(h, x, z, i)


	def buildPillar(matrix, h, p): #build a pillar in the water as support to bridge
		while matrix.getValue(h, p[0], p[1]) in air_like:
			matrix.setValue(h, p[0], p[1], pillar)
			h -= 1
		while matrix.getValue(h, p[0], p[1]) in water_like:
			matrix.setValue(h, p[0], p[1], pillar_Base)
			h -= 1

	def buildBarrierX(matrix, h_bridge, path_bridge): #build barrier on the bridge going through the X axis
		putLight(matrix, h_bridge, path_bridge[0][0], path_bridge[0][1]-2)
		putLight(matrix, h_bridge, path_bridge[0][0], path_bridge[0][1]+2)
		for i in range(1, len(path_bridge)):
			matrix.setValue(h_bridge+1, path_bridge[i][0], path_bridge[i][1]-2, pillar)
			matrix.setValue(h_bridge+1, path_bridge[i][0], path_bridge[i][1]+2, pillar)

	def buildBarrierZ(matrix, h_bridge, path_bridge): #build barrier on the bridge going through the Z axis
		putLight(matrix, h_bridge, path_bridge[0][0]-2, path_bridge[0][1])
		putLight(matrix, h_bridge, path_bridge[0][0]+2, path_bridge[0][1])
		for i in range(1, len(path_bridge)):
			matrix.setValue(h_bridge+1, path_bridge[i][0]-2, path_bridge[i][1], pillar)
			matrix.setValue(h_bridge+1, path_bridge[i][0]+2, path_bridge[i][1], pillar)

	def putLight(matrix, h, x, z): #build a light and a pillar under it
		matrix.setValue(h+1,x,z,pillar)
		matrix.setValue(h+2,x,z,pillar)
		matrix.setValue(h+3,x,z,(123,0))
		matrix.setEntity(h+4, x, z, (178,15), "daylight_detector")
		buildPillar(matrix, h, (x, z))

	def cleanFundation(matrix, p, height_map): #clean the endpoints of the bridge
		h = height_map[p[0]][p[1]]
		for neighbor_position in [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
			position_to_clean = (p[0] + neighbor_position[0], p[1] + neighbor_position[1])
			if matrix.getValue(h+1, position_to_clean[0], position_to_clean[1]) != 45:
				matrix.setValue(h, position_to_clean[0], position_to_clean[1], bridge_Base)
				fillUnder(matrix, h, position_to_clean[0], position_to_clean[1])
				cleanAbove(matrix, h, position_to_clean[0], position_to_clean[1])
				height_map[position_to_clean[0]][position_to_clean[1]] = h

	def buildSmallBridge(matrix, path_bridge, h):
		if abs(path_bridge[0][0] - path_bridge[len(path_bridge)-1][0]) >= abs(path_bridge[0][1] - path_bridge[len(path_bridge)-1][1]):
			x_val = 0
			z_val = 1
		else:
			x_val = 1
			z_val = 0

		for i in range(0, len(path_bridge)):
			x = path_bridge[i][0]
			z = path_bridge[i][1]
			matrix.setValue(h, x, z, bridge_Middle_Double)

		#build cross in the middle of the bridge
		matrix.setValue(h, middlepoint[0], middlepoint[1], bridge_Middle_Double)
		matrix.setValue(h, middlepoint[0]+x_val, middlepoint[1]+z_val, bridge_Middle_Double)
		matrix.setValue(h, middlepoint[0]-x_val, middlepoint[1]-z_val, bridge_Middle_Double)
		buildPillar(matrix, h-1, middlepoint)

		for i in range(0, len(path_bridge)-1):
			setIfCorrect(matrix, h, path_bridge[i][0]-x_val, path_bridge[i][1]-z_val, bridge_Side_Double)
			setIfCorrect(matrix, h, path_bridge[i][0]+x_val, path_bridge[i][1]+z_val, bridge_Side_Double)

	logger.info("Trying to generate Bridge between {} and {}".format(p1, p2))
	#finding height
	h1 = height_map[p1[0]][p1[1]]
	h2 = height_map[p2[0]][p2[1]]
	h_bridge = max(h1,h2)+2
	if min(h1,h2) == h1:
		min_point = p1
		max_point = p2
	else:
		min_point = p2
		max_point = p1

	#get the path for the 2 sides of the bridge
	logger.info("Calculating the path for the 2 sides of the Bridge")
	middlepoint = (int((p1[0]+p2[0])/2),(int((p1[1]+p2[1])/2)))
	path_bridge1 = getPathBridge(matrix, p1, middlepoint) #first half
	path_bridge2 = getPathBridge(matrix, p2, middlepoint) #second half

	if toolbox.getManhattanDistance(p1,p2) < 6:
		logger.info("Bridge too small with length : {}, generating a small one".format(toolbox.getManhattanDistance(p1, p2)))
		buildSmallBridge(matrix, path_bridge1, height_map[max_point[0]][max_point[1]])
		buildSmallBridge(matrix, path_bridge2, height_map[max_point[0]][max_point[1]])

	else:
		#clean the fundations only if the bridge is not small
		cleanFundation(matrix, p1, height_map)
		cleanFundation(matrix, p2, height_map)

		#check if the normal bridge is buildable
		if height_map[min_point[0]][min_point[1]] + len(path_bridge1)*0.5 >= h_bridge:
			logger.info("Bridge size enough to go up on both sides with length : {}, generating a normal bridge".format(toolbox.getManhattanDistance(p1, p2)))
			#build the bridge
			buildBridge(matrix, path_bridge1, h_bridge, h1+1, True) #first part of the bridge
			buildBridge(matrix, path_bridge2, h_bridge, h2+1 ,True) #second part
		else: #bridge can't be built that way, going up only from one side
			logger.info("Bridge too small to go up on both sides with length : {}, trying to go up only from the lowest point".format(toolbox.getManhattanDistance(p1, p2)))
			path_bridge = getPathBridge(matrix, min_point, max_point) #full bridge
			if height_map[min_point[0]][min_point[1]] + len(path_bridge)*0.5 >= height_map[max_point[0]][max_point[1]]: #check if the difference of height is still too big
				logger.info("Bridge buildable from one side")
				buildBridge(matrix, path_bridge, max(h1,h2), min(h1,h2)+1, False)
			else:
				logger.error("Bridge not buildable, cancel generation")
				raise ValueError('Bridge not buildable')
