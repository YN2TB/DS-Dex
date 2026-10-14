# DS-Dex — second brain of my uni subjects

Obsidian vault for my Data Science in Economics and Business degree at NEU. One folder per subject. The product is each subject's `contents/`: chapter notes I can pick a subject back up from fast. Not software: no build, lint or tests.

**Writable:** `<Subject>/contents/`, every `CLAUDE.md`, and `METHOD.md`. Write notes directly, no need to ask per file. Everything else stays untouched: `documents/` and `slides/` (sources), `note/` (my own material: read it, e.g. for a syllabus, never edit), `.obsidian/`, `data/` (agentmemory store), `Excalidraw/`, `Claude Code/` (my notes), `README.md`, and `Instruction.md` (an old prompt: don't follow it).

Each subject holds `CLAUDE.md` (sources, extraction quirks, boundaries, open items), `contents/00-Index.md` (scope, chapters with per-chapter status, errata, cross-links) and `contents/NN - <Chapter>.md`. How a note is made: `METHOD.md`.

## Route by task

| Task | Read |
|---|---|
| look something up, revise a subject | `<Subject>/contents/00-Index.md`, then the chapter |
| write or redo chapters | `METHOD.md`, then `<Subject>/CLAUDE.md` |
| new subject, or new sources for a blocked one | `METHOD.md` § New subject |
| new Computer Vision slides | `Computer Vision/CLAUDE.md` |
| concise rewrite (paused) | `METHOD.md` § Concise rewrite; progress in the table below |
| "checkpoint" | `METHOD.md` § Workflow, step 4 |

## Rules

- Write plainly: short sentences, bold only for key terms, no commentary about the vault.
- Verify every number with `sympy`/`numpy`/`fractions` before writing it. Flag gaps, never invent.
- Subject status lives only in the Progress table. Check it against the filesystem.
- To resume: this file + the one subject's `CLAUDE.md`. Don't re-read finished subjects or old transcripts.

## Progress

✅ complete · 🔄 in progress · 🚫 blocked (empty `documents/`) · ✂️ concise rewrite done. Row order is the concise-rewrite queue.

| Subject | Status |
|---|---|
| Data Preparation and Visualization | ✅ 01–11 ✂️ |
| Mathematical Statistics | ✅ 01–09 ✂️ |
| MLOps | ✅ 01–11 ✂️ |
| Machine Learning | ✅ 01–10 (RL only) ✂️ |
| Time-series Analysis | ✅ 01–10 ✂️ |
| Principle of Accounting | ✅ 01–09; concise rewrite at 01–02, next 03 |
| Econometrics | ✅ 01–12 |
| Probability Theory | ✅ 01–10 |
| Linear Algebra | ✅ 01–08 |
| Calculus | ✅ 01–09 |
| Optimization | ✅ 01–12 |
| Discrete Mathematics | ✅ 01–10 |
| Data Structures and Algorithms | ✅ 01–13 |
| Database Management Systems | ✅ 01–11 |
| Basic Programming (C++) | ✅ 01–11 |
| Commercial Banking | ✅ 01–12 (3 errata) |
| Macroeconomics & Microeconomics | ✅ 01–14 |
| Monetary and Financial Theories | ✅ 01–12 (1 erratum) |
| Principles of Marketing | ✅ 01–12 |
| Business Management | ✅ 01–09 |
| Deep Learning | ✅ 01–08 ✂️ |
| Computer Vision | 🔄 01–08 from lectures; 09–14 drafts await slides |
| Big Data Analytics | ✅ 01–12 (6 errata) |
| Natural Language Processing | 🚫 (`note/` empty too) |
| PowerBI | 🚫 |
| Programming for Data Science (Python) | 🚫 |

Open with me: textbook-only scopes are Claude's choices; Optimization has no optimal control (`Léonard & Long` has no text layer).
