---
subject: MLOps
chapter: 08
tags: [ds, mlops, prometheus, grafana, observability, promql, kubernetes]
source: "MLOps_K8s.pdf (slides 27–39) — MLOps Course, Swinburne Vietnam, April 2026"
---

# Monitoring with Prometheus and Grafana

The second half of the Kubernetes lecture ([[07 - Kubernetes for ML Deployment]]): the observability tooling. The theory of drift and monitoring is in [[10 - Monitoring and Drift]].

## 📘 Main Knowledge

### Why monitor

Models decay silently: unlike software bugs, ML failures are gradual and invisible. The slide's curve shows accuracy sliding below a threshold through a stretch of "silent degradation" before an alert fires; monitoring tries to shorten that stretch.

| Failure | What happens |
|---|---|
| data drift | input distribution shifts |
| concept drift | the $X\to Y$ relationship changes |
| **label drift** | target distribution changes (e.g. fraud rate 0.5% → 2%) |
| upstream failure | a feature pipeline breaks |
| infrastructure | latency spikes, out-of-memory |

### Four dimensions

| Dimension | Watch |
|---|---|
| Infrastructure | CPU/GPU, memory, disk I/O, network, pod restarts |
| Service | requests per second, latency p50/p95/p99, error rate |
| Data quality | feature distributions, missing values, schema violations, drift |
| Model quality | prediction distribution, confidence, accuracy (if labels), business KPIs |

Infrastructure enables service, which feeds data quality, which shows up in model quality. A model-quality alert can start at any lower layer, so diagnose from the bottom up. The first two are standard DevOps; the last two are what MLOps adds, and "accuracy (if labels)" acknowledges delayed labels.

### Prometheus architecture

```
pods (ML services, Node Exporter, kube-state-metrics) expose /metrics
        ↑ pull (scrape)
Prometheus (scrape + TSDB) ──PromQL──→ Grafana dashboards
        ├──→ AlertManager → PagerDuty / Slack
        └──→ HPA / KEDA (custom metrics for autoscaling)
```

Prometheus **pulls**: it scrapes `/metrics` endpoints on a schedule. Apps only expose an HTTP endpoint, targets are discovered through Kubernetes, and an unreachable target is itself a signal. Data goes into a time-series database, is queried with **PromQL**, shown in **Grafana**, alerted on through **AlertManager**, and can drive autoscaling.

### Instrumenting a service

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

PREDICTION_COUNTER = Counter('model_predictions_total', 'Total predictions served',
                             ['model_version', 'label'])
LATENCY = Histogram('model_inference_latency_seconds', 'Inference latency',
                    buckets=[.005, .01, .025, .05, .1, .25, .5, 1.0])
```

- **Counter**: only increases (total predictions); query it with `rate()`.
- **Histogram**: bucketed observations, giving quantiles.
- **Gauge**: goes up and down (drift score, queue depth).

Labels such as `model_version` let you compare v1 and v2 during a canary.

### PromQL

```promql
rate(model_predictions_total[5m])                                          # requests/s
histogram_quantile(0.95, rate(model_inference_latency_seconds_bucket[5m])) # p95 latency
100 * rate(model_errors_total[5m]) / rate(model_requests_total[5m])        # error %
model_feature_drift_score > 0.2                                            # drift alert
```

`rate()` turns a cumulative counter into a per-second rate and handles resets when pods restart. `histogram_quantile` computes tail latency from buckets; an average hides the tail users feel.

### Grafana

Layout, top to bottom: stat tiles (RPS, p95, error %, drift); predictions/s and latency p50/p95/p99; feature drift and prediction distribution; errors and alerts. It reads from "is it up?" to "is it right?". Dashboards provisioned as a ConfigMap (JSON inside YAML) are version-controlled, like declarative manifests.

### Installing with Helm

Helm is the Kubernetes package manager. `kube-prometheus-stack` installs Prometheus, Grafana, AlertManager, Node Exporter and kube-state-metrics, already wired together.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install prom -n monitoring --create-namespace \
  prometheus-community/kube-prometheus-stack \
  --set grafana.service.type=NodePort ...     # rest truncated in source
kubectl get pods -n monitoring
kubectl get svc -n monitoring
kubectl get secret -n monitoring prom-grafana -o jsonpath=".data.admin-password" | base64 -d
```
Prometheus at `localhost:30300`, Grafana at `localhost:30200` (user `admin`, password `admin` or `prom-operator`; change it outside a laptop).

### Instrumenting the FastAPI app

```python
# src/api/main.py
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
```
Add `prometheus-fastapi-instrumentator==6.1.0` to `requirements.txt`, rebuild, push, redeploy. The app now publishes metrics, but Prometheus must be told to scrape them.

### ServiceMonitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: house-price-api-monitor
  labels:
    release: prom          # must match the Prometheus Helm release
spec:
  selector:
    matchLabels:
      app: model           # must match the Service's labels
  namespaceSelector:
    matchNames: [default]
  endpoints:
    - port: "8000"         # the Service port's name (truncated in source)
```
```bash
kubectl apply -f deployment/monitoring/servicemonitor.yaml
kubectl get servicemonitor -A
```
Check `localhost:30300/targets`, then query `http_requests_total` or `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{handler="/predict"}[5m]))`. In Grafana: Dashboards → New → Import, from grafana.com or a JSON model.

## ✏️ Exercises

**1.** Explain Prometheus's pull model and why it suits Kubernetes.

> [!example]- Solution
> Prometheus GETs each target's `/metrics` on a schedule. Pods come and go with new IPs; Prometheus finds them through the Kubernetes API, so monitoring follows scaling automatically. A failed scrape sets `up` to 0, so dead pods are detected (with push, a dead app just goes quiet). Prometheus sets the scrape rate, so a buggy app can't flood it. `curl pod:8000/metrics` shows exactly what Prometheus sees.
> Trade-offs: Prometheus must reach every target, and short batch jobs may finish before a scrape (use the Pushgateway).

**2.** After adding the Instrumentator and restarting the deployment, no metrics appear in Grafana. Diagnose.

> [!example]- Solution
> 1. Is the app exposing metrics? `kubectl port-forward deploy/model 8000:8000` then `curl localhost:8000/metrics`. If not: `kubectl rollout restart` reuses the same image, so rebuild, push and update the tag; check `requirements.txt`.
> 2. Does the ServiceMonitor exist? `kubectl get servicemonitor -A`.
> 3. Is it on `/targets`? This is the decisive check. Missing: not adopted. `DOWN`: scrape failing.
>
> Common silent causes: `release:` doesn't match the Helm release (`prom`); `matchLabels` doesn't match the Service's labels (`kubectl get svc model --show-labels`); `endpoints.port` must be the Service port's name; `namespaceSelector` lists the wrong namespace.

**3.** Explain the four dimensions. Why should a model-quality alert send you to check infrastructure first?

> [!example]- Solution
> An 8% accuracy drop could come from OOM-killed pods (fallback answers), latency above the client timeout (unanswered requests), an upstream schema change leaving a feature null (imputed values), or real concept drift. Only the last needs retraining; retraining on a broken pipeline bakes the fault in. Lower layers are cheaper to check and give clear answers (restarts, p99, null rates), while drift needs statistical evidence. Hence infrastructure and service tiles at the top of the dashboard. With delayed labels, model quality relies on proxies (prediction distribution, confidence, drift scores).

**4.** Why use `rate(model_predictions_total[5m])` instead of the counter itself, and `histogram_quantile` instead of an average for p95?

> [!example]- Solution
> (a) The counter only grows, so its value says little, and any threshold is eventually crossed. `rate()` gives the per-second increase and treats a pod-restart reset as a continuation rather than a large negative rate. The window trades responsiveness for smoothness.
> (b) 95 requests at 10 ms and 5 at 2,000 ms average to 109.5 ms, close to a 100 ms SLA, while 5% of users wait 2 s. ML latency is often multimodal (cache hits, feature lookups, cold pods), so the mean may describe no real request. `histogram_quantile` interpolates within buckets, so buckets limit what you can measure: with a top bucket of 1 s, p99 can't be estimated above 1 s. Cluster buckets around the SLA.

**5.** (Advanced) Design alerting for the deployed model: what pages a human, what becomes a ticket, what triggers automatic action?

> [!example]- Solution
> Alert on symptoms users feel; alerts that need no action train people to ignore alerts.
>
> **Page** (service down, errors, SLA breach):
> ```yaml
> - alert: ModelServiceDown
>   expr: up{job="house-price-api-monitor"} == 0
>   for: 2m
>   labels: { severity: critical }
> - alert: HighErrorRate
>   expr: 100 * rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 5
>   for: 5m
>   labels: { severity: critical }
> - alert: LatencySLABreach
>   expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{handler="/predict"}[5m])) > 0.1
>   for: 10m
>   labels: { severity: critical }
> ```
> `for:` filters transients such as a rolling update.
>
> **Ticket**: drift (`model_feature_drift_score > 0.2` for 1 h) and prediction-distribution shifts. Drift is gradual and needs analysis, not a 3 a.m. restart.
>
> **Automatic**: autoscaling on latency through HPA/KEDA, and rollback on an error spike right after a rollout. Retraining can be triggered automatically ([[09 - CI-CD with GitHub Actions]]) but should promote only to staging, since the cause may be a broken pipeline.
>
> Don't alert on high CPU without user impact, single pod restarts (self-healing works), or anything without `for:`. Give each alert a runbook.

## 📝 Summary

- Models decay silently; failure modes include label drift and upstream breaks as well as data and concept drift.
- Four dimensions in causal order: infrastructure → service → data quality → model quality; diagnose bottom up.
- Prometheus pulls `/metrics`; Grafana visualizes; AlertManager notifies; metrics can drive autoscaling.
- Counter (`rate()`), Histogram (quantiles), Gauge.
- Use quantiles for latency, not means.
- `expose(app)` publishes metrics; a ServiceMonitor with matching `release:` and selector labels makes Prometheus scrape them.
- `kube-prometheus-stack` installs the whole stack; dashboards as ConfigMaps.

## ⚠️ Important Notes

1. Exposing metrics ≠ collecting them.
2. ServiceMonitor mismatches fail silently; check `/targets`.
3. `endpoints.port` is the port name.
4. `rollout restart` reuses the same image.
5. Never threshold a raw counter.
6. Mean latency hides the tail.
7. Histogram buckets cap measurable quantiles.
8. Always use `for:` in alert rules.
9. Alert on user-visible symptoms.
10. Drift alerts become tickets, not pages.
11. A model-quality alert is often not a model problem.
12. Change the default Grafana password.

> [!warning] Gaps in the source slides
> - Slides 27–29 and 32 (degradation curve, dimensions, architecture, panel layout) are diagrams, rebuilt above as text. Icon-font glyphs in the extraction are artifacts. Slide 33 has no text.
> - Truncated: slide 30 (the `prometheus_client` example stops in the bucket list; the Gauge and `start_http_server` aren't shown), 31 (the alert rule stops at `- alert: High`), 32 (Grafana JSON), 34 (Helm command at `--set grafana.serv`), 35, 36, 37 (the ServiceMonitor `endpoints` comment), 38 (third PromQL query).
> - Slide 39 refers to `enhanced_fastap_ml_dashboard` (sic), which isn't in `documents/`.
> - The deck has no complete alert rules; Exercise 5's are mine.

**Previous:** [[07 - Kubernetes for ML Deployment]] · **Next:** [[09 - CI-CD with GitHub Actions]]
