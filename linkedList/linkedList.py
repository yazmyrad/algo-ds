class Node:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedList:
    
    def __init__(self):
        self.head = Node()
        self.length = 0

    def get(self, index: int) -> int:
        if self.length == 0:
            return -1
        curr = self.head
        while curr and index > 0:
            curr = curr.next
            index -= 1
        return curr.val if curr and index == 0 else -1

    def insertHead(self, val: int) -> None:
        newHead = Node(val)
        if self.length != 0:
            newHead.next = self.head
            
        self.head = newHead
        self.length += 1

    def insertTail(self, val: int) -> None:
        if self.length == 0:
            self.insertHead(val)
            self.length += 1
            return
        
        curr = self.head
        while self.head.next:
            self.head = self.head.next
        self.head.next = Node(val)
        self.head = curr
        self.length += 1

    def remove(self, index: int) -> bool:
        if index == 0:
            if self.length:
                self.head = self.head.next
                self.length -= 1
                return True
            return False
        else:
            prev = self.head
            next = self.head.next
            index -= 1
            while next and index > 0:
                prev = next
                next = next.next
                index -= 1
            if next == None and index >= 0:
                return False
            prev.next = next.next
            self.length -= 1
            return True

    def getValues(self) -> List[int]:
        temp = self.head
        arr = []
        while temp:
            arr.append(temp.val)
            temp = temp.next
        return arr if self.length else []