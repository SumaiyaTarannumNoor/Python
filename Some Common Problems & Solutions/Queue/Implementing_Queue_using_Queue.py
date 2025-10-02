from queue import Queue as ThreadSafeQueue

class Queue:
    def __init__(self):
        self.items = ThreadSafeQueue()

    def enqueue(self, item):
        self.items.put(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.get()
        else:
            raise IndexError("Can't dequeue from empty queue.")

    def is_empty(self):
        return self.items.empty()

    def size(self):
        return self.items.qsize()

    def peek(self):
        if not self.is_empty():
            front_item = self.items.get()
            self.items.put(front_item)
            return front_item
        else:
            raise IndexError("Peek from empty queue.")

    def print_queue(self):
        temp_queue = ThreadSafeQueue()
        temp_list = []
        while not self.items.empty():
            item = self.items.get()
            temp_queue.put(item)
            temp_list.append(item)

        while not temp_queue.empty():
            self.items.put(temp_queue.get())
        print(f"Queue: {temp_list}")

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
print(f"Is empty? {queue.is_empty()}")                                 