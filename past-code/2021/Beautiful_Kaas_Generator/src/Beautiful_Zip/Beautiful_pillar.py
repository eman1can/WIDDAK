import utilityFunctions as utilityFunctions
from pymclevel import biome_types

# Information visible in mcedit, can be used for user-input
inputs = (
	("Settlement Generator", "label"),
	("Creators: me", "label")
	)

# Start of the Generation script
#  @ level: Minecraft world
#  @ box: selected box by mcedit
#  @ options: user defined inputs from mcedit
def perform(level, box, options):
	for i in range(0, 100):
		utilityFunctions.setBlock(level, (4,0), 0, i, 0)
	print biome_types.biome_types[level.biomeAt(0,0)]