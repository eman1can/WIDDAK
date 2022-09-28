from os import sep

from nbt.nbt import TAG_Compound, NBTFile, TAG_String

from interfaceUtils import runCommand
from utils import Point, setBlock, BlockAPI, get_project_path

b = BlockAPI.blocks

SIZE = "size"
PALETTE = "palette"
BLOCKS = "blocks"
BLOCK_NAME = "Name"
BLOCK_PROP = "Properties"

deprecated_name = {
    "stonebrick_stonebrick": b.StoneBricks,
    "stone_brick_stone_slab": b.StoneBrickSlab,
    "unlit_redstone_torch": b.RedstoneTorch,
    "unpowered_repeater": b.Repeater,
    "coarse_dirt_dirt": b.CoarseDirt,
    "spruce_wooden_slab": b.SpruceSlab,
    "standing_sign": b.OakSign
}


class StructureNBT:
    """
    Extends StructureNBT to handle structure void
    """

    def __init__(self, filename=None):
        self.__nbt = nbt = NBTFile(sep.join([get_project_path(), 'structures', filename]))

        size_tag = self.__nbt.get(SIZE)
        x, y, z = (tag.value for tag in size_tag)
        self.__shape = Point(x, z, y)

        self.__palette = [self.parse_palette(_) for _ in nbt.get(PALETTE)]

    def build(self, x, y, z):
        for blockTag in self.__nbt.get(BLOCKS):
            blockPos = blockTag.get('pos')
            dx, dy, dz = (tag.value for tag in blockPos)
            blockPoint = Point(x + dx, z + dz, y + dy)
            blockState = self.__palette[blockTag.get('state').value]
            if blockTag.get('nbt'):
                blockState += self.parse_data(blockTag.get('nbt'))
                runCommand(f"setblock {blockPoint.x} {blockPoint.y} {blockPoint.z} {blockState}")
            else:
                setBlock(blockPoint, blockState)

    @property
    def width(self):
        return self.__shape.x

    @property
    def height(self):
        return self.__shape.y

    @property
    def length(self):
        return self.__shape.z

    @staticmethod
    def parse_palette(tag: TAG_Compound):
        blockName = tag.get(BLOCK_NAME).value.split(':')[-1]
        prop_tag = tag.get(BLOCK_PROP)
        properties = {}
        if prop_tag:
            for property in tag.get(BLOCK_PROP).tags:
                if property.name == "variant":
                    blockName = property.value + '_' + blockName
                else:
                    properties[property.name] = property.value
                if blockName in deprecated_name:
                    blockName = deprecated_name[blockName]
        return f"minecraft:{blockName}[{', '.join(f'{key}={value}' for (key, value) in properties.items())}]"

    @staticmethod
    def parse_data(param):
        def fmt(value):
            if type(value) is str:
                return f'\'{value}\''
            return str(value)

        return "{" + ', '.join(f"{_.name}:{fmt(_.value)}" for _ in filter(lambda tag: isinstance(tag, TAG_String), param.tags)) + "}"
