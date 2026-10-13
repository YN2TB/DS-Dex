---
subject: Mathematical Statistics
chapter: 02
tags: [ds, statistics, descriptive-statistics, visualization, frequency-tables]
source: "MS_Lec02_Chart.pptx — Bui Duong Hai, Faculty of Mathematical Economics, NEU"
---

# Tables and Charts

Reading: Devore & Berk ch. 1 (pp. 9–24); Miller & Miller ch. 2 (pp. 33–79). Descriptive statistics as tables and charts; [[03 - Descriptive Statistics]] reduces data to numbers.

## 📘 Main Knowledge

### Running dataset

A customer survey with $n=50$:

| No. | Sex | Age | Waiting time (min) | Evaluation |
|---|---|---|---|---|
| 1 | Female | 43 | 15 to 20 | Bad |
| 2 | Male | 23 | 0 to 5 | Good |
| 3 | Female | 36 | 5 to 10 | Very Good |
| … | | | | |
| 50 | Female | 28 | 10 to 15 | Fair |

Sex is binary/nominal, Evaluation ordinal, Age scale, Waiting time scale (already grouped).

### Frequency tables

| Sex | Male | Female |
|---|---|---|
| frequency | 20 | 30 |
| relative frequency | 0.4 | 0.6 |

Frequency $f_i$ is the count; relative frequency $f_i/n$ makes datasets of different sizes comparable.

| Evaluation | Very Good | Good | Fair | Bad | Total |
|---|---|---|---|---|---|
| frequency | 10 | 25 | 9 | 6 | 50 |
| % | 20% | 50% | 18% | 12% | 100% |

**Pie chart**: part-to-whole; categories must be mutually exclusive and exhaustive. Use sparingly ([[Data Preparation and Visualization/contents/11 - Chart Design and Data Storytelling|Chart Design]]).

**Column chart**: better for ordinal data like Evaluation, because the axis keeps the order that a pie loses.

### Cross tables

| | Very Good | Good | Fair | Bad | Sum |
|---|---|---|---|---|---|
| Male | 6 | 11 | 2 | 1 | 20 |
| Female | 4 | 14 | 7 | 5 | 30 |
| Sum | 10 | 25 | 9 | 6 | 50 |

Marginal totals give each variable's own distribution. Three ways to compute percentages:

**Grand %** (cell / 50):

| | VG | G | F | B | Sum |
|---|---|---|---|---|---|
| Male | 12% | 22% | 4% | 2% | 40% |
| Female | 8% | 28% | 14% | 10% | 60% |

Answers "what share of all customers are females who rated Bad?"

**Column %** (cell / column total):

| | VG | G | F | B | Total |
|---|---|---|---|---|---|
| Male | 60% | 44% | 22% | 17% | 40% |
| Female | 40% | 56% | 78% | 83% | 60% |

Answers "of those who rated Bad, what share were female?" (83%).

**Row %** (cell / row total):

| | VG | G | F | B | Sum |
|---|---|---|---|---|---|
| Male | 30% | 55% | 10% | 5% | 100% |
| Female | 13% | 47% | 23% | 17% | 100% |
| Grand | 20% | 50% | 18% | 12% | 100% |

Answers "of female customers, what share rated Bad?" (17%).

"83% of Bad ratings came from women" and "17% of women rated Bad" describe the same cell and mean different things. Choose the direction that matches the question and label it.

Charts: grouped columns compare categories; stacked columns show composition.

### Grouping scale variables

Ungrouped age gives 14 thin bars:

| Age | 23 | 26 | 28 | 32 | 35 | 36 | 38 | 40 | 43 | 47 | 50 | 54 | 58 | 63 | Sum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| freq | 1 | 2 | 2 | 2 | 4 | 3 | 5 | 8 | 7 | 4 | 5 | 4 | 2 | 1 | 50 |

5-year classes:

| Age | 20–24 | 25–29 | 30–34 | 35–39 | 40–44 | 45–49 | 50–54 | 55–59 | 60–64 | Sum |
|---|---|---|---|---|---|---|---|---|---|---|
| freq | 1 | 4 | 2 | 12 | 15 | 4 | 9 | 2 | 1 | 50 |
| % | 2% | 8% | 4% | 24% | 30% | 8% | 18% | 4% | 2% | 100% |

10-year classes:

| Age | 20–29 | 30–39 | 40–49 | 50–59 | 60–69 | Sum |
|---|---|---|---|---|---|---|
| freq | 5 | 14 | 19 | 11 | 1 | 50 |
| % | 10% | 28% | 38% | 22% | 2% | 100% |

Class width matters: too narrow shows noise, too wide hides shape (compare `KBinsDiscretizer` in [[Data Preparation and Visualization/contents/07 - Data Transformation|Data Transformation]]).

### Histogram

The column chart of a grouped scale variable. Its bars touch, because the x-axis is a continuous number line; a bar chart of categories has gaps.

| Waiting time | Freq | % | Cumulative |
|---|---|---|---|
| [0 – 5) | 15 | 30% | 30% |
| [5 – 10) | 20 | 40% | 70% |
| [10 – 15) | 8 | 16% | 86% |
| [15 – 20) | 5 | 10% | 96% |
| 20+ | 2 | 4% | 100% |

`[0 – 5)` is closed on the left, open on the right: 5 belongs to the second class, so boundary values are never counted twice.

### Cumulative chart (ogive)

| Age | Freq | % | Cumulative |
|---|---|---|---|
| 20–29 | 5 | 10% | 10% |
| 30–39 | 14 | 28% | 38% |
| 40–49 | 19 | 38% | 76% |
| 50–59 | 11 | 22% | 98% |
| 60+ | 1 | 2% | 100% |

Cumulative % answers "what share is at most this value?" (76% are under 50). The slide calls it "Ogive, Pareto chart". It is the empirical distribution function; read backwards it gives percentiles ([[03 - Descriptive Statistics]]).

### Distribution shape

- Symmetric: bell-shaped; bimodal (two peaks, often two mixed groups); uniform.
- Skewed: positive/right (long right tail: income, waiting times, prices); negative/left (long left tail: exam scores near a ceiling).

Skew is why mean and median differ ([[03 - Descriptive Statistics]]) and why non-parametric methods exist ([[09 - Non-parametric Testing]]).

### Stem-and-leaf

Data 21, 22, 32, 34, 34, 35, 40, 42, 46, 48, 49, 52, 52, 57, 61:
```
2 | 1 2
3 | 2 4 4 5
4 | 0 2 6 8 9
5 | 2 2 7
6 | 1
```
Shows the shape and keeps every value. For three-digit data (329, 332, 335, …) the stem is the first two digits.

### Other charts

- **Line chart**: time series ([[Time-series Analysis/contents/00-Index|Time-series Analysis]]).
- **Combined chart**: two series with different units (VN Index and volume); beware dual axes.
- **Radar chart**: several variables on the same scale for a few units:

| Dimension | Staff A | Staff B |
|---|---|---|
| Knowledge | 50 | 80 |
| Skill | 50 | 90 |
| Learning | 60 | 80 |
| Discipline | 65 | 75 |
| Attitude | 80 | 60 |
| Harmony | 90 | 50 |
| Loyalty | 85 | 30 |

- **Scatter plot**: two scale variables measured on the same units ("pair sample, dependent sample"):

| Labor | 11 | 11 | 12 | 13 | 13 | 13 | 15 | 14 | 15 | 16 | 17 | 18 | 18 | 17 | 19 | 19 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Output | 80 | 130 | 150 | 110 | 150 | 200 | 250 | 180 | 170 | 220 | 210 | 240 | 200 | 260 | 240 | 280 |

Reference patterns (slide 23): strong positive $r=0.8$, weak positive 0.5, weak negative −0.5, none 0.

- **Bubble chart**: scatter plus a third variable as bubble size:

| Project | R&D | Adv. | Profit |
|---|---|---|---|
| A | 30 | 35 | 50 |
| B | 40 | 25 | 40 |
| C | 45 | 50 | 18 |
| D | 15 | 45 | 22 |
| E | 50 | 10 | 15 |
| F | 10 | 30 | 20 |

## ✏️ Exercises

**1.** From the cross table: (a) % of all customers who are females rating Bad; (b) of Bad ratings, % female; (c) of females, % rating Bad. Which percentage type is each?

> [!example]- Solution
> (a) Grand: $5/50=10\%$ ($P(F\cap B)$). (b) Column: $5/6=83\%$ ($P(F\mid B)$). (c) Row: $5/30=17\%$ ($P(B\mid F)$). Confusing (b) and (c) is the base-rate fallacy. (c) measures how often women have a bad experience; (b) also depends on women being 60% of the sample.

**2.** Bar chart vs histogram: why does it matter?

> [!example]- Solution
> Bar chart: categories, gaps, order can be chosen. Histogram: classes of a scale variable, touching bars, order fixed by the number line. Reordering a histogram is meaningless; reordering bars by frequency is good practice. Bin width changes a histogram's message. A histogram encodes frequency by area, so with unequal widths the height must be frequency density (frequency ÷ width).

**3.** Explain `[0 – 5)` and compute the share waiting under 15 minutes.

> [!example]- Solution
> `[0 – 5)` contains $0\le x<5$, so classes are mutually exclusive and exhaustive; "0–5, 5–10" would count 5 twice. Under 15 minutes: $30\%+40\%+16\%=86\%$ (the cumulative column). The open class `20+` has no midpoint, so a mean from the grouped table needs an assumption.

**4.** Pie or column chart for Evaluation? What about comparing two branches?

> [!example]- Solution
> Column chart: Evaluation is ordinal and the axis shows the order (peak at Good, tail toward Bad); a pie loses it, and angles are harder to compare than lengths (18% vs 20%). For two branches use grouped columns (compare categories) or 100% stacked columns (compare composition when branch sizes differ), never two pies.

**5.** (Advanced) What does "pair sample (dependent sample)" mean for a scatter plot, and what can the plot show that $r$ cannot?

> [!example]- Solution
> Both variables are measured on the same unit (each factory gives a labour and an output value), so points are real pairs. Two independent samples could be paired arbitrarily to create any correlation. The paired/independent distinction drives [[08 - Inferences on Two Samples]].
>
> The plot shows what $r$ hides: non-linear patterns ($y=x^2$ on a symmetric range gives $r\approx0$), outliers that create or destroy correlation, clusters and Simpson's paradox, and spread that changes with $x$. Anscombe's quartet: four datasets with $r=0.816$ that look completely different. For the labour/output data the plot is roughly linear and positive, so $r$ is a fair summary.

## 📝 Summary

- Frequency and relative frequency; cross tables with marginals.
- Grand, column and row percentages answer different questions.
- Pie for part-to-whole; column chart for ordered categories; never compare pies.
- Group scale variables into classes; class width is a choice.
- Histogram bars touch; classes use `[a, b)`.
- The ogive gives cumulative shares and percentiles.
- Shapes: bell, bimodal, uniform; right/left skew.
- Stem-and-leaf keeps all values; line, radar, scatter and bubble charts for other structures.

## ⚠️ Important Notes

1. Row % and column % are both correct and mean different things; state the base.
2. Use `[a, b)` classes.
3. Open-ended classes have no midpoint.
4. Report the class width you chose.
5. With unequal widths, plot frequency density.
6. Don't reorder histogram bars.
7. Bimodal data usually mix two groups; split before summarizing.
8. $r$ measures linear association only; always plot.
9. Dual-axis charts can make any two series look related.
10. Radar charts need a common scale, and their shape depends on the order of the axes.

> [!warning] Gaps in the source slides
> - All chart images are pictures; only the data tables and captions extracted.
> - Slide 17 (shape illustrations), the second stem-and-leaf diagram (slide 18), the VN Index line/combined chart (slides 19–20) and the scatter patterns (slide 23) are images.
> - Exercise set: [1] ch. 1 (p. 21) 14, 15, 20, 24, 27; [4] ch. 1 (p. 34) 1.9, 1.10, 1.13, 1.17; (p. 39) 1.20–1.29; (p. 49) 1.32, 1.34, 1.36; (p. 54) 1.49, 1.50. Textbook [4] is not in `documents/`.

**Previous:** [[01 - Introduction to Statistics]] · **Next:** [[03 - Descriptive Statistics]]
