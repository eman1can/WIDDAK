# Generates a beautiful settlement given a level and box

from numpy.lib.function_base import place
import utilityFunctions as utility
import numpy as np
import random
import math
import Beautiful_settings as settings

from Beautiful_edges import smoothen_edges
from Beautiful_meta_analysis import get_height_map, get_biome_map, get_surface_type_map
from Beautiful_starting_point import find_starting_point
from Beautiful_terraforming import flatten_box
from Beautiful_house import place_house
from Beautiful_bridge import place_bridges
from Beautiful_sign import place_vector


inputs = (
	("Beautiful Settlement Generator", "label"),
	("Creators: Koen, Elin, Tim, Sem, Jerryyyyyyyy", "label")
	)

def bully_smallest(lst, max_small):
    potentials = []
    for i in range(len(lst)):
        if lst[i] < max_small:
            for _ in range(max_small - lst[i]):
                potentials.append(i)
    
    if len(potentials) == 0:
        return False

    bullied = random.randint(0, len(potentials) - 1)
    lst[potentials[bullied]] += 1
    return True

def partition(total, min_part, max_part):
    old_total = total 
    while(total != 0):
        total = old_total
        partit = []
        while total > 10:
            rng = random.randint(min_part, max_part)
            total -= rng
            partit.append(rng)

        if total > 5:
            partit.append(total)
            total = 0

        else:
            patience = 5
            bullied = True
            while (total != 0 and bullied and patience > 0):
                bullied = bully_smallest(partit, 7)
                if bullied:
                    total -= 1
                patience -= 1
            #end while
        #end else
    #end while
    return partit

def building_size(width, length):
  cutoff = 66
  area = width*length
  height = 4 if area < cutoff else 5
  
  averea = np.sqrt(area)
  
  min_floors = max (1, int(averea / 3.5))
  max_floors = min (4, int(averea / 2.2))

  no_floors = random.randint(min_floors, max_floors)
  
  return height, no_floors

# Stores data about one building
class Building:
  def __init__(self, P, length, width, front, multiple):
    self.P = P
    self.length = length
    self.width = width
    self.front = front  # North, east, south, west
    self.multiple = multiple  # Is the plot for multiple or one building?


# Create settlement
class Settlement:
  def __init__(self, level, box):
    self.level = level
    self.box = box

    # Radius of outer and inner circles, forming the gear-shape 
    self.outer_r = random.randint(settings.MIN_OUTER, settings.MAX_OUTER)
    self.inner_r = random.randint(settings.MIN_INNER, settings.MAX_INNER)

    self.box_origin_height = self.box.origin[1]  # Height of origin block in box

    self.height_map = get_height_map(self.level, self.box)  # Relative height map of given box
    self.biome_map = get_biome_map(self.level, self.box)
    self.surface_map = get_surface_type_map(self.level, self.box)

    # Absolute centerpoint of settlement (WORLD)
    try:
      self.center_world = find_starting_point(self.box, "disk", settings.MAX_OUTER, self.height_map, self.surface_map, self.biome_map)
      print "Building village at: (x,z) = " 
      print self.center_world
      place_vector(level, self.center_world[0], 100, self.center_world[1])
      place_vector(level, self.center_world[0], 150, self.center_world[1])
      place_vector(level, self.center_world[0], 200, self.center_world[1])
    except ValueError:
      self.center_world = find_starting_point(self.box, "disk", settings.MAX_OUTER, self.height_map, self.surface_map, self.biome_map, plains=False)

    # Relative centerpoint of settlement (BOX)
    self.x_center_box = self.center_world[0] - self.box.minx
    self.z_center_box = self.center_world[1] - self.box.minz
  
    # Meta information
    self.buildings = []  # Plots of the buildings
    self.max_radius = []
    self.water = np.zeros_like(self.height_map, dtype=bool)   # Denotes where the canals are
    self.inner_canals = np.zeros_like(self.height_map, dtype=bool)
    self.domain = np.zeros_like(self.height_map, dtype=bool)  # Edge of settlement
    self.doors = [] #list of all door locations

  
  # Returns whether a block is in the given set
  def __is_element_of(self, block_set, block):
    for i in range(len(block_set)):
      if block == block_set[i][0]:  # Its a match!
        return True
    return False

  
  # Returns a random block from the given set
  def __get_element_of(self, block_set):
    return block_set[random.randrange(0, len(block_set))]


  # Check whether given (x,z) is in the box
  def __in_box(self, x, z):
    if not 0 <= x < self.box.width:
      return False
    if not 0 <= z < self.box.length:
      return False
    return True


  # Place a block, given the (x,y,z) coordinates of the box
  def __place_block(self, block, x, y, z):
    # Translate box-coordinates to the world coordinates
    world_x = x + self.box.minx
    world_y = y - 1
    world_z = z + self.box.minz

    utility.setBlock(self.level, block, world_x, world_y, world_z)  # Place block
  
  
  # Given box-coordinates (x,z), place block on top
  def __place_block_on_top(self, block, x, z):
    for y in range(self.box.maxy, self.box.miny):
      if not self.__get_block(x, y, z) == settings.AIR[0]:
        self.__place_block(block, x, y+1, z)


  # Place a grid of 3x3 blocks at given (x,z)
  def __place_grid(self, block, x, z, y_offset):
    for i in range(-1, 2):
      for j in range(-1, 2):
        if self.__in_box(x+i, z+j):
          y = self.__get_height(x+i, z+j) + y_offset
          self.__place_block(block, x+i, y, z+j)
          

  # Get absolute height at point (x,z)
  def __get_height(self, x, z):
    return self.box_origin_height + self.height_map[x][z]


  # Get block at box-coordinates (x,y,z)
  def __get_block(self, x, y, z):
    # Translate box-coordinates to the world coordinates
    world_x = x + self.box.minx
    world_y = y - 1
    world_z = z + self.box.minz

    return self.level.blockAt(world_x, world_y, world_z)


  # Get the first non-empty block, starting at box.maxy
  def __get_first_non_empty(self, x, z):
    for y in range(self.box.maxy, self.box.miny, -1):
      block = self.__get_block(x, y, z)
      if not block == settings.AIR[0]:
        return block
    
    return block  # Should never come here


  # Update the water-np-array
  def __update_water(self, x, z):
    for i in range(-1, 2):
      for j in range(-1, 2):
        if self.__in_box(x+i, z+j):
          self.water[x+i][z+j] = True   # Update where the canals are located

  # Update the water-np-array
  def __update_inner_canals(self, x, z):
    for i in range(-1, 2):
      for j in range(-1, 2):
        if self.__in_box(x+i, z+j):
          self.inner_canals[x+i][z+j] = True   # Update where the canals are located


  # Flatten area where the settlement will be
  def __flatten(self):
    values, counts = np.unique(self.height_map.flatten(), return_counts=True)  # Compute mode
    mode_height = values[np.argmax(counts)]
    y_level = mode_height + self.box_origin_height  # Mode of height map
    for r in range(1, self.outer_r+1):
      for alpha in range(0,360):
        x = int(self.x_center_box + r * math.cos(math.pi*alpha/180))
        z = int(self.z_center_box + r * math.sin(math.pi*alpha/180))
        
        for i in range(-1, 2):
          for j in range(-1, 2):
            if not self.__in_box(x+i, z+j):
              continue
            for y in range(self.box.miny, self.box.maxy):
              if y <= y_level:
                self.__place_block(settings.GRASS, x+i, y, z+j)
              else:
                self.__place_block(settings.AIR, x+i, y, z+j)
            
            self.height_map[x+i][z+j] = y_level - self.box_origin_height  # Update height map due to flattening


  # Generate canal from P0 to P1
  def __generate_canal(self, P0, P1):
    lst = utility.raytrace(P0, P1)
    for block in lst:
      self.__place_grid(settings.WATER, block[0], block[2], 0)
      self.__place_grid(settings.AIR, block[0], block[2], 1)
      self.__update_water(block[0], block[2])
      self.__update_inner_canals(block[0], block[2])
    
      y = self.__get_height(block[0], block[2])+2
      if self.__is_element_of(settings.OUTER_WALL, self.__get_block(block[0], y, block[2])):
        self.__place_grid(settings.WATER_GATE, block[0], block[2], 2)

        
  # Generate inner canals from P1 and P2 to center, then to P0
  def __generate_inner_canals(self, P0, P1, P2):
    cross_x = self.x_center_box+random.randint(-settings.OFFSET_CROSSPOINT, settings.OFFSET_CROSSPOINT)
    cross_z = self.z_center_box+random.randint(-settings.OFFSET_CROSSPOINT, settings.OFFSET_CROSSPOINT)
    crosspoint = (cross_x, self.__get_height(cross_x, cross_z), cross_z)
    
    self.__generate_canal(P1, crosspoint)
    self.__generate_canal(P2, crosspoint)
    self.__generate_canal(P0, crosspoint)


  # Update domain map; 1 = belongs to settlement
  def __update_domain(self, x, z):
    for i in range(-1, 2):
      for j in range(-1, 2):
        if self.__in_box(x+i, z+j):
          self.domain[x+i][z+j] = 1
  

  # Generate canals surrounding the settlement, has a gear-like shape
  # Also preparations for the three smaller canals
  def __generate_canals(self):
    length = 0   # Current length of a gear-segment
    outer = bool(random.randint(0,1))  # Start with inner/outer part
    init_outer = outer  # Save value of first outer

    # Angle at which the inner canal starts
    R0 = random.randint(0, settings.MAX_L_INNER)  # Left inner canal
    R1 = random.randint(settings.MIN_T_INNER, settings.MAX_T_INNER)  # Top inner canal
    R2 = random.randint(settings.MIN_B_INNER, settings.MAX_B_INNER)  # Bottom inner canal

    # Generate canals
    for alpha in range(0, 360):
      x_outer = int(self.x_center_box + self.outer_r * math.cos(math.pi*alpha/180))
      z_outer = int(self.z_center_box + self.outer_r * math.sin(math.pi*alpha/180))
      y_outer = self.__get_height(x_outer, z_outer)

      x_inner = int(self.x_center_box + self.inner_r * math.cos(math.pi*alpha/180))
      z_inner = int(self.z_center_box + self.inner_r * math.sin(math.pi*alpha/180))
      y_inner = self.__get_height(x_inner, z_inner)

      # Switch between inner and outer circle
      if length >= settings.MIN_LENGTH_C and 360-alpha > settings.MIN_LENGTH_C and random.uniform(0,1) <= settings.P_SWITCH:
        outer = not outer
        length = 0

        # Connect outer and inner parts
        lst = utility.raytrace((x_outer, y_outer, z_outer), (x_inner, y_inner, z_inner))
        for block in lst:
          self.__place_grid(settings.WATER, block[0], block[2], 0)
          self.__update_water(block[0], block[2])
      
      if outer:
        self.__place_grid(settings.WATER, x_outer, z_outer, 0)
        self.__update_water(x_outer, z_outer)
      else:
        self.__place_grid(settings.WATER, x_inner, z_inner, 0)
        self.__update_water(x_inner, z_inner)

      # Record points from which there will be canals within the gear shape
      if alpha == R0:
        P0 = (x_outer, y_outer, z_outer) if outer else (x_inner, y_inner, z_inner)
      elif alpha == R1:
        P1 = (x_outer, y_outer, z_outer) if outer else (x_inner, y_inner, z_inner)
      elif alpha == R2:
        P2 = (x_outer, y_outer, z_outer) if outer else (x_inner, y_inner, z_inner)

      length += 1
    
    # Connect ends of canals if current is not the same as the initial
    if not outer == init_outer:
      lst = utility.raytrace((x_outer, y_outer, z_outer), (x_inner, y_inner, z_inner))
      for block in lst:
        self.__place_grid(settings.WATER, block[0], block[2], 0)
        self.__update_water(block[0], block[2])

    return P0, P1, P2


  # Count number of water blocks surrounding the given coordinates
  # Grid: 5x5
  def __count_water(self, x, z):
    count = 0
    for i in range(-2, 3):
      for j in range(-2, 3):
        if i == 0 and j == 0:
          continue
        if self.__in_box(x+i, z+j):
          y = self.__get_height(x+i, z+j)
          if self.__get_block(x+i, y, z+j) == settings.WATER[0]:
            count += 1
    return count


  # Place wall, starting at (x,y,z)
  def __place_wall(self, x, y, z):
    L = settings.LEN_WALL + 1 if random.uniform(0,1) >= 0.5 else settings.LEN_WALL
    for l in range(L):
      self.__place_block(self.__get_element_of(settings.OUTER_WALL), x, y+l, z)
    self.__place_block(settings.AIR, x, y+settings.LEN_WALL+1, z)
    

  # Generates the foundation of the settlement and adds walls surrounding it
  # Outer_r is necessary to know how far to look
  def __foundation_and_walls(self):
    self.max_radius = np.full(360, self.outer_r, dtype=int)  # Max radius at which water is found per alpha

    for r in range(1, self.outer_r):
      for alpha in range(0, 360):     
        x = int(self.x_center_box + r * math.cos(math.pi*alpha/180))
        z = int(self.z_center_box + r * math.sin(math.pi*alpha/180))

        self.__update_domain(x, z)

        if r > self.max_radius[alpha]:  # Skip, water found
          continue
        # Manual placement of 3x3 grid
        for i in range(-1, 2):
          for j in range(-1, 2):
            if not self.__in_box(x+i, z+j):
              continue
            y = self.__get_height(x+i, z+j)
            if not self.__get_block(x+i, y, z+j) == settings.WATER[0]:
              if self.__count_water(x+i, z+j) > 0 and not self.__is_element_of(settings.OUTER_WALL, self.__get_block(x+i, y, z+j)):  # Create wall at (x+i,z+j)
                self.__place_wall(x+i, y, z+j)
              else:  # Foundation floor
                self.__place_block(self.__get_element_of(settings.ROAD), x+i, y, z+j)

        if self.__get_block(x, self.__get_height(x, z), z) == settings.WATER[0]:
          self.max_radius[alpha] = r  # Inner ring found for current alpha, update max_radius
        

  # Check whether there is a water gate nearby the given block, if so return True
  def __water_gate(self, x, y, z):
    for dx in range(-5, 6):
      for dy in range(-5, 6):
        for dz in range(-5, 6):
          if self.__in_box(x+dx, z+dz):
            if self.__get_block(x+dx, y+dy, z+dz) == settings.WATER_GATE[0]:
              return True
    return False  # No water gate found
  

  # Check whether current spot is suitable for an entrance
  # Entrances should be on the inner ring of the wall and not near water gates
  def __is_suitable(self, alpha):
    for i in range(-8, 9):
      if 0 <= alpha + i < 360:  # Should be in array self.max_radius
        x = int(self.x_center_box + self.inner_r * math.cos(math.pi*(alpha+i)/180))
        z = int(self.z_center_box + self.inner_r * math.sin(math.pi*(alpha+i)/180))
        y = self.__get_height(x, z)

        if self.max_radius[alpha+i] > self.inner_r or self.__water_gate(x, y+2, z):
          return False
    return True
  

  # Generate entrances into the outer walls, but only on the inner_r radius
  def __entrances(self):
    curr_len = settings.MIN_DIST_ENTRANCE-10

    for alpha in range(0, 360):
      if self.__is_suitable(alpha):  # Suitable spot for an entrance
        if curr_len >= settings.MIN_DIST_ENTRANCE and random.randint(0,1) <= settings.P_ENTRANCE:  # Enough distance between each entrance
          for r in range(1, self.inner_r+3):
            x = int(self.x_center_box + r * math.cos(math.pi*alpha/180))
            z = int(self.z_center_box + r * math.sin(math.pi*alpha/180))

            self.__place_grid(settings.AIR, x, z, 1)   # Make gap into the wall
            self.__place_grid(settings.AIR, x, z, 2)
            self.__place_grid(settings.AIR, x, z, 3)
            self.__place_grid(settings.AIR, x, z, 4)

          # Create bridge from entrance to the outside
          for r in range(self.inner_r-3, self.inner_r+4):
            x = int(self.x_center_box + r * math.cos(math.pi*alpha/180))
            z = int(self.z_center_box + r * math.sin(math.pi*alpha/180))

            self.__place_grid(settings.OUTER_BRIDGE, x, z, 1)   # Make gap into the wall

          curr_len = 0
      curr_len += 1


  # Check if space between points P1 and P2 is available
  # Available -> no buildings
  def __available(self, P1, P2):
    for x in range(P1[0], P2[0]):
      for z in range(P1[1], P2[1]):
        if not self.__is_element_of(settings.ROAD, self.__get_first_non_empty(x, z)) or \
           not self.__get_block(x, self.__get_height(x,z)+1, z) == settings.AIR[0]:
          return False
    return True


  # Compute number of free blocks in every direction around building
  # Returns optimal direction
  # If the plot is for multiple buildings (multiple=True)
  def __compute_space(self, building, multiple):
    P1_x, P1_y, P1_z = building[0][0], building[0][1], building[0][2]
    width, length = building[1][0], building[1][1]

    space = np.zeros(4, dtype=int)  # Four counters, for each direction
    indices = range(4)

    along_x = width > length  # Is the plot for the multiple buildings along the x-axis?
                              # Only the long side of the plot should be checked for canals (since it will be multiple buildings)

    for x in range(P1_x-3, P1_x+width+3):
      for z in range(P1_z-3, P1_z+length+3):
        if not self.__in_box(x, z):
          continue
        
        y = self.__get_height(x, z)
        block = self.__get_block(x, y, z)

        if not P1_x <= x < P1_x+width:
          if x < P1_x and (self.__is_element_of(settings.ROAD, block) or block == settings.WATER[0]):  # EAST
            space[0] += 1
            if block == settings.WATER[0] and (not multiple or not along_x):  # Point towards canal
              space[0] += settings.CANAL_VALUE
          elif x > P1_x+width-1 and (self.__is_element_of(settings.ROAD, block) or block == settings.WATER[0]):  # WEST
            space[3] += 1
            if block == settings.WATER[0] and (not multiple or not along_x):  # Point towards canal
              space[3] += settings.CANAL_VALUE
        if not P1_z <= z < P1_z+length:
          if z < P1_z and (self.__is_element_of(settings.ROAD, block) or block == settings.WATER[0]):  # SOUTH
            space[2] += 1
            if block == settings.WATER[0] and (not multiple or along_x):  # Point towards canal
              space[2] += settings.CANAL_VALUE
          elif z > P1_z+length-1 and (self.__is_element_of(settings.ROAD, block) or block == settings.WATER[0]):  # NORTH
            space[1] += 1
            if block == settings.WATER[0] and (not multiple or along_x):  # Point towards canal
              space[1] += settings.CANAL_VALUE
    
    # If multiple indices have max value, shuffle indices and space with same seed
    R = random.randint(0, 10000)  # Create random seed
    random.seed(R)
    random.shuffle(space)
    random.seed(R)
    random.shuffle(indices)
    return indices[np.argmax(space)]


  # Determine front of every building based on space around it
  # Also creates a new Building object, storing all necessary data
  # If multiple = True, then the plot is for multiple buildings
  def __determine_front(self, temp, multiple):
    for building in temp:      
      i = self.__compute_space(building, multiple)

      # TODO: remove =====================================================
      P1_x, P1_y, P1_z = building[0][0], building[0][1], building[0][2]
      length, width = building[1][0], building[1][1]
      if i == 0:    # WEST
        for z in range(0, width):
          y = self.__get_height(P1_x, P1_z+z)
          self.__place_block(settings.DIAMOND, P1_x, y, P1_z+z)
      elif i == 1:  # SOUTH
        for x in range(0, length):
          y = self.__get_height(P1_x+x, P1_z+width+1)
          self.__place_block(settings.DIAMOND, P1_x+x, y, P1_z+width-1)
      elif i == 2:  # NORTH
        for x in range(0, length):
          y = self.__get_height(P1_x+x, P1_z)
          self.__place_block(settings.DIAMOND, P1_x+x, y, P1_z)
      elif i == 3:  # EAST
        for z in range(0, width):
          y = self.__get_height(P1_x+length-1, P1_z+z)
          self.__place_block(settings.DIAMOND, P1_x+length-1, y, P1_z+z)
      # ==================================================================
      
      # Convert i to correct format for building
      if i == 0:    # WEST
        i = 1
      elif i == 1:  # SOUTH
        i = 2
      elif i == 2:  # NORTH
        i = 0
      else:         # EAST
        i = 3

      pos = (P1_x+self.box.minx, P1_y-1, P1_z+self.box.minz)
      self.buildings.append(Building(pos, width, length, i, multiple))  # Add new building


  # Create large plots, each containing multiple buildings
  # The plots are along one axis, and consequently the front can only be on two sides (along the selected axis)
  def __place_large_plots(self):
    temp = []  # Temporal storage of buildings

    for r in range(0, self.outer_r):
      for alpha in range(0, 360):
        if r > self.max_radius[alpha]:  # Skip, edge found
          continue
        
        x = int(self.x_center_box + r * math.cos(math.pi*alpha/180))
        z = int(self.z_center_box + r * math.sin(math.pi*alpha/180))

        attempt = 0
        while attempt < 2:  # Two attempts: 1 -> along x-axis | 2 -> along z-axis
          if attempt == 0:    # Along x-axis
            width_plot = random.randint(settings.MIN_WIDTH_MULT, settings.MAX_WIDTH_MULT)   # X
            length_plot = random.randint(settings.MIN_DEPTH, settings.MAX_DEPTH)   # Z
          elif attempt == 1:  # Along z-axis
            width_plot = random.randint(settings.MIN_DEPTH, settings.MAX_DEPTH)    # X
            length_plot = random.randint(settings.MIN_WIDTH_MULT, settings.MAX_WIDTH_MULT)  # Z

          # Try plot
          if self.__available((x-2, z-2), (x+width_plot+2, z+length_plot+2)):
            y = self.__get_height(x,z)
            for i in range(x, x+width_plot):  # Mark plot
              for j in range(z, z+length_plot):
                self.__place_block((35,12), i, self.__get_height(i,j), j)
            temp.append( [(x, y, z), (width_plot, length_plot)] )
            break
          
          attempt += 1
    
    self.__determine_front(temp, True)
  

  # Create small plots on which the small buildings can be generated
  def __place_small_plots(self):
    temp = []  # Temporal storage of buildings

    for r in range(0, self.outer_r):
      for alpha in range(0, 360):
        if r > self.max_radius[alpha]:  # Skip, edge found
          continue
        
        x = int(self.x_center_box + r * math.cos(math.pi*alpha/180))
        z = int(self.z_center_box + r * math.sin(math.pi*alpha/180))

        width_plot = random.randint(settings.MIN_WIDTH, settings.MAX_WIDTH)     # X
        length_plot = random.randint(settings.MIN_LENGTH, settings.MAX_LENGTH)  # Z

        if self.__available((x-2, z-2), (x+width_plot+2, z+length_plot+2)):
          if random.uniform(0,1) <= settings.P_PLOT:  # Probability to create plot
            y = self.__get_height(x,z)
            for i in range(x, x+width_plot):  # Mark plot
              for j in range(z, z+length_plot):
                self.__place_block((35,12), i, self.__get_height(i,j), j)
            temp.append( [(x, y, z), (width_plot, length_plot)] )
    
    self.__determine_front(temp, False)
  

  # Generate a building on top of each plot
  def __generate_buildings(self):
    for building in self.buildings:
      if building.multiple == True:
        if building.width > building.length:
          partit = partition(building.width, 5, 10)
          cum_p = 0
          for p in partit:
            base = (building.P[0] + cum_p, building.P[1], building.P[2])
            cum_p += p
            facade_type = random.randint(0, 2)
            h, n = building_size(p, building.length)
            door = place_house(self.level, p, h, building.length, base, building.front, n, facade_type)
        #end if
          
        else:
          partit = partition(building.length, 5, 10)
          cum_p = 0
          for p in partit:
            base = building.P
            base = (building.P[0], building.P[1], building.P[2] + cum_p)
            cum_p += p
            facade_type = random.randint(0, 2)
            h, n = building_size(p, building.width)
            door = place_house(self.level, p, h, building.width, base, building.front, n, facade_type)
        #end else
      #end if multiple
      else:
        facade_type = random.randint(0, 2)
        h, n = building_size(building.width, building.length)
        if building.front % 2 == 0:
          door = place_house(self.level, building.width, h, building.length, building.P, building.front, n, facade_type)
        else:
          door = place_house(self.level, building.length, h, building.width, building.P, building.front, n, facade_type)
      door[0] -= self.box.minx
      door[1] -= self.box.minz
      self.doors.append(door)
    #end for buildings
    self.doors = np.array(self.doors)


  # Check whether a 3x3 grid is available and that there is no light
  # in its NxN grid
  def __street_light(self, x, z):
    for i in range(-settings.SPARSITY, settings.SPARSITY+1):
      for j in range(-settings.SPARSITY, settings.SPARSITY+1):
        if not self.__in_box(x+i, z+j):
          continue
        y = self.__get_height(x+i, z+j)

        # Check if 3x3 grid is available
        if i in range(-1, 2) and j in range(-1, 2):
          if not self.__get_block(x+i, y+1, z+j) == settings.AIR[0]:
            return False
          if not self.__is_element_of(settings.ROAD, self.__get_block(x+i, y, z+j)):
            return False
        
        # Check for nearby street lights
        if self.__get_block(x+i, y+1, z+j) == settings.POLE[0]:
          return False
    return True


  # Place a street light at (x, z)
  def __place_street_light(self, x, z):
    y = self.__get_height(x, z)
    for i in range(settings.LEN_POLE):
      self.__place_block(settings.POLE, x, y+i+1, z)
    self.__place_block(settings.LIGHT_SOURCE, x, y+settings.LEN_POLE+1, z)


  # Generate street lights with redstone lamp + light sensor
  # They automatically turn on when it is dark
  def __generate_street_light(self):
    for r in range(1, self.outer_r):
      for alpha in range(0, 360):
        x = int(self.x_center_box + r * math.cos(math.pi*alpha/180))
        z = int(self.z_center_box + r * math.sin(math.pi*alpha/180))
        if self.__street_light(x, z):
          self.__place_street_light(x, z)
          alpha += 20  # Make sure there is enough space between street lights


  # Lower water level by one block to make it lower that the roads
  def __lower_water_level(self):
    for x in range(self.water.shape[0]):
      for z in range(self.water.shape[1]):
        if self.water[x][z]:  # Canal location
          y = self.__get_height(x, z)
          self.__place_block(settings.AIR, x, y, z)      # Remove water block
          self.__place_block(settings.WATER, x, y-1, z)  # Place water block one lower
          self.height_map[x][z] -= 1


  def __generate_bridges(self):
    place_bridges(self.level, self.box, self.inner_canals, self.doors)

  # Smoothen edges of the settlement using a gaussian filter)
  def __smoothen_edges(self):
    smoothen_edges(self.level, self.box, self.height_map, self.surface_map, self.domain,
                   self.x_center_box, self.z_center_box)


  # Determine whether there is space for a tree at (x,z)
  def __space_tree(self, x, z):
    for dx in range(-2, 3):
      for dz in range(-2, 3):
        y = self.__get_height(x+dx, z+dz)
        if not self.__get_block(x+dx, y+1, z+dz) == settings.AIR[0]:  # Space should be free
          return False
        if not self.__is_element_of(settings.ROAD, self.__get_block(x+dz, y, z+dz)):  # Tree cant be on edge
          return False
    return True


  # Recursively generate leaves on the tree
  def __generate_leave(self, x, y, z, depth):
    if depth >= len(settings.P_LEAVES) or not self.__get_block(x, y, z) == settings.AIR[0]:
      return  # Max recursive depth reached
    
    if random.randint(0,1) <= settings.P_LEAVES[depth]:  # Generate the leave
      self.__place_block(settings.LEAVE, x, y, z)

      self.__generate_leave(x+1, y, z, depth+1)
      self.__generate_leave(x-1, y, z, depth+1)

      self.__generate_leave(x, y+1, z, depth+1)
      self.__generate_leave(x, y-1, z, depth+1)

      self.__generate_leave(x, y, z+1, depth+1)
      self.__generate_leave(x, y, z-1, depth+1)

            
  # Generate tree at (x,z)
  def __generate_tree(self, x, z):
    y = self.__get_height(x, z) + 1
    height = random.randint(settings.MIN_HEIGHT_TREE, settings.MAX_HEIGHT_TREE)

    # Place logs of tree
    for i in range(height):
      self.__place_block(settings.LOG, x, y+i, z)

    # Recursively place leaves
    self.__generate_leave(x, y+height, z, 0)


  # Generate trees, bushes and grass in the settlement
  def __generate_greenery(self):
    for r in range(1, self.outer_r):
      for alpha in range(0, 360):
        if r > self.max_radius[alpha]:  # Skip
          continue
        
        x = int(self.x_center_box + r * math.cos(math.pi*alpha/180))
        z = int(self.z_center_box + r * math.sin(math.pi*alpha/180))
        if not self.water[x][z] and self.__space_tree(x, z) and random.uniform(0,1) <= settings.P_TREE:
          self.__place_block(settings.DIRT, x, self.__get_height(x, z), z)

          for dx in range(-1, 2):
            for dz in range(-1, 2):
              y = self.__get_height(x+dx, z+dz)
              if random.uniform(0,1) <= settings.P_DIRT and self.__is_element_of(settings.ROAD, self.__get_block(x+dz, y, z+dz)):
                self.__place_block(settings.DIRT, x+dx, y, z+dz)
                self.__place_block(settings.BUSH, x+dx, y+1, z+dz)

          self.__generate_tree(x, z)
          alpha += 20  # Make sure that there is sufficient space between every tree


  # EASTER EGG: generate the three stones (blue, red, white) of Leiden
  def __three_stones(self):
    pos_loc = []
    for x in range(self.domain.shape[0]):
      for z in range(self.domain.shape[1]):
        if self.domain[x][z] and not self.water[x][z]:  # Should be inside the settlement
          y = self.__get_height(x, z)
          if self.__is_element_of(settings.ROAD, self.__get_block(x, y, z)):
            pos_loc.append((x,y,z))  # Possible location for the stones
    
    loc = random.sample(pos_loc, k=3)  # 3 stones, so sample three locations
    
    self.__place_block(settings.RED_STONE, loc[0][0], loc[0][1], loc[0][2])    # RED stone
    self.__place_block(settings.BLUE_STONE, loc[1][0], loc[1][1], loc[1][2])   # BLUE stone
    self.__place_block(settings.WHITE_STONE, loc[2][0], loc[2][1], loc[2][2])  # WHITE stone


  # Generates the settlement
  def generate(self):
    print "\n==== Start generating the beautiful settlement! ===="

    print "Flatten area within the outer canals.."
    self.__flatten()  # Flatten area within outer canals -> every block becomes a grass block

    print "Generating the outer canals.."
    P0, P1, P2 = self.__generate_canals()  # Canals surrounding the settlement

    print "Generating foundation and outer walls.."
    self.__foundation_and_walls()  # Foundation of settlement + walls

    print "Generating entrances..."
    self.__entrances()  # Generating entrances in the outer walls

    print "Generating inner canals.."
    self.__generate_inner_canals(P0, P1, P2)  # Three inner canals

    print "Generating plots for the buildings.."
    self.__place_large_plots()  # Generate random big plots, each containing multiple buildings
    self.__place_small_plots()  # Generate random small plots, each containing one building

    print "Generating buildings.."
    self.__generate_buildings()

    print "Generating bridges.."
    self.__generate_bridges()  # Lower water level by one block

    print "Generating street lights.."
    self.__generate_street_light()  # Generate street lights

    print "Lower water level.."
    self.__lower_water_level()  # Lower water level by one block

    print "Generating greenery.."
    self.__generate_greenery()  # Generate trees, bushes and grass 

    print "Generating secret stuff.."
    self.__three_stones()   # The three stones of Leiden

    print "Smoothen edges.."
    self.__smoothen_edges() # Smoothen edges of the settlement

    print "\nGeneration completed!"

    print "Village built at: (x,z) = " 
    print self.center_world


# Starting point of generating the beautiful settlement
def perform(level, box, options):
  S = Settlement(level, box)
  S.generate()