# CLAUDE.md

Guidance for Claude Code in this repository.

## What this is

An Obsidian vault used as a "second brain" by a Data Science student at NEU (National Economics University, Vietnam). Not a software project: no build, lint or tests. Claude's job is to turn course material (slides, textbooks, papers) into well-structured Obsidian notes.

- `data/` is the agentmemory plugin's folder and `Excalidraw/` holds drawings; neither is a subject.
- Each subject's `note/` folder belongs to the user (their own notes, code, venvs). Don't edit it, but check it: Deep Learning's syllabus came from `note/Index.md`.

## Current state (2026-10-09)

- **22 subjects complete, 237 chapter notes** (counted from `contents/[0-9][0-9] - *.md`, including Computer Vision's 14).
- **Computer Vision is in progress.** The course is running and slides arrive weekly. Notes 01–08 were rewritten from lectures 1–8; notes 09–14 are drafts to redo when their slides appear. `Computer Vision/CLAUDE.md` is the source of truth.
- **Big Data Analytics now has sources** (added 2026-10-09): *Learning Spark* and *Spark: The Definitive Guide* in `documents/`. Not started; it has no `CLAUDE.md` yet. Check `note/` for a user syllabus before choosing a scope.
- **Blocked** (empty `documents/`): Natural Language Processing, PowerBI, Programming for Data Science (Python).
- **Deep Learning was rewritten 2026-10-09** in a shorter style at the user's request.
- Open question for the user (not blocking): textbook-only scopes are my choices, and optimal control is missing because `Optimization/documents/Léonard & Long` has no text layer.

**To resume:** read this file and the one subject's `CLAUDE.md`, then start. Don't re-read finished subjects or old transcripts.

**Keeping this current:** after each chapter (and when the user says "checkpoint"), update this section in one edit: what finished, what is next, anything mid-flight. Keep it short. Claude cannot see the session limit, so update at natural boundaries.

## Vault structure

```
[Subject Name]/
  CLAUDE.md               ← subject context: sources, scope, extraction quirks, errata, chapter list
  contents/
    00-Index.md           ← map of content, scope decision, errata table, cross-subject links
    01 - [Chapter Topic].md
  documents/              ← source PDFs (documents/slides/ if the course has slides)
  note/                   ← the user's own material
```

One subject per folder, one chapter per file, numbered in learning order.

## Chapter note template

```markdown
---
subject:
chapter:
tags: [ds]
source:
---

# Chapter Title

## 📘 Main Knowledge
Concepts, definitions and formulas in plain language. $$LaTeX$$ for maths, [[wikilinks]] for related notes.

## ✏️ Exercises
5 problems, easy → hard, solutions in collapsed callouts:
> [!example]- Solution

## 📝 Summary
5–8 bullets for quick exam review.

## ⚠️ Important Notes
Common mistakes and exam traps (8–15 items).

> [!warning] Gaps in the source material
> What was lost, reconstructed, or added beyond the source.

**Previous:** … · **Next:** …
```

## Conventions

- **Write plainly and concisely.** The user found the long, emphatic style of earlier notes hard to read (2026-10-09). Short sentences, bold only for key terms, callouts only where they help, no "⚠️" on every line, no commentary about the vault itself or about what the source "never says". Depth comes from content (derivations, tables, worked examples), not from length.
- Write `00-Index.md` first so the scope decision survives an early stop.
- Flag gaps, never invent. Label additions beyond the source in the gaps callout.
- **Verify every number** with `sympy`/`numpy`/`fractions` before writing it, including every exercise answer.
- Wikilinks (including cross-subject and forward links), tags, callouts, LaTeX.
- Standing authorisation: write notes directly without asking per file.

## Workflow for a subject

1. Read `<Subject>/CLAUDE.md` (create it for a new subject).
2. Extract the table of contents, choose the scope, write `00-Index.md`.
3. Per chapter: extract → read → verify numbers → design and verify 5 exercises → write.
4. After each chapter, update all three: the status row in `00-Index.md`, the "Current state" section above, and the subject's own `CLAUDE.md`. The third is the one that gets skipped.
5. When a subject is done, mark its `CLAUDE.md` complete and update the progress table.

## Choosing a scope

Use, in order: lecture slides; a user-written syllabus in `note/`; otherwise the standard scope for the course level. For textbook-only subjects, state the choice at the top of `00-Index.md` with a "not covered, and why" table and tell the user it needs confirming (`Econometrics/contents/00-Index.md` is the model).

## Extracting sources

`pypdf` and `python-pptx` are installed. Set `PYTHONIOENCODING=utf-8` (Vietnamese text breaks cp1252). The Read tool cannot render these PDFs, so extract text to a scratchpad file and read it in chunks:

```bash
PYTHONIOENCODING=utf-8 python -c "
from pypdf import PdfReader
import io
r = PdfReader('file.pdf')
out = []
for i in range(START, END):
    out.append('--- p%d ---' % (i+1))
    out.append((r.pages[i].extract_text() or '').strip())
io.open('out.txt','w',encoding='utf-8').write('\n'.join(out))
"
```

- Every book mangles maths differently; each subject's `CLAUDE.md` has its substitution table. Some ciphers are not fixed (Mankiw, D2L), so **never transcribe a formula**: rebuild it from the prose and check it against the book's printed numbers.
- Figures are images and never extract. Numeric tables set as text usually survive (check their subtotals). Before marking a figure lost, check whether the prose states its data.
- Some books destroy code (Goodrich: indentation and double underscores lost); details are in the subject files.

## Lessons that apply to every subject

- A self-consistent check is not verification; test against something independent of the model that produced the number.
- When you state an approximation, compute its error at a few magnitudes.
- Compare floats with a tolerance.
- Before filing an erratum, rule out your extraction, your arithmetic, an abridged table and alternative conventions. A false erratum is worse than a missed one.
- Recompute worked examples in full; if inputs are missing, back-solve them from the printed outputs.
- Put the source's scattered figures side by side and divide them; ask what a headline number actually measures and what a trivial model would score on the metric.
- Report conditioning rather than rank, compounded rates rather than per-unit rates, and typical values as well as means.
- If an invented illustration contradicts the finding it illustrates, delete it rather than tuning it.
- If a Bash call fails with a model-unavailable error, retry it.

## Progress

| Subject | Status |
|---|---|
| Data Preparation and Visualization | ✅ ch. 01–11 |
| Mathematical Statistics | ✅ ch. 01–09 |
| MLOps | ✅ ch. 01–11 |
| Machine Learning | ✅ ch. 01–10 (RL only) |
| Time-series Analysis | ✅ ch. 01–10 |
| Principle of Accounting | ✅ ch. 01–09 |
| Econometrics | ✅ ch. 01–12 |
| Probability Theory | ✅ ch. 01–10 |
| Linear Algebra | ✅ ch. 01–08 |
| Calculus | ✅ ch. 01–09 |
| Optimization | ✅ ch. 01–12 |
| Discrete Mathematics | ✅ ch. 01–10 |
| Data Structures and Algorithms | ✅ ch. 01–13 |
| Database Management Systems | ✅ ch. 01–11 |
| Basic Programming (C++) | ✅ ch. 01–11 |
| Commercial Banking | ✅ ch. 01–12 (3 errata) |
| Macroeconomics & Microeconomics | ✅ ch. 01–14 |
| Monetary and Financial Theories | ✅ ch. 01–12 (1 erratum) |
| Principles of Marketing | ✅ ch. 01–12 |
| Business Management | ✅ ch. 01–09 |
| Deep Learning | ✅ ch. 01–08 (rewritten concisely 2026-10-09) |
| Computer Vision | 🔄 01–08 from lectures; 09–14 drafts awaiting slides |
| Big Data Analytics | 🆕 sources added 2026-10-09, not started |
| Natural Language Processing | 🚫 `documents/` empty |
| PowerBI | 🚫 `documents/` empty |
| Programming for Data Science (Python) | 🚫 `documents/` empty |

Verify against the filesystem rather than trusting this table.

## Skills

`obsidian-markdown`, `obsidian-cli`, `obsidian-bases`, `json-canvas`, `defuddle` (for URL sources).
