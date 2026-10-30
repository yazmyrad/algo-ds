
from typing import List

def bubblesort(nums: List[int]):
    n = len(nums)
    if n <= 1:
        return
    i, j = 0, 1
    swapped = False
    while True:
        if j >= n:
            if not swapped: return 
            i, j = 0, 1
            swapped = False

        if nums[i] > nums[j]:
            nums[i], nums[j] = nums[j], nums[i]
            swapped = True

        i += 1
        j += 1
