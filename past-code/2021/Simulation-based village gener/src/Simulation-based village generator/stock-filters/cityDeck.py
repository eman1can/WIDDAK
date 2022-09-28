from random import shuffle

## Deck size depending of the settlement cize
S = [4, 16] # 6x6 chunks or less
M = [9, 32] # less than 9x9 chunks
L = [16, 64] # less than 12x12 chunks
XL = [36, 256] # more than 12x12 chunks

class CityDeck:

    nbBuildings = nbHouses = nbFarms = nbTowers = nbRollerCoasters = 0
    centerDeck = []
    neighbourhoodDeck = []

    def __init__(self, type, width, depth):

        def getDeckSize(width, depth):
            size = 0
            area = width * depth
            if area < 10000:                        size = S
            elif area >= 10000 and area < 20000:    size = M
            elif area >= 20000 and area < 35000:    size = L
            else:                                   size = XL
            return size

        self.type = type
        self.size = getDeckSize(width, depth)
        #print("deck size : {}".format(self.size))
        self.setType()

    def setType(self):
        if   self.type == "Village": self.setBasicType(self.size)
        elif self.type == "OneHouse": self.setOneHouseType(self.size)
        elif self.type == "City": self.setCityType(self.size)
        elif self.type == "City Center": self.setCityCenterType(self.size)
        elif self.type == "Amusement Park": self.setAmusementParkType(self.size)

        #self.printDeck()
        shuffle(self.centerDeck)
        shuffle(self.neighbourhoodDeck)
        #self.printDeck()

    def setBasicType(self, size):
        for i in range(0, size[0]):
            self.centerDeck.append("house")
        for i in range(0, size[1]):
            self.neighbourhoodDeck.append("farm")

    def setOneHouseType(self, size):
        self.centerDeck.append("house")
        for i in range(0, size[0] - 1):
            self.centerDeck.append("farm")
        for i in range(0, size[1]):
            self.neighbourhoodDeck.append("farm")

    def setCityType(self, size):
        self.centerDeck.append("building")
        for i in range(1, size[0]):
            self.centerDeck.append("building")
        for i in range(0, size[1] // 3):
            self.neighbourhoodDeck.append("house")
            self.neighbourhoodDeck.append("farm")
            self.neighbourhoodDeck.append("slope structure")

    def setCityCenterType(self, size):
        for i in range(0, size[0]):
            self.centerDeck.append("building")
        for i in range(0, size[1]):
            self.neighbourhoodDeck.append("building")

    def setAmusementParkType(self, size):
        for i in range(0, size[0]):
            self.centerDeck.append("slope structure")
        for i in range(0, size[1]):
            self.neighbourhoodDeck.append("slope structure")

    def printDeck(self):
        print("Buildings in center deck : ")
        print('[%s]' % ', '.join(map(str, self.centerDeck)))
        print("Buildings in neighbourhood deck : ")
        print('[%s]' % ', '.join(map(str, self.neighbourhoodDeck)))

    def getSize(self):
        return self.size

    def getNbStations(self):
        if self.size == S:
            return 2
        return 4

    def getCenterDeck(self):
        return self.centerDeck

    def getneighbourhoodDeck(self):
        return self.neighbourhoodDeck

    def popDeck(self, deck_type):
        return self.centerDeck.pop(0) if deck_type == "center" else self.neighbourhoodDeck.pop(0)

    def putBackToDeck(self, deck_type, structure_type):
        if deck_type == "center": self.centerDeck.append(structure_type)
        if deck_type == "neighbourhood": self.neighbourhoodDeck.append(structure_type)
