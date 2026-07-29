# Generator script: Python/Intermediate/01_Iterators_Generators_aur_Itertools.ipynb
import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

PATH = r"Python/Intermediate/01_Iterators_Generators_aur_Itertools.ipynb"

cells = []

cells += [
md("""
# 01 — Iterators, Generators aur Itertools

**Level:** Intermediate  ·  **Language:** Python 3.14  ·  **Series:** Python/Intermediate

Ye notebook Python ke **lazy evaluation** engine ko kholta hai. Jab tum `for x in something:` likhte ho,
Python andar andar jo protocol chalata hai — wahi is notebook ka mauzoo hai.

## Is notebook me kya seekhenge

- **Iterable vs Iterator** — dono me farq kya hai (interview ka favourite sawal)
- `iter()` / `next()` aur `StopIteration` ka asli role
- `for` loop ke andar ka **desugared** form (manual loop likh kar dekhenge)
- **Custom iterator class** — `__iter__` / `__next__` khud implement karna
- **Generator functions** aur `yield` — 3 line me iterator
- **Generator expressions** — comprehension ka lazy bhai
- **Lazy evaluation** ka faida: `sys.getsizeof` + timing se memory/speed comparison
- **Infinite generators** aur unko safely kaatna (`islice`)
- `yield from` — delegation
- Generator ke advanced controls: `send()`, `throw()`, `close()` (coroutine ki jhalak)
- **Pipeline pattern** — Unix pipes jaisa data processing (log analysis)
- **itertools** ka poora tour: `count, cycle, repeat, chain, islice, tee, zip_longest, product,
  permutations, combinations, groupby, accumulate, starmap, compress, dropwhile, takewhile,
  filterfalse, pairwise, batched`
- Ek "bara file" `io.StringIO` se **lazily** parhna (memory-safe file processing)
- Gotchas, Real-world problems, **LeetCode problems** (341, 284, 173, 1291), Interview Q&A, Practice, Cheat-sheet

## Prerequisites

- Python basics: `for` loop, `list`/`dict`/`set`, function define karna
- List comprehension ka basic idea
- Classes ka thora sa taaruf (`__init__`, `self`) — NB me phir bhi samjha denge

> **Tip:** Cells ko upar se neeche chalao. Har cell agle cell ke variables par depend kar sakta hai.
"""),
]

cells += [
md("""
---
## 1. Iterable vs Iterator — bunyadi farq

Ye do lafz log mila dete hain. Farq crystal clear kar lo:

| | **Iterable** | **Iterator** |
|---|---|---|
| Kya hai | Jis par loop chal sakta hai | Wo cheez jo **agli value** deti hai |
| Zaroori method | `__iter__()` | `__iter__()` **aur** `__next__()` |
| Misaal | `list`, `tuple`, `str`, `dict`, `set`, `range` | `list_iterator`, generator, `zip` object, `map` object |
| State rakhta hai? | Nahi (position yaad nahi) | **Haan** — kahan tak pohancha hua hai |
| Dobara loop? | Haan, har baar naya iterator banta hai | **Nahi** — ek baar khatam to khatam |

**Rishta:** `iterable` se `iter()` call kar ke **iterator** nikalta hai.

```
iterable  --iter()-->  iterator  --next()-->  value, value, value, ... StopIteration
```

**Kyun important?** Kyunki:
1. `for` loop isi protocol par chalta hai.
2. Lazy evaluation (memory bachana) isi ki wajah se mumkin hai.
3. Interview me "list aur generator me farq" ka jawab yahin se aata hai.
"""),
code("""
# ---- Iterable vs Iterator practically dekhte hain ----

nums = [10, 20, 30]          # ye ek ITERABLE hai (list)

# 1) Kya list ke paas __iter__ hai?
print("list me __iter__ hai?  ", hasattr(nums, "__iter__"))
# 2) Kya list ke paas __next__ hai? -> NAHI. Is liye list iterator nahi hai.
print("list me __next__ hai?  ", hasattr(nums, "__next__"))

print("-" * 45)

# iter() lagao -> ITERATOR milta hai
it = iter(nums)
print("iter(nums) ka type:    ", type(it).__name__)   # list_iterator
print("iterator me __iter__?  ", hasattr(it, "__iter__"))  # True (iterator bhi iterable hota hai)
print("iterator me __next__?  ", hasattr(it, "__next__"))  # True <- yahi asli farq hai
"""),
md("""
### Output ka matlab

- `list` ke paas sirf `__iter__` hai → wo **iterable** hai, iterator nahi.
- `iter(nums)` ne `list_iterator` object banaya jiske paas **dono** methods hain.
- **Har iterator khud bhi iterable hota hai** (`__iter__` return karta hai `self`) — is liye tum iterator par
  bhi `for` chala sakte ho. Magar ulta nahi: har iterable iterator nahi hota.

**Interview tip:** Ek line ka jawab —
*"Iterable wo hai jis se iterator banaya ja sakta hai; iterator wo hai jo `__next__` se values deta hai aur apni
position ka state rakhta hai."*
"""),
]

cells += [
md("""
---
## 2. `next()` aur `StopIteration`

`next(iterator)` iterator ko "ek qadam" chalata hai. Jab values khatam ho jayein to Python
`StopIteration` **exception** phenkta hai — ye error nahi, ek **signal** hai ke "bas, khatam".

**Syntax:**
```python
next(iterator)              # khatam hone par StopIteration raise karega
next(iterator, default)     # khatam hone par exception ke bajaye default return karega
```
"""),
code("""
# ---- next() ek ek qadam ----
it = iter([1, 2, 3])          # 3 values wala iterator

print(next(it))               # 1
print(next(it))               # 2
print(next(it))               # 3

# Ab iterator khali hai. Agla next() StopIteration dega.
# Jaan boojh kar error dikhana hai -> try/except me wrap karte hain (notebook crash na ho)
try:
    next(it)
except StopIteration:
    print("StopIteration aa gaya -> iterator exhausted (khatam) ho chuka hai")

# Safe tareeqa: default value do, exception hi nahi aayega
print("default ke sath:", next(it, "KHATAM"))
"""),
code("""
# ---- Iterator ONE-SHOT hota hai: ye gotcha bohat log ko pakadta hai ----

nums = [1, 2, 3]

it = iter(nums)
print("pehla  loop:", [x for x in it])   # sab values consume ho gayin
print("dusra  loop:", [x for x in it])   # KHALI list! iterator dobara nahi chalta

print("-" * 45)

# Lekin ITERABLE (list) par dobara loop bilkul chalta hai,
# kyunki har `for` naya iterator banata hai:
print("list par pehla loop:", [x for x in nums])
print("list par dusra loop:", [x for x in nums])
"""),
md("""
### Output ka matlab / Gotcha

Dusri list **khali** aayi kyunki `it` apni position aakhir tak le ja chuka tha.
Iterator me "rewind" ka koi tareeqa nahi hota — naya iterator banana padta hai.

**Yahan log phaste hain:** `zip()`, `map()`, `filter()`, `enumerate()`, aur `reversed()` sab **iterators**
return karte hain (Python 3 me). Un par do baar loop chalao to dusri baar khali milega.
"""),
code("""
# ---- Real gotcha: zip object do baar use karna ----
names  = ["Ali", "Sara", "Bilal"]
marks  = [90, 85, 78]

pairs = zip(names, marks)        # ye ek ITERATOR hai, list nahi

print("count karne ki koshish:", len(list(pairs)))   # 3 -> magar isne pairs consume kar liya!
print("ab loop karo         :", list(pairs))         # [] <- khali, kyunki khatam ho gaya

print("-" * 45)
# HAL: agar dobara chahiye to list me materialize kar lo
pairs = list(zip(names, marks))  # ab ye list hai (iterable, reusable)
print("length:", len(pairs))
print("loop  :", pairs)
"""),
]

cells += [
md("""
---
## 3. `for` loop andar se kaisa dikhta hai?

`for` loop koi jadoo nahi. Ye bilkul isi tarah "desugar" hota hai:

```python
for x in iterable:          #  ==  it = iter(iterable)
    body(x)                 #      while True:
                            #          try:    x = next(it)
                            #          except StopIteration: break
                            #          body(x)
```

Chalo isko haath se likh kar sabit karte hain.
"""),
code("""
# ---- `for` loop ko manually implement karna ----

def manual_for(iterable, action):
    # Step 1: iterable se iterator banao
    it = iter(iterable)
    while True:
        try:
            item = next(it)          # Step 2: agli value maango
        except StopIteration:
            break                    # Step 3: signal mila -> loop tordo
        action(item)                 # Step 4: body chalao

# Test: normal for loop jaisa hi behaviour
print("for loop:   ", end="")
for ch in "PYTHON":
    print(ch, end=" ")
print()

print("manual_for: ", end="")
manual_for("PYTHON", lambda ch: print(ch, end=" "))
print()
"""),
md("""
**Interview tip:** Agar poocha jaye *"`for` loop internally kaise kaam karta hai?"* — bas yahi 4 steps bata do:
`iter()` → `next()` loop → `StopIteration` par break. Is ek jawab se pata chal jata hai ke tumhe protocol samajh hai.
"""),
]

cells += [
md("""
---
## 4. Custom Iterator Class — `__iter__` / `__next__`

Agar tum apni class ko `for` loop me chalana chahte ho, to **iterator protocol** implement karo:

- `__iter__(self)` → iterator object return kare (agar khud class hi iterator hai to `return self`)
- `__next__(self)` → agli value return kare, ya `raise StopIteration` kare jab khatam ho

**Kahan use hota hai?** Jab data ko step-by-step generate karna ho — paging API, sensor readings,
custom range, tree traversal.
"""),
code("""
# ---- Custom iterator: Countdown (N se 1 tak ulta ginna) ----

class Countdown:
    # __init__: sirf setup, koi value generate nahi
    def __init__(self, start):
        self.start = start           # asal starting value (yaad rakhi, badalte nahi)

    def __iter__(self):
        # NOTE: har baar NAYA state banate hain -> is liye Countdown REUSABLE iterable hai
        self.current = self.start
        return self                  # khud iterator hai, is liye self

    def __next__(self):
        if self.current <= 0:        # khatam hone ki shart
            raise StopIteration      # signal: bas ho gaya
        value = self.current         # jo return karna hai
        self.current -= 1            # state aage (yahan peeche) barhao
        return value


print("for loop se:", list(Countdown(5)))
print("dobara     :", list(Countdown(5)))    # reusable, kyunki __iter__ state reset karta hai

# Manually bhi chala sakte ho
c = Countdown(3)
it = iter(c)
print("manual:", next(it), next(it), next(it))
try:
    next(it)
except StopIteration:
    print("StopIteration -> countdown khatam")
"""),
code("""
# ---- Aik zyada realistic misaal: paged API reader (fake data, koi network nahi) ----

class PagedResults:
    # Sochlo API ek waqt me sirf `page_size` records deta hai.
    # Iterator user ko ek-ek record deta hai, paging andar chupa deta hai.
    def __init__(self, records, page_size=3):
        self._records = records
        self._page_size = page_size

    def __iter__(self):
        self._i = 0                              # kis record par hain
        self._pages_fetched = 0                  # kitni "API calls" hui
        return self

    def __next__(self):
        if self._i >= len(self._records):
            raise StopIteration
        # naya page shuru ho raha hai? to "fetch" ka message dikhao
        if self._i % self._page_size == 0:
            self._pages_fetched += 1
            print(f"   [API] page {self._pages_fetched} fetch ki gayi...")
        rec = self._records[self._i]
        self._i += 1
        return rec


users = [f"user{n}" for n in range(1, 8)]        # 7 records
print("Sab users ghoomte hain (paging andar chup hui hai):")
for u in PagedResults(users, page_size=3):
    print("   ->", u)
"""),
md("""
### Output ka matlab

`[API] page N fetch ki gayi...` sirf tab print hua jab naya page chahiye tha. User ke code me koi
paging logic nahi — wo simply `for u in PagedResults(...)` likhta hai. **Yehi iterator ka asli faida hai:
complexity chhupa lena.**

### Common mistakes (custom iterator)

1. `__iter__` me `return self` bhool jana → `TypeError: iter() returned non-iterator`.
2. `__next__` me `StopIteration` raise na karna → **infinite loop**.
3. State `__init__` me rakhna aur `__iter__` me reset na karna → class sirf **ek baar** loop hogi
   (iterator ban jayegi, reusable iterable nahi).
"""),
code("""
# ---- Mistake #1 aur #3 ka live demo (try/except me safe) ----

class BadIter:
    def __iter__(self):
        return 42                 # GALAT: iterator nahi, int return kiya

try:
    for x in BadIter():
        pass
except TypeError as e:
    print("Mistake #1 ->", type(e).__name__, ":", e)

print("-" * 45)

class OneShotRange:
    # State __init__ me hai aur __iter__ reset nahi karta -> sirf ek baar chalega
    def __init__(self, n):
        self.i = 0
        self.n = n
    def __iter__(self):
        return self               # koi reset nahi
    def __next__(self):
        if self.i >= self.n:
            raise StopIteration
        self.i += 1
        return self.i

r = OneShotRange(4)
print("Mistake #3 -> pehla loop:", list(r))
print("Mistake #3 -> dusra loop:", list(r), "  <- khali! state reset nahi hua")
"""),
]

cells += [
md("""
---
## 5. Generator functions aur `yield`

Upar wali class 10-12 lines ki thi. **Generator** se wahi kaam 3 line me:

- Function ke andar `return` ki jagah **`yield`** likho.
- Aisa function call karne par body **chalti nahi** — ek **generator object** (iterator) milta hai.
- Har `next()` par body `yield` tak chalti hai, value deti hai, aur **wahin ruk jati hai** (state mehfooz).
- Function khatam hone par Python khud `StopIteration` raise kar deta hai.

**Syntax:**
```python
def gen(...):
    yield value1
    yield value2
```

**Kyun use karein?** Kam code, kam memory, lazy evaluation, aur infinite sequences mumkin.
"""),
code("""
# ---- Class vs Generator: wahi Countdown, 3 lines me ----

def countdown(start):
    n = start
    while n > 0:
        yield n            # value do aur YAHIN ruk jao
        n -= 1             # agle next() par yahan se chalna shuru hoga

print("generator se:", list(countdown(5)))

g = countdown(3)
print("type:", type(g).__name__)                  # generator
print("iterable?", hasattr(g, "__iter__"), " iterator?", hasattr(g, "__next__"))
print("values:", next(g), next(g), next(g))
try:
    next(g)
except StopIteration:
    print("StopIteration -> generator function ka body khatam")
"""),
code("""
# ---- `yield` par execution RUK jati hai: isko print se sabit karte hain ----

def noisy():
    print("   [gen] shuru hua")
    yield 1
    print("   [gen] pehle yield ke BAAD chala")
    yield 2
    print("   [gen] doosre yield ke BAAD chala")
    print("   [gen] body khatam -> StopIteration ayega")

g = noisy()
print("generator object ban gaya -- gaur karo: abhi tak body ka koi print NAHI hua")
print("next() #1 ->", next(g))
print("next() #2 ->", next(g))
try:
    next(g)
except StopIteration:
    print("next() #3 -> StopIteration")
"""),
md("""
### Output ka matlab (bohat ahem)

Gaur karo ke `g = noisy()` par `[gen] shuru hua` print **nahi** hua! Generator ka body **pehle `next()`**
par chalna shuru hota hai. Ye "lazy" hone ka pehla saboot hai.

**Interview tip:** *"Generator function call karne par kya hota hai?"* → *"Body nahi chalti; ek generator
object (iterator) return hota hai. Body pehle `next()` par shuru hoti hai aur har `yield` par suspend ho
jati hai, apna local state mehfooz rakhte hue."*
"""),
code("""
# ---- Generator me `return` ka matlab: StopIteration ki value ----

def with_return():
    yield "a"
    yield "b"
    return "MAIN RETURN VALUE"      # generator me return = "bas khatam", value StopIteration me jati hai
    # yahan ke baad kuch nahi chalega

g = with_return()
print(next(g))
print(next(g))
try:
    next(g)
except StopIteration as e:
    # return ki value e.value me milti hai (normally ignore hoti hai)
    print("StopIteration ki value:", e.value)

# Aur dhyan do: `for` loop return value ko ignore kar deta hai
print("for loop:", list(with_return()))
"""),
]

cells += [
md("""
---
## 6. Generator Expressions

List comprehension ka lazy version. Sirf brackets badalte hain:

```python
[x * x for x in range(5)]     # list comprehension  -> poori list foran banti hai
(x * x for x in range(5))     # generator expression -> lazy, kuch nahi banta
```

Agar function call ka **sirf ek** argument ho to bracket bhi nahi chahiye:
```python
sum(x * x for x in range(5))  # saaf aur memory-friendly
```
"""),
code("""
# ---- listcomp vs genexp ----
listcomp = [x * x for x in range(6)]        # foran calculate
genexp   = (x * x for x in range(6))        # lazy, sirf recipe

print("listcomp:", listcomp, type(listcomp).__name__)
print("genexp  :", genexp, type(genexp).__name__)   # object dikhata hai, values nahi

print("genexp ko materialize:", list(genexp))
print("dobara materialize   :", list(genexp), " <- khali, one-shot tha")

print("-" * 45)
# Aggregation functions ke andar bracket ki zaroorat nahi
print("sum   :", sum(x * x for x in range(6)))
print("max   :", max(len(w) for w in ["Pakistan", "Lahore", "Karachi"]))
print("any   :", any(n % 7 == 0 for n in [3, 5, 14, 9]))
print("all   :", all(n > 0 for n in [3, 5, 14, 9]))
"""),
md("""
### Kab kaun sa?

| Situation | Use |
|---|---|
| Values dobara chahiye / index chahiye / `len()` chahiye | **list comprehension** |
| Sirf ek baar loop karna hai (`sum`, `max`, `any`, `for`) | **generator expression** |
| Data bara hai / infinite hai | **generator expression** (lazzat memory me) |
| Chhota data + readability | list comprehension theek hai |

**Gotcha:** `len(genexp)` kaam nahi karta (`TypeError`), aur `genexp[0]` bhi nahi (subscript nahi hota).
"""),
code("""
# ---- Genexp ke do gotchas ----
g = (x for x in range(5))

try:
    print(len(g))
except TypeError as e:
    print("len(genexp) ->", type(e).__name__, ":", e)

try:
    print(g[0])
except TypeError as e:
    print("genexp[0]   ->", type(e).__name__, ":", e)

# Hal: itertools.islice se "index jaisa" kaam, ya list() bana lo
import itertools
g2 = (x for x in range(5))
print("islice se 3rd value:", list(itertools.islice(g2, 2, 3)))
"""),
]

cells += [
md("""
---
## 7. Lazy Evaluation — memory aur speed ka asli faida

**Lazy** ka matlab: value **sirf tab** banao jab maangi jaye. Iske do bare faide:

1. **Memory** — poora data RAM me nahi aata (constant memory).
2. **Time-to-first-result** — pehli value foran mil jati hai, poora dataset process hone ka intezar nahi.

Chalo `sys.getsizeof` aur `time.perf_counter` se numbers dekh lein.
"""),
code("""
import sys
import time

N = 1_000_000

# ---- 1) MEMORY comparison ----
big_list = [x * x for x in range(N)]          # 1 million ints ki poori list
gen_obj  = (x * x for x in range(N))          # sirf recipe

list_bytes = sys.getsizeof(big_list)
gen_bytes  = sys.getsizeof(gen_obj)

print(f"list  ({N:,} items) : {list_bytes:>10,} bytes  (~{list_bytes/1024/1024:.2f} MB)")
print(f"generator            : {gen_bytes:>10,} bytes  (~{gen_bytes} bytes, constant!)")
print(f"farq                 : ~{list_bytes // gen_bytes:,}x chhota")

# NOTE: getsizeof list ke andar wale int objects ko count nahi karta,
# yani asli farq isse bhi ZYADA hai. Neeche wo bhi naap lete hain.
deep = list_bytes + sum(sys.getsizeof(v) for v in big_list[:1000]) // 1000 * len(big_list)
print(f"list ka approx TOTAL : ~{deep/1024/1024:.1f} MB (ints ko count karte hue)")

del big_list      # RAM wapis kar do
"""),
code("""
# ---- 2) TIME-TO-FIRST-RESULT comparison ----
# Kaam: 1 million numbers me se pehla aisa number dhoondo jo 7 aur 11 dono se divide ho.

N = 1_000_000

# Eager tareeqa: PEHLE poori list banao, PHIR dhoondo
t0 = time.perf_counter()
all_matches = [x for x in range(N) if x % 7 == 0 and x % 11 == 0 and x > 0]
first_eager = all_matches[0]
t_eager = time.perf_counter() - t0

# Lazy tareeqa: generator + next() -> pehla match milte hi ruk jao
t0 = time.perf_counter()
lazy = (x for x in range(N) if x % 7 == 0 and x % 11 == 0 and x > 0)
first_lazy = next(lazy)
t_lazy = time.perf_counter() - t0

print(f"eager: pehla match = {first_eager}, time = {t_eager*1000:.2f} ms  (poori list bani)")
print(f"lazy : pehla match = {first_lazy}, time = {t_lazy*1000:.2f} ms  (77 tak ja kar ruk gaya)")
print(f"speedup (pehli value ke liye): ~{t_eager/max(t_lazy, 1e-9):.0f}x")
assert first_eager == first_lazy == 77   # dono ka jawab same
"""),
md("""
### Output ka matlab

- **Memory:** generator ka size **constant** (~200 bytes) hai, list ka size data ke sath barhta hai.
- **Time:** lazy version ne sirf 77 tak kaam kiya, baqi 999,923 numbers ko chhua bhi nahi.

### Kab lazy NAHI chahiye?

- Data chhota hai aur tumhe **kai baar** ghoomna hai → list behtar (generator dobara nahi chalega).
- `len()`, indexing, `sort()`, `reverse()` chahiye → list.
- Random access chahiye → list.

**Interview tip:** *"Generator kab use karoge?"* → *"Jab data bara/infinite ho, ya streaming ho, ya sirf ek
baar traverse karna ho — memory O(1) rehti hai. Jab reuse/indexing chahiye to list."*
"""),
]

cells += [
md("""
---
## 8. Infinite Generators — aur unko safely kaatna

Generator kabhi khatam na hone wala bhi ho sakta hai (`while True: yield ...`). Ye theek hai — bas
**consume karte waqt** limit lagana zaroori hai warna program hang ho jayega.

Kaatne ke tareeqe:
- `itertools.islice(gen, n)` → pehli `n` values
- loop ke andar `break`
- `zip(gen, range(n))`
- `itertools.takewhile(pred, gen)`

**Kabhi na karo:** `list(infinite_gen)` — ye kabhi wapis nahi aayega (memory khatam).
"""),
code("""
import itertools

# ---- Infinite generator #1: natural numbers ----
def naturals(start=1):
    n = start
    while True:          # kabhi khatam nahi hota
        yield n
        n += 1

# Safe consumption: islice se pehli 10
print("pehli 10       :", list(itertools.islice(naturals(), 10)))

# break se manually
squares_found = []
for n in naturals():
    if n * n > 200:
        break                       # 200 se bara square mil gaya -> ruk jao
    squares_found.append(n * n)
print("squares <= 200 :", squares_found)

# takewhile se declaratively
print("takewhile      :", list(itertools.takewhile(lambda n: n < 8, naturals())))
"""),
code("""
# ---- Infinite generator #2: Fibonacci (classic) ----
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b        # tuple unpacking se ek line me swap+add

print("pehli 12 fib :", list(itertools.islice(fibonacci(), 12)))

# 1000 se bari pehli fib number
first_big = next(f for f in fibonacci() if f > 1000)
print("1000 se bari pehli fib:", first_big)
assert first_big == 1597

# ---- Infinite generator #3: cyclic ID assigner (round-robin) ----
def round_robin_servers(servers):
    while True:
        for s in servers:
            yield s                 # list khatam hote hi phir shuru

rr = round_robin_servers(["srv-A", "srv-B", "srv-C"])
assigned = [next(rr) for _ in range(7)]     # 7 requests
print("round robin  :", assigned)
"""),
md("""
### Gotcha: infinite generator ko galti se materialize karna

```python
list(naturals())        # ❌ program hang / MemoryError
sum(naturals())         # ❌ same
sorted(naturals())      # ❌ same
max(naturals())         # ❌ same
```

Sab aggregation functions **poora** iterator consume karte hain. Infinite ke sath sirf lazy operations
(`islice`, `takewhile`, `next`, `break`) chalao.
"""),
]

cells += [
md("""
---
## 9. `yield from` — delegation

`yield from other_iterable` ka matlab: *"is iterable ki saari values meri taraf se yield kar do"*.

```python
# Purana tareeqa                    # yield from ke sath
for x in sub:                       yield from sub
    yield x
```

Faida sirf chhota code nahi — `yield from` **send/throw/return** bhi properly forward karta hai
(sub-generator ke sath two-way communication chalti rehti hai).

**Sab se common use:** recursion — nested structures ko flatten karna, tree traverse karna.
"""),
code("""
# ---- Basic: manual loop vs yield from ----
def manual_chain(a, b):
    for x in a:
        yield x
    for x in b:
        yield x

def yf_chain(a, b):
    yield from a          # bilkul wahi kaam, ek line
    yield from b

print("manual_chain:", list(manual_chain([1, 2], "ab")))
print("yf_chain    :", list(yf_chain([1, 2], "ab")))
assert list(manual_chain([1, 2], "ab")) == list(yf_chain([1, 2], "ab"))
"""),
code("""
# ---- Recursion ka asli power: nested list flatten (kisi bhi depth tak) ----

def flatten(nested):
    for item in nested:
        # Agar item khud ek list/tuple hai to us par RECURSE karo
        if isinstance(item, (list, tuple)):
            yield from flatten(item)      # sub-generator ki values pass-through
        else:
            yield item                    # scalar -> seedha de do

data = [1, [2, 3, [4, [5, 6]], 7], 8, (9, [10])]
print("nested :", data)
print("flat   :", list(flatten(data)))
assert list(flatten(data)) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Lazy hai: pehli 4 values ke liye poora structure walk nahi hota
print("pehli 4:", list(itertools.islice(flatten(data), 4)))
"""),
code("""
# ---- yield from ke sath tree traversal (in-order) ----

class Node:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right

def in_order(node):
    if node is None:
        return                     # generator me plain return = "khatam"
    yield from in_order(node.left)  # pehle poora left subtree
    yield node.val                  # phir khud
    yield from in_order(node.right) # phir right subtree

#         8
#       /   \\
#      3     10
#     / \\      \\
#    1   6      14
tree = Node(8, Node(3, Node(1), Node(6)), Node(10, None, Node(14)))
print("in-order:", list(in_order(tree)))
assert list(in_order(tree)) == [1, 3, 6, 8, 10, 14]   # BST ka in-order = sorted
"""),
]

cells += [
md("""
---
## 10. Generator ke advanced controls: `send()`, `throw()`, `close()`

Ab tak humne generator se sirf values **li** hain. Magar generator me values **bheji** bhi ja sakti hain —
yahan se "coroutine" ka concept shuru hota hai.

| Method | Kya karta hai |
|---|---|
| `gen.send(value)` | `yield` expression ki jagah `value` daalta hai aur generator ko aage chalata hai |
| `gen.throw(ExcType)` | Generator ke andar, current `yield` ki jagah exception raise karta hai |
| `gen.close()` | Generator ke andar `GeneratorExit` raise karta hai → cleanup ka mauqa |
| `gen.gi_frame` / `.gi_running` | Introspection (kahan ruka hua hai) |

**Ahem rule:** `send()` se pehle generator ko **prime** karna padta hai — yani ek `next(gen)` ya
`gen.send(None)` chalao taake wo pehle `yield` par pohanch jaye.
"""),
code("""
# ---- send(): running average calculator (coroutine style) ----

def running_average():
    total, count, avg = 0.0, 0, None
    while True:
        # `yield avg` do kaam karta hai: avg bahar bhejta hai AUR
        # send() se aayi value `new_value` me le leta hai
        new_value = yield avg
        if new_value is None:
            continue                       # None bheja gaya -> ignore
        total += new_value
        count += 1
        avg = total / count

ra = running_average()
print("prime (pehla next):", next(ra))     # None -> generator pehle yield par ruk gaya

for v in [10, 20, 30, 40]:
    print(f"send({v:>2}) -> running avg = {ra.send(v)}")

ra.close()                                  # kaam khatam
"""),
code("""
# ---- send() ka gotcha: prime kiye baghair send karna ----
ra2 = running_average()
try:
    ra2.send(10)          # GALAT: abhi generator start hi nahi hua
except TypeError as e:
    print("Gotcha ->", type(e).__name__, ":", e)
    print("HAL: pehle next(gen) ya gen.send(None) karo (priming)")

# Sahi tareeqa
ra2.send(None)            # prime
print("prime ke baad send(10):", ra2.send(10))
ra2.close()
"""),
code("""
# ---- close() aur GeneratorExit: cleanup guarantee ----

def resource_worker(name):
    print(f"   [open] {name} khul gaya")
    try:
        while True:
            item = yield
            print(f"   [work] {name} ne process kiya: {item}")
    except GeneratorExit:
        # close() par ye chalta hai -> yahan cleanup karo
        print(f"   [close] {name} band ho gaya (GeneratorExit)")
        raise                     # dobara raise karna acha practice hai
    finally:
        print(f"   [finally] {name} ka finally bhi chala")

w = resource_worker("db-conn")
next(w)                # prime -> [open] print hoga
w.send("row-1")
w.send("row-2")
w.close()              # -> GeneratorExit + finally
print("generator band hone ke baad send karna:")
try:
    w.send("row-3")
except StopIteration:
    print("   StopIteration -> band generator me kuch nahi bhej sakte")
"""),
code("""
# ---- throw(): generator ke andar exception inject karna ----

def resilient_worker():
    processed, errors = 0, 0
    while True:
        try:
            item = yield (processed, errors)
            processed += 1
        except ValueError as e:
            # Bahar se throw() kiya gaya error yahan pakda gaya
            errors += 1
            print(f"   [gen] ValueError handle kiya: {e}")

w = resilient_worker()
next(w)                                      # prime
print("send('a')      ->", w.send("a"))
print("send('b')      ->", w.send("b"))
print("throw(ValueError):")
print("   result      ->", w.throw(ValueError("kharab data")))
print("send('c')      ->", w.send("c"), " <- generator zinda hai, chal raha hai")
w.close()
"""),
md("""
### Output ka matlab

`throw()` ke baad bhi generator **zinda** raha kyunki usne exception ko andar `try/except` me pakad liya.
Agar generator handle na karta, to exception bahar (caller tak) aa jata aur generator band ho jata.

**Interview tip:** *"`send()` ka faida?"* → *"Two-way communication. Generator sirf producer nahi, consumer
bhi ban jata hai — yehi `async/await` coroutines ki bunyad hai. Practically aaj asyncio use karo, magar
concept samajhna zaroori hai."*
"""),
]

cells += [
md("""
---
## 11. Pipeline Pattern — Unix pipes Python me

Ye generators ka **sab se qeemti** real-world use hai. Har generator ek chhota kaam karta hai aur
apna output agle ko de deta hai:

```
read_lines  ->  filter_errors  ->  parse  ->  add_field  ->  summarize
   (lazy)          (lazy)         (lazy)      (lazy)         (consume)
```

**Faida:** poora data kabhi memory me nahi aata — chahe file 50 GB ki ho. Har stage ek waqt me **ek record**
handle karta hai. Aur stages ko lego blocks ki tarah reuse/reorder kar sakte ho.

Hum `io.StringIO` se ek fake log file banayenge (koi bahar ki file nahi chahiye).
"""),
code("""
import io

# ---- Fake log "file" (asli file ki tarah line-by-line parhi ja sakti hai) ----
LOG_TEXT = '''\\
2026-03-01 10:00:01 INFO  user=ali    action=login    ms=120
2026-03-01 10:00:04 ERROR user=sara   action=payment  ms=980  msg=card_declined
2026-03-01 10:00:07 INFO  user=bilal  action=browse   ms=45
2026-03-01 10:00:09 WARN  user=ali    action=upload   ms=1500
2026-03-01 10:00:12 ERROR user=ali    action=payment  ms=1100 msg=timeout
2026-03-01 10:00:15 INFO  user=sara   action=logout   ms=30
2026-03-01 10:00:19 ERROR user=zain   action=payment  ms=760  msg=card_declined
2026-03-01 10:00:24 INFO  user=zain   action=browse   ms=60
'''

def open_fake_log():
    # io.StringIO ek "file jaisa" object deta hai -> for line in f: chalta hai
    return io.StringIO(LOG_TEXT)

with open_fake_log() as f:
    print("Log ki pehli 3 lines:")
    for line in itertools.islice(f, 3):
        print("  ", line.rstrip())
"""),
code("""
# ================= PIPELINE STAGES (har ek chhota, lazy generator) =================

def read_lines(fileobj):
    # Stage 1: line by line parho, khali lines chhod do
    for line in fileobj:
        line = line.strip()
        if line:                     # khali line skip
            yield line

def only_level(lines, level):
    # Stage 2: sirf wo lines jinme diya gaya level ho
    for line in lines:
        if f" {level} " in line:
            yield line

def parse_record(lines):
    # Stage 3: line ko dict me todo -> structured data
    for line in lines:
        parts = line.split()
        rec = {
            "date": parts[0],
            "time": parts[1],
            "level": parts[2],
        }
        # baqi hisse key=value form me hain
        for token in parts[3:]:
            if "=" in token:
                k, v = token.split("=", 1)
                rec[k] = v
        yield rec

def add_seconds_field(records):
    # Stage 4: ms ko float seconds me convert kar ke naya field lagao
    for rec in records:
        rec["seconds"] = round(int(rec["ms"]) / 1000, 3)
        yield rec

def slow_only(records, threshold=1.0):
    # Stage 5: sirf slow requests
    for rec in records:
        if rec["seconds"] >= threshold:
            yield rec

print("Stages define ho gaye. Gaur karo: abhi tak kuch bhi execute nahi hua (sab lazy).")
"""),
code("""
# ================= PIPELINE ASSEMBLE + CONSUME =================

with open_fake_log() as f:
    # Pipeline jodo -- ye ek nested generator chain hai, abhi bhi kuch nahi chala
    lines    = read_lines(f)
    errors   = only_level(lines, "ERROR")
    records  = parse_record(errors)
    enriched = add_seconds_field(records)

    print("Pipeline bana -- pehla record maangte hain:")
    first = next(enriched)          # SIRF ek record ke liye poora chain 1 baar chala
    print("  ", first)

    print()
    print("Baqi ERROR records:")
    for rec in enriched:            # baqi stream karte hain
        print(f"   user={rec['user']:<6} msg={rec.get('msg','-'):<15} {rec['seconds']}s")
"""),
code("""
# ================= Pipeline se AGGREGATION (asli reporting) =================
from collections import Counter

with open_fake_log() as f:
    # Poora log -> parse -> enrich -> sirf slow (>=1s) -> count by user
    pipeline = slow_only(add_seconds_field(parse_record(read_lines(f))), threshold=1.0)
    slow_records = list(pipeline)          # chhota result, is liye materialize karna theek hai

print("Slow requests (>= 1.0s):")
for r in slow_records:
    print(f"   {r['time']}  {r['level']:<5} user={r['user']:<6} action={r['action']:<8} {r['seconds']}s")

print()
by_user = Counter(r["user"] for r in slow_records)
print("Slow requests per user:", dict(by_user))
assert by_user["ali"] == 2          # ali ke 2 slow requests (upload 1.5s + payment 1.1s)

# Ek aur report: error reasons
with open_fake_log() as f:
    reasons = Counter(
        r.get("msg", "unknown")
        for r in parse_record(only_level(read_lines(f), "ERROR"))
    )
print("Error reasons     :", dict(reasons))
assert reasons["card_declined"] == 2
"""),
md("""
### Output ka matlab / Pipeline ke faide

1. **Memory O(1)** — kabhi bhi sirf ek line + ek dict memory me tha.
2. **Composable** — `slow_only(...)` hatao, `only_level(...)` badlo — stages independent hain.
3. **Testable** — har stage ko alag se test kar sakte ho (chhota input do, output check karo).
4. **Early exit sasta** — `next(enriched)` ne poora log parhne ki zaroorat nahi ki.

**Interview tip:** Agar "10 GB log file process karni hai, memory 2 GB hai" wala sawal aaye — jawab
**generator pipeline** hai. Ye batao ke `read → filter → parse → aggregate` sab lazy rahenge aur
sirf final aggregate (Counter) memory me hoga.
"""),
]

cells += [
md("""
---
## 12. `itertools` — Python ka lazy toolkit

`itertools` stdlib module hai jo **iterator building blocks** deta hai. Sab C me likhe hue, tez, aur
**lazy** (memory O(1)). Interview aur real code dono me bohat kaam aata hai.

### Teen categories

**1. Infinite iterators**
| Function | Kaam |
|---|---|
| `count(start, step)` | `start, start+step, ...` hamesha |
| `cycle(iterable)` | iterable ko ghoom ghoom ke dohrata hai |
| `repeat(obj, times=None)` | `obj` ko baar baar (times na do to infinite) |

**2. Terminating (input par khatam)**
| Function | Kaam |
|---|---|
| `chain(a, b, ...)` | kai iterables ko jodta hai |
| `chain.from_iterable(iters)` | iterables ke iterable ko flatten |
| `islice(it, stop)` / `islice(it, start, stop, step)` | lazy slicing |
| `tee(it, n)` | ek iterator ki `n` independent copies |
| `zip_longest(a, b, fillvalue=)` | chhoti ko `fillvalue` se bharta hai |
| `compress(data, selectors)` | mask ke mutabiq filter |
| `dropwhile(pred, it)` | jab tak `pred` True, drop karo; phir sab |
| `takewhile(pred, it)` | jab tak `pred` True, lo; pehle False par ruk jao |
| `filterfalse(pred, it)` | `filter` ka ulta |
| `groupby(it, key)` | **consecutive** same-key items ko group |
| `accumulate(it, func)` | running total / running func |
| `starmap(func, tuples)` | `func(*tup)` har tuple par |
| `pairwise(it)` | consecutive jodey: `(a,b), (b,c), ...` (3.10+) |
| `batched(it, n)` | `n` size ke chunks (3.12+) |

**3. Combinatoric**
| Function | Kaam | Count |
|---|---|---|
| `product(a, b)` | cartesian product (nested loops) | `len(a)*len(b)` |
| `product(a, repeat=n)` | n-fold product | `len(a)**n` |
| `permutations(it, r)` | tarteeb **matters** | `n!/(n-r)!` |
| `combinations(it, r)` | tarteeb **matter nahi**, repeat nahi | `C(n,r)` |
| `combinations_with_replacement(it, r)` | tarteeb nahi, repeat allowed | `C(n+r-1, r)` |
"""),
code("""
import itertools as it_

# ================= 1) INFINITE: count, cycle, repeat =================

# count(): range jaisa magar infinite aur float step bhi chalta hai
print("count(10)      :", list(it_.islice(it_.count(10), 5)))          # 10,11,12,13,14
print("count(0, 5)    :", list(it_.islice(it_.count(0, 5), 5)))        # 0,5,10,15,20
print("count(1, 0.5)  :", list(it_.islice(it_.count(1, 0.5), 5)))      # float step -> range nahi kar sakta

# cycle(): round-robin / repeating pattern ke liye perfect
colors = it_.cycle(["red", "green", "blue"])
print("cycle 7 baar   :", [next(colors) for _ in range(7)])

# repeat(): fixed value; times do to finite
print("repeat('x', 4) :", list(it_.repeat("x", 4)))
print("repeat infinite:", list(it_.islice(it_.repeat(0), 3)))

# repeat ka classic use: map/zip ke sath constant argument
print("map+repeat pow :", list(map(pow, [2, 3, 4, 5], it_.repeat(2))))  # sab ka square
"""),
code("""
# ================= 2) chain, chain.from_iterable, islice =================

a, b, c = [1, 2], (3, 4), "56"
print("chain          :", list(it_.chain(a, b, c)))            # [1,2,3,4,'5','6']

# from_iterable: jab iterables khud ek list me hon (1-level flatten)
nested = [[1, 2], [3, 4, 5], [], [6]]
print("from_iterable  :", list(it_.chain.from_iterable(nested)))
# NOTE: ye sirf 1 level flatten karta hai. Deep flatten ke liye recursion (upar dekha) chahiye.

# islice: lazy slicing -- generator par bhi chalta hai (jahan [a:b] kaam nahi karta)
letters = it_.count(ord("a"))
print("islice(3)      :", [chr(x) for x in it_.islice(letters, 3)])
print("islice(2,7)    :", list(it_.islice(range(20), 2, 7)))          # start,stop
print("islice(0,20,4) :", list(it_.islice(range(20), 0, 20, 4)))      # step
# GOTCHA: islice negative index support NAHI karta (kyunki lazy hai, aakhir pata nahi)
try:
    list(it_.islice(range(10), -3, None))
except ValueError as e:
    print("islice(-3) ->  ValueError:", e)
"""),
code("""
# ================= 3) tee -- ek stream ki kai copies =================

def expensive_stream():
    for i in range(1, 6):
        print(f"      [source] {i} generate hua")     # dikhane ke liye
        yield i

# tee 2 independent iterators deta hai, magar source SIRF EK BAAR chalta hai
s1, s2 = it_.tee(expensive_stream(), 2)
print("s1 se pehli 2:", [next(s1), next(s1)])
print("s2 se pehli 2:", [next(s2), next(s2)], " <- source dobara nahi chala (buffer se aaya)")
print("s1 baqi      :", list(s1))
print("s2 baqi      :", list(s2))
"""),
md("""
### `tee()` ke 2 ahem gotchas

1. **Original iterator ko chhod do.** `tee()` ke baad asal iterator ko use karna undefined behaviour hai.
2. **Memory:** agar ek copy bohat aage nikal jaye aur dusri peeche reh jaye, to `tee` andar **buffer** rakhta
   hai — memory O(farq). Do copies ko roughly sath sath chalao. Agar data list me fit ho jata hai to
   `data = list(gen)` zyada simple aur saaf hai.
"""),
code("""
# ================= 4) zip vs zip_longest vs zip(strict=True) =================
names = ["Ali", "Sara", "Bilal", "Zain"]
marks = [90, 85, 78]                       # ek kam!

print("zip           :", list(zip(names, marks)))                 # Zain gayab (silently!)
print("zip_longest   :", list(it_.zip_longest(names, marks)))      # None se bhara
print("zip_longest f :", list(it_.zip_longest(names, marks, fillvalue=0)))

# Python 3.10+: strict=True se galti chup nahi rehti
try:
    list(zip(names, marks, strict=True))
except ValueError as e:
    print("zip strict    -> ValueError:", e)
"""),
md("""
**Interview tip:** `zip()` ka default behaviour **silently truncate** karna hai — ye bug ka bada source hai.
Jab length equal honi CHAHIYE, `strict=True` likho. Jab equal nahi hoti aur missing values chahiye,
`zip_longest` + `fillvalue` use karo.
"""),
code("""
# ================= 5) COMBINATORICS: product, permutations, combinations =================

sizes  = ["S", "M"]
colors = ["red", "blue"]

# product = nested for loops ka lazy version
print("product        :", list(it_.product(sizes, colors)))
# Barabar hai:  [(s, c) for s in sizes for c in colors]
assert list(it_.product(sizes, colors)) == [(s, c) for s in sizes for c in colors]

# repeat= se n-fold product (jaise 3-digit PIN ke sab combos)
print("product repeat :", ["".join(p) for p in it_.product("01", repeat=3)])

print("-" * 50)
# permutations: TARTEEB matter karti hai (AB != BA)
print("perm(ABC, 2)   :", ["".join(p) for p in it_.permutations("ABC", 2)])   # 6
print("perm(ABC)      :", ["".join(p) for p in it_.permutations("ABC")])      # 3! = 6

print("-" * 50)
# combinations: TARTEEB matter nahi (AB == BA), repeat nahi
print("comb(ABC, 2)   :", ["".join(p) for p in it_.combinations("ABC", 2)])   # 3
# combinations_with_replacement: repeat allowed (AA bhi)
print("comb_wr(ABC,2) :", ["".join(p) for p in it_.combinations_with_replacement("ABC", 2)])  # 6

# Counts verify karte hain formula se
import math
n, r = 5, 3
assert len(list(it_.permutations(range(n), r))) == math.perm(n, r)
assert len(list(it_.combinations(range(n), r))) == math.comb(n, r)
print("formula check  : perm(5,3) =", math.perm(5, 3), " comb(5,3) =", math.comb(5, 3))
"""),
code("""
# ================= 6) groupby -- aur uska SAB SE BADA gotcha =================

data = [
    ("fruit", "apple"), ("fruit", "banana"),
    ("veg",   "carrot"),
    ("fruit", "mango"),                       # ye "fruit" alag jagah hai!
    ("veg",   "peas"),
]

print("BINA sort kiye (GALAT natija):")
for key, group in it_.groupby(data, key=lambda t: t[0]):
    print(f"   {key:<6} -> {[v for _, v in group]}")

print()
print("SORT karne ke BAAD (sahi natija):")
sorted_data = sorted(data, key=lambda t: t[0])       # SAME key se sort -- ye lazmi hai
for key, group in it_.groupby(sorted_data, key=lambda t: t[0]):
    print(f"   {key:<6} -> {[v for _, v in group]}")
"""),
md("""
### `groupby` ka gotcha (interview me poocha jata hai)

`itertools.groupby` **sirf consecutive** (lagatar) same-key items ko group karta hai — SQL ka `GROUP BY`
nahi hai. Is liye:

> **Rule: `groupby` se pehle usi key par `sorted()` karo.**

Dusra gotcha: group ek **lazy iterator** hai jo agle group par jate hi **invalid** ho jata hai.
Agar baad me chahiye to foran `list(group)` bana lo.

Agar sirf counting/grouping chahiye aur sorting ka kharcha nahi karna, to `collections.defaultdict(list)`
ya `Counter` zyada seedha (aur O(n)) hai.
"""),
code("""
# ---- groupby gotcha #2: group iterator "expire" ho jata hai ----
groups = list(it_.groupby(sorted("mississippi")))       # (char, group) tuples ki list bana li
print("keys:", [k for k, g in groups])
print("pehle group ki values:", list(groups[0][1]), " <- KHALI! group expire ho gaya")

print()
print("Sahi tareeqa -- foran list bana lo:")
runs = [(k, list(g)) for k, g in it_.groupby(sorted("mississippi"))]
for k, g in runs:
    print(f"   '{k}' x {len(g)}")

# Practical: run-length style counting -- defaultdict se zyada seedha jab data already sorted ho
print("counts:", {k: len(g) for k, g in runs})
assert {k: len(g) for k, g in runs} == {"i": 4, "m": 1, "p": 2, "s": 4}
"""),
code("""
# ================= 7) accumulate -- running totals =================
import operator

sales = [100, 250, 75, 300, 125]

print("running sum    :", list(it_.accumulate(sales)))                       # default = add
print("running max    :", list(it_.accumulate(sales, max)))                   # running maximum
print("running product:", list(it_.accumulate([1, 2, 3, 4, 5], operator.mul)))
print("initial= ke sath:", list(it_.accumulate(sales, initial=0)))            # 0 se shuru (1 extra item)

# Real use: bank balance ka running statement
opening = 5000
txns = [-1200, 3000, -450, -800]
balances = list(it_.accumulate(txns, initial=opening))
print()
print("Opening balance:", opening)
for t, bal in zip(txns, balances[1:]):
    sign = "+" if t > 0 else "-"
    print(f"   {sign}{abs(t):<6} -> balance {bal}")
assert balances[-1] == opening + sum(txns)
"""),
code("""
# ================= 8) starmap, compress, filterfalse =================

# starmap: jab arguments already tuples me packed hon -> func(*tup)
pairs = [(2, 3), (4, 2), (10, 3)]
print("map    (lambda):", list(map(lambda p: pow(p[0], p[1]), pairs)))   # unpack manually
print("starmap        :", list(it_.starmap(pow, pairs)))                  # saaf!

# compress: boolean mask se filter (numpy ki boolean indexing jaisa)
students = ["Ali", "Sara", "Bilal", "Zain", "Hina"]
passed   = [True, False, True, True, False]
print("compress       :", list(it_.compress(students, passed)))

# filterfalse: filter ka ulta
nums = range(10)
print("filter   (even):", list(filter(lambda n: n % 2 == 0, nums)))
print("filterfalse    :", list(it_.filterfalse(lambda n: n % 2 == 0, nums)))   # odd
"""),
code("""
# ================= 9) takewhile vs dropwhile (dono "pehle False" par switch karte hain) =================
readings = [2, 4, 6, 1, 8, 10, 3]

print("data           :", readings)
print("takewhile(<7)  :", list(it_.takewhile(lambda n: n < 7, readings)))
print("dropwhile(<7)  :", list(it_.dropwhile(lambda n: n < 7, readings)))
print("filter(<7)     :", list(filter(lambda n: n < 7, readings)), " <- farq gaur karo!")
"""),
md("""
### `takewhile` / `dropwhile` vs `filter`

- `takewhile` **pehli** False par hamesha ke liye ruk jata hai (baqi data dekhta bhi nahi).
- `dropwhile` **pehli** False tak drop karta hai, phir **sab** de deta hai (baad me shart check nahi karta).
- `filter` **har** item ko check karta hai.

`takewhile` + `dropwhile` = `partition at first change` — sorted data par bohat useful (aur lazy, is liye
infinite streams par bhi chalta hai).
"""),
code("""
# ================= 10) pairwise (3.10+) aur batched (3.12+) =================

temps = [22, 25, 24, 28, 30, 27]

# pairwise: consecutive jodey -> differences, trends, validations ke liye perfect
print("pairwise      :", list(it_.pairwise(temps)))
diffs = [b - a for a, b in it_.pairwise(temps)]
print("din ka farq   :", diffs)
print("kitne din garm hua?", sum(1 for d in diffs if d > 0))

# is-sorted check ek line me
def is_sorted(seq):
    return all(a <= b for a, b in it_.pairwise(seq))
print("is_sorted([1,2,2,5]):", is_sorted([1, 2, 2, 5]))
print("is_sorted([1,9,2]) :", is_sorted([1, 9, 2]))

print("-" * 50)
# batched: fixed-size chunks (aakhri chunk chhota ho sakta hai)
ids = list(range(1, 11))
print("batched(3)    :", [list(b) for b in it_.batched(ids, 3)])

# Real use: API ko 4-4 ke batch me bhejna
for i, batch in enumerate(it_.batched(ids, 4), start=1):
    print(f"   POST /bulk  batch {i}: {list(batch)}")

# Python 3.13+ me strict=True bhi hai (aakhri chunk chhota ho to error)
try:
    print("batched strict:", [list(b) for b in it_.batched(ids, 3, strict=True)])
except (ValueError, TypeError) as e:
    print("batched strict-> ", type(e).__name__, ":", e)
"""),
]

cells += [
md("""
---
## 13. Ek "bara file" lazily parhna (`io.StringIO`)

Real duniya me tum `open(path)` karte ho aur `for line in f:` chalate ho — **ye already lazy hai**.
File object khud ek iterator hai! Poori file `read()` karna hi ghalti hai.

```python
# ❌ 10 GB file, 2 GB RAM -> MemoryError
data = open("huge.log").read()

# ❌ ye bhi poori file memory me laata hai
lines = open("huge.log").readlines()

# ✅ lazy: ek waqt me ek line
with open("huge.log") as f:
    for line in f:
        process(line)
```

Notebook me bahar ki file par depend nahi kar sakte (spec rule), is liye `io.StringIO` se simulate karte hain
— iska interface bilkul file jaisa hai.
"""),
code("""
# ---- Ek "bara" CSV-jaisa dataset banate hain (memory me, magar stream ki tarah parhenge) ----

def make_big_csv(rows=20_000):
    # StringIO me header + rows -- ye humari "file on disk" hai
    buf = io.StringIO()
    buf.write("order_id,city,amount,status\\n")
    cities = ["Lahore", "Karachi", "Islamabad", "Multan", "Quetta"]
    statuses = ["paid", "pending", "failed"]
    for i in range(rows):
        buf.write(f"{1000+i},{cities[i % 5]},{(i * 37) % 5000 + 100},{statuses[i % 3]}\\n")
    buf.seek(0)                    # cursor wapis shuru me -- warna kuch parha nahi jayega
    return buf

f = make_big_csv()
print("pehli 4 lines:")
for line in it_.islice(f, 4):
    print("  ", line.rstrip())
f.close()
print("\\n(gaur karo: sirf 4 lines parhin, poori 20,000 nahi)")
"""),
code("""
# ---- Lazy aggregation: 20,000 rows, memory O(1) ----
from collections import Counter

def csv_dicts(fileobj):
    # Stage 1: header se keys nikalo, phir har line ko dict me todo
    header = next(fileobj).strip().split(",")     # pehli line = header
    for line in fileobj:
        values = line.strip().split(",")
        if len(values) == len(header):            # corrupt line guard
            yield dict(zip(header, values, strict=True))

def typed(records):
    # Stage 2: amount ko int banao
    for rec in records:
        rec["amount"] = int(rec["amount"])
        yield rec

t0 = time.perf_counter()
f = make_big_csv()
total_by_city = Counter()
status_count  = Counter()
row_count = 0
for rec in typed(csv_dicts(f)):        # <- streaming: ek waqt me ek dict
    row_count += 1
    if rec["status"] == "paid":
        total_by_city[rec["city"]] += rec["amount"]
    status_count[rec["status"]] += 1
f.close()
elapsed = time.perf_counter() - t0

print(f"rows process kiye : {row_count:,}  ({elapsed*1000:.0f} ms)")
print("status breakdown  :", dict(status_count))
print("paid revenue/city :")
for city, amt in total_by_city.most_common():
    print(f"   {city:<10} Rs {amt:>10,}")
assert row_count == 20_000
"""),
md("""
### Output ka matlab

20,000 rows process hue magar memory me kabhi bhi **ek dict** se zyada nahi tha (plus chhote Counters).
Yehi code 20 million rows par bhi bilkul isi memory me chalega — sirf waqt zyada lagega.

**Interview tip:** *"Bari file kaise process karoge?"* → *"File object khud iterator hai; `for line in f`
se stream karoonga, generator pipeline lagaoonga, aur sirf aggregates memory me rakhoonga. `read()` /
`readlines()` kabhi nahi."*
"""),
]

cells += [
md("""
---
## 14. Common Mistakes / Gotchas — ek jagah sab

| # | Ghalti | Kya hota hai | Hal |
|---|---|---|---|
| 1 | Iterator ko do baar loop karna | Dusri baar khali | `list()` bana lo ya naya iterator |
| 2 | `len(generator)` | `TypeError` | `sum(1 for _ in gen)` (magar consume ho jayega) |
| 3 | `generator[0]` | `TypeError` | `next(gen)` ya `islice` |
| 4 | `list(infinite_gen)` | Hang / MemoryError | `islice` / `takewhile` / `break` |
| 5 | `groupby` bina `sorted` | Toote hue groups | Pehle usi key par sort karo |
| 6 | `groupby` group ko baad me use karna | Khali | Foran `list(group)` |
| 7 | Generator ko loop me late-binding closure ki tarah samajhna | Ghalat values | Neeche demo dekho |
| 8 | Exception generator ke andar se bahar aana | Generator mar jata hai | Andar `try/except` |
| 9 | `return` ki value expect karna | `for` ignore kar deta hai | `StopIteration.value` |
| 10 | `tee` ke baad original use karna | Undefined behaviour | Original chhod do |
| 11 | Generator me file band karna bhool jana | Resource leak | `with` andar rakho / `close()` |
| 12 | Genexp ke andar late-evaluated variable | Ghalat natija | Neeche demo dekho |
"""),
code("""
# ---- Gotcha #12: generator LAZY hai, is liye bahar ka variable badalne se natija badal jata hai ----

multiplier = 2
gen = (x * multiplier for x in range(5))     # abhi kuch calculate NAHI hua

multiplier = 10                              # ab badal diya!
print("natija:", list(gen), " <- 10 se multiply hua, 2 se nahi!")

# HAL 1: foran materialize karo
multiplier = 2
lst = [x * multiplier for x in range(5)]      # listcomp foran chalta hai
multiplier = 10
print("listcomp:", lst, " <- 2 se hi hua (safe)")

# HAL 2: value ko default argument me "freeze" kar do
def make_gen(m):
    return (x * m for x in range(5))          # m function ke scope me qaid ho gaya
multiplier = 2
g2 = make_gen(multiplier)
multiplier = 10
print("closure :", list(g2), " <- 2 se hua (safe)")
"""),
code("""
# ---- Gotcha #7: generator expression ka PEHLA `for` foran evaluate hota hai (baqi lazy) ----

data = [1, 2, 3]
gen = (x for x in data)      # `data` ka reference ABHI liya gaya

data = [100, 200]            # naam rebind kiya -> generator par asar NAHI
print("rebind ke baad:", list(gen), " <- purani list se aaya")

data2 = [1, 2, 3]
gen2 = (x for x in data2)
data2.append(4)              # SAME object mutate kiya -> generator par asar HOGA
print("mutate ke baad:", list(gen2), " <- 4 bhi aa gaya!")
"""),
code("""
# ---- Gotcha #11: generator ke andar file/resource -- `with` andar rakho ----

def bad_reader(text):
    f = io.StringIO(text)
    for line in f:
        yield line.strip()
    # Agar consumer beech me break kar de to f.close() kabhi nahi chalega!

def good_reader(text):
    with io.StringIO(text) as f:      # `with` generator ke andar -> close guaranteed
        for line in f:
            yield line.strip()
    # generator close/GC hone par `with` ka __exit__ chalta hai

sample = "line1\\nline2\\nline3\\nline4"

# Consumer beech me break karta hai
g = good_reader(sample)
for i, line in enumerate(g):
    if i == 1:
        break
print("beech me break kiya. generator close karte hain:")
g.close()                  # -> `with` ka cleanup chal jayega
print("cleanup ho gaya (koi resource leak nahi)")

print("counting without consuming? -- nahi ho sakta:")
g2 = good_reader(sample)
print("   count:", sum(1 for _ in g2))     # count mil gaya
print("   ab list:", list(g2), " <- khali, kyunki count ne consume kar liya")
"""),
]

cells += [
md("""
---
## 15. Real-World Problems

Chalo ab 4 asli masle hal karte hain — wahi cheezein jo kaam par milti hain.
"""),
md("""
### Problem 1 — Bari file me duplicate records dhoondo (memory O(unique))

**Scenario:** 5 GB transaction log hai. Duplicate `txn_id` dhoondne hain magar poori file RAM me nahi aa sakti.

**Approach:** Stream karo, ek `set` me dekhe hue IDs rakho. Memory sirf unique IDs ke barabar,
poori file ke barabar nahi. (Agar unique IDs bhi bohat zyada hon to Bloom filter / external sort chahiye.)
"""),
code("""
def find_duplicate_ids(lines):
    # Lazy generator: jaise hi duplicate mile, foran yield kar do (poori file ka intezar nahi)
    seen = set()                       # sirf IDs, poore records nahi
    for line in lines:
        txn_id = line.split(",", 1)[0]  # sirf pehla field parse karo (baqi ki zaroorat nahi)
        if txn_id in seen:
            yield txn_id                # duplicate mila
        else:
            seen.add(txn_id)

txn_log = io.StringIO('''\\
T100,ali,500
T101,sara,300
T102,bilal,900
T101,sara,300
T103,zain,150
T100,ali,500
T104,hina,700
''')

dups = list(find_duplicate_ids(txn_log))
print("duplicate txn ids:", dups)
assert dups == ["T101", "T100"]

# Pehla duplicate milte hi ruk jana (early exit) -- lazy hone ka faida
txn_log2 = io.StringIO("A,1\\nB,2\\nA,3\\nC,4\\nB,5\\n")
print("pehla duplicate  :", next(find_duplicate_ids(txn_log2)))
"""),
md("""
### Problem 2 — Infinite retry schedule (exponential backoff)

**Scenario:** API call fail ho to dobara try karo — magar har baar zyada intezar karo (0.5s, 1s, 2s, 4s...)
aur maximum cap lagao. Delay schedule ek **infinite generator** hai; caller jitne chahiye le le.

**Approach:** `itertools.count()` se attempt number, `min(base * 2**n, cap)` se delay. Generator hone ki
wajah se ye schedule reusable, testable, aur retry-logic se alag (decoupled) hai.
"""),
code("""
def backoff_delays(base=0.5, cap=30.0, jitter=0.0):
    # Infinite generator: attempt 0, 1, 2, ... ke liye delay
    for attempt in it_.count():
        delay = min(base * (2 ** attempt), cap)      # exponential, magar cap se zyada nahi
        yield round(delay + jitter, 3)

# Pehle 8 attempts ka schedule dekho (koi sleep nahi -- sirf numbers)
print("schedule:", list(it_.islice(backoff_delays(), 8)))
assert list(it_.islice(backoff_delays(base=1, cap=10), 6)) == [1, 2, 4, 8, 10, 10]

print()
# Ab isko ek fake flaky API ke sath use karte hain (real sleep bohat chhota rakha hai)
call_count = {"n": 0}
def flaky_api():
    call_count["n"] += 1
    if call_count["n"] < 4:                    # pehli 3 calls fail
        raise ConnectionError(f"attempt {call_count['n']} fail")
    return {"status": "ok", "attempt": call_count["n"]}

def call_with_retry(fn, max_attempts=6):
    # delays generator se milte hain -- retry logic saaf reh gaya
    delays = backoff_delays(base=0.001, cap=0.01)     # test ke liye micro-delays
    for attempt, delay in enumerate(it_.islice(delays, max_attempts), start=1):
        try:
            return fn()
        except ConnectionError as e:
            print(f"   attempt {attempt} fail ({e}) -> {delay}s baad retry")
            time.sleep(delay)
    raise RuntimeError("saare attempts fail ho gaye")

result = call_with_retry(flaky_api)
print("result:", result)
assert result["attempt"] == 4
"""),
md("""
### Problem 3 — Sliding window over a stream (moving average)

**Scenario:** Sensor se readings aa rahi hain (stream). Har naye reading par pichhle `k` ka average chahiye.
Poora data store nahi kar sakte.

**Approach:** `collections.deque(maxlen=k)` — jab naya item aata hai, purana khud nikal jata hai.
Generator hone ki wajah se ye infinite stream par bhi chalta hai, memory O(k).
"""),
code("""
from collections import deque

def moving_average(stream, k):
    window = deque(maxlen=k)          # maxlen = purana khud gir jata hai (O(1))
    total = 0.0
    for value in stream:
        if len(window) == k:
            total -= window[0]        # jo gir jayega usko total se ghatao
        window.append(value)
        total += value
        # sirf tab yield karo jab poora window bhar jaye
        if len(window) == k:
            yield round(total / k, 2)

readings = [10, 12, 23, 23, 16, 3, 15, 20]
avgs = list(moving_average(iter(readings), 3))
print("readings:", readings)
print("MA(3)   :", avgs)
assert avgs == [15.0, 19.33, 20.67, 14.0, 11.33, 12.67]

# Infinite stream par bhi chalta hai -- memory sirf 5 items
noisy_stream = (abs((i * 7919) % 100) for i in it_.count())
print("infinite stream ka MA(5), pehle 6:", list(it_.islice(moving_average(noisy_stream, 5), 6)))
"""),
md("""
### Problem 4 — Do sorted streams ko merge karna (external merge sort ka core)

**Scenario:** Do bari sorted files hain. Unko ek sorted stream me merge karna hai — bina dono ko RAM me laane ke.

**Approach:** Dono ke `next()` compare karo, chhota wala yield karo. Memory O(1).
Stdlib me ye already hai: `heapq.merge()` — aur wo N streams handle karta hai.
"""),
code("""
import heapq

def merge_two_sorted(a, b):
    # Manual implementation -- protocol samajhne ke liye
    ia, ib = iter(a), iter(b)
    x = next(ia, None)                     # sentinel None = stream khatam
    y = next(ib, None)
    while x is not None and y is not None:
        if x <= y:
            yield x
            x = next(ia, None)
        else:
            yield y
            y = next(ib, None)
    # jo bacha hua hai wo seedha de do
    while x is not None:
        yield x
        x = next(ia, None)
    while y is not None:
        yield y
        y = next(ib, None)

s1 = [1, 4, 7, 10, 13]
s2 = [2, 3, 8, 20]
merged = list(merge_two_sorted(s1, s2))
print("stream A:", s1)
print("stream B:", s2)
print("merged  :", merged)
assert merged == sorted(s1 + s2)

# Stdlib ka tareeqa: heapq.merge -- N streams, lazy, memory O(N)
s3 = [0, 5, 9]
print("heapq.merge (3 streams):", list(heapq.merge(s1, s2, s3)))
assert list(heapq.merge(s1, s2, s3)) == sorted(s1 + s2 + s3)

# key= bhi support karta hai -- magar har input stream USI key se sorted hona chahiye
words = [["fig", "apple"], ["kiwi", "banana"]]      # dono length ke hisab se sorted hain
print("key=len se merge:", list(heapq.merge(*words, key=len)))
assert list(heapq.merge(*words, key=len)) == ["fig", "kiwi", "apple", "banana"]
"""),
]

cells += [
md("""
---
# 16. LeetCode Problems

Ye section iterator/generator protocol ko **interview problems** par lagata hai. Char problems —
teen "design an iterator" type (jahan `__next__` khud likhna hai) aur ek bonus jo `itertools` se
elegantly hal hoti hai.
"""),
md("""
### LC 341. Flatten Nested List Iterator — Medium

**Link:** https://leetcode.com/problems/flatten-nested-list-iterator/

**Bayan (Roman Urdu):** Tumhe ek nested list di gayi hai, jaise `[[1,1],2,[1,1]]`. Har element ya to ek
**integer** hai ya khud ek **list** (jo aur nested ho sakti hai). Ek iterator class banao jiske `next()` aur
`hasNext()` methods flattened order me integers dein.

LeetCode `NestedInteger` interface deta hai jiske paas `isInteger()`, `getInteger()`, `getList()` hain —
hum wo class khud inline bana lenge taake code standalone chale.

**Approach 1 — Eager flatten (aasan, samajhne me saaf):**
1. Constructor me recursion se **poori** nested list ko ek flat list me kholo.
2. Ek index pointer rakho. `hasNext()` = `index < len(flat)`. `next()` = value do, index++.
- Trade-off: constructor O(N) time **aur** O(N) memory — poora data pehle hi flat ho jata hai.

**Approach 2 — Lazy stack (LeetCode ka "asli" jawab):**
1. Stack me list ke elements **ulta** daalo (taake top par pehla element ho).
2. `hasNext()` me: jab tak stack ka top ek **list** hai, use pop karo aur uske elements ulta push karo.
   Jab top integer ban jaye to `True`.
3. `next()` pehle `hasNext()` chalata hai (normalize), phir `stack.pop()`.
- Faida: constructor O(1)-ish, memory O(depth + breadth) — poora flatten nahi hota.

**Approach 3 — Generator (Pythonic):** `yield from` se recursive generator — code sab se chhota.

### Complexity

| Approach | Constructor | `next()` | `hasNext()` | Space |
|---|---|---|---|---|
| Eager flatten | O(N) | O(1) | O(1) | O(N) |
| Lazy stack | O(top-level) | **amortized O(1)** | amortized O(1) | O(N) worst (deep nesting) |
| Generator | O(1) | amortized O(1) | O(1) (peek buffer) | O(depth) |

`N` = total integers. Amortized O(1) kyunki har element stack par sirf ek baar push/pop hota hai.
"""),
code("""
# ================= LC 341: Flatten Nested List Iterator =================

class NestedInteger:
    # LeetCode ka interface -- hum khud bana rahe hain taake standalone chale.
    def __init__(self, value=None):
        # value int ho to integer node, list ho to list node
        if isinstance(value, list):
            self._list = [v if isinstance(v, NestedInteger) else NestedInteger(v) for v in value]
            self._int = None
        else:
            self._list = None
            self._int = value

    def isInteger(self):
        return self._int is not None

    def getInteger(self):
        return self._int

    def getList(self):
        return self._list

    def __repr__(self):
        return repr(self._int) if self.isInteger() else repr(self._list)


def build(raw):
    # Python list-of-(int|list) ko NestedInteger objects ki list me badalta hai
    return [NestedInteger(x) for x in raw]


# ---------- Approach 1: EAGER flatten ----------
class NestedIteratorEager:
    def __init__(self, nestedList):
        self._flat = []
        self._flatten(nestedList)       # constructor me hi poora khol diya
        self._i = 0

    def _flatten(self, items):
        for ni in items:
            if ni.isInteger():
                self._flat.append(ni.getInteger())
            else:
                self._flatten(ni.getList())      # recursion -- deeper level

    def hasNext(self):
        return self._i < len(self._flat)

    def next(self):
        val = self._flat[self._i]
        self._i += 1
        return val


# ---------- Approach 2: LAZY stack (optimal) ----------
class NestedIterator:
    def __init__(self, nestedList):
        # reversed() taake list ka PEHLA element stack ke TOP par aa jaye
        self._stack = list(reversed(nestedList))

    def hasNext(self):
        # Top ko "normalize" karo: jab tak top list hai, usko kholte jao
        while self._stack:
            top = self._stack[-1]
            if top.isInteger():
                return True                       # top ready hai
            self._stack.pop()                     # list thi -> nikaalo
            self._stack.extend(reversed(top.getList()))   # uske children ulta push
        return False                              # stack khali -> khatam

    def next(self):
        # hasNext() call karna zaroori hai (LeetCode guarantee deta hai magar safe rehte hain)
        if not self.hasNext():
            raise StopIteration("koi element baqi nahi")
        return self._stack.pop().getInteger()

    # Bonus: Python iterator protocol bhi de dete hain -> `for x in itr` chalega
    def __iter__(self):
        return self

    def __next__(self):
        if not self.hasNext():
            raise StopIteration
        return self._stack.pop().getInteger()


# ---------- Approach 3: GENERATOR (Pythonic) ----------
def flatten_nested(nestedList):
    # yield from se recursion -- 5 line me kaam
    for ni in nestedList:
        if ni.isInteger():
            yield ni.getInteger()
        else:
            yield from flatten_nested(ni.getList())


def drain(itr):
    # hasNext/next wale iterator ko list me convert karta hai (testing helper)
    out = []
    while itr.hasNext():
        out.append(itr.next())
    return out


# ================= TESTS =================
t1 = [[1, 1], 2, [1, 1]]
t2 = [1, [4, [6]]]
t3 = []                                  # khali
t4 = [[]]                                # sirf khali lists -> koi integer nahi
t5 = [[], [1], [], [2, [3, [4, []]]], 5]  # deep + khali mix

assert drain(NestedIteratorEager(build(t1))) == [1, 1, 2, 1, 1]
assert drain(NestedIterator(build(t1)))      == [1, 1, 2, 1, 1]
assert list(flatten_nested(build(t1)))       == [1, 1, 2, 1, 1]

assert drain(NestedIterator(build(t2))) == [1, 4, 6]
assert drain(NestedIterator(build(t3))) == []
assert drain(NestedIterator(build(t4))) == []          # edge case: khali lists
assert drain(NestedIterator(build(t5))) == [1, 2, 3, 4, 5]

# Teeno approaches ka jawab hamesha same hona chahiye
for raw in (t1, t2, t3, t4, t5):
    a = drain(NestedIteratorEager(build(raw)))
    b = drain(NestedIterator(build(raw)))
    c = list(flatten_nested(build(raw)))
    assert a == b == c, raw

print("LC 341 ke saare tests PASS")
print("  [[1,1],2,[1,1]] ->", drain(NestedIterator(build(t1))))
print("  [1,[4,[6]]]     ->", drain(NestedIterator(build(t2))))
print("  deep+khali mix  ->", drain(NestedIterator(build(t5))))
print("  for-loop (bonus)->", [x for x in NestedIterator(build(t2))])
"""),
md("""
### LC 284. Peeking Iterator — Medium

**Link:** https://leetcode.com/problems/peeking-iterator/

**Bayan (Roman Urdu):** Ek normal iterator ko wrap karo aur usme `peek()` method add karo jo **agli value
dikhaye magar iterator ko aage na barhaye**. `next()` aur `hasNext()` normal kaam karte rahein.

**Approach — one-element lookahead buffer:**
1. Andar ek `_buffer` rakho jisme "agli value" pehle se nikaal ke rakhi ho, aur ek flag `_has_buffer`.
2. `peek()`: agar buffer khali hai to underlying se ek value nikaal ke buffer me daal do; buffer return karo.
3. `next()`: agar buffer bhara hai to wahi return karo aur buffer khali kar do; warna underlying se lo.
4. `hasNext()`: `buffer bhara hai` **ya** underlying me kuch baqi hai.

**Ahem baat:** underlying iterator me "kuch baqi hai?" poochne ka koi tareeqa nahi hota — pata lagane ka
sirf ek zariya hai: `next()` maar ke dekho. Isi liye lookahead buffer chahiye. Isi ko **eager fetch** kehte hain.

**Gotcha:** `peek()` ke side-effect se underlying **already** aage barh jata hai. Agar underlying koi
expensive/one-shot stream hai (network) to `peek()` ka matlab hai "ek record pehle hi fetch ho gaya".

### Complexity
- `peek()`, `next()`, `hasNext()`: **O(1)** (amortized, sirf ek buffered element)
- Space: **O(1)** — chahe stream kitni bhi bari ho
"""),
code("""
# ================= LC 284: Peeking Iterator =================

class PeekingIterator:
    def __init__(self, iterator):
        # iterator = koi bhi Python iterator (list_iterator, generator, map object...)
        self._it = iter(iterator)
        self._buffer = None            # ek value ka lookahead
        self._has_buffer = False       # buffer valid hai ya nahi (None bhi valid value ho sakti hai)
        self._fill()                   # constructor me hi ek value pre-fetch (hasNext ke liye lazmi)

    def _fill(self):
        # Underlying se ek value nikaal ke buffer me daalne ki koshish
        if not self._has_buffer:
            try:
                self._buffer = next(self._it)
                self._has_buffer = True
            except StopIteration:
                self._has_buffer = False    # stream khatam

    def peek(self):
        # Agli value dikhao MAGAR aage na barho
        if not self._has_buffer:
            raise StopIteration("peek: koi element baqi nahi")
        return self._buffer

    def next(self):
        # Buffer wali value do, phir agli pre-fetch karo
        if not self._has_buffer:
            raise StopIteration("next: koi element baqi nahi")
        val = self._buffer
        self._has_buffer = False
        self._fill()                   # agla element buffer me
        return val

    def hasNext(self):
        return self._has_buffer

    # Python-friendly banate hain
    def __iter__(self):
        return self

    def __next__(self):
        if not self._has_buffer:
            raise StopIteration
        return self.next()


# ================= TESTS =================
# LeetCode ka example: nums = [1,2,3]
p = PeekingIterator(iter([1, 2, 3]))
assert p.next() == 1          # 1 mila, pointer 2 par
assert p.peek() == 2          # 2 dikha magar pointer wahin
assert p.peek() == 2          # dobara peek -> phir 2 (idempotent)
assert p.next() == 2          # ab 2 consume hua
assert p.next() == 3
assert p.hasNext() is False

# Edge case: khali iterator
e = PeekingIterator(iter([]))
assert e.hasNext() is False
try:
    e.peek()
    raise AssertionError("yahan StopIteration aana chahiye tha")
except StopIteration:
    pass

# Generator par bhi chalta hai (sirf iterator protocol chahiye)
p2 = PeekingIterator(x * x for x in range(1, 5))     # 1,4,9,16
seen = []
while p2.hasNext():
    seen.append((p2.peek(), p2.next()))
assert seen == [(1, 1), (4, 4), (9, 9), (16, 16)]

# Infinite stream par bhi -- kyunki space O(1) hai
p3 = PeekingIterator(it_.count(100))
assert p3.peek() == 100 and p3.next() == 100 and p3.peek() == 101

# Practical use: peek se "next group" decide karna (bina consume kiye)
def take_while_peek(pit, pred):
    out = []
    while pit.hasNext() and pred(pit.peek()):    # PEEK par faisla, phir consume
        out.append(pit.next())
    return out

p4 = PeekingIterator(iter([1, 2, 3, 10, 11, 4]))
print("LC 284 ke saare tests PASS")
print("  <5 wale prefix :", take_while_peek(p4, lambda x: x < 5))
print("  baqi           :", [x for x in p4])
"""),
md("""
### LC 173. Binary Search Tree Iterator — Medium

**Link:** https://leetcode.com/problems/binary-search-tree-iterator/

**Bayan (Roman Urdu):** Ek BST diya gaya hai. Aisa iterator banao jo `next()` par **in-order** (yani
**sorted**) tarteeb se agla chhota element de, aur `hasNext()` bataye ke aur element baqi hai ya nahi.
Shart: `next()` aur `hasNext()` **average O(1)** time me hon aur memory **O(h)** ho (h = tree ki height) —
yani poora tree flatten kar ke list me rakhna "cheating" hai.

**Approach 1 — Eager in-order (aasan):** poora in-order traversal kar ke list bana lo + index.
Space O(N) — LeetCode ki follow-up shart tordta hai, magar samajhne ke liye acha starting point.

**Approach 2 — Controlled recursion / stack (optimal):**
1. Constructor: root se shuru kar ke **saare left children** stack par push karo.
2. `next()`: stack se pop karo — **yehi** sab se chhota baqi node hai. Us node ke **right** child par jao
   aur us se neeche ke saare left children push karo. Node ki value return karo.
3. `hasNext()`: `len(stack) > 0`.

Kyun kaam karta hai? Stack me hamesha "wo ancestors jinki value abhi visit nahi hui" hote hain — yani
in-order traversal ko haath se pause/resume karna.

**Approach 3 — Generator (Pythonic):** in-order generator + `PeekingIterator` jaisa lookahead. Recursion
ka state Python khud manage kar leta hai — **is liye code sab se saaf hai**. Interview me pehle stack wala
batao (kyunki wo language-agnostic hai), phir "Python me main generator use karta" add karo.

### Complexity

| Approach | `next()` | `hasNext()` | Space |
|---|---|---|---|
| Eager list | O(1) | O(1) | O(N) ❌ |
| Stack | **amortized O(1)** (worst O(h)) | O(1) | **O(h)** ✅ |
| Generator | amortized O(1) | O(1) | O(h) ✅ |

Amortized O(1) kyunki poore traversal me har node exactly ek baar push aur ek baar pop hota hai → N
operations / N calls = O(1) per call.
"""),
code("""
# ================= LC 173: Binary Search Tree Iterator =================

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build_bst(values):
    # Values ko ek ek kar ke BST me insert karta hai (test trees banane ke liye)
    root = None
    for v in values:
        node = TreeNode(v)
        if root is None:
            root = node
            continue
        cur = root
        while True:
            if v < cur.val:
                if cur.left is None:
                    cur.left = node
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = node
                    break
                cur = cur.right
    return root


# ---------- Approach 1: EAGER in-order ----------
class BSTIteratorEager:
    def __init__(self, root):
        self._vals = []
        self._inorder(root)        # poora tree ek list me (space O(N))
        self._i = 0

    def _inorder(self, node):
        if node is None:
            return
        self._inorder(node.left)   # left
        self._vals.append(node.val)  # khud
        self._inorder(node.right)  # right

    def next(self):
        v = self._vals[self._i]
        self._i += 1
        return v

    def hasNext(self):
        return self._i < len(self._vals)


# ---------- Approach 2: STACK (optimal, space O(h)) ----------
class BSTIterator:
    def __init__(self, root):
        self._stack = []
        self._push_left_spine(root)     # sab se chhote tak ka raasta stack par

    def _push_left_spine(self, node):
        # node se shuru kar ke jitne left children hain sab push
        while node:
            self._stack.append(node)
            node = node.left

    def next(self):
        # Stack ka top = agla sab se chhota (in-order successor)
        node = self._stack.pop()
        # Uske right subtree ka left-spine ab stack par aana chahiye
        if node.right:
            self._push_left_spine(node.right)
        return node.val

    def hasNext(self):
        return len(self._stack) > 0


# ---------- Approach 3: GENERATOR (Pythonic) ----------
def bst_inorder(node):
    # Lazy in-order generator -- recursion ka state Python sambhalta hai
    if node is None:
        return
    yield from bst_inorder(node.left)
    yield node.val
    yield from bst_inorder(node.right)


class BSTIteratorGen:
    def __init__(self, root):
        # Generator ko PeekingIterator style buffer ke sath wrap kiya
        self._gen = bst_inorder(root)
        self._buf = None
        self._has = False
        self._advance()

    def _advance(self):
        try:
            self._buf = next(self._gen)
            self._has = True
        except StopIteration:
            self._has = False

    def next(self):
        v = self._buf
        self._advance()
        return v

    def hasNext(self):
        return self._has


# ================= TESTS =================
def drain_bst(itr):
    out = []
    while itr.hasNext():
        out.append(itr.next())
    return out

# LeetCode example: root = [7,3,15,null,null,9,20]
root = TreeNode(7, TreeNode(3), TreeNode(15, TreeNode(9), TreeNode(20)))

itr = BSTIterator(root)
assert itr.next() == 3        # LeetCode ka expected sequence
assert itr.next() == 7
assert itr.hasNext() is True
assert itr.next() == 9
assert itr.hasNext() is True
assert itr.next() == 15
assert itr.hasNext() is True
assert itr.next() == 20
assert itr.hasNext() is False

# Teeno approaches: jawab sorted order hona chahiye
for vals in ([7, 3, 15, 9, 20], [50], [], [5, 3, 8, 1, 4, 7, 9], [1, 2, 3, 4, 5]):
    r = build_bst(vals)
    a = drain_bst(BSTIteratorEager(r))
    b = drain_bst(BSTIterator(r))
    c = drain_bst(BSTIteratorGen(r))
    assert a == b == c == sorted(vals), vals

print("LC 173 ke saare tests PASS")
print("  tree [7,3,15,null,null,9,20] ->", drain_bst(BSTIterator(root)))
print("  skewed tree (1..5)           ->", drain_bst(BSTIterator(build_bst([1, 2, 3, 4, 5]))))
print("  khali tree                   ->", drain_bst(BSTIterator(build_bst([]))))
"""),
md("""
### LC 1291. Sequential Digits — Medium *(bonus — `itertools` ka elegant use)*

**Link:** https://leetcode.com/problems/sequential-digits/

**Bayan (Roman Urdu):** "Sequential digits" wo number hai jiske har digit apne pichhle digit se **exactly 1
zyada** ho (jaise `123`, `4567`, `89`). `[low, high]` range me aane wale saare aise numbers **sorted** order
me return karo.

**Approach — brute force par sochna chhod do, generate karo:**
Aise numbers total **sirf 36** hain (1 se 9 tak ke digits, length 2 se 9 tak) — kyunki start digit aur
length dono limited hain. To saare generate karo aur filter karo.

1. String `"123456789"` par har possible **contiguous slice** (length 2..9) lo.
2. Usko `int` banao.
3. `low <= n <= high` wale rakho, `sorted()` kar do.

`itertools.combinations` ki zaroorat nahi — simple nested slicing kaafi hai, aur `itertools.chain` se
generation lazy rakh sakte ho.

**Kyun ye "iterator" notebook me?** Kyunki ye us soch ki misaal hai: *"answer space chhota hai → generate
karo (lazily), search na karo"*. Ye generator-first thinking hai.

### Complexity
- Time: **O(1)** — candidates fixed 36 hain (`sorted` par bhi O(36 log 36)). Input size par depend nahi.
- Space: **O(1)** (output ke ilawa)
"""),
code("""
# ================= LC 1291: Sequential Digits (bonus) =================

DIGITS = "123456789"

def sequential_candidates():
    # Lazy generator: chhoti length pehle -> natija roughly sorted aata hai
    for length in range(2, 10):                     # length 2 se 9 tak
        for start in range(0, 10 - length):          # kahan se slice shuru ho
            yield int(DIGITS[start:start + length])

def sequentialDigits(low, high):
    # Generator pipeline: generate -> filter -> sort
    return sorted(n for n in sequential_candidates() if low <= n <= high)

# Total candidates gin lete hain -- sirf 36
all_cands = list(sequential_candidates())
print("total sequential numbers:", len(all_cands))
print("pehle 12                :", all_cands[:12])
assert len(all_cands) == 36

# ================= TESTS (LeetCode examples) =================
assert sequentialDigits(100, 300) == [123, 234]
assert sequentialDigits(1000, 13000) == [1234, 2345, 3456, 4567, 5678, 6789, 12345]
assert sequentialDigits(10, 100) == [12, 23, 34, 45, 56, 67, 78, 89]
assert sequentialDigits(1, 9) == []                 # single digit count nahi hota
assert sequentialDigits(123, 123) == [123]          # exact match
assert sequentialDigits(123456789, 123456789) == [123456789]   # sab se bara

print("LC 1291 ke saare tests PASS")
print("  (100, 300)      ->", sequentialDigits(100, 300))
print("  (1000, 13000)   ->", sequentialDigits(1000, 13000))
"""),
]

cells += [
md("""
---
# 17. Interview Questions & Answers

**Q1. Iterable aur iterator me farq?**
Iterable ke paas `__iter__()` hota hai — us se iterator banaya ja sakta hai (`list`, `str`, `dict`).
Iterator ke paas `__iter__()` **aur** `__next__()` dono hote hain, wo apni position ka state rakhta hai,
aur **one-shot** hota hai. Har iterator iterable hai; har iterable iterator nahi.

**Q2. `StopIteration` exception hai — phir `for` loop crash kyun nahi hota?**
`for` loop andar se `StopIteration` ko pakadta hai aur usko "loop khatam" ka signal samajh kar `break`
kar deta hai. Ye control-flow signal hai, error nahi.

**Q3. Generator aur normal function me farq?**
Normal function `return` par ek dafa value de kar **khatam** ho jata hai (local state gayab). Generator
function me `yield` hota hai — call karne par body chalti nahi, ek generator object milta hai; har `next()`
par body `yield` tak chal kar **suspend** ho jati hai aur locals mehfooz rehte hain.

**Q4. Generator aur list me kya farq, aur kab kaun sa?**
List poora data memory me rakhti hai (O(N)), reusable hai, indexing/`len()` support karti hai.
Generator lazy hai (O(1) memory), one-shot hai, indexing/`len()` nahi. Bara/infinite/streaming data →
generator. Chhota data + reuse/indexing → list.

**Q5. `yield` vs `return` generator me?**
`yield` value deta hai aur function suspend karta hai. `return` generator ko **band** kar deta hai; uski
value `StopIteration.value` me chali jati hai (jo `for` loop ignore karta hai).

**Q6. `yield from` ka faida sirf syntax hai?**
Nahi. Chhote code ke ilawa wo `send()`, `throw()`, aur sub-generator ki `return` value ko **properly
forward** karta hai. Manual `for x in sub: yield x` ye sab nahi karta.

**Q7. Generator expression aur list comprehension me farq?**
Brackets: `()` vs `[]`. Listcomp foran poori list banati hai; genexp ek lazy iterator deta hai.
`sum(x*x for x in big)` memory-efficient hai, `sum([x*x for x in big])` nahi.

**Q8. Ek generator ko do baar loop kaise karein?**
Nahi kar sakte. Options: (a) `data = list(gen)` bana lo, (b) generator **function** ko dobara call karo
(naya generator banega), (c) `itertools.tee()` (magar buffering memory leta hai).

**Q9. `itertools.groupby` aur SQL `GROUP BY` me farq?**
`groupby` sirf **consecutive** same-key items group karta hai. Is liye usi key par `sorted()` karna zaroori
hai. Warna ek hi key ke kai toote hue groups milenge.

**Q10. `next(gen)` aur `gen.send(None)` me farq?**
Koi farq nahi — dono generator ko aage barhate hain aur `yield` expression ki value `None` set karte hain.
`send(x)` se `x` value inject hoti hai, magar pehle generator **primed** hona chahiye.

**Q11. `gen.close()` kya karta hai?**
Generator ke current `yield` par `GeneratorExit` raise karta hai. Generator use pakad kar cleanup kar sakta
hai (`try/finally` ya `except GeneratorExit`). Agar generator `GeneratorExit` ke baad `yield` kare to
`RuntimeError` aata hai.

**Q12. Generator me exception handle na ho to kya hota hai?**
Exception caller tak propagate hoti hai aur generator **band** ho jata hai — dobara `next()` par
`StopIteration` milega. Resilient generator ke liye loop ke andar `try/except` lagao.

**Q13. `zip()`, `map()`, `filter()` Python 3 me list dete hain ya iterator?**
Iterator. Is liye do baar loop nahi hota aur `len()` nahi chalta. Python 2 me ye lists dete the — ye
Py2→Py3 ka classic bug source hai.

**Q14. `itertools.islice` aur normal slicing `[a:b]` me farq?**
`islice` **kisi bhi** iterator par chalta hai aur lazy hai, magar negative indices support nahi karta
(kyunki aakhir kahan hai ye pata nahi). Normal slicing sirf sequences par chalta hai, negative allow hai,
aur naya object banata hai.

**Q15. `tee()` ki memory cost kya hai?**
`O(largest gap)` — agar ek copy N items aage nikal jaye to `tee` andar N items buffer karta hai. Agar dono
copies ko poora ghumana hai to `list(gen)` hi behtar aur saaf hai.

**Q16. Lazy evaluation ka nuksan kya hai?**
(a) Debugging mushkil — error consume karte waqt aata hai, define karte waqt nahi.
(b) Do baar traverse nahi. (c) `len()` nahi. (d) Agar bahar ka mutable state badal jaye to natija badal
sakta hai (deferred evaluation trap). (e) Resource (file) generator ke andar khula reh sakta hai.

**Q17. "Generator pipeline" ka faida ek line me?**
Memory O(1) + composable stages + early exit sasta. 50 GB file 100 MB RAM me process ho jati hai.

**Q18. `iter()` ka do-argument form kya hai?**
`iter(callable, sentinel)` — `callable()` ko baar baar call karta hai jab tak wo `sentinel` return na kare.
File ko fixed-size chunks me parhne ka classic idiom: `iter(lambda: f.read(4096), b"")`.

**Q19. Generator thread-safe hai?**
Nahi. Ek generator ko kai threads se `next()` karna race condition hai (`ValueError: generator already
executing` bhi mil sakta hai). Har thread ko apna generator do, ya lock lagao, ya `queue.Queue` use karo.

**Q20. Generator function me `yield` ho magar wo kabhi na chale — phir bhi generator hai?**
Haan. `yield` ki **maujoodgi** compile-time par function ko generator bana deti hai, chahe wo line kabhi
execute na ho. Is liye `def f(): return; yield` ek khali generator hai, `None` return karne wala function nahi.
"""),
code("""
# ---- Q18 ka demo: iter() ka do-argument (sentinel) form ----

# Misaal 1: file ko fixed chunks me parhna (classic idiom)
f = io.StringIO("A" * 25)                  # 25 characters ka "file"
chunks = list(iter(lambda: f.read(10), ""))  # jab read("") de -> ruk jao
print("chunks:", [len(c) for c in chunks], "->", chunks)
assert [len(c) for c in chunks] == [10, 10, 5]

# Misaal 2: fake queue se "poll" karna jab tak sentinel na mile
queue_data = iter([3, 7, 9, None, 11])      # None = "bas"
polled = list(iter(lambda: next(queue_data), None))
print("sentinel se pehle:", polled)
assert polled == [3, 7, 9]

# ---- Q20 ka demo: yield ki maujoodgi function ko generator bana deti hai ----
def never_yields():
    return                    # foran return
    yield                     # ye line kabhi nahi chalti -- magar function generator hai!

r = never_yields()
print("type:", type(r).__name__, "| values:", list(r))
import inspect
assert inspect.isgeneratorfunction(never_yields)
print("inspect.isgeneratorfunction:", inspect.isgeneratorfunction(never_yields))
"""),
]

cells += [
md("""
---
# 18. Practice Exercises (khud karo)

Har exercise ke liye function likho aur apne `assert` se test karo. **Hint** phanse par dekho.

**1. `take(n, iterable)`** — kisi bhi iterable se pehli `n` values ki list do (agar kam hain to jitni hain).
   *Hint:* `itertools.islice`.

**2. `chunked(iterable, size)`** — generator jo lists ke chunks de: `chunked(range(7), 3)` →
   `[0,1,2], [3,4,5], [6]`. `list()` me poora data na aaye.
   *Hint:* `itertools.islice` ko `while True` loop me chalao aur khali chunk par `break`, ya `batched`
   se compare karo.

**3. `unique(iterable)`** — order barqarar rakhte hue duplicates hatao, **lazy** generator banao.
   Bonus: `key=` parameter add karo (jaise `key=str.lower`).
   *Hint:* `seen = set()`; unhashable items ke liye kya karoge?

**4. `windowed(iterable, n)`** — sliding windows: `windowed([1,2,3,4], 2)` → `(1,2), (2,3), (3,4)`.
   *Hint:* `deque(maxlen=n)`; `n=2` par `itertools.pairwise` se apna jawab verify karo.

**5. `interleave(*iterables)`** — baari baari ek ek item lo: `interleave([1,2,3], "abc")` →
   `1, 'a', 2, 'b', 3, 'c'`. Unequal lengths handle karo (chhoti khatam ho jaye to usko chhod do).
   *Hint:* `zip_longest` + sentinel, ya `cycle` of iterators.

**6. `count_lines_matching(fileobj, pattern)`** — bina poori file memory me laane ke un lines ki ginti do
   jinme `pattern` ho. `io.StringIO` se test karo.
   *Hint:* `sum(1 for line in f if pattern in line)`.

**7. `primes()`** — infinite generator jo prime numbers de. `islice` se pehle 20 nikalo aur verify karo.
   *Hint:* trial division kaafi hai; optimize: sirf `sqrt(n)` tak, aur mile hue primes se divide karo.

**8. `flatten_iter(nested, depth=None)`** — recursive flatten magar `depth` limit ke sath.
   `depth=1` sirf ek level khole. Strings ko atomic samjho (warna infinite recursion!).
   *Hint:* `isinstance(x, str)` ka special case pehle check karo.

**9. `batched_api_sender(records, batch_size)`** — records ko batches me "bhejo" (print karo) aur
   har batch ka summary dict yield karo: `{"batch": 1, "count": 4}`.
   *Hint:* `itertools.batched`.

**10. `TopN` iterator class** — stream se guzarte hue top-N sab se bari values yaad rakho, memory O(N).
   `__iter__` sorted descending order de.
   *Hint:* `heapq` (min-heap of size N) — ya `heapq.nlargest` se apna jawab check karo.

**11. (Challenge) `merge_sorted(*streams, key=None)`** — N sorted streams ko merge karo, lazy, memory O(N).
   `heapq.merge` se apna jawab compare karo — magar khud implement karo.
   *Hint:* min-heap me `(key(value), stream_index, value, iterator)` tuples rakho.

**12. (Challenge) `Peekable` class** — `PeekingIterator` ka general version jo `peek(n)` support kare
   (agli `n` values dikhaye bina consume kiye).
   *Hint:* buffer `deque` banao aur zaroorat ke mutabiq `_fill(n)` karo.
"""),
code("""
# ---- Self-check helper: apne jawab yahan test karo ----
# Neeche exercise 1 aur 3 ke solutions hain -- baqi khud karo!

def take(n, iterable):
    # Sab se saaf tareeqa: islice lazy hai aur kisi bhi iterable par chalta hai
    return list(it_.islice(iterable, n))

assert take(3, range(10)) == [0, 1, 2]
assert take(5, [1, 2]) == [1, 2]              # kam items -> jitne hain
assert take(0, range(10)) == []               # edge case
assert take(3, it_.count()) == [0, 1, 2]      # infinite par bhi chalta hai
print("exercise 1 (take) PASS ->", take(4, "PYTHON"))


def unique(iterable, key=None):
    # Lazy dedupe, order preserve
    seen = set()
    for item in iterable:
        k = item if key is None else key(item)
        if k not in seen:
            seen.add(k)
            yield item                        # pehli baar mila -> de do

assert list(unique([1, 3, 1, 2, 3, 4, 2])) == [1, 3, 2, 4]
assert list(unique("mississippi")) == ["m", "i", "s", "p"]
assert list(unique(["A", "a", "B", "b"], key=str.lower)) == ["A", "B"]
# lazy hone ka saboot: infinite stream par bhi chalta hai
assert take(4, unique(it_.cycle([5, 5, 6, 7, 6, 8]))) == [5, 6, 7, 8]
print("exercise 3 (unique) PASS ->", list(unique([1, 3, 1, 2, 3, 4, 2])))

print()
print("Baqi 10 exercises khud karo -- upar ke hints padho!")
"""),
]

cells += [
md("""
---
# 19. Summary / Cheat-sheet

## Protocol ek nazar me

```
iterable  --iter()-->  iterator  --next()-->  value ... StopIteration
```
- **Iterable** = `__iter__`  ·  **Iterator** = `__iter__` + `__next__`
- Iterator **one-shot** hai. `for` loop = `iter()` + `next()` loop + `StopIteration` par `break`.

## Iterator banane ke 3 tareeqe

| Tareeqa | Code | Kab |
|---|---|---|
| Class | `__iter__` + `__next__` + `raise StopIteration` | Complex state, reusable iterable chahiye |
| Generator function | `def g(): yield x` | **99% cases** — sab se saaf |
| Generator expression | `(f(x) for x in it)` | One-liner transformation/filter |

## Generator ke methods

| Call | Kaam |
|---|---|
| `next(g)` / `g.send(None)` | Aage barhao |
| `g.send(v)` | `yield` ki jagah `v` inject karo (**pehle prime karo!**) |
| `g.throw(Exc)` | Andar exception raise karo |
| `g.close()` | `GeneratorExit` → cleanup |
| `yield from sub` | Delegation (send/throw/return sab forward) |

## `itertools` cheat-sheet

```python
# Infinite (islice/takewhile se kaato!)
count(10, 2)          # 10, 12, 14, ...
cycle("abc")          # a, b, c, a, b, c, ...
repeat("x", 3)        # x, x, x

# Jodna / kaatna
chain([1,2], [3])              # 1, 2, 3
chain.from_iterable([[1],[2]]) # 1, 2      (1-level flatten)
islice(it, 2, 9, 2)            # lazy slicing (negative index NAHI)
tee(it, 2)                     # 2 copies (buffer memory!)
zip_longest(a, b, fillvalue=0) # chhoti ko bharo

# Filter / transform
compress(data, [1,0,1])        # mask se filter
filterfalse(pred, it)          # filter ka ulta
takewhile(pred, it)            # pehli False par RUK jao
dropwhile(pred, it)            # pehli False tak drop, phir SAB
starmap(pow, [(2,3)])          # func(*tuple)
accumulate(nums)               # running sum  (func=, initial= bhi)
groupby(SORTED_it, key)        # consecutive groups -- SORT LAZMI

# Windows / chunks
pairwise([1,2,3])              # (1,2), (2,3)          3.10+
batched(range(7), 3)           # (0,1,2), (3,4,5), (6,) 3.12+

# Combinatorics
product(a, b)                  # nested loops    len(a)*len(b)
product("01", repeat=3)        # n-fold          len**n
permutations("abc", 2)         # tarteeb MATTERS  n!/(n-r)!
combinations("abc", 2)         # tarteeb nahi     C(n,r)
combinations_with_replacement("abc", 2)   # repeat allowed
```

## Lazy vs Eager faisla

| Chahiye | Use |
|---|---|
| `len()`, indexing, sorting, dobara loop | **list** |
| Bara/infinite data, streaming, sirf ek traversal | **generator** |
| Pehli matching value | `next(x for x in it if cond)` |
| Poora aggregate (`sum`/`max`/`Counter`) | genexp + aggregate function |

## Top 8 gotchas

1. Iterator do baar loop → dusri baar **khali**
2. `zip`/`map`/`filter`/`enumerate` = iterators (Py3)
3. `len(gen)` / `gen[0]` → `TypeError`
4. `list(infinite_gen)` → hang
5. `groupby` bina `sorted` → toote groups; group **expire** ho jata hai
6. Genexp lazy hai → bahar ka variable badal gaya to natija badal jayega
7. `tee` ke baad original chhod do; gap = memory
8. Generator ke andar file? `with` **andar** rakho, warna leak

## LeetCode is notebook se

| LC | Title | Difficulty | Core idea |
|---|---|---|---|
| 341 | Flatten Nested List Iterator | Medium | Lazy stack / `yield from` recursion |
| 284 | Peeking Iterator | Medium | One-element lookahead buffer |
| 173 | Binary Search Tree Iterator | Medium | Left-spine stack, amortized O(1), space O(h) |
| 1291 | Sequential Digits | Medium | Answer space chhota → generate, search nahi |

## Interview one-liners

- *"`for` loop kaise chalta hai?"* → `iter()` → `next()` loop → `StopIteration` par break.
- *"Generator kyun?"* → Lazy: memory O(1), pehli value foran, infinite sequences mumkin.
- *"10 GB file?"* → Generator pipeline; sirf aggregates memory me.
- *"`yield from` kyun?"* → Recursion saaf + send/throw/return forwarding.

---
### Aage kya?
Agla notebook: **02 — Closures, Decorators aur Functional Python** (`functools`, `yield` ke bad ab
higher-order functions).
"""),
]

save(PATH, cells)





