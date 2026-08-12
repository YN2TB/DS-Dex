---
subject: Data Structures and Algorithms
chapter: 10
tags: [ds, dsa, search-trees, bst, avl, splay-trees, red-black-trees, b-trees, rotations, balancing]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 11 and §15.3"
---

# Search Trees

[[09 - Maps, Hash Tables and Skip Lists|Chapter 09]] ended on a warning: a hash table is $O(1)$ **expected**, its worst case is $O(n)$ and an adversary can provoke it, and it cannot answer a single ordered question. This chapter builds the alternative — structures that are $O(\log n)$ **worst case** and keep their keys in order.

The chapter has one shape. **§1 shows the binary search tree, and shows it failing** — on sorted input it degenerates into a linked list, which is both the most natural input and the worst case. Everything after that is a different answer to *"how do we stop that happening?"*:

| | strategy |
|---|---|
| **AVL** | enforce a strict height rule, rebalance immediately |
| **Splay** | don't balance at all — move each accessed key to the root |
| **Red–black** | enforce a *looser* rule, so updates are cheaper |
| **(2,4) / B-tree** | abandon binary nodes; store many keys per node |

**They all achieve $O(\log n)$.** The interest is in what each gives up to get there, and §7 shows that the choice between them is decided by the machine, not the mathematics.

## 📘 Main Knowledge

### 1. The binary search tree, and how it fails

> [!note] The binary search tree property
> For every node $x$: **all keys in $x$'s left subtree are less than $x$'s key, and all keys in its right subtree are greater.**
>
> Two consequences, both used constantly. **Search is a descent** — compare, go left or right, never backtrack — so it costs $O(h)$ where $h$ is the height. And **an inorder traversal ([[07 - Trees and Traversals|ch. 07]]) emits the keys in sorted order**, which is the ordered-query ability the hash table lacked.

**So the whole game is the height $h$.** With $n$ nodes, $h$ can be anywhere from $\lceil\lg(n+1)\rceil$ (perfectly balanced) to $n$ (a path).

**And the height depends entirely on the insertion order** — not on the keys themselves:

| insertion order ($n=2000$) | resulting height |
|---|---|
| random | **27** |
| **sorted** | **2000** |
| **reverse sorted** | **2000** |

*(Verified.)* **Sorted input produces a tree of height $n$ — every node has one child, so the "tree" is a linked list** with extra pointers. Inserting $1,2,3,\dots$ places each key to the right of everything before it.

**The cost, measured** (200 searches for the deepest key):

| $n$ | degenerate tree | ratio | random tree |
|---|---|---|---|
| 1 000 | 0.00886 s (1 000 steps) | — | 0.00010 s (height 20) |
| 2 000 | 0.01876 s (2 000 steps) | **2.12** | 0.00012 s (height 26) |
| 4 000 | 0.03696 s (4 000 steps) | **1.97** | 0.00014 s (height 26) |

**Doubling ratios of 2 — linear**, by [[02 - Algorithm Analysis in Practice|ch. 02]]'s method. The random tree is flat by comparison.

> [!warning] This is not a rare edge case — it is the *likely* case
> **The naive BST is worst exactly where real data is commonest.** Timestamps, auto-increment IDs, alphabetised names, sorted files, the output of a previous sort — all arrive in order, and all produce the linked list.
>
> **A BST that is fast in testing on shuffled data can be $O(n)$ in production**, and the symptom is a system that is fine at first and collapses as data accumulates. **Never ship an unbalanced BST.**

*(A randomly-built BST does have $O(\log n)$ expected height — about $2\ln n\approx1.39\lg n$, consistent with the measured 26–27 for $n=2000$. But that is an assumption about the *input*, and §1's table shows how easily it fails. The rest of this chapter removes the assumption.)*

### 2. Rotation — the one primitive

Every binary balancing scheme is built from one operation.

> [!note] Rotation
> A rotation moves a child above its parent while **preserving the search-tree property**:
>
> ```
>       y                x
>      / \              / \
>     x   T3    <-->   T1  y
>    / \                  / \
>   T1  T2               T2  T3
> ```
>
> Keys in $T_1$ are $<x$; keys in $T_2$ are between $x$ and $y$; keys in $T_3$ are $>y$. **The rotation relinks $T_2$ from one side to the other** — that is the only subtlety, and it is where implementations go wrong.
>
> **A rotation changes a constant number of pointers, so it is $O(1)$** — and the right rotation above **reduces the depth of everything in $T_1$ by one** while increasing $T_3$'s by one. That is how height is bought.

```python
    def _rotate_right(self, z):
        y = z.left
        z.left = y.right          # T2 changes parent -- the essential step
        y.right = z
        self._update(z); self._update(y)      # heights bottom-up: z first, then y
        return y
```

**Goodrich unifies the cases into a `restructure(x)` operation on a node, its parent and its grandparent** — a *trinode restructuring*. Relabel the three as $a,b,c$ in inorder; the result always makes $b$ the new root of the subtree with $a$ and $c$ as children. **Four configurations collapse into two implementations**: a **single rotation** when $x,y,z$ are already in a line, and a **double rotation** when $x$ is the middle key — rotate $x$ above its parent first, then above its grandparent. Either way it is $O(1)$.

### 3. AVL trees — balance by strict rule

> [!note] The height-balance property
> **For every node, the heights of its two children differ by at most 1.** A tree satisfying this is an **AVL tree** (Adelson-Velsky and Landis, 1962 — the first such structure).

Each node stores its height. After an insertion, walk back up; at the first node where the balance factor reaches $\pm2$, restructure:

```python
        b = self._balance(nd)                    # left height - right height
        if b > 1:                                # left-heavy
            if self._balance(nd.left) < 0:       # left-RIGHT: double rotation
                nd.left = self._rotate_left(nd.left)
            return self._rotate_right(nd)
        if b < -1:                               # right-heavy
            if self._balance(nd.right) > 0:      # right-LEFT: double rotation
                nd.right = self._rotate_right(nd.right)
            return self._rotate_left(nd)
```

**The result on §1's killer input:**

| $n$ (sorted input) | plain BST height | **AVL height** | $\lg n$ |
|---|---|---|---|
| 1 000 | 1 000 | **10** | 9 |
| 2 000 | 2 000 | **11** | 10 |
| 4 000 | 4 000 | **12** | 11 |
| 8 000 | 8 000 | **13** | 12 |

*(Verified, with the BST-order and height-balance invariants checked at every node after each build.)* **The pathological input now produces an essentially perfect tree** — height $\lg n + 1$.

#### Why the height is logarithmic — and the Fibonacci connection

Goodrich's Proposition 11.2 proves $h=O(\log n)$ by inverting the question: **what is the *fewest* nodes an AVL tree of height $h$ can have?** Call it $n(h)$. A minimal tree of height $h$ has a minimal subtree of height $h-1$ and another of height $h-2$ — any more balanced and it would not be minimal. So

$$n(h) = 1 + n(h-1) + n(h-2), \qquad n(1)=1,\ n(2)=2.$$

**That is a Fibonacci recurrence** — the one solved in [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]] and met empirically in [[03 - Recursion|ch. 03]].

*(Verified — it is not merely Fibonacci-*like*, it is exactly $n(h)=F_{h+2}-1$:)*

| $h$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $n(h)$ | 1 | 2 | 4 | 7 | 12 | 20 | 33 | 54 | 88 | 143 | 232 | 376 |
| $F_{h+2}-1$ | 1 | 2 | 4 | 7 | 12 | 20 | 33 | 54 | 88 | 143 | 232 | 376 |

**Since $F_k\sim\varphi^k/\sqrt5$, $n(h)$ grows like $\varphi^h$, so $h\le\log_\varphi n$:**

$$h_{\max} \;=\; \log_\varphi n \;=\; \frac{\lg n}{\lg\varphi} \;\approx\; \mathbf{1.4404\lg n}.$$

**The golden ratio decides how unbalanced an AVL tree is allowed to be.** *(Verified: for $n=10^6$, worst-case height 28.7 against $\lg n=19.9$.)* [[03 - Recursion|Ch. 03]] found $\varphi$ in the *running time* of naive Fibonacci; here it appears in the *shape* of a data structure. **Same constant, unrelated route** — and both trace back to [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]]'s characteristic equation $x^2=x+1$.

**So AVL search costs at most about $1.44\lg n$** — within 45% of a perfect tree, worst case, always.

### 4. Splay trees — no balance rule at all

> [!note] The idea
> A splay tree stores **no balance information whatsoever** — no heights, no colours. Instead, **after every access, the accessed node is rotated all the way to the root** by repeated single and double rotations. This is *splaying*.

*(Verified: with keys 50, 30, 70, 20, 40, 60, 80 inserted, `search(20)` leaves 20 at the root; `search(80)` then leaves 80 at the root; a failed `search(99)` leaves the contents intact and sorted.)*

**Splaying applies to searches too — a read restructures the tree.** That is unusual and it matters (§4.2).

**The guarantee is amortised, not worst-case.** Goodrich's Propositions 11.5–11.6: any sequence of $m$ operations costs $O(m\log n)$, so **each operation is $O(\log n)$ amortised** — an individual one may be $O(n)$. This is exactly the amortised reasoning of [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]], applied to shape rather than capacity.

**The extra property no balanced tree has** is *static optimality*: accessing entry $i$ with frequency $f(i)$ costs $O(\log(m/f(i)))$ amortised. **Frequently accessed keys become cheap** — the tree adapts to the access distribution without being told it.

#### 4.1 Does it work? Measuring node visits, not seconds

To test static optimality, I made 1% of the keys "hot" and drew accesses from a skewed distribution, then counted **nodes visited per access** — implementation-independent, unlike wall time:

| access pattern | AVL | **splay** | splay's advantage |
|---|---|---|---|
| 90% hot | 13.03 | **10.62** | 1.23× |
| **99% hot** | 14.01 | **9.26** | **1.51×** |
| uniform | **13.59** | 18.53 | 0.73× — **splay loses** |

*(Verified, $n=20\,000$, 60 000 accesses, splay allowed to adapt first.)*

**The theory is confirmed in both directions.** Under skew the splay tree visits far fewer nodes — the hot keys have migrated near the root, and at 99% skew it beats a *provably balanced* tree by half. Under uniform access it is **worse** than AVL, which is also predicted: with no pattern to exploit, splaying just churns.

#### 4.2 But it lost on the clock — and the reason is the interesting part

| | 50 000 hot-key accesses |
|---|---|
| AVL | 0.0436 s |
| splay | **0.0633 s** — 45% *slower* |
| **the same splay tree, read-only** | **0.0264 s** — the fastest of the three |

*(Verified.)*

> [!warning] The shape is excellent; the restructuring is what costs
> **The adapted splay tree is the best-shaped structure of the three** — traversed read-only it beat AVL by 1.65×, matching the node-visit count. **Yet performing the same accesses through `search()` was 2.4× slower than reading the identical tree**, because each access rotates.
>
> **So the splay tree's own maintenance costs more than the shape it maintains saves** — at least at this skew, in Python.
>
> **This has a hard engineering consequence beyond speed: a splay tree cannot be read concurrently.** Every reader mutates the tree, so readers need an exclusive write lock. **A read-only workload on a splay tree serialises completely**, while AVL, red–black and B-trees allow unlimited concurrent readers. In a multi-threaded server this alone rules splay trees out.
>
> **Splay trees remain worth knowing** — they are the simplest balanced structure to implement (no stored balance data at all), and static optimality is a genuinely remarkable property. But the measurement says: **do not reach for one by default.**

### 5. (2,4) trees — more than two children

> [!note] Definition
> A **multiway search tree** node with $d$ children stores $d-1$ keys, which separate the children's key ranges. A **(2,4) tree** additionally satisfies:
>
> - **Size property:** every internal node has **2, 3 or 4 children**.
> - **Depth property:** **all external nodes have the same depth** — the tree is perfectly balanced by construction.

The depth property looks impossible to maintain, and the trick is that **the tree grows at the root, not the leaves.**

- **Insertion** always goes into a leaf. If that leaf now has 5 children — an **overflow** — it **splits** into two nodes and the middle key is pushed up to the parent. If the parent overflows it splits too, and **if the split propagates to the root, the root splits and the tree gets one level taller everywhere at once** — which is how all leaves stay at equal depth.
- **Deletion** can cause an **underflow** (a node with only 1 child), fixed by a **transfer** from a sibling with a spare key, or by **fusing** with a sibling — possibly propagating upward.

**Height is $O(\log n)$** (Goodrich Prop. 11.8): with between 2 and 4 children per level, $2^h\le n+1\le4^h$, so $\tfrac12\lg(n+1)\le h\le\lg(n+1)$.

### 6. Red–black trees — a (2,4) tree in binary clothing

> [!note] The three properties
> A red–black tree is a BST whose nodes are coloured, satisfying:
> 1. **Root property** — the root is black.
> 2. **Red property** — a red node's children are black (**no two reds in a row**).
> 3. **Depth property** — every path from the root to a leaf passes through the **same number of black nodes** (the *black depth*).

**These are not arbitrary. A red–black tree *is* a (2,4) tree**: merge every red node into its black parent, and each black node with its 0–2 red children becomes a node with 2–4 children. **The red property caps the merge at 4; the depth property becomes the (2,4) depth property.** That correspondence is why the rules look strange and are in fact forced.

**The height bound follows** (Prop. 11.9): the shortest root–leaf path is all black, the longest alternates red and black, so **the longest path is at most twice the shortest**, giving $h\le 2\lg(n+1)$.

*(Verified — sorted input, all three properties plus BST order checked at every node:)*

| $n$ | height | black depth | $\lg n$ | bound $2\lg(n+1)$ |
|---|---|---|---|---|
| 1 000 | 17 | 10 | 10.0 | 19.9 |
| 10 000 | 24 | 13 | 13.3 | 26.6 |
| 100 000 | 31 | 17 | 16.6 | 33.2 |

**Every tree is within its bound, and comfortably taller than the AVL trees of §3** — AVL reached height 13 at $n=8\,000$ where red–black needs 24 at $n=10\,000$, nearly double. **That is the deliberate trade**, and §6.1 shows what it buys.

#### 6.1 Rebalancing work — the trade, measured

| $n$ | structure | rotations/insert | recolours/insert |
|---|---|---|---|
| 10 000 | AVL | **0.695** | — |
| 10 000 | red–black | **0.579** | 0.512 |
| 100 000 | AVL | **0.704** | — |
| 100 000 | red–black | **0.585** | 0.514 |

*(Verified, random input.)*

**Both are flat as $n$ grows tenfold — $O(1)$ rotations per insertion, confirmed.** Red–black does about **17% fewer rotations** than AVL, at the cost of recolourings, which are far cheaper (a field write, no pointer surgery).

> [!note] Which to choose
> **AVL is more rigidly balanced → shorter trees → faster lookups.** **Red–black is looser → less restructuring → faster updates.** *(Deletion sharpens this: AVL deletion may need $O(\log n)$ rotations propagating up, red–black deletion needs at most 3.)*
>
> **So: AVL for read-heavy workloads, red–black for update-heavy ones.** Red–black is the more common default — it is inside Java's `TreeMap`, C++'s `std::map`, and the Linux kernel scheduler — because most workloads mix reads and writes, and its worst case for updates is better.

### 7. B-trees — when the machine dictates the structure

Everything above assumes each node access costs the same. **On disk that is false by five orders of magnitude**: RAM responds in ~100 ns, a disk seek takes ~10 ms.

**So the cost model changes: count *block transfers*, not comparisons.** Data moves in blocks of size $B$ (typically 4 KB), and a node smaller than a block wastes the transfer.

> [!note] The B-tree
> A **B-tree of order $d$** is a multiway search tree where every internal node has between $\lceil d/2\rceil$ and $d$ children — a generalised (2,4) tree with $d$ chosen so that **one node exactly fills one disk block.** With 4 KB blocks and small keys, $d$ is in the hundreds or thousands.
>
> Insertion and deletion work exactly as in §5 — split on overflow, transfer or fuse on underflow. **Goodrich Prop. 15.2: search or update costs $O(\log_B n)$ block transfers and the tree occupies $O(n/B)$ blocks**, with every block at least half full.

**The arithmetic is the entire argument:**

| $n$ | binary tree ($B=2$) | B-tree, 100 keys/node | B-tree, 1 000 keys/node |
|---|---|---|---|
| $10^6$ | **19.93** levels | **3.00** | **2.00** |
| $10^9$ | **29.90** levels | **4.50** | **3.00** |

*(Verified.)*

**A billion records: 30 disk seeks versus 3.** At 10 ms a seek that is 0.3 s against 0.03 s — and the top levels of a B-tree stay cached, so in practice it is one or two real seeks.

> [!warning] The general lesson, and it is the biggest one in this chapter
> **All of §§3–6 are $O(\log n)$ and differ only in constants — yet changing $\log_2$ to $\log_{1000}$ changes the constant by tenfold.** The asymptotics did not improve; **the base of the logarithm did**, and that came from matching the structure to the hardware.
>
> **This is why every database index and every filesystem is a B-tree** (or its B⁺-tree variant, which stores all data in the leaves and links them for range scans) — PostgreSQL, MySQL, SQLite, NTFS, ext4. **No one uses an AVL tree on disk**, however elegant.
>
> **And the same argument now applies in RAM**, where the cache line (64 B) plays the role of the block. That is the effect [[06 - Linked Lists|ch. 06]] went looking for and measured at only ~15% — real, but much weaker in Python, whose lists hold references rather than values. **The gap between disk and RAM is $10^5$; the gap between RAM and cache is about $10^2$ — so the same reasoning applies, with a smaller payoff.**

### 8. Summary of the trade-offs

| | search | insert | delete | ordered? | notes |
|---|---|---|---|---|---|
| **hash table** ([[09 - Maps, Hash Tables and Skip Lists\|ch. 09]]) | $O(1)$ exp. | $O(1)$ exp. | $O(1)$ exp. | ✗ | $O(n)$ worst, attackable |
| **BST** | $O(n)$ | $O(n)$ | $O(n)$ | ✓ | **never use — sorted input kills it** |
| **AVL** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | ✓ | shortest trees ($1.44\lg n$); read-heavy |
| **splay** | $O(\log n)$ **amortised** | amortised | amortised | ✓ | adapts to skew; **reads mutate** |
| **red–black** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | ✓ | fewer restructures; the usual default |
| **skip list** ([[09 - Maps, Hash Tables and Skip Lists\|ch. 09]]) | $O(\log n)$ exp. | exp. | exp. | ✓ | simplest to implement |
| **B-tree** | $O(\log_B n)$ **I/O** | I/O | I/O | ✓ | **the only choice on disk** |

**In practice:** use `dict` unless you need order; use `sorted()` if you need order once; use a balanced tree if you need order maintained under updates; use a B-tree the moment the data leaves RAM.

## ✏️ Exercises

**1. (The BST and its failure.)** (a) State the BST property and its two consequences. (b) Why does sorted input produce height $n$? (c) Interpret the timing table. (d) Why is this a serious practical problem rather than a curiosity?

> [!example]- Solution
> **(a) For every node, all keys in the left subtree are smaller and all in the right subtree are larger.**
>
> **Consequence 1 — search is a descent.** At each node one comparison eliminates an entire subtree, so the cost is $O(h)$, never $O(n)$ *provided $h$ is small*.
>
> **Consequence 2 — inorder traversal yields sorted order** ([[07 - Trees and Traversals|ch. 07]]): left subtree (all smaller), node, right subtree (all larger), recursively. **This is what a hash table cannot do** and is the whole reason for the chapter. *(Verified for all three tree types in §10 of the script — BST, AVL and splay inorder traversals all equalled `sorted(data)`.)*
>
> **(b) Because each new key is larger than everything already present**, so the descent goes right at every node and the key becomes the right child of the previous one. **The result is a right-leaning path: $n$ nodes, height $n$, one child each.** Reverse-sorted input gives the mirror image. *(Verified: height 2000 for $n=2000$, both orders.)*
>
> **The tree has become a linked list** — with worse constants, since each node carries an unused pointer.
>
> **(c)**
>
> | $n$ | degenerate | ratio | random |
> |---|---|---|---|
> | 1 000 | 0.00886 s | — | 0.00010 s |
> | 2 000 | 0.01876 s | **2.12** | 0.00012 s |
> | 4 000 | 0.03696 s | **1.97** | 0.00014 s |
>
> **Doubling $n$ doubles the time — ratios 2.12 and 1.97, so the degenerate tree is $O(n)$** by [[02 - Algorithm Analysis in Practice|ch. 02]]'s method. The step counts confirm it directly: 1 000, 2 000 and 4 000 nodes visited for a single search. The random tree's times are flat (heights 20, 26, 26).
>
> **(d) Because sorted input is the normal case, not a rare one.** Auto-increment primary keys, timestamps, alphabetised names, the output of a previous sort, a rebuild from an ordered dump — all arrive sorted.
>
> **The failure mode is unusually nasty**: shuffled test data gives $O(\log n)$ and looks fine, so the bug ships. Production data arrives ordered, the structure degrades continuously as it grows, and the system slows *gradually* rather than breaking — the hardest kind of fault to attribute.
>
> **It is a stronger indictment than the hash table's worst case** ([[09 - Maps, Hash Tables and Skip Lists|ch. 09]] §7), which at least requires a deliberate adversary. **Here ordinary well-behaved data is the adversary.**

**2. (Rotations and AVL.)** (a) What does a rotation do and why is it $O(1)$? (b) Which subtree is the tricky one? (c) State the height-balance property and explain single versus double rotation. (d) Interpret the AVL-versus-BST height table.

> [!example]- Solution
> **(a) It moves a child above its parent while preserving the BST property**, reducing the depth of one subtree by 1 and increasing another's by 1. **It is $O(1)$ because it rewires a fixed number of pointers** — three or four — regardless of how large the subtrees are. The subtrees are moved *by reference*, never traversed.
>
> **That $O(1)$ is what makes balancing affordable:** rebalancing costs $O(\log n)$ only because it may rotate at each of $O(\log n)$ levels, not because any rotation is expensive.
>
> **(b) The middle subtree $T_2$** — the one holding keys between $x$ and $y$. The outer subtrees $T_1$ and $T_3$ stay attached to their nodes, but **$T_2$ must be relinked from $x$'s right to $y$'s left** (or vice versa). It is the only pointer that changes owner, and forgetting it is the classic rotation bug — one that leaves the tree looking plausible while silently losing a whole subtree.
>
> **Also easy to get wrong: heights must be recomputed bottom-up** — the demoted node first, then the promoted one, as in §2's code. Reversing the order leaves stale heights and the balance logic then misfires.
>
> **(c) Every node's two children differ in height by at most 1.**
>
> **A single rotation suffices when the three nodes are in a line** (left-left or right-right): rotating the middle one up straightens the line. **A double rotation is needed when the new node is in the middle** (left-right or right-left) — a single rotation would just move the problem to the other side. **The fix is to rotate the child first to convert the bend into a line, then rotate as usual.**
>
> Goodrich's trinode restructuring unifies all four cases: relabel $x,y,z$ as $a,b,c$ in inorder, and the answer is always "$b$ on top, $a$ and $c$ below".
>
> **The test in code is the sign of the child's balance factor** — if it disagrees with the parent's, the shape is bent and a double rotation is required.
>
> **(d)**
>
> | $n$ (sorted) | BST | AVL | $\lg n$ |
> |---|---|---|---|
> | 1 000 | 1 000 | **10** | 9 |
> | 2 000 | 2 000 | **11** | 10 |
> | 4 000 | 4 000 | **12** | 11 |
> | 8 000 | 8 000 | **13** | 12 |
>
> **On the input that destroys a plain BST, the AVL tree is essentially perfect** — height $\lg n+1$, meaning almost every level is full. **The AVL height grows by exactly 1 when $n$ doubles**, the signature of logarithmic growth.
>
> The BST column is $n$ itself. **At $n=8\,000$ the difference is 8 000 versus 13 — a factor of 615**, and it grows with $n$.
>
> *(The invariants were checked at every node after every build — BST order, the height-balance property, and the correctness of each stored height — so this is a verified AVL tree, not merely a short one.)*

**3. (Hard — the Fibonacci bound.)** (a) Why does Goodrich bound the *minimum node count* rather than the height directly? (b) Derive the recurrence. (c) The table shows $n(h)=F_{h+2}-1$ exactly — derive $1.44\lg n$ from it. (d) What does this share with [[03 - Recursion|ch. 03]]?

> [!example]- Solution
> **(a) Because "how tall can a tree with $n$ nodes be?" is awkward to attack directly, while its inverse is a clean recursive question.** If a tree of height $h$ must contain at least $n(h)$ nodes, and $n(h)$ grows exponentially in $h$, then $h$ must be logarithmic in $n$ — the bound follows by inversion.
>
> **This "bound the inverse" move is standard**, and it is the same manoeuvre as [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]] §8's sorting lower bound: don't count comparisons, count reachable leaves, then invert.
>
> **(b)** Let $n(h)$ be the fewest nodes in an AVL tree of height $h$. Such a tree has a root, and its two subtrees must be as *sparse* as possible while respecting the height-balance property. **One subtree must have height $h-1$** (or the tree would be shorter), and **the other may have height $h-2$** — one less is the most imbalance permitted. Each is itself a minimal AVL tree, so
>
> $$n(h)=1+n(h-1)+n(h-2),\qquad n(1)=1,\ n(2)=2.$$
>
> **The height-balance property enters exactly once, in "$h-2$ is the smallest allowed".** Permitting $h-3$ would give a different, slower-growing recurrence and a worse bound — which is precisely why a looser rule (red–black, §6) yields taller trees.
>
> **(c)** With the $+1$ absorbed, the recurrence is Fibonacci's. *(Verified exactly for $h=1\dots12$: 1, 2, 4, 7, 12, 20, 33, 54, 88, 143, 232, 376, matching $F_{h+2}-1$ at every $h$.)*
>
> Check the induction: $n(h)=1+n(h-1)+n(h-2)=1+(F_{h+1}-1)+(F_h-1)=F_{h+2}-1$, using $F_{h+2}=F_{h+1}+F_h$. ✓
>
> From [[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]], $F_k\sim\varphi^k/\sqrt5$ with $\varphi=(1+\sqrt5)/2$. So $n\ge n(h)\approx\varphi^{h+2}/\sqrt5$, and taking logs,
>
> $$h\;\le\;\log_\varphi n+O(1)\;=\;\frac{\lg n}{\lg\varphi}+O(1)\;\approx\;\mathbf{1.4404\lg n}.$$
>
> **So an AVL tree is never worse than about 44% taller than a perfect tree.** *(Verified: for $n=10^6$, at most 28.7 against $\lg n=19.9$.)*
>
> **And the bound is tight** — the minimal trees achieving it are the *Fibonacci trees*, built by joining minimal trees of heights $h-1$ and $h-2$. *(Verified: height 11 requires exactly 232 nodes, and $1.4404\lg 232=11.32$ — the bound is met, not merely respected.)*
>
> **(d) The same constant $\varphi$, reached by a completely different route.** [[03 - Recursion|Ch. 03]] found it in *time*: naive Fibonacci makes $\varphi^n$ calls, predicted ratio $\varphi^2=2.618$ per two steps, **measured 2.51 / 2.55 / 2.70**. Here it appears in *space* — the shape a data structure is permitted to take.
>
> **Both come from the same source: the recurrence $x_k=x_{k-1}+x_{k-2}$ and its characteristic equation $x^2=x+1$**, whose positive root is $\varphi$ ([[Discrete Mathematics/contents/07 - Recurrence Relations|DM ch. 07]]).
>
> **The lesson is that the recurrence, not the subject matter, determines the constant.** "Each thing depends on the previous two" produces $\varphi$ whether the things are call counts or subtree heights — which is why recurrences are worth solving in general rather than case by case.

**4. (Splay trees — reading a negative result.)** (a) How do splay trees differ in *kind* from AVL? (b) What is static optimality, and did the node-visit measurement confirm it? (c) Splay lost on wall-clock time — reconcile that with (b). (d) When would you use one?

> [!example]- Solution
> **(a) They store no balance information and enforce no invariant.** AVL keeps a height per node and restores the height-balance property after every update; a splay tree keeps nothing and **simply rotates each accessed node to the root.**
>
> **Three consequences.** The guarantee weakens from **worst-case** to **amortised** $O(\log n)$ — an individual operation can be $O(n)$. The implementation gets much simpler — no balance factors, no case analysis. And, uniquely, **searches mutate the structure**.
>
> **(b) Static optimality (Prop. 11.6): accessing a key of frequency $f(i)$ costs $O(\log(m/f(i)))$ amortised** — hot keys become cheap automatically. No balanced tree does this; AVL is oblivious to how often a key is used.
>
> **Confirmed, in both directions:**
>
> | pattern | AVL | splay |
> |---|---|---|
> | 90% hot | 13.03 | **10.62** |
> | 99% hot | 14.01 | **9.26** |
> | uniform | **13.59** | 18.53 |
>
> **At 99% skew the splay tree visits 34% fewer nodes than a provably balanced tree** — it has found a shape AVL is not allowed to have, because AVL must balance by key structure while splay balances by *use*. **And it is worse under uniform access**, also as predicted: with no pattern to exploit, splaying only churns.
>
> **I measured node visits rather than seconds deliberately** — my splay search is recursive and my AVL search iterative, so a wall-clock comparison would have measured my coding style.
>
> **(c) The shape is genuinely better; maintaining it costs more than it saves.**
>
> | | 50 000 hot accesses |
> |---|---|
> | AVL | 0.0436 s |
> | splay via `search()` | 0.0633 s |
> | **the same splay tree, read-only** | **0.0264 s** |
>
> **The third row settles it.** Traversing the adapted splay tree without rotating is **1.65× faster than AVL** — exactly what the node-visit count predicts. **The identical accesses through `search()` cost 2.4× more than that**, and the difference is purely the rotations.
>
> **So (b) and (c) are both true and not in tension**: the splay tree wins on nodes visited and loses on work per visit, and here the second effect is the larger.
>
> **This is the ch. 08 pattern again** — a textbook-correct claim ($O(n)$ heapify beating $O(n\log n)$ insertion) that measurement complicates. **The asymptotic claim is right; the constants decide the outcome.**
>
> **(d) Rarely, and never by default.**
>
> **Reasons to:** the access pattern is strongly skewed *and* stable; you want a balanced structure with the least code (no stored balance data at all); the working set matters more than the total size — a splay tree keeps the hot set near the root automatically, which suits caches.
>
> **Reasons not to, in order of severity:**
> 1. **Reads mutate, so concurrent reads are impossible.** Every reader needs a write lock; a read-only workload serialises completely. **AVL, red–black and B-trees allow unlimited concurrent readers.** In a multi-threaded server this is disqualifying on its own.
> 2. **No worst-case guarantee** — only amortised, so tail latency is unbounded per operation.
> 3. **Measured slower even on its own favourable pattern** (c).
> 4. Uniform access is actively worse than a balanced tree.
>
> **Verdict: a beautiful idea and an important one theoretically, but red–black or a skip list is the better default.**

**5. (Hard — red–black trees and B-trees.)** (a) State the three properties and explain why they are not arbitrary. (b) Derive $h\le2\lg(n+1)$ and check it against the data. (c) Interpret the rotation counts; when would you prefer AVL? (d) Why do B-trees exist when everything here is already $O(\log n)$?

> [!example]- Solution
> **(a) Root black; a red node's children are black; every root-to-leaf path has the same number of black nodes.**
>
> **They are not arbitrary — a red–black tree is a (2,4) tree drawn in binary form.** Merge each red node into its black parent: a black node with 0, 1 or 2 red children becomes a multiway node with 2, 3 or 4 children.
>
> Under that correspondence:
> - **The red property caps the merge at 4 children** — two reds in a row would produce a 5-way node, violating the (2,4) size property.
> - **The depth property becomes the (2,4) depth property** — exactly one black node contributes to each merged node, so equal black depth means all leaves at equal multiway depth.
> - **The root property is a normalisation** that makes the top of the tree well defined.
>
> **So the rules are the (2,4) invariants re-expressed for binary nodes**, which is why they look arbitrary until you see the correspondence and forced afterwards. Red–black trees get (2,4) balance without variable-size nodes.
>
> **(b)** Let $b$ be the black depth. **The shortest possible root–leaf path is all black**, so it has $b$ nodes. **The longest possible alternates red and black** — the red property forbids two reds in a row, so a path is at most half red — giving at most $2b$ nodes. Hence $h\le 2b$.
>
> The all-black skeleton is a tree of black depth $b$ in which every leaf is at depth $b$, so it contains at least $2^b-1$ nodes, giving $n\ge 2^b-1$, i.e. $b\le\lg(n+1)$. Combining,
>
> $$h\;\le\;2b\;\le\;2\lg(n+1).$$
>
> *(Verified:)*
>
> | $n$ | height | black depth | bound |
> |---|---|---|---|
> | 1 000 | 17 | 10 | 19.9 |
> | 10 000 | 24 | 13 | 26.6 |
> | 100 000 | 31 | 17 | 33.2 |
>
> **Every tree is inside its bound and close to it** ($h/b$ is 1.7, 1.8, 1.8 — approaching the factor-2 limit), on sorted input, with all three properties verified at every node.
>
> **Compare AVL's $1.44\lg n$**: red–black trees are genuinely taller — AVL reached 13 at $n=8\,000$ where red–black needs 24 at $n=10\,000$. **The looser rule of (a) is exactly why**, and it traces to the recurrence in Exercise 3(b): a rule permitting more imbalance allows sparser trees.
>
> **(c)**
>
> | $n$ | AVL rot./insert | RB rot./insert | RB recolours/insert |
> |---|---|---|---|
> | 10 000 | 0.695 | **0.579** | 0.512 |
> | 100 000 | 0.704 | **0.585** | 0.514 |
>
> **Both are flat across a tenfold increase in $n$ — $O(1)$ rotations per insertion, confirmed empirically.** Note this is *less than one rotation per insertion on average*: most insertions need none.
>
> **Red–black does about 17% fewer rotations**, replacing them with recolourings — a colour bit written, no pointers touched, far cheaper.
>
> **Prefer AVL when reads dominate.** AVL's trees are ~40% shorter, so every lookup is cheaper; you pay in restructuring on update. **The asymmetry is sharper for deletion**, which I did not implement: AVL deletion may cascade $O(\log n)$ rotations up the tree, while **red–black deletion needs at most three**.
>
> **So: AVL for read-heavy, red–black for update-heavy or mixed** — which is most real workloads, and why red–black is the default in Java's `TreeMap`, C++'s `std::map` and the Linux kernel.
>
> **(d) Because $O(\log n)$ counts the wrong thing once data leaves RAM.**
>
> All the analysis above assumes uniform access cost. **On disk, a seek is ~10 ms against RAM's ~100 ns — a factor of $10^5$.** One node access is then not one unit of work but the *only* unit that matters, so the right cost model counts **block transfers**.
>
> Data moves in blocks of size $B$ (≈4 KB). A binary node uses a fraction of a block, wasting the transfer. **A B-tree makes one node fill one block**, giving hundreds or thousands of children per node and reducing the height to $\log_B n$:
>
> | $n$ | $B=2$ | 100 keys/node | 1 000 keys/node |
> |---|---|---|---|
> | $10^6$ | 19.93 | 3.00 | 2.00 |
> | $10^9$ | 29.90 | 4.50 | 3.00 |
>
> **A billion records: 30 seeks versus 3 — 0.3 s versus 0.03 s**, and better still in practice because the upper levels stay cached.
>
> **The conceptual point is the sharpest in the chapter.** The complexity class did not change — both are logarithmic. **What changed is the base of the logarithm**, from 2 to 1 000, and since $\log_B n=\lg n/\lg B$ that is a constant-factor improvement of $\lg B\approx 10$. **Asymptotic analysis, by design, cannot see it** — and it is the difference between a usable database and an unusable one.
>
> **Hence every database index and filesystem is a B-tree**, usually the B⁺-tree variant that stores all entries in the leaves and links them, so a range query descends once and then scans sideways. **The same reasoning now applies inside RAM**, with the 64-byte cache line as the block — the effect [[06 - Linked Lists|ch. 06]] measured at ~15% in Python, smaller because the RAM/cache gap ($10^2$) is far narrower than the disk/RAM gap ($10^5$).

## 📝 Summary

- **A BST gives $O(h)$ search and sorted inorder traversal — but $h$ depends entirely on insertion order.** *(Verified: $n=2000$ gives height 27 from random input and **2000** from sorted input.)*
- **Sorted input degenerates a BST into a linked list**, and sorted input is the *common* case (IDs, timestamps, alphabetised data). *(Measured $O(n)$: doubling ratios 2.12 and 1.97.)* **Never ship an unbalanced BST.**
- **Rotation is the single primitive** — it preserves the BST property, is $O(1)$, and the subtlety is relinking the middle subtree $T_2$. Goodrich's **trinode restructuring** unifies four cases into single and double rotations.
- **AVL trees enforce that sibling heights differ by at most 1**, restoring it with one restructure after each insertion. *(Verified on sorted input: heights 10, 11, 12, 13 for $n=1\,000$ to $8\,000$ — essentially perfect, with all invariants checked at every node.)*
- **The AVL height bound is Fibonacci.** The fewest nodes at height $h$ obeys $n(h)=1+n(h-1)+n(h-2)$, and *(verified exactly for $h\le12$)* $n(h)=F_{h+2}-1$. Hence $h\le\log_\varphi n\approx\mathbf{1.4404\lg n}$ — **the golden ratio bounds the imbalance**, the same $\varphi$ [[03 - Recursion|ch. 03]] measured in naive Fibonacci's *running time*.
- **Splay trees store no balance data at all** and move each accessed node to the root, giving $O(\log n)$ **amortised** plus **static optimality** — frequent keys become cheap.
- **Static optimality is real:** under 99% skew a splay tree visited **9.26** nodes per access against AVL's **14.01**; under uniform access it was worse (18.53 vs 13.59). *(Both verified.)*
- **Yet splay lost on the clock** (0.0633 s vs AVL's 0.0436 s) — **while the same tree read-only took 0.0264 s, the fastest of all.** The shape is excellent; the restructuring on every read costs more than it saves. **And because reads mutate, splay trees cannot be read concurrently.**
- **(2,4) trees** keep all leaves at equal depth by **splitting on overflow** and **fusing or transferring on underflow**, growing at the root so every leaf rises together.
- **A red–black tree is a (2,4) tree in binary form** — merge each red node into its parent. That correspondence is why the three properties (root black, no two reds, equal black depth) are forced rather than arbitrary.
- **Red–black height is $\le2\lg(n+1)$**: the longest path is at most twice the shortest. *(Verified: heights 17/24/31 against bounds 19.9/26.6/33.2, all properties checked.)*
- **Both do $O(1)$ rotations per insertion** *(measured flat: AVL 0.70, red–black 0.58 across a tenfold $n$)*. **AVL builds shorter trees (faster reads); red–black restructures less (faster updates)** — hence red–black in `std::map`, Java's `TreeMap` and the Linux kernel.
- **B-trees change the cost model, not the complexity class.** Counting block transfers instead of comparisons, one node per disk block gives $O(\log_B n)$ I/O. *(Verified: $10^9$ records need **29.9** levels binary vs **3.0** at 1 000 keys/node.)*
- **The base of the logarithm is the whole story** — asymptotically invisible, practically decisive. **This is why every database index is a B-tree and none is an AVL tree.**

## ⚠️ Important Notes

1. **Never use an unbalanced BST in production.** Sorted input — the common case — makes it $O(n)$, and shuffled test data hides the fault until the data grows.
2. **A BST's shape depends on insertion order, not on the key set.** The same 2 000 keys gave height 27 or 2 000. **Inserting a sorted array into a BST is the specific thing to avoid**; if you must, insert the median first and recurse.
3. **In a rotation, relink the middle subtree $T_2$.** It is the only pointer that changes owner and the classic bug — the tree still looks valid while a subtree has been lost.
4. **Update heights bottom-up after a rotation** — the demoted node before the promoted one. Reversing the order leaves stale heights and misfires the balance logic silently.
5. **A double rotation is needed exactly when the inserted node is the *middle* of the three keys.** Test the sign of the child's balance factor against the parent's; if they disagree, rotate the child first.
6. **Check the invariant, not just the output.** A tree can produce correct sorted output while being badly unbalanced or miscoloured. Every tree here was verified with a `check()` that walks the whole structure — BST order, height-balance, and all three red–black properties. **Correct answers are not evidence of a correct structure.**
7. **AVL is at most $1.44\lg n$ tall, and the bound is tight** — the Fibonacci trees attain it.
8. **Splay tree reads mutate the tree**, so they need a write lock and cannot be read concurrently. **In a multi-threaded context this alone rules them out**, regardless of speed.
9. **Splay's guarantee is amortised, not worst-case** — an individual operation can be $O(n)$. Like [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]'s `append`, that is a throughput guarantee, not a latency one.
10. **Measure the algorithm, not your coding style.** Comparing my recursive splay search to my iterative AVL search would have measured the wrong thing; **node visits are implementation-independent** and gave the opposite (correct) answer.
11. **The red–black properties are forced, not arbitrary** — they are the (2,4) invariants in binary form. Memorising them without the correspondence makes them unmemorable.
12. **AVL for read-heavy, red–black for update-heavy.** AVL trees are ~40% shorter; red–black restructures less, and its deletion needs at most 3 rotations against AVL's possible $O(\log n)$.
13. **$O(\log n)$ is not the end of the analysis.** All of §§3–6 are logarithmic and differ by factors of two to ten in practice; **B-trees improve only the base of the logarithm and that is the decisive win.**
14. **Match the structure to the memory hierarchy.** One node per block on disk; consider cache lines in RAM. **The disk/RAM gap is $10^5$ and the RAM/cache gap about $10^2$** — same argument, smaller payoff, which is exactly why [[06 - Linked Lists|ch. 06]] measured only ~15%.
15. **In Python, default to `dict`** ([[09 - Maps, Hash Tables and Skip Lists|ch. 09]]) unless order is needed; use `sorted()` for a one-off; reach for a balanced tree only when order must be *maintained under updates*. **The standard library has no balanced tree** — use `sortedcontainers` rather than writing your own.

> [!warning] Gaps in the source material
> **Goodrich's ch. 11 prose extracts well** — the rotation and trinode-restructuring description, the AVL height-balance property and Proposition 11.2's proof sketch, the splay propositions 11.5–11.6, the (2,4) size and depth properties, the red–black properties and their (2,4) correspondence, and §15.3's Proposition 15.2 all came through readably. **Goodrich page $n$ = PDF page $n+22$; ch. 11 is PDF 481–555, §15.3 is PDF 733–737.**
>
> **His code did not**, per the standing problem in `00-Index.md`, and **Lambert has no balanced-tree chapter at all** — so **every implementation here is my own**: `BST`, `AVLTree`, `SplayTree` and `RedBlackTree`, together with the `check()` routines that verify the invariants. **All were executed**, and correctness was established three ways: inorder traversal equal to `sorted()` for all structures; **full invariant checks at every node** (BST order; AVL height-balance and stored-height correctness; all three red–black properties); and edge cases — empty-tree search, single node, and duplicate-key insertion overwriting rather than inserting.
>
> **All measurements are my own**: the insertion-order height table, the degenerate-search timings, the AVL-versus-BST heights, the $n(h)$ Fibonacci table, the splay node-visit counts, the splay wall-clock comparison, the red–black height and property checks, the rotation counts, and the B-tree level arithmetic.
>
> **Every figure is an image and is lost.** This is the worst-hit chapter in the subject — **Figures 11.8 and 11.9 (rotation and the four trinode cases), 11.11 (an AVL tree with heights), the splaying step diagrams, 11.24 (a (2,4) tree), 11.30–11.32 (a red–black tree and its (2,4) correspondence)** are all diagrams, and this material is conventionally taught entirely by picture. Substitutes: §2's ASCII rotation diagram, the running code, and the verified invariant checks. **The reader should draw the four trinode cases by hand** — they are not absorbable from prose.
>
> **No error was found in Goodrich ch. 11 or §15.3.**
>
> **Additions beyond the source.** **§4.1–4.2, the splay investigation, is entirely mine and is the chapter's main original content.** Goodrich states static optimality and proves it; he does not test whether it pays. **Measuring node visits (confirming the theory: 9.26 vs 14.01 under 99% skew) and then wall-clock time (contradicting it: splay 45% slower) and then the same tree read-only (0.0264 s, the fastest of all) is my own three-stage experiment**, and the conclusion — the shape is excellent, the maintenance costs more than it saves — appears in neither book. **The observation that splay reads require a write lock and therefore cannot be concurrent** is mine and is the strongest practical argument against them. **The exact identity $n(h)=F_{h+2}-1$** is my verification; Goodrich only argues that $n(h)$ grows exponentially. **The AVL-versus-red–black rotation-count comparison** is my experiment. **The B-tree level table and the seek arithmetic** are mine; Goodrich gives the proposition but not the numbers. Note 10's methodological point, and the cross-links to [[03 - Recursion|ch. 03]]'s $\varphi$ and [[06 - Linked Lists|ch. 06]]'s locality result, are additions.
>
> **Deliberately compressed.** **Red–black *deletion* is not implemented** — only insertion. Its fix-up has four cases and roughly doubles the code, and the insertion cases already demonstrate the principle; the claim that deletion needs at most 3 rotations is therefore quoted from Goodrich, **not verified here.** **(2,4) trees are described but not implemented** (§5) — they exist in this chapter mainly to explain *why* the red–black rules take the form they do, and the B-tree of §7 is the version that matters in practice. **Goodrich's `TreeMap` inheritance hierarchy and its `_rebalance_insert`/`_rebalance_delete`/`_rebalance_access` hooks** (§11.2.1) are omitted as a Python-framework matter rather than an algorithmic one. **§§15.1–15.2 (memory management, caching) are excluded from the scope** per `00-Index.md`, with only the block-transfer cost model retained here because B-trees are incomprehensible without it. **§15.4's external-memory multiway merge-sort is deferred to [[11 - Sorting and Selection|ch. 11]].** The **splay tree's amortised proof** (Propositions 11.3–11.5, a potential-function argument) is stated but not reproduced; the technique belongs with [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]'s amortised analysis.

**Previous:** [[09 - Maps, Hash Tables and Skip Lists]] · **Next:** [[11 - Sorting and Selection]]
