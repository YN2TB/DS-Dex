# MLOps — subject context

**Status: ✅ complete** (2026-07-27). `contents/00-Index.md` plus chapters 01–11.

## Sources

**11 lecture decks in `documents/slides/`**, authored in **LaTeX Beamer** — prose and code extracted cleanly, much better than the PowerPoint-based subjects. Every figure and TikZ diagram is still an image. Lecturer: **Dr. Nguyen Manh Toan**, Swinburne Vietnam, delivered at NEU.

## Chapters

01 Introduction to MLOps · 02 Environment Setup · 03 Data in MLOps · 04 Model Development · 05 Packaging Models with FastAPI and Docker · 06 Deployment · 07 Kubernetes for ML Deployment · 08 Monitoring with Prometheus and Grafana · 09 CI-CD with GitHub Actions · 10 Monitoring and Drift · 11 Robust AI

## Two structural findings

- **`MLOps_DeployingML_on_K8s.pdf` (23pp) is a strict subset of `MLOps_K8s.pdf` (39pp)** — slides 1–23 are identical apart from one image reference. **They are one lecture, not two.** The larger deck was split by topic into ch. 07 (Kubernetes) and ch. 08 (Prometheus/Grafana). *Without this, a future session would write the same chapter twice.*
- **The K8s architecture slide is entirely an image** (control plane, API server, scheduler, etcd, kubelet), as are the three "Why Kubernetes" slides. That is the most examinable content in the lecture and it is **unrecoverable** — if the user asks about Kubernetes internals, say the slide is lost rather than guessing what the lecturer showed.

## Other gaps to raise with the lecturer

Image-only: the **concept-drift taxonomy** (sudden / gradual / incremental / recurring), "Retraining vs Updating Model", the three-types-of-ML figure, the MLOps tool landscape. **PGD is named as an attack but never defined.**

**No application code, workflow YAML, or Kubernetes manifests appear in any deck** — they live at `github.com/NguyenMToan/house-price-predictor`. All code in ch. 05–09 is therefore written from the deck's fragments plus standard practice, and is labelled as such.

Cross-subject: ch. 04 and ch. 10 lean on `Machine Learning/contents/` and `Data Preparation and Visualization/contents/09 - Building Pipelines.md`.
