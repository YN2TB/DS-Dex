---
subject: Discrete Mathematics
chapter: 7
tags: [ds, discrete-mathematics, recurrence-relations, fibonacci, characteristic-equation, divide-and-conquer, merge-sort, tower-of-hanoi]
source: "Johnsonbaugh, *Discrete Mathematics* 8e, ch. 7 (book pp. 327–372)"
---

# Recurrence Relations

[[02 - Proofs and Mathematical Induction|Chapter 02]] ended with a limitation stated plainly: **induction can verify a closed form but cannot find one.** [[04 - Algorithms and Their Analysis|Chapter 04]] then listed three cost equations — $T(n)=T(n-1)+c$, $T(n)=T(n/2)+c$, $T(n)=2T(n/2)+cn$ — asserted their answers, and deferred the solving to here.

**This is that chapter.** It supplies the two methods that actually produce closed forms, and then applies them to get the exact running times of selection sort, binary search and merge sort. It also settles a debt from [[05 - Number Theory and Cryptography|ch. 05]]: the Fibonacci sequence appeared there as the Euclidean algorithm's worst case, with the golden ratio $\phi$ asserted rather than derived. §3 derives it.

## 📘 Main Knowledge

### 1. Recurrence relations and initial conditions

> [!note] Definition
> A **recurrence relation** for the sequence $a_0,a_1,\dots$ is an equation expressing $a_n$ in terms of one or more of its predecessors $a_0,\dots,a_{n-1}$, for all $n$ beyond some point. **Initial conditions** are the start-up values that make the sequence determinate.

Both halves are needed. The relation alone defines infinitely many sequences; the initial conditions pick one out. **A $k$th-order relation needs exactly $k$ initial conditions** — the Fibonacci recurrence $f_n=f_{n-1}+f_{n-2}$ requires two, and supplying one leaves a one-parameter family.

> [!note] This is [[02 - Proofs and Mathematical Induction|ch. 02]] wearing different clothes
> A recurrence *is* a recursive definition, and the correspondence is exact: **the initial conditions are the basis step, the relation is the inductive step.** So setting up a recurrence and setting up an induction are the same act of finding case $n$ inside case $n+1$. The difference is direction — a recurrence computes forward, an induction verifies backward.

**Setting one up** has a reliable procedure: define $a_n$ to be the quantity you want, then find the smaller instances of the *same* quantity hiding inside instance $n$.

> [!example]- Five recurrences worth knowing
> **(a) Compound interest.** \$1000 at 12% compounded annually. If $A_n$ is the amount after $n$ years, then one more year multiplies by $1.12$:
> $$A_n=1.12\,A_{n-1},\qquad A_0=1000 .$$
>
> **(b) Subsets** (J Example 7.1.5). Let $S_n$ be the number of subsets of an $n$-element set. Going from $n-1$ to $n$ elements, every old subset either stays as it is or gains the new element — so it doubles:
> $$S_n=2S_{n-1},\qquad S_0=1 .$$
> **This is the multiplication-principle argument of [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]] §1 in recurrence form**, and §2 solves it to $2^n$.
>
> **(c) Strings avoiding a pattern** (J Example 7.1.6). Let $S_n$ count $n$-bit strings with **no** occurrence of `111`. Classify by how the string starts: `0…` (any valid string of length $n-1$ follows), `10…` (any valid string of length $n-2$), or `110…` (any valid string of length $n-3$) — and a valid string cannot begin `111`. These three cases are disjoint and exhaustive, so by the Addition Principle
> $$S_n=S_{n-1}+S_{n-2}+S_{n-3},\qquad S_1=2,\ S_2=4,\ S_3=7 .$$
> *(Verified by brute force through $n=12$: $2,4,7,13,24,44,81,149,274,504,927,1705$ — the recurrence reproduces all of them.)* **Three initial conditions, because the order is 3** — and note that classifying by the leading block is the standard trick for pattern-avoidance counts.
>
> **(d) Tower of Hanoi** (J Example 7.1.8). Move $n$ disks between pegs, never placing a larger disk on a smaller one. To move $n$ disks: move the top $n-1$ to the spare peg, move the bottom disk, then move the $n-1$ back. So
> $$c_n=2c_{n-1}+1,\qquad c_1=1 .$$
> **The recurrence *is* the algorithm** — this is [[04 - Algorithms and Their Analysis|ch. 04]] §5's point, and §2 solves it to $2^n-1$.
>
> **(e) Fibonacci.** $f_n=f_{n-1}+f_{n-2}$ with $f_1=f_2=1$. Second-order, and §3 gives its closed form.

**Not every recurrence has a usable closed form.** Johnsonbaugh's **Ackermann's function** is defined by a recurrence in two variables and grows faster than any primitive-recursive function; the **Catalan numbers** satisfy a nonlinear recurrence. The methods below cover an important special class, not everything.

### 2. Solving by iteration

The first method is direct: **unwind the recurrence until the initial condition appears, then recognise the pattern.**

> [!example]- Iteration, four times
> **(a) $S_n=2S_{n-1}$, $S_0=1$:**
> $$S_n=2S_{n-1}=2(2S_{n-2})=4S_{n-2}=\cdots=2^nS_0=\mathbf{2^n}.$$
>
> **(b) Compound interest** $A_n=1.12A_{n-1}$, $A_0=1000$: identically, $A_n=1000(1.12)^n$. So after 10 years, $1000(1.12)^{10}\approx\$3105.85$.
>
> **(c) Tower of Hanoi** $c_n=2c_{n-1}+1$, $c_1=1$. Now there is an additive term, so track it:
> $$c_n=2c_{n-1}+1=2(2c_{n-2}+1)+1=4c_{n-2}+2+1=8c_{n-3}+4+2+1=\cdots$$
> $$=2^{n-1}c_1+\big(2^{n-2}+\cdots+2+1\big)=2^{n-1}+\big(2^{n-1}-1\big)=\mathbf{2^n-1},$$
> using the **geometric sum** of [[02 - Proofs and Mathematical Induction|ch. 02]] §6. *(Verified: $c_1,\dots,c_{11}=1,3,7,15,31,63,127,255,511,1023,2047=2^n-1$.)*
>
> **The famous consequence:** the legend has 64 golden disks, requiring $2^{64}-1\approx1.8\times10^{19}$ moves. At one move per second that is about **585 billion years** — which is the point of the story, and a concrete illustration of [[04 - Algorithms and Their Analysis|ch. 04]]'s remark that exponential algorithms are not merely slow.
>
> **(d) A general first-order pattern.** $a_n=ra_{n-1}+c$ iterates to
> $$a_n=r^na_0+c\big(r^{n-1}+\cdots+r+1\big)=r^na_0+c\cdot\frac{r^n-1}{r-1}\quad(r\ne1),$$
> again by the geometric sum. **This one formula handles compound interest, Hanoi, and most first-order recurrences you will meet.**

> [!warning] Iteration is a heuristic, not a proof
> It produces a *candidate* closed form by pattern recognition — and pattern recognition can mislead. **Strictly, the result should then be verified by induction**, which is exactly the division of labour [[02 - Proofs and Mathematical Induction|ch. 02]] described: **iteration finds, induction confirms.** In practice one iterates, guesses, and checks a few values; for anything load-bearing, prove it.
>
> Iteration also **fails on second-order recurrences.** Try it on $f_n=f_{n-1}+f_{n-2}$ and each substitution produces *two* terms, then four, then eight — the expressions grow instead of collapsing. That failure is what motivates §3.

### 3. Linear homogeneous recurrences with constant coefficients

> [!note] Definition
> A **linear homogeneous recurrence relation of order $k$ with constant coefficients** has the form
> $$a_n=c_1a_{n-1}+c_2a_{n-2}+\cdots+c_ka_{n-k},\qquad c_k\ne0,$$
> with the $c_i$ constants.

Three words, each doing work — and Johnsonbaugh's non-examples show what each excludes:

| Recurrence | Fails because |
|---|---|
| $a_n=3a_{n-1}a_{n-2}$ | **not linear** — terms must be constant multiples of a single $a_{n-i}$ |
| $a_n-a_{n-1}=2n$ | **not homogeneous** — the right side has a term free of the sequence |
| $a_n=3n\,a_{n-1}$ | **coefficients not constant** |

> [!note] Theorem — distinct roots (order 2)
> Let $a_n=c_1a_{n-1}+c_2a_{n-2}$. If the **characteristic equation**
> $$t^2=c_1t+c_2,\qquad\text{i.e.}\qquad t^2-c_1t-c_2=0$$
> has **distinct** roots $r_1\ne r_2$, then every solution has the form
> $$a_n=b\,r_1^{\,n}+d\,r_2^{\,n}$$
> for constants $b,d$ determined by the initial conditions.

**Where the characteristic equation comes from.** Guess $a_n=t^n$ and substitute: $t^n=c_1t^{n-1}+c_2t^{n-2}$. Divide by $t^{n-2}$ and you get $t^2=c_1t+c_2$. So **the characteristic equation is just "which geometric sequences satisfy this recurrence?"** — and since the recurrence is linear and homogeneous, any linear combination of solutions is a solution, which is why $br_1^n+dr_2^n$ works.

> [!note] Theorem — repeated root
> If the characteristic equation has a **single** (double) root $r$, then every solution has the form
> $$a_n=b\,r^{\,n}+d\,n\,r^{\,n}=(b+dn)r^{\,n}.$$

**The extra factor of $n$ is necessary**, because $r_1=r_2$ collapses $br_1^n+dr_2^n$ to $(b+d)r^n$ — one parameter, not enough to satisfy two initial conditions.

*(Verified on $S_n=4S_{n-1}-4S_{n-2}$: the characteristic equation is $t^2-4t+4=(t-2)^2$, a double root $r=2$. With $S_0=1,S_1=3$ we get $b=1$ and $2(1+d)=3$, so $d=\tfrac12$, giving $S_n=(1+\tfrac n2)2^n$. Against the recurrence: $1,3,8,20,48,112,256,576,1280$ — exact match.)*

> [!example]- The Fibonacci closed form, and where $\phi$ comes from
> $f_n=f_{n-1}+f_{n-2}$ has characteristic equation
> $$t^2=t+1\qquad\Longrightarrow\qquad t=\frac{1\pm\sqrt5}2 .$$
> The roots are distinct, so with $\phi=\frac{1+\sqrt5}2$ and $\psi=\frac{1-\sqrt5}2$ the solution is $f_n=b\phi^n+d\psi^n$. Imposing $f_1=f_2=1$ and solving gives $b=1/\sqrt5$, $d=-1/\sqrt5$:
> $$\boxed{\ f_n=\frac1{\sqrt5}\left[\left(\frac{1+\sqrt5}2\right)^{\!n}-\left(\frac{1-\sqrt5}2\right)^{\!n}\right]\ }$$
> **Binet's formula.** *(Verified symbolically: it returns exactly $1,1,2,3,5,8,13,21,34,55,89,144$ for $n=1,\dots,12$.)*
>
> **This is a genuinely surprising formula** — an integer sequence expressed with two irrational numbers, whose irrational parts cancel at every $n$.
>
> **And it settles [[05 - Number Theory and Cryptography|ch. 05]]'s debt.** Since $|\psi|=0.618<1$, the second term vanishes and $f_n\approx\phi^n/\sqrt5$: **the Fibonacci numbers grow geometrically with ratio $\phi=1.6180\dots$, the golden ratio.** Hence the ratio of consecutive terms tends to $\phi$ *(verified: $1.6190,1.6182,1.61806,1.618037$ at $n=8,10,12,14$)*, and hence Lamé's bound — $n$ Euclidean steps force $a\ge f_{n+2}\approx\phi^{n+2}$, so $n=O(\log_\phi a)$. **The $\phi$ asserted in ch. 05 is the dominant root of this characteristic equation.**

### 4. Applications: the running time of three algorithms

This is where the chapter pays off. Each algorithm's structure gives a recurrence; solving it gives the complexity.

> [!note] Selection sort — $\Theta(n^2)$
> Find the largest element ($n-1$ comparisons), put it last, and sort the remaining $n-1$ recursively:
> $$a_n=a_{n-1}+(n-1),\qquad a_1=0 .$$
> Iterating:
> $$a_n=(n-1)+(n-2)+\cdots+1+0=\frac{n(n-1)}2=\Theta(n^2).$$
> **The sum is [[02 - Proofs and Mathematical Induction|ch. 02]]'s first induction, and the answer matches insertion sort's worst case from [[04 - Algorithms and Their Analysis|ch. 04]]** — both are quadratic, for the same structural reason.

> [!note] Binary search — $\Theta(\lg n)$ (Theorem 7.3.4)
> One comparison, then recurse on half:
> $$a_n=a_{\lfloor n/2\rfloor}+1,\qquad a_1=1 .$$
> Each step halves $n$, so the number of steps is the number of halvings needed to reach 1:
> $$a_n=\lfloor\lg n\rfloor+1=\Theta(\lg n).$$
> *(Verified at $n=1,2,3,4,7,8,15,16,100,1000$ against $\lfloor\lg n\rfloor+1$ — exact at every value, confirming ch. 04 Exercise 5.)*

> [!note] Merge sort — $\Theta(n\lg n)$ (Theorem 7.3.10)
> **Merging first** (Theorem 7.3.7): merging two sorted sequences of total length $n$ takes at most $n-1$ comparisons in the worst case — each comparison outputs one element, and the last element needs none. *(Verified: merging $[1,3,5]$ with $[2,4,6]$ takes exactly $5=n-1$ comparisons, the alternating worst case.)*
>
> **Then merge sort:** split in half, sort each half, merge.
> $$a_n=2a_{n/2}+(n-1),\qquad a_1=0 .$$
> For $n=2^k$ this solves exactly to
> $$a_n=n\lg n-n+1=\Theta(n\lg n).$$
> *(Verified: $a_n=0,1,5,17,49,129,321$ at $n=1,2,4,8,16,32,64$, matching $n\lg n-n+1$ at every power of two up to $2^{11}$.)*

> [!warning] The two-line comparison that justifies the whole chapter
> | | comparisons at $n=2^{20}\approx10^6$ |
> |---|---|
> | selection sort, $\tfrac{n(n-1)}2$ | $\approx5.5\times10^{11}$ |
> | merge sort, $n\lg n-n+1$ | $\approx1.9\times10^7$ |
>
> **A factor of about 28,000** — and it came from changing the recurrence from $a_{n-1}+(n-1)$ to $2a_{n/2}+(n-1)$, i.e. from *peeling one element* to *splitting in half*. **Divide and conquer is the single most valuable structural idea in algorithm design, and the recurrence is where you see why.**
>
> Johnsonbaugh adds the sharper claim: **any sorting algorithm that moves items by comparison is $\Omega(n\lg n)$ in the worst case, so merge sort is optimal.** That lower bound is proved in [[09 - Trees|ch. 09]] using decision trees and the $\lg(n!)=\Theta(n\lg n)$ estimate from [[04 - Algorithms and Their Analysis|ch. 04]] and [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]]. **Once both are in hand the question is closed** — no comparison sort can beat merge sort's order.

**The three shapes to recognise on sight:**

| Recurrence | Solution | Typical source |
|---|---|---|
| $a_n=a_{n-1}+c$ | $\Theta(n)$ | one pass, constant work per step |
| $a_n=a_{n-1}+cn$ | $\Theta(n^2)$ | one pass, linear work per step (selection sort) |
| $a_n=a_{n/2}+c$ | $\Theta(\lg n)$ | halve, constant work (binary search) |
| $a_n=2a_{n/2}+cn$ | $\Theta(n\lg n)$ | halve **both** sides, linear merge (merge sort) |
| $a_n=2a_{n-1}+c$ | $\Theta(2^n)$ | two subproblems of size $n-1$ (Hanoi) |

**The last two rows are the ones to compare.** Splitting into two halves gives $n\lg n$; splitting into two problems each nearly as big as the original gives $2^n$. The difference between tractable and hopeless is whether the subproblems *shrink*.

## ✏️ Exercises

**1. (Setting up recurrences.)** Find a recurrence relation and initial conditions for each. (a) The number $H_n$ of moves to solve the Tower of Hanoi with $n$ disks. (b) The number $a_n$ of $n$-bit strings containing no two consecutive $0$s. (c) The number $r_n$ of regions into which $n$ lines in general position divide the plane. (d) The amount $A_n$ in an account after $n$ months at 6% annual interest compounded monthly, with \$200 deposited at the end of each month, starting from \$0.

> [!example]- Solution
> **(a)** To move $n$ disks: move the top $n-1$ off (that is $H_{n-1}$ moves), move the largest (1 move), move the $n-1$ back ($H_{n-1}$ moves):
> $$H_n=2H_{n-1}+1,\qquad H_1=1 .$$
>
> **(b)** Classify by the **last** bit. If it is $1$, the preceding $n-1$ bits are any valid string: $a_{n-1}$ ways. If it is $0$, the bit before must be $1$ (no two consecutive $0$s), and the preceding $n-2$ bits are any valid string: $a_{n-2}$ ways. Disjoint and exhaustive, so
> $$a_n=a_{n-1}+a_{n-2},\qquad a_1=2,\ a_2=3 .$$
> **This is the Fibonacci recurrence**, and indeed $a_n=f_{n+2}$: the counts run $2,3,5,8,13,\dots$ *(Check $n=2$ by hand: `01`,`10`,`11` — three strings, `00` excluded ✓)* **A pleasing fact worth noticing: Fibonacci counts binary strings without consecutive zeros.**
>
> **(c)** From [[02 - Proofs and Mathematical Induction|ch. 02]] Exercise 5(b): adding the $n$th line crosses the existing $n-1$ lines in $n-1$ distinct points, which cut it into $n$ pieces, each splitting one region in two:
> $$r_n=r_{n-1}+n,\qquad r_0=1 .$$
>
> **(d)** Monthly rate $=0.06/12=0.005$. Each month the balance grows by that factor and then \$200 is added:
> $$A_n=1.005\,A_{n-1}+200,\qquad A_0=0 .$$
> **This is the general first-order form $a_n=ra_{n-1}+c$** of §2(d), and Exercise 2(d) solves it.
>
> **The common technique in (b) and in §1(c): classify by the first or last position**, making the cases disjoint so the Addition Principle applies. Choosing *which* position to classify by is the skill — here the last bit works because the constraint is local.

**2. (Solving by iteration.)** Solve each by iteration, then verify at $n=1,2,3$. (a) $H_n=2H_{n-1}+1$, $H_1=1$. (b) $r_n=r_{n-1}+n$, $r_0=1$. (c) $a_n=3a_{n-1}$, $a_0=5$. (d) $A_n=1.005A_{n-1}+200$, $A_0=0$ — and give $A_{12}$.

> [!example]- Solution
> **(a)** $H_n=2H_{n-1}+1=4H_{n-2}+2+1=8H_{n-3}+4+2+1=\cdots=2^{n-1}H_1+\sum_{i=0}^{n-2}2^i$. With $H_1=1$ and the geometric sum $\sum_{i=0}^{n-2}2^i=2^{n-1}-1$:
> $$H_n=2^{n-1}+2^{n-1}-1=\mathbf{2^n-1}.$$
> Check: $H_1=1$, $H_2=3$, $H_3=7$ ✓ *(verified to $n=11$)*
>
> **(b)** $r_n=r_{n-1}+n=r_{n-2}+(n-1)+n=\cdots=r_0+\big(1+2+\cdots+n\big)$, so
> $$r_n=1+\frac{n(n+1)}2=\mathbf{\frac{n^2+n+2}2}.$$
> Check: $r_0=1$, $r_1=2$, $r_2=4$, $r_3=7$ ✓ — matching ch. 02's $1+n+\binom n2$, since $\binom n2=\frac{n(n-1)}2$ and $1+n+\frac{n(n-1)}2=\frac{n^2+n+2}2$ ✓
>
> **(c)** $a_n=3a_{n-1}=9a_{n-2}=\cdots=3^na_0=\mathbf{5\cdot3^n}$. Check: $5,15,45$ ✓
>
> **(d)** Using §2(d) with $r=1.005$, $c=200$, $A_0=0$:
> $$A_n=1.005^n\cdot0+200\cdot\frac{1.005^n-1}{1.005-1}=200\cdot\frac{1.005^n-1}{0.005}=40000\big(1.005^n-1\big).$$
> Check $n=1$: $40000(0.005)=200$ ✓ $n=2$: $40000(1.010025-1)=401.00$, and directly $1.005(200)+200=401.00$ ✓
> $$A_{12}=40000\big(1.005^{12}-1\big)=40000(0.0616778)\approx\mathbf{\$2467.11}.$$
> **Note this is more than $12\times200=\$2400$** — the extra \$67.11 is the interest, and the formula makes visible that it is the geometric sum doing the work. This is the standard annuity formula, derived rather than looked up.

**3. (Characteristic equation, distinct roots.)** Solve $a_n=5a_{n-1}-6a_{n-2}$ with $a_0=1$, $a_1=0$. Verify at $n=2,3,4$.

> [!example]- Solution
> **Characteristic equation.** Substituting $a_n=t^n$ and dividing by $t^{n-2}$:
> $$t^2=5t-6\qquad\Longrightarrow\qquad t^2-5t+6=0\qquad\Longrightarrow\qquad (t-2)(t-3)=0,$$
> so $r_1=2$, $r_2=3$ — **distinct**, so the general solution is
> $$a_n=b\cdot2^n+d\cdot3^n .$$
>
> **Fit the initial conditions.**
> $$n=0:\ b+d=1,\qquad n=1:\ 2b+3d=0 .$$
> From the first, $b=1-d$; substituting, $2-2d+3d=0$, so $d=-2$ and $b=3$:
> $$\boxed{\ a_n=3\cdot2^n-2\cdot3^n\ }$$
>
> **Verify.** From the formula: $a_2=12-18=-6$, $a_3=24-54=-30$, $a_4=48-162=-114$.
> From the recurrence: $a_2=5(0)-6(1)=-6$ ✓, $a_3=5(-6)-6(0)=-30$ ✓, $a_4=5(-30)-6(-6)=-150+36=-114$ ✓
>
> **Two remarks.** (i) The sequence is eventually dominated by $-2\cdot3^n$, since $3>2$ — **the largest root in absolute value always controls the asymptotics**, which is exactly the principle that gave $\phi$ for Fibonacci. (ii) **Always verify against the recurrence, not just the initial conditions.** Fitting $a_0$ and $a_1$ only checks two values; computing $a_2$ both ways checks that the *form* is right.

**4. (Repeated root, and Fibonacci.)** (a) Solve $a_n=6a_{n-1}-9a_{n-2}$ with $a_0=2$, $a_1=9$. (b) Explain why the repeated-root case needs the factor $n$. (c) Derive Binet's formula for the Fibonacci sequence and use it to explain the golden ratio's appearance in [[05 - Number Theory and Cryptography|ch. 05]].

> [!example]- Solution
> **(a)** $t^2-6t+9=(t-3)^2$, a **double root** $r=3$. So by the repeated-root theorem,
> $$a_n=(b+dn)3^n .$$
> Initial conditions: $n=0$ gives $b=2$; $n=1$ gives $3(2+d)=9$, so $d=1$:
> $$\boxed{\ a_n=(2+n)3^n\ }$$
> Verify: $a_2=4\cdot9=36$, and from the recurrence $6(9)-9(2)=54-18=36$ ✓ $a_3=5\cdot27=135$, and $6(36)-9(9)=216-81=135$ ✓
>
> **(b)** If we tried $a_n=br_1^n+dr_2^n$ with $r_1=r_2=r$, we would get
> $$a_n=br^n+dr^n=(b+d)r^n,$$
> which has **one** free parameter ($b+d$), not two. A second-order recurrence has two initial conditions, so a general solution needs two parameters — one is not enough to satisfy both.
>
> The factor $n$ supplies a genuinely independent second solution: one checks that $nr^n$ satisfies the recurrence whenever $r$ is a double root, and $r^n$ and $nr^n$ are not multiples of each other. **So $(b+dn)r^n$ has the two parameters required.** *(This is the same phenomenon as repeated roots in linear differential equations, where the second solution picks up a factor of $x$.)*
>
> **(c)** Fibonacci: $f_n=f_{n-1}+f_{n-2}$, so $t^2=t+1$, i.e. $t^2-t-1=0$, giving the **distinct** roots
> $$\phi=\frac{1+\sqrt5}2\approx1.6180,\qquad \psi=\frac{1-\sqrt5}2\approx-0.6180 .$$
> So $f_n=b\phi^n+d\psi^n$. With $f_1=f_2=1$, solving the two equations gives $b=1/\sqrt5$, $d=-1/\sqrt5$:
> $$f_n=\frac{\phi^n-\psi^n}{\sqrt5}=\frac1{\sqrt5}\left[\left(\frac{1+\sqrt5}2\right)^{\!n}-\left(\frac{1-\sqrt5}2\right)^{\!n}\right]$$
> *(verified symbolically against the recurrence for $n=1,\dots,12$).*
>
> **Why $\phi$ governs ch. 05.** Since $|\psi|\approx0.618<1$, the term $\psi^n\to0$, so
> $$f_n\approx\frac{\phi^n}{\sqrt5}\quad\text{and}\quad \frac{f_{n+1}}{f_n}\to\phi$$
> *(verified: $1.6190,1.6182,1.618056,1.618037$ at $n=8,10,12,14$, converging to $1.6180339\dots$)*.
>
> [[05 - Number Theory and Cryptography|Ch. 05]] §3 showed that the Euclidean algorithm's worst case on $n$ modulus operations forces $a\ge f_{n+2}$. Substituting the growth rate:
> $$a\gtrsim\frac{\phi^{n+2}}{\sqrt5}\quad\Longrightarrow\quad n=O(\log_\phi a)=O(\log a).$$
> **So the $\phi$ that appeared in Lamé's theorem is precisely the dominant root of the Fibonacci characteristic equation** — asserted there, derived here. **The general moral: the largest root in absolute value determines the asymptotic growth of any solution**, which is why solving the characteristic equation is often all you need even without fitting the constants.

**5. (Hard — divide and conquer.)** (a) Show that merging two sorted sequences of total length $n$ needs at most $n-1$ comparisons, and exhibit a worst case. (b) Write and solve merge sort's recurrence for $n=2^k$, obtaining an exact formula. (c) Compare selection sort and merge sort at $n=2^{20}$. (d) Explain structurally why $2a_{n/2}+cn$ gives $\Theta(n\lg n)$ while $2a_{n-1}+c$ gives $\Theta(2^n)$. (e) What would it take to prove merge sort *optimal*?

> [!example]- Solution
> **(a)** Each comparison of the two front elements outputs exactly one element to the result. After $n-1$ elements have been output, only one remains, and it can be appended with **no** comparison. So at most $n-1$ comparisons. $\blacksquare$
>
> **Worst case: strict alternation.** Merging $[1,3,5]$ with $[2,4,6]$ forces a comparison for each of the first five outputs *(verified: exactly $5=n-1$ comparisons)*. The **best** case is when one sequence is entirely below the other — $[1,2,3]$ with $[4,5,6]$ needs only 3.
>
> **(b)** Split into halves of size $n/2$, sort each, then merge at cost $n-1$:
> $$a_n=2a_{n/2}+(n-1),\qquad a_1=0 .$$
> Iterating for $n=2^k$:
> $$a_{2^k}=2a_{2^{k-1}}+(2^k-1)=4a_{2^{k-2}}+2(2^{k-1}-1)+(2^k-1)=\cdots$$
> Each of the $k$ levels contributes $2^k$ from the linear terms and subtracts a geometric series of $1$s:
> $$a_n=\underbrace{k\cdot2^k}_{n\lg n}-\underbrace{\big(2^{k-1}+\cdots+2+1\big)}_{2^k-1}=n\lg n-n+1 .$$
> *(Verified exactly: $a_n=0,1,5,17,49,129,321$ at $n=1,2,4,8,16,32,64$, and the formula matches at every power of two through $2^{11}$.)*
>
> So $a_n=n\lg n-n+1=\Theta(n\lg n)$.
>
> **(c)** At $n=2^{20}=1{,}048{,}576$:
>
> | | comparisons |
> |---|---|
> | selection sort, $\frac{n(n-1)}2$ | $\approx5.50\times10^{11}$ |
> | merge sort, $n\lg n-n+1$ | $\approx1.94\times10^7$ |
>
> **A factor of roughly 28,000.** At a million comparisons per second that is about a week versus twenty seconds.
>
> **(d) The difference is whether the subproblems shrink.**
>
> For $a_n=2a_{n/2}+cn$: the recursion tree has depth $\lg n$, and at each level the subproblems' *total* size is still $n$, so each level costs $\Theta(n)$. Total $\Theta(n)\times\Theta(\lg n)=\Theta(n\lg n)$.
>
> For $a_n=2a_{n-1}+c$: the depth is $n$, and the number of subproblems **doubles** at each level while their size barely shrinks. The tree has $\approx2^n$ nodes. Total $\Theta(2^n)$.
>
> **So "divide and conquer" earns its name only when the division is genuinely into *fractions* of the input.** Two subproblems of size $n/2$ are cheap; two of size $n-1$ are catastrophic. The Tower of Hanoi is the second kind — and unavoidably so, since $2^n-1$ moves are genuinely required.
>
> **(e)** Part (b) shows merge sort is $O(n\lg n)$. Optimality requires a matching **lower bound on the problem**: that *every* comparison-based sorting algorithm needs $\Omega(n\lg n)$ comparisons in the worst case.
>
> The argument, completed in [[09 - Trees|ch. 09]]: model any comparison sort as a **decision tree** whose leaves are the possible outcomes. Sorting $n$ distinct elements must distinguish all $n!$ permutations, so the tree has at least $n!$ leaves; a binary tree of height $h$ has at most $2^h$ leaves, so $2^h\ge n!$ and
> $$h\ge\lg(n!)=\Theta(n\lg n)$$
> using the estimate from [[04 - Algorithms and Their Analysis|ch. 04]] §3. The height is the worst-case number of comparisons. $\blacksquare$
>
> **Then merge sort is optimal in order**, and the question is closed — no comparison sort can do asymptotically better.
>
> **Note carefully what the bound does *not* say** ([[04 - Algorithms and Their Analysis|ch. 04]]'s Important Note 13): it applies only to algorithms that sort **by comparing elements**. Radix and counting sort inspect digits instead and can beat $n\lg n$ on restricted inputs — they escape the model rather than the theorem. **A lower bound always attaches to a problem *in a model of computation*.**

## 📝 Summary

- A **recurrence relation** expresses $a_n$ in terms of earlier terms; **initial conditions** pick out one sequence. **A $k$th-order relation needs exactly $k$ initial conditions.**
- **A recurrence is a recursive definition**, with the initial conditions as the basis step and the relation as the inductive step — the [[02 - Proofs and Mathematical Induction|ch. 02]] correspondence, exactly.
- **To set one up:** define $a_n$ as the quantity wanted, then find smaller instances of the *same* quantity inside instance $n$. **Classifying by the first or last position** makes the cases disjoint so the Addition Principle applies.
- **Iteration** unwinds the recurrence to the initial condition and recognises the pattern. The general first-order solution is
$$a_n=ra_{n-1}+c\ \Longrightarrow\ a_n=r^na_0+c\cdot\frac{r^n-1}{r-1}\quad(r\ne1),$$
which covers compound interest, Hanoi, and annuities. **Iteration is a heuristic — it finds; induction confirms.** It also **fails on second-order recurrences**, where substitutions multiply instead of collapsing.
- **Linear homogeneous with constant coefficients:** $a_n=c_1a_{n-1}+\cdots+c_ka_{n-k}$. *Linear* excludes $a_{n-1}a_{n-2}$; *homogeneous* excludes a term free of the sequence; *constant coefficients* excludes $3n\,a_{n-1}$.
- **Substituting $a_n=t^n$ gives the characteristic equation** $t^2=c_1t+c_2$. **Distinct roots** $r_1\ne r_2$: $a_n=br_1^n+dr_2^n$. **Double root** $r$: $a_n=(b+dn)r^n$ — the factor $n$ is needed because otherwise there is only one free parameter for two initial conditions.
- **Binet's formula:** $f_n=\frac1{\sqrt5}\big[\phi^n-\psi^n\big]$ with $\phi=\frac{1+\sqrt5}2$, $\psi=\frac{1-\sqrt5}2$ — an integer sequence written with irrationals that cancel at every $n$. Since $|\psi|<1$, $f_n\approx\phi^n/\sqrt5$ and $f_{n+1}/f_n\to\phi$.
- **The largest root in absolute value controls the asymptotics.** That is why $\phi$ governs Lamé's bound in [[05 - Number Theory and Cryptography|ch. 05]] — asserted there, derived here.
- **The three algorithm analyses:** selection sort $a_n=a_{n-1}+(n-1)\Rightarrow\frac{n(n-1)}2=\Theta(n^2)$; binary search $a_n=a_{\lfloor n/2\rfloor}+1\Rightarrow\lfloor\lg n\rfloor+1=\Theta(\lg n)$; **merge sort $a_n=2a_{n/2}+(n-1)\Rightarrow n\lg n-n+1=\Theta(n\lg n)$**, with merging costing at most $n-1$ comparisons.
- **The shapes to recognise:** $a_{n-1}+c\Rightarrow\Theta(n)$; $a_{n-1}+cn\Rightarrow\Theta(n^2)$; $a_{n/2}+c\Rightarrow\Theta(\lg n)$; $2a_{n/2}+cn\Rightarrow\Theta(n\lg n)$; $2a_{n-1}+c\Rightarrow\Theta(2^n)$.
- **Divide and conquer works only when subproblems are *fractions* of the input.** Two of size $n/2$ give $n\lg n$; two of size $n-1$ give $2^n$. That distinction is the whole difference between merge sort and the Tower of Hanoi.
- **Merge sort is optimal**, once [[09 - Trees|ch. 09]]'s decision-tree bound $h\ge\lg(n!)=\Theta(n\lg n)$ is in hand — but only among **comparison-based** sorts.

## ⚠️ Important Notes

1. **Count your initial conditions.** A $k$th-order recurrence needs $k$ of them; supplying fewer leaves a family of sequences, and supplying more may be inconsistent.
2. **State the range of $n$ for which the relation holds.** $S_n=S_{n-1}+S_{n-2}+S_{n-3}$ makes sense only for $n\ge4$, which is why there are three initial conditions and not two.
3. **When setting up a recurrence, make the cases disjoint and exhaustive.** Classifying $n$-bit strings by their leading block or final bit works because those cases partition; overlapping cases silently double-count.
4. **Iteration produces a conjecture.** Verify it — at minimum against several values, and by induction if it matters. The pattern you "see" after three substitutions is not a proof.
5. **Do not attempt iteration on a second-order recurrence.** Each substitution doubles the number of terms. Use the characteristic equation.
6. **Check the three hypotheses before using the characteristic-equation method:** linear, homogeneous, constant coefficients. $a_n-a_{n-1}=2n$ fails the second and needs a different technique (particular plus homogeneous solution).
7. **Do not forget the factor $n$ when the root is repeated.** $(b+dn)r^n$, not $br^n$ — otherwise you have one parameter for two conditions and the system is unsolvable.
8. **Fit the constants using the initial conditions, then verify against the *recurrence*.** Matching $a_0$ and $a_1$ only confirms two values; recomputing $a_2$ both ways confirms the form.
9. **The dominant root tells you the growth rate without fitting constants.** If you only need asymptotics, solve the characteristic equation and stop.
10. **Binet's formula is exact but numerically treacherous.** Computing $f_{100}$ in floating point loses precision because $\phi^{100}$ is huge and the subtraction is delicate; the recurrence is more accurate for exact work. **A closed form is not automatically the better way to compute.**
11. **Distinguish "the recurrence for the algorithm" from "the recurrence for its cost".** The Tower of Hanoi's *algorithm* is $H_n=2H_{n-1}+1$ read as instructions; its *cost* is the same equation read as a count. They coincide here and often do not.
12. **$\Theta(2^n)$ from $2a_{n-1}+c$ is not a failure of analysis.** The Tower of Hanoi genuinely requires $2^n-1$ moves — the exponential is in the problem, not the method. Do not go looking for a better algorithm.
13. **The $\Omega(n\lg n)$ sorting bound applies only to comparison-based sorts.** Radix and counting sort beat it by leaving the model. A lower bound is a statement about a problem *in a model*.
14. **Watch the floor functions.** Binary search's recurrence is $a_{\lfloor n/2\rfloor}+1$, and the clean $n=2^k$ analysis hides the general case. The $\Theta$ result is unaffected, but exact counts need care.
15. **A closed form is not always available.** Ackermann's function and the Catalan numbers satisfy recurrences outside this chapter's class. **The methods here cover an important special case, not all recurrences** — generating functions and the Master Theorem go further.

> [!warning] Gaps in the source material
> **Extraction was good for prose, definitions and theorem statements.** The `/Omega1` and `/Theta1` artefacts continue (see `00-Index.md`).
>
> **The displayed algebra is again largely lost, and in this chapter that is nearly all the content.** Every `SOLUTION` in §§7.1–7.2 arrives as its opening sentence with the derivation dropped: Examples 7.2.1–7.2.5 (all the iteration examples), Theorem 7.2.11 and Theorem 7.2.14 (**stated as "Let" and nothing more** — both theorem statements are entirely missing their conclusions), and Example 7.2.13's Fibonacci derivation. **So §3's two theorems are reconstructed from their standard form and from the surviving prose around them**, and every solution in this note was re-derived and verified:
> - Tower of Hanoi $2^n-1$ checked to $n=11$;
> - the no-`111` recurrence checked against **brute-force enumeration** through $n=12$ ($2,4,7,13,24,44,81,149,274,504,927,1705$);
> - **Binet's formula verified symbolically** with `sympy` against the recurrence for $n=1,\dots,12$, and $f_{n+1}/f_n\to\phi$ confirmed numerically;
> - the repeated-root example $S_n=4S_{n-1}-4S_{n-2}$ solved to $(1+\tfrac n2)2^n$ and checked to $n=8$;
> - **merge sort's exact count $n\lg n-n+1$ verified at every power of two through $2^{11}$**;
> - binary search's $\lfloor\lg n\rfloor+1$ verified at ten values;
> - merging's $n-1$ worst case verified by instrumented merge.
>
> **All the numbered Algorithms extract as empty headings again** — Algorithms 7.3.1 (selection sort), 7.3.2 (binary search), 7.3.5 (merge) and 7.3.8 (merge sort) survive as titles with a few line numbers. §4 therefore describes their structure and derives their recurrences from that description rather than quoting code; the recurrences were then checked against instrumented implementations.
>
> **Several worked examples are unrecoverable and are not reproduced.** Johnsonbaugh's deer-population examples (7.2.3, 7.2.12) lose their growth rates entirely — the text says "the deer population of Rustic County is 1000 at time" and stops — so the specific models cannot be reconstructed and §2's population example is omitted. Likewise **Example 7.1.9's cobweb model in economics** retains its narrative but not its constants, **Example 7.1.7's Catalan recurrence** and **Example 7.1.10's Ackermann's function** lose their defining equations (both are mentioned in §1 as examples of recurrences outside this chapter's methods, without formulas), and **Example 7.2.5's solution of the cobweb recurrence** is lost. These are flagged rather than guessed at.
>
> **All figures are images and are lost**, including Figure 7.3.1 (the merge trace) and **Figure 7.3.2 (the merge-sort trace)**, which is how merge sort is conventionally taught. §4 states the recurrence and its solution instead. The Tower of Hanoi diagram is also lost, though the puzzle is fully described in prose.
>
> **§7.4 (The Closest-Pair Problem) is omitted.** Johnsonbaugh marks it optional. It is a genuinely elegant divide-and-conquer application achieving $\Theta(n\lg n)$ for a geometric problem, and it is the one omission from this chapter a reader might regret — **flagged here in case the syllabus covers it.** Its recurrence is the same $2a_{n/2}+cn$ already solved in §4.
>
> **No error was found in Johnsonbaugh ch. 7.** Seven chapters in, the errata table in `00-Index.md` remains empty.
>
> **Additions beyond the source.** The **five-row table of recurrence shapes** in §4 is mine, as is the **$2a_{n/2}+cn$ versus $2a_{n-1}+c$ comparison** and the recursion-tree explanation in Exercise 5(d) — Johnsonbaugh solves each recurrence individually and never contrasts them structurally, yet that contrast is the chapter's most transferable idea. The **general first-order formula** $a_n=r^na_0+c\frac{r^n-1}{r-1}$ is stated here explicitly rather than rediscovered per example. The explanation in Exercise 4(b) of **why the repeated-root case needs the factor $n$** (one parameter cannot meet two conditions), and the parallel with linear differential equations, are mine. **Exercise 1(b) and its observation that Fibonacci counts binary strings without consecutive zeros** is my own addition. The **explicit numerical comparison at $n=2^{20}$** (a factor of 28,000, a week versus twenty seconds) is mine. The **closing of the sorting question** — that merge sort's $O(n\lg n)$ plus ch. 09's $\Omega(n\lg n)$ settles it, and that the bound holds only in the comparison model — is assembled by me across three chapters. Important Note 10 (**Binet's formula is numerically treacherous**) and Note 11 (algorithm recurrence versus cost recurrence) are additions, as is the closing remark that generating functions and the Master Theorem extend the methods here.

**Previous:** [[06 - Counting Methods and the Pigeonhole Principle]] · **Next:** [[08 - Graph Theory]]
