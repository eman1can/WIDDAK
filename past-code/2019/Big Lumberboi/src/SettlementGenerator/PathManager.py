import math
import sys
from random import randint

from Classes import Edge
from Classes import Node
from Classes import Point
from Common import getEuclideanDistance
from GetPath import getPath
from Kruskal import getMinimumSpanningTree

def getPathsInSections(surface, sections):
	paths = []
	for section in sections:
		paths.extend(getPathsInSection(surface, section))
	return paths

def getPathsInSection(surface, section):
	attempts = 5
	points = [Point(section.xMid, section.zMid)]
	pointPool = section.points
	poolSize = len(pointPool)
	expectedPoints = poolSize / 2500 - 1

	if expectedPoints < 1:
		section.pathConnectionPoints.extend(points)
		return []

	for _ in range(expectedPoints):
		greatestLength = 0
		nextPoint = None
		for _ in range(attempts):
			point = getRandomPoint(pointPool, poolSize, points)
			length = getLengthToNearestPoint(surface, points, point)
			if length > greatestLength:
				greatestLength = length
				nextPoint = point
		points.append(nextPoint)

	section.pathConnectionPoints.extend(points)
	return getPathBetweenPoints(surface, points)

def getPathsBetweenSections(surface, sections):
	sectionPairs = getSectionPairs(surface, sections)
	paths = []
	for sectionPair in sectionPairs:
		paths.append(getShortestIntersectionPath(surface, sectionPair[0], sectionPair[1]))
	return paths

def getRandomPoint(pointPool, poolSize, points):
	i = randint(0, poolSize - 1)
	p = pointPool[i]
	while contain(points, p):
		i = randint(0, poolSize - 1)
		p = pointPool[i]
	return p

def contain(points, point):
	for p in points:
		if p.x == point.x and p.z == point.z:
			return True
	return False

def getLengthToNearestPoint(surface, points, point):
	length = sys.maxint
	for p in points:
		l = getDistance(p.x, p.z, point.x, point.z)
		if l < length:
			length = l
	return length

sqrtOfTwo = math.sqrt(2)
def getDistance(x1, z1, x2, z2):
	shortest = 0
	longest = 0
	horizontalDist = abs(x1 - x2)
	verticalDist = abs(z1 - z2)
	if horizontalDist < verticalDist:
		shortest = horizontalDist
		longest = verticalDist
	else:
		shortest = verticalDist
		longest = horizontalDist
	return shortest * sqrtOfTwo + longest - shortest

def getPathBetweenPoints(surface, points):
	nodes = []
	for i, point in enumerate(points):
		nodes.append(Node(i, point))

	edges = []
	for node in nodes:
		for otherNode in nodes:
			if otherNode.id <= node.id:
				continue
			point1 = node.data
			point2 = otherNode.data
			cost = getDistance(point1.x, point1.z, point2.x, point2.z)
			edges.append(Edge(cost, node.id, otherNode.id))

	minimumSpanningTree = getMinimumSpanningTree(nodes, edges)

	paths = []
	for edge in minimumSpanningTree:
		point1 = getNode(nodes, edge.nodeId1).data
		point2 = getNode(nodes, edge.nodeId2).data
		path = getPath(surface, point1.x, point1.z, point2.x, point2.z)
		paths.append(path)
	return paths

def getNode(nodes, id):
	for node in nodes:
		if node.id == id:
			return node
	return None

def getSectionPairs(surface, sections):
	nodes = []
	for section in sections:
		nodes.append(Node(section.id, section))

	edges = []
	for node in nodes:
		for otherNode in nodes:
			if otherNode.id <= node.id:
				continue
			section1 = node.data
			section2 = otherNode.data
			cost = getShortestIntersectionPathLength(surface, section1, section2)
			edges.append(Edge(cost, node.id, otherNode.id))

	minimumSpanningTree = getMinimumSpanningTree(nodes, edges)

	sectionPairs = []
	for edge in minimumSpanningTree:
		section1 = getNode(nodes, edge.nodeId1).data
		section2 = getNode(nodes, edge.nodeId2).data
		sectionPairs.append((section1, section2))

	return sectionPairs

def getShortestIntersectionPath(surface, section1, section2):
	points1 = section1.pathConnectionPoints
	points2 = section2.pathConnectionPoints
	if not points1:
		points1.append(Point(section1.xMid, section1.zMid))
	if not points2:
		points2.append(Point(section2.xMid, section2.zMid))

	length = sys.maxint
	point1 = None
	point2 = None
	for p1 in points1:
		for p2 in points2:
			l = getDistance(p1.x, p1.z, p2.x, p2.z)
			if l < length:
				length = l
				point1 = p1
				point2 = p2
	path = getPath(surface, point1.x, point1.z, point2.x, point2.z)

	for point in path[:3]:
		section1.exitPoints.append(point)

	for point in path[-1:-4:-1]:
		section2.exitPoints.append(point)

	return path

def getShortestIntersectionPathLength(surface, section1, section2):
	points1 = section1.pathConnectionPoints
	points2 = section2.pathConnectionPoints
	if not points1:
		points1.append(Point(section1.xMid, section1.zMid))
	if not points2:
		points2.append(Point(section2.xMid, section2.zMid))

	length = sys.maxint
	for p1 in points1:
		for p2 in points2:
			l = getDistance(p1.x, p1.z, p2.x, p2.z)
			if l < length:
				length = l
	return length