---
subject: Data Preparation and Visualization
chapter: 02
tags: [ds, pandas, data-wrangling, missing-data, data-quality]
source: "Lesson 2_Handling Missing and Combinning.pdf — Dr. Nguyen Tuan Long, NEU"
---

# Loading, Diagnosing, Handling Missing Data, and Combining Datasets

Part 1 (Mastering the Tools), continued. This chapter covers loading data, checking its types, handling missing values, and combining sources: the course's motivating problem of turning `transactions.csv`, `user_logs.xlsx` and `support_tickets.json` into one table.

## 📘 Main Knowledge

### 1. Loading data

```python
df_csv = pd.read_csv('data.csv',
                     sep=',',                            # field separator
                     header=0,                           # row with column names
                     index_col='id',                     # use a column as the index
                     na_values=['Not Available', '--'])  # extra strings meaning "missing"
df_excel = pd.read_excel('data.xlsx', sheet_name='Sheet1')
```

- `sep`: `\t` for TSV, `;` for many European CSVs.
- `header=None` if the file has no header row; otherwise the first data row becomes the column names.
- `index_col`: set a meaningful index at load time.
- `na_values`: Pandas recognises `NaN`, `NA`, `null` etc., but not domain sentinels like `'Not Available'`, `'--'` or `-999`. Undeclared, they make the column load as `object`.

A URL works like a local path: `pd.read_csv('https://example.com/data.csv')`.

**Web APIs** via wrapper libraries, e.g. `yfinance`:
```python
import yfinance as yf
data = yf.download('AAPL', start='2023-01-01', end='2023-12-31')
```

After every load: `df.head()` and `df.info()`.

### 2. Diagnosing data types

`.info()` shows each column's dtype, non-null count and memory use.

| Dtype | Meaning |
|---|---|
| `object` | text, or a column with mixed types (suspicious) |
| `int64` | integers |
| `float64` | decimals |
| `bool` | True/False |
| `datetime64` | dates and times |

If `TotalAmount` is `object`, `.sum()` and `.mean()` fail or concatenate strings; if `OrderDate` is `object`, you cannot filter by month. One `'N/A'` among numbers is enough to make the whole column `object`.

```python
df['order_id'] = df['order_id'].astype(int)
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
```

Pass `format` when you know it: inference is slow on large data and can misread ambiguous dates (`03/04/2023` is 3 April or 4 March).

### 3. Missing data

Missing values appear as:
- `NaN` (float sentinel) and `None`/`NULL`: detected automatically;
- empty strings `''` and blanks `' '`: treated as valid strings;
- sentinel values `-999`, `9999`, `0`, `'Unknown'`: treated as valid data.

Only the first kind is detected by `isnull()`; convert the rest yourself.

```python
df.isnull().sum()       # count per column
df.isnull().mean()      # share per column
```

**Dropping**
```python
df.dropna(axis=0, how='any', thresh=None)
df.drop_duplicates()
```
`axis=0` rows, `axis=1` columns; `how='any'` (default) or `'all'`; `thresh=n` keeps rows with at least `n` non-null values.

**Filling (imputation)**
```python
df.fillna(value=None, method=None)
```
- `value`: a scalar, a dict per column (`{'Age': 0, 'City': 'Unknown'}`), or a statistic (`df['Age'].median()`).
- `method='ffill'` / `'bfill'`: carry the previous/next valid value; meant for ordered data ([[05 - String Manipulation and Time Series Data]]).
- Model-based: predict missing values from other columns (regression, k-NN); powerful but can leak (see notes).

> [!warning] Imputation is a modelling decision
> Dropping rows assumes values are missing at random; if not (customers who churned skipped the survey), you remove the signal and bias the sample. Mean filling keeps the mean but shrinks the variance and weakens correlations.

Practice data from the slides:
```python
data = {'Name': ['John', 'Anna', 'Peter', 'Linda', 'James'],
        'Age': [28, 22, np.nan, 32, 25],
        'City': ['New York', 'Paris', 'Berlin', np.nan, 'London'],
        'Salary': [70000, np.nan, 60000, 85000, np.nan]}
df = pd.DataFrame(data)
```

### 4. `concat`: stacking

```python
pd.concat(objs, axis=0, join='outer', ignore_index=False, keys=None, verify_integrity=False)
```

- `axis=0` stacks rows (default), `axis=1` places frames side by side.
- `join='outer'` keeps the union of columns (gaps become `NaN`); `'inner'` keeps the intersection.
- `ignore_index=True` renumbers 0…n−1.
- `keys=['a', 'b']` adds an outer index level recording the source ([[03 - Data Aggregation and Group Operations]]).
- `verify_integrity=True` raises on duplicate index labels.

```python
df1 = pd.DataFrame([['a', 1], ['b', 2]], columns=['letter', 'number'])
df2 = pd.DataFrame([['c', 3, 'cat'], ['d', 4, 'dog']], columns=['letter', 'number', 'animal'])
pd.concat([df1, df2])     # 'animal' is NaN for df1's rows
```

`df1.append(df2)` was removed in Pandas 2.0; use `pd.concat([df1, df2], ignore_index=True)`.

### 5. `merge`: SQL-style joins

```python
pd.merge(left, right, how='inner', on=None, left_on=None, right_on=None,
         left_index=False, right_index=False)
```

- `on`: shared key; `left_on`/`right_on` if the names differ.
- `how`: `'inner'` (default, keys in both), `'outer'`, `'left'`, `'right'`.

| Relationship | Meaning | Result rows |
|---|---|---|
| one-to-one | key unique in both | same count |
| many-to-one | key unique in one table | count of the "many" side |
| many-to-many | key repeats in both | product of counts per key |

A key appearing 3 times on the left and 4 on the right gives 12 rows. Check `len(df)` before and after each merge.

`concat` adds rows (or side-by-side columns aligned on the index); `merge` adds columns matched on key values.

## ✏️ Exercises

**1.** A column `Revenue` has values `1000`, `2500`, `Not Available`, `3000`. After a plain `read_csv`, `df['Revenue'].mean()` fails. Why, and how do you fix it?

> [!example]- Solution
> `.info()` shows `Revenue` as `object`: the string `'Not Available'` is not recognised as missing, so the column mixes numbers and text.
>
> Fix 1 (preferred): `pd.read_csv('data.csv', na_values=['Not Available'])`; the column loads as `float64` and `.mean()` skips the `NaN`.
>
> Fix 2: `df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')`. `.astype(int)` would not work: it raises on the string, and a column with `NaN` cannot be `int64`.

**2.** For the practice DataFrame, count missing values per column, then fill `Age` with its median and `City` with `'Unknown'` in one call.

> [!example]- Solution
> ```python
> df.isnull().sum()     # Name 0, Age 1, City 1, Salary 2
> df.fillna({'Age': df['Age'].median(), 'City': 'Unknown'}, inplace=True)
> ```
> The median of 22, 25, 28, 32 is 26.5. `Salary` is 40% missing; imputing 2 of 5 values is hard to justify, so flag or drop it instead. The median is a safer default than the mean for money and age because it ignores outliers.

**3.** Why does `pd.concat([df1, df2])` (frames from §4) produce duplicate index labels? Give two fixes.

> [!example]- Solution
> Both frames have index `[0, 1]` and `concat` keeps the original labels, giving `[0, 1, 0, 1]`; `result.loc[0]` returns two rows.
> - `pd.concat([df1, df2], ignore_index=True)` → index 0–3.
> - `pd.concat([df1, df2], keys=['first', 'second'])` → unique MultiIndex that also records the source.
>
> `animal` is `NaN` for df1's rows because of `join='outer'`. `verify_integrity=True` would raise on the duplicates.

**4.** `customers` (1,000 unique IDs) merged with `orders` (5,000 rows) gives 5,000 rows. Merging that with `promotions` on `customer_id` gives 47,000 rows. What happened?

> [!example]- Solution
> The first merge was many-to-one (IDs unique in `customers`). The second is many-to-many: IDs repeat in both, so each customer's orders are multiplied by their promotions, and revenue sums are inflated about 9×.
>
> Diagnose before merging: `promotions['customer_id'].duplicated().any()`. Enforce your assumption: `pd.merge(orders, promotions, on='customer_id', validate='many_to_one')` raises if it is wrong. Usually aggregate promotions to one row per customer first (e.g. `promo_count`), then merge.

**5.** (Advanced) Rank US states and territories by 2010 population density using the three files:
> ```python
> pop    = pd.read_csv('https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-population.csv')
> areas  = pd.read_csv('https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-areas.csv')
> abbrevs = pd.read_csv('https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-abbrevs.csv')
> ```

> [!example]- Solution
> The keys differ: `pop` uses abbreviations (`state/region`), `areas` full names (`state`); `abbrevs` links them.
> ```python
> merged = pd.merge(pop, abbrevs, how='outer', left_on='state/region', right_on='abbreviation')
> merged = merged.drop('abbreviation', axis=1)
> merged.loc[merged['state'].isnull(), 'state/region'].unique()    # ['PR', 'USA']
> merged.loc[merged['state/region'] == 'PR', 'state'] = 'Puerto Rico'
> merged.loc[merged['state/region'] == 'USA', 'state'] = 'United States'
> final = pd.merge(merged, areas, on='state', how='left')
> final.loc[final['area (sq. mi)'].isnull(), 'state'].unique()    # 'United States'
> final.dropna(inplace=True)
> data2010 = final.query("year == 2010 & ages == 'total'").set_index('state')
> density = data2010['population'] / data2010['area (sq. mi)']
> density.sort_values(ascending=False).head()
> ```
> The District of Columbia is first (~8,900 people per sq mi; a city compared with states), Puerto Rico second. The outer join is what reveals `PR` and `USA`; an inner join would have dropped them silently. Join outer, inspect, repair, then narrow.

## 📝 Summary

- `read_csv` parameters matter, especially `na_values`; undeclared sentinels turn numeric columns into `object`.
- Run `.info()` after every load; fix types with `.astype()` and `pd.to_datetime(..., format=...)`.
- Empty strings, blanks and sentinel numbers are not detected as missing.
- Dropping vs filling is a modelling choice; `ffill`/`bfill` assume ordered rows.
- `concat` stacks; `merge` joins on keys; many-to-many merges multiply rows (use `validate=`).

## ⚠️ Important Notes

1. One bad string makes a whole column `object`.
2. `.astype(int)` fails on columns with `NaN`; fill first or use the nullable `'Int64'` dtype.
3. Convert blanks: `df.replace(r'^\s*$', np.nan, regex=True)`.
4. Mean imputation reduces variance and weakens correlations; report how much was imputed.
5. Fit imputers on the training set only (inside a pipeline, [[09 - Building Pipelines]]) to avoid leakage.
6. `.append()` no longer exists in Pandas 2.0.
7. `concat(axis=1)` aligns on the index, not position.
8. `merge` defaults to inner and silently drops unmatched rows; explore with `how='outer'`.
9. `pd.to_datetime` without `format` may guess wrong; use `format=` or `dayfirst=True`.

> [!warning] Gaps in the source slides
> - Slide 11 (detect/handle flowchart), slide 15 (concat output), slide 17 (practice exercise) and slides 18–19 (join illustrations) are images.
> - Slide 9's exercise links to `OnlineRetail.xlsx`, which is not available.
> - The join material follows VanderPlas, *Python Data Science Handbook*, ch. 3.

**Previous:** [[01 - Getting Started with Pandas]] · **Next:** [[03 - Data Aggregation and Group Operations]]
