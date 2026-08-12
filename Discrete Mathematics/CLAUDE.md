# Discrete Mathematics — subject context

**Status: ✅ complete** (2026-07-30). `contents/00-Index.md` plus chapters **01–10**, all verified.

## Source

**Johnsonbaugh, *Discrete Mathematics* 8e** (Pearson, 2018) — `documents/Discrete Mathematics by Richard Johnsonbaugh (z-lib.org).pdf`, **773 pages, 12 chapters**. **No lecture slides.**

**Book page $n$ = PDF page $n+21$.**

## Scope — my editorial decision, needs syllabus confirmation

**Johnsonbaugh chapters 1–10, one note per chapter, mapped 1:1** (note $n$ = book chapter $n$ — easy to hold in your head).

**Excluded: ch. 11 (Boolean Algebras and Combinatorial Circuits)** — digital logic, whose mathematical content is propositional logic already in ch. 01 — **and ch. 12 (Automata, Grammars, and Languages)** — theory of computation, which presupposes nothing from ch. 1–10 and leads nowhere within them. **One partial regret:** §12.3–12.5 is where regular expressions come from, and regex is a daily DS tool; the *practical* skill is in `Data Preparation and Visualization/contents/05`, the *theory* is nowhere in the vault.

Full reasoning, plus the smaller omissions (§8.8 Instant Insanity, §9.9 game trees, §7.4 closest-pair, §2.3 resolution proofs), is in `contents/00-Index.md`'s "what is not covered, and why" table.

## Chapters

| # | Title |
|---|---|
| 01 | Sets and Logic |
| 02 | Proofs and Mathematical Induction |
| 03 | Functions, Sequences and Relations |
| 04 | Algorithms and Their Analysis |
| 05 | Number Theory and Cryptography |
| 06 | Counting Methods and the Pigeonhole Principle |
| 07 | Recurrence Relations |
| 08 | Graph Theory |
| 09 | Trees |
| 10 | Network Flows and Matching |

## Extraction — the best-and-worst source in the vault

**Johnsonbaugh's PDF is born-digital with real Unicode mathematics.** `∈`, `∪`, `∩`, `⊆`, `∅`, `∀`, `∃`, `≡`, `→`, `¬`, `∴`, `⌊⌋`, `⌈⌉` and set-builder braces all survive intact. **Prose, definitions and theorem statements extract cleanly** — better than any textbook here except Silver's Beamer slides.

**But the displayed mathematics does not.** Three systematic failures, in rough order of danger:

| What you see | What it is |
|---|---|
| `A ∪A = U`, `(A ∪B) = A ∩B`, `A = A` | **⚠️ Overlines are silently deleted.** Complement $\overline A$ becomes plain `A`, so the complement, involution and De Morgan laws arrive **false as written** rather than visibly garbled. The most dangerous quirk in the book |
| `Basis Step ( n = 1)` / `Inductive Step` with nothing between | **Displayed equations inside worked examples drop out.** Every induction in ch. 02, every asymptotic derivation in ch. 04, every recurrence solution in ch. 07, all of ch. 06's $P(n,r)$/$C(n,r)$ formulas and ch. 10's conservation and cut-capacity formulas |
| `Algorithm 5.3.3 Euclidean Algorithm` then input/output lines and nothing | **Numbered Algorithm boxes arrive as empty headings.** Only **two** survived in ten chapters: Algorithm 4.4.2 (factorial) and Algorithm 9.6.1 (preorder traversal) |
| `/Omega1`, `/Theta1` | $\Omega$, $\Theta$ (ch. 04 on) |
| `lg n` | **$\log_2 n$**, stated once and used throughout; misreading it shifts every logarithmic figure by $\ln2$ |
| `d |/n`, `x /∈ Z`, `X ̸=Y`, `x =− 3` | $d\nmid n$, $x\notin Z$, $X\ne Y$, $x=-3$ (minus migrates onto the `=`) |
| `24 23 22 21 0 1 2`, `!2` | **Inside figures only**, `2` is a minus sign and `!` a radical: $-4,-3,-2,-1,0,1,2$ and $\sqrt2$ |
| `Johnsonbaugh-50623 book February 3, 2017 13:58` + a `k / k k / k` block | Running header and registration marks — **strip both** |
| `thatx ∈ A`, `iscalledthe intersectionofX andY` | **Spaces lost at italic/maths font transitions**, and in ordinary prose too. Makes text search unreliable — search short distinctive fragments, not phrases |

**Extraction recipe** (header-stripping included):

```python
from pypdf import PdfReader
import io, re
r = PdfReader('documents/Discrete Mathematics by Richard Johnsonbaugh (z-lib.org).pdf')
out = []
for i in range(START, END):                     # PDF index = book page + 20
    t = r.pages[i].extract_text() or ''
    t = re.sub(r'Johnsonbaugh-50623 book \w+ \d+, \d+ \d+:\d+', '', t)
    t = re.sub(r'^\s*k( k)?\s*$', '', t, flags=re.M)
    t = re.sub(r'\n{3,}', '\n\n', t)
    out.append('--- book p%d ---' % (i - 20)); out.append(t.strip())
io.open('john_chN.txt', 'w', encoding='utf-8').write('\n'.join(out))
```

**Two consequences for how these notes were written.** (i) **All pseudocode is my own Python reconstruction**, verified by *running* it — the primality test, Euclidean algorithm, modular exponentiation, insertion sort, binary search, merge, Prim, Kruskal, the three traversals, Dijkstra and the max-flow labelling algorithm. (ii) **Every worked number was recomputed** before being written.

**All figures are images and are lost.** This is structural for ch. 08–10, which are taught through diagrams — every Venn diagram, arrow diagram, digraph, tree drawing, Königsberg map, $K_5$/$K_{3,3}$ picture, flow network and matching diagram. **The notes therefore describe objects by explicit vertex/edge sets, degrees and matrices** rather than referring to lost pictures, and several examples are my own replacements.

## Two data recoveries from the book's own fragments

Worth recording as evidence the technique works:

- **Ch. 03, Example 3.1.16's PRNG constants.** Only $m=11$, seed $3$, the opening $3,4,0,5$ and $x_{10}=3$ survive. Those conditions have the unique solution $x_n=(7x_{n-1}+5)\bmod11$, whose full cycle $3,4,0,5,7,10,9,2,8,6$ has period 10 and matches every printed value.
- **Ch. 05, Table 5.3.2** (Euclidean worst case) extracts as unaligned digit soup. **Recovered by independent exhaustive search:** the smallest pair needing $n$ modulus operations is $(f_{n+2},f_{n+1})$, verified for $n=0,\dots,7$ — confirming the book's Fibonacci observation rather than transcribing it.

## Errata — deliberately empty

**No mathematical error was found anywhere in ch. 1–10.** Ten chapters, every numeric claim recomputed, and the book was right every time. **Johnsonbaugh is the only textbook in this vault of which that is true.** Do not go looking for errata; every defect here is extraction damage.

One resolved ambiguity is recorded in `contents/00-Index.md` (Example 10.4.1's applicant $B$).

## The forward-reference chain

This subject was written so that each chapter pays a debt incurred earlier. Worth knowing, because it is what the cross-links carry:

- ch. 01's **nested quantifiers** → ch. 04's big-O ($\exists C\,\forall n$ is the whole definition)
- ch. 02's **induction/recursion identity** → ch. 04's correctness proofs, ch. 07's recurrences
- ch. 02's **Quotient–Remainder Theorem** → ch. 03's `mod`, ch. 05's Euclidean algorithm
- ch. 03's **congruence as an equivalence relation** → ch. 05's modular arithmetic
- ch. 03's **$(A^k)_{ij}$ counts walks** → ch. 08's adjacency matrices
- ch. 04's **$\lg(n!)=\Theta(n\lg n)$** + ch. 06's **$n!$ permutations** + ch. 09's **$h\ge\lg t$** → **ch. 09's $\Omega(n\lg n)$ sorting bound**, the subject's most-deferred result (promised in ch. 04, 07 and 08)
- ch. 05's **Fibonacci worst case** → ch. 07's Binet formula, which *derives* the $\phi$ asserted there
- ch. 06's **pigeonhole** → ch. 03's hash collisions, ch. 09's decision trees, ch. 10's Hall's theorem
- ch. 08–09's greedy algorithms → ch. 10's duality

## Additions beyond the source

Each is labelled in that chapter's gaps callout. The substantial ones:

- **ch. 01:** De Morgan in pandas; the converse error *is* $P(A|B)$ vs $P(B|A)$; affirming the conclusion *is* the base-rate fallacy
- **ch. 03:** pigeonhole explanation of why hash collisions are inevitable; exhaustive error-detection analysis of Luhn (all single-digit errors and transpositions caught, $0\!\leftrightarrow\!9$ the blind spot); `int()` vs `math.floor()` and cross-language `%`
- **ch. 04:** the quantifier unpacking of big-O and why reversal trivialises it; "$=$" as abuse of notation; log-base vs exponent-base asymmetry; **binary search** (absent from the book) as the cleanest case needing *strong* induction
- **ch. 05:** Lamé's derivation ($n$ steps ⟹ $a\ge f_{n+2}\approx\phi^{n+2}$, hence $O(\log a)$); **the extended Euclidean algorithm** (only in exercises there) since RSA needs it; the full RSA security discussion — Shor's algorithm, fixed points, OAEP, and the cheap/expensive asymmetry table
- **ch. 06:** the **four-case table** (ordered? repeats?), assembled from results the book states separately; the **stars-and-bars bijection**; double-counting as a technique; a pigeonhole exercise whose naive hole choice fails
- **ch. 07:** the **five recurrence shapes** and the $2a_{n/2}+cn$ vs $2a_{n-1}+c$ contrast; why the repeated root needs the factor $n$; Binet is numerically treacherous
- **ch. 08:** bipartite **iff no odd cycle**; components as equivalence classes; the Euler-path table; Dijkstra's correctness and its failure on negative weights; **$e\le3v-6$ and $e\le2v-4$** derived rather than left implicit
- **ch. 09:** **traversals as prefix/infix/postfix**, with inorder losing the grouping (`3 + 5 * 2` evaluating wrongly) — the book gives the traversals with no application; the exchange-argument framing; merge sort is optimal *in order* but not exactly (49 vs a floor of 45 at $n=16$)
- **ch. 10:** **Hall's theorem** stated properly (only implicit in the book) and its necessity proved by exhibiting a cut; **§5 in its entirety** — max-flow/min-cut *as* LP duality, total unimodularity, min cut as sensitivity information

## Cross-subject boundaries, as agreed in `contents/00-Index.md`

- **[[Data Structures and Algorithms/contents/00-Index|DSA]]** — **this subject owns the mathematics, DSA owns the implementations.** Big-O is defined and proved here, applied there; recurrences are solved here, used there; graphs and trees are mathematical objects here (Euler circuits, planarity, isomorphism, correctness proofs of Prim/Kruskal/Dijkstra) and data structures there (adjacency lists, BFS/DFS code, balanced BSTs). **Recorded in both indexes.**
- **[[Probability Theory/contents/01 - Combinatorial Analysis|Probability Theory]]** — ch. 06 is the same counting theory; **all serious probability is deferred there** (Johnsonbaugh §§6.5–6.6 are ~16 optional pages, Ross is far deeper).
- **[[Optimization/contents/10 - Duality|Optimization]]** — **ch. 10's max-flow/min-cut is the duality theorem Optimization's index explicitly redirects here.** Read the two together.
- **[[Database Management Systems/contents/00-Index|DBMS]]** — ch. 03 §8 keeps only "a table *is* an $n$-ary relation" and defers normalisation and keys.
- **[[Linear Algebra/contents/02 - Matrix Algebra|Linear Algebra]]** — ch. 03's relation matrices and ch. 08's adjacency matrices.

## If the syllabus arrives

The **scope is unconfirmed**. Most likely mismatches, in order:

1. **Boolean algebras / circuit minimisation** (J11) — if Karnaugh maps are examinable, this is missing.
2. **Finite-state machines, automata, regular languages** (J12) — including the *theory* of regular expressions.
3. **The closest-pair problem** (J §7.4) — an elegant $\Theta(n\lg n)$ divide-and-conquer geometry application, and the omission from ch. 07 a reader might most regret.
4. **Resolution proofs** (J §2.3) — the basis of Prolog and SAT solvers.

Adding any of these needs a **new chapter file plus an index update**, not an edit to an existing note.
