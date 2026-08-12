---
subject: Time-series Analysis
chapter: 01
tags: [ds, time-series, decomposition, python, datetime, growth-rates]
source: "Lecture01_timeseries.ipynb — Tran Thi Ha, Faculty of Mathematical Economics, NEU (2025)"
---

# What is a Time Series? Data & Visualization

> [!note] Course information
> **Time Series Analysis and Forecast in Economics and Finance** · 3 credits
> **Lecturer:** Tran Thi Ha · `tranha@neu.edu.vn` · `www.mfe.neu.edu.vn/tranthiha`
> **Assessment:** Attendance 10% · **Computer test (Python) 20%** · Assignment 20% · **Final exam 50%**
>
> **Textbooks** — all three are in `documents/`:
> - **Ben Auffarth (2021)**, *Machine Learning for Time-Series with Python*
> - **Marco Peixeiro (2022)**, *Time Series Forecasting in Python*
> - **Hamilton, J. D. (1994)**, *Time Series Analysis* — the classical econometric reference
>
> See [[00-Index]] for the full course map.

## 📘 Main Knowledge

### What is a time series?

> A **time series** is a sequence of observations on a variable, **ordered in time** and recorded at regular or irregular intervals.
>
> - **Time is an essential dimension of the data**
> - **Observations are not independent across time**
> - **Past values often contain information about the future**
>
> *Examples:* GDP, inflation, interest rates, stock prices, exchange rates.

**The second bullet is what makes this a separate subject.** Nearly all of [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] assumes i.i.d. observations — sampling distributions, confidence intervals, and hypothesis tests all rest on it. Time series violates it by construction, so the entire inferential apparatus must be rebuilt.

**Two types of series:**

| Type | Meaning | Aggregation high → low frequency |
|---|---|---|
| **Point of time → stock variable** | A level measured at an instant | **Average** |
| **Period → flow variable** | A quantity accumulated over an interval | **Sum** |

*Examples:* stock price, profit, interest rate. **Notation: $y_t$.**

**Common frequencies:** annual · quarterly · monthly · weekly · daily.

**The stock/flow distinction determines how you aggregate.** Converting quarterly profit (a flow) to annual profit means **summing** the four quarters; converting a daily stock price (a stock) to a monthly figure means **averaging**. Getting this backwards silently corrupts every downstream number.

### Lags, differences and growth rates

| Concept | Definition |
|---|---|
| **Lag** | $y_{t-1}, y_{t-2}, \dots$ |
| **Difference** | $\Delta y_t = y_t - y_{t-1}$ |
| **Growth rate** | $r_t = \dfrac{y_t - y_{t-1}}{y_{t-1}}$ |
| **Log-return** | $r_t = \ln\!\left(\dfrac{y_t}{y_{t-1}}\right)$ |

### Interpreting growth rates

The lecture's worked example:

| Year | $y_t$ | $\Delta y_t$ | $g_t$ |
|---|---|---|---|
| 2021 | 100 | – | – |
| 2022 | 120 | 20 | **20%** |
| 2023 | 135 | 15 | **12.5%** |
| 2024 | 145 | 10 | **7.4%** |

> - The **sum** of annual growth rates equals **39.9%**
> - Overall growth from **2021 to 2024** is **45%**
> - **The arithmetic average (13.3%) does *not* reflect true cumulative growth**
> - Constant annual growth rate: $(1+\bar{g})^3 = 1.45 \;\Rightarrow\; \bar{g} \approx \mathbf{13.2\%}$

**Growth rates compound, they do not add.** The correct average is the **geometric** mean, $\bar g = (y_T/y_0)^{1/n} - 1$, not the arithmetic mean of the individual rates. This is one of the most frequently made errors in applied economics.

### Log-returns

$$r_{\log} = \ln\!\left(\frac{y_t}{y_{t-1}}\right)\times 100\% = (\ln y_t - \ln y_{t-1})\times 100\%$$

**Only defined for strictly positive series.**

**Why log-returns are preferred in finance — three reasons:**

1. **They are additive across time.** $\ln(y_T/y_0) = \sum_t r_{\log,t}$, so multi-period returns are just sums. Simple returns must be compounded multiplicatively.
2. **They are symmetric.** A +50% then −50% simple return leaves you down 25%; in logs the two are $+40.5\%$ and $-69.3\%$, which correctly do not cancel.
3. **They approximate simple returns for small changes**, since $\ln(1+x) \approx x$ — so for daily data the two are nearly identical, and the log version has better statistical properties.

The lecture's exercise table (2017–2020: 100, 120, 136, 142) asks for both, and for the 2020-vs-2017 total.

### Components of a time series

> A time series can be decomposed into **four main components**:
> - **Observed** — the original recorded data
> - **Trend** — long-term movement or direction
> - **Seasonal** — repeating patterns over a fixed period
> - **Residual** — random fluctuations (the unexplained part)
>
> **This process is called *time series decomposition*.**

**Trend** — the long-term movement, the general direction over time; **sometimes called the *level* of the series**. *Example:* increasing earnings over many years.

**Seasonal** — repeating patterns over a fixed period, e.g. quarterly or yearly cycles.

**Residual** — what cannot be explained by trend or seasonality; **often interpreted as random noise**.

**Simulating a decomposable series** (the lecture's code):

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 120
t = np.arange(n)

trend    = 0.05 * t                      # linear upward trend
seasonal = 2 * np.sin(2 * np.pi * t / 12)  # period = 12
noise    = np.random.normal(0, 0.5, n)

y = trend + seasonal + noise             # additive decomposition
```

Note this is the **additive** form, $y_t = T_t + S_t + R_t$. The multiplicative form $y_t = T_t \times S_t \times R_t$ is developed in [[02 - Trend, Seasonality and Decomposition]].

---

### Time-Series Analysis (TSA)

> **Time-Series Analysis (TSA)** is a statistical approach for analysing data observed over time. The main goal is to identify **patterns** such as **trend**, **seasonality**, and **cyclical behavior**.
>
> TSA is related to **Exploratory Data Analysis (EDA)**, but is **specific to time-indexed data**. It includes **descriptive analysis** (summaries) and **exploratory analysis** (patterns and relationships).

**The key steps:**

1. Importing and parsing time-series data (e.g. dates)
2. Detecting missing values, outliers, and anomalies
3. Understanding variables and their distributions
4. Uncovering relationships between variables
5. Identifying **trend** and **seasonality**
6. **Preprocessing** — log, log-return, differencing, lag features
7. Modeling
8. Training a machine learning model

> TSA can be conducted using **univariate analysis** (one variable at a time), **multivariate analysis** (correlations between variables), and both **graphical** and **non-graphical** techniques.
>
> **TSA is iterative:** insights from visualization often lead back to data cleaning, preprocessing, and feature engineering. **Visualization → insight → preprocessing → refinement.**

This mirrors the workflow of [[Data Preparation and Visualization/contents/00-Index|Data Preparation and Visualization]], with steps 5–6 being the time-series-specific additions.

---

### Time in Python

> Python has many libraries for time handling: **`datetime`, `time`, `calendar`, `dateutil`, `pytz`**. Beginners often get confused because there are many time-related types: `date`, `datetime`, `time`, `timedelta`, `tzinfo`, …
>
> **Correct timestamps are crucial for:** sorting and indexing data by time · resampling (daily → monthly "sum/mean") · plotting and forecasting.
>
> **Key idea: treat time as a *first-class variable*, not just a string.**

**The `datetime` module's core objects:**

| Object | Meaning |
|---|---|
| **`date`** | Calendar date only (year–month–day) |
| **`datetime`** | Date **+ time** |
| **`time`** | Time of day only |
| **`timedelta`** | **Duration / difference** between two dates |

> In forecasting we usually need **`datetime` for timestamps** and **`timedelta` for shifts and horizons** (e.g. +7 days).
>
> **Rule of thumb: keep time data as `datetime` objects, not strings.**

```python
from datetime import date, datetime

today = date.today()
exam_date = date(2025, 4, 15)
days_left = exam_date - today
print("Days until exam:", days_left.days)

now = datetime.now()
ts = datetime(2021, 5, 18, 15, 39, 0)
print("ISO format:", ts.isoformat())      # 2021-05-18T15:39:00
```

**Parsing strings** — `dateutil` handles many formats:
```python
from dateutil import parser
parser.parse("2022-08")       # 2022-08-01
parser.parse("Aug 2022")
parser.parse("2022/08/15")
```

**Time zones** with `pytz`:
```python
import pytz
vn = pytz.timezone("Asia/Ho_Chi_Minh")
dt = vn.localize(datetime(2022, 8, 1, 10, 0))
```

> **ISO 8601** is the standard string format — `2021-05-18T15:39:00` — obtained via `.isoformat()`. **Many datasets store dates as strings, so we must parse them correctly.**

---

### Understanding the variables

> In TSA we start by **inspecting each variable individually** (univariate analysis): compute basic summary statistics · visualize distributions (histograms) · **detect missing values and outliers** · **check stationarity** of the series.
>
> **Key descriptive measures:** **Mean** (average level) · **Standard deviation** (variability) · **Standard error** (uncertainty of the mean) · **Median and percentiles** (robust measures for skewed data).

The theory is in [[Mathematical Statistics/contents/03 - Descriptive Statistics|Descriptive Statistics]]; **stationarity** is the time-series-specific addition and is developed in [[03 - Stationarity and Difference Equations]].

**The practical workflow** (the lecture's GDP/Trade example):

```python
import pandas as pd, matplotlib.pyplot as plt, seaborn as sns

df = pd.read_excel("GDP_Trade_Quarterly_Clean.xlsx")

# Build a proper quarterly time index
df["date"] = pd.PeriodIndex(
    df["Year"].astype(str) + df["Quarter"], freq="Q"
).to_timestamp()
df = df.set_index("date")

df[["GDP_SX", "Exports", "Imports"]].describe()
df.isna().sum()
df[["GDP_SX","Exports","Imports"]].agg(["mean","median","std"]).T
```

`pd.PeriodIndex(..., freq="Q").to_timestamp()` is the idiomatic way to turn "2020" + "Q1" into a usable timestamp index — see [[Data Preparation and Visualization/contents/05 - String Manipulation and Time Series Data|String Manipulation and Time Series Data]].

---

### Uncovering relationships

> When working with **multiple time-series variables**, we must examine how they move together to avoid **collinearity** and **feature leakage**.

**Collinearity** (highly correlated features):
- Independent variables are strongly correlated **with each other**
- **Can make linear regression coefficients unstable and hard to interpret**
- Common fixes: drop one variable, or use dimensionality reduction (e.g. PCA)

**Feature leakage** (target information leaks into inputs):
- A feature unintentionally reveals the target
- *Example:* `amount_paid` can reveal the label `has_paid`
- **Often produces "too good to be true" accuracy that fails in real deployment**

```python
plt.plot(df.index, df["GDP_SX"], label="GDP")
plt.plot(df.index, df["Exports"], label="Exports")
plt.plot(df.index, df["Imports"], label="Imports")
plt.title("GDP, Exports and Imports move together over time")

df[["GDP_SX","Imports","Exports"]].corr()
```

> [!warning] Correlation between time series is treacherous
> Two series that both **trend upward** will show high correlation whether or not they are related — this is **spurious regression**, and it is the single most common error in applied time-series work. GDP, exports, and imports all trending together tells you almost nothing until the trends are removed. The proper treatment is in [[03 - Stationarity and Difference Equations]] and the cointegration material of [[08 - VECM and Cointegration]].

## ✏️ Exercises

**1.** Using the lecture's growth table (2021: 100 → 2024: 145), verify that the arithmetic mean of growth rates is wrong and compute the correct average.

> [!example]- Solution
> | Year | $y_t$ | $g_t$ |
> |---|---|---|
> | 2021 | 100 | – |
> | 2022 | 120 | $20/100 = 20\%$ |
> | 2023 | 135 | $15/120 = 12.5\%$ |
> | 2024 | 145 | $10/135 = 7.4\%$ |
>
> **Arithmetic mean:** $(20 + 12.5 + 7.4)/3 = 13.3\%$.
>
> **Check it:** if the series grew at 13.3% for three years, it would reach $100(1.133)^3 = \mathbf{145.4}$ — close, but the reasoning is wrong and the closeness is luck. The failure is visible in the *sum*: the growth rates sum to 39.9%, yet total growth is $145/100 - 1 = \mathbf{45\%}$. **The 5.1 percentage-point gap is compounding** — growth in 2023 applies to a base already inflated by 2022's growth.
>
> **The correct (geometric) average** solves $(1+\bar g)^3 = 1.45$:
> $$\bar g = 1.45^{1/3} - 1 = 0.1319 \approx \mathbf{13.2\%}$$
>
> **Why the arithmetic mean is systematically biased.** By the AM–GM inequality, the arithmetic mean of positive numbers always **exceeds or equals** the geometric mean, with equality only when all values are identical. So **the arithmetic average of growth rates always overstates true compound growth**, and the gap widens as the rates become more dispersed.
>
> **The error becomes severe with volatility.** A fund returning +50% then −40% has arithmetic mean +5% — sounding profitable — while $1.5 \times 0.6 = 0.9$ means you actually **lost 10%**. Geometric mean: $\sqrt{0.9} - 1 = -5.1\%$.
>
> **Log-returns solve this cleanly**, which is exactly why finance uses them: $\ln(145/100) = 0.3716$, and dividing by 3 gives $0.1239$, so $e^{0.1239} - 1 = 13.2\%$ — the geometric answer, obtained by simple averaging.

**2.** Complete the lecture's log-return table (2017: 100, 2018: 120, 2019: 136, 2020: 142) and verify that log-returns are additive.

> [!example]- Solution
> | Year | $Y_t$ | Simple return | Log-return |
> |---|---|---|---|
> | 2017 | 100 | – | – |
> | 2018 | 120 | $20/100 = 20.00\%$ | $\ln(1.20) = 18.23\%$ |
> | 2019 | 136 | $16/120 = 13.33\%$ | $\ln(136/120) = 12.52\%$ |
> | 2020 | 142 | $6/136 = 4.41\%$ | $\ln(142/136) = 4.32\%$ |
>
> **2020 vs 2017:**
> - Simple: $142/100 - 1 = \mathbf{42.00\%}$
> - Log: $\ln(142/100) = \mathbf{35.07\%}$
>
> **The additivity check — this is the key property:**
> $$18.23 + 12.52 + 4.32 = \mathbf{35.07\%} \;\checkmark$$
>
> **Log-returns sum exactly to the multi-period log-return**, because
> $$\ln\frac{y_3}{y_0} = \ln\frac{y_1}{y_0} + \ln\frac{y_2}{y_1} + \ln\frac{y_3}{y_2}$$
> — the intermediate terms telescope.
>
> **Simple returns do not add:** $20 + 13.33 + 4.41 = 37.74\% \ne 42\%$. They must be **compounded**: $1.20 \times 1.1333 \times 1.0441 = 1.42$. ✓
>
> **Notice log-returns are always smaller than simple returns** for positive growth, since $\ln(1+x) < x$. The gap grows with the size of the change: negligible at 4.4% vs 4.3%, noticeable at 20% vs 18.2%. **For daily financial data, changes are small enough that the two are practically interchangeable** — which is why finance can use logs freely without losing interpretability.
>
> **The practical payoff:** to annualise a daily log-return, just multiply by 252 (trading days). To annualise a simple return you must compound. Every aggregation across time becomes addition.

**3.** Explain the stock/flow distinction and what goes wrong if you aggregate a stock variable by summing.

> [!example]- Solution
> **A flow** is measured *over a period* — profit in Q1, exports during 2023, rainfall in July. It has no meaning without a time interval attached.
>
> **A stock** is measured *at an instant* — a share price at market close, an inventory level on 31 December, an interest rate today. It has no duration.
>
> **The aggregation rule follows directly**, and the lecture states it: high → low frequency, **flow series → sum**, **stock series → average**.
>
> **Why summing a stock is nonsense.** Take a share price of \$100 on every day of January. Summing gives \$3,100 — a number corresponding to nothing. You did not own \$3,100 of stock; you owned \$100 of stock for a month. The **average** (\$100) is the meaningful monthly figure.
>
> Summing 12 monthly interest rates of 5% gives 60%, which is neither the annual rate (5%) nor the compounded rate (~6.2%).
>
> **Why averaging a flow is equally wrong.** Quarterly profits of 10, 12, 11, 13 give annual profit of **46**, not the average 11.5. Averaging reports a *typical quarter*, which is a different quantity — and understates annual profit by a factor of four.
>
> **The error is silent.** Both operations run without complaint and produce plausible-looking numbers. The most common real-world instance is aggregating **prices** (stock) alongside **quantities sold** (flow) in the same `resample().sum()` call, corrupting only the price column.
>
> ```python
> df.resample("Y").agg({"exports": "sum",      # flow
>                       "stock_price": "mean",  # stock
>                       "interest_rate": "mean"})  # stock
> ```
>
> **A caveat worth knowing:** some stocks are better summarised by *last* rather than *mean* — end-of-year inventory is `.last()`, not the average level. The right choice depends on what question the aggregate answers.

**4.** Explain why correlation between two trending time series is misleading, and what to do instead.

> [!example]- Solution
> **The problem: any two series that both trend upward will correlate strongly, whether or not they are related.**
>
> Consider $x_t = t + \varepsilon_t$ and $y_t = t + \eta_t$ with completely independent noise. Their correlation approaches **1** as the sample lengthens — not because they are connected, but because **both are dominated by $t$**. The correlation is measuring the shared trend, nothing more.
>
> This is **spurious regression**, established by Granger and Newbold (1974): regressing one random walk on another independent random walk produces a highly significant $t$-statistic and a high $R^2$ **most of the time**. The usual inference is invalid because the residuals are non-stationary, so the standard errors are wrong — the $t$-statistics do not follow a $t$-distribution and the critical values from [[Mathematical Statistics/contents/07 - Hypothesis Testing - One Sample|Hypothesis Testing]] do not apply.
>
> **This is why the lecture's GDP/Exports/Imports correlation matrix must be read cautiously.** All three trend upward with the Vietnamese economy, so a correlation near 0.95 is nearly guaranteed and tells you essentially nothing about their economic relationship.
>
> **What to do instead:**
>
> **1. Difference the series** — analyse $\Delta y_t$ rather than $y_t$. Differencing removes a linear trend, and correlations between *growth rates* are far more informative than correlations between *levels*.
>
> **2. Test for stationarity first** — the ADF and KPSS tests, developed in [[03 - Stationarity and Difference Equations]]. Correlating non-stationary series is invalid; correlating stationary ones is fine.
>
> **3. Use cointegration if the relationship is genuine.** Sometimes two series *should* trend together because a real long-run equilibrium links them — GDP and consumption, spot and futures prices. Differencing would throw that away. **Cointegration** tests whether a linear combination is stationary even though each series is not, and the VECM of [[08 - VECM and Cointegration]] models exactly this.
>
> **The decision rule:** if two series are non-stationary and **not** cointegrated, correlate their differences. If they **are** cointegrated, model the level relationship with a VECM. Never correlate raw non-stationary levels and report the number.

**5.** (Advanced) Explain why time series violates the i.i.d. assumption and what this breaks.

> [!example]- Solution
> **The lecture states it plainly: "observations are not independent across time" and "past values often contain information about the future."** Both statements deny independence.
>
> **What i.i.d. buys you in ordinary statistics** — and this is the whole of [[Mathematical Statistics/contents/04 - Sampling Distributions|Sampling Distributions]]:
> $$\mathbb{E}[\bar X] = \mu \qquad \operatorname{Var}(\bar X) = \frac{\sigma^2}{n}$$
> The second identity requires independence. It underlies the standard error, confidence intervals, every $t$-test, and the Central Limit Theorem's usual form.
>
> **What breaks, in order of severity:**
>
> **1. Standard errors are wrong — usually far too small.** With positive autocorrelation the true variance of $\bar X$ includes covariance terms:
> $$\operatorname{Var}(\bar X) = \frac{1}{n^2}\left(\sum_i \sigma^2 + 2\sum_{i<j}\operatorname{Cov}(X_i,X_j)\right)$$
> Positive covariances make this **larger** than $\sigma^2/n$, so the reported standard error understates uncertainty. **Confidence intervals are too narrow and tests reject far too often.** Effectively, 100 correlated observations carry the information of perhaps 20 independent ones.
>
> **2. Train/test splits cannot be random.** [[Data Preparation and Visualization/contents/09 - Building Pipelines|Building Pipelines]] insists on random splits; for time series that is **leakage**. Training on 2020 and 2022 to predict 2021 uses future information that will not exist at forecast time. Splits must be **chronological**, and cross-validation must use expanding or rolling windows.
>
> **3. Spurious regression** (Exercise 4) — non-stationarity makes ordinary inference invalid, not merely inefficient.
>
> **4. Shuffling destroys the data.** Every supervised-learning reflex — shuffle, split, batch randomly — is wrong here, because **the ordering *is* the information.**
>
> **The compensating advantage.** Dependence is not purely a problem: *"past values often contain information about the future"* is precisely what makes forecasting possible. If observations were genuinely independent, the best forecast of $y_{t+1}$ would always be $\bar y$ and there would be no subject. **Time-series analysis exists to exploit the dependence that classical statistics assumes away** — which is why AR, MA, and ARMA models ([[04 - AR, MA and ARMA Processes]]) model the autocorrelation structure directly rather than treating it as a nuisance.

## 📝 Summary

- **A time series is observations ordered in time**, where **observations are not independent** and **past values inform the future**.
- **Stock variables** are measured at an instant and aggregate by **averaging**; **flow variables** accumulate over a period and aggregate by **summing**.
- **Lag** $y_{t-1}$ · **difference** $\Delta y_t = y_t - y_{t-1}$ · **growth rate** $(y_t-y_{t-1})/y_{t-1}$ · **log-return** $\ln(y_t/y_{t-1})$.
- **Growth rates compound, they do not add.** The arithmetic mean overstates true growth; use the geometric mean or log-returns.
- **Log-returns are additive across time**, symmetric, and approximate simple returns for small changes — hence their use in finance.
- **Four components:** Observed = **Trend** + **Seasonal** + **Residual** — the additive decomposition.
- **TSA is EDA for time-indexed data**, focused on trend, seasonality, and cyclical behavior, and it is **iterative**.
- **Treat time as a first-class variable, not a string.** `date` (calendar), `datetime` (timestamp), `timedelta` (duration); parse with `dateutil`, localise with `pytz`, standardise with ISO 8601.
- **Check collinearity and feature leakage** before modelling multiple series.
- **Correlation between trending series is spurious** — difference or test for cointegration first.

## ⚠️ Important Notes

**Never average growth rates arithmetically.** Growth compounds, so the arithmetic mean always overstates the true rate (AM ≥ GM). The gap grows with volatility — +50% then −40% averages to +5% while you actually lost 10%.

**Log-returns require strictly positive data.** They are undefined for series that touch or cross zero.

**Aggregating a stock by summing produces a meaningless number**, and the error is silent. Prices, rates, and inventory levels average; profits, exports, and volumes sum.

**Correlation between non-stationary series is spurious.** Two independent random walks routinely produce high $R^2$ and significant $t$-statistics. Difference first, or test for cointegration.

**Random train/test splits leak future information.** Time-series validation must be chronological, with expanding or rolling windows.

**Autocorrelation makes standard errors too small.** Confidence intervals are too narrow and tests over-reject — 100 correlated observations may carry the information of 20 independent ones.

**Keep dates as `datetime` objects, never strings.** String dates sort lexicographically (so "10/2020" < "2/2020"), cannot be differenced, and break resampling entirely.

**Parse dates explicitly rather than letting pandas infer.** `03/04/2023` is ambiguous, and inference applied to the first row can silently mangle the rest — see [[Data Preparation and Visualization/contents/02 - Loading, Diagnosing, Missing Data and Combining Datasets|Loading and Diagnosing Data]].

**Time zones matter for intraday financial data.** Market opens, daylight saving transitions, and cross-exchange comparisons all depend on correct localisation.

**Feature leakage is easier in time series than elsewhere**, because a feature computed with any forward-looking window (a centred moving average, a full-sample standardisation) embeds the future.

**The additive decomposition assumes seasonal amplitude is constant.** When seasonal swings grow with the level — as they usually do for economic series — the multiplicative form is correct. See [[02 - Trend, Seasonality and Decomposition]].

> [!warning] Gaps in the source material
> **These "slides" are Google Colab notebooks in which each slide is an HTML string inside a `%%html` cell.** Text extracted cleanly once the markup was stripped, but:
> - **All plots and figures are outputs, not stored content** — the decomposition plots, distribution histograms, and the GDP/Exports/Imports time plot exist only as code that must be re-run.
> - **The dataset `GDP_Trade_Quarterly_Clean.xlsx` is referenced from `/content/`** (a Colab path) and is **not in `documents/`**. The GDP/Trade examples cannot be reproduced without it.
> - **Slides 12, 13, and 16 are exact duplicates** of the "Components of a Time Series" slide.
> - **Slides 6, 17 are code-only cells** (the simulated series) with no accompanying slide text.
> - **The log-return exercise table (slide 11) has empty cells** — it is a fill-in-the-blank for students; I have completed it in Exercise 2.
> - Some slide text is cut mid-word by the HTML structure (e.g. slide 9 ends `"Lecture 1"""))`).
>
> **⚠️ The syllabus does not match the notebook filenames.** Slide 3 lists Lecture 6 as *"ARIMA and Integrated Processes"*, Lecture 8 as *"Volatility Models: ARCH & GARCH"*, Lecture 9 as *"Time Series and ML: Concepts"* and Lecture 10 as *"ML Models for Time Series"*. But the actual files are `Lecture6_KalmanFilter`, `lecture08_VECM_DSEB`, `Lecture09_ARCH_DSEB`, and `Lecture10_SVAR`. **The delivered course appears to differ from the printed syllabus from Lecture 6 onward** — see [[00-Index]].

---
**Next:** [[02 - Trend, Seasonality and Decomposition]]
