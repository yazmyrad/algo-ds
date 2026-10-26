from typing import Any, Hashable, Optional


class Node:
    __slots__ = ("key", "val", "next")

    def __init__(self, key: Hashable = None, val: Any = None, nxt: Optional["Node"] = None):
        self.key = key
        self.val = val
        self.next = nxt


class Hash:
    def __init__(self, capacity: int = 16, threshold: float = 0.85):
        self.capacity = capacity
        self.threshold = threshold
        self.curr_len = 0
        self.buckets: list[Optional[Node]] = [None] * self.capacity

    def _hash(self, key: Hashable) -> int:
        return hash(key) % self.capacity

    def __setitem__(self, key: Hashable, value: Any) -> None:
        idx = self._hash(key)
        node = self.buckets[idx]
        while node is not None:
            if node.key == key:
                node.val = value          
                return
            node = node.next
        self.buckets[idx] = Node(key, value, self.buckets[idx])
        self.curr_len += 1
        if self.curr_len / self.capacity > self.threshold:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        node = self.buckets[self._hash(key)]
        while node is not None:
            if node.key == key:
                return node.val
            node = node.next
        raise KeyError(key)

    def __delitem__(self, key: Hashable) -> None:
        idx = self._hash(key)
        node = self.buckets[idx]
        prev = None
        while node is not None:
            if node.key == key:
                if prev is None:
                    self.buckets[idx] = node.next
                else:
                    prev.next = node.next
                self.curr_len -= 1
                return
            prev, node = node, node.next
        raise KeyError(key)

    def __contains__(self, key: Hashable) -> bool:
        node = self.buckets[self._hash(key)]
        while node is not None:
            if node.key == key:
                return True
            node = node.next
        return False

    def __len__(self) -> int:
        return self.curr_len

    def _resize(self) -> None:
        old = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        for head in old:
            node = head
            while node is not None:
                nxt = node.next
                idx = self._hash(node.key)   
                node.next = self.buckets[idx]
                self.buckets[idx] = node
                node = nxt