from linkedList import DoubleLinkedList

class Que:
    def __init__(self):
        self.linkedlist = DoubleLinkedList()

    def add(self, val: int) -> None:
        self.linkedlist.insertHead(val)
        return

    def pop(self,) -> int:
        if self.len() == 0:
            raise Exception("Queue is Empty")
        val = self.linkedlist.get(self.len()-1)
        self.linkedlist.removeTail()
        return val

    def peekLast(self) -> int:
        if self.len() == 0:
            raise Exception("Queue is Empty")
        return self.linkedlist.get(self.len()-1)

    def peekFirst(self) -> int:
        if self.len() == 0:
            raise Exception("Queue is Empty")
        return self.linkedlist.get(0)

    def len(self) -> int:
        return self.linkedlist.length
