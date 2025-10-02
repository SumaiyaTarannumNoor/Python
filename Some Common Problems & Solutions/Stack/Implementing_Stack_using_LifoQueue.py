from queue import LifoQueue

class Stack:
    def __init__(self):
        self.items = LifoQueue()

    def is_empty(self):
        return self.items.empty()

    def push(self, item):
        self.items.put(item)

    def pop(self):
        if not self.is_empty():
            return self.items.get()
        else:
            raise IndexError("Pop from empty stack.")

    def peek(self):
        if not self.is_empty():
            top_item = self.items.get()
            self.items.put(top_item)
            return top_item
        else:
            raise IndexError("Peek from empty stack.")

    def size(self):
        return self.items.qsize()

    def print_stack(self):
        temp_stack = LifoQueue()
        temp_list = []
        while not self.items.empty():
            item = self.items.get()
            temp_stack.put(item)
            temp_list.append(item)

        while not temp_stack.empty():
            self.items.put(temp_stack.get())
        print("Stack: ", temp_list)

stack = Stack()
stack.push(5)                           
stack.push(2)                           
stack.push(3)                           
stack.push(4)                           
stack.push(1)                           
stack.push(6)                           
stack.print_stack()
print("Popped: ", stack.pop())
stack.print_stack()
print(f"Peek: {stack.peek()}")
print(f"Size: {stack.size()}")
print(f"Is empty? {stack.is_empty()}")                           