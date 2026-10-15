# Discrete Mathematics

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata: `contents/00-Index.md`.

## Source

**Johnsonbaugh, *Discrete Mathematics* 8e** (Pearson, 2018) — `documents/Discrete Mathematics by Richard Johnsonbaugh (z-lib.org).pdf`, 773 pages. **No lecture slides.** **Book page $n$ = PDF page $n+21$.** Note $n$ = book chapter $n$ (ch. 1–10).

**No mathematical error found anywhere in ch. 1–10**: every defect is extraction damage. Don't go looking for errata.

## Extraction

Born-digital with real Unicode maths: `∈ ∪ ∩ ⊆ ∅ ∀ ∃ ≡ → ¬ ⌊⌋ ⌈⌉` survive, and prose, definitions and theorems extract cleanly. **Displayed maths does not:**

| What you see | What it is |
|---|---|
| `A ∪A = U`, `(A ∪B) = A ∩B` | **Overlines silently deleted**: complements arrive as plain `A`, so De Morgan etc. read **false as written**. The most dangerous quirk |
| `Basis Step ( n = 1)` with nothing after | **Displayed equations in worked examples drop out** (every induction in ch. 02, derivations in ch. 04 and 07, $P(n,r)$/$C(n,r)$ in ch. 06, ch. 10's flow formulas) |
| `Algorithm 5.3.3 …` then nothing | **Algorithm boxes arrive empty** (only 4.4.2 and 9.6.1 survived): all pseudocode is my own Python, verified by running it |
| `/Omega1`, `/Theta1` | $\Omega$, $\Theta$ |
| `lg n` | $\log_2 n$ throughout |
| `d |/n`, `x /∈ Z`, `X ̸=Y`, `x =− 3` | $d\nmid n$, $x\notin Z$, $X\ne Y$, $x=-3$ |
| `24 23 22 21 0 1 2`, `!2` | **inside figures only**: `2` is minus, `!` a radical |
| `Johnsonbaugh-50623 book February 3, 2017 13:58`, `k / k k / k` | running header and registration marks: strip both |
| `thatx ∈ A` | spaces lost at font changes: search short fragments, not phrases |

Strip the header with `re.sub(r'Johnsonbaugh-50623 book \w+ \d+, \d+ \d+:\d+', '', t)` and `re.sub(r'^\s*k( k)?\s*$', '', t, flags=re.M)`.

**All figures are lost**, structural for ch. 08–10: notes describe objects by explicit vertex/edge sets, degrees and matrices.

## Boundaries

- **`Data Structures and Algorithms/` owns the implementations; this subject owns the mathematics** (big-O, recurrences, graph/tree theory, Prim/Kruskal/Dijkstra correctness). Recorded in both indexes.
- `Probability Theory/` owns serious probability (ch. 06 here is counting only). `Optimization/contents/10 - Duality.md` redirects max-flow/min-cut here: read the two together. `Database Management Systems/` owns normalisation and keys. `Linear Algebra/contents/02` for relation and adjacency matrices.
- Chapters pay forward debts (quantifiers → big-O, pigeonhole → hashing and Hall, $\lg(n!)$ + $h\ge\lg t$ → the $\Omega(n\lg n)$ sorting bound in ch. 09). Keep those cross-links when editing.

## Open items

Scope (ch. 1–10; ch. 11 Boolean algebras and ch. 12 automata excluded) is my decision. If the syllabus arrives, likely mismatches: Karnaugh maps (J11), automata and regular-expression theory (J12), closest-pair (J §7.4), resolution proofs (J §2.3). Each needs a **new chapter file plus an index update**, not an edit to an existing note.
