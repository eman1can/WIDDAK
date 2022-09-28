import utilityFunctions as utilityFunctions
from pymclevel import box as boundingBox
from pymclevel import materials
from copy import deepcopy

inputs = (
	("Deforestation of given box", "label"),
	("Creator: Jerry", "label")
	)

# =================================================
# Dimensions of all trees (x*z), excluding height:
#  - jungle (normal) -> 5*5
#  - jungle (big)    -> 16*16
#  - acacia          -> 12*12
#  - spruce (normal) -> 7*7
#  - spruce (big)    -> 10*10
#  - oak    (normal) -> 5*5
#  - oak    (big)    -> 13*13
#  - darkoak         -> 12*12
#  - birch           -> 5*5
# =================================================

MAX_REC_DEPTH=10  # Max width of naturally generated trees in Minecraft

# TODO: - Check if leaf is inside box?
#       - Make MAX_REC_DEPTH dependent on biome?

# Removes leaves recursively
def leave_removal(level, x, y, z, depth):
  # Limit the recursive depth
  if depth == MAX_REC_DEPTH or \
     not level.blockAt(x, y, z) == 18: # Only remove leaves
    return
  
  utilityFunctions.setBlock(level, (0,0), x, y, z) # Place air-block

  # Recursive calls
  leave_removal(level, x+1, y, z, depth+1)
  leave_removal(level, x-1, y, z, depth+1)
  leave_removal(level, x, y, z+1, depth+1)
  leave_removal(level, x, y, z-1, depth+1)
  leave_removal(level, x, y+1, z, depth+1)

# Remove a single tree
def remove_tree(level, loc, biome):
  # Travel downwards until end of log is reached
  step = boundingBox.Vector(0, 1, 0)
  block = level.blockAt(loc[0], loc[1]-1, loc[2])
  while block == 0 or block == 17 or block == 18: # Air-ID=0 | Wood-ID=17 | Leave-ID=18
    loc = loc.__sub__(step)
    block = level.blockAt(loc[0], loc[1]-1, loc[2])
  utilityFunctions.setBlock(level, (2,0), loc[0], loc[1]-1, loc[2]) # Dirt -> Grass

  # Remove tree by replacing its blocks with air-blocks
  while level.blockAt(loc[0], loc[1], loc[2]) == 17: # Log-block
    for dx in range(-1, 2):
      for dz in range(-1, 2):
        if level.blockAt(loc[0]+dx, loc[1], loc[2]+dz) == 18: # Check for leaves
          x, y, z = deepcopy(loc[0]), deepcopy(loc[1]), deepcopy(loc[2])
          leave_removal(level, x+dx, y, z+dz, 1)
    utilityFunctions.setBlock(level, (0,0), loc[0], loc[1], loc[2]) # Remove log
    loc = loc.__add__(step)

# Given a box, remove all trees within that box
def deforestation(level, box):
  tree_map = utilityFunctions.treeMap(level, box) # Column = x, Row = z

  # Search through given box for trees
  for z, row in enumerate(tree_map):
    for x, pos in enumerate(row):
      if not pos == 0: # Coordinates (x,z) contains a log-block
        loc = box.origin.__add__(boundingBox.Vector(x, box.height, z))
        remove_tree(level, loc, level.biomeAt(loc[0], loc[1]))

# Start of the Deforestation
# NOTE: at least one tree block should be within the given box
def perform(level, box, options):
  deforestation(level, box)
  