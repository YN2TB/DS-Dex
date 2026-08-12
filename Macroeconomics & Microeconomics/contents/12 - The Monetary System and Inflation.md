---
subject: Macroeconomics & Microeconomics
chapter: 12
tags: [ds, economics, macroeconomics, money, money-multiplier, quantity-theory, inflation, fisher]
source: "Mankiw, *Principles of Macroeconomics* (2017), ch. 16–17"
---

# The Monetary System and Inflation

**[[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|Chapter 01]]'s Principle 9 — *prices rise when the government prints too much money* — is proved here.**

**Three results.**

**§2b — the money multiplier $1/R$ is an *upper bound*, and it collapses.** *(Computed: the textbook multiplier of 10 falls to **4.00** once households hold currency, and to **1.50** under 2008–14 conditions — **15% of the textbook value**.)* **Mankiw notes banks "may hold excess reserves" and never computes the consequence, which is that the central bank controls the *base*, not the money supply.**

**§4 — the quantity theory delivers Principle 9 exactly.** *(Verified: Mankiw's velocity of **20**; then $\%M + \%V = \%P + \%Y$ gives **inflation = money growth − real growth**.)*

**§6 — the inflation tax has a Laffer peak.** *(Computed: revenue rises to a maximum at **100% inflation** and then collapses to almost nothing by 1000%, because high inflation drives people out of holding money at all.)* **That is [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]'s Laffer curve on a different tax base, and it is why hyperinflations end.**

> [!warning] ⚠️ Equations reconstructed, not transcribed — see [[00-Index]].

## 📘 Main Knowledge

### 1. What money is

| function | |
|---|---|
| **medium of exchange** | avoids the double coincidence of wants |
| **unit of account** | the yardstick prices are quoted in |
| **store of value** | transfers purchasing power over time |

> [!note] Only the first distinguishes money from other assets
> **Bonds and houses are stores of value; only money is generally accepted in trade.** That is why **liquidity** — the ease of converting to a medium of exchange — is the property the money-supply measures are built around.
>
> **Commodity money** has intrinsic value (gold); **fiat money** does not, and works by government decree plus convention. **M1** = currency + demand deposits + other checkable deposits; **M2** adds savings deposits, small time deposits and money-market funds. **The boundary between them is a judgement about liquidity, not a fact** — which is [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]'s caution again.

### 2. Fractional-reserve banking and the money multiplier

*(Verified — Mankiw's example: \$100 of reserves, a 10% reserve ratio:)*

| round | deposit created | cumulative |
|---|---|---|
| original | 100.00 | 100.00 |
| 2 | 90.00 | 190.00 |
| 3 | 81.00 | 271.00 |
| 4 | 72.90 | 343.90 |
| … | | |
| **limit** | | **1 000.00** ✓ |

$$\textbf{money multiplier}=\frac{1}{R}=\mathbf{10}\;✓$$

> [!note] Banks create money — but not wealth
> **Nothing is printed. The same reserves support a larger stack of deposits, and deposits *are* money.**
>
> **But every new deposit arrives with a matching loan**, so the borrower's asset is offset by their debt. **Mankiw is explicit about this and it is the point most often missed** in popular accounts of "banks creating money out of nothing".

### 2b. ⚠️ $1/R$ is an upper bound, and it collapses

**$1/R$ assumes banks lend out *everything* above the required reserve and nobody holds currency.** Relax both:

$$\text{multiplier}=\frac{1+c}{R+e+c}$$

*(where $e$ = excess reserves/deposits and $c$ = currency/deposits. Computed:)*

| | $e$ | $c$ | **multiplier** | vs textbook |
|---|---|---|---|---|
| textbook | 0.00 | 0.00 | **10.0000** | 100.0% |
| realistic currency holding | 0.00 | 0.20 | **4.0000** | 40.0% |
| some excess reserves | 0.05 | 0.20 | 3.4286 | 34.3% |
| **2008–14 conditions** | **0.50** | 0.20 | **1.5000** | **15.0%** |
| heavy excess | 1.50 | 0.20 | 0.6667 | 6.7% |

> [!warning] The central bank controls the base, not the money supply
> **After 2008, US banks held enormous excess reserves — the Fed had begun paying interest on them — and the money supply did *not* expand in proportion to the monetary base.** Very large base expansion produced modest money growth and little inflation, **which surprised a great many people who had memorised $1/R$.**
>
> **Mankiw notes that banks "may hold excess reserves" and does not compute the consequence.** *(Computed: the multiplier falls below 2.)* **The multiplier is a behavioural outcome, not a policy lever** — the central bank sets the base and the requirement, while **banks decide excess reserves and households decide currency holdings.**
>
> **Boundary note:** *how* a central bank operates is [[Monetary and Financial Theories/contents/00-Index|Mishkin]]'s, per the split recorded in [[00-Index]]; **the multiplier as a macro identity belongs here.** And the bank's own balance sheet is [[Commercial Banking/contents/00-Index|Commercial Banking]]'s — **its entire subject sits inside one line of this section.**

### 3. Central-bank tools

- **Open-market operations** — buy or sell government bonds. **The main tool**, because it is continuous and reversible.
- **Reserve requirements** — change $R$ directly. **Rarely used**: disruptive.
- **The discount rate and interest on reserves** — change banks' incentive to hold reserves rather than lend.

> [!note] §2b is why control is imperfect
> **Two of the four quantities in the multiplier are decided by people the central bank does not control**, and both moved violently in 2008.

### 4. The quantity theory

$$M\times V=P\times Y$$

*(It extracts as `M 3 V 5 P 3 Y`. Verified on Mankiw's illustration — 100 units sold at \$10 with a money stock of \$50: $V=(10\times100)/50=\mathbf{20}$ ✓.)*

**Velocity is how often a dollar changes hands in a year.** Taking growth rates:

$$\%\Delta M+\%\Delta V=\%\Delta P+\%\Delta Y\;\xrightarrow{\;V\text{ stable}\;}\;\boxed{\textbf{inflation}=\%\Delta M-\%\Delta Y}$$

*(Computed, with real growth at 3%:)*

| money growth | **implied inflation** |
|---|---|
| 2% | **−1%** |
| 5% | **2%** |
| 10% | **7%** |
| 30% | **27%** |
| 100% | **97%** |

> [!warning] Inflation is money growth in excess of real growth
> **That is the precise sense of "inflation is always and everywhere a monetary phenomenon", and it is [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s Principle 9 derived rather than asserted.**
>
> **The load-bearing assumption is that $V$ is stable.** Over long horizons and in high-inflation episodes that is a good approximation; **over a few quarters it is not** — which is exactly why this is a **long-run** theory and why [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]] needs a different model.

### 5. The classical dichotomy and monetary neutrality

**Nominal** variables are measured in money; **real** variables in quantities or relative prices. **The classical dichotomy** is the claim that the two can be analysed separately.

**Monetary neutrality**: changes in the money supply affect nominal variables and leave real ones — output, employment, relative prices — unchanged.

> [!note] Money is the unit of account, so doubling it is relabelling a measuring stick
> **If every price and wage doubles, nothing real has changed.** That is the whole intuition, and Mankiw's version of it is exactly right.
>
> **⚠️ But this is a long-run claim only, and [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]] is where it fails.** **In the short run prices are sticky, so a monetary change moves real output** — which is the entire reason monetary policy exists as a stabilisation tool. **Mankiw flags this carefully, and it is the hinge between the two halves of macroeconomics.**

### 6. ⚠️ The Fisher effect and the inflation tax

$$\text{nominal rate}=\text{real rate}+\text{inflation}$$

**The Fisher effect: in the long run a 1-point rise in inflation raises the nominal rate one-for-one and leaves the real rate alone.**

| real rate | inflation | **nominal rate** |
|---|---|---|
| 3% | 0% | **3%** |
| 3% | 3% | **6%** |
| 3% | 10% | **13%** |

> [!note] High nominal rates are evidence of high *expected inflation*, not of tight money
> **Confusing the two is a classic error** — and it matters because it inverts the policy inference. *(A country with 20% nominal rates is usually one with high inflation, not one with an aggressive central bank.)*

**The inflation tax** — printing money to fund spending taxes whoever holds money.

*(Computed with a standard money demand $m = M_0e^{-k\pi}$, so real balances fall as inflation rises:)*

| inflation | real balances | **tax revenue** |
|---|---|---|
| 2% | 98.02 | 1.96 |
| 50% | 60.65 | 30.33 |
| **100%** | 36.79 | **36.79** ← **peak** |
| 200% | 13.53 | 27.07 |
| 500% | 0.67 | 3.37 |
| **1000%** | **0.00** | **0.05** |

> [!warning] The same Laffer curve as [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]], on a different base
> *(Exact optimum: $\pi^* = 1/k = 100\%$.)* **Revenue rises, peaks, and collapses — because high inflation drives people out of holding money at all.**
>
> **That is why hyperinflations end**: the tax base disappears. *(By 1000% inflation the revenue is 0.05 against a peak of 36.79.)*
>
> **And it explains *why* governments inflate: it is the one tax that requires no legislation.** Mankiw's hyperinflation examples all begin with a government unable to raise revenue any other way.

### 7. The costs of inflation

| cost | |
|---|---|
| **shoeleather** | resources wasted economising on money holdings |
| **menu costs** | the real cost of changing posted prices |
| **relative-price variability** | prices change at different times, so relative prices are distorted — **and [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]'s efficiency argument degrades** |
| **tax distortions** | nominal capital gains and nominal interest are taxed, so inflation raises the **effective** tax rate on saving |
| **confusion and inconvenience** | the unit of account changes length |
| **⚠️ arbitrary redistribution** | **unexpected** inflation transfers wealth from creditors to debtors |

**Mankiw rates the last as the most important** — and it is the only one that depends on inflation being **unexpected.**

*(Computed — a \$100 loan at an 8% nominal rate:)*

| expected | **actual** | lender's real return | |
|---|---|---|---|
| 3% | 3% | **+5.0%** | as planned |
| 3% | **8%** | **0.0%** | **lender loses** |
| 3% | **0%** | **+8.0%** | **lender gains** |

> [!warning] Nobody agreed to that transfer
> **Expected inflation is handled by the Fisher effect — it is priced into the nominal rate. It is the *surprise* that redistributes**, and the transfer can be very large.
>
> **So unexpected inflation is worse than expected inflation of the same size**, and **credibility is a central bank's main asset** — a point [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]] returns to when it computes the sacrifice ratio.

## ✏️ Exercises

**1. (Money and banking.)** (a) What makes something money? (b) Derive the multiplier. (c) Why is $1/R$ an upper bound, and what follows?

> [!example]- Solution
> **(a) Being a medium of exchange — the other two functions are shared.**
>
> **Bonds and houses store value; only money is generally accepted in trade.** So **liquidity** is the organising property, and M1/M2 are drawn by it.
>
> **Fiat money works by decree plus convention** and has no intrinsic value — which sounds fragile and is not, because **its value comes from everyone else accepting it**, a coordination equilibrium rather than a physical fact.
>
> **⚠️ The M1/M2 boundary is a judgement**, not a measurement — [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]'s caution about constructed statistics applies exactly.
>
> **(b) Each round lends out $(1-R)$ of the last.**
>
> *(Verified: \$100 → \$90 → \$81 → \$72.90 → … summing to $100/0.10 = \mathbf{\$1{,}000}$, so the multiplier is $1/R = \mathbf{10}$ ✓.)*
>
> **Banks create money by lending**: the same reserves support a larger stack of deposits, and **deposits are money.**
>
> **⚠️ But they do not create wealth.** Every deposit arrives with a matching loan, so the borrower's new asset is offset by their new debt. **The system's net worth is unchanged** — which is what popular accounts of "money from nothing" get wrong.
>
> **(c) Because it assumes no excess reserves and no currency.**
>
> $$\text{multiplier}=\frac{1+c}{R+e+c}$$
>
> *(Computed: **10.00** in the textbook case, **4.00** with realistic currency holding, **1.50** under 2008–14 conditions — **15% of the textbook value.**)*
>
> **After 2008 US banks held enormous excess reserves, and the money supply did not expand with the base.** Very large base expansion produced modest money growth and little inflation — **a result that surprised people who had memorised $1/R$ and had not noticed it was an upper bound.**
>
> **⚠️ So the central bank controls the *base*, not the money supply.** Two of the four quantities in the formula are decided by banks and households, and **both moved violently in the crisis.** *(Mankiw says banks "may hold excess reserves" and stops; the computation is what turns that into a conclusion.)*

**2. (Hard — the quantity theory.)** (a) Derive inflation from it. (b) What is monetary neutrality and when does it fail? (c) What is the Fisher effect and why does it matter?

> [!example]- Solution
> **(a) $\%\Delta M + \%\Delta V = \%\Delta P + \%\Delta Y$.**
>
> *(Verified: Mankiw's $V = (P\times Y)/M = (10\times100)/50 = \mathbf{20}$.)*
>
> **With $V$ stable, inflation $= \%\Delta M - \%\Delta Y$.** *(Computed at 3% real growth: money growth of 5% gives 2% inflation; 10% gives 7%; **100% gives 97%**.)*
>
> **That is [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s Principle 9, derived** — and the precise content of "inflation is always and everywhere a monetary phenomenon."
>
> **⚠️ The assumption is that $V$ is stable, and it is doing real work.** Over long horizons and in high-inflation episodes it holds well; **over a few quarters it does not.** **So this is a long-run theory**, and treating it as a short-run forecasting rule is the standard misuse — quantitative easing raised the base enormously without proportional inflation partly because both $V$ and the multiplier (§2b) fell.
>
> **(b) Money affects nominal variables only — in the long run.**
>
> **The classical dichotomy separates nominal from real variables; monetary neutrality says money moves only the former.** **The intuition: money is the unit of account, so doubling it relabels the measuring stick.** If every price and wage doubles, nothing real changed.
>
> **⚠️ It fails in the short run because prices are sticky.** Firms do not reprice instantly, so **a monetary change moves real output** — which is the entire reason monetary policy can stabilise an economy.
>
> **That is the hinge between the two halves of macro**: [[09 - Production and Growth|chs. 09]]–12 are the long run where money is neutral, and [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]] is the short run where it is not. **Mankiw is careful to flag it, and a reader who takes neutrality as unconditional will find ch. 14 incomprehensible.**
>
> **(c) Nominal rates move one-for-one with expected inflation.**
>
> *(Computed at a 3% real rate: inflation of 0%, 3%, 10% gives nominal rates of **3%, 6%, 13%**.)*
>
> **⚠️ So persistently high nominal rates are evidence of high *expected inflation*, not of tight money** — and inverting that inference is a classic error. **A country with 20% nominal rates is almost always a high-inflation country, not one with an aggressive central bank.**
>
> **It also completes [[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]'s real-versus-nominal distinction**: the real rate is what matters for behaviour, and the nominal rate is what is observed — so **any nominal series must be deflated before it means anything.**
>
> **And it sets up §7's most important cost**: because *expected* inflation is priced into the nominal rate, **only the surprise redistributes.**

**3. (Inflation.)** (a) What is the inflation tax and why does it have a peak? (b) List the costs. (c) Why is unexpected inflation worse?

> [!example]- Solution
> **(a) A tax on money-holders, and it peaks because the base runs away.**
>
> **Printing money to fund spending transfers real resources from whoever holds money** — nobody votes for it, and it requires no legislation.
>
> *(Computed with $m = M_0e^{-k\pi}$: revenue rises to a **peak of 36.79 at 100% inflation** and falls to **0.05 by 1000%**. Exact optimum $\pi^*=1/k$.)*
>
> **High inflation drives people out of holding money at all**, so the base shrinks faster than the rate rises.
>
> **⚠️ That is [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]'s Laffer curve on a different tax base** — and the same lesson applies: **the peak is not a target, and the damage per unit of revenue rises long before it.**
>
> **It also explains why hyperinflations end.** They are not stopped by resolve; **the tax base disappears**, people switch to foreign currency or barter, and the government must find revenue elsewhere.
>
> **(b) Six, and they are not equally serious.**
>
> **Shoeleather** (economising on money), **menu costs**, **relative-price variability** (which degrades [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]'s allocative efficiency, since prices adjust at different times), **tax distortions** (nominal gains and nominal interest are taxed, so inflation raises the effective tax on saving), **confusion**, and **arbitrary redistribution**.
>
> **⚠️ The tax distortion deserves emphasis** because it is invisible: with 3% real returns and 5% inflation, an 8% nominal gain is taxed in full, **so the effective rate on the real return far exceeds the statutory rate.** Inflation raises taxes without anyone legislating.
>
> **(c) Because expected inflation is already in the nominal rate.**
>
> *(Computed on a \$100 loan at 8% nominal: with expected and actual inflation both 3%, the lender earns **+5.0%** as planned; if actual inflation comes in at **8%**, the real return is **0.0%**; if at **0%**, it is **+8.0%**.)*
>
> **The Fisher effect handles anticipated inflation — lenders demand compensation and get it. It is the *surprise* that transfers wealth**, from creditors to debtors when inflation exceeds expectations and the reverse when it falls short.
>
> **⚠️ Nobody agreed to that transfer, and it can be large.** A five-point surprise wiped out the lender's entire real return in the example.
>
> **So unexpected inflation is strictly worse than expected inflation of the same size**, and **credibility is a central bank's main asset** — if expectations are anchored, the Fisher effect does the work and the redistribution never happens. **[[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|Ch. 14]] returns to this when it computes the cost of disinflation.**

## 📝 Summary

- **Money's three functions are medium of exchange, unit of account and store of value — but only the first distinguishes it from other assets.** **Liquidity** is what M1 and M2 are built around, and **the boundary between them is a judgement.**
- **Fractional-reserve banking creates money by lending** *(verified: \$100 of reserves at $R=10\%$ generates **\$1,000**, so the multiplier is $1/R = \mathbf{10}$)*.
- **Banks create money, not wealth** — every deposit arrives with a matching loan.
- **⚠️ $1/R$ is an upper bound** *(computed: **10.00** textbook → **4.00** with realistic currency holding → **1.50** under 2008–14 conditions, **15% of textbook**)*.
- **⚠️ So the central bank controls the *base*, not the money supply.** Excess reserves and currency holdings are decided by banks and households, and both moved violently in 2008 — **which is why huge base expansion produced little inflation.**
- **Open-market operations are the main tool**; reserve requirements are disruptive and rarely used.
- **The quantity equation $M\times V = P\times Y$** *(verified: $V = \mathbf{20}$)*, and in growth rates **inflation = money growth − real growth** *(computed across a range)*.
- **⚠️ That is [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]'s Principle 9 derived** — with **stable $V$ as the load-bearing assumption**, which makes it a **long-run** theory.
- **Monetary neutrality: money moves nominal variables and leaves real ones alone** — because money is the unit of account, so doubling it relabels the measuring stick.
- **⚠️ Neutrality is long-run only, and [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]] is where it fails.** Sticky prices mean monetary changes move real output — **the hinge between the two halves of macro.**
- **The Fisher effect: nominal = real + inflation, one-for-one in the long run** *(computed: 3% / 6% / 13%)*. **High nominal rates signal high expected inflation, not tight money.**
- **⚠️ The inflation tax peaks at 100% inflation and collapses to almost nothing by 1000%** *(computed: revenue **36.79 → 0.05**)* — **[[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]'s Laffer curve on a different base, and why hyperinflations end.**
- **Governments inflate because it is the one tax requiring no legislation.**
- **Six costs of inflation** — shoeleather, menu, relative-price variability, tax distortions, confusion, and **arbitrary redistribution**, which Mankiw rates most serious.
- **⚠️ Only *unexpected* inflation redistributes** *(computed: a 5-point surprise turns a lender's +5.0% real return into **0.0%**)*. **Expected inflation is priced in by the Fisher effect** — which is why **credibility is a central bank's main asset.**

## ⚠️ Important Notes

1. **Only the medium-of-exchange function distinguishes money.** The other two are shared with many assets.
2. **The M1/M2 boundary is a judgement about liquidity**, not a fact.
3. **Banks create money by lending, and create no wealth.**
4. **⚠️ $1/R$ is an upper bound.** Use $(1+c)/(R+e+c)$ when excess reserves or currency matter.
5. **⚠️ The multiplier is a behavioural outcome, not a policy lever.** The central bank sets the base.
6. **Huge base expansion can produce little inflation** — 2008–14 is the case.
7. **⚠️ $M\times V = P\times Y$ requires stable $V$** — a long-run assumption, not a quarterly one.
8. **Inflation = money growth − real growth.** Principle 9, derived.
9. **⚠️ Monetary neutrality is long-run only.** Taking it as unconditional makes [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]] incomprehensible.
10. **⚠️ High nominal rates mean high expected inflation**, not tight policy. The inference is frequently inverted.
11. **Deflate every nominal series before interpreting it** ([[08 - Measuring the Macroeconomy - GDP and the Cost of Living|ch. 08]]).
12. **⚠️ The inflation tax has a Laffer peak** and the damage per unit of revenue rises long before it.
13. **Hyperinflations end because the tax base disappears**, not through resolve.
14. **Inflation raises effective tax rates on saving** without any legislation — an invisible cost.
15. **⚠️ Only the *surprise* component of inflation redistributes.** Expected inflation is in the nominal rate.
16. **Credibility is a central bank's main asset** — anchored expectations make the Fisher effect do the work.

> [!warning] Gaps in the source material
> **Mankiw's prose extracts cleanly and the outline located both chapters** *(Macro 2017, PDF pp. 350–397)*.
>
> **⚠️ THE OPERATOR CIPHER applies throughout** — the quantity equation extracts as `M 3 V 5 P 3 Y`, velocity as `V 5 (P 3 Y)/M`, the Fisher equation as `Real interest rate 5 Nominal interest rate 2 Inflation rate`, and the multiplier sequence as `First National lending 5 $ 90.00 (5 .9 3 $100.00)`. **Nothing was transcribed** — and all of these were among the passages used during setup to *establish* the cipher, so they are known-good checks. **See [[00-Index]].**
>
> **⚠️ Every figure is lost**, including the money-supply time series, the money-growth-versus-inflation scatter plots (both the US time series and the international cross-section), and the money-market diagram. **The bank T-accounts survived as text** and are used in §2.
>
> **No erratum.** Every figure Mankiw states reproduces — the \$1,000 money supply, the multiplier of 10, and the velocity of 20.
>
> **Additions beyond the source.**
>
> - **⚠️ §2b is the chapter's main addition.** **Mankiw derives $1/R$, notes in passing that banks "may hold excess reserves", and never computes what that does.** The formula $(1+c)/(R+e+c)$ and the finding that **the multiplier falls to 1.50 — 15% of textbook — under 2008–14 conditions** are not in the source, and they support the conclusion that **the central bank controls the base rather than the money supply.** *(The 9th-edition text predates the full quantitative-easing experience; the mechanism it describes is what produced the outcome.)*
> - **⚠️ §6's inflation-tax Laffer curve is mine.** **Mankiw describes the inflation tax and hyperinflation qualitatively and gives no revenue function.** Using a standard money demand shows revenue **peaking at 100% inflation and collapsing to 0.05 by 1000%**, which explains *why hyperinflations end* — and connects it to [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]'s Laffer computation as the same curve on a different base. *(Corrected during drafting: my first money-demand assumption was too weak and produced monotonically rising revenue, contradicting the text above it.)*
> - **§4's growth-rate version of the quantity equation** — deriving *inflation = money growth − real growth* and tabulating it — is an addition; Mankiw states the conclusion without the differentiation step.
> - **§7's worked redistribution example** (a 5-point inflation surprise turning a +5.0% real return into 0.0%) is mine; Mankiw makes the point in prose.
> - **The emphasis that neutrality is the *hinge* between the two halves of macro**, and that a reader taking it as unconditional will find [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]] incomprehensible, is my framing.
> - **The boundary notes** — that central-bank *operations* are [[Monetary and Financial Theories/contents/00-Index|Mishkin]]'s and the bank's own balance sheet is [[Commercial Banking/contents/00-Index|Commercial Banking]]'s, with the multiplier as a macro identity belonging here — implement the split recorded in [[00-Index]].
>
> **Deliberately compressed.** **Mankiw ch. 16's history of money** (commodity money, the gold standard, the origins of fiat money, the Fed's institutional structure and the FOMC) is compressed to the definitions and tools; **the institutional detail belongs to [[Monetary and Financial Theories/contents/00-Index|Mishkin]] by the recorded boundary.** **The bank-run and deposit-insurance discussion** is noted only in passing — **[[Commercial Banking/contents/08 - Liquidity and Reserves Management|Commercial Banking ch. 08]] computes it in full**, including the point at which a run makes a solvent bank insolvent. **The extended hyperinflation case studies** are represented by §6's mechanism. **The "money in the POW camp" and cryptocurrency boxes** illustrate §1's functions. **The money-demand and money-market equilibrium diagram** is described rather than reconstructed, since the figure is lost and [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]] needs only the conclusion.

**Previous:** [[11 - Unemployment]] · **Next:** [[13 - Open-Economy Macroeconomics]]
