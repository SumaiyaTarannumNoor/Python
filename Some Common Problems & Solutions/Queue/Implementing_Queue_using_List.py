class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("Cant Dequeue from empty queue")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
    
    def peek(self):
        if not self.is_empty():
            return self.items[0]
        else:
            raise IndexError("Peek from empty queue.")
        
    def print_queue(self):
        print("Queue: ", self.items) 

queue = Queue()
queue.enqueue(1)           
queue.enqueue(2)           
queue.enqueue(3)           
queue.enqueue(4)

queue.print_queue()
print(f"Dequeued: {queue.dequeue()}")
queue.print_queue()
print(f"Peek: {queue.peek()}")
print(f"Size: {queue.size()}")
print(f"Is Empty? {queue.is_empty()}")
