import unittest
from binary_search import binary_search, binary_search_first_occurence
import sys

sys.setrecursionlimit(200)

class TestBinarySearch(unittest.TestCase):
    def test_binary_search(self):
        cases = [
            ([1, 2, 3, 4], 3, 2),
            ([-1, 2, 3, 6, 9, 10], -1, 0), 
            ([-1, 2, 3, 6, 9, 10], 10, 5), 
            ([-1, 2, 3, 6, 9, 10], 9, 4), 
            ([-1, 2, 3, 6, 9, 10], 3, 2),
            ([], 0, False),
            ([1], 1, 0), 
            ([2], 1, False)
        ]

        for nums, target, answer in cases:
            with self.subTest(inputs=[nums, target]):
                result = binary_search(nums, target)
                self.assertEqual(result, answer)

    def test_binary_search_first_occurence(self):
        cases = [
            ([1, 2, 2, 4], 2, 1),
            ([0, 1, 1, 2, 2, 2, 2, 3, 3], 1, 1),
            ([0, 1, 1, 2, 2, 2, 2, 3, 3], 0, 0),
            ([0, 1, 1, 2, 2, 2, 2, 3, 3], 2, 3),
            ([0, 1, 1, 2, 2, 2, 2, 3, 3], 3, 7)
        ]

        for nums, target, answer in cases:
            with self.subTest(inputs=[nums, target]):
                try:
                    result = binary_search_first_occurence(nums, target)
                    self.assertEqual(result, answer)
                except RecursionError as e:
                    raise Exception("Maximum Recursion depth reached")

if __name__ == "__main__":
    unittest.main()