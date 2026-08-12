---
subject: Probability Theory
chapter: 03
tags: [ds, probability, conditional-probability, bayes, independence, odds]
source: "Ross, *A First Course in Probability*, 10th ed., ch. 3 (pp. 70–130)"
---

# Conditional Probability and Independence

> [!abstract] What this chapter is for
> **Ross calls conditional probability *"one of the most important concepts in probability theory,"* and gives its importance as twofold:**
>
> 1. **We often want probabilities when partial information is available** — the obvious use.
> 2. **Even when no partial information exists, conditioning lets us compute probabilities more easily** — *the use that actually matters.*
>
> **Point 2 is the one to internalise.** Conditioning is not primarily an interpretation; **it is a computational strategy.** Split a hard problem into cases, solve each easy case, and reassemble. The same move reappears for expectations in [[07 - Properties of Expectation|ch. 07]].
>
> | § | Topic | Key formula |
> |---|---|---|
> | **2** | **Conditional probability**, the multiplication rule | $P(E\mid F)=\dfrac{P(EF)}{P(F)}$ |
> | **3** | **Law of total probability**, **Bayes's formula**, **odds** | $P(E)=\sum_iP(E\mid F_i)P(F_i)$ |
> | **4** | **Independence**, independent trials | $P(EF)=P(E)P(F)$ |
> | **5** | $P(\cdot\mid F)$ **is a probability** | All of [[02 - Axioms of Probability|ch. 02]] applies to it |

---

## 📘 Main Knowledge

### 1. Conditional probability

**Roll two dice; all 36 outcomes equally likely. Given that the first die is a 3, what is $P(\text{sum}=8)$?**

**Once we know the first die is 3, only six outcomes remain possible:** $(3,1),\dots,(3,6)$. They were equally likely before, so **they remain equally likely** — each now has conditional probability $\tfrac16$, and the other 30 outcomes have conditional probability 0. **Exactly one of the six gives a sum of 8**, so the answer is $\tfrac16$.

> [!important] Definition
> If $P(F)>0$,
> $$\boxed{P(E\mid F)=\frac{P(EF)}{P(F)}} \tag{2.1}$$

**The reasoning behind the formula:** if $F$ has occurred, then for $E$ to occur the outcome must lie in **both** — that is, in $EF$. **$F$ becomes the new, reduced sample space**, so we measure $EF$ *relative to* $F$.

> [!note] Consistency with the frequency interpretation
> In $n$ repetitions, $F$ occurs about $nP(F)$ times and $EF$ about $nP(EF)$ times. **Among the trials where $F$ occurred, the proportion in which $E$ also occurred is**
> $$\frac{nP(EF)}{nP(F)}=\frac{P(EF)}{P(F)}$$
> **The definition is not arbitrary — it is what the frequency reading forces.**

> [!example] Example 2a — Joe's key
> Joe is 80% certain his key is in his jacket: 40% left pocket, 40% right. **A search of the left pocket fails. What is $P(\text{right})$ now?**
> $$P(R\mid L^c)=\frac{P(RL^c)}{P(L^c)}=\frac{P(R)}{1-P(L)}=\frac{.4}{.6}=\mathbf{\tfrac23}$$
> **Note $RL^c=R$**, since the key cannot be in both pockets. **Failing to find it in the left pocket raises the right-pocket probability from .4 to .667** — the remaining probability is redistributed over a smaller space.

#### 1a. The reduced sample space is often the fastest route

> [!important] When outcomes are equally likely, condition by shrinking the sample space
> *"If each outcome of a finite sample space $S$ is equally likely, then, conditional on the event that the outcome lies in a subset $F\subset S$, all outcomes in $F$ become equally likely."*
>
> **So just recount inside $F$.** *"Working with this reduced sample space often results in an easier and better understood solution."*

> [!example] Example 2b — the classic trap
> Two coin flips, $S=\{(h,h),(h,t),(t,h),(t,t)\}$. **$P(\text{both heads}\mid\ ?)$:**
>
> | Given | Reduced space | Answer |
> |---|---|---|
> | **the first flip is heads** | $\{(h,h),(h,t)\}$ | $\mathbf{\tfrac12}$ |
> | **at least one flip is heads** | $\{(h,h),(h,t),(t,h)\}$ | $\mathbf{\tfrac13}$ |
>
> > [!warning] Why $\tfrac13$ surprises people
> > *"They reason that given that at least one flip lands on heads, there are two possible results: either they both land on heads or only one does. **Their mistake, however, is in assuming that these two possibilities are equally likely.**"*
> >
> > **The information "at least one head" is exactly the information "the outcome is not $(t,t)$."** That leaves **three** equally likely outcomes, not two — and only one of them is $(h,h)$.
> >
> > **The general lesson: conditioning eliminates outcomes; it does not re-weight the survivors into whatever groups feel natural.** The surviving outcomes keep their original relative weights.

> [!example] Example 2c — bridge, via the reduced space
> North and South hold 8 spades between their 26 cards. **$P(\text{East holds 3 of the remaining 5 spades})$?**
>
> **Given the condition, 26 cards remain (exactly 5 spades) to be split between East and West.** Working entirely in that reduced space:
> $$\frac{\binom53\binom{21}{10}}{\binom{26}{13}}\approx\mathbf{.339}$$
> **No unconditional computation is needed at all** — the condition simply defines a smaller problem.

#### 1b. The multiplication rule

Multiplying (2.1) through by $P(F)$:

$$P(EF)=P(F)P(E\mid F) \tag{2.2}$$

> [!important] The multiplication rule
> $$\boxed{P(E_1E_2\cdots E_n)=P(E_1)P(E_2\mid E_1)P(E_3\mid E_1E_2)\cdots P(E_n\mid E_1\cdots E_{n-1})}$$

**Proof: the right-hand side telescopes.**

$$P(E_1)\cdot\frac{P(E_1E_2)}{P(E_1)}\cdot\frac{P(E_1E_2E_3)}{P(E_1E_2)}\cdots\frac{P(E_1\cdots E_n)}{P(E_1\cdots E_{n-1})}=P(E_1\cdots E_n)\quad\blacksquare$$

> [!tip] What the rule is *for*
> **It lets you build a joint probability one stage at a time, choosing an order that makes each conditional probability easy.** The examples below are all of this shape — and the art lies entirely in **choosing the right sequence of events.**

| Example | Setup | Answer |
|---|---|---|
| **2d** | Celine flips a coin to choose French or chemistry; $P(A)=\tfrac12$ French, $\tfrac23$ chemistry. $P(\text{A in chemistry})$? | $P(C)P(A\mid C)=\tfrac12\cdot\tfrac23=\mathbf{\tfrac13}$ |
| **2e(a)** | 8 red, 4 white; draw 2 without replacement. $P(\text{both red})$? | $\tfrac8{12}\cdot\tfrac7{11}=\mathbf{\tfrac{14}{33}}$ *(= $\binom82/\binom{12}2$ ✓)* |
| **2e(b)** | Same, but balls have weights $r$ and $w$, selected proportionally | $\dfrac{8r}{8r+4w}\cdot\dfrac{7r}{7r+4w}$ |

> [!example] Example 2g — one ace in each of 4 piles
> A deck is split into 4 piles of 13. **$P(\text{each pile has exactly one ace})$?**
>
> **The clever part is the choice of events** — bring in the aces one at a time:
>
> | Event | Meaning | Probability |
> |---|---|---|
> | $E_1$ | ace of spades is in some pile | $1$ *(it always is)* |
> | $E_2$ | $\spadesuit$A and $\heartsuit$A in different piles | $1-\tfrac{12}{51}=\tfrac{39}{51}$ |
> | $E_3$ | $\spadesuit$A, $\heartsuit$A, $\diamondsuit$A all different | $1-\tfrac{24}{50}=\tfrac{26}{50}$ |
> | $E_4$ | all four aces different | $1-\tfrac{36}{49}=\tfrac{13}{49}$ |
>
> **Each step asks: given where the previous aces landed, what is the chance the next one avoids their piles?** The pile holding $\spadesuit$A has 12 other cards drawn from 51, so $\heartsuit$A joins it with probability $\tfrac{12}{51}$.
> $$P=\frac{39\cdot26\cdot13}{51\cdot50\cdot49}\approx\mathbf{.105}$$
> **Matching Example 5h(b) of [[02 - Axioms of Probability|ch. 02]], which got $.1055$ by multinomial coefficients** — two completely different routes, same answer. ✓

> [!example] Example 2h — the Champions League pairings
> 8 quarter-finalists, 4 of them strong (Barcelona, Bayern, Real Madrid, PSG). **If pairings are uniformly random, $P(\text{no two strong teams meet})$?**
>
> Let $W_i$ = "strong team $i$ draws a weak team." **Condition down the list:**
> $$P(W_1W_2W_3W_4)=\underbrace{\tfrac47}_{\text{4 weak of 7}}\cdot\underbrace{\tfrac35}_{\text{3 weak of 5 left}}\cdot\underbrace{\tfrac23}_{\text{2 weak of 3 left}}\cdot\underbrace{1}_{\text{forced}}=\mathbf{\tfrac8{35}}\approx.229$$
>
> > **Ross's aside is the interesting part:** *"Surprisingly, it seems to be a common occurrence in this tournament that, even though the pairings are supposedly random, the very strong teams are rarely matched against each other in this round."*
> >
> > **Only 23% of random draws avoid all strong-vs-strong matches.** Observing that outcome repeatedly is evidence the draw is not what it claims to be — **the same reasoning as the runs test in [[02 - Axioms of Probability|ch. 02 §4e]].**

> [!example] Example 2f — exactly $k$ matches in the hat problem
> Extending [[02 - Axioms of Probability|ch. 02]]'s Example 5m. **Fix a set of $k$ people.** By the multiplication rule, the probability *they* all match is
> $$P(F_1)P(F_2\mid F_1)\cdots=\frac1N\cdot\frac1{N-1}\cdots\frac1{N-k+1}=\frac{(N-k)!}{N!}$$
> **Given that, the other $N-k$ people face the same problem at size $N-k$**, so the probability none of them matches is $P_{N-k}$. There are $\binom Nk$ such sets, giving
> $$\boxed{P(\text{exactly }k\text{ matches})=\frac{P_{N-k}}{k!}\ \longrightarrow\ \frac{e^{-1}}{k!}}$$
>
> > **This is the Poisson distribution with $\lambda=1$**, arriving three chapters early ([[04 - Random Variables|ch. 04 §7]]). **The number of matches in a large random permutation is approximately Poisson(1)** — and the derivation is pure conditioning.

---

### 2. Bayes's formula

#### 2a. The law of total probability

Since $E=EF\cup EF^c$ (disjoint):

$$\boxed{P(E)=P(E\mid F)P(F)+P(E\mid F^c)[1-P(F)]} \tag{3.1}$$

and generally, for **mutually exclusive and exhaustive** $F_1,\dots,F_n$ (exactly one must occur):

$$\boxed{P(E)=\sum_{i=1}^{n}P(E\mid F_i)P(F_i)} \tag{3.4}$$

> [!important] What (3.4) says, and why it is the chapter's real engine
> **$P(E)$ is a weighted average of the conditional probabilities $P(E\mid F_i)$, each weighted by how likely its condition is.**
>
> > *"There are many instances in which it is difficult to compute the probability of an event directly, but it is straightforward to compute it once we know whether or not some second event has occurred."*
>
> **The strategy: find the piece of missing information that would make the problem easy, then average over its possible values.**

| Example | Condition on… | Result |
|---|---|---|
| **3a(1)** | whether the policyholder is accident prone (30% are; $.4$ vs $.2$ accident rates) | $P(A_1)=(.4)(.3)+(.2)(.7)=\mathbf{.26}$ |
| **3n(a)** | flashlight type (20/30/50% at $.7/.4/.3$) | $P(A)=(.7)(.2)+(.4)(.3)+(.3)(.5)=\mathbf{.41}$ |
| **3h** | whether a twin pair is identical | $P(SS)=\tfrac12+\tfrac12P(I)$ |

> [!example] Example 3h — measuring what you cannot observe
> **A statistician wants the fraction of twin births that are identical, but DNA testing is too expensive.** She asks only whether each pair is **same-sex** — cheap and always recorded.
>
> **Identical twins are always same-sex; fraternal twins are same-sex with probability $\tfrac12$.** So
> $$P(SS)=1\cdot P(I)+\tfrac12\cdot[1-P(I)]=\tfrac12+\tfrac12P(I)$$
> **Observed $P(SS)\approx.64$, hence $P(I)\approx\mathbf{.28}$.**
>
> > **This is the whole of applied statistics in one example.** The quantity of interest is unobservable; a cheap observable is related to it by a known conditional structure; **invert the relation.** *(The same logic underlies capture–recapture, randomised response, and every latent-variable model.)*

> [!example] Example 3b — a strategy-proof game
> A shuffled deck is turned over one card at a time. **At any point you may guess that the next card is the ace of spades; you win if right. You also win if the ace never appeared and one card remains with no guess made.** What is a good strategy?
>
> **Every strategy wins with probability $\tfrac1{52}$.**
>
> **By induction.** True for $n=1$. For an $n$-card deck, let $p$ be the probability the strategy guesses on the first card.
> - **If it guesses:** win probability $\tfrac1n$.
> - **If it does not:** win only if the first card is not the ace ($\tfrac{n-1}{n}$) and then the reduced game is exactly an $(n-1)$-card game, won with probability $\tfrac1{n-1}$ by hypothesis. Product: $\tfrac{n-1}{n}\cdot\tfrac1{n-1}=\tfrac1n$.
>
> **Both branches give $\tfrac1n$**, so conditioning on whether the strategy guesses:
> $$P(\text{win})=\tfrac1n\cdot p+\tfrac1n(1-p)=\tfrac1n\quad\blacksquare$$
>
> > **Note the structure: conditioning revealed that the two branches were equal, so the weights became irrelevant.** *"What is a bad strategy?" has no answer — there are none.*

#### 2b. Bayes's formula

> [!important] Proposition 3.1 — Bayes's formula
> For mutually exclusive and exhaustive $F_1,\dots,F_n$,
> $$\boxed{P(F_j\mid E)=\frac{P(E\mid F_j)P(F_j)}{\sum_{i=1}^{n}P(E\mid F_i)P(F_i)}} \tag{3.5}$$
>
> **If the $F_j$ are competing hypotheses, Bayes shows how the prior opinions $P(F_j)$ should be revised in the light of evidence $E$.**

> [!tip] The three-part anatomy
> $$\underbrace{P(F_j\mid E)}_{\textbf{posterior}}\;\propto\;\underbrace{P(E\mid F_j)}_{\textbf{likelihood}}\times\underbrace{P(F_j)}_{\textbf{prior}}$$
> **The denominator is just the normalising constant** — it is $P(E)$ by the law of total probability, and its only job is to make the posteriors sum to 1.
>
> **Almost every Bayes error is a failure to notice that the prior is part of the formula.**

##### The base rate fallacy

> [!example] Example 3d — the blood test
> A test is **95% effective** at detecting a disease that is present, and has a **1% false positive rate**. **0.5% of the population has the disease. Given a positive test, what is $P(\text{disease})$?**
>
> $$P(D\mid E)=\frac{(.95)(.005)}{(.95)(.005)+(.01)(.995)}=\frac{95}{294}\approx\mathbf{.323}$$
>
> **Only 32% of people who test positive actually have the disease.**
>
> > [!important] Ross's second argument — the one that actually convinces
> > *"Many students are often surprised at this result (they expect the percentage to be much higher, since the blood test seems to be a good one), so it is probably worthwhile to present a second argument."*
> >
> > **Think in counts, not probabilities. Out of every 200 people tested:**
> > - **1 has the disease**, and the test catches them with probability $.95$ → **0.95 true positives**
> > - **199 are healthy**, and $1\%$ of them test positive → $199\times.01=$ **1.99 false positives**
> >
> > $$\frac{.95}{.95+1.99}=\frac{95}{294}\approx.323\ ✓$$
> >
> > **The false positives outnumber the true positives two to one — because there are 199 times more healthy people to draw them from.** *A 1% error rate on a huge group beats a 95% success rate on a tiny one.*
> >
> > **Reframing Bayes as "natural frequencies" makes the answer obvious. Use it whenever a base rate is small.**

##### Updating a belief

> [!example] Example 3e — the doctor's dilemma
> The doctor operates if $\ge80\%$ certain. Prior: $60\%$. The **A test** is positive; it *never* gives a false positive in healthy patients — **but Jones is diabetic, and the test is positive $30\%$ of the time in diabetics without the disease.**
> $$P(D\mid E)=\frac{(.6)(1)}{(1)(.6)+(.3)(.4)}=\frac{.6}{.72}=\mathbf{.833}$$
> **Above 80%, so operate.**
>
> **The instructive point:** the diabetes news *"doesn't change my original 60 percent estimate of his chances of having the disease... **it does affect the interpretation of the results of the A test.**"* **New information can change the likelihood without touching the prior.**

> [!example] Example 3f — the inspector
> Prior guilt $.6$; the criminal has a characteristic possessed by $20\%$ of the population; the suspect has it.
> $$P(G\mid C)=\frac{1(.6)}{1(.6)+(.2)(.4)}\approx\mathbf{.882}$$
> *(Assuming an innocent suspect has the characteristic with the population rate $.2$.)*

> [!example] Example 3c — the multiple-choice student
> $P(\text{knows})=p$; a guesser is right with probability $1/m$.
> $$P(K\mid C)=\frac{p}{p+(1/m)(1-p)}=\boxed{\frac{mp}{1+(m-1)p}}$$
> **With $m=5$, $p=\tfrac12$: the answer is $\tfrac56$.** *(More alternatives make guessing less plausible, so a correct answer is stronger evidence of knowledge.)*

##### When evidence is not evidence

> [!example] Example 3g — the bridge cheating scandal
> At the 1965 world championships, Reese and Schapiro were accused of signalling. **The prosecution argued that because their play was *consistent with* guilt, it counted as evidence of guilt.** The defence noted it was equally consistent with their normal style. **Who is right?**
>
> From Bayes, $P(H\mid E)\ge P(H)$ if and only if
> $$\boxed{P(E\mid H)\ge P(E\mid H^c)}$$
>
> > **New evidence supports a hypothesis only if it is *more likely* when the hypothesis is true than when it is false.**
>
> **The prosecutor never claimed that** — only that the play was *compatible* with cheating. **So the assertion is invalid.**
>
> **And the magnitude is governed entirely by the likelihood ratio:**
> $$P(H\mid E)=\frac{P(H)}{P(H)+[1-P(H)]\dfrac{P(E\mid H^c)}{P(E\mid H)}}$$
>
> > **This is the most transferable idea in the chapter.** *"Consistent with"* is worthless. **Evidence has force only in proportion to how much *better* it is explained by one hypothesis than another.**

#### 2c. Odds and the likelihood ratio

> [!important] Definition — odds
> $$\text{odds}(A)=\frac{P(A)}{P(A^c)}=\frac{P(A)}{1-P(A)}$$
> *If $P(A)=\tfrac23$ then the odds are 2, said as "2 to 1."*

> [!important] The odds form of Bayes — the cleanest statement in the chapter
> $$\boxed{\underbrace{\frac{P(H\mid E)}{P(H^c\mid E)}}_{\text{posterior odds}}=\underbrace{\frac{P(H)}{P(H^c)}}_{\text{prior odds}}\times\underbrace{\frac{P(E\mid H)}{P(E\mid H^c)}}_{\textbf{likelihood ratio}}} \tag{3.3}$$

> [!tip] Why this form is worth memorising over (3.5)
> - **The awkward denominator vanishes.** No normalising constant to compute.
> - **It is multiplicative**, so **independent pieces of evidence just multiply their likelihood ratios** — updating is incremental.
> - **It makes Example 3g immediate:** the odds increase iff $\text{LR}>1$, decrease iff $\text{LR}<1$, and are unchanged iff $\text{LR}=1$.
>
> **In practice: "prior odds × likelihood ratio = posterior odds" is the single most useful sentence in applied Bayesian reasoning.**

> [!example] Example 3i — two type-A coins and one type-B
> Type A lands heads w.p. $\tfrac14$; type B w.p. $\tfrac34$. A random coin lands heads. **$P(\text{type A})$?**
> $$\frac{P(A\mid H)}{P(A^c\mid H)}=\underbrace{\frac{2/3}{1/3}}_{=2}\times\underbrace{\frac{1/4}{3/4}}_{=1/3}=\mathbf{\tfrac23}$$
> **Odds of $\tfrac23$ to 1 means probability $\dfrac{2/3}{1+2/3}=\mathbf{\tfrac25}$.**
>
> **Read the two factors:** type A was twice as likely a priori (2 coins of 3), but heads is three times less likely from it — **net effect $2\times\tfrac13=\tfrac23$, so the prior majority is overturned.**

#### 2d. Three more applications

> [!example] Example 3k — the missing plane
> Equally likely to be in region 1, 2 or 3. **Overlook probability $\beta_i$** = chance of missing it in a search of region $i$ when it *is* there. **A search of region 1 fails.**
> $$P(R_1\mid E)=\frac{\beta_1\cdot\tfrac13}{\beta_1\cdot\tfrac13+\tfrac13+\tfrac13}=\boxed{\frac{\beta_1}{\beta_1+2}} \qquad P(R_j\mid E)=\frac{1}{\beta_1+2},\ j=2,3$$
>
> **Both monotonicities are intuitive and worth stating:**
> - **$P(R_1\mid E)$ falls below $\tfrac13$, and $P(R_j\mid E)$ rises** — failing to find it in region 1 shifts belief elsewhere ✓
> - **$P(R_1\mid E)$ is *increasing* in $\beta_1$** — *"the larger $\beta_1$ is, the more it is reasonable to attribute the unsuccessful search to 'bad luck' as opposed to the plane's not being there."*
>
> **A negative result is only strong evidence if the search was good.** *(This is exactly why test sensitivity matters for interpreting negatives.)*

> [!example] Example 3l — the three-card problem
> Three cards: **red/red**, **black/black**, **red/black**. One is drawn and laid down; **the visible side is red.** $P(\text{other side is black})$?
> $$P(RB\mid R)=\frac{(\tfrac12)(\tfrac13)}{(1)(\tfrac13)+(\tfrac12)(\tfrac13)+0}=\mathbf{\tfrac13}$$
>
> > [!warning] Why $\tfrac12$ is wrong
> > *"Some students guess $\tfrac12$ by incorrectly reasoning that given that a red side appears, there are two equally likely possibilities... **their mistake is in assuming that these two possibilities are equally likely.**"*
> >
> > **Count sides, not cards.** There are 6 equally likely faces: $R_1,R_2$ (all-red card), $R_3,B_3$ (mixed), $B_1,B_2$ (all-black). **Seeing red means the outcome is $R_1$, $R_2$ or $R_3$ — and only $R_3$ has black behind it.** Hence $\tfrac13$.
> >
> > **The all-red card is twice as likely to produce a red face**, and that is exactly what the likelihood $P(R\mid RR)=1$ versus $P(R\mid RB)=\tfrac12$ encodes. **Same structural error as Example 2b's $\tfrac13$-versus-$\tfrac12$.**
> >
> > *Ross's dry note: this example "has often been used by unscrupulous probability students to win money from their less enlightened friends."*

> [!example] Example 3m — the two-child problem, and why it has no answer
> A couple has two children. **You meet the mother walking with one of them — a girl. $P(\text{both girls})$?**
> $$P(G_1G_2\mid G)=\frac{1}{1+P(G\mid G_1B_2)+P(G\mid B_1G_2)}$$
> **and the answer depends entirely on assumptions you have not been given:**
>
> | Assumption | Answer |
> |---|---|
> | She walks with the **elder** child w.p. $p$, regardless of sex | $\mathbf{\tfrac12}$ |
> | If the children differ, she walks with the **girl** w.p. $q$ | $\dfrac{1}{1+2q}$ |
> | …with $q=1$ (always walks with a daughter) | $\mathbf{\tfrac13}$ |
>
> > [!important] *"Hence, as stated, the problem is incapable of solution."*
> > **The sample space is not $\{GG,GB,BG,BB\}$.** It is vectors $(s_1,s_2,i)$ — the two sexes **and which child you saw**. *"It is not enough to make assumptions only about the genders of the children; it is also necessary to assume something about the conditional probabilities as to which child is with the mother."*
> >
> > **This is the deepest methodological point in the chapter: how you *came to know* something is part of the data.** The $q=1$ case reduces to *"at least one girl"* and reproduces Example 2b's $\tfrac13$; the neutral case gives $\tfrac12$. **Same observation, different answers, because different observation *processes*.**
> >
> > **Any "paradox" of this family (Monty Hall, the boy-girl problem, the sleeping beauty problem) dissolves once the observation mechanism is specified.**

> [!note] Example 3o — DNA evidence *(worth the shape, not the algebra)*
> A crime; 5 DNA strands recovered; each innocent person matches with probability $10^{-5}$. Of 1,000,000 residents, 10,000 ex-convicts are on file. **A. J. Jones is the only database match.** With ex-convicts $c$ times more likely to be guilty a priori,
> $$P(G\mid M)=\frac{\alpha}{\alpha+10^{-5}(1-10{,}000\alpha)}=\frac{1}{.9+\dfrac{10^{-5}}{\alpha}}, \qquad \alpha=\frac{c}{10{,}000c+990{,}000}$$
> **With $c=100$: $\alpha=\tfrac1{19{,}900}$ and $P(G\mid M)\approx\mathbf{.910}$.**
>
> **The point is that the answer depends critically on $c$ — a subjective input.** *"The prosecutor's fallacy"* is to report $1-10^{-5}$ as the probability of guilt, confusing $P(\text{match}\mid\text{innocent})$ with $P(\text{innocent}\mid\text{match})$. **They differ by five orders of magnitude in the base rate.**

---

### 3. Independent events

> [!important] Definition
> $E$ and $F$ are **independent** if
> $$\boxed{P(EF)=P(E)P(F)} \tag{4.1}$$
> Otherwise they are **dependent**.

**Why this definition.** $E$ is independent of $F$ when $P(E\mid F)=P(E)$ — *knowing $F$ occurred does not change the chance of $E$.* Substituting $P(E\mid F)=P(EF)/P(F)$ gives (4.1).

> [!tip] The definition is stated as (4.1) for two good reasons
> 1. **It is symmetric** — so "E is independent of F" and "F is independent of E" are automatically the same statement.
> 2. **It does not require $P(F)>0$**, so it is well defined in cases where $P(E\mid F)$ is not.

| Example | Events | Independent? |
|---|---|---|
| **4a** | $E$ = ace, $F$ = spade (one card) | **Yes**: $P(EF)=\tfrac1{52}=\tfrac4{52}\cdot\tfrac{13}{52}$ |
| **4b** | first coin heads, second coin tails | **Yes**: $\tfrac14=\tfrac12\cdot\tfrac12$ |
| **4c** | $E_1$ = sum is 6, $F$ = first die is 4 | **No**: $\tfrac1{36}\ne\tfrac5{36}\cdot\tfrac16=\tfrac5{216}$ |
| **4c** | $E_2$ = sum is **7**, $F$ = first die is 4 | **Yes**: $\tfrac1{36}=\tfrac16\cdot\tfrac16$ |

> [!important] Why sum-7 is special
> **For the sum to be 6, the first die matters** — *"if the first die landed on 6, we would be unhappy because we would no longer have a chance of getting a total of 6."*
>
> **For the sum to be 7, whatever the first die shows, exactly one value of the second die works.** So the conditional probability is $\tfrac16$ regardless. **7 is the only sum with this property**, which is why it appears constantly in dice problems.

> [!important] Proposition 4.1
> **If $E$ and $F$ are independent, then so are $E$ and $F^c$.**
>
> **Proof.** $E=EF\cup EF^c$ (disjoint), so $P(E)=P(E)P(F)+P(EF^c)$, giving $P(EF^c)=P(E)[1-P(F)]=P(E)P(F^c)$. $\blacksquare$
>
> *"If $E$ is independent of $F$, then the probability of $E$'s occurrence is unchanged by information as to whether or not $F$ has occurred."* **Independence is about the whole information content of $F$, not just its occurrence.**

#### 3a. Pairwise is not enough

> [!warning] Example 4e — the counterexample that forces the definition
> Two dice. $E$ = sum is 7; $F$ = first die is 4; $G$ = second die is 3.
>
> **$E$ is independent of $F$** ✓ (Example 4c) **and $E$ is independent of $G$** ✓ (same reasoning).
>
> **But $E$ is emphatically not independent of $FG$:** if the dice are 4 and 3, the sum *is* 7, so $P(E\mid FG)=\mathbf{1}$.
>
> **Pairwise independence does not imply anything about triples.**

> [!important] Definition — three independent events
> $E$, $F$, $G$ are **independent** if **all four** conditions hold:
> $$P(EFG)=P(E)P(F)P(G)$$
> $$P(EF)=P(E)P(F), \qquad P(EG)=P(E)P(G), \qquad P(FG)=P(F)P(G)$$
>
> **In general, $E_1,\dots,E_n$ are independent if *every* subset factorises:**
> $$P(E_{1'}E_{2'}\cdots E_{r'})=P(E_{1'})P(E_{2'})\cdots P(E_{r'}) \quad\text{for every subset of size } r\le n$$
> **An infinite family is independent if every finite subfamily is.**

> [!tip] The payoff of the full definition
> **If $E$, $F$, $G$ are (mutually) independent, then $E$ is independent of *any* event built from $F$ and $G$.** For instance:
> $$P[E(F\cup G)]=P(EF)+P(EG)-P(EFG)=P(E)[P(F)+P(G)-P(FG)]=P(E)P(F\cup G)$$
> **That closure property is what you actually use, and pairwise independence does not deliver it.**

#### 3b. Independent trials

> [!important] Independent subexperiments and trials
> **Subexperiments are independent if $E_1,E_2,\dots$ is always an independent sequence whenever $E_i$ is determined solely by the $i$th subexperiment.**
>
> **If each subexperiment has the same set of possible outcomes, they are called *trials*.**

> [!example] Example 4f — the three standard questions
> Infinitely many independent trials, each a success with probability $p$.
>
> **(a) At least one success in the first $n$?** Complement first:
> $$1-(1-p)^n$$
>
> **(b) Exactly $k$ successes in the first $n$?** Each specific sequence with $k$ successes has probability $p^k(1-p)^{n-k}$, and there are $\binom nk$ such sequences:
> $$\boxed{P(k\text{ successes})=\binom nk p^k(1-p)^{n-k}}$$
> **This is the binomial distribution**, derived here from independence plus [[01 - Combinatorial Analysis|ch. 01]]'s counting. It is formalised in [[04 - Random Variables|ch. 04 §6]].
>
> **(c) All trials succeed?** Using the **continuity of $P$** from [[02 - Axioms of Probability|ch. 02 §6]]:
> $$P\left(\bigcap_{i=1}^{\infty}E_i^c\right)=\lim_{n\to\infty}p^n=\begin{cases}0 & p<1\\ 1 & p=1\end{cases}$$
> **Note this is exactly where ch. 02's Proposition 6.1 earns its keep** — the finite answer $p^n$ is never 0, only the limit is.

> [!example] Example 4g — parallel systems
> A **parallel system** works if **at least one** of $n$ independent components works, component $i$ with probability $p_i$:
> $$P(\text{works})=1-\prod_{i=1}^{n}(1-p_i)$$
> *(Complement, then independence.)* **Contrast a series system, which needs all of them: $\prod_ip_i$.** **Redundancy is why parallel architectures are reliable** — with three components at $p=.9$, parallel gives $.999$ and series gives $.729$.

> [!example] Example 4h — "5 before 7", two ways
> **Roll a pair of dice repeatedly. $P(\text{a 5 appears before a 7})$?**
>
> **Method 1 — sum the series.** $P(5)=\tfrac4{36}$, $P(7)=\tfrac6{36}$, so $P(\text{neither})=\tfrac{26}{36}$:
> $$\sum_{n=1}^{\infty}\left(\tfrac{13}{18}\right)^{n-1}\tfrac19=\frac{1/9}{1-13/18}=\mathbf{\tfrac25}$$
>
> **Method 2 — condition on the first roll**, which is far slicker. With $F$ = first roll is 5, $G$ = 7, $H$ = neither:
> $$P(E)=1\cdot\tfrac4{36}+0\cdot\tfrac6{36}+P(E)\cdot\tfrac{26}{36}$$
> **The key is $P(E\mid H)=P(E)$** — *"if the first outcome results in neither a 5 nor a 7, then at that point the situation is exactly as it was when the problem first started."* Solving: $P(E)=\tfrac25$.
>
> > [!important] The general result, and why it is obvious in hindsight
> > **For mutually exclusive $E$ and $F$ in repeated independent trials:**
> > $$\boxed{P(E\text{ before }F)=\frac{P(E)}{P(E)+P(F)}}$$
> > **Only the relative rates matter — everything else is irrelevant filler.** Here $\tfrac{4}{4+6}=\tfrac25$ ✓.
> >
> > **Method 2's self-referential conditioning ("the situation is as it was at the start") is a fundamental technique**, reused immediately in the gambler's ruin.

> [!example] Example 4j — the problem of the points
> **Independent trials; $P(\text{success})=p$. What is $P_{n,m}$, the probability of $n$ successes before $m$ failures?**
>
> *Posed to Pascal in 1654 by the Chevalier de Méré; the Pascal–Fermat correspondence that followed is considered by some the birth of probability theory.*
>
> **Pascal's route — condition on the first trial:**
> $$P_{n,m}=pP_{n-1,m}+(1-p)P_{n,m-1}, \qquad P_{n,0}=0,\ P_{0,m}=1$$
> *"Rather than go through the tedious details, let us instead consider Fermat's solution."*
>
> **Fermat's route — imagine playing on regardless.** *$n$ successes occur before $m$ failures **iff** there are at least $n$ successes in the first $m+n-1$ trials.* (If there are $\ge n$ successes there can be at most $m-1$ failures; if fewer, there must be $\ge m$ failures.)
> $$\boxed{P_{n,m}=\sum_{k=n}^{m+n-1}\binom{m+n-1}{k}p^k(1-p)^{m+n-1-k}}$$
>
> > **The trick — *"even if the game were to end before $m+n-1$ trials, we could still imagine the necessary additional trials were performed"* — converts a variable-length experiment into a fixed-length one.** **Padding out a random stopping time to a fixed horizon is a genuinely powerful move**, reused in Example 4k to prove that "winner serves" and "alternating serve" give identical match-win probabilities.

> [!example] Example 4m — the gambler's ruin
> $A$ starts with $i$ units, $B$ with $N-i$; each round $A$ wins 1 with probability $p$ (else loses 1). **$P(A\text{ ends with everything})$?**
>
> **Condition on the first flip** — and note the self-similarity: after a win, the situation is a fresh game starting at $i+1$.
> $$P_i=pP_{i+1}+qP_{i-1}, \qquad P_0=0,\ P_N=1$$
> Rewriting as $P_{i+1}-P_i=\tfrac qp(P_i-P_{i-1})$ and telescoping:
> $$\boxed{P_i=\begin{cases}\dfrac{1-(q/p)^i}{1-(q/p)^N} & p\ne\tfrac12\\[10pt] \dfrac iN & p=\tfrac12\end{cases}} \tag{4.5}$$
>
> **Numerical illustration.** $A$ starts with 5, $B$ with 10:
> $$p=\tfrac12:\ P=\tfrac5{15}=\mathbf{\tfrac13} \qquad\qquad p=.6:\ P=\frac{1-(2/3)^5}{1-(2/3)^{15}}\approx\mathbf{.87}$$
> **A 10% edge per round turns a 33% chance into 87%.** *Small per-trial advantages compound ferociously.*
>
> > **Ross also proves $P_i+Q_i=1$** — i.e. **the probability the game continues forever is exactly 0.** *"The reader must be careful because, a priori, there are three possible outcomes of this gambling game, not two."*
>
> **Historical note:** a special case (12 coins each, dice sums 11 vs 14, giving $p=\tfrac{15}{42}$, $i=12$, $N=24$) was posed to Huygens by Fermat in 1657; **the general problem was solved by James Bernoulli**, published 1713.

> [!note] Application — sequential clinical trials
> Two drugs with unknown cure rates $p_1>p_2$. Treat patients in pairs; stop when the cumulative cure difference first reaches $+M$ or $-M$. **This is exactly gambler's ruin with $i=M$, $N=2M$**, where (conditioning on pairs that produce a difference)
> $$p=\frac{p_1(1-p_2)}{p_1(1-p_2)+(1-p_1)p_2}$$
> **Probability of the wrong conclusion:**
> $$P(\text{error})=\frac{1}{1+\gamma^M}, \qquad \gamma=\frac{p_1(1-p_2)}{p_2(1-p_1)}$$
> **With $p_1=.6$, $p_2=.4$: error $=\mathbf{.017}$ at $M=5$, and $\mathbf{.0003}$ at $M=10$.**
>
> > **A recreational gambling problem turns out to govern the error rate of a real clinical trial design.** *(This is a sequential probability ratio test in disguise — see [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]].)*

---

### 4. $P(\cdot\mid F)$ is a probability

> [!important] Proposition 5.1
> For fixed $F$ with $P(F)>0$:
> **(a)** $0\le P(E\mid F)\le1$ **(b)** $P(S\mid F)=1$ **(c)** for mutually exclusive $E_i$, $\displaystyle P\left(\bigcup_iE_i\;\middle|\;F\right)=\sum_iP(E_i\mid F)$
>
> **These are exactly the three axioms of [[02 - Axioms of Probability|ch. 02]].**

**Proof sketches.** (a) $EF\subset F$ gives $P(EF)\le P(F)$. (b) $P(SF)/P(F)=P(F)/P(F)=1$. (c) $\left(\bigcup_iE_i\right)F=\bigcup_i E_iF$, and $E_iE_j=\emptyset$ implies $E_iFE_jF=\emptyset$, so Axiom 3 applies. $\blacksquare$

> [!important] The consequence, and it is a large one
> **Define $Q(E)=P(E\mid F)$. Then $Q$ is a probability function, so *every* result of ch. 02 and ch. 03 holds for it.** For example:
> $$P(E_1\cup E_2\mid F)=P(E_1\mid F)+P(E_2\mid F)-P(E_1E_2\mid F)$$
>
> **And defining $Q(E_1\mid E_2)=Q(E_1E_2)/Q(E_2)$, a short computation gives $Q(E_1\mid E_2)=P(E_1\mid E_2F)$**, so the law of total probability itself conditionalises:
> $$\boxed{P(E_1\mid F)=P(E_1\mid E_2F)P(E_2\mid F)+P(E_1\mid E_2^cF)P(E_2^c\mid F)} \tag{5.1}$$
>
> **You never need to re-derive anything in a conditional world. Everything carries over — you simply write $\mid F$ after every event.**

> [!example] Example 5a — a second accident
> From Example 3a: 30% accident-prone (rate $.4$), rest rate $.2$, and $P(A_1)=.26$. **Given an accident in year 1, what is $P(\text{accident in year 2})$?**
>
> First update the class probability:
> $$P(A\mid A_1)=\frac{(.4)(.3)}{.26}=\tfrac6{13}, \qquad P(A^c\mid A_1)=\tfrac7{13}$$
> Then condition **within** the world where $A_1$ occurred, using (5.1):
> $$P(A_2\mid A_1)=(.4)\tfrac6{13}+(.2)\tfrac7{13}\approx\mathbf{.29}$$
>
> > **Compare $P(A_1)=.26$: having one accident raises the chance of another from $.26$ to $.29$.**
> >
> > **The accidents are *not* independent — even though, conditional on the person's class, they are.** The first accident is evidence about which class the person belongs to, and that evidence carries forward. **This is conditional independence without unconditional independence**, and it is the single most important structural idea in Bayesian modelling.

> [!example] Example 5b — chimp paternity
> Mother is $(A,A)$; male 1 is $(a,a)$; male 2 is $(A,a)$. Prior $P(M_1)=p$. **The baby is $(A,a)$.**
>
> Male 1 **must** produce $(A,a)$ with the mother; male 2 does so with probability $\tfrac12$:
> $$P(M_1\mid B_{A,a})=\frac{1\cdot p}{1\cdot p+\tfrac12(1-p)}=\boxed{\frac{2p}{1+p}}$$
> **Since $\tfrac{2p}{1+p}>p$ for $p<1$, the evidence favours male 1** — because *"it is more likely that the baby would have gene pair $(A,a)$ if $M_1$ is true than if $M_2$ is true."* **Exactly the criterion of Example 3g: likelihood ratio $=2>1$.**

---

## ✏️ Exercises

> [!note] These exercises are my own construction
> Every figure is either quoted from the text or computed by hand, and **all arithmetic below has been independently verified.**

---

**Exercise 1 — Conditional probability and the reduced sample space**

Two fair dice are rolled.

**(i)** Find $P(\text{sum}=8)$ and $P(\text{sum}=8\mid\text{first die}=3)$. Are the events independent?

**(ii)** Find $P(\text{sum}=7\mid\text{first die}=3)$ and explain why the answer would be the same for *any* value of the first die.

**(iii)** Find $P(\text{both dice even}\mid\text{sum is even})$ using the reduced sample space.

**(iv)** A family has two children. Find $P(\text{both girls}\mid\text{the elder is a girl})$ and $P(\text{both girls}\mid\text{at least one is a girl})$, assuming all four sex combinations equally likely.

**(v)** In (iv), a student objects: *"Given at least one girl, the other child is either a boy or a girl, so the answer must be $\tfrac12$."* **Diagnose the error precisely**, and connect it to Example 3l.

> [!example]- Solution
> **(i)** $P(\text{sum}=8)=\tfrac5{36}$ (from $(2,6),(3,5),(4,4),(5,3),(6,2)$).
>
> Given the first die is 3, the reduced space is $\{(3,1),\dots,(3,6)\}$, and only $(3,5)$ works:
> $$P(\text{sum}=8\mid\text{first}=3)=\mathbf{\tfrac16}$$
> **Not independent**, since $\tfrac16\ne\tfrac5{36}$. *(This is Example 4c's logic with 8 in place of 6.)*
>
> ---
> **(ii)** $P(\text{sum}=7\mid\text{first}=3)=\tfrac16$ — only $(3,4)$ works out of six.
>
> **Whatever the first die shows, exactly one value of the second die completes a 7.** So the conditional probability is always $\tfrac16=P(\text{sum}=7)$, and **the sum being 7 is independent of the first die** ✓ (Example 4c).
>
> > **7 is the unique sum with this property**, which is why it is the pivot of so many dice problems — and of the "5 before 7" and craps calculations.
>
> ---
> **(iii)** The sum is even iff both dice are even or both odd: $3\times3+3\times3=18$ outcomes. **Both even accounts for 9 of these:**
> $$P=\tfrac9{18}=\mathbf{\tfrac12}$$
> *(Check via (2.1): $\tfrac{9/36}{18/36}=\tfrac12$ ✓.)*
>
> ---
> **(iv)** Sample space $\{GG,GB,BG,BB\}$, all $\tfrac14$ (first letter = elder).
> $$P(GG\mid\text{elder is }G)=\frac{1/4}{2/4}=\mathbf{\tfrac12} \qquad P(GG\mid\text{at least one }G)=\frac{1/4}{3/4}=\mathbf{\tfrac13}$$
>
> ---
> **(v)** **The error is assuming the two surviving possibilities are equally likely.**
>
> *"At least one girl"* removes only $BB$, leaving **three** equally likely outcomes $GG,GB,BG$. **The student's "the other child is a boy" corresponds to *two* of them** ($GB$ and $BG$), and "a girl" to only one. **Two-to-one, not one-to-one.**
>
> > **This is structurally identical to Example 3l's three cards:** *"Some students guess $\tfrac12$... their mistake is in assuming that these two possibilities are equally likely."* **Count the underlying equally likely outcomes (sides of cards, birth orders), never the verbal categories they fall into.**
> >
> > **And note the warning from Example 3m:** if you learned "at least one is a girl" by *meeting one of the children*, rather than by being told, **the answer can change to $\tfrac12$.** *How you obtained the information is part of the problem.*

---

**Exercise 2 — The multiplication rule**

**(i)** Three cards are drawn without replacement from a standard deck. Find $P(\text{all three hearts})$ using the multiplication rule, and check with binomial coefficients.

**(ii)** Five cards are dealt. Find $P(\text{no ace})$ both sequentially and combinatorially.

**(iii)** An urn has 5 red and 3 blue balls. Three are drawn without replacement. Find $P(\text{red, blue, red in that order})$ and $P(\text{exactly 2 red})$.

**(iv)** In Example 2g, explain in your own words why $P(E_2\mid E_1)=\tfrac{39}{51}$ rather than $\tfrac{39}{52}$.

**(v)** Six people, three of whom are strong, are randomly paired into three pairs. Find $P(\text{no two strong people are paired})$, using the Example 2h technique.

> [!example]- Solution
> **(i)** $$\frac{13}{52}\cdot\frac{12}{51}\cdot\frac{11}{50}=\mathbf{\tfrac{11}{850}}\approx.01294$$
> **Check:** $\dfrac{\binom{13}{3}}{\binom{52}{3}}=\dfrac{286}{22100}=\tfrac{11}{850}$ ✓
>
> ---
> **(ii)** **Sequentially** — each draw must avoid the 4 aces:
> $$\frac{48}{52}\cdot\frac{47}{51}\cdot\frac{46}{50}\cdot\frac{45}{49}\cdot\frac{44}{48}=\mathbf{\tfrac{35673}{54145}}\approx.6588$$
> **Combinatorially:** $\dfrac{\binom{48}{5}}{\binom{52}{5}}=\dfrac{1{,}712{,}304}{2{,}598{,}960}=\tfrac{35673}{54145}$ ✓
>
> ---
> **(iii)** **In that order:**
> $$\frac58\cdot\frac37\cdot\frac46=\frac{60}{336}=\mathbf{\tfrac5{28}}$$
>
> **Exactly 2 red** (any order): three orders — RRB, RBR, BRR — each with the same probability by the multiplication rule:
> $$3\times\frac58\cdot\frac47\cdot\frac36=3\times\frac{60}{336}=\mathbf{\tfrac{15}{28}}$$
> **Check combinatorially:** $\dfrac{\binom52\binom31}{\binom83}=\dfrac{10\times3}{56}=\tfrac{30}{56}=\tfrac{15}{28}$ ✓
>
> > **Note all three orderings gave the same $\tfrac5{28}$** — numerators are the same factors in a different order. **That is exactly why "order doesn't matter" arguments work.**
>
> ---
> **(iv)** **We are asking where the ace of hearts is, *given* the ace of spades is already placed.**
>
> $\spadesuit$A is in some pile; **the other 12 cards of that pile are equally likely to be any 12 of the 51 cards not yet accounted for.** So $\heartsuit$A joins it with probability $\tfrac{12}{51}$, and avoids it with probability $\tfrac{39}{51}$.
>
> **Not $\tfrac{39}{52}$, because $\spadesuit$A itself is no longer available to be chosen** — we have conditioned on it, so it leaves the pool. **The denominator is always the number of cards still genuinely uncertain.**
>
> ---
> **(v)** Let $W_i$ = "strong person $i$ is paired with a weak person," $i=1,2,3$.
> $$P(W_1)=\tfrac35 \quad\text{(3 weak among the other 5)}$$
> $$P(W_2\mid W_1)=\tfrac23 \quad\text{(3 people left: strong 3, and 2 weak)}$$
> $$P(W_3\mid W_1W_2)=1 \quad\text{(only the last weak person remains)}$$
> $$P(W_1W_2W_3)=\tfrac35\cdot\tfrac23\cdot1=\mathbf{\tfrac25}$$
>
> **Check by counting.** The 6 people split into 3 unordered pairs in $\dfrac{6!}{2^3\,3!}=15$ ways ([[01 - Combinatorial Analysis|ch. 01 §5]]'s unlabelled correction). Pairings with each strong person matched to a weak one number $3!=6$. **$\tfrac6{15}=\tfrac25$** ✓
>
> > **The sequential route needed no combinatorics at all** — this is the practical advantage of the multiplication rule.

---

**Exercise 3 — Bayes and the base rate**

A diagnostic test has **sensitivity** $P(+\mid D)=.99$ and **specificity** $P(-\mid D^c)=.98$.

**(i)** Compute $P(D\mid +)$ when the prevalence is $.001$, $.01$, $.1$ and $.5$. Tabulate.

**(ii)** At prevalence $.001$, restate the calculation in **natural frequencies** out of 100,000 people.

**(iii)** At what prevalence does a positive test make disease more likely than not?

**(iv)** Compute $P(D^c\mid -)$ at prevalence $.001$ and comment on the asymmetry with (i).

**(v)** A journalist writes: *"The test is 99% accurate, so if you test positive there's a 99% chance you're ill."* **Name the fallacy and state exactly which two quantities have been confused.**

> [!example]- Solution
> **(i)** $$P(D\mid+)=\frac{.99\pi}{.99\pi+.02(1-\pi)}$$
>
> | Prevalence $\pi$ | $P(D\mid+)$ |
> |---|---|
> | $.001$ | $\mathbf{.0472}$ |
> | $.01$ | $\mathbf{.3333}$ |
> | $.1$ | $\mathbf{.8462}$ |
> | $.5$ | $\mathbf{.9802}$ |
>
> **The test never changed — only the prior. And the answer moves from 5% to 98%.**
>
> ---
> **(ii)** **Out of 100,000 people at prevalence $.001$:**
>
> | | Test + | Test − | Total |
> |---|---|---|---|
> | **Diseased** | $99$ | $1$ | $100$ |
> | **Healthy** | $1998$ | $97{,}902$ | $99{,}900$ |
> | **Total** | $2097$ | $97{,}903$ | $100{,}000$ |
>
> $$P(D\mid+)=\frac{99}{2097}\approx\mathbf{.0472}\ ✓$$
>
> > **The table makes it obvious: 1998 false positives from the 99,900 healthy people swamp the 99 true positives.** *"A 2% error rate on a huge group beats a 99% success rate on a tiny one."* **This is Ross's Example 3d device — always convert to counts when the base rate is small.**
>
> ---
> **(iii)** Set $P(D\mid+)=\tfrac12$, i.e. $.99\pi=.02(1-\pi)$:
> $$\pi=\frac{.02}{.99+.02}=\frac{.02}{1.01}\approx\mathbf{.0198}$$
> **Below about 2% prevalence, a positive result still leaves the disease more likely absent than present.**
>
> ---
> **(iv)** $$P(D^c\mid-)=\frac{.98(.999)}{.98(.999)+.01(.001)}\approx\mathbf{.99999}$$
>
> > **The asymmetry is striking and it is not a defect.** A **negative** result is enormously informative ($99.999\%$ reassurance); a **positive** result is nearly worthless ($4.7\%$).
> >
> > **Both are consequences of the same base rate.** For a rare disease, almost everyone is healthy, so *"healthy"* is easy to confirm and *"diseased"* is hard. **This is why rare-disease screening uses a cheap sensitive test first (to rule out) followed by an expensive specific test (to rule in).**
>
> ---
> **(v)** **The base rate fallacy** — a form of the **prosecutor's fallacy**. The confusion is between
> $$\underbrace{P(+\mid D)=.99}_{\text{sensitivity — a property of the test}} \qquad\text{and}\qquad \underbrace{P(D\mid+)=.047}_{\text{what the patient wants to know}}$$
>
> **These are different conditional probabilities and here they differ by a factor of 21.** *(Also: "99% accurate" is itself ambiguous — sensitivity and specificity are different numbers and neither is "accuracy.")*
>
> > **The general statement, which is worth memorising: $P(A\mid B)\ne P(B\mid A)$, and Bayes's formula is precisely the exchange rate between them.** It is why Example 3o's DNA case is dangerous — $P(\text{match}\mid\text{innocent})=10^{-5}$ is *not* $P(\text{innocent}\mid\text{match})$.

---

**Exercise 4 — The odds form of Bayes**

**(i)** State the odds form of Bayes's formula and derive it from (3.5).

**(ii)** A hypothesis has prior probability $.1$. A test with sensitivity $.99$ and specificity $.98$ comes back positive. **Use the odds form** to find the posterior, and check it against the direct formula.

**(iii)** A **second, conditionally independent** test also comes back positive. Find the new posterior.

**(iv)** In Example 3i, verify the answer $\tfrac25$ using the direct form of Bayes, and identify prior odds and likelihood ratio.

**(v)** Explain, using the odds form, exactly why the prosecutor's argument in Example 3g fails — and describe what he *would* have needed to establish.

> [!example]- Solution
> **(i)** $$\frac{P(H\mid E)}{P(H^c\mid E)}=\frac{P(H)}{P(H^c)}\times\frac{P(E\mid H)}{P(E\mid H^c)}$$
>
> **Derivation:** write Bayes twice, for $H$ and for $H^c$, and divide:
> $$\frac{P(H\mid E)}{P(H^c\mid E)}=\frac{P(E\mid H)P(H)/P(E)}{P(E\mid H^c)P(H^c)/P(E)}$$
> **$P(E)$ cancels** — which is the whole point. $\blacksquare$
>
> ---
> **(ii)** **Prior odds:** $\dfrac{.1}{.9}=\tfrac19$. **Likelihood ratio:** $\dfrac{.99}{.02}=49.5$.
> $$\text{posterior odds}=\tfrac19\times49.5=\mathbf{5.5}=\tfrac{11}{2} \quad\Longrightarrow\quad P=\frac{5.5}{6.5}=\tfrac{11}{13}\approx\mathbf{.8462}$$
> **Direct check:** $\dfrac{.99(.1)}{.99(.1)+.02(.9)}=\dfrac{.099}{.117}=.8462$ ✓
>
> ---
> **(iii)** **Multiply by the likelihood ratio again** — this is the advantage of the odds form:
> $$\text{odds}=\tfrac19\times49.5^2=\tfrac{1089}{4}=272.25 \quad\Longrightarrow\quad P=\frac{272.25}{273.25}\approx\mathbf{.9963}$$
>
> > **Two positives take you from 10% to 99.6%.** **Note the assumption doing the work: the tests must be *conditionally independent given disease status*.** **If they share a failure mode** — both fooled by the same interfering substance — **the second test adds far less than the calculation suggests.** *Real repeat tests are usually correlated, and treating them as independent overstates confidence.*
>
> ---
> **(iv)** Direct form:
> $$P(A\mid H)=\frac{(\tfrac14)(\tfrac23)}{(\tfrac14)(\tfrac23)+(\tfrac34)(\tfrac13)}=\frac{1/6}{1/6+1/4}=\frac{1/6}{5/12}=\mathbf{\tfrac25}\ ✓$$
>
> **Prior odds** $=\dfrac{2/3}{1/3}=\mathbf{2}$ (two type-A coins to one type-B). **Likelihood ratio** $=\dfrac{P(H\mid A)}{P(H\mid B)}=\dfrac{1/4}{3/4}=\mathbf{\tfrac13}$.
> $$\text{posterior odds}=2\times\tfrac13=\tfrac23 \quad\Longrightarrow\quad P=\frac{2/3}{5/3}=\tfrac25\ ✓$$
>
> > **The two factors pull in opposite directions and the likelihood wins.** A priori type A was favoured 2:1; the head made it 3× less likely; net result **type A is now the minority explanation.**
>
> ---
> **(v)** From the odds form, the evidence **raises** the probability of guilt iff
> $$\frac{P(E\mid H)}{P(E\mid H^c)}>1 \qquad\text{i.e.}\qquad P(E\mid H)>P(E\mid H^c)$$
>
> **The prosecutor established only that $P(E\mid H)>0$** — that the play was *consistent with* cheating. **That is compatible with a likelihood ratio of exactly 1** (or even below 1), in which case the evidence is worthless or actively exculpatory.
>
> **What he needed to show: that the observed play was *more probable under cheating than under honest play*.** The defence's point — that the play was also perfectly consistent with their standard line — is precisely the claim that $\text{LR}\approx1$.
>
> > **This generalises far beyond bridge.** *"The data are consistent with my theory"* is not evidence for the theory. **Evidence requires a comparison** — the theory must explain the data *better than the alternatives do*. **A theory flexible enough to accommodate any outcome ($P(E\mid H)\approx P(E\mid H^c)$ for all $E$) can never be supported by data at all.**

---

**Exercise 5 — Independence**

**(i)** Two fair coins are flipped. Let $E$ = first is heads, $F$ = second is heads, $G$ = the two flips differ. Show that $E,F,G$ are **pairwise** independent but **not** mutually independent.

**(ii)** Explain why (i) shows the three-event definition of independence needs all four conditions.

**(iii)** Three components with reliability $.9$ each. Compare a **series** and a **parallel** system.

**(iv)** Rolling two dice repeatedly, find $P(\text{6 before 7})$ using the general result of Example 4h.

**(v)** In the gambler's ruin with $N=20$ and $i=10$, compute $P_i$ for $p=.5$, $p=.49$ and $p=.45$. Comment.

**(vi)** In Example 5a, the accidents in years 1 and 2 are **not** independent, yet given the person's class they **are**. Explain how both can hold, and why this matters.

> [!example]- Solution
> **(i)** Sample space $\{HH,HT,TH,TT\}$, each $\tfrac14$.
> $$P(E)=P(F)=P(G)=\tfrac12$$
>
> | Pair | Joint | Product | Independent? |
> |---|---|---|---|
> | $EF=\{HH\}$ | $\tfrac14$ | $\tfrac12\cdot\tfrac12=\tfrac14$ | ✅ |
> | $EG=\{HT\}$ | $\tfrac14$ | $\tfrac14$ | ✅ |
> | $FG=\{TH\}$ | $\tfrac14$ | $\tfrac14$ | ✅ |
> | $EFG$ | $\mathbf{0}$ | $\tfrac12\cdot\tfrac12\cdot\tfrac12=\tfrac18$ | ❌ |
>
> **$EFG=\emptyset$** — if both flips are heads they cannot differ. **So the triple condition fails while all three pairs hold.**
>
> ---
> **(ii)** **Because pairwise independence carries no information about triples.** In (i), knowing *any one* of $E,F,G$ tells you nothing about *any other one* — yet **knowing any two determines the third completely.** ($E$ and $F$ both true forces $G$ false.)
>
> **So the four-condition definition is not redundant bookkeeping; the triple condition is genuinely independent of the three pairwise ones.**
>
> > **Ross's Example 4e makes the complementary point** — there $E$ was pairwise independent of $F$ and of $G$, but $P(E\mid FG)=1$. **Together the two examples show that neither direction of implication holds**, which is exactly why the definition demands *every* subset.
>
> ---
> **(iii)** **Series** (needs all three): $.9^3=\mathbf{.729}$
> **Parallel** (needs at least one): $1-(.1)^3=\mathbf{.999}$
>
> > **Same components, failure probability $27\%$ versus $0.1\%$ — a factor of 271.** **Redundancy buys reliability; chaining destroys it.**
> >
> > **The practical corollary: a pipeline of 20 steps each 99% reliable succeeds only $.99^{20}=81.8\%$ of the time.** Long series systems are fragile in a way that is easy to underestimate.
>
> ---
> **(iv)** $P(6)=\tfrac5{36}$, $P(7)=\tfrac6{36}$, so by $\dfrac{P(E)}{P(E)+P(F)}$:
> $$P(\text{6 before 7})=\frac{5}{5+6}=\mathbf{\tfrac5{11}}\approx.455$$
> **Only the relative rates matter** — the $\tfrac{25}{36}$ of rolls that are neither is irrelevant. *(Compare Example 4h's $\tfrac4{10}=\tfrac25$ for 5 before 7.)*
>
> ---
> **(v)** With $N=20$, $i=10$ (an even fight in stake terms):
>
> | $p$ | $P_{10}$ |
> |---|---|
> | $.50$ | $\mathbf{.5000}$ |
> | $.49$ | $\mathbf{.4013}$ |
> | $.45$ | $\mathbf{.1185}$ |
>
> > **A 1% disadvantage per round costs 10 percentage points of win probability. A 5% disadvantage costs 38.**
> >
> > **This is the mathematics of the casino.** The house edge on roulette is about $2.7\%$ — small per spin, ruinous over a session, **because the disadvantage compounds geometrically in $(q/p)^i$.** *The only reliable way to win against a negative edge is to make very few, very large bets.*
>
> ---
> **(vi)** **Both statements are true and there is no contradiction.**
>
> - **Given the class**, the accident rates are fixed ($.4$ or $.2$) and the years are independent: $P(A_2\mid A\,A_1)=P(A_2\mid A)=.4$.
> - **Unconditionally**, $P(A_2\mid A_1)\approx.29>P(A_2)=.26$ — **they are positively dependent.**
>
> **The mechanism: the first accident is *evidence about which class the person is in*.** It raises $P(A\mid A_1)$ from $.30$ to $\tfrac6{13}\approx.46$, and accident-prone people have higher rates in year 2 as well. **The dependence flows entirely through the unobserved class.**
>
> > [!important] Why this matters more than any other idea in the chapter
> > **This is *conditional independence*, and it is the structural backbone of statistical modelling:**
> > - **Latent-variable and mixture models** — observations are independent given the latent class, dependent without it
> > - **Naive Bayes classifiers** — features assumed independent *given the label*, never marginally
> > - **Bayesian networks and graphical models** — the entire formalism is a map of which conditional independences hold
> > - **Hidden Markov models** ([[09 - Additional Topics in Probability|ch. 09]]) — observations independent given the hidden state
> >
> > **Conflating "independent" with "conditionally independent" is the most consequential modelling error in the whole subject**, and Example 5a is the smallest complete instance of it.

---

## 📝 Summary

- **$P(E\mid F)=\dfrac{P(EF)}{P(F)}$ for $P(F)>0$.** Conditioning **shrinks the sample space to $F$** and re-normalises; with equally likely outcomes, just recount inside $F$. **Surviving outcomes keep their original relative weights** — the error in Example 2b, Example 3l and the two-child problem is always assuming the survivors re-group into equally likely *categories*.
- **Conditioning is primarily a computational tool.** Ross's second reason for its importance — *"even when no partial information is available, conditional probabilities can often be used to compute the desired probabilities more easily"* — is the one that matters.
- **Multiplication rule:** $P(E_1\cdots E_n)=P(E_1)P(E_2\mid E_1)\cdots P(E_n\mid E_1\cdots E_{n-1})$. **The art is choosing the order of events so each conditional probability is easy** (Examples 2g, 2h).
- **Law of total probability:** $P(E)=\sum_iP(E\mid F_i)P(F_i)$ over mutually exclusive, exhaustive $F_i$. **Find the missing information that would make the problem easy, then average over its values.**
- **Bayes's formula:** $P(F_j\mid E)=\dfrac{P(E\mid F_j)P(F_j)}{\sum_iP(E\mid F_i)P(F_i)}$ — **posterior $\propto$ likelihood $\times$ prior**, with the denominator merely normalising.
- **The base rate dominates for rare events.** A 95%-sensitive test with a 1% false positive rate on a 0.5%-prevalent disease gives $P(D\mid+)=\tfrac{95}{294}\approx\mathbf{.32}$. **Convert to natural frequencies** ("out of 200 people…") whenever the prior is small — the answer becomes obvious.
- **Odds form:** $\dfrac{P(H\mid E)}{P(H^c\mid E)}=\dfrac{P(H)}{P(H^c)}\times\dfrac{P(E\mid H)}{P(E\mid H^c)}$. **Evidence supports $H$ if and only if $P(E\mid H)>P(E\mid H^c)$** — *"consistent with"* is not evidence (Example 3g).
- **Independence is $P(EF)=P(E)P(F)$** — a numerical condition, not an intuition. **If $E\perp F$ then $E\perp F^c$.** **Pairwise independence does not imply mutual independence**, in either direction: all $\binom n2$ pairs can factorise while the triple does not (Exercise 5), and a variable can be pairwise independent of two events while being determined by their intersection (Example 4e).
- **Independent trials give the binomial:** $P(k\text{ successes in }n)=\binom nkp^k(1-p)^{n-k}$, and $P(\text{at least one success})=1-(1-p)^n$. **Parallel systems: $1-\prod(1-p_i)$; series: $\prod p_i$.**
- **For repeated trials with mutually exclusive $E$ and $F$, $P(E\text{ before }F)=\dfrac{P(E)}{P(E)+P(F)}$** — only relative rates matter. **The gambler's ruin** gives $P_i=\dfrac{1-(q/p)^i}{1-(q/p)^N}$ (or $i/N$ when fair), and small per-round edges compound dramatically.
- **$P(\cdot\mid F)$ satisfies all three axioms**, so **every theorem of [[02 - Axioms of Probability|ch. 02]] holds inside a conditional world** — just append $\mid F$ to every event.
- **Conditional independence is not independence.** Accidents in consecutive years are dependent unconditionally but independent given the person's risk class (Example 5a) — **the structural basis of naive Bayes, mixture models and graphical models.**

---

## ⚠️ Important Notes

> [!warning] $P(A\mid B)\ne P(B\mid A)$ — and Bayes is the exchange rate
> **The single most consequential error in applied probability.** Examples:
>
> | Confusing | With | Called |
> |---|---|---|
> | $P(+\mid\text{disease})=.95$ | $P(\text{disease}\mid+)=.32$ | **base rate fallacy** |
> | $P(\text{match}\mid\text{innocent})=10^{-5}$ | $P(\text{innocent}\mid\text{match})$ | **prosecutor's fallacy** |
> | $P(\text{data}\mid H_0)$ | $P(H_0\mid\text{data})$ | misreading a $p$-value |
>
> **The gap is the prior**, and it can be several orders of magnitude. **Whenever a conditional probability is quoted, ask: conditional on what, and is that the direction I need?**

> [!warning] Conditioning removes outcomes; it does not create equally likely categories
> **The recurring $\tfrac12$-versus-$\tfrac13$ error:**
>
> | Problem | Wrong reasoning | Right answer |
> |---|---|---|
> | Both heads given at least one head (2b) | *"both, or just one — 2 cases"* | $\tfrac13$ (3 outcomes survive) |
> | Other side black given red showing (3l) | *"all-red card, or mixed card"* | $\tfrac13$ (6 **faces**, 3 survive) |
> | Both girls given at least one girl | *"the other is a boy or a girl"* | $\tfrac13$ |
>
> **In every case the intuition merges outcomes of unequal weight into verbal categories.** **Enumerate the underlying equally likely outcomes — faces, birth orders, dice pairs — and count those.**

> [!warning] How you learned something is part of the data
> **Example 3m has no answer as stated.** *"Hence, as stated, the problem is incapable of solution."* Depending on how the mother chooses which child to walk with, $P(\text{both girls}\mid\text{saw a girl})$ is $\tfrac12$, $\tfrac13$, or $\dfrac1{1+2q}$.
>
> **The sample space is not $\{GG,GB,BG,BB\}$ — it is $(s_1,s_2,i)$, including which child you saw.** *"It is not enough to make assumptions only about the genders of the children."*
>
> **Every famous probability paradox in this family — Monty Hall, the boy-girl problem, the two-envelope problem — dissolves once the observation mechanism is stated.** **If a problem feels ambiguous, the missing assumption is almost always about *how the information reached you*.**

> [!warning] Mutually exclusive is the opposite of independent
> **Repeated from [[02 - Axioms of Probability|ch. 02]] because it is worth it.** If $EF=\emptyset$ and both have positive probability, then
> $$P(EF)=0\ne P(E)P(F)>0$$
> **so they are dependent — maximally so.** Knowing $E$ occurred tells you $F$ certainly did not.
>
> **The words sound similar in English ("they have nothing to do with each other") and mean opposite things in probability.**

> [!warning] Pairwise independence is strictly weaker — in both directions
> - **Exercise 5(i):** three events, all $\binom32$ pairs independent, **but $P(EFG)=0\ne\tfrac18$.**
> - **Example 4e:** $E$ independent of $F$ and of $G$, **but $P(E\mid FG)=1$.**
>
> **This is why independence of $n$ events requires *every* subset to factorise — $2^n-n-1$ conditions, not $\binom n2$.**
>
> **Practically: verifying that features are pairwise uncorrelated tells you nothing about whether they are jointly independent.**

> [!warning] "Consistent with the hypothesis" is not evidence for it
> From Example 3g: evidence supports $H$ **only if** $P(E\mid H)>P(E\mid H^c)$, and the strength is the **likelihood ratio**, not the likelihood.
>
> **The prosecutor showed only $P(E\mid H)>0$.** That is compatible with $\text{LR}=1$ (worthless) or $\text{LR}<1$ (exculpatory).
>
> > **A theory that can accommodate any observation has $P(E\mid H)\approx P(E\mid H^c)$ for every $E$ — and therefore can never be supported by data.** **Flexibility is not a virtue in a hypothesis; it is what makes it untestable.**

> [!warning] Independence given a variable is not independence
> **Example 5a:** accidents in years 1 and 2 are **independent given the person's risk class** but **dependent** unconditionally ($P(A_2\mid A_1)=.29$ versus $P(A_2)=.26$). **The first accident is evidence about the unobserved class.**
>
> **This runs in both directions**, and both are common:
> - **Dependent → conditionally independent:** the accidents above; naive Bayes features; HMM observations
> - **Independent → conditionally *dependent*:** two independent causes of a common effect become dependent once the effect is observed (*explaining away*, or **collider bias**)
>
> **Conditioning can create dependence as well as destroy it.** **In any model with latent structure, always ask which independence is being claimed and conditional on what.**

> [!warning] Small edges compound
> **Gambler's ruin with $N=20$, $i=10$:** $p=.50$ gives $.500$; $p=.49$ gives $.401$; $p=.45$ gives $.119$.
>
> **A 1% per-round disadvantage costs 10 percentage points; a 5% disadvantage costs 38.** The mechanism is the $(q/p)^i$ term — **exponential in the stake, not linear.**
>
> **This is the mathematics of the house edge**, and also of the clinical-trial error rate ($.017$ at $M=5$ falling to $.0003$ at $M=10$). **Whenever a small per-step bias is repeated many times, expect the aggregate effect to be far larger than intuition suggests.**

> [!note] Cross-subject connections
> - [[02 - Axioms of Probability|Ch. 02]] — §5 shows $P(\cdot\mid F)$ satisfies all three axioms, so **the entire chapter transfers into any conditional world unchanged.**
> - [[07 - Properties of Expectation|Ch. 07]] — **conditioning reappears for expectations**: $\mathbb{E}[X]=\mathbb{E}[\mathbb{E}[X\mid Y]]$ is the exact analogue of the law of total probability, and it is the most powerful computational tool in the book.
> - [[04 - Random Variables|Ch. 04]] — **Example 4f *is* the binomial distribution** and Example 2f produces the **Poisson** with $\lambda=1$; both arrive here as consequences of independence.
> - [[09 - Additional Topics in Probability|Ch. 09]] — **the gambler's ruin is a Markov chain** with absorbing states, and the conditioning-on-the-first-step argument is exactly how Markov chains are analysed.
> - [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] — **Bayes's formula is the whole of Bayesian inference**; the likelihood ratio of Example 3g is the Neyman–Pearson test statistic; the sequential drug trial is a sequential probability ratio test.
> - [[Machine Learning/contents/00-Index|Machine Learning]] — **naive Bayes classifiers assume conditional independence of features given the label** (Exercise 5(vi)); the base rate problem of Exercise 3 is why **precision collapses on imbalanced datasets** even when recall is excellent.
> - [[Econometrics/contents/00-Index|Econometrics]] — the conditional expectation $\mathbb{E}(u\mid x)=0$ that the whole subject turns on is built on the conditioning defined here.

---

> [!warning] Gaps in the source material
> **No lecture slides exist for this subject** — chapter scope and emphasis are my editorial decisions. See [[00-Index]].
>
> **Figures are images and cannot be extracted:**
> - **Figure 3.1** ($E=EF\cup EF^c$, with $EF$ shaded and $EF^c$ striped) — only the caption and stray labels `EF`, `EFEF c` survive. **The decomposition is stated algebraically in the text**, so §2a loses nothing.
> - **Figure 3.2** (a parallel system, "functions if current flows from A to B") — extracts as `A B`, `1`, `2`, `3`, `n`. **The circuit diagram is lost**; §3b describes it in words, which the text also does.
> - **Example 4n's NCAA bracket graph** is an image of the tournament tree; only fragments `(1,16)`, `(8,9)`, `(5,12)` extract. **This example is not developed in these notes** — it depends entirely on reading the bracket structure off the figure.
>
> **Notation mangled by the PDF layout** (all reconstructed by hand and cross-checked against worked examples):
> - **`q` is `∞`**, **`(` and `)` are `⊂` and `⊃`**, **`…` is `≤`**, **`Ú` is `≥`**, **`Z` is `≠`**, **`L` is `≈`** — the same substitution set as [[02 - Axioms of Probability|ch. 02]]. E.g. `P(H|E) Ú P(H)` is $P(H\mid E)\ge P(H)$ and `i Z 1` is $i\ne1$.
> - **Fractions extract as numerator-newline-denominator throughout**, so every displayed conditional probability had to be reassembled.
> - **Subscripts detach:** `Ec 1Ec 2` is $E_1^cE_2^c$, `BA,a` is $B_{A,a}$, `P{5 on any trial}= 4 36` is $P=\tfrac4{36}$.
> - **Greek letters survive** ($\alpha$, $\beta$, $\gamma$) but **`γ` occasionally renders as `g`** in the drug-trial passage.
>
> **A typographical error in the source (Example 2f):** the final line of the derivation reads
> > `P(exactly k matches) = ( N k ) P(EG) = PN−K/K!`
>
> **using capital $K$ in `PN−K/K!` where the rest of the example uses lower-case $k$.** The intended expression is $P_{N-k}/k!$, as the following line (`≈ e^{-1}/k!`) confirms. **Reproduced correctly in §1b.**
>
> **A second inconsistency (Example 5o of ch. 2 style, here in Example 4j):** Ross writes the boundary conditions as `Pn,0 = 0, P0, m = 1` with inconsistent spacing, but the meaning is unambiguous from the recursion.
>
> **Verification performed:** every numeric claim in Examples 2a–5b was independently recomputed — $\tfrac23$; $\tfrac12$ and $\tfrac13$; $.339$; $\tfrac13$; $\tfrac{14}{33}$ (both routes); $\tfrac{39}{51},\tfrac{26}{50},\tfrac{13}{49}$ and $.105$; $\tfrac8{35}$; $.26$ and $\tfrac6{13}$; $\tfrac56$; $\tfrac{95}{294}=.3231$ (both of Ross's arguments agree exactly); $.833$; $.882$; $.28$; $\tfrac23$ odds $\to\tfrac25$; $.41$ and $\tfrac{14}{41},\tfrac{12}{41},\tfrac{15}{41}$; $\alpha=\tfrac1{19{,}900}$ and $.9099$; $\tfrac25$ (both routes); $\tfrac13$ and $.87$; $p=\tfrac{15}{42}$; $.017$ and $.0003$; $.29$; $\tfrac{2p}{1+p}$. **All agree with the text. No arithmetic errors were found in this chapter.**
>
> **One point where the text is thinner than the result deserves:** Example 2f's conclusion that the number of matches is asymptotically **Poisson(1)** is never named as such — Ross simply writes $\approx e^{-1}/k!$. **The connection to [[04 - Random Variables|ch. 04 §7]] is flagged in §1b of these notes**, since a reader meeting the Poisson three chapters later is unlikely to recall having already derived it.

#probability #conditional-probability #bayes #independence #odds
