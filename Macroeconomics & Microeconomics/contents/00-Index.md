---
subject: Macroeconomics & Microeconomics
chapter: 0
tags: [ds, economics, microeconomics, macroeconomics, index, moc, mankiw]
source: "N. Gregory Mankiw, *Principles of Microeconomics* 6e and *Principles of Macroeconomics* (2017); Parkin & Bade, *Macroeconomics* ch. 25"
---

# Macroeconomics & Microeconomics — Index

Map of Content for the subject. **Every chapter note is listed below with a one-line description and a status.**

> [!note] ✅ Subject complete — `00-Index` + chapters 01–14
> **Two courses in one folder, 36 distinct chapters reduced to 14** *(7 micro, 7 macro, split between ch. 07 and ch. 08)*. **Every numeric claim was recomputed before it was written, and no erratum was found in any source.**
>
> > [!warning] The subject's organising result, found in ch. 04 and appearing four times
> > **Efficiency is fixed by *fundamentals*; distribution by *institutional detail*; and the two are independent.**
> >
> > | chapter | fixes the **allocation** | fixes the **split** |
> > |---|---|---|
> > | [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage\|01]] | comparative advantage | the **price** *(total gain constant at 10 oz)* |
> > | [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade\|03]] | the tax **wedge** *(the statute is irrelevant)* | **elasticities**, $\eta_s/(\eta_s+\eta_d)$ |
> > | [[04 - Externalities, Public Goods and Common Resources\|04]] | benefit vs cost | the **property right** |
> > | [[06 - Monopoly, Oligopoly and Monopolistic Competition\|06]] | $P=MC$ under perfect discrimination | the **pricing scheme** |
> >
> > ⇒ **many policy arguments conducted in the language of efficiency are really about distribution.** *Mankiw never connects them.*
>
> > [!warning] The macro half's signature — four times, "theory complete, answer empirical"
> > | chapter | question | the parameter that decides it |
> > |---|---|---|
> > | [[07 - Factor Markets and the Theory of Consumer Choice\|07]] | higher wages → hours worked? | **the sign itself** is ambiguous |
> > | [[10 - Saving, Investment and the Financial System\|10]] | crowding out of a deficit? | **100% or 33%** — the saving slope |
> > | [[11 - Unemployment\|11]] | minimum-wage job losses? | **1% or 30%** — the demand elasticity |
> > | [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve\|14]] | the fiscal multiplier? | **0.80 or 10.00** — multiplier vs crowding out |
> >
> > **In every case two identified forces oppose and the theory refuses to sign the net** — which tells you *which quantity to measure*. **Quoting a point estimate as though theory delivered it is the error, and it is made in both political directions.**
>
> **The best single cross-chapter finding:** [[06 - Monopoly, Oligopoly and Monopolistic Competition|ch. 06]]'s **Cournot oligopoly with $N$ firms *is* [[04 - Externalities, Public Goods and Common Resources|ch. 04]]'s tragedy of the commons** — identical formula $q=(a-c)/(N+1)$ and **identical percentages at every matching $N$** (100.0%, 88.9%, 33.1%, 7.7%, 0.4%). **The two chapters tell opposite stories about one piece of mathematics**, because the externality lands on different people. ⇒ *an equilibrium is not good or bad by itself; ask whose surplus the externality hits.*

> [!warning] ⚠️ READ THIS BEFORE OPENING ANY SOURCE PDF — the maths is enciphered
> **Mankiw's PDFs render every arithmetic operator as a digit.** An equation extracts as something that looks like a list of numbers and is silently wrong.
>
> | extracts as | actually means |
> |---|---|
> | `5` | **=** |
> | `1` | **+** |
> | `2` | **−** |
> | `3` | **×** |
>
> **So `Y 5 C 1 I 1 G 1 NX` is $Y = C + I + G + NX$.**
>
> **⚠️ And it is worse than a fixed substitution: the same digit means different things in the same line.** The midpoint elasticity formula extracts as
>
> ```
> Price elasticity of demand 5 (Q2 2 Q1) / [(Q2 1 Q1) / 2]
> ```
>
> which is $\dfrac{Q_2-Q_1}{(Q_2+Q_1)/2}$ — **six digits with four different meanings**: subscript, minus, subscript, plus, subscript, and a literal 2. Likewise `(6 2 4) / 5 3 100 5 40` is $(6-4)/5\times100=40$, where **`5` is a literal number and an equals sign in the same expression.**
>
> **There is no mechanical decoder. You must know the economics to read the maths**, which is why every formula in these notes was reconstructed from the surrounding prose and then verified numerically against the book's own worked figures.

## Course framing

**Economics is the study of how society manages scarce resources**, and Mankiw organises it around a single question asked at two scales:

- **Microeconomics** — how *individual* households and firms make decisions and interact in markets. **The recurring tool is surplus**: measure what buyers and sellers gain, then ask what a policy does to it.
- **Macroeconomics** — how the economy behaves *in aggregate*: output, employment, inflation, growth. **The recurring tool is a market diagram applied to unfamiliar markets** — loanable funds, foreign exchange, money.

> [!note] Why this subject matters for a data scientist
> **This is the subject that supplies the *questions* the rest of the degree answers.** [[Econometrics/contents/00-Index|Econometrics]] estimates these relationships; [[Time-series Analysis/contents/00-Index|time-series analysis]] forecasts them; **and almost every applied dataset you will meet is generated by the behaviour modelled here.**
>
> **⚠️ Mankiw is deliberately calculus-free**, which hides the fact that most of it *is* optimisation. Marginal analysis is a first derivative ([[Calculus/contents/00-Index|Calculus]]); consumer choice is constrained optimisation with a Lagrange multiplier ([[Optimization/contents/00-Index|Optimization]] ch. 11); cost minimisation is the same problem in production space. **These connections are added throughout and labelled as additions** — they are genuine enrichment for this reader, not part of the source.
>
> **The most transferable idea in the subject is *the counterfactual*.** "What would have happened otherwise" is the whole content of deadweight loss, opportunity cost, and every policy evaluation — and it is the same idea causal inference is built on.

## Chapters

**Micro first (01–07), then macro (08–14)**, following the standard sequence. **The split point is between ch. 07 and ch. 08.**

| # | Note | Source | Status | What it covers |
|---|---|---|---|---|
| 01 | [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage]] | M 1–3 | ✅ | The ten principles; models, positive vs normative; **opportunity cost and comparative advantage** — why trade creates value |
| 02 | [[02 - Supply, Demand and Elasticity]] | M 4–5 | ✅ | The market forces; shifts vs movements; **elasticity and why it decides who bears a burden** |
| 03 | [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade]] | M 6–9 | ✅ | Consumer and producer surplus; **deadweight loss**; price ceilings and floors; tax incidence; the gains from trade and the cost of tariffs |
| 04 | [[04 - Externalities, Public Goods and Common Resources]] | M 10–11 | ✅ | When markets fail; **the Coase theorem**, Pigouvian taxes and tradable permits; excludability, rivalry, and the tragedy of the commons |
| 05 | [[05 - Production Costs and Competitive Markets]] | M 13–14 | ✅ | Production functions and **diminishing marginal product**; fixed/variable/marginal cost; **why a competitive firm produces where $P = MC$**; entry, exit and the long-run supply curve |
| 06 | [[06 - Monopoly, Oligopoly and Monopolistic Competition]] | M 15–17 | ✅ | Market power and its **deadweight loss**; price discrimination; **the prisoners' dilemma and why cartels fail**; product differentiation and advertising |
| 07 | [[07 - Factor Markets and the Theory of Consumer Choice]] | M 18, 21 | ✅ | Labour demand as **marginal revenue product**; the budget constraint and indifference curves; **income and substitution effects** |
| 08 | [[08 - Measuring the Macroeconomy - GDP and the Cost of Living]] | Mac 10–11 | ✅ | **$Y = C + I + G + NX$**; real vs nominal and the GDP deflator; the CPI, its biases, and correcting for inflation |
| 09 | [[09 - Production and Growth]] | Mac 12 | ✅ | Productivity and its determinants; **capital accumulation, diminishing returns and the catch-up effect**; what policy can and cannot do |
| 10 | [[10 - Saving, Investment and the Financial System]] | Mac 13–14 | ✅ | Financial institutions; **the market for loanable funds**; crowding out; present value, risk and diversification |
| 11 | [[11 - Unemployment]] | Mac 15 | ✅ | Measurement and its problems; **frictional vs structural**; job search, minimum wages, unions and efficiency wages |
| 12 | [[12 - The Monetary System and Inflation]] | Mac 16–17 | ✅ | What money is; **the money multiplier and central-bank tools**; **the quantity theory $M\times V = P\times Y$**; the classical dichotomy, the Fisher effect and the costs of inflation |
| 13 | [[13 - Open-Economy Macroeconomics]] | Mac 18–19 + **P&B 25** | ✅ | Net exports and net capital outflow; real and nominal exchange rates; **purchasing-power parity**; the open-economy model; **the balance of payments in detail** |
| 14 | [[14 - Short-Run Fluctuations - AD-AS, Policy and the Phillips Curve]] | Mac 20–22 | ✅ | Why the short run differs; **aggregate demand and supply**; monetary and fiscal policy, multipliers; **the Phillips curve and the sacrifice ratio** |

## Scope: the largest editorial decision in this vault

> [!warning] Two courses, four books, 36 distinct chapters — reduced to 14. **Needs confirming against the real syllabus.**
> **This folder holds two separate courses.** Mankiw's micro and macro volumes together contain **36 distinct chapters**; writing all of them at this vault's depth is not sensible, and picking arbitrarily is worse.
>
> **The adopted scope is the standard one-semester-each sequence**, consolidated into 14 notes: **7 micro + 7 macro, split between ch. 07 and ch. 08.**
>
> **The bias is toward the analytical core** — the surplus toolkit, firm behaviour, market structure, the macro identities and models — **and away from applied-policy survey chapters.**
>
> **This is my editorial judgement, not the lecturer's. Please check it**, particularly whether the omissions below are required.

### What is not covered, and why

| Chapter | Why omitted |
|---|---|
| **Micro 12 — The Design of the Tax System** | US-specific tax institutions. **The analytical content — efficiency vs equity, deadweight loss, incidence — is in [[03 - Welfare Analysis - Surplus, Price Controls, Taxes and Trade\|ch. 03]]**, which is where it can be computed. |
| **Micro 19 — Earnings and Discrimination** | Important, but largely an application of [[07 - Factor Markets and the Theory of Consumer Choice\|ch. 07]]'s marginal-product theory plus institutional discussion. **The measurement problem it raises is properly an [[Econometrics/contents/00-Index\|econometrics]] topic** (omitted-variable bias in wage regressions). |
| **Micro 20 — Income Inequality and Poverty** | Measurement and policy survey. **The distributional question is real but is not analytically developed by Mankiw**, and the measurement side (Gini, Lorenz) is better handled with data. |
| **Micro 22 — Frontiers of Microeconomics** | Asymmetric information, political economy, behavioural economics. **A genuine loss** — see the note below. |
| **Macro 23 — Six Debates Over Macroeconomic Policy** | A capstone that restates earlier material as pro/con positions. **The underlying models are all covered**; the debates are a revision exercise. |

> [!note] The one omission worth arguing about
> **Micro ch. 22 (Frontiers) contains asymmetric information — adverse selection, moral hazard, signalling, screening — and that material has already earned its place elsewhere in this vault.**
>
> **[[Commercial Banking/contents/11 - Lending - Policy, Credit Risk and Business Loans|Commercial Banking ch. 11]] computed a credit-rationing result** in which the expected return on a loan is *humped*: past an optimal rate the lender earns less by charging more, because the rate itself induces default. **That is Stiglitz–Weiss, and it is asymmetric information doing real work.**
>
> **It is omitted here only because Commercial Banking already owns it with a worked computation.** [[04 - Externalities, Public Goods and Common Resources|Ch. 04]] cross-links to it, since market failure is the shared theme. **If the syllabus requires ch. 22, it should be added rather than substituted.**

## Deduplication — done first, as the subject file required

**Three Mankiw PDFs overlap heavily. The mapping was established from all three tables of contents before any chapter was planned:**

| Source | Chapters | Verdict |
|---|---|---|
| **Macro (2017)** | 1–9 | **Identical in content to Micro 1–9** — the shared introductory core |
| | 10–23 | **Macro-only.** The macro spine. |
| **Micro (6e)** | 1–9 | Same shared core, **older edition** |
| | 10–22 | **Micro-only.** The micro spine. |
| **Principles of Economics 8e** | Parts I–XIII | **A superset of both.** Not used as a source. |

> [!note] The rule adopted
> **The overlap is exactly chapters 1–9**, which appear in both spines.
>
> - **For the shared core (chs. 1–9) the Macro 2017 volume is the source**, because it is the newer edition and matches the 8e text.
> - **For micro chs. 10–22, the Micro 6e volume is the source** — the only one that has them.
> - **For macro chs. 10–23, the Macro 2017 volume is the source.**
> - **The combined 8e is used only to resolve a gap or an ambiguity**, never as an independent source. **Where it is used, the note says so.**
>
> **This is why chapters 01–03 of these notes draw on "M 1–9" without ambiguity** — the two books agree there.

**Parkin & Bade ch. 25** is a single chapter on the exchange rate and the balance of payments. **Its presence in a Mankiw-based course is a deliberate signal** that the syllabus wants open-economy macro in more depth than Mankiw gives it — so **[[13 - Open-Economy Macroeconomics|ch. 13]] uses it as a co-equal source**, not a supplement.

## Conventions for this subject

> [!note] Every number is recomputed, and every formula is reconstructed
> **The vault's verify-every-number rule applies with unusual force here, because the source's equations are enciphered.** No formula in these notes is transcribed: **each is reconstructed from the surrounding prose and then checked against the book's own worked arithmetic.** *(The CPI basket, the quantity equation and the midpoint elasticity formula were all decoded and verified this way during setup.)*
>
> **Mankiw's numerical tables are images and are lost**, so worked examples are recomputed from the stated assumptions rather than transcribed — the same approach [[Commercial Banking/contents/00-Index|Commercial Banking]] and [[Database Management Systems/contents/00-Index|DBMS]] used.

- **⚠️ Mankiw teaches through diagrams, and every diagram is lost.** Comparative statics are therefore described **in words and, where possible, in equations** — which is frequently *clearer* than the diagram, and always more checkable. **Each loss is flagged.**
- **Calculus and optimisation connections are added and labelled**, since Mankiw deliberately omits them.
- **Cross-subject links are used heavily** — especially to [[Econometrics/contents/00-Index|Econometrics]], [[Commercial Banking/contents/00-Index|Commercial Banking]] and [[Calculus/contents/00-Index|Calculus]].

## Boundaries with other subjects

> [!note] Monetary and Financial Theories (Mishkin) — decided here, to be recorded there
> **Mankiw owns the macroeconomic model; Mishkin owns the financial plumbing.**
>
> | topic | owner |
> |---|---|
> | AD–AS, the Phillips curve, the multiplier | **this subject** |
> | the quantity theory, the classical dichotomy | **this subject** |
> | what money is, the money multiplier (as a macro identity) | **this subject** |
> | how central banks actually operate; the transmission mechanism in detail | **Mishkin** |
> | the term structure and why rates are what they are | **Mishkin** |
> | financial-market microstructure, regulation | **Mishkin** |
>
> **[[12 - The Monetary System and Inflation|Ch. 12]] introduces central-bank tools at the level a macro course needs and links forward.**

> [!note] Commercial Banking — already written, and it owns the bank's balance sheet
> **[[Commercial Banking/contents/00-Index|Commercial Banking]] is complete.** Its boundary statement assigns the *monetary system* to Mishkin and the *bank's own balance sheet* to itself. **This subject sits above both**: it supplies the macro model in which banks operate.
>
> **Two specific cross-links, both flagged in Commercial Banking's own notes:**
> - **Comparative advantage** ([[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage|ch. 01]]) is the theory behind Commercial Banking ch. 09's interest-rate swap, whose gain comes from a *difference of spreads* and vanishes when the spreads are equal.
> - **Credit rationing** — Commercial Banking ch. 11's humped return curve — **is Stiglitz–Weiss**, and [[04 - Externalities, Public Goods and Common Resources|ch. 04]] links to it as an information failure.

## Errata

*(Empty so far — populated as errors are found and verified by recomputation.)*

| Chapter | Location | Book says | Should be | Verified by |
|---|---|---|---|---|

## Sources and their extraction

| File | Pages | Role |
|---|---|---|
| `1-Mankiw - Principles of Macroeconomics 2017.pdf` | 578 | **Macro spine + the shared core (chs. 1–9)** |
| `Principles of Microeconomics( 6th Edition)_N. Gregory Mankiw.pdf` | 530 | **Micro spine (chs. 10–22)** |
| `mankiw_principles_of_economic 8th (1).pdf` | 866 | Superset — **gap-filling only, and disclosed when used** |
| `1-Michael Parkin, Robin Bade - Macroeconomics _ Chapter25-BoP and ex rate.pdf` | 28 | **Co-equal source for [[13 - Open-Economy Macroeconomics\|ch. 13]]** |

> [!warning] Extraction quirks, tested
> **Body prose extracts cleanly** in all four files — full sentences, correct words, no glyph substitution *in the prose*.
>
> **All three Mankiw PDFs have usable outlines** (24, 29 and 34 top-level entries), with chapter and section titles down to sub-subsection level. **This is unusually good and makes targeted extraction easy** — locate by outline, then extract the page range.
>
> **⚠️ THE OPERATOR CIPHER (above) is the dominant hazard.** `5`→`=`, `1`→`+`, `2`→`−`, `3`→`×`, **context-dependent**, and it affects *every* equation in *both* Mankiw spines. **Verified in the macro book (the GDP identity, the quantity equation, the Fisher equation, the CPI basket) and independently in the micro book (both elasticity formulas).**
>
> **⚠️ Every figure is an image and is lost.** **This is the worst-case subject for that** — Mankiw teaches almost entirely through shifting curves and shaded surplus areas. What survives is the caption and a scatter of axis labels and tick values, which is *worse than nothing* because it looks like data. **Numerical tables are images too** and must be recomputed, not transcribed.
>
> **Minor faults observed:** possessive apostrophes occasionally mangle (`today's` → `todayrs`); short phrases sometimes duplicate (`which relates Y, which relates Y`); running heads interleave with body text.
>
> **Parkin & Bade extracts cleanly and does *not* share the cipher** — its prose and equations both come through readably, which is a further reason to use it directly in [[13 - Open-Economy Macroeconomics|ch. 13]].

**Previous:** *(start of subject)* · **Next:** [[01 - Ten Principles, Thinking Like an Economist, and Comparative Advantage]]
