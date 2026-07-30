import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

cells = []

# ============================================================
# 1. TITLE + ROADMAP + PREREQUISITES
# ============================================================
cells.append(md("""
# 02 — Indexing, Slicing, Reshaping aur Joining

**Level:** Beginner → Intermediate
**Series:** NumPy Basics

## Is notebook me kya seekhenge (roadmap)

1. 1D indexing/slicing — negative index, step, reverse, out-of-range gotcha
2. **Views vs Copies** — is notebook ka sab se important concept
3. 2D/3D indexing — `arr[i, j]` vs `arr[i][j]`, Ellipsis (`...`)
4. Boolean / mask indexing — `&`, `|`, `~`, `np.where`, `np.any`/`np.all`
5. Fancy (integer-array) indexing — broadcasting, `np.take`, `np.put`
6. Boolean + fancy combine, `np.ix_`, common submatrix mistake
7. Shape manipulation — `reshape`, `ravel` vs `flatten`, `transpose`, `newaxis`, `resize`
8. Joining — `concatenate`, `vstack`/`hstack`/`dstack`/`column_stack`/`stack`
9. Splitting — `split`, `array_split`, `vsplit`/`hsplit`
10. `insert`/`delete`/`append`, `tile` vs `repeat`, `flip`/`roll`/`rot90`
11. Sorting — `np.sort` vs `arr.sort()`, `argsort`
12. `np.unique`, `np.isin`

Phir: **Common Mistakes**, **Real-World Problems**, **LeetCode (5 problems)**,
**Interview Q&A**, **Practice Exercises**, aur ek **Cheat-sheet**.

## Prerequisites

- NumPy Basics NB1 (arrays banana, dtypes, basic operations, broadcasting ka intro).
- Python lists, loops, aur `try/except` ka basic pata ho.

## Environment note

- Python 3.14, **NumPy 2.4.2**. NumPy 2.x me kuch cheezein badal gayi hain
  (`np.in1d` removed, `arr.ptp()` method nahi raha, waghera) — jahan zaroorat hogi
  wahan notebook me clearly bataya jayega.

> **Golden rule:** Yeh notebook top-se-bottom chalao. Har cell pichle cell ke variables
> use karta hai.
"""))

cells.append(code("""
# Imports aur reproducibility ke liye seed wala random generator
import numpy as np

rng = np.random.default_rng(42)   # NumPy ka modern random API — seed fix taake results repeatable hon
print("NumPy version:", np.__version__)
"""))

# ============================================================
# 2. 1D INDEXING / SLICING
# ============================================================
cells.append(md("""
## 1. 1D Indexing aur Slicing

**Kya hai:** Array ke andar ek ya zyada elements select karne ka tareeqa — single index
(`arr[2]`) ya range (`arr[1:4]`).

**Kyun / kahan use hota hai:** Data ka koi bhi hissa nikalna ho — pehla element, aakhri
5 rows, har doosra sample — sab indexing/slicing se hota hai.

**Syntax:** `arr[start:stop:step]` — Python list slicing jaisa hi hai, bas NumPy me yeh
zyada powerful hai (multi-dimensional, boolean, fancy waghera — aage aayega).
"""))

cells.append(code("""
arr = np.array([10, 20, 30, 40, 50])
print("arr        :", arr)
print("arr[0]     :", arr[0])       # pehla element
print("arr[-1]    :", arr[-1])      # negative index -> aakhri element
print("arr[2]     :", arr[2])       # third element (0-indexed)
"""))

cells.append(code("""
# Slicing: start:stop:step (stop exclusive hota hai)
print("arr[1:4]   :", arr[1:4])     # index 1,2,3
print("arr[:3]    :", arr[:3])      # shuru se index 2 tak
print("arr[2:]    :", arr[2:])      # index 2 se aakhir tak
print("arr[::2]   :", arr[::2])     # har doosra element
print("arr[::-1]  :", arr[::-1])    # POORA array reverse — step=-1 ka jadu
print("arr[-3:-1] :", arr[-3:-1])   # negative start/stop bhi chal sakta hai
"""))

cells.append(md("""
### Gotcha: out-of-range INDEX vs out-of-range SLICE

Yeh ek common confusion hai jahan naye log phaste hain:

- Out-of-range **index** (`arr[100]`) → `IndexError` deta hai.
- Out-of-range **slice** (`arr[2:100]`) → error NAHI deta, bas jitna available hai utna
  return kar deta hai (ya empty array agar kuch bhi na mile).

**Interview tip:** Yeh farq bata dena interviewer ko impress karta hai — matlab tumhe
Python slicing semantics ache se pata hain.
"""))

cells.append(code("""
try:
    print(arr[10])          # index 10 exist nahi karta -> IndexError
except IndexError as e:
    print("IndexError:", e)

# lekin slicing me out-of-range bounds SILENTLY clip ho jate hain, error nahi aati
print("arr[2:100]   :", arr[2:100])     # jitna mila utna diya
print("arr[100:200] :", arr[100:200])   # kuch nahi mila -> empty array, error nahi
"""))

# ============================================================
# 3. VIEWS VS COPIES (dil / core concept)
# ============================================================
cells.append(md("""
## 2. Views vs Copies — Is Notebook Ka Sab Se Important Concept

**Kya hai:** Jab tum basic slicing (`arr[1:4]`) karte ho, NumPy naya data **copy nahi**
karta — bas ek naya array-object banata hai jo **wahi memory** ("buffer") dekhta hai jo
original array use kar raha hai. Isay **view** kehte hain.

**Kyun:** Agar har slice pe pura data copy ho, to bade arrays (millions of elements) ke
sath kaam karna bohat slow aur memory-heavy ho jaye. View banana **O(1)** hai (bas
metadata: shape, stride, offset) — chahe array kitna bhi bara ho.

**Konsi operations view deti hain, konsi copy:**
- **View:** basic slicing (`arr[1:4]`), `reshape` (agar possible ho), `ravel`
  (agar contiguous ho), `.T` / transpose, `arr[:, 0]` jaisi basic indexing
- **Copy:** fancy/integer-array indexing, boolean/mask indexing, `.copy()`, `flatten`,
  arithmetic operations (`arr + 1` naya array banata hai)

Chalo proof dekhte hain.
"""))

cells.append(code("""
base = np.arange(10)
view = base[2:6]           # basic slice -> yeh VIEW hai, copy nahi
print("base:", base)
print("view:", view)

view[0] = 999               # view ko modify kiya
print()
print("view[0] = 999 karne ke baad:")
print("base:", base)        # base bhi badal gaya! kyunke same memory hai
print("view:", view)
"""))

cells.append(code("""
# Proof ke tools: .base, np.shares_memory, np.may_share_memory, .flags['OWNDATA']
print("view.base is base            :", view.base is base)
print("np.shares_memory(view, base) :", np.shares_memory(view, base))
print("np.may_share_memory(view,base):", np.may_share_memory(view, base))
print("view.flags['OWNDATA']        :", view.flags['OWNDATA'])   # False -> data khud own nahi karta
print("base.flags['OWNDATA']        :", base.flags['OWNDATA'])   # True  -> base khud data ka malik hai
"""))

cells.append(md("""
`np.shares_memory` **exact** check karta hai (thora slow, guaranteed correct).
`np.may_share_memory` **fast heuristic** hai — kabhi kabhi "shayad share karta hai" bol
sakta hai jab actually nahi karta (false positive mumkin, false negative nahi). Production
correctness checks me `shares_memory` use karo, quick sanity checks me `may_share_memory`.
"""))

cells.append(code("""
# .copy() se DEEP copy milta hai — ab dono independent hain
base2 = np.arange(10)
copy_arr = base2[2:6].copy()   # explicit copy
copy_arr[0] = -1

print("base2 (unchanged):", base2)
print("copy_arr         :", copy_arr)
print("copy_arr.base is None       :", copy_arr.base is None)
print("np.shares_memory(copy_arr, base2):", np.shares_memory(copy_arr, base2))
"""))

cells.append(md("""
**Interview tip:** Agar poocha jaye "NumPy slicing view kyun deta hai copy kyun nahi?" —
jawab: **performance aur memory efficiency**. Bare datasets (jaise images, ML data) ke
sath baar baar copy banana bohat expensive hota; view O(1) hai chahe array kitna bara ho.
Lekin isi wajah se **accidental mutation** ka risk hota hai — agar tumhe original data
safe rakhna hai to explicitly `.copy()` karo.
"""))

# ============================================================
# 4. 2D / 3D INDEXING
# ============================================================
cells.append(md("""
## 3. 2D / 3D Indexing

**Kya hai:** Multi-dimensional arrays me row aur column dono specify karke element/region
nikalna.

**Syntax:** `arr[row, col]` — comma se dono dimensions ek hi indexing operation me.

**`arr[i, j]` vs `arr[i][j]` — kyun pehla behtar hai:**
- `arr[i][j]` **do steps** me hota hai: pehle `arr[i]` ek naya intermediate array
  (view) banata hai, phir us par `[j]` lagta hai. Extra intermediate object bante hain.
- `arr[i, j]` **ek hi step** me seedha element tak pohanchta hai — zyada fast aur
  NumPy-idiomatic. Assignment ke waqt bhi safer hai (chained indexing kabhi kabhi
  unexpected behavior de sakti hai jab beech ka step copy return kar de).
"""))

cells.append(code("""
mat = np.arange(1, 13).reshape(3, 4)
print("mat:\\n", mat)
print()
print("mat[1, 2] ->", mat[1, 2])   # recommended: single step
print("mat[1][2] ->", mat[1][2])   # works, lekin do steps (mat[1] pehle ek view banata hai)
"""))

cells.append(code("""
# Row aur column slicing
print("Row 1 (mat[1, :])   :", mat[1, :])
print("Col 2 (mat[:, 2])   :", mat[:, 2])
print("Sub-matrix mat[0:2, 1:3]:\\n", mat[0:2, 1:3])
"""))

cells.append(code("""
# Ellipsis (...) -> "baqi saari dimensions jitni bhi hon, unhe : samjho"
arr3d = np.arange(24).reshape(2, 3, 4)
print("arr3d.shape:", arr3d.shape)

print("arr3d[..., 0] shape :", arr3d[..., 0].shape)   # arr3d[:, :, 0] ke barabar
print("arr3d[0, ...] shape :", arr3d[0, ...].shape)   # arr3d[0, :, :] ke barabar

import numpy as _np_check
print("dono barabar hain?  :", _np_check.array_equal(arr3d[..., 0], arr3d[:, :, 0]))
"""))

cells.append(md("""
**3D par mental model:** `arr3d` ko socho as "3 rows aur 4 columns wale **2 blocks**"
(shape `(2, 3, 4)` = block, row, col).
- `arr3d[0]` → pehla poora block (3x4 matrix)
- `arr3d[0, 1]` → pehle block ki row 1 (4 elements)
- `arr3d[0, 1, 2]` → pehle block, row 1, column 2 ka single element
- `arr3d[:, :, 0]` ya `arr3d[..., 0]` → har block ke har row ka **pehla column** (2x3
  ka result)

`...` bohat useful hai jab dimensions ki tadaad pata na ho ya likhna lamba ho jaye
(jaise image processing me `img[..., 0]` = "red channel, chahe image (H,W,3) ho ya
(N,H,W,3) batch ho").
"""))

# ============================================================
# 5. BOOLEAN / MASK INDEXING
# ============================================================
cells.append(md("""
## 4. Boolean / Mask Indexing

**Kya hai:** Array par ek condition lagao (jaise `arr > 0`) — result ek **boolean array**
(mask) hota hai. Yeh mask array ko index karne ke liye use hota hai — `True` wale
positions select ho jate hain.

**Kyun:** Data filtering ka sab se common tareeqa — "sirf woh rows do jo condition
satisfy karein" — pandas ke `df[df['col'] > 5]` ka bhi yehi core idea hai.

**Syntax:** `arr[condition]`
"""))

cells.append(code("""
data = np.array([5, -3, 8, -1, 0, 12, -7])
mask = data > 0
print("data:", data)
print("mask (data > 0):", mask)
print("data[mask]     :", data[mask])   # sirf positive values
"""))

cells.append(md("""
### `&`, `|`, `~` — aur `and`/`or` kyun FAIL karte hain

Python ke `and`/`or`/`not` **sirf single boolean** par kaam karte hain (short-circuit
logic). Jab tum `array1 > 0 and array2 < 10` likhte ho, Python `array1 > 0` (jo ek poora
boolean **array** hai) ko `bool()` me convert karne ki koshish karta hai — aur agar us
array me 1 se zyada elements hon, NumPy nahi decide kar sakta ke "True" ka matlab kya hai
(saare True? koi ek True?). Isliye **`ValueError`** aata hai.

**Solution:** elementwise operators use karo: `&` (and), `|` (or), `~` (not) — aur
**brackets lazmi hain** kyunke `&`/`|` ki Python me precedence `>`/`<` se zyada hoti hai
(warna galat parsing ho jayegi).
"""))

cells.append(code("""
try:
    if data > 0 and data < 10:   # yeh FAIL hoga
        pass
except ValueError as e:
    print("ValueError:", e)

# Sahi tareeqa: & aur | ke sath brackets
cond1 = (data > -5) & (data < 10)     # AND
print("(-5 < data < 10):", data[cond1])

cond2 = (data < 0) | (data > 10)      # OR
print("(data<0 OR data>10):", data[cond2])

cond3 = ~(data > 0)                   # NOT
print("NOT(data>0):", data[cond3])
"""))

cells.append(code("""
# np.where (1-arg form) -> matching INDICES deta hai, values nahi
idx = np.where(data > 0)
print("np.where(data > 0) ->", idx)          # tuple of arrays (per-dimension)
print("data[idx]           ->", data[idx])   # values nikalne ke liye index use karo

# Mask se assignment -> negative values ko 0 se replace karo
data_clean = data.copy()
data_clean[data_clean < 0] = 0
print("data_clean:", data_clean)
"""))

cells.append(code("""
# np.any / np.all + axis
mat2 = np.array([[1, 0, 3],
                  [0, 0, 0],
                  [4, 5, 6]])

print("any per column (axis=0):", np.any(mat2 > 0, axis=0))
print("any per row    (axis=1):", np.any(mat2 > 0, axis=1))
print("all per row    (axis=1):", np.all(mat2 > 0, axis=1))
print("any overall             :", np.any(mat2 > 0))
"""))

cells.append(md("""
### Gotcha: Boolean mask ki shape/length array se match honi lazmi hai

Agar mask ka size array se mismatch ho, `IndexError` aati hai (silent wrong result NAHI
milta — yeh acchi baat hai, bug jaldi pakra jata hai).
"""))

cells.append(code("""
try:
    bad_mask = np.array([True, False])   # sirf 2 elements, data me 7 hain
    print(data[bad_mask])
except IndexError as e:
    print("IndexError:", e)
"""))

# ============================================================
# 6. FANCY / INTEGER-ARRAY INDEXING
# ============================================================
cells.append(md("""
## 5. Fancy (Integer-Array) Indexing

**Kya hai:** Ek integer array (ya list) ko index ke tor par use karna — jitne indices
utne hi results, **kisi bhi order** me, **repeat** ke sath bhi.

**Kyun:** Jab specific, non-contiguous elements chahiye ho (jaise "row 0, 3, aur 7" ya
"columns [2, 5, 1]" kisi specific order me) — slicing yeh nahi kar sakti, fancy indexing
kar sakti hai.

**Syntax:** `arr[[i1, i2, i3]]` ya `arr[np.array([i1, i2, i3])]`
"""))

cells.append(code("""
arr = np.array([100, 200, 300, 400, 500])

idx = [0, 2, 4]
print("arr[[0,2,4]]  ->", arr[idx])          # order jo diya wahi milega

idx2 = np.array([4, 4, 1, 1])
print("arr[[4,4,1,1]]->", arr[idx2])         # repeat indices allowed, order preserve
"""))

cells.append(code("""
# 2D fancy indexing -> index arrays PAIRWISE broadcast hote hain (element-by-element)
mat = np.arange(1, 17).reshape(4, 4)
print("mat:\\n", mat)

rows = np.array([0, 2])
cols = np.array([1, 3])
print("mat[rows, cols] ->", mat[rows, cols])   # (mat[0,1], mat[2,3]) -> pairwise, 2 elements
"""))

cells.append(code("""
# np.take aur np.put -> fancy indexing ke function-form equivalents
arr = np.arange(10)
print("np.take(arr, [0,2,5]) ->", np.take(arr, [0, 2, 5]))

np.put(arr, [0, 2], [-1, -2])   # specific positions ko naye values se set karo
print("np.put ke baad arr     ->", arr)
"""))

cells.append(md("""
**Order preservation & repeat indices:** fancy indexing bilkul waisi order deti hai jaisi
tumne index array me di — chahe repeat ho ya out-of-order ho. Yeh boolean masking se
farq hai (jo hamesha original array ki order me results deti hai, sirf True wale rakhti
hai).
"""))

cells.append(code("""
# PROOF: fancy indexing COPY deti hai, view NAHI (basic slicing se bara farq)
arr = np.arange(5)
fancy = arr[[0, 1, 2]]      # fancy indexing
fancy[0] = 999

print("arr (unchanged)  :", arr)     # arr par koi asar nahi
print("fancy            :", fancy)
print("shares_memory?   :", np.shares_memory(arr, fancy))   # False -> copy thi
"""))

# ============================================================
# 7. BOOLEAN+FANCY COMBINE, np.ix_, COMMON MISTAKE
# ============================================================
cells.append(md("""
## 6. Boolean + Fancy Combine, `np.ix_`, aur Common Mistake

**Kya hai:** Fancy aur boolean indexing ko combine karke complex selections banana, aur
`np.ix_` jo **"open mesh"** (cross-product) tareeqe se rows x columns ka sub-matrix nikalta
hai.
"""))

cells.append(code("""
mat = np.arange(1, 17).reshape(4, 4)
print("mat:\\n", mat)

rows = np.array([0, 2])              # fancy: specific rows
mask_cols = np.array([True, False, True, False])   # boolean: specific columns

# pehle rows select karo (fancy), phir un rows me se columns filter karo (boolean)
sub = mat[rows][:, mask_cols]
print("rows [0,2], columns [0,2] (mask se):\\n", sub)
"""))

cells.append(code("""
# np.ix_ -> "open mesh": rows x cols ka poora cross-product sub-matrix ek hi call me
sub2 = mat[np.ix_([0, 2], [1, 3])]
print("np.ix_([0,2],[1,3]) sub-matrix:\\n", sub2)
print("shape:", sub2.shape)   # (2, 2) -> asal sub-matrix
"""))

cells.append(md("""
### Common Mistake: `arr[[0,2],[1,3]]` sub-matrix NAHI deta!

Bohat log yeh expect karte hain ke `mat[[0,2],[1,3]]` unhe rows 0,2 aur columns 1,3 ka
**2x2 sub-matrix** de dega — **galat**! Yeh actually **pairwise** pairs (0,1) aur (2,3)
ke elements deta hai (jaisa Section 5 me dekha) — sirf **2 elements**, 2x2 matrix nahi.

Sahi sub-matrix ke liye `np.ix_` use karo (jaisa upar dikhaya).
"""))

cells.append(code("""
wrong = mat[[0, 2], [1, 3]]     # yeh sub-matrix NAHI hai
print("mat[[0,2],[1,3]] ->", wrong)
print("shape:", wrong.shape)    # (2,) -> sirf 2 elements, 2x2 nahi!

correct = mat[np.ix_([0, 2], [1, 3])]
print("np.ix_ se sahi sub-matrix:\\n", correct, " shape:", correct.shape)
"""))

# ============================================================
# 8. SHAPE MANIPULATION
# ============================================================
cells.append(md("""
## 7. Shape Manipulation

### `reshape` — order='C' vs order='F', `-1` ka jadu

**Kya hai:** Array ke total elements same rakh kar shape badalna.

**`order` parameter:**
- `'C'` (default) — **row-major**: last axis sab se tezi se change hoti hai (C
  language jaisi memory layout)
- `'F'` — **column-major**: first axis sab se tezi se change hoti hai (Fortran style)

`-1` ka matlab hai "yeh dimension khud calculate kar lo" — sirf ek dimension me `-1` use
kar sakte ho.
"""))

cells.append(code("""
arr = np.arange(12)
print("reshape(3,4) order=C (default):\\n", arr.reshape(3, 4))
print()
print("reshape(3,4) order=F:\\n", arr.reshape(3, 4, order='F'))
print()
print("reshape(3,-1) -> NumPy khud dusra dimension nikal leta hai:\\n", arr.reshape(3, -1))
"""))

cells.append(code("""
# Error case: agar total elements match na karein
try:
    arr.reshape(5, 3)   # 12 elements ko 15 slots me fit nahi kar sakte
except ValueError as e:
    print("ValueError:", e)
"""))

cells.append(md("""
### `ravel` vs `flatten` — VIEW vs COPY

Dono 1D array wapis dete hain, lekin:
- `.ravel()` **view deta hai jab possible ho** (array already contiguous ho to copy nahi
  banata) — fast, memory-efficient.
- `.flatten()` **hamesha copy** deta hai — safe (original par asar nahi), thora slower.
"""))

cells.append(code("""
mat = np.arange(6).reshape(2, 3)
r = mat.ravel()      # view (kyunke mat C-contiguous hai)
f = mat.flatten()     # hamesha copy

r[0] = 999
print("mat after ravel[0]=999 (mat BADAL gaya):\\n", mat)

f[0] = -999
print("mat after flatten[0]=-999 (mat WAISE hi raha):\\n", mat)

print("shares_memory(mat, r) [ravel] :", np.shares_memory(mat, r))
print("shares_memory(mat, f) [flatten]:", np.shares_memory(mat, f))
"""))

cells.append(md("""
### `transpose` / `.T` / `swapaxes` / `moveaxis`

- `.T` / `np.transpose(arr)` — saari axes ka order **reverse** kar deta hai (2D me
  rows<->cols swap)
- `.swapaxes(a, b)` — sirf do specific axes ko swap karta hai
- `np.moveaxis(arr, src, dst)` — ek axis ko specific position par le jata hai, baqi
  order preserve rehta hai
"""))

cells.append(code("""
arr3d = np.arange(24).reshape(2, 3, 4)
print("original shape       :", arr3d.shape)
print(".T shape             :", arr3d.T.shape)                 # (4,3,2) -> poora reverse
print("swapaxes(0,1) shape  :", arr3d.swapaxes(0, 1).shape)      # (3,2,4) -> sirf 0,1 swap
print("moveaxis(0,-1) shape :", np.moveaxis(arr3d, 0, -1).shape) # (3,4,2) -> axis 0 ko end par
"""))

cells.append(md("""
### `np.newaxis` / `None`, `expand_dims`, `squeeze`

Naya dimension add/remove karne ke liye — machine learning me bohat common (batch
dimension add karna, single-element dimensions hatana).
"""))

cells.append(code("""
a = np.array([1, 2, 3])
print("a shape                    :", a.shape)
print("a[:, np.newaxis] shape     :", a[:, np.newaxis].shape)   # (3,1) -> column vector
print("a[np.newaxis, :] shape     :", a[np.newaxis, :].shape)   # (1,3) -> row vector
print("a[:, None] shape (same)    :", a[:, None].shape)          # None == np.newaxis

b = np.expand_dims(a, axis=0)
print("expand_dims(a, axis=0)     :", b.shape)   # (1,3)

c = np.squeeze(b)
print("squeeze(b)                 :", c.shape)   # (3,) -> size-1 dimensions hata di
"""))

cells.append(md("""
### `np.resize` vs `arr.resize()`

- `np.resize(arr, new_shape)` — **naya array** return karta hai; agar new size bara ho
  to original values **repeat/tile** kar deta hai (error nahi deta).
- `arr.resize(new_shape)` — **in-place** modify karta hai, `None` return karta hai
  (sirf tab kaam karta hai jab array apne data ka khud malik ho — koi view na ho).
"""))

cells.append(code("""
arr = np.array([1, 2, 3])
resized = np.resize(arr, (2, 4))   # naya array, values repeat/wrap ho jate hain
print("np.resize(arr,(2,4)):\\n", resized)

arr2 = np.array([1, 2, 3, 4])
ret_val = arr2.resize((2, 2))       # in-place -> None return karta hai
print("arr2.resize() ka return value:", ret_val)
print("arr2 ab in-place badal gaya :\\n", arr2)
"""))

# ============================================================
# 9. JOINING
# ============================================================
cells.append(md("""
## 8. Joining Arrays

**Kya hai:** Do ya zyada arrays ko jorr kar ek bara array banana.

**`np.concatenate(arrays, axis=...)`** — sab se general function; jorne wali dimension
ke ilawa **baqi saari dimensions match honi lazmi hain**, warna `ValueError`.
"""))

cells.append(code("""
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6]])
print("concatenate axis=0:\\n", np.concatenate([a, b], axis=0))   # rows jorna -> col count match hona chahiye

try:
    c = np.array([[5, 6, 7]])          # 3 columns -> a ke 2 columns se mismatch
    np.concatenate([a, c], axis=0)
except ValueError as e:
    print("ValueError:", e)
"""))

cells.append(md("""
### `vstack`/`hstack`/`dstack`/`column_stack`/`stack` — farq

`np.stack` **hamesha ek NAYA axis banata hai** — yeh `concatenate` se bara farq hai
(concatenate existing axis par jorta hai, stack ek dimension aur add karta hai).
"""))

cells.append(code("""
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])

print("vstack (rows jorta hai)      :\\n", np.vstack([x, y]), " shape:", np.vstack([x, y]).shape)
print("hstack (side-by-side jorta)  :", np.hstack([x, y]), " shape:", np.hstack([x, y]).shape)
print("dstack (3rd axis pe jorta)   : shape", np.dstack([x, y]).shape)
print("column_stack (columns bana) :\\n", np.column_stack([x, y]))
print("stack (NAYA axis, default=0):\\n", np.stack([x, y]), " shape:", np.stack([x, y]).shape)
print("stack axis=1                :\\n", np.stack([x, y], axis=1))
"""))

cells.append(md("""
**1D arrays par `vstack`/`hstack` ka behaviour:** 1D arrays ke liye `vstack` unhe pehle
row vectors bana kar phir stack karta hai (result 2D), jabke `hstack` unhe seedha
end-to-end jorr deta hai (result 1D rehta hai) — jaisa upar dikhaya.
"""))

# ============================================================
# 10. SPLITTING
# ============================================================
cells.append(md("""
## 9. Splitting Arrays

**`np.split(arr, n)`** — array ko **barabar** `n` hisso me todta hai; agar equal division
mumkin na ho to `ValueError` deta hai.

**`np.array_split(arr, n)`** — same kaam, lekin **unequal** division bhi allow karta hai
(kuch parts thore bare ho sakte hain).
"""))

cells.append(code("""
arr = np.arange(9)
print("split into 3 (equal):", [p.tolist() for p in np.split(arr, 3)])

try:
    np.split(arr, 4)    # 9 elements 4 barabar hisso me nahi ban sakte
except ValueError as e:
    print("ValueError:", e)

print("array_split into 4 (unequal ok):", [p.tolist() for p in np.array_split(arr, 4)])
"""))

cells.append(code("""
mat = np.arange(16).reshape(4, 4)
print("vsplit into 2 (rows ke hisaab se):")
for part in np.vsplit(mat, 2):
    print(part)

print()
print("hsplit into 2 (columns ke hisaab se):")
for part in np.hsplit(mat, 2):
    print(part)
"""))

# ============================================================
# 11. INSERT / DELETE / APPEND
# ============================================================
cells.append(md("""
## 10. `insert` / `delete` / `append`

**Kya hai:** Elements add/remove karne ke functions — Python list ke `insert`/`del`/
`append` jaise lagte hain, **lekin bohat mehnge hain**.

**Kyun mehenge:** NumPy arrays **fixed-size, contiguous memory blocks** hote hain. Har
`insert`/`delete`/`append` call **poora NAYA array allocate** karta hai aur saara data
copy karta hai — O(n) operation, har baar. Python list ka `.append()` amortized **O(1)**
hota hai (list extra capacity reserve karti hai) — NumPy arrays aisa nahi karte.

**Best practice:** loop me baar baar `np.append` mat karo — Python list me build karo,
aakhir me ek hi baar `np.array()` banao.
"""))

cells.append(code("""
arr = np.array([1, 2, 3, 4])
print("insert 99 at index 2:", np.insert(arr, 2, 99))
print("delete index 1      :", np.delete(arr, 1))
print("append [5, 6]       :", np.append(arr, [5, 6]))
print("original arr (unchanged, sab naye arrays hain):", arr)
"""))

# ============================================================
# 12. TILE vs REPEAT
# ============================================================
cells.append(md("""
## 11. `tile` vs `repeat`

**Farq:**
- `np.tile(arr, n)` — **poora array n baar repeat** karta hai (pattern jaisa: 1,2,3,1,2,3)
- `np.repeat(arr, n)` — **har element ko individually n baar** repeat karta hai
  (1,1,2,2,3,3)
"""))

cells.append(code("""
a = np.array([1, 2, 3])
print("tile(a, 2)        :", np.tile(a, 2))          # [1 2 3 1 2 3]
print("repeat(a, 2)      :", np.repeat(a, 2))         # [1 1 2 2 3 3]
print("tile(a, (2,1)):\\n", np.tile(a, (2, 1)))        # 2D tiling
print("repeat(a, [1,2,3]) :", np.repeat(a, [1, 2, 3]))  # per-element alag count
"""))

# ============================================================
# 13. FLIP / FLIPLR / FLIPUD / ROLL / ROT90
# ============================================================
cells.append(md("""
## 12. `flip` / `fliplr` / `flipud` / `roll` / `rot90`

- `np.flip(arr, axis=...)` — general reverse (koi bhi axis)
- `np.fliplr(mat)` — left-right flip (columns reverse) — sirf 2D+ arrays
- `np.flipud(mat)` — up-down flip (rows reverse)
- `np.roll(arr, shift)` — elements ko **circularly** shift karta hai (end se wrap around)
- `np.rot90(mat)` — 90 degrees counterclockwise rotate (default)
"""))

cells.append(code("""
mat = np.arange(1, 10).reshape(3, 3)
print("mat:\\n", mat)
print()
print("flip (dono axes)   :\\n", np.flip(mat))
print("flip axis=0 (rows) :\\n", np.flip(mat, axis=0))
print("fliplr             :\\n", np.fliplr(mat))
print("flipud             :\\n", np.flipud(mat))
print("roll(arange(5), 2) :", np.roll(np.arange(5), 2))
print("rot90 (90 deg ccw) :\\n", np.rot90(mat))
"""))

# ============================================================
# 14. SORTING
# ============================================================
cells.append(md("""
## 13. Sorting Basics

**`np.sort(arr)`** — **copy** return karta hai, original unchanged.
**`arr.sort()`** — **in-place** sort karta hai, `None` return karta hai.
**`np.argsort(arr)`** — sorted **indices** deta hai (values nahi) — jab pata karna ho ke
kaunsa element kahan jayega ya rank chahiye.
"""))

cells.append(code("""
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])
sorted_copy = np.sort(arr)      # copy
print("np.sort(arr) [copy]  :", sorted_copy)
print("arr (unchanged)      :", arr)

arr.sort()                       # in-place
print("arr.sort() ke baad arr:", arr)
"""))

cells.append(code("""
arr2 = np.array([30, 10, 40, 10, 50])
print("argsort indices:", np.argsort(arr2))     # values kahan se aayen sorted order me
print("sorted via argsort:", arr2[np.argsort(arr2)])

mat = np.array([[3, 1], [2, 4]])
print("sort axis=0 (per column):\\n", np.sort(mat, axis=0))
print("sort axis=1 (per row)   :\\n", np.sort(mat, axis=1))
print("sort axis=None (poora flatten karke):", np.sort(mat, axis=None))

# kind='stable' -> equal elements ki original relative order preserve rehti hai
print("argsort kind='stable':", np.argsort(arr2, kind='stable'))
"""))

# ============================================================
# 15. UNIQUE / ISIN
# ============================================================
cells.append(md("""
## 14. `np.unique` aur `np.isin`

**`np.unique(arr, return_index=, return_inverse=, return_counts=)`** — sorted unique
values, plus optionally: pehli occurrence ka index, har element ka "unique array me kis
index par hai" mapping (inverse), aur har unique value ka count.

**`np.isin(arr, test_values)`** — boolean mask deta hai ke `arr` ka har element
`test_values` me hai ya nahi.

> **NumPy 2.0 note:** Purana `np.in1d()` function **hata diya gaya hai** (removed) —
> sirf `np.isin()` use karo.
"""))

cells.append(code("""
arr = np.array([1, 2, 2, 3, 3, 3, 1])
vals, first_idx, inverse, counts = np.unique(
    arr, return_index=True, return_inverse=True, return_counts=True
)
print("unique values      :", vals)
print("first occurrence idx:", first_idx)
print("inverse mapping     :", inverse)   # arr = vals[inverse]
print("counts              :", counts)
print("sanity: vals[inverse] == arr ?", np.array_equal(vals[inverse], arr))
"""))

cells.append(code("""
# axis=0 -> unique ROWS (poore row ko ek unit maan kar)
mat = np.array([[1, 2], [3, 4], [1, 2]])
print("unique rows:\\n", np.unique(mat, axis=0))
"""))

cells.append(code("""
print("np.isin(arr, [2,3]):", np.isin(arr, [2, 3]))

# np.in1d NumPy 2.0 me REMOVE ho chuka hai -> AttributeError aayega
try:
    np.in1d(arr, [2, 3])
except AttributeError as e:
    print("AttributeError (as expected, np.in1d removed in NumPy 2.0):", e)
"""))

# ============================================================
# 16. COMMON MISTAKES / GOTCHAS SUMMARY
# ============================================================
cells.append(md("""
## Common Mistakes / Gotchas — Summary

1. **View ko modify karna soch kar "yeh naya array hai"** — basic slicing view deti hai;
   original bhi badal jata hai. Safe rehne ke liye `.copy()` use karo.
2. **`and`/`or` numpy boolean arrays par** — `ValueError: truth value ... ambiguous`;
   `&`/`|`/`~` use karo, **brackets ke sath**.
3. **`arr[i][j]` chained indexing** — kaam karta hai lekin `arr[i, j]` behtar/fast hai.
4. **Boolean mask ki length array se match na hona** — `IndexError`.
5. **`arr[[0,2],[1,3]]` se "2x2 sub-matrix" expect karna** — yeh sirf 2 pairwise
   elements deta hai; sub-matrix ke liye `np.ix_` chahiye.
6. **`reshape` me total elements match na karna** — `ValueError`.
7. **`flatten` ko view samajhna** — hamesha copy hota hai (safe, thora slower);
   `ravel` view de sakta hai (fast, lekin original share hota hai).
8. **Loop me baar baar `np.append`/`np.insert`** — har baar poora naya array banta hai,
   O(n) per call — bohat slow bade loops me. Python list use karo, aakhir me convert karo.
9. **`np.split` equal division ke baghair** — `ValueError`; unequal ke liye
   `np.array_split`.
10. **`np.in1d` NumPy 2.0 me removed** — `np.isin` use karo.
"""))

# ============================================================
# 17. REAL-WORLD PROBLEMS
# ============================================================
cells.append(md("""
## Real-World Problems

### Problem 1: Image crop aur horizontal flip (synthetic image)

Ek synthetic image (Height, Width, Channels) banate hain aur ek region crop karke usay
horizontally flip karte hain — bilkul jaisa image-augmentation pipelines me hota hai.
"""))

cells.append(code("""
rng_img = np.random.default_rng(1)
image = rng_img.integers(0, 256, size=(8, 8, 3), dtype=np.uint8)   # 8x8 RGB "image"

cropped = image[2:6, 2:6, :]        # 4x4 region crop -> yeh VIEW hai
flipped = cropped[:, ::-1, :]        # horizontal flip (columns reverse) -> yeh bhi VIEW hai

print("original shape:", image.shape)
print("cropped shape :", cropped.shape)
print("flipped shape :", flipped.shape)
print("cropped view of original?", np.shares_memory(image, cropped))
"""))

cells.append(md("""
### Problem 2: Dataset se outlier rows filter karna (boolean mask)

Kisi score column me se sirf "reasonable range" wale values rakhne hain — boolean
masking se ek line me ho jata hai.
"""))

cells.append(code("""
rng_data = np.random.default_rng(2)
scores = rng_data.normal(50, 10, size=20).round(1)   # normal distribution ke fake scores

mask = (scores > 30) & (scores < 70)      # sirf reasonable range
clean_scores = scores[mask]

print("total scores:", scores.size, " | after outlier filter:", clean_scores.size)
print("removed (outliers):", scores[~mask])
"""))

cells.append(md("""
### Problem 3: Batches banana `reshape` se (ML training loops ke liye common)

Flat samples ka array le kar fixed-size batches me todna.
"""))

cells.append(code("""
samples = np.arange(24)             # 24 total samples (imagine: dataset indices)
batch_size = 6
batches = samples.reshape(-1, batch_size)   # -1 -> NumPy khud batch count nikal lega

print("batches shape:", batches.shape)   # (4, 6) -> 4 batches of 6
for i, batch in enumerate(batches):
    print(f"batch {i}:", batch)
"""))

cells.append(md("""
### Problem 4: Specific feature columns select karna (fancy indexing)

Ek dataset (rows=samples, cols=features) me se sirf kuch chuni hui feature columns
nikalna — ML feature-selection ka basic step.
"""))

cells.append(code("""
rng_feat = np.random.default_rng(3)
dataset = rng_feat.integers(0, 100, size=(5, 6))   # 5 samples, 6 features
print("full dataset:\\n", dataset)

feature_idx = [0, 2, 4]   # sirf yeh 3 features chahiye
selected_features = dataset[:, feature_idx]
print("selected features (cols 0,2,4):\\n", selected_features)
"""))

cells.append(md("""
### Problem 5: Train/Validation split (contiguous slicing)

Simple, non-random split — pehle 80% train, baaki 20% validation.
"""))

cells.append(code("""
n_total = 100
all_data = np.arange(n_total)

split_point = int(n_total * 0.8)
train, val = all_data[:split_point], all_data[split_point:]

print("train size:", train.shape[0], " | val size:", val.shape[0])
print("train ek VIEW hai original ka?", np.shares_memory(all_data, train))
"""))

# ============================================================
# 18. LEETCODE PROBLEMS
# ============================================================
cells.append(md("""
## LeetCode Problems

Har problem ke **do solutions**: (a) pure Python (interview-acceptable) aur
(b) NumPy/vectorized (real data-work/production ke liye). **Interview me generally pure
Python expect hota hai** (interviewer array-manipulation logic dekhna chahta hai,
library ka use nahi) — NumPy version data-science/production context ke liye faida-mand
hai.
"""))

# ---- LC 48 ----
cells.append(md("""
### LC 48. Rotate Image — Medium

<https://leetcode.com/problems/rotate-image/>

**Bayan:** Ek `n x n` matrix diya hai — usay **90 degrees clockwise in-place** rotate
karna hai (naya matrix return nahi karna, original list-of-lists ko hi modify karna hai).

**Approach:**
1. Matrix ko **transpose** karo (rows <-> columns swap, in-place).
2. Har row ko **reverse** kar do.
3. Transpose + row-reverse = 90-degree clockwise rotation.

**Time complexity:** O(n²) — har element ek baar touch hota hai.
**Space complexity:** O(1) extra (in-place, matrix ke andar hi swap).
"""))

cells.append(code("""
def rotate(matrix):
    \"\"\"LeetCode 48 -- in-place 90-degree clockwise rotation (pure Python).\"\"\"
    n = len(matrix)
    # Step 1: transpose in-place (upper triangle ke elements swap karo)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Step 2: har row reverse karo
    for row in matrix:
        row.reverse()
    return matrix


m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotate(m1)
assert m1 == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
print("rotate() pure python OK:", m1)
"""))

cells.append(code("""
def rotate_np(matrix):
    \"\"\"LeetCode 48 -- NumPy version. LeetCode list-of-lists ko IN-PLACE chahiye,
    isliye rotated result wapis original rows me likhte hain.\"\"\"
    arr = np.array(matrix)
    rotated = np.rot90(arr, -1).copy()   # k=-1 -> clockwise; .copy() zaroori hai (warna view aliasing)
    for i in range(len(matrix)):
        matrix[i][:] = rotated[i].tolist()   # row ko IN-PLACE update karo (naya list object mat banao)
    return matrix


m2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotate_np(m2)
assert m2 == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
print("rotate_np() OK:", m2)

# Agar data already NumPy array ho (list nahi), to seedha true in-place tareeqa:
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
arr[:] = np.rot90(arr, -1).copy()   # copy() zaroori: rot90 khud arr ka view hai, .copy() na ho to aliasing bug aayega
print("direct numpy in-place rotate:\\n", arr)
"""))

# ---- LC 54 ----
cells.append(md("""
### LC 54. Spiral Matrix — Medium

<https://leetcode.com/problems/spiral-matrix/>

**Bayan:** Matrix ke elements ko **spiral order** me (bahar se andar, clockwise) return
karna hai.

**Approach (pure Python):** 4 boundaries maintain karo (top, bottom, left, right).
Top row left-to-right traverse karo, top++; right column top-to-bottom, right--; agar
top<=bottom to bottom row right-to-left, bottom--; agar left<=right to left column
bottom-to-top, left++. Repeat jab tak boundaries cross na ho jayein.

**Approach (NumPy trick):** Har iteration me **pehli row le lo**, phir **baaki matrix ko
90 degrees rotate** kar do — agli "pehli row" khud-ba-khud agla spiral segment ban jati
hai. Bohat elegant vectorized trick.

**Time complexity:** O(m*n) dono approaches me (har element ek baar visit hota hai).
**Space complexity:** O(1) extra (pure Python, output ke ilawa); NumPy version me har
rotation ek naya array banati hai (O(m*n) total extra, kyunke chhote-chhote copies).
"""))

cells.append(code("""
def spiralOrder(matrix):
    \"\"\"LeetCode 54 -- pure Python, boundary-shrinking approach.\"\"\"
    if not matrix or not matrix[0]:
        return []
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for c in range(left, right + 1):          # top row: left -> right
            result.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):           # right col: top -> bottom
            result.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):   # bottom row: right -> left
                result.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):   # left col: bottom -> top
                result.append(matrix[r][left])
            left += 1
    return result


m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
assert spiralOrder(m) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
m2 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
assert spiralOrder(m2) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
print("spiralOrder() pure python OK")
"""))

cells.append(code("""
def spiralOrder_np(matrix):
    \"\"\"LeetCode 54 -- NumPy vectorized trick: pehli row lo, baaki ko rotate karo, repeat.\"\"\"
    arr = np.array(matrix)
    result = []
    while arr.size:
        result.extend(arr[0].tolist())    # current "top row" spiral order me add karo
        arr = np.rot90(arr[1:], 1)         # baaki matrix ko 90 deg (ccw, numpy default) rotate karo
    return result


assert spiralOrder_np(m) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
assert spiralOrder_np(m2) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
print("spiralOrder_np() OK:", spiralOrder_np(m))
"""))

# ---- LC 867 ----
cells.append(md("""
### LC 867. Transpose Matrix — Easy

<https://leetcode.com/problems/transpose-matrix/>

**Bayan:** Matrix ka **transpose** return karo — `result[j][i] = matrix[i][j]`
(rows aur columns swap).

**Approach:** Naya `cols x rows` shape ka result matrix banao, har element ko uski
transposed position par copy karo.

**Time complexity:** O(m*n). **Space complexity:** O(m*n) (naya output matrix).
"""))

cells.append(code("""
def transpose(matrix):
    \"\"\"LeetCode 867 -- pure Python transpose.\"\"\"
    rows, cols = len(matrix), len(matrix[0])
    result = [[0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result


m = [[1, 2, 3], [4, 5, 6]]
assert transpose(m) == [[1, 4], [2, 5], [3, 6]]
print("transpose() pure python OK:", transpose(m))
"""))

cells.append(code("""
def transpose_np(matrix):
    \"\"\"LeetCode 867 -- NumPy: .T attribute seedha transpose deta hai (view, phir list bana do).\"\"\"
    return np.array(matrix).T.tolist()


assert transpose_np(m) == [[1, 4], [2, 5], [3, 6]]
print("transpose_np() OK:", transpose_np(m))
"""))

# ---- LC 832 ----
cells.append(md("""
### LC 832. Flipping an Image — Easy

<https://leetcode.com/problems/flipping-an-image/>

**Bayan:** Binary image (0/1) ka har row **horizontally flip** karo, phir har bit
**invert** karo (0->1, 1->0).

**Approach:** Row ko reverse karo, phir har element `1 - x` kar do.

**Time complexity:** O(m*n). **Space complexity:** O(m*n) output ke liye.
"""))

cells.append(code("""
def flipAndInvertImage(image):
    \"\"\"LeetCode 832 -- pure Python: reverse row, phir invert.\"\"\"
    result = []
    for row in image:
        result.append([1 - x for x in reversed(row)])
    return result


img = [[1, 1, 0], [1, 0, 1], [0, 0, 0]]
assert flipAndInvertImage(img) == [[1, 0, 0], [0, 1, 0], [1, 1, 1]]
print("flipAndInvertImage() pure python OK:", flipAndInvertImage(img))
"""))

cells.append(code("""
def flipAndInvertImage_np(image):
    \"\"\"LeetCode 832 -- NumPy: fliplr (horizontal flip) + 1 - arr (invert).\"\"\"
    arr = np.array(image)
    flipped = np.fliplr(arr)
    inverted = 1 - flipped
    return inverted.tolist()


assert flipAndInvertImage_np(img) == [[1, 0, 0], [0, 1, 0], [1, 1, 1]]
print("flipAndInvertImage_np() OK:", flipAndInvertImage_np(img))
"""))

# ---- LC 566 ----
cells.append(md("""
### LC 566. Reshape the Matrix — Easy

<https://leetcode.com/problems/reshape-the-matrix/>

**Bayan:** `m x n` matrix ko `r x c` shape me reshape karo (row-major order flatten karke
phir refill karo). Agar total elements match na karein (`m*n != r*c`), **original matrix
wapis** return karo.

**Approach:** Matrix ko flatten karo, phir `r` rows me `c`-`c` elements bhar do.

**Time complexity:** O(m*n). **Space complexity:** O(m*n) output ke liye.
"""))

cells.append(code("""
def matrixReshape(mat, r, c):
    \"\"\"LeetCode 566 -- pure Python.\"\"\"
    m, n = len(mat), len(mat[0])
    if m * n != r * c:            # size match na ho to original wapis
        return mat
    flat = [x for row in mat for x in row]
    return [flat[i * c:(i + 1) * c] for i in range(r)]


mat = [[1, 2], [3, 4]]
assert matrixReshape(mat, 1, 4) == [[1, 2, 3, 4]]
assert matrixReshape(mat, 2, 4) == [[1, 2], [3, 4]]   # size mismatch -> original
print("matrixReshape() pure python OK")
"""))

cells.append(code("""
def matrixReshape_np(mat, r, c):
    \"\"\"LeetCode 566 -- NumPy: .size check + reshape.\"\"\"
    arr = np.array(mat)
    if arr.size != r * c:
        return mat                 # size match na ho to original wapis (NumPy khud ValueError dega warna)
    return arr.reshape(r, c).tolist()


assert matrixReshape_np(mat, 1, 4) == [[1, 2, 3, 4]]
assert matrixReshape_np(mat, 2, 4) == [[1, 2], [3, 4]]
print("matrixReshape_np() OK")
"""))

# ============================================================
# 19. INTERVIEW QUESTIONS & ANSWERS
# ============================================================
cells.append(md("""
## Interview Questions & Answers

**Q1. View aur copy me farq? Kaise pata karein ke kya mila?**
A. View original ke sath memory share karta hai (modify karne se dono badalte hain);
copy independent hota hai. `np.shares_memory(a, b)`, `a.base`, `a.flags['OWNDATA']` se
check karo.

**Q2. `ravel()` aur `flatten()` me farq?**
A. `ravel()` view deta hai jab possible ho (fast); `flatten()` hamesha copy deta hai
(safe, thora slower).

**Q3. `reshape` aur `resize` me farq?**
A. `arr.reshape()` naya view/array deta hai, total size same rehni chahiye.
`np.resize()` naya array deta hai jo size bara/chhota kar sakta hai (repeat/truncate
karta hai). `arr.resize()` (method) in-place modify karta hai, `None` return karta hai.

**Q4. Fancy indexing aur boolean indexing me farq?**
A. Fancy = integer array/list se index (specific positions, repeat allowed, custom
order). Boolean = mask se index (True/False condition based). **Dono copy dete hain**,
view nahi.

**Q5. `arr[i, j]` `arr[i][j]` se behtar kyun?**
A. `arr[i, j]` ek hi indexing operation me seedha element tak pohanchta hai; `arr[i][j]`
pehle ek intermediate array/view banata hai phir usay index karta hai — extra overhead
aur chained-assignment ke edge cases ka risk.

**Q6. Slicing view kyun deti hai, fancy indexing copy kyun?**
A. Slicing ek predictable, regular (constant stride) pattern hai — sirf metadata
(offset/stride/shape) se describe ho sakta hai, isliye view mumkin hai. Fancy/boolean
indexing arbitrary/irregular positions select karta hai jo simple stride se describe
nahi ho saktin — isliye actual naya memory block (copy) banana zaroori hai.

**Q7. `stack` aur `concatenate` me farq?**
A. `concatenate` existing axis par jorta hai (dimensions count same rehti hai).
`stack` ek **naya axis** add karta hai (result ki dimensionality ek zyada ho jati hai).

**Q8. `tile` aur `repeat` me farq?**
A. `tile` poora array/pattern repeat karta hai (`[1,2,1,2]`). `repeat` har element ko
individually repeat karta hai (`[1,1,2,2]`).

**Q9. Contiguity kya hai, kab matter karti hai?**
A. Array memory me kaisi layout me hai — C-contiguous (row-major) ya F-contiguous
(column-major). Kuch operations (jaise `ravel()` ka view-vs-copy decision, ya low-level
C/Fortran libraries ke sath interfacing) contiguity par depend karti hain.

**Q10. `and`/`or` NumPy boolean arrays par kyun fail karte hain?**
A. Yeh Python-level operators hain jo `bool()` conversion maangte hain; multi-element
array ka `bool()` ambiguous hai (`ValueError`). `&`/`|`/`~` (elementwise, NumPy-level)
use karo, saath brackets (operator precedence ki wajah se).

**Q11. `np.where(condition)` (1-arg) kya deta hai?**
A. Matching indices (tuple of arrays, per-dimension) — values nahi. 3-arg form
`np.where(cond, x, y)` values choose karta hai (`cond` True to `x`, warna `y`).

**Q12. Ellipsis (`...`) kya karta hai?**
A. "Baaki jitni bhi dimensions hain, unhe `:` samjho" — variable-dimension code likhne
me useful (jaise image ke last channel-axis ko access karna chahe image 3D ho ya batched
4D).

**Q13. `np.ix_` kis liye hai?**
A. Rows aur columns dono ki list de kar unka **cross-product (open mesh)** sub-matrix
nikalne ke liye — `arr[[0,2],[1,3]]` (pairwise) se alag, yeh true rows x cols
sub-selection deta hai.

**Q14. `np.split` aur `np.array_split` me farq?**
A. `split` sirf equal division allow karta hai (warna `ValueError`). `array_split`
unequal division bhi allow karta hai (chunks thore alag size ke ho sakte hain).

**Q15. `insert`/`delete`/`append` list operations ke muqable expensive kyun hain?**
A. NumPy arrays fixed-size contiguous buffers hain — har insert/delete/append call
**pura naya array allocate + copy** karta hai (O(n)). Python list `.append()` amortized
O(1) hai kyunke extra capacity reserve karti hai.

**Q16. `np.unique(..., axis=0)` kya karta hai?**
A. Poore **row** ko ek unit maan kar unique rows dhoondta hai (element-wise nahi,
row-wise uniqueness).

**Q17. `np.in1d` ka kya hua NumPy 2.0 me?**
A. Remove kar diya gaya — `AttributeError` deta hai. Sirf `np.isin()` use karo.

**Q18. Boolean mask ki length array se match na ho to kya hota hai?**
A. `IndexError` — NumPy silently wrong result nahi deta, turant fail ho jata hai (bug
jaldi pakra jata hai).
"""))

# ============================================================
# 20. PRACTICE EXERCISES
# ============================================================
cells.append(md("""
## Practice Exercises (khud karo)

1. Ek 1D array `np.arange(20)` se index 1 se shuru karke har 3rd element nikalo
   (slicing use karo). *Hint:* `arr[1::3]`.
2. `arr[3:8]` view hai ya copy — `np.shares_memory` se prove karo.
3. Ek 2D array me se sirf woh rows nikalo jinke pehle column ki value 50 se zyada ho
   (boolean masking). *Hint:* `arr[arr[:, 0] > 50]`.
4. Fancy indexing use kar ke ek matrix ki rows ko **reverse order** me reorder karo
   (bina `flip` use kiye). *Hint:* `mat[::-1]` ya `mat[[2,1,0]]`.
5. `np.tile` aur `np.repeat` dono use kar ke `[1,2]` se `[1,2,1,2,1,1,2,2]` jaisa kuch
   banane ki koshish karo — farq mehsoos karo.
6. `np.arange(24)` ko `(2,3,4)` shape me reshape karo, phir `.transpose(2,0,1)` laga kar
   naya shape print karo — samjho axes order kaise badla.
7. `np.ix_` use kar ke ek 5x5 matrix se rows `[0,2,4]` aur cols `[1,3]` ka sub-matrix
   nikalo.
8. `np.array_split` use kar ke 17 elements wale array ko 4 hisso me todo, har hisse ka
   size print karo (barabar nahi hoga — dekho kaise distribute hota hai).
9. `np.unique` ka `return_counts=True` use kar ke ek array me sab se zyada frequent
   value dhoondo (*hint:* `counts.argmax()`).
"""))

# ============================================================
# 21. SUMMARY / CHEAT-SHEET
# ============================================================
cells.append(md("""
## Summary / Cheat-sheet

| Operation | View ya Copy? |
|---|---|
| Basic slicing (`arr[1:4]`, `arr[:, 0]`) | **View** |
| `reshape()` (jab memory-compatible ho) | **View** |
| `ravel()` (jab contiguous ho) | **View** |
| `.T` / `transpose()` / `swapaxes()` | **View** |
| Fancy indexing (`arr[[0,2,4]]`) | **Copy** |
| Boolean/mask indexing (`arr[mask]`) | **Copy** |
| `.flatten()` | **Copy** (hamesha) |
| `.copy()` | **Copy** (explicit, hamesha) |
| Arithmetic (`arr + 1`) | **Copy** (naya array) |
| `np.concatenate`/`stack`/`vstack`/etc. | **Copy** (naya array) |

### Quick reference

- **Check view/copy:** `np.shares_memory(a, b)`, `a.base`, `a.flags['OWNDATA']`
- **`&`/`|`/`~` with brackets** — `and`/`or`/`not` NumPy arrays par mat use karo
- **`arr[i, j]` > `arr[i][j]`** — ek hi step, zyada fast, safer
- **`np.ix_`** — true rows x cols sub-matrix ke liye (fancy indexing pairwise hoti hai)
- **`stack` = naya axis, `concatenate` = existing axis par jorna**
- **`tile` = poora pattern repeat, `repeat` = per-element repeat**
- **`np.sort()` copy, `arr.sort()` in-place**
- **`np.split` equal-only, `np.array_split` unequal bhi ok**
- **`np.in1d` NumPy 2.0 me removed — `np.isin` use karo**
- Loop me baar baar `insert`/`append` mat karo — list me build karo, aakhir me
  `np.array()` banao.
"""))

save(r"Numpy/Basics/02_Indexing_Slicing_Reshaping_and_Joining.ipynb", cells)
