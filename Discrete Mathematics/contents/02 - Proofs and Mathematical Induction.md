---
subject: Discrete Mathematics
chapter: 2
tags: [ds, discrete-mathematics, proofs, induction, contradiction, contrapositive, well-ordering, loop-invariants]
source: "Johnsonbaugh, *Discrete Mathematics* 8e, ch. 2 (book pp. 62–110)"
---

# Proofs and Mathematical Induction

[[01 - Sets and Logic|Chapter 01]] built the machinery; this chapter puts it to work. It answers two questions: **what is a proof**, and **what are the standard shapes a proof can take**.

The second half is the more important. **Mathematical induction is the single most useful technique in discrete mathematics**, and it is not merely a proof method — it is the same idea as recursion, which means this chapter is also the theoretical half of [[04 - Algorithms and Their Analysis|ch. 04]], [[07 - Recurrence Relations|ch. 07]] and every recursive function you will ever write. A recursive definition builds upward; an inductive proof verifies downward. They are one thought.

## 📘 Main Knowledge

### 1. What a mathematical system is

A **mathematical system** consists of **axioms**, **definitions**, and **undefined terms**.

- **Axioms** are assumed true without proof.
- **Definitions** create new concepts from existing ones.
- **Undefined terms** are the primitives — you must start somewhere. In Euclidean geometry, *point* and *line* are undefined; the axioms describe how they behave.

Within a system you derive **theorems** — propositions proved true. A **lemma** is a theorem whose main purpose is to help prove another; a **corollary** is a theorem that follows quickly from one just proved. The distinction is one of *role*, not of difficulty or importance.

Most theorems have the form of a universally quantified conditional:

$$\forall x_1,\dots,x_n\ \big(p(x_1,\dots,x_n)\to q(x_1,\dots,x_n)\big).$$

**And [[01 - Sets and Logic|ch. 01]] already tells us how to attack it.** When the hypothesis $p$ is false the conditional is vacuously true, so **only the case "$p$ true" needs any work.** That single observation is why every proof begins "assume the hypothesis".

> [!note] Definitions exist to be used in proofs
> Everyone knows what an even number is. The point of writing it down formally is that the formal version can be *manipulated*:
>
> **Definition.** An integer $n$ is **even** if there exists an integer $k$ with $n=2k$; it is **odd** if there exists an integer $k$ with $n=2k+1$.
>
> So $12$ is even (take $k=6$) and $-21$ is odd (take $k=-11$). **Notice the shape: each definition is an existential statement, so "assume $n$ is even" means "obtain a $k$", and "prove $n$ is even" means "produce a $k$".** That is the whole technique of §2, and it generalises: whenever a proof stalls, unfold a definition into its quantified form and see what it hands you.

### 2. Direct proof

A **direct proof** of $p\to q$ assumes $p$ and derives $q$, using the hypothesis, axioms, definitions, earlier theorems and rules of inference.

> [!example]- Worked example — the anatomy of a direct proof (J Example 2.1.10)
> **Claim.** For all integers $m,n$: if $m$ is odd and $n$ is even, then $m+n$ is odd.
>
> Johnsonbaugh's presentation is worth copying because he shows the *scaffolding* before the prose. Start with the two ends:
>
> | | |
> |---|---|
> | $m$ is odd and $n$ is even | (hypothesis) |
> | ⋮ | |
> | $m+n$ is odd | (conclusion) |
>
> Now unfold each definition, which fills the gap from both directions:
>
> | | |
> |---|---|
> | $m$ is odd and $n$ is even | (hypothesis) |
> | there is $k_1$ with $m=2k_1+1$ | (definition of odd) |
> | there is $k_2$ with $n=2k_2$ | (definition of even) |
> | **need: some $k$ with $m+n=2k+1$** | (definition of odd, run backwards) |
> | $m+n$ is odd | (conclusion) |
>
> The gap is now arithmetic. **Proof.** Let $m,n$ be arbitrary integers with $m$ odd and $n$ even. Then $m=2k_1+1$ and $n=2k_2$ for some integers $k_1,k_2$. So
> $$m+n=2k_1+1+2k_2=2(k_1+k_2)+1,$$
> and since $k_1+k_2$ is an integer, $m+n$ is odd by definition. $\blacksquare$
>
> **Two habits to take from this.** (i) *Write the conclusion's definition out before you need it* — it tells you what you are hunting for. (ii) *State the conclusion explicitly at the end*, with its justification; do not let the reader infer that you finished.

> [!warning] Two failure modes that look like proofs
> Johnsonbaugh flags both, and both are worth internalising.
>
> **(a) Reusing the same letter for two different quantities.** Here is a "proof" that if $m$ and $n$ are even then $mn$ is a perfect square: *since $m,n$ are even, $m=2k$ and $n=2k$, so $mn=(2k)^2$.* **Wrong** — evenness gives $m=2k_1$ and $n=2k_2$ with *possibly different* $k$'s. And the claim is false: $m=2$, $n=4$ gives $mn=8$, not a square. **Whenever you unfold two existential statements, name the witnesses differently.**
>
> **(b) Assuming what you are proving.** Here is a "proof" that if $m$ and $m+n$ are even then $n$ is even: *let $m=2k_1$ and $n=2k_2$; then …* **Wrong at the second word** — writing $n=2k_2$ *asserts* $n$ is even, which is the conclusion. You may unfold only the **hypotheses**. (The statement is true; the honest proof uses $n=(m+n)-m$.)

### 3. Counterexamples

To disprove $\forall x\,P(x)$, exhibit one $x$ making $P(x)$ false — a **counterexample**, exactly as [[01 - Sets and Logic|ch. 01]] §5 described. Johnsonbaugh's example: $\forall n\in\mathbb Z^+\,(2^n+1\text{ is prime})$ is false, and $n=3$ settles it, since $2^3+1=9=3\cdot3$.

**A counterexample is a complete disproof and requires no further argument** beyond verifying it. Conversely — and this is the asymmetry again — **no number of confirming instances proves a universal claim.** Checking that $m=11$, $n=4$ gives the odd sum $15$ does *not* prove §2's theorem.

> [!note] What to do when you cannot tell
> Johnsonbaugh's practical advice, which is better than it sounds: **try to prove it, and let the attempt fail informatively.** Where the proof breaks tells you what a counterexample must look like. His Example 2.1.15 tests whether $(A\cap B)\cup C=A\cap(B\cup C)$; the attempted proof stalls precisely on an element of $C$ that is not in $A$, and that stall *is* the recipe — take $C\not\subseteq A$ and you have your counterexample.

### 4. Proof by contradiction

A **proof by contradiction** (or **indirect proof**) establishes $p\to q$ by assuming $p$ **and $\lnot q$**, then deriving a **contradiction** — a proposition of the form $r\land\lnot r$.

It is justified because $p\to q$ and $(p\land\lnot q)\to(r\land\lnot r)$ are logically equivalent: since $r\land\lnot r$ is always false, the second conditional can hold only if $p\land\lnot q$ is false, i.e. only if $p\to q$.

> [!warning] The one thing that distinguishes it from a direct proof
> **In a direct proof the negated conclusion is *not* assumed; in a proof by contradiction it *is*.** That extra assumption is the whole benefit — it gives you a second thing to work with — and it is also the whole risk, since a proof that never uses $\lnot q$ was secretly a direct proof, and one that derives a contradiction from $p$ alone has shown the hypothesis impossible, not the theorem.

> [!example]- Worked example (J Example 2.2.1)
> **Claim.** For every $n\in\mathbb Z$: if $n^2$ is even then $n$ is even.
>
> A direct proof stalls immediately: from $n^2=2k_1$ there is no way to extract $n=2k_2$ without essentially assuming the result.
>
> **Proof.** Assume $n^2$ is even and, for contradiction, that $n$ is **odd**. Then $n=2k+1$ for some integer $k$, so
> $$n^2=(2k+1)^2=4k^2+4k+1=2(2k^2+2k)+1,$$
> which is **odd**. So $n^2$ is both even (hypothesis) and odd — a contradiction. Hence $n$ is even. $\blacksquare$
>
> **Why contradiction was the right tool.** The hypothesis $n^2$ even is hard to *use* and the conclusion $n$ even is hard to *reach*; negating the conclusion converts the hard-to-reach thing into an easy-to-use thing ($n=2k+1$), and squaring is a forward step. **That is the general signal: reach for contradiction when the conclusion is easier to negate than to construct** — typically when it asserts non-existence, uniqueness, or irrationality.

### 5. Proof by contrapositive, cases, and equivalence

**Contrapositive.** Since $p\to q\equiv\lnot q\to\lnot p$ ([[01 - Sets and Logic|ch. 01]] §3), proving the contrapositive proves the theorem. It is often confused with contradiction; the difference is clean:

| | assume | derive |
|---|---|---|
| **contradiction** | $p$ **and** $\lnot q$ | a contradiction $r\land\lnot r$ |
| **contrapositive** | $\lnot q$ only | $\lnot p$ |

Contrapositive is a *direct* proof of an equivalent statement, and is usually tidier when it applies. §4's example works this way too: assume $n$ odd, conclude $n^2$ odd — no contradiction needed.

**Proof by cases.** Split the hypothesis into exhaustive cases and prove each. The obligation is that the cases really are exhaustive; a proof by cases that misses a case proves nothing.

**Proofs of equivalence.** To prove $p\leftrightarrow q$, prove $p\to q$ and $q\to p$ — the instruction encoded in $p\leftrightarrow q\equiv(p\to q)\land(q\to p)$. For a chain of $n$ equivalent statements it suffices to prove a cycle of implications $P_1\to P_2\to\cdots\to P_n\to P_1$, which is $n$ proofs rather than $n(n-1)$.

**Existence proofs.** A **constructive** existence proof exhibits the object; a **nonconstructive** one shows it must exist without producing it. Both are valid, and the distinction is not idle: a constructive proof is (often) an algorithm, a nonconstructive one is not. §8's well-ordering proofs are nonconstructive in exactly this way.

### 6. Mathematical induction

> [!note] The Principle of Mathematical Induction
> Let $S(n)$ be a propositional function with domain $\{n\in\mathbb Z:n\ge n_0\}$. Suppose
> 1. **Basis Step:** $S(n_0)$ is true;
> 2. **Inductive Step:** for all $n\ge n_0$, if $S(n)$ is true then $S(n+1)$ is true.
>
> Then $S(n)$ is true for **every** integer $n\ge n_0$.

The picture is a line of dominoes: the basis step topples the first, the inductive step guarantees each topples the next.

> [!warning] Both steps are indispensable, and each fails differently
> **Without the basis step** the inductive step is vacuous: "if $n=n+1$ then $n+1=n+2$" is perfectly valid, and $n=n+1$ is false for every $n$. **Without the inductive step** you have merely checked one case.
>
> **The inductive step is not an assumption that $S(n)$ is true.** It is a proof of the *conditional* $S(n)\to S(n+1)$. Saying "assume $S(n)$" is shorthand for "suppose $S(n)$ holds, and see what follows" — this is not circular, and it is worth being clear about, because the appearance of circularity is what makes induction feel like a trick the first few times.

**The whole skill is finding case $n$ inside case $n+1$.** Johnsonbaugh puts it exactly that way, and it is the only piece of advice that generalises.

> [!example]- The four standard shapes, worked
> **(a) A sum formula.** Show $1+2+\cdots+n=\dfrac{n(n+1)}2$.
> *Basis* ($n=1$): $1=\frac{1\cdot2}2$ ✓. *Inductive step:* assume $\sum_{i=1}^n i=\frac{n(n+1)}2$. Then
> $$\sum_{i=1}^{n+1}i=\underbrace{\sum_{i=1}^{n}i}_{\text{case }n\text{ appears}}+(n+1)=\frac{n(n+1)}2+(n+1)=\frac{(n+1)(n+2)}2\ \checkmark$$
> **Peeling off the last term is how case $n$ is exposed** — that one move handles most sum formulas.
>
> **(b) The geometric sum** (J Example 2.4.4), the most reused formula in the subject. For $r\ne1$,
> $$a+ar+ar^2+\cdots+ar^n=\frac{a(r^{n+1}-1)}{r-1}.$$
> Here $n_0=0$, so **the basis step is $n=0$**: the left side is $a$ and the right is $\frac{a(r-1)}{r-1}=a$ ✓. *(Verified symbolically; and with $a=3,r=2,n=4$ both sides give $93$.)* Taking $a=1,r=2$ gives $1+2+4+\cdots+2^n=2^{n+1}-1$ — the formula behind binary representations ([[05 - Number Theory and Cryptography|ch. 05]]) and the cost of doubling an array.
>
> **(c) Divisibility.** Show $5^n-1$ is divisible by $4$ for $n\ge1$.
> *Basis:* $5^1-1=4$ ✓. *Inductive step:* assume $4\mid 5^n-1$. Then
> $$5^{n+1}-1=5\cdot5^n-1=5(\underbrace{5^n-1}_{\text{case }n})+4,$$
> a sum of two multiples of $4$. ✓ **The trick — add and subtract to make case $n$ appear — is the divisibility analogue of peeling off a term.** *(Verified for $n\le40$.)*
>
> **(d) Counting.** $|X|=n\ \Rightarrow\ |\mathcal P(X)|=2^n$ (J Theorem 2.4.6).
> *Basis* ($n=0$): $\mathcal P(\emptyset)=\{\emptyset\}$ has $1=2^0$ element ✓. *Inductive step:* let $|X|=n+1$, fix $x\in X$, and split the subsets of $X$ into those containing $x$ and those not. The latter are exactly the subsets of $X-\{x\}$, and there are $2^n$ of them by hypothesis; the former are in bijection with them via $A\mapsto A\cup\{x\}$. Total $2^n+2^n=2^{n+1}$ ✓.
>
> **This proof is the template for every counting argument in [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]]:** split by a binary choice, count each part, add.

**Induction is not only for formulas.** Johnsonbaugh's Example 2.4.7 proves that **any $2^k\times2^k$ board with one square removed can be tiled by right trominoes** — a purely geometric statement, and one whose inductive step is genuinely clever: quarter the $2^{k+1}\times2^{k+1}$ board, place one tromino at the centre covering one square of each of the three quarters that are not already deficient, and apply the hypothesis to all four. **The induction supplies the recursion, and the recursion is an algorithm.**

**Loop invariants.** A **loop invariant** is a statement about program variables true just before each test of the loop condition. Proving one is an induction: the basis step establishes it before the first test, the inductive step shows one pass preserves it. Johnsonbaugh's example verifies `fact = i!` as an invariant of a factorial loop. **This is how imperative programs are proved correct**, and it is the reason induction belongs in a computing curriculum rather than only a mathematics one.

### 7. The strong form of induction

Sometimes $S(n)$ needs more than its immediate predecessor.

> [!note] Strong Form of Mathematical Induction
> Suppose (1) $S(n_0)$ is true, and (2) for all $n>n_0$: **if $S(k)$ is true for all $k$ with $n_0\le k<n$**, then $S(n)$ is true. Then $S(n)$ holds for every $n\ge n_0$.

The two forms are **logically equivalent** — neither proves more than the other — but the strong form is often far more convenient. The inductive hypothesis is now *everything below $n$*, not just $n-1$.

> [!warning] The strong form changes how many basis steps you need
> This is the part that gets missed. If the inductive step reaches back to case $n-p$, then the constraint $n_0\le n-p$ must hold, which requires $n\ge n_0+p$. **Cases $n_0,n_0+1,\dots,n_0+p-1$ are therefore not covered by the inductive step and must all be basis steps — $p$ of them.**
>
> Johnsonbaugh's Example 2.5.1: postage of $4$ cents or more can be made from $2$-cent and $5$-cent stamps. The inductive step adds a $2$-cent stamp to case $n-2$, so $p=2$ and there are **two** basis steps, $n=4$ ($2+2$) and $n=5$ (one $5$). Exercise 4 below does the same with $p=3$.

Strong induction is the natural tool whenever a sequence is defined in terms of several earlier terms, or in terms of $\lfloor n/2\rfloor$ — which is precisely the divide-and-conquer situation of [[07 - Recurrence Relations|ch. 07]]. Johnsonbaugh's Example 2.5.4 is a nice non-numeric use: **however you parenthesise a product $a_1a_2\cdots a_n$, it takes exactly $n-1$ multiplications** — strong induction on the split point, since the two halves can be any sizes.

### 8. The well-ordering property

> [!note] Well-Ordering Property
> **Every nonempty set of nonnegative integers has a least element.**

It looks too obvious to be useful and is neither. Note first that it **fails** for the negative integers, for $\mathbb Q^{\text{nonneg}}$ (the positive rationals have no least element) and for $\mathbb R^{\text{nonneg}}$ — so it is a genuine property of $\mathbb Z^{\text{nonneg}}$, not a triviality. It is **equivalent** to both forms of induction: any one of the three can be derived from the others.

Its characteristic use is to produce an object by taking the smallest one with some property.

> [!example]- Worked example — the Quotient–Remainder Theorem (J Theorem 2.5.6)
> **Theorem.** If $n$ is an integer and $d$ a positive integer, there exist **unique** integers $q$ (quotient) and $r$ (remainder) with $n=dq+r$ and $0\le r<d$.
>
> **Existence.** Let $X=\{n-dk\ :\ k\in\mathbb Z,\ n-dk\ge0\}$. This is a nonempty set of nonnegative integers, so by well-ordering it has a least element $r=n-dq$ for some $q$. Then $r\ge0$ by construction. **And $r<d$**: otherwise $r-d\ge0$, so $n-d(q+1)=r-d$ would lie in $X$ and be *smaller* than $r$ — contradicting minimality. $\blacksquare$
>
> **This is the engine of [[05 - Number Theory and Cryptography|ch. 05]]** — it is what makes `//` and `%` well defined, and the Euclidean algorithm is nothing but this theorem applied repeatedly. Note the proof is **nonconstructive** in the sense of §5: it proves $q$ and $r$ exist without telling you how to find them. Long division is the constructive counterpart.
>
> Note also the shape of the argument — *assume something smaller exists, contradict minimality* — which is the standard well-ordering move and appears again in [[09 - Trees|ch. 09]]'s minimal spanning tree proofs.

## ✏️ Exercises

**1. (Direct proof and counterexample.)** (a) Prove: for all integers $m,n$, if $m$ and $n$ are odd then $mn$ is odd. (b) Decide whether this is true, and prove it or give a counterexample: *for all integers $m,n$, if $mn$ is even then both $m$ and $n$ are even.* (c) Find the error in this "proof" that the sum of two odd integers is divisible by 4: *let $m=2k+1$ and $n=2k+1$; then $m+n=4k+2$…*

> [!example]- Solution
> **(a)** Let $m,n$ be arbitrary odd integers. By definition there are integers $k_1,k_2$ with $m=2k_1+1$ and $n=2k_2+1$. Then
> $$mn=(2k_1+1)(2k_2+1)=4k_1k_2+2k_1+2k_2+1=2\underbrace{(2k_1k_2+k_1+k_2)}_{\text{an integer}}+1,$$
> so $mn$ is odd by definition. $\blacksquare$ **Note the two distinct witnesses $k_1,k_2$** — the point of §2's warning (a).
>
> **(b) False.** **Counterexample: $m=2$, $n=3$.** Then $mn=6$ is even, but $n=3$ is not even. One counterexample is a complete disproof.
>
> *(The true statement is the converse-ish one: if $mn$ is even then **at least one** of $m,n$ is even — provable by contraposition, since if both are odd then $mn$ is odd by part (a). Notice that (a) is exactly what part (b)'s repair needs, which is why they are set together.)*
>
> **(c)** The error is **using the same letter $k$ for both integers** — §2's failure mode (a). Odd $m$ and odd $n$ give $m=2k_1+1$ and $n=2k_2+1$ with $k_1,k_2$ *possibly different*, so
> $$m+n=2k_1+2k_2+2=2(k_1+k_2+1),$$
> which is **even** but need not be divisible by $4$. The written "proof" silently assumed $m=n$.
>
> **And the claim is false:** $m=1$, $n=3$ give $m+n=4$ ✓ divisible by 4, but $m=1$, $n=5$ give $m+n=6$, which is not. **A false statement can have a proof that looks fine until you check which letters are bound where.**

**2. (Induction on a sum.)** Prove by induction that for all $n\ge1$,
$$\sum_{i=1}^n i(i+1)=\frac{n(n+1)(n+2)}{3}.$$

> [!example]- Solution
> **Basis Step ($n=1$).** Left side $=1\cdot2=2$. Right side $=\frac{1\cdot2\cdot3}3=2$ ✓
>
> **Inductive Step.** Let $n\ge1$ and assume $\sum_{i=1}^n i(i+1)=\frac{n(n+1)(n+2)}3$. Then peel off the last term to expose case $n$:
> $$\sum_{i=1}^{n+1}i(i+1)=\underbrace{\sum_{i=1}^{n}i(i+1)}_{\text{inductive hypothesis}}+(n+1)(n+2) =\frac{n(n+1)(n+2)}3+(n+1)(n+2).$$
> Factor out $(n+1)(n+2)$:
> $$=(n+1)(n+2)\left(\frac n3+1\right)=(n+1)(n+2)\cdot\frac{n+3}3=\frac{(n+1)(n+2)(n+3)}3,$$
> which is the claimed formula with $n$ replaced by $n+1$ ✓
>
> Both steps verified, so the formula holds for all $n\ge1$ by induction. $\blacksquare$
>
> **Verified independently:** `sympy` returns the closed form $n(n+1)(n+2)/3$ for the sum, and the values for $n=1,\dots,6$ are $2,8,20,40,70,112$ from both sides.
>
> **Two remarks.** (i) **Factoring rather than expanding is the labour-saving move** — multiplying everything out and re-factoring is where algebra errors enter. Always look for the common factor between the inductive hypothesis and the new term. (ii) The formula has a slicker derivation: $i(i+1)=2\binom{i+1}2$, so the sum is $2\binom{n+2}3=\frac{(n+2)(n+1)n}3$ by the hockey-stick identity of [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]]. **Induction verifies formulas; it rarely explains them.**

**3. (Divisibility and an inequality.)** (a) Prove $6\mid 7^n-1$ for all $n\ge1$. (b) Prove $2^n>n^2$ for all $n\ge5$, and say why the basis step is not $n=1$.

> [!example]- Solution
> **(a) Basis ($n=1$):** $7^1-1=6$, divisible by $6$ ✓
>
> **Inductive Step.** Assume $6\mid 7^n-1$, say $7^n-1=6t$ for an integer $t$. Then use the add-and-subtract trick to make case $n$ appear:
> $$7^{n+1}-1=7\cdot7^n-1=7\big(\underbrace{7^n-1}_{=6t}\big)+7-1=7(6t)+6=6(7t+1),$$
> a multiple of $6$ ✓ So $6\mid7^{n+1}-1$, and the result holds for all $n\ge1$. $\blacksquare$ *(Verified for $n\le40$.)*
>
> *(This generalises at no extra cost: the identical argument shows $(a-1)\mid a^n-1$ for any integer $a\ge2$ — which is J Example 2.4.5 with $a=5$, and is why $999\dots9$ is divisible by $9$.)*
>
> **(b) Basis ($n=5$):** $2^5=32>25=5^2$ ✓
>
> **Inductive Step.** Let $n\ge5$ and assume $2^n>n^2$. Then
> $$2^{n+1}=2\cdot2^n>2n^2,$$
> so it suffices to show $2n^2\ge(n+1)^2$, i.e. $2n^2\ge n^2+2n+1$, i.e. $n^2-2n-1\ge0$. For $n\ge5$ we have $n^2-2n-1=n(n-2)-1\ge5\cdot3-1=14>0$ ✓ Hence $2^{n+1}>(n+1)^2$. $\blacksquare$
>
> **Why the basis is $n=5$.** The statement is **false** for $n=2,3,4$:
> $$\begin{array}{c|cccccc} n&1&2&3&4&5&6\\\hline 2^n&2&4&8&16&32&64\\ n^2&1&4&9&16&25&36 \end{array}$$
> It holds at $n=1$ ($2>1$), then **fails at $n=2$ and $n=4$ (equality) and $n=3$**, then holds from $n=5$ on. *(All verified computationally for $n\le200$.)*
>
> **So starting at $n=1$ would be a genuine error, not pedantry** — the inductive step would be asked to carry a false statement forward from $n=2$. And note that the inductive step itself *needs* $n\ge5$: at $n=2$, $n^2-2n-1=-1<0$ and the argument collapses. **When an induction has a nontrivial starting point, the inductive step usually reveals what it must be.**

**4. (Strong induction — and counting the basis steps.)** A shop sells stamps in $3$-cent and $5$-cent denominations only. Prove that **every** postage amount of $8$ cents or more can be made exactly. State clearly how many basis steps are required and why.

> [!example]- Solution
> **First, why $8$.** The achievable amounts are $0,3,5,6,8,9,10,11,\dots$; the **unreachable** ones are exactly $\{1,2,4,7\}$. *(Verified by enumeration.)* So $8$ is the correct threshold — $7$ genuinely cannot be made, and everything from $8$ up can.
>
> **How many basis steps.** The inductive step will make $n$ cents by adding a **$3$-cent** stamp to an amount of $n-3$ cents. For the inductive hypothesis to apply we need $n-3\ge8$, i.e. $n\ge11$. So cases $n=8,9,10$ are **not** reachable by the inductive step and must be basis steps: **three basis steps**, matching §7's rule with $p=3$.
>
> **Basis Steps.**
> - $n=8$: one $3$-cent and one $5$-cent stamp ✓
> - $n=9$: three $3$-cent stamps ✓
> - $n=10$: two $5$-cent stamps ✓
>
> **Inductive Step.** Let $n\ge11$ and assume every amount $k$ with $8\le k<n$ can be made. Since $n\ge11$ we have $n-3\ge8$, and clearly $n-3<n$, so the inductive hypothesis applies to $n-3$: it can be made from $3$- and $5$-cent stamps. Adding one more $3$-cent stamp makes $n$ cents. ✓
>
> By the strong form of induction, every amount $n\ge8$ can be made. $\blacksquare$ *(Verified: all of $8,\dots,30$ are achievable.)*
>
> **Why the *strong* form is needed.** The step goes from $n-3$ to $n$, not from $n-1$ to $n$, so the ordinary form — whose hypothesis is only the immediate predecessor — does not apply. The strong form's hypothesis covers *everything* below $n$, so reaching back three places is free.
>
> **The general fact behind this** (worth knowing, not required here): for coprime denominations $a,b$ the largest unreachable amount is $ab-a-b$, the **Frobenius number**. Here $3\cdot5-3-5=7$ ✓ exactly matching the enumeration. If the denominations were *not* coprime — say $3$ and $6$ — no amount not divisible by $3$ would ever be reachable and no such threshold would exist.

**5. (Hard — a fallacious induction, and well-ordering.)** (a) The following argument claims that in any set of $n\ge1$ horses, all horses have the same colour. Find the exact error. *Basis: a set of one horse trivially has all horses the same colour. Inductive step: given a set of $n+1$ horses, remove one to get a set of $n$ horses, all the same colour by hypothesis; remove a different one instead, again all the same colour; since the two sets overlap, all $n+1$ horses have the same colour.* (b) Prove by induction that $n$ straight lines in the plane, no two parallel and no three concurrent, divide it into $1+n+\binom n2$ regions. (c) Use the well-ordering property to prove that $\sqrt2$ is irrational.

> [!example]- Solution
> **(a)** The basis step is fine and the inductive step is fine **for $n+1\ge3$**. It fails at exactly one place: **$n+1=2$.**
>
> With two horses $\{h_1,h_2\}$, removing one gives $\{h_2\}$ and removing the other gives $\{h_1\}$. Both are single-horse sets, so both are monochromatic — but **the two sets are disjoint**, so the phrase "since the two sets overlap" is false. There is no shared horse to transfer the colour through, and nothing links $h_1$'s colour to $h_2$'s.
>
> **So the induction proves $S(1)$, and proves $S(n)\to S(n+1)$ for $n\ge2$, but never proves $S(1)\to S(2)$.** The chain of dominoes has its second domino missing, and everything after it is unsupported. **The error is not in the logic of induction but in an unstated case assumption inside the inductive step** — which is the most common way a bogus induction hides. *(Johnsonbaugh's Exercise 50 is the same fallacy dressed as "any two numbers $a$ and $b$ are equal".)*
>
> **The lesson worth extracting:** when an inductive step says "the two sets overlap", "pick an element other than $x$", or "split into two nonempty parts", **check the smallest case where that phrase must be honoured.**
>
> **(b)** Let $R(n)$ be the number of regions.
>
> **Basis ($n=0$):** no lines, one region — the whole plane. Formula: $1+0+\binom02=1$ ✓
>
> **Inductive Step.** Assume $n$ lines in general position create $1+n+\binom n2$ regions, and add an $(n+1)$st line $\ell$. Since $\ell$ is parallel to none of the others it meets each in a point, and since no three lines are concurrent these $n$ points are **distinct**. They cut $\ell$ into $n+1$ pieces, and **each piece splits exactly one existing region into two**, so
> $$R(n+1)=R(n)+(n+1).$$
> Therefore
> $$R(n+1)=1+n+\binom n2+(n+1)=1+(n+1)+\left[\binom n2+n\right]=1+(n+1)+\binom{n+1}2,$$
> using Pascal's identity $\binom{n+1}2=\binom n2+\binom n1$ ([[06 - Counting Methods and the Pigeonhole Principle|ch. 06]]). ✓ $\blacksquare$
>
> Values: $1,2,4,7,11,16,22$ for $n=0,\dots,6$ — and the recurrence $R(n)=R(n-1)+n$ was verified for $n\le50$, as was the closed form $\tfrac{n^2+n+2}2$.
>
> **Note where the hypotheses were used.** "No two parallel" gave $n$ intersection points; "no three concurrent" made them distinct. **Drop either and the count drops** — $n$ parallel lines give only $n+1$ regions. This is a good example of an induction whose real content is geometric, with the algebra merely bookkeeping.
>
> **(c)** Suppose, for contradiction, that $\sqrt2$ is rational. Then the set
> $$X=\{n\in\mathbb Z^+\ :\ n\sqrt2\in\mathbb Z^+\}$$
> is **nonempty** — if $\sqrt2=p/q$ with $p,q$ positive integers then $q\in X$, since $q\sqrt2=p$.
>
> By the **well-ordering property**, $X$ has a least element $n$. Consider
> $$m=n\sqrt2-n=n(\sqrt2-1).$$
> - $m$ is a **positive integer**: it is $n\sqrt2-n$, a difference of two positive integers, and it is positive because $\sqrt2>1$.
> - $m\sqrt2=(n\sqrt2-n)\sqrt2=2n-n\sqrt2$ is also an **integer** (difference of integers), and it is positive since $\sqrt2<2$. So $m\in X$.
> - But $\sqrt2-1\approx0.414<1$, so $m=n(\sqrt2-1)<n$.
>
> So $m\in X$ and $m<n$, contradicting the minimality of $n$. Hence $X$ is empty and $\sqrt2$ is **irrational**. $\blacksquare$
>
> **Why this is a nicer proof than the usual one.** The familiar argument assumes $p/q$ in *lowest terms* and derives that both $p$ and $q$ are even — which needs §4's lemma that $n^2$ even $\Rightarrow$ $n$ even, and needs the fact that every fraction *has* a lowest-terms form (itself a well-ordering argument in disguise). **This version uses well-ordering once, explicitly, and needs no divisibility theory at all.** It is also the standard well-ordering move from §8: *build a smaller element and contradict minimality.*

## 📝 Summary

- A **mathematical system** is axioms + definitions + undefined terms. **Theorems** are derived within it; a **lemma** is a helper, a **corollary** a quick consequence — the distinction is one of role, not importance.
- Most theorems are $\forall\mathbf x\,(p(\mathbf x)\to q(\mathbf x))$, and since a false hypothesis makes the conditional **vacuously true** ([[01 - Sets and Logic|ch. 01]]), **only the case "$p$ true" needs proving.** That is why every proof starts "assume the hypothesis".
- **Definitions are existential statements**: $n$ even means *there exists* $k$ with $n=2k$. So *assuming* evenness hands you a $k$, and *proving* evenness requires producing one. When stuck, unfold a definition.
- **Direct proof:** assume $p$, derive $q$. Write the conclusion's definition out first so you know what you are hunting for.
- **Two ways a "proof" fails while looking fine:** reusing one letter for two witnesses ($m=2k$ *and* $n=2k$), and unfolding the **conclusion** rather than the hypotheses (assuming what you are proving).
- **One counterexample completely disproves a universal claim**; no number of instances proves one. If you cannot decide, attempt the proof — **where it stalls is the recipe for the counterexample.**
- **Proof by contradiction:** assume $p$ **and $\lnot q$**, derive $r\land\lnot r$. Reach for it when the conclusion is easier to negate than to construct — non-existence, uniqueness, irrationality.
- **Contrapositive vs contradiction:** contrapositive assumes only $\lnot q$ and derives $\lnot p$; contradiction assumes $p\land\lnot q$ and derives an absurdity. Contrapositive is a *direct* proof of an equivalent statement, and usually tidier.
- **To prove $p\leftrightarrow q$, prove both directions.** For $n$ equivalent statements, a cycle $P_1\to P_2\to\cdots\to P_n\to P_1$ suffices.
- **Induction:** *Basis* $S(n_0)$, plus *Inductive Step* $S(n)\to S(n+1)$ for all $n\ge n_0$. Both are indispensable — without the basis the step is vacuous, without the step you have checked one case. **The inductive step proves a conditional; it does not assume $S(n)$ is true.**
- **The skill is finding case $n$ inside case $n+1$.** Sums: peel off the last term. Divisibility: add and subtract to expose $a^n-1$. Counting: split on a binary choice. Geometry: identify the recursive structure.
- **The geometric sum** $a+ar+\cdots+ar^n=\frac{a(r^{n+1}-1)}{r-1}$ ($r\ne1$) is the most reused formula in the subject; $a=1,r=2$ gives $2^{n+1}-1$.
- **Induction proves more than formulas:** $|\mathcal P(X)|=2^{|X|}$, tromino tilings, and **loop invariants** — which is how imperative programs are proved correct.
- **Strong induction** assumes $S(k)$ for *all* $n_0\le k<n$. It is logically equivalent to the ordinary form but often far more convenient. **If the inductive step reaches back $p$ places, you need $p$ basis steps** — the most commonly missed detail in the chapter.
- **Well-ordering:** every nonempty set of nonnegative integers has a least element. It **fails** for $\mathbb Z^-$, $\mathbb Q^+$ and $\mathbb R^+$, and is **equivalent** to both forms of induction. Its move is: *take the smallest element, build a smaller one, contradict.*
- **The Quotient–Remainder Theorem** ($n=dq+r$, $0\le r<d$, uniquely) follows from well-ordering and is the engine of [[05 - Number Theory and Cryptography|ch. 05]] — it is what makes `//` and `%` well defined.

## ⚠️ Important Notes

1. **Name your witnesses distinctly.** Unfolding "$m$ is even and $n$ is even" gives $m=2k_1$, $n=2k_2$ — **never $m=2k$ and $n=2k$.** This single slip "proves" false statements, and it is the most common error in a first proofs course.
2. **You may unfold only the hypotheses.** Applying a definition to the *conclusion* assumes what you are proving. If your first line manipulates the thing you are supposed to establish, stop.
3. **A universally quantified claim needs a proof; a single counterexample kills it.** Do not check three cases and write "therefore, in general". Conversely, do not construct an elaborate argument when one value suffices.
4. **In a proof by contradiction, you must actually *use* $\lnot q$.** If you never do, you wrote a direct proof with a redundant assumption. And if the contradiction comes from $p$ alone, you proved the hypothesis is impossible — a different (and usually alarming) result.
5. **Contradiction and contrapositive are different techniques.** Confusing them is harmless in outcome but produces muddled writing. If you can conclude $\lnot p$ directly from $\lnot q$, say so and stop — that is contrapositive, and it is cleaner.
6. **Proof by cases must be exhaustive.** A missed case proves nothing. State the cases before proving them so the gap is visible.
7. **"If and only if" means two proofs.** Half the theorems ahead — Euler circuits, tree characterisations, max-flow/min-cut — are stated as equivalences, and each needs both directions.
8. **Never omit the basis step.** The inductive step alone proves nothing: "if $n=n+1$ then $n+1=n+2$" is a valid implication about a false statement.
9. **Check whether your basis step is at the right place.** $2^n>n^2$ holds at $n=1$, **fails at $n=2,3,4$**, and holds from $n=5$ — so the basis is $n=5$, and the inductive step needs $n\ge5$ to work at all. When an inequality is involved, find where the step's algebra becomes valid; that is usually the true starting point.
10. **The inductive step must genuinely link $n$ to $n+1$.** A "proof" that verifies $S(n+1)$ from scratch without using $S(n)$ has proved nothing about the general case.
11. **A bogus induction usually hides an unstated case assumption inside the inductive step**, not a flaw in induction itself. When the step says "the two sets overlap", "choose an element other than $x$", or "split into two nonempty parts", **test the smallest $n$ where that must hold** — the horses fail at exactly $n+1=2$.
12. **With strong induction, count your basis steps.** Reaching back $p$ places requires $p$ of them. Writing one basis step for a step that uses $n-3$ leaves three cases unproved, and the resulting "theorem" may be false.
13. **Prefer factoring to expanding** in the inductive step of a sum formula. Multiplying out and re-factoring is where algebra errors enter; the common factor between the hypothesis and the new term is almost always the way through.
14. **Induction verifies formulas; it rarely explains them.** It cannot *find* the closed form. [[07 - Recurrence Relations|Ch. 07]] supplies methods that do — and this is why the two chapters are best read together.
15. **Constructive and nonconstructive existence proofs are both valid but not equally useful.** A constructive proof is usually an algorithm; a well-ordering proof usually is not. When you need to *compute* the object, note which kind you have.
16. **Well-ordering is a property of $\mathbb Z^{\text{nonneg}}$, not of ordered sets in general.** The positive rationals have no least element. Any argument of the form "take the smallest such $x$" must be over the integers, or it is unfounded.

> [!warning] Gaps in the source material
> **Extraction was clean for prose and definitions.** As in ch. 01, Johnsonbaugh's Unicode mathematics survives ($\in$, $\ne$, $\ge$, $\lfloor\cdot\rfloor$, $\Rightarrow$), and the definitions, theorem statements and proof text came through intact. See `00-Index.md` for the standing quirk list.
>
> **What was lost, and it is the substance of this chapter: every displayed equation inside the induction proofs.** Johnsonbaugh's worked inductions extract as their *scaffolding only* — the labels `Basis Step ( n = 1)` and `Inductive Step` survive while the algebra between them is dropped. Example 2.4.3, Example 2.4.4 (the geometric sum), Example 2.4.5, Theorem 2.4.6 and every example in §2.5 arrive as headings with empty bodies. **So every inductive computation in this note was reconstructed from the statement and then verified independently**: the geometric sum was confirmed symbolically with `sympy` (and numerically at $a=3,r=2,n=4$ giving $93$); $5^n-1$ divisible by $4$ and $7^n-1$ divisible by $6$ were checked for $n\le40$; $2^n>n^2$ was checked for $n\le200$ and its failure at $n=2,3,4$ confirmed; the stamp problem's unreachable set $\{1,2,4,7\}$ was found by enumeration; and the region count $1,2,4,7,11,16,22$ and its recurrence $R(n)=R(n-1)+n$ were verified for $n\le50$. **No error was found in Johnsonbaugh ch. 2.**
>
> **All figures are images and are lost.** The costly one is **Example 2.4.7's tromino tiling** — four figures showing the quartering of a $2^{k+1}\times2^{k+1}$ deficient board and the placement of the central tromino, which *are* the inductive step. §6 describes the construction in words precisely enough to carry out; the pictures are not reconstructed. The pseudocode of §6's loop-invariant example (Example 2.4.8) also extracts only partially, so the invariant `fact = i!` is stated and the loop it belongs to is described rather than quoted.
>
> **§2.3 (Resolution Proofs) is omitted.** Johnsonbaugh marks it "can be omitted without loss of continuity," and it is a specialised automated-theorem-proving technique with no downstream use in chapters 3–10. It is genuinely interesting as the basis of logic programming (Prolog) and SAT solvers — **flagged here in case the syllabus covers it**, since a reader would not otherwise learn that it exists.
>
> **Additions beyond the source.** Exercise 5's **horses fallacy** is the standard version of Johnsonbaugh's Exercise 50 ("any two numbers are equal"), chosen because the disjointness failure at $n+1=2$ is easier to see. Exercise 5(c)'s **well-ordering proof that $\sqrt2$ is irrational** is my own inclusion — Johnsonbaugh proves irrationality by the classical even/odd route in §2.2, and the well-ordering version is a better advertisement for §8; the comparison of the two proofs is mine. The **Frobenius number** remark in Exercise 4, the generalisation $(a-1)\mid a^n-1$ in Exercise 3, the **hockey-stick derivation** of Exercise 2's formula, and the observation that a constructive existence proof is an algorithm while a well-ordering proof is not, are all additions. The framing of induction and recursion as one idea — and hence of this chapter as the theoretical half of ch. 04 and ch. 07 — is mine; Johnsonbaugh keeps them apart.

**Previous:** [[01 - Sets and Logic]] · **Next:** [[03 - Functions, Sequences and Relations]]
