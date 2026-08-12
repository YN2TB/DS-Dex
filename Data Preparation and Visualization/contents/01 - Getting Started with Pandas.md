---
subject: Data Preparation and Visualization
chapter: 01
tags: [ds, pandas, data-wrangling, python]
source: "Lesson 1_Getting started with Pandas.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Getting Started with Pandas

> [!note] Where this sits in the course
> This is the first chapter of **Part 1 — Mastering the Tools**. Everything downstream (cleaning, transforming, feature selection, plotting) is expressed in the vocabulary introduced here. See [[00-Index]] for the full roadmap.

## 📘 Main Knowledge

### Why Pandas exists

Pandas is the standard library for **tabular** data in Python. Its value is not that it can do things NumPy cannot — it's that it attaches **labels** to data and keeps those labels correct through every operation. Three properties matter:

- **Flexible** — one table can hold numbers, strings, and dates side by side, unlike a homogeneous NumPy array.
- **Powerful** — complex manipulations (joins, group-bys, reshaping) are single method calls.
- **Fast** — the core is written in C/Cython, so operations run at compiled speed rather than Python-loop speed.

```python
import pandas as pd
```

### The three building blocks

Pandas has exactly three objects you need to understand. Everything else is built from them.

| Object | Dimensions | Think of it as |
|---|---|---|
| `Series` | 1-D | A single labelled column |
| `DataFrame` | 2-D | A table — a collection of `Series` sharing one index |
| `Index` | — | The axis labels themselves |

**Series** — a one-dimensional array of *indexed* data. It is a pairing of `values` (the data) with an `index` (the labels).

```python
# From a list, with an explicit index
s1 = pd.Series([10, 20, 30], index=['a', 'b', 'c'])

# From a dictionary — keys become the index automatically
s2 = pd.Series({'Hanoi': 1000, 'HCMC': 2000})

country_population = pd.Series(
    data=[61, 46, 11, 65, 10],
    index=["IT", "ES", "GR", "FR", "PO"],
    name="Country Population"
)
```

The point of the index is **meaningful access**: `s2['HCMC']` says what it means; `s2[1]` does not. Attributes: `Series.index`, `Series.values`.

**DataFrame** — a two-dimensional table with named columns and an index on the rows. This is the object you will actually spend your career in: every CSV, every SQL table, every Excel sheet becomes a DataFrame when it enters Python.

```python
data = {
    'Province': ['Hanoi', 'HCMC', 'Danang'],
    'Population (millions)': [8.05, 8.99, 1.13]
}
df = pd.DataFrame(data)
```

Attributes: `DataFrame.index`, `DataFrame.columns`, `DataFrame.values`.

**Index** — the labels, as a first-class object. Two things make it distinctive:

1. **It is immutable.** `idx = df.index; idx[0] = 5` raises a `TypeError`. This is a feature: because indexes cannot be mutated, they can be safely *shared* between DataFrames without one object corrupting another.
2. **It behaves like a set.** Indexes support `union`, `intersection`, and friends — which is exactly the machinery that makes automatic alignment (below) and joins possible.

Best practice: give your data a **unique, meaningful index** (`OrderID`, `CustomerID`) rather than leaving the default integer counter.

### Reindexing and dropping

`reindex` conforms an object to a *new* set of labels, inserting `NaN` (or `fill_value`) wherever the new index has no matching data:

```python
s1_reindexed = s1.reindex(['a', 'b', 'c', 'd'], fill_value=0)  # 'd' becomes 0
```

`drop` removes labels along an axis:

```python
df_dropped_row = df.drop(1)                  # drop the row labelled 1
df_dropped_col = df.drop('Province', axis=1) # axis=1 → operate on columns
```

Both return a **new object** and leave the original untouched, unless you pass `inplace=True`.

### Indexing, selection, filtering — the four tools

Pandas offers several ways to do the same selection, which is the single most common source of beginner confusion. Learn the four tools and when each applies.

**1. `[]` — for columns.**

```python
df['Province']                # → Series (single column)
df[['Province', 'Population (millions)']]  # → DataFrame (list of columns)
```

Attribute access (`df.Province`) also works but breaks whenever the column name contains a space, starts with a number, or collides with an existing method (`df.count`). Avoid it outside of quick interactive exploration.

**2. `.loc` — label-based.** Syntax: `df.loc[row_labels, column_labels]`.

```python
df.loc[0]                        # row with index label 0
df.loc[[0, 2]]                   # rows labelled 0 and 2
df.loc[0:1]                      # slice by label — INCLUSIVE of endpoint
df.loc[0, 'Population (millions)']  # a single scalar
df.loc[[0, 2], ['Province']]     # rows × columns
```

**3. `.iloc` — integer-position-based.** Syntax: `df.iloc[row_positions, column_positions]`.

```python
df.iloc[0]        # first row by position
df.iloc[[0, 2]]   # rows at positions 0 and 2
df.iloc[0:2]      # slice by position — EXCLUSIVE of endpoint, like a Python list
df.iloc[0, 1]     # first row, second column
df.iloc[0:2, [0]]
```

**4. Boolean masking — for filtering rows on their values.** Build a `True`/`False` `Series`, then pass it in:

```python
mask = df['Population (millions)'] > 5
df[mask]

# Combine with & (and) / | (or) — parentheses are mandatory
df[(df['Population (millions)'] > 1) & (df['Population (millions)'] < 9)]
```

> [!tip] Rule of thumb
> `[]` for columns, `.loc`/`.iloc` for rows and cells, boolean masks for conditions. Preferring the explicit accessors makes code readable and avoids a whole class of silent bugs.

### Arithmetic and automatic data alignment

When you combine two Pandas objects, Pandas **aligns them on the index first**, then computes. Labels present in one operand but not the other produce `NaN`:

```python
s1 = pd.Series([7.3, -2.5, 3.4], index=['a', 'c', 'd'])
s2 = pd.Series([-2.1, 3.6, -1.5], index=['a', 'c', 'e'])

s1 + s2            # 'a' and 'c' compute; 'd' and 'e' → NaN
s1.add(s2, fill_value=0)   # treat missing labels as 0 instead
```

This is a safety mechanism: it makes it impossible to accidentally add row 5 of one dataset to row 5 of an unrelated dataset. The cost is that `NaN` can appear where you did not expect it — always inspect the result. Handling those `NaN`s is the subject of [[02 - Loading, Diagnosing, Missing Data and Combining Datasets]].

### Function application: `apply` vs `map`

The distinction is **what the function receives**.

- **`.apply()`** operates on a whole row or column (a `Series`) of a DataFrame. Use it when the output depends on *several columns at once* — i.e. for feature engineering.

```python
DataFrame.apply(func, axis=0)   # axis=0 → per column, axis=1 → per row
```

- **`.map()`** operates on **each individual element** of a `Series`. Use it for reformatting or encoding values one at a time.

```python
format_func = lambda x: f'{x:.2f} million people'
df['Population (millions)'].map(format_func)
```

Element-wise recoding via `.map()` is the seed of categorical encoding, developed properly in [[07 - Data Transformation]].

### Sorting and ranking

```python
df.sort_values(by='Population (millions)', ascending=False)
df['Population (millions)'].rank(method='first')
```

Sorting is an exploration tool: best-selling products, highest-spending customers, most effective campaigns are all a `sort_values` away. `rank` assigns each value its position in the ordering rather than reordering the table.

### Descriptive statistics

```python
data_num.sum()          # sum down each column
data_num.mean(axis=1)   # mean across each row
data_num.describe()     # count, mean, std, min, 25%, 50%, 75%, max
```

`.describe()` is the fastest diagnostic you have. Read it for two signals:

- **Outliers** — a `max` far above the `75%` quartile (or `min` far below `25%`) means a long tail.
- **Skewness** — `mean` pulled away from the `50%` median means an asymmetric distribution.

Both signals feed directly into [[06 - Data Cleaning]] and [[07 - Data Transformation]]. The underlying theory lives in [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]].

### Correlation and covariance

```python
data_num['a'].corr(data_num['b'])
data_num.cov()
```

Covariance measures how two variables move together; correlation is covariance normalised to $[-1, 1]$:

$$\operatorname{cov}(X,Y) = \mathbb{E}\big[(X - \mu_X)(Y - \mu_Y)\big] \qquad
\rho_{X,Y} = \frac{\operatorname{cov}(X,Y)}{\sigma_X \, \sigma_Y}$$

Business use: "does advertising spend correlate with revenue?" A high coefficient is a *hint* that a predictive model may work — see [[Machine Learning/contents/00-Index|Machine Learning]]. It is never proof of a causal mechanism. **Correlation does not imply causation.** #probability

### Categorical variables

```python
df['Province'].unique()        # distinct values
df['Province'].value_counts()  # frequency of each value
df['Province'].isin(['Hanoi', 'Can Tho'])  # membership → boolean mask
```

`.value_counts()` is among the most-used functions in practice: it exposes market segments, popular product types, and class imbalance in a target variable. `.isin()` pairs naturally with boolean masking for filtering against a list.

## ✏️ Exercises

**1.** Given `s1 = pd.Series([10, 20, 30], index=['a', 'b', 'c'])`, predict the output of `s1.loc['a':'b']` and `s1.iloc[0:2]`. Do they return the same thing? Explain the difference in the two slicing rules.

> [!example]- Solution
> Both return `a → 10, b → 20`, but **for different reasons**.
> - `.loc['a':'b']` slices by **label** and is **inclusive** of the endpoint `'b'`.
> - `.iloc[0:2]` slices by **position** and is **exclusive** of the endpoint, exactly like a Python list — positions 0 and 1.
>
> They coincide here by coincidence. If you asked for `.loc['a':'c']` you would get all three elements, while `.iloc[0:3]` also gets three — but `.iloc[0:2]` and `.loc['a':'c']` differ. Never assume the two are interchangeable.

**2.** Using the two Series below, compute `s1 + s2`. Which labels produce `NaN`, and why? Then rewrite the operation so that missing labels are treated as zero.
> ```python
> s1 = pd.Series([7.3, -2.5, 3.4], index=['a', 'c', 'd'])
> s2 = pd.Series([-2.1, 3.6, -1.5], index=['a', 'c', 'e'])
> ```

> [!example]- Solution
> Pandas aligns on the index before adding. The union of the indexes is `{a, c, d, e}`:
>
> | label | s1 | s2 | s1 + s2 |
> |---|---|---|---|
> | a | 7.3 | −2.1 | 5.2 |
> | c | −2.5 | 3.6 | 1.1 |
> | d | 3.4 | — | NaN |
> | e | — | −1.5 | NaN |
>
> `d` and `e` are `NaN` because each appears in only one operand — Pandas refuses to guess what the missing counterpart should be.
>
> To treat absences as zero, use the method form with `fill_value`:
> ```python
> s1.add(s2, fill_value=0)   # d → 3.4, e → -1.5
> ```
> Note this is *not* the same as filling the result with 0 afterwards — `fill_value` substitutes before the addition, so `d` keeps its real value 3.4.

**3.** Load the Titanic dataset with `sns.load_dataset('titanic')`. Sort passengers by age descending, compute the overall survival rate, and count the unique values of `embarked`.

> [!example]- Solution
> ```python
> import seaborn as sns
> import pandas as pd
>
> df = sns.load_dataset('titanic')
>
> # Sort by age, oldest first. NaN ages are pushed to the end by default.
> df.sort_values(by='age', ascending=False)
>
> # Survival rate: 'survived' is 0/1, so the mean IS the proportion.
> df['survived'].mean()          # ≈ 0.384
>
> # Unique values and their frequencies
> df['embarked'].nunique()       # 3
> df['embarked'].value_counts()  # S: 644, C: 168, Q: 77
> ```
> Two things worth noticing: taking the `.mean()` of a 0/1 column to get a rate is an idiom you will use constantly, and `value_counts()` **excludes `NaN` by default** — the counts sum to 889, not 891, because `embarked` has 2 missing values. Pass `dropna=False` to see them.

**4.** Add an `AgeGroup` column to the Titanic DataFrame labelling each passenger `'Child'` (< 18), `'Adult'` (18–59), or `'Senior'` (≥ 60). Should you use `.apply()` or `.map()`? Justify the choice.

> [!example]- Solution
> The rule depends on **one column only**, so either works on that column — but the idiomatic choice is `.apply()` on the `age` Series, or `.map()` if you prefer to emphasise element-wise work. What you must *not* do is `.apply(axis=1)` over the whole DataFrame; that is slower and unnecessary when a single column drives the result.
>
> ```python
> def age_group(age):
>     if pd.isna(age):
>         return 'Unknown'      # handle NaN FIRST — comparisons with NaN are always False
>     if age < 18:
>         return 'Child'
>     elif age < 60:
>         return 'Adult'
>     return 'Senior'
>
> df['AgeGroup'] = df['age'].apply(age_group)
> ```
>
> The trap: Titanic's `age` has 177 missing values. Without the `pd.isna` guard, every `NaN` falls through all comparisons (since `NaN < 18` is `False`) and silently lands in the `'Senior'` bucket — a wrong answer that no error message will warn you about.
>
> A vectorised alternative, faster on large data and the tool of choice later in [[07 - Data Transformation]]:
> ```python
> df['AgeGroup'] = pd.cut(df['age'], bins=[0, 18, 60, 120],
>                         labels=['Child', 'Adult', 'Senior'], right=False)
> ```

**5.** (Advanced) For the Titanic data, build a function that classifies each passenger using **two** columns at once — returning `'Priority'` if the passenger is female **and** in 1st class, `'Standard'` otherwise. Then compute the correlation matrix of the numeric columns and identify which variable correlates most strongly with `survived`. Interpret the sign.

> [!example]- Solution
> Because the rule reads two columns, this genuinely requires `.apply(axis=1)` — each call receives a whole row:
>
> ```python
> def priority(row):
>     if row['sex'] == 'female' and row['pclass'] == 1:
>         return 'Priority'
>     return 'Standard'
>
> df['Tier'] = df.apply(priority, axis=1)   # axis=1 → row-wise
> ```
>
> For the correlation matrix, restrict to numeric columns first:
> ```python
> df.select_dtypes(include='number').corr()['survived'].sort_values()
> ```
> The strongest relationship is `pclass` at roughly **−0.34**. The sign is the interesting part: `pclass` is coded 1 = first class, 3 = third class, so *higher number = lower status*. A **negative** correlation therefore means lower-status passengers survived less often — the coefficient is negative while the real-world effect is "wealth helped."
>
> This is the classic reason to inspect what the encoding *means* before interpreting a coefficient. Also note `fare` (≈ +0.26) carries much of the same information as `pclass`; that redundancy is what [[08 - Feature Selection]] deals with.

## 📝 Summary

- **`Series` = 1-D labelled array, `DataFrame` = 2-D table, `Index` = the labels.** A DataFrame is just Series sharing one index.
- **`Index` objects are immutable** so they can be shared safely between objects, and support set operations — which is what makes alignment and joins possible.
- **Four selection tools, four jobs:** `[]` for columns, `.loc` for labels, `.iloc` for positions, boolean masks for conditions.
- **`.loc` slices are inclusive of the endpoint; `.iloc` slices are exclusive.** This is the most common indexing bug in Pandas.
- **Arithmetic aligns on the index automatically**, producing `NaN` for non-matching labels; `fill_value` in the method form (`.add`, `.sub`, …) controls this.
- **`.apply()` takes a whole row/column, `.map()` takes one element.** Multi-column logic needs `.apply(axis=1)`.
- **`.describe()` is the fastest diagnostic** for outliers (max ≫ 75%) and skew (mean ≠ median); `.value_counts()` is the equivalent for categorical variables.
- **Most Pandas methods return a new object** — nothing changes in place unless you assign the result or pass `inplace=True`.

## ⚠️ Important Notes

**The `.loc` / `.iloc` slicing asymmetry.** `df.loc[0:1]` returns **two** rows (labels 0 and 1); `df.iloc[0:2]` returns **two** rows (positions 0 and 1). Label slicing includes the endpoint because a label has no "next" value to stop before; positional slicing follows Python's half-open convention. Expect this on an exam.

**Integer labels make `[]` genuinely ambiguous.** If your index is `[0, 1, 2]`, then `df[0:2]` slices *rows by position*, but `df['col']` selects a *column*. The `[]` operator guesses based on what you give it. This is precisely why the slides insist on `.loc`/`.iloc` — they never guess.

**Parentheses in boolean masks are not optional.** `df[df['a'] > 1 & df['a'] < 9]` fails, because `&` binds tighter than `>` in Python. You must write `df[(df['a'] > 1) & (df['a'] < 9)]`. Likewise use `&`/`|`, never the keywords `and`/`or`, which cannot operate element-wise on a Series.

**`NaN` fails every comparison.** `NaN < 18`, `NaN > 18`, and `NaN == NaN` are all `False`. Any `if/elif` chain without an explicit `pd.isna()` guard will silently dump missing values into the final `else` branch. This is the single most dangerous trap in Exercise 4 and it produces no error.

**Attribute access degrades quietly.** `df.Province` works until someone renames the column to `Province Name`, or until you try `df.count` and get the *method* instead of your column. Use `df['Province']`.

**Chained assignment does not reliably write.** `df[df['a'] > 5]['b'] = 0` may modify a temporary copy and leave `df` untouched (`SettingWithCopyWarning`). Write `df.loc[df['a'] > 5, 'b'] = 0` — a single `.loc` call — instead.

**`fill_value` ≠ filling afterwards.** `s1.add(s2, fill_value=0)` substitutes 0 for *absent labels before* adding, preserving the present operand's real value. `(s1 + s2).fillna(0)` destroys that value by overwriting the `NaN` with 0. In Exercise 2 the two approaches give `d = 3.4` and `d = 0` respectively.

**`value_counts()` drops `NaN` by default.** When auditing data quality this hides exactly what you are looking for. Use `value_counts(dropna=False)`.

> [!warning] Gaps in the source slides
> Two slides in Lesson 1 contain only images, so their content is not captured above:
> - **Slide 9 — "Implicit → Explicit Index"** (the distinction between the automatic integer position and a user-assigned label, which is what motivates `.loc` vs `.iloc`). The idea is reconstructed from context in the selection section above, but the lecturer's specific worked example is missing.
> - **Slide 18** — the `.apply()` example computing "the range of each column" is described in the caption but the code itself is an image.
>
> Ask the lecturer or check *Python for Data Analysis* (McKinney), Ch. 5, if the exam emphasises these.

> [!note] Course reference texts
> Cited in Lesson 0: VanderPlas, *Python Data Science Handbook* (2e) · Brownlee, *Data Preparation for Machine Learning* · McKinney, *Python for Data Analysis* (3e) · Knaflic, *Storytelling with Data*. This chapter maps to McKinney Ch. 5.

---
**Next:** [[02 - Loading, Diagnosing, Missing Data and Combining Datasets]]
