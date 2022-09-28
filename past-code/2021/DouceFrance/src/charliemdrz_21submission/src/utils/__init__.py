# Relevant generic imports throughout the project
from typing import List, Dict, Set, Iterable
from numpy import ndarray, full, zeros, array
from itertools import product
from time import time
from random import shuffle

from utils.pymclevel import *

from utils.misc_objects_functions import sym_range, pos_bound, bernouilli, get_project_path, argmin, mean
from utils.geometry_utils import Point, Direction, BuildArea, euclidean, manhattan, cardinal_directions, all_directions
from utils.geometry_utils import TransformBox
from utils.block_utils import BlockAPI, setBlock, water_blocks, lava_blocks, fillBlocks, clear_tree_at, connected_component, place_torch, ground_blocks, getBlockRelativeAt
import utils.parameters


X_ARRAY: ndarray = array([[x for z in range(BuildArea().length)] for x in range(BuildArea().width)])
Z_ARRAY: ndarray = array([[z for z in range(BuildArea().length)] for x in range(BuildArea().width)])
alpha = BlockAPI.blocks
