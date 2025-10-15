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


We want `range_sum(L=14, R=44)`.

---

## Step-by-Step Traversal

### Classic Traversal (Visits All Nodes)
- Traversal sequence (in-order style, visiting all nodes):
  - Visit 6 → 6 < 14 → not added  
  - Visit 10 → 10 < 14 → not added  
  - Visit 16 → in range → add  
  - Visit 20 → in range → add  
  - Visit 26 → in range → add  
  - Visit 30 → in range → add  
  - Visit 36 → in range → add  
  - Visit 46 → 46 > 44 → not added  
  - Visit 56 → 56 > 44 → not added  
  - Visit 66 → 66 > 44 → not added  

- **Nodes contributing to sum:** `16, 20, 26, 30, 36`  
- **Nodes visited unnecessarily:** `6, 10, 46, 56, 66`

---

### Your Version (Root-First + Pruning)
- Traversal sequence (prunes subtrees outside range):
  - Check root 20 → in range → add  
  - 20 > L=14 → traverse left (16)  
    - Check 16 → in range → add  
    - 16 > L → left child 10 → 10 < 14 → skip left child 6 ✅  
  - 20 < R=44 → traverse right (30)  
    - Check 30 → in range → add  
    - 30 > L → left child 26 → in range → add  
    - 30 < R → right child 56 → 56 > 44 → skip right child 66 ✅  
      - 56 > L → left child 46 → 46 > 44 → skip left  
        - 46 > L → left child 36 → in range → add  

- **Nodes contributing to sum:** `16, 20, 26, 30, 36`  
- **Nodes skipped completely:** `6, 10, 46, 56, 66`

---

## Node Visited Table

| Node | Classic (Visited All Nodes) | Classic (Sum Contribution) | Your Version |
|------|-----------------------------|-----------------------------|--------------|
| 6    | ✅ Visited                  | ❌ Not added                | ✅ Skipped   |
| 10   | ✅ Visited                  | ❌ Not added                | ✅ Skipped   |
| 16   | ✅ Visited                  | ✅ Added                    | ✅ Visited, added |
| 20   | ✅ Visited                  | ✅ Added                    | ✅ Visited, added |
| 26   | ✅ Visited                  | ✅ Added                    | ✅ Visited, added |
| 30   | ✅ Visited                  | ✅ Added                    | ✅ Visited, added |
| 36   | ✅ Visited                  | ✅ Added                    | ✅ Visited, added |
| 46   | ✅ Visited                  | ❌ Not added                | ✅ Skipped   |
| 56   | ✅ Visited                  | ❌ Not added                | ✅ Skipped   |
| 66   | ✅ Visited                  | ❌ Not added                | ✅ Skipped   |

---

## Key Benefits of Your Version

1. **Root-first evaluation:** Ensures the root node is checked and included if in range.  
2. **Subtree pruning:** Left/right subtrees outside the range are skipped completely.  
3. **Efficient traversal:** Only visits nodes that can possibly contribute to the sum.  
4. **Corner-case handling:** Works correctly when `root = L`, `root = R`, or when the range overlaps unevenly.  
5. **Time complexity:** O(log n + k) for balanced AVL trees, where `k` = number of nodes within range `[L, R]`.

---
