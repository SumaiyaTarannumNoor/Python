class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def insert_into_bst(root, val):
    if not root:
        return TreeNode(val)

    if val < root.val:
        root.left = insert_into_bst(root.left, val)

    if val > root.val:
        root.right = insert_into_bst(root.right, val)

    return root    

def create_bst(arr):
    root = None
    for val in arr:
        root = insert_into_bst(root, val)      
    return root

def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.val, end=" ")
        inorder_traversal(root.right)


values = [5, 3, 7, 2, 4, 6, 8]
root = create_bst(values)

print("Version 1: ")
inorder_traversal(root)

root = insert_into_bst(root, 1)
print("\nVersion 2: ")
inorder_traversal(root)

root = insert_into_bst(root, 9)
print("\nVersion 3: ")
inorder_traversal(root)

def delete_from_bst(root, val):
    if not root:
        return None
    if val < root.val:
        root.left = delete_from_bst(root.left, val)
    if val > root.val:
        root.right = delete_from_bst(root.right, val)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left
        temp = root.right
        while temp.left:
            temp = temp.left
        root.val = temp.val
        root.right = delete_from_bst(root.right, temp.val)

    return root


root = delete_from_bst(root, 5)

print("\nVersion 4: ")
inorder_traversal(root)
