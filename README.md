# Artificial-Intelligence — Python se Data Science tak ka Complete Learning Repo

Ye repo Jupyter notebooks ka ek mukammal course hai — **zero se advance tak**, Roman Urdu + English mix me samjhaya gaya,
chalte hue code examples, common mistakes, real-world problems, **LeetCode problems (number + title + link + solution)**,
interview Q&A aur practice exercises ke sath.

Target: **interview preparation + university syllabus + practical skill**.

---

## Folder Structure

```
Artificial-Intelligence/
├── Python/                 # Core Python language
│   ├── Basics/
│   ├── Intermediate/
│   └── Advance/
├── OOP in Python/          # Object Oriented Programming
│   ├── Basics/
│   ├── Intermediate/
│   └── Advance/
├── DSA in Python/          # Data Structures & Algorithms
│   ├── Basics/
│   ├── Intermediate/
│   └── Advance/
├── Numpy/                  # Numerical computing
│   ├── Basics/
│   ├── Intermediate/
│   └── Advance/
├── Pandas/                 # Data analysis
│   ├── Basics/
│   ├── Intermediate/
│   └── Advance/
└── _tools/                 # notebook generators + validators (learning material nahi)
```

---

## Har Notebook ka Format

Har `.ipynb` file ek hi pattern follow karti hai:

1. **Title + roadmap** — is notebook me kya seekhenge, prerequisites
2. **Concept sections** — har concept: *Kya hai → Kyun → Syntax → Chalta hua example → Output ka matlab → Common mistakes → Interview tip*
3. **Common Mistakes / Gotchas** — wo jagahain jahan log phaste hain
4. **Real-World Problems** — realistic masle, commented solutions
5. **LeetCode Problems** — `LC <number>. <Title> — <Difficulty>` + link + approach + **time/space complexity** + solution code with `assert` tests
6. **Interview Questions & Answers** — 10-40 real interview sawal
7. **Practice Exercises** — khud karne ke liye tasks with hints
8. **Summary / Cheat-sheet** — quick revision

---

## Kaise Padhein (Recommended Order)

| # | Folder | Kyun |
|---|--------|------|
| 1 | `Python/Basics` | Language ki buniyad — syntax, data types, control flow, collections, functions |
| 2 | `Python/Intermediate` | Generators, decorators, modules, exceptions, stdlib, Pythonic idioms |
| 3 | `OOP in Python/Basics` → `Intermediate` | Classes se SOLID + design patterns tak |
| 4 | `DSA in Python/Basics` → `Intermediate` → `Advance` | Interview ka sab se bara hissa |
| 5 | `Python/Advance` | Memory model, asyncio, concurrency, metaprogramming, performance |
| 6 | `OOP in Python/Advance` | Descriptors, metaclasses, architecture, LeetCode design problems |
| 7 | `Numpy/*` | Vectorized computing — ML ki buniyad |
| 8 | `Pandas/*` | Data analysis, groupby/merge/time-series, EDA case studies |

**Tip:** ek notebook padhte waqt sirf parhna kaafi nahi — har code cell khud chala kar, values badal kar dekho.

---

## Environment / Setup

```bash
python --version           # 3.11+ (repo Python 3.14 par bana hai)
pip install jupyter numpy pandas
jupyter notebook           # ya VS Code me .ipynb khol lo
```

Notebooks **self-contained** hain:
- koi bahar ki data file ya internet ki zaroorat nahi (data inline banaya jata hai)
- `input()` nahi hai — sab kuch ek click par chal jata hai
- plotting libraries ki zaroorat nahi

---

## Tools (`_tools/`)

| File | Kaam |
|------|------|
| `nbgen.py` | Chhota helper jo valid `.ipynb` JSON banata hai (bina nbformat) |
| `validate.py` | Saare notebooks ka JSON/structure check + cell counts + LeetCode coverage |
| `runnb.py` | Har notebook ke code cells ko upar se neeche chala kar errors check karta hai |
| `gen/` | Har notebook ka generator script (content ka source) |
| `AGENT_SPEC.md` | Authoring standard — naye notebooks isi format me banao |

```bash
python _tools/validate.py                    # structure check (sab notebooks)
python _tools/runnb.py                       # sab notebooks chala kar test karo
python _tools/runnb.py "Python/Basics"       # sirf ek folder
```

Notebook ka content badalna ho to behtar hai `_tools/gen/<script>.py` edit kar ke dobara chalao —
is tarah notebook regenerate ho jata hai aur format consistent rehta hai.

---

## LeetCode Coverage

Har topic ke sath uske related LeetCode problems solve kiye gaye hain — **problem number, exact title, link,
approach, time/space complexity aur test cases** ke sath. DSA folders me 250+ problems cover hoti hain
(arrays, strings, binary search, sorting, linked list, stack/queue, hashing, trees, heaps, backtracking,
graphs, DP, trie/union-find/segment-tree, greedy, bits, math, matrix, design problems).

`DSA in Python/Advance/06_Advanced_Patterns_Interview_Roadmap_aur_MockTests.ipynb` me
**must-do problems ki curated list**, pattern→problem mapping, 3 mock tests aur 8-week study plan hai.

---

Happy learning — aur yaad rakho: **notebook parhna nahi, chalana hai.** 🚀
