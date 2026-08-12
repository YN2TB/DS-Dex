---
subject: Discrete Mathematics
chapter: 6
tags: [ds, discrete-mathematics, counting, combinatorics, permutations, combinations, binomial-theorem, pigeonhole, probability]
source: "Johnsonbaugh, *Discrete Mathematics* 8e, ch. 6 (book pp. 255–326)"
---

# Counting Methods and the Pigeonhole Principle

Counting is the most reused chapter in the subject, and several earlier notes have been quietly borrowing from it. [[01 - Sets and Logic|Ch. 01]] used $|X\times Y|=|X|\cdot|Y|$ and $|\mathcal P(X)|=2^{|X|}$ before either was justified. [[02 - Proofs and Mathematical Induction|Ch. 02]] proved the second by induction and called it "the template for every counting argument in ch. 06". [[03 - Functions, Sequences and Relations|Ch. 03]] observed that **a bijection between finite sets proves they have the same size**, and that **hash collisions are guaranteed** — by the principle §7 finally states. [[04 - Algorithms and Their Analysis|Ch. 04]] needs $\lg(n!)=\Theta(n\lg n)$ for a lower bound proved in [[09 - Trees|ch. 09]].

All of it lands here. The chapter has two halves that feel unrelated and are not: **§§1–5 count things exactly**, and **§7 proves that something must exist without counting it at all.**

## 📘 Main Knowledge

### 1. The two principles everything is built from

> [!note] Multiplication Principle
> If an activity can be performed in $t$ successive steps, with $n_1$ ways to do step 1, $n_2$ ways to do step 2, …, $n_t$ ways to do step $t$, then the number of distinct ways to perform the activity is
> $$n_1\cdot n_2\cdots n_t .$$

> [!note] Addition Principle
> If $X_1,\dots,X_t$ are **pairwise disjoint** sets with $|X_i|=n_i$, then
> $$|X_1\cup\cdots\cup X_t|=n_1+n_2+\cdots+n_t .$$

**Multiply for successive steps; add for disjoint alternatives.** Johnsonbaugh's mnemonic: at a lunch counter with 3 main courses and 4 beverages, there are $3\cdot4=12$ *dinners* (choose a course **and** a beverage) but $3+4=7$ *items* (a course **or** a beverage). Which principle applies depends on whether you are making one compound choice or classifying into disjoint cases.

> [!warning] The Addition Principle needs *pairwise disjoint*, and the Multiplication Principle needs the counts to be *independent of earlier choices*
> Both hypotheses fail quietly.
>
> If the sets overlap, adding **double-counts** the overlap — that is what §2's Inclusion–Exclusion repairs.
>
> And the multiplication principle needs $n_i$ to be the same *whatever was chosen before*. Counting strings of length 4 from `ABCDE` **without** repetition works ($5\cdot4\cdot3\cdot2$) because each step always has one fewer option regardless of *which* letters were used. But "choose a 2-letter string with distinct letters, then a letter not yet used" would need care if the count depended on the specific earlier picks.

> [!example]- Worked examples (all verified)
> **Strings of length 4 from `ABCDE`.**
> - *Repetitions allowed:* four independent choices from five letters, $5^4=\mathbf{625}$.
> - *Repetitions not allowed:* $5\cdot4\cdot3\cdot2=P(5,4)=\mathbf{120}$.
> - *Not beginning with `B`, no repetitions:* first letter in 4 ways, then $4\cdot3\cdot2$: total $4\cdot4\cdot3\cdot2=\mathbf{96}$. **Or by subtraction:** $120-P(4,3)=120-24=96$ ✓ — the same answer two ways, which is the standard sanity check.
>
> **Eight-bit strings beginning `101` or `111`.** Each is $2^5=32$ strings, and the two sets are **disjoint** (a string cannot start with both), so the Addition Principle gives $32+32=\mathbf{64}$.
>
> **A set with $n$ elements has $2^n$ subsets** (J Example 6.1.5). Build a subset in $n$ successive steps: for each $x_i$, *include it or not* — two ways each, independent of the others. By the Multiplication Principle, $2\cdot2\cdots2=2^n$. **This is the same fact [[02 - Proofs and Mathematical Induction|ch. 02]] proved by induction, and the multiplication argument is the more illuminating one** — it shows *why* the answer is a power of two.
>
> **How many reflexive relations are there on an $n$-element set?** (J Example 6.1.7.) A relation on $X$ is an $n\times n$ $0/1$ matrix ([[03 - Functions, Sequences and Relations|ch. 03]] §7); reflexivity forces the $n$ diagonal entries to $1$ and leaves the other $n^2-n$ entries free. So $2^{n^2-n}$.

### 2. Inclusion–Exclusion

When the sets overlap, addition over-counts.

> [!note] Theorem — Inclusion–Exclusion for two sets
> $$|X\cup Y|=|X|+|Y|-|X\cap Y|$$

For three sets:
$$|X\cup Y\cup Z|=|X|+|Y|+|Z|-|X\cap Y|-|X\cap Z|-|Y\cap Z|+|X\cap Y\cap Z|.$$

**The alternating signs have a reason:** subtracting the three pairwise intersections removes the triple intersection three times, having added it three times, so it must be added back once. In general the signs alternate with the number of sets intersected. [[01 - Sets and Logic|Ch. 01]] Exercise 3 already used the three-set version; this is where it comes from.

### 3. Permutations and combinations

> [!note] Definitions and formulas
> A **permutation** of $n$ distinct elements is an ordering of all of them; an **$r$-permutation** is an ordering of an $r$-element subset. An **$r$-combination** is an *unordered* $r$-element subset.
>
> | | count | formula |
> |---|---|---|
> | permutations of $n$ | $n!$ | |
> | $r$-permutations | $P(n,r)$ | $n(n-1)\cdots(n-r+1)=\dfrac{n!}{(n-r)!}$ |
> | $r$-combinations | $C(n,r)=\dbinom nr$ | $\dfrac{P(n,r)}{r!}=\dfrac{n!}{r!\,(n-r)!}$ |

**Ordered or not — that is the only question to ask**, and getting it wrong is the commonest error in the chapter. A committee of 3 from 6 people is $C(6,3)=20$; *president, secretary and treasurer* from 6 is $P(6,3)=120$, because now the order matters. The ratio is exactly $3!=6$.

**Where $C(n,r)=P(n,r)/r!$ comes from** is worth seeing, because it is a *double count*: build an $r$-permutation in two steps — choose the $r$-element subset ($C(n,r)$ ways), then order it ($r!$ ways). By the Multiplication Principle,
$$P(n,r)=C(n,r)\cdot r! .$$

> [!note] The same fact via equivalence classes
> Johnsonbaugh gives a second derivation that ties the chapter to [[03 - Functions, Sequences and Relations|ch. 03]]. Define a relation on the set $S$ of $r$-permutations: $p_1\mathrel{R}p_2$ if they use *the same $r$ elements* in some order. This is an **equivalence relation**, its classes are exactly the $r$-combinations, and every class has exactly $r!$ members. By ch. 03's counting corollary ($|X|/r$ classes when each has $r$ elements),
> $$C(n,r)=\frac{|S|}{r!}=\frac{P(n,r)}{r!}.$$
> **"Divide by the symmetries" is the general move**, and this is the cleanest instance of it. Whenever a count over-counts each object equally often, divide.

### 4. Generalized permutations and combinations

Two variations cover most real problems.

> [!note] Permutations of a multiset
> If a sequence of $n$ items has $n_1$ identical objects of type 1, …, $n_t$ of type $t$ (so $n_1+\cdots+n_t=n$), the number of **distinguishable orderings** is
> $$\frac{n!}{n_1!\,n_2!\cdots n_t!}.$$

**Same "divide by the symmetries" idea:** $n!$ orderings of the items treated as distinct, but each distinguishable arrangement is counted $n_1!\cdots n_t!$ times, once for each way of permuting identical objects among themselves.

*Verified:* `MISSISSIPPI` has 11 letters with M$\times1$, I$\times4$, S$\times4$, P$\times2$, giving
$$\frac{11!}{1!\,4!\,4!\,2!}=\mathbf{34{,}650},$$
confirmed by brute-force enumeration of distinct permutations.

> [!note] Combinations with repetition ("stars and bars")
> The number of **unordered** $k$-element selections from $t$ types, **repetitions allowed**, is
> $$C(k+t-1,\ k).$$

**The bijection that proves it** is the reason to remember it rather than the formula. Represent a selection as $k$ stars and $t-1$ bars separating the types: `**|*||***` means 2 of type 1, 1 of type 2, 0 of type 3, 3 of type 4. Every arrangement of $k$ stars and $t-1$ bars is one selection and vice versa — a **bijection** — so the count is the number of ways to choose which $k$ of the $k+t-1$ positions are stars.

*Verified:* choosing 6 doughnuts from 4 types gives $C(9,6)=C(9,3)=\mathbf{84}$, confirmed by enumerating all solutions of $a+b+c+d=6$ in nonnegative integers.

> [!warning] The four cases, and how to tell them apart
> | | order matters | order does not matter |
> |---|---|---|
> | **no repetition** | $P(n,r)=\dfrac{n!}{(n-r)!}$ | $C(n,r)=\dfrac{n!}{r!(n-r)!}$ |
> | **repetition allowed** | $n^r$ | $C(r+n-1,\ r)$ |
>
> **Ask two questions in this order: (1) does order matter? (2) may items repeat?** Nearly every counting mistake is answering one of them wrongly, and the four formulas are otherwise easy to confuse. Note that the top-left and bottom-left are the two cases §1 already did by the Multiplication Principle.

### 5. Generating them, in order

Sometimes you need not just the *number* of combinations but the list. Johnsonbaugh gives algorithms producing all $r$-combinations of $\{1,\dots,n\}$ in **lexicographic order** — dictionary order on strings.

The idea: given the current combination $s_1s_2\cdots s_r$ with digits increasing, find the **rightmost** $s_i$ that can be incremented (i.e. $s_i<n-r+i$), increment it, and reset everything to its right to the smallest legal values $s_i+1,s_i+2,\dots$. Starting from $12\cdots r$ and repeating $C(n,r)-1$ times lists them all.

**Correctness is an induction on the output index** — the base case is the first combination $12\cdots r$, and the inductive step shows each output is lexicographically next. This is [[02 - Proofs and Mathematical Induction|ch. 02]] again, and it is worth noticing that the proof of *completeness* is a well-ordering argument: if some combination were never generated, take the least such, and derive a contradiction from its predecessor.

**In practice** you would use `itertools.combinations(range(1, n+1), r)`, which produces exactly this order.

### 6. Discrete probability, briefly

If a sample space $S$ of equally likely outcomes is finite and $E\subseteq S$ is an event,

$$P(E)=\frac{|E|}{|S|}.$$

**So a probability question with equally likely outcomes is *two* counting problems** — count the event, count the space, divide. That is the whole reason counting precedes probability.

> [!note] This section is deliberately short
> Johnsonbaugh's §§6.5–6.6 give about sixteen pages on discrete probability, and both are marked optional. **[[Probability Theory/contents/02 - Axioms of Probability|Probability Theory]] owns this subject properly** — Ross develops the axioms, conditional probability, independence, random variables and expectation at length, and [[Probability Theory/contents/01 - Combinatorial Analysis|its ch. 01]] is the same counting theory as this chapter, in more depth.
>
> What is worth carrying from here: **the equally-likely formula is a counting identity, not a definition of probability** — it applies only when outcomes are equally likely, and deciding whether they are is where most elementary probability errors live.

### 7. Binomial coefficients

> [!note] Theorem — the Binomial Theorem
> For real $a,b$ and positive integer $n$,
> $$(a+b)^n=\sum_{k=0}^{n}C(n,k)\,a^{n-k}b^k .$$

**The proof is a counting argument, and it explains the name.** Expanding
$$(a+b)^n=\underbrace{(a+b)(a+b)\cdots(a+b)}_{n\text{ factors}}$$
means choosing $a$ or $b$ from each factor and summing all $2^n$ products. A product equals $a^{n-k}b^k$ exactly when $b$ was chosen from $k$ of the factors — and there are $C(n,k)$ ways to choose which $k$. **So the binomial coefficient is called that because it *is* the coefficient in a binomial expansion**, and the "choose" interpretation is the primary one.

For $n=3$, listing all eight selections gives $aaa+aab+aba+abb+baa+bab+bba+bbb=a^3+3a^2b+3ab^2+b^3$ — and the three copies of $a^2b$ are the $C(3,1)=3$ ways to pick which factor supplied the $b$.

**The identities worth knowing** (all verified):

| Identity | Statement | Combinatorial reading |
|---|---|---|
| **Symmetry** | $C(n,k)=C(n,n-k)$ | choosing $k$ to include = choosing $n-k$ to exclude |
| **Pascal** | $C(n,k)=C(n-1,k-1)+C(n-1,k)$ | fix an element: either it is in the subset or it is not |
| **Row sum** | $\sum_{k=0}^n C(n,k)=2^n$ | count all subsets by size — and total them ($a=b=1$) |
| **Alternating sum** | $\sum_{k=0}^n(-1)^kC(n,k)=0$ | $a=1,b=-1$; equally many even- and odd-sized subsets |
| **Weighted sum** | $\sum_k k\,C(n,k)=n2^{n-1}$ | count (subset, chosen element) pairs two ways |

**Pascal's identity is the recurrence that builds Pascal's triangle**, and its proof is the archetypal combinatorial argument: to choose $k$ from $n$, fix one element $x$; either $x$ is chosen (then pick $k-1$ from the remaining $n-1$) or it is not (pick $k$ from $n-1$). The two cases are disjoint and exhaust everything, so add — the Addition Principle. **Notice there is no algebra at all.** That style — count one set two different ways, or split by a binary choice — proves most binomial identities faster than manipulation does.

### 8. The Pigeonhole Principle

Everything above counts exactly. This does something different: it proves an object **exists** without producing it or counting how many there are.

> [!note] Pigeonhole Principle — three forms
> **First form.** If $n$ pigeons fly into $k$ pigeonholes and $k<n$, some pigeonhole contains **at least two** pigeons.
>
> **Second form.** If $f:X\to Y$ with $X,Y$ finite and $|X|>|Y|$, then $f$ is **not one-to-one**.
>
> **Third form (generalized).** If $n$ pigeons fly into $k$ pigeonholes, some pigeonhole contains **at least $\lceil n/k\rceil$** pigeons.

*Proof of the first form.* By contradiction: if every hole had at most one pigeon, there would be at most $k<n$ pigeons. $\blacksquare$

**The three forms are one fact in three costumes**, and the second is the one that connects to everything earlier: it is precisely the statement that **no injection exists from a larger finite set into a smaller one.** That is why [[03 - Functions, Sequences and Relations|ch. 03]]'s hash functions must collide — 12 keys into 11 cells cannot be injective — and why any hash table needs a collision policy regardless of how clever the hash is.

> [!warning] Pigeonhole is purely existential
> It tells you a pigeonhole with two pigeons **exists**. It does not say **which** one, and it does not say **how many** such holes there are. Johnsonbaugh is explicit about this, and it matters: a pigeonhole proof can establish that a duplicate exists in a data set of size $n>k$ while giving no method to find it. **Compare [[02 - Proofs and Mathematical Induction|ch. 02]] §5's distinction between constructive and nonconstructive existence proofs — pigeonhole is the nonconstructive kind.**

**The whole skill is choosing the pigeons and the holes.** That choice is the entire content of a pigeonhole proof, and it is rarely the obvious one.

> [!example]- Worked example (J Example 6.8.1) and its restatement
> Ten people have first names Alice, Bernard, Charles and last names Lee, McDuff, Ng. Show two share a full name.
>
> **Pigeons: the 10 people. Holes: the $3\times3=9$ possible full names.** Since $10>9$, some name is shared. $\blacksquare$
>
> **Every pigeonhole proof can be rewritten as a proof by contradiction** — unsurprisingly, since that is how the principle itself was proved. Here: suppose no two share a full name; then there are at most 9 people, contradicting 10. **Neither version is better; use whichever you find clearer.**

## ✏️ Exercises

**1. (Multiplication, addition, inclusion–exclusion.)** Using the letters `ABCDEFG`: (a) how many strings of length 3 are there with repetitions allowed? without? (b) How many strings of length 3 without repetitions begin with `A` or end with `G`? (c) In a class of 40 students, 22 take statistics, 19 take programming, and 9 take both. How many take neither?

> [!example]- Solution
> **(a)** With repetitions: three independent choices from seven letters, $7^3=\mathbf{343}$.
> Without: $7\cdot6\cdot5=P(7,3)=\mathbf{210}$.
>
> **(b)** Let $X$ = strings beginning with `A`, $Y$ = strings ending with `G` (both length 3, no repetitions).
> - $|X|$: first letter fixed, then $6\cdot5=30$, so $|X|=30$.
> - $|Y|$: last letter fixed, then $6\cdot5=30$, so $|Y|=30$.
> - $|X\cap Y|$: both ends fixed, middle letter any of the remaining 5, so $|X\cap Y|=5$.
>
> **The sets overlap** (e.g. `ABG` is in both), so the Addition Principle does not apply — use Inclusion–Exclusion:
> $$|X\cup Y|=30+30-5=\mathbf{55}.$$
> *(Adding naively would give 60, double-counting the five strings of the form `A?G`.)*
>
> **(c)** $|S\cup P|=22+19-9=32$, so those taking neither number $40-32=\mathbf8$.
>
> **The check worth doing:** the four disjoint categories must partition the class — statistics only $22-9=13$, programming only $19-9=10$, both $9$, neither $8$, and $13+10+9+8=40$ ✓

**2. (Permutations vs combinations.)** From a club of 12 members: (a) how many ways to choose a committee of 4? (b) How many ways to choose a president, vice-president, secretary and treasurer? (c) What is the ratio of (b) to (a), and why? (d) How many committees of 4 include a specific member Alice? (e) How many 5-card poker hands are there from a 52-card deck?

> [!example]- Solution
> **(a)** Order does not matter, no repetition: $C(12,4)=\dfrac{12!}{4!\,8!}=\mathbf{495}$.
>
> **(b)** Order matters (the four offices are distinct), no repetition: $P(12,4)=12\cdot11\cdot10\cdot9=\mathbf{11{,}880}$.
>
> **(c)** $\dfrac{11880}{495}=\mathbf{24}=4!$
>
> **Because each unordered committee of 4 can be assigned the four offices in $4!=24$ ways.** This is the identity $P(n,r)=C(n,r)\cdot r!$ made concrete, and it is the cleanest way to remember which formula is which: **the ordered count is always $r!$ times the unordered one.**
>
> **(d)** If Alice is in, the remaining 3 members come from the other 11: $C(11,3)=\mathbf{165}$.
>
> *Cross-check with Pascal:* committees **excluding** Alice number $C(11,4)=330$, and $165+330=495=C(12,4)$ ✓ — which is exactly Pascal's identity $C(12,4)=C(11,3)+C(11,4)$, and the split "does the subset contain Alice?" is its proof.
>
> **(e)** $C(52,5)=\mathbf{2{,}598{,}960}$ *(verified)*. Order does not matter — a hand is a set of cards, not a sequence, which is why it is $C$ and not $P$. *(This is the denominator of nearly every poker probability; the numerators are further counting problems, which is §6's point.)*

**3. (Generalized counting.)** (a) How many distinguishable arrangements of the letters of `MISSISSIPPI`? (b) A shop sells 4 kinds of doughnut. How many ways to buy 6 doughnuts? (c) How many ways to buy 6 doughnuts including **at least one** of each kind? (d) How many solutions in nonnegative integers does $x_1+x_2+x_3+x_4=6$ have, and why is this the same as (b)?

> [!example]- Solution
> **(a)** 11 letters: M$\times1$, I$\times4$, S$\times4$, P$\times2$. By the multiset formula
> $$\frac{11!}{1!\,4!\,4!\,2!}=\frac{39916800}{1\cdot24\cdot24\cdot2}=\mathbf{34{,}650}$$
> *(verified by brute-force enumeration of distinct permutations).*
>
> **Why divide:** treating the letters as distinct gives $11!$ orderings, but the four I's can be permuted among themselves in $4!$ ways without changing the visible word — likewise the S's and P's. Each distinguishable arrangement is therefore counted $4!\cdot4!\cdot2!$ times.
>
> **(b)** Unordered, repetitions allowed, $k=6$ from $t=4$ types:
> $$C(k+t-1,k)=C(9,6)=C(9,3)=\mathbf{84}$$
> *(verified by enumeration).* Note $C(9,6)=C(9,3)$ by symmetry — usually easier to compute the smaller one.
>
> **(c)** Give one of each kind away first: that uses 4 doughnuts and leaves 2 to distribute freely among the 4 types. So
> $$C(2+4-1,2)=C(5,2)=\mathbf{10}.$$
> **The technique is standard and worth remembering: a "at least one of each" constraint is removed by pre-allocating the minimum**, reducing to the unconstrained problem with a smaller $k$.
>
> **(d)** $C(9,6)=\mathbf{84}$ — the **same problem**. Let $x_i$ be the number of doughnuts of type $i$; then a purchase *is* a solution of $x_1+x_2+x_3+x_4=6$ with $x_i\ge0$, and conversely.
>
> **This is a bijection, and it is why "stars and bars" is worth learning as a picture rather than a formula.** Write 6 stars and 3 bars: `**|*||***` is the purchase $(2,1,0,3)$. Every arrangement of 6 stars and 3 bars gives exactly one solution, and every solution exactly one arrangement — so the count is the number of ways to choose which 6 of the 9 positions hold stars. **Recognising that two differently-worded problems are the same bijection is most of the skill in this chapter.**

**4. (Binomial coefficients.)** (a) Expand $(a+b)^5$. (b) State and prove Pascal's identity combinatorially. (c) Prove $\sum_{k=0}^n C(n,k)=2^n$ in two ways. (d) Prove $\sum_{k=0}^n k\,C(n,k)=n2^{n-1}$ by a double count.

> [!example]- Solution
> **(a)** Coefficients $C(5,k)$ for $k=0,\dots,5$ are $1,5,10,10,5,1$ *(verified)*:
> $$(a+b)^5=a^5+5a^4b+10a^3b^2+10a^2b^3+5ab^4+b^5 .$$
> Note the palindrome — that is the symmetry $C(n,k)=C(n,n-k)$.
>
> **(b) Pascal's identity:** $C(n,k)=C(n-1,k-1)+C(n-1,k)$ for $1\le k\le n-1$ *(verified for all $n<30$)*.
>
> *Proof.* Count the $k$-element subsets of $\{x_1,\dots,x_n\}$ by splitting on whether they contain $x_n$.
> - **Containing $x_n$:** the other $k-1$ elements come from the remaining $n-1$ — that is $C(n-1,k-1)$ subsets.
> - **Not containing $x_n$:** all $k$ elements come from the remaining $n-1$ — that is $C(n-1,k)$.
>
> The two cases are **disjoint and exhaustive**, so by the Addition Principle the total is $C(n-1,k-1)+C(n-1,k)$. $\blacksquare$
>
> **No algebra was used.** That is the model for combinatorial identities: **split by a binary choice, count each part, add.**
>
> **(c)** *Way 1 — combinatorially.* $\sum_k C(n,k)$ counts all subsets of an $n$-set, grouped by size. But §1 showed there are $2^n$ subsets in total (include-or-exclude each element). Since the size classes are disjoint and exhaustive, the sum equals $2^n$. $\blacksquare$
>
> *Way 2 — algebraically.* Put $a=b=1$ in the Binomial Theorem:
> $$2^n=(1+1)^n=\sum_{k=0}^n C(n,k)1^{n-k}1^k=\sum_{k=0}^n C(n,k).\ \blacksquare$$
> *(Verified at $n=4,6,10$: $16,64,1024$.)* **The same identity twice, from a count and from an algebraic substitution — which is exactly §7's point that algebra and counting are two views of the binomial coefficients.**
>
> *(Aside: $a=1,b=-1$ gives $\sum_k(-1)^kC(n,k)=0$ — equally many even- and odd-sized subsets.)*
>
> **(d)** Count the pairs $(A,x)$ where $A\subseteq\{x_1,\dots,x_n\}$ and $x\in A$ — a subset together with a distinguished element of it.
>
> - **Choose $A$ first.** For each size $k$ there are $C(n,k)$ subsets, each offering $k$ choices of $x$. Total: $\sum_k k\,C(n,k)$.
> - **Choose $x$ first.** Pick $x$ in $n$ ways, then any subset of the *other* $n-1$ elements to accompany it: $2^{n-1}$ ways. Total: $n2^{n-1}$.
>
> Both count the same set of pairs, so
> $$\sum_{k=0}^n k\,C(n,k)=n2^{n-1}.\ \blacksquare$$
> *(Verified at $n=4,6,10$: $32,192,5120$.)*
>
> **This is the double-counting technique in its purest form** — count one collection two ways and equate. It is how most binomial identities are best proved, and it generalises: the same method gave $P(n,r)=C(n,r)r!$ in §3.

**5. (Hard — the Pigeonhole Principle.)** (a) Show that among any 5 integers chosen from $\{1,2,\dots,8\}$, two sum to 9. Is 5 optimal? (b) State the generalized form and apply it: among 45 students assigned one of 7 discussion sections, what can you guarantee? (c) Show that in any group of $n\ge2$ people, two have the same number of acquaintances within the group. (d) Explain what pigeonhole proofs cannot do.

> [!example]- Solution
> **(a) Pigeons: the 5 chosen integers. Holes: the pairs summing to 9**, namely
> $$\{1,8\},\quad\{2,7\},\quad\{3,6\},\quad\{4,5\}$$
> — **four** holes partitioning $\{1,\dots,8\}$. Each chosen integer lies in exactly one pair. With 5 pigeons in 4 holes, some hole receives two — and two integers from the same pair sum to $\mathbf9$. $\blacksquare$
>
> *(Verified exhaustively: of all $C(8,5)=56$ five-element subsets, **none** avoids a pair summing to 9.)*
>
> **Yes, 5 is optimal** — the bound cannot be improved to 4, since $\{1,2,3,4\}$ contains no such pair *(verified; it takes one element from each hole)*. **Optimality is the interesting half of a pigeonhole result, and it is shown by exhibiting an extremal example**, not by more pigeonholing.
>
> **(b) Generalized form:** $n$ pigeons in $k$ holes forces some hole to contain at least $\lceil n/k\rceil$.
>
> With $n=45$ students and $k=7$ sections, $\lceil45/7\rceil=\lceil6.43\rceil=\mathbf7$: **some section has at least 7 students** *(verified)*.
>
> Note what is *not* guaranteed: no section need have 8 (a $7,7,7,6,6,6,6$ split sums to 45), and no *particular* section is identified. **The bound is exactly tight**, which is the usual situation — $\lceil n/k\rceil$ is achieved by the most even distribution.
>
> **(c)** Let the group have $n\ge2$ people. Each person's acquaintance count lies in $\{0,1,\dots,n-1\}$ — that is $n$ possible values for $n$ people, so pigeonhole does **not** immediately apply. **The trick is to show two of the holes cannot both be occupied.**
>
> Suppose someone has $0$ acquaintances and someone else has $n-1$. The person with $n-1$ knows *everyone else*, including the person with $0$ — contradicting that person having no acquaintances. (Acquaintance is symmetric.) **So the values $0$ and $n-1$ cannot both occur.**
>
> Hence the $n$ people take values in a set of at most $n-1$ possibilities, and by pigeonhole **two people have the same acquaintance count**. $\blacksquare$
>
> **This is why the chapter says the skill is choosing the holes.** The naive choice gives $n$ pigeons and $n$ holes and fails; the observation that two holes are mutually exclusive reduces it to $n-1$ and the argument goes through. *(In the language of [[08 - Graph Theory|ch. 08]] this says no finite simple graph has all degrees distinct.)*
>
> **(d) Pigeonhole proofs are purely existential.** Three specific limitations:
> 1. **They do not locate the object.** In (a) we know two of the five integers sum to 9; the proof gives no way to say which without examining them.
> 2. **They do not count.** In (b) at least one section has $\ge7$ students; how many such sections there are is not addressed.
> 3. **They give no construction, hence no algorithm.** This is exactly [[02 - Proofs and Mathematical Induction|ch. 02]] §5's constructive/nonconstructive distinction, and it is the reason a pigeonhole argument can prove a hash collision *must* exist ([[03 - Functions, Sequences and Relations|ch. 03]] §2) while contributing nothing to finding one — the collision-resolution policy is a separate engineering problem.
>
> **What pigeonhole does exceptionally well is prove impossibility.** "No injection from a larger finite set into a smaller one" (second form) settles, in one line, that lossless compression cannot shrink *every* input, that no hash is collision-free, and that a comparison sort cannot beat $\lg(n!)$ — the bound [[09 - Trees|ch. 09]] proves and [[04 - Algorithms and Their Analysis|ch. 04]] needed.

## 📝 Summary

- **Multiply for successive steps; add for disjoint alternatives.** The Multiplication Principle needs each step's count to be **independent of earlier choices**; the Addition Principle needs the sets **pairwise disjoint**.
- **Inclusion–Exclusion** repairs overlap: $|X\cup Y|=|X|+|Y|-|X\cap Y|$, and for three sets the triple intersection is added back because subtracting the three pairs removed it three times.
- **The four core counts.** Ask *(1) does order matter? (2) may items repeat?*
  | | ordered | unordered |
  |---|---|---|
  | no repetition | $P(n,r)=\frac{n!}{(n-r)!}$ | $C(n,r)=\frac{n!}{r!(n-r)!}$ |
  | repetition | $n^r$ | $C(r+n-1,r)$ |
- **$P(n,r)=C(n,r)\cdot r!$** — the ordered count is always $r!$ times the unordered. Equivalently $C(n,r)=P(n,r)/r!$, which is **"divide by the symmetries"**, and which [[03 - Functions, Sequences and Relations|ch. 03]]'s equivalence classes prove directly.
- **Multiset permutations:** $\frac{n!}{n_1!\cdots n_t!}$ — same division-by-symmetry. `MISSISSIPPI` gives $34{,}650$.
- **Stars and bars:** $k$ items from $t$ types unordered with repetition is $C(k+t-1,k)$, **because of a bijection with arrangements of $k$ stars and $t-1$ bars**. "At least one of each" is handled by pre-allocating the minimum.
- **A bijection is the fundamental counting tool** — it proves two sets have the same size, and recognising that two problems are the same bijection is most of the skill here.
- **Discrete probability with equally likely outcomes is $P(E)=|E|/|S|$** — two counting problems. Deferred to [[Probability Theory/contents/02 - Axioms of Probability|Probability Theory]].
- **Binomial Theorem:** $(a+b)^n=\sum_k C(n,k)a^{n-k}b^k$, **proved by counting** which $k$ factors supplied a $b$. That is why the coefficient is "$n$ choose $k$".
- **The identities and their combinatorial readings:** symmetry ($C(n,k)=C(n,n-k)$: include vs exclude); **Pascal** ($C(n,k)=C(n-1,k-1)+C(n-1,k)$: does the subset contain $x_n$?); row sum ($2^n$: all subsets, or $a=b=1$); weighted sum ($n2^{n-1}$: double-count (subset, element) pairs). **Prove identities by double counting, not algebra.**
- **Pigeonhole, three forms:** $n>k$ pigeons in $k$ holes forces a shared hole; **$|X|>|Y|$ forces $f:X\to Y$ to be non-injective**; and generally some hole holds $\ge\lceil n/k\rceil$.
- **The skill is choosing the pigeons and holes** — often after an observation that reduces the number of holes (Exercise 5(c)).
- **Pigeonhole is purely existential:** it does not locate the object, count them, or give an algorithm. **What it does superbly is prove impossibility** — no collision-free hash, no universally shrinking compressor, no comparison sort below $\lg(n!)$.

## ⚠️ Important Notes

1. **Decide "ordered or not" before anything else.** Committee ($C$) versus slate of officers ($P$) is the whole distinction, and the answers differ by a factor of $r!$.
2. **The Addition Principle requires disjointness.** If the cases overlap you must use Inclusion–Exclusion, or you will double-count — Exercise 1(b) gives 60 instead of 55.
3. **The Multiplication Principle requires each step's count to be independent of earlier choices.** If the number of options depends on *which* option was taken before, break into cases and add.
4. **Check a count two ways whenever you can.** Direct count versus complement (total minus the bad cases) is the cheapest sanity check, and it caught nothing in Exercise 1(a) precisely because both gave 96.
5. **"At least one" usually means either pre-allocate the minimum, or count the complement.** For "at least one of each type", give one away first; for "at least one $A$", count the strings with **no** $A$ and subtract.
6. **Use symmetry to compute:** $C(9,6)=C(9,3)$, and the smaller is far easier by hand. Likewise $C(52,5)$ rather than $C(52,47)$.
7. **Prefer double counting to algebra for identities.** Pascal's identity has a two-line combinatorial proof and an ugly algebraic one. If an identity has factorials on both sides, look for the set that both sides count.
8. **$\sum_k C(n,k)=2^n$ is worth internalising in both directions** — as "the total number of subsets" and as $(1+1)^n$. The two readings solve different problems.
9. **The equally-likely formula $P(E)=|E|/|S|$ is not the definition of probability.** It requires equally likely outcomes, and deciding whether they are is where elementary probability goes wrong. See [[Probability Theory/contents/02 - Axioms of Probability|Probability Theory ch. 02]] for the axioms.
10. **Distinguish the sample space from the event carefully, and count both in the same way.** If you count the space as ordered and the event as unordered, the ratio is meaningless.
11. **In a pigeonhole proof, say explicitly what the pigeons are and what the holes are.** Most failed attempts are failures to make that choice well, and the reader cannot check the argument without it.
12. **Sometimes you must reduce the number of holes before pigeonhole applies.** Exercise 5(c) has $n$ people and $n$ apparent values; the proof works only after showing two values are mutually exclusive.
13. **The generalized form gives $\lceil n/k\rceil$, not $n/k$.** With 45 students in 7 sections the guarantee is 7, not $6.43$, and it is **tight** — do not claim 8.
14. **Pigeonhole proves existence, never location or count.** If you need to *find* the duplicate, you need an algorithm, not this principle.
15. **The second form is the most reusable statement in the chapter:** no injection from a larger finite set to a smaller one. It is the one-line reason hash collisions, compression limits, and comparison-sort lower bounds are all unavoidable.

> [!warning] Gaps in the source material
> **Extraction was good for prose, definitions and theorem statements**, as throughout. New artefacts: **binomial coefficients in display position often lose their structure**, and §6.7's $\sum$ notation extracts with the limits detached (`n∑ k=0`). Recorded in `00-Index.md`.
>
> **This chapter suffered the heaviest formula loss so far**, because its content *is* formulas in display position. **Theorem 6.2.10 ($P(n,r)$), Theorem 6.2.16 ($C(n,r)$), Theorem 6.3.2 (multiset permutations) and Theorem 6.3.5 (combinations with repetition) all extract as their statement's opening words with the formula itself missing** — e.g. Theorem 6.3.5 arrives as "If $X$ is a set containing $t$ elements, the number of unordered, $k$-element selections" and stops. The formulas in §§3–4 are therefore **reconstructed from the surrounding derivations** (which do survive — the $P(n,r)=C(n,r)r!$ argument and the equivalence-class argument are both intact) **and then verified numerically**: $P(8,3)=336$, $C(8,3)=56$ with $C\cdot3!=P$; `MISSISSIPPI` $=34{,}650$ confirmed by enumerating distinct permutations; $C(9,6)=84$ confirmed by enumerating solutions of $x_1+\cdots+x_4=6$; $C(52,5)=2{,}598{,}960$.
>
> **The worked example bodies are largely lost** — Examples 6.1.1–6.1.14, 6.2.x and 6.3.x arrive as problem statements with `SOLUTION` followed by fragments. Every number in this note's examples was recomputed: $5^4=625$, $P(5,4)=120$, the 96 count both directly and by complement, $2^5+2^5=64$, and the reflexive-relation count $2^{n^2-n}$.
>
> **Table 6.7.1** (the eight selections computing $(a+b)^3$) is one of the few tables that survived intact, and it is quoted because it is the clearest statement of *why* the binomial coefficient counts what it counts. **Tables 6.3.x** (the summary of the four generalized counts) did **not** survive — §4's four-case table is my own reconstruction, and the four formulas in it were each verified independently.
>
> **All figures are images and are lost**, including Figure 6.1.2 (the multiplication-principle tree), Figure 6.2.6 (the equivalence-class picture behind $C(n,r)=P(n,r)/r!$) and **Figure 6.8.1 (the six-pigeons-four-holes diagram)** — the canonical illustration of the whole of §8. The notes state the arguments in words and symbols instead.
>
> **No error was found in Johnsonbaugh ch. 6.** Six chapters in, the errata table in `00-Index.md` is still empty.
>
> **Additions beyond the source.** The **four-case table** in §4 ("does order matter? may items repeat?") is assembled by me from results Johnsonbaugh states separately; presenting them together is the single most useful thing in the chapter and the book does not do it. The **stars-and-bars picture** is mine — Johnsonbaugh proves Theorem 6.3.5 by a different route and never draws the bijection, which is what makes the formula memorable. The **"pre-allocate the minimum" technique** (Exercise 3(c)) and the **complement technique** are named and stated here as techniques rather than left implicit. Exercise 4(d)'s **double count of (subset, element) pairs** proving $\sum k\,C(n,k)=n2^{n-1}$ is my own, chosen to show double counting in its purest form; so is the framing of Pascal's identity as "split on a binary choice" and the remark that this needs no algebra. **Exercise 5(c) (two people share an acquaintance count) is my own addition**, included because the naive hole choice fails and the fix — showing that $0$ and $n-1$ are mutually exclusive — is the lesson of §8; its graph-theoretic restatement (no finite simple graph has all degrees distinct) is a forward link to [[08 - Graph Theory|ch. 08]]. The observation that **pigeonhole's second form is what makes hash collisions, compression limits and the comparison-sort bound all unavoidable** is mine and ties three separate chapters together.
>
> **Deliberately compressed.** **§§6.5–6.6 (discrete probability, ~16 pages, both marked optional by Johnsonbaugh)** are reduced to §6's short statement, because [[Probability Theory/contents/00-Index|Probability Theory]] covers the same ground far more thoroughly from Ross — ownership recorded in `00-Index.md`. **§6.4 (algorithms for generating permutations and combinations)** is summarised rather than developed: the lexicographic-successor rule and the shape of its correctness proof are given, but the pseudocode is not reconstructed, since `itertools.combinations` produces exactly this order and the algorithm's interest is historical. Johnsonbaugh's two "Problem-Solving Corner" sections (Counting, p. 267; Combinations, p. 281) are worked-example collections whose content is distributed through §§1–4 and the exercises.

**Previous:** [[05 - Number Theory and Cryptography]] · **Next:** [[07 - Recurrence Relations]]
