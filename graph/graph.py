from collections import deque
from typing import List


def adj_matrix_to_edge_list(matrix: List[List[int]]) -> List[List[int]]:
    res = []
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        for j in range(i, n):
            if matrix[i][j] == 1:
                res.append([i, j])
    return res

def adj_matrix_to_adj_list(matrix: List[List[int]]) -> List[List[int]]:
    m, n = len(matrix), len(matrix[0])
    res = [[] for _ in range(n)]
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 1:
                res[i].append(j)

    return res

def dfs_recursive(adj_list: List[List[int]], node: int, visited=None):
    if visited is None:
        visited = set()
    if node in visited:
        return []

    visited.add(node)
    res = [node]

    for neigh in adj_list[node]:
        res.extend(dfs_recursive(adj_list, neigh, visited))
    return res

def dfs_iterative(adj_list: List[List[int]], start: int = 0 ):
    stack = [start]
    visited = set()
    res = []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        res.append(node)
        visited.add(node)
        for neigh in adj_list[node]:
            stack.append(neigh)

    return res

def bfs(adj_list: List[List[int]], start=0):
    q = deque([start])
    visited = {start}
    res = []
    while q:
        node = q.popleft()
        res.append(node)
        for neigh in adj_list[node]:
            if neigh not in visited:
                visited.add(neigh)
                q.append(neigh)

    return res

