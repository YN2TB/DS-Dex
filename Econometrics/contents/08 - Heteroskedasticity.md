---
subject: Econometrics
chapter: 08
tags: [ds, econometrics, regression, heteroskedasticity, robust-inference, wls]
source: "Wooldridge, *Introductory Econometrics: A Modern Approach*, 7th ed., ch. 8 (pp. 262–293)"
---

# Heteroskedasticity

> [!abstract] What this chapter is for
> **MLR.5 says $\mathrm{Var}(u\mid x_1,\dots,x_k)=\sigma^2$ — the error variance does not depend on the regressors.** It fails whenever the unobserved factors are more variable in some parts of the population than others: savings vary more among the rich, test scores vary more in some schools, and — as [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07]] showed — **a binary dependent variable violates it automatically.**
>
> **The good news, stated up front: heteroskedasticity does not bias anything.** $\hat\beta_j$ stays unbiased and consistent, and $R^2$ still estimates what it always estimated. **What breaks is every standard error, and therefore every $t$, $F$ and LM statistic** — and unlike non-normality, **large samples do not fix it** ([[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]]).
>
> Four responses, in the order the chapter presents them:
>
> | § | Response |
> |---|---|
> | **2** | **Keep OLS, fix the standard errors** — robust inference. The modern default. |
> | **3** | **Test for it** — Breusch–Pagan, White, and White's special case |
> | **4** | **Reweight** — WLS / GLS / feasible GLS, which is *more efficient* if you get the variance right |
> | **5** | The linear probability model, where the variance function is **known exactly** |

---

## 📘 Main Knowledge

### 1. What heteroskedasticity does and does not break

> [!important] The single most important table in this chapter
>
> | Property | Survives heteroskedasticity? | Why |
> |---|---|---|
> | **Unbiasedness** of $\hat\beta_j$ | ✅ | Proved in [[03 - Multiple Regression Analysis - Estimation|ch. 03]] from **MLR.1–4 only** |
> | **Consistency** of $\hat\beta_j$ | ✅ | [[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]] Theorem 5.1 — **MLR.1–4 only** |
> | **Interpretation of $R^2$, $\bar R^2$** | ✅ | see below |
> | $\widehat{\mathrm{Var}}(\hat\beta_j)$, $\mathrm{se}(\hat\beta_j)$ | ❌ **biased** | derived under MLR.5 |
> | $t$ statistics | ❌ **not $t$ distributed** | built on those standard errors |
> | $F$ statistics | ❌ **not $F$ distributed** | " |
> | LM statistic | ❌ **not asymptotically $\chi^2$** | " |
> | **Gauss–Markov (BLUE)** | ❌ | Theorem 3.4 requires MLR.5 |
> | **Asymptotic efficiency** | ❌ | Theorem 5.3 requires MLR.5 |
>
> **And the crucial corollary: none of the ❌ rows is repaired by a large sample.** Non-normality of $u$ washes out asymptotically; **heteroskedasticity does not.**

> [!note] Why $R^2$ is untouched — a question worth being able to answer
> The population $R$-squared is $\rho^2=1-\sigma_u^2/\sigma_y^2$, and **both of those are *unconditional* variances.** Heteroskedasticity is a statement about $\mathrm{Var}(u\mid\mathbf{x})$ — the *conditional* variance — which can vary wildly while $\sigma_u^2$ stays whatever it is.
>
> $\text{SSR}/n$ consistently estimates $\sigma_u^2$ and $\text{SST}/n$ consistently estimates $\sigma_y^2$ **whether or not MLR.5 holds** (and likewise with the df adjustments). **So $R^2$ and $\bar R^2$ remain consistent estimators of $\rho^2$.**
>
> **Contrast with omitting an important variable**, which *does* cause bias. **Heteroskedasticity is an inference problem, not a bias problem** — the same distinction drawn in [[00-Index|the index]] and repeated in [[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]] for serial correlation.

---

### 2. Heteroskedasticity-robust inference after OLS

**The idea:** keep the OLS estimates; replace the standard errors with ones that are valid **whatever** form the heteroskedasticity takes — including none. These are **heteroskedasticity-robust** procedures.

#### The simple regression case, to see where it comes from

With $y_i=\beta_0+\beta_1x_i+u_i$ and $\mathrm{Var}(u_i\mid x_i)=\sigma_i^2$ (note the $i$ subscript — that *is* the heteroskedasticity),

$$\hat\beta_1=\beta_1+\frac{\sum_i(x_i-\bar x)u_i}{\sum_i(x_i-\bar x)^2}
\qquad\Longrightarrow\qquad
\boxed{\;\mathrm{Var}(\hat\beta_1)=\frac{\sum_{i=1}^n(x_i-\bar x)^2\sigma_i^2}{\text{SST}_x^2}\;}$$

**When $\sigma_i^2=\sigma^2$ for all $i$, the numerator becomes $\sigma^2\text{SST}_x$ and this collapses to the familiar $\sigma^2/\text{SST}_x$.** Otherwise it does not, and the usual formula is simply wrong.

**White's (1980) insight:** you cannot estimate each $\sigma_i^2$ (one observation per parameter), **but you do not need to** — you need the whole weighted sum, and $\hat u_i^2$ does the job in aggregate:

$$\widehat{\mathrm{Var}}(\hat\beta_1)=\frac{\sum_{i=1}^n(x_i-\bar x)^2\hat u_i^2}{\text{SST}_x^2}$$

**In the general multiple regression model:**

$$\boxed{\;\widehat{\mathrm{Var}}(\hat\beta_j)=\frac{\sum_{i=1}^n \hat r_{ij}^2\,\hat u_i^2}{\text{SSR}_j^2}\;}$$

where $\hat r_{ij}$ is the $i$th residual from **regressing $x_j$ on all the other regressors**, and $\text{SSR}_j=\sum_i\hat r_{ij}^2$. **The square root is the heteroskedasticity-robust standard error.**

> [!note] Names, and why the degrees-of-freedom correction is arbitrary
> Attributed to **White (1980)** in econometrics; **Eicker (1967)** and **Huber (1967)** in statistics. You will see *White*, *Huber*, *Eicker*, or any hyphenation of them.
>
> Some packages multiply by $n/(n-k-1)$ before taking the square root — the reasoning being that if all $\hat u_i^2$ were identical (the strongest possible sample homoskedasticity), you would recover the usual OLS standard errors. **MacKinnon & White (1985) study several variants. All are asymptotically equivalent and none is uniformly best — use whatever your package computes.**

> [!important] Multicollinearity still hurts, exactly as before
> $\text{SSR}_j=\text{SST}_j(1-R_j^2)$, so the robust standard error has the **same denominator** as the usual one. **Little variation in $x_j$, or $x_j$ nearly collinear with the other regressors, inflates the robust standard error just as it inflates the usual one** ([[03 - Multiple Regression Analysis - Estimation|ch. 03]] §3-4). **Robustness buys validity, not precision.**

#### Example 8.1 — log wage equation, both sets of standard errors

$$\widehat{\log(wage)}=0.321+0.213\,marrmale-0.198\,marrfem-0.110\,singfem+0.0789\,educ+0.0268\,exper-0.00054\,exper^2+0.0291\,tenure-0.00053\,tenure^2$$

| Variable | OLS se $(\;)$ | **Robust se $[\;]$** |
|---|---|---|
| $marrmale$ | $0.055$ | $0.057$ |
| $marrfem$ | $0.058$ | $0.058$ |
| $singfem$ | $0.056$ | $0.057$ |
| $educ$ | $0.0067$ | $\mathbf{0.0074}$ |
| $exper$ | $0.0052$ | $\mathbf{0.0051}$ |
| $exper^2$ | $0.00011$ | $0.00011$ |
| $tenure$ | $0.0068$ | $0.0069$ |
| $tenure^2$ | $0.00023$ | $0.00024$ |

$n=526$, $R^2=0.461$. **Only the standard errors are new — the equation is still estimated by OLS.**

> [!important] Three lessons from this table
> 1. **Nothing changes substantively here.** Every variable significant by the usual $t$ is still significant robustly. The biggest relative change is $educ$ ($0.0067\to0.0074$), and its robust $t$ is still above 10.
> 2. **Robust standard errors can be *smaller*.** $exper$: $0.0052$ usual, $0.0051$ robust. **You cannot predict the direction in advance** — though empirically they are more often larger.
> 3. **None of this tells you whether heteroskedasticity is present.** All we did was report numbers that are valid **either way**.

> [!warning] Then why ever use the usual standard errors?
> **Because under the full CLM assumptions (MLR.1–6) the usual $t$ statistics have *exact* $t$ distributions at any sample size.** The robust versions are justified **only asymptotically**, even when the CLM assumptions hold.
>
> **In small samples, robust $t$ statistics can have distributions far from $t$, which throws off inference.** In large cross-sections, reporting only robust standard errors is defensible and increasingly standard. **Reporting both, as above, lets the reader see whether any conclusion is sensitive to the choice.**

#### Robust $F$ (Wald) statistics

**The usual $F$ is invalid under heteroskedasticity** — including the SSR form. The robust version is called a **heteroskedasticity-robust Wald statistic**; it has no simple hand formula but is a standard package option.

**Example 8.2** (`GPA3`, spring, $n=366$): testing $H_0:\beta_{black}=0,\;\beta_{white}=0$ in a $cumgpa$ equation with $R^2_{ur}=0.4006$ and $R^2_r=0.3983$:

$$F_{\text{usual}}=\frac{(0.4006-0.3983)/2}{(1-0.4006)/359}=\mathbf{0.69}
\qquad
F_{\text{robust}}=\mathbf{0.75},\;\;p=0.474$$

**Both fail to reject, decisively.**

> [!warning] The Chow test of [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07]] §4c is **not valid** under heteroskedasticity
> Equation (7.24) is an SSR-form $F$ statistic, so it breaks — **including in the simple case where the only problem is that the two groups have different error variances**, which is exactly the situation a Chow test is often used to explore.
>
> **The robust Chow test:** build the fully interacted model (group dummy × every regressor) and use a **robust Wald test** — on all the terms for "no difference at all," or on the interactions only (leaving the dummy unrestricted) for "same slopes."
>
> **You cannot do a robust Chow test from two separate group regressions.** The interaction route is the only one.

#### 2a. The heteroskedasticity-robust LM statistic

Not every package computes robust $F$ statistics — but **any** package can produce a robust LM statistic, using only OLS regressions.

Model $y=\beta_0+\beta_1x_1+\cdots+\beta_5x_5+u$, testing $H_0:\beta_4=0,\beta_5=0$.

> [!important] The recipe
> 1. **Restricted residuals.** Estimate the model **without** $x_4,x_5$; keep $\tilde u$.
> 2. **Purge the excluded regressors.** Regress $x_4$ on $x_1,x_2,x_3$ → residuals $\tilde r_1$. Regress $x_5$ on $x_1,x_2,x_3$ → residuals $\tilde r_2$. (In general: **regress each of the $q$ excluded variables on all the included ones.**)
> 3. **Form the products** $\tilde r_1\tilde u$ and $\tilde r_2\tilde u$.
> 4. **Regress the constant 1 on $\tilde r_1\tilde u,\dots,\tilde r_q\tilde u$, with no intercept.** Then
> $$\boxed{\;LM=n-\text{SSR}_1\;\sim\;\chi^2_q\;\text{ under }H_0}$$
> where $\text{SSR}_1$ is the sum of squared residuals from that final regression.
>
> **Step 4 looks bizarre** — you literally create a dependent variable equal to 1 for every observation. **It is a computational device**, doing for the LM test exactly what robust standard errors do for the $t$ test. Rejection rule and $p$-values are as for the usual LM statistic ([[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]] §5-2).

**Example 8.3 — arrests** (`CRIME1`, $n=2{,}725$):

$$\widehat{narr86}=0.561-0.136\,pcnv+0.0178\,avgsen-0.00052\,avgsen^2-0.0394\,ptime86-0.0505\,qemp86-0.00148\,inc86+0.325\,black+0.193\,hispan$$

| Variable | OLS se | Robust se | $t_{\text{usual}}$ | $t_{\text{robust}}$ |
|---|---|---|---|---|
| $avgsen^2$ | $0.00030$ | $\mathbf{0.00021}$ | $-1.73$ | $\mathbf{-2.48}$ |
| $ptime86$ | $0.0087$ | $0.0062$ | $-4.53$ | $-6.35$ |
| $inc86$ | $0.00034$ | $0.00023$ | $-4.35$ | $-6.43$ |
| $black$ | $0.045$ | $\mathbf{0.058}$ | $7.22$ | $5.60$ |

**Here the differences are substantial** — and they go **both ways**: $avgsen^2$ becomes *more* significant under robust inference, $black$ *less*.

**The quadratic in $avgsen$:** turning point $=0.0178/[2(0.00052)]=\mathbf{17.1}$ months. Literally, sentences **increase** arrests below 17 months and deter above — hard to believe.

**Testing $H_0:\beta_{avgsen}=0,\beta_{avgsen^2}=0$:**

| Statistic | Value | $p$ |
|---|---|---|
| Usual LM | $3.54$ | $0.170$ |
| **Robust LM** | $4.00$ | $0.135$ |

**Neither rejects at 15%.** $avgsen$ does not appear to matter. (With $avgsen$ alone, $t_{\text{usual}}=0.658$, $t_{\text{robust}}=0.592$.)

---

### 3. Testing for heteroskedasticity

**Why test at all, if robust inference is available?** Two reasons:
1. **Under MLR.1–6 the usual $t$'s are exact.** Many economists prefer to see them **unless there is evidence of a problem.**
2. **If heteroskedasticity is present, OLS is no longer BLUE** — and §4 shows how to do better if you can model the variance.

**The setup.** Maintain MLR.1–4, so OLS is unbiased and consistent. The null is MLR.5 itself:

$$H_0:\;\mathrm{Var}(u\mid x_1,\dots,x_k)=\sigma^2$$

Since $\mathbb{E}(u\mid\mathbf{x})=0$, we have $\mathrm{Var}(u\mid\mathbf{x})=\mathbb{E}(u^2\mid\mathbf{x})$, so

$$H_0:\;\mathbb{E}(u^2\mid x_1,\dots,x_k)=\mathbb{E}(u^2)=\sigma^2$$

**Testing homoskedasticity = testing whether $u^2$ is related to the regressors.** Assume a linear alternative:

$$u^2=\delta_0+\delta_1x_1+\cdots+\delta_kx_k+v
\qquad\Longrightarrow\qquad
H_0:\;\delta_1=\delta_2=\cdots=\delta_k=0$$

**We cannot observe $u^2$, so use $\hat u^2$.** Using residuals instead of errors **does not affect the large-sample distribution** of the resulting $F$ or LM statistic (the proof is involved).

#### 3a. The Breusch–Pagan test

> [!important] The Breusch–Pagan (BP) test
> 1. Estimate the model by OLS. Save the **squared residuals** $\hat u_i^2$.
> 2. Regress $\hat u^2$ on $x_1,x_2,\dots,x_k$. Keep $R^2_{\hat u^2}$.
> 3. Form either statistic:
> $$F=\frac{R^2_{\hat u^2}/k}{\left(1-R^2_{\hat u^2}\right)/(n-k-1)}\;\sim\;F_{k,\,n-k-1}
> \qquad\text{or}\qquad
> \boxed{\;LM=n\cdot R^2_{\hat u^2}\;\sim\;\chi^2_k\;}$$
> 4. **Small $p$-value ⇒ reject homoskedasticity.**
>
> **The LM version is what "Breusch–Pagan test" normally means.** Breusch & Pagan (1979) originally assumed **normal** errors; **Koenker (1981)** proposed the $nR^2$ form above, which is preferred for its wider applicability.
>
> **Note the recurring pattern:** $nR^2$ on a residual-based auxiliary regression — the same shape as the LM test of [[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]] and, later, Breusch–Godfrey and Engle's ARCH test in [[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]].

#### Example 8.4 — housing prices, levels vs logs (`HPRICE1`, $n=88$)

**Levels:**
$$\widehat{price}=-21.77+0.00207\,lotsize+0.123\,sqrft+13.85\,bdrms,\qquad R^2=0.672$$
$$\qquad\quad(29.48)\;\;(0.00064)\qquad\;(0.013)\qquad\;(9.01)$$

BP auxiliary regression: $R^2_{\hat u^2}=\mathbf{0.1601}$, $k=3$.
$$F=\frac{0.1601/3}{(1-0.1601)/84}=\mathbf{5.34}\;(p=0.002),\qquad LM=88(0.1601)=\mathbf{14.09}\;(p=0.0028)$$

**Strong evidence of heteroskedasticity. The standard errors above are not reliable.**

**Logs:**
$$\widehat{\log(price)}=-1.30+0.168\log(lotsize)+0.700\log(sqrft)+0.037\,bdrms,\qquad R^2=0.643$$
$$\qquad\qquad(0.65)\;\;(0.038)\qquad\qquad(0.093)\qquad\quad(0.028)$$

$R^2_{\hat u^2}=\mathbf{0.0480}$: $F=\mathbf{1.41}$ ($p=0.245$), $LM=\mathbf{4.22}$ ($p=0.239$). **Fail to reject.**

> [!tip] Taking logs often kills the heteroskedasticity
> Exactly as [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §2a promised: strictly positive variables tend to have **skewed, heteroskedastic** conditional distributions, and the log mitigates both. **This has been noticed in a great many empirical applications** — and here it turns a decisive rejection into a comfortable non-rejection.

> [!note] Two easy modifications
> - **Suspect only some regressors drive the variance?** Regress $\hat u^2$ on just those, and use $F$ or LM with **their** count as the df. **The number of regressors in the original equation is irrelevant** — only the count in the auxiliary regression matters.
> - **Regress $\hat u^2$ on a single variable?** Then the test **is** the ordinary $t$ statistic on that variable.

#### 3b. The White test

**The motivation is precise, not arbitrary.** [[05 - Multiple Regression Analysis - OLS Asymptotics|Chapter 05]] showed that the usual OLS statistics are asymptotically valid under MLR.1–5 — but MLR.5 can be weakened to: **$u^2$ is uncorrelated with every $x_j$, every $x_j^2$, and every cross product $x_jx_h$.** So White's test checks **exactly the condition whose failure invalidates the usual statistics.**

With $k=3$ regressors:
$$\hat u^2=\delta_0+\delta_1x_1+\delta_2x_2+\delta_3x_3+\delta_4x_1^2+\delta_5x_2^2+\delta_6x_3^2+\delta_7x_1x_2+\delta_8x_1x_3+\delta_9x_2x_3+\text{error}$$

**Nine restrictions** ($H_0$: all $\delta_j=0$ except the intercept), tested with $F$ or $LM=nR^2_{\hat u^2}$.

> [!warning] The White test burns degrees of freedom fast
> | Original $k$ | White regressors |
> |---|---|
> | 3 | **9** |
> | 6 | **27** |
> | 10 | **65** |
>
> In general $2k+\binom{k}{2}$. **This is the pure White test's real weakness** — with even a moderate number of regressors the test has little power left, and you may not have the observations.

#### 3c. White's special case — the version to actually use

**Keep the spirit, spend two degrees of freedom.** The fitted values $\hat y_i$ are linear in the regressors, so $\hat y$ and $\hat y^2$ between them capture a particular combination of **all** the squares and cross products.

> [!important] The special case of the White test
> 1. Estimate the model by OLS. Compute $\hat u^2$ and $\hat y$, $\hat y^2$.
> 2. Regress $$\hat u^2=\delta_0+\delta_1\hat y+\delta_2\hat y^2+\text{error}$$ Keep $R^2_{\hat u^2}$.
> 3. Test $H_0:\delta_1=0,\delta_2=0$ using $F_{2,\,n-3}$ or $\chi^2_2$.
>
> **Always two restrictions, no matter how many regressors the original model has.**
>
> **It must be $\hat y$, not $y$.** $\hat y$ is a function of the regressors (and estimated parameters); **using $y$ does not produce a valid test** — $y$ contains $u$, and you would be regressing $\hat u^2$ on something containing $\hat u$.
>
> **When is this the right choice?** When you think the variance changes with **the level of $\mathbb{E}(y\mid\mathbf{x})$** — which is very often the case. It is a **special case of the full White test**, imposing restrictions on the $\delta_j$ in (8.19).

**Example 8.5** — applied to the log housing equation: $R^2_{\hat u^2}=0.0392$, so
$$LM=88(0.0392)=\mathbf{3.45},\qquad p=\mathbf{0.178}$$
**Stronger evidence than BP gave ($p=0.239$), but still no rejection even at 15%.**

> [!warning] A rejection may mean the **functional form** is wrong, not the variance
> All these tests maintain **MLR.1–4**. If MLR.4 fails — in particular if $\mathbb{E}(y\mid\mathbf{x})$ is **misspecified** — a heteroskedasticity test **can reject even when $\mathrm{Var}(y\mid\mathbf{x})$ is perfectly constant.** Omitting a quadratic term, or using levels where logs belong, will do it.
>
> This has led some economists to treat these as **general misspecification tests**. Wooldridge's advice is sharper:
>
> > **Test functional form first** (RESET and the other tools of [[09 - More on Specification and Data Issues|ch. 09]]) — **functional form misspecification is more important than heteroskedasticity.** Once you are satisfied with the functional form, *then* test for heteroskedasticity.
>
> **Example 8.4 is a live illustration:** the levels model rejects at $p=0.002$; taking logs — a **functional form** change — removes the rejection entirely. Was there ever heteroskedasticity, or just the wrong functional form? **The tests cannot tell you.**

---

### 4. Weighted least squares

**The pre-robust response to heteroskedasticity, and still the efficient one *if* you model the variance correctly.**

#### 4a. Variance known up to a multiplicative constant

Assume
$$\boxed{\;\mathrm{Var}(u\mid\mathbf{x})=\sigma^2h(\mathbf{x}),\qquad h(\mathbf{x})>0\;}$$

with $h(\cdot)$ **known** and $\sigma^2$ unknown. Write $h_i=h(\mathbf{x}_i)$.

**Canonical example — a savings function:**
$$sav_i=\beta_0+\beta_1 inc_i+u_i,\qquad \mathrm{Var}(u_i\mid inc_i)=\sigma^2 inc_i$$
so $h(inc)=inc$ and the conditional standard deviation is $\sigma\sqrt{inc}$. **Variability in savings rises with income** — economically sensible, and automatically positive since $inc>0$.

**The transformation.** Divide the whole equation by $\sqrt{h_i}$:

$$\frac{y_i}{\sqrt{h_i}}=\beta_0\frac{1}{\sqrt{h_i}}+\beta_1\frac{x_{i1}}{\sqrt{h_i}}+\cdots+\beta_k\frac{x_{ik}}{\sqrt{h_i}}+\frac{u_i}{\sqrt{h_i}}$$

$$y_i^*=\beta_0x_{i0}^*+\beta_1x_{i1}^*+\cdots+\beta_kx_{ik}^*+u_i^*,\qquad x_{i0}^*=\frac{1}{\sqrt{h_i}}$$

**Check the new error is homoskedastic:**
$$\mathbb{E}\left[\left(\frac{u_i}{\sqrt{h_i}}\right)^{\!2}\right]=\frac{\mathbb{E}(u_i^2)}{h_i}=\frac{\sigma^2h_i}{h_i}=\sigma^2\quad✓$$
and $\mathbb{E}(u_i/\sqrt{h_i}\mid\mathbf{x}_i)=0$ since $h_i$ is a function of $\mathbf{x}_i$. ✓

> [!important] The payoff
> **If the original model satisfies MLR.1–4, the transformed model satisfies MLR.1–5** — all five Gauss–Markov assumptions. If $u$ is normal, $u^*$ is normal too, so the transformed model satisfies **MLR.1–6**.
>
> **Therefore OLS on the transformed equation is BLUE**, exact $t$ and $F$ distributions are recovered, and $\text{SSR}^*/(n-k-1)$ is unbiased for $\sigma^2$.
>
> These are **generalized least squares (GLS)** estimators. Applied to heteroskedasticity they are called **weighted least squares (WLS)**.

**Savings example transformed:**
$$\frac{sav_i}{\sqrt{inc_i}}=\beta_0\frac{1}{\sqrt{inc_i}}+\beta_1\sqrt{inc_i}+u_i^*$$
using $inc_i/\sqrt{inc_i}=\sqrt{inc_i}$.

> [!warning] Interpret the parameters in the **original** equation, always
> $\beta_1$ is still the marginal propensity to save out of income. **The transformed regressors ($1/\sqrt{inc}$, $\sqrt{inc}$) have no useful interpretation of their own** — they are a computational device.

#### Why "weighted"

WLS minimizes the **weighted** sum of squared residuals:

$$\boxed{\;\min_{\beta}\;\sum_{i=1}^n \frac{\left(y_i-\beta_0-\beta_1x_{i1}-\cdots-\beta_kx_{ik}\right)^2}{h_i}\;}$$

Bring $1/\sqrt{h_i}$ inside the square and this **is** the ordinary SSR in the transformed variables — which is why WLS and OLS-on-transformed-data give identical estimates.

> [!warning] $1/h_i$ vs $1/\sqrt{h_i}$ — the detail everyone gets wrong
> - **The squared residuals are weighted by $1/h_i$.**
> - **The transformed variables are divided by $\sqrt{h_i}$.**
>
> Packages ask for the **weight**, i.e. $1/h_i$ — proportional to the **inverse of the variance**.

**The logic:** observations with **higher error variance get less weight**, because they carry less information. **OLS is the special case that weights every observation equally** — optimal only when every observation has the same error variance.

> [!tip] Use your package's WLS option, not hand transformation
> Hand-building starred variables is tedious and error-prone. Specifying weights **forces you to interpret the results in the original model**, and the package prints the equation in its original form. Estimates and standard errors differ from OLS; **interpretation does not.**

> [!warning] The WLS $R^2$ is nearly useless as a fit measure — but fine for $F$ tests
> Packages compute it from the **weighted** SSR and a weighted SST, so it measures explained variation in **$y_i^*$, not $y_i$.**
>
> **It is still valid for $F$ statistics on exclusion restrictions**, because the SST terms cancel — **provided the same weights are used for the restricted and unrestricted models.** Estimate the unrestricted model first, obtain the weights, then reuse them.
>
> **The $R^2$ from hand-running OLS on the transformed equation is worse still**, because you must exclude an intercept and the package then computes an **uncentred** SST — the same trap as [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07]] §3. **It tempts you to think the model fits far better than it does.**

#### Example 8.6 — net financial wealth (`401KSUBS`, singles, $n=2{,}017$)

Assuming $\mathrm{Var}(u\mid inc)=\sigma^2 inc$:

| | (1) OLS | (2) WLS | (3) OLS | (4) WLS |
|---|---|---|---|---|
| $inc$ | $0.821$ $(0.104)$ | $0.787$ $(0.063)$ | $0.771$ $(0.100)$ | $0.740$ $(0.064)$ |
| $(age-25)^2$ | — | — | $0.0251$ $(0.0043)$ | $0.0175$ $(0.0019)$ |
| $male$ | — | — | $2.48$ $(2.06)$ | $1.84$ $(1.56)$ |
| $e401k$ | — | — | $\mathbf{6.89}$ $(2.29)$ | $\mathbf{5.19}$ $(1.70)$ |
| intercept | $-10.57$ $(2.53)$ | $-9.58$ $(1.65)$ | $-20.98$ $(3.50)$ | $-16.70$ $(1.96)$ |
| $R^2$ | $0.0827$ | $0.0709$ | $0.1279$ | $0.1115$ |

*(OLS standard errors here are **robust**; WLS standard errors assume the variance model is right.)*

- **Another dollar of income raises wealth by about 82¢ (OLS) or 79¢ (WLS)** in column (1)–(2). Close, as they should be.
- **WLS is markedly more precise:** the $inc$ standard error falls from $0.104$ to $0.063$, about **40% smaller** — *provided* $\mathrm{Var}(nettfa\mid inc)=\sigma^2 inc$ is correct.
- **401(k) eligibility raises wealth by \$6,890 (OLS) or \$5,190 (WLS)** — a substantial gap.
- **Joint significance of $(age-25)^2$, $male$, $e401k$ under WLS:** using the $R^2$s,
$$F=\frac{(0.1115-0.0709)/3}{(1-0.1115)/2012}=\mathbf{30.6},$$
with a $p$-value of zero to many decimal places.

> [!warning] A large OLS–WLS gap is a warning sign, not a curiosity
> The $e401k$ estimate drops from $6.89$ to $5.19$. **Wooldridge reads this as evidence of functional-form misspecification in the mean equation** (a suggested fix: interact $e401k$ with $inc$).
>
> **Why a gap is diagnostic.** For WLS to be consistent, it is **not enough** that $u$ be uncorrelated with each $x_j$ — you need the full MLR.4, $\mathbb{E}(u\mid\mathbf{x})=0$. **If $\mathbb{E}(y\mid\mathbf{x})\ne\beta_0+\beta_1x_1+\cdots+\beta_kx_k$, then OLS and WLS have different probability limits** and will systematically disagree.
>
> **How worried to be:**
> - Signs all agree, biggest changes on already-insignificant variables → **sampling error, fine.**
> - **OLS and WLS both significant with opposite signs**, or a practically large gap → **be suspicious: suspect MLR.4.**
>
> The **Hausman (1978) test** formalizes the comparison. Beyond this text — but **eyeballing usually suffices.**

#### When the weights are not arbitrary: grouped data

> [!important] The one case where the weights come from the model itself
> Individual-level model, employee $e$ at firm $i$:
> $$contrib_{i,e}=\beta_0+\beta_1 earns_{i,e}+\beta_2 age_{i,e}+\beta_3 mrate_i+u_{i,e}$$
>
> Suppose you observe **only firm averages**. Averaging over the $m_i$ employees at firm $i$:
> $$\overline{contrib}_i=\beta_0+\beta_1\overline{earns}_i+\beta_2\overline{age}_i+\beta_3 mrate_i+\bar u_i$$
>
> **If the individual-level model is homoskedastic ($\mathrm{Var}(u_{i,e})=\sigma^2$) and errors are uncorrelated within firms**, then
> $$\mathrm{Var}(\bar u_i)=\frac{\sigma^2}{m_i}\quad\Longrightarrow\quad h_i=\frac{1}{m_i}\quad\Longrightarrow\quad \textbf{weight}=\frac{1}{h_i}=m_i$$
>
> **Weight each firm by its number of employees.** Bigger firms give more precisely measured averages and get more weight. **This recovers efficient estimates of the individual-level parameters from group averages alone.**
>
> **Identically for per-capita data** at city/county/state/country level: **weight by population.** A city-level beer-demand equation $beerpc=\beta_0+\beta_1 perc21+\beta_2 avgeduc+\beta_3 incpc+\beta_4 price+u$ should be estimated with **city population as the weight.**

> [!warning] Two ways group weighting fails
> 1. **If the *individual-level* equation is heteroskedastic**, the correct weight is not $m_i$ — it depends on the individual-level variance function.
> 2. **If errors are correlated within a group**, then $\mathrm{Var}(\bar u_i)\ne\sigma^2/m_i$ at all. (Cluster correlation — very common with geographic groups.)
>
> **This uncertainty is why more and more researchers simply use OLS with robust standard errors on per-capita data.** The hedged compromise: **weight by group size for efficiency, but report heteroskedasticity-robust statistics** — efficient if the individual model is Gauss–Markov, still valid if it is not.

#### 4b. Feasible GLS — when $h(\mathbf{x})$ must be estimated

**In practice you almost never know $h(\mathbf{x})$.** Model it and estimate the parameters. Wooldridge's flexible default:

$$\boxed{\;\mathrm{Var}(u\mid\mathbf{x})=\sigma^2\exp\left(\delta_0+\delta_1x_1+\cdots+\delta_kx_k\right)\;}$$

> [!important] Why exponential, when Breusch–Pagan used a *linear* form?
> **Because WLS needs positive estimated variances, and a linear model does not guarantee positive fitted values.**
>
> A linear variance model is fine for **testing** — you only need to detect a relationship. It is dangerous for **correcting** — one negative $\hat h_i$ and the whole procedure fails. **$\exp(\cdot)$ is positive by construction.**

**Linearizing.** Write $u^2=\sigma^2\exp(\delta_0+\mathbf{x}\boldsymbol\delta)v$ with $\mathbb{E}(v\mid\mathbf{x})=1$. If $v$ is **independent** of $\mathbf{x}$, taking logs:

$$\log(u^2)=\alpha_0+\delta_1x_1+\cdots+\delta_kx_k+e$$

with $\mathbb{E}(e)=0$ and $e$ independent of $\mathbf{x}$. **This satisfies the Gauss–Markov assumptions, so OLS gives unbiased $\hat\delta_j$.** (The intercept differs from $\delta_0$; it doesn't matter.)

> [!important] The FGLS procedure
> 1. **OLS** on $y=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+u$; save residuals $\hat u$.
> 2. Compute $\log(\hat u^2)$ — **square first, then log.**
> 3. Regress $\log(\hat u^2)$ on $x_1,\dots,x_k$; save the **fitted values** $\hat g_i$.
> 4. $\hat h_i=\exp(\hat g_i)$.
> 5. **WLS with weights $1/\hat h_i$.** (Equivalently: divide every variable — **including the intercept term** — by $\sqrt{\hat h_i}$ and run OLS.)
>
> **Variant:** replace step 3 with a regression of $\log(\hat u^2)$ on $\hat y$ and $\hat y^2$ — the same fitted-value economy as White's special case.

> [!note] What FGLS costs and what it buys
> Because $h_i$ is **estimated from the same data**, the FGLS estimator is **no longer unbiased**, and therefore **not BLUE**.
>
> **But it is consistent and asymptotically more efficient than OLS.** For large samples, **FGLS is an attractive alternative to OLS whenever heteroskedasticity is inflating the OLS standard errors.**
>
> **And FGLS still estimates the parameters of the *original* population model.** $\hat\beta_j^{FGLS}$ measures exactly what $\hat\beta_j^{OLS}$ measures.

> [!warning] Do not use this regression as a test — the Park test problem
> Park (1966) proposed testing heteroskedasticity with an $F$ or LM test on regression (8.32). **Do not.** Two defects, both absent from BP and White:
> 1. **The null must be stronger than homoskedasticity** — effectively, $u$ **independent** of $\mathbf{x}$.
> 2. **Substituting $\hat u$ for $u$ makes the $F$ statistic deviate from the $F$ distribution even in large samples.**
>
> **Regression (8.32) is fine for *building weights*** — there you only need **consistent** $\hat\delta_j$, which it delivers. **It is not fine for testing.**

#### Example 8.7 — demand for cigarettes (`SMOKE`, $n=807$)

**OLS:**
$$\widehat{cigs}=-3.64+0.880\log(income)-0.751\log(cigpric)-0.501\,educ+0.771\,age-0.0090\,age^2-2.83\,restaurn$$
$$\qquad\;\;(24.08)\;(0.728)\qquad\quad(5.773)\qquad\qquad(0.167)\qquad(0.160)\quad(0.0017)\qquad\;(1.11)$$
$$R^2=0.0526$$

- **Neither income nor price is significant.** A 10% income rise predicts $(0.880/100)(10)=\mathbf{0.088}$ more cigarettes/day — **under a tenth of a cigarette.**
- **Each year of education cuts about half a cigarette/day**, significant.
- **Smoking peaks at $age=0.771/[2(0.009)]=\mathbf{42.8}$** then declines; both quadratic terms significant.
- **Restaurant smoking restrictions cut nearly three cigarettes/day.**
- (13 of 807 fitted values are negative — **1.6%**, not a major concern. The linear model is imperfect for a variable that is zero for most people.)

**Breusch–Pagan:** $R^2_{\hat u^2}=0.040$.

> [!warning] "$R^2=0.040$ looks tiny, so there's no heteroskedasticity" — wrong
> $$LM=807(0.040)=\mathbf{32.28}\;\sim\;\chi^2_6,\qquad p<\mathbf{0.000015}$$
> **Overwhelming rejection.** With a large $n$, a seemingly negligible $R^2_{\hat u^2}$ produces a decisive statistic. **Always compute $F$ or LM — never eyeball $R^2_{\hat u^2}$.**

**FGLS/WLS estimates:**
$$\widehat{cigs}=5.64+1.30\log(income)-2.94\log(cigpric)-0.463\,educ+0.482\,age-0.0056\,age^2-3.46\,restaurn$$
$$\qquad\;(17.80)\;(0.44)\qquad\quad(4.46)\qquad\qquad(0.120)\qquad(0.097)\quad(0.0009)\qquad\;(0.80)$$
$$R^2=0.1134$$

- **The income effect is now significant** ($t=1.30/0.44=2.95$) and **larger**.
- **The price effect is much bigger** ($-0.751\to-2.94$) but **still insignificant** — because `cigpric` **varies only across states**, so $\log(cigpric)$ has far less variation than $\log(income)$, $educ$ or $age$. **A precision problem, not a heteroskedasticity problem.**
- **The story is unchanged:** smoking falls with schooling, is quadratic in age, and falls with restaurant restrictions.

#### 4c. What if the variance function is wrong?

> [!important] The three consequences, in order of importance
>
> **1. WLS stays consistent. ✅**
> If $\mathbb{E}(u\mid\mathbf{x})=0$, then **any** function of $\mathbf{x}$ is uncorrelated with $u$ — so the weighted error $u/\sqrt{h(\mathbf{x})}$ is uncorrelated with the weighted regressors $x_j/\sqrt{h(\mathbf{x})}$, for **any** positive $h$. (With estimated $h(\mathbf{x},\hat\delta)$, unbiasedness is lost but consistency survives.)
>
> **This is precisely why a large OLS–WLS gap indicts MLR.4:** under MLR.4 both are consistent for the same $\beta_j$, so they cannot systematically disagree.
>
> **2. The usual WLS standard errors become invalid — even in large samples. ❌**
> Column (4) of Table 8.1 assumes $\mathrm{Var}(nettfa\mid inc,age,male,e401k)=\sigma^2 inc$ — not just that the variance depends only on income, but that it is **linear** in income. If that is wrong, every standard error and test statistic built on it is wrong.
>
> **The fix is easy and you should always use it.** The transformed equation
> $$\frac{y_i}{\sqrt{h_i}}=\beta_0\frac{1}{\sqrt{h_i}}+\beta_1\frac{x_{i1}}{\sqrt{h_i}}+\cdots+\frac{u_i}{\sqrt{h_i}}$$
> has a heteroskedastic error whenever $\mathrm{Var}(u_i\mid\mathbf{x}_i)\ne\sigma^2h_i$ — **so apply ordinary heteroskedasticity-robust standard errors to it.** These are **fully robust WLS standard errors**: they allow the variance function to be arbitrarily misspecified.
>
> **3. WLS is no longer guaranteed to beat OLS in efficiency. ⚠️**
> If $\mathrm{Var}(y\mid\mathbf{x})$ is neither constant nor $\sigma^2h(\mathbf{x})$, **OLS and WLS cannot be ranked.** This modern criticism is theoretically correct — and practically overstated.

**Table 8.2 — WLS `nettfa` estimates, both standard errors:**

| Variable | WLS estimate | Non-robust se | **Robust se** |
|---|---|---|---|
| $inc$ | $0.740$ | $0.064$ | $\mathbf{0.075}$ |
| $(age-25)^2$ | $0.0175$ | $0.0019$ | $\mathbf{0.0026}$ |
| $male$ | $1.84$ | $1.56$ | $\mathbf{1.31}$ |
| $e401k$ | $5.19$ | $1.70$ | $\mathbf{1.57}$ |
| intercept | $-16.70$ | $1.96$ | $2.24$ |

**Robust standard errors are larger for $inc$ and $age$ (enough to stretch the CIs), and *smaller* for $male$ and $e401k$** — the same unpredictability seen with robust OLS standard errors.

> [!tip] The practical verdict, and it favours WLS
> **Compare robust to robust — that puts the two estimators on equal footing** (neither assumes homoskedasticity nor the $\sigma^2 inc$ form):
>
> | Coefficient | Robust se, **OLS** | Robust se, **WLS** | Reduction |
> |---|---|---|---|
> | $inc$ | $0.100$ | $\mathbf{0.075}$ | **25%** |
> | $(age-25)^2$ | $0.0043$ | $\mathbf{0.0026}$ | **40%** |
>
> **Even with a variance model that is almost certainly wrong, WLS is substantially more precise than OLS.**
>
> > **In cases of strong heteroskedasticity, it is often better to use a *wrong* form of heteroskedasticity and apply WLS than to ignore heteroskedasticity altogether and use OLS.**
>
> **The recommended practice: WLS for the estimates, fully robust standard errors for the inference.** Best of both.

#### 4d. Prediction under heteroskedasticity

**Point predictions are unaffected** except through the estimates: $\hat y^0=\hat\beta_0+\mathbf{x}^0\hat{\boldsymbol\beta}$. **Once you know $\mathbb{E}(y\mid\mathbf{x})$, you predict with it; the structure of $\mathrm{Var}(y\mid\mathbf{x})$ plays no direct role.** (Naturally, use WLS to get the $\hat\beta_j$.)

**Prediction *intervals* do depend on it directly.** With $\mathrm{Var}(y\mid\mathbf{x})=\sigma^2h(\mathbf{x})$,

$$\boxed{\;\mathrm{se}(\hat e^0)=\left\{\left[\mathrm{se}(\hat y^0)\right]^2+\hat\sigma^2h(\mathbf{x}^0)\right\}^{1/2},\qquad \text{95\% PI}=\hat y^0\pm t_{.025}\,\mathrm{se}(\hat e^0)\;}$$

**Compare [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §4b: the only change is $\hat\sigma^2\to\hat\sigma^2h(\mathbf{x}^0)$** — the error variance is now evaluated **at the point you are predicting.** Get $\mathrm{se}(\hat y^0)$ by the same recentring trick, estimated by WLS.

> [!note] Exactness, and a shortcut
> The interval is **exact only if $h$ is known**. With an estimated variance function, accounting for the error in both $\hat\beta_j$ and $\hat\delta_j$ is very difficult; in practice **replace $h(\mathbf{x}^0)$ with $\hat h(\mathbf{x}^0)$ and accept the approximation.**
>
> **And if you are going to ignore parameter estimation error anyway, drop $\mathrm{se}(\hat y^0)$ entirely** — it converges to zero at rate $1/\sqrt n$ while $\hat\sigma\sqrt{h(\mathbf{x}^0)}$ stays roughly constant. **Exactly the [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] finding that the error variance swamps the estimation error.**

**With $\log(y)$ as the dependent variable** and exponential, normal heteroskedasticity $u\mid\mathbf{x}\sim\mathrm{Normal}\left[0,\exp(\delta_0+\mathbf{x}\boldsymbol\delta)\right]$:

$$\mathbb{E}(y\mid\mathbf{x})=\exp\left(\beta_0+\mathbf{x}\boldsymbol\beta+\tfrac{1}{2}\exp(\delta_0+\mathbf{x}\boldsymbol\delta)\right)$$

**The [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §4d factor $\exp(\hat\sigma^2/2)$ becomes observation-specific:**

$$\hat y_i=\exp\left(\widehat{\log y_i}+\hat\sigma^2\hat h_i/2\right)$$

Take the squared correlation of $y_i$ with $\hat y_i$ as the goodness-of-fit measure, as before. An approximate 95% prediction interval is
$$\exp\left(\pm1.96\,\hat\sigma\sqrt{\hat h(\mathbf{x}^0)}\right)\exp\left(\hat\beta_0+\mathbf{x}^0\hat{\boldsymbol\beta}\right)$$

---

### 5. The linear probability model revisited

[[07 - Multiple Regression Analysis with Qualitative Information|Chapter 07]] §5 showed that a binary $y$ **must** be heteroskedastic (unless every slope is zero):

$$\mathrm{Var}(y\mid\mathbf{x})=p(\mathbf{x})\left[1-p(\mathbf{x})\right],\qquad p(\mathbf{x})=\beta_0+\beta_1x_1+\cdots+\beta_kx_k$$

**Here the variance function is not a guess — it is known exactly, up to the $\beta_j$.**

#### Option 1 — OLS with robust standard errors

**Simplest, and usually adequate.**

**Example 8.8** (`MROZ`, $n=753$):

| Variable | OLS se | Robust se |
|---|---|---|
| $nwifeinc$ | $0.0014$ | $0.0015$ |
| $educ$ | $0.007$ | $0.007$ |
| $exper$ | $0.006$ | $0.006$ |
| $exper^2$ | $0.00018$ | $0.00019$ |
| $age$ | $0.002$ | $0.002$ |
| $kidslt6$ | $0.034$ | $0.032$ |
| $kidsge6$ | $0.0132$ | $0.0135$ |

> [!important] Heteroskedasticity here is a theoretical certainty and a practical non-event
> **Several robust and usual standard errors are identical to the reported precision, and every difference is practically negligible.** No conclusion changes.
>
> **This is the general lesson of the chapter.** *"It often turns out that the usual OLS standard errors and test statistics are similar to their heteroskedasticity-robust counterparts. Furthermore, it requires a minimal effort to compute both."* **Compute both. Report both when they differ.**

#### Option 2 — WLS with the known variance function

Estimate $h_i$ by plugging OLS fitted values into the known form:

$$\boxed{\;\hat h_i=\hat y_i\left(1-\hat y_i\right)\;}$$

then apply FGLS with weights $1/\hat h_i$.

> [!warning] The hitch that kills it in practice
> **WLS requires every weight to be strictly positive.** But
> $$\hat y_i<0 \;\;\text{or}\;\; \hat y_i>1 \quad\Longrightarrow\quad \hat h_i=\hat y_i(1-\hat y_i)<0$$
> and $1/\sqrt{\hat h_i}$ is **undefined**. The method **fails outright** for any such observation.
>
> **And out-of-range fitted values are the LPM's signature defect** — 33 of 753 (**4.4%**) in `MROZ`.
>
> | $\hat y_i$ | $\hat h_i$ | Weight $1/\hat h_i$ |
> |---|---|---|
> | $0.5$ | $0.250$ | $4.00$ |
> | $0.3$ | $0.210$ | $4.76$ |
> | $0.1$ or $0.9$ | $0.090$ | $11.11$ |
> | $0.05$ | $0.0475$ | $21.05$ |
> | $-0.10$ | $-0.110$ | **undefined** |
> | $1.20$ | $-0.240$ | **undefined** |
>
> **Note the shape:** the closer a predicted probability is to 0 or 1, the *smaller* its variance and the *more* weight it earns — sensible, and precisely why the method breaks just past the boundary.
>
> **The usual patches** are to drop the offending observations, or to truncate $\hat y_i$ to something like $[0.01,0.99]$ — both **ad hoc**, and both alter the sample or the estimates in ways that are hard to justify. **Which is why option 1 dominates in practice.**

---

## ✏️ Exercises

### Exercise 1 — What heteroskedasticity does and does not break

A researcher estimates a wage equation, tests for heteroskedasticity, and rejects homoskedasticity decisively.

**(a)** She writes: *"Since MLR.5 fails, my coefficient estimates are biased and I must re-estimate."* Correct her, naming the assumptions each property actually requires.
**(b)** *"But my sample has 12,000 observations, so asymptotics will take care of it."* Evaluate.
**(c)** She reports $R^2=0.34$ and asks whether it is still meaningful. Answer, and explain why.
**(d)** List every statistic in her output that is **not** trustworthy.
**(e)** Her colleague says the fix is to switch from OLS to WLS. Is that necessary? What is the minimal fix, and when would WLS still be worth the effort?

> [!example]- Solution
> **(a) She is wrong, and the correction is precise.**
>
> **Unbiasedness of $\hat\beta_j$ was proved from MLR.1–4 alone** ([[03 - Multiple Regression Analysis - Estimation|ch. 03]], Theorem 3.1). **Consistency likewise requires only MLR.1–4** ([[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]], Theorem 5.1). **MLR.5 appears in neither proof.**
>
> **Heteroskedasticity is an inference problem, not a bias problem.** Contrast **omitting a relevant correlated variable**, which violates MLR.4 and *does* cause bias and inconsistency.
>
> **(b) Wrong, and this is the single most important thing to get right about heteroskedasticity.**
>
> **Compare the two ways the CLM assumptions can fail:**
>
> | Failure | Fixed by large $n$? |
> |---|---|
> | **Non-normality (MLR.6)** | ✅ — Theorem 5.2 gives asymptotic normality without it |
> | **Heteroskedasticity (MLR.5)** | ❌ — **never** |
>
> **Why:** Theorem 5.2 derives the asymptotic distribution of $\hat\beta_j$ **assuming MLR.5.** The variance estimator $\hat\sigma^2/[\text{SST}_j(1-R_j^2)]$ converges to the wrong thing when the true variance is $\sum\hat r_{ij}^2\sigma_i^2/\text{SSR}_j^2$. **It converges — reliably, precisely — to a number that is not $\mathrm{Var}(\hat\beta_j)$.** More data makes it converge *faster* to the *wrong* answer.
>
> **(c) Yes, $R^2$ is fine.** It consistently estimates the population $\rho^2=1-\sigma_u^2/\sigma_y^2$ **whether or not MLR.5 holds.**
>
> **The reason is that $\sigma_u^2$ and $\sigma_y^2$ are *unconditional* variances.** Heteroskedasticity is a statement about $\mathrm{Var}(u\mid\mathbf{x})$ — how the variance moves *across* values of $\mathbf{x}$. Averaged over the population, $\sigma_u^2$ is a single well-defined number, and $\text{SSR}/n$ estimates it consistently regardless. **Same for $\bar R^2$.**
>
> **(d) Everything built on a standard error:**
> - $\mathrm{se}(\hat\beta_j)$ and $\widehat{\mathrm{Var}}(\hat\beta_j)$ — **biased**
> - every $t$ statistic and $p$-value
> - every confidence interval
> - every $F$ statistic, **including the SSR form and therefore the Chow test**
> - the LM statistic
> - **and the claim that OLS is BLUE or asymptotically efficient**
>
> **What survives:** the point estimates $\hat\beta_j$, $R^2$, $\bar R^2$, and the fitted values.
>
> **(e) WLS is not necessary. The minimal fix is heteroskedasticity-robust standard errors.**
>
> **Keep the OLS point estimates** — they were never the problem — **and replace the standard errors with**
> $$\widehat{\mathrm{Var}}(\hat\beta_j)=\frac{\sum_i\hat r_{ij}^2\hat u_i^2}{\text{SSR}_j^2}$$
> which is valid **whether or not** heteroskedasticity is present. One option flag in any package. Then use robust $t$'s and a robust Wald statistic in place of $F$.
>
> **When WLS is still worth it:**
> - **Strong heteroskedasticity and a large sample**, where the efficiency gain is real. In Example 8.6, comparing *robust* standard errors, WLS beat OLS by **25% on $inc$ and 40% on $(age-25)^2$** — and that was with a variance model almost certainly wrong.
> - **Grouped or per-capita data**, where the weights ($m_i$, or population) come from the model rather than a guess.
>
> **Even then, report fully robust standard errors after WLS.** WLS for efficiency, robust inference for validity.

---

### Exercise 2 — Breusch–Pagan, White, and the special case

A model with $k=4$ regressors is estimated on $n=250$ observations.

- BP auxiliary regression ($\hat u^2$ on the 4 regressors): $R^2_{\hat u^2}=0.0873$
- Full White regression ($\hat u^2$ on the 4 regressors, their 4 squares, and the 6 cross products): $R^2_{\hat u^2}=0.1264$
- Special-case White ($\hat u^2$ on $\hat y$, $\hat y^2$): $R^2_{\hat u^2}=0.0412$

**(a)** Compute the LM statistic, degrees of freedom, and 5% critical value for each of the three tests. State each conclusion.
**(b)** Compute the $F$ form of the BP test and confirm it agrees.
**(c)** Explain why the full White test has 14 regressors here. How many would it have with $k=8$?
**(d)** The special case uses only 2 df regardless of $k$. What exactly is it testing, and why must it be $\hat y$ rather than $y$?
**(e)** The researcher's model is $wage=\beta_0+\beta_1 educ+\beta_2 exper+\beta_3 tenure+\beta_4 female+u$, in levels. Given these results, what should she do **first**, and why is testing for heteroskedasticity not the top priority?

> [!example]- Solution
> **(a)** $LM=n\,R^2_{\hat u^2}$, $df=$ number of regressors in the auxiliary regression.
>
> | Test | $q$ | $LM=250R^2$ | $\chi^2_q$ 5% crit | $p$ | Conclusion |
> |---|---|---|---|---|---|
> | **Breusch–Pagan** | $4$ | $\mathbf{21.83}$ | $9.49$ | $0.0002$ | **Reject** |
> | **White (full)** | $14$ | $\mathbf{31.60}$ | $23.69$ | $0.0046$ | **Reject** |
> | **White (special)** | $2$ | $\mathbf{10.30}$ | $5.99$ | $0.0058$ | **Reject** |
>
> **All three reject decisively.** Notice that the full White test has the **largest** statistic but the **weakest** $p$-value of the three — the 14 degrees of freedom cost more than the extra regressors buy. **This is the White test's characteristic weakness in miniature.**
>
> **(b)** $$F=\frac{R^2_{\hat u^2}/k}{(1-R^2_{\hat u^2})/(n-k-1)}=\frac{0.0873/4}{(1-0.0873)/245}=\frac{0.021825}{0.0037253}=\mathbf{5.86}$$
> Critical value $F_{4,245}$ at 5% is $\mathbf{2.41}$. **Reject** — the same conclusion as $LM=21.83$, as it must be. **The two forms are asymptotically equivalent; use whichever your package prints.**
>
> **(c)** With $k$ regressors the White regression contains:
> $$\underbrace{k}_{\text{levels}}+\underbrace{k}_{\text{squares}}+\underbrace{\binom{k}{2}}_{\text{cross products}}=2k+\frac{k(k-1)}{2}$$
> For $k=4$: $4+4+6=\mathbf{14}$ ✓. For $k=8$: $8+8+28=\mathbf{44}$.
>
> **This is why the pure White test is rarely used as $k$ grows.** With $k=8$ you would spend 44 degrees of freedom to test one assumption — and if any regressor is a dummy, its square is **identical to itself** and must be dropped as redundant, which is an extra bookkeeping trap.
>
> **(d) It tests whether $\mathrm{Var}(u\mid\mathbf{x})$ varies with the *level of the conditional mean*, $\mathbb{E}(y\mid\mathbf{x})$.**
>
> $\hat y_i=\hat\beta_0+\hat\beta_1x_{i1}+\cdots+\hat\beta_kx_{ik}$ is a **linear combination** of the regressors, so $\hat y$ and $\hat y^2$ between them are **particular functions of all the levels, squares and cross products** in the full White regression. The special case is therefore a **restricted version** of the full White test — it imposes restrictions on the $\delta_j$ in (8.19), which is why it costs only 2 df.
>
> **It must be $\hat y$, not $y$.** $\hat y$ is a function of the regressors and the estimated parameters, so it is (asymptotically) legitimate as an auxiliary regressor. But
> $$y_i=\hat y_i+\hat u_i$$
> so **$y$ contains the residual itself.** Regressing $\hat u_i^2$ on $y_i$ would find a relationship whether or not any heteroskedasticity exists — a mechanical correlation, not a test. **The result would not be a valid test at all.**
>
> **(e) She should test the functional form first — specifically, try $\log(wage)$.**
>
> **The reason:** every heteroskedasticity test maintains **MLR.1–4**. If MLR.4 fails because $\mathbb{E}(y\mid\mathbf{x})$ is misspecified — the wrong functional form, a missing quadratic — **the test can reject even when $\mathrm{Var}(y\mid\mathbf{x})$ is exactly constant.** A rejection is therefore **ambiguous**: it means "something is wrong," not "the variance is non-constant."
>
> **Example 8.4 is the demonstration.** The housing price equation in **levels** rejects at $p=0.002$ ($LM=14.09$). Put $price$, $lotsize$ and $sqrft$ in **logs** and the same test gives $LM=4.22$, $p=0.239$ — **no rejection at all.** Nothing about the variance was "corrected"; only the functional form changed.
>
> **And a wage equation in levels is exactly the case where logs are indicated** ([[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §2a): wages are a **strictly positive dollar amount**, so the conditional distribution is typically **skewed and heteroskedastic**, and $\log(wage)$ both fixes that and delivers interpretable semi-elasticities.
>
> **The order of operations:**
> 1. **Test functional form** — RESET and the tools of [[09 - More on Specification and Data Issues|ch. 09]].
> 2. **Settle on a specification.**
> 3. **Then** test for heteroskedasticity, and use robust standard errors regardless.
>
> **Wooldridge's reason for this order is blunt: functional form misspecification is more important than heteroskedasticity** — it causes **bias**, whereas heteroskedasticity only invalidates standard errors.

---

### Exercise 3 — Reading robust versus usual standard errors

From the `CRIME1` arrest equation (Example 8.3, $n=2{,}725$):

| Variable | $\hat\beta$ | OLS se | Robust se |
|---|---|---|---|
| $avgsen$ | $0.0178$ | $0.0097$ | $0.0101$ |
| $avgsen^2$ | $-0.00052$ | $0.00030$ | $0.00021$ |
| $ptime86$ | $-0.0394$ | $0.0087$ | $0.0062$ |
| $black$ | $0.325$ | $0.045$ | $0.058$ |

**(a)** Compute both $t$ statistics for $avgsen^2$ and for $black$. What changes?
**(b)** A student states: *"Robust standard errors are always larger, because they correct for a problem."* Refute using this table.
**(c)** Find the turning point of the quadratic in $avgsen$ and interpret it. Is the interpretation credible?
**(d)** The usual LM statistic for $H_0:\beta_{avgsen}=0,\beta_{avgsen^2}=0$ is $3.54$; the robust version is $4.00$. Give the $p$-values and the conclusion. Why must the *robust* LM be used here?
**(e)** Set out the four steps to compute the robust LM statistic for this hypothesis, being specific about what is regressed on what.

> [!example]- Solution
> **(a)**
>
> | Variable | $t_{\text{usual}}$ | $t_{\text{robust}}$ | Effect |
> |---|---|---|---|
> | $avgsen^2$ | $-0.00052/0.00030=\mathbf{-1.73}$ | $-0.00052/0.00021=\mathbf{-2.48}$ | **insignificant → significant at 5%** |
> | $black$ | $0.325/0.045=\mathbf{7.22}$ | $0.325/0.058=\mathbf{5.60}$ | significant either way, but **weaker** |
>
> **The two move in opposite directions**, which is the point of the exercise. Robust inference makes $avgsen^2$ *more* convincing and $black$ *less*.
>
> **(b) The claim is false, and this table refutes it twice over.**
>
> $avgsen^2$: robust se is **30% smaller** ($0.00021$ vs $0.00030$). $ptime86$: **29% smaller.** Only $black$ and $avgsen$ have larger robust standard errors.
>
> **Why the intuition is wrong.** The robust formula is
> $$\widehat{\mathrm{Var}}(\hat\beta_j)=\frac{\sum_i\hat r_{ij}^2\hat u_i^2}{\text{SSR}_j^2}$$
> versus the usual $\hat\sigma^2/\text{SSR}_j$. These differ by **how the squared residuals line up with $\hat r_{ij}^2$** — whether the large errors occur where $x_j$ is far from its conditional mean, or near it. **If the large errors happen to sit where $\hat r_{ij}^2$ is small, the robust variance is smaller.** There is no theorem forcing a direction.
>
> **The honest statement is: robust standard errors are *valid* more often, not *bigger*.** (Empirically they are more often larger, but that is a tendency, not a rule — Example 8.1 has $exper$ at $0.0052$ usual and $0.0051$ robust.)
>
> **(c)** $$avgsen^*=\frac{0.0178}{2(0.00052)}=\mathbf{17.1\text{ months}}$$
>
> **Literal reading:** below 17 months, longer average sentences are associated with **more** arrests; above 17 months, the expected **deterrent** effect appears.
>
> **Not credible as stated.** A positive relationship between sentence length and arrests over the first 17 months has no deterrence story behind it. **Two better explanations:**
> 1. **Reverse causation / selection:** men who commit more crimes accumulate longer average sentences. $avgsen$ is measuring criminal propensity, not deterrence.
> 2. **Grogger (1991)**, using a superset of these data and different methods, found $tottime$ has a significantly **positive** effect on arrests and interpreted it as **human capital built up in criminal activity** — the same logic applies here.
>
> **And [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §2b's diagnostic applies:** a turning point that makes no economic sense usually indicates **misspecification**, not a real reversal.
>
> **(d)**
>
> | Statistic | Value | $p$ ($\chi^2_2$) | Conclusion |
> |---|---|---|---|
> | Usual LM | $3.54$ | $0.170$ | do not reject |
> | **Robust LM** | $4.00$ | $0.135$ | **do not reject** |
>
> **Neither rejects even at the 15% level. Average sentence length does not appear to affect arrests.** (Consistent with $avgsen$ entering alone: $t_{\text{usual}}=0.658$, $t_{\text{robust}}=0.592$.)
>
> **Why the robust version is required.** The usual LM statistic is $n R^2_{\tilde u}$ from regressing restricted residuals on all regressors, and **its asymptotic $\chi^2_q$ distribution is derived under MLR.5.** Under heteroskedasticity it is **not asymptotically $\chi^2$**, so the $p$-value of $0.170$ is not the $p$-value of anything. And the individual robust $t$'s in this equation differ substantially from the usual ones — **direct evidence that heteroskedasticity is material here**, which is exactly when the usual LM cannot be trusted.
>
> **That the two happen to agree does not make the usual one valid.** It is a coincidence of this dataset.
>
> **(e)** With $q=2$ excluded variables ($avgsen$, $avgsen^2$) and the included set $\{pcnv,\;ptime86,\;qemp86,\;inc86,\;black,\;hispan\}$:
>
> **Step 1.** Estimate the **restricted** model — $narr86$ on $pcnv$, $ptime86$, $qemp86$, $inc86$, $black$, $hispan$ (**omitting both $avgsen$ terms**). Save the residuals $\tilde u$.
>
> **Step 2.** Purge each excluded variable of the included ones:
> - Regress $avgsen$ on $pcnv$, $ptime86$, $qemp86$, $inc86$, $black$, $hispan$ → residuals $\tilde r_1$
> - Regress $avgsen^2$ on the **same six** variables → residuals $\tilde r_2$
>
> **Step 3.** Form the products $\tilde r_1\tilde u$ and $\tilde r_2\tilde u$, observation by observation.
>
> **Step 4.** Regress **the constant 1** on $\tilde r_1\tilde u$ and $\tilde r_2\tilde u$, **with no intercept**. Then
> $$LM=n-\text{SSR}_1=2725-\text{SSR}_1\;\sim\;\chi^2_2$$
>
> Compare with $\chi^2_2$: 5% critical value $5.99$, 10% is $4.61$. **Here $LM=4.00$, so we do not reject at 10%.**
>
> > **Two traps in step 4:** the dependent variable really is a column of ones, and the regression really must **exclude the intercept** — with an intercept, $\text{SSR}_1$ would be zero. **It is a computational device with no interpretation as a regression**, doing for the LM test exactly what robust standard errors do for the $t$ test.
> >
> > **Note also that $avgsen^2$ is regressed on the included variables in step 2 — not the square of $\tilde r_1$.** Each excluded regressor is purged **as it enters the model.**

---

### Exercise 4 — Weighted least squares, by hand and by weight

**(a)** For $sav_i=\beta_0+\beta_1 inc_i+u_i$ with $\mathrm{Var}(u_i\mid inc_i)=\sigma^2 inc_i$, write the transformed equation and prove the transformed error is homoskedastic.
**(b)** Which Gauss–Markov assumptions does the transformed model satisfy that the original does not? What follows for the $t$ and $F$ statistics?
**(c)** State the weight the package needs. A student divides everything by $inc_i$ instead of $\sqrt{inc_i}$. What has gone wrong?
**(d)** A researcher has only **firm-level averages** of an individual-level contribution equation. Firms have $10$, $50$, $200$ and $1{,}000$ employees. Derive the correct weights and give the relative standard deviations of the firm-level errors. State the two assumptions the derivation needs.
**(e)** In Example 8.6, OLS gives $\hat\beta_{e401k}=6.89$ and WLS gives $5.19$. Is this a problem? What would make it a serious problem, and what does it indicate?

> [!example]- Solution
> **(a)** Here $h_i=h(inc_i)=inc_i$. Divide the equation through by $\sqrt{inc_i}$:
> $$\boxed{\;\frac{sav_i}{\sqrt{inc_i}}=\beta_0\frac{1}{\sqrt{inc_i}}+\beta_1\sqrt{inc_i}+u_i^*\;}$$
> using $inc_i/\sqrt{inc_i}=\sqrt{inc_i}$.
>
> **Note there is no intercept in the usual sense** — $\beta_0$ now multiplies the *variable* $1/\sqrt{inc_i}$, and $\beta_1$ multiplies $\sqrt{inc_i}$.
>
> **Proof of homoskedasticity.** With $u_i^*=u_i/\sqrt{inc_i}$ and conditioning on $inc_i$:
> $$\mathbb{E}(u_i^*\mid inc_i)=\frac{1}{\sqrt{inc_i}}\mathbb{E}(u_i\mid inc_i)=0$$
> since $\sqrt{inc_i}$ is a function of $inc_i$ (so it passes outside the conditional expectation). Hence
> $$\mathrm{Var}(u_i^*\mid inc_i)=\mathbb{E}\left[(u_i^*)^2\mid inc_i\right]=\frac{\mathbb{E}(u_i^2\mid inc_i)}{inc_i}=\frac{\sigma^2 inc_i}{inc_i}=\boxed{\sigma^2}$$
> **Constant — free of $inc_i$.** ∎
>
> **Also note $inc_i>0$ guarantees the variance is positive and the square root is defined** — which is why $h(inc)=inc$ is a legitimate variance model here.
>
> **(b) The transformed model satisfies MLR.5 (homoskedasticity), which the original violates.**
>
> MLR.1 (linear in parameters) ✓ — dividing by a constant per observation preserves linearity. MLR.2 (random sampling) ✓ — unchanged. MLR.3 (no perfect collinearity) ✓. MLR.4 ✓ — shown in (a). **MLR.5 ✓ — the new content.**
>
> **Therefore the transformed model satisfies all five Gauss–Markov assumptions, so OLS on it is BLUE.** And if $u$ is normal, so is $u^*$ (dividing a normal by a constant), giving **MLR.1–6 — the full classical linear model.**
>
> **Consequences:**
> - $t$ statistics have **exact $t_{n-k-1}$ distributions**; $F$ statistics have exact $F$ distributions.
> - $\text{SSR}^*/(n-k-1)$ is **unbiased** for $\sigma^2$.
> - The WLS estimator is **more efficient than OLS** on the untransformed equation.
>
> **All of this is conditional on $h(inc)=inc$ being correct.** Get it wrong and (c) of §4c applies: still consistent, but the standard errors are invalid again.
>
> **(c) The weight is $1/h_i=\boxed{1/inc_i}$** — proportional to the **inverse of the variance**.
>
> **The student has confused the two divisors.** The rule:
> - **Squared residuals** are weighted by $1/h_i$ — that is what the minimization $\sum(\cdot)^2/h_i$ does.
> - **Variables** are divided by $\sqrt{h_i}$ — the square root, because it goes *inside* the square.
>
> Dividing the variables by $inc_i$ implicitly assumes $h_i=inc_i^2$, i.e. $\mathrm{Var}(u_i\mid inc_i)=\sigma^2 inc_i^2$ — that the **standard deviation**, not the variance, is proportional to income.
>
> **The damage:** the transformed error is $u_i/inc_i$ with variance $\sigma^2 inc_i/inc_i^2=\sigma^2/inc_i$ — **still heteroskedastic, now decreasing in income.** He has over-corrected, turning heteroskedasticity of one sign into heteroskedasticity of the other.
>
> **Estimates remain consistent** (any positive $h$ preserves that under MLR.4), **but the standard errors are as invalid as before.**
>
> **(d)** Let the individual-level model be $contrib_{i,e}=\beta_0+\beta_1 earns_{i,e}+\beta_2 age_{i,e}+\beta_3 mrate_i+u_{i,e}$. Averaging over the $m_i$ employees at firm $i$ gives the firm-level equation with error $\bar u_i=m_i^{-1}\sum_{e=1}^{m_i}u_{i,e}$.
>
> **The two assumptions:**
> 1. **$\mathrm{Var}(u_{i,e})=\sigma^2$ for all $i,e$** — the *individual-level* model is homoskedastic.
> 2. **$\mathrm{Cov}(u_{i,e},u_{i,g})=0$ for $e\ne g$ within firm $i$** — no within-firm error correlation.
>
> Then, by the usual variance of an average of uncorrelated equal-variance variables,
> $$\mathrm{Var}(\bar u_i)=\frac{\sigma^2}{m_i}\quad\Longrightarrow\quad h_i=\frac{1}{m_i}\quad\Longrightarrow\quad \boxed{\text{weight}=\frac{1}{h_i}=m_i}$$
>
> | $m_i$ | $h_i=1/m_i$ | **Weight** | sd of $\bar u_i$ (in units of $\sigma$) |
> |---|---|---|---|
> | $10$ | $0.100$ | $10$ | $0.316$ |
> | $50$ | $0.020$ | $50$ | $0.141$ |
> | $200$ | $0.005$ | $200$ | $0.071$ |
> | $1{,}000$ | $0.001$ | $1{,}000$ | $0.032$ |
>
> **Weight by firm size.** The 1,000-employee firm gets **100 times** the weight of the 10-employee firm, because its average is measured with a standard deviation **10 times smaller** ($\sqrt{100}$).
>
> **This is the one case where the weights are not arbitrary** — they fall out of the model rather than being guessed. **The same applies to per-capita data at city, county, state or country level: weight by population.**
>
> **How it breaks.** If assumption 1 fails, the right weight depends on the individual-level variance function, not $m_i$. If assumption 2 fails — **within-group correlation, extremely common with geographic groups** — then $\mathrm{Var}(\bar u_i)\ne\sigma^2/m_i$ at all, and $m_i$ is simply the wrong weight.
>
> **This is why many researchers now just use OLS with robust standard errors on per-capita data. The hedge: weight by group size for efficiency, but report robust standard errors.**
>
> **(e) Not a problem *per se* — OLS and WLS always differ by sampling error — but this gap is large enough to be informative.**
>
> **$6.89 \to 5.19$ is a 25% drop**, with OLS se $2.29$ and WLS se $1.70$; the difference of $1.70$ is on the order of one standard error, so it is not decisive on its own. **But Wooldridge reads it as evidence of functional-form misspecification in the mean equation**, and suggests interacting $e401k$ with $inc$.
>
> **Why any systematic OLS–WLS gap is diagnostic.** Under **MLR.1–4** both estimators are consistent for the same $\beta_j$, **for any positive weighting function** — because $\mathbb{E}(u\mid\mathbf{x})=0$ implies the weighted error $u/\sqrt{h(\mathbf{x})}$ is uncorrelated with the weighted regressors $x_j/\sqrt{h(\mathbf{x})}$. **So under a correctly specified conditional mean, they cannot systematically disagree.**
>
> **Crucially, WLS needs the *full* MLR.4.** It is **not** enough that $u$ be uncorrelated with each $x_j$ — that would suffice for OLS. If $\mathbb{E}(y\mid\mathbf{x})\ne\beta_0+\beta_1x_1+\cdots+\beta_kx_k$, **OLS and WLS have different probability limits.**
>
> **What would make it serious:**
>
> | Symptom | Verdict |
> |---|---|
> | Same signs; biggest changes on **insignificant** variables | **Fine** — sampling error (Example 8.7's price effect) |
> | **Both significant, opposite signs** | **Alarm** — MLR.4 is almost certainly violated |
> | Practically large gap on a **key** coefficient | **Suspicious** — investigate the functional form |
>
> **The `nettfa` case is the third row**, which is why Wooldridge flags it rather than dismissing it. **The Hausman (1978) test formalizes the comparison; in most cases eyeballing is enough.**

---

### Exercise 5 — FGLS and the linear probability model

**(a)** Set out the five steps of the FGLS procedure for $\mathrm{Var}(u\mid\mathbf{x})=\sigma^2\exp(\delta_0+\delta_1x_1+\cdots+\delta_kx_k)$.
**(b)** Breusch–Pagan assumed a **linear** variance function; FGLS uses an **exponential** one. Explain why the difference is essential, not cosmetic.
**(c)** Is FGLS unbiased? Is it BLUE? What is it, and why is it still worth using?
**(d)** For a linear probability model, give the exact variance function and the estimated weights. Compute the weights for $\hat y_i\in\{0.5,\,0.1,\,0.05,\,-0.10\}$. What goes wrong, and how often does it happen in `MROZ`?
**(e)** In Example 8.7 the BP auxiliary regression gives $R^2_{\hat u^2}=0.040$ with $n=807$ and $k=6$. A student says this is negligible. Compute the LM statistic and settle it.

> [!example]- Solution
> **(a) The FGLS procedure:**
>
> 1. **Run OLS** on $y=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+u$. Save the residuals $\hat u$.
> 2. **Compute $\log(\hat u^2)$** — square first, *then* take the log.
> 3. **Regress $\log(\hat u^2)$ on $x_1,\dots,x_k$.** Save the **fitted values** $\hat g_i$ — not the coefficients, not the residuals.
> 4. **Exponentiate:** $\hat h_i=\exp(\hat g_i)$.
> 5. **Run WLS with weights $1/\hat h_i$.** Equivalently, divide every variable **including the constant** by $\sqrt{\hat h_i}$ and run OLS with no intercept.
>
> **Variant on step 3:** regress $\log(\hat u^2)$ on $\hat y$ and $\hat y^2$ instead — the same degrees-of-freedom economy as White's special case.
>
> **(b) It is essential: WLS requires strictly positive estimated variances.**
>
> | | Purpose | Linear form acceptable? |
> |---|---|---|
> | **Breusch–Pagan** | **Detect** a relationship between $u^2$ and $\mathbf{x}$ | ✅ — you only need power against an alternative; a fitted value that comes out negative is meaningless but harmless, because you never use it |
> | **FGLS** | **Correct** — build weights $1/\hat h_i$ | ❌ — **one negative $\hat h_i$ and $1/\sqrt{\hat h_i}$ is undefined; the procedure fails** |
>
> **The linear model $\hat h_i=\hat\delta_0+\hat\delta_1x_{i1}+\cdots$ has no mechanism preventing negative fitted values** — the same defect as the LPM in [[07 - Multiple Regression Analysis with Qualitative Information|ch. 07]] §5, arising for the same reason.
>
> **$\exp(\cdot)$ is positive for every real argument, so $\hat h_i=\exp(\hat g_i)>0$ is guaranteed no matter what $\hat g_i$ is.** That is the whole reason for the exponential form.
>
> **And note the pleasant side-effect:** taking logs converts a multiplicative variance model into an **additive, linear-in-parameters** one that OLS can estimate:
> $$u^2=\sigma^2\exp(\delta_0+\mathbf{x}\boldsymbol\delta)v\quad\Longrightarrow\quad\log(u^2)=\alpha_0+\delta_1x_1+\cdots+\delta_kx_k+e$$
> **You get positivity and estimability from the same transformation.**
>
> **(c)** | Property | FGLS |
> |---|---|
> | Unbiased | ❌ |
> | BLUE | ❌ |
> | **Consistent** | ✅ |
> | **Asymptotically more efficient than OLS** | ✅ |
>
> **Why unbiasedness is lost:** $h_i$ is **estimated from the same data** used to estimate the $\beta_j$, so $\hat h_i$ is correlated with the residuals. **If we could use the true $h_i$, WLS would be unbiased and BLUE.** Having to estimate it destroys both — and BLUE cannot survive the loss of unbiasedness by definition.
>
> **Why it is still worth using:** for large samples, **consistency plus asymptotic efficiency is what matters.** FGLS delivers the efficiency gain that motivated WLS in the first place, and its $t$ and $F$ statistics have the usual asymptotic distributions.
>
> **And FGLS estimates the parameters of the *original* population model** — $\hat\beta_j^{FGLS}$ measures exactly the same marginal effect as $\hat\beta_j^{OLS}$. **You are choosing a more precise estimator of the same quantity, not changing the question.**
>
> **Practical addendum:** if you doubt the exponential variance model — and you should, since it too is just a model — **compute fully robust standard errors after WLS.** They are valid under arbitrary misspecification of $h$.
>
> **(d)** For a binary $y$,
> $$\mathrm{Var}(y\mid\mathbf{x})=p(\mathbf{x})\left[1-p(\mathbf{x})\right],\qquad p(\mathbf{x})=\beta_0+\beta_1x_1+\cdots+\beta_kx_k$$
> **The variance function is known exactly, up to the $\beta_j$** — a rare luxury. Plug in the OLS fitted values:
> $$\boxed{\;\hat h_i=\hat y_i(1-\hat y_i)\;}$$
>
> | $\hat y_i$ | $\hat h_i$ | Weight $1/\hat h_i$ |
> |---|---|---|
> | $0.50$ | $0.2500$ | $\mathbf{4.00}$ |
> | $0.10$ | $0.0900$ | $\mathbf{11.11}$ |
> | $0.05$ | $0.0475$ | $\mathbf{21.05}$ |
> | $-0.10$ | $\mathbf{-0.11}$ | **undefined** |
>
> **The pattern is sensible where it works:** predicted probabilities near 0 or 1 have **small** variance and therefore earn **large** weight; the variance is maximal at $\hat y=0.5$, which gets the least weight. An observation at $\hat y=0.05$ counts more than five times one at $\hat y=0.5$.
>
> **What goes wrong.** WLS multiplies observation $i$ by $1/\sqrt{\hat h_i}$, so **every weight must be strictly positive.** Whenever $\hat y_i<0$ or $\hat y_i>1$ — which is the LPM's signature defect — $\hat h_i<0$ and the square root does not exist. **The method fails outright for that observation.**
>
> **In `MROZ`:** 16 fitted values below 0 and 17 above 1, so
> $$\frac{33}{753}=\mathbf{4.4\%}\text{ of the sample is unusable.}$$
>
> **The patches — dropping those observations, or truncating $\hat y_i$ to $[0.01,0.99]$ — are both ad hoc.** Dropping changes the sample non-randomly (it drops precisely the extreme observations); truncating assigns weights that no model justifies. **Neither has a principled defence.**
>
> **Which is why the recommended treatment of an LPM is simply OLS with robust standard errors.** Example 8.8 shows why that is not a sacrifice: in `MROZ`, several robust and usual standard errors are **identical to the reported precision**, and no conclusion changes. **Heteroskedasticity is a theoretical certainty here and a practical non-event.**
>
> **(e) The student is wrong, and decisively.**
>
> $$LM=n\,R^2_{\hat u^2}=807(0.040)=\mathbf{32.28}\;\sim\;\chi^2_6$$
>
> | | Value |
> |---|---|
> | $\chi^2_6$ critical value, 5% | $12.59$ |
> | $\chi^2_6$ critical value, 1% | $16.81$ |
> | **$p$-value** | $\mathbf{<0.000015}$ |
>
> **Overwhelming rejection of homoskedasticity.**
>
> **The error in the student's reasoning:** $R^2_{\hat u^2}$ measures how much of the variation in $\hat u^2$ the regressors explain — **it is not a measure of how strong the evidence is.** The evidence is $n R^2$, and $n=807$ multiplies a small $R^2$ into a large statistic.
>
> **The general point:** with a large sample, **a seemingly negligible $R^2_{\hat u^2}$ can produce a very strong rejection.** Conversely, with $n=40$, the same $R^2=0.040$ would give $LM=1.60$ — nowhere near significance. **Always compute $F$ or LM. Never eyeball $R^2_{\hat u^2}$.**
>
> **This is the same statistical-vs-practical-significance point as [[04 - Multiple Regression Analysis - Inference|ch. 04]]** — here running in the direction that catches people out.

---

## 📝 Summary

- **Heteroskedasticity causes no bias and no inconsistency.** $\hat\beta_j$ is unbiased under MLR.1–4 and consistent under MLR.1–4; **MLR.5 appears in neither proof.** $R^2$ and $\bar R^2$ also remain consistent for the population $\rho^2$, because $\sigma_u^2$ and $\sigma_y^2$ are **unconditional** variances.
- **What breaks is every standard error and every statistic built on one** — $t$, $F$ (including the SSR form and hence the **Chow test**), and LM — plus the Gauss–Markov and asymptotic-efficiency results. **And no sample size repairs any of it**: unlike non-normality, heteroskedasticity is not an asymptotic problem.
- **Heteroskedasticity-robust standard errors** replace $\hat\sigma^2/\text{SSR}_j$ with $\sum_i\hat r_{ij}^2\hat u_i^2/\text{SSR}_j^2$, using $\hat u_i^2$ where the unknown $\sigma_i^2$ belongs. They are valid **whether or not** heteroskedasticity is present, but only **asymptotically** — which is why the usual (exactly-$t$ under MLR.1–6) standard errors have not disappeared. **They can be larger or smaller than the usual ones.**
- **The robust LM statistic** needs only OLS: restricted residuals $\tilde u$; regress each excluded variable on the included ones to get $\tilde r_j$; regress **1 on $\tilde r_1\tilde u,\dots,\tilde r_q\tilde u$ with no intercept**; then $LM=n-\text{SSR}_1\sim\chi^2_q$.
- **Breusch–Pagan** regresses $\hat u^2$ on the regressors and uses $LM=nR^2_{\hat u^2}\sim\chi^2_k$ (the Koenker form, preferred over Breusch and Pagan's normality-based original). **White** adds all squares and cross products — $2k+\binom{k}{2}$ regressors, which burns degrees of freedom fast. **White's special case regresses $\hat u^2$ on $\hat y$ and $\hat y^2$ — always 2 df, whatever $k$ is** — and must use $\hat y$, never $y$.
- **A heteroskedasticity test can reject because the functional form is wrong.** All these tests maintain MLR.1–4. **Test functional form first** ([[09 - More on Specification and Data Issues|ch. 09]]); misspecification causes bias, heteroskedasticity only invalidates standard errors. Example 8.4 makes the point: levels reject at $p=0.002$, logs at $p=0.239$.
- **WLS transforms the model by dividing through by $\sqrt{h_i}$**, producing an equation that satisfies **all** the Gauss–Markov assumptions — so OLS on it is BLUE with exact $t$ and $F$ distributions. **Squared residuals are weighted by $1/h_i$; variables are divided by $\sqrt{h_i}$.** Always interpret the coefficients in the **original** equation.
- **For grouped or per-capita data the weights come from the model, not a guess:** if the individual-level equation is homoskedastic with uncorrelated within-group errors, $\mathrm{Var}(\bar u_i)=\sigma^2/m_i$, so **weight by group size** (firm employees, city population).
- **Feasible GLS** models $\mathrm{Var}(u\mid\mathbf{x})=\sigma^2\exp(\delta_0+\mathbf{x}\boldsymbol\delta)$, estimates it by regressing $\log(\hat u^2)$ on the regressors, and sets $\hat h_i=\exp(\hat g_i)$. **The exponential form is essential — WLS needs positive weights, and a linear variance model cannot guarantee them.** FGLS is **not unbiased and not BLUE**, but is **consistent and asymptotically more efficient than OLS**.
- **If the variance function is wrong: WLS stays consistent, its usual standard errors do not, and its efficiency advantage is not guaranteed.** The fix is **fully robust standard errors after WLS** — and in practice, *"it is often better to use a wrong form of heteroskedasticity and apply WLS than to ignore heteroskedasticity altogether and use OLS"*: in Example 8.6, robust-to-robust, WLS beat OLS by **25% on $inc$ and 40% on $(age-25)^2$**.
- **A large OLS–WLS gap indicts MLR.4, not the weights.** Both are consistent for the same $\beta_j$ under a correctly specified conditional mean, so systematic disagreement points to **functional form misspecification**.
- **In the linear probability model the variance function is known exactly**: $\hat h_i=\hat y_i(1-\hat y_i)$. **But it is negative wherever $\hat y_i\notin[0,1]$ — 4.4% of `MROZ` — so WLS fails there.** In practice, use **OLS with robust standard errors**; Example 8.8 shows the difference is negligible anyway.

---

## ⚠️ Important Notes

> [!warning] The eleven mistakes this chapter is designed to prevent
>
> 1. **Saying heteroskedasticity biases the coefficients.** It does not. Unbiasedness and consistency need only MLR.1–4.
> 2. **Believing a large sample fixes it.** It does not, ever. **Non-normality is an asymptotic non-issue; heteroskedasticity is not.**
> 3. **Claiming robust standard errors are always larger.** In Example 8.3, $avgsen^2$ goes from $0.00030$ to $0.00021$ (**30% smaller**), while $black$ goes from $0.045$ to $0.058$. **You cannot predict the direction.**
> 4. **Using the SSR-form $F$ or a Chow test under heteroskedasticity.** Both are invalid — **including when the only problem is different error variances across the two groups**, which is often exactly what you are investigating.
> 5. **Eyeballing $R^2_{\hat u^2}$.** In Example 8.7, $R^2_{\hat u^2}=0.040$ looks like nothing and gives $LM=32.28$ with $p<0.000015$, because $n=807$.
> 6. **Regressing $\hat u^2$ on $y$ instead of $\hat y$ in White's special case.** $y=\hat y+\hat u$ contains the residual, so the "test" finds a mechanical relationship. **Not a valid test at all.**
> 7. **Reading a rejected heteroskedasticity test as proof of heteroskedasticity.** It can equally mean **MLR.4 fails** — wrong functional form, missing quadratic, levels where logs belong. **Test functional form first.**
> 8. **Dividing the variables by $h_i$ instead of $\sqrt{h_i}$.** Squared residuals get $1/h_i$; variables get $1/\sqrt{h_i}$. Getting it wrong leaves you **still heteroskedastic, in the opposite direction.**
> 9. **Using a linear variance model for FGLS.** Fine for **testing** (BP), fatal for **correcting** — one negative $\hat h_i$ and $1/\sqrt{\hat h_i}$ does not exist. **Use $\exp(\cdot)$.**
> 10. **Trusting the WLS $R^2$ as a fit measure, or the raw transformed-equation $R^2$ at all.** The first measures explained variation in $y^*$; the second is uncentred, because the transformed regression has no intercept. **Both are still fine inside an $F$ statistic — provided the same weights are used for restricted and unrestricted models.**
> 11. **Reporting non-robust standard errors after WLS.** They assume your variance model is exactly right. **Fully robust WLS standard errors cost one option flag and survive arbitrary misspecification of $h$.**

> [!important] The four ideas most likely to be examined
>
> **1. The consequences table.** Which properties survive (unbiasedness, consistency, $R^2$) and which do not (all standard errors, $t$, $F$, LM, BLUE, asymptotic efficiency) — **and that large $n$ does not help.** Be able to name the assumptions each proof used.
>
> **2. $LM=nR^2_{\hat u^2}$ and its degrees of freedom.** BP: $df=k$. White: $df=2k+\binom{k}{2}$. **White's special case: $df=2$ always.** Be ready to compute both the $F$ and LM forms and confirm they agree.
>
> **3. The WLS transformation, derived.** Divide by $\sqrt{h_i}$; show $\mathrm{Var}(u_i/\sqrt{h_i}\mid\mathbf{x}_i)=\sigma^2h_i/h_i=\sigma^2$ in one line. **Then state that the transformed model satisfies MLR.1–5 (or 1–6 under normality), so OLS on it is BLUE with exact distributions.** And know that weights are $1/h_i$, not $1/\sqrt{h_i}$.
>
> **4. Why a large OLS–WLS gap indicts the conditional mean.** Under MLR.4, $u/\sqrt{h(\mathbf{x})}$ is uncorrelated with $x_j/\sqrt{h(\mathbf{x})}$ for **any** positive $h$, so both estimators are consistent for the same $\beta_j$ and cannot systematically disagree. **Systematic disagreement ⇒ suspect the functional form of $\mathbb{E}(y\mid\mathbf{x})$.**

> [!note] Cross-subject connections
> - **Heteroskedasticity is the cross-sectional twin of ARCH.** [[Time-series Analysis/contents/09 - ARCH, GARCH and Extensions|Time-series ch. 09]] models $\mathrm{Var}(u_t\mid\text{past})$ as time-varying; here it varies across the regressors instead. **Engle's ARCH test is $nR^2$ on a regression of $\hat u_t^2$ on its own lags** — the same auxiliary-regression device as Breusch–Pagan, with lags in place of regressors. Wooldridge returns to it in [[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]].
> - **GLS is the same idea as generalized least squares in [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]]** — transform until the error covariance matrix is $\sigma^2\mathbf{I}$, then apply OLS. Serial correlation ([[12 - Serial Correlation and Heteroskedasticity in Time Series Regressions|ch. 12]]) is the same machinery applied to off-diagonal rather than diagonal elements.
> - **WLS is sample weighting**, and appears throughout [[Machine Learning/contents/00-Index|Machine Learning]] as `sample_weight` in loss functions. The econometric motive is **efficiency under a known variance structure**; the ML motive is usually **class imbalance or importance weighting** — different reasons, identical arithmetic.
> - **Robust standard errors are the sandwich estimator** — the same construction underlies clustered standard errors and Newey–West HAC estimators. **All are "keep the estimates, fix the variance," and all are asymptotic.** The bootstrap (Wooldridge Appendix 6A) is a resampling alternative to the same problem.
> - **The log transformation as a variance stabilizer** connects to [[Data Preparation and Visualization/contents/00-Index|Data Preparation & Visualization]]: skewed, positive, heteroskedastic variables are exactly what log/Box–Cox transformations target. **Example 8.4 is a textbook variance-stabilizing transformation** — $p=0.002$ becomes $p=0.239$ purely by taking logs.
> - **The LPM's known variance function $p(1-p)$ is the Bernoulli variance**, and it is exactly what generalized linear models handle natively via the **variance function** in their IRLS fitting. **Logistic regression is FGLS done properly** — it weights by $\hat p(1-\hat p)$ but constrains $\hat p\in(0,1)$, which is precisely the constraint whose absence breaks WLS for the LPM.

> [!warning] Gaps in the source material
> - **No lecture slides exist for Econometrics.** Chapter scope (Wooldridge 1–12) is my own editorial decision — see [[00-Index]].
> - **No data files are in the vault.** `WAGE1`, `GPA3`, `CRIME1`, `HPRICE1`, `401KSUBS`, `SMOKE`, `MROZ` and `JTRAIN98` are all referenced and **none can be re-estimated.** Every coefficient, standard error and $R^2$ above is **quoted as printed.**
> - **Internal consistency verified wherever checkable, and it holds throughout:** the BP $F$ and LM for both housing models ($5.34/14.09$ in levels, $1.41/4.22$ in logs), the special-case White statistic ($3.45$, $p=0.178$), the Example 8.2 $F$ ($0.69$), both $avgsen$ turning points, the `SMOKE` age turning point ($42.8$) and income effect ($0.088$), the `SMOKE` LM ($32.28$), the Table 8.1 joint $F$ ($30.6$ against the printed $30.8$ — **rounding in the reported $R^2$s**), and the Table 8.2 robust-to-robust comparisons ($25\%$ and $39.5\%$, matching "25%" and "almost 40%"). ✓
> - **The robust standard errors themselves cannot be verified** — computing $\sum_i\hat r_{ij}^2\hat u_i^2$ requires the data. All robust standard errors above are **quoted**.
> - **Example 8.3's robust LM value ($4.00$) and Example 8.2's robust $F$ ($0.75$) are quoted, not reproducible** — both require software and the data.
> - **The `SMOKE` FGLS results (8.36) cannot be checked** — they depend on the estimated $\hat h_i$, which needs the data. **The $t$ statistic I compute for the WLS income effect ($1.30/0.44=2.95$) is arithmetic on the printed figures, not a re-estimation.**
> - **Tables 8.1 and 8.2 extracted intact.** Wooldridge does not report the WLS $R^2$ caveat numerically for Table 8.1, so the joint $F$ of $30.6$ is computed from the **weighted** $R^2$s as he describes — legitimate for exclusion restrictions because the SST terms cancel, but **not** interpretable as a fit comparison.
> - **The chapter's own text describes only the *first* four sections of the LPM discussion**; §8-5 is truncated in the extraction at the point where the fitted-value patch is introduced, so **the specific truncation rule Wooldridge recommends (if any) is not available.** I have described the standard patches and flagged them as ad hoc rather than attributing a recommendation to the text.
> - **All figures are images and do not extract.** Chapter 8 contains no numbered figures in the extracted text, so nothing is lost here.
> - **Notation mangling in the PDF:** `b^ j`, `s2 i` for $\sigma_i^2$, `r^ij` for $\hat r_{ij}$, `R2 ^u2` and `R22u^` (both) for $R^2_{\hat u^2}$, `u|` for $\tilde u$, `r|1` for $\tilde r_1$, `h^i` for $\hat h_i$, `!hi` for $\sqrt{h_i}$, `yp i` for $y_i^*$, `d^j` for $\hat\delta_j$, `x2 k` for $\chi^2_k$. **Every equation has been transcribed by hand against its numbered reference.**
> - **Two source errors:** equation (8.22) prints the slope as `biinci` where $\beta_1 inc_i$ is meant; and the text at Example 8.4 refers to *"the usual standard errors reported in (8.17)"* while pointing at equation (8.17) — correct, but the sentence reads as though (8.18) were meant. **Both corrected silently above.**

#econometrics #heteroskedasticity #robust-inference #wls #gls #breusch-pagan #white-test
