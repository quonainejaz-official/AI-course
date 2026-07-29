"""Generator: Pandas/Advance/02_Performance_Vectorization_aur_Memory_Optimization.ipynb"""
import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

cells = []

cells += [
md("""
# 02 — Performance, Vectorization aur Memory Optimization (Advanced)

**Level:** Advanced · **Series:** Pandas/Advance · **Notebook 2 of 4**

Ye notebook us sawal ka jawab hai jo har senior interview me aata hai:
*"Tumhara pandas script slow hai aur RAM kha raha hai — tum kya karoge?"*

Hum guess nahi karenge — **maapenge** (measure), phir fix karenge.

## Is notebook me kya seekhenge

1. **pandas slow kyun lagta hai** — Python overhead, object dtype, chhipi copies, apply ka misuse
2. **Measurement first** — `perf_counter`, `memory_usage(deep=True)`, `info(memory_usage='deep')`, `tracemalloc`
3. **Dtypes & memory** — int/float downcasting, `category`, `string`, nullable dtypes (`Int64`, `boolean`),
   `ArrowDtype` (PyArrow backend), datetime units, `Sparse` — aur 70-95% memory saving ka live demo
4. **Speed** — vectorization vs `apply` vs `map` vs `iterrows` vs `itertuples` vs list-comp,
   `np.where`/`np.select`, `eval`/`query`, merge tuning, groupby cython vs lambda
5. **Copy vs View** — pandas 3 ka **Copy-on-Write (CoW)**, chained assignment ka silent fail,
   `SettingWithCopyWarning` ki tareekh (history)
6. **Large data** — `read_csv` tuning, **chunked processing**, format benchmark (CSV/pickle/SQLite),
   SQL chunked read, out-of-core options (Dask/Polars/DuckDB/Spark) kab
7. **LeetCode** 4 pandas problems + **Interview Q&A** + cheat-sheet

## Prerequisites
- Pandas Basics + Intermediate (indexing, groupby, merge, dtypes)
- Numpy basics (dtype, broadcasting)
- Notebook 01 (MultiIndex) padh chuke hon to behtar

> **Note:** is machine par `matplotlib` nahi hai — is liye koi plotting nahi. Saara data **inline**
> generate hota hai (`default_rng`, `io.StringIO`, `tempfile`, `sqlite3`), koi external file nahi.
"""),

md("""
## 0. Setup aur environment sach-much kya hai

Pehla usool: **apne environment ko jaano**. Optional libraries (pyarrow, numexpr, bottleneck)
hone ya na hone se performance advice **badal** jati hai. Is liye code me kabhi `import pyarrow`
ko taken-for-granted na lo — `try/except` me check karo (ye production code me bhi best practice hai).
"""),

code("""
# --- Standard imports (poore notebook me inhi ko use karenge) ---
import io                 # in-memory text/CSV banane ke liye
import gc                 # garbage collector ko manually chalane ke liye
import os                 # file size dekhne ke liye
import sqlite3            # in-memory SQL warehouse simulate karne ke liye
import sys
import tempfile           # Windows-safe temp files
import time               # perf_counter timing
import timeit             # micro-benchmark
import tracemalloc        # Python-level peak memory
import warnings           # warning capture (CoW demo me kaam aayega)

import numpy as np
import pandas as pd

print("pandas :", pd.__version__)
print("numpy  :", np.__version__)
print("python :", sys.version.split()[0])

# --- Optional accelerators maujood hain ya nahi? ---
def have(mod: str) -> bool:
    \"\"\"Module import ho sakta hai? (True/False) — crash kiye baghair check.\"\"\"
    try:
        __import__(mod)
        return True
    except Exception:
        return False

HAS_PYARROW    = have("pyarrow")     # Arrow backend / parquet / feather
HAS_NUMEXPR    = have("numexpr")     # df.eval / df.query ka fast engine
HAS_BOTTLENECK = have("bottleneck")  # rolling/nan-aggregations tez karta hai
HAS_TABULATE   = have("tabulate")    # to_markdown() ke liye
HAS_TABLES     = have("tables")      # HDF5 (to_hdf) ke liye

for name, flag in [("pyarrow", HAS_PYARROW), ("numexpr", HAS_NUMEXPR),
                   ("bottleneck", HAS_BOTTLENECK), ("tabulate", HAS_TABULATE),
                   ("tables/HDF5", HAS_TABLES)]:
    print(f"{name:12s}: {'MAUJOOD' if flag else 'NAHI (is notebook me guarded rahega)'}")

# Reproducible random data ka ek hi source — hamesha seed do (interview me ye poochte hain)
SEED = 42
rng = np.random.default_rng(SEED)
print("\\nrng ready, seed =", SEED)
"""),

md("""
### Roman-Urdu me: output ka matlab

- Agar `pyarrow` **NAHI** hai to `dtype_backend="pyarrow"`, `ArrowDtype`, `string[pyarrow]`,
  `to_parquet`, `to_feather`, `read_csv(engine="pyarrow")` **sab fail** karenge.
  Is notebook me har aisa demo `try/except` me hai — code padho, output me "skip" note dekho,
  aur samjho ke pyarrow install hone par kya milta.
- `numexpr` na ho to `df.eval` / `df.query` **kaam karte hain** (pandas python fallback use karta hai)
  magar wo speed-up nahi milta jiske liye `eval` mashhoor hai.

**Interview tip:** "pandas fast karne ke liye kya install karoge?" ka behtareen jawab:
`pyarrow` (strings + IO + nullable), `numexpr` (eval/query), `bottleneck` (rolling/nan aggs).
"""),

md("""
## 1. pandas slow kyun lagta hai? (5 asli wajuhat)

| # | Wajah | Kya hota hai | Ilaj |
|---|---|---|---|
| 1 | **Python-level loop** | `iterrows`/`apply` har row par Python object banata hai — C loop ke bajaye interpreter chalta hai | vectorization, `np.where`, `np.select` |
| 2 | **Ghalat dtype** | `object`/python-string column = pointers ka array, har value alag heap object | `category`, `string`, numeric downcast, Arrow |
| 3 | **Chhipi copies** | har `df2 = df[cols]`, `merge`, `sort_values` naya buffer bana sakta hai | CoW samjho, chaining kam karo, columns select karo |
| 4 | **Loop me `concat`** | har iteration poora data dobara copy → **O(n²)** | list me jama karo, aakhir me ek `pd.concat` |
| 5 | **Zaroorat se zyada data** | poori CSV load ki jab 3 column chahiye thay | `usecols`, `dtype=`, `chunksize`, SQL me filter |

**Golden rule:** *"Pehle maapo, phir optimize karo."* Bina measurement optimize karna
guess-work hai — aur aksar ghalat jagah waqt zaya hota hai (Amdahl's law).

**Interview tip:** kaho "main pehle profile karta hoon: kaunsa step kitna waqt/memory le raha hai
(`perf_counter` + `memory_usage(deep=True)`), phir sirf sab se bara hissa fix karta hoon."
"""),
]
cells += [
md("""
## 2. Measurement toolkit — pehle maapo!

Teen cheezein maapni hoti hain:

| Kya | Tool | Kab |
|---|---|---|
| **Waqt** | `time.perf_counter()`, `timeit.timeit(..., globals=globals())` | har optimization se pehle/baad |
| **Memory (data ka size)** | `df.memory_usage(deep=True)`, `df.info(memory_usage='deep')` | dtype tuning |
| **Memory (peak allocation)** | `tracemalloc` | "operation ke dauran" RAM spike |

### `%%timeit` ka zikr
Jupyter me sab se aasan tareeqa `%%timeit` (cell magic) ya `%timeit` (line magic) hai:
```python
%timeit df["a"] * 2          # auto repeats, best-of report
%%timeit
df.groupby("g")["v"].mean()
```
Ye **IPython magics** hain — plain Python script me SyntaxError deti hain (aur ye notebook automated
runner se test hota hai), is liye hum neeche apna chhota `bench()` helper use karenge.
Interview me `%%timeit` ka naam lena zaroor — magar production script me `perf_counter` likho.

### `deep=True` kyun lazmi hai
`memory_usage()` bina `deep` sirf **pointer array** ka size deta hai (8 bytes per row).
Python strings ka asli payload heap me hai — wo sirf `deep=True` par count hota hai.
Yahi wajah hai ke log kehte hain "meri df sirf 8 MB hai" jab wo asal me 300 MB hoti hai.
"""),

code("""
# ============ bench(): chhota, dohraya ja sakne wala timing helper ============
BENCH_ROWS = []   # saare results yahan jama honge (aakhir me table print karenge)

def bench(label, fn, repeat=3, group=""):
    \"\"\"fn() ko `repeat` dafa chala kar BEHTAREEN (min) waqt return karta hai.

    min kyun, average kyun nahi? Kyun ke OS scheduling/GC sirf waqt BARHA sakta hai,
    ghata nahi sakta — is liye minimum asli lagat ka behtar andaza hai (timeit bhi yahi karta hai).
    \"\"\"
    best = float("inf")
    out = None
    for _ in range(repeat):
        t0 = time.perf_counter()
        out = fn()                       # asli kaam
        dt = time.perf_counter() - t0
        best = min(best, dt)
    BENCH_ROWS.append({"group": group, "method": label, "seconds": round(best, 6)})
    return out, best

def bench_table(group=None, baseline=None):
    \"\"\"Jama kiye hue results ko DataFrame table ki tarah print karta hai (+ speed-up ratio).\"\"\"
    t = pd.DataFrame(BENCH_ROWS)
    if group is not None:
        t = t[t["group"] == group].copy()
    t = t.sort_values("seconds").reset_index(drop=True)
    if len(t):
        fastest = t["seconds"].iloc[0]
        # 'x_slower' = ye tareeqa sab se tez tareeqe se kitna guna slow hai
        t["x_slower"] = (t["seconds"] / max(fastest, 1e-12)).round(1)
    return t

# Chhota sanity test
_, dt = bench("warmup: 1e6 numpy sum", lambda: np.arange(1_000_000).sum(), group="warmup")
print(f"warmup ho gaya: {dt:.5f} s")
print(bench_table("warmup").to_string(index=False))
"""),

code("""
# ============ memory_usage: shallow vs deep ka farq ============
n = 50_000
demo = pd.DataFrame({
    "id":   rng.integers(0, 10**6, n),                                   # int64
    "city": rng.choice(["Lahore", "Karachi", "Islamabad", "Multan"], n),  # text
    "amt":  rng.random(n) * 1000,                                        # float64
    "flag": rng.choice([True, False], n),                                # bool
})

shallow = demo.memory_usage(deep=False).sum()
deep    = demo.memory_usage(deep=True).sum()
print(f"rows            : {len(demo):,}")
print(f"shallow (deep=False): {shallow/1e6:8.3f} MB   <- text ka asli payload count NAHI hua")
print(f"deep    (deep=True) : {deep/1e6:8.3f} MB   <- ASLI RAM footprint")
print(f"farq            : {deep/shallow:.1f}x\\n")

# Per-column breakdown — yahi se pata chalta hai 'mujrim' kaunsa column hai
per_col = (demo.memory_usage(deep=True)
             .rename("bytes").to_frame()
             .assign(MB=lambda d: (d["bytes"] / 1e6).round(3),
                     dtype=[""] + [str(t) for t in demo.dtypes]))  # Index ki dtype khali
print(per_col.to_string())
"""),

code("""
# ============ df.info(memory_usage='deep') — ek nazar me sab kuch ============
buf = io.StringIO()                       # info() print karta hai; buf me capture kar lo
demo.info(buf=buf, memory_usage="deep")   # 'deep' likhna ZAROORI hai warna text under-count
print(buf.getvalue())

# ============ tracemalloc — operation ke dauran PEAK memory ============
tracemalloc.start()
tmp = demo.copy()                                  # jaan boojh kar ek copy (memory spike)
grouped = tmp.groupby("city", observed=True)["amt"].sum()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
print(f"tracemalloc -> current: {current/1e6:.2f} MB | peak: {peak/1e6:.2f} MB")
print("\\nSabaq: peak >= current. Aksar crash 'peak' par hota hai, final size par nahi —")
print("is liye pipeline me copies aur intermediate frames ginna zaroori hai.")
del tmp, grouped
"""),

md("""
### Output ka matlab (bohat ahem)

- `shallow` vs `deep` ka farq hi wo "chhipa hua" memory hai jo text columns me hoti hai.
- **`tracemalloc` ka `peak`** batata hai ke operation ke beech me RAM kahan tak gayi.
  Jab log kehte hain "8 GB RAM par 2 GB CSV crash kar gayi" — wajah yehi peak hoti hai
  (parse buffer + result + copy sab aik waqt me zinda hote hain).

**Gotchas**
- `memory_usage(deep=True)` khud thora slow hai (har string ka size ginta hai) — 100M rows par har
  cell me na chalao.
- `tracemalloc` sirf **Python-level** allocations trace karta hai; numpy ke bare buffers
  aksar Python allocator ke through aate hain, magar OS-level RSS ke liye `psutil` behtar hai
  (yahan install nahi hai — interview me naam le lena).

**Interview tip:** "How would you find which column is eating memory?" →
`df.memory_usage(deep=True).sort_values(ascending=False)`.
"""),
]
cells += [
md("""
## 3. Dtypes = memory ka steering wheel

pandas har column ko ek **typed array** ki tarah rakhta hai. Memory ka formula seedha hai:

```
column bytes  ≈  rows × bytes_per_value   (+ text ka heap payload)
```

| dtype | bytes/value | range / note |
|---|---|---|
| `int64` | 8 | ±9.2×10¹⁸ (default — aksar zaroorat se bara) |
| `int32` | 4 | ±2.1×10⁹ |
| `int16` | 2 | ±32,767 |
| `int8` | 1 | ±127 |
| `uint8` | 1 | 0..255 (sirf non-negative) |
| `float64` | 8 | default |
| `float32` | 4 | ~7 significant digits |
| `bool` | 1 | |
| `datetime64[us]` | 8 | pandas 3 ka default unit **us** hai (pehle `ns`) |
| `category` | 1-4 (codes) + ek dafa categories | kam unique values ke liye jadoo |
| python string (`str` dtype) | 8 (pointer) + ~50-80 per string | mehanga! |

**Usool:** pehle poocho *"is column ki asli range/cardinality kya hai?"* — dtype uske hisab se chuno.
"""),

code("""
# ============ Integer downcasting: 8 bytes se 1-4 bytes tak ============
ints = pd.Series(rng.integers(0, 200, 100_000))     # asli range sirf 0..199 hai!
print("original dtype :", ints.dtype, "| bytes:", ints.memory_usage(deep=True))

# Tareeqa 1: khud dtype chunna (jab range pehle se maloom ho)
as_u8 = ints.astype("uint8")        # 0..255 fit ho jata hai -> 1 byte per value
print("uint8   dtype  :", as_u8.dtype, "| bytes:", as_u8.memory_usage(deep=True))

# Tareeqa 2: pandas khud chun le -> pd.to_numeric(downcast=...)
auto_i = pd.to_numeric(ints, downcast="integer")    # signed me sab se chhota fit
auto_u = pd.to_numeric(ints, downcast="unsigned")   # non-negative ho to aur behtar
print("downcast integer :", auto_i.dtype)
print("downcast unsigned:", auto_u.dtype)

# Values badli to nahi? (lossless hona LAZMI hai)
assert (as_u8.astype("int64") == ints).all(), "downcast se value badalni nahi chahiye"
print(f"\\nsaving: {(1 - as_u8.memory_usage(deep=True)/ints.memory_usage(deep=True))*100:.1f}% "
      f"({ints.dtype} -> {as_u8.dtype})")

# np.iinfo se safe range check karne ka professional tareeqa
print("\\nuint8 range:", np.iinfo("uint8").min, "..", np.iinfo("uint8").max)
print("int16 range:", np.iinfo("int16").min, "..", np.iinfo("int16").max)
"""),

code("""
# ============ GOTCHA: andha downcast = silent overflow / precision loss ============
# 1) Integer overflow (numpy wrap kar deta hai ya error deta hai — dono soorat me data kharab)
big = pd.Series([10, 20, 300])          # 300 uint8 (max 255) me fit NAHI hota
try:
    bad = big.astype("uint8")          # pandas 3 me ye error deta hai (achhi baat)
    print("uint8 result:", bad.tolist(), "<- 300 kharab ho gaya!")
except Exception as e:
    print(f"[safe] astype('uint8') ne roka -> {type(e).__name__}: {e}")

# Isi liye pehle range CHECK karo, phir cast karo — reusable helper:
def safe_int_downcast(s: pd.Series) -> pd.Series:
    \"\"\"Sirf tab downcast karta hai jab min/max target dtype me fit ho.\"\"\"
    lo, hi = s.min(), s.max()
    kind = "unsigned" if lo >= 0 else "integer"
    out = pd.to_numeric(s, downcast=kind)
    assert (out.astype("int64") == s.astype("int64")).all()   # lossless proof
    return out

print("safe_int_downcast:", safe_int_downcast(big).dtype)

# 2) float32 = precision loss (paise/IDs par khatarnak)
f64 = pd.Series([0.1, 1/3, 123456789.123456])
f32 = f64.astype("float32")
print("\\nfloat64:", f64.tolist())
print("float32:", f32.tolist())
print("max abs error:", float((f64 - f32.astype('float64')).abs().max()))
print("\\nSabaq: analytics/features ke liye float32 theek; PAISE (money) ke liye float64 ya integer-paisa.")
"""),

md("""
### `category` — sab se bara aur sab se aasan memory win

`category` do hisson me data rakhta hai:
1. **categories** — unique values ka ek chhota array (ek dafa)
2. **codes** — har row ke liye chhota integer (`int8`/`int16`/`int32`) index

Faida = jab **unique values kam** hon aur **rows zyada**.

**Rule of thumb:** agar `nunique / len < 0.5` (aur practically `< 0.1` par to laazmi) → `category` socho.
Magar **rule se pehle measure karo** — neeche wahi kar rahe hain.
"""),

code("""
# ============ text -> category: asli measurement ============
city = demo["city"]                       # 4 unique values, 50k rows
cat  = city.astype("category")

b_before = city.memory_usage(deep=True)
b_after  = cat.memory_usage(deep=True)
print(f"dtype            : {city.dtype}  ->  {cat.dtype}")
print(f"memory (deep)    : {b_before/1e6:.3f} MB  ->  {b_after/1e6:.3f} MB")
print(f"saving           : {(1 - b_after/b_before)*100:.1f}%  ({b_before/b_after:.0f}x chhota)")
print(f"cardinality      : nunique={city.nunique()} / len={len(city)} = {city.nunique()/len(city):.5f}")
print(f"codes dtype      : {cat.cat.codes.dtype}   (isi liye itna chhota hai)")
print(f"categories       : {list(cat.cat.categories)}")

# ============ Kab category ULTA nuqsan deta hai ============
uniq = pd.Series([f"id-{i}" for i in range(50_000)])      # har value unique (cardinality = 1.0)
print(f"\\nunique-heavy column: {uniq.memory_usage(deep=True)/1e6:.3f} MB "
      f"-> category: {uniq.astype('category').memory_usage(deep=True)/1e6:.3f} MB")
print("Sabaq: high-cardinality (IDs, emails, free text) par category memory BARHA deti hai —")
print("kyun ke categories ka poora array + codes dono store hote hain.")
"""),

code("""
# ============ pandas 3 ka AHEM badlav: default string dtype ============
s = pd.Series(["Lahore", "Karachi", None])
print("pandas 3 me text ka default dtype :", s.dtype, f"({type(s.dtype).__name__})")
print("pandas 2 me hota tha              : object")

# Magar dhyan se: is machine par pyarrow nahi hai, is liye ye 'str' python-backed hai.
# Python-backed hone ka matlab: memory object jaisi hi rehti hai!
as_object = city.astype(object)
print(f"\\n'str'  dtype memory : {city.memory_usage(deep=True)/1e6:.3f} MB")
print(f"'object' dtype memory: {as_object.memory_usage(deep=True)/1e6:.3f} MB")
print("-> Dono barabar. Yaani naya default dtype API saaf karta hai (NaN ke bajaye proper NA),")
print("   lekin memory ka faida SIRF pyarrow-backed strings se milta hai.")

# astype('string') -> nullable StringDtype (kaam karta hai)
print("\\nastype('string') dtype:", city.astype("string").dtype)

# string[pyarrow] -> yahan pyarrow nahi hai, is liye guarded
try:
    arrow_str = city.astype("string[pyarrow]")
    print("string[pyarrow] memory:", arrow_str.memory_usage(deep=True)/1e6, "MB")
except Exception as e:
    print(f"\\n[skip] string[pyarrow] -> {type(e).__name__}: {str(e)[:70]}...")
    print("       pyarrow hota to: ~50-80% kam memory + 2-10x tez .str operations,")
    print("       kyun ke strings ek contiguous buffer me hote (per-string python object nahi).")
"""),
]
# --- END CHUNK 3 ---
