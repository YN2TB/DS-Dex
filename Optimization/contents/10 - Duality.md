---
subject: Optimization
chapter: 10
tags: [ds, optimization, linear-programming, duality, complementary-slackness, shadow-prices, farkas, sensitivity-analysis]
source: "Chong & Żak, *An Introduction to Optimization* 4e, ch. 17; Luenberger & Ye, *Linear and Nonlinear Programming* 4e, ch. 4; Bertsimas & Tsitsiklis, *Introduction to Linear Optimization*, ch. 4"
---

# Duality

[[09 - Linear Programming and the Simplex Method|Chapter 09]] left a loose end. When the simplex method finished on the Wyndor problem, the final reduced costs of the two slack variables were $r_{s_2}=1.5$ and $r_{s_3}=1$, and the chapter claimed those numbers were the **shadow prices** of the two constraints — the rate at which the optimal value would improve if the corresponding resource were increased. Nothing in chapter 09 explained why the leftovers of the simplex bookkeeping should mean that.

This chapter explains it. The answer is that **every linear program is secretly two linear programs**, and the simplex method solves both at once. One of them minimizes; the other maximizes; they meet exactly. The numbers left in the bottom row of the final tableau are the solution to the second one.

Duality is the single most useful idea in this book. It is the reason you can *prove* a solution is optimal instead of merely failing to improve it; the reason a linear program's answer comes with an economic interpretation for free; the reason infeasibility has a certificate; and — in the Lagrangian form that [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]] generalises it to — the reason support vector machines can be kernelised.

## 📘 Main Knowledge

### 1. Where the dual comes from: the bounding question

Start with a minimization problem in the form [[02 - Convex Sets and Convex Functions|ch. 02]] would call a polyhedron:

$$\text{minimize } \mathbf c^{\mathsf T}\mathbf x \quad\text{subject to}\quad A\mathbf x\ge\mathbf b,\ \mathbf x\ge\mathbf 0.$$

Suppose someone hands you a feasible $\mathbf x$ with $\mathbf c^{\mathsf T}\mathbf x=37$. You now know the optimal value is **at most** 37. Upper bounds are easy: every feasible point supplies one.

**Lower bounds are the hard direction.** How could you ever be sure no feasible point achieves 36? You would need an argument valid for *all* feasible $\mathbf x$ at once, and there are infinitely many of them.

Here is the trick, and the whole chapter is contained in it. Take any vector $\mathbf y\ge\mathbf 0$ and form the nonnegative combination $\mathbf y^{\mathsf T}(A\mathbf x)\ge\mathbf y^{\mathsf T}\mathbf b$ — valid because $A\mathbf x\ge\mathbf b$ componentwise and the weights $y_i$ are nonnegative, so the inequality survives. Now suppose in addition that $\mathbf y$ satisfies

$$\mathbf y^{\mathsf T}A\le\mathbf c^{\mathsf T}.$$

Then for any feasible $\mathbf x$ (in particular $\mathbf x\ge\mathbf 0$, which is what lets us multiply through by $\mathbf x$ without flipping the sign):

$$\mathbf y^{\mathsf T}\mathbf b\ \le\ \mathbf y^{\mathsf T}A\mathbf x\ \le\ \mathbf c^{\mathsf T}\mathbf x .$$

**Every such $\mathbf y$ certifies a lower bound $\mathbf y^{\mathsf T}\mathbf b$ on the optimal value, in one line, valid for all feasible $\mathbf x$ simultaneously.** The bound is a *number you can check by hand* — no optimization required to verify it, only to find it.

Naturally you want the best such bound, which means solving

$$\text{maximize } \mathbf y^{\mathsf T}\mathbf b \quad\text{subject to}\quad \mathbf y^{\mathsf T}A\le\mathbf c^{\mathsf T},\ \mathbf y\ge\mathbf 0.$$

That is another linear program. It is **the dual**, and it was not invented — it was *derived* as "the problem of finding the best certificate."

> [!note] This is the pattern for the whole subject
> The dual is always "the tightest bound obtainable by taking a nonnegative combination of the constraints." [[11 - Constrained Optimization - Lagrange and KKT|Ch. 11]] does the same thing for nonlinear constraints and gets the Lagrangian; [[12 - Convex Programming and Constrained Algorithms|ch. 12]] does it for convex programs. Everything downstream is this paragraph with harder algebra.

### 2. The symmetric form, and the dual of the dual

The pair just derived is the **symmetric form of duality**:

| Primal | Dual |
|---|---|
| minimize $\mathbf c^{\mathsf T}\mathbf x$ | maximize $\mathbf y^{\mathsf T}\mathbf b$ |
| subject to $A\mathbf x\ge\mathbf b$ | subject to $\mathbf y^{\mathsf T}A\le\mathbf c^{\mathsf T}$ |
| $\mathbf x\ge\mathbf 0$ | $\mathbf y\ge\mathbf 0$ |

Note what got swapped: **$\mathbf b$ and $\mathbf c$ trade places**, $A$ is transposed, the inequalities reverse, and min becomes max. There are $m$ dual variables (one per primal *constraint*) and $n$ dual constraints (one per primal *variable*).

**The dual of the dual is the primal.** Write the dual as a minimization, $\min\ \mathbf y^{\mathsf T}(-\mathbf b)$ subject to $\mathbf y^{\mathsf T}(-A)\ge-\mathbf c^{\mathsf T}$, $\mathbf y\ge\mathbf 0$. That is the symmetric primal form with data $(-A,-\mathbf c,-\mathbf b)$, so its dual is $\max\ (-\mathbf c^{\mathsf T})\mathbf x$ subject to $(-A)\mathbf x\le-\mathbf b$, $\mathbf x\ge\mathbf 0$ — which is the original primal. **So "primal" and "dual" are labels of convenience, not properties.** Either problem is the dual of the other, and any theorem proved for one direction applies to the other for free. This is used constantly and silently.

### 3. Every LP has a dual: the standard form and the general recipe

For the **standard form** of [[09 - Linear Programming and the Simplex Method|ch. 09]] the derivation runs through the trick of splitting an equality into two inequalities. Since $A\mathbf x=\mathbf b$ is equivalent to $A\mathbf x\ge\mathbf b$ together with $-A\mathbf x\ge-\mathbf b$, the coefficient matrix becomes $\begin{bmatrix}A\\-A\end{bmatrix}$ and the dual vector splits as $(\mathbf u,\mathbf v)\ge\mathbf 0$, giving $\max\ \mathbf u^{\mathsf T}\mathbf b-\mathbf v^{\mathsf T}\mathbf b$ subject to $(\mathbf u-\mathbf v)^{\mathsf T}A\le\mathbf c^{\mathsf T}$. Setting $\mathbf y=\mathbf u-\mathbf v$ — **a difference of two nonnegative vectors, hence an arbitrary vector** — collapses it to the **asymmetric form**:

| Primal | Dual |
|---|---|
| minimize $\mathbf c^{\mathsf T}\mathbf x$ | maximize $\mathbf y^{\mathsf T}\mathbf b$ |
| subject to $A\mathbf x=\mathbf b$ | subject to $\mathbf y^{\mathsf T}A\le\mathbf c^{\mathsf T}$ |
| $\mathbf x\ge\mathbf 0$ | ($\mathbf y$ **free**) |

**The equality constraints bought a free dual variable.** That is the general principle, and it generates the whole recipe. For a **minimization** primal:

| Primal (min) | ⟷ | Dual (max) |
|---|---|---|
| constraint $\mathbf a_i^{\mathsf T}\mathbf x\ge b_i$ | | variable $y_i\ge0$ |
| constraint $\mathbf a_i^{\mathsf T}\mathbf x\le b_i$ | | variable $y_i\le0$ |
| constraint $\mathbf a_i^{\mathsf T}\mathbf x=b_i$ | | variable $y_i$ **free** |
| variable $x_j\ge0$ | | constraint $(A^{\mathsf T}\mathbf y)_j\le c_j$ |
| variable $x_j\le0$ | | constraint $(A^{\mathsf T}\mathbf y)_j\ge c_j$ |
| variable $x_j$ **free** | | constraint $(A^{\mathsf T}\mathbf y)_j=c_j$ |

Reading the table right-to-left gives the rules for a maximization primal.

> [!warning] Do not memorise this table
> It is four sign conventions deep and everybody gets it backwards under exam pressure. **Derive it instead**, which takes fifteen seconds: convert whatever you are given into the symmetric primal form (flip $\le$ to $\ge$ by negating; split equalities; write a free variable as $x^+-x^-$), apply the one form you *do* remember, then simplify. That is exactly how the table was generated. The one thing worth committing to memory is the pair of slogans: **a tighter constraint buys a freer dual variable, and a freer primal variable buys a tighter dual constraint.**

### 4. Weak duality — the certificate property

**Lemma (weak duality).** *If $\mathbf x$ is primal-feasible and $\mathbf y$ is dual-feasible (either form), then $\mathbf c^{\mathsf T}\mathbf x\ \ge\ \mathbf y^{\mathsf T}\mathbf b$.*

*Proof (asymmetric form).* $\mathbf y^{\mathsf T}\mathbf b=\mathbf y^{\mathsf T}(A\mathbf x)=(\mathbf y^{\mathsf T}A)\mathbf x\le\mathbf c^{\mathsf T}\mathbf x$, the last step because $\mathbf y^{\mathsf T}A\le\mathbf c^{\mathsf T}$ and $\mathbf x\ge\mathbf 0$. $\blacksquare$

That is the whole proof — two equalities and one inequality. The symmetric case is the derivation of §1.

Weak duality is small and it does an enormous amount of work:

- **"maximum $\le$ minimum."** The dual value never exceeds the primal value. Every dual-feasible point sits below every primal-feasible point, with a gap in between.
- **Any feasible pair brackets the answer.** With $\mathbf c^{\mathsf T}\mathbf x=37$ and $\mathbf y^{\mathsf T}\mathbf b=35$ you know the optimum lies in $[35,37]$ without solving anything. This is how large integer programs are actually attacked: the LP dual supplies the lower bound in branch-and-bound.
- **Unboundedness in one kills feasibility in the other.** If the primal minimum is $-\infty$, no $\mathbf y$ can satisfy $\mathbf y^{\mathsf T}\mathbf b\le-M$ for every $M$, so **the dual feasible set is empty.** Symmetrically if the dual is unbounded above the primal is infeasible.
- **Matching values prove optimality.** This is the corollary that matters most:

**Theorem.** *If $\mathbf x_0,\mathbf y_0$ are feasible for primal and dual respectively and $\mathbf c^{\mathsf T}\mathbf x_0=\mathbf y_0^{\mathsf T}\mathbf b$, then both are optimal.*

*Proof.* For any primal-feasible $\mathbf x$, weak duality against $\mathbf y_0$ gives $\mathbf c^{\mathsf T}\mathbf x\ge\mathbf y_0^{\mathsf T}\mathbf b=\mathbf c^{\mathsf T}\mathbf x_0$, so $\mathbf x_0$ is primal-optimal. For any dual-feasible $\mathbf y$, weak duality against $\mathbf x_0$ gives $\mathbf y^{\mathsf T}\mathbf b\le\mathbf c^{\mathsf T}\mathbf x_0=\mathbf y_0^{\mathsf T}\mathbf b$, so $\mathbf y_0$ is dual-optimal. $\blacksquare$

**This is the certificate property, and it is a genuine change in kind.** Every algorithm in chapters 04–08 stops when it cannot improve — a *local*, negative statement that depends on trusting the algorithm's logic. A matching dual solution is a *global*, positive statement that anyone can verify with a matrix multiply and a dot product, without trusting the solver at all. If a commercial LP solver returns $\mathbf x^\star$ and $\mathbf y^\star$, you can check the answer yourself in four lines of NumPy.

### 5. The duality theorem: the gap is always zero

Weak duality permits a gap. The remarkable fact is that for linear programs there never is one.

**Theorem (strong duality).** *If either problem has a finite optimal solution, so does the other, and their optimal values are equal. If either has an unbounded objective, the other is infeasible.*

There are two standard proofs and they teach different things.

**Proof 1 — constructive, via the simplex method.** Let the primal (asymmetric form) have an optimal basic feasible solution with basis $B$, and partition $A=[B,D]$ as in [[09 - Linear Programming and the Simplex Method|ch. 09]]. Optimality of the basis means every reduced cost is nonnegative:

$$\mathbf r_D^{\mathsf T}=\mathbf c_D^{\mathsf T}-\mathbf c_B^{\mathsf T}B^{-1}D\ \ge\ \mathbf 0^{\mathsf T} \qquad\Longrightarrow\qquad \mathbf c_B^{\mathsf T}B^{-1}D\ \le\ \mathbf c_D^{\mathsf T}.$$

Now **define**

$$\boxed{\ \mathbf y^{\mathsf T}=\mathbf c_B^{\mathsf T}B^{-1}\ }$$

and check that it is dual-feasible: $\mathbf y^{\mathsf T}A=\mathbf y^{\mathsf T}[B,D]=[\mathbf c_B^{\mathsf T},\ \mathbf c_B^{\mathsf T}B^{-1}D]\le[\mathbf c_B^{\mathsf T},\mathbf c_D^{\mathsf T}]=\mathbf c^{\mathsf T}$. The first block is an equality and the second is the reduced-cost inequality just established. Its objective value is $\mathbf y^{\mathsf T}\mathbf b=\mathbf c_B^{\mathsf T}B^{-1}\mathbf b=\mathbf c_B^{\mathsf T}\mathbf x_B$, the primal optimal value. By the theorem of §4, $\mathbf y$ is dual-optimal. $\blacksquare$

**Read that again, because it is the answer to chapter 09's loose end.** The simplex method never mentions the dual, yet the quantity $\mathbf c_B^{\mathsf T}B^{-1}$ that it computes at *every* iteration in order to price the columns **is** the dual solution the moment the primal basis becomes optimal. The dual was being computed all along as a by-product. Before termination $\mathbf c_B^{\mathsf T}B^{-1}$ is dual-*infeasible* (some reduced cost is negative), so the simplex method can be read as: *maintain primal feasibility, and drive the dual towards feasibility.* [[#8 Reading the dual off the final tableau|§8]] shows how to read $\mathbf y$ straight off the tableau.

**Proof 2 — general, via a separating hyperplane.** The constructive proof assumes the primal has a basic feasible optimum, which needs the fundamental theorem of LP and hence $A$ of full rank. Luenberger & Ye prove strong duality without that, using the [[02 - Convex Sets and Convex Functions|convexity]] machinery: define the closed convex cone

$$C=\{(r,\mathbf w)\ :\ r=tz_0-\mathbf c^{\mathsf T}\mathbf x,\ \ \mathbf w=t\mathbf b-A\mathbf x,\ \ \mathbf x\ge\mathbf 0,\ t\ge0\}\subset\mathbb R^{m+1},$$

where $z_0$ is the primal optimal value. One shows $(1,\mathbf 0)\notin C$ — this is where optimality of $z_0$ is used — then separates the point from the cone by a hyperplane $[s,\mathbf y]$. Because $C$ is a *cone* the separating constant must be $0$, which forces $s<0$, normalised to $s=-1$. The separation inequality $(\mathbf c-\mathbf y^{\mathsf T}A)\mathbf x-tz_0+t\mathbf y^{\mathsf T}\mathbf b\ge0$ for all $\mathbf x\ge\mathbf 0,t\ge0$ then yields both conclusions by specialisation: **$t=0$ gives $\mathbf y^{\mathsf T}A\le\mathbf c^{\mathsf T}$ (dual feasibility), and $\mathbf x=\mathbf 0,t=1$ gives $\mathbf y^{\mathsf T}\mathbf b\ge z_0$ (dual optimality, via §4).** $\blacksquare$

The separating hyperplane *is* the dual solution. That is worth holding onto: it is why duality reappears in every convex setting and not just in linear programming, and it is the geometric content of [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]]'s multipliers.

### 6. The four states — and both problems can be infeasible

Weak and strong duality together restrict which combinations can occur. There are exactly **four**:

| | Dual optimal | Dual unbounded | Dual infeasible |
|---|---|---|---|
| **Primal optimal** | ✅ possible, equal values | ✗ impossible | ✗ impossible |
| **Primal unbounded** | ✗ impossible | ✗ impossible | ✅ possible |
| **Primal infeasible** | ✗ impossible | ✅ possible | ✅ **possible** |

The bottom-right cell is the one everybody gets wrong. **Infeasibility of one problem does *not* imply unboundedness of the other.** Chong & Żak's Example 17.7 settles it:

$$\text{minimize } x_1-2x_2 \quad\text{s.t.}\quad \begin{aligned}x_1-x_2&\ge2\\ -x_1+x_2&\ge-1\end{aligned},\quad \mathbf x\ge\mathbf 0$$

is infeasible, since the constraints demand $x_1-x_2\ge2$ and $x_1-x_2\le1$ at once. Its symmetric dual is $\max\ 2y_1-y_2$ subject to $y_1-y_2\le1$, $-y_1+y_2\le-2$, $\mathbf y\ge\mathbf 0$ — which demands $y_1-y_2\le1$ and $y_1-y_2\ge2$, also impossible. **Both infeasible.** (Verified: `linprog` returns status 2 for each.)

So "infeasible or unbounded" is a genuinely two-way ambiguity, which is exactly why solvers report those two statuses separately and why a Phase I is needed to distinguish them.

### 7. Complementary slackness: the bridge between the two solutions

Strong duality says the optimal values match. **Complementary slackness** says *how* the two solution vectors are related, and it is the tool that lets you convert a solution of one problem into a solution of the other by hand.

**Theorem (complementary slackness).** *Feasible $\mathbf x,\mathbf y$ are both optimal if and only if*

$$\text{(i)}\ \ (\mathbf c^{\mathsf T}-\mathbf y^{\mathsf T}A)\,\mathbf x=0 \qquad\text{and}\qquad \text{(ii)}\ \ \mathbf y^{\mathsf T}(A\mathbf x-\mathbf b)=0.$$

*Proof (symmetric form, ⟹).* By strong duality $\mathbf c^{\mathsf T}\mathbf x=\mathbf y^{\mathsf T}\mathbf b$. Then $(\mathbf c^{\mathsf T}-\mathbf y^{\mathsf T}A)\mathbf x=\mathbf c^{\mathsf T}\mathbf x-\mathbf y^{\mathsf T}A\mathbf x=\mathbf y^{\mathsf T}\mathbf b-\mathbf y^{\mathsf T}A\mathbf x=\mathbf y^{\mathsf T}(\mathbf b-A\mathbf x)\le0$ using $A\mathbf x\ge\mathbf b,\mathbf y\ge\mathbf 0$. But also $\mathbf y^{\mathsf T}A\le\mathbf c^{\mathsf T}$ and $\mathbf x\ge\mathbf 0$ give $(\mathbf c^{\mathsf T}-\mathbf y^{\mathsf T}A)\mathbf x\ge0$. Both, so it is $0$. Condition (ii) follows the same way. (⟸) Combining (i) and (ii) gives $\mathbf c^{\mathsf T}\mathbf x=\mathbf y^{\mathsf T}A\mathbf x=\mathbf y^{\mathsf T}\mathbf b$, so §4 applies. $\blacksquare$

**The useful form is componentwise.** Each condition is a sum of terms that are individually of one sign, so the sum vanishing forces every term to vanish:

$$x_j>0\ \Longrightarrow\ (A^{\mathsf T}\mathbf y)_j=c_j, \qquad\qquad (A^{\mathsf T}\mathbf y)_j<c_j\ \Longrightarrow\ x_j=0,$$
$$y_i>0\ \Longrightarrow\ \mathbf a_i^{\mathsf T}\mathbf x=b_i, \qquad\qquad \mathbf a_i^{\mathsf T}\mathbf x>b_i\ \Longrightarrow\ y_i=0.$$

In words: **a primal variable used at a positive level forces its dual constraint tight; a slack dual constraint forces its primal variable to zero; a positively priced constraint must be binding; a non-binding constraint has price zero.** The last is the most quotable: **you will not pay for a resource you are not using up.**

For an optimal basic feasible solution in asymmetric form, $\mathbf r^{\mathsf T}=\mathbf c^{\mathsf T}-\mathbf y^{\mathsf T}A$ is precisely the reduced-cost vector, so condition (i) reads simply

$$\mathbf r^{\mathsf T}\mathbf x=0,$$

i.e. **basic variables have zero reduced cost and variables with nonzero reduced cost are nonbasic** — a statement chapter 09 established by direct computation, now recovered as a special case of a general principle.

> [!example]- Worked example — complementary slackness in full (Chong & Żak Example 17.3)
> $$\text{maximize } 2x_1+5x_2+x_3 \quad\text{s.t.}\quad \begin{aligned}2x_1-x_2+7x_3&\le6\\ x_1+3x_2+4x_3&\le9\\ 3x_1+6x_2+x_3&\le3\end{aligned},\quad\mathbf x\ge\mathbf 0$$
>
> The dual (writing it as a minimization in nonnegative variables, which is the readable form) is
> $$\text{minimize } 6y_1+9y_2+3y_3 \quad\text{s.t.}\quad \begin{aligned}2y_1+y_2+3y_3&\ge2\\ -y_1+3y_2+6y_3&\ge5\\ 7y_1+4y_2+y_3&\ge1\end{aligned},\quad\mathbf y\ge\mathbf 0$$
>
> The optimal solutions are
> $$\mathbf x^\star=\left(0,\ \tfrac{15}{43},\ \tfrac{39}{43}\right),\qquad \mathbf y^\star=\left(\tfrac1{43},\ 0,\ \tfrac{36}{43}\right),\qquad z^\star=\tfrac{114}{43}\approx2.6512 .$$
> Both values equal $114/43$ — strong duality, verified.
>
> **Now read every complementary slackness condition off these two vectors.**
>
> | | value | tight? | partner | consistent? |
> |---|---|---|---|---|
> | primal con. 1 | $-\tfrac{15}{43}+\tfrac{273}{43}=6$ | **tight** | $y_1=\tfrac1{43}>0$ | ✅ binding ⟹ priced |
> | primal con. 2 | $\tfrac{45}{43}+\tfrac{156}{43}=\tfrac{201}{43}\approx4.67<9$ | **slack** | $y_2=0$ | ✅ unused ⟹ free |
> | primal con. 3 | $\tfrac{90}{43}+\tfrac{39}{43}=3$ | **tight** | $y_3=\tfrac{36}{43}>0$ | ✅ binding ⟹ priced |
> | dual con. 1 | $\tfrac2{43}+\tfrac{108}{43}=\tfrac{110}{43}\approx2.56>2$ | **slack** | $x_1=0$ | ✅ unprofitable ⟹ unused |
> | dual con. 2 | $-\tfrac1{43}+\tfrac{216}{43}=5$ | **tight** | $x_2=\tfrac{15}{43}>0$ | ✅ |
> | dual con. 3 | $\tfrac7{43}+\tfrac{36}{43}=1$ | **tight** | $x_3=\tfrac{39}{43}>0$ | ✅ |
>
> Every one of the six pairings is exactly as the theorem requires. Note in particular the economic reading of row 4: **product 1 is not made because making it would cost more in consumed resources ($110/43$) than it earns ($2$).** The dual slack $c_j-(A^{\mathsf T}\mathbf y)_j$ *is* the per-unit loss from forcing that product into the plan — which is the reduced cost of chapter 09, arrived at from the other side.

### 8. Reading the dual off the final tableau

Since $\mathbf y^{\mathsf T}=\mathbf c_B^{\mathsf T}B^{-1}$, the dual solution is already sitting in the final tableau. The clean case is the common one.

**If the original matrix contains an $m\times m$ identity** — which it does whenever you converted $\le$ constraints by adding slack variables — then the final tableau's last row, in the columns where that identity started, holds $\mathbf c_I^{\mathsf T}-\mathbf c_B^{\mathsf T}B^{-1}=\mathbf c_I^{\mathsf T}-\mathbf y^{\mathsf T}$. Hence

$$\mathbf y^{\mathsf T}=\mathbf c_I^{\mathsf T}-\mathbf r_I^{\mathsf T},$$

and **for slack variables $\mathbf c_I=\mathbf 0$, so $\mathbf y=-\mathbf r_I$: the dual solution is (minus) the reduced costs of the slacks.** That is chapter 09's shadow-price claim, proved.

In general, if $D$ (the nonbasic block) has rank $m$ you can solve $\mathbf y^{\mathsf T}D=\mathbf c_D^{\mathsf T}-\mathbf r_D^{\mathsf T}$ for $\mathbf y$; if $\operatorname{rank}D<m$, append the always-true equations $\mathbf y^{\mathsf T}B=\mathbf c_B^{\mathsf T}$ to get a determined system.

Luenberger & Ye's small example makes the mechanics concrete. For

$$\text{minimize } -x_1-4x_2-3x_3 \quad\text{s.t.}\quad \begin{aligned}2x_1+2x_2+x_3&\le4\\ x_1+2x_2+2x_3&\le6\end{aligned},\quad\mathbf x\ge\mathbf 0,$$

the simplex method terminates at $\mathbf x^\star=(0,1,2)$ with value $-10$, and the last row under the two original slack columns reads $(1,1)$. The dual is $\max\ 4\lambda_1+6\lambda_2$ subject to $2\lambda_1+\lambda_2\le-1$, $2\lambda_1+2\lambda_2\le-4$, $\lambda_1+2\lambda_2\le-3$, $\boldsymbol\lambda\le\mathbf 0$, and the solution is read off directly as $\boldsymbol\lambda^\star=(-1,-1)$, value $4(-1)+6(-1)=-10$. ✅ Equal.

> [!warning] Sign conventions will bite you
> Chong & Żak derive the dual of a *maximization* primal by first negating the objective into standard form, and end up with a dual variable constrained $\boldsymbol\lambda\le\mathbf 0$ carrying values like $(-\tfrac1{43},0,-\tfrac{36}{43})$ — the negatives of the $\mathbf y^\star$ in the worked example above. **The mathematics is identical; only the sign convention differs.** Whenever a printed dual solution has a sign you did not expect, check the primal's direction and the book's convention before concluding anything is wrong. Throughout this chapter, dual variables are written so that **they are nonnegative and read as prices**, because that is the only convention with an economic meaning.

### 9. Shadow prices: what the dual variables *mean*

This is the payoff, and it is why $\mathbf y$ is called a price vector.

Let the primal be $\min\ \mathbf c^{\mathsf T}\mathbf x$ s.t. $A\mathbf x=\mathbf b,\mathbf x\ge\mathbf 0$ with optimal basis $B$, so $\mathbf x_B=B^{-1}\mathbf b$ and $\mathbf y^{\mathsf T}=\mathbf c_B^{\mathsf T}B^{-1}$. Perturb the right-hand side to $\mathbf b+\Delta\mathbf b$. **Assuming the same basis stays optimal** — which it does for small enough $\Delta\mathbf b$, provided the solution is nondegenerate — the new solution is $\mathbf x_B+\Delta\mathbf x_B$ with $\Delta\mathbf x_B=B^{-1}\Delta\mathbf b$, and the change in optimal cost is

$$\Delta z=\mathbf c_B^{\mathsf T}\Delta\mathbf x_B=\mathbf c_B^{\mathsf T}B^{-1}\Delta\mathbf b=\boxed{\ \mathbf y^{\mathsf T}\Delta\mathbf b\ }$$

**So $y_i=\partial z^\star/\partial b_i$: the dual variable is the marginal value of the $i$th resource.** In the diet problem it is the most a dietitian would pay for one more unit of nutrient $i$; in a production problem it is the marginal price of output $i$; in Wyndor it says that one more hour in plant 2 is worth exactly $1.5$ units of profit. Complementary slackness now reads as pure economics: **a resource you have not exhausted has marginal value zero**, and **an activity is run only if its revenue exactly covers the imputed cost of the resources it consumes.**

The same quantity has a second reading. At *any* basis — optimal or not — the vector $\mathbf y^{\mathsf T}=\mathbf c_B^{\mathsf T}B^{-1}$ is called the vector of **simplex multipliers**, and $y_j$ is the cost of synthesising the unit vector $\mathbf e_j$ out of the current basis. Pricing out a column $\mathbf a_j$ means computing its *synthetic* cost $\mathbf y^{\mathsf T}\mathbf a_j$ and comparing with its true cost $c_j$; the difference is the reduced cost. Optimality is then the statement that **every column is cheaper to build from the basis than to buy outright**: $\mathbf y^{\mathsf T}\mathbf a_j\le c_j$ for all $j$, i.e. $\mathbf y^{\mathsf T}A\le\mathbf c^{\mathsf T}$ — dual feasibility again.

> [!warning] Two conditions, both easy to forget
> **(a) "Small enough" is a real restriction.** $z^\star(\mathbf b)$ is convex and *piecewise* linear in $\mathbf b$; $\mathbf y^{\mathsf T}\Delta\mathbf b$ is exact only within the current linear piece. Push $\Delta\mathbf b$ past a breakpoint and the basis changes, $\mathbf y$ jumps, and the prediction fails. **Exercise 4 constructs a case where it fails for $\Delta b_2=1$ but is exact for $\Delta b_2=\tfrac13$**, and locates the breakpoint precisely.
> **(b) Degeneracy destroys the derivative.** At a degenerate optimum the dual optimum is not unique, $z^\star$ has a kink, and the left and right derivatives with respect to $b_i$ differ. Then $y_i$ is only *a* subgradient — one of several defensible "prices" — and asking for "the" shadow price is asking a question with no single answer. Any solver will report one of them without warning you. This is the practical reason degeneracy matters, beyond the cycling worry of chapter 09.

### 10. Duality as a theory of certificates — Farkas' lemma

*(This section goes beyond all four source books' treatment; the connection to ML at the end is entirely my own addition.)*

Strong duality has a purely logical consequence that turns out to be its deepest form. Consider the question: **does the system $A\mathbf x=\mathbf b,\ \mathbf x\ge\mathbf 0$ have a solution?** If yes, the solution itself is the proof. If no, what is the proof?

**Farkas' Lemma.** *Exactly one of the following holds:*
1. *there exists $\mathbf x\ge\mathbf 0$ with $A\mathbf x=\mathbf b$;*
2. *there exists $\mathbf y$ with $\mathbf y^{\mathsf T}A\le\mathbf 0^{\mathsf T}$ and $\mathbf y^{\mathsf T}\mathbf b>0$.*

The two cannot both hold — if they did, $0<\mathbf y^{\mathsf T}\mathbf b=\mathbf y^{\mathsf T}A\mathbf x\le0$, absurd. That exactly one holds is strong duality applied to the LP $\min\ \mathbf 0^{\mathsf T}\mathbf x$ subject to $A\mathbf x=\mathbf b,\mathbf x\ge\mathbf 0$: the objective is identically zero, so the primal value is $0$ if feasible and $+\infty$ if not, and the dual $\max\ \mathbf y^{\mathsf T}\mathbf b$ s.t. $\mathbf y^{\mathsf T}A\le\mathbf 0$ is correspondingly $0$ or unbounded — and unbounded means some $\mathbf y$ achieves a positive value.

**Statements of this shape are called *theorems of the alternative*, and they are what "certificate" really means.** Infeasibility, which looks like the absence of an object, becomes the presence of a different object — one short vector that anyone can check. Geometrically, condition 2 is a hyperplane through the origin with $\mathbf b$ strictly on one side and the whole cone $\{A\mathbf x:\mathbf x\ge\mathbf 0\}$ on the other, which is the separating hyperplane from Proof 2 of §5 wearing different clothes.

**Where duality goes from here:**

- **[[11 - Constrained Optimization - Lagrange and KKT|Ch. 11]] generalises §1 to nonlinear constraints.** The bounding trick becomes the **Lagrangian** $L(\mathbf x,\boldsymbol\lambda)=f(\mathbf x)+\boldsymbol\lambda^{\mathsf T}\mathbf g(\mathbf x)$; the dual function is $q(\boldsymbol\lambda)=\inf_{\mathbf x}L$, weak duality is $q(\boldsymbol\lambda)\le f^\star$ and holds *always*, for any problem whatsoever, convex or not. The **KKT conditions** are then exactly primal feasibility + dual feasibility + complementary slackness + stationarity — the four things this chapter has been assembling. **Everything in §4 and §7 survives verbatim; only §5 needs a hypothesis.**
- **[[12 - Convex Programming and Constrained Algorithms|Ch. 12]] supplies that hypothesis.** For general nonlinear programs the gap $f^\star-q^\star$ can be strictly positive (a **duality gap**). Convexity plus a constraint qualification (Slater's condition) closes it. LP is the case where convexity is automatic and no qualification is needed — which is why this chapter's theorems are unusually clean.
- **In machine learning, the dual is where the algorithm lives.** The soft-margin SVM's primal has one variable per *feature*; its dual has one per *training example*, with $\alpha_i>0$ exactly for the **support vectors** — complementary slackness, §7, is the definition of "support vector". More importantly, the dual objective involves the data only through inner products $\mathbf x_i^{\mathsf T}\mathbf x_j$, which is precisely what makes the **kernel trick** possible: replace the inner product with $k(\mathbf x_i,\mathbf x_j)$ and you have fitted a classifier in an infinite-dimensional feature space you never constructed. **That entire technique is an artefact of choosing to solve the dual.** Duality also underlies the equivalence of LASSO's penalty and constraint forms ([[08 - Least Squares and Linear Equations|ch. 08]] §7), and every "primal-dual" first-order method (ADMM, Chambolle–Pock) used in large-scale ML.

## ✏️ Exercises

**1. (Mechanical — the recipe.)** Write the dual of

$$\begin{aligned}\text{minimize }\quad & 3x_1+2x_2-x_3+4x_4\\ \text{subject to }\quad & x_1+x_2+x_3+x_4\ \ge\ 6\\ & 2x_1-x_2+3x_3\ \le\ 4\\ & x_1+4x_3-x_4\ =\ 2\\ & x_1\ge0,\ \ x_2\ge0,\ \ x_3\ \text{free},\ \ x_4\le0.\end{aligned}$$

State how many variables and how many constraints the dual has, and give the sign restriction on each dual variable and the sense of each dual constraint.

> [!example]- Solution
> The primal is a **minimization**, so read the recipe table left-to-right. There are 3 constraints ⟹ **3 dual variables** $y_1,y_2,y_3$; there are 4 variables ⟹ **4 dual constraints**.
>
> Signs on the dual variables, from the constraint senses: $\ge\Rightarrow y_1\ge0$; $\le\Rightarrow y_2\le0$; $=\Rightarrow y_3$ **free**.
>
> Senses of the dual constraints, from the variable restrictions: $x_1\ge0\Rightarrow\le c_1$; $x_2\ge0\Rightarrow\le c_2$; $x_3$ free $\Rightarrow\ =c_3$; $x_4\le0\Rightarrow\ \ge c_4$.
>
> The columns of $A$ are $\mathbf a_1=(1,2,1)$, $\mathbf a_2=(1,-1,0)$, $\mathbf a_3=(1,3,4)$, $\mathbf a_4=(1,0,-1)$, so:
>
> $$\begin{aligned}\text{maximize }\quad & 6y_1+4y_2+2y_3\\ \text{subject to }\quad & y_1+2y_2+y_3\ \le\ 3 && (x_1\ge0)\\ & y_1-y_2\ \le\ 2 && (x_2\ge0)\\ & y_1+3y_2+4y_3\ =\ -1 && (x_3\text{ free})\\ & y_1-y_3\ \ge\ 4 && (x_4\le0)\\ & y_1\ge0,\ \ y_2\le0,\ \ y_3\ \text{free}.\end{aligned}$$
>
> **Check it by dualising again** — the fastest way to catch a sign slip. Applying the table right-to-left to this maximization must reproduce the original problem exactly. It does.
>
> If you prefer not to trust the table: substitute $x_3=x_3^+-x_3^-$ and $x_4=-x_4'$ with all of $x_3^\pm,x_4'\ge0$, negate the second constraint to make it $\ge$, split the third into two $\ge$ inequalities, apply the symmetric form, and recombine. Same answer, more paper.

**2. (Weak duality as a bound.)** Return to the problem of [[09 - Linear Programming and the Simplex Method|ch. 09]]:

$$\text{maximize } 2x_1+3x_2 \quad\text{s.t.}\quad x_1+x_2\le4,\ \ x_1+3x_2\le6,\ \ \mathbf x\ge\mathbf 0.$$

(a) Write the dual as a minimization in nonnegative variables. (b) Verify that $\mathbf y=(3,0)$, $(2,1)$ and $(0,2)$ are all dual-feasible, and state the upper bound each certifies. (c) The primal optimum is $\mathbf x^\star=(3,1)$ with $z^\star=9$. Find a dual-feasible $\mathbf y$ certifying the bound $9$, and explain what its existence proves.

> [!example]- Solution
> **(a)** Two constraints ⟹ two dual variables; the primal is a max with $\le$ constraints and $\mathbf x\ge\mathbf 0$, so the dual is a min with $\ge$ constraints and $\mathbf y\ge\mathbf 0$:
> $$\text{minimize } 4y_1+6y_2 \quad\text{s.t.}\quad y_1+y_2\ge2,\ \ y_1+3y_2\ge3,\ \ \mathbf y\ge\mathbf 0.$$
>
> **(b)** Check $A^{\mathsf T}\mathbf y\ge\mathbf c$ for each:
>
> | $\mathbf y$ | $y_1+y_2\ge2$ | $y_1+3y_2\ge3$ | feasible | bound $4y_1+6y_2$ |
> |---|---|---|---|---|
> | $(3,0)$ | $3\ge2$ ✓ | $3\ge3$ ✓ | ✅ | $12$ |
> | $(2,1)$ | $3\ge2$ ✓ | $5\ge3$ ✓ | ✅ | $14$ |
> | $(0,2)$ | $2\ge2$ ✓ | $6\ge3$ ✓ | ✅ | $12$ |
>
> Every one certifies $z^\star\le$ its value. Note $(2,1)$ gives the **worst** bound of the three: dual-feasible points are not equally informative, and the dual problem is precisely the search for the best one.
>
> **(c)** $\mathbf y^\star=\left(\tfrac32,\tfrac12\right)$. Feasibility: $\tfrac32+\tfrac12=2\ge2$ ✓ (tight), $\tfrac32+\tfrac32=3\ge3$ ✓ (tight). Value: $4\cdot\tfrac32+6\cdot\tfrac12=6+3=9$. ✅
>
> Its existence, together with the primal-feasible $\mathbf x^\star=(3,1)$ of the same value, **proves $\mathbf x^\star$ is optimal** — by §4, with no reference to the simplex method, no basis, and no need to trust any algorithm. Two vectors and four arithmetic checks settle a question about infinitely many feasible points.
>
> Both dual constraints are tight because both $x_1^\star,x_2^\star>0$ (complementary slackness), and $\mathbf y^\star=(1.5,0.5)$ is exactly the pair of reduced costs on the slack variables that chapter 09's final tableau produced. **This is the loose end, tied.**

**3. (Complementary slackness as a solution method.)** Consider

$$\text{minimize } 5x_1+6x_2+9x_3+8x_4 \quad\text{s.t.}\quad \begin{aligned}x_1+2x_2+3x_3+x_4&\ge5\\ x_1+x_2+2x_3+3x_4&\ge3\end{aligned},\quad\mathbf x\ge\mathbf 0.$$

You are told the dual optimum is $\mathbf y^\star=(3,0)$. **Without solving the primal**, use complementary slackness to determine $\mathbf x^\star$ and the optimal value.

> [!example]- Solution
> The dual is $\max\ 5y_1+3y_2$ s.t. $A^{\mathsf T}\mathbf y\le\mathbf c$, $\mathbf y\ge\mathbf 0$. First confirm $\mathbf y^\star=(3,0)$ is dual-feasible and compute the **dual slacks** $s_j=c_j-(A^{\mathsf T}\mathbf y^\star)_j$:
>
> | $j$ | $\mathbf a_j$ (column) | $(A^{\mathsf T}\mathbf y^\star)_j=3a_{1j}$ | $c_j$ | slack $s_j$ | conclusion |
> |---|---|---|---|---|---|
> | 1 | $(1,1)$ | $3$ | $5$ | $2>0$ | $x_1=0$ |
> | 2 | $(2,1)$ | $6$ | $6$ | $0$ | $x_2$ may be $>0$ |
> | 3 | $(3,2)$ | $9$ | $9$ | $0$ | $x_3$ may be $>0$ |
> | 4 | $(1,3)$ | $3$ | $8$ | $5>0$ | $x_4=0$ |
>
> All slacks $\ge0$, so $\mathbf y^\star$ is dual-feasible, with value $5(3)+3(0)=15$.
>
> **Step 1 — kill variables.** $s_1,s_4>0$ force $x_1=x_4=0$ by condition (i).
>
> **Step 2 — force constraints tight.** $y_1=3>0$ forces constraint 1 to be binding by condition (ii). ($y_2=0$ forces nothing — condition (ii) is satisfied whatever constraint 2 does. **Do not assume constraint 2 is slack.**)
>
> **Step 3 — solve what is left.** With $x_1=x_4=0$, constraint 1 tight gives $2x_2+3x_3=5$. That is one equation in two unknowns, so try the natural guess that constraint 2 is tight as well: $x_2+2x_3=3$. Then $x_2=3-2x_3$ and $2(3-2x_3)+3x_3=5\Rightarrow6-x_3=5\Rightarrow x_3=1$, $x_2=1$.
>
> **Step 4 — verify.** $\mathbf x^\star=(0,1,1,0)\ge\mathbf 0$ ✓. Constraint 1: $2+3=5\ge5$ ✓. Constraint 2: $1+2=3\ge3$ ✓. Objective: $6(1)+9(1)=\mathbf{15}$ — **equal to the dual value 15, so by §4 both are optimal.** ✅
>
> Note how little work this was: complementary slackness reduced a 4-variable LP to a $2\times2$ linear system. **This is the practical use of duality by hand** — and it is the same logic that turns the KKT conditions into a solution method in [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]].
>
> One honest wrinkle: constraint 2 came out **tight even though its price is zero**. Complementary slackness permits this ($y_2\cdot0=0$), but it is a warning sign — see Exercise 4.

**4. (Shadow prices, and where they stop working.)** Continue with the problem and solution of Exercise 3: $\mathbf x^\star=(0,1,1,0)$, $\mathbf y^\star=(3,0)$, $z^\star=15$.

(a) Predict the new optimal value when $\mathbf b=(5,3)$ becomes $(6,3)$, and check by re-solving.
(b) Predict it for $\mathbf b\to(5,4)$, and check. **The prediction fails. Explain why**, and find the exact largest $\Delta b_2$ for which the shadow price $y_2=0$ is still valid.

> [!example]- Solution
> **(a)** $\Delta\mathbf b=(1,0)$, so $\Delta z=\mathbf y^{\star\mathsf T}\Delta\mathbf b=3(1)+0(0)=3$, predicting $z^\star=18$. Re-solving with $\mathbf b=(6,3)$ gives exactly $\mathbf{18}$. ✅ (And $\Delta\mathbf b=(0.5,0)$ predicts $16.5$ — also exact.)
>
> **(b)** $\Delta\mathbf b=(0,1)$ predicts $\Delta z=0$, i.e. $z^\star=15$. Re-solving with $\mathbf b=(5,4)$ gives
> $$z^\star=\tfrac{115}{7}\approx16.4286,\qquad \Delta z=\tfrac{115}{7}-15=\tfrac{10}{7}\approx1.4286\ \ne\ 0 .$$
> **The prediction is wrong**, and not by a rounding error.
>
> **Why.** $z^\star(\mathbf b)=\max\{\mathbf b^{\mathsf T}\mathbf y:\mathbf y\text{ dual-feasible}\}$ is a maximum of finitely many linear functions of $\mathbf b$ — one per dual vertex — hence **convex and piecewise linear**. Enumerating the dual vertices of this problem:
>
> | dual vertex $\mathbf y$ | $\mathbf b^{\mathsf T}\mathbf y$ at $\mathbf b=(5,3)$ |
> |---|---|
> | $(0,0)$ | $0$ |
> | $(0,\tfrac83)$ | $8$ |
> | $\left(\tfrac{11}7,\tfrac{15}7\right)$ | $\tfrac{100}7\approx14.29$ |
> | $\mathbf(3,0)$ | $\mathbf{15}$ ← argmax |
>
> At $\mathbf b=(5,3)$ the winner is $(3,0)$, but only by $\tfrac{15}{1}-\tfrac{100}{7}=\tfrac57$. Moving $\mathbf b$ changes the two objective values at different rates, and the runner-up overtakes as soon as the margin is exhausted. Writing $\Delta b_2=t$, the margin is
> $$\underbrace{\tfrac57}_{\text{initial}}+t\left(0-\tfrac{15}{7}\right)=\tfrac57-\tfrac{15t}{7},$$
> which vanishes at $t=\tfrac13$. **So $y_2=0$ is valid exactly for $\Delta b_2\le\tfrac13$**, and the test value $\Delta b_2=1$ was three times too large. Verified: at $\mathbf b=(5,\tfrac{10}3)$ both vertices give exactly $15$ — a tie, the breakpoint. The same computation in the $b_1$ direction gives margin $\tfrac57+\tfrac{10t}7$, valid for $\Delta b_1\ge-\tfrac12$; and indeed re-solving at $\mathbf b=(4,3)$ gives $\tfrac{89}7\approx12.71$, **not** the predicted $12$.
>
> **The deeper reason this problem is fragile.** At $\mathbf y^\star=(3,0)$ **three** dual constraints are active in $\mathbb R^2$ — dual constraints 2 and 3, plus the bound $y_2\ge0$. A vertex in $\mathbb R^2$ needs only two, so $\mathbf y^\star$ is a **degenerate** vertex, and this is exactly the situation flagged in §9(b): the tight-but-unpriced constraint 2 discovered in Exercise 3 is the same phenomenon seen from the primal side. Degeneracy is what makes the range of validity asymmetric and small. **A solver would report $\mathbf y^\star=(3,0)$ with no warning, and reporting "the marginal value of resource 2 is zero" to a client would be seriously misleading** — its right-hand marginal value is $\tfrac{10}7$.
>
> **Moral: a shadow price is a derivative, and derivatives are local. Always compute the range of validity before quoting one.**

**5. (Hard — Farkas' lemma and infeasibility certificates.)** (a) Prove Farkas' lemma from strong duality. (b) Decide whether there exists $\mathbf x\ge\mathbf 0$ with
$$x_1+x_2+x_3=1,\qquad x_1+2x_2+3x_3=5,$$
and produce either a solution or a certificate. (c) Explain how you could have *guessed* the certificate from an optimization problem.

> [!example]- Solution
> **(a)** The two alternatives are mutually exclusive: if both held, then $0<\mathbf y^{\mathsf T}\mathbf b=\mathbf y^{\mathsf T}(A\mathbf x)=(\mathbf y^{\mathsf T}A)\mathbf x\le0$, since $\mathbf y^{\mathsf T}A\le\mathbf 0^{\mathsf T}$ and $\mathbf x\ge\mathbf 0$ — a contradiction. So **at most one** holds.
>
> For **at least one**, apply strong duality to the LP with a zero objective:
> $$\text{(P)}\quad \min\ \mathbf 0^{\mathsf T}\mathbf x\ \text{ s.t. }\ A\mathbf x=\mathbf b,\ \mathbf x\ge\mathbf 0, \qquad\qquad \text{(D)}\quad \max\ \mathbf y^{\mathsf T}\mathbf b\ \text{ s.t. }\ \mathbf y^{\mathsf T}A\le\mathbf 0^{\mathsf T}.$$
> (D) is always **feasible** — take $\mathbf y=\mathbf 0$, giving value $0$ — so by §6 it is either optimal with a finite value or unbounded, and (P) is never unbounded (its objective is constant).
>
> - If alternative 1 fails, (P) is infeasible. By the four-state table, an infeasible primal with a feasible dual forces (D) to be **unbounded above**. So some feasible $\mathbf y$ has $\mathbf y^{\mathsf T}\mathbf b>0$ — that is alternative 2. ✓
> - If alternative 1 holds, (P) is feasible with optimal value $0$, so by strong duality (D) has optimal value $0$, i.e. **no** feasible $\mathbf y$ achieves a positive value — alternative 2 fails. ✓
>
> Exactly one holds. $\blacksquare$ *(Note the cone structure: if any feasible $\mathbf y$ has $\mathbf y^{\mathsf T}\mathbf b>0$ then $\alpha\mathbf y$ is feasible for all $\alpha>0$, so "positive value" and "unbounded" coincide here — which is why the argument closes.)*
>
> **(b)** No such $\mathbf x$ exists. **Certificate: $\mathbf y=(-3,1)$.**
> $$\mathbf y^{\mathsf T}A=\big(-3+1,\ -3+2,\ -3+3\big)=(-2,-1,0)\ \le\ \mathbf 0^{\mathsf T}\ \checkmark,\qquad \mathbf y^{\mathsf T}\mathbf b=-3(1)+1(5)=2\ >\ 0\ \checkmark.$$
> Both conditions of alternative 2 hold, so by the lemma alternative 1 is impossible. **Four multiplications and two additions settle it** — no solver, no Phase I, no trust required. (Confirmed independently: `linprog` reports status 2, infeasible.)
>
> Concretely, the certificate says: multiply equation 1 by $-3$, add equation 2, and any solution would have to satisfy $-2x_1-x_2+0\cdot x_3=2$ — impossible for $\mathbf x\ge\mathbf 0$, since the left side is $\le0$. **The certificate is a recipe for the contradiction.**
>
> **(c)** The first equation says $\mathbf x$ lies on the unit simplex, so the second equation asks for the value $5$ from the quantity $x_1+2x_2+3x_3$. But
> $$\max\{x_1+2x_2+3x_3\ :\ x_1+x_2+x_3=1,\ \mathbf x\ge\mathbf 0\}=3,$$
> attained at $\mathbf x=(0,0,1)$ — the maximum of a linear function over a simplex is the largest coefficient. Since $5>3$, the system is infeasible.
>
> **And that optimization problem hands you the certificate.** Its optimal value $3$ is the multiplier on the first equation, up to sign: take $\mathbf y=(-3,1)$, and $\mathbf y^{\mathsf T}A\le\mathbf 0$ is exactly the statement "$3\cdot(\text{coefficient in eq. 1})\ge(\text{coefficient in eq. 2})$ for every column," i.e. that $3$ is a valid upper bound; while $\mathbf y^{\mathsf T}\mathbf b=5-3>0$ is exactly the statement that the demanded value exceeds it. **The dual optimal solution of the bounding problem *is* the infeasibility certificate of the original system** — which is the whole content of Farkas' lemma, and the reason §10 calls duality a theory of certificates.

## 📝 Summary

- **The dual is derived, not defined.** It is the problem of finding the best lower bound on the primal obtainable by taking a nonnegative combination of the primal constraints. Everything else follows.
- **Symmetric form:** $\min\{\mathbf c^{\mathsf T}\mathbf x:A\mathbf x\ge\mathbf b,\mathbf x\ge\mathbf 0\}$ pairs with $\max\{\mathbf y^{\mathsf T}\mathbf b:\mathbf y^{\mathsf T}A\le\mathbf c^{\mathsf T},\mathbf y\ge\mathbf 0\}$. **Asymmetric form:** equality constraints ($A\mathbf x=\mathbf b$) give a **free** dual variable. **The dual of the dual is the primal**, so the labels are arbitrary. One dual variable per primal constraint, one dual constraint per primal variable.
- **Weak duality** ($\mathbf c^{\mathsf T}\mathbf x\ge\mathbf y^{\mathsf T}\mathbf b$ for any feasible pair) is a two-line proof and gives: max $\le$ min; bracketing bounds; unbounded-one ⟹ infeasible-other; and **matching values prove optimality** — a *verifiable global certificate*, unlike "the algorithm stopped."
- **Strong duality:** if either problem has a finite optimum, so does the other and **the values are equal — no gap, ever, for an LP.** Proved constructively via $\mathbf y^{\mathsf T}=\mathbf c_B^{\mathsf T}B^{-1}$ at an optimal basis, or in full generality via a separating hyperplane.
- **The simplex method solves both problems at once.** $\mathbf y^{\mathsf T}=\mathbf c_B^{\mathsf T}B^{-1}$ is computed at every iteration to price columns; at optimality it *is* the dual solution. With slack variables, **$\mathbf y=-\mathbf r_I$: the dual solution is minus the reduced costs of the slacks.**
- **Four states, and both problems can be infeasible** (Chong & Żak Ex. 17.7). Infeasibility of one does *not* imply unboundedness of the other.
- **Complementary slackness:** $x_j>0\Rightarrow$ dual constraint $j$ tight; dual constraint slack $\Rightarrow x_j=0$; $y_i>0\Rightarrow$ constraint $i$ binding; constraint $i$ non-binding $\Rightarrow y_i=0$. Equivalently $\mathbf r^{\mathsf T}\mathbf x=0$. **You do not pay for a resource you have not used up.** It reduces solving one problem to solving a small linear system given the other's solution.
- **$y_i=\partial z^\star/\partial b_i$ is the shadow price** — the marginal value of resource $i$, exact via $\Delta z=\mathbf y^{\mathsf T}\Delta\mathbf b$ **only within the current linear piece of the piecewise-linear $z^\star(\mathbf b)$**, and only a subgradient at all under degeneracy.
- **Farkas' lemma** turns duality into a theory of certificates: exactly one of $\{\exists\mathbf x\ge\mathbf 0:A\mathbf x=\mathbf b\}$ and $\{\exists\mathbf y:\mathbf y^{\mathsf T}A\le\mathbf 0,\mathbf y^{\mathsf T}\mathbf b>0\}$ holds. **Infeasibility, the absence of an object, is certified by the presence of a different one.**

## ⚠️ Important Notes

1. **Count before you compute.** The dual of an $m\times n$ problem is $n\times m$. If your dual has the wrong number of variables or constraints, you have made a structural error and no amount of sign-checking will save it. Check this first, always.
2. **Derive the recipe table; do not memorise it.** Convert to symmetric form, apply the one rule you remember, simplify. Memorised sign conventions fail under pressure, and the four sign rules are individually 50/50 guesses.
3. **Verify a dual by dualising it again.** The dual of the dual must be the original problem, character for character. This catches essentially every sign and sense error, costs thirty seconds, and is the single most useful habit in this chapter.
4. **A sign you did not expect is usually a convention, not an error.** Chong & Żak's Example 17.3 dual solution is $(-\tfrac1{43},0,-\tfrac{36}{43})$ where this chapter writes $(\tfrac1{43},0,\tfrac{36}{43})$ — same mathematics, different starting form (they negate a max into a min first). Before declaring a printed answer wrong, reconstruct its convention.
5. **Weak duality is the direction you can rely on unconditionally.** It needs no assumptions at all, and it survives into nonlinear and non-convex problems ([[11 - Constrained Optimization - Lagrange and KKT|ch. 11]]). **Strong duality is the special one** — it is an LP luxury, and for general nonlinear programs it can genuinely fail. Never quote "the primal and dual values are equal" for a non-convex problem.
6. **"Infeasible" and "unbounded" are not duals of each other.** Primal unbounded ⟹ dual infeasible, yes. But primal infeasible ⟹ dual infeasible *or* dual unbounded, and both really occur. This is why solvers report the two statuses separately and why an "infeasible or unbounded" message from a solver is a genuine ambiguity, not laziness.
7. **Complementary slackness gives implications, not equivalences — watch the direction.** $y_i>0\Rightarrow$ constraint $i$ tight is valid. The converse is **not**: a constraint can be tight with $y_i=0$ (Exercise 3, constraint 2). Likewise $x_j=0$ does not force the dual constraint to be slack. Assuming the converses is the most common error in solving problems this way.
8. **Zero shadow price on a binding constraint is a degeneracy alarm.** It means complementary slackness is satisfied vacuously and cannot pin the price down. Expect a kink in $z^\star(\mathbf b)$, differing one-sided marginal values, and a non-unique dual optimum — Exercise 4 makes all three concrete.
9. **Always compute the range of validity before quoting a shadow price.** $\Delta z=\mathbf y^{\mathsf T}\Delta\mathbf b$ is exact within one linear piece of $z^\star(\mathbf b)$ and can be badly wrong outside it. In Exercise 4 the price $y_2=0$ is valid for $\Delta b_2\le\tfrac13$ and useless at $\Delta b_2=1$, where the true change is $\tfrac{10}7$.
10. **The shadow price is a *marginal* value, not a total one.** $y_i=1.5$ means the next unit is worth $1.5$, not that the resource is worth $1.5$ per unit throughout. Selling half your capacity at the shadow price would be a serious mistake.
11. **Solve whichever problem is smaller.** A problem with 5 constraints and 5000 variables has a dual with 5 variables and 5000 constraints. Since simplex effort scales far worse in the number of *constraints* than of variables, dualising can be a large practical win. This is a standard preprocessing decision, not a curiosity.
12. **The dual solution is free — take it.** Every LP solver returns $\mathbf y^\star$ (often as `.marginals`, `.dual`, or `y`). It costs nothing extra, it certifies the answer, and it carries the entire sensitivity analysis. Ignoring it discards most of what you paid for.
13. **Verify a solver's answer yourself.** Check $A\mathbf x^\star\ \{\ge,=\}\ \mathbf b$, $\mathbf x^\star\ge\mathbf 0$, $A^{\mathsf T}\mathbf y^\star\le\mathbf c$, $\mathbf y^\star\ge\mathbf 0$, and $\mathbf c^{\mathsf T}\mathbf x^\star=\mathbf b^{\mathsf T}\mathbf y^\star$. Four lines of NumPy, no trust required. This is a genuine engineering practice, not an exam exercise.
14. **Complementary slackness is where the KKT conditions come from.** When [[11 - Constrained Optimization - Lagrange and KKT|ch. 11]] presents KKT as four conditions — stationarity, primal feasibility, dual feasibility, complementary slackness — three of the four are already in this chapter. Learning them here, in the linear case where strong duality is unconditional, makes the nonlinear case far easier.
15. **In ML you will meet the dual before you meet duality.** The SVM's $\alpha_i$, the "support vectors" (exactly the $i$ with $\alpha_i>0$ — complementary slackness), the kernel trick's dependence on inner products, and LASSO's penalty/constraint equivalence are all consequences of this chapter. If you only remember one application, remember that **the kernel trick works because someone chose to solve the dual.**

> [!warning] Gaps in the source material
> **Extraction damage.** Chong & Żak ch. 17 is scanned; the OCR substitutions listed in `../CLAUDE.md` apply throughout ($\lambda^{\mathsf T}b$ reads as `λ b`, $\in$ as `G`, transposes lost everywhere). **Example 17.3's entire two-phase simplex run — six tableaus over five pages — extracts as bare columns of digits with no row or column structure.** Every number in this chapter's version of that example was therefore recomputed from the problem statement rather than transcribed: `linprog` gives $\mathbf x^\star=(0,\tfrac{15}{43},\tfrac{39}{43})$, $\mathbf y^\star=(\tfrac1{43},0,\tfrac{36}{43})$, $z^\star=\tfrac{114}{43}$, and all six complementary-slackness pairings in §7's table were verified independently. The book's stated answer agrees (under its own sign convention). **The tableau sequence itself is unrecoverable and is not reproduced here** — §8's method for reading $\mathbf y$ off a final tableau is stated in general form and illustrated with Luenberger & Ye's smaller example instead, which does extract.
>
> **Luenberger & Ye §4.3's figures 4.1–4.3 are images and lost.** Fig. 4.1 (the primal and dual value ranges converging on a common point) and Figs. 4.2–4.3 (the requirements-space and activity-space views) *are* the geometric argument in that section. §5 and §9 give the algebra and the verified numbers for the activity-space example ($\mathbf x^\star=(\tfrac12,\tfrac12,0,0)$, $z^\star=15$, $\boldsymbol\lambda^\star=(\tfrac{21}4,\tfrac94)$, with exactly two of four dual constraints active — as the lost figure was meant to show), but **the pictures are not reconstructed.**
>
> **Verification performed.** Every numeric claim in this chapter was recomputed with `scipy.optimize.linprog` and exact `Fraction` arithmetic before being written: C&Ż Examples 17.3 (both problems, all six CS conditions), 17.7 (both infeasible — status 2 each), 17.8 (gold, $\mathbf x^\star=(0,0,26,0)$, value 182, $\lambda=-7$); L&Y §4.3's tableau example ($\mathbf x^\star=(0,1,2)$, $\boldsymbol\lambda^\star=(-1,-1)$, both $-10$) and §4.3's geometric example; and all five exercises. **No error was found in either book's duality chapter** — consistent with the pattern that C&Ż's defects cluster in its numerical-methods chapters (see the errata table in `00-Index.md`).
>
> **Additions beyond all four sources.** §10 is mine: **Farkas' lemma is not stated in Chong & Żak ch. 17** (it appears only obliquely in Exercises 17.17–17.20, as unproved problems) and the framing of duality as *a theory of certificates* is not in any of the four books. The **Lagrangian preview**, the identification of the four KKT conditions with this chapter's ingredients, and the entire **machine-learning discussion (SVM dual, support vectors as complementary slackness, the kernel trick, LASSO, primal-dual first-order methods)** are additions — none of the four books mentions any of it, and Léonard & Long, which might have covered the economics, has **no extractable text at all**. Exercise 4's degeneracy analysis, including the dual-vertex enumeration and the exact breakpoints $\Delta b_2=\tfrac13$ and $\Delta b_1=-\tfrac12$, is also my own construction: **both books state the sensitivity formula $\Delta z=\mathbf y^{\mathsf T}\Delta\mathbf b$ with only a passing "assuming nondegeneracy" and never show it failing**, which badly understates how easily it does.
>
> **Not covered, deliberately.** The **dual simplex method** and the **primal–dual algorithm** (L&Y §§4.5–4.6, C&Ż's forward reference) are omitted — they are computational refinements, and the primal simplex of ch. 09 plus this chapter's theory is the right stopping point for this course. The **max-flow/min-cut theorem** (L&Y §4.5) is omitted as belonging to network optimization, a subject this scope excludes; it is the most attractive omission and is worth reading if graphs interest you. Both omissions are recorded in `00-Index.md`.

**Previous:** [[09 - Linear Programming and the Simplex Method]] · **Next:** [[11 - Constrained Optimization - Lagrange and KKT]]
