from Beautiful_Pallete import Pallete

P = Pallete()

# Contains settings for generating the settlement


# ==== Canal settings ====
MIN_LENGTH_C = 30  # Min length of each section of the gear-like shape

MAX_L_INNER = 2   # Angle between which the left inner canal should be

MIN_T_INNER = 200  # Angle between which the top inner canal should be
MAX_T_INNER = 230

MIN_B_INNER = 130  # Angle between which the bottom inner canal should be
MAX_B_INNER = 160

P_SWITCH = 0.4  # Probability to switch between inner and outer, when MIN_LENGTH is reached

OFFSET_CROSSPOINT = 5  # Maximum offset of the crosspoint of the three inner canals

# Radius of the outer and inner circles, forming the gear-shape
MIN_OUTER = 40
MAX_OUTER = 45
MIN_INNER = MIN_OUTER - 8
MAX_INNER = MIN_OUTER - 5

# Area outside the outer circle to smoothen,
SMOOTH_AREA = 15
SIGMA = 8

# ==== Plot generation settings ====
# PLOTS FOR ONE BUILDING
MIN_WIDTH = 5
MAX_WIDTH = 10
MIN_LENGTH = 5
MAX_LENGTH = 10

P_PLOT = 0.6  # Probability to place plot when it is available


# PLOTS FOR MULTIPLE BUILDINGS
MIN_DEPTH = 8
MAX_DEPTH = 10
MIN_WIDTH_MULT = 20
MAX_WIDTH_MULT = 35


CANAL_VALUE = 100  # Added value to direct the buildings nearby a canal to it


# ==== Street light specific ====
LEN_POLE = 4    # Length of street light pole
SPARSITY = 9    # Area (NxN) where at most one street light can be
LIGHT_SOURCE = (169,0)  # (89,0)

# ==== Outer wall specific ====
LEN_WALL = 7
P_ENTRANCE = 0.9  # Probability to generate an entrance in the outer wall
MIN_DIST_ENTRANCE = 100  # Minimum distance between two entrances, in terms of degrees in [0,360]


# ==== Greenery specific ====
MAX_HEIGHT_TREE = 8
MIN_HEIGHT_TREE = 4
P_LEAVES = [1.0, 1.0, 0.8, 0.8, 0.8]   # Probability at every recursive depth to generate leaves
P_DIRT = 0.3
P_TREE = 0.3   # Probability to generate tree


# ==== Block-specifications (with the exception of the buildings) ====
AIR = (0,0)
WATER = (9,0)
DIRT = (3,0)
GRASS = (2,0)
ROAD = [(1,0), (4,0), (98,0), (98,1), (98,2), P.andesite, P.polished_andesite]         # Grey blocks
OUTER_WALL = [(45,0), P.granite, P.polished_granite]  # Orange-ish blocks (bricks, granite)
POLE = (139,0)            # Cobblestone wall
WATER_GATE = (101,0)      # Iron bars
DIAMOND = (57,0)
OUTER_BRIDGE = (44,5)     # Stone brick slab

LOG = (17,0)
BUSH = (18,5)
LEAVE = (18,4)

RED_STONE = (152,0)       # Redstone block
BLUE_STONE = (22,0)       # LapisLazuli block
WHITE_STONE = (42,0)      # Block of iron