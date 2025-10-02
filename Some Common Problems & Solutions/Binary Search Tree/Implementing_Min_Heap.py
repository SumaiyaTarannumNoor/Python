class MinHeap:
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i -1) // 2
    
    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def insert(self, val):
        self.heap.append(val)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            return None
        min_val = self.heap[0]
        last_val = self.heap.pop()
        if self.heap:
            self.heap[0] = last_val
            self._heapify_down(0)  
        return min_val
    
    def _heapify_up(self, i):
        while i > 0 and self.heap[i] < self.heap[self.parent(i)]:
            self.heap[i], self.heap[self.parent(i)] = self.heap[self.parent(i)], self.heap[i]
            i = self.parent(i)

    def _heapify_down(self, i):
        min_index = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < len(self.heap) and self.heap[left] < self.heap[min_index]:
            min_index = left
        if right < len(self.heap) and self.heap[right] < self.heap[min_index]:
            min_index = right

        if i != min_index:
            self.heap[i], self.heap[min_index] = self.heap[min_index], self.heap[i]
            self._heapify_down(min_index)

    def print_heap(self):
        print("Min Heap: ", self.heap)

min_heap = MinHeap()
min_heap.insert(5)                                        
min_heap.insert(3)                                        
min_heap.insert(1)                                        
min_heap.insert(8)
min_heap.print_heap()
print("Extract Min: ", min_heap.extract_min())
min_heap.print_heap()                                        