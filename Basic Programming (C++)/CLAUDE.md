# Basic Programming (C++)

Read with the root `CLAUDE.md` and `../METHOD.md`. Scope, chapters, errata: `contents/00-Index.md`.

## Source

**D.S. Malik, *C++ Programming: From Problem Analysis to Program Design*** (Cengage 2017) — the only file in `documents/`. **No lecture slides.** Malik targets C++11 at best: note the modern form alongside the book's (`std::vector`/`std::string` over raw arrays and C-strings, smart pointers over `new`/`delete`, `nullptr`, range-`for`, `auto`) and label it as an addition.

## Toolchain: compile and run every program

This subject's verify-every-number rule is **compile and run**. **No `g++` or `clang++` on this machine**, but **MSVC 14.50.35717** is (Visual Studio 18 Build Tools), verified with C++17.

- Call `C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat`, then `cl /EHsc /std:c++17 /Zc:__cplusplus /W3 <file.cpp>`, then run `.\name.exe` (cmd does not search `.`).
- Without `/Zc:__cplusplus`, `__cplusplus` reports 199711 (C++98) even under `/std:c++17`. Always pass the flag.
- Label undefined-behaviour results as *this machine, this compiler, this run*.

## Extraction

- **Real bookmark outline** with exact chapter pages. **Book page $n$ = PDF page $n+50$.** 1 490 pages.
- **Code listings extract well**: braces, semicolons, `#include` and operators survive; indentation partly.
- **`C++` in prose renders as `C11`** (different font from the code). Read `C11` as `C++` in prose; trust operators in code.
- All figures and memory diagrams are images and lost (matters for ch. 08–09): print addresses and `sizeof` from running programs instead.

## Boundaries

- **Malik 15–18 excluded: `Data Structures and Algorithms/` owns them** (recursion DSA 03, searching/sorting DSA 11, linked lists DSA 06, stacks/queues DSA 05). Recorded in both indexes. C++ adds manual memory management, which ch. 08 covers.
- The angle: Python hides three things C++ exposes (manual memory, value vs reference as a choice, errors that don't announce themselves). Cross-link DSA where the language difference is the lesson.
