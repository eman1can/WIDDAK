import threading
import numpy as np
import WorldEdit
import mapUtils
from worldLoader import WorldSlice
from CornerHouse import CornerHouse
from House import House
from Courtyard import Courtyard
from Structure import Structure

# Set to True to enable multi-threading. This will make the built go slightly faster, but can also crash the
# Minecraft Forge server/client when there are too many threads, which may occur when constructing in a large
# build area.
USE_THREADING = False


class HousingBlock:

    def __init__(self,
                 x: int = 0,
                 z: int = 0,
                 houseBlockSizeX: int = 66,
                 houseBlockSizeZ: int = 66,
                 northSideWalkWidth: int = 4,
                 eastSideWalkWidth: int = 4,
                 southSideWalkWidth: int = 4,
                 westSideWalkWidth: int = 4,
                 northStreetWidth: int = 3,
                 eastStreetWidth: int = 3,
                 southStreetWidth: int = 2,
                 westStreetWidth: int = 2
                 ):

        self.houseBlockSizeX = houseBlockSizeX
        self.houseBlockSizeZ = houseBlockSizeZ

        self.northSideWalkWidth = northSideWalkWidth
        self.eastSideWalkWidth = eastSideWalkWidth
        self.southSideWalkWidth = southSideWalkWidth
        self.westSideWalkWidth = westSideWalkWidth

        self.northStreetWidth = northStreetWidth
        self.eastStreetWidth = eastStreetWidth
        self.southStreetWidth = southStreetWidth
        self.westStreetWidth = westStreetWidth

        self.x = x
        self.z = z

        self.farX = x + eastStreetWidth + eastSideWalkWidth + houseBlockSizeX + westSideWalkWidth + westStreetWidth
        self.farZ = z + northStreetWidth + northSideWalkWidth + houseBlockSizeZ + southSideWalkWidth + southStreetWidth

        worldSlice = WorldSlice((x, z, self.getSizeX(), self.getSizeZ()))
        self.heightMap = mapUtils.calcGoodHeightmap(worldSlice)
        self.y = mapUtils.getMostFrequentHeight(self.heightMap)

        self.rng = np.random.default_rng()

        self.houses = []
        self._initHouses()

    def getSizeX(self):
        return self.farX - self.x

    def getSizeZ(self):
        return self.farZ - self.z

    def _initHouses(self):
        houseBlockX = self.x + self.westStreetWidth + self.westSideWalkWidth
        houseBlockZ = self.z + self.northStreetWidth + self.northSideWalkWidth

        corners = [
            (
                lambda houseSizeX: houseBlockX + self.houseBlockSizeX - (houseSizeX + 4),
                lambda houseSizeZ: houseBlockZ + self.houseBlockSizeZ - (houseSizeZ + 1)
            ),
            (
                lambda houseSizeX: houseBlockX + houseSizeX - 1,
                lambda houseSizeZ: houseBlockZ + self.houseBlockSizeZ - (houseSizeZ + 1)
            ),
            (
                lambda houseSizeX: houseBlockX + houseSizeX - 1,
                lambda houseSizeZ: houseBlockZ + houseSizeZ + 2
            ),
            (
                lambda houseSizeX: houseBlockX + self.houseBlockSizeX - (houseSizeX + 4),
                lambda houseSizeZ: houseBlockZ + houseSizeZ + 2
            ),
        ]
        rotation = 0
        for (cornerX, cornerZ) in corners:
            cornerHouse = CornerHouse(rotation=rotation)
            xw = cornerHouse.bottomStructure.getSizeZ()
            zw = cornerHouse.bottomStructure.getSizeX()
            cornerHouse.setPosition(
                x=cornerX(xw),
                y=self.y,
                z=cornerZ(zw)
            )
            self.houses.append(cornerHouse)
            rotation += 1

        middles = [
            (
                houseBlockX + self.houses[0].bottomStructure.getSizeX(),
                houseBlockZ + self.houseBlockSizeZ - (self.houses[0].bottomStructure.getSizeZ() + 1)
            ),
            (
                houseBlockX + self.houses[1].bottomStructure.getSizeX() - 1,
                houseBlockZ + self.houses[1].bottomStructure.getSizeZ() + 3
            ),
            (
                houseBlockX + (self.houses[2].bottomStructure.getSizeX() * 2) + 1,
                houseBlockZ + self.houses[2].bottomStructure.getSizeZ() + 2
            ),
            (
                houseBlockX + self.houseBlockSizeZ - self.houses[3].bottomStructure.getSizeX() - 4,
                houseBlockZ + (self.houses[3].bottomStructure.getSizeZ() * 2) + 4
            )
        ]
        rotation = 0
        for (middleX, middleZ) in middles:
            middleHouse = House(rotation=rotation, x=middleX, y=self.y, z=middleZ)
            self.houses.append(middleHouse)
            rotation += 1

        courtyard = Courtyard(
            x=self.houses[0].x - (self.houses[0].bottomStructure.getSizeX() + 2),
            y=self.y,
            z=self.houses[0].z - (self.houses[0].bottomStructure.getSizeZ() + 2)
        )
        self.houses.append(courtyard)

    def placeStreets(self):

        # Add streets and sidewalks around the housing block
        streetHeight = self.y - 1

        WorldEdit.fill(
            self.x, streetHeight, self.z,
            self.farX, streetHeight, self.z + self.northStreetWidth,
            'minecraft:gray_concrete'
        )
        WorldEdit.fillEmpty(
            self.x, streetHeight - 1, self.z,
            self.farX, self.heightMap.min(), self.z + self.northStreetWidth,
            'minecraft:stone_bricks'
        )
        northSideWalkRect = [
            self.x + self.westStreetWidth + 1, streetHeight, self.z + self.northStreetWidth + 1,
            self.farX - self.eastStreetWidth - 1, streetHeight,
            self.z + self.northStreetWidth + self.northSideWalkWidth + 1
        ]
        self.placeSideWalk(northSideWalkRect)
        sideWalkIndex = northSideWalkRect[0] + self.rng.integers(low=3, high=10)
        while sideWalkIndex < northSideWalkRect[3] - 3:
            self.placeTree(sideWalkIndex, streetHeight + 1, northSideWalkRect[2] - 1)
            sideWalkIndex += self.rng.integers(low=10, high=20)

        WorldEdit.fill(
            self.farX - self.eastStreetWidth, streetHeight, self.z,
            self.farX, streetHeight, self.farZ,
            'minecraft:gray_concrete'
        )
        WorldEdit.fillEmpty(
            self.farX - self.eastStreetWidth, streetHeight - 1, self.z,
            self.farX, self.heightMap.min(), self.farZ,
            'minecraft:stone_bricks'
        )
        eastSideWalkRect = [
            self.farX - self.eastStreetWidth - 1, streetHeight, self.z + self.northStreetWidth + 1,
            self.farX - (self.eastStreetWidth + self.eastSideWalkWidth + 3), streetHeight,
            self.farZ - self.southStreetWidth - 1,
        ]
        self.placeSideWalk(eastSideWalkRect)
        sideWalkIndex = eastSideWalkRect[2] + self.rng.integers(low=3, high=10)
        while sideWalkIndex < eastSideWalkRect[5] - 3:
            self.placeTree(eastSideWalkRect[0] - 3, streetHeight + 1, sideWalkIndex)
            sideWalkIndex += self.rng.integers(low=10, high=20)

        WorldEdit.fill(
            self.farX, streetHeight, self.farZ - self.southStreetWidth,
            self.x, streetHeight, self.farZ,
            'minecraft:gray_concrete'
        )
        WorldEdit.fillEmpty(
            self.farX, streetHeight - 1, self.farZ - self.southStreetWidth,
            self.x, self.heightMap.min(), self.farZ,
            'minecraft:stone_bricks'
        )
        southSideWalkRect = [
            self.x + self.westStreetWidth + 1, streetHeight, self.farZ - self.southStreetWidth - 1,
            self.farX - self.eastStreetWidth - 1, streetHeight, self.farZ - (self.southStreetWidth + self.southSideWalkWidth)
        ]
        self.placeSideWalk(southSideWalkRect)
        sideWalkIndex = southSideWalkRect[0] + self.rng.integers(low=3, high=10)
        while sideWalkIndex < southSideWalkRect[3] - 3:
            self.placeTree(sideWalkIndex, streetHeight + 1, southSideWalkRect[2] - 2)
            sideWalkIndex += self.rng.integers(low=10, high=20)

        WorldEdit.fill(
            self.x + self.westStreetWidth, streetHeight, self.z,
            self.x, streetHeight, self.farZ,
            'minecraft:gray_concrete'
        )
        WorldEdit.fillEmpty(
            self.x + self.westStreetWidth, streetHeight - 1, self.z,
            self.x, self.heightMap.min(), self.farZ,
            'minecraft:stone_bricks'
        )
        westSideWalkRect = [
            self.x + self.westStreetWidth + 1, streetHeight, self.z + self.northStreetWidth + 1,
            self.x + self.westStreetWidth + self.westSideWalkWidth - 2, streetHeight, self.farZ - self.southStreetWidth - 1
        ]
        self.placeSideWalk(westSideWalkRect)

    def placeSideWalk(self, rect):
        WorldEdit.fillEmpty(
            *rect,
            'minecraft:stone_bricks'
        )
        WorldEdit.fill(
            *np.add(rect, [0, 1, 0, 0, 1, 0]),
            'minecraft:stone_brick_slab'
        )

    def placeTree(self, x, y, z):
        # Load in some trees
        Structure(
            structure=self.rng.choice(Structure.getStructuresInDir("streetFurniture")),
            x=x,
            y=y,
            z=z
        ).place(includeAir=False)

    def place(self):
        for house in self.houses:
            if USE_THREADING:
                threading.Thread(target=house.place, args=(self.heightMap,)).start()
            else:
                house.place(self.heightMap)
        if USE_THREADING:
            threading.Thread(target=self.placeStreets).start()
        else:
            self.placeStreets()


