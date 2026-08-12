---
subject: Probability Theory
chapter: 02
tags: [ds, probability, axioms, sample-space, inclusion-exclusion, set-theory]
source: "Ross, *A First Course in Probability*, 10th ed., ch. 2 (pp. 34–69)"
---

# Axioms of Probability

> [!abstract] What this chapter is for
> **This is where probability becomes a mathematical object.** [[01 - Combinatorial Analysis|Chapter 1]] taught counting; this chapter says what a probability *is* — and the answer is deliberately minimal:
>
> > **A probability is any function on events satisfying three axioms.** Everything else in the book is a consequence.
>
> **The chapter's central move is philosophical and worth understanding.** The intuitive definition — *"$P(E)$ is the long-run relative frequency of $E$"* — is **rejected as a foundation**, not because it is wrong but because it assumes far too much. Instead we assume three simple things and **prove** the long-run frequency claim later (the strong law of large numbers, [[08 - Limit Theorems|ch. 08]]).
>
> | § | Topic | Why it matters |
> |---|---|---|
> | **2** | Sample spaces, events, **set algebra**, De Morgan | The language everything is written in |
> | **3** | **The three axioms** | The entire foundation, in three lines |
> | **4** | Propositions 4.1–4.4, **inclusion–exclusion** | The workhorses |
> | **5** | **Equally likely outcomes** | Where ch. 01's counting pays off |
> | **6** | Probability as a **continuous set function** | Limits of events |
> | **7** | Probability as a **measure of belief** | The subjective interpretation |

---

## 📘 Main Knowledge

### 1. Sample spaces and events

> [!important] The two basic objects
> **Sample space $S$** — the set of **all possible outcomes** of an experiment whose outcome is not predictable with certainty. *(We do not know what will happen, but we do know the set of things that could.)*
>
> **Event $E$** — **any subset of $S$.** If the realised outcome lies in $E$, we say **$E$ has occurred**.

| Experiment | $S$ | A typical event |
|---|---|---|
| Sex of a newborn | $\{g,b\}$ | $E=\{g\}$: the child is a girl |
| Order of finish, 7 horses | all $7!$ permutations of $(1,\dots,7)$ | outcomes starting with 3: horse 3 wins |
| Flip two coins | $\{(h,h),(h,t),(t,h),(t,t)\}$ | $\{(h,h),(h,t)\}$: first coin is heads |
| Roll two dice | $\{(i,j):i,j=1,\dots,6\}$ — **36 points** | $\{(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)\}$: sum is 7 |
| Lifetime of a transistor (hours) | $\{x:0\le x<\infty\}$ | $\{x:0\le x\le5\}$: lasts at most 5 hours |

> [!note] Note the last row
> **The sample space need not be finite, or even countable.** That is exactly why Axiom 3 is stated for infinite sequences, and why §6 exists.

#### 1a. Operations on events

Because events are **sets**, the set operations all carry meaning:

| Operation | Notation | Occurs when |
|---|---|---|
| **Union** | $E\cup F$ | **$E$ or $F$ or both** occur |
| **Intersection** | $EF$ (also $E\cap F$) | **both** $E$ and $F$ occur |
| **Complement** | $E^c$ | $E$ does **not** occur |
| **Containment** | $E\subset F$ | occurrence of $E$ **implies** occurrence of $F$ |

> [!important] Two definitions to keep straight
> **Null event $\emptyset$** — the event containing no outcomes. **$S^c=\emptyset$**, since the experiment must produce *some* outcome.
>
> **Mutually exclusive** — $E$ and $F$ are mutually exclusive if $EF=\emptyset$: **they cannot both occur.**

> [!example] Reading the operations off the dice example
> $E=\{\text{sum}=7\}$ has 6 outcomes; $F=\{\text{sum}=6\}$ has 5. **$EF=\emptyset$** — a roll cannot sum to both 6 and 7 — so $E$ and $F$ are **mutually exclusive**.
>
> In the two-coin example, with $E$ = "at least 1 head" $=\{(h,h),(h,t),(t,h)\}$ and $F$ = "at least 1 tail" $=\{(h,t),(t,h),(t,t)\}$:
> $$EF=\{(h,t),(t,h)\}=\text{"exactly one head and one tail"}$$

For infinitely many events, $\bigcup_{n=1}^{\infty}E_n$ is the event that **at least one** $E_n$ occurs, and $\bigcap_{n=1}^{\infty}E_n$ that **all** of them do.

#### 1b. The algebra of events

$$\begin{array}{lll}\textbf{Commutative} & E\cup F=F\cup E & EF=FE\\ \textbf{Associative} & (E\cup F)\cup G=E\cup(F\cup G) & (EF)G=E(FG)\\ \textbf{Distributive} & (E\cup F)G=EG\cup FG & EF\cup G=(E\cup G)(F\cup G)\end{array}$$

**These are verified by showing each side contains the same outcomes** — often most easily via Venn diagrams.

> [!warning] The second distributive law has no arithmetic analogue
> $(E\cup F)G=EG\cup FG$ looks like $(a+b)c=ac+bc$ — familiar. **But $EF\cup G=(E\cup G)(F\cup G)$ has no counterpart in ordinary algebra** ($ab+c\ne(a+c)(b+c)$).
>
> **Set operations distribute *both* ways. Arithmetic ones do not.** Do not import intuition from algebra without checking.

#### 1c. De Morgan's laws

> [!important] De Morgan's laws
> $$\boxed{\left(\bigcup_{i=1}^{n}E_i\right)^{\!c}=\bigcap_{i=1}^{n}E_i^c} \qquad\qquad \boxed{\left(\bigcap_{i=1}^{n}E_i\right)^{\!c}=\bigcup_{i=1}^{n}E_i^c}$$
> For two events:
> $$(E\cup F)^c=E^cF^c \qquad\qquad (EF)^c=E^c\cup F^c$$

**Proof of the first law (general $n$).** Suppose $x\in\left(\bigcup_i E_i\right)^c$. Then $x$ is in **no** $E_i$, so $x\in E_i^c$ for **every** $i$, hence $x\in\bigcap_i E_i^c$. Conversely, if $x\in\bigcap_i E_i^c$ then $x\notin E_i$ for any $i$, so $x\notin\bigcup_iE_i$, i.e. $x\in\left(\bigcup_iE_i\right)^c$. $\blacksquare$

**The second law follows from the first**, applied to the events $E_i^c$ and using $(E^c)^c=E$.

> [!tip] The English translation is what you should memorise
> $$\textbf{"not (any)" = "all (not)"} \qquad\qquad \textbf{"not (all)" = "any (not)"}$$
>
> **This is the formal engine behind "count the complement"** from [[01 - Combinatorial Analysis|ch. 01]]. *"At least one occurs"* has complement *"none occurs"* — and **"none" is almost always the easier event to handle.**

---

### 2. The axioms of probability

#### 2a. Why not just use relative frequency?

The tempting definition is

$$P(E)=\lim_{n\to\infty}\frac{n(E)}{n}$$

where $n(E)$ counts occurrences of $E$ in the first $n$ repetitions.

> [!warning] Ross rejects this as a *foundation*, and the reason is subtle
> *"It possesses a serious drawback: **how do we know that $n(E)/n$ will converge** to some constant limiting value that will be the same for each possible sequence of repetitions?"*
>
> Proponents answer that convergence is **assumed as an axiom.** But:
> > *"To assume that $n(E)/n$ will necessarily converge to some constant value seems to be an **extraordinarily complicated assumption**."*
>
> **The alternative is far better science: assume something simple and *prove* the complicated thing.**

> [!important] The intellectual shape of the whole subject
> $$\underbrace{\text{3 simple axioms}}_{\text{ch. 02}} \;\longrightarrow\; \cdots \;\longrightarrow\; \underbrace{\text{the strong law of large numbers}}_{\text{ch. 08}}$$
> **The long-run frequency interpretation is a *theorem*, not a definition.** Keep the intuition — Ross says it *"should always be kept in mind"* — but do not build on it.

#### 2b. The three axioms

> [!important] The three axioms of probability
> For each event $E$ of a sample space $S$, a number $P(E)$ is defined satisfying:
>
> **Axiom 1** $\qquad 0\le P(E)\le1$
>
> **Axiom 2** $\qquad P(S)=1$
>
> **Axiom 3** $\qquad$ For any sequence of **mutually exclusive** events $E_1,E_2,\dots$ (i.e. $E_iE_j=\emptyset$ when $i\ne j$),
> $$P\left(\bigcup_{i=1}^{\infty}E_i\right)=\sum_{i=1}^{\infty}P(E_i)$$

**In words:** probabilities lie between 0 and 1; something must happen; and **for disjoint events, probabilities add.**

> [!important] $P(\emptyset)=0$ is a *consequence*, not an axiom
> Take $E_1=S$ and $E_i=\emptyset$ for $i>1$. These are mutually exclusive with union $S$, so Axiom 3 gives
> $$P(S)=P(S)+\sum_{i=2}^{\infty}P(\emptyset)$$
> which forces $\boxed{P(\emptyset)=0}$. $\blacksquare$
>
> **This is the chapter's method in miniature: assume little, derive the rest.**

**Finite additivity follows too:** for mutually exclusive $E_1,\dots,E_n$,

$$P\left(\bigcup_{1}^{n}E_i\right)=\sum_{i=1}^{n}P(E_i) \tag{3.1}$$

by setting $E_i=\emptyset$ for $i>n$.

> [!warning] Why Axiom 3 is stated for *infinite* sequences
> Ross asks pointedly: *"Axiom 3 is equivalent to Equation (3.1) when the sample space is finite. (Why?)"* — **and then: "the added generality of Axiom 3 is necessary when the sample space consists of an infinite number of points."**
>
> **Countable additivity is strictly stronger than finite additivity**, and it is exactly what §6's continuity result requires. **Without it, you cannot take limits of events** — and limits are the whole of [[08 - Limit Theorems|ch. 08]].

| Example | Setup | Result |
|---|---|---|
| **3a** | Fair coin | $P(\{H\})=P(\{T\})=\tfrac12$ |
| **3a** | Biased: head twice as likely as tail | $P(\{H\})=\tfrac23$, $P(\{T\})=\tfrac13$ |
| **3b** | Fair die | $P(\{i\})=\tfrac16$; $P(\{2,4,6\})=\tfrac16+\tfrac16+\tfrac16=\tfrac12$ **by Axiom 3** |

> [!note] Technical remark — measurability
> When $S$ is **uncountably infinite**, $P(E)$ can only be defined for a class of events called **measurable**. *"However, this restriction need not concern us, as all events of any practical interest are measurable."* **This is where measure theory enters a more advanced course; it changes nothing here.**

---

### 3. Some simple propositions

Four consequences of the axioms, in increasing order of usefulness.

#### 3a. The complement rule

> [!important] Proposition 4.1
> $$\boxed{P(E^c)=1-P(E)}$$

**Proof.** $E$ and $E^c$ are mutually exclusive with $E\cup E^c=S$, so by Axioms 2 and 3, $1=P(S)=P(E)+P(E^c)$. $\blacksquare$

*If $P(\text{head})=\tfrac38$, then $P(\text{tail})=\tfrac58$.*

#### 3b. Monotonicity

> [!important] Proposition 4.2
> $$\text{If } E\subset F, \text{ then } P(E)\le P(F)$$

**Proof.** If $E\subset F$ we may write $F=E\cup E^cF$, a union of **disjoint** events. Axiom 3 gives $P(F)=P(E)+P(E^cF)$, and $P(E^cF)\ge0$. $\blacksquare$

*The probability of rolling a 1 is at most the probability of rolling an odd number.*

> [!tip] The decomposition $F=E\cup E^cF$ is the trick to remember
> **Splitting an event into a piece and "the rest of it" turns a containment into an equation, which Axiom 3 can then attack.** The same manoeuvre proves Proposition 4.3 and the inclusion–exclusion bounds of §3d.

#### 3c. The addition rule

> [!important] Proposition 4.3
> $$\boxed{P(E\cup F)=P(E)+P(F)-P(EF)}$$

**Proof.** Write $E\cup F=E\cup E^cF$ (disjoint), so $P(E\cup F)=P(E)+P(E^cF)$. Also $F=EF\cup E^cF$ (disjoint), so $P(E^cF)=P(F)-P(EF)$. Substitute. $\blacksquare$

> [!tip] The Venn-diagram proof says *why*
> Split $E\cup F$ into three disjoint sections: **I** $=EF^c$ (only $E$), **II** $=EF$ (both), **III** $=E^cF$ (only $F$).
> $$P(E\cup F)=P(\mathrm{I})+P(\mathrm{II})+P(\mathrm{III}), \qquad P(E)=P(\mathrm{I})+P(\mathrm{II}), \qquad P(F)=P(\mathrm{II})+P(\mathrm{III})$$
> **Adding $P(E)+P(F)$ counts region II twice** — hence subtract $P(EF)$ once. **That double-count is the entire content of the formula, and it is what inclusion–exclusion generalises.**

> [!example] Example 4a — J's holiday books
> $P(B_1)=.5$, $P(B_2)=.4$, $P(B_1B_2)=.3$. **Probability she likes neither?**
>
> $$P(B_1\cup B_2)=.5+.4-.3=.6$$
> $$P(B_1^cB_2^c)=P\big((B_1\cup B_2)^c\big)=1-.6=\mathbf{.4}$$
>
> **Note both tools in one line: De Morgan turns "neither" into "not either", then Proposition 4.1 finishes it.**

#### 3d. Inclusion–exclusion

For three events, apply Proposition 4.3 twice with the distributive law in between:

$$P(E\cup F\cup G)=P(E)+P(F)+P(G)-P(EF)-P(EG)-P(FG)+P(EFG)$$

> [!important] Proposition 4.4 — the inclusion–exclusion identity
> $$\boxed{P\left(\bigcup_{i=1}^{n}E_i\right)=\sum_{r=1}^{n}(-1)^{r+1}\sum_{i_1<\cdots<i_r}P(E_{i_1}E_{i_2}\cdots E_{i_r})}$$
> where the inner sum runs over all $\binom nr$ subsets of size $r$ of $\{1,\dots,n\}$.
>
> **In words:** add the probabilities one at a time, subtract them two at a time, add them three at a time, and so on — **alternating signs.**

> [!tip] Ross's non-inductive proof, which explains the alternating signs
> **Take an outcome lying in exactly $m$ of the events** ($m>0$). On the left it is counted **once**. On the right it is counted in $\binom mk$ of the $k$-fold intersections, so its total count is
> $$\binom m1-\binom m2+\binom m3-\cdots\pm\binom mm$$
> **For the identity to hold, this must equal 1.** Since $1=\binom m0$, that is equivalent to
> $$\sum_{i=0}^{m}\binom mi(-1)^i=0$$
> **which is just the binomial theorem** ([[01 - Combinatorial Analysis|ch. 01 §4c]]) with $x=-1$, $y=1$:
> $$0=(-1+1)^m=\sum_{i=0}^{m}\binom mi(-1)^i(1)^{m-i} \quad\blacksquare$$
>
> **The alternating signs of inclusion–exclusion and the alternating signs of $(1-1)^m$ are the same phenomenon.** *(Outcomes in no $E_i$ contribute nothing to either side, so they need no argument.)*

##### The Bonferroni inequalities

> [!important] Truncating inclusion–exclusion gives alternating bounds
> $$P\left(\bigcup_i E_i\right)\le\sum_i P(E_i) \tag{4.1}$$
> $$P\left(\bigcup_i E_i\right)\ge\sum_iP(E_i)-\sum_{j<i}P(E_iE_j) \tag{4.2}$$
> $$P\left(\bigcup_i E_i\right)\le\sum_iP(E_i)-\sum_{j<i}P(E_iE_j)+\sum_{k<j<i}P(E_iE_jE_k) \tag{4.3}$$
>
> **One term → upper bound. Two terms → lower bound. Three → upper. And so on, alternating.**
>
> **(4.1) is known as Boole's inequality.**

**Why the bounds hold.** The key is the disjointification

$$\bigcup_{i=1}^n E_i=E_1\cup E_1^cE_2\cup E_1^cE_2^cE_3\cup\cdots\cup E_1^c\cdots E_{n-1}^cE_n$$

— *at least one $E_i$ occurs if $E_1$ occurs, or $E_1$ doesn't but $E_2$ does, or …* **The right side is a union of disjoint events**, so probabilities add. A short manipulation then gives

$$P\left(\bigcup_i E_i\right)=\sum_iP(E_i)-\sum_iP\left(\bigcup_{j<i}E_iE_j\right) \tag{4.5}$$

**Boole's inequality (4.1) is immediate** since the subtracted term is $\ge0$. **Applying (4.1) to the inner union gives (4.2); applying (4.2) to it gives (4.3)** — and the alternation continues by induction.

> [!tip] Boole's inequality is the most-used result in the chapter
> $$\boxed{P\left(\bigcup_i E_i\right)\le\sum_i P(E_i)}$$
> **It needs no assumptions at all** — no independence, no disjointness. **It is how you bound the chance that *anything* goes wrong**, and it appears throughout [[08 - Limit Theorems|ch. 08]] (and in §6's paradox below, where it delivers the answer in one line).

---

### 4. Sample spaces with equally likely outcomes

> [!important] The equally likely model
> If $S=\{1,2,\dots,N\}$ is finite and all outcomes are equally likely, then $P(\{i\})=\tfrac1N$, and for any event $E$,
> $$\boxed{P(E)=\frac{\text{number of outcomes in }E}{\text{number of outcomes in }S}}$$
>
> **This is where [[01 - Combinatorial Analysis|ch. 01]] cashes out.** Every counting technique becomes a probability technique.

| Example | Question | Answer |
|---|---|---|
| **5a** | Two dice sum to 7 | $\tfrac{6}{36}=\mathbf{\tfrac16}$ |
| **5c** | Committee of 5 from 6 men, 9 women is 3M/2W | $\dfrac{\binom63\binom92}{\binom{15}{5}}=\dfrac{720}{3003}=\mathbf{\tfrac{240}{1001}}$ |

#### 4a. Ordered or unordered? Either works — but be consistent

> [!example] Example 5b — the same problem, two sample spaces
> **3 balls drawn from 6 white and 5 black. Probability of 1 white and 2 black?**
>
> **Ordered view.** $|S|=11\cdot10\cdot9=990$. Favourable: WBB gives $6\cdot5\cdot4=120$; BWB gives $5\cdot6\cdot4=120$; BBW gives $5\cdot4\cdot6=120$.
> $$\frac{120+120+120}{990}=\frac{360}{990}=\mathbf{\tfrac4{11}}$$
>
> **Unordered view.** $|S|=\binom{11}{3}=165$.
> $$\frac{\binom61\binom52}{\binom{11}{3}}=\frac{6\times10}{165}=\frac{60}{165}=\mathbf{\tfrac4{11}}\ ✓$$

> [!important] Why both are legitimate — the argument Ross makes explicitly
> **Each unordered set of 3 balls corresponds to exactly $3!$ ordered outcomes.** So *"if all outcomes are assumed equally likely when the order of selection is noted, then it follows that they remain equally likely when the outcome is taken to be the unordered set."*
>
> **Equal likelihood is preserved because the correspondence is uniform — every unordered outcome maps to the same number ($3!$) of ordered ones.**
>
> > **The rule: choose either representation, but count the numerator and denominator in the *same* one.** Mixing an ordered numerator with an unordered denominator is the classic disaster.

> [!example] Married couples — the same lesson at scale
> **5 people chosen from 20 (= 10 married couples). Probability none are married to each other?**
>
> **Unordered:** choose 5 of the 10 couples to be represented, then 1 of 2 members from each:
> $$P(N)=\frac{\binom{10}{5}2^5}{\binom{20}{5}}$$
>
> **Ordered:** $20\cdot19\cdot18\cdot17\cdot16$ outcomes; favourable ones avoid each chosen person's spouse:
> $$P(N)=\frac{20\cdot18\cdot16\cdot14\cdot12}{20\cdot19\cdot18\cdot17\cdot16}$$
>
> *Ross leaves the verification to the reader.* **Both equal $\tfrac{168}{323}\approx0.520$.** ✓

#### 4b. Two problems with elegant second solutions

> [!example] Example 5d — the special ball
> An urn has $n$ balls, one special. $k$ are withdrawn one at a time. **Probability the special ball is chosen?**
>
> **Solution 1 (unordered):** the $k$ balls drawn are equally likely to be any of the $\binom nk$ sets, and $\binom{1}{1}\binom{n-1}{k-1}$ contain the special one:
> $$\frac{\binom{n-1}{k-1}}{\binom nk}=\boxed{\frac kn}$$
>
> **Solution 2 (decomposition):** let $A_i$ = "the special ball is the $i$th drawn". Each ball is equally likely to be the $i$th, so $P(A_i)=1/n$. The $A_i$ are **mutually exclusive**, so by Axiom 3:
> $$P(\text{special selected})=\sum_{i=1}^{k}P(A_i)=\frac kn$$
>
> > **The second solution is the one to learn.** $k/n$ is obvious in hindsight — *by symmetry, the special ball is as likely to be in any position, and $k$ of the $n$ positions get drawn.* **Look for symmetry before reaching for binomial coefficients.**

> [!example] Example 5e — why colour sequences are equally likely
> $n$ red and $m$ blue balls in a random linear order (all $(n+m)!$ orderings equally likely). **If we record only the colours, are all colour sequences still equally likely?**
>
> **Yes.** Permuting reds among themselves and blues among themselves leaves the colour sequence unchanged, so **every colour sequence corresponds to exactly $n!\,m!$ orderings**, hence has probability $\dfrac{n!\,m!}{(n+m)!}$ — *the same for all of them.*
>
> *Ross's illustration:* with $r_1,r_2,b_1,b_2$, the sequence RBRB arises from exactly $2!\,2!=4$ of the $4!=24$ orderings, giving probability $\tfrac4{24}=\tfrac16$. ✓
>
> > **The general principle: a uniform distribution stays uniform under a map that is exactly $k$-to-1.** Same argument as Example 5b.

#### 4c. Poker and bridge

| Example | Hand | Count | Probability |
|---|---|---|---|
| **5f** | **Straight** (consecutive values, not all one suit) | $10(4^5-4)=10{,}200$ | $\approx\mathbf{.0039}$ |
| **5g** | **Full house** (3 of a kind + a pair) | $13\cdot12\cdot\binom43\binom42=3744$ | $\approx\mathbf{.0014}$ |

> [!tip] How Example 5f is built
> **Fix the values first, then the suits.** For A-2-3-4-5, each of the 5 cards can be any of 4 suits: $4^5$ outcomes. **Subtract the 4 in which all cards share a suit** (those are *straight flushes*, counted separately): $4^5-4$. Multiply by **10** possible starting values (A-2-3-4-5 through 10-J-Q-K-A).
>
> **The full house is built the same way:** $13$ choices for the triple's denomination $\times\,12$ for the pair's $\times\binom43$ suits for the triple $\times\binom42$ for the pair. **Note $13\times12$, not $\binom{13}{2}$ — the triple's denomination and the pair's play different roles, so the choice is ordered.**

> [!example] Example 5h — bridge
> **(a) Some player gets all 13 spades.** $P(E_i)=1\big/\binom{52}{13}$ for each hand $i$, and the $E_i$ are mutually exclusive, so
> $$P\left(\bigcup_{i=1}^4E_i\right)=\frac{4}{\binom{52}{13}}\approx\mathbf{6.3\times10^{-12}}$$
>
> **(b) Each player gets exactly one ace.** Set the aces aside: the other 48 cards split $\binom{48}{12,12,12,12}$ ways, and the 4 aces can be distributed one each in $4!$ ways:
> $$\frac{4!\binom{48}{12,12,12,12}}{\binom{52}{13,13,13,13}}\approx\mathbf{.1055}$$
>
> **Note the use of multinomial coefficients** ([[01 - Combinatorial Analysis|ch. 01 §5]]) — bridge hands are four *labelled* groups.

#### 4d. Two surprising results

> [!example] Example 5i — the birthday problem
> **$n$ people; probability no two share a birthday?** With $365^n$ equally likely outcomes (ignoring 29 February):
> $$P(\text{no match})=\frac{365\cdot364\cdots(365-n+1)}{365^n}$$
>
> | $n$ | $P(\text{at least one match})$ |
> |---|---|
> | 10 | $.117$ |
> | **23** | $\mathbf{.507}$ ← **first $n$ exceeding $\tfrac12$** |
> | 30 | $.706$ |
> | 50 | $\mathbf{.970}$ |
> | 100 | odds better than $3{,}000{,}000:1$ |
>
> > [!important] Why 23 is not really surprising
> > *"Every pair of individuals has probability $\tfrac{365}{365^2}=\tfrac1{365}$ of having the same birthday, and in a group of 23 people there are $\binom{23}{2}=\mathbf{253}$ different pairs."*
> >
> > **You are not comparing 23 to 365 — you are comparing 253 to 365.** The count that matters grows **quadratically** in $n$, not linearly.
> >
> > **This is the single most useful reframing in the chapter**, and it recurs whenever a problem is about *coincidences among pairs*: near-duplicate records, hash collisions, false positives across many tests.

> [!example] Example 5j — the card after the first ace
> **A deck is turned up one card at a time until the first ace appears. Is the next card more likely to be the ace of spades or the two of clubs?**
>
> **They are equally likely — each has probability $\tfrac1{52}$.**
>
> **Proof.** Order the 51 cards other than the ace of spades ($51!$ ways). **For each such ordering there is exactly one place to insert the ace of spades so that it follows the first ace.** So $51!$ of the $52!$ orderings work:
> $$P=\frac{51!}{52!}=\frac1{52}$$
> **The identical argument applies to any specified card.** So *each of the 52 cards is equally likely to be the one following the first ace.*
>
> > [!warning] The two wrong intuitions — and why *both* are wrong
> > **First reaction:** *"the two of clubs is more likely, since the first ace might itself be the ace of spades."* **Correct observation** — there is 1 chance in 4 that the ace of spades **is** the first ace, disqualifying it.
> >
> > **Second reaction:** *"but the two of clubs might appear before the first ace."* **Also correct** — there is 1 chance in 5 that it does (of the 5 cards consisting of the four aces and the two of clubs, each is equally likely to come first).
> >
> > **Both effects are real. They exactly cancel** — which no amount of intuition would tell you. **The full analysis is the only reliable route.**

> [!note] Example 5k — roommates *(worth knowing the shape of, not the algebra)*
> 20 offensive and 20 defensive players are randomly paired into 20 rooms. **Probability of no offensive–defensive pair?**
> $$P_0=\frac{\left[\frac{20!}{2^{10}\,10!}\right]^2}{\frac{40!}{2^{20}\,20!}}=\frac{(20!)^3}{(10!)^2\,40!}\approx\mathbf{1.34\times10^{-6}}$$
> and more generally $P_{2i}$ for $2i$ mixed pairs, with $P_{10}\approx\mathbf{.3459}$ and $P_{20}\approx7.61\times10^{-6}$.
>
> **The instructive detail is the repeated $\dfrac{(2k)!}{2^k\,k!}$**, the number of ways to split $2k$ items into $k$ **unordered** pairs — the [[01 - Combinatorial Analysis|ch. 01 §5]] labelled/unlabelled correction, applied twice.
>
> *(Ross notes these can be approximated using **Stirling's formula**, $n!\approx n^{n+1/2}e^{-n}\sqrt{2\pi}$.)*

#### 4e. Three applications of inclusion–exclusion

> [!example] Example 5l — probability as a counting device
> A club: 36 play tennis, 28 squash, 18 badminton; 22 play tennis **and** squash, 12 tennis and badminton, 9 squash and badminton, 4 play all three. **How many play at least one sport?**
>
> **Introduce probability into a pure counting problem.** Pick a member at random, so $P(C)=|C|/N$. Then
> $$P(T\cup S\cup B)=\frac{36+28+18-22-12-9+4}{N}=\frac{43}{N}$$
> **so 43 members play at least one sport.**
>
> > **The probability was scaffolding — it cancelled out.** *"The introduction of probability enables us to obtain a quick solution to a counting problem."* **Inclusion–exclusion for sets and for probabilities are the same identity.**

> [!example] Example 5m — the matching problem
> **$N$ men throw their hats in a pile and each takes one at random. Probability that nobody gets his own hat?**
>
> Let $E_i$ = "man $i$ gets his own hat". A specific set of $n$ men all getting their own hats leaves $(N-n)!$ arrangements for the rest, so
> $$P(E_{i_1}\cdots E_{i_n})=\frac{(N-n)!}{N!}$$
> and since there are $\binom Nn$ such terms,
> $$\sum_{i_1<\cdots<i_n}P(E_{i_1}\cdots E_{i_n})=\frac{N!}{(N-n)!\,n!}\cdot\frac{(N-n)!}{N!}=\frac1{n!}$$
>
> **Every layer of inclusion–exclusion collapses to $1/n!$** — which is why the answer is so clean:
> $$P\left(\bigcup_iE_i\right)=1-\frac1{2!}+\frac1{3!}-\cdots+(-1)^{N+1}\frac1{N!}$$
> $$\boxed{P(\text{no match})=\sum_{i=0}^{N}\frac{(-1)^i}{i!}\ \longrightarrow\ e^{-1}\approx\mathbf{.3679}}$$
> by $e^x=\sum_i x^i/i!$ at $x=-1$.
>
> > [!important] The answer does not depend on $N$
> > **Whether 5 men or 5 million, the probability nobody gets his own hat is about 37%.** *"How many readers would have incorrectly thought that this probability would go to 1 as $N\to\infty$?"*
> >
> > **Convergence is startlingly fast:** $N=4$ gives $.375$, $N=10$ gives $.36788$ — already correct to 4 decimal places. **This is one of the most quoted results in elementary probability**, and the *derangement* count $D_N=N!\sum_{i=0}^N(-1)^i/i!$ is its combinatorial twin.

> [!example] Example 5n — the round table
> **10 married couples seated randomly at a round table. Probability no wife sits next to her husband?**
>
> There are $19!$ arrangements of 20 people around a round table *(fix one person to kill the rotational symmetry)*. **For a specified set of $n$ couples to be adjacent, glue each into a single entity:** $20-n$ entities give $(20-n-1)!$ circular arrangements, and each glued couple can be ordered $2$ ways:
> $$P(E_{i_1}\cdots E_{i_n})=\frac{2^n(19-n)!}{19!}$$
> Inclusion–exclusion gives
> $$P(\text{at least one couple together})=\sum_{n=1}^{10}(-1)^{n+1}\binom{10}{n}\frac{2^n(19-n)!}{19!}\approx\mathbf{.6605}$$
> **so the answer is $\approx\mathbf{.3395}$.**
>
> **Two techniques worth extracting:** *(i)* **circular arrangements of $k$ objects number $(k-1)!$**, not $k!$; *(ii)* **"must be adjacent" is handled by gluing into one entity and multiplying by the internal orderings.**

> [!note] Example 5o — runs *(asterisked in the source)*
> A team finishes with $n$ wins and $m$ losses. **Assuming all $\binom{n+m}{n}$ orderings equally likely, what is the probability of exactly $r$ runs of wins?** (A *run* is a maximal consecutive block.)
>
> **Both factors come from [[01 - Combinatorial Analysis|ch. 01]]'s Proposition 6.1:** the run sizes $x_1+\cdots+x_r=n$ (all positive) give $\binom{n-1}{r-1}$; the loss gaps $y_1+\cdots+y_{r+1}=m$ (interior ones positive) give $\binom{m+1}{r}$. Hence
> $$\boxed{P(r\text{ runs of wins})=\frac{\binom{m+1}{r}\binom{n-1}{r-1}}{\binom{m+n}{n}}}$$
>
> **The point is statistical, not combinatorial.** With $n=8$, $m=6$: both $r=7$ (WLWLWLWLWWLWLW — alternating) and $r=1$ (WWWWWWWWLLLLLL — one block) have probability $\tfrac1{429}$. **Either extreme is strong evidence that the win probability was *not* constant over the season** — an early glimpse of hypothesis testing ([[Mathematical Statistics/contents/00-Index|Mathematical Statistics]]).

---

### 5. Probability as a continuous set function

> [!important] Increasing and decreasing sequences
> $\{E_n\}$ is **increasing** if $E_1\subset E_2\subset\cdots$, and **decreasing** if $E_1\supset E_2\supset\cdots$. Define
> $$\lim_{n\to\infty}E_n=\bigcup_{i=1}^{\infty}E_i \quad\text{(increasing)}, \qquad\qquad \lim_{n\to\infty}E_n=\bigcap_{i=1}^{\infty}E_i \quad\text{(decreasing)}$$

> [!important] Proposition 6.1 — continuity of probability
> If $\{E_n\}$ is increasing **or** decreasing, then
> $$\boxed{\lim_{n\to\infty}P(E_n)=P\left(\lim_{n\to\infty}E_n\right)}$$
> **$P$ and $\lim$ commute — probability is a continuous set function.**

**Proof sketch (increasing case).** Disjointify: let $F_1=E_1$ and $F_n=E_nE_{n-1}^c$ — *the part of $E_n$ not in any earlier $E_i$.* The $F_n$ are **mutually exclusive** with $\bigcup_1^nF_i=\bigcup_1^nE_i=E_n$. Then

$$P\left(\bigcup_1^{\infty}E_i\right)=P\left(\bigcup_1^{\infty}F_i\right)\overset{\text{Ax.3}}{=}\sum_1^{\infty}P(F_i)=\lim_{n\to\infty}\sum_1^nP(F_i)=\lim_{n\to\infty}P(E_n)$$

**The decreasing case follows by taking complements** — $\{E_n^c\}$ is increasing — and applying De Morgan. $\blacksquare$

> [!tip] This is what Axiom 3's infinite form was for
> **The single step marked "Ax.3" needs *countable* additivity.** Finite additivity would not get you there. **Every limit theorem in [[08 - Limit Theorems|ch. 08]] rests on this proposition.**

> [!example] Example 6a — a "paradox" about infinity
> An infinite urn; at 1 minute to 12, balls 1–10 go in and one comes out; at $\tfrac12$ minute to 12, balls 11–20 go in and one comes out; at $\tfrac14$ minute, and so on. **How many balls at 12 P.M.?**
>
> | Which ball is withdrawn | Balls at 12 P.M. |
> |---|---|
> | **Ball $10n$** at step $n$ | **Infinitely many** — any ball not numbered $10n$ is never withdrawn |
> | **Ball $n$** at step $n$ | **None** — ball $n$ was removed at step $n$, for every $n$ |
> | **A ball chosen at random** | **None, with probability 1** |
>
> **After every finite step all three scenarios have the same number of balls in the urn (namely $9n$). The limits differ completely.**
>
> **The random case, by Proposition 6.1.** Let $E_n$ = "ball 1 still present after $n$ withdrawals". Then
> $$P(E_n)=\frac{9\cdot18\cdot27\cdots(9n)}{10\cdot19\cdot28\cdots(9n+1)}$$
> The $E_n$ are **decreasing**, so
> $$P(\text{ball 1 present at 12})=P\left(\bigcap_nE_n\right)=\lim_nP(E_n)=\prod_{n=1}^{\infty}\frac{9n}{9n+1}$$
> **This product is 0**, because its reciprocal diverges:
> $$\prod_{n=1}^{\infty}\left(1+\frac1{9n}\right)\ge\prod_{n=1}^{m}\left(1+\frac1{9n}\right)>\frac19\sum_{i=1}^{m}\frac1i\ \longrightarrow\ \infty$$
> **using the divergence of the harmonic series.** The same holds for every ball, so with $F_i$ = "ball $i$ present at 12", **Boole's inequality** finishes it:
> $$P\left(\bigcup_iF_i\right)\le\sum_iP(F_i)=0$$
> **With probability 1, the urn is empty at 12 P.M.** $\blacksquare$
>
> > [!warning] There is no actual paradox
> > *"The reason the results are different is not because there is an actual paradox, or mathematical contradiction, but rather because of the logic of the situation, and also that the surprise results because **one's initial intuition when dealing with infinity is not always correct.**"*
> >
> > **The manner of withdrawal matters, even though the count after each finite step does not.** *(Ross notes that Cantor was ridiculed for exactly this class of claim.)*
> >
> > **The transferable lesson: "the limit of the counts" and "the count of the limit" are different questions.** Proposition 6.1 says when they agree for probabilities — a guarantee you do not get for free.

---

### 6. Probability as a measure of belief

**Statements like *"it is 90% probable that Shakespeare wrote Hamlet"* have no long-run frequency reading** — the experiment cannot be repeated.

> [!important] The subjective (personal) interpretation
> $P(E)$ measures **an individual's degree of belief**. And crucially:
>
> > **A measure of degree of belief should satisfy all the axioms of probability.**
>
> *If you are 70% certain Shakespeare wrote Julius Caesar and 10% certain Marlowe did, you should be 80% certain it was one of them* — **which is Axiom 3.**
>
> **Whether probability is read as long-run frequency or as degree of belief, its mathematical properties are unchanged.** *(Everything proved in this book applies under both readings — which is why the axiomatic approach was worth the trouble.)*

> [!example] Example 7a — comparing two bets
> A 7-horse race. Your beliefs: horses 1 and 2 have 20% each; horses 3 and 4 have 15% each; horses 5, 6, 7 have 10% each. **Bet at even money on {1,2,3} or on {1,5,6,7}?**
>
> $$P(\{1,2,3\})=.2+.2+.15=\mathbf{.55} \qquad\qquad P(\{1,5,6,7\})=.2+.1+.1+.1=\mathbf{.50}$$
>
> **The first wager is more attractive** — even though it covers fewer horses. *(The stated beliefs are coherent: they sum to $.2+.2+.15+.15+.1+.1+.1=1$.)*

> [!warning] The idealisation being made
> *"In supposing that a person's subjective probabilities are always consistent with the axioms of probability, we are dealing with an **idealized rather than an actual person**."*
>
> **Real people routinely violate the axioms** — most famously by assigning a *conjunction* higher probability than one of its conjuncts, which Proposition 4.2 forbids. **The axioms describe how beliefs *should* behave, not how they do.**

---

## ✏️ Exercises

> [!note] These exercises are my own construction
> Every figure is either quoted from the text or computed by hand, and **all arithmetic below has been independently verified.**

---

**Exercise 1 — Sample spaces, events, and set algebra**

Two fair dice are rolled; $S=\{(i,j):i,j=1,\dots,6\}$. Define

$$E=\{\text{sum}=7\}, \qquad F=\{\text{first die}=1\}, \qquad G=\{\text{sum}\ge10\}$$

**(i)** List $E$, $F$ and $G$ and give $|S|$.

**(ii)** Find $EF$, $E\cup F$, and $E^cF^c$ (as counts). Which pair among $E,F,G$ is mutually exclusive?

**(iii)** Verify Proposition 4.3 numerically for $E$ and $F$.

**(iv)** Express *"the sum is 7 but the first die is not 1"* in set notation and find its probability.

**(v)** Use De Morgan to rewrite $(E\cup F\cup G)^c$, and state in plain English what that event is.

> [!example]- Solution
> **(i)** $|S|=\mathbf{36}$.
> $$E=\{(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)\} \qquad |E|=6$$
> $$F=\{(1,1),(1,2),(1,3),(1,4),(1,5),(1,6)\} \qquad |F|=6$$
> $$G=\{(4,6),(5,5),(6,4),(5,6),(6,5),(6,6)\} \qquad |G|=6$$
>
> ---
> **(ii)** $EF=\{(1,6)\}$, so $|EF|=\mathbf{1}$. Then $|E\cup F|=6+6-1=\mathbf{11}$, and by De Morgan
> $$|E^cF^c|=|(E\cup F)^c|=36-11=\mathbf{25}$$
>
> **$E$ and $G$ are mutually exclusive:** a sum of 7 cannot also be $\ge10$, so $EG=\emptyset$. *(Note $FG=\emptyset$ too — a first die of 1 caps the sum at 7.)*
>
> ---
> **(iii)** $P(E)=\tfrac6{36}=\tfrac16$, $P(F)=\tfrac16$, $P(EF)=\tfrac1{36}$:
> $$P(E)+P(F)-P(EF)=\tfrac6{36}+\tfrac6{36}-\tfrac1{36}=\tfrac{11}{36}=P(E\cup F)\ ✓$$
>
> **Note what would go wrong without the subtraction:** $\tfrac{12}{36}=\tfrac13$ would double-count $(1,6)$.
>
> ---
> **(iv)** $EF^c$ (equivalently $E\setminus F$), with $|EF^c|=6-1=5$:
> $$P(EF^c)=\tfrac5{36}$$
> **Or via the decomposition of Proposition 4.2's proof:** $E=EF\cup EF^c$ disjointly, so $P(EF^c)=P(E)-P(EF)=\tfrac6{36}-\tfrac1{36}=\tfrac5{36}$ ✓
>
> ---
> **(v)** $$(E\cup F\cup G)^c=E^cF^cG^c$$
> **In English: the sum is not 7, *and* the first die is not 1, *and* the sum is less than 10.**
>
> > **This is De Morgan doing its real job: converting *"none of these things happens"* into a conjunction you can check outcome by outcome.** It is why "at least one" problems are attacked through their complements.

---

**Exercise 2 — The axioms and the simple propositions**

A student takes three modules. Let $A$, $B$, $C$ be the events of passing each, with

$$P(A)=.5,\quad P(B)=.4,\quad P(C)=.3,\quad P(AB)=.2,\quad P(AC)=.15,\quad P(BC)=.1,\quad P(ABC)=.05$$

**(i)** Find $P(A\cup B\cup C)$ and $P(\text{passes none})$.

**(ii)** Find the probability of passing **exactly one** module, and of passing **at least two**.

**(iii)** Verify these numbers are consistent with the axioms by computing all seven disjoint regions.

**(iv)** A second student reports $P(A)=.5$, $P(B)=.4$, $P(AB)=.45$. **Show this violates the axioms**, naming the proposition breached.

**(v)** Prove that $P(EF)\ge P(E)+P(F)-1$ for any events, and interpret it.

> [!example]- Solution
> **(i)** By inclusion–exclusion for three events:
> $$P(A\cup B\cup C)=.5+.4+.3-.2-.15-.1+.05=\mathbf{.80}$$
> $$P(\text{none})=1-.80=\mathbf{.20}$$
>
> ---
> **(ii)** Compute each region as (event) − (its overlaps) + (triple), then combine:
>
> | Region | Value |
> |---|---|
> | $A$ only $=P(A)-P(AB)-P(AC)+P(ABC)$ | $.5-.2-.15+.05=.20$ |
> | $B$ only | $.4-.2-.1+.05=.15$ |
> | $C$ only | $.3-.15-.1+.05=.10$ |
>
> **Exactly one:** $.20+.15+.10=\mathbf{.45}$
>
> | Region | Value |
> |---|---|
> | $AB$ not $C$ $=P(AB)-P(ABC)$ | $.20-.05=.15$ |
> | $AC$ not $B$ | $.15-.05=.10$ |
> | $BC$ not $A$ | $.10-.05=.05$ |
> | $ABC$ | $.05$ |
>
> **At least two:** $.15+.10+.05+.05=\mathbf{.35}$
>
> *(Check: $.45+.35=.80=P(A\cup B\cup C)$ ✓, and $.80+.20=1$ ✓.)*
>
> ---
> **(iii)** **All seven regions are $\ge0$** (values $.20,.15,.10,.15,.10,.05,.05$) and sum to $.80$, with the eighth region ("none") $=.20$. **Total $=1$.** ✓
>
> > **This is the real consistency check on a set of stated probabilities.** Individual numbers can each look reasonable while implying a **negative** region — which Axiom 1 forbids. **Always decompose into disjoint pieces before trusting a specification.**
>
> ---
> **(iv)** $AB\subset A$, so **Proposition 4.2** requires $P(AB)\le P(A)=.5$ — satisfied. But $AB\subset B$ requires
> $$P(AB)\le P(B)=.4$$
> and $.45>.4$. **Proposition 4.2 (monotonicity) is violated.**
>
> **A second route to the same contradiction.** Proposition 4.3 gives
> $$P(A\cup B)=.5+.4-.45=.45$$
> but $A\subset A\cup B$, so Proposition 4.2 requires $P(A\cup B)\ge P(A)=.5$. **And $.45<.5$.** ✗
>
> **The general rule: $P(EF)\le\min\{P(E),P(F)\}$.**
>
> ---
> **(v)** From Proposition 4.3, $P(EF)=P(E)+P(F)-P(E\cup F)$. By **Axiom 1**, $P(E\cup F)\le1$, so
> $$\boxed{P(EF)\ge P(E)+P(F)-1}$$
> **This is Bonferroni's inequality (the two-event case).** $\blacksquare$
>
> **Interpretation:** *if two events are each very likely, they must very likely occur together.* With $P(E)=P(F)=.95$, the overlap is at least $.90$ — **they cannot be arranged to avoid each other.**
>
> > **This is the workhorse behind multiple-comparison corrections in statistics:** if you want 20 confidence intervals to *all* hold simultaneously at 95%, each must be built at level $1-.05/20$. **Boole's inequality (4.1) is the same statement, complemented.**

---

**Exercise 3 — Equally likely outcomes: ordered vs unordered**

An urn has 4 red, 3 green and 2 blue balls (9 total). Three are drawn without replacement.

**(i)** How many outcomes are there in the **unordered** sample space? In the **ordered** one?

**(ii)** Find $P(\text{all three red})$ in **both** representations and confirm they agree.

**(iii)** Find $P(\text{one of each colour})$ in both representations.

**(iv)** A student computes $P(\text{one of each colour})$ as $\dfrac{4\cdot3\cdot2}{\binom93}=\dfrac{24}{84}$. **Identify the error precisely.**

**(v)** In a 5-card poker hand, compute $P(\text{full house})$ and $P(\text{flush, excluding straight flushes})$, and comment on which is rarer.

> [!example]- Solution
> **(i)** **Unordered:** $\binom93=\mathbf{84}$. **Ordered:** $9\cdot8\cdot7=\mathbf{504}$. *(Note $504=84\times3!$ — each unordered set corresponds to exactly $3!=6$ ordered ones.)*
>
> ---
> **(ii)** **Unordered:** $\dfrac{\binom43}{\binom93}=\dfrac{4}{84}=\mathbf{\tfrac1{21}}$
>
> **Ordered:** $\dfrac{4\cdot3\cdot2}{9\cdot8\cdot7}=\dfrac{24}{504}=\mathbf{\tfrac1{21}}$ ✓
>
> ---
> **(iii)** **Unordered:** $\dfrac{\binom41\binom31\binom21}{\binom93}=\dfrac{4\cdot3\cdot2}{84}=\dfrac{24}{84}=\mathbf{\tfrac27}$
>
> **Ordered:** the three colours can appear in $3!=6$ orders, each contributing $4\cdot3\cdot2=24$:
> $$\frac{6\times24}{504}=\frac{144}{504}=\mathbf{\tfrac27}\ ✓$$
>
> ---
> **(iv)** **The student mixed representations.**
>
> The numerator $4\cdot3\cdot2=24$ counts... **and here it happens to be correct** for the unordered space, since $\binom41\binom31\binom21=24$. **The arithmetic gives the right answer.**
>
> **But the reasoning is unsound**, and would fail immediately on a variant. **If the student intended $4\cdot3\cdot2$ as an *ordered* count** (red first, then green, then blue), it should be paired with the ordered denominator $504$ — giving $\tfrac{24}{504}=\tfrac1{21}$, **which is wrong by a factor of 6** because it counts only *one* colour order.
>
> > **The correct statement of the rule:** $\binom41\binom31\binom21$ is an *unordered* count (choose which red, which green, which blue) and belongs over $\binom93$. **$4\cdot3\cdot2$ read as a sequence is an ordered count and belongs over $9\cdot8\cdot7$, multiplied by $3!$ for the colour orders.**
> >
> > **The numbers coincide here; the logic does not. Getting the right answer for the wrong reason is the most dangerous outcome in combinatorics** — it fails silently on the next problem.
>
> ---
> **(v)** $\binom{52}{5}=2{,}598{,}960$.
>
> **Full house** (Example 5g): $13\cdot12\cdot\binom43\binom42=13\cdot12\cdot4\cdot6=3744$
> $$P=\frac{3744}{2{,}598{,}960}\approx\mathbf{.001441}$$
>
> **Flush, excluding straight flushes:** choose a suit (4) and 5 of its 13 cards, then remove the 40 straight flushes:
> $$4\binom{13}{5}-40=4(1287)-40=5148-40=5108 \qquad P=\frac{5108}{2{,}598{,}960}\approx\mathbf{.001965}$$
>
> **The full house is rarer** ($3744<5108$) — **which is why it outranks a flush in poker.** *(For scale: a straight is $10{,}200$ hands, $\approx.0039$; four of a kind is $13\times48=624$, $\approx.00024$.)*
>
> > **Poker hand rankings are exactly the ordering of these counts.** The game's rules encode a combinatorics calculation done in the 17th century.

---

**Exercise 4 — Inclusion–exclusion and the Bonferroni bounds**

Return to the **matching problem** (Example 5m) with $N=4$ men and hats.

**(i)** Compute $S_r=\sum_{i_1<\cdots<i_r}P(E_{i_1}\cdots E_{i_r})$ for $r=1,2,3,4$, and verify each equals $1/r!$.

**(ii)** Compute the exact $P(\text{at least one match})$ and $P(\text{no match})$.

**(iii)** Compute the first three Bonferroni bounds (4.1)–(4.3) and confirm they bracket the exact answer correctly.

**(iv)** Compare $P(\text{no match})$ for $N=4$ with the limit $e^{-1}$. Comment on the rate of convergence.

**(v)** Explain why Boole's inequality is uninformative here, and give a situation where it is exactly the right tool.

> [!example]- Solution
> **(i)** With $P(E_{i_1}\cdots E_{i_r})=\dfrac{(4-r)!}{4!}$ and $\binom4r$ terms:
>
> | $r$ | $\binom4r$ | $\dfrac{(4-r)!}{4!}$ | $S_r$ | $=1/r!$? |
> |---|---|---|---|---|
> | 1 | 4 | $6/24=1/4$ | $\mathbf{1}$ | $1/1!=1$ ✓ |
> | 2 | 6 | $2/24=1/12$ | $\mathbf{1/2}$ | $1/2!=1/2$ ✓ |
> | 3 | 4 | $1/24$ | $\mathbf{1/6}$ | $1/3!=1/6$ ✓ |
> | 4 | 1 | $1/24$ | $\mathbf{1/24}$ | $1/4!=1/24$ ✓ |
>
> ---
> **(ii)** $$P(\text{at least one})=1-\tfrac12+\tfrac16-\tfrac1{24}=\mathbf{\tfrac58}=0.625$$
> $$P(\text{no match})=1-\tfrac58=\mathbf{\tfrac38}=0.375$$
> **Check against the series:** $\sum_{i=0}^4\frac{(-1)^i}{i!}=1-1+\tfrac12-\tfrac16+\tfrac1{24}=\tfrac38$ ✓
>
> ---
> **(iii)**
>
> | Terms | Bound | Value | Exact $=0.625$ |
> |---|---|---|---|
> | 1 | $\le S_1$ | $\le\mathbf{1.000}$ | ✓ (satisfied, but vacuous) |
> | 2 | $\ge S_1-S_2$ | $\ge\mathbf{0.500}$ | ✓ |
> | 3 | $\le S_1-S_2+S_3$ | $\le\mathbf{0.667}$ | ✓ |
>
> **The bounds alternate around the true value and tighten:** $[0.500,\,0.667]$ after three terms, versus $[0,\,1]$ after one. ✓
>
> ---
> **(iv)** $P(\text{no match})=0.375$ at $N=4$, against $e^{-1}=0.36788$.
>
> | $N$ | $P(\text{no match})$ |
> |---|---|
> | 3 | $.33333$ |
> | 4 | $.37500$ |
> | 5 | $.36667$ |
> | 10 | $.3678794643$ |
> | $\infty$ | $.3678794412$ |
>
> **Convergence is extraordinarily fast** — it is an alternating series with terms $1/i!$, so **the error after $N$ terms is at most $1/(N+1)!$.** At $N=10$ that bound is $1/39{,}916{,}800\approx2.5\times10^{-8}$.
>
> > **Practically: the answer is $\approx0.37$ for any party with more than a handful of guests.** The independence from $N$ is not asymptotic hand-waving — **it is essentially exact from $N=5$ onward.**
>
> ---
> **(v)** **Boole's inequality gives $P(\bigcup E_i)\le S_1=1$ here — completely vacuous**, since every probability is $\le1$ anyway. **It fails because the $E_i$ overlap substantially and $\sum P(E_i)$ is not small.**
>
> **Where it is exactly right: when the events are rare and you need only an upper bound.** Example 6a is the model case — each $P(F_i)=0$, so $P(\bigcup F_i)\le\sum P(F_i)=0$ settles the whole question in one line, **with no need to know how the $F_i$ overlap.**
>
> > **The general principle: Boole's inequality is powerful precisely when $\sum_iP(E_i)$ is small**, e.g. bounding the chance that *any* of many rare failures occurs. **It requires no independence and no disjointness — which is why it survives into settings where nothing else does** ([[08 - Limit Theorems|ch. 08]]).

---

**Exercise 5 — The birthday problem, and continuity of $P$**

**(i)** Write the exact expression for $P(\text{no shared birthday})$ among $n$ people, and evaluate the probability of **at least one** match for $n=10,23,50$.

**(ii)** Show that $n=23$ is the smallest group for which a match is more likely than not.

**(iii)** Explain via the pairs argument why 23 is not surprising.

**(iv)** Now ask a **different** question: what is the probability that someone shares **your** birthday? Find the smallest $n$ making this exceed $\tfrac12$, and explain the enormous gap.

**(v)** Let $E_n$ be the event that ball 1 is still in the urn after $n$ withdrawals in Example 6a. **Is $\{E_n\}$ increasing or decreasing?** State which part of Proposition 6.1 is used and why finite additivity would not suffice.

> [!example]- Solution
> **(i)** $$P(\text{no match})=\frac{365\cdot364\cdots(365-n+1)}{365^n}=\prod_{i=0}^{n-1}\frac{365-i}{365}$$
>
> | $n$ | $P(\text{at least one match})$ |
> |---|---|
> | 10 | $\mathbf{.1169}$ |
> | 23 | $\mathbf{.5073}$ |
> | 50 | $\mathbf{.9704}$ |
>
> ---
> **(ii)** $$n=22:\ P(\text{match})=.4757<\tfrac12 \qquad\qquad n=23:\ P(\text{match})=.5073>\tfrac12$$
> **so 23 is the smallest such group.** ✓ *(This is exactly Ross's claim that the probability of no match drops below $\tfrac12$ at $n\ge23$.)*
>
> ---
> **(iii)** **The comparison that matters is not $23$ against $365$ — it is the number of *pairs* against 365.** Each pair matches with probability $\tfrac1{365}$, and
> $$\binom{23}{2}=\mathbf{253}$$
> **253 pairs against 365 days is no longer surprising at all.**
>
> *(A crude estimate: $1-(1-\tfrac1{365})^{253}\approx1-e^{-253/365}\approx.50$ — remarkably close to the exact $.5073$. The pairs are not independent, so this is heuristic, but it captures the mechanism.)*
>
> > **The number of pairs grows as $\binom n2\approx n^2/2$ — quadratically.** That quadratic growth is the entire explanation.
>
> ---
> **(iv)** Each of the other $n-1$ people misses your birthday with probability $\tfrac{364}{365}$, so
> $$P(\text{someone shares yours})=1-\left(\tfrac{364}{365}\right)^{n-1}$$
>
> | $n$ | Probability |
> |---|---|
> | 23 | $\mathbf{.0586}$ |
> | 50 | $.1258$ |
> | 253 | $.4991$ |
> | **254** | $\mathbf{.5005}$ ← first to exceed $\tfrac12$ |
>
> **You need 254 people — versus 23 for the original question. An eleven-fold difference.**
>
> > [!important] Why the gap is so large
> > **The original question involves $\binom n2\approx n^2/2$ pairs. This one involves only $n-1$ — the pairs that include *you*.** One count is quadratic, the other linear.
> >
> > **This is the most important distinction in the whole problem, and the most commonly muddled.** *"Some two people match"* and *"someone matches me"* are entirely different questions.
> >
> > **The practical version:** *"is there a duplicate anywhere in this database?"* is far more likely than *"is there a duplicate of this particular record?"* — **which is exactly why hash collisions (the birthday attack) are so much easier to find than preimages.**
> >
> > *(A pleasing coincidence: $\binom{23}{2}=253$, and 253 is almost exactly the group size needed for the "shares mine" version to reach $\tfrac12$. The pair count for the first problem equals the person count for the second.)*
>
> ---
> **(v)** **$\{E_n\}$ is decreasing:** $E_{n+1}\subset E_n$, since ball 1 surviving $n+1$ withdrawals requires having survived $n$. So
> $$\lim_{n\to\infty}E_n=\bigcap_{n=1}^{\infty}E_n=\{\text{ball 1 present at 12 P.M.}\}$$
> and **the decreasing case of Proposition 6.1** gives
> $$P\left(\bigcap_nE_n\right)=\lim_nP(E_n)=\prod_{n=1}^{\infty}\frac{9n}{9n+1}=0$$
>
> **Why finite additivity is not enough.** Proposition 6.1's proof disjointifies into $F_1,F_2,\dots$ and applies **Axiom 3 to an infinite sequence**:
> $$P\left(\bigcup_1^{\infty}F_i\right)=\sum_1^{\infty}P(F_i)$$
> **Finite additivity (3.1) only ever tells you about $\bigcup_1^nF_i$ for finite $n$** — it says nothing about the infinite union, so **it cannot connect $\lim_nP(E_n)$ to $P(\lim_nE_n)$.**
>
> > **And that connection is the entire content of the example.** After every finite step, $P(E_n)>0$ — ball 1 might still be there. **Only the limit gives 0.** *"The limit of the probabilities" and "the probability of the limit" coincide here because Axiom 3 was stated countably.*

---

## 📝 Summary

- **A sample space $S$ is the set of all possible outcomes; an event is any subset of $S$.** Events combine by union ($E$ or $F$), intersection ($EF$: both), and complement ($E^c$: not $E$). **$E$ and $F$ are mutually exclusive when $EF=\emptyset$.**
- **Set operations obey commutative, associative and distributive laws** — but note that events distribute **both** ways, unlike arithmetic. **De Morgan's laws** $\left(\bigcup E_i\right)^c=\bigcap E_i^c$ and $\left(\bigcap E_i\right)^c=\bigcup E_i^c$ are the formal engine behind "count the complement."
- **The relative-frequency definition is rejected as a foundation** because assuming $n(E)/n$ converges is *"an extraordinarily complicated assumption."* **The long-run frequency claim is proved later as the strong law of large numbers** ([[08 - Limit Theorems|ch. 08]]).
- **The three axioms:** $0\le P(E)\le1$; $P(S)=1$; and **countable additivity** for mutually exclusive events. **$P(\emptyset)=0$ and finite additivity are consequences, not assumptions.** The infinite form of Axiom 3 is what makes §6 possible.
- **Four propositions:** $P(E^c)=1-P(E)$; $E\subset F\Rightarrow P(E)\le P(F)$; $P(E\cup F)=P(E)+P(F)-P(EF)$; and **inclusion–exclusion**, $P(\bigcup_i E_i)=\sum_r(-1)^{r+1}\sum_{i_1<\cdots<i_r}P(E_{i_1}\cdots E_{i_r})$ — whose alternating signs come directly from $(1-1)^m=0$, i.e. the binomial theorem.
- **Truncating inclusion–exclusion gives the Bonferroni inequalities**, alternating upper and lower bounds. **The first, Boole's inequality $P(\bigcup E_i)\le\sum P(E_i)$, needs no assumptions whatsoever** and is the chapter's most reusable tool.
- **When outcomes are equally likely, $P(E)=|E|/|S|$** — this is where [[01 - Combinatorial Analysis|ch. 01]] pays off. **Ordered and unordered sample spaces both work, because the correspondence between them is uniformly $k$-to-1** — but the numerator and denominator must use the **same** representation.
- **Classic results:** birthday problem (**23 people for a >50% chance**, because $\binom{23}{2}=253$ pairs); matching problem (**$P(\text{no match})\to e^{-1}\approx.368$, essentially independent of $N$**); the card after the first ace (**every card equally likely, $\tfrac1{52}$** — two opposing intuitions exactly cancel).
- **Probability is a continuous set function (Proposition 6.1):** for increasing or decreasing sequences, $\lim_nP(E_n)=P(\lim_nE_n)$. **This requires countable additivity and underpins every limit theorem later.** Example 6a shows the limit depends on *how* balls are withdrawn, even though the count after each finite step does not.
- **The subjective interpretation** treats $P(E)$ as degree of belief, and **should satisfy the same axioms** — so every theorem applies under both readings. **Real people violate them routinely; the axioms describe how beliefs should behave.**

---

## ⚠️ Important Notes

> [!warning] Mutually exclusive is not the same as independent — and they are close to opposites
> **Mutually exclusive:** $EF=\emptyset$, so $P(EF)=0$. **Independent** (defined in [[03 - Conditional Probability and Independence|ch. 03]]): $P(EF)=P(E)P(F)$.
>
> **If $E$ and $F$ are mutually exclusive with $P(E),P(F)>0$, they are *maximally dependent*** — knowing $E$ occurred tells you $F$ certainly did not. **They cannot be independent** unless one has probability zero.
>
> **This confusion is responsible for more wrong answers than any other single error in probability.** It is listed here rather than in ch. 03 because the vocabulary starts here.

> [!warning] Choose one sample space and stay in it
> **Ordered and unordered representations both give correct answers** — Example 5b computes $\tfrac4{11}$ both ways. **What is never correct is mixing them.**
>
> **The check: the numerator and denominator must count objects of the same kind.** $\binom61\binom52$ over $\binom{11}{3}$ ✓; $6\cdot5\cdot4$ over $11\cdot10\cdot9$ ✓; **$\binom61\binom52$ over $11\cdot10\cdot9$ ✗.**
>
> **And beware the numbers coinciding by accident** (Exercise 3(iv)) — **a right answer from wrong reasoning fails silently on the next problem.**

> [!warning] "At least one" almost always means "compute the complement"
> $$P(\text{at least one})=1-P(\text{none})$$
> **Every hard example in this chapter uses it:** J's books (Example 4a), the birthday problem, the matching problem, the round table. **In each case the direct computation is far worse.**
>
> **De Morgan is what licenses the move:** $\left(\bigcup E_i\right)^c=\bigcap E_i^c$, i.e. *"none of them" = "all of the nots."* **The complement of a union is an intersection, and intersections are usually easier.**

> [!warning] Inclusion–exclusion collapses only when the terms are symmetric
> The matching problem is clean because **every $r$-fold intersection has the same probability**, so each layer telescopes to $1/r!$. **The round table (Example 5n) is the same story** — $2^n(19-n)!/19!$ regardless of *which* couples.
>
> **When the intersections differ, inclusion–exclusion becomes $2^n-1$ separate terms and is useless in practice.** That is when you reach for **Bonferroni bounds** instead: two or three terms give a usable bracket without the full sum.

> [!warning] Check that a stated set of probabilities is even possible
> Exercise 2(iv): $P(A)=.5$, $P(B)=.4$, $P(AB)=.45$ is **impossible** — Proposition 4.2 forces $P(AB)\le\min\{P(A),P(B)\}$.
>
> **The systematic check is to decompose into the $2^n$ disjoint regions and confirm every one is $\ge0$.** Individual numbers can look plausible while implying a negative region — **which Axiom 1 forbids and which no single pairwise check would catch.**
>
> **This matters in practice** whenever probabilities are elicited from experts or estimated separately from different data sources: **the pieces must be checked for joint coherence, not just individual plausibility.**

> [!warning] The birthday problem's two versions are not the same question
> | Question | Pairs involved | $n$ for $P>\tfrac12$ |
> |---|---|---|
> | **Do *some two* people share a birthday?** | $\binom n2\approx n^2/2$ | **23** |
> | **Does someone share *my* birthday?** | $n-1$ | **254** |
>
> **Quadratic versus linear — an eleven-fold difference in the answer.**
>
> **The applied form matters constantly:** *"is there a duplicate anywhere?"* is vastly more likely than *"is there a duplicate of this specific record?"* — the basis of the **birthday attack** in cryptography, of hash-collision analysis, and of why running 500 hypothesis tests produces "significant" results by accident.

> [!warning] Infinity breaks intuition, and Proposition 6.1 is the guardrail
> In Example 6a, **the number of balls after every finite step is identical in all three scenarios** ($9n$). **The limits are: infinite, empty, and empty-with-probability-1.**
>
> > *"The reason the results are different is not because there is an actual paradox... but because one's initial intuition when dealing with infinity is not always correct."*
>
> **"The limit of the counts" and "the count of the limit" are different questions.** Proposition 6.1 tells you exactly when the corresponding probability statements agree — **and it needs countable additivity to do so.** Finite additivity would leave the question open.

> [!warning] Both interpretations of probability obey the same axioms — that is the payoff of being axiomatic
> **Frequentist:** $P(E)$ is a long-run frequency. **Subjective:** $P(E)$ is a degree of belief.
>
> **Everything proved in this book holds under both**, because both satisfy Axioms 1–3. *"Whether we interpret probability as a measure of belief or as a long-run frequency of occurrence, its mathematical properties remain unchanged."*
>
> **This is why the axiomatic detour at the start of the chapter was worth taking** — and why the frequentist/Bayesian debate in [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] is about *interpretation and method*, never about the probability calculus itself.

> [!note] Cross-subject connections
> - [[01 - Combinatorial Analysis|Ch. 01]] — **§5 is ch. 01 applied.** Every counting technique becomes a probability, and Proposition 4.4's proof runs directly on the binomial theorem.
> - [[03 - Conditional Probability and Independence|Ch. 03]] — takes $P(E\mid F)$ as the next primitive and shows it satisfies these same axioms (§3.5).
> - [[08 - Limit Theorems|Ch. 08]] — **proves the relative-frequency claim this chapter deliberately declined to assume.** Boole's inequality and Proposition 6.1 are used throughout.
> - [[Discrete Mathematics/contents/00-Index|Discrete Mathematics]] — set algebra, De Morgan and inclusion–exclusion for finite sets are the same theorems without the measure.
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — **Bonferroni bounds are the basis of multiple-comparison corrections**; the subjective interpretation is the foundation of Bayesian inference.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **Boole's inequality (the "union bound") is the workhorse of generalisation bounds**, converting a per-hypothesis guarantee into one holding over an entire hypothesis class.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **All Venn diagrams are images and cannot be extracted:**
> - **Figure 2.1** (three panels: $E\cup F$, $EF$, $E^c$ shaded) — only stray labels `EF EF`, `SS`, `(a) Shaded region: E < F.` survive. **The `<` is a mangled `∪`.** Reconstructed from the prose in §1a.
> - **Figure 2.2** ($E\subset F$) and **Figure 2.3** (the distributive law $(E\cup F)G=EG\cup FG$ in three panels) — same problem; the captions survive, the drawings do not.
> - **Figures 2.4 and 2.5** (the union split into regions I, II, III) — **the text describes these fully in words**, which is why the Proposition 4.3 argument in §3c is reproducible; the labels extract as `I III II`.
>
> **Notation mangled by the PDF layout** (all reconstructed by hand and cross-checked against worked examples):
> - **`q` is the extraction of `∞`** throughout — `limn→q`, `q⋃ n=1`, `S ={ x:0 … x < q}`. **Every infinity symbol in this chapter had to be restored from context.**
> - **`(` and `)` are mangled `⊂` and `⊃`** — `E ( F` means $E\subset F$, and `F ) E` means $F\supset E$. **These sit inside sentences full of genuine parentheses**, so each occurrence was disambiguated from the surrounding words.
> - **`…` is `≤`, `Ú` is `≥`, `Z` is `≠`, `L` is `≈`** — e.g. `0 … P(E) … 1` is Axiom 1, `EiEj = Ø when i Z j` is the mutual-exclusivity condition, and `L .0039` is $\approx.0039$. **Every inequality direction has been verified from context.**
> - **Binomial and multinomial coefficients extract across four lines**, as in [[01 - Combinatorial Analysis|ch. 01]]; fractions extract as numerator-newline-denominator.
> - **Superscripts detach:** `4 5 − 4` is $4^5-4$, `2 n` is $2^n$, `Ec i` is $E_i^c$, `(52)!` survives but `P0 L 1.3403 * 10−6` needs the exponent restored.
> - **In Example 5o, the substituted variables collide with the originals** — the text writes `y1 = y1 + 1, yi = yi, yr+1 = yr+1 + 1`, where the left-hand sides should carry a distinguishing mark (Ross uses a bar or prime that does not survive extraction). **Reproduced in §4e using distinct names to keep the argument readable.**
>
> **Verification performed:** every numeric claim in Examples 4a–7a was independently recomputed — $.6$ and $.4$; $\tfrac4{11}$ (both representations); $\tfrac{168}{323}$ (both representations, confirmed **equal**, which Ross leaves to the reader); $\tfrac{240}{1001}$; $k/n$; $.0039$; $.0014$; $6.3\times10^{-12}$; $.1055$; the birthday table and the $3{,}254{,}689{:}1$ odds at $n=100$ (Ross says "better than 3,000,000:1" ✓); $1.3403\times10^{-6}$, $.345861$, $7.6068\times10^{-6}$; $43$ members; the matching series and $e^{-1}$; $.6605$ and $.3395$; and both $\tfrac1{429}$ run probabilities. **All agree with the text. No arithmetic errors were found in this chapter.**
>
> **One exposition gap worth noting:** Ross asserts that the ordered and unordered answers for the married-couples problem *"are identical"* and **leaves the verification to the reader without giving the common value.** Both equal $\tfrac{168}{323}\approx0.5201$ — computed and confirmed here, since a reader checking their own work has nothing in the text to compare against.

#probability #axioms #sample-space #inclusion-exclusion #set-theory
