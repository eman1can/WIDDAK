
import utilityFunctions as utilityFunctions
import math
import random
import numpy as np

inputs = (
	("Beautiful canals", "label"),
	("Creator: Jerry", "label")
	)

GROUND = (13,0)

# Place grid of 3x3
def place_block(level, block, x, y, z):
  # x-1
  utilityFunctions.setBlock(level, block, x, y, z-1)
  utilityFunctions.setBlock(level, block, x, y, z)
  utilityFunctions.setBlock(level, block, x, y, z+1)

  # x
  utilityFunctions.setBlock(level, block, x-1, y, z-1)
  utilityFunctions.setBlock(level, block, x-1, y, z)
  utilityFunctions.setBlock(level, block, x-1, y, z+1)

  # x+1
  utilityFunctions.setBlock(level, block, x+1, y, z-1)
  utilityFunctions.setBlock(level, block, x+1, y, z)
  utilityFunctions.setBlock(level, block, x+1, y, z+1)


# Outer canal of settlement, has a gear-shape
def canal(level, origin, outer_r, inner_r):
  x_origin, y_origin, z_origin = origin[0], origin[1], origin[2]
  length, min_length = 0, 30
  outer = True

  R0, R1, R2 = random.randint(0, 10), random.randint(130, 160), random.randint(200, 230)

  for alpha in range(0, 360):
    x_outer = int(x_origin + outer_r * math.cos(math.pi*alpha/180))
    z_outer = int(z_origin + outer_r * math.sin(math.pi*alpha/180))

    x_inner = int(x_origin + inner_r * math.cos(math.pi*alpha/180))
    z_inner = int(z_origin + inner_r * math.sin(math.pi*alpha/180))

    if length > min_length and 360-alpha > min_length and random.uniform(0,1) <= 0.4:  # Switch between outer/inner
      outer = not outer
      length = 0
      # Connect outer and inner parts
      lst = utilityFunctions.raytrace((x_outer, y_origin, z_outer), (x_inner, y_origin, z_inner))
      for block in lst:
        place_block(level, (9,0), block[0], y_origin, block[2])
    
    if outer:
      place_block(level, (9,0), x_outer, y_origin, z_outer)
    else:
      place_block(level, (9,0), x_inner, y_origin, z_inner)
    
    # Record the points from which there will be canals within the gear shape
    if alpha == R0:
      p0 = (x_outer, y_origin, z_outer) if outer else (x_inner, y_origin, z_inner)
    elif alpha == R1:
      p1 = (x_outer, y_origin, z_outer) if outer else (x_inner, y_origin, z_inner)
    elif alpha == R2:
      p2 = (x_outer, y_origin, z_outer) if outer else (x_inner, y_origin, z_inner)
    
    length += 1

  if not outer:  # Connect ends of canals if current is inner
    lst = utilityFunctions.raytrace((x_outer, y_origin, z_outer), (x_inner, y_origin, z_inner))
    for block in lst:
      place_block(level, (9,0), block[0], y_origin, block[2])
  
  return p0, p1, p2


# Count number of water blocks surrounding given block
def count_water(level, x, y, z):
  count = 0
  for i in range(-2, 3):
    for j in range(-2, 3):
      if i == 0 and j == 0:
        continue
      if level.blockAt(x+i, y, z+j) == 9:
        count += 1
  return count


# Create foundation ground and outer wall (borders with canals)
def foundation(level, x_origin, y_origin, z_origin, radius):
  max_radius = np.full(360, radius, dtype=int)

  for r in range(1, radius):
    for alpha in range(0, 360):
      if r > max_radius[alpha]:
        continue

      x = int(x_origin + r * math.cos(math.pi*alpha/180))
      z = int(z_origin + r * math.sin(math.pi*alpha/180))

      for i in range(-1, 2):
        for j in range(-1, 2):
          if not level.blockAt(x+i, y_origin, z+j) == 9:
            if count_water(level, x+i, y_origin, z+j) > 0:
              utilityFunctions.setBlock(level, (35,14), x+i, y_origin+1, z+j)
            else:
              utilityFunctions.setBlock(level, GROUND, x+i, y_origin, z+j)
      
      if level.blockAt(x, y_origin, z) == 9:  # Inner ring found for current alpha, update max_radius
        max_radius[alpha] = r


# Create canal between two points
def create_canal(level, p0, p1):
  blocks = utilityFunctions.raytrace(p0, p1)
  for block in blocks:
    place_block(level, (9,0), block[0], 3, block[2])
    place_block(level, (0,0), block[0], 4, block[2])


# Create inner canals from p1 and p2 to center, then to p0
def inner_canals(level, p0, p1, p2, origin):
  x_origin, y_origin, z_origin = origin[0], origin[1], origin[2]
  crosspoint = (x_origin+random.randint(-5,5), y_origin, z_origin+random.randint(-5,5))

  create_canal(level, p1, crosspoint)
  create_canal(level, p2, crosspoint)
  create_canal(level, p0, crosspoint)


# Check if space between points p1 and p2 is available
# Available -> no roads, no buildings
def available(level, p1, p2):
  for x in range(p1[0], p2[0]):
    for z in range(p1[2], p2[2]):
      if not level.blockAt(x, p1[1], z) == GROUND[0]:  # Not ground -> not empty
        return False
  return True


# Compute free blocks in every direction
def compute_space(level, building):
  p1_x, p1_y, p1_z = building[0][0], building[0][1], building[0][2]
  p2_x, p2_y, p2_z = building[1][0], building[1][1], building[1][2]
  
  space = np.zeros(4, dtype=int)

  for x in range(p1_x-3, p1_x+p2_x+3):
    for z in range(p1_z-3, p1_z+p2_z+3):
      block = level.blockAt(x, 3, z)
      if not p1_x <= x < p1_x+p2_x:
        if x < p1_x and (block == GROUND[0] or block == 9):
          space[0] += 1
          if block == 9:  # Point towards canal
            space[0] += 100
        elif x > p1_x+p2_x-1 and (block == GROUND[0] or block == 9):
          space[3] += 1
          if block == 9:  # Point towards canal
            space[3] += 100
      if not p1_z <= z < p1_z+p2_z:
        if z < p1_z and (block == GROUND[0] or block == 9):
          space[2] += 1
          if block == 9:  # Point towards canal
            space[2] += 100
        elif z > p1_z+p2_z-1 and (block == GROUND[0] or block == 9):
          space[1] += 1
          if block == 9:  # Point towards canal
            space[1] += 100
  
  indices = range(4)

  # If multiple indices have max value, shuffle indices and space with same seed
  R = random.randint(0,10000)  # Create random seed
  random.seed(R)
  random.shuffle(space)
  random.seed(R)
  random.shuffle(indices)

  return indices[np.argmax(space)]


# Determine front of every building based on the space around it
def determine_front(level, buildings):
  for building in buildings:
    p1_x, p1_y, p1_z = building[0][0], building[0][1], building[0][2]
    p2_x, p2_y, p2_z = building[1][0], building[1][1], building[1][2]

    i = compute_space(level, building)

    if i == 0:
      for z in range(0, p2_z):
        utilityFunctions.setBlock(level, (57,0), p1_x, 3, p1_z+z)
    elif i == 1:
      for x in range(0, p2_x):
        utilityFunctions.setBlock(level, (57,0), p1_x+x, 3, p1_z+p2_z-1)
    elif i == 2:
      for x in range(0, p2_x):
        utilityFunctions.setBlock(level, (57,0), p1_x+x, 3, p1_z)
    elif i == 3:
      for z in range(0, p2_z):
        utilityFunctions.setBlock(level, (57,0), p1_x+p2_x-1, 3, p1_z+z)


# Create plots for buildings
# TODO: now only works if origin = (0,3,0)
def place_plots(level, origin, radius):
  x_origin, y_origin, z_origin = origin[0], origin[1], origin[2]

  buildings = []

  for z in range(-1*radius, radius, 2):
    width_plot = random.randint(4, 8)
    for x in range(-1*radius, radius, 1):
      length_plot = random.randint(4, 8)
      if available(level, (x-1, y_origin, z-1), (x+length_plot+1, y_origin, z+width_plot+1)):
        if random.uniform(0,1) <= 0.7:  # Probability to create plot
          for i in range(x, x+length_plot):  # Mark plot
            for j in range(z, z+width_plot):
              utilityFunctions.setBlock(level, (35,12), i, y_origin, j)
          buildings.append([(x, y_origin, z), (length_plot, y_origin, width_plot)])

  determine_front(level, buildings)


def perform(level, box, options):
  p0, p1, p2 = canal(level, (0,3,0), 42, 35)  # Outer canal (gear shape)

  foundation(level, 0, 3, 0, 42)  # Create foundation ground (pathblocks)
                                  # Also creates outer wall

  inner_canals(level, p0, p1, p2, (0,3,0))  # Create inner canals from p1 and p2 to center, then to p0

  # Create plots inside canal
  place_plots(level, (0,3,0), 42)