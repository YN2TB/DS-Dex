---
subject: Data Structures and Algorithms
chapter: 12
tags: [ds, dsa, pattern-matching, kmp, boyer-moore, dynamic-programming, lcs, huffman, greedy, tries, compression]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 13"
---

# Text Processing and Dynamic Programming

This chapter is bound together by one question: **when can you avoid redoing work you have already done?**

- **§§1–4, pattern matching.** After a mismatch, the brute-force scan throws away everything it just learned and starts again one position along. **KMP never does** — it remembers, and becomes linear.
- **§§5–7, dynamic programming.** Naive recursion recomputes identical subproblems exponentially often. **Storing each answer once** turns $4^n$ into $n^2$ — a factor that reaches $10^{29}$ at $n=50$.
- **§8, Huffman coding.** A *greedy* algorithm that provably lands within one bit per symbol of the information-theoretic minimum — [[11 - Sorting and Selection|ch. 11]]'s lower-bound theme in a second setting.
- **§9, tries.** Sharing common prefixes between stored words, so a lookup costs the length of the key rather than the size of the dictionary.

**This is also the chapter where measurement corrected me twice**, and both corrections are recorded in place (§3 and §6) because the mistakes are more instructive than the results.

## 📘 Main Knowledge

### 0. Correctness first

Three pattern-matching algorithms were checked against Python's `str.find()` on ten hand-picked cases — empty pattern, empty text, no match, match at the start, match at the end, overlapping repeats (`"aaaa"`/`"aa"`), and the classic tricky pairs (`"mississippi"`/`"issip"`, `"abababab"`/`"babab"`) — **then stress-tested on 3 000 random string pairs over the alphabet $\{a,b\}$.**

**Zero failures.** *(A two-letter alphabet is deliberate: it maximises accidental partial matches, which is exactly where these algorithms break.)*

### 1. Brute-force matching

Try every alignment; at each, compare until a mismatch.

```python
for i in range(n - m + 1):
    k = 0
    while k < m and T[i + k] == P[k]:
        k += 1
    if k == m:
        return i
```

**$O(nm)$ worst case.** The waste is specific and worth naming: **after a mismatch at $P[k]$, the algorithm restarts at $T[i+1]$, re-reading $k$ characters it has already seen.** Everything below attacks that waste.

### 2. Boyer–Moore — compare backwards, and skip

Two ideas, both counter-intuitive.

**Compare the pattern right-to-left.** A mismatch at the *end* of the pattern rules out that alignment just as decisively as one at the start — but it tells you about a character further along in the text.

**The character-jump heuristic.** On a mismatch against text character $c$: if $c$ does not occur in the pattern at all, **no alignment overlapping this position can work, so jump the whole pattern past it.**

```python
    last = {P[k]: k for k in range(m)}       # last occurrence of each character
    ...
    j = last.get(T[i], -1)
    i += m - min(k, j + 1)                   # jump forward, possibly by m
```

**This is why Boyer–Moore can be *sublinear*** — it may never look at most of the text. No left-to-right algorithm can do that.

### 3. KMP — never move backwards in the text

The **failure function** $f(k)$ = the length of the longest proper prefix of $P[0..k]$ that is also a suffix of it. On a mismatch at position $k$, **resume at $f(k-1)$ instead of restarting**: the prefix of that length is already known to match, because it *is* the text just read.

```
P      = a b a c a b
index  = 0 1 2 3 4 5
f[k]   = 0 0 1 0 1 2
```

*(Verified.)* $f[5]=2$ because `abacab` begins and ends with `ab`; $f[4]=1$ because `abaca` begins and ends with `a`.

```python
        elif k > 0:
            k = fail[k - 1]       # move the PATTERN back; j never decreases
        else:
            j += 1
```

**The text index `j` never decreases.** Each iteration either advances `j` or decreases `k`, and `k` only ever grows when `j` does — so the loop runs $O(n)$ times. Building the failure function is $O(m)$ by the same argument applied to the pattern against itself. **Total $O(n+m)$** (Goodrich Prop. 13.3).

#### 3.1 Each algorithm has its own adversary — and a correction

*(Character comparisons, $n=8\,000$, $m=100$. The linear-scan baseline is 8 000.)*

| input | brute force | Boyer–Moore | KMP |
|---|---|---|---|
| $T=a^n$, $P=a^{m-1}b$ | **790 100** | 7 901 | 16 098 |
| $T=a^n$, $P=b\cdot a^{m-1}$ | 7 901 | **790 100** | 8 099 |
| random binary $\{a,b\}$ | 15 793 | 11 916 | 10 831 |
| random 26-letter | 8 211 | **279** | 8 406 |

*(All verified.)* **The symmetry in the first two rows is the point.**

- **Row 1 is brute force's worst case:** every alignment matches $m-1$ characters, then fails on the last — $\approx nm$ comparisons.
- **Row 2 is Boyer–Moore's worst case**, and it is the *mirror image*: comparing right-to-left, BM matches $m-1$ characters before failing on the first, and can only shift by 1. The same input that is easy for one is catastrophic for the other.
- **Row 4 shows BM at its best: 279 comparisons on 8 000 characters** — it looked at 3.5% of the text. Sublinear, as promised.
- **KMP is between 8 099 and 16 098 in every row** — never much more than $n$, on any input. **That is its entire value.**

> [!warning] A correction: my first analysis of row 1 was wrong
> I initially wrote that Boyer–Moore "degenerates here, its bad case too" — **while my own data showed BM using 7 901 comparisons, the fewest in the row.** The claim contradicted the table printed directly above it.
>
> **The error was assuming that an input bad for one algorithm is bad for all.** Constructing the real BM adversary ($P=b\cdot a^{m-1}$, row 2) showed the opposite: **the two worst cases are mirror images**, because the two algorithms compare in opposite directions.
>
> **The lesson is that "worst case" is always relative to a specific algorithm.** A benchmark input that punishes one algorithm may be the easiest possible input for another — so a single test input cannot rank algorithms, however carefully it is chosen.

#### 3.2 On ordinary text, the theory barely matters

*(Searching 200 000 characters of random English-like text for a 9-character pattern of rare letters:)*

| | comparisons | time |
|---|---|---|
| brute force | 207 634 | 0.0205 s |
| **Boyer–Moore** | **27 440** | **0.0039 s** |
| KMP | 207 366 | 0.0169 s |

*(Verified.)*

> [!note] KMP and brute force are within 0.1% of each other here
> **On a large alphabet, mismatches usually occur on the very first character**, so brute force almost never re-reads anything and KMP's failure function almost never engages. **KMP's advantage is a worst-case guarantee, not an average-case speed-up.**
>
> **Boyer–Moore, by contrast, wins by 7.6× — because skipping is an *average-case* mechanism** that fires constantly on a large alphabet.
>
> **Hence the practical ranking: use Boyer–Moore (or a hybrid) for real text; use KMP when the alphabet is small, the input adversarial, or a guarantee is required.** Production tools like `grep` use Boyer–Moore variants. *(Python's `str.find` uses a hybrid of BM and Horspool with a bloom filter — and beats all three of these, being C.)*

### 4. Dynamic programming — remember your subproblems

> [!note] When dynamic programming applies
> Two conditions:
> 1. **Optimal substructure** — an optimal solution is built from optimal solutions to subproblems.
> 2. **Overlapping subproblems** — the same subproblems recur many times.
>
> **The second is what makes it pay.** Divide-and-conquer ([[11 - Sorting and Selection|ch. 11]]) has condition 1 but *not* 2 — merge-sort's halves are disjoint, so there is nothing to reuse and no table to build.

**The longest common subsequence.** For $X$ of length $n$ and $Y$ of length $m$, let $L[i][j]$ be the LCS length of the first $i$ characters of $X$ and first $j$ of $Y$:

$$L[i][j]=\begin{cases}0 & i=0\text{ or }j=0\\ L[i-1][j-1]+1 & X_i=Y_j\\ \max\big(L[i-1][j],\,L[i][j-1]\big) & \text{otherwise}\end{cases}$$

```python
    for i in range(n):
        for j in range(m):
            if X[i] == Y[j]:
                L[i + 1][j + 1] = L[i][j] + 1              # match: extend the diagonal
            else:
                L[i + 1][j + 1] = max(L[i][j + 1], L[i + 1][j])
```

*(Verified: `GTTCCTAATA` vs `CGATAATTGAGA` gives length 6, one LCS being `GTTTAA` — checked to be a genuine subsequence of **both** strings, with length matching the table.)*

**Filling the table is $O(nm)$** — each of $(n+1)(m+1)$ cells is computed once in $O(1)$. *(Verified: doubling $n$ gave ratios **4.15, 4.32, 3.99** — quadratic.)*

**The table gives the *length*; the *sequence* is recovered by walking backwards from $L[n][m]$**, stepping diagonally on a match and otherwise toward the larger neighbour.

### 5. What memoisation is worth — the number is absurd

**The naive recursion is the same formula without a table.** Its worst case is two strings with **no characters in common**, so every call mismatches and spawns two more, sharing nothing:

$$T(i,j)=T(i-1,j)+T(i,j-1)+1 \quad\Longrightarrow\quad T(n,n)=2\binom{2n}{n}-1.$$

*(Verified exactly — not approximately:)*

| $n$ | measured calls | $2\binom{2n}{n}-1$ | ratio to previous |
|---|---|---|---|
| 2 | 11 | 11 ✓ | — |
| 4 | 139 | 139 ✓ | 12.6 |
| 6 | 1 847 | 1 847 ✓ | 13.3 |
| 8 | 25 739 | 25 739 ✓ | 13.9 |
| 10 | 369 511 | 369 511 ✓ | 14.4 |
| 12 | 5 408 311 | 5 408 311 ✓ | 14.6 |

**The closed form is exact at every size.** Since $\binom{2n}{n}\sim4^n/\sqrt{\pi n}$, **the growth is exponential with base 4** — multiplying by about 14 for every $+2$ in $n$. *(The central binomial coefficient is [[Discrete Mathematics/contents/06 - Counting Methods and the Pigeonhole Principle|DM ch. 06]]'s; it counts the monotone lattice paths through the table, which is precisely what the naive recursion enumerates.)*

**Extrapolating with the verified formula** (these are too slow to run — at ~3 million calls/second):

| $n$ | naive calls | time | **table cells** |
|---|---|---|---|
| 16 | $1.2\times10^{9}$ | 401 s | **289** |
| 20 | $2.8\times10^{11}$ | 1.1 days | **441** |
| 30 | $2.4\times10^{17}$ | 2 500 years | **961** |
| 50 | $2.0\times10^{29}$ | $2.1\times10^{15}$ years | **2 601** |

> [!note] The clearest statement of what dynamic programming buys
> **At $n=50$ the table has 2 601 cells and completes instantly. The naive recursion needs longer than the age of the universe.**
>
> **The two compute the identical quantity by the identical formula.** The only difference is that one writes each answer down. **The exponential is entirely repeated work** — the naive version solves the same 2 601 subproblems about $10^{26}$ times each.
>
> *(Measured where it still terminates: at $n=12$ the table was **14 925×** faster; at $n=10$, 1 145×; at $n=8$, 137×. The speed-up itself grows exponentially.)*

**This is [[03 - Recursion|ch. 03]]'s Fibonacci memoisation over a two-dimensional subproblem space** — there the naive version was $\varphi^n$, here $4^n$, and in both cases a table of memory collapses it to polynomial.

### 6. Huffman coding — greedy, and provably near-optimal

> [!note] The greedy method
> Build a solution by repeatedly taking the choice that looks best *right now*, never reconsidering. **Greedy is fast and usually wrong** — but for some problems it is provably optimal, and Huffman coding is the classic case.

**The idea:** frequent characters should get short codes. **The algorithm:** treat each character as a node weighted by its frequency; **repeatedly merge the two lightest nodes** (a [[08 - Priority Queues and Heaps|priority queue]], hence $O(k\log k)$ for $k$ distinct characters); the tree that results assigns each character the path to its leaf.

*(Verified on a 3 260-character text with 27 distinct characters:)*

| character | frequency | code | length |
|---|---|---|---|
| `e` | 690 | `01` | **2** |
| (space) | 600 | `111` | 3 |
| `s` | 280 | `1101` | 4 |
| `z` | 40 | `100000` | **6** |
| `g` | 40 | `110000` | 6 |

**The most frequent character gets a 2-bit code, the rarest 6 bits.** That is the whole idea, working.

**The codes are prefix-free** — no code is a prefix of another *(verified)* — which is what makes the bit stream decodable without separators: **reading left to right, the first code you recognise is the only one it could be.** This is automatic from the construction, since every character sits at a *leaf*. *(Verified by round-trip: decoding the 13 020-bit stream reproduced the original text exactly.)*

#### 6.1 How good is it? The entropy bound

| | bits |
|---|---|
| fixed-width (5 bits/char, 27 symbols) | 16 300 |
| **Huffman** | **13 020** — 79.9% |
| average code length | **3.9939 bits/char** |
| **Shannon entropy $H$** | **3.9491 bits/char** |
| **excess over $H$** | **0.0448 bits/char** |

*(All verified.)*

> [!note] A second information-theoretic bound, met
> **Shannon's entropy $H=-\sum p_i\lg p_i$ is a lower bound**: no encoding that assigns a fixed code per symbol can average fewer bits. Huffman is **provably within 1 bit per symbol** of it, and **here it is within 0.045 bits — 1.1% above the theoretical floor.**
>
> **This is [[11 - Sorting and Selection|ch. 11]] §4 in another domain.** There, merge-sort came within 2% of $\lg(n!)$; here Huffman comes within 1.1% of $H$. **In both cases the bound counts information, not operations**, and in both the algorithm is essentially unimprovable.
>
> **The 79.9% compression looks unimpressive** because this text is nearly uniform ($H=3.95$ against a 4.75-bit maximum). **Huffman's gain comes entirely from *skew* in the frequencies** — on English text with its dominant `e` and spaces it does far better, and on uniformly random data it cannot help at all. *(That is why real compressors combine it with modelling — the `DEFLATE` used by `gzip` and PNG is LZ77 followed by Huffman.)*

### 7. Tries — indexing by prefix

> [!note] Definition
> A **trie** (prefix tree) stores strings by *sharing their common prefixes*: each edge is a character, each root-to-node path spells a prefix, and nodes are marked when a stored word ends there.

**Lookup costs $O(\text{length of the key})$ — independent of how many keys are stored.** A million words or ten, `"cat"` takes three steps.

*(Verified, with `cat, car, card, care, careful, cart, dog, do, done` inserted:)*

```
autocomplete "car"  ->  ['car', 'card', 'care', 'careful', 'cart']
autocomplete "do"   ->  ['do', 'dog', 'done']
autocomplete "z"    ->  []
"ca" in trie        ->  False   (a prefix is not a word unless marked)
```

**The `"ca"` case is the one to notice.** `ca` is a path in the trie but not a stored word, so the `'$'` end-marker is what distinguishes "prefix of something" from "actually present". **Omitting that marker is the standard trie bug** — every prefix would report as a member.

**And the operation a hash table simply cannot do:**

| 40 000 words, 300 prefix queries | time |
|---|---|
| scanning the word list | 0.8640 s |
| **trie** | **0.0180 s — 48× faster** |

*(Verified.)* **The scan is $O(\text{vocabulary})$ per query; the trie is $O(\text{prefix}+\text{matches})$** — it never touches words outside the subtree. **Widen the vocabulary tenfold and the scan gets ten times slower while the trie does not change.**

> [!note] This is the [[09 - Maps, Hash Tables and Skip Lists|ch. 09]] argument again
> A hash table answers *"is `car` present?"* in $O(1)$ but **cannot answer *"every word beginning with `car`"* at all**, because hashing deliberately destroys the relationship between similar keys — `car` and `card` land in unrelated buckets.
>
> **Ch. 09 solved this with sorted structures; a trie solves it by making the prefix *be* the path.** Tries also share storage between common prefixes, which is why they underpin autocomplete, spell-checkers, IP routing tables and dictionary compression.
>
> **The cost is memory** — a node per character per distinct prefix, with a child map each. **Compressed (Patricia) tries** collapse chains of single-child nodes into one edge labelled with a whole substring, which is what makes them practical at scale.

### 8. The chapter in one table

| | complexity | mechanism |
|---|---|---|
| brute-force matching | $O(nm)$ | re-reads the text after each mismatch |
| **Boyer–Moore** | $O(nm)$ worst, **sublinear typical** | skips ahead using the last-occurrence table |
| **KMP** | $O(n+m)$ **always** | failure function; the text index never retreats |
| naive LCS | $2\binom{2n}{n}-1\approx4^n$ | recomputes subproblems |
| **LCS by DP** | $O(nm)$ | each cell computed once |
| **Huffman** | $O(k\log k)$ | greedy merging; within 1 bit/symbol of entropy |
| **trie lookup** | $O(\lvert\text{key}\rvert)$ | independent of the number of keys stored |

## ✏️ Exercises

**1. (Pattern matching.)** (a) What exactly does brute force waste? (b) Explain Boyer–Moore's two ideas. (c) Define the failure function and compute it for `abacab`. (d) Why is KMP $O(n+m)$?

> [!example]- Solution
> **(a) It discards information it has already paid for.** On a mismatch at $P[k]$ from alignment $i$, it has learned that $T[i..i+k-1]$ equals $P[0..k-1]$ — a genuine fact about the text. **It then restarts at $i+1$ and re-reads those characters**, re-deriving what it knew.
>
> **That is the source of the $O(nm)$**: $n$ alignments, up to $m$ re-read characters each. *(Measured at 790 100 comparisons for $n=8\,000$, $m=100$ — close to $nm=800\,000$.)*
>
> **KMP's insight is that the discarded information determines exactly how far to shift**, and it depends only on the *pattern*, so it can be precomputed once.
>
> **(b) Compare right-to-left, and jump on a mismatch.**
>
> **Backwards comparison** seems perverse but is what enables skipping: a mismatch at the pattern's *end* refutes the alignment just as conclusively as one at the start, while telling you about a character $m-1$ positions further along the text.
>
> **The character-jump heuristic:** on a mismatch against text character $c$, consult a precomputed table of each character's **last occurrence** in the pattern. If $c$ does not occur in $P$ at all, **no alignment covering this position can match, so shift the entire pattern past it** — a jump of $m$. If $c$ occurs, shift to line that occurrence up.
>
> **Together these make Boyer–Moore sublinear** — *(measured: 279 comparisons over 8 000 characters, touching 3.5% of the text)*. **No left-to-right algorithm can skip characters**, because it cannot know what it has not examined.
>
> **(c) $f(k)$ is the length of the longest proper prefix of $P[0..k]$ that is also a suffix of it.** ("Proper" excludes the whole string, or $f$ would trivially be $k+1$.)
>
> For `abacab`:
>
> | $k$ | $P[0..k]$ | longest prefix = suffix | $f(k)$ |
> |---|---|---|---|
> | 0 | `a` | — (proper prefixes: none) | 0 |
> | 1 | `ab` | — (`a`≠`b`) | 0 |
> | 2 | `aba` | `a` | **1** |
> | 3 | `abac` | — | 0 |
> | 4 | `abaca` | `a` | **1** |
> | 5 | `abacab` | `ab` | **2** |
>
> *(Verified: `0 0 1 0 1 2`.)*
>
> **What it means operationally:** on a mismatch after matching $k$ characters, the last $f(k-1)$ characters just read are also a *prefix* of the pattern. **So those characters need not be re-examined** — shift the pattern to align that prefix and continue from the same text position.
>
> **(d) Because the text index never decreases.**
>
> Consider the loop variables $j$ (text) and $k$ (pattern). Each iteration does one of:
> - **match:** $j{+}{+}$, $k{+}{+}$;
> - **mismatch with $k>0$:** $k\leftarrow f(k-1)$, which **strictly decreases $k$** and leaves $j$ alone;
> - **mismatch with $k=0$:** $j{+}{+}$.
>
> **$j$ increases at most $n$ times and never decreases.** $k$ increases only when $j$ does, so $k$ increases at most $n$ times in total; since each decreasing step drops $k$ by at least 1 and $k\ge0$, **there can be at most $n$ decreasing steps too.** So the loop runs $O(n)$ times.
>
> **The failure function costs $O(m)$** by the identical argument applied to the pattern against itself — it is the same loop, bootstrapping on values already computed.
>
> **Total $O(n+m)$, worst case, on every input.** *(Verified: 8 099–16 098 comparisons for $n=8\,000$ across all four test inputs, including both adversarial ones.)*

**2. (Comparing the three — and a correction.)** (a) Interpret the four-row table. (b) I claimed row 1 was Boyer–Moore's worst case; what was wrong? (c) Why are KMP and brute force nearly identical on real text? (d) Which would you use?

> [!example]- Solution
> **(a)** *(comparisons, $n=8\,000$, $m=100$; the linear baseline is 8 000)*
>
> | input | brute | BM | KMP |
> |---|---|---|---|
> | $T=a^n$, $P=a^{m-1}b$ | **790 100** | 7 901 | 16 098 |
> | $T=a^n$, $P=b\cdot a^{m-1}$ | 7 901 | **790 100** | 8 099 |
> | random binary | 15 793 | 11 916 | 10 831 |
> | random 26-letter | 8 211 | **279** | 8 406 |
>
> **Rows 1 and 2 are mirror images, and that is the whole story.** Row 1 defeats brute force: every alignment matches $m-1$ characters left-to-right before failing on the last. Row 2 defeats Boyer–Moore by the identical trick *reversed*: comparing right-to-left, BM matches $m-1$ characters before failing on the first, and shifts only 1 each time.
>
> **Both bad cases produce exactly 790 100 comparisons — the same $\approx nm$**, from the same structure viewed from opposite ends.
>
> **Row 4 shows BM's best case: 279 comparisons on 8 000 characters, 3.5% of the text** — a large alphabet means most mismatched characters are absent from the pattern, so most jumps are the full $m$.
>
> **KMP spans only 8 099 to 16 098 across all four rows** — at worst about $2n$, never $nm$. **It has no adversary here.**
>
> **(b) I assumed an input bad for one algorithm is bad for all — and asserted it in the face of my own contradicting data.** The table printed BM at 7 901 comparisons, the *fewest* in that row, while my conclusion called it degenerate.
>
> **The substantive error:** in row 1, BM compares $T[i]$ against $P[m-1]=$`b`, mismatches immediately (the text is all `a`), then shifts. It does **one comparison per alignment** — about $n$ in total, i.e. linear. **It never enters the long backwards match that would make it slow**, because the failing character is the first one it looks at.
>
> **Constructing the true adversary required reversing the pattern** to $b\cdot a^{m-1}$, so that BM matches the $m-1$ trailing `a`s before failing on the leading `b`.
>
> **The transferable lesson: "worst case" is a property of an algorithm–input pair, never of an input alone.** A benchmark cannot rank algorithms unless each one's own adversary is included — and this is why [[11 - Sorting and Selection|ch. 11]] tested sorted input specifically, and [[08 - Priority Queues and Heaps|ch. 08]] had to *construct* descending input to reveal heapify's advantage.
>
> **(c) Because on a large alphabet, mismatches almost always occur on the first character compared.**
>
> With 26 letters, two random characters agree with probability $1/26$. **So a typical alignment fails immediately, brute force re-reads nothing, and there is nothing for KMP's failure function to save.** *(Measured on 200 000 characters: brute 207 634 comparisons, KMP 207 366 — a 0.1% difference, and KMP was only marginally faster in time.)*
>
> **KMP's guarantee is about the worst case, not the average.** It prevents catastrophe; it does not deliver everyday speed. **Boyer–Moore is the opposite** — its jumping is an average-case mechanism that fires constantly on large alphabets *(7.6× faster in the same test)*, while its worst case is as bad as brute force's.
>
> **This distinction — improving the worst case versus improving the typical case — is the practical heart of the chapter**, and the two goals are met by different algorithms.
>
> **(d)**
> - **Real text, large alphabet, benign input → Boyer–Moore** (or a hybrid). This is what `grep` uses.
> - **Small alphabet (DNA, binary), or highly repetitive text → KMP.** BM's skipping fails when most characters are in the pattern.
> - **Adversarial or untrusted input → KMP**, for the same reason [[11 - Sorting and Selection|ch. 11]] demands a randomised pivot: a guarantee, not an expectation.
> - **Streaming input → KMP**, uniquely: it never moves backwards, so the text need not be stored.
> - **In Python → `str.find` or the `re` module.** They are C hybrids and beat all three of these implementations regardless of asymptotics ([[11 - Sorting and Selection|ch. 11]] §8's 14× constant).

**3. (Hard — dynamic programming.)** (a) State the two conditions and explain why divide-and-conquer is not DP. (b) Derive the LCS recurrence. (c) The naive count is exactly $2\binom{2n}{n}-1$ — explain, and interpret the extrapolation. (d) How is this ch. 03's Fibonacci?

> [!example]- Solution
> **(a) Optimal substructure and overlapping subproblems.**
>
> **Optimal substructure:** an optimal solution contains optimal solutions to subproblems, so they can be combined without reconsidering. **Overlapping subproblems:** the same subproblems arise repeatedly across the recursion.
>
> **Divide-and-conquer has the first but not the second, and that is exactly why it is not dynamic programming.** Merge-sort ([[11 - Sorting and Selection|ch. 11]]) splits into *disjoint* halves — the left half's subproblems never coincide with the right's, so **nothing is ever recomputed and a table would store $n$ entries each read once.** There is no waste to eliminate.
>
> **LCS is different because its subproblems form a grid**, and $(i,j)$ is reachable from both $(i+1,j)$ and $(i,j+1)$. **The subproblem space is $O(nm)$ but the recursion tree is exponential**, so the same cells are revisited astronomically often. **That gap between tree size and space size is precisely what DP recovers.**
>
> **Diagnostic:** if the recursion's subproblems are indexed by a small number of bounded parameters, the space is polynomial and DP will pay.
>
> **(b)** Let $L[i][j]$ be the LCS length of $X[0..i-1]$ and $Y[0..j-1]$, and consider the last characters.
>
> - **Either string empty:** $L=0$.
> - **$X_i=Y_j$:** this character can be taken as the last of the LCS. **It is always safe to take it** — any LCS not using it can be modified to use it without shortening. So $L[i][j]=L[i-1][j-1]+1$.
> - **$X_i\ne Y_j$:** they cannot both be the LCS's last character, so at least one is unused. Drop one and take the better: $L[i][j]=\max(L[i-1][j],\;L[i][j-1])$.
>
> **The middle case is the one worth pausing on** — it is a greedy step inside a DP, and it needs the exchange argument above to be valid. Without it you would have to consider *not* taking a matching character, doubling the branching.
>
> **The table is filled in increasing $i,j$ so each cell's dependencies are ready.** $(n+1)(m+1)$ cells, $O(1)$ each, **$O(nm)$** *(verified: ratios 4.15, 4.32, 3.99 on doubling)*. **Reconstruction walks backwards** from $L[n][m]$, moving diagonally on a match and otherwise toward the larger neighbour. *(Verified: `GTTCCTAATA` / `CGATAATTGAGA` → length 6, `GTTTAA`, confirmed a subsequence of both.)*
>
> **(c)** With **no characters in common**, every comparison mismatches, so every call spawns two:
> $$T(i,j)=T(i-1,j)+T(i,j-1)+1,\qquad T(0,j)=T(i,0)=1.$$
>
> **This is Pascal's recurrence plus a constant**, and its solution at $(n,n)$ is $2\binom{2n}{n}-1$. *(Verified **exactly** — not asymptotically — at $n=2,4,6,8,10,12$: 11, 139, 1 847, 25 739, 369 511, 5 408 311.)*
>
> **$\binom{2n}{n}$ counts monotone lattice paths from $(0,0)$ to $(n,n)$** ([[Discrete Mathematics/contents/06 - Counting Methods and the Pigeonhole Principle|DM ch. 06]]) — and that is literally what the naive recursion enumerates: **every distinct route through the table, each rediscovering the same cells.**
>
> Since $\binom{2n}{n}\sim4^n/\sqrt{\pi n}$, **growth is exponential with base 4** — the measured ratios climb toward 16 per $+2$ in $n$ (12.6, 13.3, 13.9, 14.4, 14.6, approaching $4^2=16$ as the $\sqrt{\pi n}$ correction thins).
>
> **The extrapolation:**
>
> | $n$ | naive | table cells |
> |---|---|---|
> | 20 | 1.1 days | **441** |
> | 30 | 2 500 years | **961** |
> | 50 | $2\times10^{15}$ years | **2 601** |
>
> **At $n=50$ the table is 2 601 cells — instant — and the naive version needs 100 000 times the age of the universe.** Both compute the same number by the same formula. **The entire difference is writing answers down**, and the naive version solves those 2 601 subproblems roughly $10^{26}$ times each.
>
> *(Measured where feasible: 137×, 1 145×, **14 925×** at $n=8,10,12$ — the speed-up itself grows exponentially.)*
>
> **(d) It is the same phenomenon in two dimensions instead of one.**
>
> [[03 - Recursion|Ch. 03]] measured naive Fibonacci growing as $\varphi^n$ — predicted ratio $\varphi^2=2.618$ per two steps, **measured 2.51 / 2.55 / 2.70** — because `fib(n-2)` is recomputed inside `fib(n-1)`. Memoising collapsed it to $O(n)$.
>
> **The structure is identical:**
>
> | | ch. 03 Fibonacci | LCS |
> |---|---|---|
> | subproblem space | $n$ (1-D) | $nm$ (2-D) |
> | naive cost | $\varphi^n\approx1.62^n$ | $4^n$ |
> | memoised cost | $O(n)$ | $O(nm)$ |
> | why exponential | two recursive calls, overlapping | two recursive calls, overlapping |
>
> **Both are "small subproblem space, exponential recursion tree", and in both the fix is a table.** The base differs ($\varphi$ versus 4) only because Fibonacci's two calls are on sizes $n-1,n-2$ while LCS's are on $(i-1,j),(i,j-1)$.
>
> **So "dynamic programming" and "memoisation" are the same idea approached from opposite ends** — bottom-up filling versus top-down caching. **Bottom-up avoids recursion overhead and stack limits; top-down computes only the cells actually needed.** Neither is universally better.

**4. (Huffman and the greedy method.)** (a) What is greedy, and why is Huffman a good example? (b) What is the prefix-free property and why is it automatic? (c) Interpret the entropy comparison. (d) Why only 79.9% compression, and when does Huffman fail?

> [!example]- Solution
> **(a) Greedy means taking the locally best choice at each step and never reconsidering it.**
>
> **Greedy is usually wrong** — a locally optimal choice often forecloses a better global solution — which is why most optimisation needs DP or search. **Huffman is one of the cases where greedy is provably optimal.**
>
> **The algorithm:** each distinct character becomes a node weighted by its frequency; **repeatedly remove the two lightest nodes and merge them** under a new node of combined weight; the final tree's root-to-leaf paths are the codes. The repeated "two lightest" is a [[08 - Priority Queues and Heaps|priority queue]], giving $O(k\log k)$.
>
> **Why greedy works here** (sketch): in *some* optimal tree, the two least frequent characters are siblings at maximum depth — if not, swapping them with whatever is down there does not increase the total, since they are the least frequent. **So merging them first is safe**, and induction on the reduced problem completes the argument. **This exchange argument is the standard way to prove a greedy algorithm correct**, and it is the same shape as Exercise 3(b)'s justification for always taking a matching character.
>
> **(b) No code is a prefix of another** *(verified across all 27 codes)*.
>
> **Why it matters:** the encoded stream is bits with no separators. Reading left to right, **as soon as the bits accumulated form a valid code, that must be the intended symbol** — no other code could be extending it. Without this the stream would be ambiguous: if `a`=`0` and `b`=`01`, then `01` could be `b` or `a` followed by something.
>
> **Why it is automatic:** every character sits at a **leaf**. A code is a prefix of another exactly when its node lies on the path to the other's — i.e. when it is an internal node. **Since Huffman only ever merges nodes under new parents, original characters can only be leaves.** *(Verified by round-trip: the 13 020-bit stream decoded back to the original text exactly.)*
>
> **(c)**
>
> | | bits/char |
> |---|---|
> | fixed-width | 5.0000 |
> | **Huffman** | **3.9939** |
> | **Shannon entropy $H$** | **3.9491** |
> | excess | **0.0448** |
>
> **$H=-\sum p_i\lg p_i$ is the information-theoretic floor**: no code assigning a fixed bit-string per symbol can average fewer bits. **Huffman is guaranteed within 1 bit/symbol; here it is within 0.045 — just 1.1% above the floor.**
>
> **The excess is non-zero because code lengths must be whole numbers.** A symbol of probability $0.3$ ideally deserves $\lg(1/0.3)=1.74$ bits; Huffman must give it 1 or 2. **That rounding is the entire gap**, and it is why *arithmetic coding*, which is not restricted to integer lengths, can beat Huffman and approach $H$ arbitrarily closely.
>
> **This is [[11 - Sorting and Selection|ch. 11]] §4 in a new domain.** There, merge-sort came within 2% of $\lg(n!)$; here Huffman comes within 1.1% of $H$. **Both bounds count *information* rather than operations, and both are proved by the same style of argument** — you cannot distinguish $N$ possibilities with fewer than $\lg N$ bits. **When an algorithm meets such a bound, the problem is closed**: further effort must change the model (as [[11 - Sorting and Selection|ch. 11]]'s radix-sort did), not the algorithm.
>
> **(d) Because this text's frequencies are nearly uniform.**
>
> With 27 symbols the maximum entropy is $\lg 27=4.75$ bits, and this text's is **3.95** — only 17% below. **Huffman's saving comes entirely from skew, and there is little here to exploit.** It cannot beat $H$, so 79.9% is close to the best available.
>
> **Huffman fails or barely helps when:**
> 1. **Frequencies are near-uniform** — as here, and completely on random data, where $H$ equals the fixed-width size and compression is impossible. **No algorithm compresses random data** (a counting argument: there are not enough short strings).
> 2. **The redundancy is in *structure*, not symbol frequency.** `abababab…` has uniform character frequencies, so Huffman gains nothing — while the string is obviously compressible. **Huffman is blind to correlation between adjacent symbols.**
> 3. **The alphabet is large relative to the text** — the code table itself must be transmitted.
>
> **Hence real compressors model first, then Huffman.** `DEFLATE` (gzip, PNG, zip) runs **LZ77** — replacing repeated substrings with back-references, which captures structural redundancy — **and then Huffman-codes the result**. Each handles what the other cannot.

**5. (Hard — tries.)** (a) Why is lookup independent of the number of keys? (b) Interpret the benchmark. (c) Why can a hash table not do this, and how did ch. 09 answer? (d) What do tries cost, and how is that mitigated?

> [!example]- Solution
> **(a) Because the search is directed by the key itself, not by comparison with stored keys.**
>
> At depth $d$ the algorithm looks up character $d$ of the query among the current node's children — an $O(1)$ dictionary access — and descends. **After $\lvert\text{key}\rvert$ steps it has arrived or failed.** The number of stored words never enters: they are *branches not taken*, never examined.
>
> **Contrast the alternatives.** A sorted list needs $O(\log n)$ comparisons **each costing up to $\lvert\text{key}\rvert$ character comparisons** — so $O(\lvert\text{key}\rvert\log n)$. A balanced tree ([[10 - Search Trees|ch. 10]]) is the same. **A trie removes the $\log n$ entirely.**
>
> **The `'$'` end-marker is essential**: `ca` is a path in the trie but not a stored word. *(Verified: `"ca" in trie` is `False` while `"car"` is `True`.)* **Omitting the marker makes every prefix report as a member** — the standard trie bug, and it produces confidently wrong answers rather than crashes.
>
> **(b)**
>
> | 40 000 words, 300 prefix queries | time |
> |---|---|
> | list scan | 0.8640 s |
> | **trie** | **0.0180 s (48×)** |
>
> **The scan is $O(V)$ per query** — it tests all 40 000 words, most failing on the first character. **The trie is $O(\lvert\text{prefix}\rvert+\lvert\text{output}\rvert)$**: three steps to the subtree, then enumerate only what is inside.
>
> **The important property is not the 48× but its dependence on $V$.** Ten times the vocabulary makes the scan ten times slower and **leaves the trie unchanged**, since the subtree under `car` does not grow when unrelated words are added. **A constant-factor gap would hold steady; this one widens** — the [[02 - Algorithm Analysis in Practice|ch. 02]] diagnostic for differing complexity classes.
>
> **(c) Because hashing deliberately destroys the relationship between similar keys.** A hash function spreads keys as randomly as possible — that is what prevents clustering ([[09 - Maps, Hash Tables and Skip Lists|ch. 09]] §2). **So `car` and `card` land in unrelated buckets**, and there is no way to enumerate a prefix's members short of scanning the whole table.
>
> **The same limitation as [[09 - Maps, Hash Tables and Skip Lists|ch. 09]] §8's ordered queries, from the same cause** — and it is structural, not an implementation gap.
>
> **Ch. 09 and ch. 10 answered with order** — skip lists and balanced trees keep keys sorted, so a prefix range is contiguous. **A sorted structure does support prefix queries** (all strings with prefix $p$ lie between $p$ and $p$ + a high character), at $O(\lvert p\rvert\log V)$.
>
> **The trie answers differently: it makes the prefix *be the path*.** Structure replaces both hashing and ordering. **The three approaches — scatter, order, share — are the chapter-length answer to "how do you index strings?"**
>
> **(d) Memory: one node per character per distinct prefix, each with a child map.**
>
> Storing 40 000 short words creates far more nodes than 40 000 — one per distinct prefix — and **in Python each node is a `dict` with substantial overhead** ([[09 - Maps, Hash Tables and Skip Lists|ch. 09]] §6: a dict deliberately keeps a third of its table empty). **A trie can easily use more memory than the strings it stores.** The waste is worst at the leaves, where long unbranching tails of single-child nodes each carry a full node's overhead.
>
> **Mitigations, in increasing order of sophistication:**
> 1. **Compressed (Patricia/radix) tries** — collapse each chain of single-child nodes into one edge labelled with a whole substring. **This removes the dominant waste**, since most deep nodes have one child, and is what makes tries practical. Goodrich covers this as the *compressed trie*.
> 2. **Array children instead of dicts** when the alphabet is small and fixed (DNA's 4 symbols, or 26 letters) — trading a fixed-size array for the dict's overhead.
> 3. **A DAWG** (directed acyclic word graph) — share common *suffixes* as well as prefixes by merging identical subtrees. Much smaller, but no longer supports easy insertion.
> 4. **Suffix tries/trees** — build a trie of *all suffixes* of a text, so any substring query becomes a root descent. $O(n)$ construction exists (Ukkonen's), and this is the foundation of bioinformatics search.
>
> **Where tries earn their memory:** autocomplete and search suggestion, spell-checking with edit distance (a trie prunes the search space enormously), **IP routing tables** (longest-prefix match is exactly a trie descent), and dictionary compression, where prefix sharing *saves* space rather than costing it.

## 📝 Summary

- **Every algorithm here is about not redoing work** — matching, DP, coding and tries are four answers to that one question.
- **Brute-force matching is $O(nm)$ because it re-reads text after a mismatch**, discarding information it already paid for.
- **Boyer–Moore compares right-to-left and jumps** using a last-occurrence table, so it can be **sublinear** — *(measured 279 comparisons over 8 000 characters, touching 3.5% of the text)*. No left-to-right algorithm can skip.
- **KMP's failure function** $f(k)$ = longest proper prefix that is also a suffix *(verified `0 0 1 0 1 2` for `abacab`)*. **The text index never retreats**, giving $O(n+m)$ **on every input**.
- **Each algorithm has its own adversary, and they are mirror images:** $P=a^{m-1}b$ costs brute force 790 100 comparisons and BM only 7 901; $P=b\cdot a^{m-1}$ reverses it exactly. **KMP stayed between 8 099 and 16 098 in all four tests.**
- **On real text KMP and brute force are within 0.1%** — on a large alphabet mismatches happen immediately, so KMP's machinery never engages. **KMP buys a worst-case guarantee; Boyer–Moore buys average-case speed** *(7.6× faster in the same test)*.
- **Dynamic programming needs optimal substructure *and* overlapping subproblems.** Divide-and-conquer has only the first, which is why merge-sort needs no table.
- **LCS: $L[i][j]=L[i-1][j-1]+1$ on a match, else $\max$ of the neighbours** — $O(nm)$ *(measured ratios 4.15, 4.32, 3.99)*, with the sequence recovered by walking the table backwards.
- **The naive recursion makes exactly $2\binom{2n}{n}-1$ calls** *(verified exactly at six sizes)* $\approx4^n$ — it enumerates every lattice path through the table ([[Discrete Mathematics/contents/06 - Counting Methods and the Pigeonhole Principle|DM ch. 06]]).
- **At $n=50$: 2 601 table cells and instant, versus $2\times10^{29}$ calls and $10^{15}$ years.** Identical formula; the only difference is writing answers down. **This is [[03 - Recursion|ch. 03]]'s Fibonacci memoisation in two dimensions.**
- **Huffman coding is greedy and provably near-optimal** — merge the two lightest nodes repeatedly ($O(k\log k)$ with a heap). Frequent characters get short codes *(`e`→2 bits, rare letters→6)*.
- **Codes are prefix-free automatically**, because characters occupy only leaves — which is what makes the bit stream decodable without separators *(verified by round-trip)*.
- **Huffman came within 0.045 bits/char of the Shannon entropy** (3.9939 vs 3.9491) — **1.1% above the information-theoretic floor**, mirroring [[11 - Sorting and Selection|ch. 11]]'s merge-sort within 2% of $\lg(n!)$. **The residue is integer rounding of code lengths.**
- **Compression was only 79.9% because the text is nearly uniform.** Huffman exploits frequency skew alone and is blind to structure — hence real compressors (`DEFLATE`) run LZ77 first.
- **A trie makes the prefix *be* the path**, so lookup is $O(\lvert\text{key}\rvert)$, **independent of how many keys are stored** *(measured 48× faster than scanning 40 000 words, a gap that widens with vocabulary)*.
- **Hash tables cannot do prefix queries at all** — hashing destroys the relation between `car` and `card` by design. **Scatter, order, share are the three answers to indexing strings.**

## ⚠️ Important Notes

1. **"Worst case" is a property of an algorithm–input pair, never of an input alone.** The input that breaks brute force is Boyer–Moore's *best* case. **A benchmark cannot rank algorithms unless each one's own adversary is included.**
2. **Never assert a conclusion your own data contradicts.** I wrote that BM degenerated on an input where the table above showed it winning. **Read the numbers before writing the sentence.**
3. **KMP's benefit is a guarantee, not everyday speed** — on real text it matched brute force to within 0.1%. Use it for small alphabets, repetitive text, adversarial input, or streaming.
4. **KMP is the only one of the three that never moves backwards in the text**, so it alone works on a stream that cannot be re-read.
5. **Boyer–Moore's skipping collapses when the alphabet is small** — with 2–4 symbols nearly every mismatched character occurs in the pattern, so jumps are short. **Do not use BM on DNA or binary.**
6. **In Python, use `str.find` or `re`.** They are C hybrids and beat any of these implementations regardless of asymptotics.
7. **DP requires *overlapping* subproblems.** Without overlap a table just stores each answer for one read — divide-and-conquer, not DP.
8. **Test whether the subproblem space is polynomial**: if subproblems are indexed by a few bounded parameters, DP will pay, often enormously.
9. **The exponential in naive recursion is entirely repeated work.** At $n=50$ the naive LCS solves 2 601 distinct subproblems about $10^{26}$ times each.
10. **Bottom-up DP and top-down memoisation are the same idea.** Bottom-up avoids recursion overhead and stack limits; top-down computes only the cells actually needed. Neither always wins.
11. **A DP table gives the *value*; recovering the *solution* needs a backward walk** (or stored choices). Forgetting this is the most common DP mistake — the table alone does not tell you the LCS.
12. **Greedy is usually wrong.** Huffman is optimal only because an exchange argument proves it; **do not assume a greedy algorithm is correct without one.**
13. **Huffman is blind to structure.** `abababab…` has uniform frequencies and compresses to nothing under Huffman while being obviously redundant. **Model first, then code** — that is what `DEFLATE` does.
14. **No algorithm compresses random data.** If the entropy equals the fixed-width size, there is nothing to remove — a counting argument, not a limitation of Huffman.
15. **When an algorithm meets an information-theoretic bound, the problem is closed.** Further progress must change the model (arithmetic coding's fractional lengths, radix-sort's non-comparison), not the algorithm.
16. **A trie needs an explicit end-of-word marker.** Without it every prefix reports as a stored word — a bug that yields confident wrong answers rather than errors.
17. **Tries can use more memory than the strings they store**, especially in Python where each node is a `dict`. **Compress single-child chains** (Patricia trie) — that is what makes them practical.
18. **Reach for a trie when the query is about prefixes**: autocomplete, spell-check, longest-prefix IP routing. For plain membership, a `set` is smaller and faster.

> [!warning] Gaps in the source material
> **Goodrich's ch. 13 prose extracts well** — the brute-force analysis, Boyer–Moore's character-jump heuristic, the KMP failure function and Proposition 13.3, the LCS recurrence, Huffman coding and the greedy method, and the trie sections all came through readably. **Goodrich page $n$ = PDF page $n+22$; ch. 13 is PDF 604–634.**
>
> **His code did not**, per the standing problem in `00-Index.md`, and **Lambert's coverage ran out at ch. 08.** So **every implementation here is my own**: `find_brute`, `find_boyer_moore`, `find_kmp` with `compute_kmp_fail`, `lcs_naive`, `lcs_table` with reconstruction, `huffman_codes`, and the `Trie`. **All were executed.** The three matchers were checked against `str.find()` on ten hand-picked cases **and 3 000 random pairs over $\{a,b\}$ — zero failures**; the LCS was verified to be a genuine subsequence of both inputs with length matching the table; the Huffman codes were verified **prefix-free and round-trip decodable**; the trie was checked for the prefix-is-not-a-word case.
>
> **All measurements are my own**: the four-scenario comparison table, the 200 000-character text search, the exact naive-LCS call counts against $2\binom{2n}{n}-1$, the DP table scaling, the entropy comparison, and the trie-versus-scan benchmark.
>
> **All figures are images and are lost** — Fig. 13.2–13.4 (the Boyer–Moore intuition, the jump rules, and the worked execution trace), Fig. 13.5 (the KMP motivating example), the DP table illustrations, the Huffman tree diagrams, and every trie picture. **This chapter is unusually diagram-dependent**: Huffman trees and tries are almost always taught by drawing them. **Substitutes: the printed DP table in §4, the code-length table in §6, and the trie's actual autocomplete output in §7** — showing the real structure's behaviour rather than a static picture. **The reader should draw the Huffman tree and the `car`/`card`/`care` trie by hand.**
>
> **No error was found in Goodrich ch. 13.**
>
> **Two corrections to my own work are recorded in place** rather than silently fixed, because the mistakes are instructive: **§3.1**, where I asserted Boyer–Moore degenerated on an input my own table showed it winning (the real BM adversary is the mirror image), and **§5**, where my first attempt used *random* strings whose naive call counts were not even monotonic (9 055 at $n=14$ but 2 188 at $n=16$) and so demonstrated nothing — fixed by constructing the no-match worst case, which then matched a closed form exactly.
>
> **Additions beyond the source.** **§3.1's four-scenario comparison is mine** — Goodrich analyses each algorithm's worst case separately but never puts them on one input set, and **the mirror-image symmetry (790 100 comparisons for both, from opposite ends) is the clearest thing in the chapter.** **§3.2's finding that KMP and brute force are within 0.1% on real text** is mine and materially changes the practical advice. **The exact formula $2\binom{2n}{n}-1$ and its verification** are mine — Goodrich says only that naive LCS is exponential — as is **the lattice-path interpretation** linking it to [[Discrete Mathematics/contents/06 - Counting Methods and the Pigeonhole Principle|DM ch. 06]] and the extrapolation table. **§6.1's entropy comparison is entirely mine**: Goodrich presents Huffman without mentioning Shannon entropy at all, so **"within 1.1% of the information-theoretic floor" — and the parallel with [[11 - Sorting and Selection|ch. 11]]'s merge-sort result — does not appear in the source.** The account of *why* the gap is non-zero (integer code lengths, hence arithmetic coding), the LZ77/`DEFLATE` discussion, and the trie-versus-scan benchmark are additions, as are Exercise 5(d)'s four mitigations and the "scatter, order, share" framing.
>
> **Deliberately compressed.** **Goodrich's full Boyer–Moore with the good-suffix rule is not implemented** — §2 uses only the character-jump (bad-character) heuristic, which is the version Goodrich presents in detail and which demonstrates skipping; the full algorithm's second heuristic is mentioned but **its improved bound is not verified here.** **Compressed and suffix tries (§13.5.2–13.5.3) are described in Exercise 5(d) but not implemented** — the standard trie shows the idea, and Ukkonen's $O(n)$ suffix-tree construction is well beyond the chapter. **Matrix chain multiplication** (Goodrich §13.3.1) is omitted; LCS demonstrates the same DP principles on a problem that recurs more often. **The proof that Huffman is optimal** is sketched as an exchange argument in Exercise 4(a) rather than given in full. **Text compression beyond Huffman** (LZ77, arithmetic coding) is discussed but not implemented — both are outside Goodrich's scope and are noted as additions.

**Previous:** [[11 - Sorting and Selection]] · **Next:** [[13 - Graph Algorithms]]
