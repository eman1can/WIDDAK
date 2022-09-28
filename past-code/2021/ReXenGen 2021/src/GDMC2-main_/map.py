from worldLoader import WorldSlice

import numpy as np
import cv2
import maths
from PIL import Image
from scipy import ndimage

# Skeletonize
from skimage import img_as_bool, io, color, morphology
from skan import skeleton_to_csgraph
import matplotlib.pyplot as plt
from collections import Counter

# Test
import random


def findGround(xzStart, xz):  # TODO: Change error.
    """
    Find the surface at xz using heightmap.

    Args:
        xzStart (tuple): Starting coordinates of the heightmap (northwest corner).
        xz (tuple): Coordinates xz in the Minecraft world.

    Returns:
        tuple: Coordinates xyz in the Minecraft world.
    """
    im = Image.open("heightmap.png")
    x = round(xz[0] - xzStart[0])
    z = round(xz[-1] - xzStart[-1])
    # Alpha is defined as the height ([3]).
    width, height = im.size
    if x >= width or z >= height:
        print("img:", x, z)
        print(width, height)
        print(xzStart, xz)
    try:
        return xz[0], (im.getpixel((x, z))[2]) - 1, xz[-1]
    except:
        print("Error getpixel in map.py:42 with ", x, z)
        return None


def areaCoordinates(xyz1, xyz2):
    """
    Transform an area into a start point and a distance. Work with xyz
    coordinates and xz coordinates.

    Args:
        xyz1 (tuple): Coordinates, whatever the direction.
        xyz2 (tuple): Coordinates, whatever the direction.

    Returns:
        tuple: xzStart, xzDistance
    """
    xzStart = (min(xyz1[0], xyz2[0]), min(xyz1[-1], xyz2[-1]))
    xzDistance = (
        (abs(xyz1[0] - xyz2[0])),
        (abs(xyz1[-1] - xyz2[-1])),
    )
    return xzStart, xzDistance


def irlToMc(xzStart, xz):
    x = round(xzStart[0] + xz[0])
    z = round(xzStart[1] + xz[1])
    return (x, z)


def heightmap(
    xzStart,
    xzDistance,
    mapName="heightmap.png",
    biomeName="heightmap_biome.png",
):
    """
    Generate a heightmap using nbt data.

    Args:
        xzStart (tuple): xz coordinates of the northwest corner of the
        area to scan.
        xzDistance (tuple): xz distance of the southwest corner from the
        northwest corner.

    Returns:
        heightmap.png

    >>> heightmap((-256, -256), (512, 512))
    """

    heightmap = Image.new(
        "RGBA",
        (xzDistance[0], xzDistance[1]),
        "red",
    )

    heightmapBiome = Image.new(
        "RGBA",
        (xzDistance[0], xzDistance[1]),
        "red",
    )

    slice = WorldSlice((xzStart[0], xzStart[1], xzDistance[0], xzDistance[1]))
    heightmapData = list(
        np.array(slice.heightmaps["MOTION_BLOCKING_NO_LEAVES"], dtype=np.uint8)
    )

    for x in range(0, xzDistance[0]):
        for z in range(0, xzDistance[1]):
            y = heightmapData[x][z]
            biomeId = slice.getBiomeAt((xzStart[0] + x, 0, xzStart[1] + z))
            block = slice.getBlockAt((xzStart[0] + x, y, xzStart[1] + z))
            heightmapBiome.putpixel((x, z), heightmapColor(y, biomeId, block))
            heightmap.putpixel((x, z), (y, y, y))

    heightmap.save(mapName)
    heightmapBiome.save(biomeName)


def heightmapColor(y, biomeId, block):  # TODO: Refactoring.
    neutral = [
        16,
        26,
        12,
        129,
        1,
        3,
        131,
        162,
        2,
        17,
        37,
        39,
        35,
        36,
        163,
        164,
    ]

    # Hills: 13, 17, 18, 19, 22, 28, 31, 33, 156, 161
    water = [
        0,
        7,
        10,
        11,
        24,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
    ]

    waterBlocks = [
        "minecraft:water",
        "minecraft:seagrass",
        "minecraft:tall_seagrass",
        "minecraft:kelp_plant",
    ]

    if (biomeId in water) or (block in waterBlocks):
        return 0, 0, 0, 0
    if biomeId in neutral:
        return 255, 255, 255, 255
    else:
        return 0, 0, 0, 0


def blur(image, name="medianBlur.png", factor=5):
    img = cv2.imread(image)
    img = cv2.medianBlur(img, factor)
    plt.imsave(name, img, cmap="gray", format="png")


def sobel(image, name="heightmap_sobel.png"):
    # Open the image
    img = np.array(Image.open(image)).astype(np.uint8)

    # Apply gray scale
    gray_img = np.round(
        0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
    ).astype(np.uint8)

    # Sobel Operator
    h, w = gray_img.shape
    # define filters
    horizontal = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])  # s2
    vertical = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])  # s1

    # define images with 0s
    newhorizontalImage = np.zeros((h, w))
    newverticalImage = np.zeros((h, w))
    newgradientImage = np.zeros((h, w))

    # offset by 1
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            horizontalGrad = (
                (horizontal[0, 0] * gray_img[i - 1, j - 1])
                + (horizontal[0, 1] * gray_img[i - 1, j])
                + (horizontal[0, 2] * gray_img[i - 1, j + 1])
                + (horizontal[1, 0] * gray_img[i, j - 1])
                + (horizontal[1, 1] * gray_img[i, j])
                + (horizontal[1, 2] * gray_img[i, j + 1])
                + (horizontal[2, 0] * gray_img[i + 1, j - 1])
                + (horizontal[2, 1] * gray_img[i + 1, j])
                + (horizontal[2, 2] * gray_img[i + 1, j + 1])
            )

            newhorizontalImage[i - 1, j - 1] = abs(horizontalGrad)

            verticalGrad = (
                (vertical[0, 0] * gray_img[i - 1, j - 1])
                + (vertical[0, 1] * gray_img[i - 1, j])
                + (vertical[0, 2] * gray_img[i - 1, j + 1])
                + (vertical[1, 0] * gray_img[i, j - 1])
                + (vertical[1, 1] * gray_img[i, j])
                + (vertical[1, 2] * gray_img[i, j + 1])
                + (vertical[2, 0] * gray_img[i + 1, j - 1])
                + (vertical[2, 1] * gray_img[i + 1, j])
                + (vertical[2, 2] * gray_img[i + 1, j + 1])
            )

            newverticalImage[i - 1, j - 1] = abs(verticalGrad)

            # Edge Magnitude
            mag = np.sqrt(pow(horizontalGrad, 2.0) + pow(verticalGrad, 2.0))
            newgradientImage[i - 1, j - 1] = mag

    plt.imsave(
        "heightmap_sobel.png", newgradientImage, cmap="gray", format="png"
    )


def canny(image, name="heightmap_canny.png"):
    # Open the image
    img = cv2.imread(image)

    # Apply Canny
    edges = cv2.Canny(img, 100, 200, 3, L2gradient=True)

    plt.imsave(name, edges, cmap="gray", format="png")


def mapData(
    heightmap, heightmap_biome, heightmap_sobel, name="heightmap_data.png"
):
    im = Image.open(heightmap)
    width, height = im.size

    sobel = Image.open(heightmap_sobel)
    img = sobel.load()

    biome = Image.open(heightmap_biome)
    out = biome.load()

    for x in range(0, width):
        for z in range(0, height):
            if img[x, z][0] >= 25:
                out[x, z] = (0, 0, 0, 255)
    biome.save(name)


def skel(image, name=None, debug=False):
    """
    Transform a biome heightmap to a skeleton.

    https://jni.github.io/skan/api/skan.csr.html

    Args:
        image (str): Path of the image.

    Returns:
        list: List of tuples. Coordinates of each intersections of the
        skeleton.
        Create an image of the skeleton.
    """
    img = img_as_bool(color.rgb2gray(color.rgba2rgb(io.imread(image))))
    out = morphology.skeletonize(img)
    # out = morphology.medial_axis(img)

    pixel_graph, coordinates, degrees = skeleton_to_csgraph(out)
    pixel_graph = pixel_graph.tocoo()

    pixel_graph_row = list(pixel_graph.row)
    pixel_graph_col = list(pixel_graph.col)
    pixel_graph_data = list(pixel_graph.data)

    # List of lists. Inverted coordinates.
    coordinates = list(coordinates)
    for i in range(len(coordinates)):
        coordinates[i] = (coordinates[i][1], coordinates[i][0])

    if debug:
        f, (ax0, ax1) = plt.subplots(1, 2)
        ax0.imshow(img, cmap="gray", interpolation="nearest")
        ax1.imshow(out, cmap="gray", interpolation="nearest")
        plt.show()

    if name != None:
        plt.imsave(name, out, cmap="gray", format="png")

    return pixel_graph_row, pixel_graph_col, pixel_graph_data, coordinates


def findNextElements(key, pixel_graph_row, pixel_graph_col):
    """Find the very nearest elements"""
    line = []

    values = np.array(pixel_graph_row)
    searchval = key
    ind = np.where(values == searchval)[0]

    for i in range(len(ind)):
        if pixel_graph_row[ind[i]] == key:
            line.append(pixel_graph_col[ind[i]])
    return line


def parseGraph(pixel_graph_row, pixel_graph_col):
    lines = []
    intersections = []  # Center of intersections[i] is center[i]
    center = []
    for key, value in sorted(
        Counter(pixel_graph_row).items(), key=lambda kv: kv[1], reverse=True
    ):
        # Start from the biggest intersections.
        if value != 2:  # We don't want to be in the middle of a line.
            line = findLine(key, pixel_graph_row, pixel_graph_col)

            # We have now all the connected points if it's an
            # intersection. We need to find the line.

            if value != 1:
                # It's not an endpoint.
                center.append(key)
                intersections.append(line)
                for i in line:
                    line = findLine(
                        i,
                        pixel_graph_row,
                        pixel_graph_col,
                    )

                    if i in line:
                        # The key is inside the result : it's a line.
                        alreadyInside = False
                        for l in lines:
                            # Verification if not already inside.
                            if Counter(l) == Counter(line):
                                alreadyInside = True
                                # print(line, "inside", lines)

                        if alreadyInside == False:
                            lines.append(line)
                    else:
                        # The key is not inside the result, it's an
                        # intersection directly connected to the key.
                        line = [key, i]
                        alreadyInside = False
                        for l in lines:
                            # Verification if not already inside.
                            if Counter(l) == Counter(line):
                                alreadyInside = True
                                # print(line, "inside", lines)

                        if alreadyInside == False:
                            lines.append(line)
    return lines, intersections, center


def findLine(key, pixel_graph_row, pixel_graph_col):
    nextKeys = findNextElements(key, pixel_graph_row, pixel_graph_col)

    if len(nextKeys) >= 3:  # Intersections.
        return nextKeys

    if len(nextKeys) == 2 or len(nextKeys) == 1:  # In line or endpoints.
        line = []
        line.append(key)
        line.insert(0, nextKeys[0])
        if len(nextKeys) == 2:
            line.insert(len(line), nextKeys[1])

        nextKeys = line[0], line[-1]

        while len(nextKeys) == 2 or len(nextKeys) == 1:
            extremity = []
            for key in nextKeys:
                nextKeys = findNextElements(
                    key, pixel_graph_row, pixel_graph_col
                )

                if len(nextKeys) <= 2:
                    # Add the neighbors that is not already in the line.
                    for element in nextKeys:
                        if element not in line:
                            extremity.append(element)
                            line.append(element)

                if len(nextKeys) >= 3:
                    # Add the intersection only.
                    extremity.append(key)

                nextKeys = []
                for key in extremity:
                    ends = findNextElements(
                        key, pixel_graph_row, pixel_graph_col
                    )
                    if len(ends) == 2:
                        nextKeys.append(key)
        return line


def sortPointDistance(points, distance, debugImage=None):  # ?
    """
    Sort points depending of the distance.

    Args:
        points (dict): Keys: To be associated with the distance. Values:
        Coordinates corresponding to the key category.
        distance (dict): Keys: To be associated with the points. Values:
        Distance between all the points.

    Returns:
        list: List of tuples. Coordinates only.
        dict: Keys: The category/tag. Values: Coordinates that belong to
        the category.
    """
    tag = {}
    for key in points.keys():
        tag[key] = []

    savedPoints = []
    savedPointsWithTag = {}

    for key, value in sorted(
        distance.items(), key=lambda kv: kv[1], reverse=True
    ):
        if value != -1:
            for coord in points[key]:
                if all(
                    maths.distance2D(allPoint, coord) > value
                    for allPoint in savedPoints
                ):
                    savedPoints.append(coord)
                    if savedPointsWithTag.get(key) == None:
                        savedPointsWithTag[key] = []
                    savedPointsWithTag[key].append(coord)

    if debugImage:
        img = Image.open(debugImage)
        for i in range(len(savedPoints)):
            img.putpixel(savedPoints[i], (255, 0, 0))
        img.save("debugImage.png", "PNG")

    return savedPoints, savedPointsWithTag