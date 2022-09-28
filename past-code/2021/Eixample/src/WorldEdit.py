import interfaceUtils


def setBlock(x, y, z, material, properties=dict(), isBatched=True):
    interfaceUtils.setBlock(x, y, z, material, properties, isBatched)


# Create solid shape filling the given area.
def fill(fromX, fromY, fromZ, toX, toY, toZ, material, fillMode="replace"):
    return interfaceUtils.runCommand(
        "fill %d %d %d %d %d %d %s %s" % (fromX, fromY, fromZ, toX, toY, toZ, material, fillMode)
    )


# Create solid shape filling the given area. Non-air blocks are unaffected.
def fillEmpty(fromX, fromY, fromZ, toX, toY, toZ, material):
    return fill(fromX, fromY, fromZ, toX, toY, toZ, material, fillMode="keep")


# Create hollow shape. Blocks inside the area are replaced with air.
def hollowFill(fromX, fromY, fromZ, toX, toY, toZ, material):
    return fill(fromX, fromY, fromZ, toX, toY, toZ, material, fillMode="hollow")


# Create hollow shape. Blocks inside the area are unaffected.
def outlineFill(fromX, fromY, fromZ, toX, toY, toZ, material):
    return fill(fromX, fromY, fromZ, toX, toY, toZ, material, fillMode="outline")


# Replace all blocks in the given area with air.
def clear(fromX, fromY, fromZ, toX, toY, toZ):
    return fill(fromX, fromY, fromZ, toX, toY, toZ, "minecraft:air", fillMode="destroy")