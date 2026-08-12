---
subject: Data Preparation and Visualization
chapter: 03
tags: [ds, pandas, groupby, aggregation, pivot-table]
source: "Lesson 3_Data Aggregation and Group Operations.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Data Aggregation and Group Operations

> [!note] Where this sits in the course
> Closing chapter of **Part 1 — Mastering the Tools**. [[01 - Getting Started with Pandas]] gave you the objects, [[02 - Loading, Diagnosing, Missing Data and Combining Datasets]] got real data in and joined it. This chapter is where data becomes an *answer*: collapsing thousands of rows into the handful of numbers a manager actually reads.

## 📘 Main Knowledge

### 1. Simple aggregation

Aggregation reduces many values to one. `sum()`, `mean()`, `count()`, `min()`, `max()`, `median()`, `std()`, `var()`, `prod()`, `first()`, `last()` all apply directly to a Series or DataFrame.

```python
import seaborn as sns
planets = sns.load_dataset('planets')
planets.head()
```

The `planets` dataset (exoplanet discoveries) is the running example:

| Column | Meaning |
|---|---|
| `method` | Detection method used to find the planet |
| `number` | Number of planets in that planetary system |
| `orbital_period` | Orbital period, in days |
| `mass` | Planet mass, in Jupiter masses |
| `distance` | Distance from Earth, in parsecs |
| `year` | Year of discovery |

On a DataFrame, aggregations run **per column** by default (`axis=0`) and **skip `NaN`** silently. `describe()` runs the common ones at once.

### 2. GroupBy: split, apply, combine

The central idea of the chapter. `groupby()` implements a three-stage strategy:

1. **Split** — partition rows into groups by the value of a key.
2. **Apply** — run a function within each group independently.
3. **Combine** — reassemble the per-group results into one object.

```python
df = pd.DataFrame({'key': list("ABCABC"), "data": range(6)},
                  columns=['key', 'data'])
df.groupby('key').sum()
```

**The key must be categorical or discrete.** Grouping on a continuous variable creates one group per distinct value, which is useless — bin it first with `pd.cut` (see [[07 - Data Transformation]]).

`df.groupby('key')` on its own returns a lazy `GroupBy` object; nothing is computed until you apply something to it.

### 3. The four group operations

This is the section to know cold. Four verbs, distinguished by **what they return**.

```python
df = pd.DataFrame({'key': list("ABCABC"),
                   "data1": range(6),
                   'data2': range(6, 12)},
                  columns=['key', 'data1', 'data2'])

def myfunc(x):
    return x.sum() // 2
```

**Aggregate (`agg`) — many functions at once, one row per group.**

```python
df.groupby('key').aggregate(['sum', 'min', myfunc])            # all columns, all funcs
df.groupby('key').aggregate({'data1': ['sum', 'min'],          # per-column control
                             'data2': myfunc})
```
Accepts a string, a function, a list, or a dict mapping column → function(s). The dict form is what you use to build a real summary report.

**Filter — drop entire groups on a group-level condition.**

```python
df.groupby('key').filter(lambda x: x.data1.sum() >= 5)
```
The lambda receives the whole group and must return a single `True`/`False`. Groups returning `False` disappear **with all their rows**. This is fundamentally different from boolean masking, which tests rows individually: filter asks *"is this group worth keeping?"*, e.g. "drop products with fewer than 10 sales."

**Transform — same shape in, same shape out.**

```python
df.groupby('key').transform(lambda x: x - x.mean())   # centre within group
```
Returns an object **the same size as the original**, so the result can be assigned straight back as a new column. This is the tool for group-wise normalisation: "express each student's score relative to their own class average."

**Apply — arbitrary function, arbitrary output shape.**

```python
df.groupby('key').apply(lambda x: x / x.sum())
```
The escape hatch. Maximum flexibility, worst performance — prefer one of the three above when it fits.

| Verb | Receives | Returns | Use for |
|---|---|---|---|
| `agg` | group | one row per group | Summary tables |
| `filter` | group | the group, or nothing | Dropping small/irrelevant groups |
| `transform` | group | **same shape as input** | Group-wise normalisation |
| `apply` | group | anything | Everything else |

### 4. MultiIndex — hierarchical indexing

A `MultiIndex` lets an axis carry **more than one level** of labels, so genuinely multi-dimensional data fits in a two-dimensional table. It works on rows and on columns.

```python
index = [('California', 2000), ('California', 2010),
         ('New York', 2000), ('New York', 2010),
         ('Texas', 2000), ('Texas', 2010)]
populations = [33871648, 37253956, 18976457, 19378102, 20851820, 25145561]
under18 = [9267089, 9284094, 4687374, 4318033, 5906301, 6879014]

ind = pd.MultiIndex.from_tuples(index, names=('states', 'years'))
pop = pd.DataFrame({'pop': populations, 'under_18': under18}, index=ind)
```

**Accessing:**
```python
pop.loc['New York']            # slice the outer level
pop.xs(2010, level='years')    # cross-section on an INNER level
```
`.xs()` exists because `.loc` naturally indexes from the outside in; `.xs` reaches a named level directly.

**Building one from existing columns** — the common route in practice:
```python
df_multi_index = df.set_index(['Country', 'State'])
```

Note that `groupby()` on multiple keys *produces* a MultiIndex automatically — the two features are two views of the same idea.

### 5. Reshaping: `stack` and `unstack`

- **`stack()`** pushes column labels down into the row index → **long** format.
- **`unstack()`** lifts an index level up into columns → **wide** format.

They are inverses. Long format is what databases and plotting libraries want; wide format is what humans read. `unstack()` is what turns a `groupby` result into a readable cross-tabulation:

```python
titanic.groupby(['class', 'sex'])['survived'].mean().unstack()
```

### 6. Pivot tables

A pivot table is `groupby` + `unstack` in one call — the spreadsheet idiom, made declarative. The two lines below are equivalent:

```python
titanic.groupby(['class', 'sex'])['survived'].mean().unstack()

pd.pivot_table(data=titanic, index='class', columns='sex', values='survived')
```

```python
DataFrame.pivot_table(data, values=None, index=None, columns=None,
                      aggfunc='mean', fill_value=None, margins=False,
                      dropna=True, margins_name='All', observed=False, sort=True)
```

| Parameter | Role |
|---|---|
| `values` | Column(s) to aggregate. Omitted → all remaining numeric columns |
| `index` | Grouping keys that become **rows** |
| `columns` | Grouping keys that become **columns** |
| `aggfunc` | `'mean'` (default), `'sum'`, `'count'`, a list, or a dict per column |
| `fill_value` | Replacement for missing cells |
| `margins` | `True` adds row/column totals |
| `margins_name` | Label for the totals row/column (default `'All'`) |
| `dropna` | Drop all-`NaN` columns (default `True`) |
| `observed` | For categorical keys, show only observed combinations |

**`aggfunc='mean'` on a 0/1 column gives a rate** — which is why the Titanic survival pivot reads directly as survival *probability* by class and sex.

Binning a continuous variable first lets it serve as a pivot key:
```python
age_groups = pd.cut(titanic['age'], bins=[0, 12, 18, 35, 60, 80],
                    labels=['Child', 'Teen', 'Adult', 'Middle-aged', 'Senior'])
titanic['age_group'] = age_groups
```

### 7. Quick visualisation with `.plot()`

Pandas wraps Matplotlib so a DataFrame can plot itself — ideal for exploration, before the deliberate design work of [[10 - Visualization with Matplotlib and Seaborn]].

```python
df = pd.pivot_table(data=births, index='year', columns='gender',
                    values='births', aggfunc='sum')

df.plot(kind='line', title='Title-1', xlabel='X-axis', ylabel='Y-axis')
df.plot(kind='bar')
df.plot(kind='hist')
df.plot(kind='box')
df.plot(kind='scatter', x='F', y='M')
```

`kind` accepts: `'line'` (default), `'bar'`, `'barh'`, `'hist'`, `'box'`, `'kde'`/`'density'`, `'area'`, `'pie'`, `'scatter'` (DataFrame only), `'hexbin'` (DataFrame only).

**The pivot-then-plot pattern is the workflow**: aggregate into a small tidy table, then call `.plot()` on it. Plotting raw un-aggregated data almost never produces a readable chart.

### 8. The standard cleaning workflow

The lecturer's checklist for approaching any new dataset — not necessarily in this order:

1. Read data into a DataFrame
2. Display the top of the DataFrame
3. Display column data types
4. Display non-missing values
5. Replace NA with a value
6. Iterate through the columns
7. Statistics for each column
8. Find missing values
9. Total missing values
10. Percentage of missing values
11. Sort table values
12. Print summary information
13. Identify columns with > 50% missing values
14. Rename columns

Steps 8–10 and 13 are the quality audit that decides what the rest of [[06 - Data Cleaning]] has to do.

## ✏️ Exercises

**1.** On the `planets` dataset, compute: the total number of planets discovered, the average orbital period, the number of unique discovery methods, the maximum mass, and the minimum distance from Earth.

> [!example]- Solution
> ```python
> planets['number'].sum()          # 1035 planets
> planets['orbital_period'].mean() # ≈ 2002.9 days
> planets['method'].nunique()      # 10 methods
> planets['mass'].max()            # 25.0 Jupiter masses
> planets['distance'].min()        # ≈ 1.35 parsecs
> ```
> Two things to notice. First, `mean()` **skips `NaN` by default** — `orbital_period` has missing values, so this is the mean of the observed entries, not of all 1,035 rows. That is usually what you want, but you should know it is happening: check `planets['orbital_period'].count()` against `len(planets)`.
>
> Second, the mean orbital period (~2,000 days) is wildly higher than the median (~40 days). That gap is a **massive right skew** — a handful of very long-period planets dragging the mean. Reporting the mean alone here would misrepresent the data.

**2.** Using the DataFrame below, explain what each of the two statements returns and why they differ.
> ```python
> df = pd.DataFrame({'key': list("ABCABC"), "data1": range(6), 'data2': range(6, 12)})
> # 1. df.groupby('key').sum()
> # 2. df.groupby('key').filter(lambda x: x.data1.sum() >= 5)
> ```

> [!example]- Solution
> Groups are `A = rows 0,3`, `B = rows 1,4`, `C = rows 2,5`, so `data1` sums are A=3, B=5, C=7.
>
> **Statement 1** aggregates — one row per group, original rows gone:
> ```
>      data1  data2
> key
> A        3     15
> B        5     17
> C        7     19
> ```
>
> **Statement 2** filters — it returns **original rows**, keeping only those belonging to groups passing the test. Group A sums to 3 (< 5) so it is dropped entirely; B and C survive:
> ```
>   key  data1  data2
> 1   B      1      7
> 2   C      2      8
> 4   B      4     10
> 5   C      5     11
> ```
>
> The distinction: `sum()` changes the shape to one-row-per-group; `filter()` preserves the original shape and granularity, only removing whole groups. Filter is a *row-selection* tool driven by a *group-level* fact — something no boolean mask can express.

**3.** For each discovery method in `planets`, compute the total planets discovered and the average mass in a single call. Then keep only the methods that have discovered more than 20 planets in total.

> [!example]- Solution
> ```python
> # Combined aggregation, one function per column
> planets.groupby('method').agg({'number': 'sum', 'mass': 'mean'})
>
> # Filter to productive methods — filter() operates on ROWS, so aggregate after
> productive = planets.groupby('method').filter(lambda x: x['number'].sum() > 20)
> productive.groupby('method').agg({'number': 'sum', 'mass': 'mean'})
> ```
> The ordering trap: `filter` returns the original rows, so you must group *again* to summarise them. If you only want the summary table, it is simpler to aggregate first and mask the result:
> ```python
> summary = planets.groupby('method').agg({'number': 'sum', 'mass': 'mean'})
> summary[summary['number'] > 20]
> ```
> Use `filter` when you need the underlying rows for further work; use the mask when you only need the report. Radial Velocity and Transit dominate — they account for the overwhelming majority of discoveries, and most other methods have almost no `mass` measurements at all (so their mean mass is `NaN`).

**4.** Build a pivot table showing the Titanic survival rate by age group and passenger class. Bin the ages first.

> [!example]- Solution
> ```python
> titanic['age_group'] = pd.cut(titanic['age'], bins=[0, 12, 18, 35, 60, 80],
>                               labels=['Child', 'Teen', 'Adult', 'Middle-aged', 'Senior'])
>
> pd.pivot_table(titanic, index='age_group', columns='pclass',
>                values='survived', aggfunc='mean', observed=True)
> ```
> Because `survived` is coded 0/1, the mean **is** the survival rate — no extra arithmetic needed. That idiom is worth internalising.
>
> The result shows first-class children surviving at or near 100% while third-class adults sit around 20% — the "women and children first" protocol, but visibly stratified by ticket price.
>
> Two practical notes. `pd.cut` returns a **categorical**, so pass `observed=True` to avoid rows for empty combinations. And the 177 missing ages become `NaN` in `age_group` and are dropped from the table entirely — meaning this pivot silently describes only 714 of 891 passengers. Always report which rows an aggregate actually covers.

**5.** (Advanced) Using the CDC births data, add a `decade` column and compare male and female births by decade. Then explain why a naive `mean()` of the `births` column is misleading and what the data quality issue is.
> ```python
> births = pd.read_csv('https://raw.githubusercontent.com/jakevdp/data-CDCbirths/master/births.csv')
> ```

> [!example]- Solution
> ```python
> births['decade'] = 10 * (births['year'] // 10)
> births.pivot_table('births', index='decade', columns='gender', aggfunc='sum')
> ```
> Integer division floors the year to its decade — `1995 // 10 * 10 = 1990`. The table shows male births exceeding female consistently, by roughly 5% every decade. That is a real biological constant (the human sex ratio at birth is ~1.05), not a data artefact — a good sanity check that the pipeline is correct.
>
> ```python
> births.pivot_table('births', index='year', columns='gender', aggfunc='sum').plot()
> ```
>
> **The data quality issue:** the `day` column contains the value **99** as a placeholder for "unknown day", and some rows carry impossible dates. A naive aggregate absorbs these silently. The standard robust cleanup is a **sigma-clip** on the counts:
> ```python
> quartiles = np.percentile(births['births'], [25, 50, 75])
> mu, sig = quartiles[1], 0.74 * (quartiles[2] - quartiles[0])   # robust σ estimate
> births = births.query('(births > @mu - 5 * @sig) & (births < @mu + 5 * @sig)')
> births = births[births['day'] <= 31]
> ```
> The `0.74 * IQR` factor is a robust estimate of the standard deviation for normally distributed data — robust because it ignores the tails that outliers live in, unlike `std()` which they contaminate. Outlier handling proper is [[06 - Data Cleaning]].
>
> This exercise is the whole course in miniature: load → diagnose → clean → aggregate → visualise, with a quality check that would have poisoned every downstream number had it been skipped.

## 📝 Summary

- **GroupBy = split, apply, combine.** Partition by a key, compute within each group, reassemble.
- **Group keys must be discrete.** Bin continuous variables with `pd.cut` first.
- **Four verbs, distinguished by output shape:** `agg` → one row per group; `filter` → whole groups kept or dropped, rows unchanged; `transform` → **same shape as input**; `apply` → anything.
- **`transform` is the one to reach for when assigning back** to a column (group-wise normalisation).
- **MultiIndex holds >1 label level per axis**; `.loc` indexes outside-in, `.xs(level=...)` reaches inner levels directly.
- **`stack`/`unstack` convert long ↔ wide** and are exact inverses.
- **`pivot_table` = groupby + unstack**, with `margins=True` for totals. `aggfunc='mean'` on a 0/1 column yields a rate.
- **`.plot(kind=...)` on an aggregated table** is the fast exploratory path; aggregate first, plot second.

## ⚠️ Important Notes

**`filter` and boolean masking answer different questions.** A mask tests each row on its own values. `filter` tests a *group-level* property and then keeps or drops **every row of that group**. "Keep customers whose *total* spend exceeds $1,000" is impossible with a mask alone.

**`transform` vs `agg` — the assignment test.** If you intend `df['new_col'] = ...`, you need `transform`; `agg` returns fewer rows and the assignment will fail or misalign. `df['pct_of_group'] = df.groupby('key')['data'].transform(lambda x: x / x.sum())` works; the same with `agg` does not.

**`groupby` drops `NaN` keys by default.** Rows whose grouping key is missing vanish from the output entirely, so group totals may not sum to the dataset total. Pass `dropna=False` to keep them as their own group.

**`groupby` sorts keys by default**, which costs time on large data. `groupby(..., sort=False)` is faster when you do not need ordered output.

**`.apply()` on a GroupBy is slow.** It runs Python-level code per group. If `agg`, `transform`, or `filter` can express the operation, they will be substantially faster — the difference is large enough to matter on real datasets.

**Aggregations skip `NaN` silently.** `mean()` divides by the count of *non-missing* values, not the row count. A column that is 60% missing still reports a confident-looking mean. Always compare `.count()` to `len(df)`.

**Chained `groupby(...)['col'].mean().unstack()` and `pivot_table` are the same operation.** Use `pivot_table` when the goal is a readable report (it has `margins`, `fill_value`); use the chain when it is one step inside a longer pipeline.

**Pivot tables built on `pd.cut` categories need `observed=True`.** Otherwise Pandas generates rows for every possible category combination, including empty ones — cluttering the table with `NaN`.

**Beware the mean when the median is far away.** `planets['orbital_period']` has mean ≈ 2,003 and median ≈ 40. Reporting the mean is technically true and practically a lie. `.describe()` exposes this in one line.

**`np.percentile` and sigma-clipping beat `std()` for outlier detection**, because the outliers you are hunting are themselves inflating `std()`. The robust estimator $\hat{\sigma} \approx 0.74 \times \text{IQR}$ is not contaminated by the tails.

> [!warning] Gaps in the source slides
> - **Slide 3** — the table of built-in Pandas aggregations is an image; the list above is reconstructed from the standard set.
> - **Slide 11** — "Creating a MultiIndex" is entirely an image, so the lecturer's construction examples (`from_arrays`, `from_product`) are not captured. Slide 12's `from_tuples` example survives and is included.
> - **Slide 14** — the stack/unstack long↔wide diagram is an image; only the captions are text.
> - **Slide 4** describes the `planets` columns in **Vietnamese**; I have translated them into the table above.
>
> Source for the MultiIndex and pivot-table material: VanderPlas, *Python Data Science Handbook* Ch. 3. Slide 20 links the official [`DataFrame.plot` documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html).

---
**Previous:** [[02 - Loading, Diagnosing, Missing Data and Combining Datasets]] · **Next:** [[05 - String Manipulation and Time Series Data]]
