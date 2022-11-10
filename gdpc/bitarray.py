"""Convert from Minecraft's packed binary format to integers"""

__all__ = ['BitConverter']
__version__ = 'v5.2'
__author__ = "Ethan Wolfe"
__year__ = 2022

from .util import inclusiveBetween


class BitConverter:
    """Store an array of binary values and its metrics.

    Minecraft stores block and heightmap data in compacted arrays of longs.
    This class performs index mapping and bit shifting to access the data.
    """

    def __init__(self, bits_per_entry, array_length):
        """Initialise a BitConverter to be used with this specific bit size and array length"""
        inclusiveBetween(1, 32, bits_per_entry)

        self.array_length = array_length
        self.bits_per_entry = bits_per_entry
        self.entry_mask = (1 << bits_per_entry) - 1
        self.entries_per_long = 64 // bits_per_entry

    def __repr__(self):
        return f"BitConverter<{self.bits_per_entry}, {self.array_length}>"

    def getAt(self, array, index):
        """Return the binary integer value stored at index"""
        inclusiveBetween(0, self.array_length - 1, index)
        i = index // self.entries_per_long
        k = (index - i * self.entries_per_long) * self.bits_per_entry
        return array[i] >> k & self.entry_mask

    def size(self):
        """Return the number of longs this converter references"""
        return self.array_length
