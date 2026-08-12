---
subject: Linear Algebra
chapter: 06
tags: [ds, linear-algebra, vector-space, axioms, subspace, basis, dimension, polynomials, function-spaces]
source: "Nicholson, *Linear Algebra with Applications*, 7th ed., ch. 6 (pp. 288–330)"
---

# Vector Spaces

> [!abstract] What this chapter is for
> **Chapter 5 proved a great deal about $\mathbb{R}^n$. This chapter observes that almost none of the proofs used $\mathbb{R}^n$.**
>
> Go back and look: the arguments for the Fundamental Theorem, the Invariance Theorem, "independent sets extend to bases", "spanning sets cut down to bases" — **none of them mention coordinates, lengths, or angles.** They use only that you can add vectors and multiply them by scalars, subject to some obvious rules. **So they apply to *anything* with those two operations.**
>
> And a great many things have them:
>
> | Space | Vectors are | Dimension |
> |---|---|---|
> | $\mathbb{R}^n$ | $n$-tuples | $n$ |
> | $\mathbf M_{mn}$ | $m\times n$ matrices | $mn$ |
> | $\mathbf P_n$ | polynomials of degree $\le n$ | $n+1$ |
> | $\mathbf P$ | all polynomials | **infinite** |
> | $\mathbf F[a,b]$ | functions on $[a,b]$ | **infinite** |
> | Solutions of $y''+y=0$ | functions | $2$ |
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | **The ten axioms** | What is *actually* required — and what is not |
> | **2** | Subspaces and spanning | Identical to ch. 5, minus the coordinates |
> | **3** | Independence and dimension | **The deferred proofs of ch. 5 are finally given** |
> | **4** | Finite-dimensional spaces | Extension/reduction to bases; $\dim(U+W)$ |
>
> **The payoff is not new computation but new *reach*.** Once you know $\mathbf P_3$ is 4-dimensional, every theorem about 4-dimensional spaces applies to polynomials — including the whole apparatus of bases, coordinates and rank.

---

## 📘 Main Knowledge

### 1. The axioms

> [!important] Definition 6.1
> A **vector space** is a set $V$ with an addition and a scalar multiplication satisfying, for all $\mathbf v,\mathbf w,\mathbf u\in V$ and scalars $a,b$:
>
> | | Addition | | Scalar multiplication |
> |---|---|---|---|
> | **A1** | $\mathbf v+\mathbf w\in V$ (**closure**) | **S1** | $a\mathbf v\in V$ (**closure**) |
> | **A2** | $\mathbf v+\mathbf w=\mathbf w+\mathbf v$ | **S2** | $a(\mathbf v+\mathbf w)=a\mathbf v+a\mathbf w$ |
> | **A3** | $\mathbf u+(\mathbf v+\mathbf w)=(\mathbf u+\mathbf v)+\mathbf w$ | **S3** | $(a+b)\mathbf v=a\mathbf v+b\mathbf v$ |
> | **A4** | there is $\mathbf 0$ with $\mathbf v+\mathbf 0=\mathbf v$ | **S4** | $a(b\mathbf v)=(ab)\mathbf v$ |
> | **A5** | each $\mathbf v$ has $-\mathbf v$ with $\mathbf v+(-\mathbf v)=\mathbf 0$ | **S5** | $1\mathbf v=\mathbf v$ |

> [!tip] Notice what is *not* on the list
> **No length. No angle. No dot product. No coordinates. No multiplication of two vectors.**
>
> **That is the point.** Everything chapter 5 proved about span, independence, basis and dimension used only these ten rules — so all of it transfers unchanged. **Orthogonality does *not* transfer**, because it needs a dot product, which is extra structure. *(Adding it back is what chapter 10 does, and what makes chapter 8 possible in $\mathbb{R}^n$.)*
>
> **The axioms also make clear how these results relate: $\mathbb{R}^n$ was never special — it was merely convenient.**

> [!important] Theorem 1 (§6.1) — the consequences you would otherwise assume
> In any vector space:
> $$0\mathbf v=\mathbf 0,\qquad a\mathbf 0=\mathbf 0,\qquad (-1)\mathbf v=-\mathbf v,\qquad a\mathbf v=\mathbf 0\Rightarrow a=0\text{ or }\mathbf v=\mathbf 0$$
>
> **None of these is an axiom** — each must be *proved* from the ten. For instance $0\mathbf v=\mathbf 0$ comes from S3: $0\mathbf v=(0+0)\mathbf v=0\mathbf v+0\mathbf v$, and adding $-(0\mathbf v)$ gives $\mathbf 0=0\mathbf v$.
>
> **Nicholson's remark is worth taking seriously: the *method* of proof matters more than the statements.** The style is "use only what the axioms allow", and it is the discipline the abstract half of the course is really teaching.

> [!example] Example 4 (§6.1) — a near-miss
> On ordered pairs with the usual addition but $a(x,y)=(ay,ax)$: axioms A1–A5, S1, S2, S3 all hold — **but S4 fails**, since
> $$a\big(b(x,y)\big)=a(by,bx)=(abx,aby)\quad\text{versus}\quad (ab)(x,y)=(aby,abx)$$
> **Eight axioms out of ten is not a vector space.** *(S5 fails too.)* **The axioms are not decorative; check them all.**

**The standard examples:**

- **$\mathbf M_{mn}$**, all $m\times n$ matrices — this is [[02 - Matrix Algebra|ch. 02]]'s Theorem 1, which listed exactly eight of the axioms. **$\mathbf M_{mn}$ is really $\mathbb{R}^{mn}$ in different notation.**
- **$\mathbf P$**, all polynomials, with coefficientwise operations; **$\mathbf P_n$**, those of degree $\le n$ **together with the zero polynomial**.
- **$\mathbf F[a,b]$**, all real functions on $[a,b]$, with pointwise operations.
- **Every subspace of $\mathbb{R}^n$**, with the inherited operations.

> [!warning] "$\mathbf P_n$ has degree at most $n$" — and the zero polynomial must be thrown in by hand
> **The set of polynomials of degree *exactly* $n$ is not a vector space:** it lacks $\mathbf 0$, and $(x^2+x)+(-x^2)=x$ leaves it. **Nicholson's definition says "degree at most $n$, together with the zero polynomial"** precisely because the degree of $0$ is undefined.
>
> **This is the same lesson as $U_2=\{x+2y-z=1\}$ in [[05 - The Vector Space Rn|ch. 05]]: conditions that are not homogeneous break closure.**

---

### 2. Subspaces and spanning (§6.2)

> [!important] Definition 6.2 and Theorem 1 (§6.2) — the subspace test
> $U\subseteq V$ is a **subspace** if it is itself a vector space under $V$'s operations. **Only three things need checking:**
> 1. $\mathbf 0\in U$;
> 2. closed under addition;
> 3. closed under scalar multiplication.
>
> **The other seven axioms are inherited automatically**, since they are identities that already hold in $V$.

**Span works verbatim:** $\operatorname{span}\{\mathbf v_1,\dots,\mathbf v_k\}$ is the set of all linear combinations, and (Theorem 2, §6.2) **it is the smallest subspace containing them.**

> [!example] Subspaces you meet constantly
> | Space | Subspace | Why |
> |---|---|---|
> | $\mathbf M_{nn}$ | symmetric matrices | $(A+B)^{\mathsf T}=A^{\mathsf T}+B^{\mathsf T}$ |
> | $\mathbf M_{nn}$ | matrices with $\operatorname{tr}A=0$ | trace is linear |
> | $\mathbf P$ | $\mathbf P_n$ | degree cannot increase |
> | $\mathbf P_n$ | $\{p:p(1)=0\}$ | evaluation is linear |
> | $\mathbf F[a,b]$ | continuous functions; differentiable functions | sums and multiples preserve these |
> | $\mathbf F(\mathbb{R})$ | solutions of $y''+y=0$ | **the equation is linear and homogeneous** |
>
> **The last row is the important one.** *The solution set of any linear homogeneous differential equation is a vector space* — which is exactly why "the general solution is $c_1y_1+c_2y_2$" is a sensible thing to say. **It is [[01 - Systems of Linear Equations|ch. 01]]'s "linear combinations of homogeneous solutions are solutions", in a space of functions.**

---

### 3. Independence and dimension (§6.3)

> [!important] Definition 6.4 — unchanged
> $\{\mathbf v_1,\dots,\mathbf v_k\}$ is **independent** if $t_1\mathbf v_1+\cdots+t_k\mathbf v_k=\mathbf 0$ forces all $t_i=0$.

> [!important] Theorems 2 and 3 (§6.3) — the debts of chapter 5, paid
> **Theorem 2 (Fundamental Theorem).** If $V$ is spanned by $n$ vectors and contains $m$ independent vectors, then $m\le n$.
>
> **Theorem 3 (Invariance Theorem).** Any two finite bases of $V$ have the same number of vectors — so $\dim V$ is well defined.
>
> **These are the results [[05 - The Vector Space Rn|ch. 05]] stated and deferred.** The proof of Theorem 2 is a careful exchange argument, and it is genuinely the hard theorem of the subject — everything about dimension rests on it.

**Dimensions of the standard spaces:**

$$\dim\mathbb{R}^n=n,\qquad \dim\mathbf M_{mn}=mn,\qquad \dim\mathbf P_n=n+1,\qquad \dim\{\mathbf 0\}=0$$

with bases $\{\mathbf e_i\}$, the matrix units $\{E_{ij}\}$, and $\{1,x,x^2,\dots,x^n\}$ respectively.

> [!warning] $\dim\mathbf P_n=n+1$, not $n$
> **The basis is $\{1,x,\dots,x^n\}$ — that is $n+1$ vectors, because the constants are included.** Off-by-one here propagates into every dimension count involving polynomials.

> [!important] Infinite-dimensional spaces are the norm, not the exception
> **$\mathbf P$ and $\mathbf F[a,b]$ have no finite basis.** For $\mathbf P$: any finite set has a maximum degree $d$, so its span misses $x^{d+1}$.
>
> **Most spaces that arise in analysis are infinite-dimensional**, and this course studies the finite-dimensional case because that is where bases behave. *(The infinite-dimensional theory needs convergence, hence norms — which is functional analysis, and where Fourier series live.)*

---

### 4. Finite-dimensional spaces (§6.4)

> [!important] Theorems 1, 2 and 4 (§6.4)
> Let $\dim V=n$.
> - **Every independent set can be extended to a basis** — and, in this edition, **using vectors from any prescribed basis.**
> - **Every spanning set can be cut down to a basis.**
> - **If $U\subseteq W$ then $\dim U\le\dim W$, with equality iff $U=W$.**
> - **If $|S|=\dim V$, then $S$ is independent $\iff$ $S$ spans $V$** — so only one needs checking.
>
> **These are chapter 5's Theorems 6–8, now proved in general.**

> [!important] Theorem 5 (§6.4) — the dimension formula for sums
> For subspaces $U,W$ of a finite-dimensional $V$:
> $$\boxed{\ \dim(U+W)=\dim U+\dim W-\dim(U\cap W)\ }$$
> where $U+W=\{\mathbf u+\mathbf w:\mathbf u\in U,\mathbf w\in W\}$.
>
> **This is inclusion–exclusion for dimensions**, and the analogy is exact: $|A\cup B|=|A|+|B|-|A\cap B|$. **When $U\cap W=\{\mathbf 0\}$ the sum is *direct*, written $U\oplus W$, and dimensions simply add** — which means every vector in $U\oplus W$ splits **uniquely** as $\mathbf u+\mathbf w$.

> [!tip] Why the intersection term must be there
> **Two planes through the origin in $\mathbb{R}^3$** have $\dim U=\dim W=2$, and their sum is all of $\mathbb{R}^3$ (unless they coincide). The formula gives $2+2-\dim(U\cap W)=3$, so $\dim(U\cap W)=1$: **two distinct planes through the origin always meet in a line.**
>
> **Note that $U\cup W$ is *not* a subspace** (it fails closure — [[05 - The Vector Space Rn|ch. 05]] Exercise 1(iv)); **$U+W$ is the smallest subspace containing both**, which is why the formula is about $+$ and not $\cup$.

---

## ✏️ Exercises

> [!question] Exercise 1 — checking the axioms *(warm-up)*
> Decide whether each is a vector space under the stated operations. Name a failing axiom where one fails.
> (i) $V=\mathbb{R}^2$ with $(x,y)+(x_1,y_1)=(x+x_1,\ y+y_1)$ and $a(x,y)=(ax,\,0)$.
> (ii) $V=\{(x,y)\in\mathbb{R}^2:x\ge0,\ y\ge0\}$ with the usual operations.
> (iii) $V=$ the set of polynomials of degree **exactly** 3.
> (iv) $V=\{f\in\mathbf F[0,1]:f(0)=0\}$.
> (v) $V=\{f\in\mathbf F[0,1]:f(0)=1\}$.

> [!example]- Solution
> **(i) No — S5 fails:** $1(x,y)=(x,0)\ne(x,y)$ whenever $y\ne0$.
> **S5 looks like the most trivial axiom and is exactly the one that catches this.** *(Without it, the map $a\mathbf v=\mathbf 0$ for all $a$ would satisfy everything else.)*
>
> **(ii) No — A5 fails:** $(1,1)\in V$ but $(-1,-1)\notin V$. **Equivalently S1 fails** for $a=-1$. **The first quadrant is closed under addition and under *positive* scaling, and that is not enough.**
>
> **(iii) No.** The zero polynomial is excluded, so **A4 fails**; and closure fails too, since $(x^3+x)+(-x^3)=x$ has degree 1. **"Degree exactly $n$" is never a subspace — this is why $\mathbf P_n$ is defined as "degree at most $n$, plus $0$".**
>
> **(iv) Yes.** The zero function satisfies $f(0)=0$; if $f(0)=g(0)=0$ then $(f+g)(0)=0$ and $(af)(0)=0$. **A homogeneous linear condition, so a subspace of $\mathbf F[0,1]$.**
>
> **(v) No** — the zero function has $f(0)=0\ne1$. **Also $(f+g)(0)=2$.** **Non-homogeneous condition, not a subspace.**
>
> > [!tip] The pattern across all five
> > **Every failure is either "$\mathbf 0$ is missing" or "closure breaks".** Conditions of the form *(linear expression) $=0$* always give subspaces; inequalities, non-zero right-hand sides, and "exactly" conditions never do.

> [!question] Exercise 2 — bases and dimensions of abstract spaces
> Find a basis and the dimension of each.
> (i) $\mathbf P_3$.
> (ii) $\mathbf M_{22}$.
> (iii) $U=\{A\in\mathbf M_{22}:A=A^{\mathsf T}\}$, the symmetric $2\times2$ matrices.
> (iv) $W=\{A\in\mathbf M_{22}:\operatorname{tr}A=0\}$.
> (v) $\{p\in\mathbf P_3:p(1)=0\}$.

> [!example]- Solution
> **(i)** $\{1,x,x^2,x^3\}$; $\dim\mathbf P_3=\boxed{4}$. **Independent because a polynomial is zero iff all its coefficients are** — which is the definition of "indeterminate", not a computation.
>
> **(ii)** The four matrix units $E_{11},E_{12},E_{21},E_{22}$; $\dim=\boxed{4}$.
>
> **(iii)** $A=\begin{bmatrix}a&b\\b&c\end{bmatrix}$, so
> $$U=\operatorname{span}\left\{\begin{bmatrix}1&0\\0&0\end{bmatrix},\begin{bmatrix}0&1\\1&0\end{bmatrix},\begin{bmatrix}0&0\\0&1\end{bmatrix}\right\},\qquad \dim U=\boxed{3}$$
> **Independent because the three basis matrices have their nonzero entries in disjoint positions.**
>
> **(iv)** $\operatorname{tr}A=0$ means $d=-a$, so $A=\begin{bmatrix}a&b\\c&-a\end{bmatrix}$ and
> $$W=\operatorname{span}\left\{\begin{bmatrix}1&0\\0&-1\end{bmatrix},\begin{bmatrix}0&1\\0&0\end{bmatrix},\begin{bmatrix}0&0\\1&0\end{bmatrix}\right\},\qquad \dim W=\boxed{3}$$
> **One linear condition on a 4-dimensional space leaves 3 dimensions** — which is rank–nullity for the map $A\mapsto\operatorname{tr}A$.
>
> **(v)** $p(1)=0$ means $(x-1)$ divides $p$, so $p=(x-1)q$ with $\deg q\le2$:
> $$\{x-1,\ x(x-1),\ x^2(x-1)\},\qquad \dim=\boxed{3}$$
> **Again one linear condition on a 4-dimensional space.** *(An equivalent basis is $\{x-1,x^2-1,x^3-1\}$ — bases are never unique.)*
>
> > [!important] The recurring count
> > **Each independent linear condition removes exactly one dimension.** (iii), (iv) and (v) are all "4 minus something", and in each case the something is the number of independent constraints. **This is rank–nullity before it has been stated for abstract maps** — [[07 - Linear Transformations|ch. 07]] makes it a theorem.

> [!question] Exercise 3 — independence in function spaces
> (i) Show $\{1,x,x^2\}$ is independent in $\mathbf P_2$.
> (ii) Show $\{\sin x,\cos x\}$ is independent in $\mathbf F(\mathbb{R})$.
> (iii) Is $\{1,\sin^2x,\cos^2x\}$ independent in $\mathbf F(\mathbb{R})$?
> (iv) Show $\{e^x,e^{2x}\}$ is independent.

> [!example]- Solution
> **(i)** Suppose $a+bx+cx^2=0$ **as a function**, i.e. for every $x$. Setting $x=0$ gives $a=0$; then $x=1$ and $x=-1$ give $b+c=0$ and $-b+c=0$, so $b=c=0$. $\blacksquare$
>
> *(Alternatively: a nonzero polynomial of degree $\le2$ has at most 2 roots, so one vanishing everywhere must be the zero polynomial.)*
>
> **(ii)** Suppose $a\sin x+b\cos x=0$ for all $x$. **Substitute convenient values:** $x=0$ gives $b=0$; $x=\pi/2$ gives $a=0$. $\blacksquare$
>
> **(iii) No.** $\sin^2x+\cos^2x=1$, so
> $$1\cdot(1)+(-1)\sin^2x+(-1)\cos^2x=0$$
> is a nontrivial dependence. **A trigonometric identity *is* a linear dependence** — and this is the general lesson: identities among functions are exactly the dependence relations in $\mathbf F(\mathbb{R})$.
>
> **(iv)** Suppose $ae^x+be^{2x}=0$ for all $x$. Divide by $e^x$ (never zero): $a+be^x=0$ for all $x$. **But $e^x$ is not constant**, so taking two different values of $x$ forces $b=0$, and then $a=0$. $\blacksquare$
>
> *(Alternatively differentiate: $ae^x+2be^{2x}=0$; subtracting the original gives $be^{2x}=0$, so $b=0$.)*
>
> > [!tip] The technique for function spaces
> > **"Substitute enough values of $x$"** turns an equation between functions into a linear system in the coefficients — usually the fastest route. **Differentiating is the other standard move**, and it generalises to the *Wronskian* test.
> >
> > **And the reason all of this works is that "$f=0$" in $\mathbf F(\mathbb{R})$ means $f(x)=0$ for *every* $x$**, which is a very strong condition. Independence in function spaces is therefore usually easy to establish and hard to refute — the exception being when an identity exists, as in (iii).

> [!question] Exercise 4 — extending and cutting down
> In $\mathbf P_2$ (so $\dim=3$):
> (i) Show $S=\{1+x,\ 1-x\}$ is independent, and extend it to a basis.
> (ii) Show $T=\{1,\ 1+x,\ x,\ x^2\}$ spans $\mathbf P_2$, and cut it down to a basis.
> (iii) Is $\{1+x^2,\ x+x^2,\ 1+x\}$ a basis of $\mathbf P_2$? Use the least possible work.

> [!example]- Solution
> **(i)** If $a(1+x)+b(1-x)=0$ then $(a+b)+(a-b)x=0$, so $a+b=0$ and $a-b=0$, giving $a=b=0$. **Independent.**
>
> Since $\dim\mathbf P_2=3$, one more vector is needed. **Try $x^2$:** if $a(1+x)+b(1-x)+cx^2=0$ then comparing coefficients gives $c=0$ and then $a=b=0$. **So $\{1+x,\ 1-x,\ x^2\}$ is independent, and having 3 vectors in a 3-dimensional space it is a basis by Theorem 4.**
>
> **(ii)** $T$ spans because $1$, $x=(1+x)-1$ and $x^2$ are all in $\operatorname{span}T$. **But $|T|=4>3$, so $T$ is dependent** — indeed $(1+x)-1-x=0$.
>
> **Cut down by deleting a vector that is a combination of the others:** delete $1+x$, leaving $\{1,x,x^2\}$ — the standard basis. *(Deleting $1$ or $x$ instead would work equally well; deleting $x^2$ would not, since nothing else can produce it.)*
>
> **(iii)** Three vectors in a 3-dimensional space, **so by Theorem 4 it suffices to check independence.** Suppose
> $$a(1+x^2)+b(x+x^2)+c(1+x)=0$$
> Collecting: constant $a+c=0$, coefficient of $x$: $b+c=0$, coefficient of $x^2$: $a+b=0$. Then $c=-a$, $b=-c=a$, and $a+b=2a=0$, so $a=b=c=0$.
>
> **Independent, hence a basis** — and no spanning check was needed. $\boxed{\text{Yes}}$
>
> **The system in (iii) is $\begin{bmatrix}1&0&1\\0&1&1\\1&1&0\end{bmatrix}\mathbf t=\mathbf 0$, whose determinant is $-2\ne0$** — the abstract question has become a $3\times3$ determinant, which is the whole benefit of having a basis to write coordinates in.

> [!question] Exercise 5 — the dimension formula *(hard)*
> (a) In $\mathbb{R}^4$, let $U=\operatorname{span}\{(1,0,0,0),(0,1,0,0),(0,0,1,0)\}$ and $W=\operatorname{span}\{(0,0,1,0),(0,0,0,1)\}$.
> (i) Find $\dim U$, $\dim W$, $U\cap W$ and $U+W$.
> (ii) Verify Theorem 5.
>
> (b) $U$ and $W$ are subspaces of a 10-dimensional space with $\dim U=6$ and $\dim W=7$.
> (i) What are the possible values of $\dim(U\cap W)$?
> (ii) Show $U\cap W\ne\{\mathbf 0\}$ — in fact $\dim(U\cap W)\ge3$.
>
> (c) Show that if $V=U\oplus W$ then every $\mathbf v\in V$ is $\mathbf u+\mathbf w$ in exactly one way.

> [!example]- Solution
> **(a)(i)** $\dim U=3$, $\dim W=2$. A vector in $U$ has last coordinate 0 and a vector in $W$ has first two coordinates 0, so
> $$U\cap W=\operatorname{span}\{(0,0,1,0)\},\qquad \dim(U\cap W)=1$$
> and $U+W$ contains all four standard basis vectors, so $U+W=\mathbb{R}^4$, $\dim=4$.
>
> **(ii)** $\ 4=3+2-1$ ✓
>
> **Note that $\dim U+\dim W=5>4=\dim\mathbb{R}^4$ — which *forced* an overlap.** That is the content of part (b).
>
> **(b)(i)** Two constraints:
> - $U\cap W\subseteq U$, so $\dim(U\cap W)\le6$.
> - $U+W\subseteq V$, so $\dim(U+W)\le10$; by Theorem 5,
> $$\dim(U\cap W)=\dim U+\dim W-\dim(U+W)\ge6+7-10=3$$
>
> Hence $\boxed{3\le\dim(U\cap W)\le6}$, and every value in that range occurs. *(At $\dim(U\cap W)=6$ we have $U\subseteq W$.)*
>
> **(ii)** In particular $\dim(U\cap W)\ge3>0$, so **$U\cap W$ contains nonzero vectors.** $\blacksquare$
>
> > [!important] "Too big to miss each other"
> > **Two subspaces whose dimensions sum to more than the whole space must intersect nontrivially.** This is the dimensional version of the pigeonhole principle, and it is the reason:
> > - two planes through the origin in $\mathbb{R}^3$ ($2+2>3$) always share a line;
> > - $n+1$ vectors in $\mathbb{R}^n$ are always dependent;
> > - **a linear map $\mathbb{R}^n\to\mathbb{R}^m$ with $n>m$ always has a nontrivial kernel** — [[01 - Systems of Linear Equations|ch. 01]]'s theorem that more variables than equations gives a nontrivial solution.
>
> **(c)** **Existence** is the definition of $U+W$. For **uniqueness**, suppose
> $$\mathbf u_1+\mathbf w_1=\mathbf u_2+\mathbf w_2,\qquad \mathbf u_i\in U,\ \mathbf w_i\in W$$
> Rearranging, $\mathbf u_1-\mathbf u_2=\mathbf w_2-\mathbf w_1$. **The left side lies in $U$ and the right side in $W$, so both lie in $U\cap W=\{\mathbf 0\}$.** Hence $\mathbf u_1=\mathbf u_2$ and $\mathbf w_1=\mathbf w_2$. $\blacksquare$
>
> **This is exactly the argument that independence gives unique coordinates** ([[05 - The Vector Space Rn|ch. 05 §2]]) — direct sums are the subspace-level version of independence, and $\dim(U\oplus W)=\dim U+\dim W$ is the corresponding count.
>
> **A concrete instance you have already used:** $\mathbf M_{nn}=\text{Sym}\oplus\text{Skew}$, with $A=\tfrac12(A+A^{\mathsf T})+\tfrac12(A-A^{\mathsf T})$ the unique decomposition ([[02 - Matrix Algebra|ch. 02]], Exercise 1(iv)). For $n=2$: $4=3+1$ ✓.

---

## 📝 Summary

- **A vector space is a set with addition and scalar multiplication satisfying ten axioms** — and **nothing about length, angle, coordinates, or multiplying two vectors.** Everything chapter 5 proved used only these, so all of it transfers.
- **The basic consequences ($0\mathbf v=\mathbf 0$, $(-1)\mathbf v=-\mathbf v$, $a\mathbf v=\mathbf 0\Rightarrow a=0$ or $\mathbf v=\mathbf 0$) are theorems, not axioms.**
- **Standard examples:** $\mathbb{R}^n$ ($\dim n$), $\mathbf M_{mn}$ ($\dim mn$), $\mathbf P_n$ ($\dim n+1$), and the infinite-dimensional $\mathbf P$ and $\mathbf F[a,b]$. **The solution set of a linear homogeneous ODE is a vector space** — which is why "the general solution is $c_1y_1+c_2y_2$" makes sense.
- **Subspace test: contains $\mathbf 0$, closed under $+$, closed under scaling.** The other seven axioms are inherited. **Homogeneous linear conditions give subspaces; "exactly degree $n$", inequalities and non-zero right-hand sides do not.**
- **The Fundamental Theorem ("independent $\le$ spanning") and the Invariance Theorem ("all bases have the same size") are proved here** — discharging the two debts of chapter 5. Everything about dimension rests on them.
- **In a space of dimension $n$: independent sets extend to bases, spanning sets cut down to bases, $U\subseteq W$ with equal dimension forces $U=W$, and a set of exactly $n$ vectors is independent iff it spans** — so only one property need be checked.
- **Each independent linear condition removes exactly one dimension** — symmetric $2\times2$ matrices ($4\to3$), trace-zero matrices ($4\to3$), $\{p\in\mathbf P_3:p(1)=0\}$ ($4\to3$).
- **Independence in function spaces** is usually settled by substituting convenient values of $x$, or by differentiating. **A trigonometric identity is a linear dependence**, which is why $\{1,\sin^2x,\cos^2x\}$ fails.
- $$\boxed{\dim(U+W)=\dim U+\dim W-\dim(U\cap W)}$$ **— inclusion–exclusion for dimensions.** When the intersection is trivial the sum is **direct**, dimensions add, and **every vector splits in exactly one way.**
- **If $\dim U+\dim W>\dim V$ the subspaces must intersect nontrivially** — the dimensional pigeonhole principle behind "two planes meet in a line" and "more unknowns than equations gives a nontrivial solution".

---

## ⚠️ Important Notes

> [!warning] Check all ten axioms, including the ones that look free
> **S5 ($1\mathbf v=\mathbf v$) and S4 ($a(b\mathbf v)=(ab)\mathbf v$) are the ones that fail in practice**, precisely because they look too obvious to state. Nicholson's Example 4 satisfies eight axioms and fails S4; Exercise 1(i) satisfies nine and fails S5.
>
> **Closure (A1, S1) is the other frequent failure**, and it is where every non-subspace in this chapter goes wrong.

> [!warning] $\dim\mathbf P_n=n+1$
> **Because the basis $\{1,x,\dots,x^n\}$ includes the constant.** Every dimension count involving polynomials inherits this off-by-one — e.g. $\{p\in\mathbf P_3:p(1)=0\}$ has dimension $4-1=3$, not $3-1=2$.
>
> **Related: the degree of the zero polynomial is undefined**, which is why $\mathbf P_n$ has to be defined as "degree at most $n$, *together with* $0$".

> [!warning] Orthogonality does **not** come along for the ride
> **The ten axioms give no dot product**, hence no length, angle, projection, orthogonal basis, or least squares. **Everything in [[04 - Vector Geometry|ch. 04]] and §5.3, §5.6 needs extra structure.**
>
> **What transfers:** span, independence, basis, dimension, rank, the dimension theorem, direct sums.
> **What does not:** anything involving $\cdot$, $\|\cdot\|$, or $\perp$.
>
> **Chapter 10 adds an inner product back as an axiom**, at which point Cauchy–Schwarz, Gram–Schmidt and Fourier expansions all reappear — in spaces of functions, where they become Fourier *series*.

> [!warning] $U\cup W$ is almost never a subspace; $U+W$ is the right object
> The union of the two coordinate axes in $\mathbb{R}^2$ contains $(1,0)$ and $(0,1)$ but not their sum. **$U+W$ is the smallest subspace containing both**, and it is what Theorem 5 measures.
>
> **The set-theoretic analogy is exact except for this:** $|A\cup B|=|A|+|B|-|A\cap B|$ counts a *union*, while the dimension formula concerns a *sum*.

> [!warning] Abstraction changes what a computation looks like, not whether one is needed
> **Choosing a basis turns any question in an $n$-dimensional space into a question in $\mathbb{R}^n$** — Exercise 4(iii) became a $3\times3$ determinant. **So abstraction never removes the computation; it only postpones the choice of coordinates.**
>
> **What it buys is that a theorem proved once covers polynomials, matrices, functions and $\mathbb{R}^n$ simultaneously** — and that you can choose the *most convenient* coordinates rather than being stuck with the given ones. **That freedom is what chapters 8 and 9 exploit.**

> [!note] Cross-subject connections
> - [[05 - The Vector Space Rn|Ch. 05]] — **this chapter is that one with $\mathbb{R}^n$ deleted from the hypotheses**, and it supplies the two proofs ch. 5 deferred.
> - [[07 - Linear Transformations|Ch. 07]] — maps between abstract spaces; **"each condition removes a dimension" becomes the dimension theorem.**
> - [[08 - Orthogonality|Ch. 08]] — needs a dot product, so it stays in $\mathbb{R}^n$; **ch. 10 generalises it by adding an inner product as an axiom.**
> - [[Calculus/contents/00-Index|Calculus]] — **the solution set of a linear homogeneous ODE is a vector space, and its dimension is the order of the equation.** Differentiation is a linear map on $\mathbf P_n$ and on function spaces (ch. 7).
> - [[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07]] — **random variables with finite variance form a vector space**, with $\mathbb{E}[XY]$ as inner product; conditional expectation is a projection, and independence-in-the-linear-algebra-sense is *uncorrelatedness*.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **feature spaces, embedding spaces and function classes are all vector spaces**; the kernel trick works precisely because an inner product is all the geometry that is needed.
> - [[Discrete Mathematics/contents/00-Index|Discrete Mathematics]] — vector spaces over finite fields underlie error-correcting codes (Nicholson §8.7).

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **This chapter is where two of chapter 5's deferred proofs are discharged** — the Fundamental Theorem (§6.3 Theorem 2) and the basis extension/reduction results (§6.4 Theorem 1). **A reader who follows Nicholson's own suggestion of stopping after chapter 5 therefore never sees them.** *(Flagged in [[05 - The Vector Space Rn|ch. 05]]'s gaps callout.)*
>
> **Source typos:**
> - **§6.1 Example 5 writes the sum of two polynomials as "$p(x)+q(x)=(a_0+b_0)+(a_1+b_1)x+\cdots$" but introduces the second polynomial's coefficients only after using them**, and the scalar multiple is printed as "$ap(x)=aa_0+(aa_1)x+\cdots$" where the first term should also be bracketed for consistency.
> - **§6.1, the footnote numbering runs 1, 2 on the same page as the definition**, and footnote 2's remark that "we will usually write the vectors in $\mathbb{R}^n$ as $n$-tuples" **contradicts the preface's stated new convention of writing them as columns** — the seventh edition changed the notation and the footnote was not updated.
> - **§7.2 Theorem 4's proof (quoted in [[07 - Linear Transformations|ch. 07]]) writes "$T(\mathbf v)$ lies in $\operatorname{im}V$"** where $\operatorname{im}T$ is meant.
>
> **PDF extraction:** matrices and displayed formulas suffer as in chapters 1–5. **Set-builder braces extract as `U … V`** (so `Pn = {a0 + a1x + /cdots + anxn | a0, …, an in /bbR}` is legible only because the pipe survives), **`/bbQ` is $\mathbb{Q}$, `/bbR` is $\mathbb{R}$, `M mn` is $\mathbf M_{mn}$** — and the last is badly mangled, appearing as `M / mn` across two lines in the sentence "$\mathbf M_{mn}$ is just $\mathbb{R}^{mn}$ in different notation". **Subscripts on $\mathbf P_n$ and $\mathbf F[a,b]$ detach throughout.** **All figures are images**, though this chapter has few and none carries essential content.
>
> **Verification performed:** this chapter contains almost no arithmetic — its content is proofs and definitions — so verification consisted of **checking every dimension claim and every basis in the exercises by hand**: $\dim\mathbf P_3=4$, $\dim\mathbf M_{22}=4$, the symmetric and trace-zero subspaces both of dimension 3, $\{p\in\mathbf P_3:p(1)=0\}$ of dimension 3 with the stated basis, the independence computations in Exercises 3 and 4 (including the determinant $-2$ for Exercise 4(iii)), and both parts of the dimension-formula arithmetic in Exercise 5. **Nicholson's Example 4 (the failure of S4) was verified symbolically.**
>
> **Scope note:** **§6.5 (an application to polynomials — Lagrange interpolation and the Wronskian-style independence results) and §6.6 (an application to differential equations) are omitted as separate sections.** Their content is folded in above: the interpolation result is [[01 - Systems of Linear Equations|ch. 01]]'s Exercise 5(c) and the Vandermonde determinant of [[03 - Determinants and Diagonalization|ch. 03]], and **the differential-equations material — that the solution space of a linear homogeneous ODE of order $n$ has dimension $n$ — is stated in §2 above** because it is the single most useful instance of the chapter's abstraction. **Nicholson proves that dimension claim only in §7.4**, which is itself outside the scope of these notes.

#linear-algebra #vector-space #axioms #subspace #basis #dimension #polynomials #function-spaces #direct-sum
