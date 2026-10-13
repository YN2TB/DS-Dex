---
subject: MLOps
chapter: 02
tags: [ds, mlops, docker, git, uv, reproducibility, tooling]
source: "MLOps_Environment_Setup.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# Environment Setup

The practical answer to "reproducibility is often missing" ([[01 - Introduction to MLOps]]), in four layers: virtual environments (Python packages), editors, containers (the whole OS), Git (history and collaboration). Each layer covers what the previous one can't.

## 📘 Main Knowledge

### 1. Virtual environments

**Dependency hell:** project A needs `numpy==1.21`, project B `numpy==1.26`, and only one can be installed globally. System Python gets polluted, setups can't be reproduced elsewhere, and dev ≠ production.

A **virtual environment** is an isolated Python installation with its own interpreter (copy or symlink), `site-packages/`, pip, scripts and `activate` script. It does not duplicate the stdlib, does not manage Python versions (`venv` uses whatever created it), and does not isolate system libraries, network or filesystem. Rule: **one project, one environment.**

| Feature | `venv` | `conda` | `uv` |
|---|---|---|---|
| Speed | medium | slow | very fast (Rust; 10–100× pip) |
| Python version management | no | yes | yes |
| Non-Python libs (CUDA, MKL) | no | yes | no |
| Lock file | no | `environment.yml` | `uv.lock` |
| Needs install | no (stdlib) | yes | yes (small) |
| Docker-friendly | yes | partly | yes |

`venv` suits scripts and teaching, `conda` GPU/CUDA work, and `uv` is the course recommendation.

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux; Windows: .venv\Scripts\Activate.ps1
pip install numpy pandas scikit-learn
pip freeze > requirements.txt

conda create -n ml-project python=3.11 && conda activate ml-project
conda install numpy pandas && pip install scikit-learn mlflow
conda env export > environment.yml     # conda env create -f environment.yml elsewhere

uv init my-ml-project && cd my-ml-project
uv venv .venv --python 3.11
uv add numpy pandas scikit-learn torch # updates pyproject.toml and uv.lock
uv sync                                # rebuild the env from uv.lock
uv run python train.py
```

| Task | `uv` | `pip` + `venv` |
|---|---|---|
| create | `uv venv .venv` | `python -m venv .venv` |
| install | `uv add numpy` | `pip install numpy` |
| install from file | `uv sync` | `pip install -r requirements.txt` |
| lock | `uv lock` | `pip freeze > requirements.txt` |
| run | `uv run train.py` | `python train.py` |

`uv.lock` is cross-platform and maintained automatically; `pip freeze` is a snapshot of one machine. Commit `pyproject.toml` and `uv.lock`, never `.venv/`. Pin versions, separate dev and production dependencies, record the Python version. With conda, install conda packages first and pip packages last.

### 2. Editors

Needs: highlighting and autocomplete, venv integration, debugger, Git, terminal; for ML also notebooks, inline plots, remote/SSH and container development.

| Editor | Character |
|---|---|
| VS Code (course tool) | free, extensions, Python and Jupyter built in, Remote SSH, Dev Containers |
| JupyterLab | browser-based, notebook-first |
| PyCharm | full IDE, strong debugger, heavy |

Select the interpreter (`Python: Select Interpreter` → `.venv/bin/python`) and set `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "editor.formatOnSave": true,
  "[python]": { "editor.defaultFormatter": "ms-python.black-formatter" },
  "jupyter.notebookFileRoot": "${workspaceFolder}"
}
```

Notebooks: keep them linear, explain why in Markdown, restart and run all before committing, one per experiment, move final logic to `.py` modules. Don't store data or large outputs in them. **Notebooks are for exploration; production code lives in `src/`.**

### 3. Containers

"It works on my machine": different OS versions, CUDA/cuDNN mismatches, system libraries (`libgomp`, `libssl`), Python version drift. A venv can't fix OS-level differences, so package the OS, system libraries, Python, packages and code together.

| Property | Virtual env | Container | VM |
|---|---|---|---|
| isolates Python packages | yes | yes | yes |
| isolates system libraries | no | yes | yes |
| isolates OS | no | shares host kernel | full OS |
| startup | instant | seconds | minutes |
| size | MB | MB–GB | GB |
| portability | low | very high | medium |
| GPU | native | yes (NVIDIA runtime) | limited |

**Venvs for development, containers for deployment and CI/CD.**

- **Image**: read-only blueprint built from a **Dockerfile**.
- **Container**: a running instance; isolated filesystem, network, PIDs; ephemeral by default.
- **Registry**: Docker Hub, `ghcr.io`, AWS ECR, Google Artifact Registry.

Flow: Dockerfile → build → image → push → registry → pull → container. Docker needs a root daemon; Podman is daemonless and rootless. The course uses Docker.

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libgomp1 curl && \
    rm -rf /var/lib/apt/lists/*
RUN pip install uv
COPY pyproject.toml uv.lock ./     # dependency files first
RUN uv sync --frozen               # cached layer
COPY src/ ./src/                   # code last
CMD ["uv", "run", "python", "src/train.py"]
```

**Layer caching:** Docker reuses a layer only if it and every earlier instruction are unchanged. Order instructions from least to most frequently changed, so editing code doesn't reinstall dependencies. `--frozen` fails instead of updating the lock file.

GPU images start from `nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04`, set `NVIDIA_VISIBLE_DEVICES=all`, and run with `docker run --gpus all` (needs nvidia-container-toolkit).

**Multi-stage build**: install in a builder stage, copy only the result:
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv venv .venv && uv sync --frozen --no-dev

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv
COPY src/ ./src/
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "src/serve.py"]
```
Typical size: ~1.2 GB → ~220 MB, with a smaller attack surface.

**Docker Compose** runs several services together:
```yaml
services:
  train:
    build: .
    volumes: ["./data:/app/data", "./models:/app/models"]
    environment: ["MLFLOW_TRACKING_URI=http://mlflow:5000"]
    depends_on: [mlflow]
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.11.0
    ports: ["5000:5000"]
    volumes: ["mlflow-data:/mlflow"]
    command: mlflow server --host 0.0.0.0 --backend-store-uri /mlflow
volumes:
  mlflow-data:
```
`services`, `volumes` (persist data), `depends_on` (start order), `environment`, `ports` (host:container). A typical stack adds MinIO (S3-compatible artifacts), JupyterLab and Postgres, started with `docker compose up -d`.

| Command | Purpose |
|---|---|
| `docker build -t name:tag .` | build |
| `docker run --rm name:tag` | run, remove on exit |
| `docker run -it --rm name:tag bash` | interactive shell |
| `docker ps` / `docker images` | list |
| `docker logs -f <id>` | stream logs |
| `docker exec -it <id> bash` | shell into a running container |
| `docker compose up -d` / `down -v` | start / stop and remove volumes |
| `docker system prune -af` | clean up |

Do: pin base tags (never `:latest`), multi-stage builds, `.dockerignore`, non-root user in production, config via environment variables. Don't: dev tools or datasets in production images, secrets in images, `docker run` without `--rm`.

Pipeline: develop (VS Code + uv) → build → test (CI) → push → deploy (Kubernetes, [[07 - Kubernetes for ML Deployment]]). Dev Containers let you develop inside the CI image.

### 4. Git and GitHub

Problems: `train_v2_final_FINAL.py`, unreproducible results, overwritten work, no record of why hyperparameters changed, lost work. **Git** is local version control (Linus Torvalds, 2005); **GitHub** hosts repositories and adds pull requests, Actions (CI/CD), issues and `ghcr.io`.

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
ssh-keygen -t ed25519 -C "you@example.com"   # add the .pub key to GitHub

git status && git diff
git add src/train.py                  # git add -p for hunks
git commit -m "feat: add early stopping to trainer"
git pull --rebase origin main
git push origin main

git switch -c exp/transformer-v2      # branch per experiment
git push -u origin exp/transformer-v2
```

Branch names: `main` (deployable), `develop`, `exp/…`, `feat/…`, `fix/…`. Commit messages: a type prefix and summary, then a body explaining what and why, and `Closes #42`.

**Pull requests**: push branch → open PR → CI runs → review → merge. Include what changed and why, metric comparisons, the linked issue. **Never push directly to `main`, even in solo projects.**

**GitHub Actions** (developed in [[09 - CI-CD with GitHub Actions]]): workflow YAML in `.github/workflows/`, triggers (`on:` push, PR, schedule, manual), jobs (fresh VM), steps.
```yaml
name: ML CI
on:
  push: { branches: [main, develop] }
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install uv && uv sync
      - run: uv run ruff check src/
      - run: uv run pytest tests/ -v
      - run: uv run python src/train.py --dry-run
```
A second workflow logs in to GHCR with `docker/login-action@v3` and pushes with `docker/build-push-action@v5`, tagging both `:latest` and `:${{ github.sha }}`. The free tier gives 2,000 minutes/month.

**`.gitignore` for ML** (one pattern per line; comments on their own lines):
```gitignore
.venv/
__pycache__/
*.py[cod]
.ipynb_checkpoints/
# model files: use DVC
*.pt
*.pth
*.pkl
*.onnx
models/
# experiment tracking
mlruns/
wandb/
# data: use DVC or cloud storage
data/raw/
data/processed/
# secrets
.env
*.key
```
Never commit weights, large data, secrets, `.venv/` or notebook outputs (`nbstripout`).

| Command | When |
|---|---|
| `git restore <file>` | discard an edit |
| `git restore --staged <file>` | unstage |
| `git commit --amend` | fix the last local commit |
| `git reset --soft HEAD~1` | undo last commit, keep changes |
| `git revert <sha>` | undo on a shared branch (new commit) |
| `git stash push -m "WIP"` / `git stash pop` | switch context |

**Never rewrite history on a shared branch; use `revert`.**

## ✏️ Exercises

**1.** Why can't a virtual environment fix "works on my machine"? What does each isolation layer cover?

> [!example]- Solution
> | Layer | Isolates | Does not isolate |
> |---|---|---|
> | virtual env | Python packages | system libraries, OS, drivers |
> | container | plus system libraries, filesystem, network, processes | host kernel |
> | VM | plus OS and kernel | hardware |
>
> Failures a venv can't prevent: a PyTorch wheel built for a CUDA version the host driver doesn't support; `libgomp`/`libssl` versions from `apt`; a teammate on a different Python (plain `venv` can't pin it); OS differences between Ubuntu releases. Hence venvs for development, containers for deployment.

**2.** Why copy `pyproject.toml` and `uv.lock` before `src/`? What if the order is reversed?

> [!example]- Solution
> A changed layer invalidates every later layer. With dependencies first, editing `train.py` invalidates only the final `COPY`, and the slow `uv sync` layer is reused. Reversed, every code edit invalidates the `COPY src/` layer and so the dependency install after it: each rebuild reinstalls everything, which also burns CI minutes. Order from least to most frequently changed.

**3.** A colleague commits `.venv/` and a 2 GB `model.pt`, and cloning now takes 20 minutes. What's wrong, and what is the fix?

> [!example]- Solution
> `.venv/` is platform-specific, contains absolute paths, and is fully reproducible from `uv.lock`. Model weights are binary, and Git keeps every committed version forever; deleting the file later doesn't shrink history (that needs `git filter-repo` and a force push, which breaks every clone).
> Fix: a `.gitignore` before the first commit; commit `pyproject.toml` + `uv.lock`; track models and data with DVC (pointer files in Git, bytes in S3/GCS, [[03 - Data in MLOps]]) or MLflow's artifact store. `git rm -r --cached .venv` stops tracking but leaves history as it is.

**4.** How does a multi-stage build shrink an image, and why does that matter beyond disk space?

> [!example]- Solution
> Only files explicitly copied from the builder survive: the final stage starts from a fresh slim image and receives `.venv` and the source, while `uv`, compilers, headers and caches are discarded.
> It matters for security (no compiler or package manager for an attacker to use), for deployment speed (every new node pulls the image when pods scale up or roll back, [[07 - Kubernetes for ML Deployment]]) and for registry cost.
> Pitfall: `.venv` holds Python packages, not system libraries; anything installed with `apt` in the builder must be installed again in the runtime stage.

**5.** (Advanced) A commit on `main` broke production. Why use `git revert` rather than `reset --hard` plus force push? Design a workflow that would have caught it.

> [!example]- Solution
> `git revert <sha>` adds a commit that undoes the change; history stays append-only and teammates just pull. A force push rewrites history: teammates' clones diverge (and a careless push restores the bad commit), work based on it is orphaned, and the audit trail is lost. `reset` is fine for local, unpushed commits.
>
> Workflow:
> 1. Branch protection: PRs, reviews and passing checks required.
> 2. CI on every PR: lint, tests, `train.py --dry-run`.
> 3. ML gates: data schema validation and a test such as `accuracy >= baseline - 0.02`, because code can pass every unit test and still produce a worse model.
> 4. Images tagged by commit SHA, so rollback means redeploying the previous SHA.
> 5. Staging, then a canary release ([[06 - Deployment]]).

## 📝 Summary

- Four layers: venv → editor → container → Git.
- One project, one environment; `uv` with `uv.lock` recommended, `conda` for CUDA.
- Commit `pyproject.toml` and `uv.lock`, never `.venv/`.
- Notebooks for exploration, `src/` for production; restart and run all before committing.
- Containers fix OS-level differences: venvs for development, containers for deployment.
- Order Dockerfile layers from least to most frequently changed; multi-stage builds cut ~1.2 GB to ~220 MB.
- Pin base image tags; run as non-root.
- Everything through pull requests with CI; `git revert` on shared branches.
- Never commit weights, datasets or secrets: DVC and GitHub Secrets.

## ⚠️ Important Notes

1. A venv isolates Python packages only (plain `venv` not even the Python version).
2. `pip freeze` is not a cross-platform lock file.
3. Layer order decides rebuild time.
4. `:latest` is not a version.
5. Committed binaries stay in history; add `.gitignore` before the first commit.
6. `.gitignore` takes one pattern per line and no trailing comments.
7. Multi-stage builds don't carry `apt` libraries in `.venv`.
8. Notebooks run cells in click order; outputs can leak data.
9. Mixing conda and pip carelessly breaks environments.
10. `docker compose down` without `-v` leaves volumes behind.
11. Environment variables are visible with `docker inspect`; secrets baked into a layer stay there even if a later layer deletes them.
12. Force-pushing a shared branch destroys teammates' history and the audit trail.

> [!warning] Gaps in the source slides
> - Slides 2, 19, 30, 44 are section titles; 3, 18, 29 have no text.
> - TikZ diagrams (dependency conflict, slide 4; build/push/pull, 33; Compose stack, 40; pipeline, 42; branch graph, 49) extracted only as labels and are described in prose.
> - Code truncated by the layout on slides 23, 36, 39, 47, 51–54 was completed from context.
> - Slide 24's Jupyter extension figure is an image.
> - Corrected (2026-10-09): the `.gitignore` example previously put several patterns and trailing comments on one line, which Git does not parse.
> - Links in the deck: venv, conda, uv, VS Code, Jupyter, Docker, Podman and Docker Compose documentation.

**Previous:** [[01 - Introduction to MLOps]] · **Next:** [[03 - Data in MLOps]]
