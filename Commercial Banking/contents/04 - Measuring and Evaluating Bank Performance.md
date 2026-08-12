---
subject: Commercial Banking
chapter: 4
tags: [ds, banking, roe, roa, nim, dupont, efficiency-ratio, ratio-analysis, performance]
source: "Rose & Hudgins, *Bank Management and Financial Services* 9e, ch. 6"
---

# Measuring and Evaluating Bank Performance

**This is the examinable core of the subject**, and it is one identity plus the discipline to use it:

$$\text{ROE} = \text{ROA} \times \frac{\text{Assets}}{\text{Equity}}$$

**§3 is the reason it matters.** Three banks reporting an **identical 12% ROE** turn out to have loss-absorbing capacities of **16.67%, 10.00% and 5.00% of assets** — a **3.3× difference in safety behind the same headline number.**

**So the ratio apparatus is not a scoring system; it is a diagnostic one.** Its purpose is to say *where* a difference comes from — operations or financing, revenue or cost, genuine profit or deferred provisioning ([[03 - Bank Financial Statements|ch. 03]]).

**Balance-sheet figures below are BB&T's real ones**, extracted intact in [[03 - Bank Financial Statements|ch. 03]]. **The income statement did not extract, so those figures are my own and are labelled as such.**

## 📘 Main Knowledge

### 1. The four headline ratios

| | definition | computed |
|---|---|---|
| **ROA** | net income / total assets | **0.582%** |
| **ROE** | net income / equity | **5.962%** |
| **EM** | assets / equity | **10.24×** |
| **NIM** | net interest income / earning assets | **3.840%** |

*(Balance sheet: BB&T's. Income statement: mine — interest income 7 450 000, interest expense 2 180 000, provision 2 811 000, fee income 3 180 000, operating expense 4 260 000, 30% tax, all $ thousands.)*

> [!note] What each one is actually measuring
> **ROA is the operating measure.** It is unaffected by how the bank is financed, so it is the right basis for comparing management performance.
>
> **ROE is the shareholder measure**, and it mixes operations with financing — which is why §2 splits it.
>
> **NIM is the spread**, [[01 - The Financial-Services Industry and Its Regulation|ch. 01]] §4's business model as a ratio. **Its denominator is *earning* assets** — loans, securities and fed funds — not total assets, because cash and premises earn nothing and including them would understate the margin on the assets that work.
>
> **EM is pure financing**, and the link between the other two.

### 2. The ROE decomposition, verified as an identity

**Two-factor:**
$$\text{ROE}=\text{ROA}\times\text{EM}$$
*(Verified: 0.582% × 10.2381 = **5.962%** — exact.)*

**Three-factor (the bank DuPont):**
$$\text{ROE}=\underbrace{\frac{\text{NI}}{\text{Revenue}}}_{\text{profit margin}}\times\underbrace{\frac{\text{Revenue}}{\text{Assets}}}_{\text{asset utilisation}}\times\underbrace{\frac{\text{Assets}}{\text{Equity}}}_{\text{EM}}$$

*(Verified: 9.081% × 6.413% × 10.24 = **5.962%** — exact.)*

> [!note] These are identities, not theories — and that is the point
> **The terms cancel**, so they cannot be false. **Their value is entirely diagnostic**: they say *where* a difference in ROE comes from.
>
> | term | what it reflects |
> |---|---|
> | **profit margin** | expense control and **provisioning** |
> | **asset utilisation** | revenue earned per dollar of assets — pricing and asset mix |
> | **equity multiplier** | **financing only** — nothing to do with operations |
>
> **A bank that improves its ROE by raising the third term has not improved anything about its banking.**

### 3. ⚠️ Why a single ROE cannot rank banks

*(Computed — three banks, all reporting **12.000%** ROE:)*

| bank | ROA | EM | ROE | **loss that wipes out equity** |
|---|---|---|---|---|
| **Alpha** | 2.000% | **6.00×** | 12.000% | **16.67%** |
| Beta | 1.200% | 10.00× | 12.000% | 10.00% |
| **Gamma** | 0.600% | **20.00×** | 12.000% | **5.00%** |

> [!warning] A 3.3× difference in loss-absorbing capacity behind an identical headline
> **Gamma reaches the same return on three-tenths of Alpha's ROA, purely by borrowing more.** A 5% loss on assets ends it; Alpha survives 16.67%.
>
> **This is [[01 - The Financial-Services Industry and Its Regulation|ch. 01]] §2's arithmetic re-expressed: `1/EM` is the fraction of assets the bank can lose.** The identity that produces the return produces the fragility, and it is the same identity.
>
> **So ROE alone is not a performance measure — it is a performance measure and a risk measure multiplied together, with no way to tell which is which.** Always decompose before comparing.

### 4. The efficiency ratio

$$\text{efficiency ratio}=\frac{\text{noninterest expense}}{\text{NII}+\text{noninterest income}}$$

*(Computed: 4 260 000 / 8 450 000 = **50.414%**.)*

**Lower is better** — it is operating cost per dollar of revenue produced. **Roughly 50–70% is the usual US range; below 50% is excellent.**

> [!note] It deliberately excludes the provision
> **So it measures *operating* efficiency separately from *credit* quality.** That separation matters because [[03 - Bank Financial Statements|ch. 03]] showed the provision is a management estimate that can move net income by 47% — **a ratio that mixed the two would be no more reliable than the estimate.**

### 5. Risk ratios — the other half of performance

*(All computed from BB&T's balance sheet:)*

| ratio | value | measures |
|---|---|---|
| equity / assets | **9.767%** | capital adequacy ([[10 - Capital Adequacy and Basel\|ch. 10]]) |
| net loans / assets | **62.502%** | credit exposure |
| **net loans / deposits** | **90.100%** | funding pressure |
| liquid assets / deposits | **30.675%** | liquidity buffer ([[08 - Liquidity and Reserves Management\|ch. 08]]) |
| ALL / gross loans | **2.449%** | loss cushion ([[03 - Bank Financial Statements\|ch. 03]]) |

> [!warning] Profitability and risk ratios must be read together
> **A high ROE alongside a 90% loans-to-deposits ratio and a thin liquidity buffer is not better performance — it is the same performance with more risk.**
>
> **The loans/deposits ratio at 90.1% is the one to notice**: the bank has lent nine-tenths of its deposit base, so further lending must be funded in wholesale markets ([[09 - Managing Deposits and Nondeposit Funding|ch. 09]]) — which is faster to leave when conditions turn.

### 6. The trade-off, made explicit

**Three ways to raise ROE:**
1. **Raise ROA** — a genuine improvement in margin or efficiency.
2. **Raise leverage** — same operations, more risk.
3. **Under-provide** — [[03 - Bank Financial Statements|ch. 03]]'s discretion, worth ~47% of net income, changing nothing real.

*(Computed — the same bank at ROA 1.0%:)*

| EM | ROE | **asset loss that wipes out equity** |
|---|---|---|
| 8× | 8.000% | 12.50% |
| 11× | 11.000% | 9.09% |
| 16× | 16.000% | 6.25% |
| **25×** | **25.000%** | **4.00%** |

> [!note] Every unit of ROE bought with leverage shrinks the loss the bank can absorb
> **The same identity, read from both ends.** Shareholders read down the ROE column; regulators read down the loss column. **Neither is misreading it — they are optimising different things over the same equation**, which is why the level of capital ends up being set by rule rather than by negotiation ([[10 - Capital Adequacy and Basel|ch. 10]]).

### 7. Using a peer comparison

1. **Decompose ROE into ROA × EM** — operations or financing?
2. **Decompose ROA into margin × utilisation** — revenue or cost?
3. **Check the efficiency ratio** — operating cost per revenue dollar.
4. **Check the provision and ALL ratio** — is the profit reserved for?
5. **Check leverage and liquidity** — what risk was taken to earn it?

**R&H's **UBPR** (Uniform Bank Performance Report) exists to do exactly this against a peer group** — because an absolute ratio means little without comparable banks. **A 0.9% ROA is good or poor depending entirely on what similar banks earned that year.**

## ✏️ Exercises

**1. (The ratios.)** (a) What does each headline ratio measure? (b) Why is NIM's denominator earning assets? (c) Verify the decompositions. (d) Why does "identity, not theory" matter?

> [!example]- Solution
> **(a)** **ROA** is the operating measure — net income per dollar of assets, **unaffected by financing**, so it is the right basis for judging management. **ROE** is the shareholder's return and **mixes operations with financing**. **NIM** is the interest spread as a ratio — [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s business model measured. **EM** is pure financing and the link between ROA and ROE.
>
> *(Computed for the worked bank: ROA **0.582%**, ROE **5.962%**, EM **10.24×**, NIM **3.840%**.)*
>
> **(b) Because cash and premises earn nothing, and including them would understate the margin on the assets that actually work.**
>
> **Earning assets = loans + securities + fed funds sold** *(computed: 137 256 563 of BB&T's 165 764 218 total)*. **Roughly 83% of assets earn interest**; the rest is cash, premises, goodwill and foreclosed property.
>
> **So NIM answers "how wide is the spread on the money I have deployed?"** — a management question about pricing and mix. **Dividing by total assets would blend that with a different question**: how much of the balance sheet is deployed at all. **Keeping them separate is what makes NIM diagnostic.**
>
> **(c)** *(Both verified exactly:)*
> ```
> two-factor  : 0.582% x 10.2381               = 5.962%   = ROE
> three-factor: 9.081% x 6.413% x 10.2381      = 5.962%   = ROE
> ```
> **The three-factor version splits ROA into profit margin × asset utilisation** — *how much of each revenue dollar survives to the bottom line* × *how much revenue each asset dollar generates*.
>
> **(d) Because an identity cannot be wrong, so it can never be evidence — only a decomposition.**
>
> **The terms cancel**: $\frac{NI}{Rev}\times\frac{Rev}{A}\times\frac{A}{E}=\frac{NI}{E}$. **There is no claim about the world in it.**
>
> **Which is exactly why it is useful.** It cannot tell you whether a bank is good; **it can tell you, without ambiguity, where a difference between two banks comes from.** If Bank X's ROE exceeds Bank Y's, the identity says the excess must live in the margin, the utilisation, or the leverage — **and there is no fourth possibility.**
>
> **Mistaking it for a theory is the common error.** "ROE = ROA × EM, therefore raising leverage improves performance" treats an accounting truth as a causal one. **The identity says leverage raises ROE; it says nothing about whether that is desirable** — §6 supplies the other half.

**2. (Hard — why ROE misleads.)** (a) Explain the three-bank table. (b) Where does `1/EM` come from? (c) Why does the efficiency ratio exclude the provision? (d) What must accompany any profitability ratio?

> [!example]- Solution
> **(a) Identical returns, radically different fragility.**
>
> *(Computed — all three report **12.000%** ROE:)*
>
> | | ROA | EM | loss that wipes out equity |
> |---|---|---|---|
> | Alpha | 2.000% | 6.00× | **16.67%** |
> | Gamma | 0.600% | 20.00× | **5.00%** |
>
> **Gamma earns three-tenths of Alpha's return on assets and reaches the same ROE purely by borrowing more** — and a **3.3× difference in loss-absorbing capacity** sits behind an identical headline.
>
> **Alpha is the better bank on every operating measure.** It earns more per dollar of assets, which reflects pricing, mix and cost control. **Gamma has bought the appearance of equal performance with risk**, and the purchase is invisible in the single number.
>
> **(b) From `equity/assets` being the reciprocal of the equity multiplier.**
>
> $$\text{EM}=\frac{A}{E}\;\Longrightarrow\;\frac{E}{A}=\frac{1}{\text{EM}}$$
>
> **A loss equal to the equity ratio wipes out the equity** ([[01 - The Financial-Services Industry and Its Regulation|ch. 01]] §2), so **the maximum absorbable loss is exactly `1/EM` of assets.**
>
> *(Verified in §6: EM 8 → 12.50%, EM 11 → 9.09%, EM 25 → **4.00%**.)*
>
> **So the identity that generates the return also generates the fragility, and it is the *same* term doing both.** Raising EM multiplies ROE and divides the safety margin by the same factor. **That symmetry is the whole reason capital is regulated rather than chosen** — the shareholder's optimum and the depositor's are on opposite ends of one equation.
>
> **(c) So that operating efficiency can be judged separately from credit quality.**
>
> *(Computed: 4 260 000 / 8 450 000 = **50.414%**.)*
>
> **[[03 - Bank Financial Statements|Ch. 03]] showed the provision is a management estimate worth ~47% of net income.** A cost ratio that included it would inherit all of that discretion — **a bank could improve its "efficiency" by under-providing, which has nothing to do with efficiency.**
>
> **Excluding it makes the ratio measure what it claims to**: salaries, premises, technology and overhead per dollar of revenue produced. **Those are real, observed cash costs, not estimates.**
>
> **The corollary is that the efficiency ratio must be read alongside the provision, not instead of it.** A bank with a 45% efficiency ratio and a collapsing allowance ratio is not efficient; it is deferring.
>
> **(d) A risk ratio, and a peer group.**
>
> **A risk ratio, because profitability and risk are two readings of one identity** (§6). *(BB&T: equity/assets **9.767%**, loans/deposits **90.100%**, liquid/deposits **30.675%**.)* **The 90% loans-to-deposits ratio is the one that changes the interpretation** — the bank has lent nine-tenths of its deposit base, so growth must come from wholesale funding, which leaves faster in a crisis ([[09 - Managing Deposits and Nondeposit Funding|ch. 09]]).
>
> **And a peer group, because an absolute ratio has no meaning.** A 0.9% ROA is strong in one year and weak in another; a 60% efficiency ratio is good for a branch-heavy retail bank and poor for a wholesale one. **This is what the UBPR is for** — it reports every ratio against a peer group of similar size and business mix.
>
> **The general principle is the vault's usual one: a number without a comparison is not evidence.** [[Data Structures and Algorithms/contents/02 - Algorithm Analysis in Practice|DSA ch. 02]] made the same point about timings — **quote ratios against a baseline, not absolute values.**

**3. (Using the apparatus.)** (a) What are the three ways to raise ROE? (b) How would you tell them apart? (c) Why is the UBPR peer-based? (d) What is this chapter's lesson?

> [!example]- Solution
> **(a)** **Raise ROA** — a genuine improvement in margin, mix or cost. **Raise leverage** — identical operations, more risk (§6). **Under-provide** — [[03 - Bank Financial Statements|ch. 03]]'s estimate, worth ~47% of net income, with nothing real changing.
>
> **Only the first is performance.** The second is a financing decision the shareholder could have made without the bank's help; **the third is not a decision about banking at all.**
>
> **(b) By decomposing, in this order.**
>
> | question | check | what it rules out |
> |---|---|---|
> | operations or financing? | **did ROA rise, or only EM?** | leverage |
> | revenue or cost? | margin vs asset utilisation | mis-attributing a pricing gain to efficiency |
> | real or deferred? | **provision and ALL / gross loans** | under-provisioning |
> | efficient or just lucky? | efficiency ratio, which excludes the provision | credit-quality effects |
> | at what risk? | equity/assets, loans/deposits, liquidity | the cost of the return |
>
> **The order matters.** **ROA first**, because if ROA did not move, nothing operational happened and the remaining questions are moot. **Then the provision**, because a rise in ROA driven by a falling provision is not an improvement either.
>
> **Two banks with identical ROE, ROA and efficiency ratios can still differ entirely in the allowance ratio** — and that is the difference between a well-run bank and one borrowing from next year.
>
> **(c) Because a bank ratio has no absolute standard.**
>
> **Every ratio depends on the year, the rate environment and the business mix.** A 3.8% NIM is strong when rates are low and unremarkable when they are high. **A 60% efficiency ratio is good for a branch-based retail bank and poor for a wholesale lender with few branches**, because the two have entirely different cost structures for the same activity.
>
> **So the UBPR reports each ratio against a peer group of similar size and mix**, which controls for exactly those factors. **The comparison is the measurement**; the raw number is an input to it.
>
> *(This is also why [[02 - Organization, Structure and Market Entry|ch. 02]]'s caution applies: smaller banks "produce a different menu of services", so cross-size comparisons mislead even before leverage is considered.)*
>
> **(d) The ratio apparatus is diagnostic, not evaluative.**
>
> **It cannot tell you which bank is better.** It can tell you, without ambiguity, **where two banks differ** — and that is more useful, because the judgement about which difference matters depends on what you are: a shareholder, a depositor, or a regulator.
>
> **The chapter's three findings all point the same way:**
> - **§3** — identical ROE, **3.3× different fragility**, so the headline number carries two variables at once.
> - **§4** — the efficiency ratio excludes the provision **precisely so that an estimate cannot contaminate a measurement.**
> - **§6** — profitability and risk are **one identity read from two ends**.
>
> **So the discipline is: decompose before comparing, pair every profitability ratio with a risk ratio, and treat any single number as a question rather than an answer.**
>
> **Which is the same conclusion the technical subjects reached by a different route.** [[Database Management Systems/contents/00-Index|DBMS]] found that a query returning a plausible number is not evidence it is right; **here, a bank reporting a good ratio is not evidence it performed well.** In both cases the answer looks fine and the check is cheap.

## 📝 Summary

- **The examinable core is one identity: `ROE = ROA × EM`**, and the discipline to decompose before comparing.
- **Four headline ratios** *(computed: ROA **0.582%**, ROE **5.962%**, EM **10.24×**, NIM **3.840%**)*. **ROA is the operating measure; ROE mixes operations with financing; NIM is the spread; EM is pure financing.**
- **NIM's denominator is *earning* assets** *(137 256 563 of 165 764 218 — about 83%)*, because cash and premises earn nothing.
- **Both decompositions verified exactly**: `ROA × EM` and `profit margin × asset utilisation × EM` each reproduce ROE to the last digit. **They are identities, so they can never be evidence — only diagnosis.**
- **⚠️ Three banks with an identical 12.000% ROE absorb losses of 16.67%, 10.00% and 5.00% of assets** *(computed)* — **a 3.3× difference in fragility behind the same number.**
- **`1/EM` is the fraction of assets a bank can lose** — the same term that multiplies ROE divides the safety margin.
- **The efficiency ratio** *(computed: **50.414%**)* **deliberately excludes the provision**, so operating efficiency is judged separately from [[03 - Bank Financial Statements|ch. 03]]'s 47%-of-income estimate.
- **Risk ratios must accompany profitability ratios** *(BB&T: equity/assets **9.767%**, **loans/deposits 90.100%**, liquid/deposits **30.675%**, ALL/gross loans **2.449%**)*.
- **Three ways to raise ROE: raise ROA (real), raise leverage (risk), under-provide (nothing).** Only the first is performance.
- **⚠️ Every unit of ROE bought with leverage shrinks absorbable loss** *(computed: EM 8 → 12.50%; EM 25 → **4.00%**)*. **Shareholders read the ROE column, regulators read the loss column** — one identity, two optima, which is why capital is set by rule.
- **The UBPR is peer-based because no bank ratio has an absolute standard** — it depends on the year, the rate environment and the business mix.

## ⚠️ Important Notes

1. **⚠️ Never compare banks on ROE alone.** It carries performance and leverage in one number with no way to separate them.
2. **Decompose in order: ROA first.** If ROA did not move, nothing operational happened.
3. **Check the provision before crediting an ROA improvement** — a falling provision raises income without any change in the business ([[03 - Bank Financial Statements|ch. 03]]).
4. **ROA is the management measure**; ROE is the shareholder measure. Use ROA to judge operations.
5. **Use earning assets, not total assets, in NIM** — otherwise you blend spread with deployment.
6. **⚠️ Pair every profitability ratio with a risk ratio.** Equity/assets, loans/deposits and liquidity change the interpretation entirely.
7. **`1/EM` is the maximum absorbable loss.** Compute it whenever leverage is discussed.
8. **Read the efficiency ratio alongside the provision, not instead of it.** Low cost with a collapsing allowance is deferral, not efficiency.
9. **A loans-to-deposits ratio near 90% means further growth is wholesale-funded** — faster to leave in a crisis.
10. **⚠️ An absolute ratio means nothing without a peer group.** Business mix and size make cross-comparisons misleading.
11. **Treat the identity as a decomposition, never as an argument.** "ROE = ROA × EM, so leverage improves performance" mistakes an accounting truth for a causal one.
12. **A single number is a question, not an answer** — the same discipline the technical subjects reached from the other direction.

> [!warning] Gaps in the source material
> **Rose & Hudgins ch. 6 extracts as clean prose** — the profitability formulas, the ROE decomposition discussion, the risk measures and the UBPR material all came through readably. **Book page $n$ = PDF page $n+18$; ch. 6 is PDF pages 185–234.** *(The four standing extraction hazards in `00-Index.md` apply.)*
>
> **⚠️ Exhibit 6-1 — "Elements That Determine the Rate of Return Earned on the Stockholders' Investment (ROE)" — is an image and is lost.** Only its caption survives. **That exhibit *is* the decomposition diagram**, so §2 reconstructs the relationship algebraically and verifies it numerically instead. **This is the graphical-versus-tabular distinction recorded in [[03 - Bank Financial Statements|ch. 03]]**: the flow diagram is gone, while ch. 03's balance-sheet table survived.
>
> **The balance-sheet figures used throughout are BB&T's own**, extracted intact in [[03 - Bank Financial Statements|ch. 03]] and verified there. **The Report of Income did not extract**, so **every income-statement figure in this chapter is my own assumption**, chosen to be plausible for a bank of that size and era, and labelled as such in the program output. **Consequently ROA, ROE, NIM, the efficiency ratio and the decompositions are illustrative in level and exact in relationship** — the identities hold regardless of the inputs, which is the point of §2.
>
> **The risk ratios in §5 are computed entirely from the book's real figures** and are therefore BB&T's actual ratios.
>
> **No error was found in Rose & Hudgins ch. 6.**
>
> **A correction to my own work, made before writing.** §3's program initially reported that a **25.00%** asset loss would wipe out the high-leverage bank's equity. **That is wrong — at EM 20 the figure is 5.00%** — and it contradicted §6's own table, which computes `1/EM` correctly. The line was a garbled expression that happened to produce a plausible number. **It was caught by checking §3 against §6 and fixed**; the corrected output gives 5.00% versus 16.67%, a 3.3× difference. *(A plausible wrong number that contradicts another section of the same output is exactly the failure mode this vault keeps finding — here in my own code.)*
>
> **Additions beyond the source.** **R&H ch. 6 presents the ratios and the decomposition thoroughly — this is the book's strongest chapter. What is added is the verification and the risk framing:**
>
> - **§2 verifies both decompositions numerically** rather than presenting them as formulas. **The insistence that they are *identities and therefore never evidence*** — useful only as diagnosis — is my framing, and it guards against the common misreading in Exercise 1(d).
> - **§3 is the chapter's centrepiece and is mine.** R&H notes that ROE reflects leverage; **constructing three banks with an identical 12% ROE and computing their loss-absorbing capacities (16.67% / 10.00% / 5.00%) turns that into a 3.3× difference you can point at.**
> - **The observation that `1/EM` is the maximum absorbable loss, and that the same term multiplies return and divides safety**, is my own link back to [[01 - The Financial-Services Industry and Its Regulation|ch. 01]] §2 — and it is what makes §6's "one identity, two optima" framing possible.
> - **§4's point that the efficiency ratio excludes the provision *by design*** — so that [[03 - Bank Financial Statements|ch. 03]]'s estimate cannot contaminate an operating measurement — is an addition.
> - **§7's ordered diagnostic checklist**, and Exercise 3(b)'s table of what each check rules out, are mine.
> - **The closing parallel with [[Database Management Systems/contents/00-Index|DBMS]]** — a plausible number is not evidence, in either domain — is a cross-subject addition.
>
> **Deliberately compressed.** **R&H's full catalogue of performance ratios** (dozens, including several tax-adjusted and per-share variants) is reduced to the four headline measures, the efficiency ratio and five risk ratios — **the ones that carry an argument.** The rest are computable from the same statements and add no new insight. **The stock-market measures** (price/earnings, market-to-book, dividend yield) are noted in the source as a "surrogate for stock values" but omitted here: they measure the market's view rather than the bank's performance, and belong with valuation. **The extended UBPR walkthrough** is compressed into §7's rationale — the report's mechanics are jurisdiction-specific and its principle (peer comparison) is the transferable part. **Comparisons with non-bank financial firms** are omitted, consistent with [[03 - Bank Financial Statements|ch. 03]].

**Previous:** [[03 - Bank Financial Statements]] · **Next:** [[05 - Interest-Rate Risk - Gap and Duration]]
