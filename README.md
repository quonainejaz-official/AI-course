# Artificial-Intelligence — A Complete Learning Repository from Python to Data Science

This repository is a complete course of Jupyter notebooks, covering everything **from beginner to advanced**. It is explained in **simple English**, with executable code examples, common mistakes, real-world problems, **LeetCode problems (number + title + link + solution)**, interview Q&A, and practice exercises.

**Target:** Interview preparation + university syllabus + practical programming skills.

---

## Folder Structure

```text
Artificial-Intelligence/
├── Python/                 # Core Python language
│   ├── Basics/
│   ├── Intermediate/
│   └── Advance/
├── OOP in Python/          # Object-Oriented Programming
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
└── _tools/                 # Notebook generators and validators (not learning material)
```

---

## Notebook Format

Every `.ipynb` notebook follows the same structure:

1. **Title + Roadmap** — What you'll learn in this notebook and the prerequisites.
2. **Concept Sections** — Each concept includes:
   - What it is
   - Why it matters
   - Syntax
   - Working example
   - Explanation of the output
   - Common mistakes
   - Interview tip
3. **Common Mistakes / Gotchas** — The places where learners commonly make mistakes.
4. **Real-World Problems** — Practical scenarios with fully commented solutions.
5. **LeetCode Problems** — `LC <number>. <Title> — <Difficulty>` along with the problem link, approach, **time/space complexity**, and solution code with `assert` test cases.
6. **Interview Questions & Answers** — 10–40 real interview questions and answers.
7. **Practice Exercises** — Tasks to solve independently, with hints.
8. **Summary / Cheat Sheet** — Quick revision notes.

---

## Recommended Learning Order

| # | Folder | Why |
|---|--------|-----|
| 1 | `Python/Basics` | Learn the fundamentals of Python—syntax, data types, control flow, collections, and functions. |
| 2 | `Python/Intermediate` | Learn generators, decorators, modules, exceptions, the standard library, and Pythonic programming techniques. |
| 3 | `OOP in Python/Basics` → `Intermediate` | Progress from classes to SOLID principles and design patterns. |
| 4 | `DSA in Python/Basics` → `Intermediate` → `Advance` | Covers the largest portion of coding interviews. |
| 5 | `Python/Advance` | Learn memory management, asyncio, concurrency, metaprogramming, and performance optimization. |
| 6 | `OOP in Python/Advance` | Covers descriptors, metaclasses, software architecture, and LeetCode design problems. |
| 7 | `Numpy/*` | Learn vectorized computing—the foundation of machine learning. |
| 8 | `Pandas/*` | Learn data analysis, groupby, merge, time-series analysis, and exploratory data analysis (EDA). |

**Tip:** Simply reading a notebook is not enough. Run every code cell yourself and experiment by changing the values.

---

## Environment / Setup

```bash
python --version           # 3.11+ (the repository was developed using Python 3.14)
pip install jupyter numpy pandas
jupyter notebook           # or open the .ipynb files in VS Code
```

The notebooks are **self-contained**:

- No external datasets or internet connection are required (all data is generated inline).
- No `input()` calls—everything runs with a single click.
- No plotting libraries are required.

---

## Tools (`_tools/`)

| File | Purpose |
|------|---------|
| `nbgen.py` | A small helper that generates valid `.ipynb` JSON files (without using `nbformat`). |
| `validate.py` | Validates notebook JSON structure, cell counts, and LeetCode coverage across all notebooks. |
| `runnb.py` | Executes every notebook from top to bottom to detect runtime errors. |
| `gen/` | Generator scripts for every notebook (the source of the notebook content). |
| `AGENT_SPEC.md` | Authoring standard—create new notebooks following this format. |

```bash
python _tools/validate.py                    # Validate the structure of all notebooks
python _tools/runnb.py                       # Execute and test all notebooks
python _tools/runnb.py "Python/Basics"       # Execute notebooks from a single folder
```

If you need to modify a notebook, it is recommended to edit the corresponding script in `_tools/gen/<script>.py` and regenerate the notebook. This keeps the formatting consistent across the repository.

---

## LeetCode Coverage

Every topic includes its relevant LeetCode problems, complete with the **problem number, exact title, problem link, solution approach, time and space complexity, and test cases**.

The DSA section covers **250+ problems**, including:

- Arrays
- Strings
- Binary Search
- Sorting
- Linked Lists
- Stacks & Queues
- Hashing
- Trees
- Heaps
- Backtracking
- Graphs
- Dynamic Programming
- Trie
- Union-Find
- Segment Tree
- Greedy Algorithms
- Bit Manipulation
- Mathematics
- Matrices
- System Design / Design Problems

`DSA in Python/Advance/06_Advanced_Patterns_Interview_Roadmap_aur_MockTests.ipynb` contains:

- A curated list of must-do interview problems
- Pattern-to-problem mapping
- Three full mock coding interviews
- An eight-week interview preparation study plan

---

Happy learning—and remember:

**Don't just read the notebooks. Run them.** 🚀