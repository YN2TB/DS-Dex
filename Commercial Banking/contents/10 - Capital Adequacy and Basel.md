---
subject: Commercial Banking
chapter: 10
tags: [ds, banking, capital, basel, tier-1, risk-weighted-assets, leverage-ratio, moral-hazard]
source: "Rose & Hudgins, *Bank Management and Financial Services* 9e, ch. 15"
---

# Capital Adequacy and Basel

**Nine chapters have been pointing here.** [[01 - The Financial-Services Industry and Its Regulation|Ch. 01]] showed a 9% asset loss making a bank insolvent while it still holds 91% of its assets; [[04 - Measuring and Evaluating Bank Performance|ch. 04]] showed three banks with an identical 12.000% ROE differing **3.3×** in how much loss they could absorb; [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]] found a +3% rate shock removing **55.86%** of equity; [[08 - Liquidity and Reserves Management|ch. 08]] destroyed a solvent bank with a run; [[09 - Managing Deposits and Nondeposit Funding|ch. 09]] priced the deposit-insurance subsidy at roughly **a quarter of equity per year**.

**That last one is the argument. Ch. 09 priced the subsidy; this chapter is the charge for it.**

**§3 is the result, and it is uncomfortable.** Basel I and II risk-weight **credit** risk. Government securities get a **0%** weight. So a bank holding nothing but long Treasuries has **zero risk-weighted assets, an undefined-because-infinite capital ratio, and no capital requirement at all** — while *(computed)* **a rate rise of 1.16% wipes out its entire equity.**

**That is the 2023 failure, and it is a design feature of the rule rather than an oversight by the bank.** [[05 - Interest-Rate Risk - Gap and Duration|Ch. 05]] sized the loss, [[08 - Liquidity and Reserves Management|ch. 08]] supplied the trigger, and ch. 10 shows the rule that was supposed to catch it looking in the other direction.

> [!warning] Two errors in the source, both verified
> R&H's Basel I worked example contains **an internal contradiction in the off-balance-sheet figures** and **a wrong Tier 1 ratio (5.52% printed; 4.97% correct)**. Both are in the errata table in `00-Index.md`. **The book's conclusion survives both.**

## 📘 Main Knowledge

### 1. What capital is for, and what counts

**Capital absorbs losses so that depositors do not.** R&H lists its tasks: **a cushion against failure**, funds for the start-up and growth of the institution, **public confidence**, funds for expansion, and — the one that makes it a management problem — **a regulatory constraint on how far the balance sheet can be levered.**

| **Tier 1 (core)** | **Tier 2 (supplemental)** |
|---|---|
| common stock and surplus | allowance for loan losses *(general, capped)* |
| undivided profits (retained earnings) | subordinated debt |
| qualifying non-cumulative preferred | limited-life preferred stock |
| minority interests in consolidated subsidiaries | mandatory convertible debt |

**Basel I's minima:**

| ratio | minimum |
|---|---|
| **Tier 1 / risk-weighted assets** | **4%** |
| **(Tier 1 + Tier 2) / risk-weighted assets** | **8%** |

**with Tier 2 capped at 100% of Tier 1**, and subordinated debt plus limited-life preferred capped at 50% of Tier 1.

> [!note] The tiers rank by how reliably the item absorbs a loss
> **Common equity absorbs losses immediately and without anybody's permission.** Subordinated debt absorbs them only in liquidation, and only after depositors are paid. **The ordering is the whole idea, and it is why post-2008 reform pushed toward *common equity Tier 1* specifically** — Basel I's Tier 1 admitted instruments that turned out not to absorb losses in practice while the bank was still operating.

### 2. Risk-weighted assets — R&H's worked example, verified

**Every asset and every off-balance-sheet commitment is multiplied by a weight meant to reflect its credit risk.** Off-balance-sheet items are first converted to a **credit-equivalent amount**.

**The bank:** Tier 1 = 4,000; Tier 2 = 2,000; total assets = 100,000.

*(Verified — the balance sheet sums to 100,000 exactly, and both leverage ratios match the book:)*

| asset | amount | weight |
|---|---|---|
| cash | 5 000 | **0%** |
| **U.S. Treasury securities** | 20 000 | **0%** |
| deposits at domestic banks | 5 000 | 20% |
| 1–4 family residential mortgages | 5 000 | 50% |
| loans to private corporations | 65 000 | 100% |
| **total** | **100 000** | |

| leverage ratio | | book |
|---|---|---|
| Tier 1 / total assets | **4.00%** | 4.00% ✓ |
| total capital / total assets | **6.00%** | 6.00% ✓ |

**Risk-weighted assets** *(computed, matching the book's total exactly)*:

| bucket | amount | × weight | = |
|---|---|---|---|
| 0% | 25 000 | 0.00 | 0 |
| 20% | 15 000 *(deposits 5 000 + SLC credit-equivalent 10 000)* | 0.20 | 3 000 |
| 50% | 5 000 | 0.50 | 2 500 |
| 100% | 75 000 *(corporate loans 65 000 + commitment credit-equivalent 10 000)* | 1.00 | 75 000 |
| **total RWA** | | | **80 500** ✓ |

> [!warning] ⚠️ Erratum 1 — the off-balance-sheet figures contradict each other
> **R&H's OBS listing** (p. 495): standby letters of credit **\$10,000**, credit commitments \$20,000, **total \$30,000**.
>
> **R&H's credit-conversion table**, same page: SLCs **\$50,000** × 0.20 = \$10,000; commitments \$20,000 × 0.50 = \$10,000.
>
> **The SLC face value is \$10,000 in one place and \$50,000 in the other.** *(Computed: at a \$10,000 face the credit equivalent is **\$2,000**, not \$10,000, and RWA would be **78,900**.)*
>
> **The downstream arithmetic settles which the book used**: its risk-weight table adds "deposits 5,000 + SLC credit-equivalent 10,000 = 15,000", and its RWA total of 80,500 requires the \$50,000 face. **So the \$10,000 face and the \$30,000 OBS subtotal are the inconsistent lines.**

> [!warning] ⚠️ Erratum 2 — the printed Tier 1 ratio is wrong
> **The book prints:** *"\$4,000 / 80,500 = 0.0552, or 5.52 percent"*, and the following sentence calls 5.52% the Tier 1 risk-based ratio.
>
> $$\frac{4{,}000}{80{,}500}=\mathbf{4.97\%},\text{ not }5.52\%$$
>
> **The internal check confirms which figure is wrong.** The book's *total* ratio of **7.45%** is correct, and $7.45\%/4.97\%=1.5000$ exactly, matching $6{,}000/4{,}000$. **So 7.45% and 80,500 are mutually consistent and 5.52% is not.** *(A ratio of 5.52% would require RWA ≈ 72,500 — which would make the total ratio 8.28% and the bank **pass**, contradicting the book's own conclusion.)*
>
> **The display is also mislabelled**, heading a Tier 1 calculation "Total regulatory capital ÷ Total risk-weighted assets".
>
> **The conclusion survives both errors** — see §2b.

**The verdict, recomputed:**

| test | value | minimum | |
|---|---|---|---|
| Tier 1 / RWA | **4.97%** | 4% | **pass** |
| **total / RWA** | **7.45%** | **8%** | **FAIL** |
| Tier 1 leverage | 4.00% | 4% | pass |

*(Computed: the shortfall is $0.08\times80{,}500-6{,}000=\mathbf{440}$ of new capital — **or** a reduction in risk-weighted assets to 75,000, i.e. **5,500** less risk.)*

> [!note] The two remedies are not equivalent, and that is the seed of §4
> **A bank can satisfy the ratio by raising capital *or* by shrinking risk-weighted assets** — and shrinking RWA does not require shrinking the balance sheet, only **reclassifying it into lower-weighted buckets.** Swapping 5,500 of corporate loans for Treasuries fixes the ratio and changes the bank's actual risk in ways the ratio cannot see.

### 3. ⚠️ The hole: Basel weights credit risk only

**Look at the weight list again: 0% for cash and *government securities*, 20% interbank, 50% mortgages, 100% corporate. Nothing in it measures interest-rate risk.**

*(Computed — two banks, each with assets of 163,000 and equity of 16,000:)*

| | risk-weighted assets | Tier 1 / RWA |
|---|---|---|
| **Bank A** — 100% long Treasuries (duration 9) | **0** | **infinite — no requirement at all** |
| Bank B — ch. 05's actual mix | 122 250 | 13.09% |

**Bank A would be reported as the safest bank in the country.** Its risk-weighted assets are zero, so no amount of capital is required and the ratio is undefined.

**But [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s arithmetic still applies to it.** *(Computed, with a duration gap of ~9 years — long assets funded by overnight deposits:)*

| shock | Δ net worth | **as % of equity** |
|---|---|---|
| +1.0% | −13 840 | **−86.5%** |
| +2.0% | −27 679 | **−173.0%** |
| +3.0% | −41 519 | −259.5% |

$$\textbf{a rate rise of only }\mathbf{1.16\%}\textbf{ wipes out Bank A entirely}$$

> [!warning] The capital requirement is exactly zero throughout
> **This is not a bank that broke the rules. It is a bank that followed them perfectly.** Holding government securities is the most conservative thing a credit officer can do, and Basel I and II reward it with a zero weight — **correctly, as a statement about credit risk, and catastrophically as a statement about risk.**
>
> **A portfolio of government bonds has no credit risk and enormous interest-rate risk. The ratio can see the first and is blind to the second.**
>
> **The full chain across this subject:**
> 1. **[[05 - Interest-Rate Risk - Gap and Duration|Ch. 05]] sized the loss** — duration gap × rate shock.
> 2. **[[07 - The Investment Portfolio|Ch. 07]] explained why the assets were there** — Treasuries are the collateral the rules accept and carry a zero risk weight, so the portfolio is shaped by regulation.
> 3. **[[08 - Liquidity and Reserves Management|Ch. 08]] supplied the trigger** — held-to-maturity accounting hides the loss until a run forces the sale.
> 4. **Ch. 10 shows the rule looking the other way.**
>
> **Every step is a rule working as designed, and the outcome is a failed bank.**
>
> *(Basel II added an explicit market-risk charge for the **trading** book, and Pillar 2 asks supervisors to consider interest-rate risk in the **banking** book — but the headline Pillar 1 ratio, the number that is published and compared, still weights credit. The 9th edition predates the 2023 demonstration; the mechanism it describes is what produced it.)*

### 4. Why the leverage ratio exists

*(Computed — two banks, identical size (100,000) and identical Tier 1 (6,000):)*

| | RWA | **Tier 1 / RWA** | **leverage ratio** |
|---|---|---|---|
| **Bank C** — all corporate loans | 100 000 | **6.00%** | 6.00% |
| **Bank D** — 50% Treasuries, 50% mortgages | 25 000 | **24.00%** | 6.00% |

**Bank D's risk-based ratio is four times Bank C's on the same balance sheet with the same capital.**

> [!note] If the weights are right this is correct; if they are wrong it is a subsidy
> **The weights are a regulator's opinion about relative risk, fixed in advance and identical for every bank.** So **an error in them is not diversified away — it is amplified**, because every bank optimises against the same mistake.
>
> **2008 established that 50% for residential mortgages was wrong.** And [[06 - Hedging with Derivatives|ch. 06]] §10 showed the same structure from the other side: **everybody held the same senior tranches, for the same reason, and they failed together.** A common rule produces common exposure.
>
> **Hence the leverage ratio — Tier 1 over *total* assets, unweighted.** No model, no opinion, no scope to reclassify. **Both banks above show 6.00%.**
>
> **It is deliberately crude, and that is the point.** It is a backstop against the possibility that the sophisticated measure is wrong, and it cannot be gamed by moving assets between buckets.
>
> **R&H's own example demonstrates the disagreement without remarking on it**: the bank **passes** on leverage (4.00% ≥ 4%) and **fails** on the risk-based total (7.45% < 8%). **Two measures, two answers — which is exactly why both are required.**

### 5. Why capital is regulated rather than chosen

**The accumulated case from this subject:**

| chapter | finding |
|---|---|
| [[01 - The Financial-Services Industry and Its Regulation\|01]] | 9% equity: a **9% asset loss is insolvency** while the bank still holds 91% of its assets |
| [[04 - Measuring and Evaluating Bank Performance\|04]] | **$1/EM$ is the maximum absorbable loss** — three banks with an **identical 12.000% ROE** absorb 16.67% / 10.00% / **5.00%** |
| [[05 - Interest-Rate Risk - Gap and Duration\|05]] | a **+3% rate shock removes 55.86%** of equity |
| [[06 - Hedging with Derivatives\|06]] | hedging leaves a residual — **1.46% of equity at +2%** — that nothing else covers |
| [[08 - Liquidity and Reserves Management\|08]] | a run makes a **solvent** bank insolvent at **48.5%** withdrawals |
| [[09 - Managing Deposits and Nondeposit Funding\|09]] | **deposit insurance is worth about a quarter of equity per year** |

> [!warning] The last line is the argument
> **The bank does not bear its own downside.** Insured depositors do not demand a higher rate as leverage rises — that is what insurance *does* — so **the price signal that would normally restrain leverage has been removed.**
>
> **Therefore the private optimum leverage exceeds the social optimum**, and no amount of good management closes the gap, because the manager is optimising correctly against the prices they face.
>
> **[[04 - Measuring and Evaluating Bank Performance|Ch. 04]] put it as one identity with two optima: shareholders read the ROE column, regulators read the loss column.** Both are reading the same equation.
>
> **So the ratio is imposed.** Not because managers are reckless, but because **the discipline was deliberately removed in 1934 to stop the runs of [[08 - Liquidity and Reserves Management|ch. 08]]** — and something had to replace it. **[[09 - Managing Deposits and Nondeposit Funding|Ch. 09]] priced the subsidy; ch. 10 is the charge for it.**
>
> **This is [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s claim that all five regulatory rationales reduce to *leverage plus externality*, arriving at its destination.**

### 6. What the rule costs

*(Computed — the ROA a bank must earn to deliver a 12% ROE at each capital ratio:)*

| capital ratio | equity on a 100,000 balance sheet | **ROA needed for a 12% ROE** |
|---|---|---|
| 4.0% | 4 000 | **0.48%** |
| 8.0% | 8 000 | 0.96% |
| 10.5% | 10 500 | 1.26% |
| **13.0%** | **13 000** | **1.56%** |

> [!note] More than triples the required ROA — which is why it is fought over
> **Going from 4% to 13% more than triples the earning power a bank needs to deliver the same return to shareholders.** *(This is [[04 - Measuring and Evaluating Bank Performance|ch. 04]]'s $ROE = ROA\times EM$ read backwards: capping $EM$ forces $ROA$ up.)*
>
> **So the industry's resistance to higher requirements is not irrational or even dishonest — it is arithmetic.** And the counter-argument is equally arithmetic: **a better-capitalised bank is less risky, so its shareholders should require a lower return.** How much lower is the empirical question the whole debate turns on, and it is unresolved.
>
> **Basel III's response** was to raise the effective requirement toward the bottom of that range — a **4.5% common equity Tier 1 minimum plus a 2.5% conservation buffer (7%)**, a countercyclical buffer, surcharges for globally systemic banks, **a hard leverage ratio**, and — from [[08 - Liquidity and Reserves Management|ch. 08]] — the **Liquidity Coverage Ratio** and Net Stable Funding Ratio alongside it.
>
> **Note what that list is: every one of them is a response to a failure this subject has computed.** The leverage ratio answers §4; the LCR answers ch. 08 §5; the conservation buffer answers the fact that a minimum is a cliff rather than a cushion; the countercyclical buffer answers ch. 08 §1's finding that risk builds in booms.

### 7. Basel I → II → III, and what each was trying to fix

| | fix attempted | what went wrong |
|---|---|---|
| **Basel I** (1988) | one crude credit-risk grid, internationally uniform | too crude — all corporate loans weighted alike, so it **rewarded holding the riskiest asset in each bucket** |
| **Basel II** (2004) | three pillars; **internal models** for banks able to run them; explicit operational and market-risk charges | **banks calibrated their own risk weights**, models were trained on a benign period, and it was procyclical — weights fall in booms |
| **Basel III** (post-2010) | more and better capital, **buffers**, a hard **leverage ratio**, **liquidity** rules | still weights credit in Pillar 1 — **§3's hole is not closed** |

> [!note] Each generation fixed the previous one's failure and inherited the underlying problem
> **Basel I was too crude, so Basel II let banks model their own weights — which is asking the regulated party to state how much regulation it needs.** *(The same conflict [[06 - Hedging with Derivatives|ch. 06]] found in credit ratings, where the issuer pays the rater.)*
>
> **Basel III's answer was not a better model but a floor underneath it**: buffers, a leverage backstop, and liquidity requirements that cannot be optimised away. **The direction of travel is away from precision and toward robustness** — which is the right lesson from a sequence in which the sophisticated measure failed three times.

## ✏️ Exercises

**1. (Basel I.)** (a) Compute the ratios for R&H's bank and state the verdict. (b) What are the two errors? (c) What are the bank's options? (d) Why are there both risk-based and leverage ratios?

> [!example]- Solution
> **(a) It passes on Tier 1 and leverage and fails on total capital.**
>
> *(Computed: RWA = **80,500** — matching the book — from buckets of 25,000 × 0, 15,000 × 0.20, 5,000 × 0.50 and 75,000 × 1.00.)*
>
> | test | value | minimum | |
> |---|---|---|---|
> | Tier 1 / RWA | 4.97% | 4% | pass |
> | **total / RWA** | **7.45%** | **8%** | **FAIL** |
> | Tier 1 leverage | 4.00% | 4% | pass *(exactly)* |
>
> **Note where the risk-weighting bites.** Total assets are 100,000 but risk-weighted assets are only 80,500, **because 25,000 of cash and Treasuries carry a zero weight.** The bank's leverage ratio (4.00%) is therefore *lower* than its Tier 1 risk-based ratio (4.97%) — **which is the normal relationship and the reason the leverage ratio binds first for banks holding safe assets.**
>
> **Also note the off-balance-sheet items are not free.** They add 20,000 of credit-equivalent exposure to a 100,000 balance sheet — **a fifth of the bank's risk-weighted assets came from commitments that appear nowhere on it.** [[08 - Liquidity and Reserves Management|Ch. 08]] measured these at 70.9% of industry assets.
>
> **(b) An internal contradiction in the OBS figures, and a wrong Tier 1 ratio.**
>
> **Erratum 1**: the SLC face value is **\$10,000** in the OBS listing and **\$50,000** in the conversion table. *(Computed: a \$10,000 face gives a credit equivalent of \$2,000 and RWA of 78,900.)* **The downstream arithmetic uses \$50,000** — the risk-weight table's "5,000 + 10,000 = 15,000" and the 80,500 total both require it — **so the \$10,000 face and \$30,000 subtotal are the inconsistent lines.**
>
> **Erratum 2**: the book prints **5.52%** for Tier 1 / RWA when $4{,}000/80{,}500=\mathbf{4.97\%}$.
>
> **The internal check identifies which figure is wrong**, which is what makes this filable rather than a guess: **the total ratio of 7.45% is correct, and $7.45/4.97 = 1.5000$ exactly, matching $6{,}000/4{,}000$.** So 7.45% and 80,500 are consistent with each other and 5.52% is consistent with neither. *(5.52% would need RWA ≈ 72,500 — which would make the total ratio 8.28% and the bank **pass**, contradicting the book's own conclusion.)*
>
> **Extraction was ruled out** ([[03 - Bank Financial Statements|ch. 03]]'s discipline): **"5.52 percent" appears twice, in the displayed calculation and again in the following sentence**, and the correct 7.45% appears in that same sentence — so the passage extracted faithfully. **[[08 - Liquidity and Reserves Management|Ch. 08]] separately established that numeric tables in this book survive intact.**
>
> **Neither error changes the conclusion**: the bank passes the 4% Tier 1 test on either figure and fails the 8% total test at 7.45%.
>
> **(c) Raise 440 of capital, or shed 5,500 of risk-weighted assets — and they are not equivalent.**
>
> *(Computed: $0.08\times80{,}500-6{,}000=\mathbf{440}$; or cut RWA to $6{,}000/0.08=75{,}000$, a reduction of **5,500**.)*
>
> **Raising capital genuinely increases loss-absorbing capacity. Shedding risk-weighted assets need not shrink the balance sheet at all** — swapping 5,500 of corporate loans for Treasuries satisfies the ratio while leaving total assets unchanged.
>
> **And the second route is cheaper and faster**, which is why it is the one taken. **That is the seed of §4's problem: the ratio can be satisfied by reclassification**, and reclassification changes measured risk far more than actual risk. **A rule that can be satisfied two ways will be satisfied the cheap way.**
>
> **(d) Because they fail in opposite directions.**
>
> **The risk-based ratio is sensitive to what the bank holds and depends on weights being right. The leverage ratio ignores composition entirely and cannot be wrong about it.**
>
> *(Computed: Bank C, all corporate loans, and Bank D, half Treasuries and half mortgages, both with 100,000 of assets and 6,000 of Tier 1 — **risk-based ratios of 6.00% and 24.00%, leverage ratios of 6.00% and 6.00%.**)*
>
> **Bank D looks four times safer on the measure that thinks, and identical on the measure that does not.** If the weights are right, the risk-based ratio is the better measure. **If they are wrong, it is a subsidy for whatever is underweighted** — and 2008 established that 50% for residential mortgages was wrong.
>
> **The deeper problem is that the weights are common to every bank.** An error is not diversified away; **it is amplified, because every bank optimises against the same mistake** — exactly [[06 - Hedging with Derivatives|ch. 06]] §10's structure, where everyone held the same senior tranches for the same reason and they failed together.
>
> **So the leverage ratio is a backstop against the possibility that the clever measure is wrong.** Deliberately crude, immune to reclassification. **R&H's own bank illustrates the disagreement — passing on leverage and failing on the risk-based ratio.**

**2. (Hard — the hole.)** (a) How can a bank have no capital requirement and fail? (b) Why is this a design feature? (c) Trace the chain across this subject. (d) What would fix it?

> [!example]- Solution
> **(a) By holding assets with no credit risk and enormous interest-rate risk.**
>
> *(Computed: a bank with 163,000 of assets entirely in long Treasuries has **risk-weighted assets of zero**, so its Tier 1 ratio is undefined and its requirement is nil. With a duration gap of ~9 years, **a +1% shock costs 86.5% of equity, +2% costs 173%, and a rise of just 1.16% wipes it out entirely.**)*
>
> **Government securities carry a 0% weight because they have no default risk** — which is true. **They have very large price risk**, which the weight says nothing about.
>
> **The two risks are unrelated**, and Basel I's grid measures only one of them.
>
> **(b) Because the framework was built to solve the previous crisis.**
>
> **Basel I (1988) followed the LDC debt crisis and a decade of credit losses** — the problem in front of it was banks holding too much of the wrong credit. **A single internationally uniform credit grid was a real advance**, and it did what it was designed to do.
>
> **So the zero weight on government paper is correct within the framework's own terms.** **It is not a loophole and not an oversight; the framework simply does not have interest-rate risk in it.**
>
> **And note it is worse than neutral: it is an incentive.** A bank under capital pressure can satisfy the ratio by buying government bonds, which requires no capital at all — **so the rule actively pushes banks toward the exposure it cannot measure.** [[07 - The Investment Portfolio|Ch. 07]] found the same force shaping the investment portfolio: Treasuries are held because they are the collateral the rules accept and carry a zero weight, **not because anyone chose them for return.**
>
> *(Basel II added a market-risk charge for the **trading** book, and Pillar 2 directs supervisors to consider interest-rate risk in the **banking** book. But the headline Pillar 1 ratio — the published, compared, binding number — still weights credit, and assets held to maturity sit in the banking book.)*
>
> **(c) Five rules, each working as designed, producing a failed bank.**
>
> 1. **[[05 - Interest-Rate Risk - Gap and Duration|Ch. 05]] sizes the loss.** A positive duration gap means rising rates cut net worth — computed there at **37.24% of equity** for a +2% shock on a far less extreme balance sheet than Bank A's.
> 2. **[[07 - The Investment Portfolio|Ch. 07]] explains why the assets are there.** Pledging requirements and the zero risk weight make Treasuries the natural holding; the yield give-up is accepted as a cost.
> 3. **[[08 - Liquidity and Reserves Management|Ch. 08]] hides the loss.** Held-to-maturity accounting carries the securities at cost, so the loss is **unrealised and invisible** — computed there at **14.68% of equity** before any withdrawal.
> 4. **[[08 - Liquidity and Reserves Management|Ch. 08]] then triggers it.** A run forces the sale that recognises the loss, and **insolvency arrives at 43.7% of liabilities.**
> 5. **Ch. 10 measures none of it.** The capital ratio was fine throughout.
>
> **No step involves anyone breaking a rule.** **Every step involves someone following one.** That is what makes it a systemic design problem rather than a supervisory failure — and it is why [[08 - Liquidity and Reserves Management|ch. 08]]'s conclusion that *interest-rate risk and liquidity risk are one risk with two names* needs a third name added: **capital regulation, which sees neither.**
>
> **(d) A leverage ratio, mark-to-market, and an explicit rate-risk charge — each with a cost.**
>
> 1. **The leverage ratio already helps** (§4). It ignores weights, so Bank A would face a real requirement — **though sized to its balance sheet, not to its duration gap**, so it constrains without measuring.
> 2. **Marking held-to-maturity securities to market** would make the loss visible before the run. *(Computed in [[08 - Liquidity and Reserves Management|ch. 08]]: 14.68% of equity, invisible.)* **The cost is volatility in reported capital from rate moves that may never be realised** — which is exactly why the exemption exists, and it is a real argument, not a cover story.
> 3. **An explicit interest-rate-risk charge in Pillar 1** — capital against the duration gap, which [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]] shows is straightforward to compute. **The cost is that it requires the regulator to model rate scenarios, and [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]] §5 showed duration itself failing at large shocks** — so the model would need the very sophistication §4 warns against.
>
> **Which is the honest closing point: every fix trades precision against robustness, and this subject has now seen precision fail three times** — Basel I too crude, Basel II's internal models self-serving and procyclical, and Basel III still blind to §3's hole. **The direction of reform since 2008 has been toward robustness: buffers, backstops and floors rather than better models.** **[[06 - Hedging with Derivatives|Ch. 06]] reached the same place** — the only instrument with a bounded downside was the one that required no model and nobody's promise.

**3. (Why regulate?)** (a) Assemble the case. (b) What does the rule cost? (c) What did Basel III change and why?

> [!example]- Solution
> **(a) Leverage plus a removed price signal.**
>
> **[[01 - The Financial-Services Industry and Its Regulation|Ch. 01]] argued that all five regulatory rationales reduce to leverage plus externality. Nine chapters have now supplied the numbers**:
>
> | | |
> |---|---|
> | [[01 - The Financial-Services Industry and Its Regulation\|01]] | a **9% asset loss is insolvency** at 9% equity |
> | [[04 - Measuring and Evaluating Bank Performance\|04]] | identical **12.000% ROEs** hiding a **3.3×** difference in absorbable loss |
> | [[05 - Interest-Rate Risk - Gap and Duration\|05]] | **55.86%** of equity gone on a +3% shock |
> | [[06 - Hedging with Derivatives\|06]] | a hedged position still leaks **1.46%** of equity |
> | [[08 - Liquidity and Reserves Management\|08]] | a **solvent** bank fails at **48.5%** withdrawals |
> | [[09 - Managing Deposits and Nondeposit Funding\|09]] | insurance worth **~a quarter of equity per year** |
>
> **The last line is the whole argument.** Insured depositors **do not demand a higher rate as leverage rises** — that is precisely what the insurance does. **So the price that would restrain leverage has been removed**, and the private optimum exceeds the social one.
>
> **This is not a story about bad managers.** A manager maximising shareholder value at the prices they face **should** lever up; [[04 - Measuring and Evaluating Bank Performance|ch. 04]]'s $ROE = ROA \times EM$ says so directly, and ch. 04 also showed the same identity produces a *different* optimum for a regulator reading the loss column. **One equation, two optima, and the market cannot arbitrate between them because one side has been insured.**
>
> **So the ratio is imposed.** The discipline was removed deliberately in 1934 to stop the runs of [[08 - Liquidity and Reserves Management|ch. 08]], and something had to take its place. **Risk-based deposit-insurance premiums ([[09 - Managing Deposits and Nondeposit Funding|ch. 09]]) are the same idea charged directly rather than imposed as a constraint.**
>
> **(b) More than triple the required ROA, going from 4% to 13%.**
>
> *(Computed: to deliver a 12% ROE a bank needs an ROA of **0.48%** at a 4% capital ratio, **0.96%** at 8%, and **1.56%** at 13%.)*
>
> **This is [[04 - Measuring and Evaluating Bank Performance|ch. 04]]'s identity read backwards: capping the equity multiplier forces ROA up.** *(And [[04 - Measuring and Evaluating Bank Performance|ch. 04]] showed how hard ROA is to move — it is the product of margin and asset utilisation, both set by competition.)*
>
> **So the industry's resistance is arithmetic, not dishonesty.** **The counter-argument is also arithmetic**: a better-capitalised bank is genuinely less risky, so its shareholders should accept a lower required return, and the ROE target should fall. **How much it falls is an empirical question and it is not settled** — which is why this remains contested rather than resolved.
>
> **The honest summary: higher capital makes each bank safer and makes banking less profitable, and the second effect is certain while the first is probabilistic.** That asymmetry, not stupidity, is why the requirement had to be imposed internationally and simultaneously — **a bank that raises capital alone loses to one that does not.**
>
> **(c) It stopped trying to be precise.**
>
> **Basel III's additions** — a **4.5% CET1 minimum plus a 2.5% conservation buffer**, a **countercyclical buffer**, systemic surcharges, a hard **leverage ratio**, and the **LCR** and NSFR from [[08 - Liquidity and Reserves Management|ch. 08]] — **are each a response to a specific failure this subject has computed:**
>
> | addition | answers |
> |---|---|
> | **leverage ratio** | §4 — risk-weighting is gameable and the weights can be wrong |
> | **LCR / NSFR** | [[08 - Liquidity and Reserves Management\|ch. 08]] §5 — borrowing capacity is worth zero exactly when needed |
> | **conservation buffer** | a *minimum* is a cliff; a bank at the limit must stop lending. A buffer gives room to absorb a loss and keep operating |
> | **countercyclical buffer** | [[08 - Liquidity and Reserves Management\|ch. 08]] §1 — risk builds in booms, and Basel II's own weights *fell* in booms |
> | **CET1 focus** | Basel I's Tier 1 admitted instruments that did not absorb losses in practice |
>
> **Every one is a floor, a backstop or a buffer rather than a better model.**
>
> **That is the direction of travel and it is the right lesson from three failures of precision**: Basel I too crude, Basel II asking banks to state their own weights *(the same conflict [[06 - Hedging with Derivatives|ch. 06]] found where the issuer pays the rating agency)*, and Basel III still blind to §3's interest-rate hole.
>
> **[[06 - Hedging with Derivatives|Ch. 06]] ended in the same place** — of every instrument in that chapter, the only one with a bounded downside was the one requiring no model and nobody's promise. **Robustness beat sophistication there too.**

## 📝 Summary

- **Capital absorbs losses so depositors do not**, and it is ranked by how reliably it does so: **Tier 1** (common equity, retained earnings) absorbs immediately; **Tier 2** (loan-loss reserves, subordinated debt) only in liquidation. **Basel I: 4% Tier 1 / RWA, 8% total / RWA, Tier 2 capped at 100% of Tier 1.**
- **Risk-weighted assets** multiply each asset and each off-balance-sheet credit-equivalent by a credit-risk weight — **0% cash and government securities, 20% interbank, 50% mortgages, 100% corporate.**
- *(Verified on R&H's example: RWA = **80,500** exactly; leverage ratios **4.00%** and **6.00%** exactly; total risk-based ratio **7.45%**. **The bank passes Tier 1 and leverage and fails the 8% total test.**)*
- **⚠️ Erratum 1: the SLC face value is \$10,000 in the OBS listing and \$50,000 in the conversion table.** The downstream arithmetic requires \$50,000, so the \$10,000 face and \$30,000 subtotal are the inconsistent lines.
- **⚠️ Erratum 2: the printed Tier 1 ratio of 5.52% should be 4.97%** ($4{,}000/80{,}500$). **The internal check identifies which is wrong**: 7.45%/4.97% = 1.5000 exactly, matching 6,000/4,000. **Neither error changes the conclusion.**
- **The shortfall is 440 of new capital *or* 5,500 less risk-weighted assets — and these are not equivalent.** RWA can be cut by **reclassifying** rather than shrinking, which changes measured risk far more than actual risk.
- **⚠️ The chapter's result: Basel I and II weight *credit* risk only.** *(Computed: a bank holding only long Treasuries has **RWA = 0**, an **infinite capital ratio and no requirement at all**, while **a 1.16% rate rise wipes out its entire equity** — +1% costs 86.5%, +2% costs 173%.)*
- **That is a design feature, not an oversight** — and worse than neutral, since **a bank under capital pressure can satisfy the ratio by buying the exposure the rule cannot see.**
- **The full chain: [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]] sizes the loss, [[07 - The Investment Portfolio|ch. 07]] explains why the assets are there, [[08 - Liquidity and Reserves Management|ch. 08]] hides it (14.68% of equity, invisible) then triggers it, and ch. 10 measures none of it.** **Every step is a rule working as designed.**
- **⚠️ Risk-weighting is gameable** *(computed: two banks, same size, same capital — risk-based ratios of **6.00%** and **24.00%**, leverage ratios of **6.00%** and **6.00%**)*. **The weights are a regulator's opinion, common to every bank, so an error is amplified rather than diversified** — [[06 - Hedging with Derivatives|ch. 06]] §10's structure again.
- **Hence the leverage ratio**: Tier 1 over *total* assets, no model, no opinion, **immune to reclassification.** R&H's own bank passes on it and fails the risk-based test — **which is why both are required.**
- **⚠️ Capital is regulated because insured depositors do not price leverage.** The private optimum exceeds the social one, and no amount of good management closes the gap. **[[09 - Managing Deposits and Nondeposit Funding|Ch. 09]] priced the subsidy; ch. 10 is the charge for it.**
- **The rule costs real money** *(computed: a 12% ROE needs an ROA of **0.48%** at 4% capital and **1.56%** at 13% — [[04 - Measuring and Evaluating Bank Performance|ch. 04]]'s identity read backwards)*. **Resistance is arithmetic, not dishonesty** — as is the counter-argument that a safer bank should face a lower required return.
- **Basel I was too crude; Basel II let banks model their own weights and was procyclical; Basel III added buffers, a leverage backstop and liquidity rules.** **Each addition answers a failure computed in this subject.**
- **The direction of reform is away from precision and toward robustness** — floors, backstops and buffers rather than better models. **[[06 - Hedging with Derivatives|Ch. 06]] reached the same conclusion by a different route.**

## ⚠️ Important Notes

1. **Tier 1 absorbs losses while the bank operates; Tier 2 only in liquidation.** The ordering is the entire logic of the tiers.
2. **Both minima must be met** — 4% Tier 1 *and* 8% total. Passing one says nothing about the other.
3. **⚠️ R&H's Tier 1 ratio of 5.52% is wrong; use 4.97%.** The 7.45% total ratio is correct.
4. **⚠️ R&H's SLC face value is internally contradictory** (\$10,000 vs \$50,000); the \$50,000 figure is the one the example uses.
5. **Off-balance-sheet items are converted to credit equivalents and then weighted** — a fifth of this bank's RWA came from items not on its balance sheet.
6. **⚠️ A capital shortfall can be met by raising capital or by shedding RWA, and the second is cheaper.** Expect reclassification, not recapitalisation.
7. **⚠️ Basel I and II weight credit risk. Interest-rate risk in the banking book carries no Pillar 1 charge.**
8. **⚠️ A zero risk weight is an incentive, not just a measurement.** The rule pushes capital-constrained banks toward the exposure it cannot see.
9. **A perfect capital ratio is not evidence of safety.** Ask what the ratio does not measure before reading it.
10. **⚠️ Compute the duration gap ([[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]) alongside the capital ratio.** Neither sees the other's risk.
11. **⚠️ Risk weights are common to all banks, so an error in them is amplified, not diversified.** Everyone optimises against the same mistake.
12. **The leverage ratio is deliberately crude** — that is what makes it a backstop.
13. **When the two ratios disagree, that disagreement is information**, not a defect.
14. **Capital is imposed because insured deposits removed the price signal**, not because managers are reckless.
15. **Higher capital requirements genuinely reduce ROE at a given ROA** ([[04 - Measuring and Evaluating Bank Performance|ch. 04]]) — which is why they must be imposed internationally and simultaneously.
16. **A minimum is a cliff; a buffer is a cushion.** A bank at exactly the minimum must stop lending to absorb any loss.
17. **⚠️ Asking a regulated party to model its own requirement is the Basel II problem** — the same conflict as an issuer paying its rating agency ([[06 - Hedging with Derivatives|ch. 06]]).

> [!warning] Gaps in the source material
> **R&H ch. 15 extracts well** *(PDF pp. 502–538; book page $n$ = PDF page $n+18$)*. **The Basel I worked example came through complete**, including the asset list, the conversion factors, the risk-weight buckets and the ratios — which is what made the two errata findable. *(The four standing hazards in `00-Index.md` apply.)*
>
> **Verified from the book: the balance sheet total (100,000), both leverage ratios (4.00%, 6.00%), the risk-weight buckets, the RWA total (80,500) and the total risk-based ratio (7.45%) — all exact.**
>
> **Two errata found and filed** *(see `00-Index.md`)*. **Extraction was ruled out for both**, per [[03 - Bank Financial Statements|ch. 03]]'s discipline: **"5.52 percent" appears twice** — in the displayed calculation and again in the following sentence — **and the correct 7.45% appears in that same sentence**, so the passage extracted faithfully; and [[08 - Liquidity and Reserves Management|ch. 08]] separately established that numeric tables in this book survive intact. **The internal consistency check ($7.45/4.97 = 1.5000 = 6{,}000/4{,}000$) identifies which figure is wrong rather than merely flagging a disagreement**, which is what makes the erratum filable.
>
> **Lost:** Exhibit 15-1's capital-structure diagram and the trend charts, as expected of graphical exhibits.
>
> **Figures that are mine**: Bank A and Bank B in §3, Banks C and D in §4, and the ROE/ROA table in §6. **The Basel I example, the weights, the tier definitions and the minima are the book's.**
>
> **Additions beyond the source.**
>
> - **⚠️ §3 is the chapter's main addition and is entirely mine.** **R&H explains the risk-weight framework carefully and never asks what it fails to measure.** The construction of a bank with **zero risk-weighted assets and a 1.16% fatal rate shock**, and the identification of this as a *design feature* rather than a loophole, are not in the source. **The 9th edition predates 2023**, so the mechanism is derived from the framework rather than from the event — which is the stronger form of the point.
> - **The five-step chain across ch. 05 → 07 → 08 → 10**, showing a failure produced entirely by rules working as designed, is my synthesis and is what the whole subject has been building toward.
> - **§4's Bank C / Bank D comparison** — identical size and capital, risk-based ratios of 6.00% and 24.00% — is mine, as is the argument that **common weights amplify rather than diversify an error** (linking to [[06 - Hedging with Derivatives|ch. 06]] §10) and the framing of the leverage ratio as a deliberate refusal to model. **R&H describes the leverage ratio without explaining why a crude measure is kept alongside a sophisticated one.**
> - **§5's assembly of the regulatory case from nine chapters' computed figures** is mine; R&H argues for capital regulation qualitatively and in one place.
> - **§6's ROA-for-a-given-ROE table** is mine — it makes the cost of the rule concrete and shows why the debate is arithmetic rather than ideological. R&H discusses the burden without quantifying it.
> - **§7's table of what each Basel generation fixed and inherited**, and the observation that **every Basel III addition answers a specific failure computed in this subject**, are mine.
> - **Basel III detail** (CET1 4.5% + 2.5% conservation buffer, countercyclical buffer, systemic surcharges, the hard leverage ratio, LCR/NSFR) is an **addition**: the 9th edition was written as Basel III was being finalised and describes it only in outline. It is included because it is examinable today and because it is the direct answer to §§3–4.
>
> **Deliberately compressed.** **R&H §15-5's history of the capital-adequacy debate** — the long argument over whether regulators or the market should set capital, and the research on whether capital prevents failure — is compressed to §5's conclusion; it is interesting but the operative content is the moral-hazard argument. **The derivatives capital treatment** (potential vs current market risk exposure, conversion factors of 0.005 for interest-rate swaps and 0.05 for currency swaps) is noted in principle but not worked: the mechanics have been entirely superseded by the SA-CCR framework, and [[06 - Hedging with Derivatives|ch. 06]] owns the underlying instruments. **US-specific capital categories** (well capitalized / adequately capitalized / undercapitalized and the prompt-corrective-action triggers) are compressed to the minima — the thresholds are jurisdiction-specific and have changed. **Basel II's three pillars and the internal-ratings-based approaches** are summarised rather than worked; the IRB formulas are beyond this course and the approach is being retired under the Basel III endgame. **Planning to meet capital needs** (dividend policy, internal vs external capital generation) is a corporate-finance topic touched on in [[04 - Measuring and Evaluating Bank Performance|ch. 04]]'s ROE decomposition.

**Previous:** [[09 - Managing Deposits and Nondeposit Funding]] · **Next:** [[11 - Lending - Policy, Credit Risk and Business Loans]]
