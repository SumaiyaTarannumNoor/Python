from collections import deque

class Deque:
    def __init__(self):
        self.items = deque()

    def add_front(self, item):
        self.items.appendleft(item)

    def add_rear(self, item):
        self.items.append(item)

    def remove_front(self):
        if not self.is_empty():
            return self.items.popleft()
        else:
            raise IndexError("Can't remove from empty deque.")

    def remove_rear(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("Can't remove from empty deque.")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def peek_front(self):
        if not self.is_empty():
            return self.items[0] 
        else:
            raise IndentationError("Peek from empty deque.")

    def peek_rear(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("Peek from empty deque.")

    def print_deque(self):
        print("Deque: ", list(self.items))   

queue = Deque()
queue.add_front(2)
queue.add_rear(3)
queue.add_front(1)
queue.add_rear(4) 
queue.print_deque()
print(f"Remove from front: {queue.remove_front()}")                               
print(f"Remove from rear: {queue.remove_rear()}") 
queue.print_deque()
print(f"Add front: {queue.add_front(1)}")                              
print(f"Add raer: {queue.add_rear(4)}")    
queue.print_deque()
print(f"Peek front: {queue.peek_front()}")
print(f"Peek rear: {queue.peek_rear()}")
print(f"Size: {queue.size()}")
print(f"Is empty? {queue.is_empty()}")