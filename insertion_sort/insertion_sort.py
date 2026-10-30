from typing import List

def sort(nums: List[int]):
    n = len(nums)
    if n <= 1:
        return

    i = 1
    while i < n:
        j = i
        while j-1 >= 0 and nums[j] < nums[j-1]:
            nums[j-1], nums[j] = nums[j], nums[j-1]
            j -= 1
        i += 1