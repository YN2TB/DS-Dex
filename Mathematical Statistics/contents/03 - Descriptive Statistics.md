---
subject: Mathematical Statistics
chapter: 03
tags: [ds, statistics, descriptive-statistics, variance, correlation, boxplot]
source: "MS_Lec03_Descriptive.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Numerical Summary (Descriptive Statistics)

> [!note] Reading
> **[1] Devore & Berk, Ch. 1, pp. 25–49** · **[2] Miller & Miller, Ch. 3, pp. 99–162** · **[4] Anderson et al., Ch. 2, pp. 59–**

> [!warning] Source note
> **Almost every formula in this deck is an embedded equation image** and did not survive text extraction. The data tables, Excel/R reference tables, and section structure did. The formulas below are the standard ones the slide titles name — verify against the original slides, since notation (especially $n$ vs $n-1$) is exam-critical.

## 📘 Main Knowledge

### The measurement families

| Family | Measures |
|---|---|
| **Location — Central tendency** | Mean, Median, Mode |
| **Location — Extremes** | Minimum, Maximum |
| **Location — Quantiles** | Quartile, Percentile |
| **Variability** | Range, Variance, Standard Deviation, Coefficient of Variation, Interquartile Range |
| **Shape** | Skewness (and kurtosis) |
| **Relationship** | Covariance, Correlation |

---

## Location

### 3.1 Mean (arithmetic mean)

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i \qquad\qquad \mu = \frac{1}{N}\sum_{i=1}^{N} x_i$$

Sample mean $\bar{x}$ (a statistic) estimates population mean $\mu$ (a parameter) — the distinction from [[01 - Introduction to Statistics]].

**Weighted mean** — when observations carry different importance:

$$\bar{x}_w = \frac{\sum w_i x_i}{\sum w_i}$$

The slide's example is a volume-weighted average price:

| | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Price | 10 | 12 | 18 | 14 |
| Volume | 70 | 90 | 110 | 130 |

The unweighted mean price is 13.5, but that treats a quarter with 70 units sold as equal to one with 130. The volume-weighted price is the economically meaningful figure.

**Mean of grouped data** — frequencies are the weights:

$$\bar{x} = \frac{\sum f_i x_i}{\sum f_i} = \sum p_i x_i \quad\text{where } p_i = f_i/n$$

| Wage (\$) | 7 | 8 | 9 |
|---|---|---|---|
| Frequency | 4 | 10 | 6 |
| Proportion | 0.2 | 0.5 | 0.3 |
| Percent | 20% | 50% | 30% |

$\bar{x} = 0.2(7) + 0.5(8) + 0.3(9) = 1.4 + 4.0 + 2.7 = \mathbf{8.1}$

For data grouped into **classes**, use each class's **midpoint** as $x_i$ — an approximation that assumes values are evenly spread within each class.

### 3.2 Median

The value splitting the ordered data into a lower 50% and an upper 50%.

$$\tilde{x} = \begin{cases} x_{(\frac{n+1}{2})} & n \text{ odd} \\[4pt] \dfrac{x_{(\frac{n}{2})} + x_{(\frac{n}{2}+1)}}{2} & n \text{ even}\end{cases}$$

**The data must be sorted first.**

### 3.3 Mode

The most frequently occurring value. A dataset may have no mode, one mode (unimodal), or several (bimodal, multimodal).

### Which measure for which variable type

Slide 14 poses this as a table to be completed — the answers follow from the permitted-operations hierarchy in [[01 - Introduction to Statistics]]:

| | Mean | Median | Mode |
|---|---|---|---|
| **Nominal variable** | ✗ | ✗ | ✓ |
| **Ordinal variable** | ✗ | ✓ | ✓ |
| **Scale variable** | ✓ | ✓ | ✓ |
| **Affected by extreme values** | **✓ Yes** | ✗ No | ✗ No |

The mode needs only counting; the median needs ordering; the mean needs arithmetic. **The last row is the practical one**: the mean is the only measure an outlier can drag.

**Grouped data** (slide 17) — customer waiting time:

| Waiting time | 0–5 | 5–10 | 10–15 | 15–20 | 20+ |
|---|---|---|---|---|---|
| Frequency | 15 | 20 | 8 | 5 | 2 |
| **Midpoint** | 2.5 | 7.5 | 12.5 | 17.5 | 22.5 |

- **Median** is in the class **[5 – 10)** — cumulative frequency reaches 15 before it and 35 after, so the 25th and 26th values both fall there.
- **Modal class** is **[5 – 10)** (highest frequency, 20).
- **Mean** uses the midpoints: $\bar{x} = \frac{15(2.5)+20(7.5)+8(12.5)+5(17.5)+2(22.5)}{50} = \frac{382.5}{50} = 7.65$

Note the final class `20+` is **open-ended**; its midpoint of 22.5 is an assumption, so the mean is only as good as that guess.

### 3.4 Quantiles

Values dividing sorted data into equal-sized parts.

- **Q1 (1st quartile, "lower fourth")** — 25% below
- **Q2 (2nd quartile)** — the **median**, 50% below
- **Q3 (3rd quartile, "upper fourth")** — 75% below
- **Percentile $k$** — $k\%$ below

### Normal QQ plot

Compares a sample's distribution against normality: plot sample quantiles against the theoretical normal quantiles. **Points on a straight line ⇒ approximately normal.** Systematic curvature indicates skew; S-shapes indicate heavy or light tails.

This is the standard visual check for the normality assumption that [[06 - Confidence Interval]] and [[07 - Hypothesis Testing - One Sample]] rely on, and its failure is what motivates [[09 - Non-parametric Testing]].

---

## Variability

> Central Tendency may not provide efficient information about the data. **Data can have the same Mean and Median but differ in variability** (dispersion, spread).

The slide illustrates two datasets with Mean = Median = 5 and visibly different spread. This is why every summary needs a location measure *and* a variability measure.

### 3.5 Range

$$\text{Range} = x_{\max} - x_{\min}$$

**Simplest, but poorest information** — it uses only two observations and ignores everything between them, so a single outlier determines it entirely.

### 3.6 Variance and standard deviation

**Population:**
$$\sigma^2 = \frac{\sum_{i=1}^{N}(x_i - \mu)^2}{N} \qquad \sigma = \sqrt{\sigma^2}$$

**Sample:**
$$s^2 = \frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n-1} \qquad s = \sqrt{s^2}$$

The numerator $\sum(x_i - \bar{x})^2$ is the **sum of squares (SS)**, which appears as a column in the slide's comparison table.

> [!warning] Why $n-1$ and not $n$ — the single most examinable point in this chapter
> Deviations are taken about $\bar{x}$, which was itself computed from the same data. $\sum(x_i - \bar{x})^2$ is **minimised** at $\bar x$ — it is smaller than $\sum(x_i - \mu)^2$ would be — so dividing by $n$ **systematically underestimates** $\sigma^2$.
>
> Dividing by $n-1$ (the **degrees of freedom**) corrects the bias exactly, making $\mathbb{E}[s^2] = \sigma^2$. The intuition for "degrees of freedom": once $\bar{x}$ is fixed, only $n-1$ deviations are free — the last is determined, since deviations sum to zero.
>
> The distinction is not merely notational: Excel's `VAR` uses $n-1$ (sample) while `VARP` uses $N$ (population), and choosing wrong gives a wrong answer.

**Standard deviation is preferred for reporting** because it is in the **original units** — variance is in units squared, so a variance of "16 dollars²" is uninterpretable while "4 dollars" is not.

### 3.7 Coefficient of variation

$$CV = \frac{s}{\bar{x}} \times 100\%$$

A **relative** measure of dispersion — dimensionless, so it compares variability across datasets with different units or wildly different means.

**The comparison exercise (slide 30):**

| | Data | Mean | $s^2$ | $s$ | $CV$ |
|---|---|---|---|---|---|
| **Firm A** | Profit: 5, 6, 7, 8, 9 | 7 | 2.5 | 1.58 | **22.6%** |
| **Firm B** | Profit: 51, 53, 55, 57, 59 | 55 | 10 | 3.16 | **5.7%** |
| **Firm C** | Price: 15, 16, 17, 18, 19 | 17 | 2.5 | 1.58 | **9.3%** |

The point of the exercise: **B has the largest standard deviation but the smallest relative variability.** And A and C have *identical* $s$ but different $CV$ — and are in different units anyway, so only $CV$ can compare them.

### 3.8 Interquartile range

$$IQR = Q_3 - Q_1$$

The range of the **middle 50%**. Because it discards both tails it is **robust** — immune to outliers, unlike range, variance, and standard deviation.

### Outliers and extremes

The lecture's two-tier fence rule:

| Region | Boundary |
|---|---|
| **Outlier** | beyond $Q_1 - 1.5\,IQR$ or $Q_3 + 1.5\,IQR$ |
| **Extreme** | beyond $Q_1 - 3\,IQR$ or $Q_3 + 3\,IQR$ |

This is the rule used in [[Data Preparation and Visualization/contents/06 - Data Cleaning|Data Cleaning]], and it is robust for the reason given there: outliers inflate the mean and standard deviation used by σ-based rules, but cannot move the quartiles.

### The five-number summary and boxplot

**Five key points:** Minimum, Q1, Median, Q3, Maximum.

A **boxplot** draws the box from Q1 to Q3 (spanning the IQR) with a line at the median; **whiskers** extend to the most extreme points *within* the 1.5·IQR fences; anything beyond is plotted individually as an outlier.

**Slide 34–35 worked example** — salary distribution:

| Salary | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|
| No. of workers | 10 | 16 | 30 | 19 | 14 | 10 | 0 | 0 | 1 |

$n = 100$. The slide's annotation reads `10  11  12  13.5 … 18` — the min, Q1, median, Q3, and max. The single worker at 18 is separated from the rest by a gap of 3, and the fence is $Q_3 + 1.5\,IQR = 13.5 + 1.5(2.5) = 17.25$, so **18 is an outlier**.

Boxplots are ideal for **comparing groups side by side** — slide 37 tabulates Max/Q3/Q2/Q1/Min/Mean across 2014–2017.

### 3.9 Skewness

$$Sk = \frac{\sum(x_i - \bar{x})^3}{n s^3}$$

A dimensionless measure of asymmetry:

- $Sk > 0$ — **positively (right) skewed**; long right tail; typically **mean > median**
- $Sk = 0$ — symmetric
- $Sk < 0$ — **negatively (left) skewed**; long left tail; typically **mean < median**

The cube preserves sign, so large deviations above the mean contribute positively and those below negatively. The R output on slide 48 gives `skewness = 0.255` (mild right skew) and `kurtosis = -0.582` (lighter tails than normal).

---

## Relationship

### 3.10 Covariance and correlation

$$\operatorname{cov}(X,Y) = s_{xy} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{n-1}$$

Covariance measures joint variation, but its magnitude depends on units — so it cannot be compared across datasets. **Correlation normalises it:**

$$r_{xy} = \frac{\operatorname{cov}(X,Y)}{s_x \, s_y} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum(x_i-\bar{x})^2}\sqrt{\sum(y_i-\bar{y})^2}}$$

$$-1 \le r \le +1$$

**Reference values** (slide 41, repeated from [[02 - Tables and Charts]]): strong positive $r = 0.8$; weak positive $r = 0.5$; weak negative $r = -0.5$; uncorrelated $r = 0$.

### 3.11 Standardised value (z-score)

$$z_i = \frac{x_i - \bar{x}}{s} \qquad\text{(or } \frac{x_i - \mu}{\sigma}\text{)}$$

Expresses each observation as **how many standard deviations it sits from the mean**. Dimensionless, so values from different variables become comparable. Standardising gives a set with mean 0 and standard deviation 1 — exactly what `StandardScaler` does in [[Data Preparation and Visualization/contents/07 - Data Transformation|Data Transformation]], and the transformation underlying all normal-distribution tables.

### Excel functions

| Statistic | Function |
|---|---|
| Sum | `=SUM(array)` |
| Mean | `=AVERAGE(array)` |
| Median | `=MEDIAN(array)` |
| Mode | `=MODE(data)` |
| $k$th Quartile | `=QUARTILE(array, k)` |
| Percentile $k$ | `=PERCENTILE(data, k)` |
| Sample variance $s^2$ | `=VAR(array)` |
| Sample SD $s$ | `=STDEV(array)` |
| Covariance | `=COVAR(array1, array2)` |
| Correlation $r_{XY}$ | `=CORREL(array1, array2)` |
| $X \sim N(\mu,\sigma^2)$, $P(X<b)$ | `=NORMDIST(b, µ, σ, 1)` |

### R extension

```r
x3 <- c(rep(11,8), rep(12,24), rep(13,30), rep(14,22), rep(15,12), rep(16,4))
hist(x3, breaks = c(10,11,12,13,14,15,16), col="lightgreen")
summary(x3)
#  Min. 1st Qu. Median  Mean 3rd Qu.  Max.
# 11.00   12.00  13.00 13.18   14.00 16.00

length(x3)     # 100
mean(x3)       # 13.18
var(x3)        # 1.603
sd(x3)         # 1.266
skewness(x3)   # 0.255
kurtosis(x3)   # -0.582
```

**Grouped data in R:**

```r
ll  <- c(10,12,14,16,18)        # lower limits
ul  <- c(12,14,16,18,20)        # upper limits
fr  <- c(8,25,30,24,13)         # frequencies
mid <- (ll+ul)/2                # class midpoints

n    <- sum(fr)                              # 100
mean <- sum(mid*fr)/n                        # 15.18
ssq  <- sum((mid-mean)^2*fr)/(n-1)           # 5.341
s    <- sqrt(ssq)                            # 2.311
skew <- sum((mid-mean)^3*fr)/n/s^3           # 0.021
kurt <- sum((mid-mean)^4*fr)/n/s^4           # 2.117
```

## ✏️ Exercises

**1.** For the grouped wage data, compute the mean. Then explain why the mean of grouped *class* data is only an approximation.

> [!example]- Solution
> | Wage | 7 | 8 | 9 |
> |---|---|---|---|
> | $f_i$ | 4 | 10 | 6 |
>
> $$\bar{x} = \frac{4(7) + 10(8) + 6(9)}{20} = \frac{28 + 80 + 54}{20} = \frac{162}{20} = 8.1$$
>
> Equivalently with proportions: $0.2(7) + 0.5(8) + 0.3(9) = 8.1$. This is **exact**, because each value (7, 8, 9) is a distinct observed value, not a class.
>
> **For class data it becomes an approximation.** With classes like `[5 – 10)` we no longer know the individual values, so we substitute the **midpoint** (7.5) for all 20 observations in that class. That assumes the values are **symmetrically distributed within the class** — equivalently, that their within-class mean equals the midpoint.
>
> When it fails: if waiting times cluster near 5 and thin out toward 10 (a right-skewed class), the true within-class mean is below 7.5 and the grouped mean overstates. The error grows with class width, which is one more reason bin width is an analytical decision.
>
> **Open-ended classes are worse.** `20+` has no midpoint at all; assuming 22.5 is a guess, and if a few customers waited 90 minutes the grouped mean is badly wrong. Report the median instead when a distribution has an open-ended tail.

**2.** Complete the Mean/Median/Mode applicability table and justify each cell.

> [!example]- Solution
> | | Mean | Median | Mode |
> |---|---|---|---|
> | **Nominal** | ✗ | ✗ | ✓ |
> | **Ordinal** | ✗ | ✓ | ✓ |
> | **Scale** | ✓ | ✓ | ✓ |
> | **Affected by extreme values** | **Yes** | No | No |
>
> The logic mirrors the permitted-operations hierarchy from [[01 - Introduction to Statistics]]:
>
> - **Mode needs only counting**, so it works for every type. "The most common eye colour is brown" is meaningful.
> - **Median needs ordering.** For ordinal data — Very Good > Good > Fair > Bad — the middle response is meaningful, so the median works. Not for nominal: there is no "middle" eye colour.
> - **Mean needs arithmetic.** Only scale variables support addition and division. Coding Bad=1…Very Good=4 and averaging to 2.8 is extremely common and **technically invalid**: it assumes the gap Bad→Fair equals Fair→Good, which ordinal data does not guarantee.
>
> **Why only the mean is outlier-sensitive:** it uses every value's *magnitude*, so one extreme observation shifts it in proportion to its size. The median uses only *rank position* — replacing the largest value with one a thousand times larger moves it not at all. In the salary data, the single worker at 18 pulls the mean up while the median stays at 12.

**3.** Complete the three-firm comparison table and explain which firm has the greatest variability.

> [!example]- Solution
> Each dataset has 5 evenly spaced values, so the arithmetic is clean.
>
> **Firm A** (5,6,7,8,9): $\bar{x} = 7$. Deviations −2,−1,0,1,2 → $SS = 10$, $s^2 = 10/4 = 2.5$, $s = 1.58$.
> **Firm B** (51,…,59): $\bar{x} = 55$. Deviations −4,−2,0,2,4 → $SS = 40$, $s^2 = 10$, $s = 3.16$.
> **Firm C** (15,…,19): $\bar{x} = 17$. Deviations −2,−1,0,1,2 → $SS = 10$, $s^2 = 2.5$, $s = 1.58$.
>
> | | Mean | SS | $s^2$ | $s$ | **CV** |
> |---|---|---|---|---|---|
> | A (profit) | 7 | 10 | 2.5 | 1.58 | **22.6%** |
> | B (profit) | 55 | 40 | 10 | 3.16 | **5.7%** |
> | C (price) | 17 | 10 | 2.5 | 1.58 | **9.3%** |
>
> **"Greatest variability" depends on which question you mean.**
>
> In **absolute** terms B is most variable ($s = 3.16$) — its profits swing by twice as much in dollars. In **relative** terms **A is by far the most variable** ($CV = 22.6\%$): its profit fluctuates by nearly a quarter of its typical level, while B's fluctuates by under 6% of its. For an investor judging risk, **A is the riskier firm** despite the smaller standard deviation.
>
> A and C are the sharpest illustration: **identical $s = 1.58$, different $CV$** — because C's values are larger. And they are not even in the same units ($ millions vs $), so $s$ cannot compare them at all while $CV$, being dimensionless, can.
>
> **Use $CV$ when means differ substantially or units differ.** Its limitation: it is meaningless when $\bar{x}$ is near zero (the ratio explodes) or negative.

**4.** For the salary data, find the five-number summary and identify any outliers using the 1.5·IQR rule.

> [!example]- Solution
> | Salary | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
> |---|---|---|---|---|---|---|---|---|---|
> | Freq | 10 | 16 | 30 | 19 | 14 | 10 | 0 | 0 | 1 |
> | **Cumulative** | 10 | 26 | 56 | 75 | 89 | 99 | 99 | 99 | 100 |
>
> $n = 100$.
>
> - **Min = 10**, **Max = 18**
> - **Q1** — the 25th/26th values. Cumulative reaches 26 at salary 11 → **Q1 = 11**
> - **Median (Q2)** — the 50th/51st values. Cumulative passes 50 within salary 12 (27th–56th) → **Median = 12**
> - **Q3** — the 75th/76th values. The 75th is the last of salary 13, the 76th the first of 14 → **Q3 = 13.5**
>
> This matches the slide's annotation `10  11  12  13.5 … 18`.
>
> $$IQR = 13.5 - 11 = 2.5$$
> $$\text{Lower fence} = 11 - 1.5(2.5) = 7.25 \qquad \text{Upper fence} = 13.5 + 1.5(2.5) = 17.25$$
>
> **The single worker earning 18 exceeds 17.25 and is an outlier.** The extreme fence is $13.5 + 3(2.5) = 21$, so it is an outlier but **not** an "extreme".
>
> The boxplot therefore runs: box from 11 to 13.5, median line at 12, lower whisker to 10, upper whisker to **15** (the largest value within the fence — *not* to 18), and a single plotted point at 18.
>
> **The whisker stops at the last value inside the fence, not at the fence itself** — a detail routinely got wrong. Note also the distribution is right-skewed (median 12 sits left of centre in the box, and the upper tail is longer), consistent with mean > median.

**5.** (Advanced) Explain why sample variance divides by $n-1$, why standard deviation is preferred to variance for reporting, and why correlation is preferred to covariance.

> [!example]- Solution
> **(a) Why $n-1$.** We want $s^2$ to be an **unbiased** estimator: $\mathbb{E}[s^2] = \sigma^2$.
>
> The problem is that deviations are measured about $\bar{x}$, not the true $\mu$ — and $\bar{x}$ is computed *from the same sample*. The function $g(c) = \sum(x_i - c)^2$ is minimised at $c = \bar{x}$, so
> $$\sum(x_i - \bar{x})^2 \le \sum(x_i - \mu)^2$$
> **always**, with equality only in the impossible case $\bar x = \mu$ exactly. Dividing by $n$ therefore underestimates $\sigma^2$ systematically. One can show
> $$\mathbb{E}\Big[\sum(x_i-\bar x)^2\Big] = (n-1)\sigma^2$$
> so dividing by $n-1$ corrects it exactly.
>
> **Degrees of freedom intuition:** the deviations satisfy $\sum(x_i - \bar{x}) = 0$, one linear constraint. Given any $n-1$ of them the last is determined — only $n-1$ pieces of information about spread are free. Estimating $\mu$ from the data "used up" one degree of freedom. This same $n-1$ reappears as the degrees of freedom of the $t$-distribution in [[06 - Confidence Interval]], and it is not a coincidence.
>
> With **population** data no estimation occurs — $\mu$ is known — so we divide by $N$.
>
> **(b) SD over variance:** variance is in **squared units**. A wage variance of "1.603 dollars²" has no interpretation; $s = 1.27$ dollars does, and can be compared directly against the mean and plotted on the same axis. Variance remains the theoretically convenient quantity because it is **additive** for independent variables ($\operatorname{Var}(X+Y) = \operatorname{Var}(X)+\operatorname{Var}(Y)$), which standard deviations are not — this is exactly the diversification result from [[01 - Introduction to Statistics]].
>
> **(c) Correlation over covariance:** covariance carries the units of both variables. $\operatorname{cov}(\text{ad spend}, \text{sales})$ is in "dollar-dollars", and rescaling advertising from dollars to thousands divides the covariance by 1,000 without any change in the underlying relationship. Its magnitude is therefore uninterpretable — you can only read the **sign**.
>
> Dividing by $s_x s_y$ cancels both units, bounding the result in $[-1, +1]$ where 0 is no linear relationship and ±1 is perfect. That gives a scale readable across any pair of variables — hence the reference values 0.8 (strong), 0.5 (weak), 0 (none).
>
> **Both share a fatal limitation:** they capture **linear** association only. $r \approx 0$ for a perfect parabola, and neither implies causation. Always plot — Anscombe's quartet, [[02 - Tables and Charts]].

## 📝 Summary

- **Location:** mean (uses every value, outlier-sensitive), median (rank-based, robust), mode (most frequent, works on any type).
- **Mode for any variable; median needs ordinal; mean needs scale.** Only the mean is dragged by outliers.
- **Grouped-class statistics use midpoints** and are approximations; open-ended classes have no midpoint.
- **Sample variance divides by $n-1$** (degrees of freedom) for unbiasedness; population variance divides by $N$.
- **SD is preferred for reporting** (original units); **variance** for theory (it is additive under independence).
- **CV = $s/\bar{x}$ is dimensionless** and the only fair comparison across different units or very different means.
- **IQR = Q3 − Q1 is robust**; fences at 1.5·IQR (outlier) and 3·IQR (extreme).
- **Five-number summary → boxplot.** Whiskers stop at the last value *inside* the fence.
- **Skewness:** $Sk>0$ right-skewed (mean > median), $Sk<0$ left-skewed.
- **Correlation is standardised covariance**, bounded in $[-1,1]$, dimensionless — and linear-only.
- **z-score** $=(x-\bar x)/s$ measures distance from the mean in SD units.

## ⚠️ Important Notes

**$n-1$ vs $n$ is the classic exam trap.** Sample variance uses $n-1$; population uses $N$. Excel: `VAR`/`STDEV` are sample, `VARP`/`STDEVP` are population. The wrong choice gives a wrong number, not merely a different convention.

**Never average an ordinal variable.** Coding Bad=1…Very Good=4 and reporting a mean of 2.8 assumes equal spacing between categories, which ordinal data does not provide. Report the median or the frequency distribution.

**The mean is not robust; the median is.** In right-skewed data (income, waiting times, house prices) the mean exceeds the median and overstates the typical case. Report both — a large gap *is* the finding.

**$CV$ breaks down when $\bar{x} \approx 0$ or is negative.** The ratio explodes or changes sign meaninglessly.

**Boxplot whiskers extend to the most extreme point within the fences, not to the fences.** In the salary example the upper whisker reaches 15, not 17.25.

**A boxplot hides multimodality.** Two clearly separated clusters can produce a boxplot identical to a unimodal distribution's. Pair it with a histogram — the lecture shows table, histogram, and boxplot together for exactly this reason.

**Range uses only two observations** and is determined entirely by the most extreme ones. Almost never the right dispersion measure.

**Covariance magnitude is uninterpretable** — only its sign is. Rescaling a variable rescales the covariance. Use $r$.

**$r$ measures linear association only**, and is itself sensitive to outliers: a single point can move $r$ from 0 to 0.8. Plot first.

**Correlation does not imply causation** — nor does it rule out a confounder driving both variables.

**Quartile conventions differ between software.** Excel's `QUARTILE`, R's default `quantile(type=7)`, and the textbook's "lower fourth" can disagree on small samples. Exam answers should follow the textbook's definition.

> [!warning] Gaps in the source slides
> **Nearly all formulas are embedded equation images** and did not extract. Specifically, slides 6, 8, 10–13, 15–16, 18–20, 26–29, 31–33, 36, 38–40, 42–43, 45–46 contain the mathematical content as images. **Every formula in this note is the standard textbook form, reconstructed from the slide titles** — check the notation against the originals.
>
> Also unrecoverable:
> - **Slides 2–4 ("Comparison", profit of two projects A & B)** — the motivating example is entirely images.
> - **Slides 21–22 (Normal QQ plot)** — titles and one caption only; the plots and interpretation guidance are images.
> - **Slide 28 ("Population and Sample: difference")** — the population/sample formula contrast is an image. Given how examinable $n$ vs $n-1$ is, **this is the most costly gap in the lecture.**
> - **Slide 45 ("Combined sample")** — title only. Presumably the pooled mean/variance formulas for merging two samples; not recoverable.
> - **Slide 46 ("Summary")** — the lecturer's own summary is an image.
> - **Slides 14, 30, 37** are tables the student is meant to complete; I have filled them in Exercises 2–3 and the main text.
> - **Slide 48's R output** lists `x3` values as 11,13,15,17,19,21 in the side table but the code uses `rep(11..16)` — the table appears to be a **different or mislabelled dataset**. The `summary()` output (mean 13.18) matches the code, not the table.
>
> **Exercises set:** [1] Ch. 1 (p. 31) 30, 33, 35–40; (p. 41) 41, 44, 46, 49, 50, 54, 55, 59; (p. 44) 60, 63, 67, 75, 76, 78 · [4] Ch. 2 (p. 67) 2.9, 2.10, 2.11.

---
**Previous:** [[02 - Tables and Charts]] · **Next:** [[04 - Sampling Distributions]]
