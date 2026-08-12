---
subject: Data Structures and Algorithms
chapter: 4
tags: [ds, dsa, arrays, dynamic-arrays, amortised-analysis, python-list, referential-arrays]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 5; Lambert, *Fundamentals of Python: Data Structures*, ch. 4"
---

# Array-Based Sequences and Amortised Analysis

Two things happen in this chapter.

The first is that **Python's `list` stops being magic.** You will build one, see why `append` is fast and `insert(0, x)` is not, and be able to predict the cost of any list operation from first principles.

The second is **amortised analysis** — and this is the one significant analytical technique that [[Discrete Mathematics/contents/00-Index|Discrete Mathematics]] does not cover, so it is developed properly here rather than cross-linked. It answers a question the worst-case analysis of [[02 - Algorithm Analysis in Practice|ch. 02]] cannot: *what if an operation is usually cheap but occasionally expensive?*

## 📘 Main Knowledge

### 1. Low-level arrays, and what a Python list really holds

A computer's memory is a sequence of bytes at consecutive addresses. An **array** is a contiguous block of equal-sized cells, and that is what buys $O(1)$ indexing:

$$\text{address of } A[k] \;=\; \text{start} + k \times \text{cell size}$$

**One multiplication and one addition, regardless of $k$ or of the array's length.** Every $O(1)$ claim about arrays traces back to this arithmetic.

> [!note] Python lists are **referential** arrays
> A Python list does **not** store its objects; it stores **references** (pointers) to them. So every cell is the same size — a machine address — no matter how big the objects are.
>
> Three consequences that matter:
> 1. **A list of a million integers is a million *pointers*** plus the integer objects themselves. `sys.getsizeof(L)` reports only the pointer array.
> 2. **Slicing and copying are shallow** — the new list holds the *same* references, which is [[01 - Python and Object-Oriented Foundations|ch. 01]] §1's aliasing, now explained at the storage level.
> 3. **`[None]*n` is genuinely cheap** — $n$ copies of one reference — whereas the equivalent in C would allocate $n$ objects.
>
> *(By contrast, a `bytes`, `str` or `array.array` object is a **compact** array storing the values directly. That is why `array.array('i', ...)` uses far less memory than a list of the same integers, and why NumPy arrays exist.)*

### 2. Dynamic arrays: how `list` grows

A low-level array has a **fixed** size. Yet `list.append` works indefinitely. The trick:

**Keep an array with spare capacity. When it fills, allocate a bigger one and copy everything across.**

```python
import ctypes

class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""

    def __init__(self):
        self._n = 0                                   # elements currently stored
        self._capacity = 1                            # slots currently available
        self._A = self._make_array(self._capacity)

    def __len__(self):
        return self._n

    def __getitem__(self, k):
        if not 0 <= k < self._n:
            raise IndexError('invalid index')
        return self._A[k]                             # O(1)

    def append(self, obj):
        if self._n == self._capacity:                 # no room left
            self._resize(2 * self._capacity)          # DOUBLE the capacity
        self._A[self._n] = obj
        self._n += 1

    def _resize(self, c):
        B = self._make_array(c)                       # new, bigger array
        for k in range(self._n):                      # the O(n) copy
            B[k] = self._A[k]
        self._A = B
        self._capacity = c

    @staticmethod
    def _make_array(c):
        return (c * ctypes.py_object)()               # raw array of c references
```

*(Verified: appending 0–9 gives `len` 10, `da[0]`=0, `da[9]`=9, capacity 16, and `da[10]` raises `IndexError`.)*

**Note `__getitem__` raises `IndexError`** — [[01 - Python and Object-Oriented Foundations|ch. 01]] §3's requirement, so that iteration terminates cleanly.

> [!example]- Python's real `list` does the same thing — you can watch it (verified)
> `sys.getsizeof` reports the size of the underlying pointer array, so appending and watching for jumps reveals the growth strategy:
>
> ```
> capacity increases at n = 1, 5, 9, 17, 25, 33, 41, 53, 65, 77, 93, 109, 129
> successive ratios       = 5.00, 1.80, 1.89, 1.47, 1.32, 1.24, 1.29, 1.23
> ```
>
> **The ratios settle towards a constant** (CPython over-allocates by roughly $\tfrac18$, so about 1.125 asymptotically) rather than dropping towards 1. **It is geometric growth, not constant growth** — which §4 shows is the whole ballgame.
>
> *(An empty list is 56 bytes of object header with no capacity at all; the first append allocates.)*

### 3. Amortised analysis

Here is the puzzle. **Most `append`s are $O(1)$** — write into a spare slot. **Occasionally one is $O(n)$** — allocate and copy everything. So what is the cost of an `append`?

- "$O(n)$ worst case" is **true and useless** — it suggests $n$ appends cost $O(n^2)$, which is wrong.
- "$O(1)$ average" is **misleading** — it sounds probabilistic, and there is nothing random here.

> [!note] Definition — amortised cost
> The **amortised** cost of an operation is the **total** cost of a sequence of $n$ operations, divided by $n$.
>
> It is a **worst-case guarantee about sequences**, not a probabilistic claim about individual operations.

**Claim: with a doubling strategy, `append` has amortised cost $O(1)$.**

*Proof by counting the copies.* Starting from capacity 1, resizes happen when the array holds $1,2,4,8,\dots,2^k$ elements, and the resize at capacity $2^i$ copies $2^i$ elements. Over $n$ appends the total copying is
$$1+2+4+\cdots+2^k \;=\; 2^{k+1}-1 \;<\; 2n,$$
by the **geometric sum** of [[Discrete Mathematics/contents/02 - Proofs and Mathematical Induction|DM ch. 02]] §6, since $2^k<n$. Adding the $n$ constant-time writes, the total for $n$ appends is $O(n)$, so the amortised cost per append is $O(1)$. $\blacksquare$

*(Verified — total element-copies during $n$ appends:)*

| $n$ | copies | as a multiple of $n$ |
|---|---|---|
| 1 000 | 1 023 | 1.02 |
| 10 000 | 16 383 | 1.64 |
| 100 000 | 131 071 | 1.31 |
| 1 000 000 | 1 048 575 | 1.05 |

**Always under $2n$, exactly as the bound says.**

> [!note] The banker's argument — the intuition worth having
> Charge every `append` **three tokens**: one to write the new element, and two saved in the bank. When a resize copies $n$ elements, each of the $n/2$ elements added since the last resize has two tokens saved — exactly enough to pay for copying itself and one older element.
>
> **The bank never goes overdrawn, so the constant charge of 3 covers everything** — which is what amortised $O(1)$ means. *(This is the standard accounting method; Goodrich gives the equivalent geometric argument.)*

> [!warning] Amortised is not average, and the difference is measurable
> "Amortised $O(1)$" does **not** mean every operation is fast. It means the *total* is bounded. Individual operations really do spike:
>
> *(Measured over 200 000 appends:)*
>
> | | |
> |---|---|
> | slowest single `append` | 0.000529 s |
> | mean `append` | 0.000000104 s |
> | **ratio** | **≈ 5 084×** |
>
> **One append was five thousand times slower than the average — and the total was still linear.** *(Verified.)*
>
> **This matters in practice.** In a real-time or latency-sensitive system, a guarantee about the *total* is not a guarantee about the *tail*: that one 0.5 ms pause is a missed frame or a blown deadline. **Amortised bounds are the right tool for throughput and the wrong tool for worst-case latency**, and knowing which you need is the engineering judgement.

### 4. Why *doubling*, and not "grow by one"

The obvious alternative — enlarge by a constant each time — is catastrophic, and it is worth seeing how catastrophic.

**Growing by 1:** the resize at size $i$ copies $i$ elements, so $n$ appends cost
$$1+2+3+\cdots+n=\frac{n(n+1)}2=\Theta(n^2),$$
the triangular sum of [[Discrete Mathematics/contents/02 - Proofs and Mathematical Induction|DM ch. 02]] and [[02 - Algorithm Analysis in Practice|ch. 02]] §3. **Amortised cost $\Theta(n)$ per append**, not $O(1)$.

*(Verified — total copies with constant growth:)*

| $n$ | copies | per append | $n^2/2$ |
|---|---|---|---|
| 1 000 | 499 500 | 499.5 | 500 000 |
| 5 000 | 12 497 500 | 2 499.5 | 12 500 000 |
| 20 000 | 199 990 000 | 9 999.5 | 200 000 000 |

**Compare the doubling table in §3: 1.05×$n$ against 9 999×$n$.**

> [!note] Any growth *factor* > 1 works; any constant *increment* fails
> The essential property is that the capacity grows **geometrically**, so the resize costs form a geometric series that sums to $O(n)$. Doubling is the simplest choice; CPython uses ≈1.125, which wastes less memory at the cost of more frequent resizes. **Both are amortised $O(1)$; they differ only in the constant.**
>
> **The trade-off is time versus space:** a larger factor means fewer resizes and more wasted capacity. Doubling can leave up to 50% of the array unused; growing by 1.125 leaves at most about 12%.

### 5. The cost of every list operation

Now the practical payoff — knowing what is cheap.

*(Measured on a 100 000-element list, per operation:)*

| Operation | Time | Complexity | Why |
|---|---|---|---|
| `L[500]` | 18 ns | $O(1)$ | address arithmetic (§1) |
| `L.append(x)` | 25 ns | $O(1)$ **amortised** | write into spare slot |
| `L.pop()` | 28 ns | $O(1)$ amortised | drop the last element |
| **`L.pop(0)`** | **9 315 ns** | $O(n)$ | **every element shifts left** |
| **`L.insert(0, x)`** | **54 117 ns** | $O(n)$ | **every element shifts right** |
| `500 in L` (early hit) | 3 292 ns | $O(n)$ | linear scan, exits early |
| `99999 in L` (late hit) | 618 048 ns | $O(n)$ | linear scan, full length |

**`insert(0, x)` is about 2 000× slower than `append`** on this list, and the gap grows with $n$.

> [!example]- Confirmed by the doubling test (verified)
> **`append`** — amortised $O(1)$ each, so $O(n)$ total, predicting a time ratio of **2**:
>
> | $n$ | time | ratio |
> |---|---|---|
> | 100 000 | 0.0036 s | — |
> | 200 000 | 0.0081 s | 2.26 |
> | 400 000 | 0.0209 s | 2.59 |
> | 800 000 | 0.0416 s | **1.99** |
>
> **`insert(0, x)`** — $O(n)$ each, so $O(n^2)$ total, predicting a ratio of **4**:
>
> | $n$ | time | ratio |
> |---|---|---|
> | 10 000 | 0.0253 s | — |
> | 20 000 | 0.1021 s | **4.04** |
> | 40 000 | 0.4195 s | **4.11** |
> | 80 000 | 1.6808 s | **4.01** |
>
> **Ratios of 2 and 4, as predicted.** Note the $n$ values differ by an order of magnitude between the tables — building a list of 800 000 by `append` is *faster* than building one of 80 000 by `insert(0, ·)`.

> [!warning] The single most common Python performance bug
> ```python
> queue = []
> queue.append(item)      # O(1)  -- fine
> item = queue.pop(0)     # O(n)  -- every dequeue shifts the whole list
> ```
> **Using a list as a queue is $O(n)$ per dequeue and $O(n^2)$ overall.** The fix is `collections.deque`, which gives $O(1)$ at both ends — the subject of [[05 - Stacks, Queues and Deques|ch. 05]].
>
> **A list is a good stack** (`append`/`pop` at the end are both $O(1)$) **and a bad queue.** That asymmetry follows directly from §1's memory layout: the end of an array can grow into spare capacity, but the front cannot move without shifting everything.

### 6. When the array is the wrong structure

Arrays are excellent at: indexing, appending, iterating in order, and memory locality. They are poor at: inserting or deleting anywhere but the end, and searching (unless sorted).

**The obvious alternative is to abandon contiguity** — store each element in its own node with a pointer to the next, so insertion is a pointer update rather than a shift. That is [[06 - Linked Lists|ch. 06]], and the comparison there is the point.

## ✏️ Exercises

**1. (Referential arrays.)** (a) What does a Python list store? (b) Why is `[None]*n` cheap? (c) Explain aliasing in terms of storage. (d) Why does `array.array('i', ...)` use less memory than a list of the same integers?

> [!example]- Solution
> **(a) References**, not the objects themselves. Each cell holds a machine address of fixed size, so cells are uniform regardless of what they point to.
>
> **(b)** It allocates $n$ cells and writes **the same reference** into each — one object (`None`), $n$ pointers. No objects are constructed. *(Contrast a C array of $n$ structs, which allocates $n$ structs.)*
>
> **(c)** `b = a` copies **one reference**, so both names denote the same list object. `c = a[:]` builds a **new** pointer array whose cells hold **the same references** as `a`'s — hence a shallow copy: the outer list is independent, the inner objects are shared. **[[01 - Python and Object-Oriented Foundations|Ch. 01]] §1's rules are simply what pointer-copying looks like from above.**
>
> This also explains `[[0]*2]*2`: the outer multiplication copies **one reference** to the inner list twice, so both rows are the same object.
>
> **(d) `array.array` is compact, not referential** — it stores the machine integers directly, typically 4 bytes each. A list stores an 8-byte pointer per element *plus* a Python `int` object (28+ bytes) per distinct value. **So a million-element list costs roughly 8 MB of pointers plus the integer objects, while `array.array('i')` costs 4 MB total.**
>
> *(Small integers are cached and shared by CPython, so a list of a million small values shares objects and is less wasteful than the arithmetic suggests — but the pointer array is still 8 MB.)* **This is precisely why NumPy exists**: numerical work needs compact arrays, and every element of [[Data Preparation and Visualization/contents/01 - Getting Started with Pandas|pandas]] rests on that.

**2. (Dynamic arrays.)** (a) Explain how a dynamic array supports unbounded `append` on fixed-size storage. (b) Implement one with doubling. (c) How many resizes occur while appending 100 000 items? (d) How many elements are copied in total?

> [!example]- Solution
> **(a)** Maintain an array with **spare capacity** and a count of elements actually used. `append` writes into the next free slot in $O(1)$. When full, allocate a **larger** array, copy everything across, and continue — an $O(n)$ operation, but a rare one.
>
> **(b)** §2's `DynamicArray`. *(Verified: appending 0–9 gives length 10, correct elements, capacity 16, and `IndexError` beyond the end.)*
>
> **(c) 17 resizes** *(verified)*. Starting from capacity 1 and doubling, capacities go $1,2,4,\dots,2^{17}=131\,072$, and $2^{16}=65\,536<100\,000\le131\,072$. So the number of resizes is $\lceil\lg 100\,000\rceil=17$.
>
> **In general $\lceil\lg n\rceil$ resizes** — logarithmically few, which is the first hint of why the total is cheap.
>
> **(d) 131 071 copies** *(verified)* — that is $1+2+4+\cdots+65\,536=2^{17}-1$, or about $1.31n$.
>
> **The general bound is $<2n$** by the geometric sum, and the measured values confirm it: 1.02$n$, 1.64$n$, 1.31$n$, 1.05$n$ at $n=10^3,10^4,10^5,10^6$. **The oscillation between 1.0 and 1.6 depends on where $n$ falls between powers of two** — worst just after a resize, best just before.

**3. (Amortised analysis.)** (a) Define amortised cost and distinguish it from average cost. (b) Prove `append` is amortised $O(1)$ under doubling. (c) Show that growing by a constant is not. (d) Give evidence that individual appends are *not* uniformly fast.

> [!example]- Solution
> **(a)** **Amortised cost** = total cost of $n$ operations, divided by $n$. It is a **worst-case guarantee about a sequence**.
>
> **Average cost** is a probabilistic statement about a *distribution* of inputs. **The distinction matters:** amortised $O(1)$ holds for *every* sequence of appends, with no assumption about randomness; an average-case bound would fail on an adversarial input. **Amortised analysis is the stronger claim.**
>
> **(b)** Resizes occur at sizes $1,2,4,\dots,2^k$ with $2^k<n$; the resize at capacity $2^i$ copies $2^i$ elements. Total copying:
> $$\sum_{i=0}^{k}2^i=2^{k+1}-1<2n$$
> by the geometric sum ([[Discrete Mathematics/contents/02 - Proofs and Mathematical Induction|DM ch. 02]] §6). Adding $n$ constant-time writes gives $O(n)$ total for $n$ appends, hence **$O(1)$ amortised.** $\blacksquare$ *(Verified: always under $2n$.)*
>
> **(c)** With growth by 1, the resize before the $i$th append copies $i-1$ elements, so the total is
> $$\sum_{i=1}^{n}(i-1)=\frac{n(n-1)}2=\Theta(n^2),$$
> giving **$\Theta(n)$ amortised per append.** *(Verified: at $n=20\,000$, 199 990 000 copies — 9 999.5 per append, against $n^2/2=2\times10^8$ ✓)*
>
> **The difference is 1.05$n$ versus 9 999$n$ at comparable sizes** — geometric growth versus arithmetic growth, and it is the same distinction as [[02 - Algorithm Analysis in Practice|ch. 02]]'s constant factor versus growth rate.
>
> **(d) Direct measurement.** Timing each of 200 000 individual appends *(verified)*:
> $$\text{slowest} = 0.000529\ \text{s},\qquad \text{mean} = 0.000000104\ \text{s},\qquad \text{ratio} \approx \mathbf{5084\times}$$
>
> **So one append really was five thousand times slower than typical** — that is the resize copying 100 000-odd references — **and the total was still linear.**
>
> **This is what makes "amortised" the right word and "average" the wrong one.** The spikes are real, predictable (they occur at powers of two), and irrelevant to throughput — but decisive if you care about the tail. **A latency-sensitive system needs a worst-case bound, not an amortised one.**

**4. (List operation costs.)** Rank by cost, with reasons: `L[k]`, `L.append(x)`, `L.insert(0,x)`, `L.pop()`, `L.pop(0)`, `x in L`. Then explain why a list is a good stack and a bad queue.

> [!example]- Solution
> *(Measured on a 100 000-element list.)*
>
> | Rank | Operation | Time | Complexity | Reason |
> |---|---|---|---|---|
> | 1 | `L[k]` | 18 ns | $O(1)$ | address arithmetic — one multiply, one add |
> | 2 | `L.append(x)` | 25 ns | $O(1)$ amortised | write to a spare slot; occasional resize |
> | 3 | `L.pop()` | 28 ns | $O(1)$ amortised | decrement the count |
> | 4 | `x in L` | 3 μs–618 μs | $O(n)$ | linear scan; cost depends on position |
> | 5 | `L.pop(0)` | 9.3 μs | $O(n)$ | shift all $n-1$ remaining elements left |
> | 6 | `L.insert(0,x)` | 54 μs | $O(n)$ | shift all $n$ elements right, possibly resize |
>
> **The two $O(n)$ shifts are ~2 000–3 000× slower than the $O(1)$ operations here**, and the ratio grows with $n$.
>
> *(Note `x in L` spans two orders of magnitude depending on where the target sits — 3 μs for an early hit, 618 μs for a late one. **Always time the worst case**, [[02 - Algorithm Analysis in Practice|ch. 02]] Note 9.)*
>
> **Why a list is a good stack.** A stack pushes and pops at **one end**. Choosing the *back* means `append` and `pop()` — both $O(1)$ amortised, both operating in spare capacity, both with excellent locality. **A Python list is an ideal stack**, and [[05 - Stacks, Queues and Deques|ch. 05]] uses one.
>
> **Why it is a bad queue.** A queue adds at one end and removes at the **other**. Whichever end you choose for removal, that operation is $O(n)$:
> - `pop(0)` shifts every remaining element left;
> - `insert(0, x)` shifts every element right.
>
> **So a list-backed queue is $O(n)$ per operation and $O(n^2)$ overall** — the measured `insert(0,·)` ratios of 4.04, 4.11, 4.01 confirm the quadratic total.
>
> **The root cause is §1's memory layout.** An array's elements are at consecutive addresses, so the *index* of every element after a removal must change — and since the index is computed from the start address, that means physically moving the data. **The end can grow into spare capacity; the front cannot.** Fixing this requires either giving up contiguity ([[06 - Linked Lists|ch. 06]]) or tracking the front separately (`collections.deque`, and the circular buffer of [[05 - Stacks, Queues and Deques|ch. 05]]).

**5. (Hard — the growth factor.)** (a) Why must the array grow *geometrically*? (b) Prove growing by a constant $c$ is $\Theta(n^2)$ regardless of $c$. (c) What does the choice of factor trade off? (d) CPython uses ≈1.125 rather than 2 — why might that be right? (e) When is an amortised bound unacceptable?

> [!example]- Solution
> **(a) Because the resize costs must form a convergent (geometric) series.**
>
> With growth factor $r>1$, resizes occur at sizes $1,r,r^2,\dots$ and the copy at size $r^i$ costs $r^i$. The total up to $n$ is
> $$\sum_{i=0}^{\log_r n}r^i=\frac{r^{\log_r n+1}-1}{r-1}<\frac{r}{r-1}\,n=O(n),$$
> **linear in $n$ with constant $\frac{r}{r-1}$.** *(For $r=2$ that constant is 2, matching §3's $<2n$ ✓)* The essential point is that **the last resize dominates** — it copies more than all previous resizes combined — so the total is proportional to the final size rather than to the number of resizes.
>
> **(b)** With growth by a constant $c$, resizes occur at sizes $c,2c,3c,\dots$ and there are $n/c$ of them, the $i$th copying $ic$ elements:
> $$\sum_{i=1}^{n/c}ic=c\cdot\frac{(n/c)(n/c+1)}2=\frac{n^2}{2c}+\frac n2=\Theta(n^2).$$
> **The constant $c$ affects only the coefficient $\frac1{2c}$, never the exponent.** Doubling $c$ halves the work and leaves it quadratic. *(Verified for $c=1$: 199 990 000 copies at $n=20\,000$, against $n^2/2=2\times10^8$ ✓)*
>
> **This is the arithmetic-versus-geometric distinction**, and it is why "grow by a generous fixed amount" is not a fix.
>
> **(c) Time against space.**
>
> | Factor $r$ | resizes for $n$ items | total copies | worst-case waste |
> |---|---|---|---|
> | 2 | $\lg n$ | $<2n$ | up to **50%** |
> | 1.5 | $\log_{1.5}n\approx1.7\lg n$ | $<3n$ | up to 33% |
> | 1.125 | $\approx5.9\lg n$ | $<9n$ | up to **11%** |
>
> **A larger factor means fewer, larger resizes and more wasted memory; a smaller factor means more frequent resizes and tighter memory.** All are amortised $O(1)$; only the constants differ.
>
> **(d) Because memory is often the binding constraint, and the copying is cheap.** Three reasons CPython's choice is defensible:
> 1. **Lists are ubiquitous in Python** — millions may exist at once, so 50% average waste across all of them is a large absolute cost, whereas an extra few resizes on each is not.
> 2. **`memcpy` of contiguous memory is extremely fast** — bounded by memory bandwidth, not per-element work — so the constant hidden in "$<9n$ copies" is small.
> 3. **Growing by $\tfrac18$ plus a constant behaves well for small lists too**, where doubling from 1 would over-allocate proportionally more.
>
> *(Measured growth points $1,5,9,17,25,33,41,53,65,\dots$ show ratios falling from 5.00 toward ≈1.125, consistent with `newsize + (newsize >> 3) + 6`.)* **The general lesson: the asymptotic argument fixes the *class*, and the constant is then an engineering choice about the actual workload** — exactly [[02 - Algorithm Analysis in Practice|ch. 02]] §4's division of labour.
>
> **(e) Whenever you need a bound on the *individual* operation rather than the total.** Three concrete cases:
> 1. **Real-time systems.** A 0.5 ms pause — the measured worst append — misses a 60 fps frame deadline. **Amortised $O(1)$ guarantees nothing about any single call.**
> 2. **Interactive latency.** Tail latency (p99, p999) is what users notice; a structure that is fast on average and occasionally slow can have terrible tail behaviour.
> 3. **Adversarial settings.** If an attacker can time operations, resize spikes leak information about the structure's internal size.
>
> **The remedy is an incremental or "de-amortised" structure** that copies a few elements on every operation rather than all of them at once — trading a worse constant for a genuine per-operation worst-case bound.
>
> **The judgement to carry forward: amortised bounds are about throughput; worst-case bounds are about latency.** Both are legitimate; using the wrong one is how a system passes benchmarks and fails in production.

## 📝 Summary

- **An array's $O(1)$ indexing is address arithmetic**: $\text{start}+k\times\text{cell size}$. Every array complexity claim traces back to this.
- **Python lists are *referential*** — they store fixed-size pointers, not objects. Hence uniform cells, shallow copies, cheap `[None]*n`, and the aliasing rules of [[01 - Python and Object-Oriented Foundations|ch. 01]] explained at the storage level. **`array.array` and NumPy use *compact* arrays instead**, which is why they use far less memory.
- **A dynamic array keeps spare capacity** and, when full, allocates a bigger array and copies. `append` is $O(1)$ in the common case and $O(n)$ on a resize.
- **Amortised cost = total cost of $n$ operations ÷ $n$.** It is a **worst-case guarantee about sequences**, strictly stronger than an average-case claim because it assumes nothing about the input distribution.
- **`append` is amortised $O(1)$ under doubling**, because total copying is $1+2+4+\cdots<2n$ by the geometric sum. *(Measured: always under $2n$ — 1.02$n$ to 1.64$n$.)*
- **The banker's argument:** charge 3 tokens per append — one to write, two banked — and the bank always covers the next resize.
- **Amortised is NOT average.** Measured over 200 000 appends, the slowest was **5 084× the mean** — and the total was still linear. **Amortised bounds are for throughput, not latency.**
- **Growing by a constant is $\Theta(n^2)$ regardless of the constant**, since $\sum ic=\Theta(n^2)$; the constant changes the coefficient, never the exponent. *(Measured: 9 999 copies per append at $n=20\,000$.)* **Any factor $>1$ works and gives total $<\frac{r}{r-1}n$.**
- **The growth factor trades time against space:** doubling wastes up to 50% and resizes $\lg n$ times; CPython's ≈1.125 wastes ~11% and resizes ~5.9$\lg n$ times. Both amortised $O(1)$.
- **List operation costs** (measured, 100 000 elements): indexing 18 ns, `append` 25 ns, `pop()` 28 ns — versus **`pop(0)` 9.3 μs and `insert(0,x)` 54 μs**, both $O(n)$, and `x in L` up to 618 μs.
- **A list is an excellent stack and a terrible queue.** Both stack operations act at the end, in spare capacity; a queue must act at both ends, and the front of an array cannot move without shifting everything. **Use `collections.deque`** — [[05 - Stacks, Queues and Deques|ch. 05]].
- **Confirmed by doubling:** `append` ratios 2.26, 2.59, 1.99 (linear total); `insert(0,·)` ratios 4.04, 4.11, 4.01 (quadratic total).

## ⚠️ Important Notes

1. **`list.insert(0, x)` and `list.pop(0)` are $O(n)$.** They look like single operations and shift the entire array. This is the commonest Python performance bug, and it turns a loop into $O(n^2)$.
2. **Never use a list as a queue.** Use `collections.deque`, which is $O(1)$ at both ends.
3. **A list *is* the right stack.** `append` and `pop()` at the end are both $O(1)$ amortised with good locality.
4. **Amortised is a worst-case bound on a sequence, not an average.** It requires no assumption about input distribution, which makes it stronger than an average-case claim — and it says nothing about any individual operation.
5. **Do not rely on amortised bounds when latency matters.** The measured worst single append was 0.5 ms; in a real-time loop that is a missed deadline. **Ask whether you need throughput or tail latency.**
6. **The growth must be geometric.** Any factor $>1$ gives amortised $O(1)$; any constant increment gives $\Theta(n^2)$ no matter how large the increment.
7. **`sys.getsizeof(L)` measures the pointer array only**, not the objects referenced. A list of large objects is far bigger than `getsizeof` suggests.
8. **Prefer `array.array` or NumPy for large homogeneous numeric data.** A referential list of a million ints carries a million pointers plus a million objects.
9. **Preallocate when the size is known.** `[None]*n` then assigning by index avoids all resizing — worth it in a hot loop, pointless otherwise.
10. **Building a list by `+=` in a loop can be $O(n^2)$** if it creates a new list each time. Use `append`, or `extend`, or a comprehension.
11. **Slicing copies.** `L[a:b]` is $\Theta(b-a)$ and allocates. In a loop — or a recursion ([[03 - Recursion|ch. 03]] Exercise 2) — that silently adds a factor of $n$.
12. **`x in L` is $O(n)$ and its cost depends on position.** Time the miss (or late hit), not the early hit, or you will measure the wrong thing.
13. **Resizes happen at predictable points** — powers of two for doubling — so latency spikes are reproducible, not random. That is useful when profiling.
14. **The amortised argument depends on never shrinking eagerly.** A structure that halves capacity as soon as it is half empty can be forced to resize on alternate operations, destroying the bound. Real implementations shrink only at a lower threshold (typically 1/4).
15. **Contiguity buys locality as well as $O(1)$ indexing.** That advantage is invisible to asymptotic analysis and shows up in measurement — the point [[06 - Linked Lists|ch. 06]] will make by comparison.

> [!warning] Gaps in the source material
> **Goodrich's ch. 5 prose extracts cleanly** — the discussion of referential arrays, compact arrays, dynamic arrays and the amortised argument all came through readably, including his geometric-series proof.
>
> **His code did not**, per the standing problem in `00-Index.md`. **`DynamicArray` is my own implementation** of the design his prose describes (including the `ctypes.py_object` trick for a raw array, which is his), **and it was executed** — verified for correct length, indexing, `IndexError` on out-of-range access, and instrumented to count resizes.
>
> **Every measurement in this chapter is my own**, taken for these notes: the `sys.getsizeof` growth-point experiment revealing CPython's ≈1.125 factor; resize counts and total copies at four sizes; the constant-growth comparison; the `append` and `insert(0,·)` doubling tests; the per-operation timing table; and **the individual-append spike measurement (5 084×)**, which is the chapter's most useful single number and has no counterpart in either book.
>
> **All figures are images and are lost**, including Goodrich's diagrams of array memory layout, the referential-array illustration showing pointers into an object pool, and the step-by-step resize pictures. **§1's address formula and §2's instrumented code compensate**, and the `getsizeof` experiment arguably shows the growth strategy more convincingly than a diagram — but the memory-layout picture is a real loss for a reader meeting pointers for the first time.
>
> **No error was found in Goodrich ch. 5.** His $<2n$ bound on total copying was confirmed at four sizes, and his claim that CPython over-allocates geometrically was confirmed directly.
>
> **Additions beyond the source.** **The "amortised is not average" measurement is mine and is the chapter's centrepiece** — Goodrich proves the amortised bound and does not exhibit the spikes it conceals, yet the 5 084× ratio is exactly what a practitioner needs to know before trusting the bound in a latency-sensitive setting. The **banker's/accounting argument** (three tokens per append) is the standard alternative proof and is my addition; Goodrich gives only the geometric one. **The growth-factor trade-off table** (§4, and Exercise 5(c)) with the general bound $\frac{r}{r-1}n$, the analysis of **why CPython chose ≈1.125**, and the **de-amortisation** discussion in Exercise 5(e) are all mine. **The measured operation-cost table (§5) is my own**, as is the identification of list-as-queue as "the single most common Python performance bug" and the explanation grounding it in memory layout. Note 14 (**shrinking eagerly destroys the amortised bound**) is an addition, and it is a subtlety that bites anyone implementing a shrinking dynamic array.
>
> **Deliberately compressed.** Goodrich §5.4 (efficiency of Python's sequence types, with its extensive tables) is condensed into §5's measured table — **measuring the operations was preferred to transcribing his figures**, since the numbers are machine-dependent and the *ratios* are what transfer. **§5.5 (case studies: high scores, insertion sort, Caesar cipher) is omitted** — insertion sort belongs to [[11 - Sorting and Selection|ch. 11]] where it can be compared properly, and the other two are applications rather than structures. **§5.6 (multidimensional lists)** is reduced to the `[[0]*n]*m` warning already made in [[01 - Python and Object-Oriented Foundations|ch. 01]], now explained at the pointer level in Exercise 1(c).

**Previous:** [[03 - Recursion]] · **Next:** [[05 - Stacks, Queues and Deques]]
