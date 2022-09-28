from Common import setBlock

def removeTree(level, x, y, z):
	blocks = [Block(x, y, z)]
	while blocks:
		nextBlock = blocks.pop()
		x = nextBlock.x
		y = nextBlock.y
		z = nextBlock.z

		if not isTreeBlock(level, x, y, z):
			continue

		setBlock(level, None, x, y, z, 0)

		#Removes snow layer
		if level.blockAt(x, y + 1, z) == 78:
			setBlock(level, None, x, y + 1, z, 0)

		# Adds neighbors to stack
		blocks.extend([Block(x + 1, y, z), Block(x - 1, y, z), Block(x, y + 1, z), Block(x, y - 1, z), Block(x, y, z + 1), Block(x, y, z - 1)])
		blocks.extend([Block(x + 1, y + 1, z), Block(x - 1, y + 1, z), Block(x, y + 1, z + 1), Block(x, y + 1, z - 1)])
		blocks.extend([Block(x + 1, y - 1, z), Block(x - 1, y - 1, z), Block(x, y - 1, z + 1), Block(x, y - 1, z - 1)])

treeBlocks = [17, 18, 99, 100, 106, 161, 162]
def isTreeBlock(level, x, y, z):
		for block in treeBlocks:
			if (level.blockAt(x, y, z) == block):
				return True
		return False

class Block:

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z