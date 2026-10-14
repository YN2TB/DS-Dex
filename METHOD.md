# METHOD — how a DS-Dex note is made

The factory every subject shares. Routing and status: `CLAUDE.md`. A subject's own quirks: `<Subject>/CLAUDE.md`.

## Folder shape

```
[Subject Name]/
  CLAUDE.md               ← subject context (shape below)
  contents/
    00-Index.md           ← map of content: scope decision, chapter list with status, errata table, cross-subject links
    01 - [Chapter Topic].md
  documents/              ← source PDFs (documents/slides/ or slides/ if the course has slides)
  note/                   ← my own material: read, never edit
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

A subject with almost no formulas may adapt the template rather than pad it (`Principles of Marketing/CLAUDE.md` has the reasoning).

## Style

- **Write plainly and concisely** (my request, 2026-10-09). Short sentences, bold only for key terms, callouts only where they help, no "⚠️" on every line, no commentary about the vault itself or about what the source "never says". Depth comes from content (derivations, tables, worked examples), not from length.
- Flag gaps, never invent. Label additions beyond the source in the gaps callout.
- **Verify every number** with `sympy`/`numpy`/`fractions` before writing it, including every exercise answer.
- Wikilinks (including cross-subject and forward links), tags, callouts, LaTeX.

## Workflow for a subject

1. Read the root `CLAUDE.md`, then `<Subject>/CLAUDE.md`.
2. Extract the table of contents, choose the scope, write `00-Index.md` first, so the scope decision survives an early stop.
3. Per chapter: extract → read → verify numbers → design and verify 5 exercises → write.
4. After each chapter (and on "checkpoint"): update the chapter's status in `00-Index.md` and the subject's Progress row in the root `CLAUDE.md`. Put any new extraction quirk, boundary or open item in `<Subject>/CLAUDE.md`. Findings go in the chapter, not in `CLAUDE.md`. Claude can't see the session limit, so update at natural boundaries.
5. When the subject is done, mark its Progress row ✅.

## New subject

Create `<Subject>/CLAUDE.md` in this shape. Aim for ≤ 40 lines; a subject with heavy extraction tables may run longer (≤ 50), and the tables are kept whole.

```
# <Subject>
Read with the root CLAUDE.md and ../METHOD.md. Scope, chapters, errata: contents/00-Index.md.
## Sources        files, page offsets, lecturer
## Extraction     quirks and substitution tables
## Boundaries     cross-subject ownership
## Open items     gaps to raise with the lecturer; what to do if a syllabus or slides arrive
```

Then add its row to the root Progress table. A subject whose `documents/` is empty is 🚫 blocked: don't write notes from general knowledge.

## Choosing a scope

Use, in order: lecture slides; a syllabus I wrote in `note/`; otherwise the standard scope for the course level. For textbook-only subjects, state the choice at the top of `00-Index.md` with a "not covered, and why" table and tell me it needs confirming (`Econometrics/contents/00-Index.md` is the model).

## Extracting sources

`pypdf` and `python-pptx` are installed. Set `PYTHONIOENCODING=utf-8` (Vietnamese text breaks cp1252). The Read tool can't render these PDFs, so extract text to a scratchpad file and read it in chunks:

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
- If a Bash call fails with a model-unavailable error, retry it.

## Lessons that apply to every subject

- A self-consistent check is not verification; test against something independent of the model that produced the number.
- When you state an approximation, compute its error at a few magnitudes.
- Compare floats with a tolerance.
- Before filing an erratum, rule out your extraction, your arithmetic, an abridged table and alternative conventions. A false erratum is worse than a missed one.
- Recompute worked examples in full; if inputs are missing, back-solve them from the printed outputs.
- Put the source's scattered figures side by side and divide them; ask what a headline number actually measures and what a trivial model would score on the metric.
- Report conditioning rather than rank, compounded rates rather than per-unit rates, and typical values as well as means.
- If an invented illustration contradicts the finding it illustrates, delete it rather than tuning it.

## Concise rewrite (paused)

My request of 2026-10-09, paused 2026-10-14 for token cost. Rewrite each older subject's chapters in the plain style above, keeping verified content. Skip Computer Vision (already reworked). Recheck numbers while rewriting: each pass so far found 3–4 slips in old exercises (record them in the subject's errata). Also shorten the subject's `00-Index.md`. Order: the root Progress table from the top. Mark a finished subject ✂️ in its Progress row.

## Skills

`obsidian-markdown`, `obsidian-cli`, `obsidian-bases`, `json-canvas`, `defuddle` (for URL sources).
