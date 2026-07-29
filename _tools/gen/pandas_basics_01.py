import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

cells = []

# ============================================================
# TITLE + ROADMAP
# ============================================================
cells.append(md("""
# 01 — Pandas Introduction: Series aur DataFrame

**Level:** Beginner (zero se shuru)
**Series:** Pandas Basics
**Environment:** Python 3.14, pandas 3.0, numpy 2.4

## Is notebook me kya seekhenge (roadmap)

1. pandas kya hai aur data analysis me kyun lazmi hai
2. numpy se rishta — pandas numpy ke upar kyun bana
3. Excel se comparison, SQL se comparison
4. install / import convention aur version check
5. **Series** — labeled 1D array: banane ke 5 tareeqe, index, `name`, `dtype`
6. `values` vs `.array` vs `.to_numpy()` ka farq
7. Series par vectorized operations
8. **Index alignment** — 2 Series jama karne par NaN kyun aata hai (bara interview point)
9. Series vs list vs numpy array vs dict — kab kaunsa
10. **DataFrame** — labeled 2D table: banane ke 7 tareeqe
11. `columns` aur `index` objects (Index immutable kyun hai)
12. `dtypes` — int64/float64/**str**/bool/datetime64/category + nullable dtypes (`Int64`, `boolean`, `string`)
13. Inspection toolkit — `head/tail/sample/shape/size/ndim/info/describe/memory_usage/nunique/count`
14. Column select — `df['c']` vs `df[['c']]` (Series vs DataFrame)
15. Naya column banana, drop, rename, reorder
16. `set_index` / `reset_index`
17. `astype` conversions aur `IntCastingNaNError` ka trap
18. `to_csv` / `read_csv` round-trip (`tempfile`) — `index=False` kyun zaroori hai
19. `read_csv` ke 11 ahem parameters — har ek chalta hua
20. Excel / JSON / parquet / SQL readers ka zikr
21. Display options — `pd.set_option`, `pd.option_context`

Phir: **Common Mistakes / Gotchas**, **Real-World Problems**, **LeetCode (LC 2877/2878/2879)**,
**Interview Q&A**, **Practice Exercises**, aur ek **Cheat-sheet**.

## Prerequisites

- Python basics (list, dict, function, loop)
- numpy ki thori waqfiyat behtar hai (array, dtype, vectorization) — lekin lazmi nahi
- Notebook ko **top-se-bottom** chalao: har cell pichle cell ke variables use karta hai

> **pandas 3.0 note:** Is notebook me pandas 3 ka naya behaviour use hua hai —
> default string dtype ab `str` hai (`object` nahi), `copy-on-write` default hai,
> aur `df.append()` **hata diya gaya hai**. Ye sab aage detail me aayega.
"""))

# ============================================================
# 1. PANDAS KYA HAI
# ============================================================
cells.append(md("""
## 1. pandas Kya Hai Aur Kyun

**Kya hai:** pandas ek open-source Python library hai jo **tabular / labeled data** ke sath kaam
karne ke liye banayi gayi hai. Ismein do main data structures hain:

| Structure | Dimensions | Ek line me |
|---|---|---|
| `Series` | 1D | labeled column (values + index) |
| `DataFrame` | 2D | labeled table (rows + columns) = dict of Series |

Naam "pandas" **"panel data"** (econometrics ki term for multi-dimensional structured data) se
aaya hai. Isay **Wes McKinney** ne 2008 me AQR Capital (ek hedge fund) me banaya tha kyunke
financial time-series data ko numpy se handle karna takleef-deh tha.

**Kyun / kahan use hota hai:**

- **Data cleaning** — missing values, duplicates, wrong dtypes theek karna (asli duniya ka 80% kaam)
- **Data analysis / EDA** — group by, aggregate, pivot, summarize
- **Data pipelines / ETL** — CSV/Excel/SQL/JSON/parquet se read, transform, write
- **Machine learning prep** — features banana, encoding, train data tayyar karna
- **Reporting** — daily sales report, student result sheet, inventory summary

**Kyun numpy kaafi nahi tha:**

1. numpy array **homogeneous** hoti hai (ek hi dtype). Asli data me `name` (string),
   `age` (int), `salary` (float), `joined` (date) — sab ek table me hote hain.
2. numpy me **labels nahi** hote — sirf integer positions. `arr[3]` se pata nahi chalta ye
   kaunsa student hai. pandas me `df.loc["Ali"]` likh sakte ho.
3. numpy me **missing data** ka koi first-class concept nahi.
4. numpy me group-by, join, time-series resampling jaisi cheezein nahi hain.

**Interview tip:** "pandas kya hai?" ka best jawab — *"numpy ke upar bani ek library jo
**labeled**, **heterogeneous**, aur **missing-value-aware** tabular data ke liye hai; iska core
DataFrame hai jo columns ka dict of Series hai."*
"""))

cells.append(code("""
# Import convention — poori duniya isi tarah likhti hai. Interview me `import pandas` (bina as pd)
# likhna amateur lagta hai. `pd` aur `np` universal aliases hain.
import numpy as np
import pandas as pd

print("pandas version :", pd.__version__)
print("numpy version  :", np.__version__)

# pd.show_versions() bhi hota hai — poora environment dump karta hai (pandas + dependencies).
# Output bohat lamba hota hai isliye yahan call nahi kar rahe, sirf yaad rakho:
#   pd.show_versions()   -> bug report file karte waqt ye output attach karo
print("\\nshow_versions available?", hasattr(pd, "show_versions"))

# Install kaise hota hai (yahan chalane ki zaroorat nahi, sirf reference):
#   pip install pandas
#   pip install pandas==3.0.5        <- exact version pin (production me aisa karo)
#   conda install pandas            <- Anaconda users
"""))

# ============================================================
# 2. NUMPY SE RISHTA
# ============================================================
cells.append(md("""
## 2. numpy Se Rishta — pandas Andar Se Kya Hai

**Kya hai:** pandas ka har numeric column andar se ek **numpy array** hai. pandas us array ke
upar ek **index** (row labels) aur ek **column name** chipka deta hai, aur missing values ka
handling add kar deta hai.

Yaani: `Series ≈ numpy array + index + name`, aur `DataFrame ≈ columns ka dict of Series`.

**Kyun jaan-na zaroori hai:** kyunke isi wajah se pandas ke operations **vectorized** (tez) hote
hain — woh andar numpy ke C-level loops chalata hai, Python ka slow `for` loop nahi.

**Output ka matlab (neeche wale cell me):** dekhna ke `s.to_numpy()` bilkul wahi numbers deta
hai jo humne diye the — matlab data numpy me hi para hai, pandas sirf labels manage kar raha hai.
"""))

cells.append(code("""
# numpy array — sirf values, koi label nahi
arr = np.array([50, 60, 70, 80])
print("numpy array :", arr)
print("arr[2]      :", arr[2], "  <- sirf position se access, pata nahi ye kis ka number hai")

# wahi data pandas Series me — ab har value ka ek LABEL hai
marks = pd.Series([50, 60, 70, 80], index=["Ali", "Sara", "Bilal", "Ayesha"])
print("\\npandas Series:")
print(marks)
print("\\nmarks['Bilal']:", marks["Bilal"], "  <- label se access, code self-documenting ban gaya")

# Saboot ke andar numpy hi hai:
print("\\ntype(marks.to_numpy()) :", type(marks.to_numpy()).__name__)
print("marks.to_numpy()       :", marks.to_numpy())
print("dono barabar?          :", np.array_equal(arr, marks.to_numpy()))

# Aur heterogeneous data? numpy me sab kuch string ban jata hai (upcasting):
mixed_np = np.array([1, "Ali", 3.5])
print("\\nnumpy mixed dtype :", mixed_np.dtype, "->", mixed_np, "  <- sab string ban gaye!")

# pandas DataFrame me har column apna dtype rakhta hai — yehi asal faida hai
mixed_df = pd.DataFrame({"id": [1, 2], "name": ["Ali", "Sara"], "gpa": [3.5, 3.9]})
print("\\npandas per-column dtypes:")
print(mixed_df.dtypes)
"""))

# ============================================================
# 3. EXCEL / SQL SE COMPARISON
# ============================================================
cells.append(md("""
## 3. Excel Se Comparison, SQL Se Comparison

Interview me ye sawal bohat aata hai: *"pandas kyun, Excel ya SQL kyun nahi?"*

### pandas vs Excel

| Cheez | Excel | pandas |
|---|---|---|
| Data size | ~1 million rows ki limit, 100k par hang | RAM tak (millions of rows aaram se) |
| Repeatability | manually click-click, agla mahina phir wahi | script chalao — **reproducible** |
| Version control | `.xlsx` binary, git me diff nahi | `.py` text, git diff perfect |
| Audit trail | formula kis cell me hai? koi nahi janta | code padh kar poori pipeline saaf |
| Automation | VBA macros (dard) | Python — scheduler par laga do |
| Learning curve | asaan shuru | thora seekhna parta hai |

**Ek line me:** Excel **exploration** ke liye theek hai, pandas **repeatable pipelines** ke liye.

### pandas vs SQL

| Concept | SQL | pandas |
|---|---|---|
| Table | `TABLE` | `DataFrame` |
| Column | column | `Series` |
| `SELECT col1, col2` | `SELECT name, age FROM t` | `df[["name", "age"]]` |
| `WHERE` | `WHERE age > 18` | `df[df["age"] > 18]` ya `df.query("age > 18")` |
| `ORDER BY` | `ORDER BY age DESC` | `df.sort_values("age", ascending=False)` |
| `GROUP BY` | `GROUP BY city` | `df.groupby("city")` |
| `HAVING` | `HAVING COUNT(*) > 5` | groupby ke baad boolean filter |
| `LIMIT 5` | `LIMIT 5` | `df.head(5)` |
| `DISTINCT` | `SELECT DISTINCT city` | `df["city"].unique()` / `drop_duplicates()` |
| `JOIN` | `JOIN ... ON` | `pd.merge(df1, df2, on=...)` |
| `IS NULL` | `WHERE x IS NULL` | `df[df["x"].isna()]` |

**Farq ki asal baat:** SQL **declarative** hai (kya chahiye batao, engine plan banaye) aur data
disk/server par rehta hai. pandas **imperative + in-memory** hai — data RAM me aata hai, tum
step-by-step transform karte ho, aur beech ka natija dekh sakte ho (debugging asaan).

**Interview tip:** Best jawab — *"SQL data ko fetch/aggregate karne ke liye database me,
pandas us fetched data par complex transformation, reshaping aur ML prep ke liye. Dono
competitor nahi, pipeline ke do hisse hain."*
"""))

# ============================================================
# 4. SERIES — KYA HAI
# ============================================================
cells.append(md("""
## 4. Series — Labeled 1D Array

**Kya hai:** `Series` ek **one-dimensional labeled array** hai. Do hisse hote hain:

1. **values** — asli data (andar numpy array / ExtensionArray)
2. **index** — har value ka label (default `0,1,2,...` = `RangeIndex`)

Isay yaad rakhne ka asaan tareeqa: **Series = Excel ki ek column** (header = `name`,
row numbers = `index`, cells = `values`).

**Kyun / kahan:** DataFrame ka har column ek Series hai. Jab tum `df["age"]` likhte ho tumhein
Series milti hai. Isliye Series samajhna DataFrame samajhne ki bunyaad hai.

**Syntax:**
```python
pd.Series(data, index=None, dtype=None, name=None)
```
`data` ho sakta hai: list, dict, scalar, numpy array, ya doosri Series.
"""))

cells.append(code("""
# --- Tareeqa 1: list se (sab se aam) -------------------------------------
s1 = pd.Series([10, 20, 30, 40])
print("1) list se:")
print(s1)
# Output ka matlab: baayen column = INDEX (0,1,2,3 automatic bana), daayen = values.
# Aakhri line `dtype: int64` — pandas ne khud dtype infer kiya.
print("index :", s1.index)      # RangeIndex(start=0, stop=4, step=1)
print("values:", s1.values)     # numpy array
"""))

cells.append(code("""
# --- Tareeqa 2: custom index ke sath -------------------------------------
# index dena tab useful hai jab labels ka koi asli matlab ho (naam, date, city, id)
s2 = pd.Series([50, 60, 70], index=["Ali", "Sara", "Bilal"])
print("2) custom index:")
print(s2)
print("\ns2['Sara'] ->", s2["Sara"])

# GOTCHA: index ki length data ki length se match karni chahiye warna ValueError
try:
    pd.Series([1, 2, 3], index=["a", "b"])       # 3 values, 2 labels
except ValueError as e:
    print("\n[ValueError]", e)
"""))

cells.append(code("""
# --- Tareeqa 3: dict se (keys hi index ban jati hain) --------------------
s3 = pd.Series({"Karachi": 15000000, "Lahore": 11000000, "Islamabad": 1100000})
print("3) dict se (keys -> index):")
print(s3)

# dict + index dono do to index FILTER + REORDER ka kaam karta hai
s3b = pd.Series({"Karachi": 15000000, "Lahore": 11000000}, index=["Lahore", "Karachi", "Quetta"])
print("\n3b) dict + index (Quetta dict me nahi tha -> NaN):")
print(s3b)
# Output ka matlab: jo label dict me nahi mila uski value NaN ban gayi, aur poora
# column float64 ho gaya (kyunke NaN ek float hai) -- ye classic pandas behaviour hai.
print("dtype ab:", s3b.dtype)
"""))

cells.append(code("""
# --- Tareeqa 4: scalar + index (broadcast) ------------------------------
# Ek hi value ko poore index par phaila dena -- default/placeholder column banane me kaam aata hai
s4 = pd.Series(0, index=["Mon", "Tue", "Wed", "Thu", "Fri"])
print("4) scalar broadcast:")
print(s4)

# --- Tareeqa 5: numpy array se ----------------------------------------
rng = np.random.default_rng(42)          # seed do -> har baar wahi numbers (reproducible)
s5 = pd.Series(rng.integers(50, 100, size=5), index=[f"Q{i}" for i in range(1, 6)])
print("\n5) numpy array se:")
print(s5)
print("\ndtype:", s5.dtype, "| shape:", s5.shape, "| size:", s5.size)
"""))

cells.append(md("""
### 4.1 `name` attribute aur `index.name`

**Kya hai:** Series ka `name` woh label hai jo DataFrame me jaane par **column ka naam** ban jata
hai. `index.name` row-labels ke group ka naam hota hai.

**Kyun:** jab tum `groupby` ya `value_counts` karte ho, pandas khud `name` set karta hai — aur
jab Series ko `to_frame()` se DataFrame banate ho to wahi `name` column header ban jata hai.
"""))

cells.append(code("""
marks_named = pd.Series([50, 60, 70], index=["Ali", "Sara", "Bilal"], name="maths")
marks_named.index.name = "student"          # index ko bhi naam de diya
print(marks_named)
# Output ka matlab: pehli line 'student' (index ka naam), aakhri line 'Name: maths' (Series ka naam)

print("\ns.name       :", marks_named.name)
print("s.index.name :", marks_named.index.name)

# name ka asal faida: to_frame() par wahi column header ban jata hai
print("\nto_frame() ke baad:")
print(marks_named.to_frame())

# rename() se naya naam (naya object banta hai, original safe rehta hai)
print("\nrename ke baad name:", marks_named.rename("mathematics").name)
print("original ka name    :", marks_named.name, " <- original nahi badla")
"""))

cells.append(md("""
### 4.2 `values` vs `.array` vs `.to_numpy()` — teen tareeqe, teen matlab

Ye interview ka favourite sawal hai. Teenon "raw data" dete hain lekin **type alag** hota hai:

| Property | Kya deta hai | Kab use karo |
|---|---|---|
| `s.values` | numpy array (ya extension array) — **legacy** | naya code me avoid karo |
| `s.array` | pandas ka **ExtensionArray** (dtype-faithful) | jab pandas ka apna dtype preserve karna ho |
| `s.to_numpy()` | **hamesha** numpy ndarray | **recommended** — explicit aur predictable |

**Kyun `values` avoid karein:** `values` ka return type dtype par depend karta hai — kabhi numpy
array, kabhi ExtensionArray. `to_numpy()` hamesha numpy deta hai, isliye woh **predictable** hai.

**pandas 3 note:** string column par `.array` ek `StringArray` deta hai (numpy array nahi),
jabke `.to_numpy()` `dtype=object` ki numpy array deta hai. Neeche dekho.
"""))

cells.append(code("""
int_s = pd.Series([1, 2, 3])
str_s = pd.Series(["Ali", "Sara", "Bilal"])

print("--- int Series ---")
print("s.values      ->", type(int_s.values).__name__, "|", int_s.values)
print("s.array       ->", type(int_s.array).__name__)
print("s.to_numpy()  ->", type(int_s.to_numpy()).__name__, "| dtype:", int_s.to_numpy().dtype)

print("\n--- string Series (pandas 3 me dtype 'str') ---")
print("s.dtype       ->", str_s.dtype)
print("s.array       ->", type(str_s.array).__name__, " <- StringArray, numpy nahi!")
print("s.to_numpy()  ->", type(str_s.to_numpy()).__name__, "| dtype:", str_s.to_numpy().dtype)

# to_numpy() me dtype force bhi kar sakte ho
print("\nto_numpy(dtype=float) :", int_s.to_numpy(dtype=float))

# GOTCHA: to_numpy() par index KHATAM ho jata hai -- labels chale gaye
print("\nIndex bach gaya? ", hasattr(int_s.to_numpy(), "index"), " <- nahi, numpy me index nahi hota")
"""))

cells.append(md("""
### 4.3 Series indexing ki bunyaad

**Kya hai:** Series se value nikalne ke do zehni model hain — **label se** aur **position se**.

- `s["Ali"]` → label se
- `s.iloc[0]` → position se
- `s.loc["Ali"]` → label se (explicit — **yehi likho**)

**Common mistake / gotcha:** agar index **integers** ka ho to `s[0]` confusing ho jata hai —
label 0 chahiye ya position 0? Isi ambiguity ki wajah se pandas ne positional `s[0]` ko
integer-index par hatana shuru kiya. **Hamesha `.loc` (label) aur `.iloc` (position) explicitly
likho** — ye habit tumhein bohat bugs se bachayegi. (Poori detail notebook 02 me.)
"""))

cells.append(code("""
s = pd.Series([100, 200, 300, 400], index=["a", "b", "c", "d"])

print("s['b']        :", s["b"])          # label
print("s.loc['b']    :", s.loc["b"])      # label (explicit) <- best practice
print("s.iloc[1]     :", s.iloc[1])       # position
print("s.iloc[-1]    :", s.iloc[-1])      # aakhri element (numpy jaisa negative index)

# Multiple labels -> Series wapas
print("\ns.loc[['a','c']] ->")
print(s.loc[["a", "c"]])

# Slicing ka BARA farq: .loc INCLUSIVE hai, .iloc EXCLUSIVE
print("\ns.loc['a':'c'] (inclusive - 'c' shamil hai) :", s.loc["a":"c"].tolist())
print("s.iloc[0:3]    (exclusive - 3rd index nahi)  :", s.iloc[0:3].tolist())

# Boolean mask -- filtering ki bunyaad
print("\ns[s > 150] ->", s[s > 150].tolist())

# GOTCHA: jo label maujood nahi
try:
    s.loc["zz"]
except KeyError as e:
    print("\n[KeyError]", e)
"""))

cells.append(md("""
### 4.4 Vectorized operations — pandas ka superpower

**Kya hai:** Series par arithmetic/comparison lagao to woh **poori Series par ek saath** apply
hota hai — koi `for` loop nahi. Ye numpy ke C loops chalate hain, isliye 10x-100x tez hota hai.

**Kyun:** ye pandas ka asal idiom hai. Interview me "pandas me loop kyun bura hai?" ka jawab
yehi hai — vectorized alternative maujood hai jo tez aur padhne me saaf hai.

**Output ka matlab:** har operation naya Series banata hai, **index preserve** hota hai.
"""))

cells.append(code("""
prices = pd.Series([100, 250, 80, 500], index=["pen", "bag", "book", "shoes"], name="price")

print("original:\n", prices.to_dict())

# Arithmetic -- har element par
print("\n17% GST lagao      :", (prices * 1.17).round(2).to_dict())
print("100 rupees discount :", (prices - 100).to_dict())

# Comparison -> boolean Series (filtering ke liye)
print("\nprices > 150 :", (prices > 150).to_dict())

# Do Series ke darmiyan element-wise (same index)
qty = pd.Series([2, 1, 3, 1], index=["pen", "bag", "book", "shoes"])
total = prices * qty
print("\ntotal = price * qty :", total.to_dict())

# Aggregations -- ek scalar
print("\nsum:", total.sum(), "| mean:", round(total.mean(), 2), "| max:", total.max(),
      "| idxmax:", total.idxmax())

# String methods .str accessor se (poori detail notebook 03 me)
names = pd.Series([" ali ", "SARA", "bilal"])
print("\nstrip+title:", names.str.strip().str.title().tolist())

# Numpy ufuncs bhi seedha chalte hain aur index preserve karte hain
print("\nnp.sqrt(prices):", np.sqrt(prices).round(2).to_dict())
"""))

cells.append(md("""
### 4.5 Index Alignment — "NaN kahan se aa gaya?" (BARA interview point)

**Kya hai:** jab do Series par operation karte ho, pandas unhein **position se nahi, index (label)
se align** karta hai. Jo label dono me maujood ho uska hisaab hota hai; jo label sirf ek me ho
uska natija **NaN** aata hai.

**Kyun aisa design:** kyunke labels ka matlab hota hai. Agar ek Series me January-June ka sales
hai aur doosri me March-August ka, to March ka March se jama hona chahiye — pehla element pehle
element se nahi. Ye **feature** hai, bug nahi.

**Kyun log phaste hain:** numpy me positional addition hoti hai, isliye numpy se aane wale log
expect karte hain ke pehla+pehla ho jayega. pandas me aisa **nahi** hota.

**Fix ke tareeqe:**
- `s1.add(s2, fill_value=0)` — missing labels ko 0 maan lo
- `s1.reset_index(drop=True) + s2.reset_index(drop=True)` — jaan boojh kar positional
- `s1.to_numpy() + s2.to_numpy()` — labels bilkul ignore
"""))

cells.append(code("""
q1 = pd.Series([100, 200, 300], index=["Ali", "Sara", "Bilal"])
q2 = pd.Series([10, 20, 30], index=["Sara", "Bilal", "Ayesha"])   # Ali nahi, Ayesha naya

print("q1:", q1.to_dict())
print("q2:", q2.to_dict())

total = q1 + q2
print("\nq1 + q2:")
print(total)
# Output ka matlab:
#   Ali    -> sirf q1 me tha  -> NaN
#   Sara   -> 100 + 10 = 110  (dono me tha)
#   Bilal  -> 200 + 30 = 230
#   Ayesha -> sirf q2 me tha  -> NaN
# Aur dtype float64 ho gaya kyunke NaN float hai.

print("\nUnion index (dono ka jor):", sorted(total.index.tolist()))
print("NaN kitne?", int(total.isna().sum()))
"""))

cells.append(code("""
# --- Alignment ke 3 fixes ---

# FIX 1: fill_value -- missing label ko 0 samjho (sab se saaf tareeqa)
print("1) q1.add(q2, fill_value=0):")
print(q1.add(q2, fill_value=0).to_dict())

# FIX 2: positional jama karna chahte ho to index hata do
a = q1.reset_index(drop=True)
b = q2.reset_index(drop=True)
print("\n2) positional (reset_index):", (a + b).tolist())

# FIX 3: numpy me convert -- labels bilkul ignore
print("3) numpy se positional      :", (q1.to_numpy() + q2.to_numpy()).tolist())

# Interview tip: alignment sirf + par nahi -- -, *, /, comparison, DataFrame operations,
# assignment (df['new'] = other_series) -- SAB par hota hai. Ye pandas ka core rule hai.
assert q1.add(q2, fill_value=0)["Ali"] == 100        # Ali ko 0 add hua
assert (a + b).tolist() == [110, 220, 330]          # positional natija
print("\n[OK] asserts pass")
"""))

cells.append(md("""
### 4.6 Series vs list vs numpy array vs dict — kab kaunsa?

| Feature | `list` | `np.array` | `dict` | `pd.Series` |
|---|---|---|---|---|
| Labels (keys) | ❌ | ❌ | ✅ | ✅ |
| Order guaranteed | ✅ | ✅ | ✅ (3.7+) | ✅ |
| Mixed types | ✅ | ❌ (upcast) | ✅ | ⚠️ (object dtype me) |
| Vectorized math | ❌ | ✅ | ❌ | ✅ |
| Missing data support | ❌ | ⚠️ (sirf float NaN) | ❌ | ✅ (NaN/NA/NaT) |
| Duplicate labels | — | — | ❌ | ✅ |
| Aggregations (`sum/mean`) | `sum()` only | ✅ | ❌ | ✅ (+ `describe`) |
| Alignment on ops | ❌ | ❌ (positional) | ❌ | ✅ (by label) |
| Memory efficiency | kam | **behtareen** | kam | behtareen (numpy backed) |

**Faisla asaan tareeqe se:**
- Sirf chhoti collection, koi math nahi → **list**
- Numeric math, koi label nahi, max speed → **numpy array**
- Key→value lookup, koi analytics nahi → **dict**
- Labeled data + analytics + missing values → **Series**
"""))

cells.append(code("""
# Practical demo: dict me average nikalna vs Series me
scores_dict = {"Ali": 80, "Sara": 92, "Bilal": 67}
scores_series = pd.Series(scores_dict)

# dict ke sath -- manual kaam
avg_dict = sum(scores_dict.values()) / len(scores_dict)
print("dict se average   :", round(avg_dict, 2))

# Series ke sath -- built-in, aur bohat kuch free milta hai
print("Series se average :", round(scores_series.mean(), 2))
print("Series describe   :")
print(scores_series.describe())
# Output ka matlab: ek hi call me count/mean/std/min/quartiles/max -- dict me ye sab manually likhte.

# Aur list par vectorized math? Chalta hi nahi:
try:
    [1, 2, 3] * 1.5          # list * float -> TypeError
except TypeError as e:
    print("\n[TypeError] list * 1.5 ->", e)
print("Series * 1.5 ->", (pd.Series([1, 2, 3]) * 1.5).tolist(), " <- kaam kar gaya")
"""))

# ============================================================
# 5. DATAFRAME
# ============================================================
cells.append(md("""
## 5. DataFrame — Labeled 2D Table

**Kya hai:** `DataFrame` ek **2-dimensional labeled table** hai. Teen hisse:

1. **index** — row labels
2. **columns** — column labels
3. **values** — asli data

Sab se ahem zehni model: **DataFrame = dict of Series jo ek common index share karti hain.**
Har column ek Series hai, aur sab columns ka index same hai.

```
        columns ->   name     age    city
index
  0            |    Ali       22    Karachi
  1            |    Sara      25    Lahore
  2            |    Bilal     23    Karachi
```

**Kyun:** asli duniya ka data table ki shakal me hota hai — CSV, Excel sheet, SQL table,
API ka JSON array. DataFrame unka natural container hai.

**Banane ke tareeqe (aage har ek chalta hua):** dict of lists, list of dicts, list of lists +
`columns=`, numpy 2D array, dict of Series, `from_records`, aur CSV text se `read_csv`.
"""))

cells.append(code("""
# --- Tareeqa 1: dict of lists (SAB SE AAM) ------------------------------
# Sochne ka tareeqa: har KEY ek column ka naam, har LIST us column ka data
df1 = pd.DataFrame({
    "name": ["Ali", "Sara", "Bilal", "Ayesha"],
    "age": [22, 25, 23, 21],
    "city": ["Karachi", "Lahore", "Karachi", "Islamabad"],
    "gpa": [3.2, 3.8, 2.9, 3.6],
})
print("1) dict of lists:")
print(df1)
print("\nshape:", df1.shape, " <- (rows, columns)")

# GOTCHA: sab lists ki length same honi chahiye
try:
    pd.DataFrame({"a": [1, 2, 3], "b": [1, 2]})
except ValueError as e:
    print("\n[ValueError]", e)
"""))

cells.append(code("""
# --- Tareeqa 2: list of dicts (API / JSON se aane wala data) ------------
# Har dict = ek ROW. Ye shakal REST API responses aur MongoDB me aam hai.
records = [
    {"name": "Ali", "age": 22, "city": "Karachi"},
    {"name": "Sara", "age": 25, "city": "Lahore"},
    {"name": "Bilal", "age": 23},                    # 'city' missing hai!
]
df2 = pd.DataFrame(records)
print("2) list of dicts:")
print(df2)
# Output ka matlab: Bilal ke paas 'city' nahi thi -> pandas ne khud NaN daal diya.
# Ye list-of-dicts ka bara faida hai: missing keys automatically NaN ban jati hain.
print("\nmissing values per column:")
print(df2.isna().sum())
"""))

cells.append(code("""
# --- Tareeqa 3: list of lists + columns= --------------------------------
# Yahan column names ALAG se dene parte hain warna 0,1,2 headers ban jate hain
rows = [["Ali", 22, "Karachi"], ["Sara", 25, "Lahore"], ["Bilal", 23, "Karachi"]]

df3_bad = pd.DataFrame(rows)                                   # columns= bhoola
print("3a) columns= ke baghair (headers 0,1,2 ban gaye):")
print(df3_bad.head(2))

df3 = pd.DataFrame(rows, columns=["name", "age", "city"])       # sahi tareeqa
print("\n3b) columns= ke sath:")
print(df3)

# --- Tareeqa 4: numpy 2D array se -------------------------------------
mat = np.arange(1, 13).reshape(4, 3)          # 4 rows x 3 columns
df4 = pd.DataFrame(mat, columns=["jan", "feb", "mar"], index=["p1", "p2", "p3", "p4"])
print("\n4) numpy 2D array se:")
print(df4)
# Output ka matlab: poora frame ek hi dtype (int64) ka hai kyunke numpy array homogeneous thi.
print("\ndtypes (sab int64 -- numpy homogeneous thi):")
print(df4.dtypes.to_dict())
"""))

cells.append(code("""
# --- Tareeqa 5: dict of Series (alignment ka jadoo) ---------------------
# Yahan index automatically UNION ban jata hai aur missing values NaN
maths = pd.Series({"Ali": 80, "Sara": 92, "Bilal": 67})
urdu = pd.Series({"Ali": 75, "Sara": 88, "Ayesha": 90})       # Bilal nahi, Ayesha naya

df5 = pd.DataFrame({"maths": maths, "urdu": urdu})
print("5) dict of Series:")
print(df5)
# Output ka matlab: index = union(Ali, Sara, Bilal, Ayesha).
#   Bilal ka urdu -> NaN, Ayesha ka maths -> NaN.
# Yehi wajah hai ke DataFrame ko "dict of Series sharing an index" kehte hain.

# --- Tareeqa 6: from_records ------------------------------------------
tuples = [("Ali", 22), ("Sara", 25), ("Bilal", 23)]
df6 = pd.DataFrame.from_records(tuples, columns=["name", "age"])
print("\n6) from_records (tuples se):")
print(df6)

# from_dict bhi hota hai -- orient='index' se dict keys ROWS ban jati hain
df6b = pd.DataFrame.from_dict({"r1": [1, 2], "r2": [3, 4]}, orient="index", columns=["x", "y"])
print("\n6b) from_dict(orient='index'):")
print(df6b)
"""))

cells.append(code("""
# --- Tareeqa 7: CSV text se (io.StringIO) ------------------------------
# io.StringIO ek string ko "file jaisa" bana deta hai -- notebooks/tests me
# bina asli file banaye read_csv ka demo karne ka behtareen tareeqa.
import io

csv_text = '''name,age,city,gpa
Ali,22,Karachi,3.2
Sara,25,Lahore,3.8
Bilal,23,Karachi,2.9
Ayesha,21,Islamabad,3.6'''

df7 = pd.read_csv(io.StringIO(csv_text))
print("7) read_csv(StringIO):")
print(df7)
print("\ndtypes -- pandas ne khud infer kiye:")
print(df7.dtypes)
# Output ka matlab: age -> int64, gpa -> float64, name/city -> str (pandas 3 ka naya default).
# pandas ne har column ka type khud pehchan liya -- isay TYPE INFERENCE kehte hain.

assert df7.shape == (4, 4)
assert df7["age"].dtype == "int64"
print("\n[OK] asserts pass")
"""))

cells.append(md("""
## 6. `columns` aur `index` — Index Object Kya Hai

**Kya hai:** `df.index` aur `df.columns` dono ek hi class ke objects hain — **`pd.Index`**.
Index ek **immutable, array-like** structure hai jo labels rakhta hai aur andar ek hash table
maintain karta hai taake lookup **O(1)** ho.

**Kyun immutable:** kyunke Index ko multiple objects share karte hain (do DataFrames ek hi index
object point kar sakte hain). Agar mutable hota to ek jagah change doosri jagah silently tor deta.
Isliye label badalne ka tareeqa `rename()` hai — naya object banta hai.

**Kyun Index tez hai:** `df.loc["Ali"]` ek hash lookup hai (dictionary jaisa), poori list scan
nahi hoti. Isliye set_index karke lookup karna linear filtering se tez hota hai.

**Index ke qism:** `RangeIndex` (default), `Index` (generic, str/object), `DatetimeIndex`,
`CategoricalIndex`, `MultiIndex` (nested levels — Intermediate notebooks me).
"""))

cells.append(code("""
print("df1.index   :", df1.index)
print("df1.columns :", df1.columns)
print("\ndono ka type:", type(df1.index).__name__, "aur", type(df1.columns).__name__)

# Index array-like hai -- iterate, slice, membership sab chalta hai
print("\ncolumns list  :", df1.columns.tolist())
print("'age' maujood? :", "age" in df1.columns)
print("index[0]       :", df1.index[0])
print("index unique?  :", df1.index.is_unique)

# IMMUTABLE ka saboot -- seedha assign karne par TypeError
try:
    df1.columns[0] = "student_name"
except TypeError as e:
    print("\n[TypeError] Index immutable hai ->", e)

# Sahi tareeqe: rename() (naya object) ya poori columns list replace karna
print("\nrename se:", df1.rename(columns={"name": "student_name"}).columns.tolist())

# Index par set-operations bhi hote hain (bohat kaam ke)
i1 = pd.Index(["a", "b", "c"])
i2 = pd.Index(["b", "c", "d"])
print("\nunion       :", i1.union(i2).tolist())
print("intersection:", i1.intersection(i2).tolist())
print("difference  :", i1.difference(i2).tolist())
"""))

cells.append(md("""
## 7. `dtypes` — pandas Ke Data Types

**Kya hai:** har column ka apna **dtype** hota hai. `df.dtypes` sab dikhata hai.

| dtype | Kya rakhta hai | Missing value |
|---|---|---|
| `int64` | integers | ❌ (NaN nahi rakh sakta) |
| `float64` | decimals | `np.nan` |
| `str` | **pandas 3 ka default string dtype** | `nan` |
| `bool` | True/False | ❌ |
| `datetime64[us]` | timestamps | `NaT` |
| `timedelta64` | durations | `NaT` |
| `category` | limited unique values (repeated) | `NaN` |
| `object` | kuch bhi (Python objects) — legacy | `None`/`nan` |

### pandas 3 ka BARA change: default string dtype `str` hai, `object` nahi

pandas 2 tak string columns ka dtype `object` hota tha (har value ek alag Python `str` object —
slow aur memory-heavy). pandas 3 me (PDEP-14) default **`str`** hai — ye tez aur memory-efficient
hai. Purane tutorials me `object` likha milega — ghabrao nahi, wahi cheez hai.

### Nullable (extension) dtypes — capital letter wale

| Normal | Nullable version | Faida |
|---|---|---|
| `int64` | `Int64` | NaN rakh sakta hai (`pd.NA`) |
| `float64` | `Float64` | `pd.NA` semantics |
| `bool` | `boolean` | teen halat: True/False/`pd.NA` |
| `str` | `string` | missing value `pd.NA` (na `nan`) |

**Kyun zaroori:** normal `int64` me missing value nahi ho sakti — isliye jab bhi NaN aata hai
pandas poore column ko `float64` bana deta hai (`1` → `1.0`). `Int64` is masle ko hal karta hai.
"""))

cells.append(code("""
# Ek frame jisme har ahem dtype maujood ho
types_df = pd.DataFrame({
    "int_col": [1, 2, 3],
    "float_col": [1.5, 2.5, 3.5],
    "str_col": ["Ali", "Sara", "Bilal"],              # pandas 3 -> dtype 'str'
    "bool_col": [True, False, True],
    "date_col": pd.to_datetime(["2024-01-15", "2024-02-20", "2024-03-25"]),
    "cat_col": pd.Series(["A", "B", "A"], dtype="category"),
})
print("dtypes:")
print(types_df.dtypes)
# Output ka matlab: str_col ka dtype 'str' hai (pandas 2 me 'object' hota tha).
# date_col ka dtype datetime64[us] hai -- pandas 3 me default unit MICROseconds hai (ns nahi).

print("\nstr dtype ki asli shakal:", repr(types_df["str_col"].dtype))
print("is_string_dtype?          :", pd.api.types.is_string_dtype(types_df["str_col"]))

# Purana 'object' dtype aaj bhi mil sakta hai (mixed Python objects)
obj_s = pd.Series([1, "Ali", [1, 2], None])
print("\nmixed values ka dtype    :", obj_s.dtype, " <- object (kuch bhi rakh sakta hai, lekin SLOW)")
"""))

cells.append(code("""
# --- Nullable dtypes ka faida ---

# Masla: normal int64 column me ek NaN aane par poora column float ban jata hai
normal = pd.Series([1, 2, None])
print("int + NaN -> dtype:", normal.dtype, "| values:", normal.tolist())
print("   dekho 1 ab 1.0 ho gaya -- IDs/counts ke liye ye bura hai")

# Hal: nullable Int64 (capital I)
nullable = pd.Series([1, 2, None], dtype="Int64")
print("\nInt64 -> dtype:", nullable.dtype, "| values:", nullable.tolist())
print("   integer integer hi raha, aur missing value <NA> hai")

# boolean nullable -- teen halat
tri = pd.Series([True, False, None], dtype="boolean")
print("\nboolean nullable:", tri.tolist())

# 'string' dtype (pd.NA semantics) vs default 'str' dtype (nan semantics)
s_str = pd.Series(["a", None])                      # default -> 'str'
s_string = pd.Series(["a", None], dtype="string")   # nullable -> 'string'
print("\ndefault 'str' dtype   :", s_str.dtype, "| missing value:", repr(s_str[1]))
print("nullable 'string' dtype:", s_string.dtype, "| missing value:", repr(s_string[1]))
print("dono ke liye isna() same kaam karta hai:", s_str.isna().tolist(), s_string.isna().tolist())

# Interview tip: Int64 use karo jab column me IDs/counts hon aur missing values mumkin hon.
assert nullable.dtype == "Int64" and normal.dtype == "float64"
print("\n[OK] asserts pass")
"""))

cells.append(md("""
## 8. Inspection Toolkit — Naya Data Mile To Pehle Kya Karein

**Kya hai:** ek fixed checklist jo har naye dataset par chalani chahiye. Interview me bhi poochte
hain: *"tumhein ek naya CSV mile to pehle 5 minute me kya karoge?"*

**Standard order (yaad kar lo):**

| Step | Code | Kya batata hai |
|---|---|---|
| 1 | `df.shape` | kitne rows/columns |
| 2 | `df.head()` / `df.tail()` | data dikhta kaisa hai |
| 3 | `df.info()` | dtypes + non-null count + memory |
| 4 | `df.describe()` | numeric summary (outliers ka ishara) |
| 5 | `df.isna().sum()` | kis column me kitna missing |
| 6 | `df.nunique()` | kaunsa column categorical lagta hai |
| 7 | `df.duplicated().sum()` | duplicate rows |
| 8 | `df["c"].value_counts()` | categories ka distribution |

Chalo ek thora bara realistic frame banate hain aur poori checklist chalate hain.
"""))

cells.append(code("""
# Realistic employees dataset (inline -- koi bahar ki file nahi)
emp = pd.DataFrame({
    "emp_id": [101, 102, 103, 104, 105, 106, 107, 108],
    "name": ["Ali Khan", "Sara Ahmed", "Bilal Raza", "Ayesha Malik",
             "Usman Tariq", "Hina Shah", "Zain Abbas", "Mariam Ali"],
    "dept": ["IT", "HR", "IT", "Finance", "IT", "HR", "Finance", "IT"],
    "salary": [85000, 60000, 92000, 75000, 110000, 58000, 81000, np.nan],
    "experience": [3, 5, 7, 4, 10, 2, 6, 1],
    "is_remote": [True, False, True, False, True, False, True, True],
    "joined": pd.to_datetime(["2021-03-01", "2019-07-15", "2017-01-20", "2020-11-05",
                              "2014-06-10", "2022-02-28", "2018-09-01", "2023-05-15"]),
})
print(emp)
print("\nshape:", emp.shape)
"""))

cells.append(code("""
# --- head / tail / sample ---
print("head(3) -- pehli 3 rows:")
print(emp.head(3))

print("\ntail(2) -- aakhri 2 rows:")
print(emp.tail(2))

# sample() random rows deta hai -- random_state se natija reproducible ho jata hai
print("\nsample(2, random_state=1) -- random 2 rows (seed fix):")
print(emp.sample(2, random_state=1)[["name", "dept"]])

# head() ka default 5 hai; negative bhi de sakte ho
print("\nhead(-6) -- aakhri 6 chhor kar:", emp.head(-6)["name"].tolist())
"""))

cells.append(code("""
# --- shape / size / ndim / len ---
print("shape :", emp.shape, "  <- (rows, columns) tuple")
print("size  :", emp.size, "  <- total cells = rows * columns")
print("ndim  :", emp.ndim, "  <- DataFrame hamesha 2, Series hamesha 1")
print("len() :", len(emp), "  <- sirf rows (index ki length)")
print("columns count:", len(emp.columns))

# Series par yehi properties
print("\nemp['salary'].shape:", emp["salary"].shape, "| ndim:", emp["salary"].ndim)

assert emp.shape == (8, 7)
assert emp.size == 8 * 7
assert emp.ndim == 2 and emp["salary"].ndim == 1
print("\n[OK] asserts pass")
"""))

cells.append(code("""
# --- info() -- sab se zyada kaam ka ek single command ---
emp.info()
# Output ka matlab (line by line):
#   <class 'pandas.DataFrame'>        -> object ka type
#   RangeIndex: 8 entries, 0 to 7     -> 8 rows, index 0..7
#   Data columns (total 7 columns)    -> 7 columns
#   Non-Null Count                   -> 'salary' me 7 non-null hai (1 missing!)
#   Dtype                            -> har column ka type ('str' pandas 3 me)
#   memory usage                     -> approximate RAM

# GOTCHA: default memory usage strings ko poora nahi ginta.
# Asli memory ke liye memory_usage='deep' do:
print("\n--- info(memory_usage='deep') ---")
emp.info(memory_usage="deep")
"""))
