class ListNode:
    def __init__ (self, val=0, next=None ):
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

arr1 = [1, 2, 3, 4, 5, 6]
arr2 = [7, 8, 9, 10, 11, 12]

head1 = generate_linked_list(arr1)
head2 = generate_linked_list(arr2)

def print_linked_list(head):
     current = head
     while current:
          print(current.val, end='->')
          current = current.next
     print("None")

print_linked_list(head1)
print_linked_list(head2)
    
def merge_two_lists(head1,head2):
     dummy = ListNode()
     current = dummy
     while head1 and head2:
          if head1.val<head2.val:
               current.next = head1
               head1 = head1.next
          else:
               current.next = head2
               head2 = head2.next
          current = current.next
     current.next = head1 if head1 else head2
     return dummy.next

merged_head = merge_two_lists(head1, head2)                   

print_linked_list(merged_head)