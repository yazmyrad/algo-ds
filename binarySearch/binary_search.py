from typing import List
import sys

sys.setrecursionlimit(200)

def binary_search(nums: List[int], target:int)->int|False:
    """
    Method for binary search of target on sorted array
    """
    n = len(nums)
    if n == 0:
        return False
    if n == 1:
        return 0 if nums[0] == target else False
    l, r = 0, n-1
    while l <= r:
        mid = l+(r-l)//2
        if nums[mid] == target:
            return mid
        elif nums[mid] > target:
            r = mid - 1
        else:
            l = mid + 1

    return False

def binary_search_first_occurence(nums: List[int], target:int)->int|False:
    """
    Method for binary search earliest occurence of target on sorted array
    """
    n = len(nums)
    if n == 0:
        return False
    if n == 1:
        return 0 if nums[0] == target else False
    l, r = 0, n-1
    while l <= r:
        mid = l+(r-l)//2
        if l == r == mid:
            return mid
        elif nums[mid] >= target:
            r = mid
        else:
            l = mid + 1

    return False
