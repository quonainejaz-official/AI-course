"""Generator: OOP in Python / Intermediate / 02 MRO, Multiple Inheritance, Mixins aur super deep."""

import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

CELLS = []

CELLS += [
    md("""
# MRO, Multiple Inheritance, Mixins aur `super()` — Deep Dive

**Level:** Intermediate | **Language:** Python 3.14

Bhai, multiple inheritance Python ki sabse taqatwar aur sabse **khatarnak** feature hai.
Isko samajhne ke liye ek hi cheez asli hai: **MRO (Method Resolution Order)**.
MRO samajh gaye to `super()`, diamond problem, mixins — sab khud ba khud clear ho jate hain.

## Is notebook me kya seekhenge

- MRO kya hai, `Class.__mro__` / `Class.mro()`
- **C3 linearization** ke rules aur haath se step-by-step calculation
- **Diamond problem** ka poora demo (kaun sa method chalega aur kyun)
- `super()` **cooperative** multiple inheritance (`**kwargs` chain)
- `super()` bina arguments kaise kaam karta hai (`__class__` cell ka jadoo)
- Explicit parent call vs `super()` — kab masla banta hai (double call bug)
- **Inconsistent MRO** `TypeError` ka live demo
- **Mixins** ka design: `SerializableMixin`, `LoggableMixin`, `ComparableMixin`, `TimestampMixin`
- **Mixin order matters** — practical proof
- Mixin vs base class vs composition
- *"Favor composition over inheritance"* — before/after refactor
- Delegation aur `__getattr__` based forwarding
- Debugging tools: `inspect.getmro`, `super()` object, `__init_subclass__`
- Abstract + mixin combos
- Real example: **Django-style** class hierarchy simulate karna
- Multiple inheritance ke risks + rules of thumb
- **LeetCode:** 173, 341, 284 (iterator design problems)
- Interview Q&A + practice exercises + cheat-sheet

## Prerequisites

- Single inheritance, method overriding
- `super().__init__()` ka basic istemal
- NB1 ka `ABC` / abstract methods wala hissa
"""),
    md("""
## 1. MRO kya hai?

**Kya hai:** MRO = **Method Resolution Order** — wo **tarteeb** jis me Python kisi attribute/method ko
classes me dhoondta hai. Ye ek **linear list** hoti hai (class ke `__mro__` me mehfooz).

**Kyun zaroori:** Multiple inheritance me ek hi naam ke methods kai jagah ho sakte hain.
MRO batata hai ke **kaun jeetega**, aur `super()` ka "next" kaun hai.

**Syntax:**

```python
C.__mro__        # tuple
C.mro()          # list (classmethod)
inspect.getmro(C)
help(C)          # MRO bhi dikhata hai
```

**Ahem baat:** attribute lookup instance ke `__dict__` se shuru hota hai, phir `type(obj).__mro__`
ke har class ke `__dict__` me tarteeb se dekha jata hai — **pehla match jeet jata hai**.
"""),
    code("""
import inspect

class A:
    def who(self): return "A"
    def only_a(self): return "sirf A me hai"

class B(A):
    def who(self): return "B"

class C(A):
    def who(self): return "C"
    def only_c(self): return "sirf C me hai"

class D(B, C):
    pass

# MRO dekho: D -> B -> C -> A -> object
print("D.__mro__:")
for i, k in enumerate(D.__mro__):
    print(f"  {i}. {k.__name__}")

d = D()
print("\\nd.who()   ->", d.who(), "(B jeeta kyunki MRO me pehle hai)")
print("d.only_c() ->", d.only_c(), "(sirf C me tha, MRO se mil gaya)")
print("d.only_a() ->", d.only_a())

print("\\nmro() list == __mro__ tuple:", D.mro() == list(D.__mro__))
print("inspect.getmro same:", inspect.getmro(D) == D.__mro__)
print("object hamesha aakhir me:", D.__mro__[-1].__name__)
"""),
    code("""
# Lookup ka asli mechanism: instance __dict__ -> phir MRO ke class __dict__s
d2 = D()
d2.who = lambda: "instance attribute"       # instance par seedha rakh diya

print("instance attribute jeet gaya:", d2.who())
print("class wala method (seedha B se):", B.who(d2))
del d2.who
print("instance attribute hatane ke baad:", d2.who(), "-> phir MRO chala")

def find_owner(cls, name):
    # MRO me manually dhoondo ke method kis class ka hai
    for k in cls.__mro__:
        if name in k.__dict__:
            return k.__name__
    return None

for name in ("who", "only_a", "only_c", "__init__"):
    print(f"{name:<10} kis class se aaya ->", find_owner(D, name))
"""),
    md("""
## 2. C3 Linearization — MRO banta kaise hai?

Python 2.3 se MRO **C3 linearization** algorithm se banta hai. Teen guarantees deta hai:

1. **Local precedence order:** bases jis tarteeb me likhe, wahi tarteeb qaayam rahegi (`class D(B, C)` → B se pehle C nahi aa sakta)
2. **Monotonicity:** subclass ka MRO parent ke MRO ki tarteeb ko nahi torega
3. Har class **sirf ek baar** aayegi

### Formula

```
L[C] = C + merge( L[B1], L[B2], ..., L[Bn], [B1, B2, ..., Bn] )
```

`merge` ka rule (har step par):
- Pehli list ka **head** lo (list ka pehla element)
- Agar wo head kisi doosri list ki **tail** me (yaani head ke ilawa kisi bhi position par) mojood hai
  → is head ko chhoro, agli list ka head try karo
- Warna use output me daal do aur **saari lists** se hata do
- Dobara shuru se; koi valid head na mile → **TypeError (inconsistent hierarchy)**

### Haath se hisaab: diamond

```
      object
        |
        A
       / \\
      B   C
       \\ /
        D            class D(B, C)
```

```
L[object] = [object]
L[A] = [A, object]
L[B] = [B, A, object]
L[C] = [C, A, object]

L[D] = D + merge( [B,A,object], [C,A,object], [B,C] )
  head B: kisi list ki tail me nahi        -> le lo         out=[D,B]
     baqi: merge([A,object], [C,A,object], [C])
  head A: [C,A,object] ki TAIL me hai      -> chhoro
  next list ka head C: kisi tail me nahi   -> le lo         out=[D,B,C]
     baqi: merge([A,object], [A,object], [])
  head A: ab kisi tail me nahi             -> le lo         out=[D,B,C,A]
  head object                              -> le lo         out=[D,B,C,A,object]

L[D] = [D, B, C, A, object]   <-- yehi Python bhi deta hai
```
"""),
    code("""
# Chalo apna khud ka C3 likh kar Python se compare karein (samajhne ka behtareen tareeqa)

def c3_merge(seqs):
    result = []
    seqs = [list(s) for s in seqs if s]
    while seqs:
        for seq in seqs:                       # har list ka head try karo
            head = seq[0]
            # head kisi doosri list ki TAIL (index 1 se aage) me hai?
            if any(head in s[1:] for s in seqs):
                continue                       # ye head abhi nahi le sakte
            break
        else:
            raise TypeError("Inconsistent hierarchy -> C3 fail")
        result.append(head)
        # head ko saari lists se hata do
        seqs = [s[1:] if s[0] is head else s for s in seqs]
        seqs = [s for s in seqs if s]
    return result

def my_mro(cls):
    if cls is object:
        return [object]
    return [cls] + c3_merge([my_mro(b) for b in cls.__bases__] + [list(cls.__bases__)])

for k in (D, B, C, A):
    mine = [c.__name__ for c in my_mro(k)]
    real = [c.__name__ for c in k.__mro__]
    print(f"{k.__name__}: mine={mine}")
    assert mine == real, (mine, real)
print("\\n[pass] hamara C3 Python ke MRO se bilkul match karta hai")
"""),
    code("""
# Ek zyada peecheeda hierarchy par bhi test karo (classic Python docs ka example)
class O: pass
class X(O): pass
class Y(O): pass
class Z1(X, Y): pass
class Z2(Y, X): pass

for k in (Z1, Z2):
    print(k.__name__, "->", [c.__name__ for c in k.__mro__])
    assert [c.__name__ for c in my_mro(k)] == [c.__name__ for c in k.__mro__]

# Aur ek 5-level mixed hierarchy
class F1: pass
class F2(F1): pass
class F3(F1): pass
class F4(F2, F3): pass
class F5(F3, F1): pass
class F6(F4, F5): pass

print("\\nF6 ->", [c.__name__ for c in F6.__mro__])
assert [c.__name__ for c in my_mro(F6)] == [c.__name__ for c in F6.__mro__]
print("[pass] complex hierarchy bhi match")
"""),
    md("""
## 3. Diamond problem ka poora demo

**Kya hai:** Do parents ek hi grandparent se aate hain (diamond shape). Sawal:
grandparent ka `__init__`/method **kitni baar** chalega?

- **Naive/explicit calls** ke sath: grandparent **do baar** chalta hai (bug!)
- **`super()` ke sath:** MRO linear hai, is liye har class **exactly ek baar** chalti hai

Ye "cooperative multiple inheritance" ka asli faida hai.
"""),
    code("""
# ---- GALAT tareeqa: explicit parent calls -> Base do baar chala ----
trace_bad = []

class BaseBad:
    def __init__(self):
        trace_bad.append("BaseBad.__init__")

class LeftBad(BaseBad):
    def __init__(self):
        BaseBad.__init__(self)                # explicit call
        trace_bad.append("LeftBad.__init__")

class RightBad(BaseBad):
    def __init__(self):
        BaseBad.__init__(self)                # explicit call
        trace_bad.append("RightBad.__init__")

class ChildBad(LeftBad, RightBad):
    def __init__(self):
        LeftBad.__init__(self)
        RightBad.__init__(self)               # RightBad phir BaseBad ko call karega
        trace_bad.append("ChildBad.__init__")

ChildBad()
print("explicit calls ->", trace_bad)
print("BaseBad kitni baar chala:", trace_bad.count("BaseBad.__init__"), "<- BUG (do baar)")

# ---- SAHI tareeqa: super() -> har class ek baar ----
trace_good = []

class BaseGood:
    def __init__(self):
        trace_good.append("BaseGood.__init__")

class LeftGood(BaseGood):
    def __init__(self):
        super().__init__()                    # MRO ka NEXT (na ke hard-coded parent)
        trace_good.append("LeftGood.__init__")

class RightGood(BaseGood):
    def __init__(self):
        super().__init__()
        trace_good.append("RightGood.__init__")

class ChildGood(LeftGood, RightGood):
    def __init__(self):
        super().__init__()
        trace_good.append("ChildGood.__init__")

ChildGood()
print("\\nsuper() ->", trace_good)
print("BaseGood kitni baar chala:", trace_good.count("BaseGood.__init__"), "<- theek (ek baar)")
print("MRO:", [c.__name__ for c in ChildGood.__mro__])
"""),
    md("""
### 3.1 `super()` ka asli matlab: "parent" nahi, "MRO ka next"

Ye sabse bara galat-fehmi hai. `super()` ka matlab **parent class nahi** hai —
matlab hai *"`type(self).__mro__` me **meri** class ke baad wali class"*.

Is liye `LeftGood` ke andar `super().__init__()` ne `RightGood` ko call kiya —
halanke `RightGood`, `LeftGood` ka parent bilkul nahi hai! Kyunki `ChildGood` ka MRO
`[ChildGood, LeftGood, RightGood, BaseGood, object]` tha.

**Isi liye `super()` "cooperative" hai:** class ko nahi pata aage kaun hai, wo bas
"chain me agla" call karti hai — aur poora chain chal jata hai.
"""),
    code("""
class M1:
    def ping(self):
        print("  M1.ping -> super:", type(self).__mro__[type(self).__mro__.index(M1) + 1].__name__)
        super().ping()

class M2:
    def ping(self):
        print("  M2.ping (chain ka aakhir, aage super().ping() nahi)")

class Together(M1, M2):
    def ping(self):
        print("Together.ping shuru")
        super().ping()
        print("Together.ping khatam")

print("MRO:", [c.__name__ for c in Together.__mro__])
Together().ping()

# M1 akela istemal karo to chain toot jayegi -> ye cooperative design ka trade-off hai
class OnlyM1(M1): pass
try:
    OnlyM1().ping()
except AttributeError as e:
    print("\\nAttributeError:", e, "-> M1 ko akela use nahi kar sakte (mixin hai)")

# super() object khud dekho
s = super(M1, Together())
print("\\nsuper object:", s)
print("super(M1, obj) ka __self_class__:", s.__self_class__.__name__, "| __thisclass__:", s.__thisclass__.__name__)
"""),
    md("""
## 4. Cooperative multiple inheritance: `**kwargs` chain

Sabse aam masla: har class ke `__init__` ke apne parameters hote hain.
Multiple inheritance me har class ko **apne** args lene chahiye aur **baqi** aage bhej dene chahiye.

**Golden rules:**
1. Har `__init__` `**kwargs` accept kare aur `super().__init__(**kwargs)` call kare
2. Apne consume kiye hue kwargs **aage na bhejo** (`kwargs.pop("x")` ya keyword-only params)
3. Chain ke aakhir me `object.__init__()` aata hai — usko **extra kwargs mat do** warna `TypeError`
4. Best practice: keyword-only arguments (`def __init__(self, *, size=1, **kw)`)
"""),
    code("""
class Widget:
    def __init__(self, *, name="widget", **kwargs):
        # NOTE: baqi kwargs aage bhej do -> chain chalti rahe
        super().__init__(**kwargs)
        self.name = name

class ColorMixin:
    def __init__(self, *, color="black", **kwargs):
        super().__init__(**kwargs)
        self.color = color                       # apna arg consume kiya, aage nahi bheja

class BorderMixin:
    def __init__(self, *, border=1, **kwargs):
        super().__init__(**kwargs)
        self.border = border

class ShadowMixin:
    def __init__(self, *, shadow=False, **kwargs):
        super().__init__(**kwargs)
        self.shadow = shadow


class FancyButton(ShadowMixin, BorderMixin, ColorMixin, Widget):
    def __init__(self, *, label="OK", **kwargs):
        super().__init__(**kwargs)              # sab kuch chain me chala jayega
        self.label = label

    def __repr__(self):
        return (f"FancyButton(label={self.label!r}, color={self.color!r}, "
                f"border={self.border}, shadow={self.shadow}, name={self.name!r})")


b = FancyButton(label="Save", color="blue", border=2, shadow=True, name="save-btn")
print(b)
print("MRO:", [c.__name__ for c in FancyButton.__mro__])

# Defaults bhi kaam karte hain (koi arg do ya na do)
print(FancyButton())

# Gotcha: aisa kwarg jo kisi ne consume na kiya -> object.__init__ tak pahunch kar TypeError
try:
    FancyButton(rounded=True)
except TypeError as e:
    print("\\nTypeError:", e, "-> koi bhi class 'rounded' consume nahi karti")
"""),
    md("""
## 5. `super()` bina arguments kaise kaam karta hai? (`__class__` cell)

Python 3 me `super()` likhna kaafi hai — magar andar kya hota hai?

Jab compiler kisi method ke andar `super()` (ya `__class__`) dekhta hai, wo:

1. Us function ke liye ek **closure cell** banata hai jiska naam `__class__` hota hai,
   jisme wo class rakhi jati hai jahan method **define** hua (na ke `type(self)`)
2. `super()` bina args us cell aur pehle positional argument (`self`) ko utha kar
   `super(__class__, self)` bana deta hai

**Isi liye:**
- `super()` sirf class body ke andar wale function me chalta hai (bahar `RuntimeError`)
- Function ko baad me class me chipkao (monkey-patch) to `super()` fail karega
- `staticmethod` me `self` nahi hota → `super()` bina args nahi chalega
- Nested function me `self` na ho to bhi masla
"""),
    code("""
class Parent:
    def greet(self): return "Parent.greet"

class Child(Parent):
    def greet(self):
        # compiler ne yahan chhupa hua __class__ cell bana diya
        print("  __class__ cell:", __class__.__name__)
        print("  free variables:", Child.greet.__code__.co_freevars)
        return "Child + " + super().greet()

print(Child().greet())
print("\\nnormal method ke freevars (koi super nahi):", Parent.greet.__code__.co_freevars)

# Class ke bahar define kiya function -> super() ke liye cell nahi bana
def patched_greet(self):
    return "patched + " + super().greet()      # ye fail karega

Child.patched = patched_greet
try:
    Child().patched()
except RuntimeError as e:
    print("\\nRuntimeError:", e)

# Hal: explicit 2-arg super()
def patched_ok(self):
    return "patched + " + super(Child, self).greet()
Child.patched_ok = patched_ok
print("explicit super() se theek:", Child().patched_ok())
"""),
    code("""
# super() ki teen shaklein
class Base2:
    def tag(self): return "Base2"

class Mid(Base2):
    def tag(self): return "Mid->" + super().tag()

class Leaf(Mid):
    def tag(self):
        a = super().tag()                        # normal (0-arg)
        b = super(Leaf, self).tag()               # bilkul wahi cheez (explicit)
        c = super(Mid, self).tag()                # Mid ko SKIP kar ke Base2 par jao
        return f"a={a} | b={b} | c={c}"

print(Leaf().tag())

# Class-level (unbound) super: classmethods ke liye
class CBase:
    @classmethod
    def make(cls): return f"CBase.make({cls.__name__})"

class CChild(CBase):
    @classmethod
    def make(cls):
        return "CChild -> " + super().make()      # classmethod me bhi 0-arg super chalta hai

print(CChild.make())

# staticmethod me 0-arg super nahi chalta (self/cls nahi hota)
class SBase:
    @staticmethod
    def util(): return "SBase.util"

class SChild(SBase):
    @staticmethod
    def util():
        return "SChild -> " + SBase.util()        # yahan explicit hi likhna parta hai
print(SChild.util())
"""),
]

CELLS += [
    md("""
## 6. Explicit parent call vs `super()` — kab masla?

| | Explicit (`Parent.method(self)`) | `super().method()` |
|---|---|---|
| Kis ko call karta hai | **Hard-coded** class | MRO ka next |
| Diamond me | **Double call** ka bug | Har class ek baar |
| Class ka naam badle | Manually theek karna parega | Khud chal jayega |
| Mixin friendly | Nahi (chain toot jati hai) | Haan |
| Kab theek hai | Deliberately kisi khaas class ka code chahiye (e.g. `dict.__setitem__`) | Default choice |

**Rule:** Multiple inheritance ya mixins ka imkaan ho to **hamesha** `super()`.
Explicit call sirf jab tum jaan boojh kar MRO ko bypass kar rahe ho (aur comment likh do kyun).

**Ek aur bug:** Explicit call me galti se doosri class ka naam likh diya (copy-paste) →
infinite recursion ya galat behaviour. `super()` me ye ghalti mumkin hi nahi.
"""),
    code("""
# Explicit call se infinite recursion ka classic bug
class Logger1:
    def log(self, m): return f"[L1] {m}"

class Logger2(Logger1):
    def log(self, m):
        return Logger1.log(self, m)            # sahi explicit call (parent ka naam)

class BadLogger(Logger1):
    def log(self, m):
        return BadLogger.log(self, m)          # <-- ye infinite recursion hai

print(Logger2().log("theek hai"))
import sys
sys.setrecursionlimit(200)                      # test ke liye limit choti kar li
try:
    BadLogger().log("boom")
except RecursionError as e:
    print("RecursionError:", type(e).__name__, "-> apni hi class ko call kar diya")
sys.setrecursionlimit(1000)

# Refactor ka masla: base class ka naam badla to explicit calls tootengi
class Renamed(Logger1):
    def log(self, m):
        return super().log(m).replace("L1", "L1*")   # naam badle to bhi chalta rahega
print(Renamed().log("super() safe hai"))
"""),
    md("""
## 7. Inconsistent MRO — `TypeError` ka demo

Agar tum aisi hierarchy banao jiska C3 linearization mumkin **nahi**, Python **class banate waqt hi**
`TypeError: Cannot create a consistent method resolution order (MRO)` de deta hai.

Classic misaal:

```python
class A: pass
class B(A): pass
class Bad(A, B): pass     # A ko B se pehle maanga -> magar B, A ki subclass hai (B pehle aana chahiye)
```

**Rule:** derived class hamesha apni base se **pehle** aati hai. Tum ulta demand karo to fail.
"""),
    code("""
class P: pass
class Q(P): pass

# Case 1: base ko subclass se pehle likhna
try:
    class Bad1(P, Q): pass
except TypeError as e:
    print("TypeError:", e)

# Sahi tarteeb (specific se general): Q pehle, P baad me
class Good1(Q, P): pass
print("Good1 MRO:", [c.__name__ for c in Good1.__mro__])

# Case 2: do parents ki tarteeb ka aapas me tazad (conflicting order)
class X1: pass
class Y1: pass
class First(X1, Y1): pass       # kehti hai: X1 pehle, Y1 baad me
class Second(Y1, X1): pass      # kehti hai: Y1 pehle, X1 baad me

try:
    class Impossible(First, Second): pass    # dono shartein ek sath poori nahi ho saktin
except TypeError as e:
    print("\\nTypeError:", e)

# Hamara khud ka C3 bhi wahi kehta hai
def c3_merge(seqs):
    result = []
    seqs = [list(s) for s in seqs if s]
    while seqs:
        for seq in seqs:
            head = seq[0]
            if any(head in s[1:] for s in seqs):
                continue
            break
        else:
            raise TypeError("Inconsistent hierarchy -> C3 fail")
        result.append(head)
        seqs = [s[1:] if s[0] is head else s for s in seqs]
        seqs = [s for s in seqs if s]
    return result

try:
    c3_merge([[First.__name__, "X1", "Y1"], [Second.__name__, "Y1", "X1"], [First.__name__, Second.__name__]])
except TypeError as e:
    print("hamara C3 bhi:", e)

# Case 3: duplicate base
try:
    class Dup(P, P): pass
except TypeError as e:
    print("\\nTypeError:", e)
"""),
    md("""
## 8. Mixins — design aur asool

**Kya hai:** Mixin ek chhoti class hoti hai jo **sirf behaviour** deti hai, akeli use nahi hoti,
aur usme (aam tor par) apna state/`__init__` nahi hota. Ye "is-a" nahi, **"can-do"** hai.

**Kyun:** Ek hi feature (JSON serialization, logging, timestamps, comparison) kai unrelated
classes me chahiye — copy-paste ke bagair.

**Mixin ke asool (industry conventions):**
1. Naam ke aakhir me `Mixin` (`SerializableMixin`)
2. Akela instantiate nahi hota — hamesha kisi base ke sath
3. `__init__` se bacho; agar chahiye to `**kwargs` + `super()` cooperative style
4. Chhota rakho — ek mixin, ek zimmedari
5. Base class se pehle likho: `class User(LoggableMixin, Base)` — mixin ko override ka mauqa mile
6. Mixin apne "expected" attributes document kare (jo host class dega)
"""),
    code("""
import json, time, datetime

class SerializableMixin:
    # Expects: host class me __dict__ ya `fields` list ho
    fields = None                                # None = saara __dict__

    def to_dict(self):
        if self.fields is None:
            return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return {f: getattr(self, f) for f in self.fields}

    def to_json(self, **kw):
        return json.dumps(self.to_dict(), default=str, ensure_ascii=False, **kw)


class LoggableMixin:
    # Har object apni harkatein yaad rakhta hai (asli project me logging module hota)
    @property
    def logs(self):
        if not hasattr(self, "_logs"):
            self._logs = []                      # lazy init -> __init__ ki zaroorat nahi
        return self._logs

    def log(self, msg):
        self.logs.append(f"{type(self).__name__}: {msg}")
        return msg


class ComparableMixin:
    # Expects: host class `sort_key()` de
    def _key(self):
        return self.sort_key()
    def __eq__(self, other): return isinstance(other, ComparableMixin) and self._key() == other._key()
    def __lt__(self, other): return self._key() < other._key()
    def __le__(self, other): return self._key() <= other._key()
    def __gt__(self, other): return self._key() > other._key()
    def __ge__(self, other): return self._key() >= other._key()
    def __hash__(self): return hash(self._key())


class TimestampMixin:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)               # cooperative!
        self.created_at = datetime.datetime(2026, 1, 1, 12, 0, 0)   # deterministic (test friendly)
        self.updated_at = self.created_at

    def touch(self):
        self.updated_at = self.created_at + datetime.timedelta(minutes=5)
        return self.updated_at


# ---- Ab teen mixins ko ek asli class me jodo ----
class Product(SerializableMixin, LoggableMixin, ComparableMixin, TimestampMixin):
    fields = ["sku", "title", "price"]

    def __init__(self, sku, title, price, **kwargs):
        super().__init__(**kwargs)               # TimestampMixin tak pahunchega
        self.sku, self.title, self.price = sku, title, price

    def sort_key(self):
        return (self.price, self.title)


p1 = Product("A-1", "Keyboard", 3500)
p2 = Product("A-2", "Mouse", 1200)

print("to_dict :", p1.to_dict())
print("to_json :", p2.to_json())
p1.log("price check hui")
p1.log("stock update")
print("logs    :", p1.logs)
print("compare :", p2 < p1, "| sorted:", [p.title for p in sorted([p1, p2])])
print("hashable:", len({p1, p2}), "unique objects")
print("times   :", p1.created_at.isoformat(), "->", p1.touch().isoformat())
print("MRO     :", [c.__name__ for c in Product.__mro__])
"""),
    md("""
### 8.1 Mixin order matters — amali saboot

`class C(MixinA, MixinB, Base)` me tarteeb badalne se **behaviour badal jata hai**,
kyunki MRO badal jata hai. Do usool:

1. **Mixins base class se PEHLE** — warna base ka method jeet jayega aur mixin bekar
2. Do mixins ek hi method override karte hon to **jo pehle likha wo jeetega**
   (aur `super()` ke zariye doosre ko call kar sakta hai — chain)
"""),
    code("""
class HtmlRenderMixin:
    def render(self, text):
        return f"<p>{super().render(text)}</p>"     # chain jari rakhi

class UpperMixin:
    def render(self, text):
        return super().render(text).upper()

class PlainBase:
    def render(self, text):
        return text


class V1(HtmlRenderMixin, UpperMixin, PlainBase): pass    # pehle html, phir upper
class V2(UpperMixin, HtmlRenderMixin, PlainBase): pass    # ulta

print("V1:", V1().render("salam"), " MRO:", [c.__name__ for c in V1.__mro__][:3])
print("V2:", V2().render("salam"), " MRO:", [c.__name__ for c in V2.__mro__][:3])
print("-> V1 me upper() pehle laga phir tag; V2 me tag laga phir poora upper hua")

# GALTI: base class ko pehle likh diya -> mixin ka render kabhi nahi chalega
class V3(PlainBase, HtmlRenderMixin): pass
print("\\nV3:", V3().render("salam"), "<- mixin bekar ho gaya (base pehle jeet gaya)")
print("V3 MRO:", [c.__name__ for c in V3.__mro__])

assert V1().render("hi") == "<p>HI</p>"
assert V2().render("hi") == "<P>HI</P>"
assert V3().render("hi") == "hi"
print("[pass] order ka asar sabit")
"""),
    md("""
## 9. Mixin vs Base class vs Composition

| | Mixin (inheritance) | Base/Abstract class | Composition (has-a) |
|---|---|---|---|
| Rishta | "can-do" (capability) | "is-a" (identity) | "has-a" (uses) |
| Coupling | Tight (MRO ka hissa) | Tight | **Loose** |
| Runtime badal sakte? | Nahi (class fix) | Nahi | **Haan** (object swap) |
| Name clash ka khatra | Haan (MRO) | Kam | Nahi |
| Testing | Class banani parti hai | Class banani parti hai | Fake object inject |
| Kab | Chhota cross-cutting behaviour | Asli type hierarchy + shared code | Zyada tar baqi cases |

**Rule of thumb:** Agar sawal ka jawab *"X ek Y hai"* nahi bal ke *"X, Y istemal karta hai"* ya
*"X, Y kar sakta hai magar kai tareeqon se"* → **composition**.
"""),
    md("""
### 9.1 "Favor composition over inheritance" — before/after refactor

**Scenario:** Notification bhejni hai. Pehle inheritance se solve karte hain
(`EmailNotifier`, `RetryEmailNotifier`, `EncryptedRetryEmailNotifier`, ...) —
ye **class explosion** ban jata hai: `2^n` combinations ke liye `2^n` classes!

Composition ke sath: `Notifier(transport, policies=[...])` — combinations **runtime** par bante hain.
"""),
    code("""
# ================= BEFORE: inheritance ka class explosion =================
class EmailNotifierOld:
    def send(self, msg): return f"email: {msg}"

class RetryEmailNotifierOld(EmailNotifierOld):
    def send(self, msg):
        for _ in range(2):
            r = super().send(msg)
        return f"retry({r})"

class SignedEmailNotifierOld(EmailNotifierOld):
    def send(self, msg): return f"signed({super().send(msg)})"

class SignedRetryEmailNotifierOld(RetryEmailNotifierOld):   # aur SMS ke liye? phir 4 classes!
    def send(self, msg): return f"signed({super().send(msg)})"

print("BEFORE:", SignedRetryEmailNotifierOld().send("hi"))
print("2 transports x 2 features = 4+ classes; 3 features = 8+ classes (explosion)")

# ================= AFTER: composition =================
class EmailTransport:
    name = "email"
    def deliver(self, msg): return f"email: {msg}"

class SmsTransport:
    name = "sms"
    def deliver(self, msg): return f"sms: {msg[:20]}"

class RetryPolicy:
    def __init__(self, times=2): self.times = times
    def wrap(self, fn):
        def inner(msg):
            for _ in range(self.times):
                out = fn(msg)
            return f"retry{self.times}({out})"
        return inner

class SignPolicy:
    def wrap(self, fn):
        return lambda msg: f"signed({fn(msg)})"

class Notifier:
    # transport + policies inject hote hain -> koi subclass banane ki zaroorat nahi
    def __init__(self, transport, policies=()):
        self.transport, self.policies = transport, list(policies)

    def send(self, msg):
        fn = self.transport.deliver
        for p in self.policies:                 # policies ko chain me lapet do
            fn = p.wrap(fn)
        return fn(msg)


print("\\nAFTER:")
print(" plain email :", Notifier(EmailTransport()).send("hi"))
print(" signed sms  :", Notifier(SmsTransport(), [SignPolicy()]).send("hi"))
print(" retry+sign  :", Notifier(EmailTransport(), [RetryPolicy(3), SignPolicy()]).send("hi"))
print(" runtime par policy add:", end=" ")
n = Notifier(SmsTransport())
n.policies.append(RetryPolicy(2))               # inheritance me ye mumkin hi nahi tha
print(n.send("hi"))
print("-> 2 transports x 3 policies = 0 nayi classes")
"""),
]

CELLS += [
    md("""
## 10. Delegation aur `__getattr__` based forwarding

**Masla:** Composition me har method ke liye wrapper likhna parta hai (boilerplate):

```python
def append(self, x): return self._items.append(x)
def pop(self): return self._items.pop()
```

**Hal:** `__getattr__` — jab attribute **na mile** tab Python isko call karta hai.
Wahan se hum request andar wale object ko forward kar dete hain.

**Ahem farq:**
- `__getattribute__` **har** access par chalta hai (khatarnak, recursion aasan)
- `__getattr__` **sirf** miss hone par chalta hai (safe, delegation ka standard tareeqa)

**Gotchas:**
1. Dunder methods (`len()`, `[]`, `+`) `__getattr__` se **forward nahi** hote —
   Python inko **type** par dhoondta hai, instance par nahi. Manually likhna parega.
2. `__getattr__` me `self._wrapped` access karna infinite recursion de sakta hai agar
   `_wrapped` set hone se pehle access ho → `object.__getattribute__` ya `__dict__` use karo.
3. `hasattr` sab kuch `True` dene lag sakta hai (agar tum wildcard forward karo).
"""),
    code("""
class TrackedList:
    # Composition + delegation: list ki poori taqat, magar har mutation track hoti hai
    def __init__(self, items=()):
        self._items = list(items)
        self.changes = 0

    # ---- explicit wrappers: jinme extra kaam karna hai ----
    def append(self, x):
        self.changes += 1
        self._items.append(x)
        return self

    # ---- baqi sab kuch forward kar do ----
    def __getattr__(self, name):
        # NOTE: ye sirf tab chalta hai jab normal lookup FAIL ho
        # self.__dict__ se lo taake recursion na ho
        items = self.__dict__.get("_items")
        if items is None:
            raise AttributeError(name)
        attr = getattr(items, name)             # list ka method/attribute
        return attr

    # ---- dunders manually (forward NAHI hote) ----
    def __len__(self): return len(self._items)
    def __getitem__(self, i): return self._items[i]
    def __iter__(self): return iter(self._items)
    def __repr__(self): return f"TrackedList({self._items}, changes={self.changes})"


t = TrackedList([3, 1, 2])
t.append(5)
print(t)
print("delegated sort()  :", (t.sort(), t)[1])          # list.sort forward hua
print("delegated count() :", t.count(3))
print("delegated index() :", t.index(5))
print("len (manual)      :", len(t), "| slice:", t[1:3])
print("changes counter   :", t.changes, "(sirf append track hua, sort nahi)")

# Gotcha 1 ka demo: agar __len__ na likhte to len() fail hota
class NoDunder:
    def __init__(self): self._items = [1, 2, 3]
    def __getattr__(self, n): return getattr(self._items, n)

nd = NoDunder()
print("\\nforwarded method chalta hai:", nd.count(1))
try:
    len(nd)
except TypeError as e:
    print("TypeError:", e, "-> dunder lookup TYPE par hota hai, __getattr__ se nahi")
"""),
    code("""
# Delegation ka doosra amali roop: "smart proxy" jo har call log kare
class LoggingProxy:
    def __init__(self, target):
        # NOTE: object.__setattr__ istemal kiya taake __setattr__ override safe rahe
        object.__setattr__(self, "_target", target)
        object.__setattr__(self, "calls", [])

    def __getattr__(self, name):
        target = object.__getattribute__(self, "_target")
        attr = getattr(target, name)
        if callable(attr):
            def wrapper(*a, **kw):
                object.__getattribute__(self, "calls").append(f"{name}{a}")
                return attr(*a, **kw)
            return wrapper
        return attr

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "_target"), name, value)


class BankAccount:
    def __init__(self, balance): self.balance = balance
    def deposit(self, amt): self.balance += amt; return self.balance
    def withdraw(self, amt):
        if amt > self.balance: raise ValueError("balance kam hai")
        self.balance -= amt; return self.balance

acc = LoggingProxy(BankAccount(1000))
acc.deposit(500)
acc.withdraw(200)
print("balance:", acc.balance)
print("call log:", acc.calls)
try:
    acc.withdraw(99999)
except ValueError as e:
    print("ValueError:", e, "| log:", acc.calls)
"""),
    md("""
## 11. Method resolution debugging tools

Jab bara hierarchy samajh na aaye, ye tools istemal karo:

| Tool | Kaam |
|---|---|
| `inspect.getmro(C)` | MRO tuple |
| `C.__mro__` / `C.mro()` | wahi cheez |
| `C.__bases__` | seedhe parents (MRO nahi) |
| `C.__subclasses__()` | direct children |
| `inspect.getsource(C.method)` | asli code kahan se aaya |
| `C.method.__qualname__` | method ka poora naam (kis class ka hai) |
| `vars(C)` / `C.__dict__` | sirf isi class ke members |
| `super(X, obj)` | manually chain ka koi hissa |
| `inspect.signature` | kwargs chain debug karne me |
"""),
    code("""
import inspect

class Root:
    def action(self): return "Root"

class Left(Root):
    def action(self): return "Left->" + super().action()

class Right(Root):
    def action(self): return "Right->" + super().action()

class Both(Left, Right): pass


def explain_mro(cls, method):
    print(f"MRO of {cls.__name__}: " + " -> ".join(c.__name__ for c in cls.__mro__))
    print(f"'{method}' kis kis class me mojood hai:")
    for c in cls.__mro__:
        if method in c.__dict__:
            fn = c.__dict__[method]
            print(f"   {c.__name__:<8} qualname={getattr(fn, '__qualname__', '?')}")
    winner = next(c for c in cls.__mro__ if method in c.__dict__)
    print(f"-> jeeta: {winner.__name__}")

explain_mro(Both, "action")
print("\\nnatija:", Both().action())
print("\\n__bases__ (sirf seedhe parents):", [c.__name__ for c in Both.__bases__])
print("Root ke direct subclasses:", [c.__name__ for c in Root.__subclasses__()])
print("vars(Both) me apna kuch nahi:", [k for k in vars(Both) if not k.startswith('__')])
print("\\nchain ko manually chalao:")
b = Both()
print("  super(Both, b).action() :", super(Both, b).action())
print("  super(Left, b).action() :", super(Left, b).action())
print("  super(Right, b).action():", super(Right, b).action())
"""),
    md("""
## 12. Abstract + mixin combos

ABC (contract) aur mixin (implementation) ko mila kar bohat saaf design banta hai:

- **ABC** kehti hai: "`raw_data()` lazmi do"
- **Mixin** kehta hai: "raw data se main JSON/CSV bana dunga"
- Concrete class: sirf `raw_data()` likhti hai, baqi sab muft

Isko **"abstract mixin"** ya "template mixin" kehte hain — mixin khud abstract method par depend karta hai.
`collections.abc` isi tarz par bani hui hai (`Sequence` mixin methods + abstract `__getitem__`).
"""),
    code("""
from abc import ABC, abstractmethod

class ExportMixin:
    # Abstract mixin: ye maanta hai ke host class raw_data() degi
    @abstractmethod
    def raw_data(self): ...

    def as_csv(self):
        rows = self.raw_data()
        head = ",".join(rows[0])
        body = "\\n".join(",".join(str(v) for v in r.values()) for r in rows)
        return head + "\\n" + body

    def as_json(self):
        return json.dumps(self.raw_data(), ensure_ascii=False)

    def row_count(self):
        return len(self.raw_data())


class Report(ExportMixin, ABC):        # ABC ke sath -> enforcement zinda
    @abstractmethod
    def title(self): ...


class SalesReport(Report):
    def title(self): return "Sales"
    def raw_data(self):
        return [{"city": "Lahore", "total": 4500}, {"city": "Multan", "total": 800}]


sr = SalesReport()
print(sr.title(), "| rows:", sr.row_count())
print(sr.as_csv())
print(sr.as_json())

# Adhoori class -> instantiate hi nahi hogi (ABC + abstract mixin dono ka faida)
class Incomplete(Report):
    def title(self): return "oops"      # raw_data nahi diya
try:
    Incomplete()
except TypeError as e:
    print("\\nTypeError:", e)
print("abstract set:", sorted(Incomplete.__abstractmethods__))
"""),
    md("""
## 13. Real example: Django-style class hierarchy

Django ke class-based views multiple inheritance ka **sabse mashhoor** amali istemal hain:

```
View  <-  TemplateResponseMixin  <-  ContextMixin  <-  ListView ...
```

Hum ek chhota "mini-Django" bana kar dekhenge ke `get_context_data()` me `super()` chain
kaise poora context jama karti hai — ye asli Django ka pattern hai.
"""),
    code("""
# ---------- mini framework ----------
class View:
    http_method_names = ["get", "post"]

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def dispatch(self, request):
        # method name se handler dhoondo (Django ka asli tareeqa)
        handler = getattr(self, request["method"].lower(), None)
        if handler is None:
            return {"status": 405, "body": "Method Not Allowed"}
        return handler(request)


class ContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        kwargs.setdefault("view", type(self).__name__)
        if self.extra_context:
            kwargs.update(self.extra_context)
        return kwargs                                   # chain ka aakhir


class TemplateResponseMixin:
    template_name = None

    def render_to_response(self, context):
        if not self.template_name:
            raise ValueError("template_name set karo")
        body = f"[{self.template_name}] " + ", ".join(f"{k}={v}" for k, v in sorted(context.items()))
        return {"status": 200, "body": body}


class TemplateView(TemplateResponseMixin, ContextMixin, View):
    def get(self, request):
        context = self.get_context_data(**request.get("params", {}))
        return self.render_to_response(context)


class MultipleObjectMixin(ContextMixin):
    # Ye ContextMixin ko extend karti hai aur super() se chain jari rakhti hai
    model_name = "object"
    paginate_by = None
    queryset = ()

    def get_queryset(self):
        return list(self.queryset)

    def get_context_data(self, **kwargs):
        objects = self.get_queryset()
        page = 1
        if self.paginate_by:
            objects = objects[: self.paginate_by]
            page = f"1/{-(-len(self.get_queryset()) // self.paginate_by)}"   # ceil division
        kwargs.update({f"{self.model_name}_list": objects, "count": len(objects), "page": page})
        return super().get_context_data(**kwargs)        # <-- chain upar bhejo


class ListView(TemplateResponseMixin, MultipleObjectMixin, View):
    def get(self, request):
        return self.render_to_response(self.get_context_data(**request.get("params", {})))


# ---------- app code ----------
class BookListView(ListView):
    template_name = "books.html"
    model_name = "book"
    paginate_by = 2
    queryset = ["Aab-e-Gum", "Raja Gidh", "Udaas Naslein", "Khuda Ki Basti"]
    extra_context = {"site": "kitab.pk"}


print("MRO:", " -> ".join(c.__name__ for c in BookListView.__mro__))
print()
print(BookListView().dispatch({"method": "GET", "params": {"q": "urdu"}}))
print()
print(TemplateView(template_name="home.html", extra_context={"user": "Ali"}).dispatch({"method": "GET"}))
print()
print(BookListView().dispatch({"method": "DELETE"}))

# Context chain ka saboot: teen classes ne context me apna hissa dala
ctx = BookListView().get_context_data(q="test")
print("\\njama hua context:", ctx)
assert set(ctx) == {"book_list", "count", "page", "view", "site", "q"}
print("[pass] super() chain ne teen mixins ka context merge kiya")
"""),
    md("""
## 14. Multiple inheritance ke risks aur rules of thumb

### Risks
1. **Name collision:** do parents me same method → chupchap ek jeet jata hai (silent bug)
2. **`__init__` signature clash:** ek positional args leti hai, doosri kwargs → chain toot jati hai
3. **Fragile base class:** base me method add karna subclasses ko tor sakta hai
4. **Non-cooperative class:** koi class `super().__init__()` na kare → chain wahin ruk jayegi
5. **Inconsistent MRO:** class define hi nahi hogi
6. **Debugging mushkil:** stack trace me 5 classes, samajh na aaye kaun chala
7. **`__slots__` conflict:** do parents ke non-empty `__slots__` → `TypeError` (layout conflict)

### Rules of thumb
1. **Ek** "asli" base class + baqi **stateless mixins** (Python community ka standard)
2. Mixins base se **pehle** likho
3. Hamesha `super()`, kabhi explicit parent call (mixin-friendly code)
4. `**kwargs` cooperative `__init__`, keyword-only params
5. Mixin ke method names **unique** rakho (`serialize_to_json` > `save`)
6. 2-3 se zyada mixins ho to composition par ghor karo
7. Diamond banane se pehle poochho: *"kya composition se ye simple ho jata?"*
8. Public API me MRO par depend na karo (documentation me likho ke kaunsa method override karna hai)
"""),
    code("""
# Risk 4: non-cooperative class chain tor deti hai
class Good:
    def __init__(self, **kw):
        super().__init__(**kw)
        self.good = True

class Rude:
    def __init__(self, **kw):
        # super().__init__() call NAHI kiya -> chain yahan khatam
        self.rude = True

class Tail:
    def __init__(self, **kw):
        super().__init__(**kw)
        self.tail = True

class Chain(Good, Rude, Tail):
    def __init__(self, **kw):
        super().__init__(**kw)

c = Chain()
print("MRO:", [k.__name__ for k in Chain.__mro__])
print("kaun kaun set hua:", {k: v for k, v in vars(c).items()})
print("-> 'tail' ghayab hai kyunki Rude ne super() call nahi kiya")

# Risk 2: signature clash
class PosArgs:
    def __init__(self, a, b):
        self.a, self.b = a, b

class KwArgs:
    def __init__(self, **kw):
        super().__init__(**kw)
        self.kw = kw

class Clash(KwArgs, PosArgs): pass
try:
    Clash(a=1)                       # PosArgs ko 'b' bhi chahiye
except TypeError as e:
    print("\\nTypeError:", e)

# Risk 7: __slots__ layout conflict
class S1:
    __slots__ = ("x",)
class S2:
    __slots__ = ("y",)
try:
    class S3(S1, S2): pass
except TypeError as e:
    print("TypeError:", e, "-> do non-empty __slots__ wale parents mix nahi hote")

# Hal: mixins me __slots__ = () rakho
class M1s:
    __slots__ = ()
    def hello(self): return "hi"
class S4(M1s, S1): pass
print("khaali __slots__ wale mixin ke sath theek:", S4().hello(), S4.__slots__ if hasattr(S4, '__slots__') else '(inherited)')
"""),
]

CELLS += [
    md("""
## 15. LeetCode Problems

Teen **iterator design** problems. Ye is notebook se kyun match karti hain?
Kyunki hum inko `collections.abc.Iterator` + apne mixins ke sath banayenge —
`super()`, MRO aur mixin composition ka amali istemal.

- **LC 173** — Binary Search Tree Iterator
- **LC 341** — Flatten Nested List Iterator
- **LC 284** — Peeking Iterator
"""),
    code("""
# ---- Ek chhota mixin jo teeno problems me kaam aayega ----
from collections.abc import Iterator

class CountingIteratorMixin:
    # Mixin: kitne elements consume hue, ye count karta hai.
    # NOTE: mixin ko host class se pehle likhna zaroori hai warna next() override nahi hoga.
    @property
    def consumed(self):
        if not hasattr(self, "_consumed"):
            self._consumed = 0
        return self._consumed

    def next(self):
        val = super().next()                 # chain: asli implementation
        self._consumed = self.consumed + 1
        return val


class PyIteratorMixin:
    # LeetCode ka API hasNext()/next() hai; Python ka __iter__/__next__.
    # Ye mixin dono ko jodta hai -> object for-loop me bhi chalta hai.
    def __iter__(self):
        return self

    def __next__(self):
        if not self.hasNext():
            raise StopIteration
        return self.next()

print("mixins tayyar:", CountingIteratorMixin.__name__, "|", PyIteratorMixin.__name__)
"""),
    md("""
### LC 173. Binary Search Tree Iterator — Medium

Link: https://leetcode.com/problems/binary-search-tree-iterator/

**Problem (Roman Urdu):** BST par ek iterator banao: `next()` **sorted order** me agli value de,
`hasNext()` bataye ke aur value bachi hai ya nahi. `next()` aur `hasNext()` **average O(1)**
me chalne chahiye aur memory `O(h)` (tree ki height) honi chahiye.

**Approach (controlled recursion → explicit stack):**
1. In-order traversal sorted order deti hai. Magar poori traversal pehle kar lena `O(n)` memory legi.
2. Trick: **stack** me sirf "left spine" rakho — root se le kar sabse baayen node tak.
3. `next()`: stack se pop karo (yehi sabse chhoti bachi hui value), phir us node ke
   **right child ka left spine** stack me daal do.
4. `hasNext()`: stack khaali nahi to `True`.

**Complexity:** `next()` **amortized O(1)** (har node exactly ek baar push/pop hoti hai),
`hasNext()` `O(1)`, space `O(h)` — balanced tree me `O(log n)`.
"""),
    code("""
class TreeNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def build_bst(values):
    # helper: values ko BST me insert karo (test data banane ke liye)
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
                    cur.left = node; break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = node; break
                cur = cur.right
    return root


class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)            # left spine stack me

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        node = self.stack.pop()          # sabse chhoti bachi hui value
        self._push_left(node.right)      # right subtree ka left spine
        return node.val

    def hasNext(self) -> bool:
        return len(self.stack) > 0


# ---- asserts (LeetCode ka official example: [7,3,15,null,null,9,20]) ----
root = TreeNode(7, TreeNode(3), TreeNode(15, TreeNode(9), TreeNode(20)))
it = BSTIterator(root)
assert it.next() == 3
assert it.next() == 7
assert it.hasNext() is True
assert it.next() == 9
assert it.hasNext() is True
assert it.next() == 15
assert it.hasNext() is True
assert it.next() == 20
assert it.hasNext() is False

# edge cases: single node, skewed tree, random cross-check
one = BSTIterator(TreeNode(1))
assert (one.next(), one.hasNext()) == (1, False)

import random
random.seed(11)
vals = random.sample(range(1000), 60)
bst = build_bst(vals)
out, it2 = [], BSTIterator(bst)
while it2.hasNext():
    out.append(it2.next())
assert out == sorted(vals), "in-order traversal sorted honi chahiye"
print("LC 173 ke saare asserts pass [pass] | space O(h), max stack depth chhota raha")


# ---- Mixins ke sath wahi iterator (MRO ka amali faida) ----
class PyBSTIterator(CountingIteratorMixin, PyIteratorMixin, BSTIterator):
    pass

pit = PyBSTIterator(root)
print("MRO:", [c.__name__ for c in PyBSTIterator.__mro__])
print("for-loop me chal gaya:", [v for v in pit], "| consumed:", pit.consumed)
assert list(PyBSTIterator(root)) == [3, 7, 9, 15, 20]
# __iter__ + __next__ mojood hain -> collections.abc.Iterator ka structural check pass (NB1 ka __subclasshook__)
assert isinstance(PyBSTIterator(root), Iterator) is True
print("[pass] mixin + LeetCode class ka combo")
"""),
    md("""
### LC 341. Flatten Nested List Iterator — Medium

Link: https://leetcode.com/problems/flatten-nested-list-iterator/

**Problem (Roman Urdu):** Ek nested list di gayi hai (`[[1,1],2,[1,1]]`) jiske elements
ya integer hote hain ya phir aur nested list. Iterator banao jo saare integers **flat order** me de.

**Do approaches:**

**A) Eager flatten (aasan):** constructor me poori recursion kar ke flat list bana lo.
Time `O(n)` upfront, space `O(n)`. Interview me pehle yehi batao.

**B) Lazy stack (behtar, "follow-up" ka jawab):**
1. Stack me **reversed** list daalo (taake pop se pehla element mile)
2. `hasNext()`: top ko dekho — agar list hai to expand karo (pop + reversed push), repeat
3. Integer top par aa jaye to `True`
4. `next()`: `hasNext()` yakeeni banao, phir pop kar ke value do

Lazy version ka faida: agar user sirf pehle 2 elements maange to poori structure traverse nahi hoti.

**Complexity:** dono me total `O(n)` amortized. Lazy me space `O(d + k)` (depth + top-level items),
eager me `O(n)`.
"""),
    code("""
# LeetCode ka NestedInteger interface (local mock)
class NestedInteger:
    def __init__(self, value=None):
        self._int = value if isinstance(value, int) else None
        self._list = [] if self._int is None else None
        if isinstance(value, list):
            self._list = [NestedInteger(v) for v in value]

    def isInteger(self): return self._int is not None
    def getInteger(self): return self._int
    def getList(self): return self._list
    def __repr__(self): return str(self._int) if self.isInteger() else str(self._list)


# ---------- A) Eager approach ----------
class NestedIteratorEager:
    def __init__(self, nestedList):
        self.flat = []
        self._flatten(nestedList)
        self.i = 0

    def _flatten(self, lst):
        for ni in lst:
            if ni.isInteger():
                self.flat.append(ni.getInteger())
            else:
                self._flatten(ni.getList())       # recursion
    def next(self):
        self.i += 1
        return self.flat[self.i - 1]
    def hasNext(self): return self.i < len(self.flat)


# ---------- B) Lazy stack approach ----------
class NestedIterator:
    def __init__(self, nestedList):
        # reversed daalo taake list.pop() se pehla element mile
        self.stack = list(reversed(nestedList))

    def hasNext(self) -> bool:
        while self.stack:
            top = self.stack[-1]
            if top.isInteger():
                return True                       # integer tayyar hai
            self.stack.pop()                      # list thi -> khol do
            self.stack.extend(reversed(top.getList()))
        return False

    def next(self) -> int:
        if not self.hasNext():                    # LeetCode guarantee deta hai, magar safe rehna behtar
            raise StopIteration
        return self.stack.pop().getInteger()


def make_nested(py_list):
    return [NestedInteger(x) for x in py_list]

# ---- asserts (LeetCode ke official examples) ----
for Impl in (NestedIterator, NestedIteratorEager):
    it = Impl(make_nested([[1, 1], 2, [1, 1]]))
    out = []
    while it.hasNext():
        out.append(it.next())
    assert out == [1, 1, 2, 1, 1], (Impl.__name__, out)

    it = Impl(make_nested([1, [4, [6]]]))
    out = []
    while it.hasNext():
        out.append(it.next())
    assert out == [1, 4, 6], (Impl.__name__, out)

    # edge cases: khaali list, khaali nested lists, deep nesting
    assert Impl(make_nested([])).hasNext() is False
    assert Impl(make_nested([[], [[]], []])).hasNext() is False
    deep = Impl(make_nested([[[[[5]]]], 6]))
    out = []
    while deep.hasNext():
        out.append(deep.next())
    assert out == [5, 6]

print("LC 341 ke saare asserts pass (lazy + eager dono) [pass]")

# Lazy ka faida: sirf 1 element maango to poora structure expand nahi hota
lazy = NestedIterator(make_nested([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
first = lazy.next()
print("pehla element:", first, "| stack me abhi bhi un-expanded lists:", len(lazy.stack))
"""),
    md("""
### LC 284. Peeking Iterator — Medium

Link: https://leetcode.com/problems/peeking-iterator/

**Problem (Roman Urdu):** Ek mojood iterator ko wrap karo aur usme `peek()` add karo —
jo **agli value dikhaye magar aage na barhe**. `next()` aur `hasNext()` bhi kaam karein.

**Approach (one-element lookahead / buffering):**
1. Andar wale iterator ko `self.it` me rakho aur ek **buffer** `self._peeked` (+ flag) banao
2. `peek()`: buffer khaali ho to andar se ek element nikal kar buffer me rakh do, phir wapas karo
3. `next()`: buffer bhara ho to wahi do (aur buffer khaali karo), warna andar se seedha lo
4. `hasNext()`: buffer bhara ho ya andar wala `hasNext()` `True` de

**Ye "delegation" ka classic example hai** (Section 10 wala concept):
hum inheritance nahi, **composition + forwarding** use kar rahe hain.

**Complexity:** teeno operations `O(1)`, extra space `O(1)`.
"""),
    code("""
class LeetIterator:
    # LeetCode ka diya hua base Iterator (hasNext/next API)
    def __init__(self, nums):
        self._nums = list(nums)
        self._i = 0
    def hasNext(self): return self._i < len(self._nums)
    def next(self):
        self._i += 1
        return self._nums[self._i - 1]


_SENTINEL = object()

class PeekingIterator:
    def __init__(self, iterator):
        self.it = iterator                     # composition (delegation)
        self._buf = _SENTINEL                  # None value bhi valid ho sakti hai -> sentinel behtar

    def peek(self):
        if self._buf is _SENTINEL:
            self._buf = self.it.next()         # ek element aage se le kar rakh liya
        return self._buf

    def next(self):
        if self._buf is not _SENTINEL:
            val, self._buf = self._buf, _SENTINEL
            return val
        return self.it.next()

    def hasNext(self):
        return self._buf is not _SENTINEL or self.it.hasNext()

    # ---- baqi sab andar wale iterator ko forward kar do ----
    def __getattr__(self, name):
        return getattr(self.__dict__["it"], name)


# ---- asserts (LeetCode ka official example: [1,2,3]) ----
pi = PeekingIterator(LeetIterator([1, 2, 3]))
assert pi.next() == 1
assert pi.peek() == 2
assert pi.next() == 2          # peek ne aage nahi barhaya tha
assert pi.next() == 3
assert pi.hasNext() is False

# edge cases
pi2 = PeekingIterator(LeetIterator([9]))
assert pi2.hasNext() is True
assert pi2.peek() == 9
assert pi2.hasNext() is True   # peek ke baad bhi hasNext True
assert pi2.next() == 9
assert pi2.hasNext() is False

# do baar peek karna idempotent hona chahiye
pi3 = PeekingIterator(LeetIterator([4, 5]))
assert pi3.peek() == pi3.peek() == 4
assert pi3.next() == 4 and pi3.next() == 5

# khaali iterator
assert PeekingIterator(LeetIterator([])).hasNext() is False

# None values ke sath bhi theek (isi liye sentinel istemal kiya)
class NoneIter(LeetIterator): pass
pn = PeekingIterator(NoneIter([None, 1]))
assert pn.peek() is None and pn.next() is None and pn.next() == 1
print("LC 284 ke saare asserts pass [pass]")

# delegation ka saboot: andar wale iterator ka private attribute bhi forward hua
pf = PeekingIterator(LeetIterator([1, 2, 3]))
print("forwarded attribute _nums:", pf._nums)
"""),
]

CELLS += [
    md("""
## 16. Interview Questions & Answers

**Q1. MRO kya hai?**
Method Resolution Order — wo linear tarteeb jis me Python attribute/method dhoondta hai
(`Cls.__mro__`). Multiple inheritance me faisla karti hai kaun sa method jeetega aur `super()` ka next kaun hai.

**Q2. Python kaunsa MRO algorithm use karta hai?**
**C3 linearization** (Python 2.3 se, new-style classes). `L[C] = C + merge(L[B1]...L[Bn], [B1...Bn])`.
Teen guarantees: local precedence order, monotonicity, har class ek baar.

**Q3. C3 ke merge ka rule ek line me?**
Pehli list ka head lo; agar wo kisi doosri list ki **tail** me ho to chhor kar agli list ka head try karo;
warna output me daal kar sab lists se hata do. Koi valid head na mile → `TypeError`.

**Q4. Diamond problem kya hai aur Python isko kaise hal karta hai?**
Do parents ek grandparent se aate hain → grandparent do baar chal sakta hai. Python MRO ko **linear**
banata hai aur `super()` "next in MRO" call karta hai, is liye har class **exactly ek baar** chalti hai.

**Q5. `super()` ka asli matlab?**
"Parent class" nahi — `type(self).__mro__` me **current class ke baad** wali class.
Isi liye ek mixin apni sibling class ko call kar sakta hai jise wo jaanti bhi nahi.

**Q6. 0-arg `super()` andar se kaise kaam karta hai?**
Compiler method ke liye `__class__` closure cell banata hai (jis class me method define hua),
aur `super()` us cell + pehle argument (`self`) se `super(__class__, self)` bana leta hai.
Class body ke bahar define kiya function `super()` par `RuntimeError` dega.

**Q7. `super(A, self)` aur `super(A, B)` me farq?**
`super(A, self)` — bound to instance (instance methods). `super(A, B)` jahan `B` class ho —
bound to class, `classmethod` chain ke liye. Dono me lookup `A` ke **baad** se shuru hota hai.

**Q8. Explicit `Parent.method(self)` kab masla banta hai?**
Diamond me double-call, refactor par toot jata hai, mixin chain tor deta hai,
aur galat class ka naam likhne par infinite recursion. Multiple inheritance me hamesha `super()`.

**Q9. Cooperative multiple inheritance kya hai?**
Design jisme har class `**kwargs` leti hai, apne args consume karti hai, aur `super().__init__(**kwargs)`
se chain aage barhati hai — is tarah har class initialize hoti hai bina ek doosre ko jaane.

**Q10. `TypeError: Cannot create a consistent MRO` kab aata hai?**
Jab bases ki tarteeb C3 ke constraints ko tor de — jaise `class X(A, B)` jahan `B`, `A` ki subclass hai,
ya do parents ek doosre ki tarteeb par mutazad hon.

**Q11. Mixin kya hai aur normal base class se farq?**
Mixin chhoti, stateless, akeli use na hone wali class hoti hai jo **capability** ("can-do") deti hai;
base class **identity** ("is-a") deti hai. Mixin ka naam `...Mixin` hota hai aur wo base se pehle likha jata hai.

**Q12. Mixin ki tarteeb kyun matter karti hai?**
Kyunki MRO left-to-right banta hai — jo pehle likha uska method pehle milta hai.
Base class ko pehle likh do to mixin ke overrides kabhi nahi chalenge.

**Q13. Mixin me `__init__` rakhna chahiye?**
Behtar hai na rakho (lazy init ya class attributes use karo). Agar zaroori ho to
`def __init__(self, *, x=..., **kw): super().__init__(**kw)` — cooperative style.

**Q14. "Favor composition over inheritance" ka matlab?**
Inheritance compile-time par fix hoti hai aur tight coupling deti hai; composition runtime par
badalti hai, test karna aasan hai, aur `2^n` class explosion se bachati hai. Inheritance sirf asli "is-a" ke liye.

**Q15. Delegation kya hai aur `__getattr__` ka role?**
Delegation = kaam andar wale object ko forward karna. `__getattr__` sirf **miss** hone par chalta hai,
is liye boilerplate wrappers ki zaroorat khatam. Magar **dunder methods forward nahi hote** (type par lookup hota hai).

**Q16. `__getattr__` vs `__getattribute__`?**
`__getattribute__` har access par chalta hai (override karna khatarnak, recursion aasan);
`__getattr__` sirf normal lookup fail hone par. Delegation ke liye `__getattr__`.

**Q17. Kya Python me interface aur mixin ek hi cheez hain?**
Nahi. Interface (`ABC`/`Protocol`) sirf **contract** deta hai; mixin **implementation** deta hai.
Aksar dono milte hain: ABC contract + mixin default implementation (jaise `collections.abc`).

**Q18. `__init_subclass__` MRO ke lehaz se kya karta hai?**
Ye parent me define hota hai aur **har subclass banane par** chalta hai (metaclass ki zaroorat nahi) —
plugin registry, validation, ya subclass ke attributes check karne ke liye. Implicitly `classmethod` hota hai.

**Q19. Do parents ke non-empty `__slots__` ko mix karne par kya hota hai?**
`TypeError: multiple bases have instance lay-out conflict`. Isi liye mixins me `__slots__ = ()` rakha jata hai.

**Q20. `super()` ke bagair MRO ka faida le sakte hain?**
Haan — `next(iter(type(self).__mro__[...]))` type ki hackery mumkin hai magar bewaqoofi hai.
`super()` hi standard, safe aur readable tareeqa hai.

**Q21. Practically kitne mixins tak theek hai?**
2-4 chhote, unique-named, stateless mixins theek hain. Us se zyada ho to composition
ya strategy pattern par shift karo — warna debugging duswaar ho jati hai.
"""),
    md("""
## 17. Practice Exercises (khud karo)

1. **Haath se MRO nikalo, phir check karo:**
   `class A; class B(A); class C(A); class D(B,C); class E(D,C)` — `E` ka MRO likho.
   *Hint:* pehle kaghaz par C3 chalao, phir `E.__mro__` se compare karo. (`E(D, C)` valid hai?)

2. **Inconsistent MRO** banao jaan boojh kar 3 classes se, aur error message note karo.

3. **`JsonMixin` + `XmlMixin`** banao jo `serialize()` ko chain karein (`super()` ke sath),
   phir dono orders try kar ke output ka farq likho.

4. **Cooperative `__init__` chain:** 4 classes ka diamond banao aur ek `trace` list me har
   `__init__` ka naam append karo. Sabit karo ke har class **ek** baar chali.
   *Hint:* `trace.append(type(self).__name__ + ":" + __class__.__name__)`.

5. **`Rude` class fix karo:** Section 14 wali `Rude` class ko cooperative banao aur
   dikhao ke `tail` ab set ho jata hai.

6. **`__getattr__` delegation:** `SafeDict` banao jo andar `dict` rakhe, missing key par
   exception ki jagah `None` de, magar baqi saare dict methods forward kare.
   *Hint:* `keys/values/items` forward honge, `[]` ke liye `__getitem__` khud likhna parega.

7. **Mixin + ABC:** `Repository(ABC)` (abstract `all()`) + `FilterMixin` (`where(**kw)`) +
   `PaginateMixin` (`page(n, size)`). `MemoryRepository` bana kar chain test karo.

8. **Class explosion refactor:** 3 features (compress, encrypt, sign) ko pehle inheritance se
   likho (8 classes!), phir composition se (3 objects). Lines of code compare karo.

9. **LC 173 extend:** `BSTIterator` me `prev()` (reverse direction) add karo.
   *Hint:* do stacks ya parent pointers.

10. **LC 284 extend:** `PeekingIterator` ko generic banao jo Python ke kisi bhi iterable par chale
    (`__iter__`/`__next__` support ke sath) — aur `peek(k)` (k elements aage) support kare.

11. **MRO explainer tool:** function likho `why(cls, method)` jo bataye kaunsi class ka method chalega
    aur `super()` ki poori chain print kare.
"""),
    code("""
# ---- Exercise 1, 4 aur 11 ka reference solution ----

# Ex 1: haath se: L[E] = E + merge(L[D], L[C], [D, C])
#   L[D] = [D, B, C, A, object] ; L[C] = [C, A, object]
#   head D -> lo. phir merge([B,C,A,object], [C,A,object], [C])
#   head B -> lo. head C -> ab kisi tail me nahi -> lo. phir A, object
#   L[E] = [E, D, B, C, A, object]
class A2: pass
class B2(A2): pass
class C2(A2): pass
class D2(B2, C2): pass
class E2(D2, C2): pass

expected = ["E2", "D2", "B2", "C2", "A2", "object"]
print("E2 MRO:", [c.__name__ for c in E2.__mro__])
assert [c.__name__ for c in E2.__mro__] == expected
print("[pass] Ex1 — haath ka hisaab sahi tha")


# Ex 4: diamond me har __init__ ek baar
trace = []
class T1:
    def __init__(self, **kw):
        super().__init__(**kw); trace.append("T1")
class T2(T1):
    def __init__(self, **kw):
        super().__init__(**kw); trace.append("T2")
class T3(T1):
    def __init__(self, **kw):
        super().__init__(**kw); trace.append("T3")
class T4(T2, T3):
    def __init__(self, **kw):
        super().__init__(**kw); trace.append("T4")

T4()
print("\\nEx4 trace:", trace)
assert trace == ["T1", "T3", "T2", "T4"], trace       # bottom-up: T1 pehle complete hui
assert len(set(trace)) == len(trace), "har class exactly ek baar"
print("[pass] Ex4 — cooperative chain")


# Ex 11: MRO explainer
def why(cls, method):
    owners = [c for c in cls.__mro__ if method in c.__dict__]
    if not owners:
        return f"{method} kahin nahi mila"
    chain = " -> ".join(c.__name__ for c in owners)
    return f"{cls.__name__}.{method}() chalega: {owners[0].__name__} | super() chain: {chain}"

print("\\n" + why(T4, "__init__"))
print(why(E2, "__init__"))
print(why(Both, "action"))
"""),
    md("""
## 18. Summary / Cheat-sheet

### MRO
```python
Cls.__mro__            # tuple (linear order)
Cls.mro()              # list
inspect.getmro(Cls)
Cls.__bases__          # sirf seedhe parents
Cls.__subclasses__()   # direct children
```

### C3 formula
```
L[C] = C + merge(L[B1], ..., L[Bn], [B1, ..., Bn])
merge: head lo jo kisi doosri list ki TAIL me na ho -> output, sab lists se hatao
       koi valid head na mile -> TypeError (inconsistent MRO)
```

### `super()`
| Form | Kab |
|---|---|
| `super().m()` | Default — class body ke andar (0-arg) |
| `super(Cls, self).m()` | Explicit; monkey-patched functions me lazmi |
| `super(Cls, SubCls).m()` | `classmethod` chain |
| `super(Mid, self).m()` | `Mid` ko **skip** kar ke aage jao |

- `super()` = **MRO ka next**, parent nahi
- 0-arg `super()` `__class__` closure cell par depend karta hai → class body ke bahar `RuntimeError`
- `staticmethod` me 0-arg `super()` nahi chalta

### Cooperative `__init__` recipe
```python
class Mixin:
    def __init__(self, *, my_arg=None, **kwargs):
        super().__init__(**kwargs)     # baqi aage bhejo
        self.my_arg = my_arg           # apna consume karo
```
Chain ke aakhir me `object.__init__()` — extra kwargs pahunchein to `TypeError`.

### Mixin rules
| # | Rule |
|---|---|
| 1 | Naam `...Mixin` |
| 2 | **Base class se pehle** likho: `class C(MixinA, MixinB, Base)` |
| 3 | Stateless rakho (ya cooperative `__init__`) |
| 4 | `__slots__ = ()` |
| 5 | Method names unique (collision se bacho) |
| 6 | Hamesha `super()`, kabhi explicit parent |
| 7 | 3+ mixins → composition socho |

### Faisla: inheritance ya composition?
```
"X ek Y hai" + shared code             -> inheritance / ABC
"X, Y kar sakta hai" (cross-cutting)   -> Mixin
"X, Y istemal karta hai" / runtime swap -> Composition (+ delegation)
Feature combinations ka explosion?      -> Composition (policies/strategies)
Boilerplate wrappers zyada?             -> __getattr__ delegation (dunders manually)
```

### Common errors ki fehrist
| Error | Wajah |
|---|---|
| `TypeError: Cannot create a consistent MRO` | Bases ki tarteeb C3 ke khilaaf |
| `RuntimeError: super(): __class__ cell not found` | Function class body ke bahar define hua |
| `TypeError: object.__init__() takes exactly one argument` | Koi kwarg kisi ne consume nahi kiya |
| `TypeError: multiple bases have instance lay-out conflict` | Do non-empty `__slots__` parents |
| `AttributeError` mixin par | Mixin akela use kiya (chain ka base nahi tha) |
| Silent wrong method | Mixin base ke baad likh diya |

### Iske baad kya (next notebook)
`03_Dataclasses_Enums_NamedTuple_Slots_aur_Immutability.ipynb` — modern Python data modeling:
`@dataclass`, `field()`, `frozen`, `__slots__`, `Enum`, `NamedTuple`, aur immutability ke patterns.
"""),
]

save(r"OOP in Python/Intermediate/02_MRO_Multiple_Inheritance_Mixins_and_super_Deep.ipynb", CELLS)
