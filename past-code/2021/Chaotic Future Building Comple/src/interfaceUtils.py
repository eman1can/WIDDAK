# ! /usr/bin/python3
"""### Provide tools for placing and getting blocks and more.

This module contains functions to:
* Request the build area as defined in-world
* Run Minecraft commands
* Get the name of a block at a particular coordinate
* Place blocks in the world
"""
__all__ = ['Interface', 'requestBuildArea', 'runCommand',
           'setBlock', 'getBlock', 'sendBlocks']
# __version__

from random import randrange

import requests
from numpy.lib.function_base import place
from requests import ConnectionError

from mapUtils import minecraft_colors

session = requests.Session()


class Interface():
    """**Provides tools for interacting with the HTML interface**.

    All function parameters and returns are in local coordinates.
    """

    def __init__(self, x=0, y=0, z=0, buffering=False, bufferlimit=1024):
        """**Initialise an interface with offset and buffering**."""
        self.offset = x, y, z
        self.__buffering = buffering
        self.bufferlimit = bufferlimit
        self.buffer = []

    def __del__(self):
        """**Clean up before destruction**."""
        self.sendBlocks()

    def getBlock(self, x, y, z):
        """**Return the name of a block in the world**."""
        x, y, z = self.local2global(x, y, z)

        url = 'http://localhost:9000/blocks?x={}&y={}&z={}'.format(x, y, z)
        try:
            response = requests.get(url)
        except ConnectionError:
            return "minecraft:void_air"
        return response.text

    def fill(self, x1, y1, z1, x2, y2, z2, blockStr):
        """**Fill the given region with the given block**."""
        x1, y1, z1 = self.local2global(x1, y1, z1)
        x2, y2, z2 = self.local2global(x2, y2, z2)
        xlo, ylo, zlo = min(x1, x2), min(y1, y2), min(z1, z2)
        xhi, yhi, zhi = max(x1, x2), max(y1, y2), max(z1, z2)

        for x in range(xlo, xhi + 1):
            for y in range(ylo, yhi + 1):
                for z in range(zlo, zhi + 1):
                    self.setBlock(x, y, z, blockStr)

    def setBlock(self, x, y, z, blockStr):
        """**Place a block in the world depending on buffer activation**."""
        if self.__buffering:
            self.placeBlockBatched(x, y, z, blockStr, self.bufferlimit)
        else:
            self.placeBlock(x, y, z, blockStr)

    def placeBlock(self, x, y, z, blockStr):
        """**Place a single block in the world**."""
        x, y, z = self.local2global(x, y, z)

        url = 'http://localhost:9000/blocks?x={}&y={}&z={}'.format(x, y, z)
        try:
            response = requests.put(url, blockStr)
        except ConnectionError:
            return "0"
        return response.text

    # ----------------------------------------------------- block buffers

    def toggleBuffer(self):
        """**Activates or deactivates the buffer function safely**."""
        self.buffering = not self.buffering
        return self.buffering

    def isBuffering(self):
        """**Get self.__buffering**."""
        return self.__buffering

    def setBuffering(self, value):
        """**Set self.__buffering**."""
        self.__buffering = value
        if self.__buffering:
            print("Buffering has been activated.")
        else:
            self.sendBlocks()
            print("Buffering has been deactivated.")

    def getBufferlimit(self):
        """**Get self.bufferlimit**."""
        return self.bufferlimit

    def setBufferLimit(self, value):
        """**Set self.bufferlimit**."""
        self.bufferlimit = value

    def placeBlockBatched(self, x, y, z, blockStr, limit=50):
        """**Place a block in the buffer and send once limit is exceeded**."""
        x, y, z = self.local2global(x, y, z)

        self.buffer.append((x, y, z, blockStr))
        if len(self.buffer) >= limit:
            return self.sendBlocks()
        else:
            return None

    def sendBlocks(self, x=0, y=0, z=0, retries=5):
        """**Send the buffer to the server and clear it**.

        Since the buffer contains global coordinates
            no conversion takes place in this function
        """
        url = 'http://localhost:9000/blocks?x={}&y={}&z={}'.format(x, y, z)
        body = str.join("\n", ['~{} ~{} ~{} {}'.format(*bp)
                               for bp in self.buffer])
        try:
            response = requests.put(url, body)
            self.buffer = []
            return response.text
        except ConnectionError as e:
            print("Request failed: {} Retrying ({} left)".format(e, retries))
            if retries > 0:
                return self.sendBlocks(x, y, z, retries - 1)

    
    def sendDirect(self,body, x, y, z, retries=5):
        url = 'http://localhost:9000/blocks?x={}&y={}&z={}'.format(x, y, z)
        try:
            response = requests.put(url, body)
            return response.text
        except ConnectionError as e:
            print("Request failed: {} Retrying ({} left)".format(e, retries))
            if retries > 0:
                return self.sendDirect(x, y, z, retries - 1)


    # ----------------------------------------------------- utility functions

    def local2global(self, x, y, z):
        """**Translate local to global coordinates**."""
        result = []
        if x is not None:
            result.append(x + self.offset[0])
        if y is not None:
            result.append(y + self.offset[1])
        if z is not None:
            result.append(z + self.offset[2])
        return result

    def global2local(self, x, y, z):
        """**Translate global to local coordinates**."""
        result = []
        if x is not None:
            result.append(x - self.offset[0])
        if y is not None:
            result.append(y - self.offset[1])
        if z is not None:
            result.append(z - self.offset[2])
        return result


def runCommand(command):
    """**Run a Minecraft command in the world**."""
    url = 'http://localhost:9000/command'
    try:
        response = session.post(url, bytes(command, "utf-8"))
    except ConnectionError:
        return "connection error"
    return response.text


def requestBuildArea():
    """**Return the building area**."""
    area = 0, 0, 0, 128, 256, 128   # default area for beginners
    response = requests.get('http://localhost:9000/buildarea')
    if response.ok:
        buildArea = response.json()
        if buildArea != -1:
            x1 = buildArea["xFrom"]
            y1 = buildArea["yFrom"]
            z1 = buildArea["zFrom"]
            x2 = buildArea["xTo"]
            y2 = buildArea["yTo"]
            z2 = buildArea["zTo"]
            area = x1, y1, z1, x2, y2, z2
    else:
        print(response.text)
        print("Using default build area.")
    return area

# ========================================================= global interface


globalinterface = Interface()


def isBuffering():
    """**Global isBuffering**."""
    return globalinterface.isBuffering()


def setBuffering(val):
    """**Global setBuffering**."""
    globalinterface.setBuffering(val)


def getBufferLimit():
    """**Global getBufferLimit**."""
    return globalinterface.getBufferLimit()


def setBufferLimit(val):
    """**Global setBufferLimit**."""
    globalinterface.setBufferLimit(val)


def getBlock(x, y, z):
    """**Global getBlock**."""
    return globalinterface.getBlock(x, y, z)


def fill(x1, y1, z1, x2, y2, z2, blockStr):
    """**Global fill**."""
    return globalinterface.fill(x1, y1, z1, x2, y2, z2, blockStr)


def setBlock(x, y, z, blockStr):
    """**Global setBlock**."""
    return globalinterface.setBlock(x, y, z, blockStr)

def clearBlockBuffer():
    """**Clears the block buffer.**"""
    global blockBuffer
    blockBuffer = []

def randomWool():
    return f"{minecraft_colors[randrange(len(minecraft_colors))]}_wool"

def buildWireCube(x, y, z, sx, sy, sz, blockID = None):
    blockID = randomWool() if blockID is None else blockID

    for i in range(sx):
        setBlock(x + i, y, z, blockID)
    for i in range(sy):
        setBlock(x, y + i, z, blockID)
    for i in range(sz):
        setBlock(x, y, z + i, blockID)
    for i in range(sy):
        setBlock(x + sx - 1, y + i, z, blockID)
    for i in range(sz):
        setBlock(x + sx - 1, y, z + i, blockID)
    for i in range(sx):
        setBlock(x + i, y + sy - 1, z, blockID)
    for i in range(sz):
        setBlock(x, y + sy - 1, z + i, blockID)
    for i in range(sx):
        setBlock(x + i, y, z + sz - 1, blockID)
    for i in range(sy):
        setBlock(x, y + i, z + sz - 1, blockID)
    for i in range(sx):
        setBlock(x + i, y + sy - 1, z + sz - 1, blockID)
    for i in range(sy):
        setBlock(x + sx - 1, y + i, z + sz - 1, blockID)
    for i in range(sz):
        setBlock(x + sx - 1, y + sy - 1, z + i, blockID)


def buildSolidCube(x, y, z, sx, sy, sz, blockID = None):
    blockID = randomWool() if blockID is None else blockID
    # blockID = "light_gray_concrete"


    for yy in range(y, y+sy):
        for xx in range(x, x+sx):
            for zz in range(z, z+sz):
                setBlock(xx, yy, zz, blockID)

def buildHollowCube(x, y, z, sx, sy, sz, blockID = None):
    blockID = randomWool() if blockID is None else blockID
    # blockID = "light_gray_concrete"

    for yy in range(y, y+sy):
        for xx in range(x, x+sx):
            for zz in range(z, z+sz):
                if xx == x or yy == y or zz == z or xx == x+sx-1 or yy == y+sy-1 or zz == z+sz-1:
                    setBlock(xx, yy, zz, blockID)
# ----------------------------------------------------- block buffers


def toggleBuffer():
    """**Global toggleBuffer**."""
    return globalinterface.toggleBuffer()


def sendBlocks(x=0, y=0, z=0, retries=5):
    """**Global sendBlocks**."""
    return globalinterface.sendBlocks(x, y, z, retries)

def sendDirect(body, x=0, y=0, z=0, retries=5):
    """**Global sendDirect**."""
    return globalinterface.sendDirect(body, x, y, z, retries)

