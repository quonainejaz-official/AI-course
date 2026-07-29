import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code

CELLS = []
A = CELLS.append

A(md("""
---
## 17. list vs tuple vs array vs deque vs bytes — memory ka muqabla

### Kya hai
Sab "sequence" hain magar memory model bilkul mukhtalif:

| Type | Andar kya rakhta hai | Mutable? | Best for |
|---|---|---|---|
| `list` | **pointers** (8 bytes) + over-allocation | haan | general purpose, mixed types |
| `tuple` | pointers, exact size | nahi | fixed records, dict keys |
| `array.array` | **raw C values** (e.g. 4-byte int) | haan | bohat se numbers, homogeneous |
| `bytes` / `bytearray` | raw bytes (1 byte each) | nahi / haan | binary data, buffers |
| `collections.deque` | doubly linked blocks | haan | dono taraf se O(1) push/pop |
| `numpy.ndarray` | contiguous C array + vectorized ops | haan | numeric compute |

**Ahem:** `list` me 1000 ints = 1000 pointers **+** 1000 int objects (har ek ~28 bytes).
`array('i')` me wohi 1000 ints = 4000 bytes. Farq 10x se zyada.
"""))

A(code(r"""
import sys, array
from collections import deque
import numpy as np

N = 1000
as_list  = list(range(N))
as_tuple = tuple(range(N))
as_array = array.array("i", range(N))      # 'i' = signed int (4 bytes)
as_deque = deque(range(N))
as_bytes = bytes(N)                        # N zero bytes
as_np    = np.arange(N, dtype=np.int32)

def total_list_cost(lst):
    # list ka apna size + andar wale int objects (chhote ints cached hain, phir bhi ginte hain)
    return sys.getsizeof(lst) + sum(sys.getsizeof(i) for i in lst)

rows = [
    ("list (container only)", sys.getsizeof(as_list)),
    ("list + int objects   ", total_list_cost(as_list)),
    ("tuple (container)    ", sys.getsizeof(as_tuple)),
    ("array('i')           ", sys.getsizeof(as_array)),
    ("deque                ", sys.getsizeof(as_deque)),
    ("bytes                ", sys.getsizeof(as_bytes)),
    ("numpy int32          ", as_np.nbytes + sys.getsizeof(as_np) - as_np.nbytes),
]
print(f"{N} integers rakhne ka kharcha:")
for label, size in rows:
    print(f"  {label}: {size:>8} bytes")

print("\nlist+ints vs array ratio:",
      round(total_list_cost(as_list) / sys.getsizeof(as_array), 1), "x")

# deque ka asli faida: dono sire par O(1)
import timeit
setup_l = "from collections import deque\nl=list(range(10000))\nd=deque(range(10000))"
t_list_front  = timeit.timeit("l.insert(0, 1); l.pop(0)", setup=setup_l, number=2000)
t_deque_front = timeit.timeit("d.appendleft(1); d.popleft()", setup=setup_l, number=2000)
print(f"\nfront insert/pop 2000x -> list {t_list_front:.4f}s | deque {t_deque_front:.4f}s")
print("list.insert(0) O(n) hai (sab elements shift), deque.appendleft O(1)")

# array/bytes ki limitation: sirf ek type
try:
    array.array("i", [1, "do", 3])
except TypeError as e:
    print("\narray me mixed types ->", type(e).__name__, ":", e)
"""))

A(md("""
### Output ka matlab
`list + int objects` ka number `array('i')` se kai guna bara hai — kyunki list pointers rakhti hai
aur har int alag heap object hai. Front insert/pop me `deque` list se bohat tez nikla.

### Gotchas
- Chhote ints cached hote hain, is liye `list(range(1000))` ki asli memory shared hoti hai —
  magar bare/unique numbers ke sath poora kharcha lagta hai.
- `array` sirf numeric homogeneous data ke liye; math karna ho to seedha `numpy` behtar.
- `deque` random indexing (`d[500]`) me list se slow hai (O(n)) — trade-off samjho.

### Interview tip
*"Python lists store pointers to boxed objects; `array`/`numpy` store raw values contiguously,
which is why they use far less memory and are cache-friendly."*
"""))

A(md("""
---
## 18. String concat in loop vs `join` — classic performance trap

### Kya hai
`str` **immutable** hai. Loop me `s += piece` har dafa **nayi string** banata hai aur poora
purana content copy karta hai → O(n²) total kaam.
`"".join(list_of_pieces)` ek dafa total length nikalta hai, ek buffer allocate karta hai → O(n).

### Note
CPython me `s += x` ke liye ek chhota optimization hai (jab refcount 1 ho to in-place resize
ki koshish) — is liye chhote loops me farq chhupa reh sakta hai. Bare data par `join` hi jeetta hai,
aur `join` ka intent bhi saaf hai.
"""))

A(code(r"""
import timeit, io

PIECES = [f"line-{i}\n" for i in range(2000)]

def by_concat():
    s = ""
    for p in PIECES:
        s += p                      # har dafa (potentially) nayi string
    return s

def by_join():
    return "".join(PIECES)          # ek allocation

def by_list_append():
    out = []
    for p in PIECES:
        out.append(p)               # list append sasta
    return "".join(out)

def by_stringio():
    buf = io.StringIO()             # file-jaisa buffer (streaming ke liye behtareen)
    for p in PIECES:
        buf.write(p)
    return buf.getvalue()

# sab ka natija bilkul same hona chahiye
assert by_concat() == by_join() == by_list_append() == by_stringio()
print("chaaron ka output same hai:", len(by_join()), "chars")

for name, fn in [("concat  +=", by_concat), ("join      ", by_join),
                 ("list+join ", by_list_append), ("StringIO  ", by_stringio)]:
    t = timeit.timeit(fn, number=200)
    print(f"  {name}: {t:.4f}s")

print("\nf-string chhoti cheezon ke liye sab se saaf aur tez hai:")
name, n = "ali", 3
t_fstr = timeit.timeit('f"{name} ka {n}"', globals=globals(), number=200_000)
t_plus = timeit.timeit('name + " ka " + str(n)', globals=globals(), number=200_000)
t_fmt  = timeit.timeit('"{} ka {}".format(name, n)', globals=globals(), number=200_000)
t_pct  = timeit.timeit('"%s ka %s" % (name, n)', globals=globals(), number=200_000)
print(f"  f-string {t_fstr:.4f}s | + {t_plus:.4f}s | .format {t_fmt:.4f}s | % {t_pct:.4f}s")
"""))

A(md("""
### Output ka matlab
Chaaron ka output barabar hai (assert pass hua) magar approach ka kharcha mukhtalif.
Bare inputs (100k+ pieces) par `+=` wala rasta dramatically slow ho jata hai.

### Gotchas
- `+=` ka CPython optimization sirf tab lagta hai jab string ka refcount 1 ho —
  agar tum wo string kahin aur bhi rakh do (list me append kar do) to optimization khatam.
- Logging me `logger.info("x " + str(y))` na likho — `logger.info("x %s", y)` likho
  (string tab banti hai jab log level allow kare).
- `StringIO` streaming/incremental output ke liye best (memory me poori list nahi rakhni parti).

### Interview tip
*"Strings are immutable, so repeated concatenation is O(n²) copying; accumulate pieces in a list
and `join` once, or stream into `io.StringIO`."*
"""))

A(md("""
---
## 19. `dis` — bytecode par nazar

### Kya hai
Python source ko **bytecode** me compile karta hai jo CPython ka virtual machine chalata hai.
`dis` module wohi bytecode dikhata hai. Ye "kyun ye code tez/slow hai" ka **asli jawab** deta hai.

### Kyun seekho
- Pata chalta hai `LOAD_FAST` (local) vs `LOAD_GLOBAL` ka farq
- Constant folding nazar aata hai (compiler ne khud hisaab kar liya)
- Comprehension vs loop ka difference samajh me aata hai

> **Note:** Python 3.11+ me bytecode names badle hain (`LOAD_SMALL_INT`, `LOAD_FAST_BORROW`,
> specialized adaptive instructions). Exact opcode names version-specific hain — concept dekho.
"""))

A(code(r"""
import dis

def add_tax(price):
    tax = price * 0.17          # local variable
    return price + tax

print("=== add_tax ka bytecode ===")
dis.dis(add_tax)

print("\n=== code object ke andar kya hai ===")
c = add_tax.__code__
print("co_varnames (locals):", c.co_varnames)
print("co_consts           :", c.co_consts)
print("co_names (globals)  :", c.co_names)
print("stack size          :", c.co_stacksize)
"""))

A(code(r"""
import dis

# --- Constant folding: compiler khud hisaab kar leta hai ---
def seconds_per_day():
    return 24 * 60 * 60         # ye runtime par multiply NAHI hoga

print("co_consts:", seconds_per_day.__code__.co_consts,
      " <- 86400 pehle se maujood (constant folding)")
dis.dis(seconds_per_day)

print("\n--- tuple constant bhi fold hota hai ---")
def const_tuple():
    return (1, 2, 3)
print("co_consts:", const_tuple.__code__.co_consts)

def nonconst_tuple(x):
    return (1, x, 3)            # x runtime par -> tuple runtime par banega
print("variable ke sath co_consts:", nonconst_tuple.__code__.co_consts)

print("\n--- 'in' literal set/frozenset optimization ---")
def check_literal(ch):
    return ch in {"a", "e", "i", "o", "u"}   # compiler isay frozenset constant bana deta hai
print("co_consts:", check_literal.__code__.co_consts)
print("dekha? set literal ko frozenset constant bana diya -> har call par set nahi banta")

def check_list(ch):
    return ch in ["a", "e", "i", "o", "u"]   # list constant ban sakti hai (tuple me)
print("list version co_consts:", check_list.__code__.co_consts)

print("\n--- string constant folding ki hadd ---")
def small_str():
    return "ab" * 3             # fold ho jata hai
print("co_consts:", small_str.__code__.co_consts)
print("bohat bari expressions (e.g. 'a'*10**9) jaan boojh kar fold NAHI hoti (memory bachane ke liye)")
"""))

A(md("""
### Output ka matlab
`24 * 60 * 60` ko compiler ne `86400` bana diya — runtime par koi multiplication nahi.
Set literal `{"a", ...}` ko `frozenset` **constant** bana diya, is liye membership check
har call par nayi set nahi banata. Ye sab **peephole optimizer / AST folding** ka kaam hai.

### Gotchas
- Constant folding sirf **literals** par hoti hai — `x * 60 * 60` fold nahi hoga.
- Micro-detail par optimize karne se pehle profile karo; bytecode dekhna samajhne ke liye hai.
- Bare literals ki folding jaan boojh kar mehdood hai (memory blow-up se bachne ke liye).

### Interview tip
*"CPython folds constant expressions at compile time and turns literal membership sets into
`frozenset` constants; `dis` and `co_consts` let you verify this."*
"""))

A(md("""
---
## 20. Local vs Global lookup speed — `LOAD_FAST` vs `LOAD_GLOBAL`

### Kya hai
- **Local variable** function ke code object ke ek **array slot** me hota hai → `LOAD_FAST`
  (index se seedha uthao)
- **Global / builtin** ko **dictionary lookup** se dhoondna parta hai → `LOAD_GLOBAL`
  (module dict, phir builtins dict)

### Kyun matter karta hai
Hot loop me `len()`, `append`, ya global config ko baar baar dhoondhna waqt khaata hai.
Classic trick: loop se pehle **local naam** me bind kar lo.
"""))

A(code(r"""
import dis, timeit

GLOBAL_FACTOR = 3               # module-level global

def uses_global(n):
    total = 0
    for i in range(n):
        total += i * GLOBAL_FACTOR       # har chakkar me LOAD_GLOBAL
    return total

def uses_local(n):
    total = 0
    factor = GLOBAL_FACTOR              # ek dafa uthao
    for i in range(n):
        total += i * factor             # ab LOAD_FAST
    return total

assert uses_global(1000) == uses_local(1000)     # natija bilkul same

t_g = timeit.timeit("uses_global(2000)", globals=globals(), number=300)
t_l = timeit.timeit("uses_local(2000)", globals=globals(), number=300)
print(f"global lookup: {t_g:.4f}s")
print(f"local  bind  : {t_l:.4f}s   (aam tor par thora tez)")

print("\n--- bytecode ka farq ---")
print("uses_global me:", [i.opname for i in dis.get_instructions(uses_global)
                          if "GLOBAL" in i.opname or "FAST" in i.opname])
print("uses_local  me:", [i.opname for i in dis.get_instructions(uses_local)
                          if "GLOBAL" in i.opname or "FAST" in i.opname])

# Method lookup ko bhi bind kiya ja sakta hai (classic idiom)
def append_slow(n):
    out = []
    for i in range(n):
        out.append(i)               # har dafa 'append' attribute lookup
    return out

def append_fast(n):
    out = []
    push = out.append               # bound method ek dafa uthao
    for i in range(n):
        push(i)
    return out

def append_comp(n):
    return [i for i in range(n)]    # sab se tez aur sab se saaf

assert append_slow(500) == append_fast(500) == append_comp(500)
for name, fn in [("out.append ", append_slow), ("bound push ", append_fast),
                 ("comprehension", append_comp)]:
    print(f"  {name}: {timeit.timeit(lambda fn=fn: fn(2000), number=200):.4f}s")
"""))

A(md("""
### Output ka matlab
Bytecode me saaf nazar aaya: `uses_global` me `LOAD_GLOBAL` hai, `uses_local` me sirf `FAST` variants.
Timing me local binding aur comprehension aage rehte hain.

### Gotchas
- Ye **micro-optimization** hai — sirf asli hot loop me karo, warna code ganda hota hai.
- Python 3.11+ me "specializing adaptive interpreter" ne `LOAD_GLOBAL` ko bohat behtar kar diya hai,
  is liye purani kitabon jaisa dramatic farq nahi milta.
- Pehla sawal hamesha: algorithm theek hai? (O(n²) → O(n)) — micro-opt baad me.

### Interview tip
*"Locals are array-indexed (`LOAD_FAST`), globals are dict lookups (`LOAD_GLOBAL`). In hot loops,
binding globals/methods to locals removes repeated dictionary lookups."*
"""))

A(md("""
---
## 21. Common Mistakes / Gotchas — sab ek jagah

Neeche har wo trap hai jahan log phaste hain. Cell chala kar output dekho.
"""))

A(code(r"""
print("1) [[0]*3]*3 -> rows shared")
g = [[0] * 3] * 3; g[0][0] = 1
print("   ", g, "| sahi:", [[0] * 3 for _ in range(3)])

print("\n2) dict.fromkeys mutable default -> value shared")
d = dict.fromkeys(["a", "b"], [])       # ek hi list sab keys me!
d["a"].append(1)
print("   ", d, "| sahi:", {k: [] for k in ["a", "b"]})

print("\n3) loop me list modify karna -> elements skip")
nums = [1, 2, 3, 4, 5, 6]
for x in list(nums):                    # copy par chalo
    if x % 2 == 0:
        nums.remove(x)
print("    copy par iterate (sahi):", nums)
bad = [1, 2, 3, 4, 5, 6]
for x in bad:                           # BUG: index shift ho jaata hai
    if x % 2 == 0:
        bad.remove(x)
print("    seedha iterate (bug) :", bad)

print("\n4) closure late binding -> sab functions aakhri value dekhte hain")
fns_bad = [lambda: i for i in range(3)]
print("    late binding:", [f() for f in fns_bad])
fns_ok = [lambda i=i: i for i in range(3)]   # default arg se value capture
print("    fixed       :", [f() for f in fns_ok])

print("\n5) tuple ke andar list par += -> mutate ho jata hai magar TypeError bhi aata hai")
t = (["a"],)
try:
    t[0] += ["b"]                       # __iadd__ chal gaya, phir slot assign par error
except TypeError as e:
    print("    error:", e)
print("    magar list mutate ho chuki:", t)

print("\n6) is vs == numbers/strings par")
big = 1000
print("    1000 is 1000 (do naam):", big is 1000, "| == :", big == 1000)

print("\n7) sort/sorted -- ek in-place, doosra naya object")
orig = [3, 1, 2]
srt = sorted(orig)                      # naya object
print("    sorted():", srt, "orig:", orig)
print("    orig.sort() ka return:", orig.sort(), " <- None! (in-place)")

print("\n8) mutable object ko set/dict key banane ki koshish")
try:
    {"key": 1}.setdefault([1], 2)
except TypeError as e:
    print("    ", type(e).__name__, ":", e)
"""))

A(md("""
### Har gotcha ka aik-line sabaq

1. `[[0]*3]*3` → **outer repetition** references copy karta hai, comprehension use karo.
2. `dict.fromkeys(keys, [])` → ek hi mutable value share hoti hai; dict comprehension use karo.
3. Jis list par loop chal raha hai usay modify na karo — `list(x)` copy par chalo ya nayi list banao.
4. Closure **variable** capture karta hai, **value** nahi — default arg ya `functools.partial` se bind karo.
5. `t[0] += [...]` me `__iadd__` pehle chalta hai (mutation ho jaati hai) phir tuple assignment fail hota hai.
6. `is` sirf singletons ke liye.
7. `list.sort()` `None` deta hai (in-place ka convention), `sorted()` nayi list.
8. Keys hashable honi chahiye.
"""))

A(md("""
---
## 22. Real-World Problems

Ab in sab concepts ko asli masail par lagaate hain — 4 problems, poore commented solutions ke sath.
"""))

A(code(r"""
# ---------------------------------------------------------------------------
# PROBLEM 1: 200k log lines process karni hain. Team ne pehle list banayi
#            (memory blow-up). Generator se memory ~constant kar do.
# ---------------------------------------------------------------------------
import tracemalloc

def fake_log_lines(n):
    # asli file ki jagah in-memory generator (koi bahar ki file nahi)
    for i in range(n):
        level = "ERROR" if i % 100 == 0 else "INFO"
        yield f"2026-01-01 10:00:{i % 60:02d} {level} request id={i} took={i % 500}ms"

N = 200_000

def count_errors_list(n):
    lines = [ln for ln in fake_log_lines(n)]           # BURA: sab memory me
    errors = [ln for ln in lines if " ERROR " in ln]   # BURA: doosri poori list
    return len(errors)

def count_errors_stream(n):
    # ACHA: ek waqt me ek line -> memory O(1)
    return sum(1 for ln in fake_log_lines(n) if " ERROR " in ln)

tracemalloc.start()
r1 = count_errors_list(N)
peak_list = tracemalloc.get_traced_memory()[1]
tracemalloc.stop()

tracemalloc.start()
r2 = count_errors_stream(N)
peak_stream = tracemalloc.get_traced_memory()[1]
tracemalloc.stop()

assert r1 == r2 == N // 100                 # natija bilkul same
print("errors mile         :", r1)
print("peak memory (list)  :", round(peak_list / 1024 / 1024, 2), "MB")
print("peak memory (stream):", round(peak_stream / 1024, 1), "KB")
print("Sabaq: pipeline me generator rakho, list sirf tab jab dobara chahiye ho.")
"""))

A(code(r"""
# ---------------------------------------------------------------------------
# PROBLEM 2: Default config sab requests me share ho rahi thi -> ek request ki
#            tabdeeli sab par lag gayi (classic production bug). Fix karo.
# ---------------------------------------------------------------------------
import copy

DEFAULT_CONFIG = {
    "retries": 3,
    "timeouts": {"connect": 5, "read": 30},
    "features": ["cache", "gzip"],
}

def handle_request_buggy(user_overrides):
    cfg = DEFAULT_CONFIG                     # BUG: same object!
    cfg.update(user_overrides)
    cfg["features"].append("debug")          # BUG: shared nested list mutate
    return cfg

def handle_request_shallow(user_overrides):
    cfg = dict(DEFAULT_CONFIG)               # aadha fix: top level alag
    cfg.update(user_overrides)
    cfg["features"].append("debug")          # ABHI BHI BUG: nested list shared
    return cfg

def handle_request_fixed(user_overrides):
    cfg = copy.deepcopy(DEFAULT_CONFIG)      # FIX: poora alag
    cfg.update(user_overrides)
    cfg["features"].append("debug")
    return cfg

snapshot = copy.deepcopy(DEFAULT_CONFIG)     # baad me compare karne ke liye

handle_request_buggy({"retries": 10})
print("buggy ke baad global config :", DEFAULT_CONFIG["retries"], DEFAULT_CONFIG["features"])
DEFAULT_CONFIG.clear(); DEFAULT_CONFIG.update(copy.deepcopy(snapshot))   # reset

handle_request_shallow({"retries": 7})
print("shallow ke baad global      :", DEFAULT_CONFIG["retries"], DEFAULT_CONFIG["features"],
      " <- retries bacha, features nahi")
DEFAULT_CONFIG.clear(); DEFAULT_CONFIG.update(copy.deepcopy(snapshot))   # reset

cfg = handle_request_fixed({"retries": 1})
print("fixed ke baad global        :", DEFAULT_CONFIG["retries"], DEFAULT_CONFIG["features"])
print("request wali config         :", cfg["retries"], cfg["features"])
assert DEFAULT_CONFIG == snapshot            # global bilkul nahi chhera gaya
print("\nSabaq: shared mutable default state ko har use se pehle deepcopy karo")
print("       (ya behtar: frozen/immutable config + dataclasses.replace).")
"""))

A(code(r"""
# ---------------------------------------------------------------------------
# PROBLEM 3: 50,000 rows memory me rakhni hain. Naive class vs slots + interning
#            se memory kitni bachti hai -- measure karo.
# ---------------------------------------------------------------------------
import sys, tracemalloc

CITIES = ["Lahore", "Karachi", "Islamabad", "Peshawar", "Quetta"]
N = 50_000

class RowDict:                                  # naive: __dict__ + fresh strings
    def __init__(self, rid, city, status):
        self.rid, self.city, self.status = rid, city, status

class RowSlots:                                 # optimized: slots
    __slots__ = ("rid", "city", "status")
    def __init__(self, rid, city, status):
        self.rid, self.city, self.status = rid, city, status

def build(cls, intern_strings):
    rows = []
    for i in range(N):
        city = CITIES[i % len(CITIES)]
        status = "active" if i % 2 else "inactive"
        if intern_strings:
            city, status = sys.intern(city), sys.intern(status)
        rows.append(cls(i, city, status))
    return rows

def peak_mb(cls, intern_strings):
    tracemalloc.start()
    rows = build(cls, intern_strings)
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    n = len(rows)
    del rows
    return round(peak / 1024 / 1024, 2), n

dict_mb, n1 = peak_mb(RowDict, False)
slots_mb, n2 = peak_mb(RowSlots, True)
assert n1 == n2 == N
print(f"{N} rows:")
print("  normal class          :", dict_mb, "MB")
print("  __slots__ + interning :", slots_mb, "MB")
print(f"  bachat                : {round(100 * (1 - slots_mb / dict_mb))}%")
print("\nSabaq: bohat se chhote records ho to __slots__ (ya dataclass(slots=True),")
print("       ya NamedTuple, ya columnar numpy/pandas) sab se bara memory lever hai.")
"""))

A(code(r"""
# ---------------------------------------------------------------------------
# PROBLEM 4: Event system leak. Handlers ne subscribers ko hamesha ke liye pakar
#            liya -> objects kabhi free nahi hue. weakref se fix karo.
# ---------------------------------------------------------------------------
import gc, weakref

class LeakyBus:
    # BUG: strong references -> subscriber kabhi nahi marta
    def __init__(self):
        self.handlers = []
    def subscribe(self, obj):
        self.handlers.append(obj.on_event)   # bound method -> obj ko zinda rakhta hai
    def emit(self, msg):
        return [h(msg) for h in self.handlers]

class SafeBus:
    # FIX: WeakMethod -> subscriber mar jaye to entry khud nikal do
    def __init__(self):
        self._handlers = []
    def subscribe(self, obj):
        self._handlers.append(weakref.WeakMethod(obj.on_event))
    def emit(self, msg):
        out, alive = [], []
        for ref in self._handlers:
            h = ref()                        # None = subscriber mar gaya
            if h is not None:
                out.append(h(msg)); alive.append(ref)
        self._handlers = alive               # dead entries saaf
        return out
    def __len__(self):
        return len(self._handlers)

class Widget:
    def __init__(self, name): self.name = name
    def on_event(self, msg): return f"{self.name}:{msg}"

# --- leaky ---
leaky = LeakyBus()
w = Widget("w1"); leaky.subscribe(w)
watch = weakref.ref(w)
print("leaky emit:", leaky.emit("hello"))
del w; gc.collect()
print("subscriber del ke baad zinda?", watch() is not None, " <- LEAK")

# --- safe ---
safe = SafeBus()
w2 = Widget("w2"); safe.subscribe(w2)
watch2 = weakref.ref(w2)
print("\nsafe emit :", safe.emit("hello"), "| handlers:", len(safe))
del w2; gc.collect()
print("subscriber del ke baad zinda?", watch2() is not None, " <- free ho gaya")
print("emit ke baad handlers count :", safe.emit("again"), len(safe))
print("\nSabaq: long-lived registry (bus/cache/observer) me weakref use karo,")
print("       warna registry hi memory leak ban jaati hai.")
"""))
