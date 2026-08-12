---
subject: Mathematical Statistics
chapter: 02
tags: [ds, statistics, descriptive-statistics, visualization, frequency-tables]
source: "MS_Lec02_Chart.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Tables and Charts

> [!note] Reading
> **[1] Devore & Berk, Ch. 1, pp. 9–24** · **[2] Miller & Miller, Ch. 2, pp. 33–79**
>
> This is descriptive statistics in its **presentational** form — organising raw data into tables and charts. [[03 - Descriptive Statistics]] then reduces data to single numbers.

## 📘 Main Knowledge

### The running dataset

A customer survey, $n = 50$ observations:

| No. | Sex | Age (year) | Waiting time (min) | Evaluation |
|---|---|---|---|---|
| 1 | Female | 43 | 15 to 20 | Bad |
| 2 | Male | 23 | 0 to 5 | Good |
| 3 | Female | 36 | 5 to 10 | Very Good |
| … | | | | |
| 50 | Female | 28 | 10 to 15 | Fair |

Four variables spanning three types — `Sex` (binary/nominal), `Evaluation` (ordinal), `Age` (scale), `Waiting time` (scale, pre-grouped). The chapter shows which table and chart each type admits, following the classification from [[01 - Introduction to Statistics]].

### Frequency and relative frequency

The starting point for any categorical variable: count each value, then express as a proportion.

| Sex | Male | Female |
|---|---|---|
| **Frequency** | 20 | 30 |
| **Relative frequency** | 0.4 (40%) | 0.6 (60%) |

**Frequency** $f_i$ = the count. **Relative frequency** $= f_i / n$, expressed as a proportion or percent. Relative frequency is what makes datasets of different sizes comparable.

### Pie chart

| Evaluation | Very Good | Good | Fair | Bad |
|---|---|---|---|---|
| Freq. | 10 | 25 | 9 | 6 |
| % | 20% | 50% | 18% | 12% |

Pie charts show **part-to-whole** structure. They require categories to be **mutually exclusive and exhaustive**, summing to 100%. See [[Data Preparation and Visualization/contents/11 - Chart Design and Data Storytelling|Chart Design]] for why they should be used sparingly.

### Column chart

| Evaluation | Freq. | % |
|---|---|---|
| Very Good | 10 | 20% |
| Good | 25 | 50% |
| Fair | 9 | 18% |
| Bad | 6 | 12% |
| **TOTAL** | **50** | **100%** |

For **ordinal** data like `Evaluation`, the column chart is strictly better than the pie: the categories have a natural order, which a bar chart preserves along the axis and a pie chart destroys.

### Cross (contingency) tables

Two categorical variables at once — the joint frequency distribution:

| Evaluation | Very Good | Good | Fair | Bad | **Sum** |
|---|---|---|---|---|---|
| **Male** | 6 | 11 | 2 | 1 | **20** |
| **Female** | 4 | 14 | 7 | 5 | **30** |
| **Sum** | 10 | 25 | 9 | 6 | **50** |

The marginal totals (right column, bottom row) recover each variable's individual distribution.

**Three ways to percentage a cross table — and they answer different questions.**

**Grand-percent** (each cell ÷ grand total, all cells sum to 100%):

| | Very Good | Good | Fair | Bad | Sum |
|---|---|---|---|---|---|
| Male | 12% | 22% | 4% | 2% | 40% |
| Female | 8% | 28% | 14% | 10% | 60% |
| Sum | 20% | 50% | 18% | 12% | 100% |

*Answers:* "What share of all customers are dissatisfied males?"

**Column-percent** (each cell ÷ its column total, columns sum to 100%):

| | Very Good | Good | Fair | Bad | TOTAL |
|---|---|---|---|---|---|
| Male | 60% | 44% | 22% | 17% | 40% |
| Female | 40% | 56% | 78% | 83% | 60% |
| Sum | 100% | 100% | 100% | 100% | 100% |

*Answers:* "Of those who rated us Bad, what proportion were female?" → 83%

**Row-percent** (each cell ÷ its row total, rows sum to 100%):

| | Very Good | Good | Fair | Bad | Sum |
|---|---|---|---|---|---|
| Male | 30% | 55% | 10% | 5% | 100% |
| Female | 13% | 47% | 23% | 17% | 100% |
| **GRAND** | 20% | 50% | 18% | 12% | 100% |

*Answers:* "Of female customers, what proportion rated us Bad?" → 17%

> [!warning] Column-% and row-% are not interchangeable
> "83% of Bad ratings came from women" and "17% of women gave a Bad rating" are **both true of the same table** and mean completely different things. Confusing them is the **base rate fallacy** — and it is the single most common misreading of a cross table. Choose the percentage direction that matches the question, and label it explicitly.

**Charts for cross tables:** a **grouped column chart** (bars side by side) compares categories directly; a **stacked column chart** shows composition within each group.

### Scale variables: from raw values to grouped classes

A scale variable with many distinct values makes a poor column chart. Age, ungrouped:

| Age | 23 | 26 | 28 | 32 | 35 | 36 | 38 | 40 | 43 | 47 | 50 | 54 | 58 | 63 | Sum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Freq. | 1 | 2 | 2 | 2 | 4 | 3 | 5 | 8 | 7 | 4 | 5 | 4 | 2 | 1 | 50 |

Fourteen thin bars with no shape. **Grouping into classes** fixes this — first into 5-year bands:

| Age | 20–24 | 25–29 | 30–34 | 35–39 | 40–44 | 45–49 | 50–54 | 55–59 | 60–64 | Sum |
|---|---|---|---|---|---|---|---|---|---|---|
| Freq. | 1 | 4 | 2 | 12 | 15 | 4 | 9 | 2 | 1 | 50 |
| % | 2% | 8% | 4% | 24% | 30% | 8% | 18% | 4% | 2% | 100% |

then into 10-year bands:

| Age | 20–29 | 30–39 | 40–49 | 50–59 | 60–69 | Sum |
|---|---|---|---|---|---|---|
| Freq. | 5 | 14 | 19 | 11 | 1 | 50 |
| % | 10% | 28% | 38% | 22% | 2% | 100% |

**Bin width is a real analytical choice** — too narrow and you see noise, too wide and you erase the shape. Compare `KBinsDiscretizer` and the `n_bins` trade-off in [[Data Preparation and Visualization/contents/07 - Data Transformation|Data Transformation]].

### Histogram

A **histogram** is the column chart of a grouped scale variable. It differs from a bar chart in a way worth stating precisely: **its bars touch**, because the horizontal axis is a continuous number line with no gaps between classes. A bar chart of categories has gaps because the categories are separate.

| Waiting time | Freq | % | Cumulative |
|---|---|---|---|
| [0 – 5) | 15 | 30% | 30% |
| [5 – 10) | 20 | 40% | 70% |
| [10 – 15) | 8 | 16% | 86% |
| [15 – 20) | 5 | 10% | 96% |
| 20+ | 2 | 4% | 100% |

Note the interval notation `[0 – 5)` — **closed on the left, open on the right**. A value of exactly 5 falls in the *second* class. Without this convention, boundary values would be counted twice.

### Cumulative chart (Ogive)

| Age | Freq. | % | Cumulative |
|---|---|---|---|
| 20–29 | 5 | 10% | 10% |
| 30–39 | 14 | 28% | 38% |
| 40–49 | 19 | 38% | 76% |
| 50–59 | 11 | 22% | 98% |
| 60+ | 1 | 2% | 100% |

The cumulative column answers "what proportion are **at most** this?" — 76% of customers are under 50. The lecture notes this is *"also called: Ogive, Pareto chart."*

The cumulative relative frequency is the **empirical distribution function**, and reading it backwards gives the **percentiles** used throughout [[03 - Descriptive Statistics]].

### Distribution shape

The vocabulary for describing a histogram's form:

**Symmetrical:**
- **Bell shaped** — the normal-like form underpinning most of this course
- **Two-tailed** (bimodal) — two peaks, usually a sign of two mixed subpopulations
- **Uniform** — flat, all classes roughly equal

**Asymmetrical / Skewed:**
- **Positively (Right) skewed** — a long tail toward high values. Typical of income, waiting times, and prices.
- **Negatively (Left) skewed** — a long tail toward low values. Typical of exam scores with a ceiling.

Shape determines which summary statistic is honest: **skew is precisely why the mean and median diverge** ([[03 - Descriptive Statistics]]) and why non-parametric methods exist ([[09 - Non-parametric Testing]]).

### Stem-and-leaf diagram

Splits each value into a **stem** (leading digits) and a **leaf** (final digit):

Data: 21, 22, 32, 34, 34, 35, 40, 42, 46, 48, 49, 52, 52, 57, 61

```
2 | 1  2
3 | 2  4  4  5
4 | 0  2  6  8  9
5 | 2  2  7
6 | 1
```

Its advantage over a histogram: it shows the distribution's shape **while preserving every original value**. You can still read off that the data contains 34 twice. For the second example (329, 332, 335, …) the stem becomes the first *two* digits.

### Charts for other structures

**Line chart** — for **time series**. Order along the x-axis is meaningful, so points are connected. See [[Time-series Analysis/contents/00-Index|Time-series Analysis]].

**Combined chart** — two series with different units on one figure (the slide's example: VN Index and transaction volume). Convenient, but see the dual-axis warning below.

**Radar (spider web) chart** — several variables **on the same scale**, compared across a few units:

| Dimension | Staff A | Staff B |
|---|---|---|
| Knowledge | 50 | 80 |
| Skill | 50 | 90 |
| Learning | 60 | 80 |
| Discipline | 65 | 75 |
| Attitude | 80 | 60 |
| Harmony | 90 | 50 |
| Loyalty | 85 | 30 |

The shared scale is essential — mixing units makes the enclosed area meaningless.

**Scatter plot** — two scale variables, *"using for pair sample (dependent sample)"*, i.e. both measured on the same unit:

| Labor | 11 | 11 | 12 | 13 | 13 | 13 | 15 | 14 | 15 | 16 | 17 | 18 | 18 | 17 | 19 | 19 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Output | 80 | 130 | 150 | 110 | 150 | 200 | 250 | 180 | 170 | 220 | 210 | 240 | 200 | 260 | 240 | 280 |

**Reading correlation from a scatter plot** (slide 23) — the lecture's reference values:

| Pattern | $r$ |
|---|---|
| Strong positive | 0.8 |
| Weak positive | 0.5 |
| Weak negative | −0.5 |
| No correlation | 0 |

**Bubble chart** — a scatter plot with a third variable encoded as bubble size:

| Project | R&D | Adv. | Profit |
|---|---|---|---|
| A | 30 | 35 | 50 |
| B | 40 | 25 | 40 |
| C | 45 | 50 | 18 |
| D | 15 | 45 | 22 |
| E | 50 | 10 | 15 |
| F | 10 | 30 | 20 |

## ✏️ Exercises

**1.** From the cross table, answer: (a) what % of all customers are females who rated "Bad"? (b) Of those rating "Bad", what % are female? (c) Of females, what % rated "Bad"? State which percentage type each requires.

> [!example]- Solution
> Female + Bad = 5; total = 50; Bad column total = 6; Female row total = 30.
>
> **(a) Grand-percent:** $5/50 = 10\%$
> **(b) Column-percent:** $5/6 = 83\%$
> **(c) Row-percent:** $5/30 = 17\%$
>
> All three describe the same cell, and they differ by nearly a factor of eight. The distinction is which total sits in the denominator, i.e. **which population you are conditioning on**.
>
> In probability notation the difference is stark: (a) is the joint $P(F \cap B)$, (b) is $P(F \mid B)$, (c) is $P(B \mid F)$. Confusing (b) with (c) is the **base rate fallacy** — the same error as reading "80% of accidents involve local drivers" as "local drivers are dangerous", when it may simply be that most drivers are local.
>
> For a headline about customer experience, **(c) is the right number**: it measures the rate at which women have a bad experience. **(b) confounds the answer with how many women are in the sample** — with 30 women and 20 men, women will dominate any category by construction.

**2.** Explain the difference between a bar chart and a histogram, and why it is not merely cosmetic.

> [!example]- Solution
> **Bar chart** — categorical variable; bars are **separated by gaps**; order is arbitrary (or chosen for readability); each bar is one category.
>
> **Histogram** — scale variable grouped into classes; bars **touch**; order is fixed by the number line; each bar is an interval.
>
> **Why it matters:** the touching bars assert that the x-axis is **continuous** — that the space between 30 and 40 contains real values that were measured and allocated to a class. Gaps in a bar chart assert the opposite: nothing exists between "Male" and "Female".
>
> Two practical consequences follow. **Reordering** a histogram's bars is meaningless — a nonsensical operation — whereas reordering a bar chart by frequency is good practice. And **bin width changes a histogram's message**: the age data looks quite different in 5-year versus 10-year bands, while a bar chart's categories are given by the data and cannot be retuned.
>
> Strictly, a histogram's **area** should be proportional to frequency, so with unequal class widths the bar *height* must be frequency **density** (frequency ÷ width), not raw frequency. With equal widths, as in the slides, height and density are proportional and the distinction is invisible — which is why it is so often forgotten.

**3.** The waiting-time table uses class notation `[0 – 5)`, `[5 – 10)`. Explain the convention and what breaks without it. Then compute the proportion of customers waiting under 15 minutes.

> [!example]- Solution
> `[0 – 5)` is **closed on the left, open on the right**: it contains every value $x$ with $0 \le x < 5$. A value of exactly 5 belongs to `[5 – 10)`, not to the first class.
>
> **Without the convention, classes overlap.** Written as "0–5" and "5–10", a customer waiting exactly 5 minutes qualifies for both, so different analysts get different tables from identical data, frequencies may exceed $n$, and the relative frequencies no longer sum to 100%. Classes must be **mutually exclusive and exhaustive** — this notation guarantees it.
>
> **Under 15 minutes** is the cumulative frequency at the boundary of the third class:
> $$30\% + 40\% + 16\% = 86\%$$
> — read directly from the Cumulative column, which is exactly what it is for.
>
> Note that "under 15" is unambiguous here *because* of the convention: it is precisely `[0,15)`, the union of the first three classes, with no boundary case to argue about. And the final class, `20+`, is **open-ended** — it has no upper bound, so its midpoint is undefined and a mean cannot be computed from the grouped table without an assumption.

**4.** The `Evaluation` variable is presented as both a pie chart and a column chart. Which is more appropriate, and why? What if you wanted to compare evaluations across two branches?

> [!example]- Solution
> **The column chart is better**, because `Evaluation` is **ordinal**: Very Good > Good > Fair > Bad. A column chart lays that order along an axis, so the reader sees the distribution's *shape* — here a peak at "Good" with a tail toward dissatisfaction. **A pie chart destroys the ordering**, since a circle has no beginning or end, reducing an ordered scale to four unordered wedges.
>
> The perceptual argument compounds it: length from a common baseline is judged accurately, angle is not. Comparing "Fair" (18%) against "Very Good" (20%) is immediate with bars and near-impossible with slices.
>
> **For two branches: use a grouped or stacked column chart — never two pie charts.** This is an explicit rule in [[Data Preparation and Visualization/contents/11 - Chart Design and Data Storytelling|Chart Design]]: *"Don't use multiple pie charts for comparison. Slice sizes are very difficult to compare side-by-side. Use a stacked bar chart instead."*
>
> Which to choose depends on the question. **Grouped** (bars side by side) if branch sizes differ and you want to compare each category directly. **100% stacked** if you want to compare the *composition* of satisfaction independent of branch size — the right choice when one branch has 500 customers and the other 50, since raw counts would otherwise be incomparable.

**5.** (Advanced) The scatter plot is described as *"using for pair sample (dependent sample)"*. Explain what that means, why it matters, and what a scatter plot can reveal that a correlation coefficient cannot.

> [!example]- Solution
> **A paired (dependent) sample** means both variables are measured **on the same unit** — the same factory contributes both its Labor value and its Output value. The rows are matched, so point $i$ is a genuine $(x_i, y_i)$ pair.
>
> **Why it matters:** the pairing is what makes a scatter plot meaningful at all. Two *independent* samples — labour figures from one set of factories, output from a different set — have no basis for pairing; you could sort them arbitrarily and manufacture any correlation you like. This distinction governs the whole of [[08 - Inferences on Two Samples]], where paired and independent samples require different tests, and it is why paired designs are more powerful: they remove between-unit variation.
>
> **What the plot shows that $r$ cannot:**
>
> - **Non-linear relationships.** $r$ measures *linear* association only. A perfect parabola $y = x^2$ over a symmetric range gives $r \approx 0$ — the coefficient reports "no relationship" while the plot shows a deterministic one.
> - **Outliers.** A single extreme point can drag $r$ from 0 to 0.8, or mask a strong relationship. The plot exposes it; the number conceals it.
> - **Clusters and subgroups.** Two distinct groups, each with no internal correlation, can produce a strong pooled $r$ — or reverse its sign entirely (**Simpson's paradox**).
> - **Heteroskedasticity.** Spread widening with $x$ violates the assumptions of regression inference, and is invisible in $r$.
>
> The canonical demonstration is **Anscombe's quartet**: four datasets with identical means, variances, and correlation ($r = 0.816$), that look nothing alike — one linear, one curved, one linear with an outlier, one a vertical stack with a single leverage point.
>
> **Always plot before trusting the coefficient.** For the slide's Labor/Output data the relationship does look positive and roughly linear, so $r$ is a fair summary — but that is a conclusion drawn *from the plot*, not an assumption made before it.

## 📝 Summary

- **Frequency** = count; **relative frequency** = count ÷ $n$, which makes different-sized datasets comparable.
- **Cross tables** show two categorical variables jointly; marginals recover each one alone.
- **Three percentage directions — grand, column, row — answer different questions.** Confusing column-% with row-% is the base rate fallacy.
- **Pie for part-to-whole, column for ordered categories.** Never two pies side by side.
- **Scale variables must be grouped into classes** before charting; bin width is a genuine analytical choice.
- **A histogram's bars touch** because the axis is continuous; a bar chart's do not. Reordering a histogram is meaningless.
- **Class notation `[a – b)` is closed-left, open-right**, guaranteeing mutually exclusive, exhaustive classes.
- **Cumulative frequency (ogive)** answers "what proportion is at most this?" and yields percentiles.
- **Shape vocabulary:** symmetric (bell, bimodal, uniform) vs skewed (right/positive, left/negative).
- **Stem-and-leaf shows the shape while preserving every original value.**
- **Line for time series, radar for same-scale multi-dimension, scatter for paired scale variables, bubble to add a third.**

## ⚠️ Important Notes

**Row-% and column-% mean different things and are both "correct".** "83% of Bad ratings came from women" ≠ "17% of women rated Bad". Always state the base explicitly.

**Class intervals must be mutually exclusive and exhaustive.** Use `[a, b)` notation. "0–5, 5–10" is ambiguous at every boundary.

**Open-ended classes (`20+`, `60+`) have no midpoint**, so a mean cannot be computed from the grouped table without assuming an upper bound.

**Bin width changes the story.** The age data reads differently in 5-year and 10-year bands. Bin choice is an analytical decision that should be reported, not a default to be accepted.

**With unequal class widths, plot frequency *density* (frequency ÷ width), not frequency.** A histogram encodes frequency as **area**; unequal widths with raw-frequency heights systematically exaggerate the wider classes.

**Histograms cannot be reordered; bar charts should be.** The x-axis of a histogram is a number line.

**Bimodal shape usually means two mixed subpopulations.** Summarising it with one mean describes a value that may occur in neither group. Disaggregate before summarising.

**$r$ measures linear association only.** A perfect parabola gives $r \approx 0$; a single outlier can create or destroy a correlation. Plot first — Anscombe's quartet is the standing warning.

**Avoid dual-axis "combined" charts where possible.** With two independent scales you can make two series appear to converge, diverge, or cross at will; the apparent relationship is an artefact of the scale choice.

**Radar charts require a common scale across all dimensions**, and their enclosed area depends on the arbitrary order of the axes — reordering the spokes changes the shape without changing the data.

> [!warning] Gaps in the source slides
> All **chart images are embedded pictures** — only the underlying data tables and captions extracted. So the specific visual examples (pie, column, stacked, histogram, ogive, line, radar, scatter, bubble) are **not recoverable**; the data behind each is, and is reproduced above.
> - **Slide 17 (Distribution shape)** — the shape illustrations are images; only the labels survive.
> - **Slide 18 (Stem and Leaf)** — the first diagram extracted as a table; the **second example (329, 332, 335, …) has no extracted diagram**, though its data is listed.
> - **Slides 19–20 (Line chart, Combined chart)** — VN Index example is an image with no data table.
> - **Slide 23 (Relationship)** — the four scatter patterns are images; the $r$ values (0.8, 0.5, −0.5, 0) and labels survive.
>
> **Exercises set:** [1] Ch. 1 (p. 21) 14, 15, 20, 24, 27 · [4] Ch. 1 (p. 34) 1.9, 1.10, 1.13, 1.17; (p. 39) 1.20, 1.21, 1.22–1.29; (p. 49) 1.32, 1.34, 1.36; (p. 54) 1.49, 1.50. **Textbook [4] (Anderson et al.) is not in `documents/`.**

---
**Previous:** [[01 - Introduction to Statistics]] · **Next:** [[03 - Descriptive Statistics]]
