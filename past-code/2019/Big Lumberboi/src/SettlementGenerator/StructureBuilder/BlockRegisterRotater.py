import BlockDictionary
import math

directions = ['north', 'east', 'south', 'west']

def rotateRegister(blockRegister, rotations):
	rotations = rotations % 4
	if rotations == 0:
		return blockRegister
	rotatedRegister = []
	for block in blockRegister:
		np = rotateBlock(0, 0, 1.57079632679 * rotations, (block['x'], block['z']))
		if not block.get('type') or not block.get('direction'):
			b = BlockDictionary.getBlock(block['id'], block['data'])
			if not b:
				rotatedRegister.append({'type': None, 'direction': None, 'verticalAllignment': None, 'id': block['id'], 'data': block['data'], 'x': np[0], 'y': block['y'], 'z': np[1]})
			else:
				rotatedRegister.append({'type': b.type, 'direction': changeDirection(b.direction, rotations), 'verticalAllignment': b.verticalAllignment, 'id': block['id'], 'data': block['data'], 'x': np[0], 'y': block['y'], 'z': np[1]})
			continue
		rotatedRegister.append({'type': block['type'], 'direction': changeDirection(block['direction'], rotations), 'verticalAllignment': block['verticalAllignment'], 'id': block['id'], 'data': block['data'], 'x': np[0], 'y': block['y'], 'z': np[1]})
	moveToPositive(rotatedRegister)
	return rotatedRegister

def rotateBlock(cx, cz, angle, p):
	s = round(math.sin(angle))
	c = round(math.cos(angle))

	p = (p[0] - cx, p[1] - cz)

	nx = p[0] * c - p[1] * s
	nz = p[0] * s + p[1] * c

	p = (nx + cx, nz + cz)
	return p

def changeDirection(direction, rotations):
	if not direction:
		return None
	i = (directions.index(direction) + rotations) % 4
	return directions[i]

def moveToPositive(blockRegister):
	xMin = 0
	zMin = 0
	for block in blockRegister:
		if block['x'] < xMin:
			xMin = block['x']
		if block['z'] < zMin:
			zMin = block['z']
	for block in blockRegister:
		block['x'] += abs(xMin)
		block['z'] += abs(zMin)