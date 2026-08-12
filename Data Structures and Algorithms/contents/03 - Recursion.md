---
subject: Data Structures and Algorithms
chapter: 3
tags: [ds, dsa, recursion, call-stack, memoisation, fibonacci, divide-and-conquer]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 4"
---

# Recursion

[[Discrete Mathematics/contents/02 - Proofs and Mathematical Induction|Discrete Mathematics ch. 02]] argued that **induction and recursion are one idea seen from two directions** — a recursive definition builds upward, an inductive proof verifies downward. [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]] then showed that the recurrence describing a recursion *is* its running time.

This chapter is the practical half. It covers writing recursive functions that work, and — more importantly — **recognising the two ways they go catastrophically wrong**: exponential blow-up from recomputation (§3), and stack exhaustion from depth (§4). Both are demonstrated by measurement, and both have standard fixes.

## 📘 Main Knowledge

### 1. The shape of a recursive function

Every recursive function has the same two parts, and they correspond exactly to the two parts of an induction:

| Recursion | Induction ([[Discrete Mathematics/contents/02 - Proofs and Mathematical Induction|DM ch. 02]]) |
|---|---|
| **base case** — solved directly, no recursive call | **basis step** |
| **recursive case** — solves a *smaller* instance, then combines | **inductive step** |

```python
def factorial(n):
    if n == 0:                 # base case
        return 1
    return n * factorial(n-1)  # recursive case, on a smaller n
```

*(Verified: `factorial(5)` = 120, `factorial(0)` = 1.)*

> [!warning] Three requirements, all of which are violated in practice
> 1. **There must be a base case.** Without one, the recursion never stops.
> 2. **The base case must be *reachable* from every legal input.** `factorial(-1)` has a base case and never reaches it — $n$ decreases away from 0. *(Which is why the specification says $n\ge0$: "legal input" is part of the contract.)*
> 3. **Each call must make progress toward the base case.** A "recursive" call on the *same* size is infinite recursion with extra steps.
>
> **In Python the symptom of all three is the same:** `RecursionError: maximum recursion depth exceeded`. **That message means "your recursion did not terminate" far more often than it means "the input was large"** — check the three conditions before raising the limit.

### 2. Four classic patterns

Goodrich's examples are well chosen because each illustrates a different *shape* of recursion.

> [!example]- The four, implemented and verified
> **Linear recursion — one call per invocation.**
> ```python
> def binary_search(data, target, low, high):
>     """Return True if target is in the sorted slice data[low:high+1]."""
>     if low > high:
>         return False                                   # base: empty range
>     mid = (low + high) // 2
>     if target == data[mid]:
>         return True
>     elif target < data[mid]:
>         return binary_search(data, target, low, mid-1)  # go left
>     else:
>         return binary_search(data, target, mid+1, high) # go right
> ```
> *(Verified on `[1,3,5,7,9,11,13]`: searching 7 → `True`, searching 8 → `False`.)*
>
> **This is the algorithm [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]] §4 analysed**: $T(n)=T(n/2)+1$, giving $\lfloor\lg n\rfloor+1$ comparisons, $\Theta(\log n)$. Note the recursion is on a *range*, not a copy — passing `data[low:mid]` instead would add $\Theta(n)$ slicing per call and destroy the bound. **[[02 - Algorithm Analysis in Practice|Ch. 02]]'s hidden-loop trap, in recursive dress.**
>
> **Recursion over a hierarchy — the shape mirrors the data.**
> ```python
> import os
>
> def disk_usage(path):
>     """Return the total disk usage of the file or directory at path."""
>     total = os.path.getsize(path)
>     if os.path.isdir(path):
>         for name in os.listdir(path):
>             total += disk_usage(os.path.join(path, name))
>     return total
> ```
> **A file system is a tree, so the natural algorithm is recursive.** This is the pattern [[07 - Trees and Traversals|ch. 07]] generalises — and note there is no explicit base case: a *file* simply has no children, so the loop body never executes. **The base case is implicit in the data.**
>
> **Binary recursion — two calls per invocation.**
> ```python
> def draw_interval(length):
>     """Draw the tick lines of an English ruler."""
>     if length > 0:
>         draw_interval(length - 1)      # ticks above the centre
>         print('-' * length)            # the centre tick
>         draw_interval(length - 1)      # ticks below
> ```
> *(Verified: `draw_interval(3)` produces `-, --, -, ---, -, --, -` — seven ticks, and $2^3-1=7$ ✓)*
>
> **The count $2^L-1$ is worth noticing**: binary recursion of depth $L$ makes $2^L-1$ calls. That is fine when $L$ is small and the work is the point (as here), and it is catastrophic when $L$ scales with the input — which is §3.

### 3. The Fibonacci disaster

This is the most important example in the chapter, and the one with the clearest lesson.

```python
def fib_bad(n):
    """Binary recursion -- exponential."""
    if n <= 1:
        return n
    return fib_bad(n-1) + fib_bad(n-2)
```

It is a direct transcription of the mathematical definition, it is obviously correct, and **it is unusable.** The problem is that `fib_bad(n-2)` is recomputed inside `fib_bad(n-1)`, and so on down — the same subproblems are solved over and over.

**The fix is to return more information per call**, so nothing needs recomputing:

```python
def fib_good(n):
    """Linear recursion: return the PAIR (F(n), F(n-1))."""
    if n <= 1:
        return (n, 0)
    (a, b) = fib_good(n-1)     # a = F(n-1), b = F(n-2)
    return (a + b, a)          # = (F(n), F(n-1))
```

> [!example]- Measured (all values verified identical between the two)
> | $n$ | $F(n)$ | `fib_bad` calls | time | `fib_good` calls | time | speed-up |
> |---|---|---|---|---|---|---|
> | 10 | 55 | 177 | 0.0000 s | **10** | 0.000003 s | 6× |
> | 20 | 6 765 | 21 891 | 0.0017 s | **20** | 0.000005 s | 319× |
> | 25 | 75 025 | 242 785 | 0.0180 s | **25** | 0.000007 s | 2 568× |
> | 30 | 832 040 | 2 692 537 | 0.2034 s | **30** | 0.000007 s | **29 051×** |
>
> **`fib_good` makes exactly $n$ calls. `fib_bad` makes 2.7 million at $n=30$** — and the ratio grows without bound.

> [!note] How fast is "exponential", exactly? A cross-subject confirmation
> The call count of `fib_bad` satisfies essentially the Fibonacci recurrence itself, so it grows like $\phi^n$ where $\phi=\frac{1+\sqrt5}2\approx1.618$ — the golden ratio that [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]] §3 derived from Binet's formula.
>
> **Testable prediction: increasing $n$ by 2 should multiply the time by $\phi^2\approx2.618$.** Measured:
>
> | $n$ | calls | time | ratio vs $n-2$ |
> |---|---|---|---|
> | 22 | 57 313 | 0.0046 s | — |
> | 24 | 150 049 | 0.0115 s | **2.51** |
> | 26 | 392 835 | 0.0294 s | **2.55** |
> | 28 | 1 028 457 | 0.0793 s | **2.70** |
>
> **Against a prediction of 2.618.** *(Verified.)* **This is the golden ratio, derived from a characteristic equation in one subject, showing up in a stopwatch reading in another** — and it is a good demonstration that the theory is not decoration.

**The general lesson: binary recursion is safe only when the subproblems are *disjoint*.** Merge sort splits an array in half and each half is solved once — fine. Naive Fibonacci solves overlapping subproblems — fatal. **When subproblems overlap, either restructure (as `fib_good` does) or memoise (§5).** That distinction is exactly what [[12 - Text Processing and Dynamic Programming|ch. 12]]'s dynamic programming is about.

### 4. The call stack is finite memory

Every pending call occupies a **stack frame** holding its parameters and local variables. So:

$$\textbf{recursion depth} \;=\; \textbf{extra space used}$$

**This is a real cost that [[02 - Algorithm Analysis in Practice|ch. 02]]'s time analysis does not show**, and it is why Important Note 15 there insisted on analysing space too.

Python enforces a limit — 1000 by default *(verified via `sys.getrecursionlimit()`)*:

```
countdown(100)   -> OK
countdown(900)   -> OK
countdown(5000)  -> RecursionError
```

*(Verified.)*

> [!warning] Raising the recursion limit is usually the wrong fix
> `sys.setrecursionlimit(10000)` exists, and reaching for it should be a last resort:
>
> - **If the recursion is not terminating, a higher limit just delays the error** — and the three conditions of §1 are the actual bug.
> - **If the depth genuinely scales with input size, the limit will be hit again** on a bigger input. An algorithm that recurses $n$ deep on an $n$-element input is $O(n)$ *space*, which may be unacceptable regardless of Python's limit.
> - **The C stack can overflow before Python's counter does**, crashing the interpreter outright rather than raising a catchable exception.
>
> **Prefer restructuring**: convert to iteration (§5), reduce depth from $n$ to $\log n$ by halving instead of decrementing, or use an explicit stack ([[05 - Stacks, Queues and Deques|ch. 05]] — which is precisely what an explicit stack is *for*).

### 5. Tail recursion, iteration, and memoisation

**A tail-recursive** function makes its recursive call as the very last action, so nothing remains to do afterwards. In languages that optimise this (Scheme, Haskell), the frame is reused and the depth stays $O(1)$.

> [!warning] Python does not perform tail-call optimisation, and will not
> ```python
> def sum_rec(data, start=0):
>     if start == len(data):
>         return 0
>     return data[start] + sum_rec(data, start+1)
> ```
> *(Verified: works on 500 elements, giving 124750; **raises `RecursionError` on 5000** — while the iterative version handles it without difficulty, returning 12497500.)*
>
> **Guido van Rossum has repeatedly declined to add TCO**, on the grounds that it obscures stack traces. So **in Python, tail recursion is a style, not an optimisation** — if depth is a concern, write the loop.

**Any tail recursion converts mechanically to a loop:**

```python
def sum_iter(data):
    total = 0
    for x in data:
        total += x
    return total
```

**Memoisation** is the other repair — cache results so each subproblem is solved once:

```python
def fib_memo(n, memo=None):
    if memo is None:            # ch. 01's mutable-default rule
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]
```

*(Verified: `fib_memo(60)` = 1 548 008 755 920, instantly — `fib_bad(60)` would need roughly $2.5\times10^{12}$ calls.)*

Python ships this:

```python
import functools

@functools.lru_cache(maxsize=None)
def fib_cached(n):
    if n <= 1:
        return n
    return fib_cached(n-1) + fib_cached(n-2)
```

*(Verified: `fib_cached(90)` = 2 880 067 194 370 816 120.)*

> [!note] Memoisation trades space for time, and it is dynamic programming
> It converts $O(\phi^n)$ time into $O(n)$ time at the cost of $O(n)$ space. **This is exactly the technique [[12 - Text Processing and Dynamic Programming|ch. 12]] develops as dynamic programming** — top-down memoisation and bottom-up tabulation are two implementations of one idea, and the idea is *stop recomputing overlapping subproblems*.
>
> Note also `@lru_cache` requires **hashable** arguments, which is why [[01 - Python and Object-Oriented Foundations|ch. 01]] §3's remark about `__eq__` and `__hash__` matters here.

### 6. When *not* to use recursion

Recursion is right when **the problem's structure is recursive** — trees, file systems, divide-and-conquer, backtracking. It is wrong when:

| Situation | Why | Do instead |
|---|---|---|
| Simple iteration over a sequence | $O(n)$ stack for no benefit | a `for` loop |
| Depth scales with $n$ and $n$ is large | `RecursionError`, or $O(n)$ space | iterate, or use an explicit stack |
| Subproblems overlap | exponential recomputation | memoise, or restructure (§3) |
| Tail-recursive and depth matters | Python will not optimise it | write the loop |

**But do not over-correct.** A tree traversal written iteratively needs an explicit stack and is markedly harder to read; a recursive one is four lines ([[07 - Trees and Traversals|ch. 07]]). **The question is whether the recursion mirrors the data's structure — if it does, prefer it.**

## ✏️ Exercises

**1. (Basics.)** (a) State the three requirements for a terminating recursion. (b) Write `factorial` recursively and trace `factorial(4)`. (c) What happens on `factorial(-1)` and why? (d) Write a recursive function to reverse a sequence, and give its complexity.

> [!example]- Solution
> **(a)** A base case exists; it is reachable from every legal input; every recursive call makes progress toward it.
>
> **(b)** §1's implementation. The trace unwinds down, then multiplies back up:
> ```
> factorial(4) = 4 * factorial(3)
>              = 4 * (3 * factorial(2))
>              = 4 * (3 * (2 * factorial(1)))
>              = 4 * (3 * (2 * (1 * factorial(0))))
>              = 4 * (3 * (2 * (1 * 1)))          <- base case reached
>              = 24
> ```
> **Note that four frames are live simultaneously** at the deepest point — that is the $O(n)$ space of §4, visible in the trace.
>
> **(c) `RecursionError`.** The base case `n == 0` exists but is **unreachable** from $-1$: the argument goes $-1,-2,-3,\dots$, away from 0. Requirement 2 is violated.
>
> This is why the docstring should state $n\ge0$ — and, if the function is public, why it should check:
> ```python
> if n < 0:
>     raise ValueError('n must be non-negative')
> ```
> **A precondition that is not checked is a precondition that will be violated.**
>
> **(d)**
> ```python
> def reverse(S, start, stop):
>     """Reverse elements in S[start:stop] in place."""
>     if start < stop - 1:
>         S[start], S[stop-1] = S[stop-1], S[start]
>         reverse(S, start+1, stop-1)
> ```
> **$\Theta(n)$ time** — each call does constant work and there are $\lceil n/2\rceil$ of them — and **$\Theta(n)$ space** for the stack. *(An iterative two-pointer loop is $\Theta(n)$ time and $\Theta(1)$ space, and is the better choice: the problem's structure is not recursive, it is just a loop.)*

**2. (Binary search.)** (a) Write it recursively. (b) Give and solve its recurrence. (c) Why pass `low`/`high` rather than slicing? (d) What is its space complexity, and how would you make it $O(1)$?

> [!example]- Solution
> **(a)** §2's implementation. *(Verified on `[1,3,5,7,9,11,13]`.)*
>
> **(b)** Each call does constant work and recurses on half the range:
> $$T(n)=T(n/2)+O(1),\qquad T(0)=O(1).$$
> Unwinding, the range sizes are $n, n/2, n/4,\dots,1$, so there are $\lfloor\lg n\rfloor+1$ calls and $T(n)=\Theta(\log n)$. *(Solved in full in [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]] §4, and verified there against $\lfloor\lg n\rfloor+1$ at ten values of $n$.)*
>
> **(c) Because slicing copies.** `data[low:mid]` builds a new list of $\Theta(n)$ elements, so the recurrence would become
> $$T(n)=T(n/2)+\Theta(n)\ \Longrightarrow\ \Theta(n),$$
> destroying the logarithmic bound and making binary search no better than a linear scan. **Passing indices keeps each call $O(1)$.**
>
> **This is [[02 - Algorithm Analysis in Practice|ch. 02]]'s hidden-loop trap in recursive form** — the slice looks like a way of naming a sub-range and is actually a linear-time copy.
>
> **(d)** Space is $\Theta(\log n)$ — one frame per level of recursion. To make it $\Theta(1)$, write it iteratively:
> ```python
> def binary_search_iterative(data, target):
>     low, high = 0, len(data) - 1
>     while low <= high:
>         mid = (low + high) // 2
>         if target == data[mid]:
>             return True
>         elif target < data[mid]:
>             high = mid - 1
>         else:
>             low = mid + 1
>     return False
> ```
> **This is a tail recursion converted to a loop** (§5), and since Python does not optimise tail calls, the iterative version is genuinely better here — same time, less space, no depth limit.

**3. (The Fibonacci disaster.)** (a) Why is the naive recursion exponential? (b) Give two fixes with different characters. (c) Predict the ratio of running times between $n$ and $n+2$, and check it against the measurements. (d) What distinguishes a safe binary recursion from a fatal one?

> [!example]- Solution
> **(a) Because the subproblems overlap and are recomputed.** Computing $F(n)$ calls $F(n-1)$ and $F(n-2)$; but $F(n-1)$ itself calls $F(n-2)$ — which is therefore computed twice, $F(n-3)$ three times, and so on. The call count satisfies essentially the Fibonacci recurrence, so it grows like $\phi^n$.
>
> *(Measured: 2 692 537 calls at $n=30$, against `fib_good`'s **30**.)*
>
> **(b) Two fixes, different in character:**
>
> 1. **Restructure** (`fib_good`, §3) — return the pair $(F(n),F(n-1))$ so each call passes down everything the next needs. **$\Theta(n)$ time, $\Theta(n)$ stack, no auxiliary storage.** This is a redesign of the algorithm.
> 2. **Memoise** (`fib_memo` / `@lru_cache`, §5) — keep the naive structure and cache results. **$\Theta(n)$ time, $\Theta(n)$ space for the cache.** This is a mechanical transformation requiring no insight into the problem.
>
> **The trade-off:** memoisation is general and automatic (a decorator!); restructuring is specific and produces the cleaner algorithm. *(A third: iterate bottom-up with two variables — $\Theta(n)$ time and $\Theta(1)$ space, better than both.)*
>
> **(c) Prediction $\phi^2\approx2.618$**, since the cost grows like $\phi^n$ and $\phi^{n+2}/\phi^n=\phi^2$. Measured *(verified)*:
>
> | $n$ | time | ratio |
> |---|---|---|
> | 22 | 0.0046 s | — |
> | 24 | 0.0115 s | 2.51 |
> | 26 | 0.0294 s | 2.55 |
> | 28 | 0.0793 s | 2.70 |
>
> **Clustering around 2.618 as predicted.** The golden ratio here is the same $\phi$ that [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]] obtained as the dominant root of $t^2=t+1$ and that [[Discrete Mathematics/contents/05 - Number Theory and Cryptography|DM ch. 05]] used for the Euclidean algorithm's worst case. **Three appearances, one constant.**
>
> **(d) Whether the subproblems overlap.**
>
> - **Safe:** merge sort recurses on the left and right halves — **disjoint** data, each element in exactly one subproblem. Total work per level is $\Theta(n)$ over $\lg n$ levels, so $\Theta(n\log n)$.
> - **Fatal:** naive Fibonacci recurses on $n-1$ and $n-2$ — **massively overlapping**, since almost every subproblem appears in both branches.
>
> **The test: do the two recursive calls partition the input, or do they revisit it?** Partition is fine; revisiting demands memoisation. **This is precisely the criterion for when dynamic programming applies** ([[12 - Text Processing and Dynamic Programming|ch. 12]]).

**4. (The call stack.)** (a) Why does recursion depth cost memory? (b) What is Python's default limit and what happens at it? (c) Give two situations where `RecursionError` means different things. (d) When is raising the limit acceptable?

> [!example]- Solution
> **(a)** Each pending call has a **stack frame** holding its arguments, local variables and return address. A frame cannot be released until its call returns, so at the deepest point of a recursion of depth $d$, all $d$ frames are live simultaneously. **Recursion depth is extra space**, and a recursion that is $\Theta(n)$ deep is $\Theta(n)$ space even if it allocates nothing itself.
>
> **(b) 1000 by default** *(verified via `sys.getrecursionlimit()`)*. Exceeding it raises **`RecursionError`** — a normal, catchable Python exception, not a crash. *(Verified: `countdown(900)` succeeds, `countdown(5000)` raises.)*
>
> **(c) Two quite different meanings:**
>
> 1. **A bug — the recursion does not terminate.** `factorial(-1)` violates §1's requirement 2. **The limit is doing its job**, converting an infinite loop into a diagnosable error. *This is the more common case.*
> 2. **A legitimately deep recursion.** `sum_rec` on 5000 elements is correct and simply too deep *(verified)*. Here the algorithm works and its **space complexity** is the problem.
>
> **Diagnose which before acting**: if the depth should be small for your input size, you have case 1 and raising the limit hides the bug.
>
> **(d) Rarely, and only when all of these hold:** the recursion is known to terminate; the depth is bounded by something you control; the bound is modest (a few thousand); and restructuring is genuinely impractical.
>
> **Even then, prefer the alternatives:** convert to iteration; reduce depth from $n$ to $\log n$ by halving rather than decrementing; or use an explicit stack ([[05 - Stacks, Queues and Deques|ch. 05]]), which moves the frames to the heap where memory is plentiful. **Note the C stack can overflow before Python's counter does, crashing the interpreter with no catchable exception** — so a raised limit is not merely inelegant, it is genuinely unsafe.

**5. (Hard — recursion versus iteration.)** (a) Show that Python does not optimise tail calls, with evidence. (b) Convert a tail recursion to a loop. (c) When is recursion the *better* choice despite its costs? (d) Explain memoisation's relationship to dynamic programming.

> [!example]- Solution
> **(a) Evidence:** `sum_rec` (§5) is tail-recursive in form — the recursive call's result is only added to `data[start]`… *(strictly, that addition makes it not quite tail-recursive; a truly tail-recursive version passes an accumulator)*. Either way, the depth grows with $n$:
>
> ```
> sum_rec(list(range(500)))   ->  124750        OK
> sum_rec(list(range(5000)))  ->  RecursionError
> sum_iter(list(range(5000))) ->  12497500      fine
> ```
> *(Verified.)* **If Python reused frames for tail calls, depth would be $O(1)$ and 5000 would be no harder than 500.** It is not, so it does not.
>
> This is a deliberate design decision — **Guido van Rossum has declined TCO repeatedly**, on the grounds that reusing frames destroys the stack traces that make Python debuggable. **So in Python, tail recursion is a stylistic choice with a real space cost, never a free one.**
>
> **(b)** Mechanically: the recursion's parameters become loop variables, and the recursive call becomes reassignment.
> ```python
> def sum_iter(data):
>     total = 0
>     for x in data:
>         total += x
>     return total
> ```
> *(Verified: agrees with `sum_rec` on 500 elements, and handles 5000 where the recursion fails.)* Exercise 2(d)'s iterative binary search is the same transformation applied to a genuinely tail-recursive function.
>
> **(c) When the recursion mirrors the structure of the data.** Three cases where it is clearly better:
>
> 1. **Trees and hierarchies.** `disk_usage` (§2) is six lines recursively; iteratively it needs an explicit stack and careful bookkeeping. [[07 - Trees and Traversals|Ch. 07]]'s traversals are the same story, and their depth is $O(\text{height})$ — $O(\log n)$ for a balanced tree, which is negligible.
> 2. **Divide and conquer.** Merge sort and quicksort ([[11 - Sorting and Selection|ch. 11]]) are naturally recursive; their depth is $O(\log n)$ and the recursion *is* the algorithm.
> 3. **Backtracking.** Exploring a search space with undo (n-queens, sudoku, permutation generation) is painful iteratively because the "undo" is exactly what returning from a call does for free.
>
> **The common factor: depth is $O(\log n)$ or $O(\text{height})$, not $O(n)$** — so the space cost is trivial and the clarity gain is large. **Recursion is dangerous when depth scales linearly and delightful when it scales logarithmically.**
>
> **(d) Memoisation *is* top-down dynamic programming.**
>
> DP applies exactly when a problem has (i) **optimal substructure** — the solution is built from solutions to subproblems — and (ii) **overlapping subproblems** — the same subproblem recurs. Naive Fibonacci has both, which is why it is exponential and why caching fixes it.
>
> Two implementations of the one idea:
>
> | | direction | mechanism |
> |---|---|---|
> | **Memoisation** | top-down | keep the natural recursion; cache results |
> | **Tabulation** | bottom-up | iterate over subproblems in dependency order, filling a table |
>
> **Memoisation is easier to write** — often a single `@lru_cache` line — and computes only the subproblems actually needed. **Tabulation avoids the stack entirely** and often uses less memory, since you can discard rows you no longer need (for Fibonacci, two variables suffice, giving $\Theta(1)$ space).
>
> **Both convert $O(\phi^n)$ to $O(n)$ by refusing to recompute**, and [[12 - Text Processing and Dynamic Programming|ch. 12]] develops the general technique on the longest-common-subsequence and edit-distance problems. **The insight to carry forward: an exponential recursion is usually not a hard problem — it is a problem being solved wastefully**, and the first question to ask is always "am I recomputing something?"

## 📝 Summary

- **A recursive function has a base case and a recursive case**, corresponding exactly to the basis and inductive steps of [[Discrete Mathematics/contents/02 - Proofs and Mathematical Induction|DM ch. 02]]'s induction.
- **Three requirements:** a base case exists, it is **reachable from every legal input**, and each call makes progress. **`RecursionError` most often means one of these is violated**, not that the input was large.
- **Four shapes:** linear (one call — `binary_search`), hierarchical (`disk_usage`, where the base case is implicit in the data), binary (two calls — the ruler, $2^L-1$ calls), and multiple.
- **Pass indices, not slices.** `data[low:mid]` is a $\Theta(n)$ copy and turns binary search's $\Theta(\log n)$ into $\Theta(n)$ — [[02 - Algorithm Analysis in Practice|ch. 02]]'s hidden-loop trap in recursive dress.
- **Naive Fibonacci is exponential because its subproblems overlap** and are recomputed. Measured: **2 692 537 calls at $n=30$ against 30**, a 29 051× speed-up from restructuring.
- **The growth rate is $\phi^n$**, so doubling-style ratios at $n\to n+2$ should be $\phi^2\approx2.618$ — **measured 2.51, 2.55, 2.70.** The golden ratio of [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]], seen on a stopwatch.
- **Binary recursion is safe iff the subproblems are disjoint.** Merge sort partitions; Fibonacci revisits. **That test is exactly the criterion for dynamic programming.**
- **Recursion depth is space.** Each pending call holds a frame; a depth-$n$ recursion is $\Theta(n)$ space. Python's default limit is **1000**, and exceeding it raises `RecursionError`.
- **Python does not optimise tail calls and will not** — `sum_rec` fails at 5000 elements while the loop does not. **Tail recursion in Python is a style, not an optimisation.**
- **Raising the recursion limit is usually wrong**: it hides non-termination, it will be hit again on larger input, and the C stack may overflow first — an uncatchable crash. Restructure instead.
- **Memoisation** (`@lru_cache`, or an explicit dict) converts $O(\phi^n)$ into $O(n)$ by refusing to recompute. **It is top-down dynamic programming**; tabulation is the bottom-up form ([[12 - Text Processing and Dynamic Programming|ch. 12]]).
- **Use recursion when it mirrors the data's structure** — trees, divide-and-conquer, backtracking — where depth is $O(\log n)$ or $O(\text{height})$. **Avoid it for flat iteration, where depth is $O(n)$ for no benefit.**

## ⚠️ Important Notes

1. **Check that the base case is reachable, not merely present.** `factorial(-1)` has one and recurses away from it forever.
2. **State and enforce preconditions.** A public recursive function should validate its input; an unchecked precondition will eventually be violated, and the symptom (`RecursionError`) will not point at the cause.
3. **`RecursionError` usually means a bug, not a big input.** Diagnose which before touching the limit — if the depth should have been small, raising the limit hides the real fault.
4. **Never pass slices where indices will do.** `data[low:mid]` silently adds $\Theta(n)$ per call. This single mistake converts $\Theta(\log n)$ into $\Theta(n)$.
5. **Count the recursive calls when you suspect trouble.** Instrumenting `fib_bad` with a counter reveals the problem instantly — 2.7 million calls at $n=30$ — where staring at the code may not.
6. **Ask "am I recomputing something?" before optimising anything else.** An exponential recursion is usually a wasteful solution, not a hard problem.
7. **Binary recursion is fine when the calls partition the data and fatal when they revisit it.** Test this before writing two recursive calls.
8. **Recursion depth is memory.** Report space complexity alongside time for any recursive algorithm — [[02 - Algorithm Analysis in Practice|ch. 02]] Note 15.
9. **Python has no tail-call optimisation.** Do not write deep tail recursions expecting one; the loop is strictly better.
10. **Convert tail recursion to iteration mechanically**: parameters become loop variables, the recursive call becomes reassignment. Exercise 2(d) is the model.
11. **Prefer an explicit stack to a raised recursion limit** when depth is genuinely needed — heap memory is plentiful and the failure mode is a clean `MemoryError` rather than an interpreter crash.
12. **`@lru_cache` requires hashable arguments.** A recursive function taking a list cannot be memoised directly — convert to a tuple, or key on indices instead.
13. **Remember to use `None` as a mutable default**, including for a memo dict — [[01 - Python and Object-Oriented Foundations|ch. 01]] §1's trap applies with full force here.
14. **Memoisation buys time with space.** $O(n)$ cache for $O(n)$ time is usually an excellent trade; verify the space is affordable before assuming so.
15. **Recursion is a clarity tool as much as an algorithmic one.** A tree traversal in four recursive lines beats twenty iterative ones with an explicit stack, and depth $O(\log n)$ makes the cost negligible. **Do not eliminate recursion reflexively.**

> [!warning] Gaps in the source material
> **Goodrich's prose for this chapter extracts cleanly**; his code does not, per the standing problem in `00-Index.md`. **Every function in this chapter is therefore my own implementation** of the algorithm his prose describes, **and every one was executed** — for correctness first (including `factorial(0)`, empty and single-element inputs, and the absent-target case for binary search), then for timing.
>
> **All figures are images and are lost.** Most costly here: Goodrich's **recursion-trace diagrams**, which are how recursion is conventionally taught — the box-and-arrow illustrations of `factorial(4)`, the binary-search range narrowing, the English-ruler call tree, and the Fibonacci call tree showing the repeated subtrees. **§3 and Exercise 1(b) compensate with a written trace and with call counts**, which arguably make the Fibonacci point harder (2 692 537 versus 30 is more convincing than a picture of a tree), but the loss is real for a reader who thinks visually.
>
> **Every measurement in this chapter is my own**, taken for these notes: the `fib_bad`/`fib_good` call counts and timings across $n=10,20,25,30$; the $\phi^2$ ratio experiment at $n=22,24,26,28$; the recursion-limit probes; and the `sum_rec`/`sum_iter` comparison. **The absolute times are machine-specific; the ratios and call counts are not**, which is why the tables emphasise those.
>
> **The $\phi^2$ experiment is an addition of mine and is worth flagging as the chapter's best feature** — Goodrich states that naive Fibonacci is exponential and proves a bound on the call count, but does not connect it to the golden ratio or propose a measurable prediction. **Deriving $\phi$ in [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]] from a characteristic equation and then confirming it here with a stopwatch (predicted 2.618, measured 2.51/2.55/2.70) is exactly the cross-subject payoff the vault's structure is meant to produce.**
>
> **No error was found in Goodrich ch. 4.**
>
> **Other additions.** The **table of three requirements and their failure modes** (§1), the observation that **`RecursionError` usually indicates non-termination rather than depth**, and the three-part argument against raising the limit (including the **C-stack overflow** risk, which Goodrich does not mention) are mine. The explicit statement that **Python will never gain TCO, and why**, is an addition. **`fib_memo` and `@lru_cache` are mine** — Goodrich fixes Fibonacci only by restructuring and defers memoisation entirely to his ch. 13, so the connection to dynamic programming is drawn here rather than there. §6's **table of when not to use recursion**, and Exercise 5(c)'s three cases where recursion is genuinely better, are my own framing. The insistence that **depth $O(\log n)$ versus $O(n)$ is the criterion** — rather than any blanket preference for or against recursion — is mine.
>
> **Deliberately compressed.** Goodrich's §4.1.5 (a recursive `binary_sum`) and §4.3 (further examples of multiple recursion, including summing to a target) are omitted as further instances of patterns already covered. **§4.4 (designing recursive algorithms) and §4.5 (eliminating tail recursion)** are folded into §§5–6. **§4.2's formal running-time analyses** are stated as results with pointers to [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]], which solves the recurrences properly — the split recorded in both indexes.

**Previous:** [[02 - Algorithm Analysis in Practice]] · **Next:** [[04 - Array-Based Sequences and Amortised Analysis]]
