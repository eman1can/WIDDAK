from random import choice, randrange

from interfaceUtils import sendDirect


def createPattern2D(array, palette):
    lines = []
    for i in range(len(array)):
        row = array[i]
        for j in range(len(row)):
            blockID = palette[row[j]]
            if blockID is not None:
                lines.append(f"~{i} ~ ~{j} {blockID}")

    return str.join("\n", lines)

def sendPattern(pattern, x, y, z):
    sendDirect(pattern, x, y, z)


patternElevator = createPattern2D(\
   [[0,1,0],
    [1,2,1],
    [0,1,0]], ["air", "black_stained_glass_pane", "ladder"]
)
patternElevatorFloor = createPattern2D(\
   [[0,1,0],
    [1,1,1],
    [0,1,0]], ["slime_block", "gray_concrete", "soul_sand"]
)
patternElevatorLight = createPattern2D(\
   [[0,0,4,0,0],
    [0,1,2,1,0],
    [4,2,3,2,4],
    [0,1,2,1,0],
    [0,0,4,0,0]], [None, "air", "black_stained_glass_pane", "ladder", "sea_lantern"]
)

saplings = [ "acacia_sapling", "bamboo_sapling", "birch_sapling", "dark_oak_sapling", "jungle_sapling", "oak_sapling", "spruce_sapling", "oak_sapling", "spruce_sapling", "birch_sapling", "jungle_sapling", "acacia_sapling", "dark_oak_sapling", "bamboo_sapling" ]

pottedSaplings = [f"potted_{sp}" for sp in saplings]

barrels = [f"barrel[facing={f}]" for f in ["east", "south", "up"]]

needsFacing = ["chest","furnace","blast_furnace", "smoker"]
storageRoom = barrels + ["spruce_planks"]
otherClutter = ["smithing_table", "crafting_table","jukebox","scaffolding"]


furnitureClutter = [] + storageRoom + otherClutter

simpleClutter = [] + storageRoom + otherClutter + pottedSaplings

def getSimpleRandomClutter():
    return choice(simpleClutter)

def getFurnitureRandomClutter():
    return choice(furnitureClutter)

# table, bed, flower pot
