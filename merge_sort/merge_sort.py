
from typing import List

def merge(a: List[int], b: List[int]):
    temp = []
    while a and b:
        if a[-1] < b[-1]:
            temp.append(a.pop())
        else:
            temp.append(b.pop())

    while a:
        temp.append(a.pop())
    while b:
        temp.append(b.pop())
    return temp

def merge_sort(nums: List[int]):
    n = len(nums)
    if n <= 1:
        return nums

    mid = n // 2

    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])

    left.reverse()
    right.reverse()

    return merge(left, right)

    