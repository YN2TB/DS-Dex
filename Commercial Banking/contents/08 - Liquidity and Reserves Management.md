---
subject: Commercial Banking
chapter: 8
tags: [ds, banking, liquidity, bank-run, solvency, core-deposits, pledging, lcr, reserves]
source: "Rose & Hudgins, *Bank Management and Financial Services* 9e, ch. 11"
---

# Liquidity and Reserves Management

[[01 - The Financial-Services Industry and Its Regulation|Chapter 01]] §2 asserted that **solvency is a balance-sheet fact and liquidity is a timing fact**, and that the gap between them makes a bank run *rational*. **This chapter makes that rigorous.**

**§4 is the result.** Take ch. 05's bank — **solvent, with a 9.82% equity ratio and not one loan in default** — and let depositors withdraw. Meeting the withdrawals means selling assets at a discount, and the discounts accumulate against equity. *(Computed:)* **the bank is insolvent at withdrawals of 48.5% of its liabilities**, and **43.7% once the unrealised losses ch. 05 already created are counted.**

**Nothing defaulted. Every asset performed. The run did not reveal the insolvency — it created it.**

**§3 discharges the obligation [[07 - The Investment Portfolio|ch. 07]] left**: pledged securities are encumbered, and netting them out drops this bank's liquid-securities ratio from **20.00% to 13.00%**.

**All three of R&H's tables were recomputed — 22 separate checks, all exact.** This is the best-extracting chapter in the book.

## 📘 Main Knowledge

### 1. Demand, supply, and the liquidity gap

**Liquidity is not a stock of assets. It is a *position*:**

> **A financial firm is liquid only if it has access, at reasonable cost, to liquid funds in exactly the amounts required at precisely the time they are needed.** — R&H, p. 363

**Three qualifiers, all load-bearing:** *at reasonable cost* (funds you can only get at a punitive rate are not liquidity), *in exactly the amounts* (a surplus is a cost too), *at precisely the time* (early is useless, late is fatal).

**A liquid asset needs three properties:** a **ready market**, a **stable price** (deep enough to absorb the sale without moving it), and **reversibility** (the seller recovers principal).

$$\text{liquidity gap}=\Delta\text{deposits}-\Delta\text{loans}$$

*(Verified — R&H's Table 11-2, all five weeks:)*

| week | $\Delta$deposits | $\Delta$loans | **gap** | book |
|---|---|---|---|---|
| Jan wk 2 | −100 | +50 | **−150** | −150 ✓ |
| Jan wk 3 | −100 | +100 | **−200** | −200 ✓ |
| Jan wk 4 | −50 | +50 | **−100** | −100 ✓ |
| Feb wk 1 | +300 | −250 | **+550** | +550 ✓ |
| Feb wk 2 | −50 | +150 | **−200** | −200 ✓ |

> [!note] The deadly combination arrives when things feel best
> **Liquidity falls when deposits fall *and* loans rise** — and that is the normal state of a boom. **Credit demand is strong, so loans grow; rates are rising, so depositors move money to better-paying alternatives.** The two forces push the same way at exactly the moment the business looks healthiest.
>
> **This is why liquidity risk is procyclical**, and why a bank that manages it by watching current conditions is watching the wrong thing.

### 2. Forecasting: sources and uses

R&H decomposes deposits and loans into **trend + seasonal + cyclical**.

*(Verified — Table 11-1, all **12** rows foot exactly:)*

| | trend | seasonal | cyclical | = total |
|---|---|---|---|---|
| deposits, Jan wk 1 | 1 210 | −4 | −6 | **1 200** ✓ |
| deposits, Jan wk 4 | 1 216 | −165 | −101 | **950** ✓ |
| loans, Jan wk 3 | 801 | +174 | −25 | **950** ✓ |
| loans, Feb wk 1 | 803 | +27 | −80 | **750** ✓ |

*(…and the eight others.)*

> [!note] The seasonal term dominates, and that is the useful finding
> **Look at the magnitudes.** In January week 3 the loan trend moves by **+1** while the seasonal element moves by **+174**. **The trend is almost irrelevant over a six-week horizon; the seasonal and cyclical terms are the entire story.**
>
> **So a liquidity forecast is not a growth forecast.** Annual growth rates — 10% on deposits, 8% on loans here — say nothing about whether the bank can meet next Tuesday.
>
> *(One loose end, checked and **not** an erratum: the trend column increments by 2/week for deposits where compounding 10% on a \$1,200mn base implies 2.31, and starts at 1,210 rather than ~1,202. **The trend line is evidently fitted over ten years of history rather than compounded forward from the year-end figure.** The decomposition the table actually claims is exact in all 12 rows, which is what matters.)*

### 3. Structure of funds: composition is the risk

**Classify liabilities by how likely they are to leave**, then hold a reserve behind each:

$$\text{requirement}=0.95\,H'+0.30\,V'+0.15\,S'+1.00\,(L_{\max}-L_{\text{actual}})$$

where $H', V', S'$ are hot, vulnerable and stable funds *net of legal reserves*.

*(Verified — R&H's Table 11-3, every line:)*

| | | book |
|---|---|---|
| $0.95\times(25-0.03\times25)$ | **23.04** | 23.04 ✓ |
| $0.30\times(24-0.03\times24)$ | **6.98** | 6.98 ✓ |
| $0.15\times(100-0.03\times100)$ | **14.55** | 14.55 ✓ |
| loans: $140\times0.10+(140-135)$ | **19.00** | 19.00 ✓ |
| **total** | **63.57** | **63.57** ✓ |

> [!warning] The same balance sheet, remixed
> *(Computed — holding total funding at \$149mn and varying only the mix:)*
>
> | hot | vulnerable | stable | **liability reserve** | % of funding |
> |---|---|---|---|---|
> | 10 | 24 | 115 | 32.93 | 22.1% |
> | **25** | **24** | **100** | **44.57** | **29.9%** |
> | 50 | 24 | 75 | 63.97 | 42.9% |
> | **75** | **24** | **50** | **83.37** | **56.0%** |
>
> **Moving \$50mn from core deposits into hot money raises the requirement by 87%** — from 44.57 to 83.37 — **with the balance sheet exactly the same size.**
>
> **So liquidity risk is a property of the *funding mix*, not of the bank's size or even its assets.** Two banks with identical balance-sheet totals can differ by a factor of 2.5 in what they need to hold.
>
> **And note the loan term: $1.00\times(L_{\max}-L_{\text{actual}})$ — a full 100% weight.** R&H's reasoning is that a lender must never turn down a good loan, so undrawn capacity must be funded in full. **That is an unused loan commitment, and §6 shows the industry writing them at 70.9% of total assets.**

### 4. ⚠️ When a liquidity problem becomes insolvency

**Take ch. 05's bank. It is solvent: assets 163,000, liabilities 147,000, equity 16,000 — a 9.82% equity ratio.** Depositors withdraw. The bank meets them cheapest-first, and each source costs more than the last:

| order | source | available | **haircut** |
|---|---|---|---|
| 1 | cash | 8 150 | 0.0% |
| 2 | **free** securities | 21 190 | **7.20%** — ch. 05's +2% shock, unrealised until sold |
| 3 | loans | 122 250 | **25.0%** — no ready market |
| 4 | pledged securities | 11 410 | **unavailable at any price** |

*(Computed:)*

| withdrawals | % of liabilities | realised loss | equity left | solvent? |
|---|---|---|---|---|
| 10 000 | 6.8% | 143.62 | 15 856 | yes |
| 30 000 | 20.4% | 2 255.42 | 13 745 | yes |
| 50 000 | 34.0% | 8 922.09 | 7 078 | yes |
| 70 000 | 47.6% | 15 588.75 | 411 | *barely* |
| **71 234** | **48.5%** | **16 000** | **0** | **NO** |

> [!warning] The run does not reveal insolvency — it creates it
> **The bank was solvent when the run began and every one of its assets performed. Not a single loan defaulted.** It died because it was forced to convert assets into cash faster than the market would pay par for them.
>
> **This is [[01 - The Financial-Services Industry and Its Regulation|ch. 01]] §2 made rigorous.** Solvency is about *whether* the assets are worth more than the liabilities; liquidity is about *when*. **Forced sale is the mechanism that converts the second problem into the first.**
>
> **And that is exactly why joining a run is rational.** If withdrawals will make the bank insolvent, then the depositors who withdraw *first* are paid in full and the ones who wait are not. **Waiting is only sensible if you are confident others will wait — which is a coordination problem, not a credit judgement.**
>
> **So deposit insurance does not work by making the bank stronger. It works by removing the reason to run** — it changes the depositor's payoff, not the balance sheet. **Which is also why it creates the moral hazard that [[10 - Capital Adequacy and Basel|ch. 10]]'s capital rules exist to offset.** [[01 - The Financial-Services Industry and Its Regulation|Ch. 01]] made this argument; here it is a number.

**And there is a loss already sitting there before anyone withdraws.**

*(Computed — ch. 05's +2% shock against a securities book of duration 4:)*

$$\text{unrealised loss}=7.20\%\times32{,}600=\mathbf{2{,}348.56}=\mathbf{14.68\%\text{ of equity}}$$

> [!warning] Held-to-maturity accounting hides it, and a run forces its recognition
> **If the securities are classified held-to-maturity they are carried at cost, so this loss appears nowhere.** The bank's *true* equity is **13,651**, not 16,000.
>
> *(Recomputed on true equity: **insolvency at 64,188 = 43.7% of liabilities**, down from 48.5%.)*
>
> **That is the 2023 mechanism in one line.** A rate rise creates a loss that the accounting hides; a run is what forces the sale that recognises it. **The depositors who ran were not panicking — they were reading [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]].**
>
> **The general point: an unrealised loss is a real loss that has not been *triggered* yet, and the trigger is a liquidity event.** So interest-rate risk and liquidity risk are not two risks — **they are one risk with two names, and the second is how the first gets collected.**

### 5. Asset vs liability liquidity: two very different costs

**Asset strategy** — store liquidity in cash and securities. *(Computed: the give-up is 3.75 points; a 20% allocation costs **1,222.50 per year**, every year, whether or not liquidity is ever needed.)*

**Liability strategy** — borrow when needed. *(Computed on a 30,000 need:)*

| market conditions | rate | annual cost |
|---|---|---|
| normal | 4.50% | 1 350 |
| mild stress | 5.00% | 1 500 |
| **market doubts you** | **7.50%** | **2 250** |
| **market refuses** | — | **funding is unavailable** |

> [!warning] Zero until it is infinite
> **The asset strategy's cost is certain and small. The liability strategy's cost is zero — until it is infinite.**
>
> **Purchased liquidity is reliably available on exactly the days you do not need it.** R&H notes approvingly that liability management "comes with its own control lever — the interest rate offered to borrow funds." **That lever is held at the other end.** A bank raising its offered rate to attract funds is also announcing that it needs them, which is the fact that closes the market.
>
> **This is why the balanced strategy is standard**, and why **regulators after 2008 stopped accepting borrowing capacity as a substitute for liquid assets** — the Basel III **Liquidity Coverage Ratio** requires *high-quality liquid assets* against 30 days of stressed outflows ([[10 - Capital Adequacy and Basel|ch. 10]]).
>
> **R&H's own list of the asset strategy's costs is honest and worth keeping:** forgone earnings, transaction costs, selling into a falling market, weakening the appearance of the balance sheet (because the assets sold are the safe ones), and the permanently lower yield on liquid assets.

### 6. ⚠️ Pledged securities, and what the indicators hide

R&H gives **ten liquidity indicators**. Two are *negative* — higher is worse: the **capacity ratio** (loans/assets) and the **pledged securities ratio**.

*(Computed for ch. 05's bank, with 35% of securities pledged:)*

| indicator | value |
|---|---|
| cash position (cash/assets) | 5.00% |
| **liquid securities (securities/assets)** | **20.00%** |
| capacity (loans/assets) | 75.00% *(negative)* |
| pledged securities ratio | 35.00% *(negative)* |

| | |
|---|---|
| securities | 32 600 |
| **pledged — cannot be sold** | **11 410** |
| **genuinely free** | **21 190** |
| **true liquid securities ratio** | **13.00%**, not 20.00% |

> [!warning] The headline overstates the position by 54%
> **[[07 - The Investment Portfolio|Ch. 07]] established that pledged securities are encumbered.** Here is the consequence: **R&H lists the pledged-securities ratio as one of its ten indicators but never nets it out of the others.** So a bank can report a 20% liquid-securities ratio while holding 13%.
>
> **Compute both and report the net one.** Reporting the gross figure is not fraud — it is the standard ratio — which is precisely what makes it dangerous.

**The industry's own trend** *(R&H Table 11-4, FDIC data)*:

| year | cash position | capacity | **unused commitments** |
|---|---|---|---|
| 1985 | **12.5%** | 58.9% | n/a |
| 1996 | 7.3% | 60.2% | 33.1% |
| 2003 | 4.6% | 58.6% | **70.9%** |
| **2007** | **4.3%** | 58.5% | 65.0% |
| 2010 | 7.7% | 54.0% | 45.2% |

> [!note] Both indicators moved the same way for twenty-two years
> *(Computed: the cash position fell **66%** from 1985 to 2007; unused commitments rose **114%** from 1996 to 2003, reaching **70.9% of total assets**.)*
>
> **The industry ran its cash down by two-thirds while writing off-balance-sheet promises worth more than two-thirds of its assets.** Less liquidity, more contingent claims — the same direction on both counts, for two decades, ending in 2007.
>
> **And note which way a loan commitment bites.** It is **a promise the *borrower* exercises**, so it is drawn precisely when borrowers are short of cash — **which is when the bank is short too.** [[06 - Hedging with Derivatives|Ch. 06]] §7's category: **another written option, correlated the wrong way**, and it does not appear on the balance sheet until it is drawn.
>
> **The 2010 rebound to 7.7% is not prudence returning.** R&H attributes it to an absence of loan demand — **liquidity accumulated because there was nothing else to do with the money**, which is a very different thing from choosing to hold it.

## ✏️ Exercises

**1. (Estimating liquidity needs.)** (a) What is the liquidity gap and when is it worst? (b) Verify the sources-and-uses decomposition and say what it teaches. (c) Verify the structure-of-funds requirement. (d) What does that method actually claim?

> [!example]- Solution
> **(a) $\text{gap}=\Delta\text{deposits}-\Delta\text{loans}$, and it is worst in a boom.**
>
> *(Verified against R&H Table 11-2, all five weeks: −150, −200, −100, +550, −200.)*
>
> **Liquidity comes from deposits arriving and loans running off; it is consumed by deposits leaving and loans being made.** A deficit means raising funds from the cheapest available source; a surplus means investing it until needed. *(A surplus is a cost, not a comfort — idle funds earn nothing.)*
>
> **The dangerous combination is deposits falling while loans rise, and that is the normal state of an expansion:** credit demand is strong, and rising rates pull depositors toward better-paying alternatives. **Both forces push the same way at the moment the bank looks healthiest** — which makes liquidity risk procyclical and makes "current conditions look fine" the least informative possible reassurance.
>
> **(b) Trend + seasonal + cyclical, and the trend is nearly irrelevant.**
>
> *(Verified: all **12** rows of Table 11-1 foot exactly.)*
>
> **The lesson is in the magnitudes.** In January week 3 the loan **trend** moves **+1** while the **seasonal** element moves **+174**. **Over a six-week horizon the trend contributes almost nothing.**
>
> **So a liquidity forecast is not a growth forecast.** Knowing deposits grow 10% a year tells you nothing about whether you can meet next Tuesday — and the two are routinely confused because they are computed from the same series.
>
> *(A loose end worth reporting because it was checked: the trend column increments by 2/week where compounding 10% on 1,200 implies 2.31, and starts at 1,210 rather than ~1,202. **The trend line is fitted over ten years of history, not compounded forward.** Not an erratum — the decomposition the table claims is exact everywhere. **This is the [[03 - Bank Financial Statements|ch. 03]] discipline: an internal check that passes is what matters; a reconstruction that doesn't quite reproduce is my inference failing, not the book's.**)*
>
> **(c) 63.57, verified line by line.**
>
> $$0.95(25-0.75)+0.30(24-0.72)+0.15(100-3)+\big[140\times0.10+(140-135)\big]$$
> $$=23.04+6.98+14.55+19.00=\mathbf{63.57}\;✓$$
>
> **(d) That liquidity risk is a property of the funding mix, not of the bank.**
>
> *(Computed — same \$149mn of funding, remixed: **hot 10 → 32.93**; **hot 25 → 44.57**; **hot 50 → 63.97**; **hot 75 → 83.37**. Moving \$50mn from core to hot raises the requirement **87%** with the balance sheet unchanged.)*
>
> **Two banks of identical size, holding identical assets, can differ by a factor of 2.5 in what they must hold.** The difference is entirely in who their depositors are.
>
> **What "hot money" means operationally: funding that is interest-sensitive and will leave when someone pays more.** Large CDs, brokered deposits, fed funds purchased. **Core deposits are small, insured, and sticky** — which is why the [[09 - Managing Deposits and Nondeposit Funding|next chapter]]'s question of how to price deposits is a liquidity question, not just a cost question.
>
> **The method's honest weakness, which R&H states:** the 95/30/15 weights are **"subjective estimates that rely heavily on management's judgment"**. They are not estimated from anything. **A bank that classifies optimistically gets a comfortable answer** — and the classification is exactly what a run tests.
>
> **The 100% weight on undrawn loan capacity is the aggressive part**, and §6 shows why: unused commitments reached **70.9% of industry assets**.

**2. (Hard — the run.)** (a) Trace the insolvency calculation. (b) Why is joining a run rational? (c) What does the unrealised loss add? (d) What does this say about interest-rate risk and liquidity risk?

> [!example]- Solution
> **(a) A solvent bank with no defaults is destroyed by 48.5% withdrawals.**
>
> **The bank starts solvent** — assets 163,000, liabilities 147,000, equity 16,000, a **9.82%** equity ratio, and [[03 - Bank Financial Statements|ch. 03]] confirmed that this is a realistic ratio (BB&T's was 9.77%).
>
> **Withdrawals are met cheapest-first, and the cost rises at each step**: cash at par, then free securities at a **7.20%** haircut (ch. 05's rate shock), then loans at **25%** (there is no ready market for a bank's loan book), while **pledged securities cannot be sold at any price.**
>
> *(Computed: **insolvency at withdrawals of 71,234 = 48.5% of liabilities.**)*
>
> **Two features of the arithmetic matter.** First, **the bank loses only the *discount* on each sale, not the asset** — which is why it survives withdrawals several times its equity. Second, **the cost is convex**: the first 8,150 is free, the next 21,190 costs 7.2%, and everything after that costs 25%. **The damage accelerates**, so the situation deteriorates faster than it appears to early on.
>
> **Nothing defaulted.** Every asset performed exactly as promised. **The loss is entirely the difference between what the assets are worth and what they can be sold for today.**
>
> **(b) Because the depositors who withdraw first are paid in full.**
>
> **If enough others withdraw, the bank becomes insolvent and the late ones take a loss.** So each depositor's best action depends on what the others do: **wait if they wait, run if they run.** Both are self-fulfilling.
>
> **This is a coordination problem, not a credit judgement.** A depositor who believes the bank's assets are sound should *still* run if they believe others will — **and being right about the assets does not protect them.** That is what makes runs different from ordinary credit losses and why they cannot be prevented by being a good bank.
>
> **Deposit insurance works on the payoff, not the balance sheet.** It does not make the assets better; it removes the reason to be first. **[[01 - The Financial-Services Industry and Its Regulation|Ch. 01]] argued exactly this and noted the price: the insured depositor no longer monitors the bank, so the discipline moves to the regulator** — which is why [[10 - Capital Adequacy and Basel|ch. 10]]'s capital rules are imposed rather than chosen.
>
> *(The 2023 failures are the case where insurance did not bind: deposits far above the insured limit, held by a concentrated, well-informed, electronically connected depositor base. **The coordination problem was solved much faster than in 1933** — which made the run faster, not less rational.)*
>
> **(c) It moves the insolvency point from 48.5% to 43.7% and explains the trigger.**
>
> *(Computed: ch. 05's +2% shock has already cost the securities book **7.20%** of its value = **2,348.56 = 14.68% of equity**. True equity is **13,651**, not 16,000.)*
>
> **Under held-to-maturity accounting this loss appears nowhere.** The securities are carried at cost because the bank asserts it will hold them to maturity — **an assertion that is true right up until a liquidity need makes it false.**
>
> **So the accounting classification is itself a liquidity assumption**, and it fails in exactly the state where it matters. **The bank is 14.68% weaker than its balance sheet says, in a way that becomes visible only when tested.**
>
> **That is 2023.** A rate rise created large unrealised losses across the industry; the losses were invisible under HTM; depositors who did the ch. 05 arithmetic themselves concluded the equity was gone; **the run then forced the sales that made the arithmetic true.**
>
> **(d) That they are one risk with two names.**
>
> **An unrealised loss is a real loss that has not been triggered.** The trigger is a liquidity event. **So interest-rate risk determines the *size* of the loss and liquidity risk determines *whether it is collected*.**
>
> **Managing them separately is the error**, and it is institutionally natural — ALM handles duration, treasury handles cash. **[[05 - Interest-Rate Risk - Gap and Duration|Ch. 05]] measured the loss and [[07 - The Investment Portfolio|ch. 07]] noted the sale date is set by liquidity needs; this chapter closes the loop.**
>
> **The practical consequence: a duration gap is only tolerable to the extent the bank will never be forced to sell.** A bank with a large duration gap and volatile funding has one risk, not two — **and the standard reports show it two.**

**3. (Strategies and indicators.)** (a) Compare the asset and liability strategies. (b) Why did regulators stop accepting borrowing capacity? (c) What do the ten indicators miss? (d) Read the 1985–2010 trend.

> [!example]- Solution
> **(a) One has a certain small cost; the other has none until it has an infinite one.**
>
> *(Computed: the **asset** strategy gives up 3.75 points — **1,222.50 a year** on a 20% allocation, paid every year regardless. The **liability** strategy costs 1,350 at normal rates, **2,250 when the market doubts you**, and is **unavailable** when it refuses.)*
>
> **The asymmetry is the whole comparison.** The asset strategy pays a small insurance premium continuously; the liability strategy pays nothing and then fails completely.
>
> **And the failure is not random — it is correlated with needing the funds.** A bank raising its offered rate to attract money is simultaneously announcing that it needs money, **which is the information that closes the market.** R&H praises liability management for "its own control lever — the interest rate offered." **The lever is held at the other end**, and it stops working at precisely the moment it is pulled hard.
>
> **R&H's list of the asset strategy's costs is honest**: forgone earnings, transaction costs, selling into falling markets, and — a subtle one — **weakening the appearance of the balance sheet, because the assets sold first are the safe ones.** A bank meeting withdrawals looks progressively riskier as it does so, which feeds the run.
>
> **Hence the balanced strategy**: liquid assets for the certain and immediate needs, borrowing capacity for the unexpected, and never treating the second as a substitute for the first.
>
> **(b) Because 2008 was the state in which borrowing capacity is worth zero.**
>
> **Committed lines and money-market access all evaporated together**, for the same reason and at the same time: **they are promises from counterparties who were themselves under stress.** [[06 - Hedging with Derivatives|Ch. 06]] §12's table is exactly this — *every instrument transfers risk to somebody who has a state in which they cannot pay.*
>
> **The Basel III response is the Liquidity Coverage Ratio**: hold **high-quality liquid assets** against 30 days of stressed net outflows. **It deliberately refuses to count borrowing capacity**, and it applies stress weights to funding by type — **which is the structure-of-funds method of §3, turned from management judgement into a binding rule.**
>
> **That is the pattern [[01 - The Financial-Services Industry and Its Regulation|ch. 01]] identified**: the thing management chose becomes the thing the regulator imposes, once it is clear the choice is made under a moral hazard.
>
> **(c) Encumbrance, correlation, and the fact that they are all backward-looking.**
>
> 1. **⚠️ Encumbrance.** *(Computed: netting out 35% pledged drops the liquid-securities ratio from **20.00% to 13.00%** — the headline overstates by **54%**.)* **R&H lists the pledged ratio as an indicator but never nets it out of the others**, so the standard ratio and the true one differ by half.
> 2. **Correlation.** Each indicator is computed alone, but **they deteriorate together** — the same stress that makes deposits leave makes assets hard to sell and lenders unwilling. **A dashboard of ten independent numbers implies ten independent risks.**
> 3. **They are stock measures of a flow problem.** Liquidity is about *amounts at times*. A ratio is a snapshot; it cannot show whether the cash arrives on the day it is needed. **The sources-and-uses method (§2) is the flow measure, and it is the one that answers the actual question.**
> 4. **And they compare against industry averages** — R&H says institutions "estimate their liquidity needs based upon experience and industry averages." **Being average is no defence when the whole industry has moved the same way**, which is precisely what (d) shows.
>
> **(d) Twenty-two years of moving in one direction.**
>
> *(Computed: the cash position fell from **12.5% to 4.3%** — a **66% decline** — between 1985 and 2007, while unused loan commitments rose **114%** from 1996 to 2003, reaching **70.9% of total assets**.)*
>
> **Both indicators moved the same way**: less liquidity held, more contingent claims written. **An institution that benchmarked itself against the industry average would have found itself comfortably normal throughout.**
>
> **The commitments figure deserves attention.** At 70.9% of assets these are **off-balance-sheet promises drawn at the borrower's option** — and borrowers draw them when they are short of cash, **which is when the bank is short too.** [[06 - Hedging with Derivatives|Ch. 06]] §7's category exactly: **a written option, correlated the wrong way, invisible until exercised.** §3's structure-of-funds method is right to weight it at 100%.
>
> **The 2010 rebound to 7.7% is not a return to prudence.** R&H attributes it to weak loan demand — **cash accumulated because there was nothing else to do with it.** A liquidity ratio that improves because the bank cannot find borrowers is not evidence of better liquidity management; **it is the same procyclicality from (a), running the other way.**

## 📝 Summary

- **Liquidity is a position, not a stock**: *access, at reasonable cost, to funds in exactly the amounts required at precisely the time needed.* All three qualifiers bind.
- **Liquidity gap = Δdeposits − Δloans** *(verified against R&H Table 11-2, all five weeks)*. **The deadly combination — deposits falling while loans rise — is the normal state of a boom**, which makes liquidity risk procyclical.
- **Forecasts decompose into trend + seasonal + cyclical** *(verified: all **12** rows of Table 11-1 foot exactly)*. **The trend is nearly irrelevant over six weeks** — a loan trend moving +1 against a seasonal element of +174. **A liquidity forecast is not a growth forecast.**
- **Structure of funds weights liabilities by flight risk**: 95% behind hot money, 30% vulnerable, 15% core, **100% behind undrawn loan capacity** *(verified: 23.04 + 6.98 + 14.55 + 19.00 = **63.57** ✓)*.
- **⚠️ Liquidity risk is a property of the funding mix, not the balance sheet.** *(Computed: moving \$50mn from core to hot money raises the requirement **87%**, from 44.57 to 83.37, with the bank the same size.)*
- **⚠️ The chapter's result: a solvent bank with no defaults is destroyed by a run.** *(Computed on ch. 05's bank — 9.82% equity, every asset performing — **insolvency at withdrawals of 48.5% of liabilities**, meeting them via cash, then securities at a 7.20% haircut, then loans at 25%.)*
- **The run does not reveal insolvency; it creates it.** Forced sale is the mechanism converting a *timing* problem into a *balance-sheet* one — **[[01 - The Financial-Services Industry and Its Regulation|ch. 01]] §2, now a number.**
- **Joining a run is rational**: first out is paid in full, so each depositor's best move depends on the others'. **A coordination problem, not a credit judgement** — which is why **deposit insurance works on the payoff and not on the balance sheet**, at the cost of the moral hazard [[10 - Capital Adequacy and Basel|capital rules]] offset.
- **⚠️ The loss is already there before anyone withdraws.** *(Computed: ch. 05's +2% shock has cost the securities book **7.20% = 2,348.56 = 14.68% of equity**, invisible under held-to-maturity accounting. True equity is **13,651**; insolvency moves to **43.7%**.)*
- **That is 2023 in one line: a rate rise creates a loss the accounting hides, and a run forces its recognition.** The depositors who ran were reading [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]].
- **⚠️ Interest-rate risk and liquidity risk are one risk with two names** — the first sets the size of the loss, the second decides whether it is collected. **A duration gap is only tolerable to the extent the bank will never be forced to sell.**
- **Asset liquidity costs a certain 1,222.50 a year; borrowed liquidity costs nothing until it costs everything** *(4.50% normal → 7.50% under doubt → **unavailable**)*. **Purchased liquidity is available on exactly the days you don't need it.**
- **Basel III's LCR refuses to count borrowing capacity** — it requires high-quality liquid assets against 30 days of stressed outflows, turning §3's judgement-based weights into a binding rule.
- **⚠️ Netting out pledged securities drops the liquid-securities ratio from 20.00% to 13.00%** — the headline **overstates by 54%**. R&H lists the pledged ratio as an indicator but never nets it out of the others.
- **The industry moved one way for 22 years** *(computed: cash position **12.5% → 4.3%**, a **66% fall**; unused commitments **+114%** to **70.9% of assets**)*. **A bank benchmarking against the average would have looked normal throughout.**
- **Unused loan commitments are written options drawn at the borrower's option** — exercised when borrowers are short of cash, which is when the bank is too.

## ⚠️ Important Notes

1. **Liquidity is amounts at times, not a stock of assets.** A ratio cannot answer the actual question; the sources-and-uses flow forecast can.
2. **⚠️ The dangerous combination — deposits falling, loans rising — arrives in a boom.** "Current conditions look fine" is the least informative reassurance available.
3. **A liquidity surplus is a cost too.** Idle funds earn nothing; the target is a match, not a maximum.
4. **The seasonal and cyclical terms dominate a short-horizon forecast; the trend is nearly irrelevant.**
5. **⚠️ Liquidity risk lives in the funding mix.** Two identical balance sheets can differ 2.5× in requirement.
6. **The 95/30/15 weights are management judgement, not estimates** — R&H says so. **An optimistic classification produces a comfortable answer, and classification is what a run tests.**
7. **⚠️ Forced sale converts a timing problem into a solvency problem.** The loss is the discount, not the asset — which is why the bank survives withdrawals several times its equity, and why the damage then accelerates.
8. **A run is a coordination problem.** Being right about the assets does not protect a depositor who waits.
9. **⚠️ Held-to-maturity accounting is a liquidity assumption**, and it fails in exactly the state where it matters.
10. **⚠️ Treat interest-rate risk and liquidity risk as one exposure.** Standard reporting shows them as two, in different departments.
11. **Purchased liquidity fails in a way correlated with needing it** — raising your offered rate announces the need that closes the market.
12. **Never treat borrowing capacity as a substitute for liquid assets.** Basel III's LCR encodes this refusal.
13. **⚠️ Net encumbered securities out of every liquidity ratio.** The gross figure is the standard one, which is what makes it dangerous.
14. **Selling liquid assets first makes the balance sheet look worse as you go**, because the safe assets go first — and that feeds the run.
15. **⚠️ Unused loan commitments are written options** drawn at the borrower's option, correlated the wrong way, off balance sheet until exercised.
16. **Industry averages are no defence when the whole industry has moved.** 1985–2007 is the demonstration.
17. **A liquidity ratio that improves because loan demand collapsed is not better liquidity management.**

> [!warning] Gaps in the source material
> **⚠️ This is the best-extracting chapter in the book.** *(PDF pp. 377–414; book page $n$ = PDF page $n+18$.)* **Tables 11-1, 11-2, 11-3 and 11-4 all came through complete, with every figure** — and **all 22 internal checks pass exactly.**
>
> **This confirms [[03 - Bank Financial Statements|ch. 03]]'s corrected rule rather than the original blanket claim:** *graphical exhibits are lost; numeric tables set as text survive.* **Ch. 07's strategy diagrams were destroyed while this chapter's four data tables are intact** — in the same book, ten pages apart. **Always test; never assume either way.** *(The four standing extraction hazards in `00-Index.md` still apply — the comma-for-hyphen fault is heavy here: "liquidi,ty", "six,week", "shorteHerm".)*
>
> **Verified from the book: 22 checks, all exact.** Table 11-1's twelve decompositions, Table 11-2's five liquidity gaps, and Table 11-3's five lines including the total of **63.57**. **No erratum.**
>
> **One loose end, checked and reported as not an error.** Table 11-1's trend column increments by 2/week for deposits where compounding the stated 10% on a \$1,200mn base implies 2.31, and starts at 1,210 rather than ~1,202; loans show the same pattern. **The trend is evidently a line fitted over ten years of history rather than compounded forward from the year-end figure.** The decomposition the table actually claims is exact in all twelve rows. **Recorded because [[03 - Bank Financial Statements|ch. 03]] established that a reconstruction failing to reproduce is my inference failing, not necessarily the book's arithmetic.**
>
> **Figures that are mine**: the balance sheet in §4 (ch. 05's, unchanged), the haircuts, the borrowing spreads in §5, and the pledged fraction in §6. **The formulas, the ten indicators, the 95/30/15 weights and all four tables are the book's.**
>
> **Additions beyond the source.**
>
> - **⚠️ §4 is the chapter's main addition and is entirely mine.** **R&H explains liquidity risk thoroughly and never computes a bank failing.** The cascade model — cash, then discounted securities, then heavily discounted loans, with pledged securities unavailable — and the resulting **48.5% insolvency threshold on a bank with a 9.82% equity ratio and no defaults**, are not in the source. **It is what makes ch. 01 §2's claim ("solvency is a balance-sheet fact, liquidity is a timing fact") demonstrable rather than assertable.**
> - **⚠️ §4b — the unrealised loss under held-to-maturity accounting, moving the threshold from 48.5% to 43.7% — is mine**, and connects [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s rate shock to this chapter's run. **The 9th edition predates 2023**, so the mechanism is described from the model rather than the event; the general point (an unrealised loss is a loss awaiting a trigger, and the trigger is a liquidity event) is the addition, and it is what unifies the two chapters.
> - **§3's remix table** — showing the requirement rising **87%** on an unchanged balance sheet — is mine. **R&H works one example and never varies the mix**, which is where the method's actual content is.
> - **§5's cost comparison across market conditions** is mine; R&H lists the advantages and disadvantages of each strategy in prose without pricing them. **The asymmetry ("zero until infinite") and the observation that the funding market closes on the information revealed by needing it are additions.**
> - **§6's encumbrance netting** discharges [[07 - The Investment Portfolio|ch. 07]]'s obligation and is mine: **R&H lists the pledged-securities ratio among its ten indicators but never nets it out of the liquid-securities ratio.**
> - **§6's reading of Table 11-4** — computing the 66% fall in cash and the 114% rise in commitments, and noting both moved the same way for 22 years — is mine; the book presents the table and comments only on the 2007–09 rebound.
> - **The framing that interest-rate risk and liquidity risk are one risk with two names**, and that unused loan commitments are written options correlated the wrong way ([[06 - Hedging with Derivatives|ch. 06]] §7), are mine.
> - **Basel III's LCR** is an addition — **the 9th edition predates its implementation**, and it is included because it is the direct regulatory answer to §5's asymmetry and is examinable today. Detail belongs to [[10 - Capital Adequacy and Basel|ch. 10]].
>
> **Deliberately compressed.** **R&H §11-6 on legal reserves and money position management** — reserve computation over the maintenance period, lagged vs contemporaneous accounting, clearing balances and the discount window — **is compressed to the principle.** It is intricate, entirely specific to US Federal Reserve mechanics, and **Regulation D reserve requirements were set to zero in 2020**, so the arithmetic is now of historical interest; the *idea* (a required buffer that is not usable liquidity) is retained in §3's net-of-reserves terms. **The eight-item list of liquid-asset types** is compressed to the three defining properties. **The 9/11 liquidity case study** is omitted, though its point — that a market can stop settling — reinforces §5. **Deposit pricing and the composition of funding** are deferred to [[09 - Managing Deposits and Nondeposit Funding|ch. 09]], which owns them, even though §3 shows the mix is the liquidity risk.

**Previous:** [[07 - The Investment Portfolio]] · **Next:** [[09 - Managing Deposits and Nondeposit Funding]]
