#!/usr/bin/python
# -*- coding: UTF-8 -*-


def getBoxSize(box):
    return box.maxx - box.minx, box.maxy - box.miny, box.maxz - box.minz


def get_block(level, x, y, z):
    block_id = level.blockAt(x, y, z)
    data = level.blockDataAt(x, y, z)
    return block_id, data


def setBlock(level, x, y, z, block_id, data=0):
    level.setBlockAt(x, y, z, block_id)
    level.setBlockDataAt(x, y, z, data)