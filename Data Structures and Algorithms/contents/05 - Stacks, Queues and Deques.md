---
subject: Data Structures and Algorithms
chapter: 5
tags: [ds, dsa, stack, queue, deque, circular-buffer, adt, lifo, fifo]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 6; Lambert, *Fundamentals of Python: Data Structures*, ch. 7–8"
---

# Stacks, Queues and Deques

Three ADTs, and they differ only in **which end you may touch**. That sounds trivial and it is not: the restriction is the point. A stack is useful *because* you cannot reach into the middle, and the discipline it imposes is what makes it the right model for function calls, undo histories and expression parsing.

This is also the first chapter where [[01 - Python and Object-Oriented Foundations|ch. 01]]'s ADT/implementation split does visible work. Each ADT below is a short contract; each has an obvious implementation that is wrong; and the fix for the queue — **the circular buffer** — is the first genuinely clever data structure in the subject.

## 📘 Main Knowledge

### 1. The stack ADT

> [!note] Definition
> A **stack** is a collection with **last-in, first-out (LIFO)** access.
>
> | Operation | Meaning |
> |---|---|
> | `push(e)` | add `e` to the top |
> | `pop()` | remove and return the top element |
> | `top()` | return the top without removing it |
> | `is_empty()`, `len()` | queries |

**A Python list is already an ideal stack**, for the reason [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]] established: `append` and `pop()` both act at the **end**, where spare capacity lives, so both are $O(1)$ amortised.

```python
class Empty(Exception):
    """Error attempting to access an element from an empty container."""
    pass


class ArrayStack:
    """LIFO stack implementation using a Python list as underlying storage."""

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, e):
        self._data.append(e)                    # O(1) amortised

    def top(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data[-1]

    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data.pop()                 # O(1) amortised
```

*(Verified: pushing 5, 3, 7 gives length 3 and top 7; popping returns `[7, 3, 5]` — the reverse of insertion; popping an empty stack raises `Empty`.)*

> [!note] Why wrap a list at all, when a list already does this?
> Three reasons, and they are the standard argument for any ADT wrapper:
> 1. **The interface states the intent.** A variable of type `ArrayStack` cannot be indexed or sliced by accident. **The restriction is the feature.**
> 2. **The vocabulary matches the problem.** `push`/`pop`/`top` reads as stack code; `append`/`pop`/`[-1]` reads as list code that happens to be used as a stack.
> 3. **The implementation is free to change.** A linked implementation ([[06 - Linked Lists|ch. 06]]) can be swapped in without touching any caller.
>
> **Note the custom `Empty` exception.** Python's list raises `IndexError` on `pop()` from empty — which is correct for a *list* and wrong for a *stack*, where there is no index involved. **Raising an exception that names the actual error is part of honouring the abstraction.**

> [!example]- The classic application: matching delimiters (verified)
> ```python
> def is_matched(expr):
>     """Return True if all delimiters in expr are properly matched."""
>     lefty, righty = '({[', ')}]'
>     S = ArrayStack()
>     for c in expr:
>         if c in lefty:
>             S.push(c)                              # opening: remember it
>         elif c in righty:
>             if S.is_empty():
>                 return False                       # nothing to match
>             if righty.index(c) != lefty.index(S.pop()):
>                 return False                       # wrong type of closer
>     return S.is_empty()                            # all opened were closed
> ```
>
> | input | result |
> |---|---|
> | `()(()){([()])}` | `True` |
> | `)(()){([()])}` | `False` — closer with nothing open |
> | `({[])}` | `False` — closer of the wrong type |
> | `(` | `False` — never closed |
> | `` (empty) | `True` — vacuously matched |
> | `[]{}()` | `True` |
>
> *(All verified, including the three edge cases.)*
>
> **A stack is the right structure because delimiters nest**, and nesting is LIFO: the most recently opened must be the first closed. **This is the same insight that makes a stack the right model for function calls** — the most recent call returns first, which is why [[03 - Recursion|ch. 03]]'s call stack is called that.
>
> **Note the final `return S.is_empty()`, not `return True`.** Forgetting it accepts `(` — an easy bug, and exactly the case a test suite must include.

### 2. The queue ADT — and why the obvious implementation is wrong

> [!note] Definition
> A **queue** is a collection with **first-in, first-out (FIFO)** access.
>
> | Operation | Meaning |
> |---|---|
> | `enqueue(e)` | add `e` to the back |
> | `dequeue()` | remove and return the front element |
> | `first()` | return the front without removing it |

The obvious implementation uses a list, appending at the back and popping from the front:

```python
def dequeue(self):
    return self._data.pop(0)        # WRONG: O(n)
```

**[[04 - Array-Based Sequences and Amortised Analysis|Ch. 04]] §5 already showed why this fails:** `pop(0)` shifts every remaining element left, so it is $O(n)$, and $n$ dequeues cost $\Theta(n^2)$.

> [!note] The idea that fixes it: don't move the data, move the *front index*
> Keep an array plus an index `_front` marking where the queue begins. Dequeuing just **advances the index** — no shifting.
>
> That alone would leak space: the front marches rightwards and the space behind it is abandoned. **The fix is to let the queue wrap around**, treating the array as a circle:
> $$\texttt{front} \leftarrow (\texttt{front} + 1) \bmod \texttt{capacity}$$
>
> **This is the circular buffer, and the modular arithmetic is [[Discrete Mathematics/contents/05 - Number Theory and Cryptography|DM ch. 05]]'s `mod` doing structural work** rather than number theory.

```python
class ArrayQueue:
    """FIFO queue implementation using a Python list as a circular buffer."""

    DEFAULT_CAPACITY = 10

    def __init__(self):
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._data[self._front]

    def dequeue(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None                    # help garbage collection
        self._front = (self._front + 1) % len(self._data) # THE circular step
        self._size -= 1
        if 0 < self._size < len(self._data) // 4:         # shrink when very empty
            self._resize(len(self._data) // 2)
        return answer

    def enqueue(self, e):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))             # double, as in ch. 04
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

    def _resize(self, cap):
        old = self._data
        self._data = [None] * cap
        walk = self._front
        for k in range(self._size):                       # realign: front -> index 0
            self._data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self._front = 0
```

*(Verified: enqueuing 5, 3, 7 gives length 3, `first()` = 5, and dequeuing returns `[5, 3, 7]` — the **same** order as insertion, unlike the stack.)*

> [!example]- Proving the wraparound actually happens (verified)
> Enqueue 0–7, dequeue six, then enqueue six more. The new elements must physically wrap past the end of the array:
> ```
> front index = 6,  capacity = 10,  size = 8
> contents in order: [6, 7, 100, 101, 102, 103, 104, 105]
> ```
> **The front sits at index 6 and eight elements are stored in a ten-slot array** — so elements occupy indices 6, 7, then wrap to 0, 1, 2, 3, 4, 5. **And they still come out in the right order.**
>
> **This is the test that matters** for a circular buffer, because a straight-line implementation that never wraps will pass every simple test and fail here. *(Testing the wrap explicitly is the analogue of [[01 - Python and Object-Oriented Foundations|ch. 01]]'s edge-case rule: empty, one element, and — for a circular structure — **wrapped**.)*

**Three details in that code are easy to get wrong and worth naming:**

1. **`self._data[self._front] = None` on dequeue.** Without it the array keeps a reference to a dequeued object, preventing garbage collection — a genuine memory leak in a long-running queue. **The slot is logically empty; make it physically empty too.**
2. **`_resize` realigns the front to index 0.** Copying the raw array would preserve a wrapped layout in the new, larger array, corrupting the order. **The walk uses modular arithmetic against the *old* capacity.**
3. **Shrinking at $\tfrac14$, not $\tfrac12$.** [[04 - Array-Based Sequences and Amortised Analysis|Ch. 04]] Note 14: shrinking as soon as the array is half empty allows an alternating enqueue/dequeue sequence to resize on every operation, destroying the amortised bound. **The gap between the growth and shrink thresholds is what makes it safe.**

> [!example]- Measured: the fix is asymptotic, not cosmetic (verified)
> $n$ enqueues followed by $n$ dequeues:
>
> | | $n=5000$ | $n=10\,000$ | $n=20\,000$ | $n=40\,000$ |
> |---|---|---|---|---|
> | list with `pop(0)` | 0.0020 s | 0.0052 s (×2.63) | 0.0179 s (×3.43) | 0.0656 s (×**3.66**) |
> | `ArrayQueue` (circular) | 0.0023 s | 0.0050 s (×2.14) | 0.0099 s (×1.98) | 0.0191 s (×**1.92**) |
>
> **The circular version's ratios sit at 2 — linear total. The list version's climb toward 4 — quadratic total.**
>
> *(The naive ratios reach only 3.66 rather than a clean 4 because `list.pop(0)` is implemented as a C `memmove`, so its constant is very small and lower-order terms still matter at these sizes. **Push $n$ higher and it converges on 4** — the asymptotic claim is about the trend, and the trend is unmistakable.)*

### 3. The deque ADT

> [!note] Definition
> A **double-ended queue** (deque, "deck") allows insertion and removal at **both** ends: `add_first`, `add_last`, `delete_first`, `delete_last`, `first`, `last`.

A deque generalises both previous ADTs — use one end and it is a stack, use both in FIFO fashion and it is a queue. The circular-buffer technique of §2 extends directly: adding at the front is
$$\texttt{front} \leftarrow (\texttt{front} - 1) \bmod \texttt{capacity}$$

**Python ships one: `collections.deque`**, implemented as a doubly-linked list of fixed-size blocks — so $O(1)$ at both ends, with better locality than a pure linked list.

```python
from collections import deque

D = deque()
D.append(1)          # add at the right
D.append(2)
D.appendleft(0)      # add at the left
# list(D) -> [0, 1, 2]
D.pop()              # -> 2
D.popleft()          # -> 0
```

*(Verified.)*

> [!example]- `deque` versus `list` at the front — and why the gap *grows* (verified)
> | $n$ | `list.insert(0, x)` | `deque.appendleft` | speed-up |
> |---|---|---|---|
> | 10 000 | 0.0204 s | 0.00044 s | **46×** |
> | 20 000 | 0.0858 s | 0.00112 s | **77×** |
> | 40 000 | 0.3421 s | 0.00199 s | **172×** |
>
> **The speed-up is not constant — it roughly doubles as $n$ doubles.** That is the signature of an *asymptotic* difference rather than a constant-factor one: $O(n)$ per operation against $O(1)$, so the ratio grows like $n$.
>
> **This is the practical lesson of [[02 - Algorithm Analysis in Practice|ch. 02]] §4 in a single table.** A constant-factor gap (13% for a comprehension versus a loop) stays 13% forever. An asymptotic gap widens without limit — 172× at forty thousand elements, and worse at four hundred thousand.

### 4. Choosing among the three

| Need | Use | Why |
|---|---|---|
| LIFO | `list` (as a stack) or `ArrayStack` | `append`/`pop` are $O(1)$ amortised |
| FIFO | **`collections.deque`** | $O(1)$ both ends; never `list.pop(0)` |
| Both ends | `collections.deque` | what it is for |
| Fixed capacity, must not grow | circular buffer (§2) | bounded memory, $O(1)$ operations |

> [!note] Where these ADTs actually appear
> - **Stack:** the call stack ([[03 - Recursion|ch. 03]] §4); undo/redo; expression parsing and the RPN evaluation of [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]] §6; **depth-first search** ([[13 - Graph Algorithms|ch. 13]]); backtracking.
> - **Queue:** scheduling and buffering; producer/consumer pipelines; **breadth-first search** ([[13 - Graph Algorithms|ch. 13]]); the level-order traversal of [[07 - Trees and Traversals|ch. 07]].
> - **Deque:** sliding-window algorithms; work-stealing schedulers; a bounded history buffer (`deque(maxlen=n)` discards from the far end automatically).
>
> **The BFS/DFS pair is the sharpest illustration of why the ADT matters.** The two algorithms are *the same code* with one substitution — a queue explores level by level, a stack explores deep first. **The data structure chooses the algorithm.**

## ✏️ Exercises

**1. (Stack ADT.)** (a) List the operations and their complexities. (b) Implement a stack over a Python list. (c) Why raise a custom `Empty` rather than letting `IndexError` propagate? (d) Give three applications and say what makes each LIFO.

> [!example]- Solution
> **(a)**
>
> | Operation | Complexity |
> |---|---|
> | `push(e)` | $O(1)$ amortised |
> | `pop()` | $O(1)$ amortised |
> | `top()` | $O(1)$ |
> | `len()`, `is_empty()` | $O(1)$ |
>
> **All amortised, not worst-case** — a `push` triggering a resize is $O(n)$ ([[04 - Array-Based Sequences and Amortised Analysis|ch. 04]] §3).
>
> **(b)** §1's `ArrayStack`. *(Verified: LIFO order `[7, 3, 5]` from pushes 5, 3, 7.)*
>
> **(c) Because `IndexError` describes the implementation, not the error.** A stack has no indices — the caller never supplied one — so `IndexError` leaks the fact that a list is inside and is actively confusing. `Empty('Stack is empty')` names what actually went wrong.
>
> **This is encapsulation applied to failures**, and it is the part people forget: the *exceptions* a class raises are as much a part of its interface as its methods. If you later swap in a linked implementation ([[06 - Linked Lists|ch. 06]]), an `IndexError` would no longer even be possible — so any caller catching it would silently break.
>
> **(d)**
> 1. **The call stack.** The most recent call must return before its caller resumes — [[03 - Recursion|ch. 03]] §4. Frames are pushed on call and popped on return.
> 2. **Undo history.** The last action taken is the first undone. (Redo is a second stack.)
> 3. **Matching delimiters / parsing.** Nesting is inherently LIFO: the innermost open bracket must close first (§1).
>
> **The common structure: nested lifetimes.** Whenever things are opened and closed and the nesting must be respected, a stack is the right model — and if it *isn't* LIFO, a stack will silently accept malformed input.

**2. (Queue.)** (a) Why is `list.pop(0)` unacceptable? (b) Explain the circular buffer. (c) Implement it. (d) Design a test that would catch a version that fails to wrap around.

> [!example]- Solution
> **(a)** `pop(0)` removes the element at index 0 and then **shifts every remaining element one position left**, because an array's elements must stay at consecutive addresses ([[04 - Array-Based Sequences and Amortised Analysis|ch. 04]] §1). That is $\Theta(n)$ per dequeue and $\Theta(n^2)$ for $n$ of them.
>
> *(Measured: ratios 2.63, 3.43, 3.66 climbing toward 4 — quadratic. The circular version stayed at ~2.)*
>
> **(b)** Keep the array fixed and **move an index instead of the data**. `_front` records where the queue begins; dequeuing advances it. To reuse the space left behind, indices wrap:
> $$\texttt{front} \leftarrow (\texttt{front}+1)\bmod\texttt{capacity},\qquad \texttt{next free} = (\texttt{front}+\texttt{size})\bmod\texttt{capacity}$$
> **The array is treated as a circle**, so the queue occupies a contiguous arc that rotates. Both ends are then $O(1)$.
>
> **(c)** §2's `ArrayQueue`. *(Verified: FIFO order preserved; `Empty` on underflow; wraparound correct.)*
>
> **(d) The test must force the queue to straddle the end of the array.** A test that only enqueues and dequeues a few items at the start of a fresh queue will never wrap, and **a broken implementation using plain `+1` instead of modular arithmetic will pass it.**
>
> The test used here:
> ```
> enqueue 0..7          # fills indices 0-7
> dequeue six times     # front now at index 6
> enqueue 100..105      # MUST wrap to indices 0-5
> ```
> ```
> front index = 6, capacity = 10, size = 8
> contents in order: [6, 7, 100, 101, 102, 103, 104, 105]
> ```
> *(Verified.)* **Eight elements in a ten-slot array with the front at index 6 can only be stored by wrapping**, and the retrieval order proves the arithmetic is right.
>
> **The general principle: test the structural invariant, not just the interface.** For a circular buffer the invariant is that the arc may straddle the array end; for a dynamic array it is resizing ([[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]); for a tree it will be rebalancing ([[10 - Search Trees|ch. 10]]). **Each needs a test that deliberately provokes it.**

**3. (Implementation details.)** In `ArrayQueue`, explain why: (a) `dequeue` sets the vacated slot to `None`; (b) `_resize` realigns the front to index 0; (c) shrinking happens at $\tfrac14$ capacity rather than $\tfrac12$.

> [!example]- Solution
> **(a) To release the reference and allow garbage collection.**
>
> Python lists hold **references** ([[04 - Array-Based Sequences and Amortised Analysis|ch. 04]] §1). If the slot keeps pointing at a dequeued object, that object cannot be reclaimed even though the queue has logically discarded it. In a long-running queue processing large objects this is **a genuine memory leak** — the queue's memory grows to the high-water mark of everything it has ever held.
>
> Setting `None` costs one assignment and makes the slot physically as empty as it is logically. *(The same reasoning applies to any container that "removes" by moving an index.)*
>
> **(b) Because a wrapped layout is meaningless in a differently-sized array.**
>
> Suppose the queue occupies indices 6, 7, 0, 1 of a 10-slot array (front at 6). Copying the raw array into a 20-slot one preserves those positions — but now `(front + size) % 20` computes a completely different location, and the order is destroyed.
>
> `_resize` therefore **walks the queue in logical order** using modular arithmetic against the **old** capacity, writing into positions $0,1,2,\dots$ of the new array, and sets `_front = 0`. **After a resize the queue is always unwrapped**, which is both correct and easier to reason about.
>
> **This is the standard bug in hand-written circular buffers**, and it only manifests when a resize happens while wrapped — a state that requires a specific sequence to reach.
>
> **(c) To preserve the amortised bound against alternating operations.**
>
> Suppose the queue shrank whenever it fell to half capacity. Sit at exactly the boundary and alternate `enqueue`/`dequeue`: each enqueue triggers a doubling ($O(n)$), each dequeue triggers a halving ($O(n)$). **Every operation is $O(n)$ and the amortised bound collapses.**
>
> With growth at full capacity and shrinkage at one quarter, there is a **hysteresis gap**: after a resize the queue is at half the new capacity, so $\Omega(n)$ further operations are needed before either threshold is reached again. That work pays for the resize, and $O(1)$ amortised survives.
>
> **The general rule for any resizing structure: the grow and shrink thresholds must not be adjacent.** [[04 - Array-Based Sequences and Amortised Analysis|Ch. 04]] Note 14 states it; this is the concrete instance.

**4. (Deque.)** (a) Give the deque operations. (b) Why is `collections.deque` preferred to a list for a queue? (c) Interpret the measured speed-ups 46×, 77×, 172×. (d) When would you still choose a list?

> [!example]- Solution
> **(a)** `add_first`, `add_last`, `delete_first`, `delete_last`, `first`, `last`, plus `len`/`is_empty` — all $O(1)$. In Python: `appendleft`, `append`, `popleft`, `pop`, `D[0]`, `D[-1]`.
>
> **(b) Because a list is $O(n)$ at the front and a deque is $O(1)$ at both ends.** `collections.deque` is a doubly-linked list of fixed-size blocks, so neither end requires shifting; the block structure also gives far better memory locality than a node-per-element linked list ([[06 - Linked Lists|ch. 06]]).
>
> **(c) The speed-up grows roughly in proportion to $n$ — doubling as $n$ doubles (46 → 77 → 172).**
>
> **That growth is the whole point.** A *constant-factor* advantage would show the same ratio at every size. A ratio that scales with $n$ means the two operations are in **different complexity classes**: $O(n)$ against $O(1)$, so the ratio is itself $\Theta(n)$.
>
> Extrapolating, at $n=400\,000$ the gap would be roughly 1700×. **This is [[02 - Algorithm Analysis in Practice|ch. 02]] §4's rule made concrete — you cannot optimise your way out of a wrong complexity class, and the penalty compounds.**
>
> **(d) When you need what a list gives and a deque does not:**
> 1. **$O(1)$ random access.** `deque[k]` is $O(k)$ — you must walk to it. If you index into the middle, use a list.
> 2. **Slicing.** `D[2:5]` raises `TypeError`; deques do not support slice syntax.
> 3. **Pure stack use.** A list is at least as fast for `append`/`pop` and is the more familiar type.
> 4. **Interoperation.** Many APIs expect a list; converting costs $O(n)$.
>
> **The decision rule: does anything happen at the front?** If yes, `deque`. If everything happens at the end or by index, `list`.

**5. (Hard — the ADT idea.)** (a) Why define an ADT when the built-in type already does the job? (b) Show that BFS and DFS differ only by the ADT used. (c) What does that say about the relationship between data structures and algorithms? (d) When is an ADT wrapper *not* worth it?

> [!example]- Solution
> **(a) Four reasons, in increasing order of importance:**
> 1. **Vocabulary.** `push`/`pop` states the intent; `append`/`pop` merely permits it.
> 2. **Restriction as a guarantee.** An `ArrayStack` *cannot* be indexed into. That prevents a class of bugs by construction rather than by discipline.
> 3. **Substitutability.** The implementation can change — array to linked, in-memory to on-disk — without touching callers. **This is the whole reason later chapters can present several implementations of one ADT and compare them.**
> 4. **Honest failure modes.** The exceptions are part of the interface; `Empty` survives a change of implementation where `IndexError` would not.
>
> **(b)** Graph traversal, in both forms:
> ```python
> def traverse(graph, start, container):
>     seen = {start}
>     container.add(start)
>     order = []
>     while container:
>         v = container.remove()          # <- the ONLY difference
>         order.append(v)
>         for w in graph[v]:
>             if w not in seen:
>                 seen.add(w)
>                 container.add(w)
>     return order
> ```
> - **`container` is a queue (FIFO)** → vertices leave in the order discovered → **breadth-first search**, exploring level by level.
> - **`container` is a stack (LIFO)** → the most recently discovered leaves first → **depth-first search**, plunging along one path.
>
> **Identical code, identical bookkeeping; the traversal order is chosen entirely by the ADT.** *(Developed properly in [[13 - Graph Algorithms|ch. 13]].)*
>
> **(c) That the boundary between "data structure" and "algorithm" is not where it appears to be.**
>
> Three readings of the same observation:
> - **The container encodes the strategy.** "Which vertex next?" is a policy question, and the ADT *is* the policy. Swap it and you have a different algorithm with a different name, different complexity characteristics and different applications.
> - **Generalising the container generalises the algorithm.** Replace the container with a **priority queue** ([[08 - Priority Queues and Heaps|ch. 08]]) and the same skeleton becomes **Dijkstra's algorithm** — "next" now means "cheapest known". Three famous algorithms, one loop, three containers.
> - **Hence the ADT/implementation split is not bureaucracy.** It lets you state the algorithm once and choose the behaviour separately.
>
> **This is why the subject is called *Data Structures and Algorithms* rather than treating them as two subjects.** [[Discrete Mathematics/contents/08 - Graph Theory|DM ch. 08]] proves things about graphs; here the choice of container decides what you *do* with one.
>
> **(d) When the abstraction costs more than it buys.** Concretely:
> 1. **Throwaway or local code.** A five-line script using a list as a stack does not need a class; the wrapper is noise.
> 2. **When the overhead matters.** Every `push` is an extra Python method call — real overhead in a hot loop. A list's `append` is a C-level call. **Measure before wrapping something in an inner loop.**
> 3. **When the built-in *is* the ADT.** `collections.deque` already presents exactly the deque interface with $O(1)$ operations; wrapping it adds a layer and removes nothing dangerous.
> 4. **When you need the wider interface.** If callers legitimately need indexing as well as stack discipline, forcing them through `push`/`pop` means they will reach for `._data` — and an encapsulation everyone bypasses is worse than none.
>
> **The judgement: wrap when the restriction prevents real errors or the implementation might genuinely change.** Otherwise use the built-in and name the variable well — `stack = []` communicates most of what `ArrayStack()` does, at no cost.

## 📝 Summary

- **Three ADTs differing only in which end may be touched.** The restriction is the feature: it prevents errors by construction and states intent.
- **Stack — LIFO:** `push`, `pop`, `top`. **A Python list is an ideal stack** because both operations act at the end, where [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]'s spare capacity is; both are $O(1)$ amortised.
- **Delimiter matching is the canonical stack application**, because nesting is LIFO — and the same insight explains why function calls use a *stack*.
- **Queue — FIFO:** `enqueue`, `dequeue`, `first`. **`list.pop(0)` is $O(n)$** and makes $n$ dequeues $\Theta(n^2)$ *(measured ratios climbing toward 4)*.
- **The circular buffer is the fix: move the front *index*, not the data**, with $\texttt{front}\leftarrow(\texttt{front}+1)\bmod\texttt{capacity}$ so abandoned space is reused. All operations $O(1)$ amortised *(measured ratios ≈2 — linear total)*.
- **Three details that are easy to get wrong:** blank the vacated slot (or leak memory); **realign the front to 0 on resize** (or corrupt a wrapped layout); and **shrink at $\tfrac14$, not $\tfrac12$** (or an alternating sequence destroys the amortised bound).
- **Test the structural invariant.** A circular buffer must be tested in a *wrapped* state — a version using `+1` instead of `mod` passes every naive test.
- **Deque — both ends, $O(1)$.** `collections.deque` is a linked list of blocks. Against `list.insert(0,·)` the measured speed-up was **46× → 77× → 172×**, roughly doubling with $n$ — **the signature of an asymptotic gap, not a constant one.**
- **Use a list for a stack, a `deque` for a queue.** Choose a list only when you need $O(1)$ indexing or slicing, which a deque does not provide.
- **BFS and DFS are the same code with a different container** — queue versus stack — and swapping in a priority queue gives Dijkstra. **The ADT chooses the algorithm**, which is why the two halves of this subject's name belong together.

## ⚠️ Important Notes

1. **Never use `list.pop(0)` for a queue.** It is $O(n)$ and makes the whole loop quadratic. Use `collections.deque`.
2. **A list *is* the right stack.** Do not reach for a deque out of caution; `append`/`pop` are optimal and more idiomatic.
3. **Raise an exception that names the abstraction's error.** `Empty`, not `IndexError` — the latter leaks the implementation and will become impossible if the implementation changes.
4. **In `is_matched`, remember the final `is_empty()` check.** Returning `True` at the end accepts unclosed openers like `(`.
5. **Blank the slot when dequeuing from an array-backed queue.** Otherwise the container holds references to logically-removed objects and leaks memory.
6. **Realign the front on resize.** Copying a wrapped array verbatim into a bigger one silently corrupts the order, and only under a specific enqueue/dequeue sequence.
7. **Keep grow and shrink thresholds apart** (double at full, halve at a quarter). Adjacent thresholds let an alternating workload resize on every operation.
8. **Test the wrapped state deliberately.** Enqueue past the end, dequeue past the front, and resize while wrapped — three states a naive test never reaches.
9. **`deque[k]` is $O(k)$, not $O(1)$.** A deque is not a random-access structure, and it does not support slicing.
10. **`deque(maxlen=n)` gives a bounded history for free**, discarding from the opposite end automatically — ideal for sliding windows and rolling logs.
11. **A speed-up that grows with $n$ signals a complexity difference; a constant one signals a constant factor.** 46× → 172× as $n$ quadrupled is the former, and no micro-optimisation will close it.
12. **`ArrayQueue.DEFAULT_CAPACITY` is a class attribute, not an instance one** — shared by all instances and referenced as `ArrayQueue.DEFAULT_CAPACITY`. A mutable class attribute would be the [[01 - Python and Object-Oriented Foundations|ch. 01]] shared-default bug at class scope.
13. **Wrap a built-in in an ADT when the restriction prevents errors or the implementation may change** — not reflexively. In a hot loop the extra method call is a measurable cost.
14. **When an algorithm's behaviour depends on "which item next", the container is the decision.** Recognising that turns three algorithms into one skeleton.

> [!warning] Gaps in the source material
> **Goodrich's ch. 6 prose extracts cleanly** — the ADT definitions, the circular-buffer discussion and the delimiter-matching application all came through readably.
>
> **His code did not**, per the standing problem in `00-Index.md`. **`ArrayStack`, `ArrayQueue` and `is_matched` are my own implementations** of the designs his prose describes — including his `DEFAULT_CAPACITY = 10`, the `Empty` exception, the shrink-at-one-quarter rule and the realigning `_resize`, all of which are recoverable from the surviving text. **Every one was executed**, and tested on the edge cases: empty container, single element, underflow, and — for the queue — **the wrapped state**.
>
> **Every measurement is my own:** the naive-versus-circular queue comparison across four sizes, and the `deque`/`list` front-insertion table. As always the absolute times are machine-specific and **the ratios are the transferable content.**
>
> **All figures are images and are lost.** The significant loss here is **Goodrich's circular-buffer diagrams** — the pictures of the queue as an arc rotating around an array, and of the front index advancing past the end and wrapping. **§2's wraparound experiment substitutes for them**, and printing `front index = 6, capacity = 10, size = 8` alongside the correct retrieval order arguably demonstrates the invariant better than a static picture; but the loss is real for a first encounter. Also lost: the diagrams of the delimiter-matching stack evolving through an expression.
>
> **No error was found in Goodrich ch. 6.**
>
> **Additions beyond the source.** **The measured comparisons are mine** — Goodrich states that `pop(0)` is $O(n)$ and does not demonstrate it, and the growing 46×→77×→172× speed-up (with the observation that a *growing* ratio signals an asymptotic rather than constant-factor difference) is the clearest evidence in the chapter. **The explicit wraparound test and the argument that one must test the structural invariant** is my own framing. The three implementation details of §2 are collected and explained here as a group; Goodrich mentions the `None` assignment and the realignment in passing and does not explain the **hysteresis** reason for shrinking at one quarter, which Exercise 3(c) works out. **Exercise 5(b)–(c) — that BFS and DFS are one algorithm distinguished only by the container, and that substituting a priority queue yields Dijkstra — is mine**, and is the chapter's main conceptual addition; Goodrich introduces these ADTs and defers all three algorithms to later chapters without drawing the connection. Exercise 5(d) (**when an ADT wrapper is not worth it**) is an addition, since the books present abstraction as an unqualified good.
>
> **Deliberately compressed.** Goodrich §6.1.3's further stack applications (reversing a file, HTML tag matching) are omitted as further instances of the same pattern. **§6.2.3 (queue implementations compared) is folded into §4's decision table.** His §6.3's full `ArrayDeque` implementation is **not reproduced** — it is the circular buffer of §2 with a symmetric front operation, and `collections.deque` is what one should actually use; §3 states the extension and moves on.

**Previous:** [[04 - Array-Based Sequences and Amortised Analysis]] · **Next:** [[06 - Linked Lists]]
