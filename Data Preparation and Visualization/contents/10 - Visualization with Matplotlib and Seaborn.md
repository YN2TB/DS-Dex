---
subject: Data Preparation and Visualization
chapter: 10
tags: [ds, visualization, matplotlib, seaborn, eda]
source: "Introduction To Matplotlib and Seaborn (1).pptx — Dr. Nguyen Tuan Long, NEU"
---

# Visualization with Matplotlib and Seaborn

> [!note] Where this sits in the course
> Opens **Part 3 — Turning Analysis into Impact**. The course's framing from Lesson 0: *"An analysis is only valuable if others can understand it and act upon it."* This chapter covers the **tools**; [[11 - Chart Design and Data Storytelling]] covers the **design judgement** that decides whether the chart actually communicates.

> [!warning] Source quality
> This deck is a **PowerPoint whose code samples and every output figure are images**. Only slide titles, captions, and a handful of code blocks survive text extraction. The structure below is faithful to the lecturer's sequence, but much of the code is reconstructed from the standard Matplotlib/Seaborn API (the deck follows VanderPlas, *Python Data Science Handbook* Ch. 4, one of the four course texts). **Reconstructed material is marked.** Verify against the original slides where it matters.

## 📘 Main Knowledge

### Why visualise at all

The deck opens with the `tips` dataset:

```python
tips = sns.load_dataset('tips')
tips.head()
```

The argument (developed properly in [[11 - Chart Design and Data Storytelling]]) is that summary statistics conceal structure a chart reveals instantly — the classic demonstration being Anscombe's quartet, four datasets with identical means, variances, and correlations but wildly different shapes.

---

## 1. Matplotlib

> Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python. **Matplotlib makes easy things easy and hard things possible.**

### Setting styles

```python
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
```

Available styles (from the slide):

`Solarize_Light2`, `_classic_test_patch`, `bmh`, `classic`, `dark_background`, `fast`, `fivethirtyeight`, `ggplot`, `grayscale`, `seaborn`, `seaborn-bright`, `seaborn-colorblind`, `seaborn-dark`, `seaborn-dark-palette`, `seaborn-darkgrid`, `seaborn-deep`, `seaborn-muted`, `seaborn-notebook`, `seaborn-paper`, `seaborn-pastel`, `seaborn-poster`, `seaborn-talk`, `seaborn-ticks`, `seaborn-white`, `seaborn-whitegrid`, `tableau-colorblind10`

> [!note] Version caveat
> In Matplotlib ≥ 3.6 the `seaborn-*` style names are **deprecated** and renamed with a `v0_8` prefix — `'seaborn-v0_8-whitegrid'`. The bare names in the slide list raise on current versions. Check with `plt.style.available`.

### Two interfaces — the most important concept in Matplotlib

Matplotlib has two ways to do everything, and confusing them is the source of most beginner frustration.

**MATLAB-style (state-based).** `plt.*` functions act on whatever figure is "current":

```python
plt.figure()
plt.plot(x, y)
plt.title('Title')
plt.xlabel('x')
```

Convenient for quick throwaway plots. It becomes unmanageable the moment you have more than one subplot, because "current" is implicit and easy to lose track of.

**Object-oriented (OO).** You hold explicit `Figure` and `Axes` objects and call methods on them:

```python
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title('Title')
ax.set_xlabel('x')
```

**Use the OO interface.** The slides say so directly — *"OO Style: Working directly with Figure and Axes objects."* It is explicit, it scales to complex layouts, and it is what every serious codebase uses.

The naming difference to memorise: `plt.title()` → `ax.set_title()`, `plt.xlabel()` → `ax.set_xlabel()`, `plt.xlim()` → `ax.set_xlim()`. The OO versions take a `set_` prefix.

### Parts of a figure

*(Slides 7–8 are diagrams — the anatomy below is reconstructed from the standard Matplotlib figure anatomy the slides depict.)*

| Component | What it is |
|---|---|
| **Figure** | The whole canvas. Contains all Axes. |
| **Axes** | One individual plot — the thing you usually mean by "a chart". A Figure can hold many. **Not** the plural of "axis". |
| **Axis** | A single number line (x or y), managing limits and ticks |
| **Artist** | Everything drawn on the figure — lines, text, patches |
| **Ticks / Tick labels** | Position markers and their text |
| **Spines** | The four border lines of the Axes box |

The **Figure vs Axes vs Axis** distinction is exam-relevant and genuinely confusing: `fig, ax = plt.subplots()` returns one Figure and one Axes; `ax.xaxis` is an Axis.

### Multiple subplots

Four approaches, in ascending order of control.

**`plt.subplots` — the whole grid in one go** *(code from the slide)*:

```python
fig, axes = plt.subplots(nrows=2, ncols=3,
                         figsize=(6, 4),
                         sharex=True, sharey=True)
for i in range(2):
    for j in range(3):
        axes[i, j].text(0.4, 0.4, str((i, j)))
```

`axes` is a 2-D NumPy array indexed `[row, col]`. `sharex`/`sharey` link the scales so subplots are directly comparable — and remove duplicate tick labels.

**`plt.subplot_mosaic` — layouts described by name** *(code from the slide)*:

```python
fig, axs = plt.subplot_mosaic([
    ['left',   'right'],
    ['bottom', 'right']
])
```

Repeating a label makes that Axes **span** those cells — `'right'` occupies the whole right column. Access by name: `axs['left']`. Far more readable than index arithmetic.

**`fig.add_gridspec` — detailed, flexible control** *(code from the slide)*:

```python
fig = plt.figure(figsize=(8, 6))
gs = fig.add_gridspec(3, 3)
ax1 = fig.add_subplot(gs[0, :])     # entire first row
ax2 = fig.add_subplot(gs[1, :-1])   # second row, all but last column
```

Slicing syntax defines each Axes' extent across the grid.

**`plt.axes` — by hand.** The most basic method: `plt.axes([left, bottom, width, height])` in figure coordinates (0–1). Total freedom, no convenience.

**The lecturer's comparison (slide 16):**

| Method | Character |
|---|---|
| `plt.subplots` | Simple, easy for basic layouts |
| `plt.subplot_mosaic` | Flexible with labels, suited to complex layouts |
| `plt.add_gridspec` | Detailed control and high customisation |

---

## 2. Seaborn

> Seaborn is based on matplotlib and provides a **high-level interface for drawing attractive statistical graphics.**

```python
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from warnings import filterwarnings
```

**The four basic steps** (from the slide):

1. Prepare some data
2. Control figure aesthetics
3. Plot with Seaborn
4. Further customise your plot

Step 4 matters: Seaborn *returns Matplotlib objects*, so anything Seaborn cannot express, you finish by hand with the OO interface. The two libraries are complementary, not alternatives.

**Seaborn versus Matplotlib** — the practical division: Seaborn is **statistically aware and DataFrame-native**. One call does the grouping, aggregation, error bars, and colouring that would take a dozen Matplotlib lines. Matplotlib gives total control over every pixel. Use Seaborn to draw, Matplotlib to adjust.

### The plot families covered

**Distributions** — `histplot`, `kdeplot`:

```python
sns.kdeplot(pokemon_df.Attack)
```

A KDE is a smoothed histogram — it estimates the underlying density rather than binning counts, so it does not depend on an arbitrary bin width. See [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]].

**Joint plots** — `jointplot`. Two variables' relationship in the centre, each variable's marginal distribution on the axes. Bivariate and univariate structure in one figure.

**Pair plots** — `pairplot`. *(Slide 21, quoting the deck):*

> When you generalize joint plots to datasets of larger dimensions, you end up with pair plots. This is very useful for **exploring correlations between multidimensional data**, when you'd like to plot all pairs of values against each other.

```python
sns.pairplot(iris, hue='species')
```

A scatter matrix of every variable against every other, with distributions on the diagonal. The standard first move in EDA — but it grows as $O(n^2)$, so it is unusable past ~10 columns.

**Facet plots** — `FacetGrid`. *(Slide 23, quoting the deck):*

> Sometimes the best way to view data is via histograms of subsets. Seaborn's FacetGrid makes this extremely simple.

Faceting draws the *same* plot for each subset of the data on a grid of panels — "small multiples". It is the visual equivalent of `groupby` ([[03 - Data Aggregation and Group Operations]]), and it is the right answer whenever you are tempted to cram many categories into one overloaded chart.

**Factor and bar plots** — `catplot` (formerly `factorplot`) and `barplot`. Seaborn's `barplot` shows the **mean** of a numeric variable per category, with a bootstrapped confidence interval — an aggregation and an uncertainty estimate for free.

**Heatmaps** — `heatmap`. Colour intensity encodes magnitude across a 2-D grid; the standard use is a correlation matrix:

```python
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
```

Design rules for heatmaps are in [[11 - Chart Design and Data Storytelling]].

## ✏️ Exercises

**1.** Rewrite this MATLAB-style code in the object-oriented style, and explain why the OO version is preferred.
> ```python
> plt.figure(figsize=(8, 4))
> plt.plot(x, y)
> plt.title('Sales')
> plt.xlabel('Month')
> plt.ylim(0, 100)
> ```

> [!example]- Solution
> ```python
> fig, ax = plt.subplots(figsize=(8, 4))
> ax.plot(x, y)
> ax.set_title('Sales')
> ax.set_xlabel('Month')
> ax.set_ylim(0, 100)
> ```
> Note the `set_` prefix on the OO methods — `plt.title` → `ax.set_title`, `plt.ylim` → `ax.set_ylim`. `plt.plot` → `ax.plot` keeps its name.
>
> **Why OO is preferred:** `plt.*` acts on the "current" figure, an implicit global. With one plot this is harmless. With several, any function call that creates a figure silently steals "current" status, and your `plt.title()` lands on the wrong chart — with no error. The OO version names its target explicitly, so it cannot be misdirected.
>
> It also composes: `ax` can be passed into a function, stored in a list, or handed to Seaborn (`sns.histplot(data, ax=axes[0,1])`). None of that is expressible with the state machine.

**2.** Explain the difference between **Figure**, **Axes**, and **Axis**. What does `fig, axes = plt.subplots(2, 3)` return, and how do you access the middle-bottom plot?

> [!example]- Solution
> - **Figure** — the whole canvas, the window or image file. Holds everything.
> - **Axes** — one individual plot (what people casually call "a chart"). A Figure can contain many. **Despite the "s", it is singular** — one Axes is one plot.
> - **Axis** — a single number line (x or y) belonging to an Axes, managing its limits, ticks, and scale. `ax.xaxis` is an Axis object.
>
> The naming is genuinely poor: *Axes* is not the plural of *Axis*. A 2-D Axes contains exactly two Axis objects.
>
> `plt.subplots(2, 3)` returns a tuple: one **Figure**, and a **2×3 NumPy array of Axes**. The middle-bottom plot is row 1, column 1:
> ```python
> axes[1, 1].plot(x, y)
> ```
> Edge case worth knowing: with `nrows=1` or `ncols=1`, the array is **1-D**, so it is `axes[2]` not `axes[0, 2]`. With `plt.subplots()` (no arguments) you get a bare Axes object, not an array at all — indexing it raises. Pass `squeeze=False` to force a 2-D array every time and avoid writing three different access patterns.

**3.** Using `subplot_mosaic`, build the layout the deck's Titanic practice asks for: a bar plot of survival rate by class across the top row, a box plot of age by class taking two-thirds of the second row, and a small histogram of age at the bottom right.

> [!example]- Solution
> ```python
> import seaborn as sns
> import matplotlib.pyplot as plt
>
> titanic = sns.load_dataset('titanic')
>
> fig, axs = plt.subplot_mosaic(
>     [['bar', 'bar', 'bar'],
>      ['box', 'box', 'hist']],
>     figsize=(10, 6), layout='constrained')
>
> sns.barplot(data=titanic, x='class', y='survived', ax=axs['bar'])
> axs['bar'].set_title('Survival rate by class')
>
> sns.boxplot(data=titanic, x='class', y='age', ax=axs['box'])
> axs['box'].set_title('Age distribution by class')
>
> sns.histplot(data=titanic, x='age', bins=20, ax=axs['hist'])
> axs['hist'].set_title('Age')
> ```
> The mosaic list *is* the layout, read literally as a picture: `'bar'` repeated across the top row spans all three columns; `'box'` spans two cells of the bottom row; `'hist'` takes the last. Repeating a label is what creates the span.
>
> Two things worth noting. Because `survived` is coded 0/1, `sns.barplot` plotting its **mean** gives the survival *rate* directly, with bootstrapped confidence intervals thrown in — the same 0/1-mean idiom from [[03 - Data Aggregation and Group Operations]].
>
> And `ax=axs['bar']` is how Seaborn and Matplotlib interoperate: Seaborn draws *into* an Axes you control, so you can adjust it afterwards with the OO API. That is step 4 of the deck's four-step Seaborn workflow.
>
> The equivalent with `add_gridspec` is uglier and harder to read — which is exactly the trade-off slide 16 describes:
> ```python
> gs = fig.add_gridspec(2, 3)
> ax_bar  = fig.add_subplot(gs[0, :])
> ax_box  = fig.add_subplot(gs[1, :-1])
> ax_hist = fig.add_subplot(gs[1, -1])
> ```

**4.** When would you use a `pairplot` versus a `heatmap` of the correlation matrix? Give a case where the heatmap misleads and the pairplot does not.

> [!example]- Solution
> **`heatmap(df.corr())`** — compact, scales to dozens of variables, gives one number per pair. **`pairplot`** — shows the actual joint distribution, but grows as $O(n^2)$ panels and is unreadable past ~10 columns.
>
> ```python
> sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0, vmin=-1, vmax=1)
> sns.pairplot(iris, hue='species')
> ```
>
> **Where the heatmap misleads:** Pearson's $r$ measures **linear** association only. For $y = x^2$ over a symmetric range like $[-3, 3]$, the correlation is approximately **zero** — the heatmap shows a blank, uninteresting cell — while the pairplot shows an unmistakable parabola. A perfect deterministic relationship, invisible to the summary statistic.
>
> Same failure for any non-monotonic relationship, and for **Simpson's paradox**: two subgroups each showing a positive trend can produce a negative pooled correlation. The heatmap reports the misleading pooled number; `pairplot(hue='group')` shows the truth immediately.
>
> Anscombe's quartet is the canonical demonstration — four datasets with identical means, variances, and correlation (0.816), that look completely different. `sns.load_dataset('anscombe')` is built into Seaborn.
>
> **Practical workflow:** heatmap first to find candidate pairs among many columns, then pairplot (or a targeted `jointplot`) on the interesting subset to check the relationship is what the number implies. Never trust $r$ without looking at the scatter.

**5.** (Advanced) Explain what faceting is, why it is preferable to encoding many categories with colour in a single Axes, and rebuild an overloaded chart using `FacetGrid`.

> [!example]- Solution
> **Faceting** draws the *same* plot repeatedly, once per subset of the data, on a grid of small panels — "small multiples". It is `groupby` for charts.
>
> **The overloaded version:**
> ```python
> sns.scatterplot(data=tips, x='total_bill', y='tip', hue='day',
>                 style='time', size='size')   # 3 encodings on one Axes
> ```
> Every point competes with every other. Overlapping marks hide each other, the reader must consult a legend for three separate visual channels simultaneously, and comparing "Thursday lunch" against "Saturday dinner" means visually filtering a cloud of points by two attributes at once — which people simply cannot do accurately.
>
> **The faceted version:**
> ```python
> g = sns.FacetGrid(tips, col='day', row='time', height=3, margin_titles=True)
> g.map_dataframe(sns.scatterplot, x='total_bill', y='tip')
> g.set_axis_labels('Total bill', 'Tip')
> ```
> or the figure-level shortcut:
> ```python
> sns.relplot(data=tips, x='total_bill', y='tip', col='day', row='time')
> ```
>
> **Why it is better:** each panel is simple, and — crucially — **all panels share axis scales by default**, so comparison becomes a matter of judging *position*, which human perception does extremely well. Comparing by colour or shape is far less accurate. This is the perceptual argument behind [[11 - Chart Design and Data Storytelling]]'s rules limiting charts to 4–5 categories: those limits exist because faceting is the correct escape hatch, not because you should simply drop data.
>
> Shared scales are load-bearing. If each panel auto-scaled independently, a small panel could look identical to a large one — visually implying equality where a tenfold difference exists. Only override with `sharey=False` when the panels genuinely measure different quantities.
>
> Faceting's limit is data volume: 30 categories gives 30 panels, each too small to read. Then aggregate first, or facet on the few categories that matter and pool the rest.

## 📝 Summary

- **Matplotlib has two interfaces.** Prefer the **object-oriented** one (`fig, ax = plt.subplots()`); `plt.*` acts on an implicit "current" figure and breaks down with multiple subplots.
- **OO methods take a `set_` prefix:** `ax.set_title()`, `ax.set_xlabel()`, `ax.set_ylim()`.
- **Figure = canvas, Axes = one plot, Axis = one number line.** *Axes* is not the plural of *Axis*.
- **Four layout tools:** `plt.subplots` (simple grids), `subplot_mosaic` (named, spanning, readable), `add_gridspec` (fine control), `plt.axes` (manual).
- **Repeating a label in `subplot_mosaic` makes an Axes span those cells.**
- **`sharex`/`sharey` make subplots comparable** and remove redundant tick labels.
- **Seaborn is statistically aware and DataFrame-native**; it returns Matplotlib objects, so finish customisation with the OO API.
- **Seaborn's four steps:** prepare data → control aesthetics → plot → customise.
- **`pairplot` for exploring all pairwise relationships; `heatmap` for a compact correlation matrix** — but $r$ sees only linear relationships.
- **Facet instead of overloading.** Small multiples with shared scales beat three encodings crammed onto one Axes.

## ⚠️ Important Notes

**`seaborn-*` style names are deprecated in Matplotlib ≥ 3.6.** The slide's list will raise; use `'seaborn-v0_8-whitegrid'`, or check `plt.style.available`.

**Never mix the two interfaces in one figure.** Calling `plt.title()` after building Axes objects applies it to whichever figure is "current" — often not the one you meant, and it fails silently.

**`plt.subplots()` return shape varies.** `(2,3)` → 2-D array; `(1,3)` → **1-D** array; `()` → a bare Axes. Code written for one shape breaks on another. `squeeze=False` forces 2-D consistently.

**Seaborn's `barplot` shows means with confidence intervals, not raw values.** People routinely misread it as a total. Use `estimator=sum` for totals, or `errorbar=None` to drop the CI.

**`pairplot` is $O(n^2)$.** Twenty columns produces 400 panels and will hang your notebook. Subset the columns first.

**Correlation heatmaps only capture linear association.** $y = x^2$ gives $r \approx 0$. Always inspect the scatter before trusting the coefficient — and beware Simpson's paradox, where pooled correlation reverses the sign present within every subgroup.

**Diverging colormaps need `center=0`.** Without it, `cmap='coolwarm'` on a correlation matrix puts the colour midpoint at the data mean rather than at zero, so the visual "neutral" is not actually zero correlation. Set `center=0, vmin=-1, vmax=1`.

**KDE plots invent smoothness.** They can imply density in gaps where no data exists, and can show mass below zero for a strictly non-negative variable. Show the histogram alongside, or use `cut=0`.

**Use `layout='constrained'` (or `fig.tight_layout()`)** or subplot labels will overlap in multi-panel figures.

**Facets must share scales to be comparable.** Independent auto-scaling makes different magnitudes look identical. Only unshare when panels measure genuinely different quantities.

> [!warning] Gaps in the source deck
> The `.pptx` is **image-heavy**; the following slides have titles but no extractable content:
> - **Slide 3** — the "why visualisation is needed" example (only the `tips` load survives)
> - **Slides 7–8** — "Parts of a Figure" anatomy diagrams. My table is **reconstructed** from the standard Matplotlib anatomy.
> - **Slide 9** — "Practice: California Cities" — task description not recoverable
> - **Slide 12** — a subplots example
> - **Slide 15** — `plt.axes` "Subplots by Hand" example
> - **Slides 19–26** — the Seaborn half is almost entirely images. Only the `sns.kdeplot(pokemon_df.Attack)` line, the pair-plot paragraph (slide 21), and the FacetGrid paragraph (slide 23) survive as text. **Joint plots (20), Iris practice (22), Factor/Bar plots (24), Heatmap (25), and the correlation practice (26) have no recoverable content** — all Seaborn code in this note beyond `kdeplot` is reconstructed from the standard API.
>
> Datasets referenced: `tips`, `pokemon_df` (not in `documents/` — likely a Kaggle Pokémon stats CSV), `iris`, `titanic`. All except `pokemon_df` load via `sns.load_dataset()`.
>
> The deck follows VanderPlas, *Python Data Science Handbook* Ch. 4 — consult it for the missing figures.

---
**Previous:** [[09 - Building Pipelines]] · **Next:** [[11 - Chart Design and Data Storytelling]]
