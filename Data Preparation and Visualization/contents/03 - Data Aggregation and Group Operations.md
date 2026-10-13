---
subject: Data Preparation and Visualization
chapter: 03
tags: [ds, pandas, groupby, aggregation, pivot-table]
source: "Lesson 3_Data Aggregation and Group Operations.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Data Aggregation and Group Operations

Last chapter of Part 1. After loading and joining data ([[02 - Loading, Diagnosing, Missing Data and Combining Datasets]]), aggregation turns thousands of rows into the few numbers a manager reads.

## 📘 Main Knowledge

### 1. Simple aggregation

`sum()`, `mean()`, `count()`, `min()`, `max()`, `median()`, `std()`, `var()`, `prod()`, `first()`, `last()` work on a Series or DataFrame. On a DataFrame they run per column (`axis=0`) and skip `NaN`. `describe()` runs the common ones together.

Running example: `planets = sns.load_dataset('planets')` (exoplanet discoveries).

| Column | Meaning |
|---|---|
| `method` | detection method |
| `number` | number of planets in the system |
| `orbital_period` | orbital period (days) |
| `mass` | mass (Jupiter masses) |
| `distance` | distance from Earth (parsecs) |
| `year` | year of discovery |

### 2. GroupBy: split, apply, combine

1. **Split** rows into groups by a key.
2. **Apply** a function to each group.
3. **Combine** the results.

```python
df = pd.DataFrame({'key': list("ABCABC"), "data": range(6)})
df.groupby('key').sum()
```

The key should be categorical or discrete; a continuous key gives one group per value, so bin it first with `pd.cut` ([[07 - Data Transformation]]). `df.groupby('key')` alone is a lazy object; nothing is computed until you apply something.

### 3. The four group operations

```python
df = pd.DataFrame({'key': list("ABCABC"), "data1": range(6), 'data2': range(6, 12)})
def myfunc(x):
    return x.sum() // 2
```

**`agg`: one row per group**
```python
df.groupby('key').aggregate(['sum', 'min', myfunc])
df.groupby('key').aggregate({'data1': ['sum', 'min'], 'data2': myfunc})   # per column
```

**`filter`: keep or drop whole groups**
```python
df.groupby('key').filter(lambda x: x.data1.sum() >= 5)
```
The function gets a group and returns one True/False; a False group disappears with all its rows (e.g. "drop products with fewer than 10 sales"). A boolean mask tests rows individually and cannot express this.

**`transform`: output has the same shape as the input**
```python
df.groupby('key').transform(lambda x: x - x.mean())   # center within each group
```
Can be assigned back as a new column; used for group-wise normalization (score relative to the class average).

**`apply`: any function, any output shape**
```python
df.groupby('key').apply(lambda x: x / x.sum())
```
Most flexible, slowest; prefer the other three when they fit.

| Verb | Returns | Use for |
|---|---|---|
| `agg` | one row per group | summary tables |
| `filter` | the original rows of the groups that pass | dropping small or irrelevant groups |
| `transform` | same shape as input | group-wise normalization, new columns |
| `apply` | anything | everything else |

### 4. MultiIndex

A `MultiIndex` gives an axis several levels of labels, so multi-dimensional data fits in a 2-D table.

```python
index = [('California', 2000), ('California', 2010), ('New York', 2000),
         ('New York', 2010), ('Texas', 2000), ('Texas', 2010)]
populations = [33871648, 37253956, 18976457, 19378102, 20851820, 25145561]
under18 = [9267089, 9284094, 4687374, 4318033, 5906301, 6879014]
ind = pd.MultiIndex.from_tuples(index, names=('states', 'years'))
pop = pd.DataFrame({'pop': populations, 'under_18': under18}, index=ind)

pop.loc['New York']            # outer level
pop.xs(2010, level='years')    # inner level
df.set_index(['Country', 'State'])   # build one from columns
```

`groupby` on several keys produces a MultiIndex automatically.

### 5. `stack` and `unstack`

- `stack()` moves column labels into the row index (long format).
- `unstack()` moves an index level into columns (wide format).

They are inverses. Long format suits databases and plotting libraries; wide format suits people.

```python
titanic.groupby(['class', 'sex'])['survived'].mean().unstack()
```

### 6. Pivot tables

A pivot table is `groupby` + `unstack` in one call. These are equivalent:

```python
titanic.groupby(['class', 'sex'])['survived'].mean().unstack()
pd.pivot_table(data=titanic, index='class', columns='sex', values='survived')
```

| Parameter | Role |
|---|---|
| `values` | column(s) to aggregate (default: remaining numeric columns) |
| `index` | keys that become rows |
| `columns` | keys that become columns |
| `aggfunc` | `'mean'` (default), `'sum'`, `'count'`, a list, or a dict |
| `fill_value` | value for empty cells |
| `margins`, `margins_name` | add totals (labelled `'All'`) |
| `dropna` | drop all-NaN columns (default True) |
| `observed` | for categorical keys, show only observed combinations |

The mean of a 0/1 column is a rate, so the Titanic pivot reads as survival probability by class and sex. Bin continuous variables to use them as keys:

```python
titanic['age_group'] = pd.cut(titanic['age'], bins=[0, 12, 18, 35, 60, 80],
                              labels=['Child', 'Teen', 'Adult', 'Middle-aged', 'Senior'])
```

### 7. Quick plots with `.plot()`

```python
df = pd.pivot_table(data=births, index='year', columns='gender', values='births', aggfunc='sum')
df.plot(kind='line', title='Title-1', xlabel='X-axis', ylabel='Y-axis')
df.plot(kind='bar'); df.plot(kind='hist'); df.plot(kind='box')
df.plot(kind='scatter', x='F', y='M')
```

`kind`: `'line'` (default), `'bar'`, `'barh'`, `'hist'`, `'box'`, `'kde'`, `'area'`, `'pie'`, `'scatter'` and `'hexbin'` (DataFrames only). Aggregate first into a small table, then plot; raw rows rarely make a readable chart. Deliberate chart design is in [[10 - Visualization with Matplotlib and Seaborn]].

### 8. Standard checklist for a new dataset

From the lecturer (order flexible): read into a DataFrame; show the top rows; show dtypes; show non-missing counts; replace NA; iterate through columns; per-column statistics; find missing values; total missing; percentage missing; sort values; print a summary; identify columns with > 50% missing; rename columns. The missing-value audit decides the work in [[06 - Data Cleaning]].

## ✏️ Exercises

**1.** On `planets`, compute total planets, average orbital period, number of methods, maximum mass, minimum distance.

> [!example]- Solution
> ```python
> planets['number'].sum()          # 1035
> planets['orbital_period'].mean() # ≈ 2002.9 days
> planets['method'].nunique()      # 10
> planets['mass'].max()            # 25.0
> planets['distance'].min()        # ≈ 1.35 parsecs
> ```
> `mean()` skips missing values (compare `.count()` with `len(planets)`). The mean orbital period (~2,000 days) is far above the median (~40 days): strong right skew, so the mean alone misleads.

**2.** For the DataFrame in §3, what do `df.groupby('key').sum()` and `df.groupby('key').filter(lambda x: x.data1.sum() >= 5)` return?

> [!example]- Solution
> Groups: A = rows 0, 3; B = 1, 4; C = 2, 5; `data1` sums A 3, B 5, C 7.
>
> `sum()`: one row per group: A (3, 15), B (5, 17), C (7, 19).
>
> `filter`: the original rows of groups passing the test; A (sum 3) is dropped:
> ```
>   key  data1  data2
> 1   B      1      7
> 2   C      2      8
> 4   B      4     10
> 5   C      5     11
> ```

**3.** For each method in `planets`, compute total planets and average mass in one call, then keep only methods with more than 20 planets.

> [!example]- Solution
> ```python
> summary = planets.groupby('method').agg({'number': 'sum', 'mass': 'mean'})
> summary[summary['number'] > 20]
> # or, if you need the rows themselves:
> productive = planets.groupby('method').filter(lambda x: x['number'].sum() > 20)
> ```
> `filter` returns rows, so you would group again to summarize. Radial Velocity and Transit dominate; most other methods have almost no mass measurements (mean mass `NaN`).

**4.** Pivot Titanic survival rate by age group and class.

> [!example]- Solution
> ```python
> titanic['age_group'] = pd.cut(titanic['age'], bins=[0, 12, 18, 35, 60, 80],
>                               labels=['Child', 'Teen', 'Adult', 'Middle-aged', 'Senior'])
> pd.pivot_table(titanic, index='age_group', columns='pclass', values='survived',
>                aggfunc='mean', observed=True)
> ```
> First-class children survive at or near 100%, third-class adults around 20%. `pd.cut` gives a categorical, so use `observed=True`. The 177 missing ages are excluded: the table covers 714 of 891 passengers.

**5.** (Advanced) With the CDC births data, add a `decade` column and compare male and female births by decade. What data-quality issue affects naive aggregates?
> ```python
> births = pd.read_csv('https://raw.githubusercontent.com/jakevdp/data-CDCbirths/master/births.csv')
> ```

> [!example]- Solution
> ```python
> births['decade'] = 10 * (births['year'] // 10)
> births.pivot_table('births', index='decade', columns='gender', aggfunc='sum')
> ```
> Male births exceed female by about 5% each decade (the sex ratio at birth ≈ 1.05), a useful sanity check.
>
> The `day` column uses 99 for "unknown", and some rows have impossible dates. A robust clean-up (sigma clipping):
> ```python
> q = np.percentile(births['births'], [25, 50, 75])
> mu, sig = q[1], 0.74 * (q[2] - q[0])          # robust estimate of σ
> births = births.query('(births > @mu - 5 * @sig) & (births < @mu + 5 * @sig)')
> births = births[births['day'] <= 31]
> ```
> $0.74\times\text{IQR}$ estimates σ for normal data without being inflated by outliers, unlike `std()`. See [[06 - Data Cleaning]].

## 📝 Summary

- GroupBy = split, apply, combine; keys must be discrete (bin continuous ones).
- `agg` → one row per group; `filter` → whole groups kept or dropped; `transform` → same shape (assignable); `apply` → anything.
- MultiIndex: several label levels; `.loc` outer-in, `.xs(level=...)` for inner levels.
- `stack`/`unstack` convert long ↔ wide.
- `pivot_table` = groupby + unstack, with `margins` for totals; the mean of a 0/1 column is a rate.
- Aggregate first, then `.plot()`.

## ⚠️ Important Notes

1. `filter` tests a group property and keeps or drops all its rows; a mask tests rows.
2. To assign a group result back to a column, use `transform`, not `agg`.
3. `groupby` drops rows with `NaN` keys unless `dropna=False`.
4. `groupby` sorts keys; `sort=False` is faster.
5. `GroupBy.apply` runs Python per group and is slow.
6. Aggregations skip `NaN`; compare `.count()` with `len(df)`.
7. Use `observed=True` with categorical keys from `pd.cut`.
8. When mean and median differ a lot, report the median too.
9. For outlier detection, robust estimates (IQR-based) beat `std()`.

> [!warning] Gaps in the source slides
> - Slide 3 (table of built-in aggregations) is an image; the list is the standard set.
> - Slide 11 ("Creating a MultiIndex": `from_arrays`, `from_product`) is an image; slide 12's `from_tuples` example is included.
> - Slide 14 (stack/unstack diagram) is an image.
> - Slide 4 describes the `planets` columns in Vietnamese; translated above.
> - Source for MultiIndex and pivot tables: VanderPlas, *Python Data Science Handbook*, ch. 3.

**Previous:** [[02 - Loading, Diagnosing, Missing Data and Combining Datasets]] · **Next:** [[05 - String Manipulation and Time Series Data]]
