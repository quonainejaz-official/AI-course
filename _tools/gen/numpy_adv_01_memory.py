"""Generator: Numpy/Advance/01_Memory_Strides_Views_aur_Internals.ipynb

Chalao (ROOT se):  python _tools/gen/numpy_adv_01_memory.py
"""

import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

C: list = []
A = C.append

A(md("""
# NumPy Advance 01 — Memory, Strides, Views aur Internals

**Level:** Advance | **Prerequisites:** NumPy basics (array banana, indexing, slicing, dtype, broadcasting ki basic samajh)

Ab tak tum NumPy ko "fast arrays" ki tarah use karte the. Is notebook me hum **bonnet khol kar**
dekhenge ke andar asal me kya ho raha hai — array RAM me kaise pada hota hai, `strides` kya bala hai,
"view" aur "copy" ka farq kahan se aata hai, aur wo saare bugs jo isi cheez ko na samajhne se paida hote hain.

Ye wo notebook hai jo tumhe "NumPy user" se "NumPy engineer" banata hai. Interviews me senior roles par
yehi cheezein poochi jati hain.

## Is notebook me kya seekhenge

- **ndarray ki anatomy** — data buffer + dtype + shape + strides + flags (4 alag cheezein, ek object)
- `__array_interface__` — wo raw dictionary jo array ka poora memory description deti hai
- **C-order vs F-order** (row-major vs column-major) — text diagrams ke sath
- **Strides ka hisaab** haath se — `itemsize` se stride kaise banta hai, aur byte offset ka formula
- `arr.flags` — `C_CONTIGUOUS`, `F_CONTIGUOUS`, `OWNDATA`, `WRITEABLE`, `ALIGNED`
- **View banane wale** operations (slicing, reshape jab possible ho, transpose, `view()`) vs
  **copy banane wale** (fancy indexing, boolean mask, `astype`, non-contiguous par `ravel`)
- `.base` ka jhoot, aur `np.shares_memory` / `np.may_share_memory` ka sach
- Transpose ke baad `reshape` **kyun copy** karta hai
- `ascontiguousarray` / `asfortranarray` — layout theek karna
- **Memory layout ka speed par asar** (asli benchmark, ratta nahi)
- **Stride tricks:** `as_strided` (khatarnaak) aur `sliding_window_view` (safe) — moving average,
  2D patch extraction, **im2col** for convolution
- `np.broadcast_to` / `np.broadcast_arrays` — stride-0 ka jadoo, memory bachana
- `np.newaxis` vs `reshape`
- **dtype `view()` tricks** — float ki bits ko int me dekhna, structured to unstructured, alignment rules
- **Byte order / endianness** — `>i4`, `byteswap`
- **Buffer protocol** — `np.frombuffer`, `tobytes`, `memoryview`
- `nbytes` vs asli memory, `np.empty` + in-place fill, `out=` parameters, allocator ka zikr
- `np.memmap` — RAM se bari files (out-of-core) par kaam
- NumPy me **copy-on-write nahi hota**, `setflags`, accidental mutation bugs
- Alignment aur SIMD ka zikr
- **LeetCode:** LC 48, LC 73, LC 289, LC 643 (pure-Python + vectorized NumPy dono)

> **Yaad rakho:** is notebook ka asal maqsad ye hai ke tum har array par sochna shuru karo:
> *"iska data kahan hai, kaun owner hai, aur agar main isay badlun to kaun kaun mutasir hoga?"*
"""))

A(code("""
# Setup — sab imports aik jagah
import numpy as np
import sys
import time
import tempfile
import os

print("numpy version :", np.__version__)
print("python version:", sys.version.split()[0])

# Reproducibility ke liye modern Generator API (np.random.seed purana tareeqa hai)
rng = np.random.default_rng(42)

# Printing ko qabu me rakhne ke liye
np.set_printoptions(precision=4, suppress=True, linewidth=100)


def bench(fn, repeats=5):
    \"\"\"Chhota timing helper: kaam ko kai dafa chala kar SAB SE TEZ (min) waqt deta hai.

    min kyun, average kyun nahi? Kyun ke machine par doosre programs bhi chal rahe hote hain;
    wo sirf SLOW kar sakte hain, fast nahi. Isliye min asli capability ke sab se qareeb hota hai.
    \"\"\"
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    return min(times) * 1000  # milliseconds me
"""))

A(md("""
## 1. ndarray ki anatomy — ek array asal me 4 cheezon ka joR hai

Log samajhte hain ke NumPy array "numbers ki list" hai. Ghalat. Ek `ndarray` object asal me ye
rakhta hai:

| Hissa | Kya hai | Misaal |
|---|---|---|
| **data buffer** | RAM ka ek lamba, flat, contiguous byte block. Bas bytes — isay shape ka koi ilm nahi. | 48 bytes |
| **dtype** | Un bytes ko kaise parhna hai (kitne bytes per element, integer/float, byte order) | `float64` (8 bytes) |
| **shape** | Logical dimensions ka tuple | `(2, 3)` |
| **strides** | Har axis me **ek qadam** aage jaane ke liye kitne **bytes** chhalaang lagani hai | `(24, 8)` |
| **flags** | Metadata: contiguous hai? owner hai? writeable hai? | `C_CONTIGUOUS=True` |

**Ye insight sab kuch kholta hai:** data buffer ek hi rehta hai, magar (shape, strides, dtype) badal kar
tum **usi memory** ko bilkul mukhtalif shakal me dekh sakte ho — **bina ek byte copy kiye**. Yehi "view" hai.
Yehi wajah hai ke `arr.T` (transpose) ek 10 GB array par bhi instant hota hai: sirf strides ulat diye,
data ko haath bhi nahi lagaya.

**Kyun / kahan use hota hai:** slicing, transpose, reshape, broadcasting, `sliding_window_view` — NumPy ki
saari "muft" (zero-copy) cheezein isi 4-part design se aati hain.
"""))

A(code("""
# Ek simple 2x3 float array — iske chaaron hisse dekhte hain
arr = np.array([[1.0, 2.0, 3.0],
                [4.0, 5.0, 6.0]])

print("array:")
print(arr)
print()
print("shape     :", arr.shape)       # logical dimensions
print("dtype     :", arr.dtype)       # bytes ko kaise parhna hai
print("itemsize  :", arr.itemsize)    # ek element kitne bytes = float64 -> 8
print("strides   :", arr.strides)     # (bytes per row-step, bytes per column-step)
print("nbytes    :", arr.nbytes)      # 6 elements * 8 bytes = 48
print("ndim      :", arr.ndim)
print()
# Data buffer ka asli memory address (machine par har dafa badlega -> sirf print, assert NAHI)
print("data pointer (address):", arr.__array_interface__["data"][0])
print()
print("flags:")
print(arr.flags)

# nbytes deterministic hai -> is par assert kar sakte hain
assert arr.nbytes == arr.size * arr.itemsize == 48
"""))

A(md("""
### Output ka matlab

- `strides == (24, 8)`: **agli row** par jaane ke liye 24 bytes aage jao (3 elements x 8 bytes),
  **agle column** par jaane ke liye sirf 8 bytes (1 element). Yaani row ke elements RAM me **bilkul
  bagal bagal** pade hain.
- `nbytes == 48` sirf **data** ke bytes hain — Python object ka overhead (header, shape tuple waghera)
  isme shamil nahi. Wo `sys.getsizeof` me dikhta hai.
- `data pointer` = buffer ka pehla byte kahan hai. Har run par badlega, isliye is par **kabhi assert na karo**.

### Interview tip
> *"NumPy array me kya hota hai?"* — Jawab: **pointer to a data buffer + dtype + shape + strides + flags**.
> Ye 5 lafz bol dena tumhe 90% candidates se aage kar deta hai.
"""))

A(md("""
## 2. `__array_interface__` — array ka "birth certificate"

**Kya hai:** ek dictionary jo array ka poora memory-level description deti hai. Ye ek **protocol** hai
(sirf NumPy ki cheez nahi) — isi ke zariye doosri libraries (Pillow, PyTorch, Numba) NumPy array ki
memory ko **bina copy** samajh leti hain.

**Keys:**
- `data`: `(address, read_only_flag)`
- `shape`, `strides` (agar `None` ho to matlab **C-contiguous** hai)
- `typestr`: dtype ka compact code — `'<f8'` = little-endian float 8-byte
- `descr`, `version`

**Kyun use hota hai:** zero-copy interop. Jab tum `torch.from_numpy(a)` karte ho, andar yehi
buffer information istemal hoti hai.
"""))

A(code("""
# __array_interface__ dekhte hain — pehle contiguous array par
ai = arr.__array_interface__
for k in sorted(ai):
    print(f"{k:9} : {ai[k]}")

print()
# GOTCHA: contiguous array me 'strides' None hota hai (matlab: default C-order strides)
print("contiguous array ka strides field :", ai["strides"], " <- None = C-contiguous")

# Ab ek non-contiguous view (har doosra column) par
sliced = arr[:, ::2]
print("sliced shape                      :", sliced.shape)
print("sliced ka strides field           :", sliced.__array_interface__["strides"], " <- ab asli strides")

# typestr ka matlab: '<' = little-endian, 'f' = float, '8' = 8 bytes
print("typestr                           :", ai["typestr"])
assert ai["typestr"] in ("<f8", ">f8")   # machine ke endianness par depend
assert ai["shape"] == (2, 3)
"""))

A(md("""
## 3. C-order vs F-order — row-major aur column-major

**Kya hai:** 2D (ya N-D) array ko 1D memory me rakhne ke do tareeqe hain.

Maan lo ye matrix hai:

```
        col0  col1  col2
row0 [   1     2     3  ]
row1 [   4     5     6  ]
```

**C-order (row-major)** — NumPy ka default. Rows ek ke baad ek:

```
memory:  [ 1 | 2 | 3 | 4 | 5 | 6 ]
byte  :    0   8  16  24  32  40
           ^-- row0 --^   ^-- row1 --^
strides = (24, 8)   # row jump = 24 bytes, col jump = 8 bytes
```

**F-order (column-major)** — Fortran/MATLAB/R ka tareeqa. Columns ek ke baad ek:

```
memory:  [ 1 | 4 | 2 | 5 | 3 | 6 ]
byte  :    0   8  16  24  32  40
           ^col0^   ^col1^   ^col2^
strides = (8, 24)   # row jump = 8 bytes, col jump = 24 bytes
```

**Gaur karo:** dono me **wohi 6 numbers** hain, wohi shape hai — sirf **strides ulte** hain.
`ravel()` / `flatten()` ka output isi wajah se order par depend karta hai.

**Kyun ahem hai:** speed. Jo loop memory me **aage aage seedha** chalta hai wo CPU cache ka faida uthata hai.
Ghalat layout par wohi kaam 2-3 guna slow ho sakta hai (neeche asli benchmark hai).
"""))

A(code("""
# Wohi data, do layouts
c_arr = np.array([[1.0, 2, 3], [4, 5, 6]], order="C")   # row-major (default)
f_arr = np.array([[1.0, 2, 3], [4, 5, 6]], order="F")   # column-major

print("c_arr strides:", c_arr.strides, "| f_arr strides:", f_arr.strides)
print()

# Memory me asal tarteeb dekhne ka tareeqa: ravel(order='K') = "jaisa memory me pada hai"
print("C-order memory me:", c_arr.ravel(order="K"))   # 1 2 3 4 5 6
print("F-order memory me:", f_arr.ravel(order="K"))   # 1 4 2 5 3 6
print()

# Logically dono BARABAR hain — layout logic ko badalta nahi
print("dono arrays equal?", np.array_equal(c_arr, f_arr))
print()
print("c_arr flags: C_CONTIGUOUS =", c_arr.flags["C_CONTIGUOUS"], "| F_CONTIGUOUS =", c_arr.flags["F_CONTIGUOUS"])
print("f_arr flags: C_CONTIGUOUS =", f_arr.flags["C_CONTIGUOUS"], "| F_CONTIGUOUS =", f_arr.flags["F_CONTIGUOUS"])

assert c_arr.strides == (24, 8)
assert f_arr.strides == (8, 24)
assert np.array_equal(c_arr, f_arr)          # values same
assert not np.array_equal(c_arr.ravel(order="K"), f_arr.ravel(order="K"))  # memory order different
"""))

A(md("""
### 1D array ka maza

Ek 1D array **dono** C-contiguous aur F-contiguous hota hai (kyun ke ek hi axis hai, koi farq nahi banta).
Isi tarah scalar-jaisa `shape == (1,1)` array bhi dono flags True rakhta hai. Interview me ye chhota
sa trick question aata hai.
"""))

A(code("""
# 1D array dono flags True rakhta hai
one_d = np.arange(5)
print("1D  -> C:", one_d.flags["C_CONTIGUOUS"], "F:", one_d.flags["F_CONTIGUOUS"])

# (1,1) shape bhi dono
tiny = np.ones((1, 1))
print("(1,1) -> C:", tiny.flags["C_CONTIGUOUS"], "F:", tiny.flags["F_CONTIGUOUS"])

# Aur ek khali array bhi
empty = np.ones((0, 3))
print("(0,3) -> C:", empty.flags["C_CONTIGUOUS"], "F:", empty.flags["F_CONTIGUOUS"])

assert one_d.flags["C_CONTIGUOUS"] and one_d.flags["F_CONTIGUOUS"]
assert tiny.flags["C_CONTIGUOUS"] and tiny.flags["F_CONTIGUOUS"]
"""))

A(md("""
## 4. Strides ka hisaab — haath se nikalte hain

**Formula (C-order):** aakhri axis ka stride = `itemsize`. Us se pehle wale axis ka stride =
`agle axis ka stride x agle axis ki length`.

Yaani shape `(d0, d1, d2)` aur itemsize `s` ke liye:

```
strides[2] = s
strides[1] = s * d2
strides[0] = s * d2 * d1
```

**Byte offset ka formula** — element `[i, j, k]` buffer me kahan hai:

```
offset = i*strides[0] + j*strides[1] + k*strides[2]
```

Bas! NumPy ka indexing asal me yehi ek line ka hisaab hai. Isi liye ye itna tez hai —
koi search nahi, seedha address calculation.
"""))

A(code("""
# 3D array par formula khud verify karte hain
a3 = np.arange(24, dtype=np.int32).reshape(2, 3, 4)   # itemsize = 4 bytes
s = a3.itemsize
d0, d1, d2 = a3.shape

# Formula se strides banao
expected = (s * d2 * d1, s * d2, s)
print("shape          :", a3.shape)
print("itemsize       :", s)
print("hisaab se       :", expected)
print("numpy ka actual :", a3.strides)
assert a3.strides == expected      # formula bilkul theek hai

print()
# Ab byte offset ka formula verify karte hain
i, j, k = 1, 2, 3
offset = i * a3.strides[0] + j * a3.strides[1] + k * a3.strides[2]
print(f"element [{i},{j},{k}] ka byte offset =", offset)

# Buffer me us offset par jo pada hai wo nikal kar compare karo
raw = a3.tobytes()   # C-order bytes (a3 C-contiguous hai to ye buffer ki asli copy hai)
value_at_offset = np.frombuffer(raw, dtype=a3.dtype, count=1, offset=offset)[0]

print("us offset par value          :", value_at_offset)
print("a3[1,2,3] (normal indexing)  :", a3[i, j, k])
assert value_at_offset == a3[i, j, k] == 23
print()
print("Matlab: indexing = pointer + (index . strides) ka dot product. Bas itna hi jadoo hai.")
"""))

A(md("""
### Slicing strides ko kaise chhedti hai

- `a[::2]` — stride **double** ho jata hai (ek element chhodo), shape aadha
- `a[::-1]` — stride **negative** ho jata hai (ulta chalo), aur data pointer aakhir par shift hota hai
- `a[1:]` — stride wohi, bas pointer aage khisak jata hai

Yaani slicing kabhi copy nahi karti — sirf (pointer, shape, strides) ka naya set banati hai. **Muft.**
"""))

A(code("""
base = np.arange(10, dtype=np.int64)   # itemsize 8
print("base    strides:", base.strides, "shape:", base.shape)

step2 = base[::2]
print("[::2]   strides:", step2.strides, "shape:", step2.shape, "->", step2)

rev = base[::-1]
print("[::-1]  strides:", rev.strides, "shape:", rev.shape, "->", rev, "  <- NEGATIVE stride!")

off = base[3:]
print("[3:]    strides:", off.strides, "shape:", off.shape, "->", off)

print()
# Reverse view ka data pointer aakhri element par hota hai
print("base ka pointer :", base.__array_interface__["data"][0])
print("rev  ka pointer :", rev.__array_interface__["data"][0], " <- 72 bytes aage (9*8)")

assert step2.strides == (16,)      # 2 * 8
assert rev.strides == (-8,)        # ulta
assert off.strides == (8,)         # wohi stride
# Teeno VIEWS hain -> base ke sath memory share karte hain
assert np.shares_memory(base, step2) and np.shares_memory(base, rev) and np.shares_memory(base, off)
"""))

A(md("""
## 5. `arr.flags` — array ke 5 ahem sach

| Flag | Matlab | Kab False hota hai |
|---|---|---|
| `C_CONTIGUOUS` | memory me row-major, bilkul lagatar (koi gap nahi) | slicing with step, transpose |
| `F_CONTIGUOUS` | memory me column-major, lagatar | aam C arrays me |
| `OWNDATA` | ye array **khud** buffer ka malik hai (isay free karega) | har view me False |
| `WRITEABLE` | isme likhna allowed hai | `broadcast_to`, `frombuffer(bytes)`, `setflags(write=False)` |
| `ALIGNED` | data pointer dtype ke natural boundary par hai (CPU ke liye tez) | kuch raw-buffer/struct cases me |

**Kyun ahem hai:**
- `C_CONTIGUOUS` — bohat se fast paths (BLAS calls, `reshape` without copy, `view()` dtype change)
  sirf contiguous array par hi chalte hain. Non-contiguous ho to NumPy **chupke se copy** bana leta hai.
- `OWNDATA` — ye batata hai ke tumhare paas view hai ya asli array. Debugging me sona.
- `WRITEABLE` — read-only array par likhne ki koshish `ValueError` deti hai (aur ye achi baat hai).
"""))

A(code("""
def show_flags(name, a):
    \"\"\"Ek line me sab ahem flags print karta hai — comparison ke liye behtareen.\"\"\"
    f = a.flags
    print(f"{name:22} C={int(f['C_CONTIGUOUS'])} F={int(f['F_CONTIGUOUS'])} "
          f"OWN={int(f['OWNDATA'])} WRITE={int(f['WRITEABLE'])} ALIGN={int(f['ALIGNED'])} "
          f"strides={a.strides}")


m = np.arange(12, dtype=np.float64).reshape(3, 4)

show_flags("original (3,4)", m)
show_flags("m.T (transpose)", m.T)              # C toot jata hai, F ban jata hai
show_flags("m[:, ::2] (step)", m[:, ::2])       # dono contiguous nahi
show_flags("m[1:3] (row slice)", m[1:3])        # C-contiguous rehta hai! (poori rows)
show_flags("m.copy()", m.copy())                # naya owner
show_flags("m.ravel()", m.ravel())              # 1D -> C aur F dono
show_flags("np.asfortranarray(m)", np.asfortranarray(m))

print()
# Row-slice contiguous rehti hai magar column-slice nahi — kyun?
print("m[1:3] contiguous hai kyun ke poori rows lay rahe hain (memory ka lagatar tukra).")
print("m[:, 1:3] contiguous NAHI kyun ke har row se sirf beech ka hissa -> gaps par gaps.")
show_flags("m[:, 1:3]", m[:, 1:3])

assert m.flags["C_CONTIGUOUS"] and not m.flags["F_CONTIGUOUS"]
assert m.T.flags["F_CONTIGUOUS"] and not m.T.flags["C_CONTIGUOUS"]
assert m.flags["OWNDATA"] and not m.T.flags["OWNDATA"]      # transpose ek view hai
assert m[1:3].flags["C_CONTIGUOUS"]                          # row slice -> contiguous
assert not m[:, 1:3].flags["C_CONTIGUOUS"]                   # column slice -> nahi
"""))

A(md("""
## 6. View vs Copy — NumPy ka sab se bara "yahan log phaste hain"

Ye **sab se important** section hai. Ek jumle me:

> **View** = wohi memory, naya (shape, strides) chashma. Sasta. Isay badla to **asli array bhi badal jayega**.
> **Copy** = nayi memory, data ki naqal. Mehnga. Isay badla to asli array **safe** rehta hai.

### Kaun view deta hai (zero-copy)
| Operation | View? | Note |
|---|---|---|
| basic slicing `a[1:5]`, `a[::2]` | **View** | hamesha |
| `a.T` / `a.transpose()` | **View** | sirf strides ulat gaye |
| `a.reshape(...)` | **View jab possible** | warna khamoshi se copy |
| `a.view(dtype)` | **View** | dtype ka chashma badla |
| `a.ravel()` | **View jab contiguous** | warna copy |
| `np.broadcast_to(a, shape)` | **View (read-only)** | stride-0 |
| `sliding_window_view` | **View (read-only)** | overlapping windows |
| `a[np.newaxis]` / `a[None]` | **View** | sirf shape me 1 ghusa |

### Kaun copy deta hai
| Operation | Copy? | Note |
|---|---|---|
| fancy/integer indexing `a[[0,2,4]]` | **Copy** | mangi hui tarteeb memory me maujood nahi ho sakti |
| boolean mask `a[a > 5]` | **Copy** | kitne elements aayenge, ye runtime par pata chalta hai |
| `a.astype(np.float32)` | **Copy** | naya dtype = naye bytes (default `copy=True`) |
| `a.flatten()` | **Copy** | hamesha! (`ravel` se yehi farq hai) |
| arithmetic `a + 1`, `a * 2` | **Copy** | naya result array |
| `np.concatenate`, `np.stack`, `np.tile` | **Copy** | nayi memory |

**Ek zabardast asaan rule:** agar NumPy tumhari mangi hui cheez ko **(pointer, shape, strides)** ke ek
set se bayan **nahi** kar sakta, to usay copy karna hi paRega. Fancy indexing `a[[0, 5, 2]]` ko koi
fixed stride bayan nahi kar sakta — isliye copy.
"""))

A(code("""
# --- VIEW ka demo: mutation asli array tak pohanchti hai ---
original = np.arange(10)
view = original[2:6]                 # basic slicing -> VIEW

print("pehle original :", original)
view[0] = 999                        # view me likha...
print("baad me original:", original, "  <- position 2 badal gayi!")

print()
print("shares_memory?", np.shares_memory(original, view))
print("view.base kaun hai? (original ka data)", view.base is original)
print("view OWNDATA:", view.flags["OWNDATA"])

assert original[2] == 999            # view ke zariye asli array badla
assert np.shares_memory(original, view)
assert not view.flags["OWNDATA"]
"""))

A(code("""
# --- COPY ka demo: mutation kahin nahi jati ---
original2 = np.arange(10)
copy_arr = original2[[2, 3, 4, 5]]   # FANCY indexing -> COPY (values wohi, memory nayi)

print("pehle original2 :", original2)
copy_arr[0] = 999                    # copy me likha...
print("baad me original2:", original2, "  <- kuch nahi badla (copy thi)")

print()
print("shares_memory?", np.shares_memory(original2, copy_arr))
print("copy OWNDATA   :", copy_arr.flags["OWNDATA"])

assert original2[2] == 2                                  # asli array safe raha
assert not np.shares_memory(original2, copy_arr)
assert copy_arr.flags["OWNDATA"]

print()
print("SAWAL: slicing aur fancy indexing dono 'a[...]' jaise dikhte hain,")
print("magar ek view deti hai aur doosri copy. Yehi silent bug ki jaR hai.")
"""))

A(code("""
# Ek hi array par saari operations chala kar dekhte hain: view ya copy?
src = np.arange(12, dtype=np.float64).reshape(3, 4)

ops = {
    "src[1:3]            (basic slice)": src[1:3],
    "src[:, ::2]         (step slice)": src[:, ::2],
    "src.T               (transpose)": src.T,
    "src.reshape(4, 3)   (reshape ok)": src.reshape(4, 3),
    "src.ravel()         (contig ravel)": src.ravel(),
    "src[None]           (newaxis)": src[None],
    "src.view(np.int64)  (dtype view)": src.view(np.int64),
    "src[[0, 2]]         (fancy idx)": src[[0, 2]],
    "src[src > 5]        (bool mask)": src[src > 5],
    "src.astype(np.float32)": src.astype(np.float32),
    "src.flatten()       (always copy)": src.flatten(),
    "src + 0             (arithmetic)": src + 0,
    "src.copy()": src.copy(),
    "np.tile(src, 2)": np.tile(src, 2),
}

print(f"{'operation':38} {'VIEW/COPY':10} OWNDATA")
print("-" * 62)
for label, result in ops.items():
    is_view = np.shares_memory(src, result)
    print(f"{label:38} {'VIEW' if is_view else 'COPY':10} {result.flags['OWNDATA']}")

# Ahem asserts
assert np.shares_memory(src, src[1:3])
assert np.shares_memory(src, src.T)
assert np.shares_memory(src, src.reshape(4, 3))
assert not np.shares_memory(src, src[[0, 2]])
assert not np.shares_memory(src, src[src > 5])
assert not np.shares_memory(src, src.flatten())
assert not np.shares_memory(src, src.astype(np.float32))
"""))

A(md("""
## 7. `.base` ka jhoot — aur `np.shares_memory` ka sach

**Kya hai:** `arr.base` un array ko point karta hai "jis se ye view bana". Log isay
"copy hai ya view" ka test samajhte hain:

```python
if arr.base is None:   # log samajhte hain: "matlab ye copy hai"
```

**Ye test GHALAT hai.** Kuch operations pehle andar hi andar ek copy banati hain, phir us copy ka
**view** wapas karti hain. Aise result ka `.base` `None` **nahi** hota — halan ke asli array se uska
koi taalluq nahi!

Sab se mashhoor misaal: `a.T.reshape(-1)`.

**Sahi tareeqa:** `np.shares_memory(a, b)` — ye asal me buffers ka overlap check karta hai.

| Function | Kya karta hai | Cost |
|---|---|---|
| `np.shares_memory(a, b)` | **exact** jawab (zaroorat par mehnga solver chalata hai) | slow ho sakta hai |
| `np.may_share_memory(a, b)` | tez, **conservative** — "ho sakta hai" bhi True keh deta hai | hamesha fast |

Yaani: `may_share_memory` ka `False` par bharosa karo (matlab bilkul share nahi karte).
Uske `True` par nahi (wo shak bhi True bolta hai).
"""))

A(code("""
# .base ka dhoka — ye cell zaroor samjho
a = np.arange(6).reshape(2, 3)
tricky = a.T.reshape(6)      # transpose ke baad reshape -> data copy karna paRa

print("a       :", a.tolist())
print("a.T     :", a.T.tolist())
print("a.T.reshape(6) :", tricky)
print()
print("tricky.base is None ?      ", tricky.base is None, "  <- False! matlab 'view lagta hai'")
print("np.shares_memory(a, tricky)?", np.shares_memory(a, tricky), "  <- False! matlab asal me COPY hai")
print()
print("Samjhao: reshape ko copy karni paRi, phir usi copy ka view wapas mila.")
print("Isliye .base None nahi hai -- magar a ke sath memory share NAHI hoti.")
print()

# Proof: tricky ko badlo, a par koi asar nahi
tricky[0] = 111
print("tricky badalne ke baad a:", a.tolist(), " <- bilkul mehfooz")

# SAHI test yehi hai:
assert not np.shares_memory(a, tricky)     # ye asli sach hai
assert tricky.base is not None             # aur .base yahan jhoot bol raha hai
assert a[0, 0] == 0                        # a bilkul nahi badla

print()
print("SABAQ: 'view ya copy' ka faisla HAMESHA np.shares_memory se karo, .base se kabhi nahi.")
"""))

A(code("""
# shares_memory vs may_share_memory
big = np.arange(100)
left = big[:50]
right = big[50:]        # ye do halve overlap NAHI karte

print("left aur right overlap karte hain?")
print("  np.shares_memory     :", np.shares_memory(left, right), " <- exact jawab: nahi")
print("  np.may_share_memory  :", np.may_share_memory(left, right), " <- conservative: 'ho sakta hai'")
print()
print("Wajah: may_share_memory sirf address RANGE dekhta hai (dono ek hi buffer me hain),")
print("       shares_memory asal me element-level overlap solve karta hai.")
print()

odd = big[1::2]
even = big[0::2]
print("odd aur even elements:")
print("  shares_memory    :", np.shares_memory(odd, even), " <- kabhi takra nahi sakte")
print("  may_share_memory :", np.may_share_memory(odd, even))

assert not np.shares_memory(left, right)
assert not np.shares_memory(odd, even)
# may_share_memory ka True mumkin hai -> is par assert na karo, sirf samjho
"""))

A(md("""
## 8. Transpose ke baad `reshape` kyun copy karta hai?

**Sawal:** `a.reshape(...)` to view deta hai. Phir `a.T.reshape(-1)` kyun copy karta hai?

**Jawab:** `reshape` ka waada ye hai ke elements **C-order (row-major) tarteeb** me nikal kar nayi shape
me bharay jayenge. Ye kaam **bina copy** sirf tab ho sakta hai jab wo tarteeb memory me **already
maujood** ho — yaani ek fixed stride pattern se mil jaye.

```
a       = [[0 1 2]      memory: 0 1 2 3 4 5   (C-contiguous)
           [3 4 5]]

a.T     = [[0 3]        memory wohi: 0 1 2 3 4 5
           [1 4]        magar strides ulte -> C-order padhne par 0,3,1,4,2,5 chahiye
           [2 5]]

a.T ko flat karne ke liye chahiye: 0 3 1 4 2 5
memory me maujood hai            : 0 1 2 3 4 5
```

`0 3 1 4 2 5` ko **koi bhi** single stride nahi bana sakta. Isliye NumPy ke paas do hi raste hain:
copy karo, ya error do. `reshape` **copy** karta hai (khamoshi se).

**Agar tum copy bardasht nahi kar sakte** to `a.reshape(shape)` ki jagah `arr.shape = ...` set karo —
ye copy zaroorat paRne par **error** deta hai. Ye ek behtareen defensive trick hai.
"""))

A(code("""
a = np.arange(6).reshape(2, 3)

# 1) Seedha reshape -> VIEW (kaam ban gaya bina copy)
r1 = a.reshape(3, 2)
print("a.reshape(3,2)      -> view?", np.shares_memory(a, r1))

# 2) Transpose ke baad reshape -> COPY (khamoshi se)
r2 = a.T.reshape(6)
print("a.T.reshape(6)      -> view?", np.shares_memory(a, r2), " <- COPY hui, koi warning nahi mili")

print()
# 3) Agar copy qabool NAHI: .shape assign karo -> copy ki zaroorat par error dega
t = a.T
try:
    t.shape = (6,)              # in-place shape change ki koshish
    print("shape assign ho gaya")
except AttributeError as e:
    print("AttributeError:", e)
    print("  ^ NumPy keh raha hai: 'bina copy ye shape mumkin nahi'. Ye GOOD hai --")
    print("    khamoshi se copy karne ke bajaye tumhe bata diya.")

print()
# 4) order='F' se bataya jaye to reshape view de sakta hai
r3 = a.T.reshape(6, order="F")   # F-order me padho -> 0 1 2 3 4 5 -> memory me maujood hai!
print("a.T.reshape(6, order='F') -> view?", np.shares_memory(a, r3), " ->", r3)

assert np.shares_memory(a, r1)
assert not np.shares_memory(a, r2)
assert np.shares_memory(a, r3)     # F-order padhne se copy bach gayi
"""))

A(md("""
## 9. `ascontiguousarray` / `asfortranarray` — layout theek karna

**Kya hai:** ye functions array ko maangi hui layout me laate hain. Agar array **pehle se** us layout
me hai to **kuch nahi karte** (wohi array wapas, zero cost). Warna copy banate hain.

**Kyun use hota hai:**
- Kisi C/Fortran library ko bhejne se pehle (wo contiguous buffer maangti hai)
- Bar bar chalne wale hot loop se pehle **ek dafa** layout theek kar lo — phir har iteration me
  NumPy ko chupke se copy nahi karni paRegi

**`asarray` family ka asal fayeda:** `np.ascontiguousarray(x)` likhna `if not x.flags[...]: x = x.copy()`
likhne se behtar hai — ye already-correct case me **muft** hai.
"""))

A(code("""
noncontig = np.arange(12, dtype=np.float64).reshape(3, 4)[:, ::2]   # non-contiguous view
print("noncontig C_CONTIGUOUS:", noncontig.flags["C_CONTIGUOUS"], "strides:", noncontig.strides)

fixed = np.ascontiguousarray(noncontig)        # copy banegi (majboori)
print("fixed     C_CONTIGUOUS:", fixed.flags["C_CONTIGUOUS"], "strides:", fixed.strides)
print("copy hui? ", not np.shares_memory(noncontig, fixed))

print()
# AHEM: already contiguous array par ye function MUFT hai (koi copy nahi)
already = np.arange(6, dtype=np.float64)
same = np.ascontiguousarray(already)
print("already contiguous par call kiya -> wohi array mila?", same is already)
print("(is se hot path me be-fikr call kar sakte ho)")

print()
f_version = np.asfortranarray(noncontig)
print("asfortranarray -> F_CONTIGUOUS:", f_version.flags["F_CONTIGUOUS"], "strides:", f_version.strides)

# Values kisi surat me nahi badalti — sirf layout badalta hai
assert np.array_equal(noncontig, fixed) and np.array_equal(noncontig, f_version)
assert fixed.flags["C_CONTIGUOUS"]
assert f_version.flags["F_CONTIGUOUS"]
assert same is already          # zero-cost fast path
"""))

A(md("""
## 10. Memory layout ka SPEED par asar — asli benchmark

Ab tak theory thi. Ab number dekhte hain.

**Kitaabi da'wa (jo aksar GHALAT hai):** "C-order me row-wise sum tez hota hai kyun ke rows contiguous hain."

**Asli haqeeqat (is machine par nap kar):** C-contiguous array par `sum(axis=0)` aksar `sum(axis=1)` se
**TEZ** nikalta hai! Wajah: `axis=0` par reduce karte hue NumPy ka inner loop memory me **seedha aage**
chalta hai aur natija ek **contiguous output vector** me jama karta hai — ye SIMD (vector instructions)
ke liye perfect hai. `axis=1` me har row ka jawab ek single scalar me sikuRta hai (horizontal reduction),
jo kam vector-friendly hai.

**To sabaq kya hai?** "row-wise vs column-wise" ratta lagana bekaar hai. Asli, qabil-e-bharosa qanoon ye hai:

> **Wohi operation, mukhtalif layout** par chala kar dekho. Jo layout tumhare access pattern se
> **mail khata** hai wo jeet jayega. Aur ye **naapo**, andaza na lagao.

Neeche hum yehi karte hain: ek hi `sum(axis=...)` C-order aur F-order dono par.
"""))

A(code("""
# Layout benchmark — wohi operation, do layouts. (Array ~11 MB, halka rakha hai)
N = 1200
c_big = rng.random((N, N))              # C-order (default)
f_big = np.asfortranarray(c_big)        # wohi data, F-order me

print(f"array shape {c_big.shape}, size = {c_big.nbytes / 1e6:.1f} MB")
print()

t_c0 = bench(lambda: c_big.sum(axis=0))
t_f0 = bench(lambda: f_big.sum(axis=0))
t_c1 = bench(lambda: c_big.sum(axis=1))
t_f1 = bench(lambda: f_big.sum(axis=1))

print(f"{'operation':22} {'C-order':>10} {'F-order':>10}   jeeta kaun")
print("-" * 60)
print(f"{'sum(axis=0)':22} {t_c0:9.2f}ms {t_f0:9.2f}ms   {'C-order' if t_c0 < t_f0 else 'F-order'}")
print(f"{'sum(axis=1)':22} {t_c1:9.2f}ms {t_f1:9.2f}ms   {'C-order' if t_c1 < t_f1 else 'F-order'}")
print()
print("Note: numbers har machine par mukhtalif honge. Dekhne wali cheez PATTERN hai:")
print("  ek layout ek axis par jeetti hai, doosri doosre axis par -- yehi 'layout matters' ka saboot.")
print()
print("Isi wajah se timing par ASSERT karna mana hai: ye machine, load aur cache par depend karta hai.")
"""))

A(code("""
# Strided (bikhra hua) copy vs contiguous copy — ye farq bohat qabil-e-bharosa hai
t_contig = bench(lambda: c_big.copy())        # seedha memcpy jaisa
t_strided = bench(lambda: c_big.T.copy())     # transpose ko materialize karna = bikhra access

print(f"contiguous copy (c_big.copy())   : {t_contig:7.2f} ms")
print(f"strided copy    (c_big.T.copy()) : {t_strided:7.2f} ms")
print(f"ratio                            : {t_strided / t_contig:5.2f}x slower (taqreeban)")
print()
print("Kyun: contiguous copy me CPU har cache line (64 bytes) ka poora faida uthata hai.")
print("Transpose copy me har naye element ke liye nayi cache line chhoni paRti hai -> cache miss.")
print()
print("PRACTICAL SABAQ: agar ek non-contiguous array par BOHAT kaam karna hai,")
print("to shuru me EK DAFA np.ascontiguousarray() kar lo. Us ek copy ki qeemat")
print("aage har operation ke fast hone se wasool ho jati hai.")
"""))

A(md("""
## 11. Stride tricks — `as_strided`: taqatwar, magar khatarnaak

**Kya hai:** `np.lib.stride_tricks.as_strided(arr, shape, strides)` tumhe array ka
(shape, strides) **khud** likhne deta hai. Ye NumPy ka sab se low-level, "safety off" tool hai.

**Kyun use hota hai:** overlapping windows (moving average), diagonal views, repeat-without-memory —
sab bina copy.

### KHATRAY (ye lazmi parho)
1. **Bounds check BILKUL nahi hota.** Ghalat strides diye to tum **array se bahar** ki memory parhoge.
   Natija: kachra data, ya program **crash** (segfault) — aur Python ka `try/except` isay **nahi pakaR sakta**.
2. **Overlapping windows me likhna tabahi hai** — ek element kai windows me nazar aata hai, to ek write
   kai jagah "dikhta" hai.
3. Result par `reshape`/`copy` karo to memory **phat** sakti hai (10 windows x 1000 length = bara array).

### Rules (inhe follow karo)
- Pehle **`sliding_window_view` try karo** — 99% cases me wohi kaafi hai aur **safe** hai.
- `as_strided` sirf tab jab koi chara na ho. Result ko foran **read-only** kar do (`writeable=False`).
- Strides khud se calculate karne ke bajaye array ke apne `strides` se derive karo.

> **Interview line:** *"as_strided ek loaded gun hai — ye NumPy ke andar ka `pointer arithmetic` hai,
> bounds checking ke baghair. Production me main `sliding_window_view` use karta hoon."*
"""))

A(code("""
from numpy.lib.stride_tricks import as_strided, sliding_window_view

# SAHI istemal: 1D array par overlapping windows (window=3)
data = np.arange(8, dtype=np.float64)
n, w = data.size, 3
item = data.itemsize

# shape = (windows ki tadaad, window ki lambai)
# strides = (ek window aage = 1 element, window ke andar = 1 element)  <- dono itemsize
windows = as_strided(data, shape=(n - w + 1, w), strides=(item, item), writeable=False)

print("data:", data)
print("as_strided se overlapping windows:")
print(windows)
print()
print("windows.shape        :", windows.shape)
print("memory share karta hai?", np.shares_memory(data, windows))
print("nbytes (jhoot bolta hai):", windows.nbytes, "-> lekin asli buffer sirf", data.nbytes, "bytes hai!")
print()
print("Yehi jadoo hai: 18 elements dikh rahe hain, memory me sirf 8 pade hain.")

assert windows.shape == (6, 3)
assert np.shares_memory(data, windows)
assert np.array_equal(windows[0], [0, 1, 2])
assert np.array_equal(windows[-1], [5, 6, 7])
"""))

A(code("""
# KHATRA #1 ka SAFE demo: ghalat shape maangne par tum buffer se bahar chale jate ho.
# Hum jaan boojh kar OUT-OF-BOUNDS **nahi** parhenge (wo crash kar sakta hai).
# Sirf hisaab kar ke dikhate hain ke kitna aage nikal jate.

small = np.arange(5, dtype=np.int64)     # sirf 5 elements = 40 bytes
print("asli buffer:", small.nbytes, "bytes (5 x int64)")

# Farz karo koi (10, 3) windows maang leta hai:
want_shape, want_strides = (10, 3), (8, 8)
# Aakhri element ka byte offset = (10-1)*8 + (3-1)*8
last_byte = (want_shape[0] - 1) * want_strides[0] + (want_shape[1] - 1) * want_strides[1]
print(f"maangi hui shape {want_shape} ka aakhri element byte offset = {last_byte}")
print("buffer ka aakhri legal byte offset =", small.nbytes - small.itemsize)

if last_byte > small.nbytes - small.itemsize:
    print()
    print(">>> KHATRA: ye", last_byte - (small.nbytes - small.itemsize), "bytes buffer se BAHAR jata hai.")
    print(">>> as_strided ye chup chaap bana dega -- koi error nahi.")
    print(">>> parhne par: kachra values, ya SEGFAULT (jo try/except bhi nahi pakaR sakta).")

print()
print("SAFETY RULE: windows ki tadaad khud calculate karo: n - w + 1")
safe_count = small.size - 3 + 1
print(f"  yahan safe count = {small.size} - 3 + 1 = {safe_count} (10 nahi!)")
safe = as_strided(small, shape=(safe_count, 3), strides=(8, 8), writeable=False)
print("safe windows:")
print(safe)
assert safe.shape == (3, 3)
"""))

A(code("""
# KHATRA #2: overlapping view me LIKHNA -- natija ghair-mutawaqqa hota hai
buf = np.arange(6, dtype=np.int64)
ov = as_strided(buf, shape=(4, 3), strides=(8, 8), writeable=True)   # jaan boojh kar writeable

print("shuru me buf:", buf)
print("overlapping view:")
print(ov)
print()
ov[:, 0] = 0        # "har window ka pehla element 0 karo" -- lagta hai maasoom kaam
print("ov[:, 0] = 0 ke baad buf:", buf)
print()
print("Dekha? Ek write ne kai jagah asar kiya kyun ke elements SHARED hain.")
print("Isi liye: as_strided ka natija hamesha writeable=False rakho.")

ro = as_strided(buf, shape=(4, 3), strides=(8, 8), writeable=False)
try:
    ro[0, 0] = 5
except ValueError as e:
    print()
    print("read-only view par likhne ki koshish -> ValueError:", str(e)[:60])
"""))

A(md("""
## 12. `sliding_window_view` — safe aur modern tareeqa

**Kya hai:** `np.lib.stride_tricks.sliding_window_view(arr, window_shape, axis=None)` —
`as_strided` ka **safe** version. NumPy khud shape/strides ka hisaab karta hai, bounds ka khayal rakhta hai,
aur natija **read-only** deta hai.

**Syntax:**
```python
sliding_window_view(x, 3)                       # 1D, window 3
sliding_window_view(x2d, (3, 3))                # 2D patches
sliding_window_view(x4d, (3, 3), axis=(2, 3))   # sirf in do axes par window
```

**Output shape ka qanoon:** har windowed axis `d` se `d - w + 1` ban jata hai, aur window ke
dimensions **aakhir me** add ho jate hain.

**Kyun use hota hai:** moving average / rolling statistics, image patches, convolution (im2col),
n-gram, time-series features — sab bina explicit loop.
"""))

A(code("""
# --- Real-World Use #1: Moving average (rolling mean) bina loop ---
signal = np.array([10.0, 12, 11, 15, 20, 18, 17, 22, 25, 24])
k = 3

win = sliding_window_view(signal, k)       # shape (10-3+1, 3) = (8, 3)
moving_avg = win.mean(axis=1)              # har window ka average

print("signal      :", signal)
print("windows shape:", win.shape)
print("windows:")
print(win)
print()
print(f"moving average (k={k}):", moving_avg.round(3))
print()
print("view hai? (memory share):", np.shares_memory(signal, win))
print("read-only? WRITEABLE =", win.flags["WRITEABLE"])

# Manually verify: pehla window ka mean = (10+12+11)/3 = 11
assert abs(moving_avg[0] - 11.0) < 1e-12
assert moving_avg.shape == (8,)
assert np.shares_memory(signal, win)
assert not win.flags["WRITEABLE"]      # safe by default!

# Loop wale tareeqe se milata hai?
loop_avg = np.array([signal[i:i + k].mean() for i in range(len(signal) - k + 1)])
assert np.allclose(moving_avg, loop_avg)
print()
print("loop wale jawab se match:", np.allclose(moving_avg, loop_avg))
"""))

A(code("""
# --- Real-World Use #2: 2D patch extraction (image processing ka bunyadi kaam) ---
img = np.arange(36, dtype=np.float64).reshape(6, 6)
print("image (6x6):")
print(img.astype(int))
print()

patches = sliding_window_view(img, (3, 3))     # saare 3x3 patches
print("patches.shape:", patches.shape, " <- (6-3+1, 6-3+1, 3, 3) = (4, 4, 3, 3)")
print()
print("patch [0,0] (top-left corner):")
print(patches[0, 0].astype(int))
print()
print("patch [1,2]:")
print(patches[1, 2].astype(int))
print()

# Memory ka kamaal
print(f"patches nbytes 'dikhta' hai : {patches.nbytes:,} bytes")
print(f"asli image ka buffer        : {img.nbytes:,} bytes")
print(f"bachaya                    : {patches.nbytes / img.nbytes:.1f}x memory (kyun ke ye VIEW hai)")

assert patches.shape == (4, 4, 3, 3)
assert np.shares_memory(img, patches)
assert np.array_equal(patches[0, 0], img[0:3, 0:3])
assert np.array_equal(patches[1, 2], img[1:4, 2:5])
"""))

A(code("""
# --- Real-World Use #3: im2col + convolution (yehi CNN andar se karti hai) ---
# 3x3 kernel se 2D convolution (technically cross-correlation, jo deep learning me 'conv' kehlata hai)

image = np.array([
    [1.0, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25],
])

# Edge-detection jaisa kernel
kernel = np.array([
    [0.0, -1, 0],
    [-1, 4, -1],
    [0, -1, 0],
])

# Step 1: saare patches ka VIEW banao (im2col ka dil)
patch_view = sliding_window_view(image, kernel.shape)    # (3, 3, 3, 3)

# Step 2: har patch ko kernel se multiply kar ke jama karo -- einsum se ek hi call me
#   'ijkl,kl->ij' : i,j = output position ; k,l = patch ke andar ka position (jama ho jayenge)
conv = np.einsum("ijkl,kl->ij", patch_view, kernel)

print("image:")
print(image.astype(int))
print()
print("kernel:")
print(kernel.astype(int))
print()
print("convolution output (valid mode):")
print(conv)
print()

# Verify: pehla output element haath se
manual = (image[0:3, 0:3] * kernel).sum()
print("manual hisaab conv[0,0] :", manual)
print("einsum wala conv[0,0]   :", conv[0, 0])
assert abs(conv[0, 0] - manual) < 1e-12
assert conv.shape == (3, 3)

# Loop wale reference se poora match
ref = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        ref[i, j] = (image[i:i + 3, j:j + 3] * kernel).sum()
assert np.allclose(conv, ref)
print()
print("loop reference se poora match:", np.allclose(conv, ref))
print()
print("Yehi 'im2col' technique hai. Asli CNN libraries isay BLAS matmul ke sath jorti hain")
print("taake GPU/CPU ki matrix-multiply ki poori taqat use ho jaye.")
"""))

A(md("""
## 13. `np.broadcast_to` — stride-0 ka jadoo

**Kya hai:** broadcasting ka andar ka mechanism. Jab NumPy `(3,1)` ko `(3,4)` banata hai, wo data
copy **nahi** karta — us axis ka **stride 0** kar deta hai!

**stride 0 ka matlab:** "aage baRho magar memory me hilo mat" — yaani wohi element bar bar parho.

```
v = [10, 20, 30]         shape (3,)   strides (8,)
np.broadcast_to(v, (4, 3)):
    shape   = (4, 3)
    strides = (0, 8)      <-- pehla axis ka stride ZERO
    matlab: 4 rows dikh rahi hain, magar chaaron ek hi memory parh rahi hain
```

**Kyun ahem hai:**
- Broadcasting **muft** hai (memory ke lehaz se) — `a + b` me expansion ka koi RAM kharch nahi
- `np.broadcast_to` ka natija **read-only** hota hai (aur hona bhi chahiye — ek jagah likhne se
  "saari" rows badal jatin)

> **Interview sawal:** *"Broadcasting implement kaise hoti hai?"* Jawab: **stride 0 wale views se.**
> Ye jawab interviewer ko bata deta hai ke tumne internals parhe hain.
"""))

A(code("""
v = np.array([10.0, 20.0, 30.0])
b = np.broadcast_to(v, (4, 3))       # 4 rows "bana" do

print("v            :", v, "strides:", v.strides)
print()
print("broadcast_to (4,3):")
print(b)
print()
print("b.strides    :", b.strides, "  <-- pehla 0 = 'hilo mat'")
print("b.shape      :", b.shape)
print("memory share :", np.shares_memory(v, b))
print("WRITEABLE    :", b.flags["WRITEABLE"], " <- read-only, aur ye theek hai")
print()
print(f"b 'dikhta' hai {b.nbytes} bytes ka, magar asli buffer sirf {v.nbytes} bytes hai")

assert b.strides[0] == 0            # stride-0 ka saboot
assert np.shares_memory(v, b)
assert not b.flags["WRITEABLE"]

# Likhne ki koshish -> ValueError (aur shukar hai!)
try:
    b[0, 0] = 99
except ValueError as e:
    print()
    print("b[0,0] = 99 ->  ValueError:", str(e)[:55])
    print("  Kyun mana hai? Kyun ke chaaron rows ek hi memory hain --")
    print("  ek ko badalte to 'chaaron' badal jatin. Ye confusing bug hota.")
"""))

A(code("""
# np.broadcast_arrays — kai arrays ko ek sath common shape par laao (bina memory kharch)
row = np.array([[1.0, 2.0, 3.0]])        # (1, 3)
col = np.array([[10.0], [20.0]])         # (2, 1)

r_b, c_b = np.broadcast_arrays(row, col)

print("row shape:", row.shape, " col shape:", col.shape)
print("broadcast ke baad dono ki shape:", r_b.shape, c_b.shape)
print()
print("r_b:"); print(r_b)
print("c_b:"); print(c_b)
print()
print("r_b.strides:", r_b.strides, " <- 0 wala axis broadcast hua")
print("c_b.strides:", c_b.strides)
print()
print("dono VIEWS hain? ", np.shares_memory(row, r_b), np.shares_memory(col, c_b))
print()

# Ye wohi natija hai jo row + col khud kar deta
print("row + col:"); print(row + col)
assert np.array_equal(r_b + c_b, row + col)

# np.broadcast_shapes -- sirf shape ka hisaab, koi array nahi banti
print()
print("broadcast_shapes((2,1),(1,3)) =", np.broadcast_shapes((2, 1), (1, 3)))
print("broadcast_shapes((5,1,3),(4,3)) =", np.broadcast_shapes((5, 1, 3), (4, 3)))
assert np.broadcast_shapes((2, 1), (1, 3)) == (2, 3)

# Na-mumkin shapes par error
try:
    np.broadcast_shapes((3, 4), (3, 5))
except ValueError as e:
    print()
    print("(3,4) aur (3,5) broadcast nahi ho sakte -> ValueError:", str(e)[:60])
"""))

A(code("""
# Memory bachane ka asli demo: tile vs broadcast_to
base_vec = rng.random(2000)

tiled = np.tile(base_vec, (2000, 1))            # ASLI 2000x2000 array banti hai
bcast = np.broadcast_to(base_vec, (2000, 2000))  # sirf ek view

print(f"np.tile        -> shape {tiled.shape}, asli memory: {tiled.nbytes / 1e6:7.2f} MB (OWNDATA={tiled.flags['OWNDATA']})")
print(f"broadcast_to   -> shape {bcast.shape}, asli memory: {base_vec.nbytes / 1e6:7.2f} MB (OWNDATA={bcast.flags['OWNDATA']})")
print(f"bachat         -> {tiled.nbytes / base_vec.nbytes:.0f}x kam memory")
print()

# Dono ka natija barabar
assert np.array_equal(tiled, bcast)
print("values barabar hain?", np.array_equal(tiled, bcast))
print()
print("SABAQ: jab bhi 'ek vector ko har row me repeat karna hai' -- tile ki zaroorat NAHI.")
print("       Seedha broadcasting use karo: matrix + vector. NumPy khud stride-0 laga leta hai.")

# Cleanup (bara array free karo)
del tiled
"""))

A(md("""
## 14. `np.newaxis` vs `reshape` — dono ek hi kaam ke do naam

**Kya hai:** `None` (ya `np.newaxis`) indexing me ek nayi **length-1 axis** ghusa deta hai.

```python
a[np.newaxis, :]   ==  a.reshape(1, -1)      # (n,)  -> (1, n)
a[:, np.newaxis]   ==  a.reshape(-1, 1)      # (n,)  -> (n, 1)
```

**Farq:**
- `newaxis` **hamesha view** deta hai (zero-copy, guaranteed)
- `reshape` bhi normally view deta hai magar mushkil case me copy kar sakta hai
- `newaxis` **paRhne me zyada saaf** hai jab maqsad broadcasting ho: `a[:, None] - b[None, :]`
  ek nazar me "outer difference" bata deta hai

**Interview tip:** `a[:, None] - a[None, :]` — ye pairwise-difference matrix ka mashhoor idiom hai
(distance matrix banane ka pehla qadam). Isay zubani likhna aana chahiye.
"""))

A(code("""
x = np.array([1.0, 2.0, 3.0])

print("x shape          :", x.shape)
print("x[np.newaxis, :] :", x[np.newaxis, :].shape, "(row vector)")
print("x[:, np.newaxis] :", x[:, np.newaxis].shape, "(column vector)")
print("x[None] == x[np.newaxis] ?", np.array_equal(x[None], x[np.newaxis]))
print()

# Dono view hain
assert np.shares_memory(x, x[:, None])
assert np.shares_memory(x, x.reshape(-1, 1))
print("newaxis view hai?", np.shares_memory(x, x[:, None]))
print("reshape view hai?", np.shares_memory(x, x.reshape(-1, 1)))
print()

# Asli fayda: pairwise operations ka saaf idiom
diff = x[:, None] - x[None, :]        # (3,1) - (1,3) -> (3,3)
print("x[:, None] - x[None, :]  (pairwise difference matrix):")
print(diff)
print()

# Pairwise squared distance -- kNN/k-means ka bunyadi block
pts = np.array([[0.0, 0.0], [3.0, 4.0], [6.0, 8.0]])
d2 = ((pts[:, None, :] - pts[None, :, :]) ** 2).sum(axis=-1)
print("pairwise squared distances:")
print(d2)
print("sqrt (asli distance):")
print(np.sqrt(d2))
assert abs(np.sqrt(d2)[0, 1] - 5.0) < 1e-12     # (0,0)->(3,4) = 5 (classic 3-4-5)
"""))

A(md("""
## 15. dtype `view()` tricks — usi bytes ko doosre chashme se dekhna

**Kya hai:** `arr.view(new_dtype)` bytes ko **badalta nahi** — sirf unhe parhne ka tareeqa badal deta hai.
`astype` ke bilkul ulta:

| | `view(dtype)` | `astype(dtype)` |
|---|---|---|
| bytes | **wohi** (reinterpret) | **naye** (convert) |
| memory | zero-copy view | nayi copy |
| `1.0` float64 -> int64 | `4607182418800017408` (bits!) | `1` (value) |

**Kyun use hota hai:** float ki bit-level tafteesh (NaN/inf debugging, hashing), structured arrays ko
plain array banana, binary file parsing.

### `view()` ke RULES (yahan log phaste hain)
1. Agar naye dtype ka size **mukhtalif** hai to **aakhri axis contiguous** hona lazmi hai.
2. Aakhri axis ki total bytes naye itemsize par poori taqseem honi chahiye.
3. Non-contiguous array par size-change view -> `ValueError`.
"""))

A(code("""
# --- float ki bits ko int me dekhna ---
f = np.array([1.0, 2.0, -1.0])
bits = f.view(np.int64)          # wohi 24 bytes, ab int64 ki tarah parhe

print("float values :", f)
print("wohi bytes as int64:", bits)
print()
print("1.0 ke bits binary me:", format(bits[0], "064b"))
print("                       ^sign  ^^^^^^^^^^^ exponent  ^^^^^ mantissa")
print()
print("view hai? memory share:", np.shares_memory(f, bits))
print()
# astype se muqabla
print("f.astype(np.int64) (VALUE convert):", f.astype(np.int64))
print("f.view(np.int64)   (BITS reinterpret):", f.view(np.int64))
print()
print("Dekha farq? astype -> 1, view -> 4607182418800017408 (IEEE-754 bit pattern)")

assert np.shares_memory(f, bits)
assert bits[0] == 4607182418800017408          # 1.0 ka IEEE-754 pattern (deterministic)
assert np.array_equal(f.astype(np.int64), [1, 2, -1])

# Practical use: sign bit nikalna bina comparison
sign_bits = (f.view(np.int64) >> 63) & 1
print()
print("sign bit (1 = negative):", sign_bits, " <- -1.0 ka sign bit 1 hai")
assert np.array_equal(sign_bits, [0, 0, 1])
"""))

A(code("""
# --- view() ke RULES ka demo: kab ValueError aata hai ---

# Rule OK: contiguous array, size change chalega
ok = np.arange(4, dtype=np.int64)              # 32 bytes
print("int64 array:", ok)
print("int32 ki tarah dekho:", ok.view(np.int32), " <- 4 elements 8 ban gaye (har int64 = 2 int32)")
print()

# Rule TOOTA: non-contiguous par size-change view
bad = np.arange(10, dtype=np.int64)[::2]        # step slice -> non-contiguous
print("non-contiguous view ka strides:", bad.strides, "(itemsize 8, magar stride 16)")
try:
    bad.view(np.int32)
except ValueError as e:
    print("bad.view(np.int32) -> ValueError:", e)
    print("  ^ NumPy kehta hai: aakhri axis contiguous nahi, main ye reinterpret nahi kar sakta.")

print()
# Hal: pehle contiguous banao
fixed_view = np.ascontiguousarray(bad).view(np.int32)
print("ascontiguousarray ke baad view chal gaya, shape:", fixed_view.shape)

print()
# Same-size view par ye rule laagu nahi (int64 -> float64 dono 8 bytes)
same_size = bad.view(np.float64)
print("same-size view (int64->float64) non-contiguous par bhi chalta hai:", same_size.shape)
assert same_size.shape == (5,)
"""))

A(code("""
# --- structured array <-> unstructured ---
# numpy 2.x me recfunctions ko ALAG import karna paRta hai (np.lib.recfunctions kaam nahi karta)
from numpy.lib import recfunctions as rfn

# Structured array = C struct ki tarah, har record me named fields
dt = np.dtype([("x", np.float64), ("y", np.float64), ("label", np.int32)])
records = np.array([(1.0, 2.0, 0), (3.0, 4.0, 1), (5.0, 6.0, 0)], dtype=dt)

print("structured array:")
print(records)
print()
print("itemsize per record:", records.itemsize, "bytes (8 + 8 + 4 = 20)")
print("field 'x':", records["x"], " <- ye ek VIEW hai!")
print("field x memory share karta hai?", np.shares_memory(records, records["x"]))
print("field x ka strides:", records["x"].strides, "<- 20 bytes (poora record chhod kar agla x)")
print()

# Sirf float fields ko plain 2D array banao
xy = rfn.structured_to_unstructured(records[["x", "y"]])
print("structured_to_unstructured (x, y):")
print(xy)
print("shape:", xy.shape, "dtype:", xy.dtype)
print()

assert np.shares_memory(records, records["x"])
assert np.array_equal(records["x"], [1.0, 3.0, 5.0])
assert xy.shape == (3, 2)
assert np.allclose(xy, [[1, 2], [3, 4], [5, 6]])
print("Field access zero-copy hai -- isi wajah se structured arrays CSV-jaisa data")
print("rakhne ke liye memory-efficient hain (pandas se bhi halke, magar kam features).")
"""))

A(md("""
## 16. Byte order / Endianness — `>i4` vs `<i4`

**Kya hai:** multi-byte number ko memory me rakhne ke do tareeqe:

- **little-endian** (`<`) — kam ahem byte pehle. x86/ARM (yaani tumhara laptop) ka tareeqa.
- **big-endian** (`>`) — zyada ahem byte pehle. "Network byte order", kuch purane file formats.

Number `1` as int32:
```
little-endian:  01 00 00 00
big-endian   :  00 00 00 01
```

**Kahan phaste ho:** binary file ya network se data parhte waqt. Agar file big-endian hai aur tum
default (little) se parh lo to numbers **bilkul bekaar** aayenge (1 ke bajaye 16777216).

**Do alag operations, farq samjho:**
- `arr.byteswap()` — **bytes ulat do** (values badal jayengi agar dtype wohi rahe)
- `arr.view(dtype.newbyteorder())` — **label badal do** (bytes wohi, parhne ka tareeqa badla)
- Dono sath karo -> value wohi rehti hai, sirf representation badalti hai

> **NumPy 2.x note:** `arr.newbyteorder()` **method hata diya gaya hai**.
> Ab `arr.view(arr.dtype.newbyteorder())` likho.
"""))

A(code("""
# Big-endian aur little-endian arrays
le = np.array([1, 256], dtype="<i4")     # little-endian int32
be = np.array([1, 256], dtype=">i4")     # big-endian int32

print("little-endian values:", le, " dtype:", le.dtype, " byteorder:", le.dtype.byteorder)
print("big-endian    values:", be, " dtype:", be.dtype, " byteorder:", be.dtype.byteorder)
print()
print("Values BARABAR hain:", np.array_equal(le, be), " <- NumPy khud handle kar leta hai")
print()
print("magar RAW BYTES mukhtalif hain:")
print("  little-endian bytes:", le.tobytes().hex(" "))
print("  big-endian    bytes:", be.tobytes().hex(" "))
print()

assert np.array_equal(le, be)
assert le.tobytes() != be.tobytes()

# byteswap: bytes ulat do (dtype label wohi) -> VALUE badal jati hai
swapped = le.byteswap()
print("le.byteswap() ->", swapped, " <- 1 ban gaya 16777216 (bytes ulat gaye)")
assert swapped[0] == 16777216

print()
# Sahi tareeqa: byteswap + label change -> value mehfooz
converted = le.byteswap().view(le.dtype.newbyteorder())
print("byteswap + view(newbyteorder) ->", converted, " <- value wohi, ab big-endian")
print("naya dtype:", converted.dtype)
assert np.array_equal(converted, [1, 256])
"""))

A(code("""
# ASLI DUNIYA ka masla: big-endian binary file parhna
# Farz karo ek sensor big-endian int32 bhejta hai: values [1000, 2000, 3000]
sensor_bytes = np.array([1000, 2000, 3000], dtype=">i4").tobytes()
print("raw bytes (network se aaye):", sensor_bytes.hex(" "))
print()

# GHALAT tareeqa: default (little-endian) maan kar parh liya
wrong = np.frombuffer(sensor_bytes, dtype="<i4")
print("GHALAT parhna (<i4):", wrong, " <- bilkul kachra!")

# SAHI tareeqa: bataya ke data big-endian hai
right = np.frombuffer(sensor_bytes, dtype=">i4")
print("SAHI  parhna (>i4):", right, " <- perfect")
print()

assert not np.array_equal(wrong, [1000, 2000, 3000])
assert np.array_equal(right, [1000, 2000, 3000])

# Aage ke hisaab ke liye native order me le aao (tez chalega)
native = right.astype(np.int32)
print("native order me convert:", native, "dtype:", native.dtype)
print()
print("SABAQ: binary data parhte waqt endianness POOCHO, maan mat lo.")
print("       Aur hisaab se pehle native dtype me convert kar lo -- non-native")
print("       byte order par har operation slow hota hai (byte swapping per element).")
"""))

A(md("""
## 17. Buffer protocol — `frombuffer`, `tobytes`, `memoryview`

**Kya hai:** Python ka standard "raw memory share karne" ka protocol. `bytes`, `bytearray`,
`memoryview`, `array.array`, NumPy arrays — sab ise support karte hain. Isi liye NumPy doosri
libraries ke sath **bina copy** data share kar leta hai.

| Function | Kya karta hai | Copy? |
|---|---|---|
| `arr.tobytes()` | array -> `bytes` object (C-order by default) | **Copy** (hamesha) |
| `np.frombuffer(buf, dtype)` | buffer -> array | **Zero-copy view!** |
| `memoryview(arr)` | array ka Python-level memory view | Zero-copy |
| `np.asarray(memoryview)` | wapas array | Zero-copy |

**Sab se bara gotcha:** `np.frombuffer(b"...")` ka natija **read-only** hota hai — kyun ke Python ka
`bytes` immutable hai. Writeable chahiye to `bytearray` do.

**Kahan use hota hai:** binary file parsing, socket se aaye packets, shared memory,
doosri library (image decoder, audio) se aaye buffers.
"""))

A(code("""
arr_src = np.array([10, 20, 30, 40], dtype=np.int16)

# 1) tobytes -> raw bytes (COPY)
raw_bytes = arr_src.tobytes()
print("array         :", arr_src, "dtype:", arr_src.dtype)
print("tobytes()     :", raw_bytes, "=", raw_bytes.hex(" "))
print("length        :", len(raw_bytes), "bytes (4 x int16)")
print()

# 2) frombuffer -> wapas array (ZERO COPY, magar read-only)
back = np.frombuffer(raw_bytes, dtype=np.int16)
print("frombuffer    :", back)
print("WRITEABLE     :", back.flags["WRITEABLE"], " <- False! bytes immutable hai")
try:
    back[0] = 99
except ValueError as e:
    print("likhne ki koshish -> ValueError:", str(e)[:50])

print()
# 3) Writeable chahiye? bytearray do
mutable_buf = bytearray(raw_bytes)
writable = np.frombuffer(mutable_buf, dtype=np.int16)
print("bytearray se frombuffer -> WRITEABLE:", writable.flags["WRITEABLE"])
writable[0] = 999
print("array me likha    :", writable)
print("bytearray bhi badla:", np.frombuffer(mutable_buf, dtype=np.int16))
print("  ^ dono ek hi memory hain (zero-copy ka saboot)")

assert np.array_equal(back, [10, 20, 30, 40])
assert not back.flags["WRITEABLE"]
assert writable.flags["WRITEABLE"] and writable[0] == 999
"""))

A(code("""
# memoryview ke zariye interop
buf = bytearray(b"\\x01\\x00\\x02\\x00\\x03\\x00")     # 3 int16 little-endian
mv = memoryview(buf)

as_array = np.frombuffer(mv, dtype="<i2")
print("bytearray      :", bytes(buf).hex(" "))
print("numpy array    :", as_array)
print("zero-copy?     :", as_array.flags["WRITEABLE"], "(bytearray mutable tha to writeable mila)")
print()

# Doosri taraf: numpy array ka memoryview
np_arr = np.arange(4, dtype=np.int32)
np_mv = memoryview(np_arr)
print("numpy array ka memoryview:")
print("  format  :", np_mv.format, "(i = int32)")
print("  itemsize:", np_mv.itemsize)
print("  shape   :", np_mv.shape)
print("  nbytes  :", np_mv.nbytes)
print("  readonly:", np_mv.readonly)
print()

# Ek chhoti binary "file format" parse karte hain (asli kaam jaisa)
# Format: [magic:2 bytes][count:int32][data:count x float32]
payload = (b"NP" + np.int32(3).tobytes() + np.array([1.5, 2.5, 3.5], dtype=np.float32).tobytes())
print("payload:", payload.hex(" "))

magic = payload[:2]
count = np.frombuffer(payload, dtype=np.int32, count=1, offset=2)[0]
values = np.frombuffer(payload, dtype=np.float32, count=int(count), offset=6)

print("parse kiya -> magic:", magic, "count:", count, "values:", values)
assert magic == b"NP"
assert count == 3
assert np.allclose(values, [1.5, 2.5, 3.5])
print()
print("Gaur karo: poori parsing me DATA ki ek bhi copy nahi hui -- sirf offsets se views.")
"""))

A(md("""
## 18. `nbytes` vs asli memory — kitna jhoot hai?

`arr.nbytes` sirf **data buffer** ke bytes batata hai. Asli RAM ka istemal is se **zyada** ya
(views me) **bohat kam** ho sakta hai.

| Cheez | `nbytes` | Asli RAM |
|---|---|---|
| `np.arange(1000)` (int64) | 8000 | 8000 + ~112 bytes object overhead |
| `a[::2]` (view) | 4000 | **~0** (koi nayi data memory nahi) |
| `np.broadcast_to(v, (1000, 1000))` | 8,000,000 | **8000** (sirf v) |
| `sliding_window_view(a, 100)` | bohat bara | asli array jitna |
| `object` dtype array | pointers ke bytes | + har Python object ka apna size |

**Sab se bara jhoot:** `object` dtype. `np.array([1, 2, 3], dtype=object).nbytes` sirf pointers ginta hai,
asli Python integers ka size shamil nahi.
"""))

A(code("""
small_arr = np.arange(1000, dtype=np.int64)

print(f"{'cheez':42} {'nbytes':>12} {'OWNDATA':>8}")
print("-" * 66)
items = [
    ("np.arange(1000) int64", small_arr),
    ("small_arr[::2] (view)", small_arr[::2]),
    ("np.broadcast_to(v, (1000, 1000))", np.broadcast_to(small_arr, (1000, 1000))),
    ("sliding_window_view(a, 100)", sliding_window_view(small_arr, 100)),
]
for label, a in items:
    print(f"{label:42} {a.nbytes:12,} {str(a.flags['OWNDATA']):>8}")

print()
print("Gaur karo: aakhri do ka nbytes GB me ja raha hai, magar OWNDATA=False --")
print("matlab asli data memory sirf pehle array ki hai (8,000 bytes).")
print()
print("Python object ka overhead dekhne ke liye sys.getsizeof:")
print("  sys.getsizeof(small_arr) =", sys.getsizeof(small_arr), "(machine-specific, assert na karo)")
print("  small_arr.nbytes         =", small_arr.nbytes, "(deterministic, assert kar sakte ho)")
print()

# object dtype ka jhoot
obj_arr = np.array([1, 2, 3], dtype=object)
int_arr = np.array([1, 2, 3], dtype=np.int64)
print("object dtype nbytes:", obj_arr.nbytes, "(sirf 3 pointers)")
print("int64  dtype nbytes:", int_arr.nbytes)
print("magar object array me har element ek poora Python int hai:")
print("  sys.getsizeof(1) =", sys.getsizeof(1), "bytes! (per element)")
print("  yaani asli memory taqreeban:", obj_arr.nbytes + 3 * sys.getsizeof(1), "bytes")
print()
print("SABAQ: object dtype se bacho -- memory phoolti hai aur har operation Python loop banta hai.")

assert small_arr.nbytes == 8000
assert not small_arr[::2].flags["OWNDATA"]
"""))

A(md("""
## 19. `np.empty` + in-place fill, aur `out=` parameter

**Kya hai:**
- `np.empty(shape)` — memory **allocate** karta hai magar **initialize nahi** karta. Isliye
  `np.zeros` se tez hai, magar andar **kachra** hota hai.
- `out=` — har ufunc/reduction ka parameter: "natija naye array me na banao, is maujooda array me likho".

**Kyun use hota hai:** temporary arrays se bachna. `a * 2 + b * 3` me NumPy 3 temporary arrays banata hai
aur RAM me 3 dafa aata-jata hai. `out=` se ye kharch bachta hai — bare arrays par **2x tak** faster.

**`np.empty` ka gotcha:** log samajhte hain ye zeros deta hai. **Nahi deta.** Kabhi kabhi ittefaqan
zeros dikh jate hain (freshly-allocated OS pages), isliye bug **chhup** jata hai aur baad me phatta hai.
Rule: `np.empty` sirf tab jab tum **foran poora array bhar** rahe ho.
"""))

A(code("""
# np.empty ka kachra dekhte hain (values machine par mukhtalif -> sirf print)
garbage = np.empty(5, dtype=np.float64)
print("np.empty(5) ka content (initialized NAHI):", garbage)
print("  ^ jo bhi purana data us memory me tha wohi hai. zeros ki umeed na karo!")
print()
print("np.zeros(5):", np.zeros(5), " <- ye guarantee se zeros hai (magar zero karne ka waqt lagta hai)")
print()

# SAHI pattern: empty + foran poora bharo
n = 5
result = np.empty(n, dtype=np.float64)     # allocate
result[:] = np.arange(n) * 2.0             # foran poora bhar diya -> ab safe
print("empty + poora fill:", result)
assert np.array_equal(result, [0, 2, 4, 6, 8])

print()
# zeros vs empty ki speed (bare array par)
big_shape = (1000, 1000)
t_zeros = bench(lambda: np.zeros(big_shape))
t_empty = bench(lambda: np.empty(big_shape))
print(f"np.zeros({big_shape}) : {t_zeros:6.3f} ms")
print(f"np.empty({big_shape}) : {t_empty:6.3f} ms")
print("empty tez hai kyun ke usay memory ko zero karne ki mehnat nahi karni paRti.")
print("(Note: OS aksar nayi pages khud zero deta hai, isliye farq machine par badalta hai.)")
"""))

A(code("""
# out= ka demo: temporaries se bachna
size = 2_000_000
a_big = rng.random(size)
b_big = rng.random(size)

# Tareeqa 1: normal expression -- NumPy andar temporaries banata hai
def with_temporaries():
    return a_big * 2.0 + b_big * 3.0        # temp1 = a*2, temp2 = b*3, temp3 = temp1+temp2

# Tareeqa 2: pre-allocated buffer + out= -> zero temporaries
out_buf = np.empty(size, dtype=np.float64)

def with_out():
    np.multiply(a_big, 2.0, out=out_buf)    # out_buf = 2a
    out_buf.__iadd__(b_big)                 # += b   (teen dafa jama karke 3b)
    out_buf.__iadd__(b_big)
    out_buf.__iadd__(b_big)
    return out_buf

t1 = bench(with_temporaries)
t2 = bench(with_out)

print(f"array size: {size:,} float64 ({a_big.nbytes / 1e6:.0f} MB per array)")
print()
print(f"normal expression (temporaries) : {t1:7.2f} ms")
print(f"out= + in-place (zero temp)     : {t2:7.2f} ms")
print(f"faida                           : {t1 / t2:5.2f}x (taqreeban)")
print()

# Natija BILKUL barabar hona chahiye
assert np.allclose(with_temporaries(), with_out())
print("dono ka natija barabar?", np.allclose(with_temporaries(), with_out()))
print()
print("Kyun tez? Har temporary ka matlab: nayi memory allocate + poora array RAM me likhna")
print("aur wapas parhna. Ye 'memory bandwidth' kharch hai, jo bare arrays par asli bottleneck hai.")
print()
print("MEMORY ALLOCATOR ka zikr: NumPy chhote arrays ke liye ek internal cache/arena rakhta hai")
print("taake bar bar OS se memory maangne ka kharch bache. Bare arrays seedha OS se aate hain")
print("(malloc/mmap). Isi wajah se chhote arrays ki allocation ka kharch aksar nazar nahi aata,")
print("magar 100 MB ke temporary ka poora kharch dikhta hai.")
"""))

A(code("""
# out= reductions me bhi chalta hai
matrix = rng.random((100, 50))
row_sums = np.empty(100)
np.sum(matrix, axis=1, out=row_sums)      # natija maujooda buffer me
print("row_sums ke pehle 5:", row_sums[:5].round(4))
assert np.allclose(row_sums, matrix.sum(axis=1))

# where= ke sath out= -- sirf chuninda jagah likho (baqi buffer ka purana data rehta hai)
vals = np.array([1.0, -2.0, 3.0, -4.0, 5.0])
dest = np.zeros(5)
np.sqrt(vals, out=dest, where=vals > 0)   # sirf positive par sqrt (negative par NaN warning se bacha)
print()
print("vals          :", vals)
print("sqrt with where:", dest, " <- negative wali jagah 0 rahi (chhui hi nahi)")
assert abs(dest[0] - 1.0) < 1e-12 and dest[1] == 0.0

print()
# GOTCHA: out= ka dtype match karna zaroori hai
try:
    int_out = np.empty(5, dtype=np.int64)
    np.sqrt(np.arange(5.0), out=int_out)
except (TypeError, np.exceptions.UFuncTypeError) as e:
    print("float ka natija int buffer me -> error:", type(e).__name__)
    print("  ", str(e)[:90])
    print("  ^ out= buffer ka dtype natije se compatible hona chahiye.")
"""))

A(md("""
## 20. `np.memmap` — RAM se bari files par kaam (out-of-core)

**Kya hai:** file ko "array ki tarah" khol lo. Data disk par rehta hai; jab tum kisi hisse ko chhoote ho
to OS us page ko RAM me le aata hai (demand paging). 100 GB file ko 8 GB RAM par process karna mumkin.

**Syntax:**
```python
mm = np.memmap(path, dtype=np.float32, mode="w+", shape=(1000, 500))
mm[:] = ...        # likho
mm.flush()         # disk par pakka karo
del mm             # map band karo
```

**Modes:** `'r'` (read-only), `'r+'` (read-write, file mojood ho), `'w+'` (nayi banao/overwrite), `'c'`
(copy-on-write — changes RAM me, file safe).

**Kab use karo:** data RAM me na aata ho, aur tum us par **sequential ya chunk-wise** kaam karte ho.
**Kab NA karo:** random access har jagah — disk seek maar dega. Aur network drive par bilkul nahi.

**Windows par gotcha:** file khuli (mapped) rehte hue delete nahi hoti. Pehle `flush()` + `del` karo.
"""))

A(code("""
# memmap ka poora demo -- tempfile me (spec ke mutabiq, koi bahar ki file nahi)
tmpdir = tempfile.mkdtemp(prefix="memmap_demo_")
path = os.path.join(tmpdir, "big_data.dat")

rows, cols = 2000, 100
print(f"'bara' dataset banate hain: ({rows}, {cols}) float32 = {rows * cols * 4 / 1e6:.2f} MB")

# 1) Likhna (mode='w+' nayi file banata hai)
mm = np.memmap(path, dtype=np.float32, mode="w+", shape=(rows, cols))
print("memmap type:", type(mm).__name__, "| ndarray ka subclass?", isinstance(mm, np.ndarray))

# Chunk-by-chunk bharo -- yehi asli out-of-core pattern hai
chunk = 500
for start in range(0, rows, chunk):
    stop = min(start + chunk, rows)
    mm[start:stop] = np.arange(start, stop, dtype=np.float32)[:, None] * np.ones(cols, np.float32)

mm.flush()              # disk par likhna pakka karo
del mm                  # map band karo (Windows par ye ZAROORI hai)

print("file disk par size:", os.path.getsize(path), "bytes")
assert os.path.getsize(path) == rows * cols * 4
"""))

A(code("""
# 2) Parhna (mode='r' = read-only, mehfooz)
mm_read = np.memmap(path, dtype=np.float32, mode="r", shape=(rows, cols))

print("shape:", mm_read.shape, "dtype:", mm_read.dtype)
print("pehli row ke pehle 5:", mm_read[0, :5])
print("aakhri row ke pehle 5:", mm_read[-1, :5])
print()

# Out-of-core mean: chunk-wise, poori file kabhi RAM me nahi aati
total, count = 0.0, 0
for start in range(0, rows, chunk):
    block = np.asarray(mm_read[start:start + chunk], dtype=np.float64)  # sirf ye chunk RAM me
    total += block.sum()
    count += block.size

chunked_mean = total / count
print(f"chunk-wise mean: {chunked_mean:.4f}")

# Verify: har row ki value = row index, to mean = (0+1+...+1999)/2000 = 999.5
expected_mean = (rows - 1) / 2
print(f"expected mean  : {expected_mean}")
assert abs(chunked_mean - expected_mean) < 1e-6

print()
# read-only memmap par likhna mana hai
try:
    mm_read[0, 0] = 123.0
except ValueError as e:
    print("read-only memmap par write -> ValueError:", str(e)[:55])

del mm_read      # Windows par map band karna zaroori
print()
print("SABAQ: memmap ka poora fayda tab hai jab tum CHUNKS me kaam karo.")
print("       mm.sum() likh dena poori file ko RAM me kheench sakta hai -- ehtiyat!")
"""))

A(md("""
## 21. NumPy me copy-on-write NAHI hota — aur `setflags`

**Kya hai:** kuch languages/libraries (jaise pandas ka naya CoW mode, ya Linux ka `fork`) me
"copy" ka waada hota hai magar asal me copy sirf **likhne ke waqt** hoti hai. **NumPy aisa nahi karta.**

NumPy me qanoon bilkul saaf hai:
- View = view. Likha to **sab ko dikhega**. Koi khud-kar copy nahi.
- Copy chahiye to **khud** `.copy()` likho. Explicit is better than implicit.

**Iska nateeja:** wo mashhoor "accidental mutation" bug — function ko array diya, function ne
usay in-place badal diya, aur caller ka data khamoshi se kharab ho gaya.

**Bachne ke tareeqe:**
1. Function ke shuru me `arr = np.asarray(arr)` + zaroorat ho to `.copy()`
2. Ya array ko **read-only** kar do: `arr.setflags(write=False)` — phir koi ghalti se likh hi nahi sakta
3. Documentation me saaf likho: "ye function in-place modify karta hai"
"""))

A(code("""
# --- Accidental mutation ka classic bug ---
def normalize_buggy(data):
    \"\"\"BUG: data ko in-place badal deta hai -- caller ka array barbaad!\"\"\"
    data -= data.mean()        # in-place subtraction (-=) -> ASLI array badal gaya
    data /= data.std()
    return data


def normalize_safe(data):
    \"\"\"SAHI: pehle copy (ya naya array) banao, phir kaam karo.\"\"\"
    data = np.asarray(data, dtype=np.float64)      # input ko array banao
    out = (data - data.mean()) / data.std()        # naya array banta hai (in-place nahi)
    return out


measurements = np.array([10.0, 20.0, 30.0, 40.0])
backup = measurements.copy()

print("shuru me measurements :", measurements)
_ = normalize_buggy(measurements)
print("buggy function ke baad :", measurements, " <-- ASLI DATA TABAH!")
print()

measurements2 = backup.copy()
print("shuru me measurements2:", measurements2)
result = normalize_safe(measurements2)
print("safe function ke baad  :", measurements2, " <-- bilkul mehfooz")
print("return kiya natija     :", result.round(4))

assert not np.array_equal(measurements, backup)      # buggy ne barbaad kiya
assert np.array_equal(measurements2, backup)         # safe ne haath nahi lagaya
print()
print("Yaad rakho: -=, +=, *=, /= sab IN-PLACE hain. Ye view/caller ke data tak pohanchte hain.")
print("            x = x - 1  aur  x -= 1  ka farq yahan zindagi aur maut ka farq hai.")
"""))

A(code("""
# --- setflags se defensive programming ---
shared_config = np.array([1.0, 2.0, 3.0, 4.0])
shared_config.setflags(write=False)          # ab ye constant hai

print("read-only array:", shared_config)
print("WRITEABLE flag :", shared_config.flags["WRITEABLE"])
print()

try:
    shared_config[0] = 100.0
except ValueError as e:
    print("likhne ki koshish -> ValueError:", str(e)[:55])
    print("  ^ Bug run-time par FORAN pakRa gaya, chup chaap data kharab nahi hua.")

print()
# Read karna bilkul theek hai, aur hisaab bhi
print("parhna theek hai      :", shared_config[2])
print("hisaab bhi theek hai  :", (shared_config * 2))   # naya array banta hai, asli safe
print()

# Wapas writeable karna (agar tum OWNER ho)
writable_copy = shared_config.copy()          # copy hamesha writeable hoti hai
print("copy WRITEABLE:", writable_copy.flags["WRITEABLE"])
writable_copy[0] = 100.0
print("copy me likha :", writable_copy, "| asli:", shared_config)

assert not shared_config.flags["WRITEABLE"]
assert shared_config[0] == 1.0                # bilkul nahi badla
assert writable_copy[0] == 100.0
"""))

A(md("""
## 22. Alignment aur SIMD ka zikr

**Alignment kya hai:** CPU ke liye behtar hai ke 8-byte `float64` ka address 8 ka multiple ho.
Aise data ko **aligned** kehte hain. `ALIGNED` flag yehi batata hai.

- NumPy ke apne allocate kiye arrays **hamesha aligned** hote hain (fikr ki baat nahi)
- Un-aligned sirf tab mil sakta hai jab tum raw buffer se offset par view banao (jaise
  `frombuffer(..., offset=1)`) ya kuch structured dtypes me
- Un-aligned par NumPy phir bhi kaam karta hai, magar **slow** path se

**SIMD kya hai:** *Single Instruction, Multiple Data* — modern CPU ek hi instruction me 4/8/16 numbers
par kaam kar sakta hai (SSE/AVX2/AVX-512 registers). NumPy ke ufunc loops isi ke liye likhe gaye hain.

**Isi liye ye teen cheezein maayne rakhti hain:**
1. **Contiguity** — SIMD ko lagatar memory chahiye. Bikhra data = SIMD off = slow.
2. **dtype** — `float32` me ek AVX register me `float64` se **dugne** numbers aate hain -> taqreeban 2x tez
3. **Alignment** — aligned load instructions un-aligned se tez hain

> **Interview line:** *"NumPy tez kyun hai?"* — sirf "C me likha hai" na kehna. Kaho:
> *"contiguous typed memory par likhe hue C loops jo SIMD vectorize hote hain, plus BLAS ka istemal,
> plus per-element Python object overhead ka na hona."*
"""))

A(code("""
# ALIGNED flag ka muzahira
normal = np.arange(10, dtype=np.float64)
print("NumPy ka apna array -> ALIGNED:", normal.flags["ALIGNED"])
print("data address:", normal.__array_interface__["data"][0], "| 8 se taqseem:",
      normal.__array_interface__["data"][0] % 8 == 0)
print()

# Raw buffer se offset par view -> alignment toot sakti hai
raw = bytearray(np.arange(10, dtype=np.float64).tobytes())
offset_view = np.frombuffer(raw, dtype=np.float64, offset=8, count=5)   # 8 ka multiple -> aligned
print("offset=8 (8 ka multiple)  -> ALIGNED:", offset_view.flags["ALIGNED"])
print()

# float32 vs float64 ki speed (SIMD width ka asar)
n_simd = 2_000_000
a64 = rng.random(n_simd)
a32 = a64.astype(np.float32)

t64 = bench(lambda: a64 * a64)
t32 = bench(lambda: a32 * a32)

print(f"float64 multiply ({a64.nbytes / 1e6:.0f} MB): {t64:6.2f} ms")
print(f"float32 multiply ({a32.nbytes / 1e6:.0f} MB): {t32:6.2f} ms")
print(f"float32 taqreeban {t64 / t32:.2f}x tez")
print()
print("Wajah do hain: (1) aadhi memory bandwidth chahiye, (2) ek SIMD register me dugne numbers.")
print("SAWDA: float32 me precision kam hoti hai (~7 decimal digits vs ~16).")
print("       ML/graphics me float32 aam hai; paise ka hisaab ya scientific accumulation me float64 rakho.")
"""))

A(md("""
## 23. Common Mistakes / Gotchas — ek jagah jama

Ye wo galtiyaan hain jo asli code me sab se zyada dekhi jati hain:

| # | Ghalti | Kya hota hai | Theek tareeqa |
|---|---|---|---|
| 1 | `.base is None` se "copy hai" check karna | jhoot jawab (`a.T.reshape` case) | `np.shares_memory(a, b)` |
| 2 | Function me `arr -= x` likhna | caller ka data barbaad | pehle `.copy()` ya naya array banao |
| 3 | `np.empty` ko zeros samajhna | kachra values, chhupa bug | `np.zeros` ya foran poora bharo |
| 4 | Slice ko copy samajhna | mutation "ghair-mutawaqqa" jagah dikhti hai | `arr[1:5].copy()` |
| 5 | `as_strided` me shape khud se ghalat dena | out-of-bounds read, segfault | `sliding_window_view` |
| 6 | Non-contiguous array par hot loop | har call par chupki copy | shuru me `ascontiguousarray` |
| 7 | `np.tile` se broadcasting "manually" karna | GB memory zaya | seedha broadcasting |
| 8 | `flatten()` bar bar call karna | har dafa poori copy | `ravel()` (contiguous par view) |
| 9 | Big-endian data ko default se parhna | numbers kachra | `dtype='>i4'` batao |
| 10 | `broadcast_to` ke natije me likhne ki koshish | `ValueError` | `.copy()` pehle |
"""))

A(code("""
# Gotcha #4 aur #8 ka live muqabla: ravel vs flatten
contig = np.arange(6).reshape(2, 3)

r = contig.ravel()        # contiguous hai -> VIEW (muft)
f = contig.flatten()      # HAMESHA copy (mehnga)

print("ravel   view hai?", np.shares_memory(contig, r))
print("flatten view hai?", np.shares_memory(contig, f), " <- hamesha copy")
print()

# Non-contiguous par ravel bhi copy karne par majboor hai
noncontig2 = contig[:, ::2]
r2 = noncontig2.ravel()
print("non-contiguous par ravel view hai?", np.shares_memory(noncontig2, r2), " <- majboori me copy")
print()

# Speed ka farq bare array par
big_c = rng.random((1000, 1000))
t_ravel = bench(lambda: big_c.ravel())
t_flat = bench(lambda: big_c.flatten())
print(f"ravel   (view) : {t_ravel:7.4f} ms")
print(f"flatten (copy) : {t_flat:7.4f} ms")
print(f"ravel taqreeban {t_flat / max(t_ravel, 1e-9):.0f}x tez (kyun ke kuch kaam hi nahi karta)")

assert np.shares_memory(contig, r)
assert not np.shares_memory(contig, f)
"""))

A(code("""
# Gotcha: in-place operation dtype ko badal NAHI sakta (bohat aam trap)
int_arr2 = np.arange(5)                      # int64
print("int array:", int_arr2, int_arr2.dtype)

try:
    int_arr2 += 0.5                          # float ko int me in-place jama karne ki koshish
except Exception as e:
    print()
    print("int_arr2 += 0.5 ->", type(e).__name__)
    print("  ", str(e)[:100])
    print("  ^ In-place op ka natija USI buffer me aana hai, jo int64 hai.")
    print("    float ko int me 'same_kind' cast nahi mana jata -> error.")

print()
# Hal 1: naya array (dtype khud float ban jayega)
fixed1 = int_arr2 + 0.5
print("hal 1: int_arr2 + 0.5 =", fixed1, fixed1.dtype)

# Hal 2: shuru se float dtype
fixed2 = np.arange(5, dtype=np.float64)
fixed2 += 0.5
print("hal 2: float array par += 0.5 =", fixed2)

assert fixed1.dtype == np.float64
assert np.allclose(fixed2, [0.5, 1.5, 2.5, 3.5, 4.5])
print()
print("SABAQ: '+=' sirf tez nahi hota -- wo dtype ke bare me SAKHT bhi hota hai. Ye achi baat hai.")
"""))

# ==END==

save(r"Numpy/Advance/01_Memory_Strides_Views_aur_Internals.ipynb", C)
