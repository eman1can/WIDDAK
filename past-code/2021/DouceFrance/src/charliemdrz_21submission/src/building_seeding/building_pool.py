import logging
from enum import Enum
from typing import Dict

from numpy.random import choice

from building_seeding.building_encyclopedia import BUILDING_ENCYCLOPEDIA
from generation import CropGenerator, ProcHouseGenerator, WindmillGenerator
from generation.generators import Generator
from generation.plaza import PlazaGenerator
from parameters import AVERAGE_PARCEL_SIZE


class BuildingType(Enum):
    """
    All types of buildings. Holds generator for each type. At the generation step, new_instance is called to instantiate
    a new generator.
    """
    ghost = PlazaGenerator
    house = ProcHouseGenerator
    crop = CropGenerator
    windmill = WindmillGenerator

    def new_instance(self, box) -> Generator:
        return self.value(box)

    @property
    def generator(self):
        return self.value

    def __str__(self):
        return "Building type {}".format(self.name)


class BuildingPool:
    def __init__(self, exploitable_surface):
        self._building_count = 0  # type: int
        self._buildings_max = 0  # type: int
        self.__current_type: BuildingType = BuildingType.house
        self.__init_building_count(exploitable_surface)

    def __init_building_count(self, exploitable_surface):
        average_parcel_surface = AVERAGE_PARCEL_SIZE**2
        self._buildings_max = int((exploitable_surface / average_parcel_surface) ** .9)
        self._buildings_max = max(self._buildings_max, 1)
        # self._settlement_limit = min(self._settlement_limit, 50)
        # self.settlement_limit = geometric(1 / average_parcel_count)  # yielded values too high
        logging.info('New BuildingPool will generate {} parcels'.format(self._buildings_max))

    def __iter__(self):
        return self

    def __next__(self):
        """
        Pick randomly a building type in the pool
        Returns a BuildingType to build next
        -------

        """
        # first version, distribution based
        # if self.building_count < self.settlement_limit:
        #     self.building_count += 1
        #     norm = sum([v for v in self.building_types.values()])
        #     prob = [v / norm for v in self.building_types.values()]
        #     btype = choice(self.building_types.keys(), p=prob)
        #     return btype

        # second version, markov chain based:
        if 0 < self._building_count < self._buildings_max:
            transition_matrix = BUILDING_ENCYCLOPEDIA["Flat_scenario"]["markov"]
            transition_states = transition_matrix[self.__current_type.name]  # type: Dict[str, int]
            types = list(transition_states.keys())
            probs = transition_states.values()
            probs = [p / sum(probs) for p in probs]
            next_type = choice(types, p=probs)
            self.__current_type = BuildingType[next_type]
        elif self._building_count >= self._buildings_max:
            raise StopIteration

        self._building_count += 1
        return BuildingType(self.__current_type)

    @property
    def size(self):
        return self._buildings_max

    @property
    def count(self):
        return self._building_count
