---
subject: Commercial Banking
chapter: 1
tags: [ds, banking, intermediation, leverage, regulation, bank-runs, risk]
source: "Rose & Hudgins, *Bank Management and Financial Services* 9e, ch. 1–2"
---

# The Financial-Services Industry and Its Regulation

**A bank is a leveraged balance sheet that holds illiquid promises and funds them with callable money.** Every risk in this subject, and every regulation imposed on the industry, follows from that one structural fact.

**§2 is the number that matters:** with 9% equity, **a 5% loss on assets destroys 55.6% of the equity, and a 9% loss makes the bank insolvent while it still holds 91% of its assets.** No other industry is built this way, and it is why banking is regulated more heavily than any other.

**Every figure below is computed**, from a balance sheet I state explicitly — the book's own exhibits are images and lost (see the gaps callout).

## 📘 Main Knowledge

### 1. What a bank does

> [!note] Financial intermediation
> A bank stands between **savers** (who want safety, liquidity and small denominations) and **borrowers** (who want large, long, risky sums). **It buys one kind of claim and sells another.**

**Rose & Hudgins gives four things intermediaries provide, and each is a *transformation*:**

| transformation | savers want | borrowers want |
|---|---|---|
| **denomination** | small units | large sums |
| **risk** | low-risk claims | to borrow despite being risky |
| **liquidity** | funds available on demand | long-term commitment |
| **information** | not to have to evaluate borrowers | to be evaluated cheaply |

**The fourth is the one that justifies the bank's existence.** A bank evaluates credit better and more cheaply than a depositor could — *"their superior ability to evaluate information"* — and that expertise is the product. **[[11 - Lending - Policy, Credit Risk and Business Loans|Ch. 11]] is how it is exercised.**

**The bank's revenue is the *spread* between what it charges borrowers and pays savers**, and §4 shows why that spread is precarious.

### 2. ⚠️ The arithmetic of leverage

*(Computed from a stated balance sheet — $ millions:)*

```
ASSETS                        LIABILITIES + EQUITY
Cash & reserves       50      Deposits            850
Securities           150      Other borrowings     60
Loans (net)          760      Total liabilities   910
Premises              40      Equity capital       90
Total assets       1,000      Total L + E       1,000
```
```
equity / assets    = 9.0%
equity multiplier  = assets/equity = 11.11x
```

**A bank funds about 91% of its assets with other people's money.**

**And a small loss on assets is a large loss of equity** *(verified):*

| loan loss | equity after | **% of equity lost** | solvent? |
|---|---|---|---|
| 1% (10) | 80.0 | 11.1% | yes |
| 2% (20) | 70.0 | 22.2% | yes |
| **5% (50)** | **40.0** | **55.6%** | yes |
| **9% (90)** | **0.0** | **100.0%** | **insolvent** |
| 12% (120) | −30.0 | 133.3% | insolvent |

> [!warning] A 9% loss makes the bank insolvent while it still holds 91% of its assets
> **Nine cents in the dollar going bad is enough**, and in a recession a 5% loan-loss rate is not extraordinary.
>
> **This single table motivates the rest of the subject.** [[10 - Capital Adequacy and Basel|Ch. 10]] exists because the equity buffer is thin and regulators do not trust management to set it. [[05 - Interest-Rate Risk - Gap and Duration|Ch. 05]] and [[08 - Liquidity and Reserves Management|ch. 08]] exist because the two most likely sources of that loss are rate moves and forced sales.

### 3. Leverage is the product, not a side effect

$$\text{ROE} = \text{ROA} \times \frac{\text{Assets}}{\text{Equity}} = \text{ROA} \times \text{EM}$$

*(Verified:)*

| ROA | EM = 4 | EM = 8 | **EM = 11.11** | EM = 20 |
|---|---|---|---|---|
| 0.50% | 2.00% | 4.00% | 5.56% | 10.00% |
| **1.00%** | 4.00% | 8.00% | **11.11%** | **20.00%** |
| 1.50% | 6.00% | 12.00% | 16.67% | 30.00% |

> [!note] The same 1% ROA becomes 4% or 20% ROE purely by borrowing more
> **A 1% return on assets is a thin margin** — thinner than most industries would accept. **Only leverage turns it into a competitive return on equity.**
>
> **So leverage is what the business sells**, not an accident of financing. **And it magnifies losses by exactly the same multiple** (§2) — the identity works in both directions.
>
> **This identity is [[04 - Measuring and Evaluating Bank Performance|ch. 04]]'s core**, where it is decomposed further.

### 4. Borrowing short and lending long — the spread and its fragility

*(Verified, using the §2 balance sheet, deposits at 1% and loans at 5%:)*
```
interest income   = 910 x 5%  =  45.5
interest expense  = 910 x 1%  =   9.1
net interest income           =  36.4
net interest margin           =   4.00%
```

**Now rates rise. Deposits reprice immediately; fixed-rate loans do not:**

| rate rise | income | expense | NII | NIM |
|---|---|---|---|---|
| +0% | 45.5 | 9.1 | **36.4** | 4.00% |
| +1% | 45.5 | 18.2 | 27.3 | 3.00% |
| **+2%** | 45.5 | **27.3** | **18.2** | **2.00%** |
| +3% | 45.5 | 36.4 | 9.1 | 1.00% |

*(All verified.)*

> [!warning] The income is fixed and the expense is not
> **NII falls by (liabilities × the rate rise)**, and the bank breaks even at a rise of **4.00%** — beyond which the spread is negative.
>
> **This is the business model *and* the risk, and they are the same thing.** The bank earns a spread precisely *because* it takes maturities the market will not; **that is why the exposure cannot simply be removed.**
>
> **Measuring it is exactly what [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s gap and duration analysis does**, and [[06 - Hedging with Derivatives|ch. 06]] is how it is hedged.
>
> *(Simplification, stated: all liabilities are charged the deposit rate and all earning assets the loan rate. A real bank's repricing schedule is what ch. 05 builds properly.)*

### 5. Liquidity is not solvency

*(Verified:)*
```
liquid assets (cash + securities) = 200
deposits withdrawable             = 850
liquid / deposits                 = 23.5%
```

> [!note] The bank in §2 is solvent and could still fail
> **Assets (1 000) exceed liabilities (910), so it is solvent.** But it cannot turn 760 of loans into cash quickly, **so if more than about a quarter of depositors ask at once, it cannot pay** — even though every loan is perfectly good.
>
> **Solvency is a balance-sheet fact; liquidity is a timing fact.** Confusing them is what makes bank runs possible: **a run is rational for each depositor precisely because the bank cannot pay everyone**, so being early matters.
>
> **This is [[08 - Liquidity and Reserves Management|ch. 08]]'s subject, and it is why deposit insurance exists** — it removes the individual's reason to run.

### 6. Why banking is regulated more than any other industry

**Rose & Hudgins's reasons, and what each is really about:**

1. **Banks hold the public's savings**, and savers *"lack the financial expertise or depth of information needed to correctly evaluate the riskiness of a bank"* — so regulators gather and assess that information on their behalf. **This is an information-asymmetry argument**, not a paternalistic one.
2. **Banks create money** through deposit-taking and lending, so their behaviour affects the money supply and the economy — **the link to [[Monetary and Financial Theories/contents/00-Index|Mishkin]]'s territory.**
3. **They are the payment system.** A failure is not one firm's problem; it stops transactions between unrelated parties.
4. **Credit is a social good**, so access to it is regulated (anti-discrimination, community reinvestment, consumer protection).
5. **Failure is contagious** — §5's run logic spreads to healthy banks, because depositors cannot distinguish them.

> [!note] The unifying reason is §2
> **Every argument above is amplified by leverage.** A 9%-equity firm holding the public's money, running the payment system, and vulnerable to a rational run **is fragile in a way that an equity-financed manufacturer is not** — and its failure imposes costs on people who were never its customers.
>
> **That externality is the economic justification for regulation**, and it is why the regulatory apparatus concentrates on exactly the three risks of §7.

### 7. The three risks, and where each is handled

| risk | question | chapter |
|---|---|---|
| **credit risk** | will the loans be repaid? | [[11 - Lending - Policy, Credit Risk and Business Loans\|11]]–[[12 - Consumer, Credit Card and Real Estate Lending\|12]] |
| **interest-rate risk** | what if rates move? | [[05 - Interest-Rate Risk - Gap and Duration\|05]]–[[06 - Hedging with Derivatives\|06]] |
| **liquidity risk** | can I meet withdrawals today? | [[08 - Liquidity and Reserves Management\|08]] |
| **capital adequacy** | is there enough equity to absorb the losses the other three cause? | [[10 - Capital Adequacy and Basel\|10]] |

**Every one is a consequence of §1: a leveraged balance sheet holding illiquid promises funded by callable money.**

### 8. The competitive picture

**Two figures from the book, for scale:**
- **~6 600 US commercial banks** — the most of any country, with Germany next at ~2 500.
- **Banking's share of US financial-institution assets fell from more than two-thirds a century ago to just under one-quarter.**

> [!note] The industry did not shrink; the rest of the financial system grew around it
> Money-market funds, mutual funds, pension funds, insurers and finance companies took share by offering **one** of the bank's transformations without the others — a money-market fund gives denomination and liquidity without credit evaluation.
>
> **This is disintermediation**, and it is the competitive pressure behind [[02 - Organization, Structure and Market Entry|ch. 02]]'s consolidation and behind banks' push into fee income.

## ✏️ Exercises

**1. (Intermediation and leverage.)** (a) What four transformations does a bank perform? (b) Interpret the loss table. (c) Explain ROE = ROA × EM. (d) Why is leverage the product?

> [!example]- Solution
> **(a) Denomination, risk, liquidity and information.**
>
> **Denomination** — savers have hundreds, borrowers need millions; the bank pools. **Risk** — it accepts risky loans while issuing low-risk deposits, holding the difference against its capital. **Liquidity** — deposits are payable on demand while loans are not; §5 shows the cost of that promise. **Information** — the bank evaluates borrowers so depositors need not.
>
> **The fourth is what justifies its existence.** The first three could be provided by a fund; **credit evaluation is expertise, and it cannot be disintermediated as easily** — which is why banks retain lending even as they lose share elsewhere (§8).
>
> **(b)** *(Verified with 9% equity:)*
>
> | loss on assets | equity destroyed |
> |---|---|
> | 1% | 11.1% |
> | 5% | **55.6%** |
> | 9% | **100% — insolvent** |
>
> **The multiplier is exactly the equity multiplier, 11.11×.** A 1% asset loss is an 11.1% equity loss because equity is 1/11.11 of assets.
>
> **The 9% row is the one to remember: the bank is insolvent while still holding 91% of its assets.** Every loan but one in eleven is fine, and the firm is gone.
>
> **And 5% is not a remote scenario.** In a serious recession, loan-loss rates of that order occur — which is why the buffer is regulated rather than chosen.
>
> **(c)** $$\text{ROE}=\frac{\text{NI}}{\text{Equity}}=\frac{\text{NI}}{\text{Assets}}\times\frac{\text{Assets}}{\text{Equity}}=\text{ROA}\times\text{EM}$$
>
> **It is an identity, not a theory** — `Assets` cancels. Its content is that **profitability for shareholders has exactly two sources: how well the assets earn, and how many assets are supported per unit of equity.**
>
> *(Verified: 1% ROA gives 4% ROE at EM = 4 and **20% at EM = 20**.)*
>
> **[[04 - Measuring and Evaluating Bank Performance|Ch. 04]] decomposes it further** into margin, asset utilisation and leverage — but this two-term version already separates *operating* skill from *financing* choice, which is the distinction that matters.
>
> **(d) Because a 1% ROA is not a viable return on equity, and leverage is what converts it.**
>
> **Banking is a thin-margin business.** A 1% return on assets is normal and would be a poor business if equity-financed. **At 11× leverage it becomes an 11% ROE, which is competitive.**
>
> **So leverage is not a financing decision taken after the business is designed — it *is* the design.** A bank that deleveraged to a manufacturer's capital structure would earn a return no shareholder would accept.
>
> **Which sets up the central tension of the subject.** **Shareholders want more leverage; regulators want less** — and they are arguing about the same identity, one looking at §3 and the other at §2. **[[10 - Capital Adequacy and Basel|Ch. 10]] is where that argument is settled by rule.**

**2. (Hard — the spread and its risks.)** (a) Explain the spread arithmetic. (b) Why can the exposure not simply be removed? (c) Distinguish liquidity from solvency. (d) Why does that make runs rational?

> [!example]- Solution
> **(a)** *(Verified: deposits 1%, loans 5%, earning assets 910.)*
> ```
> interest income  45.5  -  interest expense 9.1  =  NII 36.4,  NIM 4.00%
> ```
> **A rate rise hits only the expense side**, because deposits reprice quickly and fixed-rate loans do not:
>
> | +1% | +2% | +3% |
> |---|---|---|
> | NII 27.3 | **NII 18.2** | NII 9.1 |
>
> **NII falls by (liabilities × the shock)** — a linear relationship, and the bank **breaks even at a 4.00% rise** *(verified)*, which is the original spread.
>
> **The asymmetry is the whole point.** Assets and liabilities have different *repricing speeds*, so a parallel rate move is not neutral. **Quantifying that mismatch is [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s repricing gap.**
>
> **(b) Because the exposure and the revenue are the same thing.**
>
> **The bank earns 4% because it takes a maturity mismatch the market will not.** Savers want their money back on demand; borrowers want thirty-year mortgages. **Somebody must bear the mismatch, and being paid to bear it is the business.**
>
> **So a bank that matched every maturity exactly would eliminate interest-rate risk and its margin with it** — it would be a fee-charging broker, not a bank.
>
> **The task is therefore not elimination but *measurement and control*:**
> - **measure it** — gap and duration ([[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]);
> - **set a tolerance** — a policy limit on how much NII may move per 1% shock;
> - **hedge the excess** — swaps, futures, options ([[06 - Hedging with Derivatives|ch. 06]]), which transfer the risk without changing the loans;
> - **hold capital against what remains** ([[10 - Capital Adequacy and Basel|ch. 10]]).
>
> **This is the shape of every risk in the subject: it is priced, not avoided.**
>
> **(c) Solvency is about *values*; liquidity is about *timing*.**
>
> **Solvent** means assets exceed liabilities — a balance-sheet fact. **Liquid** means you can produce cash when it is demanded — a timing fact.
>
> *(Verified: the §2 bank has assets of 1 000 against liabilities of 910 — comfortably solvent — and just **23.5%** of its deposits available as liquid assets.)*
>
> **So it can be solvent and fail.** Every loan may be perfectly good and still not be cash today; forcing their sale means accepting a discount, **which turns a liquidity problem into a solvency problem.** That feedback is what makes liquidity crises fast.
>
> **The reverse also holds**: an insolvent bank can keep paying for a long time if funding continues, which is why failures are often recognised late.
>
> **(d) Because with only 23.5% liquidity, being early genuinely matters.**
>
> **The bank pays depositors in the order they arrive**, and it can pay only about a quarter of them from liquid assets. **So a depositor who believes others will withdraw should withdraw** — not because the bank is unsound, but because the queue is real.
>
> **That makes the run self-fulfilling.** The belief that others will run is sufficient reason to run, and enough people running makes the bank fail — **so the belief becomes true regardless of whether it started true.**
>
> **And it is contagious** (§6), because depositors cannot distinguish a sound bank from an unsound one and the safe response to uncertainty is to withdraw from both.
>
> **Deposit insurance is the standard fix, and it works by changing the incentive rather than the balance sheet.** If your deposit is guaranteed, being early buys nothing, so you do not queue — **and the run does not start.**
>
> *(The cost is moral hazard: insured depositors stop caring about bank risk, so the discipline they would have imposed must be replaced by supervision and capital rules — [[10 - Capital Adequacy and Basel|ch. 10]]. **The regulation exists to replace the market discipline the insurance removed.**)*

**3. (Regulation and competition.)** (a) Why is banking regulated more heavily? (b) What unifies those reasons? (c) What did banking's falling share mean? (d) How does this chapter frame the subject?

> [!example]- Solution
> **(a) Five reasons, from the book:** banks hold the public's savings and savers cannot evaluate bank risk; banks create money; they run the payment system; credit access is treated as a social good; and failure is contagious.
>
> **The first is explicitly an information argument** — R&H says savers *"lack the financial expertise or depth of information needed to correctly evaluate the riskiness of a bank"*, so regulators gather that information on their behalf. **That is a market-failure justification, not a paternalistic one**: the service being provided is assessment that individuals cannot efficiently produce.
>
> **(b) Leverage plus externality.**
>
> **Every reason is amplified by §2's capital structure.** A firm financed 91% by other people's money, whose failure is triggerable by a rational run (§5), **is fragile in a way an equity-financed firm is not.**
>
> **And the costs of failure fall on people who were never its customers** — payments stop, credit contracts, and other banks face runs. **That externality is the economic case for regulation**: the bank's private calculation of how much risk to bear leaves out the costs it imposes on everyone else.
>
> **Which explains what regulation actually regulates.** Not prices or products, but **capital** ([[10 - Capital Adequacy and Basel|ch. 10]]), **liquidity** ([[08 - Liquidity and Reserves Management|ch. 08]]) and **risk-taking** — precisely the three channels through which the externality operates.
>
> **(c) That the rest of the financial system grew, not that banking shrank.**
>
> **From more than two-thirds of US financial-institution assets a century ago to just under a quarter** — but in absolute terms banking is far larger than it was.
>
> **Competitors took share by unbundling.** A money-market fund offers **denomination and liquidity** transformation without credit evaluation; a finance company offers **credit** without deposits; a pension fund offers **maturity** transformation without payments. **Each competitor does one of the bank's four jobs (§1) and avoids the others** — and so avoids the capital requirements that come with them.
>
> **The consequences run through the subject:** pressure on the spread (§4), a push into **fee income** that does not consume capital, and **consolidation** to recover scale economies — [[02 - Organization, Structure and Market Entry|ch. 02]].
>
> *(It is also why "bank" is a slippery term. R&H's own title says *Financial Services* — the legal definition matters mainly because it determines who is regulated, which is exactly what unregulated competitors are avoiding.)*
>
> **(d) As one structure with four consequences.**
>
> **§1's transformations create the business; §2's leverage makes it fragile; §4 shows the spread and the rate risk are the same thing; §5 shows solvency and liquidity are different problems.** Everything after this chapter is one of those four being measured or controlled:
>
> | | measured in | controlled in |
> |---|---|---|
> | the spread | [[04 - Measuring and Evaluating Bank Performance\|ch. 04]] | [[09 - Managing Deposits and Nondeposit Funding\|ch. 09]] |
> | rate mismatch | [[05 - Interest-Rate Risk - Gap and Duration\|ch. 05]] | [[06 - Hedging with Derivatives\|ch. 06]] |
> | liquidity | [[08 - Liquidity and Reserves Management\|ch. 08]] | [[07 - The Investment Portfolio\|ch. 07]] |
> | credit quality | [[03 - Bank Financial Statements\|ch. 03]] | [[11 - Lending - Policy, Credit Risk and Business Loans\|ch. 11]]–[[12 - Consumer, Credit Card and Real Estate Lending\|ch. 12]] |
> | **all of them at once** | | **[[10 - Capital Adequacy and Basel\|ch. 10]]** |
>
> **Capital is the residual.** It is what absorbs whatever the other four controls fail to prevent — **which is why §2's table is the single most important arithmetic in the subject.**

## 📝 Summary

- **A bank performs four transformations — denomination, risk, liquidity and information** — and the fourth, credit evaluation, is what justifies its existence and is hardest to disintermediate.
- **Its revenue is a spread**, and §4 shows why that spread is fragile.
- **⚠️ A bank funds ~91% of assets with other people's money** *(computed: equity/assets **9.0%**, equity multiplier **11.11×**)*.
- **⚠️ So a 5% loss on assets destroys 55.6% of equity, and a 9% loss makes the bank insolvent while it still holds 91% of its assets** *(verified)*. **This single table motivates the rest of the subject.**
- **ROE = ROA × EM is an identity** *(verified: 1% ROA gives 4% ROE at EM 4 and **20% at EM 20**)*. **Leverage is the product, not a side effect** — a 1% ROA is only a viable return on equity because of it.
- **Hence the subject's central tension: shareholders want more leverage, regulators want less**, and they are reading the same identity from opposite ends.
- **Borrowing short and lending long earns the spread and *is* the risk** *(verified: a +2% rate rise cut NIM from 4.00% to 2.00%; break-even at +4.00%)*. **NII falls by liabilities × the shock.**
- **The exposure cannot be removed without removing the revenue** — so it is measured ([[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]), limited, hedged ([[06 - Hedging with Derivatives|ch. 06]]), and capitalised ([[10 - Capital Adequacy and Basel|ch. 10]]).
- **Liquidity is not solvency** *(verified: the bank is solvent — assets 1 000 vs liabilities 910 — with only **23.5%** of deposits liquid)*. **Solvency is a balance-sheet fact; liquidity is a timing fact.**
- **That gap makes runs rational and self-fulfilling**, and contagious because depositors cannot tell sound banks from unsound ones. **Deposit insurance works by removing the incentive to be early** — at the cost of moral hazard, which capital regulation then has to replace.
- **Banking is regulated because leverage plus externality**: a fragile firm whose failure harms people who were never its customers. **So regulation targets capital, liquidity and risk-taking** — the channels the externality runs through.
- **Banking's share of US financial assets fell from over two-thirds to just under a quarter** *(book figures)* — **by competitors unbundling one transformation each and avoiding the capital rules that come with the rest.**

## ⚠️ Important Notes

1. **Read every bank statement leverage-first.** The equity multiplier tells you how much a given asset loss costs shareholders before you look at anything else.
2. **⚠️ A loan-loss rate equal to the equity ratio is insolvency.** At 9% equity, a 9% loss ends the firm.
3. **ROE = ROA × EM is an identity, so a high ROE says nothing on its own** — it may be operating skill or it may be leverage, and they carry very different risk.
4. **Always ask which term is driving an ROE comparison** before concluding one bank outperforms another.
5. **NII falls by roughly (repricing liabilities × the rate shock).** That is the back-of-envelope version of [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s gap.
6. **A bank cannot hedge away all interest-rate risk without hedging away its margin.** Treat it as priced, not avoided.
7. **⚠️ Never treat solvency and liquidity as the same question.** A solvent bank can fail this afternoon; an insolvent one can keep paying for years.
8. **Forced asset sales convert a liquidity problem into a solvency problem** — which is why liquidity crises move fast.
9. **A run is rational for the individual even when the bank is sound.** Do not model depositor behaviour as irrational panic.
10. **Deposit insurance stops runs by changing incentives, not balance sheets** — and its cost is moral hazard, which is why capital regulation exists alongside it.
11. **Regulation targets capital, liquidity and risk-taking** because those are the channels through which one bank's failure harms outsiders.
12. **When a competitor "does what a bank does more cheaply", check which transformation it is *not* doing** — usually credit evaluation, and usually the capital requirement with it.

> [!warning] Gaps in the source material
> **Rose & Hudgins chapters 1–2 extract as clean prose** — the intermediation discussion, the list of services, the reasons for regulation, and the regulatory-agency descriptions all came through readably. **Book page $n$ = PDF page $n+18$; ch. 1–2 are PDF pages 19–82.**
>
> **⚠️ Four extraction hazards, all recorded in the subject file and all encountered here:**
> 1. **A watermark is interleaved with the body text on every page** (`Username: …`, `No part of any book may be reproduced…`) and must be stripped or it corrupts the extraction.
> 2. **Hyphens sometimes render as commas** — `Financial,Services`, `Asset,Liability`, `disas,ter`. Read `,` as `-` inside a hyphenated word.
> 3. **The PDF outline is unusable** — bookmarks are scan-sheet numbers at ten-page intervals, so the chapter list had to be recovered from the Brief Contents pages.
> 4. **The file is 554 MB and whole-book scans time out**; only targeted page ranges are workable.
>
> **⚠️ ALL EXHIBITS AND TABLES ARE IMAGES AND ARE LOST.** *(Verified twice: on the Exhibit 6-1 page only the caption survives, and Exhibit 1-2's **row labels** extract while every number does not.)*
>
> **This is the most serious limitation in the subject**, because R&H teaches through financial statements. **Consequently the balance sheet in §2 is my own**, stated explicitly, with round figures chosen so the arithmetic is checkable by eye. **Every ratio, spread and shock figure in this note is computed from it in Python.** Nothing is reconstructed from a partial table.
>
> **What *is* the book's:** the four intermediation transformations, the five reasons for regulation (quoted in part), the ~6 600 US banks and ~2 500 German banks, and the fall from "more than two-thirds" to "just under one-quarter" of US financial-institution assets.
>
> **No error was found in Rose & Hudgins ch. 1–2** — though with the exhibits lost, only prose claims could be checked.
>
> **Additions beyond the source.** **R&H ch. 1–2 is descriptive: what banks do, what services they sell, who regulates them. Every quantitative element here is added:**
>
> - **§2's leverage table is mine**, and it is the chapter's organising result. **R&H discusses capital adequacy in ch. 15; showing at the outset that a 9% loss ends a 9%-equity bank is what makes the rest of the subject feel necessary** rather than procedural.
> - **§3's ROE = ROA × EM table is an addition here** — R&H introduces the identity in ch. 6, but **stating it in chapter 1 is what turns "banks are leveraged" into "leverage is the product".** The framing that shareholders and regulators are reading the same identity from opposite ends is mine.
> - **§4's rate-shock table is mine**, including the computed **4.00% break-even**, and the argument that **the exposure cannot be removed without removing the revenue** — which R&H does not state this directly.
> - **§5's liquidity-versus-solvency computation, and §6's derivation of run dynamics from it**, are additions. **The point that a run is rational for the individual** — and that deposit insurance therefore works on incentives rather than balance sheets, at the cost of moral hazard that capital rules must replace — is my own framing.
> - **§6's synthesis that all five regulatory reasons reduce to leverage plus externality** is mine.
> - **The unbundling explanation of §8's market-share decline** — each competitor performing one of §1's transformations and avoiding the capital rules attached to the others — is an addition.
>
> **Deliberately compressed.** **R&H ch. 1's catalogue of bank services** (trust, brokerage, insurance, cash management, merchant banking, …) is a list; the structurally important ones appear where they matter — fee income in [[04 - Measuring and Evaluating Bank Performance|ch. 04]], investment services in [[07 - The Investment Portfolio|ch. 07]]. **Ch. 2's detailed tour of US regulatory agencies** (OCC, FDIC, Federal Reserve, state authorities, and the alphabet of acts from Glass-Steagall to Dodd-Frank) **is summarised rather than reproduced** — it is jurisdiction-specific, dates quickly, and the transferable content is *why* regulation exists (§6) rather than which agency does what in one country. **The career-opportunities appendix** is omitted. **The money-creation and monetary-policy material is deferred to [[Monetary and Financial Theories/contents/00-Index|Mishkin]]**, per the boundary recorded in `00-Index.md`.

**Previous:** [[00-Index]] · **Next:** [[02 - Organization, Structure and Market Entry]]
