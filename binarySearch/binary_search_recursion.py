from typing import List
import sys

sys.setrecursionlimit(200)

def binary_search(nums: List[int], target: int)->int|False:
    n = len(nums)
    if n == 0: return False
    if n == 1: return 0 if nums[0] == target else False

    def recursion(l: int, r:int)->int|False:
        if l > r: return False
        mid = l+(r-l)//2
        if nums[mid] == target: return mid
        elif nums[mid] > target: return recursion(l, mid-1)
        else: return recursion(mid+1, r)

    return recursion(0, n-1)