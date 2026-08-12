---
subject: Commercial Banking
chapter: 12
tags: [ds, banking, consumer-lending, credit-scoring, classification, ecoa, disparate-impact, mortgages]
source: "Rose & Hudgins, *Bank Management and Financial Services* 9e, ch. 18"
---

# Consumer, Credit Card and Real Estate Lending

**This is the chapter where the degree closes on itself.** Credit scoring is **supervised binary classification with asymmetric misclassification costs** — [[Machine Learning/contents/00-Index|Machine Learning]] and [[Econometrics/contents/00-Index|Econometrics]] applied to the [[11 - Lending - Policy, Credit Risk and Business Loans|previous chapter]]'s six Cs — **and it is one of the most heavily regulated applications of statistical modelling that exists.**

**Three results.**

**§3 — R&H's "criterion score" is a classification threshold, and its 40%/10% is a point on an ROC curve.** The book says management "can experiment with other criterion scores" and never does. *(Computed: sweeping the threshold puts the optimum near **322 points** for a net saving of **\$707,070**, against R&H's 280 and \$540,000.)*

**§4 — and the optimum is not a property of the model at all.** R&H charges **\$600** for a bad loan and **\$600** for a rejected good one, but **a rejected good customer costs only the forgone profit.** *(Computed: at \$600 against \$100 the optimal cutoff moves from **322 to 418 points**, rejecting **89.0%** of good applicants instead of 30.2%.)* **The threshold is a business decision wearing a statistical costume, and it is where the harm lives.**

**§5 — omitting a protected variable does not remove its effect.** *(Computed: one facially neutral feature worth 20 points, held by 95% of one group and 70% of another, produces a **1.69%** gap in approval rates among *equally creditworthy* applicants. Real models have dozens.)*

## 📘 Main Knowledge

### 1. Consumer lending is a different business

| | business lending ([[11 - Lending - Policy, Credit Risk and Business Loans\|ch. 11]]) | consumer lending |
|---|---|---|
| decision | individual judgement, six Cs | **statistical model** |
| repayment source | business cash flow | **personal income** |
| size | large, few | small, very many |
| rate sensitivity | high — borrowers shop | **low** — convenience and access dominate |
| cost per decision | high, and worth it | **must be near zero** |

> [!note] The economics force the method
> **A \$2,000 loan cannot support an hour of an officer's time**, so consumer lending is only viable if the decision is automated. **That is why credit scoring exists** — not because it is more accurate than judgement, but because it is cheap enough to be used at all.
>
> **And consumer loans are the least rate-sensitive category R&H identifies**, which is why they carry the highest rates in the bank and why [[04 - Measuring and Evaluating Bank Performance|ch. 04]]'s margin analysis is flattered by a large consumer book.

### 2. The scoring model, verified

*(Verified — R&H's Table 18-4, all eight factors and all 28 point values extracted intact:)*

| factor | best | worst |
|---|---|---|
| occupation | 100 | 20 |
| housing status | 60 | 20 |
| credit rating | 100 | 0 |
| time in current job | 50 | 20 |
| time at current address | 20 | 10 |
| telephone in home | 20 | 0 |
| **dependents** | **40** | **20** |
| deposit accounts held | 40 | 0 |
| **total** | **430** ✓ | **90** ✓ |

**And the score sets the *amount*, not the rate** *(Table 18-5)*: reject at ≤280, **\$1,000** at 290–300, rising to **\$10,000** at 410–430.

> [!warning] ⚠️ Factor 7 is non-monotonic, and that is the whole problem in miniature
> **Dependents: none 30, one 30, two 40, three 40, more than three 20.**
>
> **The best score goes to applicants with two or three dependents — not to those with none.** No human writing a rule from first principles would produce that. **It is what the data said.**
>
> **This is exactly what makes a fitted model powerful and hard to defend.** It found a real pattern *(plausibly: family formation correlates with stability, while very large families strain income)* — **but a rejected applicant told "you have too few dependents" receives an answer that sounds arbitrary, and §5 shows the law requires a specific reason.**
>
> **Even a point system — the most inspectable model there is — can be hard to justify.** That is the floor of the explainability problem, not the ceiling.

### 3. ⚠️ The cutoff is a classification threshold

*(Verified — R&H's cost-benefit at a 280-point cutoff:)*

| | | book |
|---|---|---|
| 1,200 bad loans avoided × \$600 | 720 000 | 720,000 ✓ |
| 300 good loans rejected × \$600 | 180 000 | 180,000 ✓ |
| **net saving** | **540 000** | **540,000 ✓** |

> [!note] A wording ambiguity, resolved by the book itself — not filed
> R&H writes "*of those … scoring 280 points or less, 40 percent (or 1,200) became bad loans*". *(Computed: read that way, low-scorers = 3,000, of whom **1,800 would be good** — but the book says only 300 good loans scored that low. Contradiction.)*
>
> **Its later sentence gives the consistent reading:** "*denying all applications scoring 280 or less will reduce loss accounts by about 40 percent and reject just 10 percent of the good loan customers*" — i.e. **40% of all bad loans and 10% of all good loans score ≤280**, implying 3,000 of each.
>
> **The arithmetic is right throughout; one sentence is loosely worded and a later one resolves it. Not an erratum.**

**Written properly, that is a confusion matrix:**

| | **predicted bad** (reject) | **predicted good** (approve) |
|---|---|---|
| **actually bad** | 1 200 *(TP)* | 1 800 *(FN)* |
| **actually good** | 300 *(FP)* | 2 700 *(TN)* |

$$\text{TPR}=\frac{1200}{3000}=\mathbf{40\%}\qquad\text{FPR}=\frac{300}{3000}=\mathbf{10\%}$$

> [!note] R&H's "criterion score" is a threshold and its \$540,000 is a cost-weighted objective
> **(40%, 10%) is one point on an ROC curve.** Move the cutoff and you trace the rest of it.
>
> **So credit scoring is [[Machine Learning/contents/00-Index|supervised binary classification]] with asymmetric misclassification costs** — and every part of the apparatus transfers: [[Probability Theory/contents/00-Index|probability]] for the score distributions, [[Econometrics/contents/00-Index|logistic regression]] for the fitting, and the whole discipline of out-of-sample validation.
>
> **R&H's own caveat is the classic one**: the model assumes "the same factors that separated good from bad loans in the past will … separate good from bad loans in the future," and this "can be wrong if the economy or other factors change abruptly." **That is distribution shift**, and it is why scoring systems must be revalidated — a requirement §5 shows is also *legal*, not merely statistical.

**R&H says management "can experiment with other criterion scores to determine which cutoff point yields the greatest net savings." It never does.** *(Computed — calibrating score distributions to reproduce the book's 40%/10% at 280, then sweeping:)*

| cutoff | bad caught | good lost | **net saving** |
|---|---|---|---|
| 240 | 490 | 67 | 254 002 |
| **280** *(R&H)* | **1 200** | **300** | **540 000** |
| 300 | 1 632 | 538 | 656 241 |
| **322** | **2 077** | **907** | **707 070** ← optimum |
| 340 | 2 397 | 1 273 | 674 026 |
| 380 | 2 824 | 2 113 | 426 511 |

**R&H's 280 is reasonable but not optimal** on its own criterion — the peak is near **322**, worth about **31% more.**

### 4. ⚠️ The optimum is a property of the cost ratio, not the model

**R&H charges \$600 for a bad loan *and* \$600 for a rejected good one. Those are not the same quantity.**

- **A bad loan loses the principal** (net of recovery).
- **A rejected good loan loses only the profit you would have made** — on a \$2,000 consumer loan at a 5% net margin, about **\$100**, not \$600.

*(Computed — the optimal cutoff at different cost ratios:)*

| cost of a bad loan | profit forgone | **optimal cutoff** | good applicants rejected |
|---|---|---|---|
| \$600 | \$600 *(R&H)* | 322 | 907 — **30.2%** |
| \$600 | \$300 | 359 | 1 685 — **56.2%** |
| **\$600** | **\$100** | **418** | **2 671 — 89.0%** |
| \$1 200 | \$100 | 455 | 2 914 — **97.1%** |

> [!warning] The same model and the same data justify a cutoff anywhere across that range
> **When rejecting a good customer is cheap relative to funding a bad one, the model rejects almost everybody** — 89.0% of *creditworthy* applicants at a realistic cost ratio.
>
> **So the "optimal" cutoff is not a statistical result. It is a business decision wearing a statistical costume.**
>
> **This is the single most important thing to understand about deploying a classifier, in any domain: the model produces a *ranking*; the threshold is chosen by somebody with an objective.** The ranking can be excellent and the threshold still cause enormous harm — **and the threshold is the part that never appears in the model documentation.**
>
> **Note also what the cost ratio quietly encodes.** The lender's cost of a false rejection is its forgone margin. **The *applicant's* cost of a false rejection is not in the objective function at all** — which is precisely the gap that §5's regulation exists to fill.

### 5. ⚠️ The regulation, and why it binds this model specifically

**The Equal Credit Opportunity Act and Regulation B prohibit scoring on race, colour, religion, national origin, sex, marital status, age, or receipt of public assistance.** *(Age is permitted only if the lender can demonstrate statistical significance and revalidate regularly.)* **Truth in Lending requires disclosure of the APR and all finance charges; the Fair Credit Reporting Act governs the bureau data the model is built on.**

> [!warning] Omitting a protected variable does not remove its effect
> *(Computed — take one facially neutral feature, "telephone in home", worth 20 points, held by 95% of one group and 70% of another:)*
>
> | | expected points from that one factor |
> |---|---|
> | group A | 19.0 |
> | group B | 14.0 |
> | **gap** | **5.0 points** |
>
> **At a 280-point cutoff that 5-point gap produces approval rates of 90.00% and 88.31% among *equally creditworthy* applicants — a 1.69% difference** *(computed)*.
>
> **The model never saw the protected characteristic, and one proxy variable produced a measurable gap. Real models have dozens of features, and the proxies compound.**
>
> **Hence the legal doctrine of disparate impact: a lender is liable for the *effect*, not merely the intent.** Removing the protected variable is necessary and nowhere near sufficient — **the correct test is to measure outcomes across groups, which requires collecting the very data the model may not use.**

> [!warning] A model that cannot be explained cannot legally decline an applicant
> **ECOA requires a lender taking adverse action to give the applicant *specific* reasons** — not "our model said no."
>
> **This is a binding constraint on model choice, not a preference.** It is why consumer credit remains one of the few high-stakes domains where **simple, inspectable models are still standard**, decades after more accurate methods became available.
>
> **And §2's non-monotonic dependents factor shows the floor of the problem**: even a hand-built point system produces reasons that are hard to defend to a rejected applicant. **A model whose reasons are post-hoc reconstructions has not met the requirement — it has met the appearance of it.**
>
> **For a data scientist this is the transferable lesson of the whole chapter**: *in regulated domains the constraint on your model is not accuracy — it is whether you can justify a single decision to the person it was made about.* **Choose the model class before choosing the features.**

### 6. ⚠️ Card lending sits past the peak — and why it works anyway

**[[11 - Lending - Policy, Credit Risk and Business Loans|Ch. 11]] §6 found the expected return humped, peaking at $r^*=18.00\%$. Credit cards post APRs well above that.** *(Computed on the same model:)*

| posted APR | implied P(default) | **expected return** |
|---|---|---|
| 6% | 1.00% | 5.3400% |
| **18%** | 14.20% | **6.9240%** ← peak |
| **25%** | 21.90% | **6.3850%** |
| 30% | 27.40% | 5.3400% |
| 36% | 34.00% | 3.3600% |

**A 25% card APR is past the peak: 6.39% expected return against the 6.92% available at 18%.** *(And R&H notes payday lending at APRs "up to 400 percent".)*

> [!note] So the lender rations by quantity instead of price — and R&H's own table says so
> **Card lending works because price is not the risk-management tool. Three things are:**
>
> 1. **The credit limit.** [[#2 The scoring model, verified|§2]]'s Table 18-5 is the mechanism: **the score sets the *amount*, not the rate** — \$1,000 at 290 points, \$10,000 at 410+. **Everyone pays roughly the same APR; the score decides how much they can borrow.**
> 2. **The limit can be cut at any time**, which no term loan allows.
> 3. **Fee and interchange income**, which does not depend on the borrower carrying a balance at all.
>
> **[[11 - Lending - Policy, Credit Risk and Business Loans|Ch. 11]] predicted exactly this: past $r^*$, refuse or limit — do not reprice.** Business lending rations by *declining*; consumer lending rations by *capping*. **Same response to the same mathematics, and R&H's Table 18-5 has been showing it all along without saying why.**
>
> **The CARD Act of 2009** — restricting rate increases without notice — **removes some of the lender's ability to reprice after the fact**, which pushes the business further toward limit management and fee income.

### 7. Real estate lending: the differences that matter

**Mortgages differ from other consumer loans in ways that recur throughout this subject:**

- **They are the largest and longest loans a bank makes** — so [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s duration gap is dominated by them.
- **The collateral is the point**, and its value moves with a market the borrower does not control.
- **They carry prepayment risk** — [[07 - The Investment Portfolio|ch. 07]] §4's negative convexity: **the borrower refinances when rates fall and does not when they rise.** A written option the bank was never paid a visible premium for.
- **They are securitised** ([[06 - Hedging with Derivatives|ch. 06]]), which is what made a local credit decision a systemic exposure.

> [!warning] The mortgage is where every chapter of this subject meets
> **A 30-year fixed-rate mortgage funded by overnight deposits is [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s duration gap in its purest form; it is [[07 - The Investment Portfolio|ch. 07]]'s negative convexity; it is [[10 - Capital Adequacy and Basel|ch. 10]]'s 50% risk weight that 2008 proved wrong; it is [[06 - Hedging with Derivatives|ch. 06]]'s tranching input; and it is [[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]] §7's concentration risk, because house prices across a region move together.**
>
> **That last point is the one to carry.** [[11 - Lending - Policy, Credit Risk and Business Loans|Ch. 11]] computed that correlation leaves the mean loss unchanged and transforms the tail. **A mortgage book is the most correlated portfolio a bank holds**, because every loan in it is a bet on the same house-price index — **and each individual loan can be underwritten impeccably while the portfolio is one position.**

## ✏️ Exercises

**1. (Credit scoring as classification.)** (a) Verify the model and the cutoff. (b) What is the cutoff, in statistical terms? (c) Find the optimum. (d) What does R&H get wrong about the costs?

> [!example]- Solution
> **(a) Both verify.**
>
> *(Computed: the maximum score is **430** and the minimum **90**, matching the book — from all eight factors and 28 point values. The cost-benefit at a 280 cutoff: $1{,}200\times\$600=\$720{,}000$ saved, $300\times\$600=\$180{,}000$ forgone, **net \$540,000** ✓.)*
>
> *(One wording ambiguity, resolved and not filed: the book says "of those scoring 280 or less, 40 percent (or 1,200) became bad loans", which would imply 3,000 low-scorers of whom **1,800 are good** — contradicting the stated 300. **Its later sentence gives the consistent reading**: 40% of all *bad* loans and 10% of all *good* loans score ≤280. The arithmetic is right throughout.)*
>
> **(b) A classification threshold, and the 40%/10% is a point on an ROC curve.**
>
> | | predicted bad | predicted good |
> |---|---|---|
> | actually bad | **1,200** (TP) | 1,800 (FN) |
> | actually good | **300** (FP) | 2,700 (TN) |
>
> **TPR = 40%, FPR = 10%**, and the \$540,000 is a **cost-weighted objective function**.
>
> **So this is supervised binary classification with asymmetric misclassification costs**, and everything from [[Machine Learning/contents/00-Index|Machine Learning]] transfers: the score is a ranking, the cutoff turns it into a decision, and the two are separate choices.
>
> **R&H's own caveat is the standard one** — the model assumes the past separates the future, and "can be wrong if the economy or other factors change abruptly." **That is distribution shift**, and it is why revalidation is required both statistically and (per §5) legally.
>
> **(c) Near 322 points, worth about 31% more than R&H's 280.**
>
> **R&H says management "can experiment with other criterion scores" and stops.** *(Computed by calibrating score distributions to reproduce 40%/10% at 280, then sweeping: the net saving rises from **\$540,000 at 280** to **\$707,070 near 322**, then falls to \$674,026 at 340 and \$426,511 at 380.)*
>
> **The curve is humped, exactly like [[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]] §6's** — and for a structurally similar reason: **tightening catches more bad loans at an accelerating cost in good ones.** Past the peak you reject more good customers than the additional bad loans are worth.
>
> **(d) It charges the same \$600 for both errors, and they are not the same quantity.**
>
> **A bad loan loses the principal. A rejected good loan loses only the margin** — about **\$100** on a \$2,000 loan at a 5% net margin.
>
> *(Computed: at \$600 against \$100 the optimal cutoff moves from **322 to 418**, and good applicants rejected goes from **30.2% to 89.0%**. At \$1,200 against \$100 it reaches 455 and **97.1%**.)*
>
> **So the optimal cutoff is not a property of the scoring model. It is a property of the cost ratio** — and the same model on the same data justifies a cutoff anywhere across that range.
>
> **This is the general lesson and it is worth more than the banking context: the model gives you a ranking, and someone with an objective picks the threshold.** A superb model with a badly chosen threshold does enormous damage, and **the threshold is the part that never appears in the model documentation.**
>
> **And note what the objective omits.** The lender's cost of a false rejection is its forgone margin; **the applicant's cost is not in the function at all.** That asymmetry is not a modelling oversight — it is a correct representation of the lender's incentives, **which is exactly why the constraint has to come from outside**, in §5.

**2. (Hard — regulation.)** (a) What does ECOA prohibit and why isn't omission enough? (b) Compute disparate impact. (c) What does explainability require? (d) What does this mean for a data scientist?

> [!example]- Solution
> **(a) It prohibits the variables, and the variables are not the problem — the correlations are.**
>
> **ECOA and Regulation B prohibit scoring on race, colour, religion, national origin, sex, marital status, age, or receipt of public assistance.** *(Age is admissible only on a demonstrated statistical showing, with regular revalidation.)*
>
> **But a model built without those variables still uses whatever correlates with them.** Occupation, housing status, time at address, deposit accounts held, telephone in home — **every factor in R&H's Table 18-4 is plausibly correlated with a protected characteristic**, and a fitted model will use them precisely to the extent they predict, which is partly *because* of that correlation.
>
> **So omission removes the label and keeps the effect.**
>
> **(b) One 20-point proxy produces a 1.69% approval gap.**
>
> *(Computed — "telephone in home", worth 20 points, held by 95% of group A and 70% of group B:)*
>
> | | expected points | approval rate among **equally creditworthy** applicants |
> |---|---|---|
> | group A | 19.0 | **90.00%** |
> | group B | 14.0 | **88.31%** |
>
> **A 5-point expected gap becomes a 1.69 percentage-point gap in approvals between applicants of identical creditworthiness.**
>
> **And that is one feature.** R&H's model has eight; a modern model has hundreds, and **the proxies compound rather than cancel** — each one that correlates with the protected characteristic pushes the same direction.
>
> **Hence disparate impact: liability attaches to the *effect*, not the intent.** A lender cannot defend itself by showing the variable was excluded; **it must show the outcomes are acceptable.**
>
> **Which produces a genuine and underappreciated bind: testing for disparate impact requires measuring outcomes by protected class, so the lender must *collect* data it is forbidden to *use*.** Collecting it and modelling with it are different acts, and conflating them is a common and expensive error.
>
> **(c) A specific reason for every adverse action — which constrains the model class.**
>
> **ECOA requires a lender declining an application to tell the applicant *why*, specifically.** "The model scored you below our cutoff" does not satisfy it.
>
> **So a model whose decisions cannot be explained cannot legally be used to decline an applicant.** That is not a preference or a best practice; **it is a constraint on the hypothesis space**, and it is why consumer credit remains one of the few high-stakes domains where **simple, inspectable models are still standard** long after more accurate methods existed.
>
> **§2's non-monotonic dependents factor shows how low the floor is.** A hand-built point system — the most transparent model there is — **already produces a reason ("you have too few dependents") that is hard to defend.** The pattern is real and the explanation is unsatisfying, **and an explanation that does not satisfy the applicant does not satisfy the statute.**
>
> **A post-hoc attribution over an opaque model is worse**, because it produces a reason that was not the reason. **That meets the appearance of the requirement and not the requirement.**
>
> **(d) Choose the model class before choosing the features.**
>
> **The transferable lesson: in a regulated domain the binding constraint is not accuracy — it is whether you can justify a single decision to the person it was made about.**
>
> **Four things follow, and they generalise well beyond lending:**
>
> 1. **Decide what must be explainable before modelling.** Retrofitting explainability onto a chosen model does not work; it changes which models are admissible.
> 2. **Separate the ranking from the threshold, and treat the threshold as a policy decision.** §4 showed it moving the rejection rate from 30% to 89% with no change in the model.
> 3. **Measure outcomes across groups**, and understand that this requires collecting protected data you may not model on.
> 4. **Revalidate.** R&H's own caveat is distribution shift, and here it is a legal obligation as well as a statistical one.
>
> **This is the most directly applicable material in the subject for a data-science degree**, and it is why the [[00-Index|index]] flagged it at the start: **credit scoring is where a model meets a person who is entitled to an answer.**

**3. (Card and mortgage lending.)** (a) Why do card APRs exceed $r^*$? (b) How is the risk managed instead? (c) What makes mortgages different? (d) Why is a mortgage book the most correlated portfolio a bank holds?

> [!example]- Solution
> **(a) They do exceed it, and on [[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]]'s model they are past the peak.**
>
> *(Computed on ch. 11 §6's model: the peak is at **18.00%** with an expected return of **6.9240%**; a **25%** card APR returns **6.3850%**, and 36% returns **3.3600%**.)*
>
> **So a card lender charging 25% earns less per dollar lent than one charging 18% would** — the higher rate raises the default probability faster than it raises revenue. *(And R&H notes payday lending at APRs "up to 400 percent", which on any such model is far past the point of self-defeat.)*
>
> **(b) By quantity, not price — and R&H's own Table 18-5 is the mechanism.**
>
> **The score sets the *credit limit*, not the rate**: reject at ≤280, **\$1,000** at 290–300, rising to **\$10,000** at 410–430. **Everyone pays roughly the same APR; the score decides how much they can borrow.**
>
> **That is rationing by quantity, and it is precisely what [[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]] §6 predicted**: past $r^*$, refuse or limit — do not reprice. **Business lending rations by declining; consumer lending rations by capping. Same mathematics, same response, different instrument.**
>
> **Two further defences make card lending work:**
>
> - **The limit can be cut at any time**, which no term loan permits — so the exposure is revocable in a way ch. 11's business loans are not.
> - **Fee and interchange income does not depend on the borrower carrying a balance**, so a large share of card revenue is not exposed to default at all.
>
> **The CARD Act of 2009** restricts repricing without notice, **pushing the business further toward limit management and fee income** — a regulation whose effect was to strengthen the mechanism that was already doing the work.
>
> **(c) Size, duration, collateral and the prepayment option.**
>
> - **Largest and longest loans the bank makes** — so [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s duration gap is dominated by them. A 30-year fixed mortgage funded by overnight deposits is the maturity mismatch in its purest form.
> - **The collateral is central**, and its value moves with a market neither party controls.
> - **⚠️ Prepayment risk is negative convexity** ([[07 - The Investment Portfolio|ch. 07]] §4). **The borrower refinances when rates fall and does not when they rise** — so the bank's asset shortens exactly when it wanted length and lengthens exactly when it wanted none. **A written option, correlated the wrong way, for which no visible premium was received.**
> - **They are securitised** ([[06 - Hedging with Derivatives|ch. 06]]), which converted a local credit decision into a systemic exposure.
>
> **(d) Because every loan in it is a bet on the same house-price index.**
>
> **[[11 - Lending - Policy, Credit Risk and Business Loans|Ch. 11]] §7 computed that correlation leaves the mean loss untouched and transforms the tail** — 99th-percentile loss going from 3.60% to 17.60%, and the probability of exhausting equity from 0.0000% to 4.3770%.
>
> **A mortgage book is the extreme case.** Each borrower is independently underwritten — income verified, credit scored, collateral appraised — **and every one of them defaults for the same reason at the same time**, because regional employment and house prices drive all of them.
>
> **So the loan-by-loan process can be flawless and the portfolio still be a single position.** [[06 - Hedging with Derivatives|Ch. 06]] §10 showed what happens next: tranching such a pool prices the senior claim on an assumption about correlation, and **nothing about the individual loans has to change for that assumption to be wrong.**
>
> **This is the subject's deepest result appearing for the fourth time** — [[02 - Organization, Structure and Market Entry|ch. 02]]'s $\sigma\sqrt{(1+\rho)/2}$, [[06 - Hedging with Derivatives|ch. 06]]'s tranching, [[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]]'s loan book, and now the mortgage portfolio. **The average is always fine and the joint behaviour is everything.**

## 📝 Summary

- **Consumer lending is automated because it must be**: a \$2,000 loan cannot support an officer's judgement, so the decision is a model. **Consumer loans are also the least rate-sensitive category**, which flatters [[04 - Measuring and Evaluating Bank Performance|ch. 04]]'s margins.
- **R&H's scoring model verified** — eight factors, 28 point values, **maximum 430 and minimum 90** ✓. **The score sets the credit *limit*** (Table 18-5: \$1,000 at 290 points to \$10,000 at 410+), **not the rate.**
- **⚠️ Factor 7 is non-monotonic** — two or three dependents score **40**, none scores **30**. **No human would write that rule; the data did** — powerful, and hard to justify to a rejected applicant.
- **The cutoff cost-benefit verified**: 1,200 × \$600 saved less 300 × \$600 forgone = **\$540,000** ✓. *(A wording ambiguity in the book is resolved by its own later sentence; not an erratum.)*
- **⚠️ The "criterion score" is a classification threshold and the 40%/10% is a point on an ROC curve.** Credit scoring is **supervised binary classification with asymmetric misclassification costs** — [[Machine Learning/contents/00-Index|ML]], [[Econometrics/contents/00-Index|econometrics]] and [[Probability Theory/contents/00-Index|probability]] all transfer directly.
- **R&H says management "can experiment with other criterion scores" and never does.** *(Computed: the optimum is near **322 points** for **\$707,070**, about **31% more** than the book's 280/\$540,000, and the curve is humped like [[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]] §6's.)*
- **⚠️ R&H charges \$600 for both error types, but a rejected good loan costs only the forgone profit (~\$100).** *(Computed: at \$600/\$100 the optimal cutoff moves **322 → 418** and good applicants rejected goes **30.2% → 89.0%**; at \$1,200/\$100 it reaches **97.1%**.)*
- **⚠️ So the optimal cutoff is a property of the cost ratio, not of the model** — a business decision wearing a statistical costume. **The model gives a ranking; someone with an objective picks the threshold, and that is where the harm lives.**
- **And the applicant's cost of a false rejection is not in the objective function at all** — which is exactly the gap regulation exists to fill.
- **ECOA/Reg B prohibit scoring on protected characteristics, but ⚠️ omission removes the label and keeps the effect.** *(Computed: one 20-point proxy held by 95% vs 70% of two groups produces a **1.69%** approval gap among **equally creditworthy** applicants — and real models have dozens of proxies, which compound.)*
- **Hence disparate impact: liability attaches to the *effect*, not the intent** — and testing for it requires **collecting protected data the model may not use.**
- **⚠️ ECOA requires a specific reason for every adverse action, so a model that cannot be explained cannot legally decline an applicant.** **A constraint on the model class, not a preference** — which is why simple inspectable models remain standard here.
- **⚠️ Card APRs sit past [[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]]'s peak** *(computed: 25% APR returns **6.3850%** against **6.9240%** at 18%)*. **It works because the lender rations by *quantity*** — the credit limit, revocable at any time — **plus fee and interchange income.** Exactly what ch. 11 predicted: past $r^*$, limit rather than reprice.
- **Mortgages are the largest, longest loans a bank makes**, dominate [[05 - Interest-Rate Risk - Gap and Duration|ch. 05]]'s duration gap, and carry **prepayment risk = negative convexity** ([[07 - The Investment Portfolio|ch. 07]]) — a written option correlated the wrong way.
- **⚠️ A mortgage book is the most correlated portfolio a bank holds**, because every loan is a bet on the same house-price index. **Each loan can be underwritten impeccably while the portfolio is one position** — the subject's deepest result, for the fourth time.

## ⚠️ Important Notes

1. **Consumer lending is automated for cost reasons, not accuracy reasons.**
2. **⚠️ A fitted model finds patterns no rule-writer would produce** (the non-monotonic dependents factor). That is its value and its liability.
3. **⚠️ Separate the ranking from the threshold.** They are different objects and different decisions.
4. **A criterion score is a classification threshold; a criterion score's performance is (TPR, FPR).**
5. **⚠️ Never charge the same cost to both error types.** A bad loan loses principal; a rejected good loan loses margin.
6. **⚠️ The optimal cutoff is a property of the cost ratio.** The same model justifies rejecting 30% or 97% of good applicants.
7. **The threshold never appears in the model documentation** and does most of the damage.
8. **The applicant's cost of rejection is not in the lender's objective function.** That is why the constraint must be external.
9. **⚠️ Omitting a protected variable does not remove its effect** — proxies carry it, and they compound.
10. **⚠️ Liability attaches to the effect (disparate impact), not the intent.**
11. **Testing for disparate impact requires collecting data you may not model on.** Collection and use are different acts.
12. **⚠️ ECOA requires specific adverse-action reasons — so explainability constrains the model class.**
13. **A post-hoc explanation of an opaque model gives a reason that was not the reason.** That is the appearance of compliance.
14. **Revalidate: R&H's own caveat is distribution shift**, and here it is a legal duty too.
15. **⚠️ Card lending rations by quantity, not price** — the score sets the limit, and the limit is revocable.
16. **⚠️ Prepayment risk is negative convexity** — the borrower's option, exercised against the bank ([[07 - The Investment Portfolio|ch. 07]], [[06 - Hedging with Derivatives|ch. 06]]).
17. **A mortgage book is one bet made many times.** Perfect underwriting does not diversify it.

> [!warning] Gaps in the source material
> **R&H ch. 18 extracts well** *(PDF pp. 609–~665; book page $n$ = PDF page $n+18$)*. **Table 18-4's scoring model came through complete — all eight factors and all 28 point values — and Table 18-5's credit-limit schedule likewise.** This is the fifth consecutive chapter in which a numeric table set as text survived intact, confirming the rule [[08 - Liquidity and Reserves Management|ch. 08]] settled. *(The four standing hazards in `00-Index.md` apply; the comma-for-hyphen fault appears as "Chec~ngaccounton~", "Equal Credit Opportunity (ECO) Act".)*
>
> **Verified from the book: the maximum (430) and minimum (90) scores, and the entire cutoff cost-benefit (\$720,000 − \$180,000 = \$540,000). No erratum filed.**
>
> **One wording ambiguity reported and deliberately not filed** (§3): "of those … scoring 280 points or less, 40 percent (or 1,200) became bad loans" implies 1,800 good low-scorers against the stated 300. **The book's own later sentence gives the consistent reading** (40% of *bad* loans and 10% of *good* loans fall below the cutoff), **and all the arithmetic is correct** — so this is loose phrasing, not an error.
>
> **Figures that are mine**: the calibrated score distributions in §3 (fitted to reproduce R&H's own 40%/10% at 280), the cost ratios in §4, the group prevalences in §5, and ch. 11's default model reused in §6. **Tables 18-4 and 18-5, the cutoff example and the statutory list are the book's.**
>
> **Additions beyond the source.**
>
> - **⚠️ §3's reframing of the criterion score as a classification threshold** — writing R&H's numbers as a confusion matrix, identifying 40%/10% as (TPR, FPR), and the \$540,000 as a cost-weighted objective — **is mine.** R&H never uses the vocabulary, and the connection to [[Machine Learning/contents/00-Index|Machine Learning]] and [[Econometrics/contents/00-Index|Econometrics]] is the reason this chapter matters for the degree.
> - **⚠️ §3's threshold sweep does what the book explicitly says management "can" do and does not** — finding the optimum near **322 points** and **\$707,070**. The score distributions are mine, calibrated to the book's two stated rates; **the finding that R&H's 280 is reasonable but suboptimal on its own criterion is an addition.**
> - **⚠️ §4 is the chapter's most transferable content and is entirely mine.** R&H charges \$600 for both error types without comment. **Correcting the asymmetry and showing the optimal cutoff move from 322 to 455 — rejecting 30.2% to 97.1% of good applicants — establishes that the threshold is a business decision rather than a statistical result.**
> - **⚠️ §5's disparate-impact computation is mine.** R&H mentions ECOA and the litigation risk in two sentences and **never demonstrates that omitting a protected variable fails**. The proxy calculation, the collection-vs-use distinction, and the argument that **explainability is a constraint on the model class** are additions.
> - **§6 discharges [[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]]'s obligation** by applying its humped-return model to card APRs, and identifies **R&H's own Table 18-5 as the resolution** — consumer lenders ration by quantity. R&H presents the table as a mechanical schedule and never connects it to risk pricing.
> - **§7's identification of prepayment risk as negative convexity** ([[07 - The Investment Portfolio|ch. 07]]) and of the mortgage book as the maximally correlated portfolio ([[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]] §7) are my cross-chapter connections.
> - **The CARD Act's effect on the limit-management business model** is my inference; R&H reports the Act's provisions without drawing it.
>
> **Deliberately compressed.** **R&H ch. 18's survey of consumer loan types** (instalment, non-instalment, residential mortgage, home equity, education, auto) is compressed to the characteristics that drive the analysis. **The worked consumer loan application (§18-5)** is omitted — it is a narrative walkthrough whose analytical content is the six Cs from [[11 - Lending - Policy, Credit Risk and Business Loans|ch. 11]] plus the scoring model already covered. **Interest-rate computation methods** (simple interest, add-on, discount, and the Rule of 78s) are noted but not worked: **the Rule of 78s is prohibited or obsolete in most jurisdictions**, and the examinable content is that the **APR** is the comparable figure, which Truth in Lending requires. **The detailed statutory list** (FCRA, FDCPA, CRA, Fair Housing, RESPA, predatory-lending and payday rules) is compressed to ECOA and Truth in Lending — the two that shape the *model*; the rest are US-specific and change often. **Mortgage mechanics** (points, escrow, PMI, ARM index construction) are omitted as jurisdictional. **Disparate impact and adverse-action requirements are treated at more length than R&H gives them**, because they are the part that binds a practitioner.

**Previous:** [[11 - Lending - Policy, Credit Risk and Business Loans]] · **Next:** *(end of subject — return to [[00-Index]])*
