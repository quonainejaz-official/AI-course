import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code

CELLS = []
A = CELLS.append

A(md("""
---
## 11. Garbage Collector — refcount + cycle detector

### Kya hai
CPython me **do** cleanup mechanisms hain:

1. **Reference counting** (primary) — refcount 0 → foran free. Fast, deterministic.
2. **Cycle collector** (`gc` module) — un objects ke liye jo aik doosre ko pakar kar baithe hain
   (`a.peer = b; b.peer = a`). In ka refcount kabhi 0 nahi hota, is liye alag detector chahiye.

### Generational idea
Objects "generations" me rakhe jaate hain (0 = naye). Zyada tar objects jawan hi mar jaate hain
(*weak generational hypothesis*), is liye gen-0 baar baar aur purani generations kam kam scan hoti hain.
**Python 3.13+ me GC incremental hai** — is liye `gc.get_threshold()` ki teesri value `0` dikhti hai;
purani "700, 10, 10" wali baat ratna nahi, khud print kar ke dekho.

### Ahem
Sirf **container** objects (jo doosre objects ko refer kar sakte hain) GC track karta hai.
`int`/`str` jaise atomic objects cycle bana hi nahi sakte → track nahi hote.
"""))

A(code(r"""
import gc, weakref

print("gc enabled?      :", gc.isenabled())
print("thresholds       :", gc.get_threshold(), " (3.13+ incremental GC)")
print("gen counts       :", gc.get_count())
print("tracked? list    :", gc.is_tracked([1, 2]))
print("tracked? int     :", gc.is_tracked(42), " <- atomic objects track nahi hote")

# ---- Reference cycle live demo ----
class Node:
    def __init__(self, name):
        self.name = name
        self.peer = None
    def __repr__(self):
        return f"Node({self.name})"

a, b = Node("A"), Node("B")
a.peer = b
b.peer = a                    # cycle: A -> B -> A

watch_a = weakref.ref(a)      # weakref refcount nahi barhata -> jasoosi ke liye perfect
del a, b                      # dono naam gaye... magar objects aik doosre ko pakre hain

alive_before = watch_a() is not None
print("\ndel ke baad zinda hai?      ", alive_before, " <- refcounting nakaam (cycle)")
collected = gc.collect()      # cycle collector chalao
print("gc.collect() ne free kiye   :", collected, "objects")
print("ab zinda hai?               ", watch_a() is not None, " <- cycle collector ne saaf kiya")

# ---- Cycle se bachne ka tareeqa: weakref parent pointer ----
class Child:
    def __init__(self, parent):
        self._parent = weakref.ref(parent)     # strong ref nahi -> koi cycle nahi
    @property
    def parent(self):
        return self._parent()                  # call karo -> object ya None

class Parent:
    def __init__(self):
        self.children = []
    def add(self):
        c = Child(self); self.children.append(c); return c

p = Parent(); c = p.add()
watch_p = weakref.ref(p)
print("\nchild se parent milta hai?  ", c.parent is p)
del p
print("parent del ke baad (bina gc):", watch_p(), " <- foran free, cycle bana hi nahi")
print("child ka parent ab           :", c.parent)
"""))

A(md("""
### Output ka matlab
`del a, b` ke baad bhi object zinda tha (aik doosre ki wajah se refcount 1 baaqi tha).
`gc.collect()` ne cycle detect kar ke free kiya. Doosre demo me `weakref` ki wajah se cycle
bana hi nahi — object foran free ho gaya, GC ki zaroorat hi nahi pari.

### Gotchas
- `gc.disable()` sirf tab jab yaqeen ho ke cycles nahi banenge (kuch high-perf short-request services
  karte hain) — warna memory barhti rahegi.
- Cycles aam hain: doubly linked list, parent/child trees, `self.callback = self.method`,
  exception + `__traceback__` (frames ko pakarta hai), closures.
- Leak hunting: `gc.get_referrers(obj)` / `gc.get_referents(obj)`, aur
  `gc.set_debug(gc.DEBUG_SAVEALL)` + `gc.garbage`.

### Interview tip
*"Refcounting frees objects immediately but cannot free reference cycles; the generational
(now incremental) `gc` handles cycles and only tracks container objects."*
"""))

A(md("""
---
## 12. `__del__` ke khatray

### Kya hai
`__del__` "destructor" hai — refcount 0 hone par (ya GC ke waqt) chalta hai.

### Kyun bachna chahiye
1. **Waqt ka koi wada nahi** — interpreter shutdown par bilkul na chale to bhi legal hai.
2. **Exceptions nigal jaate hain** — sirf "unraisable exception" stderr par jaata hai.
3. **Resurrection** — `__del__` me object ko kahin store kar do to wo zinda ho jata hai.
4. Shutdown par module globals `None` ho sakte hain → `__del__` me module use karna crash-prone.

### Sahi rasta
- Resource cleanup → **context manager** (`with`, `__enter__`/`__exit__`) ya explicit `.close()`
- "object mar jaye to ye chalao" → **`weakref.finalize`** (safe, ek dafa, predictable)
"""))

A(code(r"""
import weakref

# 1) __del__ me exception chup-chaap gum ho jata hai
class Risky:
    def __del__(self):
        try:
            raise ValueError("cleanup fail!")   # asli code me ye gum ho jata
        except Exception as e:
            print("   [__del__] exception khud handle kiya:", e)

r = Risky(); del r
print("dekha? program chalta raha -- error kahin report nahi hua\n")

# 2) Resurrection: __del__ object ko zinda kar sakta hai
GRAVEYARD = []
class Zombie:
    def __init__(self, n): self.n = n
    def __del__(self):
        GRAVEYARD.append(self)      # KHATRA: khud ko zinda kar liya
z = Zombie(1); del z
print("del ke baad bhi zinda:", len(GRAVEYARD) == 1, "-> aur __del__ dobara nahi chalega")
GRAVEYARD.clear()

# 3) Behtar A: weakref.finalize
class Connection:
    def __init__(self, name):
        self.name = name
        # NOTE: callback me self capture NA karo warna object kabhi marega hi nahi
        self._fin = weakref.finalize(self, print, f"   [finalize] {name} band ho gaya")
    def close(self):
        self._fin()                 # explicit close -> foran, sirf ek dafa

c = Connection("db-1")
print("\nfinalize alive?", c._fin.alive)
c.close()
print("close ke baad alive?", c._fin.alive)
c2 = Connection("db-2")
del c2                              # yahan finalize khud chalega
print()

# 4) Behtar B: context manager (sab se pasandeeda)
class Session:
    def __enter__(self):
        print("   [enter] session khula")
        return self
    def __exit__(self, exc_type, exc, tb):
        print("   [exit ] session band (exception ho ya na ho)")
        return False                # exception dabao mat

with Session() as s:
    print("   kaam ho raha hai...")
try:
    with Session():
        raise RuntimeError("kuch toot gaya")
except RuntimeError as e:
    print("   exception bahar aaya, magar cleanup pehle hua:", e)
"""))

A(md("""
### Output ka matlab
`Risky` me error gum ho gaya, `Zombie` ne khud ko zinda kar liya, jab ke `finalize` aur `with`
dono ne predictable ek-dafa cleanup diya — aur `with` ne exception ke sath bhi cleanup kiya.

### Interview tip
*"`__del__` is non-deterministic, swallows exceptions and can resurrect objects. Use context
managers for resource lifetime and `weakref.finalize` for 'run when this dies' hooks."*
"""))

A(md("""
---
## 13. `weakref` aur `WeakValueDictionary` — memory-safe cache

### Kya hai
**Weak reference** = object ka pata jo uska refcount **nahi** barhata. Object mar sakta hai
chahe weakref maujood ho; baad me weakref call karne par `None` milta hai.

### Asli use-cases
1. **Cache / identity map** — jab tak object kahin asal me use ho raha hai cache me raho,
   warna khud nikal jao (`WeakValueDictionary`)
2. **Parent pointers / back-references** — cycles se bachne ke liye
3. **Observers / callbacks** — listener ko zinda mat rakho
4. **Per-object metadata** — `WeakKeyDictionary` (object → extra info)

### Gotcha
Har object weakref-able nahi: plain `int`/`str`/`tuple`, aur `__slots__` wali class
(jab tak `__weakref__` slot na ho) support nahi karte.
"""))

A(code(r"""
import weakref, gc

class Record:
    __slots__ = ("rid", "payload", "__weakref__")   # <-- __weakref__ warna weakref fail
    def __init__(self, rid, payload):
        self.rid, self.payload = rid, payload
    def __repr__(self):
        return f"Record({self.rid})"

# 1) Basic weakref
rec = Record(1, "data")
wr = weakref.ref(rec)
print("weakref se object:", wr(), "| alive?", wr() is not None)
del rec
gc.collect()
print("del ke baad      :", wr(), " <- reference khud dead ho gaya\n")

# 2) WeakValueDictionary se identity-map cache
class RecordCache:
    # Maqsad: agar same rid ka object pehle se zinda hai to wohi do (duplicate memory na lage)
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()
        self.hits = self.misses = 0
    def get(self, rid, payload):
        obj = self._cache.get(rid)
        if obj is not None:
            self.hits += 1
            return obj
        self.misses += 1
        obj = Record(rid, payload)
        self._cache[rid] = obj          # weak -> koi strong ref na bache to nikal jayega
        return obj

cache = RecordCache()
r1 = cache.get(7, "seven")
r2 = cache.get(7, "seven")              # same object milna chahiye
print("dono same object?", r1 is r2, "| hits:", cache.hits, "misses:", cache.misses)
print("cache size       :", len(cache._cache))

del r1, r2                              # aakhri strong references gaye
gc.collect()
print("references jaane ke baad cache size:", len(cache._cache), " <- leak nahi hua")

# Muqabla: normal dict cache object ko zinda pakar leta hai
strong = {}
r3 = Record(8, "eight")
strong[8] = r3
del r3
gc.collect()
print("normal dict cache size:", len(strong), " <- object phansa hua (potential leak)")

# 3) WeakKeyDictionary se per-object metadata
meta = weakref.WeakKeyDictionary()
r4 = Record(9, "nine")
meta[r4] = {"last_seen": "2026-01-01"}
print("\nmetadata:", meta[r4], "| entries:", len(meta))
del r4
gc.collect()
print("object marne par metadata bhi gaya:", len(meta))

# 4) Non-weakref-able types
try:
    weakref.ref((1, 2))
except TypeError as e:
    print("\nweakref.ref((1,2)) ->", type(e).__name__, ":", e)
"""))

A(md("""
### Output ka matlab
`WeakValueDictionary` ne duplicate objects bachaye (`r1 is r2`) **aur** references jaane par
khud saaf bhi ho gayi. Normal `dict` me entry phansi rah gayi — yehi classic
"cache = memory leak" bug hai.

### Gotchas
- Weak dict par iterate karte waqt entries beech me gaayab ho sakti hain → `list(d.items())` le kar chalo.
- Bounded (LRU) cache chahiye to weakref kaafi nahi — `functools.lru_cache` ya manual LRU
  (dekho LC 146 neeche).
- `__slots__` ke sath `__weakref__` slot add karna zaroori hai.

### Interview tip
*"Use `WeakValueDictionary` for identity-map caches: entries vanish when the last strong reference
dies, so the cache can't keep objects alive forever."*
"""))

A(md("""
---
## 14. `__slots__` — memory aur speed dono

### Kya hai
Default me har instance ke paas ek **`__dict__`** hota hai (attributes ka dictionary) —
flexible magar mehnga. `__slots__` batata hai ke attributes ki list fixed hai, to CPython
`__dict__` ke bajaye **fixed-size C array** use karta hai.

### Faide
1. **Memory** — per-instance dict (~100+ bytes) khatam
2. **Speed** — attribute access thora tez (offset lookup, dict hashing nahi)
3. **Typo safety** — `obj.nmae = 1` par `AttributeError` (naya attribute ban hi nahi sakta)

### Nuqsanat
- Naye attributes add nahi kar sakte (dynamic patching band)
- `__weakref__` alag se maangna parta hai
- Multiple inheritance me slots conflict pechida
- Class-level defaults + slots ka naam clash nahi ho sakta
"""))

A(code(r"""
import sys, timeit

class PointDict:                        # normal class -> __dict__ ke sath
    def __init__(self, x, y):
        self.x, self.y = x, y

class PointSlots:                       # slots wali class
    __slots__ = ("x", "y")
    def __init__(self, x, y):
        self.x, self.y = x, y

pd, ps = PointDict(1, 2), PointSlots(1, 2)

# --- MEMORY ---
dict_total = sys.getsizeof(pd) + sys.getsizeof(pd.__dict__)
slots_total = sys.getsizeof(ps)
print("PointDict : object", sys.getsizeof(pd), "+ __dict__", sys.getsizeof(pd.__dict__),
      "=", dict_total, "bytes")
print("PointSlots:", slots_total, "bytes")
print(f"bachat    : {dict_total - slots_total} bytes per instance "
      f"({100 * (1 - slots_total / dict_total):.0f}% kam)")
print("100k objects par bachat: ~", round((dict_total - slots_total) * 100_000 / 1024 / 1024, 1), "MB")

# --- SPEED (sirf print, koi timing assert nahi) ---
t_dict = timeit.timeit("pd.x", globals=globals(), number=200_000)
t_slot = timeit.timeit("ps.x", globals=globals(), number=200_000)
print(f"\nattribute read: dict {t_dict:.4f}s | slots {t_slot:.4f}s "
      f"(slots aam tor par ~10-25% tez)")

# --- Typo safety ---
try:
    ps.z = 5
except AttributeError as e:
    print("\nslots par naya attribute:", type(e).__name__, ":", e)
pd.z = 5
print("dict wali class par chal gaya (typo pakra nahi gaya):", pd.z)

# --- __dict__ hai ya nahi ---
print("\nhasattr(ps, '__dict__'):", hasattr(ps, "__dict__"))
print("PointSlots.__slots__   :", PointSlots.__slots__)

# --- Inheritance ka gotcha: subclass bina __slots__ ke to dict wapas aa jata hai ---
class Child(PointSlots):
    pass                                # __slots__ nahi diya -> __dict__ wapas
ch = Child(1, 2); ch.anything = 1
print("subclass bina __slots__ -> __dict__ wapas:", hasattr(ch, "__dict__"))

class ChildOK(PointSlots):
    __slots__ = ()                      # sahi tareeqa: khaali slots
print("subclass with __slots__=() -> __dict__?", hasattr(ChildOK(1, 2), "__dict__"))
"""))

A(md("""
### Output ka matlab
Slots wale object ka size sirf object hai (koi alag dict nahi) — is liye 100k rows par
megabytes ki bachat. Attribute read bhi thora tez. Aur `ps.z = 5` ne typo pakar liya.

### Gotchas
1. Subclass me `__slots__ = ()` na likho to `__dict__` wapas aa jata hai aur poora faida khatam.
2. `@dataclass(slots=True)` (Python 3.10+) se dataclass ke sath slots asaani se mil jaate hain.
3. Slots + `weakref` chahiye to `__slots__` me `"__weakref__"` add karo.
4. Slots premature optimization ban sakte hain — sirf tab jab **hazaaron/lakhon** instances ho.

### Interview tip
*"`__slots__` replaces the per-instance `__dict__` with a fixed C-level array: less memory,
slightly faster attribute access, no dynamic attributes."*
"""))

A(md("""
---
## 15. `sys.getsizeof` vs asli size — recursive sizer

### Kya hai
`sys.getsizeof(obj)` sirf **us object ka apna** size deta hai — andar wale objects ka nahi.
List ke liye ye sirf pointer array ka size hai, elements ka nahi!

### Kyun matter karta hai
Memory audit karte waqt log `getsizeof(big_list)` dekh kar khush ho jaate hain ke "sirf 8KB".
Asal me andar 10,000 strings ho sakti hain = megabytes.

### Sahi tareeqa
Recursive sizer likho jo `id()` ke sath **seen** set rakhe (shared objects do dafa na ginay,
cycles me na phanse). Ya `tracemalloc` / `pympler` jaisi cheez use karo.
"""))

A(code(r"""
import sys
from itertools import chain
from collections import deque

def deep_size(obj, seen=None):
    # Object ka 'asli' size: khud + andar wale sab (shared objects sirf ek dafa)
    seen = set() if seen is None else seen
    oid = id(obj)
    if oid in seen:                      # pehle gin liya (ya cycle) -> 0
        return 0
    seen.add(oid)
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(deep_size(k, seen) + deep_size(v, seen) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset, deque)):
        size += sum(deep_size(i, seen) for i in obj)
    elif hasattr(obj, "__dict__"):       # custom object -> uska dict bhi
        size += deep_size(vars(obj), seen)
    elif hasattr(obj, "__slots__"):      # slots wale object ke fields
        size += sum(deep_size(getattr(obj, s), seen)
                    for s in obj.__slots__ if hasattr(obj, s))
    return size

# Demo: shallow vs deep --------------------------------------------------------
words = [f"user_number_{i}" for i in range(500)]
print("getsizeof(list) :", sys.getsizeof(words), "bytes  <- sirf pointer array")
print("deep_size(list) :", deep_size(words), "bytes  <- strings bhi shaamil")
print("farq            :", deep_size(words) - sys.getsizeof(words), "bytes chhup rahe the")

nested = {"users": [{"id": i, "name": f"name{i}"} for i in range(50)]}
print("\ngetsizeof(dict):", sys.getsizeof(nested), "| deep_size:", deep_size(nested))

# Shared object ko do dafa na ginna
shared = ["x" * 1000]
pair = [shared, shared]
print("\nshared list do jagah -> deep_size:", deep_size(pair),
      "(1000-char string sirf ek dafa gini)")

# Cycle safe?
cyc = [1, 2]; cyc.append(cyc)
print("cyclic structure par deep_size chal gaya:", deep_size(cyc), "bytes")
"""))

A(md("""
### Output ka matlab
`getsizeof` ne 500 strings ki list ko chand hazaar bytes bataya, `deep_size` ne asli
(kai guna bara) number diya. `seen` set ki wajah se shared string ek dafa gini gayi aur
self-referencing list par bhi crash nahi hua.

### Gotchas
- `getsizeof` custom object ke `__dict__` ko count nahi karta.
- Interned/shared objects ki wajah se "asli" size ki tareef hi mushkil hai — 2 lists ka
  deep_size jama karna double-count kar sakta hai.
- Production memory analysis ke liye `tracemalloc` (allocations by line) behtar hai.

### Interview tip
*"`sys.getsizeof` is shallow — for containers it excludes referenced objects. Deep accounting
needs recursion with an id-based `seen` set, or `tracemalloc`."*
"""))

A(md("""
---
## 16. CPython Object Overhead aur list over-allocation

### Kya hai
Python me "chhoti" cheez bhi sasti nahi: har object ke sath **header** hota hai
(refcount + type pointer, aur variable-size objects me length).

Approx (64-bit CPython): `object` header 16 bytes, `int` 28 bytes (chhota), `float` 24,
khaali `list` 56, khaali `dict` 64, khaali `set` 216, `str` ~41 + chars.

### list over-allocation
`list.append` har dafa exact 1 slot nahi barhaati — **thora zyada** allocate karti hai
(growth pattern ~1.125x) taake har append par realloc na ho. Isi liye `append` amortized O(1) hai.
"""))

A(code(r"""
import sys

print("--- khaali containers ka size ---")
for label, obj in [("int 0", 0), ("int 2**70", 2 ** 70), ("float", 1.5), ("bool", True),
                   ("str ''", ""), ("str 'a'", "a"), ("str 'a'*100", "a" * 100),
                   ("list []", []), ("tuple ()", ()), ("dict {}", {}), ("set()", set()),
                   ("bytes b''", b"")]:
    print(f"{label:>14}: {sys.getsizeof(obj):>4} bytes")

print("\n--- int arbitrary precision: digits ke sath size barhta hai ---")
for n in (1, 2 ** 30, 2 ** 60, 2 ** 300):
    print(f"  {str(n)[:12]:>14}... -> {sys.getsizeof(n)} bytes")

print("\n--- list over-allocation (append par capacity jumps) ---")
lst = []
last = sys.getsizeof(lst)
print(f"  len=0  size={last}")
for i in range(1, 40):
    lst.append(i)
    cur = sys.getsizeof(lst)
    if cur != last:                    # sirf tab print jab capacity badli
        print(f"  len={i:<3} size={cur}   <- realloc hua (jump {cur - last} bytes)")
        last = cur

print("\n--- exact-size banane ke tareeqe ---")
from_list = list(range(20))
from_tuple = tuple(range(20))
print("list(range(20))  :", sys.getsizeof(from_list), "bytes (thori extra capacity)")
print("tuple(range(20)) :", sys.getsizeof(from_tuple), "bytes (exact, immutable)")
print("bachat           :", sys.getsizeof(from_list) - sys.getsizeof(from_tuple), "bytes")
"""))

A(md("""
### Output ka matlab
Capacity jumps sabit karte hain ke `list` "batch" me barhti hai. Isi liye 1 million appends
par bhi performance theek rehti hai (amortized O(1)) — magar memory zaroorat se thori zyada.

### Gotchas
- Agar size pehle se maloom ho, list comprehension / `list(iterable)` faster + tighter hai.
- `int` arbitrary precision hai — bara number bara object.
- `set` ka khaali size sab se bara (hash table pehle se allocate).

### Interview tip
*"CPython lists over-allocate on growth (amortised O(1) append) and store pointers, not values —
which is why a list of ints costs far more than a C array of ints."*
"""))
