---
subject: Optimization
chapter: 09
tags: [ds, optimization, linear-programming, simplex-method, basic-feasible-solution, standard-form, degeneracy, klee-minty]
source: "Chong & Żak, *An Introduction to Optimization* 4e, ch. 15–16; Luenberger & Ye, *Linear and Nonlinear Programming* 4e, ch. 2–3; Bertsimas & Tsitsiklis, *Introduction to Linear Optimization*, ch. 1–3"
---

# Linear Programming and the Simplex Method

> [!abstract] What this chapter is for
> **A self-contained world with its own geometry, its own algorithm and — in [[10 - Duality|ch. 10]] — the cleanest duality theory in mathematics.**
>
> $$\text{minimize }\ \mathbf c^{\mathsf T}\mathbf x\quad\text{subject to}\quad A\mathbf x=\mathbf b,\ \ \mathbf x\ge\mathbf 0$$
>
> **The whole subject rests on one observation and one algorithm:**
>
> | | |
> |---|---|
> | **The observation** | A linear objective on a polyhedron attains its optimum **at a vertex** — so an infinite search becomes a finite one |
> | **The algorithm** | **Simplex**: walk from vertex to neighbouring vertex, always downhill, and stop when no neighbour improves |
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Standard form | Everything converts, at the cost of extra variables |
> | **2** | **Basic solutions** | $\text{vertex}=\text{basic feasible solution}=$ a choice of $m$ columns |
> | **3** | **The fundamental theorem** | The optimum, if it exists, is at a **BFS**: at most $\binom nm$ candidates |
> | **4–5** | **The simplex algorithm** | Reduced costs choose who enters; the **ratio test** chooses who leaves |
> | **6** | Degeneracy, ties, unboundedness | The three things that go wrong, and what each means |
> | **7** | Complexity | **Exponential in the worst case, linear in practice** — the most famous gap in the subject |
>
> **§2 is the conceptual key.** "Vertex", "extreme point", "basic feasible solution" and "choice of $m$ linearly independent columns" are four names for one object, seen geometrically, convex-analytically, algebraically and combinatorially.

---

## 📘 Main Knowledge

### 1. Standard form

> [!important] Standard form
> $$\text{minimize }\ \mathbf c^{\mathsf T}\mathbf x\quad\text{s.t.}\quad A\mathbf x=\mathbf b,\ \ \mathbf x\ge\mathbf 0$$
> with $A\in\mathbb R^{m\times n}$, **$m<n$**, $\operatorname{rank}A=m$, and $\mathbf b\ge\mathbf 0$.
>
> **Note the shape: fewer equations than unknowns.** This is the underdetermined case of [[08 - Least Squares and Linear Equations|ch. 08]] — infinitely many solutions of $A\mathbf x=\mathbf b$ — and the constraints $\mathbf x\ge\mathbf 0$ plus the objective pick one out.

**Every linear program converts**, by the moves of [[01 - The Optimization Problem|ch. 01]] Exercise 1:

| Given | Do |
|---|---|
| $\max\mathbf c^{\mathsf T}\mathbf x$ | minimise $-\mathbf c^{\mathsf T}\mathbf x$ |
| $\mathbf a^{\mathsf T}\mathbf x\le b$ | add a **slack**: $\mathbf a^{\mathsf T}\mathbf x+s=b$, $s\ge0$ |
| $\mathbf a^{\mathsf T}\mathbf x\ge b$ | subtract a **surplus**: $\mathbf a^{\mathsf T}\mathbf x-s=b$, $s\ge0$ |
| $x_j\le0$ | substitute $x_j=-x_j'$ with $x_j'\ge0$ |
| $x_j$ free | split $x_j=u-v$ with $u,v\ge0$ |
| $b_i<0$ | multiply that row by $-1$ |
| $\lvert x_j\rvert\le c$ | write as two inequalities, then slack each |

**Neither slack nor surplus variables appear in the objective** — their cost coefficients are zero.

> [!note] The dimension changes but the problem does not
> Adding a slack moves the feasible set from $\{x_1\le7\}\subset\mathbb R$ to $\{x_1+x_2=7,\ x_2\ge0\}\subset\mathbb R^2$ — **a different set in a different space.** Chong & Żak spend three examples on this; the resolution is that **the orthogonal projection of the new set onto the original coordinates is exactly the old set**, so the two problems have the same solutions in the original variables.
>
> **The cost is dimension.** An LP with $m$ inequality constraints in $n$ variables becomes one with $m$ equalities in $n+m$ variables. **This is why the simplex method's complexity is usually quoted in terms of $m$ and $n$ after conversion.**

---

### 2. Basic solutions: the four names for one object

Since $\operatorname{rank}A=m$, pick $m$ linearly independent columns of $A$. Reorder so $A=[B\ |\ D]$ with $B$ the $m\times m$ non-singular **basis matrix**. Solve

$$B\mathbf x_B=\mathbf b\ \Longrightarrow\ \mathbf x_B=B^{-1}\mathbf b,\qquad \mathbf x=\begin{bmatrix}\mathbf x_B\\ \mathbf 0\end{bmatrix}$$

> [!important] Definitions
> | Term | Meaning |
> |---|---|
> | **Basic solution** | $\mathbf x=[\mathbf x_B^{\mathsf T},\mathbf 0^{\mathsf T}]^{\mathsf T}$ for some basis $B$ |
> | **Basic variables** / **basic columns** | the components of $\mathbf x_B$ / the columns of $B$ |
> | **Degenerate** basic solution | some basic variable is **zero** |
> | **Feasible solution** | any $\mathbf x$ with $A\mathbf x=\mathbf b$, $\mathbf x\ge\mathbf 0$ |
> | **Basic feasible solution (BFS)** | both — equivalently $\mathbf x_B=B^{-1}\mathbf b\ge\mathbf 0$ |

> [!important] The identification that makes LP work
> $$\underbrace{\text{vertex of the polyhedron}}_{\textbf{geometry}}=\underbrace{\text{extreme point}}_{\textbf{convexity, ch. 02}}=\underbrace{\text{basic feasible solution}}_{\textbf{algebra}}=\underbrace{\text{a choice of }m\text{ columns}}_{\textbf{combinatorics}}$$
>
> **The last equality is what turns a continuous problem into a finite one**: there are at most
> $$\binom{n}{m}=\frac{n!}{m!\,(n-m)!}$$
> choices, so at most that many candidates for the optimum. **The whole of LP algorithm design is about not examining all of them.**

> [!example]- Worked example — all ten bases, verified
> Wyndor Glass: $\max\ 3x_1+5x_2$ subject to $x_1\le4$, $2x_2\le12$, $3x_1+2x_2\le18$, $\mathbf x\ge\mathbf 0$. In standard form with slacks $s_1,s_2,s_3$:
> $$A=\begin{pmatrix}1&0&1&0&0\\0&2&0&1&0\\3&2&0&0&1\end{pmatrix},\quad \mathbf b=\begin{pmatrix}4\\12\\18\end{pmatrix},\quad \mathbf c=(-3,-5,0,0,0)^{\mathsf T}$$
> Here $m=3$, $n=5$, so $\binom53=10$ candidate bases:
>
> | Basis | $\mathbf x$ | Status | $\mathbf c^{\mathsf T}\mathbf x$ |
> |---|---|---|---|
> | $\{x_1,x_2,s_1\}$ | $(2,\ 6,\ 2,\ 0,\ 0)$ | **feasible** | $\mathbf{-36}$ |
> | $\{x_1,x_2,s_2\}$ | $(4,\ 3,\ 0,\ 6,\ 0)$ | feasible | $-27$ |
> | $\{x_1,x_2,s_3\}$ | $(4,\ 6,\ 0,\ 0,\ -6)$ | infeasible | — |
> | $\{x_1,s_1,s_2\}$ | $(6,\ 0,\ -2,\ 12,\ 0)$ | infeasible | — |
> | $\{x_1,s_1,s_3\}$ | — | **singular** | — |
> | $\{x_1,s_2,s_3\}$ | $(4,\ 0,\ 0,\ 12,\ 6)$ | feasible | $-12$ |
> | $\{x_2,s_1,s_2\}$ | $(0,\ 9,\ 4,\ -6,\ 0)$ | infeasible | — |
> | $\{x_2,s_1,s_3\}$ | $(0,\ 6,\ 4,\ 0,\ 6)$ | feasible | $-30$ |
> | $\{x_2,s_2,s_3\}$ | — | **singular** | — |
> | $\{s_1,s_2,s_3\}$ | $(0,\ 0,\ 4,\ 12,\ 18)$ | feasible | $0$ |
>
> **Ten bases, two singular, five feasible — and the feasible region is a pentagon with exactly five vertices.** The optimum is $(2,6)$ with value $36$ (as a maximum).
>
> **The correspondence is exact and it is the whole point.** *(Note also that "at most $\binom nm$" is genuinely "at most": singular column sets give no basic solution at all.)*

---

### 3. The Fundamental Theorem of Linear Programming

> [!important] Theorem (C&Ż 15.1)
> For an LP in standard form:
> 1. **If a feasible solution exists, a *basic* feasible solution exists.**
> 2. **If an optimal feasible solution exists, an optimal *basic* feasible solution exists.**

**Proof idea for part 1** — and it is worth knowing, because it is constructive. Let $\mathbf x$ be feasible with $p$ positive components, so $x_1\mathbf a_1+\cdots+x_p\mathbf a_p=\mathbf b$.

- **If $\mathbf a_1,\dots,\mathbf a_p$ are independent**, then $p\le m$; extend to a basis and $\mathbf x$ is already basic (degenerate if $p<m$). Done.
- **If they are dependent**, there are $y_i$ not all zero with $\sum y_i\mathbf a_i=\mathbf 0$, and we may assume some $y_i>0$. Then $A(\mathbf x-\varepsilon\mathbf y)=\mathbf b$ for every $\varepsilon$. **Take**
$$\varepsilon=\min\{x_i/y_i:\ y_i>0\}$$
**and at least one component becomes exactly zero while none goes negative.** Now $p$ has dropped by at least one; repeat.

**Part 2 adds one step:** if $\mathbf x$ is optimal one must also show $\mathbf c^{\mathsf T}\mathbf y=0$, else moving a small $\varepsilon$ in the profitable direction would beat $\mathbf x$ — contradicting optimality.

> [!important] Why this is *the* theorem
> **It converts a search over a continuum into a search over a finite set.** Without it, "minimise a linear function over a polyhedron" has uncountably many candidates; with it, at most $\binom nm$.
>
> **And note the $\varepsilon=\min\{x_i/y_i:y_i>0\}$ in the proof.** *That expression is the simplex method's ratio test*, appearing here for the first time — the algorithm of §4 is this proof turned into a loop.

---

### 4. The simplex algorithm: moving between bases

**Suppose $\mathbf x=[\mathbf x_B^{\mathsf T},\mathbf 0^{\mathsf T}]^{\mathsf T}$ is a BFS and we want to bring a non-basic column $\mathbf a_q$ into the basis.** Express it in the current basis, $\mathbf a_q=\sum_iy_{iq}\mathbf a_i$, multiply by $\varepsilon>0$ and subtract from $\sum_iy_{i0}\mathbf a_i=\mathbf b$:

$$\sum_{i=1}^m\big(y_{i0}-\varepsilon y_{iq}\big)\mathbf a_i+\varepsilon\mathbf a_q=\mathbf b$$

**As $\varepsilon$ grows from $0$, $x_q$ increases and each basic variable moves linearly.** To stay feasible, stop at the first zero:

> [!important] The ratio test
> $$\varepsilon=\min_i\left\{\frac{y_{i0}}{y_{iq}}:\ y_{iq}>0\right\},\qquad p=\arg\min_i\left\{\frac{y_{i0}}{y_{iq}}:\ y_{iq}>0\right\}$$
> **$\mathbf a_q$ enters the basis and $\mathbf a_p$ leaves.**
>
> **If no $y_{iq}>0$, no basic variable ever hits zero: $\varepsilon$ can grow without bound, the feasible set is unbounded in that direction — and if the objective improves along it, the LP is unbounded.**

**Which column should enter?** Compare objective values. With $\mathbf c_B$ the cost coefficients of the basic variables:

> [!important] Reduced costs
> $$\boxed{r_j=c_j-\mathbf c_B^{\mathsf T}B^{-1}\mathbf a_j}$$
> **$r_j$ is the net rate of change of the objective per unit increase of $x_j$** — the direct cost $c_j$ minus the saving from the basic variables that must adjust.
>
> | | |
> |---|---|
> | **Some $r_q<0$** | bringing $x_q$ in **decreases** the objective — do it |
> | **All $r_j\ge0$** | **no neighbouring vertex improves: the current BFS is optimal. STOP.** |

> [!important] The algorithm
> ```
> 1. Find an initial BFS (see §5) and its basis B.
> 2. Compute reduced costs  r = c − c_Bᵀ B⁻¹A.
> 3. If  r ≥ 0  →  STOP, current BFS is optimal.
> 4. Choose  q  with  r_q < 0        (entering variable)
> 5. Compute the column  y_q = B⁻¹a_q.
>    If  y_q ≤ 0  →  STOP, the LP is UNBOUNDED.
> 6. Ratio test:  p = argmin { y_i0 / y_iq : y_iq > 0 }   (leaving variable)
> 7. Pivot: swap a_q in, a_p out. Go to 2.
> ```
> **Each iteration is one pivot, costing $O(mn)$ in tableau form.**

**Entering-variable rules.** *Dantzig's rule* takes the most negative $r_q$ — greedy, and the classical default. *Bland's rule* takes the smallest index $q$ with $r_q<0$ — slower but **provably terminates** (§6).

> [!example]- The full trace, verified
> Wyndor Glass, standard form as in §2, minimising $\mathbf c^{\mathsf T}\mathbf x=-3x_1-5x_2$.
>
> **Iteration 0.** Basis $\{s_1,s_2,s_3\}$ (the slacks — an obvious starting BFS since $B=I$). $\mathbf x_B=(4,12,18)$, $z=0$.
> $$\mathbf r=(-3,\ -5,\ 0,\ 0,\ 0)$$
> Most negative is $r_2=-5$, so **$x_2$ enters**. Its column is $(0,2,2)^{\mathsf T}$; ratios $\tfrac{12}2=6$ and $\tfrac{18}2=9$ (row 1 has $y_{1q}=0$, skipped). **Minimum at row 2, so $s_2$ leaves.**
>
> **Iteration 1.** Basis $\{s_1,x_2,s_3\}$, $\mathbf x_B=(4,6,6)$, $z=-30$.
> $$\mathbf r=(-3,\ 0,\ 0,\ 2.5,\ 0)$$
> **$x_1$ enters.** Its column is $(1,0,3)^{\mathsf T}$; ratios $\tfrac41=4$ and $\tfrac63=2$. **Minimum at row 3, so $s_3$ leaves.**
>
> **Iteration 2.** Basis $\{s_1,x_2,x_1\}$, $\mathbf x_B=(2,6,2)$, $z=-36$.
> $$\mathbf r=(0,\ 0,\ 0,\ 1.5,\ 1)\ \ge\ \mathbf 0\quad\Longrightarrow\quad\textbf{OPTIMAL}$$
> $$\boxed{\mathbf x^*=(2,\ 6),\qquad \max=36}$$
>
> **Two pivots visited three of the five vertices** — $(0,0)\to(0,6)\to(2,6)$ — and never examined the other two. **That is simplex: a walk along edges of the polyhedron, always downhill.**
>
> *(Notice $r_{s_2}=1.5$ and $r_{s_3}=1$ at the optimum. Those two numbers are the **shadow prices** of constraints 2 and 3, and [[10 - Duality|ch. 10]] shows they are the optimal dual solution — the reduced costs of the slacks are the dual variables.)*

---

### 5. Finding a starting BFS: the two-phase method

**When all constraints are $\le$ with $\mathbf b\ge\mathbf 0$, the slacks form an obvious initial basis** ($B=I$, $\mathbf x_B=\mathbf b\ge\mathbf 0$) — as in the example above. **With equalities or $\ge$ constraints there is no such gift.**

> [!important] Phase I
> Add **artificial variables** $\mathbf u\ge\mathbf 0$ and solve
> $$\min\ \sum_i u_i\quad\text{s.t.}\quad A\mathbf x+I\mathbf u=\mathbf b,\ \ \mathbf x,\mathbf u\ge\mathbf 0$$
> **This has an obvious BFS ($\mathbf x=\mathbf 0$, $\mathbf u=\mathbf b$) and a bounded optimum $\ge0$.**
>
> | Phase I optimum | Meaning |
> |---|---|
> | $=0$ | all artificials driven to zero — **the resulting basis is a BFS of the original problem.** Proceed to Phase II |
> | $>0$ | **the original problem is infeasible** |
>
> **Phase II** then runs §4's algorithm from that BFS on the real objective.
>
> **So the simplex method also answers the feasibility question, for free** — a fact [[10 - Duality|ch. 10]] explains via Farkas' lemma.

**The revised simplex method** carries $B^{-1}$ (or a factorisation of it) rather than the full tableau, updating it by rank-one corrections. **For sparse large-scale LPs this is the only practical form** — the full tableau is dense even when $A$ is not.

---

### 6. The three things that go wrong

| | Symptom | Meaning | Fix |
|---|---|---|---|
| **Degeneracy** | a basic variable is $0$; the ratio test ties | **several bases describe the same vertex** — more than $n$ constraints meet there | usually harmless; see below |
| **Multiple optima** | $r_j=0$ for a **non-basic** $j$ at optimality | an entire edge or face is optimal | any of them is a solution |
| **Unboundedness** | $r_q<0$ but $\mathbf y_q\le\mathbf 0$ | improvement forever along a ray | the model is wrong |

> [!warning] Degeneracy can cause **cycling** — and it is a real phenomenon
> When the ratio test ties, the pivot moves to a *different basis for the same vertex* and the objective does not change. **In principle the algorithm can return to a basis it has already visited and loop forever.**
>
> - **Bland's rule** (smallest index among eligible entering *and* leaving variables) **provably prevents cycling** — the algorithm then terminates in finitely many steps, since it never repeats a basis and there are finitely many.
> - **Lexicographic / perturbation rules** do the same by breaking ties consistently.
> - **In practice cycling essentially never occurs**, and most implementations use Dantzig's rule with an anti-cycling fallback. **Degeneracy itself is extremely common** — any LP with redundant constraints has it — and merely causes wasted pivots.
>
> **Luenberger & Ye's assessment:** *"When degenerate solutions are encountered, the simplex procedure generally does not enter a cycle. However, anticycling procedures are simple, and many codes incorporate such a procedure for the sake of safety."*

---

### 7. Complexity: the famous gap

> [!important] Worst case: exponential
> **Klee and Minty (1972)** constructed an LP — a slightly perturbed $n$-dimensional cube — on which **Dantzig's rule visits all $2^n-1$ vertices before terminating.**
>
> | $n$ | vertices visited |
> |---|---|
> | $3$ | $7$ |
> | $10$ | $1\,023$ |
> | $20$ | $1\,048\,575$ |
> | $30$ | $1\,073\,741\,823$ |
>
> **So the simplex method is not a polynomial-time algorithm**, and *no* known pivoting rule is.

> [!important] Practice: linear
> **In practice simplex takes roughly $2m$ to $3m$ pivots** — linear in the number of constraints, essentially independent of $n$. Million-variable LPs are solved routinely.
>
> **The gap between $2^n$ and $3m$ is the most famous discrepancy between worst-case and typical behaviour in all of algorithms**, and explaining it took thirty years: **smoothed analysis** (Spielman & Teng, 2001) showed that simplex runs in polynomial time on any LP subjected to arbitrarily small random perturbation — i.e. **the exponential instances are isolated and infinitely fragile.**

> [!note] Polynomial-time methods exist, and both matter
> | Method | Complexity | Character |
> |---|---|---|
> | **Simplex** | exponential worst case, $\approx3m$ pivots typically | **vertex-following**, exact, warm-starts beautifully |
> | **Ellipsoid** (Khachiyan, 1979) | **polynomial** | first proof LP $\in$ P; **hopeless in practice** |
> | **Interior point** (Karmarkar, 1984) | **polynomial**, $O(\sqrt n\,L)$ iterations | cuts *through* the interior; wins on very large sparse problems |
>
> **Both simplex and interior-point are in every serious solver, and the solver chooses.** Simplex remains unbeaten when an LP must be re-solved after a small change — which is what branch-and-bound for integer programming does millions of times.
>
> **And the tractability line of [[02 - Convex Sets and Convex Functions|ch. 02]] holds:** LP is easy, but **integer** LP — the same problem with $\mathbf x\in\mathbb Z^n$ — is NP-hard. **Adding integrality, not nonlinearity, is what breaks it.**

---

## ✏️ Exercises

> [!question] Exercise 1 — standard form and basic solutions *(easy)*
> $$\max\ 2x_1+3x_2\quad\text{s.t.}\quad x_1+x_2\le4,\quad x_1+3x_2\le6,\quad \mathbf x\ge\mathbf 0$$
> **(a)** Convert to standard form.
> **(b)** How many candidate bases are there? Enumerate all basic solutions and mark the feasible ones.
> **(c)** Identify the optimum, and check it against the geometry.

> [!example]- Solution
> **(a)** Minimise $-2x_1-3x_2$ subject to
> $$x_1+x_2+s_1=4,\qquad x_1+3x_2+s_2=6,\qquad x_1,x_2,s_1,s_2\ge0$$
> $$A=\begin{pmatrix}1&1&1&0\\1&3&0&1\end{pmatrix},\quad\mathbf b=\begin{pmatrix}4\\6\end{pmatrix},\quad\mathbf c=(-2,-3,0,0)^{\mathsf T}$$
>
> **(b)** $m=2$, $n=4$, so $\binom42=6$ candidate bases.
>
> | Basis | $\mathbf x=(x_1,x_2,s_1,s_2)$ | Feasible? | Objective (max) |
> |---|---|---|---|
> | $\{x_1,x_2\}$ | $(3,\ 1,\ 0,\ 0)$ | ✔ | $\mathbf{9}$ |
> | $\{x_1,s_1\}$ | $(6,\ 0,\ -2,\ 0)$ | ✘ | — |
> | $\{x_1,s_2\}$ | $(4,\ 0,\ 0,\ 2)$ | ✔ | $8$ |
> | $\{x_2,s_1\}$ | $(0,\ 2,\ 2,\ 0)$ | ✔ | $6$ |
> | $\{x_2,s_2\}$ | $(0,\ 4,\ 0,\ -6)$ | ✘ | — |
> | $\{s_1,s_2\}$ | $(0,\ 0,\ 4,\ 6)$ | ✔ | $0$ |
>
> *(Basis $\{x_1,x_2\}$: solve $x_1+x_2=4$, $x_1+3x_2=6$ — subtracting gives $2x_2=2$, so $x_2=1$, $x_1=3$.)*
>
> **(c) The optimum is $(3,1)$ with value $9$.** The feasible region is a quadrilateral with vertices $(0,0)$, $(4,0)$, $(3,1)$, $(0,2)$ — **exactly the four feasible basic solutions** ✔, and the two infeasible bases correspond to the two intersection points of constraint lines that lie outside the region.
>
> **Note that $\binom42=6$ overcounts by two.** In general many bases are singular or infeasible, so the number of vertices is usually far below $\binom nm$ — but $\binom nm$ still grows exponentially, which is why §7 matters.

---

> [!question] Exercise 2 — the simplex method by hand *(medium)*
> Solve Exercise 1's problem by the simplex algorithm, tabulating reduced costs and ratio tests at every iteration.

> [!example]- Solution
> **Iteration 0.** Basis $\{s_1,s_2\}$, so $B=I$, $\mathbf c_B=\mathbf 0$, $\mathbf x_B=(4,6)$, $z=0$.
> $$\mathbf r=\mathbf c-\mathbf c_B^{\mathsf T}B^{-1}A=(-2,\ -3,\ 0,\ 0)$$
> Most negative is $r_2=-3$: **$x_2$ enters.** Column $\mathbf y_2=(1,3)^{\mathsf T}$; ratios $\tfrac41=4$ and $\tfrac63=2$. **Minimum in row 2: $s_2$ leaves.**
>
> **Iteration 1.** Basis $\{s_1,x_2\}$. Pivoting gives $\mathbf x_B=(2,\ 2)$, i.e. $\mathbf x=(0,2,2,0)$, $z=-6$.
> $$B=\begin{pmatrix}1&1\\0&3\end{pmatrix},\quad B^{-1}=\begin{pmatrix}1&-\tfrac13\\0&\tfrac13\end{pmatrix},\quad\mathbf c_B=(0,-3)$$
> $$\mathbf c_B^{\mathsf T}B^{-1}A=(-1,\ -3,\ 0,\ -1)\ \Longrightarrow\ \mathbf r=(-1,\ 0,\ 0,\ 1)$$
> **$x_1$ enters.** Column $\mathbf y_1=B^{-1}(1,1)^{\mathsf T}=(\tfrac23,\ \tfrac13)^{\mathsf T}$; ratios $\tfrac{2}{2/3}=3$ and $\tfrac{2}{1/3}=6$. **Minimum in row 1: $s_1$ leaves.**
>
> **Iteration 2.** Basis $\{x_1,x_2\}$, $\mathbf x=(3,1,0,0)$, $z=-9$.
> $$B=\begin{pmatrix}1&1\\1&3\end{pmatrix},\quad B^{-1}=\tfrac12\begin{pmatrix}3&-1\\-1&1\end{pmatrix},\quad\mathbf c_B=(-2,-3)$$
> $$\mathbf r=(0,\ 0,\ \tfrac32,\ \tfrac12)\ \ge\ \mathbf 0\quad\Longrightarrow\quad\textbf{OPTIMAL}$$
> $$\boxed{\mathbf x^*=(3,\ 1),\qquad \max=9}$$
>
> **Two pivots, path $(0,0)\to(0,2)\to(3,1)$ — three of the four vertices, and $(4,0)$ was never visited.**
>
> > [!tip]- Reading the final reduced costs
> > $r_{s_1}=\tfrac32$ and $r_{s_2}=\tfrac12$. **These are the shadow prices**: relaxing the first constraint from $4$ to $5$ would increase the optimal value by $\tfrac32$, and the second from $6$ to $7$ by $\tfrac12$. *(Check: with $x_1+x_2\le5$, $x_1+3x_2\le6$ the optimum moves to $(4.5,\ 0.5)$ with value $10.5=9+\tfrac32$ ✔.)*
> >
> > **[[10 - Duality|Chapter 10]] shows these are exactly the optimal dual variables** — so the simplex method solves the dual problem simultaneously and for free.

---

> [!question] Exercise 3 — degeneracy, multiple optima, unboundedness *(medium)*
> Diagnose each LP and say what the simplex method does.
> **(a)** $\max\ x_1+x_2$ s.t. $x_1+x_2\le4$, $2x_1+2x_2\le8$, $\mathbf x\ge\mathbf 0$
> **(b)** $\max\ 2x_1+4x_2$ s.t. $x_1+2x_2\le6$, $x_1\le4$, $\mathbf x\ge\mathbf 0$
> **(c)** $\max\ x_1+x_2$ s.t. $x_1-x_2\le1$, $-x_1+x_2\le1$, $\mathbf x\ge\mathbf 0$
> **(d)** $\min\ x_1+x_2$ s.t. $x_1+x_2\ge4$, $x_1+x_2\le2$, $\mathbf x\ge\mathbf 0$

> [!example]- Solution
> **(a) Degeneracy** — the second constraint is exactly twice the first, so both are active on the whole segment from $(4,0)$ to $(0,4)$. At the vertex $(4,0)$, the slacks are $s_1=0$ **and** $s_2=0$: **two basic variables are zero, so the BFS is degenerate.** The ratio test ties, and simplex may perform a pivot that changes the basis without moving the vertex or the objective.
>
> **Consequence:** wasted pivots, and in principle cycling — use Bland's rule. **The objective value is unaffected**, and $\max=4$ along the entire face.
>
> **(b) Multiple optima.** The objective $2x_1+4x_2$ is exactly twice the first constraint's left-hand side $x_1+2x_2$, so **the objective is constant on the line $x_1+2x_2=6$.** Every point of the segment from $(0,3)$ to $(4,1)$ is optimal with $\max=12$.
>
> **In the simplex tableau:** at the optimum some **non-basic** variable has $r_j=0$. **Bringing it in changes the vertex but not the objective** — which is exactly the signature of an optimal edge. *(The algorithm returns one vertex, arbitrarily; that a whole face is optimal is invisible unless you check the reduced costs.)*
>
> **(c) Unbounded.** The feasible region is the strip between $x_2\le x_1+1$ and $x_2\ge x_1-1$ in the first quadrant, which **extends to infinity along the direction $(1,1)$** — and the objective increases without limit along it.
>
> **In the tableau:** some $r_q<0$ while **every** entry of $\mathbf y_q=B^{-1}\mathbf a_q$ is $\le0$. **No ratio test is possible, $\varepsilon$ can grow forever, and the algorithm stops and reports unboundedness.**
>
> **Practical reading: an unbounded LP is almost always a modelling error** — a real resource constraint was omitted.
>
> **(d) Infeasible.** $x_1+x_2\ge4$ and $x_1+x_2\le2$ cannot both hold. **The feasible set is empty.**
>
> **This is detected in Phase I** (§5): the auxiliary problem $\min\sum u_i$ terminates with a **positive** optimum, certifying that no feasible point exists. **Phase II is never reached.**
>
> > [!important]- The complete taxonomy
> > **Every LP is in exactly one of four states**, and simplex identifies which:
> > | State | How simplex reports it |
> > |---|---|
> > | **Infeasible** | Phase I optimum $>0$ |
> > | **Unbounded** | some $r_q<0$ with $\mathbf y_q\le\mathbf 0$ |
> > | **Unique optimum** | all $r_j\ge0$, with $r_j>0$ for every non-basic $j$ |
> > | **Multiple optima** | all $r_j\ge0$, with $r_j=0$ for some non-basic $j$ |
> >
> > **This trichotomy — infeasible, unbounded, or an optimum attained at a vertex — has no analogue in nonlinear programming**, and it is the reason LP theory is so clean. **[[10 - Duality|Chapter 10]] explains it: each state has a *certificate* in the dual.**

---

> [!question] Exercise 4 — the geometry of a pivot *(medium–hard)*
> For the Wyndor problem of §2:
> **(a)** Sketch the feasible region and label all five vertices with their bases.
> **(b)** Trace the simplex path and show that each pivot moves along an **edge**.
> **(c)** Explain why exactly one basic variable changes per pivot, and what that means geometrically.
> **(d)** How many pivots would the worst possible pivoting rule need here?

> [!example]- Solution
> **(a)** The region is bounded by $x_1=0$, $x_2=0$, $x_1=4$, $2x_2=12$ and $3x_1+2x_2=18$. Its five vertices, with the slack that is *zero* at each shown alongside:
>
> | Vertex | Zero (non-basic) variables | Basis | Objective |
> |---|---|---|---|
> | $(0,0)$ | $x_1,x_2$ | $\{s_1,s_2,s_3\}$ | $0$ |
> | $(4,0)$ | $x_2,s_1$ | $\{x_1,s_2,s_3\}$ | $12$ |
> | $(4,3)$ | $s_1,s_3$ | $\{x_1,x_2,s_2\}$ | $27$ |
> | $(2,6)$ | $s_2,s_3$ | $\{x_1,x_2,s_1\}$ | $\mathbf{36}$ |
> | $(0,6)$ | $x_1,s_2$ | $\{x_2,s_1,s_3\}$ | $30$ |
>
> **A vertex in $\mathbb R^2$ is where two constraints are active, i.e. where two of the five variables are zero — i.e. where three are basic.** ✔
>
> **(b)** The trace of §4 was
> $$(0,0)\ \xrightarrow{\ x_2\text{ in},\ s_2\text{ out}\ }\ (0,6)\ \xrightarrow{\ x_1\text{ in},\ s_3\text{ out}\ }\ (2,6)$$
> with objective $0\to30\to36$. **$(0,0)$ and $(0,6)$ are adjacent** (both have $x_1=0$: they lie on the edge $x_1=0$), and **$(0,6)$ and $(2,6)$ are adjacent** (both have $s_2=0$: the edge $2x_2=12$). **Each pivot traverses one edge.**
>
> **(c)** A pivot swaps **one** column in and **one** out, so the new basis shares $m-1$ columns with the old. **Equivalently, the set of zero variables changes in exactly one place** — one constraint becomes inactive and another becomes active.
>
> **Geometrically, two vertices sharing $m-1$ basic variables lie on a common edge**, since the $n-m-1$ constraints still active at both define a one-dimensional face. **So "swap one column" and "walk one edge" are the same operation** — that identification is the geometric content of the simplex method.
>
> **(d)** There are five vertices, so **at most four pivots** — a path visiting every vertex once. The rule used took two.
>
> **In general the bound is the number of BFSs, at most $\binom nm$**; here $\binom53=10$, of which five are feasible. **The gap between "at most 4" and "took 2" is small in two dimensions and catastrophic in $n$**: §7's Klee–Minty cube has $2^n$ vertices and Dantzig's rule visits all but one of them.
>
> *(An open question worth knowing: the **Hirsch conjecture** asked whether any two vertices of a polyhedron with $m$ facets in $n$ dimensions are joined by a path of at most $m-n$ edges. **Santos disproved it in 2012**, but only barely — the true bound is still not known to be polynomial. **So it is not even known whether a good pivoting rule *could* exist.**)*

---

> [!question] Exercise 5 — worst case versus practice *(hard)*
> **(a)** The Klee–Minty cube in $n$ dimensions forces Dantzig's rule to visit $2^n-1$ vertices. Tabulate for $n=3,10,20,30$ and comment.
> **(b)** In practice simplex takes about $2m$–$3m$ pivots. Compare for an LP with $m=1000$, $n=5000$.
> **(c)** What is the resolution of this discrepancy?
> **(d)** LP is polynomial-time solvable. By what, and why is simplex still used?
> **(e)** Integer LP is NP-hard. Reconcile this with (d) and with [[02 - Convex Sets and Convex Functions|ch. 02]]'s tractability claim.

> [!example]- Solution
> **(a)**
>
> | $n$ | $2^n-1$ |
> |---|---|
> | $3$ | $7$ |
> | $10$ | $1\,023$ |
> | $20$ | $1\,048\,575$ |
> | $30$ | $\mathbf{1\,073\,741\,823}$ |
>
> **A 30-variable LP requiring a billion pivots.** *(The Klee–Minty construction is a unit cube whose facets are slightly tilted, so that the greedy rule is led along a Hamiltonian path through every vertex. The LP is trivial to solve by inspection — the difficulty is entirely an artefact of the pivoting rule.)*
>
> **(b)** With $m=1000$: **roughly $2\,000$–$3\,000$ pivots**, each $O(mn)=5\times10^6$ operations, so $\approx10^{10}$ operations — **seconds on a laptop.** The worst-case bound for the same problem is $\binom{5000}{1000}$, a number with over a thousand digits.
>
> **The observed count depends on $m$ and barely on $n$** — adding variables costs work per pivot but hardly changes the number of pivots. **That is why LPs with millions of columns are routine while ones with millions of rows are hard.**
>
> **(c) Smoothed analysis** (Spielman & Teng, 2001, Gödel Prize 2008). **The simplex method runs in expected polynomial time on any LP whose data is perturbed by arbitrarily small random noise.**
>
> **The resolution: the exponential instances are measure zero and infinitely fragile.** Klee–Minty needs its facets tilted at *exactly* the adversarial angles; perturb any coefficient in the tenth decimal place and the path collapses. **Real data — measured, rounded, estimated — is never adversarial in that way.**
>
> **This is a general lesson worth carrying beyond LP: worst-case complexity can be a bad predictor when the worst cases are unstable.** *(The same is true of the simplex method's cousin in machine learning: many hardness results about training are about adversarially constructed instances that do not resemble data.)*
>
> **(d) LP is in P**, proved by **Khachiyan's ellipsoid method** (1979) — a theoretical landmark that is **useless in practice**, being slow and numerically fragile on every real problem. **Karmarkar's interior-point method** (1984) is both polynomial *and* fast, and it cuts through the interior rather than following vertices.
>
> **Simplex survives for four reasons:**
> 1. **It is competitive** — often faster than interior-point on small and medium problems.
> 2. **It returns an exact vertex solution**, whereas interior-point converges to the *analytic centre* of the optimal face and needs a "crossover" step to reach a vertex.
> 3. **It warm-starts.** After changing one coefficient or adding one constraint, simplex resumes from the old basis in a few pivots; interior-point essentially restarts. **This is decisive for branch-and-bound**, which solves millions of nearly identical LPs.
> 4. **It produces the dual solution for free** ([[10 - Duality|ch. 10]]), which is what sensitivity analysis needs.
>
> **(e) There is no contradiction, and the reconciliation is the point of [[02 - Convex Sets and Convex Functions|ch. 02]] §4.**
>
> **The LP relaxation of an integer program is a convex problem and is easy.** Adding $\mathbf x\in\mathbb Z^n$ makes the feasible set a **finite scatter of lattice points** — which is not convex, has no interior, and admits no notion of "local information" at all. **The fundamental theorem of §3 fails immediately: the optimum need not be at a vertex of the relaxation, and rounding the LP solution can be arbitrarily bad or infeasible.**
>
> $$\textbf{LP} \in \text{P}\qquad\text{but}\qquad \textbf{ILP is NP-hard}$$
>
> **This is the sharpest confirmation of ch. 02's claim that the tractability boundary is convexity and not linearity.** Everything here is linear; **integrality alone moves the problem from polynomial to NP-hard.** *(And it is why integer programming is solved by **branch-and-bound**: relax to an LP, solve it, branch on a fractional variable, repeat — using LP as a subroutine, warm-started, millions of times.)*

---

## 📝 Summary

- **Standard form is $\min\mathbf c^{\mathsf T}\mathbf x$ s.t. $A\mathbf x=\mathbf b$, $\mathbf x\ge\mathbf 0$ with $m<n$, $\operatorname{rank}A=m$, $\mathbf b\ge\mathbf 0$.** Every LP converts, at the cost of slack, surplus and split variables.
- **Choosing $m$ independent columns gives a *basis* $B$ and a *basic solution* $\mathbf x_B=B^{-1}\mathbf b$**, with all non-basic variables zero. It is a **BFS** if $\mathbf x_B\ge\mathbf 0$, and **degenerate** if some basic variable is zero.
- **Vertex $=$ extreme point $=$ basic feasible solution $=$ choice of $m$ columns** — four names for one object, and the identification that turns a continuous problem into a finite one with at most $\binom nm$ candidates.
- **Fundamental theorem: if a feasible solution exists so does a BFS, and if an optimum exists it is attained at a BFS.** The proof's $\varepsilon=\min\{x_i/y_i:y_i>0\}$ *is* the simplex ratio test.
- **Simplex walks from vertex to adjacent vertex.** The **reduced costs** $r_j=c_j-\mathbf c_B^{\mathsf T}B^{-1}\mathbf a_j$ choose who enters ($r_q<0$) and the **ratio test** $\min\{y_{i0}/y_{iq}:y_{iq}>0\}$ chooses who leaves. **Stop when all $r_j\ge0$.**
- **Each pivot swaps one column and traverses one edge.** No $y_{iq}>0$ means unbounded; a positive Phase I optimum means infeasible.
- **The optimal reduced costs of the slacks are the shadow prices**, and [[10 - Duality|ch. 10]] shows they are the optimal dual solution — obtained for free.
- **Every LP is infeasible, unbounded, or has an optimum at a vertex** (unique if all non-basic $r_j>0$, otherwise a whole face). **There is no nonlinear analogue of this trichotomy.**
- **Worst case exponential ($2^n-1$ pivots on Klee–Minty), practice $\approx2m$–$3m$ pivots.** Smoothed analysis explains the gap: the bad instances are infinitely fragile. **LP is in P by ellipsoid and interior-point methods; simplex survives because it warm-starts, is exact, and hands you the dual.**
- **Integer LP is NP-hard.** Linearity is not the tractability boundary; **convexity is.**

---

## ⚠️ Important Notes

> [!warning] The six errors
> 1. **Running simplex without converting to standard form.** Equalities, $\mathbf x\ge\mathbf 0$ and $\mathbf b\ge\mathbf 0$ are all required.
> 2. **Forgetting that slacks have zero cost.** They do not appear in $\mathbf c$, but they *are* variables and *can* be basic.
> 3. **Ratio-testing on non-positive entries.** Only rows with $y_{iq}>0$ enter the test; if none do, the problem is unbounded.
> 4. **Confusing degeneracy with multiple optima.** Degeneracy is a *basic* variable equal to zero; multiple optima is a *non-basic* reduced cost equal to zero.
> 5. **Reading $\binom nm$ as the number of vertices.** It is an upper bound: many column sets are singular or infeasible.
> 6. **Concluding from Klee–Minty that simplex is impractical.** See Exercise 5(c).

> [!tip] Reading a final tableau
> | Look at | To learn |
> |---|---|
> | $\mathbf x_B=B^{-1}\mathbf b$ | the optimal solution |
> | $\mathbf c_B^{\mathsf T}\mathbf x_B$ | the optimal value |
> | $r_j$ for non-basic $j$ | **$=0$ $\Rightarrow$ multiple optima** |
> | $r_j$ of the **slacks** | **the shadow prices $=$ the optimal dual solution** |
> | which slacks are basic | which constraints are **not** binding |

> [!note] Where this chapter connects
> - **[[02 - Convex Sets and Convex Functions|Ch. 02]] §2** supplies the geometry — the feasible set is a polyhedron, extreme points are §2's vertices — **and the polytope/polyhedron naming clash flagged there matters here**, since C&Ż's ch. 15–16 use the non-standard convention.
> - **[[10 - Duality|Ch. 10]]** is the other half of this chapter: the reduced costs already computed *are* the dual variables.
> - **[[08 - Least Squares and Linear Equations|Ch. 08]]** — $A\mathbf x=\mathbf b$ with $m<n$ is the same underdetermined system; **least squares picks the minimum-norm solution, LP picks the one optimising a linear objective subject to $\mathbf x\ge\mathbf 0$.**
> - **[[12 - Convex Programming and Constrained Algorithms|Ch. 12]]** — interior-point methods for LP are the ancestors of modern convex solvers.
> - **[[Microeconomics/contents/00-Index|Microeconomics]]** — the diet problem, the transportation problem and production planning are the founding applications, and **shadow prices are marginal values of resources.**

---

> [!warning] Gaps in the source material
> **Source split.** Structure and all worked material from **Chong & Żak ch. 15–16**; the fundamental theorem and the degeneracy discussion cross-checked against **Luenberger & Ye ch. 2–3**, whose extraction is clean. **Bertsimas & Tsitsiklis was consulted and largely could not be used** — see below.
>
> **Chong & Żak OCR damage:**
> - **Every matrix and every tableau loses its structure.** Example 15.12's $A$ extracts as `11-14 / 1-2-11`, which is $\begin{psmallmatrix}1&1&-1&4\\1&-2&-1&1\end{psmallmatrix}$; Example 15.13's augmented matrix extracts as `2 3-1-1 -1 / 4 11-29`, which is $\left(\begin{smallmatrix}2&3&-1&-1&\vline&-1\\4&1&1&-2&\vline&9\end{smallmatrix}\right)$. **Minus signs run into the digits that follow them**, so every entry had to be recovered by checking against the book's own stated solutions.
> - **`XB`, `Xß`, `xB`, `x5` are all $\mathbf x_B$**; `2/io`, `y^`, `yiq`, `ypq` are the tableau entries $y_{i0}$, $y_{iq}$, $y_{pq}$; `ε` prints as `e`, `£`, `zy` and `£*`; `Ω` is the feasible set; `1Z(A)` is $\mathcal R(A)$.
> - **`sigmin` and `diTgrnm` and `arg min` all mean $\arg\min$**, and `mm{...}` means $\min\{\dots\}$.
> - **Figures 15.7–15.10 (the projection arguments for slack variables) and every figure showing a feasible region are images and are lost.** For a chapter whose central claim is geometric — *the optimum is at a vertex* — **this is the most damaging figure loss in the book.** §2's table of ten bases and Exercise 4's vertex table are my substitutes.
>
> **Bertsimas & Tsitsiklis was largely unusable, as [[00-Index|the index]] warned.** Its ch. 1–3 cover exactly this material at greater depth, but **its OCR scrambles words internally** (`cOllstraints`, `dirrlem;ion`, `ort;hogo'rralto`), **drops `=` signs entirely** (`Ax b` for $A\mathbf x=\mathbf b$), renders both $\ge$ and $\le$ as `2:`/`~`/`:::;`, and — worst — **leaves some boxed definitions and theorems with no text layer at all**, so the surrounding prose reads as though nothing is missing. **Nothing in this chapter is taken from it that Chong & Żak or Luenberger & Ye do not independently state.**
>
> **Verification performed.** All computations checked with `numpy` and `scipy.optimize.linprog`:
> - **The Wyndor example**: the optimum $(2,6)$ with value $36$; **all ten bases enumerated**, confirming two singular, five feasible and five infeasible, with the five feasible ones matching the pentagon's five vertices exactly.
> - **The full simplex trace**: reduced costs $(-3,-5,0,0,0)\to(-3,0,0,2.5,0)\to(0,0,0,1.5,1)$, the ratio tests $\{6,9\}$ and $\{4,2\}$, the bases $\{s_1,s_2,s_3\}\to\{s_1,x_2,s_3\}\to\{s_1,x_2,x_1\}$, and the objective $0\to-30\to-36$ — **every number computed independently from $B^{-1}$.**
> - **Exercise 1's six bases** and **Exercise 2's two pivots**, including the shadow-price check that relaxing constraint 1 from $4$ to $5$ raises the optimum from $9$ to $10.5$.
> - **The Klee–Minty counts** $2^n-1$ for $n=3,10,20,30$.
> - **C&Ż Example 15.13's six basic solutions** — $(14/5,-11/5,0,0)$, $(4/3,0,11/3,0)$, the singular basis $[\mathbf a_1,\mathbf a_4]$, $(0,2,7,0)$, $(0,-11/5,0,-28/5)$ and $(0,0,11/3,-8/3)$ — **all reproduce exactly as printed.**
>
> **No mathematical error was found in Chong & Żak ch. 15–16.**
>
> **Scope and additions.**
> - **§7 (complexity) is almost entirely my own addition.** Chong & Żak never mention Klee–Minty, worst-case complexity, or smoothed analysis; Luenberger & Ye mention in one sentence that the number of steps "could be exponential" without saying how or why it does not matter. **For a reader deciding whether to trust an LP solver, the worst-case/practice gap and its resolution are the operative facts**, and the Spielman–Teng result is the answer.
> - **The four-way identification in §2 (vertex $=$ extreme point $=$ BFS $=$ column choice) is my own framing.** The books establish the pieces in separate sections; **stating it as one identification is what makes the fundamental theorem feel inevitable rather than surprising.**
> - **The observation in §3 that the fundamental theorem's $\varepsilon$ *is* the simplex ratio test is mine**, and is the cleanest way to see that the algorithm is the proof.
> - **§6's four-state taxonomy table and Exercise 3's version of it are my own**, as is the remark that the trichotomy has no nonlinear analogue.
> - **The shadow-price readings in §4 and Exercise 2, and the observation that simplex solves the dual for free, are mine** — C&Ż defer all of it to ch. 17 without forward reference, and it is the single most useful thing in a final tableau.
> - **Exercise 5(e) (the LP/ILP boundary as confirmation of ch. 02's convexity claim) and the Hirsch conjecture remark in Exercise 4(d) are my own additions.**

#optimization #linear-programming #simplex-method #basic-feasible-solution #standard-form #degeneracy #shadow-price #klee-minty #interior-point
