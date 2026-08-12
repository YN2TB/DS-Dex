---
subject: MLOps
chapter: 05
tags: [ds, mlops, fastapi, streamlit, docker-compose, serving, packaging]
source: "MLOps_Packaging_Model.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# Packaging ML Models with FastAPI and Docker Compose

> [!note] Where this sits in the course
> The handover point. [[04 - Model Development]] produced a `.pkl` file; this chapter turns it into something **other systems can call**. It is the first hands-on chapter, built around a single running project — `house-price-predictor` — and it uses the Docker skills from [[02 - Environment Setup]].

## 📘 Main Knowledge

### The reproducible pipeline

```
house-price-predictor/
├── configs/            # YAML-based configuration for models
├── data/               # Raw and processed datasets
├── deployment/
│   └── mlflow/         # Docker Compose setup for MLflow
├── models/             # Trained models and preprocessors
├── notebooks/          # Jupyter notebooks for experimentation
├── src/
│   ├── data/           # Data cleaning and preprocessing
│   ├── features/       # Feature engineering pipeline
│   └── models/         # Model training and evaluation
├── requirements.txt
└── README.md
```

The structure enforces the separation [[02 - Environment Setup]] insisted on: **notebooks for exploration, `src/` for production code**.

**Step 1 — Data processing:**
```bash
python src/data/run_processing.py \
  --input data/raw/house_data.csv \
  --output data/processed/cleaned_house_data.csv
```
`data/raw/` is **read-only — never overwritten**, so the original is always available for reprocessing.

**Step 2 — Feature engineering:**
```bash
python src/features/engineer.py \
  --input data/processed/cleaned_house_data.csv \
  --output data/processed/featured_house_data.csv \
  --preprocessor models/trained/preprocessor.pkl
```
Note the `--preprocessor` output: the **fitted** transformer is saved as an artefact. It must be applied identically at inference time — the training/serving parity requirement from [[03 - Data in MLOps]].

**Step 3 — Model training:**
```bash
python src/models/train_model.py \
  --config configs/model_config.yaml \
  --data data/processed/featured_house_data.csv \
  --models-dir models \
  --mlflow-tracking-uri http://localhost:5555
```

| Argument | Purpose |
|---|---|
| `--config` | YAML hyperparameters. **Externalising config avoids hardcoding and enables experiment sweeps.** |
| `--models-dir` | Where `.pkl`/`.pt` artefacts are saved. Centralised under `models/` and **added to `.gitignore`**. |
| `--mlflow-tracking-uri` | Where to log metrics, parameters, and artefacts (`mlflow server --port 5555`). |

> **Key design principle: each step's `--output` is the next step's `--input`.** This explicit chaining makes every pipeline run fully **reproducible and automatable in CI/CD**.

That chaining is what makes the pipeline a **DAG** — see [[09 - CI-CD with GitHub Actions]].

### From notebook to production

**The problem:**
- A trained model is just a `.pkl`/`.pt` file.
- Data scientists work in notebooks — **other systems cannot call them**.
- Models need a **standard interface** to receive input and return predictions.
- Business users need a **UI** to interact with the model.

**The solution:** **FastAPI** exposes the model as a REST API; **Streamlit** builds an interactive web UI. Both are pure Python and both containerisable.

```
Jupyter Notebook --train--> model.pkl --> FastAPI (REST API) --> Streamlit (Web App)
                                              [ Docker Container ]
```

### FastAPI

> A modern, high-performance Python web framework for building REST APIs, built on **Starlette** (ASGI) and **Pydantic** (data validation), with full `async/await` support.

**Key features:** fast — on par with Node.js and Go · **automatic docs** — Swagger UI at `/docs`, ReDoc at `/redoc` · **type-safe** — Pydantic validates all inputs · async-native · dependency injection built in.

```bash
uv add fastapi uvicorn
uv run uvicorn main:app --reload          # development
uv run uvicorn main:app --host 0.0.0.0    # production
```

**Project structure:**
```
/app/
├── main.py           # App entry point, routes
├── inference.py      # Model loading & prediction logic
├── schemas.py        # Pydantic request/response models
├── models/
│   └── trained/
│       ├── house-price-model.pkl    # Serialised model artefact
│       └── preprocessor.pkl         # Fitted preprocessing pipeline
└── requirements.txt
```

> **Entry point convention:** `main:app` tells uvicorn — file `main.py` ▷ object `app = FastAPI()`.

Note that **both** the model *and* the preprocessor are shipped. Serving the model without its fitted preprocessor guarantees train/serve skew.

### Streamlit

> A pure-Python library that turns a Python script into an interactive web application — **no HTML, CSS, or JavaScript required.**

**Key features:** pure Python (`st.` calls) · **reactive** — re-runs the script on every interaction · rich widgets (sliders, selects, file upload, chat input) · native plots (Matplotlib, Plotly, Altair, Vega) · **caching** — `@st.cache_resource` for models, `@st.cache_data` for data · Streamlit Cloud for free public hosting.

```bash
uv add streamlit
uv run streamlit run app.py
```

`@st.cache_resource` matters in production: without it, Streamlit's reactive model reloads the model file **on every widget interaction**, making the app unusably slow.

### Containerising the API

```dockerfile
FROM python:3.11-slim                     # Base image
WORKDIR /app                              # Working directory
COPY src/api/ .                           # Copy project files
RUN pip install -r requirements.txt       # Install dependencies
COPY models/trained/*.pkl models/trained/ # Copy models
EXPOSE 8000                               # Expose port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> `--host 0.0.0.0` is **mandatory in a container.** The default `127.0.0.1` binds only to the container's own loopback, so the port mapping works but no traffic ever reaches the app.

```bash
docker image build -t fastapi .
docker run -idtP fastapi
```

**Debugging workflow** when the container fails:
```bash
docker ps -l                        # most recently created container
docker logs <container_id>          # all output from the container
docker run --rm -it fastapi bash    # debug shell inside the container
```
Typical cause: a **library version mismatch**. Update `requirements.txt`, reinstall, exit (the container is deleted because of `--rm`), and rebuild as `fastapi:v2`.

**Streamlit container:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app.py requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
```

### Connecting services with Docker Compose

```yaml
services:
  fastapi:
    image: fastapi:dev
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - 8000:8000
  streamlit:
    image: streamlit:dev
    build:
      context: ./streamlit_app
      dockerfile: Dockerfile
    ports:
      - 8501:8501
    environment:
      API_URL: http://fastapi:8000
```

- **FastAPI** builds from `.`, runs on port 8000, reachable at `http://localhost:8000`.
- **Streamlit** builds from `./streamlit_app`, runs on 8501, reachable at `http://localhost:8501`.

> **Communication:** Docker Compose creates a network, and each service can talk to others **using the service name**. Inside Streamlit, `http://fastapi:8000` resolves — `fastapi` is the *service name*, 8000 the port exposed **inside** the container.

| Feature | `docker compose up -d` | `docker compose build` |
|---|---|---|
| Builds images | Yes (if needed) | Yes |
| Starts containers | **Yes** | No |
| Runs application | **Yes** | No |
| Detached mode | Yes (`-d`) | No |
| Use case | Run the full application | Prepare/update images |

## ✏️ Exercises

**1.** Explain why `--host 0.0.0.0` is required in the Dockerfile's `CMD`, and what symptom appears without it.

> [!example]- Solution
> **The symptom is the confusing part: `docker ps` shows the container running and the port mapped, but `curl http://localhost:8000` returns "connection reset" or "empty reply". No error appears in the logs** — uvicorn reports it started successfully.
>
> **Why.** Uvicorn defaults to binding `127.0.0.1`, the **loopback interface**. Inside a container, that loopback belongs to the *container's* network namespace, not the host's. So uvicorn is listening — but only for connections originating inside the container itself.
>
> `docker run -p 8000:8000` forwards host port 8000 to the *container's* port 8000 on its **external** interface. Traffic arrives at an interface where nothing is listening.
>
> `--host 0.0.0.0` means "bind all interfaces", so uvicorn accepts connections arriving from outside the container, and the port mapping works.
>
> **Verify from inside:**
> ```bash
> docker exec -it <id> curl http://localhost:8000/   # works — inside the namespace
> curl http://localhost:8000/                        # fails — from the host
> ```
> Same for Streamlit, hence `--server.address=0.0.0.0`.
>
> On a developer laptop `127.0.0.1` is the safer default, which is why frameworks choose it — binding all interfaces exposes the dev server to the local network. In a container the isolation boundary is the container itself, so `0.0.0.0` is correct **and** still isolated, since only explicitly mapped ports are reachable.

**2.** In the Compose file, Streamlit is given `API_URL: http://fastapi:8000`. Explain why `http://localhost:8000` would fail, and why the port is 8000 rather than the mapped host port.

> [!example]- Solution
> **`localhost` fails because each container has its own network namespace.** From inside the Streamlit container, `localhost` means *the Streamlit container itself* — where nothing listens on 8000. The two services are as isolated from each other as two separate machines.
>
> **Compose creates a network and a DNS entry per service**, so `fastapi` resolves to the FastAPI container's IP. Using the service name is also more robust than an IP, since container IPs change on every restart.
>
> **Why 8000 and not the host-mapped port:** `ports: - 8000:8000` maps `host:container`. That mapping exists **only for traffic from the host**. Container-to-container traffic travels over the Compose network directly to the container's **internal** port, bypassing the mapping entirely.
>
> So if the mapping were `ports: - 9000:8000` (host 9000 → container 8000):
> - From your browser: `http://localhost:9000` ✓
> - From the Streamlit container: still `http://fastapi:8000` ✓ — the internal port is unchanged.
>
> **The practical consequence: `ports:` is only needed for services humans access.** If Streamlit is the only consumer of the API, the FastAPI `ports:` block could be dropped entirely and inter-service communication would still work — while removing the API from external exposure, which is better security. Backend databases in a Compose stack are normally configured exactly this way.
>
> Passing the URL via `environment:` rather than hardcoding it follows the [[02 - Environment Setup]] rule — environment variables for config — and lets the same image run locally, in staging, and in Kubernetes with only the variable changing.

**3.** Both `house-price-model.pkl` **and** `preprocessor.pkl` are copied into the API container. Explain why shipping only the model would be a serious bug.

> [!example]- Solution
> **The model was trained on *transformed* features, not raw ones.** In Step 2 the pipeline fitted a preprocessor — scaling, encoding, imputation — and saved it. The model has only ever seen the output of that transformation.
>
> At inference, the API receives **raw** user input: `{"sqft": 1800, "neighborhood": "Downtown", "bedrooms": 3}`. Feeding that straight to the model either raises (a string where a number is expected) or, far worse, **silently produces nonsense** — the model interprets an unscaled 1800 as though it were a standardised value near 0, and predicts wildly.
>
> ```python
> # inference.py — correct
> preprocessor = joblib.load("models/trained/preprocessor.pkl")
> model        = joblib.load("models/trained/house-price-model.pkl")
>
> def predict(raw_input: dict):
>     X = preprocessor.transform(pd.DataFrame([raw_input]))   # transform, NEVER fit
>     return model.predict(X)[0]
> ```
>
> **`transform`, never `fit_transform`.** Calling `fit_transform` at inference would recompute the scaling statistics from the single incoming request — meaning a request's own value becomes its own mean, and every prediction is computed in a different coordinate system. This is the serving-side face of the leakage discipline in [[Data Preparation and Visualization/contents/09 - Building Pipelines|Building Pipelines]].
>
> **This failure mode is exactly what [[03 - Data in MLOps]] calls training–serving parity**, and what the fraud case study's **feature store** exists to prevent. The most dangerous version is not a crash but **silent skew** — the API returns plausible-looking numbers that are simply wrong, and no monitor catches it because nothing errored.
>
> **The cleaner design** is to save the preprocessor and model as a single scikit-learn `Pipeline`, so one artefact cannot be deployed without the other:
> ```python
> mlflow.sklearn.log_model(full_pipeline, artifact_path="model")
> ```

**4.** Walk through the debugging sequence on slide 19. Why is `docker run --rm -it fastapi bash` the right diagnostic, and what does `--rm` do?

> [!example]- Solution
> **The sequence and what each step buys you:**
>
> 1. **`docker ps -l`** — the container exited immediately, so it does not appear in plain `docker ps` (which shows only *running* containers). `-l` shows the **last created** container regardless of state, giving you its ID.
> 2. **`docker logs <id>`** — prints everything the container wrote to stdout/stderr before dying, which is where the Python traceback lives. A crashed container is not gone; its logs persist until it is removed.
> 3. **`docker run --rm -it fastapi bash`** — **overrides the `CMD`**. Instead of running uvicorn (which crashes), it runs `bash`, giving an interactive shell **inside the exact image** that is failing.
>
> **Why step 3 is the right diagnostic:** the whole point of a container is that its environment differs from your laptop's. Reproducing the bug locally may be impossible — the versions differ. A shell inside the image lets you inspect the *actual* environment: run `pip list` to see resolved versions, `ls models/trained/` to confirm the artefacts were copied, and `python -c "import joblib; joblib.load(...)"` to reproduce the failure line by line.
>
> This is the fastest route to the slide's diagnosed cause — a **library version mismatch**, typically a model pickled with one scikit-learn version and loaded under another, which raises on unpickling or, worse, loads with subtly different behaviour.
>
> **`--rm` deletes the container when the shell exits** — hence the slide's note that it "will be deleted since we use `--rm`". Debug containers are throwaway; without `--rm` every session leaves a stopped container behind, which is exactly the accumulation [[02 - Environment Setup]] warns about.
>
> **The root fix is pinning.** `requirements.txt` with `scikit-learn` unpinned resolves to whatever is newest at build time, so an image that built fine last month breaks today with no code change — the same class of problem as `FROM python:latest`. Pin every version, or use `uv.lock`.

**5.** (Advanced) The Compose file rebuilds both images from source. Redesign it for production, explaining what changes and why.

> [!example]- Solution
> The development file is right for development — `build:` gives fast iteration. **For production it is wrong in five ways.**
>
> ```yaml
> services:
>   fastapi:
>     image: manhtoannb87/fastapi:v1.2.0      # PULLED, not built; pinned, not :latest
>     restart: unless-stopped
>     expose:
>       - 8000                                 # internal only — no host mapping
>     environment:
>       MODEL_PATH: /app/models/trained/house-price-model.pkl
>     healthcheck:
>       test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
>       interval: 30s
>       timeout: 5s
>       retries: 3
>     deploy:
>       resources:
>         limits: { cpus: "2.0", memory: 2G }
>
>   streamlit:
>     image: manhtoannb87/streamlit:v1.2.0
>     restart: unless-stopped
>     ports:
>       - 8501:8501                            # the only public entry point
>     environment:
>       API_URL: http://fastapi:8000
>     depends_on:
>       fastapi:
>         condition: service_healthy           # wait for READY, not just started
> ```
>
> **1. Pull pinned images instead of building.** Production must run the **exact artefact CI tested**, not a rebuild that might resolve different dependencies. This is why [[09 - CI-CD with GitHub Actions]] pushes to a registry — and why the tag is `v1.2.0`, not `:latest`, so rollback is possible.
>
> **2. Remove the FastAPI host port.** Only Streamlit needs external exposure; the API is reached over the Compose network (Exercise 2). `expose:` documents the internal port without publishing it, shrinking the attack surface.
>
> **3. Add health checks.** Without one, Docker considers a container "running" even if the model failed to load and every request 500s. A `/health` endpoint that verifies the model is loaded turns a silent failure into a restart.
>
> **4. `depends_on` with `condition: service_healthy`.** Plain `depends_on` only waits for the container to *start*, not to be *ready* — so Streamlit can come up while FastAPI is still loading a large model, and its first requests fail. The health condition fixes the race.
>
> **5. `restart: unless-stopped` and resource limits.** Recover from crashes automatically, and prevent one runaway container from starving the host.
>
> **The honest caveat:** Compose is a **single-host** tool. It cannot do rolling updates, horizontal autoscaling, or multi-node scheduling. Once you need any of those, the answer is Kubernetes — [[07 - Kubernetes for ML Deployment]] and [[08 - Monitoring with Prometheus and Grafana]]. Compose remains excellent for development, CI, and small single-server deployments.

## 📝 Summary

- **Each pipeline step's `--output` is the next step's `--input`** — explicit chaining makes runs reproducible and CI-automatable.
- **`data/raw/` is read-only**; config lives in YAML, artefacts in `models/` (gitignored), experiments in MLflow.
- **A `.pkl` is not a product.** FastAPI provides the machine interface; Streamlit provides the human one.
- **FastAPI** — Starlette + Pydantic, type-safe, async, with automatic Swagger docs at `/docs`. Entry point convention `main:app`.
- **Streamlit** — pure Python UI, reactive (re-runs on every interaction), so cache models with `@st.cache_resource`.
- **`--host 0.0.0.0` is mandatory in containers**, or the port mapping silently delivers nothing.
- **Ship the preprocessor with the model**, and call `transform`, never `fit_transform`, at inference.
- **Compose creates a network with DNS by service name**; use the container's **internal** port, not the host-mapped one.
- **`docker compose build` prepares images; `up -d` builds if needed and runs them.**

## ⚠️ Important Notes

**`--host 0.0.0.0` failures are silent.** The container runs, the port maps, and connections are refused with nothing in the logs.

**Deploying a model without its fitted preprocessor causes silent train/serve skew** — plausible-looking predictions that are simply wrong. Prefer packaging both as one scikit-learn `Pipeline`.

**Never call `fit_transform` at inference.** It refits scaling statistics on a single request.

**Unpinned `requirements.txt` breaks images over time.** An image that built last month can fail today with no code change; a model pickled under one scikit-learn version may not load under another.

**Use the internal port for service-to-service calls.** Host port mappings apply only to traffic from the host.

**`ports:` is only needed for services humans reach.** Everything else should stay internal to the Compose network.

**Plain `depends_on` waits for start, not readiness.** A large model can still be loading when dependents begin sending requests. Use a health check with `condition: service_healthy`.

**Streamlit re-runs the entire script on every interaction.** Without `@st.cache_resource`, the model reloads on each slider move.

**`docker compose build` does not start anything.** Running it and expecting a live app is a common early mistake.

**Debug containers need `--rm`**, or every session leaves a stopped container behind.

**Compose is single-host.** It has no rolling updates, no autoscaling, no multi-node scheduling — that is Kubernetes' job.

**Never bake credentials into an image.** Layers are permanent even if a later layer deletes the file.

> [!warning] Gaps in the source slides
> This is a **hands-on lab deck**, so it leans heavily on figures and live demonstration:
> - **Slides 2–3 — "Role Involvement" and "Handover from Data Scientist to ML"** are entirely images. The framing of *who* hands over *what* is therefore not captured.
> - **Slides 4, 11, 15** produced no text — section dividers.
> - **Slide 21 — "Docker Compose: Packaging and Model Serving Infra"** is a title-only slide; the architecture diagram is an image.
> - **Several code and table cells truncate:** slide 6 (the `--output` explanation, cut at "making"), slide 7 (`--preprocessor` row), slide 8 (`--data` row, cut at "Input datas"), slide 13 (the production uvicorn command, cut at `--host 0.0.0`), slide 14 (`uv run streamlit`, cut at "stre"), slide 19 (the final test-run step, cut at "Test ru").
> - **No actual application code is shown** — `main.py`, `inference.py`, `schemas.py`, and `app.py` are named in the structure but never displayed. The FastAPI route definitions, Pydantic schemas, and Streamlit UI code must come from the repository or the live session.
>
> **Links:** [FastAPI](https://fastapi.tiangolo.com/) · [Streamlit](https://streamlit.io/)
>
> The running project is `house-price-predictor`; the companion repository appears in [[09 - CI-CD with GitHub Actions]] as `github.com/NguyenMToan/house-price-predictor`.

---
**Previous:** [[04 - Model Development]] · **Next:** [[06 - Deployment]]
