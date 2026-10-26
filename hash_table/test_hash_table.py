import pytest
from hash_table import Hash         

# ---------- basic functionality ----------
def test_add_and_get_int():
    h = Hash()
    h["a"] = 1
    assert h["a"] == 1


def test_get_missing_raises():
    h = Hash()
    with pytest.raises(KeyError):
        _ = h["nope"]


def test_update_existing_key():
    h = Hash()
    h[1] = "x"
    h[1] = "y"
    assert h[1] == "y"
    assert len(h) == 1


def test_delete():
    h = Hash()
    h[1] = "a"; h[2] = "b"
    del h[1]
    assert 1 not in h
    assert h[2] == "b"
    with pytest.raises(KeyError):
        _ = h[1]


def test_delete_missing_raises():
    h = Hash()
    with pytest.raises(KeyError):
        del h["missing"]


def test_len_tracks_ops():
    h = Hash()
    for i in range(10):
        h[i] = i
    assert len(h) == 10
    del h[3]
    assert len(h) == 9


# ---------- collision handling ----------
def test_collisions_all_present():
    # force many keys into same bucket by using tiny capacity
    h = Hash(capacity=4, threshold=10.0)   # threshold high → no resize
    for i in range(0, 200, 4):             # all ≡ 0 mod 4
        h[i] = i * 10
    for i in range(0, 200, 4):
        assert h[i] == i * 10


def test_delete_head_of_chain():
    h = Hash(capacity=4, threshold=10.0)
    h[0] = "a"; h[4] = "b"; h[8] = "c"     # same bucket
    del h[0]
    assert 4 in h and 8 in h
    assert 0 not in h


def test_delete_middle_of_chain():
    h = Hash(capacity=4, threshold=10.0)
    h[0] = "a"; h[4] = "b"; h[8] = "c"
    del h[4]
    assert h[0] == "a" and h[8] == "c"


# ---------- resize ----------
def test_resize_preserves_all():
    h = Hash()
    for i in range(100):
        h[i] = i
    assert len(h) == 100
    assert h.capacity > 16               # grew
    for i in range(100):
        assert h[i] == i


def test_resize_actually_rehashes():
    h = Hash(capacity=4, threshold=0.5)
    for i in range(20):
        h[i] = i
    for i in range(20):
        assert h[i] == i


# ---------- generic key types ----------
def test_string_keys():
    h = Hash()
    h["hello"] = 1
    h["world"] = 2
    assert h["hello"] == 1 and h["world"] == 2


def test_float_keys():
    h = Hash()
    h[1.5] = "x"
    assert h[1.5] == "x"


def test_tuple_keys():
    h = Hash()
    h[(1, 2)] = "a"
    h[(1, 3)] = "b"
    assert h[(1, 2)] == "a"
    assert h[(1, 3)] == "b"


def test_bool_and_int_key_equivalence():
    # Python: True == 1 and hash(True) == hash(1) → same slot
    h = Hash()
    h[True] = "yes"
    assert h[1] == "yes"


def test_unhashable_key_raises():
    h = Hash()
    with pytest.raises(TypeError):
        h[[1, 2, 3]] = "list"


def test_custom_hashable_class():
    class Point:
        def __init__(self, x, y):
            self.x, self.y = x, y
        def __hash__(self):
            return hash((self.x, self.y))
        def __eq__(self, other):
            return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)

    h = Hash()
    h[Point(1, 2)] = "p12"
    assert h[Point(1, 2)] == "p12"
    assert Point(1, 3) not in h


# ---------- edge cases ----------
def test_empty_table_lookups():
    h = Hash()
    assert 42 not in h
    assert len(h) == 0


def test_many_keys_string():
    h = Hash()
    words = [f"key_{i}" for i in range(500)]
    for i, w in enumerate(words):
        h[w] = i
    for i, w in enumerate(words):
        assert h[w] == i
    assert len(h) == 500


def test_buckets_not_shared():
    # this catches the `[Node()]*n` aliasing bug
    h = Hash()
    h[0] = "a"
    assert 0 in h
    assert 1 not in h
    assert len(h) == 1