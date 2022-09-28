# Name to display in MCEdit filter menu

import logging
from time import gmtime, strftime, time

from building_seeding import VillageSkeleton, BuildingType
from building_seeding.village_skeleton import CityBlock
from settlement import Settlement
from terrain.maps import Maps
from pymclevel import BoundingBox, MCLevel
from utils import TransformBox, Point2D

displayName = "Masked Parcels test"
# Dictionary representing different options
inputs = ()


def perform(level, box, options):
    # type: (MCLevel, BoundingBox, dict) -> None
    t0 = time()
    print("Hello Settlers!")
    box = TransformBox(box)
    maps = Maps(level, box)
    settlement = Settlement(maps)
    settlement.init_town_center()   # define town settlement as point close to roads and geometric center of the box
    W, L = box.width, box.length

    # create road cycle
    p1, p2, p3, p4 = Point2D(int(.1*W), int(.2*L)), Point2D(int(.8*W), int(.1*L)), Point2D(int(.8*W), int(.9*L)), Point2D(int(.3*W), int(.9*L))
    maps.road_network.create_road(p1, p2)
    maps.road_network.connect_to_network(p3)
    maps.road_network.connect_to_network(p4)
    maps.road_network.create_road(p1, p4)

    skeleton = VillageSkeleton('Flat_scenario', maps, settlement.town_center, settlement._parcels)

    city_block = CityBlock(maps.road_network.road_blocks, maps)
    block_parcel = city_block.parcels()
    skeleton.add_parcel(block_parcel, BuildingTypes.ghost)
    block_parcel.mark_as_obstacle(maps.obstacle_map)

    settlement._parcels.pop(0)
    settlement.define_parcels()     # define parcels around seeds
    settlement.generate(level, True)      # build buildings on parcels
