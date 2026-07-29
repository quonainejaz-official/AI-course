"""Generator: Pandas/Advance/01_MultiIndex_Advanced_Indexing_aur_Reshaping.ipynb"""

import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

CELLS = []
A = CELLS.append

A(md("""
# MultiIndex, Advanced Indexing aur Reshaping Mastery

**Level:** Advanced &nbsp;|&nbsp; **Folder:** `Pandas/Advance` &nbsp;|&nbsp; **pandas:** 3.0.5, **numpy:** 2.4.2, **Python:** 3.14

Ek DataFrame me jab **ek se zyada key** milkar row ko unique banati hai — country + city + month,
ya date + ticker, ya respondent + question — tab flat index kaam nahi deta. Wahan `MultiIndex`
aata hai. Ye notebook usi ka poora tour hai: banane se le kar select, reshape aur performance tak.

## Is notebook me kya seekhenge

- **MultiIndex kyun** — hierarchical data, groupby ka natija, panel data
- **Banane ke 5 tareeqe** — `from_tuples`, `from_arrays`, `from_product`, `set_index([...])`, groupby result
- **Anatomy** — `levels`, `codes`, `names`, `nlevels`, `get_level_values`
- **Lexsort depth** — `_lexsort_depth`, `is_monotonic_increasing`, `sortlevel`, aur asli **timing** ka farq
- **Selection mastery** — partial indexing, tuple keys, `slice(None)`, `pd.IndexSlice`, `xs()`, boolean masks
- **Column MultiIndex** — multi-agg `groupby().agg({...})`, `unstack`, columns flatten karna
- **Level surgery** — `droplevel`, `swaplevel`, `reorder_levels`, `rename_axis`, `set_names`, `sort_index(level=)`
- **Alignment** — `reindex(fill_value=)`, `align(join=)`, `combine_first` vs `update` vs `where`/`mask` (+ CoW)
- **Cross-section aggregation** — `groupby(level=)`, aur `df.sum(level=0)` jo pandas 3 me **hat gaya**
- **stack / unstack mastery** — multiple levels, NaN, `fill_value`, round-trip proof, pandas 3 ke naye rules
- **pivot vs pivot_table** — `aggfunc` dict, `margins=True`, duplicate keys ka error
- **wide_to_long, melt, crosstab**
- **Nested data** — `explode` (single + multi column), `pd.json_normalize(record_path=, meta=)`
- **Index vs column trade-off** — kab index banao, kab na banao (timing ke sath)
- **Index types tour** — `RangeIndex`, `DatetimeIndex`, `CategoricalIndex`, `IntervalIndex`, `PeriodIndex`
- **Memory** — MultiIndex vs flat columns `memory_usage(deep=True)`
- **5 Real-World Problems**, **Common Mistakes**, **4 LeetCode problems (pandas + SQL)**,
  **16 Interview Q&A**, **8 Practice Exercises**, aur **Cheat-sheet**

## Prerequisites

- Pandas basics: `DataFrame`, `Series`, `.loc` / `.iloc`, `groupby`, `merge`
- Numpy arrays ka basic idea
- Is notebook me **koi external file nahi** — saara data inline banta hai (`default_rng`, `io.StringIO`, `sqlite3`)

> **Note:** Ye notebook top-se-neeche chalta hai (shared namespace). Cells ko order me chalao.
> Koi IPython magic (`%timeit`) use nahi hui — plain `time.perf_counter()` se timing li gayi hai.
"""))

A(md("""
## 0. Setup — imports aur ek chhota helper

`to_markdown()` is environment me kaam **nahi** karta (`tabulate` install nahi hai), is liye
apna chhota `md_table()` helper bana rahe hain. Tables ke liye `to_string()` bhi bilkul theek hai.
"""))

A(code('''
import io
import json
import sqlite3
import time
import warnings

import numpy as np
import pandas as pd

SEED = 42                                  # har jagah same seed -> deterministic output
rng = np.random.default_rng(SEED)          # numpy ka naya (recommended) random generator

pd.set_option("display.width", 110)        # wide output thoda tidy dikhe
pd.set_option("display.max_rows", 24)      # bohat lambi tables se bachne ke liye


def md_table(d):
    """DataFrame ko markdown table string banata hai (to_markdown ka substitute)."""
    cols = list(d.columns)                                                   # column names
    head = "| " + " | ".join(map(str, cols)) + " |"                          # header row
    sep = "|" + "|".join("---" for _ in cols) + "|"                          # separator row
    rows = ["| " + " | ".join(map(str, r)) + " |"                            # data rows
            for r in d.itertuples(index=False)]
    return "\\n".join([head, sep] + rows)


print("pandas :", pd.__version__)          # 3.0.5 expected
print("numpy  :", np.__version__)          # 2.4.2 expected
print("CoW ON :", pd.get_option("mode.copy_on_write"))   # pandas 3 me default True
'''))

A(md("""
## 1. MultiIndex kyun? (Kya hai → Kyun)

**Kya hai:** `MultiIndex` (hierarchical index) ek aisa index hai jis me **ek se zyada level** hote
hain. Har row ka "address" ek single value nahi, balke ek **tuple** hota hai — jaise
`("Pakistan", "Lahore", "2024-01")`.

**Kyun / kahan use hota hai:**

1. **Hierarchical / nested data** — country → city → month. Natural tree ko table me daalna.
2. **groupby ka natija** — `df.groupby(["a", "b"]).sum()` khud hi MultiIndex return karta hai.
   Yani agar tum groupby use karte ho, tum **pehle se** MultiIndex use kar rahe ho.
3. **Panel data** — (date × ticker) returns, (respondent × question) survey. 2-D key, 1 value column.
4. **Fast aligned lookups** — sorted MultiIndex par binary search chalti hai; automatic alignment
   arithmetic ko sahi rakhti hai.

**Output ka matlab (neeche):** flat version me `country` aur `city` **repeat** ho rahe hain aur
row ki identity implicit hai. MultiIndex version me wahi cheez index me chali gayi — repetition
display se hat gaya aur `sales` ek saaf 1-column frame ban gaya jise hum level-wise slice kar sakte hain.

**Interview tip:** "MultiIndex kab use karoge?" ka best jawab — *jab keys ka combination row ko
identify karta ho aur tum us hierarchy par slice/aggregate karna chahte ho*. Sirf data rakhne ke
liye MultiIndex mat banao.
"""))

A(code('''
# Flat ("tidy") shakal — keys normal columns me hain
flat = pd.DataFrame({
    "country": ["PK", "PK", "PK", "PK", "IN", "IN", "IN", "IN"],
    "city":    ["Lahore", "Lahore", "Karachi", "Karachi", "Delhi", "Delhi", "Mumbai", "Mumbai"],
    "month":   ["2024-01", "2024-02"] * 4,
    "sales":   [120, 135, 200, 190, 300, 310, 280, 295],
})
print("FLAT (keys columns me):")
print(flat.to_string(index=False))          # index=False -> 0..7 wala shor hat jaye

# Wahi data hierarchical shakal me — 3 columns index bana diye
hier = flat.set_index(["country", "city", "month"]).sort_index()
print("\\nHIERARCHICAL (keys index me):")
print(hier.to_string())

print("\\nindex ka type :", type(hier.index).__name__)   # MultiIndex
print("nlevels        :", hier.index.nlevels)            # 3 levels
print("shape          :", hier.shape)                    # 8 rows, sirf 1 column (sales)
'''))

A(md("""
## 2. MultiIndex banane ke tareeqe (Syntax + Example)

Paanch raste hain, har ek ka apna mauqa:

| tareeqa | kab |
|---|---|
| `pd.MultiIndex.from_tuples(list_of_tuples)` | tumhare paas already row-wise tuples hain |
| `pd.MultiIndex.from_arrays([arr1, arr2])` | har level ki poori column alag list me hai |
| `pd.MultiIndex.from_product([l1, l2])` | **cartesian product** chahiye (complete grid) |
| `df.set_index([...])` | data already DataFrame me hai (sab se aam) |
| `df.groupby([...]).agg(...)` | natija khud MultiIndex ho kar aata hai |

**Gotcha:** `from_product` **saare** combinations banata hai — 3 countries × 12 months = 36 rows,
chahe data me sirf 20 mojood hon. Ye *feature* hai (missing combos expose karne ke liye), magar
galti se bara grid bana dena easy hai.

**Interview tip:** `from_product` ka classic use — panel ko **complete grid** par `reindex` karna
taake missing (country, month) combos NaN ki shakal me nazar aa jayein.
"""))

A(code('''
# --- 1) from_tuples: row-wise tuples ---
tuples = [("PK", "Lahore"), ("PK", "Karachi"), ("IN", "Delhi"), ("IN", "Mumbai")]
mi_tuples = pd.MultiIndex.from_tuples(tuples, names=["country", "city"])  # names dena best practice
print("from_tuples:")
print(mi_tuples)

# --- 2) from_arrays: har level ki alag list ---
mi_arrays = pd.MultiIndex.from_arrays(
    [["PK", "PK", "IN", "IN"], ["Lahore", "Karachi", "Delhi", "Mumbai"]],  # level 0, level 1
    names=["country", "city"],
)
print("\\nfrom_arrays == from_tuples ?", mi_arrays.equals(mi_tuples))      # dono barabar hain

# --- 3) from_product: cartesian product (complete grid) ---
mi_prod = pd.MultiIndex.from_product(
    [["PK", "IN"], ["2024-01", "2024-02", "2024-03"]],                     # 2 x 3 = 6 combos
    names=["country", "month"],
)
print("\\nfrom_product ->", len(mi_prod), "rows (2 x 3 = complete grid)")
print(mi_prod.tolist())
'''))

A(code('''
# --- 4) set_index([...]) : sab se aam tareeqa ---
sales = pd.DataFrame({
    "country": ["PK", "PK", "IN", "IN", "PK", "IN"],
    "city":    ["Lahore", "Karachi", "Delhi", "Mumbai", "Lahore", "Delhi"],
    "month":   ["2024-01", "2024-01", "2024-01", "2024-01", "2024-02", "2024-02"],
    "units":   [10, 20, 30, 40, 15, 35],
    "revenue": [100, 220, 330, 440, 160, 370],
})
idx2 = sales.set_index(["country", "city"])            # 2 columns -> 2-level MultiIndex
print("set_index(['country','city']) ->", type(idx2.index).__name__, "| nlevels =", idx2.index.nlevels)

# drop=False rakho to columns index me AUR column me dono jagah reh jati hain
keep_both = sales.set_index(["country", "city"], drop=False)
print("drop=False ke baad columns:", list(keep_both.columns))   # country/city columns me bhi maujood

# --- 5) groupby ka natija = MultiIndex (ye sab se zyada baar milta hai) ---
g = sales.groupby(["country", "month"])[["units", "revenue"]].sum()
print("\\ngroupby(['country','month']).sum() ka index type:", type(g.index).__name__)
print(g.to_string())
print("\\nindex.names ->", g.index.names)               # groupby keys automatically names ban gaye
'''))

A(md("""
## 3. Anatomy — `levels`, `codes`, `names`, `get_level_values`

**Kya hai:** MultiIndex andar se **do cheezon** ka jorr hai (memory bachane ka trick):

- `levels` — har level ki **unique** values (chhoti lookup table, sorted)
- `codes` — har row ke liye us lookup table me **integer position** (`-1` = missing)

Yani `"Lahore"` string 50,000 baar store nahi hoti — sirf ek dafa `levels` me, aur baaki jagah
uska chhota integer code. Ye exactly `Categorical` ka idea hai.

**Syntax:**

```python
mi.levels              # FrozenList of Index objects
mi.codes               # FrozenList of integer arrays
mi.names               # level ke naam
mi.nlevels             # kitne levels
mi.get_level_values(0) # ek level ki POORI (repeated) values, row-count ke barabar
```

**Output ka matlab:** `levels[1]` me sirf unique cities aayengi (sorted), jabke
`get_level_values("city")` me har row ke liye value aayegi — length = `len(df)`.

**Gotcha (bara wala):** `levels` me woh values bhi **reh jati hain** jo filter ke baad data me
nahi bachi. Yani filter karne se `levels` khud-ba-khud saaf nahi hoti → `remove_unused_levels()`
chalao. Ye groupby/unstack me "ghost rows" ki sab se aam wajah hai.

**Interview tip:** "MultiIndex memory-efficient kyun hai?" → *levels + codes (dictionary encoding);
strings ek hi dafa store hoti hain, rows me sirf int codes.*
"""))

A(code('''
mi = idx2.index                                  # (country, city) wala 2-level index

print("names            :", mi.names)            # ['country', 'city']
print("nlevels          :", mi.nlevels)          # 2
print("levels[0]        :", mi.levels[0].tolist())   # unique countries (sorted)
print("levels[1]        :", mi.levels[1].tolist())   # unique cities (sorted)
print("codes[0]         :", mi.codes[0].tolist())    # har row ka country ka integer code
print("codes[1]         :", mi.codes[1].tolist())    # har row ka city ka integer code

# get_level_values = poori (repeat hone wali) values, length == len(df)
print("\\nget_level_values('country'):", mi.get_level_values("country").tolist())
print("get_level_values(1)          :", mi.get_level_values(1).tolist())
print("len(df) == len(get_level_values) ?", len(idx2) == len(mi.get_level_values(0)))

# codes + levels se original value reconstruct karna (andar yehi hota hai)
row0 = (mi.levels[0][mi.codes[0][0]], mi.levels[1][mi.codes[1][0]])
print("\\nrow 0 reconstructed from codes+levels:", row0)
'''))

A(code('''
# GOTCHA: filter karne ke baad bhi purani levels zinda rehti hain
small = idx2.loc[["PK"]]                                   # sirf PK wali rows rakhi
print("filter ke baad rows           :", len(small))
print("levels[1] (cities) ab bhi     :", small.index.levels[1].tolist())   # Delhi/Mumbai bhi maujood!

# Iska asli nuqsaan: groupby/unstack me khaali "ghost" categories aa jati hain
print("\\nghost rows ke sath unstack:")
print(small["units"].unstack("city").to_string())          # Delhi/Mumbai columns NaN ke sath

# Ilaaj: remove_unused_levels()
cleaned = small.copy()
cleaned.index = cleaned.index.remove_unused_levels()       # ab levels sirf bachi values par
print("\\nremove_unused_levels ke baad :", cleaned.index.levels[1].tolist())
print("saaf unstack:")
print(cleaned["units"].unstack("city").to_string())
'''))

A(md("""
## 4. Lexsort depth — sorted MultiIndex kyun zaroori hai

**Kya hai:** MultiIndex par slicing tab tez (aur kabhi kabhi tab *possible*) hoti hai jab index
**lexicographically sorted** ho. `_lexsort_depth` batata hai ke shuru se **kitne levels** sorted hain:

- `0` → kuch bhi sorted nahi
- `2` → pehle 2 levels sorted hain

`_lexsort_depth` **private** API hai (underscore se shuru) — yani pandas guarantee nahi deta ke ye
future me rahega. Teaching/debugging ke liye theek hai, **production code me na use karo**;
wahan `index.is_monotonic_increasing` par bharosa karo.

**pandas 3.0.5 ka verified behaviour (ahem):** unsorted MultiIndex par slicing par
`PerformanceWarning` **actually emit nahi hoti** (purane versions me hoti thi). Warning class
`pd.errors.PerformanceWarning` ab bhi maujood hai. Is liye hum warning par bharosa **nahi** karenge —
neeche `time.perf_counter()` se **asli cost** naapenge.

**Syntax:**

```python
df.index.is_monotonic_increasing     # public, isi ko use karo
df.index._lexsort_depth              # private, sirf samajhne ke liye
df.sort_index()                      # ilaaj
df.index.sortlevel(0)                # (sorted_index, indexer) tuple deta hai
```

**Gotcha:** `slice(...)` ke sath unsorted index par slice karne par pandas
`UnsortedIndexError` (jo `KeyError` ka subclass hai) bhi de sakta hai — yani ye sirf speed ka
masla nahi, **correctness/error** ka bhi ho sakta hai.

**Interview tip:** "MultiIndex slicing slow kyun hai?" → *lexsort depth kam hai; pandas binary
search nahi kar sakta, poora scan karta hai. `sort_index()` ek dafa karo, phir saare lookups tez.*
"""))

A(code('''
# Ek maqsad se UNSORTED MultiIndex banate hain
raw = pd.DataFrame({
    "grp": ["b", "a", "b", "a", "c", "a"],
    "sub": [2, 2, 1, 1, 1, 3],
    "val": [10, 20, 30, 40, 50, 60],
})
uns = raw.set_index(["grp", "sub"])                  # jaisa data tha waisa hi -> unsorted
srt = uns.sort_index()                               # lexicographically sorted version

print("UNSORTED index:", uns.index.tolist())
print("  is_monotonic_increasing :", uns.index.is_monotonic_increasing)
print("  _lexsort_depth (private):", uns.index._lexsort_depth)      # 0 expected

print("\\nSORTED index  :", srt.index.tolist())
print("  is_monotonic_increasing :", srt.index.is_monotonic_increasing)
print("  _lexsort_depth (private):", srt.index._lexsort_depth)      # 2 expected

print("\\nPerformanceWarning class maujood hai:", pd.errors.PerformanceWarning.__name__)
'''))

A(code('''
# sortlevel(): (sorted_index, indexer) tuple return karta hai
sorted_idx, indexer = uns.index.sortlevel(0)         # level 0 par sort
print("sortlevel(0) -> sorted index:", sorted_idx.tolist())
print("sortlevel(0) -> indexer     :", indexer.tolist())   # original positions ka order

# Level 1 par sort karna ho to level= do
by_sub, _ = uns.index.sortlevel(1)
print("\\nsortlevel(1) (sub par pehle):", by_sub.tolist())

# GOTCHA: unsorted index par slice(...) error de sakta hai
try:
    out = uns.loc[("a", slice(None)), :]              # slice ke sath partial key
    print("\\nunsorted slice chal gaya, rows =", len(out))
except Exception as e:
    print("\\nunsorted slice FAIL ->", type(e).__name__, ":", str(e)[:90])

# Sorted par wahi cheez bila masla chalti hai
print("sorted slice rows =", len(srt.loc[("a", slice(None)), :]))
'''))

A(code('''
# ASLI COST: sorted vs unsorted lookup ka timing (koi assert nahi, sirf print)
n = 60_000                                                    # 60k rows = halka aur maani-khez
keys_a = rng.integers(0, 500, n)                              # level 0: 500 unique
keys_b = rng.integers(0, 120, n)                              # level 1: 120 unique
big = pd.DataFrame({"a": keys_a, "b": keys_b, "v": rng.normal(size=n)}).set_index(["a", "b"])

big_uns = big                                                 # random order -> unsorted
big_srt = big.sort_index()                                    # sorted copy
print("unsorted _lexsort_depth:", big_uns.index._lexsort_depth,
      "| sorted _lexsort_depth:", big_srt.index._lexsort_depth)

probe = rng.integers(0, 500, 200)                             # 200 lookups karenge


def timed_lookup(frame):
    """200 partial lookups ka total waqt (seconds) return karta hai."""
    t0 = time.perf_counter()                                  # start
    for k in probe:
        _ = frame.loc[k]                                      # level-0 partial lookup
    return time.perf_counter() - t0                           # elapsed


t_uns = timed_lookup(big_uns)                                 # unsorted par
t_srt = timed_lookup(big_srt)                                 # sorted par
print(f"\\n200 partial lookups | unsorted: {t_uns:.4f}s | sorted: {t_srt:.4f}s")
print(f"sorted index takreeban {t_uns / max(t_srt, 1e-9):.1f}x tez raha (machine par farq mumkin)")
print("\\nSabaq: MultiIndex banane ke FAURAN BAAD ek dafa sort_index() kar lo.")
'''))

A(md("""
## 5. Selection Mastery — `.loc`, tuples, `slice(None)`, `IndexSlice`, `xs`

Yahan log sab se zyada phaste hain. Zehen me ek asool rakho:

> **MultiIndex par `.loc` ka first argument row-key hai, aur tuple = "levels ke aar-paar ek address"**,
> jabke list = "isi level me kai values".

| kaam | code |
|---|---|
| poora outer group | `df.loc["a"]` (level 0 **gir jata hai**) |
| exact 2-level address | `df.loc[("a", 1)]` |
| level 0 fix, level 1 sab | `df.loc[("a", slice(None)), :]` |
| readable slicing | `df.loc[pd.IndexSlice["a", 1:3], :]` |
| kai exact addresses | `df.loc[[("a", 1), ("b", 2)]]` |
| kisi bhi level par cross-section | `df.xs(1, level="sub")` |
| custom condition | `df[df.index.get_level_values("sub") > 1]` |

**Sab se aham farq:** `df.loc["a"]` level 0 ko **drop** kar deta hai (kyunki wo constant ho gaya),
magar `df.loc[["a"]]` (list) level ko **rakhta** hai. Ye chhota `[]` bara farq daalta hai.

**Gotcha:** `df.loc["a", 1]` ko pandas **`(row="a", column=1)`** samajh sakta hai, na ke
2-level row key! Ambiguity se bachne ke liye row-key ko **tuple** me lapeto aur columns ke liye
doosra argument do: `df.loc[("a", 1), :]`.

**Interview tip:** `xs` vs `.loc` → *`xs` tab jab tumhein **beech ke** ya kisi bhi named level par
slice karna ho bina aage ke levels ko `slice(None)` se bharne ke; `.loc` (+ `IndexSlice`) tab jab
multiple levels par ek sath aur columns ke sath slice karna ho. `xs` read-only style hai —
uss se assignment na karo.*
"""))

A(code('''
# Kaam ke liye ek saaf sorted 2-level frame
demo = pd.DataFrame({
    "grp": ["a", "a", "a", "b", "b", "c"],
    "sub": [1, 2, 3, 1, 2, 1],
    "val": [10, 20, 30, 40, 50, 60],
    "qty": [1, 2, 3, 4, 5, 6],
}).set_index(["grp", "sub"]).sort_index()
print(demo.to_string())

# 1) Partial indexing: level 0 ki poori branch -> level 0 GIR jata hai
print("\\ndemo.loc['a']  (level 0 drop ho gaya):")
print(demo.loc["a"].to_string())
print("index ab:", demo.loc["a"].index.name)      # 'sub' -- single level bacha

# 2) List do to level BACHA rehta hai (bohat ahem farq)
print("\\ndemo.loc[['a']] (level 0 bacha hua hai):")
print(demo.loc[["a"]].to_string())
print("nlevels:", demo.loc[["a"]].index.nlevels)  # 2
'''))

A(code('''
# 3) Exact address = tuple -> ek row (Series ban jati hai)
print("demo.loc[('a', 2)] -> Series:")
print(demo.loc[("a", 2)])
print("type:", type(demo.loc[("a", 2)]).__name__)

# 4) Ek cell: tuple row-key + column name
print("\\ndemo.loc[('a', 2), 'val'] =", demo.loc[("a", 2), "val"])

# 5) GOTCHA: .loc['a', 1] ambiguous hai -- pandas ise (row='a', col=1) samajh sakta hai
try:
    print("\\ndemo.loc['a', 1] ->", demo.loc["a", 1])
except Exception as e:
    print("\\ndemo.loc['a', 1] FAIL ->", type(e).__name__, ":", str(e)[:80])
    print("Sabaq: row-key ko tuple me lapeto -> demo.loc[('a', 1), :]")
print("safe version demo.loc[('a', 1), :] ->", demo.loc[("a", 1), :].to_dict())
'''))

A(code('''
# 6) slice(None) = "is level ki saari values" (yehi ':' ka programmatic roop hai)
print("level 0 sab, sub == 1 wali rows:")
print(demo.loc[(slice(None), 1), :].to_string())

# 7) Range slicing: 'a' se 'b' tak, sub 1 se 2 tak
print("\\ngrp 'a'..'b', sub 1..2:")
print(demo.loc[("a":= "a", slice(1, 2)), :].to_string() if False else
      demo.loc[(slice("a", "b"), slice(1, 2)), :].to_string())

# 8) pd.IndexSlice -> wahi cheez, magar ':' ke sath readable
idx = pd.IndexSlice                                   # convention: chhota naam
print("\\nIndexSlice se (zyada readable):")
print(demo.loc[idx[:, 1], :].to_string())              # sab grp, sub == 1
print("\\nIndexSlice range 'a':'b', sub 1:2 :")
print(demo.loc[idx["a":"b", 1:2], :].to_string())      # NOTE: label slicing INCLUSIVE hoti hai
print("\\nYaad rakho: label-based slice me dono ends SHAMIL hote hain (1:2 -> 1 aur 2 dono).")
'''))

A(code('''
# 9) Kai exact addresses ek sath -> list of tuples
picks = [("a", 1), ("b", 2), ("c", 1)]
print("demo.loc[list_of_tuples]:")
print(demo.loc[picks].to_string())

# 10) xs(): kisi bhi level par cross-section
print("\\nxs(1, level='sub')  -> har grp ki sub==1 wali row:")
print(demo.xs(1, level="sub").to_string())             # 'sub' level drop ho gaya

print("\\nxs(1, level='sub', drop_level=False) -> level bacha liya:")
print(demo.xs(1, level="sub", drop_level=False).to_string())

print("\\nxs('a') -> level 0 par cross-section (loc['a'] jaisa):")
print(demo.xs("a").to_string())

print("\\nxs(('a', 2)) -> poora address:")
print(demo.xs(("a", 2)).to_dict())
'''))

A(code('''
# 11) Boolean masks: get_level_values se banao -> sab se flexible tareeqa
subs = demo.index.get_level_values("sub")              # har row ka sub (length == len(df))
mask = (subs >= 2) & (demo["val"] > 20)                # index-condition + column-condition mila kar
print("mask (sub>=2 AND val>20):")
print(demo[mask].to_string())

# Kai values ke liye isin() -- IndexSlice se zyada saaf jab list dynamic ho
grps = demo.index.get_level_values("grp")
print("\\ngrp in ('a','c'):")
print(demo[grps.isin(["a", "c"])].to_string())

# Faida: mask ko index sorted hone ki zaroorat NAHI (magar ye poora scan karta hai -> O(n))
print("\\nMask O(n) scan hai; sorted index par .loc binary search karta hai.")
print("Chhote data par mask theek, bare data par sorted .loc behtar.")
'''))

A(md("""
### Gotcha: `.at` aur MultiIndex

`.at` scalar (ek single cell) ke fast access ke liye hai. MultiIndex ke sath iska behaviour
**version-dependent** raha hai, is liye hum ise `try/except` me chala kar **asli natija** print
karte hain.

**Is environment (pandas 3.0.5) me verified:**

- `df.at[("a", 1), "val"]` — **chalta hai** (poora tuple address diya to theek)
- `df.at["a", "val"]` — **`KeyError`** (partial key `.at` ke sath allowed nahi)

Yani asli gotcha ye nahi ke `.at` MultiIndex par mana hai; asli gotcha ye hai ke `.at` **sirf poora
exact address** leta hai — partial key, slice, ya list bilkul nahi.

**Interview tip:** `.at` ko sirf tab use karo jab loop me single cells parh rahe ho aur poora tuple
address maujood ho; warna `.loc` hi use karo — thoda slow, magar bohat zyada forgiving.
"""))

A(code('''
# .at ke teen scenarios -- har ek try/except me, asli natija dekhte hain
cases = [
    ("df.at[('a', 2), 'val']  (poora tuple)", lambda: demo.at[("a", 2), "val"]),
    ("df.at['a', 'val']       (partial key)", lambda: demo.at["a", "val"]),
    ("df['val'].at[('a', 2)]  (Series par)  ", lambda: demo["val"].at[("a", 2)]),
]
for label, fn in cases:
    try:
        print(f"{label} -> {fn()}")                    # chal gaya to value
    except Exception as e:
        print(f"{label} -> {type(e).__name__}: {str(e)[:60]}")   # warna error ka naam

print("\\nNateeja: poora tuple address kaam karta hai, partial key KeyError deti hai.")
'''))

A(md("""
## 6. Column MultiIndex — jab hierarchy columns me ho

**Kya hai:** MultiIndex sirf rows ke liye nahi — **columns** bhi hierarchical ho sakte hain
(`df.columns` bhi ek `MultiIndex` ho sakta hai).

**Kahan khud-ba-khud ban jata hai:**

1. Multi-aggregation: `df.groupby("k").agg({"x": ["sum", "mean"], "y": "max"})`
   → columns ban jate hain `("x","sum")`, `("x","mean")`, `("y","max")`
2. `unstack()` — jo level rows se columns me jata hai wo column level ban jata hai
3. `pivot_table` with multiple `values` + `columns`

**Selection ke do tareeqe:**

- `df["x"]` → **poora outer block** (sub-DataFrame), phir `df["x"]["sum"]`  ← *2 lookups (chained)*
- `df[("x", "sum")]` → **ek hi dafa** exact column  ← *behtar, ye prefer karo*

**Gotcha:** `df["x"]["sum"]` chained lookup hai. Read ke liye theek, magar **assignment** ke liye
kabhi na karo — Copy-on-Write (pandas 3 me default ON) me ye **chup-chaap no-op** ho jata hai.
Assignment ke liye hamesha `df[("x", "sum")] = ...` ya `df.loc[:, ("x","sum")] = ...`.

**Interview tip:** downstream tools (CSV export, plotting libs, `merge`) ko column MultiIndex pasand
nahi. Reshape ke fauran baad columns **flatten** kar do:
`df.columns = ["_".join(c) for c in df.columns]`.
"""))

A(code('''
# 1) Multi-agg se column MultiIndex banta hai
agg = sales.groupby("country").agg({
    "units":   ["sum", "mean"],       # ek column par 2 aggregations
    "revenue": ["sum", "max"],
})
print("groupby().agg(dict) ka natija -- columns MultiIndex hain:")
print(agg.to_string())
print("\\ncolumns.nlevels :", agg.columns.nlevels)
print("columns.tolist() :", agg.columns.tolist())      # tuples ki list

# 2) Selection: outer block vs exact column
print("\\nagg['units'] -> poora outer block (DataFrame):")
print(agg["units"].to_string())
print("\\nagg[('units','sum')] -> ek column (Series), EK lookup:")
print(agg[("units", "sum")].to_string())
print("\\ndono barabar ?", agg["units"]["sum"].equals(agg[("units", "sum")]))
'''))

A(code('''
# 3) Columns flatten karna -- reshape ke baad ka standard step
flat_cols = agg.copy()
flat_cols.columns = ["_".join(c) for c in flat_cols.columns]     # ('units','sum') -> 'units_sum'
print("flatten ke baad columns:", list(flat_cols.columns))
print(flat_cols.to_string())

# Agar kuch levels khaali ho sakte hain to strip() lagana behtar hai
mixed = sales.groupby("country").agg(units_sum=("units", "sum"))  # named agg -> flat columns direct!
print("\\nNamed aggregation (BEHTAR): columns pehle se flat aate hain")
print(mixed.to_string())
print("columns:", list(mixed.columns))

# 4) xs columns par bhi chalta hai (axis=1)
print("\\nagg.xs('sum', level=1, axis=1) -> har column ka 'sum' wala hissa:")
print(agg.xs("sum", level=1, axis=1).to_string())
'''))

A(code('''
# 5) CoW gotcha: chained assignment column MultiIndex par chup-chaap fail hota hai
demo_cow = agg.copy()
before = demo_cow[("units", "sum")].iloc[0]                      # pehle ki value

with warnings.catch_warnings(record=True) as caught:             # warnings pakar lete hain
    warnings.simplefilter("always")
    demo_cow["units"]["sum"].iloc[0] = 99999                     # chained -> GALAT tareeqa
    cats = [w.category.__name__ for w in caught]

after = demo_cow[("units", "sum")].iloc[0]                       # baad ki value
print("chained assignment se pehle :", before)
print("chained assignment ke baad  :", after)
print("value badli ?", before != after, "| warnings:", cats or "koi nahi")
print("-> Copy-on-Write me chained assignment CHUP-CHAAP no-op hai. Sab se khatarnak bug.")

# Sahi tareeqa: ek hi indexing operation
demo_cow.loc[demo_cow.index[0], ("units", "sum")] = 99999        # SAHI
print("\\n.loc se sahi assignment ke baad:", demo_cow[("units", "sum")].iloc[0])
'''))

A(md("""
## 7. Level surgery — `droplevel`, `swaplevel`, `reorder_levels`, naam badalna, sort

**Kya hai:** Ye woh tools hain jin se tum index ke levels ko **hataate, aage-peeche karte aur
rename** karte ho — bina data ko dobara banane ke.

| kaam | code |
|---|---|
| ek level hatao | `df.droplevel("sub")` / `df.droplevel(0, axis=1)` |
| do levels ki jagah badlo | `df.swaplevel("grp", "sub")` (ya `swaplevel(0, 1)`) |
| poora naya order do | `df.reorder_levels(["sub", "grp"])` |
| axis ka naam set karo | `df.rename_axis(index=["G", "S"])` |
| index ke naam badlo | `df.index = df.index.set_names([...])` |
| level-wise sort | `df.sort_index(level="sub", ascending=[True])` |
| sirf kuch levels wapas column banao | `df.reset_index(level="sub")` |

**Sab se bara gotcha:** `swaplevel` / `reorder_levels` ke baad index **dobara unsorted** ho jata hai
(`_lexsort_depth` 0 par gir jata hai). Is liye **hamesha** `swaplevel(...).sort_index()` chalao —
warna aage ki slicing slow ya error ban jayegi.

**Interview tip:** `reset_index(level="sub")` sirf **ek** level ko column banata hai, baaki index me
rehte hain — jab tumhein "ek key par groupby karna hai magar doosri index me hi chahiye" tab bohat
kaam ka hai.
"""))

A(code('''
print("Original (grp, sub):")
print(demo.to_string())

# 1) swaplevel -> (sub, grp)
sw = demo.swaplevel("grp", "sub")
print("\\nswaplevel('grp','sub') ke baad:")
print(sw.to_string())
print("_lexsort_depth ab:", sw.index._lexsort_depth, "  <-- 0! sort tut gaya")

# Is liye hamesha sort_index() lagao
sw_sorted = demo.swaplevel("grp", "sub").sort_index()
print("\\nswaplevel(...).sort_index() ke baad _lexsort_depth:", sw_sorted.index._lexsort_depth)
print(sw_sorted.to_string())

# 2) reorder_levels -> poora naya order (3+ levels par zyada kaam aata hai)
three = hier.copy()                                             # (country, city, month)
ro = three.reorder_levels(["month", "country", "city"]).sort_index()
print("\\nreorder_levels(['month','country','city']):")
print(ro.head(4).to_string())
'''))

A(code('''
# 3) droplevel -- rows se aur columns se
print("droplevel('sub') -> sirf grp bacha (duplicate index ban sakta hai!):")
print(demo.droplevel("sub").to_string())
print("index unique hai ?", demo.droplevel("sub").index.is_unique)   # False -> khayal rakho

print("\\ncolumns par droplevel(1, axis=1) -> agg ka doosra column level hata:")
print(agg.droplevel(1, axis=1).to_string())
print("columns ab:", list(agg.droplevel(1, axis=1).columns), " <-- duplicate names!")

# 4) rename_axis / set_names
renamed = demo.rename_axis(index=["GROUP", "SUBID"])            # naye axis names
print("\\nrename_axis ke baad names:", renamed.index.names)

renamed2 = demo.copy()
renamed2.index = renamed2.index.set_names(["G", "S"])           # index object par seedha
print("set_names ke baad names   :", renamed2.index.names)

# Sirf ek level ka naam badalna ho to level= do
one = demo.copy()
one.index = one.index.set_names("SUB_ONLY", level=1)
print("sirf level 1 ka naam badla :", one.index.names)
'''))

A(code('''
# 5) sort_index(level=, ascending=[...]) -- per-level direction
multi_sort = demo.sort_index(level=["grp", "sub"], ascending=[True, False])
print("grp ASC, sub DESC:")
print(multi_sort.to_string())

# Sirf doosre level par sort (level 0 ka order barbaad ho jata hai)
print("\\nsort_index(level='sub') -- sub par sort:")
print(demo.sort_index(level="sub").to_string())

# 6) reset_index(level=) -- sirf chuni hui levels wapas columns me
partial_reset = demo.reset_index(level="sub")
print("\\nreset_index(level='sub'):")
print(partial_reset.to_string())
print("index ab:", partial_reset.index.name, "| columns:", list(partial_reset.columns))

# drop=True do to level column banne ke bajaye GHAYAB ho jata hai
print("\\nreset_index(level='sub', drop=True) -> sub column bana hi nahi:")
print(demo.reset_index(level="sub", drop=True).to_string())
'''))

# --- END ---

