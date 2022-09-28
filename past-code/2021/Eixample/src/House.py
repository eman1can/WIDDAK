import WorldEdit
from Structure import Structure
from materials import Fences, Walls, BuildingBlocks, Doors
import numpy as np


class House:

    bottomFloorDir = 'bottomFloor'
    floorDir = 'floor'
    roofDir = 'roof'

    def __init__(self, x=0, y=0, z=0, rotation=Structure.ROTATE_NORTH):
        self.x = x
        self.y = y
        self.z = z
        self.rotation = rotation

        self.rng = np.random.default_rng()

        # Set random number of floors between 6 and 9
        self.numberOfFloors = self.rng.integers(6, 8)

        self.interiorFloorMaterial = self.rng.choice([
            "minecraft:birch_planks",
            "minecraft:acacia_planks",
            "minecraft:dark_oak_planks",
            "minecraft:jungle_planks",
            "minecraft:oak_planks",
            "minecraft:spruce_planks"
        ])

        self.structures = dict()

        self._getStructureFiles()

        self.bottomStructure = self._getStructure('bottomFloor')

    def setPosition(self, x=None, y=None, z=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z

    def setRotation(self, rotation):
        if rotation is not None and 0 <= rotation <= 3:
            self.rotation = rotation

    def _getStructureFiles(self):
        self.structures['bottomFloor'] = Structure.getStructuresInDir(self.bottomFloorDir)
        self.structures['floor'] = Structure.getStructuresInDir(self.floorDir)
        self.structures['roof'] = Structure.getStructuresInDir(self.roofDir)

    def findMaterials(self, structure):
        materials = structure.getMaterialList()
        materialSet = set(materials)
        materialsDict = {}

        # find the current balcony
        fence = materialSet.intersection(Fences)
        if fence:
            fence = fence.pop()
            materialsDict['fence'] = fence

        wall = materialSet.intersection(Walls)
        if wall:
            wall = wall.pop()
            materialsDict['wall'] = wall

        buildingblock = materialSet.intersection(BuildingBlocks)
        if buildingblock:
            buildingblock = buildingblock.pop()
            materialsDict['buildingblock'] = buildingblock

        door = materialSet.intersection(Doors)
        if door:
            door = door.pop()
            materialsDict['door'] = door

        return materialsDict

    def place(self, heightMap):

        yOffset = 1

        # Reint bottomstructure with new position
        self.bottomStructure = Structure(
            structure=self.bottomStructure.structurePath,
            x=self.x,
            y=self.y + yOffset,
            z=self.z,
            rotation=self.rotation
        )
        defaultMaterials = self.findMaterials(self.bottomStructure)
        if 'buildingblock' in defaultMaterials:
            self.bottomStructure.replaceMaterial(defaultMaterials['buildingblock'], self.rng.choice(BuildingBlocks))
        if 'door' in defaultMaterials:
            self.bottomStructure.replaceMaterial(defaultMaterials['door'], self.rng.choice(Doors))
        foundationFarCorner = self.bottomStructure.getFarCornerInWorldSpace()
        WorldEdit.fill(
            self.bottomStructure.x, self.y - 1, self.bottomStructure.z,
            foundationFarCorner[0], self.y, foundationFarCorner[2],
            "minecraft:stone_bricks"
        )
        WorldEdit.fillEmpty(
            self.bottomStructure.x, self.y - 2, self.bottomStructure.z,
            foundationFarCorner[0], heightMap.min(), foundationFarCorner[2],
            "minecraft:stone_bricks"
        )
        self.bottomStructure.place()

        yOffset = yOffset + self.bottomStructure.getSizeY()

        floorStructure = self._getStructure('floor')
        defaultMaterials = self.findMaterials(floorStructure)
        if 'fence' in defaultMaterials:
            floorStructure.replaceMaterial(defaultMaterials['fence'], self.rng.choice(Fences))
        if 'wall' in defaultMaterials:
            floorStructure.replaceMaterial(defaultMaterials['wall'], self.rng.choice(Walls))
        if 'buildingblock' in defaultMaterials:
            floorStructure.replaceMaterial(defaultMaterials['buildingblock'], self.rng.choice(BuildingBlocks))
        if 'door' in defaultMaterials:
            floorStructure.replaceMaterial(defaultMaterials['door'], self.rng.choice(Doors))

        for floorIndex in range(1, self.numberOfFloors):
            floorStructure.setPosition(y=self.y + yOffset)
            floorStructure.place()
            yOffset = yOffset + floorStructure.getSizeY()

    def _getStructure(self, structureType) -> Structure:
        return Structure(
            self.rng.choice(self.structures[structureType]),
            rotation=self.rotation,
            x=self.x,
            z=self.z
        )
