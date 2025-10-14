class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t

    def insert(self, k):
        root = self.root
        if len(root.keys) == (2*self.t) - 1:
            new_root = BTreeNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, k)


    def _insert_non_full(self, node, k):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(0)
            while i >= 0 and k < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k

        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2*self.t) - 1:
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)


    def _split_child(self, parent, idx):
        t = self.t
        child = parent.children[idx]
        new_node = BTreeNode(child.leaf)
        parent.keys.insert(idx, child.keys[t - 1])
        parent.children.insert(idx + 1, new_node)
        new_node.keys = child.keys[t : (2 * t -1)] 
        child.keys = child.keys[0 : (t - 1)]
        if not child.leaf:
            new_node.children = child.children[t : (2* t)]
            child.children = child.children[0 : t] 


    def search(self, k, node=None):
        node = node or self.root
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and k == node.keys[i]:
            return True
        if node.leaf:
            return False
        return self.search(k, node.children[i])


    def print_tree(self, node=None, level=0):
        node = node or self.root
        print(f"Level {level}: {node.keys}")
        if not node.leaf:
            for child in node.children:
                self.print_tree(child, level + 1) 


btree = BTree(t=2)
keys = [10, 20, 6, 16, 12, 22, 4, 14]
for key in keys:
    btree.insert(key)

print(f"B-Tree Structure: ") 
btree.print_tree()

print(f"\n Search for 6: {btree.search(6)}")
print(f"\n Search for 14: {btree.search(14)}")


# Time Complexity: O(log n)
# Space Complexity: O(n)
# Auxiliary Space: O(log n)