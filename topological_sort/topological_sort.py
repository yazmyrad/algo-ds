from collections import defaultdict
from typing import List, Dict

graph = {
    "A": ["B", "C"],
    "B": ["C", "D"],
    "C": ["D"],
    "D": []
}

def topological_sort(graph: Dict[str, List[str]]) -> List[str]:
    tpl = []
    has_cycle = False
    status = defaultdict(int)

    def dfs(node):
        nonlocal has_cycle
        if has_cycle:
            return
        if status[node] == 2:
            return 
        if status[node] == 1:
            has_cycle = True
            return

        status[node] = 1
        for nei in graph[node]:
            dfs(nei)

        status[node] = 2

        tpl.append(node)


    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)

    for node in all_nodes:
        if status[node] == 0:
            dfs(node)

    tpl.reverse()
    return tpl if not has_cycle else []

