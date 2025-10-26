# Huffman Coding Tree and Compression Ratio Calculation

## Question

A file has the following characters along with their frequencies:  
a:20, b:30, c:78, d:12, e:27, f:67, g:5, h:80.

Draw the Huffman coding tree for each character mentioned above.  
Also compute the compression ratio via this encoding.

---

## Solution

### 1. List of Characters and Their Frequencies

| Character | Frequency |
|-----------|-----------|
| a         | 20        |
| b         | 30        |
| c         | 78        |
| d         | 12        |
| e         | 27        |
| f         | 67        |
| g         | 5         |
| h         | 80        |

Total number of characters:  
**Sum = 20 + 30 + 78 + 12 + 27 + 67 + 5 + 80 = 319**

---

### 2. Building the Huffman Tree

**Step 1: List characters by frequency (ascending):**

- g: 5
- d: 12
- a: 20
- e: 27
- b: 30
- f: 67
- c: 78
- h: 80

**Step 2: Build the tree iteratively:**

#### Iteration 1

- Combine g (5) + d (12) = 17  
  Tree: [g,d]:17

#### Iteration 2

- Combine [g,d]:17 + a:20 = 37  
  Tree: [[g,d],a]:37

#### Iteration 3

- Combine e:27 + b:30 = 57  
  Tree: [e,b]:57

#### Iteration 4

- Combine [[g,d],a]:37 + [e,b]:57 = 94  
  Tree: [[[g,d],a],[e,b]]:94

#### Iteration 5

- Combine f:67 + c:78 = 145  
  Tree: [f,c]:145

#### Iteration 6

- Combine [[[g,d],a],[e,b]]:94 + [f,c]:145 = 239  
  Tree: [[[[g,d],a],[e,b]],[f,c]]:239

#### Iteration 7

- Combine [[[[g,d],a],[e,b]],[f,c]]:239 + h:80 = 319  
  Tree: [[[[[g,d],a],[e,b]],[f,c]],h]:319

#### Final Huffman Tree Representation

Below is a text-based representation of the Huffman tree.  
`0` denotes left branches, `1` denotes right branches.

```
                [319]
               /     \
         [239]        h:80
        /     \
    [94]     [145]
   /   \     /    \
[37] [57]  f:67   c:78
/  \  / \
g:5 d:12 e:27 b:30
    a:20
```

**Huffman Codes for Each Character:**  
Assign 0 for left, 1 for right at each split.

| Character | Path in Tree       | Huffman Code |
|-----------|--------------------|--------------|
| h         | rightmost          | `1`          |
| f         | left-left-right-left  | `0100`      |
| c         | left-left-right-right | `0101`      |
| g         | left-left-left-left-left | `00000`   |
| d         | left-left-left-left-right| `00001`   |
| a         | left-left-left-right     | `0001`    |
| e         | left-left-right-left     | `0010`    |
| b         | left-left-right-right    | `0011`    |

Let's assign codes explicitly for clarity:

- h: `1`
- f: `0100`
- c: `0101`
- g: `00000`
- d: `00001`
- a: `0001`
- e: `0010`
- b: `0011`

---

### 3. Calculating Average Code Length

Multiply each character's code length by its frequency:

| Character | Code   | Length | Frequency | Contribution |
|-----------|--------|--------|-----------|--------------|
| h         | 1      | 1      | 80        | 80           |
| f         | 0100   | 4      | 67        | 268          |
| c         | 0101   | 4      | 78        | 312          |
| g         | 00000  | 5      | 5         | 25           |
| d         | 00001  | 5      | 12        | 60           |
| a         | 0001   | 4      | 20        | 80           |
| e         | 0010   | 4      | 27        | 108          |
| b         | 0011   | 4      | 30        | 120          |

**Total bits used = 80 + 268 + 312 + 25 + 60 + 80 + 108 + 120 = 1053 bits**

Average code length per character:  
= Total bits / Total characters  
= 1053 / 319 ≈ **3.30 bits/character**

---

### 4. Uncompressed Data Calculation

Assume fixed-length encoding (equal length for all):

- Number of unique characters: 8
- Minimum bits needed per character: ceil(log₂(8)) = 3 bits

But since Huffman is variable-length, let's compare:

- Uncompressed (fixed) bits: 3 bits/character  
- Total bits: 319 x 3 = **957 bits**

Alternatively, if each character stored in 1 byte (8 bits):

- Total bits: 319 x 8 = **2552 bits**

But for fair compression ratio, use fixed-length: **3 bits/character**

---

### 5. Compression Ratio Calculation

**Compression Ratio = (Uncompressed size) / (Compressed size)**

- Uncompressed size: 957 bits
- Compressed size (Huffman): 1053 bits

**Compression Ratio = 957 / 1053 ≈ 0.91**

So, in this particular distribution, Huffman coding does **not** compress compared to the minimum possible fixed-length encoding, because the fixed-length code is already quite efficient due to the small number of unique characters.

If the original encoding used 8-bit ASCII:

- Compression Ratio = 2552 / 1053 ≈ **2.42**

---

## Summary

- **Huffman Coding Tree** was built and codes assigned.
- **Average code length**: ≈ 3.30 bits/character
- **Compression Ratio** (vs 8-bit ASCII): ≈ 2.42  
- **Compression Ratio** (vs fixed-length 3-bit): ≈ 0.91 (i.e., not compressed)

---

### Visual Huffman Tree (Text Representation)

```
                [319]
               /     \
         [239]        h:80
        /     \
    [94]     [145]
   /   \     /    \
[37] [57]  f:67   c:78
/  \  / \
g:5 d:12 e:27 b:30
    a:20
```

### Code Assignments

| Character | Huffman Code |
|-----------|--------------|
| h         | 1            |
| f         | 0100         |
| c         | 0101         |
| g         | 00000        |
| d         | 00001        |
| a         | 0001         |
| e         | 0010         |
| b         | 0011         |

---
