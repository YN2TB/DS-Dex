---
subject: Data Preparation and Visualization
chapter: 05
tags: [ds, pandas, regex, time-series, feature-engineering, text-processing]
source: "Lesson 5 String Manipulation and Time Series Data.pdf — Dr. Nguyen Tuan Long, NEU"
---

# String Manipulation and Time Series Data

> [!note] Where this sits in the course
> The bridge from **Part 1 (tools)** into **Part 2 (data architecture)**. Everything so far treated columns as opaque values. This chapter cracks open the two column types that hide the most information — **text** and **dates** — and turns them into model-ready features.
>
> **⚠️ Lesson 4 is missing from the source material.** The lesson sequence jumps from 3 to 5, so whatever the lecturer covered as Lesson 4 is not represented anywhere in this vault. See [[00-Index]].

## 📘 Main Knowledge

### Business context

The motivating scenario, carried through the whole lesson:

- **Text** — a `Description` column holds product descriptions like `'WHITE HANGING HEART T-LIGHT HOLDER'`. How do you extract `'WHITE'` and `'HEART'` to categorise products, or reconcile several spellings of the same product?
- **Time** — an `InvoiceDate` column holds timestamps. How do you analyse revenue by day of week or by month, or build a report covering *every* day in a quarter including days with no sales?

Both are the same task: **turn a raw column into intelligent features**.

---

## Topic 1 — Vectorised string operations

### The `.str` accessor

Looping over strings in Python is slow, verbose, and — the real problem — **crashes on missing values**:

```python
data = pd.Series(['peter', 'Paul', None, 'MARY', 'gUIDO'])

# [s.capitalize() for s in data]   # AttributeError: 'NoneType' has no attribute 'capitalize'

data.str.capitalize()              # works — None stays NaN
```

The `.str` accessor applies string methods across a whole Series, **vectorised and `NaN`-safe**. Missing values pass through untouched instead of raising.

### Common methods

| Method | Description |
|---|---|
| `Series.str.split()` | Split on a delimiter or regex |
| `Series.str.strip()` | Trim whitespace from both sides, including newlines |
| `Series.str.lower()` / `.upper()` | Case conversion |
| `Series.str.get()` | Index into each element (retrieve the *i*-th item) |
| `Series.str.replace()` | Replace each occurrence of a pattern/regex |

**Normalisation:**

```python
s = pd.Series([' house ', 'kitchen', 'BATHROOM '])
s.str.upper()
s.str.strip()
s.str.replace(' ', '_')
```

> [!warning] Why normalisation is not cosmetic
> `'Hanoi'`, `'hanoi'`, and `'Hanoi '` are **three different keys** to `groupby` and `merge`. Skip normalisation and your regional sales report splits one city across three rows — and nobody notices, because the numbers still look plausible. Normalise *before* every grouping or join.

**Searching:**

```python
s = pd.Series(['apple', 'banana', 'apricot', 'blueberry'])
s.str.contains('A', case=False)   # substring anywhere, case-insensitive
s.str.startswith('a')
s.str.endswith('t')
```

**Splitting:**

```python
s = pd.Series(['a_b_c', 'c_d_e', 'f_g_h'])
s.str.split('_')                  # → Series of lists
s.str.split('_').str.get(1)       # → the second element of each
s.str.split('_', expand=True)     # → DataFrame, one column per part
```

`expand=True` is the one that matters: it converts one messy column into several clean ones — splitting `'Full Name'` into first/last, or a URL into domain and campaign parameters.

### Regular expressions

Regex is a mini-language for describing text patterns — "find and replace" with real expressive power.

| Token | Matches |
|---|---|
| `\d` | Any digit (0–9) |
| `\w` | Any alphanumeric character (a-z, A-Z, 0-9, `_`) |
| `+` | One or more occurrences |
| `*` | Zero or more occurrences |
| `()` | **Capture group** — the part you want to extract |

`\d+` finds any run of digits; `([A-Z]+)` finds *and captures* a run of uppercase letters.

**The four Pandas regex methods** — the distinction is *where* it matches and *what* it returns:

| Method | Matches | Returns |
|---|---|---|
| `.str.match()` | Only at the **start** of the string | Boolean Series |
| `.str.contains()` | **Anywhere** in the string | Boolean Series |
| `.str.extract()` | First match, from capture groups | **DataFrame**, one column per group |
| `.str.findall()` | **Every** non-overlapping match | Series of **lists** |

All accept a `flags` argument; `re.IGNORECASE` (aliased `re.I`) is by far the most used — `import re` first.

```python
import re

# match — validation. Anchored at the start.
s = pd.Series(['Apple', 'Banana', 'apricot', 'Avocado'])
s.str.match(r'A.*')
s.str.match(r'a.*', flags=re.IGNORECASE)

# contains — filtering. The workhorse.
s = pd.Series(['Order #123', 'REF:456', 'order #789'])
s.str.contains(r'order', flags=re.IGNORECASE)

# extract — pull out one structured piece
s = pd.Series(['ID: A123', 'id: b456', 'No ID here'])
s.str.extract(r'ID: [A-Z](\d+)')            # misses 'id: b456'
s.str.extract(r'id: [a-z](\d+)', flags=re.I)  # catches both; 'No ID here' → NaN

# findall — every occurrence
s = pd.Series(['#sale #promo', '#Sale #new', '#shipping'])
s.str.findall(r'#([a-z]+)', flags=re.IGNORECASE)
```

Typical uses: `match` validates that every SKU starts with `SKU-`; `contains` filters reviews mentioning "delivery"; `extract` pulls a zip code out of an address; `findall` collects every hashtag from a post.

---

## Topic 2 — Time series basics

### What makes a time series different

A time series is data points **listed in time order**, where the *sequence itself carries meaning*. GDP, inflation, stock prices, interest rates, daily revenue — all time series. Full treatment lives in [[Time-series Analysis/contents/00-Index|Time-series Analysis]]; this chapter covers the Pandas mechanics.

Two structures:

- **`Timestamp`** — a single point in time, nanosecond precision.
- **`DatetimeIndex`** — an Index of `Timestamp`s. The backbone: it is what unlocks time-aware selection and the specialised time functions.

### Converting with `pd.to_datetime`

```python
# Mixed formats
dates_str = ['2023-01-01', '2023/01/02', '05-Jan-2023']
pd.to_datetime(dates_str, format="mixed")

# Non-standard format, declared explicitly
pd.to_datetime('01--2023--15', format='%m--%Y--%d')

# Unparseable values → NaT instead of a crash
pd.to_datetime(['2023-01-01', 'not a date'], errors='coerce')
```

**`NaT`** ("Not a Time") is the datetime equivalent of `NaN`. `errors='coerce'` is what keeps a single malformed date from killing an entire pipeline.

**Convert date columns first, always.** It (1) unlocks `resample()`, `rolling()`, and the `.dt` accessor, which simply do not exist for strings, and (2) makes filtering and aggregation dramatically faster.

### Setting the DatetimeIndex

```python
df = pd.DataFrame({'sale_date': pd.to_datetime(['2023-01-15', '2023-01-16']),
                   'sales': [100, 150]})
df.set_index('sale_date', inplace=True)
```

This is *the* critical step. It converts an ordinary DataFrame into a time-series-aware object:

- **Intuitive slicing** — `df['2023-05']` just works.
- **Prerequisite for `resample()`** (change frequency, e.g. daily → monthly) and `rolling()` (moving averages).
- **Faster** — `DatetimeIndex` operations are heavily optimised.

### Selection and slicing

```python
ts = pd.Series(np.random.randn(1000),
               index=pd.date_range('1/1/2020', periods=1000))

ts['2021']                        # a whole year
ts['2021-05']                     # a whole month
ts['2022-01-01':'2022-01-31']     # an explicit range
```

This is **partial string indexing** — a string that names a period selects everything inside it. `pd.date_range(start, end, periods, freq)` generates the index itself; it needs any three of the four arguments.

`date_range` also answers the "report every day in the quarter, including days with no sales" problem from the business context: generate the complete index, then reindex your sparse data onto it.

### Feature engineering with `.dt`

`.dt` is to datetimes what `.str` is to strings:

```python
dates = pd.Series(pd.to_datetime(['2023-01-01', '2023-02-15', '2023-03-30']))

dates.dt.year
dates.dt.month
dates.dt.dayofweek     # Monday = 0, Sunday = 6
dates.dt.day_name()    # 'Sunday', 'Wednesday', ...
dates.dt.quarter
```

These map straight onto decisions: `dayofweek` identifies peak trading days for staffing, `quarter` drives financial reporting, and a derived `is_weekend` flag measurably improves retail forecasting models.

## ✏️ Exercises

**1.** Clean and structure this customer sign-up data: produce a title-cased, whitespace-free `cleaned_name`; select only New York customers; split `location` into `street`, `city`, and `country`.
> ```python
> df_lab1 = pd.DataFrame({
>     'full_name': [' John Smith ', 'Jane Doe', ' peter jones '],
>     'location': ['123 Main St, New York, USA', '456 Oak Ave, London, UK',
>                  '789 Pine Ln, New York, USA']})
> ```

> [!example]- Solution
> ```python
> # 1. Normalise — chain accessors, order matters
> df_lab1['cleaned_name'] = df_lab1['full_name'].str.strip().str.title()
>
> # 2. Filter
> ny_customers = df_lab1[df_lab1['location'].str.contains('New York')]
>
> # 3. Split into three columns
> df_lab1[['street', 'city', 'country']] = (
>     df_lab1['location'].str.split(',', expand=True))
> ```
> Note you must **re-enter `.str`** after each call: `.str.strip().str.title()`, not `.str.strip().title()`. Each `.str` method returns a plain Series, so the accessor is needed again.
>
> Strip before title-casing — `' peter jones '` → `'Peter Jones'`. Reversing the order leaves the padding in place.
>
> One flaw worth seeing: `str.split(',', expand=True)` leaves a **leading space** on `city` and `country` (`' New York'`), because the delimiter is `,` and not `, `. That is exactly the invisible defect that later breaks a `groupby`. Fix it:
> ```python
> df_lab1[['street', 'city', 'country']] = (
>     df_lab1['location'].str.split(',', expand=True).apply(lambda c: c.str.strip()))
> ```

**2.** Explain the difference between `.str.match(r'A.*')` and `.str.contains(r'A')` on `pd.Series(['Apple', 'Banana', 'apricot', 'Avocado'])`. Which rows does each return?

> [!example]- Solution
> `.match()` is **anchored at the start**; `.contains()` matches **anywhere**.
>
> | | `match(r'A.*')` | `contains(r'A')` |
> |---|---|---|
> | Apple | True | True |
> | Banana | False | False |
> | apricot | False | False |
> | Avocado | True | True |
>
> On *this* data the two agree, because no string contains an interior capital `A` — `'Banana'` is `B-a-n-a-n-a`, all lowercase after the `B`. Identical output here does **not** mean the methods are interchangeable.
>
> To expose the real difference you need a string with an interior match, e.g. `'Pineapple'`:
> - `contains(r'a')` → **True** (the `a` in "-apple")
> - `match(r'a.*')` → **False** (the string does not *start* with `a`)
>
> **Rule:** validation → `match`; filtering → `contains`. Both take `flags=re.IGNORECASE`, which makes `apricot` match in both columns.

**3.** From the comments below: validate which start with "REF" or "Complaint" (case-insensitive), extract just the digits of each reference number, and collect all hashtags.
> ```python
> df_comments = pd.DataFrame({'comments': [
>     'REF-1234: Great product!',
>     'Complaint: The item (REF-5678) was broken.',
>     'REF-9101, love it! #awesome #greatbuy',
>     'This is not a valid comment',
>     'complaint: another issue with REF-1122']})
> ```

> [!example]- Solution
> ```python
> import re
> c = df_comments['comments']
>
> # 1. Validate — anchored, so match()
> is_valid = c.str.match(r'(REF|Complaint).*', flags=re.IGNORECASE)
> # → True, True, True, False, True
>
> # 2. Categorise — anywhere, so contains()
> complaints_df = df_comments[c.str.contains('complaint', flags=re.IGNORECASE)]
>
> # 3. Extract the digits — capture group holds ONLY the digits
> df_comments['ref_id'] = c.str.extract(r'REF-(\d+)', flags=re.I)
> # → '1234', '5678', '9101', NaN, '1122'
>
> # 4. All hashtags
> df_comments['hashtags'] = c.str.findall(r'#(\w+)')
> # → [], [], ['awesome','greatbuy'], [], []
> ```
> The key idea in step 3: the parentheses decide what you *get back*, not what you *match*. `r'REF-(\d+)'` matches the whole `REF-1234` but returns only `1234`. Widening the group to `r'(REF-\d+)'` would return `REF-1234`.
>
> Row 4 has no match, so `extract` yields `NaN` rather than erroring — extract is `NaN`-safe by design. And `extract` returns a **DataFrame** when there are multiple groups; with one group it collapses to a Series, which is why the assignment above works.
>
> Note `findall` returns **empty lists**, not `NaN`, where nothing matched. Lists in a column are awkward downstream — `.explode()` turns them into one row per hashtag, which is what you want for a trend count.

**4.** Prepare this sales data for time analysis: convert and index by date, total February 2023 sales, add a day-of-week column, and find the most profitable weekday.
> ```python
> df_sales = pd.DataFrame({
>     'date': ['2023-01-29', '2023-01-30', '2023-02-01', '2023-02-02', '2023-02-03'],
>     'sales': [250, 275, 310, 290, 350]})
> ```

> [!example]- Solution
> ```python
> # 1. Convert and index — always this order
> df_sales['date'] = pd.to_datetime(df_sales['date'])
> df_sales.set_index('date', inplace=True)
>
> # 2. Partial string indexing selects the whole month
> df_sales['2023-02']
> df_sales['2023-02']['sales'].sum()      # 950
>
> # 3. .dt is NOT needed on the index — it has the attributes directly
> df_sales['day_of_week'] = df_sales.index.day_name()
>
> # 4. Average by weekday
> df_sales.groupby('day_of_week')['sales'].mean()
> ```
> The trap in step 3: once `date` is the **index**, it is a `DatetimeIndex`, and `DatetimeIndex` exposes `.day_name()`, `.year`, `.month` **directly** — no `.dt`. Writing `df_sales.index.dt.day_name()` raises an `AttributeError`. `.dt` is only for datetime data sitting in a *column*.
>
> Step 2 is why setting the index was worth it: `df_sales['2023-02']` reads as plain English and needs no comparison operators.
>
> With five rows the "most profitable day" (Friday, 350) is noise, not insight — worth stating out loud when reporting on a small sample.

**5.** (Advanced) Using `OnlineRetail.csv`: clean it, find the busiest transaction hour, flag coffee-related products and compare their revenue to everything else, then find the best-selling gift/christmas product in December.

> [!example]- Solution
> ```python
> df = pd.read_csv('OnlineRetail.csv', encoding='latin-1')
>
> # 1. Clean
> df = df.dropna(subset=['CustomerID'])
> df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
>
> # 2. Busiest hour
> df['Hour'] = df['InvoiceDate'].dt.hour
> df['Hour'].value_counts().idxmax()          # → 12 (midday peak)
>
> # 3. Text analysis
> df['Description'] = df['Description'].str.lower()
> df['IsCoffeeRelated'] = df['Description'].str.contains('coffee', na=False)
>
> df['Revenue'] = df['Quantity'] * df['UnitPrice']
> df.groupby('IsCoffeeRelated')['Revenue'].agg(['sum', 'mean', 'count'])
>
> # 4. December gift/christmas bestseller
> december = df[df['InvoiceDate'].dt.month == 12]
> festive = december[december['Description'].str.contains('gift|christmas', na=False)]
> festive.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head()
> ```
> Four things this exercise is really testing:
>
> **`na=False` is mandatory.** `Description` has missing values, and `.str.contains` returns `NaN` — not `False` — for them. `NaN` in a boolean mask raises `ValueError: cannot mask with non-boolean array`. Passing `na=False` treats missing as "no match".
>
> **`'gift|christmas'` is a regex alternation**, so one call covers both terms. That is regex earning its keep over two chained conditions.
>
> **The file needs `encoding='latin-1'`.** OnlineRetail contains non-UTF-8 bytes and the default read raises `UnicodeDecodeError`.
>
> **This dataset has negative `Quantity`** — those are returns/cancellations (invoice numbers starting with `C`). Revenue summed without excluding them understates the total, and a "bestseller" ranking can be quietly corrupted by them. Filter with `df[df['Quantity'] > 0]` unless you specifically want net figures.

## 📝 Summary

- **`.str` is vectorised and `NaN`-safe**; Python loops over strings are slow and crash on `None`.
- **Normalise text (`strip`, `lower`/`title`) before any `groupby` or `merge`** — `'Hanoi'` and `'hanoi '` are different keys and will silently split your report.
- **`.str.split(..., expand=True)`** turns one messy column into several clean ones.
- **Four regex methods:** `match` (start-anchored, boolean), `contains` (anywhere, boolean), `extract` (first match of capture groups → DataFrame), `findall` (all matches → lists).
- **Capture groups `()` decide what you get back**, not what you match.
- **`pd.to_datetime` first, `set_index` second.** That pair unlocks partial string indexing, `resample`, `rolling`, and real speed.
- **`NaT` is `NaN` for datetimes**; `errors='coerce'` prevents one bad date from crashing a pipeline.
- **`.dt` on a datetime column, bare attributes on a `DatetimeIndex`** — `year`, `month`, `dayofweek` (Mon=0), `day_name()`, `quarter`.

## ⚠️ Important Notes

**Re-enter `.str` on every chained call.** `.str.strip().str.title()` — not `.str.strip().title()`. Each method returns a normal Series.

**`.str.contains()` returns `NaN` for missing values, and `NaN` breaks boolean masks.** Always pass `na=False` when filtering a column that might have gaps. This is the single most common runtime error in this chapter.

**`.dt` works on columns; `DatetimeIndex` has the attributes directly.** `df['col'].dt.year` but `df.index.year`. Mixing them up raises `AttributeError`.

**`match` is anchored, `fullmatch` is exact, `contains` is unanchored.** Using `contains` for validation accepts junk with a valid-looking prefix buried inside it.

**Regex special characters must be escaped when meant literally.** `.` matches *any* character, so `.str.contains('3.5')` also matches `'385'`. Use `re.escape()` or pass `regex=False`.

**`.str.replace()` defaults changed.** In Pandas ≥ 2.0 the default is `regex=False`; older code that relied on regex behaviour silently stops working. Pass `regex=True` explicitly.

**`findall` returns empty lists, not `NaN`.** Lists inside a column are hard to aggregate — use `.explode()` to get one row per match.

**`pd.to_datetime` without `format` can guess wrong on ambiguous dates.** `03/04/2023` is April 3rd or March 4th. Pass `format=` or `dayfirst=True`.

**`format="mixed"` requires Pandas ≥ 2.0** and is slower, since it infers per element. Fine for messy data, wasteful for uniform data.

**Partial string indexing needs a *sorted* index.** Slicing an unsorted `DatetimeIndex` raises or returns wrong results — call `df.sort_index()` after setting it.

**Missing dates are invisible.** If no sale occurred on 3 February, there is simply no row — and a chart drawn from it will imply continuity that does not exist. Build a complete index with `pd.date_range` and reindex onto it, filling with zeros. This is the "report every day in the quarter" requirement from the business context, and it is the one people forget.

> [!warning] Gaps in the source slides
> - **Slides 4 and 18** are section dividers with no content.
> - **Slide 12** links to "all available flags" without an extractable URL — see the [Python `re` documentation](https://docs.python.org/3/library/re.html#flags).
> - **Slide 26 (Lab #4)** requires `OnlineRetail.csv`, which is **not present** in `documents/`. The same file was referenced in [[02 - Loading, Diagnosing, Missing Data and Combining Datasets]] via a hyperlink that also did not survive extraction. My Exercise 5 solution is written against the standard UCI Online Retail dataset; verify the column names against the lecturer's copy.
> - **Lesson 4 does not exist in the provided material** — the sequence runs 0, 1, 2, 3, **5**, 6, 7, 8, 9.

---
**Previous:** [[03 - Data Aggregation and Group Operations]] · **Next:** [[06 - Data Cleaning]]
