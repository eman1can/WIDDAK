from House import House
from Structure import Structure


class CornerHouse(House):

    def __init__(self, x=0, y=0, z=0, rotation=Structure.ROTATE_NORTH):
        self.bottomFloorDir = 'cornerHouseBottomFloor'
        self.floorDir = 'cornerHouseFloor'
        super().__init__(x, y, z, rotation)
