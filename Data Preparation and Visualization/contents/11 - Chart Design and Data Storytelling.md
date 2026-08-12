---
subject: Data Preparation and Visualization
chapter: 11
tags: [ds, visualization, design, storytelling, communication]
source: "Hubspot_Data_Visualization_101_How_to_Design_Charts_and_Graphs.pdf (HubSpot × Visage)"
---

# Chart Design and Data Storytelling

> [!note] Where this sits in the course
> Closes **Part 3** and the course. [[10 - Visualization with Matplotlib and Seaborn]] covered *how to draw*; this chapter covers *what to draw and why*. Lesson 0's framing: **"An analysis is only valuable if others can understand it and act upon it."**
>
> Unlike the other chapters, this source is not a lecture deck but an industry design guide (HubSpot × Visage), aligned with Cole Nussbaumer Knaflic's *Storytelling with Data* — the fourth course text.

## 📘 Main Knowledge

> If your data is misrepresented or presented ineffectively, key insights and understanding are lost, **which hurts both your message and your reputation.**

### 1. Finding the story in your data

Before choosing a chart, identify **the relationship you want to show**. Three starting places when hunting for a story:

| Pattern | Example |
|---|---|
| **Trends** | Ice cream sales over time |
| **Correlations** | Ice cream sales vs. temperature |
| **Outliers** | Ice cream sales in an unusual region |

The order is deliberate: **story first, chart second.** Choosing a chart type before knowing your message is the root cause of most bad visualisations.

### 2. Know your data

**Data types:**

| Type | Definition | Example |
|---|---|---|
| **Categorical** | Sortable by group or category | Types of products sold |
| **Quantitative** | Countable or measurable; all values numerical | — |
| **Discrete** | Numerical with a *finite* number of possible values | Number of employees in the office |
| **Continuous** | Measured, with a value within a range | Rainfall in a year |

These map directly onto the encoder choices in [[07 - Data Transformation]] and the statistical test matrix in [[08 - Feature Selection]] — the same distinction drives all three.

**Data relationships** — the seven the guide names:

| Relationship | What it shows | Example |
|---|---|---|
| **Time-series** | Changes in a consistent metric over time | Monthly sales |
| **Ranking** | How values compare in relative magnitude | Months ranked hottest to coldest |
| **Part-to-whole** | A subset compared to the larger whole | % of customers buying specific products |
| **Deviation** | How far a data point differs from the mean | Park tickets on a rainy vs. normal day |
| **Distribution** | How data spreads, often around a central value | Heights of basketball players |
| **Correlation** | Two+ variables moving together, positively or negatively | Salary by education level |
| **Nominal comparison** | Simple comparison of subcategory values | Visitors to various websites |

**Identify the relationship, then pick the chart that expresses it.** This table is the most exam-likely content in the chapter.

---

### 3. Guide to chart types

#### Bar chart

Best for **change over time, comparing categories, or comparing parts of a whole.** The most versatile chart type.

**Variations:**

- **Vertical (column)** — chronological data (*time-series should always run left to right*), or when showing negative values below the x-axis.
- **Horizontal** — when category labels are long.
- **Stacked** — comparing multiple part-to-whole relationships. Works with discrete or continuous data, either orientation.
- **100% stacked** — when the *total* of each category is unimportant and the **percentage distribution** of subcategories is the message.

**Design best practices:**

- **Start the y-axis at 0.** Starting above zero truncates the bars and misrepresents values.
- **Use horizontal labels** — steep diagonal or vertical text is hard to read.
- **Order data appropriately** — alphabetically, sequentially, or by value.
- **Space bars appropriately** — the gap should be **½ a bar's width**.
- **Use consistent colours** — one colour for the whole chart, with an accent colour only to highlight a significant point.

#### Pie chart

Best for **part-to-whole comparisons**, with a **small** dataset.

> [!warning] The case against the pie chart
> The guide includes an unusual, honest caveat. Critics such as **Stephen Few** argue we can only judge slice sizes reliably at familiar percentages (25%, 50%, 75%, 100%) and positions, because those are common angles. **We interpret other angles inconsistently**, making relative sizes hard to compare — and the chart therefore less effective.
>
> The underlying perceptual fact: humans compare **lengths and positions** far more accurately than **angles and areas**. A bar chart uses the accurate channel; a pie chart uses the inaccurate one. When in doubt, use a bar chart.

**Design best practices:**

- **Visualise no more than 5 categories.** Group small values into "other" — but make sure that does not hide something significant.
- **Don't use multiple pie charts for comparison.** Slice sizes are very hard to compare side by side — **use a stacked bar chart instead.**
- **Order slices correctly**, one of two ways:
  - *Option 1* — largest section at 12 o'clock going clockwise; second largest at 12 o'clock going counterclockwise; remainder continue counterclockwise.
  - *Option 2* — largest at 12 o'clock, then all remaining in descending order clockwise.
- **Make sure values total 100%** and slices are proportionate.

#### Line chart

For **time-series relationships with continuous data.** Shows trend, acceleration, deceleration, and volatility.

**Design best practices:**

- **Don't plot more than 4 lines.** Break into separate charts to compare more.
- **Use solid lines only** — dashes and dots distract.
- **Use the right height** — data should occupy about **two-thirds of the y-axis scale**.
- **Include a zero baseline if possible.** A line chart need not start at zero, but should where feasible. **Exception:** when small fluctuations are meaningful (stock market data), truncating the scale to show variance is legitimate.
- **Label lines directly** rather than forcing readers to consult a legend.

> [!note] Bar vs. line and the zero baseline
> The rules differ, and the reason is *how each chart encodes value*. A bar encodes value as **length from the axis**, so truncating the axis literally lies about the ratio between bars. A line encodes value as **position**, and the reader interprets the *slope*, so a truncated axis is defensible when resolution matters. **Bars: zero baseline always. Lines: usually, but negotiable.**

#### Area chart

Depicts time-series like a line chart, but **can represent volume**.

- **Standard** — comparing a quantitative progression over time.
- **Stacked area** — part-to-whole relationships, showing each category's contribution to a cumulative total.
- **100% stacked area** — distribution of categories as part of a whole, where the cumulative total is unimportant.

**Design best practices:**

- **Don't display more than 4 data categories** — more becomes cluttered.
- **Make it easy to read** — in stacked area charts, put highly variable categories at the **top** and low-variability ones at the **bottom**.
- **Start the y-axis at 0.**
- **Use transparent colours** so background data is not obscured.
- **Don't use area charts for discrete data** — the connected line implies intermediate values that only exist for continuous data.

#### Scatter plot

Shows the relationship between two sets of variables. Best for **correlation in a large amount of data.**

**Design best practices:**

- **Start the y-axis at 0.**
- **Use trend lines** to draw out the correlation.
- **Don't compare more than 2 trend lines.**
- **Include more variables** — encode additional dimensions with dot **size** and **colour**.

#### Bubble chart

For **nominal comparison or ranking relationships.**

- **Bubble plot** — a scatter plot with sized bubbles, adding one more variable.
- **Bubble map** — values for specific geographic regions.

**Design best practices:**

- **Size bubbles by area, not diameter.** *(This is the critical one — see Exercise 3.)*
- **Make sure labels are visible** and unobstructed.
- **Don't use odd shapes** — non-circular shapes lead to inaccurate readings.

#### Heat map

Displays categorical data using **colour intensity** to represent values, across geographic areas or data tables.

**Design best practices:**

- **Use a simple map outline** — lines frame the data, they should not distract.
- **Select colours appropriately.** Some colours stand out more than others, giving unnecessary weight to that data. Use **a single colour with varying shades**, or a spectrum between two **analogous** colours. Code intensity intuitively — darker should mean more.
- **Use patterns sparingly** — one pattern overlay for a second variable is acceptable; multiple are overwhelming.
- **Choose appropriate data ranges** — 3–5 numerical ranges giving fairly even distribution, using +/− signs to extend the extremes.

---

### 4. The 10 data design do's and don'ts

**DO:**

1. Use **one colour** to represent each category.
2. Order data sets using a **logical hierarchy**.
3. Use **callouts** to highlight important or interesting information.
4. Visualise data so it is **easy for readers to compare values**.
5. Use **icons** to enhance comprehension and reduce unnecessary labelling.

**DON'T:**

6. Use **high-contrast colour combinations** such as red/green or blue/yellow.
7. Use **3D charts** — they skew perception of the visualisation.
8. Add **chart junk** — unnecessary illustrations, drop shadows, or ornamentation distract from the data.
9. Use **more than 6 colours** in a single layout.
10. Use **distracting fonts or elements** (bold, italic, underlined text).

> [!tip] The unifying principle
> Nearly every rule above is one idea: **maximise the proportion of ink that carries information.** Tufte called it the *data-ink ratio*. 3D effects, drop shadows, ornamental fills, and rainbow palettes all add ink without adding meaning — and actively distort perception. Rule 6 has a second reason beyond aesthetics: **red/green is the most common form of colour blindness**, affecting roughly 8% of men.

## ✏️ Exercises

**1.** For each message, name the data relationship and the appropriate chart: (a) "Our top 3 products by revenue"; (b) "Marketing spend drives signups"; (c) "Mobile grew from 20% to 60% of traffic over five years"; (d) "Most support tickets are resolved in 2–4 hours."

> [!example]- Solution
> **(a) Ranking → horizontal bar chart.** Sorted by value, descending. Horizontal because product names are usually long labels — one of the guide's explicit criteria. Not a pie chart: "top 3" is a comparison of magnitudes, not parts of a whole.
>
> **(b) Correlation → scatter plot with a trend line.** Spend on x, signups on y. Note the guide's caution that a trend line *draws out* correlation — it does not establish causation, despite the word "drives" in the framing. See [[01 - Getting Started with Pandas]].
>
> **(c) Part-to-whole over time → 100% stacked area chart** (or 100% stacked bar for a few discrete years). The message is explicitly about *percentage distribution* while the absolute total is not the point — which is exactly the guide's definition of the 100% stacked variant.
>
> **(d) Distribution → histogram.** The message is about the *shape* of resolution times. A bar chart of category averages would destroy it: an average of 3 hours is consistent with everything resolving at 3 hours, or half at 1 hour and half at 5 — completely different operational realities.
>
> The lesson: **each message names a relationship, and the relationship names the chart.** Choosing a chart first inverts the process and produces charts that don't say anything.

**2.** A colleague presents a bar chart of quarterly revenue with the y-axis starting at $4.8M, making Q4's $5.2M bar look roughly three times Q1's $4.9M. Explain what is wrong, and why the same criticism is weaker for a line chart.

> [!example]- Solution
> **A truncated y-axis on a bar chart is a misrepresentation**, and the guide states it flatly: *"Starting at a value above zero truncates the bars and doesn't accurately reflect the full value."*
>
> The reason is that a bar **encodes value as length from the axis**. The reader's eye compares lengths, so bar-length ratio *is* the perceived value ratio. Truncating at $4.8M leaves visible lengths of 0.1 and 0.4 — a **4× visual ratio** representing a real difference of about **6%**. The chart is off by a factor of roughly 60.
>
> **Why a line chart survives the same criticism:** a line encodes value as **position**, and the reader interprets the **slope** — the *change*. No length is being compared against the axis, so moving the baseline rescales the trend without falsifying a ratio. The guide reflects this asymmetry precisely: bars say *"start the y-axis at 0"* unconditionally, while lines say *"include a zero baseline if possible"* and explicitly permit truncation *"if relatively small fluctuations in data are meaningful (e.g., in stock market data)."*
>
> **The fix:** either start at zero and accept the change looks small (because it *is* small), or switch to a line chart with a labelled axis, or plot % change directly. If a 6% rise is genuinely the story, say "6%" in the title — the honest way to make a small number feel important is words, not axis manipulation.

**3.** The guide insists bubbles be sized "by **area**, not diameter". Show mathematically why this matters, and calculate the distortion for a value that doubles.

> [!example]- Solution
> The reader perceives a circle's magnitude by its **area**, and for a circle
>
> $$A = \pi r^2$$
>
> so area grows with the **square** of the radius. Sizing by diameter therefore squares the encoded value.
>
> **Worked example — value doubles from 100 to 200:**
>
> *Wrong (diameter ∝ value):* $d_2 = 2 d_1$, so $r_2 = 2r_1$ and
> $$\frac{A_2}{A_1} = \frac{\pi (2r_1)^2}{\pi r_1^2} = 4$$
> The bubble **looks 4× bigger** for a value that only doubled — a **100% overstatement**.
>
> *Correct (area ∝ value):* we need $A_2 = 2A_1$, so
> $$r_2 = r_1\sqrt{2} \approx 1.414\, r_1$$
>
> The general rule: **radius must scale with the square root of the value.**
>
> ```python
> import numpy as np
> # Matplotlib's `s` parameter is area in points², so this is already correct:
> plt.scatter(x, y, s=values * 10)
> # WRONG — this squares the encoding:
> plt.scatter(x, y, s=(values * 10) ** 2)
> ```
> The distortion compounds badly at range: a 10× value difference sized by diameter appears **100×**, which is why bubble charts are so often accused of lying. Matplotlib's `scatter(s=...)` takes **area**, so passing values directly is right; Seaborn's `size=` handles the scaling internally.
>
> This is the same perceptual principle behind the case against pie charts — humans read **length and position** accurately, **area and angle** poorly. It is also why the guide bans 3D charts (rule 7): adding a third dimension makes perceived *volume* scale with the **cube**, distorting even more severely.

**4.** Critique this chart specification against the guide's rules, and rewrite it: *"A 3D pie chart showing our 9 product categories' share of revenue, with each slice a different bright colour, drop shadows, and the category names in bold italic."*

> [!example]- Solution
> It violates **six** rules simultaneously.
>
> | Violation | Rule |
> |---|---|
> | **3D** | Don't use 3D charts — they skew perception (#7). Perspective makes front slices look larger than identical back slices. |
> | **9 categories in a pie** | Max 5 per pie chart. Beyond that slices become indistinguishable. |
> | **9 bright colours** | Don't use more than 6 colours in a layout (#9); "bright" risks red/green adjacency (#6). |
> | **Drop shadows** | Chart junk (#8). |
> | **Bold italic labels** | Distracting fonts and elements (#10). |
> | **Pie chart at all** | Angle comparison is unreliable — Stephen Few's objection. |
>
> **Rewrite:**
>
> > A **horizontal bar chart**, flat (no 3D), of the **top 5 product categories** by revenue share, remaining 4 grouped as "Other" *(after confirming none individually matters)*. Bars sorted descending. **One single colour**, with a **single accent colour** on the category being discussed. Zero baseline. Horizontal category labels, plain regular weight. Value labels at the end of each bar so no legend or gridlines are needed. A **callout** on the accent bar stating the insight in words.
>
> Why the bar chart wins: it uses **length from a common baseline**, the most accurately perceived visual channel, so readers can genuinely rank and compare — the guide's do #4. It handles 5+ categories without degrading. And it leaves colour free to carry *meaning* (the highlight) rather than merely distinguishing categories.
>
> The one caveat on grouping into "Other": the guide explicitly warns to *"make sure it does not hide interesting or significant information."* If one of those four hidden categories is collapsing 40% year-on-year, that is the actual story and burying it in "Other" destroys it.

**5.** (Advanced) You must present to executives: revenue grew 8% but customer churn rose from 5% to 9%, and the growth came entirely from a price increase while customer count fell. Design a narrative sequence of charts, and explain why one chart cannot do this.

> [!example]- Solution
> **Why one chart fails:** this is not one relationship but **four** — a time-series (revenue), a second time-series moving oppositely (churn), a decomposition (price vs. volume), and an implication (future revenue). The guide's framework requires identifying *the* relationship a chart shows; here there are several, and the message is the **tension between them**. Cramming them together produces a dual-axis chart, which lets you manufacture any apparent relationship by choosing the two scales — the most criticised chart type in the field.
>
> **A four-chart sequence, each answering the question the previous one raises:**
>
> **1. "Revenue is up 8%" — line chart, quarterly revenue, zero baseline.** Open with the number they expect. Establish trust before complicating it.
>
> **2. "But we're serving fewer customers" — line chart, customer count, same time axis.** A separate chart, *not* a second axis. Same x-scale so the reader aligns them by position. The contrast between charts 1 and 2 is the pivot of the story.
>
> **3. "The growth is entirely price" — waterfall or stacked bar decomposing revenue change into price effect (+) and volume effect (−).** This answers "how can revenue rise while customers fall?" before it is asked.
>
> **4. "And churn is accelerating" — line chart, churn 5% → 9%, with a callout on the inflection point.** Direct labelling, no legend. This is the *action* chart, so it gets a callout (do #3).
>
> **Design decisions throughout:** one colour, with a single accent reserved for the churn line — colour spent on the thing that matters (do #1, #3). Consistent x-axis across all four so position comparisons hold. Titles that state the **finding**, not the contents — *"Churn has nearly doubled since Q1"* rather than *"Churn over time"*. That single habit is the highest-leverage idea in *Storytelling with Data*: the title is the sentence people remember, so it should carry the message rather than label the axes.
>
> **Sequence is the argument.** Each chart raises the question the next answers, so the audience reaches the conclusion themselves rather than being told. Lesson 0's phrasing: *"building a logical data narrative that guides the audience to a conclusion."*
>
> **What to avoid:** a dual-axis revenue-and-churn chart. With two independent scales you can make the lines appear to converge, diverge, or cross wherever you like — the relationship is an artefact of scale choice, not of data. Two aligned charts convey the same comparison honestly.

## 📝 Summary

- **Find the story first, then choose the chart.** Look for trends, correlations, and outliers.
- **Seven data relationships** — time-series, ranking, part-to-whole, deviation, distribution, correlation, nominal comparison — and each implies its chart.
- **Bar charts are the most versatile**; zero baseline always, one colour, bar spacing ½ a bar width, horizontal labels.
- **Pie charts: ≤5 categories, never side by side** (use stacked bars). Angles are read unreliably — Stephen Few's objection.
- **Line charts: ≤4 lines, solid only, label directly, data filling ~⅔ of the y-scale.** Zero baseline preferred but negotiable when small fluctuations matter.
- **Area charts add volume to time-series; ≤4 categories, transparent colours, never for discrete data.**
- **Scatter plots for correlation in large data**; add trend lines, encode extra variables with size and colour, ≤2 trend lines.
- **Bubbles must be sized by area, not diameter** — otherwise the encoding is squared.
- **Heat maps: single-hue or analogous spectrum, 3–5 ranges, intuitive intensity coding.**
- **The 10 rules reduce to one:** maximise the share of ink that carries information. No 3D, no chart junk, ≤6 colours, no red/green.

## ⚠️ Important Notes

**Bars must start at zero; lines need not.** A bar encodes *length*, so truncating falsifies the ratio. A line encodes *position* and is read as slope. This asymmetry is a favourite exam question.

**Humans compare length and position accurately, angle and area poorly.** This single perceptual fact explains the case against pie charts, the area-not-diameter bubble rule, the 3D ban, and why bar charts are the default recommendation.

**Sizing bubbles by diameter squares your data.** A doubled value appears 4× larger. Radius must scale with $\sqrt{\text{value}}$. Matplotlib's `scatter(s=...)` already takes area — passing squared values is the common bug.

**3D distorts twice over** — perspective enlarges nearer elements, and perceived volume scales with the cube of the encoded dimension.

**Red/green is the worst colour pairing** — roughly 8% of men have red-green colour deficiency. Use `tableau-colorblind10` or `seaborn-colorblind` ([[10 - Visualization with Matplotlib and Seaborn]]), and never rely on colour alone to carry meaning.

**Avoid dual-axis charts.** Two independent y-scales let you produce almost any apparent relationship between two series. Use two aligned charts sharing an x-axis instead. *(Not in the guide, but standard practice and directly relevant to Exercise 5.)*

**"Other" can hide the story.** The guide's own caveat: grouping small categories is fine only after checking none of them is individually significant.

**Never use an area chart for discrete data.** Connecting the points implies intermediate values that do not exist.

**Colour should encode meaning, not decoration.** One colour per chart with a single accent for the point being made. Colour spent distinguishing nine arbitrary categories is colour unavailable for emphasis.

**Titles should state the finding, not the contents.** "Churn has nearly doubled since Q1" beats "Churn over time". The title is the sentence people remember.

**Order is never arbitrary.** Alphabetical, sequential, or by value — but chosen deliberately. Unordered categories force the reader to do the sorting.

> [!warning] Source notes and gaps
> - Every chart and graph in the guide was **created with Visage**, and all example figures are images — so the specific examples illustrating each rule are not recoverable, only the rules themselves. The rule text above is complete and verbatim.
> - **Page 3** poses "What's the ideal distance between columns in a bar chart?" as a teaser; the answer appears on page 10 — **½ bar width**.
> - The guide's own cited sources: *Infographics: The Power of Visual Storytelling* (Crooks, Lankow & Ritchie, Wiley 2012); *The Wall Street Journal Guide to Information Graphics* (Dona Wong, Dow Jones 2010); *Visualize This* (Nathan Yau, Wiley 2011).
> - This is a **marketing-industry design guide, not an academic text.** It is practical and broadly consistent with the field, but it is not the course's assigned book. Lesson 0 lists **Knaflic, *Storytelling with Data*** as the Part 3 text — check it for the narrative-construction material (audience, context, call to action) that this guide only touches on.
> - Pages 24–25 are HubSpot/Visage promotional material.

---
**Previous:** [[10 - Visualization with Matplotlib and Seaborn]] · **Back to** [[00-Index]]
