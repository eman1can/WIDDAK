from traceback import format_exc

import numpy as np

from .lookup import PALETTELOOKUP

TEXTURE_MISSING = 0xFF00C7  # Hot Pink


class Color:
    """A class for managing colors. Pass in a color map to use pre defined color or to reuse a previously computed color map"""
    def __init__(self, color_map, palette=PALETTELOOKUP):
        self._color_map = color_map
        self._palette = palette

    def _hex_to_scalar(self, hex, o=None, dtype=np.float64):
        if hex in self._color_map:
            return self._color_map[hex]
        if o is None:
            o = [0, 8, 16]
        r = ((hex >> o[0]) & 0xFF) / 0xFF
        g = ((hex >> o[1]) & 0xFF) / 0xFF
        b = ((hex >> o[2]) & 0xFF) / 0xFF
        c = np.array([r, g, b], dtype)
        self._color_map[hex] = c
        return c

    def swap_rgb_bgr(self, val):
        """Switch the color channels for this color. Will only work for ints or hex"""
        a = val & 0xFF
        b = val & (0xFF << 8)
        c = (val >> 16) & 0xFF
        return c | b | a << 16

    def rgb_hex_to_float_rgb(self, hex):
        """Convert a hex scaler into a float64 array of rgb"""
        return self._hex_to_scalar(hex)

    def bgr_hex_to_float_rgb(self, hex):
        """Convert a bgr hex scaler into a float64 array of rgb"""
        return self._hex_to_scalar(hex, [16, 8, 0])

    def rgb_hex_to_int_rgb(self, hex):
        """Convert a hex scaler into a uint8 array of rgb"""
        return self._hex_to_scalar(hex, dtype=np.uint8)

    def bgr_hex_to_int_rgb(self, hex):
        """Convert a bgr hex scaler into a uint8 array of rgb"""
        return self._hex_to_scalar(hex, [16, 8, 0], dtype=np.uint8)

    def get_hex_color_for_id(self, blockID):
        """Convert a minecraft blockID into a hex color based on the internal palette"""
        if blockID == 'minecraft:air' or blockID == 'minecraft:cave_air':
            return 0x000000  # Empty / Black
        elif blockID not in self._palette:
            print(f'Unknown block: {blockID}')
            return TEXTURE_MISSING
        else:
            return self._palette[blockID]

    def get_hex_color(self, world_slice, x, y, z):
        """Get the hex color for the block at a location"""
        try:
            blockID = world_slice.get_block_id_at(x, y, z)
            return self.get_hex_color_for_id(blockID)
        except IndexError as ie:
            print(format_exc())
            return TEXTURE_MISSING