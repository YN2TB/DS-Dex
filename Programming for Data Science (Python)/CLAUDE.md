# Programming for Data Science (Python) — subject context

**Status: 🚫 blocked. Do not start.**

## Why

**`documents/` is empty.** There is no source material of any kind — no slides, no textbook, no notebooks. `contents/` is empty and must stay that way.

Writing notes here from general knowledge would violate the vault's core rule (root `../CLAUDE.md`): *notes are built from the user's course material, and gaps are flagged rather than invented*. It is especially tempting for this subject, because the content is so familiar — which is exactly why the rule matters. A confident-looking note matching no syllabus and no lecturer's conventions is worse than an empty folder.

## What to do instead

**If the user asks about this subject, say the material is missing and ask them to supply it.** Most useful: the lecture notebooks or slides, the lab/assignment sheets, the assessment brief, or a photographed syllabus.

**Once any material arrives:** treat it as a normal new subject — read everything, then write `00-Index.md` first, then chapters. Verify by *running* the code, as in `Data Structures and Algorithms/CLAUDE.md`.

## Note the overlap before writing anything

Substantial Python content **already exists** in the vault and should be linked, not duplicated:

- `Data Preparation and Visualization/contents/01 - Getting Started with Pandas.md` through `03` — pandas, indexing, groupby
- `Data Preparation and Visualization/contents/10 - Visualization with Matplotlib and Seaborn.md`
- `Data Structures and Algorithms/` (not yet written) will own Python data structures and complexity
- `MLOps/contents/02 - Environment Setup.md` — virtualenvs, dependency management, project layout

**When material arrives, map it against these first** and record in `00-Index.md` which chapters are new and which are cross-links. The likely genuinely-new content is core-language material (functions, comprehensions, OOP, error handling, file I/O, NumPy fundamentals) that the applied subjects assume rather than teach.

Same situation: `PowerBI/`.
