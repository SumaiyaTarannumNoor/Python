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

arr = [1, 2, 3, 4, 4, 3, 2]
list = generate_linked_list(arr)

def print_linked_list(list):
    current = list
    while current:
        print(current.val, end='->')
        current = current.next
    print("None")    

print_linked_list(list)


def is_circular(head):
    if not head:
        return False
    
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False

print(is_circular(list))

