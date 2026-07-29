"""Generator: Python/Intermediate/05_Collections_Regex_Datetime_aur_DataFormats.ipynb

Chalao (ROOT se):  python _tools/gen/py_inter_05_collections_regex.py
"""

import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

cells = []
A = cells.append

# =====================================================================
# 1. TITLE
# =====================================================================
A(md(r"""
# 05 - Collections, Regex, Datetime aur Data Formats

**Level:** Intermediate  |  **Track:** Python  |  **Python:** 3.14

Yeh notebook Python ki **"batteries included"** taqat ka dil hai. Jo cheezein
tum haath se `dict`/`list` se banate ho, standard library me unke **fast, tested,
C-level** versions maujood hain. Interview me yahi cheezein ginti hain, aur
production code me yahi din bachati hain.

---

## Is notebook me kya seekhenge

**A. `collections` module (specialised containers)**
- `Counter` - counting ka baadshah: `most_common`, `elements`, `+ - & |`, `update`, `subtract`, `total`
- `defaultdict` - missing key par khud value bana deta hai (`list` / `int` / `set`) + factory gotcha
- `deque` - dono taraf se O(1) push/pop, `rotate`, `maxlen` sliding window, `list` se performance comparison
- `namedtuple` - halka immutable record: `_fields`, `_replace`, `_asdict`, `defaults`
- `OrderedDict` - Python 3.7+ me `dict` ordered hai, phir yeh **kab** kaam aata hai? (`move_to_end`, order-sensitive equality)
- `ChainMap` - config layering (CLI > env > file > defaults) bina merge ke

**B. `heapq` (priority queue / heap)**
- `heappush`, `heappop`, `heapify`, `nlargest`, `nsmallest`, `heapreplace`, `heappushpop`
- min-heap ko max-heap banane ka **negate trick**
- tuple-based priority queue + tie-breaking counter (unorderable items ka hal)

**C. `bisect` (sorted list par binary search)**
- `insort`, `bisect_left` vs `bisect_right`, grade/tax-slab lookup, sorted list maintain karna

**D. `re` - Regular Expressions (deep dive)**
- literals, character classes, predefined classes (`\d \w \s` + negations)
- quantifiers: greedy vs lazy vs possessive
- anchors: `^ $ \b \B`
- groups, non-capturing `(?:...)`, named `(?P<name>...)`, alternation, backreferences
- lookahead / lookbehind (positive + negative)
- flags: `IGNORECASE`, `MULTILINE`, `DOTALL`, `VERBOSE`
- `match` vs `search` vs `fullmatch` vs `findall` vs `finditer` vs `sub` vs `subn` vs `split`
- compiled patterns + speed, **catastrophic backtracking** warning
- real validations: email, Pakistani mobile number, password strength, log parsing, date extraction, HTML-tag caution

**E. `datetime` / `zoneinfo` / `time`**
- `datetime`, `date`, `time`, `timedelta` arithmetic
- `strftime` / `strptime` directive table, ISO parsing
- naive vs timezone-aware, `timezone.utc`, `ZoneInfo("Asia/Karachi")`
- `time.perf_counter`, `time.monotonic`, `time.sleep`
- age / duration calculators

**F. Data formats**
- `json`: `dumps`/`loads`, `indent`, `sort_keys`, `default=`, custom `JSONEncoder`, non-str keys gotcha
- `csv` (via `io.StringIO`): `reader`, `DictReader`, `writer`, `DictWriter`, delimiters, quoting, `newline=''`
- `pickle` vs `json` (**security warning**)
- `base64`: bytes <-> str
- `dataclass` -> `dict` (`dataclasses.asdict`) -> JSON round-trip

**G.** Common Mistakes, 5 Real-World Problems, 6 LeetCode problems, Interview Q&A, Practice Exercises, Cheat-sheet.

---

## Prerequisites
- Python basics: `list`, `dict`, `set`, `tuple`, loops, functions
- Comprehensions aur `lambda`
- Classes ki basic samajh (`dataclass` section ke liye)
- Big-O ki bilkul basic samajh (O(1) vs O(n) vs O(log n))

> **Tip:** har code cell ko khud chalao, values badal kar dekho. Regex sirf parh kar samajh nahi aata - todna parta hai.
"""))

A(code(r"""
# ------------------------------------------------------------------
# Setup cell - poore notebook ke imports yahin, ek dafa.
# (Notebook top-to-bottom chalta hai, is liye pehle imports.)
# ------------------------------------------------------------------
import sys
import re                 # regular expressions
import json               # JSON serialization
import csv                # CSV read/write
import io                 # StringIO - memory me "file"
import base64             # bytes <-> ascii text
import pickle             # Python object serialization (KHATARNAAK - neeche parhna)
import heapq              # heap / priority queue
import bisect             # sorted list par binary search
import random
import tempfile
import os
import textwrap
import time as time_mod   # 'time' naam datetime.time se clash karta hai -> alias

from collections import Counter, defaultdict, deque, namedtuple, OrderedDict, ChainMap
from datetime import datetime, date, time as dtime, timedelta, timezone
from dataclasses import dataclass, field, asdict, fields as dc_fields
from time import perf_counter, monotonic, sleep

random.seed(42)           # deterministic output taake results repeatable hon

print("Python version :", sys.version.split()[0])
print("Imports ready   : collections, heapq, bisect, re, datetime, json, csv, pickle, base64")
"""))

# =====================================================================
# COUNTER
# =====================================================================
A(md(r"""
---

# A1. `Counter` - counting ka baadshah

## Kya hai?
`Counter` ek **`dict` ka subclass** hai jo "cheez -> kitni dafa aayi" store karta hai.
Yani `dict[hashable, int]`, magar bohat si counting-specific superpowers ke sath.

## Kyun / kahan?
- Word frequency, log me status-code counting, votes ginna
- "Top K most frequent" wale sawaal (LeetCode 347, 692 - neeche karenge)
- Anagram check, multiset (bag) arithmetic, inventory add/subtract

## Syntax
```python
from collections import Counter

Counter()                        # khaali
Counter("mississippi")           # iterable se
Counter(["a", "b", "a"])         # list se
Counter({"a": 3, "b": 1})        # mapping se
Counter(a=3, b=1)                # keyword se
```

## Sabse ahem baat (interview me poocha jata hai)
`Counter` me **missing key error nahi deta** - `0` return karta hai:
```python
c = Counter("abc")
c["z"]      # 0  (KeyError NAHI)
```
Lekin dhyan rakho: yeh **key add nahi karta** (`defaultdict` ke bar-aks). Read karne se
`c` me `"z"` shaamil nahi hoga.

## `most_common(n)`
- `n` do to top-n `(element, count)` tuples, **descending count** me
- `n` na do to saare, sorted
- **Ties ka order = insertion order** (Python 3.7+), guaranteed lexicographic nahi.
  Is liye LeetCode 692 (Top K Frequent **Words**) me alag se sorting chahiye hoti hai.
"""))

A(code(r"""
# ------------------------------------------------------------------
# Counter: banane ke tareeqe aur most_common
# ------------------------------------------------------------------
text = "the quick brown fox jumps over the lazy dog the fox barks"
words = text.split()

wc = Counter(words)                 # list of words -> frequency map
print("Counter object :", wc)
print("type           :", type(wc).__mro__[:2])   # dict ka subclass hai
print()

# --- Access -------------------------------------------------------
print("wc['the']      :", wc["the"])        # 3
print("wc['zebra']    :", wc["zebra"])      # 0  <-- KeyError nahi!
print("'zebra' in wc  :", "zebra" in wc)    # False - read karne se key BANI NAHI
print()

# --- most_common --------------------------------------------------
print("top 3          :", wc.most_common(3))
print("sabse kam wala :", wc.most_common()[-1])   # last element = least common
print()

# --- total() (Python 3.10+) : saare counts ka jama --------------
print("total()        :", wc.total(), "| len(words) =", len(words))
assert wc.total() == len(words)      # har word ek dafa gina gaya

# --- character level counting -------------------------------------
cc = Counter("mississippi")
print("char counts    :", cc)
print("i kitni dafa   :", cc["i"])
assert cc["s"] == 4 and cc["i"] == 4 and cc["p"] == 2 and cc["m"] == 1

# --- Anagram check ek line me -------------------------------------
def is_anagram(a: str, b: str) -> bool:
    # Dono strings ke letter-counts barabar hon to anagram hain. O(n) time.
    return Counter(a.replace(" ", "").lower()) == Counter(b.replace(" ", "").lower())

print()
print("anagram 'listen'/'silent' :", is_anagram("listen", "silent"))
print("anagram 'hello'/'world'   :", is_anagram("hello", "world"))
assert is_anagram("Dirty Room", "Dormitory") is True
assert is_anagram("abc", "abd") is False
"""))

A(code(r"""
# ------------------------------------------------------------------
# Counter arithmetic: + - & |   aur   update / subtract / elements
# Counter ko "multiset / bag" samjho.
# ------------------------------------------------------------------
a = Counter(a=4, b=2, c=0, d=-2)
b = Counter(a=1, b=2, c=3, d=4)

print("a =", a)
print("b =", b)
print()

# 1) ADDITION: counts jama; result me sirf POSITIVE counts rehte hain
print("a + b  (jama, non-positive drop)   :", a + b)
#   a:5, b:4, c:3, d:2   -> c=0+3=3 rakha gaya, kuch bhi <=0 nahi bacha

# 2) SUBTRACTION: ghatao; non-positive REMOVE ho jate hain
print("a - b  (ghatao, non-positive drop) :", a - b)
#   a:3 sirf. b:0 -> hata, c:-3 -> hata, d:-6 -> hata

# 3) INTERSECTION (&) : har key ka MINIMUM
print("a & b  (min per key)               :", a & b)

# 4) UNION (|) : har key ka MAXIMUM
print("a | b  (max per key)               :", a | b)
print()

# --- Unary operators (Python 3.3+) --------------------------------
print("+a  (sirf positive counts rakho)   :", +a)   # a=4, b=2
print("-a  (negative ko positive bana do) :", -a)   # d=2
print()

# --- update() vs subtract() : IN-PLACE, aur inhe non-positive se farq nahi ---
stock = Counter(pen=10, book=5)
stock.update(Counter(pen=3, eraser=7))     # jama kar deta hai (dict.update ki tarah REPLACE nahi!)
print("update ke baad  :", stock)          # pen=13, book=5, eraser=7

stock.subtract(Counter(pen=20, book=1))    # ghatata hai, NEGATIVE bhi rehne deta hai
print("subtract ke baad:", stock)          # pen=-7  <-- yeh zinda hai
print("negative stock  :", {k: v for k, v in stock.items() if v < 0})
print()

# GOTCHA: '-' operator negative drop karta hai, .subtract() nahi.
print("operator '-'  :", Counter(pen=10) - Counter(pen=20))     # Counter()  (khaali!)
tmp = Counter(pen=10)
tmp.subtract(Counter(pen=20))
print(".subtract()   :", tmp)                                   # Counter({'pen': -7... }) -> -10
assert (Counter(pen=10) - Counter(pen=20)) == Counter()
assert tmp["pen"] == -10
print()

# --- elements() : counts ko wapas iterable me kholta hai --------
inv = Counter(apple=3, banana=2, cherry=0, rotten=-1)
print("elements()    :", sorted(inv.elements()))
# NOTE: count <= 0 wale elements() me BILKUL nahi aate (cherry, rotten gayab)
assert sorted(inv.elements()) == ["apple", "apple", "apple", "banana", "banana"]

# --- Chhota use-case: weighted random-free "expand" -------------
print("expanded str  :", "".join(sorted(Counter("aaabbc").elements())))
"""))

# =====================================================================
# DEFAULTDICT
# =====================================================================
A(md(r"""
---

# A2. `defaultdict` - missing key par default khud ban jaye

## Kya hai?
`dict` ka subclass jise ek **`default_factory`** (zero-argument callable) diya jata hai.
Jab tum aisi key maango jo maujood nahi, to `defaultdict` `default_factory()` chala kar
value bana deta hai, **key insert kar deta hai**, aur wapas de deta hai.

## Kyun?
Grouping / accumulating code se `if key not in d:` boilerplate hata deta hai.

```python
# Purana tareeqa
groups = {}
for k, v in pairs:
    if k not in groups:
        groups[k] = []
    groups[k].append(v)

# defaultdict
groups = defaultdict(list)
for k, v in pairs:
    groups[k].append(v)      # bas!
```

## Common factories
| Factory | `d[missing]` deta hai | Kab |
|---|---|---|
| `list` | `[]` | grouping / one-to-many |
| `int` | `0` | counting / summing |
| `set` | `set()` | unique members |
| `dict` | `{}` | nested maps |
| `lambda: "N/A"` | `"N/A"` | custom default |
| `lambda: defaultdict(int)` | nested counter | 2-level counting |

## Interview tip
`defaultdict(int)` vs `Counter`: dono counting karte hain, magar `Counter` ke sath
`most_common`, arithmetic, `elements` free milta hai. `defaultdict(int)` general
accumulation (sum of prices, totals) ke liye behtar hai.
"""))

A(code(r"""
# ------------------------------------------------------------------
# defaultdict ke teen sabse common patterns
# ------------------------------------------------------------------
students = [
    ("Lahore", "Ali"), ("Karachi", "Sana"), ("Lahore", "Bilal"),
    ("Islamabad", "Hina"), ("Karachi", "Usman"), ("Lahore", "Ali"),
]

# 1) defaultdict(list) -> GROUPING (one key -> many values)
by_city = defaultdict(list)
for city, name in students:
    by_city[city].append(name)          # no 'if city not in' needed
print("group by city :", dict(by_city))

# 2) defaultdict(int) -> COUNTING / SUMMING
sales = [("pen", 50), ("book", 300), ("pen", 20), ("bag", 900), ("book", 150)]
revenue = defaultdict(int)
for item, amount in sales:
    revenue[item] += amount             # 0 + amount pehli dafa
print("revenue       :", dict(revenue))

# 3) defaultdict(set) -> UNIQUE members (duplicates khud khatam)
unique_by_city = defaultdict(set)
for city, name in students:
    unique_by_city[city].add(name)
print("unique names  :", {k: sorted(v) for k, v in unique_by_city.items()})
print()

# 4) NESTED defaultdict -> 2-level counting (lambda zaroori: factory callable ho)
#    Note: defaultdict(defaultdict(int)) GHALAT hai - woh instance hai, callable nahi.
matrix = defaultdict(lambda: defaultdict(int))
for city, name in students:
    matrix[city][name] += 1
print("nested counts :", {c: dict(v) for c, v in matrix.items()})
print()

# 5) defaultdict se GRAPH (adjacency list) - DSA me roz kaam aata hai
edges = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)]
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)                  # undirected
print("adjacency     :", dict(graph))

assert by_city["Lahore"] == ["Ali", "Bilal", "Ali"]
assert revenue["pen"] == 70
assert unique_by_city["Lahore"] == {"Ali", "Bilal"}
assert graph[4] == [2, 3, 5]
"""))

A(code(r"""
# ------------------------------------------------------------------
# defaultdict ke GOTCHAS - yahan log phaste hain
# ------------------------------------------------------------------

# GOTCHA 1: Sirf PARHNE se bhi key BAN jati hai (silent mutation!)
d = defaultdict(list)
print("shuru me        :", dict(d), "| len =", len(d))
_ = d["ghost"]                       # bas read kiya... par key insert ho gayi
print("read ke baad    :", dict(d), "| len =", len(d))
assert "ghost" in d and d["ghost"] == []

# Bachne ka tareeqa: .get() ya 'in' use karo - yeh factory trigger NAHI karte
d2 = defaultdict(list)
print("d2.get('x')     :", d2.get("x"), "| len =", len(d2))     # None, len 0
print("'x' in d2       :", "x" in d2, "| len =", len(d2))       # False, len 0
assert len(d2) == 0
print()

# GOTCHA 2: default_factory None ho to normal dict jaisa KeyError
d3 = defaultdict()                   # koi factory nahi di
print("default_factory :", d3.default_factory)
try:
    d3["nope"]
except KeyError as e:
    print("KeyError mila   :", e, " <-- factory None hone par yehi hota hai")
print()

# GOTCHA 3: factory zero-argument hona chahiye - key pass nahi hoti
#           "missing key ke hisaab se default" chahiye to __missing__ override karo
class KeyAwareDict(dict):
    def __missing__(self, key):
        # Yahan key available hai - defaultdict me nahi hoti
        value = f"<default for {key}>"
        self[key] = value
        return value

kad = KeyAwareDict()
print("KeyAwareDict    :", kad["speed"])
print()

# GOTCHA 4: defaultdict ko function me pass karna -> caller ka dict bhi mutate hoga
def count_chars(s, sink=None):
    sink = defaultdict(int) if sink is None else sink   # mutable default se bacho
    for ch in s:
        sink[ch] += 1
    return sink
print("count_chars     :", dict(count_chars("banana")))
print()

# GOTCHA 5: JSON / printing ke waqt plain dict me convert karo
nested = defaultdict(lambda: defaultdict(int))
nested["a"]["x"] = 1
try:
    print(json.dumps(nested))        # ye chal jata hai (dict subclass hai)...
except TypeError as e:
    print("json error      :", e)
# ...magar nested lambda factory PICKLE nahi hoti:
try:
    pickle.dumps(nested)
except Exception as e:
    print("pickle error    :", type(e).__name__, "->", e)
    print("Fix             : json/pickle se pehle dict() me convert karo")
"""))

# =====================================================================
# DEQUE
# =====================================================================
A(md(r"""
---

# A3. `deque` - double-ended queue (dono siron par O(1))

## Kya hai?
"Deck" parho (double-ended queue). Yeh ek **doubly-linked list of blocks** hai.
`list` ke bar-aks, `deque` ke **dono** sire O(1) hain.

| Operation | `list` | `deque` |
|---|---|---|
| append right | O(1) amortized | **O(1)** |
| pop right | O(1) | **O(1)** |
| insert at 0 / pop at 0 | **O(n)** (sab shift) | **O(1)** |
| random index `x[i]` | **O(1)** | O(n) (middle me) |
| slicing `x[1:5]` | supported | **NOT supported** |

## Kyun / kahan?
- **Queue / BFS** - `popleft()` bilkul O(1) (`list.pop(0)` O(n) hai)
- **Sliding window** - `maxlen` do, purane khud gir jate hain
- **Undo history / recent-N log** - fixed size buffer
- **Round-robin scheduling** - `rotate()`
- **Palindrome check** - dono siron se compare

## Syntax
```python
deque(iterable=(), maxlen=None)

d.append(x)      d.appendleft(x)
d.pop()          d.popleft()
d.extend(it)     d.extendleft(it)   # extendleft ULTA daalta hai!
d.rotate(n)      # n>0 -> right shift, n<0 -> left shift
d.maxlen         # read-only
```

## Trade-off (interview)
`deque` random access ke liye bura hai (middle element O(n)). Agar tum index se
bohat access karte ho to `list` behtar. Agar dono siron par kaam hai to `deque`.
"""))

A(code(r"""
# ------------------------------------------------------------------
# deque basics
# ------------------------------------------------------------------
dq = deque([2, 3, 4])
print("start          :", dq)

dq.append(5)          # right
dq.appendleft(1)      # left  <-- list me yeh insert(0, x) = O(n) hota
print("after appends  :", dq)

print("pop()          :", dq.pop(), "->", dq)        # right se nikala
print("popleft()      :", dq.popleft(), "->", dq)    # left se nikala
print()

# extend vs extendleft (extendleft REVERSE order me daalta hai - classic gotcha)
d1 = deque([1, 2, 3])
d1.extend([4, 5])
print("extend([4,5])      :", d1)
d2 = deque([1, 2, 3])
d2.extendleft([4, 5])
print("extendleft([4,5])  :", d2, " <-- 5 pehle aaya (ulta!)")
assert list(d2) == [5, 4, 1, 2, 3]
print()

# rotate: circular shift
r = deque([1, 2, 3, 4, 5])
r.rotate(2)      # right shift 2  -> aakhri 2 aage aa gaye
print("rotate(2)      :", r)
r.rotate(-2)     # wapas
print("rotate(-2)     :", r)
assert list(r) == [1, 2, 3, 4, 5]

# rotate ka asli use: round-robin turn
players = deque(["Ali", "Sana", "Bilal"])
for turn in range(4):
    print(f"  turn {turn}: {players[0]} khelega")
    players.rotate(-1)          # left rotate = next player front par
print()

# deque me slicing NAHI hoti - yeh deliberate error demo hai
try:
    _ = dq[0:2]
except TypeError as e:
    print("slicing error  :", e)
    print("Fix            : list(dq)[0:2]  ya  itertools.islice(dq, 0, 2)")
print("workaround     :", list(deque([1, 2, 3, 4]))[0:2])
print()

# Palindrome check dono siron se - deque ka natural fit
def is_palindrome(s: str) -> bool:
    d = deque(ch for ch in s.lower() if ch.isalnum())
    while len(d) > 1:
        if d.popleft() != d.pop():       # dono taraf O(1)
            return False
    return True

print("palindrome 'A man, a plan, a canal: Panama' :", is_palindrome("A man, a plan, a canal: Panama"))
print("palindrome 'hello'                          :", is_palindrome("hello"))
assert is_palindrome("Madam, I'm Adam") is True
assert is_palindrome("python") is False
"""))

A(code(r"""
# ------------------------------------------------------------------
# maxlen: khud-ba-khud bounded buffer (sliding window / recent-N)
# ------------------------------------------------------------------
last3 = deque(maxlen=3)
for x in [10, 20, 30, 40, 50]:
    last3.append(x)
    print(f"append {x:>2} -> {list(last3)}")     # 3 se zyada hote hi left se gir jata hai
assert list(last3) == [30, 40, 50]
print("maxlen         :", last3.maxlen, "(read-only property)")
print()

# maxlen + sliding window average (moving average) - streaming data ka pattern
readings = [12, 15, 11, 20, 25, 22, 30, 28]
window = deque(maxlen=3)
mov_avg = []
for r in readings:
    window.append(r)
    mov_avg.append(round(sum(window) / len(window), 2))
print("readings       :", readings)
print("3-point moving :", mov_avg)
print()

# maxlen + appendleft -> doosri taraf se girta hai
tail = deque(maxlen=3)
for x in "abcde":
    tail.appendleft(x)
print("appendleft w/ maxlen=3 :", list(tail), " <-- right se gira")
assert list(tail) == ["e", "d", "c"]
print()

# ------------------------------------------------------------------
# PERFORMANCE: list.pop(0) vs deque.popleft()  (queue simulation)
# ------------------------------------------------------------------
N = 60_000

lst = list(range(N))
t0 = perf_counter()
while lst:
    lst.pop(0)                  # O(n) har dafa -> total O(n^2)
t_list = perf_counter() - t0

dqq = deque(range(N))
t0 = perf_counter()
while dqq:
    dqq.popleft()               # O(1) har dafa -> total O(n)
t_deque = perf_counter() - t0

print(f"N = {N:,}")
print(f"list.pop(0)      : {t_list*1000:8.2f} ms   (O(n) per op)")
print(f"deque.popleft()  : {t_deque*1000:8.2f} ms   (O(1) per op)")
if t_deque > 0:
    print(f"deque ~{t_list/t_deque:.1f}x tez (machine par number badalta rahega)")
print()
print("Sabaq: BFS / queue / producer-consumer me list.pop(0) NA use karo -> deque use karo.")
"""))

# =====================================================================
# NAMEDTUPLE
# =====================================================================
A(md(r"""
---

# A4. `namedtuple` - halka, immutable, self-documenting record

## Kya hai?
`namedtuple` ek **class factory** hai. Yeh `tuple` ka subclass banata hai jisme
fields ke **naam** hote hain. Memory `tuple` jitni (no `__dict__`), speed `tuple` jitni,
magar readability class jaisi.

```python
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x, p[0]       # dono kaam karte hain
```

## Kyun?
- `row[2]` ki jagah `row.price` - code self-documenting
- Immutable -> hashable -> `dict` key / `set` member ban sakta hai
- Function se multiple values return karne ka saaf tareeqa
- CSV / DB rows ko wrap karne ke liye perfect (memory-friendly)

## Ahem API (sab underscore se shuru - field names se clash na ho)
| Member | Kaam |
|---|---|
| `_fields` | field names ka tuple |
| `_field_defaults` | defaults ka dict |
| `_replace(**kw)` | **naya** object with badli hui values (original safe) |
| `_asdict()` | `dict` me convert (JSON ke liye) |
| `_make(iterable)` | iterable se instance (CSV row -> record) |
| `defaults=` | rightmost fields ke defaults (constructor arg) |

## namedtuple vs dataclass vs dict (interview favourite)
| | `namedtuple` | `dataclass` | `dict` |
|---|---|---|---|
| Mutable | Nahi | Haan (default) | Haan |
| Memory | Sabse kam | Zyada | Sabse zyada |
| Hashable | Haan | `frozen=True` se | Nahi |
| Type hints | `NamedTuple` class se | Built-in | Nahi |
| Unpacking / iteration | Haan | Nahi | keys par |
"""))

A(code(r"""
# ------------------------------------------------------------------
# namedtuple: poora tour
# ------------------------------------------------------------------
# defaults= rightmost fields par lagta hai (yahan: qty=1, discount=0.0)
Product = namedtuple("Product", ["name", "price", "qty", "discount"], defaults=(1, 0.0))

p1 = Product("Laptop", 250000, 2, 0.1)
p2 = Product("Mouse", 1500)                  # qty=1, discount=0.0 default se
print("p1 :", p1)
print("p2 :", p2)
print()

print("_fields          :", Product._fields)
print("_field_defaults  :", Product._field_defaults)
print("name se access   :", p1.name, "| index se:", p1[0], "| dono same:", p1.name == p1[0])
print("unpacking        :", end=" ")
name, price, qty, disc = p1
print(name, price, qty, disc)
print()

# _replace -> NAYA object banata hai (tuple immutable hai, mutate nahi hota)
p3 = p1._replace(qty=5)
print("_replace(qty=5)  :", p3)
print("original safe    :", p1)
assert p1.qty == 2 and p3.qty == 5 and p1 is not p3

# Immutability proof (deliberate error)
try:
    p1.price = 1
except AttributeError as e:
    print("mutate error     :", e, " <-- immutable hai, _replace use karo")
print()

# _asdict -> JSON friendly
print("_asdict()        :", p1._asdict())
print("json             :", json.dumps(p1._asdict()))

# _make -> CSV / DB row se seedha record
raw_rows = [("Keyboard", 4500, 3, 0.05), ("Monitor", 42000, 1, 0.0)]
records = [Product._make(r) for r in raw_rows]
for r in records:
    total = r.price * r.qty * (1 - r.discount)
    print(f"  {r.name:<10} qty={r.qty} total={total:,.2f}")
print()

# Hashable -> set / dict key ban sakta hai (dict nahi ban sakta!)
Point = namedtuple("Point", "x y")           # space-separated string bhi chalti hai
pts = {Point(0, 0), Point(1, 2), Point(0, 0)}
print("set of points    :", sorted(pts))     # duplicate khud khatam
print("dict key         :", {Point(1, 1): "origin-ish"})
assert len(pts) == 2

# GOTCHA: namedtuple == plain tuple compare karta hai (naam ignore hota hai)
print()
print("Point(1,2) == (1,2) :", Point(1, 2) == (1, 2), " <-- True! tuple hi hai")
Other = namedtuple("Other", "x y")
print("Point(1,2) == Other(1,2) :", Point(1, 2) == Other(1, 2), " <-- class farq nahi parta")

# Typed version (behtar - editors autocomplete dete hain)
from typing import NamedTuple
class City(NamedTuple):
    name: str
    population: int
    province: str = "Punjab"      # default

khi = City("Karachi", 15_000_000, "Sindh")
lhr = City("Lahore", 11_000_000)
print()
print("typed NamedTuple :", khi, "|", lhr)
assert lhr.province == "Punjab"
assert isinstance(khi, tuple)
"""))

# =====================================================================
# ORDEREDDICT + CHAINMAP
# =====================================================================
A(md(r"""
---

# A5. `OrderedDict` (ab kab useful?) aur `ChainMap` (config layering)

## `OrderedDict` - Python 3.7 ke baad bhi zaroorat?
Python 3.7+ me **plain `dict` insertion order guarantee karta hai** (3.6 me
implementation detail thi). To phir `OrderedDict` kyun? **4 asli wajhein:**

1. **`move_to_end(key, last=True/False)`** - `dict` me yeh nahi hai. LRU cache ka dil.
2. **`popitem(last=False)`** - `dict` ka `popitem()` sirf last se nikalta hai; `OrderedDict`
   dono taraf se nikal sakta hai (queue-like behaviour).
3. **Order-sensitive equality** - `OrderedDict` ka `==` order dekhta hai, `dict` ka nahi.
   Yeh testing me kaam aata hai jahan order matter karta ho.
4. **Explicit intent / API contract** - code parhne wale ko pata chal jata hai ke
   "order yahan matter karta hai, isse na chhero". Plus `reversed()` `dict` par 3.8+ chalta hai
   magar `OrderedDict` par hamesha chalta tha.

> Interview answer: *"Plain dict ordered hai, is liye zyadatar OrderedDict ki zaroorat khatam.
> Magar `move_to_end`, `popitem(last=False)`, aur order-sensitive equality ke liye ab bhi
> OrderedDict use karta hoon - jaise LRU cache implement karte waqt."*

---

## `ChainMap` - kai dictionaries ka ek "view"

## Kya hai?
`ChainMap(d1, d2, d3)` in dicts ko **copy nahi karta**. Lookup pehle `d1` me,
na mile to `d2` me, phir `d3` me. Pehla match jeetta hai.

## Kyun?
**Config layering** ka textbook use-case:
```
CLI args   (sabse zyada priority)
  -> environment variables
    -> config file
      -> built-in defaults   (sabse kam priority)
```
`{**defaults, **file, **env, **cli}` bhi kaam karta hai, magar woh **copy** banata hai.
`ChainMap`:
- Zero-copy (bara config ho to memory bachti hai)
- **Live** hai - underlying dict badlo to `ChainMap` me nazar aa jayega
- `.maps` list se layers dekh/badal sakte ho
- `.new_child()` se temporary scope (jaise nested function scopes / template context)

## Ahem gotcha
**Writes sirf pehle map (`maps[0]`) par jate hain.** `del` bhi sirf `maps[0]` se hota hai -
peeche wali layer me key ho to `KeyError` milega. `parents` property `maps[1:]` deti hai.
"""))

A(code(r"""
# ------------------------------------------------------------------
# OrderedDict: aaj bhi kaam ki cheezein
# ------------------------------------------------------------------
od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
print("start            :", od)

od.move_to_end("a")                    # 'a' ko aakhir me bhejo
print("move_to_end('a') :", od)
od.move_to_end("c", last=False)        # 'c' ko shuru me bhejo
print("move_to_end('c', last=False):", od)

print("popitem()        :", od.popitem(), "-> ", od)                # last se
print("popitem(last=False):", od.popitem(last=False), "-> ", od)    # first se
print()

# Order-sensitive equality: yahi asli farq hai
d_a, d_b = {"x": 1, "y": 2}, {"y": 2, "x": 1}
o_a, o_b = OrderedDict(d_a), OrderedDict(d_b)
print("dict        {x,y} == {y,x} :", d_a == d_b, " <-- order ignore")
print("OrderedDict {x,y} == {y,x} :", o_a == o_b, " <-- order matters")
assert d_a == d_b
assert o_a != o_b
# NOTE: OrderedDict == plain dict compare order-insensitive rehta hai
print("OrderedDict == dict        :", o_a == d_b, " <-- mixed compare = order ignore")
print()

# Asli use-case: LRU cache (move_to_end + popitem(last=False))
class LRUCache:
    '''Chhota LRU cache. get/put dono O(1). (LeetCode 146 ka core.)'''
    def __init__(self, capacity: int):
        self.cap = capacity
        self.data = OrderedDict()          # front = sabse purana, back = sabse naya

    def get(self, key):
        if key not in self.data:
            return -1
        self.data.move_to_end(key)         # touch -> recent bana do
        return self.data[key]

    def put(self, key, value):
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.cap:
            evicted, _ = self.data.popitem(last=False)   # sabse purana nikalo
            print(f"   (evicted: {evicted})")

cache = LRUCache(2)
cache.put("a", 1); cache.put("b", 2)
print("get a :", cache.get("a"))       # 'a' recent ban gaya
cache.put("c", 3)                      # capacity full -> 'b' evict hoga (a recent hai)
print("keys  :", list(cache.data.keys()))
print("get b :", cache.get("b"))       # -1 (evicted)
assert cache.get("b") == -1 and cache.get("a") == 1
"""))

A(code(r"""
# ------------------------------------------------------------------
# ChainMap: config layering (zero-copy, live)
# ------------------------------------------------------------------
defaults    = {"host": "localhost", "port": 8000, "debug": False, "workers": 1}
config_file = {"host": "db.bizee.internal", "port": 5432}
env_vars    = {"debug": True}
cli_args    = {"port": 9999}

# Priority: cli > env > file > defaults  (pehla map jeetta hai)
cfg = ChainMap(cli_args, env_vars, config_file, defaults)

print("host    :", cfg["host"],    "(config_file se)")
print("port    :", cfg["port"],    "(cli_args se - sabse aage)")
print("debug   :", cfg["debug"],   "(env_vars se)")
print("workers :", cfg["workers"], "(defaults se)")
print("as dict :", dict(cfg))
print("layers  :", len(cfg.maps), "->", cfg.maps)
print()

# LIVE hai: underlying dict badlo, ChainMap me foran nazar aayega
config_file["host"] = "prod.bizee.internal"
print("file badla, cfg['host'] ab :", cfg["host"], " <-- copy nahi, view hai")

# {**a, **b} ka farq: woh SNAPSHOT hai
merged = {**defaults, **config_file, **env_vars, **cli_args}
config_file["host"] = "another.host"
print("merged snapshot host       :", merged["host"], " <-- purana (frozen)")
print("chainmap live host         :", cfg["host"])
print()

# WRITES sirf maps[0] par jate hain
cfg["timeout"] = 30
print("cli_args ab               :", cli_args, " <-- timeout yahan gaya")
assert "timeout" in cli_args and "timeout" not in defaults

# GOTCHA: del sirf maps[0] se hota hai
try:
    del cfg["workers"]                  # 'workers' defaults me hai, maps[0] me nahi
except KeyError as e:
    print("del error                 :", e)
    print("Fix                       : del cfg.maps[3]['workers']  (layer target karo)")
print()

# new_child() -> temporary scope (function-call scope jaisa)
base = ChainMap({"lang": "en"}, {"theme": "dark"})
temp = base.new_child({"lang": "ur"})       # naya khaali/diya hua layer front me
print("base['lang'] :", base["lang"], "| temp['lang'] :", temp["lang"])
print("temp.parents == base layers :", temp.parents.maps == base.maps)
assert temp["theme"] == "dark" and base["lang"] == "en"

# Practical: nested template/variable scopes
scopes = ChainMap({}, {"user": "guest"}, {"user": "anon", "role": "reader"})
scopes["user"] = "imran"                    # innermost scope me likha
print("resolved     :", dict(scopes))
assert scopes["user"] == "imran" and scopes["role"] == "reader"
"""))

# =====================================================================
# HEAPQ
# =====================================================================
A(md(r"""
---

# B. `heapq` - priority queue / binary heap

## Kya hai?
`heapq` ek **min-heap** hai jo **plain `list` par** kaam karta hai (koi alag class nahi).
Invariant: `heap[k] <= heap[2*k+1]` aur `heap[k] <= heap[2*k+2]`.
Matlab **`heap[0]` hamesha sabse chhota element hai** - O(1) me.

> **Bara gotcha:** heap **sorted list nahi hai**. Sirf root minimum guaranteed hai.
> `print(heap)` karo to andar ka order "random" lagega - yeh normal hai.

## Complexity
| Operation | Time |
|---|---|
| `heap[0]` (peek min) | **O(1)** |
| `heappush(h, x)` | O(log n) |
| `heappop(h)` | O(log n) |
| `heapify(list)` | **O(n)** (sorting O(n log n) se tez!) |
| `heapreplace(h, x)` | O(log n) - **ek** sift, do se sasta |
| `nlargest(k, it)` / `nsmallest(k, it)` | O(n log k) |

## Kab heap, kab sorting?
- Poora order chahiye -> `sorted()`
- Sirf **top-k** ya **repeatedly minimum nikalna** -> heap
- Stream aa rahi hai (data khatam nahi hota) -> heap of size k

## Kyun / kahan (real world)
- Task scheduler (next-deadline-first)
- Dijkstra / A* shortest path
- Merge K sorted streams (`heapq.merge`)
- Top-K trending items
- Median maintain karna (two heaps)
"""))

A(code(r"""
# ------------------------------------------------------------------
# heapq basics: heappush / heappop / heapify / peek
# ------------------------------------------------------------------
h = []
for x in [5, 1, 8, 3, 9, 2]:
    heapq.heappush(h, x)
    print(f"push {x} -> {h}   (heap[0] = {h[0]})")
print()
print("Dhyan do: list SORTED nahi hai, sirf h[0] minimum hai.")
print("is_sorted?", h == sorted(h))
print()

print("pops (sorted order me nikalte hain):", end=" ")
out = []
while h:
    out.append(heapq.heappop(h))
print(out)
assert out == sorted([5, 1, 8, 3, 9, 2])
print()

# heapify: MOJOODA list ko in-place heap banata hai - O(n), sorting se tez
data = [9, 4, 7, 1, 8, 2, 6]
heapq.heapify(data)                 # in-place, return None
print("heapify ke baad :", data, "| min =", data[0])
assert data[0] == 1

# Heapsort (naive) - sirf samajhne ke liye; asal me sorted() use karo
def heapsort(iterable):
    h = list(iterable)
    heapq.heapify(h)                          # O(n)
    return [heapq.heappop(h) for _ in range(len(h))]   # n x O(log n)

print("heapsort        :", heapsort([3, 1, 4, 1, 5, 9, 2, 6]))
assert heapsort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]
print()

# Khaali heap se pop -> IndexError (deliberate error demo)
try:
    heapq.heappop([])
except IndexError as e:
    print("empty pop error :", type(e).__name__, "->", e)
    print("Fix             : 'if heap:' check karo ya try/except lagao")
"""))

A(code(r"""
# ------------------------------------------------------------------
# nlargest / nsmallest / heapreplace / heappushpop
# ------------------------------------------------------------------
scores = [88, 45, 92, 67, 100, 23, 76, 95, 51]

print("nlargest(3)   :", heapq.nlargest(3, scores))
print("nsmallest(3)  :", heapq.nsmallest(3, scores))
print()

# key= support - dict/object list par direct chalta hai
employees = [
    {"name": "Ali",   "salary": 120000},
    {"name": "Sana",  "salary": 180000},
    {"name": "Bilal", "salary": 95000},
    {"name": "Hina",  "salary": 210000},
]
top2 = heapq.nlargest(2, employees, key=lambda e: e["salary"])
print("top 2 salaries:", [(e["name"], e["salary"]) for e in top2])
assert [e["name"] for e in top2] == ["Hina", "Sana"]
print()
print("Rule of thumb:")
print("  k == 1        -> min()/max() use karo (tez tareen)")
print("  k ~ n         -> sorted()[:k] use karo")
print("  1 << k << n   -> nlargest/nsmallest (O(n log k))")
print()

# ---- heapreplace: POP pehle, PUSH baad me (size same rehta hai) ----
hr = [1, 3, 5, 7]
heapq.heapify(hr)
popped = heapq.heapreplace(hr, 4)      # 1 nikla, 4 andar aaya
print("heapreplace(h, 4) -> popped:", popped, "| heap:", sorted(hr))
assert popped == 1

# ---- heappushpop: PUSH pehle, POP baad me ----
hp = [1, 3, 5, 7]
heapq.heapify(hp)
popped2 = heapq.heappushpop(hp, 0)     # 0 push hua, phir min pop -> 0 hi wapas
print("heappushpop(h, 0) -> popped:", popped2, "| heap:", sorted(hp))
assert popped2 == 0                    # naya element hi sabse chhota tha
print()
print("Farq yaad rakho:")
print("  heapreplace  = pop THEN push  -> naya element us round me pop NAHI ho sakta")
print("  heappushpop  = push THEN pop  -> naya element wapas aa sakta hai")
print("  heapreplace khaali heap par IndexError deta hai, heappushpop nahi.")
print()

# 'top k of a stream' pattern - heap size k se zyada nahi barhne dete (memory O(k))
def top_k_stream(stream, k):
    h = []                                  # min-heap of size k
    for x in stream:
        if len(h) < k:
            heapq.heappush(h, x)
        elif x > h[0]:                      # naya element sabse chhote se bara hai?
            heapq.heapreplace(h, x)         # chhota nikalo, naya daalo (1 sift)
    return sorted(h, reverse=True)

print("top 3 of stream:", top_k_stream(scores, 3))
assert top_k_stream(scores, 3) == [100, 95, 92]

# heapq.merge - kai sorted iterables ko lazily merge karta hai (memory friendly)
a, b, c = [1, 4, 7], [2, 5, 8], [3, 6, 9]
print("heapq.merge    :", list(heapq.merge(a, b, c)))
"""))

A(md(r"""
## B2. Min-heap ko max-heap banana + Priority Queue

### `heapq` sirf min-heap hai. Max-heap chahiye to?
**Trick: values negate kar do.** `-x` ka minimum = `x` ka maximum.

```python
h = [-x for x in nums]
heapq.heapify(h)
largest = -heapq.heappop(h)      # wapas nikaalte waqt phir negate
```
- Sirf **numbers** ke liye chalta hai (string negate nahi hoti).
- Strings/objects ke liye `key`-based wrapper class ya `nlargest` use karo.
- `_heapify_max` / `_heappop_max` **private** hain - production me na use karo.

### Priority Queue tuples se
`heapq` tuples ko **lexicographically** compare karta hai: pehle `[0]`, tie ho to `[1]`, aage.

```python
heapq.heappush(pq, (priority, task))
```

**Do bare gotchas:**
1. **Tie par `task` compare hoga.** Agar task `dict` ya custom object hai to
   `TypeError: '<' not supported` aayega. **Fix:** ek monotonically increasing
   `counter` beech me daalo: `(priority, counter, task)`. Yeh FIFO tie-break bhi de deta hai (stable).
2. **Priority `0` ya negative** bilkul theek hai - `heapq` sirf compare karta hai.

Interview me `queue.PriorityQueue` ka zikar bhi karo: woh thread-safe wrapper hai
`heapq` ke oopar, magar locking ki wajah se single-thread me `heapq` tez hai.
"""))

A(code(r"""
# ------------------------------------------------------------------
# Max-heap trick + Priority Queue with tie-breaking counter
# ------------------------------------------------------------------
nums = [5, 1, 8, 3, 9, 2]

# MAX-HEAP via negation
mx = [-x for x in nums]
heapq.heapify(mx)
print("max-heap pops :", [-heapq.heappop(mx) for _ in range(len(mx))])
assert sorted(nums, reverse=True) == [9, 8, 5, 3, 2, 1]
print()

# ------------------------------------------------------------------
# GOTCHA: tuple tie par second element compare hota hai
# ------------------------------------------------------------------
pq_bad = []
heapq.heappush(pq_bad, (1, {"task": "email"}))
try:
    heapq.heappush(pq_bad, (1, {"task": "sms"}))   # same priority -> dict vs dict compare
except TypeError as e:
    print("tie error     :", e)
    print("Fix           : (priority, counter, item) - counter se tie hamesha toot jata hai")
print()

# ------------------------------------------------------------------
# Sahi Priority Queue: counter se stable FIFO tie-breaking
# ------------------------------------------------------------------
import itertools

class PriorityQueue:
    '''Min-heap based PQ. Chhoti priority = pehle nikle. Ties FIFO order me.'''
    def __init__(self):
        self._heap = []
        self._counter = itertools.count()      # 0,1,2,... hamesha unique & increasing

    def push(self, item, priority):
        # counter beech me: priority tie ho to insertion order faisla karta hai
        heapq.heappush(self._heap, (priority, next(self._counter), item))

    def pop(self):
        if not self._heap:
            raise IndexError("pop from empty PriorityQueue")
        priority, _, item = heapq.heappop(self._heap)
        return item, priority

    def peek(self):
        return (self._heap[0][2], self._heap[0][0]) if self._heap else None

    def __len__(self):
        return len(self._heap)

pq = PriorityQueue()
pq.push({"task": "deploy"},        priority=2)
pq.push({"task": "fix-prod-bug"},  priority=1)
pq.push({"task": "write-tests"},   priority=2)   # 'deploy' ke sath tie
pq.push({"task": "reply-email"},   priority=5)
pq.push({"task": "server-down"},   priority=0)   # sabse urgent

print("peek          :", pq.peek())
print("drain order:")
order = []
while len(pq):
    item, prio = pq.pop()
    order.append(item["task"])
    print(f"  p={prio}  {item['task']}")

# 'deploy' 'write-tests' se pehle push hua tha -> tie me pehle nikla (stable)
assert order == ["server-down", "fix-prod-bug", "deploy", "write-tests", "reply-email"]
print()

# Max-priority chahiye (bara number = zyada urgent)? -> priority negate karo
pq2 = PriorityQueue()
for task, importance in [("low", 1), ("critical", 10), ("medium", 5)]:
    pq2.push(task, -importance)              # negate = max-heap behaviour
print("max-priority order:", [pq2.pop()[0] for _ in range(3)])
"""))

# =====================================================================
# BISECT
# =====================================================================
A(md(r"""
---

# C. `bisect` - sorted list par binary search (C speed)

## Kya hai?
`bisect` ek **already sorted** list me binary search karta hai: O(log n).
Yeh khud sort nahi karta - **tumhari zimmedari hai list sorted rakhna**.

## Do bunyadi functions
| Function | Kya deta hai | Duplicates ke sath |
|---|---|---|
| `bisect_left(a, x)` | pehla index jahan `x` daala ja sakta hai | `x` ke **barabar walon se PEHLE** |
| `bisect_right(a, x)` / `bisect(a, x)` | aakhri aisa index | `x` ke barabar walon ke **BAAD** |

`a = [1, 2, 2, 2, 5]`, `x = 2`:
- `bisect_left  -> 1` (pehle 2 ki jagah)
- `bisect_right -> 4` (aakhri 2 ke baad)
- `bisect_right - bisect_left = 3` = **`x` ki count** (O(log n) me!)

## Insert helpers
- `insort_left(a, x)` / `insort_right(a, x)` = search **+** `a.insert(...)`
- **Search O(log n), magar insert O(n)** (elements shift hote hain) -> total O(n).
  Bohat inserts ho to `list.append` + ek dafa `sort()`, ya `SortedList` (third-party) socho.

## `key=` support (Python 3.10+)
`bisect_left(records, target, key=lambda r: r.score)` - list `key` ke hisaab se sorted ho.

## Kahan use hota hai
- **Grade / tax-slab / shipping-rate lookup** (range mapping, `if/elif` chain ki jagah)
- Leaderboard rank nikalna
- Sorted timestamps me "is waqt se pehle kitne events" (prefix count)
- LIS (Longest Increasing Subsequence) O(n log n)
- Weighted random selection (cumulative weights)
"""))

A(code(r"""
# ------------------------------------------------------------------
# bisect: left vs right, insort, aur classic lookups
# ------------------------------------------------------------------
a = [1, 2, 2, 2, 5, 8]
print("list          :", a)
print("bisect_left (a, 2) :", bisect.bisect_left(a, 2),  " <- pehle 2 ki jagah")
print("bisect_right(a, 2) :", bisect.bisect_right(a, 2), " <- aakhri 2 ke baad")
print("count of 2         :", bisect.bisect_right(a, 2) - bisect.bisect_left(a, 2))
assert bisect.bisect_left(a, 2) == 1
assert bisect.bisect_right(a, 2) == 4
assert bisect.bisect_right(a, 2) - bisect.bisect_left(a, 2) == a.count(2)

# Maujood na hone wali value: dono same index dete hain (insert position)
print("bisect_left (a, 4) :", bisect.bisect_left(a, 4), "| bisect_right:", bisect.bisect_right(a, 4))
print()

# ---- 'exists?' check bisect se (binary search) ----
def contains(sorted_list, x) -> bool:
    i = bisect.bisect_left(sorted_list, x)
    return i < len(sorted_list) and sorted_list[i] == x

print("contains(a, 5) :", contains(a, 5), "| contains(a, 4):", contains(a, 4))
assert contains(a, 8) and not contains(a, 7)
print()

# ---- insort: sorted list maintain karna ----
sorted_scores = []
for s in [55, 91, 72, 12, 88, 72]:
    bisect.insort(sorted_scores, s)          # = insort_right
    print(f"insort {s:>2} -> {sorted_scores}")
assert sorted_scores == sorted(sorted_scores)
print()

# ---- GRADE LOOKUP: if/elif chain ki jagah bisect ----
# breakpoints: 60, 70, 80, 90   grades: F  D  C  B  A
BREAKS = [60, 70, 80, 90]
GRADES = "FDCBA"

def grade(score: int) -> str:
    # bisect_right: 90 -> index 4 -> 'A' (yani 90 bhi A hai, inclusive lower bound)
    return GRADES[bisect.bisect_right(BREAKS, score)]

for s in [0, 59, 60, 69, 70, 79, 85, 89, 90, 100]:
    print(f"  score {s:>3} -> {grade(s)}")
assert grade(59) == "F" and grade(60) == "D" and grade(90) == "A" and grade(100) == "A"
print()

# ---- TAX SLAB (Pakistan-style illustrative slabs) ----
SLAB_LIMITS = [600_000, 1_200_000, 2_400_000, 3_600_000]
SLAB_RATES  = [0.0,     0.025,     0.125,     0.20,      0.25]

def tax_rate(income: int) -> float:
    return SLAB_RATES[bisect.bisect_right(SLAB_LIMITS, income)]

for inc in [500_000, 600_000, 900_000, 2_000_000, 5_000_000]:
    print(f"  income {inc:>9,} -> rate {tax_rate(inc):.1%}")
assert tax_rate(500_000) == 0.0 and tax_rate(5_000_000) == 0.25
print()

# ---- key= (Python 3.10+): objects par bisect ----
Rec = namedtuple("Rec", "name score")
recs = [Rec("Ali", 40), Rec("Sana", 65), Rec("Bilal", 80), Rec("Hina", 95)]   # score se sorted
idx = bisect.bisect_left(recs, 70, key=lambda r: r.score)
print("pehla record with score >= 70 :", recs[idx])
assert recs[idx].name == "Bilal"
print()

# ---- GOTCHA: unsorted list par bisect = bakwaas jawab (koi error NAHI) ----
bad = [5, 1, 9, 3]
print("unsorted par bisect_left(bad, 3):", bisect.bisect_left(bad, 3), " <-- silently GHALAT")
print("Sabaq: bisect use karne se pehle list sorted honi CHAHIYE.")
"""))

# =====================================================================
# REGEX
# =====================================================================
A(md(r"""
---

# D. `re` - Regular Expressions (deep dive)

## Kya hai?
Regex ek chhoti si **pattern language** hai text search/validate/replace ke liye.
Python me `re` module. Engine **backtracking** based hai (NFA) - is liye taqatwar hai
magar khatarnaak bhi (neeche "catastrophic backtracking" parhna).

## Pehla aur sabse ahem rule: **raw strings use karo**
```python
re.search("\\d+", s)     # bura: Python pehle "\\d" ko process karta hai
re.search(r"\d+", s)     # SAHI: r"" me backslash jaisa hai waisa engine tak jata hai
```
`"\b"` Python me **backspace character** (0x08) hai, regex ka word-boundary NAHI.
`r"\b"` sahi hai. **Hamesha `r""` likho** - koi exception nahi.

---

## D1. Literals aur character classes

| Pattern | Matlab |
|---|---|
| `abc` | literal "abc" |
| `.` | koi bhi ek character **siwa newline** (`DOTALL` se newline bhi) |
| `[aeiou]` | in me se koi ek (character class / set) |
| `[a-z]` | range: a se z |
| `[a-zA-Z0-9_]` | multiple ranges jama |
| `[^abc]` | **negated**: a, b, c ke ilawa kuch bhi |
| `[.]` ya `\.` | literal dot (class ke andar `.` special nahi) |
| `a\|b` | alternation: `a` ya `b` |

**Class ke andar ke rules (log yahan galti karte hain):**
- Andar `.` `*` `+` `(` `)` `?` special **nahi** hote: `[.*+]` teen literal chars hain.
- `-` ko literal chahiye to shuru/aakhir me rakho (`[-a-z]` ya `[a-z-]`) ya escape (`[a\-z]`).
- `^` sirf **pehli position** par negation hai: `[a^b]` me `^` literal hai.
- `]` ko literal chahiye to pehle rakho ya escape: `[]a]` / `[\]a]`.

## D2. Predefined (shorthand) classes

| Shorthand | Barabar | Negation |
|---|---|---|
| `\d` | `[0-9]` (+ Unicode digits!) | `\D` = non-digit |
| `\w` | `[a-zA-Z0-9_]` (+ Unicode letters) | `\W` = non-word |
| `\s` | `[ \t\n\r\f\v]` | `\S` = non-space |

**Unicode gotcha:** default me `str` patterns **Unicode-aware** hote hain. `\d` Arabic-Indic
digits (`٣`) aur `\w` Urdu/Chinese letters bhi match karta hai. Sirf ASCII chahiye to
`re.ASCII` flag do ya `[0-9]` / `[a-zA-Z0-9_]` explicit likho.
"""))

A(code(r"""
# ------------------------------------------------------------------
# Literals, character classes, predefined classes
# ------------------------------------------------------------------
s = "Order #A-42 shipped to Lahore on 2024-03-15 for Rs. 15,000."

print("literal 'Lahore' :", re.search(r"Lahore", s))          # Match object ya None
print("dot '.' (any)    :", re.findall(r"L.h", s))            # L + koi 1 char + h
print("vowels           :", re.findall(r"[aeiou]", s)[:8], "...")
print("digit runs       :", re.findall(r"[0-9]+", s))
print("NOT digit/space  :", re.findall(r"[^0-9\s]+", s)[:5], "...")
print()

# Class ke andar special chars literal ho jate hain
print(r"[.*+] literal    :", re.findall(r"[.*+]", "a.b*c+d"))
print(r"escaped \. dot   :", re.findall(r"\.", s))
print(r"[-+] dash first  :", re.findall(r"[-+]", "a-b+c"))     # '-' shuru me = literal
print(r"[a^b] caret mid  :", re.findall(r"[a^b]", "a^b"))      # '^' beech me = literal
print()

# --- Predefined classes ---
line = "Ali_123 scored 87% on 2024-05-01\tGrade: A+"
print(r"\d+  :", re.findall(r"\d+", line))
print(r"\D+  :", re.findall(r"\D+", line)[:3], "...")
print(r"\w+  :", re.findall(r"\w+", line))
print(r"\W+  :", re.findall(r"\W+", line))
print(r"\s+  :", re.findall(r"\s+", line))       # space aur tab
print(r"\S+  :", re.findall(r"\S+", line))
print()

# --- UNICODE gotcha ---
mixed = "abc ٣٤ 123 اردو"       # arabic digits + urdu word
print("unicode-aware \\d :", re.findall(r"\d+", mixed))        # arabic digits BHI aaye
print("ASCII flag    \\d :", re.findall(r"\d+", mixed, re.ASCII))
print("unicode-aware \\w :", re.findall(r"\w+", mixed))        # urdu word bhi \w hai
print("ASCII flag    \\w :", re.findall(r"\w+", mixed, re.ASCII))
assert re.findall(r"\d+", mixed, re.ASCII) == ["123"]
print()

# --- re.escape: user input ko literal banane ka SAHI tareeqa ---
user_typed = "price (Rs.) +tax?"
print("raw pattern se search karna crash/ghalat de sakta hai; re.escape use karo:")
print("escaped :", re.escape(user_typed))
print("found   :", re.search(re.escape(user_typed), f"Column: {user_typed} here") is not None)
try:
    re.compile(user_typed)                # unbalanced paren ho to error
except re.error as e:
    print("re.error:", e)
"""))

A(md(r"""
## D3. Quantifiers - greedy vs lazy vs possessive

| Quantifier | Matlab |
|---|---|
| `*` | 0 ya zyada |
| `+` | 1 ya zyada |
| `?` | 0 ya 1 (optional) |
| `{n}` | exactly n |
| `{n,}` | n ya zyada |
| `{,m}` | 0 se m tak |
| `{n,m}` | n se m tak |

Har quantifier ke **teen mode** hain:

| Mode | Likhne ka tareeqa | Behaviour | Backtrack? |
|---|---|---|---|
| **Greedy** (default) | `.*` `a+` `\d{2,5}` | **max** lo, phir zaroorat par peeche hato | Haan |
| **Lazy / non-greedy** | `.*?` `a+?` `\d{2,5}?` | **min** lo, phir zaroorat par aage barho | Haan |
| **Possessive** (3.11+) | `.*+` `a++` `\d{2,5}+` | max lo aur **kabhi peeche na hato** | **Nahi** |

Possessive ka bhai: **atomic group** `(?>...)` (bhi 3.11+). Dono backtracking band kar
dete hain -> catastrophic backtracking se bachao, aur tez.

### Classic example
Text: `<b>bold</b> and <i>italic</i>`
- `<.*>`  -> **poora** `<b>bold</b> and <i>italic</i>` (greedy!)
- `<.*?>` -> `<b>` (lazy - sirf pehla tag)
- `<[^>]*>` -> `<b>` (**behtar tareeqa** - lazy se bhi tez, kyunki backtracking nahi)

> **Interview line:** *"Greedy `.*` pehle poora line kha jata hai, phir peeche hat kar
> match banata hai. Lazy `.*?` ulta karta hai. Magar best practice negated class
> (`[^>]*`) hai kyunki woh deterministic hai - backtracking hi nahi hoti."*

---

## D4. Anchors - position match karte hain, character nahi

| Anchor | Matlab |
|---|---|
| `^` | string ka shuru (`MULTILINE` me har line ka shuru) |
| `$` | string ka aakhir, **ya aakhri `\n` se pehle** (`MULTILINE` me har line ka aakhir) |
| `\A` | string ka shuru - `MULTILINE` se **kabhi** affect nahi hota |
| `\Z` | string ka bilkul aakhir - trailing newline ki koi rehmat nahi |
| `\b` | word boundary (`\w` aur non-`\w` ke darmiyan) |
| `\B` | **non**-boundary (word ke andar) |

**`$` ka bara gotcha:** `re.search(r"abc$", "abc\n")` **match karta hai!**
Bilkul strict chahiye to `\Z` use karo.

Anchors **zero-width** hain - koi character consume nahi karte.
"""))

A(code(r"""
# ------------------------------------------------------------------
# Greedy vs Lazy vs Possessive
# ------------------------------------------------------------------
html = "<b>bold</b> and <i>italic</i>"

print("GREEDY <.*>     :", re.findall(r"<.*>", html))
print("LAZY   <.*?>    :", re.findall(r"<.*?>", html))
print("BEST   <[^>]*>  :", re.findall(r"<[^>]*>", html))
assert re.findall(r"<.*>", html) == [html]                       # poora string!
assert re.findall(r"<.*?>", html) == ["<b>", "</b>", "<i>", "</i>"]
print()

# Number example: greedy peeche hat kar match banata hai
num = "12345"
print("greedy \\d{2,4}   :", re.match(r"\d{2,4}", num).group())       # '1234' (max)
print("lazy   \\d{2,4}?  :", re.match(r"\d{2,4}?", num).group())      # '12'   (min)
print()

# Greedy backtracking ka nazara: \d+ ko aakhri digit chhorni parti hai
m = re.match(r"(\d+)(\d)", "12345")
print(r"(\d+)(\d) on 12345 -> group1 =", m.group(1), ", group2 =", m.group(2))
print("   \\d+ ne pehle 12345 liya, phir peeche hat kar 1234 par aaya (backtrack)")
print()

# POSSESSIVE / ATOMIC (Python 3.11+) - backtrack karne se INKAR
try:
    print(r"possessive (\d++)(\d) :", re.match(r"(\d++)(\d)", "12345"))
    print("   None mila -> \\d++ ne 12345 poora le liya aur peeche NAHI hata,")
    print("   is liye doosre (\\d) ke liye kuch na bacha -> fail.")
    print(r"atomic     (?>\d+)\d  :", re.match(r"(?>\d+)\d", "12345"))
    print(r"possessive .*+ alone  :", re.fullmatch(r"\d*+", "999"))
except re.error as e:
    print("Possessive/atomic support nahi (Python < 3.11):", e)
print()

# {n,m} ke saare roop
for pat in [r"^a{3}$", r"^a{2,}$", r"^a{,2}$", r"^a{2,4}$"]:
    results = {t: bool(re.match(pat, t)) for t in ["a", "aa", "aaa", "aaaaa"]}
    print(f"  {pat:<10} -> {results}")
print()

# GOTCHA: '?' ke do bilkul alag kaam
print("optional '?'  colou?r :", re.findall(r"colou?r", "color and colour"))
print("lazy     '?'  o+?     :", re.match(r"o+?", "ooo").group(), "(sirf 1)")
"""))

A(code(r"""
# ------------------------------------------------------------------
# Anchors: ^ $ \A \Z \b \B
# ------------------------------------------------------------------
text = "cat catalog concat the cat sat"

print("plain  'cat'  :", len(re.findall(r"cat", text)), "matches (catalog/concat bhi)")
print(r"\bcat\b      :", re.findall(r"\bcat\b", text), "<- poora word 'cat' sirf")
print(r"\bcat        :", re.findall(r"\bcat\w*", text), "<- 'cat' se SHURU hone wale")
print(r"cat\b        :", re.findall(r"\w*cat\b", text), "<- 'cat' par KHATAM hone wale")
print(r"\Bcat        :", re.findall(r"\Bcat\w*", text), "<- word ke ANDAR (boundary nahi)")
assert re.findall(r"\bcat\b", text) == ["cat", "cat"]
print()

# ^ aur $ (single line)
print("^cat  :", bool(re.search(r"^cat", text)))
print("sat$  :", bool(re.search(r"sat$", text)))
print()

# ---- $ ka bara GOTCHA: trailing newline ----
print(r"re.search(r'abc$',  'abc\n') :", bool(re.search(r"abc$", "abc\n")),  " <-- TRUE! surprise")
print(r"re.search(r'abc\Z', 'abc\n') :", bool(re.search(r"abc\Z", "abc\n")), " <-- strict")
print(r"re.fullmatch(r'abc','abc\n') :", bool(re.fullmatch(r"abc", "abc\n")))
assert re.search(r"abc$", "abc\n") is not None
assert re.search(r"abc\Z", "abc\n") is None
print()

# ---- MULTILINE me ^ $ per-line ban jate hain, \A \Z nahi ----
log = "line one\nline two\nline three"
print("^line  (no flag)  :", len(re.findall(r"^line", log)), "match")
print("^line  (MULTILINE):", len(re.findall(r"^line", log, re.M)), "matches")
print(r"\Aline (MULTILINE):", len(re.findall(r"\Aline", log, re.M)), "match  <-- flag ka asar nahi")
assert len(re.findall(r"^line", log, re.M)) == 3
assert len(re.findall(r"\Aline", log, re.M)) == 1
print()

# \b ki definition Unicode/underscore par surprise deti hai
print(r"\bfoo\b in 'foo_bar' :", bool(re.search(r"\bfoo\b", "foo_bar")), " <-- False, '_' word-char hai")
print(r"\bfoo\b in 'foo-bar' :", bool(re.search(r"\bfoo\b", "foo-bar")), " <-- True, '-' non-word")

# Practical: whole-word replace (naive replace se behtar)
sentence = "I like Java. Javascript is not Java."
print()
print("str.replace :", sentence.replace("Java", "Python"))       # Javascript bhi bigar gaya!
print("regex \\b    :", re.sub(r"\bJava\b", "Python", sentence))  # sahi
assert re.sub(r"\bJava\b", "Python", sentence) == "I like Python. Javascript is not Python."
"""))

A(md(r"""
## D5. Groups, non-capturing, named groups, alternation, backreferences, lookaround

### Groups `( ... )`
- Sub-pattern ko **capture** karte hain -> `m.group(1)`, `m.groups()`
- Quantifier ka scope banate hain: `(ab)+` = "ab" repeat, `ab+` = "ab", "abb", ...
- `findall` **groups return karta hai**, poora match nahi - classic surprise!

### Non-capturing `(?: ... )`
Grouping chahiye magar capture nahi -> tez, saaf, aur group numbers shift nahi hote.
```python
r"(?:Mr|Mrs|Ms)\. (\w+)"      # title group nahi, naam group 1
```

### Named groups `(?P<name> ... )`
```python
m = re.match(r"(?P<y>\d{4})-(?P<m>\d{2})", "2024-03")
m.group("y"), m.groupdict()      # '2024', {'y': '2024', 'm': '03'}
```
Backreference: `(?P=name)` pattern me, `\g<name>` replacement me.
**Named groups log-parsing ke liye best hain** - `group(7)` yaad rakhne se bachao.

### Alternation `|`
- **Left-to-right, pehla jo match kar jaye** (longest nahi!). `r"a|ab"` par "ab" -> `"a"` milega.
- Scope poore pattern par hota hai -> `(?:...)` se ghero: `r"^(?:cat|dog)$"`, na ke `r"^cat|dog$"`.
- Zyada specific alternative pehle likho: `r"\b(?:Javascript|Java)\b"`.

### Backreferences `\1`, `\2`, `(?P=name)`
Pehle capture ki hui **exact same text** dobara match karo:
- `r"\b(\w+) \1\b"` -> duplicate word ("the the")
- `r"(['\"]).*?\1"` -> matching quotes
- `re.sub(r"(\w+)@(\w+)", r"\2 at \1", s)` -> replacement me `\1` `\2`

### Lookaround (zero-width assertions)
| Syntax | Naam | Matlab |
|---|---|---|
| `(?=...)` | positive lookahead | aage yeh hona chahiye (consume nahi) |
| `(?!...)` | negative lookahead | aage yeh **na** ho |
| `(?<=...)` | positive lookbehind | peeche yeh hona chahiye |
| `(?<!...)` | negative lookbehind | peeche yeh **na** ho |

**Python ki lookbehind fixed-width honi chahiye:** `(?<=abc)` theek, `(?<=a+)` **error**.
(Workaround: `(?<=aa|bb)` same length alternatives, ya text ulta karo.)

Lookarounds "AND conditions" lagane ke liye best hain - password strength ka classic pattern.
"""))

A(code(r"""
# ------------------------------------------------------------------
# Groups, non-capturing, named groups, alternation
# ------------------------------------------------------------------
m = re.match(r"(\d{4})-(\d{2})-(\d{2})", "2024-03-15")
print("group(0) poora  :", m.group(0))
print("group(1..3)     :", m.group(1), m.group(2), m.group(3))
print("groups()        :", m.groups())
print("group(1,3) tuple:", m.group(1, 3))
print("span(2)         :", m.span(2), "| start/end:", m.start(2), m.end(2))
print()

# findall ka SURPRISE: groups hon to groups milte hain
print("findall no group :", re.findall(r"\d{4}-\d{2}-\d{2}", "2024-03-15 and 2025-01-01"))
print("findall 1 group  :", re.findall(r"(\d{4})-\d{2}-\d{2}", "2024-03-15 and 2025-01-01"))
print("findall 3 groups :", re.findall(r"(\d{4})-(\d{2})-(\d{2})", "2024-03-15 and 2025-01-01"))
print("Fix (poora match chahiye) -> (?:...) non-capturing use karo:")
print("  ", re.findall(r"(?:\d{4})-(?:\d{2})-(?:\d{2})", "2024-03-15 and 2025-01-01"))
print()

# Group + quantifier scope
print("(ab)+ on 'ababab' :", re.match(r"(ab)+", "ababab").group(0), "| last capture:", re.match(r"(ab)+", "ababab").group(1))
print("ab+   on 'abbb'   :", re.match(r"ab+", "abbb").group(0))
print()

# NAMED groups - readable code
pat = re.compile(r"(?P<user>[\w.]+)@(?P<domain>[\w.]+)\.(?P<tld>\w{2,})")
mm = pat.match("imran.bizee@cyggs.tech")
print("groupdict()     :", mm.groupdict())
print("group('domain') :", mm.group("domain"))
assert mm.group("user") == "imran.bizee" and mm.group("tld") == "tech"

# Optional group jo match na ho -> None (empty string NAHI)
mo = re.match(r"(\d+)(?:\.(\d+))?", "42")
print("optional group  :", mo.groups(), " <-- doosra None hai")
print("groups(default) :", mo.groups(default="0"), " <-- default de sakte ho")
assert mo.group(2) is None
print()

# ALTERNATION: pehla match jeetta hai (longest nahi)
print(r"'a|ab'  on 'ab' :", re.match(r"a|ab", "ab").group(), " <-- 'a' (pehla alternative)")
print(r"'ab|a'  on 'ab' :", re.match(r"ab|a", "ab").group(), " <-- specific pehle likho")
print(r"^cat|dog$ scope :", bool(re.match(r"^cat|dog$", "catdog")), " <-- galat scope!")
print(r"^(?:cat|dog)$   :", bool(re.match(r"^(?:cat|dog)$", "catdog")), " <-- sahi")
print()

# ------------------------------------------------------------------
# BACKREFERENCES
# ------------------------------------------------------------------
# 1) Duplicate word pakro
dup = "this is is a test test sentence with the the bug"
print("duplicate words :", re.findall(r"\b(\w+)\s+\1\b", dup))
print("fixed           :", re.sub(r"\b(\w+)\s+\1\b", r"\1", dup))
assert re.sub(r"\b(\w+)\s+\1\b", r"\1", dup) == "this is a test sentence with the bug"

# 2) Matching quotes (single ya double, magar dono same)
q = "He said \"hello\" and 'bye' but \"mismatched'"
print("quoted strings  :", re.findall(r"(['\"])(.*?)\1", q))

# 3) Named backreference (?P=name)
print("named backref   :", re.findall(r"(?P<c>\w)(?P=c)", "aabbcdee"))   # double letters

# 4) Repeated HTML-ish tag pair
print("tag pair        :", re.findall(r"<(\w+)>(.*?)</\1>", "<b>bold</b><i>it</i>"))

# 5) sub me \g<name> - jab \1 ke baad digit aata ho
print("swap with \\g<>  :", re.sub(r"(?P<a>\w+)@(?P<b>\w+)", r"\g<b>_at_\g<a>", "ali@bizee"))
print("digit clash fix :", re.sub(r"(\d)", r"\g<1>0", "5"), "  <-- r'\\10' hota to group 10 samjha jata")
assert re.sub(r"(\d)", r"\g<1>0", "5") == "50"
"""))

A(code(r"""
# ------------------------------------------------------------------
# LOOKAHEAD / LOOKBEHIND (positive + negative)
# ------------------------------------------------------------------
prices = "Laptop Rs.250000, Mouse USD 15, Bag Rs.4500, Pen EUR 3"

# (?<=...) positive lookbehind: 'Rs.' ke BAAD wale numbers (Rs. match me shamil nahi)
print("after Rs.  (?<=Rs\\.)\\d+ :", re.findall(r"(?<=Rs\.)\d+", prices))

# (?=...) positive lookahead: aisa word jiske baad ' Rs.' aata ho
print("before Rs. \\w+(?= Rs\\.) :", re.findall(r"\w+(?= Rs\.)", prices))

# (?<!...) negative lookbehind: numbers jinke peeche 'Rs.' NAHI hai
print("not after Rs.           :", re.findall(r"(?<!Rs\.)\b\d+\b", prices))

# (?!...) negative lookahead: 'a' se shuru word jo 'and' na ho
words = "apple and ant android answer"
print("a-word not 'and'        :", re.findall(r"\ba(?!nd\b)\w*", words))
print()

# --- Thousands separator daalna (classic lookahead puzzle) ---
n = "1234567890"
print("commas via lookahead :", re.sub(r"\B(?=(\d{3})+(?!\d))", ",", n))
assert re.sub(r"\B(?=(\d{3})+(?!\d))", ",", n) == "1,234,567,890"
print("   (?=(\\d{3})+(?!\\d)) = 'aage se aakhir tak digits ke poore 3-3 group banein'")
print("   \\B = string ke shuru me comma na lage")
print()

# --- Multiple AND conditions ek pattern me (lookaheads zero-width hain,")
#     is liye sab same position se check hote hain) ---
strong = re.compile(r'''
    ^                 # shuru
    (?=.*[a-z])       # kahin ek lowercase ho
    (?=.*[A-Z])       # kahin ek uppercase ho
    (?=.*\d)          # kahin ek digit ho
    (?=.*[^\w\s])     # kahin ek symbol ho
    (?!.*\s)          # koi whitespace NA ho
    .{8,}             # kam az kam 8 chars
    $
''', re.VERBOSE)
for pw in ["Pak@1234", "weakpass", "NOLOWER1@", "Has Space1@", "Sh0rt@"]:
    print(f"  {pw!r:<16} -> {'STRONG' if strong.match(pw) else 'weak'}")
assert strong.match("Pak@1234") and not strong.match("weakpass")
print()

# --- Lookbehind FIXED-WIDTH hona chahiye (Python limitation) ---
try:
    re.compile(r"(?<=a+)b")
except re.error as e:
    print("variable-width lookbehind error :", e)
    print("Workaround : (?<=aa|bb) same-length alternatives, ya \\K wali engine (Python me nahi)")
print()

# --- Lookaround zero-width hai: consume nahi karta -> overlapping matches ---
print("overlapping via lookahead:", re.findall(r"(?=(\d\d))", "12345"))
print("   normal findall(r'\\d\\d')  :", re.findall(r"\d\d", "12345"), "<-- overlap nahi")
"""))

A(md(r"""
## D6. Flags - pattern ka behaviour badalne wale switches

| Flag | Short | Kaam |
|---|---|---|
| `re.IGNORECASE` | `re.I` | case-insensitive |
| `re.MULTILINE` | `re.M` | `^` `$` har line par |
| `re.DOTALL` | `re.S` | `.` newline bhi match kare |
| `re.VERBOSE` | `re.X` | pattern me whitespace + `#` comments allowed |
| `re.ASCII` | `re.A` | `\d \w \s \b` sirf ASCII |
| `re.UNICODE` | `re.U` | default for `str` (redundant) |
| `re.NOFLAG` | - | 0 (koi flag nahi, 3.11+) |

Combine `|` se: `re.I | re.M`.

**Inline flags** pattern ke andar bhi likh sakte ho:
- `(?i)` poore pattern par (Python me **pattern ke shuru me** hona chahiye, warna error)
- `(?i:...)` sirf us group par (**scoped**, 3.6+) - yeh zyada mehfooz hai
- `(?-i:...)` us hisse par flag **off**

### `VERBOSE` (X-mode) - production regex ka must
```python
pat = re.compile(r'''
    ^(?P<code>[A-Z]{3})     # 3 uppercase letters = airport code
    -(?P<num>\d{3,4})$      # dash + 3-4 digit flight number
''', re.VERBOSE)
```
VERBOSE me:
- **Un-escaped whitespace ignore hoti hai** -> space chahiye to `\ ` ya `[ ]` ya `\s` likho
- `#` se line ke aakhir tak comment
- Character class **ke andar** whitespace ignore **nahi** hoti (`[a b]` me space literal hai)
"""))

A(code(r"""
# ------------------------------------------------------------------
# Flags: I, M, S, X + inline scoped flags
# ------------------------------------------------------------------
# IGNORECASE
print("no flag  :", re.findall(r"python", "Python PYTHON python PyThOn"))
print("re.I     :", re.findall(r"python", "Python PYTHON python PyThOn", re.I))
print()

# MULTILINE
csvish = "name,age\nAli,25\nSana,30\nBilal,28"
print("^\\w+ no flag :", re.findall(r"^\w+", csvish))
print("^\\w+ re.M    :", re.findall(r"^\w+", csvish, re.M))
print("\\w+$ re.M    :", re.findall(r"\w+$", csvish, re.M))
assert re.findall(r"^\w+", csvish, re.M) == ["name", "Ali", "Sana", "Bilal"]
print()

# DOTALL - '.' newline bhi khaye
block = "START\nline1\nline2\nEND"
print("START.*END no flag :", re.search(r"START.*END", block))
print("START.*END re.S    :", repr(re.search(r"START.*END", block, re.S).group()[:20]) + "...")
assert re.search(r"START.*END", block) is None
assert re.search(r"START.*END", block, re.S) is not None
print()

# Combining flags
print("re.I|re.M :", re.findall(r"^ali", "ALI\nali\nAli", re.I | re.M))
print()

# VERBOSE: commented, readable pattern
flight_re = re.compile(r'''
    ^                       # string ka shuru
    (?P<origin>[A-Z]{3})    # 3-letter origin code, e.g. LHE
    \s*->\s*                # arrow, aas paas whitespace optional
    (?P<dest>[A-Z]{3})      # 3-letter destination code
    \s+                      # separator (escape/class zaroori nahi, \s hai)
    (?P<flight>[A-Z]{2}\d{3,4})   # airline code + number, e.g. PK301
    $                       # aakhir
''', re.VERBOSE)

for line in ["LHE -> KHI PK301", "ISB->DXB EK615", "lhe -> khi pk301", "LHE KHI PK301"]:
    mt = flight_re.match(line)
    print(f"  {line!r:<22} -> {mt.groupdict() if mt else None}")
assert flight_re.match("LHE -> KHI PK301").group("flight") == "PK301"
print()

# VERBOSE gotcha: literal space chahiye to escape karo
print("VERBOSE me plain space ignore:", bool(re.match(r"a b", "ab", re.X)))
print("escaped space \\  kaam karta  :", bool(re.match(r"a\ b", "a b", re.X)))
print("[ ] class bhi theek           :", bool(re.match(r"a[ ]b", "a b", re.X)))
assert re.match(r"a b", "ab", re.X) is not None
print()

# Inline flags
print("(?i) at start   :", re.findall(r"(?i)python", "Python PYTHON"))
print("(?i:..) scoped  :", re.findall(r"(?i:hello) world", "HELLO world | HELLO WORLD"))
try:
    re.compile(r"abc(?i)")          # global inline flag beech me = error (3.11+)
except re.error as e:
    print("inline flag mid-pattern error :", e)
"""))

A(md(r"""
## D7. `re` ka poora API + compiled patterns + catastrophic backtracking

| Function | Kya deta hai | Kahan match dhundta hai |
|---|---|---|
| `re.match(p, s)` | `Match` ya `None` | **sirf shuru** se |
| `re.fullmatch(p, s)` | `Match` ya `None` | **poori** string match ho |
| `re.search(p, s)` | `Match` ya `None` | **kahin bhi**, pehla |
| `re.findall(p, s)` | `list[str]` ya `list[tuple]` | saare non-overlapping |
| `re.finditer(p, s)` | **iterator of `Match`** | saare (memory-friendly, span/groupdict milta hai) |
| `re.sub(p, repl, s)` | nayi string | replace all (`count=` se limit) |
| `re.subn(p, repl, s)` | `(new_string, n_replacements)` | jab count chahiye |
| `re.split(p, s)` | `list[str]` | pattern par tod do (capture group ho to separators bhi aate hain) |

**Validation ke liye `fullmatch` use karo, `match` nahi.** `re.match(r"\d+", "123abc")`
match kar jata hai (sirf shuru dekhta hai) - `fullmatch` nahi karega.

### `sub` ke saath **function** repl
```python
re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "a1 b2")   # 'a2 b4'
```
Function ko `Match` milta hai, string return karni hoti hai. Conditional/computed
replacements ke liye yeh bohat taqatwar hai.

### Compiled patterns
`re.compile()` ek dafa parse karta hai, phir reuse. `re` module ke andar bhi ~512
patterns ka cache hai, is liye faida chhota hota hai - magar **loops me aur bare patterns par
compile karna behtar hai**, plus `re.VERBOSE` ke sath readable code milta hai.

### Catastrophic backtracking (ReDoS) - **yeh mat chalao**
```python
BAD  = r"^(a+)+$"          # nested quantifier
TEXT = "a" * 40 + "b"      # match fail hoga
# ^ engine 2**40 raaste try karega -> minute/ghante lag sakte hain
```
Wajah: **nested quantifiers** (`(a+)+`, `(a*)*`, `(\s|\t)+$`) + fail hone wala input.
Engine ke paas "a" ko groups me batne ke exponentially bohat tareeqe hote hain.

**Ilaaj:**
1. Nested quantifier na likho: `^a+$` kaafi hai
2. Possessive/atomic: `^(?>a+)+$` ya `^(a++)+$`
3. Negated class se deterministic banao: `"[^"]*"` na ke `".*?"`
4. Ambiguous alternation `(a|a)*` se bacho
5. Input length limit karo, aur user-supplied regex **kabhi** trust na karo
6. `regex` (third-party) library timeout support karti hai; stdlib `re` me timeout **nahi** hai
""",))

A(code(r"""
# ------------------------------------------------------------------
# match vs fullmatch vs search vs findall vs finditer
# ------------------------------------------------------------------
s = "123abc456"

print("match(r'\\d+')     :", re.match(r"\d+", s))        # shuru se match -> '123'
print("fullmatch(r'\\d+') :", re.fullmatch(r"\d+", s))    # poora nahi -> None
print("search(r'[a-z]+') :", re.search(r"[a-z]+", s))     # kahin bhi -> 'abc'
print("match(r'[a-z]+')  :", re.match(r"[a-z]+", s))      # shuru me letter nahi -> None
print("findall(r'\\d+')   :", re.findall(r"\d+", s))
print()
print("VALIDATION ka sabaq: match kaafi nahi!")
print("  match(r'\\d+', '123abc')     :", bool(re.match(r"\d+", "123abc")), " <-- ghalat 'valid'")
print("  fullmatch(r'\\d+', '123abc') :", bool(re.fullmatch(r"\d+", "123abc")), " <-- sahi")
assert re.match(r"\d+", "123abc") and not re.fullmatch(r"\d+", "123abc")
print()

# finditer -> Match objects (span, groupdict, lazy)
log = "ERROR at 10:30, WARN at 11:45, ERROR at 12:00"
for mt in re.finditer(r"(?P<level>ERROR|WARN) at (?P<time>\d{2}:\d{2})", log):
    print(f"  span={mt.span()} level={mt.group('level'):<5} time={mt.group('time')}")
print()

# ------------------------------------------------------------------
# sub / subn / split
# ------------------------------------------------------------------
print("sub simple  :", re.sub(r"\s+", " ", "too    many\t\tspaces\n\nhere"))
print("sub count=1 :", re.sub(r"a", "X", "banana", count=1))
print("subn        :", re.subn(r"a", "X", "banana"))       # (result, kitni dafa)
res, n = re.subn(r"a", "X", "banana")
assert res == "bXnXnX" and n == 3
print()

# sub with FUNCTION repl - computed replacement
def double_num(mt):
    return str(int(mt.group()) * 2)
print("sub(func)   :", re.sub(r"\d+", double_num, "a1 b20 c300"))
assert re.sub(r"\d+", double_num, "a1 b20 c300") == "a2 b40 c600"

# Practical: masking sensitive data
def mask_card(mt):
    digits = re.sub(r"\D", "", mt.group())          # sirf digits rakho
    return "*" * (len(digits) - 4) + digits[-4:]    # aakhri 4 dikhao
print("masked cards:", re.sub(r"\b(?:\d[ -]?){13,16}\d\b", mask_card, "Card 4111-1111-1111-1111 ok"))

# Practical: template rendering
ctx = {"name": "Imran", "city": "Karachi"}
tpl = "Salam {{name}}, aap {{city}} se hain. Missing: {{age}}"
print("rendered    :", re.sub(r"\{\{(\w+)\}\}", lambda m: str(ctx.get(m.group(1), "N/A")), tpl))
print()

# split
print("split \\s+       :", re.split(r"\s+", "a b   c\td"))
print("split multi-sep  :", re.split(r"[,;|]\s*", "a, b; c|d"))
print("split maxsplit=1 :", re.split(r",", "a,b,c", maxsplit=1))
print("split w/ GROUP   :", re.split(r"(\d)", "a1b2c"), " <-- separators bhi list me!")
print("split empty match:", re.split(r"", "abc"), " <-- 3.7+ zero-width split allowed")
assert re.split(r"(\d)", "a1b2c") == ["a", "1", "b", "2", "c"]
"""))

A(code(r"""
# ------------------------------------------------------------------
# Compiled patterns: speed + reuse
# ------------------------------------------------------------------
lines = [f"user{i}@mail{i % 7}.com scored {i % 100}" for i in range(4000)]
PAT = r"(\w+)@([\w.]+) scored (\d+)"

t0 = perf_counter()
for ln in lines:
    re.search(PAT, ln)                 # module-level (internal cache hit hota hai)
t_module = perf_counter() - t0

compiled = re.compile(PAT)             # ek dafa parse
t0 = perf_counter()
for ln in lines:
    compiled.search(ln)                # method call - koi cache lookup nahi
t_compiled = perf_counter() - t0

print(f"lines            : {len(lines):,}")
print(f"re.search()      : {t_module*1000:7.2f} ms")
print(f"compiled.search(): {t_compiled*1000:7.2f} ms")
print(f"speedup          : ~{t_module/max(t_compiled, 1e-9):.2f}x (chhota, kyunki re ka internal cache hai)")
print()
print("Compile karne ki asli wajhein:")
print("  1. re.VERBOSE ke sath readable, documented pattern")
print("  2. Module-level constant -> intent saaf, hot loop me cache lookup nahi")
print("  3. Pattern object ke methods: .search .match .findall .sub .split .finditer")
print("  4. pos/endpos arguments sirf compiled patterns par milte hain")
print()

# compiled pattern ke extra tools
cp = re.compile(r"\d+")
print("pattern string  :", cp.pattern)
print("search(pos=5)   :", cp.search("12 34 56 78", 5))      # index 5 se aage dhundo
print("groupindex      :", re.compile(r"(?P<a>x)(?P<b>y)").groupindex)
print()

# ------------------------------------------------------------------
# CATASTROPHIC BACKTRACKING - sirf padhne ke liye, CHALANA NAHI
# ------------------------------------------------------------------
BAD_PATTERNS = [
    r"^(a+)+$",              # nested quantifier
    r"^(\w+\s?)*$",          # ambiguous: \w+ aur \s? overlap
    r"^(.*,)*$",             # nested star
    r"^(a|a)*$",             # ambiguous alternation
]
print("KHATARNAAK patterns (yeh cell inhe chalata NAHI):")
for p in BAD_PATTERNS:
    print("   ", p)
print()
print('Input "aaaa...ab" (match FAIL) par engine 2**n raaste try karta hai.')
print("40 a's = ~1e12 steps = minutes/hours. Yehi ReDoS attack hai.")
print()

# SAFE versions - inhe chalana bilkul theek hai
SAFE_TEXT = "a" * 5000 + "b"           # 5001 chars, match fail hoga
safe_checks = [
    (r"^a+$",        "flat quantifier - koi nesting nahi"),
    (r"^[^b]*$",     "negated class - deterministic"),
]
for pat, why in safe_checks:
    t0 = perf_counter()
    ok = re.fullmatch(pat, SAFE_TEXT) is not None
    dt = (perf_counter() - t0) * 1000
    print(f"  {pat:<12} match={ok!s:<5} {dt:7.3f} ms   ({why})")

# Possessive/atomic bhi safe bana deta hai (Python 3.11+)
try:
    t0 = perf_counter()
    ok = re.fullmatch(r"^(?>a+)+$", SAFE_TEXT) is not None
    print(f"  {'^(?>a+)+$':<12} match={ok!s:<5} {(perf_counter()-t0)*1000:7.3f} ms   (atomic group)")
except re.error:
    print("  atomic groups is Python me available nahi")
print()
print("Golden rules: nested quantifier na likho | negated class prefer karo |")
print("              user ka regex trust na karo | input length cap karo.")
"""))

A(md(r"""
## D8. Real validations - email, Pakistani mobile, password, log parsing, dates

### Email
"Perfect" email regex **exist nahi karta** (RFC 5322 ka regex ~6000 chars ka hai).
Practical approach:
1. Ek **sane** regex se obvious ghalat cheezein rok do
2. Asli verification **confirmation email** bhej kar karo
3. Production me `email.utils.parseaddr` / `email-validator` library use karo

```python
r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)+$"
```

### Pakistani mobile number
Formats jo log likhte hain:
| Input | Valid? |
|---|---|
| `03001234567` | haan (local, 11 digits) |
| `0300-1234567` | haan (dash) |
| `+923001234567` | haan (E.164) |
| `+92 300 1234567` | haan (spaces) |
| `00923001234567` | haan (old international prefix) |
| `0300123456` | **nahi** (10 digits) |
| `04001234567` | **nahi** (mobile network code `3` se shuru hota hai) |

```python
r"^(?:(?:\+92|0092)[\s-]?|0)3\d{2}[\s-]?\d{7}$"
```

### Password strength
Lookaheads se AND-conditions (D5 me dekha). Plus **length limit** rakho (DoS se bachao)
aur asli app me `zxcvbn` jaisi entropy library socho - regex sirf minimum floor hai.

### Log parsing
`re.VERBOSE` + **named groups** + `finditer` = maintainable log parser jo seedha `dict` deta hai.

### HTML/XML - **regex se parse na karo**
Regex nested/recursive structures handle nahi kar sakta (regular languages me nesting nahi hoti).
Attributes me `>` , comments, CDATA, unclosed tags - sab tod dete hain.
**Use `html.parser`, `lxml`, ya `BeautifulSoup`.** Regex sirf **chhote, controlled**
extraction (jaise apni hi generated string se ek tag nikalna) ke liye theek hai.
"""))

A(code(r"""
# ------------------------------------------------------------------
# VALIDATION 1: Email  |  VALIDATION 2: Pakistani mobile number
# ------------------------------------------------------------------
EMAIL_RE = re.compile(r'''
    ^
    [A-Za-z0-9_.+-]+          # local part: letters, digits, . _ + -
    @
    [A-Za-z0-9-]+             # domain ka pehla label
    (?:\.[A-Za-z0-9-]+)*      # optional sub-domains
    \.[A-Za-z]{2,}            # TLD: kam az kam 2 letters
    $
''', re.VERBOSE)

emails = [
    "imran.bizee@cyggs.tech",     # valid
    "ali+news@gmail.com",         # valid (plus addressing)
    "a_b@sub.domain.co.uk",       # valid (multi-level)
    "no-at-sign.com",             # invalid
    "double@@mail.com",           # invalid
    "trailing@dot.",              # invalid
    "spaces in@mail.com",         # invalid
    "short@d.c",                  # valid (2-letter TLD)
    "@nolocal.com",               # invalid
]
print("EMAIL VALIDATION")
for e in emails:
    print(f"  {e:<26} -> {'VALID' if EMAIL_RE.fullmatch(e) else 'invalid'}")

assert EMAIL_RE.fullmatch("imran.bizee@cyggs.tech")
assert EMAIL_RE.fullmatch("ali+news@gmail.com")
assert not EMAIL_RE.fullmatch("no-at-sign.com")
assert not EMAIL_RE.fullmatch("double@@mail.com")
assert not EMAIL_RE.fullmatch("trailing@dot.")
print()

# ------------------------------------------------------------------
PK_MOBILE_RE = re.compile(r'''
    ^
    (?:                       # country prefix ka hissa
        (?:\+92|0092)[\s-]?   #   +92 ya 0092, aage optional space/dash
      | 0                     #   ya local trunk '0'
    )
    3                         # mobile numbers hamesha 3 se shuru
    \d{2}                     # network code ke baqi 2 digits (300, 321, 345...)
    [\s-]?                    # optional separator
    \d{7}                     # subscriber number: 7 digits
    $
''', re.VERBOSE)

phones = [
    "03001234567", "0321-1234567", "+923451234567", "+92 300 1234567",
    "00923331234567", "0300123456", "04001234567", "3001234567",
    "+91 300 1234567", "0300 1234 567",
]
print("PAKISTANI MOBILE VALIDATION")
for p in phones:
    print(f"  {p:<18} -> {'VALID' if PK_MOBILE_RE.fullmatch(p) else 'invalid'}")

assert PK_MOBILE_RE.fullmatch("03001234567")
assert PK_MOBILE_RE.fullmatch("0321-1234567")
assert PK_MOBILE_RE.fullmatch("+923451234567")
assert PK_MOBILE_RE.fullmatch("+92 300 1234567")
assert PK_MOBILE_RE.fullmatch("00923331234567")
assert not PK_MOBILE_RE.fullmatch("0300123456")      # 1 digit kam
assert not PK_MOBILE_RE.fullmatch("04001234567")     # 4 se shuru
assert not PK_MOBILE_RE.fullmatch("3001234567")      # koi prefix nahi
print()

# Normalize karne ka helper (validation ke baad canonical form banao)
def normalize_pk(phone: str) -> str | None:
    if not PK_MOBILE_RE.fullmatch(phone):
        return None
    digits = re.sub(r"\D", "", phone)                # sirf digits
    digits = re.sub(r"^(?:0092|92|0)", "", digits)   # prefix hatao -> 10 digits
    return "+92" + digits

for p in ["03001234567", "0321-1234567", "+92 300 1234567", "00923331234567", "bad"]:
    print(f"  normalize({p!r:<18}) -> {normalize_pk(p)}")
assert normalize_pk("03001234567") == "+923001234567"
assert normalize_pk("+92 300 1234567") == "+923001234567"
assert normalize_pk("bad") is None
"""))

A(code(r"""
# ------------------------------------------------------------------
# VALIDATION 3: Password strength (score + reasons)
# ------------------------------------------------------------------
PW_RULES = [
    (r".{8,}",        "kam az kam 8 characters"),
    (r"[a-z]",        "ek lowercase letter"),
    (r"[A-Z]",        "ek uppercase letter"),
    (r"\d",           "ek digit"),
    (r"[^A-Za-z0-9]", "ek special character"),
]
NO_SPACE   = re.compile(r"^\S+$")
NOT_COMMON = {"password", "12345678", "qwerty123", "pakistan"}

def check_password(pw: str) -> dict:
    '''Rules ka score + missing reasons ki list deta hai.'''
    missing = [why for pat, why in PW_RULES if not re.search(pat, pw)]
    if not NO_SPACE.fullmatch(pw):
        missing.append("whitespace nahi hona chahiye")
    if pw.lower() in NOT_COMMON:
        missing.append("bohat aam password hai")
    if len(pw) > 128:
        missing.append("128 chars se lamba nahi (DoS guard)")
    score = len(PW_RULES) - len([m for m in missing if m in [w for _, w in PW_RULES]])
    label = ["very weak", "weak", "fair", "good", "strong", "very strong"][score]
    return {"ok": not missing, "score": score, "label": label, "missing": missing}

for pw in ["Pak@1234", "abc", "alllowercase1!", "NoDigits!!", "Has Space1@", "Password", "Karachi#2024Rocks"]:
    r = check_password(pw)
    flag = "OK  " if r["ok"] else "FAIL"
    print(f"  {flag} {pw!r:<20} score={r['score']}/5 ({r['label']})")
    if r["missing"]:
        print(f"        missing -> {', '.join(r['missing'])}")

assert check_password("Pak@1234")["ok"] is True
assert check_password("abc")["ok"] is False
assert "whitespace nahi hona chahiye" in check_password("Has Space1@")["missing"]
assert check_password("Karachi#2024Rocks")["score"] == 5
print()

# Single-regex version (lookaheads) - chhota, magar "kya missing hai" nahi bata sakta
ONE_SHOT = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9])(?!.*\s).{8,128}$")
print("ONE_SHOT 'Pak@1234' :", bool(ONE_SHOT.fullmatch("Pak@1234")))
print("ONE_SHOT 'weakpass' :", bool(ONE_SHOT.fullmatch("weakpass")))
print()
print("Interview tip: rule-list wala approach production me behtar hai kyunki user ko")
print("actionable feedback deta hai; single regex sirf yes/no deta hai.")
"""))

A(code(r"""
# ------------------------------------------------------------------
# LOG PARSING -> list[dict]   +   DATE EXTRACTION   +   HTML caution
# ------------------------------------------------------------------
ACCESS_LOG = '''\
203.0.113.7 - imran [15/Mar/2024:13:55:36 +0500] "GET /api/orders?page=2 HTTP/1.1" 200 2326 "-" "curl/8.4.0"
198.51.100.22 - - [15/Mar/2024:13:55:40 +0500] "POST /api/login HTTP/1.1" 401 128 "-" "Mozilla/5.0"
203.0.113.7 - imran [15/Mar/2024:13:56:02 +0500] "GET /static/app.css HTTP/1.1" 304 - "-" "Mozilla/5.0"
BROKEN LINE THAT SHOULD NOT PARSE
192.0.2.9 - admin [15/Mar/2024:14:01:11 +0500] "DELETE /api/orders/88 HTTP/1.1" 500 512 "-" "PostmanRuntime/7.36"
'''

# Combined Log Format ka parser: VERBOSE + named groups = maintainable
LOG_RE = re.compile(r'''
    ^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})      \s+   # IPv4
    (?P<ident>\S+)                        \s+   # identd (usually '-')
    (?P<user>\S+)                         \s+   # authenticated user ya '-'
    \[(?P<ts>[^\]]+)\]                    \s+   # [15/Mar/2024:13:55:36 +0500]
    "(?P<method>[A-Z]+)\s+
     (?P<path>\S+)\s+
     (?P<proto>HTTP/[\d.]+)"              \s+   # request line
    (?P<status>\d{3})                     \s+   # status code
    (?P<size>\d+|-)                       \s+   # bytes ya '-'
    "(?P<referer>[^"]*)"                  \s+
    "(?P<agent>[^"]*)"$
''', re.VERBOSE)

parsed, bad = [], []
for line in ACCESS_LOG.strip().splitlines():
    mt = LOG_RE.match(line)
    if not mt:
        bad.append(line)
        continue
    d = mt.groupdict()
    d["status"] = int(d["status"])                             # types theek karo
    d["size"] = 0 if d["size"] == "-" else int(d["size"])
    d["ts"] = datetime.strptime(d["ts"], "%d/%b/%Y:%H:%M:%S %z")   # tz-aware datetime
    parsed.append(d)

print(f"parsed {len(parsed)} lines, {len(bad)} rejected")
for d in parsed:
    print(f"  {d['ts']:%H:%M:%S} {d['ip']:<14} {d['method']:<6} {d['status']} {d['size']:>5}B  {d['path']}")
print("rejected:", bad)
assert len(parsed) == 4 and len(bad) == 1
assert parsed[0]["status"] == 200 and parsed[2]["size"] == 0
assert parsed[0]["ts"].tzinfo is not None
print()

# ------------------------------------------------------------------
# DATE EXTRACTION - kai formats ek pattern me
# ------------------------------------------------------------------
doc = ("Invoice dated 2024-03-15 was due 15/04/2024, reminder sent on Apr 20, 2024 "
       "and finally paid 2024-05-01. Bogus date 2024-13-45 bhi likha hai.")

DATE_RE = re.compile(r'''
      (?P<iso>\d{4}-\d{2}-\d{2})                          # 2024-03-15
    | (?P<dmy>\d{1,2}/\d{1,2}/\d{4})                      # 15/04/2024
    | (?P<mdy>(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)
       [a-z]*\s+\d{1,2},\s*\d{4})                         # Apr 20, 2024
''', re.VERBOSE)

print("DATE EXTRACTION")
FORMATS = {"iso": "%Y-%m-%d", "dmy": "%d/%m/%Y", "mdy": "%b %d, %Y"}
found = []
for mt in DATE_RE.finditer(doc):
    kind = mt.lastgroup                       # kaunsa named group match hua
    raw = mt.group()
    try:
        # normalize -> real date object. Bogus dates yahan pakre jate hain (regex se nahi)
        clean = re.sub(r"\s+", " ", raw.replace(",", ", ").replace(",  ", ", "))
        parsed_date = datetime.strptime(raw if kind != "mdy" else clean[:12].strip(), FORMATS[kind]).date()
        found.append(parsed_date)
        print(f"  {raw:<16} ({kind}) -> {parsed_date}")
    except ValueError as e:
        print(f"  {raw:<16} ({kind}) -> INVALID: {e}")

print("Sabaq: regex SHAPE check karta hai, VALIDITY nahi. 2024-13-45 shape me sahi hai")
print("       magar strptime use reject karta hai. Dono milakar use karo.")
assert date(2024, 3, 15) in found and date(2024, 4, 15) in found
print()

# ------------------------------------------------------------------
# HTML: regex ki hadd
# ------------------------------------------------------------------
tricky = '<a href="x>y.html" title="not > a tag">Click</a><!-- <b>comment</b> -->'
print("HTML CAUTION")
print("  naive <.*?>  :", re.findall(r"<.*?>", tricky))
print("  ^ attribute ke andar '>' ne pattern tod diya. Nested/comment/CDATA bhi todte hain.")
print()
print("  SAHI tareeqa: stdlib html.parser (ya lxml / BeautifulSoup)")
from html.parser import HTMLParser
class TagCollector(HTMLParser):
    def __init__(self):
        super().__init__(); self.tags = []; self.text = []
    def handle_starttag(self, tag, attrs): self.tags.append((tag, dict(attrs)))
    def handle_data(self, data):
        if data.strip(): self.text.append(data.strip())

tc = TagCollector(); tc.feed(tricky)
print("  parser tags  :", tc.tags)
print("  parser text  :", tc.text)
assert tc.tags[0][0] == "a" and tc.tags[0][1]["href"] == "x>y.html"
print()
print("  Regex sirf tab theek hai jab input CHHOTA aur CONTROLLED ho, e.g. tag strip:")
print("  strip tags   :", re.sub(r"<[^>]+>", "", "<p>Hello <b>World</b></p>"))
"""))

# ---------------------------------------------------------------
# PART 3 MARKER
# ---------------------------------------------------------------
# @@PART3@@

print(f"cells so far: {len(cells)}")
save(r"Python/Intermediate/05_Collections_Regex_Datetime_aur_DataFormats.ipynb", cells)
