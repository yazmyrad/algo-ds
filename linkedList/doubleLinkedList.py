class Node:
    def __init__(self, val=0, nextNode=None, prevNode=None):
        self.val = val
        self.next = nextNode
        self.prev = prevNode

class DoubleLinkedList:
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def get(self, index: int) -> int:
        if self.length == 0:
            return -1
        if index == 0: return self.head.val
        if index == self.length: return self.tail.val
        curr = self.head
        while curr and index > 0:
            curr = curr.next
            index -= 1
        return curr.val if curr and index == 0 else -1

    def insertHead(self, val: int) -> None:
        newHead = Node(val)
        if self.length != 0:
            self.head.prev = newHead
            newHead.next = self.head
            self.head = newHead            
        else:
            self.head = self.tail = newHead
        self.length += 1

    def append(self, val: int) -> None:
        if self.length == 0:
            self.insertHead(val)
            return
        
        self.tail.next = Node(val, None, self.tail)
        self.tail = self.tail.next
        self.length += 1

    def removeHead(self,) -> bool:
        if self.length == 0:
            return False

        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.length -= 1
        return True

    def removeTail(self,) -> bool:
        if self.length == 0:
            return False

        self.tail = self.tail.prev
        self.tail.next = None
        self.length -= 1
        return True
    
    def remove(self, index: int) -> bool:
        if index < 0 or self.length <= index:
            return False
        if index == 0:
            return self.removeHead()
        if index == self.length-1:
            return self.removeTail()
        curr = self.head
        while curr and index > 0:
            curr = curr.next
            index -= 1
        prevNode = curr.prev
        nextNode = curr.next
        prevNode.next = nextNode
        nextNode.prev = prevNode
        self.length -= 1
        return True            

    def getValues(self) -> List[int]:
        temp = self.head
        arr = []
        while temp:
            arr.append(temp.val)
            temp = temp.next
        return arr