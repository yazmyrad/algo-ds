from typing import List

class Node:
    def __init__(self, val:int = 0):
        self.val: int = val
        self.left: Node | None = None
        self.right: Node | None = None

class BT:

    def __init__(self, values: List[int] = None)->None:
        pass

    def build_tree(self, nums: List[int])->None:
        pass
    
    def insert(self, num: int)->None:
        ...

    def get_node_count(self)->int:
        pass

    def print_values(self)->None:
        pass

    def delete_tree(self)->None:
        pass

    def is_in_tree(self, val: int)->bool:
        pass

    def get_height(self)->int:
        pass

    def get_min(self)->int:
        pass

    def get_max(self)->int:
        pass

    def delete_value(self, val: int)->bool:
        pass

    def get_successor(self, val: int)->int:
        pass

    def is_bst(self)->bool:
        pass


    
