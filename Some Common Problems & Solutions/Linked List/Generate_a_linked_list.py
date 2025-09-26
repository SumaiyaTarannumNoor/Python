class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def generate_linked_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

arr = [1, 2, 3, 4, 5, 6]
head = generate_linked_list(arr)

def print_linked_list(head):
    current = head
    while current:
        print(current.val, end='->')
        current = current.next
    print("None")

print_linked_list(head)        