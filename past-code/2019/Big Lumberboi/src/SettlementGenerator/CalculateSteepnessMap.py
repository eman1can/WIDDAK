def calculateSteepnessMap(surface):
	for x in range(surface.xLength):
		for z in range(surface.zLength):
			surface.surfaceMap[x][z].steepness = calculateSurfacePointSteepness(surface, x, z)

def calculateSurfacePointSteepness(surface, x, z):
	heights = []
	if x + 1 < surface.xLength:
		heights.append(surface.surfaceMap[x + 1][z].height)
	if x - 1 >= 0:
		heights.append(surface.surfaceMap[x - 1][z].height)
	if z + 1 < surface.zLength:
		heights.append(surface.surfaceMap[x][z + 1].height)
	if z - 1 >= 0:
		heights.append(surface.surfaceMap[x][z - 1].height)

	minHeight = surface.surfaceMap[x][z].height
	maxHeight = surface.surfaceMap[x][z].height
	for h in heights:
		if h < minHeight:
			minHeight = h
		elif h > maxHeight:
			maxHeight = h
	return maxHeight - minHeight