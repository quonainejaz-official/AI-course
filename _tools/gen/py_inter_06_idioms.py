"""Generator: Python/Intermediate/06_Comprehension_Patterns_Idioms_aur_Interview_Problems.ipynb

Chalao (ROOT se):  python _tools/gen/py_inter_06_idioms.py
"""

import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

CELLS: list = []
A = CELLS.append

# ---------------------------------------------------------------- title
A(md("""
# 06 — Comprehension Patterns, Pythonic Idioms aur Interview Problems

**Level:** Intermediate → Interview-ready
**Zubaan:** Roman Urdu + English (technical terms English me)

Ye notebook is series ka **sabse bara aur sabse "practical"** notebook hai. Yahan hum wo cheezein
seekhenge jo *code review me tumhari izzat banati ya bigarti hain* — yani **Pythonic idioms**.
Ek hi kaam ke do tareeqe hote hain: **"C/Java jaisa Python"** (anti-pattern) aur **"Python jaisa Python"**
(idiomatic). Interviewer 5 minute me pehchan leta hai tum kis camp me ho.

## Is notebook me kya seekhenge

**Part 1 — Pythonic idioms vs anti-patterns (bad way vs good way, side by side)**
- `enumerate()` vs `range(len(...))`, `enumerate(start=)`
- `zip()` aur `zip(..., strict=True)` (Python 3.10+)
- tuple unpacking, variable swap `a, b = b, a`, chained comparison `0 <= x <= 10`
- `any()` / `all()` vs manual flag loops
- `sorted(key=...)` / lambda
- `dict.get(k, default)`, `setdefault` vs `collections.defaultdict`
- `"".join()` vs loop me `+=` (asli **timing** ke sath)
- truthiness / falsy values, EAFP vs LBYL
- slicing tricks: `[::-1]`, `[::2]`, copy `[:]`, `del lst[a:b]`
- `_` ke conventions: throwaway `_`, `_private`, `__dunder` (name mangling), REPL `_`, digit separators `1_000_000`
- ternary expression, walrus `:=`, f-string debugging `f"{x=}"` + format specs (`:.2f`, `:>10`, `:,`)
- `str.translate()` / `str.maketrans()`

**Part 2 — Comprehension mastery**
- list / dict / set comprehensions, nested loops, flattening
- conditional **filtering** (`if` end me) vs conditional **value** (ternary shuru me)
- comprehension vs generator expression (memory + timing)
- kab comprehension **unreadable** ho jata hai (readability rules)

**Part 3 — Shallow vs deep copy (nested structures)** — `copy.copy`, `copy.deepcopy`, `is` vs `==`, mutable default argument trap

**Part 4 — Sorting mastery** — multi-key sort, per-key reverse (negate / two-pass stable sort),
`operator.itemgetter` / `attrgetter`, stability ka proof, objects sorting (`__lt__` vs `key`),
`functools.cmp_to_key`, `sorted` vs `list.sort`, dict ko value se sort karna

**Part 5 — Unpacking mastery** — `*rest`, `a, *b, c`, nested unpacking, `{**a, **b}`, `a | b`,
`zip(*matrix)` transpose, `*` function calls me, `*args` / `**kwargs`, keyword-only args

**Part 6 — Common Mistakes / Gotchas** (late binding, list mutate-while-iterate, `+=` on tuple, `is` vs `==` ...)

**Part 7 — Real-World Problems** (student marks report, text cleanup pipeline, gaming leaderboard)

**Part 8 — 20 classic interview coding problems** (har ek: approach + complexity + passing `assert` tests)

**Part 9 — LeetCode section** (LC 49, 3, 13, 12, 48, 54, 443 — brute force vs optimal)

**Part 10 — Interview Q&A, Practice Exercises, Cheat-sheet**

## Prerequisites
- Python basics: `list`, `dict`, `set`, `tuple`, loops, functions
- Functions ka `*args/**kwargs` ka thora sa idea
- Previous notebooks: iterators/generators, functions, OOP basics ka halka sa taaruf

> **Padhne ka tareeqa:** har code cell ko *chala kar* output dekho, phir comment padho.
> Sirf padhna = kuch nahi seekha. Ek ek line badal kar tor-phor karo — wahi asli seekhna hai.
"""))

# ---------------------------------------------------------------- idioms I
A(md("""
---
# Part 1 — Pythonic Idioms vs Anti-patterns

## 1.1 `enumerate()` vs `range(len(...))`

**Kya hai:** `enumerate(iterable, start=0)` ek iterator deta hai jo `(index, item)` pairs banata hai.

**Kyun:** `for i in range(len(lst)): lst[i]` likhna C/Java ki aadat hai. Python me ye:
- lamba hai, padhne me shor (noise) hai
- `lst[i]` indexing har baar karni parti hai (galti ka chance)
- sirf sequences par chalta hai (generator/set par `len()` nahi hota)

**Syntax:** `for idx, value in enumerate(items, start=1): ...`

## 1.2 `zip()` — do (ya zyada) sequences saath chalao

`zip(a, b)` sabse **chhoti** sequence par ruk jata hai — ye chupke se data kha sakta hai (silent bug).
Python 3.10+ me `zip(a, b, strict=True)` length mismatch par **`ValueError`** deta hai — production code me
`strict=True` tumhara dost hai.

`itertools.zip_longest(a, b, fillvalue=...)` ka ulta kaam karta hai: **sabse lambi** tak chalta hai.

**Interview tip:** "Why is `enumerate` better than `range(len())`?" ka jawab —
*readability + kaam karta hai kisi bhi iterable par + index/value dono ek sath, indexing bug ka chance khatam.*
"""))
A(code(r'''
# ============ 1.1  enumerate vs range(len) ============
cities = ["Karachi", "Lahore", "Islamabad", "Quetta"]

print("BAD  (range(len(...)) - C/Java style):")
for i in range(len(cities)):                 # index banao, phir manually index karo
    print("   ", i, cities[i])               # cities[i] -> extra lookup, typo ka chance

print("GOOD (enumerate - Pythonic):")
for i, city in enumerate(cities):            # index + value ek hi sath mil gaye
    print("   ", i, city)

# enumerate(start=) -> human friendly 1-based numbering (reports/menus me kaam aata hai)
print("GOOD (enumerate with start=1):")
for rank, city in enumerate(cities, start=1):    # start sirf counter badalta hai, data nahi
    print(f"    {rank}. {city}")

# enumerate kisi bhi iterable par chalta hai - generator par bhi (jahan len() fail ho jata hai)
gen = (c for c in cities if len(c) > 6)          # generator expression
print("GOOD (enumerate on a generator):", list(enumerate(gen, start=1)))

try:
    len(c for c in cities)                       # generator ka len() nahi hota
except TypeError as e:                           # jaan boojh kar error -> wrapped
    print("TypeError (generator ka len nahi hota):", e)

# ============ 1.2  zip ============
names = ["Ali", "Sara", "Bilal"]
marks = [88, 92, 75]
roll  = [101, 102, 103]

print("\nBAD  (index se do list saath chalana):")
for i in range(len(names)):
    print("   ", names[i], marks[i])

print("GOOD (zip):")
for name, mark in zip(names, marks):             # parallel iteration, koi index nahi
    print("   ", name, mark)

# 3+ sequences bhi chal sakti hain -> tuple unpacking ke sath
for r, name, mark in zip(roll, names, marks):
    print(f"    roll={r} name={name:<6} mark={mark}")

# GOTCHA: zip chhoti list par ruk jata hai -> data chupke se gayab
short = [1, 2]
print("zip silently truncates ->", list(zip(names, short)))   # sirf 2 pairs!

# FIX: strict=True (Python 3.10+) -> mismatch par ValueError
try:
    print(list(zip(names, short, strict=True)))
except ValueError as e:
    print("ValueError (strict=True ne bug pakar liya):", e)

# Ulta case: sabse lambi tak chalo, missing jagah fillvalue
from itertools import zip_longest
print("zip_longest ->", list(zip_longest(names, short, fillvalue=0)))

# Do list -> dict (bohat common idiom)
name_to_mark = dict(zip(names, marks, strict=True))
print("dict(zip(...)) ->", name_to_mark)
assert name_to_mark == {"Ali": 88, "Sara": 92, "Bilal": 75}
print("[ok] 1.1 & 1.2 done")
'''))

# ---------------------------------------------------------------- idioms II
A(md("""
## 1.3 Tuple unpacking, variable swap, chained comparison, `any`/`all`, truthiness

### Tuple unpacking
Python me `a, b = 1, 2` ek **tuple unpacking** hai. Isi se:
- **swap:** `a, b = b, a` (koi `temp` variable nahi — right side pehle tuple banta hai, phir assign hota hai)
- **multiple return values:** `q, r = divmod(17, 5)`
- **nested:** `(name, (h, m)) = ("Ali", (9, 30))`

### Chained comparison
`0 <= x <= 100` — Python isko `0 <= x and x <= 100` ki tarah samajhta hai, **magar `x` sirf ek baar evaluate hota hai**.
Ye C/Java me galat chalta hai, Python me bilkul theek aur zyada readable hai.

### `any()` / `all()`
Manual flag loop (`found = False; for ...: found = True; break`) ki jagah:
- `any(cond for x in items)` → koi ek bhi `True`?
- `all(cond for x in items)` → sab `True`?
Dono **short-circuit** karte hain (pehla faisla milne par ruk jate hain) — yani efficient bhi hain.
Khyal rahe: `all([])` → `True` (vacuous truth), `any([])` → `False`.

### Truthiness (falsy values)
Ye sab falsy hain: `False`, `None`, `0`, `0.0`, `0j`, `""`, `[]`, `()`, `{}`, `set()`, `range(0)`,
aur wo objects jinka `__bool__`/`__len__` 0 deta hai.
**Idiom:** `if items:` likho, `if len(items) > 0:` nahi.
**Magar gotcha:** agar `0` ek valid value hai to `if value:` ghalat hai → `if value is not None:` likho.
"""))
A(code(r'''
# ============ 1.3a tuple unpacking + swap ============
a, b = 10, 20                      # ek line me do assignment (tuple unpacking)
print("pehle:", a, b)

# BAD (temp variable - C style)
tmp = a; a = b; b = tmp
print("swap via temp:", a, b)

# GOOD (Pythonic swap) - right side pehle (b, a) tuple banata hai, phir unpack hota hai
a, b = b, a
print("swap via unpacking:", a, b)

q, r = divmod(17, 5)               # function se do values -> seedha unpack
print(f"divmod(17,5) -> quotient={q} remainder={r}")

person = ("Ali", (9, 30))          # nested structure
name, (hour, minute) = person      # nested unpacking - shape match karna zaroori hai
print(f"{name} ka time {hour}:{minute:02d}")

# _ = throwaway variable (jo value chahiye nahi)
_, second, *_rest = [1, 2, 3, 4, 5]
print("second =", second)

# ============ 1.3b chained comparison ============
marks = 87
print("BAD :", 0 <= marks and marks <= 100)      # kaam karta hai, par verbose
print("GOOD:", 0 <= marks <= 100)                # ek hi baar 'marks' evaluate hota hai

calls = []
def value():                                     # side-effect wala function
    calls.append(1)                              # kitni baar chala, count karo
    return 50

print("chained result:", 0 <= value() <= 100)
print("value() kitni baar chala? ->", len(calls), "(sirf 1 baar - yahi chaining ka faida)")

# 3-way chaining bhi valid: a < b < c
x, y, z = 1, 5, 9
print("1 < 5 < 9 ->", x < y < z)

# ============ 1.3c any / all ============
nums = [4, 8, 15, 16, 23, 42]

# BAD: manual flag
has_odd = False
for n in nums:
    if n % 2:
        has_odd = True
        break
print("BAD  has_odd:", has_odd)

# GOOD: any() + generator expression (list nahi banti -> memory bachti hai)
print("GOOD has_odd:", any(n % 2 for n in nums))
print("GOOD all_even:", all(n % 2 == 0 for n in nums))

# Edge cases jo interview me poochte hain
print("any([]) =", any([]), "| all([]) =", all([]), "  <- all([]) True hota hai!")

# any/all short-circuit ka proof
seen = []
def check(n):
    seen.append(n)                               # record karo kis kis par chala
    return n > 3
print("any(...) ->", any(check(n) for n in [1, 2, 4, 5, 6]))
print("check() sirf in par chala:", seen, "-> 4 milte hi ruk gaya (short-circuit)")

# ============ 1.3d truthiness / falsy ============
falsy_values = [False, None, 0, 0.0, 0j, "", [], (), {}, set(), range(0)]
print("\nfalsy check:", [bool(v) for v in falsy_values])
assert not any(bool(v) for v in falsy_values)     # sab falsy hain

items = []
print("BAD :", "khali hai" if len(items) == 0 else "bhara hai")   # len() ki zaroorat nahi
print("GOOD:", "khali hai" if not items else "bhara hai")         # truthiness use karo

# GOTCHA: 0 valid value ho to truthiness dhoka deti hai
def discount_msg_bad(discount):
    if discount:                                  # 0 falsy hai -> galat branch!
        return f"discount {discount}%"
    return "koi discount field nahi mila"

def discount_msg_good(discount):
    if discount is not None:                      # sahi check: existence vs value
        return f"discount {discount}%"
    return "koi discount field nahi mila"

print("BAD  discount=0 ->", discount_msg_bad(0))
print("GOOD discount=0 ->", discount_msg_good(0))

# Custom object ki truthiness: __len__ ya __bool__
class Cart:
    def __init__(self, items): self.items = items
    def __len__(self): return len(self.items)     # len 0 -> object falsy ban jata hai
print("empty Cart truthy?", bool(Cart([])), "| non-empty?", bool(Cart(["pen"])))
print("[ok] 1.3 done")
'''))

# ---------------------------------------------------------------- idioms III
A(md("""
## 1.4 `dict.get()`, `setdefault()` vs `defaultdict`, aur EAFP vs LBYL

### `dict.get(key, default)`
`d[k]` missing key par `KeyError` deta hai. `d.get(k)` → `None`, `d.get(k, 0)` → tumhara default.
**Zaroori:** `get()` dict me kuch **insert nahi** karta.

### `setdefault(key, default)`
"agar key nahi hai to ye default daal do aur wapas do, warna maujood value do" — ek hi atomic step me.
Grouping ke liye classic: `groups.setdefault(key, []).append(item)`.

### `collections.defaultdict(factory)`
Har missing key par `factory()` chala kar value bana deta hai. `defaultdict(list)`, `defaultdict(int)`,
`defaultdict(set)` sabse common hain.
**Gotcha:** `defaultdict` me missing key ko **padhna** bhi usko create kar deta hai (dict grow ho jati hai).
Sirf read karna ho to `.get()` behtar hai. `Counter` bhi `defaultdict(int)` ka bara bhai hai — counting ke liye best.

### EAFP vs LBYL
- **LBYL** = Look Before You Leap → `if key in d: ...` (pehle check, phir kaam)
- **EAFP** = Easier to Ask Forgiveness than Permission → `try: d[key] except KeyError: ...`

Python community **EAFP** ko prefer karti hai kyunki:
1. race condition nahi (file/dict check aur use ke darmiyan cheez badal sakti hai)
2. happy path fast hota hai (`try` block ka cost tab tak zero jab tak exception na aaye)
3. do lookups ki jagah ek

Lekin jab exception "expected/normal" ho aur bohat baar aaye, to `if` sasta rehta hai — andaza se nahi, **measure** karke faisla karo.
"""))
A(code(r'''
from collections import defaultdict, Counter

stock = {"pen": 12, "book": 3}

# ============ 1.4a dict.get ============
print("BAD  (if-in-else):")
if "eraser" in stock:                    # do lookups: 'in' + indexing
    qty = stock["eraser"]
else:
    qty = 0
print("   qty =", qty)

print("GOOD (get with default):")
qty = stock.get("eraser", 0)             # ek lookup, ek line
print("   qty =", qty)
print("get() dict ko modify nahi karta ->", stock)   # 'eraser' add nahi hui

# get() ka doosra rup: nested/chained safe access
config = {"db": {"host": "localhost"}}
print("nested get ->", config.get("db", {}).get("port", 5432))   # missing port -> default

# ============ 1.4b grouping: manual vs setdefault vs defaultdict ============
words = ["apple", "avocado", "banana", "blueberry", "cherry", "apricot"]

# BAD: manual key existence check
by_letter_bad = {}
for w in words:
    first = w[0]
    if first not in by_letter_bad:        # har iteration me manual check
        by_letter_bad[first] = []
    by_letter_bad[first].append(w)

# BETTER: setdefault (ek line, koi extra import nahi)
by_letter_sd = {}
for w in words:
    by_letter_sd.setdefault(w[0], []).append(w)   # missing -> [] daalo, phir append

# BEST (readable + fast): defaultdict
by_letter_dd = defaultdict(list)
for w in words:
    by_letter_dd[w[0]].append(w)          # missing key par list khud ban jati hai

assert by_letter_bad == by_letter_sd == dict(by_letter_dd)
print("\ngrouped:", dict(by_letter_dd))

# defaultdict(int) counting, aur Counter (isse behtar)
counts_dd = defaultdict(int)
for ch in "mississippi":
    counts_dd[ch] += 1                    # missing -> 0 se shuru
print("defaultdict(int):", dict(counts_dd))
print("Counter        :", dict(Counter("mississippi")))
print("top-2          :", Counter("mississippi").most_common(2))

# GOTCHA: defaultdict me missing key PADHNE se bhi key ban jati hai
dd = defaultdict(list)
_ = dd["ghost"]                           # sirf read kiya... par
print("defaultdict read ne key bana di ->", dict(dd))
plain = {}
print("plain dict .get() se kuch nahi banta ->", plain.get("ghost", []), plain)

# ============ 1.4c EAFP vs LBYL ============
def get_price_lbyl(prices, item):
    # LBYL: pehle dekho phir chalo (do lookups, race-condition ka risk)
    if item in prices:
        return prices[item]
    return None

def get_price_eafp(prices, item):
    # EAFP: seedha try karo, galat ho to sambhal lo (Pythonic)
    try:
        return prices[item]
    except KeyError:
        return None

prices = {"pen": 50}
print("\nLBYL:", get_price_lbyl(prices, "pen"), get_price_lbyl(prices, "bag"))
print("EAFP:", get_price_eafp(prices, "pen"), get_price_eafp(prices, "bag"))

# EAFP type conversion me bohat kaam aata hai
raw_inputs = ["10", "abc", "3.5", "", "42"]
def to_int_eafp(s):
    try:
        return int(s)                     # jo ban jaye
    except ValueError:
        return None                       # jo na bane
print("parsed:", [to_int_eafp(s) for s in raw_inputs])

# LBYL ka classic fail: str.isdigit() negative numbers ko reject kar deta hai
print('"-5".isdigit() ->', "-5".isdigit(), "| int('-5') ->", to_int_eafp("-5"), " <- LBYL yahan galat")
print("[ok] 1.4 done")
'''))

# ---------------------------------------------------------------- idioms IV
A(md("""
## 1.5 `"".join()` vs loop me `+=` (timing ke sath), aur `str.translate()` / `str.maketrans()`

### Strings immutable hain
Python strings **immutable** hain. `s += "x"` naya string banata hai aur purana copy karta hai.
Loop me ye O(n²) work ban jata hai (CPython ka ek internal optimization kabhi bacha leta hai, magar
uspar bharosa **nahi** karna — dusre interpreters (PyPy/Jython) me nahi hota).

**Rule:** pieces ko `list` me jama karo, aakhir me `"".join(pieces)` — ye O(n) hai:
`join` pehle total length nikalta hai, ek hi buffer allocate karta hai, phir copy karta hai.

### `str.translate()` + `str.maketrans()`
Character-level bulk replace/delete ka **sabse tez** tareeqa (C level me table lookup):
```python
table = str.maketrans("aeiou", "12345")        # 1-to-1 mapping
table = str.maketrans("", "", string.punctuation)   # 3rd arg = delete karo
s.translate(table)
```
Multiple `.replace()` calls ki chain se behtar hai kyunki string ek hi baar traverse hoti hai
aur intermediate strings nahi banti.
"""))
A(code(r'''
import timeit, string

# ============ 1.5a += vs join (timing) ============
N = 3000            # chhota rakha hai taake notebook fast rahe

def build_with_plus(n):
    s = ""
    for i in range(n):
        s += "x"                     # har baar naya string object (copy)
    return s

def build_with_join(n):
    parts = []                       # pieces jama karo
    for i in range(n):
        parts.append("x")
    return "".join(parts)            # ek hi baar allocate + copy

def build_with_comprehension(n):
    return "".join("x" for _ in range(n))   # sabse compact idiom

assert build_with_plus(N) == build_with_join(N) == build_with_comprehension(N)

REPEAT = 40
t_plus = timeit.timeit(lambda: build_with_plus(N), number=REPEAT)
t_join = timeit.timeit(lambda: build_with_join(N), number=REPEAT)
t_comp = timeit.timeit(lambda: build_with_comprehension(N), number=REPEAT)

print(f"+= loop        : {t_plus*1000:8.2f} ms   (BAD  - O(n^2) soch ke likho)")
print(f"list + join    : {t_join*1000:8.2f} ms   (GOOD)")
print(f"genexp + join  : {t_comp*1000:8.2f} ms   (GOOD, sabse Pythonic)")
print("Note: exact numbers machine par depend karte hain; trend important hai.")

# Practical example: CSV jaisi line banana
rows = [("Ali", 88), ("Sara", 92)]
print("\nBAD  :", " | ".join(f"{n}={m}" for n, m in rows))   # yahi GOOD bhi hai :)
line = ",".join(str(x) for row in rows for x in row)          # nested comprehension + join
print("flat  :", line)

# ============ 1.5b translate / maketrans ============
text = "Hello, World! Python's idioms... aren't they great?"

# BAD: replace ki lambi chain (har call naya string banata hai)
cleaned_bad = text
for p in string.punctuation:
    cleaned_bad = cleaned_bad.replace(p, "")

# GOOD: ek hi translate pass, 3rd argument = delete list
drop_punct = str.maketrans("", "", string.punctuation)
cleaned_good = text.translate(drop_punct)

print("\npunctuation removed (replace chain):", cleaned_bad)
print("punctuation removed (translate)    :", cleaned_good)
assert cleaned_bad == cleaned_good

t_replace = timeit.timeit(lambda: [text.replace(p, "") for p in string.punctuation], number=2000)
t_trans   = timeit.timeit(lambda: text.translate(drop_punct), number=2000)
print(f"replace-chain: {t_replace*1000:7.2f} ms   translate: {t_trans*1000:7.2f} ms")

# 1-to-1 character mapping (leetspeak / rot-style / masking)
leet = str.maketrans("aeiost", "43105+")
print("leet   :", "association of testers".translate(leet))

# maketrans dict form: keys ko ord() se int hona chahiye ya single char
mask = str.maketrans({str(d): "*" for d in range(10)})   # sab digits -> *
print("masked :", "card 4111-1111-1111-1111".translate(mask))

# Multi-char replacement translate se NAHI hota -> wahan replace/re use karo
print("multi-char ke liye replace:", "colour theatre".replace("our", "or").replace("tre", "ter"))
print("[ok] 1.5 done")
'''))

# ---------------------------------------------------------------- idioms V
A(md("""
## 1.6 Slicing tricks aur `_` ke saare conventions

### Slicing: `seq[start:stop:step]`
- `[::-1]` → poora ulta (reverse). String reverse ka Pythonic tareeqa.
- `[::2]` → har doosra element. `[1::2]` → odd indexes.
- `[:]` → **shallow copy** (nayi list, wahi andar ke objects)
- `del lst[2:5]` → beech se elements nikal do (in place)
- `lst[2:4] = [...]` → slice assignment: length badal bhi sakti hai (in place)
- Slicing **out-of-range se crash nahi karti**: `lst[:100]` safe hai, `lst[100]` `IndexError` deta hai.

### `_` ke 5 chehre (interview me poocha jata hai)
1. **Throwaway variable:** `for _ in range(3):`, `_, y = point` — "mujhe is value se kaam nahi".
2. **`_single_leading`**: "internal / private, please don't touch" — sirf **convention** hai, enforce nahi hota.
   `from module import *` inko skip karta hai.
3. **`__double_leading` (dunder prefix)**: class ke andar **name mangling** — `self.__x` → `self._ClassName__x`.
   Maqsad *privacy nahi*, subclass ke sath naam ki takkar (collision) rokna hai.
4. **`__dunder__` (both sides)**: Python ke special/magic methods — `__init__`, `__len__`. Apne naam aise **na** banao.
5. **REPL `_`**: interactive shell me pichhle expression ka result `_` me hota hai (notebook/script me ye
   automatic nahi — is liye neeche hum manually dikhate hain).
6. **Digit separators:** `1_000_000`, `0xFF_FF`, `3.141_592` — sirf padhne ke liye, value par asar nahi.
   `int("1_000")` bhi chalta hai.
"""))
A(code(r'''
# ============ 1.6a slicing tricks ============
nums = list(range(10))
word = "interview"
print("nums:", nums)

print("reverse  nums[::-1] ->", nums[::-1])
print("reverse  word[::-1] ->", word[::-1])          # string reverse ka Pythonic tareeqa
print("every 2  nums[::2]  ->", nums[::2])
print("odd idx  nums[1::2] ->", nums[1::2])
print("last 3   nums[-3:]  ->", nums[-3:])
print("drop last nums[:-1] ->", nums[:-1])
print("middle   nums[2:7]  ->", nums[2:7])
print("step -2  nums[::-2] ->", nums[::-2])

# BAD reverse: manual loop
rev_bad = []
for i in range(len(nums) - 1, -1, -1):
    rev_bad.append(nums[i])
assert rev_bad == nums[::-1]
print("manual reverse == nums[::-1] ?", rev_bad == nums[::-1], " -> loop ki zaroorat nahi thi")

# reversed() vs [::-1]: reversed() lazy iterator hai (memory sasti), [::-1] nayi list banati hai
print("reversed() ->", list(reversed(nums))[:4], "... (lazy iterator)")

# [:] = shallow copy vs alias
original = [1, 2, 3]
alias = original                   # SAME object (do naam, ek list)
shallow = original[:]              # NAYI list (copy)
alias.append(99)
print("\nalias ke baad original:", original, "| shallow copy:", shallow)
print("alias is original ?", alias is original, "| shallow is original ?", shallow is original)

# del slice + slice assignment (in-place operations)
letters = list("abcdefg")
del letters[2:5]                   # index 2,3,4 gayab
print("after del [2:5] ->", letters)
letters[1:1] = ["X", "Y"]          # insert without append/insert loop
print("after insert    ->", letters)
letters[::2] = ["-"] * len(letters[::2])   # extended slice assignment (length match zaroori)
print("after step-assign ->", letters)

# Slicing out-of-range safe hai, indexing nahi
print("\nnums[:100] safe ->", nums[:100][-1])
try:
    nums[100]
except IndexError as e:
    print("IndexError:", e)

# ============ 1.6b _ conventions ============
# 1) throwaway
for _ in range(3):                 # counter ki value chahiye nahi
    pass
point = (3, 7)
_, y_coord = point                 # sirf y chahiye
print("\nthrowaway _ ->  y =", y_coord)

first, *_middle, last = [1, 2, 3, 4, 5]        # _middle bhi "mujhe farq nahi" wala naam
print("first/last:", first, last, "| ignored:", _middle)

# 2 & 3) _private aur __mangled
class Account:
    def __init__(self, balance):
        self.balance = balance             # public API
        self._audit_log = []               # convention: internal, chhero mat
        self.__pin = "1234"                # name mangling -> _Account__pin

    def check_pin(self, pin):
        return pin == self.__pin           # class ke andar naam kaam karta hai

acc = Account(500)
print("public   :", acc.balance)
print("internal :", acc._audit_log, "(access ho gaya - Python rokta nahi, sirf convention hai)")
print("mangled attrs:", [k for k in vars(acc) if "pin" in k])
print("check_pin('1234') ->", acc.check_pin("1234"))
try:
    print(acc.__pin)                       # bahar se __pin naam mojood nahi
except AttributeError as e:
    print("AttributeError:", e)
print("par mangled naam se mil jata hai ->", acc._Account__pin, "(privacy nahi, collision-safety hai)")

# 4) __dunder__ = Python ke special methods
print("dunder example: len('abcd') ->", "abcd".__len__())

# 5) REPL _ ka behaviour simulate
_repl_history = []
_repl_history.append(2 + 3)
print("REPL me: >>> 2+3 ; >>> _  -> ", _repl_history[-1], "(script me automatic nahi hota)")

# 6) digit separators
budget = 1_500_000                        # readable
mask16 = 0xFF_FF
pi_ish = 3.141_592_653
print("\n1_500_000 ->", budget, "| 0xFF_FF ->", mask16, "| 3.141_592_653 ->", pi_ish)
print('int("1_000") ->', int("1_000"), "| f-string comma format ->", f"{budget:,}")
assert budget == 1500000 and mask16 == 65535
print("[ok] 1.6 done")
'''))

# ---------------------------------------------------------------- idioms VI
A(md("""
## 1.7 Ternary expression, walrus `:=`, f-string debugging aur format specs

### Ternary (conditional expression)
`value = A if condition else B` — ek **expression** hai (value deti hai), is liye comprehension,
function argument, aur `return` me seedha lag sakti hai.
Nested ternary (`a if x else b if y else c`) padhna mushkil ho jata hai → 2 se zyada branches ho to
normal `if/elif` ya dict-dispatch use karo.

### Walrus `:=` (assignment expression, Python 3.8+)
"assign **aur** value wapas do" — jahan hum ek value pehle compute karte hain phir usko condition me use karte hain:
- `if (n := len(data)) > 10:` → `n` baad me bhi available
- `while (chunk := f.read(1024)):` → read-and-test ek line me
- comprehension me repeat calculation bachana: `[y for x in xs if (y := heavy(x)) > 0]`

**Kab NA use karo:** sirf "cool" dikhne ke liye. Agar line samajhne me ruk jaye to normal do lines behtar hain.

### f-string debugging `f"{x=}"` (3.8+)
`f"{total=}"` → `total=42` — variable ka **naam + value** dono. `print` debugging ka best friend.
`f"{a + b = :.2f}"` bhi chalta hai (expression + format spec).

### Format specs (cheat-sheet)
| Spec | Matlab | Example |
|---|---|---|
| `:.2f` | 2 decimal fixed | `f"{3.14159:.2f}"` → `3.14` |
| `:>10` / `:<10` / `:^10` | right / left / center pad | `f"{'hi':>5}"` → `'   hi'` |
| `:,` / `:_` | thousands separator | `f"{1234567:,}"` → `1,234,567` |
| `:05d` | zero padding | `f"{42:05d}"` → `00042` |
| `:.1%` | percent | `f"{0.256:.1%}"` → `25.6%` |
| `:+d` | sign always | `f"{5:+d}"` → `+5` |
| `:#x` / `:b` / `:o` / `:e` | hex / binary / octal / scientific | `f"{255:#x}"` → `0xff` |
| `:{w}.{p}f` | nested (dynamic) spec | width/precision variable se |
| `!r` | `repr()` | `f"{'hi'!r}"` → `'hi'` |
"""))
A(code(r'''
# ============ 1.7a ternary ============
marks_list = [95, 67, 42, 88, 33]

# BAD: 4 line if/else jahan ek expression kaafi thi
def label_bad(m):
    if m >= 50:
        return "pass"
    else:
        return "fail"

# GOOD: ternary
def label_good(m):
    return "pass" if m >= 50 else "fail"

print([label_bad(m) for m in marks_list] == [label_good(m) for m in marks_list])
print("labels:", [label_good(m) for m in marks_list])

# Ternary comprehension ke andar (conditional VALUE - filter nahi)
print("capped :", [m if m <= 90 else 90 for m in marks_list])

# Nested ternary padhna mushkil -> readable alternative
def grade_nested(m):
    return "A" if m >= 80 else ("B" if m >= 60 else ("C" if m >= 40 else "F"))

def grade_readable(m):
    # bisect/loop style: thresholds table -> add karna aasan, padhna aasan
    for cutoff, g in ((80, "A"), (60, "B"), (40, "C")):
        if m >= cutoff:
            return g
    return "F"

assert [grade_nested(m) for m in marks_list] == [grade_readable(m) for m in marks_list]
print("grades :", [grade_readable(m) for m in marks_list])

# ============ 1.7b walrus := ============
data = [3, 9, 27, 81]

# BAD: len do baar / pehle assign phir if
n = len(data)
if n > 3:
    print("BAD  style: length", n)

# GOOD: assign + test ek sath
if (n := len(data)) > 3:
    print("GOOD walrus: length", n, "(n baad me bhi zinda hai)")

# while loop me read-and-test (chunk processing ka classic)
import io
stream = io.StringIO("abcdefghij")
chunks = []
while (chunk := stream.read(4)):        # khali string falsy -> loop khatam
    chunks.append(chunk)
print("chunks:", chunks)

# iterator + sentinel
it = iter([5, 6, 7])
out = []
while (val := next(it, None)) is not None:   # sentinel None (khyal: 0 valid value ho sakti hai!)
    out.append(val)
print("drained:", out)

# comprehension me double-computation bachana
calls = []
def slow_square(x):
    calls.append(x)                     # kitni baar chala?
    return x * x

no_walrus = [slow_square(x) for x in range(6) if slow_square(x) > 8]   # 2x calls!
print("\nbina walrus calls:", len(calls))
calls.clear()
with_walrus = [y for x in range(6) if (y := slow_square(x)) > 8]        # 1x calls
print("walrus ke sath calls:", len(calls))
assert no_walrus == with_walrus == [9, 16, 25]

# ============ 1.7c f-string debugging ============
total, count, name = 250, 4, "Ali"
print("\nold way :", "total =", total, "count =", count)
print(f"new way : {total=} {count=} {name=}")          # naam + value automatic
print(f"expression bhi: {total / count = }")           # spaces bhi preserve hote hain
print(f"format ke sath: {total / count = :.2f}")

# ============ 1.7d format specs ============
pi = 3.14159265
big = 9876543.21
print("\n:.2f    ->", f"{pi:.2f}")
print(":>10    ->", repr(f"{'hi':>10}"))
print(":<10    ->", repr(f"{'hi':<10}"))
print(":^11    ->", repr(f"{'mid':^11}"))
print(":,      ->", f"{big:,.2f}")
print(":_      ->", f"{1234567:_}")
print(":05d    ->", f"{42:05d}")
print(":+d     ->", f"{5:+d}", f"{-5:+d}")
print(":.1%    ->", f"{0.2567:.1%}")
print(":#x :b  ->", f"{255:#x}", f"{5:b}")
print(":.3e    ->", f"{0.000123456:.3e}")
print("!r      ->", f"{'hi'!r}")

# Nested (dynamic) spec: width/precision variables se
w, p = 12, 3
print("dynamic ->", repr(f"{pi:>{w}.{p}f}"))

# Aligned table banane ka idiom (report printing ka basic)
report = [("Ali", 88, 0.88), ("Sara", 92, 0.92), ("Abdul-Rehman", 75, 0.75)]
print(f"\n{'Name':<14}{'Marks':>6}{'Pct':>8}")
print("-" * 28)
for nm, mk, pct in report:
    print(f"{nm:<14}{mk:>6}{pct:>8.1%}")
print("[ok] 1.7 done")
'''))

# ---------------------------------------------------------------- comprehension I
A(md("""
---
# Part 2 — Comprehension Mastery

## 2.1 List comprehension: filtering vs conditional value

**Kya hai:** ek expression jo iterable se nayi list banati hai.

```
[  expression   for item in iterable   if condition  ]
   ^ VALUE            ^ LOOP              ^ FILTER
```

Padhne ka tareeqa (English me bolo): *"expression, for each item in iterable, if condition"*.

**Do bilkul alag cheezein — inko mix na karo:**
1. **Filtering** → `if` **aakhir** me: `[x for x in nums if x % 2 == 0]` → output **chhota** ho sakta hai.
2. **Conditional value (ternary)** → `if/else` **shuru** me: `[x if x > 0 else 0 for x in nums]` →
   output ki length **wahi** rehti hai, sirf values badalti hain.
3. Dono sath: `[x * 2 if x % 3 else -1 for x in nums if x > 2]`

**Kyun use karein:**
- Intent clear: "main nayi list bana raha hoon" (loop ka matlab kuch bhi ho sakta hai)
- Thora fast: `.append` ka attribute lookup + function call har baar nahi hota
- Expression hai → seedha function argument me pass ho sakti hai

**Kab NA karein:** side effects ke liye (`[print(x) for x in items]` ← bad; ye list bana kar phenk deta hai).
Side effect chahiye to normal `for` loop likho.

**Interview tip:** `map`/`filter` vs comprehension — comprehension zyada readable hai; `map(str, nums)`
jaisa built-in-function case thora fast ho sakta hai, magar `map(lambda x: ..., nums)` par comprehension jeet jati hai.
"""))
A(code(r'''
nums = [-4, -1, 0, 3, 5, 8, 11, 12]

# ---- BAD: loop + append (kaam karta hai, magar shor zyada hai)
squares_bad = []
for x in nums:
    squares_bad.append(x * x)

# ---- GOOD: list comprehension
squares_good = [x * x for x in nums]
assert squares_bad == squares_good
print("squares      :", squares_good)

# ---- 1) FILTERING: if aakhir me -> length chhoti ho sakti hai
evens = [x for x in nums if x % 2 == 0]
print("evens (filter):", evens, "| length", len(nums), "->", len(evens))

# multiple conditions: 'and' ya do 'if' (dono barabar hain)
both = [x for x in nums if x > 0 if x % 2 == 0]      # = if x > 0 and x % 2 == 0
print("positive+even :", both)

# ---- 2) CONDITIONAL VALUE: ternary shuru me -> length same
clipped = [x if x > 0 else 0 for x in nums]
print("clipped (map) :", clipped, "| length same:", len(clipped) == len(nums))

# ---- 3) Dono ek sath (pehle filter, phir value transform)
mixed = [("big" if x > 6 else "small") for x in nums if x > 0]
print("mixed         :", mixed)

# ---- map / filter se comparison
print("\nmap(str, nums)          :", list(map(str, nums))[:4], "...")
print("comprehension equivalent:", [str(x) for x in nums][:4], "...")
print("filter(None, ...) falsy hata deta hai:", list(filter(None, [0, 1, "", "a", [], [2]])))

# ---- comprehension me function call + unpacking
pairs = [("Ali", 88), ("Sara", 92), ("Bilal", 75)]
names_upper = [name.upper() for name, _ in pairs]        # tuple unpacking loop me
print("names_upper   :", names_upper)
print("pass list     :", [n for n, m in pairs if m >= 80])

# ---- ANTI-PATTERN: side effect ke liye comprehension
print("\nBAD: [print(x) for x in ...] -> ek bekaar list [None, None] bhi banati hai")
junk = [print("   printing", x) for x in (1, 2)]
print("wo bekaar list:", junk, " <- memory waste; normal for loop likho")

# ---- comprehension variable leak NAHI karta (Python 3)
try:
    _ = [q for q in range(3)]
    print(q)                       # NameError - q comprehension ke andar hi zinda tha
except NameError as e:
    print("NameError:", e, "-> comprehension ka scope alag hai (Python 3 me leak nahi hota)")
print("[ok] 2.1 done")
'''))

# ---------------------------------------------------------------- comprehension II
A(md("""
## 2.2 Dict / set comprehension, nested loops, flattening

### Dict comprehension
`{key_expr: value_expr for item in iterable if cond}` — dict invert, filter, transform sab isse.
Duplicate key aaye to **aakhri wali jeet jati hai** (silent overwrite — dict invert karte waqt gotcha).

### Set comprehension
`{expr for item in iterable}` — automatic dedupe. Khyal: `{}` khali **dict** hai, khali set `set()` hai.

### Nested loops in comprehension
Order **wahi** hota hai jo normal nested loop ka:
```python
[(i, j) for i in range(2) for j in range(3)]     # i outer, j inner
```
==
```python
for i in range(2):
    for j in range(3):
        ...
```
Inner loop outer ke variable ko use kar sakta hai: `[c for word in words for c in word]` ← **flattening**.

**Yaad rakhne ka trick:** `for` clauses **left-to-right** wahi order me likho jaise normal loops nest karte ho;
**expression** sabse pehle likha jata hai (magar sabse aakhir me chalta hai).

### Nested comprehension (list of lists)
`[[i * j for j in range(3)] for i in range(3)]` → matrix. Andar wali comprehension **value** hai, loop nahi.
Ye "flatten" wale se bilkul alag hai — dhyan se dekho.
"""))
A(code(r'''
# ============ 2.2a dict comprehension ============
marks = {"Ali": 88, "Sara": 92, "Bilal": 75, "Hina": 59}

# BAD: loop + assignment
scaled_bad = {}
for k, v in marks.items():
    scaled_bad[k] = v / 100

# GOOD
scaled = {k: v / 100 for k, v in marks.items()}
assert scaled_bad == scaled
print("scaled      :", scaled)

# filter + transform ek sath
toppers = {k.upper(): v for k, v in marks.items() if v >= 80}
print("toppers     :", toppers)

# invert (value -> key)
inverted = {v: k for k, v in marks.items()}
print("inverted    :", inverted)

# GOTCHA: duplicate values -> invert me keys kha jati hain
dupe = {"a": 1, "b": 1, "c": 2}
print("dupe invert :", {v: k for k, v in dupe.items()}, "<- 'a' gum ho gaya (last wins)")

# safe invert: value -> list of keys (defaultdict/setdefault ka comprehension version)
from collections import defaultdict
safe = defaultdict(list)
for k, v in dupe.items():
    safe[v].append(k)
print("safe invert :", dict(safe))

# zip se dict banana
cols = ["id", "name", "city"]
row = [7, "Ali", "Karachi"]
print("row -> dict :", {c: val for c, val in zip(cols, row, strict=True)})
print("ya sirf     :", dict(zip(cols, row, strict=True)))

# dict comprehension se lookup table (fast membership/mapping)
squares_table = {n: n * n for n in range(1, 6)}
print("squares tbl :", squares_table)

# ============ 2.2b set comprehension ============
words = ["apple", "Banana", "APPLE", "cherry", "banana"]
unique_lower = {w.lower() for w in words}                 # dedupe + normalize
print("\nunique     :", sorted(unique_lower))
print("lengths set :", {len(w) for w in words})
print("khali set   :", type({}).__name__, "vs", type(set()).__name__, "<- {} dict hai!")

# vowels nikalna (set = fast membership test)
VOWELS = set("aeiou")
print("vowels in 'comprehension':", sorted({ch for ch in "comprehension" if ch in VOWELS}))

# ============ 2.2c nested loops in comprehension ============
pairs = [(i, j) for i in range(3) for j in "ab"]          # i outer, j inner
print("\npairs      :", pairs)

# barabar wala normal loop (order same)
manual = []
for i in range(3):
    for j in "ab":
        manual.append((i, j))
assert manual == pairs

# condition dono levels par lag sakti hai
coprime_ish = [(i, j) for i in range(1, 5) for j in range(1, 5) if i != j if (i + j) % 2 == 0]
print("filtered    :", coprime_ish)

# inner loop outer variable use kar sakta hai (jagged data)
matrix = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flat = [x for row in matrix for x in row]                 # FLATTENING idiom
print("flatten     :", flat)

# yaad rakho: 'for row' pehle, 'for x' baad me - ulta likhne par NameError
try:
    bad = [x for x in row for row in matrix]              # row abhi define nahi hua tha
    print("ye chal gaya kyunki 'row' pehle cell me bacha hua tha:", bad[:3], "... (dhoka!)")
except NameError as e:
    print("NameError:", e)

# nested comprehension = list of lists (andar wali comprehension VALUE hai)
table = [[i * j for j in range(1, 5)] for i in range(1, 4)]
print("nested comp :", table)
print("flatten wapas:", [x for row_ in table for x in row_])

# 3-level flatten (arbitrary depth ke liye recursion behtar - Part 8 problem #2 dekho)
deep = [[[1, 2], [3]], [[4], [5, 6]]]
print("2-level flat:", [x for mid in deep for inner in mid for x in inner])
print("[ok] 2.2 done")
'''))

# ---------------------------------------------------------------- comprehension III
A(md("""
## 2.3 Comprehension vs Generator expression (memory), aur "kab comprehension unreadable ho jati hai"

### `[...]` vs `(...)`
| | List comprehension `[x for ...]` | Generator expression `(x for ...)` |
|---|---|---|
| Kab compute | **foran**, poori list | **lazy**, ek waqt me ek item |
| Memory | O(n) — sab items RAM me | O(1) — bas state |
| Dobara use | haan, list rehti hai | **nahi** — ek baar exhaust, khatam |
| `len()` / indexing | haan | nahi |
| Best for | list chahiye, dobara loop chalana hai | ek hi baar loop, ya bohat bara/infinite data |

**Idiom:** `sum(x*x for x in nums)` — list banane ki koi zaroorat nahi. Extra brackets bhi nahi chahiye jab
genexp function ka **single** argument ho.

**Gotcha 1 — exhaustion:** ek genexp par doosra `sum()` chalaoge to `0` milega (khatam ho chuka hai).
**Gotcha 2 — late binding:** genexp ke andar ka variable **iterate karte waqt** padha jata hai (sirf pehla
iterable foran evaluate hota hai) — beech me variable badal do to natija badal jayega.
**Gotcha 3:** `min`/`max`/`sorted`/`any`/`all` genexp se khush hain, magar `len()` nahi.

### Kab comprehension **unreadable** ho jati hai (rule of thumb)
Refactor kar do agar:
1. 2 se zyada `for` clauses hain, **ya**
2. `for` + `if` mila kar 3 se zyada clauses hain, **ya**
3. ek line 79 columns se lambi ho rahi hai, **ya**
4. andar nested ternary hai, **ya**
5. tumhe khud padhne ke liye ruk kar sochna par gaya 🙂

**Refactor ke 3 tareeqe:** (a) named helper function bana lo, (b) do steps me tor do (do comprehensions),
(c) sirf normal `for` loop likh do — loop koi gunah nahi hai.
"""))
A(code(r'''
import sys, timeit

nums = list(range(100_000))          # 1_00_000 items (digit separator readability ke liye)

# ============ 2.3a memory: list vs generator ============
list_comp = [x * x for x in nums]                 # sab kuch foran RAM me
gen_exp   = (x * x for x in nums)                 # sirf recipe

print("list comp size :", f"{sys.getsizeof(list_comp):>9,} bytes")
print("genexp    size :", f"{sys.getsizeof(gen_exp):>9,} bytes  <- constant, data ka size se azaad")
print("ratio          :", f"{sys.getsizeof(list_comp) / sys.getsizeof(gen_exp):,.0f}x")
print("type           :", type(list_comp).__name__, "vs", type(gen_exp).__name__)

# sum: extra list ki zaroorat nahi
print("\nsum(list comp) :", sum([x * x for x in range(1000)]))
print("sum(genexp)    :", sum(x * x for x in range(1000)), " <- ek hi pair of brackets, list nahi bani")

t_list = timeit.timeit(lambda: sum([x * x for x in range(2000)]), number=200)
t_gen  = timeit.timeit(lambda: sum(x * x for x in range(2000)), number=200)
print(f"timing -> list: {t_list*1000:6.1f} ms | genexp: {t_gen*1000:6.1f} ms "
      "(chhote data par list thori tez, magar memory genexp ki jeet)")

# ============ 2.3b GOTCHA: genexp ek baar chalta hai ============
g = (x for x in range(5))
print("\npehla  sum(g):", sum(g))
print("doosra sum(g):", sum(g), " <- 0! generator exhaust ho gaya (silent bug)")
print("list par     :", (lambda L: (sum(L), sum(L)))([x for x in range(5)]), " <- list dobara chalti hai")

# GOTCHA: genexp lazy hai -> beech me data badla to result badal jata hai
base = [1, 2, 3]
lazy = (x * 10 for x in base)         # 'base' ka reference foran liya, values baad me
base.append(4)                        # abhi tak iterate nahi hua...
print("lazy result :", list(lazy), " <- 4 bhi aa gaya!")

# any/all + genexp = short circuit (poori list banane ki zaroorat nahi)
big_check = any(x > 5 for x in range(1_000_000))    # 7th item par ruk jata hai
print("any short-circuit ->", big_check)

# len() genexp par nahi chalta -> sum(1 for _ in ...) ka idiom
gen2 = (x for x in range(7) if x % 2)
try:
    len(gen2)
except TypeError as e:
    print("TypeError:", e, "-> count karne ka idiom: sum(1 for _ in gen)")
print("count via sum(1 for _):", sum(1 for _ in (x for x in range(7) if x % 2)))

# ============ 2.3c readability: kab refactor karein ============
students = [
    {"name": "Ali", "marks": [80, 90, 70], "active": True},
    {"name": "Sara", "marks": [95, 85, 100], "active": True},
    {"name": "Bilal", "marks": [40, 55, 60], "active": False},
    {"name": "Hina", "marks": [60, 65, 75], "active": True},
]

# BAD: sab kuch ek line me (3 clauses + nested ternary) -> dimaag ka dahi
ugly = [(s["name"], "A" if sum(s["marks"]) / len(s["marks"]) >= 85 else ("B" if sum(s["marks"]) / len(s["marks"]) >= 65 else "C")) for s in students if s["active"] and len(s["marks"]) > 0]
print("\nugly one-liner:", ugly)

# GOOD (a): named helper functions -> intent nazar aata hai, test bhi ho sakta hai
def average(marks):
    return sum(marks) / len(marks) if marks else 0.0

def grade_of(marks):
    avg = average(marks)
    if avg >= 85:
        return "A"
    if avg >= 65:
        return "B"
    return "C"

pretty = [(s["name"], grade_of(s["marks"])) for s in students if s["active"]]
print("readable      :", pretty)
assert pretty == ugly            # bilkul wahi natija, magar padha ja sakta hai

# GOOD (b): do steps me tor do
active = [s for s in students if s["active"]]                 # step 1: filter
graded = {s["name"]: grade_of(s["marks"]) for s in active}    # step 2: transform
print("two-step      :", graded)

# GOOD (c): normal loop - jab har item par kaam lamba ho (logging, try/except, multiple outputs)
report = {}
for s in students:
    if not s["active"]:
        continue                      # guard clause -> nesting kam
    report[s["name"]] = {"avg": round(average(s["marks"]), 1), "grade": grade_of(s["marks"])}
print("loop version  :", report)
print("[ok] 2.3 done")
'''))

# ---------------------------------------------------------------- copy
A(md("""
---
# Part 3 — Shallow vs Deep Copy (nested structures) + Mutable Default Argument Trap

## Teen alag cheezein
```python
b = a              # ALIAS   -> koi copy nahi. do naam, ek hi object.
b = a.copy()       # SHALLOW -> nayi outer container, andar wale objects SHARED
b = copy.deepcopy(a)  # DEEP -> recursively sab kuch naya
```

Shallow copy ke tareeqe: `list(a)`, `a[:]`, `a.copy()`, `copy.copy(a)`, `dict(d)`, `{**d}` — **sab shallow hain**.
Ye sirf top level naya banate hain. Agar andar list/dict/object hai to wo **share** hoti hai → ek jagah change
karne se doosri jagah bhi dikhta hai. Yehi bug production me ghanton kharab karta hai.

## `is` vs `==`
- `==` → **values barabar hain?** (`__eq__` chalta hai)
- `is` → **wahi object hai?** (memory identity, `id()` same)

Deep copy ke baad: `a == b` → `True`, `a is b` → `False`.
`is` sirf `None` / `True` / `False` / sentinel objects ke sath use karo. Chhote int aur short strings CPython
cache karta hai (`a = 256; b = 256; a is b` → `True`) — is par **kabhi** logic na banao.

## Mutable default argument trap
```python
def add(item, bucket=[]):      # BAD: default ek hi baar (function define hote waqt) banta hai
    bucket.append(item)
    return bucket
```
Har call **wahi** list share karti hai → values jama hoti rehti hain.
**Fix:** `def add(item, bucket=None): bucket = [] if bucket is None else bucket`.
Yehi trap `{}`, `set()`, `datetime.now()`, aur mutable class attributes ke sath bhi hai.
"""))
A(code(r'''
import copy

original = {"name": "Ali", "marks": [80, 90], "meta": {"city": "Karachi"}}

alias    = original                      # 1) alias
shallow  = copy.copy(original)           # 2) shallow (== dict(original) == {**original})
deep     = copy.deepcopy(original)       # 3) deep

# top level change
alias["name"] = "ALIAS-CHANGED"
print("alias ne original ko badal diya ->", original["name"])
original["name"] = "Ali"                 # wapas theek

shallow["name"] = "SHALLOW-ONLY"         # top level: alag hai
print("shallow top-level change -> original:", original["name"], "| shallow:", shallow["name"])

# NESTED change - yahan asli farq nazar aata hai
shallow["marks"].append(999)             # andar wali list SHARED hai!
print("\nnested change via shallow:")
print("  original['marks'] :", original["marks"], "<- ye bhi badal gayi!")
print("  shallow['marks']  :", shallow["marks"])
print("  same object?      :", original["marks"] is shallow["marks"])

deep["marks"].append(-1)                 # deep copy ka apna alag object
print("nested change via deep:")
print("  original['marks'] :", original["marks"], "<- mehfooz")
print("  deep['marks']     :", deep["marks"])
print("  same object?      :", original["marks"] is deep["marks"])

# saare shallow tareeqe barabar hain
lst = [[1, 2], [3, 4]]
copies = [lst[:], list(lst), lst.copy(), copy.copy(lst)]
print("\nsab shallow hain? ->", [c[0] is lst[0] for c in copies], "(andar wali list shared)")
deep_lst = copy.deepcopy(lst)
print("deepcopy           ->", deep_lst[0] is lst[0], "| values equal?", deep_lst == lst)

# 2D matrix banane ka classic BUG: [[0]*3]*2
bug_matrix = [[0] * 3] * 2               # 2 references, ek hi row!
bug_matrix[0][0] = 9
print("\nBAD  [[0]*3]*2 ->", bug_matrix, " <- dono rows badal gayi")
good_matrix = [[0] * 3 for _ in range(2)]   # GOOD: har row nayi
good_matrix[0][0] = 9
print("GOOD comprehension ->", good_matrix)

# ============ is vs == ============
a1 = [1, 2, 3]
a2 = [1, 2, 3]
print("\n[1,2,3] == [1,2,3] ->", a1 == a2, "| is ->", a1 is a2)
print("deep copy: == ->", deep_lst == lst, "| is ->", deep_lst is lst)
small_a, small_b = 256, 256
print("256 is 256 ->", small_a is small_b, "(CPython cache - is par logic na banao)")
big_a, big_b = 1000, 1000
print("1000 is 1000 ->", big_a is big_b, "(implementation detail; kabhi bhi badal sakta hai)")
print("None check ka sahi tareeqa: x is None ->", (None is None))

# ============ mutable default argument trap ============
def add_bad(item, bucket=[]):            # BAD: default ek hi baar banta hai
    bucket.append(item)
    return bucket

print("\nBAD  call 1:", add_bad("pen"))
print("BAD  call 2:", add_bad("book"), " <- pichhli value bhi mojood! (shared default)")
print("default kahan chhupa hai ->", add_bad.__defaults__)

def add_good(item, bucket=None):         # GOOD: None sentinel
    if bucket is None:                   # 'is None' - '== None' nahi
        bucket = []                      # har call par nayi list
    bucket.append(item)
    return bucket

print("GOOD call 1:", add_good("pen"))
print("GOOD call 2:", add_good("book"), " <- saaf")
assert add_good("x") == ["x"] and add_good("y") == ["y"]

# Wahi trap class attribute me
class TeamBad:
    members = []                         # class-level = sab instances share karenge
    def add(self, m): self.members.append(m)

class TeamGood:
    def __init__(self):
        self.members = []                # instance-level = har object ka apna
    def add(self, m): self.members.append(m)

t1, t2 = TeamBad(), TeamBad()
t1.add("Ali")
print("\nTeamBad  -> t2.members:", t2.members, " <- leak!")
g1, g2 = TeamGood(), TeamGood()
g1.add("Ali")
print("TeamGood -> g2.members:", g2.members, " <- theek")
print("[ok] Part 3 done")
'''))

# ---------------------------------------------------------------- sorting I
A(md("""
---
# Part 4 — Sorting Mastery

## 4.1 `sorted()` vs `list.sort()`, `key=`, multi-key, aur per-key reverse

| | `sorted(iterable)` | `list.sort()` |
|---|---|---|
| Return | **nayi list** | `None` (in place) |
| Kis par | koi bhi iterable (dict, set, genexp) | sirf `list` |
| Memory | extra list | in-place (thora sasta) |

**#1 beginner bug:** `nums = nums.sort()` → `nums` ban gaya `None`. `sort()` kuch return nahi karta.

### `key=` function
Har element par `key(x)` chalta hai (**sirf ek baar per element** — Schwartzian transform / decorate-sort-undecorate
internally), phir un keys par compare hota hai. `cmp` (Python 2 wala) khatam ho gaya hai.

### Multi-key sort — **tuple key** ka jaadu
`key=lambda s: (s["dept"], s["name"])` → pehle dept, tie ho to name. Tuples element-by-element compare hote hain.

### Har key ki apni direction (kuch asc, kuch desc)? Do tareeqe:
1. **Numeric ko negate karo:** `key=lambda s: (-s["score"], s["name"])` → score desc + name asc. Ek hi pass. Fastest.
   (Strings ko negate nahi kar sakte!)
2. **Two-pass stable sort:** pehle **secondary** key par sort karo, phir **primary** par.
   Python ka sort **stable** hai, is liye pehla order surakhshit rehta hai. Ye har type par chalta hai:
   ```python
   rows.sort(key=itemgetter("name"))                  # secondary (asc)
   rows.sort(key=itemgetter("score"), reverse=True)   # primary  (desc)
   ```
   **Yaad rakho: ulta order — least significant key pehle.**
3. `reverse=True` **poore** result ko ultaata hai, per-key nahi.
"""))
A(code(r'''
# ============ 4.1a sorted vs sort ============
nums = [5, 2, 9, 1, 7]

print("sorted() nayi list deta hai :", sorted(nums), "| original:", nums)
copy_nums = nums.copy()
ret = copy_nums.sort()                       # in place
print("list.sort() ka return       :", ret, " <- None! (classic bug)")
print("copy_nums ab               :", copy_nums)

# BAD (bohat common):
bad = [3, 1, 2]
bad = bad.sort()                             # ab bad = None
print("BAD  'x = x.sort()' ->", bad, " <- data gum")
good = [3, 1, 2]
good.sort()                                  # ya: good = sorted(good)
print("GOOD 'x.sort()'     ->", good)

# sorted() kisi bhi iterable par: set, dict, string, genexp
print("\nsorted(set)   :", sorted({3, 1, 2}))
print("sorted(dict)  :", sorted({"b": 1, "a": 2}), "<- keys sort hoti hain")
print("sorted(string):", "".join(sorted("python")))
print("sorted(genexp):", sorted(x % 5 for x in range(8)))

# ============ 4.1b key= ============
words = ["banana", "Fig", "apple", "cherry", "date"]
print("\ndefault (ASCII: capital pehle):", sorted(words))
print("key=str.lower (case-insensitive):", sorted(words, key=str.lower))
print("key=len                        :", sorted(words, key=len))
print("key=len, reverse=True          :", sorted(words, key=len, reverse=True))
print("key=last char                  :", sorted(words, key=lambda w: w[-1]))

# key sirf EK baar per element chalta hai (proof)
calls = []
def noisy_key(w):
    calls.append(w)
    return len(w)
sorted(words, key=noisy_key)
print("key calls =", len(calls), "for", len(words), "items -> exactly once per element")

# ============ 4.1c multi-key (tuple key) ============
employees = [
    {"name": "Zara",  "dept": "IT",    "salary": 90},
    {"name": "Ali",   "dept": "Sales", "salary": 70},
    {"name": "Bilal", "dept": "IT",    "salary": 90},
    {"name": "Hina",  "dept": "IT",    "salary": 60},
    {"name": "Umar",  "dept": "Sales", "salary": 85},
]

def show(title, rows):
    print(title)
    for r in rows:
        print(f"   {r['dept']:<6} {r['salary']:>4} {r['name']}")

# dept asc, phir name asc
by_dept_name = sorted(employees, key=lambda e: (e["dept"], e["name"]))
show("\ndept ASC, name ASC:", by_dept_name)

# dept asc, phir salary DESC (numeric -> negate)
by_dept_sal_desc = sorted(employees, key=lambda e: (e["dept"], -e["salary"]))
show("\ndept ASC, salary DESC (negate trick):", by_dept_sal_desc)
assert [e["name"] for e in by_dept_sal_desc][:3] in (["Zara", "Bilal", "Hina"], ["Bilal", "Zara", "Hina"])

# salary DESC + name ASC -> negate nahi ho sakta name par, is liye TWO-PASS stable sort
two_pass = employees.copy()
two_pass.sort(key=lambda e: e["name"])                       # step 1: secondary key ASC
two_pass.sort(key=lambda e: e["salary"], reverse=True)       # step 2: primary key DESC
show("\nsalary DESC, name ASC (two-pass stable):", two_pass)
assert [e["name"] for e in two_pass] == ["Bilal", "Zara", "Umar", "Ali", "Hina"]

# ek hi pass me bhi ho sakta hai: negate numeric + normal string
one_pass = sorted(employees, key=lambda e: (-e["salary"], e["name"]))
assert [e["name"] for e in one_pass] == [e["name"] for e in two_pass]
print("\none-pass (-salary, name) == two-pass ->", True)

# reverse=True POORA result ultaata hai (per-key nahi) - farq dekho
whole_rev = sorted(employees, key=lambda e: (e["salary"], e["name"]), reverse=True)
print("reverse=True ne name bhi ulta kar diya:", [e["name"] for e in whole_rev])
print("[ok] 4.1 done")
'''))

# ---------------------------------------------------------------- sorting II
A(md("""
## 4.2 `operator.itemgetter` / `attrgetter`, stability ka proof, dict ko value se sort karna

### `operator.itemgetter` / `attrgetter` / `methodcaller`
`lambda e: e["dept"]` ki jagah `itemgetter("dept")`. Faide:
- C me implemented → lambda se **tez** (bara data par nazar aata hai)
- multi-key: `itemgetter("dept", "salary")` seedha **tuple** deta hai
- `attrgetter("dept")` objects/dataclass ke liye, `attrgetter("addr.city")` nested attribute bhi
- `methodcaller("lower")` = `lambda s: s.lower()`

**Limitation:** `itemgetter` me negate (`-x`) nahi ho sakta → mixed direction ke liye two-pass stable sort.

### Stability
Python ka sort (Timsort) **stable** hai: barabar keys wale elements apne **original order** me rehte hain.
Isi ki wajah se multi-pass sorting kaam karti hai. Ye ek **guarantee** hai (language spec me likha hai) —
`sorted`/`list.sort` dono ke liye.

### Dict ko value se sort karna
```python
sorted(d.items(), key=itemgetter(1))                 # value asc -> list of tuples
dict(sorted(d.items(), key=lambda kv: -kv[1]))       # value desc -> naya dict (order preserved 3.7+)
Counter(d).most_common(3)                            # top-3 (heap based, sabse aasan)
heapq.nlargest(3, d.items(), key=itemgetter(1))      # top-k jab d bohat bara ho: O(n log k)
```
"""))
A(code(r'''
from operator import itemgetter, attrgetter, methodcaller
from dataclasses import dataclass
from collections import Counter
import heapq, timeit

employees = [
    {"name": "Zara",  "dept": "IT",    "salary": 90},
    {"name": "Ali",   "dept": "Sales", "salary": 70},
    {"name": "Bilal", "dept": "IT",    "salary": 90},
    {"name": "Hina",  "dept": "IT",    "salary": 60},
    {"name": "Umar",  "dept": "Sales", "salary": 85},
]

# ============ 4.2a itemgetter ============
by_lambda = sorted(employees, key=lambda e: e["salary"])
by_getter = sorted(employees, key=itemgetter("salary"))
assert by_lambda == by_getter
print("itemgetter == lambda ->", True)

# multi-key itemgetter (tuple automatically)
multi = sorted(employees, key=itemgetter("dept", "name"))
print("multi-key:", [(e["dept"], e["name"]) for e in multi])
print("itemgetter('dept','name') ek item par ->", itemgetter("dept", "name")(employees[0]))

# tuples/list of lists par index se
rows = [("Ali", 70, "Sales"), ("Zara", 90, "IT"), ("Hina", 60, "IT")]
print("rows by index 1 :", sorted(rows, key=itemgetter(1)))
print("rows by (2, 1)  :", sorted(rows, key=itemgetter(2, 1)))

# speed comparison (chhota data, farq chhota - trend dekho)
big = [{"v": i % 997} for i in range(4000)]
t_lam = timeit.timeit(lambda: sorted(big, key=lambda d: d["v"]), number=20)
t_ig  = timeit.timeit(lambda: sorted(big, key=itemgetter("v")), number=20)
print(f"lambda: {t_lam*1000:6.1f} ms | itemgetter: {t_ig*1000:6.1f} ms")

# ============ 4.2b attrgetter / methodcaller ============
@dataclass
class Emp:
    name: str
    dept: str
    salary: int

emps = [Emp(e["name"], e["dept"], e["salary"]) for e in employees]
print("\nattrgetter('dept','salary'):",
      [(e.dept, e.salary) for e in sorted(emps, key=attrgetter("dept", "salary"))])

@dataclass
class Address:
    city: str

@dataclass
class Person:
    name: str
    addr: Address

people = [Person("Ali", Address("Lahore")), Person("Sara", Address("Karachi"))]
print("nested attrgetter('addr.city'):", [p.name for p in sorted(people, key=attrgetter("addr.city"))])

names_mixed = ["banana", "Apple", "cherry"]
print("methodcaller('lower'):", sorted(names_mixed, key=methodcaller("lower")))

# ============ 4.2c stability ka proof ============
records = [("a", 2), ("b", 1), ("c", 2), ("d", 1), ("e", 2)]
by_second = sorted(records, key=itemgetter(1))
print("\ninput      :", records)
print("sorted by 1:", by_second)
# barabar keys (1,1) aur (2,2,2) apne original order me hain -> b before d, a before c before e
assert by_second == [("b", 1), ("d", 1), ("a", 2), ("c", 2), ("e", 2)]
print("stability proof pass -> equal keys ka original order mehfooz hai")

# stability ka practical faida: "pehle ye, phir wo" - multi-pass sorting
files = [("report.pdf", 300), ("a.txt", 300), ("z.txt", 100)]
files_sorted = sorted(files, key=itemgetter(0))                    # naam se
files_sorted = sorted(files_sorted, key=itemgetter(1), reverse=True)  # size desc, naam order bacha
print("multi-pass:", files_sorted)

# ============ 4.2d dict ko value se sort karna ============
scores = {"Ali": 70, "Zara": 95, "Bilal": 88, "Hina": 88, "Umar": 60}

print("\nvalue ASC  :", sorted(scores.items(), key=itemgetter(1)))
print("value DESC :", sorted(scores.items(), key=itemgetter(1), reverse=True))
# ties par naam alphabetically -> (-value, name)
print("value DESC + name ASC:", sorted(scores.items(), key=lambda kv: (-kv[1], kv[0])))
print("naya dict  :", dict(sorted(scores.items(), key=lambda kv: -kv[1])))
print("sirf keys sorted by value:", sorted(scores, key=scores.get))    # neat idiom
print("top-2 (Counter):", Counter(scores).most_common(2))
print("top-2 (heapq)  :", heapq.nlargest(2, scores.items(), key=itemgetter(1)))
print("max/min        :", max(scores, key=scores.get), "/", min(scores, key=scores.get))
print("[ok] 4.2 done")
'''))

# ---------------------------------------------------------------- sorting III
A(md("""
## 4.3 Objects ki sorting: `__lt__` vs `key=`, aur `functools.cmp_to_key`

### Do raste
1. **`key=`** (recommended, 99% cases): sorting rule call site par likha hota hai → ek hi class ko
   kai tareeqon se sort kar sakte ho.
2. **`__lt__`** (natural ordering): jab class ka ek "obvious" order ho (Version, Money, Date).
   `sort` sirf `__lt__` use karta hai. `functools.total_ordering` decorator `__eq__` + `__lt__` se
   `<=`, `>`, `>=` khud bana deta hai. Dataclass me `order=True` bhi fields ke order par comparisons de deta hai.

### `functools.cmp_to_key(cmp)`
Kabhi rule "pairwise" hota hai — ek single key nahi ban sakti (mashhoor example: numbers ko jor kar
sabse bara number banana). Tab purana style comparator likho:
`cmp(a, b)` → `negative` (a pehle), `0` (barabar), `positive` (b pehle) — aur `cmp_to_key` se wrap karo.
Ye **slow** hai (har comparison par Python function call) → sirf tab jab key possible na ho.

### Mixed types
`sorted([1, "a"])` → `TypeError` (Python 3 me `int` aur `str` compare nahi hote).
Fix: `key=str`, ya data ko pehle saaf karo (better).
"""))
A(code(r'''
from functools import total_ordering, cmp_to_key
from dataclasses import dataclass, field

# ============ 4.3a key= (flexible) ============
@dataclass
class Book:
    title: str
    year: int
    pages: int

books = [
    Book("Zen of Python", 2001, 120),
    Book("Algorithms", 1990, 500),
    Book("Clean Code", 2008, 350),
    Book("Refactoring", 1999, 500),
]
print("by year :", [b.title for b in sorted(books, key=lambda b: b.year)])
print("by pages desc, title asc:",
      [b.title for b in sorted(books, key=lambda b: (-b.pages, b.title))])

# ============ 4.3b natural ordering via __lt__ ============
@total_ordering                  # __eq__ + __lt__ se baqi operators khud ban jate hain
class Version:
    def __init__(self, text):
        self.text = text
        self.parts = tuple(int(p) for p in text.split("."))   # "1.10.2" -> (1,10,2)

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):     # sort SIRF isi ko call karta hai
        return self.parts < other.parts     # tuple comparison = element by element

    def __repr__(self):
        return f"v{self.text}"

vs_list = [Version("1.10.0"), Version("1.2.0"), Version("2.0.1"), Version("1.2.10")]
print("\nstring sort (GALAT):", sorted(v.text for v in vs_list))    # "1.10" < "1.2" (lexicographic)
print("__lt__ sort (SAHI) :", sorted(vs_list))
assert sorted(vs_list)[0].text == "1.2.0" and sorted(vs_list)[-1].text == "2.0.1"
print("total_ordering ne diya: >=", Version("2.0.0") >= Version("1.9.9"), "| max:", max(vs_list))

# dataclass(order=True) - fields ke order par automatic comparisons
@dataclass(order=True)
class Score:
    points: int
    name: str = field(compare=True)

print("dataclass(order=True):", sorted([Score(50, "b"), Score(50, "a"), Score(70, "z")]))

# ============ 4.3c cmp_to_key ============
# Problem: numbers ko arrange karo taake concatenation se sabse bara number bane
def largest_concat(nums):
    strs = [str(n) for n in nums]

    def cmp(a, b):
        # agar a+b bara hai to 'a' pehle aana chahiye -> -1
        if a + b > b + a:
            return -1
        if a + b < b + a:
            return 1
        return 0

    return "".join(sorted(strs, key=cmp_to_key(cmp)))

print("\nlargest_concat([3,30,34,5,9]) ->", largest_concat([3, 30, 34, 5, 9]))
assert largest_concat([3, 30, 34, 5, 9]) == "9534330"
assert largest_concat([10, 2]) == "210"
assert largest_concat([1, 1]) == "11"

# Wahi kaam key= se (trick: repeat kar ke fixed length) - jahan mumkin ho key hi behtar
def largest_concat_key(nums):
    strs = [str(n) for n in nums]
    width = max(len(s) for s in strs) + 1
    # "3" -> "3333", "30" -> "3030" -> lexicographic compare sahi natija deta hai
    return "".join(sorted(strs, key=lambda s: (s * width)[:width], reverse=True))

assert largest_concat_key([3, 30, 34, 5, 9]) == "9534330"
print("key= version ka same natija ->", largest_concat_key([3, 30, 34, 5, 9]))

# cmp_to_key slow hota hai - halka sa proof
import timeit
sample = [str(i % 500) for i in range(1500)]
t_cmp = timeit.timeit(lambda: sorted(sample, key=cmp_to_key(lambda a, b: (a > b) - (a < b))), number=5)
t_key = timeit.timeit(lambda: sorted(sample), number=5)
print(f"cmp_to_key: {t_cmp*1000:6.1f} ms | plain key/default: {t_key*1000:6.1f} ms")

# ============ 4.3d mixed types ============
try:
    sorted([3, "apple", 1])
except TypeError as e:
    print("\nTypeError:", e, "-> Python 3 int/str compare nahi karta")
print("workaround key=str:", sorted([3, "apple", 1], key=str), "(ASCII order - soch samajh kar use karo)")
mixed = [3, "apple", 1, "banana"]
print("behtar: type ke hisaab se alag karo ->",
      sorted(x for x in mixed if isinstance(x, int)), sorted(x for x in mixed if isinstance(x, str)))
print("[ok] 4.3 done")
'''))

# ---------------------------------------------------------------- unpacking I
A(md("""
---
# Part 5 — Unpacking Mastery

## 5.1 `*rest`, `a, *b, c`, nested unpacking, `zip(*matrix)` transpose

### Starred assignment (PEP 3132)
```python
first, *rest      = [1,2,3,4]      # 1        [2,3,4]
*init, last       = [1,2,3,4]      # [1,2,3]  4
first, *mid, last = [1,2,3,4]      # 1  [2,3] 4
```
Rules:
- **Sirf ek** star allowed per level.
- Starred variable **hamesha `list`** banta hai (string/tuple/generator par bhi) — aur khali `[]` bhi ho sakta hai.
- Baqi fixed names ke liye kaafi items honi chahiye warna `ValueError`.

### Nested unpacking
`(name, (h, m)) = ("Ali", (9, 30))` — shape exactly match karni chahiye. Loops me bohat kaam:
`for name, (a, b) in pairs:`

### `zip(*matrix)` = transpose
`*matrix` matrix ki rows ko **alag arguments** bana kar `zip` ko de deta hai → `zip(row0, row1, ...)` →
columns mil jate hain. `[list(col) for col in zip(*matrix)]` = transpose. Ye rotate-image jaisi
problems ka basic building block hai.

### Unpacking in literals (PEP 448)
`[*a, *b]`, `(*a, x)`, `{*a, *b}` — concatenation/merge ka clean tareeqa (`a + b` se zyada flexible
kyunki different types mix ho sakte hain).
"""))
A(code(r'''
data = [10, 20, 30, 40, 50]

first, *rest = data
print("first, *rest      ->", first, rest, "| rest type:", type(rest).__name__)

*init, last = data
print("*init, last       ->", init, last)

first, *middle, last = data
print("first, *mid, last ->", first, middle, last)

a, b, *empty = [1, 2]
print("extra items nahi  ->", a, b, empty, "(starred khali list ban sakta hai)")

# BAD: manual slicing (off-by-one ka khatra + intent chhup jata hai)
print("\nBAD  slicing: head =", data[0], "tail =", data[1:], "last =", data[-1])
print("GOOD unpacking: upar wali lines - naam se maloom hai kya chahiye")

# kam items -> ValueError (wrapped)
try:
    x, y, z = [1, 2]
except ValueError as e:
    print("ValueError:", e)

# star kisi bhi iterable par chalta hai (string, generator, range)
head, *tail = "python"
print("\nstring unpack :", head, tail)
h2, *t2 = (n * n for n in range(5))
print("genexp unpack  :", h2, t2)

# throwaway ke sath combine
_, *scores_only = ["Ali", 80, 90, 100]
print("name skip      :", scores_only)

# ============ nested unpacking ============
record = ("Ali", (2024, 6, 15), [88, 92])
name, (yy, mm, dd), (m1, m2) = record
print(f"\nnested: {name} joined {dd:02d}/{mm:02d}/{yy} marks {m1},{m2}")

pairs = [("Ali", (9, 30)), ("Sara", (14, 5))]
for who, (hh, mn) in pairs:                     # loop me nested unpacking
    print(f"   {who:<5} -> {hh:02d}:{mn:02d}")

# dict.items() ke sath nested
inventory = {"pen": (12, 50.0), "book": (3, 250.0)}
total_value = sum(qty * price for _, (qty, price) in inventory.items())
print("stock value    :", total_value)

# swap / rotate multiple variables
p, q, r = 1, 2, 3
p, q, r = r, p, q                               # rotate ek line me
print("rotated        :", p, q, r)

# ============ zip(*matrix) transpose ============
matrix = [[1, 2, 3],
          [4, 5, 6]]
print("\nmatrix     :", matrix)
print("zip(*m)    :", list(zip(*matrix)), "<- tuples of columns")
transposed = [list(col) for col in zip(*matrix)]
print("transpose  :", transposed)
assert transposed == [[1, 4], [2, 5], [3, 6]]
print("double transpose == original ->", [list(r) for r in zip(*transposed)] == matrix)

# transpose + reverse = rotate 90 degrees clockwise (Part 8/9 me phir aayega)
rot90 = [list(row) for row in zip(*matrix[::-1])]
print("rotate 90  :", rot90)

# zip(*pairs) = unzip
names, marks = zip(*[("Ali", 88), ("Sara", 92), ("Bilal", 75)])
print("unzip      :", names, marks)

# ============ unpacking in literals (PEP 448) ============
xs, ys = [1, 2], [3, 4]
print("\n[*xs, *ys]        ->", [*xs, *ys])
print("[0, *xs, 99]      ->", [0, *xs, 99])
print("(*xs, *ys)        ->", (*xs, *ys))
print("{*xs, *ys, 1}     ->", {*xs, *ys, 1}, "(set - dedupe)")
print("mixed types merge ->", [*"ab", *range(2), *{"k": 1}])   # str, range, dict(keys)
print("[ok] 5.1 done")
'''))

# ---------------------------------------------------------------- unpacking II
A(md("""
## 5.2 `{**a, **b}` merge, `|` dict union, `*` function calls me, `*args`/`**kwargs`, keyword-only args

### Dict merge — 3 tareeqe
```python
merged = {**a, **b}          # 3.5+  -> naya dict, b jeet ta hai (right wins)
merged = a | b               # 3.9+  -> zyada readable, same rule
a |= b                       # 3.9+  -> in place update (a.update(b) jaisa)
a.update(b)                  # purana in-place tareeqa
```
`{**a, **b, "extra": 1}` — merge ke sath sath naye keys/overrides bhi. Default config + user overrides ka
best pattern: `config = {**DEFAULTS, **user}`.
**Nested dicts ka merge shallow hota hai** — andar wali dict poori replace ho jati hai (deep merge khud likhna parta hai).

### `*` / `**` function call me (unpacking, definition nahi)
```python
def area(w, h): ...
dims = (3, 4);       area(*dims)          # positional unpack
kw = {"w": 3, "h": 4}; area(**kw)         # keyword unpack
print(*items, sep=", ")                   # sabse common real use
```

### `*args` / `**kwargs` (definition me — collecting)
- `*args` → extra positional arguments ek **tuple** me
- `**kwargs` → extra keyword arguments ek **dict** me
- Order: `def f(pos, /, normal, *args, kw_only, **kwargs)`
- `/` se pehle wale **positional-only**, `*` ke baad wale **keyword-only** (PEP 3102) — API design me
  clarity ke liye bohat useful (`sorted(iterable, *, key=None, reverse=False)` yehi karta hai).
- Forwarding idiom: `def wrapper(*args, **kwargs): return real(*args, **kwargs)` — decorators ki bunyad.
"""))
A(code(r'''
DEFAULTS = {"host": "localhost", "port": 8080, "debug": False, "retries": 3}
user_cfg = {"port": 9000, "debug": True}

# ============ 5.2a dict merge ============
# BAD: manual loop
merged_bad = dict(DEFAULTS)
for k, v in user_cfg.items():
    merged_bad[k] = v

merged_star = {**DEFAULTS, **user_cfg}          # 3.5+
merged_pipe = DEFAULTS | user_cfg               # 3.9+ (sabse readable)
assert merged_bad == merged_star == merged_pipe
print("merged      :", merged_pipe)
print("right wins  :", ({'x': 1} | {'x': 2}))
print("DEFAULTS safe:", DEFAULTS["port"], "(merge ne original ko nahi chhera)")

# merge + extra override ek sath
print("with extra  :", {**DEFAULTS, **user_cfg, "debug": False, "region": "PK"})

# in-place union
live = dict(DEFAULTS)
live |= {"port": 7000}                          # = live.update({...})
print("|= in place :", live["port"])

# GOTCHA: merge SHALLOW hai -> nested dict poori replace
base = {"db": {"host": "h1", "port": 5432}}
over = {"db": {"host": "h2"}}
print("\nshallow merge:", base | over, "<- port gum ho gaya!")

def deep_merge(a, b):
    # dono dict ho to recursive merge, warna b ki value
    out = dict(a)
    for k, v in b.items():
        out[k] = deep_merge(a[k], v) if isinstance(a.get(k), dict) and isinstance(v, dict) else v
    return out

print("deep merge   :", deep_merge(base, over), "<- port bacha")

# ============ 5.2b * / ** function CALL me ============
def area(width, height, unit="cm"):
    return f"{width * height} sq{unit}"

dims_t = (3, 4)
dims_d = {"width": 3, "height": 4, "unit": "m"}
print("\nnormal      :", area(3, 4))
print("*tuple      :", area(*dims_t))
print("**dict      :", area(**dims_d))
print("mix         :", area(*dims_t, **{"unit": "in"}))

items = ["a", "b", "c"]
print("print(*items, sep='|') ->", end=" ")
print(*items, sep="|")

# ** se wrong key -> TypeError (wrapped)
try:
    area(**{"width": 1, "heigth": 2})            # typo: heigth
except TypeError as e:
    print("TypeError:", e)

# ============ 5.2c *args / **kwargs ============
def summarize(label, *args, sep=" | ", **kwargs):
    # label      -> normal positional
    # *args      -> baqi positional tuple me
    # sep        -> KEYWORD-ONLY (kyunki *args ke baad aaya hai)
    # **kwargs   -> baqi keywords dict me
    body = sep.join(str(a) for a in args)
    extra = sep.join(f"{k}={v}" for k, v in kwargs.items())
    return f"[{label}] {body}" + (f" ({extra})" if extra else "")

print("\n", summarize("nums", 1, 2, 3))
print("", summarize("nums", 1, 2, sep=" + ", author="Ali", version=2))
print("", summarize("empty"))

# keyword-only args (explicit * marker) -> call site self-documenting ban jati hai
def make_user(name, *, admin=False, active=True):
    return {"name": name, "admin": admin, "active": active}

print("\nkw-only ok  :", make_user("Ali", admin=True))
try:
    make_user("Ali", True)                       # positionally dena mana hai
except TypeError as e:
    print("TypeError:", e, "-> yehi kw-only ka faida (galat call rok di)")

# positional-only ( / ) - 3.8+
def dist(x, y, /, scale=1):
    return ((x * x + y * y) ** 0.5) * scale
print("positional-only:", dist(3, 4, scale=2))
try:
    dist(x=3, y=4)
except TypeError as e:
    print("TypeError:", e)

# forwarding idiom (decorators ki bunyad)
import functools, time

def timed(func):
    @functools.wraps(func)                       # naam/docstring preserve
    def wrapper(*args, **kwargs):                # kuch bhi lo...
        t0 = time.perf_counter()
        result = func(*args, **kwargs)           # ...aur waisa hi aage bhej do
        wrapper.last_ms = (time.perf_counter() - t0) * 1000
        return result
    return wrapper

@timed
def slow_sum(n, start=0):
    return sum(range(start, n))

print("\nforwarding  :", slow_sum(10_000, start=5), f"in {slow_sum.last_ms:.2f} ms")
print("wraps ne naam bachaya ->", slow_sum.__name__)
print("[ok] 5.2 done")
'''))

# ---------------------------------------------------------------- gotchas
A(md("""
---
# Part 6 — Common Mistakes / Gotchas (Anti-pattern Museum)

Ye section "yahan log phaste hain" ka collection hai. Har ek interview me poocha ja sakta hai.

| # | Gotcha | Kya hota hai | Fix |
|---|---|---|---|
| 1 | Mutable default arg `def f(x=[])` | default ek hi baar banta hai, calls ke darmiyan share | `x=None` + `if x is None` |
| 2 | Late binding closures | `[lambda: i for i in range(3)]` → sab `2` dete hain | default arg `lambda i=i: i` ya `functools.partial` |
| 3 | List ko iterate karte waqt modify | items skip ho jate hain / `RuntimeError` | copy par loop (`for x in lst[:]`) ya nayi list banao |
| 4 | `dict` ko loop me modify | `RuntimeError: dictionary changed size` | `list(d.items())` par loop |
| 5 | `x = x.sort()` | `None` mil jata hai | `x.sort()` ya `x = sorted(x)` |
| 6 | `is` vs `==` | `1000 is 1000` implementation detail hai | values ke liye `==`; `is` sirf `None`/sentinel |
| 7 | `+=` on tuple ka list element | `TypeError` **magar mutation ho jati hai** | list ko bahar nikal kar `.extend()` |
| 8 | `[[0]*3]*2` | saari rows ek hi object | `[[0]*3 for _ in range(2)]` |
| 9 | Bare `except:` | `KeyboardInterrupt`/`SystemExit` bhi kha jata hai | `except Exception as e:` |
| 10 | Float equality `0.1+0.2 == 0.3` | binary float ki wajah se `False` | `math.isclose()` |
| 11 | `str` ko iterable samajh kar `extend` | `"ab"` → `['a','b']` | `.append("ab")` |
| 12 | Comprehension side-effects ke liye | bekaar list banti hai | normal `for` loop |
| 13 | `range` me `len()` off-by-one | `range(1, len(x))` pehla item chhor deta hai | `enumerate` |
| 14 | Shadowing built-ins (`list = [...]`, `id`, `sum`) | baad me `list(...)` crash | dusra naam (`items`, `row_id`) |
| 15 | `except Exception: pass` | bug chup chaap gum | log karo ya raise karo |
"""))
A(code(r'''
import math

# ---- 2) Late binding closures ----
funcs_bad = [lambda: i for i in range(3)]         # 'i' loop ke baad ki value padhta hai
print("BAD  late binding :", [f() for f in funcs_bad], " <- sab 2!")
funcs_good = [lambda i=i: i for i in range(3)]    # default arg = value ko FORAN capture
print("GOOD default arg  :", [f() for f in funcs_good])
from functools import partial
funcs_partial = [partial(lambda x: x, i) for i in range(3)]
print("GOOD partial      :", [f() for f in funcs_partial])

# ---- 3) list ko iterate karte waqt modify ----
nums = [1, 2, 3, 4, 5, 6]
bad = nums.copy()
for x in bad:
    if x % 2 == 0:
        bad.remove(x)                             # index shift -> items skip
print("\nBAD  remove-in-loop:", bad, " <- 4 bacha reh gaya (skip ho gaya)")
good = [x for x in nums if x % 2]                 # GOOD: nayi list banao
print("GOOD comprehension :", good)
good2 = nums.copy()
for x in good2[:]:                                # GOOD: copy par loop (slice)
    if x % 2 == 0:
        good2.remove(x)
print("GOOD copy par loop :", good2)

# ---- 4) dict ko loop me modify ----
d = {"a": 1, "b": 2, "c": 3}
try:
    for k in d:
        if d[k] == 2:
            del d[k]
except RuntimeError as e:
    print("\nRuntimeError:", e)
d = {"a": 1, "b": 2, "c": 3}
for k in list(d):                                 # FIX: keys ka snapshot
    if d[k] == 2:
        del d[k]
print("FIX list(d) par loop ->", d)
print("ya comprehension     ->", {k: v for k, v in {"a": 1, "b": 2}.items() if v != 2})

# ---- 6) is vs == ----
print("\n0.1+0.2 == 0.3 ->", 0.1 + 0.2 == 0.3, "| repr:", repr(0.1 + 0.2))
print("math.isclose   ->", math.isclose(0.1 + 0.2, 0.3))
print("Decimal se exact:", __import__("decimal").Decimal("0.1") + __import__("decimal").Decimal("0.2"))

# ---- 7) += on a list inside a tuple (favourite interview gotcha) ----
t = (["a"], "b")
try:
    t[0] += ["c"]                                 # __iadd__ list ko mutate karta hai, phir tuple assign FAIL
except TypeError as e:
    print("\nTypeError:", e)
print("magar mutation ho gayi ->", t, " <- ['a','c'] ! (aadha kaam ho gaya)")
t2 = (["a"], "b")
t2[0].extend(["c"])                               # FIX: assignment hi na karo
print("FIX .extend()         ->", t2)

# ---- 9) bare except vs except Exception ----
def risky(n):
    return 10 / n
try:
    risky(0)
except Exception as e:                            # GOOD: Exception (BaseException nahi)
    print("\ncaught:", type(e).__name__, "-", e)
print("bare 'except:' KeyboardInterrupt/SystemExit bhi kha jata hai -> kabhi na likho")

# ---- 11) extend vs append with strings ----
box = ["x"]
box.extend("ab")                                  # string iterable hai -> chars
print("\nextend('ab') ->", box, " <- shayad ye nahi chahiye tha")
box2 = ["x"]
box2.append("ab")
print("append('ab') ->", box2)

# ---- 13) off-by-one ----
letters = ["a", "b", "c"]
print("\nBAD  range(1, len()) ->", [letters[i] for i in range(1, len(letters))], "<- pehla gum")
print("GOOD enumerate       ->", [(i, c) for i, c in enumerate(letters)])

# ---- 14) built-in shadowing ----
list_backup = list                                # demo ke liye asli 'list' bacha lo
list = [1, 2, 3]                                  # BAD: built-in ko chhupa diya
try:
    list("abc")
except TypeError as e:
    print("\nTypeError:", e, "-> 'list' naam shadow ho gaya")
del list                                          # FIX: naam hata do (ya kabhi use na karo)
print("recovered ->", list("abc"))
assert list is list_backup

# ---- 15) silent except ----
def parse_bad(s):
    try:
        return int(s)
    except Exception:
        pass                                      # bug gum ho gaya, None wapas
def parse_good(s, default=None):
    try:
        return int(s)
    except ValueError:                            # sirf expected error, specific
        return default
print("\nparse_bad('x') ->", parse_bad("x"), "| parse_good('x', -1) ->", parse_good("x", -1))
print("[ok] Part 6 done")
'''))

# ---------------------------------------------------------------- real world 1
A(md("""
---
# Part 7 — Real-World Problems

## 7.1 Student Marks Report (sorting + comprehension + f-string report)

**Scenario:** ek class ke students ke 3 subjects ke marks hain. Banana hai:
1. Har student ka total, average, percentage aur grade
2. Class topper aur subject-wise topper
3. Ranked report table: **grade ke hisaab se (A pehle), phir total DESC, phir naam ASC**
4. Pass/fail statistics aur subject-wise class average

**Idioms jo use honge:** dict comprehension, `sum()`, multi-key sort with negate trick,
`operator.itemgetter`, `zip(*...)` transpose (subject-wise columns), f-string format specs,
`max(..., key=...)`, `enumerate(start=1)`.
"""))
A(code(r'''
from operator import itemgetter

SUBJECTS = ("Math", "Physics", "English")
raw_marks = {
    "Ali Raza":      [78, 82, 91],
    "Sara Khan":     [95, 88, 99],
    "Bilal Ahmed":   [45, 38, 55],
    "Hina Tariq":    [88, 92, 79],
    "Umar Farooq":   [60, 71, 65],
    "Ayesha Noor":   [95, 88, 99],      # Sara ke barabar -> tie-break test
}

def grade_for(pct):
    # thresholds table -> nested ternary se behtar (readable + extend karna aasan)
    for cutoff, g in ((90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D")):
        if pct >= cutoff:
            return g
    return "F"

# --- 1) har student ka summary (dict comprehension + helper) ---
def summarize(name, marks):
    total = sum(marks)                                    # sum built-in
    pct = total / (len(marks) * 100) * 100                # har subject 100 marks ka
    return {
        "name": name,
        "marks": dict(zip(SUBJECTS, marks, strict=True)), # strict=True -> mismatch pakra jaye
        "total": total,
        "avg": total / len(marks),
        "pct": pct,
        "grade": grade_for(pct),
        "passed": all(m >= 40 for m in marks),            # all() -> har subject me 40+
    }

report = {name: summarize(name, marks) for name, marks in raw_marks.items()}

# --- 2) ranking: grade order, phir total DESC, phir naam ASC ---
GRADE_ORDER = {g: i for i, g in enumerate(("A+", "A", "B", "C", "D", "F"))}
ranked = sorted(report.values(), key=lambda r: (GRADE_ORDER[r["grade"]], -r["total"], r["name"]))

print(f"{'#':<3}{'Name':<14}{'Math':>6}{'Phy':>6}{'Eng':>6}{'Total':>7}{'Pct':>8}{'Grade':>7}{'Result':>8}")
print("-" * 65)
for rank, r in enumerate(ranked, start=1):                # enumerate(start=1) -> 1-based rank
    m = r["marks"]
    print(f"{rank:<3}{r['name']:<14}{m['Math']:>6}{m['Physics']:>6}{m['English']:>6}"
          f"{r['total']:>7}{r['pct']:>7.1f}%{r['grade']:>7}"
          f"{('PASS' if r['passed'] else 'FAIL'):>8}")

# --- 3) toppers ---
topper = max(report.values(), key=itemgetter("total"))     # max + key
print(f"\nClass topper : {topper['name']} ({topper['total']}/300, {topper['pct']:.1f}%)")

# subject-wise topper: zip(*...) se columns nikalo
names = list(raw_marks)
columns = list(zip(*raw_marks.values()))                   # transpose: har subject ki poori column
for subject, col in zip(SUBJECTS, columns, strict=True):
    best_idx = max(range(len(col)), key=lambda i: col[i])  # index-based max
    print(f"{subject:<8} topper: {names[best_idx]:<12} ({col[best_idx]})  class avg = {sum(col)/len(col):.1f}")

# --- 4) statistics ---
passed = [r["name"] for r in report.values() if r["passed"]]
failed = [r["name"] for r in report.values() if not r["passed"]]
grade_count = {}
for r in report.values():
    grade_count[r["grade"]] = grade_count.get(r["grade"], 0) + 1   # dict.get idiom

print(f"\nPassed {len(passed)}/{len(report)} ({len(passed)/len(report):.0%}) | Failed: {failed}")
print("Grade distribution:", dict(sorted(grade_count.items(), key=lambda kv: GRADE_ORDER[kv[0]])))
print("Above 80%:", sorted(r["name"] for r in report.values() if r["pct"] >= 80))

# --- tests ---
assert report["Sara Khan"]["total"] == 282 and report["Sara Khan"]["grade"] == "A+"
assert report["Bilal Ahmed"]["passed"] is False
assert ranked[0]["name"] in ("Ayesha Noor", "Sara Khan")
assert [r["name"] for r in ranked][:2] == ["Ayesha Noor", "Sara Khan"]   # tie -> naam ASC
assert ranked[-1]["name"] == "Bilal Ahmed"
print("\n[ok] 7.1 all assertions passed")
'''))

# ---------------------------------------------------------------- real world 2
A(md("""
## 7.2 Text Cleanup + Word Frequency Pipeline

**Scenario:** user reviews ka raw text mila hai. Ek "pipeline" banani hai jo:
1. lowercase kare
2. punctuation hataye (`str.translate` — sabse tez tareeqa)
3. digits/URLs jaisa shor saaf kare
4. stopwords (the, is, a...) nikaal de — `set` membership O(1)
5. word frequency nikaale aur **top-k** words de
6. bonus: har review ki length stats aur unique-word ratio

**Idioms:** `str.maketrans`, generator pipeline, `Counter.most_common`, set membership,
comprehension chaining, `sum(1 for ...)`, f-string alignment.

**Design note:** har step ek chhota **function** hai (test karna aasan), aur pipeline `functools.reduce`
ki tarah steps ko chain karti hai — yehi asli code me maintainable hota hai.
"""))
A(code(r'''
import string
from collections import Counter

REVIEWS = [
    "The delivery was FAST and the packaging was great!! Highly recommend :)",
    "Terrible service... the product arrived broken. The support team ignored me!!!",
    "Good value for money; the quality is average but the delivery was fast.",
    "Fast delivery, great quality, great price -- 10/10 would buy again!",
    "The app kept crashing (visit http://example.com/help) -- support was useless.",
]

STOPWORDS = {
    "the", "was", "and", "is", "a", "an", "for", "but", "me", "i", "it",
    "of", "to", "in", "would", "be", "this", "that", "my",
}
PUNCT_TABLE = str.maketrans("", "", string.punctuation)     # ek hi table, dobara dobara use hoga

# ---------- pipeline ke chhote, test-able steps ----------
def strip_urls(text):
    # URL jaisa token nikaal do (regex ke baghair, simple aur readable)
    return " ".join(w for w in text.split() if not w.startswith(("http://", "https://", "www.")))

def normalize(text):
    return strip_urls(text).lower().translate(PUNCT_TABLE)   # lower + punctuation delete

def tokenize(text):
    # sirf alphabetic tokens, stopwords aur 2 se chhote words hata do
    return [w for w in normalize(text).split() if w.isalpha() and len(w) > 2 and w not in STOPWORDS]

def word_counts(docs):
    # generator chain -> saari tokens memory me ek sath nahi aati
    return Counter(word for doc in docs for word in tokenize(doc))

# ---------- chalao ----------
print("RAW  :", REVIEWS[4])
print("CLEAN:", normalize(REVIEWS[4]))
print("TOKEN:", tokenize(REVIEWS[4]))

counts = word_counts(REVIEWS)
TOP_K = 6
print(f"\nTop {TOP_K} words:")
for rank, (word, n) in enumerate(counts.most_common(TOP_K), start=1):
    bar = "#" * n                                            # chhota text bar-chart (matplotlib nahi)
    print(f"  {rank}. {word:<12} {n:>2}  {bar}")

# ---------- per-review stats ----------
print(f"\n{'#':<3}{'words':>6}{'unique':>8}{'ratio':>8}  first-3-tokens")
for i, r in enumerate(REVIEWS, start=1):
    toks = tokenize(r)
    uniq = set(toks)
    ratio = len(uniq) / len(toks) if toks else 0
    print(f"{i:<3}{len(toks):>6}{len(uniq):>8}{ratio:>8.2f}  {toks[:3]}")

# ---------- kuch aur useful aggregates ----------
all_tokens = [w for r in REVIEWS for w in tokenize(r)]
print("\ntotal tokens        :", len(all_tokens))
print("unique tokens       :", len(set(all_tokens)))
print("hapax (sirf 1 baar) :", sorted(w for w, n in counts.items() if n == 1)[:6], "...")
print("words with 'fast'   :", counts["fast"], "| 'great':", counts["great"])
print("longest word        :", max(all_tokens, key=len))
print("avg word length     :", f"{sum(len(w) for w in all_tokens) / len(all_tokens):.2f}")
print("reviews mentioning 'delivery':", sum(1 for r in REVIEWS if "delivery" in tokenize(r)))

# sentiment ka bohat simple version (set intersection)
POSITIVE = {"fast", "great", "good", "recommend", "quality", "value"}
NEGATIVE = {"terrible", "broken", "ignored", "useless", "crashing"}
for i, r in enumerate(REVIEWS, start=1):
    toks = set(tokenize(r))
    score = len(toks & POSITIVE) - len(toks & NEGATIVE)       # set intersection
    verdict = "positive" if score > 0 else ("negative" if score < 0 else "neutral")
    print(f"  review {i}: score {score:+d} -> {verdict}")

# ---------- tests ----------
assert normalize("Hello, World!!") == "hello world"
assert "http" not in " ".join(tokenize(REVIEWS[4]))
assert "the" not in all_tokens                                # stopword hat gaya
assert counts["fast"] == 3 and counts["delivery"] == 3
assert counts.most_common(1)[0][1] == max(counts.values())
print("\n[ok] 7.2 all assertions passed")
'''))

# ---------------------------------------------------------------- real world 3
A(md("""
## 7.3 Gaming Leaderboard (ranking with ties, dense vs competition rank)

**Scenario:** ek multiplayer game ke matches ka data hai. Banana hai:
1. Har player ka total score, matches, best score, average
2. Leaderboard: **score DESC, phir naam ASC** (two-pass stable sort **aur** negate trick, dono dikhayenge)
3. **Ranking with ties** — do standard tareeqe:
   - **Competition ranking (1, 2, 2, 4)** — tie ke baad number "jump" karta hai (Olympics style)
   - **Dense ranking (1, 2, 2, 3)** — koi jump nahi
4. Top-3 medals, aur "kaun kis se aage nikla" wala movement (previous snapshot se compare)

**Idioms:** `defaultdict`, `Counter`, walrus, `itertools.groupby` (sorted data par), multi-key sorting,
dict comprehension, f-string alignment, `zip` for pairwise comparison.
"""))
A(code(r'''
from collections import defaultdict
from operator import itemgetter
from itertools import groupby

MATCHES = [
    ("ninja_ali",  120), ("proSara", 200), ("bilal_x",  90), ("hina99", 150),
    ("ninja_ali",  180), ("proSara", 100), ("bilal_x", 210), ("hina99",  50),
    ("ninja_ali",   50), ("umar_g",  300), ("proSara",  30), ("bilal_x",  60),
    ("ayesha_pro", 360),
]

# --- 1) aggregate (defaultdict = grouping ka best tool) ---
scores = defaultdict(list)
for player, points in MATCHES:                       # tuple unpacking loop me
    scores[player].append(points)

stats = {
    p: {
        "player": p,
        "total": sum(pts),
        "matches": len(pts),
        "best": max(pts),
        "avg": sum(pts) / len(pts),
    }
    for p, pts in scores.items()                     # dict comprehension
}

# --- 2) leaderboard: total DESC, naam ASC (do tareeqe, ek hi natija) ---
lb_one_pass = sorted(stats.values(), key=lambda s: (-s["total"], s["player"]))
lb_two_pass = sorted(stats.values(), key=itemgetter("player"))            # secondary ASC
lb_two_pass = sorted(lb_two_pass, key=itemgetter("total"), reverse=True)  # primary DESC (stable)
assert [s["player"] for s in lb_one_pass] == [s["player"] for s in lb_two_pass]

# --- 3) ranking with ties ---
def competition_ranks(rows, key=itemgetter("total")):
    # 1,2,2,4 style: tie ke baad rank jump karta hai
    ranks, prev_val, prev_rank = [], None, 0
    for i, row in enumerate(rows, start=1):
        val = key(row)
        rank = prev_rank if val == prev_val else i    # barabar score -> pichhla rank
        ranks.append(rank)
        prev_val, prev_rank = val, rank
    return ranks

def dense_ranks(rows, key=itemgetter("total")):
    # 1,2,2,3 style: groupby (data pehle sorted hona chahiye!)
    out = []
    for rank, (_val, group) in enumerate(groupby(rows, key=key), start=1):
        # group ek iterator hai (sirf ek baar chalta hai) -> sum(1 for _ in group) = uska size
        out.extend([rank] * sum(1 for _ in group))
    return out

# artificial tie banate hain taake ranking clearly nazar aaye
stats["tie_bot"] = {"player": "tie_bot", "total": stats["hina99"]["total"], "matches": 1,
                    "best": 0, "avg": 0.0}
board = sorted(stats.values(), key=lambda s: (-s["total"], s["player"]))
comp = competition_ranks(board)
dens = dense_ranks(board)

MEDALS = {1: "gold", 2: "silver", 3: "bronze"}
print(f"{'comp':>5}{'dense':>6}  {'player':<12}{'total':>7}{'matches':>9}{'best':>6}{'avg':>8}  medal")
print("-" * 66)
for c, dn, s in zip(comp, dens, board, strict=True):
    print(f"{c:>5}{dn:>6}  {s['player']:<12}{s['total']:>7}{s['matches']:>9}"
          f"{s['best']:>6}{s['avg']:>8.1f}  {MEDALS.get(c, '')}")

print("\ncompetition ranks:", comp, "(tie ke baad jump)")
print("dense ranks      :", dens, "(koi jump nahi)")

# --- 4) movement vs previous snapshot ---
previous = ["umar_g", "proSara", "ayesha_pro", "ninja_ali", "hina99", "tie_bot", "bilal_x"]
current = [s["player"] for s in board]
pos_prev = {p: i for i, p in enumerate(previous)}          # naam -> purani position
print("\nmovement:")
for i, p in enumerate(current):
    if (delta := pos_prev.get(p, i) - i) > 0:              # walrus + get(default)
        arrow = f"UP {delta}"
    elif delta < 0:
        arrow = f"DOWN {-delta}"
    else:
        arrow = "same"
    print(f"  {i+1:>2}. {p:<12} {arrow}")

# --- 5) chhote insights ---
print("\nsabse zyada matches :", max(stats.values(), key=itemgetter("matches"))["player"])
print("best single match   :", max(stats.values(), key=itemgetter("best"))["player"])
print("consistent (avg)    :", max((s for s in stats.values() if s["matches"] > 1), key=itemgetter("avg"))["player"])
print("total points scored :", sum(s["total"] for s in stats.values()))

# --- tests ---
assert stats["ninja_ali"]["total"] == 350 and stats["ninja_ali"]["matches"] == 3
assert stats["bilal_x"]["total"] == 360 and stats["ayesha_pro"]["total"] == 360
# top par 360 ka tie hai -> naam ASC ne faisla kiya
assert [s["player"] for s in board][:2] == ["ayesha_pro", "bilal_x"]
assert comp[0] == comp[1] == 1 and comp[2] == 3, "competition rank tie ke baad jump karta hai"
assert dens[0] == dens[1] == 1 and dens[2] == 2, "dense rank jump nahi karta"
# tie wale do players ka comp rank barabar, dense rank bhi barabar
tie_positions = [i for i, s in enumerate(board) if s["total"] == 200]
assert len({comp[i] for i in tie_positions}) == 1, "tie par same competition rank"
assert dens[-1] <= comp[-1], "dense rank kabhi competition rank se bara nahi hota"
print("\n[ok] 7.3 all assertions passed")
'''))

# ================================================================ 20 problems
A(md("""
---
# Part 8 — 20 Classic Interview Coding Problems

Ye wo problems hain jo Pakistani/international companies ke **screening rounds** aur university
vivas me bar bar aati hain. Har problem ke sath:
- **Problem** (Roman Urdu me)
- **Approach** + kyun ye approach
- **Time & Space complexity**
- Code + heavy comments + `assert` tests (jo chal kar pass hote hain)

> **Naming note:** aage LeetCode section me kuch problems dobara aayengi (optimal/LeetCode-style signature ke sath).
> Naam jaan boojh kar **alag** rakhe gaye hain (e.g. `rotate_90` vs `rotate_image_inplace`) taake koi cell
> doosre ko override na kare.

## Problem 1 — Word frequency (top-k words)

**Problem:** ek text/sentence me har word kitni baar aaya, aur sabse zyada aane wale **k** words batao.

**Approach:**
1. Normalize: lowercase + punctuation remove (`str.translate` — O(n))
2. `collections.Counter` se count (hash map, har word par O(1))
3. Top-k: `Counter.most_common(k)` — andar `heapq.nlargest` use hota hai → O(n log k),
   poora sort (`O(n log n)`) karne se behtar jab k chhota ho
4. Ties par deterministic output chahiye to `key=(-count, word)` se sort karo (interviewer ye zaroor poochta hai)

**Complexity:** Time O(n log k) (ya ties-sorted version me O(m log m), m = unique words), Space O(m).
"""))
A(code(r'''
from collections import Counter
import string, heapq

def top_k_words(text, k=3, deterministic=True):
    # step 1: normalize -> lowercase + punctuation delete (ek hi pass, C speed)
    table = str.maketrans("", "", string.punctuation)
    words = text.lower().translate(table).split()          # split() whitespace par tor deta hai

    # step 2: count (Counter = dict subclass, missing key par 0)
    counts = Counter(words)

    # step 3: top-k
    if deterministic:
        # ties par alphabetical -> output har machine par same (interview me ye maango)
        ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return ordered[:k]
    return counts.most_common(k)                           # heap based, ties ka order undefined

def word_freq_manual(text):
    # bina Counter (interviewer kabhi 'built-in mat use karo' kehta hai)
    freq = {}
    for w in text.lower().split():
        freq[w] = freq.get(w, 0) + 1                       # dict.get default idiom
    return freq

sample = "the cat sat on the mat the cat was fat and the mat was flat"

print("top 3          :", top_k_words(sample, 3))
print("top 5          :", top_k_words(sample, 5))
print("most_common(3) :", top_k_words(sample, 3, deterministic=False))
print("manual freq    :", word_freq_manual("a b a c b a"))
print("heapq nlargest :", heapq.nlargest(2, Counter(sample.split()).items(), key=lambda kv: kv[1]))

# ---- tests ----
assert top_k_words(sample, 1) == [("the", 4)]
assert top_k_words(sample, 3) == [("the", 4), ("cat", 2), ("mat", 2)]   # ties -> alphabetical
assert top_k_words("Hello, hello! HELLO?", 1) == [("hello", 3)]         # case + punctuation
assert top_k_words("", 3) == []                                        # empty edge case
assert top_k_words("one", 5) == [("one", 1)]                           # k > unique words
assert word_freq_manual("a b a") == {"a": 2, "b": 1}
print("[pass] Problem 1")
'''))

A(md("""
## Problem 2 — Flatten a nested list (recursive + generator versions)

**Problem:** `[1, [2, [3, [4]], 5]]` → `[1, 2, 3, 4, 5]`. Depth kitni bhi ho sakti hai.

**Approach A — recursion:** har item dekho; agar wo list/tuple hai to us par khud ko dobara call karo (`extend`),
warna `append`. Base case: non-iterable item.

**Approach B — generator (`yield from`):** memory efficient — items ek ek nikalte hain, poori list nahi banti.
Ye bara data (streaming) ke liye best hai.

**Approach C — iterative with stack:** recursion limit (default ~1000) se bachne ke liye. Bohat deep nesting
par `RecursionError` aata hai — ye interviewer ka follow-up question hota hai.

**Zaroori detail:** `str`/`bytes` bhi iterable hain — unko flatten karne se **infinite recursion** ho sakti hai
(`"a"[0]` phir `"a"` hi hai). Is liye strings ko **atomic** treat karo.

**Complexity:** Time O(n) (n = total items including nested containers), Space O(d) recursion depth
(generator version me output memory O(1)).
"""))
A(code(r'''
from collections.abc import Iterable

# ---------- A) recursive ----------
def flatten_recursive(nested):
    out = []
    for item in nested:
        # str/bytes ko atomic maano warna infinite recursion (kyunki "a"[0] == "a")
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            out.extend(flatten_recursive(item))    # recursion: sub-list ko flatten kar ke jor do
        else:
            out.append(item)
    return out

# ---------- B) generator (lazy, memory friendly) ----------
def flatten_gen(nested):
    for item in nested:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten_gen(item)           # yield from = sub-generator ko delegate
        else:
            yield item

# ---------- C) iterative (stack) - deep nesting par RecursionError se bachta hai ----------
def flatten_iterative(nested):
    out, stack = [], list(nested)[::-1]            # ulta rakha taake pop() front se nikale
    while stack:
        item = stack.pop()
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            stack.extend(list(item)[::-1])         # sub-items wapas stack par
        else:
            out.append(item)
    return out

# ---------- sirf 1 level (jab depth fix ho -> comprehension kaafi hai) ----------
def flatten_one_level(nested):
    return [x for sub in nested for x in sub]      # classic nested comprehension idiom

deep = [1, [2, [3, [4, [5]]], 6], 7, [[8], [[9]]]]
print("recursive :", flatten_recursive(deep))
print("generator :", list(flatten_gen(deep)))
print("iterative :", flatten_iterative(deep))
print("one level :", flatten_one_level([[1, 2], [3], [], [4, 5]]))
print("lazy proof:", next(flatten_gen(deep)), "<- sirf pehla item nikala, poori list nahi bani")
print("strings   :", flatten_recursive(["ab", ["cd", ["e"]]]), "<- strings atomic rahe")
print("mixed     :", flatten_recursive([1, (2, 3), {4, 5}, [6]]))

# bohat deep list par recursion vs iteration
very_deep = current = []
for i in range(200):
    nxt = []
    current.append(i)
    current.append(nxt)
    current = nxt
print("deep-200 recursive length:", len(flatten_recursive(very_deep)))
print("deep-200 iterative length:", len(flatten_iterative(very_deep)))

# ---- tests ----
assert flatten_recursive([1, [2, [3, [4]], 5]]) == [1, 2, 3, 4, 5]
assert list(flatten_gen([1, [2, [3, [4]], 5]])) == [1, 2, 3, 4, 5]
assert flatten_iterative([1, [2, [3, [4]], 5]]) == [1, 2, 3, 4, 5]
assert flatten_recursive([]) == [] and list(flatten_gen([])) == []
assert flatten_recursive([[], [[]], [[[]]]]) == []               # sirf khali containers
assert flatten_recursive(["ab", ["cd"]]) == ["ab", "cd"]
assert flatten_one_level([[1], [2, 3]]) == [1, 2, 3]
assert flatten_recursive(deep) == list(flatten_gen(deep)) == flatten_iterative(deep)
print("[pass] Problem 2")
'''))

A(md("""
## Problem 3 — Merge two dicts, summing values of common keys

**Problem:** `{"a":1,"b":2}` + `{"b":3,"c":4}` → `{"a":1,"b":5,"c":4}`.

**Approach A — `Counter` + `+`:** sabse chhota code. **Gotcha:** `Counter` addition **zero/negative values
ko phenk deta hai** — agar negative/0 chahiye to ye galat hai.

**Approach B — manual (`dict.get`)**: pehla dict copy karo, doosre ko loop karke `get(k, 0) + v`.
Har type ke numbers ke sath sahi kaam karta hai. Ye production-safe version hai.

**Approach C — comprehension over key union:** `{k: a.get(k,0) + b.get(k,0) for k in a | b.keys()}`
(`a.keys() | b.keys()` = set union — `dict.keys()` set-like hai).

**Complexity:** Time O(n + m), Space O(n + m).
"""))
A(code(r'''
from collections import Counter

def merge_sum_counter(a, b):
    # sabse chhota, magar 0/negative results gayab kar deta hai
    return dict(Counter(a) + Counter(b))

def merge_sum_dicts(a, b):
    # production-safe: har key rehti hai, negative/0 bhi
    out = dict(a)                                  # shallow copy (a ko chhera nahi)
    for k, v in b.items():
        out[k] = out.get(k, 0) + v                 # dict.get default idiom
    return out

def merge_sum_comprehension(a, b):
    # keys ka union: dict.keys() set-like hai -> | operator chalta hai
    return {k: a.get(k, 0) + b.get(k, 0) for k in a.keys() | b.keys()}

def merge_sum_many(*dicts):
    # N dicts ka merge (*args) - reduce style
    out = {}
    for d in dicts:
        for k, v in d.items():
            out[k] = out.get(k, 0) + v
    return out

d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
print("Counter version      :", merge_sum_counter(d1, d2))
print("manual version       :", merge_sum_dicts(d1, d2))
print("comprehension version:", dict(sorted(merge_sum_comprehension(d1, d2).items())))
print("many dicts           :", merge_sum_many(d1, d2, {"a": 10, "d": 7}))
print("original safe        :", d1, d2)

# Counter ka gotcha live
neg1, neg2 = {"x": 5, "y": 1}, {"x": -5, "y": -3}
print("\nCounter (BAD here)   :", merge_sum_counter(neg1, neg2), "<- x=0, y=-2 gayab!")
print("manual  (GOOD)       :", merge_sum_dicts(neg1, neg2))

# ---- tests ----
assert merge_sum_dicts({"a": 1, "b": 2}, {"b": 3, "c": 4}) == {"a": 1, "b": 5, "c": 4}
assert merge_sum_comprehension({"a": 1, "b": 2}, {"b": 3, "c": 4}) == {"a": 1, "b": 5, "c": 4}
assert merge_sum_counter({"a": 1}, {"a": 2}) == {"a": 3}
assert merge_sum_dicts({}, {"a": 1}) == {"a": 1} and merge_sum_dicts({"a": 1}, {}) == {"a": 1}
assert merge_sum_dicts({}, {}) == {}
assert merge_sum_dicts({"x": 5}, {"x": -5}) == {"x": 0}          # manual me 0 rehta hai
assert merge_sum_many({"a": 1}, {"a": 2}, {"a": 3}) == {"a": 6}
assert merge_sum_dicts({"a": 1.5}, {"a": 2.5}) == {"a": 4.0}     # floats bhi
print("[pass] Problem 3")
'''))

A(md("""
## Problem 4 — Group anagrams

**Problem:** `["eat","tea","tan","ate","nat","bat"]` → `[["eat","tea","ate"],["tan","nat"],["bat"]]`

**Approach:** Anagrams ka ek **canonical signature** hota hai. Us signature ko dict key bana kar group karo.
- Signature 1: `"".join(sorted(word))` → O(k log k) per word
- Signature 2: 26-length count **tuple** → O(k) per word (Unicode ke liye `tuple(sorted(Counter(w).items()))`)

`defaultdict(list)` grouping ka best tool hai.

**Complexity:** sorted-key version → Time O(n · k log k), count-key version → O(n · k). Space O(n · k).
"""))
A(code(r'''
from collections import defaultdict, Counter

def group_anagrams_sorted(words):
    # signature = letters sorted (anagrams ka same hoga)
    groups = defaultdict(list)
    for w in words:
        key = "".join(sorted(w.lower()))           # 'eat' aur 'tea' dono -> 'aet'
        groups[key].append(w)
    return list(groups.values())                   # insertion order (Python 3.7+) mehfooz

def group_anagrams_count(words):
    # signature = har letter ka count (sort se tez: O(k) vs O(k log k))
    groups = defaultdict(list)
    for w in words:
        counts = [0] * 26
        for ch in w.lower():
            counts[ord(ch) - 97] += 1              # 'a' -> index 0
        groups[tuple(counts)].append(w)            # list unhashable hai -> tuple banao
    return list(groups.values())

def group_anagrams_unicode(words):
    # Unicode-safe (sirf a-z par depend nahi)
    groups = defaultdict(list)
    for w in words:
        groups[tuple(sorted(Counter(w.lower()).items()))].append(w)
    return list(groups.values())

words = ["eat", "tea", "tan", "ate", "nat", "bat"]
print("sorted-key :", group_anagrams_sorted(words))
print("count-key  :", group_anagrams_count(words))
print("unicode    :", group_anagrams_unicode(words))
print("with case  :", group_anagrams_sorted(["Listen", "Silent", "Enlist", "Google"]))
print("empty str  :", group_anagrams_sorted(["", "", "a"]))

def normalized(groups):
    # comparison ke liye deterministic shape (andar sorted, bahar bhi sorted)
    return sorted(sorted(g) for g in groups)

# ---- tests ----
expected = [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
assert normalized(group_anagrams_sorted(words)) == expected
assert normalized(group_anagrams_count(words)) == expected
assert normalized(group_anagrams_unicode(words)) == expected
assert group_anagrams_sorted([]) == []
assert normalized(group_anagrams_sorted(["a"])) == [["a"]]
assert len(group_anagrams_sorted(["abc", "cba", "bac"])) == 1        # sab ek group
assert len(group_anagrams_sorted(["abc", "abd"])) == 2
print("[pass] Problem 4")
'''))

A(md("""
## Problem 5 — Find duplicates in a list

**Problem:** list me wo saare items batao jo **ek se zyada baar** aate hain.

**Approach A — `set` based (single pass):** ek `seen` set rakho; jo item pehle mil chuka ho use
`dupes` set me daal do. Time O(n), Space O(n). Order matter kare to `dict.fromkeys` ya list use karo.

**Approach B — `Counter`:** `[item for item, n in Counter(lst).items() if n > 1]` — sabse readable,
aur count bhi mil jata hai.

**Approach C — sorting:** `O(n log n)` time, `O(1)` extra space (agar in-place sort allowed ho) —
jab memory tight ho ya items hashable na hon.

**Follow-ups jo interviewer poochta hai:**
- "First duplicate" (sirf pehla) → single pass, mil jate hi return
- "Unhashable items (list of lists)?" → sorting/tuple conversion
- "Duplicate indexes chahiye?" → `defaultdict(list)` me index jama karo
"""))
A(code(r'''
from collections import Counter, defaultdict

def find_duplicates(items):
    # A) single pass, order-preserving (pehli baar duplicate detect hone ke order me)
    seen, dupes = set(), []
    for x in items:
        if x in seen:                              # set membership O(1)
            if x not in dupes:                     # dobara add na ho
                dupes.append(x)
        else:
            seen.add(x)
    return dupes

def find_duplicates_counter(items):
    # B) Counter -> sabse readable
    return [x for x, n in Counter(items).items() if n > 1]

def find_duplicates_sorted(items):
    # C) sorting based, hashing ki zaroorat nahi (sirf comparable hona chahiye)
    s = sorted(items)
    out = []
    for a, b in zip(s, s[1:]):                     # pairwise (neighbour) comparison
        if a == b and (not out or out[-1] != a):   # barabar padosi = duplicate (dobara add na karo)
            out.append(a)
    return out

def first_duplicate(items):
    seen = set()
    for x in items:
        if x in seen:
            return x                               # mil gaya -> foran return
        seen.add(x)
    return None

def duplicate_positions(items):
    # duplicates ke saare indexes
    pos = defaultdict(list)
    for i, x in enumerate(items):
        pos[x].append(i)
    return {x: idxs for x, idxs in pos.items() if len(idxs) > 1}

data = [1, 3, 5, 3, 7, 1, 9, 1]
print("set based    :", find_duplicates(data))
print("Counter based:", sorted(find_duplicates_counter(data)))
print("sorted based :", find_duplicates_sorted(data))
print("with counts  :", {x: n for x, n in Counter(data).items() if n > 1})
print("first dup    :", first_duplicate(data))
print("positions    :", duplicate_positions(data))
print("strings      :", find_duplicates(["a", "b", "a", "c", "b"]))
print("unhashable   :", find_duplicates([tuple(x) for x in ([1, 2], [3], [1, 2])]))
print("no dupes     :", find_duplicates([1, 2, 3]), first_duplicate([1, 2, 3]))

# ---- tests ----
assert find_duplicates([1, 3, 5, 3, 7, 1, 9, 1]) == [3, 1]
assert sorted(find_duplicates_counter([1, 3, 5, 3, 7, 1])) == [1, 3]
assert find_duplicates([]) == [] and find_duplicates([1]) == []
assert first_duplicate([1, 2, 3, 2, 1]) == 2
assert first_duplicate([]) is None
assert duplicate_positions([1, 1, 2]) == {1: [0, 1]}
assert find_duplicates(["x", "x", "x"]) == ["x"]                 # 3 baar -> ek hi entry
assert set(find_duplicates(data)) == set(find_duplicates_counter(data)) == set(find_duplicates_sorted(data))
print("[pass] Problem 5")
'''))

A(md("""
## Problem 6 — Rotate a matrix 90° (clockwise)

**Problem:** `[[1,2],[3,4]]` → `[[3,1],[4,2]]` (clockwise 90°).

**Approach (Pythonic one-liner):** `[list(row) for row in zip(*matrix[::-1])]`
- `matrix[::-1]` → rows ulti (bottom row upar aa gayi)
- `zip(*...)` → transpose (columns → rows)
- Dono mila kar = clockwise rotation

**Counter-clockwise:** `[list(row) for row in zip(*matrix)][::-1]` (transpose phir reverse rows).

**Manual formula:** clockwise me `new[c][rows-1-r] = old[r][c]`.

**In-place version** (square matrix) LeetCode 48 section me — wahan `rotate_image_inplace` naam se.

**Complexity:** Time O(n·m), Space O(n·m) (new matrix) — in-place O(1) extra.
"""))
A(code(r'''
def rotate_90(matrix):
    # clockwise: pehle rows ulti karo, phir transpose
    return [list(row) for row in zip(*matrix[::-1])]

def rotate_90_ccw(matrix):
    # counter-clockwise: transpose karo, phir rows ulti
    return [list(row) for row in zip(*matrix)][::-1]

def rotate_90_manual(matrix):
    # index math wala version (interviewer 'zip mat use karo' keh de to)
    if not matrix:
        return []
    rows, cols = len(matrix), len(matrix[0])
    out = [[0] * rows for _ in range(cols)]        # naya size: cols x rows (comprehension - shared row bug se bachao)
    for r in range(rows):
        for c in range(cols):
            out[c][rows - 1 - r] = matrix[r][c]    # clockwise mapping
    return out

def rotate_180(matrix):
    return [row[::-1] for row in matrix[::-1]]     # 90 do baar = row+col dono ulte

m2 = [[1, 2], [3, 4]]
m3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rect = [[1, 2, 3], [4, 5, 6]]                      # non-square bhi chalna chahiye

print("2x2 cw   :", rotate_90(m2))
print("3x3 cw   :", rotate_90(m3))
print("3x3 ccw  :", rotate_90_ccw(m3))
print("2x3 cw   :", rotate_90(rect), "<- shape 3x2 ban gaya")
print("manual   :", rotate_90_manual(m3))
print("180      :", rotate_180(m3))
print("original safe:", m3)                        # naya matrix bana, purana chhera nahi

# ---- tests ----
assert rotate_90([[1, 2], [3, 4]]) == [[3, 1], [4, 2]]
assert rotate_90(m3) == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
assert rotate_90_manual(m3) == rotate_90(m3)
assert rotate_90(rect) == [[4, 1], [5, 2], [6, 3]]
assert rotate_90_ccw([[1, 2], [3, 4]]) == [[2, 4], [1, 3]]
assert rotate_90(rotate_90(rotate_90(rotate_90(m3)))) == m3       # 4 baar = wapas wahi
assert rotate_180(m3) == rotate_90(rotate_90(m3))
assert rotate_90([]) == [] and rotate_90_manual([]) == []
assert rotate_90([[1]]) == [[1]]
print("[pass] Problem 6")
'''))

A(md("""
## Problem 7 — Spiral print of a matrix

**Problem:** matrix ko bahar se andar, ghadi ki soi ki tarah (clockwise spiral) print karo.
```
1 2 3        ->  1 2 3 6 9 8 7 4 5
4 5 6
7 8 9
```

**Approach A — boundary shrinking (classic):** 4 pointers rakho — `top, bottom, left, right`.
Har round me: top row left→right, right column top→bottom, bottom row right→left, left column bottom→top.
Phir boundaries andar khiskao. **Zaroori guard:** teesre/chauthe step se pehle check karo ke `top <= bottom`
aur `left <= right` warna single row/column double count ho jata hai (yehi sabse common bug hai).

**Approach B — "peel + rotate" (bohat Pythonic):** pehli row nikalo, baqi matrix ko counter-clockwise
rotate karo, repeat. 3 lines me kaam. Time same, code chhota.

**Complexity:** Time O(n·m) (har cell ek baar), Space O(n·m) output ke liye, O(1) extra (approach A).
"""))
A(code(r'''
def spiral_print(matrix):
    # A) boundary shrinking
    if not matrix or not matrix[0]:
        return []
    out = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for c in range(left, right + 1):           # 1) top row: left -> right
            out.append(matrix[top][c])
        top += 1

        for r in range(top, bottom + 1):           # 2) right column: top -> bottom
            out.append(matrix[r][right])
        right -= 1

        if top <= bottom:                          # GUARD: warna single row do baar
            for c in range(right, left - 1, -1):   # 3) bottom row: right -> left
                out.append(matrix[bottom][c])
            bottom -= 1

        if left <= right:                          # GUARD: warna single column do baar
            for r in range(bottom, top - 1, -1):   # 4) left column: bottom -> top
                out.append(matrix[r][left])
            left += 1
    return out

def spiral_peel(matrix):
    # B) peel + rotate CCW (Pythonic, recursion/loop dono se ho sakta hai)
    rows = [list(r) for r in matrix]               # copy (input safe rahe)
    out = []
    while rows:
        out.extend(rows.pop(0))                    # pehli row utha lo
        rows = [list(r) for r in zip(*rows)][::-1] # baqi ko CCW rotate -> nayi "pehli row" tayyar
    return out

m3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
m34 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
print("3x3      :", spiral_print(m3))
print("3x4      :", spiral_print(m34))
print("peel 3x4 :", spiral_peel(m34))
print("1 row    :", spiral_print([[1, 2, 3, 4]]))
print("1 col    :", spiral_print([[1], [2], [3]]))
print("2x2      :", spiral_print([[1, 2], [3, 4]]))
print("original safe:", m34[0])

# pretty print (spiral order me numbers ko grid me wapas rakhna)
def spiral_fill(n):
    # 1..n*n ko spiral order me bharo (reverse problem - ye bhi poocha jata hai)
    grid = [[0] * n for _ in range(n)]
    top, bottom, left, right, val = 0, n - 1, 0, n - 1, 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            grid[top][c] = val; val += 1
        top += 1
        for r in range(top, bottom + 1):
            grid[r][right] = val; val += 1
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                grid[bottom][c] = val; val += 1
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                grid[r][left] = val; val += 1
            left += 1
    return grid

print("\nspiral_fill(4):")
for row in spiral_fill(4):
    print("   ", " ".join(f"{v:>2}" for v in row))

# ---- tests ----
assert spiral_print(m3) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
assert spiral_print(m34) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
assert spiral_peel(m3) == spiral_print(m3)
assert spiral_peel(m34) == spiral_print(m34)
assert spiral_print([[1, 2, 3, 4]]) == [1, 2, 3, 4]              # single row - guard test
assert spiral_print([[1], [2], [3]]) == [1, 2, 3]                # single column - guard test
assert spiral_print([[7]]) == [7]
assert spiral_print([]) == [] and spiral_print([[]]) == []
assert sorted(spiral_print(m34)) == sorted(x for row in m34 for x in row)   # koi cell miss/duplicate nahi
assert spiral_print(spiral_fill(4)) == list(range(1, 17))         # fill aur print ek doosre ka ulta
print("[pass] Problem 7")
'''))

A(md("""
## Problem 8 — Chunk a list into pieces of size n

**Problem:** `[1,2,3,4,5], n=2` → `[[1,2],[3,4],[5]]` (aakhri chunk chhota ho sakta hai).

**Approach A — slicing + `range(0, len, n)`:** sabse readable aur fast: `[lst[i:i+n] for i in range(0, len(lst), n)]`.
Slicing out-of-range par crash nahi karti, is liye aakhri chhota chunk automatic sambhal jata hai.

**Approach B — `itertools.islice` generator:** bare data/iterator ke liye (memory O(chunk)).

**Approach C — `itertools.batched(it, n)`** — Python **3.12+** ka naya built-in (tuples deta hai). 3.14 me available hai.

**Zaroori validation:** `n <= 0` par `ValueError` raise karo — warna infinite loop ya khali output.

**Complexity:** Time O(n), Space O(n) (generator version me O(chunk)).
"""))
A(code(r'''
from itertools import islice, batched

def chunk_list(items, size):
    # A) slicing based - sabse aasan aur tez
    if size <= 0:
        raise ValueError("size must be positive")          # defensive check
    return [items[i:i + size] for i in range(0, len(items), size)]

def chunk_gen(iterable, size):
    # B) kisi bhi iterator par chalta hai (list banane ki zaroorat nahi)
    if size <= 0:
        raise ValueError("size must be positive")
    it = iter(iterable)                                    # explicit iterator
    while chunk := list(islice(it, size)):                 # walrus + islice
        yield chunk

def chunk_builtin(iterable, size):
    # C) Python 3.12+ ka itertools.batched (tuples deta hai)
    return [list(b) for b in batched(iterable, size)]

def chunk_evenly(items, parts):
    # Bonus: N *parts* me barabar taqseem (chunk size nahi, parts count diya hai)
    k, m = divmod(len(items), parts)                       # divmod -> quotient + remainder
    out, start = [], 0
    for i in range(parts):
        end = start + k + (1 if i < m else 0)              # pehle m parts ko ek extra item
        out.append(items[start:end])
        start = end
    return out

data = [1, 2, 3, 4, 5, 6, 7]
print("size 2   :", chunk_list(data, 2))
print("size 3   :", chunk_list(data, 3))
print("size 10  :", chunk_list(data, 10), "<- size > len")
print("generator:", list(chunk_gen(iter(data), 3)))
print("batched  :", chunk_builtin(data, 3))
print("string   :", chunk_list("abcdefg", 3))
print("3 parts  :", chunk_evenly(data, 3), "<- 3,2,2")
try:
    chunk_list(data, 0)
except ValueError as e:
    print("ValueError:", e)

# ---- tests ----
assert chunk_list([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
assert chunk_list([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]
assert chunk_list([], 3) == []
assert chunk_list([1], 5) == [[1]]
assert list(chunk_gen(range(5), 2)) == [[0, 1], [2, 3], [4]]
assert chunk_builtin([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
assert chunk_list("abcde", 2) == ["ab", "cd", "e"]                # strings par bhi (slicing generic hai)
assert chunk_evenly([1, 2, 3, 4, 5, 6, 7], 3) == [[1, 2, 3], [4, 5], [6, 7]]
assert sum(len(c) for c in chunk_list(data, 3)) == len(data)       # kuch gum na hua
print("[pass] Problem 8")
'''))

A(md("""
## Problem 9 — Run-Length Encoding (encode + decode)

**Problem:** `"aaabbbcccc"` → `"a3b3c4"`, aur wapas decode.

**Approach (encode):** consecutive characters count karo. Do tareeqe:
- Manual single pass: pichhla char yaad rakho, count barhao, badalne par flush karo.
- `itertools.groupby(s)` — consecutive groups **built-in** de deta hai (sabse saaf).

**Approach (decode):** digits jama karo (multi-digit counts! `"a12"` → 12 baar) aur `char * count` jor do.
`re` bhi chalta hai, magar interview me manual parsing dikhana behtar hai.

**Round-trip property:** `decode(encode(s)) == s` — ye best test hai (digits wale input ke ilawa;
`"a1b2"` jaisa input ambiguous ho jata hai — ye edge case interviewer ko batao).

**Complexity:** encode Time O(n) Space O(n); decode Time O(output length).
"""))
A(code(r'''
from itertools import groupby

def rle_encode(s):
    # single pass manual version
    if not s:
        return ""
    out = []
    prev, count = s[0], 1
    for ch in s[1:]:                               # doosre char se shuru
        if ch == prev:
            count += 1                             # streak jari
        else:
            out.append(f"{prev}{count}")           # streak khatam -> flush
            prev, count = ch, 1
    out.append(f"{prev}{count}")                   # aakhri streak (bhoolna common bug hai)
    return "".join(out)                            # join idiom, += nahi

def rle_encode_groupby(s):
    # itertools.groupby = consecutive grouping built-in
    return "".join(f"{ch}{sum(1 for _ in grp)}" for ch, grp in groupby(s))

def rle_decode(s):
    # multi-digit counts support ("a12" -> 12 a's)
    out, i, n = [], 0, len(s)
    while i < n:
        ch = s[i]                                  # character
        i += 1
        digits = []
        while i < n and s[i].isdigit():            # uske baad ke saare digits
            digits.append(s[i])
            i += 1
        count = int("".join(digits)) if digits else 1   # count na ho to 1
        out.append(ch * count)
    return "".join(out)

def rle_encode_smart(s):
    # practical version: count 1 ho to number skip (chhota output)
    return "".join(ch if (n := sum(1 for _ in g)) == 1 else f"{ch}{n}" for ch, g in groupby(s))

print("encode 'aaabbbcccc' :", rle_encode("aaabbbcccc"))
print("groupby version     :", rle_encode_groupby("aaabbbcccc"))
print("decode 'a3b3c4'     :", rle_decode("a3b3c4"))
print("multi-digit         :", rle_encode("a" * 12), "->", rle_decode(rle_encode("a" * 12))[:5], "...")
print("smart encode        :", rle_encode_smart("aaabcccd"), "(count 1 skip)")
print("mixed case          :", rle_encode("aAaA"))
print("compression ratio   :", f"{len(rle_encode('a'*50))}/{50}")
print("expansion warning   :", rle_encode("abcd"), "<- 4 chars -> 8 chars (RLE hamesha chhota nahi karta)")

# ---- tests ----
assert rle_encode("aaabbbcccc") == "a3b3c4"
assert rle_encode_groupby("aaabbbcccc") == "a3b3c4"
assert rle_encode("") == "" and rle_encode_groupby("") == ""
assert rle_encode("a") == "a1"
assert rle_encode("abc") == "a1b1c1"
assert rle_decode("a3b3c4") == "aaabbbcccc"
assert rle_decode("") == ""
assert rle_decode("a12") == "a" * 12                              # multi-digit
assert rle_decode("x") == "x"                                     # count missing -> 1
for original in ("aaabbbcccc", "a", "", "abcd", "zzzzzzzzzzzz", "aAaA", "  a  "):
    assert rle_decode(rle_encode(original)) == original, f"round-trip fail: {original!r}"
assert rle_encode_smart("aaabcccd") == "a3bc3d"
print("[pass] Problem 9")
'''))

A(md("""
## Problem 10 — Balanced brackets

**Problem:** `"{[()]}"` → `True`, `"{[(])}"` → `False`. Sirf order aur pairing check karni hai.

**Approach — stack (classic):**
1. Opening bracket aaye → stack me push
2. Closing aaye → stack se pop karo aur dekho ke matching opening hai ya nahi
   (khali stack par closing = fail)
3. Aakhir me stack **khali** honi chahiye (warna koi bracket band nahi hua)

Mapping dict (`{")": "("}`) code ko saaf rakhti hai. Non-bracket characters ignore.

**Common bugs:** (a) aakhir me stack empty check bhoolna, (b) khali stack par `pop()` → `IndexError`,
(c) sirf counting karna (`count("(") == count(")")`) — ye `")("` ko galat pass kar deta hai.

**Complexity:** Time O(n), Space O(n) worst case (sab opening brackets).
"""))
A(code(r'''
PAIRS = {")": "(", "]": "[", "}": "{"}            # closing -> opening
OPENERS = set(PAIRS.values())

def is_balanced(s):
    stack = []
    for ch in s:
        if ch in OPENERS:                          # opening -> push
            stack.append(ch)
        elif ch in PAIRS:                          # closing -> match check
            if not stack or stack.pop() != PAIRS[ch]:
                return False                       # khali stack ya galat pairing
        # baqi characters (letters, spaces) ignore
    return not stack                               # khali stack = sab band ho gaya

def is_balanced_counting(s):
    # BAD approach (sirf single type ke liye kaam karta hai) - demo ke liye
    return s.count("(") == s.count(")")

def first_unbalanced_index(s):
    # bonus: kahan gharbar hui? (linter/editor jaisa feedback)
    stack = []
    for i, ch in enumerate(s):
        if ch in OPENERS:
            stack.append((ch, i))
        elif ch in PAIRS:
            if not stack or stack[-1][0] != PAIRS[ch]:
                return i                           # ye closing galat hai
            stack.pop()
    return stack[0][1] if stack else -1            # jo opening kabhi band nahi hua

tests = ["{[()]}", "{[(])}", "((", "))", "", "a(b)c[d]{e}", "([)]", "(()())", ")("]
for t in tests:
    print(f"  {t!r:<14} -> {is_balanced(t)}")

print("\ncounting approach ka fail:", ")(", "->", is_balanced_counting(")("), "(stack ne pakra:", is_balanced(")("), ")")
print("first bad index in '([)]' :", first_unbalanced_index("([)]"))
print("first bad index in '(('   :", first_unbalanced_index("(("))
print("valid string ka index     :", first_unbalanced_index("{[()]}"), "(-1 = sab theek)")

# ---- tests ----
assert is_balanced("{[()]}") is True
assert is_balanced("{[(])}") is False
assert is_balanced("") is True                     # khali string balanced hai
assert is_balanced("(") is False and is_balanced(")") is False
assert is_balanced(")(") is False                  # order galat
assert is_balanced("a(b)c[d]{e}") is True          # non-bracket chars ignore
assert is_balanced("(()())") is True
assert is_balanced("([)]") is False
assert is_balanced("[" * 100 + "]" * 100) is True  # deep nesting
assert first_unbalanced_index("{[()]}") == -1
assert first_unbalanced_index("(()") == 0
print("[pass] Problem 10")
'''))

A(md("""
## Problem 11 — Roman ↔ Integer (dono directions)

**Roman → Integer:** Rule ye hai ke agar chhoti value bari value se **pehle** aaye to wo **minus** hoti hai
(`IV = 5 - 1 = 4`). Do tareeqe:
- **Right-to-left scan:** aakhir se chalo; agar current value pichhli (right wali) se **chhoti** hai to
  minus karo warna plus. Ek pass, bohat saaf.
- **Pair lookup:** 6 special pairs (`IV, IX, XL, XC, CD, CM`) ko pehle handle karo.

**Integer → Roman:** greedy — sabse bari value se shuru karo, jitni baar fit ho utni baar likho, phir
next value par jao. Value table me subtractive pairs (`900: "CM"`) **shamil** kar do → greedy khud hi sahi
jawab de deta hai.

**Complexity:** dono O(1) practically (roman numerals ki max length bounded hai; technically O(len(s)) / O(#symbols)).
Valid range LeetCode par 1..3999.
"""))
A(code(r'''
ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

def roman_to_int_basic(s):
    # right-to-left scan: chhota symbol bare se pehle -> minus
    total, prev = 0, 0
    for ch in reversed(s.upper()):                 # aakhir se shuru
        val = ROMAN_VALUES[ch]
        total += -val if val < prev else val       # ternary: subtractive case
        prev = max(prev, val)                      # sabse bari dekhi hui value yaad rakho
    return total

INT_TO_ROMAN_TABLE = (
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
)

def int_to_roman_basic(num):
    if not 1 <= num <= 3999:
        raise ValueError("roman numerals support 1..3999")
    out = []
    for value, symbol in INT_TO_ROMAN_TABLE:       # bari value se chhoti taraf (greedy)
        count, num = divmod(num, value)            # divmod = kitni baar + baqi
        out.append(symbol * count)                 # count 0 ho to khali string (safe)
        if num == 0:
            break                                  # early exit
    return "".join(out)

print("MCMXCIV ->", roman_to_int_basic("MCMXCIV"))
print("1994    ->", int_to_roman_basic(1994))
for n in (1, 4, 9, 14, 40, 58, 400, 1987, 3999):
    r = int_to_roman_basic(n)
    print(f"  {n:>4} -> {r:<15} -> back {roman_to_int_basic(r)}")
try:
    int_to_roman_basic(4000)
except ValueError as e:
    print("ValueError:", e)

# ---- tests ----
assert roman_to_int_basic("III") == 3
assert roman_to_int_basic("IV") == 4 and roman_to_int_basic("IX") == 9
assert roman_to_int_basic("LVIII") == 58
assert roman_to_int_basic("MCMXCIV") == 1994
assert roman_to_int_basic("mcmxciv") == 1994                 # lowercase bhi
assert int_to_roman_basic(3) == "III"
assert int_to_roman_basic(4) == "IV" and int_to_roman_basic(9) == "IX"
assert int_to_roman_basic(58) == "LVIII"
assert int_to_roman_basic(1994) == "MCMXCIV"
assert int_to_roman_basic(3999) == "MMMCMXCIX"
# round trip 1..3999 (poora range - sabse strong test)
assert all(roman_to_int_basic(int_to_roman_basic(n)) == n for n in range(1, 4000))
print("[pass] Problem 11 (round-trip 1..3999 verified)")
'''))

A(md("""
## Problem 12 — Caesar cipher (encrypt + decrypt)

**Problem:** har letter ko `k` positions aage shift karo (`a` + 3 → `d`), case preserve karo,
non-letters (space, punctuation, digits) waise hi rakho. Decrypt = `-k` shift.

**Approach A — arithmetic:** `chr((ord(ch) - base + k) % 26 + base)` jahan `base` = `ord('a')` ya `ord('A')`.
`% 26` wrap-around sambhalta hai (z + 1 → a) aur negative `k` bhi (Python ka `%` hamesha non-negative
deta hai jab divisor positive ho — C se different!).

**Approach B — `str.maketrans` translate table:** ek table bana kar poore string par ek pass — sabse tez,
aur "idiomatic Python" wala jawab.

**Complexity:** Time O(n), Space O(n) (output string) / O(1) table.

**Interview follow-up:** `k=13` = ROT13, jiska encrypt aur decrypt **same** function hai (self-inverse).
"""))
A(code(r'''
import string

def caesar_encrypt(text, k=3):
    # arithmetic version - har char par kaam
    out = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")     # case preserve
            out.append(chr((ord(ch) - base + k) % 26 + base)) # % 26 -> wrap-around
        else:
            out.append(ch)                                    # non-letters untouched
    return "".join(out)

def caesar_decrypt(text, k=3):
    return caesar_encrypt(text, -k)                # ulta shift (Python ka % negative sambhal leta hai)

def caesar_translate(text, k=3):
    # translate table version (tez + Pythonic)
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    k %= 26
    table = str.maketrans(lower + upper, lower[k:] + lower[:k] + upper[k:] + upper[:k])
    return text.translate(table)

def rot13(text):
    return caesar_encrypt(text, 13)                # self-inverse (13 + 13 = 26)

msg = "Attack at Dawn, Zulu-7!"
enc = caesar_encrypt(msg, 3)
print("plain  :", msg)
print("enc(3) :", enc)
print("dec(3) :", caesar_decrypt(enc, 3))
print("translate version matches:", caesar_translate(msg, 3) == enc)
print("wrap   :", caesar_encrypt("xyz XYZ", 3), "<- z -> c")
print("k=0    :", caesar_encrypt(msg, 0))
print("k=26   :", caesar_encrypt(msg, 26), "<- full circle")
print("k=-3   :", caesar_encrypt("def", -3))
print("rot13  :", rot13("Hello"), "->", rot13(rot13("Hello")), "(self-inverse)")

# brute force crack (25 possibilities) - short secret ke liye kaafi
secret = caesar_encrypt("the meeting is at noon", 7)
print("\ncracking:", secret)
for shift in range(1, 26):
    candidate = caesar_decrypt(secret, shift)
    if "the" in candidate:                          # common word detector
        print(f"  shift {shift:>2} -> {candidate}   <-- mil gaya!")

# ---- tests ----
assert caesar_encrypt("abc", 3) == "def"
assert caesar_encrypt("xyz", 3) == "abc"                      # wrap
assert caesar_encrypt("XYZ", 3) == "ABC"                      # uppercase wrap
assert caesar_encrypt("Hello, World!", 3) == "Khoor, Zruog!"  # punctuation safe
assert caesar_decrypt(caesar_encrypt("Hello, World!", 5), 5) == "Hello, World!"
assert caesar_encrypt("abc", 0) == "abc" and caesar_encrypt("abc", 26) == "abc"
assert caesar_encrypt("abc", -1) == "zab"                     # negative shift
assert caesar_encrypt("abc", 29) == caesar_encrypt("abc", 3)  # k > 26
assert caesar_translate(msg, 11) == caesar_encrypt(msg, 11)
assert rot13(rot13("Any Text 123!")) == "Any Text 123!"
assert caesar_encrypt("", 5) == ""
print("[pass] Problem 12")
'''))

A(md("""
## Problem 13 — First non-repeating character

**Problem:** `"swiss"` → `"w"` (pehla character jo sirf ek baar aata hai). Koi na ho to `None`.

**Approach — two pass with `Counter`:**
1. Pehla pass: har char ka count (O(n))
2. Doosra pass: **original order** me chalo, pehla `count == 1` wala return karo

Kyun do pass? Kyunki "pehla" ka matlab original order me pehla — sirf counts se order nahi milta.
Python 3.7+ me `dict`/`Counter` insertion-ordered hain, is liye `next(c for c, n in counts.items() if n == 1)`
bhi kaam kar jata hai — ye ek pass + ek scan wala smart jawab hai.

**Complexity:** Time O(n), Space O(k) (k = distinct characters, ASCII me O(1)).

**Follow-up:** streaming data me? → `OrderedDict` + "repeated" set, ya index+count store karo.
"""))
A(code(r'''
from collections import Counter, OrderedDict

def first_non_repeating(s):
    counts = Counter(s)                            # pass 1: counts
    for ch in s:                                   # pass 2: original order
        if counts[ch] == 1:
            return ch
    return None                                    # sab repeat hote hain

def first_non_repeating_dictorder(s):
    # Counter khud insertion-ordered hai -> alag se s par loop ki zaroorat nahi
    counts = Counter(s)
    return next((ch for ch, n in counts.items() if n == 1), None)   # next + default

def first_non_repeating_index(s):
    # index bhi chahiye (kabhi problem ye maangti hai)
    counts = Counter(s)
    return next(((i, ch) for i, ch in enumerate(s) if counts[ch] == 1), (-1, None))

def first_non_repeating_word(sentence):
    # word-level version (real interview twist)
    words = sentence.lower().split()
    counts = Counter(words)
    return next((w for w in words if counts[w] == 1), None)

for s in ("swiss", "aabbcc", "abcabc", "x", "", "aabbc", "Swiss"):
    print(f"  {s!r:<10} -> {first_non_repeating(s)!r:<6} (dict-order: {first_non_repeating_dictorder(s)!r})")

print("\nwith index :", first_non_repeating_index("swiss"))
print("word level :", first_non_repeating_word("the cat the dog a cat runs"))
print("case matters:", first_non_repeating("sSwiss"), "<- 's' aur 'S' alag characters hain")

# ---- tests ----
assert first_non_repeating("swiss") == "w"
assert first_non_repeating("aabbcc") is None
assert first_non_repeating("aabbc") == "c"
assert first_non_repeating("x") == "x"
assert first_non_repeating("") is None
assert first_non_repeating("abcabc") is None
assert first_non_repeating("leetcode") == "l"
assert first_non_repeating("loveleetcode") == "v"
assert first_non_repeating_dictorder("swiss") == "w"
assert first_non_repeating_index("swiss") == (1, "w")          # index 1 par 'w'
assert first_non_repeating_index("aabb") == (-1, None)
assert first_non_repeating_word("the cat the dog a cat runs") == "dog"
assert all(first_non_repeating(x) == first_non_repeating_dictorder(x) for x in ("swiss", "", "aab", "xyz"))
print("[pass] Problem 13")
'''))

A(md("""
## Problem 14 — Longest word in a sentence

**Problem:** sentence me sabse lamba word batao. Punctuation count nahi honi chahiye, aur tie par
**pehla** word jeetna chahiye.

**Approach:** `max(words, key=len)` — bas. `max` **pehle** maximum ko rakhta hai (ties par pehla),
`min` bhi wahi. Punctuation `str.translate`/`strip` se hatao.

**Edge cases:** khali string → `max()` `ValueError` deta hai → `default=` argument use karo:
`max(words, key=len, default="")`. Ye chhoti detail interview me impress karti hai.

**Complexity:** Time O(n), Space O(n) (words list) — streaming version O(1) extra.
"""))
A(code(r'''
import string

PUNCT = str.maketrans("", "", string.punctuation)

def longest_word(sentence):
    words = sentence.translate(PUNCT).split()      # punctuation hata kar tokenize
    return max(words, key=len, default="")         # default -> khali input par crash nahi

def longest_word_all(sentence):
    # saare longest words (tie hone par sab)
    words = sentence.translate(PUNCT).split()
    if not words:
        return []
    longest = max(len(w) for w in words)
    return [w for w in words if len(w) == longest]

def top_n_longest(sentence, n=3):
    words = sentence.translate(PUNCT).split()
    # -len(w) se DESC, phir w se alphabetical (deterministic ties)
    return sorted(words, key=lambda w: (-len(w), w))[:n]

def longest_word_streaming(sentence):
    # O(1) extra space: sirf best yaad rakho (bare files ke liye pattern)
    best = ""
    for w in sentence.translate(PUNCT).split():
        if len(w) > len(best):                     # '>' (na ke '>=') -> tie par pehla jeeta
            best = w
    return best

s = "Python's comprehension syntax makes extraordinary transformations effortless!"
print("longest      :", longest_word(s))
print("all longest  :", longest_word_all("cat bat dog"))
print("top 3        :", top_n_longest(s, 3))
print("streaming    :", longest_word_streaming(s))
print("punctuation  :", longest_word("wow, unbelievable!!!"), "<- '!' count nahi hua")
print("empty        :", repr(longest_word("")), "| repr(...) se nazar aata hai ke khali string hai")
print("tie          :", longest_word("abc xyz"), "<- pehla jeeta")
print("shortest     :", min(s.translate(PUNCT).split(), key=len))

# ---- tests ----
assert longest_word("I love programming in Python") == "programming"
assert longest_word("wow, unbelievable!!!") == "unbelievable"
assert longest_word("abc xyz") == "abc"                       # tie -> pehla
assert longest_word("") == ""                                 # default ne bachaya
assert longest_word("   ") == ""
assert longest_word("a") == "a"
assert longest_word_all("cat bat dog") == ["cat", "bat", "dog"]
assert longest_word_all("") == []
assert top_n_longest("aaa bb cccc dd", 2) == ["cccc", "aaa"]
assert longest_word_streaming(s) == longest_word(s)
assert longest_word("Python's") == "Pythons"                  # apostrophe hat gaya
print("[pass] Problem 14")
'''))

A(md("""
## Problem 15 — Sum of digits till single digit (digital root)

**Problem:** `9875` → `9+8+7+5 = 29` → `2+9 = 11` → `1+1 = 2`. Jawab `2`.

**Approach A — loop (jo interviewer dekhna chahta hai):** jab tak `n >= 10`, digits ka sum lo.
Digits nikalne ke do tareeqe: `divmod`/`%10` arithmetic, ya `sum(int(d) for d in str(n))`
(string wala readable hai, arithmetic wala "proper" maana jata hai).

**Approach B — O(1) formula (digital root):** `0` ho to `0`, warna `1 + (n - 1) % 9`.
Ye kaam karta hai kyunki `n ≡ digit_sum(n) (mod 9)` — base-10 ka property. Ye jawab dene par
interviewer khush hota hai ("mod 9 congruence").

**Complexity:** A → O(log n) per pass, kul O(log n) (passes bohat jaldi ghat jate hain); B → O(1).
"""))
A(code(r'''
def digital_root_loop(n):
    n = abs(n)                                     # negative ko positive maan lo
    while n >= 10:                                 # jab tak ek digit na bache
        n = sum(int(d) for d in str(n))            # readable digit sum
    return n

def digital_root_arithmetic(n):
    n = abs(n)
    while n >= 10:
        total = 0
        while n:
            n, digit = divmod(n, 10)               # aakhri digit nikalo
            total += digit
        n = total
    return n

def digital_root_formula(n):
    # O(1): mod-9 congruence
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9

def digit_sum_steps(n):
    # steps dikhane ke liye (teaching / debugging)
    steps = [n]
    while n >= 10:
        n = sum(int(d) for d in str(n))
        steps.append(n)
    return steps

print("9875 steps :", " -> ".join(map(str, digit_sum_steps(9875))))
print("38 steps   :", " -> ".join(map(str, digit_sum_steps(38))))
print("999999999  :", digital_root_loop(999999999), digital_root_formula(999999999))
for n in (0, 5, 10, 18, 38, 123, 9875, 99999):
    print(f"  {n:>6} -> loop {digital_root_loop(n)} | arithmetic {digital_root_arithmetic(n)} | formula {digital_root_formula(n)}")

# ---- tests ----
assert digital_root_loop(9875) == 2
assert digital_root_loop(38) == 2
assert digital_root_loop(0) == 0
assert digital_root_loop(9) == 9
assert digital_root_loop(10) == 1
assert digital_root_formula(0) == 0
assert digital_root_formula(9) == 9 and digital_root_formula(18) == 9
assert digit_sum_steps(9875) == [9875, 29, 11, 2]
# teeno versions 0..2000 tak barabar hone chahiye (strong equivalence test)
assert all(digital_root_loop(n) == digital_root_arithmetic(n) == digital_root_formula(n) for n in range(2001))
assert digital_root_loop(-38) == 2                            # negative handle
print("[pass] Problem 15 (0..2000 tak teeno approaches barabar)")
'''))

A(md("""
## Problem 16 — Transpose a matrix

**Problem:** rows ↔ columns badal do. `[[1,2,3],[4,5,6]]` → `[[1,4],[2,5],[3,6]]`.

**Approach A — `zip(*matrix)`:** Pythonic king. `*` rows ko separate arguments bana deta hai,
`zip` unko column-wise jor deta hai (tuples milte hain → `list()` se convert karo).

**Approach B — nested comprehension:** `[[row[c] for row in matrix] for c in range(len(matrix[0]))]`
Ye "interviewer said no zip" wala jawab hai. Dhyan do: bahar wali loop **columns** par hai.

**Approach C — in-place (sirf square matrix):** `for i in range(n): for j in range(i+1, n): swap` —
O(1) extra space. Non-square me in-place possible nahi (shape badalti hai).

**Complexity:** Time O(n·m), Space O(n·m) (A/B) ya O(1) extra (C).

**Gotcha:** jagged (uneven) rows par `zip` chhoti row par ruk jata hai → data gum. `zip_longest` use karo.
"""))
A(code(r'''
from itertools import zip_longest

def transpose_matrix(matrix):
    # A) zip(*matrix) - tuples ko list me convert
    return [list(col) for col in zip(*matrix)]

def transpose_nested(matrix):
    # B) bina zip (index math) - bahar wali loop columns par
    if not matrix or not matrix[0]:
        return []
    return [[row[c] for row in matrix] for c in range(len(matrix[0]))]

def transpose_inplace(square):
    # C) sirf square matrix, O(1) extra space
    n = len(square)
    for i in range(n):
        for j in range(i + 1, n):                  # sirf upper triangle -> warna do baar swap
            square[i][j], square[j][i] = square[j][i], square[i][j]
    return square

def transpose_jagged(matrix, fill=None):
    # jagged rows safe (zip data kha jata hai)
    return [list(col) for col in zip_longest(*matrix, fillvalue=fill)]

rect = [[1, 2, 3], [4, 5, 6]]
sq = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
jag = [[1, 2, 3], [4, 5], [6]]

print("rect        :", rect)
print("transpose   :", transpose_matrix(rect))
print("nested ver  :", transpose_nested(rect))
print("tuples only :", list(zip(*rect)), "<- zip tuples deta hai")
print("jagged+zip  :", transpose_matrix(jag), "<- data gum! (zip truncate)")
print("jagged safe :", transpose_jagged(jag, fill=0))
print("in-place    :", transpose_inplace([r[:] for r in sq]))
print("single row  :", transpose_matrix([[1, 2, 3]]))
print("single col  :", transpose_matrix([[1], [2], [3]]))

# ---- tests ----
assert transpose_matrix([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
assert transpose_nested([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
assert transpose_matrix(transpose_matrix(rect)) == rect        # double transpose = original
assert transpose_matrix([[1]]) == [[1]]
assert transpose_matrix([[1, 2, 3]]) == [[1], [2], [3]]
assert transpose_matrix([]) == [] and transpose_nested([]) == []
assert transpose_inplace([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
assert transpose_jagged(jag, 0) == [[1, 4, 6], [2, 5, 0], [3, 0, 0]]
# transpose + reverse rows == rotate 90 (Problem 6 se link)
assert [r[::-1] for r in transpose_matrix(sq)] == rotate_90(sq)
print("[pass] Problem 16")
'''))

A(md("""
## Problem 17 — Moving average (sliding window)

**Problem:** `[1,2,3,4,5]`, window `k=3` → `[2.0, 3.0, 4.0]` (har consecutive 3 ka average).

**Approach A — slicing (readable):** `[sum(nums[i:i+k]) / k for i in range(len(nums) - k + 1)]`
Time O(n·k) — chhote k ke liye theek.

**Approach B — running sum (optimal):** window ko slide karte waqt naya element **add** karo aur purana
**subtract** karo → har step O(1), total **O(n)**. Ye wo jawab hai jo interviewer chahta hai.

**Approach C — `collections.deque(maxlen=k)`:** streaming data ke liye — deque khud purana element
girata rehta hai (real-time metrics/monitoring ka pattern).

**Edge cases:** `k > len(nums)` → khali list; `k <= 0` → `ValueError`; float precision ke liye
`round()` ya `math.isclose` se compare karo.

**Complexity:** A → O(n·k); B, C → O(n) time, O(1)/O(k) space.
"""))
A(code(r'''
from collections import deque

def moving_average(nums, k):
    # A) slicing based - readable
    if k <= 0:
        raise ValueError("window size must be positive")
    return [sum(nums[i:i + k]) / k for i in range(len(nums) - k + 1)]

def moving_average_running(nums, k):
    # B) running sum - O(n)
    if k <= 0:
        raise ValueError("window size must be positive")
    if len(nums) < k:
        return []
    window_sum = sum(nums[:k])                     # pehla window
    out = [window_sum / k]
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]        # naya andar, purana bahar (O(1))
        out.append(window_sum / k)
    return out

def moving_average_stream(k):
    # C) streaming: deque(maxlen=k) purana element khud girata hai
    window = deque(maxlen=k)
    def add(value):
        window.append(value)
        return sum(window) / len(window)           # shuru me window adhoori -> len(window)
    return add

def cumulative_average(nums):
    # bonus: running (expanding) average
    total, out = 0, []
    for i, x in enumerate(nums, start=1):
        total += x
        out.append(total / i)
    return out

data = [1, 2, 3, 4, 5, 6, 7]
print("k=3 slicing :", moving_average(data, 3))
print("k=3 running :", moving_average_running(data, 3))
print("k=1         :", moving_average(data, 1), "<- original hi")
print("k=len       :", moving_average(data, len(data)))
print("k > len     :", moving_average_running(data, 100))
print("cumulative  :", [round(x, 2) for x in cumulative_average(data)])

feed = moving_average_stream(3)
print("streaming   :", [round(feed(x), 2) for x in data], "<- shuru ke 2 partial windows")

try:
    moving_average(data, 0)
except ValueError as e:
    print("ValueError:", e)

# real use: temperature smoothing (noise kam karna)
temps = [30, 45, 31, 33, 47, 32, 34]
print("\nraw temps   :", temps)
print("smoothed(3) :", [round(x, 1) for x in moving_average_running(temps, 3)])

# ---- tests ----
assert moving_average([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]
assert moving_average_running([1, 2, 3, 4, 5], 3) == [2.0, 3.0, 4.0]
assert moving_average(data, 1) == [float(x) for x in data]
assert moving_average([1, 2], 5) == [] and moving_average_running([1, 2], 5) == []
assert moving_average([], 3) == []
assert moving_average_running([10, 20], 2) == [15.0]
assert moving_average(data, 3) == moving_average_running(data, 3)     # dono approaches barabar
assert cumulative_average([2, 4]) == [2.0, 3.0]
f = moving_average_stream(2)
assert (f(4), f(6), f(10)) == (4.0, 5.0, 8.0)
print("[pass] Problem 17")
'''))

A(md(r"""
## Problem 18 — Remove punctuation from a string

**Problem:** `"Hello, World!"` → `"Hello World"`.

**Approach A — `str.translate(str.maketrans("", "", string.punctuation))`:** **sabse tez** (C level,
ek pass). Ye standard jawab hai.

**Approach B — comprehension + `str.punctuation`/`isalnum()`:**
`"".join(ch for ch in s if ch not in string.punctuation)` — readable, magar per-char Python loop (slow).

**Approach C — `re.sub(r"[^\w\s]", "", s)`:** regex; Unicode ke sath flexible, magar setup cost.

**Zaroori:** `string.punctuation` sirf ASCII punctuation hai (`!"#$%&'()*+,-./...`). Unicode quotes
(`“ ” ’ …`), em-dash, aur emoji ismein **nahi** hain → `unicodedata.category(ch).startswith("P")` use karo.

**Complexity:** sab O(n); constants me translate sabse behtar.
"""))
A(code(r'''
import string, re, timeit, unicodedata

TRANS_TABLE = str.maketrans("", "", string.punctuation)      # ek hi baar bana kar reuse karo

def remove_punctuation(s):
    # A) translate - fastest
    return s.translate(TRANS_TABLE)

def remove_punctuation_comprehension(s):
    # B) readable comprehension
    return "".join(ch for ch in s if ch not in string.punctuation)

def remove_punctuation_regex(s):
    # C) regex: word chars aur whitespace ke ilawa sab hata do
    return re.sub(r"[^\w\s]", "", s)

def remove_punctuation_unicode(s):
    # Unicode-aware: category 'P*' = punctuation (smart quotes, em-dash sab)
    return "".join(ch for ch in s if not unicodedata.category(ch).startswith("P"))

def clean_for_search(s):
    # practical pipeline: punctuation hatao + lowercase + extra spaces collapse
    return " ".join(s.translate(TRANS_TABLE).lower().split())

text = "Hello, World! It's a test... (really?) -- 100% #python @ 5:30pm"
print("original  :", text)
print("translate :", remove_punctuation(text))
print("comprehen :", remove_punctuation_comprehension(text))
print("regex     :", remove_punctuation_regex(text))
print("search key:", clean_for_search("  Hello,   WORLD!!  "))
print("punctuation set:", string.punctuation)

unicode_text = "It’s a “smart” quote — really…"
print("\nunicode text        :", unicode_text)
print("ascii-only translate:", remove_punctuation(unicode_text), "<- smart quotes bach gaye")
print("unicode-aware       :", remove_punctuation_unicode(unicode_text), "<- sab saaf")

t_tr = timeit.timeit(lambda: remove_punctuation(text), number=3000)
t_cp = timeit.timeit(lambda: remove_punctuation_comprehension(text), number=3000)
t_re = timeit.timeit(lambda: remove_punctuation_regex(text), number=3000)
print(f"\ntranslate {t_tr*1000:6.1f} ms | comprehension {t_cp*1000:6.1f} ms | regex {t_re*1000:6.1f} ms")

# ---- tests ----
assert remove_punctuation("Hello, World!") == "Hello World"
assert remove_punctuation_comprehension("Hello, World!") == "Hello World"
assert remove_punctuation("") == ""
assert remove_punctuation("!!!") == ""
assert remove_punctuation("no punctuation here") == "no punctuation here"
assert remove_punctuation("a.b,c;d") == "abcd"
assert remove_punctuation(text) == remove_punctuation_comprehension(text)
assert remove_punctuation_regex("Hello, World!") == "Hello World"
assert clean_for_search("  Hello,   WORLD!!  ") == "hello world"
assert "’" not in remove_punctuation_unicode(unicode_text)
assert remove_punctuation("don't") == "dont"
print("[pass] Problem 18")
'''))

A(md("""
## Problem 19 — Count words in a sentence

**Problem:** sentence me kitne words hain? Aur har word kitni baar aaya?

**Approach:** `len(sentence.split())`. Bas. Magar **details** hi asli sawal hain:
- `split()` (no argument) → **kisi bhi** whitespace (space, tab, newline, multiple spaces) par tor deta hai
  aur khali strings nahi deta.
- `split(" ")` → **exactly** ek space par → `"a  b".split(" ")` = `['a', '', 'b']` (khali string!) ← classic bug
- Punctuation words se chipki hoti hai (`"cat,"` vs `"cat"`) → pehle clean karo
- Unique words → `set`, frequency → `Counter`
- Hyphenated words, apostrophes, aur Urdu/Unicode text ke liye rules define karna parta hai

**Complexity:** Time O(n), Space O(n).
"""))
A(code(r'''
import string
from collections import Counter

PUNCT_T = str.maketrans("", "", string.punctuation)

def count_words(sentence):
    # basic: whitespace par split (multiple spaces safe)
    return len(sentence.split())

def count_words_clean(sentence):
    # punctuation-safe count (words normalize kar ke)
    return len(sentence.translate(PUNCT_T).split())

def word_frequency(sentence):
    words = sentence.lower().translate(PUNCT_T).split()
    return Counter(words)

def sentence_stats(sentence):
    words = sentence.lower().translate(PUNCT_T).split()
    freq = Counter(words)
    return {
        "words": len(words),
        "unique": len(freq),
        "chars_no_space": len(sentence.replace(" ", "")),
        "sentences": sum(sentence.count(p) for p in ".!?") or 1,      # motay taur par
        "avg_word_len": round(sum(len(w) for w in words) / len(words), 2) if words else 0,
        "most_common": freq.most_common(1)[0] if freq else None,
    }

s = "The quick brown fox jumps over the lazy dog. The dog barks!"
print("count_words       :", count_words(s))
print("count_words_clean :", count_words_clean(s))
print("frequency         :", dict(word_frequency(s)))
print("stats             :", sentence_stats(s))

# split() vs split(" ") ka farq (yahan log phaste hain)
messy = "a  b   c"
print("\nsplit()    :", messy.split(), "-> count", len(messy.split()))
print('split(" ") :', messy.split(" "), "-> count", len(messy.split(" ")), " <- khali strings!")
print("tabs/newlines:", "a\tb\nc".split())
print("khali string :", "".split(), "-> count", len("".split()))
print("sirf spaces  :", "     ".split(), "-> count", len("     ".split()))

# maxsplit argument (log parsing me kaam aata hai)
log_line = "2026-07-28 ERROR database connection failed"
date, level, rest = log_line.split(" ", 2)                    # sirf 2 splits
print("\nmaxsplit=2  :", (date, level, rest))
print("rsplit      :", "a.b.c.txt".rsplit(".", 1), "<- extension nikalne ka idiom")

# ---- tests ----
assert count_words("Hello world") == 2
assert count_words("  extra   spaces   here  ") == 3          # split() ne sambhal liya
assert count_words("") == 0 and count_words("     ") == 0
assert count_words("one") == 1
assert count_words("a\tb\nc") == 3                            # tabs/newlines bhi whitespace
assert len("a  b".split(" ")) == 3                            # gotcha ka proof
assert count_words_clean("Hello, world!") == 2
assert word_frequency("The the THE")["the"] == 3              # case-insensitive
assert word_frequency("a b a")["a"] == 2
assert sentence_stats(s)["unique"] < sentence_stats(s)["words"]
assert sentence_stats("")["words"] == 0
print("[pass] Problem 19")
'''))

A(md("""
## Problem 20 — Validate an IP address

**Problem:** string valid **IPv4** hai ya nahi? `"192.168.1.1"` → `True`, `"256.1.1.1"` → `False`.

**Rules (jo interviewer test karta hai):**
1. Exactly **4** parts, `.` se separated
2. Har part sirf **digits** (`"1e2"`, `"-1"`, `" 1"`, `"+1"` sab invalid)
3. Value **0..255**
4. **Leading zeros** allowed nahi (`"01"` invalid, `"0"` valid) — ye sabse zyada bhoola jane wala rule hai
5. Khali part invalid (`"1..1.1"`)

**Approach:** `split(".")`, length check, phir har part par digit + range + leading-zero check.
`str.isdigit()` use karo (`int()` + try/except bhi chalta hai magar `"１２３"` jaise Unicode digits
`isdigit()` ko dhoka de sakte hain → `isascii()` bhi check karo).

**Bonus:** `ipaddress` module (stdlib) production me use karo: `ipaddress.ip_address(s)` — magar
dhyan rahe wo `"1.1.1.01"` ko Python 3.9+ me reject karta hai aur IPv6 bhi accept karta hai.

**Complexity:** Time O(1) (max 15 chars), Space O(1).
"""))
A(code(r'''
import ipaddress

def is_valid_ipv4(s):
    parts = s.split(".")
    if len(parts) != 4:                            # rule 1
        return False
    for p in parts:
        if not p or not p.isdigit() or not p.isascii():   # rule 2 + khali part (rule 5)
            return False
        if len(p) > 1 and p[0] == "0":             # rule 4: leading zero
            return False
        if not 0 <= int(p) <= 255:                 # rule 3: range
            return False
    return True

def is_valid_ipv4_stdlib(s):
    # production tareeqa - khud parsing likhne ki zaroorat nahi
    try:
        return isinstance(ipaddress.ip_address(s), ipaddress.IPv4Address)
    except ValueError:
        return False

def ip_kind(s):
    # IPv4 / IPv6 / invalid - ipaddress dono sambhalta hai
    try:
        return f"IPv{ipaddress.ip_address(s).version}"
    except ValueError:
        return "invalid"

cases = [
    "192.168.1.1", "0.0.0.0", "255.255.255.255", "127.0.0.1",
    "256.1.1.1", "1.1.1", "1.1.1.1.1", "01.1.1.1", "1.-1.1.1",
    "", "1..1.1", "192.168.1.a", " 1.1.1.1", "1.1.1.1 ", "1e2.1.1.1",
]
print(f"{'input':<18}{'mine':>7}{'stdlib':>9}   note")
print("-" * 55)
notes = {
    "01.1.1.1": "leading zero",
    "256.1.1.1": "range > 255",
    "1.1.1": "parts < 4",
    " 1.1.1.1": "space",
    "1e2.1.1.1": "non-digit",
    "1..1.1": "khali part",
}
for c in cases:
    print(f"{c!r:<18}{str(is_valid_ipv4(c)):>7}{str(is_valid_ipv4_stdlib(c)):>9}   {notes.get(c, '')}")

print("\nip_kind checks:", ip_kind("10.0.0.1"), "|", ip_kind("::1"), "|", ip_kind("hello"))
print("Unicode digit trap: '１.1.1.1'.isdigit() ->", "１".isdigit(),
      "| isascii() ->", "１".isascii(), "-> is liye dono check kiye")

# ---- tests ----
assert is_valid_ipv4("192.168.1.1") is True
assert is_valid_ipv4("0.0.0.0") is True
assert is_valid_ipv4("255.255.255.255") is True
assert is_valid_ipv4("256.255.255.255") is False              # range
assert is_valid_ipv4("1.1.1") is False                        # parts
assert is_valid_ipv4("1.1.1.1.1") is False
assert is_valid_ipv4("01.1.1.1") is False                     # leading zero
assert is_valid_ipv4("1.1.1.01") is False
assert is_valid_ipv4("") is False and is_valid_ipv4("...") is False
assert is_valid_ipv4("1..1.1") is False                       # khali part
assert is_valid_ipv4(" 1.1.1.1") is False and is_valid_ipv4("1.1.1.1 ") is False
assert is_valid_ipv4("1.1.1.-1") is False
assert is_valid_ipv4("１.1.1.1") is False                 # Unicode digit
assert is_valid_ipv4_stdlib("192.168.1.1") is True and is_valid_ipv4_stdlib("::1") is False
assert ip_kind("::1") == "IPv6" and ip_kind("1.2.3.4") == "IPv4"
print("[pass] Problem 20  --  saare 20 problems mukammal!")
'''))

# ================================================================ LeetCode
A(md("""
---
# Part 9 — LeetCode Problems

Ye section Part 8 se **alag** hai: yahan LeetCode ki **exact problem signatures**, brute-force vs optimal
comparison, aur complexity analysis par focus hai. (Function names jaan boojh kar `_lc` / alag rakhe gaye hain
taake Part 8 wale functions par asar na ho.)

### LC 49. Group Anagrams — Medium
🔗 https://leetcode.com/problems/group-anagrams/

**Bayan:** strings ki array di gayi hai; anagrams ko ek sath group kar do. Output groups kis order me hon,
farq nahi parta.

**Approach (step by step):**
1. Anagrams ka koi bhi **canonical key** ek hi hona chahiye. Do options:
   - **Brute/simple:** `"".join(sorted(word))` → `"eat"`, `"tea"`, `"ate"` sab ka key `"aet"`. Per word O(k log k).
   - **Optimal:** 26-size count array ko `tuple` bana kar key (`tuple` hashable hai, `list` nahi). Per word O(k).
2. `defaultdict(list)` me key ke against words append karte jao.
3. `list(groups.values())` return karo.

**Brute force (real brute):** har word ka har doosre word se comparison → O(n² · k log k) → bara input par TLE.

**Complexity:**
- Sorted-key: **Time O(n · k log k)**, **Space O(n · k)**
- Count-key: **Time O(n · k)** (26 constant), **Space O(n · k)**
(n = words ki tadaad, k = sabse lambe word ki length)
"""))
A(code(r'''
from collections import defaultdict

def group_anagrams_brute(strs):
    # O(n^2 * k log k): har word ko maujooda groups se compare karo (LeetCode par TLE)
    groups = []
    for w in strs:
        placed = False
        for g in groups:
            if sorted(g[0]) == sorted(w):          # kisi group ke representative se match?
                g.append(w)
                placed = True
                break
        if not placed:
            groups.append([w])                     # naya group
    return groups

def group_anagrams_lc(strs):
    # OPTIMAL: 26-length count tuple key -> O(n*k)
    groups = defaultdict(list)
    for w in strs:
        counts = [0] * 26                          # sirf lowercase a-z (LeetCode constraint)
        for ch in w:
            counts[ord(ch) - ord("a")] += 1
        groups[tuple(counts)].append(w)            # tuple hashable -> dict key ban sakti hai
    return list(groups.values())

def group_anagrams_sortkey(strs):
    # sorted-key version: chhota code, thora slow (O(n*k log k)) - interview me pehle ye batao
    groups = defaultdict(list)
    for w in strs:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())

def norm(groups):
    return sorted(sorted(g) for g in groups)       # comparison ke liye deterministic shape

words = ["eat", "tea", "tan", "ate", "nat", "bat"]
print("brute    :", group_anagrams_brute(words))
print("optimal  :", group_anagrams_lc(words))
print("sort-key :", group_anagrams_sortkey(words))

# ---- LeetCode ke official test cases ----
assert norm(group_anagrams_lc(["eat", "tea", "tan", "ate", "nat", "bat"])) == \
       [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
assert group_anagrams_lc([""]) == [[""]]
assert group_anagrams_lc(["a"]) == [["a"]]
assert group_anagrams_lc([]) == []
assert norm(group_anagrams_brute(words)) == norm(group_anagrams_lc(words)) == norm(group_anagrams_sortkey(words))
assert len(group_anagrams_lc(["abc", "bca", "cab", "xyz"])) == 2
assert len(group_anagrams_lc(["ab", "ba", "abb"])) == 2       # counts different -> alag group
print("[pass] LC 49 Group Anagrams")
'''))

A(md("""
### LC 3. Longest Substring Without Repeating Characters — Medium
🔗 https://leetcode.com/problems/longest-substring-without-repeating-characters/

**Bayan:** string `s` me sabse lambi **substring** (contiguous) ki length batao jisme koi character
repeat na ho. `"abcabcbb"` → `3` (`"abc"`).

**Approach (sliding window + hash map):**
1. Do pointers: `start` (window ka bayan kinara) aur `i` (dayan kinara, loop variable).
2. `last` dict me har character ka **last seen index** rakho.
3. Jab current char window ke andar dobara mile (`last[ch] >= start`) to `start = last[ch] + 1`
   → window ko utna aage khiskao ke duplicate bahar ho jaye.
4. Har step par `best = max(best, i - start + 1)`.

**Kyun `>= start` ki shart?** Kyunki dict me purane (window se bahar wale) indexes bhi pare rehte hain —
unko ignore karna zaroori hai warna `start` peeche chala jayega (classic bug).

**Brute force:** saari substrings check karo (`set` se uniqueness) → **O(n³)** / optimized O(n²).
**Optimal:** har character exactly ek baar andar, ek baar bahar → **O(n)**.

**Complexity:** Brute O(n²)–O(n³) time; Optimal **Time O(n)**, **Space O(min(n, charset))**.
"""))
A(code(r'''
def length_of_longest_substring_brute(s):
    # O(n^2): har start se aage barho jab tak duplicate na aaye
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break                              # duplicate -> ye window khatam
            seen.add(s[j])
        best = max(best, len(seen))
    return best

def length_of_longest_substring(s):
    # OPTIMAL: sliding window + last-seen index map -> O(n)
    last = {}                                      # char -> last index dekha gaya
    start = best = 0
    for i, ch in enumerate(s):
        # sirf tab jump karo jab duplicate CURRENT window ke andar ho
        if (prev := last.get(ch, -1)) >= start:
            start = prev + 1                       # window ka left kinara duplicate ke baad
        last[ch] = i                               # update (hamesha)
        best = max(best, i - start + 1)            # window ki current length
    return best

def longest_substring_text(s):
    # bonus: sirf length nahi, asli substring bhi (debug/teaching ke liye)
    last, start, best, best_start = {}, 0, 0, 0
    for i, ch in enumerate(s):
        if (prev := last.get(ch, -1)) >= start:
            start = prev + 1
        last[ch] = i
        if i - start + 1 > best:
            best, best_start = i - start + 1, start
    return s[best_start:best_start + best]

for s in ("abcabcbb", "bbbbb", "pwwkew", "", "au", "dvdf", "tmmzuxt", "abcdefg"):
    print(f"  {s!r:<12} brute={length_of_longest_substring_brute(s)} "
          f"optimal={length_of_longest_substring(s)}  substring={longest_substring_text(s)!r}")

# "dvdf" wo case hai jahan galat implementation 3 ki jagah 2 deti hai (start peeche chala jata hai)
print("\ntricky 'dvdf'  ->", length_of_longest_substring("dvdf"), "(expected 3: 'vdf')")
print("tricky 'tmmzuxt' ->", length_of_longest_substring("tmmzuxt"), "(expected 5: 'mzuxt')")

# ---- LeetCode ke official test cases ----
assert length_of_longest_substring("abcabcbb") == 3
assert length_of_longest_substring("bbbbb") == 1
assert length_of_longest_substring("pwwkew") == 3
assert length_of_longest_substring("") == 0
assert length_of_longest_substring(" ") == 1
assert length_of_longest_substring("au") == 2
assert length_of_longest_substring("dvdf") == 3                # window ka classic trap
assert length_of_longest_substring("tmmzuxt") == 5
assert length_of_longest_substring("abcdefg") == 7             # sab unique
assert longest_substring_text("pwwkew") == "wke"
# brute aur optimal har random-ish input par barabar hone chahiye
import random
random.seed(42)
for _ in range(60):
    t = "".join(random.choice("abcd") for _ in range(random.randint(0, 12)))
    assert length_of_longest_substring_brute(t) == length_of_longest_substring(t), t
print("[pass] LC 3 Longest Substring Without Repeating Characters (60 random tests bhi pass)")
'''))

A(md("""
### LC 13. Roman to Integer — Easy
🔗 https://leetcode.com/problems/roman-to-integer/

**Bayan:** roman numeral string ko integer me badlo. Range 1..3999. Input **valid** hoti hai.

**Approach (left-to-right, sabse chhota):** har symbol par dekho — agar iska value **agle** symbol se
chhota hai to **minus** karo, warna **plus**. `IV` → `-1 + 5 = 4`.
(Ya right-to-left scan — Part 8 Problem 11 me wo version hai.)

**Complexity:** **Time O(n)** (n ≤ 15), **Space O(1)**.

---

### LC 12. Integer to Roman — Medium
🔗 https://leetcode.com/problems/integer-to-roman/

**Bayan:** integer (1..3999) ko roman numeral me badlo.

**Approach (greedy + subtractive table):**
1. Value→symbol table **descending** order me banao aur ismein 6 subtractive pairs
   (`900:"CM"`, `400:"CD"`, `90:"XC"`, `40:"XL"`, `9:"IX"`, `4:"IV"`) **shamil** kar do.
2. Har value par `divmod(num, value)` → jitni baar fit hota hai utni baar symbol likho, remainder le kar aage barho.
3. Greedy yahan **provably correct** hai kyunki table me har "gap" ke liye symbol maujood hai.

**Kyun `divmod`?** `while num >= value: ...` bhi chalta hai, magar `divmod` ek hi step me count + remainder
deta hai (Pythonic + tez).

**Complexity:** **Time O(1)** (max 13 iterations, output ≤ 15 chars), **Space O(1)**.
"""))
A(code(r'''
# ================= LC 13. Roman to Integer =================
VALUES_LC = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

def roman_to_int_lc(s):
    total = 0
    for i, ch in enumerate(s):
        val = VALUES_LC[ch]
        # agla symbol bara hai? -> ye subtractive pair ka hissa hai
        if i + 1 < len(s) and val < VALUES_LC[s[i + 1]]:
            total -= val
        else:
            total += val
    return total

def roman_to_int_pairs(s):
    # alternative: pehle 2-char pairs handle karo (kuch log ye version pasand karte hain)
    two = {"IV": 4, "IX": 9, "XL": 40, "XC": 90, "CD": 400, "CM": 900}
    total, i = 0, 0
    while i < len(s):
        if s[i:i + 2] in two:                      # slicing out-of-range safe hai
            total += two[s[i:i + 2]]
            i += 2
        else:
            total += VALUES_LC[s[i]]
            i += 1
    return total

# ================= LC 12. Integer to Roman =================
ROMAN_TABLE_LC = (
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
)

def int_to_roman_lc(num):
    out = []
    for value, symbol in ROMAN_TABLE_LC:           # descending order = greedy
        if num == 0:
            break
        count, num = divmod(num, value)            # kitni baar + remainder
        if count:
            out.append(symbol * count)
    return "".join(out)

print("LC13: 'III' ->", roman_to_int_lc("III"), "| 'LVIII' ->", roman_to_int_lc("LVIII"),
      "| 'MCMXCIV' ->", roman_to_int_lc("MCMXCIV"))
print("LC12: 3 ->", int_to_roman_lc(3), "| 58 ->", int_to_roman_lc(58), "| 1994 ->", int_to_roman_lc(1994))
print("\n  num   roman            back")
for n in (1, 4, 9, 14, 40, 90, 400, 1994, 3888, 3999):
    r = int_to_roman_lc(n)
    print(f"  {n:>4}  {r:<16} {roman_to_int_lc(r)}")

# ---- LC 13 tests ----
assert roman_to_int_lc("III") == 3
assert roman_to_int_lc("IV") == 4
assert roman_to_int_lc("IX") == 9
assert roman_to_int_lc("LVIII") == 58
assert roman_to_int_lc("MCMXCIV") == 1994
assert roman_to_int_lc("I") == 1 and roman_to_int_lc("MMMCMXCIX") == 3999
assert roman_to_int_pairs("MCMXCIV") == 1994

# ---- LC 12 tests ----
assert int_to_roman_lc(3) == "III"
assert int_to_roman_lc(4) == "IV"
assert int_to_roman_lc(9) == "IX"
assert int_to_roman_lc(58) == "LVIII"
assert int_to_roman_lc(1994) == "MCMXCIV"
assert int_to_roman_lc(3999) == "MMMCMXCIX"
assert int_to_roman_lc(1) == "I" and int_to_roman_lc(2024) == "MMXXIV"

# ---- dono milkar: full range round-trip + Part 8 wale versions se cross-check ----
assert all(roman_to_int_lc(int_to_roman_lc(n)) == n for n in range(1, 4000))
assert all(int_to_roman_lc(n) == int_to_roman_basic(n) for n in range(1, 4000))
assert all(roman_to_int_lc(int_to_roman_lc(n)) == roman_to_int_basic(int_to_roman_lc(n))
           for n in range(1, 4000, 7))
print("[pass] LC 13 + LC 12 (1..3999 round-trip verified)")
'''))

A(md("""
### LC 48. Rotate Image — Medium
🔗 https://leetcode.com/problems/rotate-image/

**Bayan:** `n x n` matrix ko **in-place** 90° clockwise rotate karo — nayi matrix allocate **nahi** karni
(`O(1)` extra memory). Function ko kuch return karne ki zaroorat nahi, matrix khud badalni hai.

**Approach (transpose + reverse each row):**
1. **Transpose:** `matrix[i][j]` ↔ `matrix[j][i]` swap karo — magar sirf **upper triangle** par
   (`j` `i+1` se shuru), warna har pair do baar swap ho kar wapas apni jagah aa jayega.
2. **Har row reverse:** `row.reverse()` (ya `matrix[i][:] = matrix[i][::-1]` — dhyan do, `matrix[i] = ...`
   nahi likhna kyunki wo in-place nahi rehta agar caller ne rows ka reference rakha ho).

Kyun ye kaam karta hai: transpose se `(r,c)` → `(c,r)`, phir row reverse se `(c,r)` → `(c, n-1-r)` —
aur clockwise rotation ka formula bhi yahi hai.

**Counter-clockwise:** transpose + **columns** reverse (`matrix.reverse()` pehle karo, phir transpose).

**Complexity:** **Time O(n²)** (har cell ek baar), **Space O(1)** extra.
"""))
A(code(r'''
def rotate_image_inplace(matrix):
    # LeetCode signature: matrix ko jagah par (in-place) modify karo
    n = len(matrix)

    # step 1: transpose (sirf upper triangle - warna double swap)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]   # tuple swap

    # step 2: har row ko ulta karo
    for row in matrix:
        row.reverse()                              # in-place reverse (naya object nahi banta)
    return matrix                                  # sirf convenience ke liye (LeetCode void chahta hai)

def rotate_image_inplace_ccw(matrix):
    # counter-clockwise: pehle rows ka order ulta, phir transpose
    matrix.reverse()
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    return matrix

def rotate_image_layers(matrix):
    # alternative: 4-way cycle swap (ek hi pass, "layer by layer")
    n = len(matrix)
    for layer in range(n // 2):
        last = n - 1 - layer
        for i in range(layer, last):
            offset = i - layer
            top = matrix[layer][i]                                  # top bacha lo
            matrix[layer][i] = matrix[last - offset][layer]          # left -> top
            matrix[last - offset][layer] = matrix[last][last - offset]  # bottom -> left
            matrix[last][last - offset] = matrix[i][last]            # right -> bottom
            matrix[i][last] = top                                   # top -> right
    return matrix

m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rows_before = [id(r) for r in m]                   # in-place proof: row objects wahi rehne chahiye
print("before :", m)
rotate_image_inplace(m)
print("after  :", m)
print("same row objects (in-place)?", [id(r) for r in m] == rows_before)

m4 = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
print("\n4x4 before:", m4)
print("4x4 after :", rotate_image_inplace([r[:] for r in m4]))
print("layers ver:", rotate_image_layers([r[:] for r in m4]))
print("ccw       :", rotate_image_inplace_ccw([r[:] for r in [[1, 2], [3, 4]]]))

# ---- LeetCode ke official test cases ----
a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotate_image_inplace(a)
assert a == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]

b = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]
rotate_image_inplace(b)
assert b == [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]

c = [[1]]
rotate_image_inplace(c)
assert c == [[1]]

d = [[1, 2], [3, 4]]
rotate_image_inplace(d)
assert d == [[3, 1], [4, 2]]

# layers version aur transpose version ka same natija
assert rotate_image_layers([r[:] for r in m4]) == rotate_image_inplace([r[:] for r in m4])
# 4 rotations = identity
e = [r[:] for r in m4]
for _ in range(4):
    rotate_image_inplace(e)
assert e == m4
# Part 8 ke non-in-place version se cross-check
assert rotate_image_inplace([r[:] for r in m4]) == rotate_90(m4)
print("[pass] LC 48 Rotate Image")
'''))

A(md("""
### LC 54. Spiral Matrix — Medium
🔗 https://leetcode.com/problems/spiral-matrix/

**Bayan:** `m x n` matrix ke saare elements **spiral order** (clockwise, bahar se andar) me ek list me do.
Matrix square hona zaroori **nahi**.

**Approach (four boundaries):**
1. `top, bottom, left, right` maintain karo.
2. Har loop me 4 traversals: → (top row), ↓ (right col), ← (bottom row), ↑ (left col).
3. Har traversal ke baad us boundary ko andar khiskao.
4. **Sabse ahem:** ← aur ↑ karne se pehle `if top <= bottom` / `if left <= right` check karo.
   Warna jab sirf ek row (ya ek column) bache to elements **do baar** aa jayenge — LeetCode par
   `[[1,2,3]]` ya `[[1],[2],[3]]` wale test cases yehi pakarte hain.

**Alternative (bohat Pythonic, "peel + rotate"):**
```python
out = []
while matrix:
    out += matrix.pop(0)                       # pehli row utha lo
    matrix = [list(r) for r in zip(*matrix)][::-1]   # baqi ko CCW rotate karo
```
Time same O(m·n) magar zip se rotation ki wajah se extra memory lagti hai.

**Complexity:** **Time O(m·n)** (har cell exactly ek baar), **Space O(1)** extra (output ke ilawa).
"""))
A(code(r'''
def spiral_matrix_lc(matrix):
    if not matrix or not matrix[0]:
        return []
    out = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for c in range(left, right + 1):           # -> top row
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):           # v right column
            out.append(matrix[r][right])
        right -= 1
        if top <= bottom:                          # <- bottom row (guard!)
            for c in range(right, left - 1, -1):
                out.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:                          # ^ left column (guard!)
            for r in range(bottom, top - 1, -1):
                out.append(matrix[r][left])
            left += 1
    return out

def spiral_matrix_peel(matrix):
    # Pythonic version: peel first row + rotate rest counter-clockwise
    rows = [list(r) for r in matrix if r]          # copy + khali rows drop
    out = []
    while rows:
        out += rows.pop(0)
        rows = [list(r) for r in zip(*rows)][::-1]
    return out

def spiral_matrix_direction(matrix):
    # teesra tareeqa: direction vectors + visited set (grid problems ka general pattern)
    if not matrix or not matrix[0]:
        return []
    rows, cols = len(matrix), len(matrix[0])
    seen = [[False] * cols for _ in range(rows)]
    dr, dc = (0, 1, 0, -1), (1, 0, -1, 0)          # right, down, left, up
    r = c = d = 0
    out = []
    for _ in range(rows * cols):
        out.append(matrix[r][c])
        seen[r][c] = True
        nr, nc = r + dr[d], c + dc[d]
        if not (0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc]):
            d = (d + 1) % 4                        # deewar mili -> mur jao
            nr, nc = r + dr[d], c + dc[d]
        r, c = nr, nc
    return out

grid3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
grid34 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
print("3x3       :", spiral_matrix_lc(grid3))
print("3x4       :", spiral_matrix_lc(grid34))
print("peel      :", spiral_matrix_peel(grid34))
print("direction :", spiral_matrix_direction(grid34))
print("1 row     :", spiral_matrix_lc([[1, 2, 3]]))
print("1 col     :", spiral_matrix_lc([[1], [2], [3]]))
print("input safe:", grid34[0])

# ---- LeetCode ke official test cases ----
assert spiral_matrix_lc([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
assert spiral_matrix_lc([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]) == [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
assert spiral_matrix_lc([[1]]) == [1]
assert spiral_matrix_lc([[1, 2, 3]]) == [1, 2, 3]              # single row guard
assert spiral_matrix_lc([[1], [2], [3]]) == [1, 2, 3]          # single column guard
assert spiral_matrix_lc([[1, 2], [3, 4]]) == [1, 2, 4, 3]
assert spiral_matrix_lc([]) == [] and spiral_matrix_lc([[]]) == []
# teeno approaches ek jaisa jawab dein
for g in (grid3, grid34, [[1]], [[1, 2, 3]], [[1], [2], [3]], [[1, 2], [3, 4]]):
    assert spiral_matrix_lc(g) == spiral_matrix_peel(g) == spiral_matrix_direction(g), g
# koi cell miss/duplicate na ho
assert sorted(spiral_matrix_lc(grid34)) == sorted(x for row in grid34 for x in row)
# Part 8 wale version se cross-check
assert spiral_matrix_lc(grid34) == spiral_print(grid34)
print("[pass] LC 54 Spiral Matrix")
'''))

A(md("""
### LC 443. String Compression — Medium
🔗 https://leetcode.com/problems/string-compression/

**Bayan:** characters ki **list** `chars` di gayi hai. Isko **in-place** compress karo: har group of
consecutive repeating characters ke liye character likho, aur agar group ki length `> 1` ho to uske baad
length ke **digits** (har digit alag cell me!) likho. Nayi length return karo.
`["a","a","b","b","c","c","c"]` → `["a","2","b","2","c","3"]`, return `6`.

**Approach (two pointers: `read` aur `write`):**
1. `read` se group ki shuruaat pakro, aage barho jab tak same character mile → `count` mil gaya.
2. `chars[write] = character` likho, `write += 1`.
3. Agar `count > 1` → `str(count)` ke **har digit** ko alag cell me likho
   (`count = 12` → `"1"`, `"2"` — ye sabse zyada bhoola jane wala rule hai).
4. Aakhir me `write` return karo (yehi nayi length hai; aage ka kachra ignore hota hai).

**Kyun `write` hamesha `read` se peeche rehta hai?** Kyunki group ki length `L` ke liye hum
`1 + len(str(L))` cells likhte hain, jo `L` se kabhi bara nahi hota (`L=1` → 1 cell, `L=2` → 2 cells,
`L≥3` → chhota) — is liye overwrite safe hai. Interviewer ye "why is it safe?" zaroor poochta hai.

**Complexity:** **Time O(n)**, **Space O(1)** extra.
"""))
A(code(r'''
def compress_chars(chars):
    # in-place, two pointers
    write = read = 0
    n = len(chars)
    while read < n:
        ch = chars[read]
        count = 0
        while read < n and chars[read] == ch:      # poora group naap lo
            read += 1
            count += 1
        chars[write] = ch                          # character likho
        write += 1
        if count > 1:
            for digit in str(count):               # har DIGIT alag cell me
                chars[write] = digit
                write += 1
    del chars[write:]                              # (bonus) kachra hatao - LeetCode isko ignore karta hai
    return write

def compress_chars_groupby(chars):
    # readable version (in-place nahi, comparison ke liye)
    from itertools import groupby
    out = []
    for ch, grp in groupby(chars):
        count = sum(1 for _ in grp)
        out.append(ch)
        if count > 1:
            out.extend(str(count))                 # extend -> digits alag alag
    return out

def compressed_string(s):
    # string version (RLE se milta julta, magar count 1 skip)
    from itertools import groupby
    return "".join(ch if (n := sum(1 for _ in g)) == 1 else f"{ch}{n}" for ch, g in groupby(s))

demo = list("aabbccc")
length = compress_chars(demo)
print("aabbccc ->", demo, "length:", length)

demo2 = list("abbbbbbbbbbbb")                      # 12 b's -> multi-digit
length2 = compress_chars(demo2)
print("a + 12 b ->", demo2, "length:", length2, "<- '1','2' alag cells me")

print("single   :", (lambda c: (compress_chars(c), c))(list("a")))
print("no repeat:", (lambda c: (compress_chars(c), c))(list("abc")))
print("groupby  :", compress_chars_groupby(list("aabbccc")))
print("string ver:", compressed_string("aabbccc"), "|", compressed_string("abc"))

# ---- LeetCode ke official test cases ----
c1 = ["a", "a", "b", "b", "c", "c", "c"]
assert compress_chars(c1) == 6 and c1[:6] == ["a", "2", "b", "2", "c", "3"]

c2 = ["a"]
assert compress_chars(c2) == 1 and c2[:1] == ["a"]

c3 = ["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]
assert compress_chars(c3) == 4 and c3[:4] == ["a", "b", "1", "2"]      # multi-digit count

c4 = []
assert compress_chars(c4) == 0

c5 = ["a", "a", "a", "b"]
assert compress_chars(c5) == 3 and c5[:3] == ["a", "3", "b"]

# groupby version se cross-check
for text in ("aabbccc", "a", "abc", "abbbbbbbbbbbb", "", "aaaaaaaaaa"):
    expected = compress_chars_groupby(list(text))
    got = list(text)
    assert compress_chars(got) == len(expected) and got[:len(expected)] == expected, text
print("[pass] LC 443 String Compression")
'''))

# ================================================================ Q&A
A(md("""
---
# Part 10 — Interview Questions & Answers

**Q1. `enumerate()` `range(len())` se behtar kyun hai?**
Index aur value ek sath milte hain, indexing bug ka chance khatam, kisi bhi iterable par chalta hai
(generator par bhi jahan `len()` fail hota hai), aur `start=` se 1-based numbering free milti hai.

**Q2. List comprehension aur generator expression me farq?**
List comprehension foran poori list banati hai (memory O(n), dobara use ho sakti hai, `len()` chalta hai).
Genexp lazy hai (memory O(1), **ek baar** exhaust hone ke baad khatam, `len()` nahi). Bare data ya
`sum()/any()/all()/max()` jaise consumers ke liye genexp behtar.

**Q3. `sorted()` aur `list.sort()` me farq?**
`sorted()` nayi list return karta hai aur kisi bhi iterable par chalta hai; `list.sort()` in-place hai aur
**`None`** return karta hai (`x = x.sort()` classic bug). `sort()` thora zyada memory-efficient hai.

**Q4. Python ka sort stable hai? Iska faida?**
Haan — Timsort stable hai (barabar keys wale elements ka original order mehfooz). Faida: **multi-pass sorting** —
pehle secondary key par sort karo, phir primary par → mixed asc/desc directions bhi ho jati hain
(jahan `-value` negate mumkin nahi, jaise strings par).

**Q5. Multi-key sorting kaise? Ek key asc aur doosri desc chahiye to?**
Tuple key: `key=lambda r: (r.a, r.b)`. Mixed direction ke liye (a) numeric key negate karo
`(-r.score, r.name)`, ya (b) two-pass stable sort: pehle `name` (asc), phir `score` (`reverse=True`).

**Q6. `key=` aur `cmp` (comparator) me farq? `cmp_to_key` kab?**
Python 3 me `cmp` khatam. `key` har element par **ek baar** chalta hai (fast, O(n) key calls).
Jab decision **pairwise** ho aur single key na ban sake (jaise "largest concatenated number") tab
`functools.cmp_to_key(cmp)` use karo — slow hai (har comparison par Python call).

**Q7. Shallow copy aur deep copy me farq? `list(a)`, `a[:]`, `a.copy()` kaun sa hai?**
Teeno **shallow** hain — sirf outer container naya, andar wale objects shared. `copy.deepcopy()` recursively
sab kuch naya banata hai (aur cycles bhi sambhalta hai memo dict se). Nested data me shallow copy modify
karna original ko bhi badal deta hai.

**Q8. `is` aur `==` me farq?**
`==` value equality (`__eq__`), `is` identity (same object, same `id()`). `is` sirf `None`/`True`/`False`/
sentinels ke liye. Chhote ints (-5..256) aur interned strings CPython cache karta hai — is par logic
banana galti hai.

**Q9. Mutable default argument ka masla kya hai?**
Default value function **define** hote waqt ek hi baar banti hai (`func.__defaults__` me rehti hai) —
saari calls wahi object share karti hain. Fix: `def f(x=None): x = [] if x is None else x`.

**Q10. EAFP vs LBYL?**
LBYL = pehle check (`if key in d`), EAFP = seedha try karo aur exception handle karo. Python EAFP prefer
karta hai: race conditions nahi, happy path fast (try ka cost ~0 jab exception na aaye), ek lookup.
Jab exception "normal" aur frequent ho, tab `if` sasta ho sakta hai.

**Q11. `str` immutable hai — loop me `+=` kyun bura hai?**
Har `+=` naya string object banata hai aur purana content copy karta hai → O(n²). `list` me pieces jama
kar ke `"".join(parts)` karo → ek allocation, O(n). (CPython ka refcount-1 optimization par bharosa na karo.)

**Q12. `zip()` ka silent-truncation masla aur uska hal?**
`zip` sabse chhoti sequence par ruk jata hai → data chupke se gayab. `strict=True` (3.10+) mismatch par
`ValueError` deta hai; `itertools.zip_longest(fillvalue=...)` sabse lambi tak chalta hai.

**Q13. `defaultdict` aur `dict.setdefault()` me kya farq?**
`setdefault(k, default)` har call par default **banata** hai (chahe key mojood ho) aur plain dict par chalta hai.
`defaultdict(factory)` missing key par factory call karta hai — lekin missing key ko sirf **padhne** se bhi
wo key create ho jati hai (dict grow karti hai). Sirf reading ke liye `.get()` behtar.

**Q14. Walrus operator `:=` kab use karna chahiye aur kab nahi?**
Jab ek hi value compute kar ke usko test aur baad me use dono karna ho (`if (n := len(x)) > 10`),
`while (chunk := f.read(n))`, ya comprehension me duplicate computation bachani ho. Na karo jab readability
kharab ho ya sirf line chhoti karni ho.

**Q15. `any()`/`all()` ka short-circuit behaviour aur khali iterable par kya?**
`any` pehla `True` milne par ruk jata hai, `all` pehla `False` par. `any([]) == False`,
`all([]) == True` (vacuous truth). Generator ke sath use karo taake poori list na bane.

**Q16. Late binding closure ka bug kya hai?**
`[lambda: i for i in range(3)]` sab `2` dete hain kyunki lambda `i` ko **call time** par padhta hai.
Fix: default argument se value capture karo (`lambda i=i: i`) ya `functools.partial(f, i)`.

**Q17. `zip(*matrix)` kaise transpose karta hai?**
`*matrix` rows ko separate positional arguments bana deta hai, phir `zip` unka i-th element jor kar tuple
banata hai — yani columns. `[list(c) for c in zip(*m)]` = transpose. Jagged rows par `zip` truncate karta hai
→ `zip_longest` use karo.

**Q18. `*args`/`**kwargs` aur keyword-only arguments?**
`*args` extra positional (tuple), `**kwargs` extra keyword (dict). Signature me `*` ke baad ke parameters
**keyword-only** ho jate hain (`def f(a, *, verbose=False)`), aur `/` se pehle wale **positional-only**.
Keyword-only args API ko self-documenting aur future-proof banate hain.

**Q19. Comprehension ke andar variable leak hota hai?**
Python 3 me nahi — comprehension ka apna scope hota hai (Python 2 me list comp leak karti thi).
Isi wajah se comprehension ke andar walrus se assign kiya gaya variable... **leak karta hai** (jaan boojh kar
design kiya gaya hai) — ye ek accha trivia sawal hai.

**Q20. `dict` ko value se sort kar ke wapas `dict` kaise banaoge?**
`dict(sorted(d.items(), key=itemgetter(1), reverse=True))` — Python 3.7+ me dict insertion order
preserve karti hai. Sirf top-k chahiye to `Counter(d).most_common(k)` ya `heapq.nlargest(k, ...)` (O(n log k)).
"""))

# ================================================================ practice
A(md("""
---
# Part 11 — Practice Exercises (khud karo)

Har exercise ke sath **hint** hai. Pehle khud likho, phir hint dekho. Apna code assert se test karo.

**E1. Anti-pattern hunter.** Ye code Pythonic banao:
```python
result = []
for i in range(len(names)):
    if names[i] != "":
        result.append(names[i].upper())
```
*Hint:* comprehension + truthiness (`if name:`) + `enumerate` ki zaroorat bhi nahi (index use hi nahi ho raha).

**E2. Group by first letter, sorted by group size.** Words ki list se `{letter: [words]}` banao, aur
groups ko **size DESC, letter ASC** sort karo.
*Hint:* `defaultdict(list)` + `sorted(..., key=lambda kv: (-len(kv[1]), kv[0]))`.

**E3. Nested config merge.** Do nested dicts ka **deep merge** likho jahan andar ki dicts merge hon
(replace na hon), aur list values concatenate ho jayein.
*Hint:* recursion + `isinstance(v, dict)` check + `{**a, **b}` sirf top level ke liye.

**E4. Student report v2.** Part 7.1 ke data me ek naya subject add karo aur:
(a) subject-wise class average, (b) har student ka best/worst subject, (c) percentile rank nikalo.
*Hint:* `zip(*...)` transpose, `max(marks, key=marks.get)`, `sorted` + index se percentile.

**E5. `chunk_evenly` reverse.** Ek function likho jo chunks ki list wapas flat list bana de **aur**
verify kare ke koi element gum/duplicate nahi hua.
*Hint:* flatten comprehension + `Counter` comparison.

**E6. Stable multi-key sort ka test.** Ek function `assert_stable(rows, key)` likho jo saabit kare ke
`sorted` stable hai (barabar keys wale rows ka original relative order same rehta hai).
*Hint:* `enumerate` se original index attach karo, sort ke baad indexes ka order check karo.

**E7. LRU-ish word counter.** Ek generator likho jo text ka stream le aur har 100 words ke baad
top-3 words yield kare (running counter).
*Hint:* `Counter` + `enumerate(start=1)` + `yield` + `most_common(3)`.

**E8. `flatten` with depth limit.** `flatten(nested, depth=1)` likho — sirf `depth` levels tak flatten kare.
*Hint:* recursion me `depth - 1` pass karo; `depth == 0` par item waise hi de do.

**E9. RLE v2 (LeetCode 443 style).** `rle_encode` ka wo version likho jo count `1` skip kare **aur**
decode bhi us format ko samajh le. Round-trip test likho (digits wale input par kya hoga? — soch kar
documented limitation likho).
*Hint:* decode me digit missing = count 1.

**E10. Spiral in any direction.** `spiral(matrix, clockwise=True)` — dono directions support karo.
*Hint:* counter-clockwise = transpose kar ke clockwise spiral, ya boundaries ka order badal do.
"""))

# ================================================================ summary
A(md("""
---
# Part 12 — Summary / Cheat-sheet

## Idioms: BAD → GOOD

| Kaam | BAD ❌ | GOOD ✅ |
|---|---|---|
| Index + value | `for i in range(len(x)): x[i]` | `for i, v in enumerate(x)` |
| Parallel loop | `for i in range(len(a)): a[i], b[i]` | `for x, y in zip(a, b, strict=True)` |
| Swap | `t = a; a = b; b = t` | `a, b = b, a` |
| Range check | `if 0 <= x and x <= 10` | `if 0 <= x <= 10` |
| Flag loop | `found = False; for ...` | `any(cond for x in xs)` |
| Empty check | `if len(items) == 0` | `if not items` |
| Missing key | `if k in d: v = d[k] else: 0` | `v = d.get(k, 0)` |
| Grouping | `if k not in d: d[k] = []` | `defaultdict(list)` / `d.setdefault(k, []).append(v)` |
| Counting | `d[k] = d.get(k,0)+1` | `Counter(items)` |
| String build | `s += piece` in loop | `"".join(pieces)` |
| Punctuation strip | `.replace()` chain | `s.translate(str.maketrans("", "", punctuation))` |
| Reverse | manual loop | `x[::-1]` / `reversed(x)` |
| Copy list | manual loop | `x[:]` / `list(x)` (shallow!) |
| 2D grid | `[[0]*n]*m` ❌ | `[[0]*n for _ in range(m)]` |
| Debug print | `print("x =", x)` | `print(f"{x=}")` |
| Check then act | `if k in d: d[k]` | `try: d[k] except KeyError:` (EAFP) |
| Mutable default | `def f(a=[])` | `def f(a=None)` |
| Sort in place | `x = x.sort()` ❌ | `x.sort()` / `x = sorted(x)` |

## Comprehensions
```python
[expr for x in it if cond]            # filter -> length chhoti ho sakti hai
[a if cond else b for x in it]        # conditional VALUE -> length same
{k: v for k, v in pairs}              # dict comp
{expr for x in it}                    # set comp ( {} khali DICT hai! )
(expr for x in it)                    # generator: lazy, O(1) memory, ek baar
[x for row in matrix for x in row]    # FLATTEN (for clauses = normal nested order)
[[f(i,j) for j in ...] for i in ...]  # nested = list of lists
```
**Refactor karo jab:** 2+ `for` clauses, 3+ total clauses, nested ternary, line > 79 chars.

## Sorting
```python
sorted(it, key=..., reverse=...)          # nayi list, koi bhi iterable
lst.sort(key=...)                          # in-place, returns None
key=lambda r: (r["a"], -r["n"])            # multi-key; numeric desc = negate
lst.sort(key=itemgetter("name"))           # two-pass stable: secondary pehle
lst.sort(key=itemgetter("score"), reverse=True)   # phir primary
itemgetter("a", "b") / attrgetter("x.y") / methodcaller("lower")
functools.cmp_to_key(cmp)                  # sirf jab pairwise rule ho
sorted(d.items(), key=itemgetter(1))       # dict by value
sorted(d, key=d.get)                       # keys by value
Counter(d).most_common(k) / heapq.nlargest(k, ...)
```
Timsort: **stable**, worst O(n log n), best O(n) (already-sorted data par).

## Unpacking
```python
a, *rest = xs        *init, last = xs        a, *mid, b = xs      # starred -> list
name, (h, m) = rec                                                # nested
{**a, **b}   a | b   a |= b                                       # dict merge (right wins, SHALLOW)
[*a, *b]  (*a, x)  {*a, *b}                                       # literal unpacking
list(zip(*matrix))                                                # transpose / unzip
f(*args, **kwargs)                                                # call unpacking
def f(pos, /, normal, *args, kw_only, **kwargs)                    # full signature order
```

## Copy
| Expression | Kya milta hai |
|---|---|
| `b = a` | alias — same object |
| `a[:]`, `list(a)`, `a.copy()`, `copy.copy(a)`, `{**d}` | **shallow** — andar wale shared |
| `copy.deepcopy(a)` | **deep** — sab naya (cycles bhi safe) |
| `a == b` / `a is b` | values barabar / same object |

## Interview problems ki complexity (quick revision)
| Problem | Optimal Time | Space |
|---|---|---|
| Top-k words | O(n log k) | O(m unique) |
| Flatten nested | O(n) | O(depth) |
| Group anagrams | O(n·k) count-key | O(n·k) |
| Find duplicates | O(n) set | O(n) |
| Rotate matrix | O(n²) | O(1) in-place |
| Spiral order | O(m·n) | O(1) extra |
| Chunk list | O(n) | O(n) / O(k) gen |
| RLE encode/decode | O(n) | O(n) |
| Balanced brackets | O(n) | O(n) stack |
| Roman ↔ int | O(1)* | O(1) |
| Caesar cipher | O(n) | O(n) |
| First non-repeating | O(n) 2-pass | O(k) |
| Longest word | O(n) | O(n) |
| Digital root | O(1) formula | O(1) |
| Transpose | O(m·n) | O(m·n) / O(1) sq |
| Moving average | O(n) running sum | O(1) |
| Longest substring (LC 3) | O(n) sliding window | O(min(n, Σ)) |
| String compression (LC 443) | O(n) 2 pointers | O(1) |

## Aakhri naseehat
1. **Readability > cleverness.** Ek line ka jaadu jo 5 minute me samajh aaye, wo bug hai jo abhi likha nahi gaya.
2. **Interview me:** pehle brute force batao + complexity, phir optimize karo, phir edge cases (`""`, `[]`,
   `None`, single element, duplicates, negative, overflow) khud se batao. Yehi senior signal hai.
3. **Test likho:** `assert` chhote hote hain magar `round-trip` aur `cross-check` tests (do approaches ka
   natija barabar) sabse zyada bug pakarte hain — is notebook me hum ne har jagah wahi kiya.
"""))

# ==MARKER==

save(
    r"Python/Intermediate/06_Comprehension_Patterns_Idioms_aur_Interview_Problems.ipynb",
    CELLS,
)
