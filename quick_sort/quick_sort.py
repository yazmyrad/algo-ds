from typing import List
import random

def partition(nums: List[int], left: int, right: int):
    pivot = random.randint(left, right)
    i, j = left, right 
    while True:
        while nums[i] < nums[pivot]: i += 1
        while nums[j] > nums[pivot]: j -= 1

        if nums[i] == nums[j]:
            i += 1
            j -= 1

        if i >= j: return j
        nums[i], nums[j] = nums[j], nums[i]

def quicksort(nums: List[int], left: int, right: int):
    if left < right:
        p = partition(nums, left, right)
        quicksort(nums, left, p)
        quicksort(nums, p+1, right)
