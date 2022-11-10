from typing import List, Optional
from nbt.nbt import NBTFile as SimpleNBTFile


class NBTFile(SimpleNBTFile):
    def __add__(self, other):
        if self.name != other.name:
            raise TypeError('Are you trying to add different types of NBT data together?')
        if self.name == 'file':
            for chunk in other.chunks.tags:
                self.chunks.append(chunk)
            self.chunkX.value = min(self.chunkX.value, other.chunkX.value)
            self.chunkZ.value = min(self.chunkZ.value, other.chunkZ.value)
            self.chunkDX.value = max(self.chunkX.value + self.chunkDX.value, other.chunkX.value + other.chunkDX.value) - self.chunkX.value
            self.chunkDZ.value = max(self.chunkZ.value + self.chunkDZ.value, other.chunkZ.value + other.chunkDZ.value) - self.chunkZ.value
            return self
        else:
            raise NotImplementedError('We can\'t handle adding this type of NBT data yet!')

    def __getattr__(self, name):
        raised_name = 'C' + name[1:]
        for tag in self.tags:
            if tag.name == name or tag.name == raised_name:
                return tag
        raise AttributeError(f'\'{type(self)}\' has no attribute \'{name}\'')

    @staticmethod
    def signNBT(
            line1: Optional[str] = None,
            line2: Optional[str] = None,
            line3: Optional[str] = None,
            line4: Optional[str] = None,
            color: Optional[str] = None,
    ):
        """ Returns an nbt string with sign contents """
        nbtFields: List[str] = []

        for i, line in enumerate([line1, line2, line3, line4]):
            if line is not None:
                nbtFields.append(f"Text{i + 1}: '{{\"text\":\"{line}\"}}'")

        if color is not None:
            nbtFields.append(f"Color: \"{color}\"")

        return ",".join(nbtFields)
