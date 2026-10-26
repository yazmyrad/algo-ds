# test_max_heap.py
from __future__ import annotations

import random

import pytest

from heap import MaxHeap 


# ---------------------------------------------------------------- helpers

def is_valid_max_heap(h: MaxHeap) -> bool:
    """Every parent >= both children."""
    a = h.heap
    n = len(a)
    for i in range(n):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and a[i] < a[left]:
            return False
        if right < n and a[i] < a[right]:
            return False
    return True


def drain(h: MaxHeap) -> list[int]:
    """Extract everything; result must be non-increasing."""
    out = []
    while not h.is_empty():
        out.append(h.extract_max())
    return out


# ---------------------------------------------------------------- fixtures

@pytest.fixture
def empty() -> MaxHeap:
    return MaxHeap()

@pytest.fixture
def single() -> MaxHeap:
    h = MaxHeap()
    h.insert(42)
    return h

@pytest.fixture
def sample() -> MaxHeap:
    h = MaxHeap()
    for v in [3, 1, 4, 1, 5, 9, 2, 6]:
        h.insert(v)
    return h


# ================================================================ insert

class TestInsert:
    def test_insert_into_empty(self, empty: MaxHeap):
        empty.insert(10)
        assert empty.get_size() == 1
        assert empty.get_max() == 10
        assert is_valid_max_heap(empty)

    def test_insert_ascending(self):
        h = MaxHeap()
        for v in range(10):
            h.insert(v)
        assert h.get_max() == 9
        assert is_valid_max_heap(h)

    def test_insert_descending(self):
        h = MaxHeap()
        for v in range(10, 0, -1):
            h.insert(v)
        assert h.get_max() == 10
        assert is_valid_max_heap(h)

    def test_insert_sift_up_reaches_root(self):
        # Regression: shift_up must bubble all the way, not stop after 1 swap.
        h = MaxHeap()
        for v in [1, 2, 3, 4, 5]:
            h.insert(v)
        assert h.heap[0] == 5
        assert is_valid_max_heap(h)

    def test_insert_duplicates_allowed(self):
        h = MaxHeap()
        for v in [5, 5, 5]:
            h.insert(v)
        assert h.get_size() == 3
        assert drain(h) == [5, 5, 5]

    def test_insert_zero(self):
        # Regression: `if left and right` must not treat 0 as "no child".
        h = MaxHeap()
        for v in [0, 1, 0, 2]:
            h.insert(v)
        assert is_valid_max_heap(h)
        assert drain(h) == [2, 1, 0, 0]

    def test_insert_negative(self):
        h = MaxHeap()
        for v in [-3, -1, -7]:
            h.insert(v)
        assert h.get_max() == -1
        assert is_valid_max_heap(h)


# ================================================================ get_max

class TestGetMax:
    def test_get_max_empty_raises(self, empty: MaxHeap):
        with pytest.raises(ValueError):
            empty.get_max()

    def test_get_max_single(self, single: MaxHeap):
        assert single.get_max() == 42

    def test_get_max_does_not_remove(self, sample: MaxHeap):
        before = sample.get_size()
        _ = sample.get_max()
        assert sample.get_size() == before

    def test_get_max_peek_is_root(self, sample: MaxHeap):
        assert sample.get_max() == sample.heap[0] == 9


# ================================================================ size / empty

class TestSizeAndEmpty:
    def test_empty_initially(self, empty: MaxHeap):
        assert empty.get_size() == 0
        assert empty.is_empty() is True

    def test_size_grows(self, empty: MaxHeap):
        for i, v in enumerate([1, 2, 3], start=1):
            empty.insert(v)
            assert empty.get_size() == i
            assert empty.is_empty() is False

    def test_size_after_extract(self, sample: MaxHeap):
        n = sample.get_size()
        sample.extract_max()
        assert sample.get_size() == n - 1

    def test_size_after_remove(self, sample: MaxHeap):
        n = sample.get_size()
        sample.remove(4)
        assert sample.get_size() == n - 1

    def test_len_if_implemented(self, sample: MaxHeap):
        # Optional: only run if you added __len__
        if hasattr(sample, "__len__"):
            assert len(sample) == sample.get_size()


# ================================================================ extract_max

class TestExtractMax:
    def test_extract_empty_raises(self, empty: MaxHeap):
        with pytest.raises(ValueError):
            empty.extract_max()

    def test_extract_single(self, single: MaxHeap):
        assert single.extract_max() == 42
        assert single.is_empty()
        assert is_valid_max_heap(single)

    def test_extract_returns_descending(self, sample: MaxHeap):
        assert drain(sample) == [9, 6, 5, 4, 3, 2, 1, 1]

    def test_extract_keeps_heap_valid(self, sample: MaxHeap):
        while not sample.is_empty():
            sample.extract_max()
            assert is_valid_max_heap(sample)

    def test_extract_all_from_ascending(self):
        h = MaxHeap()
        for v in range(10):
            h.insert(v)
        assert drain(h) == list(range(9, -1, -1))


# ================================================================ shift_up / shift_down

class TestShiftUp:
    def test_shift_up_bubbles_to_root(self):
        h = MaxHeap()
        # Heap-valid except the new element at idx 4:
        h.heap = [10, 9, 8, 7, 20]
        h.shift_up(4)
        assert h.heap[0] == 20
        assert is_valid_max_heap(h)

    def test_shift_up_no_op_at_root(self):
        h = MaxHeap()
        h.heap = [10]
        h.shift_up(0)
        assert h.heap == [10]

    def test_shift_up_stops_when_parent_bigger(self):
        h = MaxHeap()
        h.heap = [10, 9, 8, 1]     # valid heap; shift_up(3) should be no-op
        before = h.heap[:]
        h.shift_up(3)
        assert h.heap == before


class TestShiftDown:
    def test_shift_down_picks_larger_child(self):
        # Regression: `5, 10, 9` used to break out without swapping.
        h = MaxHeap()
        h.heap = [5, 10, 9]
        h.shift_down(0)
        assert h.heap[0] == 10
        assert is_valid_max_heap(h)

    def test_shift_down_both_children_larger(self):
        h = MaxHeap()
        h.heap = [5, 10, 20]
        h.shift_down(0)
        assert h.heap[0] == 20
        assert is_valid_max_heap(h)

    def test_shift_down_handles_zero_child(self):
        # Regression: truthiness check treated 0 as "no child".
        h = MaxHeap()
        h.heap = [1, 0]
        h.shift_down(0)
        assert h.heap[0] == 1
        assert is_valid_max_heap(h)

    def test_shift_down_leaf_is_no_op(self):
        h = MaxHeap()
        h.heap = [10, 5, 3]
        before = h.heap[:]
        h.shift_down(2)
        assert h.heap == before

    def test_shift_down_from_root_full_tree(self):
        h = MaxHeap()
        h.heap = [1, 9, 8, 7, 6, 5, 4]
        h.shift_down(0)
        assert is_valid_max_heap(h)


# ================================================================ remove

class TestRemove:
    def test_remove_empty_raises(self, empty: MaxHeap):
        with pytest.raises(ValueError):
            empty.remove(1)

    def test_remove_missing_raises(self, sample: MaxHeap):
        with pytest.raises(ValueError):
            sample.remove(999)

    def test_remove_root(self, sample: MaxHeap):
        sample.remove(9)
        assert not any(v == 9 for v in sample.heap)
        assert is_valid_max_heap(sample)
        assert sample.get_size() == 7

    def test_remove_leaf(self, sample: MaxHeap):
        sample.remove(1)  # one of the two 1s
        assert sample.get_size() == 7
        assert is_valid_max_heap(sample)
        assert 1 in sample.heap  # the other one survives

    def test_remove_single(self, single: MaxHeap):
        single.remove(42)
        assert single.is_empty()

    def test_remove_only_the_last_index(self):
        h = MaxHeap()
        for v in [10, 9, 8]:
            h.insert(v)
        h.remove(8)  # leaf at last index
        assert is_valid_max_heap(h)
        assert drain(h) == [10, 9]

    def test_remove_preserves_remaining(self, sample: MaxHeap):
        expected = sorted(sample.heap)
        expected.remove(4)
        sample.remove(4)
        assert drain(sample) == list(reversed(expected))

    def test_remove_all_one_by_one(self):
        h = MaxHeap()
        vals = [5, 3, 8, 1, 9, 2, 7]
        for v in vals:
            h.insert(v)
        for v in vals:
            h.remove(v)
            assert is_valid_max_heap(h)
        assert h.is_empty()


# ================================================================ heapify

class TestHeapify:
    def test_heapify_empty_list(self, empty: MaxHeap):
        empty.heapify([])
        assert empty.is_empty()

    def test_heapify_single(self):
        h = MaxHeap()
        h.heapify([7])
        assert h.get_size() == 1
        assert h.get_max() == 7
        assert is_valid_max_heap(h)

    def test_heapify_builds_valid_heap(self):
        h = MaxHeap()
        h.heapify([3, 1, 4, 1, 5, 9, 2, 6])
        assert is_valid_max_heap(h)
        assert h.get_max() == 9
        assert h.get_size() == 8

    def test_heapify_ascending_input(self):
        # Worst case for naive insert; O(n) build should still be correct.
        h = MaxHeap()
        h.heapify(list(range(100)))
        assert h.get_max() == 99
        assert h.get_size() == 100
        assert is_valid_max_heap(h)

    def test_heapify_descending_input(self):
        h = MaxHeap()
        h.heapify(list(range(100, 0, -1)))
        assert h.get_max() == 100
        assert is_valid_max_heap(h)

    def test_heapify_duplicates(self):
        h = MaxHeap()
        h.heapify([2, 2, 2, 2])
        assert h.get_size() == 4
        assert drain(h) == [2, 2, 2, 2]

    def test_heapify_negatives_and_zero(self):
        h = MaxHeap()
        h.heapify([-3, 0, -1, -7, 0])
        assert is_valid_max_heap(h)
        assert h.get_max() == 0
        assert drain(h) == [0, 0, -1, -3, -7]

    def test_heapify_matches_sequential_insert(self):
        vals = [3, 1, 4, 1, 5, 9, 2, 6]
        a, b = MaxHeap(), MaxHeap()
        a.heapify(vals)
        for v in vals:
            b.insert(v)
        assert drain(a) == drain(b)

    def test_heapify_replaces_existing_contents(self):
        # Contract: heapify starts from nums, not from the current heap.
        h = MaxHeap()
        for v in [100, 200]:
            h.insert(v)
        h.heapify([1, 2, 3])
        assert h.get_size() == 3
        assert h.get_max() == 3
        assert sorted(h.heap) == [1, 2, 3]

    def test_heapify_does_not_alias_input(self):
        # Mutating nums afterward must not corrupt the heap
        nums = [3, 1, 4, 1, 5]
        h = MaxHeap()
        h.heapify(nums)
        nums[0] = 999
        assert h.get_max() == 5
        assert is_valid_max_heap(h)

    def test_heapify_is_on_time(self):
        # Sanity: 10_000 elems should be fast for O(n); this is a smoke test,
        # not a benchmark. If heapify were O(n log n) by repeated insert,
        # this would still pass but much slower — do not use as a perf gate.
        import time
        h = MaxHeap()
        nums = list(range(10_000))
        t0 = time.perf_counter()
        h.heapify(nums)
        dt = time.perf_counter() - t0
        assert dt < 1.0  # generous; O(n) is ~ms, O(n log n) is still < 1s
        assert h.get_max() == 9_999


# ================================================================ heap_sort
# Contract: heap_sort(nums) sorts `nums` IN PLACE, ascending, returns None.
# The tests check `nums` after the call. They do NOT assume self is reusable
# afterwards (heap_sort may clobber self.heap); a separate test covers that
# only if your implementation promises it.

class TestHeapSort:
    def test_heap_sort_empty(self):
        nums: list[int] = []
        MaxHeap().heap_sort(nums)
        assert nums == []

    def test_heap_sort_single(self):
        nums = [42]
        MaxHeap().heap_sort(nums)
        assert nums == [42]

    def test_heap_sort_two(self):
        nums = [2, 1]
        MaxHeap().heap_sort(nums)
        assert nums == [1, 2]

    def test_heap_sort_random(self):
        nums = [3, 1, 4, 1, 5, 9, 2, 6]
        MaxHeap().heap_sort(nums)
        assert nums == sorted([3, 1, 4, 1, 5, 9, 2, 6])

    def test_heap_sort_already_sorted(self):
        nums = [1, 2, 3, 4, 5]
        MaxHeap().heap_sort(nums)
        assert nums == [1, 2, 3, 4, 5]

    def test_heap_sort_reverse_sorted(self):
        nums = [5, 4, 3, 2, 1]
        MaxHeap().heap_sort(nums)
        assert nums == [1, 2, 3, 4, 5]

    def test_heap_sort_duplicates(self):
        nums = [3, 3, 1, 3, 2, 2, 1]
        MaxHeap().heap_sort(nums)
        assert nums == [1, 1, 2, 2, 3, 3, 3]

    def test_heap_sort_negatives_and_zero(self):
        nums = [0, -1, 2, 2, -5, 10, -10]
        MaxHeap().heap_sort(nums)
        assert nums == [-10, -5, -1, 0, 2, 2, 10]

    def test_heap_sort_all_equal(self):
        nums = [7] * 50
        MaxHeap().heap_sort(nums)
        assert nums == [7] * 50

    def test_heap_sort_returns_none(self):
        # In-place contract: return value is None.
        assert MaxHeap().heap_sort([3, 1, 2]) is None

    def test_heap_sort_is_in_place(self):
        # Identity check: same list object, contents mutated.
        nums = [3, 1, 4, 1, 5]
        ident = id(nums)
        MaxHeap().heap_sort(nums)
        assert id(nums) == ident
        assert nums == sorted([3, 1, 4, 1, 5])

    @pytest.mark.parametrize("size", [1, 2, 3, 7, 16, 31, 64, 100])
    def test_heap_sort_sizes(self, size: int):
        rng = random.Random(size)
        nums = [rng.randint(-100, 100) for _ in range(size)]
        expected = sorted(nums)
        MaxHeap().heap_sort(nums)
        assert nums == expected

    def test_heap_sort_reusable_across_calls(self):
        h = MaxHeap()
        a = [3, 1, 2]
        b = [9, 7, 8]
        h.heap_sort(a)
        h.heap_sort(b)
        assert a == [1, 2, 3]
        assert b == [7, 8, 9]

    def test_heap_sort_object_still_usable_afterward(self):
        # If your implementation leaves self.heap as scratch, this will fail.
        # Either reset self.heap in heap_sort, or delete this test.
        h = MaxHeap()
        for v in [10, 5, 20]:
            h.insert(v)
        h.heap_sort([3, 1, 2])
        # Either self is intact or was cleared — assert whichever you promise.
        # Common choice: heap_sort clears self.heap.
        if h.get_size() != 0:
            assert is_valid_max_heap(h)
# ================================================================ randomized / invariant

class TestRandomized:
    @pytest.mark.parametrize("seed", range(5))
    def test_random_ops_keep_heap_valid(self, seed: int):
        rng = random.Random(seed)
        h = MaxHeap()
        model: list[int] = []
        for _ in range(200):
            op = rng.choice(["insert", "insert", "extract", "remove", "heapify"])
            if op == "insert" or not model:
                v = rng.randint(-50, 50)
                h.insert(v)
                model.append(v)
            elif op == "extract":
                assert h.extract_max() == max(model)
                model.remove(max(model))
            elif op == "remove":
                v = rng.choice(model)
                h.remove(v)
                model.remove(v)
            elif op == "heapify":
                # only use heapify to rebuild from the model
                h.heapify(model)
            assert is_valid_max_heap(h)
            assert h.get_size() == len(model)
        assert sorted(h.heap) == sorted(model)

    @pytest.mark.parametrize("seed", range(3))
    def test_random_heap_sort(self, seed: int):
        rng = random.Random(seed)
        nums = [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 200))]
        expected = sorted(nums)
        MaxHeap().heap_sort(nums)
        assert nums == expected