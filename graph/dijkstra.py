import heapq
from typing import List, Tuple 

weighted_adj_list: List[List[Tuple[int, int]]] = [
    [(1, 2), (2, 5)],          
    [(0, 2), (3, 3)],          
    [(0, 5), (3, 1)],          
    [(1, 3), (2, 1)],          
]

def shortest_path(graph: List[List[Tuple[int, int]]], start, target):
    n = len(graph)
    dist = [float("inf")] * n
    dist[start] = 0
    hp = [(0, start)]              
    visited = set()
    predecessors = {node: None for node in range(n)}
    while hp:
        d, node = heapq.heappop(hp)
        if node in visited:
            continue
        if node == target:
            return d, predecessors
        visited.add(node)
        for neigh, w in graph[node]:
            nd = d + w
            if nd < dist[neigh]:
                dist[neigh] = nd
                predecessors[neigh] = node
                heapq.heappush(hp, (nd, neigh))

    return None   


def reconstruct_path(predecessors, start_node, target_node):
    path = []
    current = target_node
    while current is not None:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    
    return path if path[0] == start_node else []

