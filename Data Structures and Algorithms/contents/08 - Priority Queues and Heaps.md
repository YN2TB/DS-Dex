---
subject: Data Structures and Algorithms
chapter: 8
tags: [ds, dsa, priority-queue, heap, heapify, heapsort, heapq, array-representation]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 9"
---

# Priority Queues and Heaps

A queue serves in arrival order; a **priority queue** serves in order of importance. That one change turns out to be exactly what [[13 - Graph Algorithms|Dijkstra's algorithm]] needs, what schedulers need, and what heapsort is.

The structure that implements it — the **binary heap** — is the most elegant object in this subject, for one reason: **it is a tree that needs no pointers.** [[07 - Trees and Traversals|Ch. 07]] built trees from nodes with three references each; a heap stores the same tree in a flat array, deriving parent and child positions by arithmetic. All of [[06 - Linked Lists|ch. 06]]'s memory overhead disappears.

This chapter also contains the clearest case in the subject of **measurement correcting a textbook claim** — §5.

## 📘 Main Knowledge

### 1. The priority queue ADT

> [!note] Definition
> A **priority queue** stores (key, value) pairs and serves the **smallest key** first.
>
> | Operation | Meaning |
> |---|---|
> | `add(k, v)` | insert an item with key `k` |
> | `min()` | return (not remove) the item with smallest key |
> | `remove_min()` | remove and return the item with smallest key |
> | `len()`, `is_empty()` | queries |
>
> *(This is the **min**-oriented version. A max-oriented one is identical with the comparison reversed — or store negated keys.)*

**The key is the priority; the value is the payload.** Keeping them separate matters: Dijkstra stores `(distance, vertex)`, a scheduler stores `(deadline, job)`.

**Two obvious implementations, both unsatisfactory:**

| Implementation | `add` | `remove_min` |
|---|---|---|
| unsorted list | $O(1)$ | $O(n)$ — scan for the minimum |
| sorted list | $O(n)$ — find the insertion point | $O(1)$ |

**Each makes one operation trivial and the other linear.** The heap makes both $O(\log n)$, which is the better bargain whenever you do many of each.

### 2. The binary heap

> [!note] Definition
> A **(min-)heap** is a binary tree satisfying two properties:
>
> 1. **Heap-order:** for every node other than the root, `key(node) >= key(parent)`.
> 2. **Complete:** every level is full except possibly the last, which is filled left to right.

**Heap-order is much weaker than a search-tree ordering.** It says nothing about siblings — only that every path from the root is non-decreasing. That weakness is precisely what makes the heap cheap to maintain.

**The consequence that matters: the minimum is at the root**, reachable in $O(1)$.

**And completeness bounds the height.** A complete binary tree with $n$ nodes has height exactly $\lfloor\lg n\rfloor$ — the minimum possible by [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]'s $h\ge\lg t$ bound. **A heap is balanced by construction**, needing none of the rebalancing machinery of [[10 - Search Trees|ch. 10]].

### 3. The array representation — a tree with no pointers

Because the tree is complete, its nodes can be numbered level by level, left to right, and stored in an array at those indices. Then the tree structure is pure arithmetic:

$$\texttt{parent}(j)=\left\lfloor\frac{j-1}{2}\right\rfloor,\qquad \texttt{left}(j)=2j+1,\qquad \texttt{right}(j)=2j+2$$

*(Verified: node 0's children are 1 and 2; node 3's parent is 1.)*

> [!note] Why this is such a good idea
> - **No pointers at all.** [[06 - Linked Lists|Ch. 06]] measured 48 bytes per node with `__slots__`; a heap costs one array slot — 8 bytes.
> - **Perfect locality.** The array is contiguous, so a sift walks memory that is likely already cached — the advantage [[06 - Linked Lists|ch. 06]] §3 found was muted for Python lists but is real at the machine level.
> - **Completeness is maintained for free.** Appending at the end of the array *is* adding at the next position of the last level.
>
> **This only works because the tree is complete.** A tree with gaps would waste array slots — an array representation of a degenerate tree of $n$ nodes needs $2^n$ slots. **Completeness is what makes the representation possible, and the heap-order property is weak enough to allow completeness to be preserved.**

### 4. The two operations

Both fix a single violation of heap-order by walking one path — hence $O(\log n)$.

**`add`: append at the end, then sift up.**

```python
    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            self._upheap(parent)               # recur at the new position

    def add(self, key, value):
        self._data.append((key, value))        # keeps the tree complete
        self._upheap(len(self._data) - 1)      # restore heap-order
```

**`remove_min`: swap the root with the last item, pop it, then sift down.**

```python
    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right        # must compare BOTH children
            if self._data[small_child] < self._data[j]:
                self._swap(j, small_child)
                self._downheap(small_child)

    def remove_min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty')
        self._swap(0, len(self._data) - 1)     # move min to the end
        item = self._data.pop()                # remove it -- O(1), ch. 04
        self._downheap(0)                      # restore heap-order
        return item
```

> [!warning] The two details that break a hand-written heap
> **`remove_min` must swap with the *last* element, not simply promote a child.** Promoting the smaller child leaves a gap in the middle of the array and destroys completeness. Swapping with the last element keeps the array contiguous; the displaced value is then sifted down.
>
> **`_downheap` must compare *both* children** and descend to the smaller. Descending to the left child unconditionally can place a larger key above a smaller one — the heap silently becomes invalid, and the error only surfaces much later as a wrong `min()`.

> [!example]- Verified behaviour, including edge cases
> Adding $4,5,6,15,9,7,20,8$ gives the array
> ```
> [4, 5, 6, 8, 9, 7, 20, 15]      valid heap: True      min: (4, 'D')
> ```
> **Note the array is *not* sorted** — `[4, 5, 6, 8, 9, 7, ...]` has 7 after 9. Heap-order constrains only parent–child pairs, not siblings or array order.
>
> **Repeated `remove_min` yields sorted output** *(verified)*: `4, 5, 6, 7, 8, 9, 15, 20`. That is heapsort (§6).
>
> **Edge cases** *(all verified)*: `min()` and `remove_min()` on an empty heap raise `Empty`; a single-element heap works and empties correctly; duplicates are handled — `[3,1,3,1,2]` comes out `[1,1,2,3,3]`.
>
> *(The validity check `is_valid_heap` — scanning every node against its parent — is worth writing for any heap implementation. It is the structural invariant, and [[05 - Stacks, Queues and Deques|ch. 05]] §2's lesson is that invariants must be tested directly.)*

**Complexity.** Both operations follow one root-to-leaf path, and the height is $\lfloor\lg n\rfloor$, so both are $O(\log n)$ **worst case**. `min()` is $O(1)$.

### 5. Building a heap: where measurement corrected the theory

Given $n$ items, there are two ways to build a heap.

**By repeated insertion:** $n$ calls to `add`, each $O(\log n)$ — apparently $O(n\log n)$.

**By bottom-up heapify:** put all items in the array in any order, then `_downheap` every internal node, from the last one backwards.

```python
    def _heapify(self):
        start = self._parent(len(self._data) - 1)   # the last internal node
        for j in range(start, -1, -1):              # backwards to the root
            self._downheap(j)
```

**Heapify is $O(n)$, not $O(n\log n)$** — and the reason is a sum worth seeing. Roughly $n/2$ nodes are leaves and sift 0 levels, $n/4$ sift at most 1, $n/8$ at most 2, and so on:

$$\sum_{i\ge1}\frac{n}{2^{i}}\cdot i \;=\; n\sum_{i\ge1}\frac{i}{2^{i}} \;=\; 2n$$

*(Verified for $n=2^{20}$: total sift steps $=2\,097\,130=2.00\times n$ exactly.)*

**The point is that most nodes are near the bottom and barely move.** The expensive sifts — near the root — are the rare ones.

> [!warning] But the obvious experiment shows heapify *losing*, and the reason is instructive
> Building from **random** data:
>
> | $n$ | by insertion | by heapify | |
> |---|---|---|---|
> | 100 000 | 0.0434 s | 0.0539 s | insertion **faster** |
> | 400 000 | 0.1921 s | 0.2705 s | insertion **faster** |
>
> *(Verified.)* **That contradicts the textbook claim.** Counting swaps explains why:
>
> | input | insertion swaps/element | heapify swaps/element |
> |---|---|---|
> | **random** | **1.28** | 0.74 |
> | ascending | 0.00 | 0.00 |
> | **descending** | **14.69** | **1.00** |
>
> **For random data an insertion travels barely one level on average.** The reason is the same as heapify's: a random new key most likely belongs near the bottom, and there are far more positions near the bottom than near the top. **So insertion is $O(n)$ *expected* on random input; the $O(\log n)$ per insertion is a worst case, not a typical one.**
>
> **Measuring random data therefore hides the entire difference.** On the true worst case — **descending** input, where every new key is a new minimum and must climb to the root — the theory reappears:
>
> | $n$ | insertion | heapify | |
> |---|---|---|---|
> | 50 000 | 0.1311 s | 0.0263 s | heapify **4.99×** faster |
> | 100 000 | 0.2862 s | 0.0591 s | heapify **4.84×** faster |
> | 200 000 | 0.5781 s | 0.1254 s | heapify **4.61×** faster |
>
> And the doubling test separates the classes *(verified on worst-case input)*: **insertion ratios 2.16, 2.11** (above 2 — the $\log n$ factor) against **heapify 2.13, 1.92** (at 2 — linear).
>
> **Three lessons, and they are the chapter's most valuable content.**
> 1. **"$O(n)$ beats $O(n\log n)$" is a worst-case statement.** On typical input the gap may not exist at all.
> 2. **Benchmark the worst case deliberately** — [[02 - Algorithm Analysis in Practice|ch. 02]] Note 9. Random data made the better algorithm look worse.
> 3. **Ascending input costs *zero* swaps** for a min-heap, because each new key is the largest and stays put. **The same algorithm on the same $n$ ranges from 0 to 14.69 swaps per element depending only on order** — which is why "the average case" needs a stated distribution to mean anything.

### 6. Heapsort

Build a heap, then remove the minimum repeatedly:

```python
def heapsort(seq):
    pq = HeapPriorityQueue([(x, None) for x in seq])   # O(n)
    return [pq.remove_min()[0] for _ in range(len(pq))]  # n x O(log n)
```

*(Verified against `sorted()` on: a normal list, empty, single element, all-equal, and reversed input.)*

**$O(n)$ to build plus $n\times O(\log n)$ to drain gives $\Theta(n\log n)$** — meeting [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]'s $\Omega(n\lg n)$ lower bound, so heapsort is asymptotically optimal.

**Its distinguishing property is space.** Done in place — using the input array as the heap and shrinking it — heapsort needs $O(1)$ extra memory, where merge sort needs $O(n)$. [[11 - Sorting and Selection|Ch. 11]] compares them properly.

### 7. Use `heapq`

Python's `heapq` module implements exactly this on a plain list.

```python
import heapq

hq = []
heapq.heappush(hq, item)      # add
smallest = heapq.heappop(hq)  # remove_min
heapq.heapify(existing_list)  # O(n) bottom-up, in place
heapq.nsmallest(3, data)      # the k smallest
heapq.nlargest(3, data)
```

*(Verified: `heappush`/`heappop` reproduce sorted order; `nlargest(3, [5,2,9,1,7])` = `[9,7,5]`.)*

**It is min-oriented and written in C** — *(measured: heapifying 200 000 items took 0.0057 s against our Python implementation's 0.1198 s, a **21× difference**)*.

> [!note] Two practical notes
> **For a max-heap, negate the keys** — `heapq` offers no max variant.
>
> **Push tuples `(priority, item)`**, and if items may tie on priority, include a tiebreaker: `(priority, counter, item)`. Otherwise Python compares the *items* when priorities are equal, which raises `TypeError` for objects that do not define `<`. **This bites in exactly the situation heaps are for — a scheduler with equal-priority jobs.**

### 8. What priority queues are for

- **[[13 - Graph Algorithms|Dijkstra's algorithm]]** — repeatedly extract the nearest unfinished vertex. [[05 - Stacks, Queues and Deques|Ch. 05]] Exercise 5(b) noted that BFS, DFS and Dijkstra are one algorithm distinguished by the container; **the priority queue is what makes the third one Dijkstra.**
- **Prim's algorithm** for minimum spanning trees ([[Discrete Mathematics/contents/09 - Trees|DM ch. 09]] §4 proves it correct) — extract the cheapest crossing edge.
- **Schedulers and event simulation** — process the earliest deadline or timestamp next.
- **Top-$k$ selection** — keep a heap of size $k$ and stream the data past it: $O(n\log k)$ time and $O(k)$ memory, without sorting all $n$. This is what `heapq.nlargest` does.
- **Huffman coding** ([[Discrete Mathematics/contents/09 - Trees|DM ch. 09]] §1) — repeatedly merge the two least frequent items.

## ✏️ Exercises

**1. (The ADT.)** (a) Give the priority queue operations. (b) Analyse the unsorted-list and sorted-list implementations. (c) Why is a heap preferable? (d) When would a sorted list be the better choice?

> [!example]- Solution
> **(a)** `add(k, v)`, `min()`, `remove_min()`, `len()`, `is_empty()`. Items are (key, value) pairs; the key is the priority.
>
> **(b)**
>
> | | `add` | `min` | `remove_min` |
> |---|---|---|---|
> | unsorted list | $O(1)$ — append | $O(n)$ — scan | $O(n)$ — scan, then remove |
> | sorted list | $O(n)$ — find position and shift | $O(1)$ | $O(1)$ — from the end |
> | **heap** | $O(\log n)$ | $O(1)$ | $O(\log n)$ |
>
> **(c) Because it balances the two operations.** For $n$ adds and $n$ removes:
> - unsorted: $n\cdot O(1)+n\cdot O(n)=O(n^2)$
> - sorted: $n\cdot O(n)+n\cdot O(1)=O(n^2)$
> - **heap: $n\cdot O(\log n)+n\cdot O(\log n)=O(n\log n)$**
>
> **Both list versions are quadratic; the heap is linearithmic.** Making one operation $O(1)$ at the cost of the other being $O(n)$ is a bad trade whenever both are used.
>
> **(d) When the mix is lopsided, or you need more than the ADT.** A sorted list wins if you insert rarely and remove constantly — for instance a fixed set of jobs loaded once and then drained. It also gives you what a heap cannot: **the full sorted order at any moment**, and $O(\log n)$ *search* for an arbitrary key by binary search. **A heap can find the minimum in $O(1)$ and any other element only in $O(n)$** — its ordering is too weak for search.

**2. (The heap.)** (a) State the two heap properties. (b) Why does completeness bound the height? (c) Give the index arithmetic and explain why no pointers are needed. (d) Why is heap-order weaker than a search-tree ordering, and why is that good?

> [!example]- Solution
> **(a)** **Heap-order:** every non-root node's key is $\ge$ its parent's. **Complete:** all levels full except possibly the last, filled left to right.
>
> **(b) Because a complete tree is as short as a binary tree with $n$ nodes can be.** Level $i$ holds $2^i$ nodes when full, so $h$ full levels hold $2^{h+1}-1$ nodes; a complete tree with $n$ nodes therefore has height exactly $\lfloor\lg n\rfloor$.
>
> **This is optimal**, by [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]'s bound $h\ge\lg t$. **So a heap is balanced by construction and needs no rebalancing** — the entire apparatus of [[10 - Search Trees|ch. 10]] is unnecessary here.
>
> **(c)** $\texttt{parent}(j)=\lfloor(j-1)/2\rfloor$, $\texttt{left}(j)=2j+1$, $\texttt{right}(j)=2j+2$ *(verified)*.
>
> **No pointers are needed because completeness makes the level-order numbering gap-free.** Number the nodes level by level, left to right; every index from 0 to $n-1$ is used, so the array is exactly full and navigation is arithmetic.
>
> **The saving is large:** [[06 - Linked Lists|ch. 06]] measured 48 bytes per linked node against 8 bytes for an array slot — six times less, plus contiguity.
>
> **This fails for a general tree.** An array representation of a degenerate tree of $n$ nodes would need $2^n$ slots, almost all empty. **Completeness is a precondition for the representation, not a bonus.**
>
> **(d) Heap-order constrains only parent–child pairs; a BST constrains entire subtrees.** In a heap, siblings are unrelated — the verified array `[4, 5, 6, 8, 9, 7, 20, 15]` has 7 after 9 and is a valid heap.
>
> **The weakness is exactly why it is cheap.** A single insertion or deletion violates heap-order along **one path only**, so one sift of length $\le h$ repairs it. A BST insertion can unbalance the whole tree, requiring rotations. **Heap-order is the weakest ordering that still puts the minimum at the root** — and demanding no more than you need is why the structure is fast.

**3. (Operations.)** (a) Describe `add` and `remove_min`. (b) Why must `remove_min` swap with the *last* element? (c) Why must `_downheap` compare both children? (d) Give the complexity of each operation.

> [!example]- Solution
> **(a)** **`add`**: append at the end of the array (which keeps the tree complete), then **sift up** — repeatedly swap with the parent while smaller. **`remove_min`**: swap the root with the last element, pop the last element (now the old minimum), then **sift down** from the root — repeatedly swap with the smaller child while larger.
>
> **(b) To preserve completeness.** The node that must disappear is the *last* one in the array, because removing anything else leaves a gap and the array representation requires indices $0..n-1$ to be contiguous.
>
> So the value to be removed (the root) is swapped to the end and popped in $O(1)$ ([[04 - Array-Based Sequences and Amortised Analysis|ch. 04]] — `list.pop()` from the end is cheap), and the displaced last value, now at the root, is sifted down.
>
> **The alternative — promoting the smaller child recursively — leaves a hole** wherever the promotion chain ends, breaking the index arithmetic for every subsequent node.
>
> **(c) Because descending to the wrong child can leave a smaller key below a larger one.**
>
> Suppose node $j$ holds 10 with children 8 (left) and 3 (right). Swapping with the left child puts 8 at $j$ — but 3 is still below it, and $3<8$ violates heap-order. **Swapping with the smaller child (3) guarantees the promoted key is $\le$ both former children**, so the property holds locally after the swap.
>
> **This is a silent failure.** The heap remains structurally complete and looks fine; only a later `min()` returns the wrong element. *(Which is why `is_valid_heap` — checking every node against its parent — is worth writing, and why it is used in the verification above.)*
>
> **(d)**
>
> | Operation | Complexity |
> |---|---|
> | `min()` | $O(1)$ |
> | `add` | $O(\log n)$ **worst case** |
> | `remove_min` | $O(\log n)$ worst case |
> | build by heapify | **$O(n)$** |
> | build by insertion | $O(n\log n)$ worst case, $O(n)$ expected on random input |
>
> Both sifts follow a single root-to-leaf path of length $\le\lfloor\lg n\rfloor$. **Note these are worst-case, not amortised** — the underlying `list.append` is amortised, but the sift itself is bounded.

**4. (Building a heap.)** (a) Give both construction methods and their complexities. (b) Prove heapify is $O(n)$. (c) The measurements showed insertion *beating* heapify on random data — explain. (d) What does this teach about benchmarking?

> [!example]- Solution
> **(a)** **Repeated insertion:** $n$ calls to `add`, worst case $O(n\log n)$. **Bottom-up heapify:** load the array in any order, then `_downheap` each internal node from the last backwards — $O(n)$.
>
> **(b)** A node at height $i$ above the leaves sifts down at most $i$ levels, and a complete tree has at most $n/2^{i+1}$ nodes at height $i$. So the total work is
> $$\sum_{i\ge0}\frac{n}{2^{i+1}}\cdot i \;=\; \frac n2\sum_{i\ge0}\frac{i}{2^{i}} \;=\; \frac n2\cdot 2 \;=\; n \;=\; O(n).$$
> **The series $\sum i/2^i$ converges to 2** — which is why the total is linear rather than $n\log n$. *(Verified for $n=2^{20}$: exactly $2\,097\,130$ sift steps $=2.00n$.)*
>
> **The intuition: half the nodes are leaves and never move; only the few nodes near the root can sift far.** Repeated insertion has it backwards — every new element enters at the *bottom* and may climb the whole way.
>
> **(c) Because on random input, insertion is also effectively linear.**
>
> *(Measured swaps per element at $n=100\,000$:)*
>
> | input | insertion | heapify |
> |---|---|---|
> | random | **1.28** | 0.74 |
> | descending | **14.69** | 1.00 |
>
> **A randomly chosen key almost certainly belongs near the bottom**, because a complete tree has half its nodes in the last level and three-quarters in the last two. So a random insertion sifts up about one level on average, and $n$ insertions cost $O(n)$ *expected*.
>
> **The $O(\log n)$ per insertion is a worst case**, realised when every new key is a new minimum — i.e. **descending** input. There, insertion did 14.69 swaps per element (against $\lg100\,000\approx16.6$) and heapify did 1.00, and heapify was **4.6–5.0× faster**.
>
> *(Ascending input costs **zero** swaps for a min-heap: each new key is the largest so far and stays where it lands.)*
>
> **(d) Three lessons.**
>
> 1. **Random input is not a neutral choice — it is a specific distribution, and often a favourable one.** Here it made the asymptotically worse algorithm look better.
> 2. **Benchmark the worst case deliberately** ([[02 - Algorithm Analysis in Practice|ch. 02]] Note 9). The worst case had to be *constructed* — descending order — and it was not obvious in advance which order that was.
> 3. **An asymptotic advantage may be invisible on the inputs you actually have.** If your data really is random, insertion is fine and simpler. **The theory tells you the guarantee; the measurement tells you the typical experience; you need both** — and this is the clearest example in the subject of them disagreeing.
>
> **The honest summary: heapify is better, and the reason to prefer it is the worst-case guarantee, not the typical speed.**

**5. (Hard — applications and `heapq`.)** (a) Implement heapsort and give its complexity. (b) How does it compare with merge sort? (c) Why does Dijkstra need a priority queue? (d) Find the $k$ largest of $n$ items efficiently. (e) What two traps does `heapq` set?

> [!example]- Solution
> **(a)** §6's implementation. *(Verified against `sorted()` on normal, empty, single-element, all-equal and reversed inputs.)*
>
> **$\Theta(n\log n)$:** $O(n)$ to heapify plus $n$ removals at $O(\log n)$ each. **This meets [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]'s $\Omega(n\lg n)$ lower bound, so heapsort is asymptotically optimal** among comparison sorts.
>
> **(b)**
>
> | | heapsort | merge sort |
> |---|---|---|
> | time | $\Theta(n\log n)$ worst case | $\Theta(n\log n)$ worst case |
> | **extra space** | **$O(1)$** in place | $O(n)$ |
> | stable? | **no** | **yes** |
> | locality | poor — sifts jump by factors of 2 | good — sequential merges |
>
> **Heapsort's advantage is space; merge sort's are stability and locality.** In practice merge sort (or a hybrid like Timsort) usually wins on speed despite the memory, because sequential access is far friendlier to caches than a heap's scattered index jumps. **Heapsort is chosen when memory is tight or a worst-case guarantee is required** — quicksort is faster on average but $O(n^2)$ in the worst case ([[11 - Sorting and Selection|ch. 11]]).
>
> **(c) Because Dijkstra must repeatedly ask "which unfinished vertex is nearest?"**
>
> [[05 - Stacks, Queues and Deques|Ch. 05]] Exercise 5(b) showed BFS and DFS are the same traversal skeleton differing only in the container — a queue or a stack. **Replace the container with a priority queue keyed on tentative distance and the same skeleton becomes Dijkstra**: "next" now means "cheapest known" rather than "oldest" or "newest".
>
> Without a priority queue you would scan all unfinished vertices for the minimum each round — $O(V)$ per step, $O(V^2)$ overall. With one it is $O(\log V)$ per operation, giving $O((V+E)\log V)$ — much better for sparse graphs. *(Correctness is proved in [[Discrete Mathematics/contents/08 - Graph Theory|DM ch. 08]]; the implementation is [[13 - Graph Algorithms|ch. 13]].)*
>
> **(d) Keep a min-heap of size $k$ and stream the data past it.**
> ```python
> import heapq
>
> def k_largest(data, k):
>     h = []
>     for x in data:
>         if len(h) < k:
>             heapq.heappush(h, x)
>         elif x > h[0]:                 # bigger than the smallest kept
>             heapq.heapreplace(h, x)    # pop-then-push in one sift
>     return sorted(h, reverse=True)
> ```
> **$O(n\log k)$ time and $O(k)$ space** — against $O(n\log n)$ time and $O(n)$ space for sorting everything.
>
> **The gain is largest exactly where it matters:** for $k=10$ out of $n=10^9$, sorting is impossible and this is trivial. **And it streams** — the data never needs to be held in memory at once, which is why this is the standard "top-$k$ over a large log file" solution. *(This is what `heapq.nlargest` implements; verified: `nlargest(3, [5,2,9,1,7])` = `[9,7,5]`.)*
>
> **Note the min-heap for *largest* elements**, which is initially counter-intuitive: the heap's root is the *weakest* of the current champions, so it is the one to evict.
>
> **(e) Two traps.**
>
> 1. **`heapq` is min-only.** For a max-heap, push negated keys and negate on the way out. Forgetting this yields a silently reversed priority order.
> 2. **Ties fall through to comparing the payload.** Pushing `(priority, item)` and hitting equal priorities makes Python compare the `item`s — which raises `TypeError` if they define no `<`, or worse, imposes an arbitrary order if they do.
>
> **The fix is a monotonic tiebreaker:**
> ```python
> import itertools
> counter = itertools.count()
> heapq.heappush(h, (priority, next(counter), task))
> ```
> The counter is unique and increasing, so it breaks every tie, never compares the payload, and yields FIFO order among equal priorities — usually what a scheduler wants.
>
> **This bites in precisely the situation heaps are for**: a task queue where many jobs share a priority. It is the commonest `heapq` bug in production code.

## 📝 Summary

- **A priority queue serves the smallest key first**: `add`, `min`, `remove_min`. Unsorted and sorted lists each make one operation $O(1)$ and the other $O(n)$ — **both give $O(n^2)$ for $n$ adds and $n$ removes; a heap gives $O(n\log n)$.**
- **A heap is a complete binary tree with heap-order** (every key $\ge$ its parent's). **The minimum is at the root**, and completeness forces height exactly $\lfloor\lg n\rfloor$ — optimal by [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]], so **a heap is balanced by construction**.
- **The array representation needs no pointers**: $\texttt{parent}(j)=\lfloor(j-1)/2\rfloor$, $\texttt{left}=2j+1$, $\texttt{right}=2j+2$. **8 bytes per element against [[06 - Linked Lists|ch. 06]]'s 48**, plus contiguity. It works *only* because the tree is complete.
- **Heap-order is deliberately weak** — siblings are unrelated, and the array is not sorted. That weakness is why one insertion or deletion violates it along **one path only**, repairable by a single $O(\log n)$ sift.
- **`add`:** append (preserving completeness), then sift up. **`remove_min`:** swap the root with the **last** element (to keep the array contiguous), pop, then sift down **to the smaller child**.
- **Both mistakes are silent:** promoting a child instead of swapping with the last element breaks completeness; descending to the wrong child breaks heap-order. **Write an `is_valid_heap` check and test it.**
- **Bottom-up heapify is $O(n)$**, because $\sum_{i}\frac{n}{2^{i+1}}i=n$ — most nodes are leaves that never move. *(Verified: exactly $2.00n$ sift steps at $n=2^{20}$.)*
- **⚠️ But on *random* data, insertion is also linear** — measured 1.28 swaps per element, because a random key belongs near the bottom. **The $O(\log n)$ per insertion is a worst case.** On descending input, insertion did **14.69** swaps per element against heapify's **1.00**, and heapify was **4.6–5.0× faster**.
- **So random input hid the entire difference.** Benchmark the worst case deliberately; **an asymptotic advantage can be invisible on typical data**, and the reason to prefer heapify is the guarantee, not the typical speed.
- **Heapsort** is $\Theta(n\log n)$, optimal, and **$O(1)$ extra space** — but unstable and cache-unfriendly, so merge sort usually wins in practice.
- **Use `heapq`** — 21× faster than a Python implementation. **Two traps: it is min-only (negate for max), and ties fall through to comparing the payload (add a `count()` tiebreaker).**
- **Applications:** Dijkstra and Prim, schedulers and event simulation, Huffman coding, and **top-$k$ in $O(n\log k)$ time and $O(k)$ space** by streaming past a size-$k$ heap.

## ⚠️ Important Notes

1. **A heap's array is not sorted.** Only parent–child pairs are ordered; `[4,5,6,8,9,7,20,15]` is valid. Do not read the array expecting order.
2. **A heap cannot search.** Finding an arbitrary key is $O(n)$ — the ordering is too weak. If you need search *and* priority, use a balanced BST ([[10 - Search Trees|ch. 10]]) or keep a separate index.
3. **`remove_min` must swap with the last element**, not promote a child, or the array develops a hole and the index arithmetic breaks.
4. **`_downheap` must descend to the *smaller* child.** Descending left unconditionally silently invalidates the heap.
5. **Write and run a heap-validity check.** Both errors above leave a structurally plausible array; only an invariant check catches them.
6. **Prefer heapify to repeated insertion when building from a known collection** — $O(n)$ versus $O(n\log n)$ worst case, and it is one call.
7. **Do not benchmark only on random data.** It made insertion look better than heapify here. Construct the worst case: for a min-heap built by insertion, that is **descending** input.
8. **State the distribution when quoting an average case.** The same build ranged from 0 to 14.69 swaps per element depending purely on input order.
9. **`heapq` is min-oriented.** Negate keys for a max-heap, and remember to negate back.
10. **Always add a tiebreaker to `heapq` tuples** — `(priority, next(counter), item)`. Otherwise equal priorities compare the payloads, raising `TypeError` or imposing an arbitrary order.
11. **Use `heapreplace` rather than `heappop` then `heappush`** — one sift instead of two, and it is the natural operation for a bounded top-$k$ heap.
12. **For top-$k$, use a min-heap of size $k$**, not a max-heap. The root is the weakest champion and hence the one to evict.
13. **Heapsort is not stable.** If equal elements must retain their input order, use merge sort or Timsort.
14. **A heap's $O(\log n)$ bounds are worst case, not amortised** — a genuine per-operation guarantee, unlike [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]'s dynamic array.
15. **Heapsort's poor locality costs real time** despite optimal complexity: sift indices jump by factors of two, defeating the cache. Another case where [[02 - Algorithm Analysis in Practice|ch. 02]] §4's blind spots matter.

> [!warning] Gaps in the source material
> **Goodrich's ch. 9 prose extracts cleanly** — the ADT, the two heap properties, the array-representation arithmetic, and the bottom-up heapify argument all came through readably.
>
> **His code did not**, per the standing problem in `00-Index.md`. **And Lambert has no heaps chapter at all**, so unlike ch. 05–07 there was no second source to fall back on: **`HeapPriorityQueue`, both sift operations, `_heapify`, `heapsort`, the validity checker and the instrumented swap-counting subclass are entirely my own**, written from Goodrich's prose and **all executed** — verified for the heap invariant after every construction, for sorted removal order, against `sorted()` on five input shapes, and on the edge cases (empty, single element, duplicates).
>
> **All measurements are my own**, and one of them **corrected the received account**. Goodrich states that bottom-up heapify is $O(n)$ against $O(n\log n)$ for repeated insertion, which is correct; **measuring on random data showed insertion winning**, and the swap counts explained why — a random insertion sifts about one level, so insertion is $O(n)$ *expected*. **Only on constructed worst-case (descending) input does the theoretical gap appear**, at 4.6–5.0×. **Neither book mentions this**, and it is the chapter's most useful finding: it is a concrete case where benchmarking the obvious input distribution would have led to the wrong engineering conclusion.
>
> **All figures are images and are lost** — every diagram of a heap as a tree, the sift-up and sift-down animations, and the picture relating tree positions to array indices. **The index arithmetic in §3 and the verified array dumps in §4 are the substitutes**, and printing the actual array alongside the claimed invariant is arguably more convincing than a static picture; but the tree/array correspondence is genuinely easier to see drawn, and the reader should sketch it.
>
> **No error was found in Goodrich ch. 9.**
>
> **Additions beyond the source.** **The entire §5 investigation is mine** — the random-versus-descending comparison, the swap counts, the observation that ascending input costs zero swaps, and the three benchmarking lessons. **The verification of $\sum_i i/2^i=2$ by direct computation** ($2.00n$ at $n=2^{20}$) is my addition to Goodrich's algebraic argument. **The `is_valid_heap` checker and the emphasis on testing the structural invariant** follow [[05 - Stacks, Queues and Deques|ch. 05]]'s lesson and are not in the source. **The two `heapq` traps (min-only, and ties comparing payloads) are mine** and are the commonest production bugs with this module; so is the `itertools.count()` tiebreaker idiom. **Exercise 5(d)'s streaming top-$k$** with its $O(n\log k)$/$O(k)$ analysis, and the note that a *min*-heap is used for *largest* elements, are additions. The heapsort-versus-merge-sort table including **stability and locality** is mine, as is the connection in §8 and Exercise 5(c) back to [[05 - Stacks, Queues and Deques|ch. 05]]'s "the container chooses the algorithm".
>
> **Deliberately compressed.** **Goodrich §9.5's adaptable priority queue** (supporting `update` and `remove` of arbitrary entries via location-aware tokens) is not implemented — it is a substantial apparatus, and [[13 - Graph Algorithms|ch. 13]] will use the standard "push a duplicate and skip stale entries" idiom instead, which is simpler and what real Dijkstra implementations do. **§9.4.2's in-place heapsort** is described in §6 but not implemented separately, since [[11 - Sorting and Selection|ch. 11]] compares the sorting algorithms properly. **The correctness proofs of Prim and Dijkstra are owned by [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]] and [[Discrete Mathematics/contents/08 - Graph Theory|DM ch. 08]]**, per the boundary in both indexes.

**Previous:** [[07 - Trees and Traversals]] · **Next:** [[09 - Maps, Hash Tables and Skip Lists]]
