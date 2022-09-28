from abc import ABC

from utils import Point


class Map(ABC):
    def __init__(self, values):
        self._values = values

    @property
    def width(self):
        return self._values.shape[0]

    @property
    def length(self):
        return self._values.shape[1]

    def __getitem__(self, item):
        if isinstance(item, Point):
            return self._values[item.x, item.z]
        else:
            return self._values[item]
