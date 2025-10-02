class PriorityQueue():
    def __init__(self):
        self.items = []

    def enqueue(self, item, priority):
        self.items.append((item, priority))
        self.items.sort(key=lambda x: x[1], reverse=True)    

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)[0]
        else:
            raise IndexError("Can't dequeue from empty queue.")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def peek(self):
        if not self.is_empty():
            return self.items[0][0]
        else: 
            raise IndexError("Peek from empty queue.")

    def print_queue(self):
        print("Priority Queue: {self.items}")   

queue = PriorityQueue()
queue.enqueue("Task 1", 1)                       
queue.enqueue("Task 2", 2)                       
queue.enqueue("Task 3", 3)                       
queue.enqueue("Task 2", 4)
queue.print_queue()
print(f"Dequeued: {queue.dequeue()}")
queue.print_queue()
print(f"Peek: {queue.peek()}")                       
print(f"Size: {queue.size()}")                       
print(f"Is empty? {queue.is_empty()}")                                