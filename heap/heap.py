from typing import List

class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, num: int) -> None:
        self.heap.append(num)
        idx = self.get_size() - 1
        self.shift_up(idx)

    def shift_up(self, idx: int) -> None:
        
        while idx > 0:
            parent = (idx - 1) // 2
            if self.heap[parent] < self.heap[idx]:
                self.heap[parent], self.heap[idx] = self.heap[idx], self.heap[parent]
                idx = parent
            else:
                break

    def get_max(self) -> int: 
        if self.heap == []:
            raise ValueError("Empty heap")
        return self.heap[0]

    def get_size(self) -> int:
        return len(self.heap)

    def is_empty(self) -> bool:
        return self.get_size() == 0

    def extract_max(self) -> int:
        if self.get_size() == 0: raise ValueError("Empty heap")
        max_val = self.heap[0]
        temp = self.heap.pop()
        if self.heap:
            self.heap[0] = temp 
            self.shift_down(0)
        return max_val

    def shift_down(self, idx: int, size: int | None = None) -> None:
        n = len(self.heap) if size is None else size
        while True:
            left  = 2 * idx + 1
            right = 2 * idx + 2
            largest = idx

            if left < n and self.heap[left] > self.heap[largest]:
                largest = left
            if right < n and self.heap[right] > self.heap[largest]:
                largest = right

            if largest == idx:
                break

            self.heap[idx], self.heap[largest] = self.heap[largest], self.heap[idx]
            idx = largest

    def remove(self, val: int) -> None:
        if self.get_size() == 0: raise ValueError("Heap is empty")
        if self.get_size() == 1 and self.heap[0] == val: 
            del self.heap[0]
            return
        
        idx, found = -1, False
        for i, num in enumerate(self.heap):
            if not found and num == val:
                found = True
                idx = i
                break

        if not found:
            raise ValueError("Value not found")

        last = self.heap.pop()
        if idx < len(self.heap):            
            self.heap[idx] = last
            self.shift_down(idx)
            self.shift_up(idx)  

    def heapify(self, nums: List[int]) -> None:
        if nums == []: return
        n = len(nums)
        self.heap = list(nums)
        for i in range(n // 2 - 1, -1, -1):
            self.shift_down(i)

    def heap_sort(self, nums: List[int]) -> None:
        if nums == []: return

        self.heap = nums
        n = len(nums)
        for i in range(n // 2 - 1, -1, -1):
            self.shift_down(i)

        for end in range(n - 1, 0, -1):
            self.heap[0], self.heap[end] = self.heap[end], self.heap[0]
            self.shift_down(0, end)

        self.heap = []