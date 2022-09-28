import random

inputs = (
    ("Get color palets based on a given box", "label"),
    ("Creator: Elin, Koen", "label")
)

class Pallete():
    def __init__(self, pillars=False):
        self.quartz_stair = 156
        self.quartz_block = (155, 0)
        self.quartz_slab = (44, 7)
        self.granite = (1, 1)
        self.polished_granite = (1, 2)
        self.andesite = (1,5)
        self.polished_andesite = (1,6)
        color = 33
        rng_wall = random.randint(0, color+11)
        if rng_wall <= color:#orange bricks
            self.wall = (45, 0)
        elif rng_wall == color + 1:#orange
            self.wall = (251, 1)
        elif rng_wall == color + 2:#magenta
            self.wall = (251, 2)
        elif rng_wall == color + 3:#lightblue
            self.wall = (251, 3)
        elif rng_wall == color + 4:#yellow
            self.wall = (251, 4)
        elif rng_wall == color + 5:#lime
            self.wall = (251, 5)
        elif rng_wall == color + 6:#pink
            self.wall = (251, 6)
        elif rng_wall == color + 7:#cyan
            self.wall = (251, 9)
        elif rng_wall == color + 8:#purple
            self.wall = (251, 10)
        elif rng_wall == color + 9:#blue
            self.wall = (251, 11)
        elif rng_wall == color + 10:#green
            self.wall = (251, 13)
        elif rng_wall == color + 11:#red
            self.wall = (251, 14)

        #self.wall = (45, 0)#FIXME hardcoded
        self.pillar = self.wall#(251, 0)TODO if pillars == True...

        rng_plank = random.randint(0, 2)
        #print('plank = ', rng_plank)
        if rng_plank == 0:#oak
            self.stair = 53
            self.floor = (5, 0)
            self.fence = (85, 0)
            alt_plank = random.randint(0, 2)
            if alt_plank == 0:#spruce
                self.int_slab = (126, 1)
                self.int_wood = (5, 1)
                self.int_fence = (188, 0)
                self.int_stair = 134
                self.int_sign = 68#TODO find out if it works
            if alt_plank == 1:#birch
                self.int_slab = (126, 2)
                self.int_wood = (5, 2)
                self.int_fence = (189, 0)
                self.int_stair = 135
                self.int_sign = 68#TODO find out if it works
            if alt_plank == 2:#dark oak
                self.int_slab = (126, 5)
                self.int_wood = (5, 5)
                self.int_fence = (191, 0)
                self.int_stair = 164
                self.int_sign = 68#TODO find out if it works
        elif rng_plank == 1:#spruce
            self.stair = 134
            self.floor = (5, 1)
            self.fence = (188, 0)
            alt_plank = random.randint(0, 2)
            if alt_plank == 0:#oak
                self.int_slab = (126, 0)
                self.int_wood = (5, 0)
                self.int_fence = (85, 0)
                self.int_stair = 53
                self.int_sign = 68#TODO find out if it works
            if alt_plank == 1:#birch
                self.int_slab = (126, 2)
                self.int_wood = (5, 2)
                self.int_fence = (189, 0)
                self.int_stair = 135
                self.int_sign = 68#TODO find out if it works
            if alt_plank == 2:#dark oak
                self.int_slab = (126, 5)
                self.int_wood = (5, 5)
                self.int_fence = (191, 0)
                self.int_stair = 164
                self.int_sign = 68#TODO find out if it works
        elif rng_plank == 2:#birch
            self.stair = 135
            self.floor = (5, 2)
            self.fence = (189, 0)
            alt_plank = random.randint(0, 2)
            if alt_plank == 0:#spruce
                self.int_slab = (126, 1)
                self.int_wood = (5, 1)
                self.int_fence = (188, 0)
                self.int_stair = 134
                self.int_sign = 68#TODO find out if it works
            if alt_plank == 1:#oak
                self.int_slab = (126, 0)
                self.int_wood = (5, 0)
                self.int_fence = (85, 0)
                self.int_stair = 53
                self.int_sign = 68#TODO find out if it works
            if alt_plank == 2:#dark oak
                self.int_slab = (126, 5)
                self.int_wood = (5, 5)
                self.int_fence = (191, 0)
                self.int_stair = 164
                self.int_sign = 68#TODO find out if it works

        rng_door = random.randint(0, 4)
        #print('door = ', rng_door)
        if rng_door == 0:#oakw
            self.door = 64
        elif rng_door == 1:#spruce
            self.door = 193
        elif rng_door == 2:#birch
            self.door = 194
        elif rng_door == 3:#jungle
            self.door = 195
        elif rng_door == 4:#dark oak
            self.door = 197

        rng_roof = random.randint(0, 3)
        #print('roof = ', rng_roof)
        if rng_roof == 0:#acacia
            self.roof_stair = 163
            self.roof_block = (5, 4)
            self.roof_slab = (126, 4)
        elif rng_roof == 1:#gray bricks
            self.roof_stair = 109
            self.roof_block = (98, 0)
            self.roof_slab = (44, 5)
        elif rng_roof == 2:#nether bricks
            self.roof_stair = 114
            self.roof_block = (112, 0)
            self.roof_slab = (44, 6)
        elif rng_roof == 3:#dark oak
            self.roof_stair = 164
            self.roof_block = (5, 5)
            self.roof_slab = (126, 5)

        #self.decoration_slab #TODO add if nescassary TODO
        raam = random.randint(0, 3)
        #print('raam = ', raam)
        if raam == 0:#vanilla
            self.window = (102, 0)
            self.door_window = (20, 0)
        elif raam == 1:#gray
            self.window = (160, 7)
            self.door_window = (95, 7)
        elif raam == 2:#black
            self.window = (160, 15)
            self.door_window = (95, 15)
        elif raam == 3:#light_gray
            self.window = (160, 8)
            self.door_window = (95, 8)

        self.ladder = 65
        self.bed = 26

        self.torch = (50, 5)

        self.cauldron = 118
        self.furnace = 61
        self.chest = 54
        self.bookshelf = (47, 0)

        self.int_pot = (140, 0)
        self.int_flower = (38, random.randint(0, 8))
        self.crafting_table = (58, 0)
