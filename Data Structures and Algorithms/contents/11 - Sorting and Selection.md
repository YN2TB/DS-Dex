---
subject: Data Structures and Algorithms
chapter: 11
tags: [ds, dsa, sorting, merge-sort, quicksort, radix-sort, timsort, lower-bound, selection, quickselect, stability]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 12"
---

# Sorting and Selection

Sorting is the most studied problem in computing, and it is studied not because sorting is interesting but because **it is the one problem where we know the answer is optimal.** [[Discrete Mathematics/contents/09 - Trees|Discrete Maths ch. 09]] §8 proved that **no comparison-based sort can beat $\Omega(n\lg n)$**, and this chapter exhibits algorithms that meet it.

That makes sorting the natural home for three ideas that recur everywhere else:

- **A matching lower bound.** §4 checks how close real algorithms come to the information-theoretic floor — merge-sort turns out to be within **2%**.
- **Escaping a lower bound by changing the rules.** §5's radix sort is *linear*, which sounds impossible until you notice it never compares two keys.
- **Worst case versus expected case.** §3's quicksort is the fastest sort in practice and $O(n^2)$ on the most ordinary input imaginable.

**This chapter also closes the loop on [[10 - Search Trees|ch. 10]]**, which opened with a BST destroyed by sorted input. §3 shows quicksort has the identical flaw, from the identical cause, with the identical fix.

## 📘 Main Knowledge

### 0. Correctness before speed

Every algorithm below was checked against `sorted()` on nine inputs *before* anything was timed:

| input | merge | quick | randomised quick |
|---|---|---|---|
| empty, single element | ✓ | ✓ | ✓ |
| already sorted, reverse sorted | ✓ | ✓ | ✓ |
| **all elements equal** | ✓ | ✓ | ✓ |
| duplicates, two distinct values | ✓ | ✓ | ✓ |
| random, negative numbers | ✓ | ✓ | ✓ |

*(All pass.)* **The all-equal and two-value cases are the ones that break hand-written partition loops** — a partition that puts equal keys on one side recurses on a subarray of size $n-1$ and goes quadratic, or worse, loops forever. **A sort that only handles distinct random integers is not a working sort.**

### 1. Merge-sort — divide and conquer

Split in half, sort each half recursively, then merge the two sorted halves.

```python
def merge(A, B, S):
    """Merge sorted A and sorted B into S -- one pass, no backtracking."""
    i = j = 0
    while i + j < len(S):
        if j == len(B) or (i < len(A) and A[i] < B[j]):
            S[i + j] = A[i]; i += 1
        else:
            S[i + j] = B[j]; j += 1
```

**The merge is the whole idea.** Both inputs are sorted, so the smallest remaining element is at the front of one of them — one comparison decides. Each element is placed once, so merging is $O(n)$.

**The recursion tree has height exactly $\lceil\lg n\rceil$** (Goodrich Prop. 12.1), since the input halves each level:

| $n$ | 1 | 2 | 5 | 8 | 100 | 1 000 | 1 024 | 1 025 |
|---|---|---|---|---|---|---|---|---|
| depth | 0 | 1 | **3** | **3** | 7 | 10 | **10** | **11** |
| $\lceil\lg n\rceil$ | 0 | 1 | 3 | 3 | 7 | 10 | 10 | 11 |

*(Verified — note $n=1024$ gives 10 and $n=1025$ gives 11, the ceiling behaving exactly as claimed.)*

**Each level does $O(n)$ total merging work across all its subproblems, and there are $\lceil\lg n\rceil$ levels, so merge-sort is $O(n\log n)$** — worst case, not merely expected. Formally the recurrence is

$$T(n)=2T(n/2)+O(n)\;\Longrightarrow\;O(n\log n),$$

solved in [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]] and by the Master Theorem.

*(Verified — best-of-5 timings, since $n\log n$ predicts a doubling ratio of $2+2/\lg n$:)*

| $n$ | time | ratio | predicted |
|---|---|---|---|
| 50 000 | 0.1485 s | — | — |
| 100 000 | 0.3098 s | **2.09** | 2.13 |
| 200 000 | 0.6516 s | **2.10** | 2.12 |
| 400 000 | 1.6252 s | 2.49 | 2.11 |

**Ratios just above 2 — the signature of $n\log n$**, distinguishable from linear (exactly 2) and from quadratic (4). *(The last row runs high; single timings were noisier still — 2.56, 1.90, 2.78 — which is why the minimum of five repeats is the right estimator: scheduler noise only ever adds time.)*

### 2. Quicksort — divide and conquer the other way round

Merge-sort does trivial splitting and clever combining. **Quicksort inverts this: clever splitting, trivial combining.** Choose a pivot, partition into (smaller, equal, larger), recurse on the outer two — and then there is nothing to merge, because the parts are already in the right order relative to one another.

**When the pivot splits evenly, the recurrence is merge-sort's**, $T(n)=2T(n/2)+O(n)$, giving $O(n\log n)$.

### 3. Quicksort's worst case is sorted input — [[10 - Search Trees|ch. 10]]'s lesson again

**If the pivot is always the smallest or largest element, the partition is maximally uneven**: one side empty, the other of size $n-1$. Then

$$T(n)=T(n-1)+O(n)\;\Longrightarrow\;O(n^2).$$

**And taking the last element as the pivot does exactly that on sorted input:**

| $n$ (sorted input) | naive pivot | random pivot | naive slower by |
|---|---|---|---|
| 1 000 | 0.02214 s | 0.00073 s | **30.3×** |
| 2 000 | 0.07711 s | 0.00147 s | **52.6×** |
| 4 000 | 0.32218 s | 0.00443 s | **72.8×** |

**And the naive version's own doubling ratios confirm the class:**

| $n$ | time | ratio |
|---|---|---|
| 1 000 | 0.02436 s | — |
| 2 000 | 0.09822 s | **4.03** |
| 4 000 | 0.39098 s | **3.98** |

*(All verified.)* **Ratio 4 on doubling is $O(n^2)$** — and the slowdown factor grows with $n$ (30×, 53×, 73×), which is what a difference in complexity class looks like.

> [!warning] This is [[10 - Search Trees|ch. 10]] §1 all over again
> **Same input** (sorted), **same cause** (a structure that degenerates when every split is maximally uneven), **same $O(n)$-deep recursion**, **same practical danger** — sorted data is the *common* case, not an exotic one.
>
> **The fix here is randomisation:** choose the pivot uniformly at random. Goodrich Prop. 12.3 then gives $O(n\log n)$ **expected on every input**, because the adversary can no longer choose an input that provokes bad splits — they would have to predict the random choices.
>
> **So randomising the pivot is not a performance tweak; it is a correctness-of-performance requirement.** A textbook quicksort with a fixed pivot is a landmine. *(This is exactly the defence of [[09 - Maps, Hash Tables and Skip Lists|ch. 09]] §7 — randomised hashing against hash flooding — and of the [[09 - Maps, Hash Tables and Skip Lists|skip list]]: **move the choice out of the adversary's control.**)*
>
> **Median-of-three** (pivot = median of first, middle, last) is the common cheaper alternative. It removes the sorted-input case but **is still deterministic, so a crafted input can defeat it** — a real attack against PHP and Java has been demonstrated. Randomisation cannot be defeated this way.

**Quicksort can be made *in-place***, using $O(1)$ extra space beyond the recursion stack, by partitioning within the array with two converging indices. **Merge-sort cannot** — merging fundamentally needs somewhere to put the result, so it uses $O(n)$ extra space. **That, plus better cache behaviour, is why quicksort usually wins in practice despite the worse worst case.**

### 4. The lower bound, and how close we get

> [!note] The bound — proved in [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]] §8, not re-proved here
> **Any comparison-based sorting algorithm requires $\Omega(n\log n)$ comparisons in the worst case.**
>
> The argument in one line: a comparison sort is a **decision tree** whose leaves are the possible answers. There are $n!$ orderings, so the tree needs $\ge n!$ leaves; a binary tree with $n!$ leaves has height $\ge\lg(n!)$; and $\lg(n!)=\Theta(n\lg n)$ by Stirling. **The height is the worst-case number of comparisons.**

**The bound is $\lg(n!)$, and it does approach $n\lg n$:**

| $n$ | $\lg(n!)$ | $n\lg n$ | ratio |
|---|---|---|---|
| 10 | 21.8 | 33.2 | 0.656 |
| 100 | 524.8 | 664.4 | 0.790 |
| 1 000 | 8 529.4 | 9 965.8 | 0.856 |
| 10 000 | 118 458.1 | 132 877.1 | 0.891 |
| 100 000 | 1 516 704.2 | 1 660 964.0 | **0.913** |

*(Verified.)* **The ratio climbs steadily toward 1** — Stirling's $\lg(n!)=n\lg n-n\lg e+O(\lg n)$, whose correction term shrinks *relatively* as $n$ grows.

**Now the question the bound exists to answer: how close do real algorithms come?**

| $n$ | bound $\lg(n!)$ | merge-sort | vs bound | randomised quicksort | vs bound |
|---|---|---|---|---|---|
| 1 000 | 8 529 | 8 733 | **1.02×** | 10 624 | 1.25× |
| 10 000 | 118 458 | 120 487 | **1.02×** | 164 656 | 1.39× |
| 100 000 | 1 516 704 | 1 536 513 | **1.01×** | 2 056 471 | 1.36× |

*(Verified by instrumenting the comparison itself.)*

> [!note] Merge-sort is within 1–2% of the information-theoretic minimum
> **This is the strongest statement available about any algorithm: not "fast", but *provably almost unimprovable*.** No comparison sort, existing or yet to be invented, can do more than about 2% better than merge-sort on these inputs.
>
> **Randomised quicksort uses 25–39% more comparisons** — it is *asymptotically* optimal but has a worse constant, because a random pivot splits unevenly on average while merge-sort splits perfectly by construction. **Quicksort still usually wins on the clock**, because comparisons are not the only cost: it is in-place, moves less data, and is far kinder to the cache. **Counting comparisons is the right model for the lower bound and the wrong model for predicting runtime.**

### 5. Beating the bound by not comparing

The bound constrains **comparison-based** sorts. **Algorithms that look *inside* keys are not bound by it.**

**Bucket-sort.** If keys are integers in $[0,N)$, make $N$ buckets, drop each key into its bucket, concatenate. **$O(n+N)$ time and space** — linear when $N=O(n)$, useless when $N$ is huge (sorting 1 000 keys drawn from $[0,2^{32})$ would need four billion buckets).

**Radix-sort.** Fix that by sorting one digit at a time, least-significant first, with a *stable* bucket-sort per digit. With $d$ digits in base $b$: **$O(d(n+b))$ — linear in $n$.**

```python
def radix_sort(S, digits, base=10):
    out = list(S)
    for d in range(digits):                        # least significant digit first
        buckets = [[] for _ in range(base)]
        div = base ** d
        for x in out:
            buckets[(x // div) % base].append(x)   # stable: append preserves order
        out = [x for b in buckets for x in b]
    return out
```

> [!warning] Radix-sort only works because bucket-sort is stable
> Each pass must preserve the order established by the previous, less significant digit. **If the per-digit sort were unstable, every pass would destroy the last one's work and the result would be wrong.** This is stability doing real algorithmic work, not just being a convenience — see §6.
>
> **Least-significant-digit first is also essential.** Most-significant-first sounds more natural and gives the wrong answer without recursing separately into every bucket.

*(Verified correct on 3-digit and 6-digit keys, and against `sorted()` at $n=2\,000$.)*

**Timings, keys in $[0,10^6)$:**

| $n$ | my merge-sort | my radix-sort | `sorted()` |
|---|---|---|---|
| 100 000 | 0.2816 s | **0.0571 s** | 0.0136 s |
| 200 000 | 0.5998 s | **0.1368 s** | 0.0309 s |
| 400 000 | 1.3122 s | **0.4332 s** | 0.0686 s |

**Radix beats my merge-sort by 3–5×** — both written in Python, so this is a fair like-for-like comparison. **It does not contradict [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]** because it never compares two keys; it reads digits out of them.

> [!note] The general lesson
> **A lower bound constrains a *model*, not a problem.** $\Omega(n\lg n)$ says "no algorithm that only compares keys can do better". Change what the algorithm may do — look inside keys — and the bound simply does not apply.
>
> **This is worth generalising: when you hit a proven lower bound, check its assumptions before concluding the problem is closed.** The bound is a statement about the rules of the game.
>
> **The catch is that the rules cost something.** Radix-sort needs keys of bounded, known length that decompose into digits; it is not a general-purpose sort. `sorted()` still beats it here by 6× — because `sorted()` is C and mine is Python (§8).

### 6. Stability

> [!note] Definition
> A sort is **stable** if elements with equal keys keep their original relative order.

```
records                     [('alice',3), ('bob',1), ('carol',3), ('dave',1), ('eve',2)]
sorted by score (stable)    [('bob',1), ('dave',1), ('eve',2), ('alice',3), ('carol',3)]
```

*(Verified.)* **`bob` precedes `dave` and `alice` precedes `carol`** — the input order survives within each score.

**Why it matters: stability makes multi-key sorting composable.** To sort by score, then by name within score, **sort by name first, then by score.** The second sort preserves the first's work exactly where the scores tie. *(Verified: the two-pass result matches.)* Without stability you would need a compound comparator for every combination.

**And §5's radix-sort depends on it outright** — each digit pass would otherwise destroy the previous one.

| stable | not stable |
|---|---|
| merge-sort, bucket, radix, **Timsort (Python's)** | **quicksort**, heap-sort ([[08 - Priority Queues and Heaps\|ch. 08]]) |

**Quicksort is unstable because partitioning swaps distant elements**, jumping equal keys past one another. Making it stable requires $O(n)$ extra space, which forfeits its main advantage over merge-sort.

**Python's `sorted()` and `list.sort()` are guaranteed stable** — a documented language guarantee you may rely on.

### 7. Timsort — Python's sort exploits order that is already there

`sorted()` uses **Timsort**: merge-sort hybridised with insertion sort, which finds already-ordered **runs** in the input and merges them.

| input ($n=10^6$) | time | vs random |
|---|---|---|
| random | 0.2212 s | — |
| **already sorted** | **0.0261 s** | **8.5× faster** |
| **reverse sorted** | **0.0275 s** | **8.0× faster** |
| 90% sorted | 0.0661 s | 3.3× faster |
| **all equal** | **0.0040 s** | **55× faster** |

*(Verified.)*

> [!note] The comparison that matters
> **Sorted input is Timsort's *best* case and naive quicksort's *worst* case.** §3 measured naive quicksort 73× *slower* on sorted input; Timsort is 8.5× *faster* on it.
>
> **Timsort is $O(n)$ on already-sorted input** — one pass finds a single run and there is nothing to merge. It detects descending runs and reverses them, hence reverse-sorted being equally fast. The all-equal case is fastest of all: one run, no merging, and every comparison fails immediately.
>
> **This is real-world engineering, not asymptotics.** Real data is often partly ordered — appended logs, concatenated sorted files, data sorted by another key. Timsort's worst case is still $O(n\log n)$, so exploiting order costs nothing when there is none.

### 8. The constant factor: never write your own sort in Python

| $n=400\,000$ | time |
|---|---|
| my merge-sort | 1.7507 s |
| **`sorted()`** | **0.1216 s — 14× faster** |

*(Verified.)* **Both are $O(n\log n)$.** The entire gap is a constant factor: `sorted()` is C, mine is interpreted Python.

> [!warning] A 14× constant swamps most algorithmic improvements
> Getting from $O(n^2)$ to $O(n\log n)$ is worth far more than 14× at large $n$ — that is why complexity is the primary lens ([[02 - Algorithm Analysis in Practice|ch. 02]]). **But between two algorithms of the same class, implementation language decides**, and no amount of cleverness in Python recovers 14×.
>
> **Practical rule: call `sorted()`.** Hand-written sorts are for understanding, not for use. The same applies to `heapq` ([[08 - Priority Queues and Heaps|ch. 08]]), `dict` ([[09 - Maps, Hash Tables and Skip Lists|ch. 09]]) and `collections.deque` ([[05 - Stacks, Queues and Deques|ch. 05]]) — **all are C implementations of what these chapters build by hand.**

### 9. Selection — finding the $k$-th smallest without sorting

**Sorting to find the median does far more work than necessary.** *Quick-select* uses quicksort's partition but **recurses into only one side**, since after partitioning you know which part contains the $k$-th element.

```python
def quick_select(S, k):
    if len(S) == 1:
        return S[0]
    pivot = random.choice(S)
    L = [x for x in S if x < pivot]
    E = [x for x in S if x == pivot]
    G = [x for x in S if x > pivot]
    if k <= len(L):
        return quick_select(L, k)              # ONE side, not two
    elif k <= len(L) + len(E):
        return pivot
    return quick_select(G, k - len(L) - len(E))
```

*(Verified against `sorted()[k-1]` for $k=1,2,100,2500,4999,5000$ — first, last, middle and near-boundary.)*

**Recursing into one side changes everything:**

$$T(n)=T(n/2)+O(n)=n+\tfrac n2+\tfrac n4+\cdots=2n\;\Longrightarrow\;\mathbf{O(n)}.$$

**The geometric series collapses.** Compare merge-sort's $T(n)=2T(n/2)+O(n)$: the *only* difference is the coefficient 2 versus 1, and that single coefficient is the whole difference between $n\log n$ and $n$.

*(Verified — elements examined to find the median:)*

| $n$ | elements examined | $\div n$ |
|---|---|---|
| 50 000 | 176 340 | 3.53 |
| 100 000 | 279 756 | 2.80 |
| 200 000 | 506 866 | 2.53 |
| 400 000 | 1 242 294 | 3.11 |
| 800 000 | 2 458 107 | 3.07 |

**A bounded multiple of $n$ that does not grow — linear, confirmed.** *(It fluctuates because the pivot is random; sorting would need $n\lg n$, which at $n=800\,000$ is $\lg n\approx19.6$ times more work.)*

**Like-for-like in Python** (both my own code, so the language cancels):

| $n$ | merge-sort | ratio | quick-select | ratio | select faster by |
|---|---|---|---|---|---|
| 50 000 | 0.1481 s | — | 0.0236 s | — | **6.3×** |
| 100 000 | 0.3326 s | 2.25 | 0.1044 s | — | 3.2× |
| 200 000 | 0.7142 s | 2.15 | 0.1087 s | 1.04 | **6.6×** |
| 400 000 | 1.8807 s | 2.63 | 0.3409 s | 3.14 | 5.5× |

*(Verified.)*

> [!warning] My first attempt at this measurement was wrong, and instructively so
> I initially compared `quick_select` against `sorted(data)[k-1]` and **quick-select lost** — 0.3117 s against 0.1216 s at $n=400\,000$.
>
> **That comparison measures the language, not the algorithm**: a linear algorithm in interpreted Python against an $n\log n$ algorithm in C, where §8's 14× constant dominates. **The fix is to compare like with like** — both in Python, or count operations instead of seconds. Both corrected measurements agree with the theory.
>
> **This is the same trap as [[10 - Search Trees|ch. 10]] §4.2's splay-versus-AVL timing**, and the general rule is worth stating: **when a measurement contradicts a sound proof, suspect the measurement first** — usually something other than the intended variable is being measured.

*(A deterministic $O(n)$ worst-case selection exists — *median of medians* — but its constant is large enough that randomised quick-select is preferred in practice.)*

### 10. Choosing

| | worst case | space | stable | in-place | notes |
|---|---|---|---|---|---|
| **merge-sort** | $O(n\log n)$ | $O(n)$ | ✓ | ✗ | within 2% of the bound; good for linked lists and external data |
| **quicksort** | $O(n^2)$ | $O(\log n)$ | ✗ | ✓ | fastest in practice — **randomise the pivot** |
| **heap-sort** ([[08 - Priority Queues and Heaps\|ch. 08]]) | $O(n\log n)$ | $O(1)$ | ✗ | ✓ | the only one that is both worst-case optimal and in-place |
| **Timsort** | $O(n\log n)$ | $O(n)$ | ✓ | ✗ | **$O(n)$ on sorted input**; Python's, and the right default |
| **radix-sort** | $O(dn)$ | $O(n+b)$ | ✓ | ✗ | linear, but needs bounded decomposable keys |
| **quick-select** | $O(n^2)$ | $O(1)$ | — | ✓ | $O(n)$ expected — **selection, not sorting** |

**In Python: use `sorted()`.** Use `heapq.nsmallest(k, …)` for the $k$ smallest, and `statistics.median` for a median. Write a sort yourself only to understand one.

## ✏️ Exercises

**1. (Merge-sort.)** (a) Why is merging linear? (b) Why is the tree height exactly $\lceil\lg n\rceil$, and why is merge-sort $O(n\log n)$ *worst case*? (c) Interpret the timings and explain the best-of-5 method. (d) What does merge-sort give up?

> [!example]- Solution
> **(a) Because each comparison places one element permanently.** Both inputs are sorted, so the overall smallest remaining element must be at the front of one of them — a single comparison identifies it, with no backtracking and no rescanning. **$n$ elements, one placement each, $O(n)$.**
>
> **This is why sortedness is worth having**: merging two *unsorted* halves would require comparing everything with everything.
>
> **(b) Because each level halves the input**, so after $k$ levels the pieces have size $n/2^k$, and recursion stops at size 1 when $2^k\ge n$, i.e. $k=\lceil\lg n\rceil$. *(Verified: $n=1024\to10$ and $n=1025\to11$.)*
>
> **Each level does $O(n)$ total work** — the subproblems at a level partition the input, so their merges sum to $n$ regardless of how many there are. **Height $\times$ work per level $=O(n\log n)$.**
>
> **It is worst case, not expected, because the split is by *position*, not by value.** Merge-sort halves the array no matter what the data is, so no input can unbalance it. **This is precisely what quicksort cannot promise** (§3): its split depends on the pivot's value.
>
> **(c)**
>
> | $n$ | time | ratio | predicted |
> |---|---|---|---|
> | 50 000 | 0.1485 s | — | — |
> | 100 000 | 0.3098 s | 2.09 | 2.13 |
> | 200 000 | 0.6516 s | 2.10 | 2.12 |
> | 400 000 | 1.6252 s | 2.49 | 2.11 |
>
> **For $n\log n$, doubling $n$ multiplies the time by $2+2/\lg n$** — slightly above 2, and decreasing slowly. The measured 2.09 and 2.10 match 2.13 and 2.12 closely.
>
> **Best-of-5 matters because timing noise is one-sided.** The OS can only ever *steal* time; nothing makes a run faster than it should be. **So the minimum is the best estimate of true cost**, while a mean is inflated by whatever else the machine was doing. Single runs gave 2.56, 1.90, 2.78 — too noisy to distinguish $n\log n$ from linear; the minimum-of-5 gave 2.09, 2.10.
>
> **(d) $O(n)$ extra space** — it cannot sort in place, because merging needs somewhere to write. Quicksort and heap-sort need $O(\log n)$ and $O(1)$ respectively.
>
> **Also worse cache behaviour and more data movement**, which is why quicksort usually wins on the clock despite needing 25–39% more comparisons (§4).
>
> **But merge-sort keeps three things quicksort lacks:** a **worst-case** guarantee, **stability**, and the fact that it works well when data cannot be randomly accessed — linked lists, or files too large for memory, where the sequential merge is exactly right.

**2. (Quicksort's worst case.)** (a) Why does sorted input trigger it? (b) Derive $O(n^2)$ and interpret the ratios. (c) Why is randomising the pivot not merely an optimisation? (d) Why is median-of-three weaker than randomisation?

> [!example]- Solution
> **(a) Because the last element of a sorted array is its maximum.** Partitioning around the maximum puts all $n-1$ other elements on one side and nothing on the other — **the least useful split possible.** The recursion then shrinks the problem by one element per level instead of halving it.
>
> **The tree of recursive calls becomes a path of depth $n$** — structurally identical to [[10 - Search Trees|ch. 10]] §1's degenerate BST, and for the same reason: every split is maximally uneven.
>
> **(b)** With splits of sizes $0$ and $n-1$, and partitioning costing $O(n)$:
> $$T(n)=T(n-1)+O(n)=\sum_{k=1}^{n}O(k)=O(n^2).$$
>
> *(Verified:)*
>
> | $n$ | time | ratio |
> |---|---|---|
> | 1 000 | 0.02436 s | — |
> | 2 000 | 0.09822 s | **4.03** |
> | 4 000 | 0.39098 s | **3.98** |
>
> **Ratio 4 on doubling is quadratic** ([[02 - Algorithm Analysis in Practice|ch. 02]]): $(2n)^2/n^2=4$.
>
> **And the comparison against the randomised version shows the classes diverging** — 30.3×, 52.6×, 72.8× slower at $n=1\,000$, $2\,000$, $4\,000$. **A constant-factor difference would hold steady; a growing multiple means different complexity classes.**
>
> **(c) Because without it the algorithm is quadratic on the most ordinary input there is.**
>
> Sorted (or reverse-sorted, or nearly-sorted) data is everywhere: database exports, log files, IDs, the output of a previous sort, concatenated sorted files. **A fixed-pivot quicksort meets its worst case routinely, not rarely.**
>
> **The randomised version's guarantee is qualitatively different.** Goodrich Prop. 12.3 gives $O(n\log n)$ expected **for every input** — the expectation is over the algorithm's coin flips, not over a distribution of inputs. **No input is bad; only unlucky coin flips are, and the adversary cannot see them.**
>
> **This is the third appearance of the same defence:** [[09 - Maps, Hash Tables and Skip Lists|ch. 09]] §7's randomised hashing against hash flooding, and the skip list's random levels. **Move the choice out of the adversary's control** — and note this pattern is invisible to worst-case analysis alone, which is why it is worth naming.
>
> **(d) Because it is deterministic, and anything deterministic can be reverse-engineered.**
>
> Median-of-three (first, middle, last) does eliminate the sorted-input case — the middle element of a sorted array is its median, the *best* possible pivot. It is cheap and widely used.
>
> **But an attacker who knows the rule can construct an input that makes all three choices bad at every level**, restoring $O(n^2)$. Such "quicksort killer" inputs have been demonstrated against real language runtimes, as a denial-of-service vector.
>
> **Randomisation is immune** because the attacker would have to predict the random number generator, not merely read the source. **Hence: median-of-three for speed on benign data; randomisation when input is untrusted.** *(Production sorts often use `introsort` — quicksort that counts its recursion depth and switches to heap-sort past $\sim2\lg n$, guaranteeing $O(n\log n)$ worst case while keeping quicksort's speed.)*

**3. (Hard — the lower bound.)** (a) Sketch the $\Omega(n\lg n)$ argument. (b) Why does $\lg(n!)/(n\lg n)$ rise toward 1? (c) Interpret the comparison counts. (d) Merge-sort uses fewer comparisons but quicksort is usually faster — resolve this.

> [!example]- Solution
> **(a)** *(Proved in [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]] §8 — sketched here, not re-proved.)*
>
> Model any comparison sort as a **decision tree**: internal nodes are comparisons, the two branches are the outcomes, leaves are output orderings. A particular execution is a root-to-leaf path, so **the worst-case comparison count is the tree's height.**
>
> 1. The algorithm must distinguish all $n!$ input orderings — if two reached the same leaf it would output the same permutation for both, and one would be wrong.
> 2. So the tree has $\ge n!$ leaves.
> 3. A binary tree with $L$ leaves has height $\ge\lg L$, so height $\ge\lg(n!)$.
> 4. $\lg(n!)=\Theta(n\lg n)$ by Stirling.
>
> **The elegance is that it constrains *every* algorithm, including undiscovered ones**, by counting information rather than examining any procedure: distinguishing $n!$ possibilities needs $\lg(n!)$ binary answers. **This is why it holds for a model, not a problem — see (d) of Exercise 4.**
>
> **(b) Because Stirling's correction term shrinks *relatively*.** Taking logs of $n!\approx\sqrt{2\pi n}\,(n/e)^n$:
> $$\lg(n!)=n\lg n-n\lg e+O(\lg n),$$
> with $\lg e\approx1.4427$. So
> $$\frac{\lg(n!)}{n\lg n}\approx1-\frac{1.4427}{\lg n}.$$
>
> **Check against the data:** at $n=10^5$, $\lg n=16.6$, giving $1-1.4427/16.6=0.913$ — **exactly the measured 0.913.** At $n=1\,000$: $1-1.4427/9.97=0.855$ against the measured 0.856. ✓
>
> **The convergence is slow** — the correction is $O(1/\lg n)$, so even at $n=10^5$ the bound is 9% below $n\lg n$. **Both forms are correct asymptotically**; $\lg(n!)$ is the exact bound and $n\lg n$ its leading term.
>
> **(c)**
>
> | $n$ | bound | merge-sort | randomised quicksort |
> |---|---|---|---|
> | 1 000 | 8 529 | 8 733 (**1.02×**) | 10 624 (1.25×) |
> | 10 000 | 118 458 | 120 487 (**1.02×**) | 164 656 (1.39×) |
> | 100 000 | 1 516 704 | 1 536 513 (**1.01×**) | 2 056 471 (1.36×) |
>
> **Merge-sort comes within 1–2% of the information-theoretic minimum, and the gap narrows as $n$ grows.** This is an unusually strong statement: **not "merge-sort is fast" but "no comparison sort can be more than ~2% better."**
>
> Merge-sort achieves this because **it splits perfectly by construction** — position-based halving needs no luck. Randomised quicksort's pivot lands off-centre on average, so its subproblems are less balanced and it pays 25–39% more comparisons.
>
> **(d) Because comparisons are not the cost that dominates.**
>
> The lower bound counts comparisons because that is the model in which it can be *proved*. **Actual runtime is dominated by other things:**
>
> 1. **Memory traffic.** Merge-sort allocates and copies $O(n)$ extra data at every level. Quicksort partitions in place — the same array throughout.
> 2. **Cache behaviour.** Quicksort's partition is two scans converging through contiguous memory, which prefetchers handle perfectly. Merge-sort interleaves reads from two regions and writes to a third. **This is [[10 - Search Trees|ch. 10]] §7's memory-hierarchy argument** — the constant that asymptotic analysis is designed not to see.
> 3. **Allocation.** In Python, merge-sort's slicing creates new list objects constantly.
>
> **So merge-sort wins the metric the bound measures and loses the one users experience.** Neither is wrong; they measure different things.
>
> **The general lesson — perhaps the most transferable in this chapter: a lower bound tells you what is impossible in a model, not what is fastest on a machine.** Use it to know when to stop optimising (merge-sort is within 2% — there is nothing left to find), not to predict runtime. **§8's 14× C-versus-Python gap is invisible to every argument in this exercise.**

**4. (Radix-sort and stability.)** (a) How is radix-sort linear? (b) Why must the per-digit sort be stable and least-significant-first? (c) Why is this not a contradiction? (d) Why is `sorted()` still preferred?

> [!example]- Solution
> **(a) By sorting on one digit at a time with bucket-sort, never comparing two keys.**
>
> Bucket-sort places each key directly into the bucket its digit names — an array index, not a comparison — so a pass over $n$ keys with $b$ buckets is $O(n+b)$. With $d$ digits, **$O(d(n+b))$, linear in $n$** for fixed $d$ and $b$.
>
> **The reason it evades the bound is that a bucket placement extracts more than one bit of information.** A comparison yields one bit; indexing into one of $b=10$ buckets yields $\lg 10\approx3.3$ bits. **The decision tree of Exercise 3 is not binary any more**, so the height bound $\lg_2(n!)$ does not apply.
>
> **The hidden cost is that $d$ depends on the key range**: distinguishing $n$ distinct keys needs $d\ge\log_b n$ digits, so "linear" quietly assumes bounded key length. Sorting $n$ arbitrary-precision integers is not linear.
>
> **(b) Stability is what makes the passes compose.** After sorting by the units digit, keys agreeing in the units digit are correctly ordered among themselves. The tens-digit pass must **preserve that order wherever tens digits tie.** A stable sort does exactly this; **an unstable one would scramble the previous pass's work and the result would be wrong.**
>
> *(In §5's code the stability comes from `buckets[...].append(x)` while scanning left to right — equal-digit keys enter their bucket in their current relative order and leave in it.)*
>
> **Least-significant-first is essential** because the passes build the ordering from weakest key to strongest: the final, most-significant pass dominates, and stability preserves all the earlier work as tie-breaking. **Most-significant-first destroys this** — the first pass would group by leading digit and later passes would reorder across those groups. MSD radix sort exists but must recurse into each bucket separately.
>
> **This is stability doing load-bearing algorithmic work**, not merely being convenient as in §6's multi-key sorting.
>
> **(c) Because the $\Omega(n\lg n)$ bound constrains comparison-based algorithms, and radix-sort is not one.**
>
> Exercise 3's proof assumes the only operation is a two-way comparison. Radix-sort reads digits **out of** keys and uses them as addresses — an operation the model does not contain. **The theorem is not violated; its hypothesis is not met.**
>
> **The transferable point: a lower bound is a statement about a model of computation, so when you hit one, check its assumptions before concluding the problem is closed.** The cost is generality — radix-sort needs fixed-length keys decomposable into digits, and cannot sort by an arbitrary comparator. **Bounds are usually traded away, not broken.**
>
> **(d)**
>
> | $n$ | my merge-sort | my radix-sort | `sorted()` |
> |---|---|---|---|
> | 100 000 | 0.2816 s | 0.0571 s | **0.0136 s** |
> | 400 000 | 1.3122 s | 0.4332 s | **0.0686 s** |
>
> **Radix beats my merge-sort by 3–5× — a fair Python-to-Python comparison confirming the theory. But `sorted()` beats radix by 4–6× despite being $O(n\log n)$ against $O(n)$**, purely because it is C (§8's 14× constant).
>
> **Five further reasons to prefer `sorted()`:**
> 1. **Generality** — any comparable objects, any `key=`; radix needs integer-like keys.
> 2. **Timsort exploits existing order** (§7) — up to 55× on structured input; radix always pays $d$ full passes.
> 3. **Memory** — radix rebuilds the whole list once per digit.
> 4. **Stability and correctness are guaranteed and tested** by the language.
> 5. **Zero code to maintain.**
>
> **Radix-sort earns its place only with huge $n$, fixed-width keys, and an implementation in a compiled language** — which is where it genuinely wins, in databases and GPU sorting.

**5. (Hard — selection.)** (a) Why is quick-select $O(n)$ when quicksort is $O(n\log n)$? (b) Interpret the elements-examined table. (c) My first timing said quick-select was *slower* — what went wrong and what is the general lesson? (d) When would you sort instead of selecting?

> [!example]- Solution
> **(a) Because it recurses into one side instead of two.** After partitioning, the sizes of $L$ and $E$ say which part contains the $k$-th element; **the other part cannot contain it and is discarded entirely.**
>
> $$\text{quicksort:}\quad T(n)=2T(n/2)+O(n)\;\Rightarrow\;O(n\log n)$$
> $$\text{quick-select:}\quad T(n)=1\cdot T(n/2)+O(n)\;\Rightarrow\;O(n)$$
>
> **Unrolling the second:** $n+\frac n2+\frac n4+\cdots=2n$. **The geometric series converges**, so the total is a constant multiple of the first level's work.
>
> **The contrast with quicksort is exact and worth dwelling on.** There, each level's subproblems still total $n$ — halving the size doubles the count, so the sum telescopes to $n$ *per level*, over $\lg n$ levels. **Here the count stays at one, so the sizes shrink geometrically and the total is $O(n)$.**
>
> **The whole difference is the coefficient 2 versus 1** — nothing else about the two algorithms differs. **That is the clearest illustration in the vault of why the coefficient in a divide-and-conquer recurrence matters more than anything else in it** ([[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]]; Master Theorem).
>
> **(b)**
>
> | $n$ | examined | $\div n$ |
> |---|---|---|
> | 50 000 | 176 340 | 3.53 |
> | 100 000 | 279 756 | 2.80 |
> | 200 000 | 506 866 | 2.53 |
> | 400 000 | 1 242 294 | 3.11 |
> | 800 000 | 2 458 107 | 3.07 |
>
> **The ratio stays around 3 and shows no upward trend across a 16-fold increase in $n$ — that is what linear looks like.** Had it been $O(n\log n)$ the column would have grown like $\lg n$: 15.6, 16.6, 17.6, 18.6, 19.6.
>
> **The fluctuation (2.53 to 3.53) is the random pivot**, not noise in the timer — this counts operations exactly. Some runs are luckier than others; the theory promises a bound in *expectation*.
>
> **Why ~3 rather than the idealised 2:** the analysis assumes a perfect halving, but a uniformly random pivot leaves a fraction that is uniform on average, so the expected constant for the median is nearer 4. **The measured ~3 sits sensibly between the idealised 2 and the pessimistic 4.**
>
> **And the comparison with sorting:** at $n=800\,000$, sorting needs $\approx n\lg n$ operations against selection's $\approx3n$ — **about 6.5× less work, growing with $n$.**
>
> **(c) I compared my Python `quick_select` against C's `sorted()`** and got 0.3117 s versus 0.1216 s at $n=400\,000$ — apparently refuting a correct proof.
>
> **The error is that two variables changed at once**: the algorithm ($O(n)$ vs $O(n\log n)$) *and* the implementation language. §8 measured the language gap at **14×**, while the algorithmic advantage here is about 6× — so the language term dominated and reversed the sign.
>
> **Two fixes, both applied, both agreeing with the theory:**
> - **Count operations instead of seconds** — table (b), unambiguously linear.
> - **Compare like with like** — both in Python: quick-select is **3.2–6.6× faster** than merge-sort.
>
> **The general lesson: when a measurement contradicts a sound proof, suspect the measurement.** Something other than the intended variable is usually being measured. **The remedy is to hold everything else constant, or to count operations, which no implementation detail can distort.**
>
> **This is the third time in this subject that a first measurement misled:** [[08 - Priority Queues and Heaps|ch. 08]]'s heapify-versus-insertion (fixed by constructing the worst case rather than trusting random input), [[10 - Search Trees|ch. 10]] §4.2's splay-versus-AVL (fixed by counting node visits), and this one. **In all three the theory was right and the first experiment was badly designed — which is itself the most useful thing this subject has taught.**
>
> **(d) Sort when you need more than a constant number of order statistics.**
>
> - **One value** (median, minimum, 90th percentile) — **select**: $O(n)$ against $O(n\log n)$.
> - **A few values** — select repeatedly, while $k\cdot n<n\log n$, i.e. while $k<\log n$ (about 20 for $n=10^6$).
> - **Many values, or a full ranking, or repeated queries against the same data** — **sort once.** After sorting, every order statistic is $O(1)$, so one $O(n\log n)$ investment answers unlimited queries; repeated selection would pay $O(n)$ each time.
> - **The $k$ smallest** — neither: use a bounded heap ([[08 - Priority Queues and Heaps|ch. 08]]), $O(n\log k)$, better than both when $k\ll n$. In Python, `heapq.nsmallest`.
>
> **Also prefer sorting when you need stability, a worst-case guarantee (quick-select's worst case is $O(n^2)$ too), or output that is useful for anything else.** *(Median-of-medians gives deterministic $O(n)$ worst-case selection but with a constant large enough that randomised quick-select is preferred in practice.)*
>
> **In Python, all of this is library work:** `sorted()`, `heapq.nsmallest(k, …)`, `statistics.median`.

## 📝 Summary

- **Correctness before speed.** Every sort was checked on nine inputs including **all-equal** and two-value data — the cases that break hand-written partition loops.
- **Merge-sort:** split by position, sort, merge. Merging is $O(n)$ because both halves are sorted; the tree height is exactly $\lceil\lg n\rceil$ *(verified, including $n=1024\to10$ and $1025\to11$)*; so $O(n\log n)$ **worst case** — the split is by position, so no input can unbalance it. *(Measured ratios 2.09, 2.10 against a predicted 2.13.)*
- **Quicksort inverts merge-sort** — clever splitting, trivial combining — and is **$O(n^2)$ on sorted input** with a fixed pivot. *(Measured: doubling ratios 4.03, 3.98, and 30×/53×/73× slower than the randomised version.)*
- **This is [[10 - Search Trees|ch. 10]] §1's failure exactly** — same input, same cause, same fix. **Randomising the pivot is a correctness-of-performance requirement, not an optimisation.** Median-of-three is deterministic and therefore still defeatable.
- **The $\Omega(n\lg n)$ bound is proved in [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]] §8** by decision tree: $n!$ orderings need $\lg(n!)$ comparisons. *(Verified that $\lg(n!)/(n\lg n)$ climbs 0.656 → 0.913, matching Stirling's $1-1.4427/\lg n$ to three decimals.)*
- **Merge-sort comes within 1–2% of that bound** *(measured 1.02×, 1.02×, 1.01×)* — **provably almost unimprovable.** Randomised quicksort needs 25–39% more comparisons yet is usually faster, because comparisons are not what dominates runtime.
- **Radix-sort is linear** *(measured 3–5× faster than my merge-sort)* and does **not** contradict the bound, because it never compares keys — it reads digits out of them. **A lower bound constrains a model, not a problem.**
- **Radix-sort works only because its per-digit bucket-sort is stable and runs least-significant-digit first** — otherwise each pass destroys the last.
- **Stability** means equal keys keep their input order. It makes multi-key sorting composable (sort by the secondary key first). **Merge, bucket, radix and Timsort are stable; quicksort and heap-sort are not.**
- **Timsort (Python's) exploits existing order:** *(measured at $n=10^6$)* already-sorted **8.5×** faster than random, reverse-sorted 8.0×, all-equal **55×**. **Sorted input is Timsort's best case and naive quicksort's worst.**
- **`sorted()` beat my merge-sort by 14×** at the same complexity — a pure C-versus-Python constant. **Never hand-write a sort in Python.**
- **Quick-select finds the $k$-th smallest in $O(n)$** by recursing into **one** side: $T(n)=T(n/2)+O(n)=2n$. **The only difference from merge-sort is the coefficient 2 versus 1 — and that is the entire difference between $n\log n$ and $n$.** *(Verified: ~3n elements examined, flat across a 16-fold increase in $n$.)*
- **My first quick-select timing said it was slower** — because it compared Python against C. **When a measurement contradicts a sound proof, suspect the measurement**: hold the implementation constant, or count operations.

## ⚠️ Important Notes

1. **Test all-equal and two-value inputs.** They are what break partition loops — a partition that sends equal keys one way goes quadratic or loops forever, and random-integer tests never reveal it.
2. **Never use a fixed-pivot quicksort.** Sorted input makes it $O(n^2)$, and sorted input is ordinary. **Randomise, or use `sorted()`.**
3. **Median-of-three is not a substitute for randomisation** against untrusted input — it is deterministic, so a crafted input restores $O(n^2)$. Real "quicksort killer" attacks exist.
4. **Merge-sort is $O(n\log n)$ worst case; quicksort only in expectation.** If tail latency matters, that difference is the whole story. Production sorts use **introsort** — quicksort that falls back to heap-sort past depth $\sim2\lg n$.
5. **The lower bound is $\lg(n!)$; $n\lg n$ is its leading term.** They differ by 9% even at $n=10^5$, since the correction is $O(1/\lg n)$.
6. **The $\Omega(n\lg n)$ bound applies only to comparison sorts.** Radix and bucket sort are linear and violate nothing. **Check a bound's assumptions before believing a problem is closed.**
7. **Radix-sort's "linear" hides a dependence on key length** — $d\ge\log_b n$ digits are needed to distinguish $n$ keys, so it is not linear for unbounded keys.
8. **Radix-sort breaks silently if the per-digit sort is unstable or runs most-significant-first.** It produces plausible, wrong output.
9. **Python's `sorted()` and `list.sort()` are guaranteed stable** — rely on it. Sort by the *secondary* key first when sorting on multiple keys.
10. **Sorting already-sorted data is nearly free in Python and catastrophic in a fixed-pivot quicksort.** Know which sort you are using before reasoning about its input.
11. **`sorted()` is ~14× faster than an equivalent hand-written Python sort.** Between algorithms of the same complexity class, **the implementation language decides.**
12. **Compare like with like.** Timing Python against C measures the language. **Count operations when the implementations differ** — no implementation detail can distort an operation count.
13. **When a measurement contradicts a sound proof, suspect the measurement first.** This chapter, [[08 - Priority Queues and Heaps|ch. 08]] and [[10 - Search Trees|ch. 10]] all produced a misleading first result from a badly designed experiment.
14. **Select, don't sort, for a single order statistic** — $O(n)$ against $O(n\log n)$. But **sort once** if you need many, or will query repeatedly.
15. **For the $k$ smallest use a bounded heap** ([[08 - Priority Queues and Heaps|ch. 08]]), $O(n\log k)$ — better than sorting *and* than repeated selection when $k\ll n$. In Python, `heapq.nsmallest`.
16. **Quick-select's worst case is $O(n^2)$ too**, for the same reason as quicksort's. Randomise the pivot here as well.

> [!warning] Gaps in the source material
> **Goodrich's ch. 12 prose extracts well** — the merge-sort tree and Propositions 12.1–12.2, the randomised quicksort analysis (Prop. 12.3), the in-place partition discussion, the decision-tree lower bound (Prop. 12.4), bucket-sort and radix-sort, the definition of stability, and §12.7 on selection all came through readably. **Goodrich page $n$ = PDF page $n+22$; ch. 12 is PDF 558–597.**
>
> **His code did not**, per the standing problem in `00-Index.md`, and **Lambert's coverage ran out at ch. 08**. So **every implementation here is my own**: `merge`/`merge_sort`, both quicksorts, the instrumented comparison counters, `bucket_sort`, `radix_sort` and `quick_select`. **All were executed and checked against `sorted()`** on the nine inputs of §0 before any timing, and `quick_select` was separately verified against `sorted()[k-1]` at $k=1,2,100,2500,4999,5000$.
>
> **All measurements are my own**: the recursion-depth table, the merge-sort scaling runs, the naive-versus-randomised quicksort timings and ratios, the $\lg(n!)$ table, the comparison counts against the bound, the radix timings, the Timsort input-shape table, the C-versus-Python constant, and the quick-select operation counts.
>
> **All figures are images and are lost** — the merge-sort tree diagrams (Figs. 12.2–12.6), the quicksort execution traces, the in-place partition illustration (Fig. 12.14), and **Fig. 12.15, the decision-tree visualisation of the lower bound.** The last is the significant loss, though [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]] §8 owns that proof and covers it.
>
> **No error was found in Goodrich ch. 12.**
>
> **Additions beyond the source.** **§4's comparison-count experiment is mine** — Goodrich proves the bound and describes the algorithms but never measures how close they come, and "merge-sort is within 2% of the information-theoretic minimum" is a much stronger statement than "merge-sort is $O(n\log n)$". **The verification that $\lg(n!)/(n\lg n)=1-1.4427/\lg n$ to three decimals** is mine. **§7's Timsort table is entirely mine** — Goodrich mentions that Python uses Timsort but gives no data, and the 55× on all-equal input and the sorted-input contrast with quicksort are the chapter's most practically useful numbers. **§8's C-versus-Python measurement and the rule never to hand-write a sort** are additions. **§9's operation-count methodology, and the account in §9 and Exercise 5(c) of my own failed first measurement**, are mine; so is the cross-chapter observation that this is the third such failure. The framing of randomisation as one defence recurring across [[09 - Maps, Hash Tables and Skip Lists|ch. 09]], [[10 - Search Trees|ch. 10]] and this chapter is mine, as is the note on **introsort** and on deterministic **quicksort-killer** attacks against median-of-three.
>
> **Deliberately compressed.** **In-place quicksort is described but not implemented** (§3) — Goodrich's Code Fragment 12.6 is one of the listings destroyed by extraction, and my three-way-partition version demonstrates the algorithm while being far clearer about duplicate handling; the $O(1)$-space claim is therefore **quoted, not verified here.** **Median-of-medians** (deterministic $O(n)$ selection) is mentioned in §9 and Exercise 5(d) but not implemented — its constant makes it a theoretical result in practice. **Goodrich §12.5's full comparison table** is condensed into §10, and **§12.6's tour of `sorted()`'s parameters** (`key`, `reverse`) is assumed known from [[01 - Python and Object-Oriented Foundations|ch. 01]]. **Heap-sort is not re-derived** — it belongs to [[08 - Priority Queues and Heaps|ch. 08]] and appears here only in §10's comparison table. **§15.4's external-memory multiway merge-sort, deferred here from [[10 - Search Trees|ch. 10]], is covered only by the remark in Exercise 1(d) that merge-sort suits data too large for memory**; the block-transfer analysis is in ch. 10 §7.

**Previous:** [[10 - Search Trees]] · **Next:** [[12 - Text Processing and Dynamic Programming]]
