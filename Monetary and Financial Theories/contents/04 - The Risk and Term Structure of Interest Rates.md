---
subject: Monetary and Financial Theories
chapter: 4
tags: [ds, economics, interest-rates, term-structure, yield-curve, risk-premium, credit-ratings, taxes]
source: "Mishkin, *The Economics of Money, Banking, and Financial Markets*, Global Edition, ch. 6"
---

# The Risk and Term Structure of Interest Rates

**[[03 - The Behavior of Interest Rates|Ch. 03]] proceeded "as if there were only one type of security and one interest rate in the entire economy". This chapter drops that.** **Two questions: why do bonds of the *same* maturity differ (risk structure), and why do bonds of *different* maturities differ (term structure)?**

> [!warning] ⚠️ THIS CHAPTER DISCHARGES [[Commercial Banking/contents/07 - The Investment Portfolio|Commercial Banking ch. 07]]'s FORWARD REFERENCE
> **CB ch. 07 used the term structure to explain the shape of a bank's securities portfolio and explicitly deferred the derivation to here.** **§7 pays the debt — and pays back more than was borrowed: it turns out the bank's measured 3.75-point yield give-up *is* the term premium it is declining to earn.**

**Four results.**

**§2 — the crisis spread verified, with an internal check that passes** *(Baa +280 bp, Treasury **−80** bp, spread +360 bp; and **+280 − (−80) = +360** exactly)*. **⚠️ 22% of the widening came from the safe asset moving the *other* way.**

**§3 — the critical tax rate, which Mishkin does not compute.** *(Computed: $t^*=20\%$ — **below it the Treasury wins and above it the municipal bond does.** The exemption does not make munis cheap for everyone; **it sorts investors by tax bracket.**)*

**§5 — inverting the curve, which Mishkin never does.** *(Computed: **ignoring the term premium makes you forecast rate rises that are not there, and the error grows with horizon** — a true path of 5→9% reads as 5→11%.)* **This is exactly the 1980s empirical failure he reports.**

**§6 — what actually drives the error in his approximation.** *(Computed: **it is the dispersion of expected rates, not their level** — Mishkin's stated justification points at the wrong quantity.)*

## 📘 Main Knowledge

### 1. The risk structure — three factors, one maturity

$$\textbf{risk structure}=\text{why bonds of the SAME maturity have different yields}$$

| factor | effect |
|---|---|
| **default risk** | **risk premium**, always positive, rising in default risk |
| **liquidity** | less liquid ⇒ **higher** yield |
| **tax treatment** | tax-exempt ⇒ **lower** yield |

> [!note] Mishkin's own caveat is worth keeping
> **Because liquidity is bundled into the observed spread, "a risk premium should more accurately be called a *risk and liquidity premium*, but convention dictates the label risk premium."** **⚠️ So the "credit spread" you read off a screen is not a pure default measure** — a fact that matters whenever a spread is used to infer a default probability.

> [!warning] ⚠️ The mechanism is always the same and always TWO-SIDED
> **Bad news about corporate bonds shifts demand for them LEFT *and* demand for Treasuries RIGHT.** **Both moves widen the spread**, which is why spreads move faster than either yield alone. *(Everything in this chapter is [[03 - The Behavior of Interest Rates|ch. 03]]'s apparatus applied twice, in two markets at once.)*

**Credit ratings** *(Moody's / S&P / Fitch)*: **Aaa/AAA down to C/D.** **Baa (BBB) and above = investment grade; below = speculative grade, junk, or "high-yield".**

> [!warning] Conflicts of interest at the rating agencies
> **In the run-up to the crisis the agencies *advised* clients on how to structure subprime products and *rated those same products*.** **The advisory fees removed the incentive to rate accurately.** **Many AAA products were downgraded repeatedly to junk.**
>
> **⚠️ And [[Commercial Banking/contents/06 - Hedging with Derivatives|CB ch. 06]] computed *why the AAA was wrong even without any dishonesty*: the mean pool loss is 5.00% at every correlation while senior-tranche loss goes 0.0000% → 1.8044%.** **Nothing about the loans had to change for the rating to be wrong** — the rating depended on a correlation assumption. **⇒ The conflict of interest and the modelling error are separate failures, and the second would have been sufficient on its own.**

### 2. ⚠️ The global financial crisis and the Baa–Treasury spread

*(Every figure verified against Mishkin:)*

| | Jul 2007 | mid-Oct 2008 | change |
|---|---|---|---|
| **Baa corporate** | 6.63% | 9.43% | **+280 bp** ✓ |
| **US Treasury** | 4.78% | **3.98%** | **−80 bp** ✓ |
| **spread** | **1.85%** ✓ | **5.45%** ✓ | **+360 bp** ✓ |

> [!note] The table refereed itself
> **$+280-(-80)=+360$ exactly, and $9.43-3.98=5.45$, and $6.63-4.78=1.85$.** **All six figures are mutually consistent** — the kind of internal check the vault's rule 4 asks for before trusting a source's table.

> [!warning] ⚠️ The Treasury yield FELL during the worst financial crisis since 1929
> **That is the "flight to quality": the same event that made one bond less desirable made the other *more* so.** *(Computed: **77.8% of the widening is the Baa leg and 22.2% is the Treasury leg moving the opposite way.**)*
>
> **⚠️ So reading a spread as "the risky yield rose" is wrong about a fifth of the time here.** **A spread is a difference, and the difference does not say which of its parts moved** — [[01 - The Financial System and What Money Is|ch. 01]]'s *which M?*, [[02 - The Meaning of Interest Rates|ch. 02]]'s *which rate?*, [[03 - The Behavior of Interest Rates|ch. 03]]'s *which curve?*, and now ***which leg?***

### 3. ⚠️ Taxes — and the critical tax rate

*(Mishkin's example, verified — \$1,000 bonds at par, 40% bracket:)*

| | coupon | after tax |
|---|---|---|
| **Treasury** | \$100 = **10%** | keeps \$60 ⇒ **6.0%** ✓ |
| **Municipal** | \$80 = **8%**, exempt | **8.0%** ✓ |

**The muni wins despite being riskier, less liquid, and carrying a headline yield two points lower.**

> [!warning] ⚠️ But for *whom* does it win? — the question Mishkin leaves
> **Break-even: $10\%(1-t)=8\%\Rightarrow t^*=\mathbf{20\%}$.**
>
> | $t$ | after-tax Treasury | muni | winner |
> |---|---|---|---|
> | 0% | 10.00% | 8.0% | Treasury |
> | 15% | 8.50% | 8.0% | Treasury |
> | **20%** | **8.00%** | **8.0%** | **tie — $t^*$** |
> | 25% | 7.50% | 8.0% | **muni** |
> | 40% | 6.00% | 8.0% | muni |
>
> **⚠️ The tax exemption does not make municipal bonds cheap for everybody — it *sorts investors by tax bracket*.** **Below 20% they are a bad deal.**
>
> **And this explains Mishkin's own historical aside**, which otherwise sits unexplained: *"this was not true before World War II, when the tax-exempt status did not convey much of an advantage because income tax rates were extremely low."* **Exactly — with $t<20\%$ the exemption is worth nothing. The instrument did not change; the tax code did.**

> [!note] The practitioner's version — taxable-equivalent yield
> $$\text{taxable equivalent}=\frac{\text{muni yield}}{1-t}$$
> *(Computed: an 8% muni is worth a **10.00%** taxable bond at $t=20\%$, **12.31%** at 35%, **13.11%** at 39%, **16.00%** at 50%.)* **The same bond is a different asset to different holders.**

**The Obama tax increase (2013), 35% → 39%:** *(computed)* **the after-tax Treasury yield falls 6.50% → 6.10%, so the muni's advantage widens from +1.50 to +1.90 points.** **Demand for munis shifts right (price up, yield down); demand for Treasuries shifts left.**

> [!warning] ⚠️ So raising income tax rates lowers municipal borrowing costs
> **A tax change that names no municipality alters what every city in the country pays to build a school.** *(And note Mishkin's footnote 1: Treasuries are exempt from **state and local** income taxes, which is a further reason corporate yields exceed Treasury yields — the tax factor cuts more than one way.)*

### 4. ⚠️ The term structure — three theories, three facts

$$\textbf{yield curve}=\text{yields on bonds identical in risk, liquidity and tax, plotted against maturity}$$

**Three empirical facts a theory must explain:**

1. **Rates on different maturities move together over time.**
2. **When short rates are low the curve usually slopes up; when short rates are high it is more often inverted.**
3. **The curve almost always slopes up.**

| theory | key assumption | 1 | 2 | 3 |
|---|---|---|---|---|
| **expectations** | maturities are **perfect substitutes** | ✓ | ✓ | **✗** |
| **segmented markets** | maturities are **not substitutes at all** | ✗ | ✗ | **✓** |
| **liquidity premium / preferred habitat** | **substitutes but not perfect ones** | ✓ | ✓ | ✓ |

> [!note] ⚠️ Why Mishkin keeps all three
> **The two extremes are opposite assumptions and each explains exactly what the other cannot.** **The accepted theory is the middle case.** **His stated reason for teaching the failures is methodological:** *"it is important to see how economists modify theories to improve them when they find that the predicted results are inconsistent with the empirical evidence."* **⚠️ That is the chapter's most transferable content — a theory is not discarded for being wrong, it is *repaired at the assumption that produced the wrong prediction*.**

**Expectations theory.** **Perfect substitutes ⇒ equal expected returns ⇒ two one-year bonds must return the same as one two-year bond:**

$$i_{nt}=\frac{i_t+i^e_{t+1}+i^e_{t+2}+\cdots+i^e_{t+(n-1)}}{n}$$

*(Verified against Mishkin's example — expected one-year rates 5, 6, 7, 8, 9%:)*

| $n$ | average | yield | book |
|---|---|---|---|
| 1 | 5/1 | **5.000%** | 5.00 ✓ |
| 2 | (5+6)/2 | **5.500%** | 5.50 ✓ |
| 3 | (5+6+7)/3 | **6.000%** | 6.00 ✓ |
| 4 | (5+6+7+8)/4 | **6.500%** | 6.50 ✓ |
| 5 | (5+6+7+8+9)/5 | **7.000%** | 7.00 ✓ |

**Explains facts 1 and 2. Fails fact 3** — **if short rates are as likely to fall as rise, the typical curve should be *flat*, and it is not.**

**Segmented markets.** **Not substitutes at all** — investors match maturity to holding period and so "obtain a certain return with no risk at all". **Explains fact 3** *(short-bond demand is higher, so long bonds have lower prices and higher yields)* **but not 1 or 2** — **completely separate markets give no reason for yields to move together.**

**Liquidity premium / preferred habitat.**

$$\boxed{\ i_{nt}=\frac{i_t+i^e_{t+1}+\cdots+i^e_{t+(n-1)}}{n}+\ell_{nt}\ }\qquad \ell_{nt}>0,\ \text{rising in }n$$

*(Verified — same expectations, premiums 0, 0.25, 0.5, 0.75, 1.0%:)*

| $n$ | average | premium | yield | book |
|---|---|---|---|---|
| 1 | 5.000% | 0.00 | **5.000%** | 5.00 ✓ |
| 2 | 5.500% | 0.25 | **5.750%** | 5.75 ✓ |
| 3 | 6.000% | 0.50 | **6.500%** | 6.50 ✓ |
| 4 | 6.500% | 0.75 | **7.250%** | 7.25 ✓ |
| 5 | 7.000% | 1.00 | **8.000%** | 8.00 ✓ |

> [!warning] ⚠️ The decisive demonstration — flat expectations, upward curve
> *(Computed with expected short rates held **constant at 7%**:)*
>
> | $n$ | expectations theory | liquidity premium theory |
> |---|---|---|
> | 1 | 7.00% | 7.00% |
> | 3 | 7.00% | **7.50%** |
> | 5 | 7.00% | **8.00%** |
>
> **A flat curve and an upward-sloping one from *identical* expectations.** **That is fact 3, and it is precisely what the expectations theory cannot produce.**
>
> **The economics: investors prefer short bonds because they bear less interest-rate risk — [[02 - The Meaning of Interest Rates|ch. 02]]'s Table 2 measured exactly how much less** *(a 30-year bond losing 39.75% in a year where a one-year bond returned +10.00%)*. **So they must be *paid* to hold long ones, and that payment is the term premium.**

> [!note] Preferred habitat reaches the same equation by a different route
> **Investors have a preferred maturity and will leave it only for extra expected return.** **Since risk-averse investors mostly prefer the short habitat, long bonds must pay more** ⇒ **the same Equation (3).** *(Mishkin's footnote 3 adds a fourth fact the expectations theory explains: **short rates are more volatile than long rates**, because if rates are mean-reverting an *average* of them must be less volatile than the rates themselves.)*

### 5. ⚠️ Inverting the curve — the direction Mishkin never runs

**He runs the theory forwards: expectations → curve. The useful direction is backwards.**

$$i^e_{t+n-1}=n\left(i_{nt}-\ell_{nt}\right)-(n-1)\left(i_{n-1,t}-\ell_{n-1,t}\right)$$

*(Verified: inverting the liquidity-premium curve 5.00, 5.75, 6.50, 7.25, 8.00 **with** the premiums recovers 5, 6, 7, 8, 9% exactly — the true expectations.)*

> [!warning] ⚠️ Now invert the same curve while ignoring the premium
> | | $n=1$ | 2 | 3 | 4 | 5 |
> |---|---|---|---|---|---|
> | **naive "expected" short rate** | 5.00% | **6.50%** | **8.00%** | **9.50%** | **11.00%** |
> | **truth** | 5.00% | 6.00% | 7.00% | 8.00% | 9.00% |
> | **error** | 0.00 | +0.50 | +1.00 | +1.50 | **+2.00** |
>
> **⚠️ Ignoring the term premium makes you forecast rate rises that are not there, and the error grows with horizon.** **The true path rises 5→9%; the naive reading says 5→11%.**
>
> **This is not a toy problem — it is precisely the empirical failure Mishkin reports from the 1980s:** *"the spread between long- and short-term interest rates does not always help predict future short-term interest rates, a finding that **may stem from substantial fluctuations in the liquidity (term) premium** for long-term bonds."*
>
> **⚠️ And it is the vault's recurring hazard in a new dress: the naive inversion produces a plausible answer with no error signal.** **Nothing about the sequence 5.00, 6.50, 8.00, 9.50, 11.00 announces that it is wrong** — it looks like a perfectly ordinary tightening forecast.

### 6. ⚠️ Mishkin's approximation — and what really drives its error

**To reach $i_{2t}=(i_t+i^e_{t+1})/2$ he drops the cross terms, justifying it thus: "$(i_{2t})^2$ is extremely small — if $i_{2t}=10\%$, then $(i_{2t})^2=0.01$."**

**The exact condition is $(1+i_{2t})^2=(1+i_t)(1+i^e_{t+1})$ — the *geometric* mean, where the theory uses the *arithmetic* one.**

*(Computed:)*

| $i_t$ | $i^e_{t+1}$ | arithmetic | **exact (geometric)** | error |
|---|---|---|---|---|
| 9% | 11% | 10.0000% | 9.9955% | +0.0045 |
| **10%** | **10%** | 10.0000% | 10.0000% | **0.0000** |
| **5%** | **15%** | 10.0000% | 9.8863% | **+0.1137** |
| **0%** | **20%** | 10.0000% | 9.5445% | **+0.4555** |
| **20%** | **20%** | 20.0000% | 20.0000% | **0.0000** |
| 2% | 38% | 20.0000% | 18.6423% | **+1.3577** |
| **40%** | **40%** | 40.0000% | 40.0000% | **0.0000** |

> [!warning] ⚠️ The error is driven by dispersion, not level
> **Rows 2–4 all have mean 10% and errors of 0.0000, 0.1137, 0.4555** — **the error is zero when the rates are equal and grows with their spread.** **Rows 2, 5 and 7 have zero dispersion at levels 10%, 20% and 40% and *all* have exactly zero error.**
>
> **So Mishkin's justification points at $(i)^2$ — the *level* — and the level is demonstrably not what controls the error.** **The correct statement: the approximation is exact for a flat expected path and degrades with the volatility of expected rates.**
>
> **Not filed as an erratum** — his approximation is standard, his conclusion is right, and at ordinary dispersions the error is hundredths of a point. **But knowing *which* quantity controls an error is the difference between a rule of thumb and a rule.**
>
> **⚠️ This is the third dropped cross term in three chapters** — [[02 - The Meaning of Interest Rates|ch. 02]]'s Fisher equation (dropping $r\pi^e$), ch. 02's duration (first-order, dropping convexity), and now this. **Each is excellent inside its domain and silently wrong outside it, and in all three cases the source states the approximation without ever computing its error.**

### 7. ⚠️ Discharging Commercial Banking ch. 07

> [!warning] The debt, and what it pays back
> **[[Commercial Banking/contents/07 - The Investment Portfolio|CB ch. 07]] measured that a bank's securities portfolio yields 3.75 percentage points less than its loan book, and holds it anyway** — for liquidity, pledging and collateral. **It used the term structure to explain the portfolio's shape and explicitly deferred the derivation here.** **Four connections, and they run both ways:**
>
> **1. Why the curve slopes up is now a *result*, not an assumption.** **It is the liquidity/term premium** — investors must be paid to bear the interest-rate risk [[02 - The Meaning of Interest Rates|ch. 02]] measured.
>
> **2. ⚠️ So the bank's 3.75-point give-up is partly the term premium it is *declining to earn*.** **Not a mistake and not a subsidy: it is the price of the option to sell in a hurry.** **CB ch. 07 measured the price; this chapter names what is being bought.**
>
> **3. And [[Commercial Banking/contents/08 - Liquidity and Reserves Management|CB ch. 08]] says why the bank pays it.** **A bank with 9.82% equity, every asset performing and zero defaults went insolvent at 48.5% withdrawals.** **A bank forced to sell long bonds into a run realises ch. 02's Table 2 losses** — the term premium is what it forgoes to avoid that.
>
> **4. ⚠️ The segmented-markets argument *is* [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|CB ch. 05]]'s duration matching.** **Mishkin: investors "match the maturity of the bond to the desired holding period" and thereby "obtain a certain return with no risk at all."** **That is duration matching stated as a *theory of the yield curve* rather than as a risk-management technique.**
>
> **⇒ One mechanism, three subjects: [[02 - The Meaning of Interest Rates|ch. 02]] *measures* the risk, this chapter *prices* it, and Commercial Banking *manages* it.**

### 8. Reading yield curves

| slope | the market expects short rates to… |
|---|---|
| **steeply upward** | **rise** |
| mildly upward | stay about the same *(the premium alone)* |
| **flat** | **fall moderately** |
| **inverted** | **fall sharply** |

> [!warning] ⚠️ Zero slope is not the neutral point
> **Because the premium is positive, a *mildly* upward curve already means "no change" — so a *flat* curve is already bearish.** **This is the single most common misreading of a yield curve.**

*(Mishkin's worked case: the steeply inverted curve of **15 January 1981** forecast sharply lower short rates, and **three-month bills fell from 16% to 13% by March — −300 bp in about two months.**)*

> [!note] The chain that makes the yield curve a forecasting tool
> $$\text{yield curve}\ \to\ \text{expected future short rates}\quad(\textbf{this chapter})$$
> $$\text{short rates rise in booms, fall in recessions}\quad(\textbf{[[03 - The Behavior of Interest Rates|ch. 03]], Figure 7})$$
> $$\Rightarrow\ \textbf{a flat or inverted curve predicts a recession}$$
> $$\text{and since } i=r+\pi^e\quad(\textbf{[[02 - The Meaning of Interest Rates|ch. 02]]})\ \Rightarrow\ \textbf{a steep curve predicts rising inflation}$$
>
> **⚠️ So the yield curve is a free, daily, market-priced forecast — and nothing new was needed to build it.** **It is [[02 - The Meaning of Interest Rates|ch. 02]]'s present value plus [[03 - The Behavior of Interest Rates|ch. 03]]'s behaviour of rates, and it yields the best-known leading indicator in macroeconomics.** *(Mishkin adds that the slope is "often viewed as a useful indicator of the stance of monetary policy" — **which is [[03 - The Behavior of Interest Rates|ch. 03]] §7's problem partly solved**: the *level* of rates does not measure the policy stance, but the *slope* carries information the level does not.)*
>
> **Two cautions, both from Mishkin's own evidence section.** **(i) The term structure is informative over the next few months and over several years, and *unreliable in between*.** **(ii) §5 showed the inversion is only as good as your estimate of the term premium.**

## ✏️ Exercises

**1. (Risk structure.)** (a) Name the three factors. (b) Verify the crisis spread and decompose it. (c) What does the Treasury leg's sign tell you?

> [!example]- Solution
> **(a) Default risk, liquidity, tax treatment.**
>
> **These are exhaustive for bonds of the *same* maturity** — anything else is the term structure. **And the mechanism is identical in all three cases and always two-sided**: whatever makes one bond worse makes its alternative relatively better, **so both demand curves move and the spread widens from both ends.**
>
> *(Mishkin's caveat is worth carrying: **since liquidity is bundled into the observed spread, the "risk premium" is really a risk-and-liquidity premium.** So inferring a default probability from a credit spread over-states it — the spread also pays for the difficulty of selling.)*
>
> **(b) All six figures verify and the table refereed itself.**
>
> | | Jul 2007 | Oct 2008 | change |
> |---|---|---|---|
> | Baa | 6.63% | 9.43% | **+280 bp** ✓ |
> | Treasury | 4.78% | 3.98% | **−80 bp** ✓ |
> | spread | 1.85% ✓ | 5.45% ✓ | **+360 bp** ✓ |
>
> **Internal check: $+280-(-80)=+360$ exactly**, and both spread levels equal the differences of the levels. **Six numbers, all mutually consistent** — which is what the vault's rule 4 asks for before trusting a table.
>
> *(Decomposition: **77.8% of the widening is the Baa leg; 22.2% is the Treasury leg moving the other way.**)*
>
> **(c) That the safe asset became *more* desirable during the crisis — the flight to quality.**
>
> **The Treasury yield *fell* 80 bp during the worst financial crisis since 1929.** **One event, two opposite effects: perceived default risk on Baa bonds rose, which shifted demand for them left *and* demand for default-free Treasuries right.**
>
> **⚠️ So reading a spread as "the risky yield rose" is wrong about a fifth of the time here** — and in some episodes the entire widening comes from the safe leg. **A spread is a difference, and a difference never says which of its parts moved.**
>
> *(Fourth instance of the vault's running theme: **which M?** ([[01 - The Financial System and What Money Is|ch. 01]]), **which interest rate?** ([[02 - The Meaning of Interest Rates|ch. 02]]), **which curve moved?** ([[03 - The Behavior of Interest Rates|ch. 03]]), **which leg?** — here.)*

**2. (Taxes.)** (a) Verify Mishkin's example. (b) For whom does the muni win? (c) What did the 2013 tax increase do, and to whom?

> [!example]- Solution
> **(a) 6.0% against 8.0% — the muni wins.**
>
> **Treasury: \$100 coupon, keep \$60 after a 40% tax ⇒ 6.0% after tax** ✓. **Municipal: \$80 coupon, exempt ⇒ 8.0% after tax** ✓.
>
> **The muni wins *despite* being riskier** (Detroit, Stockton, Jefferson County, Harrisburg all defaulted), ***despite* being less liquid, and *despite* a headline yield two points lower.** **⚠️ The headline yield is not the yield to the investor** — a fourth "which number?" case.
>
> **(b) Anyone in a bracket above 20%.**
>
> **$10\%(1-t)=8\%\Rightarrow t^*=\mathbf{20\%}$.** Below it the Treasury wins; above it the muni does; at exactly 20% they tie.
>
> **⚠️ So the tax exemption does not make municipal bonds cheap for everybody — it *sorts investors by bracket*.** **Munis are held disproportionately by high-bracket investors not by preference but by arithmetic**, and a low-bracket investor buying them is simply making a mistake.
>
> **And this explains Mishkin's historical aside**, which otherwise floats free: *"this was not true before World War II, when the tax-exempt status did not convey much of an advantage because income tax rates were extremely low."* **Exactly — with $t<20\%$ the exemption is worthless.** **The bonds were identical; the tax code was different.**
>
> *(The practitioner's form is the **taxable-equivalent yield**, $\text{muni}/(1-t)$: **an 8% muni is worth 10.00% to a 20% taxpayer, 12.31% at 35%, 16.00% at 50%.** **The same bond is a different asset to different holders** — which is why "the" interest rate on a municipal bond is not a well-defined quantity.)*
>
> **(c) It lowered municipal borrowing costs — for every city in the country.**
>
> *(Computed: raising the top rate 35% → 39% cuts the after-tax Treasury yield from 6.50% to 6.10%, so **the muni's advantage widens from +1.50 to +1.90 points**.)*
>
> **Demand for munis shifts right ⇒ price up, yield down. Demand for Treasuries shifts left ⇒ price down, yield up.**
>
> **⚠️ So a change in the *income tax code*, which names no municipality and mentions no bond, alters what every city in the country pays to build a school.** *(And Mishkin's footnote 1 notes the mirror image: Treasuries are exempt from **state and local** income tax, which is an additional reason corporate yields exceed Treasury yields. **The tax factor cuts in more than one direction, and the three markets are linked through the tax code rather than through anything financial.**)*

**3. (Hard — the three theories.)** (a) State each theory's key assumption and verify both numerical examples. (b) Which facts does each explain? (c) Show what the liquidity premium adds that expectations cannot produce.

> [!example]- Solution
> **(a) Perfect substitutes / no substitutes / imperfect substitutes.**
>
> **Expectations theory** — bonds of different maturities are **perfect substitutes**, so expected returns must be equal, so
> $$i_{nt}=\frac{i_t+i^e_{t+1}+\cdots+i^e_{t+(n-1)}}{n}$$
> *(Verified on Mishkin's example — expected short rates 5, 6, 7, 8, 9% give yields **5.000, 5.500, 6.000, 6.500, 7.000%**, all five matching.)*
>
> **Segmented markets** — different maturities are **not substitutes at all**; each market is priced separately.
>
> **Liquidity premium / preferred habitat** — **substitutes but not perfect ones**, so
> $$i_{nt}=\frac{i_t+\cdots+i^e_{t+(n-1)}}{n}+\ell_{nt},\qquad \ell_{nt}>0\text{ and rising in }n$$
> *(Verified with premiums 0, 0.25, 0.5, 0.75, 1.0%: yields **5.000, 5.750, 6.500, 7.250, 8.000%**, all five matching.)*
>
> **(b)**
>
> | | move together | low rates ⇒ upward | usually upward |
> |---|---|---|---|
> | **expectations** | ✓ | ✓ | **✗** |
> | **segmented markets** | **✗** | **✗** | ✓ |
> | **liquidity premium** | ✓ | ✓ | ✓ |
>
> **Expectations gets 1 because a rise in short rates raises expectations of future short rates, and long rates are an average of those.** **It gets 2 because rates are mean-reverting — low rates are expected to rise, high rates to fall.** **It fails 3 because if short rates are as likely to fall as rise, the *typical* curve should be flat.**
>
> **Segmented markets gets 3** (short-bond demand is higher, so long bonds price lower and yield more) **and fails 1 and 2 for the same structural reason: completely separate markets give no channel for one maturity's yield to affect another's.**
>
> **⚠️ The two are opposite assumptions, and each explains exactly what the other cannot — which is what makes the middle case the answer rather than a compromise.**
>
> **(c) An upward-sloping curve from flat expectations.**
>
> *(Computed with expected short rates constant at 7%:)*
>
> | $n$ | expectations | liquidity premium |
> |---|---|---|
> | 1 | 7.00% | 7.00% |
> | 3 | 7.00% | **7.50%** |
> | 5 | 7.00% | **8.00%** |
>
> **Identical expectations, and one curve is flat while the other slopes up.** **That is fact 3, and no choice of expectations lets the first theory produce it** *(other than assuming rates are always expected to rise, which is not credible)*.
>
> **The economics is [[02 - The Meaning of Interest Rates|ch. 02]] exactly: investors prefer short bonds because they bear less interest-rate risk — Table 2 measured a 30-year bond losing 39.75% in a year where a one-year bond returned +10.00%.** **So they must be paid to hold long ones.**
>
> **⚠️ And Mishkin's methodological point is the most transferable thing here:** *"it is important to see how economists modify theories to improve them when they find that the predicted results are inconsistent with the empirical evidence."* **The expectations theory was not discarded for failing fact 3 — it was repaired *at the assumption that produced the failure*** (perfect substitutability), **and the repair preserved everything it already explained.** *(Contrast the temptation to add a free parameter wherever the fit is poor: here the modification is derived from the risk measured in the previous chapter, so it is a mechanism, not a fudge.)*

**4. (Hard — inverting the curve.)** (a) Derive the inversion formula and recover the expectations. (b) What happens if you forget the term premium? (c) Why does this matter beyond the arithmetic?

> [!example]- Solution
> **(a) Difference the definition.**
>
> **From $n\,i_{nt}=\sum_{k=0}^{n-1}i^e_{t+k}+n\ell_{nt}$, subtract the same identity at $n-1$:**
> $$i^e_{t+n-1}=n\left(i_{nt}-\ell_{nt}\right)-(n-1)\left(i_{n-1,t}-\ell_{n-1,t}\right)$$
>
> *(Verified: inverting the curve **5.00, 5.75, 6.50, 7.25, 8.00%** with the premiums **0, 0.25, 0.50, 0.75, 1.00** returns **5, 6, 7, 8, 9%** — exactly the expectations that generated it.)*
>
> **This is the direction that matters in practice.** **Mishkin only runs the theory forwards, but nobody observes expectations and everybody observes the curve.**
>
> **(b) You over-forecast rate rises, and the error grows with horizon.**
>
> | $n$ | 1 | 2 | 3 | 4 | 5 |
> |---|---|---|---|---|---|
> | **naive** | 5.00% | 6.50% | 8.00% | 9.50% | **11.00%** |
> | **truth** | 5.00% | 6.00% | 7.00% | 8.00% | 9.00% |
> | **error** | 0.00 | +0.50 | +1.00 | +1.50 | **+2.00** |
>
> **The true path rises 5→9%. The naive reading says 5→11%** — it attributes the entire term premium to expected tightening.
>
> **⚠️ The bias is systematic and one-directional**, because the premium is always positive and rising. **You will never under-forecast; you will always over-forecast, and by more at longer horizons.**
>
> **(c) Because it is exactly the empirical failure the literature found — and because nothing announces it.**
>
> **Mishkin reports that 1980s researchers found "the spread between long- and short-term interest rates does not always help predict future short-term interest rates, a finding that **may stem from substantial fluctuations in the liquidity (term) premium** for long-term bonds."** **That is this computation, observed in data.**
>
> **⚠️ And note the failure mode: the naive inversion produces a plausible answer with no error signal.** **The sequence 5.00, 6.50, 8.00, 9.50, 11.00 looks like a perfectly ordinary tightening forecast** — nothing about it is malformed, out of range, or internally inconsistent. **This is the vault's standing finding that the expensive errors are the ones that produce a believable wrong answer** *(the fan trap, `NOT IN`, integer overflow, object slicing — and here, a forward curve)*.
>
> **⚠️ It also compounds §6's warning.** **The premium must be *estimated*, and if it fluctuates then even a careful inversion inherits the estimate's error.** **So "the market expects" is always shorthand for "the market expects, given my term-premium model"** — a sentence worth saying out loud before quoting a forward rate.

**5. (The approximation, and the yield curve as a forecast.)** (a) What does Mishkin drop, and what really controls the error? (b) Should it be filed as an erratum? (c) Set out the forecasting chain and its cautions.

> [!example]- Solution
> **(a) He drops the cross terms; the error is controlled by *dispersion*, not level.**
>
> **The exact relation is $(1+i_{2t})^2=(1+i_t)(1+i^e_{t+1})$ — the geometric mean — and the theory uses the arithmetic mean.** **So the error is the arithmetic–geometric gap.**
>
> | $i_t$ | $i^e_{t+1}$ | mean | error |
> |---|---|---|---|
> | 10% | 10% | 10% | **0.0000** |
> | 5% | 15% | 10% | +0.1137 |
> | 0% | 20% | 10% | **+0.4555** |
> | 20% | 20% | 20% | **0.0000** |
> | 40% | 40% | 40% | **0.0000** |
>
> **Three rows share a mean of 10% and have errors of 0.0000, 0.1137, 0.4555 — the error is zero when the rates are equal and grows with their spread.** **Three rows have zero dispersion at levels of 10%, 20% and 40%, and *all three* have exactly zero error.**
>
> **⚠️ Mishkin's justification — "$(i_{2t})^2$ is extremely small" — points at the *level*, and the level is demonstrably not what controls the error.** **The correct statement: the approximation is exact for a flat expected path and degrades with the volatility of expected rates.**
>
> **(b) No.**
>
> **Rule 4 requires ruling out my own extraction, my own arithmetic, an abridged table, and alternative conventions — and beyond that, an erratum is a claim that the *source is wrong*.** **Here the formula is standard, the conclusion is correct, and at any ordinary dispersion the error is hundredths of a percentage point.** **What is imprecise is the *justification*, not the result.**
>
> **⚠️ But the distinction is worth recording, because knowing which quantity controls an error is the difference between a rule of thumb and a rule.** **"It's small because rates are small" gives you no guidance about when it stops being small; "it's small because the path is flat" tells you exactly when to worry — a steeply sloped curve, which is when you most want the formula.**
>
> **This is the third dropped cross term in three chapters** — the Fisher equation (dropping $r\pi^e$), duration (dropping convexity), and this. **In all three the source states the approximation and never computes its error, and in all three the error is negligible in the ordinary case and decisive in the interesting one.**
>
> **(c) Curve → expected rates → business cycle and inflation.**
>
> 1. **The curve reveals expected future short rates** *(this chapter)*.
> 2. **Short rates rise in expansions and fall in recessions** *([[03 - The Behavior of Interest Rates|ch. 03]], Figure 7)* ⇒ **a flat or inverted curve predicts a recession.**
> 3. **Since $i=r+\pi^e$** *([[02 - The Meaning of Interest Rates|ch. 02]])* ⇒ **a steep curve predicts rising inflation.**
>
> **⚠️ And nothing new was needed to build it** — present value from ch. 02, the behaviour of rates from ch. 03. **The best-known leading indicator in macroeconomics falls out of two chapters of definitions.**
>
> **Reading rule: because the premium is positive, a *mildly* upward curve means "no change expected".** **⚠️ So zero slope is not the neutral point — a flat curve is already bearish**, and this is the most common misreading.
>
> **Mishkin's worked case: the steeply inverted curve of 15 January 1981 forecast sharply lower short rates, and three-month bills fell from 16% to 13% by March — −300 bp in about two months.**
>
> **Three cautions.** **(i) The term structure is informative over the next few months and over several years, and *unreliable in between*.** **(ii) The inversion is only as good as the term-premium estimate (§5).** **(iii) The slope is "often viewed as an indicator of the stance of monetary policy" — which is [[03 - The Behavior of Interest Rates|ch. 03]] §7's problem *partly* solved: the *level* of rates does not measure the stance, but the *slope* carries information the level does not.**

## 📝 Summary

- **Risk structure = why same-maturity bonds differ: default risk, liquidity, tax treatment.** **The mechanism is always two-sided** — bad news shifts demand for one bond left *and* its alternative right.
- **⚠️ The observed "risk premium" is really a risk-*and-liquidity* premium**, so inferring default probabilities from spreads overstates them.
- **⚠️ The crisis spread verified, and the table refereed itself** *(Baa +280 bp, Treasury **−80** bp, spread +360 bp; $+280-(-80)=+360$ exactly)*.
- **⚠️ The Treasury yield FELL during the crisis — the flight to quality** *(computed: **22.2%** of the widening came from the safe leg)*. **A spread never says which of its parts moved.**
- **Rating agencies advised on the products they rated.** **But [[Commercial Banking/contents/06 - Hedging with Derivatives|CB ch. 06]] computed that the AAA was wrong even without dishonesty** — senior-tranche loss goes 0.0000% → 1.8044% on a correlation assumption alone. **Two separate failures.**
- **⚠️ The tax break-even is $t^*=20\%$** *(computed)* — **the exemption sorts investors by bracket rather than making munis cheap for everyone**, which is exactly why it was worthless before WWII.
- **Taxable-equivalent yield $=\text{muni}/(1-t)$** — an 8% muni is worth **10.00%** at $t=20\%$ and **16.00%** at 50%. **The same bond is a different asset to different holders.**
- **⚠️ Raising income tax rates lowers municipal borrowing costs** *(computed: 35%→39% widens the muni advantage from +1.50 to +1.90 points)* — **a tax change naming no municipality alters what every city pays to build a school.**
- **Three facts: rates move together; low short rates ⇒ upward curve; the curve almost always slopes up.** **Expectations explains 1 and 2; segmented markets explains 3; liquidity premium explains all three.**
- **Both of Mishkin's numerical curves verified** — expectations **5.00/5.50/6.00/6.50/7.00%**, liquidity premium **5.00/5.75/6.50/7.25/8.00%**.
- **⚠️ The decisive demonstration: with a positive rising premium the curve slopes up even when expected short rates are FLAT** *(computed at a constant 7%)* — **which the expectations theory cannot produce.**
- **⚠️ Inverting the curve while ignoring the premium over-forecasts tightening, systematically, by more at longer horizons** *(computed: true 5→9% reads as 5→11%)* — **and this is precisely the 1980s empirical failure Mishkin reports.**
- **⚠️ Mishkin's arithmetic-average approximation errs with the *dispersion* of expected rates, not their level** *(computed: 0.0000 / 0.1137 / 0.4555 at an identical 10% mean; exactly 0.0000 at 10%, 20% and 40% when the path is flat)*. **His stated justification points at the wrong quantity.** **Third dropped cross term in three chapters.**
- **⚠️ CB ch. 07's forward reference discharged: the bank's 3.75-point yield give-up *is* the term premium it declines to earn** — the price of the option to sell in a hurry, which [[Commercial Banking/contents/08 - Liquidity and Reserves Management|CB ch. 08]]'s run (insolvency at 48.5% withdrawals with zero defaults) explains why it pays. **And segmented markets *is* duration matching, stated as a theory of the curve.**
- **⚠️ Zero slope is not the neutral point** — a mildly upward curve means "no change", so **a flat curve is already bearish.**
- **The yield curve is a free daily forecast of the business cycle and inflation, built entirely from ch. 02 and ch. 03** — **but unreliable at intermediate horizons, and only as good as the term-premium estimate.**

## ⚠️ Important Notes

1. **Risk structure = same maturity; term structure = same everything else.** Never mix the two questions.
2. **⚠️ A credit spread pays for illiquidity as well as default.** Do not read a default probability straight off it.
3. **Every risk-structure effect is two-sided** — both demand curves move, which is why spreads move faster than yields.
4. **⚠️ In a flight to quality the safe yield falls.** A widening spread does not imply the risky yield rose.
5. **Investment grade is Baa/BBB and above.** Below is junk / high-yield / speculative grade.
6. **⚠️ The tax advantage has a break-even bracket.** Below it, tax-exempt bonds are simply a worse deal.
7. **Compare after-tax yields, never headline yields** — an 8% muni beats a 10% Treasury above $t=20\%$.
8. **Treasuries are exempt from state and local tax**, a further reason corporate yields exceed them.
9. **⚠️ Expectations theory fails only fact 3, and fails it for a good reason** — if rates are as likely to fall as rise, the typical curve should be flat.
10. **Segmented markets is the opposite extreme**, and its explanatory pattern is exactly complementary.
11. **⚠️ The term premium is positive and *rising in maturity*.** Both properties are needed — a constant premium would shift the curve, not tilt it.
12. **⚠️ Zero slope is not neutral.** Mildly upward = no expected change; flat = expected fall.
13. **⚠️ Inverting a curve requires a term-premium estimate**, and the naive inversion is biased toward forecasting rate rises.
14. **The bias grows with horizon** — negligible at one year, two full points at five in the worked case.
15. **⚠️ A wrong forward curve looks exactly like a right one.** No error signal.
16. **The arithmetic-average approximation is exact for a flat path** and degrades with dispersion — not with the level.
17. **⚠️ Three dropped cross terms in three chapters** (Fisher, duration, this). **Always ask what the neglected term is proportional to.**
18. **The term structure is informative short-run and long-run, unreliable in between** — Mishkin's own evidence section says so.
19. **⚠️ The yield curve's *slope* carries policy-stance information its *level* does not** — the partial answer to [[03 - The Behavior of Interest Rates|ch. 03]]'s problem.

> [!warning] Gaps in the source material
> **All seven figures are images and are lost, and unlike [[03 - The Behavior of Interest Rates|ch. 03]] the prose does not name their data points** — so the [[03 - The Behavior of Interest Rates|ch. 03]] recovery trick does not apply here. **Checked, per the rule that chapter established.**
>
> - **Figure 1** (long-term bond yields 1919–2017: Baa, Aaa, Treasury, municipal) — **the chapter's opening puzzle and the evidence for every risk-structure claim.** Its qualitative content *is* stated in the prose (corporates always above Treasuries; Baa always above Aaa; **the Depression spike in 1930–33**; the widening after 1970; **munis below Treasuries for most of the past 100 years**) and is reproduced here on that basis. **The series themselves are not recoverable.**
> - **Figures 2 and 3** are shift diagrams with no numbers; their content is the direction of a shift, which the prose states and this note reproduces.
> - **Figure 4** (rates on different maturities, 1950–2017) — **the evidence for fact 1**, and also for the footnote's claim that short rates are more volatile than long ones.
> - **Figure 5** (liquidity-premium versus expectations curve) is schematic; **§4's flat-expectations computation reproduces its content numerically and more precisely.**
> - **Figure 6** (four curve shapes) is schematic; §8's table reproduces it.
> - **⚠️ Figure 7** (yield curves for six dates 1980–2017) and the **"Following the Financial News" curve for 24 July 2017** are the real losses — **actual yield curves with actual numbers.** **Only the qualitative readings survive in the prose** (15 Jan 1981 steeply inverted; 28 Mar 1985 and 24 Jul 2017 steeply upward; 16 May 1980 and 3 Mar 1997 moderately upward; 6 Feb 2006 flat), **together with the one quantitative outcome — three-month bills falling from 16% to 13% between January and March 1981.** **No curve is reconstructed; doing so from the verbal descriptions would be fabrication.**
>
> **⚠️ Table 1 (the rating scales of Moody's, S&P and Fitch) survived extraction complete** — all 21 rows across three agencies with the definitions. **Fourth confirmation of the vault's rule: graphical exhibits are lost; tables set as text survive whole.**
>
> **No erratum found in this chapter.** **Everything Mishkin states numerically reproduces** — the six crisis figures *(with the internal check $+280-(-80)=+360$ passing)*, both after-tax yields, both five-point yield curves, and the 1981 bill-rate move.
>
> **⚠️ One imprecision investigated and deliberately NOT filed** *(§6)*. **Mishkin justifies dropping the cross term with "$(i_{2t})^2$ is extremely small — if $i_{2t}=10\%$, then $(i_{2t})^2=0.01$", which points at the *level* of rates.** *(Computed: the error is exactly **0.0000** at 10%, 20% and 40% when the two rates are equal, and **0.1137 / 0.4555** at an unchanged 10% mean as dispersion grows — **so the level demonstrably does not control it; the dispersion does.**)* **Not filed: the approximation is standard, the conclusion is correct, and the error is hundredths of a point at ordinary dispersions.** **It is the justification that is imprecise, not the result** — and **an erratum is a claim that the source is wrong, which this is not.**
>
> **Additions beyond the source.**
>
> - **⚠️ §3's critical tax rate is the chapter's cleanest addition.** **Mishkin computes one bracket and stops.** Solving $10\%(1-t)=8\%$ gives **$t^*=20\%$**, which converts a worked example into a *rule*, explains **who** holds municipal bonds, and — most usefully — **supplies the reason for his own unexplained historical aside about pre-war tax rates.** *(The taxable-equivalent-yield table and the quantified effect of the 2013 increase are also mine.)*
> - **⚠️ §5's inversion is the chapter's most useful addition and is entirely absent from the source.** **Mishkin runs the theory only forwards.** Deriving $i^e_{t+n-1}=n(i_{nt}-\ell_{nt})-(n-1)(i_{n-1,t}-\ell_{n-1,t})$, verifying it recovers his own expectations exactly, and then running it *without* the premium **quantifies the bias his own evidence section attributes to term-premium fluctuations** — turning a reported empirical puzzle into a computed and explained one.
> - **⚠️ §6's diagnosis of the approximation error is mine** and it corrects the source's reasoning without contradicting its result.
> - **§2's decomposition of the spread widening into its two legs (77.8% / 22.2%) is mine**; Mishkin gives the three changes without noting that a fifth of the move came from the safe asset.
> - **§4's flat-expectations demonstration is mine.** Mishkin asserts that the liquidity premium explains fact 3; **computing the two curves side by side from identical expectations is what makes it visible**, and it substitutes for the lost Figure 5.
> - **⚠️ §7 is written to discharge [[Commercial Banking/contents/07 - The Investment Portfolio|CB ch. 07]]'s forward reference, and the identification of the bank's 3.75-point give-up with the term premium is mine.** **So is the observation that Mishkin's segmented-markets argument is [[Commercial Banking/contents/05 - Interest-Rate Risk - Gap and Duration|CB ch. 05]]'s duration matching stated as a theory of the yield curve.** **Neither source connects them** — Rose & Hudgins uses the curve without deriving it, and Mishkin derives it without ever discussing a bank's portfolio.
> - **§8's forecasting chain is assembled from Mishkin's FYI box plus [[02 - The Meaning of Interest Rates|ch. 02]] and [[03 - The Behavior of Interest Rates|ch. 03]];** **the observation that the *slope* answers what [[03 - The Behavior of Interest Rates|ch. 03]] §7 showed the *level* cannot is mine.**
> - **The "which leg?" framing as the fourth instance of the running theme is my synthesis.**

**Previous:** [[03 - The Behavior of Interest Rates]] · **Next:** [[05 - The Stock Market, Rational Expectations and Efficient Markets]]
