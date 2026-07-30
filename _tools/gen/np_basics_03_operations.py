import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

CELLS = []
A = CELLS.append

# ============================================================
# 1. TITLE
# ============================================================
A(md("""
# 03 — Operations, Broadcasting aur Aggregations (NumPy)

**Level:** Beginner → Intermediate → Interview-ready

## Is notebook me kya seekhenge (roadmap)
1. Vectorization — loop vs vectorized code, kyun NumPy tez hai
2. Element-wise arithmetic, in-place operations aur dtype traps
3. Comparison & logical operators (aur operator precedence trap)
4. Ufuncs ki poori tour — sqrt, exp, log family, trig, rounding, power, mod/fmod, reciprocal, ufunc attributes
5. Broadcasting — rules, examples, memory considerations, practical use-cases
6. Axis ka mental model (0/1/2, tuple axis, keepdims)
7. Aggregations — sum/mean/std/var/percentile/cumsum/argmin/argmax + NaN-safe versions
8. `np.where`, `np.select`, `np.piecewise`
9. Sorting (`argsort`, `take_along_axis`, top-k idea)
10. Dot product & `@` (matmul vs elementwise)
11. Floating point rounding & equality (`isclose`, `allclose`)
12. Real-World Problems, LeetCode Problems, Interview Q&A, Practice Exercises, Cheat-sheet

## Prerequisites
- **NB1** — NumPy introduction, array creation (`array`, `zeros`, `arange`, `linspace`, dtypes)
- **NB2** — Indexing, slicing, fancy indexing, boolean masks, views vs copies

Is notebook me hum maan kar chal rahe hain ke aap upar wale dono topics se comfortable hain.
Chaliye shuru karte hain!
"""))

A(md("""
## 0. Setup

Pura notebook me ek hi random generator (`rng`) use karenge taake results **reproducible** rahein
(seed = 42). Jahan bhi random data chahiye, `rng` se hi lenge.
"""))

A(code("""
import numpy as np
import timeit

rng = np.random.default_rng(42)  # fixed seed -> pura notebook me reproducible randomness
print("NumPy version:", np.__version__)
"""))

# ============================================================
# 2. VECTORIZATION
# ============================================================
A(md("""
## 1. Vectorization — Kya hai, Kyun

**Kya hai:** Vectorization matlab element-wise operation Python `for` loop likhe baghair,
poore array par ek hi call me apply karna — jaise `arr * 2` (loop ki zaroorat nahi).

**Kyun tez hota hai (C loop wajah):**
- NumPy arrays **contiguous memory block** me hote hain (ek hi type ke elements, back-to-back).
- Operation ek compiled **C loop** me chalta hai — Python interpreter ka per-iteration overhead nahi.
- Modern CPUs **SIMD** instructions (ek hi cycle me multiple numbers process) use kar sakte hain
  jab data contiguous ho.
- Python `for` loop me har element ek Python object (box/unbox overhead) hota hai — bohat slow.

**Syntax:** bas normal operators (`+ - * /` etc.) array par lagao.

**Interview tip:** "Vectorization" ka matlab yeh nahi ke code parallel chal raha hai (zaroori nahi) —
matlab ye hai ke loop Python me nahi, C me chal raha hai.
"""))

A(code("""
# Chalta hua example: pure python loop vs vectorized numpy
n = 100_000
arr_vec = np.arange(n, dtype=np.float64)

def python_loop():
    out = []
    for x in arr_vec:          # Python level loop -> har element par overhead
        out.append(x * 2 + 1)
    return out

def vectorized():
    return arr_vec * 2 + 1     # C loop ke andar chalta hai

# NOTE: hum sirf print kar rahe hain, timing par ASSERT nahi lagate (machine-dependent hota hai)
t_loop = timeit.timeit("python_loop()", globals=globals(), number=3)
t_vec = timeit.timeit("vectorized()", globals=globals(), number=3)
print(f"pure python loop (3 runs): {t_loop:.4f} sec")
print(f"vectorized numpy (3 runs): {t_vec:.4f} sec")
print("Gotcha: vectorized hamesha tez hoti hai (contiguous memory + C loop + SIMD + no per-element")
print("Python object overhead) — is notebook me hum yehi principle baar baar use karenge.")
"""))

# ============================================================
# 3. ELEMENT-WISE ARITHMETIC
# ============================================================
A(md("""
## 2. Element-wise Arithmetic

**Kya hai:** `+ - * / // % **` sab element-wise chalte hain (matching shape par), ya broadcasting
ke through (scalar sabse simple broadcasting case hai).

**Kyun:** Har element independently process hota hai — ye NumPy ka core building block hai.

**Syntax:** `a + b`, `a - b`, `a * b`, `a / b` (true divide), `a // b` (floor divide), `a % b` (mod),
`a ** b` (power).

**Gotcha:** integer `/` (true divide) ka result **hamesha float** hota hai, integer `//` ka result
integer hi rehta hai (agar dono operand int hon).
"""))

A(code("""
a = np.array([10, 20, 30, 40])
b = np.array([3, 4, 5, 6])

print("a + b  =", a + b)
print("a - b  =", a - b)
print("a * b  =", a * b)
print("a / b  =", a / b, " dtype:", (a / b).dtype)   # true divide -> float64
print("a // b =", a // b, " dtype:", (a // b).dtype) # floor divide -> int rehta hai
print("a % b  =", a % b)
print("a ** 2 =", a ** 2)

# scalar broadcasting -> sabse simple case (scalar har element par apply hota hai)
print("a + 100 =", a + 100)
print("a * 2   =", a * 2)
"""))

A(code("""
# Integer division by zero -> warning aata hai (crash nahi), np.errstate se suppress karte hain
a = np.array([10, 20, 30])
b = np.array([2, 0, 5])

with np.errstate(divide="ignore", invalid="ignore"):
    floor_result = a // b   # integer floor-divide by zero -> 0 result (with warning suppressed)
    true_result = a / b     # true divide by zero -> inf (float dtype ban jata hai)

print("a // b (zero-safe print):", floor_result)
print("a / b  (zero-safe print):", true_result, " dtype:", true_result.dtype)
print("Gotcha: integer array / integer array me zero-division silently 0 ya inf de deta hai,")
print("exception NAHI aati — isliye np.errstate se warning dikhana/suppress karna zaroori hai.")
"""))

# ============================================================
# 4. IN-PLACE OPS
# ============================================================
A(md("""
## 3. In-place Operations (`+=`, `*=`, ...)

**Kya hai:** `a += b` naya array nahi banata — same memory me values update karta hai
(`a = a + b` naya array banata hai, phir `a` us naye array ko point karta hai — farق important hai).

**Kyun:** Memory saving — bare arrays ke sath naya allocation avoid karta hai.

**Gotcha (bohat zaroori):** in-place op saare **views** ko bhi update kar deta hai (kyunke memory
shared hoti hai). Aur agar array ka dtype `int` hai aur aap usme `float` in-place add karo, to
**`UFuncTypeError`** aata hai (dtype "same_kind" casting rule violate hoti hai) — jabke
`a = a + 0.5` (naya array) bilkul chal jata — kyunke wahan naya float array ban jata hai.
"""))

A(code("""
a = np.array([1, 2, 3])
view_of_a = a[:]          # ye ek VIEW hai, copy nahi
a += 10                   # in-place -> same memory update
print("a          =", a)
print("view_of_a  =", view_of_a, "  (view bhi badal gaya kyunke memory shared hai)")
assert np.array_equal(a, view_of_a)
"""))

A(code("""
# dtype trap: integer array me float in-place add
a = np.arange(3)          # dtype int64
print("a dtype:", a.dtype)
try:
    a += 0.5               # UFuncTypeError -> int array me float in-place allowed nahi
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

# lekin naya array banane se (in-place nahi) bilkul chal jata hai:
b = np.arange(3)
b = b + 0.5                # naya float64 array bana, dtype change ho gaya
print("b (naya array, float ban gaya):", b, b.dtype)
print("Interview tip: '+=' dtype badal nahi sakta (same array memory), '=' naya array bana kar")
print("dtype badal sakta hai.")
"""))

# ============================================================
# 5. COMPARISON OPERATORS
# ============================================================
A(md("""
## 4. Comparison Operators → Boolean Arrays

**Kya hai:** `== != < <= > >=` element-wise boolean array dete hain (Python ke `==` jaisa
scalar bool nahi).

**`==` vs `is`:** `a == b` element-wise comparison (naya boolean array), `a is b` sirf yeh check
karta hai ke dono NAAM same object ko point karte hain ya nahi.

**Gotcha:** `if arr:` jab `arr` me 1 se zyada elements hon to **`ValueError`** deta hai
("truth value ... ambiguous") — `.any()` ya `.all()` use karo.
"""))

A(code("""
a = np.array([1, 2, 3])
b = np.array([3, 2, 1])

print("a == b        :", a == b)          # element-wise -> [False True False]
print("a < b         :", a < b)
print("np.array_equal:", np.array_equal(a, b))   # poora array barabar hai ya nahi (single bool)

c = np.array([1, 2, 3])
d = np.array([1, 2, 3])
print("c == d :", c == d)      # elementwise [True True True]
print("c is d :", c is d)      # False -> alag objects hain (chahe values same hon)
print("np.array_equal(c, d):", np.array_equal(c, d))   # True
"""))

A(code("""
# 'if arr:' ambiguous truth value gotcha
arr = np.array([1, 2, 3])
try:
    if arr:                    # ValueError -> array me >1 element, truth value ambiguous
        print("truthy")
except ValueError as e:
    print(f"Error: {e}")

# sahi tareeqa:
print("arr.any():", arr.any())   # koi bhi element truthy hai?
print("arr.all():", arr.all())   # sab elements truthy hain?
"""))

# ============================================================
# 6. LOGICAL FUNCTIONS + PRECEDENCE TRAP
# ============================================================
A(md("""
## 5. Logical Functions — `logical_and/or/not/xor` aur `& | ~`

**Kya hai:** Boolean arrays ko combine karne ke liye `np.logical_and`, `np.logical_or`,
`np.logical_not`, `np.logical_xor` — ya operators `&` (and), `|` (or), `~` (not).

**Gotcha — Operator Precedence Trap (bohat common interview/debugging mistake):**
Python me `&` `|` ka precedence comparison operators (`> < ==`) se **zyada** hota hai.
Isliye `a > 1 & b < 3` **galat** parse hota hai — brackets lazmi hain: `(a > 1) & (b < 3)`.
"""))

A(code("""
a = np.array([1, 2, 3, 4])
b = np.array([3, 3, 1, 5])

print("logical_and:", np.logical_and(a > 1, b < 4))
print("logical_or :", np.logical_or(a > 3, b > 3))
print("logical_not:", np.logical_not(a > 2))
print("logical_xor:", np.logical_xor(a > 2, b > 2))

# operator form (& | ~) bhi same karte hain, lekin brackets zaroori hain
print("(a>1) & (b<4):", (a > 1) & (b < 4))
"""))

A(code("""
# Precedence trap demo: brackets ke baghair
a = np.array([1, 2, 3, 4])
b = np.array([3, 3, 1, 5])
try:
    # '&' ki precedence '>' '<' se zyada hai -> ye asal me "a > (1 & b) < 3" ban jata hai
    # jo chained comparison hai: (a > (1&b)) and ((1&b) < 3) -> arrays par 'and' -> ambiguous
    result = a > 1 & b < 3
    print(result)
except ValueError as e:
    print(f"Error (precedence trap): {e}")

# sahi tareeqa -> hamesha brackets lagao
correct = (a > 1) & (b < 3)
print("Sahi (with brackets):", correct)
"""))

# ============================================================
# 7. UFUNCS TOUR
# ============================================================
A(md("""
## 6. Ufuncs ki Tour

Ufunc (universal function) matlab element-wise C-level function jo broadcasting bhi support
karti hai. Chaliye common ufuncs dekhte hain, ek ek karke.

### 6.1 sqrt, exp, log family
- `np.sqrt` — negative number par `nan` deta hai (warning ke sath, `errstate` se handle karo).
- `np.exp` — e^x.
- `np.log` (natural log), `np.log2`, `np.log10`, **`np.log1p`** (= `log(1+x)`, lekin chhoti `x`
  values ke liye zyada precise hai kyunke `1 + x` khud precision loss kar sakta hai).
"""))

A(code("""
with np.errstate(invalid="ignore"):
    print("sqrt([4,-1,9]) :", np.sqrt(np.array([4.0, -1.0, 9.0])))   # nan for negative

print("exp([0,1,2])   :", np.exp(np.array([0, 1, 2])))
print("log([1,e,10])  :", np.log(np.array([1, np.e, 10])))
print("log2([1,2,8])  :", np.log2(np.array([1, 2, 8])))
print("log10([1,10,1000]):", np.log10(np.array([1, 10, 1000])))

# log1p ka faida -> bohat choti x ke liye precision
x_small = 1e-12
print(f"log1p(x)     : {np.log1p(x_small):.18f}")
print(f"log(1+x)     : {np.log(1 + x_small):.18f}  (precision kho gayi, 1+x round ho gaya)")
"""))

A(md("""
### 6.2 Trigonometric functions
`np.sin/cos/tan` **radians** expect karte hain — degrees se convert karne ke liye `np.deg2rad`.
"""))

A(code("""
degrees = np.array([0, 30, 45, 60, 90])
radians = np.deg2rad(degrees)   # degree -> radian conversion
print("radians:", radians)
print("sin:", np.round(np.sin(radians), 4))
print("cos:", np.round(np.cos(radians), 4))
print("tan:", np.round(np.tan(radians), 4))
"""))

A(md("""
### 6.3 abs, sign
"""))

A(code("""
vals = np.array([-3, 2, -1, 0, 7])
print("abs :", np.abs(vals))
print("sign:", np.sign(vals))    # -1, 0, +1
"""))

A(md("""
### 6.4 Rounding family — `round/floor/ceil/trunc/rint`

**Gotcha (Banker's Rounding):** `np.round` "round half to even" use karta hai, standard
"round half up" nahi! Isliye `np.round(0.5) == 0.0` (0 even hai), `np.round(1.5) == 2.0`,
`np.round(2.5) == 2.0` (2 even hai, 3 nahi).
"""))

A(code("""
vals = np.array([0.5, 1.5, 2.5, -0.5, -1.5])
print("round:", np.round(vals))   # banker's rounding -> [0. 2. 2. -0. -2.]
print("floor:", np.floor(vals))
print("ceil :", np.ceil(vals))
print("trunc:", np.trunc(vals))   # zero ki taraf truncate
print("rint :", np.rint(vals))    # round jaisa hi (nearest even)

assert np.round(0.5) == 0.0   # gotcha verify -> 0 (not 1!)
assert np.round(2.5) == 2.0   # gotcha verify -> 2 (not 3!)
print("Confirmed: np.round '0.5' ko 0 aur '2.5' ko 2 round karta hai (banker's rounding).")
"""))

A(md("""
### 6.5 `np.clip` — values ko range me bandh dena
"""))

A(code("""
a = np.array([1, 5, 10, -3, 20, 7])
clipped = np.clip(a, 0, 10)   # har value ko [0, 10] range me force karo
print("original:", a)
print("clipped :", clipped)
assert clipped.min() >= 0 and clipped.max() <= 10
"""))

A(md("""
### 6.6 `np.power` — integer negative exponent gotcha
Integer array ko negative integer power par raise karna **`ValueError`** deta hai
(kyunke result fractional hota, integer dtype me store nahi ho sakta). Float array ke sath theek chalta hai.
"""))

A(code("""
try:
    print(np.power(np.array([2, 3], dtype=int), -2))   # ValueError
except ValueError as e:
    print(f"Error: {e}")

# float array ke sath theek chalta hai
print("float power:", np.power(np.array([2.0, 3.0]), -2))
"""))

A(md("""
### 6.7 `np.maximum`/`np.minimum` (element-wise) vs `np.max`/`np.min` (reduction)

Ye interview me **bohat** poocha jata hai:
- `np.maximum(a, b)` — do arrays ke beech, element-wise bara wala choose karta hai (shape same rehti hai).
- `np.max(a)` — ek array ko **reduce** kar ke ek scalar (ya kam-dimension array agar axis diya ho) deta hai.
"""))

A(code("""
a = np.array([1, 5, 3])
b = np.array([4, 2, 6])

print("np.maximum(a, b):", np.maximum(a, b))   # element-wise -> [4 5 6]
print("np.minimum(a, b):", np.minimum(a, b))   # element-wise -> [1 2 3]
print("np.max(a)       :", np.max(a))          # reduction -> scalar 5
print("np.min(b)       :", np.min(b))          # reduction -> scalar 2
print("Gotcha: 'maximum/minimum' do arrays compare karte hain; 'max/min' EK array ko reduce karte hain.")
"""))

A(md("""
### 6.8 `np.mod` vs `np.fmod` — negative numbers ka farq
- `np.mod` — Python `%` jaisa, result ka sign **divisor** ke sath match karta hai.
- `np.fmod` — C `fmod` jaisa, result ka sign **dividend** ke sath match karta hai.
"""))

A(code("""
print("np.mod(-7, 3) :", np.mod(-7, 3))    # 2  (sign follows divisor 3)
print("np.fmod(-7, 3):", np.fmod(-7, 3))   # -1 (sign follows dividend -7)
print("np.mod(7, -3) :", np.mod(7, -3))    # -2
print("np.fmod(7, -3):", np.fmod(7, -3))   # 1
"""))

A(md("""
### 6.9 `np.reciprocal` — integer dtype trap
Integer array par `reciprocal` **integer truncation** karta hai — `1/x` floor ho jata hai
(sirf `x=1` ke liye 1 result deta hai, baaqi sab `0`!). Float array ke sath sahi kaam karta hai.
"""))

A(code("""
int_arr = np.array([1, 2, 3, 4])
float_arr = np.array([1.0, 2.0, 3.0, 4.0])
print("reciprocal(int)  :", np.reciprocal(int_arr))     # [1 0 0 0] -> galat lagta hai par integer truncation hai
print("reciprocal(float):", np.reciprocal(float_arr))   # [1. 0.5 0.333.. 0.25] -> sahi
print("Gotcha: integer array par reciprocal use karne se pehle float me convert karo (.astype(float))")
"""))

A(md("""
### 6.10 Ufunc attributes — `.reduce`, `.accumulate`, `.outer`, `.nin`/`.nout`
Har ufunc ke andar built-in reduction tools hote hain.
"""))

A(code("""
nums = np.array([1, 2, 3, 4])

print("np.add.reduce    :", np.add.reduce(nums))        # sum jaisa -> 10
print("np.add.accumulate:", np.add.accumulate(nums))     # cumsum jaisa -> [1 3 6 10]
print("np.add.outer     :\\n", np.add.outer(np.array([1, 2, 3]), np.array([10, 20])))  # outer sum matrix
print("np.add.nin, nout :", np.add.nin, np.add.nout)     # 2 inputs, 1 output

assert np.add.reduce(nums) == np.sum(nums)
assert np.array_equal(np.add.accumulate(nums), np.cumsum(nums))
"""))

# ============================================================
# 8. BROADCASTING
# ============================================================
A(md("""
## 7. Broadcasting — Deep Dive

**Kya hai:** Broadcasting NumPy ka rule-set hai jisse **different shapes** ke arrays ke beech
bhi arithmetic ho sakti hai — bina data copy kiye (jahan tak mumkin ho).

**Rules (step by step, dono shapes ko right se compare karo):**
1. Dono shapes ko **trailing (right-most) dimension** se align karo.
2. Agar kisi dimension me size **1** hai, wo doosri shape ke us dimension ke barabar **stretch**
   ho jati hai.
3. Agar ek shape **choti** hai (kam dimensions), uske **left side** me missing dimensions ko
   size **1** samjha jata hai.
4. Agar kisi dimension par sizes match nahi karti (aur dono me se koi 1 nahi hai) — **error**.
"""))

A(md("""
### 7.1 Examples (shape table)

| Shape A       | Shape B     | Result Shape  | Kyun |
|---------------|-------------|----------------|------|
| (3, 4)        | (4,)        | (3, 4)         | B left-pad -> (1,4), phir 1->3 stretch |
| (3, 1)        | (1, 4)      | (3, 4)         | dono dimensions me 1 stretch hoti hai |
| (5, 1, 4)     | (3, 4)      | (5, 3, 4)      | B left-pad -> (1,3,4), phir 1->5 |
| (8, 1, 6, 1)  | (7, 1, 5)   | (8, 7, 6, 5)   | classic NumPy docs example |
"""))

A(code("""
r1 = np.ones((3, 4)) + np.ones((4,))
print("(3,4)+(4,)         ->", r1.shape)

r2 = np.ones((3, 1)) + np.ones((1, 4))
print("(3,1)+(1,4)        ->", r2.shape)

r3 = np.ones((5, 1, 4)) + np.ones((3, 4))
print("(5,1,4)+(3,4)      ->", r3.shape)

r4 = np.ones((8, 1, 6, 1)) + np.ones((7, 1, 5))
print("(8,1,6,1)+(7,1,5)  ->", r4.shape)

assert r1.shape == (3, 4)
assert r2.shape == (3, 4)
assert r3.shape == (5, 3, 4)
assert r4.shape == (8, 7, 6, 5)
"""))

A(md("""
### 7.2 Shape mismatch error
Agar koi dimension match nahi karti (aur 1 nahi hai) to `ValueError` aata hai.
"""))

A(code("""
try:
    np.ones((3, 4)) + np.ones((3, 5))   # last dim: 4 vs 5, koi bhi 1 nahi -> error
except ValueError as e:
    print(f"Error: {e}")
"""))

A(md("""
### 7.3 `np.broadcast_shapes` — bina array banaye result shape pata karo
"""))

A(code("""
print(np.broadcast_shapes((5, 1, 4), (3, 4)))          # (5, 3, 4)
print(np.broadcast_shapes((8, 1, 6, 1), (7, 1, 5)))     # (8, 7, 6, 5)
try:
    np.broadcast_shapes((3, 4), (3, 5))
except ValueError as e:
    print(f"Error: {e}")
"""))

A(md("""
### 7.4 `np.broadcast_to` — read-only view (writeable=False gotcha)
`broadcast_to` naya data allocate nahi karta — sirf ek "virtual" bara view banata hai, isliye
result **read-only** hota hai. Likhne ki koshish `ValueError` degi.
"""))

A(code("""
a = np.array([1, 2, 3])
b = np.broadcast_to(a, (3, 3))   # (3,) -> (3,3) bina data copy kiye
print(b)
print("writeable:", b.flags.writeable)   # False

try:
    b[0, 0] = 100
except ValueError as e:
    print(f"Error: {e}")
"""))

A(md("""
### 7.5 Kab memory blow ho sakti hai
Broadcasting bohat bara result bhi bana sakta hai — likhne se pehle size ka andaza laga lo!
Neeche hum sirf **hisaab** kar rahe hain, actual array allocate nahi kar rahe.
"""))

A(code("""
shape_a = (10_000, 1)
shape_b = (1, 10_000)
result_shape = np.broadcast_shapes(shape_a, shape_b)
n_elements = int(np.prod(result_shape))
n_bytes = n_elements * 8   # float64 = 8 bytes per element
print(f"result shape : {result_shape}")
print(f"elements     : {n_elements:,}")
print(f"memory needed: {n_bytes / 1e6:.1f} MB  (agar float64 me allocate karte)")
print("Gotcha: (10000,1) aur (1,10000) chhote lagte hain, par unka broadcast result 1e8 elements")
print("(sau MB+) ban jata hai -- allocate karne se pehle hamesha shape/size soch lo.")
"""))

A(md("""
### 7.6 `np.newaxis` se broadcasting control karna
`np.newaxis` (== `None`) se hum manually ek naya axis daal kar broadcasting ka shape control
karte hain.
"""))

A(code("""
a = np.array([1, 2, 3])
print("a[:, np.newaxis].shape:", a[:, np.newaxis].shape)   # (3,1) -> column vector
print("a[np.newaxis, :].shape:", a[np.newaxis, :].shape)    # (1,3) -> row vector
"""))

A(md("""
### 7.7 Practical use: Row-wise normalize (mean/std with `keepdims`)
"""))

A(code("""
X = rng.normal(loc=5, scale=2, size=(4, 3))   # 4 samples, 3 features
row_mean = X.mean(axis=1, keepdims=True)      # keepdims=True -> shape (4,1) rehti hai, broadcasting ke liye
row_std = X.std(axis=1, keepdims=True)
X_row_norm = (X - row_mean) / row_std

print("row means after normalize (~0):", np.round(X_row_norm.mean(axis=1), 10))
assert np.allclose(X_row_norm.mean(axis=1), 0, atol=1e-10)
"""))

A(md("""
### 7.8 Practical use: Outer product
"""))

A(code("""
a = np.array([1, 2, 3])
b = np.array([10, 20])

outer_broadcast = a[:, None] * b[None, :]   # (3,1)*(1,2) broadcasting -> (3,2)
outer_builtin = np.outer(a, b)
print(outer_broadcast)
assert np.array_equal(outer_broadcast, outer_builtin)
"""))

A(md("""
### 7.9 Practical use: Pairwise Euclidean distance matrix (bina loop)
"""))

A(code("""
pts = rng.normal(size=(5, 2))   # 5 points in 2D
diff = pts[:, None, :] - pts[None, :, :]     # shape (5,5,2) -> broadcasting se sab pairs ka diff
dist_matrix = np.sqrt((diff ** 2).sum(axis=-1))   # (5,5) -> pairwise distances

print("shape:", dist_matrix.shape)
print(np.round(dist_matrix, 2))
assert np.allclose(np.diag(dist_matrix), 0)          # apne aap se distance 0 honi chahiye
assert np.allclose(dist_matrix, dist_matrix.T)        # symmetric honi chahiye
"""))

A(md("""
### 7.10 Practical use: One-hot encoding (broadcasting se, bina loop)
"""))

A(code("""
labels = np.array([0, 2, 1, 0, 3])
k = 4   # total classes
one_hot = (labels[:, None] == np.arange(k)).astype(int)   # (5,1)==(4,) -> broadcasting -> (5,4)
print(one_hot)
assert np.array_equal(one_hot.argmax(axis=1), labels)
"""))

# ============================================================
# 9. AXIS MENTAL MODEL
# ============================================================
A(md("""
## 8. Axis ka Mental Model

**Sabse asaan tareeqa yaad rakhne ka:** jis axis number do, wo axis **collapse/gayab** ho jati
hai result me — result me baqi axes reh jati hain.

- 2D array `(rows, cols)`: `axis=0` → **rows collapse** (per-column result, shape `(cols,)`).
  `axis=1` → **cols collapse** (per-row result, shape `(rows,)`).
- `keepdims=True` — collapsed axis ko size-1 rakhta hai (gayab nahi karta) — taake baad me
  original array ke sath broadcasting asaan ho.
"""))

A(code("""
mat = np.array([[1, 2, 3],
                [4, 5, 6]])   # shape (2,3) -> 2 rows, 3 cols

print("mat.sum(axis=0):", mat.sum(axis=0), " <- rows collapse, per-COLUMN sum, shape:", mat.sum(axis=0).shape)
print("mat.sum(axis=1):", mat.sum(axis=1), " <- cols collapse, per-ROW sum, shape:", mat.sum(axis=1).shape)
print("keepdims=True  :", mat.sum(axis=1, keepdims=True).shape, " <- shape (2,1) rehta hai, gayab nahi hota")
"""))

A(code("""
# 3D example
arr3d = np.arange(24).reshape(2, 3, 4)   # shape (2,3,4)
print("original shape       :", arr3d.shape)
print("sum axis=0 shape     :", arr3d.sum(axis=0).shape)      # (3,4) -> axis0 (size2) collapse
print("sum axis=1 shape     :", arr3d.sum(axis=1).shape)      # (2,4) -> axis1 (size3) collapse
print("sum axis=2 shape     :", arr3d.sum(axis=2).shape)      # (2,3) -> axis2 (size4) collapse
print("sum axis=(0,1) shape :", arr3d.sum(axis=(0, 1)).shape) # (4,)  -> dono collapse (tuple axis)
print("sum axis=1 keepdims  :", arr3d.sum(axis=1, keepdims=True).shape)  # (2,1,4)
"""))

# ============================================================
# 10. AGGREGATIONS
# ============================================================
A(md("""
## 9. Aggregations

### 9.1 Basic stats + `ddof` (population vs sample)
`std`/`var` ka default `ddof=0` (**population**). Sample standard deviation ke liye `ddof=1`
use karo (denominator `n-1` ho jata hai — Bessel's correction).
"""))

A(code("""
data = np.array([2, 4, 4, 4, 5, 5, 7, 9])

print("sum   :", np.sum(data))
print("prod  :", np.prod(data[:4]))   # chhoti slice (warna number bohat bara ho jata)
print("mean  :", np.mean(data))
print("median:", np.median(data))
print("std (ddof=0, population):", np.std(data))
print("std (ddof=1, sample)    :", np.std(data, ddof=1))
print("var (ddof=0):", np.var(data), "  var (ddof=1):", np.var(data, ddof=1))
"""))

A(md("""
### 9.2 `np.ptp`, `percentile`, `quantile`
**Gotcha:** NumPy 2.x me `arr.ptp()` **method hata diya gaya** — sirf `np.ptp(arr)` function form
use karo. `percentile` 0-100 scale leta hai, `quantile` 0-1 scale.
"""))

A(code("""
print("ptp (max-min):", np.ptp(data))          # function form -> arr.ptp() AttributeError dega numpy2 me
print("50th percentile:", np.percentile(data, 50))
print("0.5 quantile   :", np.quantile(data, 0.5))     # same as 50th percentile
assert np.percentile(data, 50) == np.quantile(data, 0.5) == np.median(data)
"""))

A(md("""
### 9.3 Cumulative aggregations
"""))

A(code("""
small = np.array([1, 2, 3, 4])
print("cumsum :", np.cumsum(small))
print("cumprod:", np.cumprod(small))
"""))

A(md("""
### 9.4 `argmin`/`argmax` + `np.unravel_index` (2D ke liye), `count_nonzero`
`argmax`/`argmin` **flat index** dete hain multi-dim array par — asal (row, col) nikalne ke liye
`np.unravel_index` use karo.
"""))

A(code("""
mat = rng.integers(0, 100, size=(3, 4))
print(mat)

flat_idx = np.argmax(mat)
row, col = np.unravel_index(flat_idx, mat.shape)
print(f"flat argmax index: {flat_idx} -> (row={row}, col={col}) -> value={mat[row, col]}")
assert mat[row, col] == mat.max()

nz = np.array([0, 1, 2, 0, 3, 0])
print("count_nonzero:", np.count_nonzero(nz))
"""))

A(md("""
### 9.5 NaN-safe versions — `nansum, nanmean, nanstd, nanmin, nanmax, nanargmax, nanmedian`
**Bina** nan-safe function ke, agar array me ek bhi `nan` ho to result **poora `nan`** ban jata hai
(NaN "propagate" karta hai)!
"""))

A(code("""
data_nan = np.array([1.0, 2.0, np.nan, 4.0, 5.0])

print("np.sum   (galat, propagate):", np.sum(data_nan))
print("np.nansum(sahi)            :", np.nansum(data_nan))
print("np.mean   (galat)          :", np.mean(data_nan))
print("np.nanmean(sahi)           :", np.nanmean(data_nan))
print("np.nanstd, nanmin, nanmax  :", np.nanstd(data_nan), np.nanmin(data_nan), np.nanmax(data_nan))
print("np.nanargmax               :", np.nanargmax(data_nan))
print("np.nanmedian                :", np.nanmedian(data_nan))

assert not np.isnan(np.nanmean(data_nan))
assert np.isnan(np.mean(data_nan))
"""))

# ============================================================
# 11. WHERE / SELECT / PIECEWISE
# ============================================================
A(md("""
## 10. `np.where`, `np.select`, `np.piecewise`

- `np.where(cond, a, b)` — 3-argument form: `cond` jahan True wahan `a`, jahan False wahan `b`.
- `np.select(conditions_list, choices_list, default=...)` — **multiple** conditions ek sath
  (`where` ki jagah jab 2 se zyada cases hon).
- `np.piecewise(x, conditions, functions)` — har condition ke liye alag function apply karta hai.
"""))

A(code("""
a = np.array([1, -2, 3, -4, 5])
abs_via_where = np.where(a > 0, a, -a)   # 3-arg where -> custom abs()
print("abs via where:", abs_via_where)
assert np.array_equal(abs_via_where, np.abs(a))

# nested where -> 3 categories
b = np.array([-5, 0, 5])
categories = np.where(b < 0, "neg", np.where(b == 0, "zero", "pos"))
print("categories:", categories)

# where + broadcasting
mat = np.arange(6).reshape(2, 3)
row_thresh = np.array([1, 3])[:, None]   # (2,1) -> broadcast against (2,3)
print(np.where(mat > row_thresh, mat, 0))
"""))

A(code("""
scores = np.array([95, 82, 67, 45, 30])
conditions = [scores >= 90, scores >= 75, scores >= 60, scores >= 40]
choices = ["A", "B", "C", "D"]
grades = np.select(conditions, choices, default="F")   # multiple conditions ek sath
print("grades:", grades)
assert list(grades) == ["A", "B", "C", "D", "F"]
"""))

A(code("""
# np.piecewise -> chhota example (custom abs jaisa function, alag formula alag range me)
x = np.array([-2, -1, 0, 1, 2])
y = np.piecewise(x, [x < 0, x >= 0], [lambda v: -v, lambda v: v * 2])
print("piecewise result:", y)   # negative -> -x, non-negative -> 2x
"""))

# ============================================================
# 12. SORTING
# ============================================================
A(md("""
## 11. Sorting — `argsort` per axis, `take_along_axis`, top-k idea

`argsort` sorted **indices** deta hai (values nahi). `np.take_along_axis` un indices se values
wapis nikalne ka sahi tareeqa hai (multi-dim ke liye).
"""))

A(code("""
mat = rng.integers(0, 50, size=(3, 4))
print("original:\\n", mat)

sorted_rows = np.sort(mat, axis=1)              # har row sort
idx = np.argsort(mat, axis=1)                    # har row ke liye sorted indices
reconstructed = np.take_along_axis(mat, idx, axis=1)   # indices se values wapis nikalna
assert np.array_equal(sorted_rows, reconstructed)
print("sorted (via sort)       :\\n", sorted_rows)
print("sorted (via argsort+take):\\n", reconstructed)

# top-k idea: har row ke sabse bare k=2 elements
k = 2
topk_idx = np.argsort(mat, axis=1)[:, -k:]              # last k sorted indices = sabse bare
topk_vals = np.take_along_axis(mat, topk_idx, axis=1)
print(f"top-{k} per row:\\n", topk_vals)
"""))

# ============================================================
# 13. DOT / @
# ============================================================
A(md("""
## 12. Dot Product & `@` — matmul vs elementwise `*`

- `np.dot(a, b)` / `a @ b` — **matrix multiplication** (1D par: scalar/inner product).
- `a * b` — **element-wise** multiplication (shape same rehti hai, broadcasting ke sath).
- 2D `@` 2D: shape rule `(m,n) @ (n,p) -> (m,p)` — inner dimensions match honi chahiye.
"""))

A(code("""
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
print("np.dot(v1,v2):", np.dot(v1, v2), "  v1 @ v2:", v1 @ v2)   # 1D dot -> scalar (32)
print("v1 * v2 (elementwise):", v1 * v2)                          # [4 10 18], NOT scalar

A_mat = np.array([[1, 2], [3, 4]])
B_mat = np.array([[5, 6], [7, 8]])
print("A @ B (matmul):\\n", A_mat @ B_mat)
print("np.dot(A,B)  :\\n", np.dot(A_mat, B_mat))
print("A * B (elementwise, DIFFERENT!):\\n", A_mat * B_mat)

assert (v1 @ v2) == np.dot(v1, v2) == 32
assert np.array_equal(A_mat @ B_mat, np.dot(A_mat, B_mat))
"""))

# ============================================================
# 14. ROUNDING & FLOAT EQUALITY
# ============================================================
A(md("""
## 13. Floating Point Rounding & Equality

Floating point numbers **binary** me store hote hain — kai decimal fractions (jaise 0.1) exactly
represent nahi ho sakte. Isliye `==` se float compare karna risky hai.

- `np.isclose(a, b, rtol=..., atol=...)` — element-wise "kaafi qareeb hai?" check.
- `np.allclose(a, b)` — poore array ke liye single `True/False`.
- `np.finfo(np.float64).eps` — smallest representable difference (machine epsilon).
"""))

A(code("""
print("0.1 + 0.2 == 0.3       :", 0.1 + 0.2 == 0.3)          # False! (floating point precision)
print("0.1 + 0.2              :", repr(0.1 + 0.2))
print("np.isclose(0.1+0.2,0.3):", np.isclose(0.1 + 0.2, 0.3))  # True

arr1 = np.array([0.1 + 0.2, 1.0])
arr2 = np.array([0.3, 1.0000000001])
print("np.allclose:", np.allclose(arr1, arr2, rtol=1e-5, atol=1e-8))

print("float64 eps:", np.finfo(np.float64).eps)
print("isclose with nan, equal_nan=False:", np.isclose(np.nan, np.nan))
print("isclose with nan, equal_nan=True :", np.isclose(np.nan, np.nan, equal_nan=True))
"""))

# ============================================================
# 15. GOTCHAS SUMMARY
# ============================================================
A(md("""
## 14. Common Mistakes / Gotchas — Quick Recap

1. `arr.ptp()` **method removed** in NumPy 2 → `np.ptp(arr)` function use karo.
2. Integer array me `+=` float value → **`UFuncTypeError`** (dtype cast rule); `a = a + 0.5` chalta hai.
3. `if arr:` (multi-element) → `ValueError: truth value ambiguous`; `.any()`/`.all()` use karo.
4. `a > 1 & b < 3` → precedence trap, **brackets lazmi**: `(a > 1) & (b < 3)`.
5. Integer `//`/`/ ` by zero → silently `0`/`inf` (exception nahi), `np.errstate` se dikhao.
6. `np.power(int_arr, -2)` → `ValueError` (negative int power); float array me theek chalta hai.
7. `np.reciprocal` integer array par truncate ho jata hai (`1/2 -> 0`), float me convert karo.
8. `np.round` **banker's rounding** use karta hai (`0.5 -> 0`, `2.5 -> 2`), standard rounding nahi.
9. `np.mod` vs `np.fmod` negative numbers par alag sign dete hain.
10. Bina `nan*` function ke, ek bhi `nan` poore aggregation ko `nan` bana deta hai.
11. `np.broadcast_to` result **read-only** hota hai (`writeable=False`).
12. Shape mismatch (broadcasting fail) → `ValueError: operands could not be broadcast together`.
13. Multi-element array par direct `assert arr1 == arr2` mat lagao — `np.array_equal`/`np.allclose` use karo.
14. `0.1 + 0.2 == 0.3` → `False` (floating point), `np.isclose`/`np.allclose` use karo.
"""))

# ============================================================
# 16. REAL-WORLD PROBLEMS
# ============================================================
A(md("""
## 15. Real-World Problems

### 15.1 Min-max & Z-score normalization of a feature matrix
"""))

A(code("""
X = rng.uniform(low=0, high=100, size=(6, 4))   # 6 samples x 4 features

X_minmax = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))   # per-column (axis=0) normalize
X_zscore = (X - X.mean(axis=0)) / X.std(axis=0)

print("min-max range [0,1] check:", np.allclose(X_minmax.min(axis=0), 0), np.allclose(X_minmax.max(axis=0), 1))
print("z-score mean~0 check    :", np.allclose(X_zscore.mean(axis=0), 0, atol=1e-10))

assert np.allclose(X_minmax.min(axis=0), 0)
assert np.allclose(X_minmax.max(axis=0), 1)
assert np.allclose(X_zscore.mean(axis=0), 0, atol=1e-10)
"""))

A(md("""
### 15.2 Temperature Celsius → Fahrenheit + monthly stats with axis
"""))

A(code("""
# 3 cities x 12 months (celsius readings)
celsius = rng.uniform(-5, 40, size=(3, 12)).round(1)
fahrenheit = celsius * 9 / 5 + 32   # scalar broadcasting

monthly_avg_across_cities = celsius.mean(axis=0)   # axis=0 collapses cities -> per MONTH avg
city_avg_across_year = celsius.mean(axis=1)        # axis=1 collapses months -> per CITY avg

print("monthly avg (12 values):", np.round(monthly_avg_across_cities, 1))
print("city avg (3 values)    :", np.round(city_avg_across_year, 1))
print("hottest month (index)  :", np.argmax(monthly_avg_across_cities))
print("coldest city (index)   :", np.argmin(city_avg_across_year))

assert monthly_avg_across_cities.shape == (12,)
assert city_avg_across_year.shape == (3,)
"""))

A(md("""
### 15.3 Student marks report — per-student & per-subject aggregates + grades
"""))

A(code("""
students = ["Ali", "Sara", "Bilal", "Ayesha"]
subjects = ["Math", "Physics", "Chem"]
marks = rng.integers(30, 100, size=(4, 3))   # 4 students x 3 subjects

per_student_avg = marks.mean(axis=1)   # axis=1 collapses subjects -> per STUDENT avg
per_subject_avg = marks.mean(axis=0)   # axis=0 collapses students -> per SUBJECT avg

conditions = [per_student_avg >= 85, per_student_avg >= 70, per_student_avg >= 50]
choices = ["A", "B", "C"]
grades = np.select(conditions, choices, default="F")

for name, avg, grade in zip(students, per_student_avg, grades):
    print(f"{name:8s} avg={avg:5.1f}  grade={grade}")
print("subject-wise average:", dict(zip(subjects, per_subject_avg.round(1))))

assert len(grades) == len(students)
"""))

A(md("""
### 15.4 Missing-value (NaN) handling in a dataset with NaN-safe aggregations
"""))

A(code("""
raw_data = rng.uniform(50, 100, size=(5, 4))
missing_mask = rng.random(size=(5, 4)) < 0.2         # ~20% readings "missing" hain
data_with_nan = np.where(missing_mask, np.nan, raw_data)

print("data with NaN:\\n", np.round(data_with_nan, 1))
print("WITHOUT nan-safe (galat, propagate):", np.mean(data_with_nan, axis=0))
print("WITH nan-safe (sahi)              :", np.round(np.nanmean(data_with_nan, axis=0), 2))

assert not np.isnan(np.nanmean(data_with_nan, axis=0)).any()
"""))

A(md("""
### 15.5 Simple linear regression prediction with `@` + MSE
"""))

A(code("""
n_samples = 20
X_feat = rng.uniform(0, 10, size=(n_samples, 2))
true_w = np.array([2.0, -1.5])
true_b = 5.0
noise = rng.normal(0, 0.5, size=n_samples)
y_true = X_feat @ true_w + true_b + noise   # asal (noisy) targets

# design matrix (bias column + features), 'known' weights se prediction (fitting nahi, sirf demo)
X_design = np.hstack([np.ones((n_samples, 1)), X_feat])
w_full = np.concatenate([[true_b], true_w])
y_pred = X_design @ w_full

mse = np.mean((y_true - y_pred) ** 2)
print(f"MSE (should be close to noise variance ~0.25): {mse:.4f}")
assert mse < 1.0   # chhota noise hai isliye MSE bhi chhota hona chahiye
"""))

# ============================================================
# 17. LEETCODE PROBLEMS
# ============================================================
A(md("""
## 16. LeetCode Problems

Har problem ke 2 solutions denge: **(a) pure Python** (interview-acceptable) aur
**(b) NumPy/vectorized**. Interview me generally pure Python expect hota hai; NumPy
production/data-work ke liye use hota hai.
"""))

A(md("""
### LC 1672. Richest Customer Wealth — Easy
Link: https://leetcode.com/problems/richest-customer-wealth/

**Bayan:** `accounts[i][j]` = customer `i` ka bank `j` me paisa. Har customer ki **wealth**
= uske sab accounts ka sum. Sabse ameer customer ki wealth return karo.

**Approach:** Har row ka sum nikalo, phir un sums ka max le lo.

**Complexity:** Time `O(m*n)`, Space `O(1)` (extra, sums ke ilawa).
"""))

A(code("""
# (a) Pure Python
def richest_customer_wealth_py(accounts):
    return max(sum(row) for row in accounts)

# Tests
assert richest_customer_wealth_py([[1, 2, 3], [3, 2, 1]]) == 6
assert richest_customer_wealth_py([[1, 5], [7, 3], [3, 5]]) == 10
assert richest_customer_wealth_py([[2, 8, 7], [7, 1, 3], [1, 9, 5]]) == 17
print("pure python: sab tests pass")
"""))

A(code("""
# (b) NumPy / vectorized
def richest_customer_wealth_np(accounts):
    arr = np.array(accounts)
    return int(arr.sum(axis=1).max())   # axis=1 collapses banks -> per-customer wealth, phir max

assert richest_customer_wealth_np([[1, 2, 3], [3, 2, 1]]) == 6
assert richest_customer_wealth_np([[1, 5], [7, 3], [3, 5]]) == 10
assert richest_customer_wealth_np([[2, 8, 7], [7, 1, 3], [1, 9, 5]]) == 17
print("numpy: sab tests pass")
"""))

A(md("""
### LC 1470. Shuffle the Array — Easy
Link: https://leetcode.com/problems/shuffle-the-array/

**Bayan:** `nums` length `2n` hai: pehle `n` elements `x1..xn`, baaqi `n` elements `y1..yn`.
Return karo `[x1,y1,x2,y2,...,xn,yn]`.

**Approach:** Do halves nikalo aur interleave (alternate) kar do.

**Complexity:** Time `O(n)`, Space `O(n)` (output ke liye).
"""))

A(code("""
# (a) Pure Python
def shuffle_py(nums, n):
    result = []
    for i in range(n):
        result.append(nums[i])
        result.append(nums[n + i])
    return result

assert shuffle_py([2, 5, 1, 3, 4, 7], 3) == [2, 3, 5, 4, 1, 7]
assert shuffle_py([1, 2, 3, 4, 4, 3, 2, 1], 4) == [1, 4, 2, 3, 3, 2, 4, 1]
assert shuffle_py([1, 1, 2, 2], 2) == [1, 2, 1, 2]
print("pure python: sab tests pass")
"""))

A(code("""
# (b) NumPy / vectorized -> column_stack + ravel se interleave (bina explicit loop ke)
def shuffle_np(nums, n):
    arr = np.array(nums)
    x, y = arr[:n], arr[n:]
    return np.column_stack((x, y)).ravel().tolist()   # (n,2) -> flatten interleaved

assert shuffle_np([2, 5, 1, 3, 4, 7], 3) == [2, 3, 5, 4, 1, 7]
assert shuffle_np([1, 2, 3, 4, 4, 3, 2, 1], 4) == [1, 4, 2, 3, 3, 2, 4, 1]
assert shuffle_np([1, 1, 2, 2], 2) == [1, 2, 1, 2]
print("numpy: sab tests pass")
"""))

A(md("""
### LC 561. Array Partition — Easy
Link: https://leetcode.com/problems/array-partition/

**Bayan:** `2n` integers ko `n` pairs me todo taake har pair ka **minimum** ka sum
**maximize** ho.

**Approach:** Sort karo, phir har alternate element (index 0, 2, 4, ...) ka sum lo —
sorted array me consecutive pairs banane se min-waste minimize hota hai.

**Complexity:** Time `O(n log n)` (sorting), Space `O(n)` (sorted copy ke liye, in-place sort O(1) extra).
"""))

A(code("""
# (a) Pure Python
def array_pair_sum_py(nums):
    nums_sorted = sorted(nums)
    return sum(nums_sorted[::2])   # 0th, 2nd, 4th... index ka sum

assert array_pair_sum_py([1, 4, 3, 2]) == 4
assert array_pair_sum_py([6, 2, 6, 5, 1, 2]) == 9
print("pure python: sab tests pass")
"""))

A(code("""
# (b) NumPy / vectorized
def array_pair_sum_np(nums):
    arr = np.sort(np.array(nums))
    return int(arr[::2].sum())   # slicing bhi vectorized hai

assert array_pair_sum_np([1, 4, 3, 2]) == 4
assert array_pair_sum_np([6, 2, 6, 5, 1, 2]) == 9
print("numpy: sab tests pass")
"""))

A(md("""
### LC 1004. Max Consecutive Ones III — Medium
Link: https://leetcode.com/problems/max-consecutive-ones-iii/

**Bayan:** Binary array `nums` aur integer `k` diya hai — at most `k` zeros ko `1` me flip
kar ke maximum consecutive `1`s ki length nikalo.

**Approach (sliding window):** Do pointers `left`/`right`. `right` aage barhao, zeros count
karo; jab zeros count `k` se zyada ho jaye, `left` aage barhao jab tak zeros count wapis `<=k` na ho.
Har step par window size (`right-left+1`) ka max rakho.

**Complexity:** Time `O(n)`, Space `O(1)`.

**Honest note:** Ye problem **inherently sequential** hai (`left` pointer ka move `right` par
depend karta hai) — is liye pure Python sliding window hi **optimal O(n)** solution hai. Neeche
NumPy version sirf **demonstration** ke liye hai (prefix-sum zero-count ke liye numpy use karta
hai), window logic phir bhi ek Python loop me sequential chalta hai — ye "true vectorization"
nahi hai.
"""))

A(code("""
# (a) Pure Python -- optimal O(n) sliding window
def longest_ones_py(nums, k):
    left = 0
    zeros = 0
    best = 0
    for right, val in enumerate(nums):
        if val == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best

assert longest_ones_py([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
assert longest_ones_py([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3) == 10
print("pure python: sab tests pass")
"""))

A(code("""
# (b) NumPy-assisted (demonstration only -- sliding window part is still sequential)
def longest_ones_np(nums, k):
    arr = np.array(nums)
    n = len(arr)
    prefix_zeros = np.concatenate(([0], np.cumsum(arr == 0)))   # prefix_zeros[i] = zeros in nums[0:i]
    left = 0
    best = 0
    for right in range(n):   # ye loop sequential hi rehta hai (left depends on history)
        while prefix_zeros[right + 1] - prefix_zeros[left] > k:
            left += 1
        best = max(best, right - left + 1)
    return int(best)

assert longest_ones_np([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
assert longest_ones_np([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3) == 10
print("numpy (demo): sab tests pass -- lekin real-world me pure python version hi use karo")
"""))

A(md("""
### LC 53. Maximum Subarray — Medium
Link: https://leetcode.com/problems/maximum-subarray/

**Bayan:** Integer array me sabse bara sum wala **contiguous subarray** dhoondo.

**Approach (Kadane, pure Python):** Har index par decide karo — "current element se naya
subarray shuru karo" ya "purani running sum me isse add karo" (jo bara ho). `O(n)` optimal.

**Approach (NumPy, cumsum trick):** `C[0]=0, C[i]=sum(nums[0:i])`. Kisi bhi subarray
`(l, r]` ka sum = `C[r] - C[l]`. Maximum subarray sum = `max_r (C[r] - min_{l<r} C[l])`.
Ye `cumsum` + running-minimum-prefix se vectorized ho jata hai.

**Complexity:** Dono `O(n)` time, `O(n)` space (NumPy version extra cumsum array banata hai).
"""))

A(code("""
# (a) Pure Python -- Kadane's algorithm
def max_subarray_py(nums):
    best = nums[0]
    cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)      # naya subarray shuru karo ya extend karo
        best = max(best, cur)
    return best

assert max_subarray_py([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
assert max_subarray_py([1]) == 1
assert max_subarray_py([5, 4, -1, 7, 8]) == 23
print("pure python (Kadane): sab tests pass")
"""))

A(code("""
# (b) NumPy -- cumsum + running-minimum-prefix trick
def max_subarray_np(nums):
    arr = np.array(nums, dtype=float)
    cumsum = np.concatenate(([0.0], np.cumsum(arr)))        # C[0..n]
    running_min = np.minimum.accumulate(cumsum[:-1])         # min(C[0..i]) for i=0..n-1
    diffs = cumsum[1:] - running_min                          # C[r] - min_{l<r} C[l], r=1..n
    return float(diffs.max())

assert max_subarray_np([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
assert max_subarray_np([1]) == 1
assert max_subarray_np([5, 4, -1, 7, 8]) == 23
print("numpy (cumsum trick): sab tests pass")
"""))

# ============================================================
# 18. INTERVIEW Q&A
# ============================================================
A(md("""
## 17. Interview Questions & Answers

1. **Vectorization loops se tez kyun hoti hai?**
   Contiguous memory, compiled C loop, SIMD instructions, aur per-element Python object
   overhead nahi hota.

2. **Broadcasting ke rules kya hain?**
   Trailing dims se align karo; size-1 dims stretch hoti hain; missing (left-side) dims 1
   samjhi jati hain; agar match na ho (aur 1 na ho) to error.

3. **`axis=0` vs `axis=1` ka matlab?**
   Jis axis number do wo axis result me **collapse** ho jati hai (2D: axis=0 -> per-column
   result, axis=1 -> per-row result).

4. **`keepdims=True` kyun use karte hain?**
   Taake collapsed dimension size-1 reh jaye aur result ko wapis original array ke sath
   broadcast kiya ja sake (jaise normalize karte waqt).

5. **`np.max` vs `np.maximum` ka farq?**
   `np.max` ek array ko **reduce** karta hai (scalar/kam-dim). `np.maximum` do arrays ko
   **element-wise** compare karta hai (shape same rehti hai).

6. **`dot`/`@` vs `*` ka farq?**
   `@`/`dot` matrix multiplication (sum-of-products) karte hain; `*` sirf element-wise
   multiply karta hai.

7. **Integer array me `arr += 0.5` karne se kya hota hai?**
   `UFuncTypeError` — in-place op array ka dtype badal nahi sakta (same_kind casting rule).

8. **`if arr:` multi-element array par kyun fail hota hai?**
   `ValueError: truth value ... ambiguous` — Python ko pata nahi konsa element check kare;
   `.any()`/`.all()` use karo.

9. **`ddof` kya hai `std`/`var` me?**
   Delta Degrees of Freedom. `ddof=0` = population (default), `ddof=1` = sample (Bessel's
   correction, denominator `n-1`).

10. **`arr.ptp()` kyun error deta hai NumPy 2 me?**
    Method form NumPy 2.0 me hata diya gaya — `np.ptp(arr)` function form use karo.

11. **NaN values sum/mean me kya karte hain?**
    Propagate ho jate hain — poora result `nan` ban jata hai. Bachne ke liye
    `nansum`/`nanmean`/etc use karo.

12. **`np.broadcast_to` ka result read-only kyun hota hai?**
    Kyunke data actually copy nahi hota — same memory ko multiple baar "virtually" dikhaya
    jata hai, isliye ek jagah likhna kai jagah asar dalega — NumPy safety ke liye writeable
    band kar deta hai.

13. **`0.1 + 0.2 == 0.3` False kyun hai?**
    Floating point binary representation me 0.1, 0.2, 0.3 exactly store nahi hote —
    rounding error hota hai. `np.isclose`/`np.allclose` use karo.

14. **`np.isclose` vs `np.allclose`?**
    `isclose` element-wise boolean array deta hai; `allclose` poore array ke liye ek hi
    `True/False` (sab elements close hain ya nahi).

15. **`a > 1 & b < 3` me brackets kyun zaroori hain?**
    Python me `&` ki precedence comparison operators se zyada hai, isliye ye expression
    galat parse hoti hai (chained comparison + ambiguous `and`). Hamesha `(a>1) & (b<3)`
    likho.

16. **`np.log1p(x)` kyun use karte hain `np.log(1+x)` ki jagah?**
    Bohat choti `x` values ke liye `1+x` khud precision kho deta hai (floating point);
    `log1p` internally is precision loss se bachta hai.

17. **`np.reciprocal` integer array par galat result kyun deta hai?**
    Integer dtype ke sath result bhi integer truncate hota hai (`1/2 -> 0`), isliye float
    array par use karo.

18. **`np.select` kab `np.where` se behtar hai?**
    Jab 2 se zyada (multiple) conditions ek sath handle karni hon — `where` sirf 2 cases
    (if/else) ke liye clean hai, `select` N cases ke liye.
"""))

# ============================================================
# 19. PRACTICE EXERCISES
# ============================================================
A(md("""
## 18. Practice Exercises (khud karo)

1. Ek `(5,)` random array bana kar uska **z-score normalize** karo bina explicit loop ke.
   *Hint: `(arr - arr.mean()) / arr.std()`*

2. Do vectors ka **dot product** aur **cosine similarity** nikalo.
   *Hint: `cos_sim = dot(a,b) / (norm(a)*norm(b))`, `np.linalg.norm` use karo.*

3. Ek `(4,5)` random integer matrix banao aur row-wise aur column-wise **max** nikalo
   `keepdims=True` ke sath. Check karo shape kya reh jati hai.

4. `np.where` use kar ke ek array ke saare **negative values ko 0** se replace karo.

5. Broadcasting se ek `(3,1)` aur `(1,4)` array ka addition-table banao, aur bataye ke result
   shape kya hogi aur kyun.

6. Ek dataset (2D array) me kuch values ko `np.nan` bana kar `nanmean`/`nanstd` se stats
   nikalo — bina nan-safe function ke result se compare karo.

7. `np.select` se student marks ko **5 grades** (A/B/C/D/F) me convert karo (4 conditions).

8. `argsort` use kar ke ek matrix ke har **row ka top-3** elements nikalo (bina explicit
   Python loop ke, `take_along_axis` use karo).

9. `np.clip` se ek array ke values ko `[0, 100]` range me force karo, phir verify karo
   `min()`/`max()` se.

10. Loop use kiye baghair, 2D points ke beech **pairwise distance matrix** banao
    (broadcasting + `sqrt`).
"""))

# ============================================================
# 20. SUMMARY / CHEAT-SHEET
# ============================================================
A(md("""
## 19. Summary / Cheat-sheet

### Broadcasting Rules
| Step | Rule |
|------|------|
| 1 | Shapes ko **trailing (right)** dimension se align karo |
| 2 | Size **1** dimension doosri shape ke size tak **stretch** hoti hai |
| 3 | Missing (left-side) dimensions **1** samjhi jati hain |
| 4 | Match na ho (aur 1 na ho) to `ValueError` |

### Axis Cheat-sheet (2D array, shape `(rows, cols)`)
| axis | Kya collapse hota hai | Result shape |
|------|------------------------|--------------|
| `axis=0` | rows (top-to-bottom) | `(cols,)` — per column |
| `axis=1` | cols (left-to-right) | `(rows,)` — per row |
| `axis=None` | sab kuch | scalar |
| `keepdims=True` | collapse hone wali axis size-1 reh jati hai | broadcasting-friendly |

### Aggregation Functions Quick List
`sum, prod, min, max, mean, median, std, var (ddof), np.ptp, percentile, quantile, cumsum,
cumprod, argmin, argmax (+ np.unravel_index), count_nonzero` — aur inke **nan-safe** versions
(`nansum, nanmean, nanstd, nanmin, nanmax, nanargmax, nanmedian`).

### Ufuncs Quick List
`sqrt, exp, log/log2/log10/log1p, sin/cos/tan (+deg2rad), abs, sign, round/floor/ceil/trunc/rint,
clip, power, maximum/minimum, mod/fmod, reciprocal` — aur ufunc attributes `.reduce`,
`.accumulate`, `.outer`, `.nin`/`.nout`.

### Gotchas jo yaad rakhne hain
- `arr.ptp()` removed → `np.ptp(arr)`
- integer `+=` float → `UFuncTypeError`
- `if arr:` multi-element → ambiguous `ValueError`
- `&`/`|` precedence > comparisons → brackets lazmi
- `np.round` = banker's rounding
- NaN propagate hota hai bina `nan*` functions ke
- `broadcast_to` result read-only
- float `==` risky → `isclose`/`allclose` use karo

Mubarak ho — is notebook ke baad aap NumPy ke operations, broadcasting aur aggregations me
confident hain. Agla step: linear algebra / advanced indexing / performance tricks!
"""))

save(r"Numpy/Basics/03_Operations_Broadcasting_and_Aggregations.ipynb", CELLS)
print(f"Total cells: {len(CELLS)}")
