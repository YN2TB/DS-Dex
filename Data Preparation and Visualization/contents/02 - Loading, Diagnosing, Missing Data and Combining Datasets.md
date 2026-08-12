---
subject: Data Preparation and Visualization
chapter: 02
tags: [ds, pandas, data-wrangling, missing-data, data-quality]
source: "Lesson 2_Handling Missing and Combinning.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Loading, Diagnosing, Handling Missing Data, and Combining Datasets

> [!note] Where this sits in the course
> Still **Part 1 — Mastering the Tools**. [[01 - Getting Started with Pandas]] gave you the objects; this chapter covers getting real data *in*, checking it is what it claims to be, and stitching multiple sources together. This is the chapter that solves the course's motivating problem: three files (`transactions.csv`, `user_logs.xlsx`, `support_tickets.json`) that must become one table.

## 📘 Main Knowledge

### 1. Loading data

**From files.** `read_csv` is the workhorse. The parameters matter more than beginners expect:

```python
df_csv = pd.read_csv('data.csv',
                     sep=',',                          # field separator
                     header=0,                         # which row holds column names
                     index_col='id',                   # promote a column to the index
                     na_values=['Not Available', '--'])  # extra strings meaning "missing"

df_excel = pd.read_excel('data.xlsx', sheet_name='Sheet1')
```

- `sep` — change it for TSV (`\t`) or European CSVs (`;`).
- `header` — set `header=None` when the file has no header row, else the first data row is silently eaten.
- `index_col` — setting a meaningful index at load time speeds up later access.
- **`na_values` is the one people forget.** Pandas recognises `NaN`, `NA`, `null` and friends automatically, but not domain-specific sentinels. If your source writes `'Not Available'`, `'--'`, or `-999`, you must declare them here — otherwise the whole column loads as `object` and every numeric operation breaks.

Pandas reads a URL exactly like a local path:

```python
url = 'https://example.com/data.csv'
df = pd.read_csv(url)
```

**From web APIs.** Many providers expose data programmatically; wrapper libraries turn that into one call. The course uses `yfinance` for finance data:

```python
# !pip install yfinance
import yfinance as yf
data = yf.download('AAPL', start='2023-01-01', end='2023-12-31')
data.head()
```

**First two commands after any load, always:** `df.head()` to see the shape of the thing, `df.info()` to see what Pandas *thinks* it is.

### 2. Diagnosing data types

`.info()` reports the index dtype, each column's dtype, the non-null count, and memory usage. Learn to read the dtypes:

| Dtype | Meaning |
|---|---|
| `object` | Text — **or a column with mixed types**. The suspicious one. |
| `int64` | Integers |
| `float64` | Decimals |
| `bool` | True/False |
| `datetime64` | Dates and times |

The business consequence of a wrong dtype is concrete: if `TotalAmount` loaded as `object`, `.sum()` and `.mean()` fail or silently concatenate strings. If `OrderDate` is an `object`, you cannot filter by month or year. **A single bad cell — one `'N/A'` in a column of numbers — is enough to demote the entire column to `object`.** That is why `na_values` at load time matters so much.

**Correcting types** with `.astype()` and `pd.to_datetime()`:

```python
df['order_id'] = df['order_id'].astype(int)
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
```

Always pass `format` when you know it. Without it Pandas infers the format by inspecting values, which is slow on large data and — worse — can guess wrong on ambiguous dates. `03/04/2023` is 3 April or 4 March depending on the convention, and Pandas cannot know which.

### 3. Handling missing data

**How missingness hides.** A missing value is not always `NaN`. Real datasets encode it as:

- `NaN` (Not a Number) — the float sentinel Pandas uses natively
- `NULL` / `None` — Python's object-level null
- **Empty strings** `''` — which Pandas treats as a *valid string*, not missing
- **Special indicators** — `-999`, `9999`, `0`, `'Unknown'`
- **Blanks or spaces** `' '` — also a valid string as far as Pandas is concerned

Only the first two are detected automatically. Everything else must be converted deliberately, or `.isnull()` will cheerfully report zero missing values in a column that is half empty.

**Detecting.**

```python
df.isnull()             # elementwise boolean mask
df.isnull().sum()       # count per column — the practical form
df.isnull().mean()      # proportion per column
```

**Handling — two families of strategy:**

**Dropping.**
```python
df.dropna(axis=0, how='any', thresh=None)
df.drop_duplicates()
```
- `axis=0` drops rows, `axis=1` drops columns.
- `how='any'` (default) drops if *any* value is missing; `how='all'` only if *all* are.
- `thresh=n` keeps rows having at least `n` non-null values — the more surgical option.

**Filling (imputation).**
```python
df.fillna(value=None, method=None, axis=None, inplace=False)
```
- `value` accepts a scalar, a **dict** (`{'Age': 0, 'City': 'Unknown'}` — different fill per column), or a computed statistic such as `df['Age'].mean()` / `.median()`.
- `method='ffill'` propagates the last valid observation **forward**; `method='bfill'` pulls the next valid observation **backward**. These are designed for ordered data — see [[05 - String Manipulation and Time Series Data]].
- **Filling by base model** — predicting the missing value from other columns (regression, k-NN) rather than substituting a constant. Sophisticated, but it invites leakage; see the warning below.

> [!warning] Imputation is a modelling decision, not a cleanup chore
> Every strategy injects an assumption. Dropping rows assumes the missingness is random — if it is not (customers who churned skipped the survey), you have just deleted your signal and biased the sample. Mean-filling preserves the mean but **shrinks the variance** and weakens correlations. There is no neutral choice; there is only a choice you can defend.

**Practice data from the slides:**
```python
data = {'Name': ['John', 'Anna', 'Peter', 'Linda', 'James'],
        'Age': [28, 22, np.nan, 32, 25],
        'City': ['New York', 'Paris', 'Berlin', np.nan, 'London'],
        'Salary': [70000, np.nan, 60000, 85000, np.nan]}
df = pd.DataFrame(data)
```

### 4. Combining datasets — `concat`

`pd.concat` **stacks** objects along an axis. It is the "add more of the same" tool.

```python
pd.concat(objs, axis=0, join='outer', ignore_index=False, keys=None,
          verify_integrity=False)
```

- `objs` — a sequence of Series/DataFrames, e.g. `[df1, df2]`
- `axis=0` stacks rows (default); `axis=1` stacks columns side by side
- `join='outer'` (default) keeps the **union** of columns, filling gaps with `NaN`; `'inner'` keeps only the **intersection**
- `ignore_index=True` discards the original indexes and renumbers 0..n−1
- `keys=['a', 'b']` adds an outer MultiIndex level recording which source each row came from — see [[03 - Data Aggregation and Group Operations]]
- `verify_integrity=True` raises if the result has duplicate index labels

```python
df1 = pd.DataFrame([['a', 1], ['b', 2]], columns=['letter', 'number'])
df2 = pd.DataFrame([['c', 3, 'cat'], ['d', 4, 'dog']],
                   columns=['letter', 'number', 'animal'])
pd.concat([df1, df2])   # outer join → 'animal' is NaN for df1's rows
```

The old `df1.append(df2)` is shorthand for `pd.concat([df1, df2], ignore_index=True)`. **`.append()` was removed in Pandas 2.0** — use `pd.concat`.

### 5. Combining datasets — `merge`

`pd.merge` implements **SQL-style joins**: match rows across tables on shared key values. This is "combine different information about the same entities."

```python
pd.merge(left, right, how='inner', on=None,
         left_on=None, right_on=None,
         left_index=False, right_index=False)
```

- `on` — the shared key column name; `left_on`/`right_on` when the two tables name it differently
- `how` — `'inner'` (default, keys in both), `'outer'` (keys in either), `'left'` (all of left), `'right'` (all of right)

**The three cardinalities:**

| Type | Meaning | Result size |
|---|---|---|
| **one-to-one** | Key unique in both tables | Same row count |
| **many-to-one** | Key unique in one table only | Row count of the "many" side |
| **many-to-many** | Key repeats in both | **Cartesian product within each key — rows multiply** |

Many-to-many is where silent disasters live. If a key appears 3 times on the left and 4 times on the right, that key alone yields 12 rows. A table that was supposed to grow slightly instead explodes, and every aggregate computed afterwards is wrong. Check `len(df)` before and after every merge.

> [!tip] `concat` vs `merge` in one line
> **`concat` = more rows (or blind side-by-side columns), aligned on the index.** **`merge` = more columns, aligned on matching key *values*.**

## ✏️ Exercises

**1.** A CSV column `Revenue` contains the values `1000`, `2500`, `Not Available`, `3000`. You load it with a plain `pd.read_csv` and `df['Revenue'].mean()` raises an error. Diagnose the cause and give two fixes.

> [!example]- Solution
> `.info()` will show `Revenue` as **`object`**, not `int64`. Pandas does not recognise `'Not Available'` as missing, so the column contains a mix of integers and a string — and the only dtype able to hold both is `object`. Arithmetic on it fails.
>
> **Fix 1 — declare it at load time (preferred):**
> ```python
> df = pd.read_csv('data.csv', na_values=['Not Available'])
> ```
> The string becomes `NaN`, the column loads as `float64`, and `.mean()` works (skipping `NaN` by default).
>
> **Fix 2 — repair after the fact:**
> ```python
> df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
> ```
> `errors='coerce'` turns anything unparseable into `NaN`. Note `.astype(int)` would **not** work here — it raises on the string, and even after coercion a column containing `NaN` cannot be `int64` (`NaN` is a float).
>
> Fix 1 is better because it catches every occurrence, including sentinels in columns you have not inspected yet.

**2.** Using the practice DataFrame below, count the missing values per column, then fill `Age` with its median and `City` with `'Unknown'` in a single `fillna` call.
> ```python
> data = {'Name': ['John', 'Anna', 'Peter', 'Linda', 'James'],
>         'Age': [28, 22, np.nan, 32, 25],
>         'City': ['New York', 'Paris', 'Berlin', np.nan, 'London'],
>         'Salary': [70000, np.nan, 60000, 85000, np.nan]}
> ```

> [!example]- Solution
> ```python
> df.isnull().sum()
> # Name 0, Age 1, City 1, Salary 2
> ```
> A dict passed to `fillna` maps column → fill value, so one call handles both:
> ```python
> df.fillna({'Age': df['Age'].median(), 'City': 'Unknown'}, inplace=True)
> ```
> `Age` median is 26.5 (of 22, 25, 28, 32). Note `Salary` is deliberately left alone — it is 40% missing, and imputing that much of a column is rarely defensible. Dropping the column or flagging it for the stakeholder beats inventing 2 of 5 salaries.
>
> Median rather than mean is the safer default for money and age: it does not chase outliers.

**3.** Explain why `pd.concat([df1, df2])` produces a DataFrame with duplicate index labels, and give two different ways to avoid it.
> ```python
> df1 = pd.DataFrame([['a', 1], ['b', 2]], columns=['letter', 'number'])
> df2 = pd.DataFrame([['c', 3, 'cat'], ['d', 4, 'dog']], columns=['letter', 'number', 'animal'])
> ```

> [!example]- Solution
> Both frames carry the default index `[0, 1]`. `concat` **preserves** original indexes rather than renumbering, so the result is indexed `[0, 1, 0, 1]`. Now `result.loc[0]` returns **two rows**, and any downstream `.loc` lookup or join is ambiguous.
>
> **Option A — renumber:**
> ```python
> pd.concat([df1, df2], ignore_index=True)   # index becomes 0,1,2,3
> ```
> **Option B — keep provenance with a MultiIndex:**
> ```python
> pd.concat([df1, df2], keys=['first', 'second'])
> ```
> Now the index is `('first', 0), ('first', 1), ('second', 0), ('second', 1)` — unique *and* it records which source each row came from, which is valuable when combining monthly files or per-region exports.
>
> Also note `animal` is `NaN` for `df1`'s rows: the default `join='outer'` keeps the union of columns. `join='inner'` would drop `animal` entirely.
>
> To catch this class of bug automatically, pass `verify_integrity=True` and let it raise.

**4.** You merge a `customers` table (1,000 unique `customer_id`s) with an `orders` table (5,000 rows, each with a `customer_id`). Before merging you expect 5,000 rows out. You get 5,000. You then merge that result with a `promotions` table on `customer_id` and get 47,000 rows. What happened, and how do you diagnose it?

> [!example]- Solution
> The first merge was **many-to-one**: `customer_id` is unique in `customers`, so each order matched exactly one customer. 5,000 in, 5,000 out.
>
> The second is **many-to-many**: `customer_id` repeats in the orders result *and* repeats in `promotions` (a customer can receive several promotions). For each customer, Pandas produces the Cartesian product — $n_{\text{orders}} \times n_{\text{promotions}}$ rows. Every order is now duplicated once per promotion, so any `sum()` of revenue afterwards is inflated by roughly a factor of 9.
>
> **Diagnose before merging**, not after:
> ```python
> promotions['customer_id'].duplicated().any()   # True → not a unique key
> promotions['customer_id'].value_counts().head()
> ```
> **Let Pandas enforce your assumption:**
> ```python
> pd.merge(orders, promotions, on='customer_id', validate='many_to_one')
> ```
> `validate` raises immediately if the relationship is not what you claimed — far better than discovering it in a revenue figure. If the many-to-many really is intended, you usually want to aggregate `promotions` down to one row per customer first (e.g. `promo_count`), then do a clean many-to-one merge.

**5.** (Advanced) Using the three CDC/US-states files, rank states and territories by 2010 population density.
> ```python
> pop    = pd.read_csv('https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-population.csv')
> areas  = pd.read_csv('https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-areas.csv')
> abbrevs = pd.read_csv('https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-abbrevs.csv')
> ```

> [!example]- Solution
> The interesting part is not the arithmetic — it is that **the merge keys disagree across files**. `pop` uses abbreviations (`state/region`), while `areas` uses full names (`state`). `abbrevs` is the bridge table.
>
> ```python
> # Step 1: attach full names to the population data
> merged = pd.merge(pop, abbrevs, how='outer',
>                   left_on='state/region', right_on='abbreviation')
> merged = merged.drop('abbreviation', axis=1)   # now redundant
>
> # Step 2: audit the outer join for unmatched keys — do NOT skip this
> merged[merged.isnull().any(axis=1)]
> merged.loc[merged['state'].isnull(), 'state/region'].unique()
> # → array(['PR', 'USA'])  — Puerto Rico and the national total have no entry in abbrevs
>
> # Step 3: repair the known gaps by hand
> merged.loc[merged['state/region'] == 'PR', 'state'] = 'Puerto Rico'
> merged.loc[merged['state/region'] == 'USA', 'state'] = 'United States'
>
> # Step 4: bring in areas, then audit again
> final = pd.merge(merged, areas, on='state', how='left')
> final.loc[final['area (sq. mi)'].isnull(), 'state'].unique()
> # → 'United States' has no area entry; drop the aggregate row
> final.dropna(inplace=True)
>
> # Step 5: filter to the 2010 total population, then compute density
> data2010 = final.query("year == 2010 & ages == 'total'").set_index('state')
> density = data2010['population'] / data2010['area (sq. mi)']
> density.sort_values(ascending=False).head()
> ```
> Top result is the **District of Columbia** at ~8,900 people/sq mi — an order of magnitude above any state, because it is a city being compared against states. Puerto Rico is second.
>
> The lesson this exercise exists to teach: **an outer join is a diagnostic tool.** Using `how='outer'` and then inspecting the `NaN` rows is how you *discover* that `PR` and `USA` exist. Had you used `how='inner'`, those rows would have vanished silently and you would never have known your data was incomplete. Join outer, inspect, repair, then narrow.

## 📝 Summary

- **`read_csv`'s parameters do the real work** — `na_values` in particular, because undeclared sentinels (`'--'`, `-999`) demote a whole numeric column to `object`.
- **`.info()` is the first diagnostic after every load.** `object` where you expected a number means the column is contaminated.
- **Fix types explicitly** with `.astype()` and `pd.to_datetime(..., format=...)`; always pass the format to avoid slow, ambiguous inference.
- **Missing ≠ `NaN`.** Empty strings, blanks, and sentinel numbers read as *valid data*; convert them yourself or `.isnull()` will lie to you.
- **Dropping vs filling is a modelling choice.** `dropna` assumes missingness is random; mean-filling shrinks variance. Neither is neutral.
- **`ffill`/`bfill` assume meaningful row order** — they belong to time series, not arbitrary tables.
- **`concat` stacks (more rows), `merge` joins on key values (more columns).**
- **Many-to-many merges multiply rows.** Check row counts before and after, or pass `validate=` and let Pandas raise.

## ⚠️ Important Notes

**One bad string poisons an entire column.** A single `'N/A'` among 100,000 numbers gives you `dtype: object` and breaks `.mean()`, `.sum()`, and every comparison. This is the number one cause of "why doesn't my arithmetic work" in real data.

**`.astype(int)` fails on any column containing `NaN`.** `NaN` is a float by definition, so `int64` cannot hold it. Either fill first, or use the nullable integer dtype: `.astype('Int64')` (capital I).

**Empty strings are not missing values.** `''` and `' '` pass `.isnull()` as `False`. Convert deliberately: `df.replace(r'^\s*$', np.nan, regex=True)`.

**`fillna(df.mean())` distorts your distribution.** It preserves the mean but reduces variance and attenuates correlations toward zero — so a model trained afterwards *understates* the relationships you are trying to find. Report how much you imputed.

**Model-based imputation can leak.** Fitting an imputer on the full dataset and *then* splitting into train/test lets test-set information influence training values. The imputer must be fitted on the training set only — this is exactly what Lesson 0's "Avoiding Data Leakage" principle is about, and why imputation belongs inside a Pipeline. See [[09 - Building Pipelines]].

**`.append()` no longer exists.** Removed in Pandas 2.0. `pd.concat([df1, df2], ignore_index=True)`.

**`concat(axis=1)` aligns on the index, not on position.** If two frames have different indexes you get a sparse mess of `NaN`s rather than a neat side-by-side table. Reset or align the indexes first.

**Default `merge` is `'inner'` — it silently deletes unmatched rows.** SQL users expect this; spreadsheet users are shocked. Merge with `how='outer'` while exploring so you can *see* what fails to match, then narrow once you understand the gaps. Exercise 5 turns on exactly this point.

**`pd.to_datetime` without `format` can guess wrong.** `03/04/2023` is ambiguous. Pandas may also infer the format from the first row and apply it to all — silently mangling the rest. Pass `format=` explicitly, or `dayfirst=True` where appropriate.

> [!warning] Gaps in the source slides
> Several Lesson 2 slides are diagrams with no extractable text:
> - **Slide 11** — the detect/handle decision flowchart (`isnull` → dropping/filling).
> - **Slide 15** — worked `concat` output for `ignore_index` and MultiIndex `keys`.
> - **Slide 17** — a practice exercise whose content is an image.
> - **Slides 18–19** — the visual illustrations of one-to-one, many-to-one, and many-to-many joins. The definitions above come from the slide text; the lecturer's specific worked examples are not recoverable.
>
> **Slide 9's mini-exercise** references `OnlineRetail.xlsx` via a hyperlink ("download or API from: link") — the URL is not in the extractable text, so that dataset is not available to me.
>
> For the join illustrations, VanderPlas *Python Data Science Handbook* Ch. 3 ("Combining Datasets: Merge and Join") is the source these slides are adapted from.

---
**Previous:** [[01 - Getting Started with Pandas]] · **Next:** [[03 - Data Aggregation and Group Operations]]
