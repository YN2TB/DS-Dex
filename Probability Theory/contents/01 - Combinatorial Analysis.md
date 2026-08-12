---
subject: Probability Theory
chapter: 01
tags: [ds, probability, combinatorics, counting, binomial-coefficient]
source: "Ross, *A First Course in Probability*, 10th ed., ch. 1 (pp. 13–33)"
---

# Combinatorial Analysis

> [!abstract] What this chapter is for
> **This chapter contains no probability at all.** It is pure counting — and it comes first because of one observation made on the book's opening page:
>
> > **Many problems in probability theory can be solved simply by counting the number of different ways that a certain event can occur.**
>
> When every outcome is equally likely, $P(E)$ is just $\dfrac{\text{outcomes in }E}{\text{total outcomes}}$ — **so the whole problem collapses into two counting exercises.** [[02 - Axioms of Probability|Chapter 2]] makes that precise; this chapter builds the tools.
>
> | § | Tool | Answers |
> |---|---|---|
> | **2** | Basic principle of counting | "How many ways in total?" |
> | **3** | **Permutations**, $n!$ | "How many *orderings*?" |
> | **4** | **Combinations**, $\binom{n}{r}$ | "How many *groups*, order irrelevant?" |
> | **5** | **Multinomial coefficients** | "How many ways to split into $r$ labelled groups?" |
> | **6** | Integer solutions of $x_1+\cdots+x_r=n$ | "How many ways to distribute $n$ identical things?" |
>
> > [!tip] The question that unlocks every problem in this chapter
> > **Does order matter, and are the objects distinguishable?** Almost every mistake in combinatorics is answering one of those two questions wrongly.

---

## 📘 Main Knowledge

### 1. The motivating problem

Ross opens with a problem worth keeping in mind throughout, because it recurs three times in the chapter:

> **A communication system consists of $n$ antennas in a line. It is *functional* as long as no two consecutive antennas are defective. If exactly $m$ of the $n$ are defective, what is the probability the system is functional?**

For $n=4$, $m=2$ there are 6 configurations (1 = working, 0 = defective):

$$0110\quad 0101\quad 1010\quad 0011\quad 1001\quad 1100$$

**The first three are functional, the last three are not**, so the probability is $\tfrac36=\tfrac12$.

> [!important] What this example demonstrates
> **We answered a probability question by counting twice** — once for the favourable configurations, once for all of them. **For general $n$ and $m$, listing is hopeless. We need formulas.**
>
> The general answer, derived twice in this chapter (§4 Example 4c and §6 Example 6d), turns out to be
> $$\boxed{\frac{\binom{n-m+1}{m}}{\binom{n}{m}}}$$
> **Check it against the special case:** $n=4$, $m=2$ gives $\binom{3}{2}\big/\binom{4}{2}=3/6=\tfrac12$ ✓.

---

### 2. The basic principle of counting

> [!important] The basic principle of counting
> Suppose two experiments are performed. If experiment 1 has $m$ possible outcomes, and **for each outcome of experiment 1** experiment 2 has $n$ possible outcomes, then there are
> $$\boxed{mn}$$
> possible outcomes of the two experiments together.

**Proof:** enumerate them as a rectangular array — write $(i,j)$ when experiment 1 gives its $i$th outcome and experiment 2 its $j$th:

$$\begin{matrix}(1,1)&(1,2)&\cdots&(1,n)\\ (2,1)&(2,2)&\cdots&(2,n)\\ \vdots&&&\vdots\\ (m,1)&(m,2)&\cdots&(m,n)\end{matrix}$$

**$m$ rows of $n$ elements each.** $\blacksquare$

> [!warning] The clause that does the work
> ***"for each outcome of experiment 1, there are $n$ possible outcomes of experiment 2"***
>
> **The second experiment need not have the *same* outcomes each time — only the same *number* of them.** This is what lets the principle handle sampling without replacement, where the available choices shrink but do so predictably.

> [!example] Example 2a
> A community has 10 women, each with 3 children. Choose one woman and one of *her* children as mother and child of the year. How many choices?
>
> **$10\times3=\mathbf{30}$.** *(Note the children available depend on which woman was chosen — but there are always exactly 3.)*

**The generalized principle** extends this to $r$ experiments: if the first has $n_1$ outcomes, the second $n_2$ for each of those, and so on, there are

$$\boxed{n_1\cdot n_2\cdots n_r}$$

possible outcomes in total.

> [!example] Example 2b
> A planning committee has 3 freshmen, 4 sophomores, 5 juniors, 2 seniors. A subcommittee of 4 takes one person from each class. How many subcommittees?
>
> **$3\times4\times5\times2=\mathbf{120}$.**

---

### 3. Permutations

**A permutation is an ordered arrangement.** With 3 objects there are $3\cdot2\cdot1=6$ orderings: 3 choices for the first slot, 2 for the second, 1 for the last.

> [!important] Permutations of $n$ distinct objects
> $$\boxed{n(n-1)(n-2)\cdots3\cdot2\cdot1=n!}$$
> with the convention
> $$\boxed{0!=1}$$

> [!note] Why $0!=1$ is a definition worth making, not a trick
> It is chosen so that formulas do not need special cases. **There is exactly one way to arrange nothing** (the empty arrangement), and setting $0!=1$ makes $\binom{n}{n}=\binom{n}{0}=1$ come out right automatically. **Every combinatorial formula in this chapter would need an exception clause without it.**

| Example | Question | Answer |
|---|---|---|
| **3a** | Batting orders for 9 players | $9!=\mathbf{362{,}880}$ |
| **3b(a)** | Rankings of 6 men and 4 women | $10!=\mathbf{3{,}628{,}800}$ |
| **3b(b)** | Men ranked among themselves, women among themselves | $6!\,4!=720\times24=\mathbf{17{,}280}$ |

> [!example] Example 3c — a two-level arrangement
> Ms. Jones shelves 10 books: 4 maths, 3 chemistry, 2 history, 1 language, **with same-subject books together.** How many arrangements?
>
> **Two things are being ordered: the books within each subject, and the subjects themselves.**
> $$\underbrace{4!}_{\text{subject blocks}}\times\underbrace{4!\,3!\,2!\,1!}_{\text{within blocks}}=24\times288=\mathbf{6912}$$
>
> **The commonest error is forgetting the outer $4!$** — arranging within the blocks but leaving the blocks in a fixed order.

#### 3a. Permutations with indistinguishable objects

> [!example] Example 3d — PEPPER
> How many letter arrangements of **PEPPER**?
>
> **Start by pretending the repeats are distinguishable:** $P_1E_1P_2P_3E_2R$ gives $6!$ permutations. But permuting the P's among themselves ($3!$ ways) and the E's among themselves ($2!$ ways) leaves the *visible* word unchanged — so **each genuine arrangement has been counted $3!\,2!=12$ times.**
> $$\frac{6!}{3!\,2!}=\frac{720}{12}=\mathbf{60}$$

> [!important] Permutations with repeats
> There are
> $$\boxed{\frac{n!}{n_1!\,n_2!\cdots n_r!}}$$
> permutations of $n$ objects of which $n_1$ are alike, $n_2$ are alike, …, $n_r$ are alike.

> [!tip] The "overcount then divide" pattern
> **This is the most reusable idea in the chapter.** Count as if everything were distinguishable, work out the constant factor by which each real object was overcounted, then divide.
>
> **It reappears immediately** in §4 (each group of $r$ counted $r!$ times) and in Example 5c (each unlabelled team split counted $2!$ times).

| Example | Question | Answer |
|---|---|---|
| **3e** | Nationality orderings: 4 Russian, 3 US, 2 GB, 1 Brazil | $\dfrac{10!}{4!\,3!\,2!\,1!}=\mathbf{12{,}600}$ |
| **3f** | Signals from 4 white, 3 red, 2 blue flags | $\dfrac{9!}{4!\,3!\,2!}=\mathbf{1260}$ |

---

### 4. Combinations

**Now order does *not* matter.** How many groups of 3 from $\{A,B,C,D,E\}$? Selecting in order gives $5\cdot4\cdot3=60$, **but each group of 3 is counted $3!=6$ times** (ABC, ACB, BAC, BCA, CAB, CBA all give the same group), so

$$\frac{5\cdot4\cdot3}{3\cdot2\cdot1}=\mathbf{10}$$

> [!important] The binomial coefficient
> $$\boxed{\binom{n}{r}=\frac{n(n-1)\cdots(n-r+1)}{r!}=\frac{n!}{(n-r)!\,r!}}, \qquad r\le n$$
> read **"$n$ choose $r$"**. It counts:
> - the number of **groups of size $r$** from $n$ objects when order is irrelevant, equivalently
> - the number of **subsets of size $r$** of a set of size $n$.
>
> **Conventions:** $\binom{n}{n}=\binom{n}{0}=\dfrac{n!}{0!\,n!}=1$ (using $0!=1$), and
> $$\boxed{\binom{n}{r}=0 \quad\text{when } r>n \text{ or } r<0}$$

> [!note] Why the conventions are sensible, not arbitrary
> A set of size $n$ has **exactly one** subset of size $n$ (itself) and **exactly one** of size 0 (the empty set) — so $\binom{n}{n}=\binom{n}{0}=1$ is forced. And **there are genuinely zero ways to choose 8 things from 5**, so $\binom{5}{8}=0$ is the honest answer. **The convention lets you write sums without worrying about their limits.**

| Example | Question | Answer |
|---|---|---|
| **4a** | Committees of 3 from 20 people | $\binom{20}{3}=\dfrac{20\cdot19\cdot18}{3\cdot2\cdot1}=\mathbf{1140}$ |
| **4b** | 2 women from 5 and 3 men from 7 | $\binom52\binom73=10\times35=\mathbf{350}$ |

> [!example] Example 4b, part two — the feuding men
> **Two of the 7 men refuse to serve together.** How many committees now?
>
> **Count the bad cases and subtract.** Groups of 3 men containing *both* feuders: choose both feuders ($\binom22=1$ way) and one more man from the remaining 5 ($\binom51=5$ ways) $\Rightarrow$ **5 bad groups** out of $\binom73=35$. So $35-5=\mathbf{30}$ acceptable male groups, and
> $$30\times\binom52=30\times10=\mathbf{300}$$
>
> **The "count the complement" move is worth internalising** — "at least one" and "not both" conditions are almost always easier to handle by subtraction.

#### 4a. The antenna problem, solved

> [!example] Example 4c — no two defectives consecutive
> $n$ antennas, $m$ defective, $n-m$ functional, all defectives alike and all functionals alike. How many orderings have **no two defectives adjacent**?
>
> **The trick: place the functional ones first, then slot the defectives into the gaps.**
>
> Line up the $n-m$ functional antennas. This creates $n-m+1$ gaps (including the two ends):
> $$\wedge\;1\;\wedge\;1\;\wedge\;1\;\cdots\;\wedge\;1\;\wedge\;1\;\wedge$$
> **No two defectives are adjacent precisely when each gap holds at most one defective.** So we simply choose which $m$ of the $n-m+1$ gaps get one:
> $$\boxed{\binom{n-m+1}{m}}$$
>
> **Why this construction is the right one:** it converts an *adjacency constraint* — awkward to count directly — into a plain *selection*. **Look for this whenever a problem forbids certain items from touching.**

#### 4b. Pascal's identity

> [!important] Pascal's identity
> $$\boxed{\binom{n}{r}=\binom{n-1}{r-1}+\binom{n-1}{r}}, \qquad 1\le r\le n \tag{4.1}$$

**Combinatorial proof — no algebra needed.** Fix one particular object, call it object 1. Every group of size $r$ either contains it or does not:

- **Contains object 1:** choose the other $r-1$ from the remaining $n-1$ $\Rightarrow\binom{n-1}{r-1}$ groups
- **Does not:** choose all $r$ from the remaining $n-1$ $\Rightarrow\binom{n-1}{r}$ groups

**These cases are exhaustive and disjoint, so they sum to $\binom nr$.** $\blacksquare$

> [!tip] Combinatorial proofs beat algebraic ones
> The identity can also be verified by expanding factorials — **but the argument above explains *why* it is true.** This "condition on whether a particular object is included" technique proves most binomial identities, and it is the discrete ancestor of the conditioning arguments in [[03 - Conditional Probability and Independence|ch. 03]].
>
> *(Pascal's identity is also the rule generating **Pascal's triangle**: each entry is the sum of the two above it.)*

#### 4c. The binomial theorem

> [!important] The binomial theorem
> $$\boxed{(x+y)^n=\sum_{k=0}^{n}\binom{n}{k}x^ky^{n-k}} \tag{4.2}$$
> **This is why the $\binom nk$ are called *binomial coefficients*.**

Ross gives two proofs. **The combinatorial one is the one to remember.**

> [!tip] Combinatorial proof — the informative one
> Expand $(x_1+y_1)(x_2+y_2)\cdots(x_n+y_n)$. **Each of the $2^n$ terms picks either $x_i$ or $y_i$ from each factor.** For example
> $$(x_1+y_1)(x_2+y_2)=x_1x_2+x_1y_2+y_1x_2+y_1y_2$$
> **How many terms have exactly $k$ of the $x$'s?** Each corresponds to choosing which $k$ of the $n$ factors contribute their $x$ — so there are $\binom nk$ of them. Setting every $x_i=x$ and $y_i=y$ gives (4.2). $\blacksquare$
>
> **The insight: $\binom nk$ appears in the binomial theorem for exactly the reason it counts subsets. It is the same act of choosing.**

*(The inductive proof works too, using Pascal's identity (4.1) at the key step — but it verifies the result rather than explaining it.)*

> [!example] Example 4d
> $$(x+y)^3=\binom30y^3+\binom31xy^2+\binom32x^2y+\binom33x^3=y^3+3xy^2+3x^2y+x^3$$

> [!example] Example 4e — how many subsets does an $n$-set have?
> **Method 1 (sum the sizes).** There are $\binom nk$ subsets of size $k$, so
> $$\sum_{k=0}^{n}\binom nk=(1+1)^n=\boxed{2^n}$$
> by the binomial theorem with $x=y=1$.
>
> **Method 2 (bijection).** Assign 0 or 1 to each element; the subset is everything assigned 1. **This is a one-to-one correspondence between subsets and binary strings of length $n$**, of which there are $2^n$.
>
> **The null set is included**, so the number of **non-empty** subsets is $\mathbf{2^n-1}$.
>
> > **Two proofs of the same fact, and the second explains the first.** The identity $\sum_k\binom nk=2^n$ is not a coincidence — both sides count the same objects.

---

### 5. Multinomial coefficients

**Generalising from two groups (chosen / not chosen) to $r$ labelled groups.**

Divide $n$ distinct items into $r$ distinct groups of sizes $n_1,\dots,n_r$ with $\sum_i n_i=n$. By the generalized counting principle:

$$\binom{n}{n_1}\binom{n-n_1}{n_2}\cdots\binom{n-n_1-\cdots-n_{r-1}}{n_r}$$

and the factorials telescope beautifully:

$$=\frac{n!}{(n-n_1)!\,n_1!}\cdot\frac{(n-n_1)!}{(n-n_1-n_2)!\,n_2!}\cdots\frac{(n-n_1-\cdots-n_{r-1})!}{0!\,n_r!}=\frac{n!}{n_1!\,n_2!\cdots n_r!}$$

> [!important] Multinomial coefficient
> $$\boxed{\binom{n}{n_1,n_2,\dots,n_r}=\frac{n!}{n_1!\,n_2!\cdots n_r!}} \qquad\text{where } n_1+\cdots+n_r=n$$
> the number of ways to divide $n$ **distinct** objects into $r$ **distinct** groups of sizes $n_1,\dots,n_r$.

> [!important] The identity hiding in plain sight
> **This is the same formula as §3's permutations-with-repeats.** That is not an accident.
>
> **The bijection:** write down the string $1,1,\dots,1,2,\dots,2,\dots,r,\dots,r$ where $i$ appears $n_i$ times. **Read a permutation of that string as an assignment: item $j$ goes to the group named by position $j$.**
>
> *Ross's illustration:* with $n=8$, $(n_1,n_2,n_3)=(4,3,1)$, the permutation $1,1,2,3,2,1,2,1$ assigns items **1, 2, 6, 8** to group 1; items **3, 5, 7** to group 2; item **4** to group 3.
>
> **Every permutation gives a division and every division comes from a permutation — so the counts must be equal.** *"Arranging objects with repeats" and "splitting objects into labelled groups" are the same problem in different clothes.*

| Example | Question | Answer |
|---|---|---|
| **5a** | 10 officers → 5 patrol, 2 full-time, 3 reserve | $\dfrac{10!}{5!\,2!\,3!}=\mathbf{2520}$ |
| **5b** | 10 children → team A of 5, team B of 5 | $\dfrac{10!}{5!\,5!}=\mathbf{252}$ |

> [!example] Example 5c — the labelled/unlabelled distinction
> **10 children divide themselves into two teams of 5. Now there is no "A" and "B" — just a split.**
> $$\frac{10!/(5!\,5!)}{2!}=\frac{252}{2}=\mathbf{126}$$
>
> > [!warning] This is the single most-missed distinction in the chapter
> > **Example 5b and Example 5c ask the same question with one word changed, and the answers differ by a factor of 2.**
> >
> > **The test: would swapping two groups produce a different outcome?**
> > - **Yes** (team A plays a different league from team B) → labelled → $\dfrac{n!}{n_1!\cdots n_r!}$
> > - **No** (just two teams on a playground) → unlabelled → **divide by $k!$**, where $k$ is the number of groups **of equal size** that could be permuted
> >
> > **Only equal-sized groups need the correction.** Example 5a's groups (5, 2, 3) have distinct sizes, so they are automatically distinguishable — no division needed even if the roles were unnamed.

#### 5a. The multinomial theorem

> [!important] The multinomial theorem
> $$\boxed{(x_1+x_2+\cdots+x_r)^n=\sum_{\substack{(n_1,\dots,n_r)\\ n_1+\cdots+n_r=n}}\binom{n}{n_1,n_2,\dots,n_r}x_1^{n_1}x_2^{n_2}\cdots x_r^{n_r}}$$
> summed over all **nonnegative integer** vectors $(n_1,\dots,n_r)$ summing to $n$.

> [!example] Example 5e
> $$(x_1+x_2+x_3)^2 = \binom{2}{2,0,0}x_1^2+\binom{2}{0,2,0}x_2^2+\binom{2}{0,0,2}x_3^2+\binom{2}{1,1,0}x_1x_2+\binom{2}{1,0,1}x_1x_3+\binom{2}{0,1,1}x_2x_3$$
> $$=x_1^2+x_2^2+x_3^2+2x_1x_2+2x_1x_3+2x_2x_3$$
> **The familiar expansion, with the cross-term 2's explained: $\binom{2}{1,1,0}=2!/(1!1!0!)=2$.**

#### 5b. A striking application

> [!example] Example 5d — the knockout tournament
> $n=2^m$ players; each round pairs them up, losers are eliminated, until one remains. **Take $n=8$.**
>
> **(a) Outcomes of the first round.**
> Divide 8 players into a 1st, 2nd, 3rd and 4th pair: $\binom{8}{2,2,2,2}=\dfrac{8!}{2^4}=2520$. **But the pairs are not ordered**, so divide by $4!$: $\dfrac{8!}{2^4\,4!}=\mathbf{105}$ pairings. Each pairing has **2 possible winners per game**, i.e. $2^4$ results:
> $$\frac{8!\cdot2^4}{2^4\,4!}=\frac{8!}{4!}=\mathbf{1680}$$
>
> *(Cleaner route: choose the 4 winners, $\binom84=70$ ways, then pair each winner with a loser, $4!=24$ ways $\Rightarrow70\times24=1680$ ✓.)*
>
> **(b) Outcomes of the whole tournament.** Round 2 has $4!/2!$ outcomes for each round-1 result, round 3 has $2!/1!$:
> $$\frac{8!}{4!}\cdot\frac{4!}{2!}\cdot\frac{2!}{1!}=\mathbf{8!}=40{,}320$$
>
> > **A knockout tournament of $n=2^m$ players has exactly $n!$ possible outcomes** — the telescoping is not a coincidence.
> >
> > **Ross's bijective explanation is the satisfying one:** rank the champion 1 and the final-round loser 2; of the two semi-final losers, rank 3 the one who lost to player 1 and rank 4 the one who lost to player 2; and so on. *(Succinctly: a player who lost in a round having $2^k$ matches gets rank $2^k$ plus the rank of whoever beat them.)* **This assigns every tournament result a distinct permutation of $1,\dots,n$, and every permutation arises — so the two sets have the same size.**
> >
> > **Whenever a count comes out to something as clean as $n!$, look for a bijection.**

---

### 6. The number of integer solutions of equations

> [!note] Ross marks this section optional (asterisked). **Do not skip it** — it is how you count distributions of *identical* objects, and it is used constantly from ch. 4 onward.

**The motivating question.** Lake Ticonderoga holds four fish types. You catch 10 fish. **How many possible outcomes**, where an outcome records only *how many of each type*?

That is the number of nonnegative integer vectors $(x_1,x_2,x_3,x_4)$ with $x_1+x_2+x_3+x_4=10$ — and more generally, solutions of

$$x_1+x_2+\cdots+x_r=n \tag{6.1}$$

#### 6a. Positive solutions — the "stars and bars" argument

Line up $n$ zeroes in a row, with the $n-1$ gaps between adjacent zeroes marked:

$$0\;\wedge\;0\;\wedge\;0\;\wedge\;\cdots\;\wedge\;0\;\wedge\;0$$

**Choose $r-1$ of these $n-1$ gaps as dividers.** Let $x_1$ be the number of zeroes before the first divider, $x_2$ the number between the first and second, and so on.

*Ross's illustration:* with $n=8$, $r=3$, choosing the gaps marked by dots,

$$0\,\boldsymbol{\cdot}\,0000\,\boldsymbol{\cdot}\,000 \qquad\Longrightarrow\qquad x_1=1,\ x_2=4,\ x_3=3$$

**Every positive solution corresponds to exactly one choice of dividers, and vice versa.**

> [!important] Proposition 6.1 — positive solutions
> There are
> $$\boxed{\binom{n-1}{r-1}}$$
> positive integer vectors $(x_1,\dots,x_r)$ with $x_1+\cdots+x_r=n$, $x_i>0$.

> [!tip] Why the dividers must go in *distinct* gaps
> **Each part must be at least 1** — so no two dividers may share a gap, and none may sit at the ends. **That is exactly what "choose $r-1$ of the $n-1$ internal gaps" enforces.** *(The nonnegative version, where empty parts are allowed, is handled next by a change of variable rather than by relaxing this.)*

#### 6b. Nonnegative solutions — by substitution

**Do not re-derive; transform.** The nonnegative solutions of $x_1+\cdots+x_r=n$ correspond one-to-one with the **positive** solutions of

$$y_1+\cdots+y_r=n+r, \qquad \text{via } y_i=x_i+1$$

*(Adding 1 to each of $r$ variables adds $r$ to the total.)* Apply Proposition 6.1 with $n+r$ in place of $n$:

> [!important] Proposition 6.2 — nonnegative solutions
> There are
> $$\boxed{\binom{n+r-1}{r-1}}$$
> nonnegative integer vectors $(x_1,\dots,x_r)$ with $x_1+\cdots+x_r=n$.

> [!tip] The shifting trick generalises to *any* lower bound
> **To impose $x_i\ge c_i$, substitute $y_i=x_i-c_i$ and reduce the total by $\sum_i c_i$.** The problem becomes a plain nonnegative count. **This one manoeuvre handles every constrained version you will meet** — see Example 6d and Exercise 4.
>
> **It does not work for *upper* bounds**, which require inclusion–exclusion ([[02 - Axioms of Probability|ch. 02]]).

**So the fishing problem:** $n=10$, $r=4$ gives $\binom{13}{3}=\mathbf{286}$ outcomes.

| Example | Question | Answer |
|---|---|---|
| **6a** | Nonneg. solutions of $x_1+x_2=3$ | $\binom{4}{1}=\mathbf{4}$: $(0,3),(1,2),(2,1),(3,0)$ |
| **6b** | \$20,000 in \$1000 units among 4 investments, all invested | $\binom{23}{3}=\mathbf{1771}$ |
| **6b** | …if not all need be invested | $\binom{24}{4}=\mathbf{10{,}626}$ |
| **6c** | Number of terms in $(x_1+\cdots+x_r)^n$ | $\binom{n+r-1}{r-1}$ |

> [!tip] The slack-variable idea in Example 6b
> **"Not all the money need be invested" turns an inequality into an equation** by adding $x_5$ = amount held in reserve, so $x_1+\cdots+x_5=20$. **Converting $\le$ into $=$ with a slack variable is a standard move** — it also appears in linear programming ([[Optimization/contents/00-Index|Optimization]]).

#### 6c. The antenna problem, again

> [!example] Example 6d — the same answer by a different route
> $n$ items, $m$ defective. Let $x_1$ = functional items left of the first defective, $x_2$ = functional items between defectives 1 and 2, …, $x_{m+1}$ = functional items after the last defective:
> $$x_1\ 0\ x_2\ 0\ \cdots\ x_m\ 0\ x_{m+1}$$
> **No two defectives adjacent means every *internal* gap has at least one functional item:**
> $$x_1+\cdots+x_{m+1}=n-m, \qquad x_1\ge0,\ x_{m+1}\ge0,\ x_i>0 \text{ for } i=2,\dots,m$$
> Substitute $y_1=x_1+1$, $y_i=x_i$ for $i=2,\dots,m$, $y_{m+1}=x_{m+1}+1$ to make everything positive:
> $$y_1+\cdots+y_{m+1}=n-m+2$$
> By Proposition 6.1, there are $\binom{n-m+1}{m}$ solutions — **in agreement with Example 4c.** ✓
>
> **Now generalise, which the gap-selection argument cannot easily do.** For each pair of defectives separated by **at least 2** functional items, require $x_i\ge2$ for $i=2,\dots,m$. The same substitution gives $y_1+\cdots+y_{m+1}=n-2m+3$, hence
> $$\boxed{\binom{n-2m+2}{m}}$$
>
> > **This is why §6 is worth the effort.** §4's construction answered one question elegantly; §6's method answers the whole family. **When a constraint has a threshold that might change, set it up as an integer equation.**

---

## ✏️ Exercises

> [!note] These exercises are my own construction
> Every figure is either quoted from the text or computed by hand, and **all arithmetic below has been independently verified.**

---

**Exercise 1 — The basic principle, with and without repetition**

**(i)** How many 7-place licence plates are possible if the first 2 places are letters (26) and the last 5 are digits (10)?

**(ii)** Same question if no letter and no digit may repeat.

**(iii)** A die is rolled 4 times, recording the ordered sequence. How many outcomes?

**(iv)** A safe opens with a 3-digit code (digits 0–9). How many codes? How many with no repeated digit?

**(v)** In (ii) and (iv), the counts fell. **State precisely which clause of the basic principle still holds and which fails**, and explain why the principle still applies.

> [!example]- Solution
> **(i)** $26^2\times10^5=676\times100{,}000=\mathbf{67{,}600{,}000}$
>
> **(ii)** $26\times25\times10\times9\times8\times7\times6=\mathbf{19{,}656{,}000}$
>
> **(iii)** $6^4=\mathbf{1296}$
>
> **(iv)** $10^3=\mathbf{1000}$; with no repeats, $10\times9\times8=\mathbf{720}$
>
> ---
> **(v)** **What fails: the outcomes of the later experiments are no longer the *same* set.** After choosing 'Q' for the first letter, 'Q' is unavailable for the second — **the available options genuinely change.**
>
> **What holds — and it is all the principle requires: the *number* of options is the same regardless of what was chosen.** Whatever the first letter was, exactly 25 remain.
>
> > **This is the clause emphasised in §2:** *"for each outcome of experiment 1, there are $n$ possible outcomes of experiment 2."* **It says "for each," not "the same ones."**
> >
> > **Where the principle would genuinely fail:** if the number of continuations varied with the earlier choice. *(E.g. "pick a letter, then pick a different letter that comes later in the alphabet" — 25 options after A, but 0 after Z. Then you must sum rather than multiply.)*

---

**Exercise 2 — Combinations, and counting the complement**

A club has 5 women and 7 men. A committee of 5 is chosen.

**(i)** How many committees are possible in total?

**(ii)** How many contain exactly 2 women and 3 men?

**(iii)** How many contain **at least one** woman? Do it two ways.

**(iv)** Verify Pascal's identity for $\binom{7}{3}$ numerically, then explain the identity combinatorially in the language of this club.

**(v)** How many **subsets** of the 12 members are there in total, of any size? Prove it two ways.

> [!example]- Solution
> **(i)** $\binom{12}{5}=\mathbf{792}$
>
> ---
> **(ii)** $\binom52\binom73=10\times35=\mathbf{350}$ *(matching Example 4b)*
>
> ---
> **(iii)** **Method 1 — complement (the right way).** Committees with **no** women use only the 7 men: $\binom75=21$. So
> $$792-21=\mathbf{771}$$
>
> **Method 2 — direct sum over the number of women $k$:**
>
> | $k$ women | $\binom5k$ | $\binom{7}{5-k}$ | Product |
> |---|---|---|---|
> | 1 | 5 | $\binom74=35$ | 175 |
> | 2 | 10 | $\binom73=35$ | 350 |
> | 3 | 10 | $\binom72=21$ | 210 |
> | 4 | 5 | $\binom71=7$ | 35 |
> | 5 | 1 | $\binom70=1$ | 1 |
>
> $$\sum_{k=1}^{5}\binom5k\binom{7}{5-k}=175+350+210+35+1=\mathbf{771}\ ✓$$
>
> > **The complement method took one line; the direct sum took five terms and is easy to botch.** *"At least one"* almost always means **count the complement.**
>
> ---
> **(iv)** $\binom73=35$ and $\binom62+\binom63=15+20=\mathbf{35}$ ✓
>
> **In club language:** count 3-member male subcommittees. **Fix on one particular man, say Ahmed.** Either the subcommittee includes Ahmed — then choose 2 more from the other 6, giving $\binom62=15$ — or it excludes him, and all 3 come from the other 6, giving $\binom63=20$. **The two cases are disjoint and cover everything, so they sum to $\binom73$.**
>
> ---
> **(v)** **Method 1 — binomial theorem.** $\displaystyle\sum_{k=0}^{12}\binom{12}{k}=(1+1)^{12}=2^{12}=\mathbf{4096}$
>
> **Method 2 — bijection.** Each member is in or out: 2 choices each, independently, so $2^{12}=4096$ binary strings, each corresponding to exactly one subset.
>
> **Non-empty subsets: $4096-1=\mathbf{4095}$.**
>
> > **Method 2 is the explanation; Method 1 is the verification.** They count the same objects, which is *why* the identity $\sum_k\binom nk=2^n$ holds.

---

**Exercise 3 — Permutations with repeats, and the labelled/unlabelled trap**

**(i)** How many distinct letter arrangements of **MISSISSIPPI**?

**(ii)** How many of **STATISTICS**?

**(iii)** 12 students are divided into a Python group of 5, an R group of 4, and a SQL group of 3. How many divisions?

**(iv)** 12 students divide into three project teams of 4, with the teams doing identical work and having no names. How many divisions?

**(v)** 12 students divide into groups of 5, 4 and 3, again with no names attached. **How many divisions now?** Explain carefully why the answer differs from (iv) in structure.

> [!example]- Solution
> **(i)** MISSISSIPPI has 11 letters: **M**×1, **I**×4, **S**×4, **P**×2.
> $$\frac{11!}{1!\,4!\,4!\,2!}=\frac{39{,}916{,}800}{1\times24\times24\times2}=\frac{39{,}916{,}800}{1152}=\mathbf{34{,}650}$$
>
> ---
> **(ii)** STATISTICS has 10 letters: **S**×3, **T**×3, **A**×1, **I**×2, **C**×1.
> $$\frac{10!}{3!\,3!\,1!\,2!\,1!}=\frac{3{,}628{,}800}{6\times6\times1\times2\times1}=\frac{3{,}628{,}800}{72}=\mathbf{50{,}400}$$
>
> ---
> **(iii)** **Labelled groups of distinct sizes:**
> $$\binom{12}{5,4,3}=\frac{12!}{5!\,4!\,3!}=\frac{479{,}001{,}600}{120\times24\times6}=\frac{479{,}001{,}600}{17{,}280}=\mathbf{27{,}720}$$
>
> ---
> **(iv)** Labelled first: $\dfrac{12!}{4!\,4!\,4!}=\dfrac{479{,}001{,}600}{13{,}824}=34{,}650$. **All three groups have the same size and no names, so each division has been counted $3!=6$ times:**
> $$\frac{34{,}650}{3!}=\mathbf{5775}$$
>
> ---
> **(v)** **Still $\mathbf{27{,}720}$ — no division is needed.**
>
> > **This is the point of the exercise.** In (iv) the correction was necessary because **permuting the three groups produced a genuinely different labelling of the same division.** Here the groups have **distinct sizes (5, 4, 3), so they are already distinguishable by size alone** — there is no name to strip away. The group of 5 can never be confused with the group of 3.
>
> **The general rule:**
> $$\text{divide by } \prod_j k_j! \quad\text{where } k_j = \text{the number of groups sharing size } j$$
>
> **Check it against the chapter:** Example 5a's groups are 5, 2, 3 — all distinct, no division (2520). Example 5c's are 5 and 5 — two of equal size, divide by $2!$ (126). Example 5d's initial pairing has four groups of size 2, divide by $4!$. ✓ **All three follow the one rule.**

---

**Exercise 4 — Integer solutions, with constraints**

Consider $x_1+x_2+x_3+x_4+x_5=12$ over the integers.

**(i)** How many **nonnegative** solutions?

**(ii)** How many **positive** solutions?

**(iii)** How many solutions with $x_i\ge2$ for every $i$?

**(iv)** How many solutions with $x_1\ge3$, $x_2\ge1$ and the rest $\ge0$?

**(v)** A vending machine takes 12 identical \$1 coins distributed among 5 slots. **Explain why this is the same problem**, and state what would change if the coins were distinguishable (e.g. each bore a serial number).

> [!example]- Solution
> **(i)** Proposition 6.2 with $n=12$, $r=5$:
> $$\binom{12+5-1}{5-1}=\binom{16}{4}=\mathbf{1820}$$
>
> ---
> **(ii)** Proposition 6.1:
> $$\binom{12-1}{5-1}=\binom{11}{4}=\mathbf{330}$$
>
> ---
> **(iii)** **Shift:** let $y_i=x_i-1$, so $y_i\ge1$ becomes $y_i\ge1$… more directly, let $y_i=x_i-1\ge1$. Then $\sum y_i=12-5=7$ with all $y_i\ge1$ — **positive** solutions of a total of 7 in 5 variables:
> $$\binom{7-1}{5-1}=\binom{6}{4}=\mathbf{15}$$
>
> *(Sanity check: with all five parts at least 2, the minimum total is 10, leaving only 2 units of slack to distribute among 5 parts — $\binom{2+5-1}{4}=\binom64=15$ ✓, same answer by the nonnegative route.)*
>
> ---
> **(iv)** **Shift only the constrained variables.** Let $y_1=x_1-3\ge0$ and $y_2=x_2-1\ge0$, leaving $x_3,x_4,x_5\ge0$. The total drops by $3+1=4$:
> $$y_1+y_2+x_3+x_4+x_5=8, \qquad\text{all}\ \ge0$$
> $$\binom{8+5-1}{4}=\binom{12}{4}=\mathbf{495}$$
>
> **Note the method's generality: shift each variable by its own lower bound and reduce the total by the sum of the bounds.** Different bounds cause no extra difficulty.
>
> ---
> **(v)** **It is the same problem because the coins are *identical*.** An outcome is fully described by *how many* coins each slot receives — a vector $(x_1,\dots,x_5)$ of nonnegative integers summing to 12. **Answer: $\binom{16}{4}=1820$.**
>
> **If the coins were distinguishable, the answer would be $\mathbf{5^{12}=244{,}140{,}625}$** — each of the 12 distinct coins independently chooses one of 5 slots.
>
> > **This is the deepest distinction in the chapter, and §6 exists to handle one side of it:**
> >
> > | Objects | Boxes | Count |
> > |---|---|---|
> > | **Distinguishable** | Distinguishable | $r^n$ |
> > | **Identical** | Distinguishable | $\binom{n+r-1}{r-1}$ ← **§6** |
> >
> > **The gap is enormous — 1820 versus 244 million.** Deciding whether your objects are genuinely interchangeable is not a detail; **it changes the answer by five orders of magnitude.**
> >
> > *(Ross's fish are identical: the catch is described by counts per species, not by which individual fish was landed.)*

---

**Exercise 5 — The antenna problem, end to end**

A communication system has $n=12$ antennas in a line, of which $m=4$ are defective. All defectives are indistinguishable, as are all functionals. The system is **functional** iff no two defectives are adjacent.

**(i)** How many orderings are there in total?

**(ii)** How many are functional? Use the gap-selection argument of Example 4c.

**(iii)** What is the probability the system is functional?

**(iv)** Re-derive (ii) by the integer-equation method of Example 6d, and confirm the two agree.

**(v)** Now require **at least 2** functional antennas between any two defectives. How many orderings qualify? **Why can't the Example 4c argument be adapted as easily?**

**(vi)** Verify the general formula against Ross's opening case $n=4$, $m=2$.

> [!example]- Solution
> **(i)** Choose which 4 of the 12 positions hold the defectives:
> $$\binom{12}{4}=\mathbf{495}$$
>
> ---
> **(ii)** Line up the $n-m=8$ functional antennas, creating $8+1=9$ gaps. **Choose 4 gaps to receive one defective each:**
> $$\binom{n-m+1}{m}=\binom{9}{4}=\mathbf{126}$$
>
> ---
> **(iii)** All $\binom{12}{4}$ orderings are equally likely, so
> $$P(\text{functional})=\frac{126}{495}=\frac{14}{55}\approx\mathbf{0.2545}$$
>
> ---
> **(iv)** Let $x_1$ = functionals before the first defective, $x_2,\dots,x_4$ = functionals in the three internal gaps, $x_5$ = functionals after the last. Then
> $$x_1+x_2+x_3+x_4+x_5=8, \qquad x_1,x_5\ge0,\quad x_2,x_3,x_4\ge1$$
> Substitute $y_1=x_1+1$, $y_i=x_i$ for $i=2,3,4$, $y_5=x_5+1$ to make all parts positive; the total becomes $8+2=10$:
> $$y_1+\cdots+y_5=10,\quad\text{all }y_i\ge1 \quad\Longrightarrow\quad \binom{10-1}{5-1}=\binom94=\mathbf{126}\ ✓$$
> **Agrees with (ii)** — and matches the general formula $\binom{n-m+1}{m}$.
>
> ---
> **(v)** Require $x_i\ge2$ for the three internal gaps, still $x_1,x_5\ge0$, total 8. **Subtract the minimum $2\times3=6$ from the total:**
> $$\binom{8-6+5-1}{5-1}=\binom{6}{4}=\mathbf{15}$$
> matching the general formula $\binom{n-2m+2}{m}=\binom{12-8+2}{4}=\binom64=15$ ✓.
>
> *(Probability: $15/495=1/33\approx0.030$ — a much harsher requirement.)*
>
> **Why Example 4c's argument does not adapt easily:** the gap-selection argument works because *"at most one defective per gap"* is exactly *"choose which gaps"* — **a plain selection with no arithmetic left over.** Requiring **two or more** functionals between defectives is a constraint on **how many items each gap holds**, not on which gaps are used. **There is nothing left to simply choose.**
>
> > **The integer-equation method absorbs any lower bound by a shift, so it handles the whole family $\ge0,\ \ge1,\ \ge2,\dots$ with the same three lines. That generality is the reason §6 is worth learning even though §4 answered the original question more elegantly.**
>
> ---
> **(vi)** $n=4$, $m=2$:
> $$\frac{\binom{n-m+1}{m}}{\binom nm}=\frac{\binom32}{\binom42}=\frac{3}{6}=\mathbf{\tfrac12}$$
> **Exactly the answer obtained by listing all six configurations on the chapter's first page** — $0110,\ 0101,\ 1010$ functional; $0011,\ 1001,\ 1100$ not. ✓
>
> > **A formula that reproduces a hand-enumerated case is a formula you can trust. Always test a general result on the smallest case you can list.**

---

## 📝 Summary

- **This chapter is pure counting, and it comes first because** when outcomes are equally likely, $P(E)$ reduces to a ratio of two counts. **The antenna problem is solved three separate ways to make the point.**
- **Basic principle of counting:** $m$ outcomes then $n$ outcomes gives $mn$; generalised to $r$ stages, $n_1n_2\cdots n_r$. **The requirement is that the *number* of continuations is constant, not that the options are identical** — which is why sampling without replacement still obeys it.
- **Permutations:** $n!$ orderings of $n$ distinct objects, with $0!=1$ by convention. **With repeats**, $\dfrac{n!}{n_1!\cdots n_r!}$ — derived by the **overcount-then-divide** pattern that recurs throughout the chapter.
- **Combinations:** $\binom nr=\dfrac{n!}{(n-r)!\,r!}$ counts unordered groups of size $r$, equivalently subsets of size $r$; $\binom nr=0$ when $r>n$ or $r<0$.
- **Pascal's identity** $\binom nr=\binom{n-1}{r-1}+\binom{n-1}{r}$ is proved by **conditioning on whether one fixed object is in the group** — the discrete ancestor of the conditioning arguments of [[03 - Conditional Probability and Independence|ch. 03]].
- **Binomial theorem:** $(x+y)^n=\sum_k\binom nk x^ky^{n-k}$. **The combinatorial proof explains why the coefficient is $\binom nk$ — choosing which factors contribute their $x$ is literally the same act as choosing a subset.** Setting $x=y=1$ gives $\sum_k\binom nk=2^n$, the number of subsets of an $n$-set.
- **Multinomial coefficient:** $\binom{n}{n_1,\dots,n_r}=\dfrac{n!}{n_1!\cdots n_r!}$ divides $n$ distinct objects into $r$ **labelled** groups. **It is numerically the same formula as permutations-with-repeats, and the bijection between the two problems is exact, not coincidental.**
- **Labelled vs unlabelled groups is the chapter's most-missed distinction.** Examples 5b (252) and 5c (126) differ by exactly $2!$. **Divide by $k_j!$ for each set of $k_j$ groups sharing the same size** — groups of distinct sizes need no correction.
- **Integer solutions (stars and bars):** $x_1+\cdots+x_r=n$ has $\binom{n-1}{r-1}$ **positive** solutions and $\binom{n+r-1}{r-1}$ **nonnegative** ones. **Any lower bound $x_i\ge c_i$ is handled by shifting** ($y_i=x_i-c_i$) and reducing the total by $\sum c_i$; upper bounds are *not* — they need inclusion–exclusion.
- **The deepest distinction in the chapter is whether the objects are distinguishable.** Distributing $n$ objects into $r$ boxes gives $r^n$ if the objects are distinct and $\binom{n+r-1}{r-1}$ if they are identical. **For 12 objects and 5 boxes, that is 244 million versus 1820.**

---

## ⚠️ Important Notes

> [!warning] Ask two questions before writing anything down
> $$\textbf{1. Does order matter?} \qquad\qquad \textbf{2. Are the objects distinguishable?}$$
>
> | Order matters | Objects distinct | Formula |
> |---|---|---|
> | ✅ | ✅ | $n!$ or $\dfrac{n!}{(n-r)!}$ (arrangements of $r$ from $n$) |
> | ✅ | ❌ (repeats) | $\dfrac{n!}{n_1!\cdots n_r!}$ |
> | ❌ | ✅ | $\dbinom nr$ |
> | ❌ | ❌ | $\dbinom{n+r-1}{r-1}$ (stars and bars) |
>
> **Almost every error in this chapter is answering one of these two questions wrongly, not misremembering a formula.**

> [!warning] Labelled or unlabelled? The factor you will forget
> **Example 5b:** team A and team B of 5 each → $\dfrac{10!}{5!\,5!}=252$
> **Example 5c:** two unnamed teams of 5 → $\dfrac{252}{2!}=126$
>
> **The test: does swapping two groups give a different outcome?** If not, divide by $k!$ for each collection of $k$ **equal-sized** groups.
>
> **The trap within the trap:** groups of **different** sizes need **no** correction even when unnamed — they are distinguishable by size. *(Exercise 3(iv) vs 3(v): three groups of 4 need $\div3!$; groups of 5, 4, 3 do not.)*

> [!warning] "At least one" means count the complement
> **Exercise 2(iii): 771 committees contain at least one woman.** By complement: $792-21$, one line. By direct summation: five terms, each a product of two binomial coefficients, with ample opportunity for arithmetic slips.
>
> **The same instinct applies to "at least one success," "not all the same," and "at least one match"** — all standard probability questions from [[02 - Axioms of Probability|ch. 02]] onward. **Whenever a condition says *at least*, first ask what *none* looks like.**

> [!warning] Two proofs are better than one, and bijections beat algebra
> Ross proves the binomial theorem twice, derives the multinomial coefficient twice, and solves the antenna problem twice. **This is deliberate.**
>
> - **The bijective/combinatorial argument tells you *why*** — subsets ↔ binary strings, tournament results ↔ permutations, group divisions ↔ permutations-with-repeats
> - **The algebraic argument tells you *that*** — useful for verification, useless for intuition
>
> **A clean answer ($2^n$, $n!$, $\binom nk$) almost always signals that a bijection exists.** Finding it is usually easier than the algebra, and it generalises where the algebra will not.

> [!warning] Sampling without replacement still obeys the basic principle
> A common worry: *"but the options change after each draw, so surely the principle doesn't apply?"*
>
> **The principle requires only that the *number* of continuations be the same for each earlier outcome.** After any first letter, exactly 25 remain — **which letter is irrelevant.** That is why $26\times25\times10\times9\times8\times7\times6$ is legitimate (Exercise 1(ii)).
>
> **It genuinely fails when the *count* varies with the earlier choice** — then you must condition and sum rather than multiply. **This is precisely the situation [[03 - Conditional Probability and Independence|ch. 03]] is built to handle.**

> [!warning] Shifting handles lower bounds; it does **not** handle upper bounds
> **$x_i\ge c_i$:** substitute $y_i=x_i-c_i$, reduce the total by $\sum c_i$, apply Proposition 6.2. **Any combination of different lower bounds works** (Exercise 4(iv)).
>
> **$x_i\le c_i$:** the trick fails — there is no substitution that turns a ceiling into a free variable. **You must subtract the violating cases using inclusion–exclusion** ([[02 - Axioms of Probability|ch. 02]] §4), which gets messy fast with several bounds.
>
> **Recognising which kind of constraint you have saves a great deal of wasted effort.**

> [!warning] $\binom nr = 0$ for $r>n$ is a convention that earns its keep
> It lets you write $\sum_{k}\binom nk\binom{m}{r-k}$ without fussing over the summation limits — impossible terms simply contribute zero. **Exercise 2(iii) Method 2 relies on this.** *(The identity being used there, $\sum_k\binom nk\binom{m}{r-k}=\binom{n+m}{r}$, is **Vandermonde's identity** — Ross develops it in the theoretical exercises.)*

> [!note] Cross-subject connections
> - [[Discrete Mathematics/contents/00-Index|Discrete Mathematics]] — **near-total overlap.** Counting, the pigeonhole principle, inclusion–exclusion and generating functions are developed there with more proof detail; this chapter is the applied subset probability needs.
> - [[02 - Axioms of Probability|Ch. 02]] — **where the counting cashes out.** The equally-likely-outcomes model turns every result here into a probability, and inclusion–exclusion generalises the "count the complement" move.
> - [[04 - Random Variables|Ch. 04]] — **$\binom nk$ is the binomial PMF's coefficient**, for exactly the reason established in §4: it counts which $k$ of $n$ trials succeeded. The multinomial coefficient plays the same role for the multinomial distribution.
> - [[06 - Jointly Distributed Random Variables|Ch. 06]] — stars and bars counts the states of exchangeable systems; **the hypergeometric distribution is a ratio of binomial coefficients.**
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **$\binom nk$ is the size of the hypothesis space** in many combinatorial learning bounds, and $2^n$ (Example 4e) is the number of possible labellings that shattering arguments count.
> - [[Data Structures and Algorithms/contents/00-Index|Data Structures and Algorithms]] — $n!$ and $2^n$ are the running times that make brute-force search infeasible; **this chapter is where those numbers come from.**

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **Figures are images and cannot be extracted:**
> - **Figure 1.1** ("No consecutive defectives") — only fragments survive extraction: `^ 1 ^ 1 ^ 1 . . . ^ 1 ^ 1 ^`, `1 5 functional`, `^ 5 place for at most one defective`. **The `5` characters are mangled `=` signs** (the legend reads "1 = functional" and "^ = place for at most one defective"). **The diagram is reconstructed in §4a from the surrounding prose, which describes it fully.**
> - **Figure 1.2** ("Number of positive solutions") — extracts as `0 ^ 0 ^ 0 ^ . . . ^ 0 ^ 0`, `n objects 0`, `Choose r 2 1 of the spaces ^`. **Here `2` is a mangled minus sign** ("choose $r-1$ of the spaces"). **Reconstructed in §6a.**
>
> **Notation mangled by the PDF's stacked layout** (all reconstructed by hand and cross-checked against the worked examples):
> - **Binomial coefficients extract across four lines** — $\binom{n}{r}$ becomes `(`, `n`, `r`, `)`. Every occurrence has been re-paired with its correct arguments by following the surrounding sentence.
> - **Fractions extract as numerator-newline-denominator**, so $\frac{10!}{4!\,3!\,2!\,1!}$ appears as two separate lines. **Every formula has been verified against the numeric answer the text gives for it.**
> - **`≤` extracts as `…`** — `f o rr … n` is "for $r\le n$", and `1 … r … n` in Pascal's identity is $1\le r\le n$. **`≥` extracts as `Ú`.** *(By contrast `<` and `>` survive intact — unlike the extraction bug in [[Time-series Analysis/contents/00-Index|Time-series Analysis]].)*
> - **Emphasised text loses word spacing**, e.g. `t h e r e i s a t o t a l o f`. Cosmetic, but it makes text search over the extraction unreliable.
> - **Superscripts detach from their base**: `2 n` for $2^n$, `x 1y0` for $x^1y^0$, `2 k matches` for $2^k$ matches. **Every exponent has been restored from context.**
>
> **Verification performed:** every numeric answer in Examples 2a–6d was recomputed independently — 30, 120, 362880, 3628800, 17280, 6912, 60, 12600, 1260, 1140, 350, 300, 2520, 252, 126, 1680, 40320, 286, 4, 1771, 10626 — **and all agree with the text.** No arithmetic errors were found in this chapter.
>
> **One genuine gap in the exposition, not the extraction:** Ross states the multinomial theorem and says *"the proof is left as an exercise."* **It is never proved in the chapter.** The proof follows the combinatorial argument for the binomial theorem almost verbatim (count how many of the $r^n$ terms have $n_i$ copies of $x_i$), and I have indicated the route in §5a rather than leaving it unremarked.

#probability #combinatorics #counting #binomial-coefficient
