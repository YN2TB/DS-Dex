---
subject: Time-series Analysis
chapter: 01
tags: [ds, time-series, decomposition, python, datetime, growth-rates]
source: "Lecture01_timeseries.ipynb — Tran Thi Ha, Faculty of Mathematical Economics, NEU (2025)"
---

# What is a Time Series? Data and Visualization

Course: *Time Series Analysis and Forecast in Economics and Finance*, 3 credits. Lecturer: Tran Thi Ha. Assessment: attendance 10%, computer test (Python) 20%, assignment 20%, final exam 50%. Textbooks (all in `documents/`): Auffarth (2021), *Machine Learning for Time-Series with Python*; Peixeiro (2022), *Time Series Forecasting in Python*; Hamilton (1994), *Time Series Analysis*. Course map: [[00-Index]].

## 📘 Main Knowledge

### Time series

A **time series** is a sequence of observations on a variable, ordered in time, at regular or irregular intervals (GDP, inflation, interest rates, stock prices, exchange rates). Time is an essential dimension, observations are not independent across time, and past values often carry information about the future. The i.i.d. assumption behind [[Mathematical Statistics/contents/00-Index|Mathematical Statistics]] fails, so inference has to be rebuilt.

| Type | Meaning | Aggregating to lower frequency |
|---|---|---|
| point in time → **stock** variable | a level at an instant (price, interest rate) | average |
| period → **flow** variable | accumulated over an interval (profit, exports) | sum |

Notation $y_t$; frequencies annual, quarterly, monthly, weekly, daily.

### Lags, differences, growth rates

| Concept | Definition |
|---|---|
| lag | $y_{t-1},y_{t-2},\dots$ |
| difference | $\Delta y_t=y_t-y_{t-1}$ |
| growth rate | $g_t=(y_t-y_{t-1})/y_{t-1}$ |
| log-return | $r_t=\ln(y_t/y_{t-1})\times100\%=(\ln y_t-\ln y_{t-1})\times100\%$ |

Lecture example:

| Year | $y_t$ | $\Delta y_t$ | $g_t$ |
|---|---|---|---|
| 2021 | 100 | – | – |
| 2022 | 120 | 20 | 20% |
| 2023 | 135 | 15 | 12.5% |
| 2024 | 145 | 10 | 7.4% |

The growth rates sum to 39.9%, but total growth 2021–2024 is 45%. The arithmetic average (13.3%) doesn't reflect cumulative growth; the constant rate solves $(1+\bar g)^3=1.45$, so $\bar g\approx13.2\%$. Growth compounds, so average it geometrically: $\bar g=(y_T/y_0)^{1/n}-1$.

**Log-returns** need strictly positive data. They add over time ($\ln(y_T/y_0)=\sum_tr_t$), and they approximate simple returns for small changes ($\ln(1+x)\approx x$). A +50% then −50% simple return leaves you 25% down; in logs these are +40.5% and −69.3%, which correctly don't cancel.

### Components

A series decomposes into **observed = trend + seasonal + residual** (time series decomposition):
- **trend**: long-term direction, sometimes called the level (e.g. earnings rising over years);
- **seasonal**: patterns repeating over a fixed period;
- **residual**: what trend and seasonality don't explain, often treated as noise.

```python
import numpy as np
np.random.seed(42)
n = 120; t = np.arange(n)
trend = 0.05 * t
seasonal = 2 * np.sin(2 * np.pi * t / 12)   # period 12
noise = np.random.normal(0, 0.5, n)
y = trend + seasonal + noise                 # additive
```
The multiplicative form $y_t=T_t\times S_t\times R_t$ is in [[02 - Trend, Seasonality and Decomposition]].

### Time-series analysis

**TSA** analyses time-indexed data to find trend, seasonality and cycles; it is EDA for time series, both descriptive and exploratory. Steps: import and parse dates; find missing values, outliers, anomalies; study distributions; find relationships; identify trend and seasonality; preprocess (log, log-return, differencing, lags); model; train ML models. Use univariate and multivariate, graphical and non-graphical methods. It is iterative: visualization → insight → preprocessing → refinement.

### Time in Python

Libraries: `datetime`, `time`, `calendar`, `dateutil`, `pytz`. Correct timestamps matter for sorting and indexing, resampling (daily → monthly sum/mean), plotting and forecasting. Treat time as a first-class variable, not a string.

| Object | Meaning |
|---|---|
| `date` | calendar date |
| `datetime` | date and time |
| `time` | time of day |
| `timedelta` | duration |

```python
from datetime import date, datetime
from dateutil import parser
import pytz

days_left = (date(2025, 4, 15) - date.today()).days
ts = datetime(2021, 5, 18, 15, 39, 0)
ts.isoformat()                       # '2021-05-18T15:39:00' (ISO 8601)
parser.parse("Aug 2022")             # parse many formats
pytz.timezone("Asia/Ho_Chi_Minh").localize(datetime(2022, 8, 1, 10, 0))
```

### Variables and relationships

Univariate checks: summary statistics, histograms, missing values and outliers, stationarity ([[03 - Stationarity and Difference Equations]]). Measures: mean, standard deviation, standard error, median and percentiles.

```python
df = pd.read_excel("GDP_Trade_Quarterly_Clean.xlsx")
df["date"] = pd.PeriodIndex(df["Year"].astype(str) + df["Quarter"], freq="Q").to_timestamp()
df = df.set_index("date")
df[["GDP_SX", "Exports", "Imports"]].describe()
df.isna().sum()
df[["GDP_SX", "Imports", "Exports"]].corr()
```

With several series, check **collinearity** (predictors correlated with each other; unstable coefficients; drop one or use PCA) and **feature leakage** (a feature reveals the target, e.g. `amount_paid` for `has_paid`; too-good accuracy that fails in deployment).

Two upward-trending series correlate strongly whether or not they are related (**spurious regression**). GDP, exports and imports moving together says little until trends are removed ([[03 - Stationarity and Difference Equations]], [[08 - VECM and Cointegration]]).

## ✏️ Exercises

**1.** Using the growth table (100 → 145 over 2021–2024), show the arithmetic mean of growth rates is wrong and find the correct average.

> [!example]- Solution
> Rates 20%, 12.5%, 7.41%: arithmetic mean 13.30%, sum 39.9%, but total growth is 45%; the 5.1-point gap is compounding. Geometric: $1.45^{1/3}-1=13.19\%$. (At 13.30% for three years you'd reach 145.45, close only by luck.) By AM ≥ GM the arithmetic mean always overstates compound growth, more so with volatile rates: +50% then −40% averages +5%, yet $1.5\times0.6=0.9$, a 10% loss (geometric mean −5.1%). With logs: $\ln1.45/3=0.1239$ and $e^{0.1239}-1=13.19\%$.

**2.** Complete the log-return table (2017–2020: 100, 120, 136, 142) and check additivity.

> [!example]- Solution
> | Year | $y_t$ | Simple | Log |
> |---|---|---|---|
> | 2018 | 120 | 20.00% | 18.23% |
> | 2019 | 136 | 13.33% | 12.52% |
> | 2020 | 142 | 4.41% | 4.32% |
>
> 2020 vs 2017: simple 42.00%, log $\ln1.42=35.07\%$. Logs add: 18.23 + 12.52 + 4.32 = 35.07% (the intermediate terms telescope). Simple returns don't (sum 37.74%); they compound: $1.20\times1.1333\times1.0441=1.42$. Log-returns are below simple returns for gains, and the gap grows with size (4.41 vs 4.32; 20 vs 18.23), so for daily data they are nearly interchangeable.

**3.** Explain stocks vs flows. What goes wrong if you sum a stock?

> [!example]- Solution
> A flow is measured over a period (quarterly profit); a stock at an instant (a closing price). A price of \$100 every day in January sums to \$3,100, which corresponds to nothing; the monthly figure is the average, \$100. Averaging a flow is also wrong: quarterly profits 10, 12, 11, 13 give annual profit 46, not 11.5. Both mistakes run without errors. In pandas aggregate each column appropriately:
> ```python
> df.resample("YE").agg({"exports": "sum", "stock_price": "mean", "interest_rate": "mean"})
> ```
> Some stocks are better summarized by the last value (year-end inventory).

**4.** Why is correlation between trending series misleading, and what should be done?

> [!example]- Solution
> If $x_t=t+\varepsilon_t$ and $y_t=t+\eta_t$ with independent noise, their correlation tends to 1: it measures the shared trend. Regressing one independent random walk on another often gives significant t-statistics and a high $R^2$ (Granger & Newbold 1974), because non-stationary residuals invalidate the usual inference. Instead: test for stationarity (ADF, KPSS); if non-stationary and not cointegrated, work with differences; if cointegrated (a real long-run link, such as GDP and consumption), model levels with a VECM.

**5.** (Advanced) Why does time series violate i.i.d., and what breaks?

> [!example]- Solution
> $\operatorname{Var}(\bar X)=\sigma^2/n$ needs independence. With dependence, $\operatorname{Var}(\bar X)=\frac1{n^2}\big(n\sigma^2+2\sum_{i<j}\operatorname{Cov}(X_i,X_j)\big)$; positive autocorrelation makes it larger, so naive standard errors are too small and tests over-reject. Random train/test splits leak the future, so splits and cross-validation must be chronological. Non-stationarity adds spurious regression. Shuffling destroys the information in the order.
> The upside: dependence is what makes forecasting possible, and AR/MA models ([[04 - AR, MA and ARMA Processes]]) model it directly.

## 📝 Summary

- Time series: ordered, dependent observations; the past informs the future.
- Stocks average, flows sum when aggregating.
- Lag, difference, growth rate, log-return.
- Growth compounds: use geometric means or log-returns.
- Log-returns add over time and need positive data.
- Additive decomposition: trend + seasonal + residual.
- TSA is iterative EDA for time-indexed data.
- Keep dates as `datetime`; ISO 8601; parse with `dateutil`, localize with `pytz`.
- Check collinearity and leakage; correlation between trending series is spurious.

## ⚠️ Important Notes

1. Don't average growth rates arithmetically.
2. Log-returns need strictly positive data.
3. Summing a stock gives a meaningless number.
4. Correlated trends are not evidence of a relationship.
5. Splits must be chronological.
6. Autocorrelation makes naive standard errors too small.
7. String dates sort wrongly ("10/2020" < "2/2020") and can't be differenced.
8. Parse ambiguous dates (03/04/2023) explicitly ([[Data Preparation and Visualization/contents/02 - Loading, Diagnosing, Missing Data and Combining Datasets|Loading Data]]).
9. Time zones matter for intraday data.
10. Centred moving averages and full-sample scaling leak the future.
11. Additive decomposition assumes constant seasonal amplitude.

> [!warning] Gaps in the source material
> - The slides are HTML strings in Colab cells; no outputs were saved, so all plots are lost.
> - `GDP_Trade_Quarterly_Clean.xlsx` is loaded from a Colab path and is not in `documents/`.
> - Slides 12, 13, 16 duplicate the components slide; slides 6 and 17 are code only; slide 11's log-return table is blank for students (completed in Exercise 2).
> - The syllabus (slide 3) lists different topics from Lecture 6 on (ARIMA, ARCH/GARCH, ML for time series) than the notebooks delivered (Kalman filter, VECM, ARCH, SVAR). The notes follow the notebooks ([[00-Index]]).

**Next:** [[02 - Trend, Seasonality and Decomposition]]
