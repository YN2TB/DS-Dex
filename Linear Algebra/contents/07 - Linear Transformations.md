---
subject: Linear Algebra
chapter: 07
tags: [ds, linear-algebra, linear-transformation, kernel, image, dimension-theorem, isomorphism, rank-nullity]
source: "Nicholson, *Linear Algebra with Applications*, 7th ed., ch. 7 (pp. 331–367)"
---

# Linear Transformations

> [!abstract] What this chapter is for
> **Chapter 6 built the spaces; this chapter studies the maps between them.** Nicholson quotes the standard remark: *vector spaces exist so that linear transformations can act on them.*
>
> Everything reduces to **two subspaces** attached to a map $T:V\to W$:
>
> $$\ker T=\{\mathbf v: T(\mathbf v)=\mathbf 0\}\subseteq V,\qquad \operatorname{im}T=\{T(\mathbf v)\}\subseteq W$$
>
> **The kernel measures what $T$ destroys; the image measures what $T$ reaches** — and the chapter's central theorem says the two are complementary:
>
> $$\boxed{\ \dim V=\dim(\ker T)+\dim(\operatorname{im}T)\ }$$
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Definition and examples | **$T$ is determined by its action on a basis** — and that action is arbitrary |
> | **2** | **Kernel and image** | One-to-one $\iff\ker T=\{\mathbf 0\}$; **the dimension theorem** |
> | **3** | Isomorphisms | **$V\cong W\iff\dim V=\dim W$** — dimension is the *only* invariant |
>
> **The dimension theorem is [[01 - Systems of Linear Equations|ch. 01]]'s "$n-r$ parameters" and [[05 - The Vector Space Rn|ch. 05]]'s rank–nullity, stated for the last time and in full generality.** Meeting it three times is not repetition — it is the same fact becoming steadily less about arithmetic and more about structure.

---

## 📘 Main Knowledge

### 1. Linear transformations

> [!important] Definition 7.1
> $T:V\to W$ between vector spaces is a **linear transformation** if for all $\mathbf v,\mathbf v_1\in V$ and scalars $a$:
> $$T(\mathbf v+\mathbf v_1)=T(\mathbf v)+T(\mathbf v_1),\qquad T(a\mathbf v)=aT(\mathbf v)$$
> **A linear transformation $V\to V$ is called an *operator*.**

> [!important] Theorem 1 (§7.1) — immediate consequences
> $$T(\mathbf 0)=\mathbf 0,\qquad T(-\mathbf v)=-T(\mathbf v),\qquad T\!\left(\sum_i t_i\mathbf v_i\right)=\sum_i t_iT(\mathbf v_i)$$
>
> **$T(\mathbf 0)=\mathbf 0$ is the fastest test available:** if a candidate map sends $\mathbf 0$ anywhere else, it is not linear. *(This is why $\mathbf x\mapsto A\mathbf x+\mathbf b$ with $\mathbf b\ne\mathbf 0$ is **affine**, not linear.)*

> [!example] Linear transformations you already know
> | $T$ | From $\to$ To | Linear because |
> |---|---|---|
> | $\mathbf x\mapsto A\mathbf x$ | $\mathbb{R}^n\to\mathbb{R}^m$ | [[02 - Matrix Algebra\|ch. 02]] Theorem 2 (§2.2) |
> | $A\mapsto A^{\mathsf T}$ | $\mathbf M_{mn}\to\mathbf M_{nm}$ | $(A+B)^{\mathsf T}=A^{\mathsf T}+B^{\mathsf T}$ |
> | $A\mapsto\operatorname{tr}A$ | $\mathbf M_{nn}\to\mathbb{R}$ | trace is a sum of entries |
> | $p\mapsto p'$ | $\mathbf P_n\to\mathbf P_{n-1}$ | **differentiation is linear** |
> | $f\mapsto\int_a^b f$ | $\mathbf F[a,b]\to\mathbb{R}$ | **integration is linear** |
> | $p\mapsto p(a)$ | $\mathbf P_n\to\mathbb{R}$ | evaluation |
> | $X\mapsto UX$ ($U$ fixed) | $\mathbf M_{mn}\to\mathbf M_{mn}$ | distributivity |
>
> **Calculus is largely a study of two linear operators.** $\frac{d}{dx}$ and $\int$ are linear transformations on function spaces, and every "differentiate term by term" or "the integral of a sum" is that linearity being used.

> [!important] Theorems 2 and 3 (§7.1) — a linear map is a basis-length list of choices
> **Theorem 2.** If $\{\mathbf e_1,\dots,\mathbf e_n\}$ is a basis of $V$ and $T(\mathbf e_i)=S(\mathbf e_i)$ for all $i$, then **$T=S$.**
>
> **Theorem 3.** Given a basis $\{\mathbf e_1,\dots,\mathbf e_n\}$ of $V$ and **any** vectors $\mathbf w_1,\dots,\mathbf w_n$ in $W$, there is **exactly one** linear $T:V\to W$ with $T(\mathbf e_i)=\mathbf w_i$.

> [!tip] This is the most economical fact in the subject
> **To specify a linear map out of an $n$-dimensional space, you make $n$ free choices and nothing else.** The images of the basis may be *anything* — repeated, zero, dependent — and each choice extends uniquely.
>
> **In $\mathbb{R}^n$ this is exactly "the columns of the standard matrix are $T(\mathbf e_j)$"** ([[02 - Matrix Algebra|ch. 02 §6]]). **Here it holds for polynomials, matrices and functions too**, and it is what makes "the matrix of $T$ relative to a basis" possible (ch. 9).

---

### 2. Kernel and image

> [!important] Definition 7.2 and Theorem 1 (§7.2)
> $$\ker T=\{\mathbf v\in V:T(\mathbf v)=\mathbf 0\},\qquad \operatorname{im}T=T(V)=\{T(\mathbf v):\mathbf v\in V\}$$
> **Both are subspaces** — $\ker T$ of $V$, $\operatorname{im}T$ of $W$.
>
> For $T_A(\mathbf x)=A\mathbf x$: $\ \ker T_A=\operatorname{null}A$ and $\operatorname{im}T_A=\operatorname{col}A$.

> [!important] Definition 7.3 and Theorem 2 (§7.2)
> - **$T$ is onto** if $\operatorname{im}T=W$ — every target is hit **at least** once.
> - **$T$ is one-to-one** if $T(\mathbf v)=T(\mathbf v_1)\Rightarrow\mathbf v=\mathbf v_1$ — nothing is hit **twice**.
>
> $$\boxed{\ T\text{ is one-to-one}\iff\ker T=\{\mathbf 0\}\ }$$

**The proof is worth remembering because the technique recurs.** If $T(\mathbf v)=T(\mathbf v_1)$ then $T(\mathbf v-\mathbf v_1)=\mathbf 0$, so $\mathbf v-\mathbf v_1\in\ker T=\{\mathbf 0\}$.

> [!tip] Why checking one vector settles injectivity
> **A linear map is one-to-one iff it fails to be one-to-one *at the origin*.** By linearity, any collision $T(\mathbf v)=T(\mathbf v_1)$ can be translated to a collision with $\mathbf 0$.
>
> **So instead of comparing all pairs of inputs — infinitely many — you solve a single homogeneous equation.** This is a large reduction, and it exists only because $T$ is linear.

> [!important] Theorem 3 (§7.2) — for matrices, everything is rank
> For $T_A:\mathbb{R}^n\to\mathbb{R}^m$:
> $$T_A\text{ is onto}\iff\operatorname{rank}A=m,\qquad T_A\text{ is one-to-one}\iff\operatorname{rank}A=n$$
>
> **Consequences that need no computation:**
> | Shape | Conclusion |
> |---|---|
> | $n>m$ (more inputs than outputs) | **never one-to-one** — $\operatorname{rank}\le m<n$ |
> | $n<m$ (fewer inputs than outputs) | **never onto** — $\operatorname{rank}\le n<m$ |
> | $n=m$ | one-to-one $\iff$ onto $\iff$ invertible |
>
> **The first row is [[01 - Systems of Linear Equations|ch. 01]]'s theorem that more variables than equations gives a nontrivial solution.** The third row adds two more entries to the Inverse Theorem.

#### 2a. The dimension theorem

> [!important] Theorem 4 (§7.2) — the Dimension Theorem
> For any linear $T:V\to W$ with $\ker T$ and $\operatorname{im}T$ finite-dimensional:
> $$\boxed{\ \dim V=\dim(\ker T)+\dim(\operatorname{im}T)\ }\qquad\text{i.e.}\qquad \dim V=\text{nullity}(T)+\text{rank}(T)$$

**The proof is a construction worth seeing.** Take a basis $\{T(\mathbf e_1),\dots,T(\mathbf e_r)\}$ of $\operatorname{im}T$ and a basis $\{\mathbf f_1,\dots,\mathbf f_k\}$ of $\ker T$; then $\{\mathbf e_1,\dots,\mathbf e_r,\mathbf f_1,\dots,\mathbf f_k\}$ is shown to be a basis of $V$. **Spanning:** given $\mathbf v$, subtract the right combination of the $\mathbf e_i$ so that the remainder lies in $\ker T$. **Independence:** apply $T$ to a vanishing combination — the $\mathbf f$ terms die, forcing the $\mathbf e$ coefficients to vanish, after which the $\mathbf f$ coefficients do too.

> [!tip] Read it as conservation of dimension
> **$V$ has $\dim V$ dimensions going in. $T$ crushes $\dim(\ker T)$ of them to zero and passes the remaining $\dim(\operatorname{im}T)$ through.** Nothing is lost or created.
>
> **The three appearances of one theorem:**
> | Where | Statement |
> |---|---|
> | [[01 - Systems of Linear Equations\|Ch. 01]] Thm 2 (§1.2) | a consistent system has $n-r$ parameters |
> | [[05 - The Vector Space Rn\|Ch. 05]] Thm 2 (§5.4) | $\operatorname{rank}A+\dim(\operatorname{null}A)=n$ |
> | **Here, Thm 4** | $\dim(\operatorname{im}T)+\dim(\ker T)=\dim V$ |
>
> **The practical value is that you compute whichever side is easier and get the other free** — usually the kernel, since it is one homogeneous equation.
>
> **A bonus in the statement: $V$ is not assumed finite-dimensional.** Showing $\ker T$ and $\operatorname{im}T$ are both finite-dimensional *proves* that $V$ is.

**Theorem 5 (§7.2)** sharpens the construction: if $\{\mathbf e_1,\dots,\mathbf e_r,\mathbf e_{r+1},\dots,\mathbf e_n\}$ is a basis of $V$ whose **last $n-r$ vectors form a basis of $\ker T$**, then $\{T(\mathbf e_1),\dots,T(\mathbf e_r)\}$ is a basis of $\operatorname{im}T$. **So: find the kernel, extend to a basis of $V$, and the images of the extra vectors are a basis of the image.**

---

### 3. Isomorphisms (§7.3)

> [!important] Definition 7.4
> $T:V\to W$ is an **isomorphism** if it is linear, one-to-one and onto. $V$ and $W$ are **isomorphic** ($V\cong W$) if such a $T$ exists.

> [!important] Theorem 1 (§7.3) — dimension is the only invariant
> For finite-dimensional $V,W$:
> $$\boxed{\ V\cong W\iff\dim V=\dim W\ }$$
> In particular, **every $n$-dimensional space is isomorphic to $\mathbb{R}^n$.**

> [!tip] What this says, and what it does not
> **Every 4-dimensional vector space *is* $\mathbb{R}^4$, as far as linear algebra can tell.** $\mathbf P_3$, $\mathbf M_{22}$ and $\mathbb{R}^4$ are indistinguishable by any statement about addition, scaling, span, independence, dimension or rank.
>
> **The isomorphism is: pick a basis and read off coordinates.** For $\mathbf P_3$, $a+bx+cx^2+dx^3\mapsto(a,b,c,d)$; for $\mathbf M_{22}$, list the four entries.
>
> **What it does *not* say is that the spaces are interchangeable in every respect.** $\mathbf P_3$ has multiplication of polynomials, differentiation, and evaluation at a point; $\mathbf M_{22}$ has matrix multiplication and determinants. **An isomorphism preserves the linear structure and nothing else** — so a theorem *about that structure* transfers, and everything else does not.
>
> **This is why chapter 6's abstraction costs nothing and buys a lot: there is only one vector space of each dimension, so proving something once proves it everywhere.**

**Composition** (§7.3): if $S:V\to W$ and $T:W\to U$ are linear, so is $T\circ S$; and **the matrix of a composite is the product of the matrices** — [[02 - Matrix Algebra|ch. 02 §3]]'s reason for defining $AB$ as it did, now in general. $T$ is an isomorphism iff it has an inverse $T^{-1}$, which is automatically linear.

---

## ✏️ Exercises

> [!question] Exercise 1 — which maps are linear? *(warm-up)*
> (i) $T:\mathbb{R}^2\to\mathbb{R}^2$, $T(x,y)=(x+y,\ x-y)$
> (ii) $T:\mathbb{R}^2\to\mathbb{R}^2$, $T(x,y)=(x+1,\ y)$
> (iii) $T:\mathbb{R}^2\to\mathbb{R}$, $T(x,y)=xy$
> (iv) $T:\mathbf M_{nn}\to\mathbb{R}$, $T(A)=\det A$ (take $n=2$)
> (v) $T:\mathbf P_2\to\mathbb{R}^2$, $T(p)=(p(0),\ p(1))$
> (vi) $D:\mathbf P_3\to\mathbf P_3$, $D(p)=p'$

> [!example]- Solution
> **(i) Linear.** It is $T_A$ with $A=\begin{bmatrix}1&1\\1&-1\end{bmatrix}$.
>
> **(ii) Not linear** — $T(0,0)=(1,0)\ne\mathbf 0$. **This is an *affine* map** ($\mathbf x\mapsto A\mathbf x+\mathbf b$), and the distinction matters: a regression *with* an intercept is affine in the inputs, though still linear in the parameters.
>
> **(iii) Not linear.** $T(1,1)=1$ but $T(2,2)=4\ne2T(1,1)$. **It passes the $T(\mathbf 0)=\mathbf 0$ test and still fails** — so that test is necessary, not sufficient.
>
> **(iv) Not linear.** $\det I_2=1$ and $\det(2I_2)=4\ne2$. **In general $\det(kA)=k^n\det A$** ([[03 - Determinants and Diagonalization|ch. 03]]), and $\det(A+B)\ne\det A+\det B$. **The determinant is multilinear in the *columns*, which is a much weaker property.**
>
> **(v) Linear.** $(p+q)(0)=p(0)+q(0)$ and $(ap)(0)=a\,p(0)$; likewise at 1. **Evaluation is linear, and so is any finite list of evaluations.**
>
> **(vi) Linear** — $(p+q)'=p'+q'$ and $(ap)'=ap'$. **This is the linearity of differentiation, used constantly in calculus without being named.**
>
> > [!tip] The order to test in
> > 1. **Does $T(\mathbf 0)=\mathbf 0$?** If not, stop.
> > 2. **Does any variable appear squared, multiplied by another, or inside a non-linear function?** If so, test $T(2\mathbf v)$ against $2T(\mathbf v)$ — it will fail.
> > 3. Otherwise verify both axioms.

> [!question] Exercise 2 — kernel and image
> For each $T$, find $\ker T$, $\operatorname{im}T$, their dimensions, and verify the dimension theorem.
> (i) $T:\mathbf P_2\to\mathbb{R}^2$, $T(p)=(p(0),p(1))$
> (ii) $D:\mathbf P_3\to\mathbf P_3$, $D(p)=p'$
> (iii) $T:\mathbf M_{22}\to\mathbf M_{22}$, $T(X)=X-X^{\mathsf T}$
> (iv) $T_A:\mathbb{R}^4\to\mathbb{R}^3$ for $A=\begin{bmatrix}1&2&2&-1\\3&6&5&0\\1&2&1&2\end{bmatrix}$

> [!example]- Solution
> **(i)** $p=a+bx+cx^2$ has $T(p)=(a,\ a+b+c)$. So $\ker T$ needs $a=0$ and $b+c=0$:
> $$\ker T=\{c(x^2-x)\}=\operatorname{span}\{x^2-x\},\qquad \dim=1$$
> $\operatorname{im}T$: given any $(s,t)$, take $a=s$ and $b=t-s$, $c=0$ — **so $T$ is onto**, $\dim(\operatorname{im}T)=2$.
> $$\dim\mathbf P_2=3=1+2\ ✓$$
> *(Note $x^2-x$ vanishes at both 0 and 1, as it must.)*
>
> **(ii)** $D(p)=0$ iff $p$ is constant: $\ker D=\operatorname{span}\{1\}$, $\dim=1$. $\operatorname{im}D=\mathbf P_2$ (every polynomial of degree $\le2$ is a derivative), $\dim=3$.
> $$\dim\mathbf P_3=4=1+3\ ✓$$
> **$D$ is neither one-to-one (constants are lost) nor onto ($x^3$ is not a derivative of anything in $\mathbf P_3$).**
>
> **(iii)** $T(X)=\mathbf 0$ iff $X=X^{\mathsf T}$, so $\ker T$ is the **symmetric** matrices, $\dim=3$ ([[06 - Vector Spaces|ch. 06]], Exercise 2(iii)). And $T(X)^{\mathsf T}=(X-X^{\mathsf T})^{\mathsf T}=-T(X)$, so $\operatorname{im}T\subseteq$ **skew-symmetric** matrices, $\dim=1$.
>
> **Equality holds:** for skew $S$, $T\!\left(\tfrac12S\right)=\tfrac12S-\tfrac12S^{\mathsf T}=\tfrac12S+\tfrac12S=S$.
> $$\dim\mathbf M_{22}=4=3+1\ ✓$$
> **This is [[02 - Matrix Algebra|ch. 02]]'s symmetric/skew decomposition read as a linear map**, and $\mathbf M_{22}=\ker T\oplus\operatorname{im}T$ here — **which is a coincidence of this example, not a general fact** (in (ii) the kernel and image both sit inside $\mathbf P_3$ and overlap).
>
> **(iv)** From [[05 - The Vector Space Rn|ch. 05]], $\operatorname{rank}A=2$:
> $$\ker T_A=\operatorname{null}A=\operatorname{span}\{(-2,1,0,0),(-5,0,3,1)\},\qquad \dim=2$$
> $$\operatorname{im}T_A=\operatorname{col}A=\operatorname{span}\{(1,3,1),(2,5,1)\},\qquad \dim=2$$
> $$\dim\mathbb{R}^4=4=2+2\ ✓$$
> **Not one-to-one ($\operatorname{rank}\ne4$), not onto ($\operatorname{rank}\ne3$)** — by Theorem 3, with no further work.

> [!question] Exercise 3 — using the dimension theorem to avoid work
> (i) $T:\mathbb{R}^7\to\mathbb{R}^4$ is linear with $\dim(\ker T)=3$. Is $T$ onto?
> (ii) $T:\mathbf P_4\to\mathbf M_{22}$ is linear and onto. Find $\dim(\ker T)$.
> (iii) Can a linear $T:\mathbb{R}^3\to\mathbb{R}^5$ be onto? Can it be one-to-one?
> (iv) $T:V\to V$ is linear on a finite-dimensional $V$. Show $T$ is one-to-one $\iff$ $T$ is onto. Give an example on an infinite-dimensional space where this fails.

> [!example]- Solution
> **(i)** $\dim(\operatorname{im}T)=7-3=4=\dim\mathbb{R}^4$, and a subspace of the same dimension as the whole space *is* the whole space ([[06 - Vector Spaces|ch. 06]] Theorem 2). **So yes, $T$ is onto.** $\boxed{\text{Yes}}$
>
> **(ii)** $\dim\mathbf P_4=5$ and $\dim\mathbf M_{22}=4$; onto means $\dim(\operatorname{im}T)=4$, so
> $$\dim(\ker T)=5-4=\boxed{1}$$
>
> **(iii)** $\dim(\operatorname{im}T)\le\dim\mathbb{R}^3=3<5$, so **never onto.** But it **can** be one-to-one — e.g. $(x,y,z)\mapsto(x,y,z,0,0)$, whose kernel is $\{\mathbf 0\}$. $\boxed{\text{Not onto; can be one-to-one}}$
>
> **(iv)** With $\dim V=n$, the dimension theorem gives $\dim(\ker T)+\dim(\operatorname{im}T)=n$. Then
> $$T\text{ one-to-one}\iff\dim(\ker T)=0\iff\dim(\operatorname{im}T)=n\iff\operatorname{im}T=V\iff T\text{ onto}$$
> $\blacksquare$
>
> **The infinite-dimensional counterexample:** on $\mathbf P$ (all polynomials), the **shift** $S(p)=x\,p(x)$ is one-to-one (multiplying by $x$ never gives 0) but **not onto** (nothing maps to the constant 1). Dually, $D(p)=p'$ is onto but not one-to-one.
>
> > [!important] Why the equivalence needs finite dimension
> > **The dimension theorem's bookkeeping is what forces "no loss $\Rightarrow$ full coverage".** In infinite dimensions the arithmetic $\infty=0+\infty$ carries no information, and the equivalence genuinely fails.
> >
> > **This is the same phenomenon as Hilbert's hotel**, and it is why the Inverse Theorem is a statement about **square** matrices: for $\mathbb{R}^n\to\mathbb{R}^n$, injective, surjective and invertible coincide; for rectangular maps they come apart ([[02 - Matrix Algebra|ch. 02]] Corollary 1).

> [!question] Exercise 4 — building maps from bases
> (i) Find the unique linear $T:\mathbb{R}^2\to\mathbb{R}^3$ with $T(1,1)=(1,0,2)$ and $T(1,-1)=(3,2,0)$. Give its standard matrix.
> (ii) Is there a linear $T:\mathbb{R}^2\to\mathbb{R}^2$ with $T(1,1)=(1,0)$, $T(2,2)=(0,1)$?
> (iii) Find a linear $T:\mathbf P_2\to\mathbf P_2$ with $\ker T=\operatorname{span}\{1\}$ and $\operatorname{im}T=\operatorname{span}\{1,x\}$, or show none exists.

> [!example]- Solution
> **(i)** $\{(1,1),(1,-1)\}$ is a basis of $\mathbb{R}^2$, so by Theorem 3 a unique $T$ exists. To get the standard matrix, find $T(\mathbf e_1)$ and $T(\mathbf e_2)$:
> $$\mathbf e_1=\tfrac12(1,1)+\tfrac12(1,-1)\ \Rightarrow\ T(\mathbf e_1)=\tfrac12(1,0,2)+\tfrac12(3,2,0)=(2,1,1)$$
> $$\mathbf e_2=\tfrac12(1,1)-\tfrac12(1,-1)\ \Rightarrow\ T(\mathbf e_2)=\tfrac12(1,0,2)-\tfrac12(3,2,0)=(-1,-1,1)$$
> $$A=\begin{bmatrix}2&-1\\1&-1\\1&1\end{bmatrix}$$
> **Check:** $A(1,1)^{\mathsf T}=(1,0,2)^{\mathsf T}$ ✓ and $A(1,-1)^{\mathsf T}=(3,2,0)^{\mathsf T}$ ✓.
>
> **(ii) No.** $(2,2)=2(1,1)$, so linearity **forces** $T(2,2)=2T(1,1)=(2,0)\ne(0,1)$.
>
> **Theorem 3 requires a *basis*, and $\{(1,1),(2,2)\}$ is dependent.** **On a basis the images are completely free; on a dependent set they are constrained by the same dependence.** *(This is the whole difference between the two theorems of §7.1.)*
>
> **(iii) Yes.** Use Theorem 5 in reverse: take the basis $\{x,x^2,1\}$ of $\mathbf P_2$ with $1$ spanning the intended kernel, and send
> $$T(x)=1,\qquad T(x^2)=x,\qquad T(1)=0$$
> By Theorem 3 this defines a unique linear $T$; explicitly $T(a+bx+cx^2)=b+cx$. Then $\ker T=\{a\}=\operatorname{span}\{1\}$ ✓ and $\operatorname{im}T=\operatorname{span}\{1,x\}$ ✓.
> $$\dim\mathbf P_2=3=1+2\ ✓$$
> **The dimension theorem is the feasibility check: any requested pair of dimensions summing to $\dim V$ is achievable, and any other pair is impossible.**

> [!question] Exercise 5 — isomorphisms *(hard)*
> (a) (i) Show $\mathbf P_3\cong\mathbf M_{22}\cong\mathbb{R}^4$ by exhibiting isomorphisms.
> (ii) Give a property of $\mathbf M_{22}$ **not** shared by $\mathbf P_3$, and explain why this does not contradict (i).
>
> (b) Let $T:V\to W$ be linear with $\dim V=\dim W=n$. Prove the following are equivalent: (1) $T$ is an isomorphism; (2) $T$ is one-to-one; (3) $T$ is onto; (4) $T$ carries some basis of $V$ to a basis of $W$.
>
> (c) Show that $\operatorname{tr}:\mathbf M_{nn}\to\mathbb{R}$ is linear and onto, and find $\dim(\ker\operatorname{tr})$.

> [!example]- Solution
> **(a)(i)** Coordinate maps relative to a basis:
> $$\Phi:\mathbf P_3\to\mathbb{R}^4,\quad a+bx+cx^2+dx^3\mapsto(a,b,c,d)$$
> $$\Psi:\mathbf M_{22}\to\mathbb{R}^4,\quad \begin{bmatrix}a&b\\c&d\end{bmatrix}\mapsto(a,b,c,d)$$
> **Both are linear (operations are coefficientwise/entrywise), one-to-one (all coefficients zero $\Rightarrow$ the object is zero), and onto.** Composing, $\Psi^{-1}\circ\Phi:\mathbf P_3\to\mathbf M_{22}$ is an isomorphism. *(Or simply cite Theorem 1: all three have dimension 4.)*
>
> **(ii)** $\mathbf M_{22}$ has a **multiplication** of vectors — matrix product — under which, for instance, $\left[\begin{smallmatrix}0&1\\0&0\end{smallmatrix}\right]^2=0$ with the matrix nonzero. **$\mathbf P_3$ is not even closed under polynomial multiplication** ($x^2\cdot x^2=x^4\notin\mathbf P_3$). Also $\mathbf M_{22}$ has $\det$ and $\operatorname{tr}$; $\mathbf P_3$ has $p\mapsto p'$ and $p\mapsto p(2)$.
>
> **No contradiction: an isomorphism preserves *only* addition and scalar multiplication.** Multiplication, determinants and differentiation are **extra structure**, invisible to the vector-space axioms. **"Isomorphic as vector spaces" is a precise and limited claim** — the spaces agree on everything chapters 5–7 can express, and may differ on everything else.
>
> **(b)** Prove a cycle.
>
> **(1)$\Rightarrow$(2)** by definition.
>
> **(2)$\Rightarrow$(3):** one-to-one gives $\dim(\ker T)=0$, so by the dimension theorem $\dim(\operatorname{im}T)=n=\dim W$; a subspace of $W$ with $\dim W$ dimensions is $W$ ([[06 - Vector Spaces|ch. 06]] Thm 2). **So $T$ is onto.**
>
> **(3)$\Rightarrow$(4):** onto gives $\dim(\operatorname{im}T)=n$, so $\dim(\ker T)=0$, so $T$ is one-to-one. Now take any basis $\{\mathbf e_1,\dots,\mathbf e_n\}$ of $V$; $\{T(\mathbf e_i)\}$ spans $\operatorname{im}T=W$ and consists of $n=\dim W$ vectors, hence is a basis ([[06 - Vector Spaces|ch. 06]] Thm 4).
>
> **(4)$\Rightarrow$(1):** if $\{T(\mathbf e_i)\}$ is a basis of $W$ then it spans, so $T$ is onto; and if $T(\sum t_i\mathbf e_i)=\mathbf 0$ then $\sum t_iT(\mathbf e_i)=\mathbf 0$, so all $t_i=0$ by independence, giving $\ker T=\{\mathbf 0\}$. **Hence $T$ is an isomorphism.** $\blacksquare$
>
> > [!important] This is the Inverse Theorem for abstract spaces
> > **Compare [[02 - Matrix Algebra|ch. 02]]'s Theorem 5** — invertible, trivial kernel, always solvable, one-sided inverse — **which is this list for $V=W=\mathbb{R}^n$.** The unifying reason is the same in both places: **the dimension theorem forces "no loss" and "full coverage" to coincide when the dimensions match.**
>
> **(c)** $\operatorname{tr}(A+B)=\operatorname{tr}A+\operatorname{tr}B$ and $\operatorname{tr}(kA)=k\operatorname{tr}A$, since the trace is a sum of diagonal entries. **Onto:** for any $r\in\mathbb{R}$, $\operatorname{tr}(rE_{11})=r$. So $\dim(\operatorname{im})=1$ and
> $$\dim(\ker\operatorname{tr})=\dim\mathbf M_{nn}-1=\boxed{n^2-1}$$
> *(At $n=2$: $\dim=3$, matching [[06 - Vector Spaces|ch. 06]] Exercise 2(iv).)*
>
> **The general principle: a single non-trivial linear functional $V\to\mathbb{R}$ always has kernel of dimension $\dim V-1$** — a **hyperplane** through the origin. **Every homogeneous linear equation removes exactly one dimension**, which is the abstract version of what row-reduction has been counting since chapter 1.

---

## 📝 Summary

- **A linear transformation preserves addition and scalar multiplication**, hence $T(\mathbf 0)=\mathbf 0$ and $T(\sum t_i\mathbf v_i)=\sum t_iT(\mathbf v_i)$. **$T(\mathbf 0)=\mathbf 0$ is the fastest test** — and it is necessary, not sufficient. **A map $\mathbf x\mapsto A\mathbf x+\mathbf b$ with $\mathbf b\ne\mathbf 0$ is affine, not linear.**
- **Differentiation, integration, evaluation, transposition and trace are all linear** — which is why "differentiate term by term" needs no justification.
- **A linear map is determined by its action on a basis, and that action is completely free** (Theorems 2 and 3). In $\mathbb{R}^n$ this is "the columns are $T(\mathbf e_j)$". **On a *dependent* set the images are constrained** — which is why Exercise 4(ii) has no solution.
- **$\ker T$ and $\operatorname{im}T$ are subspaces of $V$ and $W$**; for $T_A$ they are $\operatorname{null}A$ and $\operatorname{col}A$.
- $$\boxed{T\text{ one-to-one}\iff\ker T=\{\mathbf 0\}}$$ **— injectivity is decided by one homogeneous equation rather than by comparing all pairs of inputs**, and only linearity makes that reduction possible.
- **For matrices everything is rank:** $T_A$ is onto iff $\operatorname{rank}A=m$, one-to-one iff $\operatorname{rank}A=n$. **So $n>m$ is never one-to-one and $n<m$ is never onto**, with no computation.
- $$\boxed{\dim V=\dim(\ker T)+\dim(\operatorname{im}T)}$$ **— the same theorem as ch. 1's parameter count and ch. 5's rank–nullity.** Compute whichever side is easier. **It does not assume $V$ is finite-dimensional** — proving both pieces finite proves $V$ is.
- **Theorem 5 gives the construction:** find a basis of $\ker T$, extend it to a basis of $V$, and the images of the added vectors are a basis of $\operatorname{im}T$.
- **On a finite-dimensional space, an operator is one-to-one iff it is onto** — and this **fails** in infinite dimensions ($p\mapsto xp$ is injective and not surjective; $p\mapsto p'$ is the reverse).
- $$\boxed{V\cong W\iff\dim V=\dim W}$$ **— dimension is the only invariant, so every $n$-dimensional space is $\mathbb{R}^n$ in disguise.** But an isomorphism preserves **only** the linear structure: multiplication, determinants and differentiation do not transfer.
- **A nonzero linear functional $V\to\mathbb{R}$ has kernel of dimension $\dim V-1$** — a hyperplane. **Every homogeneous linear condition costs exactly one dimension.**

---

## ⚠️ Important Notes

> [!warning] Linear versus affine
> $$T(\mathbf x)=A\mathbf x\ \ \text{(linear)}\qquad\text{versus}\qquad T(\mathbf x)=A\mathbf x+\mathbf b\ \ \text{(affine)}$$
> **The second is not a linear transformation** unless $\mathbf b=\mathbf 0$ — it fails $T(\mathbf 0)=\mathbf 0$.
>
> **This is why "linear regression" is a confusing name**: the fitted function $\hat y=\beta_0+\beta_1x$ is affine in $x$ and **linear in the parameters $(\beta_0,\beta_1)$** — and the second is what matters, since it is the parameters that are being solved for. **The trick that reconciles them is a column of 1s**, which turns the affine map into a linear one on a space of one higher dimension. *(The same trick is homogeneous coordinates in computer graphics.)*

> [!warning] $T(\mathbf 0)=\mathbf 0$ is necessary but not sufficient
> $T(x,y)=xy$ and $T(x,y)=\|(x,y)\|$ both fix the origin and are not linear. **Passing the first test only means you must do the real one** — check $T(a\mathbf v)=aT(\mathbf v)$ on a specific vector, which is where non-linearity almost always shows up.
>
> **Most notably, $\det$ is not linear**: $\det(kA)=k^n\det A$ and $\det(A+B)\ne\det A+\det B$.

> [!warning] Theorem 3 needs a **basis**, not just any set
> **The images of a basis may be assigned completely freely.** The images of a *dependent* set may not: if $\mathbf v_3=2\mathbf v_1$ then $T(\mathbf v_3)=2T(\mathbf v_1)$ is forced.
>
> **And on a set that is independent but not spanning, $T$ exists but is not unique** — any extension of the assignment to a full basis works.
>
> **Before assigning images, check: independent (existence) and spanning (uniqueness).**

> [!warning] $V=\ker T\oplus\operatorname{im}T$ is **not** a general fact
> The dimension theorem says the *dimensions* add. **It does not say the subspaces are complementary** — and usually they cannot even be compared, since $\ker T\subseteq V$ while $\operatorname{im}T\subseteq W$.
>
> **Even for an operator $T:V\to V$ it can fail.** For $D:\mathbf P_3\to\mathbf P_3$, $\ker D=\operatorname{span}\{1\}$ and $\operatorname{im}D=\mathbf P_2$ — and $1\in\mathbf P_2$, so the intersection is nontrivial and the sum is not direct. **Exercise 2(iii) happens to give a direct sum; that is a feature of the example, not a theorem.**

> [!warning] One-to-one $\iff$ onto needs finite dimension **and** equal dimensions
> | Situation | Equivalence? |
> |---|---|
> | $T:V\to V$, $\dim V<\infty$ | **Yes** |
> | $T:V\to W$, $\dim V=\dim W<\infty$ | **Yes** |
> | $T:V\to W$, $\dim V\ne\dim W$ | **No** — at most one can hold |
> | $\dim V=\infty$ | **No** — $p\mapsto xp$ and $p\mapsto p'$ are the standard counterexamples |
>
> **The equivalence is pure dimension bookkeeping**, and it is exactly why the Inverse Theorem is stated for square matrices.

> [!warning] Isomorphic means "the same *linear* structure", nothing more
> $\mathbf P_3\cong\mathbf M_{22}\cong\mathbb{R}^4$ — **and $\mathbf M_{22}$ still has matrix multiplication and determinants that $\mathbf P_3$ has no analogue of.**
>
> **What transfers:** dimension, rank, independence, span, everything expressible with $+$ and scalars.
> **What does not:** products of vectors, $\det$, $\operatorname{tr}$, differentiation, evaluation, and — crucially — **anything involving lengths or angles**, since the vector-space axioms have no inner product ([[06 - Vector Spaces|ch. 06]]).
>
> **So "every 4-dimensional space is $\mathbb{R}^4$" is a genuine and useful theorem, and it is not a licence to treat polynomials as matrices.**

> [!note] Cross-subject connections
> - [[01 - Systems of Linear Equations|Ch. 01]] — the "$n-r$ parameters" count is the dimension theorem in its first and most concrete form.
> - [[02 - Matrix Algebra|Ch. 02]] — §2.6 is this chapter for $\mathbb{R}^n\to\mathbb{R}^m$; **composition of maps is matrix multiplication**, and Theorem 5 of §2.4 is Exercise 5(b) for $V=W=\mathbb{R}^n$.
> - [[05 - The Vector Space Rn|Ch. 05]] — rank–nullity is the dimension theorem for $T_A$; $\operatorname{null}A$ and $\operatorname{col}A$ are $\ker$ and $\operatorname{im}$.
> - [[06 - Vector Spaces|Ch. 06]] — supplies the dimension theory the proofs rest on; **"each linear condition costs a dimension" is Exercise 5(c) made general.**
> - [[Calculus/contents/00-Index|Calculus]] — **$\frac{d}{dx}$ and $\int$ are linear operators**; the kernel of $\frac{d}{dx}$ being the constants is why indefinite integrals carry $+C$, and $\dim\ker=1$ is why there is exactly one such constant.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **a network layer is affine, and the non-linearity between layers is what stops the composite from collapsing to one matrix**; $\operatorname{rank}$ of a layer bounds the information it can pass, and an autoencoder's bottleneck is a deliberately large kernel.
> - [[Econometrics/contents/00-Index|Econometrics]] — **the intercept is exactly what makes the model affine rather than linear**, and the column of 1s is the standard device for absorbing it.
> - [[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07]] — **$\mathbb{E}[\cdot]$ is a linear functional** on the space of integrable random variables, and $\mathbb{E}[Y\mid X]$ is a linear operator; "linearity of expectation needs no independence" is precisely the statement that $\mathbb{E}$ is linear.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **Source typos:**
> - **The proof of the Dimension Theorem (Thm 4, §7.2) writes "$T(\mathbf v)$ lies in $\operatorname{im}V$"** where $\operatorname{im}T$ is meant. **$\operatorname{im}V$ is not defined anywhere** — $V$ is a space, not a map.
> - **§7.2 Example 5 ends with an unclosed parenthesis**: "(in fact, $x=\tfrac12(s+t)$, $y=\tfrac12(s-t)$, and $z=0$." — the closing bracket is missing and the sentence runs into the next.
> - **§7.2, the paragraph before Theorem 5, refers to "Theorem 1 Section 6.4"** for basis extension; the result used is the extension clause of that theorem, but the cross-reference does not say which clause, and §6.4's Theorem 1 has several.
> - **§7.2 Example 3 (the projection $P(S)=S-S^{\mathsf T}$ material) prints $P[\tfrac12S]=\tfrac12S-[\tfrac12S]^{\mathsf T}$ with mismatched bracket styles**, and the running argument switches between $P$ and $T$ for the same map.
>
> **A structural note rather than a defect:** **Nicholson proves the Dimension Theorem *without* assuming $V$ is finite-dimensional**, which is stronger than the usual textbook statement and is used later to establish that certain function spaces are finite-dimensional. **The proof's construction (extend a kernel basis, take images of the rest) is more useful than the equation itself** and is easy to miss, since it is buried in the proof rather than stated as the method. *(Theorem 5 does state it, one page later.)*
>
> **PDF extraction:** as in chapters 1–6, matrices and displayed formulas lose their structure. **`/bbR` is $\mathbb{R}$, `/cdots` is $\cdots$, `M mn` is $\mathbf M_{mn}$, `1V` is the identity transformation $1_V$, `ker` and `im` survive intact.** Composition symbols extract as `◦` correctly, but **the commutative diagrams of §7.3 are images and are lost** — they are the clearest statement of what $T\circ S$ and $T^{-1}$ mean, and the algebra alone is a poor substitute.
>
> **Verification performed:** this chapter is proof-based, so verification consisted of **checking every dimension count and every kernel/image claim in the exercises by hand**: $\ker$ and $\operatorname{im}$ for all four maps in Exercise 2, with the dimension theorem confirmed in each ($3=1+2$, $4=1+3$, $4=3+1$, $4=2+2$ — the last reusing the verified rank and bases from [[05 - The Vector Space Rn|ch. 05]]); the standard matrix in Exercise 4(i), **checked against both defining conditions**; and $\dim(\ker\operatorname{tr})=n^2-1$. **Nicholson's Example 5 (the maps $S:\mathbb{R}^3\to\mathbb{R}^2$ and $T:\mathbb{R}^2\to\mathbb{R}^3$) was verified, including that $(0,0,1)\notin\operatorname{im}T$ and $(0,0,1)\in\ker S$.**
>
> **Scope note:** **§7.4 (a theorem about differential equations) and §7.5 (more on linear recurrences) are omitted.** §7.4's content — that the solution space of an $n$th-order linear homogeneous ODE with constant coefficients has dimension exactly $n$ — **is stated in [[06 - Vector Spaces|ch. 06 §2]] because it is the best advertisement for the abstraction**, but its proof needs machinery beyond this course's scope. §7.5 is [[03 - Determinants and Diagonalization|ch. 03 §3c]] redone with linear-transformation language; **the computational content is identical and is already covered there.**

#linear-algebra #linear-transformation #kernel #image #dimension-theorem #rank-nullity #isomorphism #injective #surjective
