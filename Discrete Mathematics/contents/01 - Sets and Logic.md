---
subject: Discrete Mathematics
chapter: 1
tags: [ds, discrete-mathematics, sets, logic, propositions, quantifiers, inference, truth-tables]
source: "Johnsonbaugh, *Discrete Mathematics* 8e, ch. 1 (book pp. 1–61)"
---

# Sets and Logic

Every other chapter of this subject is written in the language this chapter defines. That is the honest reason to take it seriously: not because sets and truth tables are difficult, but because **almost every mistake in later chapters is a mistake made here** — confusing a conditional with its converse, negating a quantifier wrongly, or assuming "and" means what it means in conversation.

Johnsonbaugh opens with a genuinely good illustration. At one time Naperville, Illinois had an ordinance: *"It shall be unlawful for any person to keep more than three dogs and three cats upon his property within the city."* A citizen owns **five dogs and no cats.** Are they in violation? The answer turns entirely on how one word is read, and §2 below settles it.

## 📘 Main Knowledge

### 1. Sets

A **set** is a collection of objects, called its **elements** or **members**. Two things are true of it by definition, and both matter:

- **Order is irrelevant.** $\{1,2,3,4\}$ and $\{1,3,4,2\}$ are the same set.
- **Duplicates collapse.** $\{1,2,2,3,4\}$ is the same set as $\{1,2,3,4\}$.

Small finite sets can be given by listing. Large or infinite ones need **set-builder notation**:

$$B=\{x\mid x\text{ is a positive, even integer}\},$$

read "$B$ equals the set of all $x$ **such that** $x$ is a positive even integer" — the vertical bar is "such that", and the membership property goes *after* it.

A set may contain anything, of mixed type, including other sets: $\{3,\{5,1\},12,\{\pi,4.5,40,16\}\}$ has **four** elements, two of which are sets. That counting is a standard exam trap.

**The standard number sets:**

| Symbol | Set | Note |
|---|---|---|
| $\mathbb Z$ | integers | from German *Zahlen* |
| $\mathbb Q$ | rationals | quotients of integers — $\mathbb Q$ for *quotient* |
| $\mathbb R$ | reals | |

Superscripts restrict sign: $\mathbb Z^-$ the negative integers, $\mathbb Q^+$ the positive rationals, $\mathbb Z^{\text{nonneg}}=\{0,1,2,\dots\}$.

**Membership and cardinality.** $x\in X$ and $x\notin X$; for finite $X$, $|X|$ is the number of elements, the **cardinality**. The **empty set** $\emptyset=\{\,\}$ has $|\emptyset|=0$ — and note $|\{\emptyset\}|=1$, since that set contains one thing, namely the empty set.

> [!note] Equality and subsets — the two-condition method
> $X=Y$ means they have the same elements, which unpacks into **two** obligations:
> $$\text{for every }x:\ x\in X\Rightarrow x\in Y \qquad\text{and}\qquad \text{for every }x:\ x\in Y\Rightarrow x\in X.$$
> $X\subseteq Y$ ($X$ is a **subset**) is just the first of these. And $X\subset Y$ ($X$ is a **proper subset**) means $X\subseteq Y$ **and** $X\ne Y$.
>
> **This is the shape of every set-identity proof in the subject.** To prove $X=Y$, prove two inclusions. To *disprove* it, you need only **one** element on the wrong side — and you need only one of the two directions to fail, so do not waste effort showing both.

**Operations.** With $U$ a **universal set** and $X,Y\subseteq U$:

$$X\cup Y=\{x\mid x\in X\text{ or }x\in Y\},\qquad X\cap Y=\{x\mid x\in X\text{ and }x\in Y\},$$
$$X-Y=\{x\mid x\in X\text{ and }x\notin Y\},\qquad \overline X=U-X .$$

$X$ and $Y$ are **disjoint** if $X\cap Y=\emptyset$; a family is **pairwise disjoint** if every two distinct members are. The **power set** $\mathcal P(X)$ is the set of all subsets of $X$, and $|\mathcal P(X)|=2^{|X|}$.

A **partition** of $X$ is a family $\mathcal S$ of nonempty subsets such that **every element of $X$ lies in exactly one member of $\mathcal S$** — equivalently, $\mathcal S$ is pairwise disjoint and $\bigcup\mathcal S=X$. Partitions return with full force in [[03 - Functions, Sequences and Relations|ch. 03]], where they are shown to be *the same thing* as equivalence relations.

For a family $\mathcal S$ of sets, $\bigcup\mathcal S=\{x\mid x\in X\text{ for \textbf{some} }X\in\mathcal S\}$ and $\bigcap\mathcal S=\{x\mid x\in X\text{ for \textbf{all} }X\in\mathcal S\}$. *(Johnsonbaugh's Example 1.1.24 is worth keeping: with $A_i=\{i,i+1,\dots\}$, the union is $\{1,2,\dots\}$ but the intersection is $\boldsymbol\emptyset$ — no integer survives every tail.)*

**Cartesian products** take order into account. An **ordered pair** has $(a,b)=(c,d)$ precisely when $a=c$ and $b=d$, so $(a,b)\ne(b,a)$ unless $a=b$. Then
$$X\times Y=\{(x,y)\mid x\in X,\ y\in Y\},\qquad |X\times Y|=|X|\cdot|Y|,$$
and generally $|X_1\times\cdots\times X_n|=|X_1|\cdots|X_n|$. **This is the multiplication principle of [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]], arriving three chapters early.** In general $X\times Y\ne Y\times X$.

**The algebra of sets.** All of the following hold for subsets of $U$ (Johnsonbaugh's Theorem 1.1.22 — he defers the proofs to ch. 2, since they need the logic developed below):

| Law | Statement |
|---|---|
| Associative | $(A\cup B)\cup C=A\cup(B\cup C)$; same for $\cap$ |
| Commutative | $A\cup B=B\cup A$; same for $\cap$ |
| **Distributive** | $A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$; $\ A\cup(B\cap C)=(A\cup B)\cap(A\cup C)$ |
| Identity | $A\cup\emptyset=A$; $\ A\cap U=A$ |
| Complement | $A\cup\overline A=U$; $\ A\cap\overline A=\emptyset$ |
| Idempotent | $A\cup A=A$; $\ A\cap A=A$ |
| Bound | $A\cup U=U$; $\ A\cap\emptyset=\emptyset$ |
| Absorption | $A\cup(A\cap B)=A$; $\ A\cap(A\cup B)=A$ |
| Involution | $\overline{\overline A}=A$ |
| 0/1 | $\overline\emptyset=U$; $\ \overline U=\emptyset$ |
| **De Morgan** | $\overline{A\cup B}=\overline A\cap\overline B$; $\ \overline{A\cap B}=\overline A\cup\overline B$ |

**Note that both distributive laws hold** — unlike arithmetic, where $a\times(b+c)=ab+ac$ but $a+(b\times c)\ne(a+b)(a+c)$. Set union genuinely distributes over intersection. Compare the same structure in [[Linear Algebra/contents/02 - Matrix Algebra|Linear Algebra ch. 02]], where matrix multiplication distributes but does not commute.

**Venn diagrams** give pictorial views and are excellent for *suggesting* whether a set identity is true. They are **not proofs** — with three sets they are already awkward, and with four they cannot be drawn with circles at all.

### 2. Propositions and the connectives

A **proposition** is a sentence that is either true or false, but not both. "Paris is the capital of France" is one; "$x+1>2$" is not, until $x$ is fixed (see §5).

| Name | Notation | English | True exactly when |
|---|---|---|---|
| **conjunction** | $p\land q$ | $p$ and $q$ | both are true |
| **disjunction** | $p\lor q$ | $p$ or $q$ | at least one is true |
| **negation** | $\lnot p$ | not $p$ | $p$ is false |

A **truth table** for a proposition built from $n$ propositions has $2^n$ rows.

$$\begin{array}{cc|ccc} p & q & p\land q & p\lor q & \lnot p\\\hline \text T&\text T&\text T&\text T&\text F\\ \text T&\text F&\text F&\text T&\text F\\ \text F&\text T&\text F&\text T&\text T\\ \text F&\text F&\text F&\text F&\text T \end{array}$$

> [!warning] "Or" in logic is *inclusive*
> $p\lor q$ is the **inclusive-or**: it is true when *both* disjuncts are true. Everyday English often means the exclusive-or ("soup or salad"), and this is a live source of error. **Exclusive-or**, true when exactly one holds, is a different connective — and it equals $\lnot(p\leftrightarrow q)$.
>
> Likewise, in logic $p$ and $q$ **need not be related in any way.** "It is raining and $2+2=4$" is a perfectly good conjunction. Ordinary language implies relevance; logic does not.

**Precedence**, in the absence of parentheses: evaluate $\lnot$ first, then $\land$, then $\lor$, and **$\to$ last of all.** So $\lnot p\lor q\land r$ means $(\lnot p)\lor(q\land r)$, and $p\lor q\to\lnot r$ means $(p\lor q)\to(\lnot r)$.

> [!note] Back to Naperville
> *"Unlawful to keep more than three dogs **and** three cats."* Let $d$: the person keeps more than three dogs, and $c$: more than three cats. The ordinance forbids $d\land c$.
>
> Our citizen has five dogs and no cats: $d$ is **true**, $c$ is **false**, so $d\land c$ is **false**. **They are not in violation.** The ordinance as written prohibits only exceeding *both* limits at once — so someone with fifty dogs and no cats is entirely legal. Presumably the drafters meant $d\lor c$. **This is why lawyers and logicians both worry about "and".**

### 3. Conditional propositions — where the errors live

$$p\to q\qquad\text{``if }p\text{ then }q\text{''}$$

$p$ is the **hypothesis** (or antecedent), $q$ the **conclusion** (consequent).

$$\begin{array}{cc|c} p & q & p\to q\\\hline \text T&\text T&\text T\\ \text T&\text F&\textbf{F}\\ \text F&\text T&\text T\\ \text F&\text F&\text T \end{array}$$

**The only way $p\to q$ is false is a true hypothesis with a false conclusion.** In particular, **whenever $p$ is false, $p\to q$ is true** regardless of $q$ — such a statement is called **vacuously true** or **true by default**.

Johnsonbaugh motivates the two puzzling rows with a promise: a Mathematics Department says *"if the legislature grants us \$60{,}000, we will hire one new faculty member."* If the money comes and nobody is hired, the promise is broken — row 2, false. If the money does **not** come, the department has broken no promise whether or not it hires — rows 3 and 4, true.

> [!warning] Five English phrasings that all mean $p\to q$
> These are the highest-yield lines in the chapter, and (d) and (e) are where students lose marks.
>
> | English | Symbolic |
> |---|---|
> | (a) if $p$, then $q$ / $q$ **when** $p$ | $p\to q$ |
> | (b) $p$ **only if** $q$ | $p\to q$ — **not** $q\to p$ |
> | (c) $q$ **if** $p$ | $p\to q$ |
> | (d) a **necessary** condition for $p$ is $q$ | $p\to q$ — the *conclusion* is the necessary one |
> | (e) a **sufficient** condition for $q$ is $p$ | $p\to q$ — the *hypothesis* is the sufficient one |
>
> **"Only if" is the trap.** "John takes calculus only if he has sophomore standing" says *taking calculus* forces *standing* — it does **not** say standing forces calculus. Johnsonbaugh's own gloss: a sophomore need not take calculus.
>
> **Necessary vs sufficient, in one line.** *Necessary* = cannot happen without it (so it is implied). *Sufficient* = guarantees it (so it implies). "A necessary condition for the Cubs to win the World Series is that they sign a right-handed relief pitcher" means *win $\to$ sign*; it certainly does not mean signing one produces a championship.

**Converse, contrapositive, inverse.** Given $p\to q$:

| Name | Form | Equivalent to $p\to q$? |
|---|---|---|
| **converse** | $q\to p$ | ❌ **No** |
| **contrapositive** | $\lnot q\to\lnot p$ | ✅ **Yes** |
| inverse | $\lnot p\to\lnot q$ | ❌ No (it is the converse's contrapositive) |

**Both facts are load-bearing.** The contrapositive's equivalence is what licenses proof by contraposition in [[02 - Proofs and Mathematical Induction|ch. 02]]. The converse's *non*-equivalence is the single most common reasoning error in mathematics — and in statistics, where $P(A\mid B)\ne P(B\mid A)$ is exactly the same mistake wearing probability notation ([[Probability Theory/contents/03 - Conditional Probability and Independence|Probability Theory ch. 03]]).

**Biconditional.** $p\leftrightarrow q$, read "$p$ **if and only if** $q$" (often "iff"), is true exactly when $p$ and $q$ have the **same** truth value. Equivalently, "$p$ is a **necessary and sufficient** condition for $q$", and

$$p\leftrightarrow q\ \equiv\ (p\to q)\land(q\to p).$$

**That equivalence is a work instruction:** to prove an "if and only if" theorem, prove two implications. Half the theorems in this subject are stated that way.

**Logical equivalence.** $P\equiv Q$ means $P$ and $Q$ have the same truth value for *every* assignment to their constituent propositions. The essential ones:

$$\lnot(p\lor q)\equiv\lnot p\land\lnot q,\qquad \lnot(p\land q)\equiv\lnot p\lor\lnot q \qquad\textbf{(De Morgan for logic)}$$
$$\boxed{\ \lnot(p\to q)\ \equiv\ p\land\lnot q\ }$$
$$p\to q\ \equiv\ \lnot p\lor q,\qquad p\to q\ \equiv\ \lnot q\to\lnot p$$

**The boxed one deserves attention.** The negation of a conditional is **not** a conditional — it is a conjunction. "It is not the case that if Jerry receives a scholarship he goes to college" means *Jerry receives a scholarship **and** does not go to college.* Writing $\lnot(p\to q)$ as $p\to\lnot q$ is wrong, and it is a common slip.

> [!example]- Why this is immediately practical: De Morgan in code
> Johnsonbaugh's Example 1.3.12. In Java, `!(x >= 10 && x <= 20)` — with $p$: `x >= 10` and $q$: `x <= 20`, this is $\lnot(p\land q)$, which by De Morgan is $\lnot p\lor\lnot q$, i.e. **`x < 10 || x > 20`**.
>
> Every time you simplify a compound `if` condition, or invert a pandas boolean mask, you are applying De Morgan. In pandas the same law reads `~((df.a >= 10) & (df.a <= 20))` $\equiv$ `(df.a < 10) | (df.a > 20)` — and **getting it wrong silently returns the wrong rows** rather than raising an error, which is why the law is worth knowing rather than rediscovering.

### 4. Arguments and rules of inference

An **argument** is a sequence of propositions
$$p_1,p_2,\dots,p_n\ /\therefore\ q$$
where $p_1,\dots,p_n$ are the **hypotheses** (or premises) and $q$ the **conclusion**; $\therefore$ is read "therefore". The argument is **valid** provided that *if all the hypotheses are true, then $q$ must also be true.* Otherwise it is **invalid**, or a **fallacy**.

> [!warning] Validity is not truth
> A valid argument does **not** assert that its conclusion is true — only that *if you grant the hypotheses, you must grant the conclusion.* **An argument is valid because of its form, not its content.** Johnsonbaugh's opening example — *all mathematicians wear sandals; anyone who wears sandals is an algebraist; therefore all mathematicians are algebraists* — is perfectly valid and has a false conclusion, because a premise is false.
>
> Conversely, an argument with a true conclusion can be invalid. **Never grade an argument by whether you agree with where it ends up.**

**The seven rules of inference** (Johnsonbaugh's Table 1.4.1). Each is a short valid argument, verifiable by truth table:

| Rule | Form |
|---|---|
| **Modus ponens** (law of detachment) | $p\to q,\ p\ /\therefore q$ |
| **Modus tollens** | $p\to q,\ \lnot q\ /\therefore\lnot p$ |
| **Hypothetical syllogism** | $p\to q,\ q\to r\ /\therefore p\to r$ |
| **Disjunctive syllogism** | $p\lor q,\ \lnot p\ /\therefore q$ |
| Addition | $p\ /\therefore p\lor q$ |
| Simplification | $p\land q\ /\therefore p$ |
| Conjunction | $p,\ q\ /\therefore p\land q$ |

The first four do the real work. **Modus tollens is the contrapositive in action**, and it is how proof by contraposition operates step by step.

**The two classic fallacies**, both of which look like rules and are not:

$$\underbrace{p\to q,\ q\ /\therefore p}_{\textbf{affirming the conclusion}}\qquad\qquad \underbrace{p\to q,\ \lnot p\ /\therefore\lnot q}_{\textbf{denying the hypothesis}}$$

Both are the converse error of §3 in argument form. Johnsonbaugh's illustration of the first is memorable: *"If $2=3$, then I ate my hat. I ate my hat. Therefore $2=3$."* Take $p$ false and $q$ true and both hypotheses hold while the conclusion fails.

**Chaining rules is how a proof is built.** An extended argument is valid provided every intermediate step is. Johnsonbaugh's Example 1.4.5: from $p\lor q$, $r$, $r\to\lnot q$, conclude $p$ — modus ponens on the last two gives $\lnot q$, then disjunctive syllogism with $p\lor q$ gives $p$. That two-step pattern *is* what a written proof looks like once the prose is stripped away.

### 5. Quantifiers

Most interesting mathematical statements contain variables and so are not propositions at all.

> [!note] Definition — propositional function
> Let $P(x)$ be a statement involving a variable $x$, and let $D$ be a set. $P$ is a **propositional function** (or **predicate**) with **domain of discourse** $D$ if $P(x)$ is a proposition for each $x\in D$.

$P$ by itself is neither true nor false; $P(x)$ for a specific $x$ is. **The domain of discourse is part of the statement, not decoration** — "$x^2\ge x$" is true for all $x\in\mathbb Z$ and false for $x\in\mathbb R$ (take $x=\tfrac12$).

| | Statement | Notation | True when | False when |
|---|---|---|---|---|
| **universal** | for every $x$, $P(x)$ | $\forall x\,P(x)$ | $P(x)$ true for **every** $x\in D$ | $P(x)$ false for **at least one** $x$ |
| **existential** | there exists $x$ with $P(x)$ | $\exists x\,P(x)$ | $P(x)$ true for **at least one** $x$ | $P(x)$ false for **every** $x$ |

An $x\in D$ making $P(x)$ false is a **counterexample** to $\forall x\,P(x)$.

> [!warning] The asymmetry of proof and disproof
> **To prove $\forall x\,P(x)$** you must handle every $x$ — typically by letting $x$ be *arbitrary* and reasoning without further assumption. **To disprove it, one counterexample suffices.** And the reverse holds for $\exists$: one witness proves it, but refuting it requires an argument about all of $D$.
>
> This asymmetry is why $\forall x(x^2-1>0)$ falls to the single value $x=1$, and it is the practical content of the whole $\forall/\exists$ distinction.

In $P(x)$ the variable $x$ is **free** — free to roam over $D$. In $\forall x\,P(x)$ it is **bound** by the quantifier. **A statement with a free variable is not a proposition; a statement with all variables bound is.**

**Negation — generalised De Morgan laws:**

$$\boxed{\ \lnot\forall x\,P(x)\equiv\exists x\,\lnot P(x),\qquad \lnot\exists x\,P(x)\equiv\forall x\,\lnot P(x)\ }$$

In words: *the negation of "all are" is "some is not"*, and *the negation of "some is" is "none is"*. To negate, **swap each quantifier and negate the inside.** Note the exact parallel with $\lnot(p\land q)\equiv\lnot p\lor\lnot q$ — a universal quantifier is a long conjunction, an existential a long disjunction.

### 6. Nested quantifiers — and why order matters

With two variables there are four quantifications, and **they do not say the same thing.** Take $D=\mathbb R$ and $P(x,y)$: $x+y=0$.

| Statement | Meaning | Truth |
|---|---|---|
| $\forall x\,\exists y\ (x+y=0)$ | every $x$ has *some* $y$ cancelling it | **True** — take $y=-x$ |
| $\exists y\,\forall x\ (x+y=0)$ | *one* $y$ cancels *every* $x$ | **False** — no single $y$ works |
| $\forall x\,\forall y\ (x+y=0)$ | all pairs sum to zero | False |
| $\exists x\,\exists y\ (x+y=0)$ | some pair sums to zero | True |

**$\forall x\exists y$ and $\exists y\forall x$ are genuinely different statements**, and the second is stronger: it demands a single witness that works uniformly. Reading the quantifiers left to right and asking *"does $y$ get to depend on $x$?"* settles it every time — under $\forall x\exists y$ it does; under $\exists y\forall x$ it does not.

> [!note] This distinction is not academic
> It is exactly the difference between **pointwise** and **uniform** convergence in analysis, between a bound that holds *for each* input and one that holds *for all* inputs at once, and — in [[04 - Algorithms and Their Analysis|ch. 04]] — between "for every input size there is some constant" and "there is a constant working for every input size", which is what big-O actually asserts. **Getting the order wrong changes the theorem.**

**Negating nested quantifiers** is mechanical: swap every quantifier and negate the predicate.
$$\lnot\big(\forall x\,\exists y\ P(x,y)\big)\ \equiv\ \exists x\,\forall y\ \lnot P(x,y).$$

Verify against the table: the first row is true, so its negation — "some $x$ has no $y$ cancelling it" — must be false, and it is.

## ✏️ Exercises

**1. (Set algebra.)** Let $U=\{1,2,\dots,12\}$, let $A$ be the even elements of $U$, $B$ the multiples of 3, and $C=\{1,2,3,4,5,6\}$. (a) List $A\cup B$, $A\cap B$, $A-C$ and $\overline A$. (b) Verify the distributive law $A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$ by computing both sides. (c) Verify De Morgan's law $\overline{A\cup B}=\overline A\cap\overline B$. (d) Give $|A\times C|$ and $|\mathcal P(B)|$.

> [!example]- Solution
> $A=\{2,4,6,8,10,12\}$, $B=\{3,6,9,12\}$, $C=\{1,2,3,4,5,6\}$.
>
> **(a)** $A\cup B=\{2,3,4,6,8,9,10,12\}$; $\ A\cap B=\{6,12\}$; $\ A-C=\{8,10,12\}$; $\ \overline A=\{1,3,5,7,9,11\}$.
>
> **(b)** $B\cup C=\{1,2,3,4,5,6,9,12\}$, so $A\cap(B\cup C)=\{2,4,6,12\}$. On the other side, $A\cap B=\{6,12\}$ and $A\cap C=\{2,4,6\}$, whose union is $\{2,4,6,12\}$. **Equal** ✓
>
> **(c)** $\overline{A\cup B}=U-\{2,3,4,6,8,9,10,12\}=\{1,5,7,11\}$. And $\overline A=\{1,3,5,7,9,11\}$, $\overline B=\{1,2,4,5,7,8,10,11\}$, so $\overline A\cap\overline B=\{1,5,7,11\}$. **Equal** ✓
>
> *(Read the result: $\overline{A\cup B}$ is the numbers divisible by neither 2 nor 3 — namely $1,5,7,11$. Note they are $1$ together with the primes above 3 up to 12, which is not an accident: it is the start of the sieve of Eratosthenes, and [[05 - Number Theory and Cryptography|ch. 05]] returns to it.)*
>
> **(d)** $|A\times C|=|A|\cdot|C|=6\cdot6=\mathbf{36}$. $\ |\mathcal P(B)|=2^{|B|}=2^4=\mathbf{16}$.
>
> All parts verified by direct computation. **The habit worth taking from (b) and (c):** a set identity is checked by computing *both sides independently* and comparing, never by transforming one into the other and trusting the algebra.

**2. (Truth tables and equivalence.)** (a) Build one truth table containing $p\to q$, its converse $q\to p$, its contrapositive $\lnot q\to\lnot p$, and $p\land\lnot q$. (b) Read off which of these are logically equivalent to $p\to q$. (c) Use the table to write the negation of *"If it rains, the match is cancelled"* in idiomatic English. (d) Explain why *"If $2+2=5$, then I am the Pope"* is **true**.

> [!example]- Solution
> **(a)**
> $$\begin{array}{cc|cccc} p&q& p\to q & q\to p & \lnot q\to\lnot p & p\land\lnot q\\\hline \text T&\text T& \text T & \text T & \text T & \text F\\ \text T&\text F& \textbf{F} & \text T & \textbf{F} & \textbf{T}\\ \text F&\text T& \text T & \textbf{F} & \text T & \text F\\ \text F&\text F& \text T & \text T & \text T & \text F \end{array}$$
>
> **(b)** Comparing columns:
> - **$\lnot q\to\lnot p$ matches $p\to q$ in all four rows** — the **contrapositive is equivalent** ✓
> - **$q\to p$ differs in rows 2 and 3** — the **converse is not equivalent** ✓
> - $p\land\lnot q$ is the exact complement of $p\to q$, so $\lnot(p\to q)\equiv p\land\lnot q$ ✓
>
> **(c)** With $p$: it rains, $q$: the match is cancelled, the statement is $p\to q$ and its negation is $p\land\lnot q$:
> $$\textbf{``It rains and the match is not cancelled.''}$$
> Note what the negation is **not**: it is not "if it rains the match is not cancelled", and not "if it does not rain the match is cancelled". **The negation of a conditional is a conjunction** — an actual counterexample, a rainy day with the match still on.
>
> **(d)** The hypothesis $2+2=5$ is **false**, so the conditional falls in row 3 or 4 of the table, where $p\to q$ is **true** regardless of $q$ — it is **vacuously true**. Nothing is being claimed about the papacy: a conditional with a false hypothesis makes no demand on its conclusion, because it can never be tested.
>
> This is the row that feels wrong and is indispensable. Without it, $\forall x\,(x>2\to x^2>4)$ could not be true — it would fail at every $x\le2$, where the hypothesis does not hold. **Vacuous truth is what lets universally quantified conditionals mean what we want them to mean.**

**3. (Inclusion–exclusion.)** Of 120 data science students: 65 use Python, 50 use R, 40 use SQL; 25 use Python and R, 20 use Python and SQL, 15 use R and SQL; and 8 use all three. How many use (a) at least one, (b) none, (c) Python only, (d) exactly two of the three? (e) Check your answers are consistent.

> [!example]- Solution
> Write $|P|=65$, $|R|=50$, $|S|=40$, $|P\cap R|=25$, $|P\cap S|=20$, $|R\cap S|=15$, $|P\cap R\cap S|=8$.
>
> **(a)** Three-set inclusion–exclusion:
> $$|P\cup R\cup S|=|P|+|R|+|S|-|P\cap R|-|P\cap S|-|R\cap S|+|P\cap R\cap S|$$
> $$=65+50+40-25-20-15+8=155-60+8=\mathbf{103}.$$
> *(Why the last term returns: subtracting the three pairwise overlaps removes the triple overlap three times, having added it three times — so it has been removed entirely and must be added back once.)*
>
> **(b)** None: $120-103=\mathbf{17}$.
>
> **(c)** Python only $=|P|-|P\cap R|-|P\cap S|+|P\cap R\cap S|=65-25-20+8=\mathbf{28}$. *(Same logic one level down: the students in both other pairs were double-subtracted.)*
>
> **(d)** Exactly two $=(25-8)+(20-8)+(15-8)=17+12+7=\mathbf{36}$.
>
> **(e)** Partition the 103 by how many tools they use:
> $$\underbrace{59}_{\text{exactly one}}+\underbrace{36}_{\text{exactly two}}+\underbrace{8}_{\text{all three}}=103\ \checkmark$$
> where exactly one $=103-36-8=59$. All figures verified computationally.
>
> **The check in (e) is the point of the exercise.** The three counts *must* partition the union — the categories are disjoint and exhaustive by construction (§1). If they do not sum correctly, the data are inconsistent or you have miscounted, and you find out immediately. [[06 - Counting Methods and the Pigeonhole Principle|Ch. 06]] generalises this to $n$ sets with alternating signs.

**4. (English into logic.)** Let $c$: *the model converges*, $r$: *the learning rate is small*, $d$: *the data are normalised*. Write each of the following symbolically, then say which are equivalent to each other. (a) The model converges only if the learning rate is small. (b) A small learning rate is sufficient for convergence. (c) A small learning rate is necessary for convergence. (d) The model converges if the data are normalised and the learning rate is small. (e) The model does not converge unless the data are normalised.

> [!example]- Solution
> | | Symbolic | Reasoning |
> |---|---|---|
> | **(a)** | $c\to r$ | **"$p$ only if $q$" is $p\to q$.** Convergence forces a small rate; it does not say a small rate forces convergence |
> | **(b)** | $r\to c$ | A *sufficient* condition is the **hypothesis** — it guarantees the conclusion |
> | **(c)** | $c\to r$ | A *necessary* condition is the **conclusion** — it is implied |
> | **(d)** | $(d\land r)\to c$ | "$q$ **if** $p$" is $p\to q$; the hypothesis is the conjunction |
> | **(e)** | $c\to d$ | "not $X$ unless $Y$" = "if $Y$ fails then $X$ fails" = $\lnot d\to\lnot c$, whose **contrapositive** is $c\to d$ |
>
> **Equivalences: (a) $\equiv$ (c).** "Only if" and "is necessary for" say the same thing — both put the condition in the conclusion. **(b) is the converse of these and is *not* equivalent to them**, which is the whole point of the exercise: (a)/(c) and (b) are the two directions people routinely swap.
>
> (e) is equivalent to $\lnot d\to\lnot c$ by contraposition — worth writing both ways, since "unless" is easiest to handle by first rendering it as "if not … then not".
>
> **Sanity check on (a) vs (b) with content.** A small learning rate is genuinely *necessary* for convergence (too large and gradient descent diverges — [[Optimization/contents/05 - Gradient Methods|Optimization ch. 05]] proves the threshold $\alpha<2/\lambda_{\max}$) but nowhere near *sufficient*: a tiny rate on unnormalised, badly conditioned data may not converge in any practical time. **So (a)/(c) are true of gradient descent and (b) is false** — which is exactly why the distinction is worth being fussy about.

**5. (Hard — nested quantifiers.)** Let the domain of discourse be $\mathbb Z^+$ and let $P(x,y)$ be "$x<y$". (a) Determine the truth of $\forall x\,\exists y\,P(x,y)$ and of $\exists y\,\forall x\,P(x,y)$, with justification. (b) Write the negation of each, and confirm the negations have the opposite truth values. (c) Now let the domain be $\{1,2,3\}$ and re-answer (a). (d) Explain what (c) shows about the role of the domain of discourse.

> [!example]- Solution
> **(a)** Over $\mathbb Z^+$:
> - **$\forall x\,\exists y\,(x<y)$ is TRUE.** Let $x$ be an arbitrary positive integer and take $y=x+1$; then $x<y$. Since $x$ was arbitrary, the statement holds for all $x$. *(Note $y$ was allowed to depend on $x$ — that is what the quantifier order permits.)*
> - **$\exists y\,\forall x\,(x<y)$ is FALSE.** It asserts a single positive integer exceeding *every* positive integer. For any candidate $y$, take $x=y$: then $x<y$ fails. So every candidate has a counterexample, and no witness exists. *(In words: $\mathbb Z^+$ has no largest element.)*
>
> **This is the whole lesson.** The two statements differ in truth value while containing the same symbols in a different order, so **quantifier order is part of the meaning.**
>
> **(b)** Swap each quantifier and negate the predicate; $\lnot(x<y)$ is $x\ge y$.
> $$\lnot\forall x\,\exists y\,(x<y)\ \equiv\ \exists x\,\forall y\,(x\ge y),\qquad \lnot\exists y\,\forall x\,(x<y)\ \equiv\ \forall y\,\exists x\,(x\ge y).$$
> - The first reads "**some** positive integer is $\ge$ **every** positive integer" — i.e. $\mathbb Z^+$ has a largest element. **FALSE** ✓ (opposite of the TRUE original).
> - The second reads "for **every** $y$ there is **some** $x$ with $x\ge y$" — take $x=y$. **TRUE** ✓ (opposite of the FALSE original).
>
> Both flips confirmed, which is the check worth doing whenever you negate something with two quantifiers.
>
> **(c)** Over $D=\{1,2,3\}$:
> - **$\forall x\,\exists y\,(x<y)$ becomes FALSE.** Take $x=3$: there is no $y\in D$ with $3<y$. So $x=3$ is a **counterexample**, and one counterexample is all it takes.
> - **$\exists y\,\forall x\,(x<y)$ is still FALSE** — for $y=3$ the choice $x=3$ fails, and smaller $y$ fail sooner. *(In fact on any finite set with $\ge1$ element both statements are false, since the maximum element defeats the first and is undefeated in the second.)*
>
> **(d)** The first statement **changed truth value when only the domain changed** — the predicate and the quantifier structure were untouched. So:
>
> **The domain of discourse is part of the statement, not context around it.** $\forall x\exists y\,(x<y)$ is not true or false in the abstract; it is true over $\mathbb Z^+$, $\mathbb Z$, $\mathbb Q$ and $\mathbb R$, and false over any finite set. What it actually asserts is *"the domain has no maximum element"* — a property of the domain, expressed in the predicate's clothing.
>
> **This is why a quantified statement should never be written without its domain**, and why "$x^2\ge x$" is a genuinely different claim over $\mathbb Z$ (true) and over $\mathbb R$ (false at $x=\tfrac12$). It is also the first appearance of a theme running through [[08 - Graph Theory|ch. 08]] and [[09 - Trees|ch. 09]]: many theorems are really statements about *which structures* satisfy a property, not about the property itself.

## 📝 Summary

- **A set is determined by its elements**; order and duplicates are irrelevant. Set-builder notation puts the membership property after the bar: $\{x\mid \dots\}$. $|\{\emptyset\}|=1$, not $0$.
- **To prove $X=Y$, prove two inclusions.** To disprove it, exhibit **one** element on the wrong side of **one** direction. This is the shape of every set proof in the subject.
- **The set operations obey a full algebra** — associative, commutative, **both distributive laws**, identity, complement, idempotent, bound, absorption, involution, 0/1, and **De Morgan**: $\overline{A\cup B}=\overline A\cap\overline B$. Venn diagrams *suggest* identities; they do not prove them.
- $|X\times Y|=|X|\cdot|Y|$ and $|\mathcal P(X)|=2^{|X|}$ — the multiplication principle and the subset count, arriving early from [[06 - Counting Methods and the Pigeonhole Principle|ch. 06]].
- **A partition** splits a set into nonempty pieces with every element in **exactly one**. [[03 - Functions, Sequences and Relations|Ch. 03]] shows partitions and equivalence relations are the same thing.
- **"Or" is inclusive**, and connected propositions need not be related in meaning. Precedence: $\lnot$, then $\land$, then $\lor$, and **$\to$ last**.
- **$p\to q$ is false only when $p$ is true and $q$ is false.** A false hypothesis makes it **vacuously true** — the row that feels wrong and is indispensable.
- **Five phrasings of $p\to q$:** *if $p$ then $q$*; *$q$ if $p$*; **$p$ only if $q$**; *$q$ is necessary for $p$*; *$p$ is sufficient for $q$*. **Necessary = implied (conclusion); sufficient = implies (hypothesis).**
- **The contrapositive $\lnot q\to\lnot p$ is equivalent; the converse $q\to p$ is not.** The first licenses proof by contraposition; the second is the most common reasoning error in mathematics — and is $P(A\mid B)$ versus $P(B\mid A)$ in disguise.
- **$\lnot(p\to q)\equiv p\land\lnot q$** — the negation of a conditional is a **conjunction**, i.e. an explicit counterexample. And $p\leftrightarrow q\equiv(p\to q)\land(q\to p)$, which is the instruction for proving any "iff" theorem.
- **An argument is valid if true hypotheses force a true conclusion — because of its form, not its content.** Validity is not truth: a valid argument can have a false conclusion, and an invalid one a true conclusion.
- **The four rules that matter:** modus ponens, modus tollens, hypothetical syllogism, disjunctive syllogism. **The two fallacies:** affirming the conclusion ($p\to q,q\therefore p$) and denying the hypothesis ($p\to q,\lnot p\therefore\lnot q$).
- **A propositional function is not a proposition until quantified**, and its **domain of discourse is part of the statement.** $\forall x\,P(x)$ falls to one counterexample; $\exists x\,P(x)$ needs one witness.
- **Negation swaps quantifiers and negates inside:** $\lnot\forall x\,P(x)\equiv\exists x\,\lnot P(x)$, $\ \lnot\exists x\,P(x)\equiv\forall x\,\lnot P(x)$.
- **$\forall x\exists y$ and $\exists y\forall x$ are different statements**, the second being stronger. Ask: *may $y$ depend on $x$?* This is pointwise versus uniform, and it is what big-O really asserts in [[04 - Algorithms and Their Analysis|ch. 04]].

## ⚠️ Important Notes

1. **$\{\emptyset\}$ is not $\emptyset$.** The first has one element; the second has none. Likewise $\{\{a\},\{a,b\},a,b\}$ has **four** elements, two of them sets. Counting elements of sets-containing-sets is a reliable exam question.
2. **$\in$ and $\subseteq$ are different relations.** $1\in\{1,2\}$ but $1\not\subseteq\{1,2\}$; $\{1\}\subseteq\{1,2\}$ but $\{1\}\notin\{1,2\}$. Writing one for the other is the most common notational error in the chapter.
3. **$\emptyset\subseteq X$ for every $X$**, vacuously — there is no element of $\emptyset$ to check. And $X\subseteq X$ always. Both follow from §3's vacuous truth, which is why the logic is placed alongside the sets.
4. **A Venn diagram is not a proof.** It is excellent for forming a conjecture and useless as justification; with four sets it cannot even be drawn with circles.
5. **"Or" is inclusive unless stated otherwise.** If you mean exclusive-or, say so, and remember it is $\lnot(p\leftrightarrow q)$.
6. **Write the parentheses.** Precedence rules exist ($\lnot$, $\land$, $\lor$, $\to$) but relying on them makes expressions unreadable and errors invisible. $\lnot p\lor q$ and $\lnot(p\lor q)$ are different propositions.
7. **The negation of a conditional is never a conditional.** $\lnot(p\to q)\equiv p\land\lnot q$, not $p\to\lnot q$. This one slip invalidates whole proofs.
8. **Never confuse a statement with its converse.** Contrapositive: equivalent. Converse: not. If you find yourself proving the converse of what was asked, you have proved a different theorem.
9. **"Only if" introduces the conclusion, not the hypothesis.** "$p$ only if $q$" is $p\to q$. Reading it as $q\to p$ is the single highest-frequency translation error, and "unless" is nearly as bad — convert it to "if not … then not" and take the contrapositive.
10. **Necessary and sufficient are opposite directions.** *Necessary* $\Rightarrow$ it is the **conclusion**; *sufficient* $\Rightarrow$ it is the **hypothesis**. If you cannot remember which, ask "could the thing happen without it?" (necessary) versus "does it guarantee the thing?" (sufficient).
11. **Validity is about form, truth about content.** Do not accept an argument because you like its conclusion, or reject it because you do not. Check whether the *form* forces the conclusion.
12. **Affirming the conclusion is the fallacy that hides best.** "The test is positive; the test is positive when you have the disease; therefore you have the disease" is $p\to q,q\therefore p$ — invalid, and it is precisely the base-rate fallacy of [[Probability Theory/contents/03 - Conditional Probability and Independence|Probability Theory ch. 03]].
13. **State the domain of discourse.** A quantified statement without one is incomplete, and Exercise 5 shows the truth value can flip when only the domain changes.
14. **One counterexample kills a universal claim.** Do not build an elaborate argument when a single value will do — and conversely, do not think three confirming examples establish $\forall x\,P(x)$.
15. **Quantifier order is part of the statement.** $\forall x\exists y$ lets $y$ depend on $x$; $\exists y\forall x$ demands one $y$ for all. Swapping them is not a stylistic choice and usually changes the theorem — including in the definition of big-O, of convergence, and of continuity.
16. **De Morgan is the law you will actually use.** In code, in pandas masks, in SQL `WHERE` clauses, and in every negated compound condition. Its failure mode is silent — the wrong rows, not an error message.

> [!warning] Gaps in the source material
> **Extraction quality is excellent and this chapter needed almost no reconstruction** — Johnsonbaugh's PDF is born-digital and `∈`, `∉`, `∪`, `∩`, `⊆`, `∅`, `∀`, `∃`, `≡`, `→`, `↔`, `∧`, `∨`, `¬` and `∴` all survive intact. This is the cleanest textbook in the vault; see `00-Index.md` for the full quirk list.
>
> **One dangerous exception, and it hits this chapter hardest: overlines are silently deleted.** Set complement $\overline A$ extracts as plain `A`, so Theorem 1.1.22's complement, involution and De Morgan laws arrive as `A ∪A = U`, `A = A` and `(A ∪B) = A ∩B` — **statements that are false as written rather than visibly garbled.** Every complement in §1's table was restored by hand from the law's name and its standard form. **If you compare this note against the PDF's extracted text, expect the PDF to look wrong.**
>
> **Also lost: all truth-table bodies.** Johnsonbaugh's tables extract as run-together headers with no rows — Definition 1.2.3's table appears as the single string `pqp ∧q`, and Example 1.4.2's as `pqp → qpq`. **Every truth table in this note was constructed from the definition and then verified computationally** (the four-column table of Exercise 2 was generated and checked programmatically, confirming that the contrapositive matches $p\to q$ in all four rows, the converse differs in rows 2 and 3, and $\lnot(p\to q)\equiv p\land\lnot q$).
>
> **All figures are images and are lost**: Figure 1.1.1 (the number-set table — recoverable, its content is in the prose), Figures 1.1.3–1.1.7 (**every Venn diagram**), Figure 1.1.8 (the $|X\times Y|$ tree diagram), and Figure 1.2.1 (a Google search screenshot). The Venn diagrams are the real loss, since §1's operations are conventionally taught through them; the notes give the set-builder definitions instead, which is what a proof needs anyway.
>
> **Verification performed.** All of Exercise 1's set computations, Exercise 2's complete truth table, Exercise 3's inclusion–exclusion figures (union 103, none 17, Python-only 28, exactly-two 36, exactly-one 59, and the partition check $59+36+8=103$), and Exercise 5's quantifier claims over both $\mathbb Z^+$ and $\{1,2,3\}$ were computed and confirmed programmatically before being written. **No error was found in Johnsonbaugh ch. 1.**
>
> **Additions beyond the source.** The **De Morgan-in-pandas** callout extends Johnsonbaugh's Java example to the tool the reader actually uses. The observation that the converse error **is** $P(A\mid B)$ versus $P(B\mid A)$, and that affirming the conclusion **is** the base-rate fallacy, are mine — the book never connects its logic to statistics. The remark in §6 that quantifier order is what distinguishes pointwise from uniform statements, and that **big-O is itself a nested-quantifier statement**, is an addition pointing forward to ch. 04. Exercise 4 is my own construction, deliberately using gradient descent so that the necessary/sufficient distinction has real content rather than being a grammar drill. The note in Exercise 1(c) that $\overline{A\cup B}=\{1,5,7,11\}$ is the beginning of the sieve of Eratosthenes is also mine.
>
> **Not covered from this chapter.** Johnsonbaugh's §1.1 "Problem-Solving Corner: Quantifiers" (book p. 57) is a worked-example section rather than new material, and its content is distributed through §§5–6 and Exercise 5. **§3.6-style applications and the Web-search discussion (Example 1.2.13) are omitted** as dated — the point that search engines implement Boolean connectives is made in the pandas callout instead.

**Previous:** [[00-Index]] · **Next:** [[02 - Proofs and Mathematical Induction]]
