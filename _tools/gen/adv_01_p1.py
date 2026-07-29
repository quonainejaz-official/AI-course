import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

CELLS = []
A = CELLS.append

A(md("""
# Python Memory Model, References, GC aur Performance Internals

**Level:** Advanced &nbsp;|&nbsp; **Folder:** `Python/Advance` &nbsp;|&nbsp; **Python:** 3.14 (CPython)

Ye notebook Python ke *andar* jhankne ke liye hai. Zyada tar log Python 5 saal likhte hain
magar ye nahi jaante ke `a = b` ne asal me kya kiya, `copy()` kaafi tha ya `deepcopy()`,
memory kahan lag rahi hai, aur code slow kyun hai. Yahan hum wohi khaali jagah bharenge.

## Is notebook me kya seekhenge

- **Names vs objects vs references** — Python me "variable" naam ki cheez asal me kya hai
- **Assignment semantics** — rebinding vs mutation (interview ka favourite)
- **Reference counting** — `sys.getrefcount`, immortal objects (PEP 683)
- **Identity** — `id()`, `is` vs `==`, id-reuse ka dhoka
- **Small int cache** aur **string interning** (`sys.intern`)
- **Mutable vs immutable** ki asli wajah (hashing, sharing, safety)
- **Function argument passing** — "pass-by-object-reference" ke 3 proofs
- **Mutable default argument trap** — deep dive with `__defaults__`
- **Shallow vs deep copy internals** — `copy`, `__copy__`, `__deepcopy__`, recursive structures, memo
- **Garbage collector** — refcount + cycle detector, generational/incremental, `gc` module, `__del__` ke khatray
- **weakref** & `WeakValueDictionary` — cache jo memory leak na kare
- **`__slots__`** — memory aur speed dono ki measurement
- **`sys.getsizeof` vs real size** — recursive sizer khud likhenge
- **CPython object overhead**, list over-allocation
- **list vs tuple vs array vs deque** memory comparison
- **String concat in loop vs `join`** — `timeit` se sabit
- **`dis` se bytecode peek**, constant folding / peephole optimizer
- **Local vs global lookup speed** — `LOAD_FAST` vs `LOAD_GLOBAL`
- **LeetCode:** 138 (Copy List with Random Pointer), 133 (Clone Graph), 146 (LRU Cache)

## Prerequisites

Functions, classes, dict/list/tuple, decorators ki basic samajh. `timeit` ka naam suna ho.

> **Note:** Is notebook me kuch numbers (refcount, memory sizes, timings) tumhare machine par
> thore mukhtalif aa sakte hain — ye normal hai. Concept dekho, exact number ratna nahi.
"""))

A(md("""
---
## 1. Names vs Objects vs References

### Kya hai
Python me **variable ek dabba (box) nahi hai** jis me value rakhi ho. Python me:

- **Object** = heap par asli cheez (value + type + refcount)
- **Name** = ek *label / sticky note* jo kisi object par chipka hua hai
- **Reference** = us label ka object tak pointer

C/Java ka mental model: `int x = 5` → memory me `x` naam ka dabba, us me 5.
Python ka mental model: heap me `5` naam ka object, aur `x` label us par chipka.

### Kyun important hai
Isi ek baat se ye sab samajh aata hai: `a = b` copy nahi karta, list function me
"badal" kyun jaati hi, `is` aur `==` me farq kya hai, aur deep copy kab chahiye.

### Syntax
```python
x = 10        # object 10 banao (ya cached lo), naam x us par chipkao
y = x         # naya object NAHI — sirf ek aur label usi object par
```
"""))

A(code(r"""
# Ek object, do naam --------------------------------------------------------
a = [10, 20, 30]      # heap par ek list object bana; naam 'a' us par chipka
b = a                 # koi copy NAHI hui — 'b' bhi usi object par chipak gaya

print("a       =", a)
print("b       =", b)
print("id(a)   =", id(a))          # id() = object ka unique pehchan (CPython me memory address)
print("id(b)   =", id(b))
print("a is b  =", a is b)         # is  -> same object? -> True
print("a == b  =", a == b)         # == -> same value?  -> True

# ab object ko MUTATE karo (object ke andar tabdeeli)
b.append(40)
print("\nb.append(40) ke baad:")
print("a =", a, "  <-- 'a' bhi badal gaya, kyunki object aik hi hai")
print("b =", b)

# lesson: naam copy hote hain, objects nahi
"""))

A(md("""
### Output ka matlab
`id(a) == id(b)` aur `a is b == True` ka matlab: heap par **ek hi list** hai jis par do labels
lage hain. Is liye `b.append(40)` ne `a` ko bhi "badla" — asal me `a` badla hi nahi,
**object** badla, aur dono naam usi object ko dekh rahe hain.

### Gotcha
Beginners kehte hain "list function me by-reference jaati hai, int by-value". **Ghalat.**
Dono barabar reference se jaate hain — farq sirf ye hai ke `int` **immutable** hai, is liye
usay badalna mumkin nahi, sirf naam ko naye object par chipkaya ja sakta hai.

### Interview tip
Bolo: *"Python names are references to heap objects; assignment binds a name, it never copies
the object. Behaviour differences come from mutability, not from a value/reference distinction."*
"""))

A(md("""
---
## 2. Assignment Semantics — Rebinding vs Mutation

### Kya hai
Do bilkul mukhtalif operations jo dekhne me ek jaise lagte hain:

| Operation | Naam ka kaam | Object ka kaam | Doosre naamon par asar |
|---|---|---|---|
| `x = new_value` | naam ko **naye object** par chipkao (**rebinding**) | purana object jaisa tha waisa | **koi asar nahi** |
| `x.append(1)` / `x[0]=1` | naam wahi rehta | object **andar se badla** (**mutation**) | **sab ko dikhta hai** |

`x += y` dhoka hai: list par ye *mutation* (`__iadd__`, in-place extend) hai,
int/tuple/str par *rebinding* (naya object) hai.
"""))

A(code(r"""
# Rebinding vs Mutation ka farq -------------------------------------------
lst1 = [1, 2]
lst2 = lst1
print("shuru me:      lst1", lst1, " lst2", lst2, " same object?", lst1 is lst2)

lst1 = lst1 + [3]            # + naya object banata hai -> REBINDING
print("lst1 = lst1+[3]:  lst1", lst1, " lst2", lst2, " same object?", lst1 is lst2)

lst3 = [1, 2]
lst4 = lst3
lst3 += [3]                  # += list par __iadd__ = IN-PLACE MUTATION
print("lst3 += [3]:      lst3", lst3, " lst4", lst4, " same object?", lst3 is lst4)

# int par += hamesha rebinding (int immutable hai)
n = 5
before = id(n)
n += 1
print("\nint: id badla?", before != id(n), "-> yaani naya object bana")

# tuple ke andar list: tuple immutable, magar uska element mutable ho sakta hai
t = (1, [2, 3])
t[1].append(4)               # ye JAIZ hai -> list ko mutate kiya, tuple ko nahi
print("tuple ke andar list mutate:", t)
try:
    t[0] = 99                # ye NAJAIZ -> tuple ka slot badalna
except TypeError as e:
    print("t[0] = 99 ->", type(e).__name__, ":", e)
"""))

A(md("""
### Output ka matlab
`lst1 = lst1 + [3]` ke baad `lst1 is lst2` **False** ho gaya — kyunki `+` ne **naya** object
banaya aur `lst1` naam us naye par chala gaya; `lst2` purane par hi hai.
Magar `lst3 += [3]` ke baad dono ab bhi **same object** hain aur `lst4` me bhi 3 nazar aayega.

### Common mistake
Function ke andar `param = param + [x]` likh kar log samajhte hain caller ki list update ho gayi.
Nahi hui — wo rebinding thi. `param.append(x)` ya `param += [x]` karte to hoti.

### Interview tip
*"`+` returns a new object, `+=` calls `__iadd__` which mutates in place for mutable types and
falls back to `__add__` + rebinding for immutable types."*
"""))

A(md("""
---
## 3. Reference Counting — CPython memory management ki reeh ki haddi

### Kya hai
Har CPython object ke sath ek **counter** hota hai: kitne references us par lage hain.
Counter `0` hote hi object ki memory **foran** free ho jaati hai (deterministic!).

### Kyun
Ye "instant cleanup" hai — is liye Python me file band karne ke liye GC ka intezar nahi karna parta
(magar phir bhi `with` use karo!). Cycles is se hal nahi hote — us ke liye alag cycle collector hai (section 10).

### Syntax
```python
sys.getrefcount(obj)   # NOTE: khud argument bhi ek reference banata hai -> jawab me +1
```

### Immortal objects (PEP 683, Python 3.12+)
`None`, `True`, `False`, chhote ints, chhoti strings ab **immortal** hain — unka refcount
jaan boojh kar ek bohat bara constant (`3221225472` jaisa) rakh diya gaya hai taake
multi-threaded programs me counter par lock lagane ki zaroorat na pare. Is liye unka
refcount dekh kar ghabraana nahi.
"""))

A(code(r"""
import sys

# Normal object ka refcount ---------------------------------------------------
data = {"k": "v"}
print("1 naam:            ", sys.getrefcount(data), " (+1 kyunki argument bhi reference hai)")

alias = data
print("2 naam:            ", sys.getrefcount(data))

holder = [data, data]                 # list ke andar 2 references
print("list me 2 aur:     ", sys.getrefcount(data))

del alias
print("del alias ke baad: ", sys.getrefcount(data))

holder.clear()
print("holder.clear():    ", sys.getrefcount(data))

# Immortal objects (PEP 683) --------------------------------------------------
print("\n--- immortal objects ---")
for obj, label in [(None, "None"), (True, "True"), (1, "int 1"), (256, "int 256")]:
    print(f"{label:>8}: {sys.getrefcount(obj)}")
print("Ye bohat bare/fixed numbers = immortal. In par assert lagana bekaar hai.")

# refcount 0 hone par foran cleanup (deterministic destruction)
class Loud:
    def __init__(self, name):
        self.name = name
    def __del__(self):                 # refcount 0 hone par CPython yahan aata hai
        print(f"   [__del__] {self.name} ki memory free ho gayi")

print("\n--- deterministic cleanup ---")
x = Loud("obj-A")
y = x                                  # refcount 2
print("del x  (refcount 2 -> 1): kuch nahi hona chahiye")
del x
print("del y  (refcount 1 -> 0): abhi __del__ chalega")
del y
print("dekha? cleanup exactly wahan hua jahan aakhri reference gaya")
"""))

A(md("""
### Output ka matlab
Har naya reference (`alias`, list ke slots) counter barhaata hai, har `del`/scope-exit ghataata hai.
`Loud` class ne dikhaya ke aakhri reference jaate hi `__del__` **usi lamhe** chala —
Java/C# ki tarah "kabhi baad me" nahi.

### Gotchas
1. `sys.getrefcount()` ka jawab **hamesha +1** hota hai (function argument bhi reference hai).
2. Exception traceback, module globals, aur interpreter caches bhi chupke se references rakhte hain —
   number expected se zyada aa sakta hai.
3. Free-threaded build (PEP 703) me refcounting ka mechanism mukhtalif hai (biased/deferred).

### Interview tip
*"CPython uses reference counting for immediate reclamation plus a generational cycle collector
for reference cycles. Refcounting is deterministic but can't free cycles; the GC handles those."*
"""))

A(md("""
---
## 4. Object Identity — `id()`, `is` vs `==`

### Kya hai
- `id(obj)` → object ka unique integer (CPython me memory address).
- `is` → **identity** compare (same object?) — `id(a) == id(b)`
- `==` → **value** compare (`__eq__` call hota hai)

### Kyun / kahan
`is` sirf **singletons** ke sath: `None`, `True`, `False`, sentinel objects.
Numbers/strings ke liye hamesha `==`.

### Sab se bara dhoka: id-reuse
Object mar jaye to uska address dobara istemal ho sakta hai. Is liye purane `id()` ko
sambhaal kar rakhna aur baad me compare karna **bug** hai.
"""))

A(code(r"""
# is vs == --------------------------------------------------------------------
a = [1, 2, 3]
b = [1, 2, 3]        # alag object, wohi value
c = a

print("a == b:", a == b, "  (value same)")
print("a is b:", a is b, "  (object alag)")
print("a is c:", a is c, "  (same object)")

# None ke liye hamesha 'is'
val = None
print("\nval is None:", val is None)

# khatarnaak: == ko override kiya ja sakta hai, is ko nahi
class Weird:
    def __eq__(self, other):
        return True                    # sab ke barabar hone ka daawa!
w = Weird()
print("w == 42     :", w == 42, " <- __eq__ jhooth bol raha hai")
print("w is 42     :", w is 42, " <- identity jhooth nahi bol sakti")

# id-reuse ka dhoka
print("\n--- id reuse ---")
old_id = id([1, 2, 3])                 # ye list foran mar gayi (koi reference nahi)
fresh = [9, 9, 9]                      # naya object usi jagah ban sakta hai
print("purana id ==  naye object ka id?", old_id == id(fresh))
print("Sabaq: id() ko store kar ke baad me compare karna galat hai (object zinda rakho warna address recycle).")

# sentinel pattern — 'is' ka sahi istemal
MISSING = object()                     # unique sentinel
def get(d, key, default=MISSING):
    v = d.get(key, MISSING)
    if v is MISSING:                   # None bhi valid value ho sakti hai, is liye sentinel
        return None if default is MISSING else default
    return v
print("\nsentinel:", get({"a": None}, "a"), get({}, "b", "fallback"))
"""))

A(md("""
### Output ka matlab
`a == b` True magar `a is b` False → do alag objects, same value. `Weird` ne dikhaya ke `==`
class ke control me hai (jhooth bol sakta hai) magar `is` interpreter ke control me.

### Common mistakes
- `if x is 5:` / `if s is "hello":` — kabhi nahi. Chhote ints/strings par *ittefaqan* chal jata hai,
  bare values par fail ho jata hai (Python 3.8+ me `SyntaxWarning` bhi milti hai).
- `id()` ko object ka "permanent ID" samajhna — object marne ke baad address recycle hota hai.

### Interview tip
*"`is` compares identity, `==` compares value via `__eq__`. Use `is` only for singletons/sentinels."*
"""))

A(md("""
---
## 5. Small Integer Cache aur String Interning

### Kya hai
CPython start hote hi **-5 se 256** tak ke ints pehle se bana leta hai (small int cache).
Isi tarah identifier jaisi strings (compile-time literals) **interned** hoti hain — ek hi copy.

### Kyun
Ye values program me hazaaron dafa aati hain; ek hi object share karna memory aur waqt bachata hai.
Interned strings ka comparison **pointer comparison** se shuru hota hai → dict lookup tez.

### Syntax
```python
sys.intern(s)   # string ko interning table me daal do (ya wahan se maujooda lo)
```
"""))

A(code(r"""
import sys

# Small int cache -------------------------------------------------------------
x, y = 256, 256
print("256 is 256 :", x is y, " <- cached range (-5..256)")
p, q = 257, 257
print("257 is 257 :", p is q, " <- alag statements/objects ho sakte hain")
print("range check:", [(n, id(n) == id(n + 0)) for n in (-5, 0, 100, 256)][:2], "...")

# Ek hi cell/line me constants compile-time par fold ho kar share ho jaate hain,
# is liye 'is' ka natija context par depend karta hai -> is par bharosa na karo.

# String interning ------------------------------------------------------------
s1 = "hello_world"          # identifier jaisa literal -> interned
s2 = "hello_world"
print("\nliteral interning:", s1 is s2)

t1 = "hello world!"          # space/!' wali string
t2 = "".join(["hello", " ", "world", "!"])   # runtime par bani
print("runtime built  is  literal:", t1 is t2, " (aksar False)")
print("values equal            :", t1 == t2)

i1, i2 = sys.intern(t1), sys.intern(t2)
print("sys.intern ke baad      :", i1 is i2, " <- ab ek hi object")

# Kahan faida: bohat si repeated string keys (log parsing, CSV columns, JSON keys)
rows = [{"user_id": i, "status": sys.intern("active" if i % 2 else "inactive")} for i in range(5)]
statuses = [r["status"] for r in rows]
print("\ninterned statuses ek hi object share karte hain:",
      statuses[1] is statuses[3])

# memory ka faida: 100k rows me 'status' ki 100k copies ki jagah 2 objects
big_naive = ["pending_review_state" + "" for _ in range(3)]          # naye objects ban sakte
big_intern = [sys.intern("pending_review_state") for _ in range(3)]
print("naive all-same-object? ", all(s is big_naive[0] for s in big_naive))
print("intern all-same-object?", all(s is big_intern[0] for s in big_intern))
"""))

A(md("""
### Output ka matlab
`256 is 256` → True (cache), magar runtime par bani strings ka `is` aksar False.
`sys.intern()` ke baad dono naam ek hi object par aa gaye.

### Gotchas
- Interning/caching **implementation detail** hai — *optimization* ke liye theek, *logic* ke liye kabhi nahi.
- `sys.intern` sirf tab use karo jab bohat si duplicate strings ho (parsing, ETL). Warna faida nahi.
- Interned strings kabhi free nahi hoti (process ki umar tak) — random user input intern na karo,
  warna memory barhti rahegi.

### Interview tip
*"Small ints (-5..256) and compile-time string literals are cached/interned by CPython.
`sys.intern` is a memory/lookup optimisation for many duplicate strings — never rely on it for equality."*
"""))

A(md("""
---
## 6. Mutable vs Immutable — asli wajah

### Kya hai
| Immutable | Mutable |
|---|---|
| `int`, `float`, `bool`, `str`, `bytes`, `tuple`, `frozenset`, `complex`, `range` | `list`, `dict`, `set`, `bytearray`, most custom classes |

### Asli wajah (sirf "badal nahi sakte" nahi)
1. **Hashability** — dict key / set member banne ke liye value ki hash zindagi bhar same honi chahiye.
   Mutable object ki value badal jati hai → hash badal jati → dict me kho jata. Is liye
   mutable types `__hash__ = None` rakhte hain.
2. **Safe sharing** — immutable object ko bina dar share/cache/intern kiya ja sakta hai (thread-safe read).
3. **Optimizations** — constant folding, interning, `tuple` reuse — sab immutability par mabni.
"""))

A(code(r"""
# Hashability ka asli imtihan -------------------------------------------------
print("hash('abc') :", hash("abc") is not None)
print("hash((1,2)) :", hash((1, 2)))

try:
    hash([1, 2])                       # list mutable -> hash nahi
except TypeError as e:
    print("hash([1,2]) ->", type(e).__name__, ":", e)

print("\nlist.__hash__ :", list.__hash__, " <- jaan boojh kar None")
print("tuple.__hash__:", tuple.__hash__ is not None)

# tuple hashable hai... lekin sirf tab jab uske andar sab hashable ho
try:
    hash((1, [2]))
except TypeError as e:
    print("hash((1,[2])) ->", type(e).__name__, ":", e)

# Agar mutable object ko key banane ki ijazat hoti to kya hota (simulate)
class BadKey:
    def __init__(self, v): self.v = v
    def __hash__(self): return hash(self.v)      # hash mutable state par -> KHATRA
    def __eq__(self, other): return isinstance(other, BadKey) and self.v == other.v

k = BadKey(1)
d = {k: "mila"}
print("\nlookup pehle :", d.get(k))
k.v = 99                                # state badal di -> hash badal gaya
print("state badalne ke baad lookup:", d.get(k), " <- object kho gaya!")
print("magar wo ab bhi dict me maujood hai:", list(d.values()))
print("Yehi wajah hai ke list/dict/set hashable nahi hain.")

# Immutable ka matlab 'deeply frozen' nahi hota
t = (1, [2, 3])
t[1].append(4)
print("\ntuple immutable hai magar deep-immutable nahi:", t)
"""))

A(md("""
### Output ka matlab
`BadKey` demo Python ka core reason dikhata hai: hash badal jaye to object apne bucket me
"kho jata" hai — dict me hai magar `get()` nahi milta. Is liye Python mutable containers ko
hashable hone hi nahi deta.

### Interview tip
*"Immutability isn't about being 'read-only' for convenience — it's what makes an object safely
hashable, shareable and cacheable. `tuple` is immutable but not deeply immutable."*
""" ))
