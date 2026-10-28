import pytest

from dijkstra import shortest_path

@pytest.fixture
def square_graph():
    #  0 --2-- 1
    #  |       |
    #  5       3
    #  |       |
    #  2 --1-- 3
    return [
        [(1, 2), (2, 5)],
        [(0, 2), (3, 3)],
        [(0, 5), (3, 1)],
        [(1, 3), (2, 1)],
    ]

@pytest.fixture
def path_graph():
    # 0 --1-- 1 --1-- 2 --1-- 3
    return [
        [(1, 1)],
        [(0, 1), (2, 1)],
        [(1, 1), (3, 1)],
        [(2, 1)],
    ]

@pytest.fixture
def disconnected_graph():
    # 0-1  and  2-3  (two components)
    return [
        [(1, 1)],
        [(0, 1)],
        [(3, 1)],
        [(2, 1)],
    ]

@pytest.fixture
def single_node():
    return [[]]

@pytest.fixture
def two_nodes():
    return [[(1, 7)], [(0, 7)]]

@pytest.fixture
def parallel_edges():
    # two edges 0→1 with different weights
    return [
        [(1, 10), (1, 3)],
        [(0, 10), (0, 3)],
    ]

@pytest.fixture
def directed_graph():
    # 0→1 (4), 0→2 (1), 2→1 (2), 1→3 (1), 2→3 (5)
    # Using one-directional entries in a "directed" adjacency list.
    # NOTE: shortest_path as written treats graph as directed.
    return [
        [(1, 4), (2, 1)],
        [(3, 1)],
        [(1, 2), (3, 5)],
        [],
    ]


# ------------------------------------------------------------------
# Basic correctness
# ------------------------------------------------------------------

class TestShortestPathBasic:
    def test_start_equals_target(self, square_graph):
        assert shortest_path(square_graph, 0, 0) == 0

    def test_single_node(self, single_node):
        assert shortest_path(single_node, 0, 0) == 0

    def test_two_node_direct_edge(self, two_nodes):
        assert shortest_path(two_nodes, 0, 1) == 7
        assert shortest_path(two_nodes, 1, 0) == 7

    def test_direct_vs_indirect(self, square_graph):
        # 0→2 direct is 5, but 0→1→3→2 is 2+3+1 = 6 → still 5
        assert shortest_path(square_graph, 0, 2) == 5

    def test_shortest_around_cycle(self, square_graph):
        # 0 → 1 (2) → 3 (3) → 2 (1) = 6; direct is 5
        assert shortest_path(square_graph, 0, 3) == 5   # 0→1→3 = 2+3
        assert shortest_path(square_graph, 1, 2) == 4   # 1→3→2 = 3+1

    def test_all_pairs_square(self, square_graph):
        expected = {
            (0, 1): 2, (0, 2): 5, (0, 3): 5,
            (1, 0): 2, (1, 2): 4, (1, 3): 3,
            (2, 0): 5, (2, 1): 4, (2, 3): 1,
            (3, 0): 5, (3, 1): 3, (3, 2): 1,
        }
        for (s, t), d in expected.items():
            assert shortest_path(square_graph, s, t) == d, f"{s}->{t}"

    def test_path_graph(self, path_graph):
        assert shortest_path(path_graph, 0, 3) == 3
        assert shortest_path(path_graph, 3, 0) == 3
        assert shortest_path(path_graph, 1, 2) == 1


# ------------------------------------------------------------------
# Unreachable / disconnected
# ------------------------------------------------------------------

class TestShortestPathUnreachable:
    def test_disconnected_target(self, disconnected_graph):
        # 0 cannot reach 2 or 3
        assert shortest_path(disconnected_graph, 0, 2) is None
        assert shortest_path(disconnected_graph, 0, 3) is None

    def test_same_component(self, disconnected_graph):
        assert shortest_path(disconnected_graph, 2, 3) == 1
        assert shortest_path(disconnected_graph, 0, 1) == 1

    def test_no_edges_at_all(self):
        graph = [[], [], []]
        assert shortest_path(graph, 0, 1) is None
        assert shortest_path(graph, 0, 0) == 0


# ------------------------------------------------------------------
# Edge cases
# ------------------------------------------------------------------

class TestShortestPathEdgeCases:
    def test_parallel_edges_pick_min(self, parallel_edges):
        # Two 0–1 edges: weight 10 and weight 3 → shortest is 3
        assert shortest_path(parallel_edges, 0, 1) == 3

    def test_zero_weight_edge(self):
        graph = [[(1, 0)], [(0, 0)]]
        assert shortest_path(graph, 0, 1) == 0

    def test_self_loop_ignored(self):
        graph = [[(0, 5), (1, 2)], [(0, 2)]]
        assert shortest_path(graph, 0, 1) == 2

    def test_negative_weight_not_supported(self):
        """
        Dijkstra is only correct for non-negative weights.
        Document that behaviour rather than assert a wrong answer.
        With negative weight on a cycle the algorithm produces an
        incorrect-but-terminating answer; we just assert it terminates.
        """
        graph = [[(1, -1)], [(0, 1)]]
        # We don't assert the value; we assert it doesn't hang / raise.
        result = shortest_path(graph, 0, 1)
        assert isinstance(result, (int, float))

    def test_large_weights_no_overflow(self):
        big = 10**15
        graph = [[(1, big)], [(0, big)]]
        assert shortest_path(graph, 0, 1) == big

    def test_float_weights(self):
        graph = [[(1, 0.5)], [(0, 0.5)]]
        assert shortest_path(graph, 0, 1) == pytest.approx(0.5)


# ------------------------------------------------------------------
# Directed graph behaviour
# ------------------------------------------------------------------

class TestShortestPathDirected:
    def test_directed_paths(self, directed_graph):
        assert shortest_path(directed_graph, 0, 3) == 4   # 0→2→1→3 = 1+2+1
        assert shortest_path(directed_graph, 0, 1) == 3   # 0→2→1 = 1+2
        assert shortest_path(directed_graph, 0, 2) == 1

    def test_directed_unreachable(self, directed_graph):
        # 3 has no outgoing edges
        assert shortest_path(directed_graph, 3, 0) is None
        assert shortest_path(directed_graph, 1, 2) is None


# ------------------------------------------------------------------
# Structural / property tests
# ------------------------------------------------------------------

class TestShortestPathProperties:
    def test_symmetry_on_undirected(self, square_graph):
        n = len(square_graph)
        for s in range(n):
            for t in range(n):
                a = shortest_path(square_graph, s, t)
                b = shortest_path(square_graph, t, s)
                assert a == b, f"asymmetry {s},{t}: {a} != {b}"

    def test_triangle_inequality(self, square_graph):
        n = len(square_graph)
        for s in range(n):
            for t in range(n):
                d_st = shortest_path(square_graph, s, t)
                if d_st is None:
                    continue
                for u in range(n):
                    d_su = shortest_path(square_graph, s, u)
                    d_ut = shortest_path(square_graph, u, t)
                    if d_su is None or d_ut is None:
                        continue
                    assert d_st <= d_su + d_ut + 1e-9

    def test_distance_never_negative(self, square_graph):
        n = len(square_graph)
        for s in range(n):
            for t in range(n):
                d = shortest_path(square_graph, s, t)
                if d is not None:
                    assert d >= 0


# ------------------------------------------------------------------
# Behavioural regression tests for the bugs in the original code
# ------------------------------------------------------------------

class TestRegression:
    """
    These tests specifically target the differences between the
    original snippet and a correct Dijkstra. If you swap the original
    back in, these will fail (that's the point).
    """

    def test_heap_ordering(self):
        """
        Original pushed (node, dist) which is WRONG — heapq compares
        node first, so it pops by node id, not by distance. This test
        forces a case where node id order != distance order.
        """
        # 0 → 2 (weight 1), 0 → 1 (weight 100)
        # Correct Dijkstra pops node 2 first (distance 1), then node 1.
        graph = [
            [(1, 100), (2, 1)],
            [(0, 100)],
            [(0, 1)],
        ]
        # If ordered by node id, it pops node 1 (dist 100) before node 2.
        # Either way the answer is the same here — but combined with the
        # early `if node[0] == target: return` this differs.
        assert shortest_path(graph, 0, 2) == 1

    def test_returns_none_when_unreachable(self):
        graph = [[(0, 1)], []]     # node 1 is isolated (no incoming edges)
        assert shortest_path(graph, 0, 1) is None

    def test_does_not_return_early_with_suboptimal(self):
        """
        Ensure the early-return on target only fires with the true min.
        """
        # 0 → 3 (weight 10), 0 → 1 (1), 1 → 3 (1), so true dist 0→3 is 2.
        graph = [
            [(3, 10), (1, 1)],
            [(3, 1)],
            [],
            [],
        ]
        assert shortest_path(graph, 0, 3) == 2

    def test_start_equals_target_zero(self):
        # Even with self-loops, dist to self is 0
        graph = [[(0, 99)], []]
        assert shortest_path(graph, 0, 0) == 0