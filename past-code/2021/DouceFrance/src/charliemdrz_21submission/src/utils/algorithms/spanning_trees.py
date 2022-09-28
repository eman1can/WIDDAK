"""
method to compute min spanning tree from points and generate distance maps in these trees
"""
from itertools import product
from typing import List, Set, Tuple

from numpy import full, zeros

from utils import Point, manhattan


def min_spanning_tree(points: List[Point]) -> Set[Tuple[Point, Point]]:
    n = len(points)

    # Init graph
    weights = full((n, n), -1)
    edges = []

    for i, j in filter(lambda ij: ij[0] < ij[1], product(range(n), range(n))):
        weights[i, j] = weights[j, i] = manhattan(points[i], points[j])
        edges.append((i, j))
    edges.sort(key=lambda e: weights[e[0], e[1]])

    # Connected components
    p_to_comp = {i: i for i in range(n)}
    comp_to_p = {i: [i] for i in range(n)}

    def join_components(_c1, _c2):
        for _ in comp_to_p[_c2]:
            p_to_comp[_] = _c1
        comp_to_p[_c1].extend(comp_to_p[_c2])
        del comp_to_p[_c2]

    tree_edges: Set[Tuple[Point, Point]] = set()
    for (i, j) in edges:
        comp_i, comp_j = p_to_comp[i], p_to_comp[j]
        if comp_i != comp_j:
            join_components(comp_i, comp_j)
            tree_edges.add((points[i], points[j]))

    return tree_edges


def tree_distance(edges: Set[Tuple[Point, Point]]):
    vertex_to_index = {}
    for e in edges:
        for u in e:
            if u not in vertex_to_index:
                vertex_to_index[u] = len(vertex_to_index)


    # Connected components
    n = len(vertex_to_index)
    p_to_comp = {i: i for i in range(n)}
    comp_to_p = {i: [i] for i in range(n)}
    distance_map = zeros((n, n))

    def w(edge):
        """Edge weight = manhattan distance between extremities"""
        return manhattan(edge[0], edge[1])

    for e in edges:
        i, j = vertex_to_index[e[0]], vertex_to_index[e[1]]  # vertices of edge e
        ci, cj = p_to_comp[i], p_to_comp[j]  # components of the vertices
        for ni in comp_to_p[ci]:
            for nj in comp_to_p[cj]:
                # for each neighbour ni of point i, each neighbour nj of point j, the distance btwn ni and nj is
                # the distance btwn ni and i + the distance btwn i and j + the distance btwn j and nj (bc tree)
                d = distance_map[ni, i] + w(e) + distance_map[j, nj]
                distance_map[ni, nj] = distance_map[nj, ni] = d

        # merge component cj into component ci
        for _ in comp_to_p[cj]:
            p_to_comp[_] = ci
        comp_to_p[ci].extend(comp_to_p[cj])
        del comp_to_p[cj]

    return {(u, v): distance_map[vertex_to_index[u], vertex_to_index[v]] for u in vertex_to_index for v in vertex_to_index if v != u}


if __name__ == '__main__':
    from random import randint
    from matplotlib import pyplot as plt
    SIZE = 100
    N_POINTS = 15
    points = [Point(randint(0, SIZE), randint(0, SIZE)) for _ in range(N_POINTS)]
    print(points)

    print(tree_distance(min_spanning_tree(points)))

    plt.scatter([_.x for _ in points], [_.z for _ in points])
    for p1, p2 in min_spanning_tree(points):
        plt.plot([p1.x, p2.x], [p1.z, p2.z])
    plt.show()
