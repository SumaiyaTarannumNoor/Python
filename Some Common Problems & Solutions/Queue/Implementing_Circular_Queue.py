class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = [None] * capacity
        self.front = -1
        self.rear = -1

    def is_empty(self):
        return self.front == -1

    def is_full(self):
        return (self.rear + 1) % self.capacity == self.front

    def enqueue(self, item):
        if self.is_full():
            raise IndexError("Can't Enqueue to full circular queue.")
        elif self.is_empty():
            self.front = self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.capacity
        self.items[self.rear] = item

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Can't dequeue from empty circular queue.")
        item = self.items[self.front]
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity
        return item        

    def size(self):
        if self.is_empty():
            return 0
        elif self.front <= self.rear:
            return self.rear - self.front + 1
        else:
            return self.capacity - self.front + self.rear +1
        
    def peek(self):
        if not self.is_empty():
            return self.items[self.front]
        else:
            raise IndentationError("Peek from empty circular queue.")    
           

    def print_queue(self):
        if self.is_empty():
            print("Circular Queue: []")
        elif self.front <= self.rear:
            print("Circular Queue: ", self.items[self.front:self.rear + 1]) 
        else:
            print("Circular Queue: ", self.items[self.front:] + self.items[:self.rear + 1])       

queue = CircularQueue(4)
queue.enqueue(1)                       
queue.enqueue(2)                       
queue.enqueue(3)                       
queue.enqueue(4)
queue.print_queue()
print(f"Dequeued: {queue.dequeue()}")
queue.print_queue()
print(f"Peek: {queue.peek()}")                       
print(f"Size: {queue.size()}")                       
print(f"Is empty? {queue.is_empty()}") 