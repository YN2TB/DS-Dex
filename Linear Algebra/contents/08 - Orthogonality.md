---
subject: Linear Algebra
chapter: 08
tags: [ds, linear-algebra, orthogonality, gram-schmidt, spectral-theorem, positive-definite, qr-factorization, pca]
source: "Nicholson, *Linear Algebra with Applications*, 7th ed., ch. 8 (pp. 368–435)"
---

# Orthogonality

> [!abstract] What this chapter is for
> **This is the payoff chapter, and the one a data-science reader cannot skip.**
>
> Chapter 5 showed that orthogonal bases are enormously convenient — coordinates become dot products, projections become formulas, variances add. **It did not say where to get one.** This chapter answers that (Gram–Schmidt), and then proves something far stronger:
>
> $$\boxed{\ A=A^{\mathsf T}\ \Longrightarrow\ A=PDP^{\mathsf T}\ \text{with }P\text{ orthogonal and }D\text{ real diagonal}\ }$$
>
> **Every symmetric matrix has an orthonormal basis of its own eigenvectors.** Both ways diagonalization failed in [[03 - Determinants and Diagonalization|ch. 03]] — too few eigenvectors, or no real ones — are impossible for symmetric matrices. **And covariance matrices, Gram matrices $A^{\mathsf T}A$, Hessians and adjacency matrices of undirected graphs are all symmetric**, which is why this one theorem does so much work.
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | **Orthogonal complements, projections, Gram–Schmidt** | Project onto a *subspace*; manufacture orthogonal bases |
> | **2** | **The Principal Axis / spectral theorem** | symmetric $\iff$ orthogonally diagonalizable |
> | **3** | **Positive definite matrices** | $\mathbf x^{\mathsf T}A\mathbf x>0$; leading minors; **Cholesky** |
> | **4** | **QR-factorization** | Gram–Schmidt written as a matrix identity |
> | **10** | **Principal Component Analysis** | The spectral theorem applied to a covariance matrix |
>
> **§8.10 is where the whole book has been heading for a data-science reader**, and it is four pages long. Everything before it is the machinery it needs.

---

## 📘 Main Knowledge

### 1. Orthogonal complements, projections, Gram–Schmidt

> [!important] Definition 8.1 — orthogonal complement
> For a subspace $U\subseteq\mathbb{R}^n$,
> $$U^\perp=\{\mathbf x\in\mathbb{R}^n:\mathbf x\cdot\mathbf u=0\text{ for all }\mathbf u\in U\}$$
> **$U^\perp$ is a subspace**, and it suffices to check orthogonality against a spanning set of $U$.

> [!important] Definition 8.2 and Theorem 3 (§8.1) — the Projection Theorem
> If $\{\mathbf f_1,\dots,\mathbf f_m\}$ is an **orthogonal** basis of $U$, define
> $$\operatorname{proj}_U(\mathbf x)=\frac{\mathbf x\cdot\mathbf f_1}{\|\mathbf f_1\|^2}\mathbf f_1+\cdots+\frac{\mathbf x\cdot\mathbf f_m}{\|\mathbf f_m\|^2}\mathbf f_m$$
> Then:
> 1. $\mathbf p=\operatorname{proj}_U(\mathbf x)\in U$ and $\mathbf x-\mathbf p\in U^\perp$;
> 2. **$\mathbf p$ is the unique closest point of $U$ to $\mathbf x$:** $\|\mathbf x-\mathbf p\|<\|\mathbf x-\mathbf y\|$ for every other $\mathbf y\in U$.

**Part 2's proof is Pythagoras in one line.** Write $\mathbf x-\mathbf y=(\mathbf x-\mathbf p)+(\mathbf p-\mathbf y)$; the two pieces are orthogonal, so

$$\|\mathbf x-\mathbf y\|^2=\|\mathbf x-\mathbf p\|^2+\|\mathbf p-\mathbf y\|^2>\|\mathbf x-\mathbf p\|^2$$

> [!important] The formula does not depend on which orthogonal basis you use
> **This needs proving and Nicholson proves it.** If $\mathbf p'$ came from another orthogonal basis, then $\mathbf p-\mathbf p'$ lies in $U$ (both terms do) **and** in $U^\perp$ (both $\mathbf x-\mathbf p$ and $\mathbf x-\mathbf p'$ do), so it is **orthogonal to itself** and therefore $\mathbf 0$.
>
> **"Orthogonal to itself hence zero" is the standard move of the whole chapter** — it is the only way $\|\mathbf v\|^2=\mathbf v\cdot\mathbf v=0$ can happen.

**Theorem 4 (§8.1)** collects the consequences: $T(\mathbf x)=\operatorname{proj}_U(\mathbf x)$ is a **linear operator** with

$$\operatorname{im}T=U,\qquad \ker T=U^\perp,\qquad \boxed{\dim U+\dim U^\perp=n}$$

**The last is the dimension theorem** ([[07 - Linear Transformations|ch. 07]]) applied to the projection — and it says $\mathbb{R}^n=U\oplus U^\perp$: every vector splits **uniquely** into a piece in $U$ and a piece perpendicular to it.

> [!example] Example 3 (§8.1)
> $U=\operatorname{span}\{(1,1,0,1),(0,1,1,2)\}$, $\mathbf x=(3,-1,0,2)$. The spanning vectors are **not** orthogonal, so first orthogonalise:
> $$\mathbf f_1=(1,1,0,1),\qquad \mathbf f_2=(0,1,1,2)-\tfrac33\mathbf f_1=(-1,0,1,1)$$
> Then
> $$\mathbf p=\tfrac43\mathbf f_1-\tfrac13\mathbf f_2=\tfrac13(5,4,-1,3),\qquad \mathbf x-\mathbf p=\tfrac13(4,-7,1,3)$$
> *(Verified.)* **The projection formula requires an orthogonal basis — that is exactly why Gram–Schmidt is needed.**

> [!important] The Gram–Schmidt algorithm
> Given any basis $\{\mathbf x_1,\dots,\mathbf x_m\}$ of $U$, set
> $$\mathbf f_1=\mathbf x_1,\qquad \mathbf f_k=\mathbf x_k-\sum_{j<k}\frac{\mathbf x_k\cdot\mathbf f_j}{\|\mathbf f_j\|^2}\mathbf f_j$$
> Then $\{\mathbf f_1,\dots,\mathbf f_m\}$ is an **orthogonal** basis of $U$, and $\operatorname{span}\{\mathbf f_1,\dots,\mathbf f_k\}=\operatorname{span}\{\mathbf x_1,\dots,\mathbf x_k\}$ for every $k$.

> [!tip] What the algorithm is doing
> **At each step, subtract off everything already accounted for.** $\mathbf f_k$ is $\mathbf x_k$ minus its projection onto the span of the previous vectors — so what remains is exactly the genuinely new direction.
>
> **The nesting property matters:** the first $k$ output vectors span the same subspace as the first $k$ inputs. **That is what makes QR possible** (§4), and it means the algorithm can be run incrementally as new vectors arrive.
>
> **Rescale freely.** Multiplying any $\mathbf f_k$ by a nonzero constant keeps everything orthogonal and clears fractions — Example 3 above and Exercise 2 both use this.

---

### 2. Orthogonal matrices and the spectral theorem

> [!important] Definition 8.3 — orthogonal matrix
> A square $P$ is **orthogonal** if $P^{\mathsf T}P=I$, i.e. $\ P^{-1}=P^{\mathsf T}$.
>
> **Equivalently: the columns of $P$ are orthonormal.** (And then so are the rows.)

> [!warning] "Orthogonal matrix" means **orthonormal** columns, not merely orthogonal ones
> **The name is a historical misnomer and it catches everyone once.** Nicholson's Example 2 gives $\left[\begin{smallmatrix}2&1&1\\1&-1&1\\0&1&-1\end{smallmatrix}\right]$-type matrices with orthogonal rows that are **not** orthogonal matrices; **normalising the rows is what fixes it.**
>
> **After normalising, the columns become orthonormal too** — which is not obvious and is a consequence of $P^{\mathsf T}P=I\Rightarrow PP^{\mathsf T}=I$ for square matrices ([[02 - Matrix Algebra|ch. 02]] Corollary 1).

**Properties:** products and inverses of orthogonal matrices are orthogonal; $\det P=\pm1$; and **orthogonal matrices are exactly the distance-preserving linear operators**, $\|P\mathbf x\|=\|\mathbf x\|$ — the rotations and reflections of [[04 - Vector Geometry|ch. 04]].

> [!important] Definition 8.4 and Theorem 2 (§8.2) — the Principal Axis Theorem
> For an $n\times n$ real matrix $A$ the following are **equivalent**:
> 1. $A$ has an **orthonormal set of $n$ eigenvectors**;
> 2. $A$ is **orthogonally diagonalizable**: $P^{\mathsf T}AP=D$ with $P$ orthogonal;
> 3. **$A$ is symmetric.**
>
> **Also called the real spectral theorem.** A set of orthonormal eigenvectors is a set of **principal axes**, and the set of distinct eigenvalues is the **spectrum**.

> [!important] Why this theorem is the climax of the book
> **Symmetry — a condition you can check by eye — guarantees the best possible diagonalization.** Compare with [[03 - Determinants and Diagonalization|ch. 03]]:
>
> | Failure mode in ch. 3 | Example | For symmetric $A$ |
> |---|---|---|
> | Too few eigenvectors | $\left[\begin{smallmatrix}2&1\\0&2\end{smallmatrix}\right]$ | **impossible** |
> | No real eigenvalues | $\left[\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right]$ | **impossible** — all eigenvalues are real |
> | $P$ hard to invert | generic | **$P^{-1}=P^{\mathsf T}$, free** |
>
> **And eigenvectors for distinct eigenvalues are automatically orthogonal**, not merely independent: if $A\mathbf x=\lambda\mathbf x$, $A\mathbf y=\mu\mathbf y$ then
> $$\lambda(\mathbf x\cdot\mathbf y)=(A\mathbf x)\cdot\mathbf y=\mathbf x\cdot(A\mathbf y)=\mu(\mathbf x\cdot\mathbf y)$$
> using $A=A^{\mathsf T}$, so $(\lambda-\mu)(\mathbf x\cdot\mathbf y)=0$ forces $\mathbf x\cdot\mathbf y=0$. **Only within a repeated eigenvalue's eigenspace must you run Gram–Schmidt.**

**Reading $A=PDP^{\mathsf T}$ column by column gives the *spectral decomposition*:**

$$A=\lambda_1\mathbf p_1\mathbf p_1^{\mathsf T}+\lambda_2\mathbf p_2\mathbf p_2^{\mathsf T}+\cdots+\lambda_n\mathbf p_n\mathbf p_n^{\mathsf T}$$

— **a symmetric matrix is a weighted sum of projections onto its principal axes**, and dropping the small $\lambda_i$ gives the best low-rank approximation.

---

### 3. Positive definite matrices (§8.3)

> [!important] Definition 8.5
> A symmetric $A$ is **positive definite** if
> $$\mathbf x^{\mathsf T}A\mathbf x>0\qquad\text{for every }\mathbf x\ne\mathbf 0$$
> (**positive semi-definite** if $\ge0$).

> [!important] The equivalent characterisations
> For symmetric $A$, all of the following are equivalent:
> 1. $A$ is positive definite;
> 2. **every eigenvalue of $A$ is positive**;
> 3. $\det\big({}^{(r)}A\big)>0$ for each leading principal submatrix $r=1,\dots,n$;
> 4. $\boxed{A=U^{\mathsf T}U}$ with $U$ **upper triangular with positive diagonal** — the **Cholesky factorization**, which is unique.

**(1)$\iff$(2) is the spectral theorem:** with $A=PDP^{\mathsf T}$ and $\mathbf y=P^{\mathsf T}\mathbf x$,

$$\mathbf x^{\mathsf T}A\mathbf x=\mathbf y^{\mathsf T}D\mathbf y=\lambda_1y_1^2+\cdots+\lambda_ny_n^2$$

**which is positive for all $\mathbf y\ne\mathbf 0$ exactly when every $\lambda_i>0$.**

> [!important] The Cholesky algorithm
> **Step 1.** Row-reduce $A$ to upper triangular $U_1$ **using only "add a multiple of a row to a lower row"**.
> **Step 2.** Divide each row of $U_1$ by the square root of its diagonal entry.
>
> **That Step 1 never needs a row interchange is itself a consequence of positive definiteness** — and it is why Cholesky is about twice as fast as LU and numerically stable without pivoting.

> [!example] Example 2 (§8.3)
> $A=\begin{bmatrix}10&5&2\\5&3&2\\2&2&3\end{bmatrix}$ has leading minors $10,\ 5,\ 3$ — **all positive, so $A$ is positive definite**, with
> $$U=\begin{bmatrix}\sqrt{10}&\tfrac{5}{\sqrt{10}}&\tfrac{2}{\sqrt{10}}\\ 0&\tfrac1{\sqrt2}&\sqrt2\\ 0&0&\sqrt{3/5}\end{bmatrix}\approx\begin{bmatrix}3.162&1.581&0.632\\0&0.707&1.414\\0&0&0.775\end{bmatrix}$$
> *(Verified: $U^{\mathsf T}U=A$ exactly.)*

> [!tip] Where positive definiteness comes from, and why it is everywhere
> **$A^{\mathsf T}A$ is always positive *semi*-definite**, because $\mathbf x^{\mathsf T}A^{\mathsf T}A\mathbf x=\|A\mathbf x\|^2\ge0$ — and **positive definite exactly when the columns of $A$ are independent** ([[05 - The Vector Space Rn|ch. 05]], Exercise 5(b)).
>
> | Where it appears | Why it is PSD |
> |---|---|
> | **Covariance matrices** $\Sigma$ | $\mathbf a^{\mathsf T}\Sigma\mathbf a=\mathrm{Var}(\mathbf a^{\mathsf T}\mathbf X)\ge0$ |
> | **Gram matrices** $A^{\mathsf T}A$, kernel matrices | $=\|A\mathbf x\|^2\ge0$ |
> | **Hessians at a minimum** | second-order condition |
>
> **"Positive definite" is the matrix analogue of "positive number"** — it has a square root ($U$), its inverse is positive definite, and $\mathbf x^{\mathsf T}A\mathbf x$ is a genuine notion of "size". **That analogy is why a variance can never be negative and why a minimum needs a PD Hessian.**

---

### 4. QR-factorization (§8.4)

> [!important] Theorem 2 (§8.4)
> Every $m\times n$ matrix $A$ with **independent columns** factors as
> $$\boxed{\ A=QR\ }$$
> with $Q$ ($m\times n$) having **orthonormal columns** and $R$ ($n\times n$) **upper triangular with positive diagonal** — and the factorization is unique.

**$QR$ *is* Gram–Schmidt, written as a matrix identity.** The columns of $Q$ are the normalised Gram–Schmidt outputs; $R$ records the coefficients that were subtracted off. The nesting property of §1 is exactly why $R$ is triangular.

> [!important] Why QR replaces the normal equations
> Substituting $A=QR$ into $A^{\mathsf T}A\mathbf z=A^{\mathsf T}\mathbf b$ and using $Q^{\mathsf T}Q=I$:
> $$R^{\mathsf T}R\,\mathbf z=R^{\mathsf T}Q^{\mathsf T}\mathbf b\quad\Longrightarrow\quad \boxed{R\mathbf z=Q^{\mathsf T}\mathbf b}$$
> — **one triangular solve, and $A^{\mathsf T}A$ is never formed.**
>
> **That matters because forming $A^{\mathsf T}A$ squares the condition number**, so a merely awkward problem becomes an unsolvable one. **Every serious least-squares implementation uses QR (or the SVD), not the normal equations** — the formula $(X^{\mathsf T}X)^{-1}X^{\mathsf T}\mathbf y$ is how you *state* the answer, never how you compute it.

**§8.5 (computing eigenvalues)** adds the practical counterpart: the **QR algorithm** repeatedly factors $A_k=Q_kR_k$ and sets $A_{k+1}=R_kQ_k$, which converges to triangular form with the eigenvalues on the diagonal. **This, not the characteristic polynomial, is how eigenvalues are actually computed.**

---

### 5. Principal Component Analysis (§8.10)

**The whole chapter exists to make this work.**

> [!important] The setup
> Random variables $X_1,\dots,X_n$ with covariance matrix $\Sigma=[\sigma_{ij}]$, $\sigma_{ij}=\operatorname{cov}(X_i,X_j)$.
>
> **$\Sigma$ is symmetric, and positive semi-definite** — because for any $\mathbf a$,
> $$\mathbf a^{\mathsf T}\Sigma\mathbf a=\mathrm{Var}\!\left(\mathbf a^{\mathsf T}\mathbf X\right)\ge0$$
> **A variance cannot be negative; that *is* the positive-semi-definiteness of $\Sigma$.**

> [!important] The construction
> By the Principal Axis Theorem there is an orthogonal $P$ with
> $$P^{\mathsf T}\Sigma P=\operatorname{diag}(\lambda_1,\dots,\lambda_n),\qquad \lambda_1\ge\lambda_2\ge\cdots\ge\lambda_n\ge0$$
> Define the **principal components** $\mathbf Y=P^{\mathsf T}\mathbf X$. Then
> $$\operatorname{cov}(Y_i,Y_j)=0\ (i\ne j),\qquad \mathrm{Var}(Y_i)=\lambda_i$$
>
> **The $Y_i$ are uncorrelated linear combinations of the $X_i$, with variances exactly the eigenvalues.**

> [!important] Why the variances add up
> **Similar matrices have the same trace** ([[05 - The Vector Space Rn|ch. 05 §5]]), so
> $$\underbrace{\sigma_{11}+\cdots+\sigma_{nn}}_{\text{total variance of the }X_i}=\underbrace{\lambda_1+\cdots+\lambda_n}_{\text{total variance of the }Y_i}$$
> **The transformation redistributes variance without creating or destroying any.** Since $\lambda_1\ge\cdots\ge\lambda_n$, most of it sits in the first few components — **so keeping those few loses little, and that is the entire method.**
>
> **"PC1 explains 80% of the variance" means $\lambda_1/\sum\lambda_i=0.8$.** The statement is only meaningful because the components are **orthogonal**, so their variances add with no double counting ([[05 - The Vector Space Rn|ch. 05]], Exercise 4(iv)).

> [!warning] Two things §8.10 does not say
> - **It is a covariance-matrix eigendecomposition, which is the numerically inferior route.** Forming $\Sigma$ from a data matrix $X$ squares the condition number, exactly as with the normal equations. **In practice PCA is computed by the SVD of the centred data matrix** — and **the SVD does not appear anywhere in Nicholson.** See [[00-Index]].
> - **PCA is scale-dependent.** Multiplying a variable by 1000 multiplies its variance by $10^6$ and it will dominate PC1. **Standardising first (using the correlation matrix instead of $\Sigma$) is usually necessary**, and the choice is a modelling decision the linear algebra cannot make for you.

**Related applications:** **§8.8 quadratic forms** — every $q(\mathbf x)=\mathbf x^{\mathsf T}A\mathbf x$ becomes $\sum\lambda_iy_i^2$ in principal axes, which classifies conics and quadric surfaces and gives the second-derivative test. **§8.9 constrained optimization** — $\max\{\mathbf x^{\mathsf T}A\mathbf x:\|\mathbf x\|=1\}=\lambda_{\max}$, attained at the corresponding unit eigenvector, **which is exactly why PC1 is the maximum-variance direction.**

---

## ✏️ Exercises

> [!question] Exercise 1 — complements and projections *(warm-up)*
> Let $U=\operatorname{span}\{(1,1,0),(1,0,1)\}\subseteq\mathbb{R}^3$.
> (i) Find $U^\perp$ and verify $\dim U+\dim U^\perp=3$.
> (ii) Find $\operatorname{proj}_U(3,1,2)$ **after** orthogonalising a basis of $U$.
> (iii) Find the point of the plane $2x+y-z=0$ closest to $(2,-1,-3)$.

> [!example]- Solution
> **(i)** $\mathbf x\in U^\perp$ iff $x_1+x_2=0$ and $x_1+x_3=0$, i.e. $\mathbf x=t(1,-1,-1)$:
> $$U^\perp=\operatorname{span}\{(1,-1,-1)\},\qquad 2+1=3\ ✓$$
> **Note $U^\perp$ is the null space of the matrix whose *rows* span $U$** — which is why $\dim U+\dim U^\perp=n$ is rank–nullity in disguise.
>
> **(ii)** Orthogonalise: $\mathbf f_1=(1,1,0)$, and since $(1,0,1)\cdot\mathbf f_1=1$ with $\|\mathbf f_1\|^2=2$,
> $$\mathbf f_2=(1,0,1)-\tfrac12(1,1,0)=\tfrac12(1,-1,2)\ \longrightarrow\ (1,-1,2)$$
> With $\mathbf x=(3,1,2)$: $\mathbf x\cdot\mathbf f_1=4$, $\mathbf x\cdot\mathbf f_2=3+(-1)+4=6$, $\|\mathbf f_2\|^2=6$:
> $$\operatorname{proj}_U(\mathbf x)=\tfrac42(1,1,0)+\tfrac66(1,-1,2)=(2,2,0)+(1,-1,2)=\boxed{(3,1,2)}$$
> **The projection is $\mathbf x$ itself — so $\mathbf x\in U$.** *(Check: $(3,1,2)=2(1,1,0)+1(1,0,1)$ ✓, and $\mathbf x\cdot(1,-1,-1)=3-1-2=0$ ✓.)*
>
> **(iii)** The plane is $U'=\{(s,t,2s+t)\}=\operatorname{span}\{(0,1,1),(1,0,2)\}$. Orthogonalising: $\mathbf f_1=(0,1,1)$ and $\mathbf f_2=(1,0,2)-\tfrac22(0,1,1)=(1,-1,1)$.
> With $\mathbf x=(2,-1,-3)$: $\mathbf x\cdot\mathbf f_1=-4$, $\mathbf x\cdot\mathbf f_2=2+1-3=0$, so
> $$\operatorname{proj}_{U'}(\mathbf x)=-2(0,1,1)+0=\boxed{(0,-2,-2)}$$
> *(Verified.)* **The second coefficient vanishing means $\mathbf x$ already had no component along $\mathbf f_2$** — a coincidence of the numbers, but a useful reminder that a zero Fourier coefficient carries information.

> [!question] Exercise 2 — Gram–Schmidt
> (i) Apply Gram–Schmidt to $\{(1,1,0),(1,0,1),(0,1,1)\}$, rescaling to avoid fractions.
> (ii) Verify all three pairwise dot products.
> (iii) Normalise to get an orthonormal basis, and assemble the orthogonal matrix $P$.
> (iv) Why must the *first* vector be unchanged, and what would happen if you reordered the inputs?

> [!example]- Solution
> **(i)** $\mathbf f_1=(1,1,0)$, $\|\mathbf f_1\|^2=2$.
> $$\mathbf f_2=(1,0,1)-\tfrac12(1,1,0)=\left(\tfrac12,-\tfrac12,1\right)\ \longrightarrow\ (1,-1,2),\qquad \|\mathbf f_2\|^2=6$$
> $$\mathbf f_3=(0,1,1)-\tfrac12(1,1,0)-\tfrac16(1,-1,2)=\left(-\tfrac23,\tfrac23,\tfrac23\right)\ \longrightarrow\ \boxed{(-1,1,1)}$$
> *(Verified.)*
>
> **(ii)** $(1,1,0)\cdot(1,-1,2)=0$ ✓; $(1,1,0)\cdot(-1,1,1)=0$ ✓; $(1,-1,2)\cdot(-1,1,1)=-1-1+2=0$ ✓.
>
> **(iii)** $$P=\begin{bmatrix}\tfrac1{\sqrt2}&\tfrac1{\sqrt6}&-\tfrac1{\sqrt3}\\[2pt] \tfrac1{\sqrt2}&-\tfrac1{\sqrt6}&\tfrac1{\sqrt3}\\[2pt] 0&\tfrac2{\sqrt6}&\tfrac1{\sqrt3}\end{bmatrix}$$
> and $P^{\mathsf T}P=I$ — **columns of length 1 and pairwise orthogonal.**
>
> **(iv)** **$\mathbf f_1=\mathbf x_1$ because there is nothing yet to subtract.** The algorithm is inherently sequential and **its output depends on the input order**: starting with $(0,1,1)$ instead would give a different orthogonal basis spanning the same space.
>
> **The invariant that *is* order-independent is the nesting**: $\operatorname{span}\{\mathbf f_1,\dots,\mathbf f_k\}=\operatorname{span}\{\mathbf x_1,\dots,\mathbf x_k\}$ for each $k$. **That is what makes $R$ triangular in $A=QR$** — and it is also why numerical implementations reorder the columns (pivoting) for stability.

> [!question] Exercise 3 — orthogonal diagonalization
> (i) Orthogonally diagonalize $A=\begin{bmatrix}3&1\\1&3\end{bmatrix}$.
> (ii) Orthogonally diagonalize $B=\begin{bmatrix}2&1&1\\1&2&1\\1&1&2\end{bmatrix}$.
> (iii) Write $B$ in spectral form $\sum\lambda_i\mathbf p_i\mathbf p_i^{\mathsf T}$ and verify the $\lambda=4$ term.
> (iv) Explain why $C=\begin{bmatrix}1&2\\0&1\end{bmatrix}$ cannot be orthogonally diagonalized — **in one sentence.**

> [!example]- Solution
> **(i)** $c_A(x)=(x-3)^2-1=(x-4)(x-2)$, so $\lambda=4,2$ with eigenvectors $(1,1)$ and $(1,-1)$ — **already orthogonal**, since the eigenvalues differ.
> $$P=\tfrac1{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix},\qquad P^{\mathsf T}AP=\begin{bmatrix}4&0\\0&2\end{bmatrix}$$
> *(Verified.)*
>
> **(ii)** $B=I+J$ where $J$ is all-ones, so the eigenvalues are $1+3=4$ and $1+0=1$ (twice) — *(verified: $4,1,1$)*.
> - $\lambda=4$: $\mathbf p_1\propto(1,1,1)$.
> - $\lambda=1$: $B-I=J$ has rank 1, so the eigenspace is **2-dimensional** — $\{\mathbf x:x_1+x_2+x_3=0\}$. **Pick an orthogonal basis of it:** $(1,-1,0)$ and $(1,1,-2)$, which are orthogonal to each other and (automatically) to $(1,1,1)$.
> $$P=\begin{bmatrix}\tfrac1{\sqrt3}&\tfrac1{\sqrt2}&\tfrac1{\sqrt6}\\[2pt] \tfrac1{\sqrt3}&-\tfrac1{\sqrt2}&\tfrac1{\sqrt6}\\[2pt] \tfrac1{\sqrt3}&0&-\tfrac2{\sqrt6}\end{bmatrix},\qquad P^{\mathsf T}BP=\operatorname{diag}(4,1,1)$$
> *(All eigenvector claims verified: $B(1,1,1)=4(1,1,1)$, $B(1,-1,0)=(1,-1,0)$, $B(1,1,-2)=(1,1,-2)$.)*
>
> **The work is entirely inside the repeated eigenvalue.** Across distinct eigenvalues, orthogonality is free; within one eigenspace you must supply it yourself, by Gram–Schmidt or by inspection.
>
> **(iii)** With $\mathbf p_1=\tfrac1{\sqrt3}(1,1,1)$:
> $$4\,\mathbf p_1\mathbf p_1^{\mathsf T}=\tfrac43\begin{bmatrix}1&1&1\\1&1&1\\1&1&1\end{bmatrix}$$
> and the two $\lambda=1$ terms supply $I-\tfrac13J$, giving $\tfrac43J+I-\tfrac13J=I+J=B$ ✓
>
> **Notice $\tfrac43J$ alone is the best rank-1 approximation to $B$** — this is exactly what "keep the largest eigenvalues" means, and it is the finite-dimensional version of low-rank approximation.
>
> **(iv)** **$C$ is not symmetric**, and by the Principal Axis Theorem only symmetric matrices are orthogonally diagonalizable. *(In fact $C$ is not diagonalizable at all: $\lambda=1$ twice with a one-dimensional eigenspace.)*

> [!question] Exercise 4 — positive definiteness
> (i) Which are positive definite? $\ A=\begin{bmatrix}2&-1\\-1&2\end{bmatrix}$, $\ B=\begin{bmatrix}1&2\\2&1\end{bmatrix}$, $\ C=\begin{bmatrix}1&0\\0&0\end{bmatrix}$.
> (ii) Find the Cholesky factorization of $A$ and check it.
> (iii) Show that $A^{\mathsf T}A$ is positive semi-definite for **any** $A$, and positive definite iff the columns of $A$ are independent.
> (iv) A Hessian at a critical point is $H=\begin{bmatrix}4&2\\2&3\end{bmatrix}$. Classify the point.

> [!example]- Solution
> **(i)** Leading minors:
> - $A$: $2>0$ and $\det A=3>0$ — **positive definite.** *(Eigenvalues $1,3$.)*
> - $B$: $1>0$ but $\det B=1-4=-3<0$ — **not** positive definite. *(Eigenvalues $3,-1$: indefinite.)*
> - $C$: $1>0$ and $\det C=0$ — **positive semi-definite but not definite**, since $\mathbf x=(0,1)$ gives $\mathbf x^{\mathsf T}C\mathbf x=0$.
>
> *(All verified.)* **Note the minor test needs *strict* positivity at every stage; $C$ shows why.**
>
> **(ii)** Row-reduce with $R_2+\tfrac12R_1$: $\ U_1=\begin{bmatrix}2&-1\\0&\tfrac32\end{bmatrix}$. Divide each row by the square root of its diagonal entry:
> $$U=\begin{bmatrix}\sqrt2&-\tfrac1{\sqrt2}\\[2pt] 0&\sqrt{3/2}\end{bmatrix}\approx\begin{bmatrix}1.4142&-0.7071\\0&1.2247\end{bmatrix}$$
> **Check:** $U^{\mathsf T}U=\begin{bmatrix}2&-1\\-1&\tfrac12+\tfrac32\end{bmatrix}=\begin{bmatrix}2&-1\\-1&2\end{bmatrix}$ ✓ *(verified numerically too).*
>
> **(iii)** For any $\mathbf x$,
> $$\mathbf x^{\mathsf T}(A^{\mathsf T}A)\mathbf x=(A\mathbf x)^{\mathsf T}(A\mathbf x)=\|A\mathbf x\|^2\ge0$$
> so $A^{\mathsf T}A$ is PSD. It is **positive definite** iff $\|A\mathbf x\|^2>0$ for all $\mathbf x\ne\mathbf 0$, i.e. iff $A\mathbf x=\mathbf 0$ only for $\mathbf x=\mathbf 0$ — **iff the columns of $A$ are independent.** $\blacksquare$
>
> **This is the same computation as [[05 - The Vector Space Rn|ch. 05]]'s Exercise 5(b), and it explains three things at once:** why $X^{\mathsf T}X$ is invertible exactly when there is no perfect multicollinearity, why covariance matrices are PSD, and why kernel matrices in machine learning are PSD by construction.
>
> **(iv)** Leading minors $4>0$ and $\det H=12-4=8>0$, so **$H$ is positive definite** and the critical point is a **local minimum.**
>
> **The eigenvalues are $\tfrac{7\pm\sqrt{17}}2\approx5.56,\ 1.44$** — both positive, as they must be. **Their ratio $\approx3.9$ is the condition number, which controls how fast gradient descent converges**: a large ratio means a long narrow valley and slow zig-zagging progress ([[Optimization/contents/00-Index|Optimization]]).

> [!question] Exercise 5 — PCA *(hard)*
> **(a)** Two standardised variables have covariance matrix $\Sigma=\begin{bmatrix}5&3\\3&5\end{bmatrix}$.
> (i) Find the principal components and their variances.
> (ii) What proportion of total variance does PC1 explain?
> (iii) Interpret PC1 and PC2 in terms of the original variables.
>
> **(b)** Three variables have $\Sigma=\begin{bmatrix}4&2&0\\2&4&0\\0&0&1\end{bmatrix}$. Find the eigenvalues and the variance explained by the first two components.
>
> **(c)** (i) Show $\mathbf a^{\mathsf T}\Sigma\mathbf a=\mathrm{Var}(\mathbf a^{\mathsf T}\mathbf X)$, and deduce that $\Sigma$ is positive semi-definite.
> (ii) Show that $\max\{\mathbf a^{\mathsf T}\Sigma\mathbf a:\|\mathbf a\|=1\}=\lambda_1$, attained at the first eigenvector — **i.e. PC1 really is the maximum-variance direction.**

> [!example]- Solution
> **(a)(i)** $c_\Sigma(x)=(x-5)^2-9=(x-8)(x-2)$, so $\lambda_1=8$, $\lambda_2=2$ *(verified)*, with orthonormal eigenvectors
> $$\mathbf p_1=\tfrac1{\sqrt2}(1,1),\qquad \mathbf p_2=\tfrac1{\sqrt2}(1,-1)$$
> $$Y_1=\tfrac{X_1+X_2}{\sqrt2}\ \ (\mathrm{Var}=8),\qquad Y_2=\tfrac{X_1-X_2}{\sqrt2}\ \ (\mathrm{Var}=2)$$
>
> **(ii)** Total variance $=5+5=10=8+2$ ✓, so PC1 explains $\ \boxed{8/10=80\%}$.
>
> **(iii)** **$Y_1$ is the "size" or "average" component** — the two variables moving together — and it carries most of the variation. **$Y_2$ is the "contrast" component**, measuring how much they differ, and carries the rest.
>
> **This size/contrast split is the most common PCA outcome for positively correlated variables**, and it is worth recognising: PC1 is almost always "everything at once", PC2 the leading contrast.
>
> **(b)** The block structure splits the problem: $\begin{bmatrix}4&2\\2&4\end{bmatrix}$ has eigenvalues $6$ and $2$, and the $1\times1$ block gives $1$.
> $$\lambda=6,\ 2,\ 1;\qquad \text{total}=9=4+4+1\ ✓$$
> *(Verified.)* The first two components explain
> $$\frac{6+2}{9}=\boxed{88.9\%}$$
> **so dropping to two dimensions loses about 11% of the variance** — a typical justification for retaining two components.
>
> **(c)(i)** Writing $\mathbf X$ for the centred vector,
> $$\mathrm{Var}(\mathbf a^{\mathsf T}\mathbf X)=\mathbb{E}\big[(\mathbf a^{\mathsf T}\mathbf X)^2\big]=\mathbb{E}\big[\mathbf a^{\mathsf T}\mathbf X\mathbf X^{\mathsf T}\mathbf a\big]=\mathbf a^{\mathsf T}\mathbb{E}[\mathbf X\mathbf X^{\mathsf T}]\mathbf a=\mathbf a^{\mathsf T}\Sigma\mathbf a$$
> **A variance is never negative, so $\mathbf a^{\mathsf T}\Sigma\mathbf a\ge0$ for every $\mathbf a$ — which is the definition of positive semi-definite.** $\blacksquare$
>
> **This is the cleanest possible statement of why covariance matrices are PSD: it is not a technical condition, it is the impossibility of negative variance.** *(And it is not merely definite: $\Sigma$ is singular exactly when some linear combination of the variables is constant — perfect collinearity.)*
>
> **(c)(ii)** Write $\Sigma=PDP^{\mathsf T}$ and substitute $\mathbf y=P^{\mathsf T}\mathbf a$. Since $P$ is orthogonal, $\|\mathbf y\|=\|\mathbf a\|=1$, and
> $$\mathbf a^{\mathsf T}\Sigma\mathbf a=\mathbf y^{\mathsf T}D\mathbf y=\lambda_1y_1^2+\lambda_2y_2^2+\cdots+\lambda_ny_n^2$$
> With $\lambda_1\ge\lambda_i$ for all $i$ and $\sum y_i^2=1$,
> $$\sum_i\lambda_iy_i^2\le\lambda_1\sum_i y_i^2=\lambda_1$$
> **with equality iff all the weight is on $y_1$**, i.e. $\mathbf y=\mathbf e_1$, i.e. $\mathbf a=P\mathbf e_1=\mathbf p_1$. $\blacksquare$
>
> > [!important] This is the theorem that defines PCA
> > **PC1 is not "the eigenvector of $\Sigma$ for the largest eigenvalue" by definition — it is *the direction of maximum variance*, and this argument proves the two are the same thing.**
> >
> > **The rest follows by induction:** maximising over directions orthogonal to $\mathbf p_1$ gives $\lambda_2$ at $\mathbf p_2$, and so on. **So each principal component is the most informative direction remaining**, which is why the eigenvalues come out ordered and why truncating after $k$ components is optimal among all rank-$k$ projections.
> >
> > **Two independent things had to be true for this to work, and both are the spectral theorem:** $\Sigma$ has a *complete* set of eigenvectors (so $\mathbf y$ ranges over everything), and they are *orthonormal* (so $\|\mathbf y\|=\|\mathbf a\|$ and the variances add). **Neither holds for a general matrix.**

---

## 📝 Summary

- **$U^\perp$ is a subspace, $\dim U+\dim U^\perp=n$, and $\mathbb{R}^n=U\oplus U^\perp$** — every vector splits uniquely into a component in $U$ and one perpendicular to it.
- **The Projection Theorem:** with an orthogonal basis of $U$, $\operatorname{proj}_U(\mathbf x)$ is the **unique closest point of $U$ to $\mathbf x$**, and $\mathbf x-\operatorname{proj}_U(\mathbf x)\in U^\perp$. **The formula does not depend on which orthogonal basis is used** — proved by "orthogonal to itself hence zero".
- **Gram–Schmidt manufactures an orthogonal basis from any basis**, subtracting at each step everything already accounted for. **It preserves the nested spans**, which is why $R$ is triangular in $QR$, and outputs may be rescaled freely.
- **An orthogonal matrix has orthonormal columns, $P^{-1}=P^{\mathsf T}$, $\det P=\pm1$**, and is exactly a distance-preserving operator. **"Orthogonal rows" is not enough — they must be normalised.**
- $$\boxed{A\text{ symmetric}\iff A\text{ orthogonally diagonalizable}\iff A\text{ has }n\text{ orthonormal eigenvectors}}$$ **— the Principal Axis / real spectral theorem, and the climax of the book.** Both failure modes of ch. 3 become impossible; eigenvalues are all real; **eigenvectors for distinct eigenvalues are automatically orthogonal**, so Gram–Schmidt is needed only *within* a repeated eigenspace.
- **Spectral decomposition $A=\sum\lambda_i\mathbf p_i\mathbf p_i^{\mathsf T}$** — a symmetric matrix is a weighted sum of projections onto its principal axes, and truncating gives the best low-rank approximation.
- **Positive definite ($\mathbf x^{\mathsf T}A\mathbf x>0$) $\iff$ all eigenvalues positive $\iff$ all leading principal minors positive $\iff$ $A=U^{\mathsf T}U$ (Cholesky, unique).** The algorithm is row-reduce-then-divide-by-$\sqrt{\text{diagonal}}$ and needs no pivoting.
- **$A^{\mathsf T}A$ is always PSD because $\mathbf x^{\mathsf T}A^{\mathsf T}A\mathbf x=\|A\mathbf x\|^2$, and PD iff the columns of $A$ are independent.** This single identity explains covariance matrices, Gram/kernel matrices, and the invertibility condition for OLS.
- **$A=QR$ is Gram–Schmidt as a matrix identity**, and it turns least squares into the triangular solve $R\mathbf z=Q^{\mathsf T}\mathbf b$ — **without ever forming $A^{\mathsf T}A$, which would square the condition number.** The **QR algorithm**, not the characteristic polynomial, is how eigenvalues are computed in practice.
- **PCA is the spectral theorem applied to a covariance matrix.** $\mathbf Y=P^{\mathsf T}\mathbf X$ gives uncorrelated components with $\mathrm{Var}(Y_i)=\lambda_i$; **trace invariance means total variance is preserved**, so "PC$_1$ explains $\lambda_1/\sum\lambda_i$" is exact.
- **PC1 is genuinely the maximum-variance direction**: $\max_{\|\mathbf a\|=1}\mathbf a^{\mathsf T}\Sigma\mathbf a=\lambda_1$, attained at $\mathbf p_1$ — which needs both completeness and orthonormality of the eigenbasis, i.e. the whole spectral theorem.

---

## ⚠️ Important Notes

> [!warning] "Orthogonal matrix" means orthonormal columns
> **$P^{\mathsf T}P=I$ requires each column to have length 1, not merely to be perpendicular to the others.** A matrix with orthogonal-but-not-unit columns satisfies $P^{\mathsf T}P=D$ (diagonal), which is useful but is not the same thing.
>
> **Normalise before assembling $P$**, or the identity $P^{-1}=P^{\mathsf T}$ — the entire reason for using orthogonal matrices — fails.

> [!warning] Symmetry is the hypothesis, and it must be checked
> **The spectral theorem is an "if and only if".** For non-symmetric matrices:
> - eigenvalues may be complex ($\left[\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right]$);
> - eigenvectors may be too few ($\left[\begin{smallmatrix}2&1\\0&2\end{smallmatrix}\right]$);
> - eigenvectors for distinct eigenvalues need **not** be orthogonal.
>
> **Before invoking any of this chapter, verify $A=A^{\mathsf T}$.** It usually holds for a good reason — $\Sigma$, $A^{\mathsf T}A$, a Hessian — and when it does not, the right tool is the SVD, **which Nicholson does not cover** ([[00-Index]]).

> [!warning] Orthogonality within a repeated eigenspace is your job
> **Distinct eigenvalues give orthogonal eigenvectors for free.** A repeated eigenvalue gives a multi-dimensional eigenspace whose *basic solutions from row-reduction are generally not orthogonal* — and using them directly produces a $P$ that is invertible but **not orthogonal**, so $P^{-1}\ne P^{\mathsf T}$.
>
> **Run Gram–Schmidt inside each eigenspace, then normalise.** This is the single most-skipped step in orthogonal diagonalization.

> [!warning] The minor test needs *leading* principal minors, and strict positivity
> **Only the top-left $r\times r$ submatrices**, and every one of them must be **strictly** positive. Two failure modes:
> - **Checking all principal minors instead of the leading ones** is a different (and correct) test for *semi*-definiteness, but is exponentially more work.
> - **Allowing $\det=0$** admits positive *semi*-definite matrices like $\left[\begin{smallmatrix}1&0\\0&0\end{smallmatrix}\right]$.
>
> **And the test only applies to symmetric matrices.** For a non-symmetric matrix "$\mathbf x^{\mathsf T}A\mathbf x>0$" is still meaningful but the minor criterion is false.

> [!warning] Never form $A^{\mathsf T}A$ if you can avoid it
> **Forming the normal equations squares the condition number.** A matrix that is merely awkward becomes numerically singular.
>
> | Task | Textbook formula | What to actually use |
> |---|---|---|
> | Least squares | $(A^{\mathsf T}A)^{-1}A^{\mathsf T}\mathbf b$ | **QR:** $R\mathbf z=Q^{\mathsf T}\mathbf b$ |
> | Eigenvalues | roots of $c_A(x)$ | **QR algorithm** |
> | PCA | eigendecomposition of $\Sigma$ | **SVD of the centred data matrix** |
>
> **In every row the formula is correct and the algorithm is different** — which is the recurring lesson of numerical linear algebra, and the reason §8.5 exists.

> [!warning] PCA is scale-dependent and rotation-only
> **Multiply a variable by 1000 and its variance grows by $10^6$; it will dominate PC1** regardless of its importance. **Standardise first** — i.e. use the correlation matrix — unless the variables are already in comparable units. **The linear algebra cannot make this decision for you, and it changes the answer.**
>
> **Two further limitations worth stating plainly:**
> - **PCA finds only linear structure.** Data on a circle has no informative principal direction.
> - **Components are optimal for variance, not for interpretability or prediction.** A low-variance direction may carry all the signal you care about — **"explains 2% of the variance" does not mean "unimportant".**

> [!warning] The largest omission in the textbook sits exactly here
> **Nicholson never covers the singular value decomposition.** The spectral theorem handles **symmetric** matrices; the SVD $A=U\Sigma V^{\mathsf T}$ handles **every** matrix, square or not.
>
> **What is out of reach without it:** PCA computed stably from a data matrix, low-rank approximation of rectangular data (Eckart–Young), the pseudo-inverse, latent semantic analysis, and the numerically sound route to least squares. **§8.10's covariance-eigendecomposition is mathematically correct and is the route no practitioner uses.**
>
> **Fill this gap from Strang ch. 7 or Trefethen & Bau.** It is the single highest-value thing to read outside this book.

> [!note] Cross-subject connections
> - [[04 - Vector Geometry|Ch. 04]] — the projection formula, generalised from a line to a subspace; the symmetry of $\mathbf d\mathbf d^{\mathsf T}$ is why §4.4's projection matrices are orthogonally diagonalizable.
> - [[05 - The Vector Space Rn|Ch. 05]] — the Expansion Theorem is the projection onto $U$ itself; **least squares becomes $R\mathbf z=Q^{\mathsf T}\mathbf b$**; $\dim U+\dim U^\perp=n$ is rank–nullity.
> - [[03 - Determinants and Diagonalization|Ch. 03]] — **both failure modes of diagonalization vanish for symmetric matrices**, which is the whole content of §8.2.
> - [[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07]] — **$\Sigma$ is PSD because variances are non-negative**; the multivariate normal is determined by $\boldsymbol\mu$ and $\Sigma$; uncorrelated means orthogonal.
> - [[Econometrics/contents/00-Index|Econometrics]] — **$X^{\mathsf T}X$ invertible $\iff$ no perfect multicollinearity**; QR is why software does not invert it; near-singularity is what inflates standard errors.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **PCA is §8.10**; kernel matrices are PSD by construction (Exercise 4(iii)); whitening is $\Sigma^{-1/2}$, which exists because $\Sigma$ is PSD; spectral clustering uses eigenvectors of a symmetric graph Laplacian.
> - [[Optimization/contents/00-Index|Optimization]] — **a PD Hessian is the second-order condition for a minimum**, and the **condition number $\lambda_{\max}/\lambda_{\min}$ governs gradient-descent convergence**; §8.9's $\max\{\mathbf x^{\mathsf T}A\mathbf x:\|\mathbf x\|=1\}=\lambda_{\max}$ is the simplest constrained optimisation there is.
> - [[Calculus/contents/00-Index|Calculus]] — the Hessian is symmetric (Clairaut), hence orthogonally diagonalizable, and its principal axes are the directions of extreme curvature.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **The book's largest omission is in this chapter's territory: there is no singular value decomposition anywhere in Nicholson.** It is absent from the table of contents, the index, and the text. **§8.10 therefore derives PCA by eigendecomposing $\Sigma$** — correct, but the route no practitioner takes, and one that squares the condition number of the data matrix. **This is flagged in [[00-Index]] and in the notes above**, and it is the one thing a data-science reader must obtain elsewhere.
>
> **A second structural gap: §8.10 is four pages and states three results without proof** — that $\Sigma$ is positive semi-definite, that $\operatorname{cov}(Y_i,Y_j)=0$ for $i\ne j$, and that $\mathrm{Var}(Y_i)=\lambda_i$. Each is a one-line consequence of $\mathbf a^{\mathsf T}\Sigma\mathbf a=\mathrm{Var}(\mathbf a^{\mathsf T}\mathbf X)$ together with the spectral theorem, **so I have proved them in Exercise 5(c)** rather than leave the section's central claims asserted. **The characterisation of PC1 as the maximum-variance direction — arguably the definition of PCA — is not stated at all in §8.10**; it appears only obliquely in §8.9 on constrained optimization.
>
> **Source typos:**
> - **§8.2, proof of the Principal Axis Theorem, writes $A^{\mathsf T}=P^{\mathsf T\mathsf T}D^{\mathsf T}P^{\mathsf T}$** — the doubled transpose is printed as `PTT`, which is $(P^{\mathsf T})^{\mathsf T}=P$; legible but easy to misread as a typo for something else.
> - **§8.1, the paragraph introducing projections, reads "the line $U=\mathbb{R}\mathbf d=\{t\mathbf d\mid t\in\mathbb{R}\}$ a subspace of $\mathbb{R}^3$"** — the verb "is" is missing.
> - **§8.10 writes the covariance as $\operatorname{cov}(X,Y)=E\{(X-\mu)(Y-\upsilon)\}$ using $\upsilon$ (upsilon) for the mean of $Y$**, while $\mu$ is used for $X$; the two symbols are visually near-identical to $v$ and are used inconsistently with the $\mu_i$ notation introduced two lines later.
> - **§8.3, Lemma 1's proof carries a stray footnote marker "5" inside the displayed mathematics.**
>
> **PDF extraction:** matrices and displayed formulas suffer as throughout. **`Q … R` are large parentheses** in the projection formulas, **`S … T` are large brackets**, **`∥ … ∥` survives but detaches from its exponent** ($\|\mathbf f_1\|^2$ appears as `∥ f 1 ∥ 2`), **`/micro` is $\mu$ and `υ` is upsilon** in §8.10, **`__X` with the bar on a separate line is the random vector $\mathbf X$**, and **`(r)A` for the leading principal submatrix extracts with the superscript displaced.** **All figures are images** — including the diagram of $\mathbf x$, $\mathbf p$ and $U$ that makes the Projection Theorem obvious, and every quadric-surface picture in §8.8. **Fractions with square roots (the entries of every orthogonal $P$) extract across three lines each**, so every matrix $P$ in these notes has been reconstructed and re-derived from the eigenvectors.
>
> **Verification performed:** every worked example quoted was independently recomputed. Confirmed: the Gram–Schmidt output $\mathbf f_2=(-1,0,1,1)$, the projection $\mathbf p=\tfrac13(5,4,-1,3)$ and the residual $\tfrac13(4,-7,1,3)$ (§8.1 Ex. 3); $\mathbf f_2=(1,-1,1)$ and the closest point $(0,-2,-2)$ (§8.1 Ex. 4); and **the leading minors $10,5,3$ together with the full Cholesky factor $U$ of $\left[\begin{smallmatrix}10&5&2\\5&3&2\\2&2&3\end{smallmatrix}\right]$, checked by re-multiplying $U^{\mathsf T}U=A$ exactly** (§8.3 Ex. 2). **All agree with the text.** Every exercise figure in these notes was likewise verified before being written down — including all eigenvalues and eigenvectors in Exercise 3 (checked by direct multiplication), the Cholesky factor in Exercise 4(ii) (checked by re-multiplication), and both PCA spectra in Exercise 5 with their trace identities.
>
> **Scope note:** **§8.6 (complex matrices, Schur's theorem, the complex spectral theorem, Cayley–Hamilton) and §8.7 (linear codes over finite fields) are omitted.** §8.6 is the right generalisation — over $\mathbb{C}$, *Hermitian* replaces symmetric and *unitary* replaces orthogonal, and every theorem of §8.2 survives — **but the real case covers every application in this course**, and complex matrices belong with the material excluded in [[00-Index]]. §8.7 is a self-contained excursion into coding theory whose linear algebra is chapters 1–5 over $\mathbb{Z}_p$ rather than $\mathbb{R}$. **§§8.8 (quadratic forms) and 8.9 (constrained optimization) are compressed into §5 above**, because their content is the spectral theorem applied twice: diagonalising $\mathbf x^{\mathsf T}A\mathbf x$ into $\sum\lambda_iy_i^2$, and maximising it on the unit sphere to get $\lambda_{\max}$. **Both results are needed to justify PCA, so neither is dropped — only their separate treatment is.**

#linear-algebra #orthogonality #orthogonal-complement #gram-schmidt #spectral-theorem #principal-axis #positive-definite #cholesky #qr-factorization #pca
