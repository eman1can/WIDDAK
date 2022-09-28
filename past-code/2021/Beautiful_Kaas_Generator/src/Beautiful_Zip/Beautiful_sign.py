import utilityFunctions as utilityFunctions
#from pymclevel import entity
#from pymclevel import TAG_String
import random 
import numpy as np
# Information visible in mcedit, can be used for user-input
inputs = (
	("Settlement Generator", "label"),
	("Creators: Koen", "label")
	)

def place_vector(level, x, y, z):
    iron = (42, 0)
    gold = (41, 0)
    rich = (57, 0)

    r = 5.0

    x = float(x)
    z = float(z)
    lenght = np.sqrt(x*x + y*y) + 0.001#add to prevent div by zero

    x_dir = x/lenght
    z_dir = z/lenght

    utilityFunctions.setBlock(level, iron, 0, y, 0)
    utilityFunctions.setBlock(level, gold, int(r*x_dir), y, int(r*z_dir))
    utilityFunctions.setBlock(level, rich, int(r*2.0*x_dir), y, int(r*2.0*z_dir))


# Start of the Generation script
#  @ level: Minecraft world
#  @ box: selected box by mcedit
#  @ options: user defined inputs from mcedit
def perform(level, box, options):
    x_loc = "x = " + str(101)
    z_loc = "y = " + str(20)

    x = random.randint(100, 1000)
    z = random.randint(100, 1000)
    y0 = 100
    y1 = 150
    y2 = 200
    place_vector(level, x, 10, z)
    place_vector(level, x, y0, z)
    place_vector(level, x, y1, z)
    place_vector(level, x, y2, z)

    print x
    print z
'''
    for i in range(255, 0, -1):
	    if level.blockAt(0, i, 0) != 0:
              utilityFunctions.setBlock(level, (1,0), 0, i, 0)#turn to stone to prevent signs on water/lava/etc
              utilityFunctions.setBlock(level, (63,0), 0, i+1, 0)
              #sign_thing = 'Sign:(TAG_String("Village located at:"), x_loc, z_loc, TAG_String(''))'
              sign_thing = "Sign:(Village located at, " + x_loc + ", " + z_loc + ", .)"
              #sign_thing = TAG_String(sign_thing)
              entity.TileEntity.Create(sign_thing, (0, i+1, 0))
              
              break
'''