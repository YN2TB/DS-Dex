---
subject: Commercial Banking
chapter: 3
tags: [ds, banking, financial-statements, balance-sheet, loan-loss-allowance, provisioning, accounting]
source: "Rose & Hudgins, *Bank Management and Financial Services* 9e, ch. 5"
---

# Bank Financial Statements

**A bank's balance sheet is the ordinary accounting equation with unusual contents.** Assets are mostly *loans*; liabilities are mostly *deposits*; equity is thin. [[Principle of Accounting/contents/02 - The Accounting Equation|Accounting ch. 02]]'s equation is unchanged — only what fills each side is different.

**This chapter is unusual in the subject because the book's actual figures survived extraction.** R&H's BB&T Corporation Report of Condition came through with full numbers, so §2 **verifies the book's own statement** rather than a schema of my own — and §3 puts [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s leverage arithmetic on a real bank.

**§4 is the chapter's substantive point.** The **allowance for loan losses** means a bank's reported earnings depend on **management's estimate of future losses**, not on losses actually incurred — and §5 shows that estimate moving net income by **47%** with nothing about the loans changing.

## 📘 Main Knowledge

### 1. The two statements

| | | |
|---|---|---|
| **Report of Condition** | the balance sheet | a **stock**, at a point in time |
| **Report of Income** | the income statement | a **flow**, over a period |

**R&H's framing: the balance sheet shows the *sources* of funds and how they were *allocated*; the income statement shows what those funds cost and what they earned.**

**This is [[Principle of Accounting/contents/00-Index|Accounting]] applied**, with one structural difference worth noting: **for a bank, loans are receivables** — so the allowance-for-loan-losses logic in §4 is the same machinery as the allowance for doubtful accounts, at much larger scale and with far more discretion.

### 2. Verifying the book's own balance sheet

**BB&T Corporation, Report of Condition, 12/31/2009, $ thousands** *(as printed in R&H)*:

| assets | |
|---|---|
| Cash and due from depository institutions | 1 623 978 |
| Securities | 33 252 255 |
| Federal funds & reverse repos | 397 592 |
| **Net loans and leases** | **103 606 716** |
| Trading account assets | 1 098 289 |
| Bank premises and fixed assets | 1 582 808 |
| Other real estate owned | 1 623 417 |
| Goodwill and miscellaneous other assets | 21 681 734 |
| **Total assets (stated)** | **165 764 218** |

**Checks that pass exactly** *(computed)*:
```
gross loans           106,207,386
less loan loss allow.  -2,600,670
less unearned income            0
= net loans           103,606,716      MATCHES the stated figure

equity components (common stock + surplus + retained earnings
                   + miscellaneous) = 16,190,879
stated total equity capital          = 16,190,879      EXACT, both years
```

> [!note] The totals do not foot — and it is an abridged table, not an error
> *(Computed for both years:)*
>
> | | 2009 | 2008 |
> |---|---|---|
> | equity components vs stated | **0** | **0** |
> | liability items vs stated | +450 | +50 |
> | **(liabilities + equity) vs total assets** | **−49 742** | **−44 227** |
>
> **The shortfall is consistent across both years** (~0.03% of assets), and **every subtotal that can be checked internally is exact.**
>
> **That pattern indicates an omitted line item, not a mistake.** A consistent gap of similar magnitude in two independent years is what an abridged table looks like — most plausibly **minority interest / noncontrolling interests**, which sits between liabilities and equity in bank regulatory reporting and belongs to neither.
>
> **So this is *not* filed as an erratum.** The check was worth running: it confirmed the extraction is reliable where it can be verified, and it identified the discrepancy as structural rather than arithmetic. *(The printed exhibit is an image and is lost, so the omitted line cannot be confirmed directly — which is itself why the conclusion is stated as an inference.)*

### 3. What the structure says — [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s arithmetic on a real bank

*(Computed from the figures above:)*

| | BB&T 2009 | ch. 01's model bank |
|---|---|---|
| **equity / assets** | **9.77%** | 9.00% |
| **equity multiplier** | **10.24×** | 11.11× |
| deposits / assets | 69.37% | 85.00% |
| **net loans / assets** | **62.50%** | 76.00% |
| securities / assets | 20.06% | 15.00% |
| cash + securities + fed funds / assets | 21.28% | 20.00% |

> [!note] The model bank was not a caricature
> **9.77% equity against the model's 9.00%**, and a similar liquid-asset share. **[[01 - The Financial-Services Industry and Its Regulation|Ch. 01]] §2's conclusion transfers directly: a loss of 9.77% of assets would wipe out BB&T's equity.**
>
> **And loans are 62.5% of assets** — the bank *is* its loan book, which is why credit risk dominates ([[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]]–[[12 - Consumer, Credit Card and Real Estate Lending|ch. 12]]) and why §4's allowance is the most consequential estimate in the accounts.

### 4. The allowance for loan losses

> [!note] Definitions
> **ALL (allowance for loan losses)** — a **contra-asset** account on the balance sheet: an accumulated reserve against which uncollectible loans are charged off.
> **PLL (provision for loan losses)** — the **non-cash expense** on the income statement that adds to the ALL.

**R&H's worked example, recomputed** *(all matches)*:
```
ALL held                              $100 mn
anticipated losses this year          $  1 mn

Report of Income   : PLL = $1 mn            (non-cash expense)
Report of Condition: ALL = 100 + 1 = $101 mn      book states $101mn  MATCHES

then actual write-offs total $0.5 mn:
                     ALL = 101 - 0.5 = $100.5 mn
```

> [!warning] Writing off a bad loan does not touch current income
> **A charge-off reduces the ALL and reduces gross loans by the same amount.** Net loans and total assets fall; **the income statement is untouched.**
>
> **The income hit happened earlier, through the PLL** — which was based on *management's estimate*.
>
> **So a bank's reported earnings depend on an estimate of future losses, not on losses actually realised.** That is the single largest source of discretion in a bank's accounts, and §5 measures it.

### 5. ⚠️ How much discretion that is

*(Computed — the same bank, the same loan book, three provision choices; pre-provision earnings $2 000 mn, 30% tax:)*

| PLL | pre-tax | net income | vs the lowest provision |
|---|---|---|---|
| 500 | 1 500 | **1 050** | — |
| 800 | 1 200 | 840 | −20.0% |
| **1 200** | 800 | **560** | **−46.7%** |

**A 140% swing in the provision moves net income by 47%.** Nothing about the loans changed; only the estimate did.

**And BB&T's own allowance ratio shows the estimate moving in practice** *(computed)*:

| | ALL / gross loans |
|---|---|
| 12/31/2008 | **1.60%** |
| 12/31/2009 | **2.45%** |
| change | **+0.85 pp — a 54% increase in the ratio** |

> [!note] The financial crisis, visible in one line of the balance sheet
> **BB&T's allowance ratio rose by more than half in a single year.** No individual loan had to default for that to happen — **management's estimate of future credit losses rose**, and the provision that produced it went through the income statement.
>
> **This is why analysts look at the allowance ratio and the charge-off history rather than reported earnings alone** ([[04 - Measuring and Evaluating Bank Performance|ch. 04]]). **A bank can smooth earnings by under-providing in bad years and over-providing in good ones** — and the accounts will still balance.

### 6. Off-balance-sheet items

**Loan commitments, standby letters of credit and derivatives positions create real exposure without appearing among the assets.**

> [!note] So the leverage computed in §3 is a lower bound
> **A bank's true exposure can exceed what the balance sheet shows** — which is exactly why [[10 - Capital Adequacy and Basel|ch. 10]]'s capital rules assign **risk weights to off-balance-sheet items** rather than ignoring them. **A framework that only counted balance-sheet assets could be evaded by moving exposure off it**, and in the run-up to 2008, it was.

## ✏️ Exercises

**1. (The statements.)** (a) What does each statement answer? (b) How does a bank's balance sheet differ from a manufacturer's? (c) What did §2's checks establish? (d) Why not file an erratum?

> [!example]- Solution
> **(a)** The **Report of Condition** is a *stock*: what is owned, owed and owned outright at an instant. The **Report of Income** is a *flow*: what was earned and spent over a period.
>
> **The accounting equation is unchanged** — [[Principle of Accounting/contents/02 - The Accounting Equation|Accounting ch. 02]]'s $A = L + E$ holds exactly. **Only the contents are unusual.**
>
> **(b) In three ways, and all three drive the rest of the subject.**
>
> | | manufacturer | bank |
> |---|---|---|
> | main asset | inventory, plant | **loans** (62.5% of assets) |
> | main liability | trade credit, bonds | **deposits** (69.4%) |
> | equity share | 30–60% typical | **9.77%** |
>
> **The assets are financial claims**, so their value depends on someone else's willingness to pay — credit risk. **The liabilities are callable on demand**, so timing matters — liquidity risk. **And equity is thin**, so neither has much room to go wrong.
>
> **(c) That the extraction is reliable and the internal arithmetic is sound.**
>
> *(Verified: net loans = gross − allowance − unearned, exactly; **equity components summed to the stated total exactly in both years**.)*
>
> **The exactness of the equity check across two independent years is what makes the extraction trustworthy** — four components in 2009 and five in 2008, both footing to the cent.
>
> **(d) Because the discrepancy is consistent across years, which points to an omitted line rather than an error.**
>
> *(Computed: liabilities + equity fell short of total assets by **49 742** in 2009 and **44 227** in 2008 — both about 0.03%.)*
>
> **A typo produces one discrepancy, not two of similar relative size in different years.** A systematically omitted category produces exactly this pattern — most plausibly **minority interest**, which in bank regulatory reporting sits between liabilities and equity and belongs to neither.
>
> **The printed exhibit is an image and is lost**, so the omitted line cannot be confirmed directly. **That is why the conclusion is stated as an inference and the errata table stays empty.**
>
> **The general discipline is worth naming: before recording an error in a source, rule out your own extraction and rule out an abridged presentation.** The check was still worth running — it established which figures can be trusted.

**2. (Hard — the allowance.)** (a) Trace the ALL/PLL mechanics. (b) Why does a charge-off not affect income? (c) How much discretion is there? (d) What should an analyst look at?

> [!example]- Solution
> **(a)** *(R&H's example, recomputed and matching:)*
>
> 1. **The bank estimates $1 mn of losses this year.**
> 2. **Income statement:** a **provision (PLL)** of $1 mn is charged against revenue — **a non-cash expense**.
> 3. **Balance sheet:** the **allowance (ALL)** rises from $100 mn to **$101 mn** — the book's stated figure.
> 4. **Later, actual write-offs of $0.5 mn occur:** ALL falls to **$100.5 mn**, and gross loans fall by $0.5 mn.
>
> **The two accounts are linked but sit on different statements**: the PLL is the flow that feeds the ALL, which is the stock that absorbs the losses.
>
> **(b) Because the income was already charged when the provision was made.**
>
> **A charge-off is a balance-sheet event only**: reduce the ALL, reduce gross loans by the same amount. **Net loans and total assets fall; the income statement is untouched.**
>
> **This is deliberate and it is good accounting.** It matches the *expense* to the period in which the risk was incurred rather than the period in which the borrower finally failed — **which is the matching principle** ([[Principle of Accounting/contents/00-Index|Accounting]]) applied to credit.
>
> **But it has a consequence: reported earnings reflect an *estimate*, not an outcome.** The bank charges income when it *expects* losses, so **the number that determines profit is a forecast made by the people whose performance it measures.**
>
> **(c) Enough to move net income by nearly half.**
>
> *(Computed: with $2 000 mn pre-provision earnings and 30% tax, a provision of 500 gives **1 050** of net income and a provision of 1 200 gives **560** — a **46.7%** difference.)*
>
> **Nothing about the loan book changed between those three columns.** Only the estimate.
>
> **And the discretion is used in both directions:**
> - **Under-provide** in a bad year to protect reported earnings — which leaves the bank under-reserved when losses actually arrive.
> - **Over-provide** in a good year to bank reserves for later — *"cookie-jar" reserving*, which smooths earnings and is what accounting standards have progressively tried to constrain.
>
> **It is not fraud in either direction; it is judgement**, which is precisely why it is hard to police. *(The post-crisis move to expected-credit-loss models — IFRS 9, CECL — was an attempt to make the estimate more rule-driven and forward-looking, and it postdates this edition.)*
>
> **(d) The allowance ratio, the charge-off history, and their relationship.**
>
> *(Computed for BB&T: ALL/gross loans rose from **1.60%** to **2.45%** between 2008 and 2009 — **a 54% increase in the ratio**.)*
>
> **That single line shows the financial crisis** without any loan having to default: management's estimate of future losses rose sharply, and the provision that produced it went through earnings.
>
> **What to check:**
> 1. **ALL / gross loans over time** — is the reserve keeping pace with the risk in the book?
> 2. **Net charge-offs / gross loans** — what is actually going bad?
> 3. **The ratio of the two** — an allowance far below recent charge-offs suggests under-reserving; far above suggests either caution or smoothing.
> 4. **Non-performing loans / gross loans** — the leading indicator that should drive the allowance.
>
> **The point is that reported earnings alone cannot distinguish a well-run bank from an under-reserved one**, which is why [[04 - Measuring and Evaluating Bank Performance|ch. 04]] uses a battery of ratios rather than a single profit figure.

**3. (Structure and what is missing.)** (a) What do the ratios say? (b) Why do loans dominate? (c) What are off-balance-sheet items and why do they matter? (d) What is the chapter's lesson?

> [!example]- Solution
> **(a) That [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s model bank was realistic.**
>
> *(Computed for BB&T 2009: equity/assets **9.77%**, equity multiplier **10.24×**, deposits/assets **69.4%**, net loans/assets **62.5%**.)*
>
> **The model bank in ch. 01 had 9.0% equity and an 11.11× multiplier** — close enough that its conclusions transfer without adjustment. **A loss of 9.77% of BB&T's assets would have eliminated its equity.**
>
> **The main difference is funding mix**: the model bank was 85% deposit-funded, BB&T 69%, with more borrowed funds and subordinated debt. **That is a real choice with consequences for [[08 - Liquidity and Reserves Management|liquidity]] and cost** — deposits are cheaper and stickier, wholesale funding is faster to leave ([[09 - Managing Deposits and Nondeposit Funding|ch. 09]]).
>
> **(b) Because lending is the service the bank uniquely provides.**
>
> **[[01 - The Financial-Services Industry and Its Regulation|Ch. 01]] §1's four transformations** — denomination, risk, liquidity, information — **and the fourth, credit evaluation, is the one competitors could not replicate.** Loans at 62.5% of assets is that expertise on the balance sheet.
>
> **It also explains the risk hierarchy.** With loans at 62.5% and equity at 9.77%, **credit risk is arithmetically the dominant exposure**: a 15% loss on the loan book alone destroys the firm. Securities are 20% of assets and far safer; cash earns nothing.
>
> **So the balance sheet's shape *is* the business model**, and reading it tells you which risk chapter matters most for a given bank.
>
> **(c) Commitments, standby letters of credit and derivatives — exposure without an asset entry.**
>
> **A loan commitment is a promise to lend if asked.** It creates real exposure — the borrower will draw precisely when they are in trouble — **but until drawn there is no asset and no funding.**
>
> **Why it matters:**
> 1. **§3's leverage is a lower bound.** True exposure exceeds what the statement shows.
> 2. **It is an obvious avenue for evasion.** A capital rule counting only balance-sheet assets can be satisfied by moving exposure off it — **which is why [[10 - Capital Adequacy and Basel|ch. 10]]'s framework assigns risk weights to off-balance-sheet items via credit-conversion factors.**
> 3. **In the run-up to 2008 this is exactly what happened**, through off-balance-sheet vehicles that returned to the balance sheet when they failed.
>
> **The general lesson: any measure computed from the balance sheet alone can be managed by moving things off it.**
>
> **(d) The statement is an estimate presented as a fact, and knowing which parts are which is the skill.**
>
> **Some figures are observations**: cash held, deposits owed, securities at market. **Others are judgements**: the allowance for loan losses, goodwill, the fair value of illiquid securities.
>
> **The allowance is the largest and most consequential judgement** — §5 showed it moving net income by 47% — **and it is made by the people whose performance it measures.**
>
> **So reading a bank's accounts means asking, line by line, "is this counted or estimated?"** and treating the estimated lines as a range rather than a number.
>
> **This is the same discipline the technical subjects arrived at from the other direction.** [[Database Management Systems/contents/07 - Database Design|DBMS ch. 07]] asked which business rules the schema actually *enforced* rather than merely stated; here the question is which figures the accounts actually *observe* rather than merely estimate. **In both cases the answer is fewer than it appears, and the gap is where the risk lives.**

## 📝 Summary

- **The accounting equation is unchanged; only the contents are unusual** — assets are **loans**, liabilities are **deposits**, equity is thin.
- **⚠️ The book's own balance sheet extracted with full figures**, so §2 verifies R&H rather than a constructed schema — the only chapter so far where that is possible.
- **Checks that pass exactly:** net loans = gross − allowance − unearned; **equity components sum to the stated total exactly in both years.**
- **The totals do not foot** — liabilities + equity fell short of total assets by **49 742 (2009)** and **44 227 (2008)**, ~0.03% each year. **The consistency across years indicates an omitted category (most plausibly minority interest), not an error — so no erratum is filed.**
- **BB&T 2009: equity/assets **9.77%**, equity multiplier **10.24×**, net loans/assets **62.5%**, deposits/assets **69.4%*** *(all computed)*. **[[01 - The Financial-Services Industry and Its Regulation|Ch. 01]]'s model bank was realistic**, and its conclusion transfers: a 9.77% asset loss wipes out equity.
- **The ALL is a contra-asset; the PLL is the non-cash expense that feeds it.** *(R&H's example recomputed and matching: 100 + 1 = **101**, then −0.5 = **100.5**.)*
- **⚠️ Writing off a bad loan does not touch current income** — the charge went through earlier, via the provision. **So reported earnings depend on management's *estimate* of future losses.**
- **⚠️ That estimate is worth ~47% of net income** *(computed: provisions of 500 vs 1 200 give net income of **1 050** vs **560**)* — with nothing about the loans changing.
- **BB&T's allowance ratio rose from 1.60% to 2.45% in one year — a 54% increase** *(computed)*. **The crisis, visible in one balance-sheet line, with no loan needing to default.**
- **So analysts read the allowance ratio, charge-offs and non-performing loans, not just reported profit.**
- **Off-balance-sheet items create exposure with no asset entry**, so §3's leverage is a lower bound — and **any measure computed from the balance sheet alone can be managed by moving things off it.**

## ⚠️ Important Notes

1. **Read a bank's balance sheet as loans-and-deposits first.** The proportions tell you which risk chapter matters most for that bank.
2. **⚠️ Before recording an error in a source, rule out your own extraction and an abridged presentation.** A discrepancy consistent across two years is a missing line, not a typo.
3. **Check the internal subtotals that must hold** (net loans, equity components) before trusting any figure from an extracted table.
4. **⚠️ Distinguish observed figures from estimated ones.** Cash and deposits are counted; the allowance, goodwill and illiquid fair values are judged.
5. **⚠️ Reported earnings reflect an estimate of future losses, not realised ones.** The provision is where that estimate enters.
6. **A charge-off is a balance-sheet event only** — it never touches current income, so a rising charge-off rate can coexist with stable reported profit.
7. **Track ALL / gross loans over time**, and against net charge-offs and non-performing loans. Divergence signals under- or over-reserving.
8. **Suspect earnings smoothing in both directions** — under-providing in bad years, over-providing in good ones. Neither is fraud; both distort.
9. **Off-balance-sheet exposure means computed leverage is a lower bound.** Ask what commitments and guarantees exist.
10. **Any ratio built from the balance sheet alone can be evaded by moving exposure off it** — which is why capital rules use risk weights and conversion factors ([[10 - Capital Adequacy and Basel|ch. 10]]).
11. **Loans are receivables.** The allowance logic is [[Principle of Accounting/contents/00-Index|Accounting]]'s allowance for doubtful accounts, at far larger scale and with far more discretion.

> [!warning] Gaps in the source material
> **Rose & Hudgins ch. 5 extracts as clean prose, and — unusually — one major table extracted with its figures intact.** **Book page $n$ = PDF page $n+18$; ch. 5 is PDF pages 147–184.** *(The four standing extraction hazards in `00-Index.md` all apply.)*
>
> **⚠️ This chapter corrects an over-general finding recorded earlier.** `00-Index.md` states that **all** exhibits and tables are images and lost. **That is too strong**: the **BB&T Report of Condition extracted completely, with every line item and both years' figures**, and its internal subtotals verify exactly. **The correct statement is that *graphical* exhibits (charts, diagrams, the cost curve of [[02 - Organization, Structure and Market Entry|ch. 02]], Exhibit 6-1's flow diagram) are images and lost, while some *tabular* financial statements are set as text and survive.** The index has been left as the conservative warning, and this note records the refinement.
>
> **The Report of Income did not extract** — searches for interest income, interest expense and net income lines returned nothing — **so the income-statement material in this chapter is structural rather than numerical**, and §5's discretion example uses figures of my own, labelled as such.
>
> **What is the book's, verbatim:** the entire BB&T Report of Condition used in §2, and the ALL/PLL worked example in §4 (the $100 mn allowance, $1 mn provision, $101 mn result, and $0.5 mn write-off). **What is mine:** every ratio in §3, every check in §2, and §5's three-provision comparison.
>
> **No error was found in Rose & Hudgins ch. 5.** The non-footing totals in §2 were investigated and attributed to an abridged table — see the note there, and Exercise 1(d) for the reasoning.
>
> **Additions beyond the source.** **R&H ch. 5 explains what each line of the statements means, at length and clearly. The verification and the analysis are added:**
>
> - **§2's audit of the book's own balance sheet is mine.** Checking that net loans and the equity components foot exactly — **and that they do so in both years** — establishes which extracted figures can be trusted, and it is the check that identified the totals discrepancy as structural.
> - **§3's ratio comparison against [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s model bank is mine**, and it does something a textbook rarely does: **tests whether the teaching example was realistic.** It was — 9.77% against 9.00% equity.
> - **§5 is the chapter's substantive addition.** R&H explains the ALL/PLL mechanics correctly and does not quantify the discretion they create. **Computing that a 140% swing in the provision moves net income by 47%, and that BB&T's own allowance ratio rose 54% in one year, turns "management estimates losses" into a measured statement about earnings quality.**
> - **The earnings-smoothing discussion** (under-providing versus cookie-jar reserving) and **the note that IFRS 9 and CECL postdate this edition** are additions.
> - **§6's argument that any balance-sheet measure can be evaded by moving exposure off it** — connecting forward to [[10 - Capital Adequacy and Basel|ch. 10]]'s risk weights and back to 2008 — is my framing.
> - **The closing observation in Exercise 3(d)** — that reading accounts means asking which lines are observed and which estimated, paralleling [[Database Management Systems/contents/07 - Database Design|DBMS ch. 07]]'s question of which rules a schema actually enforces — is a cross-subject addition.
>
> **Deliberately compressed.** **R&H's line-by-line walkthrough of every asset and liability category** (each type of security, each deposit class, each borrowing) is summarised by the statement itself in §2 — the definitions are readable in the source and reproducing them adds nothing. **The comparison with the statements of non-bank financial competitors** (§5-6 in the book) is omitted; the structural point — that the asset side differs while the equation does not — is made in Exercise 1(b). **The detailed regulatory-reporting apparatus** (Call Report schedules, UBPR mechanics) is deferred to [[04 - Measuring and Evaluating Bank Performance|ch. 04]], where peer comparison actually uses it. **The Report of Income's line-by-line structure** is deferred to [[04 - Measuring and Evaluating Bank Performance|ch. 04]] as well, where the ratios give it a purpose — and where its absence from the extraction matters less, since the ratios are computed from a stated schema.

**Previous:** [[02 - Organization, Structure and Market Entry]] · **Next:** [[04 - Measuring and Evaluating Bank Performance]]
