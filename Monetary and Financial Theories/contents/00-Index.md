---
subject: Monetary and Financial Theories
chapter: 0
tags: [ds, economics, money, banking, monetary-policy, index, moc, mishkin]
source: "Frederic S. Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition"
---

# Monetary and Financial Theories — Index

Map of Content for the subject. **Every chapter note is listed below with a one-line description and a status.**

> [!warning] ⚠️ Extraction: Mishkin does **not** share Mankiw's operator cipher — but displayed equations have their own fault
> **Good news first: inline arithmetic extracts correctly.** `$1 million/(1 + 0.10) = $909,090` comes through with real `+`, `=` and `/`. **This subject does *not* need [[Macroeconomics & Microeconomics/contents/00-Index|Macro/Micro]]'s never-transcribe rule in its strong form.**
>
> **⚠️ But *displayed* equations lose their parentheses to digits:**
>
> | extracts as | actually means |
> |---|---|
> | `11 + i2` | $(1+i)$ |
> | `11 + i22` | $(1+i)^2$ |
> | `11 + i2n` | $(1+i)^n$ |
> | `11 + 0.0723` | $(1+0.07)^3$ |
>
> **So `(` → `1` and `)` → `2`, with any exponent appended immediately after the closing digit.** The yield-to-maturity formula extracts as
>
> ```
> LV = FP/11 + i2 + FP/11 + i22 + FP/11 + i23 + ... + FP/11 + i2n
> ```
>
> which is $LV=\sum_{t=1}^{n} FP/(1+i)^t$.
>
> **⚠️ And in *inline* maths the parentheses survive but superscripts flatten**: `$1 million/(1 + 0.10)2` means $\div(1.10)^2$, not $\times 2$.
>
> **Verified against four of Mishkin's own figures during setup** — the \$909,090 and \$826,446 present values, the \$85.81 payment implying a 7% yield, and the \$9,439.29 mortgage payment. **All four reproduce exactly under this decoding.** *(So the rule here is milder than Macro/Micro's: read prose arithmetic directly, but **reconstruct every displayed formula and check it against a worked number.**)*

## Course framing

**This subject is about the *monetary system*: why interest rates are what they are, how the financial system channels funds, and what a central bank can and cannot do.**

> [!note] Why this is the third leg of a tripod
> **Two subjects in this vault already cover neighbouring ground, and the boundary between all three is recorded below and in both of their indexes.**
>
> - **[[Commercial Banking/contents/00-Index|Commercial Banking]]** owns **the bank's own balance sheet** — the spread, gap and duration, capital adequacy, credit risk.
> - **[[Macroeconomics & Microeconomics/contents/00-Index|Macro/Micro]]** owns **the macro model** — AD–AS, the Phillips curve, the quantity theory, the multiplier as a macro identity.
> - **This subject owns the monetary system** — rate determination, the term structure, central-bank operations and the transmission mechanism, financial-market structure and regulation.
>
> **Two forward references are waiting here.** [[Commercial Banking/contents/07 - The Investment Portfolio|CB ch. 07]] **uses the term structure without deriving it** and links forward; [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation|Macro/Micro ch. 12]] **treats the money multiplier as a macro identity and explicitly defers central-bank operations.** **[[04 - The Risk and Term Structure of Interest Rates|Ch. 04]] and [[08 - Central Banks and the Money Supply Process|ch. 08]] discharge them.**

> [!note] Why it matters for a data scientist
> **Interest rates, exchange rates and asset prices are the most heavily modelled series in existence**, and this subject supplies the structural reasoning behind them — what [[Time-series Analysis/contents/00-Index|time-series analysis]] forecasts and [[Econometrics/contents/00-Index|econometrics]] estimates.
>
> **And the subject's central analytical tool is asymmetric information** — adverse selection and moral hazard — **which is the same machinery behind credit scoring, insurance pricing, and every market where one side knows more than the other.** [[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|Commercial Banking ch. 11]] already computed one instance of it.

## Chapters

| # | Note | Source | Status | What it covers |
|---|---|---|---|---|
| 01 | [[01 - The Financial System and What Money Is]] | M 2–3 | ✅ | Why financial markets exist; direct vs indirect finance; **why financial intermediaries dominate**; debt/equity, primary/secondary, money/capital markets; what money is and how it is measured |
| 02 | [[02 - The Meaning of Interest Rates]] | M 4 | ✅ | Present value; **yield to maturity** for the four credit-market instruments; **why price and yield move inversely**; the distinction between **return and interest rate**; real vs nominal |
| 03 | [[03 - The Behavior of Interest Rates]] | M 5 | ✅ | The **bond-market (loanable funds) and liquidity-preference** frameworks; what shifts each curve; **the Fisher effect**; why rates fall in recessions |
| 04 | [[04 - The Risk and Term Structure of Interest Rates]] | M 6 | ✅ | **Default risk, liquidity and tax treatment**; the yield curve and **three theories of the term structure**; **why an inverted curve predicts recessions** ← *discharges [[Commercial Banking/contents/07 - The Investment Portfolio\|CB ch. 07]]'s forward reference* |
| 05 | [[05 - The Stock Market, Rational Expectations and Efficient Markets]] | M 7 | ✅ | Stock valuation and the **Gordon growth model**; rational expectations; the **efficient market hypothesis**, its evidence and its critics; behavioural finance |
| 06 | [[06 - Asymmetric Information and Financial Structure]] | M 8 (+ 10) | ✅ | **Eight puzzles of financial structure**; **adverse selection (lemons) and moral hazard**; why debt dominates equity; **the principal–agent problem**; the rationale for financial regulation |
| 07 | [[07 - Financial Crises]] | M 12–13 | ✅ | The **anatomy of a crisis** — asset-price booms, deterioration of balance sheets, banking crises, debt deflation; 2007–09; **why emerging-market crises differ** |
| 08 | [[08 - Central Banks and the Money Supply Process]] | M 14–15 | ✅ | Central-bank structure and **independence**; the monetary base; **the money multiplier derived properly, with currency and excess reserves** ← *discharges [[Macroeconomics & Microeconomics/contents/12 - The Monetary System and Inflation\|Macro/Micro ch. 12]]'s forward reference* |
| 09 | [[09 - Tools and Conduct of Monetary Policy]] | M 16–17 | ✅ | **The market for reserves** and how the policy rate is set; open-market operations, discount lending, reserve requirements, **interest on reserves**; goals, **inflation targeting**, the **Taylor rule**; the zero lower bound |
| 10 | [[10 - Foreign Exchange and the International Financial System]] | M 18–19 | ✅ | Exchange-rate determination in the **short and long run**; **interest parity**; foreign-exchange intervention and the balance of payments; fixed vs floating; capital controls |
| 11 | [[11 - Money Demand and the Monetary Policy Framework]] | M 20–22 | ✅ | The **quantity theory and velocity**; Keynesian money-demand theories; **the IS curve and the monetary policy (MP) curve**; deriving aggregate demand |
| 12 | [[12 - Monetary Policy Theory, Expectations and Transmission]] | M 24–26 | ✅ | Responding to shocks; **the time-inconsistency problem** and why credibility matters; **the transmission mechanisms** — interest-rate, exchange-rate, asset-price and credit channels |

## Scope: 12 chapters from 26

> [!warning] Scope decision — needs confirming against the real syllabus
> **Mishkin has 26 chapters in 6 parts. This vault covers 12**, and the omissions are driven mainly by **ownership decisions already recorded in two other subjects' indexes** rather than by judgements about importance.
>
> **The bias is toward the analytical core** — rate determination, the term structure, asymmetric information, the money supply process, and monetary transmission — **and away from institutional survey material and anything another subject already owns.**
>
> **This is my editorial judgement, not the lecturer's. Please check it.**

### What is not covered, and why

| Chapter | Why omitted |
|---|---|
| **1 — Why Study Money, Banking and Financial Markets?** | A motivational overview. **Its appendix (aggregate output, price level, growth rates) is [[Macroeconomics & Microeconomics/contents/08 - Measuring the Macroeconomy - GDP and the Cost of Living\|Macro/Micro ch. 08]]'s material** and is computed there. |
| **9 — Banking and the Management of Financial Institutions** | **⚠️ [[Commercial Banking/contents/00-Index\|Commercial Banking]] owns this entirely** — its chs. 03–08 cover bank statements, ratios, gap and duration, liquidity and funding **with every figure computed**. Duplicating it would contradict the recorded boundary. |
| **10 — Economic Analysis of Financial Regulation** | **Split.** The distinctive analytical content — **deposit insurance as moral hazard, and the too-big-to-fail problem** — is folded into [[06 - Asymmetric Information and Financial Structure\|ch. 06]]. The prudential-supervision machinery is [[Commercial Banking/contents/10 - Capital Adequacy and Basel\|CB ch. 10]]'s. |
| **11 — Banking Industry: Structure and Competition** | **[[Commercial Banking/contents/02 - Organization, Structure and Market Entry\|CB ch. 02]] owns it**, including the finding that R&H's own cost-curve evidence undercuts the standard consolidation argument. |
| **23 — Aggregate Demand and Supply Analysis** | **[[Macroeconomics & Microeconomics/contents/14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve\|Macro/Micro ch. 14]] owns AD–AS**, per the recorded split. **[[11 - Money Demand and the Monetary Policy Framework\|Ch. 11]] here derives the AD curve from the IS and MP curves — which Mankiw does not do — and then links across.** |
| **25 (part) — the new-classical / new-Keynesian debate** | A survey of competing schools. **The time-inconsistency result, which is the durable content, is kept** in [[12 - Monetary Policy Theory, Expectations and Transmission\|ch. 12]]. |

> [!note] The one omission worth arguing about
> **Mishkin ch. 9 is a genuinely good treatment of bank management, and a reader who has *not* done Commercial Banking would lose a great deal by skipping it.** It is omitted only because **that subject is complete in this vault and covers the same ground in more depth with worked numbers.** *(If the syllabus for this course expects bank management, read [[Commercial Banking/contents/00-Index|Commercial Banking]] chs. 03–08 rather than adding a chapter here.)*

## Boundaries — recorded in all three indexes

> [!warning] The three-way split, now stated in every subject that touches it
> | topic | owner |
> |---|---|
> | a bank's balance sheet, spread, gap/duration, capital, credit risk | **[[Commercial Banking/contents/00-Index\|Commercial Banking]]** |
> | bank ratios, liquidity management, deposit pricing, lending policy | **[[Commercial Banking/contents/00-Index\|Commercial Banking]]** |
> | AD–AS, the Phillips curve, the quantity theory as a macro identity | **[[Macroeconomics & Microeconomics/contents/00-Index\|Macro/Micro]]** |
> | growth, unemployment, the fiscal multiplier | **[[Macroeconomics & Microeconomics/contents/00-Index\|Macro/Micro]]** |
> | **why interest rates are what they are** | **this subject** |
> | **the term structure, as theory** | **this subject** |
> | **central-bank operations and the transmission mechanism** | **this subject** |
> | **financial-market structure, asymmetric information, crises** | **this subject** |
>
> **Both other indexes already state this split.** This one matches it — **if it ever diverges, the vault contradicts itself.**

**Where the subjects meet, this one cross-links rather than re-deriving.** Notably: [[Macroeconomics & Microeconomics/contents/10 - Saving, Investment and the Financial System|Macro/Micro ch. 10]] already computed present value, diversification and crowding out; [[Commercial Banking/contents/06 - Hedging with Derivatives|CB ch. 06]] already computed the correlation result that governs securitisation; and [[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|CB ch. 11]] already computed the credit-rationing curve that [[06 - Asymmetric Information and Financial Structure|ch. 06]] here explains theoretically.

## Conventions for this subject

> [!note] Every number recomputed; every displayed formula reconstructed
> **The vault's verify-every-number rule applies.** **And because displayed equations lose their parentheses (above), no formula is transcribed** — each is reconstructed from the prose and checked against one of Mishkin's own worked figures.
>
> **This subject is unusually well supplied with worked numerical examples**, so most chapters can be verified against the source directly rather than against a schema of my own — which is a better position than [[Commercial Banking/contents/00-Index|Commercial Banking]] or [[Macroeconomics & Microeconomics/contents/00-Index|Macro/Micro]] were in.

- **⚠️ Every figure is an image and is lost**, which matters a great deal here: **this subject teaches through shifting curves** — bond supply and demand, liquidity preference, yield curves, the market for reserves, IS–MP. **Comparative statics are described in words and equations and each loss is flagged.**
- **Cross-subject links are used heavily**, especially to the two subjects above and to [[Econometrics/contents/00-Index|Econometrics]] where a claim is empirical.

## Errata

**Every entry is verified by recomputation, and the vault's rule 4 is applied before filing: rule out your own extraction, your own arithmetic, an abridged table, *and* alternative conventions. Filing a false erratum against a correct source is the worse failure.**

| # | Location | Book says | Correct | Basis |
|---|---|---|---|---|
| 1 | **ch. 4, footnote 6, p. 129** | `($1,555 − $1,000)/1,000 = 0.155 = 15.5%` | **\$1,155**, not \$1,555 | **\$1,555 − \$1,000 = \$555 = 55.5%, not 15.5%.** The line *immediately above* correctly computes \$1,100 × 1.05 = **\$1,155**, which does give 15.5%. **A typo; the stated answer is right.** *(Extraction ruled out — both figures appear one line apart. No convention produces \$1,555.)* → [[02 - The Meaning of Interest Rates]] |

### Investigated and deliberately NOT filed

| Location | Apparent problem | Why not filed |
|---|---|---|
| **ch. 18, Table 1, p. 480** *(Big Mac index)* | Japan's index prints **−36.7%** and Venezuela's **−86.5%**, where the table's own columns give **−36.96%** and **−86.61%**. | *(Diagnosed: the indices require actual exchange rates of **0.008434** and **0.005042**, both of which round to the printed four-decimal 0.0084 and 0.0050.)* **So column 3 is rounded and the indices are computed from unrounded rates — an internal rounding difference, not an error.** **All six implied PPP rates, the other four indices, and both prose cross-checks (\$6.44 and \$0.66) reproduce exactly.** → [[10 - Foreign Exchange and the International Financial System]] |
| **ch. 15, p. 406** *(money multiplier)* | The fourth worked case prints $0.10+1.56+1.50=\mathbf{3.20}$, giving $m=0.78$. | **The sum is 3.16, giving 0.79.** *(Diagnosed: **rounding $e$ to 1.60 instead of 1.56 reproduces both 3.20 and 0.78 exactly.**)* **An internal ROUNDING INCONSISTENCY, not an arithmetic error** — the other three cases reproduce exactly — **and the conclusion (the multiplier *rises*) is unaffected either way.** Rule 4: rule out alternative conventions. → [[08 - Central Banks and the Money Supply Process]] |
| **ch. 12, p. 327** *(debt deflation)* | Real liabilities computed as $\$90\text{m}\times1.1=\$99\text{m}$, giving net worth of **\$1m**. | **The exact figure is $90/0.9=\$100\text{m}$, i.e. net worth of \$0** — he used $D(1+\pi)$ for $D/(1-\pi)$. **The error is $D\pi^2/(1-\pi)=\$1\text{m}$: 1.1% of the debt but 100% of the remaining equity**, so it is the difference between "survives, barely" and "insolvent". **Not filed — the approximation is standard and it *understates* his own conclusion.** ⚠️ **Fourth dropped cross term in this subject and the most consequential, because the error straddles zero.** → [[07 - Financial Crises]] |
| **ch. 12, p. 326** *(coffee price)* | "the price of coffee decreased from \$.22 per lb to \$.10 per lb — **a 46% decline**". | *(Computed: \$0.22 → \$0.10 is **−54.5%**. A −46% fall needs an end price ≈\$0.118 or a start ≈\$0.185.)* **Not filed: the wheat figure in the SAME SENTENCE checks perfectly** (\$1.37 → \$0.87 = −36.5%, printed as 37%), **which makes a mis-extracted digit in the `$.10`/`$.22` format likelier than an author's arithmetic error.** Rule 4 — rule out your own extraction first. **Do not quote without checking the page image.** → [[07 - Financial Crises]] |
| **ch. 6, p. 178** | Mishkin justifies dropping the cross term with "$(i_{2t})^2$ is extremely small — if $i_{2t}=10\%$, then $(i_{2t})^2=0.01$", pointing at the **level** of rates. | *(Computed: the error is exactly **0.0000** at 10%, 20% **and** 40% when the two rates are equal, and **0.1137 / 0.4555** at an unchanged 10% mean as dispersion grows.)* **So the level does not control the error — the DISPERSION does.** **The approximation is standard, the conclusion correct, and the error hundredths of a point at ordinary dispersions.** **It is the justification that is imprecise, not the result, and an erratum is a claim the source is *wrong*.** → [[04 - The Risk and Term Structure of Interest Rates]] |
| **ch. 5, Figure 1 axis label, p. 140** | Label extracts as `(i 5 33.0%)`; the prose says **33.3%** and the truth is **33.3333%**. | **Figure labels are part of a graphic and their digits are unreliable under extraction** — note the `5` standing for `=` in the same label. **The prose is correct.** Rule 4: rule out your own extraction first. **Recorded as an extraction hazard: never take a number from a figure label.** |
| **ch. 4, footnote 6, p. 129** | The two annualisations disagree in method: **32% over two years → 14.9%** *(geometric)* but **15.5% over two years → 7.2%** *(continuous)*. Geometric would give **7.47%**. | **Neither number is wrong under its own convention** *(verified: geometric 14.89%/7.47%, continuous 13.88%/7.21%)*. **Rule 4 requires ruling out alternative conventions first.** Recorded because the coexistence is itself the lesson: **"at an annual rate" is undefined until you name the annualisation.** |

| Chapter | Location | Book says | Should be | Verified by |
|---|---|---|---|---|

## Source and its extraction

**Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition. 746 PDF pages, 26 chapters in 6 parts. No lecture slides.**

> [!warning] Extraction quirks, tested
> **Body prose extracts cleanly** — full sentences, correct words.
>
> **⚠️ The PDF outline is excellent** — 25 top-level entries resolving down to sub-section level, so chapters and sections locate precisely. **Locate by outline, then extract the page range.**
>
> **⚠️ Displayed equations lose parentheses to digits** (`(`→`1`, `)`→`2`, exponents appended) — see the callout at the top. **Inline arithmetic is fine.** *(Verified against four worked figures.)*
>
> **⚠️ Expect every figure and every statistical table to be an image and lost.** No data files exist in the vault, so nothing can be re-derived from raw sources.
>
> **Page mapping**: the PDF is offset from the printed book — *"CHAPTER 4 The Meaning of Interest Rates 117"* appears on **PDF page 118**, so **book page $n$ = PDF page $n+1$** in the body. *(The outline's page numbers are PDF pages and are what should be used.)*

**Previous:** *(start of subject)* · **Next:** [[01 - The Financial System and What Money Is]]
