---
subject: MLOps
chapter: 07
tags: [ds, mlops, kubernetes, kind, kubectl, orchestration, scaling]
source: "MLOps_K8s.pdf (slides 1–25) — MLOps Course, Swinburne Vietnam, April 2026. Note MLOps_DeployingML_on_K8s.pdf is a strict subset of this deck."
---

# Kubernetes for ML Deployment

> *Creating a Deployment & Service for a FastAPI-Wrapped Model*

> [!note] Where this sits in the course
> [[05 - Packaging Models with FastAPI and Docker]] ended with Docker Compose, which [[06 - Deployment]] noted is **single-host**: no rolling updates, no autoscaling, no multi-node scheduling. Kubernetes provides all three, and is the *"low-level infrastructure"* production environment named in [[06 - Deployment]].

> [!warning] Duplicate source decks
> `MLOps_DeployingML_on_K8s.pdf` (23 pages) is a **strict subset** of `MLOps_K8s.pdf` (39 pages) — slides 1–23 are identical, differing only in one command (`--image=streamlit:v2` vs the Docker Hub path). The larger deck adds slides 27–39 on Prometheus and Grafana, covered in [[08 - Monitoring with Prometheus and Grafana]]. **They are one lecture, not two.**

## 📘 Main Knowledge

### Why Kubernetes — the challenges it solves

Once containers span multiple hosts, two problems appear that Docker alone cannot answer:

- **Scheduling** — which container runs where?
- **Networking** — how do containers on different hosts reach each other?

Kubernetes' answer bundles five capabilities:

| Capability | What it gives you |
|---|---|
| **Load Balancing** | Distribute requests across replicas |
| **Service Discovery** | Find a service by stable name, not by IP |
| **HA = Replication** | High availability through multiple copies |
| **Auto Scaling** | Add or remove replicas with demand |
| **Self Healing** | Restart or reschedule failed containers |
| **Rollout** | Update versions without downtime |

**Self-healing and rollout are what Compose cannot do**, and they are exactly what [[06 - Deployment]]'s canary and rolling strategies require.

### Tools: kind and kubectl

**kind — Kubernetes IN Docker**
- Runs Kubernetes **nodes as Docker containers**
- Designed for **local development and CI**
- Lightweight, fast to spin up
- **Multi-node clusters on one machine**

**kubectl — Kube Control CLI**
- The official Kubernetes CLI
- Deploy, inspect, and manage workloads
- Works with **any** Kubernetes cluster
- Communicates via the **API server**

> **Why this stack? No cloud account needed. Reproduce production-like pipelines entirely on your laptop.**

The elegance of kind is that nodes are containers, so a "three-node cluster" is three Docker containers — the same nesting idea as Dev Containers in [[02 - Environment Setup]].

**Docker Desktop shortcut:** `kubectl` may already be bundled. Check with `kubectl version --client`, and enable the cluster under *Settings → Kubernetes → Enable Kubernetes*.

**Installing kind on Windows:**
```powershell
# One-time setup (run once as Admin)
New-Item -ItemType Directory -Force -Path C:\tools
[Environment]::SetEnvironmentVariable(
    "Path", $env:Path + ";C:\tools", [EnvironmentVariableTarget]::User)

# Install kind
curl.exe -Lo kind.exe https://kind.sigs.k8s.io/dl/v0.31.0/kind-windows-amd64
Move-Item .\kind.exe C:\tools\kind.exe
kind version
```

### Creating clusters

**Single node:**
```bash
kind create cluster --name mlops-cluster
```
```
Creating cluster "mlops-cluster" ...
 * Ensuring node image (kindest/node:v1.30.0) ...
 * Preparing nodes ...
 * Writing configuration ...
 * Starting control-plane ...
 * Installing CNI ...
 * Installing StorageClass ...
Set kubectl context to "kind-mlops-cluster"
```

**Multi-node** — `kind-three-node-cluster.yaml`:
```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
```
```bash
kind create cluster --name mlops-cluster --config kind-three-node-cluster.yaml
```

> **When to use multi-node:** test **pod scheduling across nodes** · simulate **node affinity** rules · validate **DaemonSets** in MLOps pipelines · mirror a real multi-worker cluster.

> Kubernetes is an orchestration engine, typically orchestrating containers **across different nodes**. You should have **at least three nodes** to get a sense of a real Kubernetes setup.

The course config comes from the project repository:
```bash
curl.exe -O https://raw.githubusercontent.com/NguyenMToan/house-price-predictor/main/kind-three-node-cluster.yaml
kind create cluster --name mlops-cluster --config kind-three-node-cluster.yaml
```
A cluster **visualizer** is cloned from `github.com/schoolofdevops/kube-...` *(URL truncated in source)*.

**Verifying:**
```bash
kubectl config get-contexts        # list all contexts
kubectl config current-context     # kind sets this automatically
kubectl get nodes                  # all nodes should show Ready
kubectl get pods -n kube-system    # system pods
```

**Useful kind commands:**
```bash
kind get clusters                                              # list clusters
kind load docker-image fastapi:v2 --name mlops-cluster         # load a LOCAL image
docker exec -it mlops-cluster-control-plane crictl images      # images on a node
kind delete cluster --name mlops-cluster
```

> **`kind load docker-image` is the one people forget.** A kind cluster cannot see your local Docker images — its nodes are separate containers with their own image stores. Either push to a registry, or load the image explicitly.

### The ML serving setup

Two components, each with a **Deployment** and a **Service**:

- **`app`** — the ML model serving layer (a FastAPI or Flask app wrapping the model). It gets a **Deployment** (to manage replicas and rolling updates) and a **Service** (to expose it to incoming prediction requests).
- **`db`** — a database backend storing prediction logs, feature data, or model metadata. It also gets a Deployment and a Service, **so the app can reach it internally via a stable DNS name**.

That stable DNS name is the Kubernetes equivalent of Compose's service-name networking from [[05 - Packaging Models with FastAPI and Docker]] — and it is why the Streamlit app can be pointed at `http://model:8000`.

**Deployment vs Service** — the division of labour:
- A **Deployment** manages *pods*: how many replicas, which image, how to roll out a new version, and restarting them when they die.
- A **Service** provides a *stable network identity*: pods come and go with changing IPs, so the Service gives a fixed name and load-balances across whichever pods currently exist.

### Deploying and exposing an app

```bash
kubectl create deployment --help

# Create a Deployment named "streamlit"
kubectl create deployment streamlit \
  --image=manhtoannb87/streamlit:latest --port=8501

kubectl describe deploy streamlit          # inspect detailed state
kubectl scale deploy streamlit --replicas=4  # maintain 4 running Pods
kubectl get pods
```

**Exposing with a NodePort Service:**
```bash
kubectl create service nodeport --help

# Expose container port 8501 on port 30000 of EVERY node
kubectl create service nodeport streamlit --tcp=8501 --node-port=30000
```

**NodePort opens the same port on every node in the cluster**, which is simple and ideal for local development. Production normally uses a LoadBalancer or an Ingress instead, since NodePort ports are restricted to the 30000–32767 range and expose nodes directly.

**Deploying the FastAPI-wrapped model:**
```bash
kubectl create deployment model \
  --image=manhtoannb87/house-price-model:latest --port=8000 --replicas=2

kubectl create service nodeport model --tcp=8000 --node-port=30100
kubectl describe service model
```

### Connecting Streamlit to the model

In `streamlit_app/main.py`, change:
```python
api_endpoint = os.getenv("API_URL", "http://localhost:8000")
```
to point at `http://model:8000` — **the Service name**, exactly as Compose used the service name.

```bash
cd streamlit_app
docker image build -t manhtoannb87/streamlit:v3 .
docker image push manhtoannb87/streamlit:v3

kubectl scale deploy streamlit --replicas=8
# Update the container image within the streamlit deployment
kubectl set image deploy/streamlit streamlit=manhtoannb87/streamlit:v3
```

**Monitoring the rollout:**
```bash
kubectl rollout status deploy streamlit
```

This is a **rolling deployment** ([[06 - Deployment]]) executed for real: Kubernetes replaces pods gradually, keeping the service available throughout. `kubectl rollout undo deploy/streamlit` reverses it.

## ✏️ Exercises

**1.** Explain what `kind load docker-image fastapi:v2 --name mlops-cluster` does and why it is necessary. What happens without it?

> [!example]- Solution
> **Without it, your pod sits in `ErrImagePull` or `ImagePullBackOff` forever.**
>
> The confusion is understandable: kind runs *inside* Docker, so surely it can see Docker's images? It cannot. **kind's nodes are Docker containers running their own container runtime (containerd) with their own separate image store.** Building `fastapi:v2` on your host puts it in the *host's* Docker image store, which the node containers cannot read.
>
> When Kubernetes schedules a pod, the node's kubelet looks for the image locally; not finding it, it tries to pull from a registry — where `fastapi:v2` does not exist either, because you never pushed it. Hence the pull failure.
>
> ```bash
> kubectl get pods
> # NAME                     READY   STATUS             RESTARTS
> # model-7d4f8b9c5-x2klm    0/1     ImagePullBackOff   0
>
> kubectl describe pod model-7d4f8b9c5-x2klm    # Events show "Failed to pull image"
> ```
>
> **Two fixes:**
> ```bash
> kind load docker-image fastapi:v2 --name mlops-cluster   # copy into node stores
> docker exec -it mlops-cluster-control-plane crictl images  # verify
> ```
> or push to a registry and reference it by its full name — which is what the course does with `manhtoannb87/house-price-model:latest`, and why [[09 - CI-CD with GitHub Actions]] publishes to Docker Hub.
>
> **A trap on top of a trap:** with a **multi-node** cluster, `kind load` copies the image to *all* nodes, but the default `imagePullPolicy` for a `:latest` tag is `Always` — so Kubernetes tries to pull even though the image is present locally. Tag your images with a real version (`fastapi:v2`, not `:latest`) and the policy becomes `IfNotPresent`, using the loaded image. This is another reason [[02 - Environment Setup]] insists on never using `:latest`.

**2.** Explain the difference between a **Deployment** and a **Service**, and why both are needed for the `model` component.

> [!example]- Solution
> They answer different questions: a Deployment manages **which pods exist**; a Service manages **how to reach them**.
>
> **The Deployment** creates and maintains pods. `--replicas=2` is a *declaration of desired state*: Kubernetes continuously reconciles reality against it. Kill a pod and a replacement appears within seconds — that is **self-healing**. It also owns the **rollout** process, replacing pods gradually when the image changes.
>
> **The Service** exists because **pods are ephemeral and their IPs change.** Every restart, every scale event, every rollout produces new pods with new IPs. Hardcoding a pod IP guarantees breakage. The Service provides:
> - a **stable DNS name** — `model` resolves cluster-wide, regardless of which pods exist
> - **load balancing** — requests distribute across all healthy pods automatically
> - **decoupling** — Streamlit does not know or care how many model replicas there are
>
> **Without the Deployment:** you could create bare pods, but nothing would restart them when they crash, and updating the image would mean manual deletion and recreation with downtime.
>
> **Without the Service:** Streamlit would need to discover pod IPs itself, and every scale or rollout would break it. This is exactly why `api_endpoint` becomes `http://model:8000` — the Service name — rather than any IP.
>
> **The two are linked by labels, not by name.** `kubectl create deployment model` labels its pods `app=model`, and `kubectl create service nodeport model` selects pods with that label. This is why the *names* matching is a convention rather than a requirement — and why a Service with a typo'd selector silently routes to nothing. `kubectl describe service model` shows the `Endpoints:` field; if it is empty, the selector matches no pods.

**3.** Trace what happens when `kubectl set image deploy/streamlit streamlit=manhtoannb87/streamlit:v3` runs on a deployment with 8 replicas. Which deployment strategy from [[06 - Deployment]] is this?

> [!example]- Solution
> **This is a rolling deployment**, and it is Kubernetes' default (`RollingUpdate`).
>
> **The sequence:**
> 1. The Deployment's pod template is updated to the new image.
> 2. Kubernetes creates a **new ReplicaSet** for v3 and begins scaling it up while scaling the old one down — **gradually, not all at once**.
> 3. Default parameters are `maxSurge: 25%` and `maxUnavailable: 25%`, so with 8 replicas it may run up to 10 pods temporarily and never drop below 6 available.
> 4. Each new pod must pass its readiness check before an old pod is removed.
> 5. Repeat until all 8 pods run v3. The old ReplicaSet is retained at 0 replicas — which is what makes rollback instant.
>
> ```bash
> kubectl rollout status deploy streamlit    # watch it progress
> kubectl get rs                             # see old and new ReplicaSets
> kubectl rollout undo deploy/streamlit      # instant rollback
> ```
>
> **Why the Service matters here:** throughout the rollout, pods of *both* versions carry the label `app=streamlit`, so the Service load-balances across them. Users are served by a mix of v2 and v3 during the transition — **zero downtime, but temporary version inconsistency**, exactly the limitation [[06 - Deployment]] lists for rolling deployments.
>
> **The critical prerequisite people miss: readiness probes.** Without one, Kubernetes considers a pod "ready" as soon as its container process starts — before the model has finished loading from disk. It then removes an old pod, and the Service routes traffic to a pod that cannot yet serve. **Traffic is dropped, silently.** This is the Kubernetes form of the `depends_on` readiness problem from [[05 - Packaging Models with FastAPI and Docker]]:
> ```yaml
> readinessProbe:
>   httpGet: { path: /health, port: 8000 }
>   initialDelaySeconds: 10
>   periodSeconds: 5
> ```
> For ML services this matters more than for ordinary web apps, because model loading can take tens of seconds.
>
> Note that `kubectl create deployment` (imperative) cannot express probes, resource limits, or rollout parameters — which is why production uses **declarative YAML manifests** applied with `kubectl apply -f`. The imperative commands here are a teaching shortcut.

**4.** Why does the course insist on a three-node cluster when a single node would run the same containers?

> [!example]- Solution
> The deck's reason: *"Kubernetes is an orchestration engine, typically orchestrating containers across different nodes. You should have at least three nodes to get a sense of a real Kubernetes setup."*
>
> **On a single node, orchestration is invisible** — every pod lands in the same place, so scheduling is trivial and cross-host networking never gets exercised. Yet those are precisely the two problems slide 6 says Kubernetes exists to solve. A single-node cluster hides the entire value proposition.
>
> **What only appears with multiple nodes:**
>
> - **Pod scheduling** — with `--replicas=8` you can watch pods distribute across workers, and see how resource requests influence placement. `kubectl get pods -o wide` shows the `NODE` column.
> - **Node affinity** — real ML clusters have heterogeneous nodes (GPU nodes for training, CPU nodes for serving), and affinity rules direct workloads accordingly. On one node the concept is meaningless.
> - **DaemonSets** — a workload that runs exactly one pod *per node*, used for log collectors and metric exporters. On a single node a DaemonSet is indistinguishable from a one-replica Deployment. This matters directly for [[08 - Monitoring with Prometheus and Grafana]], where Node Exporter is a DaemonSet.
> - **Real high availability** — replicas on one node all die together when that node dies. HA means surviving node loss, which is only testable with more than one node.
> - **Cross-node networking** — the CNI plugin routing pod traffic between hosts is exercised only when pods actually sit on different hosts.
>
> **The practical test:** `kubectl drain` a worker and watch pods reschedule onto the survivor. That is self-healing at the *node* level rather than the container level, and it is the behaviour that justifies Kubernetes over Docker Compose in the first place.
>
> Because kind runs nodes as containers, all of this costs three containers on one laptop rather than three machines — which is the whole point of the tool.

**5.** (Advanced) The course uses `kubectl create` imperatively. Rewrite the model deployment as declarative YAML with production-grade settings, and explain why declarative is preferred.

> [!example]- Solution
> ```yaml
> # deployment/model-deployment.yaml
> apiVersion: apps/v1
> kind: Deployment
> metadata:
>   name: model
>   labels: { app: model }
> spec:
>   replicas: 2
>   selector:
>     matchLabels: { app: model }
>   strategy:
>     type: RollingUpdate
>     rollingUpdate: { maxSurge: 1, maxUnavailable: 0 }   # never lose capacity
>   template:
>     metadata:
>       labels: { app: model }
>     spec:
>       containers:
>         - name: model
>           image: manhtoannb87/house-price-model:v1.2.0   # PINNED, not :latest
>           ports:
>             - containerPort: 8000
>           resources:
>             requests: { cpu: "500m", memory: "512Mi" }   # for scheduling
>             limits:   { cpu: "2000m", memory: "2Gi" }     # prevents noisy neighbours
>           readinessProbe:                                 # ready to SERVE?
>             httpGet: { path: /health, port: 8000 }
>             initialDelaySeconds: 15
>             periodSeconds: 5
>           livenessProbe:                                  # still ALIVE?
>             httpGet: { path: /health, port: 8000 }
>             initialDelaySeconds: 30
>             periodSeconds: 20
>           env:
>             - name: MODEL_PATH
>               value: /app/models/trained/house-price-model.pkl
> ---
> apiVersion: v1
> kind: Service
> metadata:
>   name: model
> spec:
>   type: NodePort
>   selector: { app: model }
>   ports:
>     - port: 8000
>       targetPort: 8000
>       nodePort: 30100
> ```
> ```bash
> kubectl apply -f deployment/model-deployment.yaml
> ```
>
> **Why declarative wins — five reasons:**
>
> **1. It is version-controlled.** The manifest lives in Git beside the code, so the cluster's desired state is reviewable, diffable, and auditable — the traceability requirement from [[01 - Introduction to MLOps]]. An imperative `kubectl create` exists only in someone's shell history.
>
> **2. It is idempotent.** `kubectl apply` can run repeatedly and converges to the declared state; `kubectl create` fails with `AlreadyExists`. This is the *idempotent stages* requirement from [[09 - CI-CD with GitHub Actions]], and it is what makes the manifest safe to apply from CI on every merge.
>
> **3. It expresses what imperative commands cannot.** Probes, resource limits, rollout parameters, volumes, affinity, and environment variables have no `kubectl create` flags. Everything that makes a deployment production-ready is only reachable through YAML.
>
> **4. `maxUnavailable: 0` guarantees no capacity loss** during a rollout — the default 25% would drop two of eight replicas mid-update.
>
> **5. Resource requests are how scheduling works.** Without `requests`, the scheduler assumes a pod needs nothing and can overcommit a node until it OOMs. Without `limits`, one runaway pod starves its neighbours. For ML serving, where a model may hold hundreds of MB in memory, both are essential.
>
> **The probe distinction is worth stating precisely**, because confusing them causes outages: **readiness** removes a pod from the Service when it cannot serve (but leaves it running); **liveness** *restarts* the container when it is hung. Pointing liveness at a slow endpoint with too short a delay creates a restart loop — the pod is killed while still loading the model, forever.
>
> The natural next step is a **HorizontalPodAutoscaler** driven by custom metrics — which is what the Prometheus stack in [[08 - Monitoring with Prometheus and Grafana]] enables.

## 📝 Summary

- **Kubernetes solves scheduling and cross-host networking**, and adds load balancing, service discovery, replication, autoscaling, self-healing, and rollouts.
- **kind runs Kubernetes nodes as Docker containers** — production-like multi-node clusters on a laptop, no cloud account.
- **`kubectl` talks to any cluster via the API server.**
- **A kind cluster cannot see local Docker images** — use `kind load docker-image` or push to a registry.
- **Deployment manages pods** (replicas, rollouts, self-healing); **Service gives a stable DNS name and load-balances** across whichever pods exist.
- **Deployment and Service are linked by labels**, not by name.
- **Services are why `http://model:8000` works** — the same service-name pattern as Docker Compose.
- **NodePort exposes the same port on every node** — simple for local dev; production prefers LoadBalancer or Ingress.
- **`kubectl set image` triggers a rolling update by default** — zero downtime, temporary version mixing, instant `rollout undo`.
- **Use three nodes** to exercise scheduling, affinity, DaemonSets, and real HA.
- **Prefer declarative YAML** — version-controlled, idempotent, and the only way to express probes and resource limits.

## ⚠️ Important Notes

**`kind load docker-image` is required for locally built images.** Otherwise pods sit in `ImagePullBackOff` — kind's nodes have their own image stores.

**`:latest` forces `imagePullPolicy: Always`**, so even a loaded image is re-pulled and fails. Tag with a real version.

**Without a readiness probe, rolling updates drop traffic.** Kubernetes marks a pod ready as soon as its process starts, before an ML model has finished loading — then routes requests to it. This is the single most common ML-on-Kubernetes outage.

**Readiness and liveness are different.** Readiness removes a pod from the Service; liveness restarts the container. A liveness probe with too short a delay creates an infinite restart loop.

**Services select pods by label, not by name.** A typo'd selector routes to nothing and produces no error — check `Endpoints:` in `kubectl describe service`.

**Pod IPs are ephemeral.** Never hardcode one; always use the Service name.

**`kubectl create` cannot express probes, resource limits, or rollout parameters.** Imperative commands are a teaching shortcut; production needs `kubectl apply -f`.

**Missing resource requests break scheduling.** The scheduler assumes zero, overcommits the node, and pods get OOM-killed. Missing limits lets one pod starve the rest.

**Default `maxUnavailable: 25%` reduces capacity during a rollout.** Set it to 0 with `maxSurge: 1` when capacity matters.

**Rolling updates mix versions temporarily.** During the transition the Service serves both old and new pods — fine for compatible changes, dangerous when the API contract changed.

**NodePort ports are restricted to 30000–32767** and expose every node directly. Not suitable for production ingress.

**A single-node cluster hides everything Kubernetes is for.** Scheduling, affinity, DaemonSets, and node-level HA are all invisible.

> [!warning] Gaps in the source slides
> **This is a hands-on lab deck and the conceptual slides are all images:**
> - **Slides 3, 4, 5 — "Scalable Infrastructure for Model Inference" and both "Why Kubernetes" slides — are title-only.** The motivation for Kubernetes is therefore **not captured** beyond the challenge fragments on slide 6.
> - **Slide 7 — "K8s Architecture" is entirely an image.** The control plane / node architecture (API server, scheduler, etcd, kubelet, kube-proxy) — arguably the most examinable content — is **not recoverable**.
> - **Slide 20 — "Deployment Pattern"** is an image.
> - **Slides 2, 8, 12, 17, 26** produced no text — section dividers.
> - **Several commands truncate:** slide 9 (footer), slide 13 (the "What happened?" explanation, cut at "started Docker containers as K8"), slide 19 (**the visualizer repo URL is cut at `schoolofdevops/kube`**), slide 21 (`kubectl scale`, cut at "kubectl s"), slide 24 (**the `kubectl set image` command is cut at "streamlit dep"** — I have reconstructed it).
> - **No YAML manifests are shown** apart from the kind cluster config. All Deployments and Services are created imperatively, so production-grade manifests (probes, resources, strategy) do not appear anywhere in the deck; Exercise 5's manifest is my reconstruction.
>
> **The two K8s PDFs are near-duplicates.** `MLOps_DeployingML_on_K8s.pdf` slides 1–23 match `MLOps_K8s.pdf` slides 1–25 except that slide 19/21 uses `--image=streamlit:v2` in the shorter deck and `--image=manhtoannb87/streamlit:latest` in the longer — suggesting the shorter is an earlier draft before Docker Hub publishing was introduced.
>
> **Links:** [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/) · [kubectl reference](https://kubernetes.io/docs/reference/kubectl/) · project repo `github.com/NguyenMToan/house-price-predictor`

---
**Previous:** [[06 - Deployment]] · **Next:** [[08 - Monitoring with Prometheus and Grafana]]
