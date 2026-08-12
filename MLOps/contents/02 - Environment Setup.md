---
subject: MLOps
chapter: 02
tags: [ds, mlops, docker, git, uv, reproducibility, tooling]
source: "MLOps_Environment_Setup.pdf — Dr. Nguyen Manh Toan, Swinburne Vietnam"
---

# Environment Setup

> [!note] Where this sits in the course
> [[01 - Introduction to MLOps]] argued that **reproducibility is often missing**. This chapter is the practical answer, in four escalating layers of isolation: **virtual environments** (Python packages) → **editors** (the workbench) → **containers** (the whole OS) → **Git** (history and collaboration).
>
> The layering is the point. Each tool solves a problem the previous one cannot.

## 📘 Main Knowledge

---

## Part 1 — Virtual environments

### The problem: dependency hell

> Project A needs `numpy==1.21`. Project B needs `numpy==1.26`. **Only one version can be globally installed.** Upgrading one project breaks the other.

Further risks: system Python gets polluted over time; the setup becomes impossible to reproduce on another machine; and `pip install` in dev ends up ≠ production.

### What a virtual environment is

> An **isolated, self-contained Python installation** with its own interpreter, packages, and scripts — completely separate from the system Python and other environments.

| Contains | Does **not** do |
|---|---|
| A Python interpreter (copy or symlink) | Duplicate the stdlib (shared via symlinks) |
| Its own `site-packages/` | Replace Docker or OS-level isolation |
| Isolated pip and scripts | Manage Python versions (use `pyenv`/`uv`) |
| An `activate` shell script | Sandbox network or filesystem access |

That right-hand column matters: **a virtual environment isolates Python packages and nothing else.** It is why Part 3 exists.

**Why it matters for ML:** reproducibility (pin exact PyTorch, scikit-learn, CUDA versions) · isolation (experiment without breaking production) · collaboration (share `requirements.txt`/`pyproject.toml`) · CI/CD (maps cleanly onto Docker `RUN pip install` layers).

> **Rule of thumb: one project ⇒ one virtual environment.**

**A typical ML dependency stack**, all inside one environment: Python 3.10/3.11 → `numpy`, `pandas`, `scipy` → `scikit-learn`, `xgboost`, `lightgbm` → `torch`/`tensorflow` + CUDA → `mlflow`, `wandb`, `dvc` → `jupyter`, `black`, `pytest`, `ruff`.

### Three tools

| Feature | `venv` | `conda` | **`uv`** |
|---|---|---|---|
| Speed | Medium | Slow | **Very fast** |
| Python version mgmt | No | Yes | Yes |
| Non-Python libs (CUDA) | No | **Yes** | No |
| Lock file | No | `env.yml` | **`uv.lock`** |
| Requires install | No (stdlib) | Yes | Yes (tiny) |
| Docker-friendly | Yes | Partial | Yes |

- **`venv`** — stdlib, zero dependencies, pure-Python packages only. *Best for scripts and teaching.*
- **`conda`** — manages Python versions and **non-Python libraries (CUDA, MKL)**, via conda-forge. Heavier and slower. *Best for GPU/CUDA work.*
- **`uv`** — written in Rust, **10–100× faster than pip**, replaces pip + venv, lock files built in. **The course recommendation.**

**`venv`:**
```bash
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
.venv\Scripts\Activate.ps1         # Windows PowerShell
pip install numpy pandas scikit-learn
pip freeze > requirements.txt
deactivate
```
**Always add `.venv/` to `.gitignore`.**

**`conda`:**
```bash
conda create -n ml-project python=3.11
conda activate ml-project
conda install numpy pandas
pip install scikit-learn mlflow
conda env export > environment.yml
conda env create -f environment.yml     # reproduce elsewhere
```
*Tip: conda for CUDA/GPU packages, pip for pure Python ML libraries.*

**`uv`** — install once:
```bash
curl -Ls https://astral.sh/uv/install.sh | sh                    # macOS/Linux
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"   # Windows
```
Daily workflow:
```bash
uv init my-ml-project && cd my-ml-project
uv venv .venv --python 3.11
uv add numpy pandas scikit-learn torch    # auto-updates the lock file
uv sync                                   # reproduce env from lock file
uv run python train.py                    # run inside the venv
```

Key files: `pyproject.toml` (metadata + deps) · `uv.lock` (exact pinned versions) · `.venv/` (never commit).

> **The key advantage is `uv.lock`.** Unlike `pip freeze`, it is **cross-platform and automatically maintained** — no manual freeze after every install.

**Translation table:**

| Task | `uv` | `pip` + `venv` |
|---|---|---|
| Create environment | `uv venv .venv` | `python -m venv .venv` |
| Install a package | `uv add numpy` | `pip install numpy` |
| Install from file | `uv sync` | `pip install -r requirements.txt` |
| Lock / freeze | `uv lock` → `uv.lock` | `pip freeze > requirements.txt` |
| Run a script | `uv run train.py` | `python train.py` |
| Choose Python version | `uv venv --python 3.11` | `python3.11 -m venv .venv` |

**Best practices — DO:** one environment per project · pin exact versions · commit `pyproject.toml`/`requirements.txt` · separate dev and production deps · document the Python version.
**AVOID:** installing into system Python · committing `.venv/` · `pip install` without pinning · sharing environments by copying folders · mixing conda and pip carelessly · forgetting to activate.

---

## Part 2 — Editors

**Core requirements:** syntax highlighting and autocomplete · virtual environment integration · debugger with variable inspection · Git support · terminal access.
**ML-specific:** Jupyter notebooks · inline plot rendering · remote/SSH editing · Docker container development.

| Editor | Character |
|---|---|
| **VS Code** *(course tool)* | Free, huge extension library, Python + Jupyter built in, Remote SSH / Docker dev |
| **JupyterLab** | Browser-based, notebook-first, rich interactive output |
| **PyCharm** | Full IDE, best-in-class debugger, professional edition paid, heavy |

**VS Code strengths:** free and cross-platform · IntelliSense · integrated terminal · **Remote Development** (edit on a GPU server over SSH as if local) · **Dev Containers** (develop inside Docker) · GitLens.

**Configuring for a Python/ML project** — select the interpreter with `Ctrl+Shift+P` → `Python: Select Interpreter` → `.venv/bin/python`, then:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "editor.formatOnSave": true,
  "[python]": { "editor.defaultFormatter": "ms-python.black-formatter" },
  "jupyter.notebookFileRoot": "${workspaceFolder}"
}
```

> Use VS Code for everything; switch to JupyterLab only when you need its classic multi-panel layout.

**Notebook best practices — DO:** keep notebooks **linear** (top to bottom) · use Markdown to explain **why** · **restart kernel & run all before committing** · one notebook per experiment · **export final logic to `.py` modules** · `nbconvert` for HTML reports.
**AVOID:** running cells out of order · storing large datasets in `.ipynb` · committing huge outputs · putting all project logic in notebooks · global variables across notebooks.

> **Rule: notebooks are for exploration. Production code lives in `src/`.**

---

## Part 3 — Containers

### The problem containers solve

> **"It works on my machine."** Different OS versions between dev and prod · CUDA/cuDNN mismatches · system library conflicts (`libgomp`, `libssl`) · Python version drift. **Virtual envs alone cannot fix OS-level differences.**

The answer: package **everything** — OS, system libs, Python, packages, and code — into one portable unit.

| Property | Virtual Env | **Container** | Virtual Machine |
|---|---|---|---|
| Isolates Python packages | Yes | Yes | Yes |
| **Isolates system libraries** | **No** | **Yes** | Yes |
| Isolates OS | No | Shares host kernel | Full OS |
| Startup time | Instant | Seconds | Minutes |
| Disk footprint | MB | MB–GB | GB |
| Portability | Low | **Very high** | Medium |
| GPU passthrough | Native | Yes (NVIDIA runtime) | Limited |

> **In MLOps: virtual envs during development, containers for deployment and CI/CD.**

### Core concepts

- **Image** — a read-only blueprint (OS + dependencies + code), built from a **Dockerfile**, stored in a registry.
- **Container** — a running instance of an image; isolated process with its own filesystem, network, PID space. **Ephemeral by default.**
- **Registry** — a repository of images: Docker Hub, GitHub Container Registry (`ghcr.io`), AWS ECR, Google Artifact Registry.

Flow: `Dockerfile` --build--> `Image` --push--> `Registry` --pull--> `Container`.

**Docker vs Podman:** Docker is the industry standard since 2013 but requires a **daemon running as root**; Podman is a **daemonless, rootless** drop-in replacement with better security on shared Linux servers. *Docker is the course recommendation.*

### Anatomy of an ML Dockerfile

```dockerfile
FROM python:3.11-slim                    # 1. Base image
WORKDIR /app                             # 2. Working directory

RUN apt-get update && apt-get install -y \
    libgomp1 curl && \
    rm -rf /var/lib/apt/lists/*          # 3. System deps

RUN pip install uv                       # 4. Fast package manager

COPY pyproject.toml uv.lock ./           # 5. Dependency files FIRST
RUN uv sync --frozen                     # 6. Cached layer

COPY src/ ./src/                         # 7. Source code
CMD ["uv", "run", "python", "src/train.py"]
```

> **Layer caching strategy — the single most important idea here.** Copy `pyproject.toml` and `uv.lock` **before** the source code. Docker caches each layer, so dependencies reinstall only when the lock file changes; editing `train.py` (step 7) does not invalidate the slow dependency layer.

**GPU-enabled:**
```dockerfile
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y python3.11 python3-pip curl && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY src/ ./src/
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
CMD ["uv", "run", "python", "src/train_gpu.py"]
```
```bash
docker run --rm --gpus all ml-train-gpu:latest    # requires nvidia-container-toolkit
```

**Multi-stage build** — build tools in one stage, only the runtime in the next:
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv venv .venv && uv sync --frozen --no-dev

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv      # copy ONLY the installed venv
COPY src/ ./src/
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "src/serve.py"]
```
**Typical size reduction: ~1.2 GB → ~220 MB**, with a smaller attack surface.

### Docker Compose

```yaml
services:
  train:
    build: .
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000
    depends_on:
      - mlflow
  mlflow:
    image: ghcr.io/mlflow/mlflow:v2.11.0
    ports:
      - "5000:5000"
    volumes:
      - mlflow-data:/mlflow
    command: >
      mlflow server --host 0.0.0.0 --backend-store-uri /mlflow
volumes:
  mlflow-data:
```

**Concepts:** `services` (container definitions) · `volumes` (persist data across restarts) · `depends_on` (startup ordering) · `environment` (config as env vars) · `ports` (host:container).

A **typical MLOps stack** — `train` (Python + uv), `mlflow` (experiment tracker), `minio` (S3-compatible artefact store), `notebook` (JupyterLab), `postgres` (metadata DB) — all started with a single `docker compose up -d`.

**Essential commands:**

| Command | Description |
|---|---|
| `docker build -t name:tag .` | Build image from Dockerfile |
| `docker run --rm name:tag` | Run container, remove on exit |
| `docker run -it --rm name:tag bash` | Interactive shell |
| `docker run --gpus all name:tag` | Run with GPU access |
| `docker ps` / `docker images` | List containers / images |
| `docker logs -f <id>` | Stream logs |
| `docker exec -it <id> bash` | Shell into a running container |
| `docker compose up -d` | Start all services (detached) |
| `docker compose down -v` | Stop and remove volumes |
| `docker system prune -af` | Clean up unused images and containers |

**Best practices — DO:** specific base image tags, **never `:latest`** · multi-stage builds · dependency files before source · include a `.dockerignore` · **run as non-root in production** · environment variables for config, never hardcoded secrets · `uv sync --frozen`.
**AVOID:** `FROM python:latest` · dev tools in production images · baking large datasets into the image · running training as root · committing `.env` files · `docker run` without `--rm`.

**Docker across the pipeline:** Develop (VS Code + uv) → Build (Dockerfile) → Test (CI/CD) → Push (Registry) → Deploy (Kubernetes). The **Dev Containers** extension lets you develop inside the same image CI/CD uses — zero "works on my machine". Later in the course: **Kind** (Kubernetes in Docker), `kubectl`, and image scanning with Docker Scout. → [[07 - Kubernetes for ML Deployment]]

---

## Part 4 — Git and GitHub

### The problem

> `train_v2_final_FINAL.py` · cannot reproduce last week's best model · a teammate overwrites your changes · no record of **why** hyperparameters changed · deploying the wrong script version · losing work after a disk failure.

**Git** is the local version control system — offline, tracks commits, manages branches, created by Linus Torvalds (2005). **GitHub** hosts remote repositories and adds Pull Requests, **GitHub Actions** (free CI/CD), issues, and a container registry (`ghcr.io`).

> **Git is the tool. GitHub is where your team meets.**

### Setup and daily workflow

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"

ssh-keygen -t ed25519 -C "you@example.com"    # then add the .pub to GitHub
```

```bash
git status && git diff              # 1. what changed
git add src/train.py                # 2. stage (git add -p for hunk-by-hunk)
git commit -m "feat: add early stopping to trainer"
git pull --rebase origin main       # 4. pull before push
git push origin main
git log --oneline --graph
```

**A good commit message:**
```
feat: add dropout regularisation

- Add configurable dropout rate to TransformerBlock
- Default rate 0.1 matches paper
- Update tests in test_model.py

Closes #42
```

### Branches

```bash
git switch -c experiment/transformer-v2
git commit -m "exp: try transformer arch"
git push -u origin experiment/transformer-v2
git switch main
git merge experiment/transformer-v2
git branch -d experiment/transformer-v2
```

**ML branch naming:** `main` (stable, deployable) · `develop` (integration) · `exp/...` (experiments) · `fix/...` · `feat/...`

### Pull requests

Push branch → open PR against `main` → automated checks run (CI/CD, tests, linting) → review → address feedback → approve → merge → branch deleted.

**Include in a PR:** what changed and **why** · experiment results or metric comparisons · link to the Issue · plots if relevant · testing steps.

> **MLOps rule: never push directly to `main`. All changes go through a Pull Request, even in solo projects.**

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: ML CI
on:
  push:
    branches: [main, develop]
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        run: pip install uv
      - name: Install dependencies
        run: uv sync
      - name: Run linter
        run: uv run ruff check src/
      - name: Run tests
        run: uv run pytest tests/ -v
      - name: Check model training
        run: uv run python src/train.py --dry-run
```

**Concepts:** *Workflow* (YAML in `.github/workflows/`) · *Trigger* (`on:` — push, PR, schedule, manual) · *Job* (fresh VM) · *Step* (a command or reusable Action). Free tier: 2,000 minutes/month. Developed fully in [[09 - CI-CD with GitHub Actions]].

**Building and pushing an image:**
```yaml
# .github/workflows/docker.yml
name: Build and Push Image
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}
```

### `.gitignore` for ML

```gitignore
.venv/ venv/ env/
__pycache__/ *.py[cod] *.egg-info/
.ipynb_checkpoints/
*.pt *.pth *.pkl *.h5 *.onnx      # model files — use DVC instead
models/
mlruns/ wandb/                     # experiment tracking
data/raw/ data/processed/          # data — use DVC or cloud storage
.env *.key                         # secrets
```

**Never commit:** model weights (use DVC or S3/GCS) · large datasets · secrets/API keys (use `.env` + GitHub Secrets) · `.venv/` (reproducible from `uv.lock`) · notebook outputs (clear first, or use `nbstripout`).

### Undoing mistakes

| Command | When |
|---|---|
| `git restore <file>` | Small accidental edit |
| `git restore --staged <file>` | Unstage, keep changes |
| `git commit --amend` | Fix the last commit message locally |
| `git reset --soft HEAD~1` | Undo last commit, keep changes staged |
| `git revert <sha>` | **Undo on a shared branch** — adds a new commit |
| `git stash push -m "WIP"` / `git stash pop` | Context switch mid-work |

> **Golden rule: never rewrite history (`reset --hard`, force push) on a shared branch. Use `revert` instead.**

## ✏️ Exercises

**1.** Explain why a virtual environment cannot solve the "works on my machine" problem, and what each layer of isolation actually covers.

> [!example]- Solution
> A virtual environment isolates **Python packages only**. The slides are explicit that it does *not* replace Docker or OS-level isolation.
>
> | Layer | Isolates | Does not isolate |
> |---|---|---|
> | **Virtual env** | Python packages, pip, scripts | System libraries, OS, kernel, CUDA drivers |
> | **Container** | + system libs, filesystem, network, processes | The **host kernel** (shared) |
> | **VM** | + the entire OS and kernel | Hardware |
>
> **Concrete failures a venv cannot prevent:**
> - **CUDA/cuDNN mismatch.** `pip install torch` pulls a wheel compiled against a particular CUDA version. If the host driver is older, it fails at import — no Python package can fix a driver.
> - **System library conflicts.** `libgomp` (OpenMP) and `libssl` are installed by `apt`, outside the venv entirely. scikit-learn links against the system `libgomp`; a different Ubuntu version ships a different one.
> - **Python version drift.** `venv` **cannot manage Python versions** — it uses whatever interpreter created it. A teammate on Python 3.9 gets different behaviour from your 3.11, and `requirements.txt` says nothing about it. (`conda` and `uv` *can* manage versions, which is one reason `uv` is recommended.)
> - **OS-level differences.** Path separators, default encodings, and available system binaries all differ between Ubuntu 20.04 and 22.04 — the slide's exact example.
>
> **The practical rule the lecture gives:** *virtual envs during development, containers for deployment and CI/CD.* The venv is fast and lightweight for the edit-run loop; the container is what you ship. And **Dev Containers** collapse the distinction by letting you develop *inside* the deployment image.

**2.** In the ML Dockerfile, why are `pyproject.toml` and `uv.lock` copied **before** `src/`? What happens if you reverse the order?

> [!example]- Solution
> **Docker builds images as a stack of cached layers.** Each instruction creates a layer, and Docker reuses a cached layer only if that instruction *and every instruction before it* are unchanged. One invalidated layer invalidates everything after it.
>
> **Correct order:**
> ```dockerfile
> COPY pyproject.toml uv.lock ./     # changes rarely
> RUN uv sync --frozen               # SLOW (~2 min) — cached
> COPY src/ ./src/                   # changes constantly
> ```
> Editing `train.py` invalidates only the final `COPY`. The expensive dependency install is reused. **Rebuild: ~2 seconds.**
>
> **Reversed:**
> ```dockerfile
> COPY src/ ./src/                   # changes constantly
> COPY pyproject.toml uv.lock ./
> RUN uv sync --frozen               # now invalidated on EVERY code change
> ```
> Any edit to any source file invalidates the `COPY src/` layer, and therefore everything after it — including the dependency install. **Rebuild: ~2 minutes, every time.**
>
> The general principle: **order Dockerfile instructions from least- to most-frequently-changing.** System packages first, then Python dependencies, then application code last.
>
> The cost compounds in CI. A workflow triggered on every push and PR that rebuilds dependencies each time burns the 2,000 free minutes/month quickly, and slows the feedback loop that CI exists to shorten.
>
> `--frozen` matters too: it makes `uv sync` fail rather than silently update the lock file, guaranteeing the image matches exactly what was committed.

**3.** A colleague commits their `.venv/` folder and a 2 GB `model.pt` to Git, then asks why cloning takes 20 minutes. Explain the problems and give the correct approach for each.

> [!example]- Solution
> **`.venv/` should never be committed** for four reasons:
> 1. **It is platform-specific.** It contains compiled binaries and absolute paths for one OS and architecture. A macOS `.venv` is unusable on Linux.
> 2. **It is fully reproducible** from `uv.lock`/`requirements.txt` — the lock file is a few KB against hundreds of MB.
> 3. **It contains absolute paths.** `pyvenv.cfg` and the activate scripts hardcode the creator's home directory.
> 4. **It bloats history permanently.** Which leads to the second problem.
>
> **Model weights should never be committed** because **Git stores every version forever**. Git is designed for text — it stores diffs efficiently for source but must keep a full copy of each version of a binary. Train the model ten times, commit each result, and the repository holds 20 GB permanently. **Deleting the file later does not shrink the repo**; the blobs remain in history, and removing them requires rewriting history (`git filter-repo`) and force-pushing — which breaks every existing clone.
>
> **The correct approach:**
> ```gitignore
> .venv/
> *.pt *.pth *.pkl *.h5 *.onnx
> models/
> data/raw/ data/processed/
> mlruns/
> ```
> - **Environments** → commit `pyproject.toml` + `uv.lock`; teammates run `uv sync`.
> - **Models and data** → **DVC**, which commits a small pointer file to Git while the actual bytes live in S3/GCS. Git tracks *which version* is current; object storage holds the bytes. → [[03 - Data in MLOps]]
> - **Model artifacts from experiments** → MLflow's artifact store, per [[01 - Introduction to MLOps]].
>
> The slide states this directly: "*ML model files (use DVC instead)*" and "*Data (use DVC or cloud storage)*".
>
> To fix an already-polluted repo, `git rm -r --cached .venv` removes it going forward, but the history still carries the weight — hence "**always include a `.gitignore` before the first commit**."

**4.** Explain the multi-stage Docker build. Why does it reduce a 1.2 GB image to 220 MB, and why does that matter beyond disk space?

> [!example]- Solution
> **The mechanism:** the build runs in two `FROM` stages, and **only explicitly copied files survive from stage 1 to stage 2.**
>
> Stage 1 (`builder`) installs `uv`, compilers, headers, and dev dependencies to produce `.venv`. Stage 2 starts from a *fresh* `python:3.11-slim` and copies **only** `/app/.venv` plus the source. Everything else in the builder — `uv` itself, `gcc`, header files, the pip cache, `--no-dev` test dependencies — is discarded.
>
> **Why it matters beyond disk:**
>
> **Security — the smaller attack surface** the slides mention. A production container that contains `gcc`, `curl`, and a package manager gives an attacker who achieves code execution the tools to compile exploits and pull down payloads. A runtime-only image gives them a Python interpreter and little else. This is the same reasoning behind "run as a non-root user in production."
>
> **Deployment speed.** Every Kubernetes pod start pulls the image. At 1.2 GB, autoscaling from 3 to 30 pods transfers 36 GB; at 220 MB it is 6.6 GB. This directly determines how fast you can scale under load, and how long a rollback takes. → [[07 - Kubernetes for ML Deployment]]
>
> **CI/CD cost.** Images are pushed and pulled on every merge; registry storage and egress are billed.
>
> **A common failure to know:** copying only `.venv` breaks if the application needs a **system** library that the builder installed via `apt`. `.venv` contains Python packages, not `libgomp1`. If stage 1 installed system deps, stage 2 must install them too — they do not travel with the venv. This is exactly the venv-vs-container isolation boundary from Exercise 1, appearing inside a single Dockerfile.

**5.** (Advanced) Your team's `main` branch has a commit that broke production. Explain why `git revert` is correct and `git reset --hard` + force push is dangerous. Then design a workflow that would have caught the problem.

> [!example]- Solution
> **`git revert <sha>` creates a *new* commit that undoes the changes.** History is append-only: the bad commit remains, followed by its reversal. Everyone's clone stays consistent — a `git pull` simply brings the new commit.
>
> **`git reset --hard` + force push *rewrites* history**, deleting the commit from the branch. The damage:
> - **Every teammate's local clone diverges.** Their `main` still has the deleted commit; their next `pull` produces confusing conflicts, and a careless `push` **restores the bad commit**.
> - **Work built on top is destroyed.** Anyone who branched from the deleted commit is orphaned.
> - **The audit trail is gone.** In a regulated context this is a compliance failure — [[01 - Introduction to MLOps]] lists auditability as a core MLOps benefit, and rewriting history destroys it.
> - **It is silent.** Nothing records that a force push happened.
>
> Hence the slides' golden rule: *never rewrite history on a shared branch.* `reset --soft`/`--hard` are fine for **local, unpushed** commits.
>
> ```bash
> git revert a3f8b12
> git push origin main        # no force needed
> ```
>
> **A workflow that catches it — the layers, in order of cost:**
>
> **1. Branch protection on `main`** — no direct pushes, PR required, approving review required, status checks must pass. This is the slides' "never push directly to `main`, even in solo projects."
>
> **2. CI on every PR** — the `ci.yml` workflow: `ruff check` for lint, `pytest` for tests, and `train.py --dry-run` to verify the pipeline executes. That `--dry-run` step is the ML-specific one: it catches a broken training pipeline before merge, which no unit test would.
>
> **3. ML-specific gates that generic CI misses:**
> ```yaml
>       - name: Validate data schema
>         run: uv run python src/validate_data.py
>       - name: Check model metrics against baseline
>         run: uv run pytest tests/test_model_quality.py
> ```
> Because ML systems are **probabilistic** ([[01 - Introduction to MLOps]]), code can be syntactically perfect and behaviourally broken. A test asserting `accuracy >= baseline - 0.02` catches a regression that every lint and unit test passes.
>
> **4. Build the image in CI and tag it with the commit SHA** — `ghcr.io/repo:${{ github.sha }}`. This makes rollback trivial: redeploy the previous SHA's image, which is guaranteed to be exactly what was running before. Tagging only `:latest` makes rollback impossible, which is why the slides tag both.
>
> **5. Staged rollout** — deploy to staging first, then canary a small traffic percentage. → [[05 - Packaging Models with FastAPI and Docker]]
>
> The general principle: **every MLOps safeguard exists because ML systems fail silently.** A crashed server pages you; a model quietly predicting the majority class does not.

## 📝 Summary

- **Four layers of isolation:** virtual env (Python packages) → editor (workbench) → container (OS + system libs) → Git (history). Each solves what the previous cannot.
- **One project ⇒ one virtual environment.** Never install into system Python.
- **`uv` is the course recommendation** — 10–100× faster than pip, with a cross-platform `uv.lock` that `pip freeze` cannot match. Use `conda` when you need CUDA/non-Python libraries.
- **Commit `pyproject.toml` and `uv.lock`; never commit `.venv/`.**
- **Notebooks are for exploration; production code lives in `src/`.** Restart-and-run-all before committing.
- **A virtual env cannot fix OS-level differences** — that is what containers are for. Dev with venvs, deploy with containers.
- **Order Dockerfile layers least- to most-frequently-changing**; copy dependency files before source code.
- **Multi-stage builds** cut ~1.2 GB to ~220 MB and shrink the attack surface.
- **Pin base image tags; never `:latest`.** Run as non-root in production.
- **Never push directly to `main`** — everything goes through a Pull Request with CI.
- **Never commit model weights, datasets, or secrets** — use DVC and GitHub Secrets.
- **`git revert` on shared branches; never `reset --hard` + force push.**

## ⚠️ Important Notes

**A virtual environment isolates Python packages and nothing else** — not system libraries, not CUDA drivers, not the OS, and (for `venv`) not even the Python version.

**`pip freeze` is not a lock file.** It records what happens to be installed on *your* platform, including transitive dependencies with no distinction from direct ones. `uv.lock` is cross-platform and maintained automatically.

**Docker layer order determines build time.** Copying source before dependencies turns a 2-second rebuild into a 2-minute one, on every commit.

**`:latest` is not a version.** `FROM python:latest` means your build silently changes when Python releases. Always pin.

**Committing binaries to Git is permanent.** History retains every version even after deletion; removing them requires rewriting history and breaking every clone.

**`.gitignore` must exist before the first commit.** Adding it later does not remove already-tracked files from history.

**Copying only `.venv` in a multi-stage build misses system libraries.** Anything installed via `apt` in the builder must be reinstalled in the runtime stage.

**Notebooks run cells in whatever order you click.** A notebook that "works" may be unreproducible top-to-bottom. Restart kernel and run all before trusting or committing it.

**Committed notebook outputs bloat diffs and can leak data.** Cell outputs may embed sample rows containing personal information. Clear them, or use `nbstripout`.

**Mixing conda and pip carelessly breaks environments.** Conda does not track pip-installed packages, so a later `conda install` can silently overwrite them. Install conda packages first, pip packages last, and never alternate.

**`docker compose down` without `-v` leaves volumes behind**, which accumulate silently until the disk fills.

**Secrets in environment variables are visible via `docker inspect`.** Env vars are fine for config; use Docker secrets or a secrets manager for credentials, and never bake them into an image layer — layers are permanent even if a later layer deletes the file.

**`git reset --hard` on a shared branch is unrecoverable for teammates** and destroys the audit trail that MLOps governance depends on.

> [!warning] Gaps in the source slides
> LaTeX Beamer, so extraction was near-complete. Missing:
> - **Slides 2, 19, 30, 44** are section-title slides with no content.
> - **Slides 3, 18, 29** produced no text — likely section dividers or full-page figures.
> - The architecture and flow **diagrams** (dependency-conflict figure on slide 4, the Docker build/push/pull figure on slide 33, the Compose stack on slide 40, the pipeline on slide 42, the branch graph on slide 49) are drawn with TikZ and extracted only as scattered labels; I have reconstructed them in prose.
> - **Several code blocks are truncated mid-listing** by the PDF layout — slide 23 (`.vscode/settings.json`, cut at "T"), slide 36 (layer caching note, cut at "(st"), slide 39 (Compose commands, cut after "#"), slide 47 (the `git clone` line), slide 51 (free tier note), slide 52 (resulting image tags), slide 53 ("What to always..."), slide 54 (golden rule, cut at "new c"). I have completed these from context; verify against the original.
> - **Slide 24** references a "Jupyter Extension" figure that is an image.
>
> **Links given in the deck:** [venv docs](https://docs.python.org/3/library/venv.html) · [conda env management](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments) · [uv installation](https://docs.astral.sh/uv/getting-started/installation/) · [uv pip interface](https://docs.astral.sh/uv/pip/) · [VS Code](https://code.visualstudio.com/) · [Jupyter](https://jupyter.org/) · [Docker](https://www.docker.com/) · [Podman](https://podman.io/) · [Docker Compose](https://docs.docker.com/compose/)

---
**Previous:** [[01 - Introduction to MLOps]] · **Next:** [[03 - Data in MLOps]]
