""" NBT-generating utility functions """

__author__    = "Arthur van der Staaij"
__copyright__ = "Copyright 2022, Arthur van der Staaij"
__licence__   = "MIT"


from typing import List, Optional


def signNBT(
    line1:   Optional[str] = None,
    line2:   Optional[str] = None,
    line3:   Optional[str] = None,
    line4:   Optional[str] = None,
    color:   Optional[str] = None,
):
    """ Returns an nbt string with sign contents """
    nbtFields: List[str] = []

    for i, line in enumerate([line1, line2, line3, line4]):
        if line is not None:
            nbtFields.append(f"Text{i+1}: '{{\"text\":\"{line}\"}}'")

    if color is not None:
        nbtFields.append(f"Color: \"{color}\"")

    return ",".join(nbtFields)
