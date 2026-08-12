---
subject: Linear Algebra
chapter: 04
tags: [ds, linear-algebra, vector-geometry, dot-product, projection, cross-product, planes, orthogonality]
source: "Nicholson, *Linear Algebra with Applications*, 7th ed., ch. 4 (pp. 184–228)"
---

# Vector Geometry

> [!abstract] What this chapter is for
> **This is the chapter that makes the rest of the book visual.** Everything so far has been algebra with arrays; here vectors get **length** and **direction**, and two products appear that turn algebraic statements into geometric ones.
>
> | Product | Input | Output | Measures |
> |---|---|---|---|
> | **Dot** $\mathbf v\cdot\mathbf w$ | two vectors, any $\mathbb{R}^n$ | a **scalar** | how much they point the same way |
> | **Cross** $\mathbf v\times\mathbf w$ | two vectors, **$\mathbb{R}^3$ only** | a **vector** | the plane they span, and its area |
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Vectors, length, lines | $\|\mathbf v\|=\sqrt{\mathbf v\cdot\mathbf v}$; a line is a point plus a direction |
> | **2** | **Dot product and projection** | $\mathbf v\cdot\mathbf w=\|\mathbf v\|\|\mathbf w\|\cos\theta$; **orthogonal $\iff$ dot product zero** |
> | **2b** | Planes | A plane is a point plus a **normal** |
> | **3** | **Cross product** | $\|\mathbf v\times\mathbf w\|$ is area; the triple product is volume |
> | **4** | Operators on $\mathbb{R}^3$ | Projection and reflection matrices, derived not memorised |
>
> **The single most important formula in the chapter is the projection:**
> $$\operatorname{proj}_{\mathbf d}\mathbf u=\frac{\mathbf u\cdot\mathbf d}{\|\mathbf d\|^2}\,\mathbf d$$
> **Least squares, orthogonal bases, Gram–Schmidt, QR, regression fitted values and PCA are all this formula, generalised.** If you take one thing from chapter 4 into chapters 5 and 8, take this.

---

## 📘 Main Knowledge

### 1. Vectors, length, and lines

A vector in $\mathbb{R}^3$ is written as a column $\mathbf v=\begin{bmatrix}x\\y\\z\end{bmatrix}$, and identified with the arrow from the origin to $(x,y,z)$. **Two arrows represent the same vector iff they have the same length and direction** — position is irrelevant.

> [!important] Length, and the operations
> $$\|\mathbf v\|=\sqrt{x^2+y^2+z^2}=\sqrt{\mathbf v\cdot\mathbf v}$$
>
> - **Addition is the parallelogram law** (equivalently, tip-to-tail).
> - **$k\mathbf v$ scales the length by $|k|$** and reverses direction if $k<0$; so $\|k\mathbf v\|=|k|\,\|\mathbf v\|$.
> - **$\mathbf v$ and $\mathbf w$ are parallel iff $\mathbf w=k\mathbf v$ for some scalar $k$.**
> - **A unit vector is $\dfrac{\mathbf v}{\|\mathbf v\|}$** — same direction, length 1. *(Normalising is the single most-used small operation in the subject.)*
> - The distance between points $P$ and $Q$ is $\|\overrightarrow{PQ}\|$, where $\overrightarrow{PQ}=\mathbf q-\mathbf p$.

> [!important] Lines
> The line through $P_0$ (position vector $\mathbf p_0$) with **direction vector** $\mathbf d\ne\mathbf 0$:
> $$\mathbf p=\mathbf p_0+t\,\mathbf d,\qquad t\in\mathbb{R}$$
> or in coordinates, $x=x_0+ta$, $y=y_0+tb$, $z=z_0+tc$.

> [!tip] "A point plus a direction" is the pattern for everything
> | Object | Description |
> |---|---|
> | Line in $\mathbb{R}^3$ | one point $+$ **one** direction |
> | Plane in $\mathbb{R}^3$ | one point $+$ **two** directions (or one **normal**) |
> | Solution set of $A\mathbf x=\mathbf b$ | one particular solution $+$ the homogeneous solutions |
>
> **The third row is [[02 - Matrix Algebra|ch. 02]]'s Theorem 3, and it is the same statement.** A line through the origin is the solution set of a homogeneous system; a line not through the origin is a *translate* of one. **In chapter 5 these become "subspace" and "coset of a subspace".**

---

### 2. The dot product

$$\mathbf v\cdot\mathbf w=v_1w_1+v_2w_2+v_3w_3\qquad(\text{equivalently }\mathbf v^{\mathsf T}\mathbf w)$$

> [!important] Theorem 1 (§4.2) — the rules
> 1. $\mathbf v\cdot\mathbf w$ is a **scalar**  2. $\mathbf v\cdot\mathbf w=\mathbf w\cdot\mathbf v$  3. $\mathbf v\cdot\mathbf 0=0$
> 4. $\boxed{\mathbf v\cdot\mathbf v=\|\mathbf v\|^2}$  5. $(k\mathbf v)\cdot\mathbf w=k(\mathbf v\cdot\mathbf w)=\mathbf v\cdot(k\mathbf w)$  6. $\mathbf u\cdot(\mathbf v\pm\mathbf w)=\mathbf u\cdot\mathbf v\pm\mathbf u\cdot\mathbf w$
>
> **Properties 5 and 6 say the dot product is *bilinear*** — linear in each argument separately — so you may expand $(\mathbf v-3\mathbf w)\cdot(\mathbf v-3\mathbf w)$ exactly like $(a-3b)^2$, **remembering that $\mathbf v\cdot\mathbf v=\|\mathbf v\|^2$.**

> [!important] Theorem 2 (§4.2) — the geometric meaning
> If $\mathbf v,\mathbf w\ne\mathbf 0$ and $\theta\in[0,\pi]$ is the angle between them,
> $$\boxed{\ \mathbf v\cdot\mathbf w=\|\mathbf v\|\,\|\mathbf w\|\cos\theta\ }\qquad\text{so}\qquad \cos\theta=\frac{\mathbf v\cdot\mathbf w}{\|\mathbf v\|\,\|\mathbf w\|}$$

**The proof computes $\|\mathbf v-\mathbf w\|^2$ twice** — once by the law of cosines, once by expanding the dot product — and compares. **Nothing deeper is involved, but the consequence is the whole of orthogonality.**

> [!important] Reading the sign
> | | Meaning |
> |---|---|
> | $\mathbf v\cdot\mathbf w>0$ | $\theta$ acute — the vectors broadly agree |
> | $\mathbf v\cdot\mathbf w=0$ | $\theta=\pi/2$ — **orthogonal** |
> | $\mathbf v\cdot\mathbf w<0$ | $\theta$ obtuse — they broadly oppose |
>
> **Definition: $\mathbf v$ and $\mathbf w$ are orthogonal if $\mathbf v\cdot\mathbf w=0$** — which by convention includes the case where one of them is $\mathbf 0$. *(The zero vector is orthogonal to everything, which is convenient and occasionally surprising.)*

> [!example] Example 3 (§4.2)
> $\mathbf u=(-1,1,2)$, $\mathbf v=(2,1,-1)$: $\ \mathbf u\cdot\mathbf v=-2+1-2=-3$, $\|\mathbf u\|=\|\mathbf v\|=\sqrt6$, so
> $$\cos\theta=\frac{-3}{6}=-\tfrac12\qquad\Longrightarrow\qquad \theta=\frac{2\pi}{3}=120°$$
> *(Verified.)*

> [!tip] The dot product is where "angle" comes from, not the other way round
> **In $\mathbb{R}^2$ and $\mathbb{R}^3$ you already know what an angle is, and Theorem 2 is a theorem.** In $\mathbb{R}^{100}$ — or in a space of functions, or of polynomials — **there is no prior notion of angle, and the formula becomes the *definition*.**
>
> **This is the move chapter 10 makes for abstract inner-product spaces**, and it is why cosine similarity between document vectors is a sensible quantity: it is literally the cosine of an angle in $\mathbb{R}^{\text{vocabulary}}$.

#### 2a. Projection — the formula that runs the rest of the book

> [!important] Definition 4.6 and Theorem 4 (§4.2)
> For $\mathbf d\ne\mathbf 0$, the **projection of $\mathbf u$ on $\mathbf d$** is
> $$\boxed{\ \operatorname{proj}_{\mathbf d}\mathbf u=\frac{\mathbf u\cdot\mathbf d}{\|\mathbf d\|^2}\,\mathbf d\ }$$
> and **$\mathbf u-\operatorname{proj}_{\mathbf d}\mathbf u$ is orthogonal to $\mathbf d$.**

**The derivation is the whole idea and takes two lines.** The projection must be parallel to $\mathbf d$, so $\mathbf u_1=t\mathbf d$; the leftover must be perpendicular, so

$$0=(\mathbf u-t\mathbf d)\cdot\mathbf d=\mathbf u\cdot\mathbf d-t\|\mathbf d\|^2\quad\Longrightarrow\quad t=\frac{\mathbf u\cdot\mathbf d}{\|\mathbf d\|^2}$$

> [!important] The orthogonal decomposition
> $$\mathbf u=\underbrace{\operatorname{proj}_{\mathbf d}\mathbf u}_{\text{parallel to }\mathbf d}+\underbrace{\left(\mathbf u-\operatorname{proj}_{\mathbf d}\mathbf u\right)}_{\text{orthogonal to }\mathbf d}$$
> **Every vector splits uniquely into a component along a direction and a component perpendicular to it.** *(Note $\|\mathbf d\|$ does not matter — only its direction — since $\mathbf d$ appears once upstairs and twice downstairs. If $\mathbf d$ is a **unit** vector the formula collapses to $(\mathbf u\cdot\mathbf d)\mathbf d$.)*

> [!example] Example 7 (§4.2)
> $\mathbf u=(2,-3,1)$ on $\mathbf d=(1,-1,3)$: $\ \mathbf u\cdot\mathbf d=8$, $\|\mathbf d\|^2=11$, so
> $$\mathbf u_1=\tfrac8{11}(1,-1,3),\qquad \mathbf u_2=\mathbf u-\mathbf u_1=\tfrac1{11}(14,-25,-13)$$
> *(Verified, including $\mathbf d\cdot\mathbf u_2=0$.)*

> [!example] Example 8 (§4.2) — distance from a point to a line
> $P(1,3,-2)$, line through $P_0(2,0,-1)$ with $\mathbf d=(1,-1,0)$. With $\mathbf u=\overrightarrow{P_0P}=(-1,3,-1)$:
> $$\operatorname{proj}_{\mathbf d}\mathbf u=\tfrac{-4}{2}(1,-1,0)=(-2,2,0),\qquad \mathbf u-\operatorname{proj}_{\mathbf d}\mathbf u=(1,1,-1)$$
> **Distance $=\sqrt3$**, and the closest point is $Q=P_0+\operatorname{proj}_{\mathbf d}\mathbf u=(0,2,-1)$. *(Verified.)*
>
> **The pattern — "project, then take what is left over" — is the entire method for every distance problem in the chapter, and for least squares in [[05 - The Vector Space Rn|ch. 05 §6]].**

#### 2b. Planes

> [!important] Definition 4.7 and the equations of a plane
> A **normal** to a plane is a nonzero vector orthogonal to every vector lying in it. The plane through $P_0(x_0,y_0,z_0)$ with normal $\mathbf n=(a,b,c)$:
> $$a(x-x_0)+b(y-y_0)+c(z-z_0)=0\qquad\Longleftrightarrow\qquad \mathbf n\cdot(\mathbf p-\mathbf p_0)=0$$
> and every plane with normal $\mathbf n$ has an equation
> $$ax+by+cz=d\qquad\Longleftrightarrow\qquad \mathbf n\cdot\mathbf p=d$$

> [!tip] Read the coefficients as the normal
> **Given $2x-3y+z=7$, the normal is $(2,-3,1)$ — just read it off.** Consequently:
> - **two planes are parallel iff their normals are parallel** (Example 10: the plane through $(3,-1,2)$ parallel to $2x-3y=6$ is $2x-3y=9$, since $d=2(3)-3(-1)=9$);
> - the angle between two planes is the angle between their normals;
> - a line is parallel to a plane iff its direction is **orthogonal** to the normal.

> [!important] Distance from a point to a plane
> $$\text{dist}\big(P,\ ax+by+cz=d\big)=\frac{|ax_1+by_1+cz_1-d|}{\sqrt{a^2+b^2+c^2}}=\frac{|\mathbf n\cdot\mathbf p-d|}{\|\mathbf n\|}$$

> [!example] Example 11 (§4.2)
> $P(2,1,-3)$ and $3x-y+4z=1$: distance $=\dfrac{|6-1-12-1|}{\sqrt{26}}=\dfrac{8}{\sqrt{26}}\approx1.569$. *(Verified.)*
>
> **This is again "project and take the leftover":** pick any point $P_0$ on the plane, and the distance is $\|\operatorname{proj}_{\mathbf n}\overrightarrow{P_0P}\|$ — the component of the displacement *along* the normal.

---

### 3. The cross product

> [!important] Definition 4.8
> For $\mathbf v=(v_1,v_2,v_3)$ and $\mathbf w=(w_1,w_2,w_3)$ in $\mathbb{R}^3$:
> $$\mathbf v\times\mathbf w=\det\begin{bmatrix}\mathbf i&\mathbf j&\mathbf k\\ v_1&v_2&v_3\\ w_1&w_2&w_3\end{bmatrix}=(v_2w_3-v_3w_2)\mathbf i-(v_1w_3-v_3w_1)\mathbf j+(v_1w_2-v_2w_1)\mathbf k$$
> **The "determinant" has vectors in its first row, so it is a mnemonic rather than a determinant — but it is exactly the right mnemonic.**

> [!important] Theorem 5 (§4.2) and Theorems 1–5 (§4.3)
> 1. **$\mathbf v\times\mathbf w$ is orthogonal to both $\mathbf v$ and $\mathbf w$.**
> 2. For nonzero $\mathbf v,\mathbf w$: **$\mathbf v\times\mathbf w=\mathbf 0\iff\mathbf v$ and $\mathbf w$ are parallel.**
> 3. $\boxed{\|\mathbf v\times\mathbf w\|=\|\mathbf v\|\,\|\mathbf w\|\sin\theta}$ — **the area of the parallelogram they span.**
> 4. $\mathbf w\times\mathbf v=-(\mathbf v\times\mathbf w)$ — **anticommutative.**
> 5. **Triple product:** $\mathbf u\cdot(\mathbf v\times\mathbf w)=\det\begin{bmatrix}\mathbf u\\ \mathbf v\\ \mathbf w\end{bmatrix}$, whose absolute value is the **volume** of the parallelepiped.

> [!tip] Dot and cross are complementary detectors
> $$\mathbf v\cdot\mathbf w=0\iff\text{perpendicular},\qquad \mathbf v\times\mathbf w=\mathbf 0\iff\text{parallel}$$
> $$\mathbf v\cdot\mathbf w=\|\mathbf v\|\|\mathbf w\|\cos\theta,\qquad \|\mathbf v\times\mathbf w\|=\|\mathbf v\|\|\mathbf w\|\sin\theta$$
> **One measures agreement, the other measures spread**, and $(\mathbf v\cdot\mathbf w)^2+\|\mathbf v\times\mathbf w\|^2=\|\mathbf v\|^2\|\mathbf w\|^2$ — Pythagoras in disguise.

> [!example] Example 13 (§4.2) — a plane through three points
> $P(1,3,-2)$, $Q(1,1,5)$, $R(2,-2,3)$. Then $\overrightarrow{PQ}=(0,-2,7)$ and $\overrightarrow{PR}=(1,-5,5)$ lie in the plane, so
> $$\mathbf n=\overrightarrow{PQ}\times\overrightarrow{PR}=(25,7,2)$$
> and the plane is $25x+7y+2z=d$ with $d=25(1)+7(3)+2(-2)=42$. *(Verified.)*
>
> **This is the standard use of the cross product: it converts "two directions in the plane" into "one normal", which is the form the equation needs.**

> [!warning] The cross product exists only in $\mathbb{R}^3$
> **There is no cross product in $\mathbb{R}^2$, $\mathbb{R}^4$ or $\mathbb{R}^n$** — the construction is special to three dimensions. *(A genuine analogue exists only in $\mathbb{R}^7$, for reasons far outside this course.)*
>
> **So nothing in chapters 5–8 can use it.** The dot product generalises to every $\mathbb{R}^n$ and to abstract inner-product spaces; the cross product does not. **When you need "a vector orthogonal to these" in $\mathbb{R}^n$, the tool is Gram–Schmidt** ([[08 - Orthogonality|ch. 08]]), not the cross product.
>
> **The *area* and *volume* interpretations do generalise** — as $|\det|$ — which is why §4.3's results reappear as the Jacobian in [[Calculus/contents/00-Index|Calculus]].

---

### 4. Linear operators on $\mathbb{R}^3$

**Projections and reflections have matrices, and the matrices are derived from the projection formula rather than memorised.**

> [!important] The four standard operators
> Let $L$ be the line through the origin with direction $\mathbf d$, and $M$ the plane through the origin with normal $\mathbf n$.
>
> | Operator | Formula | Matrix |
> |---|---|---|
> | Projection on $L$ | $\dfrac{\mathbf x\cdot\mathbf d}{\|\mathbf d\|^2}\mathbf d$ | $\dfrac{1}{\|\mathbf d\|^2}\mathbf d\mathbf d^{\mathsf T}$ |
> | Reflection in $L$ | $2\operatorname{proj}_{\mathbf d}\mathbf x-\mathbf x$ | $\dfrac{2}{\|\mathbf d\|^2}\mathbf d\mathbf d^{\mathsf T}-I$ |
> | Projection on $M$ | $\mathbf x-\operatorname{proj}_{\mathbf n}\mathbf x$ | $I-\dfrac{1}{\|\mathbf n\|^2}\mathbf n\mathbf n^{\mathsf T}$ |
> | Reflection in $M$ | $\mathbf x-2\operatorname{proj}_{\mathbf n}\mathbf x$ | $I-\dfrac{2}{\|\mathbf n\|^2}\mathbf n\mathbf n^{\mathsf T}$ |
>
> **Every one is built from $\operatorname{proj}$, and the outer product $\mathbf d\mathbf d^{\mathsf T}$ is what turns the formula into a matrix.**

> [!tip] Three facts worth noticing
> - **All four matrices are symmetric**, because $(\mathbf d\mathbf d^{\mathsf T})^{\mathsf T}=\mathbf d\mathbf d^{\mathsf T}$. **By [[08 - Orthogonality|ch. 08]]'s spectral theorem they are therefore orthogonally diagonalizable — and their eigenvalues are visibly $0$ and $1$ (projections) or $\pm1$ (reflections).**
> - **Projections satisfy $P^2=P$; reflections satisfy $R^2=I$.** Projecting twice does nothing new; reflecting twice returns you home.
> - **$\det$ of a reflection is $-1$** (orientation reversed) and of a rotation is $+1$.
>
> **Areas and volumes under a transformation scale by $|\det A|$** — which is why $\det=0$ means "flattened", i.e. not invertible ([[03 - Determinants and Diagonalization|ch. 03]]).

---

## ✏️ Exercises

> [!question] Exercise 1 — dot products and angles *(warm-up)*
> Let $\mathbf u=(1,1,0)$, $\mathbf v=(1,0,1)$, $\mathbf w=(1,-1,0)$.
> (i) Find $\|\mathbf u\|$ and the unit vector in the direction of $\mathbf u$.
> (ii) Find the angle between $\mathbf u$ and $\mathbf v$.
> (iii) Which pairs are orthogonal?
> (iv) Verify $\|\mathbf v-3\mathbf w\|^2=1$ given only $\|\mathbf v\|=2$, $\|\mathbf w\|=1$, $\mathbf v\cdot\mathbf w=2$ (a *different* $\mathbf v,\mathbf w$).

> [!example]- Solution
> **(i)** $\|\mathbf u\|=\sqrt{1+1+0}=\sqrt2$, so the unit vector is $\tfrac1{\sqrt2}(1,1,0)$.
>
> **(ii)** $\mathbf u\cdot\mathbf v=1$, so $\cos\theta=\dfrac1{\sqrt2\sqrt2}=\dfrac12$ and $\theta=\boxed{60°=\pi/3}$. *(Verified.)*
>
> **(iii)** $\mathbf u\cdot\mathbf w=1-1+0=0$ — **$\mathbf u\perp\mathbf w$.** The others are not: $\mathbf v\cdot\mathbf w=1$.
>
> **(iv)** Expand bilinearly, exactly as with $(a-3b)^2$:
> $$\|\mathbf v-3\mathbf w\|^2=(\mathbf v-3\mathbf w)\cdot(\mathbf v-3\mathbf w)=\|\mathbf v\|^2-6(\mathbf v\cdot\mathbf w)+9\|\mathbf w\|^2=4-12+9=\boxed{1}$$
>
> **The point of (iv) is that no coordinates were needed** — lengths and one dot product sufficed. **This is how every proof in chapters 5 and 8 is done**, since there the vectors may not have coordinates you can write down.
>
> *(Nicholson's printed version of this computation has $9\|\mathbf v\|^2$ where $9\|\mathbf w\|^2$ is meant — see the gaps callout.)*

> [!question] Exercise 2 — projection and distance to a line
> Let $P(1,2,3)$ and let $L$ be the line through $P_0(0,1,1)$ with direction $\mathbf d=(1,1,1)$.
> (i) Decompose $\mathbf u=\overrightarrow{P_0P}$ into components parallel and perpendicular to $\mathbf d$.
> (ii) Find the distance from $P$ to $L$ and the closest point $Q$ on $L$.
> (iii) Verify that the perpendicular component really is orthogonal to $\mathbf d$.
> (iv) Explain why replacing $\mathbf d$ by $5\mathbf d$ changes nothing.

> [!example]- Solution
> **(i)** $\mathbf u=(1,1,2)$, $\mathbf u\cdot\mathbf d=4$, $\|\mathbf d\|^2=3$:
> $$\mathbf u_1=\operatorname{proj}_{\mathbf d}\mathbf u=\tfrac43(1,1,1),\qquad \mathbf u_2=\mathbf u-\mathbf u_1=\tfrac13(-1,-1,2)$$
>
> **(ii)** $\ \text{dist}=\|\mathbf u_2\|=\tfrac13\sqrt{1+1+4}=\boxed{\dfrac{\sqrt6}{3}\approx0.816}$, and
> $$Q=P_0+\mathbf u_1=\left(\tfrac43,\ \tfrac73,\ \tfrac73\right)$$
> *(All verified.)*
>
> **(iii)** $\mathbf d\cdot\mathbf u_2=\tfrac13(-1-1+2)=0$ ✓ — **which is guaranteed by Theorem 4, so this is a check on arithmetic, not on theory.** *(Doing it anyway catches sign errors, and costs three multiplications.)*
>
> **(iv)** In $\dfrac{\mathbf u\cdot\mathbf d}{\|\mathbf d\|^2}\mathbf d$, replacing $\mathbf d$ by $k\mathbf d$ multiplies the numerator by $k$, the denominator by $k^2$, and the trailing $\mathbf d$ by $k$ — **net factor $k^2/k^2=1$.**
>
> **The projection depends only on the *direction*, which is as it must be: the line $L$ has many direction vectors and only one geometry.** **If $\mathbf d$ is a unit vector the formula simplifies to $(\mathbf u\cdot\mathbf d)\mathbf d$** — the reason orthonormal bases are worth the trouble of building.

> [!question] Exercise 3 — planes
> (i) Find the equation of the plane through $A(1,0,2)$, $B(2,1,0)$, $C(0,2,1)$.
> (ii) Find the distance from $D(4,4,4)$ to that plane.
> (iii) Find the plane through $A$ parallel to $3x-y+2z=5$.
> (iv) Does the line $(1,1,1)+t(1,-2,1)$ lie in, meet, or run parallel to the plane of part (i)?

> [!example]- Solution
> **(i)** $\overrightarrow{AB}=(1,1,-2)$ and $\overrightarrow{AC}=(-1,2,-1)$ lie in the plane, so
> $$\mathbf n=\overrightarrow{AB}\times\overrightarrow{AC}=(3,3,3)\ \parallel\ (1,1,1)$$
> With $d=\mathbf n\cdot\mathbf a=1+0+2=3$:
> $$\boxed{x+y+z=3}$$
> *(Verified: $B$ gives $2+1+0=3$ ✓ and $C$ gives $0+2+1=3$ ✓ — **always check the two points you did not use to fix $d$.**)*
>
> **(ii)** $\ \text{dist}=\dfrac{|4+4+4-3|}{\sqrt3}=\dfrac{9}{\sqrt3}=\boxed{3\sqrt3\approx5.196}$ *(verified).*
>
> **(iii)** Same normal $(3,-1,2)$, new constant: $d=3(1)-0+2(2)=7$, so $\boxed{3x-y+2z=7}$.
>
> **(iv)** The direction is $\mathbf d=(1,-2,1)$ and the normal is $\mathbf n=(1,1,1)$:
> $$\mathbf d\cdot\mathbf n=1-2+1=0$$
> — **so the line is parallel to the plane** (its direction lies *in* the plane). Now test whether the point $(1,1,1)$ is on the plane: $1+1+1=3$ ✓ — **it is.**
>
> **So the line lies entirely inside the plane.** *(Had the point failed the test, the line would have been parallel and disjoint; had $\mathbf d\cdot\mathbf n\ne0$, it would have crossed at exactly one point.)*
>
> > [!tip] The two-step test
> > **$\mathbf d\cdot\mathbf n$ decides the *orientation*; a single point decides the *position*.** This is the same particular-plus-homogeneous split as everywhere else: the direction question is homogeneous, the position question is not.

> [!question] Exercise 4 — cross products, areas, volumes
> (i) Compute $(1,2,3)\times(0,1,4)$ and verify it is orthogonal to both.
> (ii) Find the area of the triangle with vertices $A(1,0,2)$, $B(2,1,0)$, $C(0,2,1)$.
> (iii) Find the volume of the parallelepiped spanned by $(1,2,3)$, $(0,1,4)$, $(5,6,0)$.
> (iv) Show that $\mathbf u\times\mathbf u=\mathbf 0$ for every $\mathbf u$, and that the cross product is **not** associative by comparing $(\mathbf i\times\mathbf i)\times\mathbf j$ with $\mathbf i\times(\mathbf i\times\mathbf j)$.

> [!example]- Solution
> **(i)** $$\det\begin{bmatrix}\mathbf i&\mathbf j&\mathbf k\\1&2&3\\0&1&4\end{bmatrix}=(2\cdot4-3\cdot1)\mathbf i-(1\cdot4-3\cdot0)\mathbf j+(1\cdot1-2\cdot0)\mathbf k=\boxed{(5,-4,1)}$$
> Checks: $(1,2,3)\cdot(5,-4,1)=5-8+3=0$ ✓ and $(0,1,4)\cdot(5,-4,1)=0-4+4=0$ ✓.
>
> **(ii)** From Exercise 3, $\overrightarrow{AB}\times\overrightarrow{AC}=(3,3,3)$, and the triangle is **half** the parallelogram:
> $$\text{area}=\tfrac12\|(3,3,3)\|=\tfrac12\cdot3\sqrt3=\boxed{\frac{3\sqrt3}{2}\approx2.598}$$
> *(Verified.)*
>
> **(iii)** The triple product is the determinant:
> $$\left|\det\begin{bmatrix}1&2&3\\0&1&4\\5&6&0\end{bmatrix}\right|=|1|=\boxed{1}$$
> *(Verified — this is the matrix from [[03 - Determinants and Diagonalization|ch. 03]], Exercise 3, whose determinant is 1.)*
>
> **A volume of 1 from vectors of length $\sqrt{14}$, $\sqrt{17}$ and $\sqrt{61}$** means the three are very nearly coplanar — **and "nearly coplanar" is exactly "nearly linearly dependent", i.e. the matrix is close to singular.** *(That is why its inverse in ch. 02, Exercise 3, had entries as large as $-24$: a nearly-flat parallelepiped inverts violently. This is the geometric content of *ill-conditioning*.)*
>
> **(iv)** $\mathbf u\times\mathbf u=\mathbf 0$: either from anticommutativity ($\mathbf u\times\mathbf u=-\mathbf u\times\mathbf u$ forces it to be zero), or from $\|\mathbf u\times\mathbf u\|=\|\mathbf u\|^2\sin0=0$, or because the mnemonic determinant has two equal rows.
>
> **Non-associativity:**
> $$(\mathbf i\times\mathbf i)\times\mathbf j=\mathbf 0\times\mathbf j=\mathbf 0,\qquad \mathbf i\times(\mathbf i\times\mathbf j)=\mathbf i\times\mathbf k=-\mathbf j$$
> **$\mathbf 0\ne-\mathbf j$**, so the cross product is not associative — **unlike matrix multiplication, and unlike almost every other product in this book.** *(Brackets are never optional in a cross-product expression.)*

> [!question] Exercise 5 — Cauchy–Schwarz, and skew lines *(hard)*
> **(a)** (i) Deduce the **Cauchy–Schwarz inequality** $|\mathbf u\cdot\mathbf v|\le\|\mathbf u\|\|\mathbf v\|$ from Theorem 2, and say when equality holds.
> (ii) Use it to prove the **triangle inequality** $\|\mathbf u+\mathbf v\|\le\|\mathbf u\|+\|\mathbf v\|$.
> (iii) Why does the argument in (i) *not* work in $\mathbb{R}^n$ for $n>3$, and what replaces it?
>
> **(b)** Find the shortest distance between the skew lines
> $$L_1:\ (1,0,-1)+t(2,0,1),\qquad L_2:\ (0,1,0)+s(1,1,0)$$

> [!example]- Solution
> **(a)(i)** For nonzero $\mathbf u,\mathbf v$, Theorem 2 gives $\mathbf u\cdot\mathbf v=\|\mathbf u\|\|\mathbf v\|\cos\theta$, and $|\cos\theta|\le1$, so
> $$|\mathbf u\cdot\mathbf v|=\|\mathbf u\|\|\mathbf v\|\,|\cos\theta|\le\|\mathbf u\|\|\mathbf v\|$$
> *(If either vector is $\mathbf 0$ both sides are 0.)*
>
> **Equality holds iff $|\cos\theta|=1$, i.e. $\theta=0$ or $\pi$ — iff the vectors are parallel.**
>
> **(ii)** Expand and apply (i):
> $$\|\mathbf u+\mathbf v\|^2=\|\mathbf u\|^2+2(\mathbf u\cdot\mathbf v)+\|\mathbf v\|^2\le\|\mathbf u\|^2+2\|\mathbf u\|\|\mathbf v\|+\|\mathbf v\|^2=\big(\|\mathbf u\|+\|\mathbf v\|\big)^2$$
> Taking square roots gives the result. $\blacksquare$
>
> **The geometry: the direct route is never longer than a detour** — and equality holds exactly when $\mathbf u$ and $\mathbf v$ point the *same* way (not merely parallel: $\mathbf v=-\mathbf u$ gives strict inequality).
>
> **(iii)** **The argument is circular in higher dimensions.** In $\mathbb{R}^3$ we knew what "the angle between two vectors" meant *before* Theorem 2, so the theorem was a genuine statement about geometry. **In $\mathbb{R}^{100}$ there is no prior notion of angle** — $\cos\theta$ is *defined* by $\dfrac{\mathbf u\cdot\mathbf v}{\|\mathbf u\|\|\mathbf v\|}$, and that definition is only legitimate if the quotient already lies in $[-1,1]$, which is Cauchy–Schwarz.
>
> **So the logical order reverses: in general one proves Cauchy–Schwarz *first*, algebraically, and then defines the angle.** The standard proof considers
> $$0\le\|\mathbf u-t\mathbf v\|^2=\|\mathbf u\|^2-2t(\mathbf u\cdot\mathbf v)+t^2\|\mathbf v\|^2$$
> — a quadratic in $t$ that is never negative, so its discriminant satisfies $4(\mathbf u\cdot\mathbf v)^2-4\|\mathbf u\|^2\|\mathbf v\|^2\le0$. **No geometry is used, so it works in any inner-product space** — including spaces of functions, where it becomes the integral form $\left|\int fg\right|^2\le\int f^2\int g^2$. *(In probability, the same inequality is $|\mathrm{Cov}(X,Y)|\le\sigma_X\sigma_Y$, i.e. $|\rho|\le1$ — see [[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07 §3b]], where the proof is the identical "a variance is non-negative" argument.)*
>
> **(b)** The two directions are $\mathbf d_1=(2,0,1)$ and $\mathbf d_2=(1,1,0)$. **Any vector joining the lines has a component along $\mathbf d_1\times\mathbf d_2$, and that component is the same for every such vector** — it is the gap between the two parallel planes containing the lines.
> $$\mathbf n=\mathbf d_1\times\mathbf d_2=\det\begin{bmatrix}\mathbf i&\mathbf j&\mathbf k\\2&0&1\\1&1&0\end{bmatrix}=(-1,1,2)$$
> Take $\mathbf w=(0,1,0)-(1,0,-1)=(-1,1,1)$ joining a point of $L_1$ to a point of $L_2$. Then
> $$\text{dist}=\big\|\operatorname{proj}_{\mathbf n}\mathbf w\big\|=\frac{|\mathbf w\cdot\mathbf n|}{\|\mathbf n\|}=\frac{|1+1+2|}{\sqrt6}=\frac{4}{\sqrt6}=\boxed{\frac{2\sqrt6}{3}\approx1.633}$$
> *(Verified.)*
>
> > [!important] Every distance problem in this chapter is the same problem
> > | Distance from… | Project onto… | Take… |
> > |---|---|---|
> > | point to line | the direction $\mathbf d$ | the **leftover** |
> > | point to plane | the normal $\mathbf n$ | the **projection** |
> > | line to skew line | $\mathbf d_1\times\mathbf d_2$ | the **projection** |
> >
> > **Project onto the relevant direction; keep whichever piece is perpendicular to the object.** **In [[05 - The Vector Space Rn|ch. 05 §6]] this becomes "project onto the column space and keep the residual" — which is least squares**, and in [[08 - Orthogonality|ch. 08]] it becomes the orthogonal-complement theorem in full generality.

---

## 📝 Summary

- **$\|\mathbf v\|=\sqrt{\mathbf v\cdot\mathbf v}$**, unit vectors are $\mathbf v/\|\mathbf v\|$, and **a line is a point plus a direction** — the same "particular + homogeneous" shape as every solution set in the book.
- **The dot product is bilinear and symmetric with $\mathbf v\cdot\mathbf v=\|\mathbf v\|^2$**, so expressions like $\|\mathbf v-3\mathbf w\|^2$ expand exactly as $(a-3b)^2$ — **with no coordinates required.**
- **$\mathbf v\cdot\mathbf w=\|\mathbf v\|\|\mathbf w\|\cos\theta$**: positive means acute, negative obtuse, **zero means orthogonal**. In $\mathbb{R}^2$ and $\mathbb{R}^3$ this is a theorem; **in higher dimensions it becomes the definition of angle**, licensed by Cauchy–Schwarz.
- $$\boxed{\operatorname{proj}_{\mathbf d}\mathbf u=\frac{\mathbf u\cdot\mathbf d}{\|\mathbf d\|^2}\mathbf d}$$ **and $\mathbf u-\operatorname{proj}_{\mathbf d}\mathbf u\perp\mathbf d$.** The projection depends only on the *direction* of $\mathbf d$, and collapses to $(\mathbf u\cdot\mathbf d)\mathbf d$ when $\mathbf d$ is a unit vector. **Every vector splits uniquely into parallel and perpendicular parts.**
- **A plane is a point plus a normal**, and the coefficients of $ax+by+cz=d$ *are* the normal. Parallel planes share a normal and differ only in $d$; **distance from a point is $|\mathbf n\cdot\mathbf p-d|/\|\mathbf n\|$.**
- **The cross product exists only in $\mathbb{R}^3$.** $\mathbf v\times\mathbf w$ is orthogonal to both, vanishes iff they are parallel, and **$\|\mathbf v\times\mathbf w\|=\|\mathbf v\|\|\mathbf w\|\sin\theta$ is the area of the parallelogram.** It is anticommutative and **not associative**.
- **The triple product $\mathbf u\cdot(\mathbf v\times\mathbf w)$ is a determinant, and its absolute value is a volume** — so $\det=0$ means coplanar, i.e. dependent, i.e. singular.
- **Dot and cross are complementary:** $\cos$ versus $\sin$, agreement versus spread, perpendicularity versus parallelism.
- **Projection and reflection matrices are built from $\mathbf d\mathbf d^{\mathsf T}$**, are all symmetric, and satisfy $P^2=P$ or $R^2=I$. **Reflections have $\det=-1$.**
- **Cauchy–Schwarz $|\mathbf u\cdot\mathbf v|\le\|\mathbf u\|\|\mathbf v\|$ implies the triangle inequality**, and in general spaces it must be proved *first* (by "a squared norm is non-negative") so that angles can be defined at all.
- **Every distance problem is solved by projecting and keeping the perpendicular piece** — the method that becomes least squares in ch. 5 and the orthogonal-complement theorem in ch. 8.

---

## ⚠️ Important Notes

> [!warning] The cross product does not generalise; the dot product does
> **$\mathbf v\times\mathbf w$ is defined only in $\mathbb{R}^3$.** Nothing in chapters 5–8 uses it, and reaching for it in $\mathbb{R}^n$ is a category error.
>
> **What to use instead:**
> | Want | In $\mathbb{R}^3$ | In $\mathbb{R}^n$ |
> |---|---|---|
> | a vector orthogonal to two others | cross product | solve $A\mathbf x=\mathbf 0$, or **Gram–Schmidt** |
> | area / volume | $\|\mathbf v\times\mathbf w\|$, triple product | $\vert\det\vert$, or $\sqrt{\det(A^{\mathsf T}A)}$ |
> | angle | either product | **dot product only** |

> [!warning] $\mathbf v\cdot\mathbf w=0$ includes the zero vector
> By convention **$\mathbf 0$ is orthogonal to everything**, even though "the angle between $\mathbf 0$ and $\mathbf v$" is undefined. **The convention is what makes "orthogonal set" and "orthogonal complement" work smoothly in ch. 8** — but it means "$\mathbf u\cdot\mathbf v=0$" does *not* by itself imply both vectors are nonzero, and proofs that need nonzero vectors must say so.

> [!warning] Three products, three different failures of familiar algebra
> | Product | $ab=ba$? | Associative? | $ab=0\Rightarrow a=0$ or $b=0$? |
> |---|---|---|---|
> | Numbers | ✅ | ✅ | ✅ |
> | Matrices | ❌ | ✅ | ❌ |
> | Dot | ✅ | **meaningless** ($\mathbf u\cdot\mathbf v$ is a scalar) | ❌ |
> | Cross | ❌ (anti) | ❌ | ❌ |
>
> **"$(\mathbf u\cdot\mathbf v)\cdot\mathbf w$" is not an expression** — the first factor is a number and the dot product needs two vectors. **Write $(\mathbf u\cdot\mathbf v)\mathbf w$ if that is what you mean**, and note it is entirely different from $\mathbf u(\mathbf v\cdot\mathbf w)$.

> [!warning] Distance formulas: project or take the leftover?
> **The two cases differ, and mixing them is the standard error.**
> - **Point to a *line*:** the line's data is a **direction**, so project onto it and keep **what is left over**.
> - **Point to a *plane*:** the plane's data is a **normal**, so project onto it and keep **the projection itself**.
>
> **The rule: keep the component perpendicular to the object, and the object's given vector is sometimes in it (a direction) and sometimes perpendicular to it (a normal).** Ask which before writing anything down.

> [!warning] Normalise before you compare
> A dot product on its own says nothing about alignment — **$\mathbf u\cdot\mathbf v=100$ may mean the vectors are nearly parallel or nearly perpendicular**, depending on their lengths. Only $\cos\theta=\dfrac{\mathbf u\cdot\mathbf v}{\|\mathbf u\|\|\mathbf v\|}$ is comparable across pairs.
>
> **This is exactly why "cosine similarity" and not "dot-product similarity" is the standard in text and embedding work:** a long document would otherwise appear similar to everything. **Normalising is what removes magnitude and leaves direction.**

> [!note] Cross-subject connections
> - [[02 - Matrix Algebra|Ch. 02]] — the dot-product rule for $A\mathbf x$ is §4.2's dot product; **projection and reflection matrices are §2.6's standard matrices, derived here rather than asserted.**
> - [[03 - Determinants and Diagonalization|Ch. 03]] — **the triple product *is* a determinant**, so "$\det=0$" and "coplanar" and "linearly dependent" are one condition; $|\det|$ as a volume factor is this chapter's geometry.
> - [[05 - The Vector Space Rn|Ch. 05]] — **the projection formula becomes least squares**, and orthogonal bases make coordinates into dot products.
> - [[08 - Orthogonality|Ch. 08]] — orthogonal complements, Gram–Schmidt and QR are all built on §4.2; **the symmetry of the projection matrices is what makes the spectral theorem apply to them.**
> - [[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07]] — **covariance is a dot product and correlation is $\cos\theta$**; $|\rho|\le1$ is Cauchy–Schwarz, proved by the identical "a variance is non-negative" argument. **Uncorrelated means orthogonal**, and the law of total variance is Pythagoras.
> - [[Econometrics/contents/00-Index|Econometrics]] — **fitted values are a projection and residuals are the leftover**, orthogonal to every regressor by construction; $R^2$ is $\cos^2\theta$.
> - [[Calculus/contents/00-Index|Calculus]] — the gradient is the direction of steepest ascent *because* the directional derivative is a dot product; the Jacobian determinant is §4.3's volume factor.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **cosine similarity is Theorem 2**; a linear classifier's decision boundary is a plane $\mathbf w\cdot\mathbf x=b$ with $\mathbf w$ the normal, and the SVM margin is the point-to-plane distance formula.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **This is the chapter the PDF extraction damages most, because its content is largely pictorial.** Nicholson's own preface says the first part of §4.1 was rewritten for this edition around new diagrams, and **all of them are images with no extractable content.** Lost figures include: the parallelogram law and tip-to-tail addition; the acute/obtuse angle diagrams (Figure 3); the law-of-cosines triangle (Figure 2); the two cases of projection, with $\operatorname{proj}_{\mathbf d}\mathbf u$ pointing along or against $\mathbf d$ (Figure 5); the plane-with-normal picture (Figure 6); the right-handed axes with $\mathbf i,\mathbf j,\mathbf k$ (Figure 7); and every diagram in §4.5 on computer graphics. **The algebra is fully recoverable from the text and is reproduced above, but the pictures that make it intuitive are not.**
>
> **Source typos:**
> - **§4.2 Example 2 prints $\|\mathbf v\|^2-6(\mathbf v\cdot\mathbf w)+9\|\mathbf v\|^2$** where the last term must be $9\|\mathbf w\|^2$. **The arithmetic that follows ($4-12+9=1$) only works with $\|\mathbf w\|=1$**, confirming the intent. *(Corrected in Exercise 1(iv).)*
> - **The sign discussion after Example 3 prints "$\mathbf v\cdot\mathbf w<0$ if and only if $\theta$ is obtuse $(\pi/2<\theta\le0)$"** — the range should be $\pi/2<\theta\le\pi$. As printed the interval is empty.
> - **The same paragraph reads "since $\|\mathbf v\|$ and $\|\mathbf v\|$ are nonzero"** — the second should be $\|\mathbf w\|$.
> - **Example 3 states the vectors as $\mathbf u$ and $\mathbf v$ but the formula uses $\mathbf v$ and $\mathbf w$**, so the displayed computation names variables that were never introduced.
> - **Theorem 1(5) prints $(k\mathbf v)\cdot\mathbf w=k(\mathbf w\cdot\mathbf v)=\mathbf v\cdot(k\mathbf w)$** — harmless, since the dot product is symmetric, but the middle term should read $k(\mathbf v\cdot\mathbf w)$ to match the pattern.
> - **The proof of Theorem 1 has an unclosed parenthesis and a stray conjunction:** "(because $\mathbf w\cdot\mathbf v=\mathbf v^{\mathsf T}\mathbf w$, and are left to the reader."
>
> **Notation mangled by the layout:** `∥` survives but its pairing does not, so $\|\mathbf v\|^2$ often extracts as `∥v∥ 2`; `/longarrowright PQ` is $\overrightarrow{PQ}$; `/bbR` is $\mathbb{R}$; `π __ 2` is $\tfrac\pi2$; `√ __ 6` is $\sqrt6$; `S … T` are large brackets. **Column vectors extract one entry per line with minus signs displaced**, exactly as in chapters 1–3.
>
> **Verification performed:** every worked example quoted was independently recomputed. Confirmed: $\cos\theta=-\tfrac12$ and $\theta=120°$ (§4.2 Ex. 3); $\mathbf u\cdot\mathbf d=8$, $\|\mathbf d\|^2=11$, $\mathbf u_1=\tfrac8{11}(1,-1,3)$, $\mathbf u_2=\tfrac1{11}(14,-25,-13)$ **and $\mathbf d\cdot\mathbf u_2=0$** (§4.2 Ex. 7); the distance $\sqrt3$ and the closest point $Q(0,2,-1)$ (§4.2 Ex. 8); $d=10$ (§4.2 Ex. 9); $d=9$ (§4.2 Ex. 10); the distance $8/\sqrt{26}=1.5689$ (§4.2 Ex. 11); and **$\overrightarrow{PQ}\times\overrightarrow{PR}=(25,7,2)$ with $d=42$** (§4.2 Ex. 13). **All agree with the text.** The only defects found are the typographical ones above; **no computational error was found in this chapter.** Every exercise figure in these notes was likewise verified before being written down.
>
> **Scope note:** §4.5 (computer graphics) is omitted — it is a presentation of homogeneous coordinates and $4\times4$ transformation matrices whose mathematical content is §4.4 plus a translation trick, and its value is almost entirely in the figures, which do not survive extraction. **§4.3's detailed development of the cross product is compressed into §3 above**, keeping the results (orthogonality, the $\sin\theta$ formula, anticommutativity, the triple product) and omitting the identity-verification exercises, since **nothing in chapters 5–8 uses the cross product at all.**

#linear-algebra #vector-geometry #dot-product #projection #cross-product #planes #orthogonality #cauchy-schwarz
