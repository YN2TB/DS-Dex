---
subject: Discrete Mathematics
chapter: 9
tags: [ds, discrete-mathematics, trees, spanning-trees, prim, kruskal, binary-trees, traversals, decision-trees, huffman, sorting-lower-bound]
source: "Johnsonbaugh, *Discrete Mathematics* 8e, ch. 9 (book pp. 438–505)"
---

# Trees

Trees are the most useful special case of a graph, and the most common data structure in computing — file systems, parse trees, search indexes, decision trees, and phylogenies are all trees. They are graphs with just enough structure to be easy and just enough freedom to be interesting.

This chapter also **settles the largest outstanding debt in the subject.** [[04 - Algorithms and Their Analysis|Ch. 04]] Exercise 5(e), [[07 - Recurrence Relations|ch. 07]] Exercise 5(e) and [[08 - Graph Theory|ch. 08]] all deferred the same result here: that **every comparison-based sorting algorithm needs $\Omega(n\lg n)$ comparisons**, and hence that merge sort is optimal. §8 proves it, and the proof is a tree argument — which is why it had to wait.

## 📘 Main Knowledge

### 1. Trees, rooted and free

> [!note] Definition
> A **(free) tree** is a simple graph in which, for any two vertices $v$ and $w$, there is a **unique simple path** from $v$ to $w$.
>
> A **rooted tree** is a tree with one vertex designated the **root**.

The uniqueness in the definition is the whole content: a tree is connected (a path exists) and has no cycles (the path is unique — two distinct paths would form a cycle).

**Rooted trees are drawn with the root at the top**, and give every vertex a **level**: the length of the unique simple path from the root. The **height** of a rooted tree is the maximum level.

> [!warning] The root is a choice, and it changes the height
> The *same* free tree becomes different rooted trees under different choices of root, with different levels and different heights. Johnsonbaugh's Example 9.1.4 makes the point: one tree rooted at one vertex has height 2; rooted elsewhere it has height 3.
>
> **So "the height of a tree" is meaningless until the root is named** — a distinction worth keeping, because most algorithmic uses of trees care about height.

**Family-tree vocabulary** transfers wholesale to rooted trees: **parent**, **child**, **sibling**, **ancestor**, **descendant**. A vertex with no children is a **terminal vertex** or **leaf**; the others are **internal vertices**.

> [!example]- Huffman codes: variable-length encoding from a tree
> Fixed-length encodings (ASCII: 8 bits per character) waste space when characters have unequal frequencies. A **Huffman code** assigns **variable-length bit strings**, shorter ones to commoner characters.
>
> The code *is* a rooted binary tree: label each left edge $0$ and each right edge $1$, and read a character's code off the path from root to its leaf. **Because every character sits at a leaf, no code is a prefix of another** — so a bit string decodes uniquely, left to right, with no separators. That prefix-free property is the reason a tree is the right object.
>
> **Huffman's algorithm** builds the optimal tree greedily: repeatedly take the two lowest-frequency items, merge them into a subtree whose frequency is their sum, and reinsert. **The optimal tree is not unique** — ties can be broken differently, giving trees of different heights but the same total encoded length.
>
> **Still in use:** Huffman coding is a component of DEFLATE (`gzip`, PNG) and of fax compression. *(Cross-reference: this is data compression by exploiting non-uniform frequencies, which is exactly what entropy measures — see [[Probability Theory/contents/09 - Additional Topics in Probability|Probability Theory ch. 09]].)*

### 2. Four equivalent characterisations

> [!note] Theorem 9.2.3
> Let $T$ be a graph with $n$ vertices. The following are **equivalent**:
> 1. $T$ is a tree;
> 2. $T$ is **connected and acyclic**;
> 3. $T$ is **connected and has $n-1$ edges**;
> 4. $T$ is **acyclic and has $n-1$ edges**.

**This is the most useful theorem in the chapter**, because it lets you verify treeness by whichever condition is cheapest to check — usually counting edges.

Note the shape of (3) and (4): **connected + $n-1$ edges**, or **acyclic + $n-1$ edges**. Either pairing suffices; the edge count alone does not.

> [!warning] Two immediate consequences worth memorising
> - **A connected graph with $n$ vertices and *fewer* than $n-1$ edges is impossible** — connectivity requires at least $n-1$.
> - **A connected graph with $n$ vertices and *more* than $n-1$ edges must contain a cycle.** If it were acyclic it would be a tree by (2), and would have exactly $n-1$ edges.
>
> So among connected graphs on $n$ vertices, **$n-1$ edges is exactly the boundary between "has a cycle" and "impossible"** — trees are the minimally connected graphs, and equivalently the maximally acyclic ones.

Johnsonbaugh proves the cycle of implications by induction, using the standard device: in a connected acyclic graph, take a longest path with no repeated edges; **its endpoint must be a leaf** (otherwise the path extends or a cycle appears), so delete it and apply the inductive hypothesis to a graph with one fewer vertex.

### 3. Spanning trees

> [!note] Definition and Theorem 9.3.4
> $T$ is a **spanning tree** of $G$ if $T$ is a subgraph of $G$ containing **all** the vertices of $G$, and $T$ is a tree.
>
> **$G$ has a spanning tree if and only if $G$ is connected.**

*(⟹)* If $T$ spans $G$, any two vertices are joined by a path in $T$, hence in $G$.
*(⟸)* If $G$ is connected but has a cycle, delete an edge of that cycle — **deleting a cycle edge cannot disconnect the graph**, since the rest of the cycle still joins its endpoints. Repeat until acyclic; the result is connected, acyclic and spans, hence a spanning tree. $\blacksquare$

**A graph generally has many spanning trees.** Both breadth-first and depth-first search produce one, and which one depends on the search order — the algorithms are in [[Data Structures and Algorithms/contents/00-Index|DSA]]; here the point is the existence theorem.

### 4. Minimal spanning trees: Prim and Kruskal

> [!note] Definition
> In a weighted graph, a **minimal spanning tree** is a spanning tree of minimum total edge weight.

> [!note] Prim's algorithm
> Start with a single vertex. Repeatedly **add the cheapest edge joining a vertex already in the tree to one not yet in it.** Stop after $n-1$ edges.

```python
def prim(V, E, start):               # E = list of (u, v, weight)
    in_tree, chosen, total = {start}, [], 0
    while in_tree != V:
        # cheapest edge with exactly one endpoint inside
        w, u, v = min((w, u, v) for u, v, w in E
                      if (u in in_tree) != (v in in_tree))
        chosen.append((u, v, w))
        total += w
        in_tree |= {u, v}
    return chosen, total
```

> [!note] Kruskal's algorithm
> Sort all edges by weight. Scan them in order, **adding each edge unless it would create a cycle.** Stop after $n-1$ edges.

Prim grows **one** tree; Kruskal grows a **forest** that merges into one. Both are **greedy** — each step takes the locally cheapest option — and remarkably, both are correct.

> [!warning] Greedy usually fails; here it does not, and that needs proof
> Johnsonbaugh is careful about this. "Doing the best locally" generally does **not** give a global optimum — his counterexample is a "shortest path algorithm" that always follows the cheapest available edge, which is easily fooled. ([[08 - Graph Theory|Ch. 08]] §6's Dijkstra example makes the same point: the shortest route to $d$ did **not** start with the cheapest edge from $a$.)
>
> **So Theorem 9.4.5 — that Prim's algorithm is correct — is a real theorem.** Its proof is the standard **exchange argument**: maintain the invariant that the partial tree $T_i$ is contained in *some* minimal spanning tree $T'$. If the next edge $(j,k)$ chosen by Prim is not in $T'$, then $T'\cup\{(j,k)\}$ has a cycle; some other edge of that cycle also crosses between the tree and its complement, and it cannot be cheaper than $(j,k)$ (or Prim would have taken it). **Swap them:** the result is still a spanning tree, weighs no more, and contains $T_i\cup\{(j,k)\}$. So the invariant survives, and at termination $T_{n-1}$ *is* a minimal spanning tree. $\blacksquare$
>
> **This "assume it extends to an optimum, then exchange" pattern is the standard way to prove a greedy algorithm correct**, and it is worth recognising — it recurs throughout [[Optimization/contents/09 - Linear Programming and the Simplex Method|combinatorial optimization]].

> [!example]- Prim and Kruskal on the same graph (verified)
> Vertices $1,\dots,6$ with edges (weights in parentheses):
> $$12(7),\ 13(2),\ 15(4),\ 23(5),\ 26(8),\ 34(3),\ 45(6),\ 56(3),\ 36(9)$$
>
> | | edges chosen, in order | total |
> |---|---|---|
> | **Prim** from vertex 1 | $13(2),\ 34(3),\ 15(4),\ 56(3),\ 23(5)$ | $\mathbf{17}$ |
> | **Kruskal** | $13(2),\ 34(3),\ 56(3),\ 15(4),\ 23(5)$ | $\mathbf{17}$ |
>
> Both use $5=n-1$ edges ✓ and **both total 17** ✓ — here they even choose the same *set* of edges, in a different order.
>
> **The general fact:** minimal spanning trees need not be unique (ties in weights allow alternatives), but **every minimal spanning tree has the same total weight** — that is what "minimal" means. So two correct algorithms may disagree on edges and must agree on weight.

**Complexity.** Johnsonbaugh's stated version of Prim examines $\Theta(n^3)$ edges; a better implementation achieves $\Theta(n^2)$, which is optimal in the dense case since $K_n$ has $\Theta(n^2)$ edges. With a heap and adjacency lists one gets $O(|E|\log|V|)$, which is better for sparse graphs.

### 5. Binary trees and two counting theorems

> [!note] Definition
> A **binary tree** is a rooted tree in which each vertex has at most two children, each designated a **left child** or a **right child**. A **full binary tree** has every vertex with **either two children or none**.

The left/right designation matters: two binary trees with the same shape but a child on opposite sides are different binary trees.

> [!note] Theorem 9.5.4
> A full binary tree with $i$ internal vertices has **$i+1$ terminal vertices** and $2i+1$ vertices in total.

*(Verified for $i=0,\dots,5$: terminals $1,2,3,4,5,6$; totals $1,3,5,7,9,11$.)*

**Why:** each internal vertex has exactly 2 children, so there are $2i$ non-root vertices, hence $2i+1$ in all; subtracting the $i$ internal ones leaves $i+1$ leaves. **A single-elimination tournament is a full binary tree**, which is why $n$ players require exactly $n-1$ matches — one internal vertex per match.

> [!note] Theorem 9.5.6 — the lemma that proves the sorting bound
> If a binary tree of height $h$ has $t$ terminal vertices, then
> $$t\le2^h,\qquad\text{equivalently}\qquad h\ge\lg t .$$

*Proof (induction on $h$).* For $h=0$ the tree is one vertex, $t=1=2^0$. For $h>0$, the root has one or two subtrees; each has height $\le h-1$ and, by hypothesis, at most $2^{h-1}$ leaves. The leaves of $T$ are exactly those of the subtrees, so $t\le2\cdot2^{h-1}=2^h$. $\blacksquare$

**The bound is tight** — a complete binary tree of height $h$ has exactly $2^h$ leaves. *(Verified: Johnsonbaugh's Example 9.5.7 has $h=3$, $t=8$, and $\lg 8=3=h$ exactly.)*

**Read the contrapositive form and its importance becomes clear:** *if you need to distinguish $t$ outcomes with a binary decision, you need height at least $\lg t$.* That single sentence is §8.

A **binary search tree** stores data so that everything in a vertex's left subtree precedes it and everything in the right subtree follows. **Search time is proportional to height**, so keeping the height near $\lg n$ — the minimum permitted by Theorem 9.5.6 — is the whole business of balanced trees (AVL, red–black), which [[Data Structures and Algorithms/contents/00-Index|DSA]] owns.

### 6. Tree traversals

Three recursive ways to visit every vertex of a binary tree exactly once, distinguished only by **when the root is processed**:

| Traversal | Order |
|---|---|
| **preorder** | **root**, left subtree, right subtree |
| **inorder** | left subtree, **root**, right subtree |
| **postorder** | left subtree, right subtree, **root** |

```python
def preorder(v):                 # Johnsonbaugh's Algorithm 9.6.1
    if v is None:
        return
    process(v)
    preorder(left_child(v))
    preorder(right_child(v))
```

The other two move `process(v)` to the middle or the end. **Each is a three-line recursion, and each is an induction** — the base case is the empty tree, which is why the `None` check comes first.

> [!example]- Traversals, and why they matter (verified)
> Take the binary tree with root $A$; $A$'s children $B$ (left) and $C$ (right); $B$'s children $D$ and $E$; and $C$ having only a **right** child $F$.
>
> | traversal | output |
> |---|---|
> | preorder | $A\,B\,D\,E\,C\,F$ |
> | inorder | $D\,B\,E\,A\,C\,F$ |
> | postorder | $D\,E\,B\,F\,C\,A$ |
>
> **The application that explains all three: expression trees.** Represent $(3+5)\times2$ with root $\times$, left subtree $+(3,5)$, right child $2$:
>
> | traversal | output | name |
> |---|---|---|
> | preorder | `* + 3 5 2` | **prefix** / Polish notation |
> | inorder | `3 + 5 * 2` | **infix** — the ordinary way |
> | postorder | `3 5 + 2 *` | **postfix** / reverse Polish (RPN) |
>
> **Prefix and postfix need no parentheses** — the structure is recoverable from the order alone, which is why RPN is what a stack machine and a compiler's intermediate form use. Evaluating `3 5 + 2 *` on a stack gives $16$ ✓
>
> **But look at the infix output: `3 + 5 * 2`.** Read with ordinary precedence that is $3+10=13$, not $16$. **Inorder traversal loses the grouping**, which is exactly why infix notation requires parentheses and precedence rules while the other two do not. *(This comparison is my own addition — Johnsonbaugh gives the traversals without the notation application.)*

### 7. Isomorphism of trees

Two rooted trees are isomorphic if there is a bijection preserving the parent–child relation; for **binary** trees, one must also preserve left/right. As in [[08 - Graph Theory|ch. 08]] §8, **invariants** (number of vertices, height, degree sequence, number of leaves at each level) can prove two trees different but never prove them the same.

Tree isomorphism is markedly **easier** than general graph isomorphism — there are polynomial-time algorithms for trees, by canonically encoding each subtree bottom-up, whereas no polynomial algorithm is known for general graphs.

### 8. Decision trees and the minimum time for sorting

Here is the chapter's payoff. A **decision tree** represents an algorithm: each internal vertex asks a question, each edge is an answer, each leaf is an outcome. **The worst-case number of questions is the height of the tree.**

> [!example]- Warm-up: the five-coins puzzle needs three weighings
> Five coins look alike; one is either heavier or lighter. Using only a pan balance, identify the bad coin **and** whether it is heavy or light.
>
> **Count the outcomes:** 5 choices of coin $\times$ 2 (heavy or light) $=\mathbf{10}$ possible answers.
>
> **Count what a shallow tree can distinguish.** Each weighing has **three** results (left heavier, right heavier, balanced), so the decision tree is **ternary**, and a ternary tree of height $h$ has at most $3^h$ leaves. With $h=2$:
> $$3^2=9<10 .$$
> *(Verified.)* **Nine leaves cannot cover ten outcomes, so no algorithm solves the puzzle in two weighings** — three are necessary, and Johnsonbaugh exhibits an algorithm achieving three, so three is optimal. $\blacksquare$
>
> **The whole method in one line: count the outcomes, bound the leaves, compare.**

Now the same argument with two-way comparisons.

> [!note] Theorem 9.7.3 — the sorting lower bound
> If $f(n)$ is the worst-case number of comparisons used by a sorting algorithm on $n$ items, then
> $$f(n)=\Omega(n\lg n).$$

*Proof.* Let $T$ be the decision tree of the algorithm on inputs of size $n$, and $h$ its height. Then:

1. **$h=f(n)$** — the height is the worst-case number of comparisons.
2. **$T$ has at least $n!$ leaves.** The algorithm must be able to produce any of the $n!$ orderings of $n$ distinct items, and different orderings require different leaves.
3. **By Theorem 9.5.6**, a binary tree with $t$ leaves has $h\ge\lg t$. Hence
$$h\ \ge\ \lg(n!).$$
4. **By [[04 - Algorithms and Their Analysis|ch. 04]] §3**, $\lg(n!)=\Theta(n\lg n)$, so $Cn\lg n\le\lg(n!)$ for some $C>0$ and all large $n$.

Combining, $Cn\lg n\le f(n)$ for all but finitely many $n$, i.e. $f(n)=\Omega(n\lg n)$. $\blacksquare$

> [!note] The debt is paid — and note exactly which pieces were needed
> **Each step came from a different chapter.** The tree lemma is §5 of this chapter; the leaf count is [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]]'s $n!$ permutations; the estimate $\lg(n!)=\Theta(n\lg n)$ is [[04 - Algorithms and Their Analysis|ch. 04]] Example 4.3.9. **This is why the result could not be proved earlier.**
>
> **And it closes the sorting question.** [[07 - Recurrence Relations|Ch. 07]] proved merge sort uses $n\lg n-n+1$ comparisons, i.e. $O(n\lg n)$. Now the problem itself requires $\Omega(n\lg n)$. **So merge sort is optimal in order, and no comparison sort can do asymptotically better.**
>
> *(Verified numerically. The lower bound $\lceil\lg(n!)\rceil$ against merge sort's actual count:)*
>
> | $n$ | $\lceil\lg(n!)\rceil$ | merge sort |
> |---|---|---|
> | 4 | 5 | 5 |
> | 8 | 16 | 17 |
> | 16 | 45 | 49 |
>
> **Merge sort is optimal in *order* but not exactly optimal** — it exceeds the information-theoretic minimum by a few comparisons. At $n=4$ it is exactly optimal; at $n=16$ it uses 49 against a floor of 45. **"Optimal" in the $\Theta$ sense is a statement about growth, not about every input size** — the same caution as ch. 04's Important Note 8.

> [!warning] What the theorem does not say
> It applies **only to algorithms that sort by comparing elements**. Radix sort and counting sort inspect digits or use values as array indices, and can beat $n\lg n$ on restricted inputs — they **escape the model**, not the theorem.
>
> **A lower bound always attaches to a problem *in a model of computation*.** Change the model and the bound need not hold. This is the third time this caution has appeared ([[04 - Algorithms and Their Analysis|ch. 04]], [[07 - Recurrence Relations|ch. 07]]) because it is the most common misuse of the result.

## ✏️ Exercises

**1. (Tree characterisations.)** (a) State the four equivalent conditions of Theorem 9.2.3. (b) A connected graph has 12 vertices and 11 edges. Must it be a tree? (c) A graph has 12 vertices and 15 edges and is connected. What can you conclude? (d) A full binary tree has 7 internal vertices. How many leaves and how many vertices in total? (e) How many matches does a single-elimination tournament with 64 players require?

> [!example]- Solution
> **(a)** For a graph $T$ with $n$ vertices, these are equivalent: (1) $T$ is a tree; (2) $T$ is connected and acyclic; (3) $T$ is connected with $n-1$ edges; (4) $T$ is acyclic with $n-1$ edges.
>
> **(b) Yes.** It is connected with $n-1=12-1=11$ edges, which is condition (3). **So it is a tree** — no need to check for cycles, which is the practical value of the theorem.
>
> **(c) It must contain a cycle.** With $n=12$, a connected acyclic graph would be a tree and have exactly $11$ edges. Since $15>11$, it cannot be acyclic. *(More precisely, it has $15-11=4$ edges "in excess", and removing 4 suitable edges yields a spanning tree.)*
>
> **(d)** By Theorem 9.5.4, $i=7$ internal vertices gives $i+1=\mathbf8$ leaves and $2i+1=\mathbf{15}$ vertices in total *(verified)*.
>
> **(e) 63 matches.** The tournament graph is a **full binary tree** whose 64 leaves are the players and whose internal vertices are the matches. By Theorem 9.5.4, $t=i+1$, so $i=t-1=64-1=\mathbf{63}$.
>
> **The slick way to see it:** every match eliminates exactly one player, and 63 players must be eliminated to leave one winner. **Same answer, and it works for any number of players, not just powers of two** — 100 players need 99 matches, though the tree is then not perfectly balanced.

**2. (Spanning trees, Prim and Kruskal.)** For the weighted graph on $\{1,\dots,6\}$ with edges $12(7)$, $13(2)$, $15(4)$, $23(5)$, $26(8)$, $34(3)$, $45(6)$, $56(3)$, $36(9)$: (a) run Prim from vertex 1, listing edges in order; (b) run Kruskal; (c) compare the results; (d) must a minimal spanning tree be unique? Must its weight be?

> [!example]- Solution
> **(a) Prim from vertex 1** — at each step take the cheapest edge with exactly one endpoint in the tree:
>
> | step | tree vertices | cheapest crossing edge | added |
> |---|---|---|---|
> | 1 | $\{1\}$ | $13(2)$ | $13$ |
> | 2 | $\{1,3\}$ | $34(3)$ | $34$ |
> | 3 | $\{1,3,4\}$ | $15(4)$ | $15$ |
> | 4 | $\{1,3,4,5\}$ | $56(3)$ | $56$ |
> | 5 | $\{1,3,4,5,6\}$ | $23(5)$ | $23$ |
>
> Total weight $2+3+4+3+5=\mathbf{17}$, using $5=n-1$ edges ✓ *(verified)*
>
> *(Note step 3: $15(4)$ beat $45(6)$ and $23(5)$ — and at step 4, $56(3)$ was available only once vertex 5 joined.)*
>
> **(b) Kruskal** — sort all edges and add unless a cycle forms:
>
> $13(2)$ ✓, $34(3)$ ✓, $56(3)$ ✓, $15(4)$ ✓, $23(5)$ ✓ — five edges, stop.
> *(Skipped: $45(6)$ would close $1\text-5\text-4\text-3\text-1$; $12(7)$, $26(8)$, $36(9)$ likewise.)*
>
> Total $\mathbf{17}$ *(verified)*.
>
> **(c)** Both produce **the same set of edges** $\{13,34,56,15,23\}$ and the same weight 17 — but **in different orders**. Prim's order is dictated by connectivity to the growing tree; Kruskal's purely by weight. Note Kruskal took $56(3)$ third, at a time when its component was disjoint from the rest — **Prim could not have done that**, since Prim maintains one connected tree throughout.
>
> **(d) The tree need not be unique; the weight must be.**
>
> *Not unique:* if two edges have equal weight and either would complete a spanning tree, both choices give minimal spanning trees. Here $34(3)$ and $56(3)$ tie, and Johnsonbaugh notes exactly this kind of tie in his own example.
>
> *Weight is unique:* "minimal" means minimum total weight, so **every** minimal spanning tree attains the same minimum by definition. **Hence two correct algorithms may output different edge sets and must output the same total** — which is the right way to check an implementation.
>
> *(A sufficient condition for uniqueness: if all edge weights are distinct, the minimal spanning tree is unique.)*

**3. (Binary trees and heights.)** (a) State the bound relating a binary tree's height to its number of leaves. (b) What is the minimum possible height of a binary tree with 100 leaves? (c) What is the maximum? (d) Why do balanced search trees matter?

> [!example]- Solution
> **(a)** Theorem 9.5.6: a binary tree of height $h$ with $t$ terminal vertices satisfies
> $$t\le2^h,\qquad\text{i.e.}\qquad h\ge\lg t .$$
>
> **(b)** We need $2^h\ge100$. Since $2^6=64<100\le128=2^7$, the minimum height is $h=\mathbf7$. Equivalently $h\ge\lceil\lg100\rceil=\lceil6.64\rceil=7$ *(verified against the table of $2^h$)*.
>
> This is achieved by a nearly complete tree — the bound is tight for $t$ an exact power of 2, and within one otherwise.
>
> **(c) There is no maximum bound short of $t-1$... and in fact the height can be as large as 99.** A binary tree with 100 leaves can be a long "caterpillar": a path of 99 internal vertices, each with one leaf hanging off and one child continuing the path, ending in a final leaf. Height $=\mathbf{99}$.
>
> **So the same 100 leaves can sit at height 7 or height 99**, and Theorem 9.5.6 constrains only the *minimum*. That gap is the entire motivation for (d).
>
> **(d)** Search in a binary search tree costs time proportional to the **height**, since a search follows one root-to-leaf path. From (b) and (c), a tree holding $n$ items may have height anywhere from about $\lg n$ to $n-1$:
>
> | $n$ | best height $\approx\lg n$ | worst height $\approx n$ |
> |---|---|---|
> | $10^3$ | 10 | 1000 |
> | $10^6$ | 20 | $10^6$ |
>
> **A degenerate tree is no better than a linked list** — and a plain BST degenerates exactly when data arrive already sorted, which is depressingly common. **Balanced structures (AVL, red–black, B-trees) enforce $O(\lg n)$ height**, guaranteeing the best case of Theorem 9.5.6 rather than hoping for it. That is why they exist, and [[Data Structures and Algorithms/contents/00-Index|DSA]] covers how.

**4. (Traversals.)** For the binary tree with root $A$, $A$'s children $B$ (left) and $C$ (right), $B$'s children $D$ and $E$, and $C$ with only a right child $F$: (a) give the preorder, inorder and postorder outputs. (b) Draw the expression tree for $(3+5)\times2$ and give all three traversals. (c) Which traversals allow the expression to be reconstructed without parentheses, and why?

> [!example]- Solution
> **(a)** *(all verified)*
>
> | traversal | output |
> |---|---|
> | preorder (root, L, R) | $\mathbf{A\,B\,D\,E\,C\,F}$ |
> | inorder (L, root, R) | $\mathbf{D\,B\,E\,A\,C\,F}$ |
> | postorder (L, R, root) | $\mathbf{D\,E\,B\,F\,C\,A}$ |
>
> Note $C$ has no left child, so in inorder nothing precedes $C$ within its subtree — giving $\dots A\,C\,F$.
>
> **(b)** Expression tree: root $\times$, left subtree $+$ with children $3$ and $5$, right child $2$.
>
> | traversal | output | name |
> |---|---|---|
> | preorder | `* + 3 5 2` | **prefix** (Polish) |
> | inorder | `3 + 5 * 2` | **infix** |
> | postorder | `3 5 + 2 *` | **postfix** (RPN) |
>
> *(All verified; RPN `3 5 + 2 *` evaluates on a stack to $16$ ✓)*
>
> **(c) Prefix and postfix reconstruct uniquely; infix does not.**
>
> **Why prefix/postfix work.** Every operator has a known arity (here 2), so scanning the output determines the structure with no ambiguity. For postfix, push operands on a stack and on seeing an operator pop the right number of arguments — `3 5 + 2 *` gives $\text{push }3,5$; $+\to8$; $\text{push }2$; $\times\to16$ ✓ The traversal order *is* the evaluation order.
>
> **Why infix fails.** The inorder output `3 + 5 * 2` is ambiguous: read with standard precedence ($\times$ before $+$) it means $3+(5\times2)=13$, **not** the intended $(3+5)\times2=16$. **Inorder traversal discards the grouping**, so infix notation must recover it externally — by parentheses and precedence conventions.
>
> **This is why compilers and stack machines use postfix internally**, and why RPN calculators need no bracket keys. **The parenthesis-free property is not a notational curiosity; it is what makes one-pass evaluation possible.**

**5. (Hard — the sorting lower bound.)** (a) Show the five-coins puzzle needs at least 3 weighings. (b) State and prove that any comparison sort needs $\Omega(n\lg n)$ comparisons. (c) Compute the bound for $n=4,8,16$ and compare with merge sort's exact count. (d) Reconcile with the fact that radix sort can run in linear time.

> [!example]- Solution
> **(a)** **Count the outcomes.** The bad coin can be any of 5, and can be heavy or light: $5\times2=\mathbf{10}$ distinct outcomes, each needing its own leaf.
>
> **Bound the leaves.** Each weighing on a pan balance has **three** results (left heavy, right heavy, balanced), so the decision tree is **ternary** and a ternary tree of height $h$ has at most $3^h$ leaves.
>
> Suppose an algorithm used at most 2 weighings. Then $h\le2$ and the tree has at most $3^2=9$ leaves — **but 10 outcomes must be distinguished.** By pigeonhole ([[06 - Counting Methods and the Pigeonhole Principle|ch. 06]] §8) two outcomes share a leaf, so the algorithm cannot tell them apart, contradiction. **Hence at least 3 weighings are needed** *(verified: $3^2=9<10\le27=3^3$)*, and since a 3-weighing algorithm exists, 3 is optimal. $\blacksquare$
>
> **(b) Theorem.** If $f(n)$ is the worst-case number of comparisons of a comparison-based sorting algorithm, then $f(n)=\Omega(n\lg n)$.
>
> *Proof.* Represent the algorithm on inputs of size $n$ by its decision tree $T$, of height $h$. Each internal vertex is one comparison with **two** outcomes, so $T$ is **binary**.
> 1. $h=f(n)$: the height is the worst-case comparison count.
> 2. **$T$ has at least $n!$ leaves.** There are $n!$ possible input orderings ([[06 - Counting Methods and the Pigeonhole Principle|ch. 06]] §3), and two different orderings require different output permutations, hence different leaves.
> 3. **Theorem 9.5.6** gives $h\ge\lg t\ge\lg(n!)$.
> 4. **$\lg(n!)=\Theta(n\lg n)$** ([[04 - Algorithms and Their Analysis|ch. 04]] §3), so $\lg(n!)\ge Cn\lg n$ for some $C>0$ and all large $n$.
>
> Chaining: $f(n)=h\ge\lg(n!)\ge Cn\lg n$, so $f(n)=\Omega(n\lg n)$. $\blacksquare$
>
> **Notice the argument is information-theoretic:** each comparison yields one bit, you must distinguish $n!$ possibilities, so you need at least $\lg(n!)$ bits. The tree is just bookkeeping for that idea.
>
> **(c)** *(verified)*
>
> | $n$ | $n!$ | $\lg(n!)$ | lower bound $\lceil\lg n!\rceil$ | merge sort $n\lg n-n+1$ |
> |---|---|---|---|---|
> | 4 | 24 | 4.58 | **5** | **5** |
> | 8 | 40 320 | 15.30 | **16** | **17** |
> | 16 | $2.09\times10^{13}$ | 44.25 | **45** | **49** |
>
> **Merge sort matches the bound exactly at $n=4$ and exceeds it slightly beyond** — by 1 at $n=8$, by 4 at $n=16$. So merge sort is **optimal in order** ($\Theta(n\lg n)$ both ways) but **not exactly optimal**: a few comparisons are wasted relative to the information-theoretic floor.
>
> **This is the right way to read a $\Theta$ claim** — it constrains growth, not constants, and certainly not every input size. (Algorithms closer to the floor exist, e.g. merge-insertion sort, at the cost of much greater complexity.)
>
> **(d) Radix sort escapes the model, not the theorem.**
>
> The theorem constrains algorithms whose **only** operation on data is **comparing two elements**. Radix sort never compares elements: it examines individual digits and distributes items into buckets by digit value. Counting sort likewise uses values directly as array indices.
>
> **So the $n!$-leaf argument does not apply** — these algorithms are not binary decision trees over comparisons. Radix sort runs in $O(d\cdot n)$ for $d$-digit keys, which is linear when $d$ is constant.
>
> **The price is a restricted input domain.** Radix sort needs keys decomposable into a bounded number of digits from a bounded alphabet; it cannot sort arbitrary reals or user-supplied comparison functions. **Comparison sorts are universal and pay $n\lg n$; radix sort is fast and demands structure.**
>
> **The general lesson, for the third time in this subject:** *a lower bound belongs to a problem **in a model of computation**.* Ch. 04 made the point for binary search versus sorting; ch. 05 for factoring versus gcd; here for comparison versus digit-based sorting. **Whenever you meet an impossibility result, ask what model it assumes** — that is usually where the escape is.

## 📝 Summary

- A **tree** is a simple graph with a **unique simple path** between any two vertices — equivalently connected and acyclic. A **rooted** tree designates a root, giving **levels** and a **height**; the root is a *choice*, and different roots give different heights.
- **Theorem 9.2.3 — four equivalent conditions**, and use whichever is cheapest: tree / connected+acyclic / **connected with $n-1$ edges** / acyclic with $n-1$ edges. Hence a connected graph on $n$ vertices with **more** than $n-1$ edges has a cycle, and fewer is impossible. **Trees are the minimally connected graphs.**
- **Huffman codes** are rooted binary trees; because characters sit at **leaves**, no code is a prefix of another, so decoding is unambiguous. Built greedily by merging the two least-frequent items; **not unique**. Used in `gzip`, PNG and fax.
- **$G$ has a spanning tree iff $G$ is connected** — proved by repeatedly deleting an edge of a cycle, which cannot disconnect.
- **Prim** grows one tree by the cheapest crossing edge; **Kruskal** sorts all edges and adds any that avoids a cycle. **Both are greedy and both are correct** — and correctness needs proof, since greedy usually fails. The proof is an **exchange argument**: assume the partial tree extends to some MST, and swap edges around a cycle.
- **Minimal spanning trees need not be unique, but their weight is.** Two correct algorithms may return different edge sets and must return the same total — the right implementation check.
- **Theorem 9.5.4:** a full binary tree with $i$ internal vertices has $i+1$ leaves and $2i+1$ vertices. Hence a single-elimination tournament with $n$ players needs $n-1$ matches.
- **Theorem 9.5.6:** a binary tree of height $h$ has $t\le2^h$ leaves, i.e. **$h\ge\lg t$** — *to distinguish $t$ outcomes by binary decisions you need height $\lg t$.* The bound is tight, and it is the engine of §8.
- **A binary tree with $n$ leaves may have height anywhere from $\lceil\lg n\rceil$ to $n-1$.** Search costs are proportional to height, so **balanced trees exist to guarantee the best case rather than hope for it.**
- **Three traversals differ only in when the root is processed**: preorder (root first), inorder (middle), postorder (last). On an **expression tree** they give **prefix, infix and postfix** notation. **Prefix and postfix are parenthesis-free and reconstruct uniquely; inorder loses the grouping** — which is why compilers and stack machines use postfix.
- **Decision trees** represent algorithms; **the worst-case cost is the height**. Count the outcomes, bound the leaves, compare. The five-coins puzzle has 10 outcomes and a ternary tree of height 2 holds only $9$ — so 3 weighings are necessary.
- **Theorem 9.7.3: any comparison-based sort needs $\Omega(n\lg n)$ comparisons.** The decision tree is binary, needs $\ge n!$ leaves, so $h\ge\lg(n!)=\Theta(n\lg n)$. **The argument is information-theoretic:** one bit per comparison, $n!$ possibilities to distinguish.
- **Merge sort is therefore optimal in order** — $O(n\lg n)$ from [[07 - Recurrence Relations|ch. 07]] meets $\Omega(n\lg n)$ here — **but not exactly optimal** (49 comparisons against a floor of 45 at $n=16$).
- **The bound holds only in the comparison model.** Radix and counting sort beat it by never comparing elements, paying with a restricted input domain. **A lower bound belongs to a problem in a model.**

## ⚠️ Important Notes

1. **"The height of a tree" requires a root.** The same free tree has different heights under different roots, so name the root before quoting a height.
2. **Use the edge count to test treeness.** Connected with $n-1$ edges is sufficient — no cycle-hunting needed. And connected with more than $n-1$ edges *guarantees* a cycle.
3. **$n-1$ edges alone does not make a tree.** A triangle plus an isolated vertex has $4$ vertices and $3$ edges and is neither connected nor acyclic. Theorem 9.2.3 always pairs the count with connectivity **or** acyclicity.
4. **Huffman codes work because characters sit at leaves.** If a character were at an internal vertex its code would prefix its descendants' codes and decoding would be ambiguous. **The prefix-free property is structural, not a coincidence.**
5. **Greedy algorithms usually fail; Prim and Kruskal are exceptions that were proved.** Do not assume a new greedy heuristic is optimal because these two are — Johnsonbaugh's own "cheapest edge" shortest-path heuristic is a counterexample, and so is greedy coin change for arbitrary denominations.
6. **Check an MST implementation by total weight, not by edge list.** Different correct algorithms legitimately return different trees.
7. **If all edge weights are distinct, the MST is unique.** Ties are precisely where alternatives arise.
8. **Distinguish binary trees from full binary trees.** Theorem 9.5.4's $t=i+1$ needs *every* internal vertex to have exactly two children; it is false for general binary trees.
9. **Left and right children are distinguishable.** Two binary trees with mirror-image structure are different binary trees, even though the underlying rooted trees are isomorphic.
10. **Theorem 9.5.6 bounds the height from below, never from above.** A binary tree with $n$ leaves can be as tall as $n-1$. This is the entire reason for balanced trees.
11. **A plain BST degenerates on sorted input** — the worst case is not exotic but the commonest real-world arrival order. Use a balanced structure if you cannot control insertion order.
12. **Inorder traversal loses the grouping.** `3 + 5 * 2` from the tree for $(3+5)\times2$ evaluates to the wrong answer under standard precedence. If you need reconstructibility, use prefix or postfix.
13. **In a decision-tree argument, get the branching factor right.** A pan balance has **three** outcomes, so the tree is ternary and the bound is $3^h$; a comparison has two, giving $2^h$. Using the wrong base gives the wrong bound.
14. **Count outcomes, not inputs.** The five-coins puzzle has 5 coins but **10** outcomes, because "heavy or light" must also be determined. Miscounting the outcome set is the usual error.
15. **$\Omega(n\lg n)$ constrains growth, not constants.** Merge sort exceeds the information-theoretic floor by a few comparisons and is still "optimal". Do not read a $\Theta$ claim as exactness.
16. **Ask what model a lower bound assumes.** Radix sort beats $\Omega(n\lg n)$ by not comparing; hashing beats $\Omega(\lg n)$ search the same way. **The escape from an impossibility result is almost always a change of model, not a cleverer algorithm.**

> [!warning] Gaps in the source material
> **Extraction was good for prose, definitions and theorem statements**, and this chapter had two notable successes: **Theorem 9.7.3's proof survived essentially intact** — including the three-step chain and its citation of Example 4.3.9 — and **Algorithm 9.6.1 (preorder traversal) came through complete with line numbers.** Those are the only two full derivations recovered verbatim in nine chapters, and the sorting proof is the one that most needed to be.
>
> **The usual losses apply and are severe here.** The numbered Algorithms **9.1.9 (Huffman construction), 9.4.3 (Prim), 9.4.6 (alternate Prim)** and the breadth-first spanning-tree algorithm all extract as headings with input/output lines and no body; **Kruskal's algorithm is in the exercises and was never printed in full** at all. **So §4's Python is my own reconstruction** from the prose descriptions, verified by running both algorithms on a six-vertex weighted graph and confirming they return the same total weight (17) with $n-1$ edges.
>
> **Every worked example's arithmetic is lost.** Example 9.4.4 (Prim's trace) survives only as narration — "vertex 1 is added… edge (1, 3) is added" — with the weights and the graph itself in a lost figure, so **the trace in §4 uses my own verified graph rather than Johnsonbaugh's.** Examples 9.1.10 (Huffman construction from Table 9.1.2), 9.5.7, 9.6.x (traversal outputs) and the coin-puzzle decision tree are likewise unrecoverable in detail; §§5–8's examples are my own constructions, each verified computationally.
>
> **Tables 9.1.1–9.1.2 (Huffman frequencies) did not survive**, so no specific Huffman code is worked through — §1 explains the construction and the prefix-free property without a numeric instance.
>
> **All figures are images and are lost**, which matters more in this chapter than any other so far. Lost: Figures 9.1.2–9.1.16 (**every rooted-tree illustration and the entire Huffman construction sequence**), 9.2.1 (the family tree defining the terminology), 9.3.1–9.3.2 (spanning trees shown in black within a graph), 9.4.1–9.4.3 (**the weighted graph on which Prim is traced, and the contrast between a non-minimal spanning tree of weight 20 and the minimal one of weight 12**), 9.5.1–9.5.6 (binary trees, the single-elimination tournament, binary search trees), 9.6.1–9.6.2 (traversal examples), and **9.7.1–9.7.3 (the restaurant decision tree, the pan balance, and the five-coins algorithm)**. The notes describe trees by explicit parent–child structure and verify all outputs by running the traversals.
>
> **Verified computationally before writing:** Theorem 9.5.4's counts for $i=0,\dots,5$; Theorem 9.5.6's bound and its tightness at $h=3,t=8$; **the sorting lower bound $\lceil\lg(n!)\rceil$ at $n=3,4,5,8,10,16$ and its comparison with merge sort's $n\lg n-n+1$**; the five-coins outcome count ($10$) against ternary tree capacity ($3^2=9$); **Prim and Kruskal on the same graph, agreeing at weight 17**; and all three traversals on two trees, including the RPN evaluation of `3 5 + 2 *` to $16$. **No error was found in Johnsonbaugh ch. 9** — nine chapters in, the errata table in `00-Index.md` remains empty.
>
> **Additions beyond the source.** The **expression-tree application of the three traversals** (§6 and Exercise 4), including the observation that **inorder loses the grouping** so `3 + 5 * 2` evaluates wrongly, is entirely mine — Johnsonbaugh defines the traversals without any notation application, which leaves the reader with three algorithms and no reason to care about the difference. The **exchange-argument framing** of Prim's correctness proof, and the remark that this pattern is the standard way to prove greedy algorithms correct, is my own emphasis. **Exercise 3(c)'s caterpillar tree** and the best-versus-worst height table are mine, as is the explanation of why a plain BST degenerates on sorted input. The observation that **merge sort is optimal in order but not exactly optimal** — with the verified table showing 49 against a floor of 45 at $n=16$ — is my addition; Johnsonbaugh says only that merge sort "is optimal". The **information-theoretic reading** of Theorem 9.7.3 (one bit per comparison, $\lg(n!)$ bits needed) is mine, as is the closing point, now made for the third time in the subject, that **a lower bound belongs to a problem in a model** and that radix sort escapes the model rather than the theorem. The tournament argument in Exercise 1(e) (**every match eliminates one player**, so $n-1$ matches for any $n$) is a cleaner alternative to the tree count and is my own. The cross-reference from Huffman coding to **entropy** is mine.
>
> **Deliberately compressed.** **§9.8 (Isomorphisms of Trees)** is reduced to §7's short statement — Johnsonbaugh's algorithms for tree isomorphism depend on lost figures, and the useful facts (invariants prove difference only; tree isomorphism is polynomial-time unlike general graph isomorphism) fit in a paragraph. **§9.9 (Game Trees, minimax, alpha–beta pruning)** is omitted per the scope decision in `00-Index.md`, since [[Machine Learning/contents/08 - Integrating Learning and Planning|Machine Learning ch. 08]] and [[Machine Learning/contents/10 - Case Study - RL in Classic Games|ch. 10]] already cover game-tree search including MCTS. **The coin-puzzle exercises beyond the five-coin case** (four, eight and twelve coins) are not worked, though the method transfers directly. Johnsonbaugh's "Problem-Solving Corner: Trees" (p. 450) is a worked-example section distributed through §§1–2.

**Previous:** [[08 - Graph Theory]] · **Next:** [[10 - Network Flows and Matching]]
