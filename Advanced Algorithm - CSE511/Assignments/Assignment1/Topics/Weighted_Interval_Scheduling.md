# Weighted Interval Scheduling: All Approaches Explained with Examples and Simulation

Weighted Interval Scheduling is a classic dynamic programming problem. Given a set of jobs, each with a start time, finish time, and weight (profit), the goal is to select a subset of non-overlapping jobs with maximum total weight.

This guide covers **all approaches** to solve Weighted Interval Scheduling, with step-by-step examples and simulation.

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Naive Recursive Approach](#naive-recursive-approach)
3. [Memoization (Top-Down DP)](#memoization-top-down-dp)
4. [Iterative (Bottom-Up DP)](#iterative-bottom-up-dp)
5. [Efficient p(j) Computation (Binary Search)](#efficient-pj-computation-binary-search)
6. [Simulation Example](#simulation-example)
7. [Summary Table](#summary-table)
8. [References](#references)

---

## Problem Statement

Given `n` jobs. Each job `j` has:
- Start time: `start[j]`
- Finish time: `finish[j]`
- Weight (profit): `weight[j]`

Choose a subset of non-overlapping jobs to maximize total profit.

### Example Input

| Job | Start | Finish | Weight |
|-----|-------|--------|--------|
| 1   | 1     | 4      | 3      |
| 2   | 3     | 5      | 2      |
| 3   | 0     | 6      | 4      |
| 4   | 4     | 7      | 5      |
| 5   | 3     | 8      | 2      |
| 6   | 5     | 9      | 4      |
| 7   | 6     | 10     | 6      |
| 8   | 8     | 11     | 8      |

---

## 1. Naive Recursive Approach

### Idea

For each job `j`:
- Either **include** job `j` (and add its weight), skipping all jobs overlapping with it.
- Or **exclude** job `j`.

Let `OPT(j)` be the max total weight for jobs up to `j`.

### Recurrence

Let `p(j)` be the last job before `j` that does **not** overlap with `j`.
- `OPT(j) = max(weight[j] + OPT(p(j)), OPT(j-1))`

### Finding `p(j)`

For job `j`, search for the rightmost job `i < j` with `finish[i] <= start[j]`.

### Implementation Sketch

```python
def OPT(j, jobs):
    if j == -1:
        return 0
    # Find p(j)
    i = j - 1
    while i >= 0 and jobs[i][1] > jobs[j][0]:
        i -= 1
    return max(jobs[j][2] + OPT(i, jobs), OPT(j-1, jobs))
```

### Time Complexity
- Exponential, O(2^n)

---

## 2. Memoization (Top-Down DP)

### Idea

Store already computed results in a memo table to avoid recomputation.

### Implementation Sketch

```python
memo = {}
def OPT(j, jobs):
    if j == -1:
        return 0
    if j in memo:
        return memo[j]
    i = find_p(j, jobs)
    memo[j] = max(jobs[j][2] + OPT(i, jobs), OPT(j-1, jobs))
    return memo[j]
```

### Time Complexity
- O(n^2) (if `find_p` is O(n) per job)

---

## 3. Iterative (Bottom-Up DP)

### Steps

1. **Sort jobs** by finish time.
2. Compute `p(j)` for each job in advance.
3. Build DP table (`dp[j]` = OPT(j))

### Algorithm

```python
# jobs = [(start, finish, weight)]
jobs.sort(key=lambda x: x[1])
n = len(jobs)
p = [0]*n
for j in range(n):
    for i in range(j-1, -1, -1):
        if jobs[i][1] <= jobs[j][0]:
            p[j] = i
            break
    else:
        p[j] = -1

dp = [0]*(n+1)
for j in range(1, n+1):
    incl = jobs[j-1][2] + dp[p[j-1]+1]
    excl = dp[j-1]
    dp[j] = max(incl, excl)
```

### Time Complexity
- O(n^2) (if `find_p` is O(n))

---

## 4. Efficient p(j) Computation (Binary Search)

If jobs are **sorted by finish time**, use binary search to compute `p(j)` in O(log n).

```python
def binary_search(jobs, j):
    lo, hi = 0, j-1
    while lo <= hi:
        mid = (lo + hi) // 2
        if jobs[mid][1] <= jobs[j][0]:
            if jobs[mid+1][1] <= jobs[j][0]:
                lo = mid + 1
            else:
                return mid
        else:
            hi = mid - 1
    return -1
```

Using this, total time complexity becomes **O(n log n)**.

---

## 5. Simulation Example

Let's walk through the example jobs above.

### Step 1: Sort Jobs by Finish Time

| Job | Start | Finish | Weight |
|-----|-------|--------|--------|
| 1   | 1     | 4      | 3      |
| 2   | 3     | 5      | 2      |
| 3   | 0     | 6      | 4      |
| 4   | 4     | 7      | 5      |
| 5   | 3     | 8      | 2      |
| 6   | 5     | 9      | 4      |
| 7   | 6     | 10     | 6      |
| 8   | 8     | 11     | 8      |

### Step 2: Compute p(j) for Each Job

| Job | p(j) |
|-----|------|
| 1   | -1   |
| 2   | -1   |
| 3   | -1   |
| 4   | 0    |
| 5   | -1   |
| 6   | 2    |
| 7   | 3    |
| 8   | 5    |

### Step 3: DP Table

Let `dp[j]` be the optimal value up to job `j` (1-based).

| j | incl (weight + dp[p[j-1]+1]) | excl (dp[j-1]) | dp[j] |
|---|------------------------------|---------------|-------|
| 1 | 3 + dp[0] = 3                | 0             | 3     |
| 2 | 2 + dp[0] = 2                | 3             | 3     |
| 3 | 4 + dp[0] = 4                | 3             | 4     |
| 4 | 5 + dp[1] = 8                | 4             | 8     |
| 5 | 2 + dp[0] = 2                | 8             | 8     |
| 6 | 4 + dp[3] = 8                | 8             | 8     |
| 7 | 6 + dp[4] = 14               | 8             | 14    |
| 8 | 8 + dp[6] = 16               | 14            | 16    |

**Max profit: 16**

### Optimal Subset

Backtrack:
- Job 8 is included (8 + dp[6] = 16)
- dp[6] = 8: Job 4 included (5 + dp[1] = 8)
- dp[1] = 3: Job 1 included

Thus, select **Jobs 1, 4, 8**.

---

## 6. Summary Table

| Approach              | Time Complexity   | Space Complexity | Comments                  |
|-----------------------|------------------|------------------|---------------------------|
| Naive Recursive       | O(2^n)           | O(n)             | Exponential, impractical  |
| Memoization (Top-Down)| O(n^2)           | O(n)             | Much better; still slow   |
| Iterative DP          | O(n^2)           | O(n)             | Standard DP               |
| DP + Binary Search    | O(n log n)       | O(n)             | Best; sort & binary search|

---

## 7. References

- [CLRS 3rd Edition, Section 15.1: Weighted Interval Scheduling](https://mitpress.mit.edu/9780262033848/introduction-to-algorithms/)
- [Wikipedia: Weighted Interval Scheduling](https://en.wikipedia.org/wiki/Interval_scheduling_maximization)
- [MIT OpenCourseWare: Weighted Interval Scheduling](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/lecture-16-dynamic-programming-ii-weighted-interval-scheduling/)

---

## 8. Full Python Simulation

```python
def weighted_interval_scheduling(jobs):
    # jobs: list of (start, finish, weight)
    jobs = sorted(jobs, key=lambda x: x[1])
    n = len(jobs)
    # Compute p(j) with binary search
    def binary_search(j):
        lo, hi = 0, j-1
        while lo <= hi:
            mid = (lo + hi) // 2
            if jobs[mid][1] <= jobs[j][0]:
                if mid + 1 < j and jobs[mid+1][1] <= jobs[j][0]:
                    lo = mid + 1
                else:
                    return mid
            else:
                hi = mid - 1
        return -1
    p = [binary_search(j) for j in range(n)]
    dp = [0] * (n + 1)
    for j in range(1, n+1):
        incl = jobs[j-1][2] + dp[p[j-1]+1]
        excl = dp[j-1]
        dp[j] = max(incl, excl)
    # Reconstruct solution
    res = []
    j = n
    while j > 0:
        if jobs[j-1][2] + dp[p[j-1]+1] > dp[j-1]:
            res.append(j-1)
            j = p[j-1]+1
        else:
            j -= 1
    res.reverse()
    return dp[n], [jobs[i] for i in res]
# Example usage:
jobs = [
    (1, 4, 3),
    (3, 5, 2),
    (0, 6, 4),
    (4, 7, 5),
    (3, 8, 2),
    (5, 9, 4),
    (6, 10, 6),
    (8, 11, 8)
]
max_profit, selected_jobs = weighted_interval_scheduling(jobs)
print("Max profit:", max_profit)
print("Selected jobs:", selected_jobs)
```

---

# Conclusion

Weighted Interval Scheduling is best solved using Dynamic Programming with efficient `p(j)` computation via binary search (O(n log n)). The method works for any set of intervals/jobs with weights, and is widely used in resource allocation, scheduling, and optimization problems.
