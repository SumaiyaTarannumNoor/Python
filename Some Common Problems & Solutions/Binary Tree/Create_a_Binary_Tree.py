class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val 
        self.left = left
        self.right = right

# Example: Construct a binary tree
#        1
#       / \
#      2   3
#     / \
#    4   5

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

## Inorder Traversal (Left->Root->Right)

def inorder_traversal(root):
    if root:
        inorder_traversal(root.left)
        print(root.val, end=" ")
        inorder_traversal(root.right)

print(f"{inorder_traversal(root)}") 


## Preorder Traversal (Root->Left->Right)

def preorder_traversal(root):
    if root:
        print(root.val, end=" ")
        preorder_traversal(root.left)
        preorder_traversal(root.right)

print(f"{preorder_traversal(root)}") 


## Postorder Traversal (Left->Right->Root)

def postorder_traversal(root):
    if root:
        postorder_traversal(root.left)
        postorder_traversal(root.right)
        print(root.val, end=" ")

print(f"{postorder_traversal(root)}") 


def tree_height(root):
    if not root:
        return 0
    return 1 + max(tree_height(root.left), tree_height(root.right))

print(f"Height: {tree_height(root)}")
