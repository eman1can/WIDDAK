def findBiomes(level, surface):
	for x in range(surface.xStart, surface.xEnd):
		for z in range(surface.zStart, surface.zEnd):
			chunk = level.getChunk(x / 16, z / 16)
			chunkBiomeData = chunk.root_tag["Level"]["Biomes"].value
			surface.surfaceMap[x - surface.xStart][z - surface.zStart].biomeId = chunkBiomeData[chunkIndexToBiomeDataIndexV2(x % 16, z % 16)]

def chunkIndexToBiomeDataIndex(x, z):
	return x * 16 + z

def chunkIndexToBiomeDataIndexV2(x, z):
	return 255 - ((15 - x) + (15 - z) * 16)