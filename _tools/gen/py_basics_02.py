"""Generator: Python/Basics/02_Variables_DataTypes_aur_Operators.ipynb"""

import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

cells = []
M = lambda s: cells.append(md(s))   # noqa: E731  markdown cell shortcut
C = lambda s: cells.append(code(s))  # noqa: E731  code cell shortcut

M(r"""
# 02 — Variables, Data Types aur Operators

**Level:** Beginner → Intermediate
**Series:** Python Basics (Notebook 2 / 7)

Notebook 1 me humne Python ka setup, `print()` aur environment samjha. Ab asli kaam shuru:
**data ko naam dena (variables)**, **data ki qismein (types)** aur **data par kaam karna (operators)**.

Ye notebook interview ka sab se zyada "poocha jane wala" hissa cover karta hai — `is` vs `==`,
float precision, mutable vs immutable, operator precedence. In sawalon me log rozana phaste hain.

## Is notebook me kya seekhenge

- **Variables**: naming rules, multiple / chained assignment, swap, unpacking, `del`
- **Core types**: `int`, `float`, `complex`, `bool`, `str`, `NoneType`
- **Type casting**: implicit (automatic) vs explicit, aur kahan data kho jata hai
- **Float precision**: `0.1 + 0.2 != 0.3` ka asli sabab, `Decimal`, `Fraction`, `math.isclose`
- **Rounding**: `round()` ka banker's rounding gotcha
- **Operators**: arithmetic, comparison, logical, bitwise, assignment, identity, membership
- **Walrus operator** `:=` — kahan asli faida deta hai
- **Precedence & associativity** — poori table, aur `-2**2` jaise trap
- **`is` vs `==`**, small-int caching, string interning
- **Mutable vs immutable** — `id()` ke saath proof
- **String formatting**: f-strings, `str.format()`, purana `%` style
- **`input()`** ka theory (notebook me call NAHI karenge — kyun, wo bhi batayenge)

## Prerequisites

- Notebook 01 (`print()`, comments, indentation, `type()`, `id()`)
- Bas itna hi — baqi sab yahan se banayenge.

> **Padhne ka tareeqa:** har code cell khud chala kar output dekho, phir output ko cover kar ke
> guess karo ke kya aayega. Jahan guess ghalat ho — wahi tumhara asli seekhne ka point hai.
""")

M(r"""
---
## 1. Variable kya hai?

**Kya hai:** Variable ek **naam** (name / label) hai jo memory me pare kisi **object** ki taraf
ishara karta hai. C/C++ ki tarah Python me variable koi "dabba" (box) nahi hota jis me value
rakhi jati hai — Python me variable ek **naam ka tag** hai jo object par chipka diya jata hai.

**Kyun ahem:** Ye ek line poore Python ko samajhne ki chaabi hai. Isi wajah se:
- ek hi object ke do naam ho sakte hain (aliasing),
- list ko function me bhejo to andar ki tabdeeli bahar bhi dikhti hai,
- `a = b` copy nahi banata.

**Syntax:**
```python
name = value        # "=" assignment operator hai, equality nahi
```

**Naming rules (lazmi):**
- Letters, digits aur underscore `_` — magar **digit se shuru nahi** ho sakta.
- Case-sensitive: `age`, `Age`, `AGE` teen alag naam hain.
- Python keyword (`if`, `class`, `for`...) naam nahi ban sakta.

**Convention (PEP 8):** `snake_case` variables/functions ke liye, `UPPER_CASE` constants,
`PascalCase` classes. Aur builtin naam (`list`, `str`, `sum`, `id`, `type`) ko **shadow na karo**.
""")

C(r"""
# --- Variable banane ka sab se basic tareeqa ---
student_name = "Ayesha"      # str object bana, uska tag 'student_name'
student_age = 21             # int object
student_cgpa = 3.72          # float object
is_enrolled = True           # bool object

# f-string se saaf output (tafseel isi notebook ke aakhir me)
print(f"Naam   : {student_name}")
print(f"Umar   : {student_age}")
print(f"CGPA   : {student_cgpa}")
print(f"Enroll : {is_enrolled}")

# type() batata hai object ki qism, id() batata hai uska memory identity
print("\ntype aur id:")
print(type(student_name), id(student_name))
print(type(student_age),  id(student_age))
""")

C(r"""
# --- Naam = tag, dabba nahi. Ye demo dil se samajh lo ---
a = [10, 20, 30]     # ek list object bana
b = a                # NAYA list nahi bana! sirf usi object par doosra tag 'b' laga

print("a:", a, "| id(a):", id(a))
print("b:", b, "| id(b):", id(b))
print("a is b ->", a is b, "(dono ka object ek hi hai)")

b.append(40)         # object ko mutate kiya (b ke zariye)
print("\nb.append(40) ke baad:")
print("a:", a)       # a bhi badal gaya — kyunki object wahi ek hai
print("b:", b)

# Ab REBINDING (naya object) — mutation nahi
b = [1, 2]           # 'b' tag hata kar naye object par laga diya
print("\nb = [1, 2] ke baad:")
print("a:", a, "  <- a purane object par hi hai")
print("b:", b)
""")

M(r"""
### Output ka matlab

- `a is b -> True` ka matlab: dono naam **bilkul wahi ek object** point kar rahe hain.
- `b.append(40)` ne object ko **andar se badla** (mutation) → `a` me bhi 40 nazar aaya.
- `b = [1, 2]` ne object badla nahi, **tag shift** kiya (rebinding) → `a` par koi asar nahi.

**Common mistake:** `b = a` likh kar samajhna ke backup ban gaya. Nahi bana. Copy ke liye
`a.copy()`, `list(a)`, `a[:]` ya `copy.deepcopy(a)` chahiye (tafseel Notebook 05 me).

**Interview tip:** "Python pass-by-value hai ya pass-by-reference?" — dono nahi.
Sahi jawab: **pass-by-object-reference** (a.k.a. call-by-sharing). Object ka reference pass hota
hai; mutable object mutate ho sakta hai, magar parameter ko rebind karna caller ko nazar nahi aata.
""")

M(r"""
---
## 2. Assignment ki saari shaklein

| Shakal | Misaal | Kab |
|---|---|---|
| Simple | `x = 5` | rozana |
| Multiple (chained) | `a = b = c = 0` | kai naam, ek hi value |
| Parallel / tuple unpacking | `x, y = 1, 2` | ek line me kai values |
| Swap | `a, b = b, a` | temp variable ki zaroorat nahi |
| Starred unpack | `first, *rest = [1,2,3]` | pehla + baqi |
| Augmented | `x += 1` | update-in-place style |
| Walrus | `if (n := len(s)) > 3:` | assign + use ek sath |

**Gotcha (bohat ahem):** `a = b = []` teen alag list nahi banata — **ek hi** list par do tag.
Mutable ke sath ye bug ban jata hai.
""")

C(r"""
# --- Multiple (chained) assignment ---
x = y = z = 0                 # teeno naam ek hi int object (0) par
print("x, y, z =", x, y, z)

# Immutable (int) ke sath chained assignment bilkul safe hai:
x += 1                        # int immutable hai -> naya object bana, sirf x shift hua
print("x += 1 ke baad ->", x, y, z)

# MAGAR mutable ke sath khatarnaak:
p = q = []                    # ek hi list par do tag!
p.append("boom")
print("\np:", p, "| q:", q, "  <- q bhi badla, kyunki object ek hi hai")

# Sahi tareeqa: alag alag objects banao
p2, q2 = [], []               # do alag list objects
p2.append("safe")
print("p2:", p2, "| q2:", q2)
""")

C(r"""
# --- Parallel assignment / tuple unpacking ---
name, age, city = "Bilal", 24, "Lahore"   # right side ek tuple hai, left side unpack
print(name, age, city)

# Swap — Python ka sab se khoobsurat idiom (temp ki zaroorat nahi)
a, b = 10, 20
print("\npehle : a =", a, ", b =", b)
a, b = b, a                                # right side pehle poora evaluate hota hai
print("baad  : a =", a, ", b =", b)

# Teen ka rotate bhi ek line me
i, j, k = 1, 2, 3
i, j, k = k, i, j
print("rotate:", i, j, k)

# Starred unpacking — pehla/aakhri + baqi
first, *rest = [1, 2, 3, 4, 5]
print("\nfirst:", first, "| rest:", rest)     # rest hamesha list hoti hai

head, *middle, tail = [1, 2, 3, 4, 5]
print("head:", head, "| middle:", middle, "| tail:", tail)

# Nested unpacking
(p, q), r = (1, 2), 3
print("nested ->", p, q, r)

# Jo value nahi chahiye, convention se '_' me daal do
_, important, _ = ("kachra", "asli-value", "kachra")
print("important:", important)
""")

C(r"""
# --- Unpacking ke errors (jaan boojh kar, try/except me) ---
try:
    a, b = 1, 2, 3                 # 3 values, 2 targets
except ValueError as e:
    print("ValueError:", e)        # too many values to unpack

try:
    a, b, c = [1, 2]               # 2 values, 3 targets
except ValueError as e:
    print("ValueError:", e)        # not enough values to unpack

# Starred target zaroor list deta hai, chahe khali ho
x, *y = [9]
print("x:", x, "| y:", y, "(khali list, None nahi)")
""")

C(r"""
# --- del: naam hatana (object nahi, tag hatata hai) ---
temp_value = 99
print("temp_value:", temp_value)

del temp_value                      # sirf naam khatam hua

try:
    print(temp_value)
except NameError as e:
    print("NameError:", e)          # naam ab maujood nahi

# Object khud tab free hota hai jab uska koi reference na bache (reference counting + GC)
shared = [1, 2, 3]
alias = shared
del shared                          # ek tag gaya, magar object zinda hai (alias hai na)
print("alias abhi bhi zinda:", alias)
""")

M(r"""
---
## 3. Python ke core data types

Python **dynamically typed** hai: variable ki type declare nahi karte, type **object** ke sath
hoti hai aur runtime par pata chalti hai. Magar Python **strongly typed** bhi hai — yani
`"5" + 5` chup chaap kaam nahi karega, error dega (JavaScript ki tarah guess nahi karta).

| Type | Misaal | Mutable? | Notes |
|---|---|---|---|
| `int` | `42`, `-7`, `10**50` | ❌ | **arbitrary precision** — koi overflow nahi |
| `float` | `3.14`, `2e-3`, `inf` | ❌ | IEEE-754 double (64-bit), approximate |
| `complex` | `3+4j` | ❌ | `.real`, `.imag`, `abs()` = magnitude |
| `bool` | `True`, `False` | ❌ | `int` ka **subclass** (`True == 1`) |
| `str` | `"salam"` | ❌ | Unicode text (poori tafseel NB 03) |
| `NoneType` | `None` | ❌ | "koi value nahi" — singleton |
| `list` | `[1, 2]` | ✅ | NB 05 |
| `tuple` | `(1, 2)` | ❌ | NB 05 |
| `set` | `{1, 2}` | ✅ | NB 06 |
| `dict` | `{"a": 1}` | ✅ | NB 06 |

Is notebook me pehle 6 (scalar-ish) types par focus hai.
""")

C(r"""
# --- Type tour: har type ka namoona ---
samples = [
    42,                 # int
    3.14159,            # float
    3 + 4j,             # complex
    True,               # bool
    "Assalam-o-Alaikum",  # str
    None,               # NoneType
    [1, 2, 3],          # list
    (1, 2, 3),          # tuple
    {1, 2, 3},          # set
    {"a": 1},           # dict
    b"bytes",           # bytes
    range(3),           # range
]

print(f"{'value':<22} {'type':<12} {'truthy?'}")
print("-" * 46)
for item in samples:
    # type(item).__name__ se saaf naam milta hai (class 'int' wali shakal ke bajaye)
    print(f"{repr(item):<22} {type(item).__name__:<12} {bool(item)}")
""")

C(r"""
# --- Dynamic typing: ek hi naam, badalti type ---
value = 10
print(f"{value!r:<12} -> {type(value).__name__}")

value = 10.5            # naam ko naye object par bind kiya
print(f"{value!r:<12} -> {type(value).__name__}")

value = "das"
print(f"{value!r:<12} -> {type(value).__name__}")

value = [10]
print(f"{value!r:<12} -> {type(value).__name__}")

# Magar STRONGLY typed: types khud-ba-khud mix nahi hote
try:
    result = "5" + 5
except TypeError as e:
    print("\nTypeError:", e)
    print("Sabaq: Python guess nahi karta. Khud cast karo -> int('5') + 5 =", int("5") + 5)
""")

M(r"""
---
## 4. `int` — poora tafseel se

**Kya hai:** Whole numbers (positive, negative, zero). Python 3 me `int` ki koi **limit nahi** —
arbitrary precision. Jitni RAM hai, utna bara number.

**Kyun ahem:** C/C++/Java me `int` overflow ho jata hai (32/64-bit). Python me `2**1000` bhi
theek chalta hai — interview me ye "Python ka faida" ke tor par bataya jata hai.

**Likhne ke tareeqe:**
- Decimal: `42`
- Underscore separator (readability): `1_000_000` (Python ise ignore karta hai)
- Binary: `0b1010`, Octal: `0o17`, Hex: `0xFF`
- Kisi bhi base se: `int("1010", 2)`
""")

C(r"""
# --- int: arbitrary precision ka jaadu ---
big = 2 ** 100
print("2**100 =", big)
print("digits:", len(str(big)))          # 31 digits — koi overflow nahi

# Factorial 50 — Java/C me long bhi fail ho jata
import math
print("50! =", math.factorial(50))

# Underscore separators: sirf padhne ke liye, value par asar nahi
salary = 1_250_000
print("\nsalary =", salary, "| 1_250_000 == 1250000 ->", salary == 1250000)

# Alag alag bases me likhna
print("\n0b1010 =", 0b1010, "(binary)")
print("0o17   =", 0o17, "(octal)")
print("0xFF   =", 0xFF, "(hex)")
""")

C(r"""
# --- Base conversion: int -> string aur string -> int ---
n = 255

# int se string (prefix ke sath)
print("bin(255) =", bin(n))          # '0b11111111'
print("oct(255) =", oct(n))          # '0o377'
print("hex(255) =", hex(n))          # '0xff'

# f-string se prefix ke baghair (formatting NB 03 me tafseel se)
print("\nbina prefix -> bin:", f"{n:b}", "| oct:", f"{n:o}", "| hex:", f"{n:x}", "| HEX:", f"{n:X}")

# string se int, base bata kar
print("\nint('11111111', 2) =", int("11111111", 2))
print("int('377', 8)       =", int("377", 8))
print("int('ff', 16)       =", int("ff", 16))
print("int('0xff', 16)     =", int("0xff", 16), "(prefix chalta hai)")
print("int('z', 36)        =", int("z", 36), "(base 36 tak allowed)")

# Ghalat base/string -> ValueError
try:
    int("12", 2)                      # base-2 me '2' allowed nahi
except ValueError as e:
    print("\nValueError:", e)
""")

M(r"""
---
## 5. `float` — aur uski "approximate" fitrat

**Kya hai:** Decimal numbers, IEEE-754 **double precision** (64-bit) ke tor par store hote hain:
1 sign bit + 11 exponent bits + 52 mantissa bits.

**Kyun ahem:** Computer binary me kaam karta hai. `0.1` binary me **exactly** likha hi nahi ja
sakta (jaise decimal me `1/3` = 0.333... khatam nahi hota). Isi liye chhoti si error rehti hai —
aur wahi error `0.1 + 0.2 != 0.3` ban jati hai.

**Likhne ke tareeqe:** `3.14`, `.5`, `5.`, `2e3` (=2000.0), `1.5e-3` (=0.0015), `float('inf')`,
`float('nan')`.
""")

C(r"""
# --- float ke likhne ke tareeqe aur limits ---
import sys

print("3.14   ->", 3.14)
print(".5     ->", .5)              # leading zero optional
print("5.     ->", 5.)              # trailing zero optional
print("2e3    ->", 2e3, type(2e3).__name__)      # scientific notation, float hi hai
print("1.5e-3 ->", 1.5e-3)
print("1_000.5 ->", 1_000.5)        # underscore yahan bhi chalta hai

print("\n--- float ki limits (sys.float_info) ---")
print("max        :", sys.float_info.max)
print("min (>0)   :", sys.float_info.min)
print("epsilon    :", sys.float_info.epsilon, "(1.0 se agla representable number ka farq)")
print("mant_digits:", sys.float_info.mant_dig, "bits mantissa")
print("dig        :", sys.float_info.dig, "reliable decimal digits")
""")

C(r"""
# --- inf aur nan ---
import math

pos_inf = float("inf")
neg_inf = float("-inf")
not_a_num = float("nan")

print("inf  :", pos_inf, "| math.inf:", math.inf, "| barabar?", pos_inf == math.inf)
print("-inf :", neg_inf)
print("nan  :", not_a_num, "| math.nan:", math.nan)

print("\n--- inf ke sath arithmetic ---")
print("inf + 1     =", pos_inf + 1)
print("inf * 2     =", pos_inf * 2)
print("1 / inf     =", 1 / pos_inf)
print("inf > 10**100 ->", pos_inf > 10 ** 100)

print("\n--- nan ka sab se bara gotcha ---")
print("nan == nan  ->", not_a_num == not_a_num, "  <-- FALSE! nan kisi ke barabar nahi, khud ke bhi nahi")
print("nan != nan  ->", not_a_num != not_a_num)
print("nan is nan  ->", not_a_num is not_a_num, "  <-- identity check True hai (same object)")
print("Sahi test   -> math.isnan(x):", math.isnan(not_a_num))

# Overflow float me exception nahi, inf de sakta hai
print("\nfloat overflow:")
try:
    print(1e308 * 10)               # inf
except OverflowError as e:
    print("OverflowError:", e)
# Magar int -> float conversion me overflow error aata hai
try:
    float(10 ** 400)
except OverflowError as e:
    print("OverflowError (int too large):", e)
""")

M(r"""
---
## 6. Float precision — interview ka classic

**Sawal:** `0.1 + 0.2 == 0.3` kyun `False` hai?

**Jawab:** `0.1`, `0.2`, `0.3` teeno binary float me **approximate** store hote hain. Jama karne
par error jama ho jati hai aur natija `0.30000000000000004` banta hai.

**Hal (3 tareeqe):**
1. `math.isclose(a, b)` — comparison ke liye (tolerance ke sath)
2. `decimal.Decimal` — **paisa / accounting** ke liye (exact decimal arithmetic)
3. `fractions.Fraction` — exact rational numbers (1/3 wagera) ke liye
""")

C(r"""
# --- Asli masla apni aankhon se dekho ---
print("0.1 + 0.2       =", 0.1 + 0.2)
print("0.1 + 0.2 == 0.3 ->", 0.1 + 0.2 == 0.3, "  <-- FALSE")

# Andar ki asli value 20 decimal digits tak
print("\n0.1 asli value :", format(0.1, ".20f"))
print("0.2 asli value :", format(0.2, ".20f"))
print("0.3 asli value :", format(0.3, ".20f"))
print("0.1+0.2 asli   :", format(0.1 + 0.2, ".20f"))

# Exact fraction dekho (float ki asli rational value)
from fractions import Fraction
print("\n0.1 ki EXACT value =", Fraction(0.1))
print("Yani 0.1 asal me thoda bara hai 1/10 se.")

# Aur ek mashhoor misaal
total = 0.0
for _ in range(10):
    total += 0.1                     # 10 baar 0.1 jama karo
print("\n0.1 das baar jama =", total, "| == 1.0 ->", total == 1.0)
""")

C(r"""
# --- Hal 1: math.isclose (comparison ka sahi tareeqa) ---
import math

a, b = 0.1 + 0.2, 0.3
print("a == b            ->", a == b)
print("math.isclose(a,b) ->", math.isclose(a, b), "  <-- SAHI tareeqa")

# Apni tolerance bhi de sakte ho
print("isclose(1.0, 1.05, rel_tol=0.1) ->", math.isclose(1.0, 1.05, rel_tol=0.1))
print("isclose(1.0, 1.05, rel_tol=0.01) ->", math.isclose(1.0, 1.05, rel_tol=0.01))
# Zero ke qareeb rel_tol kaam nahi karta -> abs_tol do
print("isclose(0.0, 1e-12) ->", math.isclose(0.0, 1e-12))
print("isclose(0.0, 1e-12, abs_tol=1e-9) ->", math.isclose(0.0, 1e-12, abs_tol=1e-9))

# Purana manual tareeqa (agar isclose na ho)
print("\nmanual: abs(a-b) < 1e-9 ->", abs(a - b) < 1e-9)
""")

C(r"""
# --- Hal 2: Decimal — paise ke liye LAZMI ---
from decimal import Decimal, getcontext, ROUND_HALF_UP

# GALAT: float se Decimal banana (float ki error saath aa jati hai)
print("Decimal(0.1) =", Decimal(0.1))

# SAHI: string se Decimal banao
print("Decimal('0.1') =", Decimal("0.1"))

print("\n--- Exact decimal arithmetic ---")
print("Decimal('0.1') + Decimal('0.2') =", Decimal("0.1") + Decimal("0.2"))
print("== Decimal('0.3') ->", Decimal("0.1") + Decimal("0.2") == Decimal("0.3"), "  <-- TRUE!")

# Precision control
getcontext().prec = 6                       # 6 significant digits
print("\nprec=6, 1/7 =", Decimal(1) / Decimal(7))
getcontext().prec = 28                      # default wapas

# Paise wala rounding (banker's nahi, aam insaan wala)
price = Decimal("19.995")
print("\n19.995 -> 2 decimals (HALF_UP):", price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
print("float ke sath wahi kaam:", round(19.995, 2), "  <-- float ki approximation ka asar")
""")

C(r"""
# --- Hal 3: Fraction — exact rational numbers ---
from fractions import Fraction

one_third = Fraction(1, 3)
print("Fraction(1, 3) =", one_third)
print("teen baar jama =", one_third + one_third + one_third, "  <-- EXACT 1")

# float se yahi kaam karo to error aati hai
print("float 1/3 teen baar =", 1/3 + 1/3 + 1/3, "| == 1.0 ->", (1/3 + 1/3 + 1/3) == 1.0)

# String se bhi ban jata hai, aur normalize khud karta hai
print("\nFraction('3/6')  =", Fraction("3/6"))     # 1/2
print("Fraction(6, 8)   =", Fraction(6, 8))       # 3/4
print("mixed math       =", Fraction(1, 2) + Fraction(1, 3))
print("float me convert :", float(Fraction(1, 3)))

# .as_integer_ratio() — float ki chhupi hui asli qeemat
print("\n(0.25).as_integer_ratio() =", (0.25).as_integer_ratio(), "(0.25 exact hai)")
print("(0.1).as_integer_ratio()  =", (0.1).as_integer_ratio(), "(0.1 exact nahi)")
""")

M(r"""
### Kab kya use karein — decision table

| Kaam | Type | Kyun |
|---|---|---|
| Paisa, invoice, tax, banking | `Decimal` | exact decimal, rounding control |
| Science / engineering / ML | `float` | tez, hardware-supported |
| Exact ratios (1/3, 2/7) | `Fraction` | koi rounding error nahi |
| Counting, index, ID | `int` | exact aur unlimited |
| Float barabari check | `math.isclose` | `==` **kabhi nahi** |

**Interview tip:** "Money ko float me kyun store nahi karte?" — kyunki `0.1 + 0.2 != 0.3`;
har transaction par chhoti error jama hoti hai aur lakhon transactions ke baad balance mismatch
ho jata hai. Practical hal: `Decimal` ya integer **paise/cents** me store karo.
""")

C(r"""
# --- round() ka BANKER'S ROUNDING gotcha (interview favourite) ---
# Python "round half to even" karta hai (IEEE-754 standard), school wala "half up" nahi.
print("round(0.5) =", round(0.5), "  <-- 0, na ke 1!")
print("round(1.5) =", round(1.5), "  <-- 2")
print("round(2.5) =", round(2.5), "  <-- 2, na ke 3!")
print("round(3.5) =", round(3.5), "  <-- 4")
print("Pattern: tie hone par QAREEB TARIN EVEN number chunta hai.")

print("\n--- ndigits ke sath ---")
print("round(3.14159, 2) =", round(3.14159, 2))
print("round(1234.5678, -2) =", round(1234.5678, -2), "(-ve ndigits = 100 ke multiple par)")
print("round(2.675, 2) =", round(2.675, 2), "  <-- 2.68 nahi! float 2.675 asal me 2.67499... hai")

print("\n--- Agar school wala rounding chahiye ---")
from decimal import Decimal, ROUND_HALF_UP
def round_half_up(x, places=0):
    '''Insani (half-up) rounding — 2.5 -> 3, 3.5 -> 4.'''
    q = Decimal(1).scaleb(-places)              # 0 -> 1, 2 -> 0.01
    return float(Decimal(str(x)).quantize(q, rounding=ROUND_HALF_UP))

for v in (0.5, 1.5, 2.5, 3.5):
    print(f"round({v}) = {round(v)}   |   round_half_up({v}) = {round_half_up(v)}")

# int() vs round() vs floor/ceil/trunc
import math
print("\n--- int/floor/ceil/trunc ka farq (-2.7 par) ---")
x = -2.7
print(f"int({x})        = {int(x)}     (zero ki taraf truncate)")
print(f"math.trunc({x}) = {math.trunc(x)}     (wahi kaam)")
print(f"math.floor({x}) = {math.floor(x)}     (neeche ki taraf)")
print(f"math.ceil({x})  = {math.ceil(x)}     (upar ki taraf)")
print(f"round({x})      = {round(x)}     (qareeb tarin)")
""")

M(r"""
---
## 7. `complex`, `bool` aur `NoneType`

### `complex`
`a + bj` shakal. Electrical engineering, signal processing, FFT me kaam aata hai.
Python me `j` (na ke `i`) use hota hai — aur `1j` likhna zaroori hai, sirf `j` variable samjha jayega.

### `bool`
`bool` **`int` ka subclass** hai! `True == 1`, `False == 0`. Isi liye `sum([True, True, False])`
= 2 chalta hai — aur ye counting ka mashhoor idiom hai.

### `NoneType`
`None` = "koi value nahi". **Singleton** hai (poore program me ek hi object), isi liye compare
karne ke liye hamesha `is None` / `is not None` likho, `== None` nahi.
""")

C(r"""
# --- complex numbers ---
z = 3 + 4j
print("z        =", z, "| type:", type(z).__name__)
print("z.real   =", z.real, "(float hoti hai)")
print("z.imag   =", z.imag)
print("abs(z)   =", abs(z), "(magnitude = sqrt(3^2+4^2))")
print("z.conjugate() =", z.conjugate())

print("\narithmetic:")
print("(3+4j) + (1-2j) =", (3 + 4j) + (1 - 2j))
print("(3+4j) * (1-2j) =", (3 + 4j) * (1 - 2j))
print("complex(2, 5)   =", complex(2, 5))
print("complex('2+5j') =", complex("2+5j"), "(string me space na ho!)")

# Gotcha: complex ko order (< >) se compare nahi kar sakte
try:
    print((1 + 2j) < (3 + 4j))
except TypeError as e:
    print("\nTypeError:", e, "-> complex me order nahi hota, sirf == / != chalta hai")

# math module complex support nahi karta, cmath karta hai
import cmath
print("\ncmath.sqrt(-1) =", cmath.sqrt(-1))
try:
    math.sqrt(-1)
except ValueError as e:
    print("math.sqrt(-1) -> ValueError:", e)
""")

C(r"""
# --- bool: int ka subclass ---
print("isinstance(True, int) ->", isinstance(True, int), "  <-- bool IS an int")
print("issubclass(bool, int) ->", issubclass(bool, int))
print("True == 1  ->", True == 1)
print("False == 0 ->", False == 0)
print("True + True =", True + True, "(yani 2)")
print("True * 5    =", True * 5)

# Isi wajah se counting ka khoobsurat idiom:
marks = [45, 78, 92, 33, 67, 88, 21]
passed = sum(m >= 50 for m in marks)          # har comparison True/False -> 1/0
print(f"\n{len(marks)} me se {passed} pass hue (sum of booleans idiom)")

# bool() kis kis cheez ko False kehta hai (falsy values)
falsy = [0, 0.0, 0j, "", [], (), {}, set(), None, False, range(0)]
print("\nFalsy values:")
for f in falsy:
    print(f"  bool({repr(f):<9}) = {bool(f)}")
print("\nBaqi sab kuch truthy hai -> bool(-1) =", bool(-1), ", bool('False') =", bool("False"))

# Gotcha: True/False ko dict key ki tarah use karna
d = {1: "ek", True: "sach"}                   # 1 aur True ka hash same!
print("\n{1:'ek', True:'sach'} ->", d, "  <-- ek hi key bani")
""")

C(r"""
# --- None ---
nothing = None
print("nothing      =", nothing)
print("type         =", type(nothing).__name__)
print("bool(None)   =", bool(nothing), "(falsy hai)")

# Singleton proof: har None ek hi object hai
a = None
b = None
print("\na is b ->", a is b, "| id same? ->", id(a) == id(b))

# Function jo kuch return na kare, None deta hai
def greet(name):
    print("Salam,", name)                     # sirf print, return nahi

result = greet("Sara")
print("greet() ka return:", result)

# list.sort() bhi None deta hai (yahi classic bug hai)
nums = [3, 1, 2]
wrong = nums.sort()                            # in-place sort, return None
print("\nnums.sort() ka return:", wrong, "  <-- yahan log phaste hain")
print("nums khud sort ho gaya:", nums)
print("Naya list chahiye to sorted() use karo:", sorted([3, 1, 2]))

# == None vs is None
print("\n--- == None kyun bura hai ---")
class Weird:
    def __eq__(self, other):
        return True                            # sab ke barabar hone ka dawa!

w = Weird()
print("w == None ->", w == None, "  <-- jhoot bol raha hai")
print("w is None ->", w is None, "  <-- sach: identity jhoot nahi bol sakti")
""")

M(r"""
---
## 8. Type casting (type conversion)

**Do qismein:**

1. **Implicit (automatic / coercion):** Python khud chhoti type ko bari me badalta hai taake
   information na khoye. Numeric tower: `bool → int → float → complex`.
2. **Explicit (manual):** Tum khud `int()`, `float()`, `str()`, `bool()`, `complex()`,
   `list()`, `tuple()`, `set()`, `dict()` call karte ho.

**Gotcha:** Explicit conversion me data **kho sakta** hai (`int(3.9)` → `3`) ya
**ValueError** aa sakta hai (`int("abc")`).
""")

C(r"""
# --- Implicit conversion (Python khud karta hai) ---
print("int + float   =", 2 + 3.5, "->", type(2 + 3.5).__name__, "(int float me promote hua)")
print("bool + int    =", True + 10, "->", type(True + 10).__name__)
print("float+complex =", 1.5 + (2 + 3j), "->", type(1.5 + (2 + 3j)).__name__)
print("int / int     =", 7 / 2, "->", type(7 / 2).__name__, "(/ hamesha float deta hai!)")
print("int // int    =", 7 // 2, "->", type(7 // 2).__name__)
print("int ** int    =", 2 ** 3, "| negative power:", 2 ** -1, "->", type(2 ** -1).__name__)

print("\nNumeric tower: bool -> int -> float -> complex")
print("Chhoti type bari me jati hai, ulta nahi (taake data na khoye).")

# Magar str ke sath koi implicit conversion NAHI
try:
    print("Umar: " + 25)
except TypeError as e:
    print("\nTypeError:", e)
    print("Hal 1 (cast):   'Umar: ' + str(25)  ->", "Umar: " + str(25))
    print("Hal 2 (f-str):  f'Umar: {25}'       ->", f"Umar: {25}")
""")

C(r"""
# --- Explicit conversion aur uske khatre ---
print("--- int() ---")
print("int(3.9)     =", int(3.9),   "(truncate, round NAHI)")
print("int(-3.9)    =", int(-3.9),  "(zero ki taraf, -4 nahi)")
print("int('42')    =", int("42"))
print("int('  42 ') =", int("  42 "), "(aage peeche space chal jata hai)")
print("int(True)    =", int(True))

for bad in ("42.5", "abc", "", "4 2"):
    try:
        int(bad)
    except ValueError as e:
        print(f"int({bad!r}) -> ValueError: {e}")

print("\n--- float() ---")
print("float('3.14')  =", float("3.14"))
print("float('1e-3')  =", float("1e-3"))
print("float('  2 ')  =", float("  2 "))
print("float(7)       =", float(7))
print("float('inf')   =", float("inf"))
try:
    float("3.14.15")
except ValueError as e:
    print("float('3.14.15') -> ValueError:", e)

print("\n--- str() vs repr() ---")
print("str(3.14)   =", str(3.14),  "| repr(3.14)  =", repr(3.14))
print("str('hi')   =", str("hi"),  "| repr('hi')  =", repr("hi"), "<- repr me quotes hain")
print("str([1,2])  =", str([1, 2]))

print("\n--- bool() ---")
print("bool('False') =", bool("False"), "<-- non-empty string TRUTHY hai! classic trap")
print("bool('0')     =", bool("0"),     "<-- yeh bhi True!")
print("bool(0.0)     =", bool(0.0))
print("bool([])      =", bool([]), "| bool([0]) =", bool([0]), "<- non-empty list True")

print("\n--- Do-qadam conversion ('42.7' -> int) ---")
print("int('42.7') fail hota hai, is liye: int(float('42.7')) =", int(float("42.7")))
""")

C(r"""
# --- Container conversions ---
print("list('abc')          =", list("abc"))
print("tuple([1, 2, 3])     =", tuple([1, 2, 3]))
print("set([1, 2, 2, 3])    =", set([1, 2, 2, 3]), "(duplicates gaye)")
print("list({'a': 1, 'b': 2}) =", list({"a": 1, "b": 2}), "(sirf keys aati hain)")
print("dict([('a', 1), ('b', 2)]) =", dict([("a", 1), ("b", 2)]))
print("dict(zip('abc', [1,2,3]))  =", dict(zip("abc", [1, 2, 3])))
print("list(range(5))       =", list(range(5)))
print("''.join(['a','b'])   =", "".join(["a", "b"]), "(list -> str ka sahi tareeqa)")

# Gotcha: str(list) vs join
nums = [1, 2, 3]
print("\nstr([1,2,3])              =", repr(str(nums)), "<- brackets bhi aa gaye")
print("','.join(map(str, nums))  =", repr(",".join(map(str, nums))), "<- yeh chahiye tha")
""")

M(r"""
---
## 9. Operators — poora nazariya

Python ke operators 7 gharanon me:

| Gharana | Operators |
|---|---|
| Arithmetic | `+  -  *  /  //  %  **  @` |
| Comparison (relational) | `==  !=  >  <  >=  <=` |
| Logical | `and  or  not` |
| Bitwise | `&  \|  ^  ~  <<  >>` |
| Assignment | `=  +=  -=  *=  /=  //=  %=  **=  &=  \|=  ^=  <<=  >>=` |
| Identity | `is  is not` |
| Membership | `in  not in` |

(`@` matrix multiplication ke liye hai — numpy/pandas me kaam aata hai, plain Python types me nahi.)

### 9.1 Arithmetic operators

| Op | Naam | `7` aur `2` par |
|---|---|---|
| `+` | jama | `9` |
| `-` | tafreeq | `5` |
| `*` | zarb | `14` |
| `/` | **true division** — hamesha `float` | `3.5` |
| `//` | **floor division** — neeche ki taraf | `3` |
| `%` | modulo (baqi) | `1` |
| `**` | power | `49` |
""")

C(r"""
# --- Arithmetic operators ka pura tour ---
a, b = 7, 2
print(f"a = {a}, b = {b}\n")
print(f"a + b  = {a + b}")
print(f"a - b  = {a - b}")
print(f"a * b  = {a * b}")
print(f"a / b  = {a / b}   <- type {type(a / b).__name__} (int/int bhi float deta hai)")
print(f"a // b = {a // b}   <- type {type(a // b).__name__} (floor division)")
print(f"a % b  = {a % b}")
print(f"a ** b = {a ** b}")
print(f"divmod(a, b) = {divmod(a, b)}   <- (a//b, a%b) ek sath, tez bhi hai")

print("\n--- float ke sath ---")
print("7.0 // 2 =", 7.0 // 2, "->", type(7.0 // 2).__name__, "(float floor bhi float rehta hai)")
print("7.5 % 2  =", 7.5 % 2)
print("2 ** 0.5 =", 2 ** 0.5, "(square root)")
print("2 ** -1  =", 2 ** -1, "-> int**negative = float")
print("pow(2, 10) =", pow(2, 10), "| pow(2, 10, 1000) =", pow(2, 10, 1000), "(modular power)")

# ZeroDivisionError
for op, fn in [("/", lambda: 1 / 0), ("//", lambda: 1 // 0), ("%", lambda: 1 % 0)]:
    try:
        fn()
    except ZeroDivisionError as e:
        print(f"1 {op} 0 -> ZeroDivisionError: {e}")
""")

M(r"""
### 9.2 `//` aur `%` negative numbers ke sath — C/Java se ALAG!

Ye interview me bohat poocha jata hai.

- **Python:** `//` **floor** karta hai (yani `-inf` ki taraf), aur `%` ka natija **divisor ke sign**
  ka hota hai. Hamesha `a == (a // b) * b + (a % b)`.
- **C / C++ / Java:** division zero ki taraf truncate karta hai, aur `%` ka sign **dividend** ka hota hai.

Yani `-7 // 2` Python me `-4` hai magar C me `-3`. Aur `-7 % 2` Python me `1` hai magar C me `-1`.

**Faida:** Python ka modulo hamesha `0 <= result < abs(b)` (positive divisor ke sath) deta hai,
is liye circular indexing (`arr[i % n]`), clock arithmetic aur hashing me bug nahi hota.
""")

C(r"""
# --- Negative floor division / modulo ---
import math

cases = [(7, 2), (-7, 2), (7, -2), (-7, -2)]
print(f"{'a':>4} {'b':>4} | {'a//b':>5} {'a%b':>5} | {'divmod':>10} | {'C-style %':>10}")
print("-" * 52)
for a, b in cases:
    c_style = math.fmod(a, b)          # fmod = C jaisa behaviour (sign dividend ka)
    print(f"{a:>4} {b:>4} | {a // b:>5} {a % b:>5} | {str(divmod(a, b)):>10} | {c_style:>10}")

print("\nQanoon: a == (a // b) * b + (a % b) — hamesha sach")
for a, b in cases:
    print(f"  {a} == ({a}//{b})*{b} + ({a}%{b}) = {(a // b) * b + (a % b)} ->", a == (a // b) * b + (a % b))

print("\n--- Practical faida: circular index ---")
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
print("aaj Wed (index 2) hai; 5 din pehle kaun tha?")
print("  (2 - 5) % 7 =", (2 - 5) % 7, "->", days[(2 - 5) % 7], "(negative index par bhi sahi)")
print("Modulo se even/odd:", [(n, "even" if n % 2 == 0 else "odd") for n in (-3, -2, 3, 4)])
""")

M(r"""
### 9.3 Comparison operators + chained comparison

`==  !=  >  <  >=  <=` — natija hamesha `bool`.

**Python ka special tohfa: chaining.** `1 < x < 10` asal me `(1 < x) and (x < 10)` hai —
magar `x` sirf **ek baar** evaluate hota hai. Ye C/Java me mumkin nahi (wahan `1 < x < 10`
ka matlab kuch aur ban jata hai).
""")

C(r"""
# --- Comparison basics ---
print("5 == 5.0   ->", 5 == 5.0, "(value barabar, type mukhtalif — == ko farq nahi)")
print("5 is 5.0   ->", 5 is 5.0, "(identity alag hai)")
print("'abc' < 'abd' ->", "abc" < "abd", "(lexicographic, NB 03 me tafseel)")
print("[1,2] < [1,3] ->", [1, 2] < [1, 3], "(element-by-element)")
print("(1,2) == (1,2) ->", (1, 2) == (1, 2))

# Mukhtalif types ka order compare karna -> TypeError
try:
    print(3 < "4")
except TypeError as e:
    print("\n3 < '4' -> TypeError:", e)
print("Magar == chalta hai (False deta hai):", 3 == "4")

print("\n--- Chained comparison ---")
x = 5
print("1 < x < 10        ->", 1 < x < 10)
print("1 < x < 3         ->", 1 < x < 3)
print("0 <= x <= 10 == True? ->", 0 <= x <= 10)
print("a == b == c style  ->", 1 == 1.0 == True, "(teeno value-barabar hain)")

# Sabot ke sath: middle expression sirf EK baar evaluate hota hai
def middle():
    print("   [middle() chala]")
    return 5

print("\n1 < middle() < 10 ->", end=" ")
print()
res = 1 < middle() < 10
print("natija:", res, "-> 'middle() chala' sirf ek baar chapa")
""")

M(r"""
### 9.4 Logical operators — aur do bare gotcha

`and`, `or`, `not`.

**Gotcha 1 — short-circuiting:** `and` me agar pehla falsy hai to doosra **chalta hi nahi**.
`or` me agar pehla truthy hai to doosra nahi chalta. Isi se safe-guard likhte hain:
`if user and user.is_active:`

**Gotcha 2 — `and`/`or` bool nahi, OPERAND return karte hain:**
- `a and b` → `a` falsy ho to `a`, warna `b`
- `a or b` → `a` truthy ho to `a`, warna `b`

Isi se mashhoor default-value idiom banta hai: `name = user_input or "Guest"`.
""")

C(r"""
# --- Short-circuiting ka sabot ---
def loud(label, value):
    '''Har call par print karta hai, taake pata chale ke chala ya nahi.'''
    print(f"   [{label} evaluate hua]")
    return value

print("False and loud('B', True):")
r1 = False and loud("B", True)      # B chalega hi nahi
print("natija:", r1)

print("\nTrue or loud('B', True):")
r2 = True or loud("B", True)        # B chalega hi nahi
print("natija:", r2)

print("\nTrue and loud('B', 'value-B'):")
r3 = True and loud("B", "value-B")  # ab B chalega
print("natija:", r3)

# Practical: crash se bachao
users = [{"name": "Ali", "email": "ali@test.com"}, None]
for u in users:
    # 'u and' pehle check karta hai; None hone par u['email'] chalta hi nahi
    email = u and u.get("email")
    print(f"user={u} -> email={email}")

# ZeroDivision se bachne ka safe pattern
n = 0
print("\nsafe average:", (10 / n) if n else "n=0, division skip kiya")
""")

C(r"""
# --- and/or OPERAND return karte hain, bool nahi ---
print("1 and 2        =", 1 and 2,        "(pehla truthy -> doosra return)")
print("0 and 2        =", 0 and 2,        "(pehla falsy -> pehla return)")
print("1 or 2         =", 1 or 2,         "(pehla truthy -> pehla return)")
print("0 or 2         =", 0 or 2,         "(pehla falsy -> doosra return)")
print("'' or 'Guest'  =", "" or "Guest",  "<- default value idiom")
print("None or 0 or [] or 'last' =", None or 0 or [] or "last", "(pehla truthy ya aakhri)")
print("type(1 and 2)  =", type(1 and 2).__name__, "<- int, bool NAHI")
print("not 5          =", not 5, "<- 'not' hamesha bool deta hai")

print("\n--- 'or' default idiom ka KHATRA ---")
def set_quantity(qty):
    q = qty or 10                     # 0 falsy hai -> 10 ban jayega! BUG
    return q
def set_quantity_fixed(qty):
    q = 10 if qty is None else qty    # sirf None par default
    return q

for val in (5, 0, None):
    print(f"qty={val!r:<5} -> or-idiom: {set_quantity(val):<3} | fixed: {set_quantity_fixed(val)}")
print("Sabaq: 0, '', [] valid values ho sakti hain -> 'is None' se check karo.")

# Truth table
print("\n--- Truth table ---")
print(f"{'A':<6} {'B':<6} {'A and B':<9} {'A or B':<8} {'not A'}")
for A in (True, False):
    for B in (True, False):
        print(f"{str(A):<6} {str(B):<6} {str(A and B):<9} {str(A or B):<8} {not A}")
""")

M(r"""
### 9.5 Bitwise operators

Ye numbers ke **binary bits** par kaam karte hain. Low-level, tez, aur interview me
"is number power of 2?" jaise sawalon me kaam aate hain.

| Op | Naam | Matlab |
|---|---|---|
| `&` | AND | dono bit 1 hon to 1 |
| `\|` | OR | koi ek 1 ho to 1 |
| `^` | XOR | bits **mukhtalif** hon to 1 |
| `~` | NOT (complement) | `~x == -(x+1)` |
| `<<` | left shift | `x << n == x * 2**n` |
| `>>` | right shift | `x >> n == x // 2**n` |

**Yaad rakho:** `~5 == -6` (two's complement ki wajah se, `-(5+1)`).
""")

C(r"""
# --- Bitwise operators, binary ke sath sath ---
a, b = 12, 10                  # 12 = 1100, 10 = 1010

print(f"a = {a:>3} = {a:04b}")
print(f"b = {b:>3} = {b:04b}\n")
print(f"a & b  = {a & b:>3} = {a & b:04b}   (AND)")
print(f"a | b  = {a | b:>3} = {a | b:04b}   (OR)")
print(f"a ^ b  = {a ^ b:>3} = {a ^ b:04b}   (XOR)")
print(f"a << 1 = {a << 1:>3} = {a << 1:04b}   (left shift = *2)")
print(f"a >> 1 = {a >> 1:>3} = {a >> 1:04b}   (right shift = //2)")
print(f"~a     = {~a:>3}          (NOT, = -(a+1))")

print("\n--- ~ ko samjho ---")
for n in (0, 1, 5, -1, -6):
    print(f"~{n:<3} = {~n:<4}  (formula: -(n+1))")

print("\n--- shift = fast multiply/divide by 2 ---")
print("5 << 3 =", 5 << 3, "== 5 * 2**3 =", 5 * 2 ** 3)
print("40 >> 2 =", 40 >> 2, "== 40 // 2**2 =", 40 // 2 ** 2)
print("-7 >> 1 =", -7 >> 1, "(negative par bhi FLOOR karta hai, == -7 // 2 =", -7 // 2, ")")

# Bitwise sirf int (aur bool/set) par chalta hai
try:
    3.5 & 1
except TypeError as e:
    print("\n3.5 & 1 -> TypeError:", e)
""")

C(r"""
# --- Bitwise ke asli practical tricks (interview me kaam aate hain) ---

# 1. Even / odd — sab se tez tareeqa
print("--- 1. Even/odd via x & 1 ---")
for n in (4, 7, 0, -3):
    print(f"  {n:>3} -> {'even' if n & 1 == 0 else 'odd'}")

# 2. Power of two check (LC 231 me isi ka use karenge)
print("\n--- 2. Power of two: n > 0 and n & (n-1) == 0 ---")
for n in (1, 2, 8, 12, 0, -8):
    print(f"  {n:>3}: {n:>5b} & {n-1:>5b} = {n & (n - 1):<3} -> {n > 0 and n & (n - 1) == 0}")

# 3. Swap without temp variable (XOR trick)
print("\n--- 3. XOR swap ---")
x, y = 15, 27
print(f"  pehle : x={x}, y={y}")
x ^= y
y ^= x
x ^= y
print(f"  baad  : x={x}, y={y}  (Python me a,b=b,a behtar hai, magar trick jaanna chahiye)")

# 4. XOR se duplicate dhoondna (LC 136 ka core idea)
print("\n--- 4. XOR se akela number ---")
nums = [4, 1, 2, 1, 2]
xor_all = 0
for n in nums:
    xor_all ^= n                # a^a = 0, a^0 = a -> jode kat jate hain
print(f"  {nums} -> akela: {xor_all}")

# 5. Bit count aur bit_length
print("\n--- 5. int ke bit helpers ---")
n = 156
print(f"  n = {n} = {n:b}")
print(f"  n.bit_length() = {n.bit_length()}  (kitne bits chahiye)")
print(f"  n.bit_count()  = {n.bit_count()}  (kitne 1 hain — Python 3.10+)")
""")

C(r"""
# --- Bitwise FLAGS system: real-world use ---
# Har permission ko ek alag bit do
READ    = 0b001      # 1
WRITE   = 0b010      # 2
EXECUTE = 0b100      # 4

def describe(perm):
    '''Permission integer ko insani shakal me badalta hai.'''
    names = []
    if perm & READ:                     # bit set hai?
        names.append("READ")
    if perm & WRITE:
        names.append("WRITE")
    if perm & EXECUTE:
        names.append("EXECUTE")
    return "+".join(names) or "NONE"

user = READ | WRITE                      # do permissions jama (OR se set karte hain)
print(f"user = {user} = {user:03b} -> {describe(user)}")

user |= EXECUTE                          # permission ADD karo
print(f"EXECUTE add   -> {user:03b} -> {describe(user)}")

user &= ~WRITE                           # permission REMOVE karo (AND with NOT)
print(f"WRITE remove  -> {user:03b} -> {describe(user)}")

user ^= READ                             # TOGGLE karo
print(f"READ toggle   -> {user:03b} -> {describe(user)}")

print("\nCheck:", "WRITE hai?" , bool(user & WRITE), "| EXECUTE hai?", bool(user & EXECUTE))
print("Faida: 1 integer me kai boolean flags — memory aur speed dono behtar.")
""")

M(r"""
### 9.6 Assignment aur augmented assignment

| Op | Barabar hai | Note |
|---|---|---|
| `x = 5` | — | bind / rebind |
| `x += 3` | `x = x + 3` | mutable par **in-place** ho sakta hai |
| `x -= 3` | `x = x - 3` | |
| `x *= 3` | `x = x * 3` | |
| `x /= 3` | `x = x / 3` | natija float ban jata hai |
| `x //= 3` | `x = x // 3` | |
| `x %= 3` | `x = x % 3` | |
| `x **= 3` | `x = x ** 3` | |
| `x &= y`, `x \|= y`, `x ^= y`, `x <<= n`, `x >>= n` | bitwise versions | |

**Bara farq:** immutable (int, str, tuple) ke liye `+=` **naya object** banata hai.
Mutable (list) ke liye `+=` object ko **usi jagah** (in-place) badalta hai — jo `x = x + y`
se mukhtalif behaviour deta hai. Ye interview ka bohat sundar sawal hai.
""")

C(r"""
# --- Augmented assignment: int (immutable) ---
x = 10
print("shuru      : x =", x, "| id:", id(x))
x += 5          # naya int object bana (15), x us par shift hua
print("x += 5     : x =", x, "| id badal gaya:", id(x))
x -= 3
x *= 2
x //= 4
x **= 2
print("kai steps  : x =", x)
y = 10
y /= 4          # / hamesha float
print("y /= 4     :", y, "->", type(y).__name__)

print("\n--- list (mutable): += vs = x + y ---")
lst1 = [1, 2]
alias1 = lst1                 # doosra tag
lst1 += [3]                   # IN-PLACE extend (list.__iadd__)
print("lst1 += [3]  -> lst1:", lst1, "| alias1:", alias1, "<- alias BHI badla")

lst2 = [1, 2]
alias2 = lst2
lst2 = lst2 + [3]             # NAYA list bana, lst2 shift hua
print("lst2 = lst2+[3] -> lst2:", lst2, "| alias2:", alias2, "<- alias purana hi raha")

print("\n--- += string ke sath (immutable) ---")
s = "ab"
print("id pehle:", id(s), end="  ")
s += "c"                      # naya string bana
print("| id baad:", id(s), "-> str immutable hai")

# += list par kisi bhi iterable ko le leta hai (extend jaisa), + sirf list leta hai
lst3 = [1, 2]
lst3 += "xy"                  # string bhi iterable hai -> chars add ho gaye!
print("\nlst3 += 'xy' ->", lst3, "<- GOTCHA: chars alag alag add hue")
try:
    [1, 2] + "xy"
except TypeError as e:
    print("[1,2] + 'xy' -> TypeError:", e)
""")

C(r"""
# --- Sab se mashhoor tuple gotcha: t[0] += [...] ---
t = ([1, 2], "immutable-part")
print("pehle t =", t)

try:
    t[0] += [3]                 # do kaam: list.__iadd__ (chalta hai) phir t[0] = ... (fail)
except TypeError as e:
    print("TypeError:", e)

print("baad  t =", t, "  <-- HAIRANI: error ke BAWAJOOD list badal gayi!")
print('''
Wajah: `t[0] += [3]` ka matlab hai:
   tmp = t[0]
   tmp = tmp.__iadd__([3])   # list in-place badal gayi -> KAAMYAB
   t[0] = tmp                # tuple assignment -> TypeError
Yani mutation pehle ho chuka, error baad me aaya.
Hal: t[0].append(3)  ya  t[0].extend([3])  likho — assignment se bacho.
''')
""")

M(r"""
### 9.7 Identity operators (`is`, `is not`) — aur `is` vs `==`

| | `==` | `is` |
|---|---|---|
| Kya check karta hai | **value** barabar hai? | **wahi ek object** hai? |
| Kaise | `__eq__()` call karta hai (customize ho sakta hai) | `id()` compare karta hai |
| Kab use karo | rozana comparison | `None`, `True`, `False`, sentinel, singleton |

**Sunehri qanoon:**
- `x is None` ✅ / `x == None` ❌
- `x == 5` ✅ / `x is 5` ❌ (kabhi kabhi chal jata hai — aur wahi khatra hai)

Python **performance optimizations** karta hai jo `is` ko dhoka-daih bana dete hain:
1. **Small-integer caching:** `-5` se `256` tak ke ints pehle se bane hue hain aur reuse hote hain.
2. **String interning:** identifier-jaise string literals (letters/digits/underscore) cache hote hain.
3. **Constant folding:** ek hi code block me same literal aik hi object ban jata hai.

Ye sab **implementation detail** hain — inhe apne logic ki bunyaad na banao.
""")

C(r"""
# --- Small integer caching ---
a = 256
b = 256
print("a = 256, b = 256      -> a is b:", a is b, "(cached range me hai)")

# 257 ke liye: ek hi cell me likhne se constant-folding dhoka de deti hai,
# is liye runtime par banate hain
x = 1000
y = int("1000")                 # runtime par naya object
print("x = 1000, y = int('1000') -> x is y:", x is y, "<- FALSE (cache se bahar)")
print("magar x == y:", x == y, "<- value barabar hai, bas yahi ahem hai")

print("\ncache ki hadd (-5 se 256):")
for n in (-6, -5, 0, 256, 257):
    left = n
    right = int(str(n))         # runtime par doosra object banane ki koshish
    print(f"  {n:>5}: {left} is {right} -> {left is right}")

print("\n--- String interning ---")
s1 = "hello"
s2 = "hello"
print("s1 = 'hello', s2 = 'hello'  -> s1 is s2:", s1 is s2, "(interned literal)")

part = "hel"
s3 = part + "lo"                # runtime par bana -> intern nahi hua
print("s3 = part + 'lo'          -> s1 is s3:", s1 is s3, "<- FALSE")
print("magar s1 == s3:", s1 == s3, "<- yahi check karna chahiye")

s4 = "hello world!"             # space aur ! ki wajah se identifier-jaisa nahi
s5 = "".join(["hello", " world!"])
print("\ns4 = 'hello world!' vs runtime-built -> is:", s4 is s5, "| == :", s4 == s5)

import sys
print("sys.intern se zabardasti intern:", sys.intern(s5) is sys.intern(s4))
""")

C(r"""
# --- is vs == : kab kaun sa (rules of thumb) ---
print("--- None ke sath hamesha 'is' ---")
val = None
print("val is None     ->", val is None)
print("val is not None ->", val is not None)

print("\n--- Alag objects, barabar value ---")
l1 = [1, 2, 3]
l2 = [1, 2, 3]
print("l1 == l2 ->", l1 == l2, "(value same)")
print("l1 is l2 ->", l1 is l2, "(object alag)")
print("l1 is l1 ->", l1 is l1)

print("\n--- True/False/None singleton hain ---")
print("True is True   ->", True is True)
print("bool(1) is True ->", bool(1) is True)
print("1 == True      ->", 1 == True, "| 1 is True ->", 1 is True, "<- alag objects")

print("\n--- Sentinel pattern: 'None bhi ek valid value hai' wala masla ---")
MISSING = object()                       # unique sentinel object

def get_setting(config, key, default=MISSING):
    '''Agar default na diya jaye to missing key par error, warna default.'''
    if key in config:
        return config[key]
    if default is MISSING:               # 'is' zaroori — value compare nahi karna
        raise KeyError(f"'{key}' missing aur koi default nahi diya")
    return default

cfg = {"debug": None, "port": 8080}
print("config me 'debug' hai magar value None hai ->", get_setting(cfg, "debug"))
print("missing key + default None          ->", get_setting(cfg, "nope", None))
try:
    get_setting(cfg, "nope")
except KeyError as e:
    print("missing key + koi default nahi   -> KeyError:", e)
""")

M(r"""
### 9.8 Membership operators (`in`, `not in`)

`x in container` — "kya `x` andar maujood hai?"

| Container | `in` kya dekhta hai | Complexity |
|---|---|---|
| `str` | **substring** | O(n·m) |
| `list` / `tuple` | element (`==` se) | **O(n)** |
| `set` / `frozenset` | element (hash se) | **O(1)** |
| `dict` | **keys** (values nahi!) | **O(1)** |
| `range` | integer (hisaab se) | O(1) |

**Interview tip:** Bare data me `x in my_list` slow hai. Agar baar baar check karna hai to
pehle `set(my_list)` bana lo — O(n) se O(1) ho jata hai.
""")

C(r"""
# --- Membership har container par ---
print("'ell' in 'hello'      ->", "ell" in "hello", "(substring check)")
print("'h' not in 'hello'    ->", "h" not in "hello")
print("3 in [1, 2, 3]        ->", 3 in [1, 2, 3])
print("3 in (1, 2, 3)        ->", 3 in (1, 2, 3))
print("3 in {1, 2, 3}        ->", 3 in {1, 2, 3})
print("5 in range(10)        ->", 5 in range(10), "| 5 in range(0, 10, 2) ->", 5 in range(0, 10, 2))

d = {"name": "Ali", "age": 25}
print("\n--- dict par 'in' KEYS dekhta hai ---")
print("'name' in d      ->", "name" in d)
print("'Ali' in d       ->", "Ali" in d, "<-- value hai, key nahi -> False")
print("'Ali' in d.values() ->", "Ali" in d.values(), "<-- values ke liye .values()")
print("('name','Ali') in d.items() ->", ("name", "Ali") in d.items())

# Speed ka farq
import time
big_list = list(range(50_000))
big_set = set(big_list)
target = 49_999                          # sab se bura case (aakhir me)

t0 = time.perf_counter()
for _ in range(200):
    _ = target in big_list               # O(n) — poori list scan
t_list = time.perf_counter() - t0

t0 = time.perf_counter()
for _ in range(200):
    _ = target in big_set                # O(1) — hash lookup
t_set = time.perf_counter() - t0

print(f"\n200 lookups | list: {t_list*1000:.2f} ms | set: {t_set*1000:.3f} ms")
print(f"set taqreeban {t_list / max(t_set, 1e-9):.0f}x tez hai")
""")

M(r"""
### 9.9 Walrus operator `:=` (assignment expression, Python 3.8+)

**Kya hai:** Ek *expression* jo value assign bhi karta hai aur **return** bhi karta hai.

**Kyun:** Do faide — (1) ek hi cheez do baar calculate karne se bachao, (2) code chhota aur saaf.

**Syntax:** `(name := expression)` — aksar parentheses ki zaroorat parti hai.

**Kahan ILLEGAL hai:** akela statement ke tor par (`x := 5` galat, `(x := 5)` theek),
aur `f(x = 1)` jaise keyword-argument ki jagah.

**Ehtiyat:** Zaroorat se zyada use karne se code parhna mushkil ho jata hai. Sirf wahan use karo
jahan waqai duplication khatam ho.
""")

C(r"""
# --- Walrus: use case 1 — dobara calculate karne se bachao ---
data = [3, 7, 1, 9, 4, 8]

# Bina walrus: len() do baar (ya ek extra line)
if len(data) > 5:
    print(f"Bina walrus : {len(data)} items hain (len 2 baar chala)")

# Walrus ke sath: ek hi baar
if (n := len(data)) > 5:
    print(f"Walrus ke sath: {n} items hain (len 1 baar chala)")

# --- use case 2 — while loop me "read then check" ---
print("\nwhile + walrus (chunks parhna):")
chunks = iter(["header", "row-1", "row-2", "footer"])
while (chunk := next(chunks, None)) is not None:     # next() ka default None sentinel
    print("   mila:", chunk)

# --- use case 3 — comprehension me compute-once-filter ---
print("\ncomprehension me walrus:")
def expensive(x):
    '''Farz karo ye slow hai — do baar call nahi karna chahte.'''
    return x * x

# Bina walrus: expensive() do baar chalta (filter me aur output me)
without = [expensive(n) for n in data if expensive(n) > 20]
# Walrus ke sath: sirf ek baar
with_walrus = [sq for n in data if (sq := expensive(n)) > 20]
print("   bina walrus :", without)
print("   walrus ke sath:", with_walrus, "(natija same, kaam aadha)")

# --- use case 4 — regex match (bohat common) ---
import re
print("\nregex ke sath (sab se aam use):")
for line in ("age=25", "naam=Ali", "kachra"):
    if (m := re.match(r"age=(\d+)", line)):
        print(f"   {line!r} -> age mila: {m.group(1)}")
    else:
        print(f"   {line!r} -> match nahi")
""")

C(r"""
# --- Walrus kahan ILLEGAL hai ---
bad_snippets = [
    ("x := 5",              "akela statement — parentheses lazmi: (x := 5)"),
    ("y = (a := 1, b := 2)", "ye theek hai — sirf compile test"),
]
for src, note in bad_snippets:
    try:
        compile(src, "<demo>", "exec")
        print(f"OK       : {src!r:<22} ({note})")
    except SyntaxError as e:
        print(f"SyntaxError: {src!r:<20} -> {e.msg}")

# Sahi shakal
(z := 42)                       # parentheses ke sath statement bhi chalta hai
print("\n(z := 42) ke baad z =", z)

# Ek aur maza: while loop ka accumulator
total, values = 0, iter([10, 20, 30])
while (v := next(values, 0)):
    total += v
print("walrus se total:", total)
""")

M(r"""
### 9.10 Operator precedence aur associativity

Jab ek expression me kai operators hon to **precedence** batata hai kaun pehle chalega,
aur **associativity** batata hai barabar precedence walon me direction kya hogi.

**Precedence: sab se ZYADA se sab se KAM (upar se neeche):**

| # | Operator | Associativity |
|---|---|---|
| 1 | `()` grouping | — |
| 2 | `x[i]`, `x[a:b]`, `f(...)`, `x.attr` | left |
| 3 | `await x` | — |
| 4 | `**` | **RIGHT** ⚠️ |
| 5 | `+x`, `-x`, `~x` (unary) | right |
| 6 | `*`, `@`, `/`, `//`, `%` | left |
| 7 | `+`, `-` | left |
| 8 | `<<`, `>>` | left |
| 9 | `&` | left |
| 10 | `^` | left |
| 11 | `\|` | left |
| 12 | `in`, `not in`, `is`, `is not`, `<`, `<=`, `>`, `>=`, `!=`, `==` | chain |
| 13 | `not x` | right |
| 14 | `and` | left |
| 15 | `or` | left |
| 16 | `if – else` (ternary) | right |
| 17 | `lambda` | — |
| 18 | `:=` (walrus) | right |

**Yaad rakhne wale 4 traps:**
1. `**` right-associative: `2**3**2` = `2**(3**2)` = **512**, na ke 64.
2. Unary minus `**` se **kam** precedence rakhta hai: `-2**2` = `-(2**2)` = **-4**.
3. `not` comparison se **kam** precedence rakhta hai: `not a == b` = `not (a == b)`.
4. Bitwise `&` comparison se **zyada** strong hai (C ke ULTA!): `1 & 2 == 2` = `(1 & 2) == 2` = `False`.
   C/C++ me `&` ki precedence `==` se **kam** hai, is liye C wala zehen yahan dhoka khata hai.

**Interview tip:** Sahi jawab jaan lo, magar asli code me **parentheses** lagao. Precedence
yaad karna interview ke liye hai; readable code ke liye brackets hain.
""")

C(r"""
# --- Precedence ke classic traps ---
tests = [
    ("2 + 3 * 4",        2 + 3 * 4,        "* pehle -> 14"),
    ("(2 + 3) * 4",      (2 + 3) * 4,      "brackets ne order badla -> 20"),
    ("2 ** 3 ** 2",      2 ** 3 ** 2,      "** RIGHT assoc -> 2**(3**2) = 512"),
    ("(2 ** 3) ** 2",    (2 ** 3) ** 2,    "zabardasti left -> 64"),
    ("-2 ** 2",          -2 ** 2,          "** pehle, phir minus -> -(2**2) = -4"),
    ("(-2) ** 2",        (-2) ** 2,        "brackets ke sath -> 4"),
    ("10 - 5 - 2",       10 - 5 - 2,       "- LEFT assoc -> (10-5)-2 = 3"),
    ("10 - (5 - 2)",     10 - (5 - 2),     "right karo to 7"),
    ("1 + 2 * 3 ** 2",   1 + 2 * 3 ** 2,   "** -> * -> + = 19"),
    ("7 // 2 * 2",       7 // 2 * 2,       "left assoc -> (7//2)*2 = 6"),
    ("'a' + 'b' * 3",    "a" + "b" * 3,    "* pehle -> 'abbb'"),
]
print(f"{'expression':<20} {'natija':<10} kyun")
print("-" * 62)
for expr, val, why in tests:
    print(f"{expr:<20} {repr(val):<10} {why}")
""")

C(r"""
# --- Logical + comparison precedence traps ---
print("not True == False   ->", not True == False, "  # not (True == False) = not False = True")
print("(not True) == False ->", (not True) == False, "  # False == False = True (ittefaq se same)")
print("not 5 > 3           ->", not 5 > 3, "  # not (5 > 3) = not True = False")

print("\nTrue or False and False  ->", True or False and False, "  # and pehle: True or False")
print("(True or False) and False ->", (True or False) and False, "  # brackets se ulta natija!")

print("\n1 & 2 == 2      ->", 1 & 2 == 2, "  # & zyada strong -> (1 & 2) == 2 -> 0 == 2 -> False")
print("(1 & 2) == 2    ->", (1 & 2) == 2, "  # wahi cheez, saaf likhi hui")
print("1 & (2 == 2)    ->", 1 & (2 == 2), "  # zabardasti ulta karo -> 1 & True -> 1")
print("Note: C/C++ me '&' ki precedence '==' se KAM hai — Python me ZYADA. Yahan C-wale phaste hain.")

print("\nnot 1 in [1, 2] ->", not 1 in [1, 2], "  # 'in' pehle -> not True = False")
print("1 not in [1, 2] ->", 1 not in [1, 2], "  # yahi likhna chahiye (PEP8 bhi kehta hai)")

print("\n--- Ternary ki precedence ---")
print("1 + 2 if True else 99      ->", 1 + 2 if True else 99, "  # (1+2) if True else 99")
print("1 + (2 if True else 99)    ->", 1 + (2 if True else 99))

print("\nSABAQ: bracket lagane se koi sharmindagi nahi. Code doosre insan ke liye likha jata hai.")
""")

M(r"""
---
## 10. Mutable vs Immutable — poora nazariya

| Immutable (badla nahi ja sakta) | Mutable (badla ja sakta hai) |
|---|---|
| `int`, `float`, `complex`, `bool` | `list` |
| `str` | `dict` |
| `tuple` | `set` |
| `frozenset` | `bytearray` |
| `bytes` | custom classes (aam tor par) |
| `range`, `NoneType` | |

**Kyun ahem — 4 asli natije:**
1. **Hashability:** sirf immutable objects `dict` key ya `set` element ban sakte hain.
2. **Function arguments:** mutable argument ko function andar se badal sakta hai (caller ko dikhta hai).
3. **Default arguments:** `def f(x, items=[])` — mashhoor bug (tafseel NB 07 me).
4. **Copy:** immutable ko copy karne ki zaroorat hi nahi (koi badal nahi sakta).

**Gotcha:** `tuple` immutable hai — magar uske **andar** rakha `list` mutable rehta hai!
Tuple sirf ye guarantee deta hai ke "kaun se objects" andar hain, ye nahi ke wo objects khud na badlein.
""")

C(r"""
# --- Immutable: badalne ki koshish -> TypeError ---
s = "hello"
try:
    s[0] = "H"
except TypeError as e:
    print("str item assignment -> TypeError:", e)
print("Hal: naya string banao ->", "H" + s[1:], "| ya s.replace('h','H') ->", s.replace("h", "H"))

t = (1, 2, 3)
try:
    t[0] = 99
except TypeError as e:
    print("\ntuple item assignment -> TypeError:", e)

# int/float/bool bhi immutable hain — unka koi mutating method hi nahi
print("\nint ke paas mutate karne wala method hai?",
      [m for m in dir(int) if not m.startswith('_') and 'set' in m] or "nahi")

print("\n--- Mutable: seedha badal jate hain ---")
lst = [1, 2, 3]
print("id pehle:", id(lst))
lst[0] = 99
lst.append(4)
print("badalne ke baad:", lst, "| id WAHI:", id(lst), "<- object same, andar badla")
""")

C(r"""
# --- id() ke sath immutability ka sabot ---
def show(label, obj):
    print(f"{label:<26} value={obj!r:<18} id={id(obj)}")

print("--- immutable (str): har 'tabdeeli' naya object ---")
name = "Ali"
show("shuru", name)
name += " Khan"                      # naya object
show("after += ' Khan'", name)

print("\n--- mutable (list): tabdeeli usi object me ---")
nums = [1, 2]
show("shuru", nums)
nums.append(3)                       # wahi object
show("after append(3)", nums)
nums = nums + [4]                    # ye REBINDING hai -> naya object
show("after nums = nums + [4]", nums)

print("\n--- Hashability (dict key / set element ban sakta hai?) ---")
candidates = [42, "text", (1, 2), frozenset([1, 2]), True, None, [1, 2], {"a": 1}, {1, 2}]
for c in candidates:
    try:
        h = hash(c)
        print(f"  {type(c).__name__:<10} {str(c):<12} -> hashable ✔ (hash={h})")
    except TypeError:
        print(f"  {type(c).__name__:<10} {str(c):<12} -> NOT hashable ✘ (mutable hai)")
""")

C(r"""
# --- Tuple immutable hai, magar andar ka list mutable! ---
config = ("localhost", 8080, ["admin", "user"])     # teesra element list hai
print("pehle :", config)

config[2].append("guest")            # list ko mutate kiya — tuple ko farq nahi para
print("baad  :", config, "<- tuple 'badla' nahi, uska andar wala list badla")

# Isi wajah se ye tuple hashable NAHI hai
try:
    hash(config)
except TypeError as e:
    print("\nhash(config) -> TypeError:", e)

# Poora immutable tuple hashable hota hai
safe = ("localhost", 8080, ("admin", "user"))
print("hash(safe) kaam karta hai ->", hash(safe) is not None)
print("Sabaq: tuple ki immutability 'shallow' hai — sirf top level.")

# Function argument par asar
def add_tax(prices, rate=0.17):
    '''GALAT: caller ki list ko mutate kar deta hai.'''
    for i in range(len(prices)):
        prices[i] = round(prices[i] * (1 + rate), 2)
    return prices

def add_tax_safe(prices, rate=0.17):
    '''SAHI: naya list banata hai, caller ka data mehfooz.'''
    return [round(p * (1 + rate), 2) for p in prices]

original = [100.0, 250.0]
add_tax(original)
print("\nmutating version ke baad original:", original, "<- caller ka data barbad")

original2 = [100.0, 250.0]
result = add_tax_safe(original2)
print("safe version -> naya:", result, "| original2 mehfooz:", original2)
""")

M(r"""
---
## 11. `input()` — theory (yahan call NAHI karenge)

**Kya hai:** `input()` user se keyboard par ek line parhta hai.

**Syntax:**
```python
name = input("Apna naam likho: ")     # prompt optional hai
age  = int(input("Umar: "))           # input() HAMESHA str deta hai -> cast karo
```

**3 lazmi baatein:**
1. `input()` ka natija **hamesha `str`** hota hai — `input()` se aaye "25" par `+ 1` karo to
   `TypeError` milega. Number chahiye to `int()` / `float()` se cast karo.
2. Ghalat input par `int()` **`ValueError`** phenkta hai → `try/except` me lapeto.
3. Python 2 ka `input()` khatarnaak tha (input ko **code** ki tarah evaluate karta tha).
   Python 2 ka safe version `raw_input()` tha. Python 3 ka `input()` = Python 2 ka `raw_input()`.

**Safe pattern (production style):**
```python
def read_int(prompt, lo=None, hi=None):
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
        except ValueError:
            print("Sirf number likho.");  continue
        if lo is not None and val < lo:  print(f"{lo} se bara likho.");  continue
        if hi is not None and val > hi:  print(f"{hi} se chhota likho."); continue
        return val
```

> **Is notebook (aur poori series) me `input()` kabhi call nahi hoga.** Wajah: notebook
> automated tor par chalta hai; `input()` par wo hamesha ke liye ruk jayega (hang ho jayega).
> Iske bajaye hum data **inline** (list/dict) me rakhte hain — jo testing ke liye behtar bhi hai.
> Ye asal me acha software design hai: logic ko I/O se alag rakho.
""")

C(r"""
# --- input() ki jagah: list se "simulated input" (testable style) ---
# GALAT tareeqa (notebook hang kar dega):  age = int(input("Umar: "))
# SAHI tareeqa: logic ko alag function me rakho, data bahar se do.

def parse_age(raw):
    '''String ko age me badalta hai; masla ho to (None, error) deta hai.'''
    raw = raw.strip()                              # aage peeche ki space hatao
    if not raw:
        return None, "khali input"
    try:
        age = int(raw)                             # cast — yahan ValueError aa sakta hai
    except ValueError:
        return None, f"'{raw}' number nahi hai"
    if not 0 < age < 130:                          # chained comparison
        return None, f"{age} ghair-haqeeqi umar hai"
    return age, None

# "Farzi user inputs" — asli input() ke bajaye
fake_inputs = ["25", " 30 ", "abc", "", "-5", "200", "42"]
for raw in fake_inputs:
    age, err = parse_age(raw)
    status = f"OK -> {age}" if err is None else f"REJECT -> {err}"
    print(f"input {raw!r:<7} : {status}")

print("\nFaida: ye function testable hai. Agar input() andar hota, test likhna mushkil hota.")
""")

M(r"""
---
## 12. String formatting — teen tareeqe

| Tareeqa | Misaal | Kab |
|---|---|---|
| **f-string** (3.6+) | `f"{name} ki umar {age}"` | ✅ **default choice** — tez aur saaf |
| `str.format()` | `"{} ki umar {}".format(name, age)` | template pehle, values baad me |
| `%` (purana) | `"%s ki umar %d" % (name, age)` | legacy code, logging module |

**Interview tip:** f-string sab se **tez** hai kyunki wo compile-time par bytecode me badal jati
hai (koi runtime function call nahi). Lekin `logging` me `logger.info("x=%s", x)` style behtar hai —
wahan string sirf tab banti hai jab log level match kare (lazy evaluation).
""")

C(r"""
# --- f-string: basics ---
name, age, cgpa = "Ayesha", 21, 3.7248

print(f"Seedha       : {name} ki umar {age} saal hai")
print(f"Expression   : agle saal umar {age + 1} hogi")
print(f"Method call  : upper -> {name.upper()}, length -> {len(name)}")
print(f"Ternary      : {'bara' if age >= 18 else 'chhota'}")
sample = {"a": 1, "b": 2}
scores = [90, 85, 70]
print(f"Dict access  : sample['a'] = {sample['a']}")
print(f"List slice   : scores[:2] = {scores[:2]}, sum = {sum(scores)}")
print(f"Repr (!r)    : {name!r}  <- quotes ke sath")
print(f"Str (!s)     : {name!s}")

# Self-documenting '=' (Python 3.8+) — debugging ka best friend
print(f"\nDebug (=)    : {age=}")
print(f"Debug expr   : {age * 2 + 1=}")
print(f"Debug + fmt  : {cgpa=:.2f}")

# Nested quotes: purane Python me alag quotes zaroori thi, 3.12+ me same bhi chalti hain
data = {"city": "Karachi"}
print(f"\nNested quote : {data['city']}")

# Multiline f-string
report = (
    f"Naam : {name}\n"
    f"Umar : {age}\n"
    f"CGPA : {cgpa:.2f}"
)
print("\nMultiline:")
print(report)
""")

C(r"""
# --- f-string format specs: ALIGNMENT aur WIDTH ---
# Shakal: {value:[[fill]align][sign][#][0][width][,][.precision][type]}
word = "Ali"

print(f"default (str left) : [{word:10}]")
print(f"left     '<'       : [{word:<10}]")
print(f"right    '>'       : [{word:>10}]")
print(f"center   '^'       : [{word:^10}]")
print(f"fill '*' + center  : [{word:*^10}]")
print(f"fill '.' + right   : [{word:.>10}]")
print(f"fill '-' + left    : [{word:-<10}]")

print("\n--- numbers default RIGHT align hote hain ---")
print(f"number default : [{42:10}]")
print(f"number left    : [{42:<10}]")
print(f"zero padded    : [{42:010}]")

print("\n--- Dynamic width (nested braces) ---")
for w in (6, 10, 14):
    print(f"width={w:<3} -> [{word:>{w}}]")

# Table banane ka asli use
print("\n--- Aligned table ---")
rows = [("Ali", 92, 3.85), ("Fatima", 88, 3.66), ("Abdul-Rehman", 79, 3.10)]
print(f"{'Naam':<15}{'Marks':>7}{'CGPA':>8}")
print("-" * 30)
for nm, mk, cg in rows:
    print(f"{nm:<15}{mk:>7}{cg:>8.2f}")
""")

C(r"""
# --- f-string format specs: NUMBERS ---
n, big, frac = 255, 1234567.891, 0.2567

print("--- precision ---")
print(f"{frac:.0f}  {frac:.1f}  {frac:.3f}  {frac:.6f}")
print(f"pi -> {3.14159265:.4f}")

print("\n--- thousands separator ---")
print(f"comma      : {big:,}")
print(f"comma+prec : {big:,.2f}")
print(f"underscore : {1234567:_}")

print("\n--- percent ---")
print(f"{frac:%}      <- default 6 decimals")
print(f"{frac:.1%}    <- 1 decimal")
print(f"{frac:.2%}")

print("\n--- sign ---")
for v in (42, -42):
    print(f"  default [{v:d}]  plus [{v:+d}]  space [{v: d}]")

print("\n--- zero padding + precision (width me point bhi ginta hai) ---")
print(f"{3.7:05.1f}   <- total width 5 ('003.7')")
print(f"{-3.7:07.2f}  <- sign bhi width me")

print("\n--- bases (sirf int par) ---")
print(f"binary  : {n:b}   | with prefix: {n:#b}")
print(f"octal   : {n:o}   | with prefix: {n:#o}")
print(f"hex     : {n:x}   | HEX: {n:X} | with prefix: {n:#x}")
print(f"padded binary (8 bits): {5:08b}")

print("\n--- scientific / general ---")
print(f"exponent 'e' : {big:e}  | 2 decimals: {big:.2e}")
print(f"general  'g'  : {0.000012345:g}  | {123456789.0:g}")
print(f"char     'c'  : {65:c} (ASCII 65)")

print("\n--- braces ko escape karna ---")
print(f"literal braces: {{{name}}}  <- {{ }} do baar likho")
print(f'JSON jaisa: {{"key": {n}}}')

# datetime formatting (deterministic date, taake output hamesha same rahe)
from datetime import datetime, date
fixed = datetime(2026, 7, 29, 14, 5, 9)
print("\n--- date/time specs ---")
print(f"ISO-ish  : {fixed:%Y-%m-%d %H:%M:%S}")
print(f"Padha hua: {fixed:%d %B %Y}")
print(f"Sirf din : {fixed:%A}")
""")

C(r"""
# --- str.format() ---
name, age = "Ayesha", 21

print("auto index    :", "{} ki umar {} hai".format(name, age))
print("explicit index:", "{0} ki umar {1} hai".format(name, age))
print("reuse index   :", "{0}, haan {0}!".format(name))
print("reorder       :", "{1} saal, naam {0}".format(name, age))
print("named         :", "{n} ki umar {a}".format(n=name, a=age))
print("dict unpack   :", "{n} / {a}".format(**{"n": name, "a": age}))

# Same format specs chalte hain (: ke baad)
print("\nspecs         :", "[{:>10}] [{:^10}] [{:<10.2f}]".format("hi", "mid", 3.14159))
print("comma         :", "{:,.2f}".format(1234567.891))

# Container access format string ke andar
data = {"user": {"name": "Ali"}, "scores": [90, 80]}
print("\nnested access :", "{0[user][name]} -> {0[scores][0]}".format(data))

# Braces escape
print("escape braces :", "{{literal}} aur {}".format("value"))

# builtin format() — ek hi value ke liye
print("\nformat(3.14159, '.2f') =", format(3.14159, ".2f"))
print("format(255, '#x')      =", format(255, "#x"))
print("format(0.25, '.1%')    =", format(0.25, ".1%"))

# Kab format() behtar hai: jab template pehle mile, values baad me
TEMPLATE = "Salam {name}, aap ka order #{order} tayyar hai."
for cust in ({"name": "Ali", "order": 101}, {"name": "Sara", "order": 102}):
    print(TEMPLATE.format(**cust))
""")

C(r"""
# --- % formatting (purana style, legacy code me milta hai) ---
name, age, cgpa = "Ayesha", 21, 3.7248

print("%s ki umar %d saal hai" % (name, age))
print("CGPA: %.2f" % cgpa)
print("Multiple: %s / %d / %.1f" % (name, age, cgpa))

print("\n--- conversion types ---")
print("%s -> str  :", "%s" % [1, 2])
print("%r -> repr :", "%r" % "text")
print("%d -> int  :", "%d" % 3.99, "(truncate karta hai)")
print("%f -> float:", "%f" % 3.5, "| %.3f ->", "%.3f" % 3.5)
print("%e -> sci  :", "%e" % 1234.5)
print("%x -> hex  :", "%x" % 255, "| %o ->", "%o" % 255)
print("%%  -> literal percent:", "100%% done" % ())

print("\n--- width / align ---")
print("right width 8 : [%8s]" % "ab")
print("left  width 8 : [%-8s]" % "ab")
print("zero pad      : [%05d]" % 42)
print("sign          : [%+d] [%+d]" % (42, -42))

print("\n--- dict style (%(name)s) ---")
print("%(n)s ki umar %(a)d" % {"n": name, "a": age})

print("\n--- GOTCHA: single tuple value ---")
point = (1, 2)
try:
    print("point = %s" % point)          # tuple ko arguments samjha -> "not all arguments converted"
except TypeError as e:
    print("TypeError:", e)
print("Hal 1 (comma):", "point = %s" % (point,))
print("Hal 2 (list) :", "point = %s" % [point])
print("Hal 3 (f-str):", f"point = {point}")
""")

C(r"""
# --- Teeno tareeqon ki speed (chhota benchmark) ---
import time

name, age = "Ayesha", 21
N = 100_000

def bench(label, fn):
    t0 = time.perf_counter()
    for _ in range(N):
        fn()
    return label, (time.perf_counter() - t0) * 1000

results = [
    bench("f-string      ", lambda: f"{name} is {age}"),
    bench("str.format()  ", lambda: "{} is {}".format(name, age)),
    bench("% formatting  ", lambda: "%s is %d" % (name, age)),
    bench("str +  concat ", lambda: name + " is " + str(age)),
]
results.sort(key=lambda r: r[1])

print(f"{N:,} iterations:")
fastest = results[0][1]
for label, ms in results:
    print(f"  {label} {ms:7.2f} ms   ({ms / fastest:.2f}x)")
print("\nNatija: f-string aam tor par sab se tez — aur parhne me bhi sab se saaf.")
print("Note: exact numbers machine par depend karte hain, tarteeb aam tor par yahi rehti hai.")
""")

M(r"""
---
## 13. Common Mistakes / Gotchas — ek jagah

| # | Ghalti | Kyun bura | Sahi tareeqa |
|---|---|---|---|
| 1 | `if x == None` | custom `__eq__` jhoot bol sakta hai | `if x is None` |
| 2 | `if x is 5` | small-int cache par bharosa | `if x == 5` |
| 3 | `0.1 + 0.2 == 0.3` | float approximation | `math.isclose(a, b)` |
| 4 | paisa `float` me | error jama hoti hai | `Decimal` ya integer paise |
| 5 | `round(2.5)` se 3 ki umeed | banker's rounding | `Decimal` + `ROUND_HALF_UP` |
| 6 | `"5" + 5` | Python strongly typed hai | `int("5") + 5` ya f-string |
| 7 | `a = b = []` mutable ke sath | ek hi object, do tag | `a, b = [], []` |
| 8 | `b = a` ko copy samajhna | alias banta hai | `a.copy()` / `deepcopy` |
| 9 | `-2 ** 2` se 4 ki umeed | `**` unary minus se strong | `(-2) ** 2` |
| 10 | `2 ** 3 ** 2` se 64 ki umeed | `**` right-associative | `(2 ** 3) ** 2` |
| 11 | `qty or 10` default ke liye | `0` bhi falsy hai | `10 if qty is None else qty` |
| 12 | `int('3.5')` | `int()` decimal string nahi leta | `int(float('3.5'))` |
| 13 | `bool("False")` se False ki umeed | non-empty string truthy | explicit check karo |
| 14 | `7 / 2` se 3 ki umeed | `/` float deta hai | `7 // 2` |
| 15 | `-7 // 2` se -3 ki umeed | Python floor karta hai | samjho ya `math.trunc` |
| 16 | `t[0] += [x]` tuple par | error ke bawajood mutation | `t[0].append(x)` |
| 17 | builtin shadow: `list = [1,2]` | `list()` khatam ho gaya | `items = [1,2]` |
| 18 | `x in big_list` loop me | O(n) har baar | `set(big_list)` bana lo |
""")

C(r"""
# --- Gotcha #17 ka nuqsan (builtin shadowing) — aur uska ilaj ---
list = [1, 2, 3]                     # builtin 'list' ko shadow kar diya (BURI harkat)
print("list variable:", list)

try:
    print(list("abc"))               # ab 'list' function nahi, list object hai
except TypeError as e:
    print("TypeError:", e, "-> builtin 'list' mar gaya!")

del list                             # naam hatao -> builtin wapas nazar aane laga
print("del ke baad, list('abc') =", list("abc"), "✔ theek ho gaya")

print("\nAam tor par shadow ho jane wale naam (in se bacho):")
risky = ["list", "dict", "set", "str", "int", "float", "type", "id", "sum",
         "min", "max", "len", "input", "next", "object", "bytes", "file", "hash"]
print("  " + ", ".join(risky))
print("Behtar naam: items, mapping, values, text, count, total, user_input ...")
""")

C(r"""
# --- Gotcha round-up: ek cell me sab 'phasne wali' baatein ---
checks = [
    ("0.1 + 0.2 == 0.3",           0.1 + 0.2 == 0.3,            False),
    ("round(2.5)",                 round(2.5),                  2),
    ("round(0.5)",                 round(0.5),                  0),
    ("7 / 2",                      7 / 2,                       3.5),
    ("-7 // 2",                    -7 // 2,                     -4),
    ("-7 % 2",                     -7 % 2,                      1),
    ("2 ** 3 ** 2",                2 ** 3 ** 2,                 512),
    ("-2 ** 2",                    -2 ** 2,                     -4),
    ("~5",                         ~5,                          -6),
    ("True + True",                True + True,                 2),
    ("bool('False')",              bool("False"),               True),
    ("1 == 1.0 == True",           1 == 1.0 == True,            True),
    ("type(1 and 2).__name__",     type(1 and 2).__name__,      "int"),
    ("0 or 'x'",                   0 or "x",                    "x"),
    ("not 1 in [1]",               not 1 in [1],                False),
    ("1 & 2 == 2",                 1 & 2 == 2,                  False),
    ("1 & (2 == 2)",               1 & (2 == 2),                1),
    ("int(-3.9)",                  int(-3.9),                   -3),
    ("len({1, True, 1.0})",        len({1, True, 1.0}),         1),
]
print(f"{'expression':<26} {'natija':<10} expected")
print("-" * 50)
for expr, got, expected in checks:
    mark = "✔" if got == expected and type(got) is type(expected) else "≈"
    print(f"{expr:<26} {repr(got):<10} {repr(expected)} {mark}")
    assert got == expected, f"{expr} ne {got!r} diya, {expected!r} chahiye tha"
print("\nSab assertions pass ✔  (agar koi tumhein hairan kare, upar wala section dobara parho)")
""")

M(r"""
---
## 14. Real-World Problems

Ab in sab concepts ko mila kar asli masle hal karte hain — waisa code jaisa job par likha jata hai.
""")

C(r"""
# =====================================================================
# Problem 1: Invoice generator — Decimal ke sath (paisa NEVER float me)
# =====================================================================
from decimal import Decimal, ROUND_HALF_UP

TAX_RATE = Decimal("0.17")            # 17% GST — string se banaya (float se NAHI)
PAISA = Decimal("0.01")               # rounding ka quantum

def money(d):
    '''Decimal ko 2 decimal places par half-up round karta hai.'''
    return d.quantize(PAISA, rounding=ROUND_HALF_UP)

# (item, qty, unit_price) — prices string me, taake exact rahen
cart = [
    ("Notebook A4",      3, "249.99"),
    ("Ball Pen (pack)",  2, "120.50"),
    ("Highlighter",      5,  "89.95"),
    ("Stapler",          2, "455.00"),
]

DISCOUNT_THRESHOLD = Decimal("2000")
DISCOUNT_RATE = Decimal("0.10")       # 2000 se upar 10% off

print("=" * 54)
print(f"{'ITEM':<20}{'QTY':>4}{'RATE':>11}{'AMOUNT':>13}")
print("=" * 54)

subtotal = Decimal("0")
for item, qty, rate_str in cart:
    rate = Decimal(rate_str)
    amount = money(rate * qty)        # exact zarb, phir round
    subtotal += amount
    print(f"{item:<20}{qty:>4}{rate:>11}{amount:>13,}")

discount = money(subtotal * DISCOUNT_RATE) if subtotal > DISCOUNT_THRESHOLD else Decimal("0.00")
taxable = subtotal - discount
tax = money(taxable * TAX_RATE)
total = money(taxable + tax)

print("-" * 54)
print(f"{'Subtotal':<35}{subtotal:>19,}")
print(f"{'Discount (10%)' if discount else 'Discount':<35}{-discount:>19,}")
print(f"{'Tax (17%)':<35}{tax:>19,}")
print("=" * 54)
print(f"{'TOTAL (PKR)':<35}{total:>19,}")
print("=" * 54)

# Float ke sath wahi hisaab — farq dekho
float_total = 0.0
for _, qty, rate_str in cart:
    float_total += float(rate_str) * qty
print(f"\nDecimal subtotal : {subtotal}")
print(f"float   subtotal : {float_total!r}  <- yahan chhoti error nazar aa rahi hai")
assert money(total) == total
""")

C(r"""
# =====================================================================
# Problem 2: Universal unit converter — casting + formatting ka mazboot use
# =====================================================================
# Har conversion: (naya unit, factor) — value * factor
CONVERSIONS = {
    ("km", "mile"):  ("mile", 0.621371),
    ("mile", "km"):  ("km",   1.609344),
    ("kg", "lb"):    ("lb",   2.2046226),
    ("lb", "kg"):    ("kg",   0.45359237),
    ("cm", "inch"):  ("inch", 0.3937008),
}

def convert(value, frm, to):
    '''Linear units convert karta hai; temperature alag se handle hoti hai.'''
    if frm == to:
        return float(value)
    # Temperature linear-factor se nahi chalti (offset hai)
    if (frm, to) == ("c", "f"):
        return value * 9 / 5 + 32
    if (frm, to) == ("f", "c"):
        return (value - 32) * 5 / 9
    if (frm, to) == ("c", "k"):
        return value + 273.15
    key = (frm, to)
    if key not in CONVERSIONS:                  # membership operator
        raise ValueError(f"'{frm}' se '{to}' ki conversion maloom nahi")
    _, factor = CONVERSIONS[key]
    return value * factor

jobs = [(5, "km", "mile"), (10, "mile", "km"), (70, "kg", "lb"),
        (30, "c", "f"), (98.6, "f", "c"), (25, "c", "k"), (12, "cm", "inch")]

print(f"{'INPUT':>12}  {'':2}  {'OUTPUT':>14}")
print("-" * 34)
for val, frm, to in jobs:
    out = convert(val, frm, to)
    print(f"{val:>8,.2f} {frm:<3} ->  {out:>10,.2f} {to}")

# Error handling
try:
    convert(1, "km", "kg")
except ValueError as e:
    print("\nValueError:", e)

# Round-trip test (float ke liye isclose, == nahi)
import math
back = convert(convert(5, "km", "mile"), "mile", "km")
print(f"\nRound-trip 5 km -> mile -> km = {back!r}")
print("== 5 ?", back == 5, "| isclose ?", math.isclose(back, 5, rel_tol=1e-6), "<- SAHI check")
assert math.isclose(back, 5, rel_tol=1e-6)
assert math.isclose(convert(30, "c", "f"), 86.0)
""")

C(r"""
# =====================================================================
# Problem 3: Human-readable file size — // % ** aur formatting ka mila-jula use
# =====================================================================
UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]

def human_size(num_bytes, binary=True):
    '''Bytes ko padhne layak shakal me badalta hai.
    binary=True -> 1 KB = 1024 B (Windows style), False -> 1000 B (SI style).'''
    if num_bytes < 0:
        raise ValueError("bytes negative nahi ho sakte")
    step = 1024 if binary else 1000
    if num_bytes < step:
        return f"{num_bytes} B"
    idx = 0
    size = float(num_bytes)
    while size >= step and idx < len(UNITS) - 1:   # while loop + comparison
        size /= step                               # true division
        idx += 1
    return f"{size:,.2f} {UNITS[idx]}"

samples = [0, 512, 1023, 1024, 1536, 1_048_576, 15_728_640, 3_221_225_472, 2 ** 50]
print(f"{'BYTES':>20}  {'BINARY (1024)':>15}  {'SI (1000)':>15}")
print("-" * 56)
for b in samples:
    print(f"{b:>20,}  {human_size(b):>15}  {human_size(b, binary=False):>15}")

# Bitwise se bhi ho sakta hai (shift = divide by 1024 == >> 10)
print("\nBitwise shortcut: 15,728,640 >> 20 =", 15_728_640 >> 20, "MB (integer, tez magar precision kam)")

assert human_size(0) == "0 B"
assert human_size(1024) == "1.00 KB"
assert human_size(1_048_576) == "1.00 MB"
assert human_size(1000, binary=False) == "1.00 KB"
try:
    human_size(-1)
except ValueError as e:
    print("negative -> ValueError:", e)
print("\nSab tests pass ✔")
""")

C(r"""
# =====================================================================
# Problem 4: Config loader — safe type coercion (casting + exceptions)
# =====================================================================
# Asli duniya me config (env vars, .ini, CLI args) hamesha STRING me aati hai.
RAW_CONFIG = {
    "app_name":    "BizeeApp",
    "port":        "8080",
    "debug":       "true",
    "timeout":     "2.5",
    "max_retries": "3",
    "workers":     "abc",        # kharab value
    "rate_limit":  "",           # khali
    "verbose":     "0",
}

TRUE_WORDS = {"true", "yes", "y", "1", "on"}
FALSE_WORDS = {"false", "no", "n", "0", "off"}

def to_bool(text):
    '''String ko bool me badalta hai — bool(text) NAHI use karte (wo sab kuch True kehta hai).'''
    t = text.strip().lower()
    if t in TRUE_WORDS:
        return True
    if t in FALSE_WORDS:
        return False
    raise ValueError(f"'{text}' ko bool nahi bana sakte")

def coerce(raw, key, caster, default=None):
    '''raw[key] ko caster se convert karta hai; fail hone par default deta hai.'''
    if key not in raw:
        return default
    text = raw[key]
    if not text.strip():                       # khali string -> default
        return default
    try:
        return caster(text)
    except (ValueError, TypeError) as e:       # ek hi except me kai types
        print(f"  ⚠ '{key}' = {text!r} invalid ({type(e).__name__}) -> default {default!r}")
        return default

print("Config parse ho rahi hai...")
config = {
    "app_name":    coerce(RAW_CONFIG, "app_name", str,     "MyApp"),
    "port":        coerce(RAW_CONFIG, "port",     int,     8000),
    "debug":       coerce(RAW_CONFIG, "debug",    to_bool, False),
    "timeout":     coerce(RAW_CONFIG, "timeout",  float,   5.0),
    "max_retries": coerce(RAW_CONFIG, "max_retries", int,  1),
    "workers":     coerce(RAW_CONFIG, "workers",  int,     4),      # 'abc' -> default
    "rate_limit":  coerce(RAW_CONFIG, "rate_limit", int,   100),    # khali -> default
    "verbose":     coerce(RAW_CONFIG, "verbose",  to_bool, True),   # '0' -> False
    "missing_key": coerce(RAW_CONFIG, "nope",     int,     -1),     # nahi hai -> default
}

print(f"\n{'KEY':<14}{'VALUE':<12}{'TYPE'}")
print("-" * 34)
for k, v in config.items():
    print(f"{k:<14}{repr(v):<12}{type(v).__name__}")

assert config["port"] == 8080 and isinstance(config["port"], int)
assert config["debug"] is True
assert config["verbose"] is False, "'0' ko False banna chahiye tha — bool('0') ka trap!"
assert config["workers"] == 4, "kharab value par default aana chahiye"
print("\nSab assertions pass ✔  (note: bool('0') True hota hai — isi liye to_bool likha)")
""")

C(r"""
# =====================================================================
# Problem 5: Marks statistics report — operators + formatting + booleans
# =====================================================================
students = [
    ("Ali Raza",       78, 85, 92),
    ("Fatima Noor",    95, 88, 91),
    ("Bilal Ahmed",    45, 52, 38),
    ("Sana Iqbal",     67, 71, 80),
    ("Usman Tariq",    88, 94, 79),
]
SUBJECTS = ("Math", "Physics", "CS")
PASS_MARK = 50

def grade(pct):
    '''Percentage ko grade me badalta hai (chained comparison ka khoobsurat use).'''
    if pct >= 90:  return "A+"
    if 80 <= pct < 90: return "A"
    if 70 <= pct < 80: return "B"
    if 60 <= pct < 70: return "C"
    if PASS_MARK <= pct < 60: return "D"
    return "F"

print(f"{'STUDENT':<15}{'MATH':>6}{'PHY':>6}{'CS':>6}{'TOTAL':>7}{'%':>8}{'GRADE':>7}{'STATUS':>9}")
print("=" * 64)

all_pct = []
for name, *marks in students:                      # starred unpacking!
    total = sum(marks)
    pct = total / (len(marks) * 100) * 100         # true division
    all_pct.append(pct)
    # sum of booleans idiom: kitne subjects pass hue
    passed_count = sum(m >= PASS_MARK for m in marks)
    status = "PASS" if passed_count == len(marks) else "FAIL"
    print(f"{name:<15}{marks[0]:>6}{marks[1]:>6}{marks[2]:>6}{total:>7}{pct:>7.2f}%{grade(pct):>7}{status:>9}")

print("-" * 64)
class_avg = sum(all_pct) / len(all_pct)
best = max(all_pct)
worst = min(all_pct)
print(f"{'CLASS AVERAGE':<15}{class_avg:>36.2f}%")
print(f"{'HIGHEST':<15}{best:>36.2f}%")
print(f"{'LOWEST':<15}{worst:>36.2f}%")
print(f"{'SPREAD':<15}{best - worst:>36.2f}%")
print(f"{'PASS RATE':<15}{sum(p >= PASS_MARK for p in all_pct) / len(all_pct):>36.1%}")

assert grade(95) == "A+" and grade(85) == "A" and grade(45) == "F"
assert isinstance(class_avg, float)
print("\nAssertions pass ✔")
""")

M(r"""
---
## 15. LeetCode Problems (Easy)

Is notebook ke concepts (modulo, comparison, string building, bitwise) seedha in do problems me
lagte hain. Dono **Easy** hain aur dono asli interviews me poochi jati hain.

| # | Title | Difficulty | Kaam aane wala concept |
|---|---|---|---|
| 412 | Fizz Buzz | Easy | `%`, `if/elif`, string building, `or` idiom |
| 231 | Power of Two | Easy | bitwise `&`, loops, `//` |
""")

M(r"""
### LC 412. Fizz Buzz — Easy

**Link:** https://leetcode.com/problems/fizz-buzz/

**Problem (Roman Urdu):** Ek integer `n` diya hai. `1` se `n` tak strings ki ek list banao jahan:
- number 3 aur 5 **dono** se divisible ho → `"FizzBuzz"`
- sirf 3 se divisible ho → `"Fizz"`
- sirf 5 se divisible ho → `"Buzz"`
- warna → number khud, string ki shakal me (`str(i)`)

**Approach 1 — modulo + if/elif (seedha):**
1. `1` se `n` tak loop chalao (`range(1, n + 1)`).
2. **Sab se pehle** `i % 15 == 0` check karo (ya `i % 3 == 0 and i % 5 == 0`).
   Ye tarteeb ahem hai — agar `i % 3` pehle check karo to 15 par sirf `"Fizz"` aayega. **Yahi is
   problem ka asli trap hai.**
3. Phir `i % 3`, phir `i % 5`, warna `str(i)`.

**Approach 2 — string concatenation (zyada scalable):**
Khali string se shuru karo, `3` par `"Fizz"` jodo, `5` par `"Buzz"` jodo. Aakhir me
`s or str(i)` — jo humne `or` operator wale section me seekha (khali string falsy hai).
Agar kal "7 par Bazz" ki requirement aaye to sirf ek line barhani paregi — `elif` ka jungle nahi.

**Time complexity:** O(n) — har number ek baar. (String banane ki lagat ko constant maan rahe hain.)
**Space complexity:** O(n) — output list me `n` strings. Output ko chhor kar auxiliary space O(1).
""")

C(r"""
# --- LC 412: Fizz Buzz ---

def fizz_buzz(n):
    '''Approach 1: modulo + if/elif. 15 ka check SAB SE PEHLE aana chahiye.'''
    result = []
    for i in range(1, n + 1):                 # 1 se n tak (n bhi shamil)
        if i % 15 == 0:                       # 3 aur 5 ka LCM = 15 -> pehle check
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))             # int ko str me cast karna LAZMI hai
    return result


def fizz_buzz_concat(n):
    '''Approach 2: string jodte jao. Naye rules add karna aasan.'''
    result = []
    for i in range(1, n + 1):
        s = ""                                # khali string se shuru
        if i % 3 == 0:
            s += "Fizz"
        if i % 5 == 0:                        # 'elif' NAHI -> 15 par dono jud jayenge
            s += "Buzz"
        result.append(s or str(i))            # khali string falsy -> str(i) chun lega
    return result


def fizz_buzz_rules(n, rules=((3, "Fizz"), (5, "Buzz"))):
    '''Approach 3: rules data-driven. Production code isi shakal me hota hai.'''
    out = []
    for i in range(1, n + 1):
        word = "".join(label for div, label in rules if i % div == 0)
        out.append(word or str(i))
    return out


# --- Tests ---
expected_15 = ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
               "11", "Fizz", "13", "14", "FizzBuzz"]

for fn in (fizz_buzz, fizz_buzz_concat, fizz_buzz_rules):
    assert fn(3) == ["1", "2", "Fizz"], fn.__name__
    assert fn(5) == ["1", "2", "Fizz", "4", "Buzz"], fn.__name__
    assert fn(15) == expected_15, fn.__name__
    assert fn(1) == ["1"], fn.__name__
    assert len(fn(100)) == 100, fn.__name__
    assert fn(15)[14] == "FizzBuzz", fn.__name__      # index 14 = number 15
    print(f"{fn.__name__:<18} ✔ saare tests pass")

print("\nn = 15 ka natija:")
print(" ".join(fizz_buzz(15)))

# 15 ka trap dikhao: agar tarteeb ghalat ho to kya hota hai
def fizz_buzz_buggy(n):
    '''GHALAT version — 3 ka check pehle, 15 ka baad me (ya bilkul nahi).'''
    out = []
    for i in range(1, n + 1):
        if i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        elif i % 15 == 0:      # yahan kabhi nahi pohnchega!
            out.append("FizzBuzz")
        else:
            out.append(str(i))
    return out

print("\nBuggy version, 15 par:", fizz_buzz_buggy(15)[14], "<- 'FizzBuzz' hona chahiye tha")
assert fizz_buzz_buggy(15)[14] == "Fizz"      # bug ka sabot
print("Sabaq: if/elif me KHAAS SE AAM ki tarteeb rakho.")
""")

M(r"""
### LC 231. Power of Two — Easy

**Link:** https://leetcode.com/problems/power-of-two/

**Problem (Roman Urdu):** Ek integer `n` diya hai. Batao ke `n` **2 ki koi power** hai ya nahi —
yani koi aisa `x` maujood hai jahan `n == 2**x`? (`n` negative ya zero bhi ho sakta hai.)

**Approach 1 — Brute force (division loop):**
1. `n <= 0` ho to foran `False` (2 ki koi power negative ya zero nahi hoti).
2. Jab tak `n` even hai, `n //= 2` karte jao.
3. Aakhir me agar `n == 1` bacha to haan, 2 ki power thi.
   - Misaal: `16 → 8 → 4 → 2 → 1` ✔ ; `12 → 6 → 3` ✘ (3 bacha)

**Time:** O(log n) — har step me n aadha hota hai. **Space:** O(1).

**Approach 2 — Bitwise (optimal, one-liner):**
Binary me 2 ki har power me **theek ek** `1` bit hota hai:
```
1  = 0001      2  = 0010      4  = 0100      8  = 1000
```
Aur `n - 1` us akele `1` ke neeche ke saare bits ko `1` kar deta hai, us `1` ko `0`:
```
   8 = 1000            12 = 1100
 8-1 = 0111          12-1 = 1011
 AND = 0000  ✔        AND = 1000  ✘ (zero nahi)
```
To formula: **`n > 0 and n & (n - 1) == 0`**

`n > 0` ki shart lazmi hai — warna `0` galat tor par `True` ban jata (`0 & -1 == 0`).

**Time:** O(1) — sirf ek subtraction aur ek AND. **Space:** O(1).

**Approach 3 — `bit_count()` (Python 3.10+):** `n > 0 and n.bit_count() == 1` — sab se
padhne-layak, kyunki seedha "ek hi 1 bit hai" keh raha hai.
""")

C(r"""
# --- LC 231: Power of Two ---

def is_power_of_two_loop(n):
    '''Approach 1: brute force. O(log n) time, O(1) space.'''
    if n <= 0:                       # 2 ki power hamesha positive hoti hai
        return False
    while n % 2 == 0:                # jab tak even hai, aadha karte jao
        n //= 2                      # floor division (/ nahi — warna float ban jayega)
    return n == 1                    # sirf 1 bacha to haan


def is_power_of_two(n):
    '''Approach 2: bitwise. O(1) time, O(1) space — interview ka expected jawab.'''
    # n > 0 ki shart zaroori: 0 & -1 == 0 hota hai, jo galat True de deta
    return n > 0 and n & (n - 1) == 0


def is_power_of_two_bitcount(n):
    '''Approach 3: 2 ki power = binary me theek ek '1' bit.'''
    return n > 0 and n.bit_count() == 1


def is_power_of_two_recursive(n):
    '''Bonus: recursion se (NB 07 me tafseel).'''
    if n < 1:
        return False
    if n == 1:
        return True
    if n % 2:                        # odd hai (aur 1 nahi) -> nahi
        return False
    return is_power_of_two_recursive(n // 2)


# --- Bit-level tashreeh ---
print(f"{'n':>6} {'n (binary)':>12} {'n-1 (binary)':>14} {'n & (n-1)':>10}  jawab")
print("-" * 58)
for n in (1, 2, 3, 4, 8, 12, 16, 31, 32, 64):
    print(f"{n:>6} {n:>12b} {n - 1:>14b} {n & (n - 1):>10}  {is_power_of_two(n)}")

# --- Tests: chaaron approach ek jaisa jawab dein ---
cases = [
    (1, True), (2, True), (4, True), (8, True), (16, True),
    (1024, True), (2 ** 30, True), (2 ** 62, True),
    (3, False), (5, False), (6, False), (12, False), (100, False),
    (0, False), (-1, False), (-2, False), (-16, False),
]
funcs = (is_power_of_two, is_power_of_two_loop, is_power_of_two_bitcount, is_power_of_two_recursive)
for fn in funcs:
    for n, expected in cases:
        got = fn(n)
        assert got == expected, f"{fn.__name__}({n}) ne {got} diya, {expected} chahiye tha"
    print(f"{fn.__name__:<28} ✔ {len(cases)} tests pass")

print("\nEdge cases jo log bhool jate hain: n = 0, aur negative n.")
print("  is_power_of_two(0)   =", is_power_of_two(0),  "(0 & -1 == 0 hai — is liye n > 0 lazmi)")
print("  is_power_of_two(-16) =", is_power_of_two(-16))
print("\nBonus: powers of two 1 se 1024 tak ->",
      [n for n in range(1, 1025) if is_power_of_two(n)])
""")

M(r"""
---
## 16. Interview Questions & Answers

**Q1. Python me variable kaise kaam karta hai — dabba (box) ya label?**
Label. Variable memory me pare object par lagaya gaya **naam** hai. `a = b` object copy nahi
karta, sirf doosra naam bana deta hai. Isi liye `id(a) == id(b)` hota hai.

**Q2. `is` aur `==` me farq?**
`==` **value** compare karta hai (`__eq__` call hota hai, jo class customize kar sakti hai).
`is` **identity** compare karta hai (`id()` barabar hai?). `None`, `True`, `False` aur sentinels
ke liye `is`, baqi sab ke liye `==`.

**Q3. `a = 256; b = 256; a is b` `True` kyun, magar 1000 ke sath `False`?**
CPython `-5` se `256` tak ke integers **pehle se bana kar cache** rakhta hai (small-int cache),
is liye wahi object reuse hota hai. 1000 har baar naya object banta hai (agar constant folding na
ho). Ye **implementation detail** hai — is par logic na banao.

**Q4. `0.1 + 0.2 == 0.3` `False` kyun hai?**
Float IEEE-754 binary me store hote hain; `0.1` aur `0.2` binary me exactly represent nahi ho
sakte. Natija `0.30000000000000004` banta hai. Hal: `math.isclose()`, ya paise ke liye `Decimal`.

**Q5. `round(2.5)` `2` kyun deta hai?**
Python **banker's rounding** (round half to even) karta hai — IEEE-754 standard. Ye statistical
bias kam karta hai. School wala half-up chahiye to `Decimal(...).quantize(..., ROUND_HALF_UP)`.

**Q6. `/` aur `//` me farq? `-7 // 2` kya hai?**
`/` true division hai — hamesha `float` (`7/2 = 3.5`). `//` floor division hai — `-inf` ki taraf
neeche jata hai, is liye `-7 // 2 = -4` (na ke -3). Aur `-7 % 2 = 1` (result ka sign divisor ka).

**Q7. `bool` aur `int` ka rishta?**
`bool` `int` ka **subclass** hai. `True == 1`, `False == 0`, `isinstance(True, int)` → `True`.
Isi liye `sum([True, False, True])` = 2 (counting idiom).

**Q8. Mutable aur immutable types kaun kaun se hain, aur farq kyun ahem hai?**
Immutable: `int, float, complex, bool, str, tuple, frozenset, bytes, None`.
Mutable: `list, dict, set, bytearray`. Farq ahem hai kyunki (a) sirf immutable (hashable) objects
`dict` key / `set` element ban sakte hain, (b) mutable default arguments bug banate hain,
(c) mutable arguments function ke andar se badal jate hain.

**Q9. `tuple` immutable hai to `t = ([1], 2); t[0].append(9)` kaise chal gaya?**
Tuple ki immutability **shallow** hai. Tuple guarantee deta hai ke "kaun se objects" andar hain,
ye nahi ke wo objects khud na badlein. Isi liye aisa tuple **hashable nahi** hota.

**Q10. `and` / `or` kya return karte hain?**
`bool` nahi — **operand** return karte hain. `a and b` → `a` falsy ho to `a`, warna `b`.
`a or b` → `a` truthy ho to `a`, warna `b`. Isi se `name = value or "default"` idiom banta hai —
magar khayal rakho: `0`, `""`, `[]` bhi falsy hain, to `is None` check zyada safe hai.

**Q11. Short-circuiting kya hai, faida kya?**
`and`/`or` zaroorat se zyada evaluate nahi karte. Faida: safety (`if user and user.name`),
aur performance (mehnga check baad me rakho).

**Q12. `2 ** 3 ** 2` kitna hai? `-2 ** 2`?**
`512` — `**` right-associative hai, yani `2 ** (3 ** 2)`.
`-4` — `**` unary minus se **zyada** precedence rakhta hai, yani `-(2 ** 2)`.

**Q13. Walrus operator kya hai, kab use karte hain?**
`:=` assignment expression hai (3.8+): assign karta hai aur value return bhi karta hai.
Use: `if (n := len(x)) > 10:`, `while (chunk := next(it, None)) is not None:`,
comprehension me `[y for x in xs if (y := f(x)) > 0]` — jahan dobara calculation se bachna ho.

**Q14. Python strongly typed hai ya weakly typed? Dynamically ya statically?**
**Dynamically typed** (type runtime par object ke sath hoti hai, declare nahi karte) aur
**strongly typed** (`"5" + 5` chup chaap kaam nahi karta, `TypeError` deta hai).
JavaScript dynamically **aur** weakly typed hai — wo `"5" + 5` ko `"55"` bana deta hai.

**Q15. `int` ki koi limit hai?**
Nahi. Python 3 ka `int` **arbitrary precision** hai — `2**10000` bhi theek chalta hai (sirf RAM
ki hadd). C/Java me 32/64-bit overflow hota hai. `float` par magar hadd hai (`sys.float_info.max`,
uske baad `inf`).

**Q16. `x += y` aur `x = x + y` me farq?**
Immutable ke liye koi practical farq nahi (dono naya object). **Mutable (list)** ke liye `+=`
`__iadd__` call karta hai → **in-place** mutation → doosre aliases bhi badalte hain.
`x = x + y` naya object banata hai → aliases purane object par rehte hain.
Aur `list += "ab"` chal jata hai (extend jaisa) jabke `list + "ab"` TypeError deta hai.

**Q17. String formatting ke 3 tareeqe, kaun sa behtar?**
f-string (3.6+) — sab se tez aur saaf, default choice. `str.format()` — jab template pehle mile
aur values baad me. `%` — legacy; magar `logging` me `logger.info("v=%s", v)` style behtar hai
kyunki string sirf zaroorat par banti hai (lazy).

**Q18. Paisa kis type me store karein?**
`Decimal` (string se banaya hua) ya integer **paise/cents**. `float` **kabhi nahi** — rounding
error har transaction par jama hoti hai.

**Q19. `bool("False")` kya deta hai?**
`True`! `bool()` string ki **khaali-pan** dekhta hai, uska matlab nahi. Sirf `""` falsy hai.
Isi liye config parsing me apna `to_bool()` likhna parta hai.

**Q20. `x = y = []` me kya masla hai?**
Dono naam **ek hi** list par lagte hain. `x.append(1)` ke baad `y` bhi `[1]` ho jayega.
Sahi tareeqa: `x, y = [], []`.
""")

M(r"""
---
## 17. Practice Exercises (khud karo)

Pehle khud likho, phir apna jawab test karo. Hints diye hain — magar pehle bina hint koshish karo.

**1. Swap without temp, teen variables ke sath.**
`a, b, c` ko aise rotate karo ke `a←c, b←a, c←b`. Ek line me.
*Hint:* right side pehle poora evaluate hota hai — tuple packing/unpacking.

**2. `to_number(text)`**
Function jo string ko `int` de agar poora integer ho, `float` de agar decimal ho, warna `None`.
`"42"` → `42` (int), `"3.5"` → `3.5` (float), `"abc"` → `None`.
*Hint:* pehle `int()` try karo, `ValueError` par `float()` try karo, phir `None`.

**3. `safe_divide(a, b)`**
Division karo magar `b == 0` par `None` do (crash nahi). Phir isi ka version banao jo
`float('inf')` de agar `a > 0` ho aur `-inf` agar `a < 0`.
*Hint:* `try/except ZeroDivisionError`, ya `if b else ...`.

**4. `count_bits(n)`**
Bina `bin()` aur bina `bit_count()` — sirf bitwise operators se ginno ke `n` me kitne `1` bits hain.
*Hint:* `while n: count += n & 1; n >>= 1` — ya tez tareeqa `n &= n - 1` (har baar ek 1 hatata hai).

**5. `is_leap(year)`**
Leap year check: 4 se divisible **aur** (100 se divisible nahi **ya** 400 se divisible).
Test: 2000 ✔, 1900 ✘, 2024 ✔, 2023 ✘.
*Hint:* `%`, `and`, `or` — aur brackets lagana na bhoolo.

**6. `format_money(amount)`**
Number ko `"Rs 1,234,567.89"` shakal me do. Negative par `"-Rs 1,234.50"` (minus pehle).
*Hint:* f-string `{abs(x):,.2f}` + sign alag se handle karo.

**7. `nearly_equal(a, b, tol=1e-9)`**
Do floats ko safely compare karo. Phir test karo ke `nearly_equal(0.1 + 0.2, 0.3)` `True` hai.
*Hint:* `abs(a - b) <= tol` — ya seedha `math.isclose` se compare kar ke dekho.

**8. `describe_number(n)`**
Ek string do jis me batao: even/odd, positive/negative/zero, power-of-two hai ya nahi, aur binary shakal.
Misaal: `describe_number(8)` → `"8: even, positive, power of two, 0b1000"`.
*Hint:* list me tukre jama karo phir `", ".join(parts)`.

**9. Permission checker.**
`READ=1, WRITE=2, EXEC=4`. Functions likho: `grant(perm, flag)`, `revoke(perm, flag)`,
`has(perm, flag)`, `toggle(perm, flag)` — sirf bitwise operators se.
*Hint:* `|` add, `& ~` remove, `&` check, `^` toggle.

**10. `truthiness_report(values)`**
List ke har item ke liye print karo: value, type, `bool()`, aur `len()` (agar mumkin ho).
`len()` na ho to `"-"` likho.
*Hint:* `try/except TypeError` ya `hasattr(v, '__len__')`.
""")

M(r"""
---
## 18. Summary / Cheat-Sheet

### Types
```python
int   -> 42, 1_000, 0b1010, 0o17, 0xFF        # arbitrary precision
float -> 3.14, 2e3, float('inf'), float('nan')  # IEEE-754, approximate
complex -> 3+4j        bool -> True/False (int ka subclass)
str -> "text"          None -> NoneType (singleton)
```

### Casting
```python
int("42")  int(3.9)->3  int("ff",16)  int(float("3.5"))
float("1e-3")   str(42)   bool("")->False   complex(2,5)
list("abc")  tuple([1,2])  set([1,1,2])  dict(zip(k, v))  ",".join(map(str, nums))
```

### Operators (precedence: upar se neeche = strong se weak)
```
()  ->  x[i]/f()  ->  **  ->  -x ~x  ->  * / // % @  ->  + -
->  << >>  ->  &  ->  ^  ->  |  ->  comparisons/in/is  ->  not  ->  and  ->  or  ->  if-else  ->  :=
```
```python
7 / 2  == 3.5      7 // 2 == 3       7 % 2 == 1      2 ** 10 == 1024
-7 // 2 == -4      -7 % 2 == 1       divmod(7,2) == (3,1)
2 ** 3 ** 2 == 512      -2 ** 2 == -4      ~5 == -6
5 & 3 == 1   5 | 3 == 7   5 ^ 3 == 6   5 << 1 == 10   5 >> 1 == 2
```

### Golden rules
```python
x is None                 # None ke liye 'is' (== nahi)
x == 5                    # values ke liye '==' ('is' nahi)
math.isclose(a, b)        # floats ke liye (== nahi)
Decimal("19.99")          # paise ke liye (float nahi)
10 if q is None else q    # default ke liye ('q or 10' nahi)
a, b = [], []             # do lists ke liye ('a = b = []' nahi)
x not in y                # ('not x in y' nahi)
```

### Falsy values (baqi sab truthy)
`0`, `0.0`, `0j`, `""`, `[]`, `()`, `{}`, `set()`, `range(0)`, `None`, `False`

### Mutable vs Immutable
| Immutable (hashable ✔) | Mutable (hashable ✘) |
|---|---|
| `int float complex bool str tuple frozenset bytes None range` | `list dict set bytearray` |

### f-string spec: `{value:[fill][align][sign][#][0][width][,][.prec][type]}`
```python
f"{x:>10}"    f"{x:<10}"    f"{x:^10}"    f"{x:*^10}"      # align + fill
f"{x:.2f}"    f"{x:,}"      f"{x:,.2f}"   f"{x:_}"          # precision + separators
f"{x:.1%}"    f"{x:+d}"     f"{x:05.2f}"  f"{x:e}"          # percent, sign, pad, sci
f"{x:b}" f"{x:o}" f"{x:x}" f"{x:#x}"      f"{65:c}"         # bases, char
f"{x!r}"      f"{x=}"       f"{x:>{w}}"   f"{{literal}}"    # repr, debug, dynamic, escape
f"{dt:%Y-%m-%d}"                                            # date
```

### Bitwise tricks
```python
n & 1 == 0                     # even?
n > 0 and n & (n-1) == 0       # power of two?
n & (n - 1)                    # sab se right wala 1 bit hatao
x ^= y; y ^= x; x ^= y         # XOR swap
reduce(xor, nums)              # akela number (LC 136)
perm |= FLAG  /  perm &= ~FLAG /  perm & FLAG  /  perm ^= FLAG   # set/clear/test/toggle
```

### Ye 6 baatein interview me sab se zyada aati hain
1. `is` vs `==` (+ small-int cache, interning)
2. `0.1 + 0.2 != 0.3` aur uska hal
3. mutable vs immutable (+ hashability)
4. `and`/`or` operand return karte hain (short-circuit)
5. `**` right-associative aur `-2**2 == -4`
6. `-7 // 2 == -4`, `-7 % 2 == 1` (Python vs C)

---

**Agla notebook:** `03_Strings_aur_String_Methods.ipynb` — slicing, saare string methods,
unicode/encode-decode, aur `+` vs `join` ki performance.
""")

# CHUNK_MARKER

save(r"Python/Basics/02_Variables_DataTypes_aur_Operators.ipynb", cells)
