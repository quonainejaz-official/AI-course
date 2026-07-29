# ENV NOTES — Python/Advance authors (probe kiye hue asli facts, guess nahi)

Ye notes `runnb.py` ke asli execution environment par test kar ke likhi gayi hain.
`AGENT_SPEC.md` ke saath ye bhi LAZMI follow karo.

## Runtime
- Python **3.14.0** (CPython, GIL enabled → `sys._is_gil_enabled()` == True), numpy 2.4.2, pandas 3.0.5.
- matplotlib/seaborn NAHI hain. Network NAHI. `input()` NAHI.
- `runnb.py` har code cell ko `exec(compile(src,...), ns)` se **ek shared namespace** me chalata hai,
  `ns["__name__"] == "__main__"`, aur cwd ek fresh temp dir hota hai.
  Har cell error-free chalna chahiye warna `[FAIL]`.

## Wo cheezein jo exec-namespace me TOOT jaati hain (test-verified)

1. **`ProcessPoolExecutor` / `multiprocessing.Pool` cell ke andar kaam NAHI karega.**
   Windows par start method `spawn` hai; child `__main__` (yaani runnb.py) ko re-import karta hai
   aur cell me define kiya function wahan nahi milta → `RuntimeError` / pickling error.
   **SAFE PATTERN (yehi use karo):** script ko `textwrap.dedent` se string me likho,
   `tempfile` me `.py` file likho (guard `if __name__ == "__main__":` + `mp.freeze_support()` ke sath),
   phir `subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=120)`
   se chala kar `r.stdout` print karo. Ye verified chalta hai (rc 0).
   Aise har cell ko `try/except` me bhi rakho aur `r.returncode` check karo.

2. **`inspect.getsource()`** cell me define kiye function par `OSError: could not get source code` deta hai.
   Options: (a) stdlib function par demo karo (`inspect.getsource(textwrap.shorten)`),
   (b) tempfile module likh kar `importlib.util` se import kar ke uske function par getsource,
   (c) `try/except` me wrap kar ke message print karo. `inspect.signature`/`getmembers` theek chalte hain.

3. **`get_type_hints(Cls)`** string/`from __future__ import annotations` wale annotations ke liye
   `NameError` de sakta hai (module `__main__` = runnb.py, cell ka ns nahi).
   Fix: **`get_type_hints(Cls, globalns=globals())`** — verified kaam karta hai.

4. **`timeit`** me cell ke variables use karne ke liye `globals=globals()` LAZMI:
   `timeit.timeit("sum(data)", globals=globals(), number=100)`. Warna `NameError`.
   `setup=` string bhi `globals=globals()` ke sath likho ya self-contained rakho.

## 3.14-specific numbers (in par assert MAT karo, sirf print + samjhao)
- **Immortal objects (PEP 683):** `sys.getrefcount(1)` / `(None)` / `(True)` → `3221225472`.
  Isay concept ke tor par samjhao ("immortal — refcount fixed rehta hai"), koi exact assert nahi.
  Normal objects ke refcount deltas (`+1` on alias) reliable hain.
- **GC:** `gc.get_threshold()` → `(2000, 10, 0)` (3.13+ incremental GC; teesri value 0).
  "700" jaisa hardcoded number na likho — `gc.get_threshold()` print karo.
- **Race condition:** 3.14 me naive `counter += 1` loop **race show nahi karta** (specialized bytecode).
  Reliable recipe (verified: 20000×4 → 20000 instead of 80000):
  ```python
  tmp = counter          # read
  time.sleep(0)          # yield → yahan doosra thread ghus jata hai
  counter = tmp + 1      # write (lost update)
  ```
  `n` chhota rakho (~5000 per thread, 4 threads) taake tez rahe. Assert sirf
  `assert final <= expected` (kabhi kabhi theek bhi aa sakta hai) — exact wrong value assert na karo.
- **`dis`** output 3.14 ka naya hai (`LOAD_SMALL_INT`, `LOAD_FAST_BORROW`, `BINARY_OP`).
  Constant folding demo: `2*3` compile-time par `6` ban jata hai — bas print/samjhao,
  bytecode text par assert NAHI.
- String literal interning (`"hello world" is "hello world"` same cell me → True) aur
  `sys.intern` verified. Lekin runtime-built strings ke liye `is` ka natija implementation-defined —
  print karo, assert na karo.
- `type Vec = list[float]` (PEP 695), `StrEnum`, `asyncio.TaskGroup`, `asyncio.timeout`,
  `tomllib`, `zoneinfo("Asia/Karachi")`, `weakref` + `gc.collect()`, `tracemalloc`,
  `cProfile`+`pstats` (stream=StringIO) — sab verified chalte hain.
- `@dataclass(slots=True, kw_only=True)` verified.

## Timing / determinism rules
- Har notebook **total < ~30 second**. `asyncio.sleep`/workload chhote rakho (0.01–0.1s).
- Timing numbers machine par badalte hain → `assert fast < slow` jaisi **timing-based assert NAHI**.
  Sirf print karo aur "aam tor par X tez hota hai" likho.
- LeetCode asserts deterministic hone chahiye (koi timing/threading luck par depend nahi).
  Threading wale LC (1114/1115/1116/1195) me output ko `list`/`str` me collect kar ke `join` ke baad assert karo.

## Style reminders (spec se)
- Roman Urdu + English mix, har concept: Kya hai → Kyun → Syntax → Example → Output ka matlab → Gotchas → Interview tip.
- `md()`/`code()` ke triple-quoted string ka content **column 0** se; code me backslash ho to `r"""..."""`.
- 55+ cells per notebook, asli depth. LeetCode section me exact number + title + link + approach + complexity + chalte asserts.
