from linkedList import LinkedList

class Stack:
    def __init__(self):
        self.linkedlist = LinkedList()

    def add(self, val: int) -> None:
        self.linkedlist.insertHead(val)
        return

    def pop(self,) -> int:
        if self.len() == 0:
            raise Exception("Stack is Empty")
        val = self.linkedlist.get(0)
        self.linkedlist.remove(0)
        return val

    def peek(self) -> int:
        if self.len() == 0:
            raise Exception("Stack is Empty")
        return self.linkedlist.get(0)

    def len(self) -> int:
        return self.linkedlist.length
