---
subject: MLOps
chapter: 05
tags: [ds, mlops, fastapi, streamlit, docker-compose, serving, packaging]
source: "MLOps_Packaging_Model.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# Packaging ML Models with FastAPI and Docker Compose

[[04 - Model Development]] produced a `.pkl` file; this chapter turns it into something other systems can call. It is the first hands-on lab, built around the `house-price-predictor` project, and uses the Docker skills from [[02 - Environment Setup]].

## 📘 Main Knowledge

### A reproducible pipeline

```
house-price-predictor/
├── configs/            # YAML model configuration
├── data/               # raw and processed data
├── deployment/mlflow/  # Docker Compose setup for MLflow
├── models/             # trained models and preprocessors
├── notebooks/          # experimentation
├── src/{data,features,models}/
├── requirements.txt
└── README.md
```

```bash
python src/data/run_processing.py --input data/raw/house_data.csv \
  --output data/processed/cleaned_house_data.csv
python src/features/engineer.py --input data/processed/cleaned_house_data.csv \
  --output data/processed/featured_house_data.csv \
  --preprocessor models/trained/preprocessor.pkl
python src/models/train_model.py --config configs/model_config.yaml \
  --data data/processed/featured_house_data.csv --models-dir models \
  --mlflow-tracking-uri http://localhost:5555
```

- `data/raw/` is read-only, so you can always reprocess from the original.
- The fitted preprocessor is saved as an artifact and must be applied identically at inference (training–serving parity, [[03 - Data in MLOps]]).
- `--config` keeps hyperparameters out of the code and makes sweeps easy; `--models-dir` keeps artifacts under `models/` (gitignored); `--mlflow-tracking-uri` points to `mlflow server --port 5555`.
- **Each step's `--output` is the next step's `--input`**, so runs are reproducible and can be automated in CI ([[09 - CI-CD with GitHub Actions]]).

### From notebook to service

A model file can't be called by other systems, and a notebook isn't an interface. **FastAPI** exposes the model as a REST API; **Streamlit** gives business users a web UI. Both are pure Python and containerizable:

```
notebook → model.pkl → FastAPI (REST) → Streamlit (web app), each in a container
```

### FastAPI

A Python web framework built on Starlette (ASGI) and Pydantic (validation), with `async/await`. Fast, type-checked inputs, automatic docs at `/docs` (Swagger) and `/redoc`, dependency injection.

```bash
uv add fastapi uvicorn
uv run uvicorn main:app --reload        # development
uv run uvicorn main:app --host 0.0.0.0  # production
```
`main:app` means file `main.py`, object `app = FastAPI()`. Structure: `main.py` (routes), `inference.py` (loading and prediction), `schemas.py` (Pydantic models), `models/trained/house-price-model.pkl` and `preprocessor.pkl`. Ship both: a model without its fitted preprocessor guarantees train/serve skew.

### Streamlit

Turns a Python script into a web app with no HTML, CSS or JavaScript: widgets, native plots, free Streamlit Cloud hosting. It re-runs the whole script on every interaction, so cache the model with `@st.cache_resource` (and data with `@st.cache_data`), or the model reloads at every slider move.

```bash
uv add streamlit
uv run streamlit run app.py
```

### Containers

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY src/api/ .
RUN pip install -r requirements.txt
COPY models/trained/*.pkl models/trained/
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`--host 0.0.0.0` is required in a container: the default `127.0.0.1` listens only on the container's own loopback, so mapped traffic never arrives. (Copying `requirements.txt` alone before the source would cache the install better, as in ch. 02.)

```bash
docker image build -t fastapi .
docker run -idtP fastapi
docker ps -l                       # last created container, even if it exited
docker logs <container_id>         # the traceback
docker run --rm -it fastapi bash   # shell inside the failing image
```
The usual cause is a library version mismatch: fix `requirements.txt`, rebuild as `fastapi:v2`. The Streamlit image is similar (`python:3.9-slim`, port 8501, `CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]`).

### Docker Compose

```yaml
services:
  fastapi:
    image: fastapi:dev
    build: { context: ., dockerfile: Dockerfile }
    ports: ["8000:8000"]
  streamlit:
    image: streamlit:dev
    build: { context: ./streamlit_app, dockerfile: Dockerfile }
    ports: ["8501:8501"]
    environment:
      API_URL: http://fastapi:8000
```

Compose creates a network where services reach each other **by service name**: inside Streamlit, `http://fastapi:8000` resolves to the API container on its internal port.

| | `docker compose up -d` | `docker compose build` |
|---|---|---|
| builds images | if needed | yes |
| starts containers | yes | no |
| use | run the application | prepare images |

## ✏️ Exercises

**1.** Why does the Dockerfile's `CMD` need `--host 0.0.0.0`? What happens without it?

> [!example]- Solution
> The container runs, `docker ps` shows the port mapped, uvicorn logs a successful start, but `curl localhost:8000` from the host gets "connection reset" or an empty reply.
> Uvicorn defaults to `127.0.0.1`, the loopback of the container's own network namespace. `-p 8000:8000` forwards traffic to the container's external interface, where nothing listens. `0.0.0.0` binds all interfaces. Check: `docker exec -it <id> curl localhost:8000` works inside, while the host request fails. On a laptop `127.0.0.1` is the safer default; in a container only mapped ports are reachable anyway.

**2.** Streamlit gets `API_URL: http://fastapi:8000`. Why would `http://localhost:8000` fail, and why 8000 rather than the host port?

> [!example]- Solution
> Inside the Streamlit container, `localhost` is the Streamlit container itself. Compose gives each service a DNS name, which also survives IP changes on restart.
> `ports: host:container` applies only to traffic from the host. Container-to-container traffic goes straight to the internal port. With `9000:8000`, the browser uses `localhost:9000` but Streamlit still uses `fastapi:8000`.
> So only services people reach need `ports:`; the API could drop its mapping and stay private. Passing the URL as an environment variable lets the same image run anywhere.

**3.** Why would shipping only `house-price-model.pkl` without `preprocessor.pkl` be a serious bug?

> [!example]- Solution
> The model has only seen transformed features. Raw input like `{"sqft": 1800, "neighborhood": "Downtown"}` either errors (a string where a number is expected) or, worse, is taken as if 1800 were a standardized value and gives a confident wrong prediction.
> ```python
> preprocessor = joblib.load("models/trained/preprocessor.pkl")
> model = joblib.load("models/trained/house-price-model.pkl")
>
> def predict(raw_input: dict):
>     X = preprocessor.transform(pd.DataFrame([raw_input]))  # transform, never fit
>     return model.predict(X)[0]
> ```
> `fit_transform` at inference would refit the statistics on one request. Saving one scikit-learn `Pipeline` (`mlflow.sklearn.log_model(full_pipeline, "model")`) makes it impossible to deploy one part without the other.

**4.** Walk through the slide-19 debugging sequence. Why `docker run --rm -it fastapi bash`, and what does `--rm` do?

> [!example]- Solution
> `docker ps -l` finds the exited container (plain `docker ps` shows only running ones); `docker logs` shows its traceback. `docker run -it fastapi bash` overrides `CMD` and opens a shell in the exact failing image, where you can run `pip list`, check `ls models/trained/`, and load the pickle by hand. That is how you find a model pickled under one scikit-learn version and loaded under another. `--rm` deletes the container on exit so debug sessions don't pile up. The root fix is pinning versions (or `uv.lock`).

**5.** (Advanced) Redesign the Compose file for production.

> [!example]- Solution
> ```yaml
> services:
>   fastapi:
>     image: <registry>/fastapi:v1.2.0     # pulled and pinned, not built
>     restart: unless-stopped
>     expose: ["8000"]                     # internal only
>     healthcheck:
>       test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
>       interval: 30s
>       timeout: 5s
>       retries: 3
>     deploy:
>       resources:
>         limits: { cpus: "2.0", memory: 2G }
>   streamlit:
>     image: <registry>/streamlit:v1.2.0
>     restart: unless-stopped
>     ports: ["8501:8501"]                 # the only public entry point
>     environment:
>       API_URL: http://fastapi:8000
>     depends_on:
>       fastapi: { condition: service_healthy }
> ```
> 1. Run the exact image CI tested, with a version tag so rollback is possible.
> 2. Keep the API off the host network.
> 3. A `/health` endpoint that checks the model loaded turns silent failure into a restart. `python:3.11-slim` has no `curl`, so the check uses Python (or install `curl` in the image).
> 4. Plain `depends_on` waits for start, not readiness; `service_healthy` waits until the model has loaded.
> 5. Restart policy and resource limits.
>
> Compose runs on one host: no rolling updates, autoscaling or multi-node scheduling. For those, use Kubernetes ([[07 - Kubernetes for ML Deployment]]).

## 📝 Summary

- Chain pipeline steps by `--output` → `--input`; raw data read-only; config in YAML; artifacts in `models/`; experiments in MLflow.
- FastAPI is the machine interface (Pydantic validation, `/docs`); Streamlit the human one (cache the model).
- `--host 0.0.0.0` in containers.
- Ship the preprocessor with the model and call `transform` at inference.
- Compose services talk by service name on internal ports.
- `compose build` prepares images; `compose up -d` runs them.

## ⚠️ Important Notes

1. A wrong host binding fails silently.
2. A model without its preprocessor gives plausible wrong predictions.
3. Never `fit_transform` at inference.
4. Unpinned requirements break images over time; pickles may not load across scikit-learn versions.
5. Service-to-service calls use internal ports.
6. Publish ports only for services people reach.
7. `depends_on` doesn't wait for readiness; use health checks.
8. Slim images have no `curl`; write health checks accordingly.
9. Streamlit re-runs the script on every interaction.
10. `compose build` doesn't start anything.
11. Use `--rm` for debug containers.
12. Never bake credentials into image layers.

> [!warning] Gaps in the source slides
> - Slides 2–3 ("Role Involvement", "Handover from Data Scientist to ML") and slide 21's Compose architecture are images; slides 4, 11, 15 have no text.
> - Truncated: slides 6, 7, 8, 13 (production uvicorn command), 14, 19 (final test step).
> - `main.py`, `inference.py`, `schemas.py` and `app.py` are named but never shown; they are in `github.com/NguyenMToan/house-price-predictor`.
> - Exercise 5's production Compose file is mine, not the lecturer's.
> - Links: FastAPI and Streamlit documentation.

**Previous:** [[04 - Model Development]] · **Next:** [[06 - Deployment]]
