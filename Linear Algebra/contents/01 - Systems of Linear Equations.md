---
subject: Linear Algebra
chapter: 01
tags: [ds, linear-algebra, linear-systems, gaussian-elimination, row-echelon, rank, homogeneous]
source: "Nicholson, *Linear Algebra with Applications*, 7th ed., ch. 1 (pp. 1–31)"
---

# Systems of Linear Equations

> [!abstract] What this chapter is for
> **Linear algebra was invented to solve systems of linear equations**, and this chapter is that original problem, done properly. It looks like arithmetic bookkeeping — and it is — but three ideas are being smuggled in that the rest of the book depends on entirely.
>
> | Idea | Looks like | Really is |
> |---|---|---|
> | **Row operations** | a tidy way to eliminate variables | operations that **preserve the solution set** |
> | **Rank** | the number of leading 1s | the amount of **genuinely independent information** in the system |
> | **Basic solutions** | a way to write the answer | a **basis** for the solution space (ch. 5) |
>
> | § | Topic | The thing to take away |
> |---|---|---|
> | **1** | Elementary operations | Three reversible moves; reversibility is why solutions are preserved |
> | **2** | **Gaussian elimination** | A finite, mechanical algorithm that always terminates |
> | **3** | Row-echelon form and **rank** | **Exactly three outcomes**: none, one, or infinitely many solutions |
> | **4** | Homogeneous systems | Always consistent; **more variables than equations $\Rightarrow$ nontrivial solutions** |
> | **5** | Basic solutions | Every solution is a **linear combination** of $n-r$ of them |
>
> **The single most important sentence in the chapter is Theorem 2 of §1.2:** a consistent system in $n$ variables whose augmented matrix has rank $r$ has **exactly $n-r$ parameters.** Everything about dimension, nullity and degrees of freedom later in the book is that statement generalised.

---

## 📘 Main Knowledge

### 1. Systems, solutions, and the augmented matrix

A **linear equation** in $x_1,\dots,x_n$ is

$$a_1x_1+a_2x_2+\cdots+a_nx_n=b$$

with the $a_i$ the **coefficients** and $b$ the **constant term**. **Every variable appears to the first power only** — no $x^2$, no $xy$, no $\sin x$. A finite collection of such equations is a **system**.

A system is **consistent** if it has at least one solution and **inconsistent** otherwise. When there are infinitely many solutions they are written in **parametric form**, with free parameters $s,t,\dots$; this is the **general solution**.

> [!warning] The same solution set can look completely different
> $3x-y+2z=6$ solved for $y$ gives $(x,y,z)=(s,\ 3s+2t-6,\ t)$; solved for $x$ it gives $\left(\tfrac13(p-2q+6),\ p,\ q\right)$. **Two parametrisations, one solution set.**
>
> **So "my answer looks different from the book's" is not evidence of an error.** To check, substitute back into the original equations — that is the only reliable test.

**The augmented matrix** strips away the variable names:

$$\begin{aligned}3x_1+2x_2-x_3+x_4&=-1\\ 2x_1\phantom{{}+2x_2}-x_3+2x_4&=0\\ 3x_1+x_2+2x_3+5x_4&=2\end{aligned}\qquad\longleftrightarrow\qquad\left[\begin{array}{cccc|c}3&2&-1&1&-1\\2&0&-1&2&0\\3&1&2&5&2\end{array}\right]$$

The part left of the bar is the **coefficient matrix**; the column to the right is the **constant matrix**.

> [!tip] Why the geometric picture runs out, and why that is the point
> With two variables, each equation is a line, and the three possible configurations — **crossing, parallel, identical** — give **one, no, or infinitely many** solutions. With three variables, each equation is a plane. **With four or more there is no picture at all.**
>
> **Gaussian elimination is what replaces the picture.** It is purely algebraic, works in any number of variables, and — crucially — it *proves* that those same three outcomes are the only ones possible, however many variables there are (Theorem 2 below).

---

### 2. Elementary operations

> [!important] Definitions 1.1 and 1.2 — the three moves
> On **equations**, and equivalently on the **rows** of the augmented matrix:
>
> | Type | Operation | Its inverse |
> |---|---|---|
> | **I** | Interchange two rows | interchange them again |
> | **II** | Multiply a row by a **nonzero** number $k$ | multiply by $1/k$ |
> | **III** | Add $k$ times row $p$ to a **different** row $q$ | add $-k$ times row $p$ to row $q$ |

> [!important] Theorem 1
> **Elementary operations do not change the solution set.** Systems related by a sequence of them are **equivalent**.

**The proof is entirely about reversibility, and it is worth seeing why.** Every solution of the old system solves the new one, because adding equations and scaling by a nonzero number always produces valid equations. The converse needs the *inverse* operations: since the original system can be recovered from the new one, every solution of the new system solves the original. **Both directions, hence the same solution set.**

> [!warning] Two conditions in Definitions 1.1–1.2 are doing real work
> - **Type II requires $k\ne0$.** Multiplying an equation by 0 turns it into $0=0$, which is not reversible — **information is destroyed, and the solution set grows.**
> - **Type III requires $p\ne q$.** Adding $k$ times a row *to itself* multiplies it by $1+k$, which is a Type II operation in disguise and is **not reversible when $k=-1$** — the row becomes zero.
>
> **Both restrictions exist so that every operation is undoable, and undoability is the entire proof of Theorem 1.**

---

### 3. Row-echelon form and Gaussian elimination

> [!important] Definition 1.3
> A matrix is in **row-echelon form** if
> 1. all zero rows are at the bottom;
> 2. the first nonzero entry of each nonzero row is a **1** (the **leading 1**);
> 3. each leading 1 is strictly to the **right** of the leading 1 in the row above.
>
> It is in **reduced row-echelon form** if in addition
> 4. **each leading 1 is the only nonzero entry in its column.**

The shape is a staircase descending to the right:

$$\begin{bmatrix}0&1&*&*&*&*&*\\0&0&0&1&*&*&*\\0&0&0&0&1&*&*\\0&0&0&0&0&0&1\\0&0&0&0&0&0&0\end{bmatrix}$$

**Everything below and to the left of the leading 1s is zero; everything above and to the right is arbitrary.** Reduced form additionally clears the entries *directly above* each leading 1.

> [!important] Theorem 1 (§1.2) and the Gaussian algorithm
> **Every matrix can be brought to (reduced) row-echelon form by elementary row operations.**
>
> > **Step 1.** If the matrix is all zeros, stop.
> > **Step 2.** Find the leftmost column containing a nonzero entry $a$; move that row to the top.
> > **Step 3.** Multiply the new top row by $1/a$ to create a leading 1.
> > **Step 4.** Subtract multiples of that row from the rows below to zero out the rest of the column.
> > **Step 5.** Repeat steps 1–4 on the remaining rows.
>
> **The algorithm is recursive** — after each leading 1 is placed, the same procedure runs on what is left — which is exactly why it is easy to program and why it always terminates.

> [!tip] In hand calculation, deviate from the algorithm to avoid fractions
> Nicholson's own Example 3 of §1.1 does not follow the algorithm literally: to solve
> $$3x+4y+z=1,\quad 2x+3y=0,\quad 4x+3y-z=-2$$
> he creates the first leading 1 by **subtracting row 2 from row 1** rather than dividing row 1 by 3. **Same result, no fractions until the very end** — which is $x=-\tfrac37$, $y=\tfrac27$, $z=\tfrac87$.
>
> **The algorithm guarantees termination; it does not claim to be the tidiest route.** By hand, hunt for a 1 (or make one by subtraction) before dividing.

> [!important] Gaussian elimination — the full procedure
> 1. Carry the **augmented** matrix to reduced row-echelon form.
> 2. **If a row $[0\ 0\ \cdots\ 0\ |\ 1]$ appears, the system is inconsistent — stop.**
> 3. Otherwise assign the **nonleading** variables as parameters and solve for the **leading** variables in terms of them.

**The variables corresponding to columns with leading 1s are the *leading variables*; the rest are *free variables* and become the parameters.**

> [!example] Example 2 (§1.2) — an inconsistent system
> $$3x+y-4z=-1,\qquad x+10z=5,\qquad 4x+y+6z=1$$
> reduces to
> $$\left[\begin{array}{ccc|c}1&0&10&5\\0&1&-34&-16\\0&0&0&-3\end{array}\right]$$
> **The last row says $0x+0y+0z=-3$** — impossible. The system has no solution.
>
> **This is the only way inconsistency can appear**, and it is unmistakable: a row of zeros in the coefficient part with a nonzero constant.

> [!example] Example 3 (§1.2) — infinitely many solutions
> $$x_1-2x_2-x_3+3x_4=1,\quad 2x_1-4x_2+x_3=5,\quad x_1-2x_2+2x_3-3x_4=4$$
> reduces to
> $$\left[\begin{array}{cccc|c}1&-2&0&1&2\\0&0&1&-2&1\\0&0&0&0&0\end{array}\right]$$
> Leading 1s in columns 1 and 3, so $x_1,x_3$ are leading and $x_2,x_4$ are free. Setting $x_2=s$, $x_4=t$:
> $$x_1=2+2s-t,\qquad x_2=s,\qquad x_3=1+2t,\qquad x_4=t$$
> *(Verified: all three equations hold for every $s,t$.)*

> [!example] Example 4 (§1.2) — a system with symbolic constants
> $$x_1+3x_2+x_3=a,\qquad -x_1-2x_2+x_3=b,\qquad 3x_1+7x_2-x_3=c$$
> Row-reducing carries the constant column to $\left[\begin{smallmatrix}-2a-3b\\a+b\\c-a+2b\end{smallmatrix}\right]$ with coefficient part $\left[\begin{smallmatrix}1&0&-5\\0&1&2\\0&0&0\end{smallmatrix}\right]$. The last row reads $0=c-(a-2b)$, so
> $$\boxed{\text{consistent}\iff c=a-2b}$$
> and then, with $x_3=t$,
> $$x_1=5t-(2a+3b),\qquad x_2=(a+b)-2t,\qquad x_3=t$$
> *(Verified at $a=b=1$, $c=-1$.)*
>
> **The technique generalises: reduce with the symbols carried along, then read the consistency condition off the last row.** It is how you find *when* a model is solvable rather than merely solving one instance — and it is the same move as checking whether a design matrix has full rank.

> [!tip] Back-substitution is the efficient variant, and the difference is not small
> Instead of going all the way to *reduced* form, stop at row-echelon form, solve the last equation, substitute upward, and repeat.
>
> **Nicholson's footnote gives the operation counts: $\approx n^3/2$ multiplications and divisions for full reduction versus $\approx n^3/3$ with back-substitution.** A 33% saving, and both are **cubic** in $n$ — which is why solving a large system is expensive, and why §2.7's LU-factorization exists (it does the $O(n^3)$ work once and reuses it for every new right-hand side).

---

### 4. Rank

> [!important] Definition 1.4
> The **rank** of a matrix $A$ is the number of leading 1s in **any** row-echelon matrix obtained from $A$.

> [!warning] Rank is well defined, but row-echelon form is not
> **Different sequences of row operations give different row-echelon matrices.** Nicholson's example: $A=\left[\begin{smallmatrix}1&-1\\-4&2\end{smallmatrix}\right]$-type matrices can reach $\left[\begin{smallmatrix}1&-1\\0&1\end{smallmatrix}\right]$-shaped forms with different entries above the diagonal.
>
> **Two things are nonetheless unique.** The **reduced** row-echelon form is unique (proved at the end of §2.5), and **the *number* of leading 1s is the same however you reduce** (proved in ch. 5). **Rank is a property of the matrix, not of your arithmetic.**
>
> **Until ch. 5 this is an assertion you are asked to accept** — the definition is stated before the theorem that makes it legitimate. *(Flagged in the gaps callout.)*

> [!example] Example 5 (§1.2)
> $$A=\begin{bmatrix}1&1&-1&4\\2&1&3&0\\0&1&-5&8\end{bmatrix}\ \longrightarrow\ \begin{bmatrix}1&1&-1&4\\0&1&-5&8\\0&1&-5&8\end{bmatrix}\ \longrightarrow\ \begin{bmatrix}1&1&-1&4\\0&1&-5&8\\0&0&0&0\end{bmatrix}$$
> Two leading 1s, so $\operatorname{rank}A=2$. *(Verified. The last two rows become identical, which is the visible sign that the third equation carried no new information.)*

**Bounds:** if $A$ is $m\times n$ then $\operatorname{rank}A\le m$ (leading 1s are in distinct rows) and $\operatorname{rank}A\le n$ (they are in distinct columns).

> [!important] Theorem 2 (§1.2) — the counting theorem
> For a **consistent** system of $m$ equations in $n$ variables whose augmented matrix has rank $r$:
> 1. the solution set involves **exactly $n-r$ parameters**;
> 2. if $r<n$ there are **infinitely many** solutions;
> 3. if $r=n$ the solution is **unique**.

$$\boxed{\#\text{parameters}=\underbrace{n}_{\text{variables}}-\underbrace{r}_{\text{independent equations}}}$$

> [!tip] Read rank as "how much the system actually tells you"
> $n$ variables are $n$ unknowns. Each *independent* equation removes one degree of freedom. **$r$ counts the equations that are genuinely independent** — the rest are redundant combinations of the others and constrain nothing new.
>
> **This is the first appearance of the theme that runs through the whole book:** in ch. 5 the same count becomes $\operatorname{rank}+\text{nullity}=n$, and in ch. 7 it becomes the **dimension theorem** $\dim(\ker T)+\dim(\operatorname{im}T)=\dim V$. **They are one theorem, stated three times at increasing levels of abstraction.**

> [!important] Exactly three outcomes, and no others
> | Outcome | Diagnostic in the row-echelon form |
> |---|---|
> | **No solution** | a row $[0\ \cdots\ 0\ |\ 1]$ appears |
> | **Unique solution** | consistent, and every variable is leading ($r=n$) |
> | **Infinitely many** | consistent, and at least one variable is free ($r<n$) |
>
> **"Exactly two solutions" is impossible.** If $\mathbf x$ and $\mathbf y$ both solve the system, so does $\mathbf x+t(\mathbf y-\mathbf x)$ for every $t$ — the whole line through them. **This is a genuinely non-obvious fact about linear systems, and it fails immediately for non-linear ones** ($x^2=1$ has exactly two solutions).

---

### 5. Homogeneous systems

A system is **homogeneous** if every constant term is zero:

$$a_1x_1+a_2x_2+\cdots+a_nx_n=0$$

**Every homogeneous system is consistent**, because $x_1=\cdots=x_n=0$ — the **trivial solution** — always works. The question is whether there is anything else.

> [!important] Theorem 1 (§1.3)
> **If a homogeneous system has more variables than equations, it has a nontrivial solution** — in fact infinitely many.

**Proof in one line:** with $m$ equations and $n>m$ variables, $r\le m<n$, so there is at least one free variable, hence at least one parameter.

> [!warning] The converse is false
> $x_1+x_2=0$, $2x_1+2x_2=0$ has $m=n=2$ and plenty of nontrivial solutions. **"More variables than equations" is sufficient, not necessary** — what actually matters is $r<n$, and the equation count is merely a cheap way to guarantee it.
>
> **In applied terms: having at least as many equations as unknowns does not mean you have pinned the answer down.** Duplicate or linearly dependent equations look like information and are not — which in a regression setting is exactly perfect multicollinearity ([[Econometrics/contents/00-Index|Econometrics]]).

> [!example] Example 2 (§1.3) — a conic through any five points
> A conic is $ax^2+bxy+cy^2+dx+ey+f=0$ with $a,b,c$ not all zero. Demanding it pass through five given points gives **five homogeneous equations in the six unknowns $a,\dots,f$** — so by Theorem 1 there is a nontrivial solution.
>
> If $a=b=c=0$ then all five points satisfy $dx+ey+f=0$, i.e. they are collinear. **So provided the points are not all on a line, some genuine conic passes through them.**
>
> **This is a template worth recognising:** *count the unknowns, count the constraints, and if unknowns exceed constraints a nonzero solution must exist.* It proves existence without producing the object — the same style of argument as the probabilistic method in [[Probability Theory/contents/07 - Properties of Expectation|Probability ch. 07]].

---

### 6. Linear combinations and basic solutions

For columns $\mathbf x,\mathbf y$ with the same number of entries, $\mathbf x+\mathbf y$ adds entrywise and $k\mathbf x$ scales every entry. **A sum of scalar multiples $s\mathbf x+t\mathbf y+\cdots$ is a *linear combination*.**

> [!tip] "Is $\mathbf v$ a linear combination of $\mathbf x,\mathbf y,\mathbf z$?" is a linear system in disguise
> Asking whether $\mathbf v=r\mathbf x+s\mathbf y+t\mathbf z$ means asking whether a certain system in $r,s,t$ is **consistent** — and Gaussian elimination answers it.
>
> In Nicholson's Example 4, $\mathbf v=(0,-1,2)$ **is** such a combination (the system has solutions $r=2-k$, $s=-1-k$, $t=k$, so $\mathbf v=2\mathbf x-\mathbf y$ among infinitely many ways), while $\mathbf w=(1,1,1)$ **is not** (the system is inconsistent).
>
> **This one observation is the bridge to chapter 5.** "Spanning" will mean *every* vector is such a combination; "independent" will mean the representation is *unique*. Both are questions about consistency and uniqueness of linear systems — which is all of chapter 1.

> [!important] Linear combinations of solutions are solutions
> **If $\mathbf x$ and $\mathbf y$ solve a homogeneous system, so does $s\mathbf x+t\mathbf y$ for all $s,t$.**
>
> The verification is direct: $\sum_i a_i(sx_i+ty_i)=s\sum_i a_ix_i+t\sum_i a_iy_i=s(0)+t(0)=0$.
>
> **This is exactly the statement that the solution set is a *subspace* — closed under addition and scaling** — which is Definition 1 of §5.1. **It fails for non-homogeneous systems:** if $A\mathbf x=\mathbf b$ and $A\mathbf y=\mathbf b$ with $\mathbf b\ne\mathbf 0$, then $A(\mathbf x+\mathbf y)=2\mathbf b\ne\mathbf b$.

> [!important] Definition 1.5 and Theorem 2 (§1.3) — basic solutions
> The Gaussian algorithm produces one **basic solution** per parameter. For an $m\times n$ coefficient matrix of rank $r$:
> 1. there are **exactly $n-r$ basic solutions**;
> 2. **every solution is a linear combination of them.**
>
> **Any nonzero scalar multiple of a basic solution is still called a basic solution** — which lets you clear fractions.

> [!example] Example 5 (§1.3)
> $$A=\begin{bmatrix}1&-2&3&-2\\-3&6&1&0\\-2&4&4&-2\end{bmatrix}\ \longrightarrow\ \begin{bmatrix}1&-2&0&-\tfrac15\\0&0&1&-\tfrac35\\0&0&0&0\end{bmatrix}$$
> so $x_1=2s+\tfrac15t$, $x_2=s$, $x_3=\tfrac35t$, $x_4=t$, and
> $$\mathbf x=s\begin{bmatrix}2\\1\\0\\0\end{bmatrix}+t\begin{bmatrix}\tfrac15\\0\\\tfrac35\\1\end{bmatrix}=s\begin{bmatrix}2\\1\\0\\0\end{bmatrix}+\tfrac t5\begin{bmatrix}1\\0\\3\\5\end{bmatrix}$$
> **Rescaling the second basic solution by 5 clears the fractions** — legitimate, because $t/5$ is just as arbitrary a parameter as $t$. *(Verified.)*

> [!example] Example 6 (§1.3) — rank 2 out of 5 columns
> $$A=\begin{bmatrix}1&-3&0&2&2\\-2&6&1&2&-5\\3&-9&-1&0&7\\-3&9&2&6&-8\end{bmatrix}\ \longrightarrow\ \begin{bmatrix}1&-3&0&2&2\\0&0&1&6&-1\\0&0&0&0&0\\0&0&0&0&0\end{bmatrix}$$
> $r=2$, $n=5$, so **three** basic solutions:
> $$\mathbf x_1=\begin{bmatrix}3\\1\\0\\0\\0\end{bmatrix},\quad \mathbf x_2=\begin{bmatrix}-2\\0\\-6\\1\\0\end{bmatrix},\quad \mathbf x_3=\begin{bmatrix}-2\\0\\1\\0\\1\end{bmatrix}$$
> **Four equations, and only two of them carried information.** *(Verified — my reconstruction of the four-by-five matrix from the mangled extraction was checked by confirming it reduces to the printed row-echelon form.)*

---

## ✏️ Exercises

> [!question] Exercise 1 — solve, classify, and count *(warm-up)*
> (i) Solve by Gaussian elimination:
> $$x+2y-z=3,\qquad 2x+5y+z=7,\qquad 3x+7y=10$$
> (ii) State $\operatorname{rank}$ of the augmented matrix and verify Theorem 2's parameter count.
> (iii) Change the third equation's constant to $11$ and re-solve. What changed, and where does the algorithm detect it?

> [!example]- Solution
> **(i)** $R_2-2R_1$ and $R_3-3R_1$ give $[0\ 1\ 3\ |\ 1]$ **twice**; subtracting one from the other kills row 3. Then $R_1-2R_2$:
> $$\left[\begin{array}{ccc|c}1&0&-7&1\\0&1&3&1\\0&0&0&0\end{array}\right]$$
> With $z=t$: $\boxed{x=1+7t,\quad y=1-3t,\quad z=t}$
> *(Verified by substitution at $t=0$ and $t=2$: all three equations give $3,7,10$.)*
>
> **(ii)** $r=2$, $n=3$, so $n-r=1$ parameter ✓ — matching the single $t$.
> **The third equation was redundant:** $R_3=R_1+R_2$ in the original system, so it added nothing. **Three equations, two equations' worth of information.**
>
> **(iii)** Now $R_3-3R_1$ gives $[0\ 1\ 3\ |\ 2]$ against $[0\ 1\ 3\ |\ 1]$ from $R_2$, and subtracting leaves
> $$\left[\begin{array}{ccc|c}1&0&-7&0\\0&1&3&0\\0&0&0&1\end{array}\right]$$
> **The row $[0\ 0\ 0\ |\ 1]$ — inconsistent.**
>
> **The geometry: the left-hand sides still satisfy $R_3=R_1+R_2$, but the constants no longer do.** Three planes whose normals are dependent but whose offsets are not: they form a triangular prism with no common point. **A single digit changed the answer from an infinite family to nothing at all** — which is why near-dependent systems are numerically dangerous.

> [!question] Exercise 2 — all three outcomes from one parameter
> For which values of $a$ does the system
> $$x+y+z=2,\qquad x+2y+z=3,\qquad x+y+(a^2-3)z=a$$
> have (i) a unique solution, (ii) no solution, (iii) infinitely many solutions? Give the solution in each case.

> [!example]- Solution
> $R_2-R_1$ and $R_3-R_1$:
> $$\left[\begin{array}{ccc|c}1&1&1&2\\0&1&0&1\\0&0&a^2-4&a-2\end{array}\right]$$
> and $a^2-4=(a-2)(a+2)$, so **everything turns on the last row**.
>
> **(i) $a\ne\pm2$:** the pivot $a^2-4$ is nonzero, giving
> $$z=\frac{a-2}{(a-2)(a+2)}=\frac1{a+2},\qquad y=1,\qquad x=1-\frac1{a+2}$$
> **A unique solution.** *(Checked at $a=1$: $(x,y,z)=(\tfrac23,1,\tfrac13)$ ✓; at $a=3$: $(\tfrac45,1,\tfrac15)$ ✓.)*
>
> **(ii) $a=-2$:** the last row is $[0\ 0\ 0\ |\ -4]$ — **no solution.**
>
> **(iii) $a=2$:** the last row is $[0\ 0\ 0\ |\ 0]$ — it vanishes entirely. Now $r=2<3=n$, so one parameter: with $z=t$,
> $$x=1-t,\qquad y=1,\qquad z=t$$
> **Infinitely many solutions.**
>
> > [!tip] Why the cancellation of $a-2$ is the whole exercise
> > The last row is $(a-2)(a+2)z=(a-2)$. **When $a=2$ both sides vanish and the equation disappears; when $a=-2$ the left side vanishes but the right does not.** Dividing by $a-2$ without checking — the single most common error here — silently assumes $a\ne2$ and loses case (iii).
> >
> > **The general lesson: whenever a pivot involves a parameter, the cases where it is zero must be handled separately.**

> [!question] Exercise 3 — rank, counting, and what is impossible
> Decide each, with a reason or a counterexample.
>
> (i) A consistent system of 4 equations in 6 variables has a unique solution.
> (ii) A system whose augmented matrix is $3\times7$ can have rank 4.
> (iii) A homogeneous system of 5 equations in 3 unknowns has only the trivial solution.
> (iv) A system with more equations than variables must be inconsistent.
> (v) If a linear system has two distinct solutions, it has infinitely many.

> [!example]- Solution
> **(i) Impossible.** $r\le4$ (the number of rows) and $n=6$, so $n-r\ge2$ — **at least two parameters**, hence infinitely many solutions.
> **The general statement (Nicholson's Exercise 22): a consistent system with more variables than equations always has infinitely many solutions.**
>
> **(ii) Impossible.** A $3\times7$ matrix has only 3 rows, and the leading 1s occupy distinct rows, so $\operatorname{rank}\le3$. **Rank is bounded by both dimensions:** $\operatorname{rank}\le\min(m,n)$.
>
> **(iii) Possible.** Nothing rules it out — take $x=0$, $y=0$, $z=0$ as three of the five equations. What is *needed* is $r=3$; five equations make that easy to achieve but do not guarantee it. **Contrast (i): extra *equations* can pin things down, extra *variables* never can.**
>
> **(iv) False.** $x=1$, $2x=2$, $3x=3$ has more equations than variables and the unique solution $x=1$. **Extra equations may be redundant rather than contradictory** — the count tells you nothing; only the rank does.
>
> **(v) True, and it is the reason "exactly two solutions" never happens.** If $\mathbf x\ne\mathbf y$ both satisfy the system, consider $\mathbf z_t=\mathbf x+t(\mathbf y-\mathbf x)$. Each equation is linear, so
> $$\sum_i a_i(z_t)_i=(1-t)\sum_i a_ix_i+t\sum_i a_iy_i=(1-t)b+tb=b$$
> — **every point on the line through $\mathbf x$ and $\mathbf y$ is a solution.**
>
> > [!important] This is linearity doing the work
> > **The argument uses only that each equation is linear in the unknowns**, which is why it fails instantly for $x^2=1$ (two solutions) or $\sin x=0$ (countably many). **"Zero, one, or infinitely many" is a theorem about *linear* systems and about nothing else.**

> [!question] Exercise 4 — homogeneous systems and basic solutions
> Consider the homogeneous system with coefficient matrix
> $$A=\begin{bmatrix}1&2&-1&3\\2&4&1&0\\3&6&0&3\end{bmatrix}$$
> (i) Find $\operatorname{rank}A$ and predict the number of basic solutions **before** solving.
> (ii) Find the basic solutions and write the general solution as a linear combination.
> (iii) Verify that $\mathbf x_1+7\mathbf x_2$ is also a solution, and explain why this had to be so.
> (iv) Is the vector $(1,0,0,0)$ a solution? What does your answer say about the columns of $A$?

> [!example]- Solution
> **(i)** $R_2-2R_1=[0,0,3,-6]$ and $R_3-3R_1=[0,0,3,-6]$ — identical, so the third row dies. Dividing by 3 and clearing upward:
> $$\left[\begin{array}{cccc}1&2&0&1\\0&0&1&-2\\0&0&0&0\end{array}\right]$$
> $\operatorname{rank}A=2$, $n=4$, so **$n-r=2$ basic solutions.**
>
> **(ii)** Free variables $x_2=s$, $x_4=t$; then $x_1=-2s-t$ and $x_3=2t$:
> $$\mathbf x=s\underbrace{\begin{bmatrix}-2\\1\\0\\0\end{bmatrix}}_{\mathbf x_1}+t\underbrace{\begin{bmatrix}-1\\0\\2\\1\end{bmatrix}}_{\mathbf x_2}$$
> *(Both verified: $A\mathbf x_1=A\mathbf x_2=\mathbf 0$.)*
>
> **(iii)** It is a solution because **every linear combination of solutions to a homogeneous system is a solution** (§6) — take $s=1$, $t=7$. **No computation is needed**, and that is the point: the solution set is closed under addition and scaling, which is what makes it a *subspace*.
>
> **(iv)** $A(1,0,0,0)^{\mathsf T}=(1,2,3)^{\mathsf T}\ne\mathbf 0$ — **not a solution.**
>
> **What that means: the first column of $A$ is not zero, so $1\cdot\mathbf c_1+0+0+0\ne\mathbf 0$.** More usefully, run the reasoning the other way: $\mathbf x_1=(-2,1,0,0)$ *being* a solution says
> $$-2\mathbf c_1+1\cdot\mathbf c_2=\mathbf 0,\qquad\text{i.e.}\qquad \mathbf c_2=2\mathbf c_1$$
> — **a nontrivial solution of $A\mathbf x=\mathbf 0$ is precisely a dependence relation among the columns.** *(Check: column 2 is $(2,4,6)=2\times(1,2,3)$ ✓.)*
>
> > [!important] This identification is the whole of chapter 5 in advance
> > $$A\mathbf x=\mathbf 0\text{ has only }\mathbf x=\mathbf 0\iff\text{the columns of }A\text{ are independent}$$
> > **Basic solutions are a complete list of the dependencies among the columns**, and there are $n-r$ of them because $r$ columns are independent and the other $n-r$ are combinations of those. **Everything ch. 5 says about rank, nullity and independence is already visible here.**

> [!question] Exercise 5 — fitting curves, and a proof *(hard)*
> **(a)** Find the quadratic $y=a+bx+cx^2$ whose graph passes through $(-1,6)$, $(2,0)$ and $(3,2)$.
> **(b)** Find the circle $x^2+y^2+ax+by+c=0$ through $(-2,1)$, $(5,0)$ and $(4,1)$, and give its centre and radius.
> **(c)** Show that **any** three points with distinct $x$-coordinates lie on a curve $y=a+bx+cx^2$. Where does the argument break down if two $x$-coordinates coincide?

> [!example]- Solution
> **(a)** Each point gives one linear equation in $a,b,c$:
> $$a-b+c=6,\qquad a+2b+4c=0,\qquad a+3b+9c=2$$
> Row-reducing gives $\boxed{a=2,\ b=-3,\ c=1}$, i.e. $y=2-3x+x^2$.
> *(Check: $p(-1)=2+3+1=6$ ✓, $p(2)=2-6+4=0$ ✓, $p(3)=2-9+9=2$ ✓.)*
>
> **Note the structure: the unknowns are the *coefficients*, and the equations are linear in them even though the curve is not linear in $x$.** This is the general trick behind polynomial interpolation, and behind why polynomial regression is still "linear" regression ([[Econometrics/contents/00-Index|Econometrics]]).
>
> **(b)** Substituting each point into $x^2+y^2+ax+by+c=0$:
> $$-2a+b+c=-5,\qquad 5a+c=-25,\qquad 4a+b+c=-17$$
> Subtracting the first from the third gives $6a=-12$, so $a=-2$; then $c=-15$ and $b=6$:
> $$\boxed{x^2+y^2-2x+6y-15=0}$$
> Completing the square: $(x-1)^2+(y+3)^2=25$, so the **centre is $(1,-3)$ and the radius is $5$**.
> *(All three points verified.)*
>
> **(c)** Given $(p_1,q_1),(p_2,q_2),(p_3,q_3)$ with distinct $p_i$, we need $a,b,c$ with
> $$a+bp_i+cp_i^2=q_i,\qquad i=1,2,3$$
> — three equations in three unknowns with coefficient matrix
> $$V=\begin{bmatrix}1&p_1&p_1^2\\1&p_2&p_2^2\\1&p_3&p_3^2\end{bmatrix}$$
> **Suppose the system had no unique solution.** Then the associated homogeneous system $V\mathbf u=\mathbf 0$ would have a nontrivial solution $(a,b,c)\ne\mathbf 0$, meaning the quadratic $a+bx+cx^2$ vanishes at all three distinct points $p_1,p_2,p_3$. **But a nonzero polynomial of degree $\le2$ has at most 2 roots** — contradiction. So $V$ has rank 3, the system has a unique solution, and the curve exists and is unique. $\blacksquare$
>
> **If two $x$-coordinates coincide**, say $p_1=p_2$, then rows 1 and 2 of $V$ are identical, so $\operatorname{rank}V\le2$ and the argument collapses. Concretely:
> - if also $q_1=q_2$, the two constraints are the same and there are **infinitely many** quadratics through the points;
> - if $q_1\ne q_2$, the system is **inconsistent** — no function can take two values at one $x$.
>
> > [!tip] $V$ is the Vandermonde matrix, and this is a theorem in disguise
> > **$\det V=(p_2-p_1)(p_3-p_1)(p_3-p_2)$**, which is nonzero exactly when the $p_i$ are distinct — the same conclusion, reached in ch. 3 by determinants rather than by counting roots.
> >
> > **The general statement: $n+1$ points with distinct $x$-coordinates determine a unique polynomial of degree $\le n$.** This is what makes polynomial interpolation work, and — read pessimistically — it is also why **fitting a degree-$n$ polynomial to $n+1$ data points always gives a perfect fit and tells you nothing.** Interpolation and overfitting are the same theorem seen from two sides ([[Machine Learning/contents/00-Index|Machine Learning]]).

---

## 📝 Summary

- **A linear system has exactly three possible outcomes: no solution, exactly one, or infinitely many.** "Exactly two" is impossible, because the line joining two solutions consists entirely of solutions — a fact that uses linearity and nothing else.
- **The three elementary row operations preserve the solution set**, and the proof is entirely about their being **reversible**. That is why Type II forbids $k=0$ and Type III forbids adding a row to itself.
- **The Gaussian algorithm always terminates** and carries any matrix to (reduced) row-echelon form: leading 1s marching down and to the right, zeros below and left. **In hand calculation, deviate from it to avoid fractions.**
- **Gaussian elimination:** reduce the augmented matrix; if a row $[0\ \cdots\ 0\ |\ 1]$ appears the system is inconsistent; otherwise make the nonleading variables parameters and solve for the leading ones.
- **Back-substitution costs $\approx n^3/3$ operations versus $\approx n^3/2$ for full reduction** — both cubic, which is why LU-factorization exists.
- **Rank $=$ the number of leading 1s, and it does not depend on how you reduce.** For an $m\times n$ matrix, $\operatorname{rank}\le\min(m,n)$.
- **Theorem 2 is the chapter: a consistent system in $n$ variables with augmented rank $r$ has exactly $n-r$ parameters.** Unique when $r=n$, infinitely many when $r<n$. **This becomes rank–nullity in ch. 5 and the dimension theorem in ch. 7.**
- **Carrying symbolic constants through the reduction finds the *consistency condition*** — the value of the last row tells you when the system is solvable at all (Example 4: consistent iff $c=a-2b$).
- **Homogeneous systems are always consistent** (the trivial solution), and **more variables than equations guarantees a nontrivial solution.** The converse is false: what matters is $r<n$, not the equation count.
- **Any linear combination of solutions to a homogeneous system is a solution** — the solution set is closed under addition and scaling, i.e. it is a subspace. **This fails for non-homogeneous systems.**
- **The Gaussian algorithm produces $n-r$ basic solutions, and every solution is a linear combination of them.** Nonzero rescaling is allowed, which clears fractions.
- **"Is $\mathbf v$ a linear combination of $\mathbf x,\mathbf y,\dots$?" is a consistency question about a linear system** — and **a nontrivial solution of $A\mathbf x=\mathbf 0$ is exactly a dependence relation among the columns of $A$.** Chapter 5 is these two observations taken seriously.

---

## ⚠️ Important Notes

> [!warning] Different-looking answers can be the same answer
> Parametric solutions are not unique — different choices of free variable, or of parameter scaling, give expressions that look nothing alike.
>
> **The only reliable check is substitution into the original equations**, not comparison with the back of the book. And when comparing two parametrisations, ask whether each is obtainable from the other by a change of parameter (Example 5: $t\mapsto t/5$ turns $(\tfrac15,0,\tfrac35,1)$ into $(1,0,3,5)$).

> [!warning] Inconsistency has exactly one signature
> $$[\,0\ \ 0\ \ \cdots\ \ 0\ \ |\ \ c\,]\quad\text{with } c\ne0$$
> **Nothing else indicates inconsistency**, and in particular a **row of zeros in the *augmented* matrix does not** — that signals a redundant equation, which is entirely harmless (Exercise 1(i)).
>
> **The distinction matters:** $[0\ 0\ 0\ |\ 0]$ means "one equation told you nothing new"; $[0\ 0\ 0\ |\ 1]$ means "your equations contradict each other". **A single digit in the constant column separates them** (Exercise 1(iii)).

> [!warning] Counting equations is not counting information
> | Belief | Reality |
> |---|---|
> | "$n$ equations in $n$ unknowns $\Rightarrow$ unique solution" | **False** — the equations may be dependent ($r<n$) or contradictory |
> | "More equations than unknowns $\Rightarrow$ inconsistent" | **False** — extra equations may be redundant |
> | "Fewer equations than unknowns $\Rightarrow$ infinitely many" | **True if consistent**; it may still be inconsistent |
>
> **Only the rank tells you anything.** In applied terms: collecting more data rows does not help if they carry no new information, and **duplicated or perfectly collinear predictors look like information and are not.**

> [!warning] When a pivot contains a parameter, split into cases
> A step like "divide the last row by $a^2-4$" quietly assumes $a\ne\pm2$ — **and the interesting behaviour is exactly at the excluded values.**
>
> **Procedure: reduce as far as you can without dividing by anything that could vanish, then case-split on each such quantity.** In Exercise 2 the final row was $(a-2)(a+2)z=(a-2)$, and the three cases $a\ne\pm2$, $a=2$, $a=-2$ gave one solution, infinitely many, and none respectively.

> [!warning] Rank is defined before it is proved to be well defined
> Definition 1.4 says "the number of leading 1s in **any** row-echelon matrix" — **which presupposes that the number is the same for all of them.** Nicholson states this and defers the proof to chapter 5.
>
> **This is a real logical gap in the chapter as read**, not merely a stylistic one: nothing so far rules out two reductions of the same matrix giving different counts. **Accept it provisionally, and note that ch. 5 discharges the debt** (via "row rank = column rank = dimension of the row space").

> [!warning] Row operations change the columns, and this bites later
> Row-reducing **preserves** the solution set, the row space, and which *sets of columns* are independent. It **does not preserve** the column space itself.
>
> $$\begin{bmatrix}1&2\\2&4\end{bmatrix}\ \longrightarrow\ \begin{bmatrix}1&2\\0&0\end{bmatrix}$$
> — the column space was spanned by $(1,2)$ and is now spanned by $(1,0)$. **Different subspaces.**
>
> **So reading a basis for the column space off the reduced form is wrong**; you must take the *corresponding columns of the original matrix*. **This is the single most common error in chapter 5**, and it is worth planting the flag here.

> [!note] Cross-subject connections
> - [[02 - Matrix Algebra|Ch. 02]] — the augmented matrix becomes an object with its own arithmetic; **row operations turn out to be left-multiplication by elementary matrices** (§2.5).
> - [[03 - Determinants and Diagonalization|Ch. 03]] — $\det A\ne0$ will be one more equivalent of "$\operatorname{rank}A=n$", i.e. of unique solvability.
> - [[05 - The Vector Space Rn|Ch. 05]] — **basic solutions become a *basis* for the null space**, $n-r$ becomes the *nullity*, and the well-definedness of rank is finally proved.
> - [[07 - Linear Transformations|Ch. 07]] — Theorem 2's count $n=r+(n-r)$ becomes the **dimension theorem** $\dim V=\dim(\operatorname{im}T)+\dim(\ker T)$.
> - [[Econometrics/contents/00-Index|Econometrics]] — **perfect multicollinearity is $\operatorname{rank}(X)<k$**, i.e. a nontrivial solution of $X\mathbf c=\mathbf 0$; the "dummy variable trap" is a dependence relation among columns exactly like Exercise 4(iv).
> - [[Machine Learning/contents/00-Index|Machine Learning]] — Exercise 5(c) is polynomial interpolation, and read pessimistically it is **overfitting**: $n+1$ points are fitted exactly by a degree-$n$ polynomial, which is a fact about rank, not about learning.
> - [[Data Structures and Algorithms/contents/00-Index|Data Structures and Algorithms]] — Gaussian elimination is the canonical $O(n^3)$ algorithm, and the $n^3/2$ vs $n^3/3$ comparison is a constant-factor analysis of exactly the kind that subject formalises.
> - [[Optimization/contents/00-Index|Optimization]] — the **simplex algorithm** for linear *inequalities*, mentioned at the end of §1.2, is Gaussian elimination with a pivoting rule chosen to improve an objective.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **A logical gap in the text itself.** **Definition 1.4 defines rank as "the number of leading 1s in *any* row-echelon matrix to which $A$ can be carried"** — which is only meaningful if that number is independent of the reduction. **Nicholson states this without proof and defers it to chapter 5**, five chapters later, having in the meantime built Theorem 2 (§1.2) and Theorem 2 (§1.3) on top of it. He is explicit about the deferral, so this is a pedagogical choice rather than an error — **but the chapter's central quantity is undefined until ch. 5 as the book is actually read.**
>
> **PDF extraction — matrices are destroyed, and this chapter is nothing but matrices:**
> - **Every matrix loses its brackets, its row structure, and the position of its minus signs.** Nicholson's Example 3 of §1.1 has the augmented matrix $\left[\begin{smallmatrix}3&4&1&|&1\\2&3&0&|&0\\4&3&-1&|&-2\end{smallmatrix}\right]$, which extracts as the bare text `34 1 1 / 23 0 0 / 43 1 2−−` — **with both minus signs collected at the end of the last row.** **Every matrix in these notes has been reconstructed by hand and then verified by recomputing the example's stated answer.**
> - **One matrix is printed inconsistently within a single page.** In §1.2 Example 5, the matrix whose rank is being computed appears once with second row `21 0 3` and once with `21 3 0`. **Only the second gives rank 2** (the value the text asserts); the first has rank 3. **Resolved computationally in favour of $\left[\begin{smallmatrix}1&1&-1&4\\2&1&3&0\\0&1&-5&8\end{smallmatrix}\right]$**, and the reduction shown in the text confirms it (rows 2 and 3 become identical).
> - **Fractions extract as numerator-newline-denominator**, so $-\tfrac37$ appears as `3 / 7` with a stray `−` elsewhere on the line. Every fraction has been re-derived.
> - **Large delimiters extract as stray capitals:** `S … T` is a large column-vector bracket, and a lone `e` or `u` at the start of a display is a large brace grouping a system.
> - **`/bbR` is $\mathbb{R}$, `/cdots` is $\cdots$, `/vdots` and `/vertellipsis` are both $\vdots$, `/uni25ba.001` is the ▶ marking the start of a solution, `/a51.001` marks an exercise with a printed answer.** The last of these appears *inside* exercise text, so `/a51.001(b)` is simply "(b)".
> - **Figure 1 of §1.1** (three plots showing one, no, and infinitely many solutions for two lines) is an image; only the axis and equation labels survive. **The content is fully described in the prose**, so nothing is lost mathematically, but the picture that makes "three outcomes" obvious is gone.
> - **Example 5 of §1.3 has a genuine typo in the printed general solution**, where the second basic solution is introduced as "$\mathbf x_1=\dots$" twice — the second should be $\mathbf x_2$.
>
> **Verification performed:** every worked example in §§1.1–1.3 was independently row-reduced in exact rational arithmetic. Confirmed: $x=-\tfrac37,y=\tfrac27,z=\tfrac87$ (§1.1 Ex. 3); the inconsistency of §1.2 Ex. 2 (final row $[0\ 0\ 0\,|\,-3]$ after the printed reduction, which my reduction reproduces up to scaling); the general solution of §1.2 Ex. 3 **and its substitution back into all three original equations at three parameter values**; the consistency condition $c=a-2b$ and the resulting solutions of §1.2 Ex. 4 (checked at $a=b=1$, $c=-1$); $\operatorname{rank}=2$ in §1.2 Ex. 5; the general solution of §1.3 Ex. 1 (checked by substitution); the reduced form and both basic solutions of §1.3 Ex. 5; and **the full $4\times5$ matrix of §1.3 Ex. 6, reconstructed from the mangled extraction and confirmed by checking that it reduces to the printed row-echelon form and yields the printed basic solutions.** **All agree with the text.** No arithmetic errors were found in this chapter.
>
> **Scope note:** §§1.4–1.6 (network flow, electrical networks, chemical reactions) are Nicholson's optional applications. **All three are the same exercise — set up a linear system from a conservation law and solve it — so I have omitted them** rather than repeat §1.2 three times in different vocabulary. The one structural idea they share, that **flow conservation at each node gives one equation and the equations are always dependent** (their sum is $0=0$), is worth knowing and is the reason such systems always have free parameters.

#linear-algebra #linear-systems #gaussian-elimination #row-echelon #rank #homogeneous #basic-solutions
