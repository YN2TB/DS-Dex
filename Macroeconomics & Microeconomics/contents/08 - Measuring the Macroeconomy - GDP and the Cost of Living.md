---
subject: Macroeconomics & Microeconomics
chapter: 8
tags: [ds, economics, macroeconomics, gdp, deflator, cpi, inflation, substitution-bias]
source: "Mankiw, *Principles of Macroeconomics* (2017), ch. 10–11"
---

# Measuring the Macroeconomy: GDP and the Cost of Living

**Macroeconomics begins here.** [[07 - Factor Markets and the Theory of Consumer Choice|Chapters 01–07]] studied individual markets; the next seven study the economy as a whole. **And before anything can be explained it has to be measured** — which turns out to be much less straightforward than it sounds.

**Three results.**

**§1 — the operator cipher, caught doing real damage.** Mankiw's GDP table lists net exports as `2532`. *(Computed: read literally the identity fails by **\$3,064 billion** and the US has a trade **surplus**. Decoded as **−532**, **all three columns balance exactly** — the totals, the per-person figures and the percentage shares.)* **That is as strong a confirmation of the cipher as could be asked for.**

**§5 — the substitution bias, measured.** Mankiw describes it and never computes it. *(Computed on his own data: by 2018 the CPI reads **250** against the deflator's **240** — the CPI **overstates cumulative inflation by 4.17%**.)*

**And the reason inflation measurement matters so much: so much is indexed to it.** *(Computed: a 1-point annual overstatement compounds to **10.46%** over a decade.)*

> [!warning] ⚠️ Equations reconstructed, not transcribed — and §1 shows exactly why. See [[00-Index]].

## 📘 Main Knowledge

### 1. ⚠️ The cipher, caught in the act

**Mankiw's Table 1 (US GDP, 2015) extracts like this:**

```
Gross domestic product, Y   $17,938   $55,882   100%
Consumption, C               12,268    38,218    68
Investment, I                 3,018     9,402    17
Government purchases, G       3,184     9,919    18
Net exports, NX                2532    21,657    23
```

**Read literally, $NX = +2{,}532$ and the accounting identity fails:**

$$12{,}268+3{,}018+3{,}184+2{,}532=21{,}002\;\ne\;17{,}938\qquad\textbf{off by 3,064}$$

**Decoded — `2` is a minus sign — every column balances exactly:**

| | | |
|---|---|---|
| **totals** | $12{,}268+3{,}018+3{,}184-532$ | $=\mathbf{17{,}938}$ ✓ |
| **per person** | $38{,}218+9{,}402+9{,}919-1{,}657$ | $=\mathbf{55{,}882}$ ✓ |
| **shares** | $68+17+18-3$ | $=\mathbf{100}$ ✓ |

> [!warning] Three independent columns balance only under the decoding
> **A transcriber reading the table literally would report a \$3,064 billion error and a United States running a trade *surplus*.**
>
> **This is the clearest evidence yet for the cipher recorded in [[00-Index]]**, and it is why the rule for this subject is *never transcribe — reconstruct from prose and verify numerically.* **The identity itself extracts as `Y 5 C 1 I 1 G 1 NX`.**

### 2. What GDP is

$$\textbf{GDP} = \text{the market value of all }\textit{final}\text{ goods and services produced }\textit{within}\text{ a country in a given period}$$

**Every word carries weight:**

| | |
|---|---|
| **market value** | prices are the weights — **unpriced activity is excluded** |
| **final** | intermediate goods are excluded, or they would be counted twice |
| **produced** | not *resold* — a used car is not new production |
| **within** | location, not nationality *(GDP vs GNP)* |
| **given period** | a **flow**, not a stock |

> [!note] GDP is simultaneously total income and total expenditure
> **Every transaction has a buyer and a seller, so one person's spending is another's income.** The two measures are not merely similar; **they are the same sum counted from opposite ends**, which is why the circular-flow diagram closes.
>
> **The identity $Y = C + I + G + NX$ is an accounting identity, not a theory.** It cannot be false and it explains nothing on its own — **it is a bookkeeping frame that later chapters put behaviour into.**
>
> *(One trap worth naming: **investment** in this identity means new **capital** — plant, equipment, inventories, new housing. **Buying shares is not investment** in the GDP sense; it is a transfer of ownership of existing assets.)*

### 3. Real versus nominal GDP

*(Verified — Mankiw's Table 2, an economy of hot dogs and hamburgers:)*

| year | $P_{hd}$ | $Q_{hd}$ | $P_{hb}$ | $Q_{hb}$ | **nominal** | **real (base 2016)** | **deflator** |
|---|---|---|---|---|---|---|---|
| 2016 | \$1 | 100 | \$2 | 50 | **200** | **200** | **100.00** |
| 2017 | \$2 | 150 | \$3 | 100 | **600** | **350** | **171.43** |
| 2018 | \$3 | 200 | \$4 | 150 | **1 200** | **500** | **240.00** |

$$\text{real GDP}=\sum P_{\text{base}}\,Q_t \qquad\qquad \text{GDP deflator}=\frac{\text{nominal}}{\text{real}}\times100$$

> [!warning] Nominal GDP triples while real GDP rises 150%
> *(Computed: 2016→2017 nominal **+200.0%** against real **+75.0%**; 2017→2018 nominal **+100.0%** against real **+42.9%**.)*
>
> **Reporting the nominal figure as "growth" would be badly wrong** — most of it is prices.
>
> **The construction is the point: real GDP holds prices fixed so that only quantities move.** The deflator is then the residual — **whatever nominal GDP did that real GDP did not.** It is a price index derived from the two, not measured separately.

### 4. The consumer price index

**The CPI prices a *fixed basket* of what a typical consumer buys.**

*(Verified — Mankiw's basket of 4 hot dogs and 2 hamburgers:)*

| year | cost of the basket | **CPI (base 2016)** |
|---|---|---|
| 2016 | $(4\times\$1)+(2\times\$2)=\mathbf{\$8}$ | **100.00** |
| 2017 | $(4\times\$2)+(2\times\$3)=\mathbf{\$14}$ | **175.00** |
| 2018 | $(4\times\$3)+(2\times\$4)=\mathbf{\$20}$ | **250.00** |

**Mankiw's five steps: fix the basket → find the prices → compute the basket's cost → choose a base year and index → compute the inflation rate.**

### 5. ⚠️ The substitution bias, computed

**Both indices now exist on the same data, so the gap can be measured rather than described.**

| year | **GDP deflator** | **CPI** | difference | **CPI overstates by** |
|---|---|---|---|---|
| 2016 | 100.00 | 100.00 | 0.00 | — |
| 2017 | **171.43** | **175.00** | 3.57 | **2.08%** |
| 2018 | **240.00** | **250.00** | **10.00** | **4.17%** |

$$\text{deflator}=\frac{\sum P_t Q_t}{\sum P_0 Q_t}\;\text{(current quantities)}\qquad \text{CPI}=\frac{\sum P_t Q_0}{\sum P_0 Q_0}\;\text{(fixed quantities)}$$

> [!warning] The CPI's fixed basket keeps buying the good whose price rose most
> *(Computed: hot-dog prices rose **×3** while quantities rose only **×2**; hamburger prices rose **×2** while quantities rose **×3**.)*
>
> **Consumers shifted toward hamburgers — the good that got relatively cheaper. The CPI's fixed 4:2 basket ignores that and keeps paying for hot dogs.**
>
> **So the CPI measures the cost of an *unchanged basket*, not the cost of an *unchanged standard of living*.** That is the substitution bias, and here it reaches **10 index points — a 4.17% overstatement — in two years.**
>
> **The deflator has the mirror problem**: by using current quantities it understates. **Neither is "right" — they answer different questions**, which is why both are published.

**Mankiw's other three biases all push the same way:**

| bias | mechanism |
|---|---|
| **new goods** | a new product expands choice, but enters the basket late, at its lower mature price — **the early gains are never counted** |
| **quality change** | if a car improves and costs 5% more, that is not 5% inflation. Statisticians adjust, **imperfectly** |
| **outlet substitution** | shifting to cheaper retailers is a real saving a fixed-outlet basket misses |

> [!warning] All four biases point the same way: the CPI overstates inflation
> **US estimates have put the total near 1 percentage point a year**, and this matters far more than a measurement footnote suggests **because so much is indexed to the CPI** — social security payments, tax brackets, wage contracts.
>
> *(Computed: a 1-point annual overstatement compounds to **10.46% over a decade**.)*
>
> **So a technical question about basket construction is also a very large fiscal question**, which is why the 1996 Boskin Commission was politically contentious rather than merely statistical.

**Deflator vs CPI, summarised:**

| | **GDP deflator** | **CPI** |
|---|---|---|
| covers | everything **produced domestically** | what **consumers buy** |
| imports | **excluded** | **included** |
| basket | **changes** automatically | **fixed** |

*(So a rise in the price of imported oil shows up in the CPI and not in the deflator — while a rise in the price of a domestically-produced military aircraft does the reverse.)*

### 6. Correcting for inflation

$$\text{amount in today's dollars}=\text{amount in year }T\text{ dollars}\times\frac{P_{\text{today}}}{P_T}$$

*(Verified — Mankiw's Babe Ruth example: the CPI was **15.2** in 1931 and **237** in 2015, so prices rose by a factor of $237/15.2 = \mathbf{15.59}$ (book: 15.6). Ruth's \$80,000 salary becomes $\$80{,}000\times15.59=\mathbf{\$1{,}247{,}368}$ — the book's "about \$1.2 million".)*

> [!note] Raw historical dollar figures are meaningless
> **Ruth's inflation-adjusted salary is a good income and only a fraction of a modern average player's** — a comparison that is only possible *after* deflating.
>
> **The same logic gives the Fisher equation**, which extracts as `Real interest rate 5 Nominal interest rate 2 Inflation rate`:
>
> $$\textbf{real rate}=\textbf{nominal rate}-\textbf{inflation rate}$$
>
> | nominal | inflation | **real** |
> |---|---|---|
> | 8.0% | 3.0% | **+5.0%** |
> | 5.0% | 5.0% | **0.0%** |
> | 3.0% | 6.0% | **−3.0%** |
>
> **A negative real rate means the lender loses purchasing power while still being paid interest.** Nominal figures hide that entirely — and [[12 - The Monetary System and Inflation|ch. 12]] returns to it.

### 7. What GDP leaves out

- **Leisure** has value and is not counted.
- **Non-market activity** — housework, childcare, volunteering — is excluded, **so a country that marketises childcare records "growth" with no change in what is actually done.**
- The **underground economy** is missed.
- **Environmental quality** is not deducted.
- **Distribution is invisible** — GDP per person is a *mean*, not a median.

> [!note] Not a measure of welfare, but a good measure of the ability to buy it
> **Real GDP per person nonetheless correlates strongly with life expectancy, literacy and almost every other indicator of well-being**, which is why Mankiw's conclusion is the right one: **GDP is not welfare, but it measures the ability to purchase the inputs to welfare.**
>
> **[[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|Ch. 03]]'s caution applies exactly: a number that looks objective rests on choices about what to count.** GDP, the CPI and the deflator are all constructions, and knowing what each one excludes is most of knowing how to use it.

## ✏️ Exercises

**1. (GDP.)** (a) Unpack the definition. (b) Why are income and expenditure equal? (c) Distinguish real from nominal and compute the deflator.

> [!example]- Solution
> **(a) Market value of all final goods and services produced within a country in a period.**
>
> | word | why it is there |
> |---|---|
> | **market value** | prices weight the goods; **unpriced activity is excluded** |
> | **final** | including intermediates would double-count — the steel *and* the car |
> | **produced** | a used car resold is not new production, though the dealer's *service* is |
> | **within** | GDP is geographic; **GNP** is by nationality |
> | **given period** | a **flow** (per year), not a stock |
>
> **⚠️ One trap: "investment" here means new *capital*** — plant, equipment, inventories, new housing. **Buying shares is not investment in this sense**; it transfers ownership of an existing asset and adds nothing to production.
>
> **(b) Because every transaction has two sides.**
>
> **Your spending is someone else's income, necessarily.** GDP can be computed by adding up all spending or all income and **must** give the same answer — they are one sum counted from opposite ends.
>
> **This makes $Y = C + I + G + NX$ an accounting identity, not a theory.** It cannot be false, and **it explains nothing on its own** — it is a frame that later chapters fill with behaviour. *(Confusing an identity with a causal claim is a common error: "government spending is part of GDP, therefore raising G raises Y" assumes the other components hold still, which is precisely what needs arguing.)*
>
> **(c) Real GDP holds prices fixed; the deflator is the residual.**
>
> *(Verified against Mankiw's Table 2: nominal **200 / 600 / 1 200**; real **200 / 350 / 500**; deflator **100 / 171.43 / 240**.)*
>
> $$\text{real GDP}=\sum P_{\text{base}}Q_t\qquad \text{deflator}=\frac{\text{nominal}}{\text{real}}\times100$$
>
> **Nominal GDP moves with both prices and quantities; real GDP moves only with quantities; the deflator is whatever is left over.**
>
> *(Computed: nominal grew **+200.0%** then **+100.0%**, real only **+75.0%** then **+42.9%**. Nominal GDP triples over two years while real output rises 150%.)*
>
> **Reporting nominal growth as "growth" is badly wrong**, and this is why "GDP" in economic discussion almost always means **real** GDP.

**2. (Hard — price indices.)** (a) Construct the CPI. (b) Compute the substitution bias. (c) What are the other biases and why do they matter? (d) When do the CPI and deflator diverge?

> [!example]- Solution
> **(a) Price a fixed basket and index it to a base year.**
>
> *(Verified on Mankiw's basket of 4 hot dogs and 2 hamburgers: **\$8 / \$14 / \$20**, giving a CPI of **100 / 175 / 250**.)*
>
> **The fixed basket is the whole design.** By holding quantities constant, changes in the index reflect only prices — **which is exactly the property that creates the bias in (b).**
>
> **(b) The CPI overstates cumulative inflation by 4.17% in two years.**
>
> | year | deflator | CPI | **overstatement** |
> |---|---|---|---|
> | 2017 | 171.43 | 175.00 | **2.08%** |
> | 2018 | **240.00** | **250.00** | **4.17%** |
>
> $$\text{deflator}=\frac{\sum P_tQ_t}{\sum P_0Q_t}\quad\text{(current }Q\text{)}\qquad\qquad \text{CPI}=\frac{\sum P_tQ_0}{\sum P_0Q_0}\quad\text{(base }Q\text{)}$$
>
> **The mechanism, in this economy:** *(computed)* **hot-dog prices rose ×3 while quantities rose only ×2; hamburger prices rose ×2 while quantities rose ×3.** **Consumers substituted toward the good that got relatively cheaper — and the CPI's fixed 4:2 basket ignores that entirely**, continuing to pay for the good whose price rose most.
>
> **So the CPI measures the cost of an unchanged *basket*, not the cost of an unchanged *standard of living*.** A consumer who substitutes is better off than the index says.
>
> **⚠️ And the deflator has the opposite bias** — using current quantities, it implicitly assumes consumers were always buying the new basket, so it *understates*. **Neither index is correct; they answer different questions, which is why both are published.**
>
> **(c) Three more, all pushing the same way — and the stakes are fiscal.**
>
> | bias | why it overstates |
> |---|---|
> | **new goods** | a new product raises welfare by expanding choice but enters the basket late, at its mature (lower) price — **the early gains are never counted** |
> | **quality change** | a better car costing 5% more is not 5% inflation; adjustment is attempted and imperfect |
> | **outlet substitution** | moving to cheaper retailers is a real saving the fixed-outlet basket misses |
>
> **All four biases push in the same direction: the CPI overstates inflation, by an estimated ~1 percentage point a year in the US.**
>
> **This is not a footnote, because so much is indexed to the CPI** — social security, tax brackets, many wage contracts. *(Computed: **1 point compounded over a decade is 10.46%**.)* **A statistical question about basket construction is therefore a very large fiscal question**, which is why the Boskin Commission was politically contested rather than merely technical.
>
> **(d) Whenever imports move, or the composition of output shifts.**
>
> | | deflator | CPI |
> |---|---|---|
> | covers | everything **produced domestically** | what **consumers buy** |
> | **imports** | **excluded** | **included** |
> | basket | **changes** with output | **fixed** |
>
> **A rise in imported oil prices shows up in the CPI and not the deflator.** A rise in the price of a domestically-built military aircraft does the reverse — it is in GDP but nobody's consumption basket.
>
> **In practice the two track each other closely**, and the divergences are informative: **a gap usually means either an import-price shock or a large shift in the composition of output.**

**3. (Corrections and limits.)** (a) Compare across time. (b) What is the real interest rate? (c) What does GDP miss, and does that make it useless?

> [!example]- Solution
> **(a) Multiply by the ratio of price levels.**
>
> $$\text{today's dollars}=\text{year-}T\text{ dollars}\times\frac{P_{\text{today}}}{P_T}$$
>
> *(Verified: CPI **15.2** in 1931 and **237** in 2015, a factor of **15.59**; Babe Ruth's \$80,000 becomes **\$1,247,368** — Mankiw's "about \$1.2 million".)*
>
> **Raw historical dollar figures are meaningless without this**, and the correction changes the conclusion completely: Ruth's salary looks enormous for 1931 and is a fraction of a modern average player's.
>
> **(b) The nominal rate minus inflation — and it can be negative.**
>
> $$\text{real rate}=\text{nominal rate}-\text{inflation rate}$$
>
> | nominal | inflation | real |
> |---|---|---|
> | 8% | 3% | **+5%** |
> | 5% | 5% | **0%** |
> | **3%** | **6%** | **−3%** |
>
> **A negative real rate means the lender is being paid interest and losing purchasing power.** The nominal figure conceals that completely.
>
> **This is the distinction that makes [[12 - The Monetary System and Inflation|ch. 12]] possible**, and it is also why [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|Commercial Banking]]'s interest-rate analysis is conducted in nominal terms while its *economic* interpretation requires the real rate.
>
> **(c) A great deal — and no, it remains the best single number available.**
>
> **GDP omits leisure, non-market production, the underground economy, environmental damage, and all distributional information.** *(A country that shifts childcare from homes to the market records "growth" with no change in what is actually done — a genuine defect, not a quibble.)*
>
> **But real GDP per person correlates strongly with life expectancy, literacy, and nearly every other well-being measure.** So Mankiw's formulation is right: **GDP is not a measure of welfare; it is a good measure of the *ability to purchase the inputs to* welfare.**
>
> **The honest position is neither "GDP is everything" nor "GDP is meaningless"** — it is that **a number which looks objective rests on choices about what to count**, and knowing those choices is most of knowing how to use it. **[[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|Ch. 03]] made exactly this point about deadweight loss**, and [[04 - Externalities, Public Goods and Common Resources|ch. 04]] about surplus. **It is the same caution three times.**

## 📝 Summary

- **⚠️ The operator cipher caught doing real damage**: Mankiw's `NX 2532` is **−532**. *(Computed: read literally the identity fails by **\$3,064 bn** and the US shows a trade surplus; decoded, **all three columns balance exactly** — totals, per person and shares.)*
- **GDP = market value of all *final* goods and services produced *within* a country in a period.** Every word is load-bearing; **investment means new capital, not buying shares.**
- **GDP is total income and total expenditure simultaneously** — one sum from two ends. **$Y = C+I+G+NX$ is an accounting identity, not a theory.**
- **Real GDP holds prices at base-year levels; the deflator is nominal/real × 100** *(verified: nominal **200/600/1200**, real **200/350/500**, deflator **100/171.43/240**)*.
- **⚠️ Nominal GDP triples while real GDP rises 150%** *(computed: nominal **+200.0%** then **+100.0%**; real **+75.0%** then **+42.9%**)*. "GDP" in economics means **real** GDP.
- **The CPI prices a fixed basket** *(verified: **\$8 / \$14 / \$20** → CPI **100 / 175 / 250**)*.
- **⚠️ The substitution bias, measured on the same data: the CPI reads 250 against the deflator's 240 — a 4.17% overstatement in two years.** *(Mechanism: hot-dog prices ×3 with quantities ×2; hamburger prices ×2 with quantities ×3 — consumers substituted and the fixed basket ignored it.)*
- **The CPI measures the cost of an unchanged *basket*, not an unchanged *standard of living*.** The deflator has the mirror bias — **neither is right; they answer different questions.**
- **All four CPI biases push the same way** — substitution, new goods, quality change, outlet substitution — **for an estimated ~1 point a year.**
- **⚠️ That is a fiscal question, not a footnote**, because so much is indexed to it *(computed: **10.46%** compounded over a decade)*.
- **Deflator vs CPI: the deflator covers domestic *production* and excludes imports; the CPI covers *consumption* and includes them.** A gap usually signals an import-price shock or a compositional shift.
- **Correct across time by multiplying by $P_{\text{today}}/P_T$** *(verified: Babe Ruth's \$80,000 in 1931 = **\$1,247,368** in 2015 dollars)*.
- **Real rate = nominal rate − inflation, and it can be negative** — the lender is paid interest and loses purchasing power.
- **GDP omits leisure, non-market production, the underground economy, environmental damage and all distribution.** **It is not welfare; it measures the ability to purchase the inputs to welfare** — and it correlates strongly with every other well-being measure.

## ⚠️ Important Notes

1. **⚠️ Never transcribe a number from this book.** §1 shows a literal reading producing a \$3,064 bn error and the wrong sign on the trade balance.
2. **Check that a table's rows and columns *sum*.** Three independent balances confirmed the decoding here.
3. **Only *final* goods count.** Intermediates would be double-counted.
4. **⚠️ "Investment" means new capital, not financial purchases.**
5. **$Y = C+I+G+NX$ is an identity.** It cannot be false and it explains nothing by itself.
6. **⚠️ "GDP" means *real* GDP** in any discussion of growth.
7. **The deflator is derived from nominal and real GDP**, not measured independently.
8. **⚠️ The CPI's fixed basket creates substitution bias** — it prices an unchanged basket, not an unchanged living standard.
9. **The deflator's changing basket biases the other way.** Neither index is correct.
10. **⚠️ All four CPI biases push upward**, totalling roughly a point a year.
11. **Indexation makes the bias fiscally enormous** — 10.46% over a decade.
12. **⚠️ Imports are in the CPI and not the deflator.** That is the usual reason they diverge.
13. **Always deflate before comparing across time.** Raw historical dollars mean nothing.
14. **⚠️ Real rates can be negative** — nominal figures hide it.
15. **GDP is not welfare**, but it is not useless either; know what it excludes.
16. **A number that looks objective rests on choices about what to count** — the same caution as [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]'s deadweight loss.

> [!warning] Gaps in the source material
> **Mankiw's prose extracts cleanly and the outline located both chapters** *(Macro 2017, PDF pp. 220–261)*. **Per the deduplication rule in [[00-Index]], macro chapters 10–23 come from the Macro 2017 volume — so the source switches back here as the macro half begins.**
>
> **⚠️ BOTH TABLES SURVIVED EXTRACTION COMPLETELY** — Table 1 (GDP and its components, all three columns) and Table 2 (prices, quantities, nominal, real and the deflator for all three years), as did ch. 11's CPI basket calculation. **That is now six Mankiw tables extracted whole across this subject**, confirming the settled rule: **graphical exhibits are lost; numeric tables set as text survive.**
>
> **⚠️ THE OPERATOR CIPHER IS AT ITS MOST DANGEROUS IN THIS CHAPTER, and §1 documents it.** Table 1's net-exports row reads `2532`, `21,657` and `23` — all three are **negative** numbers with the minus rendered as `2`. **The confirmation is unusually strong: three independent columns balance to the stated totals only under the decoding.** *(A literal transcription gives a \$3,064 billion discrepancy and reverses the sign of the US trade balance.)* **See [[00-Index]] for the full cipher table.**
>
> **⚠️ Every figure is lost**, including the GDP-components pie chart, the real-versus-nominal GDP time series, the CPI history, and the inflation-rate comparison of the two indices. **What survives is captions and axis tick values.**
>
> **No erratum.** Every figure Mankiw tabulates or states reproduces exactly *(nominal 200/600/1200, real 200/350/500, deflator 100/171/240, basket \$8/\$14/\$20, the 15.6 price-level factor, and the "about \$1.2 million" Ruth figure)*.
>
> **Additions beyond the source.**
>
> - **⚠️ §5 is the chapter's main addition.** **Mankiw defines the CPI in ch. 11 and the deflator in ch. 10, describes the substitution bias qualitatively, and never computes both indices on the same data.** Doing so gives **250 against 240 by 2018 — a 4.17% overstatement** — and shows the mechanism explicitly (prices ×3 with quantities ×2 for the good the fixed basket over-weights). **The observation that the deflator has the mirror bias, so neither index is "right", is also an addition.**
> - **⚠️ §1's documentation of the cipher failure is mine**, and it is included because it is simultaneously the best available *evidence* for the cipher and the clearest demonstration of *why the rule matters*. The three-column balance check is the verification.
> - **The compounding calculation** showing a 1-point annual bias reaching **10.46%** over a decade — turning a statistical footnote into a fiscal magnitude — is an addition.
> - **§2's warning that $Y = C+I+G+NX$ is an identity rather than a theory**, and that "government spending is part of GDP therefore raising G raises Y" smuggles in an assumption, is mine. *(It matters for [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve|ch. 14]].)*
> - **§6's link between the Fisher equation and [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|Commercial Banking]]'s nominal-terms analysis** is my cross-subject connection.
> - **§7's framing that GDP, the CPI and the deflator are all constructions whose exclusions must be known** — the same caution as [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade|ch. 03]]'s deadweight loss and [[04 - Externalities, Public Goods and Common Resources|ch. 04]]'s surplus — is mine.
>
> **Deliberately compressed.** **Mankiw's detailed treatment of the four GDP components** (the sub-categories of consumption and investment, the treatment of government transfers) is compressed to the definitions plus the investment trap; the detail is national-accounting convention. **The "other measures of income"** (GNP, NNP, national income, personal income, disposable personal income) are noted only as GDP-vs-GNP — the distinctions are accounting refinements that move together in practice. **The extended case studies** (international differences in GDP and quality of life; the shopping-basket composition chart; the Boskin Commission history) are represented by their analytical content. **The magnitude of the CPI's individual biases** is not decomposed further, since the source gives only the aggregate estimate. **Indexation mechanics and the history of real-wage measurement** are noted in §5 rather than developed.

**Previous:** [[07 - Factor Markets and the Theory of Consumer Choice]] · **Next:** [[09 - Production and Growth]]
