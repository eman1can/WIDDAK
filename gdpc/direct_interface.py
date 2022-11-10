"""
Provide access to the HTTP interface of the Minecraft HTTP server.

This file contains various functions that map directly onto the HTTP interface.
It is recommended to use `interface.py` instead.
"""

__all__ = ['getBlock', 'placeBlock', 'sendBlocks', 'runCommand', 'getBuildArea', 'getChunks']
__version__ = "v5.2"
__year__ = 2022

from typing import Optional

import requests
from glm import ivec3
from requests.exceptions import ConnectionError, ReadTimeout

from gdpc.lookup import TCOLORS
from gdpc.vector_util import Box, Rect


def get(*args, **kwargs):
    try:
        return requests.get(*args, **kwargs)
    except ConnectionError:
        raise ConnectionError("Connection could not be established! (is Minecraft running?)")


def post(*args, **kwargs):
    try:
        return requests.post(*args, **kwargs)
    except ConnectionError:
        raise ConnectionError("Connection could not be established! (is Minecraft running?)")


def put(*args, **kwargs):
    try:
        return requests.put(*args, **kwargs)
    except ConnectionError:
        raise ConnectionError("Connection could not be established! (is Minecraft running?)")


def getBlock(point: ivec3):
    """ Return the block ID from the world """
    return get(f'http://localhost:9000/blocks?x={point.x}&y={point.y}&z={point.z}')


def placeBlock(point: ivec3, blockID, doBlockUpdates=True, flags=None):
    """ Place one or multiple blocks in the world """
    if flags is not None:
        queryParam = f"customFlags={flags}"
    else:
        queryParam = f"doBlockUpdates={doBlockUpdates}"

    if point is None:
        point = ivec3()

    url = f'http://localhost:9000/blocks?x={point.x}&y={point.y}&z={point.z}&{queryParam}'

    response = put(url, blockID).text.strip()
    return response


def sendBlocks(blockList, point: Optional[ivec3] = None, doBlockUpdates=True, customFlags=None):
    """ Take a list of blocks and place them into the world in one go """
    body = str.join("\n", ['~{} ~{} ~{} {}'.format(*bp) for bp in blockList])

    return placeBlock(point, body, doBlockUpdates, customFlags)


def runCommand(command):
    """ Run a Minecraft command in the world """
    return post(f'http://localhost:9000/command', bytes(command, "utf-8"))


def getBuildArea(timeout=0.25):
    """ Return the building area """
    area = Box.from_box(0, 0, 0, 128, 256, 128)   # default area for beginners

    try:
        response = get('http://localhost:9000/buildarea', timeout=timeout)
        if response.ok:
            buildArea = response.json()
            if buildArea != -1:
                x1 = buildArea["xFrom"]
                y1 = buildArea["yFrom"]
                z1 = buildArea["zFrom"]
                x2 = buildArea["xTo"]
                y2 = buildArea["yTo"]
                z2 = buildArea["zTo"]
                area = Box.from_corners(x1, y1, z1, x2, y2, z2)
        else:
            print("Using default build area Box(0, 0, 0, 128, 256, 128).")
    except ReadTimeout:
        print('Server is Busy')
    return area


def getChunks(rect: Rect, rtype='text'):
    """ Get raw chunk data """
    url = f'http://localhost:9000/chunks?x={rect.x1}&z={rect.z1}&dx={rect.dx}&dz={rect.dz}'
    acceptType = 'application/octet-stream' if rtype == 'bytes' else 'text/raw'
    response = get(url, headers={"Accept": acceptType})
    if response.status_code >= 400:
        print(f"Error: {response.text}")
        raise Exception(f'Failed to get chunk data: {response.text}')

    if rtype == 'text':
        return response.text
    elif rtype == 'bytes':
        return response.content
    else:
        raise Exception(f"{rtype} is not a valid return type.")
