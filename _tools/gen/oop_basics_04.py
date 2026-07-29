import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

cells = []

# ---------------------------------------------------------------------------
# 1. TITLE
# ---------------------------------------------------------------------------
cells.append(md(r"""
# 04 — Magic (Dunder) Methods, `@classmethod` aur `@staticmethod`

**Level:** Intermediate → Advanced (interview prep + university syllabus)

Ye OOP series ka chautha notebook hai. Ab tak humne classes banaye (01), data protect kiya (02),
aur hierarchy + polymorphism seekha (03). Ab hum apni classes ko **Python ke apne built-in
types jaisa** banayenge — yani `len(obj)`, `obj[0]`, `for x in obj`, `with obj:`, `obj()`,
`a + b`, `print(obj)` — sab kuch tumhari class par kaam karega.

Yehi cheez "Pythonic" code ki jaan hai, aur interview me sab se zyada impress karti hai.

## Is notebook me kya seekhenge (roadmap)

1. Dunder / magic methods kya hain aur Python inhein kaise call karta hai
2. `__new__` vs `__init__` — object asal me kahan banta hai (+ singleton, immutable subclass)
3. `__str__` vs `__repr__` — poora farq, `print` vs REPL vs container
4. `__format__` — f-string ka custom spec (`f"{obj:short}"`)
5. `__eq__` aur `__hash__` ka **contract** (dict/set me kya hota hai)
6. Ordering dunders + `functools.total_ordering`
7. Arithmetic dunders: `__add__`, `__radd__`, `__iadd__`, `__neg__`, `__abs__`, `__round__`
8. `__len__` aur `__bool__` — truthiness ka asli qanoon
9. Container protocol: `__getitem__`, `__setitem__`, `__delitem__`, `__contains__`
10. Iteration protocol: `__iter__`, `__next__`, generator wala shortcut, `__reversed__`
11. `__call__` — objects jo function ki tarah chalte hain
12. Attribute access: `__getattr__` vs `__getattribute__`, `__setattr__`, `__delattr__`
13. Context manager: `__enter__` / `__exit__` (+ `contextlib.contextmanager`)
14. `__slots__` ke sath dunders, `__copy__` / `__deepcopy__` ka zikr
15. `@classmethod` — `cls`, alternative constructors (factory pattern), inheritance-aware
16. `@staticmethod` — kab, kyun, aur module-level function se farq
17. Instance vs class vs static method — poora comparison table
18. `abc.ABC` + `@abstractmethod` — abstract class vs interface
19. `__init_subclass__` — plugin registry ka clean tareeqa (bonus)
20. `dataclasses` — dunders khud likhne se bachao
21. Common mistakes / gotchas
22. Real-world problems (Money, Matrix, LRU-ish cache, DB connection, CSV row set)
23. LeetCode: LC 155, LC 232, LC 225, LC 359 (asserts ke sath)
24. Interview Q&A (22 sawal)
25. Practice exercises + cheat-sheet

## Prerequisites

Notebook 01-03 (classes, `self`, encapsulation, `@property`, inheritance, `super()`, MRO).
"""))

# ---------------------------------------------------------------------------
# 2. DUNDER INTRO
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 1. Dunder / Magic methods kya hain?

**Dunder** = **d**ouble **under**score → `__name__`. Inhein "magic methods" bhi kehte hain,
magar magic kuch nahi — ye simple **protocol** hai:

> Jab tum `len(x)` likhte ho, Python `type(x).__len__(x)` chalata hai.

| Tum likhte ho | Python chalata hai |
|---|---|
| `str(x)`, `print(x)` | `type(x).__str__(x)` |
| `repr(x)` | `type(x).__repr__(x)` |
| `len(x)` | `type(x).__len__(x)` |
| `x[k]` | `type(x).__getitem__(x, k)` |
| `x + y` | `type(x).__add__(x, y)` |
| `x()` | `type(x).__call__(x)` |
| `for i in x` | `type(x).__iter__(x)` |
| `with x:` | `__enter__` / `__exit__` |
| `k in x` | `__contains__` (warna `__iter__`) |

**AHEM (interview point):** dunder lookup **type** par hota hai, **instance** par nahi.
Yani instance ke `__dict__` me `__len__` daal dene se `len()` kaam nahi karega!

**Naming rule:** apne khud ke `__myname__` mat banao — ye namespace Python ka reserved hai.
"""))

cells.append(code(r"""
# ---- Proof: dunder lookup TYPE par hota hai, instance par nahi -------------
class Bag:
    def __init__(self, items):
        self.items = list(items)

    def __len__(self):                      # len() ke liye
        return len(self.items)


b = Bag([1, 2, 3])
print("len(b) =", len(b))                   # 3 -> __len__ chala

# Instance par dunder daalne ki koshish
b.__len__ = lambda: 999                     # instance dict me daal diya
print("b.__len__() =", b.__len__())         # 999 (seedha call kiya to hamara lambda)
print("len(b) =", len(b))                   # PHIR BHI 3 -> Python ne type par dekha!

print("\ninstance dict:", list(b.__dict__))
print("type par __len__:", Bag.__len__)

assert len(b) == 3 and b.__len__() == 999
print("\n[ok] dunder lookup type par hota hai")
"""))

cells.append(code(r"""
# ---- Kitne dunders hote hain? ek nazar --------------------------------------
sample = [1, 2, 3]
dunders = [d for d in dir(sample) if d.startswith("__")]
print(f"list par {len(dunders)} dunders hain, kuch:")
print(" ", ", ".join(dunders[:14]))

# Har built-in operation ke peeche ek dunder hai
print("\n[1,2,3] + [4]  ->", sample.__add__([4]))         # yani + operator
print("len([1,2,3])    ->", sample.__len__())
print("2 in [1,2,3]    ->", sample.__contains__(2))
print("str([1,2,3])    ->", sample.__str__())
print("[1,2,3][0]      ->", sample.__getitem__(0))
"""))

# ---------------------------------------------------------------------------
# 3. __new__ vs __init__
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 2. `__new__` vs `__init__` — object banta kahan hai?

Object banne ke **2 marhale** hain:

1. **`__new__(cls, ...)`** — asal me memory allocate kar ke **naya object banata hai**.
   Ye implicitly **static method** hai (pehla parameter `cls`). Object **return** karta hai.
2. **`__init__(self, ...)`** — bane hue object ko **initialize** karta hai. `None` return karta
   hai (kuch aur return karo to `TypeError`).

```
Point(3, 4)
   ↓
type.__call__  →  Point.__new__(Point, 3, 4)  →  obj
                  Point.__init__(obj, 3, 4)   →  None
   ↓
returns obj
```

**`__new__` kab chahiye (99% waqt nahi chahiye):**

- **Immutable** types (`int`, `str`, `tuple`) ko subclass karte waqt — kyunke `__init__` me value
  set karne ke liye late ho chuka hota hai.
- **Singleton** / instance caching / object pooling.
- Metaclass-level tricks.

**Gotcha:** agar `__new__` `cls` ka instance **return na kare**, to `__init__` **chalega hi nahi**.
"""))

cells.append(code(r"""
# ---- dono marhalon ko print se dekho --------------------------------------
class Point:
    def __new__(cls, x, y):
        print(f"  1) __new__ chala   -> cls={cls.__name__}, args=({x}, {y})")
        obj = super().__new__(cls)          # asli object yahan bana (args pass NAHI karte)
        print(f"     object ban gaya  -> id={id(obj) % 100000}")
        return obj                          # return karna LAZMI

    def __init__(self, x, y):
        print(f"  2) __init__ chala  -> self ko values di")
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


print("Point(3, 4) likhne par:")
p = Point(3, 4)
print("natija:", p)

# ---- Agar __new__ galat cheez return kare -> __init__ SKIP -------------
class Weird:
    def __new__(cls):
        return "main string hoon"       # cls ka instance nahi!

    def __init__(self):
        print("ye kabhi nahi chalega")


w = Weird()
print("\nWeird() ne diya:", repr(w), "| type:", type(w).__name__)
assert isinstance(w, str)
print("[ok] __new__ / __init__ ka farq")
"""))

cells.append(code(r"""
# ---- Use-case 1: SINGLETON (ek hi instance) -------------------------------
class AppConfig:
    "Poore program me ek hi config object."
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)     # sirf pehli baar banao
            cls._instance._initialized = False
        return cls._instance                          # hamesha wahi object

    def __init__(self, env="dev"):
        if self._initialized:          # dobara initialize na karo
            return
        self.env = env
        self.settings = {}
        self._initialized = True


c1 = AppConfig("prod")
c2 = AppConfig("dev")                  # naya nahi bana!
print("c1 is c2 ?", c1 is c2)
print("env:", c2.env, "(pehli baar wali value bachi rahi)")
c1.settings["debug"] = True
print("c2 se bhi wahi settings:", c2.settings)

# ---- Use-case 2: immutable type ko subclass karna ----------------------
class PositiveInt(int):
    "int immutable hai -> value __new__ me set karni parti hai."

    def __new__(cls, value):
        if value <= 0:
            raise ValueError("sirf positive number")
        return super().__new__(cls, value)      # value yahan set hoti hai


class BadPositiveInt(int):
    def __init__(self, value):          # bohat der ho gayi — int already bana hua hai
        if value <= 0:
            raise ValueError("sirf positive")
        self.value = value              # ye int ki value nahi badalta


print("\nPositiveInt(5) + 10 =", PositiveInt(5) + 10)
try:
    PositiveInt(-3)
except ValueError as err:
    print("PositiveInt(-3) ->", err)

print("BadPositiveInt(-3) ->", BadPositiveInt(-3), "<- validation bekar (int pehle ban gaya)")

assert c1 is c2 and PositiveInt(5) == 5
print("\n[ok] __new__ use-cases")
"""))

# ---------------------------------------------------------------------------
# 4. __str__ vs __repr__
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 3. `__str__` vs `__repr__` — sab se zyada poocha jane wala sawal

| | `__repr__` | `__str__` |
|---|---|---|
| Maqsad | **developer** ke liye — unambiguous, debugging | **user** ke liye — readable |
| Kaun call karta | `repr()`, REPL, **containers** (list/dict ke andar), debugger | `str()`, `print()`, f-string, `format()` |
| Ideal shakal | `Point(3, 4)` — jise `eval()` kar sako | `(3, 4)` — jo user parh sake |
| Default (object se) | `<__main__.Point object at 0x...>` | `__repr__` ko call kar deta hai |

**Golden rules:**

- **Sirf ek** likhna ho to **`__repr__`** likho — `str()` khud usi par gir jaata hai (fallback).
- Ulta nahi hota: sirf `__str__` likhne se `repr()` default hi rehta hai.
- Container ke andar **hamesha `__repr__`** chalta hai — list print karo to `__str__` ignore.
- `__repr__` me `!r` use karo (`f"{self.name!r}"`) taake strings quotes ke sath dikhein.
"""))

cells.append(code(r"""
# ---- teen classes: sirf repr / sirf str / dono -----------------------------
class OnlyRepr:
    def __init__(self, n): self.n = n
    def __repr__(self): return f"OnlyRepr(n={self.n})"


class OnlyStr:
    def __init__(self, n): self.n = n
    def __str__(self): return f"main {self.n} hoon"


class Both:
    def __init__(self, n): self.n = n
    def __repr__(self): return f"Both(n={self.n})"        # developer
    def __str__(self): return f"Number {self.n}"          # user


for obj in (OnlyRepr(1), OnlyStr(2), Both(3)):
    print(f"{type(obj).__name__:<9} str()={str(obj):<28} repr()={repr(obj)}")

print("\nContainer ke andar (yahan HAMESHA repr chalta hai):")
print([OnlyRepr(1), OnlyStr(2), Both(3)])
print({"key": Both(3)})

print("\nf-string str use karta hai:", f"{Both(9)}")
print("f-string me !r se repr:", f"{Both(9)!r}")

# Sabaq: OnlyStr ka repr default (bekar) reh gaya -> list me kuch samajh nahi aata
assert repr(OnlyRepr(1)) == str(OnlyRepr(1))       # str -> repr par fallback
assert "object at" in repr(OnlyStr(2))             # default repr
print("\n[ok] str vs repr")
"""))

cells.append(code(r"""
# ---- __format__: f-string ke custom spec ---------------------------------
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __repr__(self):
        return f"Temperature({self.celsius})"

    def __str__(self):
        return f"{self.celsius}°C"

    def __format__(self, spec):
        # spec wahi hai jo f"{obj:SPEC}" me colon ke baad likha ho
        if spec == "" or spec == "c":
            return f"{self.celsius:.1f}°C"
        if spec == "f":
            return f"{self.celsius * 9 / 5 + 32:.1f}°F"
        if spec == "k":
            return f"{self.celsius + 273.15:.2f}K"
        if spec == "short":
            return f"{round(self.celsius)}C"
        # anjaan spec ko number ki tarah handle karo (e.g. ".3f")
        return format(self.celsius, spec)


t = Temperature(36.6667)
print("default :", f"{t}")            # __format__ ("" spec)
print("celsius :", f"{t:c}")
print("fahren. :", f"{t:f}")
print("kelvin  :", f"{t:k}")
print("short   :", f"{t:short}")
print("numeric :", f"{t:.3f}")        # fallback -> number formatting
print("str()   :", str(t))            # __str__ (format se alag ho sakta hai)
print("repr()  :", repr(t))

assert f"{t:short}" == "37C"
assert f"{t:f}".endswith("°F")
print("\n[ok] __format__")
"""))

# ---------------------------------------------------------------------------
# 5. __eq__ / __hash__
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 4. `__eq__` aur `__hash__` ka contract (bohat ahem)

**Default behaviour:** `object.__eq__` identity (`is`) check karta hai, aur `__hash__` = `id()`
par based hota hai. Yani do alag objects same data ke sath bhi barabar nahi hote.

**Contract (rattna zaroori hai):**

1. `a == b` ho to `hash(a) == hash(b)` **lazmi** hona chahiye.
2. Ulta zaroori nahi (`hash` same magar equal nahi = collision, allowed hai).
3. `__eq__` define karo → Python `__hash__` ko **`None`** kar deta hai → object **unhashable**
   (set/dict key me nahi ja sakega). Solution: `__hash__` khud define karo.
4. Hash **immutable** cheezon par based ho — mutable field par hash banaya to dict me object
   "kho" jayega.
5. `__ne__` khud ban jaata hai (`__eq__` ka ulta) — likhne ki zaroorat nahi.

**Interview line:** *"`__eq__` value semantics deta hai; `__hash__` ke baghair object
hash-based collections me use nahi ho sakta, aur mutable state par hash banana bug hai."*
"""))

cells.append(code(r"""
# ---- Step 1: bina __eq__ -> sirf identity ---------------------------------
class P0:
    def __init__(self, x, y): self.x, self.y = x, y


print("bina __eq__:", P0(1, 2) == P0(1, 2))       # False — different objects

# ---- Step 2: __eq__ diya -> unhashable ho gaya --------------------------
class P1:
    def __init__(self, x, y): self.x, self.y = x, y
    def __eq__(self, other):
        if not isinstance(other, P1):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)


print("__eq__ ke sath:", P1(1, 2) == P1(1, 2))    # True
print("__ne__ mufat  :", P1(1, 2) != P1(3, 4))    # True
print("P1.__hash__ ab:", P1.__hash__)             # None!
try:
    {P1(1, 2)}
except TypeError as err:
    print("set me daalne par TypeError:", err)

# ---- Step 3: __hash__ bhi do -> sab theek ------------------------------
class P2:
    def __init__(self, x, y): self.x, self.y = x, y
    def __repr__(self): return f"P2({self.x}, {self.y})"
    def __eq__(self, other):
        return isinstance(other, P2) and (self.x, self.y) == (other.x, other.y)
    def __hash__(self):
        return hash((self.x, self.y))      # SAME fields jo __eq__ me hain


s = {P2(1, 2), P2(1, 2), P2(3, 4)}
print("\nset me duplicates khatam:", s)
d = {P2(0, 0): "origin"}
print("dict lookup naye object se:", d[P2(0, 0)])

assert len(s) == 2 and hash(P2(1, 2)) == hash(P2(1, 2))
print("[ok] eq + hash contract")
"""))

cells.append(code(r"""
# ---- GOTCHA: mutable field par hash -> object dict me "kho" jata hai -----
class MutableKey:
    def __init__(self, name): self.name = name
    def __repr__(self): return f"MutableKey({self.name!r})"
    def __eq__(self, o): return isinstance(o, MutableKey) and self.name == o.name
    def __hash__(self): return hash(self.name)     # KHATARNAAK: name badal sakta hai


k = MutableKey("ali")
registry = {k: "student record"}
print("pehle mila:", registry.get(k))

k.name = "ALI"                          # hash badal gaya, bucket purana hi hai
print("naam badalne ke baad:", registry.get(k), "<- object kho gaya!")
print("magar dict me phir bhi maujood hai:", list(registry.items()))
print("Poori dict me dhoondo:", [v for kk, v in registry.items() if kk is k])

print("\nFIX ke tareeqe:")
print("  1) hash sirf IMMUTABLE / never-changing fields par (jaise id)")
print("  2) object ko frozen banao (__setattr__ rok do ya dataclass(frozen=True))")
print("  3) mutable objects ko dict key hi na banao")

# frozen dataclass ka demo (hash mufat + immutability)
from dataclasses import dataclass

@dataclass(frozen=True)
class FrozenKey:
    name: str


fk = FrozenKey("ali")
print("\nfrozen dataclass hash:", isinstance(hash(fk), int))
try:
    fk.name = "ALI"
except Exception as err:
    print("badalne ki koshish ->", type(err).__name__, ":", err)
print("[ok] hash gotcha")
"""))

# ---------------------------------------------------------------------------
# 6. Ordering + arithmetic
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 5. Ordering aur Arithmetic dunders

**Comparison:** `__lt__` (`<`), `__le__` (`<=`), `__gt__` (`>`), `__ge__` (`>=`), `__eq__`, `__ne__`.
`sorted()`, `min()`, `max()`, `heapq`, `bisect` — sab sirf **`__lt__`** par chalte hain.

**Arithmetic:**

| Operator | Normal | Reflected (dayen taraf) | In-place (`+=`) |
|---|---|---|---|
| `+` | `__add__` | `__radd__` | `__iadd__` |
| `-` | `__sub__` | `__rsub__` | `__isub__` |
| `*` | `__mul__` | `__rmul__` | `__imul__` |
| `/` | `__truediv__` | `__rtruediv__` | `__itruediv__` |
| `//` | `__floordiv__` | `__rfloordiv__` | `__ifloordiv__` |

Aur unary: `__neg__` (`-x`), `__pos__`, `__abs__`, `__round__`, `__invert__`.

**Reflected kab chalta hai:** `5 * money` me pehle `int.__mul__(5, money)` try hota hai →
`NotImplemented` → phir Python `money.__rmul__(5)` chalata hai. Is liye `sum()` ke liye
`__radd__` chahiye hota hai (kyunke `sum` `0 + obj` se shuru karta hai).

**In-place gotcha:** `__iadd__` na ho to `x += y` `x = x + y` ban jaata hai (naya object).
Mutable containers ke liye `__iadd__` define karna performance ke liye behtar hai.
"""))

cells.append(code(r"""
from functools import total_ordering

@total_ordering
class Version:
    "Semantic version — sorting, comparison, aur arithmetic ka demo."

    def __init__(self, text):
        self.parts = tuple(int(x) for x in text.split("."))

    def __repr__(self):
        return "v" + ".".join(map(str, self.parts))

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self.parts == other.parts

    def __lt__(self, other):               # sirf ye + __eq__ -> total_ordering baqi bana dega
        if not isinstance(other, Version):
            return NotImplemented
        return self.parts < other.parts

    def __hash__(self):
        return hash(self.parts)


vs = [Version("1.2.10"), Version("1.10.0"), Version("1.2.3")]
print("sorted    :", sorted(vs))                    # __lt__ se
print("max       :", max(vs))
print("1.2.10 > 1.2.3 ?", Version("1.2.10") > Version("1.2.3"))   # total_ordering
print("1.2.3 <= 1.2.3 ?", Version("1.2.3") <= Version("1.2.3"))
print("set       :", {Version("1.0.0"), Version("1.0.0")})

# total_ordering ne kaun kaun se methods bana diye?
made = [m for m in ("__le__", "__gt__", "__ge__") if m in Version.__dict__]
print("\ntotal_ordering ne diye:", made)

assert sorted(vs)[0] == Version("1.2.3")
assert Version("1.10.0") > Version("1.2.10")        # 10 > 2 (numeric, string nahi)
print("[ok] ordering")
"""))

cells.append(code(r"""
# ---- arithmetic: normal, reflected, in-place, unary -----------------------
class Cash:
    "PKR amount — poora numeric protocol."

    def __init__(self, amount):
        self.amount = amount

    def __repr__(self):
        return f"Cash({self.amount})"

    # --- normal ---
    def __add__(self, other):
        print(f"    __add__ chala ({self!r} + {other!r})")
        if isinstance(other, Cash):
            return Cash(self.amount + other.amount)
        if isinstance(other, (int, float)):
            return Cash(self.amount + other)
        return NotImplemented

    def __sub__(self, other):
        o = other.amount if isinstance(other, Cash) else other
        return Cash(self.amount - o)

    def __mul__(self, k):
        if not isinstance(k, (int, float)):
            return NotImplemented
        return Cash(self.amount * k)

    # --- reflected: jab hum operator ke DAYEN taraf hon ---
    def __radd__(self, other):
        print(f"    __radd__ chala ({other!r} + {self!r})")
        return self.__add__(other)          # addition commutative hai

    def __rmul__(self, k):
        return self.__mul__(k)              # 3 * cash

    # --- unary ---
    def __neg__(self):
        return Cash(-self.amount)

    def __abs__(self):
        return Cash(abs(self.amount))

    def __round__(self, n=0):
        return Cash(round(self.amount, n))

    def __eq__(self, other):
        return isinstance(other, Cash) and self.amount == other.amount


a, b = Cash(100), Cash(250)
print("Cash + Cash:")
print("  =", a + b)
print("Cash + int:")
print("  =", a + 50)
print("int + Cash (reflected):")
print("  =", 50 + a)                        # int.__add__ fail -> __radd__
print("\n3 * cash (rmul):", 3 * a)
print("-cash          :", -a)
print("abs(-cash)     :", abs(Cash(-99)))
print("round          :", round(Cash(12.3456), 2))

# sum() ko __radd__ chahiye hota hai (0 + Cash se shuru)
print("\nsum([...]) ka natija:", sum([Cash(10), Cash(20), Cash(30)]))

assert (a + b) == Cash(350) and (50 + a) == Cash(150)
assert sum([Cash(1), Cash(2)]) == Cash(3)
print("[ok] arithmetic dunders")
"""))

cells.append(code(r"""
# ---- __iadd__ ka farq: naya object vs mutate ----------------------------
class Basket:
    "Bina __iadd__ — += naya object banata hai."
    def __init__(self, items): self.items = list(items)
    def __add__(self, other): return Basket(self.items + other.items)
    def __repr__(self): return f"Basket({self.items})"


class BasketFast:
    "__iadd__ ke sath — += usi object ko mutate karta hai (efficient)."
    def __init__(self, items): self.items = list(items)
    def __add__(self, other): return BasketFast(self.items + other.items)
    def __iadd__(self, other):
        self.items.extend(other.items)      # in-place
        return self                         # return karna LAZMI
    def __repr__(self): return f"BasketFast({self.items})"


b1 = Basket([1]); before = id(b1)
b1 += Basket([2])
print("Basket     : same object?", id(b1) == before, "->", b1)

b2 = BasketFast([1]); before2 = id(b2)
b2 += BasketFast([2])
print("BasketFast : same object?", id(b2) == before2, "->", b2)

# Gotcha: shared reference ke sath __iadd__ ka asar dusri jagah bhi dikhega
x = BasketFast([1]); y = x
x += BasketFast([9])
print("\ny bhi badal gaya (same object):", y)

assert b1.items == [1, 2] and b2.items == [1, 2] and y.items == [1, 9]
print("[ok] __iadd__")
"""))

# ---------------------------------------------------------------------------
# 7. __len__ / __bool__
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 6. `__len__` aur `__bool__` — truthiness ka asli qanoon

`if obj:` likhne par Python ye tarteeb follow karta hai:

1. `__bool__` maujood hai? → wahi use karo (`True`/`False` return karna lazmi)
2. Warna `__len__` maujood hai? → `len(obj) != 0`
3. Warna → object **hamesha `True`** (default)

**Gotchas:**

- `__len__` ne 0 diya to object **falsy** ho jayega — kabhi kabhi ye ghalat hota hai
  (jaise khali `Order` object jise phir bhi valid samajhna ho) → `__bool__` explicitly do.
- `__len__` ko **non-negative int** return karna hoga, warna `ValueError`/`TypeError`.
- `if obj is not None:` aur `if obj:` bilkul **different** cheezein hain — khali container
  `None` nahi hota magar falsy hota hai. Ye bug bohat aam hai.
"""))

cells.append(code(r"""
# ---- teen surtein ----------------------------------------------------------
class NoDunders:
    pass


class WithLen:
    def __init__(self, n): self.n = n
    def __len__(self): return self.n


class WithBoth:
    "Khali hone par bhi 'valid' object — __bool__ ne __len__ ko override kiya."
    def __init__(self, n): self.n = n
    def __len__(self): return self.n
    def __bool__(self): return True          # hamesha truthy


print("NoDunders()      truthy?", bool(NoDunders()))     # True (default)
print("WithLen(0)       truthy?", bool(WithLen(0)))      # False (len se)
print("WithLen(3)       truthy?", bool(WithLen(3)))      # True
print("WithBoth(0)      truthy?", bool(WithBoth(0)), "<- __bool__ ki jeet")
print("len(WithBoth(0)) =", len(WithBoth(0)))

# ---- asli duniya ka bug ------------------------------------------------
class Cart:
    def __init__(self, items=None): self.items = items or []
    def __len__(self): return len(self.items)


def process_bad(cart):
    if not cart:                      # BUG: khali cart ko "cart hi nahi" samjha
        return "koi cart nahi mila"
    return f"{len(cart)} items process hue"


def process_good(cart):
    if cart is None:                  # SAHI: existence ka check
        return "koi cart nahi mila"
    if len(cart) == 0:                # khali hone ka ALAG check
        return "cart khali hai"
    return f"{len(cart)} items process hue"


print("\nkhali cart -> bad :", process_bad(Cart()))
print("khali cart -> good:", process_good(Cart()))
print("None       -> good:", process_good(None))

# ---- __len__ galat value de to error ----------------------------------
class BadLen:
    def __len__(self): return -1


try:
    len(BadLen())
except ValueError as err:
    print("\nlen() ne -1 diya ->", type(err).__name__, ":", err)

assert bool(WithBoth(0)) is True and bool(WithLen(0)) is False
print("[ok] len / bool")
"""))

# ---------------------------------------------------------------------------
# 8. CONTAINER PROTOCOL
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 7. Container protocol — apni class ko list/dict jaisa banao

| Tum likhte ho | Dunder |
|---|---|
| `obj[k]` | `__getitem__(self, k)` |
| `obj[k] = v` | `__setitem__(self, k, v)` |
| `del obj[k]` | `__delitem__(self, k)` |
| `k in obj` | `__contains__(self, k)` (na ho to `__iter__` se linear search) |
| `len(obj)` | `__len__` |
| `obj[1:3]` | `__getitem__` me `slice` object aata hai |

**Ahem baatein:**

- `__getitem__` **akela** bhi iteration de deta hai (purana protocol: `0, 1, 2...` tak
  `IndexError` — magar `__iter__` behtar hai).
- Negative index aur `slice` **khud** handle karna parta hai (Python automatic nahi karta).
- Galat key par `KeyError`, galat index par `IndexError` phenkna chahiye — is se `dict`/`list`
  jaisa behaviour milta hai aur `for` loops sahi rukte hain.
- Shortcut: `collections.abc.Sequence` / `MutableMapping` se inherit karo → bohat se methods
  (`index`, `count`, `get`, `keys`, `items`, `pop`) **mufat** mil jaate hain.
"""))

cells.append(code(r"""
# ---- Apna Playlist: getitem/setitem/delitem/contains/len + slicing --------
class Playlist:
    def __init__(self, songs=()):
        self._songs = list(songs)

    def __len__(self):
        return len(self._songs)

    def __getitem__(self, index):
        # slice bhi aa sakta hai -> naya Playlist wapis do (list nahi)
        if isinstance(index, slice):
            return Playlist(self._songs[index])
        return self._songs[index]              # negative index list khud sambhal legi

    def __setitem__(self, index, value):
        self._songs[index] = value

    def __delitem__(self, index):
        del self._songs[index]

    def __contains__(self, song):
        # case-insensitive membership — apna custom rule
        return song.lower() in (s.lower() for s in self._songs)

    def __repr__(self):
        return f"Playlist({self._songs})"


pl = Playlist(["Dil Dil Pakistan", "Sayonee", "Aadat", "Bol Hu"])
print("len       :", len(pl))
print("pl[0]     :", pl[0])
print("pl[-1]    :", pl[-1])                 # negative index
print("pl[1:3]   :", pl[1:3], "<- slice ne Playlist diya")
print("'sayonee' in pl:", "sayonee" in pl)   # custom case-insensitive
print("'xyz' in pl    :", "xyz" in pl)

pl[0] = "Hum Dekhenge"                       # __setitem__
del pl[1]                                    # __delitem__
print("badalne ke baad:", pl)

# __getitem__ hone se for loop bhi chal jata hai (legacy protocol)
print("iteration:", [s[:4] for s in pl])

try:
    pl[99]
except IndexError as err:
    print("\npl[99] ->", type(err).__name__, ":", err)

assert len(pl) == 3 and pl[0] == "Hum Dekhenge"
assert isinstance(pl[0:2], Playlist)
print("[ok] container protocol")
"""))

cells.append(code(r"""
from collections.abc import MutableMapping

# ---- ABC se mufat methods: CaseInsensitiveDict ---------------------------
class CaseInsensitiveDict(MutableMapping):
    "5 dunders do, ~15 methods mufat milte hain (get/keys/items/pop/update...)."

    def __init__(self, data=None):
        self._store = {}
        if data:
            self.update(data)          # ye method ABC se mila!

    def __setitem__(self, k, v):
        self._store[k.lower()] = (k, v)      # original naam bhi yaad rakha

    def __getitem__(self, k):
        return self._store[k.lower()][1]

    def __delitem__(self, k):
        del self._store[k.lower()]

    def __iter__(self):
        return (orig for orig, _ in self._store.values())

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return f"CaseInsensitiveDict({dict(self.items())})"


headers = CaseInsensitiveDict({"Content-Type": "application/json"})
headers["ACCEPT"] = "text/html"

print("repr        :", headers)
print("lower se    :", headers["content-type"])
print("upper se    :", headers["CONTENT-TYPE"])
print("get()       :", headers.get("accept"), "(ABC se mufat)")
print("keys()      :", list(headers.keys()))
print("items()     :", list(headers.items()))
print("'Accept' in :", "Accept" in headers)
print("pop()       :", headers.pop("accept"), "| len ab:", len(headers))

# Mufat methods ki list
free = [m for m in ("get", "keys", "items", "values", "pop", "setdefault", "update", "clear")
        if hasattr(headers, m)]
print("\nMufat mile methods:", free)

assert headers["Content-Type"] == "application/json"
assert len(headers) == 1
print("[ok] MutableMapping ABC")
"""))

# ---------------------------------------------------------------------------
# 9. ITERATION
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 8. Iteration protocol — `__iter__` aur `__next__`

- **Iterable** = jis par `iter()` chal sake (`__iter__` hai). Misaal: `list`, `str`, `dict`.
- **Iterator** = jis par `next()` chal sake (`__next__` **aur** `__iter__` dono hain).
  Khatam hone par `StopIteration` raise karta hai.

`for x in obj:` asal me ye karta hai:

```python
it = iter(obj)          # obj.__iter__()
while True:
    try:    x = next(it)    # it.__next__()
    except StopIteration: break
```

**Design faisla:**

| Tareeqa | Kab |
|---|---|
| `__iter__` me **generator** (`yield`) return karo | 95% cases — sab se aasan |
| `__iter__` naya **iterator object** de | Jab multiple independent passes chahiye |
| Class khud iterator ho (`__iter__` `return self`) | Sirf ek-baar-chalne wale streams |

**Sab se bara gotcha:** agar class khud iterator ho (`return self`) to woh **ek hi baar**
chalegi — doosri `for` loop khali nikle gi (exhausted).
"""))

cells.append(code(r"""
# ---- Tareeqa 1: generator (behtareen) — har baar naya pass ---------------
class Fib:
    "Pehle n Fibonacci numbers — reusable iterable."

    def __init__(self, n): self.n = n

    def __iter__(self):
        a, b = 0, 1
        for _ in range(self.n):
            yield a                     # generator = iterator khud ban jata hai
            a, b = b, a + b


f = Fib(8)
print("pehla pass :", list(f))
print("doosra pass:", list(f), "<- dobara chal gaya (reusable)")
print("unpacking  :", [*Fib(4)])
print("max/sum    :", max(Fib(8)), sum(Fib(8)))

# ---- Tareeqa 2: class khud iterator (ek hi baar chalega) --------------
class Countdown:
    def __init__(self, start): self.current = start
    def __iter__(self): return self              # KHUD iterator hai
    def __next__(self):
        if self.current <= 0:
            raise StopIteration                  # khatam ka signal
        self.current -= 1
        return self.current + 1


cd = Countdown(3)
print("\npehla pass :", list(cd))
print("doosra pass:", list(cd), "<- KHALI! (exhausted) — classic gotcha")

# Manual next()
cd2 = Countdown(2)
print("\nnext():", next(cd2), next(cd2))
try:
    next(cd2)
except StopIteration:
    print("StopIteration -> iteration mukammal")

# ---- __reversed__ + lazy infinite iterator ------------------------
class NumberRange:
    def __init__(self, lo, hi): self.lo, self.hi = lo, hi
    def __iter__(self): return iter(range(self.lo, self.hi))
    def __reversed__(self): return iter(range(self.hi - 1, self.lo - 1, -1))
    def __len__(self): return self.hi - self.lo


nr = NumberRange(1, 6)
print("\nseedha :", list(nr))
print("ulta   :", list(reversed(nr)))          # __reversed__ se

import itertools
class Naturals:
    "Infinite iterable — lazy hone ka faida."
    def __iter__(self):
        i = 1
        while True:
            yield i
            i += 1


print("infinite se pehle 5:", list(itertools.islice(Naturals(), 5)))

assert list(Fib(6)) == [0, 1, 1, 2, 3, 5]
assert list(cd) == [] and list(reversed(nr)) == [5, 4, 3, 2, 1]
print("[ok] iteration protocol")
"""))

# ---------------------------------------------------------------------------
# 10. __call__
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 9. `__call__` — object jo function ki tarah chale

`__call__` define karne se object **callable** ban jata hai: `obj(args)`.

**Kyun (function se behtar kab):**

- **State ke sath function** — counters, caches, rate-limiters, accumulators.
- **Configurable function** (parametrized): `Multiplier(3)` phir `triple(10)`.
- **Class-based decorators**.
- Function bhi asal me object hai — `def f(): ...` ka `type(f).__call__` maujood hai.

`callable(x)` check karta hai ke `type(x)` me `__call__` hai ya nahi. Classes khud callable
hain — `MyClass()` asal me `type.__call__` hai (jo `__new__` + `__init__` chalata hai).
"""))

cells.append(code(r"""
# ---- 1) Configurable function ---------------------------------------------
class Multiplier:
    def __init__(self, factor): self.factor = factor
    def __call__(self, x): return x * self.factor
    def __repr__(self): return f"Multiplier({self.factor})"


triple = Multiplier(3)
print("triple(10) =", triple(10))
print("map ke sath:", list(map(triple, [1, 2, 3])))       # normal function ki jagah chal gaya
print("callable?", callable(triple))

# ---- 2) State-ful counter (closure ka clean alternative) --------------
class CallCounter:
    "Kitni baar call hua — state object me, global me nahi."
    def __init__(self, fn):
        self.fn, self.count = fn, 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.fn(*args, **kwargs)


@CallCounter                 # class-based decorator!
def greet(name):
    return f"Salam {name}"


print("\n", greet("Ali"))
print(greet("Sara"))
print("greet kitni baar chala?", greet.count)

# ---- 3) Memoizing callable (LeetCode/DP me bohat kaam aata hai) -----
class Memoized:
    def __init__(self, fn):
        self.fn, self.cache, self.hits, self.misses = fn, {}, 0, 0

    def __call__(self, *args):
        if args in self.cache:
            self.hits += 1
            return self.cache[args]
        self.misses += 1
        self.cache[args] = self.fn(*args)
        return self.cache[args]

    def stats(self):
        return f"hits={self.hits} misses={self.misses} cached={len(self.cache)}"


@Memoized
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print("\nfib(30) =", fib(30))
print("stats:", fib.stats(), "<- cache ke baghair ~1.6 million calls hote")

assert triple(10) == 30 and greet.count == 2
assert fib(30) == 832040 and fib.hits > 0
print("[ok] __call__")
"""))

# ---------------------------------------------------------------------------
# 11. ATTRIBUTE ACCESS
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 10. Attribute access dunders

| Dunder | Kab chalta hai |
|---|---|
| `__getattribute__` | **HAR** attribute access par (pehle) |
| `__getattr__` | Sirf jab normal lookup **fail** ho jaye (fallback) |
| `__setattr__` | Har assignment (`obj.x = v`) par |
| `__delattr__` | `del obj.x` par |
| `__dir__` | `dir(obj)` par |

**Rules:**

- **`__getattr__`** safe hai aur aam use hota hai (lazy loading, proxies, dict-jaisa access).
- **`__getattribute__`** override karna khatarnaak hai — har access par chalta hai, aur andar
  `self.x` likha to **infinite recursion**. Hamesha `super().__getattribute__(name)` use karo.
- `__setattr__` ke andar `self.x = v` bhi recursion hai → `super().__setattr__(...)` ya
  `self.__dict__[...]` use karo.
- `__getattr__` ko missing attribute par **`AttributeError`** raise karna chahiye (warna
  `hasattr`, `copy`, `pickle` waghera toot jaate hain).
"""))

cells.append(code(r"""
# ---- __getattr__: dict ko attribute ki tarah access karo -----------------
class Config:
    "JSON/dict ko obj.key.key style me parho."

    def __init__(self, data):
        self._data = dict(data)

    def __getattr__(self, name):
        # SIRF tab chalta hai jab normal lookup fail ho
        if name.startswith("_"):
            raise AttributeError(name)          # internals ko chhero mat
        try:
            val = self._data[name]
        except KeyError:
            raise AttributeError(f"'{name}' config me nahi hai") from None
        return Config(val) if isinstance(val, dict) else val    # nested support

    def __dir__(self):
        return sorted(self._data)               # tab-completion ke liye


cfg = Config({"db": {"host": "localhost", "port": 5432}, "debug": True})
print("cfg.debug      :", cfg.debug)
print("cfg.db.host    :", cfg.db.host)           # nested — __getattr__ recursive
print("cfg.db.port    :", cfg.db.port)
print("dir(cfg)       :", dir(cfg))
try:
    cfg.missing
except AttributeError as err:
    print("cfg.missing    ->", err)
print("hasattr(cfg,'x'):", hasattr(cfg, "x"), "(AttributeError sahi raise hua)")

# ---- __setattr__: read-only / validating object ------------------------
class Frozen:
    "Ek baar set, phir badla nahi ja sakta."

    def __init__(self, **kw):
        for k, v in kw.items():
            self.__dict__[k] = v         # __setattr__ bypass (warna neeche wala rok deta)
        self.__dict__["_locked"] = True

    def __setattr__(self, name, value):
        if getattr(self, "_locked", False):
            raise AttributeError(f"'{name}' badla nahi ja sakta — object frozen hai")
        super().__setattr__(name, value)         # RECURSION se bachne ka sahi tareeqa

    def __delattr__(self, name):
        raise AttributeError("frozen object se kuch delete nahi hota")


fr = Frozen(host="db.local", port=5432)
print("\nfr.host:", fr.host)
for action, fn in (("set", lambda: setattr(fr, "host", "x")),
                   ("del", lambda: delattr(fr, "host"))):
    try:
        fn()
    except AttributeError as err:
        print(f"{action} ->", err)

assert cfg.db.host == "localhost" and not hasattr(cfg, "nope")
print("[ok] attribute dunders")
"""))

cells.append(code(r"""
# ---- __getattribute__ ka khatra: infinite recursion --------------------
class LoggedAccess:
    "Har attribute read ko log karo — sahi tareeqe se."

    def __init__(self, **kw):
        self.__dict__["_log"] = []
        self.__dict__.update(kw)

    def __getattribute__(self, name):
        # AGAR yahan `self._log` likhein to phir __getattribute__ chalega -> RECURSION
        if not name.startswith("_"):
            log = super().__getattribute__("_log")     # SAHI tareeqa
            log.append(name)
        return super().__getattribute__(name)


la = LoggedAccess(x=1, y=2)
print("padha:", la.x, la.y, la.x)
print("access log:", la._log)

# Galat version ka demo (recursion se bacha kar dikhaya)
class BrokenAccess:
    def __init__(self): self.__dict__["n"] = 0
    def __getattribute__(self, name):
        _ = self.tracker        # BUG: ye READ khud __getattribute__ ko phir bulayega
        return super().__getattribute__(name)


try:
    BrokenAccess().n
except RecursionError as err:
    print("\nRecursionError:", str(err)[:60], "...")

print("\nSabaq: __getattribute__ ke andar hamesha super().__getattribute__() se kaam lo.")
assert la._log.count("x") == 2
print("[ok] __getattribute__")
"""))

# ---------------------------------------------------------------------------
# 12. CONTEXT MANAGER
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 11. Context manager — `__enter__` / `__exit__`

`with` statement resource ko **guarantee** ke sath band karta hai (exception aaye ya na aaye).

```python
with Thing() as t:      # t = Thing().__enter__()
    body()
                        # Thing().__exit__(exc_type, exc_value, traceback)
```

**`__exit__` ke 3 arguments:** exception ka type, value, traceback. Agar koi exception nahi
to teenon `None`.

**Return value ka jadoo:**

- `__exit__` **`True`** return kare → exception **daba** diya jayega (suppress).
- `False`/`None` → exception aage barhta rahega (**normal aur behtar** default).

**Shortcut:** `contextlib.contextmanager` decorator se generator hi context manager ban jata hai
(`yield` se pehle setup, baad me cleanup — `try/finally` me).
"""))

cells.append(code(r"""
import time, tempfile, pathlib

# ---- Class-based context manager -----------------------------------------
class Timer:
    "Block kitni der chala — aur exception ho to bata do."

    def __init__(self, label="block"):
        self.label = label

    def __enter__(self):
        self.start = time.perf_counter()
        print(f"[{self.label}] shuru")
        return self                       # `as t` me yehi milega

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        status = "kamyab" if exc_type is None else f"FAIL ({exc_type.__name__})"
        print(f"[{self.label}] khatam — {self.elapsed*1000:.2f} ms, {status}")
        return False                      # exception ko dabao mat


with Timer("hisaab") as t:
    total = sum(i * i for i in range(100_000))
print("total:", total, "| elapsed maujood:", hasattr(t, "elapsed"))

print()
# Exception ke sath bhi __exit__ chalta hai (cleanup guarantee)
try:
    with Timer("error wala"):
        raise ValueError("kuch toot gaya")
except ValueError as err:
    print("bahar pakra gaya:", err)


# ---- __exit__ True return kare -> exception dab jata hai --------------
class Suppress:
    def __init__(self, *exc_types): self.exc_types = exc_types
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.exc_types):
            print(f"  ({exc_type.__name__} dabaya gaya)")
            return True                   # SUPPRESS
        return False


print()
with Suppress(ZeroDivisionError):
    1 / 0                                  # program crash nahi hua
print("code chalta raha")
print("[ok] context managers (class based)")
"""))

cells.append(code(r"""
from contextlib import contextmanager, suppress

# ---- generator-based context manager (aksar sab se saaf) ----------------
@contextmanager
def temp_csv(rows, headers=("id", "name")):
    "Temp CSV banao, path do, aakhir me khud saaf kar do (Windows-safe)."
    tmpdir = tempfile.mkdtemp()
    path = pathlib.Path(tmpdir) / "data.csv"
    try:
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(",".join(headers) + "\n")
            for r in rows:
                fh.write(",".join(map(str, r)) + "\n")
        print("setup: file bani ->", path.name)
        yield path                       # <- `as path` yahan milta hai
    finally:
        # cleanup HAMESHA chalega (exception me bhi)
        for p in pathlib.Path(tmpdir).iterdir():
            p.unlink()
        pathlib.Path(tmpdir).rmdir()
        print("cleanup: temp folder delete")


with temp_csv([(1, "Ali"), (2, "Sara")]) as csv_path:
    print("padha:", csv_path.read_text(encoding="utf-8").strip().splitlines())
    existed = csv_path.exists()

print("file abhi maujood?", csv_path.exists(), "(cleanup ho gaya)")

# ---- stdlib ka suppress + kai context managers ek sath -------------
with suppress(FileNotFoundError):
    open("aisi-file-nahi-hai.txt")        # error dab gaya
print("\nsuppress ke baad code chal raha hai")

import io
with Timer("multi") as tm, io.StringIO() as buf:      # ek hi with me 2 managers
    buf.write("dono managers ek sath")
    print("buffer:", buf.getvalue())

assert existed and not csv_path.exists()
print("[ok] contextlib")
"""))

cells.append(md(r"""
## 12. `__copy__` / `__deepcopy__` aur `__slots__` ke sath dunders (chhota tour)

- `copy.copy(obj)` → **shallow** copy (andar ke objects share hote hain) → `__copy__`
- `copy.deepcopy(obj)` → **deep** copy (sab kuch naya) → `__deepcopy__`
- `__slots__` (notebook 02 se) → `__dict__` khatam, memory kam, typo par error.
  **Gotcha:** slots ke sath `__weakref__` aur dynamic attributes chali jaati hain, aur
  subclass me slots dobara declare na karo (warna faida khatam).
"""))

cells.append(code(r"""
import copy

class Team:
    def __init__(self, name, members):
        self.name, self.members = name, list(members)

    def __repr__(self):
        return f"Team({self.name!r}, {self.members})"

    def __copy__(self):
        # shallow: members list SHARE hogi
        print("  __copy__ chala")
        new = type(self)(self.name, self.members)
        new.members = self.members          # jaan boojh kar share
        return new

    def __deepcopy__(self, memo):
        print("  __deepcopy__ chala")
        return type(self)(self.name, copy.deepcopy(self.members, memo))


orig = Team("Dev", ["Ali", "Sara"])
sh = copy.copy(orig)
dp = copy.deepcopy(orig)

sh.members.append("Bilal")                # shallow copy me daala
print("orig:", orig, "<- shallow copy ne isay bhi badla")
dp.members.append("Kashif")
print("orig:", orig, "<- deep copy ne kuch nahi bigara")

# ---- __slots__ + dunders ---------------------------------------------
class SlimPoint:
    __slots__ = ("x", "y")               # koi __dict__ nahi

    def __init__(self, x, y): self.x, self.y = x, y
    def __repr__(self): return f"SlimPoint({self.x}, {self.y})"
    def __eq__(self, o): return isinstance(o, SlimPoint) and (self.x, self.y) == (o.x, o.y)
    def __hash__(self): return hash((self.x, self.y))


sp = SlimPoint(1, 2)
print("\nslots object:", sp, "| hash ok:", isinstance(hash(sp), int))
print("__dict__ hai?", hasattr(sp, "__dict__"))
try:
    sp.z = 5                              # typo protection
except AttributeError as err:
    print("naya attribute ->", type(err).__name__, ":", err)

assert orig.members == ["Ali", "Sara", "Bilal"] and "Kashif" not in orig.members
print("[ok] copy + slots")
"""))

# ---------------------------------------------------------------------------
# 13. CLASSMETHOD / STATICMETHOD
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 13. `@classmethod` — `cls` ke sath kaam

**Kya hai:** Method jo **instance ki jagah class** par bind hoti hai. Pehla parameter `cls`
(class khud) hota hai, `self` nahi.

**Kyun (2 asli use-cases):**

1. **Alternative constructors / factories** — `Date.from_string("2026-07-29")`,
   `dict.fromkeys(...)`, `datetime.now()`.
2. **Class-level state** ke sath kaam — counters, registries, class config badalna.

**Sab se bara faida (interview point):** `cls` **inheritance-aware** hota hai. Factory me
`cls(...)` likho to subclass par call karne se **subclass ka object** banta hai — hard-coded
class name se ye nahi hota.

```python
@classmethod
def from_string(cls, text):
    return cls(...)          # NOT MyClass(...) — warna subclass toot jayega
```
"""))

cells.append(code(r"""
# ---- Alternative constructors (factory pattern) ---------------------------
class Duration:
    "Seconds ko kai tareeqon se banao."

    def __init__(self, seconds):
        self.seconds = int(seconds)

    # --- factories: sab `cls` use karti hain ---
    @classmethod
    def from_minutes(cls, mins):
        return cls(mins * 60)

    @classmethod
    def from_hours(cls, hours):
        return cls(hours * 3600)

    @classmethod
    def from_string(cls, text):
        "'1:30:00' ya '30:00' ya '45' parse karo."
        parts = [int(p) for p in text.split(":")]
        total = 0
        for p in parts:                  # sexagesimal
            total = total * 60 + p
        return cls(total)

    @classmethod
    def zero(cls):
        return cls(0)

    def __repr__(self):
        h, rem = divmod(self.seconds, 3600)
        m, s = divmod(rem, 60)
        return f"{type(self).__name__}({h:02d}:{m:02d}:{s:02d})"

    def __eq__(self, o):
        return isinstance(o, Duration) and self.seconds == o.seconds


print("seedha        :", Duration(90))
print("from_minutes  :", Duration.from_minutes(90))
print("from_hours    :", Duration.from_hours(2))
print("from_string   :", Duration.from_string("1:30:00"))
print("zero          :", Duration.zero())

# ---- `cls` ka jadoo: subclass par factory sahi class deti hai ---------
class Workout(Duration):
    "Subclass ne koi factory dobara nahi likhi — sab inherit ho gayi."
    def calories(self):
        return self.seconds * 0.15


w = Workout.from_minutes(45)             # <- Workout ka object bana, Duration ka nahi!
print("\nWorkout.from_minutes(45):", w, "| type:", type(w).__name__)
print("calories:", w.calories())

# ---- Ulta: hard-coded class name -> subclass toot gaya ---------------
class BadDuration:
    def __init__(self, seconds): self.seconds = seconds

    @classmethod
    def from_minutes(cls, mins):
        return BadDuration(mins * 60)    # GALTI: cls ki jagah naam likh diya


class BadWorkout(BadDuration):
    def calories(self): return self.seconds * 0.15


bw = BadWorkout.from_minutes(45)
print("\nBadWorkout.from_minutes ->", type(bw).__name__, "<- subclass nahi mila!")
print("calories() milega?", hasattr(bw, "calories"))

assert isinstance(w, Workout) and w.seconds == 2700
assert type(bw) is BadDuration
print("\n[ok] classmethod factories")
"""))

cells.append(code(r"""
# ---- classmethod se class-level state manage karna ----------------------
class Employee:
    _count = 0                        # class state
    _id_prefix = "EMP"

    def __init__(self, name):
        type(self)._count += 1        # `type(self)` — subclass-safe
        self.name = name
        self.emp_id = f"{self._id_prefix}-{self._count:03d}"

    @classmethod
    def total_employees(cls):
        return cls._count             # class-level data padha

    @classmethod
    def reset_counter(cls):
        cls._count = 0                # class-level data badla
        return cls._count

    @classmethod
    def set_prefix(cls, prefix):
        cls._id_prefix = prefix       # config change (subclass par alag ho sakta hai)

    def __repr__(self):
        return f"{self.emp_id}:{self.name}"


for nm in ("Ali", "Sara", "Bilal"):
    Employee(nm)
print("total:", Employee.total_employees())
print("instance se bhi chalta hai:", Employee("Kashif").total_employees())

Employee.set_prefix("BIZEE")
print("naye prefix ke sath:", Employee("Nadia"))
print("reset ke baad:", Employee.reset_counter())
assert Employee.total_employees() == 0
print("[ok] classmethod + class state")
"""))

cells.append(md(r"""
## 14. `@staticmethod` — na `self`, na `cls`

**Kya hai:** Class ke andar rakha hua **normal function** — koi automatic pehla argument nahi.

**Kyun class me rakhein (module function ki jagah):**

- **Namespacing / cohesion** — helper logically usi class se ta'aluq rakhta hai (`Date.is_leap_year`).
- **Discoverability** — `Date.` type karne par IDE me nazar aa jata hai.
- **Inheritance se milta hai** aur subclass **override** kar sakti hai (polymorphism possible).

**Kab na use karein:** agar function ko class ki koi cheez chahiye hi nahi aur kahin aur bhi
kaam aata hai → simple module-level function behtar hai.

### Teenon ka comparison (interview table)

| | Instance method | `@classmethod` | `@staticmethod` |
|---|---|---|---|
| Pehla arg | `self` (object) | `cls` (class) | kuch nahi |
| Instance data | ✅ | ❌ | ❌ |
| Class data | ✅ (via `self.__class__`) | ✅ | ❌ (sirf hard-coded naam se) |
| Instance se call | ✅ `obj.m()` | ✅ `obj.m()` | ✅ `obj.m()` |
| Class se call | ⚠️ `C.m(obj)` | ✅ `C.m()` | ✅ `C.m()` |
| Aam use | object ka kaam | factories, class state | utility helpers |
| Inheritance-aware | ✅ | ✅ (`cls`) | ✅ (override ho sakta) |
"""))

cells.append(code(r"""
# ---- teenon ek hi class me ------------------------------------------------
class Circle2:
    PI = 3.141592653589793

    def __init__(self, radius):
        self.radius = self.validate_radius(radius)      # static helper ka use

    # 1) INSTANCE method — object ka data chahiye
    def area(self):
        return self.PI * self.radius ** 2

    # 2) CLASSMETHOD — alternative constructor
    @classmethod
    def from_diameter(cls, d):
        return cls(d / 2)

    @classmethod
    def from_area(cls, area):
        return cls((area / cls.PI) ** 0.5)

    # 3) STATICMETHOD — na self na cls, sirf utility
    @staticmethod
    def validate_radius(r):
        if not isinstance(r, (int, float)) or isinstance(r, bool):
            raise TypeError("radius number hona chahiye")
        if r <= 0:
            raise ValueError("radius positive hona chahiye")
        return float(r)

    @staticmethod
    def circumference_of(r):
        return 2 * Circle2.PI * r         # static me class ka naam likhna parta hai

    def __repr__(self):
        return f"{type(self).__name__}(r={self.radius:g})"


c = Circle2(3)
print("instance method :", round(c.area(), 2))
print("classmethod     :", Circle2.from_diameter(10))
print("classmethod     :", Circle2.from_area(50.265))
print("staticmethod    :", round(Circle2.circumference_of(3), 2))
print("static instance se bhi:", c.validate_radius(7))

for bad in (-1, "abc", True):
    try:
        Circle2(bad)
    except (TypeError, ValueError) as err:
        print(f"Circle2({bad!r}) -> {type(err).__name__}: {err}")

# ---- Andar se kya hote hain? (descriptor protocol ki jhalak) ---------
print("\nclass par types:")
print("  area      :", type(Circle2.__dict__["area"]).__name__)
print("  from_area :", type(Circle2.__dict__["from_area"]).__name__)
print("  validate  :", type(Circle2.__dict__["validate_radius"]).__name__)
print("bound hone ke baad:")
print("  c.area    :", type(c.area).__name__)
print("  c.validate:", type(c.validate_radius).__name__, "<- plain function")

assert isinstance(Circle2.from_diameter(10), Circle2)
assert Circle2.validate_radius(2) == 2.0
print("\n[ok] instance vs class vs static")
"""))

cells.append(code(r"""
# ---- staticmethod bhi override ho sakta hai (polymorphic utility) --------
class Validator:
    @staticmethod
    def clean(text):
        return text.strip()

    @classmethod
    def process(cls, text):
        return cls.clean(text)         # `cls.` se subclass ka version milega


class UpperValidator(Validator):
    @staticmethod
    def clean(text):                   # static override
        return text.strip().upper()


class SlugValidator(Validator):
    @staticmethod
    def clean(text):
        return "-".join(text.strip().lower().split())


for klass in (Validator, UpperValidator, SlugValidator):
    print(f"{klass.__name__:<16} ->", repr(klass.process("  Hello Pakistan  ")))

assert UpperValidator.process(" hi ") == "HI"
assert SlugValidator.process(" Hello Pakistan ") == "hello-pakistan"
print("[ok] static override + template method")
"""))

# ---------------------------------------------------------------------------
# 14. ABC
# ---------------------------------------------------------------------------
cells.append(md(r"""
## 15. Abstract Base Classes (`abc`) — abstract class vs interface

**Masla:** `NotImplementedError` (notebook 03) sirf **method call** par pakra jata hai — bohat
der ho chuki hoti hai. `abc` object **banane hi nahi** deta.

```python
from abc import ABC, abstractmethod

class Repo(ABC):
    @abstractmethod
    def save(self, item): ...
```

| | Abstract class | Interface (Java/C#) |
|---|---|---|
| Implementation de sakti? | ✅ (concrete + abstract dono) | ❌ (sirf signature) |
| State/attributes? | ✅ | ❌ |
| Kitni inherit ho sakti? | Python me kai (multiple inheritance) | kai |
| Python me | `abc.ABC` + `@abstractmethod` | `abc` ya `typing.Protocol` |

**Baatein:**

- `@abstractmethod` ko `@property`, `@classmethod`, `@staticmethod` ke sath mila sakte ho
  (`@abstractmethod` **sab se andar/neeche** likho).
- Abstract class me **concrete** methods bhi ho sakti hain (template method pattern).
- `typing.Protocol` = **structural** typing (duck typing ka type-checked version) — inheritance
  ki zaroorat nahi.
- `register()` se koi bhi class "virtual subclass" ban sakti hai (isinstance True, inheritance nahi).
"""))

cells.append(code(r"""
from abc import ABC, abstractmethod

class Repository(ABC):
    "Abstract: contract + kuch concrete helpers (template method pattern)."

    @abstractmethod
    def save(self, item):
        "Item store karo, id wapis do."

    @abstractmethod
    def get(self, item_id):
        "Id se item lao."

    @property
    @abstractmethod
    def name(self):                     # abstract PROPERTY (decorators ki tarteeb dhyan se)
        "Repo ka naam."

    # --- concrete: sab subclasses ko mufat ---
    def save_many(self, items):
        return [self.save(i) for i in items]

    def describe(self):
        return f"<{self.name} repository>"


# 1) Adhoori class -> object hi nahi banega
class BrokenRepo(Repository):
    def save(self, item):
        return 1                        # get() aur name reh gaye


try:
    BrokenRepo()
except TypeError as err:
    print("TypeError:", err)

# 2) Poori implementation
class MemoryRepo(Repository):
    def __init__(self):
        self._data, self._next = {}, 1

    def save(self, item):
        item_id, self._next = self._next, self._next + 1
        self._data[item_id] = item
        return item_id

    def get(self, item_id):
        if item_id not in self._data:
            raise KeyError(f"id {item_id} nahi mili")
        return self._data[item_id]

    @property
    def name(self):
        return "in-memory"


repo = MemoryRepo()
ids = repo.save_many(["Ali", "Sara", "Bilal"])       # concrete method (mufat)
print("\n", repo.describe(), "| ids:", ids)
print("get(2):", repo.get(2))
print("abstract methods:", sorted(Repository.__abstractmethods__))

assert ids == [1, 2, 3] and repo.get(1) == "Ali"
print("[ok] abc")
"""))

cells.append(code(r"""
from typing import Protocol, runtime_checkable

# ---- Protocol: structural typing (duck typing + type checking) -----------
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...           # sirf shape, inheritance ki zaroorat nahi


class Button:                            # Drawable se inherit NAHI kiya
    def draw(self): return "[ Button ]"


class Icon:
    def draw(self): return "( Icon )"


class Label:
    def render(self): return "Label"      # draw nahi hai


def render_all(widgets):
    out = []
    for w in widgets:
        if isinstance(w, Drawable):       # runtime_checkable ki wajah se chala
            out.append(w.draw())
        else:
            out.append(f"<{type(w).__name__} draw nahi kar sakta>")
    return out


print("\n".join(render_all([Button(), Icon(), Label()])))
print("\nButton Drawable ka subclass?", issubclass(Button, Drawable), "(structural!)")

# ---- ABC.register: virtual subclass ------------------------------------
from collections.abc import Sized

class MyBox:
    def __len__(self): return 5


Sized.register(MyBox)                     # koi inheritance nahi, phir bhi...
print("MyBox Sized hai?", isinstance(MyBox(), Sized))
print("MyBox ke bases:", MyBox.__bases__)

assert isinstance(Button(), Drawable) and not isinstance(Label(), Drawable)
print("[ok] Protocol + register")
"""))

cells.append(md(r"""
## 16. `__init_subclass__` aur `dataclasses` — kaam bachane wale tools

**`__init_subclass__(cls, **kwargs)`:** jab bhi **koi subclass define** hoti hai ye chalta hai
(implicitly `classmethod`). Metaclass likhne ki zaroorat ke baghair plugin registry, validation,
ya required-attribute enforcement ho jaata hai.

**`dataclasses`:** `__init__`, `__repr__`, `__eq__` (aur `order=True` par comparisons,
`frozen=True` par `__hash__`) **khud** bana deta hai.

| Feature | Manual class | `@dataclass` |
|---|---|---|
| `__init__` | khud likho | mufat |
| `__repr__` | khud likho | mufat |
| `__eq__` | khud likho | mufat (`eq=True` default) |
| Ordering | 4 methods | `order=True` |
| Immutability | `__setattr__` trick | `frozen=True` |
| Default factory | `if x is None` dance | `field(default_factory=list)` |
"""))

cells.append(code(r"""
# ---- __init_subclass__: auto plugin registry -----------------------------
class Exporter:
    registry = {}

    def __init_subclass__(cls, fmt=None, **kw):
        super().__init_subclass__(**kw)
        if fmt is None:
            raise TypeError(f"{cls.__name__} ko fmt= dena hoga")
        cls.fmt = fmt
        Exporter.registry[fmt] = cls          # khud ba khud register
        print(f"  [registry] {fmt!r} -> {cls.__name__}")

    def export(self, rows):
        raise NotImplementedError


print("Subclasses define karte waqt:")

class JsonExporter(Exporter, fmt="json"):
    def export(self, rows):
        import json
        return json.dumps(rows)


class TsvExporter(Exporter, fmt="tsv"):
    def export(self, rows):
        return "\n".join("\t".join(map(str, r)) for r in rows)


print("\nregistry:", {k: v.__name__ for k, v in Exporter.registry.items()})
rows = [(1, "Ali"), (2, "Sara")]
picked = Exporter.registry["tsv"]()          # naam se plugin uthaya
print("tsv output:", repr(picked.export(rows)))

try:
    class NoFmt(Exporter): pass
except TypeError as err:
    print("\nfmt bhoolne par:", err)

assert set(Exporter.registry) == {"json", "tsv"}
print("[ok] __init_subclass__")
"""))

cells.append(code(r"""
from dataclasses import dataclass, field, asdict

# ---- manual vs dataclass -------------------------------------------------
class ManualPoint:
    def __init__(self, x, y=0, tags=None):
        self.x, self.y = x, y
        self.tags = tags if tags is not None else []      # mutable default dance
    def __repr__(self): return f"ManualPoint(x={self.x}, y={self.y}, tags={self.tags})"
    def __eq__(self, o): return isinstance(o, ManualPoint) and \
        (self.x, self.y, self.tags) == (o.x, o.y, o.tags)


@dataclass(order=True)                       # __init__, __repr__, __eq__, ordering — sab mufat
class Point3:
    x: int
    y: int = 0
    tags: list = field(default_factory=list) # mutable default ka SAHI tareeqa

    def distance(self):                      # normal methods bhi likh sakte ho
        return (self.x ** 2 + self.y ** 2) ** 0.5


p1, p2 = Point3(3, 4), Point3(3, 4)
print("repr mufat :", p1)
print("eq mufat   :", p1 == p2)
print("ordering   :", sorted([Point3(5), Point3(1), Point3(3)]))
print("method     :", p1.distance())
print("asdict     :", asdict(p1))
print("lines bachi:", "manual ~6 lines vs dataclass ~4 (aur bug-free)")

# frozen + slots
@dataclass(frozen=True, slots=True)
class Coord:
    lat: float
    lon: float


cd = Coord(24.86, 67.01)
print("\nfrozen hashable:", isinstance(hash(cd), int), "| set me:", len({cd, Coord(24.86, 67.01)}))
try:
    cd.lat = 0
except Exception as err:
    print("badalne par:", type(err).__name__)

# GOTCHA: mutable default seedha likha to error
try:
    @dataclass
    class BadDefault:
        items: list = []
except ValueError as err:
    print("\nmutable default ->", type(err).__name__, ":", str(err)[:60], "...")

assert p1 == p2 and asdict(p1)["x"] == 3
print("[ok] dataclasses")
"""))

# <<<CHUNK_END>>>


