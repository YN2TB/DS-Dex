---
subject: Discrete Mathematics
chapter: 3
tags: [ds, discrete-mathematics, functions, sequences, strings, relations, equivalence-relations, partial-orders, hashing]
source: "Johnsonbaugh, *Discrete Mathematics* 8e, ch. 3 (book pp. 111–172)"
---

# Functions, Sequences and Relations

[[01 - Sets and Logic|Chapter 01]] gave us sets and [[02 - Proofs and Mathematical Induction|ch. 02]] gave us proof. This chapter supplies the three structures that everything afterwards is built from — and the striking thing is that **all three are the same kind of object**: a set of ordered pairs. A function is a relation with a uniqueness condition; a sequence is a function whose domain is a set of integers; a relation is the general case with no conditions at all.

Two things make this chapter more than definitions. First, its applications are unusually concrete for a mathematics chapter — **check digits, hash tables and pseudorandom number generators** all appear, and all three are things a data scientist uses weekly. Second, it contains the chapter's one genuinely surprising theorem: **equivalence relations and partitions are two views of the same thing**, which is the conceptual bridge to [[06 - Counting Methods and the Pigeonhole Principle|counting]], to modular arithmetic in [[05 - Number Theory and Cryptography|ch. 05]], and to connected components in [[08 - Graph Theory|ch. 08]].

## 📘 Main Knowledge

### 1. Functions

> [!note] Definition
> Let $X$ and $Y$ be sets. A **function** $f$ from $X$ to $Y$ is a subset of $X\times Y$ such that **for each $x\in X$ there is exactly one $y\in Y$ with $(x,y)\in f$.**
>
> $X$ is the **domain**, $Y$ the **codomain**, and $\{y\in Y:(x,y)\in f\text{ for some }x\}$ — a subset of $Y$ — is the **range**.

Note what the definition *permits* and what it *forbids*. It permits reusing elements of $Y$ (two inputs may share an output) and permits elements of $Y$ receiving nothing. It forbids an $x$ with two outputs, and forbids an $x$ with none.

So $f=\{(1,a),(2,b),(3,a)\}$ **is** a function from $\{1,2,3\}$ to $\{a,b,c\}$ — its range is $\{a,b\}$, and $c$ is simply unused. But $\{(1,a),(2,b),(3,c),(1,b)\}$ is **not**, because $1$ is assigned twice.

> [!warning] A rule is not a function until you state the domain and codomain
> "$f(x)=x^2$" is an incomplete specification. With domain $\mathbb R$ and codomain $\mathbb R$ its range is $[0,\infty)$; with codomain $[0,\infty)$ the same rule becomes surjective; with domain $[0,\infty)$ it becomes injective. **The same rule gives different functions with different properties**, and the properties in §3 are the ones exam questions turn on. Always ask what the domain and codomain are.

**Two workhorse functions.** For $x$ an integer and $y$ a positive integer, $x\bmod y$ is the remainder when $x$ is divided by $y$ — well defined by the Quotient–Remainder Theorem of [[02 - Proofs and Mathematical Induction|ch. 02]] §8, which is exactly why that theorem mattered. And:

$$\lfloor x\rfloor=\text{the greatest integer}\le x \quad(\text{\textbf{floor}, ``round down''}),\qquad \lceil x\rceil=\text{the least integer}\ge x \quad(\text{\textbf{ceiling}, ``round up''}).$$

$$\lfloor8.3\rfloor=8,\quad\lceil9.1\rceil=10,\quad\lfloor-8.7\rfloor=-9,\quad\lceil-11.3\rceil=-11,\quad\lceil6\rceil=6.$$

**The negative cases are the ones to check.** Floor is not truncation: $\lfloor-8.7\rfloor=-9$, not $-8$. In Python, `math.floor(-8.7)` is $-9$ ✓ but `int(-8.7)` is $-8$ ✗ — a real bug source. Note also that $q=\lfloor n/d\rfloor$ *is* the quotient of the Quotient–Remainder Theorem, which is what ties the two functions together.

### 2. Three applications you already use

This section is Johnsonbaugh at his best: three genuinely practical constructions, all of which are just "a function into a small set".

> [!example]- (a) Check digits — the Luhn algorithm
> Append one extra digit to an identification number so that most typing errors become detectable. The **Luhn algorithm** (used by every credit-card number, and in the public domain):
>
> 1. From the **rightmost** digit leftwards, **double every second digit**.
> 2. If a doubled value exceeds 9, subtract 9 (equivalently, add its two digits).
> 3. Sum everything. **The number is valid iff the total is $\equiv0\pmod{10}$.**
>
> So the check digit $c$ for payload $7992739871$ is chosen to make the sum a multiple of 10; computing gives $c=\mathbf3$, and $79927398713$ has Luhn sum $70\equiv0$ ✓ *(all verified computationally; the test card number $4539148803436467$ also checks out, sum $80$).*
>
> **Why it is designed this way.** Verified exhaustively on $79927398713$: **every one of the possible single-digit alterations fails the check** (zero false passes out of all $11\times9$ of them), and **every adjacent transposition is caught too.** That is the whole point — the doubling step is what breaks the symmetry that would let $\dots ab\dots\to\dots ba\dots$ slip through. (The one family Luhn misses is transposing $0$ and $9$, since $0\to0$ and $9\to18\to9$ double to the same thing; $79927398713$ happens to contain no adjacent $09$ or $90$.)
>
> **This is error *detection*, not correction** — and it is the elementary ancestor of the coding theory that [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]]'s Hamming-distance arguments formalise.

> [!example]- (b) Hash functions
> Suppose memory cells are indexed $0$ to $n-1$ and you must store records with much larger keys. A **hash function** maps a key to a cell. The simplest is
> $$h(n)=n\bmod 11.$$
> Inserting $15,558,32,132,102,5$ gives cells $4,8,10,0,3,5$ respectively *(verified)* — six distinct cells, so this particular batch is lucky.
>
> A **collision** occurs when $h(k_1)=h(k_2)$ for $k_1\ne k_2$. It takes only one more key to produce one: $h(26)=4=h(15)$.
>
> **Collisions are not a defect but a certainty**, and here is the reason, which is [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]] arriving early: **a hash function maps an infinite (or merely larger) key space into a finite set of cells, so by the pigeonhole principle it cannot possibly be injective.** Every hash table therefore needs a collision policy — chaining, or probing to the next free cell. When it has one, hashing gives near-constant-time storage and retrieval, which is why employee records, Python `dict`s, database indexes and `git`'s object store all use it.

> [!example]- (c) Pseudorandom numbers
> Computers simulate randomness with a **linear congruential generator**: pick a modulus $m$, a multiplier $a$, an increment $c$ and a **seed** $x_0=s$, then
> $$x_n=(a\,x_{n-1}+c)\bmod m.$$
> Johnsonbaugh's small illustration uses $m=11$ and seed $3$. **The book's constants do not survive extraction, but they are recoverable from the fragments it does print** — the sequence begins $3,4,0,5$ and returns to $x_{10}=3$. Solving those three conditions gives a unique answer:
> $$\boxed{\ x_n=(7x_{n-1}+5)\bmod 11\ }$$
> and the full cycle is $3,4,0,5,7,10,9,2,8,6$ then back to $3$ — **period 10, hitting every residue except 1** *(recovered and verified computationally; see the gaps callout)*.
>
> **Three lessons.** (i) The output is *entirely determined* by the seed — "pseudo" is doing real work. This is why `random.seed(42)` makes an experiment reproducible, and why it must be set in any ML pipeline you intend to rerun. (ii) The sequence **must** eventually repeat, since there are only $m$ possible states — pigeonhole again — so the design goal is a long period. Real generators use $m=2^{31}-1$ or better. (iii) The choice of $a$ and $c$ is delicate: change $c$ to $0$ here and the value $0$ becomes an absorbing state.
>
> Johnsonbaugh's accompanying anecdote is worth keeping: a player worked out that a casino's electronic keno machine was **regenerating the same sequence**, and won a bet the officials had priced at 6 billion to 1. They initially refused to pay. **A predictable "random" generator is a security hole**, which is why cryptographic work requires a CSPRNG and never an LCG.

### 3. One-to-one, onto, and bijections

> [!note] Definitions
> $f:X\to Y$ is
> - **one-to-one** (**injective**) if $f(x_1)=f(x_2)$ implies $x_1=x_2$ — equivalently, each $y$ in the range comes from **exactly one** $x$;
> - **onto $Y$** (**surjective**) if the range equals the codomain $Y$ — i.e. for every $y\in Y$ there is some $x$ with $f(x)=y$;
> - a **bijection** (one-to-one correspondence) if both.

**Arrow-diagram reading:** injective means every element of $Y$ has **at most one** arrow in; surjective means every element has **at least one**; bijective means **exactly one**.

**How to prove each, and how to disprove it** — note the shapes, which are [[01 - Sets and Logic|ch. 01]] §5's $\forall/\exists$ asymmetry in practice:

| | to prove | to disprove |
|---|---|---|
| injective | assume $f(x_1)=f(x_2)$, derive $x_1=x_2$ | exhibit **one** pair $x_1\ne x_2$ with equal images |
| surjective | take arbitrary $y\in Y$, **construct** an $x$ with $f(x)=y$ | exhibit **one** $y$ hit by nothing |

So $f(n)=2n+1$ on $\mathbb Z^+$ is injective ($2n_1+1=2n_2+1\Rightarrow n_1=n_2$) but **not** onto $\mathbb Z^+$, since no $n$ gives $f(n)=2$. And $f(n)=2^n-n^2$ is not injective — $f(2)=0=f(4)$.

**Bijections matter more than the other two**, because a bijection is exactly a function with an **inverse** $f^{-1}$, and because — this is the idea [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]] runs on — **a bijection between two finite sets proves they have the same size.** Most counting arguments are secretly the construction of a bijection.

**Composition.** If $f:X\to Y$ and $g:Y\to Z$, then $(g\circ f)(x)=g(f(x))$ is a function $X\to Z$. Note the order: **$g\circ f$ applies $f$ first.** Composition of injections is an injection, of surjections a surjection, hence of bijections a bijection.

### 4. Sequences and strings

> [!note] Definition
> A **sequence** $s$ is a function whose domain is a set of integers. We write $s_n$ rather than $s(n)$.

That is all a sequence is — and it explains why sequences take order into account while sets do not: **the order is carried by the domain.** $2,4,6,\dots,2n,\dots$ is the sequence $s_n=2n$ on $\mathbb Z^+$; $a,a,b,a,b$ is a sequence with repeats, which a set could not have.

**Monotonicity.** For all $i<j$ in the domain:

| | condition |
|---|---|
| **increasing** | $s_i<s_j$ |
| **decreasing** | $s_i>s_j$ |
| **nondecreasing** | $s_i\le s_j$ |
| **nonincreasing** | $s_i\ge s_j$ |

> [!warning] "Increasing" means *strictly* increasing in this book
> Conventions differ between textbooks, and this one is explicit: increasing uses $<$, and the $\le$ version is called **nondecreasing**. So $100,90,90,74,74,74,30$ is nonincreasing but **not** decreasing, and $2,5,13,104,300$ is both increasing and nondecreasing (every increasing sequence is nondecreasing).
>
> A one-element sequence such as $100$ is **all four at once** — vacuously, since there are no distinct $i<j$ to test. That is [[01 - Sets and Logic|ch. 01]]'s vacuous truth again, and it is a favourite exam trap.

A **subsequence** of $s$ is obtained by selecting terms **while preserving order**: from $a,b,b,c$ the sequence $b,c$ is a subsequence but $c,b$ is not. Formally a subsequence is $s_{n_1},s_{n_2},\dots$ with $n_1<n_2<\cdots$ — so **the indices themselves form an increasing sequence.**

**Sum and product notation.** $\sum_{i=m}^n a_i$ and $\prod_{i=m}^n a_i$. Re-indexing (substituting $j=i+1$ and adjusting the limits) is a routine manipulation and the commonest source of off-by-one errors; the geometric sum of [[02 - Proofs and Mathematical Induction|ch. 02]] is usually written $\sum_{i=0}^n ar^i$.

**Strings.** A **string** over a finite set $X$ is a finite sequence of elements of $X$. The empty one is the **null string** $\lambda$; $X^*$ is all strings including $\lambda$, and $X^+$ all nonnull ones. Write $|\alpha|$ for the length, and $\alpha\beta$ for the **concatenation**. A **substring** of $\alpha$ is any $\beta$ with $\alpha=\gamma\beta\delta$ for some strings $\gamma,\delta$ — i.e. a *contiguous* block, unlike a subsequence.

> [!note] A nice non-injective function
> Concatenation $f(\alpha,\beta)=\alpha\beta$ from $X^*\times X^*$ to $X^*$ is **onto** (every string is $\alpha\lambda$) but **not one-to-one** — over $X=\{a,b\}$, the pairs $(a,ab)$ and $(aa,b)$ both give $aab$. **This is why you cannot recover a split from its result**, which is exactly the difficulty that tokenisation, CSV parsing without quoting, and ambiguous grammars all run into.

### 5. Relations

> [!note] Definition
> A **binary relation** $R$ from $X$ to $Y$ is **any** subset of $X\times Y$. We write $xRy$ for $(x,y)\in R$. A relation **on** $X$ is a relation from $X$ to $X$.

No conditions at all — which is why relations are more general than functions, and why they can model things functions cannot (a student taking *several* courses, a city connected to *several* cities).

A relation on $X$ is drawn as a **digraph**: vertices are the elements, and an edge $x\to y$ for each $(x,y)\in R$. A pair $(x,x)$ appears as a **loop**. **This is the first appearance of [[08 - Graph Theory|ch. 08]]: a relation on a finite set and a directed graph are the same object written two ways.**

**The four properties.** $R$ on $X$ is:

| Property | Definition | Digraph reading |
|---|---|---|
| **reflexive** | $(x,x)\in R$ for **every** $x\in X$ | a loop at every vertex |
| **symmetric** | $(x,y)\in R\Rightarrow(y,x)\in R$ | every edge is bidirectional |
| **antisymmetric** | $(x,y)\in R$ and $(y,x)\in R$ $\Rightarrow x=y$ | between distinct vertices, **at most one** direction |
| **transitive** | $(x,y),(y,z)\in R\Rightarrow(x,z)\in R$ | every 2-step path has a 1-step shortcut |

> [!warning] "Not symmetric" is **not** the same as "antisymmetric"
> This is the chapter's most reliable exam trap. The equivalent contrapositive form of antisymmetry is easier to apply: *for all $x\ne y$, not both $(x,y)$ and $(y,x)$ are in $R$.*
>
> Read that and you see the two are independent, not opposite:
> - $R=\{(a,a),(b,b),(c,c)\}$ is **both symmetric and antisymmetric** — it has no pairs with $x\ne y$ at all, so antisymmetry holds vacuously.
> - $R=\{(a,a),(b,c),(c,b),(d,d)\}$ is symmetric and **not** antisymmetric.
> - $\le$ on $\{1,2,3,4\}$ is antisymmetric and **not** symmetric.
>
> **A relation can be both, neither, or exactly one.** Never infer one from the failure of the other.

**Partial orders.** $R$ is a **partial order** if it is **reflexive, antisymmetric and transitive**. The canonical example is $\le$; the notation $x\preceq y$ is used generally. Elements $x,y$ are **comparable** if $x\preceq y$ or $y\preceq x$; **the word "partial" is there because some pairs may be incomparable.** For $\le$ on the integers every pair is comparable — a **total order** — but for "$x$ divides $y$" the pair $2,3$ is not.

**Application: task scheduling.** Let $T$ be a set of tasks with $t_1\preceq t_2$ meaning $t_1$ must be finished before $t_2$. This is a partial order, and the scheduling problem is to find a **total order consistent with it** — a *topological sort*. **That such an ordering always exists for a finite partial order is a real theorem**, and it is what `make`, a build system, a Spark DAG and a course-prerequisite checker all compute.

**Inverse and composition.** $R^{-1}=\{(y,x):(x,y)\in R\}$. If $R_1$ goes from $X$ to $Y$ and $R_2$ from $Y$ to $Z$, then
$$R_2\circ R_1=\{(x,z):(x,y)\in R_1\text{ and }(y,z)\in R_2\text{ for some }y\in Y\},$$
generalising composition of functions.

> [!example]- Which operations preserve transitivity? (J Example 3.3.27)
> Given transitive $R$ and $S$ on $X$, is each of $R\cup S$, $R\cap S$, $R\circ S$ transitive? The answers are **no, yes, no** — and the method is [[02 - Proofs and Mathematical Induction|ch. 02]] §3's advice: attempt the proof and let it fail informatively.
>
> - **$R\cap S$: yes.** If $(x,y),(y,z)\in R\cap S$ then both are in $R$, so $(x,z)\in R$ by transitivity of $R$; likewise $(x,z)\in S$. Hence $(x,z)\in R\cap S$. ✓ *(The proof goes through because both pairs land in the **same** relation.)*
> - **$R\cup S$: no.** The attempt fails exactly when one pair comes from $R$ and the other from $S$ — and that failure is the recipe. Take $R=\{(1,2)\}$ and $S=\{(2,3)\}$, both trivially transitive. Then $R\cup S=\{(1,2),(2,3)\}$ lacks $(1,3)$.
> - **$R\circ S$: no.** Take $R=\{(5,2),(6,3)\}$ and $S=\{(1,5),(2,6)\}$, both transitive. Then $R\circ S=\{(1,2),(2,3)\}$, which again lacks $(1,3)$.
>
> **Intersection preserves properties; union generally does not.** That pattern recurs — it is why "the smallest relation containing $R$ with property $P$" (a **closure**) is defined by intersecting, and why the transitive closure of Exercise 5 is well defined.

### 6. Equivalence relations *are* partitions

This is the chapter's main theorem, and it goes both ways.

> [!note] Definition
> A relation on $X$ that is **reflexive, symmetric and transitive** is an **equivalence relation**.

Compare a partial order: swap *antisymmetric* for *symmetric* and you get a completely different kind of object. Orders arrange elements; equivalences group them.

> [!note] Theorem (partition ⟹ equivalence relation)
> Let $\mathcal S$ be a partition of $X$. Define $xRy$ to mean *$x$ and $y$ belong to the same member of $\mathcal S$.* Then $R$ is an equivalence relation on $X$.

*Proof.* **Reflexive:** every $x$ lies in some $S\in\mathcal S$ (definition of partition), so $xRx$. **Symmetric:** "same member" is symmetric in $x$ and $y$. **Transitive:** if $x,y\in S$ and $y,z\in S'$ then $S$ and $S'$ both contain $y$, and since partition members are disjoint, $S=S'$; so $x,z\in S$. $\blacksquare$

> [!note] Theorem (equivalence relation ⟹ partition)
> Let $R$ be an equivalence relation on $X$. For $a\in X$ put
> $$[a]=\{x\in X\ :\ xRa\}\qquad(\textbf{the equivalence class of }a).$$
> Then $\mathcal S=\{[a]:a\in X\}$ is a **partition** of $X$.

The heart of the proof is that **two equivalence classes are either identical or disjoint** — if $[a]$ and $[b]$ share an element then $[a]=[b]$ — which is precisely what "every element in exactly one member" requires. Reflexivity guarantees $a\in[a]$, so no class is empty and every element is covered.

> [!warning] All three properties are needed, and reflexivity is the one people drop
> If $R$ is symmetric and transitive but **not** reflexive, the sets $[a]$ do **not** partition $X$: some $b$ has $bRb$ failing, so $b\notin[b]$, and one checks $b$ lies in no class at all. **The construction silently loses elements.** So "equivalence relation" cannot be weakened.

**Putting the two theorems together: *equivalence relation* and *partition of a set* are two descriptions of one situation.** Each determines the other. This is genuinely useful in both directions — if a problem asks for a partition, you may instead find an equivalence relation and take its classes, and conversely.

> [!example]- Worked example — congruence (J Example 3.4.14)
> On $X=\{1,2,\dots,10\}$ define $xRy$ to mean **$3$ divides $x-y$**. This is an equivalence relation: $3\mid0$ (reflexive); $3\mid x-y\Rightarrow3\mid y-x$ (symmetric); $3\mid x-y$ and $3\mid y-z$ give $3\mid(x-y)+(y-z)=x-z$ (transitive).
>
> The classes are found by grouping equal remainders *(verified)*:
> $$[1]=\{1,4,7,10\},\qquad [2]=\{2,5,8\},\qquad [3]=\{3,6,9\},$$
> and $[1]=[4]=[7]=[10]$ — **a class has many names and one identity.** These three sets partition $X$ ✓
>
> **This is congruence modulo 3**, written $x\equiv y\pmod 3$, and it is the single most important equivalence relation in mathematics. [[05 - Number Theory and Cryptography|Ch. 05]] builds all of modular arithmetic and RSA on it; the classes are what `%` computes; and the reason arithmetic *works* on the classes — that you may add and multiply representatives — is exactly the statement that the operations respect the partition.

**A counting corollary.** If every equivalence class has exactly $r$ elements, there are $|X|/r$ classes — because the classes partition $X$ into equal-sized blocks. Trivial to state, and it is the "divide by the symmetries" step behind half the counting arguments of [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]].

### 7. Matrices of relations

Represent a relation $R$ from $X$ to $Y$ by a matrix: label rows by $X$ and columns by $Y$ (in some fixed order), and put $1$ in position $(x,y)$ iff $xRy$, else $0$. **The matrix depends on the chosen orderings**, so it is not canonical — but it is exactly what a computer stores.

For a relation **on** $X$ the matrix is square, using the same order for rows and columns, and two properties can be read off instantly:

| | matrix condition |
|---|---|
| **reflexive** | the **main diagonal** is all $1$s |
| **symmetric** | the matrix is **symmetric about the main diagonal** ($a_{ij}=a_{ji}$) |

**Composition is matrix multiplication.** If $A_1$ is the matrix of $R_1$ and $A_2$ of $R_2$, then the matrix of $R_2\circ R_1$ is obtained by **replacing every nonzero entry of the product $A_1A_2$ by $1$.**

The reason is worth seeing, because it explains a fact used constantly in [[08 - Graph Theory|ch. 08]]. Entry $(i,k)$ of $A_1A_2$ is $\sum_j (A_1)_{ij}(A_2)_{jk}$, a sum of products of $0$s and $1$s; it is nonzero **iff there is some $j$ with $(i,j)\in R_1$ and $(j,k)\in R_2$** — iff $(i,k)\in R_2\circ R_1$. And the *value* of the entry counts **how many such $j$ there are**, i.e. the number of two-step paths from $i$ to $k$. **So matrix multiplication does combinatorics**, and $(A^k)_{ij}$ counts paths of length $k$ — see [[Linear Algebra/contents/02 - Matrix Algebra|Linear Algebra ch. 02]].

**Hence a transitivity test.** Compute $A^2$ and compare with $A$:

$$R\text{ is transitive}\iff \text{whenever }(A^2)_{ij}\ne0,\text{ also }A_{ij}\ne0.$$

*(Verified on Johnsonbaugh's two examples: for $R=\{(a,a),(b,b),(c,c),(d,d),(b,c),(c,b)\}$ no entry of $A^2$ is nonzero where $A$ is zero, so $R$ is transitive; for $R=\{(a,a),(b,b),(c,c),(d,d),(a,c),(c,b)\}$ entry $(1,2)$ of $A^2$ is nonzero while $A_{12}=0$, so $R$ is not transitive — matching the book exactly.)*

**This is a mechanical test suitable for a computer**, which is the point: the definition of transitivity quantifies over triples, but the matrix version is one multiplication.

### 8. Relational databases

An **$n$-ary relation** is a subset of $X_1\times\cdots\times X_n$ — a table with $n$ columns. The columns are **attributes**, and the **domain** of an attribute is the set its values come from.

A single attribute or a combination is a **key** if its values uniquely determine a row. In a table of players with attributes *ID Number, Name, Position, Age*, the ID number is a key; **Name is not**, because two people can share a name (Johnsonbaugh's own table contains two players named Johnsonbaugh — a nice touch), and neither is Position or Age. *Name and Position together* might serve.

The **relational database model** (E. F. Codd) is built on exactly this, and its query operations are set operations on relations: **SELECT** (choose rows), **PROJECT** (choose columns), **JOIN** (combine tables on a shared attribute). **`WHERE`, the column list in `SELECT`, and `JOIN` in SQL are these three.**

> [!note] This is deliberately brief
> **A database table *is* an $n$-ary relation** — that identification is the illuminating part, and it is why the subject is called *relational*. Everything else (normalisation, functional dependencies, keys in earnest, query optimisation) belongs to [[Database Management Systems/contents/00-Index|Database Management Systems]], which owns it properly. Worth knowing here: **normalisation is applied relation theory**, and a functional dependency is a statement that one projection determines another.

## ✏️ Exercises

**1. (Functions.)** For each of the following, state whether it is one-to-one, onto, or both, with justification. (a) $f:\mathbb Z\to\mathbb Z$, $f(n)=3n-2$. (b) $g:\mathbb Z\to\mathbb Z$, $g(n)=n^2-n$. (c) $h:\mathbb R\to\mathbb R$, $h(x)=x^3$. (d) The hash function $h(n)=n\bmod 11$ from $\mathbb Z^+$ to $\{0,1,\dots,10\}$ — and explain why no hash function on $\mathbb Z^+$ can be injective.

> [!example]- Solution
> **(a) One-to-one, not onto.** Injective: if $3n_1-2=3n_2-2$ then $3n_1=3n_2$, so $n_1=n_2$ ✓. Not surjective: $f(n)=0$ would need $n=\tfrac23\notin\mathbb Z$. **One counterexample in the codomain suffices.**
>
> **(b) Neither.** Not injective: $g(0)=0$ and $g(1)=0$, so $0\ne1$ have the same image. Not surjective: $g(n)=n(n-1)$ is a product of consecutive integers, hence **always even** (one of them is even), so no odd value — say $1$ — is attained. *(Even $g(n)=-1$ fails, since $n^2-n+1>0$ for all integers.)*
>
> **(c) Both — a bijection.** Injective: $x^3$ is strictly increasing, so $x_1<x_2\Rightarrow x_1^3<x_2^3$, and equal cubes force equal inputs. Surjective: every real $y$ has the real cube root $x=y^{1/3}$ with $h(x)=y$. **Note this is a construction, which is what proving surjectivity requires.**
>
> **(d) Onto, not one-to-one.** Onto: each $c\in\{0,\dots,10\}$ is hit — take $n=c$ if $c\ge1$, and $n=11$ for $c=0$. Not one-to-one: $h(15)=4=h(26)$.
>
> **Why no hash function on $\mathbb Z^+$ can be injective.** An injective function from $\mathbb Z^+$ into $\{0,\dots,10\}$ would put infinitely many distinct inputs into eleven distinct outputs, which is impossible — **the pigeonhole principle** ([[06 - Counting Methods and the Pigeonhole Principle|ch. 06]]). More carefully: any $12$ distinct keys already force two into the same cell. **So collisions are structurally guaranteed, not a symptom of a bad hash**, and the only design question is how to handle them.

**2. (Floor, ceiling, mod, and a check digit.)** (a) Evaluate $\lfloor-7.2\rfloor$, $\lceil-7.2\rceil$, $\lfloor7.2\rfloor$, $\lceil7\rceil$, $-17\bmod5$, $\lfloor-17/5\rfloor$. (b) Verify that $n=d\lfloor n/d\rfloor+(n\bmod d)$ for $n=-17$, $d=5$. (c) Compute the Luhn check digit for the payload $7992739871$ and verify the result. (d) Explain what the doubling step in Luhn buys.

> [!example]- Solution
> **(a)** $\lfloor-7.2\rfloor=\mathbf{-8}$, $\ \lceil-7.2\rceil=\mathbf{-7}$, $\ \lfloor7.2\rfloor=\mathbf7$, $\ \lceil7\rceil=\mathbf7$.
>
> For the last two: the Quotient–Remainder Theorem demands $0\le r<d$, so $-17=5(-4)+3$ gives $-17\bmod5=\mathbf3$ and $\lfloor-17/5\rfloor=\lfloor-3.4\rfloor=\mathbf{-4}$.
>
> **The two traps.** $\lfloor-7.2\rfloor=-8$, **not** $-7$ — floor rounds *down*, away from zero for negatives, so it is not truncation. And $-17\bmod5=3$, **not** $-2$: the remainder is by definition nonnegative. Python agrees on both (`-17 % 5` is `3`, `math.floor(-3.4)` is `-4`), but C, Java and JavaScript return $-2$ for `-17 % 5` — **the same expression gives different answers in different languages**, which is worth knowing before you index an array with it.
>
> **(b)** $d\lfloor n/d\rfloor+(n\bmod d)=5(-4)+3=-20+3=-17=n$ ✓ The identity holds *because* the quotient uses floor rather than truncation — with truncation ($-3$) you would get $-15+3=-12\ne-17$.
>
> **(c)** Payload $7992739871$; we seek $c$ making the Luhn sum $\equiv0\pmod{10}$. Working from the right of the **full** number $7992739871c$, double every second digit, reduce values over $9$ by $9$, and sum. The answer is
> $$c=\mathbf3,\qquad\text{giving } \mathbf{79927398713},$$
> whose Luhn sum is $70\equiv0\pmod{10}$ ✓ *(verified computationally; the standard test number $4539148803436467$ also validates, sum $80$).*
>
> **(d)** Without doubling, the check would be "the digit sum is $\equiv0\pmod{10}$" — which catches every single-digit error but **no transposition at all**, since addition is commutative and swapping two digits leaves the sum unchanged. Doubling alternate positions breaks that symmetry: the two swapped digits get different weights, so the sum changes.
>
> **Verified exhaustively on $79927398713$:** of all single-digit alterations, **zero** still pass; of all adjacent transpositions, **zero** still pass. *(Luhn's one blind spot is swapping $0$ with $9$ — since $0\to0$ and $9\to18\to9$ contribute the same doubled value — and this number happens to contain no adjacent $09$ or $90$.)*

**3. (Relation properties.)** Let $R=\{(1,1),(1,2),(2,2),(2,3),(3,3)\}$ on $X=\{1,2,3\}$. (a) Determine which of reflexive, symmetric, antisymmetric, transitive hold. (b) Is $R$ a partial order? (c) Give a relation on $\{a,b,c\}$ that is **both** symmetric and antisymmetric, and explain why that is not a contradiction.

> [!example]- Solution
> **(a)** *(all four verified computationally)*
> - **Reflexive: yes.** $(1,1),(2,2),(3,3)$ are all present.
> - **Symmetric: no.** $(1,2)\in R$ but $(2,1)\notin R$.
> - **Antisymmetric: yes.** The only pairs with $x\ne y$ are $(1,2)$ and $(2,3)$, and neither reverse is present — so the condition "$(x,y),(y,x)\in R\Rightarrow x=y$" is never triggered.
> - **Transitive: NO.** $(1,2)\in R$ and $(2,3)\in R$, but $(1,3)\notin R$.
>
> **(b) No** — a partial order needs reflexive **and** antisymmetric **and** transitive, and transitivity fails. It satisfies two of the three, which is exactly why all three must be checked. *(Adding $(1,3)$ would make it a partial order; see Exercise 5.)*
>
> **(c)** Take $R=\{(a,a),(b,b),(c,c)\}$ — the equality relation.
> - **Symmetric:** for every $(x,y)\in R$ we have $x=y$, so $(y,x)=(x,y)\in R$ ✓
> - **Antisymmetric:** the condition only constrains pairs with $x\ne y$, and there are none, so it holds **vacuously** ✓
>
> **No contradiction, because the two properties are not negations of each other.** Symmetry says *if $(x,y)$ then $(y,x)$*; antisymmetry says *you cannot have both unless $x=y$*. A relation containing **no** off-diagonal pairs satisfies both trivially. The four possibilities all occur: equality (both), $\{(a,b),(b,a)\}$ (symmetric only), $\le$ (antisymmetric only), and $\{(a,b),(b,a),(b,c)\}$ (neither).
>
> **The lesson:** "not symmetric" and "antisymmetric" are independent conditions. Never derive one from the other — this is the most reliably examined confusion in the chapter.

**4. (Equivalence relations and partitions.)** On $X=\{1,2,\dots,12\}$ define $xRy$ to mean $4\mid(x-y)$. (a) Prove $R$ is an equivalence relation. (b) List the equivalence classes. (c) Confirm they partition $X$, and check the count against the rule "$|X|/r$ classes when every class has $r$ elements". (d) Explain why $[1]=[5]$ even though $1\ne5$.

> [!example]- Solution
> **(a)** Write $xRy$ as $x\equiv y\pmod4$.
> - **Reflexive:** $x-x=0$ and $4\mid0$ ✓
> - **Symmetric:** if $4\mid x-y$, say $x-y=4k$, then $y-x=4(-k)$, so $4\mid y-x$ ✓
> - **Transitive:** if $x-y=4k_1$ and $y-z=4k_2$ then $x-z=(x-y)+(y-z)=4(k_1+k_2)$ ✓
>
> Hence $R$ is an equivalence relation. *(Note the distinct witnesses $k_1,k_2$ — [[02 - Proofs and Mathematical Induction|ch. 02]]'s Important Note 1.)*
>
> **(b)** Grouping by remainder on division by 4 *(verified)*:
> $$[1]=\{1,5,9\},\quad [2]=\{2,6,10\},\quad [3]=\{3,7,11\},\quad [4]=\{4,8,12\}.$$
>
> **(c)** The four sets are pairwise disjoint, none is empty, and their union is $\{1,\dots,12\}$ — so every element lies in **exactly one**, which is the definition of a partition ✓
>
> Count check: every class has $r=3$ elements, so the rule predicts $|X|/r=12/3=\mathbf4$ classes, and there are indeed $4$ ✓ *(verified)*
>
> **(d) Because an equivalence class is a set, and a set is determined by its elements.** $[1]$ means "everything related to $1$", and $[5]$ means "everything related to $5$"; since $1R5$ (as $4\mid1-5$), transitivity and symmetry make these the *same collection*, namely $\{1,5,9\}$. **A class has as many names as it has members but only one identity** — here $[1]=[5]=[9]$.
>
> This is why one speaks of *choosing a representative*. It also explains why modular arithmetic is well defined: $\bmod4$, the class $[1]$ is "the numbers leaving remainder 1", and adding $[1]+[2]=[3]$ does not depend on which representatives you pick — $1+2=3$ and $5+10=15\equiv3$ ✓ **That independence is what makes [[05 - Number Theory and Cryptography|ch. 05]] possible.**

**5. (Hard — matrices of relations.)** Let $R=\{(1,1),(1,2),(2,2),(2,3),(3,3)\}$ on $\{1,2,3\}$ as in Exercise 3. (a) Write its matrix $A$. (b) Compute $A^2$ and use it to decide transitivity, confirming Exercise 3(a). (c) Interpret the *values* in $A^2$, not just their nonzero-ness. (d) Find the **transitive closure** of $R$ — the smallest transitive relation containing it — and explain why "smallest" is well defined. (e) Why does the matrix test not directly detect antisymmetry?

> [!example]- Solution
> **(a)** With the ordering $1,2,3$ for both rows and columns:
> $$A=\begin{pmatrix}1&1&0\\0&1&1\\0&0&1\end{pmatrix}$$
> The diagonal is all $1$s, confirming **reflexive** ✓; the matrix is not symmetric ($a_{12}=1$, $a_{21}=0$), confirming **not symmetric** ✓ — both readable at a glance, as §7 promised.
>
> **(b)**
> $$A^2=\begin{pmatrix}1&2&1\\0&1&2\\0&0&1\end{pmatrix}$$
> Compare entrywise: $(A^2)_{13}=1\ne0$ but $A_{13}=0$. **So $R$ is not transitive** ✓ — and the test even names the missing pair: $(1,3)$. This agrees exactly with Exercise 3(a), where transitivity failed on $(1,2),(2,3)\not\Rightarrow(1,3)$. *(Verified computationally; the only offending position is $(1,3)$.)*
>
> **(c)** $(A^2)_{ik}$ counts the number of $j$ with $(i,j)\in R$ and $(j,k)\in R$ — i.e. **the number of two-step paths from $i$ to $k$** in the digraph. So $(A^2)_{12}=2$ says there are two ways to get from $1$ to $2$ in exactly two steps: $1\to1\to2$ and $1\to2\to2$ (the loops count). And $(A^2)_{13}=1$ says exactly one: $1\to2\to3$.
>
> **This is the fact that makes adjacency matrices powerful** — $(A^k)_{ij}$ counts walks of length $k$, so a matrix product answers a combinatorial question. [[08 - Graph Theory|Ch. 08]] uses it for connectivity and [[Machine Learning/contents/02 - Markov Decision Processes|Markov chains]] use the same identity with probabilities in place of $0/1$.
>
> **(d)** Add the missing pair: $R^*=R\cup\{(1,3)\}=\{(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)\}$. Checking all compositions, $R^*$ **is** transitive *(verified)*, and no proper subset of it containing $R$ is — $(1,3)$ was forced. So $R^*$ is the transitive closure, and $R^*$ is now **reflexive, antisymmetric and transitive: a partial order** (indeed $\le$ on $\{1,2,3\}$).
>
> **Why "smallest" is well defined.** By §5's result, **an intersection of transitive relations is transitive.** There is at least one transitive relation containing $R$ (namely $X\times X$), so we may intersect *all* of them; the result contains $R$, is transitive, and is contained in every transitive relation containing $R$ — hence is the unique smallest. **The union would not work**, which is exactly why §5's asymmetry between $\cup$ and $\cap$ was worth noting.
>
> **(e)** The matrix test for reflexivity and symmetry works because both are conditions on **single entries or entry pairs**: "all diagonal entries are 1", "$a_{ij}=a_{ji}$". Antisymmetry is a condition on **pairs of off-diagonal positions with an exception at the diagonal** — it says: for every $i\ne j$, not both $a_{ij}=1$ and $a_{ji}=1$. That *is* checkable ($A$ and $A^{\mathsf T}$ must have no common $1$ off the diagonal, i.e. $A\wedge A^{\mathsf T}$ is diagonal), but it is not the single clean "is the matrix symmetric?" test, because **antisymmetry is not a symmetry of the matrix — it is a near-absence of one.** For $A$ here: $A\wedge A^{\mathsf T}=I$, off-diagonal part empty, so **antisymmetric** ✓ agreeing with Exercise 3.

## 📝 Summary

- **A function $f:X\to Y$ is a subset of $X\times Y$ with exactly one pair per $x$.** It may reuse elements of $Y$ and may leave some unused. **Domain and codomain are part of the function** — the same rule gives different functions, with different properties, over different sets.
- **$x\bmod y$, $\lfloor x\rfloor$ and $\lceil x\rceil$** are the workhorses. Floor is **not** truncation: $\lfloor-8.7\rfloor=-9$. The remainder is **nonnegative**: $-17\bmod5=3$. And $n=d\lfloor n/d\rfloor+(n\bmod d)$ — the Quotient–Remainder Theorem of [[02 - Proofs and Mathematical Induction|ch. 02]] made concrete.
- **Three applications, all "a function into a small set":** the **Luhn check digit** (catches all single-digit errors *and* transpositions — the doubling step is what buys the latter); **hash functions** (collisions are guaranteed by pigeonhole, so a policy is mandatory); **linear congruential PRNGs** $x_n=(ax_{n-1}+c)\bmod m$ (fully determined by the seed — hence reproducibility; must eventually cycle; and predictable enough to be a security hole).
- **Injective** = each output from at most one input; **surjective** = range equals codomain; **bijective** = both, and equivalent to having an inverse. To prove injectivity assume $f(x_1)=f(x_2)$; to prove surjectivity **construct** a preimage; to disprove either, one counterexample. **A bijection between finite sets proves equal size** — the engine of [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]].
- **A sequence is a function with an integer domain** — that is where the ordering comes from. In this book **"increasing" means strictly**, with **nondecreasing** for $\le$. A one-element sequence is all four monotonicity types vacuously.
- **A subsequence preserves order** (its indices form an increasing sequence); a **substring** is contiguous. **Concatenation is onto but not one-to-one**, which is why a split cannot be recovered from its result.
- **A relation is *any* subset of $X\times Y$** — no conditions. A relation on a finite set **is** a directed graph, which is the first appearance of [[08 - Graph Theory|ch. 08]].
- **The four properties:** reflexive (loops everywhere), symmetric (all edges bidirectional), antisymmetric (at most one direction between distinct vertices), transitive (every 2-step path has a shortcut). **"Not symmetric" $\ne$ "antisymmetric"** — a relation can be both, neither, or one.
- **Partial order = reflexive + antisymmetric + transitive.** "Partial" because some pairs may be incomparable; a **total order** has none. Finding a total order consistent with a partial one is a **topological sort** — what every build system computes.
- **Intersection preserves transitivity; union and composition do not.** That asymmetry is why **closures** are defined by intersecting, and it makes the transitive closure well defined.
- **Equivalence relation = reflexive + symmetric + transitive**, and **equivalence relations and partitions are the same thing**: a partition induces one, and the **equivalence classes $[a]=\{x:xRa\}$ of one form a partition.** Two classes are identical or disjoint. **Drop reflexivity and the construction silently loses elements.**
- **Congruence mod $n$ is the canonical example.** A class has many names and one identity ($[1]=[5]=[9]$ mod 4), which is precisely why modular arithmetic is well defined and why [[05 - Number Theory and Cryptography|ch. 05]] works.
- **Matrix of a relation:** reflexive ⟺ all-$1$ diagonal; symmetric ⟺ symmetric matrix. **The matrix of $R_2\circ R_1$ is $A_1A_2$ with nonzeros replaced by $1$**, so **$R$ is transitive iff every nonzero entry of $A^2$ is nonzero in $A$** — a mechanical test. And $(A^k)_{ij}$ **counts walks of length $k$**: matrix multiplication doing combinatorics.
- **A database table is an $n$-ary relation.** Attributes are columns, a **key** determines a row uniquely, and SELECT/PROJECT/JOIN are SQL's `WHERE`, column list and `JOIN`.

## ⚠️ Important Notes

1. **State the domain and codomain before claiming any property.** "$f(x)=x^2$ is not injective" is meaningless without them — it is injective on $[0,\infty)$ and surjective onto $[0,\infty)$.
2. **Range $\subseteq$ codomain, and usually strictly.** "Onto" is precisely the claim that they coincide, so it is a claim about the *codomain you chose*, not about the rule.
3. **Floor is not truncation and `int()` is not `floor()`.** $\lfloor-8.7\rfloor=-9$ but `int(-8.7)` is $-8$ in Python. Use `math.floor`.
4. **`%` differs across languages for negative operands.** Python gives `-17 % 5 == 3` (matching the mathematical definition); C, Java and JavaScript give $-2$. If you index or bucket with it, check which you have.
5. **To prove surjectivity you must construct a preimage.** Asserting "every $y$ is hit" is not an argument; producing the $x$ is.
6. **One counterexample disproves injectivity or surjectivity.** Do not build a general argument when $g(0)=g(1)$ will do.
7. **Collisions in a hash table are guaranteed, not a bug.** Any map from a larger set into a smaller one fails injectivity by pigeonhole. Judge a hash by *distribution*, and always have a collision policy.
8. **A seeded PRNG is deterministic — use that deliberately.** Set the seed to make an experiment reproducible; never use an LCG where unpredictability matters, and never assume "random" means "unguessable".
9. **In this book "increasing" is strict.** Other texts use it for $\le$. Check the convention before answering a monotonicity question, and beware the one-element sequence, which is vacuously all four.
10. **Subsequence preserves order; substring must be contiguous.** From $a,b,b,c$: $b,c$ is a subsequence, $c,b$ is not, and $bb$ is a substring while $ac$ is not.
11. **"Not symmetric" and "antisymmetric" are independent.** The equality relation is **both**; $\le$ is antisymmetric but not symmetric; $\{(a,b),(b,a),(b,c)\}$ is neither. Test each definition directly.
12. **Antisymmetry is easiest in its contrapositive form:** for all $x\ne y$, not both $(x,y)$ and $(y,x)$ belong to $R$. A relation with no off-diagonal pairs satisfies it vacuously.
13. **Check all three conditions for a partial order and all three for an equivalence relation.** Exercise 3's relation passes two of three and is neither. Two out of three is not a near miss; it is a different object.
14. **Reflexivity is the property people forget, and its loss is silent.** A symmetric, transitive, non-reflexive relation produces "classes" that leave some elements out of every class — no error message, just a wrong partition.
15. **An equivalence class is a set, so $[1]=[5]$ whenever $1R5$.** Choosing a representative is a convenience; the class does not depend on it, and that independence is what makes arithmetic on classes legitimate.
16. **Union does not preserve transitivity (or antisymmetry); intersection does.** So closures are built by intersecting. If you find yourself unioning to force a property, check whether the result actually has it.
17. **$(A^k)_{ij}$ counts walks of length $k$ — the entries, not just their nonzero pattern, carry information.** Replacing nonzeros by $1$ throws that away, and sometimes the count is what you wanted.
18. **The matrix of a relation depends on the ordering you chose.** Two different-looking matrices can represent the same relation, so never compare matrices to test whether relations are equal without fixing the order.

> [!warning] Gaps in the source material
> **Extraction was good for prose, definitions and theorem statements**, as in ch. 01–02: Johnsonbaugh's Unicode mathematics ($\in$, $\notin$, $\lfloor\cdot\rfloor$, $\lceil\cdot\rceil$, $\preceq$, $\circ$, $\lambda$, $R^{-1}$) survives. See `00-Index.md` for the standing quirk list.
>
> **Matrices survive better here than anywhere else in the vault** — §3.5's matrices extract with their rows intact (as digit strings such as `0101 / 0010 / 0110 / 1000` plus separate row and column labels), so they were reconstructable and were then checked by recomputing the book's stated conclusions. **All of §7's claims were re-verified with `numpy`**, including both of Johnsonbaugh's transitivity examples: Example 3.5.7 is transitive, and Example 3.5.8 fails at exactly **row 1, column 2** — the position the book names.
>
> **Two worked examples lost their data, and one was recovered.**
> - **Example 3.1.16's PRNG constants are not printed in any surviving text** — the modulus $11$ and seed $3$ appear, but $a$ and $c$ do not. **They were recovered from the fragments the book does print:** the sequence begins $3,4,0,5$ and satisfies $x_{10}=3$. Those three conditions have the unique solution $a=7$, $c=5$, giving the full cycle $3,4,0,5,7,10,9,2,8,6$ of period $10$ — consistent with every printed value. **Recorded as a reconstruction, not an extraction.**
> - **Example 3.1.15's collision cannot be recovered.** The six keys the book lists ($15,558,32,132,102,5$) hash to the *distinct* cells $4,8,10,0,3,5$, so the collision it goes on to discuss must involve a further key shown only in **Figure 3.1.6, which is an image and is lost.** §2(b) supplies its own colliding key ($h(26)=4=h(15)$) rather than guessing the book's.
> - **Example 3.1.13's Luhn formula is lost.** §2(a) states the standard public-domain algorithm and verifies it independently (check digit $3$ for payload $7992739871$; the test number $4539148803436467$ validates; and exhaustive checks confirming that **all** single-digit errors and **all** adjacent transpositions in $79927398713$ are caught).
>
> **All figures are images and are lost.** Most consequential: Figures 3.1.1 and 3.1.9–3.1.12 (**every arrow diagram**, which is how injectivity and surjectivity are conventionally taught — §3 gives the "at most one / at least one arrow" reading in words instead), Figure 3.1.7 (graphs of floor and ceiling), Figure 3.1.6 (the hash table, discussed above), Figures 3.3.1–3.3.2 and 3.4.1 (**the digraphs of relations and the equivalence-class picture**), and the Hasse-diagram material in the §3.3 exercises. For a chapter about structures usually drawn as diagrams this is a real loss; the notes give set-theoretic and matrix descriptions, which is what a proof needs anyway.
>
> **Verification performed.** Every claim above plus all five exercises: the four relation properties of Exercise 3 checked exhaustively over $\{1,2,3\}$; $A$, $A^2$ and the offending entry $(1,3)$; the transitive closure confirmed transitive; the mod-4 classes $\{1,5,9\},\{2,6,10\},\{3,7,11\},\{4,8,12\}$ and the count $12/3=4$; Johnsonbaugh's mod-3 classes $[1]=\{1,4,7,10\}$, $[2]=\{2,5,8\}$, $[3]=\{3,6,9\}$ reproduced exactly; and the hash and Luhn computations. **No error was found in Johnsonbaugh ch. 3** — the errata table in `00-Index.md` remains empty after three chapters.
>
> **Additions beyond the source.** The **pigeonhole explanation of why hash collisions are inevitable** is mine — Johnsonbaugh defines collisions and moves on without noting that injectivity is impossible in principle. The **error-detection analysis of Luhn** (exhaustive single-digit and transposition checks, and the $0\!\leftrightarrow\!9$ blind spot) is my own addition; the book gives the algorithm but not its guarantees. The **`int()` vs `math.floor()` and cross-language `%` warnings** are mine. The observation that $(A^k)_{ij}$ **counts walks** — and hence that matrix multiplication performs combinatorics — is stated here explicitly and forward-linked to [[08 - Graph Theory|ch. 08]] and Markov chains; Johnsonbaugh proves the $k=2$ case only, as a device for testing transitivity, and does not draw the general moral. Exercise 5(c)–(e) is my own construction, including the matrix characterisation of antisymmetry ($A\wedge A^{\mathsf T}$ diagonal) and the argument that transitive closure is well defined **because** intersection preserves transitivity. The framing of the whole chapter around "functions, sequences and relations are all sets of ordered pairs" is mine.
>
> **§3.6 is deliberately compressed.** Johnsonbaugh's four pages on relational databases introduce $n$-ary relations, attributes, keys and the SELECT/PROJECT/JOIN operations. §8 keeps the one genuinely illuminating identification — **a table is an $n$-ary relation** — and defers the rest to [[Database Management Systems/contents/00-Index|Database Management Systems]], per the ownership split recorded in `00-Index.md`. Johnsonbaugh marks the section optional himself.

**Previous:** [[02 - Proofs and Mathematical Induction]] · **Next:** [[04 - Algorithms and Their Analysis]]
