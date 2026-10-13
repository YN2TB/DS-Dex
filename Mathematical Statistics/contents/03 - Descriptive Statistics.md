---
subject: Mathematical Statistics
chapter: 03
tags: [ds, statistics, descriptive-statistics, variance, correlation, boxplot]
source: "MS_Lec03_Descriptive.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Numerical Summary (Descriptive Statistics)

Reading: Devore & Berk ch. 1 (pp. 25–49); Miller & Miller ch. 3 (pp. 99–162); Anderson et al. ch. 2 (pp. 59–).

> [!warning] Source note
> Almost every formula in this deck is an image. Data tables, Excel/R tables and the section structure extracted; the formulas below are the standard ones named in the slide titles. Check notation (especially $n$ vs $n-1$) against the original slides.

## 📘 Main Knowledge

| Family | Measures |
|---|---|
| central tendency | mean, median, mode |
| extremes | minimum, maximum |
| quantiles | quartiles, percentiles |
| variability | range, variance, standard deviation, coefficient of variation, IQR |
| shape | skewness, kurtosis |
| relationship | covariance, correlation |

### Location

**Mean**
$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i,\qquad \mu = \frac{1}{N}\sum_{i=1}^{N} x_i$$

**Weighted mean**: $\bar{x}_w = \sum w_i x_i/\sum w_i$. Slide example:

| | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| price | 10 | 12 | 18 | 14 |
| volume | 70 | 90 | 110 | 130 |

Unweighted mean price 13.5; volume-weighted $5580/400=13.95$, the economically meaningful average.

**Grouped data**: $\bar{x} = \sum f_i x_i/\sum f_i = \sum p_i x_i$ with $p_i=f_i/n$.

| Wage (\$) | 7 | 8 | 9 |
|---|---|---|---|
| frequency | 4 | 10 | 6 |
| proportion | 0.2 | 0.5 | 0.3 |

$\bar x = 0.2(7)+0.5(8)+0.3(9)=8.1$. For classes, use class midpoints (assumes values spread evenly within each class).

**Median**: the middle of the sorted data.
$$\tilde{x} = \begin{cases} x_{((n+1)/2)} & n \text{ odd}\\[3pt] \tfrac12\left(x_{(n/2)} + x_{(n/2+1)}\right) & n \text{ even}\end{cases}$$

**Mode**: the most frequent value; there may be none, one or several.

| | Mean | Median | Mode |
|---|---|---|---|
| nominal | ✗ | ✗ | ✓ |
| ordinal | ✗ | ✓ | ✓ |
| scale | ✓ | ✓ | ✓ |
| affected by extreme values | yes | no | no |

(Slide 14's table, completed: mode needs counting, median needs ordering, mean needs arithmetic.)

**Grouped waiting times** (slide 17):

| Waiting time | 0–5 | 5–10 | 10–15 | 15–20 | 20+ |
|---|---|---|---|---|---|
| frequency | 15 | 20 | 8 | 5 | 2 |
| midpoint | 2.5 | 7.5 | 12.5 | 17.5 | 22.5 |

- Median class [5–10): cumulative frequency is 15 before it and 35 after, so the 25th and 26th values lie in it.
- Modal class [5–10) (frequency 20).
- Mean from midpoints: $(37.5+150+100+87.5+45)/50=420/50=8.4$. The midpoint 22.5 for the open class `20+` is an assumption.

**Quantiles**: $Q_1$ (25% below, "lower fourth"), $Q_2$ = median, $Q_3$ (75%, "upper fourth"), percentile $k$.

**Normal QQ plot**: sample quantiles vs theoretical normal quantiles; a straight line means roughly normal, curvature means skew, an S shape means heavy or light tails. Used to check the normality assumed in [[06 - Confidence Interval]] and [[07 - Hypothesis Testing - One Sample]].

### Variability

Data can share mean and median and still differ in spread, so report both location and variability.

**Range** $=x_{\max}-x_{\min}$: simplest, uses only two values.

**Variance and standard deviation**
$$\sigma^2 = \frac{\sum_{i=1}^{N}(x_i - \mu)^2}{N},\qquad s^2 = \frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n-1},\qquad \sigma=\sqrt{\sigma^2},\ s=\sqrt{s^2}$$
The numerator is the sum of squares (SS).

Why $n-1$: deviations are measured about $\bar x$, which minimizes $\sum(x_i-c)^2$, so $\sum(x_i-\bar x)^2\le\sum(x_i-\mu)^2$ and dividing by $n$ underestimates $\sigma^2$. In fact $E[\sum(x_i-\bar x)^2]=(n-1)\sigma^2$, so dividing by $n-1$ makes $E[s^2]=\sigma^2$. Degrees of freedom: the deviations sum to zero, so only $n-1$ are free. Excel: `VAR`/`STDEV` (sample), `VARP`/`STDEVP` (population).

Report the standard deviation (same units as the data); variance is used in theory because variances of independent variables add.

**Coefficient of variation**: $CV = s/\bar{x}\times100\%$; dimensionless, compares spread across units or very different means.

| | Data | Mean | $s^2$ | $s$ | CV |
|---|---|---|---|---|---|
| Firm A | profit 5, 6, 7, 8, 9 | 7 | 2.5 | 1.58 | 22.6% |
| Firm B | profit 51, 53, 55, 57, 59 | 55 | 10 | 3.16 | 5.7% |
| Firm C | price 15, 16, 17, 18, 19 | 17 | 2.5 | 1.58 | 9.3% |

B has the largest $s$ but the smallest relative spread; A and C have equal $s$ but different CV (and different units).

**Interquartile range**: $IQR=Q_3-Q_1$, the spread of the middle 50%; robust to outliers.

**Fences** (lecture):

| | boundary |
|---|---|
| outlier | below $Q_1-1.5\,IQR$ or above $Q_3+1.5\,IQR$ |
| extreme | below $Q_1-3\,IQR$ or above $Q_3+3\,IQR$ |

Same rule as in [[Data Preparation and Visualization/contents/06 - Data Cleaning|Data Cleaning]].

**Five-number summary and boxplot**: min, $Q_1$, median, $Q_3$, max. The box spans $Q_1$–$Q_3$ with a line at the median; whiskers go to the most extreme values inside the 1.5·IQR fences; points beyond are drawn individually.

Salary example (slides 34–35, $n=100$):

| Salary | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|
| workers | 10 | 16 | 30 | 19 | 14 | 10 | 0 | 0 | 1 |

Five-number summary 10, 11, 12, 13.5, 18. Upper fence $13.5+1.5(2.5)=17.25$, so 18 is an outlier. Boxplots are good for comparing groups (slide 37: max/Q3/Q2/Q1/min/mean for 2014–2017).

**Skewness**
$$Sk = \frac{\sum(x_i - \bar{x})^3}{n s^3}$$
$Sk>0$: right skew, usually mean > median; $Sk<0$: left skew, mean < median.

### Relationship

**Covariance**: $s_{xy} = \sum (x_i - \bar{x})(y_i - \bar{y})/(n-1)$; its size depends on units, only its sign is interpretable.

**Correlation**
$$r_{xy} = \frac{s_{xy}}{s_x s_y} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum(x_i-\bar{x})^2}\sqrt{\sum(y_i-\bar{y})^2}}\in[-1,1]$$
Reference values (slide 41): strong positive 0.8, weak positive 0.5, weak negative −0.5, none 0.

**z-score**: $z_i=(x_i-\bar x)/s$ (or $(x_i-\mu)/\sigma$), the distance from the mean in standard deviations; standardized data have mean 0 and SD 1 (`StandardScaler` in [[Data Preparation and Visualization/contents/07 - Data Transformation|Data Transformation]]).

### Excel functions

| Statistic | Function |
|---|---|
| sum, mean, median, mode | `SUM`, `AVERAGE`, `MEDIAN`, `MODE` |
| quartile $k$, percentile $k$ | `QUARTILE(array, k)`, `PERCENTILE(data, k)` |
| sample variance, SD | `VAR`, `STDEV` |
| covariance, correlation | `COVAR`, `CORREL` |
| $P(X<b)$ for $X\sim N(\mu,\sigma^2)$ | `NORMDIST(b, µ, σ, 1)` |

### R

```r
x3 <- c(rep(11,8), rep(12,24), rep(13,30), rep(14,22), rep(15,12), rep(16,4))
hist(x3, breaks = c(10,11,12,13,14,15,16), col="lightgreen")
summary(x3)     # Min 11, Q1 12, Median 13, Mean 13.18, Q3 14, Max 16
var(x3)         # 1.603
sd(x3)          # 1.266
skewness(x3)    # 0.255  (package-dependent definition)
kurtosis(x3)    # -0.582 (excess kurtosis)
```

Grouped data:
```r
ll <- c(10,12,14,16,18); ul <- c(12,14,16,18,20); fr <- c(8,25,30,24,13)
mid <- (ll+ul)/2; n <- sum(fr)                  # n = 100
mean <- sum(mid*fr)/n                           # 15.18
ssq  <- sum((mid-mean)^2*fr)/(n-1)              # 5.341
s    <- sqrt(ssq)                               # 2.311
skew <- sum((mid-mean)^3*fr)/n/s^3              # 0.021
kurt <- sum((mid-mean)^4*fr)/n/s^4              # 2.117
```

## ✏️ Exercises

**1.** Mean of the grouped wage data; why is the mean of class data only approximate?

> [!example]- Solution
> $\bar x=(4\cdot7+10\cdot8+6\cdot9)/20=162/20=8.1$, exact because 7, 8, 9 are actual values. With classes like [5–10), each value is replaced by the midpoint 7.5, assuming values are symmetric within the class; if they cluster near 5, the grouped mean overstates. The error grows with class width, and open classes (`20+`) have no midpoint, so report the median there.

**2.** Complete and justify the mean/median/mode table.

> [!example]- Solution
> See the table above. Mode needs only counting (works for all types); median needs order (ordinal and scale); mean needs arithmetic (scale only). Averaging codes Bad = 1 … Very Good = 4 assumes equal gaps, which ordinal data do not guarantee. Only the mean uses magnitudes, so only it is moved by outliers: in the salary data the worker at 18 raises the mean (12.47) while the median stays 12.

**3.** Complete the three-firm table. Which firm varies most?

> [!example]- Solution
> A: deviations −2…2, SS = 10, $s^2=2.5$, $s=1.58$, CV 22.6%. B: deviations −4, −2, 0, 2, 4, SS = 40, $s^2=10$, $s=3.16$, CV 5.7%. C: SS = 10, $s=1.58$, CV 9.3%.
>
> B varies most in absolute terms; A varies most relative to its level (riskiest for an investor). A and C have the same $s$ but different CV and units. CV is meaningless when the mean is near zero or negative.

**4.** Five-number summary and outliers for the salary data.

> [!example]- Solution
> Cumulative: 10, 26, 56, 75, 89, 99, 99, 99, 100. Min 10, max 18. $Q_1$ (25th/26th) = 11; median (50th/51st) = 12; $Q_3$: 75th value 13, 76th 14 → 13.5. IQR = 2.5; fences 7.25 and 17.25; extreme fence 21. So 18 is an outlier but not extreme. The upper whisker ends at 15 (largest value inside the fence), not at 17.25. (Software may give $Q_3=13.25$ with linear interpolation; follow the textbook definition in exams.)

**5.** (Advanced) Why divide by $n-1$? Why report SD rather than variance, and correlation rather than covariance?

> [!example]- Solution
> (a) $g(c)=\sum(x_i-c)^2$ is minimized at $\bar x$, so the sum of squared deviations from $\bar x$ is smaller than from $\mu$; $E[\sum(x_i-\bar x)^2]=(n-1)\sigma^2$, so $n-1$ gives an unbiased estimate. One degree of freedom is used by estimating $\mu$; the same $n-1$ appears in the $t$-distribution ([[06 - Confidence Interval]]). With the whole population, divide by $N$.
>
> (b) Variance is in squared units (1.603 dollars² means little; $s=1.27$ dollars is interpretable), but variances of independent variables add, which is why theory uses them.
>
> (c) Covariance has the units of both variables; rescaling one rescales it. Dividing by $s_xs_y$ gives a unit-free number in [−1, 1]. Both measure only linear association and say nothing about causation.

## 📝 Summary

- Mean (uses all values, sensitive to outliers), median (robust), mode (any type).
- Mode for all types, median needs ordinal, mean needs scale.
- Grouped statistics use midpoints and are approximate.
- Sample variance divides by $n-1$; population by $N$.
- Report SD; use variance in theory.
- CV compares relative spread; IQR is robust; fences at 1.5 and 3 IQR.
- Five-number summary → boxplot; whiskers stop at the last value inside the fence.
- Skewness sign: right skew → mean > median.
- Correlation = standardized covariance, linear only; z-score = distance in SDs.

## ⚠️ Important Notes

1. $n-1$ vs $n$: `VAR`/`STDEV` are sample, `VARP`/`STDEVP` population.
2. Don't average ordinal codes; report the median or the distribution.
3. In right-skewed data the mean exceeds the median; report both.
4. CV fails when the mean is near zero or negative.
5. Whiskers end at the last data value inside the fence.
6. A boxplot can hide multimodality; pair it with a histogram.
7. Range depends only on the two extremes.
8. Covariance magnitude is not interpretable; use $r$.
9. $r$ is linear-only and sensitive to outliers; plot first.
10. Correlation does not imply causation.
11. Quartile conventions differ across software (Excel, R type 7, textbook "fourths").

> [!warning] Gaps in the source slides
> - Formulas on slides 6, 8, 10–13, 15–16, 18–20, 26–29, 31–33, 36, 38–40, 42–43, 45–46 are images; all formulas here are standard reconstructions.
> - Slides 2–4 (profit comparison of projects A and B), 21–22 (QQ plots), 28 (population vs sample formulas, the most costly gap), 45 ("Combined sample", probably pooled mean/variance) and 46 (summary) are images.
> - Slides 14, 30, 37 are tables to complete; filled in above.
> - Slide 48's side table lists `x3` as 11, 13, …, 21, but the code uses 11–16; the `summary()` output matches the code.
> - Corrected (2026-10-09): the grouped mean waiting time is 420/50 = 8.4 (an earlier version had 382.5/50 = 7.65); added the weighted price 13.95.
> - Exercise set: [1] ch. 1 (p. 31) 30, 33, 35–40; (p. 41) 41, 44, 46, 49, 50, 54, 55, 59; (p. 44) 60, 63, 67, 75, 76, 78; [4] ch. 2 (p. 67) 2.9–2.11.

**Previous:** [[02 - Tables and Charts]] · **Next:** [[04 - Sampling Distributions]]
