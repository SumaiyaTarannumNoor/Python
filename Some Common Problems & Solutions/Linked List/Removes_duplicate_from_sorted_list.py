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

arr = [1, 1, 2, 2, 3, 3]
list = generate_linked_list(arr)

def print_linked_list(list):
    current = list
    while current:
        print(current.val, end='->')
        current = current.next
    print("None")

print_linked_list(list)    

def remove_duplicate(list):
    current = list
    while current and current.next:
        if current.val == current.next.val:
            current.next = current.next.next
        else:
            current = current.next

    return list

unique_list = remove_duplicate(list)

print_linked_list(unique_list)

