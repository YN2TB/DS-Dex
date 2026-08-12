---
subject: Commercial Banking
chapter: 2
tags: [ds, banking, consolidation, economies-of-scale, holding-companies, diversification, branching]
source: "Rose & Hudgins, *Bank Management and Financial Services* 9e, ch. 3–4"
---

# Organization, Structure and Market Entry

**The US had about 14 000 commercial banks in the mid-1980s and about 6 600 by the book's edition.** More than half the industry's firms disappeared in a generation, while the industry itself grew.

**The obvious explanation is economies of scale — and the book's own evidence does not support it.** §3 reports R&H's finding that banks anywhere from **$100 million to $25 billion** in assets can be at or near least-cost size: **a 250× span**. If a $500 million bank and a $25 billion bank have broadly similar unit costs, scale cannot be why one buys the other.

**§5 tests the other standard justification — geographic diversification — and finds it conditional.** Merging two banks whose earnings move together reduces risk by *nothing*, which is exactly what R&H reports Levonian and Rose found: **crossing a state line is not diversification.**

## 📘 Main Knowledge

### 1. The scale of the change

*(Computed from the book's bank counts:)*
```
14,000 -> 6,600 over ~27 years
compound annual change = -2.75% per year
at that rate the count halves every 25 years
```

**This is steady attrition, not a single event** — roughly one bank in forty disappeared every year for a generation.

**And the industry grew while the count fell**, so the average bank is several times larger. **Consolidation is a change in *structure*, not a contraction.**

### 2. The organisational forms

| | what it is |
|---|---|
| **independent bank** | one bank, one charter, no parent |
| **bank holding company (BHC)** | a parent corporation that *owns* one or more banks |
| **financial holding company (FHC)** | a BHC permitted (post-1999) to own securities and insurance affiliates too |

> [!note] The holding company is a legal device, and it is why the change happened
> **It let a banking organisation cross state lines and enter other businesses while each bank kept its own charter and its own capital requirement** ([[10 - Capital Adequacy and Basel|ch. 10]]).
>
> **So "the number of banks fell" and "the number of banking *organisations* fell" are different statements**, and the second fell faster: many charters were absorbed into holding companies before being converted into branches. **Branches replaced charters.**
>
> **When reading any statistic about bank numbers, check which is being counted.**

### 3. ⚠️ Do economies of scale explain consolidation?

**R&H's reported finding:**
- the average cost curve is **roughly U-shaped**,
- **but with a fairly flat middle portion**,
- small and mid-size banks reach lowest cost somewhere between **$100 million and $500 million or $1 billion** in assets,
- larger banks reach lowest cost between **$2 billion and $25 billion**.

*(Computed from those ranges: the span from the smallest to the largest "efficient" size is **250×**.)*

> [!warning] A 250× range of sizes is near-optimal, so scale cannot be the main driver
> **If a $500 million bank and a $25 billion bank have broadly similar unit costs, cost is not why one acquires the other.**
>
> **The flat middle is the important part of the finding**, and it is easy to lose: a U-shaped curve *sounds* like it implies an optimal size, but a U with a long flat bottom implies almost the opposite — **that size is nearly irrelevant over the range most banks occupy.**
>
> **Note the claim is about *average cost*, not profit.** A larger bank may still earn more — §4 considers why.

### 4. Four candidate explanations

| explanation | what it predicts if true |
|---|---|
| **scale economies** | merged unit costs fall — **weak evidence** (§3) |
| **deregulation** | consolidation follows law changes — **strong** |
| **risk diversification** | geographic spread lowers earnings volatility — **conditional** (§5) |
| **expense preference** | managers maximise *size*, not profit; ROE need not improve |

> [!note] Deregulation is the explanation with the clearest evidence
> **The Riegle-Neal Interstate Banking and Branching Efficiency Act of 1994** removed the legal barriers to interstate banking. **Consolidation followed the removal of a constraint** — which means the pre-1994 structure was an artefact of law, not of efficient scale.
>
> **Expense preference** is the uncomfortable one: managers may pursue size because pay and status track it, even when shareholders gain nothing. **It predicts mergers that raise assets without raising ROE** — and [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s identity says that is testable: if ROE rose only because leverage rose, no efficiency was created.

### 5. ⚠️ Geographic diversification is conditional on correlation

**Merging two banks of equal size, each with earnings volatility $\sigma$:**

$$\sigma_{\text{combined}}=\sigma\sqrt{\tfrac{1+\rho}{2}}$$

*(Computed, with $\sigma = 2\%$ of assets:)*

| correlation $\rho$ | combined SD | **risk reduction** |
|---|---|---|
| **+1.00** | 0.0200 | **0.0%** |
| +0.90 | 0.0195 | 2.5% |
| +0.70 | 0.0184 | 7.8% |
| +0.50 | 0.0173 | 13.4% |
| +0.00 | 0.0141 | 29.3% |
| −0.30 | 0.0118 | 40.8% |

> [!warning] Merging two banks whose earnings move together reduces risk by nothing
> **At $\rho = 1$ the reduction is exactly zero**, and at $\rho = 0.9$ it is 2.5% — negligible.
>
> **Two banks in adjacent states with the same industries and the same weather have a high correlation.** So expanding across a state line into a similar economy achieves almost nothing.
>
> **This is precisely what R&H reports from Levonian and Rose:** risk reduction *"does not occur automatically simply because a banking organization crosses state lines"* — a bank must **enter a number of different regions and be selective about which states it enters.**
>
> **This is [[Probability Theory/contents/00-Index|Probability Theory]]'s portfolio variance applied to a banking organisation** rather than a securities portfolio. **The mathematics is identical, and so is the conclusion: diversification is about correlation, not about count.**

### 6. What this means for reading a merger

1. **A bigger bank is not automatically a lower-cost bank** (§3).
2. **A geographically spread bank is not automatically a safer one** (§5).
3. **So when a merger is justified by "scale" or "diversification", ask which, and ask for the correlation.**
4. **And [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s identity still applies**: a higher post-merger ROE may be leverage rather than efficiency, since $\text{ROE} = \text{ROA}\times\text{EM}$.

## ✏️ Exercises

**1. (Structure and scale.)** (a) Distinguish the three organisational forms. (b) Why do bank counts mislead? (c) What does the flat middle mean? (d) Why is that surprising?

> [!example]- Solution
> **(a)** An **independent bank** has one charter and no parent. A **bank holding company** is a parent corporation owning one or more banks — the banks keep their charters and their own capital requirements. A **financial holding company** is a BHC permitted since 1999 to own securities and insurance affiliates.
>
> **The holding company exists to do what a bank legally could not**: hold banks in several states, and later hold non-banking businesses. **It is a regulatory workaround that became the standard structure.**
>
> **(b) Because a bank can disappear as a charter without disappearing as a business.**
>
> When a holding company converts an acquired bank into a **branch**, the charter count falls by one and nothing about the offices, staff or customers necessarily changes. **So "14 000 → 6 600 banks" overstates the disappearance of institutions and understates the growth of branches.**
>
> **Three different counts move differently**: banks (charters), banking organisations (holding companies), and banking offices (branches). **The first fell fastest and the last rose.**
>
> **Always check which is being counted** — a claim that "half the banks disappeared" is true of charters and misleading about access to banking.
>
> **(c) That a very wide range of sizes is nearly equally efficient.**
>
> *(From R&H's own ranges: least cost for small/mid banks at $100mn–$1bn, for large banks at $2bn–$25bn — computed span **250×**.)*
>
> **A U-shaped curve with a flat bottom is almost the opposite of what "U-shaped" suggests.** A sharp U implies one optimal size and a penalty for deviating; **a flat-bottomed U implies size barely matters over the range most banks occupy.**
>
> **So the cost evidence does not support scale as the driver of consolidation**, which is why §4 has to look elsewhere.
>
> **(d) Because "bigger is cheaper" is the default assumption about every industry.**
>
> Banking has obvious fixed costs — branch networks, core systems, compliance, regulatory reporting — **and fixed costs normally produce falling average costs.** The intuition is not silly; it is just not what the cost studies find beyond a fairly modest size.
>
> **The likely reason is that banking's costs are not mostly fixed.** Beyond the systems layer, the dominant costs are **credit evaluation and relationship management**, which scale roughly with the number of loans rather than being spread over them. **A bank twice the size needs roughly twice the loan officers.**
>
> *(And R&H notes smaller banks produce a **different menu of services** from larger ones, so the two are not strictly comparable — which is a reason to be cautious about the comparison in either direction.)*

**2. (Hard — diversification.)** (a) Derive the two-bank result. (b) What does $\rho = 1$ mean? (c) Explain the Levonian and Rose finding. (d) What does this imply for merger analysis?

> [!example]- Solution
> **(a)** For two equal-weight banks with equal volatility $\sigma$:
> $$\sigma^2_{\text{combined}}=\left(\tfrac12\right)^2\sigma^2+\left(\tfrac12\right)^2\sigma^2+2\left(\tfrac12\right)\left(\tfrac12\right)\rho\sigma^2=\frac{\sigma^2(1+\rho)}{2}$$
> $$\sigma_{\text{combined}}=\sigma\sqrt{\frac{1+\rho}{2}}$$
>
> *(Verified numerically at $\sigma=2\%$: $\rho=1 \to 0.0200$; $\rho=0 \to 0.0141$; $\rho=-0.3 \to 0.0118$.)*
>
> **This is [[Probability Theory/contents/00-Index|portfolio variance]] with two assets** — identical mathematics, different application. **The banking organisation *is* a portfolio of regional earnings streams.**
>
> **(b) That the two banks' earnings move identically, so combining them changes nothing.**
>
> *(Verified: risk reduction is exactly **0.0%** at $\rho = 1$.)*
>
> **The combined bank is twice as large and exactly as volatile *per dollar of assets*.** It has more absolute earnings and proportionally more absolute variation.
>
> **And this is not a hypothetical extreme.** Two banks lending to the same industry, in the same region, exposed to the same interest rates and the same property market, **can easily be correlated at 0.8–0.9 — where the reduction is under 8%.**
>
> **The intuition that "more markets is safer" quietly assumes low correlation**, and that assumption is usually not stated, let alone tested.
>
> **(c) That crossing a state line is not, by itself, diversification.**
>
> R&H reports that risk reduction *"does not occur automatically simply because a banking organization crosses state lines"*, and that to achieve any reduction a bank must **expand into a number of different regions and be selective about which states it enters.**
>
> **The arithmetic in (a) explains exactly why.** A state line is a legal boundary, not an economic one. **Two adjacent states may share an industry base, a labour market, a property cycle and a climate** — so their banks' earnings are highly correlated and the merger buys almost nothing.
>
> **"Selective" is the operative word**: the benefit comes from choosing *economically dissimilar* regions, which is a much harder thing to do than simply expanding.
>
> **(d) Ask for the correlation, and treat "diversification" as a claim requiring evidence.**
>
> **A merger justified by diversification is making a quantitative claim** — that combined earnings will be less volatile per dollar — **and §5 shows the claim is false unless correlation is low.**
>
> **What to ask for:**
> 1. **The correlation of the two banks' historical earnings**, not the number of states.
> 2. **Whether the loan portfolios overlap by industry**, which usually matters more than geography.
> 3. **Whether the diversification survives a stress scenario** — correlations rise in crises, so the benefit is smallest exactly when it is needed. *(2008 is the standard illustration: regional property markets that had looked independent fell together.)*
>
> **And the same discipline applies to the cost claim** (§3): "scale" and "diversification" are the two standard justifications for a merger, **and the book's own evidence makes both conditional.**

**3. (Explanations and reading.)** (a) Which explanation has the strongest evidence? (b) What is expense preference and how would you test it? (c) How does ch. 01's identity help? (d) What should you take away?

> [!example]- Solution
> **(a) Deregulation.**
>
> **The Riegle-Neal Act of 1994 removed the legal barriers to interstate banking, and consolidation followed.** That is a clean before-and-after, and it does not require assuming any efficiency gain.
>
> **The implication is worth stating: the pre-1994 structure was an artefact of law, not of efficient scale.** The US had far more banks than comparable economies because branching was legally restricted — **so the "excess" of banks was a regulatory outcome, and its removal was a correction rather than an improvement in efficiency.**
>
> **This also explains why §3's cost evidence can be weak while consolidation is rapid.** The industry was not moving toward a lower-cost size; **it was moving toward the structure it would have had all along without the restriction.**
>
> **(b) The hypothesis that managers maximise size rather than profit, because pay, status and security track size.**
>
> **It predicts mergers that increase assets without increasing shareholder returns.**
>
> **How to test it, in increasing order of rigour:**
> 1. **Compare post-merger ROE with pre-merger ROE** for the combined entity. Expense preference predicts no improvement.
> 2. **Decompose that ROE** (see (c)) — if it rose, check whether ROA rose or only leverage.
> 3. **Compare cost ratios**, since a genuine efficiency gain should show up in the efficiency ratio ([[04 - Measuring and Evaluating Bank Performance|ch. 04]]).
> 4. **Look at acquirer share prices on announcement** — if the market expects value destruction, it says so immediately.
>
> **It is a serious hypothesis, not cynicism**, and it is the standard principal–agent problem: the decision-maker's incentives are not the owner's. **R&H raises it precisely because the scale evidence is weak** — if scale does not explain the mergers, something must.
>
> **(c) It separates operating improvement from financial engineering.**
>
> $$\text{ROE} = \text{ROA} \times \text{EM}$$
>
> **A merged bank reporting a higher ROE has not necessarily become more efficient.** If the combination raised leverage — for instance by using the acquired bank's capacity — **ROE rises with no change in operating performance at all.**
>
> *(From [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]: 1% ROA gives 4% ROE at EM 4 and **20% at EM 20**. The entire difference is financing.)*
>
> **So the diagnostic is simple: did ROA improve?** ROA is the operating measure and is unaffected by capital structure. **If ROE rose and ROA did not, the merger created leverage, not efficiency** — and leverage was available without buying anything.
>
> **(d) Both standard justifications for consolidation are conditional, and the conditions are testable.**
>
> | claim | condition | how to check |
> |---|---|---|
> | "scale will lower costs" | you are below the flat middle | where are both banks in the $100mn–$25bn range? |
> | "this diversifies us" | correlation is low | what is the earnings correlation, not the state count? |
> | "returns improved" | ROA rose, not just EM | decompose the ROE |
>
> **The transferable habit is the vault's usual one: a plausible general claim, checked against the specific numbers.** [[Data Structures and Algorithms/contents/00-Index|DSA]] found textbook complexity claims that measurement complicated; **here the book's own cited research complicates the industry's standard rationale**, and the arithmetic of §5 shows exactly when it fails.

## 📝 Summary

- **US commercial banks fell from ~14 000 to ~6 600** — *(computed: **−2.75% per year**, halving every 25 years)*. **Steady attrition, not one event**, and the industry grew while the count fell.
- **Three organisational forms: independent bank, bank holding company, financial holding company.** The BHC is a **legal device** that allowed interstate expansion while each bank kept its charter and capital requirement.
- **⚠️ So bank counts mislead**: charters fell fastest, branches rose. **Check which is being counted.**
- **⚠️ Scale does not explain consolidation.** R&H reports a **U-shaped cost curve with a flat middle**, with least-cost sizes from **$100mn to $25bn** — *(computed: a **250× span**)*. **A flat-bottomed U means size barely matters over the range most banks occupy.**
- **Likely reason: banking's costs are not mostly fixed** — credit evaluation and relationship management scale with the number of loans.
- **Four candidate explanations**: scale (weak), **deregulation (strongest)**, diversification (conditional), expense preference (testable).
- **Riegle-Neal (1994) removed the legal barrier and consolidation followed** — implying the pre-1994 structure was **an artefact of law, not of efficient scale.**
- **⚠️ Diversification depends entirely on correlation**: $\sigma_{\text{comb}}=\sigma\sqrt{(1+\rho)/2}$. *(Verified: **0.0% reduction at $\rho=1$**, 2.5% at 0.9, 29.3% at 0.)*
- **This is exactly R&H's cited finding** that risk reduction *"does not occur automatically simply because a banking organization crosses state lines"* — a bank must enter **different** regions and be **selective**.
- **It is [[Probability Theory/contents/00-Index|portfolio variance]] applied to a banking organisation** — diversification is about correlation, not count.
- **When a merger is justified by scale or diversification, ask which and ask for the correlation** — and check whether post-merger **ROA** rose, since a higher ROE may be leverage ([[01 - The Financial-Services Industry and Its Regulation|ch. 01]]).

## ⚠️ Important Notes

1. **Check whether a statistic counts charters, organisations or offices.** They moved in different directions.
2. **⚠️ Do not assume bigger banks are cheaper.** The least-cost range spans 250×, so most banks are near-optimal already.
3. **A U-shaped cost curve with a flat bottom means size is nearly irrelevant over the usual range** — the opposite of what "U-shaped" suggests.
4. **Remember banking's costs scale with the number of *loans*, not just with assets** — which is why fixed-cost intuition misleads here.
5. **⚠️ Diversification is about correlation, not the number of markets.** At $\rho = 0.9$ the benefit is under 8%.
6. **Adjacent regions are usually highly correlated** — same industries, same property cycle. Expanding nearby diversifies least.
7. **Correlations rise in a crisis**, so measured diversification benefits are smallest exactly when they are needed.
8. **Ask for the earnings correlation, not the state count**, whenever diversification is claimed.
9. **Test an efficiency claim on ROA, not ROE.** ROA is unaffected by capital structure; ROE is not.
10. **Take expense preference seriously as a hypothesis** — it is the standard principal–agent problem, and it is testable on post-merger ROA and efficiency ratios.
11. **Deregulation explains more than efficiency does.** When structure changes rapidly, look for a constraint that was removed.

> [!warning] Gaps in the source material
> **Rose & Hudgins chapters 3–4 extract as clean prose** — the organisational forms, the Riegle-Neal discussion, the efficiency and scale-economy research summary, and the branching/entry material all came through readably. **Book page $n$ = PDF page $n+18$; ch. 3–4 are PDF pages 83–146.** *(The four standing extraction hazards recorded in `00-Index.md` all apply — watermark, comma-for-hyphen, unusable outline, slow whole-file scans.)*
>
> **⚠️ All exhibits are images and are lost**, including **Exhibit 3-10, "The Most Efficient Sizes for Banks and Selected Other Financial Firms"** — the cost curve itself. **Only its caption survives.** The numerical ranges quoted in §3 come from the surrounding *prose*, which does state them explicitly.
>
> **This chapter contains a correction I made to my own work before writing.** I first drew an illustrative U-shaped cost curve to accompany §3. **Its parameters made small banks appear 300% above minimum cost — which contradicts the flat-middle finding the curve was supposed to illustrate.** Rather than tune invented parameters until they agreed with the conclusion, **the curve was removed entirely** and the point is made from R&H's own stated ranges, which need no fabricated data. *(Tuning a fabricated illustration to match a claim would have been the worst available option: it would look like evidence and be none.)*
>
> **Similarly, the total-asset figures in §1's average-size calculation are my own illustrative assumptions and are labelled as such in the output** — only the bank counts (14 000 and 6 600) are the book's.
>
> **No error was found in Rose & Hudgins ch. 3–4.**
>
> **Additions beyond the source.** **R&H ch. 3–4 is largely descriptive and institutional: the forms of organisation, the history of branching law, and a survey of the research literature. The analysis is added:**
>
> - **§1's compound-rate calculation is mine** — turning "14 000 → 6 600" into **−2.75% per year, halving every 25 years** makes it a trend rather than an anecdote.
> - **§3's central argument is mine.** R&H reports the U-shaped curve with a flat middle and the least-cost ranges; **computing the 250× span and drawing the conclusion that scale therefore cannot be the main driver of consolidation is an inference the book does not make explicitly.** The observation that **a flat-bottomed U is almost the opposite of what "U-shaped" implies** is my own, as is the suggested reason (credit evaluation scales with loan count).
> - **§5's correlation table is entirely mine.** R&H cites Levonian and Rose for the finding that crossing state lines does not automatically reduce risk; **deriving $\sigma\sqrt{(1+\rho)/2}$ and computing that the benefit is 0.0% at $\rho=1$ and 2.5% at $\rho=0.9$ shows *why*** — and connects it to [[Probability Theory/contents/00-Index|portfolio variance]], which the book does not.
> - **§4's "what each explanation predicts" framing, and §6's checklist for reading a merger**, are additions — as is the point in Exercise 3(c) that **a post-merger ROE improvement should be tested on ROA**, which applies [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s identity as a diagnostic.
> - **Exercise 2(d)'s observation that correlations rise in a crisis** — so diversification benefits are smallest when most needed — is an addition.
>
> **Deliberately compressed.** **R&H ch. 4 (establishing new banks, branches, ATMs, telephone services and websites)** is reduced to §2's organisational forms and the entry discussion: **the chartering process is jurisdiction-specific and procedural**, and the delivery-channel material (ATMs, telephone banking, early websites) has dated badly in a book of this vintage. **The detailed history of US branching law** — unit banking, McFadden, Douglas Amendment, and the state-by-state path to Riegle-Neal — is summarised as "deregulation" in §4; it is US-specific institutional history, and the transferable content is the *mechanism* (a legal constraint was removed) rather than the sequence. **The literature survey of efficiency studies** is represented by the one finding that carries an argument (§3). **International comparisons of banking structure** are deferred, consistent with the exclusion of R&H ch. 20 in the scope decision.

**Previous:** [[01 - The Financial-Services Industry and Its Regulation]] · **Next:** [[03 - Bank Financial Statements]]
