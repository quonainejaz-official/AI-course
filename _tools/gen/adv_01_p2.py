import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code

CELLS = []
A = CELLS.append

A(md("""
---
## 7. Function Argument Passing — "Pass by Object Reference"

### Kya hai
Python na pure "pass by value" hai na "pass by reference". Sahi naam:
**call by object reference** (ya "call by sharing").

Jab tum `f(x)` likhte ho:
- function ka parameter ek **naya local naam** hai
- wo naam **usi object** par chipakta hai jo caller ke paas tha

Nateeja:
- Object ko **mutate** karo → caller ko dikhega
- Parameter ko **rebind** karo (`param = ...`) → caller ko kuch nahi dikhega
"""))

A(code(r"""
# Proof 1: rebinding caller ko nazar nahi aati -------------------------------
def rebind(items):
    print("   andar (shuru) id:", id(items))
    items = [99]                    # naye object par chipak gaya -> local baat
    print("   andar (baad)  id:", id(items))
    return items

outer = [1, 2, 3]
print("bahar id       :", id(outer))
rebind(outer)
print("call ke baad   :", outer, " <- bilkul nahi badla\n")

# Proof 2: mutation caller ko nazar aati hai
def mutate(items):
    items.append(99)                # object ke andar tabdeeli
print("mutate se pehle:", outer)
mutate(outer)
print("mutate ke baad :", outer, " <- badal gaya\n")

# Proof 3: id() se sabit ke object share ho raha hai
def show_id(obj):
    return id(obj)
d = {"a": 1}
print("same object hi gaya?", show_id(d) == id(d))

# Immutable ke sath: mutation mumkin hi nahi, is liye 'sab kuch safe' lagta hai
def try_change_number(n):
    n += 1                          # rebinding (int immutable)
    return n
num = 10
print("\nint:", try_change_number(num), "| bahar wala:", num)

# Sahi tareeqa jab caller ki list ko chhoona na ho: naya value return karo
def add_item_pure(items, x):
    return items + [x]              # naya object -> caller ki list mehfooz
base = [1, 2]
new = add_item_pure(base, 3)
print("pure style -> base:", base, " new:", new)
"""))

A(md("""
### Output ka matlab
Teen proofs: (1) `items = [99]` ka bahar zero asar, (2) `items.append(99)` ka bahar poora asar,
(3) `id()` barabar → object copy nahi hua, share hua.

### Gotchas
- Argument ko mutate karna (side effect) theek hai magar **document karo**. Library code me
  in-place functions ko `sort_in_place` / `update_*` jaisa saaf naam do.
- Defensive copy: `def f(items): items = list(items)` — jab caller ki list ko chhoona nahi chahte.

### Interview tip
*"Arguments are passed by object reference: the parameter is a new local name bound to the same
object. Mutations are visible to the caller; rebinding is not."*
"""))

A(md("""
---
## 8. Mutable Default Argument Trap — deep dive

### Kya hai
```python
def f(items=[]):   # <-- BUG
```
Default value **function define hote waqt EK dafa** evaluate hoti hai aur function object ke
`__defaults__` tuple me sambhaal li jaati hai. Har call me **wohi** list dobara use hoti hai.

### Kyun aisa hai (design wajah)
`def` ek executable statement hai; defaults usi waqt evaluate hote hain. Har call par
re-evaluate karna semantics ko closure jaisa pechida bana deta aur slow bhi hota.

### Sahi tareeqa
`None` sentinel + andar naya object banao.
"""))

A(code(r"""
# Trap live -------------------------------------------------------------------
def add_bad(item, bucket=[]):          # BUG: mutable default
    bucket.append(item)
    return bucket

print("call 1:", add_bad("a"))
print("call 2:", add_bad("b"), " <- purani list wapas aa gayi!")
print("call 3:", add_bad("c"))
print("function ka chhupa hua state:", add_bad.__defaults__)   # yahan zinda baitha hai

# Sahi tareeqa ---------------------------------------------------------------
def add_good(item, bucket=None):
    if bucket is None:                 # 'is None' -> falsy check se behtar ([] bhi falsy hai)
        bucket = []
    bucket.append(item)
    return bucket

print("\ngood call 1:", add_good("a"))
print("good call 2:", add_good("b"), " <- har dafa fresh")
print("caller ki list ke sath:", add_good("z", ["x", "y"]))

# Kyun 'if not bucket' galat hai: caller ki khaali list chup-chaap replace ho jaati hai
def add_subtle_bug(item, bucket=None):
    if not bucket:                     # [] bhi falsy -> caller ki list ignore!
        bucket = []
    bucket.append(item)
    return bucket

callers_list = []
add_subtle_bug("a", callers_list)
print("\n'if not bucket' ke sath caller ki list:", callers_list, " <- update nahi hui (bug)")

# Ye masla sirf list/dict ka nahi -- har us expression ka hai jise fresh chahiye
import time
def stamped(t=time.time()):            # BUG: define-time ka waqt hamesha
    return t
first = stamped(); time.sleep(0.01); second = stamped()
print("\ntime default same?", first == second, " <- 'now' nahi milta, define-time milta hai")

# Immutable default bilkul safe hai
def safe(n, factor=2, label="row"):    # int/str immutable -> koi masla nahi
    return f"{label}-{n * factor}"
print(safe(3), safe(3, 3))

# Class body me bhi wahi trap (shared class attribute)
class Basket:
    items = []                         # BUG: sab instances ek hi list share karenge
    def add(self, x): self.items.append(x)
b1, b2 = Basket(), Basket()
b1.add("apple")
print("\nclass attribute trap -> b2.items:", b2.items, " <- b2 ne kuch add hi nahi kiya tha")
"""))

A(md("""
### Output ka matlab
`add_bad.__defaults__` me wohi list nazar aa rahi hai jo call-to-call bharti ja rahi hai —
yaani "chhupa hua global state". `Basket` demo ne dikhaya ke class body me bhi yehi trap hai.

### Gotchas
1. `if not bucket:` vs `if bucket is None:` — pehla caller ki *khaali* list discard kar deta hai.
2. `def f(x, _cache={})` jaan boojh kar cache ke liye chalta hai, magar `functools.cache` saaf hai.
3. Mutable class attributes ke liye `__init__` me `self.items = []` likho.

### Interview tip
*"Default arguments are evaluated once at definition time and stored in `__defaults__`.
Use `None` as a sentinel for mutable defaults."*
"""))

A(md("""
---
## 9. Shallow vs Deep Copy — internals

### Kya hai
- **Shallow copy** — naya *container*, andar wale objects wohi (shared).
  `list(x)`, `x[:]`, `dict(x)`, `x.copy()`, `copy.copy(x)`
- **Deep copy** — naya container **aur** andar sab kuch recursively naya. `copy.deepcopy(x)`

### deepcopy ka internal jadoo: `memo` dict
`deepcopy` ek `memo` (id → nayi copy) dictionary rakhta hai:
1. **Cycles** infinite recursion me nahi jaate
2. Ek hi object agar do jagah tha, to copy me bhi **ek hi** (shared) rahega — structure mehfooz

### Kab kaunsa
- Flat data (numbers/strings ki list) → shallow kaafi aur bohat tez
- Nested config/tree/graph jise tum modify karogi → deep
- `deepcopy` **slow** hai; hot loop me na chalao
"""))

A(code(r"""
import copy

original = {"name": "ali", "scores": [10, 20], "meta": {"city": "Lahore"}}

shallow = copy.copy(original)          # == dict(original) == original.copy()
deep = copy.deepcopy(original)

print("shallow is original:", shallow is original)
print("deep    is original:", deep is original)

# andar wale objects?
print("\nnested list shared? shallow:", shallow["scores"] is original["scores"])
print("nested list shared? deep   :", deep["scores"] is original["scores"])

# ab mutate kar ke asar dekho
original["scores"].append(30)
original["meta"]["city"] = "Karachi"
print("\noriginal:", original)
print("shallow :", shallow, " <- saath saath badal gaya")
print("deep    :", deep, " <- bilkul mehfooz")

# top-level rebinding shallow copy ko nahi chhoota
original["name"] = "usman"
print("\nname rebind ke baad -> shallow['name']:", shallow["name"])
"""))

A(code(r"""
import copy

# Structure sharing ka proof: memo dict ka kamaal ----------------------------
inner = [1, 2]
nested = [inner, inner]                # ek hi list, do jagah
d = copy.deepcopy(nested)
print("original me dono slots same object?:", nested[0] is nested[1])
print("copy me bhi dono slots same object?:", d[0] is d[1], " <- memo ne structure bachaya")
print("copy original se alag hai?         :", d[0] is not inner)

# Recursive / self-referencing structure --------------------------------------
loop = [1, 2]
loop.append(loop)                      # khud ko contain karta hai!
print("\nself-referencing list:", str(loop)[:30], "...")
lc = copy.deepcopy(loop)               # crash nahi hoga -> memo ki wajah se
print("deepcopy ke baad khud ko contain karta hai?", lc[2] is lc)
print("original se alag?", lc is not loop)

# list ke shallow copy ke 4 tareeqe
src = [1, 2, 3]
copies = [src[:], list(src), src.copy(), copy.copy(src)]
print("\nsab equal:", all(c == src for c in copies),
      "| sab alag object:", all(c is not src for c in copies))

# 2D grid ka classic bug
grid_bug = [[0] * 3] * 3               # ek hi row 3 dafa!
grid_bug[0][0] = 9
print("\n[[0]*3]*3 ke sath:", grid_bug, " <- poora column badal gaya")
grid_ok = [[0] * 3 for _ in range(3)]  # har row alag object
grid_ok[0][0] = 9
print("comprehension ke sath:", grid_ok)
"""))

A(md("""
### Output ka matlab
- Shallow copy me `scores` list **share** thi → original ka `append` copy me bhi dikha.
- Deep copy poori tarah alag thi.
- `memo` ki wajah se (a) self-referencing list `RecursionError` ke baghair copy hui,
  (b) "do slots me ek hi object" wala rishta copy me bhi qaayam raha.

### Gotchas
- `copy.copy` custom class par default me `__dict__` shallow copy karta hai — nested attributes share honge.
- `deepcopy` un objects par masla karta hai jo copy hone layak nahi (open file, socket, lock, DB connection).
- `deepcopy` **slow** hai (recursion + memo). Config load par theek, per-request loop me nahi.

### Interview tip
*"`deepcopy` uses a memo dict keyed by `id()`, which both prevents infinite recursion on cycles
and preserves shared-object structure in the copy."*
"""))

A(md("""
---
## 10. `__copy__` aur `__deepcopy__` hooks — copy ko control karna

### Kya hai
`copy.copy(obj)` pehle `obj.__copy__()` dhoondta hai; `copy.deepcopy(obj)`
`obj.__deepcopy__(memo)` dhoondta hai. Na milne par default `__reduce_ex__`/`__dict__` wala rasta.

### Kahan zaroorat parti hai
- Object me **non-copyable resource** ho (file handle, socket, lock, connection pool)
- Copy me kuch fields **share** rakhni ho aur kuch fresh
- Copy karte waqt cache/ID **reset** karna ho
"""))

A(code(r"""
import copy, threading

class Report:
    # Ek class jis me non-copyable resource (lock) aur ek cache hai
    def __init__(self, title, rows):
        self.title = title
        self.rows = rows
        self._lock = threading.Lock()      # Lock deepcopy-friendly nahi hai
        self._cache = {"total": sum(rows)} # copy me reset karna behtar

    def __copy__(self):
        cls = self.__class__
        new = cls.__new__(cls)             # __init__ bypass
        new.__dict__.update(self.__dict__) # sab kuch shallow (rows SHARED)
        new._lock = threading.Lock()       # resource fresh
        return new

    def __deepcopy__(self, memo):
        cls = self.__class__
        new = cls.__new__(cls)
        memo[id(self)] = new               # LAZMI pehle: cycles ke liye
        new.title = copy.deepcopy(self.title, memo)
        new.rows = copy.deepcopy(self.rows, memo)
        new._lock = threading.Lock()       # naya lock, copy nahi
        new._cache = {}                    # cache reset
        return new

    def __repr__(self):
        return f"Report({self.title!r}, rows={self.rows}, cache={self._cache})"

r = Report("Q1", [1, 2, 3])
sc = copy.copy(r)
dc = copy.deepcopy(r)

print("original :", r)
print("shallow  :", sc, "| rows shared?", sc.rows is r.rows, "| lock same?", sc._lock is r._lock)
print("deep     :", dc, "| rows shared?", dc.rows is r.rows, "| lock same?", dc._lock is r._lock)

r.rows.append(4)
print("\noriginal me append ke baad -> shallow.rows:", sc.rows, " deep.rows:", dc.rows)

# Bina hook, lock wala object deepcopy par error deta hai
class Naive:
    def __init__(self):
        self.lock = threading.Lock()
try:
    copy.deepcopy(Naive())
    print("\n(is build me lock copy ho gaya -- phir bhi rely na karo)")
except Exception as e:
    print("\nbina hook deepcopy(lock) ->", type(e).__name__, ":", str(e)[:70])
"""))

A(md("""
### Output ka matlab
`__copy__` ne rows share ki magar lock naya diya; `__deepcopy__` ne sab naya diya aur cache reset kiya.

### Gotcha
`__deepcopy__` me **sab se pehle** `memo[id(self)] = new` likho, warna cyclic structure
infinite recursion me chala jayega.

### Interview tip
*"Override `__copy__`/`__deepcopy__` when your object owns resources that shouldn't be duplicated;
register yourself in `memo` first to stay cycle-safe."*
"""))
