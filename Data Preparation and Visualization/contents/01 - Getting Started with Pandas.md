---
subject: Data Preparation and Visualization
chapter: 01
tags: [ds, pandas, data-wrangling, python]
source: "Lesson 1_Getting started with Pandas.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Getting Started with Pandas

First chapter of Part 1 (Mastering the Tools). Later chapters on cleaning, transforming, feature selection and plotting all use the vocabulary introduced here. See [[00-Index]].

## 📘 Main Knowledge

### Why Pandas

Pandas is the standard Python library for tabular data. Its main addition to NumPy is **labels**: it attaches row and column labels to data and keeps them correct through every operation.

- **Flexible**: one table can hold numbers, strings and dates.
- **Powerful**: joins, group-bys and reshaping are single method calls.
- **Fast**: the core is written in C/Cython.

```python
import pandas as pd
```

### The three building blocks

| Object | Dimensions | Think of it as |
|---|---|---|
| `Series` | 1-D | one labelled column |
| `DataFrame` | 2-D | a table: several Series sharing one index |
| `Index` | — | the axis labels |

**Series**: values plus an index.

```python
s1 = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
s2 = pd.Series({'Hanoi': 1000, 'HCMC': 2000})        # dict keys become the index
country_population = pd.Series([61, 46, 11, 65, 10],
                               index=["IT", "ES", "GR", "FR", "PO"],
                               name="Country Population")
```

`s2['HCMC']` is clearer than `s2[1]`. Attributes: `.index`, `.values`.

**DataFrame**: a 2-D table with named columns and a row index. Every CSV, SQL table or Excel sheet you load becomes one.

```python
df = pd.DataFrame({'Province': ['Hanoi', 'HCMC', 'Danang'],
                   'Population (millions)': [8.05, 8.99, 1.13]})
```

Attributes: `.index`, `.columns`, `.values`.

**Index**:
1. Immutable: `df.index[0] = 5` raises `TypeError`, so indexes can be shared safely between objects.
2. Set-like: supports `union`, `intersection` etc., which is what makes alignment and joins work.

Best practice: use a unique, meaningful index (`OrderID`, `CustomerID`) rather than the default integers.

### Reindexing and dropping

```python
s1.reindex(['a', 'b', 'c', 'd'], fill_value=0)   # new label 'd' gets 0 (NaN without fill_value)
df.drop(1)                                       # drop row labelled 1
df.drop('Province', axis=1)                      # axis=1: columns
```

Both return a new object unless `inplace=True`.

### Selecting data: four tools

**1. `[]` for columns**
```python
df['Province']                              # Series
df[['Province', 'Population (millions)']]   # DataFrame
```
`df.Province` also works but fails for names with spaces or names that clash with methods (`df.count`).

**2. `.loc`: by label**, `df.loc[rows, cols]`
```python
df.loc[0]
df.loc[[0, 2]]
df.loc[0:1]                          # label slice: endpoint INCLUDED
df.loc[0, 'Population (millions)']
df.loc[[0, 2], ['Province']]
```

**3. `.iloc`: by position**, `df.iloc[rows, cols]`
```python
df.iloc[0]
df.iloc[[0, 2]]
df.iloc[0:2]                         # position slice: endpoint EXCLUDED
df.iloc[0, 1]
```

**4. Boolean masks: filter rows by value**
```python
df[df['Population (millions)'] > 5]
df[(df['Population (millions)'] > 1) & (df['Population (millions)'] < 9)]   # parentheses required
```

Rule of thumb: `[]` for columns, `.loc`/`.iloc` for rows and cells, masks for conditions.

### Arithmetic aligns on the index

```python
s1 = pd.Series([7.3, -2.5, 3.4], index=['a', 'c', 'd'])
s2 = pd.Series([-2.1, 3.6, -1.5], index=['a', 'c', 'e'])
s1 + s2                      # 'a', 'c' computed; 'd', 'e' → NaN
s1.add(s2, fill_value=0)     # treat a missing label as 0
```

Pandas matches labels before computing, so it never adds unrelated rows by position. The price is unexpected `NaN`s; check results. Missing data is handled in [[02 - Loading, Diagnosing, Missing Data and Combining Datasets]].

### `apply` vs `map`

- **`.apply(func, axis=0/1)`** on a DataFrame passes a whole column (axis=0) or row (axis=1). Use it when the result depends on several columns.
- **`.map(func)`** on a Series passes one element at a time. Use it for reformatting or recoding values.

```python
df['Population (millions)'].map(lambda x: f'{x:.2f} million people')
```

Element-wise recoding leads to categorical encoding in [[07 - Data Transformation]].

### Sorting and ranking

```python
df.sort_values(by='Population (millions)', ascending=False)
df['Population (millions)'].rank(method='first')
```

`rank` gives each value its position in the order without reordering the table.

### Descriptive statistics

```python
data_num.sum()          # per column
data_num.mean(axis=1)   # per row
data_num.describe()     # count, mean, std, min, quartiles, max
```

Two signals in `describe()`:
- **Outliers**: max far above the 75th percentile (or min far below the 25th).
- **Skew**: mean far from the median (50%).

Both feed into [[06 - Data Cleaning]] and [[07 - Data Transformation]].

### Correlation and covariance

```python
data_num['a'].corr(data_num['b'])
data_num.cov()
```

$$\operatorname{cov}(X,Y) = \mathbb{E}\big[(X - \mu_X)(Y - \mu_Y)\big],\qquad \rho_{X,Y} = \frac{\operatorname{cov}(X,Y)}{\sigma_X\sigma_Y}\in[-1,1]$$

A high correlation suggests a predictive relationship ([[Machine Learning/contents/00-Index|Machine Learning]]) but does not show causation. Theory in [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]].

### Categorical variables

```python
df['Province'].unique()
df['Province'].value_counts()          # frequencies; reveals segments and class imbalance
df['Province'].isin(['Hanoi', 'Can Tho'])
```

## ✏️ Exercises

**1.** With `s1 = pd.Series([10, 20, 30], index=['a', 'b', 'c'])`, what do `s1.loc['a':'b']` and `s1.iloc[0:2]` return? Why?

> [!example]- Solution
> Both return `a → 10, b → 20`, for different reasons: `.loc` slices by label and includes the endpoint `'b'`; `.iloc` slices by position and excludes position 2, like a Python list. They agree here by coincidence; `.loc['a':'c']` returns three elements while `.iloc[0:2]` returns two.

**2.** Compute `s1 + s2` for the Series below. Which labels give `NaN`? Rewrite so missing labels count as zero.
> ```python
> s1 = pd.Series([7.3, -2.5, 3.4], index=['a', 'c', 'd'])
> s2 = pd.Series([-2.1, 3.6, -1.5], index=['a', 'c', 'e'])
> ```

> [!example]- Solution
> | label | s1 | s2 | s1 + s2 |
> |---|---|---|---|
> | a | 7.3 | −2.1 | 5.2 |
> | c | −2.5 | 3.6 | 1.1 |
> | d | 3.4 | — | NaN |
> | e | — | −1.5 | NaN |
>
> `d` and `e` appear in only one Series. `s1.add(s2, fill_value=0)` gives d = 3.4, e = −1.5. This differs from `(s1 + s2).fillna(0)`, which gives d = 0.

**3.** Load Titanic (`sns.load_dataset('titanic')`). Sort by age descending, compute the survival rate, and count the values of `embarked`.

> [!example]- Solution
> ```python
> import seaborn as sns
> df = sns.load_dataset('titanic')
> df.sort_values(by='age', ascending=False)     # NaN ages go last
> df['survived'].mean()                         # ≈ 0.384 (mean of a 0/1 column = proportion)
> df['embarked'].nunique()                      # 3
> df['embarked'].value_counts()                 # S 644, C 168, Q 77
> ```
> The counts sum to 889, not 891: `value_counts()` drops the 2 missing values unless `dropna=False`.

**4.** Add `AgeGroup` = Child (< 18), Adult (18–59), Senior (≥ 60). `.apply()` or `.map()`?

> [!example]- Solution
> Only one column is involved, so apply a function to the `age` Series (`.apply` or `.map`); `df.apply(..., axis=1)` would be slower and unnecessary.
> ```python
> def age_group(age):
>     if pd.isna(age):
>         return 'Unknown'          # check NaN first
>     if age < 18:
>         return 'Child'
>     elif age < 60:
>         return 'Adult'
>     return 'Senior'
> df['AgeGroup'] = df['age'].apply(age_group)
> ```
> `age` has 177 missing values. Without the `pd.isna` check they fail every comparison and land in `'Senior'` with no error. Vectorised alternative:
> ```python
> df['AgeGroup'] = pd.cut(df['age'], bins=[0, 18, 60, 120],
>                         labels=['Child', 'Adult', 'Senior'], right=False)
> ```

**5.** (Advanced) Label passengers `'Priority'` if female **and** 1st class, else `'Standard'`. Then find which numeric column correlates most strongly with `survived` and interpret the sign.

> [!example]- Solution
> Two columns are needed, so use a row-wise apply:
> ```python
> df['Tier'] = df.apply(lambda r: 'Priority' if r['sex'] == 'female' and r['pclass'] == 1
>                       else 'Standard', axis=1)
> df.select_dtypes(include='number').corr()['survived'].sort_values()
> ```
> The strongest is `pclass` at about −0.34. Since 1 = first class and 3 = third, a higher number means lower status, so the negative sign means lower-class passengers survived less. `fare` (≈ +0.26) carries similar information; that redundancy is handled in [[08 - Feature Selection]].

## 📝 Summary

- `Series` = labelled 1-D array, `DataFrame` = table of Series sharing an index, `Index` = immutable, set-like labels.
- `[]` for columns, `.loc` for labels (inclusive slices), `.iloc` for positions (exclusive slices), boolean masks for conditions.
- Arithmetic aligns on the index; non-matching labels give `NaN`; `fill_value` in `.add`/`.sub` controls this.
- `.apply` gets a row/column, `.map` gets one element.
- `describe()` reveals outliers and skew; `value_counts()` reveals category frequencies.
- Most methods return a new object; assign the result or use `inplace=True`.

## ⚠️ Important Notes

1. `df.loc[0:1]` includes label 1; `df.iloc[0:2]` excludes position 2.
2. With an integer index, `df[0:2]` slices rows by position while `df['col']` selects a column; `.loc`/`.iloc` remove the ambiguity.
3. Boolean conditions need parentheses and `&`/`|`, not `and`/`or`.
4. `NaN` fails every comparison, so `if/elif` chains need an explicit `pd.isna()` check.
5. Attribute access (`df.col`) breaks for names with spaces or that clash with methods.
6. Chained assignment `df[df['a'] > 5]['b'] = 0` may change a copy; use `df.loc[df['a'] > 5, 'b'] = 0`.
7. `s1.add(s2, fill_value=0)` is not the same as `(s1 + s2).fillna(0)`.
8. `value_counts()` hides `NaN` unless `dropna=False`.

> [!warning] Gaps in the source slides
> - Slide 9 ("Implicit → Explicit Index") is an image; the idea is reconstructed in the selection section, but the lecturer's example is missing.
> - Slide 18's `.apply()` example (range of each column) is an image.
> - Reference texts (Lesson 0): VanderPlas, *Python Data Science Handbook*; Brownlee, *Data Preparation for Machine Learning*; McKinney, *Python for Data Analysis* (this chapter ≈ McKinney ch. 5); Knaflic, *Storytelling with Data*.

**Next:** [[02 - Loading, Diagnosing, Missing Data and Combining Datasets]]
