"""Generator: OOP in Python / Intermediate / 01 Abstraction, ABC, Interfaces aur Protocols."""

import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

CELLS = []

CELLS += [
    md("""
# Abstraction, ABC, Interfaces aur Protocols (Intermediate OOP)

**Level:** Intermediate | **Language:** Python 3.14

Bhai, ye notebook OOP ke us hisse par hai jahan se "code likhna" se "system design karna" shuru hota hai.
Abstraction ka matlab sirf `abstractmethod` likhna nahi — asal matlab hai **contract** define karna:
"jo bhi is family ka member banega, wo ye kaam zaroor karega".

## Is notebook me kya seekhenge

- Abstraction kya hai aur **encapsulation se farq** (interview ka favourite sawal)
- `abc` module: `ABC` vs `ABCMeta`, `@abstractmethod`
- Abstract class ko instantiate karne par kya hota hai (live error demo)
- Abstract + concrete methods ka mix (partial implementation)
- Abstract **properties**, abstract **classmethod / staticmethod**
- Python me "interface" ka concept (sirf abstract methods wali class)
- `NotImplementedError` wala purana style vs `abc` — farq aur trade-off
- **Duck typing vs nominal typing**
- `typing.Protocol` = structural typing, `@runtime_checkable`
- ABC vs Protocol: kab kaun (comparison table)
- `collections.abc` (`Iterable`, `Sized`, `Container`, `Sequence`, `Mapping`, `MutableMapping`) se apni classes
- `__subclasshook__` aur `ABCMeta.register` (virtual subclass)
- **Template Method** pattern aur **Dependency Inversion** ka taaruf
- Real projects: `Shape`, `PaymentGateway` (Stripe/JazzCash/EasyPaisa), `Notifier`, `DataExporter`, plugin architecture
- **LeetCode:** 208, 211, 1146 (design problems — abstraction ke sath)
- Interview Q&A + practice exercises + cheat-sheet

## Prerequisites

- Classes, `__init__`, instance vs class attributes
- Inheritance aur method overriding, `super()` ki basic samajh
- Dunder methods ka basic idea (`__len__`, `__iter__`)
- Decorators ka basic idea (`@property` kaam kar leta ho)
"""),
    md("""
## 1. Abstraction kya hai?

**Kya hai:** Abstraction ka matlab hai *"zaroori cheezein dikhao, faaltu tafseel chhupao"* —
user ko **kya** hota hai bataana, **kaise** hota hai chhupana.

Jaise gaari ka steering: tumhe `steer_left()` chahiye. Rack-and-pinion gear ratio se
tumhara koi lena dena nahi. Steering wheel = **abstraction**.

**Kyun / kahan use hota hai:**
- Bara system chhote contracts me tootta hai → team parallel kaam kar sakti hai
- Implementation badal do, caller code nahi badalta (Stripe se JazzCash par shift)
- Testing asaan: asli gateway ki jagah fake gateway inject kar do

### Abstraction vs Encapsulation (ye sawal 100% aayega)

| | Abstraction | Encapsulation |
|---|---|---|
| Sawal ka jawab | *Kya* expose karein? | *Kaise* protect karein? |
| Level | Design level (class/interface) | Implementation level (attributes/methods) |
| Tool | `abc`, `Protocol`, base classes | `_private`, `__name_mangling`, `@property` |
| Maqsad | Complexity chhupana | Data ki safety / invariants |
| Misaal | `PaymentGateway.charge()` ka contract | `self.__api_key` bahar se access na ho |

Ek line me: **Encapsulation data ko chhupata hai, abstraction complexity ko.**
Dono ka natija milta julta lagta hai (kuch cheez chhup gayi) lekin **niyat** alag hai.
"""),
    code("""
# ---- Abstraction ka rozmarra ka example: driver ko engine ki tafseel nahi chahiye ----

class Car:
    def __init__(self, model):
        self.model = model
        self.__fuel = 40          # encapsulation: private-ish state (name mangling)
        self.__engine_on = False  # bahar se seedha chhera nahi ja sakta

    # ---- Public API = abstraction (sirf 3 buttons) ----
    def start(self):
        self.__ignite()           # andar ka complex kaam chhupa hua hai
        return f"{self.model} start ho gayi"

    def drive(self, km):
        if not self.__engine_on:
            return "pehle start karo"
        self.__burn_fuel(km)      # fuel calculation ki tafseel user se chhupi hai
        return f"{km} km chali, fuel bacha {self.__fuel:.1f}L"

    def fuel_status(self):        # controlled read access (encapsulation)
        return self.__fuel

    # ---- Private helpers = tafseel (implementation detail) ----
    def __ignite(self):
        self.__engine_on = True

    def __burn_fuel(self, km):
        self.__fuel = max(0.0, self.__fuel - km * 0.08)   # 8L / 100km


c = Car("Corolla")
print(c.start())
print(c.drive(150))
print("fuel:", c.fuel_status())

# Encapsulation ka asar: private attribute ka asli naam mangle ho gaya hai
print("public dikhne wale members:", [a for a in dir(c) if not a.startswith("_")])
try:
    print(c.__fuel)               # ye fail hoga -> AttributeError
except AttributeError as e:
    print("AttributeError:", e)
"""),
    md("""
## 2. `abc` module: pehla abstract base class

**Kya hai:** `abc` = *Abstract Base Class*. Ye Python ka wo tool hai jisse tum keh sakte ho:
"is class ko seedha instantiate na karo; aur jo inherit karega wo ye methods **zaroor** likhega".

**Syntax:**

```python
from abc import ABC, abstractmethod

class Shape(ABC):                 # ABC se inherit = abstract base class
    @abstractmethod
    def area(self): ...           # sirf contract, body khaali
```

**Kaise kaam karta hai (andar ki baat):** `@abstractmethod` function par ek flag
(`__isabstractmethod__ = True`) lagata hai. `ABCMeta` metaclass class banate waqt
in flags ko jama karke `__abstractmethods__` (ek frozenset) banata hai.
`object.__new__` instantiate karte waqt dekhta hai ke ye set khaali hai ya nahi —
khaali na ho to `TypeError`.
"""),
    code("""
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    # NOTE: ABC se inherit kiya -> metaclass ABCMeta mil gaya
    @abstractmethod
    def area(self):
        # Contract: har shape apna area dega. Body ki zaroorat nahi.
        ...

    @abstractmethod
    def perimeter(self):
        ...


class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):                 # dono abstract methods implement kiye -> class concrete ban gayi
        return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self):
        return math.pi * self.r ** 2

    def perimeter(self):
        return 2 * math.pi * self.r


shapes = [Rectangle(3, 4), Circle(1)]
for s in shapes:
    # Caller ko farq nahi parta ye kaunsi shape hai -> abstraction ka faida
    print(type(s).__name__, "area =", round(s.area(), 3), "| perimeter =", round(s.perimeter(), 3))

print("Shape ke abstract methods:", sorted(Shape.__abstractmethods__))
print("Rectangle ke baqi abstract methods:", sorted(Rectangle.__abstractmethods__), "(khaali = concrete)")
"""),
    md("""
### 2.1 Abstract class instantiate karne par error (live demo)

Yahan log phaste hain: samajhte hain "abstract class banayi hai to instance ban jayega".
Nahi — jab tak **saare** abstract methods implement na hon, `TypeError` aayega.
Aur ye error **instantiation** par aata hai, class define karte waqt nahi.
"""),
    code("""
# 1) Poori abstract class ko instantiate karne ki koshish
try:
    s = Shape()
except TypeError as e:
    print("TypeError:", e)

# 2) Aadhi implementation wali subclass -> phir bhi abstract hi rahegi
class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def perimeter(self):            # sirf perimeter diya, area bhool gaye
        return self.a + self.b + self.c

print("Triangle abstract methods:", sorted(Triangle.__abstractmethods__))
try:
    t = Triangle(3, 4, 5)
except TypeError as e:
    print("TypeError:", e)          # 'area' missing bata dega

# 3) Note: CLASS ban gayi thi (define hone me koi error nahi aaya) -> error sirf instantiate par
print("Triangle class to mojood hai:", Triangle)

# 4) Ab area bhi de do -> chal parega
class Triangle2(Triangle):
    def area(self):
        s = self.perimeter() / 2                       # Heron's formula
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

t2 = Triangle2(3, 4, 5)
print("Triangle2 area:", t2.area(), "| ab abstract set khaali:", Triangle2.__abstractmethods__ == frozenset())
"""),
    md("""
## 3. `ABC` vs `ABCMeta` — farq kya hai?

- `ABCMeta` ek **metaclass** hai (classes banane wali machine).
- `ABC` ek **helper base class** hai jo bas `metaclass=ABCMeta` set kar deti hai.

```python
class A(ABC): ...                     # aasan tareeqa (99% cases)
class B(metaclass=ABCMeta): ...       # wahi cheez, seedha metaclass ke sath
```

**Kab `ABCMeta` seedha chahiye?** Jab tumhein **apna custom metaclass** chahiye jo `ABCMeta`
se inherit kare (e.g. registry + abstract enforcement dono), ya jab base class already
kisi doosre metaclass wali library se aa rahi ho.

**Gotcha:** Do asambandhit metaclasses ko mix karne par `TypeError: metaclass conflict`.
"""),
    code("""
from abc import ABCMeta

# Tareeqa A: ABC helper
class ExporterA(ABC):
    @abstractmethod
    def export(self, rows): ...

# Tareeqa B: seedha metaclass (bilkul same natija)
class ExporterB(metaclass=ABCMeta):
    @abstractmethod
    def export(self, rows): ...

print("A ka metaclass:", type(ExporterA).__name__, "| B ka metaclass:", type(ExporterB).__name__)
print("dono me abstractmethods:", ExporterA.__abstractmethods__, ExporterB.__abstractmethods__)

# Tareeqa C: custom metaclass jo ABCMeta ko extend karta hai -> registry + abstraction dono
class PluginMeta(ABCMeta):
    registry = {}                                  # har subclass yahan khud register hogi

    def __new__(mcls, name, bases, ns, **kw):
        cls = super().__new__(mcls, name, bases, ns, **kw)
        if bases and not cls.__abstractmethods__:   # sirf concrete subclasses register karo
            PluginMeta.registry[name.lower()] = cls
        return cls

class Plugin(metaclass=PluginMeta):
    @abstractmethod
    def run(self): ...

class CsvPlugin(Plugin):
    def run(self): return "csv chala"

class JsonPlugin(Plugin):
    def run(self): return "json chala"

print("auto registry:", sorted(PluginMeta.registry))
print(PluginMeta.registry["csvplugin"]().run())

# Gotcha: metaclass conflict
class Meta2(type): ...
try:
    class Broken(ExporterA, metaclass=Meta2): ...   # ABCMeta vs Meta2 -> conflict
except TypeError as e:
    print("TypeError:", e)
"""),
    md("""
## 4. Abstract + concrete methods ka mix (partial implementation)

Abstract class ka matlab "sab kuch khaali" nahi hai. Sabse taqatwar design hoti hai:
**kuch kaam base class khud kar de (shared logic), kuch subclass par chhor de (variable logic)**.

- **Concrete method** = common behaviour, dobara likhne ki zaroorat nahi (DRY)
- **Abstract method** = jo har subclass me lazmi mukhtalif hoga
- Base class abstract method ko **apne concrete method ke andar call** kar sakti hai (yehi Template Method pattern ki jarh hai)
"""),
    code("""
class Employee(ABC):
    bonus_rate = 0.10                       # class-level default (subclass override kar sakti hai)

    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    # ---- ABSTRACT: har employee type ka allowance formula alag hai ----
    @abstractmethod
    def allowances(self):
        ...

    # ---- CONCRETE: sab ke liye same hisaab (shared logic base me) ----
    def bonus(self):
        return self.base_salary * self.bonus_rate

    def gross_pay(self):
        # yahan base class ABSTRACT method ko call kar rahi hai -> subclass ka code chalega
        return self.base_salary + self.allowances() + self.bonus()

    def payslip(self):
        return f"{self.name:<10} base={self.base_salary:>7} allow={self.allowances():>6} gross={self.gross_pay():>8.0f}"


class Developer(Employee):
    bonus_rate = 0.15                       # override: dev ka bonus zyada
    def allowances(self):
        return 15000                        # internet + hardware allowance

class SalesPerson(Employee):
    def __init__(self, name, base_salary, sales):
        super().__init__(name, base_salary)
        self.sales = sales
    def allowances(self):
        return 5000 + 0.02 * self.sales     # commission based

for e in [Developer("Ali", 200000), SalesPerson("Sara", 120000, 900000)]:
    print(e.payslip())
"""),
    md("""
## 5. Abstract properties (`@property` + `@abstractmethod`)

Kabhi contract "method" nahi, **attribute jaisa** hona chahiye: `obj.name` na ke `obj.get_name()`.

**Syntax (order yaad rakho — ye #1 gotcha hai):**

```python
@property            # BAHAR
@abstractmethod      # ANDAR (property ke neeche)
def rate(self): ...
```

Ulta likha (`@abstractmethod` upar, `@property` neeche) to abstractness kho jati hai
kyunki `property` object par flag nahi lagta — Python enforce nahi karega.

Setter bhi abstract ho sakta hai; ya base me read-only property, subclass me writable.
"""),
    code("""
class Account(ABC):
    @property
    @abstractmethod
    def interest_rate(self):
        # Contract: har account apna rate batayega (attribute ki tarah access hoga)
        ...

    @property
    def yearly_interest(self):        # concrete property jo abstract property par bharosa karti hai
        return self.balance * self.interest_rate

    def __init__(self, balance):
        self.balance = balance


class Savings(Account):
    interest_rate = 0.11             # NOTE: plain class attribute bhi property ka contract poora kar deta hai

class TermDeposit(Account):
    def __init__(self, balance, months):
        super().__init__(balance)
        self.months = months

    @property
    def interest_rate(self):         # asli property ke tor par implement kiya
        return 0.14 if self.months >= 12 else 0.12


s, td = Savings(100_000), TermDeposit(100_000, 12)
print("savings:", s.interest_rate, "->", s.yearly_interest)
print("term   :", td.interest_rate, "->", td.yearly_interest)

# Gotcha demo: decorators ka ulta order -> modern Python me foran error
try:
    class Loose(ABC):
        @abstractmethod              # GALAT order: pehle abstractmethod, phir property
        @property
        def tag(self): ...
except AttributeError as e:
    # property object read-only hai, is liye abstractmethod uspar flag nahi laga sakta
    print("AttributeError:", e)
    print("-> sabaq: @property BAHAR (upar), @abstractmethod ANDAR (neeche)")

class Reversed(ABC):
    @property
    def tag(self):                   # ye bilkul abstract nahi -> koi enforcement nahi
        return "?"
print("Reversed abstract set:", Reversed.__abstractmethods__, "<- khaali, is liye instantiate ho jayega")
print("instance ban gaya:", Reversed().tag)
"""),
    md("""
## 6. Abstract `classmethod` aur `staticmethod`

`abstractmethod` ko `classmethod` / `staticmethod` ke sath bhi mila sakte ho.
**Rule wahi:** `@abstractmethod` sabse **andar** (neeche) hona chahiye.

```python
@classmethod
@abstractmethod
def from_dict(cls, d): ...
```

Kahan kaam aata hai: **alternative constructors** ka contract
(`from_json`, `from_row`, `parse`) — "har subclass apni parsing khud dega".

(Purane `@abstractclassmethod` / `@abstractstaticmethod` **deprecated** hain — mat use karo.)
"""),
    code("""
class Serializer(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls, data):        # alternative constructor ka contract
        ...

    @staticmethod
    @abstractmethod
    def file_extension():            # utility ka contract (self/cls ki zaroorat nahi)
        ...

    @abstractmethod
    def to_dict(self):
        ...

    def describe(self):              # concrete helper jo dono abstract cheezon ko use karta hai
        return f"{type(self).__name__} -> .{self.file_extension()} | {self.to_dict()}"


class UserRecord(Serializer):
    def __init__(self, name, city):
        self.name, self.city = name, city

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data.get("city", "unknown"))   # missing key ka default

    @staticmethod
    def file_extension():
        return "json"

    def to_dict(self):
        return {"name": self.name, "city": self.city}


u = UserRecord.from_dict({"name": "Bilal", "city": "Lahore"})
print(u.describe())
print(UserRecord.from_dict({"name": "Ayesha"}).to_dict())     # city default lag gaya

# Contract tor kar dekho: staticmethod implement nahi kiya
class BadRecord(Serializer):
    @classmethod
    def from_dict(cls, data): return cls()
    def to_dict(self): return {}
try:
    BadRecord()
except TypeError as e:
    print("TypeError:", e)
"""),
]

CELLS += [
    md("""
## 7. Python me "interface" ka concept

Java/C# me alag keyword hota hai `interface`. Python me **keyword nahi** — hum convention se banate hain:

> **Interface = abstract class jisme sirf abstract methods hon, koi state (`__init__` data) na ho.**

Aisi class ka maqsad sirf **contract** batana hai, code share karna nahi.

**Naming convention (industry):** `PaymentGateway`, ya explicit `IPaymentGateway` / `...Interface` /
`...ABC`. Python community zyada tar bina `I` prefix likhti hai.

**Interview tip:** "Python me interface kaise banate ho?" ka best jawab:
*"Do tareeqe — nominal: `ABC` with only abstract methods; structural: `typing.Protocol`.
Choti internal cheezon ke liye duck typing hi kaafi hai."*
"""),
    code("""
# ---- Pure interface: sirf contract, koi state nahi ----
class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount, currency="PKR"):
        ...

    @abstractmethod
    def refund(self, txn_id):
        ...


class StripeGateway(PaymentGateway):
    def charge(self, amount, currency="PKR"):
        return {"txn": "stripe_1001", "amount": amount, "currency": currency, "status": "ok"}
    def refund(self, txn_id):
        return {"txn": txn_id, "status": "refunded"}


class JazzCashGateway(PaymentGateway):
    def charge(self, amount, currency="PKR"):
        fee = round(amount * 0.015, 2)                 # mobile wallet ki fee
        return {"txn": "jc_5501", "amount": amount + fee, "currency": currency, "status": "ok"}
    def refund(self, txn_id):
        return {"txn": txn_id, "status": "manual_review"}   # wallet refund manual hota hai


class EasyPaisaGateway(PaymentGateway):
    def charge(self, amount, currency="PKR"):
        return {"txn": "ep_7702", "amount": amount, "currency": currency, "status": "pending"}
    def refund(self, txn_id):
        return {"txn": txn_id, "status": "refunded"}


def checkout(gateway: PaymentGateway, amount):
    # Ye function kisi bhi gateway ke sath kaam karega -> polymorphism via interface
    res = gateway.charge(amount)
    return f"{type(gateway).__name__:<18} -> {res}"

for gw in [StripeGateway(), JazzCashGateway(), EasyPaisaGateway()]:
    print(checkout(gw, 2500))
"""),
    md("""
## 8. `NotImplementedError` (purana style) vs `abc`

Purana tareeqa:

```python
class Shape:
    def area(self):
        raise NotImplementedError("subclass implement kare")
```

| | `NotImplementedError` style | `abc` style |
|---|---|---|
| Error kab pakra jata hai | **Runtime** — jab method call ho | **Instantiation** par (jaldi, safe) |
| Base class instantiate ho sakti? | Haan (khatarnak) | Nahi (`TypeError`) |
| Tooling / IDE support | Kamzor | Behtar (`__abstractmethods__`) |
| Extra machinery | Zero | `ABCMeta` metaclass |
| Multiple inheritance me metaclass clash | Nahi | Ho sakta hai |

**Trade-off:** `abc` safe hai, magar metaclass laata hai (kabhi kabhi third-party base classes ke sath
conflict). Chhoti duck-typed internal classes me `NotImplementedError` ya `...` bhi chalta hai.

**Gotcha:** `NotImplementedError` (exception) aur `NotImplemented` (singleton jo `__eq__`/`__add__`
return karte hain) do **alag** cheezein hain. `raise NotImplemented` galat hai.
"""),
    code("""
# ---- Purana style: base class ban jati hai, error sirf call par ----
class OldShape:
    def area(self):
        raise NotImplementedError(f"{type(self).__name__} ko area() implement karna chahiye")

class OldSquare(OldShape):
    def __init__(self, s): self.s = s
    # area() likhna BHOOL gaye

o = OldShape()            # koi rok nahi! object ban gaya (khatarnak)
print("OldShape instance ban gaya:", o)
try:
    OldSquare(4).area()   # masla ab pakra gaya -> production me late failure
except NotImplementedError as e:
    print("NotImplementedError:", e)

# ---- abc style: masla foran, object hi nahi banta ----
class NewShape(ABC):
    @abstractmethod
    def area(self): ...

class NewSquare(NewShape):
    def __init__(self, s): self.s = s

try:
    NewSquare(4)
except TypeError as e:
    print("TypeError (jaldi pakra gaya):", e)

# ---- NotImplemented vs NotImplementedError ka farq ----
class Money:
    def __init__(self, v): self.v = v
    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented        # "main nahi jaanta" -> Python doosri taraf poochhega
        return self.v == other.v

print("Money(5) == Money(5):", Money(5) == Money(5))
print("Money(5) == 'abc'  :", Money(5) == "abc", "(NotImplemented -> Python ne False decide kiya)")
print("types:", type(NotImplemented).__name__, "vs", NotImplementedError.__mro__[1].__name__)
"""),
    md("""
## 9. Duck typing vs nominal typing

- **Duck typing (Python ka default):** *"If it walks like a duck and quacks like a duck, it's a duck."*
  Type ka **naam** nahi dekha jata, sirf ye ke zaroori method mojood hai ya nahi.
- **Nominal typing (`ABC`/`isinstance`):** rishta **declare** karna parta hai
  (subclass ho ya `register` ho), tab hi type match maana jayega.
- **Structural typing (`Protocol`):** shape/structure dekhi jati hai — duck typing + static checking.

**EAFP vs LBYL:** Python me `try/except AttributeError` (EAFP: *Easier to Ask Forgiveness*)
ko `if hasattr(...)` (LBYL: *Look Before You Leap*) par tarjeeh di jati hai.
"""),
    code("""
# ---- Duck typing: koi inheritance nahi, sirf method hona chahiye ----
class Duck:
    def speak(self): return "Quack"

class Robot:
    def speak(self): return "Beep boop"

class Stone:
    pass                                   # speak nahi hai

def make_it_speak(thing):
    # LBYL style
    if hasattr(thing, "speak"):
        return thing.speak()
    return f"{type(thing).__name__} bol nahi sakta"

def make_it_speak_eafp(thing):
    # EAFP style (Pythonic)
    try:
        return thing.speak()
    except AttributeError:
        return f"{type(thing).__name__} bol nahi sakta"

for t in [Duck(), Robot(), Stone()]:
    print(f"{type(t).__name__:<7} LBYL={make_it_speak(t):<20} EAFP={make_it_speak_eafp(t)}")

# ---- Nominal typing: naam/rishta zaroori ----
class Speaker(ABC):
    @abstractmethod
    def speak(self): ...

print("\\nisinstance(Duck(), Speaker):", isinstance(Duck(), Speaker), "<- duck typing kaam karti hai lekin nominal check fail")
print("Robot ka speak mojood hai:", callable(getattr(Robot(), 'speak', None)))
"""),
    md("""
## 10. `typing.Protocol` — structural typing

**Kya hai:** `Protocol` (PEP 544) se tum contract likhte ho **bina** implementer ko inherit karwane ke.
Jo class wo methods rakhti hai, wo automatically protocol ko satisfy karti hai — *static* checkers
(mypy/pyright) ke liye bhi, aur `@runtime_checkable` ke sath `isinstance()` ke liye bhi.

**Kyun:** Third-party classes ko tum inherit nahi karwa sakte (unka code tumhare paas nahi).
Protocol se unko bhi contract me shamil kar sakte ho — *"duck typing with type safety"*.

**Syntax:**

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...
```

**Gotchas:**
- `isinstance()` sirf **method ke naam** dekhta hai — signature ya return type verify nahi hota
- `runtime_checkable` ke bagair `isinstance()` par `TypeError`
- Non-method (data) members wale protocol ke sath `isinstance` chalta hai (3.12+) magar `issubclass` nahi
- Protocol khud instantiate nahi hoti
"""),
    code("""
from typing import Protocol, runtime_checkable

@runtime_checkable
class SupportsExport(Protocol):
    def export(self, rows: list) -> str: ...      # sirf shape, koi body nahi


# NOTE: ye classes SupportsExport se inherit NAHI karti -> phir bhi satisfy karti hain
class CsvExporter:
    def export(self, rows):
        head = ",".join(rows[0].keys())
        body = "\\n".join(",".join(str(v) for v in r.values()) for r in rows)
        return head + "\\n" + body

class MarkdownExporter:
    def export(self, rows):
        head = "| " + " | ".join(rows[0]) + " |"
        sep = "| " + " | ".join("---" for _ in rows[0]) + " |"
        body = "\\n".join("| " + " | ".join(str(v) for v in r.values()) + " |" for r in rows)
        return "\\n".join([head, sep, body])

class Printer:
    def show(self, rows): return "..."            # galat method naam -> satisfy nahi karta


rows = [{"name": "Ali", "city": "Lahore"}, {"name": "Sara", "city": "Karachi"}]
for obj in [CsvExporter(), MarkdownExporter(), Printer()]:
    ok = isinstance(obj, SupportsExport)          # structural check (runtime_checkable ki wajah se)
    print(f"{type(obj).__name__:<18} isinstance -> {ok}")

print()
print(CsvExporter().export(rows))
print()
print(MarkdownExporter().export(rows))

# Gotcha 1: runtime_checkable ke bagair isinstance nahi chalega
class NotCheckable(Protocol):
    def export(self, rows): ...
try:
    isinstance(CsvExporter(), NotCheckable)
except TypeError as e:
    print("\\nTypeError:", e)

# Gotcha 2: isinstance sirf naam dekhta hai, signature nahi
class WrongSignature:
    def export(self):                              # rows parameter hi nahi!
        return "oops"
print("WrongSignature isinstance:", isinstance(WrongSignature(), SupportsExport), "<- naam match, signature ghalat")

# Gotcha 3: Protocol ko instantiate nahi kar sakte
try:
    SupportsExport()
except TypeError as e:
    print("TypeError:", e)
"""),
    md("""
### 10.1 Protocol ko explicitly inherit bhi kar sakte ho

Protocol se inherit karna **optional** hai, magar faida hai: typo par foran pata chal jata hai
(explicit subclass me missing method = abstract, instantiate karte waqt `TypeError`).

Isse Protocol "ABC jaisa" behave karne lagta hai — best of both worlds:
*bahar walon ke liye structural, apni team ke liye explicit.*
"""),
    code("""
class JsonExporter(SupportsExport, Protocol):     # ye khud bhi protocol reh gaya (Protocol base rakha)
    ...

class RealJsonExporter(SupportsExport):           # explicit inheritance -> concrete class
    def export(self, rows):
        import json
        return json.dumps(rows, ensure_ascii=False)

print(RealJsonExporter().export(rows))
print("isinstance:", isinstance(RealJsonExporter(), SupportsExport))

# Explicit inheritance ka faida: method bhool jao to instantiate hi nahi hoga
class BrokenExporter(SupportsExport):
    pass
try:
    BrokenExporter()
except TypeError as e:
    print("TypeError:", e)
"""),
    md("""
## 11. ABC vs Protocol — kab kaunsa?

| Feature | `ABC` (nominal) | `Protocol` (structural) |
|---|---|---|
| Rishta kaise bane | Inherit ya `register()` | Bas methods match hon |
| Shared code de sakta? | **Haan** (concrete methods) | Nahi (sirf contract; default body discourage) |
| `isinstance()` | Hamesha | Sirf `@runtime_checkable` ke sath |
| Third-party class ko fit karna | `register()` chahiye | Automatic |
| Missing method kab pakra jaye | Instantiation par | Static checker par (ya explicit inherit ho to instantiation par) |
| State / `__init__` share | Haan | Nahi (mat karo) |
| Metaclass | `ABCMeta` | Normal (`_ProtocolMeta`) |
| Best for | Tumhari **apni** class family + shared logic | **Bahari**/loose coupling, library APIs |

**Rule of thumb:**
- Tum base class **aur** subclasses dono ke malik ho + code share karna hai → **ABC**
- Sirf "is shape ka koi bhi object" chahiye (kisi ka bhi ho) → **Protocol**
- Dono ek sath bhi chal sakte hain: internally ABC, public API me Protocol.
"""),
    code("""
# Ek hi kaam do styles me -> farq khud dekho

# STYLE 1: ABC (nominal + shared logic)
class RepoABC(ABC):
    @abstractmethod
    def get(self, key): ...

    def get_or_default(self, key, default=None):    # shared helper -> ABC ka bara faida
        try:
            return self.get(key)
        except KeyError:
            return default

class DictRepo(RepoABC):
    def __init__(self, data): self.data = data
    def get(self, key): return self.data[key]

r = DictRepo({"a": 1})
print("ABC style:", r.get("a"), r.get_or_default("zz", "N/A"))

# STYLE 2: Protocol (structural, koi inheritance nahi)
@runtime_checkable
class RepoProto(Protocol):
    def get(self, key): ...

class ThirdPartyCache:                              # farz karo ye library ki class hai (hum badal nahi sakte)
    def __init__(self): self._c = {"x": 42}
    def get(self, key): return self._c[key]

def read_setting(repo: RepoProto, key):
    return repo.get(key)

print("Protocol style:", read_setting(ThirdPartyCache(), "x"))
print("library class protocol satisfy karti hai:", isinstance(ThirdPartyCache(), RepoProto))
print("library class ABC satisfy karti hai:", isinstance(ThirdPartyCache(), RepoABC), "<- nahi (nominal)")
"""),
    md("""
## 12. `ABCMeta.register()` — virtual subclass

`register()` se tum keh sakte ho: *"ye class bhi meri family ka hissa samjho"* —
**bina inherit karwaye**. Ye khaas tor par third-party classes ke liye hai.

```python
RepoABC.register(ThirdPartyCache)      # ab isinstance True dega
```

**Ahem gotchas:**
- Virtual subclass ko koi **method inherit nahi** hota (mixin nahi milta!)
- Abstract methods ka koi **enforcement nahi** — tum jhoot bol sakte ho
- `cls.__mro__` me wo class nahi aati
- Decorator ki tarah bhi use hota hai: `@RepoABC.register`
"""),
    code("""
class Jsonable(ABC):
    @abstractmethod
    def to_json(self): ...

    def pretty(self):                       # note: virtual subclass ko ye HELPER nahi milega
        return f"<{self.to_json()}>"

class LegacyRow:                            # purani class, hum ise chhedna nahi chahte
    def to_json(self): return '{"legacy": true}'

Jsonable.register(LegacyRow)                # virtual subclass bana diya

lr = LegacyRow()
print("isinstance:", isinstance(lr, Jsonable), "| issubclass:", issubclass(LegacyRow, Jsonable))
print("MRO me Jsonable hai?", Jsonable in LegacyRow.__mro__, "<- nahi! sirf claim hai")
try:
    lr.pretty()                             # helper inherit NAHI hua
except AttributeError as e:
    print("AttributeError:", e)

# Decorator style + enforcement ka na hona (khatarnak pehlu)
@Jsonable.register
class Liar:
    pass                                    # to_json bilkul nahi, phir bhi register ho gaya

print("Liar isinstance:", isinstance(Liar(), Jsonable), "<- abc ne rok nahi lagayi")
try:
    Liar().to_json()
except AttributeError as e:
    print("AttributeError:", e, "-> register() sirf 'promise' hai, guarantee nahi")
"""),
    md("""
## 13. `__subclasshook__` — automatic virtual subclass

Har class ko haath se `register` karna thakane wala hai. `__subclasshook__` se tum
`issubclass()` ka faisla **khud** likh sakte ho (structural check).

```python
@classmethod
def __subclasshook__(cls, C):
    if cls is MyABC:
        return any("method" in B.__dict__ for B in C.__mro__)   # True/False/NotImplemented
    return NotImplemented
```

- `True` → subclass hai, `False` → nahi, `NotImplemented` → normal rules chalao
- `if cls is MyABC` check zaroori hai warna subclasses par bhi hook lag jayega
- Yehi mechanism `collections.abc.Iterable` istemal karti hai (`__iter__` dekhti hai)
"""),
    code("""
class Renderable(ABC):
    @abstractmethod
    def render(self): ...

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Renderable:                                  # sirf khud ke liye, subclasses ke liye nahi
            if any("render" in B.__dict__ for B in C.__mro__):  # structural check
                return True
            return NotImplemented                              # faisla normal rules par chhor do
        return NotImplemented


class Button:                       # koi inheritance / register nahi
    def render(self): return "<button/>"

class Label:
    def render(self): return "<span/>"

class Timer:
    def tick(self): return 1

print("Button  :", issubclass(Button, Renderable), isinstance(Button(), Renderable))
print("Label   :", issubclass(Label, Renderable))
print("Timer   :", issubclass(Timer, Renderable), "<- render nahi hai")

# Ye exactly wahi trick hai jo stdlib use karti hai:
from collections.abc import Iterable, Sized, Container
class MyBag:
    def __init__(self, items): self.items = list(items)
    def __iter__(self): return iter(self.items)
    def __len__(self): return len(self.items)
    def __contains__(self, x): return x in self.items

b = MyBag([1, 2, 3])
print("\\nstdlib hooks -> Iterable:", isinstance(b, Iterable), "| Sized:", isinstance(b, Sized), "| Container:", isinstance(b, Container))
print("MyBag ne kisi cheez se inherit nahi kiya:", MyBag.__mro__)
"""),
]

CELLS += [
    md("""
## 14. `collections.abc` — stdlib ke ready-made contracts

`collections.abc` me 25+ ABCs hain. Do faide hain:

1. **`isinstance` checks:** `isinstance(x, Iterable)`, `isinstance(x, Mapping)` — duck typing ka safe tareeqa
2. **Mixin methods muft:** agar tum inherit karo to bohat kuch **khud ban jata hai**

| ABC | Lazmi methods | Muft mile mixin methods |
|---|---|---|
| `Iterable` | `__iter__` | — |
| `Sized` | `__len__` | — |
| `Container` | `__contains__` | — |
| `Collection` | `__iter__`, `__len__`, `__contains__` | — |
| `Sequence` | `__getitem__`, `__len__` | `__contains__`, `__iter__`, `__reversed__`, `index`, `count` |
| `MutableSequence` | + `__setitem__`, `__delitem__`, `insert` | `append`, `extend`, `pop`, `remove`, `+=` |
| `Mapping` | `__getitem__`, `__iter__`, `__len__` | `get`, `keys`, `values`, `items`, `__eq__`, `__contains__` |
| `MutableMapping` | + `__setitem__`, `__delitem__` | `pop`, `popitem`, `clear`, `update`, `setdefault` |
| `Hashable` | `__hash__` | — |
| `Iterator` | `__next__` (+ `__iter__`) | `__iter__` |

**Interview tip:** `list` ke bajaye `Sequence`, `dict` ke bajaye `Mapping` type-hint karo —
ye "program to an interface" ka amali roop hai. Aur `isinstance(x, Iterable)` `str` ke liye bhi
`True` deta hai — ye classic bug hai.
"""),
    code("""
from collections.abc import Sequence, Iterable

class Playlist(Sequence):
    # Sirf 2 methods do -> Sequence poora protocol muft me de degi
    def __init__(self, songs):
        self._songs = list(songs)

    def __getitem__(self, i):
        return self._songs[i]

    def __len__(self):
        return len(self._songs)


p = Playlist(["Afreen", "Sayonee", "Neend"])
print("len       :", len(p))
print("index[1]  :", p[1])
print("in check  :", "Sayonee" in p)          # __contains__ muft mila
print("loop      :", [s[:3] for s in p])      # __iter__ muft mila
print("reversed  :", list(reversed(p)))       # __reversed__ muft
print("index()   :", p.index("Neend"), "| count():", p.count("Afreen"))
print("slice     :", p[0:2], "(list milti hai kyunki __getitem__ list ka slice deta hai)")

# Classic bug: str bhi Iterable hai
def flatten_names(x):
    if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):   # str ko alag handle karo
        return [i for i in x]
    return [x]
print("\\nflatten('Ali'):", flatten_names("Ali"), "<- str ko exclude na karte to ['A','l','i'] milta")
"""),
    code("""
from collections.abc import MutableMapping

class CaseInsensitiveDict(MutableMapping):
    # Asli duniya ka example: HTTP headers case-insensitive hote hain (requests library isi tarah karti hai)
    def __init__(self, data=None):
        self._d = {}
        if data:
            self.update(data)            # update() mixin se muft mila

    def _norm(self, k):
        return k.lower() if isinstance(k, str) else k

    # ---- 5 lazmi methods ----
    def __getitem__(self, k):
        return self._d[self._norm(k)][1]

    def __setitem__(self, k, v):
        self._d[self._norm(k)] = (k, v)   # asli casing bhi yaad rakhi (display ke liye)

    def __delitem__(self, k):
        del self._d[self._norm(k)]

    def __iter__(self):
        return (orig for orig, _ in self._d.values())

    def __len__(self):
        return len(self._d)

    def __repr__(self):
        return f"CaseInsensitiveDict({dict(self.items())})"


h = CaseInsensitiveDict({"Content-Type": "application/json"})
h["ACCEPT"] = "*/*"
print(h)
print("case-insensitive read:", h["content-type"], "|", h["Accept"])
print("get() muft         :", h.get("missing", "default"))
print("keys()/items() muft:", list(h.keys()), list(h.items())[:1])
print("pop() muft         :", h.pop("accept"), "-> ab len =", len(h))
print("isinstance Mapping :", isinstance(h, MutableMapping))
"""),
    md("""
## 15. Template Method pattern

**Kya hai:** Base class **algorithm ka skeleton** (steps ka order) fix kar deti hai,
aur kuch steps ko abstract chhor deti hai jinhein subclass bharti hai.

**Kyun:** "Same process, mukhtalif tafseel" — ETL pipelines, report generators, game loops,
test setup/teardown, request handling. Order galat hone ka khatra khatam.

**Hooks:** optional steps jinki base me khaali (default) body hoti hai — subclass chahe to override kare.

**Gotcha:** template method ko subclass **override na kare** — warna maqsad hi khatam.
Naming convention: public template method + `_protected` steps.
"""),
    code("""
class DataPipeline(ABC):
    # ---- TEMPLATE METHOD: ye order fix hai, subclass isko override na kare ----
    def run(self, source):
        raw = self._extract(source)          # abstract
        clean = self._transform(raw)         # abstract
        self._before_load(clean)             # HOOK (optional)
        n = self._load(clean)                # abstract
        return self._report(source, n)       # concrete

    @abstractmethod
    def _extract(self, source): ...

    @abstractmethod
    def _transform(self, raw): ...

    @abstractmethod
    def _load(self, rows): ...

    # ---- HOOK: default me kuch nahi karta ----
    def _before_load(self, rows):
        pass

    # ---- CONCRETE: sab ke liye same ----
    def _report(self, source, n):
        return f"[{type(self).__name__}] {source} se {n} rows load hue"


class SalesCsvPipeline(DataPipeline):
    def _extract(self, source):
        return "id,amount\\n1,500\\n2,700\\n3,-50"        # inline data (koi file nahi)

    def _transform(self, raw):
        lines = raw.strip().split("\\n")[1:]
        rows = [{"id": int(a), "amount": int(b)} for a, b in (l.split(",") for l in lines)]
        return [r for r in rows if r["amount"] > 0]      # negative amount hata do

    def _load(self, rows):
        self.table = rows
        return len(rows)

    def _before_load(self, rows):                        # hook use kiya
        print("  audit: load se pehle", len(rows), "rows validate ho gaye")


class ApiPipeline(DataPipeline):
    def _extract(self, source):
        return [{"user": "ali", "score": 10}, {"user": "sara", "score": 20}]   # fake API response
    def _transform(self, raw):
        return [{**r, "grade": "A" if r["score"] >= 20 else "B"} for r in raw]
    def _load(self, rows):
        self.docs = rows
        return len(rows)


print(SalesCsvPipeline().run("sales.csv"))
print(ApiPipeline().run("https://api.example/scores"))
"""),
    md("""
## 16. Dependency Inversion ka taaruf (DIP)

**Definition:** *High-level modules ko low-level modules par depend nahi karna chahiye —
dono **abstraction** par depend karein.*

Bura design (concrete par depend):

```python
class OrderService:
    def __init__(self):
        self.gw = StripeGateway()      # hard-coded! test karna mushkil, badalna mushkil
```

Acha design (abstraction par depend + injection):

```python
class OrderService:
    def __init__(self, gateway: PaymentGateway):   # bahar se aayega
        self.gw = gateway
```

**Faide:** testing me fake gateway, runtime par gateway switch, business logic gateway se azaad.
Poori tafseel NB4 (SOLID) me — yahan sirf abstraction se rishta samajh lo.
"""),
    code("""
# ---- BEFORE: tightly coupled (DIP violation) ----
class OrderServiceBad:
    def __init__(self):
        self.gateway = StripeGateway()          # concrete class andar hi ban gayi
    def place(self, amount):
        return self.gateway.charge(amount)

# ---- AFTER: dependency injected (DIP follow) ----
class OrderService:
    def __init__(self, gateway: PaymentGateway, notifier=None):
        self.gateway = gateway                  # abstraction par depend
        self.notifier = notifier
    def place(self, amount, customer="guest"):
        res = self.gateway.charge(amount)
        if self.notifier:
            self.notifier(f"{customer} ko receipt {res['txn']} bhej diya")
        return res

# Test ke liye fake gateway (koi network nahi) -> yehi DIP ka sabse bara faida
class FakeGateway(PaymentGateway):
    def __init__(self): self.calls = []
    def charge(self, amount, currency="PKR"):
        self.calls.append(amount)
        return {"txn": "fake_1", "amount": amount, "currency": currency, "status": "ok"}
    def refund(self, txn_id): return {"txn": txn_id, "status": "refunded"}

logs = []
fake = FakeGateway()
svc = OrderService(fake, notifier=logs.append)
print(svc.place(999, "Ali"))
print("fake ko mile amounts:", fake.calls, "| notifications:", logs)

# Production me sirf argument badla, OrderService ka code nahi
print(OrderService(JazzCashGateway()).place(999))
"""),
    md("""
## 17. Common Mistakes / Gotchas (yahan log phaste hain)

1. **`@property` aur `@abstractmethod` ka ulta order** → enforcement khatam (Section 5 dekho).
2. **`ABC` inherit karna bhool jana:** `class Foo:` ke andar `@abstractmethod` likhna **bekar** hai —
   `ABCMeta` na ho to koi rok nahi, class instantiate ho jayegi.
3. **Abstract method me `pass` vs `...`** — dono chalte hain (koi functional farq nahi), `...` convention hai.
4. **Abstract method ko `super()` se call karna** — chalta hai (body agar likhi ho) magar
   khaali body `None` degi; documentation ke liye body likhna theek hai.
5. **`__init__` ko abstract banana** — kaam karta hai magar zyada tar bewaqoofi; behtar hai concrete `__init__`.
6. **`register()` ko enforcement samajhna** — wo sirf claim hai, method check nahi hota.
7. **`Protocol` ke bagair `runtime_checkable`** `isinstance` par `TypeError`.
8. **`Protocol` me state rakhna / shared implementation dena** — ye ABC ka kaam hai.
9. **`isinstance(x, Iterable)` par `str`** bhi `True` — string ko explicitly exclude karo.
10. **Metaclass conflict** — `ABCMeta` + kisi doosre metaclass wali base class.
11. **Sab kuch abstract bana dena** (over-engineering) — Python me 1 implementation ho to ABC ki zaroorat nahi;
    "abstraction premature ho to sirf boilerplate hai".
12. **Abstract class me `__slots__ = ()` bhool jana** jab memory matter kare (NB3 me tafseel).
"""),
    code("""
# Gotcha 2 ka live demo: ABC ke bina abstractmethod bilkul bekar
class NotReallyAbstract:                 # <-- ABC inherit NAHI kiya
    @abstractmethod
    def must_do(self): ...

obj = NotReallyAbstract()                # koi error nahi! (metaclass ABCMeta nahi hai)
print("bin-ABC class instantiate ho gayi:", obj)
print("__abstractmethods__ mojood hai?", hasattr(NotReallyAbstract, "__abstractmethods__"))
print("flag lagi hui hai magar bekar:", NotReallyAbstract.must_do.__isabstractmethod__)
print("call karne par khaali (None):", obj.must_do())

# Gotcha 4: abstract method me body likh kar super() se call karna
class Base(ABC):
    @abstractmethod
    def validate(self, d):
        # base me common validation likh di -> subclass super() se re-use kar sakti hai
        if not isinstance(d, dict):
            raise TypeError("dict chahiye")
        return True

class Child(Base):
    def validate(self, d):
        super().validate(d)              # abstract method ka code bhi chal sakta hai
        return "id" in d

print("\\nChild validate:", Child().validate({"id": 1}))
try:
    Child().validate([1, 2])
except TypeError as e:
    print("TypeError:", e)

# Gotcha 5: abstract __init__ ka asar
class NeedsInit(ABC):
    @abstractmethod
    def __init__(self, x): self.x = x
class Impl(NeedsInit):
    def __init__(self, x): super().__init__(x)
print("abstract __init__ ke sath:", Impl(5).x)
"""),
]

CELLS += [
    md("""
## 18. Real-World Problems

Ab theory ko asli project jaisi shakal dete hain. Char problems:

1. **Notifier system** — Email / SMS / Push, sab ke liye ek contract + shared retry logic
2. **DataExporter** — CSV / JSON export, Template Method ke sath
3. **Plugin architecture** — auto-discovery + registry (`__init_subclass__`)
4. **Report generator** — ABC + Protocol dono ka mila jula istemal
"""),
    md("""
### Problem 1: Notifier system (Email / SMS / Push)

**Requirement:** App ko notification bhejni hai. Channel badalte rehte hain.
Har channel ka "bhejna" alag hai magar **retry, logging aur rate-limit check** sab ke liye same hai.

**Design:**
- `Notifier(ABC)`: abstract `_send(to, text)` + abstract property `channel_name`
- Concrete `send()` template: validate → retry loop → log
- Har channel apni tafseel deta hai (SMS me 160 char limit, Push me payload size)
"""),
    code("""
class Notifier(ABC):
    max_retries = 2

    def __init__(self):
        self.log = []

    # ---- contract ----
    @property
    @abstractmethod
    def channel_name(self): ...

    @abstractmethod
    def _send(self, to, text):
        # Return: True (kamyab) / False (nakaam). Exception bhi phenk sakta hai.
        ...

    # ---- optional hook ----
    def _validate(self, to, text):
        if not to or not text:
            raise ValueError("recipient aur text dono zaroori hain")
        return text

    # ---- template: retry + logging sab ke liye same ----
    def notify(self, to, text):
        text = self._validate(to, text)
        for attempt in range(1, self.max_retries + 2):     # 1 asli koshish + retries
            try:
                if self._send(to, text):
                    self.log.append(f"{self.channel_name}->{to} attempt#{attempt} OK")
                    return True
            except Exception as e:                          # network flake wagaira
                self.log.append(f"{self.channel_name} attempt#{attempt} error: {e}")
                continue
            self.log.append(f"{self.channel_name} attempt#{attempt} FAIL")
        return False


class EmailNotifier(Notifier):
    channel_name = "email"
    def _validate(self, to, text):
        if "@" not in to:
            raise ValueError(f"ghalat email: {to}")
        return super()._validate(to, text)
    def _send(self, to, text):
        return True                                        # farz karo SMTP kaamyab

class SmsNotifier(Notifier):
    channel_name = "sms"
    def _validate(self, to, text):
        text = super()._validate(to, text)
        return text[:160]                                  # SMS ki limit -> kaat do
    def _send(self, to, text):
        return to.startswith("+92")                        # sirf PK numbers support

class PushNotifier(Notifier):
    channel_name = "push"
    def __init__(self, flaky_times=1):
        super().__init__()
        self._flaky = flaky_times                          # pehli baar fail hone ka simulation
    def _send(self, to, text):
        if self._flaky > 0:
            self._flaky -= 1
            raise ConnectionError("FCM timeout")
        return True


def broadcast(notifiers, to_map, text):
    out = {}
    for n in notifiers:
        out[n.channel_name] = n.notify(to_map[n.channel_name], text)
    return out

email, sms, push = EmailNotifier(), SmsNotifier(), PushNotifier()
targets = {"email": "ali@example.com", "sms": "+923001234567", "push": "device-token-1"}
print(broadcast([email, sms, push], targets, "Aap ka order dispatch ho gaya!"))
print("push ka log:", push.log)

# Fail case: ghalat SMS number -> retries ke baad False
bad_sms = SmsNotifier()
print("\\nUK number:", bad_sms.notify("+441234567", "hi"))
print(bad_sms.log)

# Validation error propagate hota hai (fail-fast)
try:
    EmailNotifier().notify("ali-at-example", "hi")
except ValueError as e:
    print("ValueError:", e)
"""),
    md("""
### Problem 2: DataExporter (CSV / JSON / Markdown)

**Requirement:** Ek hi records list ko mukhtalif formats me export karna, aur `filename`
auto-generate karna. Yahan ABC ka `Template Method` + abstract `staticmethod` dono use honge.
"""),
    code("""
import json, io, csv, tempfile, os

class DataExporter(ABC):
    @staticmethod
    @abstractmethod
    def extension(): ...

    @abstractmethod
    def dumps(self, rows): ...

    # template: naam banao + content banao + likho
    def export(self, rows, basename="report"):
        if not rows:
            raise ValueError("khaali data export nahi ho sakta")
        content = self.dumps(rows)
        path = os.path.join(tempfile.gettempdir(), f"{basename}.{self.extension()}")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        return path, len(content)


class CsvDataExporter(DataExporter):
    @staticmethod
    def extension(): return "csv"
    def dumps(self, rows):
        buf = io.StringIO()
        w = csv.DictWriter(buf, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
        return buf.getvalue()

class JsonDataExporter(DataExporter):
    @staticmethod
    def extension(): return "json"
    def dumps(self, rows):
        return json.dumps(rows, indent=2, ensure_ascii=False)

class MarkdownDataExporter(DataExporter):
    @staticmethod
    def extension(): return "md"
    def dumps(self, rows):
        cols = list(rows[0])
        lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
        lines += ["| " + " | ".join(str(r[c]) for c in cols) + " |" for r in rows]
        return "\\n".join(lines)


data = [{"order": 1, "city": "Lahore", "total": 4500},
        {"order": 2, "city": "Karachi", "total": 1200}]

for exp in [CsvDataExporter(), JsonDataExporter(), MarkdownDataExporter()]:
    path, size = exp.export(data, "orders")
    print(f"{type(exp).__name__:<22} -> {os.path.basename(path):<12} ({size} chars)")

print("\\n--- markdown preview ---")
print(MarkdownDataExporter().dumps(data))

try:
    JsonDataExporter().export([])
except ValueError as e:
    print("\\nValueError:", e)
"""),
    md("""
### Problem 3: Plugin architecture (`__init_subclass__` + ABC)

**Requirement:** Team naye "validators" add karti rehti hai. Main code ko har naye validator ka
naam **na** pata ho — subclass banate hi khud register ho jaye.

**Tool:** `__init_subclass__` (PEP 487) — metaclass ke bagair subclass hook.
Ye `ABCMeta` ke sath bhi kaam karta hai aur zyada readable hai.
"""),
    code("""
class Validator(ABC):
    registry = {}                                  # name -> class

    def __init_subclass__(cls, name=None, **kw):    # class keyword args bhi le sakta hai
        super().__init_subclass__(**kw)
        key = name or cls.__name__.replace("Validator", "").lower()
        if not getattr(cls, "__abstractmethods__", None):     # sirf concrete register karo
            Validator.registry[key] = cls

    @abstractmethod
    def check(self, value):
        # return: (ok: bool, message: str)
        ...


class EmailValidator(Validator):
    def check(self, value):
        ok = isinstance(value, str) and value.count("@") == 1 and "." in value.split("@")[-1]
        return ok, "email theek hai" if ok else "email ka format ghalat hai"

class CnicValidator(Validator, name="cnic"):        # custom registry key
    def check(self, value):
        digits = str(value).replace("-", "")
        ok = digits.isdigit() and len(digits) == 13
        return ok, "CNIC theek hai" if ok else "CNIC 13 digits ka hona chahiye"

class PhoneValidator(Validator):
    def check(self, value):
        s = str(value)
        ok = s.startswith("+92") and len(s) == 13
        return ok, "phone theek hai" if ok else "phone +92XXXXXXXXXX hona chahiye"


print("registry (auto-discovered):", sorted(Validator.registry))

def validate_form(form):
    errors = {}
    for field, value in form.items():
        v_cls = Validator.registry.get(field)
        if v_cls is None:
            continue                                  # is field ka koi validator nahi
        ok, msg = v_cls().check(value)
        if not ok:
            errors[field] = msg
    return errors or "sab fields valid hain"

print(validate_form({"email": "ali@site.com", "cnic": "35202-1234567-1", "phone": "+923001234567"}))
print(validate_form({"email": "ali_site.com", "cnic": "123", "phone": "0300123"}))

# Naya plugin banao -> koi central file edit karne ki zaroorat nahi
class IbanValidator(Validator, name="iban"):
    def check(self, value):
        ok = str(value).startswith("PK") and len(str(value)) == 24
        return ok, "IBAN theek hai" if ok else "IBAN 24 chars (PK...) hona chahiye"

print("naya registry:", sorted(Validator.registry))
print(validate_form({"iban": "PK36SCBL0000001123456702"}))
"""),
    md("""
### Problem 4: Report generator — ABC (apna code) + Protocol (bahari code)

**Requirement:** `ReportBuilder` hamari class family hai (shared header/footer logic → **ABC**).
Data source kahin se bhi aa sakta hai (DB cursor, list, API client → **Protocol**).
"""),
    code("""
@runtime_checkable
class RowSource(Protocol):
    def fetch_rows(self) -> list: ...          # bas itna contract


class ReportBuilder(ABC):
    def __init__(self, source: RowSource, title="Report"):
        if not isinstance(source, RowSource):  # structural check
            raise TypeError("source me fetch_rows() hona chahiye")
        self.source, self.title = source, title

    @abstractmethod
    def body(self, rows): ...

    def header(self):  return f"===== {self.title} ====="
    def footer(self, n): return f"----- total {n} rows -----"

    def build(self):                            # template method
        rows = self.source.fetch_rows()
        return "\\n".join([self.header(), self.body(rows), self.footer(len(rows))])


class SummaryReport(ReportBuilder):
    def body(self, rows):
        total = sum(r["total"] for r in rows)
        cities = {r["city"] for r in rows}
        return f"orders={len(rows)} | revenue={total} | cities={sorted(cities)}"

class DetailReport(ReportBuilder):
    def body(self, rows):
        return "\\n".join(f"  #{r['order']:<3} {r['city']:<10} {r['total']:>6}" for r in rows)


# Do bilkul mukhtalif sources -> koi inheritance nahi, sirf shape match
class ListSource:
    def __init__(self, rows): self.rows = rows
    def fetch_rows(self): return self.rows

class FakeCursor:                               # DB cursor jaisa (library ki class ho sakti hai)
    def fetch_rows(self):
        return [{"order": 9, "city": "Multan", "total": 800}]

print(SummaryReport(ListSource(data), "Sales Summary").build())
print()
print(DetailReport(ListSource(data), "Sales Detail").build())
print()
print(SummaryReport(FakeCursor(), "DB Summary").build())

class NoFetch: pass
try:
    SummaryReport(NoFetch())
except TypeError as e:
    print("\\nTypeError:", e)
"""),
]

CELLS += [
    md("""
## 19. LeetCode Problems

Ye teen "design" problems hain — bilkul isi notebook ka mauzoo: **contract pehle, implementation baad me**.
Hum har problem ko do shakal me dekhenge: pehle **plain LeetCode class** (jo submit hoti hai),
aur jahan faida ho wahan **abstraction ke sath** (ABC/Protocol) version bhi.

- **LC 208** — Implement Trie (Prefix Tree)
- **LC 211** — Design Add and Search Words Data Structure
- **LC 1146** — Snapshot Array
"""),
    md("""
### LC 208. Implement Trie (Prefix Tree) — Medium

Link: https://leetcode.com/problems/implement-trie-prefix-tree/

**Problem (Roman Urdu):** Ek `Trie` class banao jisme teen operations hon:
`insert(word)`, `search(word)` (poora word mojood hai?), aur `startsWith(prefix)`
(koi word is prefix se shuru hota hai?).

**Approach / intuition:**
1. Trie ek tree hai jahan har **node ek character** ko represent karta hai (edge par letter).
2. Har node ke paas `children` dict hota hai (`char -> node`) aur ek flag `is_end`.
3. `insert`: root se chalo, har char ke liye child na ho to bana do, aakhir me `is_end = True`.
4. `search`: chalte jao; raasta toot gaya → `False`; aakhir me `is_end` return karo.
5. `startsWith`: bilkul `search` jaisa, magar aakhir me `is_end` ki parwah nahi — node mil gaya to `True`.
6. `_walk(prefix)` helper likh lo (DRY) — dono search wale kaam usi par ban jate hain.

**Complexity:** har operation `O(L)` (L = word ki lambai).
Space: `O(total_chars)` worst case (`O(N*L)`), har node par 26-tak children.

**Interview tip:** `dict` children (memory efficient, any charset) vs `[None]*26` array
(thora fast, sirf a-z) — trade-off zaroor mention karo.
"""),
    code("""
class TrieNode:
    __slots__ = ("children", "is_end")           # memory bachane ke liye (NB3 me tafseel)
    def __init__(self):
        self.children = {}                       # char -> TrieNode
        self.is_end = False                      # yahan koi word khatam hota hai?


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            # setdefault: child mojood ho to wahi, warna naya bana do
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True                       # word ka end mark

    def _walk(self, prefix: str):
        # prefix ke aakhri node tak pahuncho, na mile to None (DRY helper)
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and node.is_end  # poora word hona zaroori hai

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None    # sirf raasta hona kaafi hai


# ---- asserts (LeetCode ka official example) ----
t = Trie()
t.insert("apple")
assert t.search("apple") is True
assert t.search("app") is False                  # "app" sirf prefix hai, word nahi
assert t.startsWith("app") is True
t.insert("app")
assert t.search("app") is True

# extra edge cases
t2 = Trie()
t2.insert("")                                    # khaali string bhi valid word ban sakti hai
assert t2.search("") is True
assert t2.startsWith("") is True
assert t2.search("a") is False
t2.insert("abc")
assert [t2.search(w) for w in ("a", "ab", "abc")] == [False, False, True]
assert all(t2.startsWith(p) for p in ("a", "ab", "abc"))
assert t2.startsWith("abcd") is False
print("LC 208 ke saare asserts pass [pass]")
"""),
    md("""
#### LC 208 ka abstraction wala roop (interview me impress karne ke liye)

Interviewer poochh sakta hai: *"agar kal ko Trie ki jagah HashSet-based implementation chahiye ho?"*
Jawab: **ek `PrefixIndex` ABC** banao, dono implementations us contract ko follow karein —
caller code na badle. Yahan hum `set` wala brute-force bhi likh kar complexity compare karenge.

| Implementation | insert | search | startsWith | Space |
|---|---|---|---|---|
| Trie | O(L) | O(L) | O(L) | O(N*L) nodes |
| Set (brute) | O(L) | O(L) avg | **O(N*L)** (sab words scan) | O(N*L) |
"""),
    code("""
class PrefixIndex(ABC):
    @abstractmethod
    def insert(self, word): ...
    @abstractmethod
    def search(self, word): ...
    @abstractmethod
    def startsWith(self, prefix): ...

    def insert_many(self, words):        # shared helper -> ABC ka faida
        for w in words:
            self.insert(w)
        return self


# NOTE (base order matters!): Trie PEHLE likhna zaroori hai.
# Agar (PrefixIndex, Trie) likhte to MRO me PrefixIndex ke abstract methods pehle milte
# aur class abstract hi reh jati -> TypeError. Poori tafseel NB2 (MRO) me.
class TrieIndex(Trie, PrefixIndex):      # Trie ko contract se jodh diya (koi code dobara nahi likha)
    pass

class SetIndex(PrefixIndex):
    # Brute force: sab words ek set me. startsWith har baar scan karta hai -> O(N*L)
    def __init__(self):
        self.words = set()
    def insert(self, word):
        self.words.add(word)
    def search(self, word):
        return word in self.words
    def startsWith(self, prefix):
        return any(w.startswith(prefix) for w in self.words)


words = ["car", "card", "care", "dog", "do"]
for idx in (TrieIndex().insert_many(words), SetIndex().insert_many(words)):
    # dono ka natija bilkul same -> abstraction kaamyab
    res = (idx.search("car"), idx.search("ca"), idx.startsWith("ca"), idx.startsWith("z"))
    print(f"{type(idx).__name__:<10} {res}")
    assert res == (True, False, True, False)
print("dono implementations same jawab dete hain [pass]")
"""),
    md("""
### LC 211. Design Add and Search Words Data Structure — Medium

Link: https://leetcode.com/problems/design-add-and-search-words-data-structure/

**Problem (Roman Urdu):** `WordDictionary` banao: `addWord(word)` aur `search(word)`.
Farq ye hai ke search me `'.'` **wildcard** ho sakta hai jo kisi bhi **ek** letter se match karta hai.

**Approach / intuition:**
1. Base wahi Trie hai (LC 208 wala).
2. `search` me jab normal char aaye → seedha us child par jao.
3. Jab `'.'` aaye → **saare children** par branch karo (DFS / backtracking).
4. Recursion ka base case: word khatam → `node.is_end` return karo.
5. Optimization: har node par min/max word length ya children ka count rakh kar pruning ho sakti hai
   (interview me bonus point).

**Complexity:**
- `addWord`: `O(L)`
- `search`: best `O(L)` (koi dot nahi); worst `O(26^d * L)` jahan `d` = dots ki tadaad —
  practically `O(N)` nodes tak visit ho sakte hain. Space: `O(N*L)` + recursion `O(L)`.
"""),
    code("""
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()                    # wahi TrieNode dobara istemal (re-use)

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word: str) -> bool:
        return self._dfs(self.root, word, 0)

    def _dfs(self, node, word, i):
        if i == len(word):                        # base case: word khatam
            return node.is_end
        ch = word[i]
        if ch == ".":
            # wildcard -> har child par koshish karo (backtracking)
            for child in node.children.values():
                if self._dfs(child, word, i + 1):
                    return True                   # ek raasta mil gaya to bas
            return False
        nxt = node.children.get(ch)
        return nxt is not None and self._dfs(nxt, word, i + 1)


# ---- asserts (LeetCode ka official example) ----
wd = WordDictionary()
for w in ("bad", "dad", "mad"):
    wd.addWord(w)
assert wd.search("pad") is False
assert wd.search("bad") is True
assert wd.search(".ad") is True                   # pehla letter kuch bhi
assert wd.search("b..") is True                   # do wildcards

# edge cases
assert wd.search("...") is True
assert wd.search("....") is False                 # lambai match nahi karti
assert wd.search(".") is False                    # 1-letter word koi nahi
wd.addWord("a")
assert wd.search(".") is True
assert wd.search("a") is True
assert wd.search("..") is False

wd2 = WordDictionary()
wd2.addWord("")
assert wd2.search("") is True
print("LC 211 ke saare asserts pass [pass]")
"""),
    md("""
### LC 1146. Snapshot Array — Medium

Link: https://leetcode.com/problems/snapshot-array/

**Problem (Roman Urdu):** `SnapshotArray(length)` banao (shuru me sab 0).
`set(index, val)` value set kare, `snap()` ek snapshot le kar `snap_id` return kare
(0 se shuru, har baar +1), aur `get(index, snap_id)` us snapshot ke waqt ki value de.

**Naive soch:** har `snap()` par poori array copy → `O(length)` per snap, memory phat jayegi.

**Optimal approach:**
1. Har index ke liye **history list** rakho: `[(snap_id, value), ...]` — sirf **badlaav** save hote hain.
2. `set`: agar aakhri entry ka `snap_id` current wala hi hai to usi ko update karo, warna naya append.
3. `snap()`: bas `snap_id += 1` (kuch copy nahi!) → `O(1)`.
4. `get(index, snap_id)`: us index ki history me **binary search** (`bisect_right` on `snap_id`)
   se aakhri aisi entry dhoondo jiska id `<= snap_id` ho. Kuch na mile to 0.

**Complexity:** `set` `O(1)` amortized, `snap` `O(1)`, `get` `O(log k)` (k = us index ki history).
Space: `O(total set calls)` — na ke `O(snaps * length)`.
"""),
    code("""
from bisect import bisect_right

class SnapshotArray:
    def __init__(self, length: int):
        # har index ke liye history: [(snap_id, value)]. Shuruati (-1, 0) sentinel se get() saaf ho jata hai
        self.history = [[(-1, 0)] for _ in range(length)]
        self.snap_id = 0

    def set(self, index: int, val: int) -> None:
        hist = self.history[index]
        if hist[-1][0] == self.snap_id:
            hist[-1] = (self.snap_id, val)        # isi snapshot me dobara set -> overwrite
        else:
            hist.append((self.snap_id, val))      # naya version

    def snap(self) -> int:
        self.snap_id += 1
        return self.snap_id - 1                   # jo id abhi band hui wo return hoti hai

    def get(self, index: int, snap_id: int) -> int:
        hist = self.history[index]
        # bisect_right se pehla aisa position jahan id > snap_id; us se ek peechhe hamara jawab
        i = bisect_right(hist, (snap_id, float("inf"))) - 1
        return hist[i][1]


# ---- asserts (LeetCode ka official example) ----
sa = SnapshotArray(3)
sa.set(0, 5)
assert sa.snap() == 0
sa.set(0, 6)
assert sa.get(0, 0) == 5                          # snapshot 0 me purani value
assert sa.snap() == 1                             # doosra snapshot
assert sa.get(0, 1) == 6                          # snapshot 1 me nayi value
assert sa.get(0, 0) == 5                          # purana snapshot aaj bhi salamat

# edge cases
sa2 = SnapshotArray(2)
assert sa2.get(1, 0) == 0                         # kabhi set nahi hua -> default 0
assert sa2.snap() == 0
sa2.set(1, 9)
sa2.set(1, 11)                                    # same snapshot me do baar set -> aakhri chalti hai
assert sa2.snap() == 1
assert sa2.get(1, 0) == 0
assert sa2.get(1, 1) == 11
assert sa2.snap() == 2
assert sa2.get(1, 2) == 11                        # koi change nahi hua -> purani value carry
assert [len(h) for h in sa2.history] == [1, 2], "sirf badlaav save hone chahiye"
print("LC 1146 ke saare asserts pass [pass]")


# ---- Brute force (comparison ke liye) ----
class SnapshotArrayBrute:
    def __init__(self, length):
        self.cur = [0] * length
        self.snaps = []
    def set(self, i, v): self.cur[i] = v
    def snap(self):
        self.snaps.append(list(self.cur))         # poori copy -> O(length) time + memory
        return len(self.snaps) - 1
    def get(self, i, sid): return self.snaps[sid][i]

# Randomized cross-check: dono implementations ka natija identical hona chahiye
import random
random.seed(7)
a, b = SnapshotArray(6), SnapshotArrayBrute(6)
taken = []
for _ in range(200):
    if random.random() < 0.7:
        i, v = random.randrange(6), random.randrange(100)
        a.set(i, v); b.set(i, v)
    else:
        sid_a, sid_b = a.snap(), b.snap()
        assert sid_a == sid_b
        taken.append(sid_a)
for sid in taken:
    for i in range(6):
        assert a.get(i, sid) == b.get(i, sid), (i, sid)
print(f"optimal vs brute force cross-check pass ({len(taken)} snapshots) [pass]")
"""),
]

CELLS += [
    md("""
## 20. Interview Questions & Answers

**Q1. Abstraction aur encapsulation me farq?**
Abstraction = *kya expose karna hai* (design level, complexity chhupana, `ABC`/`Protocol`).
Encapsulation = *kaise protect karna hai* (implementation level, data chhupana, `_`/`__`/`@property`).

**Q2. Python me abstract class kaise banate hain?**
`from abc import ABC, abstractmethod`; class `ABC` se inherit kare; jo methods lazmi hain unpar
`@abstractmethod`. Aisi class instantiate karne par `TypeError` aata hai.

**Q3. `ABC` aur `ABCMeta` ka farq?**
`ABCMeta` metaclass hai; `ABC` ek convenience class hai jiska metaclass `ABCMeta` hai.
`class X(ABC)` == `class X(metaclass=ABCMeta)`. `ABCMeta` seedha jab custom metaclass chahiye.

**Q4. Kya abstract class me concrete methods ho sakte hain?**
Bilkul — aur yehi ABC ki taqat hai. Shared logic base me, variable logic abstract.
(Interface-style class me sirf abstract methods rakhte hain.)

**Q5. Abstract method me body likh sakte hain?**
Haan, aur subclass `super()` se call bhi kar sakti hai. Abstractness sirf ye kehti hai
"override lazmi hai", ye nahi ke "body na ho".

**Q6. `NotImplementedError` vs `abc` — kaun behtar?**
`abc` behtar: error **instantiation** par milta hai (fail-fast), tooling support hai, base class
galti se instantiate nahi hoti. `NotImplementedError` ki failure **runtime call** par hoti hai.
Trade-off: `abc` metaclass laata hai (metaclass conflict ka imkaan).

**Q7. `NotImplementedError` aur `NotImplemented` me farq?**
`NotImplementedError` ek exception class hai (`raise` karte hain).
`NotImplemented` ek singleton value hai jo `__eq__`/`__add__` jaise operators return karte hain
taake Python doosre operand ka reflected method try kare. `raise NotImplemented` galat hai.

**Q8. Duck typing kya hai?**
Type ke naam ki jagah **behaviour** dekhna: "jo `quack()` kar sakta hai, wo duck hai".
Python me polymorphism ka default tareeqa; `isinstance` par bharosa kam hota hai.

**Q9. `typing.Protocol` kya hai aur ABC se kab behtar hai?**
Structural typing — inherit ke bina contract. Behtar jab tum implementer classes ke **malik nahi**
(third-party), loose coupling chahiye, ya sirf "shape" matter karti ho. Shared code chahiye to ABC.

**Q10. `@runtime_checkable` kya karta hai aur uski limits?**
Protocol par `isinstance()` allow karta hai. Limits: sirf **method ke naam** check hote hain —
signature/type nahi; data-only protocols ke sath `issubclass()` nahi chalta.

**Q11. Nominal vs structural typing?**
Nominal: rishta declare hona chahiye (inheritance/`register`) — `ABC`.
Structural: shape match kaafi hai — `Protocol`. Python runtime khud duck-typed (structural) hai.

**Q12. `ABCMeta.register()` kya karta hai? Kya wo abstract methods enforce karta hai?**
Virtual subclass banata hai — `isinstance`/`issubclass` `True` dene lagta hai. **Enforcement nahi**,
methods inherit bhi nahi hote, aur `__mro__` me class shamil nahi hoti.

**Q13. `__subclasshook__` ka maqsad?**
`issubclass()` ka faisla khud karna (structural check). `True`/`False`/`NotImplemented` return karta hai.
`collections.abc.Iterable` isi se `__iter__` wali kisi bhi class ko apna maan leti hai.

**Q14. `collections.abc.Sequence` se inherit karne ka faida?**
Sirf `__getitem__` + `__len__` do, aur `__contains__`, `__iter__`, `__reversed__`, `index`, `count`
muft mil jate hain — plus `isinstance(x, Sequence)` sach ho jata hai.

**Q15. `Iterable` check karte waqt kya ehtiyat?**
`str`/`bytes` bhi `Iterable` hain — recursion/flatten wale code me inko explicitly exclude karo.

**Q16. Template Method pattern kya hai?**
Base class algorithm ke steps ka **order** fix karti hai (concrete template method), tafseel
abstract steps me subclass deti hai. Optional "hooks" default khaali hote hain.

**Q17. Dependency Inversion Principle ka abstraction se kya taalluq?**
DIP kehta hai high-level aur low-level dono **abstraction** par depend karein. Abstraction
(ABC/Protocol) wo "plug point" deta hai jahan concrete implementation inject hoti hai — testing asaan.

**Q18. Kya abstract class me `__init__` ho sakta hai? State?**
Haan — abstract class normal class hi hai; `__init__` likho, subclass `super().__init__()` kare.
(Protocol me state mat rakho.)

**Q19. `@property` + `@abstractmethod` ka sahi order?**
`@property` upar, `@abstractmethod` uske neeche (andar). Ulta karne par kuch cases me abstractness
kho jati hai — safe rule: `abstractmethod` sabse **innermost**.

**Q20. Over-abstraction ke nuqsaan?**
Faaltu indirection, parhne me mushkil, ek hi implementation ke liye interface (YAGNI),
deep hierarchies jinme MRO debug karna mushkil. Rule: **doosri** implementation aane par abstract karo.
"""),
    md("""
## 21. Practice Exercises (khud karo)

1. **`Vehicle` ABC** banao: abstract `wheels` (property), abstract `fuel_type()`,
   concrete `describe()` jo dono use kare. `Car`, `Bike`, `Rickshaw` banao.
   *Hint:* `@property` + `@abstractmethod` ka order yaad rakho.

2. **`Cache` interface**: `get(k)`, `set(k, v)`, `delete(k)` abstract; concrete `get_or_set(k, factory)`.
   `DictCache` aur `NullCache` (kuch save na kare) implement karo.
   *Hint:* `get_or_set` template method hai.

3. **`Stack` ko `collections.abc.Sized` + `Container` se** banao aur `isinstance` se tasdeeq karo.
   *Hint:* `__len__` aur `__contains__` kaafi hain.

4. **`Temperature` reader Protocol** (`read_celsius()`) banao `@runtime_checkable` ke sath;
   do fake sensors likho + ek galat class jo satisfy na kare; `isinstance` se check karo.

5. **Template Method:** `ExamPaper` ABC — `generate()` = `_questions()` + `_shuffle()` (hook) + `_footer()`.
   `MathPaper` aur `EnglishPaper` banao. *Hint:* shuffle hook default me kuch na kare.

6. **`register()` ka experiment:** ek `Sizeable` ABC banao, ek purani class `register` karo jisme
   `__len__` na ho, phir `len()` call kar ke dekho kya hota hai — apne alfaz me likho kyun.

7. **`MutableSequence` se `LoggedList`** banao jo har `append`/`__setitem__` ko log kare.
   *Hint:* 5 abstract methods do, baqi mixin muft.

8. **`__subclasshook__`** se `Comparable` ABC banao jo un classes ko subclass maane
   jinme `__lt__` ho. `int`, `str`, aur apni ek class par test karo.

9. **LC 208 extend karo:** `Trie` me `delete(word)` aur `count_words_with_prefix(prefix)` add karo.
   *Hint:* har node par ek counter rakho.

10. **LC 1146 variant:** `SnapshotArray` me `snap_diff(id1, id2)` add karo jo un indexes ki list de
    jinki value badli. *Hint:* history par binary search dobara istemal karo.
"""),
    code("""
# ---- Exercise 1 aur 2 ka reference solution (khud koshish ke baad dekho) ----

class Vehicle(ABC):
    @property
    @abstractmethod
    def wheels(self): ...

    @abstractmethod
    def fuel_type(self): ...

    def describe(self):
        return f"{type(self).__name__}: {self.wheels} pahiye, {self.fuel_type()} par chalti hai"

class Car(Vehicle):
    wheels = 4
    def fuel_type(self): return "petrol"

class Bike(Vehicle):
    wheels = 2
    def fuel_type(self): return "petrol"

class Rickshaw(Vehicle):
    wheels = 3
    def fuel_type(self): return "CNG"

for v in (Car(), Bike(), Rickshaw()):
    print(v.describe())


class Cache(ABC):
    @abstractmethod
    def get(self, k): ...
    @abstractmethod
    def set(self, k, v): ...
    @abstractmethod
    def delete(self, k): ...

    def get_or_set(self, k, factory):        # template method
        val = self.get(k)
        if val is None:
            val = factory()
            self.set(k, val)
        return val

class DictCache(Cache):
    def __init__(self): self._d = {}
    def get(self, k): return self._d.get(k)
    def set(self, k, v): self._d[k] = v
    def delete(self, k): self._d.pop(k, None)

class NullCache(Cache):                      # Null Object pattern: sab kuch no-op
    def get(self, k): return None
    def set(self, k, v): pass
    def delete(self, k): pass

calls = []
def expensive():
    calls.append(1)
    return "computed"

dc, nc = DictCache(), NullCache()
print("\\ndict cache:", dc.get_or_set("x", expensive), dc.get_or_set("x", expensive), "-> factory calls:", len(calls))
calls.clear()
print("null cache:", nc.get_or_set("x", expensive), nc.get_or_set("x", expensive), "-> factory calls:", len(calls))
assert len(calls) == 2, "NullCache kuch save nahi karta, is liye har baar compute hoga"
print("[pass] exercises 1 & 2")
"""),
    md("""
## 22. Summary / Cheat-sheet

### Imports
```python
from abc import ABC, ABCMeta, abstractmethod
from typing import Protocol, runtime_checkable
from collections.abc import Iterable, Sized, Container, Sequence, Mapping, MutableMapping, Iterator
```

### ABC ka poora template
```python
class Base(ABC):
    @abstractmethod
    def must(self): ...                    # lazmi

    @property
    @abstractmethod
    def rate(self): ...                    # abstract property (order: property BAHAR)

    @classmethod
    @abstractmethod
    def from_dict(cls, d): ...             # abstract alternative constructor

    @staticmethod
    @abstractmethod
    def ext(): ...

    def template(self):                    # concrete: abstract steps ko call karta hai
        return self.must()

    def hook(self): pass                   # optional override
```

### Yaad rakhne wali baatein

| Cheez | Yaad rakho |
|---|---|
| `Base()` on abstract | `TypeError: Can't instantiate abstract class ...` |
| `Cls.__abstractmethods__` | frozenset; khaali = concrete class |
| `@abstractmethod` position | hamesha **innermost** (sabse neeche) |
| ABC without `ABC` base | bilkul bekar (koi enforcement nahi) |
| `register(X)` | virtual subclass: `isinstance` True, **methods nahi milte**, enforcement nahi |
| `__subclasshook__` | `issubclass` ka custom faisla; `NotImplemented` = default rules |
| `Protocol` | structural; `isinstance` ke liye `@runtime_checkable` lazmi |
| `Protocol` limits | signature check nahi; instantiate nahi hota; state na rakho |
| `Sequence` se inherit | `__getitem__` + `__len__` do → 5 methods muft |
| `MutableMapping` se inherit | 5 methods do → `get/keys/values/items/pop/update/setdefault` muft |
| `isinstance(x, Iterable)` | `str` bhi True deta hai — dhyan rakho |
| ABC vs Protocol | apni family + shared code → ABC; bahari/loose → Protocol |

### Decision flow (kaunsa tool?)
```
Sirf ek implementation hai?            -> koi abstraction nahi (YAGNI)
Shared code + apni class family?       -> ABC
Third-party / sirf shape matter karti? -> Protocol (+ runtime_checkable)
Standard container bana rahe ho?       -> collections.abc se inherit
Purani class ko family me lana hai?    -> register() ya Protocol
Algorithm ka order fix karna hai?      -> Template Method (ABC)
```

### Iske baad kya (next notebook)
`02_MRO_Multiple_Inheritance_Mixins_aur_super_Deep.ipynb` — MRO, C3 linearization,
diamond problem, cooperative `super()`, aur mixins ka poora design.
"""),
]

save(r"OOP in Python/Intermediate/01_Abstraction_ABC_Interfaces_and_Protocols.ipynb", CELLS)
