---
subject: Data Structures and Algorithms
chapter: 6
tags: [ds, dsa, linked-lists, singly-linked, doubly-linked, sentinels, slots, locality]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 7; Lambert, *Fundamentals of Python: Data Structures*, ch. 4, 9"
---

# Linked Lists

[[04 - Array-Based Sequences and Amortised Analysis|Chapter 04]] ended with a diagnosis: an array's elements sit at consecutive addresses, so **inserting or deleting anywhere but the end requires physically moving data.** That is the source of `insert(0, x)`'s $O(n)$ cost, and no amount of cleverness inside an array fixes it.

**The linked list is the alternative: give up contiguity.** Store each element in its own node carrying a reference to the next, and insertion becomes a pointer update — $O(1)$, regardless of position. Naturally, something is lost: without contiguity there is no address arithmetic, so **indexing degrades from $O(1)$ to $O(n)$.**

This chapter builds three linked structures and then **measures the trade-off in both directions**, which is the only way to make the comparison honest.

## 📘 Main Knowledge

### 1. The singly linked list

A **node** holds an element and a reference to the next node. The list keeps a reference to the **head**; the last node's `next` is `None`.

```python
class LinkedStack:
    """LIFO stack implementation using a singly linked list for storage."""

    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node."""
        __slots__ = '_element', '_next'          # streamline memory usage

        def __init__(self, element, next):
            self._element = element
            self._next = next

    def __init__(self):
        self._head = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def push(self, e):
        self._head = self._Node(e, self._head)   # new node points at the old head
        self._size += 1

    def top(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._head._element

    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        answer = self._head._element
        self._head = self._head._next            # the old head becomes garbage
        self._size -= 1
        return answer
```

*(Verified: pushing 5, 3, 7 gives length 3 and top 7; popping yields `[7, 3, 5]`; popping empty raises `Empty`.)*

**`push` is the whole idea in one line.** `self._Node(e, self._head)` creates a node whose `next` is the current head, then rebinds the head. **No data moves and nothing is copied** — which is why it is $O(1)$ regardless of the list's length.

> [!note] `__slots__` — a small declaration with a large effect
> By default every Python object carries a `__dict__` for its attributes, which is flexible and costly. **`__slots__` replaces it with a fixed array of named fields.**
>
> *(Measured, per node:)*
>
> | | bytes |
> |---|---|
> | `_Node` **with** `__slots__` | **48** |
> | node **without** `__slots__` | 48 + 296 (`__dict__`) = **344** |
>
> **A factor of about 7.** For a structure that allocates one object per element, this is not a micro-optimisation — it is the difference between a linked list being usable and being absurd. **Any node class should declare `__slots__`.**

> [!example]- The singly linked queue, and the two special cases (verified)
> A stack only touches one end. A queue needs both — so keep a **tail** reference as well, making `enqueue` $O(1)$ instead of $O(n)$.
>
> ```python
> class LinkedQueue:
>     """FIFO queue implementation using a singly linked list."""
>
>     def __init__(self):
>         self._head = None
>         self._tail = None
>         self._size = 0
>
>     def enqueue(self, e):
>         newest = self._Node(e, None)             # will be the new tail
>         if self.is_empty():
>             self._head = newest                  # SPECIAL CASE: was empty
>         else:
>             self._tail._next = newest
>         self._tail = newest
>         self._size += 1
>
>     def dequeue(self):
>         if self.is_empty():
>             raise Empty('Queue is empty')
>         answer = self._head._element
>         self._head = self._head._next
>         self._size -= 1
>         if self.is_empty():
>             self._tail = None                    # SPECIAL CASE: became empty
>         return answer
> ```
> *(Verified: FIFO order `[5, 3, 7]` preserved; and after emptying, a further `enqueue` works correctly — confirming the tail was reset.)*
>
> **The two `if` statements are the point.** An empty list has no node for the tail to point at, so both boundary transitions need special handling. **Forgetting the second one is the classic bug**: the tail keeps pointing at a removed node, and the next `enqueue` attaches to garbage. It only manifests after the queue empties and refills — which is why the test above does exactly that.
>
> **Why a *tail* pointer is not enough for a doubly-ended structure:** you can enqueue at the tail in $O(1)$, but you cannot *delete* the tail in $O(1)$, because finding its predecessor requires walking from the head. That is what §2 fixes.

### 2. Doubly linked lists and sentinels

Each node now carries `_prev` as well as `_next`, so from any node you can move in either direction — and **delete it in $O(1)$**, since both neighbours are reachable.

The classic annoyance with linked lists is boundary cases: inserting at the head, deleting the tail, operating on an empty list. **Sentinels remove them all.**

> [!note] Sentinel nodes
> Keep two dummy nodes — a **header** and a **trailer** — that hold no element and are never removed. The real elements always lie strictly between them.
>
> **Consequence: every real node has a genuine predecessor and successor.** Insertion and deletion are then uniform, with no `if` statements for boundaries at all.

```python
class _DoublyLinkedBase:
    """A base class providing a doubly linked list representation."""

    class _Node:
        __slots__ = '_element', '_prev', '_next'
        def __init__(self, e, p, n):
            self._element = e
            self._prev = p
            self._next = n

    def __init__(self):
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)
        self._header._next = self._trailer          # trailer follows header
        self._trailer._prev = self._header          # header precedes trailer
        self._size = 0

    def _insert_between(self, e, predecessor, successor):
        """Add element e between two existing nodes and return the new node."""
        newest = self._Node(e, predecessor, successor)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest

    def _delete_node(self, node):
        """Delete a nonsentinel node from the list and return its element."""
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor               # NO special cases
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        node._prev = node._next = node._element = None   # deprecate for GC
        return element
```

*(Verified via a `LinkedDeque` subclass: `insert_last(1)`, `insert_last(2)`, `insert_first(0)` gives first 0, last 2, length 3; `delete_first()` returns 0 and `delete_last()` returns 2.)*

**Compare `_delete_node` with the queue's `dequeue`.** The queue needed an `if` to reset the tail; this needs none. **Both methods are four lines with zero branches**, because the sentinels guarantee the neighbours exist.

> [!note] Two details worth copying
> **`node._prev = node._next = node._element = None`** on deletion. The node is unlinked but some caller may still hold a reference to it; blanking its fields prevents that stale reference from keeping the *rest of the list* alive. **The same garbage-collection reasoning as [[05 - Stacks, Queues and Deques|ch. 05]]'s blanked queue slot** — a removed thing should stop referring to its former neighbours.
>
> **`_insert_between` returns the new node.** A caller can hold onto it as a *position*, enabling $O(1)$ insertion and deletion at a remembered location. **This is the basis of Goodrich's `PositionalList`**, and it is what makes a linked list genuinely useful rather than merely a slower list: the $O(1)$ insert is only realisable if you already have a reference to the place.

### 3. The trade-off, measured in four dimensions

This is the chapter's real content. Neither structure dominates; here is exactly where each wins.

> [!example]- (a) Insertion at the front — linked wins, and the gap grows (verified)
> | $n$ | `list.insert(0, x)` | linked `push` | linked faster by |
> |---|---|---|---|
> | 10 000 | 0.0214 s | 0.00223 s | **10×** |
> | 20 000 | 0.0879 s | 0.00299 s | **29×** |
> | 40 000 | 0.3368 s | 0.00720 s | **47×** |
>
> **The advantage grows with $n$** — $O(n)$ against $O(1)$ per operation, so the ratio is itself $\Theta(n)$. Same signature as [[05 - Stacks, Queues and Deques|ch. 05]]'s deque comparison.

> [!example]- (b) Indexing — the array wins overwhelmingly (verified)
> 1000 accesses to the middle element of a 20 000-element structure:
>
> | | time | |
> |---|---|---|
> | `list[n//2]` | 0.000059 s | address arithmetic, $O(1)$ |
> | linked walk to position $n/2$ | 0.1546 s | follow 10 000 pointers, $O(n)$ |
> | | | **list 2 639× faster** |
>
> **This is the price of abandoning contiguity**, and it is steep. A linked list has no way to compute where the $k$th element lives; it must be walked to.

> [!example]- (c) Traversal — same complexity, and the result is a surprise (verified)
> Both are $O(n)$. Summing every element:
>
> | $n$ | list | linked | list faster by |
> |---|---|---|---|
> | 200 000 | 0.0158 s | 0.0176 s | 1.1× |
> | 400 000 | 0.0294 s | 0.0359 s | 1.2× |
>
> **Only about 15% — far less than the cache-locality argument would predict**, and this is worth understanding rather than glossing over.
>
> **The reason is [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]] §1: Python lists are *referential*.** Iterating a list of integers already means following a pointer per element to reach the `int` object. So both structures chase pointers, and the linked list's only extra cost is one more indirection per node.
>
> **In C or C++ with a contiguous array of values, the gap would be far larger** — the array traversal would touch consecutive cache lines with no indirection at all, while the linked list scattered across the heap would miss the cache repeatedly. **So "arrays win on locality" is true in general and much weaker in Python specifically**, and the measurement is what reveals that. *(It is also why NumPy exists: compact arrays restore the advantage that Python's object model gives away.)*

> [!example]- (d) Memory — the array wins, decisively (verified)
> | | bytes per element |
> |---|---|
> | Python list (pointer array only) | **8.0** |
> | linked node **with** `__slots__` | **48** |
> | linked node **without** `__slots__` | **344** |
>
> **A linked list costs at least 6× the memory of a list**, because every element needs a node object with a header, two references, and allocator overhead — versus one 8-byte pointer in an array. *(In both cases the referenced objects are extra.)*
>
> **And without `__slots__` it is 43×.** That single declaration is the difference between "expensive" and "unusable".

**Summary of the trade-off:**

| | array-based | linked |
|---|---|---|
| index by position | **$O(1)$** | $O(n)$ |
| insert/delete at a **known** position | $O(n)$ | **$O(1)$** |
| insert/delete at the end | **$O(1)$** amortised | $O(1)$ |
| insert/delete at the front | $O(n)$ | **$O(1)$** |
| memory per element | **8 bytes** | 48+ bytes |
| locality | **better** | worse |
| worst-case operation | $O(n)$ on resize | **$O(1)$**, never resizes |

> [!note] The one advantage of linked lists that is easy to miss
> **A linked list never resizes**, so its operations are $O(1)$ **worst case**, not amortised. [[04 - Array-Based Sequences and Amortised Analysis|Ch. 04]] §3 measured a single `append` spiking to **5 084× the mean** during a resize; a linked list has no such spike.
>
> **For real-time or latency-sensitive work that can be decisive** — the amortised bound is about throughput, and here is a structure that gives a genuine per-operation guarantee. It is the clearest practical case for choosing linked over array-based.

### 4. When to use which

**Use an array-based sequence** (the default) when you index, when you iterate more than you modify, when memory matters, or when you append at the end. **This covers most cases, which is why `list` is the default.**

**Use a linked structure** when you insert or delete at the front or at positions you already hold references to, when you need worst-case rather than amortised guarantees, or when you are splicing whole sublists (an $O(1)$ pointer update).

> [!warning] In Python specifically, the answer is usually "neither, use a built-in"
> `collections.deque` is a linked list of *blocks* — $O(1)$ at both ends with far better locality and memory behaviour than a node-per-element list, and implemented in C. **For a stack, queue or deque, use `list` or `deque`; do not hand-roll a linked list.**
>
> **So why build them?** Because the *technique* matters far more than the structure. The nodes-and-pointers idea is the foundation of every remaining chapter — **trees ([[07 - Trees and Traversals|ch. 07]]) are nodes with several children, heaps ([[08 - Priority Queues and Heaps|ch. 08]]) and search trees ([[10 - Search Trees|ch. 10]]) are linked structures with invariants, hash tables ([[09 - Maps, Hash Tables and Skip Lists|ch. 09]]) chain collisions with linked lists, and graphs ([[13 - Graph Algorithms|ch. 13]]) are adjacency lists.** A linked list is the simplest possible instance, which is why it is where you learn to think in pointers.

## ✏️ Exercises

**1. (Singly linked.)** (a) Implement a stack over a singly linked list. (b) Why is `push` $O(1)$? (c) Why does a linked *queue* need a tail reference, and what two special cases arise? (d) What bug appears if the tail is not reset when the queue empties, and what test catches it?

> [!example]- Solution
> **(a)** §1's `LinkedStack`. *(Verified: LIFO order, `Empty` on underflow.)*
>
> **(b) Because nothing is moved or copied.** `push` allocates one node, sets its `_next` to the current head, and rebinds `_head`. That is a constant number of operations **regardless of how many elements the list already holds** — contrast an array, where inserting at the front shifts everything.
>
> **(c)** Without a tail reference, `enqueue` must reach the last node by walking from the head — $O(n)$. Keeping `_tail` makes it $O(1)$.
>
> The two special cases both concern the empty list, which has no node for `_tail` to point at:
> 1. **`enqueue` onto an empty queue** — there is no tail to attach to, so `_head` must be set as well.
> 2. **`dequeue` emptying the queue** — `_head` becomes `None`, and `_tail` must be reset to `None` too.
>
> **(d) The bug: `_tail` still points at the removed node.** The next `enqueue` takes the `else` branch and executes `self._tail._next = newest`, attaching the new node to an **orphaned** node that is no longer part of the list. `_head` is `None`, so the queue reports itself empty while `_tail` points into garbage — and the enqueued element is unreachable and silently lost.
>
> **The test:** *fill, fully empty, then refill.*
> ```
> enqueue 5, 3, 7  ->  dequeue all three  ->  enqueue 9  ->  first() should be 9
> ```
> *(Verified: `first()` returns 9, confirming the reset.)*
>
> **A test that never empties the queue will not catch this** — which is the same lesson as [[05 - Stacks, Queues and Deques|ch. 05]]'s wraparound test. **Boundary states must be provoked deliberately**, and for a linked structure the boundary is *empty*.

**2. (Doubly linked and sentinels.)** (a) Why add a `_prev` reference? (b) What are sentinels and what do they eliminate? (c) Write `_insert_between` and `_delete_node`. (d) Why blank a deleted node's fields, and why return the new node from an insert?

> [!example]- Solution
> **(a) To make deletion $O(1)$.** In a singly linked list, deleting a node requires its **predecessor** (to re-point its `next`), and finding that predecessor means walking from the head — $O(n)$. With `_prev` the predecessor is immediately available.
>
> This is also what makes a linked *deque* possible: a tail reference lets you *add* at the end in $O(1)$, but only a `_prev` reference lets you *remove* from the end in $O(1)$.
>
> **(b) Sentinels are dummy header and trailer nodes** holding no element and never removed. Real elements always lie strictly between them.
>
> **They eliminate every boundary special case.** Because every real node has a genuine predecessor and successor:
> - inserting at the front is just inserting between `_header` and `_header._next`;
> - deleting the last element is just deleting `_trailer._prev`;
> - an empty list is simply header-pointing-at-trailer, requiring no separate treatment.
>
> **The cost is two extra nodes; the benefit is that every `if` disappears** — and boundary conditions are where linked-list bugs live.
>
> **(c)** §2's implementations. *(Verified.)* **Note that `_delete_node` contains no conditional at all** — compare §1's `dequeue`, which needed one.
>
> **(d) Blanking (`node._prev = node._next = node._element = None`):** the node is unlinked, but a caller may still hold a reference to it (as a position). If its fields still point into the list, that single stale reference keeps **the entire remaining list** alive and unreclaimable. Blanking severs it. *(Same reasoning as [[05 - Stacks, Queues and Deques|ch. 05]]'s `None`-ing of the dequeued slot.)*
>
> **Returning the new node** lets the caller keep it as a **position** — a handle to a place in the list. That is what makes $O(1)$ insertion actually usable: the bound assumes you already have a reference to the location, and without a way to obtain one you would have to walk there in $O(n)$, defeating the purpose. **This is the foundation of a positional list**, and it is the answer to "when is a linked list's $O(1)$ insert real?" — *when you kept the position from an earlier operation.*

**3. (The trade-off.)** Using the measurements: (a) where does linked win and by how much? (b) Where does the array win? (c) Explain why traversal shows only ~15% difference despite the locality argument. (d) Give the memory cost per element for each.

> [!example]- Solution
> **(a) Insertion at the front.** Measured: **10×, 29×, 47×** faster at $n=10\,000$, $20\,000$, $40\,000$.
>
> **The growing ratio is the important part** — it indicates $O(1)$ against $O(n)$, so the advantage is unbounded rather than a fixed factor. A linked list also wins on **worst-case guarantees** (never resizes) and on **splicing** whole sublists in $O(1)$.
>
> **(b) Indexing, memory, and locality.**
> - **Indexing: list 2 639× faster** for 1000 accesses to the middle of 20 000 elements — $O(1)$ address arithmetic against walking 10 000 pointers.
> - **Memory: 8 bytes/element against 48** — six times less.
> - **Traversal: ~15% faster.**
>
> **(c) Because Python lists are referential** ([[04 - Array-Based Sequences and Amortised Analysis|ch. 04]] §1). A list stores **pointers**, not values, so iterating a list of integers already dereferences one pointer per element to reach the `int` object. The linked list adds only *one further* indirection per element — from node to element — rather than replacing a contiguous scan with a scattered one.
>
> **The textbook locality argument assumes a compact array**, where traversal touches consecutive cache lines and dereferences nothing. **That is true of C arrays and NumPy, and false of Python lists** — so the expected large gap shrinks to 15%.
>
> **The honest conclusion: "arrays have better locality" is a real principle whose magnitude depends entirely on the language's memory model.** Measuring is what distinguishes the two cases, and it is why this subject insists on it.
>
> **(d)**
>
> | | bytes/element | ratio |
> |---|---|---|
> | Python list | **8.0** | 1× |
> | node with `__slots__` | **48** | 6× |
> | node without `__slots__` | **344** | **43×** |
>
> A list needs one 8-byte pointer per element. A node needs an object header, two or three references, and allocator overhead. **The `__slots__` difference (48 vs 344) is the single largest factor here** — a node class without it carries a full `__dict__`, and the structure becomes indefensible.

**4. (Choosing.)** For each, choose array-based or linked and justify: (a) storing pixels of an image for random access; (b) an undo history; (c) a queue of jobs with a hard latency deadline; (d) a playlist supporting "insert after the current track"; (e) a million floats for numerical work.

> [!example]- Solution
> **(a) Array-based.** Random access is the defining operation, and it is $O(1)$ for an array and $O(n)$ for a linked list — the 2 639× measured gap. Pixels are also fixed in number, so insertion never arises. *(For real images, NumPy: compact storage plus locality.)*
>
> **(b) Array-based — a `list` used as a stack.** Undo is LIFO ([[05 - Stacks, Queues and Deques|ch. 05]] §1), and both `append` and `pop` at the end are $O(1)$ amortised with better memory behaviour. **No front operations arise, so a linked list buys nothing.** *(If the history must be bounded, `deque(maxlen=n)` discards the oldest automatically.)*
>
> **(c) Linked — and this is the interesting one.** An array-based queue gives $O(1)$ **amortised**, but a resize is $O(n)$: [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]] measured a single append spiking to **5 084× the mean**. Under a hard deadline that one pause is a violation, however good the average.
>
> **A linked list never resizes**, so every operation is $O(1)$ **worst case**. **This is the case where amortised is the wrong guarantee**, and it is the clearest practical argument for a linked structure.
>
> **(d) Linked (doubly).** "Insert after the current track" is exactly the positional operation linked lists exist for: given a reference to the current node, insertion is $O(1)$. In an array it is $O(n)$ shifting. Doubly linked also gives "previous track" in $O(1)$, and a circular variant gives wrap-around for free.
>
> **Note this only works because you *hold* the position** — Exercise 2(d)'s point. If you had to search for the current track first, the search would dominate.
>
> **(e) Neither — use NumPy.** A Python list of a million floats costs 8 MB of pointers **plus** a million float objects (~24 bytes each, ~24 MB). A linked list would cost ~48 MB in nodes alone. **A NumPy array stores the values compactly: 8 MB total**, with full locality and vectorised operations.
>
> **The general lesson: the array/linked dichotomy is the *classical* framing, and Python adds a third option that often beats both.** Ask what the data is before assuming the choice is binary.

**5. (Hard — why study this at all?)** (a) Given that `list` and `deque` exist and are written in C, why implement linked lists? (b) What does `__slots__` do and why does it matter here? (c) Where do nodes-and-pointers reappear later? (d) When is a hand-written linked list actually the right choice in Python?

> [!example]- Solution
> **(a) Because the technique generalises far beyond the structure.**
>
> A linked list is the simplest possible instance of *"objects holding references to other objects, restructured by rebinding those references."* Learning it here — where there is one pointer and no invariant to maintain — is what makes the later structures tractable.
>
> **A secondary reason: it is where you learn to reason about boundary cases.** The tail-reset bug of Exercise 1(d) and the sentinel technique of §2 are lessons about *invariants*, and every structure ahead has harder ones.
>
> **(b) `__slots__` replaces an instance's `__dict__` with a fixed array of named fields.** Measured: **48 bytes per node with it, 344 without — a factor of 7.**
>
> **It matters here more than anywhere else because linked structures allocate one object per element.** A dictionary per node means the bookkeeping outweighs the data by an order of magnitude. **Every node class in every remaining chapter should declare `__slots__`.**
>
> *(The costs: no dynamic attributes, and no `__weakref__` unless declared — both irrelevant for a private node class, which is exactly why the technique fits.)*
>
> **(c) Everywhere.**
>
> | Structure | Linked idea |
> |---|---|
> | [[07 - Trees and Traversals\|Trees]] | a node with references to several children |
> | [[08 - Priority Queues and Heaps\|Heaps]] | a tree, usually flattened into an array |
> | [[09 - Maps, Hash Tables and Skip Lists\|Hash tables]] | **separate chaining** — a linked list per bucket |
> | [[09 - Maps, Hash Tables and Skip Lists\|Skip lists]] | linked lists at several levels with forward references |
> | [[10 - Search Trees\|Search trees]] | linked nodes plus a rebalancing invariant |
> | [[13 - Graph Algorithms\|Graphs]] | **adjacency lists** — a list of neighbours per vertex |
>
> **Every one is "nodes referencing nodes" with an added invariant.** A tree is a linked list where each node has several successors and no cycles; a search tree adds an ordering rule; a balanced tree adds a height rule. **The pointer manipulation is identical; only the invariant changes** — which is why this chapter comes before all of them.
>
> **(d) Rarely, and the honest answer is worth stating.** In Python, `list` and `collections.deque` cover almost every case and are implemented in C, so a hand-written linked list is usually **slower in absolute terms even where its complexity is better** — the measured 10–47× front-insertion win was against `list.insert(0,·)`, but `deque.appendleft` beats both.
>
> **Legitimate cases:**
> 1. **You need $O(1)$ splicing of sublists.** Moving a run of elements between lists is a pointer update; no built-in offers it.
> 2. **You need stable positions.** References into a linked list stay valid across insertions and deletions elsewhere; list indices do not. **This is the real differentiator**, and it is what a positional list provides.
> 3. **You need worst-case, not amortised, guarantees** — Exercise 4(c).
> 4. **You are building something else** — an LRU cache (a doubly linked list plus a dict, which is essentially `functools.lru_cache`), a scheduler's free list, or any structure with the invariant-plus-pointers shape.
>
> **The honest summary: implement linked lists to learn to think in pointers, use built-ins in production, and reach for a hand-written one when you need positions, splicing, or worst-case bounds.**

## 📝 Summary

- **A linked list gives up contiguity** to escape [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]'s shifting cost. Each node holds an element and a reference to the next.
- **`push` is $O(1)$** because nothing is moved — a node is allocated and one reference rebound, independent of length.
- **`__slots__` is essential for node classes: 48 bytes per node with it, 344 without** — a factor of 7, and the difference between usable and absurd.
- **A singly linked queue needs a tail reference** for $O(1)$ `enqueue`, and that creates **two special cases** — enqueuing onto empty, and dequeuing to empty. **Failing to reset the tail attaches later elements to an orphaned node**; only a fill-empty-refill test catches it.
- **Doubly linked lists add `_prev`**, making deletion $O(1)$ because the predecessor is directly reachable.
- **Sentinels (header and trailer) eliminate every boundary case** — `_delete_node` has no conditionals at all. Two wasted nodes buy uniform code, and boundaries are where linked-list bugs live.
- **Blank a deleted node's fields**, or a stale reference to it keeps the whole list alive. **Return the new node from an insert**, so callers can hold a **position** — without which $O(1)$ insertion is unusable.
- **The trade-off, measured:** front insertion **linked 10–47× faster and widening**; indexing **array 2 639× faster**; memory **8 bytes/element against 48**; traversal **array only ~15% faster**.
- **The traversal surprise is instructive: Python lists are referential**, so both structures chase pointers and the locality advantage nearly vanishes. **In C or NumPy the gap would be large** — the principle is real, its magnitude is language-dependent, and only measurement distinguishes them.
- **A linked list never resizes, so its operations are $O(1)$ worst case, not amortised.** Against [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]'s measured 5 084× append spike, that is decisive under a latency deadline.
- **In Python, prefer `list` and `collections.deque`.** Hand-write a linked structure for **stable positions, $O(1)$ splicing, or worst-case guarantees.**
- **The technique is the point.** Trees, heaps, hash-table chains, skip lists, search trees and adjacency lists are all nodes-referencing-nodes with an added invariant.

## ⚠️ Important Notes

1. **Always declare `__slots__` on a node class.** Without it each node carries a `__dict__` and costs 7× the memory.
2. **A singly linked list cannot delete its last node in $O(1)$**, even with a tail reference — finding the predecessor requires a walk. Use a doubly linked list.
3. **Reset the tail when a linked queue empties.** Otherwise the next enqueue attaches to an orphaned node and the element vanishes silently.
4. **Test fill → empty → refill.** Boundary states must be provoked deliberately; a test that never empties the structure misses an entire class of bug.
5. **Use sentinels for any non-trivial doubly linked structure.** Two dummy nodes remove every boundary conditional, and the resulting code is both shorter and correct by construction.
6. **Blank a deleted node's fields.** A caller holding the node would otherwise keep the entire list reachable.
7. **$O(1)$ insertion assumes you already hold the position.** If you must search for it, the search dominates and the advantage evaporates — this is the most-overstated claim about linked lists.
8. **Do not index a linked list in a loop.** Each access is $O(n)$, so the loop is $O(n^2)$. Iterate with a walking reference instead — the same trap as [[01 - Python and Object-Oriented Foundations|ch. 01]]'s `__getitem__` iteration fallback.
9. **Linked lists cost at least 6× the memory of a Python list**, and far more than a compact array. For large numeric data the answer is NumPy, not either classical option.
10. **The locality advantage of arrays is real but language-dependent.** Measured at only ~15% in Python because lists are referential; it would be far larger in C. **Do not quote the C figure for Python code.**
11. **A linked list's operations are worst-case $O(1)$, not amortised.** This is its most under-appreciated advantage and the strongest argument for it under real-time constraints.
12. **In Python, `collections.deque` beats a hand-written linked list** for stack, queue and deque use — it is a linked list of blocks, written in C, with better locality.
13. **A cycle in a linked list makes traversal loop forever.** When manipulating pointers, check that every path still terminates — the standard detector is Floyd's tortoise-and-hare.
14. **Draw the pointers before writing the code.** Every linked-list bug is a mis-ordered assignment; rebinding `_head` before reading `_head._next` loses the list. Sequence the updates so that nothing needed is overwritten first.

> [!warning] Gaps in the source material
> **Goodrich's ch. 7 prose extracts cleanly** — the node concept, the tail-reference discussion, the sentinel rationale and the array-versus-linked comparison all came through readably, as did his remark about `__slots__`.
>
> **His code did not**, per the standing problem in `00-Index.md`. **`LinkedStack`, `LinkedQueue`, `_DoublyLinkedBase` and `LinkedDeque` are my own implementations** of the designs his prose describes — including the nested `_Node` class with `__slots__`, the sentinel pair, and the blanking of deleted nodes, all recoverable from the surviving text. **Every one was executed**, and tested on the boundary states: empty, single element, underflow, and **fill-empty-refill** for the queue.
>
> **All measurements are my own:** the four-dimension trade-off study (front insertion, indexing, traversal, memory) and the `__slots__` comparison. **The traversal result is the one worth flagging** — I expected a large locality gap and measured only 15%, which sent me back to [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]'s referential-array fact for the explanation. **That is precisely the value of measuring rather than repeating the textbook claim**, and the corrected statement (the principle is real, its magnitude is language-dependent) is more useful than the received one.
>
> **All figures are images and are lost.** This chapter suffers more than most: **every box-and-arrow diagram** of nodes and pointers is gone — the illustrations of `push` rebinding the head, of the tail reference, of sentinels bracketing the real nodes, and of the pointer surgery in `_insert_between` and `_delete_node`. **These are how linked lists are conventionally taught**, and code plus prose is a poorer substitute than usual. Important Note 14 ("draw the pointers before writing the code") is the honest compensation: **the reader should sketch what the figures would have shown.**
>
> **No error was found in Goodrich ch. 7.**
>
> **Additions beyond the source.** **The entire four-dimension measurement study is mine** — Goodrich gives a qualitative advantages/disadvantages discussion with no numbers, and the specific findings (2 639× on indexing, 47× and growing on front insertion, 6× memory, and the 15% traversal surprise with its explanation) are the chapter's core. **The `__slots__` measurement (48 vs 344 bytes) is mine**; Goodrich recommends `__slots__` without quantifying it, and the factor of 7 is what makes the advice compelling. The observation that **a linked list's operations are worst-case rather than amortised $O(1)$**, connected back to ch. 04's measured 5 084× spike, is my own and is Exercise 4(c)'s answer. **Exercise 5(c)'s table mapping the linked idea onto every later structure** is mine, as is Exercise 5(d)'s honest assessment of when a hand-written linked list is genuinely right in Python — the books present these structures without acknowledging that `deque` usually beats them. The point in Exercise 2(d) that **$O(1)$ insertion is only real if you already hold the position** is emphasised here because it is the most overstated claim about linked lists.
>
> **Deliberately compressed.** **Goodrich §7.4 (the `PositionalList` ADT)** is not implemented in full — §2 explains the position concept and why `_insert_between` returns the node, which is the transferable idea, but the complete class with its `Position` wrapper and validation machinery is a large amount of code for a structure one would not use in Python. **§7.5 (sorting a positional list) is deferred to [[11 - Sorting and Selection|ch. 11]]**, where insertion sort can be compared against the alternatives. **§7.6 (case study: maintaining access frequencies / the move-to-front heuristic)** is omitted; it is a caching strategy better met alongside [[09 - Maps, Hash Tables and Skip Lists|ch. 09]]'s hash tables. **§7.7 (link-based vs array-based sequences)** is exactly §3–4 here, but argued with measurements rather than assertions.

**Previous:** [[05 - Stacks, Queues and Deques]] · **Next:** [[07 - Trees and Traversals]]
