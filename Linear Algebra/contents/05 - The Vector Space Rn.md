---
subject: Linear Algebra
chapter: 05
tags: [ds, linear-algebra, subspace, span, independence, basis, dimension, rank, orthogonality, least-squares]
source: "Nicholson, *Linear Algebra with Applications*, 7th ed., ch. 5 (pp. 229–287)"
---

# The Vector Space $\mathbb{R}^n$

> [!abstract] What this chapter is for
> **This is the pivot of the whole book, and the hardest part of the course.** Nicholson calls it a "bridging" chapter: it introduces **subspace, spanning, independence, basis, dimension** in $\mathbb{R}^n$, where you can still compute, before chapter 6 says none of it needed $\mathbb{R}^n$ at all.
>
> **The chapter answers three questions that chapters 1–4 kept raising and could not settle:**
>
> | Question raised | Where | Answered here |
> |---|---|---|
> | Is rank well defined? | [[01 - Systems of Linear Equations\|ch. 01]] Def. 1.4 | **Yes — §5.4 Theorem 1** |
> | What makes eigenvectors "enough"? | [[03 - Determinants and Diagonalization\|ch. 03]] Thm. 4 | **Independence — §5.2, §5.5** |
> | What if $A\mathbf x=\mathbf b$ has no solution? | [[02 - Matrix Algebra\|ch. 02]] Thm. 1 | **Project — §5.6, least squares** |
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Subspaces and spanning | Closed under $+$ and scaling; $\operatorname{span}$, $\operatorname{null}A$, $\operatorname{col}A$ |
> | **2** | **Independence, basis, dimension** | **Every basis of a space has the same size** |
> | **3** | Orthogonality | Orthogonal $\Rightarrow$ independent; **coordinates become dot products** |
> | **4** | **Rank** | $\dim(\operatorname{row}A)=\dim(\operatorname{col}A)=r$ and $\boxed{\operatorname{rank}+\text{nullity}=n}$ |
> | **5** | Similarity and diagonalization | Chapter 3 redone properly |
> | **6** | **Least squares** | When exact solution fails, **project onto the column space** |
>
> **The one theorem to know cold is rank–nullity.** Every "degrees of freedom" argument in statistics, every dimension count in machine learning, and the dimension theorem of [[07 - Linear Transformations|ch. 07]] are that one equation.

---

## 📘 Main Knowledge

### 1. Subspaces and spanning

> [!important] Definition 5.1 — subspace
> $U\subseteq\mathbb{R}^n$ is a **subspace** if
> 1. $\mathbf 0\in U$;
> 2. $\mathbf x,\mathbf y\in U\Rightarrow\mathbf x+\mathbf y\in U$ (**closed under addition**);
> 3. $\mathbf x\in U$, $k$ a scalar $\Rightarrow k\mathbf x\in U$ (**closed under scaling**).

> [!tip] Three tests, and the first one is nearly free
> **Check $\mathbf 0\in U$ first** — it fails immediately for anything defined by a non-homogeneous condition, and it saves you from checking the other two.
>
> **Geometrically, the subspaces of $\mathbb{R}^3$ are exactly: $\{\mathbf 0\}$, lines through the origin, planes through the origin, and $\mathbb{R}^3$.** *Through the origin* is the whole content of condition 1. A line that misses the origin is not a subspace — it is a **translate** of one, which is why [[02 - Matrix Algebra|ch. 02]]'s Theorem 3 wrote solution sets as *particular + homogeneous*.

> [!important] Definition 5.2 and Theorem 1 (§5.1) — span
> $$\operatorname{span}\{\mathbf x_1,\dots,\mathbf x_k\}=\{t_1\mathbf x_1+\cdots+t_k\mathbf x_k\ :\ t_i\in\mathbb{R}\}$$
> **is always a subspace** — indeed the **smallest** subspace containing all the $\mathbf x_i$.

**Three subspaces attached to an $m\times n$ matrix $A$:**

$$\operatorname{null}A=\{\mathbf x\in\mathbb{R}^n:A\mathbf x=\mathbf 0\}\subseteq\mathbb{R}^n$$
$$\operatorname{im}A=\{A\mathbf x:\mathbf x\in\mathbb{R}^n\}=\operatorname{col}A\subseteq\mathbb{R}^m$$
$$\operatorname{row}A=\operatorname{span}\{\text{rows of }A\}\subseteq\mathbb{R}^n$$

> [!important] $\operatorname{im}A=\operatorname{col}A$, and why that matters
> **$A\mathbf x$ is a linear combination of the columns** ([[02 - Matrix Algebra|ch. 02]], Definition 2.5), so the set of *all* outputs is exactly the span of the columns.
>
> **Hence the two big questions about $A\mathbf x=\mathbf b$ become geometry:**
> | Question | Subspace answer |
> |---|---|
> | Is there a solution? | Is $\mathbf b\in\operatorname{col}A$? |
> | Is it unique? | Is $\operatorname{null}A=\{\mathbf 0\}$? |
>
> **And $\operatorname{null}A$ being a subspace is [[01 - Systems of Linear Equations|ch. 01]]'s observation that linear combinations of homogeneous solutions are solutions** — the basic solutions were a spanning set for it all along.

---

### 2. Independence, basis, dimension

> [!important] Definition 5.3 — linear independence
> $\{\mathbf x_1,\dots,\mathbf x_k\}$ is **linearly independent** if
> $$t_1\mathbf x_1+\cdots+t_k\mathbf x_k=\mathbf 0\quad\Longrightarrow\quad t_1=\cdots=t_k=0$$
> — **the only way to combine them to zero is the trivial way.** Otherwise the set is **dependent**.

> [!tip] Three equivalent readings
> | Reading | Statement |
> |---|---|
> | **Algebraic** | $A\mathbf x=\mathbf 0$ has only the trivial solution, where $A=[\mathbf x_1\ \cdots\ \mathbf x_k]$ |
> | **Structural** | **no vector is a combination of the others** — nothing is redundant |
> | **Uniqueness** | every vector in the span is a combination in **exactly one** way |
>
> **The third is the most useful and the least often stated.** If $\mathbf v=\sum s_i\mathbf x_i=\sum t_i\mathbf x_i$ then $\sum(s_i-t_i)\mathbf x_i=\mathbf 0$, so independence forces $s_i=t_i$. **Independence is what makes "coordinates" meaningful.**
>
> **Note also that a nontrivial solution of $A\mathbf x=\mathbf 0$ *is* a dependence relation among the columns** — exactly what [[01 - Systems of Linear Equations|ch. 01]]'s basic solutions computed.

> [!important] Theorem 3 (§5.2) — the square case
> $n$ vectors in $\mathbb{R}^n$ are independent $\iff$ the matrix with them as columns is **invertible** $\iff$ its determinant is nonzero — and then they also **span** $\mathbb{R}^n$.
>
> **This adds two more entries to the Inverse Theorem** ([[02 - Matrix Algebra|ch. 02 §4]]): *the columns are independent*, and *the columns span $\mathbb{R}^n$.*

> [!important] Theorem 4 (§5.2) — the Fundamental Theorem
> If a subspace $U$ is **spanned by $m$ vectors** and contains **$k$ independent vectors**, then
> $$\boxed{k\le m}$$

**This is the engine of the whole section, and it says something intuitive: you cannot fit more independent directions into a space than it takes vectors to describe it.**

> [!important] Definitions 5.4–5.5 and Theorem 5 — basis and dimension
> A **basis** of $U$ is a set that is **independent** *and* **spans** $U$.
>
> **Invariance Theorem: any two bases of $U$ have the same number of vectors.**
> $$\dim U=\text{the number of vectors in any basis}$$

**The proof is two applications of Theorem 4**: if $\{\mathbf x_i\}_{i\le m}$ and $\{\mathbf y_j\}_{j\le k}$ are both bases, then $k\le m$ (the $\mathbf x$'s span, the $\mathbf y$'s are independent) and $m\le k$ by symmetry.

> [!tip] Independent, spanning, basis — too few, too many, just right
> | | Meaning | Failure mode |
> |---|---|---|
> | **Spanning** | enough vectors to reach everything | too few $\Rightarrow$ you miss part of $U$ |
> | **Independent** | no redundancy | too many $\Rightarrow$ some vector is superfluous |
> | **Basis** | both at once | — |
>
> **$\dim U$ is simultaneously the *minimum* size of a spanning set and the *maximum* size of an independent set.** That coincidence is the Invariance Theorem, and it is what makes dimension a number rather than a range.

$\dim(\mathbb{R}^n)=n$ with standard basis $\{\mathbf e_1,\dots,\mathbf e_n\}$, and $\dim\{\mathbf 0\}=0$ (the empty basis).

> [!important] Theorems 6, 7 and 8 (§5.2) — the three labour-savers
> **Theorem 6.** Every subspace $U\ne\{\mathbf 0\}$ has a basis, $\dim U\le n$, and moreover:
> - **any independent set in $U$ can be *enlarged* to a basis**;
> - **any spanning set for $U$ can be *cut down* to a basis.**
>
> **Theorem 7.** If $\dim U=m$ and $B\subseteq U$ has **exactly $m$ vectors**, then
> $$B\text{ is independent}\iff B\text{ spans }U$$
> **— so you need only check one.**
>
> **Theorem 8.** If $U\subseteq W$ then $\dim U\le\dim W$, and **if $\dim U=\dim W$ then $U=W$.**

> [!tip] Theorem 7 halves the work on every "is this a basis?" question
> **Count first.** If the number of vectors equals the dimension, verify *either* independence *or* spanning — whichever is easier — and stop. **Independence is almost always easier**, since it is one homogeneous system rather than a family of consistency checks.
>
> **And Theorem 8 is the standard tool for proving two subspaces are equal:** show one contains the other and that the dimensions match. **Containment plus equal dimension is equality** — no need to exhibit an explicit correspondence.

---

### 3. Orthogonality in $\mathbb{R}^n$

The dot product of [[04 - Vector Geometry|ch. 04]] extends verbatim: $\mathbf x\cdot\mathbf y=\sum x_iy_i=\mathbf x^{\mathsf T}\mathbf y$, $\|\mathbf x\|=\sqrt{\mathbf x\cdot\mathbf x}$.

A set is **orthogonal** if its vectors are pairwise orthogonal and nonzero; **orthonormal** if in addition every vector has length 1.

> [!important] Theorems 4–6 (§5.3)
> **Pythagoras.** For an orthogonal set, $\ \|\mathbf x_1+\cdots+\mathbf x_k\|^2=\|\mathbf x_1\|^2+\cdots+\|\mathbf x_k\|^2$.
>
> **Every orthogonal set is linearly independent.**
>
> **Expansion Theorem.** If $\{\mathbf f_1,\dots,\mathbf f_m\}$ is an **orthogonal basis** of $U$, then every $\mathbf x\in U$ is
> $$\boxed{\ \mathbf x=\frac{\mathbf x\cdot\mathbf f_1}{\|\mathbf f_1\|^2}\mathbf f_1+\frac{\mathbf x\cdot\mathbf f_2}{\|\mathbf f_2\|^2}\mathbf f_2+\cdots+\frac{\mathbf x\cdot\mathbf f_m}{\|\mathbf f_m\|^2}\mathbf f_m\ }$$
> — the **Fourier expansion**, with **Fourier coefficients** $t_i=\dfrac{\mathbf x\cdot\mathbf f_i}{\|\mathbf f_i\|^2}$. **If the basis is orthonormal, $t_i=\mathbf x\cdot\mathbf f_i$.**

> [!tip] Why orthogonal bases are worth the trouble
> **In an ordinary basis, finding coordinates means solving a linear system.** In an orthogonal basis, **each coordinate is one dot product** — and computing it does not require knowing any of the others.
>
> **The proof shows exactly why: dot both sides with $\mathbf f_1$ and every other term dies.** Each basis vector "reads off" its own coefficient and is blind to the rest.
>
> **This is the entire reason chapter 8 builds Gram–Schmidt and QR**, and why the Fourier expansion, PCA scores and wavelet coefficients all have the same shape. **Note also that each term is a projection** $\operatorname{proj}_{\mathbf f_i}\mathbf x$ — the chapter-4 formula, applied once per basis direction.
>
> **And "orthogonal $\Rightarrow$ independent" is a free upgrade:** an orthogonal set of $n$ vectors in $\mathbb{R}^n$ is automatically a basis, with no computation at all.

---

### 4. Rank — the chapter's central theorem

> [!important] Theorem 1 (§5.4)
> For any $m\times n$ matrix $A$ of rank $r$,
> $$\boxed{\ \dim(\operatorname{row}A)=\dim(\operatorname{col}A)=r\ }$$
> and if $A\to R$ (row-echelon) then:
> 1. **the $r$ nonzero rows of $R$ are a basis of $\operatorname{row}A$;**
> 2. **if the leading 1s are in columns $j_1,\dots,j_r$ of $R$, then columns $j_1,\dots,j_r$ *of $A$* are a basis of $\operatorname{col}A$.**

> [!warning] Part 2 says columns **of $A$**, not of $R$ — and this is the most common error in the chapter
> **Row operations preserve the row space but change the column space.**
> $$\begin{bmatrix}1&2\\2&4\end{bmatrix}\longrightarrow\begin{bmatrix}1&2\\0&0\end{bmatrix}$$
> The column space was $\operatorname{span}\{(1,2)\}$ and is now $\operatorname{span}\{(1,0)\}$ — **different subspaces.**
>
> **What *is* preserved is which sets of columns are independent**, because $R=UA$ with $U$ invertible, so $A\mathbf x=\mathbf 0$ and $R\mathbf x=\mathbf 0$ have identical solutions. **So the reduction tells you *which* columns to take; you must then take them from the original matrix.**

> [!important] "Row rank $=$ column rank" is genuinely surprising
> The row space lives in $\mathbb{R}^n$ and the column space in $\mathbb{R}^m$ — **different spaces, possibly of wildly different sizes** — yet they always have the same dimension.
>
> **This is what finally makes [[01 - Systems of Linear Equations|ch. 01]]'s Definition 1.4 legitimate.** The "number of leading 1s" is now identified with a dimension, and dimensions do not depend on how you compute them (the Invariance Theorem). **The debt taken on in chapter 1 is discharged here.**

**Corollaries (§5.4):**

| | Statement |
|---|---|
| **1** | $\operatorname{rank}A=\operatorname{rank}(A^{\mathsf T})$ |
| **2** | $\operatorname{rank}A\le\min(m,n)$ |
| **3** | $\operatorname{rank}A=\operatorname{rank}(UA)=\operatorname{rank}(AV)$ for invertible $U,V$ |
| **4** | $\operatorname{rank}(AB)\le\min(\operatorname{rank}A,\operatorname{rank}B)$ |

> [!important] Theorem 2 (§5.4) — rank–nullity
> For $A$ of size $m\times n$ and rank $r$:
> 1. **the $n-r$ basic solutions of $A\mathbf x=\mathbf 0$ are a basis of $\operatorname{null}A$**, so $\dim(\operatorname{null}A)=n-r$;
> 2. $\dim(\operatorname{im}A)=\dim(\operatorname{col}A)=r$.
>
> $$\boxed{\ \operatorname{rank}A+\dim(\operatorname{null}A)=n\ }$$

> [!tip] Read it as a conservation law
> **$n$ input dimensions go in. $r$ come out as genuine output; the other $n-r$ are crushed to zero.** Nothing is created or lost.
>
> **This is [[01 - Systems of Linear Equations|ch. 01]]'s "$n-r$ parameters" restated as a dimension**, and it becomes the **dimension theorem** $\dim(\ker T)+\dim(\operatorname{im}T)=\dim V$ in [[07 - Linear Transformations|ch. 07]]. **All three are one theorem.**
>
> **Corollary 4 has a useful reading too:** $\operatorname{rank}(AB)\le\min(\operatorname{rank}A,\operatorname{rank}B)$ says **a composition can never recover information either map destroyed** — which is why a network of narrow layers has a hard capacity ceiling, and why $X^{\mathsf T}X$ is singular whenever $X$ has more columns than rows.

---

### 5. Similarity and diagonalization, done properly (§5.5)

$A$ and $B$ are **similar** ($A\sim B$) if $B=P^{-1}AP$ for some invertible $P$.

> [!important] What similarity preserves
> $$\det,\qquad \operatorname{rank},\qquad \operatorname{tr},\qquad c_A(x)\ \text{(hence all eigenvalues, with multiplicities)}$$
> **Similar matrices are the *same transformation* written in different coordinates**, so anything that is really a property of the transformation must be preserved. *(Eigen**vectors** change, of course — they are described in the new coordinates.)*

> [!important] The diagonalization criterion, now sayable
> $$A\ (n\times n)\text{ is diagonalizable}\iff A\text{ has }n\text{ linearly independent eigenvectors}$$
> and, per eigenvalue,
> $$\iff\text{for every }\lambda,\quad \underbrace{\dim(\operatorname{null}(\lambda I-A))}_{\text{geometric multiplicity}}=\underbrace{\text{multiplicity of }\lambda\text{ in }c_A}_{\text{algebraic multiplicity}}$$
> **and always $\text{geometric}\le\text{algebraic}$.**

**Chapter 3 could only say "$P$ is invertible"; now it can say why that is the right condition.** Theorem 6 of §5.5 confirms the count: **eigenvectors from distinct eigenvalues are independent**, so if $A$ has $n$ distinct eigenvalues it is diagonalizable — the sufficient condition of [[03 - Determinants and Diagonalization|ch. 03]], now with a real proof.

---

### 6. Best approximation and least squares (§5.6)

**What if $A\mathbf x=\mathbf b$ has no solution — i.e. $\mathbf b\notin\operatorname{col}A$?** This is the *normal* situation with data: more equations than unknowns, and noise.

> [!important] Theorem 1 (§5.6) — best approximation
> The vector $\mathbf z$ minimising $\|\mathbf b-A\mathbf z\|$ is characterised by
> $$\boxed{\ A^{\mathsf T}A\,\mathbf z=A^{\mathsf T}\mathbf b\ }\qquad\text{(the \textbf{normal equations})}$$
> and if $A^{\mathsf T}A$ is invertible, $\mathbf z=(A^{\mathsf T}A)^{-1}A^{\mathsf T}\mathbf b$ is unique. **$A^{\mathsf T}A$ is invertible $\iff$ the columns of $A$ are independent.**

> [!tip] The geometry is chapter 4's projection, one dimension up
> $A\mathbf z$ ranges over $\operatorname{col}A$, so **we are finding the point of $\operatorname{col}A$ closest to $\mathbf b$ — the orthogonal projection.** The residual $\mathbf b-A\mathbf z$ must be **orthogonal to every column of $A$**, i.e.
> $$A^{\mathsf T}(\mathbf b-A\mathbf z)=\mathbf 0$$
> **which rearranges to the normal equations.** *That is the entire derivation.* **"Project onto the subspace and keep the perpendicular residual" — [[04 - Vector Geometry|ch. 04]]'s method, with $\operatorname{col}A$ in place of a line.**

> [!important] Theorem 2 (§5.6) — the line of best fit
> For data $(x_1,y_1),\dots,(x_n,y_n)$ with at least two distinct $x$'s, set
> $$M=\begin{bmatrix}1&x_1\\ \vdots&\vdots\\ 1&x_n\end{bmatrix},\qquad \mathbf y=\begin{bmatrix}y_1\\ \vdots\\ y_n\end{bmatrix}$$
> The least-squares line $y=z_0+z_1x$ has $\mathbf z=(M^{\mathsf T}M)^{-1}M^{\mathsf T}\mathbf y$.

> [!example] Example 3 (§5.6)
> With $n=5$ points giving $\sum x=21$, $\sum x^2=111$, $\sum y=15$, $\sum xy=78$:
> $$M^{\mathsf T}M=\begin{bmatrix}5&21\\21&111\end{bmatrix},\qquad M^{\mathsf T}\mathbf y=\begin{bmatrix}15\\78\end{bmatrix},\qquad \det=114$$
> $$\mathbf z=\frac1{114}\begin{bmatrix}111&-21\\-21&5\end{bmatrix}\begin{bmatrix}15\\78\end{bmatrix}=\frac1{114}\begin{bmatrix}27\\75\end{bmatrix}=\frac1{38}\begin{bmatrix}9\\25\end{bmatrix}$$
> so $y=0.24+0.66x$. *(Everything verified. **The data table is an image and does not extract**, but the four printed sums are uniquely matched by $(1,1),(3,2),(4,3),(6,4),(7,5)$ — see the gaps callout.)*
>
> **$M^{\mathsf T}M$ is exactly the table of sums $\begin{bmatrix}n&\sum x\\ \sum x&\sum x^2\end{bmatrix}$ and $M^{\mathsf T}\mathbf y=\begin{bmatrix}\sum y\\ \sum xy\end{bmatrix}$** — the formulas from any statistics course, now visibly a matrix product.

**The same theorem fits polynomials:** to fit $y=r_0+r_1x+\cdots+r_mx^m$, use $M$ with columns $1,x,x^2,\dots,x^m$. **The model is non-linear in $x$ but linear in the unknown coefficients**, which is all least squares requires.

---

## ✏️ Exercises

> [!question] Exercise 1 — subspaces *(warm-up)*
> Which of these are subspaces of $\mathbb{R}^3$? Justify.
> (i) $U_1=\{(x,y,z):x+2y-z=0\}$
> (ii) $U_2=\{(x,y,z):x+2y-z=1\}$
> (iii) $U_3=\{(x,y,z):x\ge0\}$
> (iv) $U_4=\{(x,y,z):xy=0\}$
> (v) $U_5=\operatorname{null}A$ and $U_6=\operatorname{col}A$ for $A=\begin{bmatrix}1&2&-1\\2&4&-2\end{bmatrix}$ — and which space does each live in?

> [!example]- Solution
> **(i) Yes.** $\mathbf 0$ satisfies it; if $\mathbf x,\mathbf y$ do then so do $\mathbf x+\mathbf y$ and $k\mathbf x$, because the condition is *homogeneous linear*. **It is a plane through the origin — in fact $\operatorname{null}[1\ 2\ -1]$.**
>
> **(ii) No** — $\mathbf 0$ fails the equation. **A plane not through the origin is a translate of a subspace, not a subspace.**
>
> **(iii) No.** Closed under addition, but not under scaling: $(1,0,0)\in U_3$ while $(-1)(1,0,0)\notin U_3$. **All three conditions are needed** — this set satisfies two of them.
>
> **(iv) No.** $(1,0,0)$ and $(0,1,0)$ are both in $U_4$, but their sum $(1,1,0)$ is not. **A union of two planes is not a subspace** — the failure is closure under addition, and it is the standard example.
>
> **(v)** $\operatorname{null}A\subseteq\mathbb{R}^3$ and $\operatorname{col}A\subseteq\mathbb{R}^2$; **both are subspaces automatically** (Theorem 1 of §5.1). Here $\operatorname{rank}A=1$ (row 2 is twice row 1), so
> $$\dim(\operatorname{null}A)=3-1=2,\qquad \dim(\operatorname{col}A)=1$$
> — **a plane in $\mathbb{R}^3$ and a line in $\mathbb{R}^2$.** *(Note $U_1=\operatorname{null}A$: same plane.)*
>
> > [!tip] The fast test
> > **Check $\mathbf 0$ first.** Then ask whether the defining condition is a *homogeneous linear* equation — if so, you are done, since such conditions are exactly null spaces. **Inequalities, products of variables, and non-zero right-hand sides all fail.**

> [!question] Exercise 2 — independence, basis, dimension
> Let $\mathbf u_1=(1,2,0,1)$, $\mathbf u_2=(2,4,1,3)$, $\mathbf u_3=(1,2,1,2)$ and $U=\operatorname{span}\{\mathbf u_1,\mathbf u_2,\mathbf u_3\}\subseteq\mathbb{R}^4$.
> (i) Are they independent? If not, exhibit a dependence relation.
> (ii) Find a basis of $U$ and $\dim U$.
> (iii) Extend your basis to a basis of $\mathbb{R}^4$.
> (iv) Is $\{(1,2,0,1),(0,0,1,1),(1,0,0,0)\}$ a basis of $U$? Answer with the least possible work.

> [!example]- Solution
> **(i) Not independent.** Row-reducing the matrix with these as rows:
> $$\begin{bmatrix}1&2&0&1\\2&4&1&3\\1&2&1&2\end{bmatrix}\longrightarrow\begin{bmatrix}1&2&0&1\\0&0&1&1\\0&0&0&0\end{bmatrix}$$
> **Rank 2 from three vectors** — a dependence exists. Tracking the operations: $\mathbf u_2-2\mathbf u_1=(0,0,1,1)=\mathbf u_3-\mathbf u_1$, so
> $$\boxed{\mathbf u_1-\mathbf u_2+\mathbf u_3=\mathbf 0}$$
> *(Check: $(1-2+1,\ 2-4+2,\ 0-1+1,\ 1-3+2)=(0,0,0,0)$ ✓.)*
>
> **(ii)** The nonzero rows of the reduced form are a basis of the row space, which is $U$:
> $$\{(1,2,0,1),\ (0,0,1,1)\},\qquad \dim U=2$$
> *(Verified.)* **Here the row-space route is the right one, because $U$ was given as the span of those vectors *as rows*.**
>
> **(iii)** By Theorem 6 we may add standard basis vectors. The leading 1s sit in columns 1 and 3, so **columns 2 and 4 are unconstrained** — add $\mathbf e_2$ and $\mathbf e_4$:
> $$\{(1,2,0,1),\ (0,0,1,1),\ (0,1,0,0),\ (0,0,0,1)\}$$
> This has 4 vectors and is independent (the matrix is triangular after reordering), so **by Theorem 7 it is a basis of $\mathbb{R}^4$ — no spanning check needed.**
>
> **(iv) No, immediately.** $\dim U=2$, and **a basis of $U$ must have exactly 2 vectors** (Invariance Theorem). A set of 3 vectors in a 2-dimensional space is necessarily dependent, by the Fundamental Theorem.
>
> **No arithmetic was required** — and note that $(1,0,0,0)$ is not even *in* $U$, so the set fails twice over. **Counting first is almost always the fastest move in this chapter.**

> [!question] Exercise 3 — rank, the four subspaces, and rank–nullity
> Let $A=\begin{bmatrix}1&2&2&-1\\3&6&5&0\\1&2&1&2\end{bmatrix}$.
> (i) Find $\operatorname{rank}A$ and a basis for $\operatorname{row}A$.
> (ii) Find a basis for $\operatorname{col}A$. **State carefully which matrix your basis vectors come from.**
> (iii) Find a basis for $\operatorname{null}A$ and verify rank–nullity.
> (iv) Is $\mathbf b=(1,2,3)$ in $\operatorname{col}A$? Is $\mathbf b=(1,1,1)$?

> [!example]- Solution
> **(i)** Reducing:
> $$A\longrightarrow\begin{bmatrix}1&2&2&-1\\0&0&1&-3\\0&0&0&0\end{bmatrix}\longrightarrow\begin{bmatrix}1&2&0&5\\0&0&1&-3\\0&0&0&0\end{bmatrix}$$
> $\operatorname{rank}A=2$, and a basis of $\operatorname{row}A$ is $\{(1,2,2,-1),\ (0,0,1,-3)\}$. *(Verified.)*
>
> **(ii)** The leading 1s are in **columns 1 and 3**, so a basis of $\operatorname{col}A$ is columns 1 and 3 **of the original $A$**:
> $$\left\{\begin{bmatrix}1\\3\\1\end{bmatrix},\ \begin{bmatrix}2\\5\\1\end{bmatrix}\right\}$$
> **Taking columns 1 and 3 of the *reduced* matrix would give $\{(1,0,0),(0,1,0)\}$, which spans a different plane in $\mathbb{R}^3$ and is wrong.** The reduction identifies *which* columns; the original supplies *what* they are.
>
> **(iii)** From the reduced form, $x_2=s$ and $x_4=t$ are free, with $x_1=-2s-5t$ and $x_3=3t$:
> $$\operatorname{null}A=\operatorname{span}\left\{(-2,1,0,0),\ (-5,0,3,1)\right\}$$
> *(Both verified: $A$ times each is $\mathbf 0$.)* Then
> $$\operatorname{rank}A+\dim(\operatorname{null}A)=2+2=4=n\ ✓$$
> **Note the four subspaces live in two different spaces:** $\operatorname{row}A$ and $\operatorname{null}A$ in $\mathbb{R}^4$ (dimensions $2+2=4$), $\operatorname{col}A$ in $\mathbb{R}^3$ (dimension 2).
>
> **(iv)** $\operatorname{col}A$ is the plane spanned by $(1,3,1)$ and $(2,5,1)$ in $\mathbb{R}^3$. A normal to it is
> $$(1,3,1)\times(2,5,1)=(3-5,\ 2-1,\ 5-6)=(-2,1,-1)$$
> - $\mathbf b=(1,2,3)$: $(-2)(1)+1(2)+(-1)(3)=-3\ne0$ — **not in $\operatorname{col}A$**, so $A\mathbf x=(1,2,3)$ is inconsistent.
> - $\mathbf b=(1,1,1)$: $-2+1-1=-2\ne0$ — **also not in $\operatorname{col}A$.**
>
> **Since $\operatorname{col}A$ is only 2-dimensional inside $\mathbb{R}^3$, "most" right-hand sides are unreachable** — the system is inconsistent for all $\mathbf b$ off one particular plane. **That is precisely the situation least squares exists to handle** (Exercise 5).

> [!question] Exercise 4 — orthogonal bases
> (i) Show $\{\mathbf f_1,\mathbf f_2,\mathbf f_3\}=\{(1,1,1),(1,-1,0),(1,1,-2)\}$ is an orthogonal basis of $\mathbb{R}^3$ **with only three multiplications' worth of checking.**
> (ii) Expand $\mathbf x=(1,2,3)$ in this basis using the Expansion Theorem.
> (iii) Normalise the basis and re-express the coefficients.
> (iv) Verify Pythagoras' theorem on your expansion.

> [!example]- Solution
> **(i)** Three dot products:
> $$\mathbf f_1\cdot\mathbf f_2=1-1+0=0,\quad \mathbf f_1\cdot\mathbf f_3=1+1-2=0,\quad \mathbf f_2\cdot\mathbf f_3=1-1+0=0$$
> **So the set is orthogonal, hence independent (Theorem 5), and being 3 independent vectors in the 3-dimensional $\mathbb{R}^3$ it is a basis by Theorem 7.** *(Verified.)*
>
> **No determinant, no row reduction — three dot products and two theorems.** This is the labour-saving pattern of the chapter in miniature.
>
> **(ii)** $\|\mathbf f_1\|^2=3$, $\|\mathbf f_2\|^2=2$, $\|\mathbf f_3\|^2=6$:
> $$t_1=\frac{1+2+3}{3}=2,\qquad t_2=\frac{1-2}{2}=-\tfrac12,\qquad t_3=\frac{1+2-6}{6}=-\tfrac12$$
> $$\mathbf x=2\mathbf f_1-\tfrac12\mathbf f_2-\tfrac12\mathbf f_3$$
> *(Verified: $2(1,1,1)-\tfrac12(1,-1,0)-\tfrac12(1,1,-2)=(1,2,3)$ ✓.)*
>
> **Each coefficient took one dot product and one division. In a non-orthogonal basis this would be a $3\times3$ system.**
>
> **(iii)** $\hat{\mathbf f}_1=\tfrac1{\sqrt3}(1,1,1)$, $\hat{\mathbf f}_2=\tfrac1{\sqrt2}(1,-1,0)$, $\hat{\mathbf f}_3=\tfrac1{\sqrt6}(1,1,-2)$, and now the coefficients are plain dot products:
> $$\mathbf x=(\mathbf x\cdot\hat{\mathbf f}_1)\hat{\mathbf f}_1+(\mathbf x\cdot\hat{\mathbf f}_2)\hat{\mathbf f}_2+(\mathbf x\cdot\hat{\mathbf f}_3)\hat{\mathbf f}_3=\tfrac6{\sqrt3}\hat{\mathbf f}_1-\tfrac1{\sqrt2}\hat{\mathbf f}_2-\tfrac3{\sqrt6}\hat{\mathbf f}_3$$
> *(Consistency: $t_1=\tfrac{6}{\sqrt3}\cdot\tfrac1{\sqrt3}=2$ ✓.)*
>
> **(iv)** The three components $2\mathbf f_1$, $-\tfrac12\mathbf f_2$, $-\tfrac12\mathbf f_3$ are mutually orthogonal, so
> $$\|\mathbf x\|^2=4\|\mathbf f_1\|^2+\tfrac14\|\mathbf f_2\|^2+\tfrac14\|\mathbf f_3\|^2=4(3)+\tfrac14(2)+\tfrac14(6)=12+\tfrac12+\tfrac32=14$$
> and directly $\|(1,2,3)\|^2=1+4+9=14$ ✓
>
> > [!important] This is variance decomposition
> > **In an orthonormal basis, $\|\mathbf x\|^2=\sum(\mathbf x\cdot\hat{\mathbf f}_i)^2$ — the squared length splits exactly among the coordinates**, with no cross terms.
> >
> > **That is why PCA can report "this component explains 43% of the variance":** the components are orthogonal, so the variances add. **Non-orthogonal components have overlapping contributions and no such decomposition exists** — which is the whole difficulty with interpreting correlated regressors.

> [!question] Exercise 5 — least squares *(hard)*
> **(a)** Fit a line to $(1,1),(3,2),(4,3),(6,4),(7,5)$.
> (i) Write down $M$ and form the normal equations.
> (ii) Solve them exactly.
> (iii) Compute the residual vector and verify it is orthogonal to **both** columns of $M$.
>
> **(b)** (i) Why is $A^{\mathsf T}A$ invertible exactly when the columns of $A$ are independent?
> (ii) What goes wrong if two data points share the same $x$? If **all** of them do?
> (iii) Explain in one sentence why the same machinery fits a parabola.

> [!example]- Solution
> **(a)(i)** $M=\begin{bmatrix}1&1\\1&3\\1&4\\1&6\\1&7\end{bmatrix}$, $\mathbf y=(1,2,3,4,5)^{\mathsf T}$, and
> $$M^{\mathsf T}M=\begin{bmatrix}n&\sum x\\ \sum x&\sum x^2\end{bmatrix}=\begin{bmatrix}5&21\\21&111\end{bmatrix},\qquad M^{\mathsf T}\mathbf y=\begin{bmatrix}\sum y\\ \sum xy\end{bmatrix}=\begin{bmatrix}15\\78\end{bmatrix}$$
> *(Verified.)*
>
> **(ii)** $\det(M^{\mathsf T}M)=555-441=114$, so
> $$\mathbf z=\frac1{114}\begin{bmatrix}111&-21\\-21&5\end{bmatrix}\begin{bmatrix}15\\78\end{bmatrix}=\frac1{114}\begin{bmatrix}27\\75\end{bmatrix}=\boxed{\begin{bmatrix}9/38\\25/38\end{bmatrix}}=\begin{bmatrix}0.2368\\0.6579\end{bmatrix}$$
> so $y=0.237+0.658x$. *(Verified.)*
>
> **(iii)** Fitted values $\hat y_i=\tfrac{9+25x_i}{38}$ give $\hat{\mathbf y}=\tfrac1{38}(34,84,109,159,184)$, and
> $$\mathbf r=\mathbf y-\hat{\mathbf y}=\tfrac1{38}(4,-8,5,-7,6)$$
> Checks:
> $$\mathbf 1\cdot\mathbf r=\tfrac1{38}(4-8+5-7+6)=0\ ✓$$
> $$\mathbf x\cdot\mathbf r=\tfrac1{38}(4-24+20-42+42)=0\ ✓$$
> **Both zero — the residual is orthogonal to the column space, which is what "best approximation" means.**
>
> **The first identity is why residuals sum to zero whenever the model has an intercept**, and the second is why residuals are uncorrelated with every regressor. **Neither is an assumption about the data; both are forced by the geometry** ([[Econometrics/contents/00-Index|Econometrics]]).
>
> **(b)(i)** $A^{\mathsf T}A\mathbf x=\mathbf 0\Rightarrow\mathbf x^{\mathsf T}A^{\mathsf T}A\mathbf x=0\Rightarrow\|A\mathbf x\|^2=0\Rightarrow A\mathbf x=\mathbf 0$. So
> $$\operatorname{null}(A^{\mathsf T}A)=\operatorname{null}A$$
> and $A^{\mathsf T}A$ (square) is invertible $\iff\operatorname{null}A=\{\mathbf 0\}\iff$ **the columns of $A$ are independent**, by the Inverse Theorem. $\blacksquare$
>
> **The move $\mathbf x^{\mathsf T}A^{\mathsf T}A\mathbf x=\|A\mathbf x\|^2$ is worth remembering** — it is also why $A^{\mathsf T}A$ is positive semi-definite ([[08 - Orthogonality|ch. 08]]).
>
> **(b)(ii)**
> - **Two points share an $x$:** nothing goes wrong. The columns $\mathbf 1$ and $\mathbf x$ are still independent as long as $\mathbf x$ is not constant, so $M^{\mathsf T}M$ is invertible. **The line simply cannot pass through both points, which is exactly what least squares is for.**
> - **All points share an $x$:** then $\mathbf x=c\mathbf 1$, the columns are **dependent**, $\operatorname{rank}M=1$, and $M^{\mathsf T}M$ is singular. **Geometrically: all the data sit on one vertical line, and no slope is determined** — there are infinitely many best-fitting lines. **This is Nicholson's hypothesis "at least two of the $x_i$ are distinct", and it is exactly the no-perfect-multicollinearity condition of regression.**
>
> **(b)(iii)** **Because $y=r_0+r_1x+r_2x^2$ is linear in the unknowns $r_0,r_1,r_2$** — take $M$ with columns $\mathbf 1,\mathbf x,\mathbf x^2$ and everything above applies verbatim.
>
> > [!important] "Linear model" means linear in the *parameters*
> > **The curve may be as bent as you like.** Polynomials, logs, interactions and splines are all fitted by exactly these normal equations; what is forbidden is a parameter appearing non-linearly, such as $y=r_0e^{r_1x}$.
> >
> > **The cost of flexibility is conditioning.** The columns $\mathbf 1,\mathbf x,\mathbf x^2,\dots$ become nearly dependent as the degree rises, so $M^{\mathsf T}M$ approaches singularity and the fitted coefficients become wildly unstable — **numerically the same disease as the near-coplanar parallelepiped of [[04 - Vector Geometry|ch. 04]], Exercise 4(iii).** *(The standard fixes are orthogonal polynomials — Gram–Schmidt on those columns — or QR instead of the normal equations; both are [[08 - Orthogonality|ch. 08]].)*

---

## 📝 Summary

- **A subspace contains $\mathbf 0$ and is closed under addition and scaling.** In $\mathbb{R}^3$ the subspaces are exactly $\{\mathbf 0\}$, lines and planes **through the origin**, and $\mathbb{R}^3$. **Check $\mathbf 0$ first**; homogeneous linear conditions always pass, inequalities and products never do.
- **$\operatorname{span}$ is always a subspace** — the smallest one containing the given vectors. **$\operatorname{im}A=\operatorname{col}A$**, so "$A\mathbf x=\mathbf b$ is consistent" means "$\mathbf b\in\operatorname{col}A$", and "the solution is unique" means "$\operatorname{null}A=\{\mathbf 0\}$".
- **Independent means the only combination giving $\mathbf 0$ is the trivial one** — equivalently, nothing is redundant, equivalently **every vector in the span has exactly one representation.** A nontrivial solution of $A\mathbf x=\mathbf 0$ *is* a column dependence.
- **Fundamental Theorem: an independent set can never be larger than a spanning set.** Hence the **Invariance Theorem** — all bases of a subspace have the same size — and hence $\dim$ is well defined. **$\dim U$ is both the smallest spanning set and the largest independent set.**
- **Three labour-savers.** Independent sets can be **enlarged** to bases and spanning sets **cut down** to bases (Thm 6); with exactly $\dim U$ vectors, **independence and spanning are equivalent** (Thm 7); and $U\subseteq W$ with $\dim U=\dim W$ forces $U=W$ (Thm 8).
- **Orthogonal sets are automatically independent**, Pythagoras holds for them, and the **Expansion Theorem** gives each coordinate as a single dot product $\dfrac{\mathbf x\cdot\mathbf f_i}{\|\mathbf f_i\|^2}$ — no system to solve. **Each term is a chapter-4 projection.**
- **$\dim(\operatorname{row}A)=\dim(\operatorname{col}A)=\operatorname{rank}A$** — surprising, since the two spaces sit in different $\mathbb{R}$'s. **This finally makes ch. 1's definition of rank legitimate.**
- **Read bases off correctly:** the nonzero rows of $R$ give $\operatorname{row}A$; **the pivot columns of the *original* $A$ give $\operatorname{col}A$.** Row operations preserve the row space and change the column space.
- $$\boxed{\operatorname{rank}A+\dim(\operatorname{null}A)=n}$$ **— ch. 1's "$n-r$ parameters" as a conservation law**, and the ancestor of the dimension theorem in ch. 7. Also $\operatorname{rank}(AB)\le\min(\operatorname{rank}A,\operatorname{rank}B)$: **composition never restores lost information.**
- **Similar matrices share $\det$, $\operatorname{tr}$, $\operatorname{rank}$ and the whole characteristic polynomial** — they are one transformation in two coordinate systems. **$A$ is diagonalizable iff geometric multiplicity $=$ algebraic multiplicity for every eigenvalue**, which is what ch. 3 could not yet say.
- **Least squares: when $\mathbf b\notin\operatorname{col}A$, project.** The minimiser of $\|\mathbf b-A\mathbf z\|$ solves the **normal equations** $A^{\mathsf T}A\mathbf z=A^{\mathsf T}\mathbf b$, derived in one line from "the residual must be orthogonal to every column".
- **$A^{\mathsf T}A$ is invertible $\iff$ the columns of $A$ are independent**, because $\operatorname{null}(A^{\mathsf T}A)=\operatorname{null}A$ via $\mathbf x^{\mathsf T}A^{\mathsf T}A\mathbf x=\|A\mathbf x\|^2$.
- **"Linear" model means linear in the *parameters*** — polynomials and transformations of $x$ are all fitted by the same normal equations, at the cost of worsening conditioning.

---

## ⚠️ Important Notes

> [!warning] Column-space bases come from $A$, not from its reduced form
> **Row operations change the column space.** They preserve *which* columns are independent (because $R=UA$ with $U$ invertible, so $A\mathbf x=\mathbf 0\iff R\mathbf x=\mathbf 0$), but not the columns themselves.
>
> | Space | Read off from |
> |---|---|
> | $\operatorname{row}A$ | the **nonzero rows of $R$** |
> | $\operatorname{col}A$ | the **pivot columns of $A$** |
> | $\operatorname{null}A$ | the **basic solutions** from $R$ |
>
> **The reduction tells you which columns; the original tells you what they are.** This is the most frequently mis-remembered fact in the chapter.

> [!warning] Count before you compute
> Three questions that need no arithmetic:
> - **More than $n$ vectors in $\mathbb{R}^n$?** Dependent — always.
> - **Fewer than $\dim U$ vectors?** Cannot span $U$ — always.
> - **Exactly $\dim U$ vectors?** Check independence **or** spanning, never both (Theorem 7).
>
> **Most "is this a basis?" problems are settled by counting**, and doing the row reduction first is wasted effort.

> [!warning] "Independent" and "orthogonal" are not the same strength
> $$\text{orthogonal}\ \Longrightarrow\ \text{independent},\qquad \text{but not conversely}$$
> $\{(1,0),(1,1)\}$ is independent and not orthogonal.
>
> **Orthogonality is strictly stronger and buys you the Expansion Theorem** — coordinates by dot product instead of by solving a system. **That upgrade is worth so much that chapter 8 is largely about manufacturing orthogonal bases from ordinary ones (Gram–Schmidt).**

> [!warning] Rank is bounded by *both* dimensions, and this constrains models
> $$\operatorname{rank}A\le\min(m,n)$$
> **Consequences that bite in practice:**
> - **If $A$ is $m\times n$ with $n>m$, the columns are dependent** — guaranteed. In a regression with more predictors than observations, $X^{\mathsf T}X$ is **always** singular, and no amount of data cleaning changes that. *(This is why the $p>n$ regime needs regularisation rather than ordinary least squares.)*
> - $\operatorname{rank}(AB)\le\min(\operatorname{rank}A,\operatorname{rank}B)$ — **a chain of maps cannot recover what any link destroyed.**

> [!warning] $\dim$ is a property of the *space*, not of the vectors you happened to write down
> A set of 5 vectors may span a 2-dimensional subspace; a set of 2 vectors may fail to span it. **The number of vectors you were handed says nothing about the dimension** until you have checked independence.
>
> **The corresponding error in applications: counting "features" rather than *effective* dimension.** 100 highly correlated columns may span a subspace of dimension 3, which is precisely the observation PCA exploits.

> [!warning] Least squares does not check whether the model is right
> **The normal equations always return the closest point in $\operatorname{col}A$**, however far away that is. A large residual is the *only* signal that the model is inadequate, and the fitting procedure will never complain.
>
> **Two failure modes to keep separate:**
> - **$\mathbf b$ far from $\operatorname{col}A$:** the model does not fit. Look at $\|\mathbf r\|$.
> - **Columns of $A$ nearly dependent:** the *coefficients* are unstable even if the fit is excellent. Look at $\det(A^{\mathsf T}A)$ or a condition number.
>
> **The second is the more dangerous, because the fit looks fine.** Near-dependence means $M^{\mathsf T}M$ is nearly singular, so tiny changes in the data swing $\mathbf z$ wildly — and it is invisible in the residuals.

> [!note] Cross-subject connections
> - [[01 - Systems of Linear Equations|Ch. 01]] — **§5.4 finally proves rank is well defined**; the basic solutions become a basis of $\operatorname{null}A$, and "$n-r$ parameters" becomes rank–nullity.
> - [[02 - Matrix Algebra|Ch. 02]] — **"columns independent" and "columns span" join the Inverse Theorem**; $\operatorname{im}A=\operatorname{col}A$ is Definition 2.5 restated.
> - [[03 - Determinants and Diagonalization|Ch. 03]] — §5.5 redoes diagonalization with independence available, and proves what ch. 3 could only assert.
> - [[04 - Vector Geometry|Ch. 04]] — **the projection formula becomes the Expansion Theorem and then least squares**; "project and keep the residual" is unchanged, only the target is now a subspace.
> - [[07 - Linear Transformations|Ch. 07]] — rank–nullity becomes $\dim(\ker T)+\dim(\operatorname{im}T)=\dim V$.
> - [[08 - Orthogonality|Ch. 08]] — **Gram–Schmidt manufactures the orthogonal bases §5.3 shows are so valuable**; QR replaces the normal equations; PCA is §5.7 plus the spectral theorem.
> - [[Econometrics/contents/00-Index|Econometrics]] — **§5.6 *is* OLS.** $\hat{\boldsymbol\beta}=(X^{\mathsf T}X)^{-1}X^{\mathsf T}\mathbf y$, residuals orthogonal to regressors by construction, $\sum r_i=0$ when there is an intercept, and **perfect multicollinearity is exactly "the columns of $X$ are dependent"** — Exercise 5(b)(ii).
> - [[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07]] — **the space of random variables with $\mathbb{E}[XY]$ as dot product**: uncorrelated means orthogonal, $\mathbb{E}[Y\mid X]$ is a projection, and the law of total variance is Pythagoras.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **rank is the effective number of features**; low-rank approximation, the $p>n$ problem, and the variance decomposition of Exercise 4(iv) that lets PCA report "% variance explained".

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **Two proofs are deferred out of the chapter**, and both are load-bearing:
> - **The Fundamental Theorem (Thm 4, §5.2)** — on which the Invariance Theorem, and therefore the whole notion of dimension, depends — is stated with the note "This proof is given in Theorem 2 Section 6.3 in much greater generality." **As chapter 5 is read, dimension rests on an unproved assertion.**
> - **Theorem 6 (§5.2)** — that every subspace has a basis, and that independent sets can be enlarged and spanning sets cut down — is likewise deferred to §6.4.
>
> **Both deferrals are deliberate and are stated**, and both are discharged in chapter 6. But a reader stopping at chapter 5 (which Nicholson explicitly offers as an option) **takes the two central structural theorems on trust.**
>
> **A data table that does not extract — reconstructed.** §5.6 Example 3 refers to "the accompanying table" of five data points, **which is an image and yields nothing.** The printed working, however, gives $M^{\mathsf T}M=\left[\begin{smallmatrix}5&21\\21&111\end{smallmatrix}\right]$ and $M^{\mathsf T}\mathbf y=\left[\begin{smallmatrix}15\\78\end{smallmatrix}\right]$, i.e. $n=5$, $\sum x=21$, $\sum x^2=111$, $\sum y=15$, $\sum xy=78$. **The points $(1,1),(3,2),(4,3),(6,4),(7,5)$ reproduce all four sums exactly**, and yield $\det=114$ and $\mathbf z=\tfrac1{38}(9,25)=(0.2368,0.6579)\approx(0.24,0.66)$ — **every printed figure** ✓. *(I cannot prove the table is these points, only that they are consistent with everything printed; Exercise 5 uses them and says so.)*
>
> **Source typos:**
> - **§5.6 Example 3 prints the normal equations as $\left[\begin{smallmatrix}5&21\\21&111\end{smallmatrix}\right]\ \mathbf{=}\ \left[\begin{smallmatrix}z_0\\z_1\end{smallmatrix}\right]=\left[\begin{smallmatrix}15\\78\end{smallmatrix}\right]$** — the first symbol should be multiplication, not equality. As printed the equation is nonsense.
> - **§5.4, proof of Corollary 3, writes $\operatorname{rank}(AV)=\operatorname{rank}(AV)^{\mathsf T}$** — missing the "rank of the transpose" notation; it should be $\operatorname{rank}\big((AV)^{\mathsf T}\big)$.
> - **§5.4, proof of Corollary 4, states "$\operatorname{col}(AB)\subseteq\operatorname{col}A$ and $\operatorname{row}(BA)\subseteq\operatorname{row}A$"** — the second should be $\operatorname{row}(AB)\subseteq\operatorname{row}B$ for the corollary as stated.
> - **§5.3 Theorem 4 reads "If $\{\mathbf x_1,\dots,\mathbf x_k\}$ is **a** orthogonal set"** — should be *an*.
>
> **PDF extraction:** as in chapters 1–4, **all matrices lose their brackets and row structure, with minus signs displaced to the end of a row**; column vectors extract one entry per line. **`U … V` are large set braces** (so `U { r, s, r } | r, s in /bbR V` is $\left\{(r,s,r)^{\mathsf T}\mid r,s\in\mathbb{R}\right\}$), **`Q … R` are large parentheses** in the Expansion Theorem, **`S … T` are large brackets**, and **`/bbR` is $\mathbb{R}$**. Subscripted subscripts collapse badly: $\mathbf c_{j_1},\mathbf c_{j_2},\dots,\mathbf c_{j_r}$ extracts as ` c j1 ,  c j2 , …,  c jr ` on a single run-together line. **All figures are images**, including the Pythagoras diagram of §5.3 and the projection/best-approximation picture of §5.6 — **the latter is the one that makes least squares obvious, and it is lost.**
>
> **Verification performed:** every worked example quoted was independently recomputed in exact rational arithmetic. Confirmed: $\operatorname{rank}A=2$ with row basis $\{(1,2,2,-1),(0,0,1,-3)\}$ and **column basis being columns 1 and 3 of $A$**, namely $(1,3,1)$ and $(2,5,1)$ (§5.4 Ex. 2); and **the entire least-squares computation of §5.6 Ex. 3** — $M^{\mathsf T}M$, $M^{\mathsf T}\mathbf y$, $\det=114$, and $\mathbf z=\tfrac1{38}(9,25)$ — **from the reconstructed data.** **All agree with the text.** Every exercise figure in these notes was likewise verified before being written down, including both null-space basis vectors of Exercise 3 and the orthogonality of both residual inner products in Exercise 5.
>
> **Scope note:** **§5.7 (correlation and variance) is folded into the cross-links rather than given its own section.** Its content — that the sample correlation of two data vectors is the cosine of the angle between their centred versions — is [[04 - Vector Geometry|ch. 04]]'s Theorem 2 applied to statistics, and it is treated more fully in [[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07]]. **§5.5 (similarity and diagonalization) is compressed**, because its computational content duplicates [[03 - Determinants and Diagonalization|ch. 03]]; what is genuinely new — that the criterion is *independence* of eigenvectors, and the geometric-versus-algebraic multiplicity test — is stated in §5 above.

#linear-algebra #subspace #span #independence #basis #dimension #rank #rank-nullity #orthogonality #least-squares
