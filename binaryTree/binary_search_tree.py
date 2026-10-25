from typing import Any, List, Callable
from binary_tree import Node

class BST:
    def __init__(self, values: List[int]=None):
        self._root = None
        self.count = 0
        if values:
            self.build_tree(values)

    def build_tree(self, nums: List[int])->None:
        if nums == [] or nums is None: return

        self._root = Node(nums[0])
        self.count += 1
        for num in nums[1:]:
            self.insert(num)       
    
    def insert(self, num: int)->None:
        self.count += 1
        node = self._root
        if node is None:
            self._root = Node(num)
            return
        
        parent = node
        while node != None:
            parent = node
            if num < node.val:
                node = node.left
                continue
            if num == node.val:
                self.count -= 1
                return
            node = node.right

        if num < parent.val:
            parent.left = Node(num)
            return 
        
        parent.right = Node(num)        

    def get_node_count(self)->int:
        return self.count

    def print_values(self)->None:
        arr = []
        self.dfs(self._root, lambda node: arr.append(node.val))
        print(arr)

    def delete_tree(self)->None:
        self.count = 0
        self._root = None

    def is_in_tree(self, val: int)->bool:
        inTree = False
        def check(node):
            nonlocal inTree
            inTree = True if inTree or node.val == val else False

        self.dfs(self._root, check)
        return inTree
    
    def get_height(self)->int:
        return self.dfs(
            self._root, 
            in_order_func=None, 
            post_order_func=lambda left, right: max(left, right) + 1
        )

    def get_min(self)->int:
        if self._root is None:
            raise ValueError("called on empty tree")
        curr = self._root
        while curr.left:
            curr = curr.left
        return curr.val

    def delete_value(self, val: int) -> bool:
        found = [False]

        def delete(node: Node | None, v: int) -> Node | None:
            if node is None:
                return None
            if v < node.val:
                node.left = delete(node.left, v)
            elif v > node.val:
                node.right = delete(node.right, v)
            else:
                found[0] = True
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                succ = node.right
                while succ.left is not None:
                    succ = succ.left
                node.val = succ.val
                node.right = delete(node.right, succ.val)
            return node

        self._root = delete(self._root, val)
        if found[0]:
            self.count -= 1
        return found[0]
    
    def get_max(self)->int:
        if self._root is None:
            raise ValueError("called on empty tree")
        curr = self._root
        while curr.right:
            curr = curr.right
        return curr.val

    def get_successor(self, val: int) -> int | None:
        node = self._root
        successor = None
        while node is not None:
            if val < node.val:
                successor = node          
                node = node.left
            elif val > node.val:
                node = node.right
            else:
                if node.right is not None:
                    n = node.right
                    while n.left is not None:
                        n = n.left
                    return n.val
                return successor.val if successor else -1
        return -1                   
    
    def is_bst(self)->bool:
        def isValid(node: Node | None, lo: float, hi: float)->bool:
            if node is None:
                return True
            if not(lo < node.val < hi):
                return False
            return (isValid(node.left,  lo, node.val) and
                isValid(node.right, node.val, hi))
        
        return isValid(self._root, float("-inf"), float("inf"))
    
    def dfs(self, 
            node: Node, 
            in_order_func: Callable[..., Any] =  None,
            post_order_func: Callable[..., Any] = None    
        ):
        
        if node is None:
            return 0

        left = self.dfs(node.left, in_order_func, post_order_func)
        if in_order_func:
            in_order_func(node)
        
        right = self.dfs(node.right, in_order_func, post_order_func)
        if post_order_func:
            return post_order_func(left, right)

        return 0
        