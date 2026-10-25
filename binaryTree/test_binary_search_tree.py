from __future__ import annotations

import pytest

# Adjust import to wherever your classes live.
from binary_search_tree import BST
from binary_tree import Node


# ---------- fixtures ----------

@pytest.fixture
def empty() -> BST:
    return BST()

@pytest.fixture
def sample() -> BST:
    #       50
    #      /  \
    #    30    70
    #   /  \   / \
    # 20   40 60  80
    bst = BST()
    bst.build_tree([50, 30, 70, 20, 40, 60, 80])
    return bst

@pytest.fixture
def left_skewed() -> BST:
    bst = BST()
    for v in (5, 4, 3, 2, 1):
        bst.insert(v)
    return bst

@pytest.fixture
def right_skewed() -> BST:
    bst = BST()
    for v in (1, 2, 3, 4, 5):
        bst.insert(v)
    return bst

@pytest.fixture
def single() -> BST:
    bst = BST()
    bst.insert(42)
    return bst


# ---------- construction / build ----------

class TestBuildTree:
    def test_empty_init(self, empty: BST):
        assert empty.get_node_count() == 0
        assert empty.get_height() == 0
        assert empty.is_bst()

    def test_build_from_list(self, sample: BST):
        assert sample.get_node_count() == 7

    def test_init_with_values(self):
        bst = BST([50, 30, 70])
        assert bst.get_node_count() == 3
        assert bst.is_in_tree(50)
        assert bst.is_in_tree(30)
        assert bst.is_in_tree(70)

    def test_build_empty_list(self, empty: BST):
        empty.build_tree([])
        assert empty.get_node_count() == 0

    def test_build_duplicates_ignored_or_counted(self):
        # Decide your contract: typical BST ignores duplicates.
        bst = BST()
        bst.build_tree([1, 2, 2, 3])
        assert bst.get_node_count() == 3  # change to 4 if you keep dups

    def test_instances_do_not_share_root(self):
        a = BST([1, 2, 3])
        b = BST([10, 20, 30])
        assert a.get_node_count() == 3
        assert b.get_node_count() == 3
        assert not a.is_in_tree(10)
        assert not b.is_in_tree(1)


# ---------- insert ----------

class TestInsert:
    def test_insert_into_empty(self, empty: BST):
        empty.insert(10)
        assert empty.get_node_count() == 1
        assert empty.is_in_tree(10)

    def test_insert_multiple(self, empty: BST):
        for v in (50, 30, 70, 20, 40):
            empty.insert(v)
        assert empty.get_node_count() == 5
        assert empty.is_bst()

    def test_insert_duplicate(self, single: BST):
        single.insert(42)
        # Ignored duplicate -> still 1 node. Change if you allow dups.
        assert single.get_node_count() == 1

    def test_insert_preserves_bst(self, sample: BST):
        sample.insert(55)
        sample.insert(45)
        assert sample.is_bst()
        assert sample.get_node_count() == 9


# ---------- count ----------

class TestNodeCount:
    def test_count_empty(self, empty: BST):
        assert empty.get_node_count() == 0

    def test_count_single(self, single: BST):
        assert single.get_node_count() == 1

    def test_count_sample(self, sample: BST):
        assert sample.get_node_count() == 7

    def test_count_after_delete(self, sample: BST):
        sample.delete_value(30)
        assert sample.get_node_count() == 6


# ---------- print_values (in-order) ----------

class TestPrintValues:
    def test_print_empty(self, empty: BST, capsys):
        empty.print_values()
        out = capsys.readouterr().out
        # Accept "[]" or empty/whitespace output.
        assert out.strip() in ("", "[]")

    def test_print_sample_sorted(self, sample: BST, capsys):
        sample.print_values()
        out = capsys.readouterr().out
        # Expect ascending order in some bracketed/comma form.
        nums = [int(n) for n in __import__("re").findall(r"-?\d+", out)]
        assert nums == [20, 30, 40, 50, 60, 70, 80]

    def test_print_single(self, single: BST, capsys):
        single.print_values()
        out = capsys.readouterr().out
        assert "42" in out


# ---------- delete_tree ----------

class TestDeleteTree:
    def test_delete_empty(self, empty: BST):
        empty.delete_tree()
        assert empty.get_node_count() == 0

    def test_delete_populated(self, sample: BST):
        sample.delete_tree()
        assert sample.get_node_count() == 0
        assert sample.get_height() == 0
        assert not sample.is_in_tree(50)

    def test_reuse_after_delete(self, sample: BST):
        sample.delete_tree()
        sample.insert(7)
        assert sample.get_node_count() == 1
        assert sample.is_in_tree(7)


# ---------- is_in_tree ----------

class TestIsInTree:
    def test_not_in_empty(self, empty: BST):
        assert not empty.is_in_tree(1)

    @pytest.mark.parametrize("val", [20, 30, 40, 50, 60, 70, 80])
    def test_values_present(self, sample: BST, val: int):
        assert sample.is_in_tree(val)

    @pytest.mark.parametrize("val", [10, 25, 45, 55, 65, 75, 90, -1])
    def test_values_absent(self, sample: BST, val: int):
        assert not sample.is_in_tree(val)


# ---------- height ----------

class TestHeight:
    def test_height_empty(self, empty: BST):
        assert empty.get_height() == 0

    def test_height_single(self, single: BST):
        assert single.get_height() == 1

    def test_height_sample(self, sample: BST):
        # 3 levels: 50 / {30,70} / {20,40,60,80}
        assert sample.get_height() == 3

    def test_height_left_skewed(self, left_skewed: BST):
        assert left_skewed.get_height() == 5

    def test_height_right_skewed(self, right_skewed: BST):
        assert right_skewed.get_height() == 5

    def test_height_after_insert_deepens(self, sample: BST):
        sample.insert(10)   # 50-30-20-10
        assert sample.get_height() == 4


# ---------- min / max ----------

class TestMinMax:
    def test_min_empty_raises(self, empty: BST):
        with pytest.raises((ValueError, IndexError, RuntimeError)):
            empty.get_min()

    def test_max_empty_raises(self, empty: BST):
        with pytest.raises((ValueError, IndexError, RuntimeError)):
            empty.get_max()

    def test_min_sample(self, sample: BST):
        assert sample.get_min() == 20

    def test_max_sample(self, sample: BST):
        assert sample.get_max() == 80

    def test_min_single(self, single: BST):
        assert single.get_min() == 42

    def test_max_single(self, single: BST):
        assert single.get_max() == 42

    def test_min_skewed(self, left_skewed: BST):
        assert left_skewed.get_min() == 1

    def test_max_skewed(self, right_skewed: BST):
        assert right_skewed.get_max() == 5


# ---------- delete_value ----------

class TestDeleteValue:
    def test_delete_leaf(self, sample: BST):
        assert sample.delete_value(20) is True
        assert sample.get_node_count() == 6
        assert not sample.is_in_tree(20)
        assert sample.is_bst()

    def test_delete_node_with_one_child(self, sample: BST):
        assert sample.delete_value(70) is True   # 70 has 60,80 -> two children!
        # Use a real one-child case instead:
        bst = BST()
        for v in (50, 30, 20):  # 30 has one child (20)
            bst.insert(v)
        assert bst.delete_value(30) is True
        assert bst.is_in_tree(20)
        assert bst.is_bst()
        assert bst.get_node_count() == 2

    def test_delete_node_with_two_children(self, sample: BST):
        assert sample.delete_value(30) is True   # 30 -> {20, 40}
        assert not sample.is_in_tree(30)
        assert sample.get_node_count() == 6
        assert sample.is_bst()

    def test_delete_root(self, sample: BST):
        assert sample.delete_value(50) is True
        assert not sample.is_in_tree(50)
        assert sample.get_node_count() == 6
        assert sample.is_bst()

    def test_delete_missing_value(self, sample: BST):
        assert sample.delete_value(999) is False
        assert sample.get_node_count() == 7

    def test_delete_from_empty(self, empty: BST):
        assert empty.delete_value(1) is False

    def test_delete_only_node(self, single: BST):
        assert single.delete_value(42) is True
        assert single.get_node_count() == 0
        assert single.get_height() == 0

    def test_delete_all_values(self, sample: BST):
        for v in [20, 30, 40, 50, 60, 70, 80]:
            assert sample.delete_value(v) is True
            assert sample.is_bst()
        assert sample.get_node_count() == 0
        assert sample.get_height() == 0


# ---------- successor ----------

class TestSuccessor:
    def test_successor_of_leaf(self, sample: BST):
        # in-order: 20,30,40,50,60,70,80
        assert sample.get_successor(20) == 30

    def test_successor_of_internal(self, sample: BST):
        assert sample.get_successor(40) == 50

    def test_successor_of_root(self, sample: BST):
        assert sample.get_successor(50) == 60

    def test_successor_of_max_returns_none_or_raises(self, sample: BST):
        # Pick ONE contract and keep it. This accepts None only.
        assert sample.get_successor(80) == -1

    def test_successor_missing_value(self, sample: BST):
        assert sample.get_successor(25) == -1

    def test_successor_empty(self, empty: BST):
        assert empty.get_successor(1) == -1

    def test_successor_min_of_sample(self, sample: BST):
        assert sample.get_successor(20) == 30


# ---------- is_bst ----------

class TestIsBst:
    def test_empty_is_bst(self, empty: BST):
        assert empty.is_bst() is True

    def test_single_is_bst(self, single: BST):
        assert single.is_bst() is True

    def test_sample_is_bst(self, sample: BST):
        assert sample.is_bst() is True

    def test_skewed_is_bst(self, left_skewed: BST, right_skewed: BST):
        assert left_skewed.is_bst() is True
        assert right_skewed.is_bst() is True

    def test_manually_broken_tree_not_bst(self):
        # Build by hand, bypassing insert(), to violate the invariant.
        bst = BST()
        root = Node()
        root.val = 10
        left = Node(); left.val = 5
        right = Node(); right.val = 20
        # Violation: left.left = 15 > root.val is fine, but 15 > 10
        bad = Node(); bad.val = 15
        left.right = bad
        root.left = left
        root.right = right
        root.left = left
        bst._root = root
        assert bst.is_bst() is False

    def test_equal_values_not_strictly_bst(self):
        # If your BST forbids duplicates, a tree with equal keys is not a BST.
        bst = BST()
        root = Node(); root.val = 10
        left = Node(); left.val = 10
        root.left = left
        bst._root = root
        assert bst.is_bst() is False   # change to True if you allow dups