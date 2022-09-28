def getRectangle(surface, xFirst, zFirst, heightRange, maxWidth):
	rec = Rectangle(xFirst, zFirst, xFirst + 1, zFirst + 1)
	height = surface.surfaceMap[xFirst][zFirst].height
	continueUp = True
	continueRight = True
	continueDown = True
	continueLeft = True
	while continueUp or continueRight or continueDown or continueLeft:
		if continueUp:
			if rec.zEnd < surface.zLength - 1 and rec.zLength < maxWidth and isValidHorizontalArea(surface, rec.xStart, rec.xEnd, rec.zEnd, height, heightRange):
				rec.zEnd += 1
				rec.zLength += 1
			else:
				continueUp = False
		if continueRight:
			if rec.xEnd < surface.xLength - 1 and rec.xLength < maxWidth and isValidVerticalArea(surface, rec.zStart, rec.zEnd, rec.xEnd, height, heightRange):
				rec.xEnd += 1
				rec.xLength += 1
			else:
				continueRight = False
		if continueDown:
			if 0 < rec.zStart and rec.zLength < maxWidth and isValidHorizontalArea(surface, rec.xStart, rec.xEnd, rec.zStart - 1, height, heightRange):
				rec.zStart -= 1
				rec.zLength += 1
			else:
				continueDown = False
		if continueLeft:
			if 0 < rec.xStart and rec.xLength < maxWidth and isValidVerticalArea(surface, rec.zStart, rec.zEnd, rec.xStart - 1, height, heightRange):
				rec.xStart -= 1
				rec.xLength += 1
			else:
				continueLeft = False
	return rec

def isValidHorizontalArea(surface, xStart, xEnd, z, height, heightRange):
	for x in range(xStart, xEnd):
		if surface.surfaceMap[x][z].height < height or surface.surfaceMap[x][z].height > height + heightRange or surface.surfaceMap[x][z].isOccupied or surface.surfaceMap[x][z].isWater:
			return False
	return True

def isValidVerticalArea(surface, zStart, zEnd, x, height, heightRange):
	for z in range(zStart, zEnd):
		if surface.surfaceMap[x][z].height < height or surface.surfaceMap[x][z].height > height + heightRange or surface.surfaceMap[x][z].isOccupied or surface.surfaceMap[x][z].isWater:
			return False
	return True

class Rectangle:

	def __init__(self, xStart, zStart, xEnd, zEnd):
		self.xStart = xStart
		self.zStart = zStart
		self.xEnd = xEnd
		self.zEnd = zEnd
		self.xLength = xEnd - xStart
		self.zLength = zEnd - zStart