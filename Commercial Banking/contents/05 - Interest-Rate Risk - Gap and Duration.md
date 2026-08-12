---
subject: Commercial Banking
chapter: 5
tags: [ds, banking, interest-rate-risk, repricing-gap, duration, convexity, immunisation, alm]
source: "Rose & Hudgins, *Bank Management and Financial Services* 9e, ch. 7"
---

# Interest-Rate Risk: Gap and Duration

[[01 - The Financial-Services Industry and Its Regulation|Chapter 01]] §4 showed a rate rise cutting net interest margin from 4.00% to 2.00% and asked how to measure it. **This chapter is the answer, and it is two answers**, because there are two things to protect:

| | protects | horizon |
|---|---|---|
| **repricing gap** | **net interest income** | one period |
| **duration gap** | **net worth** | the whole balance sheet |

**A bank can be hedged on one and exposed on the other**, and §6 shows one that is exposed on both.

**The number that carries the chapter is in §6:** a 2% rate rise cuts asset values by **3.66%** and net worth by **37.24% of equity** — [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s equity multiplier turning a small price move into a large solvency event.

**Every figure is computed**, and §5 checks the duration approximation against exact repricing so its error is visible rather than assumed.

## 📘 Main Knowledge

### 1. The repricing (funding) gap

**Classify every item by whether its rate resets within the period.**

$$\text{dollar gap}=\text{RSA}-\text{RSL}$$

*(Computed from a stated balance sheet — $ thousands, and it balances: L + E = 163 000 = A:)*

| | |
|---|---|
| rate-sensitive assets (RSA) | **80 000** |
| rate-sensitive liabilities (RSL) | **97 000** |
| **dollar gap** | **−17 000** |
| relative gap (gap / assets) | **−10.429%** |
| interest-sensitivity ratio (RSA/RSL) | **0.8247** |

> [!note] A negative gap means liability-sensitive
> **More liabilities reprice than assets, so rising rates hurt** — which is [[01 - The Financial-Services Industry and Its Regulation|ch. 01]] §4's bank, now measured rather than described.
>
> **The sign convention is worth fixing once:** negative gap → hurt by rising rates; positive gap → hurt by *falling* rates; zero gap → first-order neutral.

### 2. $\Delta\text{NII} = \text{gap}\times\Delta i$

*(Verified — the formula against a direct recomputation from the underlying items:)*

| shock | predicted ΔNII | recomputed | match |
|---|---|---|---|
| −2.0% | +340 | +340 | ✓ |
| +1.0% | −170 | −170 | ✓ |
| **+2.0%** | **−340** | **−340** | ✓ |
| +3.0% | −510 | −510 | ✓ |

> [!note] The formula *is* the definition
> **Only rate-sensitive items change, so the change in net interest income is exactly $(\text{RSA}-\text{RSL})\times\Delta i$.** There is nothing to approximate at this level — the approximation is in the *classification*, not the arithmetic.
>
> **A bank with a zero gap has zero first-order exposure of NII**, which is what gap management targets.

### 3. What the gap misses

**The gap protects net interest income over one period. It says nothing about the market *value* of assets and liabilities** — which move whenever rates move, and **equity is the difference between them.**

**That is what duration measures.**

### 4. Duration, from present-value weights

*(Computed — a 5-year 6% annual-coupon bond, face 1 000, yielding 6%:)*

| $t$ | CF | PV | weight | $t\times$ weight |
|---|---|---|---|---|
| 1 | 60.00 | 56.60 | 0.0566 | 0.0566 |
| 2 | 60.00 | 53.40 | 0.0534 | 0.1068 |
| 3 | 60.00 | 50.38 | 0.0504 | 0.1511 |
| 4 | 60.00 | 47.53 | 0.0475 | 0.1901 |
| **5** | **1 060.00** | **792.09** | **0.7921** | **3.9605** |
| | | **price 1 000.00** | **1.0000** | **D = 4.4651** |

$$D_{\text{Macaulay}}=\sum_t t\cdot\frac{PV(CF_t)}{P}=4.4651\text{ years}\qquad D_{\text{mod}}=\frac{D}{1+y}=4.2124$$

> [!note] Duration is a weighted average time — and a derivative
> **The weights are each cash flow's share of present value**, and they sum to 1 *(verified)*. **So duration is the average time at which the bond's value arrives**, which is why a 5-year bond has a duration below 5: some value arrives earlier as coupons.
>
> **And it is a derivative:**
> $$\frac{dP}{P}=-D_{\text{mod}}\,dy$$
> **This is [[Calculus/contents/00-Index|Calculus]] doing real work** — duration is (minus) the elasticity of price with respect to yield, and everything in §§5–6 follows from that one fact.

### 5. ⚠️ How good is the linear approximation?

*(Computed — exact repricing versus the duration estimate:)*

| $dy$ | exact $dP/P$ | $-D_{\text{mod}}\,dy$ | error |
|---|---|---|---|
| +0.01% | −0.042% | −0.042% | +0.0000% |
| +0.25% | −1.046% | −1.053% | +0.0071% |
| **+1.00%** | **−4.100%** | **−4.212%** | **+0.1122%** |
| +2.00% | −7.985% | −8.425% | +0.4393% |
| **+5.00%** | **−18.479%** | **−21.062%** | **+2.5823%** |

> [!note] Duration always predicts a *worse* outcome than reality
> **The error is one-signed and grows with the square of the move.** At 1% it is a tenth of a percentage point; **at 5% it is 2.58 points** — the estimate says −21.1% and the truth is −18.5%.
>
> **The reason is that the price-yield curve is convex.** A straight line tangent to a convex curve lies *below* it everywhere, so the linear estimate understates price in **both** directions — it overstates losses when rates rise and understates gains when they fall.
>
> **That difference is *convexity*, and it is a benefit to the holder.** It is why duration alone is conservative for small moves and unreliable for large ones — and why a bank stress-testing a 300 bp shock cannot use duration by itself.

### 6. ⚠️ The duration gap

$$D_{\text{gap}}=D_A-u\,D_L,\qquad u=\frac{L}{A}$$
$$\Delta NW\approx-D_{\text{gap}}\times\frac{\Delta i}{1+i}\times A$$

*(Computed with $D_A = 3.20$, $D_L = 1.40$, $u = 90.184\%$:)*
$$D_{\text{gap}}=3.20-0.9018\times1.40=\mathbf{1.9374\text{ years}}$$

| shock | Δ net worth | **as % of equity** |
|---|---|---|
| −2.0% | +5 958 | +37.24% |
| +1.0% | −2 979 | −18.62% |
| **+2.0%** | **−5 958** | **−37.24%** |
| +3.0% | −8 938 | **−55.86%** |

> [!warning] A 2% rise costs 37.2% of equity while asset values fall only 3.66%
> **The 10.2× amplification is [[01 - The Financial-Services Industry and Its Regulation|ch. 01]]'s equity multiplier**, appearing again in a completely different calculation. **Equity is a thin difference between two large numbers, so a small proportional move in either is a large proportional move in the difference.**
>
> **And this bank is exposed both ways**: a **negative repricing gap** (rising rates cut income) *and* a **positive duration gap** (rising rates cut value). **Rising rates hurt its earnings and its solvency simultaneously.**
>
> **A +3% shock would destroy 55.9% of equity** — not a remote scenario, and precisely the exposure [[10 - Capital Adequacy and Basel|ch. 10]]'s capital is held against.

**Note the $u$ term.** The duration gap is not $D_A - D_L$: liabilities are scaled by $L/A$ because there are fewer of them than assets. **Omitting $u$ overstates the hedge and is the standard exam mistake.**

### 7. Immunisation, and why banks do not do it

**To set $D_{\text{gap}} = 0$ requires $D_A = u\,D_L$** *(computed)*:
- hold $D_A = 3.20$ → **liabilities must lengthen from 1.40 to 3.5483 years**, or
- hold $D_L = 1.40$ → **assets must shorten from 3.20 to 1.2626 years**.

**With $D_{\text{gap}} = 0$, $\Delta NW = 0$ for any shock, to first order.**

> [!note] Perfect immunisation surrenders the business model
> **Shortening assets to 1.26 years means giving up long-dated lending; lengthening liabilities to 3.55 years means paying up for term deposits.** Either way the bank has removed the maturity mismatch — **and [[01 - The Financial-Services Industry and Its Regulation|ch. 01]] §4 showed that the mismatch *is* the spread.**
>
> **So a perfectly immunised bank has protected its net worth and abolished its margin.**
>
> **Which is why banks target a *tolerance*, not zero** — a policy limit on how much NII or net worth may move per 100 bp — **and hedge the excess with derivatives ([[06 - Hedging with Derivatives|ch. 06]]) rather than by restructuring the balance sheet.** A swap changes the rate exposure without changing the loans.

### 8. The two gaps compared

| | protects | horizon | ignores |
|---|---|---|---|
| **repricing gap** | net income | one period | value; timing *within* a bucket |
| **duration gap** | net worth | whole balance sheet | convexity; non-parallel shifts; embedded options |

**Both are first-order approximations of the same underlying exposure**, and **they can disagree** — which is why banks compute both.

## ✏️ Exercises

**1. (The repricing gap.)** (a) How is it constructed and what does the sign mean? (b) Why is $\Delta\text{NII}=\text{gap}\times\Delta i$ exact? (c) What does it miss? (d) What are its practical weaknesses?

> [!example]- Solution
> **(a) Classify every item by whether its rate resets within the period, then subtract.**
>
> *(Computed: RSA 80 000, RSL 97 000, **gap −17 000**, relative gap **−10.429%**, ISR **0.8247**.)*
>
> **Sign convention:**
>
> | gap | rising rates | falling rates |
> |---|---|---|
> | **negative** (liability-sensitive) | **hurt** | help |
> | **positive** (asset-sensitive) | help | **hurt** |
> | zero | neutral | neutral |
>
> **This bank is liability-sensitive**, which is the normal position for a deposit-funded bank — deposits reprice quickly, fixed-rate loans do not. **It is [[01 - The Financial-Services Industry and Its Regulation|ch. 01]] §4's bank, quantified.**
>
> **The relative gap and ISR exist so that banks of different sizes can be compared** — a −17 000 gap means nothing without knowing the balance sheet is 163 000.
>
> **(b) Because only rate-sensitive items change, by construction.**
>
> *(Verified: the formula matched a direct recomputation at every shock tested — +340, −170, −340, −510.)*
>
> **Non-sensitive items keep their rates for the period, so they contribute nothing to the *change*.** Sensitive assets all move up by $\Delta i$ and sensitive liabilities all move up by $\Delta i$, so the change in net interest income is $(\text{RSA}-\text{RSL})\Delta i$ exactly.
>
> **So there is nothing to approximate in the arithmetic. The approximation is in the classification** — see (d).
>
> **(c) Value. It protects income, not net worth.**
>
> **A bank can have a zero repricing gap and still lose a third of its equity to a rate move**, because the *market values* of long assets and short liabilities respond differently. **Income and value are different exposures**, and §6 measures the other one.
>
> **(d) Three, and they all live in the classification.**
>
> 1. **The bucket hides timing.** Everything repricing "within one year" is treated identically, but an asset repricing tomorrow and one repricing in eleven months are very different. *(Real practice uses multiple buckets — 0–30 days, 30–90, and so on.)*
> 2. **"Rate-sensitive" is a judgement, not a fact.** Demand deposits pay no contractual rate and are formally insensitive — **but their true behaviour depends on customers, and misclassifying a large deposit base swings the gap enormously.**
> 3. **It assumes a parallel shift**, and assumes RSA and RSL reprice by the *same* amount. **Deposit rates typically move less than one-for-one with market rates**, so the effective gap differs from the measured one.
>
> **All three mean the gap is only as good as the assumptions behind the buckets** — which is why it is a management tool rather than a precise measurement.

**2. (Hard — duration.)** (a) What is duration and why is a 5-year bond's duration 4.47? (b) Why is it a derivative? (c) Interpret the approximation errors. (d) What is convexity and who benefits?

> [!example]- Solution
> **(a) The present-value-weighted average time at which a security's cash flows arrive.**
>
> $$D=\sum_t t\cdot\frac{PV(CF_t)}{P}$$
>
> *(Computed: **4.4651 years** for a 5-year 6% bond at par, with the weights summing to 1.0000 exactly.)*
>
> **It is below 5 because the coupons arrive earlier.** The weight table shows why: **the final payment carries 79.21% of the present value** and the four coupons carry the remaining 20.79% at times 1–4. **The average is pulled down from 5 to 4.47 by that fifth.**
>
> **Two consequences worth remembering:** a **zero-coupon** bond has duration exactly equal to its maturity (one cash flow, weight 1); and **higher coupons mean shorter duration**, because more value arrives early.
>
> **(b) Because $dP/P = -D_{\text{mod}}\,dy$ — it is (minus) the elasticity of price with respect to yield.**
>
> $$P=\sum_t\frac{CF_t}{(1+y)^t}\;\Longrightarrow\;\frac{dP}{dy}=-\sum_t\frac{t\,CF_t}{(1+y)^{t+1}}=-\frac{P\,D}{1+y}$$
>
> **so** $\frac{1}{P}\frac{dP}{dy}=-\frac{D}{1+y}=-D_{\text{mod}}$ *(computed: 4.4651/1.06 = **4.2124**)*.
>
> **This is [[Calculus/contents/00-Index|Calculus]] doing real work in a finance course**, and it explains everything else: **duration is a first derivative, so it is a *local linear* approximation** — accurate near the current yield and degrading as you move away, exactly as (c) shows.
>
> **(c)** *(Computed:)*
>
> | $dy$ | error |
> |---|---|
> | +0.01% | 0.0000% |
> | +1.00% | 0.1122% |
> | +5.00% | **2.5823%** |
>
> **The error is negligible for small moves and substantial for large ones**, and it grows roughly with $dy^2$ — a factor-of-5 larger shock gives a ~23× larger error, close to $5^2$.
>
> **And it is one-signed: the estimate always predicts a worse price than reality.** At +5% duration says −21.06% and the truth is −18.48%.
>
> **So duration is *conservative* for rate rises** — it overstates the loss — **and *pessimistic* for rate falls**, understating the gain. **For a bank stress-testing a 300 bp shock, the estimate is on the safe side, but by enough to matter.**
>
> **(d) The curvature of the price–yield relationship, and it benefits the holder.**
>
> **Price is a convex function of yield** — it falls at a decreasing rate as yields rise and rises at an increasing rate as they fall. **Duration is the tangent line, and a tangent to a convex curve lies below it everywhere**, so the linear estimate understates price in both directions.
>
> **That asymmetry is valuable.** For a given duration, **more convexity means smaller losses when rates rise and larger gains when they fall** — so convexity is a desirable property and, in efficient markets, one you pay for through a lower yield.
>
> **Formally it is the second derivative**, and the second-order Taylor expansion is
> $$\frac{dP}{P}\approx-D_{\text{mod}}\,dy+\tfrac12 C\,(dy)^2$$
> **which is why the error grows with the square of the move** — exactly the pattern in the table.
>
> **Practically: use duration for small moves and for hedging, and full repricing for stress tests.** A bank that models a 300 bp shock with duration alone is using a tool outside its accurate range.

**3. (The duration gap.)** (a) Why the $u$ term? (b) Interpret the net-worth table. (c) Why don't banks immunise? (d) When do the two gaps disagree?

> [!example]- Solution
> **(a) Because there are fewer liabilities than assets, so their duration must be scaled by $L/A$.**
>
> $$D_{\text{gap}}=D_A-u\,D_L,\qquad u=\frac{L}{A}$$
>
> *(Computed: $3.20-0.9018\times1.40=$ **1.9374 years**. Without $u$ it would be $3.20-1.40=1.80$ — an understatement of the exposure by 7%.)*
>
> **The intuition: net worth is $A - L$, so its sensitivity is the sensitivity of $A$ minus the sensitivity of $L$** — and the liability side is only 90.18% as large, so its duration contributes proportionally less.
>
> **Omitting $u$ is the standard exam error**, and it always makes the bank look better hedged than it is when $u < 1$.
>
> **(b) A 2% rise destroys 37.24% of equity while asset values fall only 3.66%.**
>
> *(Computed across shocks: +1% → −18.62% of equity; **+2% → −37.24%**; +3% → **−55.86%**.)*
>
> **The amplification is 10.2×, which is exactly the equity multiplier** ([[01 - The Financial-Services Industry and Its Regulation|ch. 01]], [[04 - Measuring and Evaluating Bank Performance|ch. 04]]). **Equity is a thin difference between two large numbers**, so a small proportional change in either side is a large proportional change in the difference.
>
> **And the bank is exposed on both measures at once**: a **negative repricing gap** (rising rates cut income) and a **positive duration gap** (rising rates cut value). **That is the typical position of a deposit-funded bank holding long assets** — and it is why a sustained rate rise is the classic threat to banking, historically and in 2023.
>
> **A +3% shock removing 55.9% of equity is not a tail scenario**, which is precisely why [[10 - Capital Adequacy and Basel|ch. 10]]'s capital exists.
>
> **(c) Because immunisation removes the mismatch, and the mismatch is the business.**
>
> *(Computed: to reach $D_{\text{gap}}=0$, liabilities must lengthen from **1.40 to 3.55 years**, or assets shorten from **3.20 to 1.26 years**.)*
>
> **Either change abolishes the maturity transformation** that [[01 - The Financial-Services Industry and Its Regulation|ch. 01]] §1 identified as one of the bank's four services and §4 showed generating the spread. **A perfectly immunised bank has protected its net worth and given up its margin.**
>
> **So banks do three things instead:**
> 1. **Set a tolerance, not a target of zero** — a policy limit such as "NII may not fall more than X% for a 100 bp shock".
> 2. **Hedge the excess with derivatives** ([[06 - Hedging with Derivatives|ch. 06]]) — a swap changes the rate exposure **without touching the loan book**, which is the decisive advantage.
> 3. **Hold capital against what remains** ([[10 - Capital Adequacy and Basel|ch. 10]]).
>
> **This is the pattern [[01 - The Financial-Services Industry and Its Regulation|ch. 01]] predicted: the risk is priced and controlled, never eliminated** — because eliminating it eliminates the revenue.
>
> **(d) Whenever the timing of repricing differs from the timing of value.**
>
> **The classic case is a floating-rate loan with a long maturity.** It reprices immediately, so it is **rate-sensitive** and shortens the repricing gap. **But its duration is short too** — so it helps both. **Now reverse it: a fixed-rate mortgage funded by a 5-year CD** is insensitive in the one-year bucket (helping the repricing gap) while having a long duration (hurting the duration gap).
>
> **More generally:**
> - the **repricing gap** looks at a **window** and ignores everything outside it;
> - the **duration gap** looks at the **whole balance sheet** and ignores timing within it.
>
> **So a bank can zero its one-year gap and retain a large duration gap**, or vice versa. **They answer different questions — income this year, value overall — and a bank needs both**, which is why R&H presents them as complementary rather than as alternatives.

## 📝 Summary

- **Two measures, two things protected**: the **repricing gap** protects **net interest income** over one period; the **duration gap** protects **net worth** across the whole balance sheet.
- **Repricing gap = RSA − RSL** *(computed: **−17 000**, relative gap **−10.429%**, ISR **0.8247**)*. **Negative = liability-sensitive = hurt by rising rates.**
- **$\Delta\text{NII}=\text{gap}\times\Delta i$ is exact, not approximate** *(verified against direct recomputation at every shock)* — the approximation lives in the *classification*, not the arithmetic.
- **The gap's weaknesses are all in the buckets**: timing hidden within a bucket, "rate-sensitive" being a judgement (especially for demand deposits), and the assumption of a parallel one-for-one shift.
- **Duration is the PV-weighted average time of the cash flows** *(computed: **4.4651 years** for a 5-year 6% bond, weights summing to 1.0000)* — below 5 because the final payment carries only **79.21%** of the value.
- **And it is a derivative**: $dP/P=-D_{\text{mod}}dy$, with $D_{\text{mod}}=D/(1+y)=$ **4.2124** — [[Calculus/contents/00-Index|Calculus]] doing real work.
- **⚠️ The linear estimate degrades with the square of the move** *(computed: error **0.0000%** at 1 bp, **0.1122%** at 1%, **2.5823%** at 5%)* — and is **one-signed**, always predicting a worse price than reality.
- **That is convexity, and it benefits the holder** — smaller losses when rates rise, larger gains when they fall. **Use duration for small moves; use full repricing for stress tests.**
- **Duration gap $=D_A-u\,D_L$ with $u=L/A$** *(computed: **1.9374 years**)*. **Omitting $u$ understates the exposure** and is the standard error.
- **⚠️ A 2% rise cuts asset values 3.66% and net worth 37.24% of equity — a 10.2× amplification, the equity multiplier again.** A +3% shock removes **55.86%**.
- **This bank is exposed both ways** — negative repricing gap *and* positive duration gap — **the typical position of a deposit-funded bank holding long assets.**
- **Immunisation requires lengthening liabilities from 1.40 to 3.55 years, or shortening assets from 3.20 to 1.26** *(computed)* — **which abolishes the maturity mismatch that generates the spread.** So banks set a **tolerance**, hedge the excess with [[06 - Hedging with Derivatives|derivatives]], and hold [[10 - Capital Adequacy and Basel|capital]] against the rest.

## ⚠️ Important Notes

1. **Fix the sign convention once**: negative gap → hurt by rising rates; positive gap → hurt by falling rates.
2. **Use the relative gap or ISR when comparing banks** — a dollar gap is meaningless without the balance-sheet size.
3. **⚠️ The gap is only as good as the bucket definitions.** Timing within a bucket is invisible, and "rate-sensitive" is a judgement.
4. **Watch the treatment of demand deposits.** They have no contractual rate, so classifying them swings the gap enormously.
5. **The gap assumes a parallel, one-for-one shift.** Deposit rates usually move less than market rates, so the effective gap differs from the measured one.
6. **A zero repricing gap does not protect net worth** — that is a different exposure entirely.
7. **⚠️ Include the $u=L/A$ term in the duration gap.** Omitting it always makes the bank look better hedged than it is.
8. **Remember `1/EM` amplification**: a small percentage move in asset values is a large percentage move in equity.
9. **⚠️ Do not use duration for large shocks.** The error grows with the square of the move — 2.58 points at 5%.
10. **Duration is conservative for rate rises** (it overstates the loss) and pessimistic for falls. Convexity is a benefit you pay for in yield.
11. **Use full repricing, not duration, for stress tests** of 200–300 bp or more.
12. **Do not aim for a zero duration gap.** Perfect immunisation abolishes the maturity mismatch that generates the spread.
13. **Hedge with derivatives rather than restructuring the balance sheet** — a swap changes the exposure without touching the loans ([[06 - Hedging with Derivatives|ch. 06]]).
14. **Compute both gaps.** They answer different questions and can disagree; being hedged on one says nothing about the other.

> [!warning] Gaps in the source material
> **Rose & Hudgins ch. 7 extracts as clean prose** — the rate-sensitivity discussion, the gap definitions, the duration development and the immunisation material all came through readably. **Book page $n$ = PDF page $n+18$; ch. 7 is PDF pages 235–272.** *(The four standing extraction hazards in `00-Index.md` apply.)*
>
> **The numerical exhibits are images and are lost**, consistent with the graphical/tabular distinction established in [[03 - Bank Financial Statements|ch. 03]]: **the price–yield curve figure and the gap-schedule tables did not survive**, while prose formulas did. **So every worked example in this chapter is constructed and computed rather than reproduced.**
>
> **All figures are mine**: the rate-sensitivity schedule in §1 (stated explicitly, and verified to balance — L + E = 163 000 = A), the bond in §4, and the durations in §6. **The formulas — dollar gap, relative gap, ISR, $\Delta\text{NII}=\text{gap}\times\Delta i$, Macaulay and modified duration, and $D_{\text{gap}}=D_A-u D_L$ — are the book's.**
>
> **No error was found in Rose & Hudgins ch. 7.**
>
> **Additions beyond the source.** **R&H develops gap and duration carefully and this is among its strongest chapters. What is added is verification and the error analysis:**
>
> - **§2 verifies $\Delta\text{NII}=\text{gap}\times\Delta i$ against a direct recomputation** rather than presenting it as a formula — establishing that it is exact by construction, and that the real approximation is in the classification (§1's weaknesses, Exercise 1(d)).
> - **§4 computes duration from the PV weight table** and confirms the weights sum to 1, so "weighted average time" is visible rather than asserted. **The observation that the final payment carries 79.21% of the value** is what explains why a 5-year bond has a 4.47-year duration.
> - **⚠️ §5 is the chapter's most useful addition and is mine.** R&H states that duration is an approximation; **computing the error at five shock sizes shows it is negligible at 1 bp, 0.11 points at 1%, and 2.58 points at 5% — growing with the square of the move and always one-signed.** The practical rule that follows — *use duration for hedging, full repricing for stress tests* — is not in the source and is the operative advice.
> - **The convexity explanation** (a tangent to a convex curve lies below it, so the estimate is conservative for rises and pessimistic for falls, and convexity is therefore a benefit paid for in yield) is an addition.
> - **§6's observation that the 37.24%-of-equity impact is the equity multiplier reappearing** — the same 10.2× as [[01 - The Financial-Services Industry and Its Regulation|ch. 01]] and [[04 - Measuring and Evaluating Bank Performance|ch. 04]], now in a valuation calculation — is my cross-chapter link, as is the warning that **omitting $u$ is the standard error.**
> - **§7's argument that perfect immunisation abolishes the business model** — quantified by computing the required durations (1.40 → 3.55, or 3.20 → 1.26) — is my framing of why banks target a tolerance instead.
>
> **Deliberately compressed.** **R&H's multiple maturity-bucket gap schedules** (30-day, 90-day, cumulative gaps) are represented by the single one-year bucket, with their necessity explained in Exercise 1(d) — the arithmetic is identical per bucket and repeating it adds nothing. **The dollar-gap-versus-relative-gap-versus-ISR discussion** is condensed into §1's table. **Interest-rate futures and swaps as hedges** are deferred to [[06 - Hedging with Derivatives|ch. 06]], which owns them. **Convexity is explained and quantified but the second-order formula is given without derivation** — the derivation belongs to fixed-income mathematics, and the operative content is the error magnitude. **Yield-curve theory** (why the curve has the shape it does) is deferred to [[Monetary and Financial Theories/contents/00-Index|Mishkin]], per the boundary in `00-Index.md`; this chapter assumes parallel shifts and flags non-parallel shifts as a limitation in §8.

**Previous:** [[04 - Measuring and Evaluating Bank Performance]] · **Next:** [[06 - Hedging with Derivatives]]
