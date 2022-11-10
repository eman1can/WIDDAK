"""
Functions for communicating with GDMC HTTP Interface.
Includes, getting and placing blocks and world data.
"""

__authors__ = ["Blinkenlights", "Ethan Wolfe", "Arthur van der Staaij"]
__version__ = "v5.0"
__year__ = 2022
__copyright__ = "Copyright 2022, Arthur van der Staaij and Ethan Wolfe"
__licence__ = "MIT"

__all__ = [
    'getBuildArea', 'getWorldSlice', 'Interface', 'runCommand', 'getPlayerArea', 'getGlobalInterface'
]

import sys
from collections import OrderedDict
from copy import copy
from itertools import product

import numpy as np
from glm import ivec2, ivec3
from typing import Sequence, Union, Optional, List
from contextlib import contextmanager
from concurrent import futures
from random import choice

from . import worldLoader
from .block import Block
from .util import isign
from .vector_util import Rect, Box, scaleToFlip3D
from .toolbox import isSequence
from .transform import Transform, toTransform
from .worldLoader import WorldSlice

import gdpc.direct_interface as di


class OrderedByLookupDict(OrderedDict):
    """ Limit size, evicting the least recently looked-up key when full.
    Taken from zhttps://docs.python.org/3/library/collections.html?highlight=ordereddict#collections.OrderedDict
    """

    def __init__(self, maxsize, *args, **kwds):
        self.maxsize = maxsize
        super().__init__(*args, **kwds)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        if key in self:
            self.move_to_end(key)
        super().__setitem__(key, value)
        if 0 < self.maxsize < len(self):
            oldest = next(iter(self))
            del self[oldest]


class Interface:
    """ Provides functions to place blocks in the world by interacting with the GDMC mod's HTTP
        interface.

        Stores various settings, resources, buffers and caches related to block placement, and a
        transform that defines a local coordinate system.

        Wraps gdpc v5.0's Interface class to work with vectors and transforms, and extends it, but
        also removes some features. The wrapped gdpc Interface is available as .gdpcInterface. """

    def __init__(self,
                 transformOrVec: Optional[Union[Transform, ivec3]] = None,
                 buffering: bool = True,
                 bufferLimit: int = 1024,
                 multithreading: bool = False,
                 multithreadingWorkers: int = 8,
                 caching: bool = False,
                 cacheLimit: int = 8192
                 ):
        """ Constructs an Interface instance with the specified transform and settings """
        self.transform = Transform() if transformOrVec is None else toTransform(transformOrVec)
        self._buffer: Optional[list[tuple[int, int, int, str]]] = []
        self._buffering: bool = buffering
        self._bufferLimit: int = bufferLimit + 1
        self._caching: bool = caching
        self._cacheLimit: int = cacheLimit
        self._placeBlockFlags: tuple[bool, Optional[str]] = (True, None)
        self._bufferBlockFlags: tuple[bool, Optional[str]] = (True, None)
        self._cache: Optional[list[ivec3]] = None
        if self.caching:
            self._cache = OrderedByLookupDict(self._cacheLimit)
        self._multithreadingWorkers = multithreadingWorkers
        self._bufferFlushExecutor = None
        self._multithreading = multithreading  # Creates the buffer flush executor if True
        self._bufferFlushFutures: List[futures.Future] = []
        self._command_buffer: List[str] = []

    def __del__(self):
        """ Cleans up this Interface instance """
        self.sendBufferedBlocks()
        self.awaitBufferFlushes()

    @property
    def buffering(self) -> bool:
        """ Whether block placement buffering is enabled """
        return self._buffering

    @buffering.setter
    def buffering(self, value: bool):
        if self.buffering and not value:
            self.sendBufferedBlocks()
        self.buffering = value

    @property
    def bufferLimit(self) -> int:
        """ Size of the block buffer """
        return self._bufferLimit - 1

    @bufferLimit.setter
    def bufferLimit(self, value: int):
        self._bufferLimit = value + 1

    @property
    def caching(self):
        """ Whether caching retrieved blocks is enabled """
        return self._caching

    @caching.setter
    def caching(self, value: bool):
        self._caching = value
        if self == globalInterface and not value:
            global globalDecay
            globalDecay = None

    @property
    def cacheLimit(self):
        """ Size of the block cache """
        return self._cacheLimit

    @cacheLimit.setter
    def cacheLimit(self, value: int):
        self._cacheLimit = value

    @property
    def multithreading(self):
        """ Whether multithreaded buffer flushing is enabled """
        return self._multithreading

    @multithreading.setter
    def multithreading(self, value: bool):
        self._multithreading = value
        if value and self._bufferFlushExecutor is None:
            self._bufferFlushExecutor = futures.ThreadPoolExecutor(self._multithreadingWorkers)

    @property
    def multithreadingWorkers(self):
        """ The amount of buffer flush worker threads.\n
            Modifying the amount of workers after class construction is not supported. """
        return self._multithreadingWorkers

    @contextmanager
    def pushTransform(self, transform: Optional[Union[Transform, ivec3]] = None):
        """
        Creates a context that pushed transform to self.transform on enter, and pops all changes on exit
        Can be used to create a local coordinate system on top of the current local coordinate system
        This is different from `Transform.push()`
        """
        current = copy(self.transform)
        try:
            if transform is not None:
                self.transform = self.transform @ toTransform(transform)
            yield
        finally:
            self.transform = current

    def runCommand(self, command: str) -> str:
        """ Executes one or multiple Minecraft commands (separated by newlines).
            If buffering is enabled, the command is deferred until after the next buffer flush. """
        if self.buffering:
            self._command_buffer.append(command)
            return '0'

        if command[0] == '/':
            command = command[1:]
        return di.runCommand(command)

    def _getFlags(self, doBlockUpdates: Optional[str], flags: Optional[bool]) -> tuple:
        if doBlockUpdates is None:
            doBlockUpdates = self._placeBlockFlags[0]
        if flags is None:
            flags = self._placeBlockFlags[1]
        return doBlockUpdates, flags

    def getBlock(self, point: ivec3, local: bool = False) -> str:
        """ Get the blockID at the given coordinates
        Either pass global coords or set local
        """
        if local:
            point = self.transform.apply(point)

        if self._caching and point in self._cache.keys():
            return self._cache[point]

        if self._caching and globalWorldSlice is not None:
            bp = globalWorldSlice.to_local(point)
            build_area = getGlobalBuildArea()
            if not build_area.isOutOfBounds(bp) and not globalDecay[bp.x][bp.y][bp.z]:
                block = getGlobalWorldSlice().get_block_id_at(point)
                if block == 'minecraft:void_air':
                    block = di.getBlock(point)
                self._cache[point] = block
                return block

        response = di.getBlock(point)
        if self._caching:
            self._cache[point] = response

        return response

    def placeBlock(self, point: ivec3, block: str, replace: Optional[Union[str, Sequence[str]]] = None, doBlockUpdates: Optional[str] = None, flags: Optional[bool] = None, local: bool = False):
        """ Place a block into the world
        Pass global coordinates or set local"""
        if replace is not None:
            if isinstance(replace, str):
                if self.getBlock(point, local) != replace:
                    return '0'
            elif isSequence(replace) and self.getBlock(point, local) not in replace:
                return '0'
            elif self.caching and isinstance(block, str) and block in self.getBlock(point, local):
                return '0'

        if not isinstance(block, str) and isSequence(block):
            block = choice(block)

        if self._buffering:
            response = self.placeBlockBuffered(point, block, doBlockUpdates, flags, local, self.bufferLimit)
        else:
            response = self.placeBlockDirect(point, block, doBlockUpdates, flags, local)

        if local:
            point = self.transform.apply(point)

        if self._caching:
            self._cache[point] = block
        build_area = getGlobalBuildArea()
        if not build_area.isOutOfBounds(point) and globalDecay is not None:
            globalWorldSlice = getGlobalWorldSlice()
            bp = globalWorldSlice.to_local(point)
            getGlobalDecay()[bp.x][bp.y][bp.z] = True
        return response

    def sendBlocks(self, point: Optional[ivec3] = None) -> str:
        """ Send the blocks in the buffer to the world with an optional offset """

        if len(self._buffer) == 0:
            return '0'
        return di.sendBlocks(self._buffer, point, *self._bufferBlockFlags)

    def sendBufferedBlocks(self):
        if self._multithreading:
            self._bufferFlushFutures = [f for f in self._bufferFlushFutures if not f.done()]

            buffer = self._buffer
            command_buffer = self._command_buffer

            def task():
                di.sendBlocks(buffer, None, *self._bufferBlockFlags)
                for command in command_buffer:
                    di.runCommand(command)

            future = self._bufferFlushExecutor.submite(task)
            self._bufferFlushFutures.append(future)
        else:
            di.sendBlocks(self._buffer, None, *self._bufferBlockFlags)
            for command in self._command_buffer:
                di.runCommand(command)

        self._buffer = []
        self._command_buffer = []

    def awaitBufferFlushes(self, timeout: Optional[float] = None):
        self._bufferFlushFutures = futures.wait(self._bufferFlushFutures, timeout).not_done

    def placeBlockDirect(self, point: ivec3, blockID: str, doBlockUpdates: Optional[str] = None, flags: Optional[bool] = None, local: bool = False) -> str:
        """ Place a single block in the world directly
        Either pass in global coordinates, or set the local flag
        """
        if local:
            point = self.transform.apply(point)
        return di.placeBlock(point, blockID, *self._getFlags(doBlockUpdates, flags))

    def placeBlockBuffered(self, point: ivec3, blockID: str, doBlockUpdates: Optional[str] = None, flags: Optional[bool] = None, local: bool = False, limit: int = 50):
        """ Places a block in the write buffer, pushing the buffer
        if it is over the limit or contains different flags
        """
        flags = self._getFlags(doBlockUpdates, flags)
        if flags != self._bufferBlockFlags:
            self.sendBufferedBlocks()
            self._bufferBlockFlags = flags
        if local:
            point = self.transform.apply(point)

        self._buffer.append((*point.to_tuple(), blockID))
        if len(self._buffer) >= limit:
            return self.sendBufferedBlocks()
        return '0'

    def place(self, block: Block, t: Union[Transform, ivec3], replace: Optional[Union[str, Sequence[str]]] = None, local: bool = False):
        if local:
            return self.place(block, self.transform @ toTransform(t), replace, False)
        t = toTransform(t)

        blockState = block.blockStateString(t.rotation, scaleToFlip3D(t.scale))
        tr = t.translation
        ts = t.scale
        for x, y, z in product(range(tr.x, tr.x + ts.x, isign(ts.x)), range(tr.y, tr.y + ts.y, isign(ts.y)), range(tr.z, tr.z + ts.z, isign(ts.z))):
            if isinstance(block.name, str):
                blockID = block.name
            else:
                blockID = choice(block.name)
            if blockID == "":
                continue
            self.placeBlock(ivec3(x, y, z), block.name + blockState, replace)
        if block.nbt is not None:
            self.runCommand(blockNBTCommand(tr, block.nbt))
        if len(self._buffer) == self.bufferLimit:
            self.sendBufferedBlocks()

globalInterface: Optional[Interface] = None
globalWorldSlice: Optional[WorldSlice] = None
globalBuildArea: Optional[Box] = None
globalDecay: Optional[np.ndarray] = None


def getGlobalInterface() -> Optional[Interface]:
    global globalInterface

    if globalInterface is None:
        globalInterface = Interface()
        return globalInterface
    return globalInterface


def getGlobalBuildArea() -> Optional[Box]:
    global globalBuildArea

    if globalBuildArea is None:
        globalBuildArea = getBuildArea()
        return globalBuildArea
    return globalBuildArea


def getGlobalWorldSlice() -> WorldSlice:
    global globalWorldSlice

    if globalWorldSlice is None:
        globalWorldSlice = getWorldSlice()
    return globalWorldSlice


def resetGlobalDecay() -> np.ndarray:
    global globalDecay

    point = getGlobalBuildArea()
    globalDecay = np.zeros((point.dx, 256, point.dz), np.bool)
    return globalDecay


def getGlobalDecay() -> np.ndarray:
    global globalDecay

    if globalDecay is None:
        resetGlobalDecay()
    return globalDecay


def getBuildArea() -> Optional[Box]:
    """"Returns the build area that was specified by /setbuildarea in-game or the default"""
    try:
        build_area = di.getBuildArea().normalize()
    except Exception as e:
        print(e, file=sys.stderr)
        return None
    return build_area


def getWorldSlice(rect: Optional[Rect] = None, dat_file: Optional[str] = None, save_data: bool = False, step: int = 8) -> Optional[WorldSlice]:
    if rect.size.x < 0 or rect.size.y < 0:
        print('Gave getWorldSlide a negative area!')
        return None
    """ If dat_file is not None, will load a local file, optionally specified by rect. If None, then it will query the server, keeping world data in the cache if the save_data flag is set"""
    if rect is None and dat_file is None:
        print("Using default build area in getWorldSlice (0, 0, 128, 128)", file=sys.stderr)
        rect = Rect.from_rect(0, 0, 128, 128)
    if dat_file is None:
        return worldLoader.WorldSlice.from_server(rect, save_data, step)
    else:
        return worldLoader.WorldSlice.from_file(dat_file, rect)


def runCommand(command: str) -> str:
    """ Executes one or multiple Minecraft commands (separated by newlines) """
    return getGlobalInterface().runCommand(command)


def blockNBTCommand(position: ivec3, nbt: str) -> str:
    """Returns the command required to merge the nbt data of the block at the global position
        [position] with [nbt] """
    return f"data merge block {position.x} {position.y} {position.z} {nbt}"


def getPlayerArea(point: ivec2 = ivec2(128, 128)) -> Box:
    """**Return the building area surrounding the player**."""
    # Correcting for offset from player position
    point -= 1
    point /= 2
    runCommand(f"execute at @p run setbuildarea ~{-point.x} 0 ~{-point.y} ~{point.x} 255 ~{point.y}")
    return getBuildArea()