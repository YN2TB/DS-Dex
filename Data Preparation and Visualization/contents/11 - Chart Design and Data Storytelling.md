---
subject: Data Preparation and Visualization
chapter: 11
tags: [ds, visualization, design, storytelling, communication]
source: "Hubspot_Data_Visualization_101_How_to_Design_Charts_and_Graphs.pdf (HubSpot × Visage)"
---

# Chart Design and Data Storytelling

Closes Part 3 and the course: [[10 - Visualization with Matplotlib and Seaborn]] covered how to draw; this chapter covers what to draw. The source is an industry design guide (HubSpot × Visage), consistent with Knaflic's *Storytelling with Data* (the Part 3 course text).

## 📘 Main Knowledge

The guide: "If your data is misrepresented or presented ineffectively, key insights and understanding are lost, which hurts both your message and your reputation."

### 1. Find the story first

Decide what relationship you want to show before choosing a chart. Places to look:

| Pattern | Example |
|---|---|
| trends | ice cream sales over time |
| correlations | sales vs temperature |
| outliers | sales in an unusual region |

### 2. Know your data

| Type | Definition | Example |
|---|---|---|
| categorical | grouped by category | product types |
| quantitative | numeric, countable or measurable | |
| discrete | numeric with a finite set of values | number of employees |
| continuous | measured within a range | yearly rainfall |

The same distinction drives encoding ([[07 - Data Transformation]]) and test choice ([[08 - Feature Selection]]).

**Seven data relationships**

| Relationship | Shows | Example |
|---|---|---|
| time-series | change of a metric over time | monthly sales |
| ranking | relative magnitude | months from hottest to coldest |
| part-to-whole | a subset vs the whole | % of customers buying a product |
| deviation | distance from the mean | park visits on a rainy vs normal day |
| distribution | how values spread | heights of basketball players |
| correlation | variables moving together | salary by education level |
| nominal comparison | simple comparison of subcategories | visitors to several websites |

Identify the relationship, then pick the chart that shows it.

### 3. Chart types

**Bar chart**: change over time, comparing categories, parts of a whole; the most versatile.
- Vertical (column): time order (left to right), negative values.
- Horizontal: long category labels.
- Stacked: several part-to-whole relationships.
- 100% stacked: when only the percentage split matters.

Best practices: start the y-axis at 0; horizontal labels; order data (alphabetically, sequentially or by value); gap between bars ≈ half a bar's width; one colour, with an accent colour only for a key point.

**Pie chart**: part-to-whole with few categories. Stephen Few's criticism (quoted in the guide): we judge slices reliably only near familiar angles (25%, 50%, 75%, 100%); other angles are read inconsistently. People compare lengths and positions more accurately than angles and areas, so a bar chart is usually better.
- At most 5 categories; group small ones into "Other" (check it hides nothing important).
- Don't compare several pies; use a stacked bar.
- Order slices: largest at 12 o'clock clockwise and the second largest at 12 o'clock counterclockwise, the rest counterclockwise; or largest at 12 o'clock and the rest descending clockwise.
- Values must total 100%.

**Line chart**: time series of continuous data (trend, acceleration, volatility).
- At most 4 lines; solid lines only.
- Data should fill about two-thirds of the y-axis.
- Include a zero baseline if possible; truncation is acceptable when small fluctuations matter (stock prices).
- Label lines directly instead of using a legend.

Why the rules differ: a bar encodes value as length from the axis, so a truncated axis falsifies the ratio between bars; a line encodes position and is read as slope, so truncation can be justified.

**Area chart**: time series showing volume. Standard, stacked (contributions to a total) and 100% stacked (shares). At most 4 categories; put highly variable categories on top; start at 0; transparent colours; not for discrete data (the connected area implies values in between).

**Scatter plot**: correlation in large datasets. Start the y-axis at 0; add trend lines (at most 2); encode extra variables with size and colour.

**Bubble chart**: nominal comparison or ranking (bubble plot; bubble map for regions). Size bubbles by area, not diameter; keep labels visible; use circles, not odd shapes.

**Heat map**: values by colour intensity over a map or table. Simple outlines; one hue in shades or two analogous colours, darker = more; at most one pattern overlay; 3–5 ranges with roughly even distribution, +/− at the extremes.

### 4. Ten do's and don'ts

Do:
1. Use one colour per category.
2. Order data in a logical hierarchy.
3. Use callouts for important points.
4. Make values easy to compare.
5. Use icons to reduce labelling.

Don't:
6. Use high-contrast pairs like red/green or blue/yellow.
7. Use 3D charts.
8. Add chart junk (ornaments, drop shadows).
9. Use more than 6 colours in one layout.
10. Use distracting fonts (bold, italic, underline).

Most rules come down to Tufte's data-ink ratio: ink should carry information. Red/green also matters because red-green colour deficiency affects about 8% of men.

## ✏️ Exercises

**1.** Name the relationship and chart: (a) "our top 3 products by revenue"; (b) "marketing spend drives signups"; (c) "mobile grew from 20% to 60% of traffic over five years"; (d) "most support tickets are resolved in 2–4 hours".

> [!example]- Solution
> (a) Ranking → horizontal bar chart, sorted descending (product names are long). Not a pie: it compares magnitudes.
> (b) Correlation → scatter plot with a trend line. A trend line shows association, not causation.
> (c) Part-to-whole over time → 100% stacked area (or 100% stacked bars for a few years): the share matters, not the total.
> (d) Distribution → histogram. An average of 3 hours fits both "all at 3 hours" and "half at 1, half at 5".

**2.** A bar chart of quarterly revenue starts the y-axis at \$4.8M, so Q4 (\$5.2M) looks four times Q1 (\$4.9M). What is wrong, and why is the criticism weaker for a line chart?

> [!example]- Solution
> Visible bar lengths are 0.1 and 0.4: a 300% visual increase for a real increase of $5.2/4.9-1=6.1\%$. The guide: starting above zero "truncates the bars and doesn't accurately reflect the full value", because bars encode value as length.
>
> A line chart is read by slope (change in position), so moving the baseline rescales the trend without falsifying a length ratio; the guide allows truncation when small fluctuations matter. Fix: start at 0, switch to a line chart, or plot % change, and state "+6%" in the title.

**3.** Why size bubbles by area? Compute the distortion when a value doubles.

> [!example]- Solution
> Readers judge a circle by its area, $A=\pi r^2$. If the diameter is proportional to the value, doubling the value doubles $r$ and multiplies the area by 4: a doubled value looks 4× larger. For area ∝ value, $r_2=r_1\sqrt2\approx1.414\,r_1$; radius scales with $\sqrt{\text{value}}$. A 10× difference sized by diameter looks 100×.
> ```python
> plt.scatter(x, y, s=values * 10)          # s is area in points²: correct
> plt.scatter(x, y, s=(values * 10) ** 2)   # wrong: squares the encoding
> ```
> The same perceptual fact explains the case against pies and 3D (perceived volume grows with the cube).

**4.** Critique and rewrite: "a 3D pie chart of 9 product categories' revenue share, each slice a different bright colour, with drop shadows and bold italic labels."

> [!example]- Solution
> | Problem | Rule |
> |---|---|
> | 3D | no 3D (#7); front slices look bigger |
> | 9 categories in a pie | max 5 |
> | 9 bright colours | max 6 (#9); risk of red/green (#6) |
> | drop shadows | chart junk (#8) |
> | bold italic | distracting fonts (#10) |
> | pie at all | angles read poorly |
>
> Rewrite: a flat horizontal bar chart of the top 5 categories, the other 4 grouped as "Other" (after checking none matters on its own), sorted descending, one colour with an accent on the category discussed, zero baseline, plain horizontal labels, value labels at the bar ends, and a callout stating the insight.

**5.** (Advanced) Revenue grew 8%, but churn rose from 5% to 9%, and the growth came entirely from a price increase while customer numbers fell. Design a sequence of charts for executives. Why not one chart?

> [!example]- Solution
> There are several relationships (two opposing time series, a price/volume decomposition, an implication), and the message is the tension between them. One chart would become a dual-axis chart, where the choice of scales can create any apparent relationship.
>
> 1. "Revenue is up 8%": line chart of quarterly revenue, zero baseline.
> 2. "But we serve fewer customers": separate line chart, same time axis.
> 3. "Growth is entirely price": waterfall or stacked bar splitting the revenue change into price (+) and volume (−).
> 4. "Churn is accelerating": churn 5% → 9% with a callout on the turning point.
>
> One colour throughout, with the accent on churn; titles that state the finding ("Churn has nearly doubled since Q1"). Each chart raises the question the next one answers.

## 📝 Summary

- Find the story first (trends, correlations, outliers), then choose the chart.
- Seven relationships: time-series, ranking, part-to-whole, deviation, distribution, correlation, nominal comparison.
- Bars: versatile, zero baseline, one colour, gap ≈ ½ bar width.
- Pies: ≤ 5 categories, never side by side; angles are read poorly.
- Lines: ≤ 4 lines, solid, labelled directly, data filling ~⅔ of the axis; zero baseline negotiable.
- Area: ≤ 4 categories, transparent, not for discrete data. Scatter: correlation, trend lines, size/colour for extra variables.
- Bubbles sized by area; heat maps with single-hue or analogous scales.
- Maximize data-ink: no 3D, no chart junk, ≤ 6 colours, no red/green.

## ⚠️ Important Notes

1. Bars start at zero; lines need not.
2. People read length and position accurately, angle and area poorly.
3. Sizing bubbles by diameter squares the encoding.
4. 3D distorts through perspective and volume.
5. Avoid red/green; use colour-blind-safe palettes (`tableau-colorblind10`) and don't rely on colour alone.
6. Avoid dual-axis charts (my addition); use aligned charts sharing an x-axis.
7. "Other" can hide the real story.
8. Area charts imply continuity; not for discrete data.
9. Use colour for meaning: one colour plus one accent.
10. Titles should state the finding.
11. Choose the order of categories deliberately.

> [!warning] Source notes and gaps
> - All example figures (made with Visage) are images; the rules are complete.
> - Page 3 asks for the ideal gap between bars; page 10 answers: half a bar width.
> - The guide cites Crooks, Lankow & Ritchie, *Infographics* (2012); Wong, *WSJ Guide to Information Graphics* (2010); Yau, *Visualize This* (2011).
> - It is a marketing guide, not the course text; Knaflic's *Storytelling with Data* covers audience, context and call to action in more depth.
> - Pages 24–25 are promotional.
> - Exercise 2 corrected (2026-10-09): the visual ratio is 4×, a 300% visual increase for a 6.1% real one; an earlier "factor of about 60" claim is removed.

**Previous:** [[10 - Visualization with Matplotlib and Seaborn]] · **Back to** [[00-Index]]
