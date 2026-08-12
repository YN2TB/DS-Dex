---
subject: Discrete Mathematics
chapter: 10
tags: [ds, discrete-mathematics, network-flows, max-flow-min-cut, matching, hall-theorem, duality, bipartite-graphs]
source: "Johnsonbaugh, *Discrete Mathematics* 8e, ch. 10 (book pp. 506–531)"
---

# Network Flows and Matching

This is the last chapter of the subject, and it ties two threads together.

The first is internal: [[08 - Graph Theory|ch. 08]] gave us weighted directed graphs and [[09 - Trees|ch. 09]] gave us greedy algorithms with exchange-argument proofs. Here they combine into the **max flow, min cut theorem** — one of the most-used results in combinatorial optimization.

The second is external. [[Optimization/contents/10 - Duality|Optimization ch. 10]] omitted max-flow/min-cut from its own scope and **pointed here**, calling it (with Luenberger & Ye) "one of the most exemplary pairs of primal and dual problems". §5 below explains why: **max-flow/min-cut is a duality theorem**, and reading it alongside Optimization ch. 10 shows the same structure appearing in two subjects that look unrelated.

## 📘 Main Knowledge

### 1. Transport networks

> [!note] Definition
> A **transport network** is a simple weighted directed graph with:
> - a designated **source** $a$ with **no incoming edges**;
> - a designated **sink** $z$ with **no outgoing edges**;
> - a nonnegative weight $C_{ij}$ on each directed edge $(i,j)$, called its **capacity**.

Think of oil through pipes, data through channels, or traffic through roads: the capacity is the most the edge can carry.

> [!note] Definition — a flow
> A **flow** $F$ assigns a number $F_{ij}$ to each edge $(i,j)$ such that
> $$\text{(a) } 0\le F_{ij}\le C_{ij}\qquad\text{(the capacity constraint)}$$
> $$\text{(b) for every vertex }j\text{ other than the source and sink: }\quad \sum_i F_{ij}=\sum_k F_{jk}\qquad\text{(\textbf{conservation of flow})}$$

**Conservation says nothing is created or destroyed at an intermediate vertex** — whatever flows in flows out. In the oil analogy, no pipe leaks and no pump adds oil.

> [!note] Theorem 10.1.5 and the value of a flow
> **The flow out of the source equals the flow into the sink.** That common number is the **value** of the flow.

*Why:* sum the conservation equations over all intermediate vertices. Every internal edge is counted once positively and once negatively and cancels; what survives is (flow out of $a$) $-$ (flow into $z$) $=0$. **This is a telescoping argument, and it is why the value is well defined** — you may measure it at either end.

> [!note] Multiple sources and sinks: supersource and supersink
> Real networks often have several sources (reservoirs, factories) and several sinks (cities, warehouses). The definition allows only one of each — but the fix is trivial and worth knowing:
>
> **Add a new vertex $a$ joined to every original source, and a new vertex $z$ joined from every original sink, all with capacity $\infty$.** Any flow in the enlarged network restricts to a flow in the original, and conversely. **So the one-source-one-sink assumption costs nothing** — Johnsonbaugh applies it to a pumping network and a traffic network.
>
> The same trick appears again in §4 to turn a matching problem into a flow problem. **Reduction by adding a supersource and supersink is the standard move in this chapter.**

### 2. Increasing a flow: augmenting paths

To improve a flow, find a path from source to sink along which you can push more. Two kinds of edge can appear on such a path.

> [!note] Theorem 10.2.3 — augmenting paths
> Let $P$ be a path from $a$ to $z$ in which every edge satisfies one of:
> - the edge is **properly oriented** (pointing along the path) and $F_{ij}<C_{ij}$ — there is slack to push more;
> - the edge is **improperly oriented** (pointing against the path) and $F_{ij}>0$ — there is flow to cancel.
>
> Then the flow can be increased, by the smallest of those slacks and existing flows along $P$.

**The improperly oriented case is the subtle and essential one.** A greedy method that only pushes forward along under-used edges can get stuck at a non-maximal flow; allowing an edge to be *reduced* lets earlier commitments be undone. **This is why the algorithm needs the notion of a path rather than a directed path**, and it is what makes the method correct rather than merely plausible.

The algorithm repeatedly finds such a path — by **labelling** vertices reachable from $a$ under those two rules — and augments. When no labelled path reaches $z$, it stops.

```python
from collections import defaultdict, deque

def max_flow(cap, s, t):
    """cap: dict {(u,v): capacity}. Returns the maximum flow value."""
    res = defaultdict(int)
    for (u, v), c in cap.items():
        res[(u, v)] = c                  # residual capacities
    total = 0
    while True:
        parent, q = {s: None}, deque([s])
        while q:                          # label reachable vertices
            u = q.popleft()
            for (x, y), c in list(res.items()):
                if x == u and c > 0 and y not in parent:
                    parent[y] = u
                    q.append(y)
        if t not in parent:               # no augmenting path -> done
            return total
        path, v = [], t                   # recover the path
        while parent[v] is not None:
            path.append((parent[v], v)); v = parent[v]
        b = min(res[e] for e in path)     # bottleneck
        for (u, v) in path:
            res[(u, v)] -= b
            res[(v, u)] += b              # the "improperly oriented" allowance
        total += b
```

**The line `res[(v, u)] += b` is Theorem 10.2.3's second case**, recorded as a *residual* edge: adding backward capacity is exactly the option to cancel flow later.

### 3. Cuts

> [!note] Definitions
> A **cut** $(P,\overline P)$ consists of a set $P$ of vertices containing the source, with $\overline P$ its complement containing the sink. The cut's edge set is $\{(v,w):v\in P,\ w\in\overline P\}$, and its **capacity** is the sum of those edges' capacities.

A cut is a way of severing the network: every route from $a$ to $z$ must cross it at least once. **Only forward-crossing edges count** towards the capacity — edges from $\overline P$ back into $P$ are ignored.

> [!note] Theorem 10.3.7 — weak duality
> **The capacity of any cut is $\ge$ the value of any flow.**

*Why:* everything reaching the sink must cross the cut, and the crossing edges cannot carry more than their capacities.

**Notice the logical shape:** *any* cut bounds *any* flow. So every flow is a certificate that no cut is smaller, and every cut is a certificate that no flow is larger. **This is precisely the weak-duality pattern of [[Optimization/contents/10 - Duality|Optimization ch. 10]] §4** — one side's feasible points bound the other's.

> [!note] Theorem 10.3.9 — the Max Flow, Min Cut Theorem
> If a flow's value equals a cut's capacity, then **the flow is maximal and the cut is minimal**. Moreover, equality is achieved: **the maximum flow value equals the minimum cut capacity.**

> [!note] Theorem 10.3.11 — and where the min cut comes from
> At termination of the labelling algorithm, the flow is maximal. Moreover, taking $P$ = the **labelled** vertices and $\overline P$ = the **unlabelled** ones gives a **minimal cut**.

**This is the elegant part.** The algorithm stops because it cannot label $z$ — and the boundary between labelled and unlabelled vertices is exactly a cut whose every forward edge is saturated and every backward edge is empty. **So the algorithm outputs its own optimality certificate for free**, which is the same phenomenon as the simplex method producing the dual solution in [[Optimization/contents/10 - Duality|Optimization ch. 10]] §5.

> [!example]- A worked network, with every cut enumerated (verified)
> Source $a$, sink $z$, capacities:
> $$ab(3),\quad ad(2),\quad bc(2),\quad be(1),\quad de(3),\quad cz(2),\quad ez(3)$$
>
> **Maximum flow $=\mathbf5$** *(verified by augmentation)*.
>
> All $2^4=16$ cuts, by choice of which of $b,c,d,e$ join $P$:
>
> | $P$ | capacity | | $P$ | capacity |
> |---|---|---|---|---|
> | $\{a\}$ | **5** | | $\{a,b,c\}$ | **5** |
> | $\{a,b\}$ | **5** | | $\{a,b,d\}$ | 6 |
> | $\{a,c\}$ | 7 | | $\{a,d,e\}$ | 6 |
> | $\{a,d\}$ | 6 | | $\{a,b,d,e\}$ | **5** |
> | $\{a,e\}$ | 8 | | $\{a,b,c,d,e\}$ | **5** |
>
> *(the remaining six all exceed 5)*
>
> **Minimum cut capacity $=\mathbf5=$ maximum flow** ✓ — max-flow/min-cut confirmed.
>
> **Two things worth noticing.** First, **the minimum cut is not unique** — five different cuts here achieve capacity 5. (The *value* is unique; the cut achieving it need not be, exactly as with minimal spanning trees in [[09 - Trees|ch. 09]] §4.) Second, $P=\{a\}$ achieves the minimum, which says the source's own outgoing edges $ab(3)+ad(2)=5$ already form a bottleneck.

### 4. Matching

> [!note] Definitions
> Let $G$ be a directed bipartite graph with parts $V$ and $W$, edges directed from $V$ to $W$. A **matching** is a set of edges **no two of which share a vertex**. A **maximal matching** has the largest possible number of edges. A **complete matching** matches **every** vertex of $V$.

The application is assignment: applicants to jobs, students to projects, machines to tasks.

> [!example]- Johnsonbaugh's job-assignment example (verified)
> Applicants $A,B,C,D$; jobs $J_1,\dots,J_5$. Qualifications:
>
> | applicant | qualified for |
> |---|---|
> | $A$ | $J_2,J_5$ |
> | $B$ | $J_2,J_5$ |
> | $C$ | $J_1,J_3,J_4,J_5$ |
> | $D$ | $J_2,J_5$ |
>
> **Can every applicant get a job?** No — and the reason is a counting argument. **Consider $A$, $B$ and $D$ together: all three are qualified only for $J_2$ and $J_5$.** Three applicants competing for two jobs cannot all be placed. *(This is the pigeonhole principle of [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]] §8, in its second form: no injection from a 3-set into a 2-set.)*
>
> **Verified:** the maximum matching has size $\mathbf3$ (e.g. $B\!-\!J_2$, $C\!-\!J_3$, $D\!-\!J_5$), and a complete matching would need 4. So a **maximal** matching exists but a **complete** one does not.

> [!note] Hall's theorem — the exact criterion
> A complete matching exists **if and only if** for every subset $S\subseteq V$,
> $$|N(S)|\ \ge\ |S|,$$
> where $N(S)$ is the set of vertices in $W$ adjacent to at least one vertex of $S$.
>
> *(Also called the **marriage theorem**, or the condition for a **system of distinct representatives**.)*

**The necessity is the easy half and is exactly the argument above:** if some $S$ has $|N(S)|<|S|$, its members are competing for too few partners. In the example $S=\{A,B,D\}$ has $N(S)=\{J_2,J_5\}$, so $2<3$ and no complete matching exists *(verified)*. **Sufficiency is the theorem** — that *no* such deficient set is the only obstruction.

*(Verified on a positive case: with $A\!:\!\{W,X\}$, $B\!:\!\{X,Y\}$, $C\!:\!\{Y,Z\}$, Hall's condition holds for all $2^3-1$ nonempty subsets, and a complete matching exists — $A\!-\!W$, $B\!-\!X$, $C\!-\!Y$.)*

> [!note] Theorem 10.4.5 — matching *is* a flow problem
> Build a **matching network**: give every original edge capacity 1, add a supersource $a$ with capacity-1 edges to each vertex of $V$, and a supersink $z$ with capacity-1 edges from each vertex of $W$. Then
> - a flow gives a matching ($v$ matched to $w$ iff $F_{vw}=1$);
> - a **maximal flow** gives a **maximal matching**;
> - a flow of value $|V|$ gives a **complete matching**.

**The unit capacities do all the work.** Capacity 1 on $(a,v)$ means $v$ is used at most once; capacity 1 on $(w,z)$ means $w$ is taken at most once. **So "no two edges share a vertex" — the definition of a matching — is enforced entirely by the capacity constraints**, and conservation of flow does the rest.

*(Verified: the matching network for the job example has maximum flow $3$, exactly the maximum matching size.)*

**This is the chapter's methodological point.** A problem about *assignment* has been converted into a problem about *flow*, for which §2 supplies an algorithm and §3 a certificate of optimality. **Reduction to a solved problem is usually better than a new algorithm** — and it comes with the min-cut certificate as a bonus: the minimum cut in a matching network identifies exactly the deficient set that Hall's theorem describes.

### 5. Max-flow/min-cut as duality

*(This section is my own; Johnsonbaugh does not make the connection.)*

Everything in §3 has the shape of [[Optimization/contents/10 - Duality|Optimization ch. 10]]:

| Network flow | Linear programming duality |
|---|---|
| maximise the flow value | the **primal** (a maximisation) |
| minimise the cut capacity | the **dual** (a minimisation) |
| any cut capacity $\ge$ any flow value (Thm 10.3.7) | **weak duality**: max $\le$ min |
| max flow $=$ min cut (Thm 10.3.9) | **strong duality**: no gap |
| the labelled/unlabelled split at termination is a min cut | **the algorithm produces the dual solution** |
| the min cut identifies the bottleneck edges | **complementary slackness**: saturated edges are the "priced" constraints |

**Max flow really is a linear program:** the variables are the $F_{ij}$, the objective is linear, and the constraints (capacity and conservation) are linear inequalities and equations. Its LP dual turns out to be the minimum-cut problem — and because the constraint matrix is of a special (totally unimodular) form, **the dual has an integral optimal solution, which is why a *cut* rather than a fractional object comes out.**

**Three payoffs from seeing it this way:**

1. **Weak duality is free, and it is a proof technique.** Exhibit any flow and any cut of equal value and you have proved both optimal — no algorithm needed. This is [[Optimization/contents/10 - Duality|Optimization ch. 10]] §4's certificate property.
2. **The min cut is the shadow price information.** It names *which* capacities are binding, so it tells you where to invest to increase throughput — exactly the sensitivity reading of Optimization ch. 10 §9.
3. **Hall's theorem is a corollary.** Applying max-flow/min-cut to the matching network of §4 and analysing when the min cut falls below $|V|$ yields precisely the deficiency condition. **So a combinatorial theorem about marriages drops out of a theorem about pipes.**

**This is the standing lesson of the whole vault's optimization material**, and a good note to end the subject on: *the same mathematical structure keeps reappearing in problems that look nothing alike.* Bipartite matching, oil pipelines, LP duality and the simplex method's reduced costs are four views of one thing.

## ✏️ Exercises

**1. (Flows.)** For the network with source $a$, sink $z$ and capacities $ab(3)$, $ad(2)$, $bc(2)$, $be(1)$, $de(3)$, $cz(2)$, $ez(3)$: (a) verify that $F_{ab}=3$, $F_{ad}=2$, $F_{bc}=2$, $F_{be}=1$, $F_{de}=2$, $F_{cz}=2$, $F_{ez}=3$ is a flow. (b) Give its value, computed at both ends. (c) Is it maximal?

> [!example]- Solution
> **(a)** Check both conditions.
>
> **Capacity** $0\le F_{ij}\le C_{ij}$:
>
> | edge | $F$ | $C$ | ok? |
> |---|---|---|---|
> | $ab$ | 3 | 3 | ✓ (saturated) |
> | $ad$ | 2 | 2 | ✓ (saturated) |
> | $bc$ | 2 | 2 | ✓ (saturated) |
> | $be$ | 1 | 1 | ✓ (saturated) |
> | $de$ | 2 | 3 | ✓ (slack 1) |
> | $cz$ | 2 | 2 | ✓ (saturated) |
> | $ez$ | 3 | 3 | ✓ (saturated) |
>
> **Conservation** at each intermediate vertex:
> - $b$: in $=F_{ab}=3$; out $=F_{bc}+F_{be}=2+1=3$ ✓
> - $c$: in $=F_{bc}=2$; out $=F_{cz}=2$ ✓
> - $d$: in $=F_{ad}=2$; out $=F_{de}=2$ ✓
> - $e$: in $=F_{be}+F_{de}=1+2=3$; out $=F_{ez}=3$ ✓
>
> **So it is a valid flow.**
>
> **(b)** Out of the source: $F_{ab}+F_{ad}=3+2=\mathbf5$. Into the sink: $F_{cz}+F_{ez}=2+3=\mathbf5$. **Equal**, as Theorem 10.1.5 guarantees ✓
>
> **(c) Yes, it is maximal** — and here is the one-line proof. Take the cut $P=\{a\}$, $\overline P=\{b,c,d,e,z\}$. Its capacity is $C_{ab}+C_{ad}=3+2=5$. Since **the value of this flow equals the capacity of this cut**, Theorem 10.3.9 says the flow is maximal and the cut is minimal. $\blacksquare$
>
> *(Verified: maximum flow is indeed 5, and the minimum cut capacity is 5.)*
>
> **Note how little work that was.** We did not need to run an algorithm or check that no augmenting path exists — **exhibiting a matching flow and cut is a complete certificate.** That is the practical value of duality, and it is why §5 emphasises it.

**2. (Augmenting paths.)** (a) State the two conditions an edge on an augmenting path must satisfy. (b) Why is the "improperly oriented" case necessary? (c) In the network of Exercise 1, is there an augmenting path? Justify.

> [!example]- Solution
> **(a)** Along a path from $a$ to $z$, each edge must be either
> - **properly oriented** (pointing along the path) with $F_{ij}<C_{ij}$ — slack available to push more; or
> - **improperly oriented** (pointing against the path) with $F_{ij}>0$ — existing flow available to cancel.
>
> The increase achievable is the minimum of those slacks and flows along the path.
>
> **(b)** Because pushing forward alone can strand a flow at a non-maximal value. An early augmentation may commit capacity along a route that later proves to be the wrong one; without the ability to **reduce** flow on an edge, that commitment is permanent and the algorithm can terminate short of the optimum.
>
> Allowing improperly oriented edges lets flow be **rerouted** — pushing along a path that cancels flow on one edge while adding it elsewhere. **In the implementation this is the residual backward edge** (`res[(v,u)] += b`), and it is exactly what makes the labelling algorithm provably correct rather than merely greedy.
>
> *(Compare [[09 - Trees|ch. 09]] §4: Prim's greedy algorithm needs no undo mechanism and is correct as it stands. Max flow is the harder case, and the difference is that the exchange must happen* during *the algorithm rather than only in its proof.)*
>
> **(c) No augmenting path exists.** Every edge out of the source is **saturated**: $F_{ab}=C_{ab}=3$ and $F_{ad}=C_{ad}=2$. A properly oriented first edge would need slack, and there are no improperly oriented edges at $a$ (the source has no incoming edges by definition). **So no vertex can be labelled from $a$**, the algorithm halts immediately, and the flow is maximal.
>
> This also produces the minimal cut, by Theorem 10.3.11: $P=\{a\}$ (the only labelled vertex) with capacity 5 — agreeing with Exercise 1(c) ✓

**3. (Cuts.)** For the network of Exercise 1: (a) compute the capacity of the cut $P=\{a,b,d\}$. (b) Compute the capacity of $P=\{a,b\}$. (c) Find the minimum cut capacity and confirm max-flow/min-cut. (d) Is the minimum cut unique?

> [!example]- Solution
> **(a)** $P=\{a,b,d\}$, $\overline P=\{c,e,z\}$. Forward-crossing edges: $bc(2)$, $be(1)$, $de(3)$. Capacity $=2+1+3=\mathbf6$.
>
> *(Note $ab$ and $ad$ do **not** count — both endpoints are in $P$.)*
>
> **(b)** $P=\{a,b\}$, $\overline P=\{c,d,e,z\}$. Crossing edges: $ad(2)$, $bc(2)$, $be(1)$. Capacity $=2+2+1=\mathbf5$.
>
> **(c)** Enumerating all $2^4=16$ cuts *(verified)*, the minimum capacity is $\mathbf5$. Since Exercise 1 exhibited a flow of value 5, **max flow $=$ min cut $=5$** ✓ — the Max Flow, Min Cut Theorem confirmed on this instance.
>
> **(d) No — five different cuts achieve capacity 5:**
> $$P=\{a\},\quad\{a,b\},\quad\{a,b,c\},\quad\{a,b,d,e\},\quad\{a,b,c,d,e\}.$$
> *(All verified.)*
>
> **The minimum *value* is unique; the cut achieving it is not** — exactly the situation with minimal spanning trees in [[09 - Trees|ch. 09]] §4 and with LP optima in [[Optimization/contents/09 - Linear Programming and the Simplex Method|Optimization ch. 09]]. So two correct algorithms may report different bottleneck sets and must report the same capacity.
>
> **A practical reading:** each minimum cut names a *different* set of edges whose enlargement could raise throughput. Having several means there are several independent bottlenecks — and **relieving only one of them will not help**, since the others still cap the flow at 5. That is the sensitivity information §5 mentions.

**4. (Matching.)** Applicants $A,B,C,D$ are qualified as follows: $A$ for $J_2,J_5$; $B$ for $J_2,J_5$; $C$ for $J_1,J_3,J_4,J_5$; $D$ for $J_2,J_5$. (a) Find a maximal matching. (b) Does a complete matching exist? (c) State Hall's condition and identify the violating set. (d) Model the problem as a network.

> [!example]- Solution
> **(a)** A maximal matching has **3 edges** *(verified by exhaustive search)*, for example
> $$B\!-\!J_2,\qquad C\!-\!J_3,\qquad D\!-\!J_5 .$$
> No two share a vertex ✓ and no matching of size 4 exists.
>
> **(b) No complete matching exists** — that would need all four applicants matched, i.e. 4 edges.
>
> **(c) Hall's condition:** a complete matching exists iff $|N(S)|\ge|S|$ for **every** $S\subseteq V$.
>
> **The violating set is $S=\{A,B,D\}$.** All three are qualified only for $J_2$ and $J_5$, so
> $$N(S)=\{J_2,J_5\},\qquad |N(S)|=2\ <\ 3=|S| .$$
> *(Verified.)* **Three applicants competing for two jobs** — by pigeonhole ([[06 - Counting Methods and the Pigeonhole Principle|ch. 06]] §8, second form) no injection from a 3-set into a 2-set exists, so at most two of $A,B,D$ can be placed.
>
> **This is why $C$'s wide qualifications do not help.** $C$ can take any of four jobs, but that does nothing for the bottleneck among $A,B,D$ — **a deficiency in one subset cannot be repaired by abundance elsewhere**, which is exactly the content of Hall's theorem.
>
> **(d) The matching network:** capacity 1 on every edge, plus
> - a supersource $a$ with capacity-1 edges $a\!\to\!A$, $a\!\to\!B$, $a\!\to\!C$, $a\!\to\!D$;
> - the original qualification edges $A\!\to\!J_2$, $A\!\to\!J_5$, $B\!\to\!J_2$, …, each of capacity 1;
> - a supersink $z$ with capacity-1 edges $J_i\!\to\!z$ for each $i$.
>
> **The unit capacities enforce the matching condition:** capacity 1 out of $a$ into each applicant means each is used at most once; capacity 1 from each job into $z$ means each job is filled at most once.
>
> *(Verified: the maximum flow in this network is **3**, matching the maximum matching size from (a) — Theorem 10.4.5 confirmed. A flow of value $|V|=4$ would be a complete matching, and none exists.)*
>
> **And the minimum cut identifies the obstruction.** A cut of capacity 3 exists, and tracing which edges it severs recovers the deficient set $\{A,B,D\}$ — so **the flow algorithm not only computes the maximum matching but explains why it cannot be larger.**

**5. (Hard — duality.)** (a) State the weak and strong forms of max-flow/min-cut, and say what each corresponds to in linear programming. (b) Explain how the labelling algorithm produces a minimum cut. (c) Prove the necessity half of Hall's theorem using max-flow/min-cut ideas. (d) Why is this a good note on which to end the subject?

> [!example]- Solution
> **(a)**
>
> | Statement | LP counterpart |
> |---|---|
> | **Weak** (Thm 10.3.7): the capacity of **any** cut $\ge$ the value of **any** flow | **Weak duality** — every dual-feasible point bounds every primal-feasible one ([[Optimization/contents/10 - Duality\|Optimization ch. 10]] §4) |
> | **Strong** (Thm 10.3.9): **max** flow $=$ **min** cut | **Strong duality** — the optimal values coincide, no gap (Optimization ch. 10 §5) |
>
> Max flow is genuinely a linear program: variables $F_{ij}$, linear objective, linear capacity and conservation constraints. **Its LP dual is the minimum-cut problem**, and because the constraint matrix is totally unimodular the dual attains its optimum at an integer point — which is why the answer is a *cut* (a $0/1$ object) rather than something fractional.
>
> **The practical consequence is the certificate property:** exhibit a flow and a cut of equal value and both are proved optimal, with no algorithm and no trust required. Exercise 1(c) did exactly that in one line.
>
> **(b)** The algorithm halts when it can no longer label $z$. Let $P$ be the labelled vertices (which always includes $a$) and $\overline P$ the unlabelled ones (which includes $z$). Then $(P,\overline P)$ is a cut, and consider its edges:
> - **Every forward edge $(v,w)$ with $v\in P$, $w\in\overline P$ is saturated** ($F_{vw}=C_{vw}$). Otherwise the labelling rule's first case would have labelled $w$.
> - **Every backward edge $(w,v)$ with $w\in\overline P$, $v\in P$ carries zero flow.** Otherwise the second case would have labelled $w$.
>
> So the flow across the cut equals the cut's full capacity, with nothing flowing back. Hence value of flow $=$ capacity of this cut, and by Theorem 10.3.9 **both are optimal**. $\blacksquare$
>
> **The algorithm therefore emits its own optimality proof** — the same phenomenon as the simplex method's final tableau containing the dual solution ([[Optimization/contents/10 - Duality|Optimization ch. 10]] §5: $\mathbf y^{\mathsf T}=\mathbf c_B^{\mathsf T}B^{-1}$). **A well-designed algorithm computes the certificate as a by-product.**
>
> **(c) Necessity of Hall's condition.** Suppose some $S\subseteq V$ has $|N(S)|<|S|$. In the matching network, construct the cut
> $$P=\{a\}\cup S\cup N(S),\qquad \overline P=(V\setminus S)\cup(W\setminus N(S))\cup\{z\}.$$
> Which edges cross forward?
> - From $a$ to $V\setminus S$: one capacity-1 edge per unmatched-side applicant, $|V|-|S|$ in total.
> - From $S$ to $W\setminus N(S)$: **none**, by the definition of $N(S)$ — every neighbour of $S$ is inside $N(S)$.
> - From $N(S)$ to $z$: one capacity-1 edge each, $|N(S)|$ in total.
>
> So the cut capacity is
> $$\big(|V|-|S|\big)+|N(S)|\ <\ \big(|V|-|S|\big)+|S|\ =\ |V| .$$
> By weak duality the maximum flow is **strictly less than $|V|$**, and by Theorem 10.4.5 a complete matching would require a flow of exactly $|V|$. **So no complete matching exists.** $\blacksquare$
>
> *(Check on Exercise 4: $|V|=4$, $S=\{A,B,D\}$, $N(S)=\{J_2,J_5\}$, giving capacity $(4-3)+2=3<4$ — and the maximum flow is indeed 3 ✓ verified.)*
>
> **Notice what happened: a purely combinatorial statement about assignments was proved by exhibiting a cut.** The deficient set *is* the bottleneck, made visible as a cut in a network.
>
> **(d)** Because it shows the subject's ideas converging rather than accumulating. In this one theorem:
>
> - **[[06 - Counting Methods and the Pigeonhole Principle|Counting]]** supplies the pigeonhole argument that makes Hall's condition necessary;
> - **[[08 - Graph Theory|Graph theory]]** supplies the weighted directed graph and the bipartite structure;
> - **[[09 - Trees|Trees]]** supplied the greedy-with-exchange proof style, and the labelling search is a spanning-tree construction;
> - **[[02 - Proofs and Mathematical Induction|Proof technique]]** supplies the contradiction and the certificate reasoning;
> - **[[Optimization/contents/10 - Duality|Optimization]]** supplies the duality frame that explains why any of it works.
>
> **And the same structure appears in four disguises**: oil through pipes, applicants to jobs, LP duality, and the simplex method's reduced costs. `Optimization/contents/00-Index.md` called max-flow/min-cut "the most attractive omission" from that subject and pointed here; reading the two chapters together is the point.
>
> **The transferable lesson is the one worth keeping from the whole subject:** *look for the structure, not the surface.* A problem about marriages, a problem about pipes and a problem about linear inequalities were the same problem, and recognising that was worth more than any individual algorithm.

## 📝 Summary

- A **transport network** is a weighted directed graph with a **source** (no incoming edges), a **sink** (no outgoing edges) and nonnegative **capacities**.
- A **flow** satisfies $0\le F_{ij}\le C_{ij}$ (capacity) and **conservation of flow** at every intermediate vertex. **Flow out of the source $=$ flow into the sink** (Thm 10.1.5, by telescoping), and that common number is the **value**.
- **Multiple sources and sinks cost nothing:** add a **supersource** and **supersink** with infinite-capacity edges. The same trick converts matching into flow in §4 — **reduction by adding a supersource/supersink is this chapter's standard move.**
- **Augmenting paths** may use edges that are **properly oriented with slack** ($F<C$) *or* **improperly oriented with flow** ($F>0$). **The second case is essential** — without the ability to cancel earlier flow, a greedy method can stall below the optimum. In code it is the residual backward edge.
- A **cut** $(P,\overline P)$ has the source in $P$ and the sink in $\overline P$; its **capacity** counts only **forward**-crossing edges.
- **Weak duality (Thm 10.3.7): any cut's capacity $\ge$ any flow's value.** So a matching flow-and-cut pair is a **complete certificate of optimality for both** — no algorithm needed.
- **Max Flow, Min Cut (Thm 10.3.9): maximum flow $=$ minimum cut capacity.** The value is unique; **the minimising cut need not be** (five achieve it in the worked example).
- **The labelling algorithm produces the minimum cut for free** (Thm 10.3.11): at termination, labelled vs unlabelled is a cut whose forward edges are all saturated and backward edges all empty. **The algorithm emits its own optimality proof.**
- A **matching** is a set of edges sharing no vertex; **maximal** = most edges; **complete** = every vertex of $V$ matched.
- **Hall's theorem:** a complete matching exists **iff** $|N(S)|\ge|S|$ for every $S\subseteq V$. Necessity is pigeonhole; **a deficiency in one subset cannot be repaired by abundance elsewhere.**
- **Matching *is* a flow problem** (Thm 10.4.5): unit capacities plus supersource/supersink, and **the capacity constraints alone enforce "no shared vertex"**. Max flow $=$ max matching; flow $|V|$ $=$ complete matching.
- **Max-flow/min-cut is a duality theorem.** Max flow is an LP; its dual is min cut; weak and strong duality, complementary slackness (saturated $=$ binding) and the algorithm-produces-the-dual phenomenon all match [[Optimization/contents/10 - Duality|Optimization ch. 10]] exactly. **Hall's theorem is a corollary.**
- **The min cut is sensitivity information** — it names the binding capacities, i.e. where to invest to raise throughput. Several minimum cuts means several independent bottlenecks, and relieving one alone changes nothing.

## ⚠️ Important Notes

1. **The source has no incoming edges and the sink no outgoing edges — by definition.** If your graph violates this, add a supersource/supersink rather than bending the definitions.
2. **Conservation applies only to intermediate vertices**, never to the source or sink. Imposing it there would force the flow to be zero.
3. **A cut's capacity counts only forward-crossing edges.** Edges from $\overline P$ back into $P$ contribute nothing. Including them is the commonest arithmetic error in this chapter.
4. **$P$ must contain the source and $\overline P$ the sink.** A partition violating that is not a cut, and its "capacity" bounds nothing.
5. **Do not forget improperly oriented edges when hunting for an augmenting path.** A path may need to reduce flow somewhere to increase it overall — a purely forward search can terminate at a non-maximal flow and report it as maximal.
6. **To prove a flow maximal, exhibit a cut of equal capacity.** That is a complete proof and far easier than arguing that no augmenting path exists. It is the certificate property of duality.
7. **Max flow is unique in value, not in the flow itself** — and the minimum cut is likewise unique in capacity only. Check an implementation by comparing *values*, never edge-by-edge.
8. **Several minimum cuts means several bottlenecks.** Increasing capacity on one min cut's edges will not raise the maximum flow while another min cut remains. Read all of them before recommending an investment.
9. **Distinguish maximal from complete matching.** A maximal matching always exists; a complete one may not. Johnsonbaugh's example has a maximal matching of size 3 and no complete matching.
10. **Hall's condition must hold for *every* subset**, not just for single vertices or for $V$ itself. The failure in the worked example is at a 3-element subset, invisible if you check only individuals.
11. **Abundance elsewhere does not fix a local deficiency.** $C$'s four qualifications are irrelevant to the bottleneck among $A,B,D$ — which is precisely why Hall's condition quantifies over subsets.
12. **Unit capacities are what make the matching reduction work.** If you set them to anything else, the flow may match a vertex more than once and the correspondence with matchings breaks.
13. **Prefer reduction to a solved problem over a new algorithm.** Turning matching into max flow inherits both the algorithm and the optimality certificate. That is a general engineering principle, not a trick specific to this chapter.
14. **Read max-flow/min-cut as duality.** Weak duality gives free bounds and free proofs; the min cut gives sensitivity information; and Hall's theorem falls out as a corollary. **Cross-read with [[Optimization/contents/10 - Duality|Optimization ch. 10]]** — the two chapters are about the same mathematics.

> [!warning] Gaps in the source material
> **This is the shortest chapter in the book (26 pages) and proportionally the worst affected**, because almost everything it says is said with a labelled diagram.
>
> **Extraction preserved the definitions and theorem statements** — Definitions 10.1.1, 10.1.3, 10.1.6, 10.3.1, 10.3.4, 10.4.2 and Theorems 10.1.5, 10.2.3, 10.3.7, 10.3.9, 10.3.11 and 10.4.5 all came through with their content, which is enough to reconstruct the theory. **But every displayed formula and every worked computation is lost**, and so are all the figures.
>
> **Specifically unrecoverable:** Definition 10.1.3(b)'s conservation equation and Definition 10.1.6's definition of *value* survive only as the words preceding them; **Definition 10.3.4's formula for cut capacity is missing entirely**; and every example's numbers are gone. Examples 10.1.2, 10.1.4, 10.1.7, 10.3.2, 10.3.5, 10.3.6, 10.3.8 and 10.3.10 all refer to figures for their capacities, so **Johnsonbaugh's specific networks cannot be reconstructed.** The text mentions a cut of capacity 8 against a flow of 5, and a second cut of capacity 6 equalling a flow of 6, but **the capacities that produce those numbers are only in the lost figures.**
>
> **Consequently §3's worked example and all five exercises use my own network**, designed for the purpose and fully verified: capacities $ab(3)$, $ad(2)$, $bc(2)$, $be(1)$, $de(3)$, $cz(2)$, $ez(3)$, with **maximum flow 5 confirmed by augmentation and minimum cut 5 confirmed by enumerating all 16 cuts.** The five distinct minimum cuts were found the same way.
>
> **Algorithm 10.2.4 (the maximal flow algorithm) extracts as a heading with input/output lines and no body** — the same problem as every other Algorithm box in this book. **§2's Python is my own reconstruction** from Theorem 10.2.3 and the prose description of the labelling procedure, verified by running it on the network above and on the matching network.
>
> **All figures are images and are lost:** Figures 10.1.1–10.1.4 (the oil network, the pumping network, the supersource/supersink construction), 10.2.1–10.2.11 (**every augmenting-path illustration**, including the properly/improperly oriented examples that motivate Theorem 10.2.3), 10.3.1–10.3.2 (**the two cuts whose capacities the text discusses**), and 10.4.1–10.4.3 (the applicants-and-jobs bipartite graph, the matching shown in black, and the matching network).
>
> **Johnsonbaugh's Example 10.4.1 was recoverable**, unusually, because the qualifications are listed in prose rather than only drawn — though the text garbles applicant $B$'s list ("qualified for jobs $J_2$, and $J_5$", with a dropped item). **I have taken $B$'s qualifications to be $\{J_2,J_5\}$**, which is what makes the stated conclusion correct: the text's own argument is that "$A$, $B$ and $D$ are qualified for jobs $J_2$ and $J_5$", so all three share exactly that pair. **Verified consistent:** maximum matching 3, no complete matching, and the deficient set $\{A,B,D\}$ with $|N(S)|=2<3$.
>
> **No error was found in Johnsonbaugh ch. 10.** **Ten chapters in, the errata table in `00-Index.md` is still empty** — the only textbook in this vault of which that is true.
>
> **Additions beyond the source.** **Hall's theorem is not stated in Johnsonbaugh ch. 10** — the deficiency argument appears only inside Example 10.4.1, applied to one specific case. §4 states the theorem properly (both directions), and **Exercise 5(c) proves the necessity half by exhibiting a cut**, which is my own construction. **§5 in its entirety is mine**: the duality table, the observation that max flow is an LP whose dual is min cut, the role of total unimodularity in making the dual integral, the reading of the min cut as sensitivity information, and the identification of Hall's theorem as a corollary. Johnsonbaugh presents max-flow/min-cut purely combinatorially and never mentions linear programming. The **telescoping proof sketch** for Theorem 10.1.5, the emphasis that **unit capacities alone enforce the matching condition**, the note that **the minimum cut is not unique** (with all five exhibited), the remark that **several minimum cuts mean several independent bottlenecks**, and the observation that **the labelling algorithm emits its own certificate** — paralleling the simplex method's dual solution — are all mine. The closing framing in Exercise 5(d) is my own.
>
> **Nothing from this chapter was deliberately omitted.** Johnsonbaugh's "Problem-Solving Corner: Matching" (p. 528) is a worked-example section whose content is distributed through §4 and Exercise 4.

**Previous:** [[09 - Trees]] · **Next:** [[00-Index|back to the index]] — **this completes Discrete Mathematics.**
