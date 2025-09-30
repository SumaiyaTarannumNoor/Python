class TreeNode:
    def __init__(self, val = 0, left=None, right=None):
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
    if not root:
        return []
    return inorder_traversal(root.left) + [root.val] + inorder_traversal(root.right)            

values = [5, 3, 7, 2, 4, 6, 8]

bst_root = create_bst(values)

print(f"Inorder Traversal of BST: {inorder_traversal(bst_root)}")