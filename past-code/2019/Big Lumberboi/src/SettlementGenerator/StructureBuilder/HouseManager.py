from BlockRegisterRotater import rotateRegister
from Classes import Base
from Classes import Blueprint
from Classes import Point
from Common import loadFile

directions = ['NORTH', 'EAST', 'SOUTH', 'WEST']

def getHouseBlueprint(point, prop):
	blockRegister = []
	base = Base(point.x, point.z, prop.xLength, prop.zLength)
	blueprint = Blueprint(point, blockRegister, prop.height + 1, base, True)
	addFloor(point, prop, blueprint)
	addWalls(point, prop, blueprint.blockRegister)
	addRoof(point, prop, blueprint.blockRegister)
	return blueprint

def addFloor(point, prop, blueprint):
	for x in range(2, prop.xLength - 2):
		for z in range(2, prop.zLength - 2):
			blueprint.blockRegister.append({'type': 'oak_wood_planks', 'direction': None, 'verticalAllignment': None, 'id': 5, 'data': 0, 'x': x, 'y': 0, 'z': z})

def addWalls(point, prop, blockRegister):
	y = 0
	isDoorPlaced = False
	doorPoint = None
	# North and South default wall segments
	segmentRegister = loadSegmentRegister('wall_default')
	for x in range(2, prop.xLength - 2, 2):
		for block in segmentRegister:
			appendAdjustedBlockToRegister(blockRegister, block, x, y, 1)
			appendAdjustedBlockToRegister(blockRegister, block, prop.xLength - 1 - x, y, prop.zLength - 2)
			if x == prop.xLength - 4:
				appendAdjustedBlockToRegister(blockRegister, block, x + 1, y, 1)
				appendAdjustedBlockToRegister(blockRegister, block, prop.xLength - 2 - x, y, prop.zLength - 2)
	segmentRegister = rotateRegister(segmentRegister, directions.index('EAST'))
	# East and West default wall segments
	for z in range(2, prop.zLength - 2, 2):
		for block in segmentRegister:
			appendAdjustedBlockToRegister(blockRegister, block, 1, y, z)
			appendAdjustedBlockToRegister(blockRegister, block, prop.xLength - 2, y, prop.zLength - 1 - z)
			if z == prop.zLength - 4:
				appendAdjustedBlockToRegister(blockRegister, block, 1, y, z + 1)
				appendAdjustedBlockToRegister(blockRegister, block, prop.xLength - 2, y, prop.zLength - 2 - z)
	segmentRegister = loadSegmentRegister('wall_window')
	# North and South windows and maybe door
	for x in range(3, prop.xLength - 3, 2):
		skipNorth = False
		skipSouth = False
		if not isDoorPlaced:
			if prop.doorDirection == 'NORTH':
				skipNorth = True
			if prop.doorDirection == 'SOUTH':
				skipSouth = True
		if skipNorth:
			doorPoint = Point(x, 1)
			isDoorPlaced = True
		if skipSouth:
			doorPoint = Point(prop.xLength - 1 - x, prop.zLength - 2)
			isDoorPlaced = True
		for block in segmentRegister:
			if not skipNorth:
				appendAdjustedBlockToRegister(blockRegister, block, x, y, 1)
			if not skipSouth:
				appendAdjustedBlockToRegister(blockRegister, block, prop.xLength - 1 - x, y, prop.zLength - 2)
	segmentRegister = rotateRegister(segmentRegister, directions.index('EAST'))
	# East and West windows and maybe door
	for z in range(3, prop.zLength - 3, 2):
		skipEast = False
		skipWest = False
		if not isDoorPlaced:
			if prop.doorDirection == 'EAST':
				skipEast = True
			if prop.doorDirection == 'WEST':
				skipWest = True
		if skipEast:
			doorPoint = Point(prop.xLength - 2, prop.zLength - 1 - z)
			isDoorPlaced = True
		if skipWest:
			doorPoint = Point(1, z)
			isDoorPlaced = True
		for block in segmentRegister:
			if not skipWest:
				appendAdjustedBlockToRegister(blockRegister, block, 1, y, z)
			if not skipEast:
				appendAdjustedBlockToRegister(blockRegister, block, prop.xLength - 2, y, prop.zLength - 1 - z)
	# Corners
	segmentRegister = loadSegmentRegister('wall_corner')
	for block in segmentRegister:
		appendAdjustedBlockToRegister(blockRegister, block, 1, y, 1)
		appendAdjustedBlockToRegister(blockRegister, block, prop.xLength - 2, y, 1)
		appendAdjustedBlockToRegister(blockRegister, block, 1, y, prop.zLength - 2)
		appendAdjustedBlockToRegister(blockRegister, block, prop.xLength - 2, y, prop.zLength - 2)
	# Door
	segmentRegister = loadSegmentRegister('wall_door')
	segmentRegister = rotateRegister(segmentRegister, directions.index(prop.doorDirection))
	for block in segmentRegister:
		appendAdjustedBlockToRegister(blockRegister, block, doorPoint.x, y, doorPoint.z)
	addDoorStep(blockRegister, doorPoint, prop, y)

def addDoorStep(blockRegister, doorPoint, prop, height):
	direction = prop.doorDirection
	doorStepPoint = None
	if direction == 'NORTH':
		doorStepPoint = Point(doorPoint.x, doorPoint.z - 1)
		prop.xPathwayStart = prop.xStart + doorPoint.x
		prop.zPathwayStart = prop.zStart + doorPoint.z - 2
	elif direction == 'EAST':
		doorStepPoint = Point(doorPoint.x + 1, doorPoint.z)
		prop.xPathwayStart = prop.xStart + doorPoint.x + 2
		prop.zPathwayStart = prop.zStart + doorPoint.z
	elif direction == 'SOUTH':
		doorStepPoint = Point(doorPoint.x, doorPoint.z + 1)
		prop.xPathwayStart = prop.xStart + doorPoint.x
		prop.zPathwayStart = prop.zStart + doorPoint.z + 2
	elif direction == 'WEST':
		doorStepPoint = Point(doorPoint.x - 1, doorPoint.z)
		prop.xPathwayStart = prop.xStart + doorPoint.x - 2
		prop.zPathwayStart = prop.zStart + doorPoint.z
	blockRegister.append({'type': 'cobblestone', 'direction': None, 'verticalAllignment': 'bottom', 'id': 5, 'data': 0, 'x': doorStepPoint.x, 'y': height, 'z': doorStepPoint.z})

def addRoof(point, prop, blockRegister):
	shortest = min([prop.xLength, prop.zLength])
	longest = max([prop.xLength, prop.zLength])
	roofRegister = []
	y = 5
	for z in range(0, longest):
		if z == 0:
			roofRegister.append({'type': 'stone_brick', 'direction': 'south', 'verticalAllignment': 'top', 'id': 5, 'data': 0, 'x': 0, 'y': y, 'z': z})
			roofRegister.append({'type': 'oak_wood_fence', 'direction': None, 'verticalAllignment': None, 'id': 85, 'data': 0, 'x': 0, 'y': y + 1, 'z': z})
			roofRegister.append({'type': 'torch', 'direction': None, 'verticalAllignment': None, 'id': 50, 'data': 5, 'x': 0, 'y': y + 2, 'z': z})
			roofRegister.append({'type': 'stone_brick', 'direction': 'south', 'verticalAllignment': 'top', 'id': 5, 'data': 0, 'x': shortest - 1, 'y': y, 'z': z})
			roofRegister.append({'type': 'oak_wood_fence', 'direction': None, 'verticalAllignment': None, 'id': 85, 'data': 0, 'x': shortest - 1, 'y': y + 1, 'z': z})
			roofRegister.append({'type': 'torch', 'direction': None, 'verticalAllignment': None, 'id': 50, 'data': 5, 'x': shortest - 1, 'y': y + 2, 'z': z})
		elif z == longest - 1:
			roofRegister.append({'type': 'stone_brick', 'direction': 'north', 'verticalAllignment': 'top', 'id': 5, 'data': 0, 'x': 0, 'y': y, 'z': z})
			roofRegister.append({'type': 'oak_wood_fence', 'direction': None, 'verticalAllignment': None, 'id': 85, 'data': 0, 'x': 0, 'y': y + 1, 'z': z})
			roofRegister.append({'type': 'torch', 'direction': None, 'verticalAllignment': None, 'id': 50, 'data': 5, 'x': 0, 'y': y + 2, 'z': z})
			roofRegister.append({'type': 'stone_brick', 'direction': 'north', 'verticalAllignment': 'top', 'id': 5, 'data': 0, 'x': shortest - 1, 'y': y, 'z': z})
			roofRegister.append({'type': 'oak_wood_fence', 'direction': None, 'verticalAllignment': None, 'id': 85, 'data': 0, 'x': shortest - 1, 'y': y + 1, 'z': z})
			roofRegister.append({'type': 'torch', 'direction': None, 'verticalAllignment': None, 'id': 50, 'data': 5, 'x': shortest - 1, 'y': y + 2, 'z': z})
		else:
			roofRegister.append({'type': 'oak_wood', 'direction': 'north', 'verticalAllignment': 'top', 'id': 5, 'data': 0, 'x': 0, 'y': y, 'z': z})
			roofRegister.append({'type': 'oak_wood', 'direction': 'north', 'verticalAllignment': 'top', 'id': 5, 'data': 0, 'x': shortest - 1, 'y': y, 'z': z})
			roofRegister.append({'type': 'oak_wood_fence', 'direction': None, 'verticalAllignment': None, 'id': 85, 'data': 0, 'x': 0, 'y': y + 1, 'z': z})
			roofRegister.append({'type': 'oak_wood_fence', 'direction': None, 'verticalAllignment': None, 'id': 85, 'data': 0, 'x': shortest - 1, 'y': y + 1, 'z': z})
		xHalfRounded = int(shortest / 2)
		for x in range(1, xHalfRounded):
			if z == 0 or z == longest - 1:
				roofRegister.append({'type': 'stone_brick', 'direction': 'east', 'verticalAllignment': 'bottom', 'id': 5, 'data': 0, 'x': x, 'y': y + x, 'z': z})
				roofRegister.append({'type': 'stone_brick', 'direction': 'west', 'verticalAllignment': 'bottom', 'id': 5, 'data': 0, 'x': shortest - 1 - x, 'y': y + x, 'z': z})
				roofRegister.append({'type': 'stone', 'direction': None, 'verticalAllignment': 'top', 'id': 44, 'data': 8, 'x': x, 'y': y + x - 1, 'z': z})
				roofRegister.append({'type': 'stone', 'direction': None, 'verticalAllignment': 'top', 'id': 44, 'data': 8, 'x': shortest - 1 - x, 'y': y + x - 1, 'z': z})
				if x == xHalfRounded - 2 and shortest % 2 == 1:
					roofRegister.append({'type': 'stone', 'direction': None, 'verticalAllignment': 'top', 'id': 44, 'data': 8, 'x': xHalfRounded, 'y': y + xHalfRounded - 1, 'z': z})
					if z == 0:
						roofRegister.append({'type': 'stone_brick', 'direction': 'north', 'verticalAllignment': 'bottom', 'id': 5, 'data': 0, 'x': xHalfRounded, 'y': y + xHalfRounded, 'z': z})
					else:
						roofRegister.append({'type': 'stone_brick', 'direction': 'south', 'verticalAllignment': 'bottom', 'id': 5, 'data': 0, 'x': xHalfRounded, 'y': y + xHalfRounded, 'z': z})
			elif z == 1 or z == longest - 2:
				for i in range(1, x):
					roofRegister.append({'type': 'oak_wood_planks', 'direction': None, 'verticalAllignment': None, 'id': 5, 'data': 0, 'x': x, 'y': y + x - i, 'z': z})
					roofRegister.append({'type': 'oak_wood_planks', 'direction': None, 'verticalAllignment': None, 'id': 5, 'data': 0, 'x': shortest - 1 - x, 'y': y + x - i, 'z': z})
				roofRegister.append({'type': 'oak_wood_planks', 'direction': 'east', 'verticalAllignment': 'bottom', 'id': 5, 'data': 0, 'x': x, 'y': y + x, 'z': z})
				roofRegister.append({'type': 'oak_wood_planks', 'direction': 'west', 'verticalAllignment': 'bottom', 'id': 5, 'data': 0, 'x': shortest - 1 - x, 'y': y + x, 'z': z})
				if x == xHalfRounded - 2 and shortest % 2 == 1:
					for i in range(1, xHalfRounded):
						roofRegister.append({'type': 'oak_wood', 'direction': None, 'verticalAllignment': None, 'id': 17, 'data': 0, 'x': xHalfRounded, 'y': y + xHalfRounded - i, 'z': z})
					roofRegister.append({'type': 'stone_brick', 'direction': None, 'verticalAllignment': 'bottom', 'id': 44, 'data': 5, 'x': xHalfRounded, 'y': y + xHalfRounded, 'z': z})
			else:
				roofRegister.append({'type': 'oak_wood_planks', 'direction': 'east', 'verticalAllignment': 'bottom', 'id': 5, 'data': 0, 'x': x, 'y': y + x, 'z': z})
				roofRegister.append({'type': 'oak_wood_planks', 'direction': 'west', 'verticalAllignment': 'bottom', 'id': 5, 'data': 0, 'x': shortest - 1 - x, 'y': y + x, 'z': z})
				if x == xHalfRounded - 2 and shortest % 2 == 1:
					roofRegister.append({'type': 'stone_brick', 'direction': None, 'verticalAllignment': 'bottom', 'id': 44, 'data': 5, 'x': xHalfRounded, 'y': y + xHalfRounded, 'z': z})
	if prop.xLength > prop.zLength:
		roofRegister = rotateRegister(roofRegister, 1)
	elif prop.xLength == prop.zLength:
		roofRegister = rotateRegister(roofRegister, directions.index(prop.doorDirection))
	blockRegister.extend(roofRegister)

def loadSegmentRegister(segment):
	filePath = './stock-filters/SettlementGenerator/StructureBuilder/structures/house/' + segment + '.json'
	return loadFile(filePath)

def appendAdjustedBlockToRegister(register, block, x, y, z):
	register.append({
		'type': block['type'],
		'direction': block['direction'],
		'verticalAllignment': block['verticalAllignment'],
		'id': block['id'],
		'data': block['data'],
		'x': x + block['x'],
		'y': y + block['y'],
		'z': z + block['z']})