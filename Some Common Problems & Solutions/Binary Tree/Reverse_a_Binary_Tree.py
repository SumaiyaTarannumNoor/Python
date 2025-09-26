class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def reverse_tree(root):
    if not root:
        return None
    root.left, root.right = reverse_tree(root.right), reverse_tree(root.left)
    return root

root = TreeNode(1, TreeNode(2), TreeNode(3))


def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.val, end=" ")
        inorder_traversal(root.right)

reversed_root = reverse_tree(root)

print(f"{inorder_traversal(root)}")

print(f"{inorder_traversal(reversed_root)}")
