---
subject: Time-series Analysis
chapter: 09
tags: [ds, time-series, arch, garch, volatility, finance, heteroskedasticity]
source: "documents/slides/Lecture09_ARCH_DSEB.ipynb (ARCH, GARCH and Extensions, Dr. Thi Ha Tran); Tsay, *Analysis of Financial Time Series*; Bollerslev (1986)"
---

# ARCH, GARCH and Extensions

> [!abstract] Where this sits in the course
> Every model so far has modelled the **conditional mean** and treated the variance as a fixed nuisance parameter $\sigma^2$. **This chapter models the variance itself.** For financial data that is not a refinement — it is the main event: returns are close to unforecastable in the mean but their *volatility* is highly predictable.
>
> The clue was already visible in [[07 - SARIMA and Vector Autoregression]], where the fitted GDP model's residuals failed the Jarque–Bera test with fat tails. ARCH explains where those fat tails come from.

> [!warning] Deck numbering conflict
> The title slide of this deck reads "**LECTURE 10** — ARCH, GARCH and Extensions", but the file is `Lecture09_ARCH_DSEB.ipynb` and the SVAR deck also calls itself Lecture 10. The syllabus order places ARCH/GARCH before SVAR, which is what this vault follows. See [[10 - Structural Vector Autoregression]].

---

## 📘 Main Knowledge

### 1. The idea — conditional vs unconditional variance

#### Starting point: AR errors move the *mean*, not the variance

Take a constant-mean model with an AR(1) error:

$$
y_t = \phi+\varepsilon_t,
\qquad
\varepsilon_t = \rho\varepsilon_{t-1}+v_t,
\qquad |\rho|<1
$$

Repeated substitution gives $\varepsilon_t = v_t+\rho v_{t-1}+\rho^2v_{t-2}+\cdots$, so

$$
\mathbb{E}(\varepsilon_t) = 0
\qquad\text{(unconditional mean)}
$$
$$
\mathbb{E}(\varepsilon_t\mid I_{t-1}) = \rho\varepsilon_{t-1}
\qquad\text{(conditional mean — time-varying)}
$$

Now the variances. **Unconditional:**

$$
\mathbb{E}[(\varepsilon_t-0)^2] = \sigma_v^2(1+\rho^2+\rho^4+\cdots) = \frac{\sigma_v^2}{1-\rho^2}
$$

(cross-products vanish because the $v$'s are uncorrelated; the geometric series sums to $1/(1-\rho^2)$). **Conditional:**

$$
\mathbb{E}\big[(\varepsilon_t-\rho\varepsilon_{t-1})^2\mid I_{t-1}\big] = \mathbb{E}(v_t^2\mid I_{t-1}) = \sigma_v^2
$$

So in the AR(1)-error model:

- the **conditional mean varies** over time,
- the **conditional variance does not**.

> [!important] The one-sentence summary of this chapter
> **AR explains persistence in the *mean*; ARCH explains persistence in the *variance*.** Everything below is the second half of that sentence made precise.

---

### 2. ARCH(1)

Replace the constant conditional variance with a time-varying one:

$$
y_t = \mu_0+\varepsilon_t,
\qquad
\varepsilon_t\mid I_{t-1}\sim N(0,\sigma_t^2)
$$
$$
\boxed{\;\sigma_t^2 = \alpha_0+\alpha_1\varepsilon_{t-1}^2,
\qquad \alpha_0>0,\;\; 0\le\alpha_1<1\;}
$$

**The name decodes as:**

- **heteroskedasticity** — the variance changes over time;
- **autoregressive** — the variance depends on its own lagged information;
- **conditional** — it is the variance *given* the past that moves, not the unconditional one.

**Larger $\varepsilon_{t-1}^2$ ⇒ larger $\sigma_t^2$ ⇒ more volatility today.** The constraint $\alpha_0>0$ keeps the variance positive; $\alpha_1<1$ keeps it from exploding.

> [!important] Why this captures volatility clustering
> The single most robust empirical regularity in finance is that **large changes tend to be followed by large changes, of either sign, and small by small** (Mandelbrot, 1963). ARCH encodes exactly this: because $\varepsilon_{t-1}$ enters *squared*, a big move in either direction raises tomorrow's variance. The model is **symmetric** in the sign of the shock — a limitation that §8 removes.

#### Unconditional moments

Define the **standardised shock**

$$
z_t = \frac{\varepsilon_t}{\sigma_t}\;\Big|\;I_{t-1}\sim N(0,1)
$$

so $\varepsilon_t = \sigma_t z_t$ with $z_t$ independent of $\varepsilon_{t-1}^2$ (which is known at $t-1$).

**Mean:**

$$
\mathbb{E}(\varepsilon_t) = \mathbb{E}(z_t)\,\mathbb{E}\!\left(\sqrt{\alpha_0+\alpha_1\varepsilon_{t-1}^2}\right) = 0
$$

**Variance:** using $\mathbb{E}(z_t^2)=1$ and stationarity,

$$
\mathbb{E}(\varepsilon_t^2) = \mathbb{E}(z_t^2)\,\mathbb{E}(\alpha_0+\alpha_1\varepsilon_{t-1}^2) = \alpha_0+\alpha_1\mathbb{E}(\varepsilon_{t-1}^2)
$$

$$
\boxed{\;\mathbb{E}(\varepsilon_t^2) = \frac{\alpha_0}{1-\alpha_1}\;}
$$

finite when $\alpha_1<1$.

> [!important] Conditionally normal, unconditionally not
> $\varepsilon_t\mid I_{t-1}$ is normal by assumption — but the **unconditional** distribution of $\varepsilon_t$ is a *mixture* of normals with different variances, and a mixture of normals is **not** normal. **ARCH generates fat tails and volatility clustering from a Gaussian building block.** This is the model's most elegant property and the reason it fits financial data so well.

#### The empirical motivation

Monthly returns for Nasdaq, All Ordinaries, FTSE and Nikkei show:

- strong variability over time,
- periods of calm and turbulence,
- **clustering** of large changes.

Their histograms are **more peaked and fatter-tailed** than the normal.

Comparing simulations of $\sigma_t^2=1$ (constant) against $\sigma_t^2 = 1+0.8e_{t-1}^2$ (ARCH), the second produces visible volatility clustering and an unconditional distribution with a higher peak and fatter tails. **Big shocks today tend to create high volatility tomorrow.**

---

### 3. The fourth moment and kurtosis

Fat tails can be quantified. With $\varepsilon_t = \sigma_tz_t$, $z_t\sim N(0,1)$, $\sigma_t^2 = \alpha_0+\alpha_1\varepsilon_{t-1}^2$:

$$
\varepsilon_t^4 = (\sigma_t^2)^2z_t^4
\qquad\Longrightarrow\qquad
m_4 = \mathbb{E}(\varepsilon_t^4) = \mathbb{E}[(\sigma_t^2)^2]\,\mathbb{E}(z_t^4)
$$

For a standard normal, $\mathbb{E}(z_t^4)=3$, so $m_4 = 3\,\mathbb{E}[(\sigma_t^2)^2]$. Expanding:

$$
(\sigma_t^2)^2 = (\alpha_0+\alpha_1\varepsilon_{t-1}^2)^2 = \alpha_0^2+2\alpha_0\alpha_1\varepsilon_{t-1}^2+\alpha_1^2\varepsilon_{t-1}^4
$$

Taking expectations and using $\mathbb{E}(\varepsilon^2) = \alpha_0/(1-\alpha_1)$, $\mathbb{E}(\varepsilon^4)=m_4$:

$$
m_4 = 3\left[\alpha_0^2+2\alpha_0\alpha_1\frac{\alpha_0}{1-\alpha_1}+\alpha_1^2m_4\right]
$$

$$
m_4(1-3\alpha_1^2) = 3\alpha_0^2\left[1+\frac{2\alpha_1}{1-\alpha_1}\right] = \frac{3\alpha_0^2(1+\alpha_1)}{1-\alpha_1}
$$

$$
\boxed{\;m_4 = \frac{3\alpha_0^2(1+\alpha_1)}{(1-\alpha_1)(1-3\alpha_1^2)}\;}
$$

**Kurtosis.** Dividing by $[\mathrm{Var}(\varepsilon_t)]^2 = \alpha_0^2/(1-\alpha_1)^2$:

$$
\boxed{\;\text{Kurtosis} = \frac{\mathbb{E}(\varepsilon_t^4)}{[\mathrm{Var}(\varepsilon_t)]^2} = 3\,\frac{1-\alpha_1^2}{1-3\alpha_1^2} \;>\; 3\;}
$$

**Kurtosis above 3 means heavier tails than the normal** — the defining feature of financial returns.

> [!warning] The fourth moment requires a *stronger* condition than the second
> $m_4$ is finite only if $1-3\alpha_1^2>0$, i.e.
> $$\alpha_1 < \frac{1}{\sqrt3}\approx 0.577$$
> whereas the *variance* only needs $\alpha_1<1$. So an ARCH(1) with $\alpha_1 = 0.7$ has a perfectly finite variance but **infinite kurtosis** — the sample kurtosis will not converge as $T$ grows, and any standard error relying on fourth moments is invalid. For ARCH($m$), stronger restrictions on the $\alpha_i$ are needed still.
>
> This matters in practice: estimated $\alpha_1$ near 0.577 sits right at the boundary, and the estimate below in §6 is $0.569$ — a hair under it.

**Key idea: ARCH generates heavy tails even when $z_t$ is normal.** The fat tails come from the *mixing over variances*, not from a fat-tailed innovation.

---

### 4. Testing for ARCH effects

**Engle's LM test.**

**Step 1.** Estimate the mean equation and save the residuals $\hat e_t$.

**Step 2.** Square them and run the auxiliary regression

$$
\hat\varepsilon_t^2 = \gamma_0+\gamma_1\varepsilon_{t-1}^2+v_t
\qquad
\big(\text{or with } q \text{ lags for ARCH}(q)\big)
$$

$$
H_0:\gamma_1 = 0
\qquad\text{vs}\qquad
H_1:\gamma_1\neq0
$$

Under $H_0$ there are no ARCH effects: lagged squared residuals do not explain current squared residuals, and $R^2$ is low.

**Step 3.** The test statistic is

$$
\boxed{\;LM = (T-q)R^2\;\sim\;\chi^2_q\;}
$$

Reject $H_0$ if it exceeds the critical value.

> [!note] The same $nR^2$ trick as everywhere else
> This is the standard Lagrange multiplier construction: run an auxiliary regression of the residual-based quantity on the candidate explanators and scale the $R^2$ by the sample size. Breusch–Pagan for ordinary heteroskedasticity has exactly this form. Compare [[Mathematical Statistics/contents/07 - Hypothesis Testing - One Sample|LM tests]].

---

### 5. Estimating an ARCH($m$)

#### Choosing the order

If ARCH effects are significant, use the **PACF of $\varepsilon_t^2$** to choose the order. The reason is worth spelling out. Since $\varepsilon_t^2$ is an unbiased estimator of $\sigma_t^2$, define

$$
\eta_t = \varepsilon_t^2-\sigma_t^2,
\qquad
\mathbb{E}[\eta_t]=0,\;\; \eta_t \text{ uncorrelated}
$$

Substituting $\sigma_t^2 = \alpha_0+\sum_{i=1}^m\alpha_i\varepsilon_{t-i}^2$:

$$
\varepsilon_t^2 = \alpha_0+\alpha_1\varepsilon_{t-1}^2+\cdots+\alpha_m\varepsilon_{t-m}^2+\eta_t
$$

**This is exactly an AR($m$) in $\varepsilon_t^2$** — so the identification rules of [[05 - ACF, PACF and the Box-Jenkins Methodology]] apply: the **PACF of the squared residuals cuts off at lag $m$**.

> [!warning] But $\eta_t$ is not i.i.d.
> The disturbance $\eta_t = \varepsilon_t^2-\sigma_t^2$ is uncorrelated but **not** independent, and it is heteroskedastic by construction. So the PACF is a **useful guide**, not a valid inferential tool — the usual $\pm2/\sqrt n$ bands are only approximate here. Use it to shortlist, then decide with information criteria and diagnostics.

#### Maximum likelihood

If $\varepsilon_t$ is conditionally normal, the likelihood factors as

$$
L = f(\varepsilon_1,\ldots,\varepsilon_n\mid\alpha) = \prod_{t=m+1}^n f(\varepsilon_t\mid F_{t-1})\cdot f(\varepsilon_1,\ldots,\varepsilon_m\mid\alpha)
$$

In large samples the joint density of the initial $m$ observations is **ignored**, giving the **conditional** likelihood

$$
L_c = \prod_{t=m+1}^n\frac{1}{\sqrt{2\pi\sigma_t^2}}\exp\left(-\frac{\varepsilon_t^2}{2\sigma_t^2}\right)
$$

$$
\boxed{\;\ln L_c = -\frac{n-m}2\ln(2\pi)-\frac12\sum_{t=m+1}^n\ln(\sigma_t^2)-\frac12\sum_{t=m+1}^n\frac{\varepsilon_t^2}{\sigma_t^2}\;}
$$

> [!note] Read the two sums against each other
> The second term $-\tfrac12\sum\ln\sigma_t^2$ **penalises large variances**; the third $-\tfrac12\sum\varepsilon_t^2/\sigma_t^2$ **penalises small variances when the shock is large**. The likelihood is maximised by a $\sigma_t^2$ path that is small in calm periods and large exactly when big shocks occur — which is precisely what "fitting volatility" means. Note also the structural similarity to the Kalman likelihood $-\tfrac12\sum(\log S_t + v_t^2/S_t)$ of [[06 - The Kalman Filter and State-Space Models]]: same prediction-error decomposition, with $\sigma_t^2$ playing the role of $S_t$.

#### Initial values for the variance

Computing $\sigma_t^2$ recursively needs a starting value $\sigma_0^2$. Common choices:

| Source | Rule |
|---|---|
| **Bollerslev (1986)** | $\sigma_0^2 = \frac1T\sum_{t=1}^T\varepsilon_t^2$ — the sample variance |
| **Tsay (2005)** | $\sigma_0^2=0$, or $\sigma_0^2 = \mathrm{Var}(\varepsilon_t)$ |
| **Software** | Exponential smoothing $\sigma_t^2 = \lambda\sigma_{t-1}^2+(1-\lambda)\varepsilon_{t-1}^2$, initialised at the sample variance |

with $T = n-p$ the number of usable observations. **In large samples, different initialisation rules usually have only a small effect** — the same start-up issue as exact vs conditional MLE in [[06 - The Kalman Filter and State-Space Models]].

---

### 6. Forecasting volatility

#### Dynamic (multi-step) forecasting

Recursive, exactly like AR forecasting. With forecast origin $h$:

$$
\hat\sigma_{h+1}^2 = \alpha_0+\alpha_1\varepsilon_h^2+\alpha_2\varepsilon_{h-1}^2+\cdots+\alpha_m\varepsilon_{h-m+1}^2
$$

$$
\hat\sigma_{h+2}^2 = \alpha_0+\alpha_1\hat\varepsilon_{h+1}^2+\alpha_2\varepsilon_h^2+\cdots+\alpha_m\varepsilon_{h-m+2}^2
$$

where **$\hat\varepsilon_{h+1}^2 = \hat\sigma_{h+1}^2$** — because $\mathbb{E}[z_{h+1}^2]=1$, so the expected squared future shock *is* the forecast variance. Generally:

$$
\hat\sigma_{h+s}^2 = \alpha_0+\sum_{i=1}^m\alpha_i\hat\varepsilon_{h+s-i}^2,
\qquad
\hat\varepsilon_{h+s-i}^2 = \begin{cases}
\varepsilon_{h+s-i}^2, & h+s-i\le h\\
\hat\sigma_{h+s-i}^2, & \text{otherwise}
\end{cases}
$$

**Use actual squared shocks for periods already observed; replace future ones with forecast variances.** Identical in structure to the ARMA forecast recursion of [[04 - AR, MA and ARMA Processes]] — "use the data when you have it, the forecast when you don't".

#### Static forecasting

Static forecasting uses the **actual past shocks whenever available**:

$$
\hat\sigma_t^2 = \alpha_0+\sum_{i=1}^m\alpha_i\varepsilon_{t-i}^2,
\qquad t=1,\ldots,T+1
$$

All lagged squared shocks in the sample are replaced by their observed values. **Static forecasts are more accurate inside the sample** because they use realised information — but they are one-step-ahead only, and beyond the sample end there are no actual shocks left, so you must switch to the dynamic recursion.

**In short: static forecasting produces fitted values; dynamic forecasting produces genuine future predictions.** Never evaluate a model's forecasting ability on static forecasts.

> [!example] BYD Lighting — a complete ARCH(1) application
> **Testing.** The auxiliary regression gives
> $$\hat\varepsilon_t^2 = 0.908+0.353\,\hat\varepsilon_{t-1}^2,\qquad R^2 = 0.124$$
> $$LM = (T-q)R^2 = 61.876$$
> Against $\chi^2_{0.05}(1)=3.84$ this is overwhelming — **reject $H_0$: the data show ARCH(1) effects.** (Working backwards, $T-q = 61.876/0.124 = 499$, so the sample is about 500 observations.)
>
> **Estimation.**
> $$\hat r_t = \hat\beta_0 = 1.063
> \qquad
> \hat\sigma_t^2 = 0.642+0.569\,\hat\varepsilon_{t-1}^2$$
> The coefficient on $\hat\varepsilon_{t-1}^2$ is significant, so ARCH(1) captures the volatility dependence.
>
> **Forecast.**
> $$\hat r_{t+1} = 1.063,
> \qquad
> \hat\sigma_{t+1}^2 = 0.642+0.569(r_t-1.063)^2$$
> **The forecast return is constant but the forecast volatility changes over time** — the essential ARCH picture. All the predictability is in the second moment.
>
> **Two things the slides don't compute:**
> - Unconditional variance $= \dfrac{0.642}{1-0.569} = \mathbf{1.490}$, so unconditional volatility $\approx1.22$.
> - **Kurtosis** $= 3\dfrac{1-0.569^2}{1-3(0.569)^2} = \dfrac{2.0287}{0.0287} \approx \mathbf{70.6}$ — colossal, against 3 for a normal. And note $\alpha_1 = 0.569$ is **barely** below the $1/\sqrt3 = 0.577$ threshold: a slightly larger estimate and the fourth moment would not exist at all. Treat any kurtosis-based inference on this fit with great caution.

```python
from arch import arch_model

# ARCH(1) by maximum likelihood
res = arch_model(r, mean="Constant", vol="ARCH", p=1).fit(disp="off")
print(res.summary())

mu, omega, a1 = res.params["mu"], res.params["omega"], res.params["alpha[1]"]
h_next = omega + a1 * (r.iloc[-1] - mu)**2      # one-step-ahead variance
```

---

### 7. GARCH

#### Why generalise

**ARCH($q$)** simply adds lags:

$$
\sigma_t^2 = \alpha_0+\alpha_1\varepsilon_{t-1}^2+\cdots+\alpha_q\varepsilon_{t-q}^2
$$

Volatility today depends on shocks over the past $q$ periods, and testing/estimation/forecasting extend directly. **But if $q$ is large, too many parameters reduce precision** — and empirically $q$ *does* need to be large, because volatility is persistent over many months.

**This motivates GARCH: capture long-lag behaviour with few parameters** — exactly the parsimony argument that motivated ARMA over high-order AR in [[04 - AR, MA and ARMA Processes]].

#### GARCH($m,s$)

$$
r_t = \mu_t+\varepsilon_t,
\qquad
\varepsilon_t = \sigma_tz_t,
\qquad
\{z_t\}\;iid,\;\;\mathbb{E}(z_t)=0,\;\mathrm{Var}(z_t)=1
$$

$$
\boxed{\;\sigma_t^2 = \alpha_0+\sum_{i=1}^m\alpha_i\varepsilon_{t-i}^2+\sum_{j=1}^s\beta_j\sigma_{t-j}^2\;}
$$

**Parameter restrictions:**

$$
\alpha_0>0,
\qquad
\alpha_i\ge0,\;\;\beta_j\ge0,
\qquad
\sum_{i=1}^{\max(m,s)}(\alpha_i+\beta_i)<1
$$

ensuring a **positive** conditional variance and a **finite** unconditional variance.

**Key idea: volatility depends on both past shocks and past volatility.**

#### GARCH(1,1) — the workhorse

$$
\boxed{\;\sigma_t^2 = \delta+\alpha_1\varepsilon_{t-1}^2+\beta_1\sigma_{t-1}^2\;}
$$

| Term | Meaning |
|---|---|
| $\delta$ (or $\omega$) | Baseline / **long-run** variance level |
| $\alpha_1\varepsilon_{t-1}^2$ | Effect of the recent shock — "**news**" |
| $\beta_1\sigma_{t-1}^2$ | **Persistence** or momentum in volatility |

Stationarity typically requires $\alpha_1+\beta_1<1$. If $\alpha_1+\beta_1\ge1$, volatility is highly persistent; the boundary case is **IGARCH**.

**GARCH is popular because it mimics long-lag ARCH behaviour with only a few parameters.** Indeed, back-substituting $\sigma_{t-1}^2$ repeatedly shows GARCH(1,1) is an ARCH($\infty$) with **geometrically declining weights** $\alpha_1\beta_1^{j}$ — three parameters standing in for an infinite lag structure.

#### The ARMA representation

Define the innovation

$$
\eta_t = \varepsilon_t^2-\sigma_t^2,
\qquad
\mathbb{E}(\eta_t)=0,\;\;\mathrm{Cov}(\eta_t,\eta_{t-j})=0
$$

(uncorrelated, though **not** i.i.d.). Substituting $\sigma_t^2 = \varepsilon_t^2-\eta_t$ into the variance equation:

$$
\boxed{\;\varepsilon_t^2 = \alpha_0+\sum_{i=1}^{\max(m,s)}(\alpha_i+\beta_i)\varepsilon_{t-i}^2+\eta_t-\sum_{j=1}^s\beta_j\eta_{t-j}\;}
$$

**$\varepsilon_t^2$ follows an ARMA$(\max(m,s),\,s)$ process.** Everything you know about ARMA transfers directly to squared returns.

**Unconditional variance:**

$$
\mathbb{E}(\varepsilon_t^2) = \frac{\alpha_0}{1-\sum_{i=1}^{\max(m,s)}(\alpha_i+\beta_i)}
$$

— the same $\mu = \tfrac{c}{1-\sum\phi}$ formula as any AR, applied to squares.

**Interpretation:** $\alpha$ is the impact of shocks (news); $\beta$ is the persistence of volatility.

##### The GARCH(1,1) → ARMA(1,1) derivation

Start from $\sigma_t^2 = \alpha_0+\alpha_1\varepsilon_{t-1}^2+\beta_1\sigma_{t-1}^2$ and add and subtract $\alpha_1\sigma_{t-1}^2$:

$$
\alpha_1\varepsilon_{t-1}^2 = \alpha_1(\varepsilon_{t-1}^2-\sigma_{t-1}^2)+\alpha_1\sigma_{t-1}^2
$$

$$
\sigma_t^2 = \alpha_0+\alpha_1(\varepsilon_{t-1}^2-\sigma_{t-1}^2)+\alpha_1\sigma_{t-1}^2+\beta_1\sigma_{t-1}^2
$$

$$
\sigma_t^2 = \alpha_0+(\alpha_1+\beta_1)\sigma_{t-1}^2+\alpha_1\nu_{t-1},
\qquad \nu_t = \varepsilon_t^2-\sigma_t^2
$$

In lag-operator form:

$$
[1-(\alpha_1+\beta_1)L]\,\sigma_t^2 = \alpha_0+\alpha_1\nu_{t-1}
\qquad\Longrightarrow\qquad
\sigma_t^2\sim\mathrm{ARMA}(1,1)
$$

with AR part $(\alpha_1+\beta_1)\sigma_{t-1}^2$ and MA part $\nu_{t-1}$. The **AR root is $\alpha_1+\beta_1$** — which is why that sum is *the* persistence measure.

#### Kurtosis in GARCH(1,1)

If $\{z_t\}$ is normal or symmetric and

$$
1-2\alpha_1^2-(\alpha_1+\beta_1)^2 > 0
$$

then

$$
\boxed{\;\text{Kurtosis}(\varepsilon_t) = 3\cdot\frac{1-(\alpha_1+\beta_1)^2}{1-(\alpha_1+\beta_1)^2-2\alpha_1^2} \;>\;3\;}
$$

**Even if $z_t$ is normal, $\varepsilon_t$ is heavy-tailed** because of the time-varying volatility. Applications: financial returns, risk modelling.

#### Estimation and diagnostics

Parameters are estimated by **MLE**, with GARCH adding the variance lags $\beta_j$ relative to ARCH. Initial values must be specified (typically small starting values), and parameters are updated iteratively to convergence.

**Diagnostics** mirror those for ARCH: check the parameter constraints ($\beta_j\ge0$) and the second-order stationarity condition $\sum(\alpha_i+\beta_i)<1$. **Parameter stability** can be checked with the **Nyblom test**.

> [!tip] The essential residual diagnostic
> Apply the **Ljung–Box test to the standardised residuals $\hat z_t = \hat\varepsilon_t/\hat\sigma_t$** and to $\hat z_t^2$:
> - $\hat z_t$ autocorrelated ⇒ the **mean** equation is misspecified.
> - $\hat z_t^2$ autocorrelated ⇒ the **variance** equation is misspecified — increase $m$ or $s$.
> - Both clean ⇒ the model has captured the dynamics.
>
> This is the GARCH analogue of the residual test in [[05 - ACF, PACF and the Box-Jenkins Methodology]], and it is the step most often skipped.

#### Reading persistence

$\sum(\alpha_i+\beta_i)$ is the key indicator: **small ⇒ weak reaction and fast decay; large ⇒ strong persistence.** High persistence implies high volatility and instability.

| Case | Character | Implications |
|---|---|---|
| $\alpha+\beta\approx1$ | **Strong persistence** (long memory); shocks decay very slowly | High systemic risk; requires a long investment horizon. *Typical of emerging markets.* |
| $\alpha+\beta\ll1$ | **Transitory** volatility; fast adjustment | More stable market; suitable for short-term trading. *Typical of developed markets.* |
| $\alpha+\beta\ge1$ | **Non-stationary** volatility; explosive; shocks have permanent effects | Bubbles / financial crises; loss of risk control; **standard GARCH may fail** — consider IGARCH or extensions |

**Typical estimated range: $0.85$–$0.99$.** Always check statistical significance and combine with stationarity tests.

#### Volatility forecasting with GARCH(1,1)

**One step ahead** (static, using the observed shock):

$$
\hat\sigma_h^2(1) = \alpha_0+\alpha_1\varepsilon_h^2+\beta_1\sigma_h^2
$$

**Beyond one step**, using $\mathbb{E}[\nu_{t}] = 0$ so that the MA term drops out:

$$
\hat\sigma_h^2(2) = \alpha_0+(\alpha_1+\beta_1)\hat\sigma_h^2(1),
\qquad\ldots\qquad
\hat\sigma_h^2(k) = \alpha_0+(\alpha_1+\beta_1)\hat\sigma_h^2(k-1)
$$

**Closed form** — solve the linear recursion:

$$
\boxed{\;\hat\sigma_h^2(k) = \frac{\alpha_0}{1-(\alpha_1+\beta_1)}+(\alpha_1+\beta_1)^{k-1}\left[\hat\sigma_h^2(1)-\frac{\alpha_0}{1-(\alpha_1+\beta_1)}\right]\;}
$$

$$
\lim_{k\to\infty}\hat\sigma_h^2(k) = \frac{\alpha_0}{1-(\alpha_1+\beta_1)}
\qquad\text{— the long-run variance}
$$

> [!important] Read the closed form as mean reversion
> The forecast is *long-run variance + a decaying deviation*, converging geometrically at rate $(\alpha_1+\beta_1)$ — structurally identical to the AR(1) forecast $\mu+\phi^s(Y_t-\mu)$ of [[04 - AR, MA and ARMA Processes]], with $\alpha_1+\beta_1$ playing the role of $\phi$.
>
> **Practical reading:** with $\alpha_1+\beta_1 = 0.95$, the half-life of a volatility shock is $\ln0.5/\ln0.95 \approx 13.5$ periods. That single number is usually the most useful thing to report — it says how long a crisis keeps markets jumpy.

> [!example] BYD Lighting, continued — GARCH(1,1)
> $$\hat r_t = 1.049,
> \qquad
> \hat\sigma_t^2 = 0.401+0.492\,\hat\varepsilon_{t-1}^2+0.238\,\hat\sigma_{t-1}^2$$
> The significant coefficient on $\hat\sigma_{t-1}^2$ suggests GARCH fits better than simple ARCH.
>
> **Derived quantities (not in the slides):**
> - **Persistence** $\alpha_1+\beta_1 = 0.492+0.238 = \mathbf{0.730}$ — well below the typical $0.85$–$0.99$ range, so volatility here is comparatively **transitory**. Half-life of a volatility shock: $\ln0.5/\ln0.73 = \mathbf{2.2}$ periods.
> - **Long-run variance** $= \dfrac{0.401}{1-0.730} = \mathbf{1.485}$, essentially identical to the ARCH(1) fit's $1.490$ — a reassuring consistency check across two specifications of the same data.
> - **Note the unusual split.** $\alpha_1 = 0.492$ is large and $\beta_1 = 0.238$ small; most equity GARCH fits have the opposite pattern ($\alpha\approx0.05$–$0.15$, $\beta\approx0.8$–$0.9$). This series reacts violently to news but forgets quickly.
>
> > [!warning] The fourth moment does not exist for this fit
> > The GARCH(1,1) kurtosis condition requires $1-2\alpha_1^2-(\alpha_1+\beta_1)^2>0$. Here
> > $$1-2(0.492)^2-(0.730)^2 = 1-0.4841-0.5329 = \mathbf{-0.0170} < 0$$
> > So $\mathbb{E}(\varepsilon_t^4)=\infty$: the model implies **infinite kurtosis**. The variance is finite and the model is perfectly usable for volatility forecasting, but any quantity depending on fourth moments — sample kurtosis, some standard-error formulas, certain risk measures — is not well defined. Neither the slides nor the summary output flags this. It is a direct consequence of the large $\alpha_1$.

---

### 8. Asymmetry — the leverage effect

Standard GARCH depends only on the **magnitude** of the shock, because $\varepsilon_{t-1}^2$ destroys the sign. It cannot distinguish a positive from a negative shock. But in many financial markets **a negative shock increases future volatility more than a positive shock of the same size** — the **leverage effect**. Bad news and good news do not affect conditional variance equally.

#### T-GARCH / GJR-GARCH

$$
\boxed{\;\sigma_t^2 = \alpha_0+(\alpha_1+\gamma_1d_{t-1})\varepsilon_{t-1}^2+\beta_1\sigma_{t-1}^2\;},
\qquad
d_{t-1} = \begin{cases}1,&\varepsilon_{t-1}<0\\ 0,&\varepsilon_{t-1}\ge0\end{cases}
$$

An **indicator variable** separates bad news from good news:

| News | $d_{t-1}$ | Effect on variance |
|---|---|---|
| **Good** ($\varepsilon_{t-1}\ge0$) | 0 | $\alpha_1\varepsilon_{t-1}^2$ |
| **Bad** ($\varepsilon_{t-1}<0$) | 1 | $(\alpha_1+\gamma_1)\varepsilon_{t-1}^2$ |

- **$\gamma_1>0$**: negative shocks raise volatility more than positive ones — the leverage effect.
- **$\gamma_1 = 0$**: collapses to standard symmetric GARCH(1,1). **Testing $H_0:\gamma_1=0$ is the test for asymmetry.**

A common stationarity condition is

$$
\alpha_1+\frac{\gamma_1}{2}+\beta_1 < 1
$$

(the $\gamma_1/2$ reflects that bad news occurs about half the time under a symmetric distribution).

**General form:**

$$
\sigma_t^2 = \alpha_0+\sum_{i=1}^m(\alpha_i+\gamma_id_{t-i})\varepsilon_{t-i}^2+\sum_{j=1}^s\beta_j\sigma_{t-j}^2
$$

Estimated by **maximum likelihood**, in the same spirit as standard GARCH. **To detect leverage effects, check whether the $\gamma_i$ are statistically significant.** GJR-GARCH is useful in risk management, option pricing, and shock analysis, especially when volatility reacts more strongly to market declines than to increases.

```python
# GJR-GARCH(1,1): o=1 adds the asymmetry term
tgarch = arch_model(r, mean="Constant", vol="GARCH", p=1, o=1, q=1)
res_t = tgarch.fit(disp="off")

good_news = res_t.params["alpha[1]"]
bad_news  = res_t.params["alpha[1]"] + res_t.params["gamma[1]"]
print(f"good news effect: {good_news:.3f}   bad news effect: {bad_news:.3f}")
```

#### EGARCH

**Two problems with standard GARCH** that EGARCH solves at once:

1. Non-negativity constraints on every parameter must be **imposed** during estimation, which complicates optimisation.
2. Only the **magnitude** of the shock matters — no asymmetry.

**EGARCH models the log variance:**

$$
\boxed{\;\ln(\sigma_t^2) = \delta+\beta_1\ln(\sigma_{t-1}^2)+\alpha\left|\frac{\varepsilon_{t-1}}{\sigma_{t-1}}\right|+\gamma\left(\frac{\varepsilon_{t-1}}{\sigma_{t-1}}\right)\;}
$$

| Term | Role |
|---|---|
| $\beta$ | **Persistence** of volatility |
| $\alpha$ | **Size** effect — magnitude of the shock (uses $\lvert\cdot\rvert$) |
| $\gamma$ | **Sign** effect — asymmetry (uses the signed standardised shock) |

**Why the log form works:** $\sigma_t^2 = \exp(\cdot)>0$ automatically, so **no positivity constraints are needed** — the parameters can take any sign, which makes estimation easier and allows genuinely negative asymmetry coefficients.

**If $\gamma<0$, negative shocks increase volatility more** — the leverage effect. If $\gamma=0$, no asymmetry, and the model behaves like GARCH.

**EGARCH captures both the size and the direction of shocks.**

> [!note] Sign conventions differ between GJR and EGARCH
> In **GJR**, the leverage effect means $\gamma_1 > 0$ (bad news *adds* to the variance coefficient). In **EGARCH**, it means $\gamma < 0$ (a negative standardised shock, multiplied by a negative $\gamma$, *raises* $\ln\sigma_t^2$). Same phenomenon, opposite sign — a routine source of confusion when comparing output.

#### GARCH-in-Mean

$$
y_t = \beta_0+\theta\sigma_t^2+\varepsilon_t,
\qquad
\varepsilon_t\mid I_{t-1}\sim N(0,\sigma_t^2),
\qquad
\sigma_t^2 = \delta+\alpha_1\varepsilon_{t-1}^2+\beta_1\sigma_{t-1}^2
$$

Here **risk, measured by $\sigma_t^2$, directly affects the mean return.** If $\theta>0$, higher risk is associated with higher expected return — a direct test of the **risk–return trade-off** that sits at the centre of asset pricing. This is the one model in the family where the variance equation feeds back into the mean equation.

#### The family at a glance

| Model | Variance equation | Captures |
|---|---|---|
| **ARCH($q$)** | $\alpha_0+\sum\alpha_i\varepsilon_{t-i}^2$ | Clustering; needs many lags |
| **GARCH($m,s$)** | $+\sum\beta_j\sigma_{t-j}^2$ | Clustering + persistence, parsimoniously |
| **IGARCH** | $\sum(\alpha+\beta)=1$ | Permanent volatility shocks |
| **GJR / T-GARCH** | $+\gamma d_{t-1}\varepsilon_{t-1}^2$ | **Leverage effect** |
| **EGARCH** | Log form with signed shock | Leverage + no positivity constraints |
| **GARCH-M** | $\sigma_t^2$ enters the **mean** | Risk–return trade-off |
| **FIGARCH** | Fractional differencing | **Long memory** in volatility |

**Summary: ARCH/GARCH models explain volatility clustering, non-normal returns, persistence in variance, and asymmetric responses to shocks.**

---

## ✏️ Exercises

### Exercise 1 — ARCH(1) moments

For an ARCH(1) with $\alpha_0=0.2$, $\alpha_1=0.5$: (a) find the unconditional variance; (b) find the kurtosis; (c) if $\varepsilon_{t-1}=1.5$, what is $\sigma_t^2$ and the 95% interval for $\varepsilon_t$? (d) At what $\alpha_1$ does the fourth moment cease to exist?

> [!example]- Solution
> **(a)** $\mathbb{E}(\varepsilon_t^2) = \dfrac{\alpha_0}{1-\alpha_1} = \dfrac{0.2}{0.5} = \mathbf{0.4}$, so the unconditional standard deviation is $\sqrt{0.4}=0.632$.
>
> **(b)** $\text{Kurtosis} = 3\dfrac{1-\alpha_1^2}{1-3\alpha_1^2} = 3\dfrac{1-0.25}{1-0.75} = 3\dfrac{0.75}{0.25} = \mathbf{9}$.
>
> Three times the normal's kurtosis of 3 — substantially fat-tailed, from a model whose *conditional* distribution is exactly normal. Excess kurtosis is $9-3=6$.
>
> **(c)** $\sigma_t^2 = 0.2+0.5(1.5)^2 = 0.2+1.125 = \mathbf{1.325}$, so $\sigma_t = 1.151$.
>
> Since $\varepsilon_t\mid I_{t-1}\sim N(0,1.325)$, the 95% interval is $\pm1.96(1.151) = \mathbf{[-2.26,\;2.26]}$.
>
> **Compare with the unconditional interval** $\pm1.96(0.632) = [-1.24,\;1.24]$. After a large shock, the conditional interval is **1.8× wider**. That is the entire practical value of ARCH: risk measures like Value-at-Risk should widen after turbulent days, and a constant-variance model cannot do that.
>
> **(d)** The fourth moment requires $1-3\alpha_1^2>0$:
> $$\alpha_1 < \frac{1}{\sqrt3} = \mathbf{0.5774}$$
> With $\alpha_1=0.5$ we are inside but not comfortably. Note how quickly the kurtosis blows up as the boundary approaches:
>
> | $\alpha_1$ | 0.3 | 0.5 | 0.55 | 0.57 | 0.5774 |
> |---|---|---|---|---|---|
> | Kurtosis | 3.74 | 9.0 | 22.6 | 80.1 | $\infty$ |
>
> **The kurtosis is extremely sensitive to $\alpha_1$ near the boundary**, which is why estimates in that region should be treated with suspicion.

---

### Exercise 2 — The LM test for ARCH

Daily returns, $T=250$. An AR(1) mean equation is fitted; the auxiliary regression of $\hat e_t^2$ on its first two lags gives $R^2 = 0.087$. (a) Test for ARCH effects at 5%. (b) What would you do next? (c) Why square the residuals rather than use them directly?

> [!example]- Solution
> **(a)** With $q=2$ lags in the auxiliary regression, $T-q = 250-2 = 248$:
> $$LM = (T-q)R^2 = 248(0.087) = \mathbf{21.58}$$
> Against $\chi^2_{0.05}(2) = 5.99$: $21.58 > 5.99$, so **reject $H_0$** decisively ($p\approx2\times10^{-5}$). **Significant ARCH effects are present.**
>
> Note how a seemingly small $R^2$ of 8.7% produces an overwhelming statistic — with 250 observations, even weak volatility dependence is easily detectable. This is typical: squared-return regressions always have low $R^2$ because $\varepsilon_t^2$ is an extremely noisy proxy for $\sigma_t^2$ (it equals $\sigma_t^2z_t^2$, and $z_t^2$ has variance 2).
>
> **(b) Next steps:**
> 1. **Plot the PACF of $\hat e_t^2$** to gauge the order — but remember its bands are only approximate here (§5).
> 2. **Fit GARCH(1,1) first**, not ARCH($q$). GARCH(1,1) is the near-universal starting point and usually beats any low-order ARCH.
> 3. **Compare** GARCH(1,1) against ARCH(1), ARCH(2), GARCH(1,2), GARCH(2,1) by AIC/BIC.
> 4. **Test for asymmetry** by fitting GJR-GARCH and testing $H_0:\gamma_1=0$. Daily equity returns almost always show a leverage effect.
> 5. **Diagnose**: Ljung–Box on $\hat z_t$ and $\hat z_t^2$; check whether $\hat z_t$ is plausibly normal (if not, refit with a Student-$t$ innovation, `dist="t"` in `arch`).
> 6. **Check the mean equation.** ARCH effects can be *induced* by a misspecified mean, so confirm the AR(1) is adequate before attributing everything to volatility.
>
> **(c) Why square?** Under any correctly specified mean equation, $\hat e_t$ is **uncorrelated** with its own lags — that is what "correctly specified mean" means. So a regression of $\hat e_t$ on $\hat e_{t-1}$ would find nothing regardless of the volatility structure.
>
> But $\hat e_t^2$ is a (very noisy) estimate of $\sigma_t^2$, and it *is* autocorrelated whenever the conditional variance is. **Squaring converts unpredictability-in-mean into predictability-in-variance**, which is the entire point. It is also why $|\hat e_t|$ works as an alternative and is sometimes preferred, being less sensitive to outliers.

---

### Exercise 3 — GARCH(1,1) forecasting

A GARCH(1,1) is fitted with $\hat\alpha_0=0.00002$, $\hat\alpha_1=0.09$, $\hat\beta_1=0.88$. At time $h$, $\varepsilon_h = -0.03$ and $\sigma_h^2 = 0.0004$. (a) Forecast the variance 1, 2 and 10 steps ahead. (b) Find the long-run variance and the half-life. (c) Convert to annualised volatility. (d) Does the fourth moment exist?

> [!example]- Solution
> **Persistence:** $\alpha_1+\beta_1 = 0.09+0.88 = 0.97$ — high, typical of daily equity returns.
>
> **(a) One step** (uses the actual shock):
> $$\hat\sigma_h^2(1) = 0.00002+0.09(-0.03)^2+0.88(0.0004) = 0.00002+0.000081+0.000352 = \mathbf{0.000453}$$
>
> **Two steps** (dynamic — the MA term drops out):
> $$\hat\sigma_h^2(2) = 0.00002+0.97(0.000453) = 0.00002+0.0004394 = \mathbf{0.0004594}$$
>
> **Ten steps** — use the closed form. Long-run variance first:
> $$\bar\sigma^2 = \frac{\alpha_0}{1-(\alpha_1+\beta_1)} = \frac{0.00002}{0.03} = 0.0006667$$
> $$\hat\sigma_h^2(10) = 0.0006667+(0.97)^{9}\big[0.000453-0.0006667\big] = 0.0006667+0.7602(-0.0002137) = \mathbf{0.0005042}$$
>
> The forecast climbs steadily from $0.000453$ toward $0.000667$ — **current volatility is below its long-run level, so the forecast mean-reverts upward.**
>
> **(b) Long-run variance** $\bar\sigma^2 = \mathbf{0.0006667}$, i.e. a daily standard deviation of $\sqrt{0.0006667} = 0.0258 = \mathbf{2.58\%}$.
>
> **Half-life:**
> $$\frac{\ln 0.5}{\ln 0.97} = \frac{-0.6931}{-0.03046} = \mathbf{22.8 \text{ days}}$$
> About a month for half of any volatility shock to dissipate — matching the intuition that markets stay jumpy for weeks after a crisis.
>
> **(c) Annualised** (252 trading days, $\sqrt{252}=15.87$):
> - Long-run: $2.58\%\times15.87 = \mathbf{41.0\%}$ per year.
> - Current one-step: $\sqrt{0.000453} = 2.13\%$ daily $\to \mathbf{33.8\%}$ annualised.
>
> So the market is currently calmer than usual (34% vs 41%) and the model expects it to drift back up. **Annualised volatility is the form practitioners actually quote**, and the $\sqrt{252}$ scaling assumes independent daily returns — which the GARCH model itself contradicts, so treat it as a convention rather than a theorem.
>
> **(d) Fourth moment:** requires $1-2\alpha_1^2-(\alpha_1+\beta_1)^2>0$:
> $$1-2(0.09)^2-(0.97)^2 = 1-0.0162-0.9409 = \mathbf{0.0429} > 0 \;\;✓$$
> It exists — narrowly. Kurtosis:
> $$3\cdot\frac{1-0.9409}{0.0429} = 3\cdot\frac{0.0591}{0.0429} = \mathbf{4.13}$$
> Modest excess kurtosis, plausible for daily returns. **Contrast with the BYD fit in §7, where the same condition failed** because $\alpha_1$ was five times larger. High $\beta$ with low $\alpha$ (this exercise) gives persistence without extreme tails; high $\alpha$ (BYD) gives violent reaction and infinite kurtosis.

---

### Exercise 4 — Interpreting a GJR-GARCH

A GJR-GARCH(1,1) on daily index returns gives
$$\hat\sigma_t^2 = 0.000015+(0.022+0.118\,d_{t-1})\varepsilon_{t-1}^2+0.905\,\sigma_{t-1}^2$$
with $\hat\gamma_1$ significant at 1%. (a) Compare good- and bad-news effects. (b) Check stationarity. (c) Compute the long-run variance. (d) What does this imply for risk management, and how would the answer change under EGARCH?

> [!example]- Solution
> **(a) News impact.**
>
> | News | $d_{t-1}$ | Coefficient on $\varepsilon_{t-1}^2$ |
> |---|---|---|
> | Good ($\varepsilon_{t-1}\ge0$) | 0 | $\alpha_1 = 0.022$ |
> | Bad ($\varepsilon_{t-1}<0$) | 1 | $\alpha_1+\gamma_1 = 0.140$ |
>
> **A negative shock raises next period's variance $0.140/0.022 = \mathbf{6.4}$ times as much as a positive shock of identical magnitude.** A strong, highly significant leverage effect — entirely typical of equity indices, and completely invisible to a symmetric GARCH, which would have estimated a single blended $\alpha\approx0.08$ and mis-forecast volatility in both directions.
>
> **(b) Stationarity.**
> $$\alpha_1+\frac{\gamma_1}{2}+\beta_1 = 0.022+0.059+0.905 = \mathbf{0.986} < 1 \;\;✓$$
> Stationary, but only just. Half-life: $\ln0.5/\ln0.986 = \mathbf{49.2}$ days — roughly a **quarter** for half of a volatility shock to fade. Very persistent, and close enough to 1 that an IGARCH specification would be worth testing.
>
> **(c) Long-run variance.**
> $$\bar\sigma^2 = \frac{0.000015}{1-0.986} = \frac{0.000015}{0.014} = 0.001071$$
> Daily volatility $\sqrt{0.001071} = 3.27\%$; annualised $3.27\%\times15.87 = \mathbf{51.9\%}$.
>
> That is high for a broad index — plausible if the sample spans a crisis. **Note how sensitive this is to the persistence estimate:** if $\alpha+\gamma/2+\beta$ were $0.99$ instead of $0.986$, $\bar\sigma^2$ would be $0.0015$ and annualised volatility $61\%$. **Long-run variance estimates are unreliable when persistence is near 1**, because the denominator $1-\text{persistence}$ is a small difference of large numbers.
>
> **(d) Risk-management implications.**
> 1. **Value-at-Risk must be asymmetric in its updating.** After a $-2\%$ day, tomorrow's variance rises by $0.140(0.0004) = 5.6\times10^{-5}$; after a $+2\%$ day, only $0.9\times10^{-5}$. A symmetric model **understates risk after losses and overstates it after gains** — exactly the wrong way round for a risk manager.
> 2. **Losses cluster more tightly than gains.** Downside risk is worse than a symmetric model implies, so tail measures (VaR, expected shortfall) need the asymmetric specification.
> 3. **The high persistence means slow recovery.** After a crisis, elevated margin requirements and position limits should be expected to persist for months, not days.
> 4. **Option pricing:** the implied volatility skew — out-of-the-money puts trading at higher implied volatility than calls — is the market's pricing of exactly this asymmetry.
>
> **Under EGARCH** the qualitative story would be the same but the parameterisation different:
> $$\ln\sigma_t^2 = \delta+\beta\ln\sigma_{t-1}^2+\alpha|z_{t-1}|+\gamma z_{t-1}$$
> with $\gamma$ estimated **negative** (opposite sign convention to GJR — see §8). Three practical differences: (i) EGARCH needs no positivity constraints, so estimation is better behaved; (ii) it responds to the *standardised* shock $z_{t-1}$, so a $-2\%$ move matters more in calm markets than in turbulent ones — arguably more realistic; (iii) its persistence is read from $\beta$ alone, and the log form makes the long-run variance $\exp(\delta/(1-\beta))$ rather than a ratio, avoiding the near-singular denominator problem of (c).

---

### Exercise 5 — Derive the GARCH(1,1) forecast closed form

Show that the recursion $\hat\sigma_h^2(k) = \alpha_0+(\alpha_1+\beta_1)\hat\sigma_h^2(k-1)$ has the stated closed form, and explain why the MA term vanishes for $k\ge2$.

> [!example]- Solution
> **Why the MA term vanishes.** From §7, $\sigma_t^2 = \alpha_0+(\alpha_1+\beta_1)\sigma_{t-1}^2+\alpha_1\nu_{t-1}$ with $\nu_t = \varepsilon_t^2-\sigma_t^2$. Forecasting from origin $h$:
> $$\mathbb{E}_h[\nu_{h+j}] = \mathbb{E}_h[\varepsilon_{h+j}^2-\sigma_{h+j}^2] = \mathbb{E}_h[\sigma_{h+j}^2(z_{h+j}^2-1)] = 0
> \qquad\text{for } j\ge1$$
> because $\mathbb{E}(z^2)=1$ and $z_{h+j}$ is independent of everything dated $h+j-1$ or earlier. **At $k=1$ the shock $\nu_h$ is observed**, so it contributes; from $k=2$ onward all future $\nu$'s have expectation zero and drop out. This is exactly the "MA($q$) forecasts are $\mu$ beyond horizon $q$" result of [[04 - AR, MA and ARMA Processes]] applied to squared returns.
>
> **Solving the recursion.** Write $\lambda = \alpha_1+\beta_1$ and $\bar\sigma^2 = \dfrac{\alpha_0}{1-\lambda}$, so $\alpha_0 = (1-\lambda)\bar\sigma^2$. Define the deviation $d_k = \hat\sigma_h^2(k)-\bar\sigma^2$. Then
> $$\hat\sigma_h^2(k) = (1-\lambda)\bar\sigma^2+\lambda\hat\sigma_h^2(k-1)$$
> $$\hat\sigma_h^2(k)-\bar\sigma^2 = \lambda\big[\hat\sigma_h^2(k-1)-\bar\sigma^2\big]
> \qquad\Longrightarrow\qquad
> d_k = \lambda\,d_{k-1}$$
> A pure geometric recursion, so $d_k = \lambda^{k-1}d_1$, i.e.
> $$\boxed{\;\hat\sigma_h^2(k) = \bar\sigma^2+\lambda^{k-1}\big[\hat\sigma_h^2(1)-\bar\sigma^2\big]\;}$$
> which is the stated formula. ✓
>
> **Verify the $k=2$ case directly.** $\hat\sigma_h^2(2) = \bar\sigma^2+\lambda[\hat\sigma_h^2(1)-\bar\sigma^2] = (1-\lambda)\bar\sigma^2+\lambda\hat\sigma_h^2(1) = \alpha_0+\lambda\hat\sigma_h^2(1)$ ✓
>
> **Convergence.** Since $\lambda<1$ under stationarity, $\lambda^{k-1}\to0$ and
> $$\lim_{k\to\infty}\hat\sigma_h^2(k) = \bar\sigma^2 = \frac{\alpha_0}{1-\alpha_1-\beta_1}$$
>
> **Three readings worth keeping:**
> 1. **It is an AR(1) in disguise.** The volatility forecast mean-reverts geometrically at rate $\lambda$, exactly like $\hat Y_{t+s|t}=\mu+\phi^s(Y_t-\mu)$.
> 2. **The half-life $\ln0.5/\ln\lambda$ is the single most communicable number** from any GARCH fit.
> 3. **The IGARCH boundary.** As $\lambda\to1$, $\bar\sigma^2\to\infty$ and the closed form degenerates: $\hat\sigma_h^2(k) = \hat\sigma_h^2(1)+(k-1)\alpha_0$, a straight line with no mean reversion at all. **Volatility shocks become permanent.** With $\alpha_0=0$ this is the RiskMetrics EWMA model, which is IGARCH with $\lambda$ fixed at $0.94$ — and its lack of mean reversion is precisely why it is criticised for long-horizon risk forecasting.

---

## 📝 Summary

- **AR models persistence in the mean; ARCH models persistence in the variance.** In an AR(1)-error model the conditional mean varies but the conditional variance is constant $\sigma_v^2$; ARCH makes the variance time-varying.
- **ARCH(1):** $\varepsilon_t\mid I_{t-1}\sim N(0,\sigma_t^2)$ with $\sigma_t^2 = \alpha_0+\alpha_1\varepsilon_{t-1}^2$, $\alpha_0>0$, $0\le\alpha_1<1$. Unconditional variance $\alpha_0/(1-\alpha_1)$. **Conditionally normal but unconditionally fat-tailed** — a mixture of normals is not normal.
- **Kurtosis** $= 3\dfrac{1-\alpha_1^2}{1-3\alpha_1^2}>3$, finite only if $\alpha_1<1/\sqrt3\approx0.577$ — a **stronger** condition than that for the variance.
- **Engle's LM test:** regress $\hat\varepsilon_t^2$ on its lags; $LM = (T-q)R^2\sim\chi^2_q$. Choose the order from the **PACF of $\varepsilon_t^2$** (which follows an AR($m$)), noting its disturbance is not i.i.d.
- **Estimation** by conditional MLE, $\ln L_c = -\tfrac{n-m}2\ln2\pi-\tfrac12\sum\ln\sigma_t^2-\tfrac12\sum\varepsilon_t^2/\sigma_t^2$, with a chosen initial $\sigma_0^2$ (Bollerslev's sample variance, Tsay's alternatives, or exponential smoothing).
- **Forecasting:** dynamic uses $\hat\varepsilon^2 = \hat\sigma^2$ for future periods (since $\mathbb{E}z^2=1$); static uses realised shocks and gives fitted values only.
- **GARCH($m,s$):** $\sigma_t^2 = \alpha_0+\sum\alpha_i\varepsilon_{t-i}^2+\sum\beta_j\sigma_{t-j}^2$ — long-lag ARCH behaviour with few parameters. **$\varepsilon_t^2$ follows an ARMA$(\max(m,s),s)$**, unconditional variance $\alpha_0/(1-\sum(\alpha_i+\beta_i))$.
- **Persistence $\alpha_1+\beta_1$** is the key number: typical range $0.85$–$0.99$; half-life $=\ln0.5/\ln(\alpha_1+\beta_1)$. $\ge1$ ⇒ IGARCH, permanent volatility shocks. Multi-step forecasts mean-revert: $\hat\sigma_h^2(k) = \bar\sigma^2+(\alpha_1+\beta_1)^{k-1}[\hat\sigma_h^2(1)-\bar\sigma^2]$.
- **Asymmetry:** GJR/T-GARCH adds $\gamma_1d_{t-1}\varepsilon_{t-1}^2$ with $d_{t-1}=\mathbb{1}[\varepsilon_{t-1}<0]$, so bad news has effect $\alpha_1+\gamma_1$ and good news $\alpha_1$; $\gamma_1>0$ is the **leverage effect**. **EGARCH** models $\ln\sigma_t^2$ with separate size ($\alpha|z|$) and sign ($\gamma z$) terms, needing no positivity constraints; there the leverage effect means $\gamma<0$.
- **GARCH-in-Mean** puts $\sigma_t^2$ into the mean equation, testing the risk–return trade-off directly.

---

## ⚠️ Important Notes

> [!warning] Check both stationarity *and* fourth-moment conditions
> $\sum(\alpha_i+\beta_i)<1$ gives a finite **variance**. Finite **kurtosis** needs more: $\alpha_1<1/\sqrt3$ for ARCH(1), and $1-2\alpha_1^2-(\alpha_1+\beta_1)^2>0$ for GARCH(1,1). The BYD GARCH fit in §7 **fails** the second condition — a fact neither the slides nor the standard software summary reports. If your analysis touches kurtosis, VaR tail estimates, or fourth-moment standard errors, check it.

> [!warning] Diagnose the mean equation first
> **ARCH effects can be spuriously induced by a misspecified mean.** Omitted structural breaks, outliers, or missing seasonality all produce residuals that look conditionally heteroskedastic. Get the mean equation right, *then* test for ARCH — otherwise you will fit a volatility model to what is really a level problem.

> [!warning] Conditional normality is usually rejected
> Even after fitting GARCH, standardised residuals $\hat z_t$ typically remain fat-tailed. Two responses:
> - **Quasi-MLE**: keep the normal likelihood; the parameter estimates stay **consistent** but the standard errors need a robust (Bollerslev–Wooldridge) correction. `arch` reports these by default.
> - **Refit with $t$ or skewed-$t$ innovations** (`dist="t"`, `dist="skewt"`). Usually a better fit and materially better tail forecasts.
>
> **Never report normal-based VaR from a GARCH fit whose $\hat z_t$ fails Jarque–Bera.**

> [!tip] Read a GARCH output in this order
> 1. **$\alpha+\beta$** — persistence. Convert to a half-life; that is your headline number.
> 2. **$\alpha_0/(1-\alpha-\beta)$** — long-run variance. Annualise it ($\times\sqrt{252}$ for daily) to sanity-check against known market volatility.
> 3. **$\gamma$ (if present)** — asymmetry. Compare $\alpha$ against $\alpha+\gamma$ as a ratio.
> 4. **Ljung–Box on $\hat z_t$ and $\hat z_t^2$** — adequacy. Nothing else matters if these fail.
> 5. **The ratio $\alpha:\beta$** — a large $\alpha$ with small $\beta$ means violent reaction and fast forgetting; the reverse means smooth, persistent volatility. Most equity series are the latter; BYD in §7 is unusually the former.

> [!note] Why $\varepsilon_t^2$ is a terrible proxy for $\sigma_t^2$ — and why it still works
> $\varepsilon_t^2 = \sigma_t^2z_t^2$, and $\mathrm{Var}(z_t^2)=2$ for a standard normal. So the squared return is an **unbiased but extremely noisy** estimate of the conditional variance. This is why:
> - $R^2$ in ARCH regressions is always small (5–15%) even for excellent models;
> - evaluating volatility forecasts against realised squared returns looks discouraging;
> - **realised volatility** from intraday data is a far better target when available.
>
> A low $R^2$ is not evidence against the model — it is a property of the noise in the proxy.

> [!note] Volatility is predictable; returns are not
> The deepest lesson here. Efficient-market arguments imply returns are close to unforecastable in the **mean** — and the fitted models bear this out, with $\hat r_t$ estimated as a constant. But the **variance** is strongly predictable, which is why ARCH/GARCH underpin option pricing, VaR, portfolio optimisation, and margin setting. **Predictability of the second moment is fully consistent with efficiency of the first.**

> [!warning] Gaps in the source slides
> - **The deck numbers itself "LECTURE 10"** while the SVAR deck also claims Lecture 10 and the filename says 09. The syllabus order (ARCH before SVAR) is followed here.
> - **All data files are missing.** `returns5.csv` and `byd.csv` live on a Google Drive path (`/content/drive/MyDrive/DSEB-Time series/Sinhvien/`) and are absent from the vault. **None of the BYD results can be reproduced** — though I verified their internal consistency (the ARCH and GARCH fits imply near-identical unconditional variances, 1.490 vs 1.485, which is a good sign) and derived the kurtosis and persistence quantities the slides omit.
> - **All figures are absent** (no saved cell outputs): the four-market return plots and histograms, the ARCH simulation comparison, and the conditional-variance panels for GARCH and T-GARCH.
> - **The T-GARCH/GJR example has no numbers.** The variance equation is written and interpreted qualitatively, but no estimates are reported — so there is no worked demonstration of a leverage effect anywhere in the deck, despite it being presented as the main motivation for three separate model extensions. Exercise 4 fills the gap with constructed values.
> - **EGARCH is stated but never estimated**, and **IGARCH and FIGARCH appear only on the title slide** — they are named as topics and then never covered at all. If they are examinable, that material must come from elsewhere (Tsay Ch. 3 is the natural source).
> - **Residual diagnostics for GARCH are mentioned in one line** ("check model adequacy, similar to ARCH") with no specifics. The critical test — Ljung–Box on **standardised** residuals and their squares — is never stated. §7's tip is my own addition.
> - **Non-normal innovations are never discussed.** Given that the entire motivation is fat tails, the absence of any mention of $t$-distributed errors or quasi-MLE standard errors is a real omission.
> - **HTML extraction truncated every inline `<`.** Affected: the AR(1) condition ($|\rho| < 1$), the ARCH(1) restriction ($0\le\alpha_1 < 1$), the GARCH stationarity condition ($\sum(\alpha_i+\beta_i) < 1$), the GJR indicator definition ($\varepsilon_{t-1} < 0$), the GJR stationarity condition ($\alpha_1+\gamma_1/2+\beta_1 < 1$), the EGARCH asymmetry condition ($\gamma < 0$), and the fourth-moment existence condition. All reconstructed from context and standard theory.
> - **Slide 9 writes $E(\varepsilon_t^2)$ where it means $E(\varepsilon_{t-1}^2)$** in the fourth-moment expansion — harmless under stationarity, but confusing on first reading.
> - **No exercises are provided.** All five above are my own construction.

---

**Previous:** [[08 - VECM and Cointegration]] · **Next:** [[10 - Structural Vector Autoregression]] · **Index:** [[00-Index]]

#time-series #arch #garch #volatility #finance #leverage-effect #heteroskedasticity
