"""Generator: Numpy/Basics/01_Numpy_Introduction_Arrays_aur_Creation.ipynb

Chalao (ROOT se):  python _tools/gen/np_basics_01_intro.py
"""

import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

CELLS: list = []
A = CELLS.append

A(md("""
# NumPy 01 — Introduction, Arrays aur Creation

**Level:** Zero se shuru (Basics) | **Library:** NumPy 2.x | **Python:** 3.14

NumPy poore Python data-science stack ki **buniyad** hai. Pandas, scikit-learn,
PyTorch, TensorFlow, OpenCV — sab andar se `ndarray` (ya usi jaisa memory layout)
istemal karte hain. Yaani NumPy samajh liya to aage ka safar aasan.

## Is notebook me kya seekhenge

- NumPy kya hai aur data science / ML me kyun **buniyadi** hai
- Python `list` vs `ndarray` — **speed** benchmark, **memory** comparison, type homogeneity
- Import convention aur version check
- `np.array()` se 1D / 2D / 3D arrays banana (nested lists)
- Array attributes: `ndim`, `shape`, `size`, `dtype`, `itemsize`, `nbytes`, `T`, `flags`, `strides`
- **dtypes** poori tafseel: `int8..int64`, `uint`, `float16/32/64`, `bool`, `complex`, string, object
- **Integer overflow** ka demo aur **casting** (`astype`, safe vs unsafe)
- Creation functions: `zeros`, `ones`, `full`, `empty`, `*_like`, `eye`, `identity`, `diag`
- `arange` (float step ka masla), `linspace`, `logspace`, `geomspace`
- `np.random` — modern `default_rng` (integers, random, normal, choice, shuffle) + seed reproducibility
- `fromfunction`, `fromiter`, `meshgrid` intro
- `np.array` vs `np.asarray` (copy vs no-copy) + NumPy 2 ka `copy=False` gotcha
- Scalars vs 0-d arrays
- `np.inf` / `np.nan` aur unke ajeeb rules (`nan != nan`)
- Printing options (`np.set_printoptions`)
- **LeetCode Problems**, **Interview Q&A**, **Practice Exercises**, **Cheat-sheet**

## Prerequisites

- Python basics: variables, `list`, `for` loop, function, f-string
- Bas itna hi. NumPy ka koi tajurba zaroori nahi.
"""))

# ---------------------------------------------------------------- section 1
A(md("""
## 1. NumPy kya hai?

**Kya hai:** NumPy (Numerical Python) ek library hai jo **N-dimensional array**
(`ndarray`) deti hai — ek aisa container jisme **ek hi dtype** ke numbers
**contiguous memory** (yaani ek hi laga tar block) me rakhe jate hain, aur unke
upar operations **C/Fortran ki compiled speed** se chalte hain.

**Kyun / kahan use hota hai:**

| Jagah | NumPy ka role |
|---|---|
| Data science | Pandas ka har column andar se numpy array hai |
| Machine Learning | Feature matrix `X` (n_samples × n_features) = 2D array |
| Deep Learning | Tensors = ndarray ka GPU-wala cousin; `torch.from_numpy` roz chalta hai |
| Image processing | Image = 3D array `(height, width, channels)` |
| Signal / audio | 1D array of samples |
| Statistics | mean/std/percentile sab vectorized |

**Teen bunyadi wajah NumPy kyun:**

1. **Speed** — loop Python me nahi, C me chalta hai (vectorization).
2. **Memory** — 1 million int64 = 8 MB. Python list of ints? ~40 MB+.
3. **Expressiveness** — `(X - X.mean(0)) / X.std(0)` — ek line me poora
   standardization. Loop likhne ki zaroorat nahi.

**Interview tip:** "NumPy kyun fast hai?" ka jawab **3 lafz** me:
*contiguous memory + fixed dtype + C-level loops (vectorization)*.
"""))

A(code("""
# NumPy ka standard import convention — poori dunya "np" likhti hai, tum bhi wahi likho
import numpy as np
import sys

# Version check — NumPy 2.x me kuch cheezein badal gayi hain (aage dekhenge)
print("NumPy version :", np.__version__)
print("Python version:", sys.version.split()[0])

# ndarray ka type kya hai?
a = np.array([1, 2, 3])
print("type(a)       :", type(a))     # <class 'numpy.ndarray'>
print("a             :", a)
"""))

A(md("""
### Output ka matlab

- `np.array([1, 2, 3])` ne ek `ndarray` object banaya.
- Print karte waqt commas **nahi** dikhte (`[1 2 3]`) — list `[1, 2, 3]` print hoti hai.
  Ye pehli nazar me pehchanne ka aasan tareeqa hai ke cheez list hai ya array.

**Gotcha:** `import numpy as np` ke bajaye `from numpy import *` **kabhi na karo** —
`sum`, `min`, `max`, `abs`, `round` jaise builtins overwrite ho jate hain aur baad me
ajeeb bugs aate hain.
"""))

# ---------------------------------------------------------------- section 2
A(md("""
## 2. Python list vs ndarray

### 2.1 Speed — asli farq

**Kya hai:** Python list par loop chalao to har element ek **PyObject** hai; har
addition me pointer dereference, type check, aur naya object banta hai. NumPy me
data ek raw memory block me hai aur loop C me chalta hai — koi per-element Python
overhead nahi.

Chalo naap kar dekhte hain (`timeit` se).
"""))

A(code("""
import timeit

N = 100_000
py_list = list(range(N))            # Python list
np_arr = np.arange(N)               # NumPy array (same data)

# Har element ko double karna — dono tareeqon se
t_list = timeit.timeit("[x * 2 for x in py_list]", globals=globals(), number=20)
t_np = timeit.timeit("np_arr * 2", globals=globals(), number=20)

print(f"list comprehension : {t_list:.4f} sec (20 baar)")
print(f"numpy vectorized   : {t_np:.4f} sec (20 baar)")
print(f"NumPy taqreeban    : {t_list / t_np:.1f}x tez")

# NOTE: exact number machine par badalta rehta hai — sirf ratio ka andaza lo.
# Isi wajah se hum timing par 'assert' NAHI lagate.
"""))

A(code("""
# Sum ka muqabla — builtin sum(list) vs arr.sum()
t_sum_list = timeit.timeit("sum(py_list)", globals=globals(), number=20)
t_sum_np = timeit.timeit("np_arr.sum()", globals=globals(), number=20)

print(f"sum(py_list) : {t_sum_list:.4f} sec")
print(f"np_arr.sum() : {t_sum_np:.4f} sec")
print(f"speedup      : {t_sum_list / t_sum_np:.1f}x")

# GOTCHA: builtin sum(numpy_array) SLOW hota hai — wo numpy ke fast path ko bypass
# kar ke element-by-element Python loop chalata hai. Hamesha arr.sum() likho.
t_bad = timeit.timeit("sum(np_arr)", globals=globals(), number=5)
print(f"\\nsum(np_arr)  : {t_bad:.4f} sec (5 baar) <-- ye GALAT tareeqa hai")
"""))

A(md("""
### 2.2 Memory — ndarray kitni jagah bachata hai

**Kya hai:** Python `int` ek object hai (~28 bytes) aur list sirf **pointers** (8 bytes
each) rakhti hai. Yaani list of 1000 ints = 1000 pointers + 1000 int objects.
NumPy `int64` array me sirf **8 bytes per number**, bas.

**Do tools:**
- `arr.nbytes` → array ke **data** ka size (deterministic, reliable)
- `sys.getsizeof(obj)` → Python object ka size (shallow — nested objects count nahi hote)
"""))

A(code("""
n = 1000
lst = list(range(n))
arr64 = np.arange(n, dtype=np.int64)
arr8 = np.arange(n, dtype=np.int8)     # 0..127 tak hi safe, magar demo ke liye theek

# List ka ASLI footprint = list ka apna size + har int object ka size
list_shallow = sys.getsizeof(lst)
list_deep = list_shallow + sum(sys.getsizeof(x) for x in lst)

print(f"list shallow (sirf pointers) : {list_shallow:>8,} bytes")
print(f"list deep    (+ int objects) : {list_deep:>8,} bytes")
print(f"ndarray int64 .nbytes        : {arr64.nbytes:>8,} bytes")
print(f"ndarray int8  .nbytes        : {arr8.nbytes:>8,} bytes")
print(f"getsizeof(ndarray int64)     : {sys.getsizeof(arr64):>8,} bytes  (data + ~112 byte header)")
print(f"\\nBachat (list deep / int64)   : {list_deep / arr64.nbytes:.1f}x")

# nbytes ka formula deterministic hai -> assert kar sakte hain
assert arr64.nbytes == n * 8       # 1000 numbers x 8 bytes
assert arr8.nbytes == n * 1        # 1000 numbers x 1 byte
"""))

A(md("""
**Memory footprint ka formula (interview me poocha jata hai):**

```
nbytes = size * itemsize = (shape ke sab dimensions ka product) * (dtype ke bytes)
```

Misaal: 1000×1000 ka `float64` matrix → `1_000_000 * 8 = 8 MB`.
Agar `float32` kar do → **4 MB** (aadha). ML me yehi trick memory bachane ke liye
use hoti hai (aur GPU par speed bhi barhti hai).
"""))

A(code("""
# Practical: ek ML feature matrix ka memory budget
rows, cols = 1_000_000, 20

for dt in (np.float64, np.float32, np.float16, np.int8):
    # nbytes calculate karne ke liye poora array banane ki zaroorat NAHI
    itemsize = np.dtype(dt).itemsize            # dtype ka per-element size
    total_mb = rows * cols * itemsize / 1024**2  # bytes -> MB
    print(f"{np.dtype(dt).name:>8} : itemsize={itemsize} byte -> {total_mb:8.1f} MB")

print("\\nSabaq: dtype chhota karne se memory seedha proportionally kam hoti hai.")
"""))

A(md("""
### 2.3 Type homogeneity — ndarray ek hi dtype rakhta hai

**Kya hai:** List me kuch bhi mila-jula rakh sakte ho (`[1, "a", None]`). ndarray
me **sab elements ka ek hi dtype** hota hai. Agar mila-jula do to NumPy sab ko ek
common type par **upcast** kar deta hai (ya `object` dtype par gir jata hai).

**Kyun:** Yehi homogeneity fast C loops ko mumkin banati hai.
"""))

A(code("""
# int + float mila do -> sab float64 ban jate hain
print(np.array([1, 2, 3.5]), "->", np.array([1, 2, 3.5]).dtype)

# int + bool -> bool ko 0/1 samjha jata hai
print(np.array([True, 2, 3]), "->", np.array([True, 2, 3]).dtype)

# number + string -> sab STRING ban jate hain (ye chupa hua bug ban sakta hai!)
mixed = np.array([1, 2, "hello"])
print(mixed, "->", mixed.dtype)      # '<U21' = unicode, max 21 chars
print("Ab '1' number nahi, string hai:", repr(mixed[0]))

# Zabardasti mila-jula rakhna ho to dtype=object (magar speed khatam ho jati hai)
obj = np.array([1, "a", None, [1, 2]], dtype=object)
print("\\nobject dtype:", obj, "->", obj.dtype)
print("Yahan har element phir se PyObject hai -> NumPy ka speed faida GAYAB.")
"""))

# ---------------------------------------------------------------- section 3
A(md("""
## 3. `np.array()` — 1D, 2D, 3D banane ka tareeqa

**Syntax:** `np.array(object, dtype=None, copy=True, ndmin=0)`

- 1D = numbers ki simple list → **vector**
- 2D = list of lists → **matrix** (rows × cols)
- 3D = list of list of lists → **tensor** (jaise images ka batch)

**Mental model:** shape tuple ko **bahar se andar** parho.
`(2, 3, 4)` = 2 blocks, har block me 3 rows, har row me 4 numbers.
"""))

A(code("""
# 1D — vector
v = np.array([10, 20, 30, 40])
print("1D:", v, "| shape:", v.shape, "| ndim:", v.ndim)

# 2D — matrix (2 rows x 3 cols). Har inner list ek ROW hai.
m = np.array([[1, 2, 3],
              [4, 5, 6]])
print("\\n2D:\\n", m, "\\nshape:", m.shape, "| ndim:", m.ndim)

# 3D — 2 blocks, har block 2x3
t = np.array([[[1, 2, 3], [4, 5, 6]],
              [[7, 8, 9], [10, 11, 12]]])
print("\\n3D:\\n", t)
print("shape:", t.shape, "| ndim:", t.ndim, "| size:", t.size)
"""))

A(code("""
# dtype khud choose kar sakte ho
print(np.array([1, 2, 3], dtype=np.float32))     # [1. 2. 3.]
print(np.array([1.9, 2.9], dtype=np.int32))      # [1 2]  <- TRUNCATE hota hai, round NAHI!

# ndmin= se minimum dimensions force karo (kabhi kabhi useful)
print("\\nndmin=2 :", np.array([1, 2, 3], ndmin=2), "shape:", np.array([1, 2, 3], ndmin=2).shape)
"""))

A(md("""
### Gotcha: ragged (be-tarteeb) nested list

Agar inner lists ki lambai **barabar nahi** hai to NumPy rectangular array nahi bana
sakta. NumPy 1.x me ye warning ke sath `object` array banta tha; **NumPy 2.x me
seedha `ValueError` aata hai.** Ye acchi baat hai — bug chup ke nahi guzarta.
"""))

A(code("""
# Jaan boojh kar error — isliye try/except me
try:
    bad = np.array([[1, 2, 3], [4, 5]])      # rows ki lambai different
    print("bana gaya:", bad)
except ValueError as e:
    print("ValueError:", e)

# Hal 1: khud object dtype maango (agar waqai zaroorat ho)
ok = np.array([[1, 2, 3], [4, 5]], dtype=object)
print("\\ndtype=object se chal gaya:", ok, "->", ok.dtype)

# Hal 2 (behtar): data ko padding se rectangular banao
padded = np.array([[1, 2, 3], [4, 5, 0]])
print("padded:\\n", padded)
"""))

# ---------------------------------------------------------------- section 4
A(md("""
## 4. Array attributes — array ka "ID card"

| Attribute | Kya batata hai |
|---|---|
| `ndim` | kitne dimensions (axes) |
| `shape` | har dimension ki lambai (tuple) |
| `size` | total elements = shape ka product |
| `dtype` | elements ka data type |
| `itemsize` | ek element ke bytes |
| `nbytes` | poore data ke bytes (`size * itemsize`) |
| `T` | transpose (axes ulat gaye) |
| `flags` | memory layout info (C/F contiguous, OWNDATA, WRITEABLE) |
| `strides` | agla element dhoondhne ke liye kitne bytes aage jaana hai |

**Interview tip:** `shape` **tuple** hai, function nahi — `arr.shape` likho,
`arr.shape()` **nahi**. Yehi galti beginners bar bar karte hain.
"""))

A(code("""
X = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12]], dtype=np.int32)

print("array:\\n", X)
print("\\nndim     :", X.ndim)          # 2
print("shape    :", X.shape)            # (3, 4) -> 3 rows, 4 cols
print("size     :", X.size)             # 12
print("dtype    :", X.dtype)            # int32
print("itemsize :", X.itemsize, "bytes")# 4
print("nbytes   :", X.nbytes, "bytes")  # 12 * 4 = 48
print("T shape  :", X.T.shape)          # (4, 3)

# Rishta yaad rakho
assert X.size == X.shape[0] * X.shape[1]
assert X.nbytes == X.size * X.itemsize
"""))

A(code("""
# 3D par bhi wahi attributes — mental model pakka karo
batch = np.zeros((4, 28, 28), dtype=np.uint8)   # 4 grayscale images, 28x28 each

print("shape :", batch.shape, "-> (kitni images, height, width)")
print("ndim  :", batch.ndim)
print("size  :", batch.size, "= 4*28*28")
print("nbytes:", batch.nbytes, "bytes (uint8 = 1 byte per pixel)")

# flags -> memory layout
print("\\nC_CONTIGUOUS:", batch.flags['C_CONTIGUOUS'])   # row-major (default)
print("F_CONTIGUOUS:", batch.flags['F_CONTIGUOUS'])
print("OWNDATA     :", batch.flags['OWNDATA'])          # apna data hai ya kisi ka view

# strides -> bytes me "jump size" har axis ke liye
print("strides     :", batch.strides, "(bytes)")
print("Matlab: agli image ke liye", batch.strides[0], "bytes aage, agli row ke liye",
      batch.strides[1], "bytes.")
"""))

A(code("""
# Transpose sirf strides ulat deta hai -> data COPY nahi hota (bohat sasta operation)
Y = X.T
print("X.T:\\n", Y)
print("\\nX strides  :", X.strides)
print("X.T strides:", Y.strides, "<- ulat gaye, data waisa hi hai")
print("X.T ne data copy kiya? OWNDATA =", Y.flags['OWNDATA'], "-> False yaani VIEW hai")
print("X.T ka base X hai?", Y.base is X)
"""))

# ---------------------------------------------------------------- section 5
A(md("""
## 5. dtypes — poori tafseel

**Kya hai:** `dtype` = array ke har element ka data type. Ye decide karta hai
(a) kitni memory lagegi, (b) kitni **range** aa sakti hai, (c) kitni **precision**.

### Integer family

| dtype | bytes | range |
|---|---|---|
| `int8` | 1 | -128 .. 127 |
| `int16` | 2 | -32,768 .. 32,767 |
| `int32` | 4 | ~ -2.1e9 .. 2.1e9 |
| `int64` | 8 | ~ -9.2e18 .. 9.2e18 (default on Linux/Mac, aur Windows par NumPy 2 me bhi) |
| `uint8` | 1 | 0 .. 255 (images ke liye perfect) |
| `uint16/32/64` | 2/4/8 | sirf non-negative |

### Float family

| dtype | bytes | ~decimal digits | kahan |
|---|---|---|---|
| `float16` | 2 | ~3 | deep learning me memory bachane ke liye |
| `float32` | 4 | ~7 | ML/GPU ka default |
| `float64` | 8 | ~15-16 | NumPy ka default, scientific compute |

### Baqi

- `bool_` (1 byte — **8 bits nahi, poora 1 byte**)
- `complex64` / `complex128` (do floats: real + imaginary)
- `<U<n>` unicode string (n chars, har char 4 bytes)
- `S<n>` bytes string
- `object` (Python objects ke pointers — slow)
- `datetime64` / `timedelta64`
"""))

A(code("""
# np.iinfo -> integer types ki range
print("--- Integers ---")
for dt in (np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16):
    info = np.iinfo(dt)
    print(f"{np.dtype(dt).name:>7} | {np.dtype(dt).itemsize} byte | "
          f"min={info.min:>21} max={info.max:>21}")
"""))

A(code("""
# np.finfo -> float types ki precision aur range
print("--- Floats ---")
for dt in (np.float16, np.float32, np.float64):
    info = np.finfo(dt)
    print(f"{np.dtype(dt).name:>8} | {np.dtype(dt).itemsize} byte | "
          f"eps={float(info.eps):.3e} | max={float(info.max):.3e}")

# 'eps' = sab se chhota farq jo 1.0 ke sath jama karne par mehsoos hota hai.
# Floating point comparison me yehi eps kaam aata hai (np.isclose andar isay use karta hai).
print("\\nfloat64 eps =", np.finfo(np.float64).eps)
"""))

A(code("""
# bool, complex, string, object, datetime
b = np.array([True, False, True])
print("bool     :", b, "| dtype:", b.dtype, "| itemsize:", b.itemsize, "byte (1, na ke 1 bit)")

c = np.array([1 + 2j, 3 - 4j])
print("complex  :", c, "| dtype:", c.dtype, "| real:", c.real, "| imag:", c.imag)

s = np.array(["Lahore", "Karachi", "Multan"])
print("string   :", s, "| dtype:", s.dtype, "| itemsize:", s.itemsize, "bytes")
print("           '<U7' matlab: unicode, max 7 characters (7 * 4 = 28 bytes)")

# GOTCHA: fixed-width string me lamba value daalo to CHUP-CHAP kat jata hai!
short = np.array(["abc", "de"])          # dtype <U3
short[0] = "abcdefgh"                    # 8 chars, magar sirf 3 fit honge
print("\\ntruncation gotcha:", short[0], "<- 'abcdefgh' kat kar 'abc' reh gaya")

d = np.array(["2026-01-15", "2026-03-01"], dtype="datetime64[D]")
print("\\ndatetime :", d, "| dtype:", d.dtype, "| farq:", (d[1] - d[0]))
"""))

A(md("""
### 5.1 Integer overflow — silent aur khatarnaak

**Kya hai:** Fixed-width integer me itni hi value aati hai jitni range me fit ho.
Range se bahar jao to value **wrap around** ho jati hai (modular arithmetic), koi
exception nahi aata — sirf ek `RuntimeWarning`.

**Kyun ahem:** `uint8` images me `pixel + 100` karo to bright pixels **kaale** ho
jate hain (255 ke baad 0 se dobara shuru). Ye real bug hai jo har image-processing
beginner ko lagta hai.

**NumPy 2 ka farq:** `np.int8(200)` jaisa **scalar constructor** ab seedha
`OverflowError` deta hai (pehle chup-chap wrap karta tha). Ye behtari hai.
"""))

A(code("""
# 1) Array arithmetic me overflow -> wrap around (warning ke sath)
with np.errstate(over="ignore"):          # warning ko silent kar rahe hain, taake output saaf rahe
    x = np.array([127], dtype=np.int8)
    print("int8 127 + 1 =", x + np.int8(1), "<- -128! wrap around ho gaya")

    u = np.array([250], dtype=np.uint8)
    print("uint8 250 + 10 =", u + np.uint8(10), "<- 4 (250+10=260, 260 % 256 = 4)")

# 2) NumPy 2 me scalar constructor range check karta hai
try:
    np.int8(200)
except OverflowError as e:
    print("\\nnp.int8(200) -> OverflowError:", e)

# 3) astype se bhi chup-chap wrap hota hai (yahan warning bhi nahi aati!)
big = np.array([300, -300, 1000])
print("\\n[300, -300, 1000].astype(int8) =", big.astype(np.int8), "<- ghalat values, koi error nahi")
"""))

A(code("""
# ASLI DUNIYA ka overflow bug: image brightness barhana
img = np.array([[10, 200, 250]], dtype=np.uint8)     # 3 pixels

with np.errstate(over="ignore"):
    wrong = img + np.uint8(50)                        # GALAT tareeqa
print("original :", img)
print("GALAT    :", wrong, "<- 200->250 theek, magar 250->44 (kaala) BUG!")

# SAHI tareeqa: pehle bara dtype me jao, clip karo, phir wapas uint8
right = np.clip(img.astype(np.int16) + 50, 0, 255).astype(np.uint8)
print("SAHI     :", right, "<- 255 par ruk gaya (saturate)")

assert right.tolist() == [[60, 250, 255]]
"""))

A(md("""
### 5.2 Casting — `astype` aur safety rules

**Syntax:** `arr.astype(new_dtype, casting='unsafe', copy=True)`

- `astype` by default **naya array (copy)** banata hai — original nahi badalta.
- Default casting rule `'unsafe'` hai, yaani NumPy tumhein data khone se **nahi rokega**.
- `np.can_cast(from, to, casting=...)` se pehle pooch sakte ho ke safe hai ya nahi.

**Casting rules ka sequence (dheela se sakht):**
`'unsafe'` → `'same_kind'` → `'safe'` → `'equiv'` → `'no'`
"""))

A(code("""
f = np.array([1.7, -2.7, 3.99])

print("float -> int :", f.astype(np.int32), "<- TRUNCATE (zero ki taraf), round NAHI")
print("sahi rounding:", np.round(f).astype(np.int32), "<- pehle round, phir astype")

print("\\nint -> float :", np.array([1, 2, 3]).astype(np.float64))
print("num -> bool  :", np.array([0, 1, -5, 0.0, 0.1]).astype(bool), "<- 0 = False, baqi sab True")
print("bool -> int  :", np.array([True, False, True]).astype(np.int8))
print("num -> str   :", np.array([1, 22, 333]).astype(str))
print("str -> int   :", np.array(["10", "20"]).astype(np.int32), "<- chalta hai agar text valid ho")

# astype COPY banata hai -> original safe
orig = np.array([1, 2, 3])
conv = orig.astype(np.float64)
conv[0] = 99.9
print("\\noriginal ke sath kuch nahi hua:", orig, "| naya:", conv)
"""))

A(code("""
# can_cast se safety check
print("int8  -> int64  safe? ", np.can_cast(np.int8, np.int64, casting="safe"))    # True
print("int64 -> int8   safe? ", np.can_cast(np.int64, np.int8, casting="safe"))    # False (data ja sakta hai)
print("float64 -> int32 safe?", np.can_cast(np.float64, np.int32, casting="safe")) # False
print("float32 -> float64 safe?", np.can_cast(np.float32, np.float64, casting="safe"))  # True

# casting='safe' maango to NumPy mana kar dega
try:
    np.array([1.5, 2.5]).astype(np.int32, casting="safe")
except TypeError as e:
    print("\\ncasting='safe' ne roka -> TypeError:", str(e)[:80], "...")

# str -> int par galat text = ValueError
try:
    np.array(["10", "abc"]).astype(np.int32)
except ValueError as e:
    print("\\nghalat text -> ValueError:", str(e)[:70], "...")
"""))

A(code("""
# TYPE PROMOTION: do dtypes milne par result kya hoga? np.result_type batata hai
pairs = [(np.int8, np.int16), (np.int32, np.float32), (np.int64, np.float32),
         (np.float32, np.float64), (np.bool_, np.int8), (np.int32, np.uint32)]

for a_dt, b_dt in pairs:
    r = np.result_type(a_dt, b_dt)
    print(f"{np.dtype(a_dt).name:>8} + {np.dtype(b_dt).name:<8} -> {r.name}")

print("\\nDhyan do: int64 + float32 -> float64 (dono ko fit karne ke liye barha dtype).")
"""))

# ---------------------------------------------------------------- section 6
A(md("""
## 6. Creation functions — array banane ke tayyar shuda tareeqe

`np.array()` ke ilawa NumPy bohat si "factory" functions deta hai. Inka faida:
(a) tez, (b) memory pehle se allocate ho jati hai, (c) code saaf.

| Function | Kya deta hai |
|---|---|
| `np.zeros(shape)` | sab 0 |
| `np.ones(shape)` | sab 1 |
| `np.full(shape, v)` | sab `v` |
| `np.empty(shape)` | **garbage** (uninitialized) — sab se tez |
| `np.zeros_like(a)` | `a` ki shape/dtype ka zeros array |
| `np.eye(n)` / `np.identity(n)` | identity matrix |
| `np.diag(v)` | vector se diagonal matrix (ya matrix se diagonal) |
| `np.arange(...)` | range jaisa, magar float step bhi |
| `np.linspace(a, b, n)` | a se b tak **n** equally spaced points |
| `np.logspace` / `np.geomspace` | log scale par points |
"""))

A(code("""
# zeros / ones / full — shape tuple do (1D ke liye int bhi chalta hai)
print("zeros(3)      :", np.zeros(3), "| dtype:", np.zeros(3).dtype, "<- default FLOAT64")
print("zeros(3, int) :", np.zeros(3, dtype=int))
print("\\nones((2,3)):\\n", np.ones((2, 3)))
print("\\nfull((2,3), 7):\\n", np.full((2, 3), 7))
print("\\nfull with nan:\\n", np.full((2, 2), np.nan), "<- 'missing data' placeholder ka aam idiom")

# GOTCHA: zeros(3) float deta hai. Integer counters chahiye to dtype=int likho warna
# baad me float/int ka masla hoga.
assert np.zeros(3).dtype == np.float64
assert np.zeros(3, dtype=int).dtype == np.int64 or np.zeros(3, dtype=int).dtype == np.int32
"""))

A(code("""
# np.empty -> memory allocate karta hai magar FILL nahi karta => purana garbage
e = np.empty(5)
print("empty(5):", e)
print("\\nYe numbers 'random' nahi hain — ye us memory me pehle se para hua kachra hai.")
print("Kabhi kabhi ittefaq se sab 0 bhi aa sakte hain — us par bharosa MAT karo.")

# Kab empty use karein? Jab tum FORAN poora array khud bharne wale ho:
out = np.empty(5, dtype=np.int64)         # allocate
for i in range(5):
    out[i] = i * i                        # har khaana khud bhar diya
print("\\nbharne ke baad:", out)

# Speed ka farq (bare arrays par mehsoos hota hai)
t_zeros = timeit.timeit("np.zeros(1_000_000)", globals=globals(), number=100)
t_empty = timeit.timeit("np.empty(1_000_000)", globals=globals(), number=100)
print(f"\\nzeros: {t_zeros:.4f}s | empty: {t_empty:.4f}s  (empty ko 0 likhne ki mehnat nahi karni parti)")
"""))

A(code("""
# *_like family -> kisi maujooda array ki shape aur dtype copy kar lo
template = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32)

print("zeros_like :\\n", np.zeros_like(template))
print("ones_like  :\\n", np.ones_like(template))
print("full_like  :\\n", np.full_like(template, 9.5))
print("empty_like shape:", np.empty_like(template).shape)

# dtype override bhi kar sakte ho
print("\\nzeros_like with dtype=int:", np.zeros_like(template, dtype=int).dtype)

# Kyun useful? "Result array" banane ke liye jo input jaisa hi ho
assert np.zeros_like(template).shape == template.shape
assert np.zeros_like(template).dtype == template.dtype
"""))

A(code("""
# eye / identity / diag / diagflat / tri
print("eye(3):\\n", np.eye(3))
print("\\neye(3, k=1) -> diagonal 1 step upar:\\n", np.eye(3, k=1))
print("\\neye(2, 4) -> non-square bhi:\\n", np.eye(2, 4))
print("\\nidentity(3) == eye(3)?", np.array_equal(np.identity(3), np.eye(3)),
      "<- identity sirf square banata hai, eye zyada flexible hai")

print("\\ndiag([1,2,3]) -> vector se matrix:\\n", np.diag([1, 2, 3]))
M = np.arange(1, 10).reshape(3, 3)
print("\\nM:\\n", M)
print("diag(M) -> matrix se diagonal:", np.diag(M), "<- SAME function, dono kaam!")

print("\\ntri(3) lower-triangular ones:\\n", np.tri(3))
print("\\ntriu(M) upper:\\n", np.triu(M))
print("tril(M) lower:\\n", np.tril(M))
"""))

A(md("""
### 6.1 `np.arange` — aur float step ka mashhoor masla

**Syntax:** `np.arange(start, stop, step, dtype=None)` — `stop` **shamil nahi**.

**Gotcha (bohat ahem):** `step` float ho to floating-point error ki wajah se
elements ki **ginti predict karna mushkil** ho jata hai. Kabhi ek extra element aa
jata hai, kabhi kam. Isliye **float step ke liye `arange` mat use karo —
`linspace` use karo.**
"""))

A(code("""
print("arange(5)        :", np.arange(5))
print("arange(2, 10)    :", np.arange(2, 10))
print("arange(0, 10, 3) :", np.arange(0, 10, 3), "<- 10 shamil nahi")
print("arange(10, 0, -2):", np.arange(10, 0, -2), "<- ulta")
print("arange(5, dtype=float):", np.arange(5, dtype=float))

# FLOAT STEP KA MASLA
a1 = np.arange(0, 1, 0.1)
print("\\narange(0, 1, 0.1) -> size:", a1.size)          # 10 (theek lagta hai)
print(a1)

a2 = np.arange(0, 1.1, 0.1)
print("\\narange(0, 1.1, 0.1) -> size:", a2.size, "<- 11 ya 12? predict karna mushkil")
print("aakhri element:", a2[-1], "| kya ye theek 1.1 hai?", a2[-1] == 1.1)

a3 = np.arange(1, 1.3, 0.1)
print("\\narange(1, 1.3, 0.1) -> size:", a3.size, "| aakhri:", a3[-1],
      "<- 1.3 (stop) bhi aa gaya! kyunki 1+0.1+0.1 thoda 1.3 se kam nikla")
print("\\nSABAQ: float step ke liye linspace use karo.")
"""))

A(md("""
### 6.2 `linspace` / `logspace` / `geomspace`

**`np.linspace(start, stop, num=50, endpoint=True, retstep=False)`**

- Yahan tum **kitne points** chahiye wo batate ho (step nahi) → exact aur predictable.
- `endpoint=True` (default) → `stop` **shamil** hota hai (arange ke ulta!).
- `retstep=True` → `(array, step)` tuple milta hai.

**`np.logspace(a, b, n, base=10)`** → `base**a` se `base**b` tak, log scale par.
Hyperparameter search (learning rate `1e-5` se `1e-1`) me roz use hota hai.

**`np.geomspace(a, b, n)`** → seedha actual values do (log lena nahi parta).
"""))

A(code("""
print("linspace(0, 1, 5)   :", np.linspace(0, 1, 5), "<- 1 SHAMIL hai")
print("linspace(0, 1, 5, endpoint=False):", np.linspace(0, 1, 5, endpoint=False))

vals, step = np.linspace(0, 10, 5, retstep=True)
print("\\nretstep=True -> values:", vals, "| step:", step)

# 0..1 ke 11 exact points -- yahan arange fail karta tha, linspace nahi
lin = np.linspace(0, 1, 11)
print("\\nlinspace(0,1,11):", lin)
print("aakhri element theek 1.0 hai?", lin[-1] == 1.0)
assert lin.size == 11 and lin[-1] == 1.0        # predictable -> assert kar sakte hain
"""))

A(code("""
# logspace -- learning rate grid banane ka asli use-case
lrs = np.logspace(-5, -1, 5)          # 10^-5 se 10^-1 tak 5 values
print("logspace(-5, -1, 5):", lrs)
print("padho:", [f"{v:.0e}" for v in lrs])

print("\\nbase=2 (batch sizes):", np.logspace(4, 9, 6, base=2).astype(int))

# geomspace -- actual values do, log khud nikal lega
print("\\ngeomspace(1, 1000, 4):", np.geomspace(1, 1000, 4))
print("geomspace == logspace(log10(a), log10(b))? ",
      np.allclose(np.geomspace(1, 1000, 4), np.logspace(0, 3, 4)))
"""))

# ---------------------------------------------------------------- section 7
A(md("""
## 7. `np.random` — random data banana

**NumPy 2 ka aham message:** naye code me **`np.random.default_rng()`** use karo
(Generator API). Purana `np.random.seed()` + `np.random.rand()` (legacy
`RandomState`) sirf backward-compatibility ke liye hai.

**Kyun Generator behtar hai:**
- Bilkul alag alag independent generators bana sakte ho (global state ka masla khatam)
- Behtar statistical quality (PCG64 algorithm)
- Thread/parallel-friendly

| Generator method | Kya deta hai |
|---|---|
| `rng.integers(low, high, size)` | integers (`high` **shamil nahi**, `endpoint=True` se shamil) |
| `rng.random(size)` | uniform floats `[0, 1)` |
| `rng.uniform(a, b, size)` | uniform floats `[a, b)` |
| `rng.normal(loc, scale, size)` | Gaussian / normal distribution |
| `rng.choice(a, size, replace, p)` | sample uthana |
| `rng.shuffle(a)` | **in-place** shuffle |
| `rng.permutation(a)` | shuffled **copy** |

**Reproducibility:** seed do → hamesha wahi numbers. ML experiments me **lazmi**.
"""))

A(code("""
# Generator banao -- seed do taake result hamesha same rahe (reproducible)
rng = np.random.default_rng(42)

print("integers(0, 10, 5)   :", rng.integers(0, 10, 5), "<- 10 shamil nahi")
print("integers endpoint    :", rng.integers(1, 6, 5, endpoint=True), "<- dice roll 1..6")
print("random(5)            :", rng.random(5).round(4))
print("uniform(-1, 1, 5)    :", rng.uniform(-1, 1, 5).round(3))
print("normal(mean=100,sd=15):", rng.normal(100, 15, 5).round(2), "<- IQ jaisa data")
print("\\n2D shape bhi:\\n", rng.integers(0, 100, (3, 4)))
"""))

A(code("""
# REPRODUCIBILITY ka proof -- ek hi seed, ek hi output
r1 = np.random.default_rng(7)
r2 = np.random.default_rng(7)
print("rng(7) pehli baar :", r1.integers(0, 100, 5))
print("rng(7) doosri baar:", r2.integers(0, 100, 5))
assert np.array_equal(np.random.default_rng(7).integers(0, 100, 5),
                      np.random.default_rng(7).integers(0, 100, 5))
print("-> bilkul same. Isi wajah se paper/assignment ke results dobara ban jate hain.")

# Alag seed = alag data
print("\\nrng(8):", np.random.default_rng(8).integers(0, 100, 5))

# GOTCHA: ek hi rng se DOBARA maangoge to naye numbers aayenge (state aage barh gayi)
r3 = np.random.default_rng(7)
print("\\nsame rng, call 1:", r3.integers(0, 100, 5))
print("same rng, call 2:", r3.integers(0, 100, 5), "<- different! state advance hui")
"""))

A(code("""
# choice / shuffle / permutation
rng = np.random.default_rng(0)
cities = np.array(["Lahore", "Karachi", "Islamabad", "Multan", "Peshawar"])

print("choice 3 (replace=False):", rng.choice(cities, 3, replace=False))
print("choice 5 (replace=True) :", rng.choice(cities, 5, replace=True), "<- repeat mumkin")

# weighted choice -- p ka sum 1 hona chahiye
probs = [0.6, 0.1, 0.1, 0.1, 0.1]
print("weighted (Lahore ka 60% chance):", rng.choice(cities, 6, p=probs))

# shuffle IN-PLACE hai (original badal jata hai) aur None return karta hai
arr = np.arange(10)
rng.shuffle(arr)
print("\\nshuffle ke baad (in-place):", arr)

# permutation COPY deta hai (original safe)
orig = np.arange(10)
perm = rng.permutation(orig)
print("permutation:", perm, "| original still:", orig)

# GOTCHA: x = rng.shuffle(arr) likhoge to x = None milega!
bad = rng.shuffle(arr)
print("\\nrng.shuffle() ka return:", bad, "<- YAAD RAKHO: None")
"""))

A(code("""
# LEGACY API (purane code me milega) -- global seed
np.random.seed(0)                       # global state set
print("np.random.rand(3)   :", np.random.rand(3).round(4))
print("np.random.randn(3)  :", np.random.randn(3).round(4), "<- standard normal")
print("np.random.randint(0, 10, 3):", np.random.randint(0, 10, 3))

np.random.seed(0)                       # dobara wahi seed
print("\\nseed reset ke baad  :", np.random.rand(3).round(4), "<- same numbers")

print("\\nFARQ:")
print("  legacy : np.random.seed(0) global state badalta hai -> library code me khatarnaak")
print("  modern : rng = np.random.default_rng(0) -> apna alag, isolated state")
"""))

# ---------------------------------------------------------------- section 8
A(md("""
## 8. `fromfunction`, `fromiter`, `meshgrid`

- **`np.fromfunction(f, shape)`** — `f` ko **index arrays** milte hain, aur wo
  vectorized formula se poora array bana deta hai. Pattern/grid banane me kaam aata hai.
- **`np.fromiter(iterable, dtype, count=-1)`** — generator se array. `dtype`
  **lazmi** hai. Memory-efficient (poori list pehle nahi banti).
- **`np.meshgrid(x, y)`** — 1D coordinates se 2D grid. Har (x, y) jori par kuch
  compute karna ho to yehi tareeqa hai.
"""))

A(code("""
# fromfunction -- f ko (i, j) index arrays milte hain, scalars nahi!
add_table = np.fromfunction(lambda i, j: i + j, (4, 4), dtype=int)
print("i + j table:\\n", add_table)

mult_table = np.fromfunction(lambda i, j: (i + 1) * (j + 1), (5, 5), dtype=int)
print("\\npahara (multiplication table):\\n", mult_table)

# Checkerboard -- (i+j) % 2
checker = np.fromfunction(lambda i, j: (i + j) % 2, (6, 6), dtype=int)
print("\\ncheckerboard:\\n", checker)
"""))

A(code("""
# fromiter -- generator se array (dtype lazmi)
squares = np.fromiter((i * i for i in range(8)), dtype=np.int64)
print("squares       :", squares)

# count= dena tez hota hai (NumPy pehle se memory allocate kar leta hai)
first5 = np.fromiter(range(1000), dtype=np.int64, count=5)
print("count=5       :", first5)

# Filter ke sath -- 'list bana kar np.array' se memory-friendly
evens = np.fromiter((x for x in range(20) if x % 2 == 0), dtype=np.int64)
print("even numbers  :", evens)

# dtype bhool jao to TypeError
try:
    np.fromiter(range(5))
except TypeError as e:
    print("\\ndtype bhool gaye -> TypeError:", str(e)[:60], "...")
"""))

A(code("""
# meshgrid -- 1D coords se 2D grid
x = np.array([0, 1, 2])          # 3 values
y = np.array([10, 20])           # 2 values
XX, YY = np.meshgrid(x, y)

print("XX (x values har row me repeat):\\n", XX, "shape:", XX.shape)
print("\\nYY (y values har column me repeat):\\n", YY, "shape:", YY.shape)

# Ab har (x, y) jori par formula chala sakte ho -- ek hi step me, bina loop
Z = XX + YY
print("\\nZ = XX + YY (har jori ka sum):\\n", Z)

# indexing='ij' matrix-style (row=x, col=y) deta hai
XI, YI = np.meshgrid(x, y, indexing="ij")
print("\\nindexing='ij' shapes:", XI.shape, YI.shape, "<- (len(x), len(y))")
print("default 'xy' shapes :", XX.shape, YY.shape, "<- (len(y), len(x))  [ye gotcha hai]")
"""))

# ---------------------------------------------------------------- section 9
A(md("""
## 9. `np.array` vs `np.asarray` — copy ya no-copy?

| Call | Input already ndarray (same dtype) ho to |
|---|---|
| `np.array(x)` | **hamesha naya copy** banata hai |
| `np.asarray(x)` | **wahi object** wapas deta hai (copy nahi) |

**Kyun ahem:** Library/function likhte waqt `np.asarray(x)` use karo — caller ka
data agar pehle se array hai to bekar copy nahi banegi (performance).

**NumPy 2 ka bara change (gotcha):** `np.array(x, copy=False)` ka matlab pehle
"copy sirf zaroorat par" tha; ab iska matlab **"copy bilkul na karo"** hai, aur
copy zaroori ho to `ValueError` phenkta hai. Purana behaviour chahiye to
`np.asarray(x)` likho.
"""))

A(code("""
base = np.array([1, 2, 3])

print("np.array(base)   is base ?", np.array(base) is base)     # False -> copy
print("np.asarray(base) is base ?", np.asarray(base) is base)   # True  -> same object

# Proof: asarray ka natija modify karo to ORIGINAL badal jata hai
same = np.asarray(base)
same[0] = 999
print("\\nasarray ke through likha -> base:", base, "<- badal gaya!")

copied = np.array(base)          # naya copy
copied[0] = -1
print("array() copy ke through  -> base:", base, "<- surakshit")

# List se banao to dono copy hi karte hain (list array nahi hai)
lst = [1, 2, 3]
print("\\nlist se asarray bhi naya array banata hai:", np.asarray(lst) is lst)
"""))

A(code("""
# NumPy 2 ka copy=False gotcha
try:
    np.array([1, 2, 3], copy=False)          # list -> copy zaroori hai -> error
except ValueError as e:
    print("np.array(list, copy=False) -> ValueError:")
    print("  ", str(e).splitlines()[0])

# dtype badalna ho to bhi copy lazmi hai -> phir error
try:
    np.array(base, copy=False, dtype=np.float64)
except ValueError as e:
    print("\\ndtype change ke sath copy=False -> ValueError bhi aata hai")

# SAHI tareeqe
print("\\nHal 1 (no-copy chahiye)      :", np.asarray([1, 2, 3]))
print("Hal 2 (copy zaroor chahiye)  :", np.array(base, copy=True))
print("Hal 3 (dtype ke sath no-copy):", np.asarray(base, dtype=np.int64) is base)
"""))

# ---------------------------------------------------------------- section 10
A(md("""
## 10. Scalars vs 0-d arrays

**Kya hai:** `np.array(5)` ek **0-dimensional array** hai — shape `()`, ndim `0`.
Ye `5` (Python int) se alag cheez hai, aur `np.array([5])` (1-D, shape `(1,)`) se bhi.

Aggregations (`sum`, `mean`) **NumPy scalar** dete hain (`np.int64(6)`), Python int nahi.
Ye 99% jagah Python number ki tarah kaam karta hai, magar `repr` alag dikhta hai
(NumPy 2 me `np.int64(6)`) — yehi cheez logon ko confuse karti hai.

**`.item()`** se asli Python scalar mil jata hai (JSON dump / f-string ke liye useful).
"""))

A(code("""
zero_d = np.array(5)
one_d = np.array([5])

print("np.array(5)   -> shape:", zero_d.shape, "| ndim:", zero_d.ndim, "| repr:", repr(zero_d))
print("np.array([5]) -> shape:", one_d.shape, "| ndim:", one_d.ndim, "| repr:", repr(one_d))

# 0-d ko index nahi kar sakte
try:
    zero_d[0]
except IndexError as e:
    print("\\nzero_d[0] -> IndexError:", e)

# Magar value nikalne ke tareeqe hain
print("\\nzero_d.item() :", zero_d.item(), type(zero_d.item()))
print("float(zero_d) :", float(zero_d))
print("zero_d[()]    :", zero_d[()], "<- 0-d ko index karne ka official tareeqa")
"""))

A(code("""
# Aggregation NumPy scalar deta hai
s = np.array([1, 2, 3]).sum()
print("repr(arr.sum()) :", repr(s), "<- np.int64(6), na ke 6")
print("type            :", type(s))
print("Python int ke sath compare chalta hai? ", s == 6)
print("isinstance(s, int)?", isinstance(s, int), "<- False! (numpy scalar hai)")
print("s.item() ka type :", type(s.item()))

# Isliye assert me == likhna theek hai
assert s == 6
assert np.array([1, 2, 3]).mean() == 2.0

# f-string me bhi theek dikhta hai
print(f"\\nf-string: total = {s}, mean = {np.array([1, 2, 3]).mean()}")
"""))

# ---------------------------------------------------------------- section 11
A(md("""
## 11. `np.inf` aur `np.nan` — special floats

**`np.nan`** = "Not a Number" — missing / undefined value ka standard marker.
**`np.inf`** = infinity.

### NaN ke ajeeb (magar standard) rules

| Expression | Natija | Kyun |
|---|---|---|
| `np.nan == np.nan` | `False` | IEEE-754: NaN kisi ke barabar nahi, khud ke bhi nahi |
| `np.nan != np.nan` | `True` | isi wajah se |
| `np.nan > 5` | `False` | har comparison False |
| `nan + 5` | `nan` | NaN sab kuch "zeher" kar deta hai |
| `arr.sum()` with a nan | `nan` | poora total barbaad |
| `np.isnan(x)` | `True/False` | **NaN check karne ka SAHI tareeqa** |

**Ahem:** `nan` ek **float** hai. Isliye integer array me `nan` nahi rakha ja sakta —
array khud float ban jayega. Yehi wajah hai ke pandas me missing values wale int
columns float ban jate hain.

**NumPy 2 note:** `np.NaN` aur `np.Inf` **hata diye gaye** hain — sirf lowercase
`np.nan` / `np.inf` chalega.
"""))

A(code("""
print("np.nan == np.nan :", np.nan == np.nan, "<- False! (sab se bara gotcha)")
print("np.nan != np.nan :", np.nan != np.nan, "<- True")
print("np.nan > 5       :", np.nan > 5)
print("np.nan < 5       :", np.nan < 5, "<- dono False, ye 'unordered' hai")
print("np.isnan(np.nan) :", np.isnan(np.nan), "<- SAHI check")

print("\\nnan ka dtype:", np.array([np.nan]).dtype, "-> float64")
print("nan int array me:", np.array([1, 2, np.nan]).dtype, "<- poora array float ban gaya")

# NumPy 2 me purane naam hat gaye
try:
    np.NaN
except AttributeError as e:
    print("\\nnp.NaN ->", str(e).split(".")[0] + ".")
"""))

A(code("""
data = np.array([10.0, 20.0, np.nan, 40.0, np.nan])

print("data           :", data)
print("isnan mask     :", np.isnan(data))
print("kitne nan      :", np.isnan(data).sum())
print("koi nan hai?   :", np.isnan(data).any())

print("\\n--- Aam aggregation nan se barbaad ho jati hai ---")
print("sum  :", data.sum(), "| mean:", data.mean())

print("\\n--- nan-safe versions ---")
print("nansum :", np.nansum(data))
print("nanmean:", np.nanmean(data), "<- (10+20+40)/3, sirf 3 valid values")
print("nanmax :", np.nanmax(data), "| nanmin:", np.nanmin(data))

print("\\n--- Ya nan hata do / bhar do ---")
print("hata kar :", data[~np.isnan(data)])
filled = np.where(np.isnan(data), 0.0, data)         # nan ki jagah 0
print("0 se bhar:", filled)

assert np.nansum(data) == 70.0
assert np.nanmean(data) == 70.0 / 3
"""))

A(code("""
# inf ke rules
print("np.inf         :", np.inf, "| -np.inf:", -np.inf)
print("np.inf > 10**100:", np.inf > 10**100, "<- har number se bara")
print("inf + 1        :", np.inf + 1)
print("inf - inf      :", np.inf - np.inf, "<- nan! (undefined)")
print("inf / inf      :", np.inf / np.inf, "<- nan")
print("1 / inf        :", 1 / np.inf)

# Division by zero -- errstate se warning silent karte hain
with np.errstate(divide="ignore", invalid="ignore"):
    x = np.array([1.0, -1.0, 0.0])
    print("\\n[1, -1, 0] / 0 =", x / 0, "<- inf, -inf, nan")

# Checking helpers
vals = np.array([1.0, np.inf, -np.inf, np.nan])
print("\\nvalues     :", vals)
print("isinf      :", np.isinf(vals))
print("isnan      :", np.isnan(vals))
print("isfinite   :", np.isfinite(vals), "<- 'saaf' data ka best filter")
print("saaf values:", vals[np.isfinite(vals)])
"""))

# ---------------------------------------------------------------- section 12
A(md("""
## 12. Printing options — `np.set_printoptions`

Bara array print karo to NumPy beech se `...` daal kar chhota kar deta hai.
Aur floats bohat lambi decimal poonch ke sath aate hain. Ye sab control ho sakta hai:

| Option | Kaam |
|---|---|
| `precision` | kitne decimal digits |
| `suppress=True` | scientific notation (`1e-10`) band, plain decimals |
| `threshold` | is se zyada elements ho to `...` se summarize |
| `linewidth` | ek line me kitne characters |
| `edgeitems` | summarize karte waqt shuru/aakhir me kitne dikhaye |

**Behtar tareeqa:** `np.printoptions(...)` **context manager** use karo — sirf
`with` block ke andar asar hoga, global setting kharab nahi hogi.
"""))

A(code("""
vals = np.array([1.123456789, 0.000000123, 12345.6789])

print("default            :", vals)

with np.printoptions(precision=3):
    print("precision=3        :", vals)

with np.printoptions(precision=3, suppress=True):
    print("+ suppress=True    :", vals, "<- scientific notation gayab")

# Bara array -> khud-ba-khud truncate
big = np.arange(2000)
print("\\nbara array:", big)
print("Beech me '...' -> NumPy ne summarize kar diya (threshold=1000 default).")

with np.printoptions(threshold=10, edgeitems=2):
    print("\\nthreshold=10, edgeitems=2:", np.arange(50))
"""))

A(code("""
# Global set karna (poore session par asar) -- aur wapas reset
np.set_printoptions(precision=2, suppress=True)
print("global set ke baad:", np.array([1.23456, 2.99999]))

np.set_printoptions(precision=8, suppress=False)     # NumPy ke defaults par wapas
print("reset ke baad     :", np.array([1.23456, 2.99999]))

# Kaunsi options maujood hain?
opts = np.get_printoptions()
for k in ("precision", "threshold", "edgeitems", "linewidth", "suppress"):
    print(f"  {k:>10} = {opts[k]}")

print("\\nInterview tip: set_printoptions sirf DIKHAWA badalta hai, data ki asli")
print("precision par koi asar NAHI hota. Ye debugging/report ke liye hai.")
"""))

# ---------------------------------------------------------------- gotchas
A(md("""
## 13. Common Mistakes / Gotchas — ek jagah jama

1. **`arr.shape()`** — `shape` tuple hai, function nahi. Brackets na lagao.
2. **`np.zeros(3)` float deta hai** — integer counter chahiye to `dtype=int` likho.
3. **`np.empty` garbage deta hai** — us par bharosa na karo; ya `zeros` use karo.
4. **`arange` float step** — element count predictable nahi. `linspace` use karo.
5. **`arange` me `stop` shamil nahi, `linspace` me shamil hai** — ulta yaad rakhna aam galti hai.
6. **`nan == nan` False hai** — `np.isnan()` use karo.
7. **`nan` float hai** — int array me daalo to poora array float ban jayega.
8. **Silent integer overflow** — `uint8` par arithmetic karte waqt pehle bara dtype me jao.
9. **Mixed list se string array** — `np.array([1, 2, "3"])` sab ko string bana deta hai.
10. **`sum(np_arr)`** (builtin) slow hai — `np_arr.sum()` likho.
11. **`np.array(x, copy=False)`** NumPy 2 me `ValueError` de sakta hai — `np.asarray(x)` likho.
12. **`rng.shuffle()` `None` return karta hai** — in-place hai; `x = rng.shuffle(a)` galat.
13. **`from numpy import *`** builtins tor deta hai — hamesha `import numpy as np`.
14. **`astype` truncate karta hai, round nahi** — `np.round()` pehle lagao.
15. **Fixed-width string dtype** me lamba text chup-chap kat jata hai.
"""))

A(code("""
# Gotcha demos ek sath (sab try/except ya safe form me)
print("1) shape function nahi hai:")
try:
    np.zeros(3).shape()
except TypeError as e:
    print("   TypeError:", str(e)[:55], "...")

print("\\n2) zeros ka dtype       :", np.zeros(3).dtype, "vs", np.zeros(3, dtype=int).dtype)
print("4/5) arange vs linspace  :", np.arange(0, 1, 0.25), "|", np.linspace(0, 1, 5))
print("6) nan equality          :", np.nan == np.nan, "-> isnan:", np.isnan(np.nan))
print("7) nan int array me      :", np.array([1, 2, np.nan]).dtype)
print("9) mixed list            :", np.array([1, 2, "3"]).dtype)
print("14) astype truncate      :", np.array([2.99]).astype(int), "vs round:",
      np.round(np.array([2.99])).astype(int))

print("\\n15) string truncation:")
s = np.array(["ab"])                 # dtype <U2
s[0] = "abcdef"
print("   'abcdef' rakha, mila:", repr(s[0]))
"""))

# ---------------------------------------------------------------- real world
A(md("""
## 14. Real-World Problems

Ab wo cheezein jo asli kaam me roz aati hain.
"""))

A(md("""
### RW-1. Sensor readings ka data array banana aur summary nikalna

Ek factory me 4 sensors hain, har sensor 24 ghante ka reading deta hai.
Data ko `(4, 24)` array me rakho aur per-sensor summary nikalo.
"""))

A(code("""
rng = np.random.default_rng(101)

n_sensors, n_hours = 4, 24
# normal distribution se temperature readings (mean 30, sd 3)
readings = rng.normal(30, 3, size=(n_sensors, n_hours)).round(2)

print("shape:", readings.shape, "| dtype:", readings.dtype, "| memory:", readings.nbytes, "bytes")
print("\\npehle sensor ke pehle 6 ghante:", readings[0, :6])

# Per-sensor summary -> axis=1 (hours collapse ho jate hain)
print("\\n--- Per-sensor summary (axis=1) ---")
for i in range(n_sensors):
    row = readings[i]
    print(f"Sensor {i}: min={row.min():5.2f} max={row.max():5.2f} "
          f"mean={row.mean():5.2f} std={row.std():4.2f}")

# Ek sensor kharab ho gaya -> uski kuch readings nan kar do
readings[2, 5:8] = np.nan
print("\\nSensor 2 ke 3 readings kharab (nan) kar di.")
print("normal mean (barbaad):", readings[2].mean())
print("nanmean (sahi)       :", round(float(np.nanmean(readings[2])), 2))
print("valid readings       :", np.isfinite(readings[2]).sum(), "out of", n_hours)
"""))

A(md("""
### RW-2. Image placeholder banana (H, W, 3)

Computer vision me image = 3D `uint8` array. Chalo synthetic image banate hain
aur uska memory footprint samajhte hain.
"""))

A(code("""
H, W, C = 64, 64, 3

# Kaali image = sab zeros
black = np.zeros((H, W, C), dtype=np.uint8)
# Safed image = sab 255
white = np.full((H, W, C), 255, dtype=np.uint8)
# Sirf laal image -> channel 0 = 255
red = np.zeros((H, W, C), dtype=np.uint8)
red[:, :, 0] = 255

print("shape:", black.shape, "-> (height, width, channels)")
print("dtype:", black.dtype, "-> uint8, kyunki pixel 0..255 hota hai")
print("memory per image:", black.nbytes, "bytes =", black.nbytes / 1024, "KB")
print("\\nblack ka pehla pixel:", black[0, 0], "| white:", white[0, 0], "| red:", red[0, 0])

# Ek batch of 100 images ka budget
batch_mb = 100 * H * W * C * 1 / 1024**2
print(f"\\n100 images (uint8) : {batch_mb:.2f} MB")
print(f"wahi float32 me    : {batch_mb * 4:.2f} MB  <- normalize karne par 4x memory!")
print("Isliye ML pipelines me images ko batch-by-batch float me convert karte hain.")

assert black.nbytes == H * W * C
"""))

A(md("""
### RW-3. ML feature matrix ka dtype/memory budget plan karna

1 crore (10 million) rows, 12 features. Kaunsa dtype affordable hai?
"""))

A(code("""
n_rows, n_feats = 10_000_000, 12

print(f"{'dtype':>10} | {'MB':>10} | {'GB':>7} | 8 GB RAM me fit?")
print("-" * 52)
for dt in (np.float64, np.float32, np.float16, np.int32, np.int8):
    itemsize = np.dtype(dt).itemsize
    mb = n_rows * n_feats * itemsize / 1024**2
    fits = "haan" if mb / 1024 < 6 else "NAHI"          # ~6 GB tak safe maan lo
    print(f"{np.dtype(dt).name:>10} | {mb:10.1f} | {mb/1024:7.2f} | {fits}")

print("\\nFaisla: float32 me kaam chal jayega (float64 se aadhi memory,")
print("aur ML models ke liye float32 ki precision kaafi hoti hai).")

# Chhote sample par dikhate hain ke conversion se kya bachta hai
sample = np.random.default_rng(5).random((1000, 12))          # float64
print(f"\\nsample float64: {sample.nbytes:,} bytes")
print(f"sample float32: {sample.astype(np.float32).nbytes:,} bytes  (theek aadha)")
assert sample.astype(np.float32).nbytes * 2 == sample.nbytes
"""))

A(md("""
### RW-4. Reproducible synthetic dataset banana (train data ke liye)

Model test karne ke liye fake-magar-realistic data chahiye. Seed lazmi, warna
kal result badal jayega.
"""))

A(code("""
rng = np.random.default_rng(2026)
n = 8

# Features
age = rng.integers(18, 60, n)                              # int
salary = rng.normal(80_000, 25_000, n).round(-3)           # float, hazaar par round
experience = rng.integers(0, 20, n)
city = rng.choice(np.array(["LHR", "KHI", "ISB"]), n)
label = rng.integers(0, 2, n)                              # binary target

print(f"{'age':>4} {'salary':>9} {'exp':>4} {'city':>5} {'y':>2}")
for i in range(n):
    print(f"{age[i]:>4} {salary[i]:>9.0f} {experience[i]:>4} {city[i]:>5} {label[i]:>2}")

# Numeric features ko ek feature matrix me jama karo (column_stack)
X = np.column_stack([age, salary, experience]).astype(np.float64)
y = label
print("\\nX shape:", X.shape, "| y shape:", y.shape, "| X dtype:", X.dtype)
print("X ki per-column mean:", X.mean(axis=0).round(1))

assert X.shape == (n, 3)
assert y.shape == (n,)

# Dobara wahi seed -> bilkul wahi data (reproducible)
again = np.random.default_rng(2026).integers(18, 60, n)
assert np.array_equal(age, again)
print("\\nSame seed se same data mila -> experiment reproducible hai.")
"""))

# ---------------------------------------------------------------- leetcode
A(md("""
## 15. LeetCode Problems

> **Zaroori note:** LeetCode par NumPy ka direct role **kam** hai — interview me
> tumse **pure Python** expect kiya jata hai (aur LeetCode ke judge par numpy
> import karna aksar mana/ghair-zaroori hota hai). Neeche har problem ke **do**
> solutions hain:
>
> - **(a) Pure Python** — yehi interview me likhna hai
> - **(b) NumPy / vectorized** — production aur data-work ke liye, aur yahan
>   isliye ke tum dono soch samajh sako
>
> Interview me NumPy version zikr karna acha hai ("production me main
> `np.cumsum` use karta"), magar pehle pure Python wala likho.
"""))

A(md("""
### LC 1929. Concatenation of Array — Easy

https://leetcode.com/problems/concatenation-of-array/

**Bayan:** `nums` di gayi hai (lambai `n`). Ek array `ans` banao jiski lambai `2n` ho,
jahan `ans[i] == nums[i]` aur `ans[i + n] == nums[i]` (`0 <= i < n`).
Yaani seedha `nums` ko apne sath jorna hai.

**Approach:**
1. Pure Python: `nums + nums` (list concatenation) — bas.
   Manually bhi kar sakte ho: nayi list bana kar do baar loop.
2. NumPy: `np.concatenate([a, a])` ya `np.tile(a, 2)`.

**Complexity:** Time **O(n)**, Space **O(n)** (output ke liye) — dono solutions me.
"""))

A(code("""
def get_concatenation_py(nums):
    \"\"\"(a) PURE PYTHON -- interview me yehi likho.\"\"\"
    # List concatenation naya list banata hai: pehle nums, phir dobara nums
    return nums + nums


def get_concatenation_manual(nums):
    \"\"\"(a2) Bina '+' operator -- interviewer 'manually karo' keh de to.\"\"\"
    n = len(nums)
    ans = [0] * (2 * n)              # 2n khaane pehle se allocate
    for i in range(n):
        ans[i] = nums[i]             # pehla hissa
        ans[i + n] = nums[i]         # doosra hissa
    return ans


def get_concatenation_np(nums):
    \"\"\"(b) NUMPY -- vectorized. Bara data ho to yehi tez hai.\"\"\"
    a = np.asarray(nums)             # asarray: agar pehle se array hai to copy nahi
    return np.concatenate([a, a])    # np.tile(a, 2) bhi bilkul wahi natija deta hai


# --- Tests ---
assert get_concatenation_py([1, 2, 1]) == [1, 2, 1, 1, 2, 1]
assert get_concatenation_py([1, 3, 2, 1]) == [1, 3, 2, 1, 1, 3, 2, 1]
assert get_concatenation_manual([1, 2, 1]) == [1, 2, 1, 1, 2, 1]
assert np.array_equal(get_concatenation_np([1, 2, 1]), [1, 2, 1, 1, 2, 1])
assert np.array_equal(np.tile(np.array([1, 2, 1]), 2), [1, 2, 1, 1, 2, 1])

print("LC 1929 pass")
print("pure python :", get_concatenation_py([1, 2, 1]))
print("numpy       :", get_concatenation_np([1, 2, 1]))
"""))

A(md("""
### LC 1480. Running Sum of 1d Array — Easy

https://leetcode.com/problems/running-sum-of-1d-array/

**Bayan:** `runningSum[i] = nums[0] + nums[1] + ... + nums[i]` — yaani **prefix sums**.

**Approach:**
1. Pure Python (optimal): ek hi pass me chalta hua total rakho —
   `nums[i] += nums[i-1]`. In-place karo to extra space `O(1)`.
2. Naive galti: har `i` ke liye dobara sum karna → **O(n²)**. Interview me ye na likho.
3. NumPy: `np.cumsum(a)` — yehi cheez C speed par. `itertools.accumulate` bhi stdlib me hai.

**Complexity:** Time **O(n)**, Space **O(1)** (in-place) ya **O(n)** (naya array).
"""))

A(code("""
from itertools import accumulate


def running_sum_py(nums):
    \"\"\"(a) PURE PYTHON, O(n) time / O(1) extra space -- interview answer.\"\"\"
    out = list(nums)                       # input ko na bigaarne ke liye copy
    for i in range(1, len(out)):
        out[i] += out[i - 1]               # pichla chalta total is element me jama
    return out


def running_sum_naive(nums):
    \"\"\"(a2) NAIVE O(n^2) -- sirf muqabla dikhane ke liye, interview me NA likho.\"\"\"
    return [sum(nums[:i + 1]) for i in range(len(nums))]


def running_sum_stdlib(nums):
    \"\"\"(a3) stdlib itertools.accumulate -- Pythonic aur allowed.\"\"\"
    return list(accumulate(nums))


def running_sum_np(nums):
    \"\"\"(b) NUMPY -- cumsum. Yehi asli 'prefix sum' ka vectorized tareeqa hai.\"\"\"
    return np.cumsum(np.asarray(nums))


# --- Tests ---
cases = [([1, 2, 3, 4], [1, 3, 6, 10]),
         ([1, 1, 1, 1, 1], [1, 2, 3, 4, 5]),
         ([3, 1, 2, 10, 1], [3, 4, 6, 16, 17]),
         ([5], [5])]

for nums, expected in cases:
    assert running_sum_py(nums) == expected
    assert running_sum_naive(nums) == expected
    assert running_sum_stdlib(nums) == expected
    assert np.array_equal(running_sum_np(nums), expected)

print("LC 1480 pass")
print("input       : [3, 1, 2, 10, 1]")
print("pure python :", running_sum_py([3, 1, 2, 10, 1]))
print("numpy       :", running_sum_np([3, 1, 2, 10, 1]))

# cumsum se ek bonus: kisi bhi range ka sum O(1) me
c = np.cumsum([3, 1, 2, 10, 1])
print("\\nindex 1..3 ka sum =", c[3] - c[0], "(= 1+2+10)")
"""))

A(md("""
### LC 1512. Number of Good Pairs — Easy

https://leetcode.com/problems/number-of-good-pairs/

**Bayan:** Aisi jorion `(i, j)` ki ginti karo jahan `i < j` **aur** `nums[i] == nums[j]`.

**Approach (ye asli sikhne wali baat hai):**
1. **Brute force O(n²):** har jori check karo. Chhote input par chal jayega.
2. **Optimal O(n) — counting:** har value ki frequency ginno. Agar koi value `c`
   baar aayi hai to us value se banne wali jorian `c * (c - 1) / 2` hain
   (yaani "c me se 2 chuno" = nC2). Sab values ka total jama kar do.
3. **NumPy:** `np.bincount(a)` se frequencies, phir `(c * (c - 1) // 2).sum()` —
   poora hisaab bina kisi Python loop ke.

**Complexity:** brute force **O(n²)/O(1)**; counting **O(n + k)** time, **O(k)** space
(k = distinct values). NumPy version bhi O(n + k) magar constant factor bohat chhota.
"""))

A(code("""
from collections import Counter


def num_identical_pairs_brute(nums):
    \"\"\"(a1) BRUTE FORCE O(n^2) -- pehla jawab jo zehen me aata hai.\"\"\"
    count = 0
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):        # j hamesha i se aage -> i < j guarantee
            if nums[i] == nums[j]:
                count += 1
    return count


def num_identical_pairs_py(nums):
    \"\"\"(a2) OPTIMAL PURE PYTHON O(n) -- interview me yehi likho.\"\"\"
    seen = {}                            # value -> ab tak kitni baar dikhi
    count = 0
    for x in nums:
        # Jo pehle dikh chuki hain, un sab ke sath ye element ek nayi jori banata hai
        count += seen.get(x, 0)
        seen[x] = seen.get(x, 0) + 1
    return count


def num_identical_pairs_formula(nums):
    \"\"\"(a3) nC2 formula ke sath -- Counter se frequencies.\"\"\"
    return sum(c * (c - 1) // 2 for c in Counter(nums).values())


def num_identical_pairs_np(nums):
    \"\"\"(b) NUMPY -- bincount + nC2, bilkul loop-free.\"\"\"
    a = np.asarray(nums)
    counts = np.bincount(a)                       # index = value, value = frequency
    pairs = counts * (counts - 1) // 2            # har value ke liye nC2 (vectorized)
    return int(pairs.sum())                       # int() se Python int mila


# --- Tests ---
cases = [([1, 2, 3, 1, 1, 3], 4),
         ([1, 1, 1, 1], 6),                       # 4C2 = 6
         ([1, 2, 3], 0),
         ([2, 2, 3, 3, 3], 1 + 3)]                # 2C2=1, 3C2=3

for nums, expected in cases:
    assert num_identical_pairs_brute(nums) == expected
    assert num_identical_pairs_py(nums) == expected
    assert num_identical_pairs_formula(nums) == expected
    assert num_identical_pairs_np(nums) == expected

print("LC 1512 pass")
print("nums = [1, 2, 3, 1, 1, 3] -> good pairs =", num_identical_pairs_py([1, 2, 3, 1, 1, 3]))

# bincount ka andar ka kaam dekho
a = np.array([1, 2, 3, 1, 1, 3])
print("\\nbincount   :", np.bincount(a), "(index 1 -> 3 baar, index 3 -> 2 baar)")
print("nC2 per val:", np.bincount(a) * (np.bincount(a) - 1) // 2)
print("total      :", (np.bincount(a) * (np.bincount(a) - 1) // 2).sum())

# GOTCHA: bincount sirf non-negative integers par chalta hai
try:
    np.bincount(np.array([-1, 2]))
except ValueError as e:
    print("\\nnegative values -> ValueError:", str(e)[:50], "...")
print("Negative ya non-integer data ho to np.unique(a, return_counts=True) use karo.")
"""))

# ---------------------------------------------------------------- interview
A(md("""
## 16. Interview Questions & Answers

**Q1. NumPy Python list se tez kyun hai?**
Teen wajah: (1) data **contiguous memory** me hai (CPU cache friendly),
(2) **fixed dtype** hai to per-element type check nahi karna parta,
(3) loop **C me compiled** chalta hai (vectorization + SIMD), Python interpreter ka
per-element overhead khatam.

**Q2. `ndarray` aur `list` me buniyadi farq?**
`ndarray`: fixed dtype, fixed size, contiguous, vectorized math, kam memory.
`list`: mixed types, dynamic size (append sasta), pointers ka array, math ke liye loop chahiye.

**Q3. `arr.shape`, `arr.size`, `arr.ndim` me farq?**
`shape` = tuple of dimensions `(3, 4)`; `size` = total elements `12`;
`ndim` = dimensions ki ginti `2` = `len(shape)`.

**Q4. `dtype` kyun ahem hai?**
Memory (`nbytes = size * itemsize`), value **range** (overflow ka khatra), aur
**precision** decide karta hai. ML me `float32` par shift karke aadhi memory bachti hai.

**Q5. `np.zeros` aur `np.empty` me farq — kaunsa kab?**
`zeros` memory allocate karke sab 0 likhta hai. `empty` sirf allocate karta hai —
andar purana **garbage** hota hai, isliye tez hai. `empty` sirf tab jab tum foran
poora array khud bharne wale ho.

**Q6. `np.arange` aur `np.linspace` me farq?**
`arange(start, stop, step)` — `stop` **shamil nahi**, step batate ho.
`linspace(start, stop, num)` — `stop` **shamil** hai, points ki ginti batate ho.
Float steps ke liye hamesha `linspace` (arange me floating-point error se count badal jata hai).

**Q7. `np.array` vs `np.asarray`?**
`array` hamesha copy banata hai; `asarray` agar input pehle se matching ndarray ho to
**wahi object** wapas deta hai. Function ke andar input normalize karne ke liye
`asarray` behtar (bekar copy nahi banti).

**Q8. `nan` ko compare kyun nahi kar sakte?**
IEEE-754 me NaN "unordered" hai — `nan == nan` bhi `False`. Isliye `np.isnan()`
(ya `np.isfinite()`) use karte hain. `np.isclose(a, b, equal_nan=True)` me nan ko
barabar mana ja sakta hai.

**Q9. `nan` wale data ke aggregations kaise karein?**
nan-safe versions: `np.nansum`, `np.nanmean`, `np.nanstd`, `np.nanmax`, `np.nanargmax`,
`np.nanmedian`. Ya pehle `arr[np.isfinite(arr)]` se filter kar lo.

**Q10. Integer overflow NumPy me kya hota hai?**
Fixed-width integer wrap around karta hai (`int8`: 127 + 1 → -128) sirf ek
`RuntimeWarning` ke sath — koi exception nahi. `uint8` images me ye aam bug hai.
Hal: pehle bara dtype (`int16`) me cast karo, `np.clip` lagao, phir wapas `uint8`.

**Q11. `astype` copy banata hai ya view?**
Hamesha **naya array (copy)** — chahe dtype same ho (unless `copy=False` do aur
conversion ki zaroorat na ho). Aur ye truncate karta hai, round nahi.

**Q12. `np.random.seed()` vs `np.random.default_rng()`?**
`seed()` legacy **global** state badalta hai — library code me khatarnaak (kisi doosre
module ka randomness bhi badal jata hai). `default_rng(seed)` ek **independent
Generator** deta hai; naye code me yehi standard hai.

**Q13. 0-d array aur scalar me farq?**
`np.array(5)` 0-d array hai (`shape ()`, `ndim 0`) — index nahi kar sakte, magar
`.item()` se Python scalar milta hai. Aggregations NumPy scalar dete hain
(`np.int64(6)`), jo Python int ki tarah behave karta hai magar `isinstance(x, int)`
`False` deta hai.

**Q14. `arr.nbytes` kaise calculate hota hai? Ek misaal do.**
`nbytes = size * itemsize`. `(1000, 1000)` ka `float64` → `1_000_000 * 8` = 8 MB.
`float32` karne par 4 MB.

**Q15. Contiguous memory ka matlab kya hai aur kyun ahem hai?**
Sab elements RAM me ek laga tar block me hain. CPU cache lines poori bhar kar aati
hain → next element pehle se cache me hota hai → bohat tez. C-order (row-major)
me last axis fastest badalta hai; F-order (column-major) me first axis.

**Q16. `np.eye` aur `np.identity` me farq?**
`identity(n)` sirf square identity. `eye(N, M, k)` non-square aur shifted diagonal
(`k`) bhi bana sakta hai — zyada flexible.

**Q17. `np.array([1, 2, "3"])` ka dtype kya hoga aur kyun?**
`<U21` (unicode string). ndarray homogeneous hai, aur int + str ka common type
string hai — isliye numbers bhi string ban jate hain. Ye chupa hua bug ban sakta hai.
"""))

# ---------------------------------------------------------------- exercises
A(md("""
## 17. Practice Exercises (khud karo)

Solutions na dekho — pehle khud likho, phir check karo.

1. **Vector banao:** 10 se 100 tak ke wo numbers jo 7 ke multiple hon, ek 1D array me.
   *Hint:* `np.arange` with step.

2. **Memory calculator:** ek function `mem_mb(shape, dtype)` likho jo bina array banaye
   MB me size return kare.
   *Hint:* `np.dtype(dtype).itemsize` aur `math.prod(shape)`.

3. **Identity + border:** `5x5` array banao jisme diagonal 1 ho aur bahar ka border 9,
   baqi 0. *Hint:* `np.eye`, phir `arr[0, :]` / `arr[:, -1]` par assignment.

4. **Overflow proof:** ek `uint8` array banao aur dikhao ke `+ 60` karne par kaunse
   pixels wrap hue; phir safe version likho jo `np.clip` se 255 par ruk jaye.

5. **Dice simulation:** `default_rng(0)` se 1000 dice rolls (1..6) banao aur
   `np.bincount` se har face ki frequency print karo. Kya sab ~166 ke aas paas hain?

6. **linspace vs arange:** dikhao ke `np.arange(0, 2, 0.2)` aur `np.linspace(0, 2, 11)`
   me kya farq hai (size aur aakhri element).

7. **NaN cleaner:** ek function `clean(arr)` likho jo nan/inf hata kar sirf finite
   values return kare, aur sath me batayein kitne remove hue.
   *Hint:* `np.isfinite`.

8. **dtype detective:** in sab ka dtype **pehle guess karo** phir check karo:
   `np.array([1, 2])`, `np.array([1, 2.0])`, `np.array([True, 1])`,
   `np.array([1, None])`, `np.zeros(2)`, `np.arange(2)`.

9. **Meshgrid distance:** `np.meshgrid` se `5x5` grid banao aur har point ka
   origin `(0,0)` se distance nikalo. *Hint:* `np.sqrt(XX**2 + YY**2)`.

10. **Reproducibility test:** do functions likho jo random data banate hain — ek
    seed ke sath, ek bina. Dono ko 2 baar chala kar farq dikhao.
"""))

# ---------------------------------------------------------------- summary
A(md("""
## 18. Summary / Cheat-sheet

### Import & inspect
```python
import numpy as np
np.__version__
arr.ndim, arr.shape, arr.size, arr.dtype, arr.itemsize, arr.nbytes, arr.T
arr.flags, arr.strides
```

### Creation
| Kaam | Code |
|---|---|
| list se | `np.array([1,2,3])` |
| sab 0 / 1 / v | `np.zeros(s)`, `np.ones(s)`, `np.full(s, v)` |
| uninitialized (tez) | `np.empty(s)` — **garbage** |
| kisi jaisa | `np.zeros_like(a)`, `np.ones_like(a)`, `np.full_like(a, v)` |
| identity | `np.eye(n)`, `np.identity(n)` |
| diagonal | `np.diag([1,2,3])`, `np.diag(M)` |
| range (int step) | `np.arange(0, 10, 2)` — `stop` **NAHI** |
| n points | `np.linspace(0, 1, 11)` — `stop` **HAAN** |
| log scale | `np.logspace(-5, -1, 5)`, `np.geomspace(1, 1000, 4)` |
| formula se | `np.fromfunction(lambda i,j: i+j, (3,3), dtype=int)` |
| generator se | `np.fromiter(gen, dtype=int)` |
| grid | `np.meshgrid(x, y)` |

### dtypes
```
int8/16/32/64, uint8/16/32/64, float16/32/64, bool_, complex64/128, <U<n>, S<n>, object
np.iinfo(np.int8).max   # 127
np.finfo(np.float64).eps
arr.astype(np.float32)  # COPY, truncates (round nahi)
np.can_cast(a, b, casting='safe')
np.result_type(np.int32, np.float32)
nbytes = size * itemsize
```

### Random (modern)
```python
rng = np.random.default_rng(42)       # seed = reproducible
rng.integers(0, 10, 5)                # high shamil nahi
rng.random(5); rng.uniform(-1, 1, 5); rng.normal(mu, sd, 5)
rng.choice(a, k, replace=False, p=probs)
rng.shuffle(a)        # IN-PLACE, None return
rng.permutation(a)    # COPY
```

### nan / inf
```python
np.nan != np.nan            # True  <- isliye isnan use karo
np.isnan(a); np.isinf(a); np.isfinite(a)
np.nansum/nanmean/nanstd/nanmax/nanargmax/nanmedian
a[np.isfinite(a)]          # saaf data
```

### Printing
```python
with np.printoptions(precision=3, suppress=True):
    print(a)
np.set_printoptions(precision=8, suppress=False)   # reset
```

### Top gotchas (yaad rakho)
| Galti | Sahi |
|---|---|
| `arr.shape()` | `arr.shape` |
| `np.zeros(3)` int samajhna | `np.zeros(3, dtype=int)` |
| float step `arange` | `linspace` |
| `nan == nan` | `np.isnan(x)` |
| `sum(np_arr)` | `np_arr.sum()` |
| `np.array(x, copy=False)` | `np.asarray(x)` |
| `astype(int)` se rounding | `np.round(x).astype(int)` |
| `uint8` par seedha `+ 50` | `np.clip(x.astype(np.int16) + 50, 0, 255).astype(np.uint8)` |

### Aage kya
- **NB 02** — Indexing, Slicing, Views vs Copies, Reshaping, Joining
- **NB 03** — Operations, Broadcasting, Aggregations
- **NB 04** — 30+ Practice Problems + Interview prep
"""))

save(r"Numpy/Basics/01_Numpy_Introduction_Arrays_and_Creation.ipynb", CELLS)



