---
subject: Data Structures and Algorithms
chapter: 2
tags: [ds, dsa, algorithm-analysis, big-o, complexity, benchmarking, seven-functions]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 3; Lambert, *Fundamentals of Python: Data Structures*, ch. 3"
---

# Algorithm Analysis in Practice

[[Discrete Mathematics/contents/04 - Algorithms and Their Analysis|Discrete Mathematics ch. 04]] defined $O$, $\Omega$ and $\Theta$, proved the polynomial and logarithm rules, and established that the quantifier order $\exists C\,\forall n$ is the whole content of the definition. **None of that is repeated here.**

What this chapter does instead is the half Discrete Maths cannot: **apply the notation to real code, and then measure whether the prediction is true.** That second step is what makes this a Data Structures chapter rather than a mathematics one, and it is the discipline the whole subject runs on — *a complexity claim you have not measured is a guess.*

## 📘 Main Knowledge

### 1. Two ways to analyse, and why neither suffices alone

**Experimental analysis** means running the code and timing it. It is indispensable and it has three serious limitations, which Goodrich states plainly:

1. **Comparisons are only valid on identical hardware and software.** A timing on your laptop says nothing about a server.
2. **You can only test the inputs you actually run.** The worst case may be an input you did not think of.
3. **The algorithm must be fully implemented** before you can time it — which is far too late to discover you chose the wrong approach.

**Theoretical analysis** fixes all three: it covers all inputs, needs no implementation, and is machine-independent. It does so by counting **primitive operations** — assignments, arithmetic, comparisons, indexing, function calls — each assumed to take constant time.

> [!warning] The assumption "each primitive operation is constant time" is a model, and it leaks
> It is a very good model and it is not the truth. Three places it fails, all of which show up in later chapters:
> - **Python's `list` indexing is $O(1)$ but `list.insert(0, x)` is $O(n)$** — both look like single operations in the source ([[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]).
> - **Memory locality is invisible to the model.** Two $O(n)$ traversals can differ severalfold because one walks contiguous memory and the other chases pointers ([[06 - Linked Lists|ch. 06]]).
> - **`sum(S[0:j+1])` looks like one operation and is $\Theta(j)$** — §3's second prefix-average function is built entirely on this trap.
>
> **This is why the two methods are complements, not alternatives.** Theory tells you the growth rate; measurement tells you whether your model of "one operation" was honest.

### 2. The seven functions

Goodrich's claim is that almost all algorithm analysis uses just seven functions. In practice it is true.

| Function | Name | Typical source |
|---|---|---|
| $1$ | **constant** | arithmetic; array indexing; a hash lookup |
| $\log n$ | **logarithmic** | halving the problem — binary search, balanced-tree descent |
| $n$ | **linear** | one pass over the input |
| $n\log n$ | **linearithmic** | sorting; divide-and-conquer with linear combine |
| $n^2$ | **quadratic** | nested loops over the input |
| $n^3$ | **cubic** | triple-nested loops; naive matrix multiplication |
| $2^n$ | **exponential** | trying every subset |

$$1\ \prec\ \log n\ \prec\ n\ \prec\ n\log n\ \prec\ n^2\ \prec\ n^3\ \prec\ 2^n$$

**The base of the logarithm never matters** ($\log_b n=\Theta(\log_a n)$ — [[Discrete Mathematics/contents/04 - Algorithms and Their Analysis|DM ch. 04]] §3), so one writes $\log n$; in this subject it is base 2 unless stated. **The base of an exponent always matters.**

> [!note] The gap that decides whether a program finishes
> Between $n\log n$ and $n^2$. At $n=10^6$: about $2\times10^7$ operations versus $10^{12}$ — seconds versus days. **This is why [[11 - Sorting and Selection|ch. 11]] cares so much about which sorts are $n\log n$**, and why [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]'s proof that you cannot beat $n\log n$ by comparisons was worth the effort.

### 3. Analysing real code

The skill is reading a loop nest and seeing the growth rate. Goodrich's running examples are the best available, so here they are — with **measurements**.

> [!example]- Prefix averages: three implementations, and the one that lies (all verified)
> Compute $A[j]=\frac{1}{j+1}\sum_{i=0}^{j}S[i]$.
>
> ```python
> def prefix_average1(S):
>     """O(n^2): recompute each sum from scratch."""
>     n = len(S); A = [0]*n
>     for j in range(n):
>         total = 0
>         for i in range(j+1):
>             total += S[i]
>         A[j] = total/(j+1)
>     return A
>
> def prefix_average2(S):
>     """O(n^2): LOOKS better -- sum() hides the inner loop."""
>     n = len(S); A = [0]*n
>     for j in range(n):
>         A[j] = sum(S[0:j+1])/(j+1)
>     return A
>
> def prefix_average3(S):
>     """O(n): keep a running total."""
>     n = len(S); A = [0]*n
>     total = 0
>     for j in range(n):
>         total += S[j]
>         A[j] = total/(j+1)
>     return A
> ```
>
> *(All three verified to agree on `[]`, `[5]`, `[1,2,3,4]` and `[2,2,2]`.)*
>
> **The analysis.** The first is $\sum_{j=0}^{n-1}(j+1)=\frac{n(n+1)}2=\Theta(n^2)$ — the same sum as [[Discrete Mathematics/contents/02 - Proofs and Mathematical Induction|DM ch. 02]]'s first induction.
>
> **The second is the interesting one.** It has *one* visible loop and is still quadratic, because `S[0:j+1]` builds a slice of length $j+1$ and `sum` traverses it. **Two $\Theta(j)$ operations hide inside what looks like a single statement.** Reading it as $O(n)$ is the single commonest analysis error in Python, and it is entirely a failure of the "one operation" model of §1.
>
> The third keeps a running total: one pass, constant work each, $\Theta(n)$.
>
> **Measured** *(doubling $n$; $O(n)$ predicts a time ratio of 2, $O(n^2)$ predicts 4)*:
>
> | $n$ | `prefix_average1` | ratio | | $n$ | `prefix_average3` | ratio |
> |---|---|---|---|---|---|---|
> | 500 | 0.00273 s | — | | 500 | 0.000027 s | — |
> | 1000 | 0.01142 s | **4.18** | | 1000 | 0.000056 s | **2.10** |
> | 2000 | 0.04762 s | **4.17** | | 2000 | 0.000112 s | **2.01** |
> | 4000 | 0.18639 s | **3.91** | | 4000 | 0.000232 s | **2.07** |
> | | | | | 8000 | 0.000458 s | **1.98** |
>
> **The ratios are 4 and 2 to within measurement noise.** That is what a confirmed complexity claim looks like, and it takes about ten lines of code to obtain.

> [!example]- Element uniqueness: $n^2$ vs $n\log n$ vs $n$ (verified)
> ```python
> def unique1(S):                      # O(n^2): compare all pairs
>     for j in range(len(S)):
>         for k in range(j+1, len(S)):
>             if S[j] == S[k]: return False
>     return True
>
> def unique2(S):                      # O(n log n): sort, then check neighbours
>     temp = sorted(S)
>     for j in range(1, len(temp)):
>         if temp[j-1] == temp[j]: return False
>     return True
>
> def unique3(S):                      # O(n) expected: hash set
>     return len(set(S)) == len(S)
> ```
>
> *(All three verified to agree on `[]`, `[1]`, `[1,2,3]`, `[1,2,2]`. Timed on all-distinct input — the worst case, since any duplicate lets `unique1` exit early.)*
>
> | | $n=1000$ | $n=2000$ | $n=4000$ |
> |---|---|---|---|
> | `unique1` $O(n^2)$ | 0.014560 s | 0.058700 s (×4.03) | 0.221111 s (×3.77) |
> | `unique2` $O(n\log n)$ | 0.000059 s | 0.000128 s (×2.17) | 0.000371 s (×2.90) |
> | `unique3` $O(n)$ expected | 0.000011 s | 0.000022 s (×2.09) | 0.000042 s (×1.87) |
>
> **Three things to read off this table.**
> 1. **The ratios identify the classes:** ≈4 for quadratic, a little over 2 for $n\log n$, ≈2 for linear.
> 2. **At $n=4000$, `unique1` is about 5,300× slower than `unique3`** ($0.221$ s versus $0.000042$ s) — and the gap *widens* with $n$. **No amount of micro-optimising `unique1` closes that**; only changing the algorithm does.
> 3. **`unique2` sorts and is nearly as fast as hashing**, which is worth remembering: sorting is a cheap way to buy structure ([[11 - Sorting and Selection|ch. 11]]), and it preserves ordering that `set` throws away.

> [!example]- Three-way disjointness: $n^3$ vs $n^2$ from one moved loop (verified)
> ```python
> def disjoint1(A, B, C):              # O(n^3)
>     for a in A:
>         for b in B:
>             for c in C:
>                 if a == b == c: return False
>     return True
>
> def disjoint2(A, B, C):              # O(n^2): only look at C when a == b
>     for a in A:
>         for b in B:
>             if a == b:
>                 for c in C:
>                     if a == c: return False
>     return True
> ```
>
> | | $n=30$ | $n=60$ | $n=120$ |
> |---|---|---|---|
> | `disjoint1` $O(n^3)$ | 0.00060 s | 0.00446 s (**×7.42**) | 0.03725 s (**×8.34**) |
> | `disjoint2` $O(n^2)$ | 0.00002 s | 0.00006 s (×3.56) | 0.00022 s (×3.91) |
>
> **Ratios of ≈8 and ≈4 — exactly $2^3$ and $2^2$.** *(Verified.)*
>
> **Why `disjoint2` is quadratic** deserves care, because the innermost loop is still there. The point is that it *only runs when $a=b$*. Since the elements of $A$ are distinct, each $a$ matches at most one $b$, so the inner loop over $C$ executes at most $n$ times in total — contributing $O(n^2)$ overall, not $O(n^3)$. **The loop nesting depth is an upper bound on the exponent, not the exponent itself**, and reading depth-3 nesting as automatically cubic is a common over-estimate.

### 4. What the model cannot tell you

Asymptotic analysis deliberately discards constant factors. Usually that is right; sometimes it is exactly the information you need.

*Measured, both $O(n)$ at $n=2{,}000{,}000$:*

| | time |
|---|---|
| `for i in range(n): out.append(i*i)` | 0.1244 s |
| `[i*i for i in range(n)]` | 0.1099 s |

**About 13% — real, reproducible, and modest.** Set that beside the 5,300× gap between `unique1` and `unique3` at $n=4000$ and the priority is clear:

> [!note] The rule this establishes
> **Fix the asymptotic class first; tune constants second, and only if measurement says they matter.** A 13% constant-factor win is worth having once the algorithm is right, and worth nothing at all while you are still running an $O(n^2)$ method where an $O(n)$ one exists.
>
> **But do not over-learn it.** [[Discrete Mathematics/contents/04 - Algorithms and Their Analysis|DM ch. 04]]'s Important Note 8 makes the converse point: asymptotics say nothing about small $n$, which is why real library sorts switch to insertion sort below a threshold ([[11 - Sorting and Selection|ch. 11]]). **Constants decide small inputs; growth rates decide large ones.** Knowing which regime you are in is the actual skill.

**Three further blind spots**, each cashed out later:

- **Memory locality.** Arrays are contiguous; linked lists are not. Two $O(n)$ traversals can differ by a large constant purely from cache behaviour ([[06 - Linked Lists|ch. 06]]). *This is the one part of Goodrich's excluded memory-management chapter that has direct algorithmic consequence.*
- **Expected versus worst case.** `unique3` is $O(n)$ *expected* and $O(n^2)$ worst case, because hashing can degenerate ([[09 - Maps, Hash Tables and Skip Lists|ch. 09]]). The table above shows the expected case; an adversary could produce the other.
- **Amortised versus per-operation.** A single `list.append` is occasionally $O(n)$ while $n$ of them cost $O(n)$ total — the subject of [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]], and the one analytical idea Discrete Maths does not cover.

### 5. How to measure properly

```python
from time import perf_counter

def timeit(fn, n, reps=1):
    S = [random.random() for _ in range(n)]
    t0 = perf_counter()
    for _ in range(reps):
        fn(S)
    return (perf_counter() - t0) / reps
```

**The method that actually identifies a complexity class: double $n$ and look at the ratio of times.**

| observed ratio | class |
|---|---|
| ≈ 1 | $O(1)$ |
| slightly > 1 | $O(\log n)$ |
| ≈ 2 | $O(n)$ |
| a little over 2 | $O(n\log n)$ |
| ≈ 4 | $O(n^2)$ |
| ≈ 8 | $O(n^3)$ |

**This works because constants cancel in the ratio.** If $t(n)=cn^k$ then $t(2n)/t(n)=2^k$ regardless of $c$ — so the measurement recovers the *exponent* without needing to know the machine, the language, or how many primitive operations a line really costs. **That is why it is the right experiment**, and it is the single most useful technique in this chapter.

**Four practical cautions:**
1. **Use `perf_counter`**, not `time.time` — it is monotonic and has much better resolution.
2. **Repeat fast operations** and divide, or you measure timer granularity rather than the code.
3. **Time the worst case deliberately.** `unique1` on data with an early duplicate looks linear; the table above used all-distinct input for exactly this reason.
4. **Discard the first run** for anything JIT-compiled or cached; in plain CPython this matters less, but memory allocation still warms up.

## ✏️ Exercises

**1. (Reading loops.)** Give the complexity of each, with justification. (a) a single loop `for i in range(n)` doing constant work. (b) `for i in range(n): for j in range(n)`. (c) `for i in range(n): for j in range(i)`. (d) `while n > 1: n = n // 2`. (e) `for i in range(n): for j in range(n): for k in range(n)` but where the innermost loop only runs when `i == j`.

> [!example]- Solution
> **(a) $\Theta(n)$** — $n$ iterations, constant work each.
>
> **(b) $\Theta(n^2)$** — the inner loop runs $n$ times for each of $n$ outer iterations, so $n\cdot n$.
>
> **(c) $\Theta(n^2)$**, not $\Theta(n)$. The inner loop runs $i$ times on outer iteration $i$, so the total is
> $$\sum_{i=0}^{n-1}i=\frac{n(n-1)}2=\Theta(n^2).$$
> **A triangular loop is still quadratic** — it does half the work of the square one, and half of $n^2$ is $\Theta(n^2)$. This is `prefix_average1`.
>
> **(d) $\Theta(\log n)$** — each iteration halves $n$, so the number of iterations is the number of halvings needed to reach 1, namely $\lfloor\log_2 n\rfloor+1$. *(Same recurrence as binary search, solved in [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]] §4.)*
>
> **(e) $\Theta(n^2)$.** The innermost loop runs only when $i=j$, which happens for exactly $n$ of the $n^2$ pairs. So the cost is $n^2$ (for the two outer loops) plus $n\cdot n$ (for the $n$ times the inner loop runs, $n$ steps each) $=2n^2=\Theta(n^2)$.
>
> **This is `disjoint2`'s structure, and the lesson is (c) and (e) together: the nesting depth is an upper bound on the exponent, not the exponent.** Always ask how many times the inner loop *actually* runs.

**2. (The hidden loop.)** Explain why `prefix_average2` is $\Theta(n^2)$ despite having one visible loop. Give two more Python constructs whose cost is commonly underestimated, and say how you would confirm your answer.

> [!example]- Solution
> **Why it is quadratic.** The body is `A[j] = sum(S[0:j+1])/(j+1)`, and it contains **two hidden $\Theta(j)$ operations**:
> - `S[0:j+1]` **constructs a new list** of $j+1$ elements — allocation plus a copy;
> - `sum(...)` then **traverses** those $j+1$ elements.
>
> Summing over $j=0,\dots,n-1$ gives $2\sum_{j}(j+1)=\Theta(n^2)$. The loop looks single because the inner work is spelled with function-call syntax instead of a `for`.
>
> **Two more commonly underestimated constructs:**
>
> 1. **`x in some_list` is $O(n)$**, not $O(1)$. It looks like a single operator and is a linear scan. Inside a loop it silently produces $O(n^2)$ — the fix is `x in some_set`, which is $O(1)$ expected ([[09 - Maps, Hash Tables and Skip Lists|ch. 09]]). *(This is exactly the `unique1` versus `unique3` gap: 5,300× at $n=4000$.)*
> 2. **`s = s + piece` in a loop over strings is $O(n^2)$.** Strings are immutable, so each concatenation copies the whole accumulated string. Use `''.join(pieces)`, which is $O(n)$. The same trap applies to `list = list + [x]` versus `list.append(x)`.
>
> *(A third worth knowing: `list.insert(0, x)` and `list.pop(0)` are $O(n)$ because every element shifts — [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]. Use `collections.deque` for a queue, [[05 - Stacks, Queues and Deques|ch. 05]].)*
>
> **How to confirm:** double $n$ and check the ratio (§5). For `prefix_average2` it should be ≈4, not ≈2 — and the measurement in §3 confirms exactly that for its twin `prefix_average1`. **The general principle: when in doubt about whether a construct is $O(1)$, measure rather than assume**, because the "one operation" model of §1 is precisely what these constructs violate.

**3. (Measuring.)** Describe the doubling experiment, explain why it identifies the exponent without knowing the machine, and state what ratios you expect for $O(n)$, $O(n\log n)$, $O(n^2)$ and $O(n^3)$. Then interpret these measured ratios: 4.18, 4.17, 3.91.

> [!example]- Solution
> **The experiment.** Time the function on inputs of size $n$, $2n$, $4n$, $8n$; report each time divided by the previous one.
>
> **Why it works, and why it is machine-independent.** Suppose the true cost is $t(n)=cn^k$ for some unknown constant $c$ that absorbs the machine, the language and the number of primitive operations per line. Then
> $$\frac{t(2n)}{t(n)}=\frac{c(2n)^k}{cn^k}=2^k .$$
> **The constant $c$ cancels.** So the ratio depends only on the exponent $k$ — the experiment recovers the growth rate while knowing nothing about the hardware. **That is precisely what asymptotic notation abstracts, measured directly.**
>
> **Expected ratios:**
>
> | class | ratio on doubling |
> |---|---|
> | $O(1)$ | 1 |
> | $O(\log n)$ | slightly > 1 (an additive constant: $\log 2n=\log n+1$) |
> | $O(n)$ | **2** |
> | $O(n\log n)$ | a little over 2 — $\frac{2n\log 2n}{n\log n}=2\left(1+\frac1{\log n}\right)$, tending to 2 from above |
> | $O(n^2)$ | **4** |
> | $O(n^3)$ | **8** |
>
> **Interpreting 4.18, 4.17, 3.91:** these cluster tightly around **4**, so the algorithm is **quadratic**. *(These are the measured ratios for `prefix_average1`, whose analysis predicts $\Theta(n^2)$ — theory and measurement agree.)*
>
> **The deviation from exactly 4 is expected and informative.** Ratios slightly above 4 at small $n$ reflect lower-order terms that have not yet become negligible; the drift toward 3.91 at the largest size is measurement noise and memory effects. **Ratios within roughly ±15% of a predicted value confirm the class; a ratio of 2 or 8 would refute it.** The measurement is a discriminator between classes, not a precision instrument.
>
> *(Note $O(n\log n)$ and $O(n)$ are the hardest pair to separate this way, since the ratios are 2.1-ish versus 2.0. The measured `unique2` ratios of 2.17 and 2.90 sit above `unique3`'s 2.09 and 1.87, which is consistent — but distinguishing them reliably needs a wider range of $n$.)*

**4. (Choosing an implementation.)** You must decide whether a sequence of $n$ items contains duplicates. (a) Give three algorithms with different complexities. (b) Which would you use, and when might the answer differ? (c) At $n=4000$ the measured times were 0.221 s, 0.000371 s and 0.000042 s. What does that tell you?

> [!example]- Solution
> **(a)** §3's three:
>
> | | method | complexity |
> |---|---|---|
> | `unique1` | compare every pair | $O(n^2)$ |
> | `unique2` | sort, then check adjacent pairs | $O(n\log n)$ |
> | `unique3` | build a set, compare sizes | $O(n)$ **expected** |
>
> **(b) `unique3` in almost every case** — it is the simplest to read and the fastest. **But three situations change the answer:**
>
> 1. **The elements are unhashable** (lists, or custom classes defining `__eq__` without `__hash__` — [[01 - Python and Object-Oriented Foundations|ch. 01]] §3). Then `set` is unavailable and `unique2` is the fallback, needing only that elements be *orderable*.
> 2. **You need the sorted data anyway.** Then `unique2` is effectively free, since you were going to sort regardless.
> 3. **Memory is tight.** `unique3` builds a set of up to $n$ elements; `unique1` uses $O(1)$ extra space. For very large $n$ against a hard memory limit that can matter — **the time/space trade-off is real, and asymptotic time analysis alone will not surface it.**
>
> *(A fourth: worst-case guarantees. `unique3` is $O(n^2)$ in the worst case if hashing degenerates — [[09 - Maps, Hash Tables and Skip Lists|ch. 09]]. If an adversary controls the input, `unique2`'s $O(n\log n)$ **worst-case** bound may be preferable to `unique3`'s $O(n)$ **expected** one.)*
>
> **(c) Two things.**
>
> **First, the ordering confirms the analysis** — the three times are in the predicted order, and the ratios between successive doublings (4.03/3.77, 2.17/2.90, 2.09/1.87) identify the three classes independently.
>
> **Second, and more important: $0.221 / 0.000042 \approx 5{,}300\times$.** The quadratic method is over five thousand times slower **at only $n=4000$**, and because the gap grows with $n$ it will be worse at any realistic scale.
>
> **No constant-factor optimisation can recover that.** Rewriting `unique1` in C might buy 50×; it would still be 100× slower than the Python `unique3`. **This is the concrete case for the rule in §4: get the asymptotic class right first, and treat constant-factor tuning as a separate, later, measurement-driven activity.**

**5. (Hard — the limits of the model.)** (a) State the assumption underlying primitive-operation counting and give two cases where it fails. (b) Both `for i in range(n): out.append(i*i)` and `[i*i for i in range(n)]` are $O(n)$; measured at $n=2\times10^6$ they took 0.1244 s and 0.1099 s. Reconcile this with (c) the 5,300× gap of Exercise 4. (d) What should you conclude about when to trust asymptotic analysis?

> [!example]- Solution
> **(a) The assumption: every primitive operation takes constant time**, so counting operations is a machine-independent proxy for time.
>
> **Two failures:**
> 1. **Operations that are not primitive but look it.** `sum(S[0:j+1])` is one expression and $\Theta(j)$ work; `x in some_list` is one operator and $O(n)$; `s = s + piece` is one assignment and $O(\text{len}(s))$. **The model is only as good as your judgement about what counts as one operation** — and Python's expressive syntax makes it easy to be wrong.
> 2. **Operations that are primitive but not equal-cost.** An array access to contiguous memory and a pointer dereference to an arbitrary heap address are both "one operation"; the second may cost a cache miss worth hundreds of cycles. **This is why $O(n)$ array traversal reliably beats $O(n)$ linked-list traversal** ([[06 - Linked Lists|ch. 06]]), and the model cannot see it at all.
>
> **(b) Both observations are correct and they are about different things.**
>
> The two constructs have the **same growth rate** — doubling $n$ doubles both times. They differ by a **constant factor of about 1.13**, which arises from interpreter overhead: the explicit loop performs a method lookup and call for `append` on every iteration, while the comprehension runs a specialised bytecode.
>
> **A constant factor cannot change with $n$ — that is what "constant" means.** So the 13% is 13% at every size, whereas Exercise 4's gap is a *ratio that grows*: at $n=4000$ it is 5,300×, and at $n=8000$ it would be roughly 10,000×.
>
> **(c) The reconciliation is the distinction between a factor and a rate.**
>
> $$\underbrace{0.1244/0.1099=1.13}_{\text{constant factor — fixed}}\qquad\text{versus}\qquad \underbrace{0.221/0.000042\approx5300}_{\text{growing with }n}$$
>
> Asymptotic analysis **deliberately discards** the first and **exactly captures** the second. It is not that the model is wrong about the 13%; it is that the model was never claiming anything about it.
>
> **(d) Three conclusions.**
>
> 1. **Trust asymptotic analysis to rank algorithms at scale, and act on it first.** A better complexity class beats any constant-factor work, and the advantage grows.
> 2. **Do not trust it for small $n$, or for choosing between implementations in the same class.** There, only measurement decides — and the answer is legitimately machine-dependent. This is why library sorts switch to insertion sort below a threshold ([[Discrete Mathematics/contents/04 - Algorithms and Their Analysis|DM ch. 04]] Note 8, [[11 - Sorting and Selection|ch. 11]]).
> 3. **Always ask whether your "one operation" assumption is honest**, and confirm by doubling $n$. **The model's failures are almost never in the mathematics — they are in the accounting.**
>
> **The synthesis, and this chapter's thesis:** derive the complexity, then measure it. Agreement means your accounting was right; disagreement means you have found a hidden loop, a cache effect, or a wrong worst case — **and all three are worth finding.**

## 📝 Summary

- **Experimental analysis** is limited by hardware-dependence, by testing only the inputs you chose, and by needing a full implementation. **Theoretical analysis** fixes all three by counting **primitive operations**.
- **"Each primitive operation is constant time" is a model that leaks** — through hidden loops (`sum(S[0:j])`, `x in list`), through memory locality, and through amortisation. **The two methods are complements: theory gives the rate, measurement audits the accounting.**
- **The seven functions:** $1\prec\log n\prec n\prec n\log n\prec n^2\prec n^3\prec2^n$. The **base of a logarithm never matters**; the base of an exponent always does. **The $n\log n$ / $n^2$ gap is the one that decides whether a program finishes.**
- **Reading loops:** nesting depth is an **upper bound** on the exponent, not the exponent. A triangular loop $\sum i=\Theta(n^2)$ is still quadratic; an inner loop that runs only $n$ times out of $n^2$ contributes only $\Theta(n^2)$ (`disjoint2`).
- **`prefix_average2` is the trap worth memorising:** one visible loop, still $\Theta(n^2)$, because `S[0:j+1]` builds a list and `sum` traverses it. **Function-call syntax hides loops.**
- **The doubling experiment identifies the class**: ratios of ≈1, ≈2, a little over 2, ≈4, ≈8 for $O(1)$, $O(n)$, $O(n\log n)$, $O(n^2)$, $O(n^3)$. **It is machine-independent because the constant cancels in the ratio** — $t(2n)/t(n)=2^k$.
- **Measured confirmations:** `prefix_average1` gave 4.18, 4.17, 3.91; `prefix_average3` gave 2.10, 2.01, 2.07, 1.98; `disjoint1` gave 7.42, 8.34; `disjoint2` gave 3.56, 3.91. **Theory and measurement agreed every time.**
- **Constant factors versus growth rates:** a 13% difference between two $O(n)$ idioms is fixed forever; the 5,300× gap between $O(n^2)$ and $O(n)$ at $n=4000$ **grows without bound**. **Fix the class first; tune constants second, guided by measurement.**
- **But asymptotics say nothing about small $n$** — which is why real libraries switch to simple quadratic methods below a threshold. **Constants decide small inputs, growth rates decide large ones**, and knowing your regime is the skill.
- **Measure with `perf_counter`, repeat fast operations, deliberately construct the worst case**, and remember that expected-case results (hashing) are not worst-case guarantees.

## ⚠️ Important Notes

1. **State which case you mean.** "This is $O(n^2)$" is incomplete — worst, average or expected? `unique3` is $O(n)$ expected and $O(n^2)$ worst case, and the difference matters if an adversary supplies the input.
2. **Nesting depth is an upper bound, not the answer.** Count how many times the inner loop *actually executes*. `disjoint2` has three nested loops and is quadratic.
3. **A triangular loop is quadratic.** $\sum_{i<n} i=\frac{n(n-1)}{2}$; halving a quadratic leaves it quadratic.
4. **Function-call syntax hides loops.** `sum(...)`, `min(...)`, `sorted(...)`, `x in list`, slicing, and string concatenation all carry costs proportional to their input. **The model's failures live here.**
5. **`x in some_list` is $O(n)$; `x in some_set` is $O(1)$ expected.** Inside a loop, that single character difference is $O(n^2)$ versus $O(n)$.
6. **Building a string with `+=` in a loop is $O(n^2)$.** Strings are immutable; use `''.join(...)`.
7. **When you cannot tell whether something is $O(1)$, measure it.** Doubling $n$ and reading the ratio takes two minutes and settles the question.
8. **Use `perf_counter`, not `time.time`.** And repeat fast operations enough to exceed timer granularity, or you will measure the clock.
9. **Time the worst case on purpose.** An early-exit algorithm looks fast on data that triggers the exit; `unique1` on input with a duplicate at position 2 looks $O(1)$.
10. **Expect ratios within roughly ±15% of prediction.** The doubling test discriminates between classes; it is not a precision measurement, and lower-order terms distort it at small $n$.
11. **$O(n)$ and $O(n\log n)$ are hard to separate empirically** — ratios of 2.0 versus 2.1. Use a wide range of $n$, or rely on the analysis.
12. **Fix the asymptotic class before tuning constants.** Rewriting an $O(n^2)$ algorithm in C is almost always the wrong move when an $O(n)$ algorithm exists in Python.
13. **But do not apply that rule below the crossover.** For small $n$ the constants dominate, and the "worse" algorithm often wins — this is a real engineering fact, not a rounding error.
14. **Asymptotic analysis cannot see memory locality**, which is why contiguous arrays beat pointer-chasing structures with identical complexity. Expect measurement to reveal it in [[06 - Linked Lists|ch. 06]].
15. **Time is not the only resource.** `unique3` is fastest and uses $O(n)$ extra memory; `unique1` is slowest and uses $O(1)$. **Analyse space alongside time**, especially when recursion is involved ([[03 - Recursion|ch. 03]]).
16. **Derive, then measure.** Agreement validates your accounting; disagreement means a hidden loop, a cache effect or a wrong worst case — **all three are findings worth having.**

> [!warning] Gaps in the source material
> **Goodrich's prose for this chapter extracts cleanly** — the discussion of experimental studies, primitive operations, the seven functions and the asymptotic definitions all came through readably.
>
> **His code did not**, per the standing problem recorded in `00-Index.md`: indentation lost, double underscores rendered as spaces, identifiers split. **So all four algorithm families in §3 (`prefix_average1/2/3`, `unique1/2/3`, `disjoint1/2`, and the timing harness) are my own implementations** of the algorithms his prose describes, **and every one was executed** — first for correctness on edge cases (`[]`, single element, duplicates, all-distinct), then for timing.
>
> **Every number in this chapter is a measurement I took, not a figure copied from the book.** Goodrich's Figure 3.1 (a plot of experimental running times) is an image and is lost, as are the tables of function growth. **Replacing them with measurements is arguably an improvement** — this is the one subject where the reader can reproduce every claim by running the code — but it does mean **the timings are specific to this machine**, and the *ratios*, not the absolute times, are the transferable content. That is §5's point and it is why the ratio method is emphasised over raw timings.
>
> **All figures are images and are lost**, including the seven-functions growth chart and the illustrations of loop structure.
>
> **No error was found in Goodrich ch. 3.** Every complexity claim his prose makes was confirmed by measurement — $\Theta(n^2)$ for both slow prefix-average methods, $\Theta(n)$ for the third, $\Theta(n^3)$ and $\Theta(n^2)$ for the two disjointness methods.
>
> **Deliberately not covered.** **§3.3's formal treatment of big-$O$, big-$\Omega$ and big-$\Theta$ is owned by [[Discrete Mathematics/contents/04 - Algorithms and Their Analysis|Discrete Mathematics ch. 04]]** — including the definitions, the quantifier structure, the polynomial and logarithm rules, and the caution that "$=$" is an abuse of notation. **§3.4 (justification techniques: counterexample, contraposition, contradiction, induction and loop invariants) is owned by [[Discrete Mathematics/contents/02 - Proofs and Mathematical Induction|DM ch. 02]]**, which treats all of them at length. This chapter cross-links and spends its space on application and measurement instead — the split recorded in both indexes.
>
> **Additions beyond the source.** **The entire measurement programme is mine.** Goodrich advocates experimental analysis in §3.1 and then does none of it; every table of timings and ratios here was produced for these notes. **The doubling-ratio method and its justification** ($t(2n)/t(n)=2^k$, so the constant cancels) is stated here as the central technique — Goodrich mentions fitting a curve to data but not this much simpler discriminator. The **5,300× versus 13% contrast** framing §4's rule is mine, as is the list of Python constructs whose cost is underestimated (`x in list`, string `+=`, `list.insert(0,·)`), the four practical cautions in §5, and the three blind spots (locality, expected-vs-worst, amortised) with their forward links. **`unique3` (the hash-set method) is my addition** — Goodrich gives only the quadratic and sorting-based versions at this stage, and including it makes the asymptotic point far more vividly.

**Previous:** [[01 - Python and Object-Oriented Foundations]] · **Next:** [[03 - Recursion]]
