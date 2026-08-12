---
subject: Linear Algebra
chapter: 02
tags: [ds, linear-algebra, matrix-algebra, matrix-multiplication, inverse, linear-transformation, lu-factorization]
source: "Nicholson, *Linear Algebra with Applications*, 7th ed., ch. 2 (pp. 32–125)"
---

# Matrix Algebra

> [!abstract] What this chapter is for
> **Chapter 1 used matrices as bookkeeping. This chapter makes them objects with an algebra of their own — and then reveals what that algebra actually is.**
>
> $$\boxed{\text{A matrix is a function. Matrix multiplication is composition of functions.}}$$
>
> **Nicholson organises the entire chapter around this**, and it is why his treatment is worth following closely. He defines $AB$ by
> $$AB=[A\mathbf b_1\ \ A\mathbf b_2\ \ \cdots\ \ A\mathbf b_n]$$
> *precisely so that $AB$ means "do $B$, then do $A$"* — after which the strange-looking rules stop being strange. Associativity takes four lines. The reversal $(AB)^{-1}=B^{-1}A^{-1}$ becomes obvious (undo the last thing first). Non-commutativity becomes expected rather than surprising.
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Addition, scaling, **transpose** | Entrywise and unsurprising; symmetry ($A=A^{\mathsf T}$) matters later |
> | **2** | **$A\mathbf x$ as a linear combination of columns** | $A\mathbf x=\mathbf b$ is solvable $\iff$ $\mathbf b$ is in the span of the columns |
> | **3** | **Matrix multiplication** | $AB$ is composition; the dot-product rule is a computational consequence |
> | **4** | **Inverses** and the **Inverse Theorem** | Five conditions, all equivalent to invertibility |
> | **5** | Elementary matrices | Row operations *are* left-multiplications |
> | **6** | **Linear transformations** | Every linear $\mathbb{R}^n\to\mathbb{R}^m$ is a matrix, with columns $T(\mathbf e_j)$ |
> | **7** | **LU-factorization** | Do the $O(n^3)$ work once, reuse it for every right-hand side |
>
> **The Inverse Theorem (§4) is the chapter's centrepiece** and will keep growing: chapter 3 adds "$\det A\ne0$", chapter 5 adds "the columns are independent" and "the columns span $\mathbb{R}^n$".

---

## 📘 Main Knowledge

### 1. Addition, scalar multiplication, transposition

Matrices of the **same size** add entrywise, and $kA$ scales every entry.

> [!important] Theorem 1 (§2.1) — the eight rules
> For $m\times n$ matrices $A,B,C$ and scalars $k,p$:
>
> | | | | |
> |---|---|---|---|
> | 1. $A+B=B+A$ | 2. $A+(B+C)=(A+B)+C$ | 3. $0+A=A$ | 4. $A+(-A)=0$ |
> | 5. $k(A+B)=kA+kB$ | 6. $(k+p)A=kA+pA$ | 7. $(kp)A=k(pA)$ | 8. $1A=A$ |
>
> **These are exactly the vector-space axioms** (chapter 6), which is why matrices of a fixed size will turn out to *be* a vector space.

**Consequently you may expand, collect and factor exactly as with numbers** — Nicholson's Example 8 reduces a four-line expression to $2A-3B$ by pure schoolbook algebra. **Also $kA=0\iff k=0$ or $A=0$** (Example 7).

> [!important] Definition 2.3 — transpose
> $A^{\mathsf T}$ is the matrix whose **rows are the columns of $A$**, i.e.
> $$A=[a_{ij}]\ \Longrightarrow\ A^{\mathsf T}=[a_{ji}]$$
> **Geometrically: flip $A$ about its main diagonal $a_{11},a_{22},\dots$**

**Theorem 2 (§2.1):** $A^{\mathsf T}$ is $n\times m$; $(A^{\mathsf T})^{\mathsf T}=A$; $(kA)^{\mathsf T}=kA^{\mathsf T}$; $(A+B)^{\mathsf T}=A^{\mathsf T}+B^{\mathsf T}$.

> [!important] Symmetric matrices
> $A$ is **symmetric** if $A=A^{\mathsf T}$ — necessarily square, with entries mirrored across the diagonal.
>
> **Symmetry is not a curiosity; it is the single most important structural property in applied linear algebra.** Covariance matrices, Gram matrices $A^{\mathsf T}A$, Hessians and adjacency matrices of undirected graphs are all symmetric, and **chapter 8's spectral theorem says every symmetric matrix has an orthonormal basis of eigenvectors.** Sums of symmetric matrices are symmetric (Example 11); products generally are **not**.

---

### 2. Matrices, vectors, and transformations

> [!important] Definition 2.5 — the matrix–vector product
> For $A=[\mathbf a_1\ \mathbf a_2\ \cdots\ \mathbf a_n]$ ($m\times n$, written by columns) and $\mathbf x\in\mathbb{R}^n$,
> $$\boxed{\ A\mathbf x=x_1\mathbf a_1+x_2\mathbf a_2+\cdots+x_n\mathbf a_n\ }$$
> **$A\mathbf x$ is the linear combination of the columns of $A$ with the entries of $\mathbf x$ as coefficients.**

**This definition is the whole chapter in miniature, so it is worth dwelling on.** The left side of a linear system *is* such a combination:

$$\begin{aligned}3x_1+2x_2-4x_3&=0\\ x_1-3x_2+x_3&=3\\ x_2-5x_3&=-1\end{aligned}\quad\Longleftrightarrow\quad x_1\!\begin{bmatrix}3\\1\\0\end{bmatrix}+x_2\!\begin{bmatrix}2\\-3\\1\end{bmatrix}+x_3\!\begin{bmatrix}-4\\1\\-5\end{bmatrix}=\begin{bmatrix}0\\3\\-1\end{bmatrix}$$

> [!important] Theorem 1 (§2.2)
> 1. Every linear system is $A\mathbf x=\mathbf b$ with $A$ the coefficient matrix and $\mathbf b$ the constant column.
> 2. **$A\mathbf x=\mathbf b$ is consistent $\iff$ $\mathbf b$ is a linear combination of the columns of $A$.**
> 3. $\mathbf x$ solves the system $\iff$ its entries are coefficients making that combination equal $\mathbf b$.

> [!tip] Part 2 is a genuine change of viewpoint, not a restatement
> **"Solve the system" becomes "express $\mathbf b$ in terms of the columns of $A$."** Chapter 5 will name the set of all such $\mathbf b$ the **column space**, and part 2 becomes: *the system is consistent iff $\mathbf b\in\operatorname{col}A$.*
>
> **In data terms:** the columns of a design matrix are the predictors, and a response is exactly fittable iff it lies in their span. **When it does not — the usual case — least squares finds the closest point that is** ([[05 - The Vector Space Rn|ch. 05 §6]]).

**Theorem 2 (§2.2) — linearity of $\mathbf x\mapsto A\mathbf x$:**

$$A(\mathbf x+\mathbf y)=A\mathbf x+A\mathbf y,\qquad A(a\mathbf x)=a(A\mathbf x)=(aA)\mathbf x,\qquad (A+B)\mathbf x=A\mathbf x+B\mathbf x$$

> [!important] Theorem 3 (§2.2) — the structure of every solution set
> If $\mathbf x_1$ is **any** particular solution of $A\mathbf x=\mathbf b$, then every solution has the form
> $$\mathbf x=\mathbf x_1+\mathbf x_0,\qquad A\mathbf x_0=\mathbf 0$$
> **general solution $=$ one particular solution $+$ general solution of the homogeneous system.**

**The proof is one line:** if $A\mathbf x_2=\mathbf b$, set $\mathbf x_0=\mathbf x_2-\mathbf x_1$; then $A\mathbf x_0=\mathbf b-\mathbf b=\mathbf 0$.

> [!example] Example 7 (§2.2)
> The system $x_1-x_2-x_3+3x_4=2$, $2x_1-x_2-3x_3+4x_4=6$, $x_1-2x_3+x_4=4$ has general solution
> $$\mathbf x=\underbrace{\begin{bmatrix}4\\2\\0\\0\end{bmatrix}}_{\text{particular}}+\underbrace{s\begin{bmatrix}2\\1\\1\\0\end{bmatrix}+t\begin{bmatrix}-1\\2\\0\\1\end{bmatrix}}_{\text{homogeneous}}$$
>
> **Geometrically: the solution set is a plane through $(4,2,0,0)$ parallel to the plane of homogeneous solutions through the origin.** A linear system's solution set is never a subspace unless $\mathbf b=\mathbf 0$ — it is a *translate* of one.
>
> **The same decomposition reappears everywhere:** the general solution of a linear ODE is one particular solution plus the homogeneous family; in regression, fitted values plus residuals.

#### 2a. The dot-product rule

$$(a_1,\dots,a_n)\cdot(b_1,\dots,b_n)=a_1b_1+\cdots+a_nb_n$$

> [!important] Theorem 4 (§2.2)
> **Entry $i$ of $A\mathbf x$ is the dot product of row $i$ of $A$ with $\mathbf x$.**
>
> **Definition 2.5 (columns) says what $A\mathbf x$ *means*; the dot-product rule says how to *compute* it.** Keep both: the column view explains, the row view calculates.

#### 2b. Matrices as transformations

An $m\times n$ matrix $A$ defines a **matrix transformation** $T_A:\mathbb{R}^n\to\mathbb{R}^m$, $T_A(\mathbf x)=A\mathbf x$. In $\mathbb{R}^2$:

| Transformation | Matrix |
|---|---|
| Reflection in the $x$-axis | $\begin{bmatrix}1&0\\0&-1\end{bmatrix}$ |
| Reflection in the line $y=x$ | $\begin{bmatrix}0&1\\1&0\end{bmatrix}$ |
| Rotation by $\theta$ (counter-clockwise) | $\begin{bmatrix}\cos\theta&-\sin\theta\\ \sin\theta&\cos\theta\end{bmatrix}$ |
| Projection onto the $x$-axis | $\begin{bmatrix}1&0\\0&0\end{bmatrix}$ |
| Horizontal shear by $a$ | $\begin{bmatrix}1&a\\0&1\end{bmatrix}$ |

---

### 3. Matrix multiplication

> [!important] Definition 2.9
> For $A$ ($m\times n$) and $B=[\mathbf b_1\ \cdots\ \mathbf b_k]$ ($n\times k$),
> $$\boxed{\ AB=[A\mathbf b_1\ \ A\mathbf b_2\ \ \cdots\ \ A\mathbf b_k]\ }$$
> — **column $j$ of $AB$ is $A$ applied to column $j$ of $B$.**

> [!important] Theorem 1 (§2.3) — why this is the right definition
> $$A(B\mathbf x)=(AB)\mathbf x\qquad\text{for all }\mathbf x$$
> **$AB$ is the matrix of "do $B$, then do $A$".** Matrix multiplication is composition of transformations, and the definition was chosen to make that true.

> [!tip] Everything odd about matrix multiplication becomes ordinary
> | Fact | Reason once you think "composition" |
> |---|---|
> | $AB\ne BA$ | doing two things in the other order is a different thing |
> | $AB$ needs $\operatorname{cols}(A)=\operatorname{rows}(B)$ | $A$'s input must be $B$'s output |
> | $A(BC)=(AB)C$ | function composition is associative — **four lines, not three pages** |
> | $(AB)^{-1}=B^{-1}A^{-1}$ | to undo "$B$ then $A$", undo $A$ first |
> | $(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}$ | same reversal, different operation |

> [!important] Theorem 2 (§2.3) — the Dot Product Rule
> **The $(i,j)$-entry of $AB$ is the dot product of row $i$ of $A$ with column $j$ of $B$.**
>
> *Across row $i$ of $A$, down column $j$ of $B$, multiply and add.*

> [!example] Example 1 (§2.3)
> $$\begin{bmatrix}2&3&5\\1&4&7\\0&1&8\end{bmatrix}\begin{bmatrix}8&9\\7&2\\6&1\end{bmatrix}=\begin{bmatrix}67&29\\78&24\\55&10\end{bmatrix}$$
> *(Verified.)* By Definition 2.9 the first column is $8\binom{2}{1,0}+7\binom{3}{4,1}+6\binom{5}{7,8}$; by Theorem 2 the $(1,1)$-entry is $2(8)+3(7)+5(6)=67$. **Same answer, two readings.**

**Sizes:** $(m\times n)(n\times k)=(m\times k)$. **The inner dimensions must match and they disappear.**

#### 3a. Block multiplication

> [!important] Theorem 4 (§2.3)
> **If $A$ and $B$ are partitioned into compatible blocks, $AB$ can be computed by treating the blocks as entries.** Compatibility means: the column-count of each block of $A$ matches the row-count of the corresponding block of $B$.

Special case used constantly (Theorem 5):

$$\begin{bmatrix}B&X\\0&C\end{bmatrix}\begin{bmatrix}B_1&X_1\\0&C_1\end{bmatrix}=\begin{bmatrix}BB_1&BX_1+XC_1\\0&CC_1\end{bmatrix}$$

**Both $AB=[A\mathbf b_1\ \cdots]$ and $A\mathbf x=\sum x_j\mathbf a_j$ are themselves block multiplications** — Definition 2.9 is the case where $A$ is a single block. **Blocks are also how large matrix products are computed on machines with limited memory**, and how modern BLAS libraries get cache efficiency.

#### 3b. Directed graphs — multiplication with nothing to do with equations

For a digraph on $v_1,\dots,v_n$, the **adjacency matrix** has $a_{ij}=1$ if there is an edge $v_j\to v_i$ (**note the order**) and 0 otherwise.

> [!important] Theorem 6 (§2.3)
> **The $(i,j)$-entry of $A^r$ is the number of $r$-paths $v_j\to v_i$.**

> [!example] Nicholson's three-vertex example
> $$A=\begin{bmatrix}1&1&0\\1&0&1\\1&0&0\end{bmatrix},\quad A^2=\begin{bmatrix}2&1&1\\2&1&0\\1&1&0\end{bmatrix},\quad A^3=\begin{bmatrix}4&2&1\\3&2&1\\2&1&1\end{bmatrix}$$
> *(Verified.)* The $(2,1)$-entry of $A^2$ is 2, so there are two 2-paths $v_1\to v_2$; the $(2,3)$-entry is 0, so there are none $v_3\to v_2$. **$A^3$ has no zero entry, so every vertex reaches every vertex in exactly three steps.**
>
> **The induction is pure dot product:** every $(r+1)$-path $v_j\to v_i$ is an $r$-path $v_j\to v_k$ followed by an edge $v_k\to v_i$, and summing $a_{ik}b_{kj}$ over $k$ *is* the $(i,j)$-entry of $A^rA$.
>
> **This is the same computation as PageRank and as $n$-step transition probabilities in a Markov chain** ([[Probability Theory/contents/09 - Additional Topics in Probability|Probability ch. 09]]) — replace "number of paths" by "probability of paths" and Theorem 6 becomes Chapman–Kolmogorov.

---

### 4. Matrix inverses

$A$ ($n\times n$) is **invertible** if there is $B$ with $AB=BA=I_n$; then $B=A^{-1}$ is unique.

$$\begin{bmatrix}a&b\\c&d\end{bmatrix}^{-1}=\frac1{ad-bc}\begin{bmatrix}d&-b\\-c&a\end{bmatrix}\qquad\text{provided }ad-bc\ne0$$

> [!important] Theorem 2 (§2.4)
> If $A$ is invertible, $A\mathbf x=\mathbf b$ has the **unique** solution $\mathbf x=A^{-1}\mathbf b$.

> [!warning] This is a theorem, not a computational method
> **Never solve a linear system by forming $A^{-1}$ and multiplying.** It costs about three times as much as Gaussian elimination and is numerically worse. **$\mathbf x=A^{-1}\mathbf b$ is how you *think* about the solution; row reduction is how you *find* it.**
>
> The same warning applies in statistics: $\hat{\boldsymbol\beta}=(X^{\mathsf T}X)^{-1}X^{\mathsf T}\mathbf y$ is the formula, and **no competent implementation forms that inverse** — it solves the normal equations, or better, uses a QR factorization ([[08 - Orthogonality|ch. 08]]).

> [!important] The matrix inversion algorithm
> $$[\,A\ |\ I\,]\ \longrightarrow\ [\,I\ |\ A^{-1}\,]$$
> Row-reduce the **double matrix**, performing every operation on both halves. **If $A$ cannot be carried to $I$, it is not invertible.**
>
> **Why it works:** $AA^{-1}=I$ says $A\mathbf x_j=\mathbf e_j$ for each column $\mathbf x_j$ of $A^{-1}$ — $n$ systems with the **same** coefficient matrix, so the **same** row operations solve all of them at once.

> [!example] Example 6 (§2.4)
> $$A=\begin{bmatrix}2&7&1\\1&4&-1\\1&3&0\end{bmatrix}\qquad A^{-1}=\begin{bmatrix}-\tfrac32&-\tfrac32&\tfrac{11}2\\[2pt]\tfrac12&\tfrac12&-\tfrac32\\[2pt]\tfrac12&-\tfrac12&-\tfrac12\end{bmatrix}$$
> *(Verified; $\det A=-2$.)*

> [!important] Theorem 4 (§2.4) — the rules
> 1. $I^{-1}=I$  2. $(A^{-1})^{-1}=A$  3. $\boxed{(AB)^{-1}=B^{-1}A^{-1}}$
> 4. $(A_1A_2\cdots A_k)^{-1}=A_k^{-1}\cdots A_2^{-1}A_1^{-1}$  5. $(A^k)^{-1}=(A^{-1})^k$
> 6. $(aA)^{-1}=\tfrac1aA^{-1}$ for $a\ne0$  7. $\boxed{(A^{\mathsf T})^{-1}=(A^{-1})^{\mathsf T}}$

**Property 3 is verified by testing the candidate:** $(B^{-1}A^{-1})(AB)=B^{-1}(A^{-1}A)B=B^{-1}B=I$, and similarly the other way. **The order reversal is the "socks and shoes" rule** — to undo putting on socks then shoes, take off shoes then socks.

> [!important] Theorem 5 (§2.4) — the Inverse Theorem
> For an $n\times n$ matrix $A$, the following are **equivalent**:
> 1. $A$ is invertible.
> 2. $A\mathbf x=\mathbf 0$ has **only** the trivial solution.
> 3. $A$ can be carried to $I_n$ by row operations.
> 4. $A\mathbf x=\mathbf b$ has **at least one** solution for every $\mathbf b$.
> 5. There exists $C$ with $AC=I_n$.
>
> **Corollary 2: $A$ is invertible $\iff \operatorname{rank}A=n$.**

> [!tip] Why this theorem is the backbone of the course
> **Five very different-sounding statements collapse into one.** (2) is about uniqueness, (4) about existence, (3) about an algorithm, (5) about a one-sided inverse — **and for square matrices they are the same statement.**
>
> **The list keeps growing:** ch. 3 adds *$\det A\ne0$*; ch. 5 adds *the columns are independent*, *the columns span $\mathbb{R}^n$*, *the columns form a basis*, *$0$ is not an eigenvalue*. **By the end of the book there are a dozen entries, and knowing they are interchangeable is most of what "understanding linear algebra" means.**

> [!important] Corollary 1 (§2.4) — one-sided inverses are two-sided, for square matrices
> **If $A$ and $C$ are square and $AC=I$, then also $CA=I$.**
>
> **This fails badly for non-square matrices.** Nicholson's example:
> $$\begin{bmatrix}1&2&1\\1&1&1\end{bmatrix}\begin{bmatrix}-1&1\\1&-1\\0&1\end{bmatrix}=I_2\qquad\text{but}\qquad \begin{bmatrix}-1&1\\1&-1\\0&1\end{bmatrix}\begin{bmatrix}1&2&1\\1&1&1\end{bmatrix}=\begin{bmatrix}0&-1&0\\0&1&0\\1&1&1\end{bmatrix}\ne I_3$$
> *(Both verified.)* **A $2\times3$ matrix can have a right inverse but never a left one** — it maps $\mathbb{R}^3$ onto $\mathbb{R}^2$, losing a dimension that no map can restore. **"Inverse" is a genuinely two-sided notion, and squareness is what makes one side enough.**

**Theorem 6 (§2.4):** $A$ is invertible $\iff$ the transformation $T_A$ has an inverse, and then $(T_A)^{-1}=T_{A^{-1}}$. **Invertibility of a matrix is invertibility of the function it represents.**

---

### 5. Elementary matrices

An **elementary matrix** $E$ is obtained by performing **one** elementary row operation on $I$.

> [!important] The key fact
> **Performing a row operation on $A$ is the same as left-multiplying $A$ by the corresponding elementary matrix:**
> $$A\ \xrightarrow{\ \text{row op}\ }\ EA$$
> **Every elementary matrix is invertible**, and its inverse is the elementary matrix of the reverse operation ([[01 - Systems of Linear Equations|ch. 01 §2]]).

**Consequences.** If $A\to R$ by row operations then $R=E_k\cdots E_1A$ with each $E_i$ invertible; and

$$A\text{ is invertible}\iff A\text{ is a product of elementary matrices}$$

**Smith normal form:** for any $m\times n$ matrix $A$ of rank $r$ there are invertible $U,V$ with $UAV=\begin{bmatrix}I_r&0\\0&0\end{bmatrix}$ — **rank is the *only* invariant** once you may operate on both rows and columns.

> [!tip] This is also where a debt from chapter 1 is paid
> **The uniqueness of the reduced row-echelon form is proved at the end of §2.5** — which retroactively makes Definition 1.4 (rank) legitimate. *(The independence of the *number* of leading 1s still waits for chapter 5.)*

---

### 6. Linear transformations

> [!important] Definition 2.13
> $T:\mathbb{R}^n\to\mathbb{R}^m$ is a **linear transformation** if
> $$T(\mathbf x+\mathbf y)=T(\mathbf x)+T(\mathbf y)\qquad\text{and}\qquad T(a\mathbf x)=aT(\mathbf x)$$
> for all $\mathbf x,\mathbf y$ and scalars $a$.

> [!important] Theorem 2 (§2.6) — every linear map is a matrix
> **$T:\mathbb{R}^n\to\mathbb{R}^m$ is linear $\iff$ $T=T_A$ for a unique matrix $A$**, and
> $$\boxed{\ A=\big[\,T(\mathbf e_1)\ \ T(\mathbf e_2)\ \ \cdots\ \ T(\mathbf e_n)\,\big]\ }$$
> — **the columns of the standard matrix are the images of the standard basis vectors.**

**The proof is one computation:** $\mathbf x=x_1\mathbf e_1+\cdots+x_n\mathbf e_n$, so linearity gives $T(\mathbf x)=x_1T(\mathbf e_1)+\cdots+x_nT(\mathbf e_n)=A\mathbf x$.

> [!tip] "Linear transformation" and "matrix" are the same thing — with different emphases
> **A linear map is completely determined by what it does to $n$ vectors.** That is an extraordinary economy: to specify a function $\mathbb{R}^{1000}\to\mathbb{R}^{1000}$ you would normally need to say something about every one of uncountably many inputs; **linearity reduces it to $10^6$ numbers.**
>
> **To find the matrix of a geometric operation, just track $\mathbf e_1$ and $\mathbf e_2$.** Rotation by $\theta$ sends $\mathbf e_1\mapsto(\cos\theta,\sin\theta)$ and $\mathbf e_2\mapsto(-\sin\theta,\cos\theta)$ — **and those are the columns**, no trigonometric identities required.
>
> **This is also why every layer of a neural network is $\mathbf x\mapsto W\mathbf x+\mathbf b$ followed by a non-linearity:** without the non-linearity, composing layers would just multiply the $W$'s and the whole network would collapse to a single matrix.

---

### 7. LU-factorization

> [!important] The idea
> Write $A=LU$ with $L$ **lower** triangular and $U$ **upper** triangular (row-echelon). Then $A\mathbf x=\mathbf b$ becomes
> $$L\underbrace{(U\mathbf x)}_{\mathbf y}=\mathbf b:\qquad \text{solve } L\mathbf y=\mathbf b \text{ (forward)},\quad\text{then } U\mathbf x=\mathbf y \text{ (back)}$$
> **Two triangular solves, each $O(n^2)$, instead of one elimination at $O(n^3)$.**

> [!tip] Why factorization is the central idea of computational linear algebra
> **The factorization costs $O(n^3)$ once; each new right-hand side then costs only $O(n^2)$.** With $k$ right-hand sides, LU costs $O(n^3+kn^2)$ against $O(kn^3)$ for repeated elimination. **At $n=1000$ and $k=100$ that is a hundredfold saving.**
>
> **LU is the first of a family** — QR ([[08 - Orthogonality|ch. 08 §4]]), Cholesky (§8.3), eigendecomposition ([[03 - Determinants and Diagonalization|ch. 03]]), and the SVD (absent from this book — see [[00-Index]]). **In every case: pay once to change basis, then work in coordinates where the problem is easy.**
>
> **Caveat: not every matrix has an LU-factorization without row interchanges** — $\left[\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right]$ does not. In practice one computes $PA=LU$ with a permutation $P$, which is also what makes the algorithm numerically stable (partial pivoting).

---

### 8. Application: Markov chains (§2.9)

A **stochastic matrix** $P$ has non-negative entries and **columns summing to 1**; a **state vector** $\mathbf s$ has non-negative entries summing to 1. The chain evolves by

$$\mathbf s_{k+1}=P\mathbf s_k,\qquad\text{so}\qquad \mathbf s_k=P^k\mathbf s_0$$

> [!important] Steady state
> A **steady-state vector** satisfies $P\mathbf s=\mathbf s$ — **an eigenvector of $P$ for the eigenvalue 1** ([[03 - Determinants and Diagonalization|ch. 03]]). If some power of $P$ has all entries positive, $\mathbf s_k\to\mathbf s$ **whatever $\mathbf s_0$ is**.

> [!warning] Two conventions, and they are transposes of each other
> **Nicholson writes states as columns and stochastic matrices with columns summing to 1** ($\mathbf s_{k+1}=P\mathbf s_k$). **[[Probability Theory/contents/09 - Additional Topics in Probability|Probability ch. 09]] follows Ross: states as rows, transition matrices with *rows* summing to 1** ($\boldsymbol\pi=\boldsymbol\pi P$).
>
> **The two are transposes**, and every formula flips accordingly: Nicholson's steady state is a **right** eigenvector, Ross's is a **left** eigenvector. **Mixing them is a guaranteed error** — check which convention a source uses before copying a formula.

---

## ✏️ Exercises

> [!question] Exercise 1 — arithmetic, transpose, symmetry *(warm-up)*
> (i) With $A=\begin{bmatrix}3&-1&4\\2&0&6\end{bmatrix}$ and $B=\begin{bmatrix}1&2&-1\\0&3&2\end{bmatrix}$, compute $3A-2B$.
> (ii) Solve for $A$: $\ \left(2A^{\mathsf T}-3\begin{bmatrix}1&2\\-1&1\end{bmatrix}\right)^{\!\mathsf T}=\begin{bmatrix}2&3\\-1&2\end{bmatrix}$.
> (iii) Show that $A+A^{\mathsf T}$ is symmetric for **any** square $A$, and that $A-A^{\mathsf T}$ satisfies $(A-A^{\mathsf T})^{\mathsf T}=-(A-A^{\mathsf T})$.
> (iv) Deduce that every square matrix is the sum of a symmetric and a skew-symmetric matrix.

> [!example]- Solution
> **(i)** $3A=\begin{bmatrix}9&-3&12\\6&0&18\end{bmatrix}$, $2B=\begin{bmatrix}2&4&-2\\0&6&4\end{bmatrix}$, so
> $$3A-2B=\boxed{\begin{bmatrix}7&-7&14\\6&-6&14\end{bmatrix}}$$
>
> **(ii)** Transposition distributes over sums and scalars and $(A^{\mathsf T})^{\mathsf T}=A$, so the left side is $2A-3\begin{bmatrix}1&-1\\2&1\end{bmatrix}$. Hence
> $$2A=\begin{bmatrix}2&3\\-1&2\end{bmatrix}+3\begin{bmatrix}1&-1\\2&1\end{bmatrix}=\begin{bmatrix}5&0\\5&5\end{bmatrix}\ \Longrightarrow\ \boxed{A=\tfrac52\begin{bmatrix}1&0\\1&1\end{bmatrix}}$$
> *(Verified.)*
>
> **(iii)** $(A+A^{\mathsf T})^{\mathsf T}=A^{\mathsf T}+(A^{\mathsf T})^{\mathsf T}=A^{\mathsf T}+A=A+A^{\mathsf T}$ ✓
> $(A-A^{\mathsf T})^{\mathsf T}=A^{\mathsf T}-A=-(A-A^{\mathsf T})$ ✓ — such a matrix is **skew-symmetric**.
>
> **(iv)** $$A=\underbrace{\tfrac12(A+A^{\mathsf T})}_{\text{symmetric}}+\underbrace{\tfrac12(A-A^{\mathsf T})}_{\text{skew}}$$
> and the decomposition is **unique** (if $A=S+K$ with $S$ symmetric and $K$ skew, transposing gives $A^{\mathsf T}=S-K$, and adding/subtracting recovers $S$ and $K$).
>
> > [!tip] Why this matters
> > **The symmetric part carries the "stretching" and the skew part the "rotating."** For a Hessian, only the symmetric part exists; for a general Jacobian, the split separates deformation from rotation. **And symmetric matrices are exactly the ones chapter 8 can orthogonally diagonalize**, so this decomposition says how far a matrix is from being well behaved.

> [!question] Exercise 2 — what matrix multiplication does *not* do
> Give explicit $2\times2$ examples showing each of the following, and explain each using "matrix $=$ function".
>
> (i) $AB\ne BA$ in general.
> (ii) $AB=0$ with $A\ne0$ and $B\ne0$.
> (iii) $AB=AC$ with $A\ne0$ but $B\ne C$.
> (iv) $A^2=0$ with $A\ne0$.
> (v) Which of (i)–(iv) become impossible if $A$ is invertible?

> [!example]- Solution
> **(i)** Let $R=\begin{bmatrix}0&-1\\1&0\end{bmatrix}$ (rotation by $90°$) and $F=\begin{bmatrix}1&0\\0&-1\end{bmatrix}$ (reflection in the $x$-axis):
> $$FR=\begin{bmatrix}0&-1\\-1&0\end{bmatrix}\ (\text{reflection in }y=-x),\qquad RF=\begin{bmatrix}0&1\\1&0\end{bmatrix}\ (\text{reflection in }y=x)$$
> *(Both verified.)* **Rotate-then-reflect and reflect-then-rotate are genuinely different motions** — the two results are reflections in perpendicular lines. **This is what non-commutativity *is*.**
>
> **(ii)** $A=\begin{bmatrix}1&1\\1&1\end{bmatrix}$, $B=\begin{bmatrix}1&-1\\-1&1\end{bmatrix}$ give $AB=0$.
> **As functions: $B$ collapses everything onto the line spanned by $(1,-1)$, and $A$ sends that line to $\mathbf 0$.** Neither map is zero, but the *composite* is. **Non-zero matrices can annihilate each other because each destroys different information.**
>
> **(iii)** $A=\begin{bmatrix}1&0\\0&0\end{bmatrix}$, $B=\begin{bmatrix}1&2\\3&4\end{bmatrix}$, $C=\begin{bmatrix}1&2\\5&6\end{bmatrix}$: both products are $\begin{bmatrix}1&2\\0&0\end{bmatrix}$.
> **$A$ throws away the second row, so $B$ and $C$ differ only in information $A$ discards.** Cancellation requires that no information be lost.
>
> **(iv)** $A=\begin{bmatrix}0&1\\0&0\end{bmatrix}$ has $A^2=0$. **$A$ maps $\mathbb{R}^2$ onto the $x$-axis and the $x$-axis to $\mathbf 0$** — apply it twice and everything vanishes. *(Such a matrix is **nilpotent**; it is never diagonalizable, which ch. 3 will explain.)*
>
> **(v) All four.**
> - (ii): $AB=0$ with $A$ invertible gives $B=A^{-1}(AB)=A^{-1}0=0$.
> - (iii): $AB=AC$ gives $B=A^{-1}AB=A^{-1}AC=C$.
> - (iv): $A^2=0$ gives $A=A^{-1}A^2=0$, contradicting invertibility.
> - (i) still fails in general — **invertibility does not buy commutativity** ($R$ and $F$ above are both invertible).
>
> > [!important] The unifying reason
> > **An invertible matrix loses no information** — it is a bijection. (ii)–(iv) are all failures caused by *collapse*, and a bijection cannot collapse anything. **Non-commutativity is different in kind: it is about *order*, not about loss**, and no amount of invertibility removes it.

> [!question] Exercise 3 — inverses
> (i) Invert $A=\begin{bmatrix}1&2&3\\0&1&4\\5&6&0\end{bmatrix}$ by the algorithm $[A\,|\,I]\to[I\,|\,A^{-1}]$.
> (ii) Use it to solve $A\mathbf x=(1,0,0)^{\mathsf T}$, and say why you would not do this in practice.
> (iii) If $A$ and $B$ are invertible $n\times n$, simplify $\left(A^{-1}B\right)^{-1}\!\left(B^{\mathsf T}A\right)^{\mathsf T}$.
> (iv) Suppose $A$ is $n\times n$ with $A^3=0$. Show $I-A$ is invertible and find its inverse.

> [!example]- Solution
> **(i)** Row-reducing the double matrix gives
> $$\boxed{A^{-1}=\begin{bmatrix}-24&18&5\\20&-15&-4\\-5&4&1\end{bmatrix}}$$
> *(Verified; $\det A=1$, which is why every entry is an integer.)*
>
> **(ii)** $\mathbf x=A^{-1}(1,0,0)^{\mathsf T}=(-24,20,-5)^{\mathsf T}$ — the **first column** of $A^{-1}$.
>
> **Why not in practice:** computing $A^{-1}$ solves $n$ systems ($A\mathbf x_j=\mathbf e_j$) when you only wanted one, costing roughly three times as much, and the extra arithmetic amplifies rounding error. **Row-reduce $[A\,|\,\mathbf b]$ instead** — or factor once with LU if there will be many right-hand sides.
>
> **(iii)** $\left(A^{-1}B\right)^{-1}=B^{-1}A$ and $\left(B^{\mathsf T}A\right)^{\mathsf T}=A^{\mathsf T}B$, so the product is
> $$B^{-1}A\,A^{\mathsf T}B$$
> **which does not simplify further** — and in particular is **not** $AA^{\mathsf T}$, because $B^{-1}$ and $B$ are separated by matrices that need not commute with them. **Both reversal rules were used; watch the order every time.**
>
> **(iv)** Guess from the geometric series $\frac1{1-a}=1+a+a^2+\cdots$, which terminates here because $A^3=0$:
> $$(I-A)(I+A+A^2)=I+A+A^2-A-A^2-A^3=I-A^3=I$$
> and the same product in the other order gives $I$ too. Hence
> $$\boxed{(I-A)^{-1}=I+A+A^2}$$
> *(By Corollary 1, checking one side would have sufficed, since both matrices are square.)*
>
> > [!tip] The general principle
> > **If $A^k=0$ then $(I-A)^{-1}=I+A+\cdots+A^{k-1}$** — a *finite* geometric series. This is the algebraic heart of the **Leontief input–output model** (§2.8), where $(I-A)^{-1}$ converts final demand into total production and the series $I+A+A^2+\cdots$ counts inputs, inputs-of-inputs, and so on. **A convergent infinite version of the same identity is what makes that model economically meaningful.**

> [!question] Exercise 4 — transformations and their matrices
> (i) Find the standard matrix of $R_\theta$, rotation of $\mathbb{R}^2$ by $\theta$ counter-clockwise, by tracking $\mathbf e_1$ and $\mathbf e_2$.
> (ii) Verify $R_\alpha R_\beta=R_{\alpha+\beta}$ and say what identity this proves.
> (iii) Find the matrix $P$ of projection onto the $x$-axis. Show $P^2=P$ and explain geometrically. Is $P$ invertible?
> (iv) $T:\mathbb{R}^3\to\mathbb{R}^2$ satisfies $T(1,0,0)=(2,1)$, $T(0,1,0)=(-1,3)$, $T(1,1,1)=(4,4)$. Find its standard matrix.

> [!example]- Solution
> **(i)** Rotation sends $\mathbf e_1=(1,0)$ to $(\cos\theta,\sin\theta)$ and $\mathbf e_2=(0,1)$ to $(-\sin\theta,\cos\theta)$. **Those are the columns:**
> $$R_\theta=\begin{bmatrix}\cos\theta&-\sin\theta\\ \sin\theta&\cos\theta\end{bmatrix}$$
> **No trigonometry beyond reading off two points** — that is the value of "columns are images of basis vectors."
>
> **(ii)** Multiplying,
> $$R_\alpha R_\beta=\begin{bmatrix}\cos\alpha\cos\beta-\sin\alpha\sin\beta&-(\cos\alpha\sin\beta+\sin\alpha\cos\beta)\\ \sin\alpha\cos\beta+\cos\alpha\sin\beta&\cos\alpha\cos\beta-\sin\alpha\sin\beta\end{bmatrix}$$
> and this equals $R_{\alpha+\beta}$ precisely because
> $$\cos(\alpha+\beta)=\cos\alpha\cos\beta-\sin\alpha\sin\beta,\qquad \sin(\alpha+\beta)=\sin\alpha\cos\beta+\cos\alpha\sin\beta$$
> **The matrix identity *is* the angle-addition formulas** — rotating by $\beta$ then $\alpha$ is rotating by $\alpha+\beta$, which is geometrically obvious, so the trigonometric identities come for free. **This is one of the few places where linear algebra proves something you already believed for an independent reason.**
>
> *(Note $R_\alpha R_\beta=R_\beta R_\alpha$ — rotations of the plane **do** commute, which is exactly why plane rotations are so much simpler than rotations in $\mathbb{R}^3$.)*
>
> **(iii)** $P(\mathbf e_1)=\mathbf e_1$ and $P(\mathbf e_2)=\mathbf 0$, so $P=\begin{bmatrix}1&0\\0&0\end{bmatrix}$ and $P^2=P$.
>
> **Geometrically: projecting something already flattened onto the $x$-axis does nothing.** A matrix with $P^2=P$ is called **idempotent**, and idempotence is exactly what "projection" means algebraically — a fact chapter 8 leans on entirely.
>
> **$P$ is not invertible:** $P(0,1)=\mathbf 0=P(0,0)$, so it is not injective — and by the Inverse Theorem, $P\mathbf x=\mathbf 0$ having a nontrivial solution settles it. **Projections destroy information by design, so no projection onto a proper subspace is ever invertible.**
>
> **(iv)** Columns 1 and 2 are given directly: $T(\mathbf e_1)=(2,1)$, $T(\mathbf e_2)=(-1,3)$. For the third, use linearity:
> $$T(\mathbf e_3)=T(1,1,1)-T(\mathbf e_1)-T(\mathbf e_2)=(4,4)-(2,1)-(-1,3)=(3,0)$$
> $$\boxed{A=\begin{bmatrix}2&-1&3\\1&3&0\end{bmatrix}}$$
> **Three vectors spanning $\mathbb{R}^3$ determine $T$ completely** — and they need not be the standard basis, only a spanning set.

> [!question] Exercise 5 — the Inverse Theorem, paths, and steady states *(hard)*
> **(a)** Let $A$ be $n\times n$. Prove each, using the Inverse Theorem rather than determinants.
> (i) If $A^2=A$ and $A\ne I$, then $A$ is not invertible.
> (ii) If the columns of $A$ satisfy $\mathbf a_1+\mathbf a_2=2\mathbf a_3$, then $A$ is not invertible.
> (iii) If $A$ is invertible and $AB=AC$, then $B=C$.
>
> **(b)** A directed graph on $\{v_1,v_2,v_3\}$ has adjacency matrix $A=\begin{bmatrix}1&1&0\\1&0&1\\1&0&0\end{bmatrix}$ (entry $a_{ij}=1$ iff there is an edge $v_j\to v_i$).
> (i) How many 2-paths go $v_1\to v_2$? List them.
> (ii) How many 3-paths go $v_3\to v_1$?
> (iii) What does it mean that $A^3$ has no zero entry?
>
> **(c)** A market has two brands. Each year 20% of brand-A customers switch to B and 30% of brand-B customers switch to A. With states as columns and $P$ column-stochastic, find the transition matrix, the steady state, and the market share after 10 years starting from 100% brand A.

> [!example]- Solution
> **(a)(i)** Suppose $A$ were invertible. Then $A^2=A$ gives $A=A^{-1}A^2=A^{-1}A=I$, contradicting $A\ne I$. $\blacksquare$
> **In words: the only invertible idempotent is the identity** — every other projection collapses something.
>
> **(ii)** The relation $\mathbf a_1+\mathbf a_2-2\mathbf a_3=\mathbf 0$ says $A\mathbf x=\mathbf 0$ for $\mathbf x=(1,1,-2,0,\dots,0)^{\mathsf T}\ne\mathbf 0$, since $A\mathbf x$ is the linear combination of columns with those coefficients (Definition 2.5). **By condition (2) of the Inverse Theorem, $A$ is not invertible.** $\blacksquare$
>
> **This is the general statement: any linear dependence among the columns kills invertibility**, which is the ch. 1 observation ("a nontrivial solution of $A\mathbf x=\mathbf 0$ is a column dependence") read through Theorem 5.
>
> **(iii)** Left-multiply by $A^{-1}$: $B=IB=A^{-1}AB=A^{-1}AC=IC=C$. $\blacksquare$
> **Note the multiplication must be on the *left*, because $AB=AC$ has $A$ on the left.** From $BA=CA$ you would right-multiply instead.
>
> **(b)(i)** The $(2,1)$-entry of $A^2=\begin{bmatrix}2&1&1\\2&1&0\\1&1&0\end{bmatrix}$ is $\mathbf 2$. The paths are $v_1\to v_1\to v_2$ and $v_1\to v_3\to v_2$. *(Verified.)*
>
> **(ii)** The $(1,3)$-entry of $A^3=\begin{bmatrix}4&2&1\\3&2&1\\2&1&1\end{bmatrix}$ is $\mathbf 1$ — exactly one 3-path $v_3\to v_1$.
>
> **(iii)** **Every vertex can reach every vertex in exactly three steps.** In Markov-chain language this is precisely Ross's **ergodicity condition** $P^{(n)}_{ij}>0$ for all $i,j$ ([[Probability Theory/contents/09 - Additional Topics in Probability|Probability ch. 09 §2]]) — the hypothesis that guarantees a limiting distribution independent of the starting state.
>
> **(c)** Columns are "from", rows are "to", so brand A retains 80% and brand B retains 70%:
> $$P=\begin{bmatrix}0.8&0.3\\0.2&0.7\end{bmatrix}$$
> **Steady state** solves $(P-I)\mathbf s=\mathbf 0$, i.e. $-0.2s_1+0.3s_2=0$, so $s_1:s_2=3:2$; normalising,
> $$\boxed{\mathbf s=\begin{bmatrix}0.6\\0.4\end{bmatrix}}$$
> **After 10 years from $\mathbf s_0=(1,0)$:** $P^{10}\mathbf s_0=(0.6004,\ 0.3996)$ — *(verified)* — **already indistinguishable from the steady state.**
>
> > [!important] The two eigenvalues explain both halves of the answer
> > $P$ has eigenvalues $1$ and $0.5$ *(verified)*. **The eigenvalue 1 gives the steady state; the eigenvalue $0.5$ governs how fast you get there** — the deviation from $\mathbf s$ shrinks by half each year, so after 10 years it is $2^{-10}\approx0.001$ of its initial size, matching the fourth decimal place above.
> >
> > **This is exactly the "spectral gap" of [[Probability Theory/contents/09 - Additional Topics in Probability|Probability ch. 09]], and chapter 3 will make it a theorem.** The stationary distribution tells you *where*; the second eigenvalue tells you *when*.

---

## 📝 Summary

- **A matrix is a function and matrix multiplication is composition.** Nicholson's definition $AB=[A\mathbf b_1\ \cdots\ A\mathbf b_k]$ is chosen so that $A(B\mathbf x)=(AB)\mathbf x$ — and every awkward rule (non-commutativity, size requirements, the reversals in $(AB)^{-1}$ and $(AB)^{\mathsf T}$) follows from that reading.
- **Addition and scalar multiplication obey the eight rules of Theorem 1** — which are the vector-space axioms, making the $m\times n$ matrices a vector space (ch. 6).
- **$A^{\mathsf T}=[a_{ji}]$ is a flip about the main diagonal.** $A$ is **symmetric** if $A=A^{\mathsf T}$; every square matrix splits uniquely as symmetric $+$ skew.
- **$A\mathbf x$ is the linear combination of the columns of $A$** with entries of $\mathbf x$ as coefficients. **Hence $A\mathbf x=\mathbf b$ is consistent iff $\mathbf b$ lies in the span of the columns** — the column-space criterion, in advance.
- **The dot-product rule computes; the column definition explains.** Entry $(i,j)$ of $AB$ is row $i$ of $A$ dotted with column $j$ of $B$.
- **Every solution set is a particular solution plus the homogeneous solutions** (Theorem 3), so the solution set of $A\mathbf x=\mathbf b$ is a *translate* of the solution set of $A\mathbf x=\mathbf 0$.
- **Block multiplication works whenever the partitions are compatible**, and both $A\mathbf x$ and $AB$ are special cases of it.
- **The $(i,j)$-entry of $A^r$ counts $r$-paths** in a directed graph — the same computation as $n$-step transition probabilities and as PageRank.
- **Inverses:** $\mathbf x=A^{-1}\mathbf b$ is the *concept*, not the *method*; compute by $[A\,|\,I]\to[I\,|\,A^{-1}]$, and solve systems by elimination instead. **$(AB)^{-1}=B^{-1}A^{-1}$ and $(A^{\mathsf T})^{-1}=(A^{-1})^{\mathsf T}$** — the order reverses.
- **The Inverse Theorem: invertible $\iff$ $A\mathbf x=\mathbf 0$ only trivially $\iff$ $A\to I$ by row operations $\iff$ $A\mathbf x=\mathbf b$ always solvable $\iff$ $AC=I$ for some $C$ $\iff$ $\operatorname{rank}A=n$.** Five different-sounding statements, one property — and the list grows in chapters 3 and 5.
- **For square matrices a one-sided inverse is two-sided** (Corollary 1); for rectangular ones it is not, because a map between spaces of different dimensions must collapse or miss.
- **Row operations are left-multiplications by elementary matrices**, so $A$ is invertible iff it is a product of elementary matrices — and §2.5 finally proves the reduced row-echelon form is unique.
- **Every linear $T:\mathbb{R}^n\to\mathbb{R}^m$ is $T_A$ with $A=[T(\mathbf e_1)\ \cdots\ T(\mathbf e_n)]$.** A linear map is determined by what it does to $n$ vectors — an enormous economy, and the fastest way to write down geometric matrices.
- **LU-factorization pays $O(n^3)$ once and $O(n^2)$ per right-hand side.** It is the first instance of the governing idea of computational linear algebra: **factor into pieces where the problem is easy.**
- **A Markov chain's steady state is an eigenvector for eigenvalue 1**, and the second-largest eigenvalue controls how fast the chain forgets its start. **Beware the two conventions** — Nicholson's columns sum to 1, Ross's rows do.

---

## ⚠️ Important Notes

> [!warning] The reversals: $(AB)^{-1}=B^{-1}A^{-1}$ and $(AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}$
> **Writing $(AB)^{-1}=A^{-1}B^{-1}$ is the most common algebraic error in the chapter.**
>
> **Socks and shoes:** to undo "socks then shoes", take off shoes then socks. Since $AB$ means "$B$ first, then $A$", undoing it means undoing $A$ first.
>
> **Note also which side you may multiply on.** From $B=C$ you may deduce $AB=AC$ *or* $BA=CA$ — but **never $AB=CA$.** Nicholson's counterexample: $A=\left[\begin{smallmatrix}1&1\\0&1\end{smallmatrix}\right]$, $B=C=\left[\begin{smallmatrix}0&0\\1&0\end{smallmatrix}\right]$.

> [!warning] Three cancellation laws that fail
> | Number algebra | Matrix algebra |
> |---|---|
> | $ab=ba$ | **false** |
> | $ab=0\Rightarrow a=0$ or $b=0$ | **false** |
> | $ab=ac,\ a\ne0\Rightarrow b=c$ | **false** |
>
> **All three failures have the same cause: a non-zero matrix can still destroy information.** An invertible matrix cannot, which is why invertibility repairs the last two — **but not the first.** Non-commutativity is about order, not loss, and survives invertibility (rotations and reflections are all invertible and still do not commute).

> [!warning] Never compute an inverse to solve a system
> $$\mathbf x=A^{-1}\mathbf b\quad\text{(true)}\qquad\ne\qquad\text{how to find }\mathbf x\quad\text{(false)}$$
> **Forming $A^{-1}$ solves $n$ systems when you wanted one**, costs about $3\times$ as much, and loses accuracy. **Row-reduce $[A\,|\,\mathbf b]$**, or use LU when there are many right-hand sides.
>
> **The same warning is the standard one in numerical statistics:** $\hat{\boldsymbol\beta}=(X^{\mathsf T}X)^{-1}X^{\mathsf T}\mathbf y$ is a formula, not an algorithm — forming $X^{\mathsf T}X$ *squares the condition number*, which is why QR ([[08 - Orthogonality|ch. 08]]) is preferred.

> [!warning] One-sided inverses need squareness
> **$AC=I$ implies $CA=I$ only when $A$ and $C$ are square.** For rectangular matrices the two sides genuinely differ: a $2\times3$ matrix has a right inverse and cannot have a left one.
>
> **The reason is dimensional.** A map $\mathbb{R}^3\to\mathbb{R}^2$ must collapse a whole line to $\mathbf 0$, and nothing can restore it; a map $\mathbb{R}^2\to\mathbb{R}^3$ cannot be onto, so nothing can precede it to cover $\mathbb{R}^3$. **This is the seed of the rank–nullity theorem.**

> [!warning] Two Markov conventions, differing by a transpose
> | | State | Stochastic matrix | Steady state |
> |---|---|---|---|
> | **Nicholson (§2.9)** | column $\mathbf s$ | **columns** sum to 1 | $P\mathbf s=\mathbf s$ (**right** eigenvector) |
> | **Ross ([[Probability Theory/contents/09 - Additional Topics in Probability\|Probability ch. 09]])** | row $\boldsymbol\pi$ | **rows** sum to 1 | $\boldsymbol\pi P=\boldsymbol\pi$ (**left** eigenvector) |
>
> **Check the convention before copying any formula.** A quick test: sum a column of the matrix — if you get 1, you are in Nicholson's world.

> [!warning] Not every matrix has an LU-factorization
> $\left[\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right]$ has none, because the algorithm needs a nonzero pivot in the top-left corner. **The fix is a permutation: $PA=LU$** — which is also, and not coincidentally, what makes the computation numerically stable (partial pivoting chooses the *largest* available pivot, not merely a nonzero one).
>
> **This is the general shape of numerical linear algebra: the clean theorem needs a hypothesis, and the practical algorithm supplies it by reordering.**

> [!note] Cross-subject connections
> - [[01 - Systems of Linear Equations|Ch. 01]] — row operations become **left-multiplication by elementary matrices** (§2.5), and §2.5 finally proves the reduced row-echelon form is unique.
> - [[03 - Determinants and Diagonalization|Ch. 03]] — **$\det A\ne0$ joins the Inverse Theorem**; the Markov steady state of §2.9 is an eigenvector, and the second eigenvalue is the convergence rate.
> - [[05 - The Vector Space Rn|Ch. 05]] — "the columns span" and "the columns are independent" join the Inverse Theorem; **Definition 2.5 is what makes the column space the right object.**
> - [[07 - Linear Transformations|Ch. 07]] — §2.6 done for abstract spaces; the standard matrix becomes "the matrix relative to a basis" (ch. 9).
> - [[08 - Orthogonality|Ch. 08]] — **symmetric matrices (§2.1) are the whole subject there**, and idempotent matrices (Exercise 4(iii)) are exactly the projections.
> - [[Probability Theory/contents/09 - Additional Topics in Probability|Probability ch. 09]] — **§2.9 and §2.3's path-counting are Markov chains**; $A^r$ counting paths and $P^{(n)}$ giving $n$-step probabilities are the same theorem.
> - [[Econometrics/contents/00-Index|Econometrics]] — $\hat{\boldsymbol\beta}=(X^{\mathsf T}X)^{-1}X^{\mathsf T}\mathbf y$ is this chapter's notation; **the "do not invert" warning is the practical content of every numerical-stability discussion there.**
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **a network layer is $\mathbf x\mapsto W\mathbf x+\mathbf b$; without a non-linearity between layers the composite collapses to one matrix**, which is Theorem 1 of §2.3 read as a limitation.
> - [[Data Structures and Algorithms/contents/00-Index|Data Structures and Algorithms]] — LU is the canonical "preprocess once, query cheaply" trade-off; block multiplication is how cache-efficient matrix libraries are written.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **Source typos, several in load-bearing places:**
> - **Definition 2.5 — the definition of the matrix–vector product — is printed wrongly.** The text gives
> $$\text{“}A\mathbf x=x_1\mathbf a_1+x_1\mathbf a_2+x_1\mathbf a_n\text{”}$$
> — **every coefficient is $x_1$ and the $\cdots$ is missing.** It should be $x_1\mathbf a_1+x_2\mathbf a_2+\cdots+x_n\mathbf a_n$, as the surrounding prose ("the coefficients are the entries of $\mathbf x$, in order") and every subsequent example make clear. **This is the chapter's central definition.**
> - **The proof of Theorem 2 (§2.2) prints $A+B=[\mathbf a_1+\mathbf b_1\ \ \mathbf a_2+\mathbf b_1\ \cdots\ \mathbf a_n+\mathbf b_n]$** — the second entry should be $\mathbf a_2+\mathbf b_2$.
> - **Theorem 1 (§2.2) says "$X$ is the matrix of variables"** with a capital $X$ while the rest of the theorem and the whole chapter use lower-case bold $\mathbf x$; the following paragraph then refers to "the constant matrix $B$" where $\mathbf b$ is meant.
> - **§2.4 Example 10 justifies the final step "by Theorem 4(2)"**, but Theorem 4(2) is $(A^{-1})^{-1}=A$; the step actually used is $(A^{\mathsf T})^{\mathsf T}=A$, which is **Theorem 2(2) of §2.1**.
> - **The sentence after Corollary 1 (§2.4) reads "Observe that Corollary 2 is false if $A$ and $C$ are not square"** — it is **Corollary 1** that is being discussed; Corollary 2 (rank $=n$) has not yet been stated at that point.
> - **§2.1, after Theorem 1:** the illustration of the distributive law prints $k(A+B-C)=kA+kC-kC$, which should be $kA+kB-kC$.
> - **§2.3, block multiplication:** the display $B\mathbf x=x_1\mathbf b_1+x_2\mathbf b_2+\cdots+x_k\mathbf b_k]$ has an **unmatched closing bracket**.
>
> **PDF extraction — every matrix is destroyed:**
> - **Matrices lose their delimiters, their row structure and the position of their minus signs.** $\left[\begin{smallmatrix}2&7&1\\1&4&-1\\1&3&0\end{smallmatrix}\right]$ extracts as `27 1 / 14 1 / 13 0` with a stray `−` on a separate line. **Every matrix in these notes has been reconstructed by hand and then verified by recomputing the example's printed answer.**
> - **`S … T` is a large bracket** delimiting a matrix or column vector, and **`U`, `e`, `u` at the start of a display are large braces** grouping a system — so `U 5x1 - 3x2 = -4 / 7x1 + 4x2 = 8` is a braced pair of equations, not an expression involving $U$.
> - **Superscripts detach:** $A^{-1}$ appears variously as `A-1`, `A–1`, `A -1` and ` A  k  -1 `, and in Theorem 4's proof the expression $A_k^{-1}A_{k-1}^{-1}\cdots A_1^{-1}$ extracts across five lines.
> - **`/bbR` is $\mathbb{R}$, `/cdots` is $\cdots$, `/vdots` is $\vdots$, `/uni25ba.001` marks the start of a solution, `1_{/bbRn}` is the identity transformation on $\mathbb{R}^n$.**
> - **All figures are images**: the diagram for the dot-product rule (row $i$ across, column $j$ down), the composition diagram $\mathbb{R}^k\to\mathbb{R}^n\to\mathbb{R}^m$, the directed graph of §2.3, and every geometric picture of reflections, rotations, shears and projections in §§2.2 and 2.6. **The transformation pictures matter most** — the standard matrices are stated algebraically in the text and are recoverable, but the pictures that make them memorable are gone.
>
> **Verification performed:** every worked example quoted in these notes was independently recomputed. Confirmed: $3A-2B=\left[\begin{smallmatrix}7&-7&14\\6&-6&14\end{smallmatrix}\right]$ (§2.1 Ex. 6); $A=\tfrac52\left[\begin{smallmatrix}1&0\\1&1\end{smallmatrix}\right]$ (§2.1 Ex. 10); $AB=\left[\begin{smallmatrix}67&29\\78&24\\55&10\end{smallmatrix}\right]$ (§2.3 Ex. 1); **both $A^2$ and $A^3$ of the directed-graph example, entry by entry** (§2.3); $\det A=41$ and $\mathbf x=\left(\tfrac8{41},\tfrac{68}{41}\right)$ (§2.4 Ex. 5); $A=\left[\begin{smallmatrix}2&1\\-1&4\end{smallmatrix}\right]$ (§2.4 Ex. 10); the full inverse in §2.4 Ex. 6 ($\det=-2$); and **both products in the Corollary 1 counterexample**, confirming $PQ=I_2$ while $QP\ne I_3$. **All agree with the text.** The only defects found are the typographical ones listed above; **no computational error was found in this chapter.**
>
> **Scope note:** §2.8 (Leontief input–output models) is omitted — its mathematical content is the identity $(I-A)^{-1}=I+A+A^2+\cdots$, which appears in Exercise 3(iv) in its finite form, and the economics belongs in [[Macroeconomics/contents/00-Index|Macroeconomics]]. **§2.9 (Markov chains) is kept in summary** because it is the same object as [[Probability Theory/contents/09 - Additional Topics in Probability|Probability ch. 09 §2]] and the convention clash between the two sources is worth documenting. §§2.5 and 2.7 are given in outline: **elementary matrices matter mainly for the theorem that row-reduction is left-multiplication**, and LU matters mainly as the first example of "factor once, reuse many times."

#linear-algebra #matrix-algebra #matrix-multiplication #inverse #inverse-theorem #linear-transformation #lu-factorization #markov-chain
