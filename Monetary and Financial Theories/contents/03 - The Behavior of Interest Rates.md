---
subject: Monetary and Financial Theories
chapter: 3
tags: [ds, economics, interest-rates, portfolio-choice, bond-market, liquidity-preference, fisher-effect, monetary-policy]
source: "Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition, ch. 5"
---

# The Behavior of Interest Rates

**[[02 - The Meaning of Interest Rates|Ch. 02]] said what an interest rate *is*. This one says what makes it move** — through two frameworks that are the same framework, and one policy conclusion that reverses the intuition everybody starts with.

**Four results.**

**§2 and §5 — the figures are lost, and it does not matter here.** **Mishkin's prose names every data point of Figure 1 and Figure 8**, so *(recovered and verified: $B^d=2000-2P$, $B^s=2P-1400$, $P^*=\$850$, $i^*=17.65\%$; and $M^d=600-20i$, $M^s=300$, $i^*=15\%$)* **both models are rebuilt algebraically — which lets every experiment Mishkin performs by shifting a curve on a picture be performed numerically instead, with the exact tipping condition attached.**

**§4 — the business-cycle prediction is genuinely ambiguous, and Mishkin says so.** *(Computed: $P^*=850+(a-b)/4$ — **the rate falls iff the demand shift exceeds the supply shift, and there is no parameter-free answer.**)* **He draws the figure the way he does "because this is the outcome we actually see in the data"** — **the sign comes from Figure 7, not from the model.** *This discharges the standing obligation carried from [[Macroeconomics & Microeconomics/contents/07 - Factor Markets and the Theory of Consumer Choice|Macro/Micro ch. 07]]: when two effects oppose, say so.*

**§7 — the chapter's biggest result: faster money growth probably *raises* interest rates.** **Only the liquidity effect lowers them; the income, price-level and expected-inflation effects all push the other way.** ⇒ ***"low interest rates" and "easy money" are not the same thing and over any horizon longer than months may be opposites.***

## 📘 Main Knowledge

### 1. The theory of portfolio choice

**Four determinants of how much of an asset you hold:**

| variable | effect on quantity demanded |
|---|---|
| **wealth** | ↑ |
| **expected return** *relative to alternatives* | ↑ |
| **risk** *relative to alternatives* | **↓** |
| **liquidity** *relative to alternatives* | ↑ |

> [!warning] ⚠️ "Relative to alternatives" is doing all the work
> **None of the last three is a property of the asset alone.** **An asset can become less attractive without changing in any way, because something else changed.** *(Mishkin's own example: abolishing fixed-rate stock commissions in 1975 raised the liquidity of **stocks**, and the demand for **bonds** fell.)*

> [!note] Why the list has four entries and not one
> *(Mishkin's own figures, verified: an ExxonMobil bond returning 15% half the time and 5% the other half has $E[R]=0.5(15)+0.5(5)=\mathbf{10\%}$.)*
>
> **Fly-by-Night Airlines: 15%/5%, so $E[R]=10\%$ and risky. Feet-on-the-Ground Bus: 10% for certain.** **Identical expected returns, and a risk-averse person strictly prefers the second.** **⇒ expected return alone does not rank assets** — which is why risk enters as a separate argument, and why [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]]'s diversification result has economic content.

> [!warning] ⚠️ Mishkin's footnote 1: the asset-pricing appendix is not in the book
> Standard deviations, **diversification**, systematic risk, **CAPM and APT** are all sent to the publisher's website. **This is the second off-book appendix in three chapters** *(the first was duration — [[02 - The Meaning of Interest Rates|ch. 02]] §6)*. **The vault already holds this machinery** — $\sigma/\sqrt{n}$ and $\sigma\sqrt{(1+\rho)/2}$ in [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]] and [[Commercial Banking/contents/02 - Organization, Structure and Market Entry|CB ch. 02]] — **so it is cross-linked, not re-derived.**

### 2. ⚠️ The bond market — Figure 1 recovered from the prose

> [!note] The figure is lost; the model is not
> **Mishkin's text names every point** — A–E on the demand curve, F–I plus C on the supply curve, with prices and quantities. **So the diagram is fully reconstructible**, and this is worth far more than the picture.

*(Verified — one-year discount bonds, $F=\$1{,}000$, so $i=(1000-P)/P$:)*

| price $P$ | interest rate | $B^d$ (\$bn) | $B^s$ (\$bn) | point |
|---|---|---|---|---|
| \$950 | **5.2632%** *(book 5.3)* | 100 | 500 | A / I |
| \$900 | **11.1111%** *(11.1)* | 200 | 400 | B / H |
| **\$850** | **17.6471%** *(17.6)* | **300** | **300** | **C = equilibrium** |
| \$800 | **25.0000%** *(25.0)* | 400 | 200 | D / G |
| \$750 | **33.3333%** *(33.3)* | 500 | 100 | E / F |

$$B^d=2000-2P\qquad B^s=2P-1400\qquad\Rightarrow\qquad P^*=\$850,\ Q^*=\$300\text{bn},\ i^*=17.65\%$$

*(Both formulas reproduce all five of Mishkin's points exactly; all five interest rates match the prose.)*

> [!note] Disequilibrium, checked
> **At \$950: $B^d=100$, $B^s=500$ ⇒ excess supply of \$400bn ⇒ price falls.** **At \$750: $B^d=500$, $B^s=100$ ⇒ excess demand of \$400bn ⇒ price rises.** **⚠️ And because $i$ and $P$ move oppositely ([[02 - The Meaning of Interest Rates|ch. 02]] §3), the same arrows say the interest rate converges to 17.65% from both sides.**

> [!warning] ⚠️ Supply and demand here are STOCKS, not flows
> **The asset-market approach prices assets from the *amount outstanding at a point in time*, not the flow of new issues.** **Mishkin's reason is blunt: conducting the analysis in flows "is very tricky, especially when we encounter inflation".** *(This is exactly why his footnote 3 sends the **loanable-funds** framework — which is the flow version — to yet another off-book appendix. **[[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]] owns loanable funds**, and Mishkin's own choice confirms the boundary recorded in [[00-Index]].)*

**Movement *along* a curve = a change in the bond's own price. A *shift* = a change in anything else.** **Confusing the two is the single most common error in this chapter.**

**Shift factors — demand** *(from the four determinants)*: **wealth ↑ ⇒ right**; **expected future interest rates ↑ ⇒ left** *(because long bonds would take a capital loss — [[02 - The Meaning of Interest Rates|ch. 02]]'s Table 2 is the mechanism)*; **expected inflation ↑ ⇒ left**; **riskiness of bonds ↑ ⇒ left**; **liquidity of bonds ↑ ⇒ right.**

**Shift factors — supply**: **expected profitability of investment ↑ ⇒ right**; **expected inflation ↑ ⇒ right**; **government deficit ↑ ⇒ right.**

### 3. ⚠️ The Fisher effect — an unambiguous prediction

**Expected inflation rises 5% → 10%. Two things happen and they push the same way.**

| | why | shift |
|---|---|---|
| **demand** | real assets now offer higher *nominal* capital gains, so bonds' relative expected return falls | $B^d$ **left** |
| **supply** | the real cost of borrowing $i-\pi^e$ falls, so firms issue more | $B^s$ **right** |

$$(2000-a)-2P=(2P-1400)+b\qquad\Longrightarrow\qquad P^*=850-\frac{a+b}{4}$$

*(Computed:)*

| $a$ (demand left) | $b$ (supply right) | $P^*$ | $i^*$ | change |
|---|---|---|---|---|
| 0 | 0 | \$850.00 | 17.6471% | — |
| 40 | 0 | \$840.00 | 19.0476% | **+1.40 pts** |
| 0 | 40 | \$840.00 | 19.0476% | +1.40 pts |
| 40 | 40 | \$830.00 | 20.4819% | +2.83 pts |
| 200 | 200 | \$750.00 | 33.3333% | **+15.69 pts** |

> [!warning] ⚠️ Why this is a theorem and §4's prediction is not
> **$P^*=850-(a+b)/4$ is strictly decreasing in *both* $a$ and $b$.** **No choice of parameters reverses the sign.** **The Fisher effect is a *result* of the model; the business-cycle prediction in §4 is not.**
>
> **But the *quantity* is left open** — *(computed: the change in $Q^*$ is $(b-a)/2$, so $a=100,b=40$ gives $Q^*=270$; $a=40,b=100$ gives $330$; $a=b=100$ gives exactly $300$)*. **⚠️ The model pins the price and not the quantity — and it is worth noticing that a model can determine one margin and leave another genuinely undetermined.**

**Mishkin's evidence is Figure 5** *(lost)*: **the three-month Treasury bill rate has generally moved with expected inflation, 1953–2017.** ⇒ **many economists conclude inflation must be kept low if nominal rates are to be low** — which is §7's conclusion arriving early.

### 4. ⚠️ Business cycle expansion — genuinely ambiguous

**Expansion does two things and they push *opposite* ways.**

| | | shift | effect on $i$ |
|---|---|---|---|
| **demand** | wealth rises | $B^d$ right | raises $P$ ⇒ **lowers $i$** |
| **supply** | profitable investments abound | $B^s$ right | lowers $P$ ⇒ **raises $i$** |

$$(2000+a)-2P=(2P-1400)+b\qquad\Longrightarrow\qquad P^*=850+\frac{a-b}{4}$$

| $a$ (demand) | $b$ (supply) | $P^*$ | $i^*$ | verdict |
|---|---|---|---|---|
| 400 | 100 | \$925.00 | 8.1081% | **$i$ falls** |
| 200 | 100 | \$875.00 | 14.2857% | $i$ falls |
| **150** | **150** | **\$850.00** | **17.6471%** | **$i$ exactly unchanged** |
| 100 | 200 | \$825.00 | 21.2121% | $i$ rises |
| 100 | 400 | \$775.00 | 29.0323% | **$i$ rises** |

> [!warning] ⚠️ The model does not determine the sign, and Mishkin says so
> **$i$ falls iff $a>b$, rises iff $a<b$, and at $a=b$ the rate is exactly unchanged while the quantity of bonds rises.** **There is no parameter-free answer.**
>
> **And Mishkin is admirably explicit:** the figure *"has been drawn so that the shift in the supply curve is greater than the shift in the demand curve… **The reason the figure has been drawn such that a business cycle expansion and a rise in income lead to a higher interest rate is that this is the outcome we actually see in the data.**"*
>
> **⚠️ So the sign comes from Figure 7, not from the model** — and that is the correct relationship between a theory and its evidence. **The model narrows the possibilities to two and names the condition; the data picks.**
>
> **This is the standing obligation from [[Macroeconomics & Microeconomics/contents/07 - Factor Markets and the Theory of Consumer Choice|Macro/Micro ch. 07]] discharged in a new setting: *when two effects oppose, say so*. A model that identifies two opposing forces has done its job; demanding a sign from it anyway is how confident wrong answers get made.** *(Compare [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]], whose loanable-funds model **assumed** an upward-sloping saving curve — same structure, same warning.)*

### 5. ⚠️ Liquidity preference — Figure 8 recovered, and the two frameworks are one

**Keynes: two assets only — money (zero return) and bonds (return $i$).** **The opportunity cost of holding money *is* the interest rate**, so $M^d$ slopes down.

*(Recovered from the prose and verified:)*

| $i$ | $M^d$ (\$bn) | point |
|---|---|---|
| 25% | 100 | A |
| 20% | 200 | B |
| **15%** | **300** | **C = equilibrium** |
| 10% | 400 | D |
| 5% | 500 | E |

$$M^d=600-20i\qquad M^s=300\ \text{(vertical)}\qquad\Rightarrow\qquad i^*=\mathbf{15\%}\ ✓$$

> [!note] Disequilibrium — and note the mechanism runs through bonds
> **At $i=25\%$: $M^d=100$ against $M^s=300$ ⇒ people hold \$200bn more money than they want ⇒ they *buy bonds* ⇒ bond prices rise ⇒ $i$ falls.** **At $i=5\%$: excess demand for money of \$200bn ⇒ they *sell bonds* ⇒ $i$ rises.** **⚠️ The money market is cleared by trading bonds** — which is the first hint that the two frameworks are one.

> [!warning] ⚠️ The two frameworks are the same framework
> $$B^s+M^s=B^d+M^d\quad\Longrightarrow\quad B^s-B^d=M^d-M^s$$
> **So $M^d=M^s$ if and only if $B^d=B^s$.** *(Verified numerically: at total wealth 900, every combination gives $B^s-B^d$ exactly equal to $M^d-M^s$.)* **The two markets cannot disagree — they are one market described twice.**
>
> **So why keep both? Because they make different things easy.**
>
> | framework | natural for | blind to |
> |---|---|---|
> | **bond supply/demand** | **expected inflation** *(it contains real assets)* | — |
> | **liquidity preference** | **income, the price level, the money supply** | **real assets — it has only two** |
>
> **⚠️ And notice what happened between §4 and here.** **The bond framework gave an *ambiguous* answer for a business-cycle expansion; liquidity preference gives an *unambiguous* one** *(income ↑ ⇒ $M^d$ right ⇒ $i$ ↑)*.
>
> **Same event, same economy, different definiteness — because liquidity preference holds the money supply fixed and so suppresses the very channel that made the first ambiguous.** **⚠️ A sharper answer from a narrower model is not a better answer.** *(This is worth carrying: definiteness is often a property of what a model left out.)*

**Comparative statics** *(computed, $i^*=(600+\text{shift}-M^s)/20$):*

| experiment | $M^d$ shift | $M^s$ | $i^*$ | change |
|---|---|---|---|---|
| baseline | 0 | 300 | 15.0% | — |
| **income rises** | +60 | 300 | 18.0% | **+3.0** |
| **price level rises** | +30 | 300 | 16.5% | +1.5 |
| **money supply +\$60bn** | 0 | 360 | **12.0%** | **−3.0** |
| money supply −\$60bn | 0 | 240 | 18.0% | +3.0 |
| **income up AND money up** | +60 | 360 | **15.0%** | **0.0** |

**All three of Mishkin's Table 4 rows confirmed.** **⚠️ And the last row is §7 arriving: an increase in the money supply lowers $i$ *only if nothing else moves*.**

### 6. ⚠️ Money and interest rates — Friedman's four effects

**Does faster money growth lower interest rates?** **Friedman accepted the liquidity-preference analysis and called its result the *liquidity effect* — then pointed out it is one of four.**

| effect | direction on $i$ | speed | persistence |
|---|---|---|---|
| **liquidity** | **↓** | **immediate** | — |
| **income** | ↑ | slow | |
| **price-level** | ↑ | slow | **permanent** — remains after prices stop rising |
| **expected-inflation** | ↑ | **slow or fast** | **only while growth continues** |

> [!note] The price-level and expected-inflation effects are genuinely different
> **A *one-time* rise in $M$ raises the price level to a permanently higher level.** **The price-level effect therefore reaches its maximum at the end of the adjustment and stays.** **But once prices *stop* rising, inflation and expected inflation return to zero, so the expected-inflation effect goes to zero.**
>
> **⚠️ Only a higher *rate of growth* sustains the expected-inflation effect.** *(This distinction between a level and a growth rate is the same one that separates [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]]'s one-off price jump from ongoing inflation.)*

**Three possible outcomes** *(Mishkin's Figure 11 — a schematic with no data, lost; the three orderings stated exactly, illustrated with paths I constructed to realise them:)*

| case | condition | trough | settles | net |
|---|---|---|---|---|
| **(a)** | liquidity effect **larger** than the others | 7.21% at $t=2$ | 7.97% | **−2.03 pts** |
| **(b)** | liquidity **smaller**, expectations adjust **slowly** | 9.48% at $t=1$ | 11.89% | **+1.89 pts** |
| **(c)** | liquidity **smaller**, expectations adjust **fast** | **no trough** | 12.00% | **+2.00 pts** |

- **(a) rates fall and stay below** — raising money growth works.
- **(b) rates fall *first*, then rise *above* the start** — works in the short run, backfires in the long run.
- **(c) rates rise immediately** — **the dip never happens**, because the expected-inflation effect overpowers liquidity from the outset.

> [!warning] ⚠️ In case (c) the policy is exactly backwards
> **To lower interest rates you must *lower* money growth.** **Mishkin states it in an exclamation mark, and it is the chapter's biggest result.**
>
> **The evidence** *(Figure 12, lost)*: **money growth and interest rates rose together through the 1960s–70s and fell together from the early 1980s to the early 1990s; since 1995, with stable inflation, no clear relationship.** ⇒ **panel (a) looks doubtful and the expected-inflation effect appears dominant** — **but the data do not separate (b) from (c)**, which turns on how fast expectations adjust.
>
> **⚠️ ⇒ "low interest rates" and "easy money" are not the same thing, and over any horizon longer than months they may be opposites.** *(This is why [[09 - Tools and Conduct of Monetary Policy|ch. 09]] cannot use the interest-rate level as a straightforward measure of the policy stance, and it is Friedman's most durable contribution to central banking.)*

### 7. Why rates are so low now — and the fallacy of reading the level

**Post-crisis Europe, Japan and the US: rates near zero, sometimes negative.** **Mishkin's account, run through the recovered model:**

| cause | mechanism | shifts |
|---|---|---|
| **very low / negative inflation** | real assets less attractive ⇒ bonds better; **and** the real cost of borrowing *rises* | $B^d$ **right**, $B^s$ **left** |
| **secular stagnation** *(Summers)* | few profitable investments ⇒ firms issue fewer bonds | $B^s$ **left** |

$$P^*=850+\frac{a+b}{4}\qquad\text{— unambiguous, both shifts raise }P\text{ and lower }i$$

*(Computed: $a=b=40$ gives $P^*=\$870$ and $i^*=14.94\%$, down 2.71 points; $a=b=100$ gives $\$900$ and $11.11\%$, down 6.54.)*

> [!warning] ⚠️ Low interest rates are not automatically good news
> **They are cheap borrowing — and they are also a *symptom*, of low inflation and a dearth of profitable investment.** **The same number means opposite things depending on which curve moved.**
>
> **⚠️ Which is [[01 - The Financial System and What Money Is|ch. 01]]'s and [[02 - The Meaning of Interest Rates|ch. 02]]'s lesson a third time.** *"Which M?"*, *"which interest rate?"*, and now ***"which curve moved?"*** — **a number never carries its own explanation.**

## ✏️ Exercises

**1. (Portfolio choice.)** (a) State the four determinants and compute Mishkin's expected returns. (b) Why does the list have four entries? (c) What phrase does the real work?

> [!example]- Solution
> **(a) Wealth ↑, expected return ↑, risk ↓, liquidity ↑.**
>
> *(Verified: an ExxonMobil bond returning 15% half the time and 5% the other half has $E[R]=0.5(15)+0.5(5)=\mathbf{10\%}$, matching the book.)*
>
> **(b) Because expected return alone does not rank assets.**
>
> **Fly-by-Night Airlines returns 15% or 5% with equal probability ⇒ $E[R]=10\%$. Feet-on-the-Ground Bus returns 10% for certain ⇒ $E[R]=10\%$.** **Identical expected returns, and a risk-averse person strictly prefers the certain one.**
>
> **So a complete ranking needs at least a second argument, and risk is it.** *(Liquidity is a third: an asset can dominate on both return and risk and still be undesirable if you cannot sell it — Mishkin's house-versus-Treasury-bill contrast.)*
>
> **⚠️ And this is exactly what makes [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]]'s diversification result economically interesting rather than merely arithmetical**: combining assets lowers $\sigma$ *without* lowering $E[R]$, which moves you strictly up the ranking. **A financial intermediary sells that improvement** ([[01 - The Financial System and What Money Is|ch. 01]] §3).
>
> **(c) "Relative to alternative assets."**
>
> **None of the last three determinants is a property of the asset alone.** **An asset can become less desirable without changing in any respect, because something else changed.**
>
> *(Mishkin's own case: abolishing fixed-rate stock commissions in 1975 raised the **liquidity of stocks**, and **the demand for bonds fell** — bonds were identical the day before and the day after.)*
>
> **⚠️ This is why every shift factor in §2 comes in pairs** — "riskiness of bonds ↑ ⇒ demand falls" and "riskiness of *other* assets ↑ ⇒ demand rises". **Forgetting the relative clause is how students get the direction backwards.**

**2. (The bond market.)** (a) Recover Mishkin's Figure 1 from the prose and solve for equilibrium. (b) Show the market converges. (c) Why are supply and demand described in *stocks*?

> [!example]- Solution
> **(a) $B^d=2000-2P$, $B^s=2P-1400$, $P^*=\$850$, $i^*=17.65\%$.**
>
> **The figure is lost, but the prose names every point.** *(Verified — the rates are $i=(1000-P)/P$ and all five match the book:)*
>
> | $P$ | $i$ | $B^d$ | $B^s$ |
> |---|---|---|---|
> | \$950 | 5.2632% | 100 | 500 |
> | \$900 | 11.1111% | 200 | 400 |
> | **\$850** | **17.6471%** | **300** | **300** |
> | \$800 | 25.0000% | 400 | 200 |
> | \$750 | 33.3333% | 500 | 100 |
>
> **Both lines pass through all five of their points**, and $2000-2P=2P-1400$ gives $P^*=850$, $Q^*=300$, $i^*=17.65\%$ ✓.
>
> **(b) Excess supply above, excess demand below.**
>
> **At \$950: $B^d=100$, $B^s=500$ — borrowers want to sell \$400bn more than lenders want to buy ⇒ price falls.** **At \$750: excess demand of \$400bn ⇒ price rises.** **Only at \$850 is there no tendency to move.**
>
> **⚠️ And because $i$ and $P$ move oppositely, the same arrows describe the interest rate**: at $P=\$950$ the rate is 5.26%, *below* equilibrium, and the falling price *raises* it toward 17.65%. **A "too low" interest rate and a "too high" bond price are the same disequilibrium.**
>
> **(c) Because flows are treacherous, especially under inflation.**
>
> **The asset-market approach prices an asset from the *stock outstanding at a point in time*, not from the flow of new issues.** **Mishkin's justification is candid — "correctly conducting analyses in terms of flows is very tricky, especially when we encounter inflation" — and it is the dominant methodology among economists.**
>
> **⚠️ The flow version is the loanable-funds framework, and Mishkin sends it to an off-book appendix** *(footnote 3 — his **third** such appendix in this chapter alone, after asset pricing and the gold market)*. **[[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]] owns loanable funds**, so **Mishkin's own editorial choice confirms the boundary recorded in [[00-Index]]** — a pleasing case of the source agreeing with a decision made before it was read.

**3. (Hard — Fisher versus the business cycle.)** (a) Work the Fisher effect and show it is unambiguous. (b) Work a business-cycle expansion and show it is not. (c) What does the difference teach?

> [!example]- Solution
> **(a) Both shifts lower the bond price, so the rate must rise.**
>
> **Expected inflation 5% → 10%.** **Demand shifts left** *(real assets now offer higher nominal capital gains, so bonds' relative expected return falls)*. **Supply shifts right** *(the real cost of borrowing $i-\pi^e$ falls, so firms issue more)*.
>
> $$(2000-a)-2P=(2P-1400)+b\quad\Rightarrow\quad P^*=850-\frac{a+b}{4}$$
>
> | $a$ | $b$ | $P^*$ | $i^*$ | Δ$i$ |
> |---|---|---|---|---|
> | 40 | 40 | \$830 | 20.48% | +2.83 |
> | 200 | 200 | \$750 | 33.33% | **+15.69** |
>
> **$P^*$ is strictly decreasing in both $a$ and $b$, so no parameter choice reverses the sign.** **This is a theorem of the model.**
>
> *(But the **quantity** is undetermined: the change in $Q^*$ is $(b-a)/2$, so it rises, falls or stays put according to which shift is larger — **the model pins the price and leaves the quantity open**.)*
>
> **(b) The two shifts oppose, so the sign depends on their relative size.**
>
> **Expansion raises wealth ⇒ $B^d$ right ⇒ $P$ up ⇒ $i$ down.** **It also raises expected profitability ⇒ $B^s$ right ⇒ $P$ down ⇒ $i$ up.**
>
> $$P^*=850+\frac{a-b}{4}$$
>
> | $a$ | $b$ | $i^*$ | |
> |---|---|---|---|
> | 400 | 100 | 8.11% | **falls** |
> | **150** | **150** | **17.65%** | **exactly unchanged** |
> | 100 | 400 | 29.03% | **rises** |
>
> **$i$ falls iff $a>b$. At $a=b$ the rate is exactly unchanged while the quantity of bonds rises — so an expansion can raise borrowing without moving the rate at all.**
>
> **⚠️ Mishkin resolves it with data, not theory, and says so outright:** the figure *"has been drawn so that the shift in the supply curve is greater… because **this is the outcome we actually see in the data**"* — Figure 7 shows rates rising in expansions and falling in recessions.
>
> **(c) That the model's job is to narrow the possibilities and name the condition, not to supply a sign it does not have.**
>
> **The Fisher case shows what a model *can* deliver: a sign that holds for every admissible parameter.** **The business-cycle case shows the honest alternative: two possibilities, an explicit tipping condition ($a$ versus $b$), and evidence brought in from outside to choose.**
>
> **⚠️ The failure mode is the third option — drawing the picture one way and presenting the result as though the theory produced it.** *(This is the standing obligation carried from [[Macroeconomics & Microeconomics/contents/07 - Factor Markets and the Theory of Consumer Choice|Macro/Micro ch. 07]], where the wage effect on hours worked and the interest-rate effect on saving are both genuinely ambiguous, and [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|ch. 10]]'s loanable-funds model **assumed** an upward-sloping saving curve rather than deriving it.)*
>
> **A model identifying two opposing forces has done its job. Demanding a sign from it anyway is how confident wrong answers get made** — and **Mishkin here is a model of how to handle it.**

**4. (Hard — the two frameworks.)** (a) Recover Figure 8 and solve it. (b) Prove the two frameworks are equivalent. (c) Then why does liquidity preference give a *definite* answer where the bond market gave an ambiguous one?

> [!example]- Solution
> **(a) $M^d=600-20i$, $M^s=300$, $i^*=15\%$.**
>
> *(Recovered from the prose, verified on all five points: $i=25\Rightarrow M^d=100$; $20\Rightarrow200$; $15\Rightarrow300$; $10\Rightarrow400$; $5\Rightarrow500$.)* **$600-20i=300$ gives $i^*=15\%$** ✓.
>
> **Money demand slopes down because the opportunity cost of holding money *is* the interest rate** — money earns zero, bonds earn $i$, so a higher $i$ makes money more expensive to hold.
>
> **⚠️ And the adjustment mechanism runs through bonds.** At $i=25\%$ people hold \$200bn more money than they want, so **they buy bonds**, bidding prices up and $i$ down. **The money market is cleared by trading bonds** — which is the first sign that (b) must be true.
>
> **(b) They are one market described twice.**
>
> **Total wealth is held as money or bonds, so $B^s+M^s=B^d+M^d$, hence**
> $$B^s-B^d=M^d-M^s$$
> **⇒ $M^d=M^s$ if and only if $B^d=B^s$.** *(Verified numerically at total wealth 900: every combination gives $B^s-B^d$ exactly equal to $M^d-M^s$.)*
>
> **The two markets cannot disagree.** **An excess demand for money is an excess supply of bonds — the same fact.**
>
> **(c) Because liquidity preference has fewer assets in it, and the missing one carried the ambiguity.**
>
> **In the bond framework an expansion shifts *both* curves right and the sign is undetermined.** **In liquidity preference, income rises ⇒ $M^d$ shifts right ⇒ $i$ rises, full stop** *(computed: +60 shift ⇒ 15% → 18%)*.
>
> **The reason is that liquidity preference holds $M^s$ fixed by assumption, so the channel through which bond *supply* expanded has nowhere to appear.** **Keynes's framework has only two assets, so it is structurally blind to changes in the expected return on real assets.**
>
> **⚠️ So the definiteness is a property of what the model left out, not of the economy.** **A sharper answer from a narrower model is not a better answer** — and the honest reading is the bond framework's: *ambiguous, and here is the condition*.
>
> *(Which is why Mishkin keeps both and says which to use when: **the bond framework for expected inflation** — it contains real assets — **liquidity preference for income, the price level and the money supply.** **Neither is the "right" model; they are two instruments with different resolutions.**)*

**5. (Hard — money growth and interest rates.)** (a) Name the four effects and their speeds. (b) Distinguish the price-level from the expected-inflation effect. (c) Sketch the three outcomes and state the policy conclusion.

> [!example]- Solution
> **(a) One down, three up.**
>
> | effect | direction | speed |
> |---|---|---|
> | **liquidity** | **↓** | **immediate** |
> | **income** | ↑ | slow |
> | **price-level** | ↑ | slow |
> | **expected-inflation** | ↑ | **slow or fast — this is the crux** |
>
> **Friedman accepted the liquidity-preference result completely** and only denied that "everything else" stays equal. **More money raises income, raises the price level, and may raise expected inflation — and all three raise the interest rate.**
>
> **(b) One survives the end of inflation; the other does not.**
>
> **Suppose a *one-time* increase in $M$ raises prices to a permanently higher level over the coming year.**
>
> - **Price-level effect:** as $P$ rises, $M^d$ shifts right and $i$ rises. **When $P$ stops rising it stays high, so $M^d$ stays shifted and the effect persists.** **Maximum at the end of the adjustment.**
> - **Expected-inflation effect:** while $P$ is rising, people expect inflation and $i$ rises via Fisher. **But once $P$ stops rising, expected inflation returns to zero and the effect vanishes.** **Minimum (zero) at the end of the adjustment.**
>
> **⚠️ So the two effects are largest at opposite moments**, and **only a higher *rate of growth* — not a one-time increase — sustains the expected-inflation effect.** *(The level/growth-rate distinction is the same one separating a one-off price jump from ongoing inflation in [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]].)*
>
> **(c) Three orderings, and in the third the policy is backwards.**
>
> | case | condition | path | net |
> |---|---|---|---|
> | **(a)** | liquidity **larger** | falls to 7.21%, recovers to 7.97% | **−2.03 pts** |
> | **(b)** | liquidity smaller, expectations **slow** | dips to 9.48%, then climbs past the start | **+1.89 pts** |
> | **(c)** | liquidity smaller, expectations **fast** | **rises immediately — no dip at all** | **+2.00 pts** |
>
> *(The paths are my construction, chosen to realise Mishkin's three orderings — **they illustrate the logic and are not evidence.**)*
>
> **⚠️ In case (c) the conclusion is that to *lower* interest rates you must *lower* money growth.**
>
> **The evidence** *(Figure 12, lost)*: **money growth and rates rose together through the 1960s–70s and fell together in the 1980s–early 90s; since 1995, with stable inflation, no clear relationship.** ⇒ **panel (a) is doubtful and the expected-inflation effect looks dominant** — **but the data cannot separate (b) from (c)**, which turns entirely on the speed of expectations.
>
> **⚠️ The policy lesson is the chapter's largest: "low interest rates" and "easy money" are not the same thing, and over any horizon longer than months they may be opposites.**
>
> **And §7 supplies the mirror image.** Post-crisis rates near zero came from **low inflation** *(shifting $B^d$ right and $B^s$ left)* and **secular stagnation** *(shifting $B^s$ left)* — **both unambiguously raising bond prices and lowering rates**. **So low rates were a symptom of a weak economy, not a stimulus applied to one.**
>
> **⇒ the same number — a low interest rate — means opposite things depending on which curve moved**, which is [[01 - The Financial System and What Money Is|ch. 01]]'s and [[02 - The Meaning of Interest Rates|ch. 02]]'s lesson a third time. **This also foreshadows [[09 - Tools and Conduct of Monetary Policy|ch. 09]]: the interest-rate level is not a measure of the policy stance.**

## 📝 Summary

- **The theory of portfolio choice: wealth ↑, expected return ↑, risk ↓, liquidity ↑** — **each *relative to alternative assets*, which is the phrase doing all the work.**
- **⚠️ Expected return alone does not rank assets** *(Mishkin's two 10% stocks, one certain and one not)* — which is why risk enters separately.
- **⚠️ Figure 1 is lost but fully recoverable from the prose** *(verified: $B^d=2000-2P$, $B^s=2P-1400$, $P^*=\$850$, $Q^*=\$300$bn, $i^*=17.65\%$; all five of Mishkin's rates reproduce)*. **This converts every graphical experiment into a numerical one with an explicit tipping condition.**
- **Supply and demand are stocks, not flows** — the asset-market approach. **Mishkin sends loanable funds to an off-book appendix, confirming [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]]'s ownership of it.**
- **⚠️ The Fisher effect is unambiguous** *(computed: $P^*=850-(a+b)/4$, strictly decreasing in both, so no parameters reverse it)* — **but the quantity of bonds is left undetermined, changing by $(b-a)/2$.**
- **⚠️ A business-cycle expansion is genuinely ambiguous** *(computed: $P^*=850+(a-b)/4$; $i$ falls iff $a>b$, and at $a=b$ it is exactly unchanged)*. **Mishkin resolves it from Figure 7's data and says so — the sign comes from evidence, not from the model.**
- **⚠️ Figure 8 also recovered** *(verified: $M^d=600-20i$, $M^s=300$, $i^*=15\%$)* — **money demand slopes down because the opportunity cost of holding money *is* the interest rate.**
- **⚠️ The two frameworks are one:** $B^s+M^s=B^d+M^d\Rightarrow B^s-B^d=M^d-M^s$, **so the money market clears iff the bond market does.** They differ only in what they make easy.
- **⚠️ Liquidity preference gives a definite answer where the bond market did not — because it has fewer assets in it.** **A sharper answer from a narrower model is not a better answer.**
- **Liquidity-preference comparative statics all verify:** income ↑ ⇒ $i$ ↑; price level ↑ ⇒ $i$ ↑; **money supply ↑ ⇒ $i$ ↓.**
- **⚠️ Friedman's four effects: only the liquidity effect lowers $i$.** Income, price-level and expected-inflation all raise it.
- **The price-level effect persists after prices stop rising; the expected-inflation effect vanishes** — **they peak at opposite moments, and only a sustained higher *growth rate* keeps the second alive.**
- **⚠️ Three outcomes** — rates fall and stay down; **fall then overshoot upward**; or **rise immediately with no dip at all.** **The evidence makes the first doubtful and the expected-inflation effect dominant, but cannot separate the other two.**
- **⚠️ ⇒ "low interest rates" and "easy money" are not the same thing** — over any horizon longer than months they may be opposites, **so the interest-rate level is not a measure of the policy stance.**
- **⚠️ Today's near-zero rates come from low inflation and secular stagnation — both unambiguously rate-lowering — so they are a *symptom*, not a stimulus.** **The same number means opposite things depending on which curve moved:** *which M?*, *which interest rate?*, **now *which curve moved?***

## ⚠️ Important Notes

1. **Every determinant of asset demand is *relative*.** An asset can become undesirable without changing at all.
2. **⚠️ Movement *along* a curve vs a *shift*** — a change in the bond's own price moves you along; anything else shifts. **This is the most common error in the chapter.**
3. **Higher *expected future* interest rates shift bond demand LEFT** — because long bonds would take a capital loss ([[02 - The Meaning of Interest Rates|ch. 02]]'s Table 2 is the mechanism). Not to be confused with the current rate.
4. **Expected inflation shifts demand left AND supply right.** **Both raise the rate** — this is the only shift factor that hits both curves the same way.
5. **⚠️ The Fisher effect is a theorem; the business-cycle prediction is not.** Know which results are parameter-free.
6. **⚠️ When two effects oppose, say so** — and name the tipping condition. Then, if you must have a sign, get it from data and *say that you did*.
7. **A model can pin one margin and not another** — here, the price but not the quantity of bonds.
8. **⚠️ Money demand slopes down because of *opportunity cost*, not because money is unattractive.** Money's return is zero; the bond's is $i$.
9. **The money market is cleared by trading bonds.** An excess demand for money *is* an excess supply of bonds.
10. **⚠️ The two frameworks cannot disagree.** If they seem to, one has been misapplied.
11. **⚠️ Definiteness can come from omission.** Liquidity preference is sharper because it is blind to real assets.
12. **Use the bond framework for expected inflation; liquidity preference for income, prices and the money supply.**
13. **⚠️ Only the liquidity effect lowers rates.** Three of Friedman's four effects raise them.
14. **The price-level and expected-inflation effects are largest at opposite moments.** A one-time rise in $M$ leaves the first and kills the second.
15. **⚠️ Only a higher growth *rate* sustains the expected-inflation effect** — a level change does not.
16. **⚠️ Low rates may be a symptom, not a stimulus.** Ask which curve moved before calling them good news.
17. **The interest rate is not a measure of the monetary policy stance** — this is why [[09 - Tools and Conduct of Monetary Policy|ch. 09]] needs a different apparatus.
18. **⚠️ Three off-book appendices in one chapter** — asset pricing/CAPM, the gold market, and loanable funds. **Check the footnotes before assuming a topic is absent from the course.**

> [!warning] Gaps in the source material
> **⚠️ THE CHAPTER IS TAUGHT ALMOST ENTIRELY THROUGH SHIFTING CURVES, AND ALL TWELVE FIGURES ARE IMAGES AND ARE LOST.** **This was expected to be the worst chapter in the subject for extraction. It turned out not to be — for a specific and reusable reason.**
>
> **⚠️ MISHKIN'S PROSE NAMES EVERY DATA POINT OF FIGURE 1 AND FIGURE 8.** Points A–E and F–I with their prices and quantities; points A–E of the money-demand curve with their interest rates. **So both core models were reconstructed algebraically** *(verified: both lines pass through all five of their stated points, and all five interest rates and both equilibria reproduce the book)*. **Every comparative static Mishkin performs by shifting a curve on a picture has been performed numerically here instead** — which is **strictly more informative**, because it delivers the *magnitude* of each effect and the *exact condition* under which the ambiguous case tips.
>
> **⚠️ EXTRACTION RULE EXTENDED — worth carrying to every remaining chapter: before recording a figure as lost, check whether the prose names its points.** A textbook figure that is *explained* point by point is recoverable; one that is merely *referred to* is not. **Figures 2, 3, 4, 6, 9, 10 and 11 are the second kind and are genuinely lost — they are schematic shift diagrams with no numbers, and their content is the direction of a shift, which the prose states in words and this note reproduces.**
>
> **⚠️ FIGURE AXIS LABELS EXTRACT AS TEXT even though the graphic is lost — and their digits are NOT reliable.** Figure 1's label extracts as `(i 5 33.0%)` where **the prose says 33.3% and the truth is 33.3333%**; note the `5` standing for `=` in the same label. **Investigated and NOT filed as an erratum**: the prose is correct, and **rule 4 requires ruling out my own extraction first** — a mis-rendered glyph inside a graphic is exactly that. **Recorded as an extraction hazard: never take a number from a figure label.**
>
> **The empirical figures are the real loss.** **Figure 5** (expected inflation vs the T-bill rate, 1953–2017), **Figure 7** (the business cycle and interest rates, 1951–2017, with recession shading), and **Figure 12** (M2 growth vs interest rates, 1950–2017). **All three are the evidence for claims the model cannot settle** — **and Figure 7 is the one that decides §4's ambiguous case.** **Their conclusions are stated on Mishkin's authority and the accompanying prose, not reconstructed**; no data files exist in the vault. *(As in [[02 - The Meaning of Interest Rates|ch. 02]], note that his **expected-inflation series is model-estimated**, not observed — estimated from past rates, inflation and time trends — so "the expected inflation rate" in Figures 5 and 12 is an estimate carrying its own assumptions.)*
>
> **No erratum found in this chapter.** **All of Mishkin's stated numbers — five bond prices with their interest rates, both equilibria, the two expected returns, the money-demand schedule — reproduce.**
>
> **Additions beyond the source.**
>
> - **⚠️ §2 and §5's algebraic reconstruction is the chapter's principal addition**, and it is what makes the rest possible. **Mishkin never writes down an equation for either curve.** Recovering $B^d=2000-2P$, $B^s=2P-1400$, $M^d=600-20i$ turns a set of pictures into a model that can be interrogated.
> - **⚠️ §3 and §4's shift arithmetic is mine.** **The results $P^*=850-(a+b)/4$ (Fisher) and $P^*=850+(a-b)/4$ (business cycle) are the sharpest statements in the note**: the first shows the Fisher effect holds for *every* admissible parameter, and the second gives the exact tipping condition $a$ versus $b$ — **including the knife-edge $a=b$, at which the rate is exactly unchanged while borrowing rises, a case Mishkin's figure cannot display.**
> - **§3's finding that the Fisher effect determines the price but leaves the quantity open (change $=(b-a)/2$) is mine**, though Mishkin notes the ambiguity in words.
> - **§5's numerical verification of the equivalence identity, and the observation that liquidity preference is *sharper because it is narrower*, are mine.** **Mishkin says the frameworks are equivalent and that each is convenient for different questions; he does not observe that the extra definiteness in one is bought by suppressing a channel.** **That is the more useful lesson.**
> - **§6's three dynamic paths are my construction** — parameters chosen to realise Mishkin's three orderings, **not estimated**. **They illustrate the logic and are explicitly not evidence.** *(Mishkin's Figure 11 is itself a schematic with no data, so nothing is lost by rebuilding it; the numbers make the trough timing and the net effect explicit, which the sketch cannot.)*
> - **§7's run of the low-rate case through the recovered model is mine**, as is the framing that **low rates are a symptom rather than a stimulus** — Mishkin makes the point in words with his "you can never be too rich or too thin" analogy.
> - **The identification of this chapter as the third instance of the running theme — *which M?*, *which interest rate?*, *which curve moved?* — is my synthesis.**
> - **The cross-links implement [[00-Index]]'s boundary.** **Diversification and CAPM** go to [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]] and [[Commercial Banking/contents/02 - Organization, Structure and Market Entry|CB ch. 02]] rather than being re-derived; **loanable funds** stays with Macro/Micro, **as Mishkin's own footnote 3 independently confirms.**

**Previous:** [[02 - The Meaning of Interest Rates]] · **Next:** [[04 - The Risk and Term Structure of Interest Rates]]
