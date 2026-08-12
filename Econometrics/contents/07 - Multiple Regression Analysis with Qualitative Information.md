---
subject: Econometrics
chapter: 07
tags: [ds, econometrics, regression, dummy-variables, program-evaluation]
source: "Wooldridge, *Introductory Econometrics: A Modern Approach*, 7th ed., ch. 7 (pp. 220–261)"
---

# Multiple Regression Analysis with Qualitative Information

> [!abstract] What this chapter is for
> Every regressor so far has had **quantitative meaning** — wages, years, dollars, scores. But most of the interesting questions in economics are about **categories**: female or male, treated or untreated, South or North, manufacturing or retail, approved or denied.
>
> **The whole chapter follows from one device: code the category as a 0/1 variable and put it in the regression.** Nothing about OLS changes. Only the *interpretation* changes.
>
> | Section | Question |
> |---|---|
> | §1–2 | One binary regressor → **an intercept shift** |
> | §3 | Many categories, and **ordinal** information |
> | §4 | Interactions → **slope differences**, and the **Chow test** |
> | §5 | A **binary dependent variable** → the linear probability model |
> | §6 | **Program evaluation** and regression adjustment |
> | §7 | Discrete $y$ with quantitative meaning |

---

## 📘 Main Knowledge

### 1. Describing qualitative information

A **dummy variable** (binary variable, zero-one variable, indicator) takes the value 1 when an event occurs and 0 otherwise.

> [!tip] Name the variable after the event that equals one
> `female` is a good name: you know instantly that $female=1$ means female. `male` is equally good. **`gender` is a bad name** — does $gender=1$ mean male or female? The regression output is identical either way, but **you will misread your own results.**
>
> Same for parties: use `democrat` or `republican`, never `party`.

**Why 0 and 1 and not, say, 1 and 2?** The values are arbitrary in principle. **The payoff of 0/1 coding is that the coefficients get natural interpretations** — differences in intercepts, and later, differences in probabilities.

---

### 2. A single dummy independent variable

$$wage=\beta_0+\delta_0\,female+\beta_1 educ+u$$

Under MLR.4, $\mathbb{E}(u\mid female,educ)=0$, so

$$\boxed{\;\delta_0=\mathbb{E}(wage\mid female,educ)-\mathbb{E}(wage\mid male,educ)\;}$$

**Education is held at the same level in both expectations** — the difference is due to gender alone.

Geometrically this is an **intercept shift**. Men's line: $\beta_0+\beta_1 educ$. Women's line: $(\beta_0+\delta_0)+\beta_1 educ$. **The two lines are parallel** — the gap is the same at every level of education. (Figure 7.1 draws the $\delta_0<0$ case.)

> [!warning] The dummy variable trap
> **Do not also include `male`.** Since $female+male=1$, `male` is an exact linear function of `female` and the intercept. **That is perfect collinearity — a violation of MLR.3, and OLS cannot be computed.**
>
> **With two groups you need exactly two intercepts, and the overall intercept already supplies one.** So: **one dummy.**

**The base group** (benchmark group) is the group with no dummy — here, men. $\beta_0$ is *their* intercept; $\delta_0$ is the *difference*.

**Switching the base group changes nothing substantive.** Writing $wage=\alpha_0+\gamma_0\,male+\beta_1 educ+u$ gives $\alpha_0=\beta_0+\delta_0$ and $\gamma_0=-\delta_0$. **It does not matter which you pick — it matters enormously that you keep track of which one it is.**

> [!note] Why not drop the intercept and include both dummies?
> $wage=\beta_0 male+\alpha_0 female+\beta_1 educ+u$ has no trap, and each coefficient is a group intercept. **But it has two real drawbacks:** testing for a *difference* between groups becomes awkward (you now need a linear-combination test rather than reading off a $t$), and **$R^2$ is computed differently without an intercept** (see §3). **Always keep an overall intercept.**

**Testing.** Nothing about OLS or the distribution theory changes. $H_0:\delta_0=0$ against $H_1:\delta_0<0$ is an ordinary one-sided $t$ test.

#### Example 7.1 — the gender wage gap (`WAGE1`, 1976 wages)

$$\widehat{wage}=-1.57-1.81\,female+0.572\,educ+0.025\,exper+0.141\,tenure$$
$$\qquad\;\;(0.72)\;\;\;(0.26)\qquad\;\;(0.049)\qquad\;(0.012)\qquad\;(0.021)$$
$$n=526,\quad R^2=0.364$$

**A woman earns \$1.81/hour less than a man with the same education, experience and tenure.** (About \$7.40 in 2013 dollars: $4.09\times1.81=7.40$.)

> [!important] What "controlling for" buys you
> **The \$1.81 gap cannot be explained by differences in average education, experience or tenure between men and women — those are held fixed.** It is due to gender *or to factors associated with gender that are not in the regression.* That second clause is the whole caveat.

**Compare with the simple regression:**
$$\widehat{wage}=7.10-2.51\,female,\qquad n=526,\; R^2=0.116$$
$$\qquad\;\;(0.21)\;\;(0.30)$$

> [!tip] Simple regression on a constant and a dummy = a comparison of means
> - Intercept $=7.10$ is the **sample mean wage for men** (set $female=0$).
> - $7.10-2.51=4.59$ is the **sample mean wage for women**.
> - $t=-2.51/0.30=\mathbf{-8.37}$ is exactly a **two-sample comparison-of-means $t$ test**.
>
> (274 men, 252 women.) **This works only under homoskedasticity** — the wage variance must be equal across groups. Otherwise use the heteroskedasticity-robust version of [[08 - Heteroskedasticity|ch. 08]].

**Why is $-2.51$ bigger than $-1.81$?** Because the simple regression **omits** education, experience and tenure, which are **lower on average for women in this sample**. Classic omitted variable bias from [[03 - Multiple Regression Analysis - Estimation|ch. 03]]. **The $-1.81$ is the ceteris paribus gap and is the more reliable number — and it is still large.**

#### Example 7.2 — PC ownership and college GPA (`GPA1`)

$$\widehat{colGPA}=1.26+0.157\,PC+0.447\,hsGPA+0.0087\,ACT,\qquad n=141,\;R^2=0.219$$
$$\qquad\qquad(0.33)\;\;(0.057)\qquad(0.094)\qquad\;(0.0105)$$

Owning a PC is associated with a GPA about **0.16 points higher**, $t=0.157/0.057=2.75$. Dropping the controls gives $0.170$ (se $0.063$) — **barely different**.

> [!warning] Association is not the causal effect you want
> PC ownership is a **choice**, unlike gender. A PC could raise quality of work and save lab time — or enable games and web surfing. The controls $hsGPA$ and $ACT$ are there because **stronger students may be more likely to own computers.** What we want is *"the average effect on colGPA if a student were picked at random and given a computer."* **The regression estimates that only if the controls are sufficient.**

#### Example 7.3 — training grants (`JTRAIN`, Michigan 1988)

$$\widehat{hrsemp}=46.67+26.25\,grant-0.98\log(sales)-6.07\log(employ)$$
$$\qquad\quad\;\;(43.41)\;\;(5.59)\qquad\;(3.54)\qquad\qquad(3.88)$$
$$n=105,\quad R^2=0.237$$

- $t_{grant}=26.25/5.59=\mathbf{4.70}$ — very significant. Grant firms trained each worker **26.25 hours more**, against a sample mean of about **17 hours** (max 164). **A very large effect.**
- $\log(employ)$: a firm **10% larger** trains each worker $0.10\times6.07=\mathbf{0.61}$ hour **less**; $t=-1.56$, marginal.
- **$hrsemp$ cannot be logged** — it is zero for **29 of the 105 firms**. (§6-2a of [[06 - Multiple Regression Analysis - Further Issues|ch. 06]].)

> [!warning] Is it causal?
> **Nothing in the regression tells you.** Firms that received grants might have trained more anyway. **You must know how grants were assigned.** Wooldridge's honest verdict: *"We can only hope we have controlled for as many factors as possible."*

#### 2a. Dummies when the dependent variable is $\log(y)$

**Multiply the coefficient by 100 and read it as a percentage difference.**

**Example 7.4 — house style** (`HPRICE1`):
$$\widehat{\log(price)}=-1.35+0.168\log(lotsize)+0.707\log(sqrft)+0.027\,bdrms+0.054\,colonial$$
$$\qquad\qquad\;(0.65)\;\;(0.038)\qquad\quad(0.093)\qquad\;\;(0.029)\qquad\;(0.045)$$
$$n=88,\quad R^2=0.649$$

A colonial-style house sells for about **5.4% more**. Exact: $100[e^{0.054}-1]=\mathbf{5.5\%}$ — the correction barely matters here.

**Example 7.5 — log wage** (`WAGE1`):
$$\widehat{\log(wage)}=0.417-0.297\,female+0.080\,educ+0.029\,exper-0.00058\,exper^2+0.032\,tenure-0.00059\,tenure^2$$
$$\qquad\qquad(0.099)\;(0.036)\qquad\;(0.007)\qquad(0.005)\qquad(0.00010)\qquad\;(0.007)\qquad(0.00023)$$
$$n=526,\quad R^2=0.441$$

$$\boxed{\;\%\Delta = 100\left[\exp(\hat\beta_1)-1\right]\;}$$

$$\text{Women vs men: } 100[e^{-0.297}-1]=\mathbf{-25.7\%}$$
$$\text{Men vs women: } 100[e^{+0.297}-1]=\mathbf{+34.6\%}$$

> [!important] Which number do you report? The approximation — 29.7%.
> **The exact formula is base-group-specific.** "Women earn 25.7% less than men" and "men earn 34.6% more than women" are **both correct and both exact**, and they are different numbers because they have different denominators.
>
> $$25.7\;<\;29.7\;<\;34.6$$
>
> **The log approximation sits between them (close to the middle), so reporting "the difference in predicted wages between men and women is about 29.7%" lets you avoid taking a stand on which group is the base.** Same logic as the $\pm1$ asymmetry in [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §2a.
>
> **The correction matters more the larger $|\hat\beta_1|$ is** — 0.1 percentage points for the colonial dummy (0.054), 4 percentage points for the female dummy (0.297).

---

### 3. Dummy variables for multiple categories

**The rule:**

> [!important] $g$ groups $\Rightarrow$ $g-1$ dummies, plus the overall intercept
> - The **base group's** intercept **is** the overall intercept.
> - Each dummy coefficient is the **difference in intercepts** between that group and the base group.
> - **Including all $g$ dummies with an intercept is the dummy variable trap.**

**Example 7.6 — four gender/marital groups** (`WAGE1`). Base group: **single men**.

$$\widehat{\log(wage)}=0.321+0.213\,marrmale-0.198\,marrfem-0.110\,singfem+0.079\,educ+\cdots$$
$$\qquad\qquad(0.100)\;\;(0.055)\qquad\quad(0.058)\qquad\quad(0.056)\qquad\;(0.007)$$
$$n=526,\quad R^2=0.461$$

| Group | Coefficient | $t$ | vs single men (approx) | Exact |
|---|---|---|---|---|
| Single men | *base* | — | — | — |
| **Married men** | $+0.213$ | $3.87$ | $+21.3\%$ | $+23.7\%$ |
| **Married women** | $-0.198$ | $-3.41$ | $-19.8\%$ | $-18.0\%$ |
| **Single women** | $-0.110$ | $-1.96$ | $-11.0\%$ | $-10.4\%$ |

$t$ for $singfem$ is $-0.110/0.056=-1.96$ — **just significant at 5%**, two-sided.

**Compare with the simple additive model.** Adding `married` to (7.9) gives a marriage premium of $0.053$ (se $0.041$), $t=1.29$ — **insignificant**, and $female$ becomes $-0.290$.

> [!warning] The additive model forces the marriage premium to be the same for men and women
> **It is not.** From (7.11), marriage is worth $+21.3\%$ to a man and $-8.8\%$ to a woman (relative to being single, same sex). **Averaging those into a single 5.3% "premium" hides the entire finding.** Interactions (§4a) are the general fix.

#### Differences between two **non-base** groups

The overall intercept is common to every group, so it cancels:

$$\text{single women}-\text{married women}=-0.110-(-0.198)=\mathbf{+0.088}$$

**Single women earn about 8.8% more than married women.**

> [!warning] You cannot test this difference from (7.11)
> $\mathrm{se}(\hat\beta_{singfem})$ and $\mathrm{se}(\hat\beta_{marrfem})$ are **not enough** — you need $\mathrm{Cov}(\hat\beta_{singfem},\hat\beta_{marrfem})$, which the output doesn't print. (Same problem as [[04 - Multiple Regression Analysis - Inference|ch. 04]] §4-4.)
>
> **The fix: re-estimate with married women as the base group.** Nothing substantive changes; the number you want is now a coefficient with its own standard error.
>
> $$\widehat{\log(wage)}=0.123+0.411\,marrmale+0.198\,singmale+0.088\,singfem+\cdots$$
> $$\qquad\qquad(0.106)\;\;(0.056)\qquad\quad(0.058)\qquad\quad(0.052)$$
>
> $t_{singfem}=0.088/0.052=\mathbf{1.69}$ — **marginal evidence**, not significance at 5%.
> $t_{marrmale}=0.411/0.056=\mathbf{7.34}$ — **married men vs married women is overwhelming.**
>
> ✓ **Check:** the new intercept $0.123=0.321-0.198$, and $0.411=0.213-(-0.198)$. **Every coefficient in the rest of the regression is unchanged.** Rebasing is a pure reparameterization.

> [!warning] The uncentered $R^2$ trap
> Include all $g$ dummies and **drop** the intercept, and there's no collinearity — but packages then compute
> $$R_0^2=1-\frac{\text{SSR}}{\text{SST}_0},\qquad \text{SST}_0=\sum_i y_i^2$$
> **uncentered** — $y_i$ is no longer measured about $\bar y$. Since $\text{SST}_0\ge\text{SST}$ (equality only if $\bar y=0$), **$R_0^2$ is inflated, often wildly.**
>
> **In this example Stata reports $R_0^2=0.948$. The correct $R^2$ is $0.461$.**
>
> $R^2$ is supposed to measure fit **relative to predicting every $y_i$ by $\bar y$** — a low bar, and the right one. Note the honest version **can be negative** without an intercept, which is probably why the uncentered one (always in $[0,1]$) is the default. **Force the centred version.**

#### 3a. Ordinal information

Credit rating $CR\in\{0,1,2,3,4\}$, explaining the municipal bond rate $MBR$.

**Option 1 — enter $CR$ directly:** $MBR=\beta_0+\beta_1 CR+\cdots$

> [!warning] This imposes a constant step
> $\beta_1$ is the change in $MBR$ per one-unit rise in $CR$ — and it forces **the 3→4 step to equal the 0→1 step.** For an ordinal variable that is an assumption, not a fact. We know 4 is better than 3; **we do not know the gaps are equal.**

**Option 2 — a dummy for each value:** with $CR=0$ as the base,
$$MBR=\beta_0+\delta_1 CR1+\delta_2 CR2+\delta_3 CR3+\delta_4 CR4+\cdots$$

**Five categories → four dummies.** Each $\delta_j$ is the difference between rating $j$ and rating 0, **and every step is allowed to differ.**

> [!important] Two different tests, two different restricted models
> | Null hypothesis | Restrictions | Restricted model |
> |---|---|---|
> | **Credit rating has no effect at all** | $\delta_1=\delta_2=\delta_3=\delta_4=0$, $q=4$ | drop all four dummies |
> | **The effect is a constant step** | $\delta_2=2\delta_1,\;\delta_3=3\delta_1,\;\delta_4=4\delta_1$, $q=3$ | $MBR$ on **$CR$ itself** |
>
> The second is the clever one. Substituting the restrictions:
> $$MBR=\beta_0+\delta_1(CR1+2CR2+3CR3+4CR4)+\cdots=\beta_0+\delta_1 CR+\cdots$$
> **The term multiplying $\delta_1$ is literally the original ordinal variable.** So the "linear in $CR$" specification *is* the restricted model, and the usual $R^2$-form $F$ statistic with $q=3$ tests whether the equal-step assumption is acceptable.

**Example 7.7 — physical attractiveness and wages** (Hamermesh & Biddle 1994; `BEAUTY`). Interviewers ranked people on five categories (homely, quite plain, average, good looking, strikingly beautiful); **the extremes were too thin, so the authors collapsed to three: below average, average (base), above average.**

**Men** ($n=700$, $R^2=0.403$): $\;-0.164\,belavg\;(0.046),\quad +0.016\,abvavg\;(0.033)$
**Women** ($n=409$, $R^2=0.330$): $\;-0.124\,belavg\;(0.066),\quad +0.035\,abvavg\;(0.049)$

| | Below average | Above average |
|---|---|---|
| **Men** | $-16.4\%$, $t=-3.57$ ✅ | $+1.6\%$, $t=0.48$ ❌ |
| **Women** | $-12.4\%$, $t=-1.88$ (marginal) | $+3.5\%$, $t=0.71$ ❌ |

> [!important] The finding is a **penalty for plainness, not a premium for beauty**
> Both "above average" effects are tiny and insignificant; both "below average" effects are large and negative. **This asymmetry is invisible if you enter looks as a single linear score** — the whole point of the dummy approach.
>
> Controls include education, experience, tenure, marital status and race.

**Example 7.8 — law school rank and salary** (`LAWSCH85`). $rank$ takes a **different value for every school**, so you cannot dummy each value. **Break it into bands** — base: ranked below 100.

$$\widehat{\log(salary)}=9.17+0.700\,top10+0.594\,r11\_25+0.375\,r26\_40+0.263\,r41\_60+0.132\,r61\_100$$
$$\qquad\qquad\;\;(0.41)\;\;(0.053)\qquad\;(0.039)\qquad\;\;(0.034)\qquad\;\;(0.028)\qquad\;\;(0.021)$$
$$\qquad\qquad+0.0057\,LSAT+0.041\,GPA+0.036\log(libvol)+0.0008\log(cost)$$
$$n=136,\quad R^2=0.911,\quad \bar R^2=0.905$$

- **All rank dummies are highly significant.** Ranked 61–100 pays about **13.2%** more than below-100.
- **Top 10 vs below 100:** $100[e^{0.700}-1]=\mathbf{101.4\%}$ — **more than double.** The approximation (70%) is badly off here, exactly as expected for a large coefficient.
- **Is the banding worth it?** $\bar R^2 = 0.905$ with bands vs **$0.836$** with $rank$ entered linearly. **Yes** ([[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3b criterion).

> [!warning] Two cautions Wooldridge flags himself
> 1. **Once rank is banded, every other variable becomes insignificant.** Joint $F$ on $LSAT$, $GPA$, $\log(libvol)$, $\log(cost)$ gives $p=0.055$ — borderline. With $rank$ entered linearly, the same joint $p$-value is **0.0000**. *The banding absorbs almost everything.* And the bands are, in Wooldridge's own words, "admittedly somewhat arbitrary."
> 2. **The random sampling assumption (MLR.2) is violated.** A school's rank **depends on the other schools in the sample** — these are not independent draws. **Not fatal** provided $u$ is uncorrelated with the regressors, but it should be stated.

---

### 4. Interactions involving dummy variables

#### 4a. Dummy × dummy

Equation (7.11) can be rewritten with `female`, `married` and their interaction:

$$\widehat{\log(wage)}=0.321-0.110\,female+0.231\,married-0.301\,female\cdot married+\cdots$$
$$\qquad\qquad(0.100)\;(0.056)\qquad\;\;(0.055)\qquad\quad(0.072)$$

**Identical regression, different parameterization.** Recover the group intercepts by plugging in zeros and ones:

| $female$ | $married$ | Intercept | Group |
|---|---|---|---|
| 0 | 0 | $0.321$ | single men (base) |
| 0 | 1 | $0.321+0.231=0.552$ | married men |
| 1 | 0 | $0.321-0.110=0.211$ | single women |
| 1 | 1 | $0.321-0.110+0.231-0.301=0.141$ | married women |

> [!important] Which parameterization? It depends on the hypothesis
> - **(7.11), four group dummies:** convenient for testing **any group against the base group** — read the $t$ straight off.
> - **(7.14), interaction form:** convenient for testing **whether the gender gap depends on marital status** (equivalently, whether the marriage premium depends on gender) — that is a single $t$ on the interaction, here $-0.301/0.072=-4.18$, **strongly significant**.
>
> **They fit identically ($R^2=0.461$ both ways). Choose the one whose coefficients are the hypotheses you care about.**

**Example 7.9 — computer use and wages** (Krueger 1993, CPS 1989, $n=13{,}379$):
$$\widehat{\log(wage)}=\hat\beta_0+0.177\,compwork+0.070\,comphome+0.017\,compwork\cdot comphome+\cdots$$
$$\qquad\qquad\qquad(0.009)\qquad\quad(0.019)\qquad\quad(0.023)$$

Base group: **uses a computer neither at work nor at home.**

| Group | Approximate | Exact |
|---|---|---|
| Work only | $17.7\%$ | $\mathbf{19.4\%}$ |
| Home only | $7.0\%$ | $7.3\%$ |
| **Both** | $0.177+0.070+0.017=26.4\%$ | $\mathbf{30.2\%}$ |

**The interaction is insignificant and economically tiny** ($t=0.74$). Wooldridge's verdict: *"it is causing little harm by being in the equation."*

#### 4b. Dummy × quantitative — different slopes

$$\log(wage)=(\beta_0+\delta_0 female)+(\beta_1+\delta_1 female)educ+u$$

which for estimation is written

$$\boxed{\;\log(wage)=\beta_0+\delta_0\,female+\beta_1 educ+\delta_1\,(female\cdot educ)+u\;}$$

| Parameter | Meaning |
|---|---|
| $\beta_0,\;\beta_1$ | intercept and slope **for men** |
| $\delta_0$ | **difference in intercepts**, women − men |
| $\delta_1$ | **difference in the return to education**, women − men |

> [!note] The interaction variable is simple to build
> $female\cdot educ$ is **0 for every man** and **equal to $educ$ for every woman**. That is all.

| Hypothesis | Statement | Test |
|---|---|---|
| Same return to education | $H_0:\delta_1=0$ | $t$ test — **allows a wage gap**, just a constant one |
| No gender difference at all | $H_0:\delta_0=0,\;\delta_1=0$ | **$F$ test** — two restrictions |

Figure 7.2 shows the two interesting cases: **(a) $\delta_0<0,\delta_1<0$** — women earn less at every education level and the gap *widens*; **(b) $\delta_0<0,\delta_1>0$** — women earn less at low education but the gap *narrows*, and eventually reverses at an education level you can solve for.

**Example 7.10** (`WAGE1`):
$$\widehat{\log(wage)}=0.389-0.227\,female+0.082\,educ-0.0056\,female\cdot educ+\cdots$$
$$\qquad\qquad(0.119)\;(0.168)\qquad\;(0.008)\qquad(0.0131)$$
$$n=526,\quad R^2=0.441$$

- Return to education: **8.2% for men, $0.082-0.0056=7.6\%$ for women.** Difference is half a percentage point, $t=-0.0056/0.0131=\mathbf{-0.43}$. **No evidence the return differs.**
- $t_{female}=-0.227/0.168=-1.35$ — **no longer significant.**

> [!warning] Concluding "there is no gender gap" here would be a serious error
> In equation (7.9), $female$ had $\hat\beta=-0.297$ with $t=-8.25$. Adding the interaction **multiplied its standard error by 4.67** ($0.168/0.036$).
>
> **Why?** $female$ and $female\cdot educ$ are **highly correlated**. And there is a concrete interpretation: **$\delta_0$ is now the gap at $educ=0$**, and almost nobody in the sample has near-zero education. **You are asking the data a question it cannot answer, and the standard error tells you so.**
>
> **The fix ([[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §2c):** replace $female\cdot educ$ with $female\cdot(educ-12.5)$, centring on the sample mean. Then $\hat\delta_0$ is **the gap at average education**, estimated precisely. **Only the $female$ coefficient and its standard error change.**
>
> **And the joint test settles it:** $F$ for $H_0:\delta_0=0,\delta_1=0$ is $\mathbf{34.33}$ on $(2,518)$ df, $p=0.0000$. **The gap is there.** Since $\delta_1$ is negligible, **the preferred model is (7.9) — a constant proportional gap.**
>
> This is the [[04 - Multiple Regression Analysis - Inference|ch. 04]] lesson again: **insignificant $t$'s + collinearity ⇒ always run the $F$.**

**Example 7.11 — race, city composition and baseball salaries** (`MLB1`, $n=330$). Base group: **white players.**

$$\widehat{\log(salary)}=10.34+\cdots-0.198\,black-0.190\,hispan+0.0125\,black\cdot percblck+0.0201\,hispan\cdot perchisp$$
$$\qquad\qquad\qquad\qquad\quad(0.125)\qquad\;(0.153)\qquad\;(0.0050)\qquad\qquad\;(0.0098)$$
$$R^2=0.638$$

**First, the joint test.** Dropping all four race variables gives $R^2=0.626$, with $q=4$ and $df=330-13=317$:
$$F=\frac{(0.638-0.626)/4}{(1-0.638)/317}=\mathbf{2.63},\qquad p=0.034$$
**Jointly significant at 5%, not at 1%.**

**Interpretation — and this is where the interaction earns its place.** The effect of being black is $-0.198+0.0125\,percblck$:

| $percblck$ | Black vs white |
|---|---|
| $0$ | $-19.8\%$ |
| $10$ | $-0.198+0.125=-7.3\%$ |
| $15.8$ | $\approx 0$ |
| $20$ | $+5.2\%$ |
| $74$ (Detroit, the max) | large positive |

For Hispanics the break-even is $0.190/0.0201=\mathbf{9.45\%}$; **12 of the 22 cities are below it.** (Max $perchisp\approx31\%$.)

> [!warning] Do not call this discrimination
> **The estimates imply whites earn *less* than minorities in heavily minority cities** — which no discrimination story predicts. A competing explanation: **player preferences** — the best black players may sort disproportionately into cities with larger black populations, and likewise for Hispanic players.
>
> **The regression establishes that a relationship exists. It cannot distinguish the two hypotheses.**

#### 4c. Testing whether two groups follow the same regression — the Chow test

To let **everything** differ between two groups, interact the group dummy with **every** regressor:

$$cumgpa=\beta_0+\delta_0 female+\beta_1 sat+\delta_1 female\!\cdot\! sat+\beta_2 hsperc+\delta_2 female\!\cdot\! hsperc+\beta_3 tothrs+\delta_3 female\!\cdot\! tothrs+u$$

$$H_0:\;\delta_0=\delta_1=\delta_2=\delta_3=0$$

**Example (`GPA3`, spring semester, $n=366$):**

$$\widehat{cumgpa}=1.48-0.353\,female+0.0011\,sat+0.00075\,female\cdot sat$$
$$\qquad\qquad(0.21)\;\;(0.411)\qquad(0.0002)\qquad(0.00039)$$
$$\qquad\qquad-0.0085\,hsperc-0.00055\,female\cdot hsperc+0.0023\,tothrs-0.00012\,female\cdot tothrs$$
$$\qquad\qquad\;(0.0014)\qquad\;(0.00316)\qquad\qquad\;(0.0009)\qquad\;\;(0.00163)$$
$$R^2=0.406,\quad \bar R^2=0.394$$

**Not one of the four interaction terms is significant** — only $female\cdot sat$ has $|t|$ near 2. But the restricted $R^2$ (drop $female$ and all interactions) is $0.352$:

$$F=\frac{(0.406-0.352)/4}{(1-0.406)/358}=\mathbf{8.14},\qquad p\approx0.00000$$

**Soundly rejected. Men and women athletes follow different GPA models** — despite every individual term being insignificant.

> [!important] The SSR form — the Chow statistic
> With many regressors, building all the interactions is tedious. **The key insight: the unrestricted SSR equals the sum of the SSRs from two separate group regressions.**
>
> $$\boxed{\;F=\frac{\text{SSR}_P-(\text{SSR}_1+\text{SSR}_2)}{\text{SSR}_1+\text{SSR}_2}\cdot\frac{n-2(k+1)}{k+1}\;}$$
>
> where $\text{SSR}_P$ is from the **pooled** regression (one equation, all observations) and $\text{SSR}_1,\text{SSR}_2$ come from the two group regressions.
>
> **`GPA3`:** $\text{SSR}_P=85.515$; women ($n_1=90$) $\text{SSR}_1=19.603$; men ($n_2=276$) $\text{SSR}_2=58.752$, so $\text{SSR}_{ur}=78.355$.
> $$F=\frac{85.515-78.355}{78.355}\cdot\frac{358}{4}=\mathbf{8.18}$$
> ✓ Matches the $R^2$ form ($8.14$) up to rounding.

> [!warning] Three limitations of the Chow test
> 1. **It is an $F$ test, so it needs homoskedasticity** — and under $H_0$ the **error variances must be equal across groups.** That is a substantive assumption, not a technicality. (Normality is not needed asymptotically.)
> 2. **The null allows *no* differences at all — usually too strong.** You almost always want to permit an intercept shift and test only the **slopes**. Two equivalent ways:
>    - Include the dummy and all interactions, then $F$-test **the interactions only** ($q=k$, not $k+1$);
>    - Use the SSR formula but let $\text{SSR}_P$ come from a pooled regression **that includes the group dummy**, and divide by $k$ instead of $k+1$.
> 3. **There is no $R^2$ form when you run separate regressions** — the two groups have different SSTs. **The $R^2$ form works only via the interaction model.**

**Applying limitation 2 to `GPA3`:** testing $H_0:\delta_1=\delta_2=\delta_3=0$ with $\delta_0$ **unrestricted** gives $p=\mathbf{0.205}$ — **not rejected even at 20%.** So the right model is an intercept shift only:

$$\widehat{cumgpa}=1.39+0.310\,female+0.0012\,sat-0.0084\,hsperc+0.0025\,tothrs$$
$$\qquad\qquad(0.18)\;\;(0.059)\qquad(0.0002)\qquad(0.0012)\qquad\;(0.0007)$$
$$n=366,\quad R^2=0.398,\quad \bar R^2=0.392$$

**Now $female$ has $t>5$: female athletes have a predicted GPA 0.31 points higher** — practically important, and completely invisible in the fully interacted model.

> [!warning] The most instructive number in this chapter
> In the fully-interacted equation (7.22), the coefficient on $female$ is $\mathbf{-0.353}$. **Reading that as "women score 0.35 lower" is wrong** — it is the difference when $sat=hsperc=tothrs=0$, which is not a possible student.
>
> **At realistic values** $sat=1100$, $hsperc=10$, $tothrs=50$:
> $$-0.353+0.00075(1100)-0.00055(10)-0.00012(50)=\mathbf{+0.461}$$
>
> **The sign flips.** A female athlete is predicted to score nearly half a grade point *higher*. **Whenever interactions are present, the level coefficient is not the effect — you must plug in real values.**

---

### 5. A binary **dependent** variable: the linear probability model

Now $y$ itself is 0/1: employed or not, arrested or not, approved or not.

$$y=\beta_0+\beta_1x_1+\cdots+\beta_kx_k+u$$

$\beta_j$ cannot be "the change in $y$" — $y$ only jumps between 0 and 1. **But under MLR.4, $\mathbb{E}(y\mid\mathbf{x})=\beta_0+\beta_1x_1+\cdots$, and for a 0/1 variable**

$$\boxed{\;P(y=1\mid\mathbf{x})=\mathbb{E}(y\mid\mathbf{x})=\beta_0+\beta_1x_1+\cdots+\beta_kx_k\;}$$

$$\Longrightarrow\quad \Delta P(y=1\mid\mathbf{x})=\beta_j\,\Delta x_j$$

**This is the linear probability model (LPM).** $\hat y$ is a **predicted probability**; $\hat\beta_j$ is the **change in the probability of success** per unit of $x_j$. The mechanics of OLS are unchanged.

> [!tip] Name the dependent variable after the event $y=1$
> `inlf`, `arr86`, `approved` — you must know what counts as "success" to read the sign.

#### Example — labour force participation (`MROZ`, 1975, $n=753$, 428 in the labour force)

$$\widehat{inlf}=0.586-0.0034\,nwifeinc+0.038\,educ+0.039\,exper-0.00060\,exper^2-0.016\,age-0.262\,kidslt6+0.013\,kidsge6$$
$$\qquad\;(0.154)\;(0.0014)\qquad\quad(0.007)\qquad(0.006)\qquad(0.00018)\qquad(0.002)\qquad(0.034)\qquad\;(0.013)$$
$$R^2=0.264$$

- **$educ$:** another year raises the participation probability by **0.038**. Ten more years $\Rightarrow$ $+0.38$ — enormous.
- **$nwifeinc$:** $+\$10{,}000$ of husband's income lowers it by **0.034** — modest for 1975 dollars.
- **$kidslt6$:** one more child under six lowers it by **0.262**. Huge. (Just under 20% of the women have at least one.)
- **$exper$** enters as a quadratic: effect $=0.039-0.0012\,exper$, zero at $0.039/0.0012=\mathbf{32.5}$ years — only **13 of 753** women exceed that.

**Figure 7.3 reconstructed.** Fix $nwifeinc=50$, $exper=5$, $age=30$, $kidslt6=1$, $kidsge6=0$:
$$0.586-0.17+0.195-0.015-0.48-0.262 = \mathbf{-0.146}$$
$$\widehat{inlf}=-0.146+0.038\,educ$$

- Predicted probability is **negative below $educ=0.146/0.038=3.84$ years** — but **no woman in the sample has under 5 years**.
- At the sample maximum $educ=17$: $-0.146+0.646=\mathbf{0.50}$ exactly.
- **The marginal effect is 0.038 everywhere, whatever the other variables are set to.**

#### The four drawbacks of the LPM

> [!warning] 1. Fitted probabilities can fall outside $[0,1]$
> In `MROZ`, **16 fitted values are below 0 and 17 are above 1** — 33 of 753, about **4.4%**. Embarrassing but usually survivable.

> [!warning] 2. Constant marginal effects are implausible at the extremes
> The model says going from 0 to 1 young children costs $0.262$ of probability — **and so does going from 1 to 2, and 3 to 4.** Realistically the *first* child should matter most.
>
> Taken literally, 0 → 4 young children changes the probability by $0.262\times4=\mathbf{1.048}$. **A probability cannot change by more than 1.** The model is simply false out there.
>
> **But:** no woman in the sample has four young children, only three have three, and **over 96% have zero or one.** **The LPM works well near the middle of the data**, which is where the estimates are actually being used.

> [!important] 3. Heteroskedasticity is **built in** — this one is unavoidable
> For a Bernoulli variable,
> $$\boxed{\;\mathrm{Var}(y\mid\mathbf{x})=p(\mathbf{x})\left[1-p(\mathbf{x})\right]\;}$$
> and $p(\mathbf{x})$ depends on $\mathbf{x}$. **So MLR.5 fails by construction**, unless the probability doesn't depend on any regressor.
>
> | | Consequence |
> |---|---|
> | Bias | **None** — [[03 - Multiple Regression Analysis - Estimation|ch. 03]] unbiasedness needs only MLR.1–4 |
> | Efficiency | **Not BLUE** |
> | Standard errors, $t$, $F$ | **Invalid — and not rescued by large $n$** ([[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]]) |
>
> **The standard errors printed above are not generally valid.** [[08 - Heteroskedasticity|Chapter 08]] fixes this with robust standard errors. **In practice the usual OLS statistics are often not far off, and a standard OLS analysis of an LPM remains acceptable in applied work** — but robust errors cost nothing and should be the default.

> [!note] 4. Goodness of fit — use *percent correctly predicted*
> $R^2$ means little here. Instead define $\tilde y_i=1$ if $\hat y_i\ge0.5$ and $\tilde y_i=0$ otherwise, then report **the proportion of observations with $\tilde y_i=y_i$** — separately for $y_i=1$ and $y_i=0$, and overall. (Developed further in Wooldridge ch. 17.)

#### Example 7.12 — an LPM of arrests (`CRIME1`, $n=2{,}725$)

$$\widehat{arr86}=0.441-0.162\,pcnv+0.0061\,avgsen-0.0023\,tottime-0.022\,ptime86-0.043\,qemp86$$
$$\qquad\;\;(0.017)\;(0.021)\qquad(0.0065)\qquad\;(0.0050)\qquad\;(0.005)\qquad\;(0.005)$$
$$R^2=0.0474$$

(27.7% of the men were arrested at least once in 1986; only 7.2% more than once — which is why a binary $y$ is reasonable.)

- **Intercept $0.441$** = predicted arrest probability for a man never convicted, never imprisoned, unemployed all year.
- **$pcnv$** runs 0 to 1, so its coefficient spans the *entire* range: going from "never convicted" to "always convicted" cuts the probability by only $0.162$. A rise of $0.5$ cuts it by $0.081$.
- **$avgsen$ and $tottime$ are individually and jointly insignificant** ($F$ gives $p=0.347$), and $avgsen$ has the **wrong sign** for a deterrence story. Grogger (1991) argues $tottime$ measures **human capital built up in criminal activity**.
- **Incarceration effect:** six more months in prison lowers the probability by $0.022\times6=0.132$.
- **Employment:** all four quarters employed $\Rightarrow$ $0.043\times4=\mathbf{0.172}$ less likely to be arrested.

> [!warning] Where the LPM visibly breaks
> A man in prison **all 12 months of 1986 cannot be arrested in 1986** — the true probability is exactly 0. The model, with everything else at zero, predicts
> $$0.441-0.022(12)=\mathbf{0.177}$$
> **Not zero.** Starting instead from the unconditional rate $0.277$: $0.277-0.264=\mathbf{0.013}$ — essentially zero. **Whether the LPM looks broken depends on where you start.** That is exactly the "works near the middle of the data" caveat.

**Adding race dummies** (base: white):
$$\widehat{arr86}=0.380-0.152\,pcnv+\cdots+0.170\,black+0.096\,hispan,\qquad R^2=0.0682$$
$$\qquad\qquad\qquad\qquad\qquad\qquad\quad(0.024)\qquad\;(0.021)$$

**A black man's arrest probability is 17 percentage points higher than a white man's, all else equal; a Hispanic man's is 9.6 points higher.** Both significant.

> [!warning] "Percentage points", not "percent"
> $0.170$ is a **17 percentage point** difference in probability. If the white baseline is $0.28$, that is a *relative* increase of about 60%. **The two statements are wildly different numbers and both appear in policy writing.** (Same distinction as [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §2a.)

---

### 6. Policy analysis and program evaluation

**The control group** does not receive the program; the **treatment group** does. **Except in rare cases the assignment is not random**, so a raw difference in means confounds the program with whatever made people take it.

**Example — training grants and productivity** (`JTRAIN` 1988, $n=50$, 17 firms received grants):
$$\widehat{\log(scrap)}=4.99-0.052\,grant-0.455\log(sales)+0.639\log(employ),\quad R^2=0.072$$
$$\qquad\qquad(4.66)\;(0.431)\qquad\;(0.373)\qquad\qquad(0.365)$$

Grant firms have scrap rates about **5.2% lower** — right sign, but $t=-0.12$. **From this cross-section, no effect.**

> [!warning] "First come, first served" is not random
> Holzer et al. note grants were awarded first-come-first-served. **That is not randomization.** Firms with *less* productive workers may have seen more upside and applied harder — which biases the estimate toward finding no benefit. **Chapter 9 adds a prior year of data and reaches a very different conclusion.**

**Testing for discrimination in lending:**
$$approved=\beta_0+\beta_1 nonwhite+\beta_2 income+\beta_3 wealth+\beta_4 credrate+\cdots$$

> [!important] Race is exogenous — and that is not enough
> Race is determined at birth, so it looks like the perfect exogenous regressor. **But for historical reasons race is correlated with income, wealth and credit history**, all of which legitimately affect approval. **Testing $H_0:\beta_1=0$ against $\beta_1<0$ is only meaningful once those are controlled for.**

#### 6a. Regression adjustment, restricted and unrestricted

Let $w$ be the binary treatment and $x_1,\dots,x_k$ the **covariates**. Under **unconfoundedness / ignorability**,

$$w \perp [y(0),y(1)] \;\;\Big|\;\; \mathbf{x}$$

— *conditional on the covariates, participation is as good as random.* This is the assumption that licenses everything below, and it is **untestable**.

> [!note] The self-selection problem
> Head Start participation depends on **parental decisions**, which also predict child outcomes. Drug use, gun-control laws chosen by states, hospitals choosing for-profit status — **all self-selected**. "Self" is used broadly: cities and firms select too.

| | Regression | Estimator |
|---|---|---|
| **Restricted RA (RRA)** | $y_i$ on $w_i,\;x_{i1},\dots,x_{ik}$ | $\hat\tau_{rra}$ — the coefficient on $w_i$ |
| **Unrestricted RA (URA)** | $y_i$ on $w_i,\;x_{i1},\dots,x_{ik},\;w_i(x_{i1}-\bar x_1),\dots,w_i(x_{ik}-\bar x_k)$ | $\hat\tau_{ura}$ — the coefficient on $w_i$ |

RRA imposes a **constant treatment effect**. URA lets the effect vary with the covariates: $\hat\delta_j$ on the interaction tells you how the effect changes with $x_j$.

> [!important] You *must* demean the $x_j$ inside the interactions
> Otherwise the coefficient on $w_i$ is the treatment effect **at $\mathbf{x}=\mathbf{0}$**, not the **average treatment effect**. (Exactly the §4b trap.) The $x_j$ entering **on their own** need not be demeaned — that only shifts the intercept.

**Example 7.13 — job training** (`JTRAIN98`, $n=1{,}130$; $y=earn98$ in \$000s, $w=train$):

| Estimator | $\hat\tau$ | se |
|---|---|---|
| Difference in means | $-2.05$ | $0.48$ |
| **Restricted RA** | $+2.44$ | $0.44$ |
| **Unrestricted RA** | $+3.11$ | $0.53$ |

$$\widehat{earn98}=5.08+3.11\,train+0.353\,earn96+0.378\,educ-0.196\,age+2.76\,married$$
$$\qquad\qquad(1.39)\;(0.53)\qquad\;(0.020)\qquad\;(0.078)\qquad(0.023)\qquad(0.55)$$
$$\qquad\quad+0.133\,train(earn96-\overline{earn96})-0.035\,train(educ-\overline{educ})$$
$$\qquad\quad+0.058\,train(age-\overline{age})-0.993\,train(married-\overline{married})$$
$$R^2=0.409$$

> [!important] The sign flip is the entire lesson
> **The raw difference in means says training *reduced* earnings by \$2,050.** Adding covariates flips it to **+\$2,440**, and the unrestricted version to **+\$3,110** ($t=5.87$).
>
> **Trainees were systematically worse off to begin with** — lower $earn96$, and so on. Without adjusting for that, the program looks harmful.
>
> The interactions are **not jointly significant** ($p\approx0.113$), so RRA would be defensible here — but the URA point estimate is notably higher.

> [!tip] URA computed the counterfactual way — and why it's the same number
> 1. Regress $y$ on $\mathbf{x}$ using **only controls** ($w_i=0$) → $\hat\alpha_0,\hat\gamma_{0,j}$.
> 2. Regress $y$ on $\mathbf{x}$ using **only treated** ($w_i=1$) → $\hat\alpha_1,\hat\gamma_{1,j}$.
> 3. For **every** unit $i$ — treated or not — predict **both** counterfactuals $\hat y_i^{(0)}$ and $\hat y_i^{(1)}$.
> 4. $$\widehat{ATE}=n^{-1}\sum_i\left[\hat y_i^{(1)}-\hat y_i^{(0)}\right]=(\hat\alpha_1-\hat\alpha_0)+(\hat\gamma_{1,1}-\hat\gamma_{0,1})\bar x_1+\cdots$$
>
> **Algebraically identical to the coefficient on $w_i$ in the URA regression.** Same structure as the Chow test (§4c): a fully interacted model *is* two separate regressions.
>
> **Practical advice: run regression (7.42).** The two-regression route makes a correct standard error hard to compute by hand; the interacted regression **always produces a valid one.** And you get the Chow-style $F$ test on the interactions for free.

> [!warning] None of this rescues you from bad covariates
> **Currie & Cole (1993):** even with rich family and background controls, OLS says AFDC participation **lowers birth weight** — which is very hard to believe. Using instrumental variables (Wooldridge ch. 15) they find **no effect or a positive effect.**
>
> **With observational data, the chance of a spurious effect in either direction is high even with a rich set of $x_j$.** Unconfoundedness cannot be tested. When it fails, you need panel data or IV — chapters outside this scope.

---

### 7. Interpreting results when $y$ is discrete but quantitative

Number of children, number of arrests — small non-negative integers, often with many zeros.

$$\widehat{children}=-1.997+0.175\,age-0.090\,educ,\qquad n=4{,}361,\;R^2=0.560$$
$$\qquad\qquad\;(0.094)\;\;(0.003)\qquad(0.006)$$

> [!important] "0.090 fewer children" is nonsense for one woman and correct for the average
> **Read every OLS coefficient as an effect on $\mathbb{E}(y\mid\mathbf{x})$.** Under MLR.1 and MLR.4 that is exactly what OLS estimates ([[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §4a).
>
> **The clean way to say it: if each woman in a group of 100 got one more year of education, we estimate there would be about 9 fewer children among them.**

Dummies work the same way:
$$\widehat{children}=-2.071+0.177\,age-0.079\,educ-0.362\,electric,\qquad n=4{,}358,\;R^2=0.562$$
$$\qquad\qquad\;\;(0.095)\;\;(0.003)\qquad(0.006)\qquad\;\;(0.068)$$

**Comparing 100 women with electricity to 100 without, at the same age and education, we estimate about 36 fewer children in the first group.**

> [!note] When the linear model is not enough
> For limited-range $y$, the linear model is an approximation — often a good one for average partial effects, but Wooldridge ch. 17 (Poisson, Tobit, logit/probit) fits better. **Outside this scope, but worth knowing it exists.**

---

## ✏️ Exercises

### Exercise 1 — Base groups, the dummy trap, and exact percentages

A firm's HR analyst estimates, on $n=650$ employees,
$$\widehat{\log(salary)}=6.20-0.184\,female+0.075\,educ+0.019\,exper,\qquad R^2=0.412$$

**(a)** Interpret $-0.184$ approximately and exactly. Which do you report?
**(b)** Rewrite the equation with **women** as the base group. Give the new intercept and the new coefficient.
**(c)** The analyst adds a `male` dummy alongside `female`. What happens, and why?
**(d)** She instead drops the intercept and keeps both dummies. Is that legal? What goes wrong?
**(e)** A colleague objects that the coefficient can't be a "gender gap" because it doesn't control for job level. Is he right?

> [!example]- Solution
> **(a)** Approximately, a woman earns **18.4% less** than a man with the same education and experience.
>
> Exactly, using $100[\exp(\hat\beta)-1]$:
> $$\text{women vs men: } 100[e^{-0.184}-1]=\mathbf{-16.8\%}$$
> $$\text{men vs women: } 100[e^{+0.184}-1]=\mathbf{+20.2\%}$$
>
> **Report the approximation, 18.4%.** It lies between the two exact figures ($16.8<18.4<20.2$), so it does not require choosing a base group. Quote an exact figure only when the question names a direction — *"how much less does a woman earn?"* → 16.8%.
>
> **(b)** $\alpha_0=\beta_0+\delta_0=6.20-0.184=\mathbf{6.016}$ and $\gamma_0=-\delta_0=\mathbf{+0.184}$:
> $$\widehat{\log(salary)}=6.016+0.184\,male+0.075\,educ+0.019\,exper$$
>
> **$R^2$, all other coefficients, all other standard errors, SSR and $\hat\sigma$ are unchanged.** $\mathrm{se}(\hat\gamma_0)=\mathrm{se}(\hat\delta_0)$ too, since $\gamma_0=-\delta_0$. **Rebasing is a pure reparameterization — nothing substantive can change.**
>
> **(c) Perfect collinearity — the dummy variable trap.** $female+male=1$, which is exactly the intercept's regressor. **MLR.3 fails and OLS is not computable.** Some packages silently drop one variable; others error. **Prefer the error** — being forced to choose the base group is how you avoid misreading the output.
>
> **With $g$ groups you need $g$ intercepts. The overall intercept supplies one, so you add $g-1$ dummies.**
>
> **(d) Legal — there is no trap without an overall intercept.** Each coefficient is now a group intercept directly: $6.016$ for women, $6.20$ for men. **Two things go wrong:**
> 1. **Testing the difference is now awkward.** $H_0$: no gap is $H_0:\beta_{male}=\beta_{female}$, a linear-combination test needing $\mathrm{Cov}(\hat\beta_{male},\hat\beta_{female})$ — not a coefficient you can read off. With one dummy plus an intercept it is a single $t$.
> 2. **The reported $R^2$ becomes the uncentered $R_0^2=1-\text{SSR}/\sum y_i^2$**, which is **inflated**, because $\sum y_i^2\ge\sum(y_i-\bar y)^2$. In Wooldridge's wage example the same model reports $0.948$ uncentered versus a true $0.461$. **Force the centred version, or keep the intercept.**
>
> **(e) He is half right, and the half he is wrong about matters more.**
>
> **Right that** $-0.184$ is not "the effect of being female holding job level fixed." It holds only education and experience fixed.
>
> **Wrong that this makes it uninterpretable.** It is exactly what it claims: **the pay gap between men and women with the same schooling and experience.** Whether to add job level is a **substantive** decision, not an automatic improvement — and [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §3d says why. **If women are systematically assigned to lower-paying job levels, then job level is a *channel* of the effect**, and controlling for it shuts that channel off, measuring only *within-level* pay differences. That is a different (and narrower) question.
>
> **The right response is Betts's:** report the regression **both ways** and say what each one means.

---

### Exercise 2 — Four groups, and the difference you cannot test

Take equation (7.11), base group **single men**:

| Variable | Coefficient | se |
|---|---|---|
| intercept | $0.321$ | $0.100$ |
| $marrmale$ | $0.213$ | $0.055$ |
| $marrfem$ | $-0.198$ | $0.058$ |
| $singfem$ | $-0.110$ | $0.056$ |

**(a)** How many dummies for four groups, and why not four?
**(b)** Give the estimated proportionate difference between **married men and married women**, approximately and exactly.
**(c)** Give the difference between **single and married women**. Can you test whether it is significantly different from zero using the table above? If not, what do you do?
**(d)** Someone re-estimates with married women as the base and gets an intercept of $0.123$ and $0.411$ on $marrmale$. Verify both from the table above.
**(e)** A researcher instead runs the additive model with $female$ and $married$ entered separately and gets a marriage premium of $0.053$ (se $0.041$), $t=1.29$, and concludes marriage has no effect on wages. Critique.

> [!example]- Solution
> **(a) Three dummies.** $g=4$ groups need $4$ intercepts; the overall intercept supplies the base group's, so $g-1=3$ dummies. **Adding a fourth (`singmale`) gives $marrmale+marrfem+singfem+singmale=1$ — perfect collinearity with the intercept: the dummy variable trap.**
>
> **(b)** Both are measured against the same base, so the intercept cancels:
> $$0.213-(-0.198)=\mathbf{0.411}$$
> **Approximately 41.1% more.** Exactly: $100[e^{0.411}-1]=\mathbf{50.8\%}$.
>
> **The coefficient is large enough that the correction is worth 10 percentage points — do not skip it here.**
>
> **(c)** $$-0.110-(-0.198)=\mathbf{+0.088}\quad\Rightarrow\quad\text{single women earn about }8.8\%\text{ more than married women}$$
> (Exactly $100[e^{0.088}-1]=9.2\%$.)
>
> **No, you cannot test it from this table.** The estimator of the difference is $\hat\beta_{singfem}-\hat\beta_{marrfem}$, whose variance is
> $$\mathrm{Var}(\hat\beta_{singfem})+\mathrm{Var}(\hat\beta_{marrfem})-2\,\mathrm{Cov}(\hat\beta_{singfem},\hat\beta_{marrfem})$$
> **The covariance is not reported**, and it is not negligible — dummy coefficients sharing a base group are strongly correlated.
>
> **What to do: re-estimate with married women as the base group.** The quantity you want becomes a coefficient with its own standard error. Result: $0.088$ with $\mathrm{se}=0.052$, so
> $$t=\frac{0.088}{0.052}=\mathbf{1.69}$$
> **Marginal evidence — not significant at 5% two-sided** (critical value $\approx1.96$). Significant at 10% one-sided, but choosing one-sided after seeing the sign is exactly the [[04 - Multiple Regression Analysis - Inference|ch. 04]] sin.
>
> **(Alternative: the [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §4a recentring trick, or an $F$ test of the single restriction $\beta_{singfem}=\beta_{marrfem}$. All three give the same answer; rebasing is the least error-prone.)**
>
> **(d)** ✓ Both check out:
> $$\text{new intercept}=0.321+(-0.198)=\mathbf{0.123}$$
> $$\text{new }marrmale=0.213-(-0.198)=\mathbf{0.411}$$
> **The old intercept plus the new base group's coefficient gives the new intercept; every other coefficient shifts by the same amount.** And $t=0.411/0.056=7.34$ — **the married-men vs married-women gap is overwhelming.**
>
> **Everything outside the four-group block ($educ$, $exper$, $tenure$ and their squares) is bit-for-bit identical**, as is $R^2=0.461$. If it isn't, you built the dummies wrong.
>
> **(e) The conclusion is wrong because the additive model asks the wrong question.**
>
> $female+married$ without an interaction **forces the marriage premium to be identical for men and women.** From (7.11) it is not:
>
> | | Married vs single, same sex |
> |---|---|
> | **Men** | $+0.213$ |
> | **Women** | $-0.198-(-0.110)=\mathbf{-0.088}$ |
>
> **Marriage is worth about +21% to a man and about −9% to a woman.** The additive model averages these into $+0.053$ — a number describing neither group.
>
> **And the interaction is emphatically significant.** In the equivalent form (7.14), $\hat\beta_{female\cdot married}=-0.301$ with se $0.072$, giving $t=\mathbf{-4.18}$.
>
> **The correct statement:** *"There is a large marriage premium for men and a marriage penalty for women, and the difference between them is highly significant."* The insignificant $0.053$ is an artefact of a restriction the data reject.

---

### Exercise 3 — Ordinal information and two different $F$ tests

A city's bond rate $MBR$ is modelled with credit rating $CR\in\{0,1,2,3,4\}$ and **six** other controls, $n=200$.

**(a)** Why is entering $CR$ as a single regressor unattractive?
**(b)** Set up the dummy-variable model. How many dummies, and what is the base group?
**(c)** State the null "credit rating has no effect on $MBR$" and give $q$.
**(d)** State the null "each one-step improvement in rating has the same effect" as restrictions on the $\delta_j$. Show that the **restricted model is the one that enters $CR$ linearly**.
**(e)** The unrestricted model gives $R^2=0.372$. Dropping the four dummies gives $R^2=0.301$. Entering $CR$ linearly gives $R^2=0.349$. Carry out both tests at the 5% level and state the conclusion.

> [!example]- Solution
> **(a)** $CR$ is **ordinal**: we know $4\succ3\succ2\succ1\succ0$, but **not that the gaps are equal**. Entering $CR$ linearly forces $\beta_1$ to be the effect of *every* one-step improvement, so the 3→4 step is assumed identical to the 0→1 step. **That is an untested restriction masquerading as a specification**, and there is no reason to expect it to hold for a rating scale.
>
> **(b)** Five categories $\Rightarrow$ **four dummies**, base group $CR=0$ (worst rating):
> $$MBR=\beta_0+\delta_1 CR1+\delta_2 CR2+\delta_3 CR3+\delta_4 CR4+(\text{6 controls})+u$$
> $\delta_j$ is the difference in $MBR$ between rating $j$ and rating 0, **with each step free to differ**. Unrestricted $k=4+6=10$, so $df=200-11=\mathbf{189}$.
>
> **(c)** $$H_0:\;\delta_1=\delta_2=\delta_3=\delta_4=0,\qquad q=\mathbf{4}$$
> Restricted model: drop all four dummies, keep the six controls.
>
> **(d)** A constant per-step effect $\delta_1$ means rating $j$ is $j\delta_1$ better than rating 0:
> $$H_0:\;\delta_2=2\delta_1,\quad \delta_3=3\delta_1,\quad \delta_4=4\delta_1,\qquad q=\mathbf{3}$$
> Substituting into the model:
> $$\delta_1 CR1+2\delta_1 CR2+3\delta_1 CR3+4\delta_1 CR4=\delta_1\left(CR1+2CR2+3CR3+4CR4\right)$$
> For any observation **exactly one** dummy is 1 (or none, if $CR=0$), so the bracket equals $CR$ itself. Hence
> $$MBR=\beta_0+\delta_1 CR+(\text{6 controls})+u$$
> **The linear-in-$CR$ specification *is* the restricted model.** No special software needed: run it, take its $R^2$, and use the ordinary $R^2$-form $F$.
>
> **(e)** Both use $F=\dfrac{(R^2_{ur}-R^2_r)/q}{(1-R^2_{ur})/189}$ with $R^2_{ur}=0.372$.
>
> **Test 1 — no effect at all** ($q=4$, $R^2_r=0.301$):
> $$F=\frac{(0.372-0.301)/4}{(1-0.372)/189}=\frac{0.017750}{0.0033228}=\mathbf{5.34}$$
> Critical value $F_{4,189}$ at 5% is $\mathbf{2.42}$; $p=\mathbf{0.0004}$. **Reject decisively — credit rating matters.**
>
> **Test 2 — constant step** ($q=3$, $R^2_r=0.349$):
> $$F=\frac{(0.372-0.349)/3}{(1-0.372)/189}=\frac{0.0076667}{0.0033228}=\mathbf{2.31}$$
> Critical value $F_{3,189}$ at 5% is $\mathbf{2.65}$; $p=\mathbf{0.078}$. **Do not reject at 5%** (but do at 10%).
>
> **Conclusion.** Credit rating has a strong effect. The evidence that the steps are *unequal* is **borderline** — significant at 10%, not at 5%.
>
> **What to actually do:** report the **dummy** specification. Three reasons:
> 1. **It nests the linear one**, so nothing is lost, and the estimated $\hat\delta_j$ show you *where* the non-linearity sits.
> 2. **A $p$-value of 0.078 is not a licence to impose the restriction** — failing to reject is not evidence for $H_0$, especially with $n=200$ and four dummies competing for variation ([[04 - Multiple Regression Analysis - Inference|ch. 04]]).
> 3. Four extra parameters out of 200 observations is cheap.
>
> **Impose the linear form only if the pattern of $\hat\delta_j$ genuinely looks proportional**, or if you need the parsimony for prediction.

---

### Exercise 4 — The Chow test, two ways

From `GPA3` ($n=366$, $k=3$: $sat$, $hsperc$, $tothrs$):

| Regression | SSR | $n$ |
|---|---|---|
| Pooled (one equation, no group terms) | $85.515$ | $366$ |
| Women only | $19.603$ | $90$ |
| Men only | $58.752$ | $276$ |

Also: fully interacted $R^2_{ur}=0.406$; pooled $R^2_r=0.352$.

**(a)** Compute the Chow statistic from the SSRs. State $q$ and the df.
**(b)** Compute it from the $R^2$s. Why do the two differ slightly?
**(c)** Why is there no $R^2$ form available if you only ran the two separate regressions?
**(d)** State the assumption the Chow test needs that a $t$ test on a single dummy does **not** obviously need.
**(e)** In the fully interacted model the coefficient on $female$ is $-0.353$, and none of the four female terms is individually significant. Yet the joint test rejects overwhelmingly, and the intercept-shift-only model gives $+0.310$ on $female$ with $t>5$. Reconcile all three facts, and compute the predicted male–female difference at $sat=1100$, $hsperc=10$, $tothrs=50$.

> [!example]- Solution
> **(a)** $\text{SSR}_{ur}=\text{SSR}_1+\text{SSR}_2=19.603+58.752=\mathbf{78.355}$.
>
> $$F=\frac{\text{SSR}_P-\text{SSR}_{ur}}{\text{SSR}_{ur}}\cdot\frac{n-2(k+1)}{k+1}=\frac{85.515-78.355}{78.355}\cdot\frac{366-8}{4}=\frac{7.160}{78.355}\cdot 89.5=\mathbf{8.18}$$
>
> $q=k+1=\mathbf{4}$ restrictions (intercept plus three slopes); denominator $df=n-2(k+1)=\mathbf{358}$. Critical value $F_{4,358}$ at 5% is $\mathbf{2.40}$. **Reject decisively.**
>
> **(b)** $$F=\frac{(0.406-0.352)/4}{(1-0.406)/358}=\frac{0.013500}{0.0016592}=\mathbf{8.14}$$
>
> **The two differ only by rounding.** $R^2$ is reported to three decimals; $0.406$ and $0.352$ each carry up to $0.0005$ of slack, and the numerator is a *difference* of two such numbers, so the relative error is amplified. **The SSR form (8.18) is the more accurate of the two** because SSRs are reported to more significant figures. Substantively identical.
>
> **(c) Because the two group regressions have different SSTs.**
>
> The $R^2$ form of the $F$ statistic is derived by dividing numerator and denominator by a **common** SST — legitimate only when both models explain the same $y_i$ over the same observations. Women's SST and men's SST are different numbers, and there is no meaningful way to combine $R^2_1$ and $R^2_2$ into "the unrestricted $R^2$."
>
> **SSRs, by contrast, add.** $\text{SSR}_1+\text{SSR}_2$ *is* the SSR of the fully interacted model, exactly. So:
> - **Two separate regressions ⇒ SSR form only.**
> - **Interaction model ⇒ either form.**
>
> **(d) Equal error variances across the two groups.** The Chow test is an $F$ test, so it requires **homoskedasticity** — and here that means $\mathrm{Var}(u\mid\mathbf{x})$ must be the same for men and women *under the null*. If male and female GPAs have genuinely different residual variances, the Chow statistic is invalid **even in large samples** ([[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]]: asymptotics does not rescue you from heteroskedasticity).
>
> This is easy to overlook because the null is usually phrased purely about the *means*. **The comparison-of-means $t$ test in Example 7.1 needs exactly the same assumption**, and for exactly the same reason — it *is* an OLS $t$ test. **The robust versions of [[08 - Heteroskedasticity|ch. 08]] remove the assumption in both cases.**
>
> **(e) All three are consistent, and the resolution is the [[06 - Multiple Regression Analysis - Further Issues|ch. 06]] §2c trap plus the [[04 - Multiple Regression Analysis - Inference|ch. 04]] collinearity trap.**
>
> 1. **$-0.353$ is not the gender difference.** In a model where $female$ is interacted with $sat$, $hsperc$ and $tothrs$, the coefficient on $female$ is the difference **when all three are zero** — a student with an SAT of 0, top of their high school class, and no college hours. **No such student exists.**
>
> 2. **The individual $t$'s are insignificant because of collinearity, not because of absence of effect.** $female$, $female\cdot sat$, $female\cdot hsperc$ and $female\cdot tothrs$ are heavily correlated with each other, so each standard error is inflated — the [[03 - Multiple Regression Analysis - Estimation|ch. 03]] variance formula with $R_j^2$ near 1. **The joint $F$ of 8.18 is the correct test and it rejects.**
>
> 3. **$+0.310$ with $t>5$ in the restricted model is the trustworthy estimate**, because a separate $F$ test of $H_0:\delta_1=\delta_2=\delta_3=0$ (slopes only, intercept unrestricted) gives $p=0.205$ — **the slopes genuinely do not differ**, so the intercept-shift model is the right specification and estimates the one real difference precisely.
>
> **At realistic values:**
> $$-0.353+0.00075(1100)-0.00055(10)-0.00012(50)$$
> $$=-0.353+0.825-0.0055-0.006=\mathbf{+0.461}$$
>
> **The sign flips: a female athlete is predicted to score about 0.46 points *higher*** — comfortably in line with the $+0.310$ from the restricted model, and the opposite of what $-0.353$ appears to say.
>
> **The lesson in one line: with interactions in the model, no level coefficient is an effect until you plug in real values.**

---

### Exercise 5 — The linear probability model

From the `MROZ` labour force participation equation (§5), with $\widehat{inlf}$ as given.

**(a)** Interpret the coefficients on $educ$ and $kidslt6$ precisely.
**(b)** Fix $nwifeinc=50$, $exper=5$, $age=30$, $kidslt6=1$, $kidsge6=0$. Reduce the equation to a function of $educ$ alone. Find where the predicted probability is 0 and where it is 0.5. Should the negative region worry you?
**(c)** What does the model predict for a woman who goes from 0 to 4 children under six? Why is this fatal in principle and tolerable in practice?
**(d)** Derive $\mathrm{Var}(y\mid\mathbf{x})$ for a binary $y$, and evaluate it at $p=0.5$ and $p=0.1$. Which OLS properties survive and which do not? Does a large sample help?
**(e)** How would you report goodness of fit here?

> [!example]- Solution
> **(a)** $$\hat\beta_{educ}=0.038:\;\text{one more year of schooling raises the \textbf{probability} of being in the labour force by }\mathbf{0.038}$$
> — i.e. **3.8 percentage points**, holding husband's income, experience, age and children fixed. Ten more years would raise it by $0.38$, which is enormous and a hint that the linear form is strained over that range.
>
> $$\hat\beta_{kidslt6}=-0.262:\;\text{each additional child under six lowers the probability by }\mathbf{0.262}$$
> — **26.2 percentage points**, by far the largest effect in the equation.
>
> > **Say "percentage points," not "percent."** If the baseline probability is $0.5$, a fall of $0.262$ is a **52% relative** decline. Both numbers are correct and they are not the same statement.
>
> **(b)** Collect the constant:
> $$0.586-0.0034(50)+0.039(5)-0.00060(25)-0.016(30)-0.262(1)+0.013(0)$$
> $$=0.586-0.170+0.195-0.015-0.480-0.262=\mathbf{-0.146}$$
> $$\boxed{\widehat{inlf}=-0.146+0.038\,educ}$$
>
> | Question | Answer |
> |---|---|
> | $\widehat{inlf}=0$ | $educ=0.146/0.038=\mathbf{3.84}$ years |
> | $\widehat{inlf}=0.5$ | $educ=(0.5+0.146)/0.038=\mathbf{17.0}$ years |
> | $\widehat{inlf}$ at $educ=12$ | $\mathbf{0.31}$ |
>
> **The negative region should not worry us much here.** **No woman in the sample has fewer than five years of education**, so the offending range is outside the data — extrapolation, not a fit failure. And the largest reported education, 17 years, lands exactly at $0.50$.
>
> **But note what is fixed to get this line:** husband earning \$50,000 (1975!) and a child under six. **Set the other variables differently and the whole line shifts** — the range of predicted probabilities changes completely. **What does *not* change is the slope: $0.038$ per year of education, everywhere, always.** That constancy is the LPM's defining simplification.
>
> **(c)** $$\Delta\widehat{inlf}=-0.262\times4=\mathbf{-1.048}$$
>
> **A probability cannot change by more than 1.** The model is not merely inaccurate here — it is **logically impossible**.
>
> **Fatal in principle** because the LPM imposes a **constant marginal effect** on a quantity bounded in $[0,1]$; extend any non-zero slope far enough and it must leave the interval. Realistically the *first* young child should matter most and later ones less — **the LPM cannot represent diminishing effects on a probability at all.**
>
> **Tolerable in practice** because **no woman in the sample has four young children**; only three have three; **over 96% have zero or one.** The estimate is being used at $\Delta kidslt6=1$ from a base of 0, which is where the data are.
>
> **The general rule: the LPM is reliable for values of the regressors near the middle of the sample, and unreliable in the tails.** Quote it there and say so.
>
> **(d)** $y$ is Bernoulli with $P(y=1\mid\mathbf{x})=p(\mathbf{x})$, so $\mathbb{E}(y\mid\mathbf{x})=p(\mathbf{x})$ and $\mathbb{E}(y^2\mid\mathbf{x})=p(\mathbf{x})$ (since $y^2=y$ for a 0/1 variable). Hence
> $$\mathrm{Var}(y\mid\mathbf{x})=\mathbb{E}(y^2\mid\mathbf{x})-\left[\mathbb{E}(y\mid\mathbf{x})\right]^2=p(\mathbf{x})-p(\mathbf{x})^2=\boxed{p(\mathbf{x})\left[1-p(\mathbf{x})\right]}$$
>
> | $p$ | $\mathrm{Var}$ | $\mathrm{sd}$ |
> |---|---|---|
> | $0.5$ | $\mathbf{0.250}$ | $0.500$ |
> | $0.3$ | $0.210$ | $0.458$ |
> | $0.1$ | $\mathbf{0.090}$ | $0.300$ |
>
> **The variance is maximal at $p=0.5$ and shrinks toward the extremes — nearly a factor of 3 across this range.** Since $p(\mathbf{x})$ depends on $\mathbf{x}$, **$\mathrm{Var}(u\mid\mathbf{x})$ does too: MLR.5 fails by construction.** The only exception is the degenerate case where the probability does not depend on any regressor.
>
> | Property | Survives? |
> |---|---|
> | **Unbiasedness** of $\hat\beta_j$ | ✅ — needs only MLR.1–4 |
> | **Consistency** | ✅ — [[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]] Theorem 5.1 |
> | **BLUE** (Gauss–Markov) | ❌ — MLR.5 required |
> | **Valid $\mathrm{se}$, $t$, $F$** | ❌ |
>
> **A large sample does not help.** This is precisely the [[05 - Multiple Regression Analysis - OLS Asymptotics|ch. 05]] point: asymptotic normality (Theorem 5.2) is derived **under homoskedasticity**, so heteroskedasticity invalidates the usual standard errors **at every sample size**. Non-normality of $u$ is fixed by large $n$; **heteroskedasticity is not.**
>
> **The fix is heteroskedasticity-robust standard errors ([[08 - Heteroskedasticity|ch. 08]]).** They cost nothing and should be the default for any LPM. In practice the usual OLS statistics are often not far off — which is why plain OLS reporting of an LPM remains acceptable — but there is no reason to rely on that.
>
> **(e) Not with $R^2$.** Report **percent correctly predicted**:
> 1. Define $\tilde y_i=1$ if $\hat y_i\ge0.5$, else $\tilde y_i=0$.
> 2. Cross-tabulate $\tilde y_i$ against $y_i$.
> 3. Report **three** numbers: the share of $y_i=1$ correctly predicted, the share of $y_i=0$ correctly predicted, and the overall share.
>
> **Reporting only the overall figure is misleading when the classes are unbalanced.** If 90% of a sample is $y=0$, predicting "0" for everyone scores 90% while identifying nothing.
>
> **In `MROZ` the classes are nearly balanced** (428 of 753, about 57%, in the labour force), so the overall figure is informative — but it should still be broken out by class. (Wooldridge develops this further in ch. 17.)
>
> **Note that fitted values outside $[0,1]$ do not obstruct this**: the $\ge0.5$ rule works whether $\hat y_i$ is $-0.10$ or $1.20$.

---

## 📝 Summary

- **A dummy variable is a 0/1 indicator, and its coefficient is an intercept shift.** With one dummy and an intercept, the coefficient is the **difference in means between the two groups, holding the other regressors fixed**. Simple regression on a constant and a dummy **is** a comparison-of-means test — valid under homoskedasticity.
- **$g$ groups require $g-1$ dummies plus the overall intercept.** Including all $g$ with an intercept is the **dummy variable trap** (perfect collinearity, MLR.3 violated). Dropping the intercept avoids the trap but makes difference-testing awkward and yields an **inflated uncentered $R^2$** ($0.948$ vs the true $0.461$ in Example 7.6).
- **Base groups are arbitrary; keeping track of them is not.** Switching the base group is a pure reparameterization — every slope, $R^2$, SSR and $\hat\sigma$ is unchanged. **To get a standard error for the difference between two non-base groups, re-estimate with one of them as the base** — the reported standard errors alone are not enough, because the covariance is missing.
- **With $\log(y)$, dummy coefficients are percentage differences**, exactly $100[\exp(\hat\beta_1)-1]$. **The exact figure depends on which group is the base** ($-25.7\%$ vs $+34.6\%$ for the same $\hat\beta=-0.297$); **the raw coefficient $\times100$ lies between them**, which is why it is the number to report when you don't want to pick a base.
- **Ordinal variables should usually be dummied, not entered linearly** — entering $CR$ directly forces every step to have the same effect. **The linear specification is exactly the restricted model**, so the equal-step assumption is testable by an ordinary $F$ with $q=g-2$. Beauty (Example 7.7) shows why it matters: there is a **penalty for below-average looks and no premium for above-average** — an asymmetry a linear score cannot represent.
- **Dummy × dummy** lets one group's effect depend on another category (the marriage premium is $+21\%$ for men and $-9\%$ for women). **Dummy × quantitative** lets **slopes** differ; $\delta_0$ is then the gap **at $x=0$**, which is usually meaningless and imprecisely estimated — **centre the interaction**.
- **The Chow test** compares whether two groups follow the same regression: $q=k+1$ restrictions, and $\text{SSR}_{ur}=\text{SSR}_1+\text{SSR}_2$ from two separate group regressions. **It requires equal error variances across groups.** The **more useful variant allows an intercept shift and tests slopes only** ($q=k$). **There is no $R^2$ form when the two groups are estimated separately** — different SSTs.
- **With a binary $y$, OLS is the linear probability model** and $P(y=1\mid\mathbf{x})=\mathbb{E}(y\mid\mathbf{x})$, so $\hat\beta_j$ is the change in the **probability** of success — in **percentage points**, not percent.
- **The LPM's three defects:** fitted probabilities outside $[0,1]$ (33 of 753 in `MROZ`), a **constant** marginal effect on a bounded quantity (0→4 young children moves the probability by $1.048$), and **built-in heteroskedasticity**, since $\mathrm{Var}(y\mid\mathbf{x})=p(\mathbf{x})[1-p(\mathbf{x})]$. **Coefficients stay unbiased and consistent; standard errors do not, at any sample size.** Report **percent correctly predicted** rather than $R^2$.
- **Program evaluation needs covariates because assignment is rarely random.** "First-come, first-served" is not randomization. **Restricted regression adjustment** puts $w$ and the covariates in linearly; **unrestricted regression adjustment** adds $w\cdot(x_j-\bar x_j)$ interactions, and its coefficient on $w$ is the **average treatment effect** — but **only if the $x_j$ inside the interactions are demeaned**. In `JTRAIN98` the raw difference in means says training cost \$2,050; adjustment reverses it to **+\$3,110**.
- **When $y$ is discrete but quantitative, read every coefficient as an effect on $\mathbb{E}(y\mid\mathbf{x})$.** "0.09 fewer children per year of education" is meaningless for one woman and exactly right for a group of 100 — **about nine fewer children among them**.

---

## ⚠️ Important Notes

> [!warning] The twelve mistakes this chapter is designed to prevent
>
> 1. **Naming a dummy after the variable instead of the event.** `gender`, `party`, `race` tell you nothing about which category is 1. Use `female`, `democrat`, `nonwhite`.
> 2. **Including all $g$ dummies with an intercept.** The dummy variable trap. Some packages silently drop one — **which means you no longer know what your base group is.**
> 3. **Reporting an uncentered $R^2$.** Drop the intercept and $R^2$ silently switches to $1-\text{SSR}/\sum y_i^2$, inflating it (0.948 vs 0.461). **Always keep the intercept, or force the centred version.**
> 4. **Testing a difference between two non-base groups from the printed standard errors.** You need the covariance. **Rebase and re-estimate.**
> 5. **Quoting the exact percentage without saying which group is the base.** $-25.7\%$ and $+34.6\%$ are both exact and both from $\hat\beta=-0.297$.
> 6. **Confusing percentage points with percent.** $\hat\beta_{black}=0.170$ in an LPM is **17 percentage points**, which against a base rate of 0.28 is a **60% relative** increase.
> 7. **Reading the level coefficient as the effect when interactions are present.** `GPA3`: $-0.353$ on $female$ becomes $+0.461$ at realistic values. **The sign flips.**
> 8. **Concluding "no effect" from insignificant $t$'s on interacted terms.** In Example 7.10 the $female$ standard error grew **4.67-fold** when $female\cdot educ$ entered; the joint $F$ is $34.33$. In (7.22) not one term is significant and the joint $F$ is $8.18$.
> 9. **Entering an ordinal variable linearly without testing the restriction.** The equal-step assumption is a **testable** $q=g-2$ hypothesis, and the restricted model is free — you were going to run it anyway.
> 10. **Using the $R^2$ form of the Chow test after two separate group regressions.** Different SSTs. **SSRs add; $R^2$s do not.**
> 11. **Forgetting to demean the covariates inside URA interactions.** The coefficient on $w$ is then the effect at $\mathbf{x}=\mathbf{0}$, not the ATE. In `JTRAIN98`, using $train\cdot married$ undemeaned gives $3.79$ — **the ATE for unmarried men, not the overall ATE of $3.11$.**
> 12. **Treating "controlled for observables" as "causal."** The `JTRAIN` grants, the `GPA1` PCs, the AFDC birth-weight result — **all are correlations that survive controls and may still be spurious.** Unconfoundedness is an assumption you cannot test.

> [!important] The four ideas most likely to be examined
>
> **1. $g$ groups, $g-1$ dummies, and the base group.** Be able to (i) say why, (ii) rebase an equation by hand, (iii) recover any group's intercept, and (iv) explain why the difference between two non-base groups needs a re-estimation to be tested. Verify with the identity **new intercept $=$ old intercept $+$ new base's coefficient**.
>
> **2. $100[\exp(\hat\beta_1)-1]$ and its asymmetry.** Know that it is base-group-specific, that $100\hat\beta_1$ lies between the two exact values, and that the correction matters more the larger $|\hat\beta_1|$ (0.1 points at $\hat\beta=0.054$; 4 points at $\hat\beta=0.297$; **31 points at $\hat\beta=0.700$** in the law school example).
>
> **3. The Chow test in both forms.** $q=k+1$ for "no differences at all," $q=k$ for "same slopes, different intercepts." $\text{SSR}_{ur}=\text{SSR}_1+\text{SSR}_2$; $df=n-2(k+1)$. **And the assumption of equal group error variances.**
>
> **4. The LPM's three defects and exactly which OLS properties each one destroys.** The table in Exercise 5(d) is the answer. Be able to derive $\mathrm{Var}(y\mid\mathbf{x})=p(1-p)$ from $y^2=y$ in one line, and to say that **no sample size fixes heteroskedasticity.**

> [!note] Cross-subject connections
> - **Dummy coding is one-hot encoding** from [[Data Preparation and Visualization/contents/00-Index|Data Preparation & Visualization]] and [[Machine Learning/contents/00-Index|Machine Learning]] — with one crucial difference. **Econometrics drops one category (the base group) because the intercept is not penalized and perfect collinearity is fatal.** ML pipelines often keep all $g$ columns because **regularization** ($L^1/L^2$) makes the design matrix invertible anyway. **The dummy variable trap is real in OLS and disappears in ridge regression** — worth knowing which world you are in.
> - **The linear probability model is what logistic regression replaces.** [[Machine Learning/contents/00-Index|ML]]'s logit/probit constrain $p(\mathbf{x})$ to $(0,1)$ and give diminishing marginal effects, at the cost of coefficients that are no longer partial effects. **The LPM's coefficients are directly readable — which is why economists still use it.** Wooldridge ch. 17 covers the alternatives.
> - **"Percent correctly predicted" is classification accuracy**, and the warning about unbalanced classes is the same one that motivates precision, recall and ROC-AUC in [[MLOps/contents/00-Index|MLOps]] model evaluation. **The $\ge0.5$ rule is a decision threshold**, and moving it trades the two error types — exactly the ROC curve.
> - **Program evaluation, potential outcomes $[y(0),y(1)]$, and the ATE** are the causal-inference vocabulary that runs through A/B testing and uplift modelling. **Unconfoundedness is the "no unmeasured confounders" assumption**; regression adjustment is the simplest of the adjustment estimators (matching, propensity scores and doubly-robust methods generalize it).
> - **The Chow test is a structural-break test.** Applied to time rather than groups it becomes the **Chow breakpoint test** of [[Time-series Analysis/contents/00-Index|Time-series Analysis]] — same statistic, with "group" replaced by "before/after the break date."
> - **Comparison of means as a regression** links to [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]]: the two-sample $t$ test **is** the $t$ on a dummy, and a one-way ANOVA **is** the $F$ on a set of $g-1$ dummies. **Every ANOVA is a regression on dummies.**

> [!warning] Gaps in the source material
> - **No lecture slides exist for Econometrics.** Chapter scope (Wooldridge 1–12) is my own editorial decision — see [[00-Index]].
> - **No data files are in the vault.** `WAGE1`, `GPA1`, `GPA3`, `JTRAIN`, `JTRAIN98`, `HPRICE1`, `MROZ`, `CRIME1`, `MLB1`, `LAWSCH85`, `BEAUTY` and `FERTIL2` are all referenced here and **none can be re-estimated.** Every coefficient, standard error and $R^2$ above is **quoted as printed.**
> - **Internal consistency verified wherever the text reports enough to check itself**, and it holds throughout: the comparison-of-means arithmetic ($7.10-2.51=4.59$, $t=-8.37$), every exact-percentage conversion, the four group intercepts in (7.11) and (7.14), the rebasing identities ($0.123=0.321-0.198$ and $0.411=0.213+0.198$), the race $F$ statistic ($2.63$), **both** forms of the Chow statistic ($8.18$ and $8.14$), the `GPA3` predicted difference ($+0.461$), and — most satisfyingly — **the entire Figure 7.3 line**: substituting the stated covariate values into (7.29) gives an intercept of exactly $-0.146$, a zero crossing at $3.84$ years, and $\widehat{inlf}=0.500$ at $educ=17$, all three matching the figure's printed labels. ✓
> - **Figures 7.1, 7.2 and 7.3 are images** and do not extract. Figure 7.1 shows two parallel wage–education lines with the women's intercept below; Figure 7.2 shows the two slope-difference cases; Figure 7.3 plots the participation line described above. **All three are reconstructed from the surrounding prose, which states their content explicitly, and Figure 7.3 is additionally confirmed by the arithmetic.**
> - **Table 7.1 is a data listing**, not a result, and extracted intact.
> - **Example 7.13's $\overline{earn96}$, $\overline{educ}$, $\overline{age}$ and $\overline{married}$ are never printed**, so the interaction terms in (7.44) **cannot be reconstructed as numbers** — only the ATE and its interpretation are available. The stated alternative ($train\cdot married$ undemeaned $\Rightarrow$ $\hat\tau=3.79$, se $0.81$) is quoted, not derived.
> - **The $F$ statistic for Example 7.10's $H_0:\delta_0=\delta_1=0$ ($F=34.33$) and the `GPA3` slopes-only $p$-value of $0.205$ are quoted**, not verifiable — the underlying $R^2$ values are not all printed.
> - **Notation mangling in the PDF:** `b^ j`, `d0` for $\delta_0$, `g0` for $\gamma_0$, `E1u0female,educ2` for $\mathbb{E}(u\mid female,educ)$, `R2 0` for $R_0^2$, `t^rra` and `tura^` for $\hat\tau_{rra}$ and $\hat\tau_{ura}$, `1a^ 1 2 ^a02` for $(\hat\alpha_1-\hat\alpha_0)$. **Every equation has been transcribed by hand against its numbered reference.**
> - **Three typos survive in the source text itself:** *"quantitative meeting"* for *"quantitative meaning"* (p. 243), *"a dicussion"* for *"a discussion"* (p. 243), and *"with 'self being used broadly"* with an unclosed quotation mark (p. 245). **Section 7-6a's derivation also refers to "the $\hat\tau$ from regression (7.40)" where (7.42) is meant** — (7.40) is the population equation, (7.42) the estimable regression. Corrected above.

#econometrics #dummy-variables #program-evaluation #linear-probability-model #chow-test
