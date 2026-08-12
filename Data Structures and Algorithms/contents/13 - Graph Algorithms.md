---
subject: Data Structures and Algorithms
chapter: 13
tags: [ds, dsa, graphs, bfs, dfs, dijkstra, bellman-ford, topological-sort, mst, prim, kruskal, union-find]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 14"
---

# Graph Algorithms

The last chapter of the subject, and the one where everything before it is used at once: [[05 - Stacks, Queues and Deques|stacks and queues]] drive the traversals, [[08 - Priority Queues and Heaps|heaps]] make Dijkstra and Prim efficient, [[09 - Maps, Hash Tables and Skip Lists|hash maps]] store the adjacency structure, and [[02 - Algorithm Analysis in Practice|complexity analysis]] decides which representation to use.

**The division of labour with [[Discrete Mathematics/contents/08 - Graph Theory|Discrete Maths]] is settled and is worth restating**, because this chapter deliberately does not re-derive things already proved:

| | Discrete Maths owns | **This chapter owns** |
|---|---|---|
| graphs as objects | ch. 08 — paths, connectivity, Euler, planarity, isomorphism | **representations and their trade-offs** |
| trees | ch. 09 — properties, spanning trees | **building them in code** |
| **correctness of Dijkstra, Prim, Kruskal** | **ch. 09 — proved there** | **implementing, measuring, and knowing when they break** |

**So: no correctness proofs here.** What this chapter adds is the engineering — and one thing the proofs alone do not convey, which is **what happens when an algorithm's hypothesis is violated.** §5 runs Dijkstra on a graph with a negative edge and shows it returning a confidently wrong answer.

## 📘 Main Knowledge

### 1. Representation decides everything

A graph is $n$ vertices and $m$ edges. **The two standard representations differ by a factor of $n$ in space**, and choosing wrongly makes every later algorithm quadratic.

**Adjacency matrix** — an $n\times n$ grid, `M[u][v]` holding the edge or `None`. **Adjacency map** — a dictionary per vertex, `{u: {v: weight}}`.

*(Verified — storage cells actually used:)*

| $n$ | density | edges | adjacency map | matrix | ratio |
|---|---|---|---|---|---|
| 1 000 | 0.2% | 981 | **1 962** | 1 000 000 | **510×** |
| 1 000 | 2% | 9 974 | **19 948** | 1 000 000 | **50×** |
| 1 000 | 50% | 249 540 | 499 080 | 1 000 000 | 2.0× |
| 2 000 | 0.2% | 3 989 | **7 978** | 4 000 000 | **501×** |

**The matrix costs $n^2$ regardless of how many edges exist.** The map costs $O(n+m)$.

> [!note] Real graphs are sparse, and that is the whole argument
> A road network, a social graph, a web graph, a dependency graph — **all have $m=O(n)$, not $O(n^2)$.** People have hundreds of friends, not millions; cities have a handful of roads each. **So the matrix wastes a factor of $n$**, measured here at **510×** for a 0.2%-dense graph.
>
> **Note the last row: at 50% density the matrix costs only 2× the map and is simpler and faster.** The matrix is not wrong — it is wrong *for sparse graphs*, which is nearly all of them.

**The operation that matters is not edge lookup but neighbour iteration:**

| 1 000 vertices | time |
|---|---|
| edge query "is $u\!-\!v$ an edge?" ×200 000 — matrix | 0.0458 s |
| edge query — adjacency map | **0.0430 s** |
| **iterate all neighbours of every vertex — matrix** | 0.0291 s |
| **iterate all neighbours — adjacency map** | **0.0008 s — 38×** |

*(Verified.)*

> [!warning] The matrix loses even its supposed advantage
> **Edge lookup is the matrix's selling point — $O(1)$ array indexing.** But an adjacency *map* is also $O(1)$, because a Python `dict` is a hash table ([[09 - Maps, Hash Tables and Skip Lists|ch. 09]]), and here it was **marginally faster**. *(An adjacency **list** of lists would be $O(\deg v)$ and genuinely slower — the "map" refinement is what closes the gap, and it is Goodrich's §14.2.3.)*
>
> **Meanwhile the matrix loses neighbour iteration by 38×**, because it must scan all $n$ cells of a row to find the few that are edges — $O(n)$ per vertex, $O(n^2)$ overall, even when $m$ is tiny.
>
> **And neighbour iteration is what every algorithm in this chapter actually does.** BFS, DFS, Dijkstra and Prim all consist of "visit a vertex, look at its neighbours". **Choosing a matrix converts every $O(n+m)$ algorithm into $O(n^2)$** — which is why adjacency lists/maps are the default.

### 2. Traversals — DFS and BFS

**Both visit every vertex and every edge once: $O(n+m)$.** They differ in one line — **which end of the pending collection you take from.**

- **DFS** uses a **stack** ([[05 - Stacks, Queues and Deques|ch. 05]]): go as deep as possible, backtrack.
- **BFS** uses a **queue**: visit everything at distance 1, then distance 2, and so on.

*(Verified on `A-B, A-C, B-D, B-E, C-F, E-F, D-G, F-G`:)*

```
DFS from A:  A B D G F C E
BFS from A:  A B C D E F G
```

**BFS solves unweighted shortest paths; DFS does not.** *(Verified:)*

| vertex | A | B | **C** | D | **E** | **F** | G |
|---|---|---|---|---|---|---|---|
| **BFS distance** | 0 | 1 | **1** | 2 | **2** | **2** | 3 |
| DFS depth reached | 0 | 1 | **5** | 2 | **5** | **4** | 3 |

> [!note] Look at vertex C
> **C is directly adjacent to A — distance 1. BFS reports 1; DFS reports 5.**
>
> **The reason is structural, not a bug.** BFS visits vertices in non-decreasing distance order, so the first time it reaches a vertex it has arrived by a shortest path. **DFS commits to a deep path first**, reaching C only after wandering through `B, D, G, F` — so its depth records *the route it happened to take*, not the shortest.
>
> **So: BFS for shortest paths and level structure; DFS for cycles, connected components, and topological ordering** — problems about *structure* rather than distance, where the deep commitment is exactly what you want.

### 3. Topological sort — ordering a DAG

> [!note] Definition
> A **topological order** of a directed graph lists the vertices so that **every edge points forward.** It answers "in what order can these dependencies be done?"

**Kahn's algorithm:** repeatedly take a vertex with in-degree 0, output it, and decrement its neighbours' in-degrees. $O(n+m)$.

*(Verified on a dependency DAG:)*

```
shirt -> socks -> underwear -> tie -> pants -> belt -> shoes -> jacket
```

**Every edge checked to point forward in this order — true.** *(The order is not unique: `socks` could go anywhere before `shoes`. Any valid order will do.)*

> [!note] The key theorem, which is really a definition test
> **A topological order exists if and only if the graph is acyclic.** If there were a cycle, each of its vertices would have to precede the next and itself — impossible.
>
> **So Kahn's algorithm doubles as a cycle detector**: if it outputs fewer vertices than the graph has, the remainder lie on cycles. *(Verified: on `a→b→c→a` it returns `None`.)*
>
> **This is why build systems, package managers, spreadsheet recalculation and task schedulers all run a topological sort** — and why they report "circular dependency" rather than looping forever. **The error message is this algorithm failing.**

### 4. Dijkstra — weighted shortest paths

**Greedy with a [[08 - Priority Queues and Heaps|priority queue]]:** repeatedly settle the closest unsettled vertex and relax its outgoing edges.

```python
        settled.add(v)                       # NEVER reconsidered -- the key assumption
        for u, w in g.neighbours(v):
            if u not in settled and d + w < dist[u]:
                dist[u] = d + w
                heapq.heappush(pq, (dist[u], u))
```

**$O((n+m)\log n)$** with a binary heap — each vertex settled once, each edge relaxed once, each heap operation $O(\log n)$.

*(Verified against distances computed by hand on a 6-vertex weighted graph:)*

| from A | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| distance | 0 | **3** | 2 | 8 | 10 | 13 |

**Note $A\to B$ is 3, not the direct edge's 4** — the route via C costs $2+1=3$. **Dijkstra found the detour**, which is the entire point. *(Bellman–Ford independently agrees on every vertex.)*

### 5. Where Dijkstra breaks — and it fails silently

**The proof of Dijkstra's correctness (in [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]) needs non-negative edge weights.** Here is what happens when that hypothesis is violated.

```
s -> u : 1        s -> v : 2        v -> u : -3        u -> w : 5
```

**Directed, and with no negative cycle** — so shortest paths are perfectly well defined.

| | s | u | v | w |
|---|---|---|---|---|
| **Dijkstra** | 0 | **1** ✗ | 2 | **6** ✗ |
| **Bellman–Ford** | 0 | **−1** ✓ | 2 | **4** ✓ |

*(Verified.)* The true distance to $u$ is $\min(1,\;2+(-3))=-1$, and to $w$ is $-1+5=4$. **Dijkstra is wrong on both.**

> [!warning] Why it fails, and why the failure is dangerous
> **Dijkstra settles $u$ at distance 1 before it ever looks at $v$** — 1 is the smallest tentative distance, so $u$ comes off the heap first. **Once settled, a vertex is never reconsidered.** When $v$ is later processed and offers $u$ a path of cost $-1$, it is too late.
>
> **That "never reconsider" step is the whole efficiency of the algorithm, and it is valid only for non-negative weights** — with them, any later path must be at least as long, since extending a path can only add cost. **A negative edge destroys that guarantee.**
>
> **The danger is that it does not crash, warn, or loop.** It returns a plausible dictionary of distances that is simply wrong — the worst failure mode there is. **And the error propagates**: $w$ is wrong because $u$ was.
>
> **The fix is Bellman–Ford**: relax *every* edge $n-1$ times, $O(nm)$. Slower, but it makes no assumption about signs, and **one extra pass detects negative cycles** — if anything still improves, some cycle has negative total weight and no shortest path exists. *(Verified: on `a→b(1)→c(−3)→a(1)`, total −1, Bellman–Ford correctly returns "no solution" rather than a number.)*
>
> **Negative weights are not exotic** — they model refunds, discounts, energy gained, currency arbitrage. **Check the sign of your weights before choosing the algorithm.**

### 6. Minimum spanning trees — two greedy algorithms, one answer

> [!note] Definition
> A **minimum spanning tree** of a connected weighted undirected graph is a spanning tree ($n-1$ edges, all vertices connected, no cycle) of minimum total weight.

**Prim:** grow one tree from a start vertex, repeatedly adding the cheapest edge leaving it. A heap gives $O(m\log n)$. **Structurally Dijkstra with one line changed** — the priority is the *edge* weight, not the accumulated distance.

**Kruskal:** sort all edges by weight and add each one that does not create a cycle. $O(m\log m)$ for the sort, and cycle detection needs **union–find**:

```python
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]       # path compression
            x = self.p[x]
        return x
```

**Union–find with path compression and union by rank is effectively $O(1)$ per operation** (inverse-Ackermann, $<5$ for any conceivable input) — which is why Kruskal's cost is dominated by the sort.

*(Verified on the §4 graph — both produce weight **13** with edges `B-C(1), A-C(2), D-E(2), E-F(3), B-D(5)`, and $6$ vertices give $5$ edges as required.)*

**And across 200 randomly generated connected weighted graphs: zero disagreements in total weight.**

> [!note] Same weight, not necessarily the same tree
> **When weights tie, several MSTs exist** and the two algorithms may return different ones — Prim's depends on the start vertex, Kruskal's on the sort's tie-breaking. **The total weight is always identical**, because that is what "minimum" means.
>
> **The correctness of both is proved in [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]** via the cut property — cross-linked, not re-proved. **What the 200-graph test adds is confidence in the *implementations***, which is a different thing from confidence in the algorithms, and is exactly the gap this subject exists to close.
>
> **Choosing between them:** Prim suits dense graphs (it never sorts all $m$ edges); Kruskal suits sparse ones and is trivially parallel after the sort. **Kruskal also works on disconnected graphs**, producing a spanning *forest*.

### 7. Scaling — all near-linear on sparse graphs

*(Verified, $m\approx3n$:)*

| $n$ | $m$ | BFS | Dijkstra | Kruskal |
|---|---|---|---|---|
| 2 000 | 5 990 | 0.0026 s | 0.0032 s | 0.0088 s |
| 4 000 | 11 983 | 0.0063 s | 0.0104 s | 0.0222 s |
| 8 000 | 23 980 | 0.0150 s | 0.0263 s | 0.0578 s |
| 16 000 | 47 984 | 0.0352 s | 0.0715 s | 0.1373 s |

**Doubling $n$ multiplies each column by roughly 2.4** — slightly above 2, exactly as $O((n+m)\log n)$ predicts when $m=O(n)$: the extra factor is the slowly-growing $\log n$. **This is [[11 - Sorting and Selection|ch. 11]]'s $n\log n$ signature again.**

**With an adjacency matrix every one of these would be $\Theta(n^2)$** — the $n=16\,000$ row alone would scan 256 million cells per traversal. **§1's representation choice is what makes this table possible.**

### 8. The chapter in one table

| algorithm | complexity | requires | solves |
|---|---|---|---|
| **BFS** | $O(n+m)$ | — | unweighted shortest paths, connectivity, levels |
| **DFS** | $O(n+m)$ | — | cycles, components, topological order |
| **topological sort** | $O(n+m)$ | **acyclic** | dependency ordering; detects cycles |
| **Dijkstra** | $O((n+m)\log n)$ | **non-negative weights** | weighted shortest paths |
| **Bellman–Ford** | $O(nm)$ | — | shortest paths with negatives; detects negative cycles |
| **Prim / Kruskal** | $O(m\log n)$ | undirected, weighted | minimum spanning tree |

## ✏️ Exercises

**1. (Representation.)** (a) Compare the two representations' space. (b) Interpret the two timing results — why did the matrix lose *both*? (c) When is a matrix right? (d) Why does this choice matter more than any other in the chapter?

> [!example]- Solution
> **(a) The matrix is $\Theta(n^2)$ always; the adjacency map is $\Theta(n+m)$.**
>
> *(Verified:)*
>
> | $n$ | density | map cells | matrix cells | ratio |
> |---|---|---|---|---|
> | 1 000 | 0.2% | 1 962 | 1 000 000 | **510×** |
> | 1 000 | 2% | 19 948 | 1 000 000 | 50× |
> | 1 000 | 50% | 499 080 | 1 000 000 | 2.0× |
>
> **The ratio is $n^2/(n+m)$**, so it shrinks as the graph fills up: 510× at 0.2% density, 2× at 50%. **Note also that doubling $n$ at fixed density kept the ratio near 500** — it is driven by density, not size.
>
> **(b) Edge lookup: the matrix's advantage evaporates because a `dict` is also $O(1)$.**
>
> The classic argument gives the matrix $O(1)$ array indexing against a list's $O(\deg v)$ scan. **But an adjacency *map* stores neighbours in a hash table** ([[09 - Maps, Hash Tables and Skip Lists|ch. 09]]), so it is also $O(1)$ — measured at 0.0430 s against the matrix's 0.0458 s, marginally *faster*. **The textbook trade-off is largely an artefact of using a list rather than a map**, which is precisely why Goodrich introduces the adjacency map as a refinement.
>
> **Neighbour iteration: the matrix loses by 38×** (0.0291 s vs 0.0008 s) because it must scan an entire row of $n$ cells to find the $\deg(v)$ that are edges. **The map stores exactly the neighbours**, so iteration is $O(\deg v)$ — optimal.
>
> **Summing over all vertices: $O(n^2)$ for the matrix versus $O(n+m)$ for the map.** With $m\approx3n$ that is a factor of ~$n/3$.
>
> **(c) When the graph is dense, small, or when $O(1)$ edge testing dominates.**
> - **Dense graphs** ($m\to n^2/2$): the 50% row shows only a 2× penalty, and the matrix is simpler with far better cache locality — contiguous memory, no pointer chasing ([[10 - Search Trees|ch. 10]] §7).
> - **Small $n$**: $n=100$ is 10 000 cells, trivial.
> - **Algorithms that test arbitrary edges rather than iterate neighbours** — Floyd–Warshall's all-pairs shortest paths is $\Theta(n^3)$ and written directly against a matrix.
> - **Numerical work**: as a NumPy array the matrix supports linear algebra — powers count walks, eigenvalues give spectral clustering. **[[Linear Algebra/contents/00-Index|Linear Algebra]] operates on exactly this object.**
>
> **(d) Because it silently changes the complexity of everything built on top.**
>
> Every algorithm here is "visit a vertex, iterate its neighbours". **With a matrix that inner step is $O(n)$ instead of $O(\deg v)$, so every $O(n+m)$ algorithm becomes $\Theta(n^2)$** — regardless of how well the algorithm itself is written.
>
> **This is the strongest instance in the subject of a theme running through it**: [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]'s array-versus-list, [[09 - Maps, Hash Tables and Skip Lists|ch. 09]]'s dict-versus-list, [[10 - Search Trees|ch. 10]]'s B-tree-versus-AVL. **The data structure, not the algorithm, usually decides the complexity** — and here the penalty is a full factor of $n$, invisible in the algorithm's own code.

**2. (Traversals.)** (a) What is the single difference between DFS and BFS? (b) Why is BFS correct for shortest paths and DFS not — read vertex C. (c) Why are both $O(n+m)$? (d) Which for which problems?

> [!example]- Solution
> **(a) Which end of the pending collection you remove from.** DFS uses a **stack** (LIFO), BFS a **queue** (FIFO) — [[05 - Stacks, Queues and Deques|ch. 05]]'s two structures. **Swapping `pop()` for `popleft()` converts one into the other**, and nothing else changes.
>
> **That one line produces completely different behaviour** — deep-first commitment versus level-by-level expansion — which is a good argument for understanding the primitive structures rather than memorising algorithms.
>
> **(b) Because BFS visits vertices in non-decreasing order of distance.**
>
> The queue holds vertices at distance $d$ before any at $d+1$, so **the first time BFS reaches a vertex it has arrived by a shortest path** — an induction on $d$. Marking on *enqueue* is what makes this work: a vertex is fixed at the smallest distance that ever reaches it.
>
> **DFS makes no such promise.** *(Verified:)*
>
> | vertex | A | B | **C** | D | E | F | G |
> |---|---|---|---|---|---|---|---|
> | BFS | 0 | 1 | **1** | 2 | 2 | 2 | 3 |
> | DFS | 0 | 1 | **5** | 2 | 5 | 4 | 3 |
>
> **C is adjacent to A — its true distance is 1. DFS reports 5.** It plunged down `A→B→D→G→F` and reached C only on the way back, recording the depth of *the route it took*.
>
> **The general point: DFS's number is the length of the path it happened to follow, which has no relation to the shortest.** It is not an approximation that is sometimes off — here it is 5× wrong on a vertex one step away.
>
> *(Note this holds only for **unweighted** graphs. With weights, fewest edges ≠ shortest, and BFS is wrong too — that is Dijkstra's job, §4.)*
>
> **(c) Because each vertex is enqueued/pushed once and each edge examined a constant number of times.**
>
> The `seen` set guarantees each vertex is processed once — $O(n)$. When processing $v$, the work is $O(\deg v)$, and $\sum_v \deg v = 2m$ (undirected) or $m$ (directed) — the **handshake lemma**, [[Discrete Mathematics/contents/08 - Graph Theory|DM ch. 08]]. **Total $O(n+m)$, which is optimal**: you cannot do better than looking at the input.
>
> **The $O(n+m)$ depends entirely on §1's representation.** With a matrix the inner loop is $O(n)$ rather than $O(\deg v)$, giving $\Theta(n^2)$.
>
> **(d)**
>
> | use BFS for | use DFS for |
> |---|---|
> | **unweighted shortest paths** | **cycle detection** |
> | connectivity, components | topological sorting |
> | level structure, bipartiteness | strongly connected components |
> | web crawling near a seed | maze/puzzle solving, backtracking |
> | | recursive structure (parsing, expression trees) |
>
> **The organising distinction: BFS answers questions about *distance*, DFS about *structure*.** DFS's deep commitment builds a recursion tree whose shape encodes the graph's structure — back edges reveal cycles, finish times give topological order. **BFS's level structure destroys that information but measures distance exactly.**
>
> **Practical note: BFS's queue can hold $O(n)$ vertices at once** (an entire level), so on a wide graph it uses more memory than DFS, whose stack holds only the current path. **On a deep graph the reverse is true**, and recursive DFS risks stack overflow — hence the iterative version used here.

**3. (Topological sort.)** (a) Define it and explain Kahn's algorithm. (b) Why does it exist iff the graph is acyclic? (c) Why is the order not unique? (d) Where does this appear in practice?

> [!example]- Solution
> **(a) A listing of the vertices in which every edge points forward** — if $u\to v$, then $u$ precedes $v$.
>
> **Kahn's algorithm:** compute every vertex's in-degree; put the in-degree-0 vertices in a queue; repeatedly remove one, output it, and decrement each neighbour's in-degree, enqueuing any that reach 0.
>
> **The invariant: a vertex is output only when everything pointing to it has already been output** — which is exactly the definition. Each vertex is enqueued once and each edge decrements once, so it is $O(n+m)$.
>
> *(Verified: `shirt → socks → underwear → tie → pants → belt → shoes → jacket`, with every edge checked to point forward.)*
>
> **(b) ($\Leftarrow$) If acyclic, one exists.** A finite DAG always has a vertex of in-degree 0 — otherwise, walking backwards from any vertex forever must revisit one, creating a cycle. Output it, delete it (the rest is still a DAG), and induct.
>
> **($\Rightarrow$) If a cycle exists, none can.** Let $v_1\to v_2\to\cdots\to v_k\to v_1$ be a cycle. A topological order would need $v_1$ before $v_2$ before … before $v_k$ before $v_1$ — **so $v_1$ precedes itself.** Contradiction.
>
> **So Kahn's algorithm is also a cycle detector**, and this is the useful form: if it outputs fewer than $n$ vertices, the missing ones all lie on or after cycles, since their in-degrees never reached 0. *(Verified: `a→b→c→a` returns `None`.)*
>
> **Detecting the failure costs nothing extra** — just compare the output length to $n$.
>
> **(c) Because vertices with no dependency between them may be ordered either way.**
>
> In the verified output, `socks` appears second, but it only constrains `shoes` — it could go anywhere before it. **`socks` and `tie` are incomparable**: no path connects them, so either order is valid.
>
> **A topological order is a *linear extension* of the partial order defined by the edges** ([[Discrete Mathematics/contents/03 - Functions, Sequences and Relations|DM ch. 03]]'s partial orders). **The graph specifies a partial order; a topological sort chooses one of the total orders compatible with it**, and there are generally many. The number of them is a classic counting problem, and computing it is #P-complete.
>
> **Practical consequence: never write a test asserting one specific order.** Assert the *property* — every edge points forward — as the verification here does.
>
> **(d) Everywhere that dependencies must be resolved.**
> - **Build systems** (`make`, Bazel): compile dependencies before dependents.
> - **Package managers** (`pip`, `apt`, `npm`): install in dependency order.
> - **Spreadsheets:** recalculate cells after the cells they reference. **A circular reference error is this algorithm reporting a cycle.**
> - **Task schedulers and CI pipelines**, course prerequisites, and **instruction scheduling** in compilers.
> - **Dataflow in ML pipelines** — including the graph execution in the [[MLOps/contents/00-Index|MLOps]] tooling.
>
> **In every case the cycle-detection half is as valuable as the ordering half**: "circular dependency detected" is a far better outcome than an infinite loop, and it is free.

**4. (Hard — Dijkstra and its hypothesis.)** (a) How does Dijkstra work and why $O((n+m)\log n)$? (b) Trace the negative-edge failure precisely. (c) Why is this failure mode especially dangerous? (d) What does Bellman–Ford give up and gain?

> [!example]- Solution
> **(a) Greedily settle the closest unsettled vertex, then relax its edges.**
>
> Maintain tentative distances, all $\infty$ except the source. Repeatedly extract the minimum from a [[08 - Priority Queues and Heaps|heap]], mark it **settled** (final), and for each neighbour check whether going through it improves the neighbour's tentative distance.
>
> **Complexity:** each vertex is settled once ($n$ extractions, $O(\log n)$ each), each edge relaxed once with at most one heap insertion ($m$ pushes, $O(\log n)$ each). **$O((n+m)\log n)$.** *(With a Fibonacci heap this improves to $O(m+n\log n)$, theoretically better but slower in practice for realistic sizes.)*
>
> *(Verified against hand computation: distances 0, 3, 2, 8, 10, 13 from A. **$A\to B$ is 3 via C rather than the direct edge's 4** — the algorithm found a cheaper detour, which is what a shortest-path algorithm is for.)*
>
> **(b)** Graph: `s→u:1`, `s→v:2`, `v→u:−3`, `u→w:5`. **Directed, no negative cycle**, so shortest paths are well defined: $d(u)=\min(1,\,2-3)=-1$ and $d(w)=-1+5=4$.
>
> **The trace:**
> 1. Settle `s` at 0. Relax: `u`←1, `v`←2.
> 2. Extract the minimum: `u` at 1 — **and mark it settled, i.e. final.** Relax `w`←6.
> 3. Extract `v` at 2. Settle. Relax `u`: $2+(-3)=-1<1$ — **but `u` is already settled, so the improvement is discarded.**
> 4. Extract `w` at 6. Done.
>
> **Result: `u`=1 and `w`=6.** *(Verified; Bellman–Ford gives the correct −1 and 4.)*
>
> **The broken assumption is at step 2.** Dijkstra settles a vertex the moment it is the closest unsettled one, justified by: *any other route reaches it via some unsettled vertex at distance $\ge$ the current one, and extending a path only adds cost, so no route can be shorter.* **"Extending a path only adds cost" is false with a negative edge** — and $w$'s error is *inherited*, showing the corruption propagates.
>
> **(c) Because it fails silently, plausibly, and contagiously.**
>
> **No exception, no warning, no infinite loop.** It returns a well-formed dictionary of finite distances that looks entirely reasonable — you would need the true answer to notice.
>
> **Contrast the other failures in this subject.** [[11 - Sorting and Selection|Ch. 11]]'s quicksort on sorted input is still *correct*, just slow — and slowness is observable. **Here the answer is wrong**, and downstream computation (`w` = 6) compounds it.
>
> **And negative weights are not exotic**: refunds and discounts in cost models, energy recovered in physical routing, profit as negative cost, exchange rates where arbitrage is literally a negative cycle. **The mistake is easy to make** — you model a discount as a negative edge, and the library function returns a number.
>
> **The rule: check the sign of your weights before choosing the algorithm.** Some libraries (SciPy's `dijkstra`) raise on negative weights; many do not.
>
> **(d) It gives up speed: $O(nm)$ against $O((n+m)\log n)$** — on a sparse graph with $m\approx3n$ that is $O(n^2)$ versus $O(n\log n)$, so it is much slower at scale.
>
> **It gains generality and a second capability.**
>
> **Generality:** it makes no assumption about signs, because it abandons the greedy commitment entirely. It relaxes **every** edge, $n-1$ times. After $k$ passes every shortest path using $\le k$ edges is correct; since a shortest path in an $n$-vertex graph uses at most $n-1$ edges, $n-1$ passes suffice. **Nothing is ever "settled", so nothing can be prematurely finalised.**
>
> **Negative-cycle detection:** run one more pass. **If anything still improves, some cycle has negative total weight** — and then no shortest path exists at all, because going round again always costs less. *(Verified: on `a→b(1)→c(−3)→a(1)`, total −1, it returns "no solution" rather than a number — the honest answer.)*
>
> **This capability is used for its own sake**, not just as a safety check: a negative cycle in a currency-exchange graph *is* an arbitrage opportunity, and Bellman–Ford is how you find one.
>
> **Choosing: Dijkstra when weights are non-negative** (the common case — distances, times, costs). **Bellman–Ford when they may not be**, or when you need cycle detection. *(Johnson's algorithm combines both: run Bellman–Ford once to reweight edges non-negatively, then Dijkstra from every vertex — all-pairs shortest paths with negative edges allowed.)*

**5. (Hard — MSTs, and the subject as a whole.)** (a) Compare Prim and Kruskal. (b) Why does union–find matter, and why is Prim "Dijkstra with one line changed"? (c) Both gave weight 13 and 200 tests agreed — what does that establish and what does it not? (d) Interpret the scaling table and name what this chapter borrowed from earlier ones.

> [!example]- Solution
> **(a) Both greedy, differing in what they grow.**
>
> **Prim grows one connected tree**, repeatedly adding the cheapest edge leaving it. It needs a heap of *frontier edges*: $O(m\log n)$. **Kruskal grows a forest**, sorting all edges and adding any that joins two different components: $O(m\log m)$ for the sort, plus near-constant union–find.
>
> | | Prim | Kruskal |
> |---|---|---|
> | maintains | one tree | a forest |
> | needs | priority queue | sorting + union–find |
> | suits | **dense** graphs | **sparse** graphs |
> | disconnected input | fails (one component only) | **gives a spanning forest** |
> | parallelism | inherently sequential | trivially parallel after the sort |
>
> **Prim suits dense graphs** because it never sorts all $m$ edges — with $m\approx n^2$ that matters. **Kruskal suits sparse ones** and handles disconnected graphs naturally.
>
> **(b) Union–find is what makes Kruskal's cycle test affordable.** "Would this edge create a cycle?" is equivalent to "are its endpoints already connected?" — and a naive check (BFS/DFS per edge) would be $O(m\cdot n)$, swamping the sort.
>
> **Union–find answers it in near-constant time** with two optimisations: **path compression** (point every node directly at the root during `find`) and **union by rank** (attach the shorter tree under the taller). Together they give amortised $O(\alpha(n))$ — inverse Ackermann, **below 5 for any input that fits in the universe.** *(This is [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]'s amortised analysis again, on its most extreme example.)*
>
> **So Kruskal's real cost is the sort**, and this is a good illustration of a supporting structure determining an algorithm's complexity.
>
> **Prim is Dijkstra with the priority changed.** Both grow a set from a start vertex, both use a heap, both relax neighbours. **The only difference:**
>
> | | priority |
> |---|---|
> | Dijkstra | $d(v)+w(v,u)$ — accumulated distance from the source |
> | **Prim** | $w(v,u)$ — the edge weight alone |
>
> **Dijkstra minimises distance *from the source*; Prim minimises the cost of *attaching* the next vertex.** That is why Dijkstra's tree is a shortest-path tree and Prim's is a minimum spanning tree — **and the two are generally different.** A shortest-path tree can have far larger total weight than the MST, which is a genuinely common confusion: **the MST does not give shortest paths, and the shortest-path tree is not minimal.**
>
> **(c) It establishes that my implementations are consistent; it does not prove the algorithms correct.**
>
> **What the tests give:** on the worked graph both produced weight 13 with the same 5 edges — checked against $n-1=5$ for 6 vertices — and across **200 random connected weighted graphs the total weights never disagreed.** Two independently written algorithms agreeing on 200 inputs is strong evidence that neither has a coding error, since a bug would have to affect both identically.
>
> **What it does not give:** 200 random graphs are not a proof. They may miss structures a proof covers automatically, and **both could share a misconception I hold about the problem** — agreement is only as strong as the algorithms' independence.
>
> **The proofs are in [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]]**, via the cut property: for any partition of the vertices, the lightest crossing edge is in some MST. Both algorithms only ever add such an edge.
>
> **This is exactly the boundary the two subjects were split along** — Discrete Maths proves the algorithm correct; this subject verifies the *implementation* is a faithful realisation of it. **Both are necessary and neither substitutes for the other**: a proved algorithm can be wrongly coded, and a well-tested implementation of a wrong algorithm is still wrong. *(§5's Dijkstra failure is the sharp case — the implementation is faithful and the *hypothesis* was violated, which no amount of testing on non-negative graphs would ever reveal.)*
>
> **(d)**
>
> | $n$ | $m$ | BFS | Dijkstra | Kruskal |
> |---|---|---|---|---|
> | 2 000 | 5 990 | 0.0026 s | 0.0032 s | 0.0088 s |
> | 16 000 | 47 984 | 0.0352 s | 0.0715 s | 0.1373 s |
>
> **Each doubling multiplies the times by about 2.4** — just above linear, matching $O((n+m)\log n)$ with $m=O(n)$, where the excess over 2 is the $\log n$ factor. **The same signature as [[11 - Sorting and Selection|ch. 11]]'s merge-sort (2.09, 2.10).**
>
> **The whole table depends on §1's representation.** With a matrix, every row would be $\Theta(n^2)$ — at $n=16\,000$, 256 million cells scanned per traversal instead of 48 000 edges, roughly 5 000× more work.
>
> **What this chapter borrowed:**
>
> | from | used for |
> |---|---|
> | [[05 - Stacks, Queues and Deques\|ch. 05]] stacks & queues | **the only difference between DFS and BFS** |
> | [[08 - Priority Queues and Heaps\|ch. 08]] heaps | Dijkstra's and Prim's $\log n$ factor |
> | [[09 - Maps, Hash Tables and Skip Lists\|ch. 09]] hash maps | adjacency maps — $O(1)$ edge lookup, which is why the matrix lost |
> | [[11 - Sorting and Selection\|ch. 11]] sorting | Kruskal's dominant cost |
> | [[04 - Array-Based Sequences and Amortised Analysis\|ch. 04]] amortised analysis | union–find's $\alpha(n)$ |
> | [[02 - Algorithm Analysis in Practice\|ch. 02]] doubling method | every measurement above |
> | [[Discrete Mathematics/contents/08 - Graph Theory\|DM ch. 08–09]] | handshake lemma, cut property, all correctness proofs |
>
> **Graph algorithms are where the subject's parts combine**, and that is a fair note to end on: **the value of the earlier chapters is not the individual structures but that they compose.**

## 📝 Summary

- **Representation decides everything.** A matrix costs $\Theta(n^2)$ always; an adjacency map costs $\Theta(n+m)$. *(Measured: **510×** more cells at 0.2% density, but only 2× at 50% — real graphs are sparse.)*
- **The matrix loses both benchmarks.** Edge lookup was a tie (0.0430 s vs 0.0458 s) because a Python `dict` is a hash table ([[09 - Maps, Hash Tables and Skip Lists|ch. 09]]); **neighbour iteration lost by 38×**, because a row scan is $O(n)$ whether or not edges exist.
- **Neighbour iteration is what every graph algorithm does**, so **choosing a matrix silently turns every $O(n+m)$ algorithm into $\Theta(n^2)$.**
- **DFS and BFS differ in one line** — stack versus queue ([[05 - Stacks, Queues and Deques|ch. 05]]). Both are $O(n+m)$ by the handshake lemma.
- **BFS solves unweighted shortest paths; DFS does not.** *(Verified: vertex C is adjacent to A, so distance 1 — BFS reports 1, **DFS reports 5**.)* BFS answers questions about *distance*, DFS about *structure*.
- **Topological sort orders a DAG so every edge points forward** ($O(n+m)$ by Kahn's algorithm), and **exists iff the graph is acyclic** — so it doubles as a cycle detector, for free. *(Verified both ways.)* **The order is not unique** — it is a linear extension of a partial order, so test the property, never a specific order.
- **Dijkstra settles the closest unsettled vertex and never reconsiders it** — $O((n+m)\log n)$ with a [[08 - Priority Queues and Heaps|heap]]. *(Verified against hand computation, including a 3-cost detour beating a direct edge of 4.)*
- **Dijkstra is wrong with negative edges, and fails silently.** *(Verified: true distances −1 and 4; Dijkstra returned **1 and 6** — no error, no warning, and the second error inherited from the first.)*
- **The broken assumption is "extending a path only adds cost"**, which justifies never revisiting a settled vertex. **Check the sign of your weights before choosing the algorithm.**
- **Bellman–Ford relaxes every edge $n-1$ times** — $O(nm)$, no sign assumption, and **one extra pass detects negative cycles** *(verified: correctly reported "no solution" rather than a number)*.
- **Prim and Kruskal are both greedy and always give the same total weight** *(verified: weight 13 on the worked graph, and **0 disagreements across 200 random graphs**)* — though the trees may differ when weights tie.
- **Union–find with path compression and union by rank is $O(\alpha(n))$**, effectively constant, which is why Kruskal's cost is the sort.
- **Prim is Dijkstra with one line changed** — the priority is the edge weight, not the accumulated distance. **Hence an MST is not a shortest-path tree**, a common confusion.
- **All these are near-linear on sparse graphs** *(measured: ×2.4 per doubling, the $O((n+m)\log n)$ signature)* — but only because of the representation chosen in §1.
- **Testing 200 graphs verifies the implementation, not the algorithm.** The correctness proofs live in [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]], and §5 shows why both are needed: there the implementation was faithful and the *hypothesis* was violated.

## ⚠️ Important Notes

1. **Use an adjacency list/map unless the graph is genuinely dense.** A matrix wastes $\Theta(n^2)$ and turns linear algorithms quadratic.
2. **Use an adjacency *map* (dict of dicts), not a list of lists** — you keep $O(1)$ edge lookup *and* $O(\deg v)$ iteration, which is why the matrix had no advantage left.
3. **A matrix is right for dense graphs, small $n$, all-pairs algorithms (Floyd–Warshall), and numerical work** where NumPy operates on it directly.
4. **DFS's depth is not a distance.** Use BFS for unweighted shortest paths — DFS was 5× wrong on a directly adjacent vertex.
5. **BFS is only correct for shortest paths when edges are unweighted.** With weights, fewest edges ≠ shortest path; use Dijkstra.
6. **Mark vertices as seen on *enqueue*, not on dequeue**, or a vertex can enter the queue many times and the distances break.
7. **Prefer iterative DFS.** Recursive DFS overflows the stack on deep graphs; Python's default limit is ~1 000.
8. **A topological order exists iff the graph is acyclic** — so compare the output length with $n$ and get cycle detection free.
9. **Never assert one specific topological order in a test.** Assert that every edge points forward; many valid orders exist.
10. **Dijkstra requires non-negative weights.** With a negative edge it returns a *wrong answer* with no error — the most dangerous failure mode, and the error propagates downstream.
11. **Use Bellman–Ford when weights may be negative**, and use its extra pass deliberately: **a negative cycle means no shortest path exists**, and finding one is a useful result in its own right (currency arbitrage).
12. **A minimum spanning tree is not a shortest-path tree.** Prim and Dijkstra differ in one line and answer different questions.
13. **Prim needs a connected graph; Kruskal handles disconnected input**, producing a spanning forest.
14. **MSTs are not unique when weights tie**, but the total weight is. Compare weights in tests, not edge sets.
15. **Union–find needs both path compression and union by rank** to reach $\alpha(n)$; with neither it degrades to $O(n)$ per operation and Kruskal becomes quadratic.
16. **Agreement between two implementations is evidence, not proof.** The proofs are in [[Discrete Mathematics/contents/09 - Trees|DM ch. 09]] — and §5 shows a case where the implementation was right and the *assumption* was wrong, which no test on valid inputs would ever catch.

> [!warning] Gaps in the source material
> **Goodrich's ch. 14 prose extracts well** — the graph ADT, the four representations (edge list, adjacency list, adjacency map, adjacency matrix) with their performance tables, Propositions 14.8–14.11, DFS and BFS, topological ordering, Dijkstra, and both MST algorithms all came through readably. **Goodrich page $n$ = PDF page $n+22$; ch. 14 is PDF 642–718.**
>
> **His code did not**, per the standing problem in `00-Index.md`, and **Lambert has no graph chapter.** So **every implementation here is my own**: `GraphList` (adjacency map) and `GraphMatrix`, iterative `dfs`/`bfs` with distance tracking, Kahn's `topo_sort`, `dijkstra`, `bellman_ford`, `prim`, `kruskal`, and the `DSU` union–find with path compression and union by rank. **All were executed**, with Dijkstra checked against distances computed by hand, Dijkstra and Bellman–Ford cross-checked, the topological order verified edge-by-edge rather than against a fixed expected string, and **Prim and Kruskal cross-validated on 200 randomly generated connected weighted graphs (0 disagreements).**
>
> **All measurements are my own**: the sparse/dense storage table, both representation benchmarks, the BFS/DFS distance comparison, the negative-edge failure, and the scaling table.
>
> **All figures are images and are lost** — every graph drawing in the chapter, including Figs. 14.1–14.6 (the representations), the DFS/BFS illustrations, and the step-by-step Dijkstra and MST traces. **This is a serious loss for a subject taught almost entirely through pictures.** Compensated by printing actual traversal orders, distance dictionaries and MST edge sets from running code, and by choosing worked examples small enough to check by hand (8 edges for the traversals, 9 for the weighted graph, 4 vertices for the Dijkstra failure). **The reader should draw the §2 graph and trace both traversals.**
>
> **No error was found in Goodrich ch. 14.**
>
> **Additions beyond the source.** **§5 — Dijkstra's failure on a negative edge — is entirely mine and is the most important thing in the chapter.** Goodrich states the non-negativity requirement; he does not demonstrate what violating it does. **Constructing a graph where Dijkstra returns a confidently wrong answer (1 and 6 against the true −1 and 4), and contrasting it with Bellman–Ford, converts a footnote into something memorable.** **Bellman–Ford itself is an addition** — Goodrich does not cover it — as is the negative-cycle detection demonstration. **The §1 measurements are mine**, and the finding that **an adjacency *map* ties the matrix even on edge lookup** materially weakens the textbook trade-off as usually stated. **The DFS-versus-BFS distance table** (vertex C at 1 versus 5) is my own experiment. The 200-graph Prim/Kruskal cross-validation, the scaling table, the observation that **Prim is Dijkstra with one line changed**, and Exercise 5(d)'s summary of what this chapter borrowed from the rest of the subject are all additions.
>
> **Deliberately compressed.** **Floyd–Warshall and transitive closure** (Goodrich §14.4) are mentioned in Exercise 1(c) as the case where a matrix is the right representation, but not implemented — $\Theta(n^3)$ all-pairs shortest paths is a natural DP exercise and belongs conceptually with [[12 - Text Processing and Dynamic Programming|ch. 12]]. **The edge-list representation** (§14.2.1) is omitted; it is dominated by the adjacency map for every operation and exists in the book mainly as a stepping stone. **Strongly connected components** (Tarjan/Kosaraju) are named in Exercise 2(d) but not developed. **DFS's edge classification** (tree/back/forward/cross edges) is not covered, though it is the standard route to cycle detection via DFS — Kahn's algorithm gives the same result more simply. **Johnson's algorithm** is mentioned in Exercise 4(d) only. **The handshake lemma and the cut property are cited from [[Discrete Mathematics/contents/08 - Graph Theory|DM ch. 08–09]] rather than proved**, per the boundary recorded in both indexes.

**Previous:** [[12 - Text Processing and Dynamic Programming]] · **Next:** *(end of subject — see [[00-Index]])*
