import utilityFunctions as U
import math as m
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
import Matrix
# All generator code was taken from the University Tsukuba TrainCity submission to the GDMC competition in 2020
# with only minor changes in two files
from Generators.Structures import Building, HouseLisa, Fountain, Farm, TowerLisa
from Helper import toolbox
#displayName = "Lisa..."

#inputs = (
#    ("Lisas house", False),
#    ("Type house", ("farm", "house", "fountain", "tower", "building", "pasture")),

#)

#def perform(level, box, options):
 #   if options["Lisas house"]:
  #      print(box.origin)
   #     print(box.minz, box.minx)
    #    make_empty(level, box)
     #   build_naive_house(level, box)
    #else:
     #   make_empty(level, box)

      #  build_traincity_structure(level, box, type=options["Type house"])

       # pass
        #build_settlement_house(level, box, options)
    #pass

def build_traincity_structure(level, box, type="house", orientation="O", door_suggestion=None):
    height = box.maxy - box.miny
    width = box.maxx - box.minx
    depth = box.maxz - box.minz
    matrix = Matrix.Matrix(level, box, height, width, depth)
    door_position = None
    if type == "farm":
        build_traincity_farm(height, width, depth, matrix)
    elif type == "fountain":
        make_empty(level, box)
        build_traincity_fountain(height, width, depth, matrix)
    elif type == "house":
        door_position = build_traincity_house(height, width, depth, matrix)
    elif type == "tower":
        height_map = [[0 for z in range(box.minz, box.maxz)] for x in range(box.minx, box.maxx)]
        build_traincity_tower(height_map, height, width, depth, matrix)
    elif type == "pasture":
        boxx = BoundingBox((box.minx-1, box.miny, box.minz-1), box.size + (2, 2, 2))
        make_empty(level, boxx)
        build_animal(level, box)
    else:
        build_traincity_house(height, width, depth, matrix, job=type)
    return door_position

def build_traincity_farm(height, width, depth, matrix):
    if height > 2 and width > 7 and depth > 7:
        Farm.generateFarm(matrix, "oak", 0, height, 1, width-1, 1, depth-1, None)
        matrix.updateWorld()
    else:
        print("The lot was too small to build a farm...")


def build_traincity_fountain(height, width, depth, matrix):
    if height > 15 and width > 16 and depth > 16:
        Fountain.generateFountain(matrix, 0, height-1, 0, width, 0, depth)
        matrix.updateWorld()
    else:
        print("The lot was too small to build a fountain...")


def build_traincity_house(height, width, depth, matrix, job=None):
    wood = "oak"
    wood_dict = {"cleric": "spruce", "crafter": "birch", "smith": "jungle", "enchanter": "dark_oak", "blacksmith": "acacia"}
    if job:
        wood = wood_dict[job]
    if height > 6 and width > 11 and depth > 11:
        door_position = HouseLisa.generateHouse(matrix, wood, 0, height-1, 2, width-2, 2, depth-2, job=job)
        matrix.updateWorld()
        return door_position
    else:
        print("The lot was too small to build a house...")

def build_traincity_building(height, width, depth, matrix):
    if height > 8 and width > 12 and depth > 12:
        Building.generateBuilding(matrix, 0, height-1, 1, width-1, 1, depth-1)
        matrix.updateWorld()

    else:
        print("The lot was too small to build an apartment building...")


def build_traincity_tower(height_map, height, width, depth, matrix):
    if height > 21 and width > 9 and depth > 9:
        TowerLisa.generateTower(matrix, 1, width-1, 1, depth-1, height_map)
        matrix.updateWorld()
    else:
        print("The lot was too small to build a tower...")


def make_empty(level, box):
    for x in xrange(box.minx, box.maxx):
        for z in xrange(box.minz, box.maxz):
            for y in xrange(box.miny, box.maxy):  # nested loops can be slow
                level.setBlockAt(x, y, z, 0)

def build_animal(level, box):
    fence = 85
    #if height > 2 and width > 7 and depth > 7:
    for x in range(box.minx, box.maxx):
        for z in [box.minz, box.maxz]:
            level.setBlockAt(x, box.miny, z, fence)
    for z in range(box.minz, box.maxz):
        for x in [box.minx, box.maxx]:
            level.setBlockAt(x, box.miny, z, fence)
    #level.setBlockAt(box.minx + 3, box.miny, box.minz +3, (383,90))
    U.setBlock(level, (383,90), box.minx + 3, box.miny, box.minz +3)

def build_bridge((point_1, point_2, height), level):
    wide = True
    print("building bridge")
    x_direction = point_1[1] == point_2[1]
    set = 0
    changing = 1
    if x_direction:
        set = 1
        changing = 0
    largest = point_1
    smallest = point_2
    if point_1[changing] < point_2[changing]:
        smallest = point_1
        largest = point_2
    if x_direction:
        U.setBlock(level, (53, 0), smallest[0], height+1, smallest[1])
        U.setBlock(level, (53, 1), largest[0], height+1, largest[1])
        if wide:
            U.setBlock(level, (53, 0), smallest[0], height + 1, smallest[1]+1)
            U.setBlock(level, (53, 1), largest[0], height + 1, largest[1]+1)
    else:
        U.setBlock(level, (53, 2), smallest[0], height+1, smallest[1])
        U.setBlock(level, (53, 3), largest[0], height+1, largest[1])
        if wide:
            U.setBlock(level, (53, 2), smallest[0]+1, height + 1, smallest[1])
            U.setBlock(level, (53, 3), largest[0]+1, height + 1, largest[1])
    set_value = smallest[set]
    for change in range(smallest[changing] + 1, largest[changing] ):
        if set == 0:
            level.setBlockAt(set_value, height+2, change, 5)
            if wide:
                level.setBlockAt(set_value+1, height+2, change, 5)
        else:
            level.setBlockAt(change, height + 2, set_value, 5)
            if wide:
                level.setBlockAt(change, height + 2, set_value+1, 5)
    return True

def build_wall(x_min, x_max, z_min, z_max, gate, level):
    z_axis = True
    if gate[2] == "z":
        z_axis = False
    for x in [x_min, x_max]:
        for z in range(z_min, z_max-1):
            y1 = toolbox.findTerrain(level, x, z, 1, 250)
            y2 = toolbox.findTerrain(level, x+1, z, 1, 250)
            for i in range(1, 6):
                level.setBlockAt(x, y1+i, z, 4)
                level.setBlockAt(x+1, y2 + i, z, 4)
            #print(z_axis, gate[0][0], x, gate[1][1], z)
            if z_axis and gate[0][0] == x and gate[1][1] == z and gate[1][1] < z_max - 3:
                print("make gate")
                if y1 == -1 or y2 == -1:
                    gate[0][1] = gate[0][1] + 1
                    gate[1][1] = gate[1][1] + 1
                else:
                    print("actually make gate")
                    print(z_axis, gate[0][0], x, gate[1][1], z)
                    U.setBlock(level, (64, 3), x, y1 +1, z - 1)
                    U.setBlock(level, (64, 9), x, y1 + 2, z - 1)
                    U.setBlock(level, (64, 1), x, y1 + 1, z)
                    U.setBlock(level, (64, 8), x, y1 + 2, z)
                    level.setBlockAt(x+ 1, y2+1, z -1, 0 )
                    level.setBlockAt(x + 1, y2 + 1, z , 0)
                    level.setBlockAt(x + 1, y2 + 2, z - 1, 0)
                    level.setBlockAt(x + 1, y2 + 2, z , 0)
    for z in [z_min, z_max]:
        for x in range(x_min, x_max-1):
            y1 = toolbox.findTerrain(level, x, z+1, 1, 250)
            y2 = toolbox.findTerrain(level, x, z, 1, 250)
            for i in range(1, 6):
                level.setBlockAt(x, y1+i, z+1, 4)
                level.setBlockAt(x, y2 + i, z, 4)
            #print(z_axis, gate[1][0], x, gate[0][1], z)
            if not z_axis and gate[1][0] == x and gate[0][1] == z and gate[1][0] < x_max - 3:
                print("make gate")
                if y1 == -1 or y2 == -1:
                    gate[0][0] = gate[0][0] + 1
                    gate[1][0] = gate[1][0] + 1
                else:
                    print("actually make gate")
                    print(z_axis, gate[1][0], x, gate[0][1], z)
                    U.setBlock(level, (64, 0), x -1, y1 +1, z)
                    U.setBlock(level, (64, 8), x - 1, y1 + 2, z )
                    U.setBlock(level, (64, 4), x, y1 + 1, z )
                    U.setBlock(level, (64, 9), x, y1 + 2, z)
                    level.setBlockAt(x- 1, y2+1, z + 1, 0 )
                    level.setBlockAt(x , y2 + 1, z +1 , 0)
                    level.setBlockAt(x - 1, y2 + 2, z + 1, 0)
                    level.setBlockAt(x , y2 + 2, z + 1, 0)



def build_naive_house(level, box):
    walllength = 0.7
    end_walls = int(walllength*(box.maxy-box.miny)) + box.miny
    for x in xrange(box.minx, box.maxx):
        for z in xrange(box.minz, box.maxz):
            for y in xrange(box.miny, end_walls):  # nested loops can be slow
                if x == box.minx + 1 or x == box.maxx - 2 or z == box.minz + 1 or z == box.maxz - 2:# or y == end_walls - 1:
                    level.setBlockAt(x, y, z, 5)
    level.setBlockAt(box.minx+2, box.miny, box.minz+1, 64)
    level.setBlockAt(box.minx + 2, box.miny + 1, box.minz + 1, 64)
    build_windows(box, level, end_walls)
    build_roof(box, level, end_walls)

def build_windows(box, level, end_walls):
    length_walls = end_walls - box.miny
    #n_windows = int(m.floor(length_walls/3))
    for y in range(box.miny + 1, end_walls -1, 3):
        z = [box.minz+1, box.maxz - 2]
        for x in range(box.minx + 2, box.maxx - 2, 3):
            for zet in z:
                level.setBlockAt(x, y, zet, 20)
        x = [box.minx + 1, box.maxx - 2]
        for z in range(box.minz + 2, box.maxz - 2, 3):
            for ex in x:
                level.setBlockAt(ex, y, z, 20)



def build_roof(box, level, end_walls):
    x_length = box.maxx - box.minx
    z_length = box.maxz - box.minz

    short_x = (z_length > x_length)
    length = x_length if (z_length > x_length) else z_length
    if length%2==0:
        end_roof = end_walls + length/2
    else:
        end_roof = end_walls + (length-1)/2
    if short_x:
        short_start = box.minx
        short_end = box.maxx
        long_start = box.minz
        long_end = box.maxz
    else:
        long_start = box.minx
        long_end = box.maxx
        short_start = box.minz
        short_end = box.maxz
    for y in xrange(end_walls, end_roof):
        i = y - end_walls
        for short in xrange(short_start+i, short_end-i):
            for long in xrange(long_start, long_end):

                if short == short_start +  i:

                    if short_x:
                        #level.setBlockAt(short,  y, long, 53)
                        U.setBlock(level, (53, 0), short, y, long)
                        print(short, long, y)
                        # west
                    else:
                        U.setBlock(level, (53, 2), long, y, short)
                        #print(short_x)
                        #north
                elif short == short_end - 1 - i:
                    if short_x:

                        U.setBlock(level, (53, 1), short, y, long)
                        # east
                    else:
                        U.setBlock(level, (53, 3), long, y, short)
                        # south
                elif long == long_start or long == long_end -1 or (length%2==1 and y==end_roof-1 and short == short_start+i+1):
                    if short_x:
                        level.setBlockAt(short,  y, long, 17)
                    else:
                        level.setBlockAt(long,  y, short, 17)





