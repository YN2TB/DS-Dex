# PowerBI — subject context

**Status: 🚫 blocked. Do not start.**

## Why

**`documents/` is empty.** There is no source material of any kind — no slides, no textbook, no exports. `contents/` is empty and must stay that way.

Writing notes here from general knowledge would violate the vault's core rule (root `../CLAUDE.md`): *notes are built from the user's course material, and gaps are flagged rather than invented*. A whole subject written from general knowledge is that failure at maximum scale — it would look identical to a real note while matching no syllabus, no lecturer's notation, and no exam.

## What to do instead

**If the user asks about this subject, say the material is missing and ask them to supply it.** Useful things to ask for, in order of value: the lecture slides, the `.pbix` files used in class, the lab/practical handouts, the assessment brief, or even a photographed syllabus.

**Once any material arrives:** treat it as a normal new subject — read everything, then write `00-Index.md` first, then chapters. If only a syllabus arrives without teaching material, write `00-Index.md` alone (the scope is then *given*, not an editorial decision) and tell the user which chapters cannot be written yet.

## Where its content would attach

- `Data Preparation and Visualization/contents/11 - Chart Design and Data Storytelling.md` — the visual-design principles are tool-independent and already written.
- `Database Management Systems/` — star schemas, OLAP and the dimensional model are the data layer underneath a Power BI report. That subject should own the modelling theory; this one would own DAX, Power Query and the report canvas.

Same situation: `Programming for Data Science (Python)/`.
