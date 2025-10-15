class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return TreeNode(key)
        elif key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self._get_height(node.left),
                              self._get_height(node.right))
        balance = self._get_balance(node)

        # Left Left Case
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)
        # Right Right Case
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)
        # Left Right Case
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        # Right Left Case
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        return node

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left),
                           self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                           self._get_height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left),
                           self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                           self._get_height(y.right))
        return y

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _get_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def _inorder_traversal(self, node, result):
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node.key)
            self._inorder_traversal(node.right, result)

    def inorder_traversal(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    # ---------------- RANGE SUM AND VALUES ----------------
    def range_sum_and_values(self, L, R):
        values = []
        total = self._range_sum_and_values(self.root, L, R, values)
        return total, sorted(values)

    def _range_sum_and_values(self, node, L, R, values):
        if not node:
            return 0

        current_sum = 0

        # Step 1: checking the root first
        if L <= node.key <= R:
            current_sum += node.key
            values.append(node.key)

        # Step 2: traversing the left sub-tree if potential values exist
        if node.key > L:
            current_sum += self._range_sum_and_values(node.left, L, R, values)

        # Step 3: traversing the right sub-tree if potential values exist
        if node.key < R:
            current_sum += self._range_sum_and_values(node.right, L, R, values)

        return current_sum



avl_tree = AVLTree()
keys = [10, 20, 16, 6, 26, 30, 36, 46, 56, 66]
for key in keys:
    avl_tree.insert(key)

print(f"Inorder Traversal: {avl_tree.inorder_traversal()}")

L = int(input("Enter the lower bound of the range (L): "))
R = int(input("Enter the upper bound of the range (R): "))
total, values = avl_tree.range_sum_and_values(L, R)
print(f"Range Sum [{L}, {R}]: {total}")
print(f"Values in Range (Inorder): {values}")
