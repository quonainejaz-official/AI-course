"""Generator: Numpy/Basics/04_Numpy_Practice_Problems_aur_Interview.ipynb

Chalao (ROOT se):  python _tools/gen/np_basics_04_practice.py
"""

import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

CELLS: list = []
A = CELLS.append

A(md("""
# NumPy 04 — Practice Problems aur Interview Preparation

**Level:** Basics ka capstone | **Library:** NumPy 2.x | **Python:** 3.14

Ye notebook **practice** ka notebook hai. NB 01-03 me jo concepts seekhe (creation,
indexing, views, broadcasting, aggregations) — unko **35 problems**, **5 LeetCode
problems**, **26 interview Q&A** aur ek **"output kya hoga" quiz** se pakka karenge.

## Is notebook me kya hai

1. **35 Practice Problems** — har ek ka format: statement → **Hint** → commented
   solution → `assert` tests. Difficulty aage barhti jayegi.
2. **list vs numpy performance experiment** — different sizes par timing + speedup table
3. **LeetCode Problems** — LC 73, 240, 289, 304, 118 (pure Python **aur** NumPy version)
4. **Interview Questions & Answers** — 26 sawal, crisp jawab
5. **"Output kya hoga?" Quiz** — 10 classic trap snippets + answers + verification cell
6. **Common Mistakes / Gotchas**, **Real-World mini-projects**, **Practice Exercises**, **Cheat-sheet**

## Prerequisites

- **NB 01** — arrays, dtype, creation
- **NB 02** — indexing, slicing, views vs copies, reshape, joining
- **NB 03** — operations, broadcasting, aggregations, axis

## Kaam karne ka tareeqa (bohat zaroori)

Har problem ka **statement pehle padho, solution ko chhupa kar khud koshish karo**,
phir solution dekho. Sirf padhne se NumPy nahi aati — likhne se aati hai.
"""))

A(code("""
# Setup -- poore notebook me yehi imports aur seed use honge
import numpy as np
import timeit
import sys

# Reproducibility: har jagah fixed seed -> tumhare paas bhi wahi numbers aayenge
rng = np.random.default_rng(42)

print("NumPy:", np.__version__)
print("Python:", sys.version.split()[0])

# Saaf output ke liye printing options
np.set_printoptions(precision=4, suppress=True, linewidth=100)
print("\\nSetup ho gaya. Chalo shuru karein!")
"""))

# ================================================================= PART 1
A(md("""
---

# Hissa 1 — 35 Practice Problems

**Format:** `### P<n>. <problem>` → **Hint** → solution (comments ke sath) → `assert` tests.

Shuruaat aasan hai, aakhir tak ML-level problems aa jayengi.
"""))

# ---- P1
A(md("""
### P1. Basic creation & reshape

(a) 0 se 9 tak ka 1D array banao.
(b) 0 se 8 tak ke numbers ka `3x3` array banao.
(c) `3x3` array ko `float32` dtype me banao.

**Hint:** `np.arange`, `.reshape`, `dtype=`.
"""))

A(code("""
# (a) 0..9 ka vector
a = np.arange(10)
print("(a)", a)

# (b) 0..8 ko 3x3 me -- 9 elements, 3*3 = 9, to reshape chal jayega
b = np.arange(9).reshape(3, 3)
print("\\n(b)\\n", b)

# (c) dtype dena -- reshape ke baad astype, ya arange me hi dtype
c = np.arange(9, dtype=np.float32).reshape(3, 3)
print("\\n(c) dtype:", c.dtype)
print(c)

# -1 ka magic: NumPy khud dimension nikal leta hai
print("\\nreshape(-1, 3) se shape:", np.arange(12).reshape(-1, 3).shape, "<- rows khud 4 nikal aaye")

assert a.tolist() == list(range(10))
assert b.shape == (3, 3) and b[2, 2] == 8
assert c.dtype == np.float32
"""))

# ---- P2
A(md("""
### P2. Checkerboard pattern (8x8) — do tareeqe

`8x8` array banao jisme 0 aur 1 shatranj ki bisaat (chessboard) ki tarah alternate hon.

**Hint:** Tareeqa 1 — `np.zeros` phir slicing `[::2, ::2]`.
Tareeqa 2 — `(i + j) % 2` formula (`np.indices` ya `np.fromfunction`).
"""))

A(code("""
# --- Tareeqa 1: slicing (sab se aam interview answer) ---
board = np.zeros((8, 8), dtype=int)
board[::2, 1::2] = 1        # even rows (0,2,4,6) ke odd columns
board[1::2, ::2] = 1        # odd rows (1,3,5,7) ke even columns
print("Slicing se:\\n", board)

# --- Tareeqa 2: formula (i + j) % 2 -- ye zyada 'mathematical' hai ---
i, j = np.indices((8, 8))   # do arrays: row-index aur col-index har khaane ka
board2 = (i + j) % 2
print("\\nFormula se same? ", np.array_equal(board, board2))

# --- Tareeqa 3: np.tile se chhote 2x2 block ko repeat karo ---
board3 = np.tile(np.array([[0, 1], [1, 0]]), (4, 4))
print("Tile se same?    ", np.array_equal(board, board3))

assert board.shape == (8, 8)
assert board[0, 0] == 0 and board[0, 1] == 1
assert board.sum() == 32              # aadhe khaane 1 hain
assert np.array_equal(board, board2) and np.array_equal(board, board3)
"""))

# ---- P3
A(md("""
### P3. Border 1s, inside 0s

`5x5` array banao jiska bahar ka border poora 1 ho aur andar sab 0.

**Hint:** `np.ones` se shuru karo aur andar ka hissa `[1:-1, 1:-1]` = 0 kar do
(ye `np.zeros` se shuru karne se aasan hai). `np.pad` bhi ek tareeqa hai.
"""))

A(code("""
# --- Tareeqa 1: ones se shuru, andar ka block 0 ---
g = np.ones((5, 5), dtype=int)
g[1:-1, 1:-1] = 0            # 1 se le kar aakhri se pehle tak -> andar ka 3x3
print("ones + andar 0:\\n", g)

# --- Tareeqa 2: np.pad -- andar ka 3x3 zeros lo aur 1 ka border chipka do ---
g2 = np.pad(np.zeros((3, 3), dtype=int), pad_width=1, constant_values=1)
print("\\nnp.pad se same? ", np.array_equal(g, g2))

# Border ke elements ki ginti = 5*5 - 3*3 = 16
print("border cells:", g.sum())

assert g.sum() == 16
assert g[0, :].sum() == 5 and g[:, 0].sum() == 5     # poori pehli row/col 1
assert g[1:-1, 1:-1].sum() == 0                      # andar sab 0
assert np.array_equal(g, g2)
"""))

# ---- P4
A(md("""
### P4. Normalize array to 0-1 range (min-max scaling)

Kisi bhi array ko aise scale karo ke sab se chhoti value 0 ban jaye aur sab se bari 1.

**Formula:** `(x - min) / (max - min)`

**Hint:** Constant array (jahan max == min) par divide-by-zero ka khayal rakho.
"""))

A(code("""
def minmax_normalize(x):
    \"\"\"Array ko 0..1 range me le aata hai. Constant array ko safely handle karta hai.\"\"\"
    x = np.asarray(x, dtype=np.float64)      # asarray: pehle se array ho to copy nahi
    lo, hi = x.min(), x.max()
    rng_ = hi - lo
    if rng_ == 0:                            # sab values same -> range 0 -> divide by zero
        return np.zeros_like(x)              # convention: sab 0 kar do
    return (x - lo) / rng_


data = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
norm = minmax_normalize(data)
print("original  :", data)
print("normalized:", norm)
print("min:", norm.min(), "max:", norm.max())

# Negative values ke sath bhi chalta hai
print("\\nnegatives :", minmax_normalize([-5, 0, 5]))

# Edge case: constant array
print("constant   :", minmax_normalize([7, 7, 7]), "<- crash nahi hua")

assert np.allclose(norm, [0, 0.25, 0.5, 0.75, 1.0])
assert norm.min() == 0.0 and norm.max() == 1.0
assert np.allclose(minmax_normalize([7, 7, 7]), [0, 0, 0])
"""))

# ---- P5
A(md("""
### P5. Standardize (z-score)

Array ko aise transform karo ke mean 0 ho aur standard deviation 1.

**Formula:** `z = (x - mean) / std`

**Hint:** 2D array me **per-column** standardize karna ho to `axis=0` aur
`keepdims=True` use karo — yehi ML ka asli use-case hai (`StandardScaler`).
"""))

A(code("""
def zscore(x, axis=None):
    \"\"\"z-score standardization. axis=0 -> per column, axis=1 -> per row.\"\"\"
    x = np.asarray(x, dtype=np.float64)
    mu = x.mean(axis=axis, keepdims=True)    # keepdims -> shape barqarar, broadcast ho sake
    sd = x.std(axis=axis, keepdims=True)
    sd = np.where(sd == 0, 1.0, sd)          # constant column ko 0 se divide hone se bachao
    return (x - mu) / sd


v = np.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
z = zscore(v)
print("original:", v)
print("z-score :", z)
print("mean:", round(float(z.mean()), 10), "| std:", round(float(z.std()), 10))

# 2D: per-COLUMN standardize (har feature ka apna mean/std) -- ML ka standard
X = np.array([[1.0, 100.0],
              [2.0, 200.0],
              [3.0, 300.0],
              [4.0, 400.0]])
Xz = zscore(X, axis=0)
print("\\nX (do features, bilkul different scale):\\n", X)
print("\\nper-column z-score:\\n", Xz)
print("\\ncolumn means:", Xz.mean(axis=0).round(10), "| column stds:", Xz.std(axis=0).round(10))
print("Dono features ab ek hi scale par -> distance-based models (KNN) theek kaam karenge.")

assert np.isclose(z.mean(), 0) and np.isclose(z.std(), 1)
assert np.allclose(Xz.mean(axis=0), 0)
assert np.allclose(Xz.std(axis=0), 1)
"""))

# ---- P6
A(md("""
### P6. Sab odd values ko -1 se replace karo

0..9 ke array me tamam odd numbers ki jagah -1 kar do — (a) naya array bana kar
(original safe rahe), (b) in-place.

**Hint:** `np.where(cond, a, b)` copy deta hai; boolean-mask assignment in-place hai.
"""))

A(code("""
orig = np.arange(10)

# (a) COPY -- np.where(condition, agar_true, agar_false)
replaced = np.where(orig % 2 == 1, -1, orig)
print("original         :", orig, "<- bilkul waisa hi hai")
print("np.where se naya :", replaced)

# (b) IN-PLACE -- boolean mask se assignment
arr = np.arange(10)                # kaam karne ke liye alag array
mask = arr % 2 == 1                # kaunse odd hain
arr[mask] = -1                     # sirf un khaanon par likho
print("\\nin-place ke baad :", arr)
print("mask tha         :", mask)

# One-liner in-place form
arr2 = np.arange(10)
arr2[arr2 % 2 == 1] = -1
print("one-liner        :", arr2)

expected = [0, -1, 2, -1, 4, -1, 6, -1, 8, -1]
assert np.array_equal(replaced, expected)
assert np.array_equal(arr, expected)
assert np.array_equal(arr2, expected)
assert np.array_equal(orig, np.arange(10))      # original chhua nahi gaya
"""))

# ---- P7
A(md("""
### P7. Do rows / do columns swap karo

`3x4` matrix me row 0 aur row 2 swap karo; phir column 1 aur column 3 swap karo.

**Hint:** Fancy indexing se ek hi line me: `M[[0, 2]] = M[[2, 0]]`.
Ye kaam karta hai kyunki right side pehle **copy** ban jata hai.
"""))

A(code("""
M = np.arange(12).reshape(3, 4)
print("original:\\n", M)

# Rows swap -- fancy indexing (RHS pehle copy banta hai, isliye safe hai)
R = M.copy()
R[[0, 2]] = R[[2, 0]]
print("\\nrow 0 <-> row 2:\\n", R)

# Columns swap
C = M.copy()
C[:, [1, 3]] = C[:, [3, 1]]
print("\\ncol 1 <-> col 3:\\n", C)

# GOTCHA: Python ka tuple-swap ndarray par kaam NAHI karta jaise expect karte ho
# kyunki M[0] ek VIEW hai -- dono taraf same memory par point karte hain
G = M.copy()
G[0], G[2] = G[2], G[0]
print("\\nview-swap ka natija (GALAT):\\n", G)
print("Dekho row 0 aur row 2 dono same ho gaye -> view ki wajah se data kho gaya.")
print("Sahi tareeqa: G[[0,2]] = G[[2,0]]  ya  G[0].copy() use karo.")

assert np.array_equal(R[0], M[2]) and np.array_equal(R[2], M[0])
assert np.array_equal(C[:, 1], M[:, 3]) and np.array_equal(C[:, 3], M[:, 1])
assert np.array_equal(G[0], G[2])          # bug ka proof
"""))

# ---- P8
A(md("""
### P8. 2D array ki rows reverse karo (aur columns bhi)

**Hint:** `M[::-1]` rows ulat deta hai, `M[:, ::-1]` columns. Dono **views** hain —
copy nahi.
"""))

A(code("""
M = np.arange(1, 13).reshape(3, 4)
print("original:\\n", M)

print("\\nrows reversed M[::-1]:\\n", M[::-1])
print("\\ncols reversed M[:, ::-1]:\\n", M[:, ::-1])
print("\\ndono M[::-1, ::-1] (180 degree):\\n", M[::-1, ::-1])

# np.flip bhi wahi kaam karta hai, zyada padhne me saaf
print("\\nnp.flip(M, axis=0) same? ", np.array_equal(np.flip(M, axis=0), M[::-1]))
print("np.flipud == M[::-1]?    ", np.array_equal(np.flipud(M), M[::-1]))
print("np.fliplr == M[:, ::-1]? ", np.array_equal(np.fliplr(M), M[:, ::-1]))

# AHEM: ye sab VIEWS hain -> modify karoge to original badlega
v = M[::-1]
print("\\nview hai? base is M:", v.base is M)

assert np.array_equal(M[::-1][0], M[2])
assert np.array_equal(M[:, ::-1][:, 0], M[:, 3])
"""))

# ---- P9
A(md("""
### P9. Do arrays ke common elements dhoondo

**Hint:** `np.intersect1d(a, b)` sorted unique common values deta hai.
`np.isin(a, b)` element-wise boolean mask deta hai (jo positions batane ke liye behtar hai).
"""))

A(code("""
a = np.array([1, 2, 3, 4, 5, 6, 5])
b = np.array([4, 5, 6, 7, 8])

print("a:", a)
print("b:", b)

# intersect1d -> sorted + UNIQUE common values
common = np.intersect1d(a, b)
print("\\nintersect1d      :", common, "<- unique aur sorted (5 sirf ek baar)")

# isin -> mask: 'a' ka har element b me hai ya nahi
mask = np.isin(a, b)
print("isin mask        :", mask)
print("a ke matching vals:", a[mask], "<- duplicates bhi shamil, original order me")
print("indices          :", np.flatnonzero(mask))

# Baqi useful set operations
print("\\nsetdiff1d (a - b):", np.setdiff1d(a, b))
print("union1d          :", np.union1d(a, b))
print("setxor1d         :", np.setxor1d(a, b), "<- sirf ek me maujood")

# NOTE: np.in1d NumPy 2.0 me HATA diya gaya -- np.isin use karo
try:
    np.in1d(a, b)
except AttributeError:
    print("\\nnp.in1d ab maujood nahi hai (NumPy 2.0 me removed) -> np.isin use karo")

assert np.array_equal(common, [4, 5, 6])
assert np.array_equal(a[mask], [4, 5, 6, 5])
"""))

# ---- P10
A(md("""
### P10. NaN wali rows remove karo

Ek `(5, 3)` matrix me se wo tamam rows nikaal do jinme koi bhi `nan` ho.

**Hint:** `np.isnan(X)` element-wise mask deta hai; `.any(axis=1)` per-row batata hai
ke us row me koi nan hai ya nahi; phir `~` se ulta karke filter karo.
"""))

A(code("""
X = np.array([[1.0, 2.0, 3.0],
              [4.0, np.nan, 6.0],
              [7.0, 8.0, 9.0],
              [np.nan, np.nan, 1.0],
              [2.0, 3.0, 4.0]])
print("X:\\n", X)

nan_mask = np.isnan(X)                  # (5,3) boolean
bad_rows = nan_mask.any(axis=1)         # per-row: koi nan hai?
clean = X[~bad_rows]                    # ~ = NOT -> sirf saaf rows

print("\\nper-element nan mask:\\n", nan_mask.astype(int))
print("\\nkaunsi rows kharab :", bad_rows, "-> indices", np.flatnonzero(bad_rows))
print("\\nsaaf data:\\n", clean)
print("\\n", X.shape[0], "rows me se", clean.shape[0], "bachi,", bad_rows.sum(), "hataayi.")

# Variation: sirf wo rows hatao jo POORI nan hon -> .all(axis=1)
print("\\npoori-nan rows:", np.isnan(X).all(axis=1))

assert clean.shape == (3, 3)
assert not np.isnan(clean).any()
assert np.array_equal(clean[0], [1.0, 2.0, 3.0])
"""))

# ---- P11
A(md("""
### P11. Per-row non-zero elements ginno

**Hint:** `np.count_nonzero(X, axis=1)` — ya `(X != 0).sum(axis=1)`.
"""))

A(code("""
X = np.array([[0, 1, 0, 2],
              [0, 0, 0, 0],
              [3, 4, 5, 6],
              [1, 0, 0, 1]])
print("X:\\n", X)

per_row = np.count_nonzero(X, axis=1)       # axis=1 -> columns collapse -> per-row jawab
per_col = np.count_nonzero(X, axis=0)

print("\\nper-row non-zero:", per_row)
print("per-col non-zero:", per_col)
print("total non-zero  :", np.count_nonzero(X))

# Doosra tareeqa: boolean array ka sum (True = 1)
print("\\n(X != 0).sum(axis=1):", (X != 0).sum(axis=1), "<- bilkul wahi")

# Practical: kaunsi rows poori khali (sab zero) hain?
empty_rows = per_row == 0
print("\\nkhali rows ke indices:", np.flatnonzero(empty_rows))

assert np.array_equal(per_row, [2, 0, 4, 2])
assert np.array_equal(per_col, [2, 2, 1, 3])
assert np.count_nonzero(X) == 8
"""))

# ---- P12
A(md("""
### P12. Sab se zyada aane wali value (mode) nikalo

**Hint:** Non-negative integers ke liye `np.bincount(a).argmax()` sab se tez hai.
General data (negative / float / string) ke liye `np.unique(a, return_counts=True)`.
"""))

A(code("""
a = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 5])

# Tareeqa 1: bincount (sirf non-negative INTEGERS ke liye)
counts = np.bincount(a)                  # index = value, value = frequency
mode_bincount = counts.argmax()           # sab se bari frequency ka index
print("a          :", a)
print("bincount   :", counts)
print("mode       :", mode_bincount, "| kitni baar:", counts.max())

# Tareeqa 2: unique + return_counts (HAR tarah ke data par chalta hai)
vals, cnts = np.unique(a, return_counts=True)
mode_unique = vals[cnts.argmax()]
print("\\nunique vals:", vals)
print("counts     :", cnts)
print("mode       :", mode_unique)

# Negative / float data par bincount fail hota hai, unique chalta hai
neg = np.array([-2.5, -2.5, 1.0, 3.0])
v2, c2 = np.unique(neg, return_counts=True)
print("\\nfloat/negative data ka mode:", v2[c2.argmax()])

# GOTCHA: tie (barabar frequency) ho to argmax PEHLA wala deta hai
tie = np.array([1, 1, 2, 2])
print("\\ntie [1,1,2,2] ka mode:", np.bincount(tie).argmax(), "<- pehla (1), koi 'error' nahi")

assert mode_bincount == 5 and mode_unique == 5
assert counts.max() == 4
assert v2[c2.argmax()] == -2.5
"""))

# ---- P13
A(md("""
### P13. Moving average (window = 3)

`[1..10]` ka 3-element moving average nikalo — **loop ke baghair**.

**Hint:** Do tareeqe: (a) `np.cumsum` ka trick — `(cs[k:] - cs[:-k]) / k`,
(b) `np.convolve(a, np.ones(k)/k, mode='valid')`.
"""))

A(code("""
a = np.arange(1, 11, dtype=float)
k = 3

# --- Tareeqa 1: cumsum trick (O(n), sab se tez) ---
# 0 ko aage lagao taake pehla window bhi ek subtraction se nikal aaye
cs = np.cumsum(np.insert(a, 0, 0))
ma_cumsum = (cs[k:] - cs[:-k]) / k

# --- Tareeqa 2: convolve (padhne me saaf, 'valid' = sirf poore windows) ---
ma_conv = np.convolve(a, np.ones(k) / k, mode='valid')

# --- Tareeqa 3: sliding_window_view (NumPy >= 1.20, sab se saaf) ---
windows = np.lib.stride_tricks.sliding_window_view(a, k)
ma_swv = windows.mean(axis=1)

print("a           :", a)
print("cumsum se   :", ma_cumsum)
print("convolve se :", ma_conv)
print("swv se      :", ma_swv)
print("\\nwindows (view, koi extra memory nahi):\\n", windows)
print("\\nlambai:", len(ma_cumsum), "= n - k + 1 =", len(a) - k + 1)

assert np.allclose(ma_cumsum, [2, 3, 4, 5, 6, 7, 8, 9])
assert np.allclose(ma_cumsum, ma_conv) and np.allclose(ma_cumsum, ma_swv)
assert len(ma_cumsum) == len(a) - k + 1
"""))

# ---- P14
A(md("""
### P14. Running sum, running max aur running min

**Hint:** `np.cumsum`, `np.maximum.accumulate`, `np.minimum.accumulate`.
Ye "accumulate" wala pattern kisi bhi ufunc par chalta hai.
"""))

A(code("""
a = np.array([3, 1, 4, 1, 5, 9, 2, 6])
print("a           :", a)

print("\\ncumsum      :", np.cumsum(a))
print("cumprod     :", np.cumprod(a))
print("running max :", np.maximum.accumulate(a), "<- ab tak ka sab se bara")
print("running min :", np.minimum.accumulate(a), "<- ab tak ka sab se chhota")

# Practical: stock price ka 'drawdown' (peak se kitna neeche)
prices = np.array([100., 120., 90., 130., 110.])
peak = np.maximum.accumulate(prices)
drawdown = (prices - peak) / peak * 100
print("\\nprices   :", prices)
print("peak     :", peak)
print("drawdown%:", drawdown.round(2), "<- max loss:", round(drawdown.min(), 2), "%")

assert np.array_equal(np.cumsum(a), [3, 4, 8, 9, 14, 23, 25, 31])
assert np.array_equal(np.maximum.accumulate(a), [3, 3, 4, 4, 5, 9, 9, 9])
assert np.array_equal(np.minimum.accumulate(a), [3, 1, 1, 1, 1, 1, 1, 1])
assert np.isclose(drawdown.min(), -30.769230769230766)
"""))

# ---- P15
A(md("""
### P15. Diye gaye number ke sab se qareeb value dhoondo

`a` me se wo element dhoondo jo `target` ke sab se qareeb hai (uska index bhi).

**Hint:** `np.abs(a - target).argmin()`.
"""))

A(code("""
a = np.array([1.5, 3.7, 8.2, 4.4, 6.9, 2.1])
target = 5.0

diffs = np.abs(a - target)          # broadcasting: scalar poore array se minus
idx = diffs.argmin()               # sab se chhote fark ka index

print("a       :", a)
print("target  :", target)
print("|a-t|   :", diffs)
print("\\nqareeb tareen value:", a[idx], "index par", idx)

# Sab se qareeb K values (K = 3) -- argsort se
k = 3
near_k = a[np.argsort(diffs)[:k]]
print("sab se qareeb", k, "values:", near_k)

# Sorted array ho to np.searchsorted O(log n) me kaam kar deta hai
s = np.sort(a)
pos = np.searchsorted(s, target)
print("\\nsorted:", s, "| target", target, "ki insert position:", pos)
print("padosi candidates:", s[pos - 1], "aur", s[pos])

assert idx == 4 and a[idx] == 6.9
assert np.allclose(np.sort(near_k), [3.7, 4.4, 6.9])
"""))

# ---- P16
A(md("""
### P16. Har element ka rank nikalo (0-based)

`[10, 50, 20, 40, 30]` ke liye ranks `[0, 4, 1, 3, 2]` hone chahiye.

**Hint:** `argsort` ka **argsort** — ye classic trick hai. Pehla argsort batata hai
"kaunsa index kis position par jaye", doosra usay ulat kar rank bana deta hai.
"""))

A(code("""
a = np.array([10, 50, 20, 40, 30])

order = np.argsort(a)          # sorted order me original indices
ranks = np.argsort(order)      # argsort ka argsort = rank

print("a     :", a)
print("order :", order, "<- a[order] sorted hoga:", a[order])
print("ranks :", ranks, "<- har element ka apna rank")

# Kaise? rank[i] = 'a[i] sorted array me kis position par hai'
for val, r in zip(a, ranks):
    print(f"  {val} ka rank {r}")

# Descending rank (sab se bara = rank 0)
desc = np.argsort(np.argsort(-a))
print("\\ndescending ranks:", desc)

# GOTCHA: ties ke sath ye 'first-come' rank deta hai, average rank nahi
tied = np.array([10, 20, 20, 30])
print("ties [10,20,20,30] ke ranks:", np.argsort(np.argsort(tied)),
      "<- dono 20 ko alag rank mila (1 aur 2)")

assert np.array_equal(ranks, [0, 4, 1, 3, 2])
assert np.array_equal(a[order], np.sort(a))
assert np.array_equal(desc, [4, 0, 3, 1, 2])
"""))

# ---- P17
A(md("""
### P17. Har row ke top-3 values (aur unke indices)

**Hint:** `np.argsort(-X, axis=1)[:, :3]` se indices milte hain, phir
`np.take_along_axis` se values. Sirf top-k chahiye to `np.argpartition` O(n) me karta hai.
"""))

A(code("""
X = rng.integers(0, 100, size=(4, 6))
print("X:\\n", X)

k = 3

# --- argsort tareeqa: poora sort (O(n log n)) magar order guaranteed ---
top_idx = np.argsort(-X, axis=1)[:, :k]                  # minus se descending
top_val = np.take_along_axis(X, top_idx, axis=1)          # per-row indices se values

print("\\ntop-3 indices (har row):\\n", top_idx)
print("\\ntop-3 values (har row):\\n", top_val)

# --- argpartition tareeqa: O(n), magar top-k ka andar ka order random ---
part_idx = np.argpartition(-X, k, axis=1)[:, :k]
part_val = np.take_along_axis(X, part_idx, axis=1)
part_val_sorted = -np.sort(-part_val, axis=1)             # baad me sort kar lo
print("\\nargpartition se (sorted):\\n", part_val_sorted)

# Verification: har row ke top-3 waqai us row ki sab se bari 3 values hain
for r in range(X.shape[0]):
    assert np.array_equal(top_val[r], np.sort(X[r])[::-1][:k])

assert top_val.shape == (4, 3)
assert np.array_equal(top_val, part_val_sorted)
assert np.all(np.diff(top_val, axis=1) <= 0)       # har row descending hai
"""))

# ---- P18
A(md("""
### P18. One-hot encoding

Labels `[0, 2, 1, 2, 0]` ko 3-class one-hot matrix me badlo.

**Hint:** `np.eye(n_classes)[labels]` — identity matrix ki rows fancy-index karo.
Ye ML me bohat use hota hai (categorical target → matrix).
"""))

A(code("""
labels = np.array([0, 2, 1, 2, 0])
n_classes = 3

# --- Tareeqa 1: eye + fancy indexing (sab se elegant) ---
onehot = np.eye(n_classes, dtype=int)[labels]
print("labels:", labels)
print("\\none-hot (eye trick):\\n", onehot)

# --- Tareeqa 2: zeros + advanced indexing (manual, samajhne ke liye behtar) ---
oh2 = np.zeros((labels.size, n_classes), dtype=int)
oh2[np.arange(labels.size), labels] = 1     # (row i, column labels[i]) par 1
print("\\nmanual tareeqa same? ", np.array_equal(onehot, oh2))

# --- Tareeqa 3: broadcasting comparison ---
oh3 = (labels[:, None] == np.arange(n_classes)).astype(int)
print("broadcast tareeqa same?", np.array_equal(onehot, oh3))

# Ulta kaam (decode): argmax se wapis labels
print("\\ndecode (argmax axis=1):", onehot.argmax(axis=1))

assert onehot.shape == (5, 3)
assert np.array_equal(onehot.sum(axis=1), np.ones(5))     # har row me theek ek 1
assert np.array_equal(onehot.argmax(axis=1), labels)
assert np.array_equal(onehot, oh2) and np.array_equal(onehot, oh3)
"""))

# ---- P19
A(md("""
### P19. Pairwise Euclidean distance matrix

`(n, d)` points diye hain — `(n, n)` matrix banao jisme `D[i, j]` = point i aur j ka
distance.

**Hint:** Broadcasting: `X[:, None, :] - X[None, :, :]` se `(n, n, d)` differences
banti hain, phir `axis=-1` par square-sum-sqrt.
"""))

A(code("""
X = np.array([[0.0, 0.0],
              [3.0, 4.0],
              [6.0, 8.0]])
print("points:\\n", X)

# Shapes ka khel: (n,1,d) - (1,n,d) -> (n,n,d)
diff = X[:, None, :] - X[None, :, :]
print("\\ndiff ki shape:", diff.shape, "<- (n, n, d)")

D = np.sqrt((diff ** 2).sum(axis=-1))       # aakhri axis (d) par collapse
print("\\ndistance matrix:\\n", D)

print("\\nProperties check:")
print("  diagonal sab 0?  ", np.allclose(np.diag(D), 0))
print("  symmetric hai?   ", np.allclose(D, D.T))
print("  D[0,1] = 3-4-5 triangle ->", D[0, 1])

# Memory warning: (n,n,d) bana lena bare n par khatarnak hai
n, d = 10000, 100
print(f"\\n n={n}, d={d} par (n,n,d) float64 =",
      round(n * n * d * 8 / 1e9, 1), "GB <- RAM uda dega!")
print(" Bare data ke liye: ||a-b||^2 = |a|^2 + |b|^2 - 2 a.b  (matmul se)")

# Wahi natija, memory-efficient formula se
sq = (X ** 2).sum(axis=1)
D2 = np.sqrt(np.maximum(sq[:, None] + sq[None, :] - 2 * X @ X.T, 0))
print("\\n matmul formula se same?", np.allclose(D, D2))

assert D.shape == (3, 3)
assert np.allclose(np.diag(D), 0) and np.allclose(D, D.T)
assert np.isclose(D[0, 1], 5.0) and np.isclose(D[0, 2], 10.0)
assert np.allclose(D, D2)
"""))

# ---- P20
A(md("""
### P20. Matrix ko kisi ek column ke hisaab se sort karo

`(5, 3)` matrix ko column 1 (doosra column) ki values ke hisaab se ascending sort karo —
**poori rows** sath move honi chahiye.

**Hint:** `M[M[:, 1].argsort()]` — argsort se row-order lo aur usse index karo.
"""))

A(code("""
M = np.array([[1, 50, 9],
              [2, 20, 8],
              [3, 90, 7],
              [4, 10, 6],
              [5, 70, 5]])
print("original:\\n", M)

order = M[:, 1].argsort()                # column 1 ke hisaab se row order
sorted_by_c1 = M[order]
print("\\ncolumn 1 ka order:", order)
print("\\ncolumn 1 se sorted:\\n", sorted_by_c1)

# Descending: [::-1] laga do
print("\\ndescending:\\n", M[M[:, 1].argsort()[::-1]])

# Multi-key sort (pehle col 2 phir col 1) -- np.lexsort AAKHRI key ko primary manta hai
data = np.array([[1, 5], [2, 3], [1, 3], [2, 5]])
lex = np.lexsort((data[:, 1], data[:, 0]))    # primary = col 0, secondary = col 1
print("\\nmulti-key (col0 phir col1):\\n", data[lex])

assert np.array_equal(sorted_by_c1[:, 1], [10, 20, 50, 70, 90])
assert np.array_equal(sorted_by_c1[0], [4, 10, 6])      # poori row sath aayi
assert np.array_equal(data[lex], [[1, 3], [1, 5], [2, 3], [2, 5]])
"""))

# ---- P21
A(md("""
### P21. Cosine similarity matrix

`(n, d)` vectors ka pairwise cosine similarity nikalo.

**Formula:** `cos(a, b) = (a . b) / (|a| |b|)`

**Hint:** Pehle har row ko unit-length karo (`np.linalg.norm(..., axis=1, keepdims=True)`),
phir `Xn @ Xn.T` — ek matmul me poora matrix.
"""))

A(code("""
X = np.array([[1.0, 0.0],
              [0.0, 1.0],
              [1.0, 1.0],
              [2.0, 2.0]])
print("vectors:\\n", X)

norms = np.linalg.norm(X, axis=1, keepdims=True)   # (n,1) -> broadcast ho jayega
Xn = X / norms                                     # har row ki lambai ab 1
S = Xn @ Xn.T                                      # normalized dot = cosine

print("\\nnorms:\\n", norms)
print("\\ncosine similarity:\\n", S.round(4))

print("\\nSamajh:")
print("  S[0,1] =", round(float(S[0, 1]), 4), "-> perpendicular vectors, similarity 0")
print("  S[0,2] =", round(float(S[0, 2]), 4), "-> 45 degree ka fark = 1/sqrt(2)")
print("  S[2,3] =", round(float(S[2, 3]), 4), "-> same DIRECTION (magnitude se farq nahi padta)")

assert np.allclose(np.diag(S), 1.0)                  # khud se similarity 1
assert np.isclose(S[0, 1], 0.0)
assert np.isclose(S[0, 2], 1 / np.sqrt(2))
assert np.isclose(S[2, 3], 1.0)
assert np.allclose(S, S.T)
"""))

# ---- P22
A(md("""
### P22. Outliers ko percentile par clip karo (winsorize)

5th aur 95th percentile ke bahar ki tamam values ko un hadd par le aao.

**Hint:** `np.percentile(a, [5, 95])` + `np.clip(a, lo, hi)`.
"""))

A(code("""
a = np.arange(1.0, 101.0)          # 1..100 -- saaf percentiles ke liye
lo, hi = np.percentile(a, [5, 95])
clipped = np.clip(a, lo, hi)

print("a: 1..100")
print("5th percentile :", lo)
print("95th percentile:", hi)
print("\\nclipped ke pehle 8 :", clipped[:8])
print("clipped ke aakhri 8:", clipped[-8:])
print("\\nnaya min/max:", clipped.min(), "/", clipped.max())
print("kitni values badlin:", int((clipped != a).sum()), "out of", a.size)

# Asli outlier scenario
data = np.array([10., 12., 11., 13., 500., 12., 9., -300.])
l2, h2 = np.percentile(data, [10, 90])
print("\\nreal data     :", data)
print("mean pehle    :", round(float(data.mean()), 2), "<- 500 aur -300 ne barbaad kar diya")
print("mean baad me  :", round(float(np.clip(data, l2, h2).mean()), 2))
print("median (robust):", float(np.median(data)), "<- median outliers ko ignore karta hai")

assert np.isclose(lo, 5.95) and np.isclose(hi, 95.05)
assert clipped.min() >= lo and clipped.max() <= hi
assert (clipped != a).sum() == 10        # neeche 5 + upar 5
"""))

# ---- P23
A(md("""
### P23. Duplicates hatao **magar original order barqarar rakho**

`np.unique` sorted deta hai — humein pehli baar aane wale order me chahiye.

**Hint:** `np.unique(a, return_index=True)` se pehli appearance ke indices lo,
un indices ko `np.sort` karo, phir index karo.
"""))

A(code("""
a = np.array([5, 3, 5, 1, 3, 9, 1, 7])
print("a                :", a)

# np.unique sorted deta hai -- order kho jata hai
print("np.unique (sorted):", np.unique(a))

# Order barqarar rakhne ka tareeqa
vals, first_idx = np.unique(a, return_index=True)
keep = np.sort(first_idx)             # pehli appearance ke indices, original order me
ordered_unique = a[keep]

print("\\nunique vals      :", vals)
print("pehli appearance  :", first_idx)
print("sorted indices    :", keep)
print("order-preserved   :", ordered_unique)

# Bonus: counts bhi chahiye (ordered)
_, first2, counts = np.unique(a, return_index=True, return_counts=True)
o = np.argsort(first2)
print("\\nvalue -> count (appearance order):",
      dict(zip(a[np.sort(first2)].tolist(), counts[o].tolist())))

assert np.array_equal(np.unique(a), [1, 3, 5, 7, 9])
assert np.array_equal(ordered_unique, [5, 3, 1, 9, 7])
assert ordered_unique.size == np.unique(a).size
"""))

# ---- P24
A(md("""
### P24. Array ko non-overlapping chunks me todo aur har chunk ka mean nikalo

12 elements ko 4 ke chunks me todo (3 chunks) aur har chunk ka average nikalo.

**Hint:** `reshape(-1, chunk)` phir `.mean(axis=1)`. Agar length divide na hoti ho to
`np.array_split` use karo.
"""))

A(code("""
a = np.arange(1, 13, dtype=float)
chunk = 4

chunks = a.reshape(-1, chunk)        # -1 -> rows khud calculate
means = chunks.mean(axis=1)

print("a      :", a)
print("\\nchunks:\\n", chunks)
print("\\nper-chunk mean:", means)

# reshape sirf tab chalta hai jab poora divide ho
print("\\n12 % 4 =", 12 % 4, "-> reshape theek")
try:
    np.arange(10).reshape(-1, 4)
except ValueError as e:
    print("10 elements 4 ke chunks me:", type(e).__name__, "->", e)

# Uneven data ke liye array_split (aakhri chunk chhota reh jata hai)
parts = np.array_split(np.arange(10), 3)
print("\\narray_split(arange(10), 3):", [p.tolist() for p in parts])
print("sizes:", [p.size for p in parts], "<- barabar nahi, magar crash bhi nahi")

assert chunks.shape == (3, 4)
assert np.allclose(means, [2.5, 6.5, 10.5])
assert sum(p.size for p in parts) == 10
"""))

# ---- P25
A(md("""
### P25. Multi-condition boolean filtering

`0..19` me se wo numbers nikalo jo **5 se bare**, **15 se chhote** aur **even** hon.

**Hint:** `&` (and), `|` (or), `~` (not) — aur **har condition ko brackets me lapetna
lazmi hai** kyunki `&` ki precedence `>` se zyada hai.
"""))

A(code("""
a = np.arange(20)

# Har condition brackets me -- warna precedence bug
mask = (a > 5) & (a < 15) & (a % 2 == 0)
print("a           :", a)
print("mask        :", mask.astype(int))
print("natija      :", a[mask])

# OR aur NOT
print("\\n<3 ya >17   :", a[(a < 3) | (a > 17)])
print("NOT even    :", a[~(a % 2 == 0)])

# GOTCHA 1: Python ka 'and' array par kaam nahi karta
try:
    _ = a[(a > 5) and (a < 15)]
except ValueError as e:
    print("\\n'and' use kiya to:", type(e).__name__)
    print("  ->", str(e)[:75], "...")
    print("  Wajah: 'and' array ka truth-value maangta hai -> ambiguous. '&' use karo.")

# GOTCHA 2: brackets bhool gaye to?
try:
    _ = a > 5 & a < 15
except ValueError as e:
    print("\\nbrackets ke baghair:", type(e).__name__, "-> pehle '5 & a' hota hai (galat)")

assert np.array_equal(a[mask], [6, 8, 10, 12, 14])
assert mask.sum() == 5
assert np.array_equal(a[(a < 3) | (a > 17)], [0, 1, 2, 18, 19])
"""))

# ---- P26
A(md("""
### P26. Missing values ko **column ke mean** se bharo (imputation)

`nan` wali jaghon par us column ka mean daal do (nan ko mean me count na karo).

**Hint:** `np.nanmean(X, axis=0)` nan ignore karta hai; `np.where(np.isnan(X))` se
(row, col) indices milte hain — `col` index se mean uthao.
"""))

A(code("""
X = np.array([[1.0, 10.0, 100.0],
              [2.0, np.nan, 200.0],
              [np.nan, 30.0, np.nan],
              [4.0, 40.0, 400.0]])
print("X (nan ke sath):\\n", X)

col_mean = np.nanmean(X, axis=0)          # nan ko chhod kar per-column mean
print("\\ncolumn means (nan ignore):", col_mean)
print("normal mean hota to:", X.mean(axis=0), "<- sab nan! (nan har cheez ko nan karta hai)")

filled = X.copy()
rows, cols = np.where(np.isnan(X))        # nan kahan kahan hai
print("\\nnan positions -> rows:", rows, "cols:", cols)
filled[rows, cols] = col_mean[cols]       # har nan ki jagah uske COLUMN ka mean

print("\\nfilled:\\n", filled)

# Shortcut form (ek line)
alt = np.where(np.isnan(X), np.nanmean(X, axis=0), X)   # broadcasting (1,3) vs (4,3)
print("\\none-liner same? ", np.allclose(filled, alt))

assert not np.isnan(filled).any()
assert np.isclose(filled[2, 0], np.nanmean(X[:, 0]))    # (1+2+4)/3
assert np.isclose(filled[1, 1], 80 / 3)                 # (10+30+40)/3
assert np.allclose(filled, alt)
"""))

# ---- P27
A(md("""
### P27. Confusion matrix bina loop ke

`y_true` aur `y_pred` (3 classes) se `(3, 3)` confusion matrix banao jahan
`cm[i, j]` = "asli class i thi, model ne j predict kiya".

**Hint:** Har (true, pred) jodi ko ek unique number me badlo: `n * true + pred`,
phir `np.bincount(..., minlength=n*n).reshape(n, n)`.
"""))

A(code("""
y_true = np.array([0, 0, 1, 1, 2, 2, 2])
y_pred = np.array([0, 1, 1, 1, 2, 0, 2])
n = 3

# (true, pred) -> flat index. Ye reshape ki row-major logic hai.
flat = n * y_true + y_pred
cm = np.bincount(flat, minlength=n * n).reshape(n, n)

print("y_true:", y_true)
print("y_pred:", y_pred)
print("flat  :", flat, "<- n*true + pred")
print("\\nconfusion matrix (row = asli, col = predicted):\\n", cm)

# Metrics seedha cm se
acc = np.trace(cm) / cm.sum()                       # diagonal = sahi predictions
per_class_recall = np.diag(cm) / cm.sum(axis=1)     # row-wise
print("\\naccuracy      :", round(float(acc), 4), f"({int(np.trace(cm))}/{int(cm.sum())})")
print("per-class recall:", per_class_recall.round(4))

expected = np.array([[1, 1, 0],
                     [0, 2, 0],
                     [1, 0, 2]])
assert np.array_equal(cm, expected)
assert cm.sum() == y_true.size
assert np.isclose(acc, 5 / 7)
"""))

# ---- P28
A(md("""
### P28. Group-by sum aur mean (SQL ke `GROUP BY` jaisa)

`groups = [0,1,0,2,1,0]`, `values = [10,20,30,40,50,60]` — har group ka sum aur mean.

**Hint:** `np.bincount(groups, weights=values)` seedha group-sums deta hai;
`np.bincount(groups)` counts deta hai. Mean = sums / counts. `np.add.at` bhi option hai.
"""))

A(code("""
groups = np.array([0, 1, 0, 2, 1, 0])
values = np.array([10., 20., 30., 40., 50., 60.])

# --- bincount + weights: sab se tez group-by ---
sums = np.bincount(groups, weights=values)
counts = np.bincount(groups)
means = sums / counts

print("groups:", groups)
print("values:", values)
print("\\ngroup sums  :", sums)
print("group counts:", counts)
print("group means :", means.round(4))

# --- np.add.at: general 'unbuffered' scatter-add (duplicates ko sahi handle karta hai) ---
out = np.zeros(3)
np.add.at(out, groups, values)
print("\\nnp.add.at se same?", np.allclose(out, sums))

# GOTCHA: seedha out[groups] += values GALAT hai (duplicate indices ek hi baar lagte hain)
bad = np.zeros(3)
bad[groups] += values
print("\\nout[groups] += values ka natija:", bad, "<- GALAT")
print("Wajah: buffered operation -- group 0 ke teen values me se sirf aakhri lagi.")

assert np.allclose(sums, [100., 70., 40.])
assert np.array_equal(counts, [3, 2, 1])
assert np.allclose(means, [100 / 3, 35., 40.])
assert np.allclose(out, sums) and not np.allclose(bad, sums)
"""))

# ---- P29
A(md("""
### P29. 2D array me maximum ki (row, col) position

**Hint:** `argmax` **flat** index deta hai — `np.unravel_index(idx, shape)` usay
(row, col) me badalta hai.
"""))

A(code("""
X = rng.integers(0, 100, size=(4, 5))
print("X:\\n", X)

flat_idx = X.argmax()                              # flattened array ka index
r, c = np.unravel_index(flat_idx, X.shape)         # -> (row, col)

print("\\nflat argmax :", flat_idx)
print("unravel se  : row", r, ", col", c)
print("us jagah ki value:", X[r, c], "| X.max() =", X.max())

# Ulta kaam: (row, col) -> flat
print("\\nravel_multi_index se wapis flat:", np.ravel_multi_index((r, c), X.shape))

# Per-axis argmax (poore array ka nahi, har row/col ka)
print("\\nhar row ka argmax:", X.argmax(axis=1))
print("har col ka argmax:", X.argmax(axis=0))

assert X[r, c] == X.max()
assert np.ravel_multi_index((r, c), X.shape) == flat_idx
assert X.argmax(axis=1).shape == (4,)
"""))

# ---- P30
A(md("""
### P30. Matrix multiplication broadcasting se (khud implement karo)

`A @ B` ka natija sirf broadcasting + sum se nikalo (koi `@`, koi `np.dot` nahi).

**Hint:** `A[:, :, None] * B[None, :, :]` se `(m, k, n)` banti hai — phir shared
dimension `k` (axis=1) par sum karo.
"""))

A(code("""
A = np.arange(6).reshape(2, 3)      # (m=2, k=3)
B = np.arange(12).reshape(3, 4)     # (k=3, n=4)

print("A", A.shape, ":\\n", A)
print("\\nB", B.shape, ":\\n", B)

# Shapes: (m,k,1) * (1,k,n) -> (m,k,n) ; phir k par sum -> (m,n)
prod = A[:, :, None] * B[None, :, :]
manual = prod.sum(axis=1)

print("\\nintermediate shape:", prod.shape, "<- (m, k, n)")
print("\\nmanual natija:\\n", manual)
print("\\nA @ B:\\n", A @ B)
print("\\nbarabar hain? ", np.array_equal(manual, A @ B))

# einsum bhi wahi baat, zyada saaf
print("einsum se same?", np.array_equal(np.einsum('mk,kn->mn', A, B), A @ B))

# Kyun @ behtar hai: manual tareeqa (m*k*n) memory leta hai, @ BLAS use karta hai
print("\\n1000x1000 @ 1000x1000 me manual tareeqa banata:",
      round(1000 ** 3 * 8 / 1e9, 1), "GB intermediate -> isliye '@' hi use karo")

assert manual.shape == (2, 4)
assert np.array_equal(manual, A @ B)
assert np.array_equal(np.einsum('mk,kn->mn', A, B), A @ B)
"""))

# ---- P31
A(md("""
### P31. Rolling maximum (window = 3)

**Hint:** `np.lib.stride_tricks.sliding_window_view(a, 3)` se overlapping windows ka
**view** banta hai (extra memory nahi), phir `.max(axis=1)`.
"""))

A(code("""
a = np.array([3, 1, 4, 1, 5, 9, 2, 6])
k = 3

windows = np.lib.stride_tricks.sliding_window_view(a, k)
roll_max = windows.max(axis=1)
roll_min = windows.min(axis=1)
roll_sum = windows.sum(axis=1)

print("a         :", a)
print("\\nwindows (shape", windows.shape, "):\\n", windows)
print("\\nrolling max:", roll_max)
print("rolling min:", roll_min)
print("rolling sum:", roll_sum)

# Ye VIEW hai -- data duplicate nahi hota (bare arrays par bohat aham)
print("\\nwindows.base is a?", windows.base is a, "-> memory shared")

# READ-ONLY: sliding_window_view me likh nahi sakte
print("windows writeable?", windows.flags.writeable, "<- read-only, safety ke liye")

assert windows.shape == (len(a) - k + 1, k)
assert np.array_equal(roll_max, [4, 4, 5, 9, 9, 9])
assert np.array_equal(roll_min, [1, 1, 1, 1, 2, 2])
assert not windows.flags.writeable
"""))

# ---- P32
A(md("""
### P32. Run-Length Encoding (encode + decode)

`[1,1,2,2,2,3,1,1]` → values `[1,2,3,1]`, counts `[2,3,1,2]`. Phir wapis decode.

**Hint:** `np.diff` se pata chalta hai kahan value badli; `np.flatnonzero` un jaghon ke
indices deta hai. Decode ke liye `np.repeat`.
"""))

A(code("""
def rle_encode(a):
    \"\"\"Consecutive runs ko (values, counts) me todta hai. Vectorized, koi loop nahi.\"\"\"
    a = np.asarray(a)
    if a.size == 0:
        return a.copy(), np.array([], dtype=int)
    change = np.flatnonzero(np.diff(a)) + 1        # jahan naya run shuru hota hai
    starts = np.concatenate(([0], change))         # har run ka start
    ends = np.concatenate((change, [a.size]))      # har run ka end (exclusive)
    return a[starts], ends - starts


def rle_decode(values, counts):
    \"\"\"Encode ka ulta -- np.repeat ek hi call me kaam kar deta hai.\"\"\"
    return np.repeat(values, counts)


a = np.array([1, 1, 2, 2, 2, 3, 1, 1])
vals, cnts = rle_encode(a)

print("original:", a)
print("np.diff :", np.diff(a), "<- non-zero = value badli")
print("\\nvalues  :", vals)
print("counts  :", cnts)
print("\\ndecoded :", rle_decode(vals, cnts))
print("round-trip theek? ", np.array_equal(rle_decode(vals, cnts), a))

# Edge cases
print("\\nkhali array   :", rle_encode(np.array([], dtype=int)))
print("sab same [7]*4:", rle_encode(np.array([7, 7, 7, 7])))
print("sab alag      :", rle_encode(np.array([1, 2, 3])))

assert np.array_equal(vals, [1, 2, 3, 1])
assert np.array_equal(cnts, [2, 3, 1, 2])
assert np.array_equal(rle_decode(vals, cnts), a)
assert cnts.sum() == a.size
assert np.array_equal(rle_encode(np.array([7, 7, 7, 7]))[1], [4])
"""))

# ---- P33
A(md("""
### P33. Softmax — numerically stable

`softmax(x)_i = exp(x_i) / sum(exp(x))`, magar bare numbers par `exp` overflow kar
jata hai. Stable version banao.

**Hint:** `exp(x - max(x))` use karo — jawab mathematically same rehta hai magar
overflow nahi hota. 2D ke liye `axis=1` + `keepdims=True`.
"""))

A(code("""
def softmax(x, axis=-1):
    \"\"\"Numerically stable softmax -- max subtract karne se overflow nahi hota.\"\"\"
    x = np.asarray(x, dtype=np.float64)
    x_shift = x - x.max(axis=axis, keepdims=True)   # sab se bara ab 0 -> exp(0)=1
    e = np.exp(x_shift)
    return e / e.sum(axis=axis, keepdims=True)


logits = np.array([1.0, 2.0, 3.0])
p = softmax(logits)
print("logits :", logits)
print("softmax:", p.round(6))
print("sum    :", p.sum(), "<- probabilities, to 1 hona chahiye")

# Naive version bare numbers par phat jata hai
big = np.array([1000.0, 1001.0, 1002.0])
with np.errstate(over='ignore', invalid='ignore'):
    naive = np.exp(big) / np.exp(big).sum()
print("\\nbare logits:", big)
print("naive       :", naive, "<- inf/inf = nan")
print("stable      :", softmax(big).round(6), "<- theek kaam kiya")
print("Note: shift karne se natija wahi rehta hai jo [1,2,3] ka tha.")

# 2D: per-row softmax (batch of logits)
batch = np.array([[1.0, 2.0, 3.0],
                  [1.0, 1.0, 1.0]])
pb = softmax(batch, axis=1)
print("\\nbatch softmax:\\n", pb.round(6))
print("har row ka sum:", pb.sum(axis=1))

assert np.isclose(p.sum(), 1.0)
assert np.allclose(p, [0.09003057, 0.24472847, 0.66524096])
assert np.isnan(naive).any()                       # naive tuta
assert np.allclose(softmax(big), p)                # stable ne same jawab diya
assert np.allclose(pb.sum(axis=1), 1.0)
assert np.allclose(pb[1], [1 / 3, 1 / 3, 1 / 3])   # barabar logits -> uniform
"""))

# ---- P34
A(md("""
### P34. Values ko bins me daalo (binning / bucketing)

Ages ko categories me baanto: child (<18), adult (18-34), middle (35-59), senior (60+).

**Hint:** `np.digitize(x, bins)` batata hai har value kis bin me giri.
`np.histogram` sirf counts chahiye to behtar hai.
"""))

A(code("""
ages = np.array([5, 18, 30, 45, 70])
bins = np.array([0, 18, 35, 60])         # bin ki lower edges
names = np.array(['?', 'child', 'adult', 'middle', 'senior'])

idx = np.digitize(ages, bins)            # 0 = pehli edge se neeche
print("ages   :", ages)
print("bins   :", bins)
print("digitize:", idx)
print("labels :", names[idx])

for age, label in zip(ages, names[idx]):
    print(f"  {age:>3} -> {label}")

# Counts chahiye to histogram
counts, edges = np.histogram(ages, bins=[0, 18, 35, 60, 120])
print("\\nhistogram counts:", counts, "| edges:", edges)
print("Note: histogram ka aakhri bin BOTH ends inclusive hota hai.")

# right=True -> right edge inclusive ho jata hai
print("\\ndigitize(18, [0,18,35,60])             :", np.digitize([18], bins))
print("digitize(18, ..., right=True)          :", np.digitize([18], bins, right=True))

assert np.array_equal(idx, [1, 2, 2, 3, 4])
assert list(names[idx]) == ['child', 'adult', 'adult', 'middle', 'senior']
assert counts.sum() == ages.size
"""))

# ---- P35
A(md("""
### P35. Mini-batch generator (shuffled) — ML training ka asli pattern

`n` samples ko shuffle karo aur `batch_size` ke batches me do. Har epoch me naya shuffle.

**Hint:** `rng.permutation(n)` se shuffled indices lo, `reshape(-1, batch_size)` se
batches banao (bache hue samples ko drop ya alag handle karo).
"""))

A(code("""
def make_batches(n, batch_size, rng_, drop_last=True):
    \"\"\"Shuffled index batches deta hai. drop_last=False -> aakhri chhota batch bhi.\"\"\"
    perm = rng_.permutation(n)                   # indices shuffle (data copy nahi hota)
    n_full = (n // batch_size) * batch_size
    batches = list(perm[:n_full].reshape(-1, batch_size))
    if not drop_last and n_full < n:
        batches.append(perm[n_full:])            # bacha hua chhota batch
    return batches


X = np.arange(100).reshape(10, 10)               # 10 samples, 10 features
y = np.arange(10)

batch_list = make_batches(len(X), 4, np.random.default_rng(0), drop_last=False)
print("10 samples, batch_size=4, drop_last=False:")
for i, b in enumerate(batch_list):
    print(f"  batch {i}: indices {b.tolist()}  -> y = {y[b].tolist()}")

dropped = make_batches(len(X), 4, np.random.default_rng(0), drop_last=True)
print("\\ndrop_last=True ->", len(dropped), "batches (aakhri 2 samples chhoot gaye)")

# Ahem: har index THEEK EK BAAR aata hai (koi sample repeat/miss nahi)
all_idx = np.concatenate(batch_list)
print("\\nsab indices covered?", np.array_equal(np.sort(all_idx), np.arange(10)))

# Har batch ke features nikalna: X[batch] -> (batch_size, n_features)
print("X[batch 0] ki shape:", X[batch_list[0]].shape)

assert len(batch_list) == 3 and len(dropped) == 2
assert np.array_equal(np.sort(np.concatenate(batch_list)), np.arange(10))
assert all(len(b) == 4 for b in dropped)
assert X[batch_list[0]].shape == (4, 10)
"""))

# ================================================================= PERF
A(md("""
---

# Hissa 2 — Performance: Python list vs NumPy

Ab **naap kar** dekhte hain ke vectorization ka faida kitna hai — aur kahan NumPy ka
faida khatam ho jata hai.

**Test:** har element ka square kar ke sum nikalna, teen tareeqon se:
1. Pure Python `for` loop
2. List comprehension + `sum`
3. NumPy vectorized (`(a ** 2).sum()`)
"""))

A(code("""
def py_loop(lst):
    total = 0
    for x in lst:
        total += x * x
    return total


def py_comprehension(lst):
    return sum(x * x for x in lst)


def np_vectorized(arr):
    return (arr ** 2).sum()


# Chhote data par teeno ka jawab same hona chahiye
small_list = list(range(1000))
small_arr = np.arange(1000)
r1, r2, r3 = py_loop(small_list), py_comprehension(small_list), np_vectorized(small_arr)
print("Correctness check:", r1, r2, int(r3))
assert r1 == r2 == int(r3), "teeno ka natija same hona chahiye"
print("Teeno ka jawab same hai -> ab timing naapte hain.\\n")
"""))

A(code("""
# Different sizes par timing -- ek hi size par bharosa mat karo
sizes = [100, 1_000, 10_000, 100_000, 1_000_000]
rows = []

for n in sizes:
    lst = list(range(n))
    arr = np.arange(n)
    # repeats chhote data par zyada (noise kam karne ke liye)
    reps = max(3, min(200, 2_000_000 // n))

    t_loop = timeit.timeit(lambda: py_loop(lst), number=reps) / reps
    t_comp = timeit.timeit(lambda: py_comprehension(lst), number=reps) / reps
    t_np = timeit.timeit(lambda: np_vectorized(arr), number=reps) / reps
    rows.append((n, t_loop, t_comp, t_np))

print(f"{'size':>10} | {'loop (ms)':>10} | {'comp (ms)':>10} | {'numpy (ms)':>10} | {'speedup':>8}")
print("-" * 62)
for n, tl, tc, tn in rows:
    print(f"{n:>10,} | {tl * 1e3:>10.4f} | {tc * 1e3:>10.4f} | {tn * 1e3:>10.4f} | {tl / tn:>7.1f}x")

print("\\nDekhne wali baatein:")
print("  * Chhote arrays (n=100) par NumPy ka faida kam -- overhead (~microseconds) hai.")
print("  * n barhne ke sath speedup barhta jata hai (10x-100x aam baat hai).")
print("  * Exact numbers machine par depend karte hain, TREND aham hai.")

speedup_big = rows[-1][1] / rows[-1][3]
print(f"\\n n = {rows[-1][0]:,} par NumPy {speedup_big:.0f}x tez nikla.")
assert speedup_big > 3, "bare data par NumPy clearly tez hona chahiye"
"""))

A(code("""
# Memory ka farq bhi naapo -- NumPy compact hai
n = 100_000
lst = list(range(n))
arr = np.arange(n, dtype=np.int64)

# List: pointers ka array + har int ek alag Python object
list_bytes = sys.getsizeof(lst) + sum(sys.getsizeof(x) for x in lst[:1000]) / 1000 * n
np_bytes = arr.nbytes

print(f"{n:,} integers:")
print(f"  Python list (approx): {list_bytes / 1e6:>8.2f} MB")
print(f"  NumPy int64 array   : {np_bytes / 1e6:>8.2f} MB")
print(f"  NumPy {list_bytes / np_bytes:.1f}x kam memory le raha hai")

print("\\nWajah:")
print("  list  -> 8 bytes pointer + ~28 bytes per int object, memory me bikhre hue")
print("  array -> sirf 8 bytes per int, ek contiguous block (cache-friendly + SIMD)")

# dtype chhota karke aur bachao
print("\\nint64 :", np.arange(n, dtype=np.int64).nbytes / 1e6, "MB")
print("int32 :", np.arange(n, dtype=np.int32).nbytes / 1e6, "MB  <- aadha")
print("int16 :", np.arange(n, dtype=np.int16).nbytes / 1e6, "MB  <- chauthai")
print("(magar range ka khayal rakho -- int16 ki hadd 32,767 hai)")

assert np_bytes == n * 8
assert list_bytes > np_bytes
"""))

# ================================================================= LEETCODE
A(md("""
---

# Hissa 3 — LeetCode Problems

Har problem ke **do solutions**: (a) **pure Python** (interview-acceptable) aur
(b) **NumPy/vectorized** (real data-work/production ke liye).

> **Interview me generally pure Python expect hota hai** — interviewer tumhari
> array-manipulation aur index-handling ki logic dekhna chahta hai, library ka
> istemal nahi. Agar tum `np.nonzero` se problem solve kar do to woh kahega
> "ab bina NumPy karo". **NumPy version data-science/production context me faida-mand
> hai** (tez, saaf, bare data par practical) — dono aani chahiye.
"""))

# ---- LC 73
A(md("""
### LC 73. Set Matrix Zeroes — Medium

<https://leetcode.com/problems/set-matrix-zeroes/>

**Bayan:** `m x n` matrix diya hai. Agar koi element `0` hai to us element ki **poori row
aur poora column** `0` kar do — **in-place**.

**Trap:** Chalte chalte zeros lagate jao to naye bane zeros ko bhi "original zero" samajh
kar aage cascade ho jayega. Isliye **pehle sab zeros ki positions note karo, phir fill karo**.

**Approach (pure Python):**
1. Pehle pass: kaunsi rows aur kaunse columns me zero hai — do sets me jama karo.
2. Doosra pass: agar row set me hai **ya** column set me hai to `0` likho.

**Time complexity:** O(m × n) — do passes.
**Space complexity:** O(m + n) — do sets. (O(1) version pehli row/column ko hi marker
banata hai — interview ka "follow-up".)
"""))

A(code("""
def setZeroes(matrix):
    \"\"\"LeetCode 73 -- pure Python, in-place. O(m+n) extra space.\"\"\"
    m, n = len(matrix), len(matrix[0])
    zero_rows, zero_cols = set(), set()

    # Pass 1: zeros ki positions note karo (abhi kuch modify NAHI karna)
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == 0:
                zero_rows.add(i)
                zero_cols.add(j)

    # Pass 2: ab safely fill karo
    for i in range(m):
        for j in range(n):
            if i in zero_rows or j in zero_cols:
                matrix[i][j] = 0
    return matrix


m1 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
print("input :", m1)
print("output:", setZeroes(m1))
assert m1 == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

m2 = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
print("\\ninput :", [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]])
print("output:", setZeroes(m2))
assert m2 == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
print("\\nPure Python solution pass")
"""))

A(code("""
def setZeroes_np(matrix):
    \"\"\"NumPy version -- do line me kaam. Positions PEHLE capture hoti hain (mask),
    isliye cascade ka masla khud-ba-khud hal ho jata hai.\"\"\"
    M = np.array(matrix)                     # copy (LeetCode wala in-place chahta hai)
    rows, cols = np.nonzero(M == 0)          # tamam zeros ke (row, col)
    M[rows, :] = 0                           # poori rows
    M[:, cols] = 0                           # poore columns
    return M


t1 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
t2 = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
print("NumPy t1:\\n", setZeroes_np(t1))
print("\\nNumPy t2:\\n", setZeroes_np(t2))

# Broadcasting wala aur bhi chhota tareeqa: row-mask aur col-mask ka OR
def setZeroes_np2(matrix):
    M = np.array(matrix)
    zero_row = (M == 0).any(axis=1)          # (m,)  kis row me zero hai
    zero_col = (M == 0).any(axis=0)          # (n,)  kis col me zero hai
    M[zero_row[:, None] | zero_col[None, :]] = 0    # (m,1) | (1,n) -> (m,n)
    return M


print("\\nbroadcasting version same?", np.array_equal(setZeroes_np2(t1), setZeroes_np(t1)))

assert np.array_equal(setZeroes_np(t1), [[1, 0, 1], [0, 0, 0], [1, 0, 1]])
assert np.array_equal(setZeroes_np(t2), [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]])
assert np.array_equal(setZeroes_np2(t2), setZeroes_np(t2))
print("NumPy solutions pass")
"""))

# ---- LC 240
A(md("""
### LC 240. Search a 2D Matrix II — Medium

<https://leetcode.com/problems/search-a-2d-matrix-ii/>

**Bayan:** Matrix me **har row left→right sorted** hai aur **har column top→bottom
sorted**. Batao `target` maujood hai ya nahi.

**Approach (staircase search):** **Top-right** corner se shuru karo:
- Current value == target → mil gaya.
- Current value > target → is column ki tamam values bari hongi → `col -= 1`.
- Current value < target → is row ki tamam values chhoti hongi → `row += 1`.

Har step me ek poori row **ya** ek poora column khatam ho jata hai.

**Time complexity:** O(m + n) — bohat behtar than O(m × n).
**Space complexity:** O(1).
"""))

A(code("""
def searchMatrix(matrix, target):
    \"\"\"LeetCode 240 -- pure Python staircase search, O(m+n).\"\"\"
    if not matrix or not matrix[0]:
        return False
    r, c = 0, len(matrix[0]) - 1          # top-right corner se shuru
    while r < len(matrix) and c >= 0:
        v = matrix[r][c]
        if v == target:
            return True
        elif v > target:
            c -= 1                        # ye column poora bara hai -> chhod do
        else:
            r += 1                        # ye row poori chhoti hai -> neeche jao
    return False


mat = [[1, 4, 7, 11, 15],
       [2, 5, 8, 12, 19],
       [3, 6, 9, 16, 22],
       [10, 13, 14, 17, 24],
       [18, 21, 23, 26, 30]]

for t in [5, 20, 1, 30, 31, 0]:
    print(f"target {t:>2} -> {searchMatrix(mat, t)}")

assert searchMatrix(mat, 5) is True
assert searchMatrix(mat, 20) is False
assert searchMatrix(mat, 1) is True and searchMatrix(mat, 30) is True
assert searchMatrix(mat, 31) is False and searchMatrix(mat, 0) is False
assert searchMatrix([], 1) is False and searchMatrix([[]], 1) is False
print("\\nPure Python solution pass")
"""))

A(code("""
def searchMatrix_np(matrix, target):
    \"\"\"NumPy version: poora matrix ek saath compare. O(m*n) kaam magar C-speed par.\"\"\"
    M = np.asarray(matrix)
    if M.size == 0:
        return False
    return bool((M == target).any())


def searchMatrix_np_rows(matrix, target):
    \"\"\"Behtar: har row sorted hai -> per-row binary search (searchsorted).\"\"\"
    M = np.asarray(matrix)
    if M.size == 0:
        return False
    # har row me target ki insert position (vectorized nahi, per-row hai magar O(m log n))
    pos = np.array([np.searchsorted(row, target) for row in M])
    valid = pos < M.shape[1]                          # position row ke andar honi chahiye
    if not valid.any():
        return False
    rows = np.flatnonzero(valid)
    return bool((M[rows, pos[valid]] == target).any())


print("any() version   :", [searchMatrix_np(mat, t) for t in [5, 20, 1, 31]])
print("searchsorted ver:", [searchMatrix_np_rows(mat, t) for t in [5, 20, 1, 31]])

print("\\nComplexity ka comparison:")
print("  staircase (Python) : O(m + n)      <- algorithmically sab se behtar")
print("  searchsorted       : O(m log n)")
print("  (M == t).any()     : O(m * n) magar vectorized -> chhote matrix par sab se tez")
print("  Interview me STAIRCASE chahiye -- .any() 'brute force' mana jayega.")

for t in [5, 20, 1, 30, 31, 0]:
    assert searchMatrix_np(mat, t) == searchMatrix(mat, t)
    assert searchMatrix_np_rows(mat, t) == searchMatrix(mat, t)
print("\\nNumPy solutions pass (dono pure Python se match karte hain)")
"""))

# ---- LC 289
A(md("""
### LC 289. Game of Life — Medium

<https://leetcode.com/problems/game-of-life/>

**Bayan:** `m x n` board me har cell live (1) ya dead (0) hai. Ek step ke baad:
- Live cell + 2 ya 3 live padosi → **zinda rehta hai**; warna mar jata hai.
- Dead cell + **theek 3** live padosi → **zinda ho jata hai**.

Padosi = 8 (horizontal, vertical, diagonal). **Sab cells ek saath (simultaneously)**
update hote hain — isliye purani state ka snapshot chahiye.

**Approach (NumPy):** Board ko `np.pad` se 1 ki border do, phir **8 shifted slices** ka
sum le lo — ye ek hi baar me har cell ke live padosi gin deta hai. Koi nested loop nahi.

**Time complexity:** O(m × n) (NumPy me 8 vectorized additions).
**Space complexity:** O(m × n) — padded copy + neighbour count.
"""))

A(code("""
def gameOfLife(board):
    \"\"\"LeetCode 289 -- pure Python, in-place. Snapshot se simultaneity guarantee.\"\"\"
    m, n = len(board), len(board[0])
    snap = [row[:] for row in board]          # purani state ki copy

    for i in range(m):
        for j in range(n):
            live = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == 0 and dj == 0:
                        continue              # khud ko nahi ginna
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n:   # boundary check
                        live += snap[ni][nj]
            if snap[i][j] == 1:
                board[i][j] = 1 if live in (2, 3) else 0
            else:
                board[i][j] = 1 if live == 3 else 0
    return board


b = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
print("pehle :", [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]])
print("baad  :", gameOfLife(b))
assert b == [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]

# Blinker: 3 in a row <-> 3 in a column (period-2 oscillator)
blink = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
assert gameOfLife([r[:] for r in blink]) == [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
print("\\nblinker theek oscillate karta hai")
print("Pure Python solution pass")
"""))

A(code("""
def gameOfLife_np(board):
    \"\"\"NumPy: 8 shifted slices ka sum = neighbour count. Zero nested loops.\"\"\"
    b = np.asarray(board, dtype=np.int64)
    m, n = b.shape
    p = np.pad(b, 1)                                    # border of zeros -> boundary check khatam

    # 8 directions ke shifted views ko jama karo
    neigh = np.zeros_like(b)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            neigh += p[1 + di:1 + di + m, 1 + dj:1 + dj + n]

    # Rules ko ek boolean expression me
    alive_next = (neigh == 3) | ((b == 1) & (neigh == 2))
    return alive_next.astype(int)


b0 = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]])
print("board:\\n", b0)
nxt = gameOfLife_np(b0)
print("\\nnext generation:\\n", nxt)
print("\\nexpected:\\n", np.array([[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]))

# Neighbour count khud dekho -- yehi asli trick hai
p = np.pad(b0, 1)
counts = sum(p[1 + di:1 + di + 4, 1 + dj:1 + dj + 3]
             for di in (-1, 0, 1) for dj in (-1, 0, 1) if (di, dj) != (0, 0))
print("\\nhar cell ke live padosi:\\n", counts)

# Blinker 2 steps me wapis original par aata hai
blink = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])
assert np.array_equal(gameOfLife_np(gameOfLife_np(blink)), blink)

assert np.array_equal(nxt, [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]])
assert np.array_equal(gameOfLife_np(blink), [[0, 1, 0], [0, 1, 0], [0, 1, 0]])
print("\\nNumPy solution pass (blinker ka period bhi 2 nikla)")
"""))

# ---- LC 304
A(md("""
### LC 304. Range Sum Query 2D (Immutable) — Medium

<https://leetcode.com/problems/range-sum-query-2d-immutable/>

**Bayan:** Matrix diya hai. Bohat si queries aayengi: `(r1, c1)` se `(r2, c2)` tak ke
rectangle ka sum batao. Har query **O(1)** me chahiye.

**Approach (2D prefix sum):** `pre[i+1][j+1]` = `(0,0)` se `(i,j)` tak ka total sum.
Phir kisi bhi rectangle ka sum **inclusion-exclusion** se:

```
sum = pre[r2+1][c2+1] - pre[r1][c2+1] - pre[r2+1][c1] + pre[r1][c1]
```

(Bara block minus upar wala minus baayen wala plus do baar ghata hua corner.)

**Time complexity:** build O(m × n), har query **O(1)**.
**Space complexity:** O(m × n).
"""))

A(code("""
class NumMatrix:
    \"\"\"LeetCode 304 -- pure Python. Padding row/col se index ka jhanjhat khatam.\"\"\"

    def __init__(self, matrix):
        m, n = len(matrix), len(matrix[0])
        # (m+1) x (n+1) -- pehli row/col zeros, taake r1-1 wala case handle na karna pare
        self.pre = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                self.pre[i + 1][j + 1] = (self.pre[i][j + 1]      # upar ka
                                          + self.pre[i + 1][j]    # baayen ka
                                          - self.pre[i][j]        # do baar gina hua
                                          + matrix[i][j])

    def sumRegion(self, r1, c1, r2, c2):
        p = self.pre
        return p[r2 + 1][c2 + 1] - p[r1][c2 + 1] - p[r2 + 1][c1] + p[r1][c1]


matrix = [[3, 0, 1, 4, 2],
          [5, 6, 3, 2, 1],
          [1, 2, 0, 1, 5],
          [4, 1, 0, 1, 7],
          [1, 0, 3, 0, 5]]
nm = NumMatrix(matrix)

print("sumRegion(2,1,4,3) =", nm.sumRegion(2, 1, 4, 3), "(expected 8)")
print("sumRegion(1,1,2,2) =", nm.sumRegion(1, 1, 2, 2), "(expected 11)")
print("sumRegion(1,2,2,4) =", nm.sumRegion(1, 2, 2, 4), "(expected 12)")
print("poora matrix       =", nm.sumRegion(0, 0, 4, 4))

assert nm.sumRegion(2, 1, 4, 3) == 8
assert nm.sumRegion(1, 1, 2, 2) == 11
assert nm.sumRegion(1, 2, 2, 4) == 12
assert nm.sumRegion(0, 0, 4, 4) == sum(sum(r) for r in matrix)
assert nm.sumRegion(0, 0, 0, 0) == 3          # single cell
print("\\nPure Python solution pass")
"""))

A(code("""
class NumMatrixNP:
    \"\"\"NumPy: 2D prefix sum = do cumsum (pehle rows par, phir columns par).\"\"\"

    def __init__(self, matrix):
        a = np.asarray(matrix, dtype=np.int64)
        # cumsum(axis=0) phir cumsum(axis=1) = 2D prefix sum
        # np.pad se upar/baayen ek zero row/col -> formula seedha lag jata hai
        self.pre = np.pad(a.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)))

    def sumRegion(self, r1, c1, r2, c2):
        p = self.pre
        return int(p[r2 + 1, c2 + 1] - p[r1, c2 + 1] - p[r2 + 1, c1] + p[r1, c1])


nmp = NumMatrixNP(matrix)
print("prefix table (padded):\\n", nmp.pre)

queries = [(2, 1, 4, 3), (1, 1, 2, 2), (1, 2, 2, 4), (0, 0, 4, 4), (3, 3, 3, 3)]
print("\\n query              | python | numpy | brute-force")
print("-" * 52)
arr = np.asarray(matrix)
for q in queries:
    r1, c1, r2, c2 = q
    brute = int(arr[r1:r2 + 1, c1:c2 + 1].sum())      # seedha slice-sum (verification)
    print(f" {str(q):<18} | {nm.sumRegion(*q):>6} | {nmp.sumRegion(*q):>5} | {brute:>11}")
    assert nm.sumRegion(*q) == nmp.sumRegion(*q) == brute

print("\\nTeeno tareeqe match karte hain.")
print("Note: ek hi query ho to slice-sum kaafi hai; HAZARON queries par prefix-sum jeetta hai.")
"""))

# ---- LC 118
A(md("""
### LC 118. Pascal's Triangle — Easy

<https://leetcode.com/problems/pascals-triangle/>

**Bayan:** `numRows` diye hain — Pascal's triangle ki pehli `numRows` rows return karo.
Har number apne upar wale do numbers ka sum hota hai.

**Approach (pure Python):** Har row `[1] * (i+1)` se shuru karo (kinare hamesha 1),
phir andar wale positions `prev[j-1] + prev[j]` se bharo.

**NumPy trick:** Nayi row = purani row ka `np.convolve(prev, [1, 1])` — kyunki
convolution bilkul yehi "shifted add" karta hai.

**Time complexity:** O(numRows²) — jitne numbers hain.
**Space complexity:** O(numRows²) output ke liye.
"""))

A(code("""
def generate(numRows):
    \"\"\"LeetCode 118 -- pure Python.\"\"\"
    tri = []
    for i in range(numRows):
        row = [1] * (i + 1)                 # kinare 1
        for j in range(1, i):               # andar wale (0 aur i ko chhod kar)
            row[j] = tri[i - 1][j - 1] + tri[i - 1][j]
        tri.append(row)
    return tri


for r in generate(6):
    print(str(r).center(40))

assert generate(1) == [[1]]
assert generate(5) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
assert generate(0) == []
print("\\nPure Python solution pass")
"""))

A(code("""
def generate_np(numRows):
    \"\"\"NumPy: nayi row = convolve(purani row, [1,1]).\"\"\"
    tri, row = [], np.array([1])
    for _ in range(numRows):
        tri.append(row)
        row = np.convolve(row, [1, 1])      # [a,b] -> [a, a+b, b]  = shifted add
    return tri


print("convolve se:")
for r in generate_np(6):
    print(str(r.tolist()).center(40))

# Alternative: nth row seedha binomial coefficients se (cumprod formula)
def pascal_row(n):
    \"\"\"C(n,0..n) bina factorial ke: C(n,k) = C(n,k-1) * (n-k+1)/k\"\"\"
    k = np.arange(1, n + 1)
    return np.concatenate(([1], np.cumprod((n - k + 1) / k))).round().astype(int)


print("\\nrow 4 seedha formula se:", pascal_row(4).tolist())
print("row 6 seedha formula se:", pascal_row(6).tolist())
print("row 10 ka sum          :", pascal_row(10).sum(), "= 2^10 =", 2 ** 10)

got = [r.tolist() for r in generate_np(5)]
assert got == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
assert pascal_row(4).tolist() == [1, 4, 6, 4, 1]
assert pascal_row(10).sum() == 2 ** 10          # har row ka sum 2^n hota hai
print("\\nNumPy solutions pass")
"""))

# ==END==
