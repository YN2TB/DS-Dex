---
subject: Discrete Mathematics
chapter: 8
tags: [ds, discrete-mathematics, graph-theory, euler-cycles, hamiltonian-cycles, dijkstra, adjacency-matrix, planarity, isomorphism]
source: "Johnsonbaugh, *Discrete Mathematics* 8e, ch. 8 (book pp. 373–437)"
---

# Graph Theory

Graph theory begins with a specific puzzle. In 1736 Leonhard Euler asked whether one could walk through Königsberg crossing each of its seven bridges exactly once and returning to the start. His answer — and more importantly his *method* — created the subject, and **the paper is generally taken to be the first in graph theory.**

The reason graphs matter here is that they are the universal model for anything discrete and connected. [[03 - Functions, Sequences and Relations|Ch. 03]] §5 already noted that **a relation on a finite set *is* a directed graph**, and §7 there promised that **$(A^k)_{ij}$ counts walks of length $k$** — §7 below cashes that in. [[06 - Counting Methods and the Pigeonhole Principle|Ch. 06]]'s Exercise 5(c) proved, as a pigeonhole exercise, that no finite simple graph has all degrees distinct.

One structural warning about this chapter: **two of its central questions look almost identical and are utterly different in difficulty.** Euler cycles (use every *edge*) have a clean necessary-and-sufficient condition and a fast algorithm. Hamiltonian cycles (visit every *vertex*) have neither, and the problem is NP-complete. §§4–5 is the contrast.

## 📘 Main Knowledge

### 1. Graphs

> [!note] Definition
> A **graph** (or **undirected graph**) $G=(V,E)$ consists of a set $V$ of **vertices** and a set $E$ of **edges**, each edge associated with an unordered pair of vertices.

The definition permits two things worth naming. **Parallel edges** are distinct edges joining the same pair; a **loop** joins a vertex to itself. A graph with neither is a **simple graph**, and most theorems below assume one.

In a **weighted graph** each edge carries a number — a distance, cost or time. The **length** of a path in a weighted graph is the sum of its edge weights.

**Two families that recur constantly:**

| Graph | Definition | $|V|$ | $|E|$ | degrees |
|---|---|---|---|---|
| **$K_n$**, complete graph | simple graph on $n$ vertices with an edge between *every* pair | $n$ | $\binom n2=\frac{n(n-1)}2$ | all $n-1$ |
| **$K_{m,n}$**, complete bipartite | vertices split $m+n$; every vertex of one part joined to every vertex of the other, none within a part | $m+n$ | $mn$ | $n$ (in the $m$-part), $m$ (in the $n$-part) |

*(Verified: $K_3,K_4,K_5,K_6$ have $3,6,10,15$ edges; $K_{3,3}$ has $9$.)*

> [!note] Definition — bipartite
> $G=(V,E)$ is **bipartite** if $V$ can be split into disjoint $V_1,V_2$ such that **every edge joins a vertex of $V_1$ to a vertex of $V_2$** — no edge lies within a part.

**To show a graph *is* bipartite, exhibit the split.** Colour a vertex, then force the colours of its neighbours, and continue; if you never need to give a vertex both colours, you have the partition. **To show it is *not*, argue by contradiction** — trace the forced colours until some vertex must lie in both $V_1$ and $V_2$.

> [!note] The real criterion, worth knowing
> A graph is bipartite **iff it contains no cycle of odd length.** The forced-colouring procedure is exactly a search for an odd cycle: two-colouring succeeds precisely when every cycle alternates, which requires even length.
>
> So $K_3$ is not bipartite (a triangle is an odd cycle), and neither is any $K_n$ for $n\ge3$. But $K_1$ and $K_2$ are — $K_1$ vacuously, taking $V_1=\{v\}$ and $V_2=\emptyset$. *(This criterion is not stated in Johnsonbaugh ch. 8; it is the standard characterisation and it makes the trial-and-error procedure into a theorem.)*

### 2. Paths, cycles, connectivity

> [!note] Definitions
> A **path** from $v_0$ to $v_n$ of length $n$ is an alternating sequence of vertices and edges $v_0,e_1,v_1,\dots,e_n,v_n$ where each $e_i$ is incident on $v_{i-1}$ and $v_i$.
>
> - A **simple path** has **no repeated vertices**.
> - A **cycle** (circuit) is a path of nonzero length from $v$ to $v$ with **no repeated edges**.
> - A **simple cycle** is a cycle with no repeated vertices except the shared start/end.
>
> $G$ is **connected** if for any vertices $v,w$ there is a path from $v$ to $w$.

A **subgraph** of $G=(V,E)$ is a graph $(V',E')$ with $V'\subseteq V$, $E'\subseteq E$, and every edge of $E'$ incident only on vertices of $V'$. A **component** of $G$ is a maximal connected subgraph — informally, one "piece". **A connected graph has exactly one component.**

> [!note] Components are equivalence classes
> Define $v\sim w$ iff there is a path from $v$ to $w$. This is an **equivalence relation** — reflexive (the length-0 path), symmetric (reverse the path), transitive (concatenate) — and **its equivalence classes are exactly the components.** So [[03 - Functions, Sequences and Relations|ch. 03]] §6's theorem that equivalence relations partition a set is what guarantees that "the components" is a well-defined decomposition with every vertex in exactly one. *(This framing is my own; Johnsonbaugh defines components directly.)*

### 3. Degree and the handshaking lemma

The **degree** $\delta(v)$ of a vertex is the number of edges incident on it, **with each loop counting 2**.

> [!note] Theorem — the handshaking lemma
> $$\sum_{v\in V}\delta(v)=2|E| .$$
> **Corollary: the number of vertices of odd degree is even.**

*Proof.* Each edge contributes exactly 2 to the total degree — one at each endpoint, or twice at the same vertex if it is a loop. The corollary follows because the sum is even, so the odd terms must pair up. $\blacksquare$

*(Verified on Johnsonbaugh's Example 8.5.2 graph: degrees $2,3,3,2,2$ summing to $12=2\cdot6$ edges, with exactly $2$ odd-degree vertices.)*

**This tiny lemma does an enormous amount of work** — it is the reason §4's theorem is about *even* degrees, and it immediately settles questions like "can nine people each shake exactly three hands?" (No: nine odd degrees is an odd count.)

### 4. Euler cycles — the solvable problem

> [!note] Definition
> An **Euler cycle** in $G$ is a cycle that includes **every edge and every vertex** of $G$.

**The Königsberg bridge problem** becomes: does the graph with one vertex per landmass and one edge per bridge have an Euler cycle? The four vertices have degrees $3,3,3,5$.

> [!note] Theorem (8.2.17 and 8.2.18 together)
> **$G$ has an Euler cycle if and only if $G$ is connected and every vertex has even degree.**

*(⟹)* If a cycle uses every edge and never repeats one, then each visit to a vertex consumes exactly two edge-ends — one arriving, one leaving — so every degree is even. And any two vertices are joined by a stretch of the cycle, so $G$ is connected.

*(⟸)* The converse is proved by **strong induction on the number of edges** ([[02 - Proofs and Mathematical Induction|ch. 02]] §7): remove a suitable cycle, apply the hypothesis to the components of what remains — each still has all degrees even — and splice the pieces back together at a shared vertex.

**So Königsberg is impossible:** all four degrees are odd. *(Verified: degree sum $14$, so $7$ bridges ✓, and $4$ odd-degree vertices.)* Euler's insight was that the *shape* of the city is irrelevant — only the degree parities matter.

> [!note] Euler *paths* — the useful variant
> If exactly **two** vertices have odd degree, there is no Euler cycle but there **is** an Euler *path* (a trail using every edge, starting and ending at the two odd vertices). By the handshaking corollary the number of odd vertices is always even, so the only cases are:
>
> | odd-degree vertices | conclusion |
> |---|---|
> | $0$ | Euler **cycle** exists (if connected) |
> | $2$ | Euler **path** exists, from one odd vertex to the other |
> | $\ge4$ | neither |
>
> **This is why "draw this figure without lifting your pen" puzzles are decidable at a glance** — count the odd-degree vertices. *(The Euler-path case is in Johnsonbaugh's exercises rather than the text; the table is my own.)*

### 5. Hamiltonian cycles — the hard problem

> [!note] Definition
> A **Hamiltonian cycle** is a cycle that visits **every vertex exactly once**, except that the start vertex appears twice.

The definitions of Euler and Hamiltonian cycles differ by one word — *edges* versus *vertices* — and **everything about them differs**:

| | Euler cycle | Hamiltonian cycle |
|---|---|---|
| covers | every **edge** | every **vertex** |
| characterisation | **iff** connected and all degrees even | **none known** |
| deciding existence | linear time | **NP-complete** |
| finding one | easy (Hierholzer) | no polynomial algorithm known |

**There is no known necessary-and-sufficient condition for a Hamiltonian cycle**, and the problem is NP-complete — so a polynomial-time algorithm for it would give one for every problem in NP. Johnsonbaugh notes that a graph with odd-degree vertices (hence no Euler cycle) may perfectly well have a Hamiltonian cycle, and conversely. **The two properties are independent.**

**How to prove a graph has *no* Hamiltonian cycle.** Since every vertex of a Hamiltonian cycle has degree exactly 2 *within the cycle*, two arguments are available:

1. **Forced edges.** If $\delta(v)=2$, **both** its edges must be in the cycle. Accumulate forced edges; if they form a cycle shorter than $n$, or give some vertex three cycle-edges, there is no Hamiltonian cycle.
2. **Forced deletions.** If $\delta(v)>2$, all but two of its edges must be deleted. If the deletions leave too few edges to form an $n$-cycle, none exists.

> [!warning] The second argument is easy to get wrong
> Johnsonbaugh flags the trap explicitly. When you delete edges at several high-degree vertices, **the same edge may be deleted twice** — it has two endpoints. Counting each deletion separately therefore *overcounts*, and you can "prove" that a graph has no Hamiltonian cycle when it does. His Figure 8.3.6 is exactly such a graph: the flawed argument concludes there is no Hamiltonian cycle, and one exists.
>
> **When counting forced deletions, count *edges removed*, not *deletions performed*.**

**The traveling salesperson problem (TSP)** asks for a **minimum-length** Hamiltonian cycle in a weighted graph — cities as vertices, distances as weights. It is at least as hard as finding any Hamiltonian cycle, and in practice is attacked with approximation algorithms and heuristics rather than solved exactly. *(Cross-reference: [[Optimization/contents/09 - Linear Programming and the Simplex Method|Optimization ch. 09]]'s LP relaxations and [[Optimization/contents/12 - Convex Programming and Constrained Algorithms|ch. 12]]'s remarks on intractability are the standard modern route.)*

> [!example]- Gray codes: the $n$-cube always has a Hamiltonian cycle
> The **$n$-cube** has $2^n$ vertices labelled by $n$-bit strings, with an edge between labels differing in exactly one bit. A Hamiltonian cycle is therefore a listing of all $2^n$ bit strings in which **consecutive strings differ in one bit** — a **Gray code**.
>
> Johnsonbaugh's construction (Theorem 8.3.6) is recursive: take the list $G_{n-1}$, prefix every entry with $0$; then append $G_{n-1}$ **reversed** with every entry prefixed $1$. For $n=3$:
> $$000,\ 001,\ 011,\ 010,\ 110,\ 111,\ 101,\ 100$$
> *(Verified: every consecutive pair — including the wrap-around from $100$ back to $000$ — differs in exactly one bit.)* **So the $n$-cube has a Hamiltonian cycle for every $n\ge2$** (Corollary 8.3.7).
>
> **Gray codes are genuinely used:** in rotary encoders and analogue-to-digital converters, where an ordinary binary counter passing from $011$ to $100$ changes three bits at once and a momentary misread can give a wildly wrong value. With a Gray code only one bit ever changes, so the worst misread is off by one.

### 6. Dijkstra's shortest-path algorithm

Given a weighted graph with **nonnegative** weights and a source $a$, find the shortest path to every other vertex.

**The idea.** Maintain a tentative distance $d(v)$ for every vertex ($0$ for the source, $\infty$ otherwise) and a set of *finished* vertices. Repeatedly take the unfinished vertex $u$ of smallest $d(u)$, declare it finished, and **relax** its edges: for each neighbour $v$, if $d(u)+w(u,v)<d(v)$, improve $d(v)$.

```python
import heapq

def dijkstra(adj, src):              # adj[u] = {v: weight}
    dist = {v: float('inf') for v in adj}
    dist[src] = 0
    pq, done = [(0, src)], set()
    while pq:
        du, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)
        for v, w in adj[u].items():
            if du + w < dist[v]:
                dist[v] = du + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

**Why it is correct** is worth stating, because it is where the nonnegativity hypothesis lives. When $u$ is chosen as the minimum, no unfinished vertex has a smaller tentative distance; any *other* route to $u$ would have to pass through some unfinished vertex first, and since weights are nonnegative that route can only be longer. So $d(u)$ is final. **This is a greedy argument, and it fails the moment a negative weight is allowed** — a later negative edge could make a longer-looking prefix win. (Bellman–Ford handles negative weights; Dijkstra does not.)

*(Verified on a four-vertex example: from $a$ with edges $ab{=}2$, $ac{=}5$, $bc{=}1$, $bd{=}6$, $cd{=}3$, Dijkstra gives $d(b)=2$, $d(c)=3$, $d(d)=6$ — and the route to $d$ is $a\to b\to c\to d$ at $2+1+3=6$, beating $a\to c\to d=8$ and $a\to b\to d=8$. **Note the greedy choice was not the direct edge**, which is the point of the algorithm.)*

### 7. Representations, and why $A^k$ counts walks

**The adjacency matrix.** Fix an ordering of the vertices. Entry $(i,j)$ with $i\ne j$ is the **number of edges** joining $v_i$ and $v_j$; entry $(i,i)$ is **twice** the number of loops at $v_i$. The matrix is **symmetric**, so it stores every off-diagonal fact twice — which is why it is space-inefficient for sparse graphs (adjacency *lists* are the practical choice, and [[Data Structures and Algorithms/contents/00-Index|DSA]] owns that comparison).

**The degree of $v_i$ is the sum of row $i$** — immediate from the definition, and the reason loops count twice.

> [!note] Theorem — powers of the adjacency matrix
> If $A$ is the adjacency matrix of a simple graph with vertices labelled $1,\dots,n$, then the $(i,j)$ entry of $A^k$ is **the number of paths of length $k$ from $v_i$ to $v_j$.**

**And the proof is just what matrix multiplication does.** Entry $(i,j)$ of $A^2$ is $\sum_m A_{im}A_{mj}$, which counts the intermediate vertices $m$ adjacent to both $i$ and $j$ — i.e. the two-step routes. Induction on $k$ extends it. **This is exactly [[03 - Functions, Sequences and Relations|ch. 03]] §7's promise**, where the same identity appeared for relations and composition: $A_1A_2$ gives the matrix of $R_2\circ R_1$.

> [!example]- Verified against the book (Example 8.5.2)
> For the graph on $\{a,b,c,d,e\}$ with $A$ as below:
> $$A=\begin{pmatrix}0&1&0&1&0\\1&0&1&0&1\\0&1&0&1&1\\1&0&1&0&0\\0&1&1&0&0\end{pmatrix} \qquad A^2=\begin{pmatrix}2&0&2&0&1\\0&3&1&2&1\\2&1&3&0&1\\0&2&0&2&1\\1&1&1&1&2\end{pmatrix}$$
> **This is one of the few displays in the book that survived extraction, and recomputing it confirms the printed matrix exactly.**
>
> Read the entries: $(A^2)_{ac}=2$, and indeed there are two length-2 walks $a\to b\to c$ and $a\to d\to c$ *(verified — $b$ and $d$ are the common neighbours)*. And $(A^2)_{aa}=2$ counts $a\to b\to a$ and $a\to d\to a$, which is just $\delta(a)=2$ — **diagonal entries of $A^2$ are the degrees.**
>
> **Warning: these are *walks*, not simple paths.** $a\to b\to a$ repeats a vertex. If you want simple paths, $A^k$ over-counts.

An **incidence matrix** instead has rows for vertices and columns for edges, with a $1$ when the vertex is on the edge. It is the natural representation when edges carry identity.

### 8. Isomorphism

Two graphs are **isomorphic** if there is a bijection between their vertex sets preserving adjacency — informally, they are the same graph relabelled. Deciding isomorphism is subtle: the definition quantifies over all $n!$ bijections.

**In practice one uses invariants** — quantities preserved by isomorphism. If two graphs differ in any invariant they are **not** isomorphic:

- number of vertices; number of edges;
- the **degree sequence** (the multiset of degrees);
- number of components; number of simple cycles of each length;
- whether bipartite, whether planar.

> [!warning] Invariants can only prove graphs *different*
> Matching invariants do **not** prove isomorphism. Two graphs can agree on all the invariants above and still be non-isomorphic — to establish isomorphism you must **exhibit the bijection**.
>
> **This is the asymmetry of [[01 - Sets and Logic|ch. 01]] §5 again:** the existential claim ("an isomorphism exists") needs a witness; the universal claim implied by a differing invariant needs only that one difference.

### 9. Planar graphs

> [!note] Definition
> A graph is **planar** if it can be drawn in the plane with **no edges crossing**.

The motivating application is real: a printed circuit board cannot have crossing conductors on one layer, so **planarity decides whether a circuit needs a second layer.**

When a connected planar graph is drawn, the plane is divided into **faces** — regions bounded by cycles, **including the unbounded outer face.**

> [!note] Theorem — Euler's formula (1752)
> For any connected planar graph drawn in the plane, with $v$ vertices, $e$ edges and $f$ faces,
> $$v-e+f=2 .$$

*(Verified on Johnsonbaugh's Figure 8.7.2: $v=6$, $e=8$, $f=4$, and $6-8+4=2$ ✓)*

**Remarkably, $f$ does not depend on how the graph is drawn** — it is determined by $v$ and $e$. That is what makes the formula a tool for proving **non**-planarity: assume a planar drawing exists, use Euler's formula to pin down $f$, and derive a contradiction with an edge-counting bound.

> [!example]- The two obstructions, both proved (verified)
> The counting bound: **each face is bounded by at least $g$ edges** (where $g$ is the shortest cycle length) and **each edge borders at most 2 faces**, so $g\cdot f\le2e$.
>
> **$K_{3,3}$ is not planar.** Here $v=6$, $e=9$, so Euler's formula forces $f=2-6+9=5$. $K_{3,3}$ is bipartite, so it has no odd cycles and every cycle has **at least 4** edges. Then
> $$4f\le2e\quad\Longrightarrow\quad 4(5)=20\le18,$$
> which is false. **Contradiction, so $K_{3,3}$ is not planar.** $\blacksquare$
>
> **$K_5$ is not planar.** Here $v=5$, $e=10$, so $f=2-5+10=7$. $K_5$ is simple, so every cycle has **at least 3** edges:
> $$3f\le2e\quad\Longrightarrow\quad 3(7)=21\le20,$$
> false. **Contradiction.** $\blacksquare$
>
> **Both fail by exactly one** — $20$ against $18$, $21$ against $20$. These are the two *minimal* non-planar graphs, which is why they turn out to be the only obstructions.

**Homeomorphism.** If $v$ has degree 2 with distinct neighbours $v_1,v_2$, the edges $(v,v_1)$ and $(v,v_2)$ are **in series**; a **series reduction** deletes $v$ and replaces the pair by a single edge $(v_1,v_2)$. Two graphs are **homeomorphic** if both can be reduced by series reductions to isomorphic graphs — i.e. they agree up to subdividing edges with degree-2 vertices. *(Homeomorphism is an equivalence relation, so it partitions graphs into classes — [[03 - Functions, Sequences and Relations|ch. 03]] §6 again.)*

> [!note] Theorem — Kuratowski (1930)
> **A graph is planar if and only if it contains no subgraph homeomorphic to $K_5$ or $K_{3,3}$.**

**This is a complete characterisation, and a striking one:** among all the ways a graph could fail to be drawable in the plane, there are exactly **two** obstructions. Subdividing edges cannot help, so the condition is up to homeomorphism.

**The easy direction is obvious** — a graph containing a non-planar subgraph cannot be planar. **The converse is the deep half**, and Johnsonbaugh cites the proof rather than giving it.

## ✏️ Exercises

**1. (Degrees and bipartiteness.)** (a) State the handshaking lemma and use it to explain why no graph has degree sequence $3,3,3,3,3$. (b) How many edges does $K_7$ have, and what is each degree? (c) Is $K_{2,3}$ bipartite? Is $K_3$? Justify both. (d) In a group of 9 people, can each person shake hands with exactly 3 others?

> [!example]- Solution
> **(a)** $\sum_v\delta(v)=2|E|$, since each edge contributes 2 to the total degree (one per endpoint, or twice at one vertex if a loop).
>
> The sequence $3,3,3,3,3$ sums to $15$, which is **odd** — but the sum must equal $2|E|$, an even number. **No such graph exists.** Equivalently by the corollary: this sequence has **five** vertices of odd degree, and the number of odd-degree vertices must be even.
>
> **(b)** $K_7$ has $\binom72=\dfrac{7\cdot6}2=\mathbf{21}$ edges, and every vertex has degree $\mathbf6$ *(verified)*. Check with handshaking: $7\cdot6=42=2\cdot21$ ✓
>
> **(c)** **$K_{2,3}$ is bipartite by construction** — take $V_1$ the 2-element side and $V_2$ the 3-element side; every edge joins the two sides, and there are $2\cdot3=6$ edges.
>
> **$K_3$ is not bipartite.** Suppose $V=V_1\cup V_2$ were such a split. $K_3$'s three vertices $a,b,c$ are mutually adjacent. Say $a\in V_1$; then $b\notin V_1$ (edge $ab$), so $b\in V_2$; then $c\notin V_2$ (edge $bc$), so $c\in V_1$ — but then the edge $ac$ joins two vertices of $V_1$, contradiction. $\blacksquare$
>
> **More directly:** $K_3$ is a triangle, an **odd cycle**, and a graph is bipartite iff it has no odd cycle (§1). This also settles $K_n$ for every $n\ge3$.
>
> **(d) No.** Such a graph would have 9 vertices each of degree 3, so $\sum\delta(v)=27$, odd — impossible. **Nine vertices of odd degree is an odd count, contradicting the handshaking corollary.**
>
> *(Note the answer would be yes for **10** people: $10\cdot3=30=2\cdot15$, so a 3-regular graph on 10 vertices is not excluded — and indeed the Petersen graph is one.)*

**2. (Euler cycles and paths.)** (a) The Königsberg graph has degrees $3,3,3,5$. Does it have an Euler cycle? An Euler path? (b) State the criterion for each. (c) For which $n$ does $K_n$ have an Euler cycle? (d) Explain why the number of odd-degree vertices is always even, and what that means for the possible cases.

> [!example]- Solution
> **(a)** **No Euler cycle** — the theorem requires *every* degree even, and all four are odd. **No Euler path either**, since that requires exactly **two** odd-degree vertices and there are four. **So Königsberg admits neither a closed nor an open bridge-walk using each bridge once.** *(Verified: degree sum $14$, so $7$ bridges ✓, with 4 odd vertices.)*
>
> **(b)** For a connected graph:
>
> | odd-degree vertices | conclusion |
> |---|---|
> | $0$ | **Euler cycle** exists |
> | $2$ | **Euler path** exists, running between the two odd vertices |
> | $\ge4$ | neither |
>
> **(c)** $K_n$ has every degree $n-1$, so all degrees are even iff **$n$ is odd**. $K_n$ is connected for $n\ge1$. So $K_n$ has an Euler cycle **exactly when $n$ is odd** ($n=1,3,5,7,\dots$).
>
> Check: $K_3$ (degrees 2,2,2) — the triangle itself is an Euler cycle ✓ $K_4$ (degrees 3,3,3,3) — four odd vertices, so neither cycle nor path ✓ $K_5$ (degrees 4,4,4,4,4) — Euler cycle exists ✓
>
> **(d)** From $\sum_v\delta(v)=2|E|$ the total degree is **even**. Split the sum into even-degree and odd-degree terms: the even part is even, so the odd part must be even too — and a sum of odd numbers is even exactly when there is an **even number** of them. $\blacksquare$
>
> **Consequence: the count of odd-degree vertices is $0,2,4,\dots$ — never odd.** So the three cases in (b) are exhaustive, and in particular **"exactly one odd-degree vertex" is impossible**, which is why the Euler-path criterion asks for two rather than one.

**3. (Hamiltonian cycles.)** (a) Give the definition and contrast it with an Euler cycle. (b) Show that $K_{2,3}$ has no Hamiltonian cycle. (c) Explain the flawed "count the deletions" argument and why it fails. (d) Does every graph with a Hamiltonian cycle have an Euler cycle, or vice versa?

> [!example]- Solution
> **(a)** A **Hamiltonian** cycle visits every **vertex** exactly once (start/end excepted); an **Euler** cycle uses every **edge** exactly once. The contrast:
>
> | | Euler | Hamiltonian |
> |---|---|---|
> | covers | edges | vertices |
> | criterion | **iff** connected and all degrees even | **none known** |
> | complexity | linear time | **NP-complete** |
>
> **(b)** $K_{2,3}$ is bipartite with parts of size 2 and 3, total 5 vertices. A Hamiltonian cycle would have length 5 and, being a cycle in a bipartite graph, must **alternate** between the parts — so its length must be **even**. But 5 is odd. **Contradiction, so no Hamiltonian cycle exists.** $\blacksquare$
>
> **The general principle:** in a bipartite graph with parts of sizes $m\ne n$, no Hamiltonian cycle exists, because alternating forces the two parts to be visited equally often. *(This is the argument Johnsonbaugh uses for the knight's-tour graph $GK_n$, where the board's two colour classes play the role of the parts.)*
>
> **(c)** The flawed argument: "each vertex of degree $>2$ must have all but two of its edges deleted; total up the required deletions; if too many edges must go, no Hamiltonian cycle exists."
>
> **The error is double-counting.** Every edge has **two** endpoints, so an edge deleted "because of $u$" may be the same edge deleted "because of $v$". Summing the per-vertex deletion counts therefore **overstates** the number of edges actually removed, and the resulting contradiction can be spurious. Johnsonbaugh's Figure 8.3.6 is precisely such a case: the flawed argument concludes there is no Hamiltonian cycle, **and one exists.**
>
> **The fix: count edges removed, not deletions performed** — or use the sound argument instead, which works forwards from *forced* edges (every degree-2 vertex contributes both its edges) and derives a contradiction if the forced edges make a short cycle or give a vertex three cycle-edges.
>
> **(d) Neither implication holds — the properties are independent.** Four cases all occur:
>
> | | Euler cycle | no Euler cycle |
> |---|---|---|
> | **Hamiltonian** | $K_3$ (all degrees 2) | $K_4$ (all degrees 3, odd — yet $(a,b,c,d,a)$ is Hamiltonian) |
> | **not Hamiltonian** | two triangles sharing one vertex (all degrees even; the shared vertex must be visited twice) | $K_{2,3}$ (degrees $3,3,2,2,2$) |
>
> **The bottom-left entry is the instructive one:** two triangles glued at a vertex has an Euler cycle (every degree is even and it is connected) but no Hamiltonian cycle, since any cycle through all five vertices would have to pass through the cut vertex twice. **A graph can be perfectly traversable edge-wise and impossible vertex-wise, and conversely.**

**4. (Adjacency matrices.)** For the graph on $\{a,b,c,d,e\}$ with edges $ab,ad,bc,be,cd,ce$: (a) write the adjacency matrix $A$; (b) read the degrees off $A$; (c) compute $A^2$ and interpret entries $(a,c)$ and $(a,a)$; (d) how many walks of length 3 go from $a$ to $c$? (e) Why does $A^k$ count *walks* rather than *simple paths*?

> [!example]- Solution
> **(a)** With the ordering $a,b,c,d,e$:
> $$A=\begin{pmatrix}0&1&0&1&0\\1&0&1&0&1\\0&1&0&1&1\\1&0&1&0&0\\0&1&1&0&0\end{pmatrix}$$
> The matrix is **symmetric**, as it must be for an undirected graph.
>
> **(b)** Row sums: $\delta(a)=2$, $\delta(b)=3$, $\delta(c)=3$, $\delta(d)=2$, $\delta(e)=2$. Total $12=2\cdot6$ edges ✓ and exactly **two** odd-degree vertices ✓ *(handshaking, verified)*.
>
> **(c)** *(computed, and matching the book's printed $A^2$ exactly)*
> $$A^2=\begin{pmatrix}2&0&2&0&1\\0&3&1&2&1\\2&1&3&0&1\\0&2&0&2&1\\1&1&1&1&2\end{pmatrix}$$
> - $(A^2)_{ac}=2$: there are **two walks of length 2 from $a$ to $c$**, namely $a\to b\to c$ and $a\to d\to c$ — the common neighbours of $a$ and $c$ are exactly $b$ and $d$ *(verified)*.
> - $(A^2)_{aa}=2$: two walks of length 2 from $a$ back to $a$, namely $a\to b\to a$ and $a\to d\to a$. **In general $(A^2)_{ii}=\delta(v_i)$** — every neighbour gives an out-and-back walk. Compare with (b): the diagonal $2,3,3,2,2$ *is* the degree sequence ✓
>
> **(d)** $(A^3)_{ac}=\mathbf1$ *(verified)* — exactly one walk of length 3 from $a$ to $c$.
>
> **(e)** Because matrix multiplication imposes **no constraint against revisiting**. Entry $(i,j)$ of $A^k$ sums over all intermediate sequences $i\to m_1\to\cdots\to m_{k-1}\to j$ with each consecutive pair adjacent — and nothing forbids $m_1=j$ or $m_2=i$. So $a\to b\to a$ is counted, though it repeats a vertex and is not a simple path.
>
> **Consequence: $A^k$ over-counts simple paths, sometimes wildly.** Counting simple paths is a genuinely harder problem (it is #P-complete in general), and no matrix power computes it. **This is a good example of the gap between what is easy to compute and what you might want** — the same gap as [[05 - Number Theory and Cryptography|ch. 05]]'s $\gcd$ versus factoring.

**5. (Hard — planarity.)** (a) State Euler's formula and verify it on a graph of your choice. (b) Prove $K_5$ is not planar. (c) Prove $K_{3,3}$ is not planar, explaining why the bound differs from (b). (d) State Kuratowski's theorem and say why "homeomorphic" is needed rather than "isomorphic". (e) Show that every simple planar graph satisfies $e\le3v-6$, and use it to re-derive (b).

> [!example]- Solution
> **(a)** For a connected planar graph drawn in the plane, $v-e+f=2$, counting the unbounded outer face.
>
> Verification on $K_4$ drawn planar (a triangle with a central vertex joined to all three): $v=4$, $e=6$, and the faces are three small triangles plus the outer face, so $f=4$. Then $4-6+4=\mathbf2$ ✓ *(Johnsonbaugh's Figure 8.7.2 also checks: $6-8+4=2$ ✓)*
>
> **(b)** Suppose $K_5$ were planar. It has $v=5$ and $e=\binom52=10$, so Euler's formula forces
> $$f=2-v+e=2-5+10=7 .$$
> Now bound the edges by faces. $K_5$ is simple, so its shortest cycle has length **3**, meaning **every face is bounded by at least 3 edges**. Summing over faces counts each edge at most twice (an edge borders at most two faces):
> $$3f\le2e\quad\Longrightarrow\quad 3(7)=21\le2(10)=20,$$
> which is **false**. Contradiction, so $K_5$ is not planar. $\blacksquare$ *(Verified.)*
>
> **(c)** Suppose $K_{3,3}$ were planar. It has $v=6$, $e=9$, so
> $$f=2-6+9=5 .$$
> **Here the bound is stronger, because $K_{3,3}$ is bipartite.** A bipartite graph has **no odd cycles** (§1), so its shortest cycle has length **4**, not 3 — every face is bounded by at least 4 edges:
> $$4f\le2e\quad\Longrightarrow\quad 4(5)=20\le2(9)=18,$$
> **false.** Contradiction. $\blacksquare$ *(Verified.)*
>
> **Why the difference matters:** with the weaker bound $3f\le2e$ we would get $15\le18$, which is **true** — no contradiction, and the proof would fail. **Bipartiteness is essential**, and this is a nice case where using extra structure is not optional.
>
> Note both proofs fail by exactly one unit ($21$ vs $20$; $20$ vs $18$), which is a hint that these graphs are *minimally* non-planar — and Kuratowski confirms they are the only obstructions.
>
> **(d) Kuratowski's theorem:** $G$ is planar **iff** $G$ contains no subgraph **homeomorphic** to $K_5$ or $K_{3,3}$.
>
> **Why homeomorphic and not isomorphic.** Subdividing an edge — replacing it by a path through new degree-2 vertices — **cannot affect planarity**: a drawing of the original gives a drawing of the subdivision by putting the new vertices along the existing curve, and vice versa. So a graph may contain a "stretched" copy of $K_5$ with extra degree-2 vertices along its edges, which is not *isomorphic* to $K_5$ but is just as fatal.
>
> **Requiring only an isomorphic copy would make the theorem false** — it would fail to detect subdivided obstructions. Homeomorphism (equality up to series reductions) is exactly the right equivalence, because it identifies graphs with the same planarity.
>
> **(e)** Let $G$ be simple, connected and planar with $v\ge3$. Every face is bounded by at least 3 edges and every edge borders at most 2 faces, so $3f\le2e$, i.e. $f\le\tfrac23e$. Substituting into Euler's formula:
> $$2=v-e+f\le v-e+\tfrac23e=v-\tfrac13e\quad\Longrightarrow\quad \tfrac13e\le v-2\quad\Longrightarrow\quad \boxed{e\le3v-6}$$
>
> **Re-deriving (b):** $K_5$ has $v=5$ and $e=10$, but $3v-6=9<10$. **So $K_5$ violates the bound and cannot be planar** ✓ — the same conclusion in one line.
>
> **This inequality is the practical planarity test**, and it is worth having: any simple graph with more than $3v-6$ edges is immediately non-planar, no drawing attempts needed. *(For bipartite graphs the same argument with $4f\le2e$ gives the sharper $e\le2v-4$; $K_{3,3}$ has $e=9>2(6)-4=8$ ✓ — again settling (c) in one line. Note the bound is **necessary, not sufficient**: $K_{3,3}$ satisfies $e=9\le3(6)-6=12$, so the general bound alone does not detect it, which is why the bipartite refinement is needed.)*

## 📝 Summary

- A **graph** $G=(V,E)$ has vertices and edges; **simple** means no loops or parallel edges. $K_n$ has $\binom n2$ edges and all degrees $n-1$; $K_{m,n}$ has $mn$ edges.
- **Bipartite** means $V$ splits so every edge crosses between the parts — equivalently, **no odd cycle**. To prove it, exhibit the split; to disprove it, force a contradiction (or find an odd cycle).
- **Paths, simple paths, cycles, simple cycles** differ in what may repeat. **Components are the equivalence classes of "there is a path from $v$ to $w$"** — so [[03 - Functions, Sequences and Relations|ch. 03]]'s partition theorem guarantees each vertex lies in exactly one.
- **Handshaking lemma:** $\sum_v\delta(v)=2|E|$, so **the number of odd-degree vertices is even.** Each loop counts 2. This one lemma settles a surprising number of questions.
- **Euler cycle** (every **edge**) exists **iff** the graph is connected and **every degree is even**. Exactly **two** odd vertices gives an Euler **path** between them; four or more gives neither. **Königsberg has four odd vertices — impossible.**
- **Hamiltonian cycle** (every **vertex**) has **no known characterisation** and deciding existence is **NP-complete**. To disprove one: use **forced edges** at degree-2 vertices, or forced deletions — **but count edges removed, not deletions performed**, or you will double-count and "prove" false results.
- **Euler and Hamiltonian properties are independent** — all four combinations occur. Two triangles sharing a vertex has an Euler cycle and no Hamiltonian cycle.
- **A bipartite graph with unequal parts has no Hamiltonian cycle**, since a cycle must alternate and therefore have even length visiting the parts equally.
- **Gray codes are Hamiltonian cycles in the $n$-cube**, constructed recursively (prefix $0$ to the list, then $1$ to its reverse). Used in rotary encoders, where multi-bit transitions would be dangerous.
- **Dijkstra** computes shortest paths greedily: repeatedly finalise the nearest unfinished vertex and relax its edges. **Correct only for nonnegative weights** — the greedy choice's justification is exactly that a detour cannot be shorter.
- **Adjacency matrix:** symmetric; row sums are degrees; and **$(A^k)_{ij}$ counts walks of length $k$**, with $(A^2)_{ii}=\delta(v_i)$. **These are walks, not simple paths** — $A^k$ over-counts, and counting simple paths is genuinely hard.
- **Isomorphism** is a bijection preserving adjacency. **Invariants** (degree sequence, edge count, components, cycle lengths, bipartiteness, planarity) can prove two graphs **different** but never the same — for that you must exhibit the bijection.
- **Euler's formula:** $v-e+f=2$ for connected planar graphs, counting the outer face. **$f$ is determined by $v$ and $e$**, independent of the drawing — which is what makes it a non-planarity tool.
- **$K_5$ and $K_{3,3}$ are not planar**, each by combining Euler's formula with $g\cdot f\le2e$ — using $g=3$ for $K_5$ and **$g=4$ for the bipartite $K_{3,3}$**, where the weaker bound would not suffice.
- **$e\le3v-6$** for every simple planar graph ($e\le2v-4$ if bipartite) — the quick practical test, **necessary but not sufficient**.
- **Kuratowski:** planar **iff** no subgraph **homeomorphic** to $K_5$ or $K_{3,3}$. Only two obstructions exist, and *homeomorphic* is needed because subdividing edges cannot affect planarity.

## ⚠️ Important Notes

1. **Loops count 2 towards the degree.** Forgetting this breaks the handshaking lemma and every Euler-cycle argument.
2. **The number of odd-degree vertices is always even.** So a proposed degree sequence with an odd number of odd entries describes no graph, and "exactly one odd vertex" never arises.
3. **Euler is about edges, Hamiltonian about vertices.** The two words differ by one letter in ordinary speech and the problems differ by the P/NP boundary. Read the question carefully.
4. **Euler's criterion is *iff* and easy to check; there is no Hamiltonian criterion.** If you find yourself recalling "the condition for a Hamiltonian cycle", you are misremembering — only sufficient conditions (Dirac, Ore) exist, not a characterisation.
5. **When arguing that no Hamiltonian cycle exists by deleting edges, count edges, not deletions.** An edge has two endpoints and may be forced out twice. Johnsonbaugh's Figure 8.3.6 is a graph where the careless count "proves" a false statement.
6. **Don't infer one traversal property from the other.** All four Euler/Hamiltonian combinations occur, with concrete small examples.
7. **Dijkstra requires nonnegative weights.** With a negative edge the greedy finalisation is unjustified and the algorithm silently returns wrong answers — use Bellman–Ford.
8. **Dijkstra's first choice is often not the direct edge.** In the verified example the shortest $a\to d$ route is $a\to b\to c\to d$ at 6, beating the two-edge routes at 8. That is the whole reason an algorithm is needed.
9. **$A^k$ counts walks, not paths.** Repeated vertices are included, so $(A^2)_{ii}=\delta(v_i)$ rather than 0. If you need simple paths, matrix powers will not give them.
10. **The adjacency matrix depends on the vertex ordering.** Two different-looking matrices may represent the same graph — so never test graph equality by comparing matrices without fixing an order.
11. **Matching invariants do not prove isomorphism.** Differing invariants prove non-isomorphism; sameness proves nothing. To claim isomorphism, produce the bijection.
12. **Count the outer face in Euler's formula.** Omitting it gives $v-e+f=1$ and every subsequent argument fails.
13. **Euler's formula applies to *connected planar* graphs.** For a planar graph with $c$ components the formula is $v-e+f=1+c$.
14. **Use the bipartite girth bound when the graph is bipartite.** For $K_{3,3}$, the general $3f\le2e$ gives $15\le18$ — no contradiction. Only $4f\le2e$ works. Extra structure is sometimes required, not optional.
15. **$e\le3v-6$ is necessary, not sufficient.** $K_{3,3}$ satisfies it ($9\le12$) and is still non-planar. Use it as a fast rejection test, never as a proof of planarity.
16. **Kuratowski needs "homeomorphic", not "isomorphic".** Subdividing an edge with degree-2 vertices preserves non-planarity, so obstructions can appear stretched.

> [!warning] Gaps in the source material
> **Extraction was good for prose, definitions and theorem statements**, and this chapter had one unusual success: **the adjacency matrices of §8.5 survived intact**, including Example 8.5.2's $A$ and $A^2$ as readable digit rows. **Recomputing $A^2$ confirmed the book's printed matrix entry for entry** — the first time in this subject that a displayed calculation could be checked directly rather than reconstructed.
>
> **The dominant loss is structural and severe: this is a chapter taught through pictures, and every figure is an image.** Lost are Figures 8.1.x (the introductory graphs, $K_4$, the bipartite and non-bipartite examples, $K_{2,4}$), 8.2.1–8.2.6 (connected and disconnected graphs, subgraphs, components), **8.2.7–8.2.8 (the Königsberg bridges and their graph)**, 8.3.4–8.3.12 (**every Hamiltonian-cycle example and counterexample**, including Figure 8.3.6 — the graph whose flawed argument is the point of §5's warning), 8.5.1–8.5.2 (the graphs whose matrices *did* survive), 8.7.1–8.7.6 (**$K_{3,3}$, $K_5$, the faces diagram, the series-reduction and homeomorphism examples**), and all of §8.6's isomorphism illustrations.
>
> **Consequently the notes describe graphs by explicit vertex and edge sets, degree sequences, and counts** rather than referring to lost pictures. Where a specific figure carried an argument I have either reconstructed the graph from its stated properties (Example 8.5.2's graph is fully determined by the surviving matrix; the Königsberg graph by its degrees $3,3,3,5$ and 7 edges) or replaced it with my own verified example (Exercise 4, Exercise 5(a), §6's Dijkstra instance, and §5's "two triangles sharing a vertex"). **Figure 8.3.6 cannot be reconstructed** — the warning about double-counting deletions is stated and explained, but the specific graph is not reproduced.
>
> **The numbered Algorithms extract as empty headings again**, so Algorithm 8.3.10 (randomised Hamiltonian search) and **Dijkstra's algorithm in §8.4** survive only as titles and input/output lines. **§6's Python is my own reconstruction** from the prose description, verified by running it on a four-vertex instance (distances $0,2,3,6$ from $a$, with the non-obvious optimal route $a\to b\to c\to d$).
>
> **Verified computationally before writing:** the adjacency matrix and $A^2$ against the book; $(A^2)_{ac}=2$ with the two witnessing walks and $(A^3)_{ac}=1$; the degree sequence and handshaking sum; the Königsberg degrees; Euler's formula on Figure 8.7.2 ($6-8+4=2$); **both non-planarity proofs** ($K_{3,3}$: $f=5$ and $20\le18$ false; $K_5$: $f=7$ and $21\le20$ false); $K_n$ edge counts and degrees for $n=3,\dots,6$; the 3-bit **Gray code** with the single-bit-change property confirmed including wrap-around; and Dijkstra's output. **No error was found in Johnsonbaugh ch. 8** — eight chapters in, the errata table in `00-Index.md` is still empty.
>
> **Additions beyond the source.** The **odd-cycle characterisation of bipartiteness** (§1) is not in Johnsonbaugh ch. 8, which gives only the trial-and-error procedure; stating it turns that procedure into a theorem and settles $K_n$ for all $n\ge3$ at once. The observation that **components are the equivalence classes of path-connectivity** (§2) is mine, linking back to [[03 - Functions, Sequences and Relations|ch. 03]] §6. The **Euler-path table** (0 / 2 / $\ge4$ odd vertices) is assembled by me — Johnsonbaugh puts the Euler-path case in the exercises. **The Euler-versus-Hamiltonian comparison table** (§5) and **the four-case independence table** in Exercise 3(d), including the "two triangles sharing a vertex" example, are my own. **Dijkstra's correctness argument and the explicit statement that it fails for negative weights** (with the pointer to Bellman–Ford) are additions; the book presents the algorithm without this discussion. The warning that **$A^k$ counts walks rather than simple paths**, and that counting simple paths is #P-complete, is mine. **Exercise 5(e)'s derivation of $e\le3v-6$ and the bipartite refinement $e\le2v-4$** are additions — Johnsonbaugh proves the two non-planarity results individually and does not extract the general inequality, which is the form actually used in practice. The **Gray-code application to rotary encoders** and the explanation of why single-bit transitions matter are mine.
>
> **Deliberately compressed.** **§8.6 (Isomorphisms of Graphs)** is reduced to the definition plus the invariant list and the warning that invariants cannot prove isomorphism; Johnsonbaugh's worked isomorphism-detection examples depend entirely on lost figures. **§8.3's knight's-tour material** (the graphs $GK_n$, Pósa's argument that $GK_4$ has no Hamiltonian cycle, and the result that $GK_n$ has one for all even $n\ge6$) is summarised as the bipartite-parity argument in Exercise 3(b) rather than developed. **§8.8 (Instant Insanity)** is omitted as recreational, per the scope decision in `00-Index.md`. Johnsonbaugh's "Problem-Solving Corner: Graphs" (p. 395) is a worked-example section whose content is distributed through §§2–5.

**Previous:** [[07 - Recurrence Relations]] · **Next:** [[09 - Trees]]
