---
subject: MLOps
chapter: 07
tags: [ds, mlops, kubernetes, kind, kubectl, orchestration, scaling]
source: "MLOps_K8s.pdf (slides 1–25) — MLOps Course, Swinburne Vietnam, April 2026. Note MLOps_DeployingML_on_K8s.pdf is a strict subset of this deck."
---

# Kubernetes for ML Deployment

Creating a Deployment and a Service for a FastAPI-wrapped model. Docker Compose ([[05 - Packaging Models with FastAPI and Docker]]) runs on one host, with no rolling updates, autoscaling or multi-node scheduling; Kubernetes provides them and is the "low-level infrastructure" environment of [[06 - Deployment]].

> [!note] Source decks
> `MLOps_DeployingML_on_K8s.pdf` (23 pp) is a subset of `MLOps_K8s.pdf` (39 pp): the same slides apart from one image tag. The longer deck's slides 27–39 are in [[08 - Monitoring with Prometheus and Grafana]]. One lecture, two files.

## 📘 Main Knowledge

### Why Kubernetes

Across several hosts, two problems appear: **scheduling** (which container runs where?) and **networking** (how do containers on different hosts reach each other?). Kubernetes adds:

| Capability | Meaning |
|---|---|
| load balancing | spread requests across replicas |
| service discovery | find services by stable name, not IP |
| replication (HA) | several copies for availability |
| autoscaling | add or remove replicas with demand |
| self-healing | restart or reschedule failed containers |
| rollout | update versions without downtime |

Self-healing and rollouts are what Compose lacks and what canary and rolling releases need.

### kind and kubectl

- **kind** (Kubernetes IN Docker): runs Kubernetes nodes as Docker containers; for local development and CI; multi-node clusters on one machine.
- **kubectl**: the official CLI; works with any cluster through the API server.

No cloud account is needed. Docker Desktop may bundle `kubectl` (`kubectl version --client`; Settings → Kubernetes → Enable).

```powershell
# Windows, once as admin
New-Item -ItemType Directory -Force -Path C:\tools
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\tools", [EnvironmentVariableTarget]::User)
curl.exe -Lo kind.exe https://kind.sigs.k8s.io/dl/v0.31.0/kind-windows-amd64
Move-Item .\kind.exe C:\tools\kind.exe
kind version
```

### Clusters

```bash
kind create cluster --name mlops-cluster   # single node; sets context kind-mlops-cluster
```

`kind-three-node-cluster.yaml` (from the course repo):
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
Kubernetes orchestrates containers across nodes, so use at least three to see a realistic setup: scheduling across nodes, node affinity, DaemonSets.

```bash
kubectl config get-contexts && kubectl config current-context
kubectl get nodes                   # all Ready
kubectl get pods -n kube-system
kind get clusters
kind load docker-image fastapi:v2 --name mlops-cluster     # copy a local image into the nodes
docker exec -it mlops-cluster-control-plane crictl images  # images on a node
kind delete cluster --name mlops-cluster
```

A kind cluster can't see your local Docker images: its nodes have their own image stores. Load images explicitly or push them to a registry.

### Deployments and Services

The serving setup has two components, each with a Deployment and a Service:
- `app`: the FastAPI/Flask model server. Deployment for replicas and rollouts, Service to receive prediction requests.
- `db`: stores prediction logs, features or model metadata, reachable internally by a stable DNS name.

A **Deployment** manages pods: replica count, image, rollouts, restarts. A **Service** gives a stable name and load-balances across whatever pods currently exist (pod IPs change). Services find pods by **label**.

```bash
kubectl create deployment streamlit --image=manhtoannb87/streamlit:latest --port=8501
kubectl describe deploy streamlit
kubectl scale deploy streamlit --replicas=4
kubectl get pods
kubectl create service nodeport streamlit --tcp=8501 --node-port=30000

kubectl create deployment model --image=manhtoannb87/house-price-model:latest --port=8000 --replicas=2
kubectl create service nodeport model --tcp=8000 --node-port=30100
kubectl describe service model
```

A **NodePort** opens the same port (range 30000–32767) on every node: fine locally; production uses a LoadBalancer or Ingress.

### Connecting Streamlit to the model

In `streamlit_app/main.py`, `os.getenv("API_URL", "http://localhost:8000")` should point to `http://model:8000`, the Service name (as Compose used service names).

```bash
docker image build -t manhtoannb87/streamlit:v3 . && docker image push manhtoannb87/streamlit:v3
kubectl scale deploy streamlit --replicas=8
kubectl set image deploy/streamlit streamlit=manhtoannb87/streamlit:v3
kubectl rollout status deploy streamlit
kubectl rollout undo deploy/streamlit     # roll back
```
This is a rolling deployment ([[06 - Deployment]]).

## ✏️ Exercises

**1.** What does `kind load docker-image fastapi:v2 --name mlops-cluster` do, and what happens without it?

> [!example]- Solution
> kind nodes are containers running containerd with their own image store, so an image built on the host is invisible to them. The kubelet then tries a registry, where the image doesn't exist, and the pod sits in `ErrImagePull` / `ImagePullBackOff` (`kubectl describe pod` shows "Failed to pull image"). Fix: `kind load` (copies to every node; check with `crictl images`) or push to a registry, as the course does with Docker Hub.
> Separately, a `:latest` tag defaults to `imagePullPolicy: Always`, so Kubernetes tries to pull even a loaded image. Version tags default to `IfNotPresent`.

**2.** How do a Deployment and a Service differ, and why does `model` need both?

> [!example]- Solution
> The Deployment decides which pods exist: `--replicas=2` is desired state that Kubernetes keeps reconciling (kill a pod and a new one appears), and it runs rollouts. The Service decides how to reach them: a stable DNS name (`model`), load balancing across healthy pods, and decoupling from replica count.
> Without a Deployment, crashed pods stay dead and updates mean downtime. Without a Service, clients must track changing pod IPs.
> They are linked by labels: `create deployment model` labels pods `app=model`, and the Service selects that label. A wrong selector routes to nothing without error; check `Endpoints:` in `kubectl describe service`.

**3.** What happens when `kubectl set image` runs on a Deployment with 8 replicas? Which strategy is this?

> [!example]- Solution
> A rolling update (the default `RollingUpdate`). A new ReplicaSet for v3 scales up while the old one scales down. Defaults `maxSurge: 25%` and `maxUnavailable: 25%` give at most 10 pods and at least 6 available. New pods must be ready before old ones go. The old ReplicaSet stays at 0 replicas, which makes `rollout undo` instant.
> During the rollout both versions carry `app=streamlit`, so users get a mix: no downtime, but temporary version inconsistency.
> Without a readiness probe a pod counts as ready once its process starts, possibly before the model has loaded, and traffic is dropped:
> ```yaml
> readinessProbe:
>   httpGet: { path: /health, port: 8000 }
>   initialDelaySeconds: 10
>   periodSeconds: 5
> ```
> `kubectl create` can't set probes; production uses YAML with `kubectl apply -f`.

**4.** Why use a three-node cluster when one node runs the same containers?

> [!example]- Solution
> On one node every pod lands in the same place, so the two problems Kubernetes solves, scheduling and cross-host networking, never come up. With several nodes you can watch pods spread (`kubectl get pods -o wide`), test node affinity (GPU vs CPU nodes), see DaemonSets run one pod per node (Node Exporter in [[08 - Monitoring with Prometheus and Grafana]]), and test real HA: `kubectl drain` a worker and watch pods reschedule. With kind this costs three containers, not three machines.

**5.** (Advanced) Rewrite the model deployment as declarative YAML with production settings. Why is declarative preferred?

> [!example]- Solution
> ```yaml
> apiVersion: apps/v1
> kind: Deployment
> metadata: { name: model, labels: { app: model } }
> spec:
>   replicas: 2
>   selector: { matchLabels: { app: model } }
>   strategy:
>     type: RollingUpdate
>     rollingUpdate: { maxSurge: 1, maxUnavailable: 0 }
>   template:
>     metadata: { labels: { app: model } }
>     spec:
>       containers:
>         - name: model
>           image: manhtoannb87/house-price-model:v1.2.0
>           ports: [{ containerPort: 8000 }]
>           resources:
>             requests: { cpu: "500m", memory: "512Mi" }
>             limits: { cpu: "2000m", memory: "2Gi" }
>           readinessProbe:
>             httpGet: { path: /health, port: 8000 }
>             initialDelaySeconds: 15
>             periodSeconds: 5
>           livenessProbe:
>             httpGet: { path: /health, port: 8000 }
>             initialDelaySeconds: 30
>             periodSeconds: 20
> ---
> apiVersion: v1
> kind: Service
> metadata: { name: model }
> spec:
>   type: NodePort
>   selector: { app: model }
>   ports: [{ port: 8000, targetPort: 8000, nodePort: 30100 }]
> ```
> Declarative manifests live in Git (reviewable, auditable); `kubectl apply` is idempotent, while `create` fails with `AlreadyExists`, so CI can apply on every merge; and only YAML can express probes, resources, strategy, volumes and affinity.
> `maxUnavailable: 0` keeps full capacity during rollouts. Requests drive scheduling (without them nodes get overcommitted and pods OOM-killed); limits stop one pod starving others. Readiness removes a pod from the Service; liveness restarts it, and a liveness delay shorter than model loading causes a restart loop. A HorizontalPodAutoscaler on custom metrics is the next step.

## 📝 Summary

- Kubernetes solves scheduling and cross-host networking and adds load balancing, discovery, replication, autoscaling, self-healing and rollouts.
- kind runs nodes as Docker containers; kubectl talks to the API server.
- Load local images into kind or push them to a registry.
- Deployments manage pods; Services give stable names and load balancing; labels link them.
- NodePort for local work; LoadBalancer or Ingress in production.
- `kubectl set image` triggers a rolling update; `rollout undo` reverts it.
- Use three nodes; prefer declarative YAML.

## ⚠️ Important Notes

1. Local images need `kind load docker-image`.
2. `:latest` implies `imagePullPolicy: Always`.
3. Without readiness probes, rollouts route traffic to pods still loading the model.
4. Readiness ≠ liveness; a short liveness delay causes restart loops.
5. Services select by label; check `Endpoints:`.
6. Never hardcode pod IPs.
7. `kubectl create` can't set probes or resources.
8. Set resource requests and limits.
9. Default `maxUnavailable: 25%` loses capacity during rollouts.
10. Rolling updates mix versions; watch API compatibility.
11. NodePort is 30000–32767 and exposes every node.
12. A single node hides what Kubernetes is for.

> [!warning] Gaps in the source slides
> - Slides 3–5 ("Scalable Infrastructure for Model Inference", "Why Kubernetes") have titles only, and slide 7 (K8s architecture: API server, scheduler, etcd, kubelet, kube-proxy) is an image and can't be recovered. Slide 20 ("Deployment Pattern") is an image; slides 2, 8, 12, 17, 26 have no text.
> - Truncated: slides 9, 13, 19 (visualizer repo URL ends at `schoolofdevops/kube`), 21, 24 (the `kubectl set image` command, reconstructed).
> - The deck shows no YAML apart from the kind config; Exercise 5's manifest is mine.
> - Links: kind quick start, kubectl reference, `github.com/NguyenMToan/house-price-predictor`.

**Previous:** [[06 - Deployment]] · **Next:** [[08 - Monitoring with Prometheus and Grafana]]
