# Weighted Interval Scheduling: Generalized Explanation, Examples & Simulation

Weighted Interval Scheduling is a classic problem that asks:  
**Given a set of jobs with start/end times and profits, how do you select a set of non-overlapping jobs to maximize total profit?**

This guide presents all major solution approaches in a generalized, beginner-friendly style, with examples and a simulation.

---

## Problem Overview

- **Input:** List of jobs, each with:
  - `start`: Start time
  - `end`: End time
  - `profit`: Profit for completing the job

- **Goal:** Choose non-overlapping jobs so that the sum of their profits is maximized.

---

## Example

Suppose you have these jobs:

| Job | Start | End | Profit |
|-----|-------|-----|--------|
| A   | 1     | 3   | 5      |
| B   | 2     | 5   | 6      |
| C   | 4     | 6   | 5      |
| D   | 6     | 7   | 4      |
| E   | 5     | 8   | 11     |
| F   | 7     | 9   | 2      |

---

## Naive Recursive Approach

### How it Works

For each job, you decide:
- **Include it:** Add its profit and skip to the next job that doesn't overlap.
- **Exclude it:** Move to the next job.

Repeat until all jobs are considered.

### Generalized Steps

1. Sort jobs by end time.
2. For each job, find the last job that doesn't overlap ("previous compatible job").
3. Use recursion to try all possibilities.

### Simplified Pseudocode

```python
def find_last_compatible(jobs, index):
    # Find the last job before 'index' that ends before jobs[index] starts
    for j in range(index - 1, -1, -1):
        if jobs[j].end <= jobs[index].start:
            return j
    return -1

def max_profit(jobs, index):
    if index < 0:
        return 0
    # Include the job
    include = jobs[index].profit + max_profit(jobs, find_last_compatible(jobs, index))
    # Exclude the job
    exclude = max_profit(jobs, index - 1)
    return max(include, exclude)
```

### Drawback

- **Very slow for large inputs** (tries all possibilities).

---

## Dynamic Programming (DP): Efficient Approach

### Key Idea

- Store results of subproblems to avoid repeated work.
- Build solutions step by step.

### Steps

1. **Sort jobs by end time.**
2. **Precompute previous compatible jobs for fast lookup.**
3. **Iteratively calculate best profit for each job.**

### Generalized Iterative Solution

```python
jobs = sorted(jobs, key=lambda job: job.end)
n = len(jobs)
dp = [0] * n  # dp[i] = max profit using jobs[0] to jobs[i]

for i in range(n):
    # Include current job
    profit_with = jobs[i].profit
    last = find_last_compatible(jobs, i)
    if last != -1:
        profit_with += dp[last]
    # Exclude current job
    profit_without = dp[i - 1] if i > 0 else 0
    # Choose the better option
    dp[i] = max(profit_with, profit_without)

max_profit = dp[-1]
```

#### Efficient Previous Job Lookup

Use binary search for large inputs (not shown for simplicity).

---

## Step-by-Step Simulation

Let’s solve the example above:

### Sorted Jobs by End

| Job | Start | End | Profit |
|-----|-------|-----|--------|
| A   | 1     | 3   | 5      |
| B   | 2     | 5   | 6      |
| C   | 4     | 6   | 5      |
| D   | 6     | 7   | 4      |
| E   | 5     | 8   | 11     |
| F   | 7     | 9   | 2      |

### DP Table Building

- **Job A:** Only itself, profit = 5
- **Job B:** Overlaps with A, so max(6, 5) = 6
- **Job C:** Last compatible is A, so max(5 + 5 = 10, 6) = 10
- **Job D:** Last compatible is C, so max(4 + 10 = 14, 10) = 14
- **Job E:** Last compatible is B, so max(11 + 6 = 17, 14) = 17
- **Job F:** Last compatible is D, so max(2 + 14 = 16, 17) = 17

**Maximum profit: 17**

### What jobs to pick?

Backtrack:
- Job E included (profit 11 + 6 from B)
- Job B included (profit 6)
- Total 17 (E and B, no overlap)

---

## Summary Table

| Approach        | Description                | Speed       | Use Case         |
|-----------------|---------------------------|-------------|------------------|
| Naive Recursion | Tries all combinations    | Very slow   | Learning, small  |
| DP (Iterative)  | Remembers subproblems     | Fast        | Real problems    |

---

## Generalized Python Example

```python
class Job:
    def __init__(self, start, end, profit):
        self.start = start
        self.end = end
        self.profit = profit

jobs = [
    Job(1, 3, 5),
    Job(2, 5, 6),
    Job(4, 6, 5),
    Job(6, 7, 4),
    Job(5, 8, 11),
    Job(7, 9, 2)
]

# Sort jobs by end time
jobs.sort(key=lambda job: job.end)

def find_last_compatible(jobs, index):
    for j in range(index - 1, -1, -1):
        if jobs[j].end <= jobs[index].start:
            return j
    return -1

n = len(jobs)
dp = [0] * n
for i in range(n):
    profit_with = jobs[i].profit
    last = find_last_compatible(jobs, i)
    if last != -1:
        profit_with += dp[last]
    profit_without = dp[i - 1] if i > 0 else 0
    dp[i] = max(profit_with, profit_without)

print("Maximum Profit:", dp[-1])  # Output: 17
```

---

## Conclusion

- Weighted Interval Scheduling is about picking non-overlapping jobs for max profit.
- The dynamic programming method is fast and easy to implement.
- Always sort jobs by end time, and use a helper to find previous compatible jobs.

---

## References

- CLRS "Introduction to Algorithms"
- [Weighted Interval Scheduling — Wikipedia](https://en.wikipedia.org/wiki/Interval_scheduling_maximization)
