# Data Structures and Algorithms — subject context

**Status: ✅ COMPLETE.** `contents/00-Index.md` plus **all 13 chapters written, with every code listing executed and every complexity claim measured.**

## Sources — and the split between them

| File | Pages | Role |
|---|---|---|
| `Data Structures and Algorithms in Python ( PDFDrive ) (1) (1).pdf` | 770, 15 ch | **Goodrich, Tamassia & Goldwasser** — the spine: structure, theory, analysis, coverage |
| `Fundamentals-of-python-data-structures-2nbsped-...pdf` | 450, 12 ch | **Lambert** — narrower, but **the only usable source of code** (see below) |

**No lecture slides.** Scope is an editorial decision, recorded at the top of `contents/00-Index.md`: **13 chapters covering Goodrich 1–14 plus §15.3 (B-trees) folded into ch. 10.** Needs syllabus confirmation.

## ⚠️ The decisive finding: Goodrich's code cannot be transcribed, Lambert's can

**This is the most consequential extraction discovery in the vault**, because here the code *is* the content.

**Goodrich's Python is destroyed.** A Code Fragment arrives as:
```
1 class GameEntry:
4 def  init  (self,n a m e ,s c o r e ) :
5 self.  name = name
```
Three compounding failures:
1. **All indentation lost** — syntactically fatal in Python, and the block structure is unrecoverable without understanding the code.
2. **Double underscores render as spaces** — `__init__`→`init`, `_name`→`name`, `get_score`→`get score`. **The most dangerous, because the result looks plausible and is wrong.**
3. **Identifiers space-separated**, operators broken: `(self,n a m e ,s c o r e )`, `*=`→`=`.

Line numbers survive, which at least shows where lines begin.

**Lambert's Python extracts perfectly** — indentation, dunders, docstrings and identifiers all intact:
```python
class SavingsAccount(object):
    """This class represents a savings account
    with the owner's name, PIN, and balance."""

    def __init__(self, name, pin, balance = 0.0):
        self.name = name
```

**So: Goodrich for prose/theory/analysis; Lambert for code where the two overlap; my own implementations everywhere else.** Lambert covers roughly Goodrich 1–8, 10, 14 — **no heaps chapter, no balanced trees, no text processing**, so the advanced material (heaps, AVL/splay/red–black, skip lists, hash internals, B-trees, KMP, DP) is entirely mine.

**Every listing must be RUN before it goes in a note.** That is this subject's version of the verify-every-number rule, and here it is not optional — reconstructed code that merely *looks* right is exactly what the damage produces.

## Other extraction notes

- **Goodrich's prose extracts well**; maths in the analysis chapters is generally intact. Goodrich page $n$ ≈ PDF page $n+22$.
- **Lambert's TOC is caps-mangled** (`cHAP te R 1 b asic Python Programming`) and every page carries a Cengage copyright banner to strip. Body text is fine.
- **All figures in both books are lost** — every linked-list, tree-rotation, heap, hash-table and graph diagram. **Severe for ch. 06–10.** Compensate by printing the *actual state* of the structure from running code, which is better than a static diagram and is something only this subject can do.

## The Discrete Mathematics boundary — settled, and load-bearing

[[Discrete Mathematics/contents/00-Index|Discrete Mathematics]] is **complete**, and the split is recorded in both indexes: **Discrete Maths owns the mathematics, this subject owns the implementations.**

| Topic | Theory (do not re-derive) | Here |
|---|---|---|
| Big-O / $\Omega$ / $\Theta$ | DM ch. 04 | ch. 02 — apply **and measure** it |
| Recurrences | DM ch. 07 | ch. 03, 11 — read them off code |
| Induction & recursion | DM ch. 02 | ch. 03 — write and debug it |
| Graphs, trees | DM ch. 08–09, incl. **correctness proofs of Dijkstra/Prim/Kruskal** | ch. 07, 13 — adjacency lists, BFS/DFS, code |
| **$\Omega(n\lg n)$ sorting bound** | **DM ch. 09 §8** | ch. 11 — the algorithms meeting it |
| Hash collisions inevitable | DM ch. 06 (pigeonhole) | ch. 09 — what to do about them |
| Max-flow, matching | DM ch. 10 | ch. 13, in passing |

**Cross-link rather than re-prove.** **Amortised analysis (ch. 04) is the one major analytical topic Discrete Maths does not cover**, so develop it properly here.

## Chapter plan

| # | Title | Source | Status |
|---|---|---|---|
| 01 | Python and Object-Oriented Foundations | G1–2 | ✅ |
| 02 | Algorithm Analysis in Practice | G3 | ✅ |
| 03 | Recursion | G4 | ✅ |
| 04 | Array-Based Sequences and Amortised Analysis | G5 | ✅ |
| 05 | Stacks, Queues and Deques | G6 | ✅ |
| 06 | Linked Lists | G7 | ✅ |
| 07 | Trees and Traversals | G8 | ✅ |
| 08 | Priority Queues and Heaps | G9 | ✅ |
| 09 | Maps, Hash Tables and Skip Lists | G10 | ✅ |
| 10 | Search Trees | G11 + G15.3 | ✅ |
| 11 | Sorting and Selection | G12 | ✅ |
| 12 | Text Processing and Dynamic Programming | G13 | ✅ |
| 13 | Graph Algorithms | G14 | ✅ |

**Lambert's coverage ran out at ch. 08** — he has no heaps, balanced-trees or text-processing chapter. **Ch. 08 onward is entirely my own code.**

## Findings so far, worth carrying

- **Ch. 02 established the method:** derive the complexity, then **measure by doubling $n$ and reading the time ratio** (2 / 4 / 8 for linear / quadratic / cubic). The constant cancels, so it is machine-independent — quote **ratios**, not absolute times.
- **Ch. 03:** naive Fibonacci grows as $\phi^n$ — predicted ratio $\phi^2=2.618$ per two steps, **measured 2.51/2.55/2.70.** A direct empirical sighting of the golden ratio derived in `Discrete Mathematics/contents/07`.
- **Ch. 04:** amortised $O(1)$ `append` conceals a real spike — the slowest of 200 000 appends was **5 084× the mean**. **Amortised bounds are for throughput, not latency.**
- **Ch. 06:** the textbook locality argument is **much weaker in Python** — arrays beat linked lists on traversal by only ~15%, because Python lists are *referential* and both chase pointers. True in C/NumPy, not here.
- **Ch. 09:** dict beats list on search by **462× → 5 772× → 54 018×** at $n=10^4/10^5/10^6$ — the *growing* ratio is the $O(1)$-vs-$O(n)$ signature. And a `BadHash` class returning `1` for every key made lookups genuinely $O(n)$ (fixed lookup count, ratios 1.96/2.21 as $n$ doubled) — **the hash-flooding DoS, demonstrated rather than asserted.** Measured mean chain length equals the load factor *exactly*.
- **Ch. 11:** counted comparisons against the $\lg(n!)$ bound — **merge-sort lands within 1–2% of the information-theoretic minimum** (1.02×/1.02×/1.01×), randomised quicksort 25–39% above. Verified $\lg(n!)/(n\lg n)=1-1.4427/\lg n$ to three decimals. Timsort on $n=10^6$: **all-equal input 55× faster than random**, sorted 8.5× — *sorted input is Timsort's best case and naive quicksort's worst* (measured 73× slower). `sorted()` beats my Python merge-sort by **14×** at the same complexity class.
- **Ch. 13 (last):** **Dijkstra returning a wrong answer on a negative edge** (1 and 6 against the true −1 and 4) — Goodrich states the non-negativity requirement but never shows the violation, and a *silent* wrong answer is a sharper lesson than any proof. Also: an adjacency **map** ties the matrix even on edge lookup (dict = hash table), while losing neighbour iteration by **38×** — so the textbook trade-off is weaker than usually stated. DFS reported distance 5 for a vertex adjacent to the source.
- **Ch. 12:** the four-scenario pattern-matching table is the chapter's best result — **each algorithm's worst case is the mirror image of another's** ($P=a^{m-1}b$ costs brute force 790 100 comparisons and Boyer–Moore 7 901; $P=b\cdot a^{m-1}$ reverses it *exactly*), while KMP stays 8 099–16 098 everywhere. Also: **KMP and brute force are within 0.1% on real text** (large alphabet ⇒ mismatch on the first character ⇒ KMP never engages), naive LCS makes *exactly* $2\binom{2n}{n}-1$ calls (verified at six sizes; $n{=}50$ ⇒ $10^{15}$ years vs 2 601 table cells), and **Huffman lands 1.1% above the Shannon entropy** — Goodrich never mentions entropy, so that comparison is an addition and mirrors ch. 11's merge-sort-vs-$\lg(n!)$ result.
- **A recurring methodological failure, now four times:** the *first* measurement misled in ch. 08 (needed a constructed worst case), ch. 10 (recursive-vs-iterative → count node visits), ch. 11 (Python-vs-C → count operations), ch. 12 (twice — asserted a conclusion the printed table contradicted, and used random strings whose call counts weren't even monotonic). **When a measurement contradicts a sound proof, suspect the measurement.** Hold the implementation constant, count operations, and **construct the worst case rather than sampling for it**. Ch. 12 records its two corrections in the note itself rather than fixing them silently.
- **Ch. 10 — the best experiment so far.** Goodrich states splay trees' *static optimality* but never tests whether it pays. Three stages: (i) **node visits confirm the theory** — under 99% skew splay visits 9.26/access vs AVL's 14.01, and *loses* under uniform access (18.53 vs 13.59); (ii) **wall clock contradicts it** — splay 0.0633s vs AVL 0.0436s; (iii) **the same splay tree read-only takes 0.0264s, fastest of all.** So the adapted *shape* is excellent and the restructuring-on-every-read is what costs. Corollary that settles it practically: **splay reads mutate, so they need a write lock and cannot be concurrent.** Also verified $n(h)=F_{h+2}-1$ *exactly* (Goodrich only argues exponential growth), giving AVL's $1.4404\lg n$ — **$\varphi$ again, now in tree shape rather than ch. 03's running time.**
- **Ch. 08 — the most important one:** measurement *contradicted* the textbook. Heapify is $O(n)$ against insertion's $O(n\log n)$, yet **insertion won on random data** (1.28 swaps/element — it is $O(n)$ *expected*). The gap appears only on **constructed worst-case descending input** (14.69 vs 1.00; heapify 4.6–5× faster). **Always benchmark a deliberately built worst case.**

## Verification standard for this subject

Different from every other subject in the vault. The unit of verification is a **program**, not a number:

1. **Run every listing.** It must execute.
2. **Test the edge cases** — empty, single element, duplicates, already-sorted, reverse-sorted.
3. **Measure the complexity claim** — time a growing input and check the ratio follows the predicted curve, rather than copying the book's assertion.

## Errata

*(Empty so far.)* Full table in `contents/00-Index.md`.

## If the syllabus arrives

Likely mismatches, in order:
1. **Memory management and the memory hierarchy** (G §§15.1–15.2) — excluded as architecture; B-trees were kept and moved to ch. 10.
2. **Text processing depth** (G13) — ch. 12 keeps pattern matching, tries and DP; if the course wants full compression/regex theory, it needs more.
3. **The Python primer** (G1) — compressed into ch. 01 on the assumption of existing Python fluency. **Note ch. 01 is the only place in the vault that teaches core Python**, since `Programming for Data Science (Python)` is blocked for lack of material.
