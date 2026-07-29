"""Generator: Numpy/Intermediate/01_Axis_Mastery_Aggregations_aur_Advanced_Indexing.ipynb"""
import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

CELLS = []
def M(s): CELLS.append(md(s))
def C(s): CELLS.append(code(s))

# ----------------------------------------------------------------- title
M(r"""
# NumPy Intermediate 01 — Axis Mastery, Aggregations aur Advanced Indexing

**Level:** Intermediate → Advanced
**Prerequisites:** NumPy Basics (array banana, dtype, slicing, broadcasting ka basic idea)

Basics me humne array banana seekha. Ab asli khel shuru hota hai: **axis**.
90% NumPy bugs sirf ek wajah se hote hain — bandey ko pata nahi hota ke `axis=0` ka
matlab "rows par chalo" hai ya "rows ke andar chalo". Is notebook ke baad ye confusion
hamesha ke liye khatam.

## Is notebook me kya seekhenge

- **Multi-dimensional soch** — shape ko "nested boxes" ki tarah dekhna, 3D/4D arrays,
  ML ka classic layout `batch × height × width × channels`
- **Axis ka poora mastery** — `axis=0/1/-1`, tuple of axes, `keepdims` ka broadcasting me faida
- **Reductions** — `sum/mean/std/min/max/argmin/argmax` + `unravel_index` se 2D argmax
- **Cumulative ops** — `cumsum`, `cumprod`, `diff`, `ediff1d`, `gradient`, `trapezoid`
- **Order statistics** — `sort/argsort/lexsort/partition/argpartition` (top-k O(n) me!), stable sort
- **Searching** — `searchsorted`, binning, `where`, `nonzero`, `flatnonzero`, `argwhere`, `extract`, `count_nonzero`
- **Set ops** — `unique` ke teen return flags, `intersect1d`, `union1d`, `setdiff1d`, `isin`
- **Counting & binning** — `bincount` (+weights), `histogram`, `histogram2d`, `digitize`
- **NaN / inf handling** — poori `nan*` family, `isnan`, `nan_to_num`, masked arrays (`np.ma`)
- **Advanced indexing deep** — index arrays + broadcasting, `np.ix_`, `take_along_axis`,
  `put_along_axis`, `choose`, `np.add.at` (unbuffered scatter)
- **Group-by emulation** — pandas ke baghair `bincount` / `np.add.at` se grouped sums
- **`apply_along_axis`** — kaam karta hai magar slow kyun hai
- Gotchas, 5 real-world problems, 5 LeetCode problems, 20 interview Q&A, practice exercises

> **Padhne ka tareeqa:** har code cell khud chala kar output dekho. Shape ko har waqt
> print karo — `print(a.shape)` NumPy ka sab se bara debugging tool hai.
""")

C(r"""
# Setup — ye cell sab se pehle chalao
import numpy as np
import math

print("NumPy version:", np.__version__)

# Chhota helper: array ka poora "profile" ek line me dekhne ke liye.
def info(name, a):
    a = np.asarray(a)
    print(f"{name:<12} shape={str(a.shape):<16} ndim={a.ndim}  dtype={str(a.dtype):<8} size={a.size}  nbytes={a.nbytes}")

# Output thora saaf dikhe is liye print options set kar rahe hain.
np.set_printoptions(precision=3, suppress=True, linewidth=110)
print("setup done")
""")

# ----------------------------------------------------------------- multi-dim thinking
M(r"""
## 1. Multi-dimensional soch — shape ko "nested boxes" samjho

### Kya hai
`shape` ek tuple hai jo batata hai ke array kitni **nesting levels** rakhta hai.
Sab se aasan zehni model:

```
shape = (2, 3, 4)
         ^  ^  ^
         |  |  +-- sab se andar wala box: 4 numbers ek row me
         |  +----- us se bahar: 3 aisi rows (yaani ek 3x4 table)
         +-------- sab se bahar: 2 aisi tables
```

Yaani `shape=(2,3,4)` ka matlab: **2 tables, har table me 3 rows, har row me 4 numbers**.

### Golden rule
`shape` ko **bahar se andar** parho: pehla number sab se bahar wala container,
aakhri number sab se andar wala (contiguous memory me sab se tez chalne wala) dimension.

### Kyun / kahan use hota hai
- Grayscale image = 2D `(height, width)`
- Color image = 3D `(height, width, 3)`
- Batch of color images (deep learning ka input) = 4D `(batch, height, width, channels)`
- Video batch = 5D `(batch, frames, height, width, channels)`
- NLP: `(batch, sequence_length, embedding_dim)`

### Interview tip
"Explain the shape of a CNN input" — jawab: `(N, H, W, C)` (TensorFlow/Keras style) ya
`(N, C, H, W)` (PyTorch style). Farq **channels-last vs channels-first** ka hai.
""")

C(r"""
# 0D se 4D tak — har level ka matlab dekho
scalar = np.array(42)                       # 0D: sirf ek number, shape = () khali tuple
vec    = np.array([1, 2, 3, 4])              # 1D: ek row (vector)
mat    = np.arange(12).reshape(3, 4)         # 2D: 3 rows x 4 cols (table / matrix)
cube   = np.arange(24).reshape(2, 3, 4)      # 3D: 2 tables, har table 3x4
tensor = np.arange(48).reshape(2, 2, 3, 4)   # 4D: 2 batches x 2 tables x 3 rows x 4 cols

for nm, a in [("scalar", scalar), ("vec", vec), ("mat", mat), ("cube", cube), ("tensor", tensor)]:
    info(nm, a)

print("\ncube:\n", cube)
print("\ncube[0] = pehla table, shape:", cube[0].shape)   # ek dimension gir gaya
print("cube[0, 1] = pehle table ki doosri row:", cube[0, 1])
print("cube[0, 1, 2] = ek single number:", cube[0, 1, 2])
""")

C(r"""
# ML style layout: batch x height x width x channels (NHWC)
# 4 chhoti tasveerein, har ek 5x5 pixels, 3 channels (R,G,B) — synthetic data
rng = np.random.default_rng(42)                  # naya Generator API (NB2 me detail)
images = rng.integers(0, 256, size=(4, 5, 5, 3), dtype=np.int64)
info("images", images)

# Ek pixel: image 0, row 2, col 3, saare channels
print("images[0, 2, 3] (R,G,B) =", images[0, 2, 3])

# Sirf Red channel nikalo: aakhri axis par index 0 -> shape (4,5,5)
red = images[..., 0]          # `...` (Ellipsis) = "beech ke saare axes jaisay hain"
info("red", red)

# Per-image per-channel mean brightness -> (batch, channels) = (4,3)
# axis=(1,2) matlab height aur width dono collapse kar do
mean_per_img_chan = images.mean(axis=(1, 2))
info("mean_per_img_chan", mean_per_img_chan)
print(mean_per_img_chan)
""")

M(r"""
## 2. Axis ka poora mental model (sab se ahem section)

### Kya hai
Jab tum `a.sum(axis=k)` likhte ho to NumPy **axis k ko khatam (collapse) kar deta hai**.
Baqi axes waise hi rehte hain.

```
a.shape = (3, 4)
a.sum(axis=0)  ->  axis 0 (jiska size 3 tha) gaya  ->  result shape (4,)
a.sum(axis=1)  ->  axis 1 (jiska size 4 tha) gaya  ->  result shape (3,)
```

### Rattne wala nahi, samajhne wala rule
> **"axis=k means: us axis ke saath saath safar karo aur values ko jama karte jao;
> jab safar khatam, wo axis gayab."**

2D ke liye asaan tarjuma:
- `axis=0` → **neeche ki taraf (rows ke aar-paar)** → har **column** ka jawab → "column-wise"
- `axis=1` → **daayen ki taraf (columns ke aar-paar)** → har **row** ka jawab → "row-wise"

### Common mistake (yahan sab phaste hain)
Log samajhte hain `axis=0` ka matlab "rows ka answer do". **Ghalat.**
`axis=0` rows ko **khatam** karta hai, is liye jawab **per-column** aata hai.
Shape check karo, confusion khatam:
result ki shape me jo number bacha hai wahi batata hai kis cheez ka jawab mila.
""")

C(r"""
# 2D par axis ka pehla proof — shape trace karo
sales = np.array([
    [120,  90, 150, 200],   # Lahore    : Q1..Q4
    [ 80, 110,  95, 130],   # Karachi
    [ 60,  70,  85,  90],   # Islamabad
])
cities  = ["Lahore", "Karachi", "Islamabad"]
quarters = ["Q1", "Q2", "Q3", "Q4"]
info("sales", sales)

total_all = sales.sum()                 # axis=None (default) -> sab kuch ek scalar
per_quarter = sales.sum(axis=0)         # rows collapse -> per COLUMN (per quarter)
per_city    = sales.sum(axis=1)         # cols collapse -> per ROW (per city)

print("total_all       :", total_all, " shape:", np.shape(total_all))
print("sum(axis=0)     :", per_quarter, " shape:", per_quarter.shape, "-> per quarter (4 quarters)")
print("sum(axis=1)     :", per_city,    " shape:", per_city.shape,    "-> per city (3 cities)")

# Shape se pehchano: 4 bacha => quarters ka jawab, 3 bacha => cities ka jawab
for c, v in zip(cities, per_city):
    print(f"  {c:<10} total = {v}")
assert per_quarter.tolist() == [260, 270, 330, 420]
assert per_city.tolist() == [560, 415, 305]
""")

C(r"""
# 3D par axis — yahan asli imtihan hai. shape (2,3,4)
cube = np.arange(24).reshape(2, 3, 4)
print("cube.shape =", cube.shape, "(2 tables, 3 rows, 4 cols)\n")

print("sum(axis=0).shape =", cube.sum(axis=0).shape, "-> tables collapse, (3,4) bacha")
print("sum(axis=1).shape =", cube.sum(axis=1).shape, "-> rows collapse,   (2,4) bacha")
print("sum(axis=2).shape =", cube.sum(axis=2).shape, "-> cols collapse,   (2,3) bacha")

# Tuple of axes: ek se ziyada axes ek sath collapse
print("sum(axis=(0,1)).shape =", cube.sum(axis=(0, 1)).shape, "-> sirf cols bache (4,)")
print("sum(axis=(1,2)).shape =", cube.sum(axis=(1, 2)).shape, "-> sirf tables bache (2,)")
print("sum(axis=None) =", cube.sum(axis=None), "(scalar, sab collapse)")

# Manual verification: axis=0 ka matlab element-wise dono tables ka jama
assert np.array_equal(cube.sum(axis=0), cube[0] + cube[1])
print("\nverified: cube.sum(axis=0) == cube[0] + cube[1]")
""")

C(r"""
# Negative axis — "aakhri se ginna". Ye general code likhne me bohat kaam aata hai.
cube = np.arange(24).reshape(2, 3, 4)
print("axis=-1 == axis=2 ?", np.array_equal(cube.sum(axis=-1), cube.sum(axis=2)))
print("axis=-2 == axis=1 ?", np.array_equal(cube.sum(axis=-2), cube.sum(axis=1)))

# Kyun useful? Aik hi function 1D, 2D, 3D par chal jaye:
def last_axis_mean(a):
    # "har row ka mean" — chahe a 1D ho, 2D ho ya 4D, axis=-1 hamesha andar wala axis hai
    return np.asarray(a).mean(axis=-1)

print("1D:", last_axis_mean([1, 2, 3, 4]))
print("2D:", last_axis_mean([[1, 2], [3, 100]]))
print("3D shape:", last_axis_mean(cube).shape)

# ML me axis=-1 ka classic use: softmax har sample ke features par
# (batch, classes) ho ya (batch, seq, classes) — axis=-1 hamesha "classes" hai.
""")

M(r"""
## 3. `keepdims=True` — broadcasting ka best friend

### Kya hai
Reduction ke baad jo axis gayab hota hai, `keepdims=True` usay **size 1** ke sath
zinda rakhta hai.

```
a.shape = (3, 4)
a.sum(axis=1)                 -> shape (3,)    <- axis gayab
a.sum(axis=1, keepdims=True)  -> shape (3, 1)  <- axis size-1 ban ke maujood
```

### Kyun zaroori hai
Normalization me original array ke sath **broadcast** karna hota hai.
`(3,4) / (3,)` → error ya ghalat natija, magar `(3,4) / (3,1)` → perfect row-wise division.

### Yaad rakhne ka jumla
> "Reduce karne ke baad agar wapis original array ke sath maths karna hai → `keepdims=True`."

### Interview tip
Softmax/layer-norm ki implementation me `keepdims=True` na lagana sab se aam bug hai.
Interviewer isi ko dekhta hai.
""")

C(r"""
# keepdims ka asli faida: row-wise normalization
mat = np.array([[1., 2., 3., 4.],
                [10., 20., 30., 40.],
                [5., 5., 5., 5.]])

s_no_keep = mat.sum(axis=1)                    # (3,)
s_keep    = mat.sum(axis=1, keepdims=True)     # (3,1)
print("without keepdims:", s_no_keep.shape, " with keepdims:", s_keep.shape)

# Sahi tareeqa — har row ka jama 1 ho jaye
row_norm = mat / s_keep
print("\nrow_norm:\n", row_norm)
print("har row ka sum:", row_norm.sum(axis=1))
assert np.allclose(row_norm.sum(axis=1), 1.0)

# Ghalat tareeqa — (3,4) / (3,) -> broadcasting rules fail (4 vs 3)
try:
    bad = mat / s_no_keep
except ValueError as e:
    print("\n[expected error] mat / s_no_keep ->", e)

# Purana (verbose) hal: reshape ya np.newaxis — keepdims isi ka shortcut hai
assert np.allclose(mat / s_no_keep[:, np.newaxis], row_norm)
assert np.allclose(mat / s_no_keep.reshape(-1, 1), row_norm)
print("newaxis / reshape se bhi wohi natija — keepdims sirf saaf syntax hai")
""")

C(r"""
# keepdims + 3D: per-image per-channel normalization (ML me rozana ka kaam)
rng = np.random.default_rng(0)
imgs = rng.random((4, 5, 5, 3)) * 255.0        # (batch, H, W, C)

mu    = imgs.mean(axis=(1, 2), keepdims=True)  # (4,1,1,3) -> broadcast ready
sigma = imgs.std(axis=(1, 2), keepdims=True)   # (4,1,1,3)
print("mu.shape:", mu.shape, " sigma.shape:", sigma.shape)

norm = (imgs - mu) / sigma                     # per image, per channel standardize
print("norm.shape:", norm.shape)
print("check mean ~0:", np.abs(norm.mean(axis=(1, 2))).max() < 1e-12)
print("check std  ~1:", np.allclose(norm.std(axis=(1, 2)), 1.0))
assert norm.shape == imgs.shape
""")

# ----------------------------------------------------------------- reductions
M(r"""
## 4. Reductions ki poori list (axis ke sath)

| Function | Kaam | Nan-safe version |
|---|---|---|
| `sum` | jama | `nansum` |
| `prod` | zarb | `nanprod` |
| `mean` | ausat | `nanmean` |
| `median` | darmiyani value | `nanmedian` |
| `std` / `var` | standard deviation / variance | `nanstd` / `nanvar` |
| `min` / `max` | sab se chhoti / bari | `nanmin` / `nanmax` |
| `ptp` | peak-to-peak (max - min) | — |
| `argmin` / `argmax` | chhoti/bari value ka **index** | `nanargmin` / `nanargmax` |
| `any` / `all` | koi True hai? / sab True hain? | — |
| `count_nonzero` | non-zero (ya True) ki ginti | — |

### Syntax
```python
np.sum(a, axis=None, dtype=None, out=None, keepdims=False, where=True)
a.sum(axis=..., keepdims=...)     # method form — wohi cheez
```

### Do gotchas
1. **`std` ka default `ddof=0`** (population). Sample std ke liye `ddof=1` do —
   pandas ka default `ddof=1` hai, is liye NumPy aur pandas ke numbers match nahi karte!
2. **`where=` parameter** — conditional reduction, magar `mean` me `where` ke sath
   count bhi adjust hota hai. Chhoti masking ke liye behtar hai boolean mask use karo.
""")

C(r"""
# Sab reductions ek sath, axis ke sath
data = np.array([[3., 7., 1., 9.],
                 [4., 4., 8., 2.],
                 [6., 5., 5., 5.]])

print("sum   axis=0:", data.sum(axis=0))
print("mean  axis=1:", data.mean(axis=1))
print("median axis=0:", np.median(data, axis=0))
print("std   axis=1 (ddof=0):", data.std(axis=1))
print("std   axis=1 (ddof=1):", data.std(axis=1, ddof=1), "<- sample std, pandas jaisa")
print("min   axis=0:", data.min(axis=0), " max axis=0:", data.max(axis=0))
print("ptp   axis=1:", np.ptp(data, axis=1), "(max - min)")
print("any   > 8 axis=1:", (data > 8).any(axis=1))
print("all   > 0 axis=1:", (data > 0).all(axis=1))
print("count_nonzero(data > 4, axis=0):", np.count_nonzero(data > 4, axis=0))

# ddof ka farq numbers me
x = np.array([2., 4., 4., 4., 5., 5., 7., 9.])
print("\npopulation std (ddof=0):", x.std())
print("sample     std (ddof=1):", x.std(ddof=1), "<- n-1 se taqseem")
print("formula check:", np.sqrt(((x - x.mean())**2).sum() / (len(x) - 1)))
""")

C(r"""
# where= parameter aur mask — conditional reduction ke do tareeqe
scores = np.array([88., -1., 92., -1., 75., 60.])    # -1 = missing marker
mask = scores >= 0

print("ghalat mean (missing shamil):", scores.mean())
print("mask se mean               :", scores[mask].mean())
print("where= se mean             :", scores.mean(where=mask))
print("sum with where=            :", scores.sum(where=mask))

# 2D me where= ka faida: har row me apni apni condition, shape barqarar
grid = np.array([[1., -1., 3.], [4., 5., -1.]])
m2 = grid > 0
print("\nrow-wise mean ignoring -1:", grid.mean(axis=1, where=m2))
# Note: agar kisi row me ek bhi valid value na ho to warning + nan aata hai.
""")

M(r"""
## 5. `argmin` / `argmax` aur `unravel_index` — sirf index nahi, **position**

### Kya hai
- `argmax(a)` → **flattened** array me sab se bari value ka index (default `axis=None`).
- `argmax(a, axis=k)` → axis k ke saath sab se bare ka index, baqi axes barqarar.
- `np.unravel_index(flat_index, shape)` → flat index ko `(row, col, ...)` me todta hai.
- `np.ravel_multi_index((r, c), shape)` → ulta kaam.

### Kyun use hota hai
- Classification: `pred = probs.argmax(axis=-1)` (sab se ziyada probability wala class)
- Image me sab se roshan pixel ki jagah dhoondhna
- Recommendation: top item ka id

### Common mistakes
1. `argmax` **value** nahi, **index** deta hai. Value chahiye to `a[a.argmax()]` ya `a.max()`.
2. 2D par `argmax()` bina axis → flat index milta hai (jo confuse karta hai) → `unravel_index` lagao.
3. **Ties**: barabar values me `argmax` **sab se pehla** index deta hai — hamesha.
""")

C(r"""
# argmax ka poora khel
probs = np.array([[0.1, 0.7, 0.2],
                  [0.6, 0.1, 0.3],
                  [0.2, 0.2, 0.6],
                  [0.9, 0.05, 0.05]])

pred = probs.argmax(axis=1)                 # har sample ka predicted class
print("predicted classes:", pred)
print("un classes ki probability:", probs.max(axis=1))
assert pred.tolist() == [1, 0, 2, 0]

# Flat argmax -> 2D position
flat = probs.argmax()                       # axis=None => flattened index
pos = np.unravel_index(flat, probs.shape)   # (row, col)
print("\nflat argmax index:", flat, " -> position (row,col):", pos)
print("value wahan:", probs[pos], " aur probs.max() =", probs.max())
assert probs[pos] == probs.max()

# ulta safar: (row,col) -> flat index
print("ravel_multi_index((3,0)):", np.ravel_multi_index((3, 0), probs.shape))

# argmin bhi wohi rules
print("\nargmin axis=0 (har column ka sab se kam):", probs.argmin(axis=0))
""")

C(r"""
# Ties (barabar values) ka rule — argmax pehla index deta hai
ties = np.array([5, 9, 3, 9, 9])
print("argmax:", ties.argmax(), "-> pehla 9 (index 1), aakhri nahi")

# Saare maximum positions chahiye to flatnonzero use karo
all_max = np.flatnonzero(ties == ties.max())
print("saare max positions:", all_max)

# Aakhri max ka index (trick): array ulta karo
last_max = len(ties) - 1 - ties[::-1].argmax()
print("aakhri max ka index:", last_max)
assert ties.argmax() == 1 and last_max == 4
""")

M(r"""
## 6. Cumulative operations — `cumsum`, `cumprod`, `diff`, `gradient`

### Kya hai
Ye reductions **nahi** hain — inka output input jitna (ya thora chhota) hota hai.

| Function | Kaam | Output size (n input par) |
|---|---|---|
| `cumsum` | chalta hua total (running total) | n |
| `cumprod` | chalta hua product | n |
| `diff` | consecutive farq `a[i+1]-a[i]` | n-1 |
| `ediff1d` | `diff` jaisa magar hamesha **flatten** + `to_begin/to_end` support | n-1 |
| `gradient` | central-difference derivative (kinaron par one-sided) | n |
| `trapezoid` | trapezoid rule se integral (area under curve) | scalar |

### Kyun use hota hai
- `cumsum` → running balance, prefix sums (LeetCode ka favourite!), CDF
- `cumprod` → compound growth, portfolio value
- `diff` → daily change, velocity, "increasing hai ya nahi" check
- `gradient` → numerical derivative (physics/engineering)
- `trapezoid` → AUC (area under ROC curve!) ki bunyad

### Gotcha
`diff` ka output **1 element chhota** hota hai — plotting/alignment me off-by-one bug ki jar.
Aage `to_begin=0` (`ediff1d`) ya `np.pad` se align karo.
""")

C(r"""
# cumsum / cumprod / diff
daily = np.array([100, -20, 50, -10, 30, 40])       # roz ka cash flow
print("daily      :", daily)
print("cumsum     :", np.cumsum(daily), "<- running balance")
print("diff       :", np.diff(daily), "<- consecutive change (size n-1 =", len(np.diff(daily)), ")")
print("ediff1d    :", np.ediff1d(daily, to_begin=0), "<- to_begin=0 se size wapis n")

growth = np.array([1.10, 1.05, 0.90, 1.20])          # saalana multipliers
print("\ncumprod    :", np.cumprod(growth), "<- compounded value")
print("total growth:", round(float(np.prod(growth)), 4))

# 2D par axis lazmi warna flatten ho jata hai (bara gotcha!)
m = np.array([[1, 2, 3], [4, 5, 6]])
print("\ncumsum bina axis (flatten!):", np.cumsum(m))
print("cumsum axis=1 (row-wise):\n", np.cumsum(m, axis=1))
print("cumsum axis=0 (col-wise):\n", np.cumsum(m, axis=0))
""")

C(r"""
# diff ka doosra order + gradient + trapezoid
pos = np.array([0., 1., 4., 9., 16., 25.])           # x = t^2 ki positions
print("first  diff (velocity approx):", np.diff(pos))
print("second diff (acceleration)   :", np.diff(pos, n=2))

# gradient: central difference, output input jitna (alignment ka masla nahi)
print("gradient:", np.gradient(pos))

# trapezoid — area under curve. y = x^2 ka 0..3 integral = 9
x = np.linspace(0, 3, 301)
y = x**2
area = np.trapezoid(y, x)                            # NumPy 2.x me naam `trapezoid` hai
print("\ntrapezoid area (approx 9.0):", round(float(area), 6))
assert abs(area - 9.0) < 1e-3

# Purana naam np.trapz NumPy 2.0 me hata diya gaya — ye gotcha yaad rakho
print("np.trapz maujood hai?", hasattr(np, "trapz"), "(NumPy 2.x me remove ho gaya)")

# 2D gradient: dono directions ki list milti hai
gy, gx = np.gradient(np.arange(12, dtype=float).reshape(3, 4))
print("2D gradient -> do arrays:", gy.shape, gx.shape)
""")

M(r"""
## 7. Order statistics — `sort`, `argsort`, `lexsort`, `partition`, `argpartition`

### `sort` vs `argsort`
- `np.sort(a)` → **values** sorted (copy). `a.sort()` → **in-place** (original badal jata hai!)
- `np.argsort(a)` → wo **indices** jo sorted order dete hain. `a[np.argsort(a)] == np.sort(a)`

`argsort` hi asli hero hai: ek array ke sort order se **doosre** arrays ko rearrange kar sakte ho
(pandas ke `sort_values` ka core idea).

### `kind` parameter
| kind | algorithm | stable? | speed |
|---|---|---|---|
| `'quicksort'` (default) | introsort | **nahi** | sab se tez |
| `'stable'` | radix/timsort | **haan** | thora slow |
| `'mergesort'` | = stable | haan | — |
| `'heapsort'` | heapsort | nahi | worst-case guarantee |

**Stable** ka matlab: barabar values apni original tarteeb me rehti hain — multi-key
sorting ke liye lazmi.

### Descending sort kaise?
NumPy me `reverse=True` **nahi** hota. Tareeqe:
- `np.sort(a)[::-1]` (1D), `np.sort(a, axis=1)[:, ::-1]` (2D)
- `np.argsort(-a)` (numeric ke liye trick)
""")

C(r"""
# sort vs argsort
a = np.array([50, 10, 40, 20, 30])
print("original :", a)
print("np.sort  :", np.sort(a), " (copy — original safe:", a, ")")

idx = np.argsort(a)
print("argsort  :", idx, "<- ye indices sorted order dete hain")
print("a[idx]   :", a[idx])
assert np.array_equal(a[idx], np.sort(a))

# argsort ka asli faida: ek key se doosre arrays ko sort karna
names = np.array(["Ali", "Sara", "Bilal", "Hina", "Usman"])
marks = np.array([72, 95, 61, 88, 79])
order = np.argsort(-marks)                 # minus => descending
print("\nRanking (marks descending):")
for r, i in enumerate(order, 1):
    print(f"  {r}. {names[i]:<7} {marks[i]}")
assert names[order][0] == "Sara"

# in-place sort ka gotcha
b = np.array([3, 1, 2])
b.sort()                                   # original tabdeel!
print("\nin-place ke baad b =", b, " <- .sort() method original badal deta hai")
""")

C(r"""
# 2D sorting — axis lazmi samjho
m = np.array([[3, 1, 2],
              [9, 7, 8],
              [6, 4, 5]])
print("original:\n", m)
print("\nsort(axis=1) — har row apne andar sorted:\n", np.sort(m, axis=1))
print("\nsort(axis=0) — har column apne andar sorted:\n", np.sort(m, axis=0))
print("\nsort(axis=None) — flatten ho kar sorted 1D:", np.sort(m, axis=None))
print("\ndescending rows:\n", np.sort(m, axis=1)[:, ::-1])

# GOTCHA: axis=0 se sort karne par rows TOOT jaati hain (records mix ho jate hain).
# Poori row ko ek record samajh kar sort karna hai to argsort + fancy indexing:
key = m[:, 0]                              # pehle column ko key banao
rows_sorted = m[np.argsort(key)]            # poori rows sath move karti hain
print("\nrows sorted by column 0 (records intact):\n", rows_sorted)
""")

C(r"""
# Stability ka asli demo — multi-key sort
# Pehle secondary key se sort karo, phir primary key se STABLE sort => dono kaam
dept  = np.array(["IT", "HR", "IT", "HR", "IT"])
sal   = np.array([500, 300, 700, 900, 500])
emp   = np.array(["A", "B", "C", "D", "E"])

step1 = np.argsort(-sal, kind="stable")                 # salary descending
step2 = np.argsort(dept[step1], kind="stable")          # phir dept par stable
final = step1[step2]
print("dept, salary, name (dept asc, salary desc):")
for i in final:
    print(f"  {dept[i]:<3} {sal[i]:<4} {emp[i]}")

# Yehi kaam lexsort ek line me karta hai — magar keys ULTI tarteeb me dete hain
# (aakhri key = primary key). Note: minus se descending.
lex = np.lexsort((-sal, dept))                          # primary = dept, secondary = -sal
print("\nlexsort natija:", [f"{dept[i]}-{sal[i]}-{emp[i]}" for i in lex])
assert list(lex) == list(final)
print("lexsort == manual stable chain  ✔")
""")

C(r"""
# lexsort ko theek se samjho: AAKHRI key sab se ahem
last_name  = np.array(["Khan", "Ali",  "Khan", "Ali"])
first_name = np.array(["Zara", "Bilal", "Ahmed", "Ayesha"])

order = np.lexsort((first_name, last_name))   # primary=last_name, secondary=first_name
print("Sorted by last name, phir first name:")
for i in order:
    print("  ", last_name[i], first_name[i])
assert [f"{last_name[i]},{first_name[i]}" for i in order] == \
       ["Ali,Ayesha", "Ali,Bilal", "Khan,Ahmed", "Khan,Zara"]

# Interview tip: "lexsort me keys reverse order me kyun?"
# Jawab: implementation stable sorts ka chain hai — pehli key sab se pehle apply hoti hai
# aur baad wali usay override karti hai, is liye aakhri key ka wazan sab se ziyada.
""")

M(r"""
## 8. `partition` / `argpartition` — top-k **O(n)** me (bohat ahem)

### Kya hai
Poora sort `O(n log n)` hai. Magar agar sirf "top 5" chahiye to poora sort **zaroori nahi**.
`partition` quickselect use karta hai: **average O(n)**.

`np.partition(a, kth)` guarantee deta hai:
- position `kth` par wohi element hai jo poore sort me wahan hota
- uske **baaen** sab chhote/barabar, **daaen** sab bare/barabar
- magar dono taraf ke elements **sorted nahi** hain

### Top-k ka recipe
```python
idx = np.argpartition(a, -k)[-k:]        # k sab se bare ke indices (unsorted)
top  = a[idx]                            # values
top_sorted = top[np.argsort(-top)]       # sirf k elements sort — sasta
```

### Kyun ahem
`n = 10 million`, `k = 10` par ye poore sort se bohat tez hai. LeetCode 215 / 347 ka
"heap" solution isi idea ka Python version hai.
""")

C(r"""
# partition ka behaviour samjho
a = np.array([7, 2, 9, 4, 1, 8, 3, 6, 5])
p = np.partition(a, 3)                    # kth = 3
print("original :", a)
print("partition(3):", p)
print("index 3 par:", p[3], "  (poore sort me bhi yahi hota:", np.sort(a)[3], ")")
print("baaen sab <= :", p[:3], " daaen sab >= :", p[4:], "(dono unsorted)")
assert p[3] == np.sort(a)[3]
assert (p[:3] <= p[3]).all() and (p[4:] >= p[3]).all()

# TOP-3 nikalna (bare wale) — O(n) tareeqa
k = 3
idx = np.argpartition(a, -k)[-k:]         # top-k ke indices (kisi bhi tarteeb me)
top_vals = a[idx]
top_sorted = top_vals[np.argsort(-top_vals)]
print("\ntop-3 indices:", idx, " values:", top_vals, " sorted:", top_sorted)
assert sorted(top_vals.tolist()) == [7, 8, 9]

# SMALLEST-3 — kth positive lo
idx_small = np.argpartition(a, k)[:k]
print("smallest-3:", np.sort(a[idx_small]))
assert sorted(a[idx_small].tolist()) == [1, 2, 3]
""")

C(r"""
# 2D top-k per row — argpartition + take_along_axis ka classic combo
scores = np.array([[0.1, 0.9, 0.3, 0.7],
                   [0.8, 0.2, 0.6, 0.4],
                   [0.5, 0.5, 0.95, 0.05]])
k = 2
part = np.argpartition(-scores, k - 1, axis=1)[:, :k]         # per-row top-k indices
vals = np.take_along_axis(scores, part, axis=1)               # unke values
# top-k ko andar se sort karo (descending)
order = np.argsort(-vals, axis=1)
top_idx  = np.take_along_axis(part, order, axis=1)
top_vals = np.take_along_axis(vals, order, axis=1)

print("per-row top-2 indices:\n", top_idx)
print("per-row top-2 values:\n", top_vals)
assert top_idx[0].tolist() == [1, 3]        # 0.9 phir 0.7
assert top_idx[2].tolist() == [2, 0] or top_idx[2].tolist() == [2, 1]  # tie 0.5/0.5
print("\nRecommendation systems me 'top-N items per user' bilkul aise nikalta hai.")
""")

C(r"""
# Timing ka andaza: partition vs full sort (chhota array, sirf idea ke liye)
import timeit
big = np.random.default_rng(1).random(200_000)

t_sort = timeit.timeit("np.sort(big)[-10:]", globals=globals(), number=20)
t_part = timeit.timeit("big[np.argpartition(big, -10)[-10:]]", globals=globals(), number=20)
print(f"full sort  : {t_sort:.4f}s")
print(f"argpartition: {t_part:.4f}s")
print(f"speedup    : ~{t_sort / max(t_part, 1e-9):.1f}x")
# Note: exact numbers machine par badalte hain; asal baat concept hai — O(n) vs O(n log n).
""")

# ----------------------------------------------------------------- searching
M(r"""
## 9. Searching — `searchsorted`, `where`, `nonzero` family

### `np.searchsorted(sorted_a, values, side='left')`
Binary search — `O(log n)`. Batata hai: "agar `values` ko `sorted_a` me daalna ho to
**kis index** par daalein ke sorting barqarar rahe?"

- `side='left'` → barabar values se **pehle** insert (`a[i-1] < v <= a[i]`)
- `side='right'` → barabar values ke **baad** insert

### Kahan use hota hai
1. **Binning / bucketing** — marks se grade (fastest tareeqa)
2. **Membership test** on sorted data
3. **Time-series alignment** — "is timestamp se pehle ka aakhri record kaun?"
4. **Weighted random sampling** — CDF par searchsorted (yehi `random.choices` ka core hai)

### `where` / `nonzero` khandan

| Function | Return | Kab |
|---|---|---|
| `np.where(cond, x, y)` | element-wise choose (ternary) | if-else vectorized |
| `np.where(cond)` | indices ka tuple (== `nonzero`) | positions chahiye |
| `np.nonzero(a)` | non-zero indices, per-axis tuple | multi-dim positions |
| `np.flatnonzero(a)` | flattened indices (1D) | 1D me sab se saaf |
| `np.argwhere(a)` | `(n, ndim)` shape ka array | har match ki poori coordinate |
| `np.extract(cond, a)` | matching values (== `a[cond]`) | values chahiye |
| `np.count_nonzero(a)` | ginti | "kitne match hue" |
| `np.select([c1,c2], [v1,v2], default)` | multi-condition where | nested if-elif |
""")

C(r"""
# searchsorted ki bunyad
sorted_a = np.array([10, 20, 30, 40, 50])
print("left  positions:", np.searchsorted(sorted_a, [5, 20, 35, 60], side="left"))
print("right positions:", np.searchsorted(sorted_a, [5, 20, 35, 60], side="right"))
# 20 ke liye: left -> 1 (20 se pehle), right -> 2 (20 ke baad). Yehi ahem farq hai.

# Kaam ki baat: duplicates ki ginti O(log n) me
dup = np.array([1, 2, 2, 2, 3, 5, 5])
lo = np.searchsorted(dup, 2, side="left")
hi = np.searchsorted(dup, 2, side="right")
print("\n2 kitni dafa hai?", hi - lo, "(indices", lo, "se", hi - 1, ")")
assert hi - lo == 3
""")

C(r"""
# Binning: marks -> grade (searchsorted ka best real use)
marks = np.array([95, 82, 71, 64, 55, 33, 100, 0])
edges = np.array([0, 50, 60, 70, 80, 90])            # grade boundaries (upper-open)
labels = np.array(["F", "D", "C", "B", "A", "A+"])

# side='right' - 1 => "is se bara ya barabar aakhri edge kaun sa hai"
bin_idx = np.searchsorted(edges, marks, side="right") - 1
grades = labels[bin_idx]
for m, g in zip(marks, grades):
    print(f"  {m:>3} -> {g}")
assert grades.tolist() == ["A+", "A", "B", "C", "D", "F", "A+", "F"]

# Yehi kaam np.digitize se bhi hota hai (dhyan: digitize 1-based bins deta hai)
print("\ndigitize:", np.digitize(marks, edges[1:]))   # 0..5 indices
assert np.array_equal(np.digitize(marks, edges[1:]), bin_idx)
""")

C(r"""
# where ke dono roop
temps = np.array([31., 45., 22., 38., 15., 41.])

# (1) Ternary form: cond ? x : y  — shapes broadcast hote hain
label = np.where(temps > 40, "HOT", "OK")
print("labels:", label)
capped = np.where(temps > 40, 40., temps)             # clipping bhi kar sakte hain
print("capped:", capped, " (np.clip(temps, None, 40) bhi wohi)")
assert np.allclose(capped, np.clip(temps, None, 40.))

# (2) Single-arg form: positions milte hain (tuple me!)
pos = np.where(temps > 40)
print("\nnp.where(cond) ->", pos, " type:", type(pos).__name__, "<- TUPLE hai")
print("indices:", pos[0], " values:", temps[pos])

# Nested if-elif => np.select (ya chained where)
cat = np.select(
    [temps > 40, temps > 30, temps > 20],
    ["hot", "warm", "mild"],
    default="cold",
)
print("\nselect ->", cat)
assert cat.tolist() == ["warm", "hot", "mild", "warm", "cold", "hot"]
""")

C(r"""
# nonzero khandan — 2D par farq saaf dikhta hai
grid = np.array([[0, 5, 0],
                 [7, 0, 9],
                 [0, 0, 0]])

print("nonzero      :", np.nonzero(grid), "<- (rows_array, cols_array)")
print("argwhere     :\n", np.argwhere(grid), "<- har match ki (row,col) ek row me")
print("flatnonzero  :", np.flatnonzero(grid), "<- flattened indices")
print("extract      :", np.extract(grid > 0, grid), " == grid[grid>0]:", grid[grid > 0])
print("count_nonzero:", np.count_nonzero(grid), " per column:", np.count_nonzero(grid, axis=0))

# Kaam ka pattern: coordinates par loop karna
for r, c in np.argwhere(grid > 6):
    print(f"  bari value {grid[r, c]} at row {r}, col {c}")

# Boolean array par bhi wohi kaam karta hai (True = non-zero)
assert np.array_equal(np.flatnonzero(np.array([False, True, True])), [1, 2])
""")

M(r"""
## 10. Set operations — `unique` aur uske teen jaadui flags

### `np.unique(a, return_index, return_inverse, return_counts, axis)`

| Flag | Kya deta hai | Use case |
|---|---|---|
| `return_index=True` | har unique value ka **pehla** index original me | "pehli dafa kahan aaya" |
| `return_inverse=True` | wo mapping jisse `unique[inverse] == a` | **label encoding!** |
| `return_counts=True` | har unique ki ginti | frequency table / mode |
| `axis=0` | poori **rows** ko unique treat karo | duplicate rows hatana |

`return_inverse` sab se qeemti hai — yehi machine learning ka **label encoding** hai
aur `bincount` ke sath mil kar **group-by** ban jata hai.

### Baqi set functions
`np.intersect1d`, `np.union1d`, `np.setdiff1d`, `np.setxor1d`, `np.isin`

### NumPy 2.0 gotcha
`np.in1d` **hata diya gaya** — ab sirf `np.isin` use karo.
`np.isin` input ki shape barqarar rakhta hai (broadcasting-friendly), `in1d` flatten karta tha.
""")

C(r"""
# unique ke saare flags ek sath
fruits = np.array(["apple", "mango", "apple", "banana", "mango", "apple"])

vals, first_idx, inverse, counts = np.unique(
    fruits, return_index=True, return_inverse=True, return_counts=True
)
print("unique values :", vals)
print("first index   :", first_idx)
print("inverse (codes):", inverse, "<- LABEL ENCODING free me!")
print("counts        :", counts)

# reconstruct proof
assert np.array_equal(vals[inverse], fruits)
print("\nvals[inverse] == original  ✔")

# Mode (sab se ziyada aane wali value)
print("mode:", vals[counts.argmax()], "count:", counts.max())
assert vals[counts.argmax()] == "apple"
""")

C(r"""
# unique(axis=0) — duplicate ROWS hatana
rows = np.array([[1, 2],
                 [3, 4],
                 [1, 2],
                 [5, 6],
                 [3, 4]])
print("unique rows:\n", np.unique(rows, axis=0))
print("bina axis (flatten ho jata hai — GALAT natija):", np.unique(rows))
assert np.unique(rows, axis=0).shape == (3, 2)

# unique sorted output deta hai. Original tarteeb chahiye to return_index use karo:
u, idx = np.unique(fruits, return_index=True)
first_seen_order = fruits[np.sort(idx)]
print("\nappearance order me unique:", first_seen_order)
assert first_seen_order.tolist() == ["apple", "mango", "banana"]
""")

C(r"""
# intersect1d / union1d / setdiff1d / setxor1d / isin
a = np.array([1, 2, 3, 4, 5, 5])
b = np.array([4, 5, 6, 7])

print("intersect1d :", np.intersect1d(a, b), "(sorted + unique)")
print("union1d     :", np.union1d(a, b))
print("setdiff1d   :", np.setdiff1d(a, b), "(a me hai, b me nahi)")
print("setxor1d    :", np.setxor1d(a, b), "(sirf ek me hai)")
print("isin        :", np.isin(a, b), "<- shape a jaisi (element-wise mask)")
print("a[isin]     :", a[np.isin(a, b)])

# return_indices — dono arrays me kahan mila
common, ia, ib = np.intersect1d(a, b, return_indices=True)
print("\ncommon:", common, " a ke indices:", ia, " b ke indices:", ib)
assert np.array_equal(a[ia], common) and np.array_equal(b[ib], common)

# isin 2D par bhi shape barqarar rakhta hai
g = np.array([[1, 9], [4, 5]])
print("\n2D isin:\n", np.isin(g, b))
print("np.in1d maujood?", hasattr(np, "in1d"), "<- NumPy 2.0 me remove")
""")

M(r"""
## 11. Counting & binning — `bincount`, `histogram`, `digitize`

### `np.bincount(x, weights=None, minlength=0)`
Sirf **non-negative integers** par chalta hai. `result[i]` = `i` kitni dafa aaya.

- `weights=` do to counting ki jagah **grouped sum** milta hai — ye group-by ka core hai!
- `minlength=` output ki minimum length force karta hai (missing categories ke liye lazmi)

### `np.histogram(a, bins, range, weights, density)`
Continuous data ke liye — `(counts, bin_edges)` return karta hai.
`bins` int ho sakta hai ya edges ki list, ya `'auto'` jaisi string.

### `np.digitize(x, bins, right=False)`
Har value ka bin number.

### Gotchas
1. `bincount` par negative value → `ValueError`. Pehle offset add karo (`x - x.min()`).
2. `bincount` ki length = `max(x) + 1`. Agar kuch categories missing hain to `minlength` do
   warna arrays ki shapes match nahi karengi.
3. `histogram` ka `bin_edges` **counts se ek ziyada** hota hai (n+1 edges for n bins).
""")

C(r"""
# bincount: counting + weighted (grouped) sum
clicks = np.array([0, 2, 1, 2, 2, 0, 3])        # kis ad par click hua (ad id)
print("bincount        :", np.bincount(clicks), "<- index = ad id, value = clicks")
print("minlength=6     :", np.bincount(clicks, minlength=6), "<- missing ads bhi 0 ke sath")

revenue = np.array([5., 3., 8., 2., 4., 6., 9.])  # us click ki revenue
per_ad = np.bincount(clicks, weights=revenue, minlength=4)
print("weighted sum    :", per_ad, "<- per-ad total revenue (GROUP BY!)")
counts = np.bincount(clicks, minlength=4)
print("per-ad average  :", per_ad / np.maximum(counts, 1), "<- divide-by-zero se bacha")
assert np.allclose(per_ad, [11., 8., 9., 9.])

# Negative values ka gotcha
try:
    np.bincount(np.array([-1, 2]))
except ValueError as e:
    print("\n[expected error] negative input:", e)
""")

C(r"""
# histogram / histogram2d / digitize
rng = np.random.default_rng(7)
heights = rng.normal(loc=170, scale=8, size=500)      # cm

counts, edges = np.histogram(heights, bins=5)
print("counts:", counts, " (sum =", counts.sum(), ")")
print("edges :", np.round(edges, 1), " <- edges ki tadaad =", len(edges), "= bins+1")
for i in range(len(counts)):
    print(f"  {edges[i]:6.1f} .. {edges[i+1]:6.1f} : {'#' * (counts[i] // 5)} {counts[i]}")

# density=True -> area 1 (probability density)
d, e = np.histogram(heights, bins=5, density=True)
print("\ndensity area =", round(float((d * np.diff(e)).sum()), 10))

# 2D histogram — do variables ka joint distribution
weights_kg = heights * 0.5 + rng.normal(0, 5, 500)
H, xe, ye = np.histogram2d(heights, weights_kg, bins=(3, 3))
print("\nhistogram2d counts:\n", H.astype(int), " total:", int(H.sum()))
assert int(H.sum()) == 500
""")

M(r"""
## 12. NaN aur inf ko handle karna

### NaN kya hai
`np.nan` = "Not a Number" — missing/undefined value ka float marker.
Iski do khatarnaak khaslatein:

1. **`nan != nan`** — apne aap ke barabar bhi nahi! (`np.nan == np.nan` → `False`)
   Is liye check ka sahi tareeqa `np.isnan(x)` hai.
2. **NaN phail jata hai (propagates)** — ek NaN poore `sum`/`mean` ko NaN bana deta hai.

### Poori `nan*` family (NaN ko ignore karti hai)
`nansum`, `nanprod`, `nanmean`, `nanmedian`, `nanstd`, `nanvar`, `nanmin`, `nanmax`,
`nanargmin`, `nanargmax`, `nanpercentile`, `nanquantile`, `nancumsum`, `nancumprod`

### Detect / replace
- `np.isnan(a)`, `np.isinf(a)`, `np.isfinite(a)`
- `np.nan_to_num(a, nan=0.0, posinf=..., neginf=...)`

### Gotchas
1. `nan` sirf **float** dtype me reh sakta hai. Integer array me NaN daalna namumkin —
   is liye missing data wale int columns automatically float ban jate hain.
2. `nanmean` par agar poori slice NaN ho → warning + `nan`.
3. Sorting me NaN **aakhir me** chala jata hai (`np.sort`), aur `a.max()` NaN de deta hai.
""")

C(r"""
# NaN ka bunyadi behaviour
x = np.array([1.0, 2.0, np.nan, 4.0, np.inf, -np.inf])
print("array:", x)
print("np.nan == np.nan ->", np.nan == np.nan, " (is liye isnan lazmi)")
print("isnan   :", np.isnan(x))
print("isinf   :", np.isinf(x))
print("isfinite:", np.isfinite(x))

print("\nmean (propagate):", x.mean(), " <- ek nan ne sab kharab kar diya")
clean = x[np.isfinite(x)]
print("finite values:", clean, " mean:", clean.mean())

# nan_to_num — nan/inf ko numbers se badlo
fixed = np.nan_to_num(x, nan=0.0, posinf=1e6, neginf=-1e6)
print("\nnan_to_num:", fixed)
assert np.isfinite(fixed).all()
""")

C(r"""
# nan-aware functions ka poora tour
data = np.array([[1., 2., np.nan, 4.],
                 [np.nan, 6., 7., 8.],
                 [9., 10., 11., 12.]])

print("mean    axis=0:", data.mean(axis=0), "<- nan phail gaya")
print("nanmean axis=0:", np.nanmean(data, axis=0), "<- nan ignore")
print("nansum  axis=1:", np.nansum(data, axis=1))
print("nanstd  axis=0:", np.round(np.nanstd(data, axis=0), 3))
print("nanmin/nanmax :", np.nanmin(data), np.nanmax(data))
print("nanmedian     :", np.nanmedian(data))
print("nanargmax     :", np.nanargmax(data), "(flat index)")
print("nanpercentile :", np.nanpercentile(data, [25, 50, 75]))
print("nancumsum row0:", np.nancumsum(data[0]), "<- nan ko 0 treat karta hai")

# nan ki ginti (missing data report)
print("\nper-column nan count:", np.isnan(data).sum(axis=0))
print("kul missing %:", round(100 * np.isnan(data).mean(), 2))
""")

C(r"""
# Missing values ko column mean se bharna (ML preprocessing ka classic step)
data = np.array([[1., 2., np.nan, 4.],
                 [np.nan, 6., 7., 8.],
                 [9., 10., 11., 12.]])
col_mean = np.nanmean(data, axis=0)                  # nan ignore kar ke mean
nan_pos = np.isnan(data)                             # kahan kahan missing hai
filled = data.copy()
filled[nan_pos] = np.take(col_mean, np.where(nan_pos)[1])   # us column ka mean daalo

print("column means:", np.round(col_mean, 3))
print("filled:\n", np.round(filled, 3))
assert not np.isnan(filled).any()

# Aur bhi saaf tareeqa (broadcasting se):
filled2 = np.where(nan_pos, np.broadcast_to(col_mean, data.shape), data)
assert np.allclose(filled, filled2)
print("\ndono tareeqe barabar ✔  (np.where wala ziyada readable hai)")
""")

C(r"""
# inf kaise paida hota hai + errstate se warnings control
a = np.array([1.0, -1.0, 0.0])
b = np.array([0.0, 0.0, 0.0])

with np.errstate(divide="ignore", invalid="ignore"):   # warning band (context manager)
    r = a / b
print("1/0 =", r[0], " -1/0 =", r[1], " 0/0 =", r[2], " <- inf, -inf, nan")

# Safe division ka pattern (ML me loss functions me lazmi)
safe = np.divide(a, b, out=np.zeros_like(a), where=(b != 0))
print("safe divide (0 jahan denominator 0):", safe)
assert np.allclose(safe, [0., 0., 0.])

# inf ke sath arithmetic ke rules
print("\ninf - inf =", np.inf - np.inf, " (nan)")
print("inf * 0   =", np.float64(np.inf) * 0.0, " (nan)")
print("1/inf     =", 1 / np.inf, " (0.0)")
print("inf > 1e308:", np.inf > 1e308)
""")

M(r"""
## 13. Masked arrays (`np.ma`) — missing data ka "official" tareeqa

### Kya hai
`np.ma.masked_array(data, mask)` ek array + boolean mask ka jora hai. Jahan mask `True`
hai wo element "masked" (chhupa hua) hai aur **saare** operations use khud-ba-khud
ignore kar dete hain — `nanmean` jaisa alag function nahi chahiye.

### Kyun / kab
- Sensor data jahan sirf kuch readings kharab hain
- Integer arrays me missing values (NaN int me nahi reh sakta, mask reh sakta hai!)
- Astronomy / geoscience libraries me common

### Aaj ki haqeeqat (interview me ye kehna)
Naye code me log ziyada tar **pandas** (`NaN`/`pd.NA`) ya plain `nan*` functions use karte hain.
`np.ma` powerful hai magar slow aur kuch libraries ke sath compatible nahi.
Phir bhi legacy code me milta hai, is liye pehchan lazmi hai.
""")

C(r"""
# masked array ka demo
readings = np.array([21, 22, -999, 24, -999, 26])     # -999 = sensor error (INT array!)
m = np.ma.masked_equal(readings, -999)                # -999 ko mask kar do

print("masked array:", m)
print("mask        :", m.mask)
print("mean (masked ignore):", m.mean(), " <- galat -999 shamil nahi")
print("plain mean (galat)  :", readings.mean())
print("count valid :", m.count())
assert m.mean() == np.mean([21, 22, 24, 26])

# float data ke liye masked_invalid (nan/inf ko mask karta hai)
f = np.ma.masked_invalid(np.array([1.0, np.nan, 3.0, np.inf]))
print("\nmasked_invalid:", f, " sum:", f.sum())

# filled() se wapis normal array
print("filled(0):", m.filled(0))
print("compressed() (sirf valid):", m.compressed())
print("\nma.masked_where(cond, a) se apni marzi ki condition:",
      np.ma.masked_where(readings > 24, readings))
""")

# ----------------------------------------------------------------- advanced indexing
M(r"""
## 14. Advanced (fancy) indexing deep dive

### Teen tarah ki indexing
| Type | Misal | Result | Copy ya View? |
|---|---|---|---|
| Basic (slicing) | `a[1:3, ::2]` | strided window | **VIEW** |
| Advanced (integer arrays) | `a[[0,2], [1,3]]` | naya array | **COPY** |
| Boolean mask | `a[a > 5]` | naya 1D array | **COPY** |

### Integer-array indexing ka asli rule (yaad rakho)
```
a[rows, cols]   ->   result[i] = a[rows[i], cols[i]]
```
Yaani indices **zip** hote hain, aur pehle **broadcast** hote hain.
**Result ki shape = index arrays ki broadcast shape** (array ki shape se koi lena dena nahi).

### Sab se bara confusion
`a[[0,2], [1,3]]` **do elements** deta hai (`a[0,1]` aur `a[2,3]`) — 2x2 submatrix **nahi**!
Submatrix ke liye `np.ix_` ya reshape se broadcasting chahiye.
""")

C(r"""
# Fancy indexing ka bunyadi rule: indices zip hote hain
a = np.arange(20).reshape(4, 5)
print("a:\n", a)

rows = np.array([0, 2, 3])
cols = np.array([1, 3, 4])
picked = a[rows, cols]                      # (0,1), (2,3), (3,4)
print("\na[rows, cols] =", picked, " shape:", picked.shape)
assert picked.tolist() == [1, 13, 19]

# Result ki shape index arrays ki shape follow karti hai — 2D indices do to 2D result
r2 = np.array([[0, 1], [2, 3]])
c2 = np.array([[0, 0], [4, 4]])
print("\n2D index arrays -> 2D result:\n", a[r2, c2], " shape:", a[r2, c2].shape)

# Broadcasting: column vector + row vector => outer combination (submatrix!)
sub = a[rows[:, None], cols[None, :]]       # (3,1) x (1,3) -> (3,3)
print("\nbroadcast se 3x3 submatrix:\n", sub)
assert sub.shape == (3, 3)
""")

C(r"""
# np.ix_ — submatrix ka saaf tareeqa (open mesh banata hai)
a = np.arange(20).reshape(4, 5)
rows = [0, 2, 3]
cols = [1, 3, 4]

print("GALAT (zip ho gaya):", a[rows, cols])
sub = a[np.ix_(rows, cols)]
print("\nnp.ix_ se sahi submatrix:\n", sub, " shape:", sub.shape)

# ix_ andar kya karta hai? shapes dekho:
r_mesh, c_mesh = np.ix_(rows, cols)
print("\nix_ output shapes:", r_mesh.shape, c_mesh.shape, "<- (3,1) aur (1,3): broadcast ready")
assert np.array_equal(sub, a[np.array(rows)[:, None], np.array(cols)[None, :]])

# ix_ boolean masks ke sath bhi chalta hai
mask_r = np.array([True, False, True, False])
mask_c = np.array([False, True, True, False, False])
print("\nboolean ix_:\n", a[np.ix_(mask_r, mask_c)])
""")

M(r"""
## 15. `take_along_axis` / `put_along_axis` — `argsort`/`argmax` ke sache saathi

### Masla
`argsort(axis=1)` per-row indices deta hai. Un indices se **values** kaise nikalein?
`a[idx]` kaam nahi karega (wo axis 0 par index karega). Manual `np.arange` broadcasting
likhni parti hai — bad-soorat aur bug-prone.

### Hal
```python
np.take_along_axis(a, indices, axis)   # values nikalo (a aur indices ki shape same axis par match)
np.put_along_axis(a, indices, values, axis)   # in-place likho
```

### Kahan use hota hai
- Per-row sorting by ek key column
- Top-k values nikalna (`argpartition` ke baad)
- `argmax` se predicted class ki probability nikalna
- Beam search / attention me best candidate uthana
""")

C(r"""
# take_along_axis: argsort ke sath
scores = np.array([[0.3, 0.9, 0.1],
                   [0.7, 0.2, 0.5]])
order = np.argsort(-scores, axis=1)              # descending per row
print("order:\n", order)

# Purana takleef-deh tareeqa (manual broadcasting)
manual = scores[np.arange(scores.shape[0])[:, None], order]
# Saaf tareeqa
vals = np.take_along_axis(scores, order, axis=1)
print("\ntake_along_axis:\n", vals)
assert np.allclose(manual, vals)

# argmax se probability nikalna (keepdims lazmi taake shape match ho)
best = scores.argmax(axis=1, keepdims=True)      # (2,1)
best_p = np.take_along_axis(scores, best, axis=1)
print("\nbest class:", best.ravel(), " best prob:", best_p.ravel())
assert np.allclose(best_p.ravel(), scores.max(axis=1))
""")

C(r"""
# put_along_axis: har row me max wali jagah par 1 likho (one-hot banane ka tareeqa)
scores = np.array([[0.3, 0.9, 0.1],
                   [0.7, 0.2, 0.5]])
onehot = np.zeros_like(scores)
idx = scores.argmax(axis=1, keepdims=True)
np.put_along_axis(onehot, idx, 1.0, axis=1)      # IN-PLACE likhta hai
print("one-hot of argmax:\n", onehot)
assert onehot.tolist() == [[0., 1., 0.], [1., 0., 0.]]

# Poori table ko ek column ke hisaab se sort karna (records intact)
table = np.array([[3, 100],
                  [1, 300],
                  [2, 200]])
sorted_table = table[np.argsort(table[:, 0])]     # column 0 ke hisaab se
print("\ncolumn 0 se sorted (rows intact):\n", sorted_table)
assert sorted_table[:, 1].tolist() == [300, 200, 100]
""")

M(r"""
## 16. `np.choose` — index array se "kaun sa source" chunna

### Kya hai
`np.choose(idx, [arr0, arr1, arr2])` → `result[i] = arr{idx[i]}[i]`.
Yaani har position par batao "kaun se array se value lo".

### Kab use karein
- Multi-branch logic jahan `np.where` nested karna parta
- Piecewise functions (har region ka apna formula)

### Gotcha
`choose` ki limit hai (32 arrays) aur padhne me mushkil hai. Aaj kal `np.select` ya
`np.where` ki chain ziyada readable samjhi jati hai.
""")

C(r"""
# choose ka demo — piecewise formula
x = np.array([-5., -1., 0., 2., 8.])
region = np.digitize(x, [0., 5.])                 # 0: x<0, 1: 0<=x<5, 2: x>=5
print("region codes:", region)

opts = [ -x,        # region 0: absolute value
          x**2,     # region 1: square
          x * 10 ]  # region 2: scale
out = np.choose(region, opts)
print("choose ka natija:", out)
assert out.tolist() == [5., 1., 0., 4., 80.]

# Wohi kaam np.select se (ziyada readable)
out2 = np.select([x < 0, x < 5], [-x, x**2], default=x * 10)
assert np.allclose(out, out2)
print("np.select se bhi wohi ✔ (aaj kal select/where preferred hai)")
""")

M(r"""
## 17. `np.add.at` — unbuffered scatter (ye interview ka trap sawal hai)

### Masla
```python
a = np.zeros(3)
a[[0, 0, 1]] += 1      # tumhein lagta hai a[0] do baar barhega -> [2,1,0]
```
**Nahi!** Natija `[1, 1, 0]` aata hai.

### Kyun?
`a[idx] += 1` asal me teen steps hai: **fetch → add → store** (buffered).
Fetch ek dafa hoti hai (purani values), add hota hai, phir store. Duplicate index ki
aakhri write baqi ko **overwrite** kar deti hai — pehli increment gum ho gayi.

### Hal
`np.add.at(a, idx, values)` — **unbuffered** in-place operation.
Duplicate indices par sahi jama karta hai (scatter-add).

Har ufunc ka `.at` hota hai: `np.add.at`, `np.subtract.at`, `np.multiply.at`,
`np.maximum.at`, `np.minimum.at`.

### Kahan zaroori hota hai
- Histogram / group-by sums jahan indices repeat hote hain
- Sparse gradient accumulation (embedding layers ka backward pass — asli deep learning!)
- Graph algorithms me neighbours ka jama

### Gotcha
`np.add.at` **slow** hai (buffering ka faida nahi milta). Non-negative int keys ke liye
`np.bincount(..., weights=...)` bohat tez hai — jahan mumkin ho wo use karo.
""")

C(r"""
# Buffered vs unbuffered — farq apni aankhon se dekho
idx = np.array([0, 0, 1, 2, 2, 2])

buffered = np.zeros(3)
buffered[idx] += 1                      # GHALAT (duplicates gum)
print("a[idx] += 1      ->", buffered, "<- ghalat! duplicates count nahi hue")

unbuffered = np.zeros(3)
np.add.at(unbuffered, idx, 1)           # SAHI
print("np.add.at        ->", unbuffered, "<- sahi scatter-add")

fast = np.bincount(idx, minlength=3).astype(float)
print("np.bincount      ->", fast, "<- wohi natija, sab se tez")

assert buffered.tolist() == [1., 1., 1.]
assert unbuffered.tolist() == [2., 1., 3.]
assert np.array_equal(unbuffered, fast)

# maximum.at bhi kaam ka hai: per-key maximum
mx = np.full(3, -np.inf)
np.maximum.at(mx, idx, np.array([5., 9., 2., 1., 7., 3.]))
print("\nper-key maximum:", mx)
assert mx.tolist() == [9., 2., 7.]
""")

C(r"""
# 2D scatter-add — embedding gradient jaisa pattern
n_words, dim = 5, 3
grad_table = np.zeros((n_words, dim))                 # har word ka gradient
sentence = np.array([1, 3, 1, 1, 4])                  # word ids (1 teen dafa!)
grads = np.ones((len(sentence), dim))                 # har occurrence ka gradient

np.add.at(grad_table, sentence, grads)                # sahi accumulation
print("grad_table:\n", grad_table)
print("word 1 ka gradient (3 dafa aaya):", grad_table[1])
assert grad_table[1].tolist() == [3., 3., 3.]
assert grad_table[0].tolist() == [0., 0., 0.]
print("\nDeep learning me embedding layer ka backward pass bilkul aisa hi hota hai.")
""")

M(r"""
## 18. Group-by emulation — pandas ke baghair

### Recipe (yaad kar lo, bohat kaam aati hai)
```python
keys_unique, codes = np.unique(keys, return_inverse=True)   # 1. label encode
sums   = np.bincount(codes, weights=values)                  # 2. grouped sum
counts = np.bincount(codes)                                  # 3. group sizes
means  = sums / counts                                       # 4. grouped mean
```

Multi-column values ke liye `np.add.at` use karo (`bincount` sirf 1D weights leta hai).

### Kyun seekhna zaroori
1. Interview: "pandas ke baghair group-by kaise karoge?"
2. Performance: chhoti/medium data par ye pandas se bhi tez ho sakta hai
3. Yehi logic GPU frameworks (`scatter_add`) me use hota hai
""")

C(r"""
# Group-by: category-wise revenue aur average
cat = np.array(["food", "tech", "food", "toys", "tech", "food"])
amt = np.array([100., 500., 250., 80., 300., 150.])

uniq, codes = np.unique(cat, return_inverse=True)
g_sum   = np.bincount(codes, weights=amt)
g_count = np.bincount(codes)
g_mean  = g_sum / g_count
g_max   = np.full(len(uniq), -np.inf); np.maximum.at(g_max, codes, amt)

print(f"{'category':<8} {'count':>5} {'sum':>8} {'mean':>8} {'max':>7}")
for i, u in enumerate(uniq):
    print(f"{u:<8} {int(g_count[i]):>5} {g_sum[i]:>8.1f} {g_mean[i]:>8.1f} {g_max[i]:>7.1f}")

assert uniq.tolist() == ["food", "tech", "toys"]
assert g_sum.tolist() == [500., 800., 80.]
assert g_mean[0] == 500. / 3

# pandas se cross-check (bilkul wohi natija)
import pandas as pd
chk = pd.Series(amt).groupby(pd.Series(cat)).sum()
assert np.allclose(chk.to_numpy(), g_sum)
print("\npandas groupby se match ✔")
""")

C(r"""
# Multi-column grouped sum — np.add.at (2D)
region = np.array([0, 1, 0, 2, 1])               # region id
metrics = np.array([[10., 1.],                    # [sales, returns]
                    [20., 2.],
                    [30., 3.],
                    [40., 4.],
                    [50., 5.]])
out = np.zeros((3, 2))
np.add.at(out, region, metrics)                   # per-region sales aur returns
print("per-region [sales, returns]:\n", out)
assert out.tolist() == [[40., 4.], [70., 7.], [40., 4.]]

# 2D pivot table: (region x category) grouped sum -> flat index trick
cat2 = np.array([0, 1, 1, 0, 0])
pivot = np.zeros((3, 2))
np.add.at(pivot, (region, cat2), metrics[:, 0])   # tuple of index arrays!
print("\npivot (region x category) sales:\n", pivot)
assert pivot.tolist() == [[10., 30.], [50., 20.], [40., 0.]]
""")

M(r"""
## 19. `apply_along_axis` — chalta hai, magar slow kyun?

### Kya hai
`np.apply_along_axis(func1d, axis, arr)` — har 1D slice par tumhara Python function chalata hai.

### Kyun slow
Ye asal me **Python loop** hai! Har slice ke liye Python-level function call hota hai
(interpreter overhead), C-level vectorization ka koi faida nahi.
Ye "vectorized" nahi, sirf "convenient" hai.

### Kab theek hai
- Function genuinely vectorize nahi ho sakta (koi complex custom logic)
- Rows ki tadaad kam hai
- Readability qeemti hai aur performance masla nahi

### Behtar options
1. Built-in reduction with `axis=` (hamesha pehli koshish)
2. Broadcasting se manual formula
3. `np.einsum` ya matrix ops
4. Aakhri chara: `apply_along_axis` / explicit loop
""")

C(r"""
# apply_along_axis vs built-in axis — result same, speed different
import timeit
m = np.random.default_rng(3).random((400, 50))

def my_range(row):                              # custom 1D function
    return row.max() - row.min()

slow = np.apply_along_axis(my_range, 1, m)
fast = m.max(axis=1) - m.min(axis=1)            # built-in, C level
assert np.allclose(slow, fast)

t1 = timeit.timeit("np.apply_along_axis(my_range, 1, m)", globals=globals(), number=20)
t2 = timeit.timeit("m.max(axis=1) - m.min(axis=1)", globals=globals(), number=20)
print(f"apply_along_axis : {t1:.4f}s")
print(f"built-in axis    : {t2:.4f}s")
print(f"speedup          : ~{t1 / max(t2, 1e-9):.1f}x  (built-in jeet gaya)")

# apply_along_axis ka jaiz use: aisa function jo vectorize karna mushkil ho
def top2_gap(row):
    s = np.sort(row)
    return s[-1] - s[-2]
print("\ntop-2 gap (pehli 5 rows):", np.round(np.apply_along_axis(top2_gap, 1, m)[:5], 3))
# (ye bhi vectorize ho sakta hai: np.sort(m,axis=1)[:,-1] - np.sort(m,axis=1)[:,-2])
""")

# ----------------------------------------------------------------- gotchas
M(r"""
## 20. Common Mistakes / Gotchas — "yahan log phaste hain"

1. **`axis=0` ka matlab "rows ka jawab" samajhna.** Ghalat — `axis=0` rows ko **collapse**
   karta hai, jawab **per-column** aata hai. Hamesha `result.shape` print karo.
2. **`keepdims` bhool jana** → broadcasting error ya (worse) chupa hua ghalat natija.
3. **`std()` ka `ddof=0` default** → pandas (`ddof=1`) se numbers match nahi karte.
4. **`a.sort()` vs `np.sort(a)`** → method in-place hai, original tabah kar deta hai.
5. **`cumsum` bina `axis`** 2D par flatten kar deta hai.
6. **`diff` ka output 1 chhota** → off-by-one alignment bug.
7. **`argmax` value nahi index deta**, aur ties me pehla index.
8. **`a[[0,2],[1,3]]` submatrix nahi deta** — zip karta hai. `np.ix_` use karo.
9. **`a[idx] += 1` duplicate indices par ghalat** → `np.add.at` ya `bincount`.
10. **`np.nan == np.nan` False** → `np.isnan` lazmi. Integer array me NaN nahi reh sakta.
11. **`bincount` negative par error**, aur length `max+1` — `minlength` do.
12. **`unique` sorted deta hai**, appearance order nahi — `return_index` chahiye.
13. **Fancy indexing copy hai, slicing view** — in-place update ka natija badal jata hai.
14. **`np.in1d`, `np.trapz`, `np.float_` NumPy 2.0 me hata diye gaye** — `isin`,
    `trapezoid`, `np.float64` use karo.
15. **`where=` ke sath `mean`** par agar poora group masked ho to `nan` + warning.
""")

C(r"""
# Gotcha demos ek jagah — chala kar dekho
print("--- 1) fancy indexing COPY hai, slicing VIEW ---")
a = np.arange(6)
view = a[1:4]; view[0] = 99            # original par asar
copy_ = a[[1, 2, 3]]; copy_[1] = -1     # original par koi asar nahi
print("a =", a, " (index 1 badla, index 2 nahi)")
print("a[1:4].base is a ?", a[1:4].base is a, " | a[[1,2,3]].base is None ?",
      a[[1, 2, 3]].base is None)

print("\n--- 2) reshape ka view, transpose ka non-contiguous view ---")
b = np.arange(6).reshape(2, 3)
print("b.T ka C_CONTIGUOUS:", b.T.flags["C_CONTIGUOUS"], " (transpose sirf strides badalta hai)")

print("\n--- 3) axis confusion ka reality check ---")
m = np.arange(6).reshape(2, 3)
print("m.shape:", m.shape, " sum(axis=0).shape:", m.sum(axis=0).shape,
      " sum(axis=1).shape:", m.sum(axis=1).shape)

print("\n--- 4) integer array me nan daalne ki koshish ---")
try:
    ints = np.array([1, 2, 3])
    ints[0] = np.nan
except ValueError as e:
    print("[expected error]", e)

print("\n--- 5) bincount ki length ---")
x = np.array([0, 5])
print("bincount(x) length:", len(np.bincount(x)), "<- max+1 = 6, beech ke sab 0")
""")

# ----------------------------------------------------------------- real world
M(r"""
## 21. Real-World Problems

Ab sab tools ko mila kar 5 asli masle hal karte hain. Har hal me pehle **soch**, phir code.
""")

M(r"""
### Problem 1 — Student result system
Ek class ke 6 students, 4 subjects. Nikalna hai:
- har student ka total aur percentage
- har subject ka average, highest, lowest
- top-3 students (`argpartition` se, poora sort nahi)
- har student ki grade (`searchsorted` se binning)
- kaun kis subject me sab se acha hai (`argmax(axis=1)`)
""")

C(r"""
students = np.array(["Ali", "Sara", "Bilal", "Hina", "Usman", "Ayesha"])
subjects = np.array(["Math", "Physics", "Chem", "English"])
marks = np.array([
    [88, 92, 79, 85],   # Ali
    [95, 88, 91, 90],   # Sara
    [62, 58, 71, 66],   # Bilal
    [78, 84, 88, 92],   # Hina
    [45, 52, 60, 58],   # Usman
    [90, 95, 85, 88],   # Ayesha
])

total = marks.sum(axis=1)                      # per student (rows barqarar)
pct   = total / (marks.shape[1] * 100) * 100    # percentage

print("Per-student:")
for i, s in enumerate(students):
    print(f"  {s:<8} total={total[i]:>3}  pct={pct[i]:5.1f}%")

print("\nPer-subject stats (axis=0 => columns bachte hain):")
print(f"  {'subject':<9} {'avg':>6} {'max':>4} {'min':>4} {'std':>6}")
for j, sub in enumerate(subjects):
    print(f"  {sub:<9} {marks[:, j].mean():>6.1f} {marks[:, j].max():>4}"
          f" {marks[:, j].min():>4} {marks[:, j].std(ddof=1):>6.2f}")

# Top-3 students — O(n) partition
k = 3
top_idx = np.argpartition(-total, k - 1)[:k]
top_idx = top_idx[np.argsort(-total[top_idx])]
print("\nTop-3:", [f"{students[i]}({total[i]})" for i in top_idx])
assert students[top_idx[0]] == "Sara"

# Grade binning
edges = np.array([0, 50, 60, 70, 80, 90])
labels = np.array(["F", "D", "C", "B", "A", "A+"])
grades = labels[np.searchsorted(edges, pct, side="right") - 1]
print("Grades:", dict(zip(students.tolist(), grades.tolist())))

# Har student ka best subject
best_sub = subjects[marks.argmax(axis=1)]
print("Best subject:", dict(zip(students.tolist(), best_sub.tolist())))
assert best_sub[0] == "Physics"
""")

M(r"""
### Problem 2 — Sensor data cleaning (NaN + outliers)
5 sensors, 20 timestamps. Data me NaN bhi hain aur kuch outliers bhi.
Kaam: missing report, outlier detection (z-score), cleaning, per-sensor stats.
""")

C(r"""
rng = np.random.default_rng(11)
temps = rng.normal(25, 2, size=(5, 20))            # (sensors, time)
# Jaan boojh kar kharabi daalo
temps[1, 3] = np.nan
temps[1, 4] = np.nan
temps[3, 10] = 90.0                                 # outlier (sensor jal gaya)
temps[0, 0] = np.nan

# 1) Missing report
nan_mask = np.isnan(temps)
print("per-sensor NaN count:", nan_mask.sum(axis=1))
print("kul missing %:", round(100 * nan_mask.mean(), 2))

# 2) Outlier detection (per sensor z-score, NaN ko ignore karke)
mu = np.nanmean(temps, axis=1, keepdims=True)       # keepdims => broadcast ready
sd = np.nanstd(temps, axis=1, keepdims=True)
z = np.abs((temps - mu) / sd)
out_mask = z > 3
print("\noutlier positions (sensor, t):", np.argwhere(out_mask).tolist())
assert out_mask[3, 10]

# 3) Cleaning: outlier ko NaN banao, phir per-sensor median se bharo
clean = temps.copy()
clean[out_mask] = np.nan
med = np.nanmedian(clean, axis=1, keepdims=True)
clean = np.where(np.isnan(clean), np.broadcast_to(med, clean.shape), clean)
assert np.isfinite(clean).all()

print("\nper-sensor mean (before -> after):")
for i in range(5):
    print(f"  sensor{i}: {np.nanmean(temps[i]):6.2f} -> {clean[i].mean():6.2f}")
print("\nsensor3 ka mean theek hua kyunke 90.0 outlier hat gaya ✔")
""")

M(r"""
### Problem 3 — E-commerce order log par group-by
Orders ka log hai (category, city, amount). Nikalna hai:
- per-category revenue aur order count (`unique` + `bincount`)
- per-(city × category) pivot table (`np.add.at`)
- sab se ziyada kamane wali category
- average order value per city
""")

C(r"""
categories = np.array(["food", "tech", "food", "toys", "tech", "food", "tech", "toys"])
cities     = np.array(["LHR", "KHI", "KHI", "LHR", "LHR", "ISB", "KHI", "KHI"])
amounts    = np.array([1200., 45000., 800., 2500., 38000., 1500., 52000., 1900.])

cat_u, cat_code = np.unique(categories, return_inverse=True)
cty_u, cty_code = np.unique(cities, return_inverse=True)

rev   = np.bincount(cat_code, weights=amounts)
cnt   = np.bincount(cat_code)
aov   = rev / cnt                                   # average order value

print(f"{'category':<8} {'orders':>6} {'revenue':>10} {'AOV':>9}")
for i, c in enumerate(cat_u):
    print(f"{c:<8} {int(cnt[i]):>6} {rev[i]:>10.0f} {aov[i]:>9.0f}")
print("\nTop category:", cat_u[rev.argmax()], "revenue:", rev.max())
assert cat_u[rev.argmax()] == "tech"

# Pivot: city x category revenue
pivot = np.zeros((len(cty_u), len(cat_u)))
np.add.at(pivot, (cty_code, cat_code), amounts)
print("\nPivot (rows=city, cols=category):")
print("        " + "".join(f"{c:>9}" for c in cat_u))
for i, c in enumerate(cty_u):
    print(f"{c:<8}" + "".join(f"{v:>9.0f}" for v in pivot[i]))
assert pivot.sum() == amounts.sum()

# Per-city AOV
city_rev = np.bincount(cty_code, weights=amounts)
city_cnt = np.bincount(cty_code)
print("\nPer-city AOV:", dict(zip(cty_u.tolist(), np.round(city_rev / city_cnt).tolist())))
""")

M(r"""
### Problem 4 — Image batch processing (4D axes ka asli imtihan)
8 synthetic images `(8, 16, 16, 3)`. Kaam:
- per-image per-channel normalization (`keepdims`)
- sab se roshan image dhoondho
- har image ka sab se roshan pixel ki position (`argmax` + `unravel_index`)
- 2x2 max-pooling reshape trick se
""")

C(r"""
rng = np.random.default_rng(5)
batch = rng.integers(0, 256, size=(8, 16, 16, 3)).astype(np.float64)
batch[3] += 40.0                                        # image 3 ko roshan kar do
batch = np.clip(batch, 0, 255)
print("batch shape:", batch.shape, "(N, H, W, C)")

# 1) Per-image per-channel standardize
mu  = batch.mean(axis=(1, 2), keepdims=True)            # (8,1,1,3)
sd  = batch.std(axis=(1, 2), keepdims=True)
norm = (batch - mu) / sd
print("norm shape:", norm.shape, " per-image-channel mean ~0:",
      bool(np.abs(norm.mean(axis=(1, 2))).max() < 1e-12))

# 2) Sab se roshan image (saare pixels+channels ka mean)
brightness = batch.mean(axis=(1, 2, 3))                 # (8,)
print("\nbrightness:", np.round(brightness, 1))
print("brightest image index:", brightness.argmax())
assert brightness.argmax() == 3

# 3) Har image ka brightest pixel ka (row, col)
gray = batch.mean(axis=3)                               # (8,16,16) channels average
flat = gray.reshape(8, -1).argmax(axis=1)               # per image flat argmax
rows, cols = np.unravel_index(flat, gray.shape[1:])
print("\nbrightest pixel positions (row,col) per image:", list(zip(rows.tolist(), cols.tolist())))
assert gray[0, rows[0], cols[0]] == gray[0].max()

# 4) 2x2 max pooling: (8,16,16,3) -> (8,8,8,3) reshape + max over new axes
pooled = batch.reshape(8, 8, 2, 8, 2, 3).max(axis=(2, 4))
print("\npooled shape:", pooled.shape)
assert pooled.shape == (8, 8, 8, 3)
assert pooled[0, 0, 0, 0] == batch[0, 0:2, 0:2, 0].max()
print("pooling verified: pooled[0,0,0,0] == batch[0,0:2,0:2,0].max() ✔")
""")

M(r"""
### Problem 5 — Website sessionization (diff + where ka combo)
Ek user ke page-view timestamps (minutes) hain. Rule: agar do views me **30 min se ziyada**
gap ho to nayi session shuru. Nikalna hai: session ids, per-session views aur duration.
""")

C(r"""
ts = np.array([0, 5, 12, 13, 60, 65, 70, 200, 205, 260], dtype=float)   # minutes

gaps = np.diff(ts)                                  # size n-1
new_session = gaps > 30                             # kahan naya session shuru hua
session_id = np.concatenate(([0], np.cumsum(new_session)))   # cumsum se id banti hai
print("timestamps :", ts.astype(int))
print("gaps       :", gaps.astype(int))
print("session id :", session_id)
assert session_id.tolist() == [0, 0, 0, 0, 1, 1, 1, 2, 2, 3]

# Per-session stats — group-by pattern
views = np.bincount(session_id)
start = np.full(views.size, np.inf); np.minimum.at(start, session_id, ts)
end   = np.full(views.size, -np.inf); np.maximum.at(end, session_id, ts)
print("\nper-session views   :", views)
print("per-session duration:", (end - start).astype(int), "minutes")
assert views.tolist() == [4, 3, 2, 1]
assert (end - start).tolist() == [13., 10., 5., 0.]

# Sab se lambi session
longest = (end - start).argmax()
print("\nsab se lambi session:", longest, "duration:", int(end[longest] - start[longest]), "min")
""")

# ----------------------------------------------------------------- leetcode
M(r"""
## 22. LeetCode Problems

> **Bohat ahem baat (padh lo):** LeetCode/coding interviews me tumse **pure Python**
> solution expect hota hai — NumPy allowed nahi hota (aur online judge par import ka
> overhead bhi hota hai). Magar **data science / ML interviews** me wohi masla NumPy me
> ek line me hal karna aata hona chahiye.
>
> Is liye har problem ka **do** version diya hai:
> 1. `solve_python(...)` — jo interview me likhna hai (complexity ke sath)
> 2. `solve_numpy(...)` — jo real ML kaam me likhna hai
>
> Dono ka natija barabar hona chahiye — asserts se saabit karte hain.
""")

M(r"""
### LC 215. Kth Largest Element in an Array — Medium
https://leetcode.com/problems/kth-largest-element-in-an-array/

**Bayan:** Ek array `nums` aur number `k` diya hai. **Sorted order me k-th sab se bara**
element wapis karo (distinct nahi — duplicates ginte hain).
Misal: `[3,2,1,5,6,4], k=2` → `5`.

**Approaches:**
1. **Sort karo** → `nums[-k]`. Time `O(n log n)`, Space `O(1)`/`O(n)`.
2. **Min-heap size k** → array par chalo, heap me sirf k sab se bare rakho, `heap[0]` jawab.
   Time `O(n log k)`, Space `O(k)`. Ye interview ka expected jawab hai.
3. **Quickselect (partition)** → average `O(n)`, worst `O(n²)`. "Best" jawab jab interviewer
   `O(n)` maange.
4. **NumPy:** `np.partition(nums, -k)[-k]` — internally quickselect, average `O(n)`.

**Complexity table:** sort `O(n log n)` | heap `O(n log k)` | quickselect `O(n)` avg.
""")

C(r"""
import heapq

def kth_largest_heap(nums, k):
    "Interview solution: min-heap of size k. Time O(n log k), Space O(k)."
    heap = []                                   # min-heap: sab se chhota top par
    for x in nums:
        heapq.heappush(heap, x)                 # daalo
        if len(heap) > k:                       # size k se bara ho gaya?
            heapq.heappop(heap)                 # sab se chhota nikaal do
    return heap[0]                              # ab top = k-th largest

def kth_largest_quickselect(nums, k):
    "Quickselect: average O(n). Target index = n-k (0-based) sorted order me."
    nums = list(nums)
    target = len(nums) - k
    lo, hi = 0, len(nums) - 1
    while True:
        pivot = nums[hi]                        # simple pivot: aakhri element
        store = lo
        for i in range(lo, hi):                 # partition (Lomuto)
            if nums[i] < pivot:
                nums[i], nums[store] = nums[store], nums[i]
                store += 1
        nums[store], nums[hi] = nums[hi], nums[store]
        if store == target:
            return nums[store]                  # bilkul sahi jagah mil gayi
        elif store < target:
            lo = store + 1                      # daaen half me dhoondo
        else:
            hi = store - 1                      # baaen half me

def kth_largest_numpy(nums, k):
    "NumPy: partition average O(n). Sirf position -k ki guarantee chahiye."
    a = np.asarray(nums)
    return int(np.partition(a, -k)[-k])

tests = [([3, 2, 1, 5, 6, 4], 2, 5),
         ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
         ([1], 1, 1),
         ([7, 7, 7, 7], 3, 7),
         ([-1, -5, 0, 2], 1, 2)]
for nums, k, exp in tests:
    assert kth_largest_heap(nums, k) == exp, (nums, k)
    assert kth_largest_quickselect(nums, k) == exp, (nums, k)
    assert kth_largest_numpy(nums, k) == exp, (nums, k)
print("LC 215: saare tests pass ✔ (heap, quickselect, numpy — teenon)")
print("misal: [3,2,1,5,6,4], k=2 ->", kth_largest_numpy([3, 2, 1, 5, 6, 4], 2))
""")

M(r"""
### LC 347. Top K Frequent Elements — Medium
https://leetcode.com/problems/top-k-frequent-elements/

**Bayan:** Array me sab se ziyada aane wale `k` elements wapis karo (kisi bhi tarteeb me).
Misal: `[1,1,1,2,2,3], k=2` → `[1,2]`.

**Approaches:**
1. **Counter + heap**: frequency count `O(n)`, phir `nlargest(k)` → `O(n log k)`. Space `O(n)`.
2. **Bucket sort**: frequency 1..n ho sakti hai, is liye `n+1` buckets banao aur ulta chalo →
   `O(n)` time. Follow-up "better than O(n log n)" ka jawab.
3. **NumPy**: `np.unique(return_counts=True)` + `argpartition(counts, -k)` → `O(n log n)`
   (unique ka sort) magar C speed par. Agar values chhote non-negative ints hain to
   `np.bincount` + `argpartition` → `O(n + m)`, sab se tez.

**Complexity:** heap `O(n log k)` | bucket `O(n)` | numpy bincount `O(n + range)`.
""")

C(r"""
from collections import Counter

def top_k_freq_heap(nums, k):
    "Counter + heap. Time O(n log k), Space O(n)."
    freq = Counter(nums)                                  # value -> count
    return [v for v, _ in heapq.nlargest(k, freq.items(), key=lambda kv: kv[1])]

def top_k_freq_bucket(nums, k):
    "Bucket sort by frequency. Time O(n), Space O(n)."
    freq = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]           # index = frequency
    for v, c in freq.items():
        buckets[c].append(v)
    out = []
    for c in range(len(nums), 0, -1):                      # sab se bari frequency se ulta
        for v in buckets[c]:
            out.append(v)
            if len(out) == k:
                return out
    return out

def top_k_freq_numpy(nums, k):
    "NumPy: unique+counts, phir top-k counts ka argpartition (O(n) selection)."
    vals, counts = np.unique(np.asarray(nums), return_counts=True)
    idx = np.argpartition(counts, -k)[-k:]                  # k sab se bari counts
    idx = idx[np.argsort(-counts[idx])]                     # sirf k ko sort (descending)
    return vals[idx].tolist()

def top_k_freq_bincount(nums, k):
    "Non-negative small ints ke liye sab se tez: bincount + argpartition."
    a = np.asarray(nums)
    offset = a.min()                                        # negative bhi chalane ke liye shift
    counts = np.bincount(a - offset)
    idx = np.argpartition(counts, -k)[-k:]
    idx = idx[np.argsort(-counts[idx])]
    return (idx + offset).tolist()

cases = [([1, 1, 1, 2, 2, 3], 2, {1, 2}),
         ([1], 1, {1}),
         ([4, 4, 4, 5, 5, 6, 6, 6, 6, 7], 2, {6, 4}),
         ([-1, -1, 2, 2, 2, 3], 1, {2})]
for nums, k, exp in cases:
    assert set(top_k_freq_heap(nums, k)) == exp
    assert set(top_k_freq_bucket(nums, k)) == exp
    assert set(top_k_freq_numpy(nums, k)) == exp
    assert set(top_k_freq_bincount(nums, k)) == exp
print("LC 347: saare tests pass ✔ (heap, bucket, numpy unique, numpy bincount)")
print("[4,4,4,5,5,6,6,6,6,7], k=2 ->", top_k_freq_numpy([4, 4, 4, 5, 5, 6, 6, 6, 6, 7], 2))
""")

M(r"""
### LC 349. Intersection of Two Arrays — Easy
https://leetcode.com/problems/intersection-of-two-arrays/

**Bayan:** Do arrays ka intersection — result me har element **sirf ek dafa** (unique).
Misal: `[1,2,2,1]`, `[2,2]` → `[2]`.

**Approaches:**
1. **Set intersection** — `set(a) & set(b)`. Time `O(n+m)`, Space `O(n+m)`.
2. **Sorted + two pointers** — agar arrays pehle se sorted hain: Time `O(n+m)`, Space `O(1)`
   (output ke ilawa). Interviewer ka follow-up yehi hota hai.
3. **NumPy**: `np.intersect1d(a, b)` — sorted + unique khud-ba-khud. `O(n log n)`.
   Agar arrays pehle se sorted aur unique hain to `assume_unique=True` se tez.
""")

C(r"""
def intersect_set(a, b):
    "Set intersection. Time O(n+m)."
    return sorted(set(a) & set(b))

def intersect_two_pointers(a, b):
    "Sort + two pointers. Time O(n log n + m log m), Space O(1) extra."
    a, b = sorted(a), sorted(b)
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1
        elif a[i] > b[j]:
            j += 1
        else:                                  # barabar mila
            if not out or out[-1] != a[i]:     # duplicate avoid
                out.append(a[i])
            i += 1
            j += 1
    return out

def intersect_numpy(a, b):
    "NumPy one-liner — sorted + unique guarantee ke sath."
    return np.intersect1d(np.asarray(a), np.asarray(b)).tolist()

cases = [([1, 2, 2, 1], [2, 2], [2]),
         ([4, 9, 5], [9, 4, 9, 8, 4], [4, 9]),
         ([1, 2, 3], [4, 5], []),
         ([1, 1, 1], [1], [1])]
for a, b, exp in cases:
    assert intersect_set(a, b) == exp
    assert intersect_two_pointers(a, b) == exp
    assert intersect_numpy(a, b) == exp
print("LC 349: pass ✔  [4,9,5] & [9,4,9,8,4] ->", intersect_numpy([4, 9, 5], [9, 4, 9, 8, 4]))
""")

M(r"""
### LC 350. Intersection of Two Arrays II — Easy
https://leetcode.com/problems/intersection-of-two-arrays-ii/

**Bayan:** Ab **multiset** intersection — har element utni dafa aana chahiye jitni dafa
**dono** me common hai (`min(count_a, count_b)`).
Misal: `[1,2,2,1]`, `[2,2]` → `[2,2]`.

**Approaches:**
1. **Counter (hash map)** — chhote array ka counter banao, doosre par chalo aur count ghatao.
   Time `O(n+m)`, Space `O(min(n,m))`.
2. **Sort + two pointers** — Space `O(1)`. Famous follow-ups:
   - *"Agar array sorted hai?"* → two pointers hi behtar.
   - *"Agar nums1 chhota hai?"* → chhote wala hash me rakho.
   - *"Agar nums2 disk par hai aur memory me fit nahi?"* → nums1 ko sort/hash karo aur
     nums2 ko chunks me stream karo (external merge).
3. **NumPy**: `unique(return_counts=True)` dono par, common values par `np.minimum` counts,
   phir `np.repeat`.
""")

C(r"""
def intersect2_counter(a, b):
    "Counter based. Time O(n+m), Space O(min(n,m))."
    if len(a) > len(b):                        # chhote wala counter (space optimize)
        a, b = b, a
    need = Counter(a)
    out = []
    for x in b:
        if need[x] > 0:                        # abhi bhi chahiye?
            out.append(x)
            need[x] -= 1
    return sorted(out)

def intersect2_two_pointers(a, b):
    "Sort + two pointers. Space O(1) extra."
    a, b = sorted(a), sorted(b)
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1
        elif a[i] > b[j]:
            j += 1
        else:
            out.append(a[i])                   # har match count hota hai (duplicates ok)
            i += 1
            j += 1
    return out

def intersect2_numpy(a, b):
    "NumPy: common values + min(counts) + repeat."
    va, ca = np.unique(np.asarray(a), return_counts=True)
    vb, cb = np.unique(np.asarray(b), return_counts=True)
    common, ia, ib = np.intersect1d(va, vb, return_indices=True)
    reps = np.minimum(ca[ia], cb[ib])          # har value kitni dafa
    return np.repeat(common, reps).tolist()

cases = [([1, 2, 2, 1], [2, 2], [2, 2]),
         ([4, 9, 5], [9, 4, 9, 8, 4], [4, 9]),
         ([1, 1, 1], [1, 1], [1, 1]),
         ([1, 2], [3, 4], [])]
for a, b, exp in cases:
    assert intersect2_counter(a, b) == exp, (a, b)
    assert intersect2_two_pointers(a, b) == exp, (a, b)
    assert intersect2_numpy(a, b) == exp, (a, b)
print("LC 350: pass ✔  [1,2,2,1] & [2,2] ->", intersect2_numpy([1, 2, 2, 1], [2, 2]))
""")

M(r"""
### LC 217. Contains Duplicate — Easy
https://leetcode.com/problems/contains-duplicate/

**Bayan:** Batao ke array me koi element **ek se ziyada dafa** aata hai ya nahi.
Misal: `[1,2,3,1]` → `True`, `[1,2,3,4]` → `False`.

**Approaches:**
1. **Set (early exit)** — chalte chalte set me daalo, pehle repeat par `True`.
   Time `O(n)` avg, Space `O(n)`. **Best answer.**
2. **`len(set(nums)) != len(nums)`** — ek line, magar poora set banata hai (early exit nahi).
3. **Sort + neighbour check** — Time `O(n log n)`, Space `O(1)`. Jab memory tight ho.
4. **NumPy**: `np.unique(a).size != a.size`, ya sorted array par `np.any(np.diff(np.sort(a)) == 0)`.

**Interview tip:** trade-off zaroor bolo — "hash set time optimal hai, sorting space optimal".
""")

C(r"""
def has_dup_set(nums):
    "Early-exit set. Time O(n) average, Space O(n)."
    seen = set()
    for x in nums:
        if x in seen:                          # pehla repeat mila -> foran True
            return True
        seen.add(x)
    return False

def has_dup_sort(nums):
    "Sort + padosi compare. Time O(n log n), Space O(1) (in-place sort par)."
    s = sorted(nums)
    return any(s[i] == s[i + 1] for i in range(len(s) - 1))

def has_dup_numpy(nums):
    "NumPy: unique ki size compare karo."
    a = np.asarray(nums)
    return bool(np.unique(a).size != a.size)

def has_dup_numpy_diff(nums):
    "NumPy alternate: sorted array me consecutive farq 0 hua to duplicate hai."
    a = np.sort(np.asarray(nums))
    return bool(np.any(np.diff(a) == 0))

cases = [([1, 2, 3, 1], True), ([1, 2, 3, 4], False),
         ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True), ([], False), ([5], False)]
for nums, exp in cases:
    assert has_dup_set(nums) == exp
    assert has_dup_sort(nums) == exp
    assert has_dup_numpy(nums) == exp
    assert has_dup_numpy_diff(nums) == exp
print("LC 217: pass ✔  [1,2,3,1] ->", has_dup_numpy([1, 2, 3, 1]))

# Bonus — duplicate elements ki list bhi nikaal lo (NumPy)
arr = np.array([1, 2, 3, 2, 5, 1, 1])
v, c = np.unique(arr, return_counts=True)
print("duplicate values:", v[c > 1].tolist(), " unke counts:", c[c > 1].tolist())
assert v[c > 1].tolist() == [1, 2]
""")

# ----------------------------------------------------------------- interview Q&A
M(r"""
## 23. Interview Questions & Answers

**Q1. `axis=0` aur `axis=1` me farq kya hai?**
`axis=k` us axis ko **collapse** karta hai. 2D me `axis=0` rows ko khatam karta hai to
jawab **per-column** aata hai; `axis=1` columns khatam karta hai to jawab **per-row**.
Confirm karne ka tareeqa: `result.shape` dekho — jo dimension bacha wahi jawab ka unit hai.

**Q2. `keepdims=True` kab lazmi hai?**
Jab reduction ke baad original array ke sath broadcast karna ho — normalization, softmax,
layer-norm. Warna `(3,4) / (3,)` fail hoti hai ya galat axis par broadcast hoti hai.

**Q3. `np.sort` aur `arr.sort()` me farq?**
`np.sort` **copy** deta hai (original safe), `arr.sort()` **in-place** hai aur `None` return
karta hai. `x = arr.sort()` likhna aam bug hai (`x` None ban jata hai).

**Q4. Top-k nikalne ka sab se acha tareeqa?**
`np.argpartition(a, -k)[-k:]` — average `O(n)` (quickselect), poora sort `O(n log n)`.
Sirf un k values ko baad me sort karo agar tarteeb chahiye.

**Q5. `argsort` ka kya faida `sort` par?**
`argsort` **indices** deta hai jinse doosre parallel arrays ko bhi usi tarteeb me rearrange
kar sakte ho (jaise names ko marks ke hisaab se) — yehi pandas `sort_values` ka core hai.

**Q6. `lexsort` me keys ulti tarteeb me kyun deni parti hain?**
Ye stable sorts ka chain hai: pehli key pehle apply hoti hai aur baad wali keys usay
override karti hain, is liye **aakhri key primary** ban jati hai.

**Q7. Stable sort ka matlab aur zaroorat?**
Barabar elements apni original tarteeb me rehte hain. Multi-key sorting (pehle salary,
phir department) ke liye lazmi. `kind='stable'` do.

**Q8. `np.where(cond)` aur `np.where(cond, x, y)` me farq?**
Ek argument → matching **indices ka tuple** (== `np.nonzero`). Teen arguments →
element-wise ternary (`cond ? x : y`) jo shape barqarar rakhta hai.

**Q9. `nonzero`, `argwhere`, `flatnonzero` me farq?**
`nonzero` → per-axis index arrays ka tuple (indexing me direct use ho jata hai).
`argwhere` → `(n, ndim)` array (coordinates par loop karne ke liye).
`flatnonzero` → flattened 1D indices (1D data par sab se saaf).

**Q10. `a[idx] += 1` duplicate indices par kyun ghalat hota hai?**
Ye buffered operation hai: fetch → add → store. Duplicate index ki aakhri store baqi
increments ko overwrite kar deti hai. Hal: `np.add.at` (unbuffered) ya
`np.bincount(idx, weights=...)` (tez).

**Q11. `np.unique(return_inverse=True)` ka ML me use?**
Label encoding! `inverse` hi codes hain aur `unique[inverse] == original` guarantee hai.
`bincount` ke sath mila kar poora group-by ban jata hai.

**Q12. `bincount` vs `histogram` — kab kaun?**
`bincount`: non-negative **integers**, exact counting, sab se tez, `weights` se grouped sum.
`histogram`: **continuous** data, bins/edges define karne parte hain.

**Q13. NaN ko `==` se check kyun nahi kar sakte?**
IEEE-754 ke mutabiq NaN kisi ke barabar nahi, khud ke bhi nahi. `np.isnan()` use karo.
(Isi wajah se `np.nan in [np.nan]` `True` deta hai — wo `is` check pehle karta hai — ek famous trap.)

**Q14. `mean` vs `nanmean` — production me kaun?**
`nanmean` (ya mask) — magar pehle ye faisla karo ke missing data **kyun** missing hai.
Chupke se ignore karna data leakage/bias paida kar sakta hai.

**Q15. `np.ma` masked arrays kab use karein?**
Jab missing values integer data me hain (NaN reh nahi sakta) ya legacy code me pehle se
`np.ma` hai. Naye projects me pandas / explicit masks preferred hain (ma slow hai).

**Q16. Fancy indexing view deti hai ya copy?**
**Copy** (advanced indexing). Basic slicing **view** deti hai. Is liye `a[a>5] += 1` chalta
hai (ye special-cased assignment hai) magar `b = a[a>5]; b += 1` original ko nahi badalta.

**Q17. `a[[0,2],[1,3]]` aur `a[np.ix_([0,2],[1,3])]` me farq?**
Pehla indices **zip** karta hai → 2 elements (`a[0,1]`, `a[2,3]`).
Doosra open mesh banata hai → 2×2 **submatrix**.

**Q18. `take_along_axis` ki zaroorat kya hai?**
`argsort`/`argmax`/`argpartition` per-axis indices dete hain; unse values nikalne ke liye
manual `np.arange` broadcasting likhni parti hai. `take_along_axis` wohi kaam saaf aur
bug-free karta hai.

**Q19. `apply_along_axis` vectorized hai?**
**Nahi.** Ye Python-level loop hai, sirf syntax sugar. Hamesha pehle built-in `axis=`,
broadcasting ya `einsum` try karo.

**Q20. `std()` ka natija pandas se kyun mukhtalif hai?**
NumPy ka default `ddof=0` (population), pandas ka `ddof=1` (sample).
`np.std(x, ddof=1)` do to match ho jayega.

**Q21. `argmax` ties me kya karta hai?**
Sab se **pehla** (lowest) index deta hai. Saare max positions chahiye to
`np.flatnonzero(a == a.max())`.

**Q22. NumPy 2.0 me kya kya hata diya gaya jo intermediate code me milta hai?**
`np.in1d` (→ `isin`), `np.trapz` (→ `trapezoid`), `np.float_`/`np.unicode_`
(→ `np.float64`/`np.str_`), `np.NaN` (→ `np.nan`), `np.row_stack` (→ `vstack`).
""")

# ----------------------------------------------------------------- exercises
M(r"""
## 24. Practice Exercises (khud karo)

1. **Axis drill:** `a = np.arange(60).reshape(3,4,5)` — bina chalaye batao
   `a.sum(axis=1).shape`, `a.mean(axis=(0,2)).shape`, `a.max(axis=-1, keepdims=True).shape`.
   Phir code se check karo.
   *Hint:* jo axis diya wo gayab; `keepdims` se wo 1 ban jata hai.

2. **Column-wise min-max scaling** likho (formula `(x - min) / (max - min)`) taake har column
   0..1 me aa jaye. Constant column (max == min) par divide-by-zero se bacho.
   *Hint:* `keepdims=True` + `np.where(rng_ == 0, 1, rng_)`.

3. **Top-3 per row** nikalo ek `(5, 8)` random matrix se — values aur indices dono,
   descending order me. `argpartition` use karo, poora sort nahi.
   *Hint:* `argpartition` → `take_along_axis` → chhota `argsort`.

4. **Run-length encoding** likho: `[1,1,2,2,2,3]` → values `[1,2,3]`, counts `[2,3,1]`.
   *Hint:* `np.diff` se boundaries dhoondo, `np.flatnonzero`, phir `np.diff` of positions.

5. **Second largest unique value** nikalo ek array se (duplicates ignore).
   *Hint:* `np.unique` sorted deta hai → `u[-2]`, magar pehle `u.size >= 2` check karo.

6. **Group-by two keys:** `city` aur `month` arrays se `(city × month)` revenue pivot banao
   `np.add.at` se, aur uska row/column total bhi nikalo.
   *Hint:* dono par `unique(return_inverse=True)`, phir tuple index.

7. **Moving average (window 3)** `cumsum` se nikalo (sliding_window_view nahi).
   *Hint:* `c = np.cumsum(np.r_[0, x]); (c[3:] - c[:-3]) / 3`.

8. **Outlier report:** ek `(6, 30)` matrix me per-row IQR method se outliers dhoondho
   (`q1 - 1.5*iqr`, `q3 + 1.5*iqr`) aur `argwhere` se unki positions print karo.
   *Hint:* `np.percentile(a, [25,75], axis=1)` + `keepdims` broadcasting.

9. **`np.add.at` vs `bincount` benchmark:** 1e6 random indices par dono se grouped sum
   karo aur `timeit` se farq dekho. Kaun tez aur kyun?

10. **Mini k-NN:** 20 train points `(20,2)` aur 5 test points `(5,2)` par distance matrix
    banao (broadcasting se), phir `argpartition` se har test point ke 3 nearest neighbours
    aur unka majority label nikalo.
""")

# ----------------------------------------------------------------- summary
M(r"""
## 25. Summary / Cheat-sheet

### Axis ka qanoon
```
a.shape = (d0, d1, d2)
a.op(axis=k)                -> axis k GAYAB
a.op(axis=k, keepdims=True) -> axis k ki jagah 1
a.op(axis=(i,j))            -> dono gayab
a.op()                      -> scalar (sab collapse)
axis=-1 == aakhri axis      -> generic code ke liye best
```
2D me: `axis=0` → per-**column** | `axis=1` → per-**row**

### Reductions
| Kaam | Function |
|---|---|
| jama / zarb | `sum`, `prod`, `cumsum`, `cumprod` |
| center | `mean`, `median`, `average(weights=)` |
| spread | `std`, `var` (**`ddof=1`** sample ke liye), `ptp`, `percentile` |
| extremes | `min`, `max`, `argmin`, `argmax` + `unravel_index` |
| logic | `any`, `all`, `count_nonzero` |
| nan-safe | har ek ka `nan*` version |

### Order statistics
| Chahiye | Use |
|---|---|
| poora sorted | `np.sort(a, axis, kind='stable')` |
| sorted indices | `np.argsort` |
| multi-key sort | `np.lexsort((secondary, primary))` |
| top-k (tez) | `np.argpartition(a, -k)[-k:]` |
| per-axis values from indices | `np.take_along_axis(a, idx, axis)` |

### Searching / counting
| Chahiye | Use |
|---|---|
| insertion position / binning | `np.searchsorted(sorted_a, v, side)` |
| bins | `np.digitize`, `np.histogram`, `np.histogram2d` |
| if-else | `np.where(cond, x, y)`; multi-branch → `np.select` |
| positions | `np.nonzero`, `np.flatnonzero`, `np.argwhere` |
| ginti | `np.count_nonzero`, `np.bincount(x, weights, minlength)` |

### Sets & group-by
```python
u, code = np.unique(keys, return_inverse=True)     # label encode
sums  = np.bincount(code, weights=vals)            # grouped sum   (tez)
np.add.at(out2d, (rows, cols), vals)               # scatter-add   (general)
np.intersect1d / union1d / setdiff1d / isin        # set algebra
```

### NaN / inf
```python
np.isnan / np.isinf / np.isfinite
np.nanmean / nanstd / nanmax / nanargmax ...
np.nan_to_num(a, nan=0, posinf=..., neginf=...)
np.divide(a, b, out=np.zeros_like(a), where=b!=0)  # safe divide
with np.errstate(divide='ignore'): ...             # warnings control
```

### Indexing
| Form | Result | Copy/View |
|---|---|---|
| `a[1:3, ::2]` | slice | **view** |
| `a[[0,2],[1,3]]` | zipped elements | copy |
| `a[np.ix_(r, c)]` | submatrix | copy |
| `a[mask]` | filtered 1D | copy |
| `a[idx] += 1` | **buffered (duplicates ghalat)** | — |
| `np.add.at(a, idx, v)` | unbuffered scatter | in-place |

### Aakhri naseehat
> Jab bhi shape ka shak ho — `print(a.shape)`. Jab bhi axis ka shak ho — chhota
> `np.arange(6).reshape(2,3)` bana kar test karo. 30 second ka experiment 3 ghante ki
> debugging bachata hai.

**Aage:** `02_LinearAlgebra_Random_aur_Statistics.ipynb` — matmul, SVD, eigenvalues,
`default_rng`, Monte Carlo aur statistics.
""")

save(r"Numpy/Intermediate/01_Axis_Mastery_Aggregations_aur_Advanced_Indexing.ipynb", CELLS)
