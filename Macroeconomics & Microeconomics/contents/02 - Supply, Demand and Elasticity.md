---
subject: Macroeconomics & Microeconomics
chapter: 2
tags: [ds, economics, microeconomics, supply-demand, elasticity, total-revenue, equilibrium]
source: "Mankiw, *Principles of Macroeconomics* (2017), ch. 4–5"
---

# Supply, Demand and Elasticity

**Supply and demand is the model economists reach for first**, and elasticity is what makes it quantitative rather than directional. Without elasticity the model says only *which way* a price moves; with it, the model says *how far*, and **that is usually the question that matters.**

**Three results.**

**§3 — the "obvious" way to compute elasticity is ambiguous.** *(Computed: the same two points give **0.6667** measured one way and **1.5000** measured the other — a **125%** disagreement.)* Mankiw's midpoint method fixes it, and §3b shows why: **all three measures converge on the same derivative as the interval shrinks.**

**§5 — a straight-line demand curve has constant slope and wildly varying elasticity** *(computed: from **0.0769** to **13.0000** along one line)*, and **total revenue peaks exactly where elasticity = 1** *(computed: at $P^*=\$3.50$, where $e = 1.0000$ exactly)*. Mankiw prints a table showing this and never explains it; **one derivative he declines to write does.**

**§6 — good news for farming is bad news for farmers.** *(Computed: the same 50% productivity gain changes farm revenue by **−15.6%**, **−4.0%** or **+24.0%** depending only on the demand elasticity.)*

> [!warning] ⚠️ Every equation reconstructed, not transcribed
> Operators extract as digits (`5`→`=`, `1`→`+`, `2`→`−`, `3`→`×`). **The midpoint formula is the worst case in the whole book** — see [[00-Index]].

## 📘 Main Knowledge

### 1. The market forces

**A competitive market** has many buyers and sellers, each too small to influence the price — so everyone is a **price taker**.

| | **demand** | **supply** |
|---|---|---|
| **law** | $P\uparrow \Rightarrow Q_d\downarrow$ | $P\uparrow \Rightarrow Q_s\uparrow$ |
| **shifted by** | income, prices of related goods, tastes, expectations, **number of buyers** | input prices, technology, expectations, **number of sellers** |

> [!warning] ⚠️ Movement *along* a curve vs a *shift* of the curve — the error everyone makes
> **A change in the good's own price causes a movement along the curve. Anything else shifts the whole curve.**
>
> **The reason is that price is on the axis.** The demand curve is drawn *holding everything except price constant*, so price cannot shift it — price is the variable it is plotted against.
>
> **The practical test: ask whether the variable appears on an axis.** If it does, you move along; if it does not, you shift. **This one distinction resolves most confusion in the whole subject**, and it is the source of the classic false paradox — *"prices rose and quantity rose, so demand curves slope upward"* — which is a supply shift along a stable demand curve, not a violation of the law of demand.

**Related goods:**
- **Substitutes** — a rise in one's price raises demand for the other (butter and margarine).
- **Complements** — a rise in one's price *lowers* demand for the other (petrol and cars).

**Normal goods** — income up, demand up. **Inferior goods** — income up, demand *down* (bus travel).

### 2. Equilibrium

**Equilibrium is the price at which $Q_d = Q_s$.** Above it there is a **surplus** and sellers cut prices; below it a **shortage** and buyers bid prices up. **Both forces push toward equilibrium**, which is why the model is useful even though no market is literally ever at rest.

> [!note] The three-step method — worth using every time
> 1. **Does the event shift supply, demand, or both?**
> 2. **In which direction?**
> 3. **Use the diagram to compare the new equilibrium to the old.**
>
> **When both curves shift, one of price or quantity is always ambiguous** — the direction depends on the *relative* sizes of the shifts, which the diagram alone cannot settle. **Recognising that the answer is genuinely indeterminate is the correct answer**, not a failure of analysis.

### 3. ⚠️ Elasticity, and why the naive calculation is ambiguous

$$\text{price elasticity of demand}=\frac{\%\Delta Q_d}{\%\Delta P}$$

*(Verified: a 10% price rise causing a 20% quantity fall gives an elasticity of **2**.)*

> [!note] Elasticity is unit-free, and that is the point
> **It is a ratio of two percentages, so it does not depend on whether ice cream is measured in cones, litres or tonnes.** A *slope* does. That is why elasticity — not slope — is the standard measure of responsiveness, and why §5's distinction between them matters.
>
> *(The sign is always negative, since $Q$ falls when $P$ rises. Mankiw drops it and reports absolute values, as is conventional.)*

**But the obvious calculation gives two different answers.** *(Computed on Mankiw's own example — point A: $P=\$4$, $Q=120$; point B: $P=\$6$, $Q=80$:)*

| direction | $\%\Delta Q$ | $\%\Delta P$ | **elasticity** |
|---|---|---|---|
| A → B | −33.333% | +50.000% | **0.6667** |
| B → A | +50.000% | −33.333% | **1.5000** |

**The same two points, differing by 125%.** ✓ *(Book: 0.66 and 1.5.)*

**The midpoint method divides by the *average* rather than the starting point:**

$$e=\frac{(Q_2-Q_1)\,/\,[(Q_2+Q_1)/2]}{(P_2-P_1)\,/\,[(P_1+P_2)/2]}$$

*(Computed: midpoint $P=\$5$, $Q=100$; $\%\Delta P = 40\%$, $\%\Delta Q = -40\%$, **elasticity = 1.0000 in both directions** ✓.)*

### 3b. ⚠️ Why the midpoint method works

*(Computed — shrinking the interval around $(P,Q)=(5,100)$ on a curve with $dQ/dP=-20$:)*

| interval | naive A→B | naive B→A | midpoint | **spread** |
|---|---|---|---|---|
| ±1 | 0.66667 | 1.50000 | **1.00000** | 0.83333 |
| ±0.5 | 0.81818 | 1.22222 | **1.00000** | 0.40404 |
| ±0.1 | 0.96078 | 1.04082 | **1.00000** | 0.08003 |
| ±0.01 | 0.99601 | 1.00401 | **1.00000** | 0.00800 |
| ±0.001 | 0.99960 | 1.00040 | **1.00000** | 0.00080 |

$$\text{point elasticity}=\left|\frac{dQ}{dP}\right|\frac{P}{Q}=20\times\frac{5}{100}=\mathbf{1.00000}$$

> [!note] The midpoint method is not a different concept — it is a better approximation to the same derivative
> **All three measures converge on the point elasticity as the interval shrinks.** The naive versions are wrong by an amount proportional to the interval width; **the midpoint version is already exact at the centre**, which is why it is direction-free.
>
> **The underlying object is $e = \dfrac{dQ}{dP}\cdot\dfrac{P}{Q}$ — the elasticity of a function**, and it is the same construction used everywhere in applied work. **Mankiw never writes it**, which makes the midpoint formula look like an arbitrary trick instead of what it is: *the arc elasticity centred on the interval.* *(Labelled as an addition.)*

### 4. Total revenue

*(Verified — both of Mankiw's panels, price rising \$4 → \$5:)*

| case | quantity | total revenue | elasticity |
|---|---|---|---|
| **inelastic** | 100 → 90 | **\$400 → \$450** ✓ | 0.4737 |
| **elastic** | 100 → 70 | **\$400 → \$350** ✓ | 1.5882 |

| elasticity | price ↑ ⇒ total revenue |
|---|---|
| $e < 1$ (inelastic) | **rises** |
| $e = 1$ (unit elastic) | **unchanged** |
| $e > 1$ (elastic) | **falls** |

> [!note] The intuition, and then §5 makes it one equation
> **$TR = P\times Q$. Raising the price adds revenue on every unit still sold and loses revenue on the units no longer sold.** Elasticity is exactly the number that decides which effect is larger.

### 5. ⚠️ Constant slope, varying elasticity — and where revenue peaks

**Take a linear demand curve $Q = 14 - 2P$. The slope is $-2$ everywhere.** *(Computed:)*

| $P$ | $Q$ | **total revenue** | midpoint elasticity | region |
|---|---|---|---|---|
| 0 | 14 | 0 | 0.0769 | inelastic |
| 1 | 12 | 12 | 0.2727 | inelastic |
| 2 | 10 | 20 | 0.5556 | inelastic |
| **3** | **8** | **24** | **1.0000** | **unit elastic** |
| **4** | **6** | **24** | 1.8000 | elastic |
| 5 | 4 | 20 | 3.6667 | elastic |
| 6 | 2 | 12 | 13.0000 | elastic |
| 7 | 0 | 0 | — | |

**Elasticity sweeps from 0.0769 to 13.0000 along a line of constant slope.**

> [!warning] The grid ties at \$24 — and the tie is the clue
> **Revenue is \$24 at both $P=3$ and $P=4$, so the true maximum lies between them.** *(Solved exactly:)*
>
> $$TR(P)=P(14-2P)=14P-2P^2\qquad \frac{dTR}{dP}=14-4P=0\;\Rightarrow\;P^*=\mathbf{3.5}$$
>
> **$P^*=\$3.50$, $Q^*=7$, $TR^*=\$24.50$ — above both grid values.** *(And the tie is not a coincidence: 3 and 4 straddle 3.5 symmetrically, and a parabola gives symmetric points equal values.)*
>
> **The point elasticity there:** $e=2\times\dfrac{3.5}{7}=\mathbf{1.0000}$ exactly.

> [!warning] Total revenue is maximised exactly where elasticity = 1
> **Mankiw prints a table showing this and never explains it. One derivative does:**
>
> $$TR=P\cdot Q\;\Rightarrow\;\frac{dTR}{dP}=Q+P\frac{dQ}{dP}=Q\left[1+\frac{P}{Q}\frac{dQ}{dP}\right]=Q\,[1-e]$$
>
> **Zero exactly when $e=1$; positive when $e<1$ (inelastic — raise the price); negative when $e>1$ (elastic — cut it).**
>
> **So §4's three-way rule is not three rules. It is the sign of one derivative, and elasticity is the term that flips it.** *(Addition — Mankiw is calculus-free.)*

> [!note] Why elasticity varies on a straight line — slope and elasticity are different objects
> $$e=\left|\frac{dQ}{dP}\right|\frac{P}{Q}$$
> **The first factor is constant at 2. The second sweeps from 0 (at $P=0$) to $\infty$ (at $Q=0$).** That is the whole explanation.
>
> **"Flat curves are elastic" is a useful heuristic and not a definition** — it holds when comparing curves at the same point, not along one curve.

### 6. What determines elasticity

**Demand is more elastic when:**
- **close substitutes exist** — butter is elastic, insulin is not;
- **the good is a luxury rather than a necessity**;
- **the market is narrowly defined** — "vanilla ice cream" is far more elastic than "food";
- **the time horizon is longer.**

**Supply is more elastic when** output is easy to vary, the horizon is longer, and the firm is **below capacity** *(above capacity, supply goes near-vertical however high the price)*.

> [!note] The time-horizon point is the one that recurs
> **Petrol demand is nearly inelastic over a week and quite elastic over a decade** — you cannot change your commute tomorrow, but you can change your car, your job or where you live.
>
> **This is why short-run and long-run policy analysis reach different answers**, and it is the reason [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]]'s aggregate supply curve is flat in the short run and vertical in the long run. **The same idea, at the scale of a whole economy.**

### 7. ⚠️ Good news for farming is bad news for farmers

**A new hybrid raises yields by 50%.** *(Computed — the same supply shift against three demand curves:)*

| demand | elasticity at old equilibrium | harvest | **farm revenue** |
|---|---|---|---|
| $Q_d = 100-5P$ | **0.50 — inelastic** | +12.5% | **−15.6%** |
| $Q_d = 100-10P$ | 1.00 — unit elastic | +20.0% | −4.0% |
| $Q_d = 100-40P$ | **4.00 — elastic** | +36.4% | **+24.0%** |

> [!warning] Nothing about the technology changed — only the demand elasticity
> **With inelastic demand a better harvest makes farmers poorer**, because the price falls proportionately more than the quantity rises. **With elastic demand the identical innovation makes them richer.**
>
> **Two consequences worth carrying:**
>
> **1. It can be collectively rational for farmers to destroy crops** — and Mankiw notes that governments have paid farmers not to plant. **But each individual farmer still wants to grow more**, since one farmer's output does not move the price. **That gap between individually and collectively rational is [[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]]'s prisoners' dilemma**, and it is why the outcome requires a *policy* rather than emerging on its own.
>
> **2. Technological progress in a sector with inelastic demand shrinks that sector.** That is the entire history of agricultural employment — **US farm employment fell from about 40% of the workforce to under 2% precisely because farming got dramatically better at its job.** *(So "this industry is declining" and "this industry is improving fast" are not contradictory — for inelastic goods they are the same statement.)*

## ✏️ Exercises

**1. (Supply and demand.)** (a) Distinguish a movement along a curve from a shift, and give the test. (b) What resolves the "upward-sloping demand" paradox? (c) What happens when both curves shift?

> [!example]- Solution
> **(a) A change in the good's own price moves you *along*; anything else *shifts* the curve.**
>
> **The reason is structural: price is on an axis.** A demand curve is *defined* as the relationship between price and quantity demanded **holding all else constant** — so the variable it is plotted against cannot shift it.
>
> **The test: does the variable appear on an axis?**
>
> | change | effect |
> |---|---|
> | price of the good itself | **movement along** |
> | income, tastes, expectations, number of buyers | **shift of demand** |
> | price of a substitute or complement | **shift of demand** |
> | input prices, technology, number of sellers | **shift of supply** |
>
> **This single distinction resolves most confusion in the subject**, and the vocabulary reinforces it: a shift is a *change in demand*; a movement is a *change in quantity demanded*. **The two phrases are not interchangeable and the difference is not pedantry.**
>
> **(b) It is a supply shift traced along a stable demand curve.**
>
> **The observation "prices rose and quantity rose" looks like an upward-sloping demand curve** and is not. If supply shifts left while demand is stable, price rises and quantity falls. If *demand* shifts right while supply is stable, **both price and quantity rise** — which is what was observed.
>
> **The general point is important well beyond this chapter: what you observe is a sequence of equilibria, not a curve.** Each data point is an intersection. **Recovering the underlying curves from observed price–quantity pairs is a genuinely hard problem — it is the identification problem, and it is what [[Econometrics/contents/00-Index|Econometrics]] exists to solve.** A regression of quantity on price estimates neither curve unless something is assumed about which one is shifting.
>
> **(c) One of price or quantity becomes ambiguous.**
>
> | | supply ↑ | supply ↓ |
> |---|---|---|
> | **demand ↑** | $Q$ **rises**, $P$ **ambiguous** | $P$ **rises**, $Q$ **ambiguous** |
> | **demand ↓** | $P$ **falls**, $Q$ **ambiguous** | $Q$ **falls**, $P$ **ambiguous** |
>
> **The ambiguous variable depends on the *relative magnitudes* of the two shifts**, which the diagram does not contain.
>
> **"It is indeterminate" is the correct answer, not a failure to analyse.** Resolving it requires quantitative information the qualitative model does not have — **which is precisely the gap elasticity fills, and the reason the rest of this chapter exists.**

**2. (Hard — elasticity.)** (a) Why is the naive calculation ambiguous, and what does the midpoint method do? (b) Why does it work? (c) Why does a straight line have varying elasticity? (d) Where is total revenue maximised, and why?

> [!example]- Solution
> **(a) Because the denominator is the *starting* level, so the answer depends on which end you start from.**
>
> *(Verified on Mankiw's example — A: $P=\$4, Q=120$; B: $P=\$6, Q=80$:)*
>
> | | elasticity |
> |---|---|
> | A → B | **0.6667** |
> | B → A | **1.5000** |
>
> **A 125% disagreement about the same two points.** Going up, the \$2 rise is 50% of \$4; going down, it is 33% of \$6. **Same interval, different base.**
>
> **The midpoint method divides by the average of the two levels instead** *(computed: midpoint \$5 and 100 units, giving 40% and −40%, so **$e = 1.0000$ in both directions**)*.
>
> **(b) Because all three are approximations to the same derivative, and the midpoint one is centred.**
>
> *(Computed: shrinking the interval, the naive-forward and naive-backward measures converge on the midpoint value — the spread falls from **0.83333** at ±1 to **0.00080** at ±0.001 — and the midpoint value is exactly the point elasticity **1.00000** at every width.)*
>
> $$e=\left|\frac{dQ}{dP}\right|\frac{P}{Q}$$
>
> **So the midpoint method is not a separate concept or an arbitrary convention.** It is the **arc elasticity centred on the interval**, which is why it is exact at the centre and direction-free.
>
> **The naive versions are wrong by an amount proportional to the interval width** — negligible for small changes, large for the kind of discrete jumps a textbook table contains. **Mankiw never writes the derivative, which makes the formula look like a trick.** *(Addition.)*
>
> **(c) Because $e$ is the slope times $P/Q$, and $P/Q$ is not constant.**
>
> *(Computed on $Q = 14-2P$: the slope is $-2$ at every point, while elasticity runs from **0.0769** to **13.0000**.)*
>
> $$e=\underbrace{\left|\frac{dQ}{dP}\right|}_{\text{constant}=2}\times\underbrace{\frac{P}{Q}}_{0\to\infty}$$
>
> **At the bottom of the curve $P$ is small and $Q$ large, so $e\to0$; at the top $Q\to0$ and $e\to\infty$.**
>
> **So "flat means elastic" is a heuristic for *comparing curves at a point*, not a description of a single curve.** Slope has units and elasticity does not — **they are different objects and the confusion between them is the most common error in this chapter.**
>
> **(d) Exactly where $e=1$, and one derivative shows why.**
>
> *(Computed: on the grid, revenue ties at \$24 for $P=3$ and $P=4$ — **the tie itself signals the peak lies between**. Solving exactly: $TR = 14P-2P^2$, $dTR/dP = 14-4P = 0$, so $P^*=\$3.50$, $Q^*=7$, $TR^*=\$24.50$ — above both grid values — and $e = 2\times3.5/7 = \mathbf{1.0000}$.)*
>
> $$\frac{dTR}{dP}=Q+P\frac{dQ}{dP}=Q\left[1+\frac{P}{Q}\frac{dQ}{dP}\right]=Q\,[1-e]$$
>
> **Zero at $e=1$; positive when inelastic (raise the price); negative when elastic (cut it).**
>
> **So the three-way rule in §4 is the sign of a single derivative.** Elasticity is not three separate cases — it is one term whose value flips a sign.
>
> **This is the most useful thing in the chapter for practical work**, because it converts a qualitative rule into an optimisation: **if you know the elasticity you know which way to move the price, and you stop when $e=1$.** *(A monopolist therefore never operates on the inelastic part of its demand curve — [[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]].)*

**3. (Application.)** (a) Why does a better harvest hurt farmers? (b) When would it not? (c) What are the two wider lessons?

> [!example]- Solution
> **(a) Because food demand is inelastic, so the price falls proportionately more than the quantity rises.**
>
> *(Computed — a 50% productivity gain against $Q_d = 100-5P$, elasticity **0.50** at the old equilibrium: the harvest rises **+12.5%** and farm revenue falls **−15.6%**.)*
>
> **The mechanism is §5's, applied to a supply shift.** More output means a lower price; **whether that raises or lowers revenue depends entirely on whether $e$ exceeds 1.** Food has few substitutes and is a necessity, so demand is inelastic and revenue falls.
>
> **(b) If demand were elastic — and then the identical innovation helps.**
>
> *(Computed across three demand curves with the same supply shift:)*
>
> | elasticity | revenue change |
> |---|---|
> | **0.50** (inelastic) | **−15.6%** |
> | 1.00 (unit) | −4.0% |
> | **4.00** (elastic) | **+24.0%** |
>
> **Nothing about the technology, the farmers or the crop changed. Only the demand elasticity.** *(The unit-elastic case still falls slightly because revenue is *maximised* at $e=1$, so moving away from it in either direction reduces revenue.)*
>
> **(c) A collective-action problem, and a theory of structural change.**
>
> **1. Individually rational, collectively self-defeating.** It can be collectively rational for farmers to restrict output — and governments have paid them not to plant. **But no individual farmer wants to**, because one farm's output does not move the market price: each captures the full benefit of growing more while the price fall is borne by everybody.
>
> **That is exactly [[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]]'s prisoners' dilemma**, and it explains why the outcome needs a *policy* — the market cannot reach it, and this is also why cartels are unstable.
>
> **2. Technological progress in an inelastic sector shrinks that sector.** **US farm employment fell from roughly 40% of the workforce to under 2%, and it fell *because* farming improved enormously.** Output per worker rose far faster than demand, so fewer workers were needed.
>
> **So "this industry is declining" and "this industry is improving fast" are not contradictory — for a good with inelastic demand they are the same statement.** *(And the same logic applies wherever productivity outruns demand: manufacturing employment has followed the identical path for the identical reason, which is worth remembering before attributing it entirely to trade.)*

## 📝 Summary

- **A competitive market has price-taking buyers and sellers.** Demand slopes down, supply slopes up, and equilibrium is where $Q_d = Q_s$; surpluses and shortages both push toward it.
- **⚠️ A change in the good's own price is a movement *along* the curve; anything else *shifts* it.** The test is whether the variable appears on an axis. **"Change in demand" ≠ "change in quantity demanded."**
- **The "upward-sloping demand" paradox is a supply shift along a stable demand curve.** More generally, **observed price–quantity pairs are equilibria, not a curve** — which is [[Econometrics/contents/00-Index|econometrics]]' identification problem.
- **When both curves shift, one of price or quantity is genuinely ambiguous.** "Indeterminate" is the correct answer; resolving it needs elasticity.
- **$e = \%\Delta Q / \%\Delta P$, and it is unit-free** — which is why it, not slope, measures responsiveness.
- **⚠️ The naive calculation is direction-dependent** *(verified: **0.6667** vs **1.5000** on the same two points — a 125% disagreement)*. **The midpoint method divides by the average and gives 1.0000 both ways** ✓.
- **⚠️ And it works because all three measures approximate one derivative** *(computed: the naive spread falls 0.83333 → 0.00080 as the interval shrinks, converging on the point elasticity $|dQ/dP|(P/Q) = 1.00000$)*. **The midpoint version is the arc elasticity centred on the interval.**
- **Total revenue rules verified**: inelastic **\$400 → \$450**, elastic **\$400 → \$350** ✓.
- **⚠️ A straight-line demand curve has constant slope and elasticity running 0.0769 → 13.0000** *(computed)*. $e = |dQ/dP|\cdot P/Q$ holds the first factor fixed while the second sweeps $0\to\infty$. **Slope and elasticity are different objects.**
- **⚠️ Total revenue is maximised exactly where $e = 1$** *(computed: $P^* = \$3.50$, $Q^* = 7$, $TR^* = \$24.50$, $e = 1.0000$; the grid tie at \$24 was the clue the peak lay between)*.
- **And one derivative explains the whole rule: $dTR/dP = Q[1-e]$** — zero at $e=1$, positive when inelastic, negative when elastic. **The three-way rule is the sign of one derivative.**
- **Elasticity rises with substitutes, luxury status, narrow market definition, and time.** **The time-horizon point is why short-run and long-run analysis differ**, and why [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]]'s aggregate supply is flat short-run and vertical long-run.
- **⚠️ Good news for farming is bad news for farmers** *(computed: the same 50% productivity gain gives **−15.6%**, **−4.0%** or **+24.0%** revenue at elasticities of 0.50, 1.00 and 4.00)*. **Only the elasticity changed.**
- **It is collectively rational for farmers to restrict output and individually rational not to** — [[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]]'s prisoners' dilemma, and why the outcome requires policy.
- **⚠️ Technological progress in an inelastic sector shrinks that sector** — US farm employment fell from ~40% to under 2% *because* farming improved. **"Declining" and "improving fast" are the same statement for inelastic goods.**

## ⚠️ Important Notes

1. **⚠️ Price moves you along the curve; everything else shifts it.** Check whether the variable is on an axis.
2. **"Change in demand" and "change in quantity demanded" are different events.** The vocabulary is load-bearing.
3. **Observed data are equilibria, not curves.** Regressing $Q$ on $P$ identifies neither without further assumptions.
4. **When both curves shift, say which variable is ambiguous** rather than guessing.
5. **⚠️ Always use the midpoint method for discrete changes.** The naive one disagrees with itself by 125% here.
6. **⚠️ The midpoint method is the centred approximation to $e = |dQ/dP|(P/Q)$** — not an arbitrary convention.
7. **Elasticity is unit-free; slope is not.** Never compare slopes across goods.
8. **⚠️ Slope constant does not mean elasticity constant.** On a line, $e$ runs from 0 to $\infty$.
9. **"Flat means elastic" compares curves *at a point*** — it does not describe one curve.
10. **⚠️ $dTR/dP = Q[1-e]$.** Inelastic → raise the price; elastic → cut it; $e=1$ → you are at the peak.
11. **Revenue is maximised at unit elasticity** — so no seller with market power operates on the inelastic portion ([[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]]).
12. **Narrow markets are more elastic than broad ones.** "Food" and "vanilla ice cream" behave completely differently.
13. **⚠️ Elasticity rises with the time horizon** — the single most common reason short-run and long-run results diverge.
14. **⚠️ For an inelastic good, a supply increase lowers total revenue.** Better harvests can impoverish farmers.
15. **Individually rational ≠ collectively rational.** The gap is why some outcomes need policy.
16. **A tie in a discrete table often signals an interior optimum** — solve the continuous problem rather than picking a grid point.

> [!warning] Gaps in the source material
> **Mankiw's prose extracts cleanly and the outline is precise** *(Macro 2017, PDF pp. 96–141 for chs. 4–5)*.
>
> **⚠️ THE OPERATOR CIPHER hits this chapter harder than any other so far**, because it is the chapter with the most formulas. The midpoint formula extracts as
>
> ```
> price elasticity of demand 5 (Q2 2 Q1) / [(Q2 1 Q1) / 2]
> ```
>
> — **six digits with four different meanings** (subscript, minus, subscript, plus, subscript, literal 2). **Nothing here was transcribed**: every formula was reconstructed from the prose and verified against the book's own worked numbers, and **every one of those checks passed** (elasticity 2; the naive 0.66/1.5 pair; the midpoint 40%/40% and $e=1$; both total-revenue panels). **See [[00-Index]] for the cipher table.**
>
> **⚠️ Every figure is lost, and this chapter is built on them.** **Figure 3 (total revenue under elastic and inelastic demand) and Figure 4 (the linear demand curve with its elasticity schedule) are the chapter's core exposition and both are images.** What survives is the caption plus a scatter of axis labels and callout fragments — *"1. When the demand curve is inelastic . . ."* — which **look like data and are not.**
>
> **This is why §§4–5 recompute the schedules from the stated relationships** (a \$1 price rise costing 2 units) rather than reading them off the figure. **The reconstruction reproduces every number Mankiw states in prose**, which is what makes it verified rather than assumed.
>
> **No erratum.** Every figure the prose states reproduces exactly.
>
> **Additions beyond the source.**
>
> - **⚠️ §3b is mine and it is what makes the midpoint method make sense.** Mankiw introduces it as a fix for an "annoying problem" and never says what it approximates. **Shrinking the interval and showing all three measures converge on $|dQ/dP|(P/Q)$ establishes that it is the centred arc elasticity** — not a convention.
> - **⚠️ §5's derivation that $dTR/dP = Q[1-e]$ is the chapter's main addition.** **Mankiw prints a table showing revenue peaking at unit elasticity and never explains it.** One derivative turns his three-way rule into the sign of a single expression. *(He is deliberately calculus-free.)*
> - **§5's exact solution of the revenue maximum** ($P^*=3.50$, $TR^*=\$24.50$) is mine — **the book's integer table ties at \$24 and cannot locate the peak**, and the tie is itself evidence the maximum is interior.
> - **§7's three-elasticity comparison is mine.** Mankiw makes the farming argument qualitatively with one case; **computing it at elasticities of 0.50, 1.00 and 4.00 shows the sign of the revenue change is decided entirely by the elasticity**, which is the actual content of the claim.
> - **The identification-problem note in Exercise 1(b)** — that observed price–quantity pairs are equilibria rather than a curve, and that recovering the curves is what [[Econometrics/contents/00-Index|econometrics]] is for — is my cross-subject link.
> - **The observation that manufacturing employment has followed agriculture's path for the same reason** is an addition, and a deliberate caution against attributing it solely to trade.
> - **The forward link from §6's time-horizon point to [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]]'s aggregate supply curve** is mine.
>
> **Deliberately compressed.** **Mankiw's demand and supply schedules for individual buyers and sellers, and their horizontal summation to market curves**, are stated rather than tabulated — the arithmetic is addition and the figures are lost anyway. **The extended lists of shift factors** are compressed to the categories plus the axis test, which is the part that generalises. **The three case studies in ch. 4** (cigarette taxes, and two on shifting equilibria) are represented by the analytical content; the surplus machinery needed to evaluate the cigarette tax properly belongs to [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]. **Income and cross-price elasticity** are noted only in passing here; **income effects are treated properly in [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]]** with the indifference-curve apparatus that makes them meaningful. **Mankiw's applications on drug interdiction and OPEC** are omitted as further instances of §7's mechanism.

**Previous:** [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage]] · **Next:** [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade]]
