class Stack:
    def __init__(self):
        self.items = []


    def is_empty(self):
        return len(self.items) == 0
    

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else: 
            raise IndexError("Can't pop from empty stack.")


    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else: 
            raise IndexError("Peek from empty Stack.")
    
    def size(self):
        return len(self.items)
    
    def print_stack(self):
        print("Stack: ", self.items)

stack = Stack()
stack.push(1)        
stack.push(2)        
stack.push(3)        
stack.push(4)        
stack.push(5)        
stack.push(6)        
stack.print_stack()
print("Popped: ", stack.pop())
stack.print_stack()
print("Peek: ", stack.peek())
print(f"Stack Size: {stack.size()}")
print(f"Is empty? {stack.is_empty()}")        