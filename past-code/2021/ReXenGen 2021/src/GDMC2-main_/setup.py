import time
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
import requests

url = 'http://localhost:9000/command'

def setBlock(x, y, z, str):
    url = "http://localhost:9000/blocks?x=%i&y=%i&z=%i" % (x, y, z)
    # print('setting block %s at %i %i %i' % (str, x, y, z))
    try:
        response = requests.put(url, str)
    except ConnectionError:
        return "0"
    return response.text
    # print("%i, %i, %i: %s - %s" % (x, y, z, response.status_code, response.text))

def fill(block, pos):
    print(runCommand(f"fill %i %i %i %i %i %i {block}" % tuple(pos)))

def getBlock(x, y, z):
    url = 'http://localhost:9000/blocks?x=%i&y=%i&z=%i' % (x, y, z)
    # print(url)
    try:
        response = requests.get(url)
    except ConnectionError:
        return "void_air"
    return response.text[10:]
    # print("%i, %i, %i: %s - %s" % (x, y, z, response.status_code, response.text))

# BLOCK BUFFER STUFF

blockBuffer = []

# clear the block buffer
def clearBlockBuffer():
    global blockBuffer
    blockBuffer = []

# write a block update to the buffer
def registerSetBlock(x, y, z, str):
    global blockBuffer
    # blockBuffer += () '~%i ~%i ~%i %s' % (x, y, z, str)
    blockBuffer.append((x, y, z, str))

# send the buffer to the server and clear it
def sendBlocks(x=0, y=0, z=0, retries=5):
    global blockBuffer
    body = str.join("\n", ('~%i ~%i ~%i %s' % bp for bp in blockBuffer))
    url = 'http://localhost:9000/blocks?x=%i&y=%i&z=%i' % (x, y, z)
    try:
        response = requests.put(url, body)
        clearBlockBuffer()
        return response.text
    except ConnectionError as e:
        print("Request failed: %s Retrying (%i left)" % (e, retries))
        if retries > 0:
            return sendBlocks(x,y,z, retries - 1)

def placeBlockBatched(x, y, z, str, limit=50):
    registerSetBlock(x, y, z, str)
    if len(blockBuffer) >= limit:
        return sendBlocks(0, 0, 0)
    else:
        return None

def runCommand(command):
    # print("running cmd %s" % command)
    url = 'http://localhost:9000/command'
    try:
        response = requests.post(url, bytes(command, "utf-8"))
    except ConnectionError:
        return "connection error"
    return response.text

def requestBuildArea():
    response = requests.get('http://localhost:9000/buildarea')
    if response.ok:
        return response.json()
    else:
        print(response.text)
        return -1

def is_chunk(n):
        result = sqrt(n**2) % 16
        if result == 0:
            return True
        else:
            return False

def in_BuildingPlot(self,BuildingPlot,x,z):
    a = -1
    for elt in BuildingPlot:
        if elt[0] == x and elt[2] == z:
            a = elt[1]
    return a
        
def in_chunkCorner(self,chunkCorner,x,z):
    a = -1
    for elt in chunkCorner:
        if elt[0] == x and elt[2] == z:
            a = elt[1]
    return a

def get_biomegroup(self,biome,snow,mountain,taiga,birtchforest,darkforest,plain,swapland,mushrooms,jungle,savana,desert,mesa,neutral,material,mat1,mat2,mat3,mat4,mat5,mat6,mat7,mat8,mat9,mat10,mat11,mat12,mat13):
        if biome in snow:
            return 1
        elif biome in mountain:
            return 2
        elif biome in taiga:
            return 3
        elif biome in birtchforest:
            return 4
        elif biome in darkforest:
            return 5
        elif biome in plain:
            return 6
        elif biome in swapland:
            return 7
        elif biome in mushrooms:
            return 8
        elif biome in jungle:
            return 9
        elif biome in savana:
            return 10
        elif biome in desert:
            return 11
        elif biome in mesa:
            return 12
        elif biome in neutral:
            return 13
        else:
            return 13


#def set_materials(self,biome,material,mat1,mat2,mat3,mat4,mat5,mat6,mat7,mat8,mat9,mat10,mat11,mat12,mat13):

    
