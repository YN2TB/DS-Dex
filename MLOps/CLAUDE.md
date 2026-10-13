# MLOps: subject context

**Status: ✅ complete** (2026-07-27), rewritten concisely 2026-10-09. `contents/00-Index.md` plus chapters 01–11.

## Sources

11 LaTeX Beamer decks in `documents/slides/` by Dr. Nguyen Manh Toan (Swinburne Vietnam). Prose and code extract cleanly; figures and TikZ diagrams don't (icon-font glyphs appear as junk characters).

## Chapters

01 Introduction to MLOps · 02 Environment Setup · 03 Data in MLOps · 04 Model Development · 05 Packaging Models with FastAPI and Docker · 06 Deployment · 07 Kubernetes for ML Deployment · 08 Monitoring with Prometheus and Grafana · 09 CI-CD with GitHub Actions · 10 Monitoring and Drift · 11 Robust AI

## Things to know

- `MLOps_DeployingML_on_K8s.pdf` is a subset of `MLOps_K8s.pdf`: one lecture, split into ch. 07 (Kubernetes) and 08 (Prometheus/Grafana). Don't write it twice.
- The K8s architecture slide and "Why Kubernetes" slides are images. If asked about Kubernetes internals, say the slide is lost rather than guessing what the lecturer showed.
- Also image-only: concept-drift taxonomy, "Retraining vs Updating Model", three types of ML, the tool landscape.
- No application code, workflow YAML or manifests appear in the decks; they are in `github.com/NguyenMToan/house-price-predictor`. Code in ch. 05–09 is reconstructed and labelled.

## Errata and corrections (2026-10-09)

- `MLOPs_RobustAI.pdf` slide 9: the C&W loss printed is the targeted form, inconsistent with the untargeted constraint. Correct untargeted loss: $\max(Z_y-\max_{i\ne y}Z_i,-\kappa)$.
- ch. 02 `.gitignore` example fixed (one pattern per line); ch. 05 health check no longer uses `curl` on a slim image; ch. 11 EAD formula restored from the slide; PGD definition added.

Cross-subject: ch. 04 and 10 lean on `Machine Learning/contents/` and `Data Preparation and Visualization/contents/09 - Building Pipelines.md`.
