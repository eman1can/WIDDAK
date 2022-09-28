import BlockDictionary

from BiomeChanges import defaultBiomeChanges
from BlockRegisterRotater import rotateRegister
from Classes import Base
from Classes import Blueprint
from Common import setBlock
from HouseManager import getHouseBlueprint
from TowerManager import getTowerBlueprint

directions = ['north', 'east', 'south', 'west']

def buildStructure(level, point, baseHeight, type='tower', direction='north', biome='plains', applyBiomeChanges=True, specialBiomeChanges=None, prop=None):
	blueprint = getBlueprint(type, point, baseHeight, prop)
	applyChangesToBlueprintBlockRegister(blueprint, direction, biome, applyBiomeChanges, specialBiomeChanges)
	build(level, blueprint)

def getBlueprint(type, point, baseHeight, prop):
	if type == 'house':
		return getHouseBlueprint(point, prop)
	if type == 'tower':
		return getTowerBlueprint(point, baseHeight)

def applyChangesToBlueprintBlockRegister(blueprint, direction, biome, applyBiomeChanges, specialBiomeChanges):
	if not blueprint.blockRegister:
		return
	blueprint.blockRegister = rotateRegister(blueprint.blockRegister, directions.index(direction))
	if applyBiomeChanges and biome != 'plains':
		blueprint.blockRegister = calculateBiomeChanges(blueprint.blockRegister, specialBiomeChanges, biome)

def calculateBiomeChanges(blockRegister, specialBiomeChanges, biome):
	for block in blockRegister:
		if specialBiomeChanges and specialBiomeChanges.get(biome) and specialBiomeChanges.get(biome).get(block['type']):
			block['type'] = specialBiomeChanges[biome][block['type']]
			continue
		if defaultBiomeChanges.get(biome) and defaultBiomeChanges.get(biome).get(block['type']):
			block['type'] = defaultBiomeChanges[biome][block['type']]
	return blockRegister

def build(level, blueprint):
	for block in blueprint.blockRegister:
		x = blueprint.point.x
		z = blueprint.point.z
		b = None
		if block.get('type'):
			b = BlockDictionary.Block(block['type'], block['direction'], block['verticalAllignment'])
		else:
			b = BlockDictionary.getBlock(block['id'], block['data'])
		if not b:
			setBlock(level, None, x + int(block['x']), blueprint.baseHeight + int(block['y']), z + int(block['z']), block['id'], block['data'])
		else:
			blockIdentifier = BlockDictionary.getBlockIdentifier(b)
			setBlock(level, None, x + int(block['x']), blueprint.baseHeight + int(block['y']), z + int(block['z']), blockIdentifier[0], blockIdentifier[1])
	if blueprint.buildFoundation:
		buildFoundation(level, blueprint)

def buildFoundation(level, blueprint):
	if not blueprint.base:
		return
	xStart = blueprint.base.xStart
	zStart = blueprint.base.zStart
	xEnd = blueprint.base.xStart + blueprint.base.xLength - 1
	zEnd = blueprint.base.zStart + blueprint.base.zLength - 1
	for x in range(xStart, xEnd + 1):
		for z in range(zStart, zEnd + 1):
			i = 1
			while not isSurfaceBlock(level, x, blueprint.baseHeight - i, z):
				blockId = 1
				if i == 1:
					blockId = 98
				if (x == xStart or x == xEnd) and (z == zStart or z == zEnd):
					blockId = 98
				setBlock(level, None, x, blueprint.baseHeight - i, z, blockId)
				i += 1

aboveSurfaceBlocks = [0, 2, 3, 6, 17, 18, 31, 32, 37, 38, 39, 40, 59, 78, 81, 83, 99, 100, 103, 104, 105, 106, 111, 141, 142, 161, 162, 175]
def isSurfaceBlock(level, x, y, z):
	for block in aboveSurfaceBlocks:
		if level.blockAt(x, y, z) == block:
			return False
	return True
