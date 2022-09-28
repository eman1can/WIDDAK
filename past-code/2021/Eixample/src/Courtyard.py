from House import House
from Structure import Structure


class Courtyard(House):

    def _getStructureFiles(self):
        self.structures['courtyard'] = Structure.getStructuresInDir('courtyard')

    def _getStructure(self, structureType) -> Structure:
        return Structure(
            self.rng.choice(self.structures['courtyard']),
            rotation=self.rotation,
            rotateAroundCenter=True
        )

    def place(self):
        self.bottomStructure.setPosition(x=self.x, y=self.y, z=self.z)
        self.bottomStructure.place()
