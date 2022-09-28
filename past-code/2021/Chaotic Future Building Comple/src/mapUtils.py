# ! /usr/bin/python3
"""### Provides tools for maps and heightmaps.

This module contains functions to:
* Calculate a heightmap ideal for building
* Visualise numpy arrays
"""
__all__ = ['calcGoodHeightmap']
# __version__

import time
from math import atan2, ceil, log2

import cv2
# import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng()

minecraft_colors  = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]

minecraft_woods = ["oak", "spruce", "birch", "acacia", "dark_oak", "jungle"]


def noise(shape, noiseshape, interpolation=cv2.INTER_LINEAR):
    nse = rng.random(noiseshape[0] * noiseshape[1], dtype = np.float64).reshape(noiseshape)
    return cv2.resize(nse, shape[::-1], interpolation=interpolation)

def fractalnoise(shape, minFreq=0, maxFreq=0):
    """creates a array of size <shape> filled with perlin-noise (might not technically be perlin noise?). The noise is created by starting with a 1x1 noise, upsampling it by 2, then adding a 2x2 noise, upsampling again, then 4x4, etc. until a big enough size is reached and it's cropped down to the correct size.
    Each additional noise layer has half the amplitude of the previous, so that small features aren't over-emphasized.

    Args:
        shape (tuple): size of the output array, must be 2d. For example (400,200)

    Raises:
        Raises ValueError if <shape> is not twodimensional

    Returns:
        ndarray of shape <shape>, of type float64 with values between 0 and 1
    """
    # if len(shape) != 2:
    #     raise ValueError("Shape needs to have length 2. Only 2d noise is supported")

    depth = ceil(log2(max(shape)))

    minFreq %= depth
    maxFreq %= depth

    noise = np.zeros((1,1), dtype = np.float64)

    for i in range(depth):
        noise = cv2.pyrUp(noise)
        if i >= minFreq and i <= maxFreq:
            # noise = rng.integers(0, 128**(1/(i+1)), img.size, dtype = 'uint8')
            noiseLayer = rng.random(noise.size, dtype = np.float64)
            noiseLayer = noiseLayer * 2**(-(i+1))
            # noise = np.random.normal(0, 1, img.size)
            noiseLayer = noiseLayer.reshape(noise.shape)
            noise = cv2.add(noise, noiseLayer)

    # for i in range(3):
    #     perlin = cv2.pyrUp(perlin)

    # perlin = (perlin - perlin.min()) / (perlin.max() - perlin.min())
    noise = noise[0:shape[0], 0:shape[1]]
    noise = noise.clip(0, 1)

    return noise
    # perlin = perlin * 255
    # perlin = perlin.astype(np.uint8)

def distanceToCenter(shape):
    if len(shape) != 2:
        raise ValueError("Shape needs to have length 2. Only 2d is supported")
    
    return np.array([[((x/shape[0]-0.5)**2 + (y/shape[1]-0.5)**2)**0.5 for x in range(shape[1])] for y in range(shape[0])])

def angleToCenter(shape):
    if len(shape) != 2:
        raise ValueError("Shape needs to have length 2. Only 2d is supported")
    
    return np.array([[atan2(y/shape[1]-0.5, x/shape[0]-0.5) for x in range(shape[1])] for y in range(shape[0])])


def normalize(array):
    return (array - array.min()) / (array.max() - array.min())

# def visualize(*arrays, title=None, autonormalize=True):
#     for array in arrays:
#         array = array * 1
#         if autonormalize:
#             array = (normalize(array) * 255).astype(np.uint8)

#         plt.figure()
#         if title:
#             plt.title(title)
#         plt_image = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
#         imgplot = plt.imshow(plt_image)
#     plt.show()

def showAnimationFrame(array, title=None, autonormalize=True):
    time.sleep(0.05)
    if autonormalize:
        array = (normalize(array) * 255).astype(np.uint8)
    # frame = cv2.resize(frame, (500,500), interpolation=cv2.INTER_NEAREST)
    cv2.imshow(title, array)
    cv2.waitKey()
    # cv2.destroyAllWindows()

def calcGoodHeightmap(worldSlice):
    """**Calculate a heightmap ideal for building**.

    Trees are ignored and water is considered ground.

    Args:
        worldSlice (WorldSlice): an instance of the WorldSlice class
                                 containing the raw heightmaps and block data

    Returns:
        any: numpy array containing the calculated heightmap
    """
    hm_mbnl = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    heightmapNoTrees = hm_mbnl[:]
    area = worldSlice.rect

    for x in range(area[2]):
        for z in range(area[3]):
            while True:
                y = heightmapNoTrees[x, z]
                block = worldSlice.getBlockAt(
                    area[0] + x, y - 1, area[1] + z)
                if block[-4:] == '_log':
                    heightmapNoTrees[x, z] -= 1
                else:
                    break

    return np.array(np.minimum(hm_mbnl, heightmapNoTrees))


# def visualize(*arrays, title=None, autonormalize=True):
#     """**Visualizes one or multiple numpy arrays**.

#     Args:
#         title (str, optional): display title. Defaults to None.
#         autonormalize (bool, optional): Normalizes the array to be between
#                                         0 (black) and 255 (white).
#                                         Defaults to True.
#     """
#     for array in arrays:
#         if autonormalize:
#             array = (normalize(array) * 255).astype(np.uint8)

#         plt.figure()
#         if title:
#             plt.title(title)
#         plt_image = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
#         imgplot = plt.imshow(plt_image)  # NOQA
#     plt.show()


def normalize(array):
    """**Normalize the array to contain values from 0 to 1**."""
    array = array * 1
    difference = array.max() - array.min()
    if difference == 0:
        return array * 0
    else:
        return (array - array.min()) / difference



def listWhere(array): 
    tupleList = np.where(array)
    return list(zip(tupleList[0], tupleList[1]))

def cv2SizedWindow(name, shape, height=512):
    cv2.namedWindow(name, 0)
    cv2.resizeWindow(name, int(shape[1] / shape[0] * height), height)

def normalizeUInt8(array):
    """**Normalize the array to contain values from 0 to 255 as a uint8 type**."""
    return (normalize(array) * 255).astype(np.uint8)

def imshowLabels(windowName, array, colorMap = cv2.COLORMAP_INFERNO):
    cv2.imshow(windowName, cv2.applyColorMap(normalizeUInt8(array), colorMap))
