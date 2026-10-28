import pytest
from graph import adj_matrix_to_adj_list, adj_matrix_to_edge_list, bfs, dfs_iterative, dfs_recursive

adjacency_matrix = [
    [0, 1, 1, 0],
    [1, 0, 1, 0],
    [1, 1, 0, 1],
    [0, 0, 1, 0]
]

@pytest.fixture
def matrix():
    return [
        [0, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 0],
    ]

@pytest.fixture
def adj_list():
    return adj_matrix_to_adj_list(adjacency_matrix)

@pytest.fixture
def empty_matrix():
    return [[0]]

@pytest.fixture
def single_edge():
    return [[0, 1], [1, 0]]

@pytest.fixture
def path_graph():
    # 0 - 1 - 2 - 3
    return [[0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0]]

@pytest.fixture
def disconnected():
    # 0-1,  2-3  (two components)
    return [[0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]]


# ------------------------------------------------------------------
# adj_matrix_to_edge_list
# ------------------------------------------------------------------

class TestAdjMatrixToEdgeList:
    def test_known_graph(self, matrix):
        edges = adj_matrix_to_edge_list(matrix)
        assert edges == [[0, 1], [0, 2], [1, 2], [2, 3]]

    def test_empty_graph(self, empty_matrix):
        assert adj_matrix_to_edge_list(empty_matrix) == []

    def test_single_edge(self, single_edge):
        assert adj_matrix_to_edge_list(single_edge) == [[0, 1]]

    def test_no_duplicate_edges_for_undirected(self, matrix):
        edges = adj_matrix_to_edge_list(matrix)
        assert len(edges) == len({tuple(sorted(e)) for e in edges})

    def test_path_graph(self, path_graph):
        edges = adj_matrix_to_edge_list(path_graph)
        assert edges == [[0, 1], [1, 2], [2, 3]]


# ------------------------------------------------------------------
# adj_matrix_to_adj_list
# ------------------------------------------------------------------

class TestAdjMatrixToAdjList:
    def test_known_graph(self, matrix):
        adj = adj_matrix_to_adj_list(matrix)
        assert len(adj) == 4
        assert sorted(adj[0]) == [1, 2]
        assert sorted(adj[1]) == [0, 2]     # will FAIL with current impl
        assert sorted(adj[2]) == [0, 1, 3]  # will FAIL with current impl
        assert sorted(adj[3]) == [2]        # will FAIL with current impl

    def test_symmetric(self, adj_list):
        n = len(adj_list)
        for u in range(n):
            for v in adj_list[u]:
                assert u in adj_list[v], f"adjacency not symmetric for {u},{v}"

    def test_edge_count_matches(self, matrix):
        adj = adj_matrix_to_adj_list(matrix)
        # each undirected edge appears twice
        undirected = adj_matrix_to_edge_list(matrix)
        total_entries = sum(len(nbrs) for nbrs in adj)
        assert total_entries == 2 * len(undirected)   # FAILS with current impl

    def test_empty_graph(self, empty_matrix):
        assert adj_matrix_to_adj_list(empty_matrix) == [[]]

    def test_single_edge(self, single_edge):
        assert adj_matrix_to_adj_list(single_edge) == [[1], [0]]

    def test_disconnected(self, disconnected):
        adj = adj_matrix_to_adj_list(disconnected)
        assert sorted(adj[0]) == [1]
        assert sorted(adj[1]) == [0]
        assert sorted(adj[2]) == [3]
        assert sorted(adj[3]) == [2]


# ------------------------------------------------------------------
# DFS recursive
# ------------------------------------------------------------------

class TestDfsRecursive:
    def test_visits_all_reachable(self, adj_list):
        order = dfs_recursive(adj_list, 0)
        assert sorted(order) == [0, 1, 2, 3]

    def test_starts_at_given_node(self, adj_list):
        order = dfs_recursive(adj_list, 3)
        assert order[0] == 3

    def test_no_infinite_loop_on_cycle(self, adj_list):
        # cycle 0-1-2-0 must terminate
        order = dfs_recursive(adj_list, 0)
        assert len(order) == len(set(order))

    def test_single_node(self, single_edge):
        adj = adj_matrix_to_adj_list(single_edge)
        assert dfs_recursive(adj, 0) == [0, 1]

    def test_disconnected_stays_in_component(self, disconnected):
        adj = adj_matrix_to_adj_list(disconnected)
        order = dfs_recursive(adj, 0)
        assert set(order) == {0, 1}   # should NOT reach 2 or 3


# ------------------------------------------------------------------
# DFS iterative
# ------------------------------------------------------------------

class TestDfsIterative:
    def test_visits_all_reachable(self, adj_list):
        order = dfs_iterative(adj_list, start=0)
        assert sorted(order) == [0, 1, 2, 3]

    def test_no_duplicates(self, adj_list):
        order = dfs_iterative(adj_list, start=0)
        assert len(order) == len(set(order))

    def test_starts_at_given_node(self, adj_list):
        assert dfs_iterative(adj_list, start=2)[0] == 2

    def test_empty_adj_list(self):
        assert dfs_iterative([[]], start=0) == [0]

    def test_disconnected_stays_in_component(self, disconnected):
        adj = adj_matrix_to_adj_list(disconnected)
        assert set(dfs_iterative(adj, start=2)) == {2, 3}


# ------------------------------------------------------------------
# BFS
# ------------------------------------------------------------------

class TestBfs:
    def test_visits_all_reachable(self, adj_list):
        order = bfs(adj_list, start=0)
        assert sorted(order) == [0, 1, 2, 3]

    def test_level_order(self, adj_list):
        # 0 → {1,2}, then 3
        order = bfs(adj_list, start=0)
        assert order[0] == 0
        assert set(order[1:3]) == {1, 2}
        assert order[3] == 3

    def test_no_duplicates(self, adj_list):
        order = bfs(adj_list, start=0)
        assert len(order) == len(set(order))

    def test_path_graph_order(self, path_graph):
        adj = adj_matrix_to_adj_list(path_graph)
        order = bfs(adj, start=0)
        assert order == [0, 1, 2, 3]

    def test_disconnected(self, disconnected):
        adj = adj_matrix_to_adj_list(disconnected)
        assert set(bfs(adj, start=0)) == {0, 1}

    def test_single_node(self, empty_matrix):
        adj = adj_matrix_to_adj_list(empty_matrix)
        assert bfs(adj, start=0) == [0]


# ------------------------------------------------------------------
# Round-trip properties
# ------------------------------------------------------------------

class TestRoundTrip:
    def test_edge_list_edges_valid_in_matrix(self, matrix):
        n = len(matrix)
        for u, v in adj_matrix_to_edge_list(matrix):
            assert 0 <= u < n and 0 <= v < n
            assert matrix[u][v] == 1

    def test_adj_list_edges_match_edge_list(self, matrix):
        edges = {tuple(sorted(e)) for e in adj_matrix_to_edge_list(matrix)}
        adj = adj_matrix_to_adj_list(matrix)
        adj_edges = set()
        for u, nbrs in enumerate(adj):
            for v in nbrs:
                adj_edges.add(tuple(sorted((u, v))))
        assert edges == adj_edges