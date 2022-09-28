from Classes import Base
from Classes import Blueprint
from Common import loadFile

def getTowerBlueprint(point, baseHeight):
	filePath = "./stock-filters/SettlementGenerator/StructureBuilder/structures/tower/tower_medium.json"
	blockRegister = loadFile(filePath)
	base = Base(point.x + 2, point.z + 2, 7, 7)
	return Blueprint(point, blockRegister, baseHeight, base, True)