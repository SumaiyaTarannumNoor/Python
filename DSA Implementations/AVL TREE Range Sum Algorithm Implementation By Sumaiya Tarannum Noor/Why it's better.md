# Efficient Range Sum in AVL Tree

## Overview
The goal is to efficiently compute the sum of all values within a dynamic range `[L, R]` in an AVL tree while avoiding unnecessary traversal and handling all edge cases.

---

## AVL Tree Structure

We have the following AVL tree constructed with keys `[10, 20, 16, 6, 26, 30, 36, 46, 56, 66]`:

                    20
                   /  \
                16     30
              /       /  \
            10       26  56
            /           /  \
           6           46  66
                      / 
                    36


We want `range_sum(L=6, R=46)`.

---

## Step-by-Step Traversal

### Classic Traversal (Visits All Nodes)
- Traversal sequence (in-order style, visiting all nodes):
  - Visit 30 → in range → add
  - Traverse left subtree 16
    - Visit 16 → in range → add
    - Traverse left child 10 → in range → add
      - Traverse left 6 → in range → add
    - Traverse right child 20 → in range → add
  - Traverse right subtree 56
    - Visit 56 → 56 > 46 → not added
    - Traverse left child 36 → in range → add
      - Traverse left child 26 → in range → add
      - Traverse right child 46 → in range → add
    - Traverse right child 66 → 66 > 46 → not added

- **Nodes contributing to sum:** `6, 10, 16, 20, 26, 30, 36, 46`  
- **Nodes visited unnecessarily:** `56, 66`  

---

### Your Version (Root-First + Pruning)
- Traversal sequence (prunes subtrees outside range):
  - Check root 30 → in range → add
  - 30 > L=6 → traverse left subtree (16)
    - Check 16 → in range → add
    - 16 > L → left child 10 → in range → add
      - Traverse left child 6 → in range → add
    - 16 < R → right child 20 → in range → add
  - 30 < R=46 → traverse right subtree (56)
    - Check 56 → 56 > R → skip right child 66 ✅
    - 56 > L → left child 36 → in range → add
      - 36 > L → left child 26 → in range → add
      - 36 < R → right child 46 → in range → add

- **Nodes contributing to sum:** `6, 10, 16, 20, 26, 30, 36, 46`  
- **Nodes skipped completely:** `56, 66`  

---

## Node Visited Table

| Node | Classic (Visited All Nodes) | Classic (Sum Contribution) | Your Version |
|------|----------------------------|---------------------------|--------------|
| 6    | ✅ Visited                 | ✅ Added                 | ✅ Visited, added |
| 10   | ✅ Visited                 | ✅ Added                 | ✅ Visited, added |
| 16   | ✅ Visited                 | ✅ Added                 | ✅ Visited, added |
| 20   | ✅ Visited                 | ✅ Added                 | ✅ Visited, added |
| 26   | ✅ Visited                 | ✅ Added                 | ✅ Visited, added |
| 30   | ✅ Visited                 | ✅ Added                 | ✅ Visited, added |
| 36   | ✅ Visited                 | ✅ Added                 | ✅ Visited, added |
| 46   | ✅ Visited                 | ✅ Added                 | ✅ Visited, added |
| 56   | ✅ Visited                 | ❌ Not added             | ✅ Skipped   |
| 66   | ✅ Visited                 | ❌ Not added             | ✅ Skipped   |

---

## Key Benefits of Your Version

1. **Root-first evaluation:** ensures the root node is checked and included if in range.  
2. **Subtree pruning:** left/right subtrees outside the range are skipped completely.  
3. **Efficient traversal:** only visits nodes that may contribute to the sum.  
4. **Handles corner cases:** works correctly even if `root = L` or `root = R` or dynamic ranges overlap root.  
5. **Time complexity:** O(log n + k) for balanced AVL trees, where `k` = number of nodes in the range.




