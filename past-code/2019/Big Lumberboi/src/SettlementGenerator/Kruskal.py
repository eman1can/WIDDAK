def getMinimumSpanningTree(nodes, edges):
	edges = sorted(edges)
	nodeSets = getNodeSets(nodes)
	amountOfNodeSets = len(nodeSets)
	minimumSpanningTree = []
	for edge in edges:
		nodeSet1 = findNodeSet(nodeSets, edge.nodeId1)
		nodeSet2 = findNodeSet(nodeSets, edge.nodeId2)
		if nodeSet1.id == nodeSet2.id:
			continue
		minimumSpanningTree.append(edge)
		mergeNodeSets(nodeSet1, nodeSet2)
		amountOfNodeSets -= 1
		if amountOfNodeSets == 1:
			break
	return minimumSpanningTree

def getNodeSets(nodes):
	nodeSets = []
	for i, node in enumerate(nodes):
		s = NodeSet(i)
		s.nodes.append(node)
		nodeSets.append(s)
	return nodeSets

def findNodeSet(nodeSets, nodeId):
	for nodeSet in nodeSets:
		for node in nodeSet.nodes:
			if node.id == nodeId:
				return nodeSet
	return None

def mergeNodeSets(nodeSet1, nodeSet2):
	nodeSet1.nodes.extend(nodeSet2.nodes)
	nodeSet2.nodes = []

class NodeSet:

	def __init__(self, id):
		self.id = id
		self.nodes = []