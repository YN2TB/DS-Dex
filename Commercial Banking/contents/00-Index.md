---
subject: Commercial Banking
chapter: 0
tags: [ds, banking, finance, index, moc, roe, duration, basel, credit-risk]
source: "Rose & Hudgins, *Bank Management and Financial Services*, 9th edition, McGraw-Hill/Irwin"
---

# Commercial Banking — Index

Map of Content for the subject. **Every chapter note is listed below with a one-line description and a status.**

> [!note] ✅ Subject complete — `00-Index` + chapters 01–12
> **Every numeric claim in these notes was recomputed before it was written**, and **three errata were found in the source** (below). **The three examinable cores are [[04 - Measuring and Evaluating Bank Performance|ch. 04]] (ratios), [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]] (gap and duration) and [[10 - Capital Adequacy and Basel|ch. 10]] (capital and Basel).**
>
> **If you read only four things before an exam:** ch. 04's ROE decomposition, ch. 05's duration gap, ch. 10's risk-weighted assets — and **the result below.**
>
> > [!warning] The one result this subject keeps producing, in four independent places
> > **The average is always fine and the joint behaviour is everything.**
> >
> > | chapter | setting | mean | tail |
> > |---|---|---|---|
> > | [[02 - Organization, Structure and Market Entry\|02]] | bank mergers | — | $\sigma\sqrt{(1+\rho)/2}$: **29.3%** risk reduction at $\rho=0$, **2.5%** at 0.9 |
> > | [[06 - Hedging with Derivatives\|06]] | securitisation tranches | **5.00% at every $\rho$** | senior-tranche loss **0.0000% → 1.8044%** |
> > | [[11 - Lending - Policy, Credit Risk and Business Loans\|11]] | a business loan book | **2.00% at every $\rho$** | 99th percentile **3.60% → 17.60%** |
> > | [[12 - Consumer, Credit Card and Real Estate Lending\|12]] | a mortgage book | — | every loan is a bet on one house-price index |
> >
> > **Same mathematics each time. Any risk measure built on expected values is blind to correlation — and correlation is what turns many small independent risks into one large one.**
>
> **The second thread, and the one that explains 2023:** [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]] **sizes** the loss → [[07 - The Investment Portfolio|ch. 07]] explains **why the assets are there** (Treasuries are the collateral the rules accept, at a zero risk weight) → [[08 - Liquidity and Reserves Management|ch. 08]] **hides** it (held-to-maturity accounting) then **triggers** it (a run) → [[10 - Capital Adequacy and Basel|ch. 10]] **measures none of it** (Basel weights credit risk only). **Every step is a rule working exactly as designed, and the outcome is a failed bank.**

## Course framing

**A bank is a balance sheet that earns a spread and manages the risk of doing so.** Almost everything in this subject follows from that sentence:

- **It borrows short and lends long**, so a change in interest rates hits its assets and liabilities by different amounts — **[[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s gap and duration analysis exists to measure exactly that.**
- **It is leveraged perhaps ten to one**, so a small loss on assets wipes out a large fraction of equity — **which is why [[10 - Capital Adequacy and Basel|ch. 10]]'s capital requirements are imposed by regulators rather than left to management.**
- **Its assets are promises to pay**, so its principal risk is that they are not kept — **[[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]]'s credit risk.**

> [!note] Why this subject is worth real attention for a data scientist
> **This is a quantitative subject dressed as a descriptive one.** The prose is long and the examinable core is small and arithmetical: **ratio decomposition, gap and duration arithmetic, and capital-adequacy calculation.**
>
> **And it is the applied home of things the vault has already built.** [[Principle of Accounting/contents/00-Index|Accounting]]'s statements are the input; [[Probability Theory/contents/00-Index|probability]] and [[Econometrics/contents/00-Index|regression]] are what credit scoring ([[12 - Consumer, Credit Card and Real Estate Lending|ch. 12]]) actually is; **duration is a first derivative**, which is [[Calculus/contents/00-Index|Calculus]] doing real work.
>
> **Credit scoring is also one of the most heavily regulated applications of machine learning that exists** — a model that cannot be explained cannot legally be used to decline an applicant. That constraint is worth understanding before building one.

## Chapters

| # | Note | Source | Status | What it covers |
|---|---|---|---|---|
| 01 | [[01 - The Financial-Services Industry and Its Regulation]] | R&H 1–2 | ✅ | What banks do and why they exist; the services they sell; **why banking is regulated more heavily than any other industry**, and the main US regulatory apparatus |
| 02 | [[02 - Organization, Structure and Market Entry]] | R&H 3–4 | ✅ | Bank holding companies, branching and consolidation; **economies of scale and why the industry keeps concentrating**; chartering and market entry |
| 03 | [[03 - Bank Financial Statements]] | R&H 5 | ✅ | The balance sheet (**assets = loans; liabilities = deposits**) and income statement; the **allowance for loan losses**; off-balance-sheet items |
| 04 | [[04 - Measuring and Evaluating Bank Performance]] | R&H 6 | ✅ | **ROA, ROE, NIM, the equity multiplier, and the ROE decomposition** — the examinable core; efficiency and risk ratios; UBPR peer comparison |
| 05 | [[05 - Interest-Rate Risk - Gap and Duration]] | R&H 7 | ✅ | **Repricing gap and duration gap**; why borrowing short and lending long is the business model *and* the risk; immunisation |
| 06 | [[06 - Hedging with Derivatives]] | R&H 8–9 | ✅ | Futures, options and **interest-rate swaps** as hedges; securitisation, loan sales and credit derivatives — **and their role in 2008** |
| 07 | [[07 - The Investment Portfolio]] | R&H 10 | ✅ | Why banks hold securities at all; yield measures, the **term structure**, and portfolio strategies (ladder, barbell) |
| 08 | [[08 - Liquidity and Reserves Management]] | R&H 11 | ✅ | **Liquidity is not solvency** — the distinction that defines bank runs; estimating liquidity needs; asset vs liability liquidity strategies |
| 09 | [[09 - Managing Deposits and Nondeposit Funding]] | R&H 12–13 | ✅ | Deposit types and **pricing**; the cost of funds; nondeposit borrowing and **why funding mix is a risk decision** |
| 10 | [[10 - Capital Adequacy and Basel]] | R&H 15 | ✅ | **Why capital is regulated**; Tier 1 and Tier 2; **risk-weighted assets and the Basel ratios**; leverage and the 2008 revisions |
| 11 | [[11 - Lending - Policy, Credit Risk and Business Loans]] | R&H 16–17 | ✅ | Lending policy and the credit process; **the six Cs**; loan pricing (cost-plus, price leadership, **RAROC**); business lending |
| 12 | [[12 - Consumer, Credit Card and Real Estate Lending]] | R&H 18 | ✅ | Consumer and card lending; **credit scoring as an applied classification model** — and the regulation that constrains it; mortgage lending |

## What is not covered, and why

| R&H chapter | Why omitted |
|---|---|
| **14 — Investment Banking, Insurance and Other Fee Income** | A survey of non-interest revenue lines. **The one structurally important point — that fee income diversifies away from the interest spread — is made in [[04 - Measuring and Evaluating Bank Performance\|ch. 04]]** where it affects the ratios. |
| **19 — Acquisitions and Mergers** | Deal process and valuation mechanics. **The consolidation *trend* and its cause are covered in [[02 - Organization, Structure and Market Entry\|ch. 02]]**; the deal mechanics are a corporate-finance topic. |
| **20 — International Banking** | Cross-border regulation, currency risk and correspondent banking. **A large topic that needs its own course**, and largely US/global-institution specific. |

> [!warning] Scope decision — needs confirming against the real syllabus
> **Rose & Hudgins has 20 chapters in 7 parts. This vault covers 12**, mapping to R&H 1–13 and 15–18.
>
> **The bias is toward the quantitative core** — statements, ratios, gap/duration, capital, credit — **and away from institutional survey material.** That reflects what is examinable and what connects to the rest of a data-science degree.
>
> **This is my editorial judgement, not the lecturer's. Please check it against the syllabus** — particularly whether international banking (R&H 20) is required, since it is the largest single omission.

## Conventions for this subject

> [!note] Every number in these notes is recomputed
> **This is a quantitative subject, so the vault's verify-every-number rule applies directly**: no ratio, spread, duration or capital figure is quoted without recomputing it in Python (`numpy`, `sympy`, `pandas`).
>
> **And because the book's own exhibits are lost (below), the worked examples here are built from a schema I construct and state explicitly** — a small bank balance sheet and income statement, from which every ratio in [[04 - Measuring and Evaluating Bank Performance|ch. 04]] is derived. **The numbers are mine and are labelled as such**; the *formulas* and their interpretation are the book's.
>
> **This mirrors what [[Database Management Systems/contents/00-Index|DBMS]] had to do** — the source's sample databases were unavailable, so every schema and dataset was written for the notes and every query executed.

- **Formulas are given in LaTeX and then applied to real figures**, because a formula nobody has substituted into is a formula nobody has understood.
- **Where the book is descriptive and the mechanism is quantitative, the quantitative version is added** and labelled in the gaps callout — the subject file anticipated this.
- **Cross-subject links are used heavily**, especially to [[Principle of Accounting/contents/00-Index|Accounting]] (the statements), [[Calculus/contents/00-Index|Calculus]] (duration as a derivative), and [[Probability Theory/contents/00-Index|Probability]] / [[Econometrics/contents/00-Index|Econometrics]] (credit scoring).

## The Monetary and Financial Theories boundary

**[[Monetary and Financial Theories/contents/00-Index|Monetary and Financial Theories]] (Mishkin) is not yet written**, and the two subjects overlap substantially.

> [!note] Boundary decision — recorded here and to be recorded there
> **This subject owns the *bank's own balance sheet*; Mishkin owns the *monetary system*.**
>
> | topic | owner |
> |---|---|
> | how a bank earns and manages a spread | **this subject** |
> | gap, duration, capital adequacy, credit risk | **this subject** |
> | why interest rates are what they are | **Mishkin** |
> | the term structure, as theory | **Mishkin** |
> | central-bank operations and monetary policy | **Mishkin** |
> | money supply, the multiplier, transmission | **Mishkin** |
>
> **[[07 - The Investment Portfolio|Ch. 07]] uses the term structure without deriving it**, and links forward. **Since this subject is written first, it states the boundary; the Mishkin index must record the same split.**

## Errata

| Chapter | Location | Book says | Should be | Verified by |
|---|---|---|---|---|
| **R&H 10** *([[07 - The Investment Portfolio\|ch. 07]])* | Book p. 332, eq. (10-1) — YTM on a \$1,000 par, 8% coupon, 5-year note priced at \$900 | **YTM = 10.74%** | **YTM = 10.68%** *(10.6842%)* | **Substitution into the book's own equation.** 10.6842% prices the note at exactly **\$900.000000**; the book's 10.74% prices it at **\$898.07**. Four alternative conventions tested and rejected: semiannual bond-equivalent (10.6299%), semiannual effective annual (10.9123%), and two shortcut approximations (10.5263%, 11.1111%). **Extraction ruled out** — the prose states "8 percent coupon (or 1,000 × 0.08 = \$80)", "five years" and "price is \$900" independently of the (garbled) displayed equation. |
| **R&H 15** *([[10 - Capital Adequacy and Basel\|ch. 10]])* | Book p. 495 — off-balance-sheet items in the Basel I example | Standby letters of credit **\$10,000**, OBS total **\$30,000** | **\$50,000** and **\$70,000** — *or* the conversion table's face value is wrong | **Internal contradiction**: the credit-conversion table on the same page reads "\$50,000 × 0.20 = \$10,000". **The downstream arithmetic uses the \$50,000 face** — the risk-weight table adds "deposits 5,000 + SLC credit-equivalent 10,000 = 15,000", and the stated RWA total of **80,500** requires it. At a \$10,000 face the credit equivalent is \$2,000 and RWA would be 78,900. |
| **R&H 15** *([[10 - Capital Adequacy and Basel\|ch. 10]])* | Book pp. 496–497 — Tier 1 risk-based capital ratio | **5.52%** | **4.97%** *(4.9689%)* | **Direct computation:** $4{,}000/80{,}500=4.97\%$. **The internal check identifies which figure is wrong:** the book's *total* ratio of **7.45% is correct**, and $7.45/4.97=1.5000$ exactly, matching $6{,}000/4{,}000$ — so 7.45% and 80,500 are mutually consistent and 5.52% is consistent with neither. *(5.52% would require RWA ≈ 72,500, making the total ratio 8.28% and the bank **pass**, contradicting the book's own conclusion.)* **The display is also mislabelled** "Total regulatory capital ÷ Total risk-weighted assets" for a Tier 1 calculation. **Extraction ruled out: "5.52 percent" appears twice, and the correct 7.45% appears in the same sentence.** **Neither error changes the conclusion.** |

> [!note] Two near-misses that were *not* errors
> **[[03 - Bank Financial Statements|Ch. 03]]:** BB&T's liabilities + equity fell short of total assets by 49,742 (2009) and 44,227 (2008). **Because the gap repeats consistently across two independent years it is an omitted line item (likely minority interest), not a typo** — no erratum filed.
>
> **[[06 - Hedging with Derivatives|Ch. 06]]:** two correct figures initially flagged as mismatches because `(0.12−0.11)×100e6` is not exactly `1e6` in binary floating point. **The book was right and the test was wrong.**
>
> **The rule both produced: before recording a source error, rule out your own extraction, your own arithmetic, an abridged table, and an alternative convention.** Filing a false erratum against a correct source is the worse failure.
>
> **[[09 - Managing Deposits and Nondeposit Funding|Ch. 09]] found a third category, recorded in the chapter rather than here:** R&H's Table 12-2 is arithmetically perfect, but the sentence drawn from it — *"The 8.5 percent deposit rate is clearly the best choice"* — is not supported, since **profit is identical at 8.0% and 8.5%**. **This table is for numbers; a wrong inference from correct numbers belongs in the chapter.** *(Same category as [[02 - Organization, Structure and Market Entry|ch. 02]]'s finding that R&H's own cost-curve evidence undercuts its consolidation narrative.)*

## Source and its extraction

**Rose & Hudgins, *Bank Management and Financial Services*, 9th edition.** **760 PDF pages, 20 chapters in 7 parts.** **No lecture slides.**

**Book page $n$ = PDF page $n+18$.** *(Verified: "Chapter Three … 83" appears on PDF page 101.)*

> [!warning] Extraction quirks, tested
> **Body prose extracts cleanly** — full sentences, correct words, no glyph substitution.
>
> **⚠️ Every page carries a watermark that must be stripped**: a `Username: …` / `Book: Bank Management & Financial Services, 9th Edition. No part of any book may be reproduced…` header, plus an occasional `1216484 2015/09/03 110.52.100.70` line. **These interleave with the body text** and will corrupt any naive extraction.
>
> **⚠️ Hyphenation is broken oddly**: the source renders some hyphens as commas — *"Financial,Services"*, *"Asset,Liability"*, *"disas,ter"*. **Read `,` as `-` inside a hyphenated word.** *(Verified across the contents pages and body text.)*
>
> **⚠️ The PDF has no usable outline** — its bookmarks are scan-sheet numbers (`01`, `02`, `1`, `2`, …) at ten-page intervals, not chapter names. **The chapter list above was recovered from the Brief Contents (PDF pages 6–7)** and cross-checked against running headers.
>
> **⚠️ The file is 554 MB and slow to scan**, so page-by-page searches over the whole book time out. **Extract targeted page ranges, not the whole file.**
>
> **⚠️ GRAPHICAL exhibits are images and are lost; some TABULAR statements survive.** *(Verified both ways: on the page containing Exhibit 6-1, only the caption survives and the diagram is absent — as with Exhibit 3-10's cost curve. **But the BB&T Report of Condition in ch. 5 extracted completely**, with every line item, both years' figures, and internal subtotals that verify exactly.)*
>
> **So: charts, diagrams and flow figures are lost; financial-statement tables set as text may survive.** Test before assuming either way — and verify any extracted table's internal subtotals before trusting it.
>
> **This is severe for a subject built on reading financial statements**, and it is why the worked examples in these notes are constructed rather than copied. **Nothing is reconstructed from a partial table**: where the book's figures cannot be recovered, a stated schema of my own is used instead and labelled.

**Previous:** *(start of subject)* · **Next:** [[01 - The Financial-Services Industry and Its Regulation]]
