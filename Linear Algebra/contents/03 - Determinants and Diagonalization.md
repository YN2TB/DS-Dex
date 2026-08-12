---
subject: Linear Algebra
chapter: 03
tags: [ds, linear-algebra, determinant, cofactor-expansion, eigenvalue, eigenvector, diagonalization, dynamical-system]
source: "Nicholson, *Linear Algebra with Applications*, 7th ed., ch. 3 (pp. 126–183)"
---

# Determinants and Diagonalization

> [!abstract] What this chapter is for
> **Two topics, and the second is far more important than the first.**
>
> **Determinants** give a single number that answers "is this matrix invertible?" — and, in $\mathbb{R}^2$ and $\mathbb{R}^3$, that number is a signed area or volume. They are theoretically indispensable and computationally almost useless beyond $3\times3$.
>
> **Eigenvalues and eigenvectors** ask a different question: **are there directions the matrix does not turn?**
> $$A\mathbf x=\lambda\mathbf x,\qquad \mathbf x\ne\mathbf 0$$
> If you can find $n$ independent such directions, the matrix becomes *diagonal* in those coordinates — and diagonal matrices are trivial to raise to powers, which is why this chapter can solve dynamical systems, linear recurrences and Markov chains that nothing before it could touch.
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | **Cofactor expansion** | A recursive definition; **row-reduce instead of expanding** |
> | **2** | Products, adjugates, Cramer | $\det(AB)=\det A\det B$; **$\det A\ne0\iff$ invertible** |
> | **3** | **Eigenvalues and diagonalization** | $P^{-1}AP=D$ when there are $n$ independent eigenvectors |
> | **4–5** | Dynamical systems, recurrences | **$A^k$ is easy once $A$ is diagonalized** — the payoff |
>
> **Nicholson places this chapter unusually early** — before independence, dimension or subspaces — because diagonalization needs only determinants and inverses. **The price is that "$n$ independent eigenvectors" cannot yet be said properly**, and chapter 5 has to revisit the whole topic. **The gain is that you can compute with eigenvalues months before you can define a basis.**

---

## 📘 Main Knowledge

### 1. The cofactor expansion

For a $2\times2$ matrix, $\det\begin{bmatrix}a&b\\c&d\end{bmatrix}=ad-bc$. Beyond that the definition is **recursive**.

> [!important] Definitions 3.1–3.2 and Theorem 1 (§3.1)
> For an $n\times n$ matrix $A=[a_{ij}]$:
> - the **$(i,j)$-minor** $A_{ij}$ is the $(n-1)\times(n-1)$ matrix left after deleting row $i$ and column $j$;
> - the **$(i,j)$-cofactor** is $c_{ij}(A)=(-1)^{i+j}\det A_{ij}$;
> - **$\det A$ is the cofactor expansion along *any* row or column:**
> $$\det A=a_{i1}c_{i1}+a_{i2}c_{i2}+\cdots+a_{in}c_{in}\qquad(\text{any fixed }i)$$

**The sign pattern $(-1)^{i+j}$ is a checkerboard starting with $+$ in the top-left:**

$$\begin{bmatrix}+&-&+&\cdots\\-&+&-&\\+&-&+&\\ \vdots&&&\ddots\end{bmatrix}$$

> [!tip] Expand along the row or column with the most zeros
> Every zero entry kills a whole $(n-1)\times(n-1)$ determinant. **Choosing the sparsest line is the single biggest saving available**, and Theorem 1's guarantee that *any* line gives the same answer is what makes the choice free.

> [!important] Theorem 2 (§3.1) — the five properties
> | | Operation on $A$ | Effect on $\det A$ |
> |---|---|---|
> | 1 | a row or column of zeros | $\det A=0$ |
> | 2 | **interchange two rows (or columns)** | $\det\to-\det$ |
> | 3 | **multiply a row (or column) by $u$** | $\det\to u\det$ |
> | 4 | two rows (or columns) identical | $\det A=0$ |
> | 5 | **add a multiple of one row to a *different* row** | $\det$ **unchanged** |
>
> **Property 5 is the workhorse: the row operation you use most does not change the determinant at all.**

> [!important] Theorems 3, 4 and 5 (§3.1)
> - $\det(uA)=u^n\det A$ for an $n\times n$ matrix — **because every one of the $n$ rows is scaled.**
> - **A triangular matrix's determinant is the product of its diagonal entries.**
> - Block triangular: $\det\begin{bmatrix}A&X\\0&B\end{bmatrix}=\det\begin{bmatrix}A&0\\Y&B\end{bmatrix}=\det A\,\det B$.

> [!important] The practical algorithm
> **Row-reduce to triangular form, tracking only interchanges and scalings, then multiply the diagonal.**
>
> | Operation | Bookkeeping |
> |---|---|
> | add a multiple of a row to another | nothing |
> | interchange two rows | multiply the running answer by $-1$ |
> | multiply a row by $u$ | multiply the running answer by $1/u$ |
>
> **Cofactor expansion on an $n\times n$ matrix costs about $n!$ multiplications; row reduction costs about $n^3/3$.** At $n=20$ that is $2\times10^{18}$ against $2700$. **Cofactor expansion is a definition and a proof technique, not a method.**

> [!example] Example 8 (§3.1) — the Vandermonde determinant
> $$\det\begin{bmatrix}1&1&1\\a_1&a_2&a_3\\a_1^2&a_2^2&a_3^2\end{bmatrix}=(a_2-a_1)(a_3-a_1)(a_3-a_2)$$
> *(Verified at $(a_1,a_2,a_3)=(1,2,4)$: the determinant is $6=(1)(3)(2)$ ✓.)*
>
> **This is nonzero exactly when the $a_i$ are distinct** — which proves, in one line, that $n+1$ points with distinct $x$-coordinates determine a unique interpolating polynomial. **[[01 - Systems of Linear Equations|Chapter 1's]] Exercise 5(c) proved the same thing by counting roots; here it is a formula.**

---

### 2. Determinants, products and inverses

> [!important] Theorem 1 (§3.2) — the product theorem
> $$\boxed{\ \det(AB)=\det A\ \det B\ }$$
> and by induction $\det(A_1A_2\cdots A_k)=\det A_1\cdots\det A_k$, so $\det(A^k)=(\det A)^k$.

> [!important] Theorem 3 (§3.2) — the criterion
> $$\boxed{\ A\text{ is invertible}\iff\det A\ne0\ }\qquad\text{and then}\qquad \det(A^{-1})=\frac1{\det A}$$
>
> **This is the sixth entry in the Inverse Theorem** ([[02 - Matrix Algebra|ch. 02 §4]]), and the one that is a single computable number.

**Also $\det(A^{\mathsf T})=\det A$** — which is why every row property in Theorem 2 has a column twin.

> [!important] The adjugate and Cramer's rule
> With $\operatorname{adj}A=[c_{ij}(A)]^{\mathsf T}$ (the **transpose** of the cofactor matrix):
> $$A(\operatorname{adj}A)=(\operatorname{adj}A)A=(\det A)I\qquad\Longrightarrow\qquad A^{-1}=\frac1{\det A}\operatorname{adj}A$$
> and **Cramer's rule**: the $i$th entry of the solution of $A\mathbf x=\mathbf b$ is $\dfrac{\det A_i}{\det A}$, where $A_i$ is $A$ with column $i$ replaced by $\mathbf b$.

> [!warning] Both formulas are theoretically important and practically useless
> **The adjugate of an $n\times n$ matrix requires $n^2$ determinants of size $(n-1)$** — astronomically more work than $[A\,|\,I]\to[I\,|\,A^{-1}]$. Cramer's rule needs $n+1$ determinants to solve one system.
>
> **Their value is that they are *formulas*:** they show $A^{-1}$ depends smoothly on the entries of $A$ (useful for proving things and for differentiating), and they give closed forms for $2\times2$ and $3\times3$ cases. **For anything larger, use elimination.**

> [!tip] What a determinant *is*: signed area and volume
> **In $\mathbb{R}^2$, $|\det[\mathbf u\ \mathbf v]|$ is the area of the parallelogram spanned by $\mathbf u$ and $\mathbf v$; in $\mathbb{R}^3$ it is the volume of the parallelepiped.** The **sign** records orientation.
>
> **Every property of Theorem 2 becomes obvious:**
> - two identical rows $\Rightarrow$ the parallelogram is degenerate $\Rightarrow$ zero area;
> - scaling one edge by $u$ scales the area by $u$;
> - **adding a multiple of one edge to another shears the parallelogram — same base, same height, same area.** That is property 5, and it is why the workhorse row operation is free.
>
> **And $\det(AB)=\det A\det B$ says volume-scaling factors multiply under composition** — which is exactly the change-of-variables Jacobian in [[Calculus/contents/00-Index|Calculus]] and the density-transformation factor in [[Probability Theory/contents/06 - Jointly Distributed Random Variables|Probability ch. 06 §7]].

---

### 3. Eigenvalues, eigenvectors, diagonalization

> [!important] Definition 3.4
> $\lambda$ is an **eigenvalue** of the $n\times n$ matrix $A$ if
> $$A\mathbf x=\lambda\mathbf x\qquad\text{for some }\mathbf x\ne\mathbf 0$$
> and any such $\mathbf x$ is a **$\lambda$-eigenvector**.

> [!tip] What the definition says geometrically
> **$A$ generally turns vectors. An eigenvector is a direction $A$ leaves alone — it only stretches it (by $\lambda$), or flips it (if $\lambda<0$), or crushes it (if $\lambda=0$).**
>
> Equivalently, **the line $\mathbb{R}\mathbf x$ through the origin is $A$-invariant.** Diagonalization is the search for enough such lines to describe the whole space.

#### 3a. Finding them

$A\mathbf x=\lambda\mathbf x$ with $\mathbf x\ne\mathbf 0$ says $(\lambda I-A)\mathbf x=\mathbf 0$ has a nontrivial solution, which by the Inverse Theorem says $\lambda I-A$ is **not** invertible, which by Theorem 3 of §3.2 says its determinant vanishes.

> [!important] Definition 3.5 and Theorem 2 (§3.3)
> The **characteristic polynomial** is
> $$c_A(x)=\det(xI-A)$$
> a polynomial of degree $n$. Then:
> 1. **the eigenvalues of $A$ are the roots of $c_A(x)$;**
> 2. **the $\lambda$-eigenvectors are the nonzero solutions of $(\lambda I-A)\mathbf x=\mathbf 0$.**

> [!warning] Nicholson uses $\det(xI-A)$, not $\det(A-xI)$
> **Both conventions are in circulation and they differ by $(-1)^n$.** Nicholson's choice makes $c_A$ **monic** (leading coefficient $+1$), which is tidier. The *roots* — the eigenvalues — are identical either way, so nothing computational depends on it, **but the polynomial you write down does**, and a sign discrepancy against another textbook is usually this and not an error.

**Two invariants readable straight off the polynomial:**

$$\det A=\prod_i\lambda_i,\qquad \operatorname{tr}A=\sum_i\lambda_i$$

> [!example] Example 3 (§3.3)
> $A=\begin{bmatrix}3&5\\1&-1\end{bmatrix}$ gives $c_A(x)=x^2-2x-8=(x-4)(x+2)$, so $\lambda=4,-2$.
> $$\lambda=4:\ \mathbf x=t\begin{bmatrix}5\\1\end{bmatrix},\qquad \lambda=-2:\ \mathbf x=t\begin{bmatrix}-1\\1\end{bmatrix}\qquad(t\ne0)$$
> *(Verified: $A(5,1)=(20,4)=4(5,1)$ ✓ and $A(-1,1)=(2,-2)=-2(-1,1)$ ✓. Also $\operatorname{tr}A=2=4+(-2)$ ✓ and $\det A=-8=4\times(-2)$ ✓.)*

> [!example] Example 4 (§3.3)
> $A=\begin{bmatrix}2&0&0\\1&2&-1\\1&3&-2\end{bmatrix}$ has $c_A(x)=(x-2)(x-1)(x+1)$ and basic eigenvectors
> $$\lambda_1=2:\ (1,1,1),\qquad \lambda_2=1:\ (0,1,1),\qquad \lambda_3=-1:\ (0,1,3)$$
> *(All three verified by direct multiplication; $\det A=-2=2\cdot1\cdot(-1)$ ✓.)*

**Every nonzero multiple of an eigenvector is an eigenvector, and so is every nonzero linear combination of $\lambda$-eigenvectors for the *same* $\lambda$** — the $\lambda$-eigenvectors together with $\mathbf 0$ form the **eigenspace**, which is the null space of $\lambda I-A$. **A set of nonzero multiples of the basic solutions is a set of *basic eigenvectors*.**

#### 3b. Diagonalization

> [!important] Definition 3.6 and Theorem 4 (§3.3)
> $A$ is **diagonalizable** if $P^{-1}AP=D$ is diagonal for some invertible $P$. Then:
> 1. **$A$ is diagonalizable $\iff$ it has $n$ eigenvectors $\mathbf x_1,\dots,\mathbf x_n$ for which $P=[\mathbf x_1\ \cdots\ \mathbf x_n]$ is invertible;**
> 2. in that case $P^{-1}AP=\operatorname{diag}(\lambda_1,\dots,\lambda_n)$ with $\lambda_i$ the eigenvalue of $\mathbf x_i$.

**The proof is a one-line column comparison.** $AP=PD$ reads

$$[A\mathbf x_1\ \ \cdots\ \ A\mathbf x_n]=[\lambda_1\mathbf x_1\ \ \cdots\ \ \lambda_n\mathbf x_n]$$

— **column $i$ says exactly $A\mathbf x_i=\lambda_i\mathbf x_i$.** Nothing more is going on.

> [!tip] Check $AP=PD$, never $P^{-1}AP=D$
> **The two are equivalent but the first needs no inverse.** Nicholson says so explicitly, and it removes the most error-prone step from every diagonalization exercise.

> [!example] Example 8 (§3.3)
> Continuing Example 4:
> $$P=\begin{bmatrix}1&0&0\\1&1&1\\1&1&3\end{bmatrix},\qquad P^{-1}AP=\begin{bmatrix}2&0&0\\0&1&0\\0&0&-1\end{bmatrix}$$
> **The order of the columns of $P$ is yours to choose**, and reordering them permutes the diagonal of $D$ correspondingly.

> [!important] Theorem 5 (§3.3) — the sufficient condition
> **Eigenvectors belonging to *distinct* eigenvalues are independent.** Hence:
> $$n\text{ distinct eigenvalues}\ \Longrightarrow\ A\text{ is diagonalizable}$$
> **The converse is false**, and Example 9 is the standard counterexample.

> [!example] Example 9 (§3.3) — a repeated eigenvalue that still works
> $A=\begin{bmatrix}0&1&1\\1&0&1\\1&1&0\end{bmatrix}$ has $c_A(x)=(x-2)(x+1)^2$: eigenvalues $2$ and $-1$ (twice).
> *(Verified.)* **Yet $A$ is diagonalizable**, because the eigenspace for $\lambda=-1$ is two-dimensional — $(-1)I-A$ has rank 1, so its null space has dimension 2.
>
> **The rule that actually governs diagonalizability:**
> $$A\text{ diagonalizable}\iff\text{for every }\lambda,\ \dim(\text{eigenspace})=\text{multiplicity of }\lambda\text{ in }c_A$$
> **A repeated eigenvalue is a *warning*, not a verdict.** It may supply enough eigenvectors (as here) or not (Exercise 4).

> [!warning] Not every matrix is diagonalizable
> $$A=\begin{bmatrix}2&1\\0&2\end{bmatrix}$$
> has $c_A(x)=(x-2)^2$, so $\lambda=2$ twice — but $2I-A=\begin{bmatrix}0&-1\\0&0\end{bmatrix}$ has rank 1, so the eigenspace is only **one**-dimensional. **There is no second independent eigenvector, and no $P$ exists.** *(Verified.)*
>
> **The geometric reason:** $A$ shears as well as scales, and a shear has exactly one invariant line. **Over $\mathbb{R}$ there is a second failure mode too** — the rotation $\begin{bmatrix}0&-1\\1&0\end{bmatrix}$ has $c_A(x)=x^2+1$ with **no real roots at all**, because a rotation by $90°$ leaves no direction fixed. **Chapter 8 shows that symmetric matrices never suffer either problem.**

#### 3c. Why anyone cares: powers

$$A=PDP^{-1}\quad\Longrightarrow\quad A^k=PD^kP^{-1},\qquad D^k=\operatorname{diag}(\lambda_1^k,\dots,\lambda_n^k)$$

**Raising a diagonal matrix to a power is $n$ scalar exponentiations.** Everything expensive about $A^k$ disappears.

> [!important] Linear dynamical systems (§§3.3–3.5)
> A system evolving by $\mathbf v_{k+1}=A\mathbf v_k$ has $\mathbf v_k=A^k\mathbf v_0$. Writing $\mathbf v_0=c_1\mathbf x_1+\cdots+c_n\mathbf x_n$ in the eigenvector basis,
> $$\boxed{\ \mathbf v_k=c_1\lambda_1^k\mathbf x_1+c_2\lambda_2^k\mathbf x_2+\cdots+c_n\lambda_n^k\mathbf x_n\ }$$
> **The long-run behaviour is governed entirely by the largest $|\lambda_i|$:**
>
> | Dominant $|\lambda|$ | Behaviour |
> |---|---|---|
> | $>1$ | growth, in the direction of that eigenvector |
> | $=1$ | **steady state** — this is the Markov chain case |
> | $<1$ | decay to $\mathbf 0$ |
>
> **The second-largest $|\lambda|$ sets the *rate* at which the other components die out** — which is the "spectral gap" of [[Probability Theory/contents/09 - Additional Topics in Probability|Probability ch. 09]] and the convergence rate of the Markov example in [[02 - Matrix Algebra|ch. 02 §8]].

**Linear recurrences (§3.4)** are the same theorem in disguise: $x_{k+2}=ax_{k+1}+bx_k$ becomes

$$\begin{bmatrix}x_{k+2}\\x_{k+1}\end{bmatrix}=\begin{bmatrix}a&b\\1&0\end{bmatrix}\begin{bmatrix}x_{k+1}\\x_k\end{bmatrix}$$

— **and the characteristic polynomial of that matrix is exactly the recurrence's own characteristic equation** $x^2=ax+b$.

---

## ✏️ Exercises

> [!question] Exercise 1 — computing determinants *(warm-up)*
> (i) Compute $\det\begin{bmatrix}2&-1&3\\1&4&0\\3&2&-2\end{bmatrix}$ by cofactor expansion, choosing the best line.
> (ii) Recompute it by row-reduction to triangular form, tracking the bookkeeping.
> (iii) Without computing, state $\det$ of $\begin{bmatrix}1&5&2\\0&0&0\\3&1&7\end{bmatrix}$, $\begin{bmatrix}2&1&4\\0&3&5\\0&0&-1\end{bmatrix}$, $\begin{bmatrix}1&2&3\\4&5&6\\1&2&3\end{bmatrix}$.
> (iv) If $\det A=5$ for a $3\times3$ matrix, find $\det(2A)$, $\det(A^{\mathsf T})$, $\det(A^{-1})$, $\det(A^3)$.

> [!example]- Solution
> **(i)** Row 2 has a zero, so expand along it: $\det A=-1\cdot\left|\begin{smallmatrix}-1&3\\2&-2\end{smallmatrix}\right|+4\left|\begin{smallmatrix}2&3\\3&-2\end{smallmatrix}\right|-0$
> $$=-1(2-6)+4(-4-9)=4-52=\boxed{-48}$$
> **The signs come from the checkerboard row $(-,+,-)$.**
>
> **(ii)** $R_1\leftrightarrow R_2$ (**factor $-1$**), then $R_2-2R_1$, $R_3-3R_1$ (free), giving $\begin{bmatrix}1&4&0\\0&-9&3\\0&-10&-2\end{bmatrix}$; then $R_3-\tfrac{10}9R_2$ (free) gives the $(3,3)$ entry $-2-\tfrac{10}{3}=-\tfrac{16}3$. Hence
> $$\det A=(-1)\cdot 1\cdot(-9)\cdot\left(-\tfrac{16}3\right)=-48\ ✓$$
> *(Verified.)* **Only the interchange needed bookkeeping** — all three "add a multiple of a row" steps were free.
>
> **(iii)** $0$ (row of zeros), $2\cdot3\cdot(-1)=-6$ (triangular), $0$ (rows 1 and 3 identical).
>
> **(iv)** $\det(2A)=2^3\cdot5=\boxed{40}$ — **not $2\cdot5$**, because all three rows are scaled. $\det(A^{\mathsf T})=5$. $\det(A^{-1})=\tfrac15$. $\det(A^3)=5^3=125$.

> [!question] Exercise 2 — properties, and one that is false
> (i) Show $\det(A^{-1}BA)=\det B$ for invertible $A$. What does this say about similar matrices?
> (ii) If $A$ is $n\times n$ with $A^{\mathsf T}=-A$ and $n$ is odd, show $\det A=0$.
> (iii) Give a $2\times2$ counterexample to $\det(A+B)=\det A+\det B$.
> (iv) If $A^2=I$, what are the possible values of $\det A$? Give a matrix achieving each.

> [!example]- Solution
> **(i)** $\det(A^{-1}BA)=\det(A^{-1})\det B\det A=\dfrac{1}{\det A}\det B\det A=\det B$.
>
> **Similar matrices have equal determinants** — so $\det$ is an invariant of the underlying *transformation*, not of the coordinate system. **The same is true of the trace and of the whole characteristic polynomial**, which is why eigenvalues are basis-independent (ch. 9).
>
> **(ii)** $\det A=\det(A^{\mathsf T})=\det(-A)=(-1)^n\det A=-\det A$ for odd $n$. Hence $2\det A=0$, so $\det A=0$. $\blacksquare$
>
> **Every odd-sized skew-symmetric matrix is singular.** Geometrically, in $\mathbb{R}^3$ such a matrix is a cross-product operator $\mathbf x\mapsto\mathbf a\times\mathbf x$, which annihilates $\mathbf a$ ([[04 - Vector Geometry|ch. 04]]).
>
> **(iii)** $A=\begin{bmatrix}1&2\\3&4\end{bmatrix}$, $B=\begin{bmatrix}0&1\\1&0\end{bmatrix}$: $\det A=-2$, $\det B=-1$, but $A+B=\begin{bmatrix}1&3\\4&4\end{bmatrix}$ has $\det=-8\ne-3$. *(Verified.)*
>
> **$\det$ is multiplicative, never additive.** It *is* linear in each column separately (Theorem 6 of §3.1) — but that is a much weaker statement, and confusing the two is the standard error.
>
> **(iv)** $(\det A)^2=\det(A^2)=\det I=1$, so $\det A=\pm1$.
> Both occur: $I$ has $\det=1$; $\begin{bmatrix}1&0\\0&-1\end{bmatrix}$ (a reflection) has $\det=-1$ and squares to $I$.
>
> **Such matrices are *involutions*, and the sign of the determinant records whether orientation is preserved.** Rotations by $180°$ preserve it; reflections reverse it.

> [!question] Exercise 3 — eigenvalues and eigenvectors
> (i) Find the eigenvalues and basic eigenvectors of $A=\begin{bmatrix}4&1\\2&3\end{bmatrix}$.
> (ii) Verify your answers against $\operatorname{tr}A$ and $\det A$.
> (iii) Find the eigenvalues of $J=\begin{bmatrix}1&1&1\\1&1&1\\1&1&1\end{bmatrix}$ **without** expanding a determinant.
> (iv) Show that if $A\mathbf x=\lambda\mathbf x$ then $A^k\mathbf x=\lambda^k\mathbf x$, and that if $A$ is invertible then $A^{-1}\mathbf x=\lambda^{-1}\mathbf x$. What does the second statement require of $\lambda$?

> [!example]- Solution
> **(i)** $c_A(x)=\det\begin{bmatrix}x-4&-1\\-2&x-3\end{bmatrix}=(x-4)(x-3)-2=x^2-7x+10=(x-2)(x-5)$.
> - $\lambda=5$: $5I-A=\begin{bmatrix}1&-1\\-2&2\end{bmatrix}$, so $\mathbf x=t(1,1)$.
> - $\lambda=2$: $2I-A=\begin{bmatrix}-2&-1\\-2&-1\end{bmatrix}$, so $\mathbf x=t(1,-2)$.
>
> *(Verified: $A(1,1)=(5,5)$ ✓, $A(1,-2)=(2,-4)=2(1,-2)$ ✓.)*
>
> **(ii)** $\operatorname{tr}A=4+3=7=5+2$ ✓ and $\det A=12-2=10=5\times2$ ✓.
> **This is a free check on every $2\times2$ eigenvalue computation** — and for $2\times2$ it is a *method*: the eigenvalues are the roots of $x^2-(\operatorname{tr}A)x+\det A$.
>
> **(iii)** Two observations, no determinant needed:
> - $J(1,1,1)=(3,3,3)$, so **$\lambda=3$** with eigenvector $(1,1,1)$.
> - $\operatorname{rank}J=1$, so the null space has dimension $3-1=2$ — **$\lambda=0$ with multiplicity (at least) 2**, eigenvectors e.g. $(1,-1,0)$ and $(1,0,-1)$.
>
> That is three independent eigenvectors, so the eigenvalues are $\boxed{3,0,0}$ *(verified)* and **$J$ is diagonalizable despite the repeated eigenvalue.**
>
> **The general principle: $\lambda=0$ is an eigenvalue exactly when $A$ is singular, and its eigenspace is the null space.** Reading rank off by inspection is often faster than any characteristic polynomial.
>
> **(iv)** Induction: $A^2\mathbf x=A(\lambda\mathbf x)=\lambda A\mathbf x=\lambda^2\mathbf x$, and so on.
> For the inverse, apply $A^{-1}$ to $A\mathbf x=\lambda\mathbf x$: $\mathbf x=\lambda A^{-1}\mathbf x$, so $A^{-1}\mathbf x=\lambda^{-1}\mathbf x$ — **which requires $\lambda\ne0$**.
>
> **And that is automatic: if $A$ is invertible then $0$ is not an eigenvalue** (otherwise $A\mathbf x=\mathbf 0$ with $\mathbf x\ne\mathbf 0$, contradicting the Inverse Theorem). **So "$0$ is not an eigenvalue" joins the Inverse Theorem list.**
>
> **Note what stays fixed and what changes: the eigen*vectors* are the same for $A$, $A^k$ and $A^{-1}$ — only the eigenvalues move.**

> [!question] Exercise 4 — diagonalization and powers
> (i) Diagonalize $A=\begin{bmatrix}4&1\\2&3\end{bmatrix}$ from Exercise 3, giving $P$ and $D$ explicitly, and verify by checking $AP=PD$.
> (ii) Derive a closed formula for $A^n$ and check it at $n=1$ and $n=10$.
> (iii) Show that $B=\begin{bmatrix}2&1\\0&2\end{bmatrix}$ is **not** diagonalizable.
> (iv) Show that $C=\begin{bmatrix}0&-1\\1&0\end{bmatrix}$ has no real eigenvalues, and say what it does geometrically.

> [!example]- Solution
> **(i)** Take $P=\begin{bmatrix}1&1\\1&-2\end{bmatrix}$ (eigenvectors for $5$ and $2$) and $D=\begin{bmatrix}5&0\\0&2\end{bmatrix}$. Then
> $$AP=\begin{bmatrix}5&2\\5&-4\end{bmatrix}=PD\ ✓$$
> **Checking $AP=PD$ avoids computing $P^{-1}$ entirely.**
>
> **(ii)** $P^{-1}=\dfrac1{-3}\begin{bmatrix}-2&-1\\-1&1\end{bmatrix}=\begin{bmatrix}\tfrac23&\tfrac13\\[2pt]\tfrac13&-\tfrac13\end{bmatrix}$, so $A^n=PD^nP^{-1}$ gives
> $$\boxed{A^n=\frac13\begin{bmatrix}2\cdot5^n+2^n & 5^n-2^n\\ 2\cdot5^n-2\cdot2^n & 5^n+2\cdot2^n\end{bmatrix}}$$
> **Check $n=1$:** $\tfrac13\begin{bmatrix}12&3\\6&9\end{bmatrix}=\begin{bmatrix}4&1\\2&3\end{bmatrix}$ ✓
> **Check $n=10$:** the formula gives $\begin{bmatrix}6510758&3254867\\6509734&3255891\end{bmatrix}$, matching $A^{10}$ computed by repeated multiplication ✓ *(both verified).*
>
> **Note the $5^n$ term dominates**: $A^{10}$ has all entries close to $\tfrac{5^{10}}3\begin{bmatrix}2&1\\2&1\end{bmatrix}$, and the columns are nearly proportional to the dominant eigenvector $(1,1)$. **That is the dynamical-system statement made numerical.**
>
> **(iii)** $c_B(x)=(x-2)^2$, so $\lambda=2$ is the only eigenvalue, with multiplicity 2. But
> $$2I-B=\begin{bmatrix}0&-1\\0&0\end{bmatrix}$$
> has rank 1, so its null space is **one**-dimensional: the eigenspace is spanned by $(1,0)$ alone. **Two eigenvalues' worth of multiplicity, one eigenvector — no invertible $P$ exists.** *(Verified.)*
>
> **A cleaner argument: if $B=PDP^{-1}$ with $D=2I$, then $B=P(2I)P^{-1}=2I$ — but $B\ne2I$.** **Any matrix with a single repeated eigenvalue is diagonalizable only if it is already diagonal.**
>
> **(iv)** $c_C(x)=x^2+1$, which has **no real roots**. So $C$ has no real eigenvalues and no real eigenvectors.
>
> **$C$ is rotation by $90°$** ([[02 - Matrix Algebra|ch. 02 §2b]]) — **and a rotation leaves no direction fixed, which is precisely what "no real eigenvector" means.** *(Over $\mathbb{C}$ the eigenvalues are $\pm i$, and the matrix is diagonalizable there; §8.6 develops this.)*
>
> > [!important] The two ways diagonalization fails
> > | Failure | Example | Cause |
> > |---|---|---|
> > | **Too few eigenvectors** | $\begin{bmatrix}2&1\\0&2\end{bmatrix}$ | a shear: one invariant line, algebraic multiplicity 2 |
> > | **No real eigenvalues** | $\begin{bmatrix}0&-1\\1&0\end{bmatrix}$ | a rotation: no invariant line at all |
> >
> > **The second failure disappears over $\mathbb{C}$; the first does not.** Chapter 8's spectral theorem rules out both for **symmetric** matrices — which is why covariance matrices, Gram matrices and Hessians are always diagonalizable, and why PCA is possible.

> [!question] Exercise 5 — dynamical systems and recurrences *(hard)*
> **(a)** Fibonacci: $F_0=0$, $F_1=1$, $F_{k+2}=F_{k+1}+F_k$.
> (i) Write it as $\mathbf v_{k+1}=A\mathbf v_k$ with $\mathbf v_k=(F_{k+1},F_k)^{\mathsf T}$, and find $A$.
> (ii) Find the eigenvalues, and relate the characteristic polynomial to the recurrence.
> (iii) Derive **Binet's formula** $F_n=\dfrac{\varphi^n-\psi^n}{\sqrt5}$ and check it at $n=10$ and $n=20$.
> (iv) Explain why $F_{n+1}/F_n\to\varphi$.
>
> **(b)** A population of birds is modelled by $\mathbf v_{k+1}=A\mathbf v_k$ where $A$ has eigenvalues $1.2$ and $0.4$. Without further information, describe the long-run behaviour, and say what would change if the eigenvalues were $0.9$ and $0.4$, or $1$ and $0.4$.

> [!example]- Solution
> **(a)(i)** $F_{k+2}=F_{k+1}+F_k$ and $F_{k+1}=F_{k+1}$, so
> $$\begin{bmatrix}F_{k+2}\\F_{k+1}\end{bmatrix}=\underbrace{\begin{bmatrix}1&1\\1&0\end{bmatrix}}_{A}\begin{bmatrix}F_{k+1}\\F_k\end{bmatrix},\qquad \mathbf v_0=\begin{bmatrix}1\\0\end{bmatrix}$$
> **The second row is a trivial identity, included only to make the system first-order** — the standard device for turning any order-$k$ recurrence into a $k\times k$ matrix iteration.
>
> **(ii)** $c_A(x)=x^2-x-1$, with roots
> $$\varphi=\frac{1+\sqrt5}2=1.618034,\qquad \psi=\frac{1-\sqrt5}2=-0.618034$$
> *(Verified.)*
>
> **$c_A(x)=x^2-x-1$ is exactly the recurrence $x^2=x+1$** — substituting a trial solution $x_k=r^k$ into $x_{k+2}=x_{k+1}+x_k$ gives $r^2=r+1$. **The "characteristic equation" of a recurrence and the characteristic polynomial of its companion matrix are the same object**, which is why the two methods always agree.
>
> **(iii)** Distinct eigenvalues, so $A$ is diagonalizable; write $\mathbf v_0=c_1\mathbf x_1+c_2\mathbf x_2$ with $\mathbf x_1=(\varphi,1)$, $\mathbf x_2=(\psi,1)$. Then
> $$\mathbf v_n=c_1\varphi^n\mathbf x_1+c_2\psi^n\mathbf x_2$$
> Solving $\mathbf v_0=(1,0)$: $c_1\varphi+c_2\psi=1$ and $c_1+c_2=0$, so $c_2=-c_1$ and $c_1(\varphi-\psi)=1$; since $\varphi-\psi=\sqrt5$, $c_1=\tfrac1{\sqrt5}$. Reading the second component ($F_n$):
> $$\boxed{F_n=\frac{\varphi^n-\psi^n}{\sqrt5}}$$
> **Checks:** $n=10$ gives $55$ and $n=20$ gives $6765$ — matching $A^{10}=\begin{bmatrix}89&55\\55&34\end{bmatrix}$ and the Fibonacci sequence ✓ *(both verified).*
>
> **The formula is startling: an expression full of $\sqrt5$ returns an integer for every $n$.** It does so because the irrational parts of $\varphi^n$ and $\psi^n$ cancel exactly.
>
> **(iv)** Since $|\psi|=0.618<1<\varphi$, the $\psi^n$ term vanishes and
> $$F_n\approx\frac{\varphi^n}{\sqrt5}\quad\Longrightarrow\quad \frac{F_{n+1}}{F_n}\to\varphi$$
> **The golden ratio is the dominant eigenvalue, and nothing else.** *(In fact $|\psi^n/\sqrt5|<\tfrac12$ for all $n\ge0$, so $F_n$ is simply the nearest integer to $\varphi^n/\sqrt5$.)*
>
> **(b)** Write $\mathbf v_0=c_1\mathbf x_1+c_2\mathbf x_2$; then $\mathbf v_k=c_1\lambda_1^k\mathbf x_1+c_2\lambda_2^k\mathbf x_2$.
>
> | Eigenvalues | Long-run behaviour |
> |---|---|
> | $1.2,\ 0.4$ | **Growth at 20% per period.** The $0.4^k$ term dies, so $\mathbf v_k\approx c_1(1.2)^k\mathbf x_1$ — **the population grows geometrically and its *composition* converges to the direction of $\mathbf x_1$**, whatever the starting mix. |
> | $0.9,\ 0.4$ | **Extinction.** Both $|\lambda|<1$, so $\mathbf v_k\to\mathbf 0$ — at rate $0.9^k$, since the larger eigenvalue is the slower decay. |
> | $1,\ 0.4$ | **A steady state.** $\mathbf v_k\to c_1\mathbf x_1$, a fixed nonzero population. **This is the Markov case** ([[02 - Matrix Algebra|ch. 02 §8]]), and $\mathbf x_1$ is the stationary vector. |
>
> > [!important] The dominant eigenvalue is the whole story, and the second one sets the clock
> > **$|\lambda_{\max}|$ against 1 decides growth, stability or extinction; $\mathbf x_{\max}$ decides the eventual *shape*; and $|\lambda_2/\lambda_1|$ decides how fast that shape is reached.**
> >
> > **This one framework covers population models, Markov chains, PageRank, power iteration, and the convergence of MCMC.** It is also the reason a model's qualitative conclusion ("the species survives") can hinge on whether a computed eigenvalue is $0.99$ or $1.01$ — **which is exactly why sensitivity of eigenvalues to the data matters.**

---

## 📝 Summary

- **The determinant is defined recursively by cofactor expansion**, and Theorem 1 says every row and column gives the same answer — so **expand along the line with the most zeros.**
- **The five properties (Theorem 2):** a zero row gives $0$; interchanging rows negates; scaling a row scales; two equal rows give $0$; **adding a multiple of one row to another changes nothing.**
- **Compute determinants by row reduction, not cofactor expansion:** $O(n^3)$ against $O(n!)$. **Triangular determinants are products of diagonal entries**, and block-triangular ones factor as $\det A\det B$.
- **$\det(uA)=u^n\det A$**, $\det(A^{\mathsf T})=\det A$, and $\boxed{\det(AB)=\det A\det B}$ — **multiplicative, never additive.**
- **$A$ is invertible $\iff\det A\ne0$**, with $\det(A^{-1})=1/\det A$. **The adjugate formula and Cramer's rule are formulas, not algorithms** — exponentially more expensive than elimination.
- **Geometrically $|\det|$ is an area/volume scaling factor and its sign is orientation**, which makes every property of Theorem 2 visually obvious — especially the shear invariance behind property 5.
- **$A\mathbf x=\lambda\mathbf x$ asks for directions $A$ does not turn.** Eigenvalues are the roots of $c_A(x)=\det(xI-A)$; eigenvectors are the nonzero solutions of $(\lambda I-A)\mathbf x=\mathbf 0$. **The $\lambda$-eigenspace is the null space of $\lambda I-A$.**
- **Free checks: $\sum\lambda_i=\operatorname{tr}A$ and $\prod\lambda_i=\det A$.** For $2\times2$, the eigenvalues are the roots of $x^2-(\operatorname{tr}A)x+\det A$.
- **$A$ is diagonalizable $\iff$ it has $n$ independent eigenvectors**, and then $P=[\mathbf x_1\ \cdots\ \mathbf x_n]$, $D=\operatorname{diag}(\lambda_i)$. **Verify with $AP=PD$, which needs no inverse.**
- **$n$ distinct eigenvalues $\Rightarrow$ diagonalizable, but the converse is false.** The real criterion is $\dim(\text{eigenspace})=$ multiplicity for every $\lambda$. **A repeated eigenvalue is a warning, not a verdict.**
- **Diagonalization fails in two ways: too few eigenvectors (a shear) or no real eigenvalues (a rotation).** Complexifying fixes the second only. **Chapter 8 shows symmetric matrices suffer neither.**
- **$A^k=PD^kP^{-1}$ is why any of this matters.** For $\mathbf v_{k+1}=A\mathbf v_k$,
$$\mathbf v_k=\sum_i c_i\lambda_i^k\mathbf x_i$$
**and the dominant $|\lambda|$ decides growth ($>1$), steady state ($=1$) or extinction ($<1$)**, while $|\lambda_2/\lambda_1|$ sets the convergence rate.
- **A linear recurrence is a matrix iteration**, and its characteristic equation is the companion matrix's characteristic polynomial. **Binet's formula for Fibonacci is diagonalization applied to $\begin{bmatrix}1&1\\1&0\end{bmatrix}$.**

---

## ⚠️ Important Notes

> [!warning] $\det(A+B)\ne\det A+\det B$
> **The determinant is multiplicative, not additive.** $A=\left[\begin{smallmatrix}1&2\\3&4\end{smallmatrix}\right]$, $B=\left[\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right]$ give $-2$, $-1$ and $\det(A+B)=-8$.
>
> **What *is* true is far weaker:** $\det$ is linear in each column **separately, with the others held fixed** (Theorem 6, §3.1). **Do not upgrade that to additivity in the matrix.**
>
> **Related trap: $\det(kA)=k^n\det A$, not $k\det A$** — scaling the matrix scales all $n$ rows.

> [!warning] Cofactor expansion is a definition, not a method
> | $n$ | Cofactor expansion ($\approx n!$) | Row reduction ($\approx n^3/3$) |
> |---|---|---|
> | 5 | 120 | 42 |
> | 10 | 3,628,800 | 333 |
> | 20 | $2.4\times10^{18}$ | 2,700 |
>
> **Use cofactors for $n\le3$, for sparse rows, and for proofs. Use row reduction for everything else.** The same warning applies to $\operatorname{adj}A$ and Cramer's rule — **elegant closed forms, catastrophic algorithms.**

> [!warning] Repeated eigenvalues do not settle anything
> $$\begin{bmatrix}0&1&1\\1&0&1\\1&1&0\end{bmatrix}\ \text{is diagonalizable};\qquad \begin{bmatrix}2&1\\0&2\end{bmatrix}\ \text{is not}$$
> **Both have a repeated eigenvalue.** The deciding question is always
> $$\dim(\text{eigenspace for }\lambda)\ \overset{?}{=}\ \text{multiplicity of }\lambda\text{ in }c_A(x)$$
> and the left side is $n-\operatorname{rank}(\lambda I-A)$. **Compute that rank; do not guess from the polynomial.**
>
> **Geometric multiplicity is never greater than algebraic multiplicity**, so failure always means "too few eigenvectors", never too many.

> [!warning] Real matrices can have no real eigenvalues
> $c_A(x)=x^2+1$ for $\begin{bmatrix}0&-1\\1&0\end{bmatrix}$ — **rotation by $90°$ fixes no direction, so there is nothing for a real eigenvector to be.**
>
> **Every $n\times n$ real matrix has $n$ complex eigenvalues (with multiplicity), and complex ones come in conjugate pairs** — a real $3\times3$ therefore always has at least one real eigenvalue, but a real $2\times2$ need not.
>
> **This is why $\mathbb{C}$ eventually becomes unavoidable** (§8.6), and why chapter 8's guarantee that *symmetric matrices have all-real eigenvalues* is a genuine theorem rather than a convenience.

> [!warning] Two conventions for the characteristic polynomial
> $$\text{Nicholson: } c_A(x)=\det(xI-A)\qquad\text{Many others: }\det(A-xI)$$
> **They differ by $(-1)^n$**, so the polynomials differ in sign for odd $n$ while the **roots are identical**. Nicholson's is monic.
>
> **If your polynomial disagrees with a reference by an overall sign, this is almost always why** — check before hunting for an arithmetic error.

> [!warning] Diagonalization is a change of coordinates, and $P$ is not unique
> $P^{-1}AP=D$ says: **in the basis of eigenvectors, $A$ is just $n$ independent scalings.**
>
> **$P$ is far from unique** — you may reorder its columns (permuting $D$ correspondingly) and rescale each column by any nonzero constant. **So "the" diagonalizing matrix does not exist, and an answer differing from the book by column order or scaling is still correct.** Check by $AP=PD$, not by comparison.

> [!warning] Eigenvalues can be very sensitive to the entries
> Nicholson's own warning is worth repeating: **the exercises are rigged so that $c_A$ has integer roots, and real matrices are not.** Root-finding for a degree-$n$ polynomial is itself ill-conditioned, so **computing eigenvalues via the characteristic polynomial is numerically the *worst* available method** — §8.5 and practical software use iterative algorithms (QR iteration) instead.
>
> **This matters for conclusions, not just for arithmetic.** In Exercise 5(b) the qualitative outcome flips between "extinction" and "unbounded growth" as the dominant eigenvalue crosses 1. **A model whose answer depends on the third decimal place of an eigenvalue is telling you something about the model.**

> [!note] Cross-subject connections
> - [[02 - Matrix Algebra|Ch. 02]] — **$\det A\ne0$ joins the Inverse Theorem**, as does "0 is not an eigenvalue"; §2.9's Markov steady state is an eigenvector for $\lambda=1$, and its convergence rate is the second eigenvalue.
> - [[04 - Vector Geometry|Ch. 04]] — determinants **are** areas and volumes there, and the cross product is a determinant.
> - [[05 - The Vector Space Rn|Ch. 05]] — "$n$ independent eigenvectors" gets its proper definition; **§5.5 redoes diagonalization with the machinery this chapter had to do without.**
> - [[08 - Orthogonality|Ch. 08]] — **the spectral theorem: every symmetric matrix is diagonalizable, with real eigenvalues and an *orthonormal* eigenbasis.** Both failure modes of this chapter vanish, which is what makes PCA work.
> - [[Probability Theory/contents/09 - Additional Topics in Probability|Probability ch. 09]] — a Markov chain's stationary distribution is an eigenvector for $\lambda=1$; **the spectral gap $|\lambda_2|$ is the mixing rate**, exactly as in Exercise 5(b).
> - [[Time-series Analysis/contents/00-Index|Time-series Analysis]] — an AR($p$) process is a linear recurrence with noise, and **stationarity is precisely the condition that all roots of the characteristic polynomial lie inside the unit circle** — Exercise 5(b) with $|\lambda|<1$.
> - [[Calculus/contents/00-Index|Calculus]] — $\det$ of the Jacobian is the volume factor in change of variables; the Hessian is symmetric, so ch. 8 applies to it.
> - [[Optimization/contents/00-Index|Optimization]] — **the eigenvalues of the Hessian classify critical points** (all positive $\Rightarrow$ minimum), and their ratio is the condition number governing how fast gradient descent converges.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **PageRank is power iteration for the dominant eigenvector**; PCA is the eigendecomposition of a covariance matrix; the spectral radius controls whether a recurrent network's gradients explode or vanish.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **A structural gap the text creates for itself.** Nicholson places diagonalization in chapter 3 "as requested by our Engineering Faculty" so that it needs only determinants and inverses. **But Theorem 4 requires the matrix $P=[\mathbf x_1\ \cdots\ \mathbf x_n]$ to be invertible, and the natural criterion — that the eigenvectors be *independent* — cannot be stated**, because independence is not defined until §5.2. **The chapter works around this by talking about invertibility of $P$ rather than independence of its columns**, which is correct but obscures what is really going on, and §5.5 has to redo the whole topic. **Theorem 5 ("eigenvectors for distinct eigenvalues are independent") uses the word anyway**, two chapters before its definition.
>
> **PDF extraction — determinants suffer even more than matrices did in ch. 2:**
> - **Determinant bars, matrix brackets and row structure are all destroyed.** A displayed $3\times3$ determinant extracts as three lines of run-together digits with the minus signs migrated to the end of a row — e.g. $\left|\begin{smallmatrix}3&-1&2\\2&5&1\\0&0&0\end{smallmatrix}\right|$ becomes `31 2 / 25 1 / 00 0 −`.
> - **I could not reliably reconstruct the $4\times4$ matrix of §3.1 Example 10.** The extraction reads `231 3 / 121 1 / 01 0 1 / 040 1` with two stray minus signs, and the candidate reconstructions I tested give $-15$ and $+9$ rather than the printed $-9$. **What *is* verifiable is the arithmetic Nicholson shows: $-\left|\begin{smallmatrix}2&1\\1&-1\end{smallmatrix}\right|\cdot\left|\begin{smallmatrix}1&1\\4&1\end{smallmatrix}\right|=-(-3)(-3)=-9$, and both $2\times2$ determinants are indeed $-3$** ✓. **I have therefore presented Theorem 5 and its use rather than the unreconstructable example.**
> - **Superscripts detach**, so $u^n\det A$ appears as `undet A` in Theorem 3 — which reads as a word and is easy to misparse.
> - **Greek letters survive but subscripts do not:** $\lambda_1I-A$ extracts as a column of `λ`s with the subscripts on separate lines.
> - **`S … T` are large brackets, `/bbR` is $\mathbb{R}$, `/cdots` is $\cdots$, `/uni25ba.001` marks a solution.**
> - **All figures are images.** Chapter 3's include the geometric picture of $\mathbb{R}\mathbf x$ being $A$-invariant (§3.3's rewritten eigenvector example, which the preface singles out as new in this edition), the bird-population diagrams, and the phase pictures for §3.5's differential equations. **The $A$-invariant-line picture is the chapter's best intuition for what an eigenvector is, and it is lost.**
>
> **Verification performed:** every worked example quoted was independently recomputed. Confirmed: the Vandermonde formula at $(1,2,4)$ giving $6=(1)(3)(2)$ (§3.1 Ex. 8); **both $2\times2$ determinants and the final $-9$ in the block computation** (§3.1 Ex. 10); $c_A(x)=x^2-2x-8$, eigenvalues $4,-2$ and **both eigenvectors by direct multiplication** (§3.3 Ex. 3); **all three eigenvalues, $\det A=-2$, and all three eigenvectors of $\left[\begin{smallmatrix}2&0&0\\1&2&-1\\1&3&-2\end{smallmatrix}\right]$** (§3.3 Ex. 4, 8); and the eigenvalues $2,-1,-1$ of $\left[\begin{smallmatrix}0&1&1\\1&0&1\\1&1&0\end{smallmatrix}\right]$ (§3.3 Ex. 9). **All agree with the text.** Every exercise figure in these notes — including the closed form for $A^n$, checked at $n=1$ and $n=10$ against direct matrix powers, and Binet's formula checked at $n=1,2,5,10,20$ — was verified before being written down.
>
> **Scope note:** §3.6 (the proof of the cofactor expansion theorem) is omitted — it is a technical induction that Nicholson himself defers to the end of the chapter, and nothing later depends on the proof rather than the statement. **§3.4 (linear recurrences) and §3.5 (systems of differential equations) are kept in summary form and folded into §3c above**, because they are the *same* theorem — $\mathbf v_k=\sum c_i\lambda_i^k\mathbf x_i$ in discrete time, $\mathbf v(t)=\sum c_ie^{\lambda_it}\mathbf x_i$ in continuous time — and presenting them as two topics obscures that. **The Google PageRank discussion inside §3.3 is noted where it belongs, as power iteration for a dominant eigenvector.**

#linear-algebra #determinant #cofactor-expansion #eigenvalue #eigenvector #diagonalization #dynamical-system #linear-recurrence
