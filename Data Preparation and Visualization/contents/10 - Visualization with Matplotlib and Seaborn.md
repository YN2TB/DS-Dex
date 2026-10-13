---
subject: Data Preparation and Visualization
chapter: 10
tags: [ds, visualization, matplotlib, seaborn, eda]
source: "Introduction To Matplotlib and Seaborn (1).pptx — Dr. Nguyen Tuan Long, NEU"
---

# Visualization with Matplotlib and Seaborn

Opens Part 3 (Turning Analysis into Impact). Lesson 0: "An analysis is only valuable if others can understand it and act upon it." This chapter covers the tools; [[11 - Chart Design and Data Storytelling]] covers design.

> [!warning] Source quality
> The deck's code samples and output figures are mostly images. Slide titles, captions and a few code blocks extract; the rest is reconstructed from the standard Matplotlib/Seaborn API (the deck follows VanderPlas, *Python Data Science Handbook*, ch. 4). Reconstructed parts are marked.

## 📘 Main Knowledge

### Why visualize

The deck opens with `tips = sns.load_dataset('tips')`. Summary statistics can hide structure that a chart shows immediately; Anscombe's quartet has four datasets with the same means, variances and correlation but very different shapes.

### 1. Matplotlib

"Matplotlib makes easy things easy and hard things possible."

```python
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
```

Styles listed on the slide include `bmh`, `classic`, `dark_background`, `fivethirtyeight`, `ggplot`, `grayscale`, `seaborn-*` variants and `tableau-colorblind10`. In Matplotlib ≥ 3.6 the `seaborn-*` names are renamed `seaborn-v0_8-*` (e.g. `'seaborn-v0_8-whitegrid'`); check `plt.style.available`.

#### Two interfaces

**MATLAB-style (state-based)**: `plt.*` functions act on the "current" figure.
```python
plt.figure(); plt.plot(x, y); plt.title('Title'); plt.xlabel('x')
```
Fine for quick plots; confusing with several subplots.

**Object-oriented**: work with explicit `Figure` and `Axes` objects.
```python
fig, ax = plt.subplots()
ax.plot(x, y); ax.set_title('Title'); ax.set_xlabel('x')
```
The slides recommend this style. OO methods add `set_`: `plt.title` → `ax.set_title`, `plt.xlim` → `ax.set_xlim`.

#### Parts of a figure (reconstructed; slides 7–8 are diagrams)

| Component | Meaning |
|---|---|
| Figure | the whole canvas; holds all Axes |
| Axes | one plot (singular, not the plural of axis) |
| Axis | one number line (x or y) with limits and ticks; `ax.xaxis` |
| Artist | anything drawn: lines, text, patches |
| Ticks / tick labels | position markers and their text |
| Spines | the border lines of the Axes |

#### Multiple subplots

**`plt.subplots`** (from the slide):
```python
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(6, 4), sharex=True, sharey=True)
for i in range(2):
    for j in range(3):
        axes[i, j].text(0.4, 0.4, str((i, j)))
```
`axes` is a 2-D array indexed `[row, col]`; `sharex`/`sharey` give common scales and remove duplicate tick labels.

**`plt.subplot_mosaic`** (from the slide):
```python
fig, axs = plt.subplot_mosaic([['left', 'right'], ['bottom', 'right']])
```
Repeating a label makes that Axes span those cells; access by name (`axs['left']`).

**`fig.add_gridspec`** (from the slide):
```python
fig = plt.figure(figsize=(8, 6))
gs = fig.add_gridspec(3, 3)
ax1 = fig.add_subplot(gs[0, :])     # first row
ax2 = fig.add_subplot(gs[1, :-1])   # second row except last column
```

**`plt.axes([left, bottom, width, height])`**: place an Axes by hand in figure coordinates (0–1).

| Method (slide 16) | Character |
|---|---|
| `plt.subplots` | simple grids |
| `plt.subplot_mosaic` | named cells, complex layouts |
| `add_gridspec` | detailed control |

### 2. Seaborn

"Seaborn is based on matplotlib and provides a high-level interface for drawing attractive statistical graphics."

Four steps (slide): prepare data → control aesthetics → plot with Seaborn → customize further. Seaborn returns Matplotlib objects, so you finish with the OO API. Seaborn handles grouping, aggregation, error bars and colours from a DataFrame in one call; Matplotlib gives full control.

Plot families:

- **Distributions**: `histplot`, `kdeplot` (`sns.kdeplot(pokemon_df.Attack)`). A KDE is a smoothed estimate of the density, independent of bin width ([[Mathematical Statistics/contents/00-Index|Mathematical Statistics]]).
- **Joint plots**: `jointplot`, relationship in the centre and marginal distributions on the sides.
- **Pair plots**: the slide: "When you generalize joint plots to datasets of larger dimensions, you end up with pair plots... useful for exploring correlations between multidimensional data." `sns.pairplot(iris, hue='species')`. Grows as $O(n^2)$ panels.
- **Facet plots**: the slide: "Sometimes the best way to view data is via histograms of subsets. Seaborn's FacetGrid makes this extremely simple." The same plot for each subset (small multiples), the visual version of `groupby` ([[03 - Data Aggregation and Group Operations]]).
- **Factor and bar plots**: `catplot`, `barplot`. `barplot` shows the mean per category with a bootstrapped confidence interval.
- **Heatmaps**: `sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)`; design rules in [[11 - Chart Design and Data Storytelling]].

## ✏️ Exercises

**1.** Rewrite in OO style and explain why it is preferred.
> ```python
> plt.figure(figsize=(8, 4)); plt.plot(x, y); plt.title('Sales'); plt.xlabel('Month'); plt.ylim(0, 100)
> ```

> [!example]- Solution
> ```python
> fig, ax = plt.subplots(figsize=(8, 4))
> ax.plot(x, y); ax.set_title('Sales'); ax.set_xlabel('Month'); ax.set_ylim(0, 100)
> ```
> `plt.*` targets an implicit current figure; with several figures, a title can land on the wrong one with no error. `ax` is explicit and can be passed to functions or Seaborn (`sns.histplot(data, ax=axes[0, 1])`).

**2.** Distinguish Figure, Axes and Axis. What does `fig, axes = plt.subplots(2, 3)` return, and how do you reach the bottom-middle plot?

> [!example]- Solution
> Figure = canvas; Axes = one plot; Axis = one number line of an Axes. `plt.subplots(2, 3)` returns a Figure and a 2×3 array of Axes; bottom-middle is `axes[1, 1]`. With one row or column the array is 1-D (`axes[2]`); with no arguments you get a single Axes. `squeeze=False` always returns a 2-D array.

**3.** With `subplot_mosaic`, build: survival rate by class across the top, age by class (box plot) in two-thirds of the second row, an age histogram bottom right (Titanic).

> [!example]- Solution
> ```python
> titanic = sns.load_dataset('titanic')
> fig, axs = plt.subplot_mosaic([['bar', 'bar', 'bar'], ['box', 'box', 'hist']],
>                               figsize=(10, 6), layout='constrained')
> sns.barplot(data=titanic, x='class', y='survived', ax=axs['bar']); axs['bar'].set_title('Survival rate by class')
> sns.boxplot(data=titanic, x='class', y='age', ax=axs['box']); axs['box'].set_title('Age by class')
> sns.histplot(data=titanic, x='age', bins=20, ax=axs['hist']); axs['hist'].set_title('Age')
> ```
> The list is the layout; repeated labels span cells. The mean of the 0/1 `survived` column is the survival rate. The `add_gridspec` version (`gs[0, :]`, `gs[1, :-1]`, `gs[1, -1]`) is harder to read.

**4.** `pairplot` or correlation `heatmap`? When does the heatmap mislead?

> [!example]- Solution
> The heatmap is compact and scales to many variables; the pairplot shows actual joint distributions but becomes unreadable beyond about 10 columns.
>
> Pearson's $r$ measures linear association only: $y=x^2$ on $[-3,3]$ has $r\approx0$, a blank cell, while the pairplot shows a parabola. Simpson's paradox: subgroups with positive trends can pool to a negative correlation; `pairplot(hue='group')` shows it. Anscombe's quartet (`sns.load_dataset('anscombe')`) has correlation 0.816 in all four sets. Use the heatmap to find candidates, then look at the scatter.

**5.** (Advanced) What is faceting and why is it better than many colours on one Axes? Rebuild an overloaded chart with `FacetGrid`.

> [!example]- Solution
> Overloaded:
> ```python
> sns.scatterplot(data=tips, x='total_bill', y='tip', hue='day', style='time', size='size')
> ```
> Points overlap, and the reader must decode three channels from the legend at once.
>
> Faceted:
> ```python
> g = sns.FacetGrid(tips, col='day', row='time', height=3, margin_titles=True)
> g.map_dataframe(sns.scatterplot, x='total_bill', y='tip')
> g.set_axis_labels('Total bill', 'Tip')
> # or: sns.relplot(data=tips, x='total_bill', y='tip', col='day', row='time')
> ```
> Each panel is simple, and panels share scales by default, so comparison relies on position, which people judge accurately. Keep shared scales unless panels measure different things; with many categories, aggregate or facet on the important few.

## 📝 Summary

- Prefer Matplotlib's OO interface; OO methods use `set_`.
- Figure = canvas, Axes = one plot, Axis = one number line.
- Layouts: `subplots`, `subplot_mosaic` (named, spanning), `add_gridspec`, `plt.axes`; `sharex`/`sharey` for comparability.
- Seaborn is DataFrame-based and statistical, returns Matplotlib objects; four steps: data → aesthetics → plot → customize.
- `pairplot` for pairwise exploration, `heatmap` for correlation matrices (linear only).
- Facet instead of overloading one chart.

## ⚠️ Important Notes

1. `seaborn-*` style names fail in Matplotlib ≥ 3.6; use `seaborn-v0_8-*`.
2. Don't mix `plt.*` and OO calls in one figure.
3. The shape returned by `plt.subplots` varies; `squeeze=False` makes it consistent.
4. `barplot` shows means with confidence intervals, not totals (`estimator=sum` for totals, `errorbar=None` to drop the CI).
5. `pairplot` is $O(n^2)$; subset columns first.
6. Correlation heatmaps miss non-linear relationships and Simpson's paradox.
7. For correlation heatmaps set `center=0, vmin=-1, vmax=1`.
8. KDEs can show density where there is no data (or below zero for non-negative variables); show a histogram too or use `cut=0`.
9. Use `layout='constrained'` or `tight_layout()` to avoid overlapping labels.
10. Facets must share scales to be comparable.

> [!warning] Gaps in the source deck
> - Slide 3 (why visualize; only the `tips` load survives), slides 7–8 (figure anatomy; reconstructed), slide 9 (California cities practice), slide 12 (subplots example), slide 15 (`plt.axes` example) are images.
> - Slides 19–26 (the Seaborn half) are mostly images: only `sns.kdeplot(pokemon_df.Attack)` and the pair-plot and FacetGrid paragraphs extract. Joint plots, the Iris practice, factor/bar plots, heatmap and the correlation practice are reconstructed from the standard API.
> - Datasets: `tips`, `iris`, `titanic` (via `sns.load_dataset`) and `pokemon_df` (not in `documents/`).

**Previous:** [[09 - Building Pipelines]] · **Next:** [[11 - Chart Design and Data Storytelling]]
