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

arr1 = [1, 2, 3, 4, 5]
head1 = generate_linked_list(arr1)

arr2 = [1, 2, 3, 4, 5, 4, 3, 2, 1]
head2 = generate_linked_list(arr2)

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

head1.next.next.next.next.next=head1


print(is_circular(head1))


head2.next.next.next.next.next.next.next.next.next=head2

print(is_circular(head2))


