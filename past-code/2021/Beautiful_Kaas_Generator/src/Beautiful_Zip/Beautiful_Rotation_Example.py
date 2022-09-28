from pymclevel import schematic, block_copy, box as bx

def perform(og_level, og_box, options):
    scheme = schematic.extractSchematicFrom(og_level, og_box)

    box = bx.BoundingBox((0,0,0),(scheme.Length, scheme.Height, scheme.Width))

    scheme.rotateLeft()

    og_level.copyBlocksFrom(scheme, box, (box.minx+20, box.miny+4, box.minz))


    
