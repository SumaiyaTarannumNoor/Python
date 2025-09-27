class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

root = TreeNode(1)
root.right = TreeNode(3)
root.left = TreeNode(2)
root.right.right = TreeNode(4)
root.right.left = TreeNode(5)
root.left.right = TreeNode(6)
root.left.left = TreeNode(7)

def preorder_traversal(root):
    if root:
        print(root.val, end=" ")
        preorder_traversal(root.left)
        preorder_traversal(root.right)

preorder_traversal(root)

def diameter_of_binary_tree(root):
    diameter = 0
    def height(node):
        nonlocal diameter
        if not node:
            return 0
        left_height = height(node.left)
        right_height = height(node.right)
        diameter = max(diameter, left_height + right_height)
        return 1 + max(left_height, right_height)
    
    height(root)
    return diameter

print(f"\n{diameter_of_binary_tree(root)}")