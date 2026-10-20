import unittest
from binary_search_recursion import binary_search
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


if __name__ == "__main__":
    unittest.main()