---
subject: Data Structures and Algorithms
chapter: 9
tags: [ds, dsa, hash-tables, maps, dictionaries, collisions, load-factor, skip-lists, hashing]
source: "Goodrich, Tamassia & Goldwasser, *Data Structures and Algorithms in Python*, ch. 10; Lambert, *Fundamentals of Python: Data Structures*, ch. 11"
---

# Maps, Hash Tables and Skip Lists

The Python `dict` is the most-used data structure in the language, and it is a hash table. This chapter opens it up.

The central claim is remarkable: **a hash table finds a key in $O(1)$ expected time — independent of how many keys it holds.** Every other search structure so far has been $O(n)$ (linear scan) or at best $O(\log n)$ (a balanced tree). Constant time for a million keys, or a billion, is a different kind of promise.

Two things are worth watching. First, **the promise is *expected*, not worst case** — and §7 shows an adversary breaking it completely. Second, **the price is ordering**: a hash table forgets all order, so §8 covers the structure that keeps it.

[[Discrete Mathematics/contents/06 - Counting Methods and the Pigeonhole Principle|Discrete Maths ch. 06]] already proved the key limitation — **collisions are unavoidable by pigeonhole.** This chapter is about what to do about them.

## 📘 Main Knowledge

### 1. The map ADT

> [!note] Definition
> A **map** (dictionary, associative array) stores key–value pairs with **unique keys**.
>
> | Operation | Meaning |
> |---|---|
> | `M[k]` | return the value for key `k`, else `KeyError` |
> | `M[k] = v` | insert or **overwrite** |
> | `del M[k]` | remove the item |
> | `k in M` | membership test |
> | `len(M)`, `iter(M)` | queries |

**Note that `M[k] = v` on an existing key overwrites rather than inserting** — the size does not change. *(Verified: setting `m['beta'] = 99` on a 5-element map left `len` at 5.)* That is what "unique keys" means operationally, and forgetting it is a common source of off-by-one bugs in frequency counters.

**A map on an unsorted list gives $O(n)$ for every operation.** The hash table's ambition is $O(1)$.

### 2. Hash functions: hash code, then compression

Mapping a key to an array index happens in two stages.

**Stage 1 — the hash code.** An arbitrary key becomes an integer. Python's `hash()` does this:

```
hash(42)      -> 42
hash(42.0)    -> 42
hash('hello') -> -7581529729516087955
hash((1, 2))  -> -3550055125485641917
hash([1, 2])  -> TypeError: unhashable type: 'list'
```
*(Verified.)*

> [!warning] The hash contract, and why lists are unhashable
> **If `a == b` then `hash(a)` must equal `hash(b)`.** *(Verified: `hash(42) == hash(42.0)` is `True`, because `42 == 42.0`.)* Violating this breaks lookup entirely — an equal key would be sought in the wrong bucket.
>
> **The converse is not required**: unequal keys may share a hash code. That is a collision, and §3 shows it is unavoidable.
>
> **Mutable objects are unhashable by design.** If a list could be a key, mutating it after insertion would change its hash code, and the entry would be lost in a bucket the table no longer looks in — silently. **Python refuses rather than allowing that**, which is why [[01 - Python and Object-Oriented Foundations|ch. 01]] §3 noted that defining `__eq__` without `__hash__` makes instances unhashable.

**Stage 2 — compression.** The hash code must become a valid index in a table of $N$ buckets:

$$\text{index} = h(k) \bmod N$$

*(Verified: with $N=11$, `apple`, `banana`, `cherry`, `date` land in buckets 4, 5, 3, 0.)*

**A better scheme is the MAD (multiply-add-divide) method:**
$$\big[(a\cdot h(k)+b)\bmod p\big]\bmod N$$
with $p$ a prime larger than $N$, and $a,b$ chosen randomly. **The randomisation matters:** it means no fixed set of keys is systematically bad, which is the beginning of the defence against §7's attack.

> [!note] Why $N$ is usually prime
> If $N$ shares a factor with regularities in the keys, whole ranges of buckets go unused. With $N=100$ and keys that are all multiples of 10, only 10 buckets are ever hit. **A prime $N$ has no such factors**, so patterned keys still spread. *(Python's `dict` uses powers of two and compensates with a more elaborate probe sequence.)*

### 3. Collisions are guaranteed

> [!note] The pigeonhole argument, from [[Discrete Mathematics/contents/06 - Counting Methods and the Pigeonhole Principle|DM ch. 06]] §8
> A hash function maps a large (often infinite) key space into $N$ buckets. **With more than $N$ possible keys, no hash function can be injective** — by the second form of the pigeonhole principle. Collisions are not a defect of a poor hash function; they are a theorem.

*(Verified: 12 keys into 11 buckets produced buckets holding 3, 2, 2 and 2 keys.)*

**So every hash table needs a collision policy.** Two standard ones:

**Separate chaining** — each bucket holds a list of entries:

```python
    def __setitem__(self, k, v):
        j = self._hash_function(k)
        if self._table[j] is None:
            self._table[j] = []
        bucket = self._table[j]
        for i, (kk, vv) in enumerate(bucket):
            if kk == k:
                bucket[i] = (k, v)          # overwrite an existing key
                return
        bucket.append((k, v))
        self._n += 1
        if self._n > len(self._table) * 0.75:    # load factor threshold
            self._resize(2 * len(self._table) - 1)
```

**Open addressing** — one entry per bucket; on collision, probe elsewhere. With **linear probing** the sequence is $j, j+1, j+2, \dots$ (mod $N$).

| | separate chaining | open addressing |
|---|---|---|
| memory | table + a list per non-empty bucket | one array, no per-entry overhead |
| locality | poor — chains are scattered | **good** — probes are adjacent |
| load factor | may exceed 1 | **must stay below 1** |
| deletion | simple — remove from the list | **hard — needs tombstones** |
| clustering | none | linear probing forms clusters |

> [!warning] Deletion under open addressing needs a tombstone
> Simply blanking a slot breaks the probe sequence: a later key that probed *past* that slot becomes unreachable, because the search stops at the first empty bucket. **The fix is to mark the slot "deleted" rather than empty** — a tombstone, which searches skip but insertions may reuse. Forgetting this makes entries vanish, and only after unrelated deletions.

### 4. Load factor — the number that controls everything

> [!note] Definition
> The **load factor** is $\lambda = n/N$: entries divided by buckets.

Under chaining, **the average chain length *is* $\lambda$**, and a lookup scans one chain. So the expected cost is $O(1+\lambda)$ — **constant if and only if $\lambda$ is kept bounded.**

*(Verified — 100 keys in tables of varying capacity:)*

| capacity | load factor | longest chain | mean non-empty chain |
|---|---|---|---|
| 200 | 0.50 | **1** | 1.00 |
| 133 | 0.75 | **1** | 1.00 |
| 50 | 2.00 | 2 | 2.00 |
| 10 | 10.00 | **10** | 10.00 |

**Chain length tracks the load factor exactly.** At $\lambda=10$ every lookup scans ten entries — the table has degenerated toward a linear scan.

**Hence resizing.** When $\lambda$ exceeds a threshold (0.75 here; Python uses about 0.66), allocate a larger table and **rehash every entry** — the new $N$ changes every index, so entries cannot simply be copied.

**Rehashing is $O(n)$, but it is amortised $O(1)$ per insertion** by exactly [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]] §3's geometric argument — the table doubles, so the total rehashing work over $n$ insertions is $O(n)$. **The same 5 084× latency spike applies too**: a single insertion that triggers a rehash is $O(n)$.

### 5. The payoff, measured

*(Searching for the last element — the list's worst case:)*

| $n$ | `x in list` | `x in dict` | dict faster by |
|---|---|---|---|
| 10 000 | 0.0000577 s | 0.000000125 s | **462×** |
| 100 000 | 0.0006061 s | 0.000000105 s | **5 772×** |
| 1 000 000 | 0.0065361 s | 0.000000121 s | **54 018×** |

**The list's time grows tenfold with $n$; the dict's does not move at all.** *(Verified.)*

**The speed-up grows in proportion to $n$** — the signature of $O(n)$ against $O(1)$, as in [[05 - Stacks, Queues and Deques|ch. 05]] and [[06 - Linked Lists|ch. 06]]. At a million keys the dict is fifty thousand times faster, and at ten million it would be half a million times.

**This is why `x in some_set` instead of `x in some_list` is the single highest-value optimisation in everyday Python** — [[02 - Algorithm Analysis in Practice|ch. 02]] Note 5.

### 6. Python's `dict` and `set`

Both are hash tables using **open addressing** with a sophisticated probe sequence, and both are heavily optimised in C.

| Operation | Complexity |
|---|---|
| `d[k]`, `k in d`, `d[k] = v`, `del d[k]` | $O(1)$ **expected** |
| iteration | $O(n)$, **in insertion order** (guaranteed since Python 3.7) |
| worst case | $O(n)$ — §7 |

> [!note] Two things worth knowing
> **Insertion order is preserved and guaranteed.** This was an implementation detail in 3.6 and became part of the language in 3.7. **It is not sorted order** — do not confuse the two.
>
> **`dict` is memory-hungry.** A `set` or `dict` typically keeps $\lambda$ below about $\tfrac23$, so at least a third of the table is empty by design. **That waste is what buys the speed** — it is the space-for-time trade in its purest form, and it is why [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]'s advice about compact arrays for numeric data still applies.

### 7. The worst case is real — and is a security issue

Every "$O(1)$" above is **expected**, assuming keys spread across buckets. If they all collide, a chained table degenerates into one long list.

```python
class BadHash:
    __slots__ = 'v'
    def __init__(self, v): self.v = v
    def __hash__(self): return 1          # every key in one bucket
    def __eq__(self, o): return isinstance(o, BadHash) and self.v == o.v
```

*(Measured — a **fixed** 200 lookups against tables of growing size:)*

| $n$ | 200 lookups | ratio |
|---|---|---|
| 1 000 | 0.0070 s | — |
| 2 000 | 0.0138 s | **1.96** |
| 4 000 | 0.0305 s | **2.21** |

**The lookup count is constant while the time doubles with $n$ — so each individual lookup is $O(n)$.** The hash table has become a linked list. *(Verified.)*

> [!warning] This is exploitable, and it has been exploited
> A server that builds a dict from user-supplied keys — HTTP form fields, JSON keys, query parameters — can be attacked by sending thousands of keys engineered to collide. Every insertion becomes $O(n)$, the request takes $O(n^2)$, and a few hundred kilobytes of input consumes minutes of CPU. **This is a *hash-flooding* denial-of-service attack**, and it was demonstrated against most major languages in 2011.
>
> **The defence is randomisation.** Python since 3.3 seeds string hashing with a random value per process (`PYTHONHASHSEED`), so an attacker cannot predict which keys collide. Note this is why **`hash('abc')` differs between runs** while `hash(42)` does not — a surprise if you ever tried to persist a hash value.
>
> **Two engineering lessons.** Never persist or transmit a hash code — it is not stable across runs or versions. And **if keys are adversarial, prefer a structure with worst-case guarantees** — a balanced tree ([[10 - Search Trees|ch. 10]]) is $O(\log n)$ *worst case*, which is slower on average and cannot be attacked this way.

### 8. Sorted maps and skip lists

A hash table destroys order, so it cannot answer *"the smallest key ≥ 50"*, *"all keys between 10 and 20"*, or *"the keys in order"*. A **sorted map** supports those, and a **skip list** is one elegant implementation.

> [!note] The idea
> A sorted linked list has $O(n)$ search — you must walk it. **Add express lanes**: level 0 holds every node, level 1 holds roughly half, level 2 a quarter, and so on. Search starts at the top level and drops down when the next node overshoots.
>
> **The level of each node is chosen randomly** — promote with probability $p=\tfrac12$ — rather than by rebalancing. That gives $O(\log n)$ **expected** search, insert and delete, with no rotation logic at all.

```python
    def search(self, key):
        x = self._head
        for i in range(self._level, -1, -1):       # top level downwards
            while x.forward[i] and x.forward[i].key < key:
                x = x.forward[i]                   # advance at this level
        x = x.forward[0]                           # drop to the bottom
        return x.value if x and x.key == key else None
```

*(Verified: inserting 3, 7, 1, 9, 5, 2 gives keys in order `[1, 2, 3, 5, 7, 9]`; `search(5)` finds it, `search(4)` returns `None`; reinserting key 5 updates the value and leaves the count at 6.)*

*(And the levels track $\lg n$ as predicted:)*

| $n$ | levels used | $\lg n$ |
|---|---|---|
| 1 000 | 11 | 9.0 |
| 4 000 | 11 | 11.0 |
| 16 000 | 15 | 13.0 |
| 64 000 | 17 | 15.0 |

**Skip lists trade a worst-case guarantee for simplicity.** A balanced tree ([[10 - Search Trees|ch. 10]]) achieves $O(\log n)$ *worst case* through explicit rebalancing; a skip list achieves it *in expectation* through randomness, in far less code. **The randomness is internal, so unlike §7's attack an adversary cannot choose inputs that make it slow** — only bad luck can, and the probability is negligible.

### 9. Choosing

| Need | Structure | Complexity |
|---|---|---|
| key → value, order irrelevant | **hash table** (`dict`) | $O(1)$ expected |
| membership only | **`set`** | $O(1)$ expected |
| keys in sorted order, range queries | balanced tree or skip list | $O(\log n)$ |
| worst-case guarantee, adversarial keys | **balanced tree** | $O(\log n)$ worst case |
| tiny collection | a list | $O(n)$, but the constant wins |

**Default to `dict`.** Reach past it only when you need ordering, range queries, or a worst-case bound.

## ✏️ Exercises

**1. (Hash functions.)** (a) State the hash contract. (b) Why are lists unhashable? (c) What are the two stages of mapping a key to a bucket? (d) Why is a prime table size preferred?

> [!example]- Solution
> **(a) If `a == b` then `hash(a) == hash(b)`.** Equal objects must produce equal hash codes. *(Verified: `hash(42) == hash(42.0)` is `True`, since `42 == 42.0`.)*
>
> **The converse is not required** — unequal keys may collide, and §3 shows they must.
>
> **Why the contract is necessary:** lookup computes the bucket from the hash code. If two equal keys hashed differently, a key inserted under one would be sought in a different bucket and never found.
>
> **(b) Because mutation would invalidate the hash code after insertion.** If a list were a key, appending to it would change its hash, so the entry would sit in a bucket the table no longer searches — **silently lost**, with no error.
>
> Python forbids it rather than permitting the corruption. **This is also why defining `__eq__` without `__hash__` makes your class unhashable** ([[01 - Python and Object-Oriented Foundations|ch. 01]] §3): if you have redefined equality, Python cannot assume the inherited identity-based hash still satisfies the contract.
>
> **(c)** **Hash code:** key → arbitrary integer (`hash()`). **Compression:** integer → an index in $[0, N)$, typically $h(k)\bmod N$, or the MAD method $[(a\cdot h(k)+b)\bmod p]\bmod N$.
>
> **The separation matters** because the two stages have different jobs: the hash code must respect equality and spread well; compression must fit the current table and be recomputed whenever the table resizes.
>
> **(d) Because a composite $N$ shares factors with patterns in the keys, wasting buckets.**
>
> With $N=100$ and keys that are all multiples of 10, $h(k)\bmod 100$ can only produce multiples of 10 — **ten of the hundred buckets carry everything.** Patterned keys are common (IDs ending in a check digit, addresses aligned to a boundary, timestamps at fixed intervals).
>
> **A prime $N$ shares no factor with such a stride**, so the keys spread. *(Python's `dict` uses powers of two instead — fast masking rather than a modulo — and compensates with a probe sequence that mixes in the high bits of the hash.)*

**2. (Collisions.)** (a) Why are collisions unavoidable? (b) Compare separate chaining and open addressing. (c) Why is deletion hard under open addressing? (d) Implement chaining and verify overwrite and deletion.

> [!example]- Solution
> **(a) By the pigeonhole principle** ([[Discrete Mathematics/contents/06 - Counting Methods and the Pigeonhole Principle|DM ch. 06]] §8, second form): a hash function maps a key space larger than $N$ into $N$ buckets, so it cannot be injective. **Some two keys must share a bucket.**
>
> *(Verified: 12 keys into 11 buckets produced buckets of size 3, 2, 2, 2 — and $12>11$ makes at least one collision certain regardless of the hash function.)*
>
> **This is a theorem, not a quality problem.** A better hash spreads keys more evenly; it cannot eliminate collisions.
>
> **(b)**
>
> | | chaining | open addressing |
> |---|---|---|
> | structure | list per bucket | one entry per bucket, probe on collision |
> | memory | table + list objects | one array — **less overhead** |
> | locality | poor (scattered lists) | **good** (adjacent probes) |
> | load factor | may exceed 1 | **must stay < 1** |
> | deletion | easy | **needs tombstones** |
> | degradation | chains lengthen gradually | **clustering** — collisions beget collisions |
>
> **Chaining is simpler and degrades more gracefully; open addressing is faster and more compact when the load factor is kept low.** Python uses open addressing.
>
> **(c) Because blanking a slot severs a probe sequence.**
>
> Suppose $k_1$ hashes to bucket 5 and $k_2$ also hashes to 5, so $k_2$ is probed into bucket 6. Now delete $k_1$ and blank bucket 5. A search for $k_2$ starts at 5, finds it **empty**, and concludes $k_2$ is absent — **stopping before reaching bucket 6.**
>
> **The fix is a tombstone**: mark the slot as *deleted* rather than *empty*. Searches treat it as occupied (keep probing); insertions may reuse it. **The cost is that tombstones accumulate and slow searches**, so a table with heavy deletion must periodically rehash to clear them.
>
> **The failure mode is nasty** — entries become invisible only after *unrelated* deletions, so the bug appears far from its cause.
>
> **(d)** §3's `ChainHashMap`. *(Verified: `len` 5 after five insertions; `m['beta'] = 99` **overwrites** leaving `len` at 5 with value 99; `del m['alpha']` reduces `len` to 4 and a subsequent lookup raises `KeyError`; iteration yields the four remaining keys.)*
>
> **The overwrite test matters** — an implementation that appends without first scanning the bucket would produce duplicate keys and a wrong `len`, and simple insert-then-read tests would not catch it.

**3. (Load factor.)** (a) Define it and relate it to chain length. (b) Interpret the measured table. (c) Why must a hash table resize, and why is rehashing unavoidable? (d) What is the amortised cost, and what is the latency consequence?

> [!example]- Solution
> **(a) $\lambda = n/N$.** Under chaining with a good hash, keys spread evenly, so **the average chain length equals $\lambda$**. A lookup hashes ($O(1)$) then scans one chain ($O(\lambda)$ expected), giving $O(1+\lambda)$.
>
> **So "hash tables are $O(1)$" is really "$O(1)$ *provided $\lambda$ is bounded*"** — which is the whole reason for resizing.
>
> **(b)** *(measured, 100 keys)*
>
> | capacity | $\lambda$ | longest chain | mean non-empty |
> |---|---|---|---|
> | 200 | 0.50 | 1 | 1.00 |
> | 133 | 0.75 | 1 | 1.00 |
> | 50 | 2.00 | 2 | 2.00 |
> | 10 | 10.00 | 10 | 10.00 |
>
> **Mean chain length equals $\lambda$ exactly**, confirming (a). At $\lambda\le0.75$ the longest chain is **1** — essentially no lookup scans more than one entry, which is what makes the constant-time claim real in practice. At $\lambda=10$ every lookup scans ten, and the structure is approaching a linear scan.
>
> **(c) To keep $\lambda$ bounded as $n$ grows.** Without resizing, $\lambda$ grows linearly with $n$ and lookups degrade to $O(n)$.
>
> **Rehashing is unavoidable because the bucket index depends on $N$.** An entry at index $h(k)\bmod 11$ belongs at $h(k)\bmod 23$ in the larger table — a different place. **Every entry must be recomputed and reinserted**; copying the array verbatim would leave every key in the wrong bucket and unfindable. *(Compare [[05 - Stacks, Queues and Deques|ch. 05]]'s circular queue, where resizing also required recomputation rather than a raw copy.)*
>
> **(d) Amortised $O(1)$ per insertion, by the geometric argument of [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]] §3.** Because the table doubles, rehashing happens at sizes $1,2,4,\dots$, and the total work is $1+2+4+\cdots<2n$ — linear overall, so constant per insertion.
>
> **The latency consequence is the same as ch. 04's**: an individual insertion that triggers a rehash is $O(n)$. Ch. 04 measured a single `append` spiking to **5 084× the mean**, and a dict insertion that rehashes a million entries is worse.
>
> **So "dict insertion is $O(1)$" is an amortised claim, and amortised bounds are about throughput, not tail latency.** In a real-time system, pre-size the dict (or use a structure with worst-case bounds) rather than letting it grow.

**4. (Measuring.)** (a) Interpret the dict-versus-list measurements. (b) Why does the speed-up grow? (c) When is a list still the better choice? (d) What does the pathological measurement show?

> [!example]- Solution
> **(a)**
>
> | $n$ | list | dict | ratio |
> |---|---|---|---|
> | 10 000 | 0.0000577 s | 0.000000125 s | 462× |
> | 100 000 | 0.0006061 s | 0.000000105 s | 5 772× |
> | 1 000 000 | 0.0065361 s | 0.000000121 s | 54 018× |
>
> **The list's time grows by roughly 10× for each 10× in $n$ — linear.** The dict's time is **flat** (0.125, 0.105, 0.121 μs — the variation is noise, not trend), confirming $O(1)$.
>
> **(b) Because the ratio of an $O(n)$ cost to an $O(1)$ cost is itself $\Theta(n)$.** A constant-factor advantage would show the same ratio at every size; a *growing* ratio means different complexity classes — the same diagnostic as [[05 - Stacks, Queues and Deques|ch. 05]] §3 and [[06 - Linked Lists|ch. 06]] §3.
>
> **(c) Three cases.**
> 1. **Very small collections.** Hashing has a real constant cost; for a handful of items a linear scan of a list can win. The crossover is typically under about ten elements.
> 2. **You need order or indexing.** A dict preserves *insertion* order but offers no positional access, no slicing, and no sorted order.
> 3. **The keys are unhashable** — lists, sets, or objects with `__eq__` and no `__hash__`.
>
> *(A fourth: memory. A dict keeps $\lambda\lesssim\tfrac23$, so a third of the table is empty by design — see §6.)*
>
> **(d) That the $O(1)$ guarantee is *expected*, not worst case, and that the worst case is genuinely linear.**
>
> With every key hashing to 1, a **fixed** 200 lookups took 0.0070 s, 0.0138 s, 0.0305 s as $n$ went 1 000 → 2 000 → 4 000 — **ratios 1.96 and 2.21.** Since the number of lookups did not change, the *per-lookup* cost doubled with $n$: each lookup is $O(n)$.
>
> **The hash table has degenerated into a linked list** — same asymptotics, more overhead.
>
> **And this is reachable by an adversary, not just by bad luck.** §7's hash-flooding attack: send a server thousands of colliding keys and its $O(1)$ dict becomes $O(n)$, turning one request into $O(n^2)$ work. **The mitigation is hash randomisation** (Python seeds string hashing per process), which is also why `hash('abc')` differs between runs — and hence why **a hash code must never be persisted or transmitted.**

**5. (Hard — ordering, and skip lists.)** (a) What can a sorted map do that a hash table cannot? (b) Explain the skip list idea. (c) Why is randomisation used instead of rebalancing? (d) Interpret the level measurements. (e) Compare hash table, skip list and balanced tree.

> [!example]- Solution
> **(a) Anything requiring order.** A hash table scatters keys deliberately, so it can only answer *"is key $k$ present?"*. A sorted map additionally supports:
> - **range queries** — all keys in $[a,b]$;
> - **nearest-key queries** — the smallest key $\ge k$ (`ceiling`), the largest $\le k$ (`floor`);
> - **min / max**;
> - **iteration in sorted order.**
>
> **These are exactly what databases need** — a `WHERE age BETWEEN 20 AND 30` cannot use a hash index, which is why [[10 - Search Trees|ch. 10]]'s B-trees are what real indexes use.
>
> *(Note Python's `dict` preserves **insertion** order, which is not sorted order and answers none of these.)*
>
> **(b) A sorted linked list with express lanes.** Level 0 contains every node; each higher level contains roughly half the nodes of the one below. A search starts at the highest level and moves forward while the next key is smaller, dropping a level when it would overshoot — so high levels skip large distances and low levels refine.
>
> **With levels halving, there are $O(\log n)$ of them and $O(1)$ steps expected per level**, giving $O(\log n)$ expected search.
>
> **(c) Because it achieves the same expected bound with far less code and no rebalancing logic.**
>
> A balanced tree maintains its invariant explicitly: AVL trees track heights and perform rotations, red–black trees recolour and rotate ([[10 - Search Trees|ch. 10]]). **That logic is intricate and is where the bugs live.** A skip list instead flips a coin per node — perhaps five lines — and gets $O(\log n)$ in expectation.
>
> **The trade is a worst-case guarantee for simplicity.** In principle every node could land at level 0, giving $O(n)$; the probability is vanishingly small.
>
> **Crucially, the randomness is internal, so the [[#7. The worst case is real — and is a security issue|§7 attack does not apply]].** An adversary choosing keys cannot influence the coin flips — unlike a hash table, where the adversary chooses the inputs to the hash. **A skip list's bad case requires bad luck; a hash table's can be manufactured.**
>
> **(d)**
>
> | $n$ | levels | $\lg n$ |
> |---|---|---|
> | 1 000 | 11 | 9.0 |
> | 4 000 | 11 | 11.0 |
> | 16 000 | 15 | 13.0 |
> | 64 000 | 17 | 15.0 |
>
> **The level count tracks $\lg n$**, growing by roughly 2 when $n$ quadruples — as expected, since the tallest of $n$ geometric($\tfrac12$) draws is about $\lg n$. **The structure discovers the right height without being told $n$**, which is the appeal of the randomised approach.
>
> *(The levels run a little above $\lg n$ because the maximum of $n$ samples exceeds the mean; per-search times grew slowly and non-monotonically — 1.15, 1.79, 1.72, 5.06 μs — consistent with logarithmic growth plus measurement noise at these very small durations.)*
>
> **(e)**
>
> | | hash table | skip list | balanced tree |
> |---|---|---|---|
> | search | **$O(1)$ expected** | $O(\log n)$ expected | $O(\log n)$ **worst case** |
> | worst case | **$O(n)$** | $O(n)$ (improbable) | **$O(\log n)$** |
> | ordered? | ✗ | ✓ | ✓ |
> | range queries | ✗ | ✓ | ✓ |
> | implementation | moderate | **simple** | complex |
> | adversary-resistant | ✗ without randomised hashing | ✓ | ✓ |
> | memory | high ($\lambda<1$ by design) | moderate | moderate |
>
> **The decision rule.** Use a **hash table** by default — it is faster and the ordering is usually not needed. Use a **balanced tree** when you need ordering *and* a worst-case guarantee, or when keys are adversarial. Use a **skip list** when you need ordering and prefer simple, easily-verified code to a strict guarantee — which is why they appear in concurrent settings, where lock-free skip lists are far easier to get right than lock-free balanced trees.

## 📝 Summary

- **A map stores unique keys.** `M[k] = v` on an existing key **overwrites** — the size does not change.
- **Hashing has two stages:** a **hash code** (key → integer) and **compression** (integer → bucket index, $h(k)\bmod N$ or the randomised MAD method).
- **The hash contract: `a == b` implies `hash(a) == hash(b)`.** The converse is not required. **Mutable objects are unhashable** because mutation after insertion would strand the entry in an unsearched bucket.
- **Collisions are guaranteed by pigeonhole** ([[Discrete Mathematics/contents/06 - Counting Methods and the Pigeonhole Principle|DM ch. 06]]) — a theorem, not a defect. **Separate chaining** (list per bucket) is simple and degrades gracefully; **open addressing** is compact and cache-friendly but **needs tombstones for deletion**.
- **The load factor $\lambda=n/N$ controls everything.** Under chaining the mean chain length **is** $\lambda$ *(verified exactly)*, so lookup is $O(1+\lambda)$ — and at $\lambda\le0.75$ the longest chain was **1**.
- **Resizing rehashes every entry**, because the index depends on $N$. **Amortised $O(1)$** by ch. 04's geometric argument — but an individual rehashing insertion is $O(n)$, so the guarantee is about throughput, not latency.
- **Measured: dict beats list by 462× → 5 772× → 54 018×** as $n$ goes 10⁴ → 10⁶. **The dict's time is flat; the list's grows linearly.** A growing ratio means different complexity classes.
- **Python's `dict` and `set` use open addressing**, preserve **insertion** order (guaranteed since 3.7 — *not* sorted order), and deliberately waste about a third of their table to keep $\lambda$ low.
- **The worst case is real: with all keys colliding, lookups became $O(n)$** *(fixed lookup count, time ratios 1.96 and 2.21 as $n$ doubled)*. **This is exploitable as hash-flooding DoS**, defended by per-process hash randomisation — which is why **hash codes must never be persisted or transmitted.**
- **A hash table cannot answer ordered queries** — ranges, nearest key, min/max, sorted iteration.
- **A skip list is a sorted linked list with randomly-chosen express lanes**, giving $O(\log n)$ **expected** with no rebalancing logic. *(Verified: levels tracked $\lg n$ — 11, 11, 15, 17 for $n=10^3$ to $6.4\times10^4$.)*
- **Its randomness is internal, so an adversary cannot provoke its worst case** — unlike a hash table's.
- **Default to `dict`;** reach for a balanced tree when you need ordering with a worst-case guarantee.

## ⚠️ Important Notes

1. **`M[k] = v` overwrites an existing key.** Check `len` in tests — an implementation that appends blindly creates duplicates and a wrong count.
2. **Never define `__eq__` without `__hash__`** if instances must be dict keys or set members. Python makes them unhashable deliberately, and the fix is to define both consistently.
3. **Never mutate an object after using it as a key.** Its hash changes and the entry becomes unreachable — silently.
4. **Never persist, transmit or compare-across-runs a hash code.** Python randomises string hashing per process, so `hash('abc')` differs between runs. Use `hashlib` for anything that must be stable.
5. **`x in some_set` instead of `x in some_list` is the highest-value one-line optimisation in Python.** Measured 54 000× at a million elements, and the gap grows.
6. **Keep the load factor bounded, and resize by a *factor*.** Growing by a constant gives $\Theta(n^2)$ total rehashing, exactly as in [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]] §4.
7. **Rehash — never copy — on resize.** Bucket indices depend on $N$, so a verbatim copy leaves every key unfindable.
8. **Under open addressing, delete with a tombstone.** Blanking a slot severs probe sequences and makes later entries invisible, with the symptom appearing after *unrelated* deletions.
9. **"$O(1)$" is expected, not worst case.** With colliding keys it is $O(n)$, and that is reachable by an adversary. **If keys are user-supplied and the workload is security-sensitive, consider a balanced tree.**
10. **Dict insertion is amortised $O(1)$**, so a single insertion can be $O(n)$ when it rehashes. Pre-size the dict if tail latency matters.
11. **`dict` preserves insertion order, not sorted order.** If you need sorted iteration, sort the keys or use a sorted structure — the confusion is common.
12. **A hash table cannot do range queries.** No amount of cleverness recovers order it deliberately destroyed; use a tree.
13. **Prefer a prime table size for hand-written tables.** A composite size shares factors with patterned keys and wastes buckets.
14. **Hash tables trade memory for speed by design** — a third of the table is empty. For large homogeneous numeric data, that is the wrong trade; use arrays ([[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]).
15. **A skip list's worst case needs bad luck; a hash table's can be manufactured.** That difference, not the asymptotics, is often the deciding factor.

> [!warning] Gaps in the source material
> **Goodrich's ch. 10 prose extracts cleanly** — the map ADT, the two-stage hashing model, the MAD compression method, the chaining/probing comparison and the load-factor discussion all came through readably.
>
> **His code did not**, per the standing problem in `00-Index.md`. **Lambert's ch. 11 covers sets and dictionaries but not hash-table internals, skip lists or collision strategies**, so there was little to fall back on: **`ChainHashMap`, the `BadHash` adversary and the entire `SkipList` are my own**, written from Goodrich's prose and **all executed** — verified for insert/overwrite/delete/`KeyError`/iteration, for the load-factor relationship, and for the skip list's sorted order, hit-and-miss search, and update-not-insert behaviour.
>
> **All measurements are my own:** the collision demonstration, the load-factor/chain-length table, the dict-versus-list scaling, the adversarial-collision timing, and the skip-list level counts.
>
> **All figures are images and are lost** — the bucket-array diagrams, the chaining and linear-probing illustrations, and (most costly) **the skip-list picture showing the express lanes**, which is how that structure is conventionally explained. §8's code and the verified level table are the substitutes, and the reader should sketch the lanes.
>
> **No error was found in Goodrich ch. 10.**
>
> **Additions beyond the source.** **§7 in its entirety is mine** — Goodrich notes that the worst case is $O(n)$ but does not demonstrate it, and the `BadHash` measurement (fixed lookup count, time doubling with $n$) makes it concrete. **The hash-flooding DoS discussion, Python's per-process hash randomisation, and the consequence that hash codes must never be persisted** are all additions and are the practically important part of the chapter. **The load-factor/chain-length table is my own experiment**, and it verifies the $O(1+\lambda)$ claim directly rather than asserting it. The observation that **rehashing on resize is amortised but latency-spiking**, linked back to [[04 - Array-Based Sequences and Amortised Analysis|ch. 04]]'s measured 5 084× spike, is mine. **Exercise 5(c)'s point that a skip list's randomness is internal and therefore adversary-resistant, while a hash table's is not**, is my own framing and is the sharpest distinction between them. The comparison table in Exercise 5(e) and the decision rule in §9 are additions.
>
> **Deliberately compressed.** **Goodrich §10.2's full open-addressing implementation** (`ProbeHashMap` with its `_AVAIL` sentinel) is described in §3 and Exercise 2(c) but not implemented — chaining suffices to demonstrate the ideas, and Python's `dict` is the open-addressing implementation one should actually use. **§10.4's `SortedTableMap`** (a sorted array with binary search) is omitted; it is $O(n)$ insertion and is dominated by the tree of [[10 - Search Trees|ch. 10]]. **§10.5's multimaps and §10.3's `MutableMapping` abstract base class** are mentioned only in passing — the ABC machinery was covered in [[01 - Python and Object-Oriented Foundations|ch. 01]] §6. **The pigeonhole argument itself is owned by [[Discrete Mathematics/contents/06 - Counting Methods and the Pigeonhole Principle|DM ch. 06]]** and cross-linked rather than reproved.

**Previous:** [[08 - Priority Queues and Heaps]] · **Next:** [[10 - Search Trees]]
