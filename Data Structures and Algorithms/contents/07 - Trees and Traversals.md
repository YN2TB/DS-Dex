---
subject: Data Structures and Algorithms
chapter: 7
tags: [ds, dsa, trees, binary-trees, traversals, preorder, inorder, postorder, expression-trees]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 8; Lambert, *Fundamentals of Python: Data Structures*, ch. 10"
---

# Trees and Traversals

A tree is the first **non-linear** structure in this subject. Everything so far — arrays, stacks, queues, linked lists — has arranged elements in a line. A tree arranges them **hierarchically**, and that single change makes possible the $O(\log n)$ operations of [[08 - Priority Queues and Heaps|ch. 08]] and [[10 - Search Trees|ch. 10]].

[[Discrete Mathematics/contents/09 - Trees|Discrete Mathematics ch. 09]] owns the theory: the four equivalent characterisations, the $n-1$ edge count, the bound $h\ge\lg t$, and the $\Omega(n\lg n)$ sorting proof. **None of that is repeated here.** This chapter builds the structure, implements the traversals, and shows what they are for.

## 📘 Main Knowledge

### 1. Terminology

A **tree** is a set of **nodes** with a parent–child relation such that there is one **root** with no parent, and every other node has exactly one parent.

| Term | Meaning |
|---|---|
| **root** | the unique node with no parent |
| **leaf** (external) | a node with no children |
| **internal** | a node with at least one child |
| **ancestor / descendant** | reachable by repeatedly following parent / child links |
| **subtree rooted at $v$** | $v$ together with all its descendants |
| **depth of $v$** | number of ancestors of $v$ — the root has depth 0 |
| **height of $v$** | length of the longest downward path from $v$ to a leaf — a leaf has height 0 |
| **height of the tree** | height of the root |

**Depth and height point in opposite directions** — depth counts upward to the root, height counts downward to the deepest leaf. Confusing them is the standard beginner's error, and §5 shows they also have different costs to compute.

A **binary tree** is a tree in which every node has at most two children, distinguished as **left** and **right**. That distinction is part of the structure: swapping a node's only child from left to right gives a *different* binary tree.

### 2. The linked representation

Each node holds an element, a parent reference, and left/right child references — a linked structure in exactly the sense of [[06 - Linked Lists|ch. 06]], with three pointers instead of one or two.

```python
class LinkedBinaryTree:
    """Linked representation of a binary tree structure."""

    class _Node:
        __slots__ = '_element', '_parent', '_left', '_right'   # ch. 06 §1

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def num_children(self, n):
        count = 0
        if n._left is not None:
            count += 1
        if n._right is not None:
            count += 1
        return count

    def children(self, n):
        """Generate the children of node n (left before right)."""
        if n._left is not None:
            yield n._left
        if n._right is not None:
            yield n._right

    def is_leaf(self, n):
        return self.num_children(n) == 0

    def add_root(self, e):
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._root

    def add_left(self, n, e):
        if n._left is not None:
            raise ValueError('Left child exists')
        self._size += 1
        n._left = self._Node(e, n)
        return n._left

    def add_right(self, n, e):
        if n._right is not None:
            raise ValueError('Right child exists')
        self._size += 1
        n._right = self._Node(e, n)
        return n._right
```

**Note `add_*` returns the new node** — [[06 - Linked Lists|ch. 06]] §2's position idea, and here it is essential: without a reference to a node you cannot attach children to it.

**The parent reference is optional but useful.** It makes `depth` and "move upward" possible without a search, at the cost of one more pointer per node. [[08 - Priority Queues and Heaps|Ch. 08]] will show a representation that needs no pointers at all.

### 3. The four traversals

A **traversal** visits every node exactly once. Three are defined by *when the root is visited relative to its subtrees*; the fourth ignores subtrees entirely and works level by level.

| Traversal | Order | Implemented with |
|---|---|---|
| **preorder** | **root**, left, right | recursion |
| **inorder** | left, **root**, right | recursion (binary trees only) |
| **postorder** | left, right, **root** | recursion |
| **breadth-first** | level by level, top to bottom | **a queue** |

```python
    def preorder(self, n=None):
        if n is None:
            n = self._root
        if n is not None:
            yield n._element                      # root FIRST
            for c in self.children(n):
                yield from self.preorder(c)

    def postorder(self, n=None):
        if n is None:
            n = self._root
        if n is not None:
            for c in self.children(n):
                yield from self.postorder(c)
            yield n._element                      # root LAST

    def breadthfirst(self):
        """Level-order traversal, using a queue."""
        if self._root is None:
            return
        q = deque([self._root])                   # ch. 05
        while q:
            n = q.popleft()
            yield n._element
            for c in self.children(n):
                q.append(c)
```

*(Inorder is the same shape with the `yield` between the two recursive calls.)*

> [!example]- Verified on a concrete tree
> ```
>         A
>        / \
>       B   C
>      / \   \
>     D   E   F
> ```
> | traversal | output |
> |---|---|
> | preorder | `A B D E C F` |
> | inorder | `D B E A C F` |
> | postorder | `D E B F C A` |
> | breadth-first | `A B C D E F` |
>
> *(All verified. Structure checks: size 6, height 2, `depth(D)` = 2, `depth(A)` = 0, `is_leaf(D)` = True, `num_children(C)` = 1.)*
>
> **These are exactly the outputs computed independently in [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]] §6 for the same tree** — theory and implementation agreeing across two subjects.

> [!note] The traversals are **generators**, and that matters
> Each is a generator ([[01 - Python and Object-Oriented Foundations|ch. 01]] §4), so they are **lazy**:
> ```
> g = T.preorder()          -> <generator object ...>
> next(g), next(g)          -> 'A', 'B'      <- the rest is never computed
> ```
> *(Verified.)*
>
> **Three consequences.** Searching a tree can stop as soon as the target is found, without traversing the rest. Memory is $O(h)$ for the recursion rather than $O(n)$ for a materialised list. And traversals compose — `filter(pred, T.preorder())` streams.
>
> **This is why [[01 - Python and Object-Oriented Foundations|ch. 01]] §4 said tree traversals are naturally generators**: "produce the elements one at a time in this order" *is* the definition of both.

**Complexity: all four are $\Theta(n)$** — each node is visited once and constant work is done per node. Space differs: the recursive traversals use $O(h)$ stack, the breadth-first one uses $O(w)$ queue where $w$ is the maximum width. **For a balanced tree $h=O(\log n)$ but $w=O(n)$**, so breadth-first can use far more memory — a genuine consideration for wide trees.

### 4. Which traversal to use

The choice is not stylistic; each answers a different kind of question.

| Use | Traversal | Because |
|---|---|---|
| copy or serialise a tree | **preorder** | the root is emitted before its subtrees, so a reader can rebuild top-down |
| print a directory listing | **preorder** | the folder appears before its contents |
| **compute a value from subtrees** | **postorder** | children are finished before the parent needs them |
| delete or free a tree | **postorder** | children are released before the parent |
| **read a BST in sorted order** | **inorder** | the BST invariant makes inorder yield sorted output ([[10 - Search Trees\|ch. 10]]) |
| find the shallowest match | **breadth-first** | nearer nodes are visited first |
| level-by-level processing | **breadth-first** | that is its definition |

> [!note] The rule that covers most cases
> **If a node's result depends on its children's results, use postorder.** [[03 - Recursion|Ch. 03]]'s `disk_usage` is postorder — a directory's size needs its children's sizes first. So is computing height (§5), evaluating an expression tree (§5), and freeing memory.
>
> **If a node's result must be available before descending, use preorder** — depth computation, path-tracking, and serialisation.

### 5. Expression trees — the application that explains everything

An arithmetic expression is a tree: internal nodes are operators, leaves are operands.

> [!example]- $(3+5)\times2$, all three notations and two evaluations (verified)
> ```
>       *
>      / \
>     +   2
>    / \
>   3   5
> ```
> | traversal | output | notation |
> |---|---|---|
> | preorder | `* + 3 5 2` | **prefix** (Polish) |
> | inorder | `3 + 5 * 2` | **infix** |
> | postorder | `3 5 + 2 *` | **postfix** (RPN) |
>
> **The infix output is ambiguous.** Read with ordinary precedence, `3 + 5 * 2` is $13$ — not the $16$ the tree denotes. **Inorder traversal discards the grouping**, which is exactly why infix notation needs parentheses and precedence rules while prefix and postfix do not.
>
> **Two ways to evaluate, both verified to give 16:**
>
> ```python
> def eval_postfix(tokens):
>     """Evaluate RPN with a stack -- ch. 05."""
>     st = []
>     for t in tokens:
>         if t in '+-*/':
>             r = st.pop(); l = st.pop()
>             st.append({'+': l+r, '-': l-r, '*': l*r, '/': l/r}[t])
>         else:
>             st.append(float(t))
>     return st.pop()
> ```
> ```python
> def eval_tree(T, n=None):
>     """Evaluate directly -- postorder in disguise."""
>     if n is None:
>         n = T._root
>     if T.is_leaf(n):
>         return float(n._element)
>     l = eval_tree(T, n._left)          # left subtree first
>     r = eval_tree(T, n._right)         # then right
>     return {'+': l+r, '-': l-r, '*': l*r, '/': l/r}[n._element]   # then combine
> ```
>
> **`eval_tree` *is* a postorder traversal** — both children are fully evaluated before the operator is applied. And `eval_postfix` consumes the postorder output with a stack. **The two are the same computation**, one recursive and one with an explicit stack, which is [[03 - Recursion|ch. 03]] §6's point about recursion and explicit stacks being interchangeable.
>
> **This is why compilers parse to a tree and emit postfix**: the tree captures the grouping unambiguously, and postfix is what a stack machine executes directly.

### 6. Depth, height, and an $O(n^2)$ trap

```python
    def depth(self, n):
        """Number of ancestors of n. O(depth)."""
        if self.is_root(n):
            return 0
        return 1 + self.depth(n._parent)

    def height(self, n=None):
        """Height of the subtree rooted at n. O(size of that subtree)."""
        if n is None:
            n = self._root
        if self.is_leaf(n):
            return 0
        return 1 + max(self.height(c) for c in self.children(n))
```

*(Verified: `depth(D)` = 2, `depth(A)` = 0, `height()` = 2.)*

> [!warning] The tempting definition of height is $O(n^2)$
> Height is *"the maximum depth of any leaf"*, which suggests:
> ```python
> def height_bad(T, n):
>     return max(T.depth(m) for m in all_nodes(T, n))    # O(n^2)
> ```
> *(Verified to give the correct answer, 2 — it is correct and slow.)*
>
> **It is quadratic** because each `depth` call walks to the root, costing $O(h)$, and it is called for all $n$ nodes. In a degenerate tree $h=n-1$ and the total is $\Theta(n^2)$.
>
> **The recursive definition is $O(n)$** — each node is visited once and its height computed from its children's, which are already known. **The difference is exactly [[03 - Recursion|ch. 03]] §3's lesson: compute bottom-up from subresults instead of recomputing from scratch.** Naive Fibonacci and `height_bad` are the same mistake.

### 7. Why balance matters — the preview of chapter 10

Everything above is $\Theta(n)$ regardless of shape. But the *searching* structures ahead depend on **height**, and height depends on shape.

*(Verified:)*

| tree of 8 nodes | height |
|---|---|
| right-chain (each node has only a right child) | **7** $=n-1$ |
| perfectly balanced | **3** $=\lfloor\lg n\rfloor$ |

**A degenerate tree is a linked list wearing a tree's interface** — same $O(n)$ operations, more memory. [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]] proved the bound $h\ge\lg t$: a binary tree with $t$ leaves must have height at least $\lg t$, so $\lg n$ is the *best possible* — but nothing forces a tree to achieve it.

**That gap between $\lg n$ and $n-1$ is what [[10 - Search Trees|ch. 10]] exists to close**, and it is why AVL and red–black trees are worth their complexity.

## ✏️ Exercises

**1. (Terminology.)** For the tree of §3: (a) name the root, the leaves and the internal nodes; (b) give the depth of each node and the height of the tree; (c) list the ancestors of `E` and the descendants of `B`; (d) explain why depth and height are computed in opposite directions.

> [!example]- Solution
> ```
>         A
>        / \
>       B   C
>      / \   \
>     D   E   F
> ```
> **(a)** Root **A**. Leaves **D, E, F** (no children). Internal **A, B, C**.
>
> **(b)**
>
> | node | depth |
> |---|---|
> | A | 0 |
> | B, C | 1 |
> | D, E, F | 2 |
>
> **Height of the tree = 2** *(verified)* — the longest root-to-leaf path has two edges.
>
> **(c)** Ancestors of **E**: B, A (following parent links to the root). Descendants of **B**: D, E — plus B itself if you count a node as its own descendant, which conventions differ on; state which you mean.
>
> **(d) Because they measure toward different endpoints, and only one of them is unique.**
>
> **Depth counts upward to the root.** The root is unique, so there is exactly one path up and depth is well defined by walking parents — $O(\text{depth})$ with a parent reference.
>
> **Height counts downward to the deepest leaf.** There are many leaves and many downward paths, so height requires a **maximum** over all of them — hence the recursion over children, and hence $O(n)$ rather than $O(h)$.
>
> **This asymmetry is why §6's naive height is quadratic:** it computes height by taking a max over depths, doing an upward walk per node when one downward pass would do.

**2. (Implementation and traversals.)** (a) Implement a linked binary tree with `add_root`, `add_left`, `add_right`. (b) Why must these return the new node? (c) Implement all four traversals. (d) Give the output of each on the §3 tree and state their complexities.

> [!example]- Solution
> **(a)** §2's `LinkedBinaryTree`. *(Verified, including `ValueError` when adding a child that already exists.)*
>
> **(b) Because a node reference is the only way to address a position in the tree.** `add_left(n, e)` requires `n`; the only way to obtain a reference to a node you just created is for the creating method to return it. Without that, only the root would ever be reachable and no tree could be built.
>
> **This is [[06 - Linked Lists|ch. 06]] §2's position concept** — the same reason `_insert_between` returns its new node — and it recurs in every linked structure.
>
> **(c)** §3's implementations, as generators.
>
> **(d)** *(all verified)*
>
> | traversal | output |
> |---|---|
> | preorder | `A B D E C F` |
> | inorder | `D B E A C F` |
> | postorder | `D E B F C A` |
> | breadth-first | `A B C D E F` |
>
> **Complexity: all four are $\Theta(n)$ time** — one visit per node, constant work each.
>
> **Space differs and is worth stating:**
> - recursive traversals: $O(h)$ for the call stack — $O(\log n)$ balanced, $O(n)$ degenerate;
> - breadth-first: $O(w)$ for the queue, where $w$ is the maximum level width — and for a balanced tree the bottom level holds about $n/2$ nodes, so **$O(n)$**.
>
> **So breadth-first can use far more memory than the depth-first traversals** on a wide tree, which is the reverse of the usual intuition and worth remembering when the tree is large.

**3. (Expression trees.)** (a) Draw the tree for $(3+5)\times2$ and give all three traversal outputs. (b) Which notations are unambiguous, and why? (c) Write a recursive evaluator and say which traversal it is. (d) Write a stack-based postfix evaluator and relate the two.

> [!example]- Solution
> **(a)** §5's tree. Outputs *(verified)*: prefix `* + 3 5 2`; infix `3 + 5 * 2`; postfix `3 5 + 2 *`.
>
> **(b) Prefix and postfix are unambiguous; infix is not.**
>
> Every operator has known arity (2 here), so scanning a prefix or postfix string determines the structure uniquely — there is exactly one way to parse it. **Infix loses the grouping**: `3 + 5 * 2` read with standard precedence gives $3+10=13$, not the intended $(3+5)\times2=16$. The tree knew the grouping; inorder traversal threw it away.
>
> **That is why infix requires parentheses and a precedence table, while RPN calculators need no bracket keys.**
>
> **(c)** §5's `eval_tree`. *(Verified: 16.0.)*
>
> **It is a postorder traversal.** Both children are fully evaluated *before* the operator is applied — exactly postorder's "left, right, root". The only difference from §3's `postorder` generator is that it returns a value up the recursion instead of yielding an element.
>
> **This is the general shape of postorder computation:** recurse on children, combine their results. `disk_usage` ([[03 - Recursion|ch. 03]]), `height` (§6) and tree deletion all have it.
>
> **(d)** §5's `eval_postfix`. *(Verified: 16.0 — same answer.)*
>
> **The relationship: they are the same computation with the stack made explicit.**
>
> `eval_tree` uses the **call stack** to remember partially-evaluated operators; `eval_postfix` uses an **explicit stack** ([[05 - Stacks, Queues and Deques|ch. 05]]) holding partially-consumed operands. The postorder sequence is precisely the order in which a stack machine must receive the tokens for this to work — operands pushed, then an operator popping exactly its arity.
>
> **This is [[03 - Recursion|ch. 03]] §6's point that recursion and an explicit stack are interchangeable**, and it explains the compiler pipeline: parse to a tree (which captures grouping), emit postorder (which a stack machine executes without needing the tree).

**4. (Choosing a traversal.)** Which traversal for each, and why? (a) Print a directory tree with subfolders indented under their parent. (b) Compute the total size of a directory. (c) Delete every node, freeing children before parents. (d) Find the shallowest node matching a predicate. (e) Print a BST's keys in sorted order.

> [!example]- Solution
> **(a) Preorder.** The folder's name must appear before its contents, and preorder emits the root before descending. *(Depth for indentation comes free by passing a level parameter down the recursion.)*
>
> **(b) Postorder.** A directory's total size is its own size plus its children's totals — **the parent's result depends on the children's**, so children must finish first. This is exactly [[03 - Recursion|ch. 03]] §2's `disk_usage`.
>
> **(c) Postorder.** A parent must not be freed while its children are still reachable only through it; postorder guarantees children are released first. **Preorder would free a parent and lose the pointers to its subtrees** — a memory leak in a manually managed language, and in Python an unnecessary confusion.
>
> **(d) Breadth-first.** It visits nodes in nondecreasing order of depth, so the **first** match found is a shallowest one. A depth-first traversal might plunge down one branch and find a deep match before a shallow one in another branch.
>
> **And because the traversals are lazy generators**, `next(filter(pred, T.breadthfirst()))` stops at the first match without visiting the rest — the practical payoff of §3's laziness.
>
> **(e) Inorder.** A binary search tree's invariant is *everything in the left subtree precedes the node, everything in the right follows it* — which is exactly what inorder emits. **The inorder traversal of a BST is its keys in sorted order**, and that is the defining property [[10 - Search Trees|ch. 10]] relies on.
>
> **The rule underlying (b) and (c): if the parent needs the children's results — or must outlive them — use postorder.** If the parent's information is needed on the way down, use preorder.

**5. (Hard — height, cost and balance.)** (a) Define depth and height recursively. (b) Show that computing height as "max depth over all nodes" is $O(n^2)$, and give an $O(n)$ method. (c) Compare the heights of a degenerate and a balanced tree of $n$ nodes. (d) Why does this matter for later chapters?

> [!example]- Solution
> **(a)**
> $$\text{depth}(v)=\begin{cases}0 & v\text{ is the root}\\ 1+\text{depth}(\text{parent}(v)) & \text{otherwise}\end{cases}$$
> $$\text{height}(v)=\begin{cases}0 & v\text{ is a leaf}\\ 1+\max_{c\,\in\,\text{children}(v)}\text{height}(c) & \text{otherwise}\end{cases}$$
> **Depth recurses upward on the (unique) parent; height recurses downward with a max over (several) children.**
>
> **(b)** The naive method computes `max(depth(m) for m in all_nodes)`. Each `depth(m)` walks from `m` to the root, costing $O(\text{depth}(m))$, and it is done for all $n$ nodes:
> $$\sum_{v}\text{depth}(v)\;=\;\Theta(n\cdot h),$$
> which is $\Theta(n^2)$ for a degenerate tree ($h=n-1$) and $\Theta(n\log n)$ for a balanced one. *(Verified to return the correct answer, 2 — it is correct, just wasteful.)*
>
> **The $O(n)$ method is the recursive definition itself.** Each node's height is computed once from its children's heights, which the recursion has already produced. **One visit per node, constant work each: $\Theta(n)$.**
>
> **The difference is the same as [[03 - Recursion|ch. 03]] §3's Fibonacci lesson** — the naive version recomputes information the recursion could have carried. `depth` re-walks paths that the postorder recursion traverses anyway. **Compute bottom-up from subresults rather than top-down from scratch.**
>
> **(c)** *(verified for $n=8$)*
>
> | shape | height | general |
> |---|---|---|
> | right-chain | **7** | $n-1$ |
> | perfectly balanced | **3** | $\lfloor\lg n\rfloor$ |
>
> At $n=8$ that is 7 against 3; at $n=10^6$ it would be $999\,999$ against $19$.
>
> **A degenerate tree is a linked list with extra pointers** — the tree interface is intact and every advantage is gone.
>
> **(d) Because every searching structure ahead has costs proportional to height, not to $n$.**
>
> - A **binary search tree** ([[10 - Search Trees|ch. 10]]) locates a key by descending one path: $O(h)$. Balanced that is $O(\log n)$; degenerate it is $O(n)$ — no better than a linear scan.
> - A **heap** ([[08 - Priority Queues and Heaps|ch. 08]]) sifts up or down one path: $O(h)$. Heaps guarantee $h=\lfloor\lg n\rfloor$ **by construction**, which is why they need no rebalancing.
> - [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]'s bound $h\ge\lg t$ says $\lg n$ is the **best possible** height for $n$ leaves — so a balanced tree is optimal and a degenerate one is as bad as possible.
>
> **And crucially: a plain BST degenerates on sorted input**, which is the commonest real-world arrival order. Inserting $1,2,3,\dots,n$ in order produces exactly the right-chain above.
>
> **So the entire content of [[10 - Search Trees|ch. 10]] is: keep the height at $O(\log n)$ no matter what order the data arrives in.** AVL, splay and red–black trees are three answers to that one question, and this exercise is why the question is worth asking.

## 📝 Summary

- **A tree is the first non-linear structure**: one root, every other node with exactly one parent. **Depth counts upward to the root (unique path); height counts downward to the deepest leaf (max over paths).**
- **A binary tree** has at most two children per node, **left and right distinguished** as part of the structure.
- **The linked representation** stores element, parent and two child references per node, with `__slots__` ([[06 - Linked Lists|ch. 06]]). **`add_*` must return the new node**, since a node reference is the only way to name a position.
- **Four traversals, all $\Theta(n)$:** preorder (root, L, R), inorder (L, root, R), postorder (L, R, root) and **breadth-first (level by level, using a queue)**.
- *(Verified on `A/B,C/D,E,F`: preorder `A B D E C F`, inorder `D B E A C F`, postorder `D E B F C A`, breadth-first `A B C D E F` — **matching [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]'s independently computed results.**)*
- **Traversals are generators, hence lazy** — a search can stop at the first match, memory is $O(h)$ not $O(n)$, and they compose with `filter`/`map`.
- **Space differs even though time does not:** recursive traversals use $O(h)$ stack; breadth-first uses $O(w)$ queue, and a balanced tree's bottom level holds $\approx n/2$ nodes, so **breadth-first can be $O(n)$**.
- **Choosing:** **postorder when a node's result depends on its children's** (size, height, evaluation, deletion); **preorder when information flows downward** (serialisation, printing, paths); **inorder for a BST's sorted order**; **breadth-first for shallowest-first**.
- **An expression tree makes the three orders concrete:** preorder is **prefix**, postorder is **postfix (RPN)**, inorder is **infix and ambiguous** — `3 + 5 * 2` evaluates to 13, not the tree's 16. **Grouping is lost by inorder**, which is why infix needs parentheses.
- **Recursive evaluation *is* postorder**, and the stack-based RPN evaluator is the same computation with the stack made explicit — [[03 - Recursion|ch. 03]] §6's interchangeability.
- **Computing height as "max depth over all nodes" is $\Theta(n\cdot h)$** — quadratic on a degenerate tree. **The recursive definition is $\Theta(n)$**: compute bottom-up from subresults.
- **Height depends entirely on shape:** $n-1$ for a chain against $\lfloor\lg n\rfloor$ balanced — **7 versus 3 at $n=8$** *(verified)*. **Every searching structure ahead costs $O(h)$, so [[10 - Search Trees|ch. 10]] exists to keep $h=O(\log n)$.**

## ⚠️ Important Notes

1. **Depth and height are not opposites of one another** — depth is per-node and counts up; height is per-node and counts down. A leaf has height 0 and possibly large depth.
2. **`add_left`/`add_right` must return the node**, or the tree cannot be extended beyond the root.
3. **Left and right are distinguishable in a binary tree.** A node with a single left child differs from one with a single right child, and any code assuming otherwise will mis-handle the degenerate cases.
4. **Choose the traversal by data flow, not by habit.** If the parent needs its children's results, only postorder works — preorder will read values that have not been computed.
5. **Never free or mutate a parent before its children in a manual traversal.** Postorder exists for this.
6. **Breadth-first needs a queue, not a stack.** Substituting a stack silently turns it into a depth-first traversal — [[05 - Stacks, Queues and Deques|ch. 05]] Exercise 5(b).
7. **Breadth-first can use more memory than depth-first**, despite the intuition: $O(w)$ against $O(h)$, and $w\approx n/2$ for a balanced tree.
8. **Keep traversals as generators.** Materialising into a list forfeits early termination and $O(h)$ memory for no benefit.
9. **Do not compute height by maximising over depths.** It is $\Theta(n\cdot h)$; the recursive definition is $\Theta(n)$.
10. **Test the empty tree and the single-node tree.** *(Verified: empty gives size 0 and empty traversals; a single node has height 0, depth 0, and is a leaf.)* Both are easy to get wrong — `height` of a leaf is 0, not 1, and `max()` over no children raises `ValueError`.
11. **Recursive traversal on a degenerate tree can exhaust the stack** — depth $n$, and Python's limit is 1000 ([[03 - Recursion|ch. 03]] §4). A balanced tree is safe; an unbalanced one is not.
12. **Inorder is meaningful only for binary trees.** With three or more children there is no canonical place for the root, which is why the general tree ADT defines only pre- and postorder.
13. **A degenerate tree is a linked list with extra pointers** — same complexity, more memory, and no advantage whatever.
14. **A plain BST degenerates on sorted input**, which is depressingly common. Do not assume random arrival order; [[10 - Search Trees|ch. 10]] is the fix.

> [!warning] Gaps in the source material
> **Goodrich's ch. 8 prose extracts cleanly** — the tree terminology, the ADT definitions, the traversal descriptions and the expression-tree discussion all came through readably.
>
> **His code did not**, per the standing problem in `00-Index.md`. **`LinkedBinaryTree`, all four traversals, both expression evaluators and the height comparison are my own implementations**, written from his prose and **all executed** — verified for structure (size, height, depth, leaf tests), for all four traversal orders, for laziness, for both evaluators agreeing at 16.0, and on the **edge cases**: empty tree, single node, and a degenerate right-chain.
>
> **The strongest verification in this chapter is a cross-subject one.** The traversal outputs `A B D E C F` / `D B E A C F` / `D E B F C A` **exactly match those computed independently in [[Discrete Mathematics/contents/09 - Trees|Discrete Mathematics ch. 09]] §6** for the same tree, as do the expression-tree notations. **Two subjects, two methods, same answers** — which is the sort of check the vault's structure is meant to make possible.
>
> **All figures are images and are lost**, and this chapter feels it: **every tree diagram is gone** — the illustrations of terminology (ancestors, subtrees, depth levels), the traversal-order arrows showing the path through a tree, the expression-tree pictures, and the level-numbering diagrams. **The ASCII sketches in §3 and §5 are my substitutes.** For a structure defined by its picture this is the most damaging loss so far, and the reader should draw the trees while reading.
>
> **No error was found in Goodrich ch. 8.**
>
> **Additions beyond the source.** **The traversal-choice table (§4) is mine** — Goodrich defines the traversals and gives scattered applications, but the "if the parent needs its children's results, use postorder" rule that organises them is my framing. **The $O(n^2)$ height trap (§6) is stated here explicitly** with the connection back to [[03 - Recursion|ch. 03]]'s Fibonacci lesson; Goodrich gives the linear algorithm without contrasting it. **The observation that breadth-first uses $O(w)=O(n)$ space while recursive traversals use $O(h)=O(\log n)$** — reversing the usual intuition — is mine. **§7 and Exercise 5(d) (the degenerate-versus-balanced comparison and why it drives [[10 - Search Trees|ch. 10]]) are my addition**, tying the measurement to [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]'s $h\ge\lg t$ bound and to the fact that BSTs degenerate on sorted input. The emphasis that **traversals should stay generators**, with the laziness demonstration, follows [[01 - Python and Object-Oriented Foundations|ch. 01]] §4 and is not in the source.
>
> **Deliberately compressed.** **Goodrich §8.1's general (non-binary) Tree ADT** is mentioned but not implemented separately — the binary case carries every idea, and the general case differs only in `children()` yielding a list. **§8.3.2's array-based representation of binary trees is deferred to [[08 - Priority Queues and Heaps|ch. 08]]**, where it is not a curiosity but the reason heaps are efficient. **§8.4.6's Euler tour framework** is omitted as a generalisation whose payoff comes only for problems this scope does not reach. **The theory — characterisations, edge counts, the $h\ge\lg t$ bound, the $\Omega(n\lg n)$ sorting proof — is owned by [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]** and cross-linked rather than repeated, per the boundary recorded in both indexes.

**Previous:** [[06 - Linked Lists]] · **Next:** [[08 - Priority Queues and Heaps]]
