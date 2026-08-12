---
subject: Macroeconomics & Microeconomics
chapter: 10
tags: [ds, economics, macroeconomics, loanable-funds, crowding-out, present-value, diversification]
source: "Mankiw, *Principles of Macroeconomics* (2017), ch. 13–14"
---

# Saving, Investment and the Financial System

**[[09 - Production and Growth|Chapter 09]] showed that capital accumulation raises the level of income. This chapter is about the market that does the accumulating** — and about the tools for valuing a claim on the future.

**Three results.**

**§3 — crowding out, quantified.** Mankiw draws a budget deficit shifting the supply of loanable funds left and says investment falls. *(Computed: the **crowding-out fraction is $b/(a+b)$** — **60% here**, and **constant whatever the size of the deficit**, because it depends only on the two slopes.)*

**§4 — and its magnitude rests entirely on an assumption the theory cannot justify.** *(Computed: crowding out is **100%** if saving does not respond to the interest rate, **33.3%** if it responds strongly, and **over 100%** if the saving curve bends backward.)* **[[07 - Factor Markets and the Theory of Consumer Choice|Ch. 07]] proved the sign of that response is genuinely ambiguous** — so the model's most-quoted policy conclusion is an empirical input wearing a theoretical costume.

**§6 — Mankiw's diversification result is [[Commercial Banking/contents/02 - Organization, Structure and Market Entry|Commercial Banking ch. 02]]'s formula.** *(Computed: **29.3%** risk reduction at $\rho=0$ falling to **2.5%** at $\rho=0.9$ — the identical numbers, derived there for bank mergers.)* **The vault's recurring result, in its fifth setting.**

> [!warning] ⚠️ Equations reconstructed, not transcribed — see [[00-Index]].

## 📘 Main Knowledge

### 1. The accounting identities

**Start from [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]'s identity.** In a **closed economy** $NX = 0$, so:

$$Y = C + I + G\;\Longrightarrow\;\underbrace{Y - C - G}_{\text{national saving }S} = I$$

*(It extracts as `Y 2 C 2 G 5 I`.)*

$$S=\underbrace{(Y-T-C)}_{\text{private saving}}+\underbrace{(T-G)}_{\text{public saving}}$$

*(Computed with $Y=1000$, $C=700$, $G=200$, $T=250$: national saving **100**, private saving **50**, public saving **50** — and they sum exactly. Investment is therefore **100**.)*

> [!warning] $S = I$ is accounting, not behaviour
> **In a closed economy every dollar saved *is* a dollar invested, by definition.** So the identity **cannot be used to argue that saving causes investment** — it is true whichever way causation runs, and it would be true if neither caused the other.
>
> **[[08 - Measuring the Macroeconomy - GDP and the Cost of Living|Ch. 08]] flagged this trap and it recurs here**: an identity cannot be false and explains nothing on its own. **§2's loanable-funds market is what supplies the behaviour.**
>
> *(A **budget deficit** is negative public saving, $T < G$. That is the entire mechanism of §3.)*

### 2. The market for loanable funds

| | |
|---|---|
| **supply** | national saving — **assumed** to rise with $r$ *(see §4)* |
| **demand** | investment — falls with $r$ |
| **price** | the **real** interest rate |

*(Computed with $S = 100 + 20r$ and $I = 300 - 30r$: equilibrium $r^* = \mathbf{4.00\%}$ and $S = I = \mathbf{180}$.)*

**Mankiw's three policy experiments:** a **saving incentive** shifts supply right *(r falls, investment rises)*; an **investment tax credit** shifts demand right *(r rises, investment rises)*; a **budget deficit** shifts supply **left** — which is §3.

> [!note] Why investment slopes down — and it is §5's tool
> **A higher interest rate lowers the present value of a project's future returns, so fewer projects clear the bar.** The two halves of this chapter are one idea: **§5's discounting is what generates §2's demand curve.**

### 3. ⚠️ Crowding out, quantified

**A deficit $D$ reduces public saving, so supply becomes $S = S_0 - D + ar$:**

$$\Delta r=\frac{D}{a+b}\qquad \Delta I=-\frac{bD}{a+b}\qquad\boxed{\textbf{crowding-out fraction}=\frac{b}{a+b}}$$

*(Computed:)*

| deficit | $r$ rises to | investment falls to | $\Delta I$ | **crowded out** |
|---|---|---|---|---|
| 0 | 4.00% | 180.00 | — | — |
| 20 | 4.40% | 168.00 | −12.00 | **60.0%** |
| 50 | 5.00% | 150.00 | −30.00 | **60.0%** |
| 100 | 6.00% | 120.00 | −60.00 | **60.0%** |

> [!warning] The fraction is constant — it depends only on the two slopes
> **Whatever the size of the deficit, 60% of each dollar displaces private investment here.** Mankiw's diagram shows the direction; **this is the magnitude, and the magnitude is what a policy argument needs.**
>
> **And it varies enormously with how responsive saving is** *(computed)*:
>
> | saving slope $a$ | **crowded out** | |
> |---|---|---|
> | **0** | **100.0%** | saving fixed ⇒ **one-for-one** |
> | 5 | 85.7% | |
> | 20 | 60.0% | |
> | 60 | 33.3% | |
> | 1000 | 2.9% | saving very elastic ⇒ almost none |
>
> **If saving does not respond to the interest rate at all, a deficit crowds out investment dollar for dollar.** If saving responds strongly, almost nothing is displaced.
>
> **So the entire quantitative content of "crowding out" is a claim about the slope of the saving curve** — which is §4's problem.

### 4. ⚠️ The assumption the whole model rests on

**The loanable-funds diagram draws saving as upward-sloping. [[07 - Factor Markets and the Theory of Consumer Choice|Ch. 07]] showed that is not a result of the theory.**

**A higher real interest rate raises the price of consuming today:**

- **substitution effect** — future consumption is cheaper ⇒ **save more**
- **income effect** — a saver is richer ⇒ **save less**

**The two oppose, and nothing in consumer theory says which wins.**

*(Computed — what each case implies for §3:)*

| saving curve | $a$ | **crowding out** |
|---|---|---|
| strongly upward-sloping | 60 | **33.3%** |
| moderately upward-sloping | 20 | **60.0%** |
| **vertical (no response)** | **0** | **100.0%** |
| **backward-bending** | −10 | **150.0%** |

> [!warning] State it as an assumption
> **A backward-bending saving curve is theoretically possible** — [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]] noted that hours worked *fell* as wages rose over the last century, which is the identical structure — **and it would make crowding out exceed 100%.**
>
> **Mankiw is not wrong to draw the curve sloping up**: empirically saving does respond a little. **But it is an empirical input, not a deduction**, and the model's most-quoted policy conclusion is only as reliable as it.
>
> **This discharges [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]]'s explicit obligation** — and it is a good instance of the general rule that chapter reached: **when two effects oppose, say so, and do not let a diagram quietly pick a sign the theory refused to.**

### 5. Present value

$$\text{future value}=(1+r)^N\times\text{PV}\qquad\qquad \text{PV}=\frac{\text{future sum}}{(1+r)^N}$$

*(Verified — Mankiw's figures: \$100 at 5% for 10 years gives $(1.05)^{10}\times\$100 = \mathbf{\$162.89}$, the book's "\$163".)*

**Mankiw's question: \$100 today or \$200 in ten years?**

*(Computed: at 5% the PV of the \$200 is **\$122.78 > \$100**, so take the \$200. The break-even rate is $r^* = 2^{1/10}-1 = \mathbf{7.1773\%}$.)*

| $r$ | PV of \$200 in 10 yrs | decision |
|---|---|---|
| 2.00% | 164.07 | take the \$200 |
| 5.00% | 122.78 | take the \$200 |
| **7.18%** | **99.98** | **indifferent** |
| 10.00% | 77.11 | take the \$100 |
| 15.00% | 49.44 | take the \$100 |

> [!note] The rule of 70 checks out
> **[[09 - Production and Growth|Ch. 09]]'s rule says doubling in 10 years needs about 70/10 = 7% a year. The exact answer is 7.18%** — the approximation is good, and it is the same compounding arithmetic seen from the other end.
>
> **And note what the table shows: the higher the interest rate, the less a future sum is worth today.** That is exactly why investment demand slopes down in §2 — **discounting *is* the investment demand curve.**

### 6. ⚠️ Risk, diversification, and a formula met before

**People are *risk averse*: the disutility of losing \$1,000 exceeds the utility of gaining \$1,000, because marginal utility diminishes.** *(That is [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]]'s concave utility, applied to wealth.)* **Insurance, diversification and the risk–return trade-off all follow.**

*(Computed — $n$ equally-weighted **independent** stocks:)*

| $n$ | portfolio s.d. | **risk removed** |
|---|---|---|
| 1 | 1.0000 | 0.0% |
| 2 | 0.7071 | 29.3% |
| **20** | 0.2236 | **77.6%** |
| 40 | 0.1581 | 84.2% |
| 100 | 0.1000 | 90.0% |

**The gain is steep then flat: 1 → 20 stocks removes 78% of the risk; 20 → 100 removes only 12 points more.**

> [!warning] But independence is the assumption doing all the work
> *(Computed — two assets with correlation $\rho$: $\sigma_p=\sigma\sqrt{(1+\rho)/2}$:)*
>
> | $\rho$ | portfolio s.d. | **risk reduction** |
> |---|---|---|
> | **0.0** | 0.7071 | **29.3%** |
> | 0.3 | 0.8062 | 19.4% |
> | 0.6 | 0.8944 | 10.6% |
> | **0.9** | 0.9747 | **2.5%** |
> | 1.0 | 1.0000 | **0.0%** |
>
> **That is exactly [[Commercial Banking/contents/02 - Organization, Structure and Market Entry|Commercial Banking ch. 02]]'s formula, with the identical numbers** — derived there to explain why banks crossing state lines got no real diversification.
>
> **And it is the vault's recurring result in its fifth setting**: [[Commercial Banking/contents/02 - Organization, Structure and Market Entry|CB ch. 02]] (bank mergers), [[Commercial Banking/contents/06 - Hedging with Derivatives|ch. 06]] (securitisation tranches), [[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]] (loan books), [[Commercial Banking/contents/12 - Consumer, Credit Card and Real Estate Lending|ch. 12]] (mortgages), and now stock portfolios. **The average is always fine and the joint behaviour is everything.**
>
> **This is also precisely why market risk cannot be diversified away.** Every stock has $\rho > 0$ with the market, so **the $1/\sqrt{n}$ gain stops at the level of the common factor.** Mankiw says this in words; the formula is the arithmetic of it.

### 7. Asset valuation and efficient markets

**Fundamental analysis: a share is worth the present value of its future dividends plus its eventual sale price** — §5's tool applied.

**The efficient markets hypothesis** holds that prices already reflect all available information, so **the market price is the best available estimate of value.** Two testable consequences:

- **stock prices should follow a random walk** — anything predictable would already be in the price;
- **actively managed funds should not systematically beat index funds** — and Mankiw cites evidence that most underperform.

> [!note] Mankiw presents it as a good first approximation, not a law — which is the right posture
> **He gives the counter-evidence fairly**: bubbles and excess volatility are hard to reconcile with efficiency, and "irrational exuberance" is a real phenomenon.
>
> **The operative form for anyone doing quantitative work: if a pattern in prices were reliably predictable, trading on it would eliminate it.** **That is a genuine warning about backtested strategies and it has no analogue in most prediction problems** — the weather does not change because you forecast it. **Financial markets are the standard example of a system that responds to being modelled**, and [[Time-series Analysis/contents/00-Index|time-series]] work on prices has to reckon with it.

## ✏️ Exercises

**1. (Identities and the market.)** (a) Derive $S = I$ and decompose saving. (b) What can the identity *not* tell you? (c) Trace the three policy experiments.

> [!example]- Solution
> **(a) Subtract $C$ and $G$ from the closed-economy identity.**
>
> $$Y=C+I+G\;\Longrightarrow\;S\equiv Y-C-G=I$$
> $$S=\underbrace{(Y-T-C)}_{\text{private}}+\underbrace{(T-G)}_{\text{public}}$$
>
> *(Verified with $Y=1000$, $C=700$, $G=200$, $T=250$: **national 100 = private 50 + public 50**, and investment is 100.)*
>
> **Taxes $T$ cancel from the sum** — they move saving between the private and public columns without changing the total. **A budget deficit is simply negative public saving.**
>
> **(b) That saving causes investment — or anything else causal.**
>
> **$S = I$ is true by construction**: it holds whichever way causation runs, and it would hold if neither caused the other. **It is a constraint the data must satisfy, not a mechanism.**
>
> **This is [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]'s warning recurring**, and it matters because the identity is frequently deployed as though it were an argument. **The behaviour comes from §2's market**, where the interest rate does actual work.
>
> **(c) Each shifts one curve.**
>
> | policy | shifts | $r$ | investment |
> |---|---|---|---|
> | saving incentive | **supply right** | falls | **rises** |
> | investment tax credit | **demand right** | **rises** | **rises** |
> | **budget deficit** | **supply left** | **rises** | **falls** |
>
> **The first two both raise investment and are distinguished by what happens to the interest rate** — which is how you would tell them apart in data. **The third is §3.**

**2. (Hard — crowding out.)** (a) Quantify it. (b) What determines the fraction? (c) Why is the whole result resting on an assumption?

> [!example]- Solution
> **(a) $\Delta I = -bD/(a+b)$ — 60% of each deficit dollar here.**
>
> *(Computed: deficits of 20, 50 and 100 raise $r$ to 4.40%, 5.00% and 6.00%, cutting investment by 12, 30 and 60 — **exactly 60% in every case**.)*
>
> **The mechanism: the government borrows, competing with firms for the same pool of saving.** The interest rate rises, and some private projects that were worth doing at 4% are not worth doing at 6%.
>
> **⚠️ The fraction is constant in the size of the deficit**, because both curves are linear — **it depends only on the two slopes, not on how much is borrowed.** *(A useful property: you can quote "this economy crowds out 60 cents on the dollar" without specifying the deficit.)*
>
> **(b) The relative slopes: $b/(a+b)$.**
>
> **The more responsive *saving* is (large $a$), the less is crowded out** — because the higher interest rate calls forth new saving that partly fills the gap. **The more responsive *investment* is (large $b$), the more is crowded out** — because firms retreat quickly as the rate rises.
>
> *(Computed across saving slopes: **100.0%** at $a=0$, **85.7%** at 5, **60.0%** at 20, **33.3%** at 60, **2.9%** at 1000.)*
>
> **The limiting case is the memorable one: if saving does not respond to the interest rate at all, a deficit crowds out investment one-for-one.** Every dollar the government borrows is a dollar of private investment forgone.
>
> **(c) Because [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]] proved the saving curve's slope is theoretically ambiguous.**
>
> **A higher interest rate has a substitution effect (save more — future consumption is cheaper) and an income effect (save less — a saver is richer), and consumer theory does not say which dominates.**
>
> *(Computed: a **backward-bending** saving curve gives crowding out of **150%** — more than the deficit itself.)*
>
> **So the diagram's upward slope is an empirical input, and the model's headline policy conclusion inherits all of its uncertainty.** **Mankiw is not wrong to draw it that way** — saving does respond somewhat in the data — **but the honest statement is "crowding out is between roughly a third and all of the deficit, depending on a parameter this theory cannot sign."**
>
> **⚠️ This is the general lesson [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]] reached, in its most consequential application: when two effects oppose, say so — and do not let a diagram quietly choose a sign the theory refused to choose.** A drawn curve looks like a result and is frequently an assumption.

**3. (Finance tools.)** (a) Compute present values. (b) Why does investment demand slope down? (c) What does diversification do, and what can it not do?

> [!example]- Solution
> **(a) Discount at the interest rate.**
>
> $$\text{PV}=\frac{\text{future sum}}{(1+r)^N}$$
>
> *(Verified: \$100 at 5% for 10 years grows to **\$162.89** — Mankiw's "\$163". And \$200 in 10 years has a PV of **\$122.78** at 5%, so take the \$200; the break-even rate is **7.1773%**.)*
>
> **[[09 - Production and Growth|Ch. 09]]'s rule of 70 predicts 7% for a doubling over ten years — good to within a fifth of a point.** Same compounding arithmetic from the other direction.
>
> **(b) Because a higher rate shrinks the present value of every future return.**
>
> *(Computed: the PV of \$200 in ten years falls from **\$164.07** at 2% to **\$49.44** at 15%.)*
>
> **A firm undertakes a project if the present value of its returns exceeds its cost.** Raising $r$ lowers every project's present value, so **fewer clear the bar** — which is precisely a downward-sloping investment demand curve.
>
> **So §5 is not a separate topic bolted onto §2; it is the derivation of §2's demand curve.** *(And it is the same discounting [[Commercial Banking/contents/07 - The Investment Portfolio|Commercial Banking ch. 07]] uses to price a bond — one tool, three settings.)*
>
> **(c) It removes firm-specific risk and cannot touch market risk.**
>
> *(Computed for independent stocks: $\sigma_p=\sigma/\sqrt{n}$, so **29.3%** of risk goes with 2 stocks, **77.6%** with 20, **90.0%** with 100 — steeply diminishing.)*
>
> **The practical implication is that most of the benefit arrives quickly**: 20 stocks capture the great majority of what 100 would.
>
> **⚠️ But independence is the assumption doing the work.** *(Computed with correlation: risk reduction falls from **29.3%** at $\rho=0$ to **2.5%** at $\rho=0.9$ and **zero** at $\rho=1$.)*
>
> $$\sigma_p=\sigma\sqrt{\frac{1+\rho}{2}}$$
>
> **That is [[Commercial Banking/contents/02 - Organization, Structure and Market Entry|Commercial Banking ch. 02]]'s formula with the identical numbers**, derived there to explain why bank mergers across state lines produced no real diversification.
>
> **And it explains *why* market risk is undiversifiable in a way the verbal statement does not**: every stock is positively correlated with the market, so **the $1/\sqrt{n}$ gain stops at the level of the common factor** no matter how many holdings you add.
>
> **⚠️ This is the vault's recurring result for the fifth time** — bank mergers, securitisation tranches, loan books, mortgage portfolios, and now equity portfolios. **The average is always fine and the joint behaviour is everything**, and **any risk measure built on expected values is blind to it.**

## 📝 Summary

- **In a closed economy $Y = C+I+G$, so $S \equiv Y-C-G = I$**, and $S$ = private saving + public saving *(verified: 100 = 50 + 50)*.
- **⚠️ $S = I$ is accounting, not behaviour.** It cannot show that saving causes investment; **§2's market supplies the mechanism.** *(A budget deficit is negative public saving.)*
- **The loanable-funds market sets the *real* interest rate** *(computed: $r^*=\mathbf{4.00\%}$, $S=I=180$)*. **Saving incentives shift supply; investment tax credits shift demand; deficits shift supply left.**
- **⚠️ Crowding out quantified: the fraction is $b/(a+b)$ — 60% here, and constant whatever the deficit's size** *(computed: deficits of 20/50/100 displace 12/30/60 of investment)*.
- **⚠️ And it ranges from 100% to nearly zero depending on how responsive saving is** *(computed: **100.0%** at $a=0$, **60.0%** at 20, **33.3%** at 60, **2.9%** at 1000)*.
- **⚠️ [[07 - Factor Markets and the Theory of Consumer Choice|Ch. 07]] proved that responsiveness is theoretically ambiguous** — substitution says save more, income says save less. **A backward-bending curve gives crowding out of 150%.**
- **So the loanable-funds diagram's upward-sloping saving curve is an *assumption*, not a result** — and the model's headline policy conclusion inherits its uncertainty. **When two effects oppose, say so.**
- **Present value: $\text{PV}=\text{future sum}/(1+r)^N$** *(verified: \$100 at 5% for 10 years = **\$162.89**; break-even for \$100-vs-\$200-in-10-years is **7.1773%**, matching [[09 - Production and Growth|ch. 09]]'s rule of 70)*.
- **Discounting *is* the investment demand curve** — a higher $r$ lowers every project's present value, so fewer clear the bar. **The two halves of the chapter are one idea.**
- **Risk aversion follows from diminishing marginal utility of wealth** ([[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]]'s concavity), and it generates insurance, diversification and the risk–return trade-off.
- **⚠️ Diversification: $\sigma_p=\sigma/\sqrt{n}$ for independent assets** *(computed: **29.3%** of risk removed with 2 stocks, **77.6%** with 20, **90.0%** with 100 — steeply diminishing, so 20 captures most of it)*.
- **⚠️ But with correlation $\sigma_p=\sigma\sqrt{(1+\rho)/2}$, and the reduction collapses from 29.3% at $\rho=0$ to 2.5% at $\rho=0.9$** — **exactly [[Commercial Banking/contents/02 - Organization, Structure and Market Entry|Commercial Banking ch. 02]]'s formula and numbers.**
- **That explains why market risk is undiversifiable**: every stock correlates with the market, so **the $1/\sqrt{n}$ gain stops at the common factor.**
- **⚠️ Fifth appearance of the vault's recurring result** — bank mergers, tranches, loan books, mortgages, equity portfolios. **The average is fine and the joint behaviour is everything.**
- **The efficient markets hypothesis** predicts a random walk and that active funds do not beat index funds; **Mankiw presents it as a good first approximation, not a law.** **If a price pattern were reliably predictable, trading on it would eliminate it** — a warning specific to markets.

## ⚠️ Important Notes

1. **⚠️ $S = I$ is an identity.** It constrains the data; it explains nothing.
2. **A budget deficit is negative public saving** — that is the whole of §3's mechanism.
3. **Taxes cancel from national saving.** They move it between the private and public columns.
4. **The loanable-funds price is the *real* rate**, not the nominal one ([[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]).
5. **⚠️ Crowding-out fraction $= b/(a+b)$** — constant in the deficit's size, determined by slopes.
6. **⚠️ Zero saving response ⇒ one-for-one crowding out.** Memorise the limiting case.
7. **⚠️ The upward-sloping saving curve is an assumption**, and a drawn curve looks like a result.
8. **When two effects oppose, quote a range rather than a point.**
9. **Saving incentives and investment tax credits both raise investment** — they differ in what happens to $r$, which is how to tell them apart empirically.
10. **⚠️ Discounting generates the investment demand curve.** They are not two topics.
11. **The rule of 70 works in both directions** — growth rates and discount rates.
12. **Risk aversion comes from concave utility**, so it is the same machinery as [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]].
13. **⚠️ Most diversification benefit arrives by ~20 holdings.** The curve is $1/\sqrt{n}$.
14. **⚠️ $\sigma_p = \sigma\sqrt{(1+\rho)/2}$ — correlation destroys diversification.** Independence is the load-bearing assumption.
15. **Market risk is undiversifiable because $\rho>0$ with the market**, not because of anything mysterious.
16. **⚠️ A predictable price pattern eliminates itself when traded on.** Backtests need this caveat; most prediction problems do not.

> [!warning] Gaps in the source material
> **Mankiw's prose extracts cleanly and the outline located both chapters** *(Macro 2017, PDF pp. 288–323)*.
>
> **⚠️ THE OPERATOR CIPHER applies throughout** — the identities extract as `Y 5 C 1 I 1 G 1 NX` and `Y 2 C 2 G 5 I`, and the compounding formulas as `(1 1 r) 3 $100` and `(1 1 r)2 3 $100`. **Nothing was transcribed.** *(The chapter also shows the word-duplication fault: "`what will be the N years? That is, what will be the N future value`".)*
>
> **⚠️ Every figure is lost**, and this chapter is heavily diagrammatic: **the loanable-funds market, all three policy-experiment panels, the deficit/crowding-out figure, and the risk-reduction curve are images.** **This is why §§2–3 build the market algebraically from explicitly stated linear curves** — the diagram cannot be recovered, and the algebra yields a magnitude the diagram never had.
>
> **Ch. 13 and 14 contain no data tables**, so — unlike [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]] — **the only source figures available to verify were the present-value numbers in the prose**, which check exactly (\$163 for the future value).
>
> **No erratum.** Every figure Mankiw states reproduces.
>
> **Additions beyond the source.**
>
> - **⚠️ §3's quantification of crowding out is the chapter's main addition.** **Mankiw draws the deficit shifting the supply curve and says investment falls; he never gives a magnitude.** The result **crowding-out fraction $= b/(a+b)$**, its **constancy in the deficit's size**, and the range from **100% to 2.9%** across saving elasticities are not in the source — and the magnitude is what any policy argument actually needs.
> - **⚠️ §4 discharges [[07 - Factor Markets and the Theory of Consumer Choice|ch. 07]]'s explicit obligation and is mine.** Mankiw draws the saving curve sloping up without flagging it as an assumption. **Showing that a vertical curve gives 100% crowding out and a backward-bending one gives 150% establishes that the model's headline conclusion rests on a parameter consumer theory cannot sign.**
> - **⚠️ §6's identification of Mankiw's diversification discussion as [[Commercial Banking/contents/02 - Organization, Structure and Market Entry|Commercial Banking ch. 02]]'s formula is my cross-subject link**, and the numbers match exactly (**29.3%** at $\rho=0$, **2.5%** at $\rho=0.9$). **Mankiw states that diversification removes firm-specific but not market risk and gives no formula; the correlation version explains *why* — the $1/\sqrt{n}$ gain stops at the common factor.** This is the **fifth setting** for the vault's recurring correlation result.
> - **The observation that §5's discounting *generates* §2's investment demand curve** — making the two halves of the chapter one idea rather than two — is mine.
> - **§7's framing that a predictable price pattern eliminates itself when traded on**, and that this has no analogue in most prediction problems, is an addition aimed at this reader.
> - **The note that saving incentives and investment tax credits are distinguished empirically by the direction of $r$** is mine.
>
> **Deliberately compressed.** **Mankiw ch. 13's survey of financial institutions** (bond and stock markets, mutual funds, banks; bond terms — maturity, credit risk, tax treatment) is compressed to the market's function, because **[[Commercial Banking/contents/00-Index|Commercial Banking]] owns this material in depth** and its boundary statement assigns institutional detail there. **The US budget-deficit history and debt case study** is represented by §3's mechanism. **Ch. 14's treatment of the risk–return trade-off and the specific measurement of stock-market risk** is compressed to §6's arithmetic. **Fundamental analysis in detail, and the market/firm-specific risk decomposition**, are noted rather than developed — the formal version is portfolio theory, beyond this course. **The behavioural-finance discussion** is summarised in §7's caveats.

**Previous:** [[09 - Production and Growth]] · **Next:** [[11 - Unemployment]]
