MAX_LAMBDA = 30
MAX_ROAD_WIDTH = 7
MIN_ROAD_WIDTH = 3
MAX_WATER_EXPLORATION = 100
MAX_LAVA_EXPLORATION = 50
PARCEL_REUSE_ADVANTAGE = 2.5  # interest multiplying cost when evaluating a parcel type replacement
MAX_POND_EXPLORATION = 144  # should ideally be higher than the largest ponds to exterminate all of them

# Each bridge costs a initial cost + linear cost on length
BRIDGE_COST = 10
BRIDGE_UNIT_COST = 4

# buildings dimensions
MAX_HEIGHT = 10  # 12 -> max 3 floors
BUILDING_HEIGHT_SPREAD = 80  # at that distance from the center, buildings' height is a third of max height (1/e ~ .36)
AVERAGE_PARCEL_SIZE = 12
MIN_PARCEL_SIZE = 3
MIN_RATIO_SIDE = .5

# distances
MIN_DIST_TO_LAVA = 10
MIN_DIST_TO_OCEAN = 8
MIN_DIST_TO_RIVER = 4

# seeding
SEED_COUNT = 200
