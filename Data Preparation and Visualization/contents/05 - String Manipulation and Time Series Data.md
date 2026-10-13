---
subject: Data Preparation and Visualization
chapter: 05
tags: [ds, pandas, regex, time-series, feature-engineering, text-processing]
source: "Lesson 5 String Manipulation and Time Series Data.pdf — Dr. Nguyen Tuan Long, NEU"
---

# String Manipulation and Time Series Data

Bridge from Part 1 (tools) to Part 2 (data architecture): turning text and date columns into model-ready features. (Lesson 4 is missing from the source; the sequence jumps from 3 to 5. See [[00-Index]].)

## 📘 Main Knowledge

### Business context

- **Text**: a `Description` column like `'WHITE HANGING HEART T-LIGHT HOLDER'`. Extract `'WHITE'` and `'HEART'` to categorize products; reconcile different spellings of one product.
- **Time**: an `InvoiceDate` column. Analyse revenue by weekday or month; report every day in a quarter, including days with no sales.

### Part 1: Vectorised string operations

#### The `.str` accessor

A Python loop over strings is slow and crashes on missing values:

```python
data = pd.Series(['peter', 'Paul', None, 'MARY', 'gUIDO'])
# [s.capitalize() for s in data]   # AttributeError on None
data.str.capitalize()               # works; None stays NaN
```

`.str` applies string methods to a whole Series, vectorised and NaN-safe.

| Method | Description |
|---|---|
| `str.split()` | split on a delimiter or regex |
| `str.strip()` | trim whitespace (including newlines) |
| `str.lower()` / `upper()` | change case |
| `str.get(i)` | i-th element of each item |
| `str.replace()` | replace a pattern |

```python
s = pd.Series([' house ', 'kitchen', 'BATHROOM '])
s.str.upper(); s.str.strip(); s.str.replace(' ', '_')
```

Normalize before grouping or joining: `'Hanoi'`, `'hanoi'` and `'Hanoi '` are three different keys, and a report would split one city into three rows without any error.

**Searching**
```python
s = pd.Series(['apple', 'banana', 'apricot', 'blueberry'])
s.str.contains('A', case=False); s.str.startswith('a'); s.str.endswith('t')
```

**Splitting**
```python
s = pd.Series(['a_b_c', 'c_d_e', 'f_g_h'])
s.str.split('_')                 # Series of lists
s.str.split('_').str.get(1)      # second element
s.str.split('_', expand=True)    # DataFrame, one column per part
```

`expand=True` turns one column into several (full name → first/last; URL → domain/parameters).

#### Regular expressions

| Token | Matches |
|---|---|
| `\d` | a digit |
| `\w` | a letter, digit or `_` |
| `+` | one or more |
| `*` | zero or more |
| `()` | capture group: the part to extract |

| Method | Matches | Returns |
|---|---|---|
| `str.match()` | at the start only | boolean Series |
| `str.contains()` | anywhere | boolean Series |
| `str.extract()` | first match, capture groups | DataFrame (one column per group) |
| `str.findall()` | every non-overlapping match | Series of lists |

All take `flags`; `re.IGNORECASE` (`re.I`) is the common one.

```python
import re
s = pd.Series(['Apple', 'Banana', 'apricot', 'Avocado'])
s.str.match(r'A.*'); s.str.match(r'a.*', flags=re.IGNORECASE)

s = pd.Series(['Order #123', 'REF:456', 'order #789'])
s.str.contains(r'order', flags=re.IGNORECASE)

s = pd.Series(['ID: A123', 'id: b456', 'No ID here'])
s.str.extract(r'ID: [A-Z](\d+)')               # misses 'id: b456'
s.str.extract(r'id: [a-z](\d+)', flags=re.I)   # both; 'No ID here' → NaN

s = pd.Series(['#sale #promo', '#Sale #new', '#shipping'])
s.str.findall(r'#([a-z]+)', flags=re.IGNORECASE)
```

Uses: `match` to validate (every SKU starts with `SKU-`), `contains` to filter (reviews mentioning "delivery"), `extract` to pull a zip code, `findall` to collect hashtags.

### Part 2: Time series basics

A time series is data in time order where the order matters (GDP, prices, daily revenue). Full treatment in [[Time-series Analysis/contents/00-Index|Time-series Analysis]].

- **`Timestamp`**: one point in time (nanosecond precision).
- **`DatetimeIndex`**: an index of timestamps; enables time-aware selection and functions.

#### `pd.to_datetime`

```python
pd.to_datetime(['2023-01-01', '2023/01/02', '05-Jan-2023'], format="mixed")
pd.to_datetime('01--2023--15', format='%m--%Y--%d')
pd.to_datetime(['2023-01-01', 'not a date'], errors='coerce')   # bad value → NaT
```

`NaT` ("Not a Time") is the datetime `NaN`. Convert date columns first: `resample()`, `rolling()` and `.dt` need datetime types, and filtering is faster.

#### DatetimeIndex

```python
df = pd.DataFrame({'sale_date': pd.to_datetime(['2023-01-15', '2023-01-16']), 'sales': [100, 150]})
df.set_index('sale_date', inplace=True)
```

Gives intuitive slicing (`df['2023-05']`), is required for `resample()` (change frequency) and convenient for `rolling()` (moving averages), and is fast.

```python
ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2020', periods=1000))
ts['2021']; ts['2021-05']; ts['2022-01-01':'2022-01-31']
```

This is partial string indexing. `pd.date_range(start, end, periods, freq)` needs three of the four arguments. To report every day including days without sales, build a full index with `date_range` and reindex the data onto it.

#### Features with `.dt`

```python
dates = pd.Series(pd.to_datetime(['2023-01-01', '2023-02-15', '2023-03-30']))
dates.dt.year; dates.dt.month; dates.dt.dayofweek   # Monday = 0
dates.dt.day_name(); dates.dt.quarter
```

`dayofweek` helps staffing for peak days, `quarter` drives financial reporting, an `is_weekend` flag often helps retail forecasts.

## ✏️ Exercises

**1.** Produce a stripped, title-cased `cleaned_name`, select New York customers, and split `location` into street, city, country.
> ```python
> df_lab1 = pd.DataFrame({
>     'full_name': [' John Smith ', 'Jane Doe', ' peter jones '],
>     'location': ['123 Main St, New York, USA', '456 Oak Ave, London, UK', '789 Pine Ln, New York, USA']})
> ```

> [!example]- Solution
> ```python
> df_lab1['cleaned_name'] = df_lab1['full_name'].str.strip().str.title()
> ny_customers = df_lab1[df_lab1['location'].str.contains('New York')]
> df_lab1[['street', 'city', 'country']] = (
>     df_lab1['location'].str.split(',', expand=True).apply(lambda c: c.str.strip()))
> ```
> Re-enter `.str` after each call. Splitting on `','` leaves a leading space (`' New York'`), which would later break a groupby, hence the extra strip.

**2.** On `['Apple', 'Banana', 'apricot', 'Avocado']`, compare `.str.match(r'A.*')` with `.str.contains(r'A')`.

> [!example]- Solution
> Both give True, False, False, True here, because no string has an interior capital A. They still differ: on `'Pineapple'`, `contains(r'a')` is True but `match(r'a.*')` is False (it must start with `a`). Use `match` to validate, `contains` to filter. With `flags=re.IGNORECASE`, `apricot` matches too.

**3.** From the comments, validate which start with "REF" or "Complaint" (case-insensitive), extract the reference digits, and collect hashtags.
> ```python
> df_comments = pd.DataFrame({'comments': [
>     'REF-1234: Great product!', 'Complaint: The item (REF-5678) was broken.',
>     'REF-9101, love it! #awesome #greatbuy', 'This is not a valid comment',
>     'complaint: another issue with REF-1122']})
> ```

> [!example]- Solution
> ```python
> import re
> c = df_comments['comments']
> is_valid = c.str.match(r'(REF|Complaint).*', flags=re.IGNORECASE)  # T, T, T, F, T
> complaints_df = df_comments[c.str.contains('complaint', flags=re.IGNORECASE)]
> df_comments['ref_id'] = c.str.extract(r'REF-(\d+)', flags=re.I)     # 1234, 5678, 9101, NaN, 1122
> df_comments['hashtags'] = c.str.findall(r'#(\w+)')                 # [], [], ['awesome','greatbuy'], [], []
> ```
> The parentheses decide what is returned: `REF-(\d+)` matches `REF-1234` but returns `1234`. No match gives `NaN` for `extract` and an empty list for `findall`; `.explode()` turns lists into rows for counting.

**4.** Convert and index by date, total February 2023 sales, add a weekday column, find the best weekday.
> ```python
> df_sales = pd.DataFrame({'date': ['2023-01-29', '2023-01-30', '2023-02-01', '2023-02-02', '2023-02-03'],
>                          'sales': [250, 275, 310, 290, 350]})
> ```

> [!example]- Solution
> ```python
> df_sales['date'] = pd.to_datetime(df_sales['date'])
> df_sales.set_index('date', inplace=True)
> df_sales.loc['2023-02', 'sales'].sum()             # 310 + 290 + 350 = 950
> df_sales['day_of_week'] = df_sales.index.day_name()
> df_sales.groupby('day_of_week')['sales'].mean()
> ```
> A `DatetimeIndex` has `.day_name()`, `.year` etc. directly; `df_sales.index.dt` raises `AttributeError` (`.dt` is for columns). With five rows, "best day" (Friday, 350) is noise.

**5.** (Advanced) With `OnlineRetail.csv`: clean it, find the busiest hour, flag coffee products and compare their revenue, and find the best-selling gift/christmas product in December.

> [!example]- Solution
> ```python
> df = pd.read_csv('OnlineRetail.csv', encoding='latin-1')
> df = df.dropna(subset=['CustomerID'])
> df = df[df['Quantity'] > 0]                          # drop returns/cancellations
> df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
> df['Hour'] = df['InvoiceDate'].dt.hour
> df['Hour'].value_counts().idxmax()
> df['Description'] = df['Description'].str.lower()
> df['IsCoffeeRelated'] = df['Description'].str.contains('coffee', na=False)
> df['Revenue'] = df['Quantity'] * df['UnitPrice']
> df.groupby('IsCoffeeRelated')['Revenue'].agg(['sum', 'mean', 'count'])
> december = df[df['InvoiceDate'].dt.month == 12]
> festive = december[december['Description'].str.contains('gift|christmas', na=False)]
> festive.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head()
> ```
> - `na=False`: `str.contains` returns NaN for missing descriptions, and NaN breaks boolean masks.
> - `'gift|christmas'` is a regex alternation.
> - The file needs `encoding='latin-1'`.
> - Negative quantities are returns (invoices starting with `C`); exclude them unless you want net figures.

## 📝 Summary

- `.str` is vectorised and NaN-safe; normalize text (`strip`, case) before grouping or joining.
- `str.split(expand=True)` makes several columns from one.
- Regex methods: `match` (start), `contains` (anywhere), `extract` (capture groups → DataFrame), `findall` (all matches → lists). Capture groups decide what is returned.
- `pd.to_datetime` then `set_index`: enables partial string indexing, `resample`, `rolling`.
- `NaT` is the datetime NaN; `errors='coerce'` avoids crashes.
- `.dt` on columns; attributes directly on a `DatetimeIndex`.

## ⚠️ Important Notes

1. Re-enter `.str` on each chained call.
2. `str.contains` returns NaN for missing values; pass `na=False` when filtering.
3. `df['col'].dt.year` but `df.index.year`.
4. `match` is anchored at the start, `fullmatch` requires the whole string, `contains` is unanchored; don't validate with `contains`.
5. Escape regex special characters: `.` matches anything, so `contains('3.5')` matches `'385'`; use `re.escape()` or `regex=False`.
6. In Pandas ≥ 2.0, `str.replace` defaults to `regex=False`.
7. `pd.to_datetime` without `format` may misread ambiguous dates.
8. `format="mixed"` needs Pandas ≥ 2.0 and is slower.
9. Sort a `DatetimeIndex` (`sort_index()`) before slicing.
10. Missing dates have no row; build a complete `date_range` and reindex, filling with 0.

> [!warning] Gaps in the source slides
> - Slides 4 and 18 are section dividers.
> - Slide 12 links to "all available flags"; see the Python `re` documentation.
> - Lab #4 uses `OnlineRetail.csv`, not present in `documents/`; exercise 5 assumes the standard UCI Online Retail columns, so results could not be run here.
> - Lesson 4 is missing from the provided material.

**Previous:** [[03 - Data Aggregation and Group Operations]] · **Next:** [[06 - Data Cleaning]]
