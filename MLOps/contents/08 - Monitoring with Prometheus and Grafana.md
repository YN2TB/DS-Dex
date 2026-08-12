---
subject: MLOps
chapter: 08
tags: [ds, mlops, prometheus, grafana, observability, promql, kubernetes]
source: "MLOps_K8s.pdf (slides 27–39) — MLOps Course, Swinburne Vietnam, April 2026"
---

# Monitoring with Prometheus and Grafana

> [!note] Where this sits in the course
> The second half of the Kubernetes lecture ([[07 - Kubernetes for ML Deployment]]) — the **hands-on observability stack**. The conceptual treatment of drift and monitoring theory is [[10 - Monitoring and Drift]]; this chapter is the tooling that implements it.

## 📘 Main Knowledge

### Why monitor ML models in production

> **The core problem: models decay.** A model trained today degrades silently. **Unlike software bugs, ML failures are gradual and invisible.**

**Real-world failure modes:**

| Failure | What happens |
|---|---|
| **Data drift** | Input distribution shifts |
| **Concept drift** | The relationship $X \to Y$ changes |
| **Label drift** | Target distribution changes |
| **Upstream failures** | Feature pipeline breaks |
| **Infrastructure issues** | Latency spikes, OOM |

The slide's figure shows accuracy declining below a threshold over time, labelled *"silent degradation"* before an alert fires. **The gap between when degradation begins and when an alert fires is exactly what monitoring is trying to shrink.**

Note **label drift** as a third category beyond the two in [[01 - Introduction to MLOps]] — the *target* distribution shifting, e.g. the fraud rate rising from 0.5% to 2%.

### Four dimensions of ML monitoring

| Dimension | What to watch |
|---|---|
| **Infrastructure** | CPU/GPU usage, memory, disk I/O, network throughput, pod restarts |
| **Service** | Request rate (RPS), latency (p50/p95/p99), error rate, throughput |
| **Data Quality** | Feature distributions, missing values, schema violations, statistical drift |
| **Model Quality** | Prediction distribution, confidence scores, accuracy (if labels), business KPIs |

> **Infrastructure *enables* Service, which *feeds* Data Quality, which *reflects* Model Quality.**

That chain is the diagnostic order. A model-quality alert can originate anywhere below it — so when accuracy drops, check upward from infrastructure rather than assuming the model is at fault. It is the discipline of distinguishing drift from bugs ([[01 - Introduction to MLOps]]), expressed as a monitoring hierarchy.

**Only the top two dimensions are standard DevOps.** Data Quality and Model Quality are the MLOps additions — and note **"accuracy (if labels)"**, acknowledging the delayed-label problem.

### Prometheus architecture

```
Kubernetes Pods                      Prometheus                Grafana
  ├── ML Service A  ──/metrics──┐   ┌──────────────┐  PromQL  ┌────────────┐
  ├── ML Service B  ──/metrics──┼──▶│ Scrape+Store │─────────▶│ Dashboards │
  ├── Node Exporter ──/metrics──┤   │    (TSDB)    │          └────────────┘
  └── kube-state    ──/metrics──┘   └──────┬───────┘
                    pull (scrape)          │ alerts        HPA / KEDA
                                           ▼               (custom metrics)
                                     AlertManager ──▶ PagerDuty / Slack
```

**Prometheus uses a *pull* model** — it scrapes `/metrics` endpoints on a schedule rather than receiving pushed data. This matters: the application need only expose a plain HTTP endpoint, and Prometheus discovers targets automatically through Kubernetes. It also means an unreachable service is itself a detectable signal.

Data lands in a **TSDB** (time-series database), queried with **PromQL**, visualised in **Grafana**, alerted through **AlertManager** to PagerDuty or Slack, and — importantly — fed to **HPA/KEDA as custom metrics for autoscaling**.

That last path closes the loop from [[07 - Kubernetes for ML Deployment]]: Prometheus metrics can drive Kubernetes to add replicas when inference latency rises.

### Instrumenting an ML service

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

PREDICTION_COUNTER = Counter(
    'model_predictions_total',
    'Total predictions served',
    ['model_version', 'label'])

LATENCY = Histogram(
    'model_inference_latency_seconds',
    'Inference latency',
    buckets=[.005, .01, .025, .05, .1, .25, .5, 1.0])
```

**The three metric types:**
- **Counter** — monotonically increasing (total predictions). Query with `rate()`, never directly.
- **Histogram** — bucketed observations, enabling **quantiles** (p95 latency).
- **Gauge** — a value that goes up and down (current drift score, queue depth).

**Labels** (`model_version`, `label`) allow slicing — comparing v1 against v2 during a canary deployment, or watching prediction distribution per class.

### PromQL

```promql
# Request rate (RPS)
rate(model_predictions_total[5m])

# p95 inference latency
histogram_quantile(0.95, rate(model_inference_latency_seconds_bucket[5m]))

# Error rate %
100 * rate(model_errors_total[5m]) / rate(model_requests_total[5m])

# Feature drift alert
model_feature_drift_score > 0.2
```

**AlertManager rule:**
```yaml
groups:
  - name: ml-alerts
    rules:
      - alert: High...        # truncated in source
```

`rate()` over a counter converts a cumulative total into a per-second rate, correctly handling counter resets when a pod restarts. `histogram_quantile` over `_bucket` is how p95/p99 are computed — **not by averaging**, since the mean latency hides the tail that users actually experience.

### Grafana dashboard design

**Recommended panel layout:**

| Row | Panels |
|---|---|
| **Top — stat tiles** | RPS · p95 latency · Error % · Drift |
| **Middle** | Predictions/sec · Latency p50/p95/p99 |
| **Lower** | Feature Drift Scores · Prediction Distribution |
| **Bottom** | Error Rate & Alerts |

The layout reads top-down from *"is it up?"* to *"is it right?"* — the four dimensions in order.

**Provisioning via ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards
data:
  ml-monitoring.json: |
    {
      "title": "ML Model Monitoring",
      "panels": [
        { "type": "stat", "title": "RPS",
          "targets": [{ "expr": "sum(rate(model_predic..." }] }
      ]
    }
```

Provisioning dashboards as ConfigMaps rather than clicking them together in the UI makes them **version-controlled and reproducible** — the same argument as declarative manifests in [[07 - Kubernetes for ML Deployment]].

### Installing the stack with Helm

> **Helm is the package manager for Kubernetes.**

```bash
helm --help
helm version

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install prom -n monitoring --create-namespace \
  prometheus-community/kube-prometheus-stack \
  --set grafana.service.type=NodePort \
  --set grafana.service...        # truncated in source
```

`kube-prometheus-stack` installs Prometheus, Grafana, AlertManager, Node Exporter, and kube-state-metrics together, pre-wired — which would take a great deal of YAML by hand.

**Exploring:**
```bash
kubectl get pods -n monitoring
kubectl get svc -n monitoring       # see NodePorts
```
- **Prometheus:** `http://localhost:30300`
- **Grafana:** `http://localhost:30200` — username `admin`, password `admin` or `prom-operator`

Retrieving the generated password:
```powershell
# PowerShell
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((kubectl get secret -n monitoring prom-grafana -o jsonpath=".data.admin-password")))
```
```bash
# Bash
kubectl get secret -n monitoring prom-grafana -o jsonpath=".data.admin-password" | base64 -d
```

### Instrumenting the FastAPI app

In `src/api/main.py`:
```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```
Append to `requirements.txt`:
```
prometheus-fastapi-instrumentator==6.1.0
```
Commit, push, and deploy:
```bash
kubectl rollout restart deployment model
```

> **Now FastAPI is publishing metrics, but they are not automatically available to Prometheus and Grafana. Prometheus has to *scrape* the metrics from this endpoint.**

### ServiceMonitor — telling Prometheus what to scrape

`deployment/monitoring/servicemonitor.yaml`:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: house-price-api-monitor
  labels:
    release: prom          # must match your Prometheus instance's Helm release
spec:
  selector:
    matchLabels:
      app: model           # selects the Service to scrape
  namespaceSelector:
    matchNames:
      - default
  endpoints:
    - port: "8000"         # or the named port
```

```bash
cd deployment/monitoring
kubectl apply -f servicemonitor.yaml
kubectl get servicemonitor -A
```

**Validate** that metrics arrive at `http://localhost:30300/targets`, then query at `http://localhost:30300/`:

```promql
http_requests_total

histogram_quantile(0.95,
  rate(http_request_duration_seconds_bucket{handler="/predict"}[5m]))

rate(http_request_size_bytes...)    # truncated in source
```

> **The two label matches are the part that trips everyone up.** `labels.release: prom` must match the Helm release name so the Prometheus Operator adopts this ServiceMonitor; `spec.selector.matchLabels` must match the **Service's** labels. Either mismatch means no scraping and no error message.

### Custom dashboards

1. Log in to Grafana
2. *Dashboards → New → Import*
3. Load from [grafana.com/grafana/dashboards](https://grafana.com/grafana/dashboards/), or *Import via dashboard JSON model* and paste `enhanced_fastapi_ml_dashboard`

## ✏️ Exercises

**1.** Explain Prometheus's pull model and why it suits Kubernetes better than a push model.

> [!example]- Solution
> **Pull:** Prometheus periodically issues an HTTP GET to each target's `/metrics` endpoint and stores the response. The application only exposes a plain endpoint; it never initiates a connection.
>
> **Why it fits Kubernetes:**
>
> **Service discovery is automatic.** Pods are ephemeral ([[07 - Kubernetes for ML Deployment]]) — scaling from 2 to 8 replicas creates six new pods with new IPs. In a push model each would need to know where to send metrics and register itself. Prometheus instead queries the Kubernetes API, discovers pods matching a ServiceMonitor, and scrapes them. **Scale up and monitoring follows automatically.**
>
> **Target health is itself a signal.** A failed scrape sets the built-in `up` metric to 0, so a crashed or unreachable pod is detected without any special heartbeat mechanism. Under push, an application that dies simply stops sending — indistinguishable from one that has nothing to report.
>
> **Prometheus controls the load.** It decides scrape frequency, so a misbehaving application cannot flood the monitoring system. Under push, a bug that emits metrics in a tight loop can take down the collector — and monitoring failing during an incident is the worst possible time.
>
> **Endpoints are debuggable.** `curl http://pod:8000/metrics` shows exactly what Prometheus sees, so instrumentation can be verified without involving the monitoring stack at all.
>
> **The trade-off:** pull requires network reachability from Prometheus to every target. Short-lived batch jobs may finish before being scraped — hence the **Pushgateway** for that case. And in this course, `expose(app)` on the FastAPI app publishes the endpoint; the ServiceMonitor tells Prometheus to find it. Both halves are required, which is Exercise 2.

**2.** After adding `Instrumentator().instrument(app).expose(app)` and restarting the deployment, no metrics appear in Grafana. Diagnose systematically.

> [!example]- Solution
> The deck warns of exactly this: *"Now, FastAPI is publishing metrics, but they are not automatically available to Prometheus and Grafana."* **Publishing and scraping are separate steps.**
>
> **Work up the chain:**
>
> **1. Is the app exposing metrics?**
> ```bash
> kubectl port-forward deploy/model 8000:8000
> curl http://localhost:8000/metrics      # expect http_requests_total, etc.
> ```
> If empty: the image was not rebuilt after editing `main.py`, or `prometheus-fastapi-instrumentator` is missing from `requirements.txt`. Note `kubectl rollout restart` restarts pods with the **same image** — if you changed code you must **rebuild and push** first, then update the image tag.
>
> **2. Does the ServiceMonitor exist?**
> ```bash
> kubectl get servicemonitor -A
> ```
>
> **3. Has Prometheus picked it up?** Visit `http://localhost:30300/targets`. **This is the decisive check.** If `house-price-api-monitor` is absent, the ServiceMonitor was never adopted. If present but `DOWN`, the scrape is failing.
>
> **The two most common causes, both silent:**
>
> **(a) `labels.release` mismatch.** The Prometheus Operator only adopts ServiceMonitors whose labels match its configured selector — normally the Helm release name. Installed as `helm upgrade --install prom`, the label must be `release: prom`. Name the release `monitoring` and use `release: prom` and **nothing happens, with no error.**
>
> **(b) `spec.selector.matchLabels` does not match the Service.** The selector targets the **Service**, not the pods. Verify:
> ```bash
> kubectl get svc model --show-labels
> ```
> `kubectl create service nodeport model` labels the Service `app=model` — matching the manifest. But a Service created differently may carry different labels.
>
> **A third, subtler cause: the port.** `endpoints.port` refers to the port's **name** in the Service spec, not its number. A Service with an unnamed port needs `targetPort` instead. The deck's comment — *"or match name of your..."* — is truncated at precisely this point.
>
> **Finally, `namespaceSelector.matchNames: [default]`** must list the namespace the app actually runs in. Deploy to a different namespace and Prometheus will not look there.

**3.** Explain the four monitoring dimensions and why an alert on Model Quality should send you to check Infrastructure first.

> [!example]- Solution
> The chain is **Infrastructure *enables* Service *feeds* Data Quality *reflects* Model Quality** — a causal ordering, not just a list.
>
> **Model Quality is the top of a stack, so a symptom there can originate anywhere below.** Suppose prediction accuracy drops 8%. Four very different root causes produce identical symptoms:
>
> **Infrastructure:** a node ran out of memory and pods are OOM-killed. Requests time out, the client retries with defaults, and "predictions" are actually fallbacks. `kubectl get pods` shows restarts; the accuracy metric shows drift.
>
> **Service:** p99 latency exceeded the client timeout, so a fraction of requests never complete. The model is perfect on the requests it answers, and the *system's* accuracy still falls.
>
> **Data Quality:** an upstream schema change made a feature null. The imputer fills a median, the model predicts confidently, and the answers are wrong. This is the **upstream failure** in the deck's list, and it is a *bug*, not drift.
>
> **Model Quality:** genuine concept drift — the world changed and the model is stale.
>
> **Only the last one calls for retraining.** Retraining in response to the first three wastes days and can entrench the fault — retraining on data from a broken pipeline bakes the corruption in ([[09 - CI-CD with GitHub Actions]]).
>
> **Hence the diagnostic order: check upward from the bottom**, because lower layers are cheaper to check and their failures are unambiguous. Pod restarts, p99 latency, and null rates are all binary-ish facts; concept drift is a statistical inference that takes far longer to establish.
>
> This is why a dashboard should place infrastructure and service tiles at the top — the deck's recommended layout does exactly that — so an on-call engineer eliminates the cheap causes in seconds.
>
> Note the parenthetical **"accuracy (if labels)"**: for fraud or credit, labels arrive weeks or months later ([[06 - Deployment]]), so real-time Model Quality monitoring must rely on proxies — prediction distribution, confidence scores, drift scores — rather than accuracy itself.

**4.** Explain why `rate(model_predictions_total[5m])` is used rather than querying the counter directly, and why p95 latency uses `histogram_quantile` rather than an average.

> [!example]- Solution
> **(a) Counters are cumulative and reset.** `model_predictions_total` only ever increases — 1,000,000 after a week means nothing useful. What you want is *the current rate of predictions*, and `rate()` computes the per-second increase over the window.
>
> Crucially, **`rate()` handles counter resets correctly.** When a pod restarts, its counter drops to zero — a naive difference would compute a large negative rate. `rate()` detects the reset and treats it as a continuation. Given pods restart constantly in Kubernetes, this is not an edge case.
>
> The `[5m]` window smooths noise; shorter is more responsive but jumpier. And for alerting on counters, `rate()` is essentially mandatory — thresholds on a cumulative total are meaningless because it always eventually crosses them.
>
> **(b) Averages hide the tail, and the tail is what users experience.** Suppose 95 requests take 10 ms and 5 take 2,000 ms. The mean is **109 ms** — apparently fine against a 100 ms SLA. But 5% of users waited two seconds. **No user experiences the average.**
>
> Worse, the average is dominated by whichever effect is larger, so a serious tail regression can be masked by a small improvement in the common case.
>
> ```promql
> histogram_quantile(0.95, rate(model_inference_latency_seconds_bucket[5m]))
> ```
> A **Histogram** records counts in latency buckets (`.005, .01, .025, .05, .1, .25, .5, 1.0` in the code), so `histogram_quantile` interpolates the value below which 95% of requests fall.
>
> **Why the tail matters especially for ML serving:** inference latency is often multimodal — cache hits are fast, cache misses require feature retrieval, and cold pods must load the model. The mean sits in an empty region between modes and describes nothing real. The fraud case study's **sub-100 ms** requirement in [[01 - Introduction to MLOps]] is a p95 or p99 requirement, never an average.
>
> **The practical caveat:** quantile accuracy depends entirely on bucket choice. With the largest bucket at 1.0 s, everything slower lands in `+Inf` and p99 cannot be estimated above one second. Choose buckets around your SLA — a 100 ms target needs buckets clustered near 0.1.

**5.** (Advanced) Design an alerting strategy for the deployed model. What should page a human, what should merely be logged, and what can trigger automatic action?

> [!example]- Solution
> **The organising principle: alert on *symptoms users feel*, not on every anomaly.** An alert that fires often and requires no action trains people to ignore alerts — and they will then ignore the one that matters.
>
> **Tier 1 — Page a human immediately (user-visible, needs intervention now):**
> ```yaml
> - alert: ModelServiceDown
>   expr: up{job="house-price-api-monitor"} == 0
>   for: 2m
>   labels: { severity: critical }
>
> - alert: HighErrorRate
>   expr: 100 * rate(http_requests_total{status=~"5.."}[5m])
>       / rate(http_requests_total[5m]) > 5
>   for: 5m
>   labels: { severity: critical }
>
> - alert: LatencySLABreach
>   expr: histogram_quantile(0.95,
>           rate(http_request_duration_seconds_bucket{handler="/predict"}[5m])) > 0.1
>   for: 10m
>   labels: { severity: critical }
> ```
> All three are **Service-dimension** symptoms: the API is down, erroring, or too slow. Each is unambiguous, urgent, and actionable.
>
> **`for:` is what prevents alert fatigue.** Without it, a single slow scrape pages someone at 3 a.m. `for: 5m` requires the condition to hold continuously, filtering transients — a rolling update briefly spikes latency and should not page anyone.
>
> **Tier 2 — Ticket, not page (real but not urgent):**
> ```yaml
> - alert: FeatureDriftDetected
>   expr: model_feature_drift_score > 0.2
>   for: 1h
>   labels: { severity: warning }
>
> - alert: PredictionDistributionShift
>   expr: abs(rate(model_predictions_total{label="approve"}[1h])
>           / rate(model_predictions_total[1h]) - 0.72) > 0.1
>   for: 2h
>   labels: { severity: warning }
> ```
> Drift is **gradual by nature** — the deck's *"silent degradation"* curve. Nobody can act on it at 3 a.m., and it needs analysis rather than a restart. Waking someone for drift is the classic mistake.
>
> **Tier 3 — Automatic action, no human:**
>
> **Autoscaling** via the HPA/KEDA path in the architecture. Rising latency under load is a capacity problem, and Kubernetes can solve it:
> ```yaml
> metrics:
>   - type: Pods
>     pods:
>       metric: { name: model_inference_latency_p95 }
>       target: { type: AverageValue, averageValue: "80m" }
> ```
> **Rollback** on error-rate spikes immediately after a rollout — a deterministic, safe, reversible action.
>
> **Retraining should be Tier 2, not Tier 3.** [[09 - CI-CD with GitHub Actions]] shows drift can fire a `workflow_dispatch` retraining job, but it must promote to **Staging**, not Production. Fully automatic retrain-and-deploy risks retraining on a broken upstream pipeline — Exercise 3's failure mode — and shipping the result.
>
> **What NOT to alert on:** infrastructure metrics without user impact (high CPU that is not causing latency is just efficient use), individual pod restarts (self-healing is working as designed), or any single data point without a `for:` duration.
>
> **Every alert needs a runbook.** An alert whose recipient does not know what to do is noise wearing a uniform. Link each to a document naming the likely causes and the diagnostic order from Exercise 3.

## 📝 Summary

- **Models decay silently** — ML failures are gradual and invisible, unlike software bugs that crash loudly.
- **Five failure modes:** data drift, concept drift, **label drift**, upstream failures, infrastructure issues.
- **Four monitoring dimensions:** Infrastructure → Service → Data Quality → Model Quality, in causal order. Diagnose upward from the bottom.
- **Prometheus pulls** `/metrics` endpoints on a schedule — automatic service discovery, target health as a built-in signal, and load controlled by the collector.
- **Three metric types:** Counter (use `rate()`), Histogram (enables quantiles), Gauge (up and down).
- **`rate()` handles counter resets** across pod restarts.
- **Use `histogram_quantile` for p95/p99, never averages** — the mean hides the tail users actually experience.
- **`Instrumentator().instrument(app).expose(app)`** publishes metrics; a **ServiceMonitor** is separately required to make Prometheus scrape them.
- **ServiceMonitor needs two label matches** — `release:` for the Operator, `spec.selector` for the Service. Neither failure produces an error.
- **Helm's `kube-prometheus-stack`** installs Prometheus, Grafana, AlertManager, Node Exporter, and kube-state-metrics pre-wired.
- **Provision dashboards as ConfigMaps** so they are version-controlled.
- **Prometheus metrics can drive HPA/KEDA autoscaling**, closing the loop back to Kubernetes.

## ⚠️ Important Notes

**Exposing metrics is not the same as collecting them.** `expose(app)` publishes the endpoint; without a ServiceMonitor, Prometheus never looks at it. The deck flags this explicitly.

**ServiceMonitor failures are completely silent.** A wrong `release:` label or a selector that matches no Service produces no error anywhere — check `/targets` in the Prometheus UI, which is the only reliable signal.

**`endpoints.port` refers to the port's *name*, not its number**, unless you use `targetPort`.

**`kubectl rollout restart` reuses the same image.** Code changes require rebuild, push, and an image update — restarting alone changes nothing.

**Never threshold a raw counter.** It increases forever and will eventually cross any threshold. Always wrap in `rate()`.

**Averaged latency is misleading.** 95 requests at 10 ms and 5 at 2 s averages to 109 ms while 5% of users wait two seconds. ML inference latency is often multimodal, making the mean describe nothing real.

**Histogram buckets bound what quantiles you can measure.** With a maximum bucket of 1 s, p99 cannot be estimated above one second. Choose buckets around your SLA.

**Always use `for:` in alert rules.** Without a duration, transient spikes — including normal rolling updates — page people, and alert fatigue makes the next real alert invisible.

**Alert on user-visible symptoms, not on every anomaly.** High CPU without latency impact is efficiency, not an incident.

**Drift alerts should ticket, not page.** Gradual degradation is not a 3 a.m. problem, and it needs analysis rather than a restart.

**A model-quality alert usually is not a model problem.** Check infrastructure, then service, then data quality before concluding drift — and never retrain in response to a broken pipeline.

**"Accuracy (if labels)" is a real caveat.** For fraud and credit, labels arrive months later, so real-time model monitoring must rely on prediction distribution and confidence proxies.

**Change the default Grafana password.** `admin`/`admin` or `prom-operator` is fine for a laptop and unacceptable anywhere else.

> [!warning] Gaps in the source slides
> Hands-on lab material, so the diagrams are TikZ and the icon-font artefacts (`/da◎abase`, `Ὠ0`, `♂server`, `ὒ5`) are rendering glyphs, not content.
> - **Slides 27, 28, 29, 32** — the silent-degradation curve, the four-dimensions diagram, the Prometheus architecture, and the Grafana panel layout are diagrams; I have reconstructed them in ASCII and tables above.
> - **Several code blocks truncate:** slide 27 (the alert label, cut at "Ale"), slide 30 (**the `prometheus_client` example is cut mid-`buckets` list at `[.005`** — the full bucket set, the Gauge definition, and the `start_http_server` call are not shown; I completed the buckets plausibly), slide 31 (**the AlertManager rule is cut at `- alert: High`** — no complete alert rule appears anywhere in the deck), slide 32 (the Grafana JSON, cut mid-expression), slide 34 (**the Helm command is cut at `--set grafana.serv`** — likely `grafana.service.nodePort=30200`), slide 35 (the Bash password command, cut at `admin-pass`), slide 36 (cut at "scrape the metrics from this"), slide 37 (**the ServiceMonitor `endpoints` block is cut at "or match name of yo"** — precisely the line that causes the most common misconfiguration), slide 38 (the third PromQL query, cut at `rate(http_request_size_bytes`).
> - **Slide 33** produced no text — a section divider.
> - **Slide 39** references `enhanced_fastap_ml_dashboard` (sic — likely `enhanced_fastapi_ml_dashboard`), a JSON file **not present in `documents/`**.
> - **No complete alerting configuration appears in the deck.** Exercise 5's rules are my reconstruction.
>
> **Links:** [Prometheus community Helm charts](https://prometheus-community.github.io/helm-charts) · [Grafana dashboard library](https://grafana.com/grafana/dashboards/) · Helm official install instructions (referenced, URL not extracted).

---
**Previous:** [[07 - Kubernetes for ML Deployment]] · **Next:** [[09 - CI-CD with GitHub Actions]]
