---
subject: Basic Programming (C++)
chapter: 6
tags: [ds, cpp, arrays, array-decay, c-strings, buffer-overflow, vector, string, cache-locality]
source: "D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*, ch. 8"
---

# Arrays, C-Strings and `std::vector`

**A C++ array does not know its own length.** Pass it to a function and the length is gone — §1 shows `sizeof` dropping from 20 to 8 as the array becomes a pointer.

Everything else in this chapter follows. **§2:** a wrong length is silently accepted, because the function has no way to check. **§3:** a C-string is not a type but a *convention* — an array that happens to contain a `'\0'` — and omitting the terminator makes `strlen` read past the end. **§4:** `strcpy` writes 27 characters into an 8-byte buffer and **destroys the variable next to it**, which is the buffer overflow that has driven decades of security vulnerabilities.

**§§5–6 are the modern answer**: `std::string` and `std::vector` carry their size, so none of these bugs is expressible.

**And §7 settles something [[Data Structures and Algorithms/contents/06 - Linked Lists|DSA ch. 06]] left open.** There, cache locality was predicted to matter and measured at only **~15%** in Python. **Here the same experiment gives 2.5×**, and the reason is exactly what DSA suspected.

**Every program below was compiled and run** (MSVC 14.50, `/std:c++17 /W4`).

## 📘 Main Knowledge

### 1. ⚠️ Array decay — the length does not survive a function call

```cpp
void takesArray(int arr[]) { std::cout << sizeof(arr); }
int a[5] = {10,20,30,40,50};
```
```
in main:                sizeof(a)   = 20     -> 5 elements
inside takesArray:      sizeof(arr) = 8      <- the size of a POINTER
```
*(Verified.)*

> [!warning] `int arr[]` in a parameter list is a lie
> **It means `int*`.** The array *decays* to a pointer to its first element, and the length — which the compiler knew perfectly well in `main` — is discarded at the boundary.
>
> **So `sizeof(arr)/sizeof(arr[0])`, the standard idiom for array length, silently gives the wrong answer inside any function.**

**Two honest alternatives** *(both verified to give the correct average of 30)*:
```cpp
double average(const int* arr, std::size_t n);       // pass the length yourself
template <std::size_t N>
double averageRef(const int (&arr)[N]);              // reference-to-array keeps N
```

### 2. ⚠️ So a wrong length is silently accepted

```
average(a, 5) = 30                correct
average(a, 8) = -1.45759e+08      *** read 3 elements past the end
```
*(Verified.)*

**No error.** The function received a pointer and a number; **it has no way to tell that the number is wrong.**

**This is the single strongest argument for `std::vector`**: the size travels with the object, so there is no separate length to get wrong.

### 3. C-strings are a convention, not a type

```cpp
char s[6] = {'H','e','l','l','o','\0'};
```
```
strlen(s) = 5      <- counts up to the '\0'
sizeof(s) = 6      <- the ARRAY size, including the terminator
```

**`strlen` is $O(n)$ — it scans.** `std::string::size()` is $O(1)$.

**⚠️ Omit the terminator and it reads past the end** *(verified)*:
```cpp
char bad[5] = {'H','e','l','l','o'};     // exactly 5, no '\0'
strlen(bad) = 6                          // should be 5
```

> [!note] The terminator is the only thing that ends a C-string
> **There is no length stored anywhere.** Every C-string function — `strlen`, `strcpy`, `printf("%s")` — walks forward until it finds a zero byte. **If there isn't one, it keeps going into whatever follows.**
>
> *(It returned 6 here because the next byte happened to be non-zero and the one after that was zero. On another run, with a different layout, it could return any number.)*

### 4. ⚠️ The buffer overflow

*(Verified — `char dest[8]` with a neighbouring buffer holding `"IMPORTANT"`:)*
```
strcpy(dest, "This string is far too long")     // 27 chars into 8 bytes

after strcpy:  dest      = "This string is far too long"
               neighbour = "ing is far too long"       <- CLOBBERED
```

> [!warning] It wrote past `dest` and destroyed an unrelated variable
> **No error. No crash.** `dest` even *appears* to hold the whole string — because printing it also runs off the end into the neighbour's memory.
>
> **`strcpy` has no idea how big the destination is.** It takes two pointers and copies until it finds a terminator in the *source*. **The destination's capacity is not a parameter and cannot be checked.**
>
> **This is the mechanism behind decades of security vulnerabilities.** Overwriting an adjacent variable is the benign case; overwriting a saved return address lets an attacker redirect execution.
>
> **`std::string` cannot do this** — it owns its buffer and grows it as needed.
>
> **✅ MSVC warned:** `C4996: 'strcpy': This function or variable may be unsafe` *(verified — fired for every call)*. **Another warning-coverage data point**, and one where the compiler is genuinely helpful.

### 5. `std::string`

```cpp
std::string c = a + b;      // no buffer, no length, no terminator
c.size()                    // O(1)
c.substr(6)                 // "world"
c.find("wor")               // 6
a == "Hello"                // true -- compares TEXT
```
*(All verified.)*

> [!warning] With `char*`, `==` compares addresses
> ```
> (p1 == p2)            -> false      *** two identical strings
> strcmp(p1, p2) == 0   -> true       (the correct way)
> ```
> *(Verified.)*
>
> **It compiles.** `p1 == p2` is a perfectly legal pointer comparison, and it asks *"are these the same address?"* rather than *"do these say the same thing?"*.
>
> **It sometimes appears to work**, because identical string literals may be pooled into one address by the compiler — so the bug can pass testing and fail in production. **`std::string` compares by value and has no such trap.**

### 6. `std::vector` — a growable array that knows its size

```
v.size()   = 5        <- travels WITH the object
v.at(9)    -> throws std::out_of_range
average(v) = 30       <- no length argument to get wrong
```
*(Verified.)*

**§2's bug is not merely unlikely here — it is inexpressible**, because there is no separate length to pass.

**Growth is geometric** *(verified — capacities observed while appending 40 elements)*:
```
1  2  3  4  6  9  13  19  28  42
```

> [!note] MSVC grows by 1.5×, not 2×
> **The ratios above are ≈1.5.** libstdc++ (GCC) doubles. **Both give amortised $O(1)$ `push_back`** — [[Data Structures and Algorithms/contents/04 - Array-Based Sequences and Amortised Analysis|DSA ch. 04]]'s geometric argument works for any factor $>1$ — but the constants differ, so **capacity is not portable and must never be relied on.**
>
> *(1.5× is chosen because it can reuse previously freed blocks; 2× never can.)*
>
> **`reserve(40)` first gives capacity 40 and no reallocation at all** *(verified)* — which also removes [[04 - Repetition|ch. 04]]'s iterator-invalidation hazard.

### 7. Contiguous memory — and the answer to a question [[Data Structures and Algorithms/contents/06 - Linked Lists|DSA ch. 06]] left open

*(Verified — a 4000×4000 matrix, 16 000 000 elements, summed two ways:)*

| traversal order | time |
|---|---|
| **row-major** (`i` then `j`) | **0.0382 s** |
| column order (`j` then `i`) | **0.0965 s** |
| | **2.5× slower** |

**Identical work. Identical answer** *(verified)*. **The only difference is the order of memory access.**

> [!note] This settles DSA ch. 06's open question
> **[[Data Structures and Algorithms/contents/06 - Linked Lists|DSA ch. 06]] predicted that contiguous storage would beat pointer-chasing on cache locality, and measured only ~15% in Python** — concluding that the textbook argument was "much weaker in Python, because Python lists are *referential* and both structures chase pointers."
>
> **That diagnosis is confirmed here.** In C++ the `int`s are stored **inline**, so a 64-byte cache line carries the next 16 values you are about to want. **Row-major order uses all of them; column order uses one per line and discards the rest.**
>
> **2.5× versus 15% is the difference between a real effect and a residual one** — and it is the same principle [[Data Structures and Algorithms/contents/10 - Search Trees|DSA ch. 10]] §7 used to justify B-trees, now visible at the RAM/cache level rather than the disk/RAM level.
>
> *(This layout is `vector<vector<int>>`, so each row is separately allocated — a genuinely flat `vector<int>` indexed as `i*N+j` would show a larger gap still.)*

### 8. `std::array` — fixed size, no decay

```
std::array<int,5>: size() = 5, sizeof = 20        (identical to int[5])
inside a function: size() = 5                      <- length SURVIVES
```
*(Verified.)*

**Zero overhead over a raw array, and it does not decay.** Prefer it whenever the size is a compile-time constant.

### 9. What to use

| | verdict |
|---|---|
| `int[]` raw array | **avoid** — decays, loses its length, no bounds check |
| `char[]` / `char*` | **avoid** — no length, terminator hazard, `==` compares addresses |
| **`std::array<T,N>`** | fixed compile-time size; no overhead, no decay |
| **`std::vector<T>`** | **the default** — growable, knows its size, `.at()` checks |
| **`std::string`** | **the default for text** |

## ✏️ Exercises

**1. (Decay.)** (a) What is array decay and what did `sizeof` show? (b) Why is §2's wrong length undetectable? (c) What are the alternatives? (d) Why does this argue for `vector`?

> [!example]- Solution
> **(a) An array converts to a pointer to its first element in almost every context, including a function call.**
>
> *(Verified: `sizeof(a)` = **20** in `main` — five 4-byte ints — and `sizeof(arr)` = **8** inside the function, the size of a 64-bit pointer.)*
>
> **`void f(int arr[])` and `void f(int* arr)` declare the same function.** The `[]` is syntax that suggests an array and delivers a pointer — **the declaration misleads deliberately.**
>
> **The practical consequence: `sizeof(arr)/sizeof(arr[0])`, the standard length idiom, silently gives the wrong answer inside any function.** In `main` it gives 5; in the callee it gives 8/4 = 2.
>
> **(b) Because the function has nothing to check against.**
>
> *(Verified: `average(a, 8)` returned **−1.45759×10⁸** — it read three elements past the end.)*
>
> **The function received a pointer and a count.** There is no length stored with the array, no header, no sentinel. **The pointer says where the data starts and nothing says where it ends** — so `n = 8` is as plausible to the function as `n = 5`.
>
> **And the failure is [[04 - Repetition|ch. 04]]'s out-of-bounds read**: undefined behaviour, no diagnostic, and a value that could easily have been small and plausible instead of obviously wrong.
>
> **(c)**
>
> | approach | keeps the length? | cost |
> |---|---|---|
> | `f(const int* a, size_t n)` | **only if you pass it correctly** | none |
> | `template<size_t N> f(const int (&a)[N])` | **yes, at compile time** | a template instantiation per size |
> | **`f(const std::vector<int>&)`** | **yes, in the object** | none for the common case |
> | `f(std::span<const int>)` (C++20) | **yes** | none — the modern answer |
>
> *(Both the pointer-plus-length and reference-to-array forms were verified to give 30.)*
>
> **The reference-to-array form is exact but rigid** — `N` is part of the type, so a function taking `int(&)[5]` cannot accept an `int[6]`, and each size instantiates separately.
>
> **`std::span` is what modern C++ uses**: a pointer and a length in one non-owning object, accepting arrays, vectors and `std::array` alike, with no copy.
>
> **(d) Because it makes §2's bug inexpressible rather than merely unlikely.**
>
> **The size is a member of the object.** `v.size()` cannot disagree with the data, because it *is* the data's length. **There is no second number to pass wrongly.**
>
> **This is the same principle the vault has met repeatedly**: [[Database Management Systems/contents/01 - Databases and Data Models|DBMS ch. 01]]'s normalisation *"restricts the representable states, not the answerable questions"*, and [[01 - Fundamentals - Types, Variables and Expressions|ch. 01]]'s `const` making an invalid assignment a compile error. **The strongest fix is not detecting the bad state but making it unrepresentable.**

**2. (Hard — C-strings.)** (a) Why is a C-string a convention? (b) What did the missing terminator do? (c) Explain the overflow. (d) Why does `==` on `char*` sometimes appear to work?

> [!example]- Solution
> **(a) Because nothing in the type system says "string".**
>
> **`char[6]` is an array of six characters.** What makes it a *string* is an agreement that the text ends at the first `'\0'`. **The type carries no length and no guarantee that a terminator exists.**
>
> *(Verified: `strlen(s)` = 5 counts to the terminator, while `sizeof(s)` = 6 is the array — two different numbers for the same object, and you must know which you want.)*
>
> **`strlen` is $O(n)$ because it scans for the terminator** — so a loop written `for (i = 0; i < strlen(s); ++i)` is accidentally $O(n^2)$, a classic performance bug that `std::string::size()` (which is $O(1)$) cannot cause.
>
> **(b) `strlen` ran past the end of the array.**
>
> *(Verified: `char bad[5] = {'H','e','l','l','o'}` — no terminator — gave `strlen(bad)` = **6**, not 5.)*
>
> **It returned 6 because the byte after the array happened to be non-zero and the next one happened to be zero.** That is an accident of this stack layout on this run. **It is undefined behaviour: on another build it could return 5, or 500, or crash.**
>
> **And 6 is a *plausible* answer** — off by one, the kind of result that looks like an ordinary off-by-one bug rather than memory corruption, which sends you looking in the wrong place.
>
> **(c) `strcpy` copies until it finds a terminator in the *source*, with no knowledge of the destination's size.**
>
> *(Verified: 27 characters copied into `char dest[8]`. Afterwards `dest` printed the whole string, and the neighbouring buffer — which held `"IMPORTANT"` — read `"ing is far too long"`.)*
>
> **The neighbour was overwritten by the overflow.** The 19 bytes that did not fit in `dest` were written into the memory immediately after it, which belonged to another variable.
>
> **Two things make this worse than an ordinary bug:**
> 1. **`dest` appears to work.** Printing it walks off the end into the neighbour's bytes and reproduces the whole string — **so the variable you overflowed looks correct and the one you corrupted looks wrong.** The symptom appears in innocent code.
> 2. **It is the classic security vulnerability.** Overwriting an adjacent variable is benign by comparison; **overwriting a function's saved return address lets an attacker choose where execution resumes.** This is the stack-smashing attack, and it is why `gets` was removed from the C standard entirely.
>
> **✅ The compiler did warn** — `C4996: 'strcpy' … may be unsafe` *(verified, on every call)*. **This is a case where tooling helps**, unlike [[04 - Repetition|ch. 04]]'s stray semicolon. *(`strncpy` and `strcpy_s` take a size, but `strncpy` does not guarantee a terminator — the safe answer is `std::string`.)*
>
> **(d) Because identical string literals may share one address.**
>
> *(Verified: `p1 == p2` was **false** for two identical strings — one a literal, one a copy in a local array — while `strcmp(p1,p2) == 0` was **true**.)*
>
> **`p1 == p2` is a legal pointer comparison** asking *"same address?"*, not *"same text?"*. It compiles without complaint because comparing two `const char*` is a perfectly ordinary thing to do.
>
> **The danger is when it appears to work.** Compilers commonly pool identical string literals, so:
> ```cpp
> const char* a = "hello";
> const char* b = "hello";
> a == b        // often TRUE -- same pooled literal
> ```
> **A test using literals passes. Production code comparing a literal against a string read from a file fails**, because that one is at a different address.
>
> **This is the vault's recurring shape once more**: code that compiles, runs, gives the right answer in testing, and is wrong for a reason invisible at the call site. **`std::string`'s `==` compares text and has no such mode.**

**3. (Modern containers and locality.)** (a) What does `vector` fix? (b) What did growth show, and what must not be relied on? (c) Explain the 2.5×. (d) Why is this stronger than DSA ch. 06's result?

> [!example]- Solution
> **(a) It carries its size, checks bounds on request, and owns its memory.**
>
> *(Verified: `size()` = 5 without being told; `at(9)` threw `std::out_of_range`; the average function needed no length argument.)*
>
> **Three bugs become inexpressible:** §2's wrong length (there is no separate length), §3's missing terminator (no terminator convention), and §4's overflow (`push_back` grows the buffer rather than running past it).
>
> **And it costs nothing for the common case.** `operator[]` is unchecked and compiles to the same addressing as a raw array ([[04 - Repetition|ch. 04]] §3); the size is one extra pointer-sized member.
>
> **(b)** *(Verified — capacities while appending 40 elements:)*
> ```
> 1  2  3  4  6  9  13  19  28  42
> ```
> **The ratios are ≈1.5. MSVC grows by 1.5×; libstdc++ doubles.**
>
> **Both give amortised $O(1)$ `push_back`** — [[Data Structures and Algorithms/contents/04 - Array-Based Sequences and Amortised Analysis|DSA ch. 04]]'s geometric argument holds for any factor $>1$, since the total copying over $n$ appends is a convergent geometric series.
>
> **What must not be relied on is `capacity()` itself.** It is implementation-defined and differs between compilers and versions. **Code that assumes a doubling sequence is not portable**, and code that assumes no reallocation because "there should be room" is the [[04 - Repetition|ch. 04]] iterator-invalidation bug waiting to happen.
>
> *(The 1.5× choice is deliberate: with a 1.5 factor the sum of previously freed blocks can eventually exceed the next request, so the allocator can reuse them. With 2× it never can.)*
>
> **`reserve()` is the right tool when the size is known** *(verified: `reserve(40)` gave capacity 40 and no reallocation)* — it avoids the copying *and* removes the invalidation hazard.
>
> **(c) Cache lines.**
>
> *(Verified: summing a 4000×4000 matrix row-major took **0.0382 s**, column-major **0.0965 s** — **2.5×** — with identical answers.)*
>
> **Memory is fetched in cache lines of 64 bytes**, holding 16 `int`s. **Row-major traversal walks along a row, so each fetched line supplies the next 16 values** — one memory access per 16 elements.
>
> **Column traversal jumps a whole row between accesses**, so each fetched line supplies **one** useful value and the other 15 are evicted before being needed. **The work is identical; the memory traffic is up to 16× larger.**
>
> **This is the same argument [[Data Structures and Algorithms/contents/10 - Search Trees|DSA ch. 10]] §7 used for B-trees**, one level down the hierarchy: *match the access pattern to the block size*. There the block was a 4 KB disk page and the payoff was 30 seeks versus 3; **here the block is a 64-byte cache line and the payoff is 2.5×.**
>
> **(d) Because it confirms the diagnosis DSA ch. 06 could only conjecture.**
>
> **[[Data Structures and Algorithms/contents/06 - Linked Lists|DSA ch. 06]] set out to measure the textbook locality argument in Python and got ~15%** — far less than expected. **Its conclusion was that Python lists are *referential*: they store pointers to boxed integer objects, so traversing a list chases pointers whether or not the list itself is contiguous.** In other words, both structures had the same fundamental access pattern, and the difference could only ever be small.
>
> **C++ removes that confound.** A `vector<int>` stores the `int`s **inline**, so contiguity is real all the way down — **and the effect jumps to 2.5×.**
>
> **The pair of measurements together is worth more than either alone.** One says the effect is small in Python; the other says it is large in C++; **and the explanation — boxed versus inline storage — predicts exactly that difference.** A textbook claim that seemed overstated turns out to be correct about the mechanism and merely inapplicable to the language it was tested in.
>
> **The transferable lesson: when a measurement disappoints, ask whether the mechanism is actually present** — rather than concluding the principle is wrong. *(And note this is the reverse of the [[Data Structures and Algorithms/contents/00-Index|DSA]] pattern where a measurement contradicting a proof meant the measurement was flawed. Here the measurement was right and the *setting* was wrong.)*

## 📝 Summary

- **⚠️ Arrays decay to pointers, and the length does not survive a function call** *(verified: `sizeof` went from **20** in `main` to **8** — a pointer — inside the function)*. **`int arr[]` in a parameter list means `int*`.**
- **So `sizeof(arr)/sizeof(arr[0])` silently gives the wrong answer inside any function.**
- **⚠️ A wrong length is undetectable** *(verified: `average(a, 8)` on a 5-element array returned **−1.45759×10⁸**)* — the function has a pointer and a number, and nothing to check against.
- **A C-string is a convention, not a type.** `strlen` is $O(n)$ and scans for `'\0'`; `std::string::size()` is $O(1)$.
- **⚠️ Omit the terminator and `strlen` reads past the array** *(verified: returned **6** for a 5-character buffer)* — and 6 is *plausible*, so it looks like an ordinary off-by-one.
- **⚠️ `strcpy` overflowed an 8-byte buffer with 27 characters and destroyed the neighbouring variable** *(verified: `"IMPORTANT"` became `"ing is far too long"`)*. **`dest` still printed correctly**, so the corrupted variable is the one that looks wrong.
- **✅ MSVC warned (`C4996`)** on every `strcpy` — a case where the tooling genuinely helps.
- **⚠️ `==` on `char*` compares addresses, not text** *(verified: **false** for two identical strings, while `strcmp == 0` was true)* — **and it often appears to work**, because identical literals may be pooled.
- **`std::vector` carries its size** *(verified: `at(9)` threw; no length argument to get wrong)*, making §2's bug **inexpressible rather than unlikely.**
- **Growth is geometric, but MSVC uses 1.5× not 2×** *(verified: 1, 2, 3, 4, 6, 9, 13, 19, 28, 42)*. **Both give amortised $O(1)$** ([[Data Structures and Algorithms/contents/04 - Array-Based Sequences and Amortised Analysis|DSA ch. 04]]); **`capacity()` is implementation-defined and must not be relied on.** `reserve()` removes both the copying and [[04 - Repetition|ch. 04]]'s invalidation hazard.
- **⚠️ Row-major traversal beat column-major by 2.5×** *(verified: 0.0382 s vs 0.0965 s, identical answers)* — identical work, different memory order.
- **This settles [[Data Structures and Algorithms/contents/06 - Linked Lists|DSA ch. 06]]'s open question.** There, locality measured only **~15%** in Python and the conjecture was that Python's *referential* lists made both structures chase pointers. **C++ stores `int`s inline, and the effect jumps to 2.5×** — the mechanism was right, the setting was wrong.
- **`std::array<T,N>` has zero overhead over a raw array and does not decay** *(verified: `size()` survives a call)*.

## ⚠️ Important Notes

1. **⚠️ Never rely on `sizeof(arr)/sizeof(arr[0])` inside a function.** The array has already decayed.
2. **Prefer `std::vector` to a raw array by default**, and `std::array<T,N>` when the size is a compile-time constant.
3. **Use `std::span` (C++20) for a non-owning view** that keeps the length — it accepts arrays, vectors and `std::array` alike.
4. **If you must pass a pointer and a length, pass them together and never separately derived.**
5. **⚠️ Prefer `std::string` to `char[]` unconditionally.** No terminator to forget, no length to lose, `==` compares text.
6. **⚠️ Never use `strcpy`, `strcat` or `gets`.** They have no destination size and cannot be made safe.
7. **Never call `strlen` in a loop condition** — it re-scans every iteration, making the loop $O(n^2)$.
8. **⚠️ Never compare C-strings with `==`.** It compares addresses and may pass tests because literals are pooled. Use `strcmp`, or `std::string`.
9. **A missing `'\0'` is undefined behaviour, and its symptom is a plausible off-by-one** — which sends you debugging the wrong thing.
10. **Use `.at()` when the index is not provably in range**; `operator[]` is unchecked ([[04 - Repetition|ch. 04]]).
11. **⚠️ Never rely on `capacity()` or on a particular growth factor.** MSVC uses 1.5×, libstdc++ 2×; both are implementation details.
12. **`reserve()` when the final size is known** — it avoids reallocation cost *and* iterator invalidation.
13. **Traverse in memory order.** Row-major for row-major data; the 2.5× is free.
14. **For numeric work prefer a flat `vector<T>` indexed `i*N+j`** to `vector<vector<T>>` — one allocation, fully contiguous, better locality still.
15. **When a locality measurement disappoints, check whether the data is genuinely contiguous** before concluding the principle does not hold.

> [!warning] Gaps in the source material
> **Malik ch. 8 extracts well** — array declaration and initialisation, array parameters, C-strings and the `<cstring>` functions, two-dimensional arrays, and the `std::vector` introduction all came through readably, with listings intact. **Book page $n$ = PDF page $n+50$; ch. 8 is PDF pages 571–660.** *(Standing quirk: `C++` in prose renders as `C11`.)*
>
> **All figures are images and are lost** — chiefly the memory-layout diagrams showing array elements in consecutive addresses, and the row-major storage diagram for 2-D arrays. **§§1 and 7 substitute measured `sizeof` values and a timed traversal**, which demonstrate the same facts by consequence rather than by picture.
>
> **All programs are my own.**
>
> **No error was found in Malik ch. 8.**
>
> **Additions beyond the source.** **Malik covers arrays, C-strings and their pitfalls as a first course does — describing what to avoid. Every demonstration here is an addition:**
>
> - **§1's `sizeof` comparison is mine** — showing 20 becoming 8 across a call makes decay concrete in a way the prose statement does not.
> - **§4's buffer overflow is mine**, and it produced the chapter's most vivid result: **`strcpy` writing 27 bytes into an 8-byte buffer left `dest` printing correctly while the *neighbour* read `"ing is far too long"`.** **The observation that the overflowed variable looks fine and the corrupted one looks wrong** — so the symptom appears in innocent code — is my own, as is the connection to stack-smashing.
> - **§5's `==` on `char*` is mine**, including **why it often appears to work** (literal pooling), which is what makes it survive testing.
> - **§6's growth measurement produced a precise finding not in the book: MSVC grows by ≈1.5×, not 2×** *(1, 2, 3, 4, 6, 9, 13, 19, 28, 42)*, with the note that libstdc++ doubles and that **both satisfy [[Data Structures and Algorithms/contents/04 - Array-Based Sequences and Amortised Analysis|DSA ch. 04]]'s amortised argument** — plus the reason 1.5× is chosen (block reuse).
> - **⚠️ §7 is the chapter's most valuable addition and is entirely mine.** It **resolves a question left open in [[Data Structures and Algorithms/contents/06 - Linked Lists|DSA ch. 06]]**, which measured cache locality at only ~15% in Python and conjectured that Python's referential lists were responsible. **Running the equivalent experiment in C++ gives 2.5×**, confirming the diagnosis: the mechanism was real and the language was masking it. **Neither book contains this comparison** — it exists only because both subjects are in the same vault.
> - **The modern-practice recommendations** — `std::span`, `std::array`, flat `vector` over `vector<vector>`, never `strcpy`/`gets` — are additions per the subject file.
>
> **Deliberately compressed.** **Malik's two-dimensional-array material** is represented by §7's matrix rather than developed separately; the row-major storage order is the part that matters and it is measured. **Parallel arrays** (a pre-`struct` idiom) are omitted — [[07 - Structs and Classes|ch. 07]] gives the correct answer. **The full `<cstring>` catalogue** (`strncpy`, `strcat`, `strstr`, `strtok`) is not reproduced: the recommendation is `std::string`, and listing the C functions in detail would undercut it. **`std::vector` is introduced here rather than deferred**, because presenting raw arrays without the alternative would teach a practice this vault does not endorse.

**Previous:** [[05 - Functions and Scope]] · **Next:** [[07 - Structs and Classes]]
