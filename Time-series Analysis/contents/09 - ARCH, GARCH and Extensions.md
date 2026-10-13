---
subject: Time-series Analysis
chapter: 09
tags: [ds, time-series, arch, garch, volatility, finance, heteroskedasticity]
source: "documents/slides/Lecture09_ARCH_DSEB.ipynb (ARCH, GARCH and Extensions, Dr. Thi Ha Tran); Tsay, *Analysis of Financial Time Series*; Bollerslev (1986)"
---

# ARCH, GARCH and Extensions

Earlier models treated the variance as a constant σ². Here the variance is modelled. For financial returns this is the main point: returns are nearly unpredictable in mean, but their volatility is predictable. (The fat-tailed GDP residuals in [[07 - SARIMA and Vector Autoregression]] were a hint.)

The deck's title slide says "Lecture 10", as does the SVAR deck; the file is `Lecture09`. The notes follow the syllabus order (ARCH before SVAR).

## 📘 Main Knowledge

### Conditional vs unconditional variance

With $y_t=\phi+\varepsilon_t$, $\varepsilon_t=\rho\varepsilon_{t-1}+v_t$ ($|\rho|<1$): the unconditional mean is 0 and the conditional mean $\rho\varepsilon_{t-1}$ varies; the unconditional variance is $\sigma^2_v/(1-\rho^2)$, the conditional variance is constant at $\sigma^2_v$. **AR models persistence in the mean; ARCH models persistence in the variance.**

### ARCH(1)

$$y_t=\mu_0+\varepsilon_t,\qquad\varepsilon_t\mid I_{t-1}\sim N(0,\sigma_t^2),\qquad\sigma_t^2=\alpha_0+\alpha_1\varepsilon_{t-1}^2,\quad\alpha_0>0,\ 0\le\alpha_1<1.$$
Autoregressive conditional heteroskedasticity: the conditional variance depends on past squared shocks. A large shock of either sign raises tomorrow's variance, which produces **volatility clustering** (large changes follow large changes, Mandelbrot 1963). It is symmetric in the sign of the shock.

With $z_t=\varepsilon_t/\sigma_t\sim N(0,1)$ independent of the past: $\mathbb E(\varepsilon_t)=0$ and $\mathbb E(\varepsilon_t^2)=\alpha_0+\alpha_1\mathbb E(\varepsilon_{t-1}^2)$, so
$$\mathbb E(\varepsilon_t^2)=\frac{\alpha_0}{1-\alpha_1}.$$
Conditionally normal, unconditionally a mixture of normals with different variances, hence fat-tailed. Monthly returns of the Nasdaq, All Ordinaries, FTSE and Nikkei show calm and turbulent periods, clustering, and histograms more peaked and fat-tailed than normal; simulating $\sigma_t^2=1+0.8e_{t-1}^2$ against $\sigma_t^2=1$ reproduces this.

**Fourth moment**: $m_4=3\mathbb E[(\sigma_t^2)^2]$ with $(\sigma_t^2)^2=\alpha_0^2+2\alpha_0\alpha_1\varepsilon_{t-1}^2+\alpha_1^2\varepsilon_{t-1}^4$, giving
$$m_4=\frac{3\alpha_0^2(1+\alpha_1)}{(1-\alpha_1)(1-3\alpha_1^2)},\qquad\text{Kurtosis}=3\,\frac{1-\alpha_1^2}{1-3\alpha_1^2}>3.$$
It exists only if $\alpha_1<1/\sqrt3=0.577$, a stronger condition than for the variance: with $\alpha_1=0.7$ the variance is finite but the kurtosis infinite. Fat tails come from mixing over variances, not from fat-tailed $z_t$.

### Testing for ARCH (Engle's LM test)

1. Estimate the mean equation; keep residuals $\hat e_t$.
2. Regress $\hat\varepsilon_t^2=\gamma_0+\gamma_1\hat\varepsilon_{t-1}^2+\dots+\gamma_q\hat\varepsilon_{t-q}^2+v_t$; $H_0$: all $\gamma_i=0$ (no ARCH).
3. $LM=(T-q)R^2\sim\chi^2_q$; reject if large. (The same $nR^2$ construction as Breusch–Pagan.)

### Estimating ARCH(m)

With $\eta_t=\varepsilon_t^2-\sigma_t^2$ (mean zero, uncorrelated), $\varepsilon_t^2=\alpha_0+\alpha_1\varepsilon_{t-1}^2+\dots+\alpha_m\varepsilon_{t-m}^2+\eta_t$: an AR(m) in squared shocks, so the PACF of $\varepsilon_t^2$ cuts off at $m$ ([[05 - ACF, PACF and the Box-Jenkins Methodology]]). $\eta_t$ is not i.i.d., so its bands are only a guide.

Ignoring the first $m$ observations, the conditional log-likelihood is
$$\ln L_c=-\frac{n-m}2\ln2\pi-\frac12\sum_{t=m+1}^n\ln\sigma_t^2-\frac12\sum_{t=m+1}^n\frac{\varepsilon_t^2}{\sigma_t^2}.$$
The second term penalizes large variances, the third small variances when shocks are large; the same prediction-error form as the Kalman likelihood ([[06 - The Kalman Filter and State-Space Models]]). Starting values $\sigma_0^2$: the sample variance (Bollerslev 1986); 0 or $\operatorname{Var}(\varepsilon_t)$ (Tsay 2005); or exponential smoothing $\sigma^2_t=\lambda\sigma^2_{t-1}+(1-\lambda)\varepsilon^2_{t-1}$ from the sample variance (software). In large samples the choice matters little.

### Forecasting volatility

**Dynamic** (true forecasts): $\hat\sigma^2_{h+s}=\alpha_0+\sum_i\alpha_i\hat\varepsilon^2_{h+s-i}$, using actual $\varepsilon^2$ for observed periods and $\hat\varepsilon^2=\hat\sigma^2$ for future ones (since $\mathbb E z^2=1$). **Static**: always uses actual past shocks, so it gives one-step fitted values in sample; don't judge forecasting ability with it.

**BYD Lighting** (lecture): the auxiliary regression $\hat\varepsilon_t^2=0.908+0.353\hat\varepsilon_{t-1}^2$, $R^2=0.124$, gives $LM=61.876$ (so $T-q=499$) against 3.84: ARCH(1) effects. Estimates: $\hat r_t=1.063$, $\hat\sigma^2_t=0.642+0.569\hat\varepsilon^2_{t-1}$ (significant). Forecast $\hat r_{t+1}=1.063$, $\hat\sigma^2_{t+1}=0.642+0.569(r_t-1.063)^2$: constant mean forecast, time-varying volatility. Derived: unconditional variance $0.642/0.431=1.490$; kurtosis $3(1-0.569^2)/(1-3\cdot0.569^2)=70.6$, with $\alpha_1$ just below 0.577, so fourth-moment-based inference is fragile.

```python
from arch import arch_model
res = arch_model(r, mean="Constant", vol="ARCH", p=1).fit(disp="off")
mu, omega, a1 = res.params["mu"], res.params["omega"], res.params["alpha[1]"]
h_next = omega + a1 * (r.iloc[-1] - mu) ** 2
```

### GARCH

ARCH(q) needs many lags because volatility is persistent; GARCH captures long lags with few parameters.
$$r_t=\mu_t+\varepsilon_t,\quad\varepsilon_t=\sigma_tz_t,\quad\sigma_t^2=\alpha_0+\sum_{i=1}^m\alpha_i\varepsilon_{t-i}^2+\sum_{j=1}^s\beta_j\sigma_{t-j}^2,$$
with $\alpha_0>0$, $\alpha_i,\beta_j\ge0$, $\sum(\alpha_i+\beta_i)<1$ (positive and finite variance). Volatility depends on past shocks and past volatility.

**GARCH(1,1)**: $\sigma_t^2=\delta+\alpha_1\varepsilon^2_{t-1}+\beta_1\sigma^2_{t-1}$; δ sets the baseline, $\alpha_1$ the reaction to news, $\beta_1$ persistence. Back-substitution makes it an ARCH(∞) with weights $\alpha_1\beta_1^j$. $\alpha_1+\beta_1\ge1$ is the IGARCH boundary.

**ARMA form**: with $\eta_t=\varepsilon_t^2-\sigma_t^2$,
$$\varepsilon_t^2=\alpha_0+\sum_{i=1}^{\max(m,s)}(\alpha_i+\beta_i)\varepsilon^2_{t-i}+\eta_t-\sum_{j=1}^s\beta_j\eta_{t-j},$$
an ARMA(max(m,s), s) in squared shocks, with unconditional variance $\alpha_0/(1-\sum(\alpha_i+\beta_i))$. For GARCH(1,1), adding and subtracting $\alpha_1\sigma^2_{t-1}$ gives $\sigma_t^2=\alpha_0+(\alpha_1+\beta_1)\sigma^2_{t-1}+\alpha_1\nu_{t-1}$: the AR root $\alpha_1+\beta_1$ is the persistence.

**Kurtosis** (normal or symmetric $z_t$), if $1-2\alpha_1^2-(\alpha_1+\beta_1)^2>0$:
$$\text{Kurtosis}=3\,\frac{1-(\alpha_1+\beta_1)^2}{1-(\alpha_1+\beta_1)^2-2\alpha_1^2}>3.$$

**Estimation and diagnostics**: MLE with starting values; check $\beta_j\ge0$ and $\sum(\alpha_i+\beta_i)<1$; Nyblom test for parameter stability. Ljung–Box on standardized residuals $\hat z_t=\hat\varepsilon_t/\hat\sigma_t$ (mean equation) and on $\hat z_t^2$ (variance equation).

| Persistence $\alpha+\beta$ | Character | Implications |
|---|---|---|
| ≈ 1 | long memory, slow decay | high systemic risk; long horizons (typical of emerging markets) |
| ≪ 1 | transitory | more stable, short-term trading (developed markets) |
| ≥ 1 | non-stationary, permanent shocks | bubbles, crises; standard GARCH may fail (IGARCH) |

Typical estimates: 0.85–0.99.

**Forecasting GARCH(1,1)**: $\hat\sigma^2_h(1)=\alpha_0+\alpha_1\varepsilon_h^2+\beta_1\sigma_h^2$; then the MA term has zero expectation and $\hat\sigma^2_h(k)=\alpha_0+(\alpha_1+\beta_1)\hat\sigma^2_h(k-1)$, so
$$\hat\sigma^2_h(k)=\bar\sigma^2+(\alpha_1+\beta_1)^{k-1}\big[\hat\sigma^2_h(1)-\bar\sigma^2\big],\qquad\bar\sigma^2=\frac{\alpha_0}{1-\alpha_1-\beta_1}.$$
Mean reversion like an AR(1) forecast, at rate $\alpha_1+\beta_1$; half-life $\ln0.5/\ln(\alpha_1+\beta_1)$ (0.95 → 13.5 periods).

**BYD, GARCH(1,1)** (lecture): $\hat r_t=1.049$, $\hat\sigma^2_t=0.401+0.492\hat\varepsilon^2_{t-1}+0.238\hat\sigma^2_{t-1}$; the significant $\beta$ favours GARCH over ARCH. Derived: persistence 0.730 (half-life 2.2 periods, transitory); long-run variance $0.401/0.270=1.485$, consistent with the ARCH fit's 1.490. Unusually large α and small β (equity fits usually have α ≈ 0.05–0.15, β ≈ 0.8–0.9): strong reaction, fast forgetting. The kurtosis condition fails, $1-2(0.492)^2-0.730^2=-0.017<0$: infinite fourth moment.

### Asymmetry

GARCH uses $\varepsilon^2$, so it ignores the sign. In many markets bad news raises volatility more than good news of the same size (**leverage effect**).

**GJR / T-GARCH**:
$$\sigma_t^2=\alpha_0+(\alpha_1+\gamma_1d_{t-1})\varepsilon^2_{t-1}+\beta_1\sigma^2_{t-1},\qquad d_{t-1}=\mathbb 1(\varepsilon_{t-1}<0).$$
Good news has effect $\alpha_1$, bad news $\alpha_1+\gamma_1$; $\gamma_1>0$ is the leverage effect, and $H_0:\gamma_1=0$ tests asymmetry. A common stationarity condition: $\alpha_1+\gamma_1/2+\beta_1<1$ (bad news about half the time). General form $\sum(\alpha_i+\gamma_id_{t-i})\varepsilon^2_{t-i}+\sum\beta_j\sigma^2_{t-j}$; estimated by MLE; used in risk management and option pricing.
```python
res_t = arch_model(r, mean="Constant", vol="GARCH", p=1, o=1, q=1).fit(disp="off")
good, bad = res_t.params["alpha[1]"], res_t.params["alpha[1]"] + res_t.params["gamma[1]"]
```

**EGARCH** models the log variance:
$$\ln\sigma_t^2=\delta+\beta_1\ln\sigma^2_{t-1}+\alpha\Big|\frac{\varepsilon_{t-1}}{\sigma_{t-1}}\Big|+\gamma\frac{\varepsilon_{t-1}}{\sigma_{t-1}}.$$
β is persistence, α the size effect, γ the sign effect. The variance is positive automatically, so no parameter constraints are needed. $\gamma<0$ means negative shocks raise volatility more (opposite sign convention to GJR's $\gamma_1>0$).

**GARCH-in-mean**: $y_t=\beta_0+\theta\sigma_t^2+\varepsilon_t$ with GARCH variance; θ > 0 means higher risk, higher expected return (a direct test of the risk–return trade-off).

| Model | Adds | Captures |
|---|---|---|
| ARCH(q) | $\sum\alpha_i\varepsilon^2_{t-i}$ | clustering (many lags) |
| GARCH(m,s) | $\sum\beta_j\sigma^2_{t-j}$ | persistence, parsimoniously |
| IGARCH | $\sum(\alpha+\beta)=1$ | permanent volatility shocks |
| GJR/T-GARCH | $\gamma d_{t-1}\varepsilon^2_{t-1}$ | leverage |
| EGARCH | log form, signed shock | leverage, no constraints |
| GARCH-M | $\sigma_t^2$ in the mean | risk–return trade-off |
| FIGARCH | fractional differencing | long memory |

## ✏️ Exercises

The deck has no exercises; these are constructed.

**1.** ARCH(1) with $\alpha_0=0.2$, $\alpha_1=0.5$. (a) Unconditional variance; (b) kurtosis; (c) $\sigma_t^2$ and a 95% interval for $\varepsilon_t$ if $\varepsilon_{t-1}=1.5$; (d) when does the fourth moment stop existing?

> [!example]- Solution
> (a) $0.2/0.5=0.4$ (sd 0.632). (b) $3(0.75)/0.25=9$ (excess 6). (c) $0.2+0.5(2.25)=1.325$, sd 1.151, interval ±2.26, versus ±1.24 unconditionally: 1.8 times wider after a big shock, which is what VaR needs. (d) $\alpha_1<1/\sqrt3=0.5774$; kurtosis 3.74, 9.0, 22.6, 80.1 at $\alpha_1$ = 0.3, 0.5, 0.55, 0.57, infinite at the boundary, so estimates near it deserve suspicion.

**2.** Daily returns, $T=250$; regressing squared AR(1) residuals on two lags gives $R^2=0.087$. (a) Test for ARCH. (b) Next steps? (c) Why square the residuals?

> [!example]- Solution
> (a) $LM=248(0.087)=21.58>\chi^2_{0.05}(2)=5.99$, $p=2\times10^{-5}$: ARCH effects. Low $R^2$ is normal: $\varepsilon_t^2=\sigma_t^2z_t^2$ is a very noisy proxy ($\operatorname{Var}(z^2)=2$).
> (b) Start with GARCH(1,1); compare with ARCH(1), ARCH(2), GARCH(1,2), GARCH(2,1) by AIC/BIC; test asymmetry with GJR; Ljung–Box on $\hat z_t$ and $\hat z_t^2$; try $t$ innovations if $\hat z_t$ is non-normal; recheck the mean equation (misspecification can mimic ARCH).
> (c) A correct mean equation leaves residuals uncorrelated with their lags, so levels show nothing; squares estimate the variance and are autocorrelated when volatility is. $|\hat e_t|$ also works and is less outlier-sensitive.

**3.** GARCH(1,1) with $\alpha_0=0.00002$, $\alpha_1=0.09$, $\beta_1=0.88$; $\varepsilon_h=-0.03$, $\sigma^2_h=0.0004$. (a) Forecast 1, 2, 10 steps; (b) long-run variance and half-life; (c) annualize; (d) fourth moment?

> [!example]- Solution
> Persistence 0.97.
> (a) $\hat\sigma^2_h(1)=0.00002+0.000081+0.000352=0.000453$; $\hat\sigma^2_h(2)=0.00002+0.97(0.000453)=0.0004594$; $\bar\sigma^2=0.00002/0.03=0.000667$, $\hat\sigma^2_h(10)=0.000667+0.97^9(0.000453-0.000667)=0.000504$: rising towards the long-run level.
> (b) Daily sd 2.58%; half-life $\ln0.5/\ln0.97=22.8$ days.
> (c) ×√252: long-run 41.0%, current 33.8% (calmer than usual). The √252 rule assumes independent days, which GARCH contradicts; it is a convention.
> (d) $1-2(0.0081)-0.9409=0.0429>0$: kurtosis $3(0.0591)/0.0429=4.13$. Small α with large β gives persistence without extreme tails; BYD's large α is the opposite.

**4.** GJR-GARCH(1,1): $\hat\sigma_t^2=0.000015+(0.022+0.118d_{t-1})\varepsilon^2_{t-1}+0.905\sigma^2_{t-1}$, $\hat\gamma_1$ significant. (a) Good vs bad news; (b) stationarity; (c) long-run variance; (d) risk management, and EGARCH?

> [!example]- Solution
> (a) 0.022 vs 0.140: bad news has 6.4 times the effect. A symmetric GARCH would blend them (≈ 0.08) and misjudge both.
> (b) $0.022+0.059+0.905=0.986<1$; half-life 49.2 days; close to IGARCH.
> (c) $0.000015/0.014=0.00107$: daily 3.27%, annualized 52%. With persistence 0.99 it would be 61%: long-run variance is unreliable near 1 (small denominator).
> (d) After a −2% day variance rises by $0.140(0.0004)=5.6\times10^{-5}$, after +2% by $8.8\times10^{-6}$. Symmetric models understate risk after losses; tail measures need asymmetry; high persistence means elevated margins for months; the implied-volatility skew prices this. EGARCH would show γ < 0, needs no constraints, reacts to standardized shocks, and has long-run log variance $\delta/(1-\beta)$.

**5.** Derive the GARCH(1,1) multi-step forecast and explain why the MA term drops out.

> [!example]- Solution
> $\mathbb E_h[\nu_{h+j}]=\mathbb E_h[\sigma^2_{h+j}(z^2_{h+j}-1)]=0$ for $j\ge1$, so only $\nu_h$ (observed) affects the 1-step forecast. With $\lambda=\alpha_1+\beta_1$ and $\alpha_0=(1-\lambda)\bar\sigma^2$, the recursion gives $d_k=\hat\sigma^2_h(k)-\bar\sigma^2=\lambda d_{k-1}$, so $\hat\sigma^2_h(k)=\bar\sigma^2+\lambda^{k-1}[\hat\sigma^2_h(1)-\bar\sigma^2]\to\bar\sigma^2$. It is an AR(1) forecast in disguise. At λ = 1 (IGARCH) it becomes $\hat\sigma^2_h(1)+(k-1)\alpha_0$, with no mean reversion; with $\alpha_0=0$ that is RiskMetrics EWMA (λ = 0.94), criticized for long horizons for exactly this reason.

## 📝 Summary

- AR: persistence in mean; ARCH: persistence in variance.
- ARCH(1): $\sigma_t^2=\alpha_0+\alpha_1\varepsilon^2_{t-1}$; variance $\alpha_0/(1-\alpha_1)$; conditionally normal, unconditionally fat-tailed.
- Kurtosis $3(1-\alpha_1^2)/(1-3\alpha_1^2)$, finite only if $\alpha_1<0.577$.
- LM test $(T-q)R^2\sim\chi^2_q$; PACF of $\varepsilon^2$ suggests the order.
- Conditional MLE; dynamic forecasts use $\hat\varepsilon^2=\hat\sigma^2$.
- GARCH: $\varepsilon_t^2$ is ARMA; persistence $\alpha+\beta$; forecasts revert to $\alpha_0/(1-\alpha-\beta)$.
- GJR ($\gamma>0$) and EGARCH ($\gamma<0$) capture leverage; GARCH-M puts risk in the mean.

## ⚠️ Important Notes

1. Check the fourth-moment condition as well as stationarity (the BYD GARCH fails it).
2. Fix the mean equation before testing for ARCH.
3. Standardized residuals usually stay fat-tailed: use robust (Bollerslev–Wooldridge) standard errors or $t$/skewed-$t$ innovations; don't report normal VaR if $\hat z_t$ fails Jarque–Bera.
4. Read output as: persistence and half-life; long-run variance (annualized); asymmetry ratio; Ljung–Box on $\hat z$, $\hat z^2$; the α:β balance.
5. Low $R^2$ in squared-return regressions reflects the noisy proxy; realized volatility from intraday data is a better target.
6. Unpredictable mean returns and predictable volatility are compatible with market efficiency.

> [!warning] Gaps in the source slides
> - Data files (`returns5.csv`, `byd.csv`) are on a Google Drive path and missing; no outputs were saved. The BYD fits were checked for consistency (long-run variances 1.490 and 1.485) and the derived quantities computed.
> - The GJR model has no numerical example, EGARCH isn't estimated, and IGARCH and FIGARCH appear only on the title slide (see Tsay ch. 3).
> - GARCH diagnostics get one line; standardized-residual tests and non-normal innovations aren't discussed.
> - Inline `<` signs were lost in many conditions ($|\rho|<1$, $0\le\alpha_1<1$, the stationarity sums, the GJR indicator, γ < 0, the fourth-moment condition); reconstructed.
> - Slide 9 writes $E(\varepsilon_t^2)$ for $E(\varepsilon_{t-1}^2)$ in the fourth-moment expansion (equal under stationarity).

**Previous:** [[08 - VECM and Cointegration]] · **Next:** [[10 - Structural Vector Autoregression]]
