def calculateHeightMap(level, surface):
	for x in range(surface.xLength):
		for z in range(surface.zLength):
			height = calculateSurfacePointHeight(level, x + surface.xStart, z + surface.zStart)
			surface.surfaceMap[x][z].height = height

def calculateSurfacePointHeight(level, x, z):
	heightIsFound = False
	y = 128
	while (not heightIsFound):
		if (isSurfaceBlock(level, x, y, z)):
			heightIsFound = True
		else:
			y -= 1
	return y

aboveSurfaceBlocks = [0, 6, 17, 18, 31, 32, 37, 38, 39, 40, 59, 78, 81, 83, 99, 100, 103, 104, 105, 106, 111, 141, 142, 161, 162, 175]
def isSurfaceBlock(level, x, y, z):
	for block in aboveSurfaceBlocks:
		if (level.blockAt(x, y, z) == block):
			return False
	return True