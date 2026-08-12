---
subject: Discrete Mathematics
chapter: 4
tags: [ds, discrete-mathematics, algorithms, big-o, complexity, asymptotics, recursion, insertion-sort, binary-search]
source: "Johnsonbaugh, *Discrete Mathematics* 8e, ch. 4 (book pp. 173–213)"
---

# Algorithms and Their Analysis

This chapter answers a question every previous one has been circling: **how long does it take?**

It also collects three promises made earlier. [[01 - Sets and Logic|Ch. 01]] §6 claimed that **big-O is itself a nested-quantifier statement** and that getting the quantifier order wrong changes the theorem — §3 below makes that precise. [[02 - Proofs and Mathematical Induction|Ch. 02]] argued that induction and recursion are one idea seen from two directions — §5 cashes that in, using induction to prove a recursive algorithm correct. And [[03 - Functions, Sequences and Relations|Ch. 03]] supplied the floor function, `mod`, and sequences, all of which are the vocabulary of algorithm analysis.

> [!note] Where this chapter stops, and why
> This subject owns the **mathematics** of complexity: the definitions of $O$, $\Omega$, $\Theta$, and how to prove bounds. [[Data Structures and Algorithms/contents/00-Index|Data Structures and Algorithms]] owns the **implementations** — adjacency lists, balanced trees, hash-table internals, and production code. So insertion sort appears here as a *counting problem* and there as *code*. The split is recorded in both indexes.

## 📘 Main Knowledge

### 1. What an algorithm is

An **algorithm** is a step-by-step method for solving a problem. Johnsonbaugh lists the properties one is normally expected to have:

- **Input** — it receives data.
- **Output** — it produces a result.
- **Precision** — the steps are stated exactly, with no ambiguity.
- **Determinism** — the intermediate results are determined by the input and the steps so far.
- **Finiteness** — it terminates after finitely many steps.
- **Correctness** — the output is right.
- **Generality** — it applies to a class of inputs, not one instance.

**Finiteness and correctness are the two that need proving**, and they are usually proved by the induction of [[02 - Proofs and Mathematical Induction|ch. 02]] — a loop invariant for termination and correctness together (§2.4 there), or the recursive argument of §5 below.

A **trace** is a hand-simulation of an algorithm on specific input. It is not a proof of anything, but it is how you find out what an algorithm actually does, and it is worth doing before attempting an analysis.

### 2. Three algorithms worth knowing

Johnsonbaugh presents these before any analysis, so there is something concrete to analyse.

**Finding a maximum** (Algorithm 4.1.2). Walk the sequence keeping the largest value seen:

```python
def find_max(s):
    largest = s[0]
    for i in range(1, len(s)):
        if s[i] > largest:
            largest = s[i]
    return largest
```

**This makes exactly $n-1$ comparisons on every input of size $n$** — no best case, no worst case, they coincide. That is unusual and it makes the algorithm a clean first example.

**Text search** (Algorithm 4.2.1). To find a pattern $p$ of length $m$ inside text $t$ of length $n$, try every starting position and compare character by character:

```python
def text_search(t, p):
    n, m = len(t), len(p)
    for i in range(n - m + 1):
        j = 0
        while j < m and t[i + j] == p[j]:
            j += 1
        if j == m:
            return i          # found at position i
    return -1
```

**Best case $O(m)$** (match immediately), **worst case $O(mn)$** — e.g. $t=aaaa\dots a$ and $p=aa\dots ab$, where every position matches $m-1$ characters then fails. This naive method is what Knuth–Morris–Pratt and Boyer–Moore improve on, and it is the reason `str.find` in a real language is not this loop.

**Insertion sort** (Algorithm 4.2.3). Take each element in turn and insert it into the sorted prefix to its left:

```python
def insertion_sort(a):
    for i in range(1, len(a)):
        val = a[i]
        j = i - 1
        while j >= 0 and a[j] > val:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = val
    return a
```

Johnsonbaugh's remark is worth keeping: **insertion sort is among the fastest algorithms for sorting small sequences** (say under 50 elements), despite its quadratic worst case. That is not a paradox — asymptotic notation deliberately discards the constant factors, and for small $n$ the constants are what matter. Real library sorts (Timsort, introsort) switch to insertion sort below a threshold for exactly this reason. Exercise 3 counts its comparisons exactly.

### 3. Big-O, Omega and Theta

We rarely care about the exact time; we care how it **grows**. Johnsonbaugh's motivation is precise: if $t(n)$ is the worst-case time in seconds then $t(n)/60$ is the time in minutes, and **changing units does not change how the time grows** — only the constant. So the right notion must be blind to constant factors.

> [!note] Definition (Johnsonbaugh 4.3.2)
> Let $f,g$ have domain $\{1,2,3,\dots\}$.
>
> - $f(n)=O(g(n))$ — "$f$ is **big oh** of $g$", of order **at most** $g$ — if there is a positive constant $C_1$ with
> $$|f(n)|\le C_1|g(n)|\quad\text{for all but finitely many positive integers }n.$$
> - $f(n)=\Omega(g(n))$ — "**omega**", of order **at least** $g$ — if there is a positive constant $C_2$ with
> $$|f(n)|\ge C_2|g(n)|\quad\text{for all but finitely many }n.$$
> - $f(n)=\Theta(g(n))$ — "**theta**", of order $g$ — if **both** hold.

Loosely: **except for a constant factor and finitely many exceptions**, $g$ bounds $f$ above ($O$), below ($\Omega$), or both ($\Theta$). The three are called an **asymptotic upper bound**, **lower bound**, and **tight bound**.

> [!note] "For all but finitely many $n$" = "for all $n\ge n_0$"
> Johnsonbaugh's phrasing and the more common "there exists $n_0$ such that for all $n\ge n_0$" are equivalent: finitely many exceptions have a largest one, and beyond it the inequality holds. Use whichever you find easier to write; the second is easier to *use* in a proof, because it names the threshold.

**Now the promise from [[01 - Sets and Logic|ch. 01]] §6.** Unpack the definition into quantifiers:

$$f(n)=O(g(n))\quad\Longleftrightarrow\quad \exists C_1>0\ \ \exists n_0\ \ \forall n\ge n_0\ :\ |f(n)|\le C_1|g(n)|.$$

**The order $\exists C\,\forall n$ is the whole content of the definition.** One constant must work for *all* large $n$ — it may not depend on $n$. Reverse the quantifiers to $\forall n\,\exists C$ and the statement becomes vacuous: for any two functions and any single $n$ you can always find a big enough $C$, so *every* $f$ would be $O(g)$ for every $g$. **This is exactly the $\forall x\exists y$ versus $\exists y\forall x$ distinction of chapter 01, and here it is the difference between a useful definition and an empty one.**

> [!warning] "=" in $f(n)=O(g(n))$ is an abuse of notation
> It is **not** an equality and **not** symmetric. $O(g(n))$ is really a *set of functions*, and the honest notation is $f\in O(g)$. Consequences:
> - You may write $f(n)=O(g(n))$ but **never** $O(g(n))=f(n)$.
> - From $f_1=O(g)$ and $f_2=O(g)$ you may **not** conclude $f_1=f_2$. Both $n$ and $n^2$ are $O(n^2)$.
> - $f=O(g)$ says $g$ grows **at least** as fast as $f$ — it does not say they grow alike. $n=O(2^n)$ is true and enormously loose. **Only $\Theta$ claims matching growth**, which is why $\Theta$ is the notation to reach for when you know the answer.

**The essential facts**, all verified computationally:

| Result | Statement | Note |
|---|---|---|
| **Polynomials** | $p(n)=a_kn^k+\cdots+a_0$ with $a_k>0$ has $p(n)=\Theta(n^k)$ | only the leading term matters |
| **Logs: base is irrelevant** | $\log_b n=\Theta(\log_a n)$ for any $a,b>1$ | so one writes $\lg n$, or just $\log n$ |
| **Sums of powers** | $1^k+2^k+\cdots+n^k=\Theta(n^{k+1})$ | $k=1$ gives $\Theta(n^2)$ |
| **Log of factorial** | $\lg(n!)=\Theta(n\lg n)$ | the comparison-sorting bound, [[09 - Trees\|ch. 09]] |
| **$\Theta$ is transitive** | $f=\Theta(g)$ and $g=\Theta(h)$ $\Rightarrow$ $f=\Theta(h)$ | likewise $O$ and $\Omega$ |

*(Verified: $\log_{10}n/\lg n=0.30103$ for every $n$ tested — a constant, which is the whole content of the change-of-base formula $\log_b n=\log_b a\cdot\log_a n$. And $\sum_{i\le n}i^k/n^{k+1}\to\frac1{k+1}$, e.g. $0.2505$ for $k=3,n=1000$ against $\tfrac14$.)*

> [!note] Why the base of a logarithm never matters, but the base of an exponent always does
> $\log_2 n$ and $\log_{10}n$ differ by the **constant** factor $\log_2 10$, so they are $\Theta$ of each other. But $2^n$ and $10^n$ differ by the factor $(10/2)^n=5^n$, which is **not** constant — so $2^n\ne\Theta(10^n)$. **Constants inside a logarithm are free; constants inside an exponent are not.** This asymmetry catches people out, and it is why "exponential time" needs its base stated when the base matters.

**Applying it to algorithms** (Definition 4.3.11): if an algorithm takes $t(n)$ time in the worst case and $t(n)=O(g(n))$, we say the **worst-case time is $O(g(n))$** — and analogously for best case, average case, and for $\Omega$ and $\Theta$.

> [!warning] "Best/worst/average case" and "$O/\Omega/\Theta$" are independent axes
> They are constantly conflated. The case is **which input** you consider; the asymptotic notation is **how tightly you bound** the resulting function. So all of these are meaningful and different:
> - the **worst**-case time is $O(n^2)$ — an upper bound on the worst input;
> - the **worst**-case time is $\Omega(n^2)$ — the worst input really is that bad;
> - the **best**-case time is $\Theta(n)$ — the easiest input takes linear time exactly.
>
> **"Big-O is the worst case" is a common and wrong shorthand.** You can perfectly well give an $\Omega$ bound on the best case. Say which case *and* which bound.

### 4. Growth rates in practice

The standard hierarchy, each strictly slower-growing than the next:

$$1\ \prec\ \lg\lg n\ \prec\ \lg n\ \prec\ \sqrt n\ \prec\ n\ \prec\ n\lg n\ \prec\ n^2\ \prec\ n^3\ \prec\ 2^n\ \prec\ n!$$

At $n=2^{20}\approx10^6$ *(verified)*:

| $f(n)$ | value |
|---|---|
| $\lg\lg n$ | $4.3$ |
| $\lg n$ | $20$ |
| $\sqrt n$ | $1{,}024$ |
| $n$ | $1.05\times10^6$ |
| $n\lg n$ | $2.10\times10^7$ |
| $n^2$ | $1.10\times10^{12}$ |

**The gap between $n\lg n$ and $n^2$ is the one that decides whether a program finishes.** At a million records, $n\lg n$ is twenty million operations — instant. $n^2$ is a trillion — hours. This is precisely why sorting is done in $n\lg n$ and why the $\Omega(n\lg n)$ lower bound of [[09 - Trees|ch. 09]] is worth proving: it says you cannot do better by comparisons, so the effort is settled.

And the reason $2^n$ and $n!$ are called *intractable*: at $n=100$, $2^{100}\approx10^{30}$ operations exceeds anything physically achievable. **Algorithms with exponential worst cases are not merely slow, they are unusable at scale** — which is the standing motivation for the approximation and relaxation ideas in [[Optimization/contents/12 - Convex Programming and Constrained Algorithms|Optimization ch. 12]].

### 5. Recursive algorithms

A **recursive** function invokes itself. The technique is **divide and conquer**: decompose a problem into smaller problems *of the same type*, until the pieces are trivial, then combine.

Johnsonbaugh's introductory example is the factorial, whose recursive structure comes from one identity:

$$n!=n\cdot(n-1)!\qquad(\text{true even at }n=1).$$

```python
def factorial(n):
    if n == 0:          # base case
        return 1
    return n * factorial(n - 1)
```

Computing $5!$ reduces to $4!$, which reduces to $3!$, down to the base case $0!=1$; then the answers combine upward $1,1,2,6,24,120$.

> [!warning] Every recursion needs a base case that is actually reached
> Two failure modes: no base case at all, and a base case the recursion steps past. `factorial(-1)` on the code above recurses forever, because $n$ decreases away from $0$. **The base case must be reachable from every legal input** — and "legal input" is part of the specification, which is why the algorithm's stated input is $n\ge0$.

**Correctness is proved by induction, and the structure matches exactly.** To show `factorial(n)` returns $n!$ for all $n\ge0$:

- **Basis ($n=0$):** the function returns $1=0!$ ✓
- **Inductive step:** assume the call `factorial(n-1)` returns $(n-1)!$. For $n\ge1$ the function returns $n\cdot(n-1)!=n!$ ✓

**The base case of the recursion is the basis step of the induction; the recursive call is the inductive hypothesis.** That correspondence is not a coincidence or an analogy — it is why [[02 - Proofs and Mathematical Induction|ch. 02]] and this chapter are the same material. Recursions that reduce to $\lfloor n/2\rfloor$ rather than $n-1$ need the **strong** form (ch. 02 §7), which is the situation in Exercise 5.

> [!note] Recursion gives the algorithm; recurrences give the running time
> The recursive structure translates directly into an equation for the cost. For factorial, one call does constant work plus one call on $n-1$:
> $$T(n)=T(n-1)+c,\qquad T(0)=c,$$
> which unwinds to $T(n)=\Theta(n)$. For a divide-and-conquer method splitting in half:
> $$T(n)=T(n/2)+c\ \Rightarrow\ \Theta(\lg n),\qquad T(n)=2T(n/2)+cn\ \Rightarrow\ \Theta(n\lg n).$$
> **Solving such equations in general is [[07 - Recurrence Relations|ch. 07]]**, and the second is mergesort. Note that **induction verifies a solution you already have; it cannot find one** — which is exactly the gap ch. 07 fills.

## ✏️ Exercises

**1. (Bounds from the definition.)** Let $f(n)=3n^2+10n+7$. (a) Prove $f(n)=O(n^2)$ by exhibiting an explicit constant $C_1$ and threshold. (b) Prove $f(n)=\Omega(n^2)$. (c) Conclude a $\Theta$ statement. (d) Is $f(n)=O(n^3)$ true? Is it useful?

> [!example]- Solution
> **(a)** For $n\ge1$ we have $n\le n^2$ and $1\le n^2$, so
> $$3n^2+10n+7\ \le\ 3n^2+10n^2+7n^2\ =\ 20n^2.$$
> Take $C_1=20$ and $n_0=1$. *(Verified for all $n<10^4$; at $n=1$ it is tight, $f(1)=20=20\cdot1^2$.)* Hence $f(n)=O(n^2)$ ✓
>
> **The move worth remembering:** to bound a polynomial above, **replace every lower-order term by the leading power** — legitimate for $n\ge1$ — and add the coefficients.
>
> **(b)** All terms are positive, so for $n\ge1$
> $$3n^2+10n+7\ \ge\ 3n^2 .$$
> Take $C_2=3$, $n_0=1$ ✓ *(verified)*. Hence $f(n)=\Omega(n^2)$.
>
> **(c)** Both bounds hold, so **$f(n)=\Theta(n^2)$** — with the constants $3$ and $20$ sandwiching it: $3n^2\le f(n)\le20n^2$ for all $n\ge1$.
>
> **(d) True but useless.** $f(n)\le20n^2\le20n^3$ for $n\ge1$, so $f(n)=O(n^3)$ ✓ It is a correct *upper* bound and a badly loose one, because $f(n)\ne\Omega(n^3)$ — the ratio $f(n)/n^3\to0$.
>
> **This is the point of $\Theta$.** $O$ alone permits arbitrary overstatement: $f(n)=O(n^{100})$ and $f(n)=O(2^n)$ are also true. **When you know the growth rate, state $\Theta$**; reserve $O$ for when you genuinely only have an upper bound, and say so.

**2. (The quantifier structure.)** (a) Write "$f(n)=O(g(n))$" using explicit quantifiers. (b) Explain why reversing the two quantifiers makes the definition trivial. (c) Show by counterexample that $f=O(g)$ does not imply $g=O(f)$. (d) Explain what is wrong with writing $O(n)=f(n)$.

> [!example]- Solution
> **(a)**
> $$f(n)=O(g(n))\ \iff\ \exists C>0\ \ \exists n_0\in\mathbb Z^+\ \ \forall n\ge n_0\ :\ |f(n)|\le C\,|g(n)|.$$
> The order matters absolutely: **$C$ and $n_0$ are chosen first and must then work for every $n\ge n_0$.** $C$ may depend on $f$ and $g$ but **not on $n$**.
>
> **(b)** Reverse to $\forall n\,\exists C$:
> $$\forall n\ \ \exists C>0\ :\ |f(n)|\le C|g(n)|.$$
> Now $C$ may be chosen *after* seeing $n$, so take $C=|f(n)|/|g(n)|+1$ for that particular $n$. **The statement then holds for every pair of functions** (with $g(n)\ne0$), and so says nothing whatever. $2^n$ would be $O(1)$.
>
> This is [[01 - Sets and Logic|ch. 01]] §6 exactly: $\exists C\forall n$ demands **one witness that works uniformly**, while $\forall n\exists C$ lets the witness depend on $n$. **The uniformity is the entire content of asymptotic notation** — it is what makes "grows no faster than" mean something.
>
> **(c)** Take $f(n)=n$ and $g(n)=n^2$. Then $f=O(g)$: $n\le1\cdot n^2$ for $n\ge1$ ✓ But $g\ne O(f)$: if $n^2\le Cn$ for all $n\ge n_0$ then $n\le C$ for all large $n$, which is false for $n>C$. **So $O$ is not symmetric** — it is a one-directional comparison, which is why it reads "at most".
>
> **(d)** $O(n)$ denotes a **set of functions** — all those bounded above by a constant multiple of $n$. The honest statement is $f\in O(n)$, and the traditional $f(n)=O(n)$ is a long-standing abuse of notation kept for convenience. So:
> - $f(n)=O(n)$ is acceptable shorthand for $f\in O(n)$;
> - **$O(n)=f(n)$ is meaningless** — it reads "this set equals this function";
> - and the "$=$" is **not transitive in both directions**: $n=O(n^2)$ and $n^2=O(n^2)$, but $n\ne n^2$.
>
> Treat the notation as a **one-way claim**, always with $O$ on the right.

**3. (Insertion sort, counted exactly.)** For insertion sort on a sequence of $n$ distinct elements, counting comparisons of sequence elements: (a) find the best-case count and the input achieving it; (b) find the worst-case count and its input; (c) give $\Theta$ statements for each; (d) reconcile the quadratic worst case with Johnsonbaugh's remark that insertion sort is among the fastest methods for small sequences.

> [!example]- Solution
> **(a) Best case: $n-1$ comparisons**, achieved by an **already sorted** input. For each $i$ from $1$ to $n-1$ the inner `while` makes one comparison, finds `a[j] > val` false immediately, and stops. That is one comparison per outer pass, so $n-1$ total. *(Verified: sorted input of size 8 gives exactly 7.)*
>
> **(b) Worst case: $\dfrac{n(n-1)}2$ comparisons**, achieved by a **reverse-sorted** input. Then pass $i$ must shift every one of the $i$ elements to its left, making $i$ comparisons, so the total is
> $$\sum_{i=1}^{n-1}i=\frac{n(n-1)}2 .$$
> *(Verified: reversed input gives $10$, $28$, $66$ comparisons at $n=5,8,12$, matching $n(n-1)/2$ exactly.)*
>
> Note the sum is [[02 - Proofs and Mathematical Induction|ch. 02]]'s first induction, reappearing as a cost.
>
> **(c)** Best-case time $\Theta(n)$; worst-case time $\Theta(n^2)$, since $\frac{n(n-1)}2=\frac{n^2-n}2$ is a degree-2 polynomial with positive leading coefficient (§3's polynomial rule). The average case is also $\Theta(n^2)$ — about half the worst-case shifts.
>
> **(d) No contradiction — asymptotic notation deliberately discards exactly the information that decides small cases.** Three reasons insertion sort wins on small inputs:
> 1. **Its constant factor is tiny.** The inner loop is a comparison and a move on contiguous memory; mergesort allocates and copies, quicksort computes pivots and recurses. The hidden constant in $\Theta(n\lg n)$ can exceed the one in $\Theta(n^2)$ until $n$ is a few dozen.
> 2. **$n^2$ beats $n\lg n$ for small $n$ once constants are included.** With $c_1n^2$ and $c_2n\lg n$, the crossover is at $n\approx(c_2/c_1)\lg n$ — a threshold, not a universal fact.
> 3. **It is adaptive:** on nearly sorted data it approaches its $\Theta(n)$ best case, which mergesort and quicksort do not.
>
> **This is why real library sorts are hybrids.** Timsort (Python's `sorted`) and introsort (C++ `std::sort`) run insertion sort below a size threshold and switch above it. **The lesson: $\Theta$ tells you what happens eventually, and "eventually" may be past the input sizes you care about.** Always ask what $n$ actually is.

**4. (Growth rates.)** (a) Order these by growth rate, slowest first: $n^2$, $\lg n$, $n!$, $n\lg n$, $2^n$, $\sqrt n$, $n$, $\lg\lg n$. (b) Evaluate each at $n=2^{20}$ where feasible. (c) Which of $\log_2 n=\Theta(\log_{10}n)$ and $2^n=\Theta(10^n)$ is true, and why does the difference arise? (d) A program handles $n=10^4$ in one second with a $\Theta(n^2)$ algorithm. Roughly how long for $n=10^6$? What if the algorithm were $\Theta(n\lg n)$?

> [!example]- Solution
> **(a)**
> $$\lg\lg n\ \prec\ \lg n\ \prec\ \sqrt n\ \prec\ n\ \prec\ n\lg n\ \prec\ n^2\ \prec\ 2^n\ \prec\ n!$$
>
> **(b)** At $n=2^{20}=1{,}048{,}576$ *(verified)*:
>
> | $f(n)$ | value |
> |---|---|
> | $\lg\lg n$ | $4.32$ |
> | $\lg n$ | $20$ |
> | $\sqrt n$ | $1{,}024$ |
> | $n$ | $1.05\times10^6$ |
> | $n\lg n$ | $2.10\times10^7$ |
> | $n^2$ | $1.10\times10^{12}$ |
> | $2^n$, $n!$ | astronomically large — not representable |
>
> **(c) $\log_2 n=\Theta(\log_{10}n)$ is TRUE; $2^n=\Theta(10^n)$ is FALSE.**
>
> By change of base, $\log_{10}n=\log_{10}2\cdot\log_2 n$, and $\log_{10}2=0.30103$ is a **constant** — verified identical at $n=2,10,10^3,10^6$. Constant factors are exactly what $\Theta$ ignores, so the logarithm's base is irrelevant and one simply writes $\lg n$.
>
> But $\dfrac{10^n}{2^n}=5^n$, which **grows without bound**. So no constant $C$ satisfies $10^n\le C\cdot2^n$ for all large $n$, and $10^n\ne O(2^n)$.
>
> **The asymmetry:** changing a logarithm's base multiplies by a constant; changing an exponent's base raises to a power. **Constants inside a log are free; constants inside an exponent are not.**
>
> **(d)** For $\Theta(n^2)$, time scales as $n^2$. Going from $10^4$ to $10^6$ multiplies $n$ by $100$, so time by $100^2=10^4$:
> $$1\text{ second}\ \longrightarrow\ 10^4\text{ seconds}\approx\mathbf{2.8\text{ hours}}.$$
> For $\Theta(n\lg n)$, the factor is
> $$\frac{10^6\lg10^6}{10^4\lg10^4}=100\cdot\frac{19.93}{13.29}\approx150,$$
> so $1$ second becomes about **2.5 minutes**.
>
> **Hours versus minutes, from the same input on the same machine.** This is why the asymptotic class matters far more than micro-optimisation: no amount of tuning a $\Theta(n^2)$ constant closes a $10^4$-fold gap, and buying a machine 10× faster still leaves you 15 minutes behind.

**5. (Hard — recursion, correctness, and a recurrence.)** Consider binary search on a sorted array of $n$ distinct elements. (a) Write it recursively. (b) Prove correctness by induction, saying which form of induction you need. (c) Show the worst-case comparison count is $\lfloor\lg n\rfloor+1$. (d) Set up and solve the recurrence for the running time. (e) Why does the $\Omega(n\lg n)$ sorting bound not contradict binary search being $\Theta(\lg n)$?

> [!example]- Solution
> **(a)**
> ```python
> def bsearch(a, key, lo, hi):
>     if lo > hi:                     # base case: empty range
>         return -1
>     mid = (lo + hi) // 2            # floor division - ch. 03
>     if a[mid] == key:
>         return mid
>     if a[mid] < key:
>         return bsearch(a, key, mid + 1, hi)
>     return bsearch(a, key, lo, mid - 1)
> ```
>
> **(b)** Induct on the range size $k=hi-lo+1$.
>
> - **Basis ($k=0$):** then `lo > hi`, the range is empty, the key is absent, and $-1$ is correct ✓
> - **Inductive step:** let $k\ge1$ and assume the algorithm is correct on every range of size $<k$. Since `a` is sorted: if `a[mid] == key` we return a correct index; if `a[mid] < key` then by sortedness the key, if present, lies strictly right of `mid`, and the recursive call is on a range of size $\le k-1<k$, correct by hypothesis; symmetrically for `a[mid] > key` ✓
>
> **This needs the STRONG form of induction** ([[02 - Proofs and Mathematical Induction|ch. 02]] §7). The recursive call is on a range of size roughly $k/2$, not $k-1$, so the ordinary form — whose hypothesis is only the immediate predecessor — does not apply. The strong form's hypothesis covers *everything* below $k$, so halving is free. **This is the standard situation for divide-and-conquer, and it is why ch. 02 spent time on the strong form.**
>
> **(c)** Each call makes one comparison against `a[mid]` and at worst halves the range: sizes go $n\to\lfloor n/2\rfloor\to\lfloor n/4\rfloor\to\cdots\to0$. The number of halvings needed to reduce $n$ to $0$ is $\lfloor\lg n\rfloor+1$.
>
> *(Verified exhaustively along the worst-case path:)*
>
> | $n$ | 1 | 2 | 3 | 4 | 7 | 8 | 15 | 16 | 100 | 1000 |
> |---|---|---|---|---|---|---|---|---|---|---|
> | comparisons | 1 | 2 | 2 | 3 | 3 | 4 | 4 | 5 | 7 | 10 |
> | $\lfloor\lg n\rfloor+1$ | 1 | 2 | 2 | 3 | 3 | 4 | 4 | 5 | 7 | 10 |
>
> Matching at every value. Note the count increases only at powers of $2$ — **doubling the array costs one extra comparison**, which is the practical meaning of logarithmic time.
>
> **(d)** One comparison plus one recursive call on half the input:
> $$T(n)=T\!\left(\lfloor n/2\rfloor\right)+c,\qquad T(0)=c.$$
> Unwinding: after $k$ steps the argument is about $n/2^k$, and the base case is reached when $2^k\approx n$, i.e. $k\approx\lg n$. Each step costs $c$, so
> $$T(n)=\Theta(\lg n).$$
> *(Solving such recurrences systematically — rather than by unwinding and guessing — is [[07 - Recurrence Relations|ch. 07]].)*
>
> **(e) No contradiction: they are bounds on different problems.**
>
> - The $\Omega(n\lg n)$ bound ([[09 - Trees|ch. 09]]) is about **sorting** — putting $n$ elements in order, which requires distinguishing $n!$ possible permutations. Since $\lg(n!)=\Theta(n\lg n)$ (§3), and each comparison yields one bit, at least $\Theta(n\lg n)$ comparisons are needed.
> - Binary search **solves a different problem**: locating one key in an array **that is already sorted**. It must distinguish only $n+1$ outcomes ($n$ positions plus "absent"), needing about $\lg n$ bits.
>
> **The sortedness is a precondition, and it was paid for elsewhere.** Sorting once at $\Theta(n\lg n)$ and then searching $m$ times at $\Theta(\lg n)$ costs $\Theta(n\lg n+m\lg n)$, versus $\Theta(mn)$ for $m$ linear scans — which is why databases build indexes. **A lower bound always attaches to a problem plus a model of computation, never to an algorithm**; changing either can change it (hashing beats $\lg n$ by abandoning comparisons, and [[03 - Functions, Sequences and Relations|ch. 03]] §2 explains what it pays instead).

## 📝 Summary

- An **algorithm** should have input, output, precision, determinism, **finiteness** and **correctness**, and generality. The last two need *proof* — usually by induction or a loop invariant ([[02 - Proofs and Mathematical Induction|ch. 02]]). A **trace** explores behaviour but proves nothing.
- **Three reference algorithms:** finding a maximum ($n-1$ comparisons always — best and worst coincide); naive text search ($O(m)$ best, $O(mn)$ worst); insertion sort.
- **Asymptotic notation exists to be blind to constant factors** — because changing seconds to minutes must not change the answer.
- **$f(n)=O(g(n))$** iff $\exists C>0\,\exists n_0\,\forall n\ge n_0:|f(n)|\le C|g(n)|$ — upper bound. **$\Omega$** reverses the inequality — lower bound. **$\Theta$** is both — tight bound. Johnsonbaugh's "for all but finitely many $n$" is the same as "for all $n\ge n_0$".
- **The quantifier order $\exists C\,\forall n$ is the whole definition.** One constant must serve all large $n$; reversing to $\forall n\,\exists C$ makes every function $O$ of every other. This is [[01 - Sets and Logic|ch. 01]] §6's point, and it is load-bearing.
- **"$=$" in $f=O(g)$ is an abuse of notation** for $f\in O(g)$. Never write $O(g)=f$; never conclude $f_1=f_2$ from both being $O(g)$; and remember **$O$ is not symmetric** — $n=O(2^n)$ is true and useless.
- **Key facts:** a degree-$k$ polynomial is $\Theta(n^k)$; **the base of a logarithm is irrelevant** ($\log_b n=\Theta(\log_a n)$) **but the base of an exponent is not** ($2^n\ne\Theta(10^n)$); $\sum_{i\le n}i^k=\Theta(n^{k+1})$; and $\lg(n!)=\Theta(n\lg n)$.
- **"Case" and "bound" are independent axes.** Best/worst/average says *which input*; $O/\Omega/\Theta$ says *how tight the bound*. "Big-O means worst case" is wrong.
- **The hierarchy:** $\lg\lg n\prec\lg n\prec\sqrt n\prec n\prec n\lg n\prec n^2\prec2^n\prec n!$. The **$n\lg n$ versus $n^2$** gap decides whether a program finishes: at $n=10^6$, hours versus minutes.
- **Recursion = divide and conquer**, and it needs a **base case reachable from every legal input**.
- **Correctness of a recursive algorithm is an induction whose basis is the base case and whose hypothesis is the recursive call.** Reductions to $n-1$ use ordinary induction; reductions to $\lfloor n/2\rfloor$ need the **strong** form.
- **The recursion gives the algorithm; a recurrence gives the cost.** $T(n)=T(n-1)+c\Rightarrow\Theta(n)$; $T(n)=T(n/2)+c\Rightarrow\Theta(\lg n)$; $T(n)=2T(n/2)+cn\Rightarrow\Theta(n\lg n)$. **Solving these in general is [[07 - Recurrence Relations|ch. 07]]** — induction can verify a closed form but cannot find one.

## ⚠️ Important Notes

1. **State the case and the bound separately.** "The algorithm is $O(n^2)$" is incomplete — worst case? average? Both are legitimate and different claims.
2. **Prefer $\Theta$ when you know the growth rate.** $O$ alone licenses arbitrary overstatement: $3n^2+10n+7$ is genuinely $O(n^{100})$.
3. **The constant may not depend on $n$.** If your "proof" produces a $C$ that grows with $n$, you have proved nothing — that is the reversed-quantifier trap of Exercise 2(b).
4. **Never write $O(g(n))=f(n)$.** The notation is one-directional because $O(g)$ is a set. Keep $O$ on the right.
5. **$f=O(g)$ does not imply $g=O(f)$.** $O$ compares in one direction only. If you need mutual comparability, that is $\Theta$.
6. **To bound a polynomial above, replace lower-order terms by the leading power** (valid for $n\ge1$) and add coefficients — $3n^2+10n+7\le20n^2$. Clean and always available.
7. **Logarithm bases are free; exponent bases are not.** $\log_2$ and $\log_{10}$ differ by a constant; $2^n$ and $10^n$ differ by $5^n$. Write $\lg n$ without apology, but never treat $2^n$ and $10^n$ as interchangeable.
8. **Asymptotics deliberately hide the constants, so they say nothing about small $n$.** Insertion sort really is the right choice below a few dozen elements, and real library sorts switch to it. **Ask what $n$ actually is before choosing on asymptotics alone.**
9. **A $\Theta$ improvement beats any constant-factor improvement at scale.** No tuning closes the $10^4$-fold gap of Exercise 4(d). Fix the algorithm before optimising the loop.
10. **Every recursion needs a reachable base case.** Missing it, or stepping past it, gives infinite recursion — and note that `factorial(-1)` fails not because the code is wrong but because the input is outside the specification.
11. **Match the induction to the recursion.** $n\to n-1$ takes ordinary induction; $n\to\lfloor n/2\rfloor$ takes the **strong form**, and reaching back $p$ places needs $p$ basis steps (ch. 02 §7). Using the wrong form leaves cases unproved.
12. **Induction verifies a closed form; it does not find one.** If you do not already have a candidate, you need ch. 07's methods, not a cleverer induction.
13. **A lower bound belongs to a *problem in a model*, not to an algorithm.** The $\Omega(n\lg n)$ sorting bound is about comparison-based sorting; hashing evades it by not comparing, and binary search does not contradict it because it solves a different problem on a precondition already paid for.
14. **Watch for the hidden cost of a precondition.** "Binary search is $\Theta(\lg n)$" is true and incomplete if the array had to be sorted first. Count the setup when it is not amortised over many queries.
15. **Time is not the only resource.** Recursive algorithms consume stack proportional to their depth — $\Theta(n)$ for the factorial above, $\Theta(\lg n)$ for binary search — so a deep recursion can exhaust memory even when its time is fine. Johnsonbaugh's analysis is time-only; real analysis is not.

> [!warning] Gaps in the source material
> **Extraction was good for prose, definitions and theorem statements.** Two new artefacts appear in this chapter and are easy to misread: **$\Omega$ extracts as `/Omega1` and $\Theta$ as `/Theta1`** (so Definition 4.3.2 arrives as `f(n) = /Omega1(g(n))`), and Johnsonbaugh writes $\lg n$ for $\log_2 n$ throughout — **stated once, easy to miss, and it changes every logarithmic figure by a factor of $\ln 2$ if taken as a natural log.** Both are recorded in `00-Index.md`.
>
> **All of the numbered Algorithm boxes extract as headings with empty bodies.** `Algorithm 4.1.1`, `4.1.2` (find maximum), `4.2.1` (text search), `4.2.3` (insertion sort) and `4.2.4` (shuffle) survive only as titles and input/output lines; **the only pseudocode that came through intact is Algorithm 4.4.2 (factorial)**, which is why it is the one quoted verbatim. **So the code in §2 is my own Python reconstruction from the surrounding prose and the book's traces**, not a transcription — and each was verified by running it: insertion sort was checked to produce exactly $n-1$ comparisons on sorted input and $n(n-1)/2$ on reversed input at $n=5,8,12$, matching the theory.
>
> **Displayed derivations inside the §4.3 examples are largely lost**, as in ch. 02. Examples 4.3.3, 4.3.7, 4.3.8, 4.3.9 and 4.3.10 and Theorem 4.3.4 arrive as statements with the algebra between them dropped. **Every asymptotic claim in §3 was therefore re-derived and verified computationally:** $\log_{10}n/\lg n=0.30103$ constant across four orders of magnitude; $\sum_{i\le n}i^k/n^{k+1}\to\frac1{k+1}$ (e.g. $0.2505$ at $k=3,n=1000$ against $0.25$); $\lg(n!)/(n\lg n)$ rising through $0.656,0.790,0.856,0.892$ at $n=10,10^2,10^3,10^4$ — bounded, consistent with $\Theta$ and with Stirling's $\lg n!\approx n\lg n-n/\ln2$; and the growth table at $n=2^{20}$. **No error was found in Johnsonbaugh ch. 4** — the errata table remains empty after four chapters.
>
> **All figures are images and are lost**, including Figure 4.2.1 (the trace of the text-search algorithm) and the insertion-sort trace figures. §2 describes the worst-case input patterns explicitly instead, which is what an analysis needs.
>
> **Additions beyond the source.** **§3's quantifier unpacking of big-O, and Exercise 2, are mine** — Johnsonbaugh gives the definition in prose ("for all but finitely many $n$") and never writes it with quantifiers or observes that reversing them trivialises it; the connection back to ch. 01 §6 is the point and it is my own. The **"$=$" is an abuse of notation** discussion, the **log-base versus exponent-base asymmetry**, and the warning that **case and bound are independent axes** are all additions. **Binary search does not appear in Johnsonbaugh ch. 4 at all** — Exercise 5 is my own construction, chosen because it is the cleanest illustration that divide-and-conquer needs *strong* induction; its part (e), reconciling $\Theta(\lg n)$ search with the $\Omega(n\lg n)$ sorting bound, is also mine and is the conceptual link forward to [[09 - Trees|ch. 09]]. The **recurrence-to-cost table** in §5 and the note that induction cannot *find* a closed form are additions pointing to [[07 - Recurrence Relations|ch. 07]]. Exercise 3(d)'s explanation of **why real library sorts are hybrids** (Timsort, introsort, adaptivity) extends a single remark in the book. Exercise 4(d)'s hours-versus-minutes calculation, the **stack-space** caveat in Important Note 15, and the observation that **a lower bound attaches to a problem in a model, not to an algorithm**, are mine.
>
> **Deliberately compressed.** Johnsonbaugh's §4.2 shuffle algorithm (Algorithm 4.2.4) is mentioned only in passing; it is a nice application of the pseudorandom numbers of [[03 - Functions, Sequences and Relations|ch. 03]] §2, but its correctness argument (that every permutation is equally likely) needs the counting of [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]] and is better placed there. The §4.3 "Problem-Solving Corner: Design and Analysis of an Algorithm" is a worked-example section whose content is distributed through §§3–4 and the exercises.

**Previous:** [[03 - Functions, Sequences and Relations]] · **Next:** [[05 - Number Theory and Cryptography]]
