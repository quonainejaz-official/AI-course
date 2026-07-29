"""Generator: OOP in Python/Advance/01_Attribute_Access_Descriptors_aur_Properties_Deep.ipynb"""
import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

PATH = r"OOP in Python/Advance/01_Attribute_Access_Descriptors_aur_Properties_Deep.ipynb"

cells = []

cells += [
    md("""
# 01 — Attribute Access, Descriptors aur Properties (Deep Dive)

**Level:** Advanced OOP · **Series:** OOP in Python → Advance

Har dafa jab tum `obj.name` likhte ho, Python ek poora **algorithm** chalata hai — sirf dictionary
lookup nahi hoti. Us algorithm ka dil hai **descriptor protocol**. `property`, `classmethod`,
`staticmethod`, `__slots__`, functions ka bound-method ban jana, ORM ke `Field`s — sab isi ek
mechanism par khare hain.

Ye notebook us mechanism ko **zero se khol kar** dikhata hai.

## Is notebook me kya seekhenge

- `obj.x` ka **exact lookup order**: metaclass → `type(obj).__mro__` data descriptors → instance `__dict__` → class non-data descriptors/attrs → `__getattr__`
- `__getattribute__` override karna (aur **infinite recursion trap** se bachna)
- `__getattr__` vs `__getattribute__` — kaun kab chalta hai
- `__setattr__`, `__delattr__`, `__dir__` customize karna
- Descriptor protocol: `__get__`, `__set__`, `__delete__`, `__set_name__`
- **Data vs non-data descriptor** precedence ka live proof
- Function → method binding: methods asal me descriptors ki wajah se banti hain
- `property` ko **scratch se** likhna; `classmethod`/`staticmethod` ko descriptors se banana
- Real descriptors: `TypedField`, `RangeField`, `Positive`, `NonEmpty`, `UnitField`, `AuditedField`, `LazyProperty` vs `functools.cached_property`
- Descriptor + `__slots__` + `dataclass` ka interplay (yahan log phaste hain)
- **ORM-style declarative Model**: Field descriptors → validation + `to_dict()` + SQL generate
- Pitfalls: descriptor par shared class-level state, per-instance data theek se store karna, `__set_name__` kyun zaroori hai
- Performance considerations (plain attr vs property vs descriptor — asli timings)
- **LeetCode design problems** (146, 155, 706, 380) OOP nazariye se

## Prerequisites

- Classes, `self`, inheritance, MRO ki basic samajh
- `property` ka basic use (getter/setter) — agar nahi pata, koi masla nahi, hum yahan dobara banayenge
- Dunder methods ka concept (`__init__`, `__repr__`)

> **Padhne ka tareeqa:** har code cell chala kar output parho, phir markdown ka
> "Output ka matlab" hissa parho. Sirf theory parhne se descriptors samajh nahi aate.
"""),
    md("""
## 1. Pehla sawal: `obj.x` asal me kya karta hai?

**Kya hai:** `obj.x` ek *expression* hai jo Python ke andar `type(obj).__getattribute__(obj, "x")`
me tarjuma hota hai. Yani attribute access ek **method call** hai — aur isi liye hum use
customize kar sakte hain.

**Kyun ahem hai:** agar tumhein ye order pata hai to tum bata sakte ho ke conflict ki soorat me
kaun jeetega — instance ka data ya class ka descriptor. Interview me ye favourite sawal hai.

### Default algorithm (`object.__getattribute__`) — steps

```
obj.x  ==>  type(obj).__getattribute__(obj, "x")

1. cls = type(obj);  cls.__mro__ me "x" dhoondo  -> meta_attr
2. agar mila AUR us par __get__ AUR __set__/__delete__ dono me se koi hai
   => DATA DESCRIPTOR  => uska __get__(obj, cls) return karo   [SAB SE ZYADA priority]
3. warna obj.__dict__["x"] dekho  => mil gaya to wahi return karo (as-is)
4. warna step 1 me mila hua class attribute dekho:
      - agar us par sirf __get__ hai => NON-DATA descriptor => __get__(obj, cls)
      - warna plain class attribute return karo
5. kuch bhi na mila => AttributeError raise ho
6. AttributeError raise hone par HI Python cls.__getattr__(obj, "x") ko bulata hai (agar mojood ho)
```

**Yaad rakhne ka jumla:** *"Data descriptor > instance dict > non-data descriptor / class attr >
`__getattr__`."*
"""),
    code('''
# Chalo lookup order ko print kar kar dekhein — abhi sirf class attr vs instance dict.
class Config:
    debug = False          # class attribute (shared)

    def __init__(self, name):
        self.name = name   # instance attribute (per object, obj.__dict__ me jata hai)


c = Config("prod")

print("c.__dict__          ->", c.__dict__)          # sirf instance ka apna data
print("'debug' in c.__dict__ ->", "debug" in c.__dict__)  # False: class par hai, instance par nahi
print("c.debug             ->", c.debug)             # step 4: class attribute mila
print("Config.debug        ->", Config.debug)

# Ab instance par SAME naam se value likho -> shadowing ho jayegi
c.debug = True                                        # instance __dict__ me naya key
print("\\nbaad me c.__dict__ ->", c.__dict__)
print("c.debug             ->", c.debug, " (instance dict jeet gaya)")
print("Config.debug        ->", Config.debug, " (class wali ab bhi purani)")

# Instance wali delete karo -> dobara class wali dikhne lagegi
del c.debug
print("\\ndel ke baad c.debug ->", c.debug, " (class attr wapis dikh raha hai)")
'''),
    md("""
**Output ka matlab:** `c.debug = True` ne class ki value **change nahi ki** — sirf instance ke
`__dict__` me ek naya entry banaya jo class wali ko *chhupa* deta hai (shadowing). `del c.debug`
se wo parda hat gaya.

**Common mistake:** log samajhte hain `c.debug = True` ne `Config.debug` badal diya. Nahi.
Class-level state badalne ke liye `Config.debug = True` likhna parta hai (ya `type(c).debug`).

**Gotcha (mutable class attribute):** agar class attribute list/dict ho aur tum `c.items.append(1)`
karo to koi shadowing nahi hoti — tum **shared** object ko mutate kar rahe ho, sab instances
mutasir honge. Isi liye mutable defaults `__init__` me banao.
"""),
    code('''
# Mutable class attribute ka classic bug — dekh lo taake zindagi me kabhi na phanso.
class BadCart:
    items = []             # GALAT: sab instances is EK list ko share karenge

    def add(self, x):
        self.items.append(x)   # koi assignment nahi -> shadowing nahi -> shared list mutate


a, b = BadCart(), BadCart()
a.add("laptop")
print("b.items (BadCart) ->", b.items, " <- b ne kuch add nahi kiya tha!")
print("same object?      ->", a.items is b.items)


class GoodCart:
    def __init__(self):
        self.items = []    # THEEK: har instance ki apni list

    def add(self, x):
        self.items.append(x)


x, y = GoodCart(), GoodCart()
x.add("laptop")
print("\\ny.items (GoodCart) ->", y.items)
print("same object?       ->", x.items is y.items)
assert x.items is not y.items
'''),
    md("""
## 2. `__getattribute__` — har access ka gatekeeper

**Kya hai:** `__getattribute__` **har** attribute access par chalta hai (mile ya na mile).
`__getattr__` sirf **fallback** hai — tab chalta hai jab normal lookup `AttributeError` de.

**Kyun override karein:** logging/tracing, proxy objects, access control, lazy loading.

**Syntax:**

```python
class C:
    def __getattribute__(self, name):
        # ... apna kaam ...
        return object.__getattribute__(self, name)   # asli kaam base class se karao
```

### ⚠️ Infinite recursion trap

`__getattribute__` ke andar agar tum `self.kuch_bhi` likho to wo **dobara**
`__getattribute__` ko bulayega → infinite recursion → `RecursionError`.
Hal: `object.__getattribute__(self, name)` ya `super().__getattribute__(name)` use karo.
"""),
    code('''
# Pehle GALAT tareeqa (jaan boojh kar) — try/except me lipta hua taake notebook chalta rahe.
class RecursiveTrap:
    def __init__(self):
        self.value = 10

    def __getattribute__(self, name):
        # GALAT: self.log_count khud __getattribute__ ko bulata hai -> recursion
        self.log_count = 0
        return object.__getattribute__(self, name)


try:
    RecursiveTrap().value
except RecursionError as e:
    print("RecursionError pakra gaya:", type(e).__name__)
    print("Sabaq: __getattribute__ ke andar self.<attr> likhna = apne aap ko bulana.")
'''),
    code('''
# THEEK tareeqa: har access log karo, magar internal kaam object.__getattribute__ se.
class Traced:
    def __init__(self, value):
        # __init__ me assignment __setattr__ se guzarta hai, __getattribute__ se nahi
        object.__setattr__(self, "_log", [])   # safest: seedha object ka setattr
        object.__setattr__(self, "value", value)

    def __getattribute__(self, name):
        # log list ko bhi object.__getattribute__ se hi lo (warna recursion)
        log = object.__getattribute__(self, "_log")
        if not name.startswith("_"):
            log.append(name)                    # sirf public attrs trace karo
        return object.__getattribute__(self, name)   # asli lookup

    def double(self):
        return self.value * 2


t = Traced(21)
print("t.value  ->", t.value)
print("t.double() ->", t.double())              # 'double' + andar 'value' dono log honge
print("access log ->", object.__getattribute__(t, "_log"))
assert object.__getattribute__(t, "_log") == ["value", "double", "value"]
'''),
    md("""
**Output ka matlab:** log me `value`, `double`, `value` aaya — `t.double()` ne pehle method ko
lookup kiya, phir method ke andar `self.value` ne dobara lookup kiya. Yani **method call bhi ek
attribute access hai**.

**Interview tip:** "`__getattribute__` aur `__getattr__` me farq?" → `__getattribute__` **hamesha**
chalta hai aur default implementation poora lookup algorithm hai; `__getattr__` sirf **naakami ke
baad** bulaya jata hai. `__getattribute__` override karna khatarnak hai (performance + recursion),
`__getattr__` safe aur sasta hai.
"""),
    md("""
## 3. `__getattr__` — sirf fallback (aur bohat kaam ka)

**Kya hai:** jab normal lookup fail ho jaye (AttributeError) tab Python `__getattr__(self, name)`
bulata hai. Iska matlab: **jo attributes mojood hain unke liye ye chalta hi nahi** → zero cost.

**Kahan use hota hai:**
- Dynamic/proxy objects (`obj.anything` → API call, config key, JSON field)
- Deprecated names ko naye names par redirect karna
- Attribute-style dictionary access (`cfg.database.host`)

**Gotcha:** `__getattr__` me *hamesha* `AttributeError` raise karo agar naam handle nahi kar sakte,
warna `hasattr`, `copy`, `pickle` jaise stdlib tools jo `__deepcopy__`/`__reduce__` dhoondte hain,
galat jawab pa kar toot jate hain.
"""),
    code('''
class AttrDict:
    """dict jise obj.key ki tarah bhi parh sakein (nested bhi)."""

    def __init__(self, data):
        # __dict__ me seedha daal do -> normal lookup pehle isi ko dhoondega
        self._data = dict(data)

    def __getattr__(self, name):
        # NOTE: ye sirf tab chalta hai jab 'name' normal tareeqe se na mile
        try:
            value = self._data[name]
        except KeyError:
            # LAZMI: unknown naam par AttributeError, warna hasattr/copy/pickle toot jate hain
            raise AttributeError(f"{type(self).__name__!r} me koi attribute {name!r} nahi") from None
        # nested dict ko bhi AttrDict bana do -> cfg.db.host chalega
        return AttrDict(value) if isinstance(value, dict) else value

    def __dir__(self):
        # tab completion / dir() me keys bhi dikhao
        return sorted(set(list(super().__dir__()) + list(self._data)))


cfg = AttrDict({"env": "prod", "db": {"host": "127.0.0.1", "port": 5432}})
print("cfg.env      ->", cfg.env)
print("cfg.db.host  ->", cfg.db.host)      # nested
print("cfg.db.port  ->", cfg.db.port)

try:
    cfg.missing
except AttributeError as e:
    print("missing par  ->", e)

print("hasattr(cfg,'env')     ->", hasattr(cfg, "env"))
print("hasattr(cfg,'nope')    ->", hasattr(cfg, "nope"))   # AttributeError -> False
print("dir() me keys dikh rahi:", [n for n in dir(cfg) if not n.startswith("_")])
assert cfg.db.port == 5432 and not hasattr(cfg, "nope")
'''),
    code('''
# Use-case 2: purane attribute names ko deprecate karna, bina code toray.
import warnings

class ApiClient:
    _renamed = {"baseUrl": "base_url", "apiKey": "api_key"}   # purana -> naya

    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def __getattr__(self, name):
        # sirf un naamon par chalega jo mojood nahi (yani purane camelCase names)
        if name in self._renamed:
            new = self._renamed[name]
            warnings.warn(f"{name!r} deprecated hai, {new!r} use karo", DeprecationWarning, stacklevel=2)
            return getattr(self, new)          # naye naam par redirect
        raise AttributeError(name)


client = ApiClient("https://api.test", "k-123")
# catch_warnings(record=True) se warning capture karte hain (stderr ganda nahi hota)
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    old = client.baseUrl                       # purana naam
print("purane naam se mila ->", old)
print("warning category    ->", caught[0].category.__name__)
print("warning message     ->", caught[0].message)
assert old == "https://api.test" and caught[0].category is DeprecationWarning
'''),
    md("""
## 4. `__setattr__`, `__delattr__`, `__dir__`

- `__setattr__(self, name, value)` — **har** assignment (`obj.x = 1`) par chalta hai. Yahan bhi
  recursion trap: andar `self.x = ...` likhne se dobara khud bulao ge. `object.__setattr__` ya
  `self.__dict__[name] = value` use karo.
- `__delattr__(self, name)` — `del obj.x` par.
- `__dir__(self)` — `dir(obj)` ka output.

**Use-cases:** read-only / frozen objects, allowed-fields whitelist, auto type-coercion,
change tracking (dirty flags for ORM).
"""),
    code('''
class Frozen:
    """Ek immutable-ish object: banne ke baad koi attribute set/delete nahi ho sakta."""

    _ready = False   # class-level flag: __init__ ke doran False rehta hai

    def __init__(self, **kw):
        for k, v in kw.items():
            self.__dict__[k] = v        # __setattr__ bypass (seedha dict me)
        # instance par flag set karo — ab se lock
        self.__dict__["_ready"] = True

    def __setattr__(self, name, value):
        if self._ready:                 # normal lookup: instance dict -> True
            raise AttributeError(f"{type(self).__name__} immutable hai; {name!r} set nahi ho sakta")
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        raise AttributeError(f"{type(self).__name__} immutable hai; {name!r} delete nahi ho sakta")

    def __repr__(self):
        inner = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if k != "_ready")
        return f"Frozen({inner})"


p = Frozen(x=3, y=4)
print(p)
for action, fn in [("set", lambda: setattr(p, "x", 99)), ("del", lambda: delattr(p, "x"))]:
    try:
        fn()
    except AttributeError as e:
        print(f"{action} rok diya gaya ->", e)
assert p.x == 3
'''),
    code('''
class StrictModel:
    """Sirf declared fields allowed — typo par foran error (dirty tracking ke sath)."""

    ALLOWED = {"id", "title", "price"}

    def __init__(self, **kw):
        object.__setattr__(self, "_dirty", set())   # kaun kaun se field badle
        for k, v in kw.items():
            setattr(self, k, v)                     # apna __setattr__ hi chale (validation ke liye)
        self._dirty.clear()                         # initial load ko "change" na ginein

    def __setattr__(self, name, value):
        if name not in self.ALLOWED and not name.startswith("_"):
            # typo pakro: obj.titel = "x" chup chaap na chale
            raise AttributeError(f"unknown field {name!r}; allowed: {sorted(self.ALLOWED)}")
        object.__setattr__(self, name, value)
        if not name.startswith("_"):
            self._dirty.add(name)                   # change track karo

    def changed(self):
        return sorted(self._dirty)


m = StrictModel(id=1, title="Book", price=250)
print("shuru me changed ->", m.changed())
m.price = 300
print("price badalne ke baad ->", m.changed())
try:
    m.titel = "typo!"                               # jaan boojh kar galat naam
except AttributeError as e:
    print("typo pakra gaya ->", e)
assert m.changed() == ["price"]
'''),
]

cells += [
    md("""
## 5. Descriptor protocol — asli engine

**Kya hai:** koi bhi **class** jo in me se koi method define kare, wo **descriptor** hai:

| Method | Kab chalta hai | Signature |
|---|---|---|
| `__get__(self, obj, objtype=None)` | value parhte waqt | `obj` = instance (ya `None` agar class se access) |
| `__set__(self, obj, value)` | value likhte waqt | assignment intercept |
| `__delete__(self, obj)` | `del obj.attr` | deletion intercept |
| `__set_name__(self, owner, name)` | class banne ke waqt **ek dafa** | apna naam pata chalta hai |

**Do qismein:**

- **Data descriptor** — `__set__` ya `__delete__` (kam az kam ek) mojood ho. Instance `__dict__`
  se **zyada** priority.
- **Non-data descriptor** — sirf `__get__`. Instance `__dict__` se **kam** priority.

**Sab se ahem baat:** descriptor **class ke attribute** ke tor par rakha jata hai, instance par
nahi. `self.field = TypedField()` kaam **nahi** karega.

```python
class Model:
    age = TypedField(int)   # <- yahan (class body me) hi kaam karta hai
```
"""),
    code('''
# Sab se pehla, sab se saada descriptor: har call ko print karta hai (protocol dekhne ke liye).
class LoudDescriptor:
    def __set_name__(self, owner, name):
        # class banne ke waqt Python khud bulata hai: owner=class, name=attribute ka naam
        print(f"  __set_name__(owner={owner.__name__}, name={name!r})")
        self.name = name
        self.storage = "_" + name            # per-instance data yahan rakhenge

    def __get__(self, obj, objtype=None):
        if obj is None:
            print(f"  __get__ CLASS se ({objtype.__name__}.{self.name}) -> khud descriptor")
            return self                       # Model.age -> descriptor object
        print(f"  __get__ instance se ({self.name})")
        return getattr(obj, self.storage, None)

    def __set__(self, obj, value):
        print(f"  __set__({self.name}, {value!r})")
        setattr(obj, self.storage, value)     # instance ke apne dict me

    def __delete__(self, obj):
        print(f"  __delete__({self.name})")
        delattr(obj, self.storage)


print("class define ho rahi hai:")
class Demo:
    x = LoudDescriptor()      # <- __set_name__ abhi chalega

print("\\nobject banao:")
d = Demo()
print("\\nlikhna: d.x = 5")
d.x = 5
print("\\nparhna: d.x")
print("  natija ->", d.x)
print("\\nclass se: Demo.x")
print("  natija ->", type(Demo.x).__name__)
print("\\ndelete: del d.x")
del d.x
print("\\nab d.x ->", d.x, "(storage gayab, default None)")
'''),
    md("""
**Output ka matlab:**
1. `__set_name__` **class body chalte waqt** hi chal gaya — object banane se pehle. Isi liye
   descriptor ko apna naam khud pata chal jata hai.
2. `obj is None` check zaroori hai: `Demo.x` (class se access) me `obj=None` aata hai. Isi wajah se
   `property` bhi class se access karne par `property` object deta hai, value nahi.
3. Data hum ne `obj.__dict__["_x"]` me rakha — **descriptor par nahi**. Ye sab se important niyam
   hai (agla section iski wajah dikhata hai).
"""),
    md("""
## 6. ☠️ Pitfall #1: descriptor par per-instance data rakhna

**Ghalti:** `self.value = value` descriptor ke andar likh dena. Lekin descriptor object **ek hi**
hota hai poori class ke liye — sab instances usi ko share karte hain. Natija: ek object ki value
doosre me dikhne lagti hai.

**Hal (3 tareeqe):**
1. `obj.__dict__[self.storage]` — sab se aam aur tez (per-instance)
2. `WeakKeyDictionary` — jab owner class me `__slots__` ho ya `__dict__` chhedna na ho
3. Naming: `self.storage = "_" + name` (`__set_name__` se), ya private mangled naam
"""),
    code('''
# GALAT: shared state — do objects ek doosre ka data khich rahe hain.
class BrokenField:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.value                    # BUG: descriptor par ek hi 'value'

    def __set__(self, obj, value):
        self.value = value                   # BUG: sab instances yahi likh rahe hain


class BrokenUser:
    name = BrokenField()


u1, u2 = BrokenUser(), BrokenUser()
u1.name = "Ali"
u2.name = "Sara"
print("u1.name ->", u1.name, " <- 'Ali' hona chahiye tha!")
print("u2.name ->", u2.name)
assert u1.name == "Sara", "yahi bug hai: shared state"
print("Sabaq: descriptor object PER-CLASS hai, per-instance nahi.")
'''),
    code('''
# THEEK #1: instance ke __dict__ me store karo.
class Field:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_{name}_value"      # collision se bachne ke liye

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        try:
            return obj.__dict__[self.storage]
        except KeyError:
            raise AttributeError(f"{self.name!r} abhi set nahi hua") from None

    def __set__(self, obj, value):
        obj.__dict__[self.storage] = value   # PER-INSTANCE


class User:
    name = Field()
    city = Field()


a, b = User(), User()
a.name, a.city = "Ali", "Lahore"
b.name, b.city = "Sara", "Karachi"
print("a ->", a.name, a.city)
print("b ->", b.name, b.city)
print("a.__dict__ ->", a.__dict__)
assert (a.name, b.name) == ("Ali", "Sara")

fresh = User()
try:
    fresh.name
except AttributeError as e:
    print("unset par ->", e)
'''),
    code('''
# THEEK #2: WeakKeyDictionary — jab owner class me __slots__ ho (koi __dict__ nahi).
import weakref

class WeakField:
    def __init__(self):
        self._values = weakref.WeakKeyDictionary()   # object mar jaye to entry bhi mit jaye

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self._values.get(obj)

    def __set__(self, obj, value):
        self._values[obj] = value


class Point:
    __slots__ = ("__weakref__",)    # __dict__ nahi, magar weakref support chahiye
    x = WeakField()
    y = WeakField()


p = Point()
p.x, p.y = 3, 4
print("p.x, p.y ->", p.x, p.y)
print("has __dict__? ->", hasattr(p, "__dict__"))
print("live entries ->", len(Point.x._values))
del p
import gc; gc.collect()
print("delete ke baad entries ->", len(Point.x._values), "(memory leak nahi hui)")
assert len(Point.x._values) == 0
'''),
    md("""
**Output ka matlab:** `WeakKeyDictionary` ne object marne par entry khud saaf kar di. Agar normal
`dict` use karte to descriptor humesha reference pakre rakhta → **memory leak**, object kabhi
collect na hota.

**Trade-off:** `WeakKeyDictionary` ke liye key **hashable** aur weak-referenceable honi chahiye.
`__slots__` wali class me `"__weakref__"` add karna parta hai. Normal case me `obj.__dict__`
tareeqa hi behtar (tez + simple) hai.
"""),
    md("""
## 7. `__set_name__` kyun zaroori hai?

Python 3.6 se pehle descriptor ko apna naam **manually** batana parta tha:

```python
class Model:
    age = TypedField(int, name="age")   # naam do dafa likhna para -> DRY violation + typo risk
```

`__set_name__(self, owner, name)` class creation ke waqt automatic chalta hai aur descriptor ko
uska attribute naam de deta hai.

**Kab NAHI chalta (gotcha):** agar descriptor class body ke bahar attach karo:

```python
class C: pass
C.x = Field()      # __set_name__ NAHI chalega! khud bulao:
Field.__set_name__(C.x, C, "x")   # ya type(C.x).__set_name__(C.x, C, "x")
```
"""),
    code('''
class NeedsName:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(f"_{self.name}")

    def __set__(self, obj, value):
        obj.__dict__[f"_{self.name}"] = value


# Case A: class body me -> __set_name__ chala
class InBody:
    field = NeedsName()

print("class body me   -> name =", InBody.field.name)

# Case B: baad me attach -> __set_name__ NAHI chala
class Later:
    pass

Later.field = NeedsName()
print("baad me attach  -> name attribute hai?", hasattr(Later.field, "name"))
try:
    Later().field
except AttributeError as e:
    print("istemal par crash ->", type(e).__name__, "-", e)

# Manually bulao -> theek ho gaya
type(Later.field).__set_name__(Later.field, Later, "field")
obj = Later()
obj.field = 7
print("manual __set_name__ ke baad ->", obj.field)
assert obj.field == 7 and InBody.field.name == "field"
'''),
    md("""
## 8. Data vs non-data descriptor — precedence ka live proof

Yehi wo hissa hai jo interview me sab se zyada poocha jata hai. Chalo **saabit** karein:

- **Data descriptor** (`__get__` + `__set__`): instance `__dict__` me same naam ho **to bhi**
  descriptor jeetega.
- **Non-data descriptor** (sirf `__get__`): instance `__dict__` jeetega.

Yehi wajah hai ke `functools.cached_property` (non-data) pehli dafa compute kar ke value ko
`obj.__dict__` me daal deti hai aur agli dafa **descriptor bilkul chalta hi nahi** → zero overhead.
Aur `property` (data descriptor) hamesha chalti hai.
"""),
    code('''
class DataDesc:
    """__get__ + __set__ => DATA descriptor."""
    def __get__(self, obj, objtype=None):
        return "DATA-descriptor ki value"
    def __set__(self, obj, value):
        print("   (DataDesc.__set__ chala — value instance dict me nahi gayi)")


class NonDataDesc:
    """sirf __get__ => NON-DATA descriptor."""
    def __get__(self, obj, objtype=None):
        return "NON-DATA-descriptor ki value"


class Battle:
    d = DataDesc()
    n = NonDataDesc()


b = Battle()
print("khali instance dict:", b.__dict__)
print("b.d ->", b.d)
print("b.n ->", b.n)

# Ab instance __dict__ me ZABARDASTI same naam daalo (__set__ bypass karte hue)
b.__dict__["d"] = "instance dict ki value"
b.__dict__["n"] = "instance dict ki value"
print("\\ninstance dict bhar diya:", b.__dict__)
print("b.d ->", b.d, "  <== DATA descriptor JEETA (dict ignore hua)")
print("b.n ->", b.n, "  <== instance dict JEETA (descriptor ignore hua)")

assert b.d == "DATA-descriptor ki value"
assert b.n == "instance dict ki value"
print("\\nNiyam saabit: data descriptor > instance __dict__ > non-data descriptor")
'''),
    code('''
# Practical asar: khud ka LazyProperty (non-data) vs property (data) — kitni dafa compute hota hai.
calls = {"lazy": 0, "prop": 0}

class LazyProperty:
    """Non-data descriptor: pehli dafa compute, phir instance dict me cache -> agli dafa bypass."""

    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = self.func(obj)
        obj.__dict__[self.name] = value    # SAME naam se dict me -> non-data hone ki wajah se jeet
        return value


class Report:
    def __init__(self, rows):
        self.rows = rows

    @LazyProperty
    def total_lazy(self):
        """Mehngi calculation (cache hone ke qabil)."""
        calls["lazy"] += 1
        return sum(self.rows)

    @property
    def total_prop(self):
        calls["prop"] += 1
        return sum(self.rows)


r = Report([1, 2, 3, 4, 5])
for _ in range(3):
    r.total_lazy, r.total_prop

print("total_lazy value ->", r.total_lazy, "| compute hua:", calls["lazy"], "dafa")
print("total_prop value ->", r.total_prop, "| compute hua:", calls["prop"], "dafa")
print("instance dict     ->", {k: v for k, v in r.__dict__.items() if k != 'rows'})
assert calls["lazy"] == 1, "lazy sirf ek dafa"
assert calls["prop"] == 4, "property har dafa"
'''),
    code('''
# functools.cached_property wahi kaam karti hai — aur stale-cache ka masla bhi wahi hai.
from functools import cached_property

class Basket:
    def __init__(self, prices):
        self.prices = list(prices)
        self.computed = 0

    @cached_property
    def total(self):
        self.computed += 1
        return sum(self.prices)


bk = Basket([100, 200])
print("total       ->", bk.total, "| computed:", bk.computed)
bk.prices.append(700)                    # data badal gaya...
print("data badla, total ->", bk.total, "| computed:", bk.computed, " <- STALE!")

# Cache invalidate karne ka tareeqa: dict se key hata do
del bk.__dict__["total"]                 # ya: bk.__dict__.pop("total", None)
print("cache clear ke baad ->", bk.total, "| computed:", bk.computed)
assert bk.total == 1000 and bk.computed == 2
print("\\nSabaq: cached_property sirf un values par jo instance ki lifetime me nahi badalti.")
'''),
]

cells += [
    md("""
## 9. Function → method: binding ka raaz

**Sawal:** `obj.method()` me `self` **kaun** deta hai?

**Jawab:** functions bhi **non-data descriptors** hain! `function.__get__(obj, cls)` ek
**bound method** object banata hai jo `obj` ko pehle argument ki tarah pakre rakhta hai.

```
Class.method      -> plain function        (obj=None mila, function khud return hua)
obj.method        -> bound method          (function.__get__(obj, Class))
obj.method(1)     -> function(obj, 1)      -> self=obj
```

Isi liye `self` "magic" nahi hai — ye descriptor protocol ka natural natija hai.
"""),
    code('''
class Greeter:
    def hello(self, who):
        return f"Hello {who}, main {type(self).__name__} hoon"


g = Greeter()

print("type(Greeter.hello)  ->", type(Greeter.hello).__name__)   # function
print("type(g.hello)        ->", type(g.hello).__name__)         # method (bound)
print("g.hello.__self__ is g ->", g.hello.__self__ is g)         # bound object
print("g.hello.__func__ is Greeter.hello ->", g.hello.__func__ is Greeter.hello)

# Manually bind karo — bilkul wahi natija
manual = Greeter.hello.__get__(g, Greeter)
print("\\nmanual bind ->", manual("Ali"))
print("normal      ->", g.hello("Ali"))
assert manual("Ali") == g.hello("Ali")

# Unbound function ko self khud dena para
print("\\nfunction ko direct bulao ->", Greeter.hello(g, "Sara"))

# Functions par __get__ hai magar __set__ nahi => NON-DATA descriptor
print("\\nfunction par __get__? ->", hasattr(Greeter.hello, "__get__"))
print("function par __set__? ->", hasattr(Greeter.hello, "__set__"))
'''),
    code('''
# Non-data hone ka asal asar: instance par same naam rakh do to method 'shadow' ho jati hai.
class Calc:
    def double(self, x):
        return x * 2


c = Calc()
print("class ki method ->", c.double(5))

c.double = lambda x: x * 100          # instance __dict__ me plain function (bind NAHI hoga)
print("instance ne shadow kiya ->", c.double(5), " <- self nahi mila, x=5")
print("c.__dict__ ->", list(c.__dict__))

del c.double
print("shadow hatane ke baad ->", c.double(5))
assert c.double(5) == 10

# GOTCHA: instance par rakha function bind nahi hota — isi liye monkey-patch class par karo
Calc.triple = lambda self, x: x * 3    # class par -> bind hoga
print("\\nclass par patch ->", c.triple(5))
'''),
    md("""
**Interview gold:** "`staticmethod` kyun chahiye jab hum instance par function rakh sakte hain?"
→ Kyunki **class** par rakha function bind hota hai (`self` chala jata hai). `staticmethod` binding
ko rok deta hai. Aur instance par rakha function bind nahi hota magar wo har object ke liye alag
memory leta hai aur `pickle`/`copy` me masle deta hai.
"""),
    md("""
## 10. `property` ko scratch se banao

`property` koi language keyword nahi — ye ek **data descriptor class** hai. Chalo apni
`MyProperty` likhein: `__get__`, `__set__`, `__delete__`, aur `.setter` / `.deleter` chaining.
"""),
    code('''
class MyProperty:
    """builtin property ka apna version — data descriptor."""

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget, self.fset, self.fdel = fget, fset, fdel
        # docstring getter se lo (help() ke liye)
        self.__doc__ = doc if doc is not None else getattr(fget, "__doc__", None)

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                    # Class.attr -> descriptor khud
        if self.fget is None:
            raise AttributeError(f"{self.name!r} readable nahi (koi getter nahi)")
        return self.fget(obj)

    def __set__(self, obj, value):         # <- iski mojudgi isay DATA descriptor banati hai
        if self.fset is None:
            raise AttributeError(f"{self.name!r} read-only hai")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError(f"{self.name!r} delete nahi ho sakta")
        self.fdel(obj)

    # --- decorator chaining: @x.setter naya object banata hai (immutable style) ---
    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


class Circle:
    def __init__(self, radius):
        self.radius = radius               # setter se guzrega (validation ke sath)

    @MyProperty
    def radius(self):
        """Circle ka radius (hamesha > 0)."""
        return self._radius

    @radius.setter
    def radius(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("radius number hona chahiye")
        if value <= 0:
            raise ValueError(f"radius > 0 hona chahiye, mila {value}")
        self._radius = value

    @MyProperty
    def area(self):
        """Computed, read-only."""
        return 3.141592653589793 * self._radius ** 2


ci = Circle(2)
print("radius ->", ci.radius)
print("area   ->", round(ci.area, 4))
print("docstring ->", Circle.radius.__doc__)

ci.radius = 5
print("naya area ->", round(ci.area, 4))

for bad, exc in [(-1, ValueError), ("abc", TypeError)]:
    try:
        ci.radius = bad
    except exc as e:
        print(f"{bad!r} rok diya ->", type(e).__name__, "-", e)

try:
    ci.area = 100                          # koi setter nahi
except AttributeError as e:
    print("read-only ->", e)

assert ci.radius == 5
assert isinstance(Circle.radius, MyProperty)
'''),
    code('''
# Sanity check: builtin property se behaviour match karta hai?
class WithBuiltin:
    def __init__(self, v):
        self._v = v

    @property
    def v(self):
        return self._v * 2

    @v.setter
    def v(self, x):
        self._v = x


class WithMine:
    def __init__(self, v):
        self._v = v

    @MyProperty
    def v(self):
        return self._v * 2

    @v.setter
    def v(self, x):
        self._v = x


bi, mi = WithBuiltin(10), WithMine(10)
print("builtin ->", bi.v, "| mine ->", mi.v)
bi.v = mi.v = 3
print("set ke baad: builtin ->", bi.v, "| mine ->", mi.v)
# dono data descriptors hain
print("\\nbuiltin property data descriptor? ->",
      hasattr(property, "__get__") and hasattr(property, "__set__"))
print("MyProperty data descriptor?       ->",
      hasattr(MyProperty, "__get__") and hasattr(MyProperty, "__set__"))
assert bi.v == mi.v == 6
'''),
    md("""
## 11. `classmethod` aur `staticmethod` ko descriptors se banao

- `staticmethod` — **binding rok** deta hai: `__get__` sirf function wapis kar deta hai.
- `classmethod` — function ko **class** se bind karta hai (`cls` pehla argument).

Dono **non-data** descriptors hain (sirf `__get__`).
"""),
    code('''
import functools

class MyStaticMethod:
    """__get__ bas function lauta deta hai -> koi self/cls nahi."""

    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)   # __name__, __doc__ copy

    def __get__(self, obj, objtype=None):
        return self.func                       # <-- binding NAHI

    def __call__(self, *a, **kw):              # class body ke andar direct call ke liye
        return self.func(*a, **kw)


class MyClassMethod:
    """__get__ function ko CLASS se bind karta hai."""

    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __get__(self, obj, objtype=None):
        if objtype is None:
            objtype = type(obj)
        # MethodType(func, objtype) => pehla arg cls ban jata hai
        return functools.partial(self.func, objtype)


class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @MyClassMethod
    def from_fahrenheit(cls, f):
        """Alternative constructor — cls automatic mila."""
        return cls((f - 32) * 5 / 9)

    @MyStaticMethod
    def is_valid(value):
        """Koi self/cls nahi chahiye — pure function."""
        return -273.15 <= value <= 1000

    def __repr__(self):
        return f"Temperature({self.celsius:.2f})"


t = Temperature.from_fahrenheit(212)
print("from_fahrenheit(212) ->", t)
print("instance se bhi      ->", Temperature(0).from_fahrenheit(32))
print("is_valid(25)   ->", Temperature.is_valid(25))
print("is_valid(-500) ->", Temperature.is_valid(-500))
print("instance se static ->", t.is_valid(50))
assert abs(t.celsius - 100) < 1e-9 and Temperature.is_valid(25) is True

# Inheritance ke sath: cls SUBCLASS hoti hai (yehi classmethod ka faida hai)
class KelvinTemp(Temperature):
    def __repr__(self):
        return f"KelvinTemp({self.celsius + 273.15:.2f}K)"


k = KelvinTemp.from_fahrenheit(32)
print("\\nsubclass se ->", k, "| type:", type(k).__name__)
assert isinstance(k, KelvinTemp), "classmethod ne subclass hi banayi"
'''),
    code('''
# Builtin classmethod/staticmethod bhi descriptors hi hain — proof.
class Probe:
    @classmethod
    def cm(cls): ...
    @staticmethod
    def sm(): ...
    @property
    def pr(self): ...
    def plain(self): ...


raw = {name: Probe.__dict__[name] for name in ("cm", "sm", "pr", "plain")}
print(f"{'attribute':10} {'type':18} {'__get__':>8} {'__set__':>8}  qism")
print("-" * 62)
for name, val in raw.items():
    has_get, has_set = hasattr(type(val), "__get__"), hasattr(type(val), "__set__")
    if has_get and has_set:
        kind = "DATA descriptor"
    elif has_get:
        kind = "non-data descriptor"
    else:
        kind = "plain object"
    print(f"{name:10} {type(val).__name__:18} {str(has_get):>8} {str(has_set):>8}  {kind}")

assert hasattr(type(raw["pr"]), "__set__")          # property = data
assert not hasattr(type(raw["cm"]), "__set__")      # classmethod = non-data
'''),
]

cells += [
    md("""
## 12. Real-world descriptors — ek chhoti validation library

Ab theory se practice. Hum ek **reusable** descriptor family banayenge:

```
Validated (abstract base: storage + hook)
├── TypedField    -> type check
├── RangeField    -> numeric min/max
├── Positive      -> > 0
├── NonEmpty      -> string/collection khali na ho
├── UnitField     -> input convert kar ke store (km -> m)
└── AuditedField  -> har change ka log
```

**Design ka usool:** base class storage aur error-message sambhale; subclass sirf `validate()`
(ya `transform()`) likhe. Yehi **Template Method** pattern hai.
"""),
    code('''
from abc import ABC, abstractmethod

class Validated(ABC):
    """Descriptors ke liye base: per-instance storage + validate() hook."""

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"__{name}"          # instance dict me is naam se

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        try:
            return obj.__dict__[self.storage]
        except KeyError:
            raise AttributeError(
                f"{objtype.__name__}.{self.name} abhi set nahi hua"
            ) from None

    def __set__(self, obj, value):
        value = self.transform(obj, value)   # subclass badal sakta hai
        self.validate(obj, value)            # subclass check karta hai
        obj.__dict__[self.storage] = value

    def __delete__(self, obj):
        obj.__dict__.pop(self.storage, None)

    def transform(self, obj, value):
        """Default: koi tabdeeli nahi. Subclass override kare (e.g. unit conversion)."""
        return value

    @abstractmethod
    def validate(self, obj, value):
        """Ghalat value par TypeError/ValueError raise karo."""

    def fail(self, value, why):
        raise ValueError(f"{self.name}={value!r} qabool nahi: {why}")


class TypedField(Validated):
    def __init__(self, expected_type, allow_none=False):
        self.expected_type, self.allow_none = expected_type, allow_none

    def validate(self, obj, value):
        if value is None and self.allow_none:
            return
        if not isinstance(value, self.expected_type):
            names = getattr(self.expected_type, "__name__", str(self.expected_type))
            raise TypeError(
                f"{self.name} ko {names} chahiye, mila {type(value).__name__}"
            )


class RangeField(Validated):
    def __init__(self, minimum=None, maximum=None):
        self.minimum, self.maximum = minimum, maximum

    def validate(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} number hona chahiye")
        if self.minimum is not None and value < self.minimum:
            self.fail(value, f">= {self.minimum} hona chahiye")
        if self.maximum is not None and value > self.maximum:
            self.fail(value, f"<= {self.maximum} hona chahiye")


class Positive(RangeField):
    def __init__(self):
        super().__init__(minimum=0)

    def validate(self, obj, value):
        super().validate(obj, value)
        if value == 0:
            self.fail(value, "strictly > 0 hona chahiye")


class NonEmpty(Validated):
    def transform(self, obj, value):
        return value.strip() if isinstance(value, str) else value   # trim kar do

    def validate(self, obj, value):
        if not hasattr(value, "__len__"):
            raise TypeError(f"{self.name} ki length honi chahiye (str/list/dict)")
        if len(value) == 0:
            self.fail(value, "khali nahi ho sakta")


print("Validation descriptors tayyar:",
      [c.__name__ for c in (TypedField, RangeField, Positive, NonEmpty)])
'''),
    code('''
# Chalo inhein ek class par lagayein aur har validator ko test karein.
class Product:
    name = NonEmpty()
    sku = TypedField(str)
    price = Positive()
    discount = RangeField(0, 100)
    stock = TypedField(int)
    note = TypedField(str, allow_none=True)

    def __init__(self, name, sku, price, discount=0, stock=0, note=None):
        self.name, self.sku, self.price = name, sku, price
        self.discount, self.stock, self.note = discount, stock, note

    def final_price(self):
        return round(self.price * (1 - self.discount / 100), 2)

    def __repr__(self):
        return f"Product({self.name!r}, {self.sku!r}, Rs{self.price}, -{self.discount}%)"


p = Product("  Laptop  ", "SKU-1", 150000, discount=10, stock=4)
print(p)
print("name trim hua ->", repr(p.name))
print("final price   ->", p.final_price())

bad_cases = [
    ("name", "", ValueError, "khali string"),
    ("name", "   ", ValueError, "sirf spaces (trim ke baad khali)"),
    ("price", -5, ValueError, "negative price"),
    ("price", 0, ValueError, "zero price"),
    ("discount", 150, ValueError, "range se bahar"),
    ("stock", "bohat", TypeError, "galat type"),
    ("sku", 123, TypeError, "int diya str ki jagah"),
]
print("\\n--- Validation tests ---")
for field, value, exc, why in bad_cases:
    try:
        setattr(p, field, value)
        print(f"[FAIL] {field}={value!r} pass ho gaya (nahi hona chahiye tha)")
    except exc as e:
        print(f"[ok] {why:32} -> {type(e).__name__}: {e}")

p.note = None            # allow_none=True
print("\\nnote=None chala ->", p.note)
assert p.price == 150000 and p.name == "Laptop"
'''),
    code('''
# UnitField: user jis unit me de, hum canonical unit me store karein.
class UnitField(Validated):
    """Input ko canonical unit me convert kar ke rakhta hai (e.g. km/cm -> meters)."""

    FACTORS = {"m": 1.0, "km": 1000.0, "cm": 0.01, "mm": 0.001, "mi": 1609.344}

    def __init__(self, canonical="m"):
        self.canonical = canonical

    def transform(self, obj, value):
        # value ya to number (canonical maan lo) ya (number, unit) tuple ya "5 km" string
        if isinstance(value, tuple) and len(value) == 2:
            num, unit = value
        elif isinstance(value, str):
            parts = value.split()
            if len(parts) != 2:
                raise ValueError(f"{self.name}: format '5 km' jaisa do, mila {value!r}")
            num, unit = float(parts[0]), parts[1]
        else:
            num, unit = value, self.canonical
        if unit not in self.FACTORS:
            raise ValueError(f"{self.name}: unknown unit {unit!r}; {sorted(self.FACTORS)}")
        return float(num) * self.FACTORS[unit] / self.FACTORS[self.canonical]

    def validate(self, obj, value):
        if value < 0:
            self.fail(value, "distance negative nahi ho sakti")


class Route:
    length = UnitField("m")          # sab kuch meters me store hoga

    def __init__(self, length):
        self.length = length


for inp in [5000, (5, "km"), "5 km", (500000, "cm"), "1 mi"]:
    r = Route(inp)
    print(f"input {str(inp):16} -> stored meters: {r.length:>10.3f}")

r = Route((5, "km"))
assert r.length == 5000.0
for bad in [(-1, "km"), (5, "parsec"), "5"]:
    try:
        Route(bad)
    except (ValueError, TypeError) as e:
        print(f"[ok] {str(bad):12} -> {type(e).__name__}: {e}")
'''),
    code('''
# AuditedField: har tabdeeli ka record (kis ne, kya se kya) — audit trails ke liye.
from datetime import datetime, timezone

class AuditedField(Validated):
    """Value badalne par per-instance change log rakhta hai."""

    LOG_ATTR = "_audit_log"

    def __init__(self, expected_type=object):
        self.expected_type = expected_type

    def validate(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} ko {self.expected_type.__name__} chahiye")

    def __set__(self, obj, value):
        old = obj.__dict__.get(self.storage, "<unset>")
        super().__set__(obj, value)                 # validate + store
        if old != value:                            # sirf asli change log karo
            log = obj.__dict__.setdefault(self.LOG_ATTR, [])
            log.append({
                "field": self.name,
                "old": old,
                "new": value,
                "at": datetime(2026, 1, 1, tzinfo=timezone.utc),   # test ke liye fixed
            })

    @staticmethod
    def history(obj, field=None):
        log = obj.__dict__.get(AuditedField.LOG_ATTR, [])
        return [e for e in log if field is None or e["field"] == field]


class Employee:
    name = AuditedField(str)
    salary = AuditedField(int)
    title = AuditedField(str)

    def __init__(self, name, salary, title):
        self.name, self.salary, self.title = name, salary, title


e = Employee("Ali", 100000, "Engineer")
e.salary = 120000            # promotion
e.title = "Senior Engineer"
e.salary = 120000            # same value -> log nahi hona chahiye
e.salary = 150000

print("Poora audit trail:")
for entry in AuditedField.history(e):
    print(f"  {entry['field']:7} {str(entry['old']):18} -> {entry['new']!r}")

print("\\nSirf salary ki history:", [(x["old"], x["new"]) for x in AuditedField.history(e, "salary")])
assert len(AuditedField.history(e, "salary")) == 3      # initial + 2 real changes
# total = name(1) + salary(3) + title(2) = 6; dobara same salary set karna log nahi hua
assert len(AuditedField.history(e)) == 6
print("\\nSame value dobara set karne par log nahi bara — theek.")
'''),
    md("""
## 13. Descriptor + `__slots__` + `dataclass` ka interplay

Yahan teen chhote magar tang karne wale masle hain:

1. **`__slots__` ke sath descriptor:** `__slots__` khud ek descriptor banata hai. Agar tum
   `__slots__ = ("x",)` likho **aur** `x = MyField()` bhi, to class body me naam **takra** jayega
   (`ValueError: 'x' in __slots__ conflicts with class variable`). Hal: slot ka naam alag rakho
   (`_x`) aur descriptor `_x` me store kare — ya `WeakKeyDictionary` use karo.

2. **`dataclass` ke sath descriptor:** Python 3.10+ me descriptor-typed fields support hain, magar
   **default** ki tafseer badal jati hai: `field: int = MyDesc()` me `MyDesc()` **default value**
   ban jata hai, aur `dataclass` `__init__` me `self.field = default` karta hai — jo descriptor ke
   `__set__` se guzarta hai. Iska matlab: default na dene par `descriptor object` khud value ban
   sakta hai. Isi liye descriptor ke `__get__` me `obj is None` ke sath ek "default" strategy chahiye.
"""),
    code('''
# 1) __slots__ + class variable ka conflict — live proof.
src = "class Bad:\\n    __slots__ = ('x',)\\n    x = 42\\n"
try:
    exec(src)
except ValueError as e:
    print("conflict ->", e)

# Hal: slot ka naam alag (_x) aur descriptor us me likhe.
class SlotField:
    def __set_name__(self, owner, name):
        self.name = name
        self.slot = f"_{name}"           # ye slot me mojood hona chahiye

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        try:
            return getattr(obj, self.slot)
        except AttributeError:
            raise AttributeError(f"{self.name} set nahi hua") from None

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} number hona chahiye")
        setattr(obj, self.slot, value)   # slot descriptor me store


class Vec:
    __slots__ = ("_x", "_y")             # descriptor ke naam se ALAG
    x = SlotField()
    y = SlotField()

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vec({self.x}, {self.y})"


v = Vec(3, 4)
print("\\nslots + descriptor ->", v, "| __dict__ hai?", hasattr(v, "__dict__"))
try:
    v.z = 9                              # slots ki wajah se naya attr allowed nahi
except AttributeError as e:
    print("naya attribute ->", type(e).__name__, "-", e)
try:
    v.x = "abc"
except TypeError as e:
    print("validation      ->", e)
assert v.x == 3 and not hasattr(v, "__dict__")
'''),
    code('''
# 2) dataclass + descriptor: default ka behaviour dekho (Python 3.10+ documented).
from dataclasses import dataclass, field, fields

class IntField:
    def __set_name__(self, owner, name):
        self.storage = f"_{name}"
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self          # <- dataclass isay "default" ki tarah dekh sakta hai
        return getattr(obj, self.storage, 0)

    def __set__(self, obj, value):
        if isinstance(value, IntField):
            # dataclass ne default (khud descriptor) pass kar diya -> 0 maan lo
            value = 0
        if not isinstance(value, int):
            raise TypeError(f"{self.name} int hona chahiye, mila {type(value).__name__}")
        setattr(obj, self.storage, value)


@dataclass
class Counter:
    hits: int = IntField()       # descriptor as "default"
    misses: int = IntField()


c1 = Counter()                   # koi arg nahi -> descriptor khud pass hua -> 0
c2 = Counter(hits=10, misses=3)
print("c1 ->", c1.hits, c1.misses)
print("c2 ->", c2.hits, c2.misses)
print("repr ->", c2)
try:
    Counter(hits="bohat")
except TypeError as e:
    print("validation chali ->", e)
print("\\ndataclass fields ->", [f.name for f in fields(Counter)])
assert (c1.hits, c2.hits) == (0, 10)
print("Sabaq: dataclass + descriptor mumkin hai, magar __set__ me 'descriptor mila' case handle karo.")
'''),
]

cells += [
    md("""
## 14. 🏗️ Mini-project: ORM-style declarative Model

Ab sab kuch jor kar wo cheez banate hain jo Django/SQLAlchemy/Pydantic jaise libraries karti hain:

```python
class User(Model):
    __table__ = "users"
    id = IntegerField(primary_key=True)
    email = StringField(max_length=120, unique=True)
    age = IntegerField(min_value=0, max_value=150, null=True)
```

Aur ye sab automatic mile:
- **Validation** har assignment par
- `to_dict()` / `from_dict()`
- `CREATE TABLE` aur `INSERT` SQL **generate**
- Achha `__repr__` aur `__eq__`
- Missing required fields ki list

**Design:** `Column` (descriptor base) + `Model.__init_subclass__` (fields collect karne ke liye —
metaclass ki zaroorat nahi! ye NB2 ka topic hai).
"""),
    code('''
class Column:
    """Base column descriptor: type + constraints + SQL type."""

    py_type = object
    sql_type = "TEXT"

    def __init__(self, *, primary_key=False, unique=False, null=False, default=None):
        self.primary_key, self.unique, self.null = primary_key, unique, null
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_col_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.storage in obj.__dict__:
            return obj.__dict__[self.storage]
        if self.default is not None:
            return self.default
        if self.null:
            return None
        raise AttributeError(f"{type(obj).__name__}.{self.name} set nahi hua aur null allowed nahi")

    def __set__(self, obj, value):
        if value is None:
            if not self.null:
                raise ValueError(f"{self.name} null nahi ho sakta")
            obj.__dict__[self.storage] = None
            return
        value = self.coerce(value)
        self.check(value)
        obj.__dict__[self.storage] = value

    def coerce(self, value):
        if not isinstance(value, self.py_type):
            raise TypeError(
                f"{self.name} ko {self.py_type.__name__} chahiye, mila {type(value).__name__}"
            )
        return value

    def check(self, value):
        """Subclass extra constraints yahan lagaye."""

    def ddl(self):
        parts = [self.name, self.sql_type]
        if self.primary_key:
            parts.append("PRIMARY KEY")
        if self.unique and not self.primary_key:
            parts.append("UNIQUE")
        if not self.null and not self.primary_key:
            parts.append("NOT NULL")
        return " ".join(parts)


class IntegerField(Column):
    py_type = int
    sql_type = "INTEGER"

    def __init__(self, *, min_value=None, max_value=None, **kw):
        super().__init__(**kw)
        self.min_value, self.max_value = min_value, max_value

    def coerce(self, value):
        if isinstance(value, bool):     # bool int ka subclass hai — mana karo
            raise TypeError(f"{self.name}: bool qabool nahi, int do")
        if isinstance(value, str) and value.lstrip("-").isdigit():
            value = int(value)          # "42" -> 42 (helpful coercion)
        return super().coerce(value)

    def check(self, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} >= {self.min_value} hona chahiye, mila {value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} <= {self.max_value} hona chahiye, mila {value}")


class StringField(Column):
    py_type = str
    sql_type = "VARCHAR"

    def __init__(self, *, max_length=None, choices=None, **kw):
        super().__init__(**kw)
        self.max_length, self.choices = max_length, choices

    def coerce(self, value):
        value = super().coerce(value)
        return value.strip()

    def check(self, value):
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f"{self.name} ki length <= {self.max_length} ho, mili {len(value)}")
        if self.choices is not None and value not in self.choices:
            raise ValueError(f"{self.name} in me se ho: {self.choices}, mila {value!r}")

    def ddl(self):
        base = super().ddl()
        if self.max_length:
            base = base.replace("VARCHAR", f"VARCHAR({self.max_length})", 1)
        return base


class FloatField(Column):
    py_type = float
    sql_type = "REAL"

    def coerce(self, value):
        if isinstance(value, int) and not isinstance(value, bool):
            value = float(value)        # int -> float chalega
        return super().coerce(value)


class BoolField(Column):
    py_type = bool
    sql_type = "BOOLEAN"


print("Columns tayyar:", [c.__name__ for c in (IntegerField, StringField, FloatField, BoolField)])
'''),
    code('''
class Model:
    """Base Model — __init_subclass__ se fields collect karta hai (metaclass ke baghair)."""

    __table__ = None

    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        # parent classes ke fields bhi lo (inheritance support)
        collected = {}
        for base in reversed(cls.__mro__):
            for name, val in vars(base).items():
                if isinstance(val, Column):
                    collected[name] = val
        cls._columns = collected
        if cls.__table__ is None:
            cls.__table__ = cls.__name__.lower() + "s"

    def __init__(self, **kw):
        unknown = set(kw) - set(self._columns)
        if unknown:
            raise TypeError(f"unknown field(s): {sorted(unknown)}; allowed: {sorted(self._columns)}")
        for name, value in kw.items():
            setattr(self, name, value)       # descriptor validation chalega

    # --- introspection ---
    @classmethod
    def columns(cls):
        return dict(cls._columns)

    def missing(self):
        out = []
        for name, col in self._columns.items():
            if col.storage not in self.__dict__ and col.default is None and not col.null:
                out.append(name)
        return sorted(out)

    def is_valid(self):
        return not self.missing()

    # --- serialization ---
    def to_dict(self):
        data = {}
        for name, col in self._columns.items():
            try:
                data[name] = getattr(self, name)
            except AttributeError:
                data[name] = None
        return data

    @classmethod
    def from_dict(cls, data):
        known = {k: v for k, v in data.items() if k in cls._columns}
        return cls(**known)

    # --- SQL ---
    @classmethod
    def create_table_sql(cls):
        cols = ",\\n  ".join(col.ddl() for col in cls._columns.values())
        return f"CREATE TABLE {cls.__table__} (\\n  {cols}\\n);"

    def insert_sql(self):
        if not self.is_valid():
            raise ValueError(f"required fields missing: {self.missing()}")
        data = {k: v for k, v in self.to_dict().items() if v is not None}
        cols = ", ".join(data)
        marks = ", ".join("?" for _ in data)
        return f"INSERT INTO {self.__table__} ({cols}) VALUES ({marks});", tuple(data.values())

    def __repr__(self):
        inner = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items() if v is not None)
        return f"{type(self).__name__}({inner})"

    def __eq__(self, other):
        return type(self) is type(other) and self.to_dict() == other.to_dict()

    def __hash__(self):
        return hash((type(self).__name__, tuple(sorted(
            (k, v) for k, v in self.to_dict().items() if not isinstance(v, (list, dict))))))


class User(Model):
    __table__ = "users"
    id = IntegerField(primary_key=True)
    email = StringField(max_length=120, unique=True)
    name = StringField(max_length=50)
    age = IntegerField(min_value=0, max_value=150, null=True)
    role = StringField(choices=("admin", "user", "guest"), default="user")
    score = FloatField(default=0.0)
    active = BoolField(default=True)


print(User.create_table_sql())
print("\\nColumns:", list(User.columns()))
'''),
    code('''
# Model ko istemal karein
u = User(id=1, email="  ali@test.com ", name="Ali", age=30)
print("object   ->", u)
print("email trim hua ->", repr(u.email))
print("defaults ->", "role:", u.role, "| score:", u.score, "| active:", u.active)
print("to_dict  ->", u.to_dict())
print("\\nINSERT   ->")
sql, params = u.insert_sql()
print(sql, "\\nparams:", params)

# Round-trip: dict -> object -> dict
back = User.from_dict(u.to_dict())
print("\\nround-trip equal? ->", back == u)
assert back == u

# Validation tests
print("\\n--- Model validation ---")
checks = [
    (lambda: User(id=1, email="a@b.c", name="A", age=-5), ValueError, "age negative"),
    (lambda: User(id=1, email="a@b.c", name="A", role="hacker"), ValueError, "role choices se bahar"),
    (lambda: User(id=1, email="x" * 200, name="A"), ValueError, "email bohat lamba"),
    (lambda: User(id="abc", email="a@b.c", name="A"), TypeError, "id galat type"),
    (lambda: User(id=True, email="a@b.c", name="A"), TypeError, "bool as int"),
    (lambda: User(idd=1), TypeError, "unknown field (typo)"),
]
for fn, exc, why in checks:
    try:
        fn()
        print(f"[FAIL] {why} pass ho gaya")
    except exc as e:
        print(f"[ok] {why:26} -> {type(e).__name__}: {str(e)[:60]}")

# Incomplete object
partial = User(id=2)
print("\\nmissing fields ->", partial.missing())
print("is_valid       ->", partial.is_valid())
try:
    partial.insert_sql()
except ValueError as e:
    print("insert roka    ->", e)
assert partial.missing() == ["email", "name"]

# Coercion: "42" -> 42, int -> float
u2 = User(id="42", email="b@c.d", name="Sara", score=95)
print("\\ncoercion -> id:", repr(u2.id), "| score:", repr(u2.score))
assert u2.id == 42 and u2.score == 95.0
'''),
    code('''
# Inheritance: subclass parent ke columns bhi paye
class AdminUser(User):
    __table__ = "admin_users"
    level = IntegerField(min_value=1, max_value=10)
    department = StringField(max_length=40, default="IT")


print("AdminUser columns ->", list(AdminUser.columns()))
print("\\n" + AdminUser.create_table_sql())

adm = AdminUser(id=9, email="root@test.com", name="Root", level=10)
print("\\n", adm)
print("department default ->", adm.department)
try:
    adm.level = 99
except ValueError as e:
    print("level validation ->", e)

assert "email" in AdminUser.columns() and "level" in AdminUser.columns()
assert len(AdminUser.columns()) == len(User.columns()) + 2
print("\\nInheritance theek: parent + child dono ke columns mile.")
'''),
    md("""
## 15. Performance considerations

Descriptors sasta abstraction hai magar **muft nahi**. Har access ek Python-level function call hai.

**Rough tarteeb (tez se sust):**

```
__slots__ attr  <  instance __dict__ attr  <  cached_property (2nd+ access)
                <  property  ≈  custom descriptor  <  __getattr__ fallback
                <  __getattribute__ override (sab se mehnga)
```

**Kab fikar karein:** sirf **hot loops** me (lakhon accesses). Warna clarity + validation ka
faida overhead se zyada hai.

**Optimisation tricks:**
1. Cache-able values par `cached_property` (non-data → 2nd access par descriptor bilkul skip)
2. Validation sirf `__init__`/setter me, getter me nahi
3. Hot path me local variable me nikaal lo: `r = self.radius` phir loop me `r` use karo
4. `__slots__` se memory + access dono behtar
"""),
    code('''
import timeit

class Plain:
    def __init__(self, v):
        self.v = v


class Slotted:
    __slots__ = ("v",)
    def __init__(self, v):
        self.v = v


class WithProperty:
    def __init__(self, v):
        self._v = v
    @property
    def v(self):
        return self._v


class SimpleDesc:
    def __set_name__(self, owner, name):
        self.storage = f"_{name}"
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__[self.storage]
    def __set__(self, obj, value):
        obj.__dict__[self.storage] = value


class WithDescriptor:
    v = SimpleDesc()
    def __init__(self, v):
        self.v = v


class WithGetattr:
    def __init__(self, v):
        self._data = {"v": v}
    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(name) from None


N = 200_000
objs = {
    "plain __dict__": Plain(1),
    "__slots__": Slotted(1),
    "property": WithProperty(1),
    "custom descriptor": WithDescriptor(1),
    "__getattr__ fallback": WithGetattr(1),
}
results = {}
for label, obj in objs.items():
    t = timeit.timeit("obj.v", globals={"obj": obj}, number=N)
    results[label] = t

base = results["plain __dict__"]
print(f"{N:,} attribute reads:\\n")
print(f"{'tareeqa':22} {'waqt (s)':>10} {'nisbat':>8}")
print("-" * 44)
for label, t in sorted(results.items(), key=lambda kv: kv[1]):
    print(f"{label:22} {t:>10.4f} {t / base:>7.2f}x")
print("\\nNote: absolute numbers machine par depend karte hain; TARTEEB ahem hai.")
assert results["plain __dict__"] < results["property"] * 2
'''),
    code('''
# cached_property ka faida hot loop me (sirf dobara access par).
import timeit
from functools import cached_property

class Heavy:
    def __init__(self, n):
        self.n = n

    @property
    def prop_sum(self):
        return sum(range(self.n))         # har dafa dobara

    @cached_property
    def cached_sum(self):
        return sum(range(self.n))         # sirf pehli dafa


h = Heavy(500)
h.cached_sum                              # cache garam karo
t_prop = timeit.timeit("h.prop_sum", globals={"h": h}, number=5_000)
t_cache = timeit.timeit("h.cached_sum", globals={"h": h}, number=5_000)
print(f"property     : {t_prop:.4f}s")
print(f"cached_prop  : {t_cache:.4f}s")
print(f"faida        : {t_prop / t_cache:.1f}x tez")
assert t_cache < t_prop

# Trick 3: hot loop me local variable
class Point3:
    def __init__(self, x):
        self._x = x
    @property
    def x(self):
        return self._x

p = Point3(2)
t_attr = timeit.timeit("total = 0\\nfor _ in range(100): total += p.x",
                       globals={"p": p}, number=2_000)
t_local = timeit.timeit("x = p.x\\ntotal = 0\\nfor _ in range(100): total += x",
                        globals={"p": p}, number=2_000)
print(f"\\nloop me p.x    : {t_attr:.4f}s")
print(f"local me nikala: {t_local:.4f}s  ({t_attr / t_local:.1f}x tez)")
'''),
]

cells += [
    md("""
## 16. Pitfalls & Gotchas — ek jaga par

| # | Pitfall | Kyun hota hai | Hal |
|---|---|---|---|
| 1 | Descriptor par `self.value = v` | descriptor **per-class** hai, per-instance nahi | `obj.__dict__[self.storage]` ya `WeakKeyDictionary` |
| 2 | `self.field = Field()` `__init__` me | descriptors sirf **class** attributes par kaam karte hain | class body me rakho |
| 3 | `__getattribute__` me `self.x` | dobara khud ko call | `object.__getattribute__(self, "x")` |
| 4 | `__setattr__` me `self.x = v` | dobara khud ko call | `object.__setattr__` ya `self.__dict__[...]` |
| 5 | `__getattr__` me `AttributeError` na raise karna | `hasattr`/`copy`/`pickle` toot jate hain | unknown naam par `raise AttributeError(name)` |
| 6 | Baad me `C.x = Field()` | `__set_name__` nahi chalta | manually bulao ya class body me rakho |
| 7 | `cached_property` badalte data par | non-data descriptor, dobara compute nahi karta | `del obj.__dict__["name"]` se invalidate |
| 8 | Mutable class attribute (`items = []`) | sab instances share karte hain | `__init__` me banao |
| 9 | `__slots__` + same naam ka class variable | slot descriptor takrata hai | naam alag rakho (`_x`) |
| 10 | `property` ko class se access kar ke value ki umeed | `obj is None` → descriptor khud milta hai | `Class.attr.fget(obj)` ya instance use karo |
| 11 | Descriptor me `objtype`/`obj` ignore karna | `Class.attr` par crash | hamesha `if obj is None: return self` |
| 12 | `bool` ko `int` samajhna validation me | `bool` `int` ka subclass hai | `isinstance(v, bool)` pehle check karo |
"""),
    code('''
# Pitfall #10 ka live demo + sahi tareeqa
class Celsius:
    def __init__(self, c):
        self._c = c

    @property
    def fahrenheit(self):
        return self._c * 9 / 5 + 32


t = Celsius(100)
print("instance se     ->", t.fahrenheit)
print("class se        ->", type(Celsius.fahrenheit).__name__, "(value nahi, property object)")
print("getter manually ->", Celsius.fahrenheit.fget(t))
assert Celsius.fahrenheit.fget(t) == t.fahrenheit

# Pitfall #11: obj is None check bhula do to kya hota hai
class Careless:
    def __get__(self, obj, objtype=None):
        return obj.__dict__["_v"]        # obj None ho to AttributeError/TypeError


class Holder:
    v = Careless()


try:
    Holder.v                             # class se access -> obj=None
except (AttributeError, TypeError) as e:
    print("\\nobj is None check nahi tha ->", type(e).__name__, "-", e)
print("Isi liye har __get__ ki pehli line: if obj is None: return self")
'''),
    md("""
## 17. LeetCode — Design problems (descriptors/attribute-access nazariye se)

Spec ke mutabiq: har notebook me LeetCode section. Ye chaar problems **class design** ki hain, aur
har ek me hum specifically dekhenge ke **kaun sa attribute-access ya data-structure choice** faisla
kun hai.

### LC 146. LRU Cache — Medium

🔗 https://leetcode.com/problems/lru-cache/

**Bayan:** `LRUCache(capacity)` banao jo `get(key)` aur `put(key, value)` support kare, dono
**O(1)** me. Capacity bhar jaye to **least recently used** key nikal do.

**Approach (OOP nazariya):**
- Chahiye: O(1) lookup **aur** O(1) recency reorder. Ek hi structure dono nahi de sakta → **do**
  structures jor do: `dict` (lookup) + **doubly linked list** (order).
- `Node` class = linked list ka element (`prev`, `next`, `key`, `val`). Yahan `__slots__` istemal
  karenge — lakhon nodes par memory bachegi aur access tez hoga (section 15 ka sabaq).
- Sentinel `head`/`tail` dummy nodes → edge cases (khali list, pehla/aakhri element) khatam.
- Python me shortcut: `OrderedDict.move_to_end` — dono versions dikha rahe hain.

**Time:** `get` O(1), `put` O(1) · **Space:** O(capacity)
"""),
    code('''
class _Node:
    """Doubly linked list node — __slots__ se memory/speed behtar."""
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key=None, val=None):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    """dict + doubly linked list => O(1) get/put."""

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("capacity > 0 honi chahiye")
        self.capacity = capacity
        self._map = {}                       # key -> _Node  (O(1) lookup)
        # sentinels: head.next = most recent, tail.prev = least recent
        self._head, self._tail = _Node(), _Node()
        self._head.next, self._tail.prev = self._tail, self._head

    # --- linked list helpers ---
    def _remove(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_front(self, node):
        node.prev, node.next = self._head, self._head.next
        self._head.next.prev = node
        self._head.next = node

    def get(self, key: int) -> int:
        node = self._map.get(key)
        if node is None:
            return -1
        self._remove(node)                   # recency update
        self._add_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        node = self._map.get(key)
        if node is not None:                 # update + promote
            node.val = value
            self._remove(node)
            self._add_front(node)
            return
        if len(self._map) >= self.capacity:  # evict LRU (tail se pehla)
            lru = self._tail.prev
            self._remove(lru)
            del self._map[lru.key]
        node = _Node(key, value)
        self._map[key] = node
        self._add_front(node)

    def keys_mru_to_lru(self):
        out, cur = [], self._head.next
        while cur is not self._tail:
            out.append(cur.key)
            cur = cur.next
        return out

    def __len__(self):
        return len(self._map)

    def __contains__(self, key):             # `key in cache` — recency change NAHI karta
        return key in self._map

    def __repr__(self):
        return f"LRUCache(cap={self.capacity}, mru->lru={self.keys_mru_to_lru()})"


# LeetCode ka official example
c = LRUCache(2)
c.put(1, 1)
c.put(2, 2)
assert c.get(1) == 1          # 1 recent ban gaya
c.put(3, 3)                   # 2 evict hui
assert c.get(2) == -1
c.put(4, 4)                   # 1 evict hui
assert c.get(1) == -1
assert c.get(3) == 3
assert c.get(4) == 4
print("LC146 official example ->", c)

# Extra tests
c2 = LRUCache(3)
for i in (1, 2, 3):
    c2.put(i, i * 10)
c2.get(1)                     # 1 ko promote karo
c2.put(4, 40)                 # sab se purani (2) nikle
assert c2.get(2) == -1 and c2.get(1) == 10
assert len(c2) == 3 and 3 in c2
print("extra tests ->", c2)
print("update-existing test:", end=" ")
c2.put(3, 999)
assert c2.get(3) == 999 and len(c2) == 3
print("ok")
print("[pass] LC 146")
'''),
    code('''
# Wahi problem, OrderedDict ke sath — kam code, wahi complexity.
from collections import OrderedDict

class LRUCacheOD:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._od = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self._od:
            return -1
        self._od.move_to_end(key)                 # O(1) recency update
        return self._od[key]

    def put(self, key: int, value: int) -> None:
        if key in self._od:
            self._od.move_to_end(key)
        self._od[key] = value
        if len(self._od) > self.capacity:
            self._od.popitem(last=False)          # O(1) sab se purana nikalo


# Dono implementations ko random ops par match karao (differential testing)
import random
random.seed(42)
a, b = LRUCache(4), LRUCacheOD(4)
for _ in range(3000):
    k = random.randint(1, 8)
    if random.random() < 0.5:
        assert a.get(k) == b.get(k), f"mismatch get({k})"
    else:
        v = random.randint(1, 100)
        a.put(k, v); b.put(k, v)
print("3000 random ops par dono implementations identical -> [pass]")
print("Sabaq: manual linked-list interview me maanga jata hai; production me OrderedDict use karo.")
'''),
    md("""
### LC 155. Min Stack — Easy

🔗 https://leetcode.com/problems/min-stack/

**Bayan:** Stack jo `push`, `pop`, `top`, aur `getMin()` — sab **O(1)** me kare.

**Approach (OOP nazariya):**
- Naive: `getMin()` me `min(stack)` → O(n). Chalega nahi.
- Trick: **invariant** rakho — har element ke sath us waqt ka minimum bhi store karo.
  Yani stack me `(value, min_so_far)` tuples. Push par `min(value, current_min)`.
- Yahan `property` ka acha use: `min_value` ko computed read-only property banao — API saaf,
  aur andar se O(1).

**Time:** sab operations O(1) · **Space:** O(n)
"""),
    code('''
class MinStack:
    """(value, min_so_far) pairs => getMin O(1)."""

    __slots__ = ("_stack",)

    def __init__(self):
        self._stack = []          # list of (value, min_so_far)

    def push(self, val: int) -> None:
        current_min = val if not self._stack else min(val, self._stack[-1][1])
        self._stack.append((val, current_min))

    def pop(self) -> None:
        if not self._stack:
            raise IndexError("khali stack se pop")
        self._stack.pop()

    def top(self) -> int:
        if not self._stack:
            raise IndexError("khali stack ka top")
        return self._stack[-1][0]

    def getMin(self) -> int:
        if not self._stack:
            raise IndexError("khali stack ka min")
        return self._stack[-1][1]

    # Pythonic API (property = data descriptor, read-only)
    @property
    def min_value(self):
        """getMin() ka Pythonic chehra — read-only computed."""
        return self.getMin()

    def __len__(self):
        return len(self._stack)

    def __bool__(self):
        return bool(self._stack)

    def __repr__(self):
        return f"MinStack(values={[v for v, _ in self._stack]}, min={self.getMin() if self else None})"


# LeetCode official example
s = MinStack()
s.push(-2); s.push(0); s.push(-3)
assert s.getMin() == -3
s.pop()
assert s.top() == 0
assert s.getMin() == -2
print("LC155 official ->", s)

# Duplicates aur min property
s2 = MinStack()
for v in [5, 5, 3, 3, 7]:
    s2.push(v)
assert s2.min_value == 3
s2.pop(); s2.pop()
assert s2.min_value == 3, "ek 3 abhi baqi hai"
s2.pop()
assert s2.min_value == 5
print("duplicates test ok ->", s2)

# property read-only hai
try:
    s2.min_value = 100
except AttributeError as e:
    print("min_value read-only ->", type(e).__name__)

for fn in (lambda: MinStack().pop(), lambda: MinStack().getMin(), lambda: MinStack().top()):
    try:
        fn()
    except IndexError:
        pass
    else:
        raise AssertionError("khali stack par error hona chahiye tha")
print("[pass] LC 155")
'''),
    md("""
### LC 706. Design HashMap — Easy

🔗 https://leetcode.com/problems/design-hashmap/

**Bayan:** Bina builtin dict/map ke apna HashMap banao: `put(key, value)`, `get(key)` (na mile to
-1), `remove(key)`.

**Approach (OOP nazariya):**
- **Separate chaining**: buckets ki list; har bucket ek list of `[key, value]`.
- `hash(key) % num_buckets` se bucket chuno. Prime bucket count (2069) clustering kam karta hai.
- Load factor barh jaye to **resize** (rehash) — yahi dict ka amortized O(1) ka raaz hai.
- Descriptor connection: `obj.__dict__` khud aisa hi hash map hai; `obj.x` = hash lookup + attribute
  protocol. Isi liye `__slots__` (array offset) `__dict__` se tez hota hai.

**Time:** average O(1), worst O(n) per op · **Space:** O(n)
"""),
    code('''
class MyHashMap:
    """Separate chaining + dynamic resize."""

    INITIAL_BUCKETS = 8
    MAX_LOAD = 0.75

    def __init__(self):
        self._buckets = [[] for _ in range(self.INITIAL_BUCKETS)]
        self._size = 0

    def _index(self, key):
        return hash(key) % len(self._buckets)

    def _resize(self):
        old = self._buckets
        self._buckets = [[] for _ in range(len(old) * 2)]
        self._size = 0
        for bucket in old:
            for k, v in bucket:
                self.put(k, v)                       # rehash

    def put(self, key: int, value: int) -> None:
        bucket = self._buckets[self._index(key)]
        for pair in bucket:                          # mojood key -> update
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size / len(self._buckets) > self.MAX_LOAD:
            self._resize()

    def get(self, key: int) -> int:
        for k, v in self._buckets[self._index(key)]:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        bucket = self._buckets[self._index(key)]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return

    def __len__(self):
        return self._size

    def __contains__(self, key):
        return self.get(key) != -1

    def stats(self):
        lengths = [len(b) for b in self._buckets]
        return {"buckets": len(self._buckets), "size": self._size,
                "longest_chain": max(lengths), "empty_buckets": lengths.count(0)}


# LeetCode official example
m = MyHashMap()
m.put(1, 1)
m.put(2, 2)
assert m.get(1) == 1
assert m.get(3) == -1
m.put(2, 1)                 # update
assert m.get(2) == 1
m.remove(2)
assert m.get(2) == -1
print("LC706 official example -> ok")

# Resize + bara load test, aur builtin dict se muqabla
m2 = MyHashMap()
reference = {}
for i in range(1000):
    m2.put(i, i * i)
    reference[i] = i * i
assert all(m2.get(k) == v for k, v in reference.items())
print("1000 inserts ->", m2.stats())

for k in range(0, 1000, 3):
    m2.remove(k)
    del reference[k]
assert all(m2.get(k) == v for k, v in reference.items())
assert all(m2.get(k) == -1 for k in range(0, 1000, 3))
assert len(m2) == len(reference)
print("deletions ke baad size match ->", len(m2))
print("0 in m2? ->", 0 in m2, "| 1 in m2? ->", 1 in m2)
print("[pass] LC 706")
'''),
    md("""
### LC 380. Insert Delete GetRandom O(1) — Medium

🔗 https://leetcode.com/problems/insert-delete-getrandom-o1/

**Bayan:** `insert(val)`, `remove(val)`, `getRandom()` — teeno **average O(1)**. `getRandom` har
mojood element ko barabar probability de.

**Approach (OOP nazariya):**
- `getRandom` O(1) ke liye **contiguous array** chahiye (`random.choice` index se). Magar array se
  remove O(n) hai.
- Trick: **swap-with-last** — jo element hatana hai use aakhri element se badal do, phir `pop()`.
  O(1) ho gaya.
- Position track karne ke liye `dict: val -> index`. Yani phir **do structures ka combo**
  (LC 146 wala hi usool).
- Design lesson: "O(1) random access" + "O(1) delete" ek structure se nahi milte → **compose** karo.

**Time:** teeno average O(1) · **Space:** O(n)
"""),
    code('''
import random

class RandomizedSet:
    """list (random access) + dict val->index (O(1) locate) + swap-with-last delete."""

    def __init__(self):
        self._items = []          # dense array
        self._pos = {}            # val -> index in _items

    def insert(self, val: int) -> bool:
        if val in self._pos:
            return False
        self._pos[val] = len(self._items)
        self._items.append(val)
        return True

    def remove(self, val: int) -> bool:
        idx = self._pos.get(val)
        if idx is None:
            return False
        last = self._items[-1]
        # aakhri element ko hatne wali jagah par le aao
        self._items[idx] = last
        self._pos[last] = idx
        self._items.pop()
        del self._pos[val]
        return True

    def getRandom(self) -> int:
        if not self._items:
            raise IndexError("khali set")
        return random.choice(self._items)     # O(1)

    def __len__(self):
        return len(self._items)

    def __contains__(self, val):
        return val in self._pos

    def _check_invariant(self):
        """Har val ka index theek hai? (testing ke liye)"""
        assert len(self._items) == len(self._pos)
        for v, i in self._pos.items():
            assert self._items[i] == v, f"invariant tuta: {v} index {i} par nahi"
        return True


# LeetCode official example
rs = RandomizedSet()
assert rs.insert(1) is True
assert rs.remove(2) is False
assert rs.insert(2) is True
assert rs.getRandom() in (1, 2)
assert rs.remove(1) is True
assert rs.insert(2) is False
assert rs.getRandom() == 2
print("LC380 official example -> ok")

# Invariant stress test
random.seed(7)
rs2 = RandomizedSet()
mirror = set()
for _ in range(4000):
    v = random.randint(1, 60)
    if random.random() < 0.55:
        assert rs2.insert(v) == (v not in mirror)
        mirror.add(v)
    else:
        assert rs2.remove(v) == (v in mirror)
        mirror.discard(v)
    rs2._check_invariant()
assert len(rs2) == len(mirror) and all(v in rs2 for v in mirror)
print(f"4000 random ops, invariant qaim, size={len(rs2)}")

# Distribution fairness (uniform?)
rs3 = RandomizedSet()
for v in range(5):
    rs3.insert(v)
random.seed(1)
counts = {}
for _ in range(50_000):
    k = rs3.getRandom()
    counts[k] = counts.get(k, 0) + 1
print("distribution ->", dict(sorted(counts.items())))
assert all(8_500 < c < 11_500 for c in counts.values()), "kaafi uniform hona chahiye"
print("[pass] LC 380")
'''),
    md("""
## 18. Khud karo — Exercises

Koshish khud karo, phir neeche solution cell chala kar match karo.

1. **`ChoiceField`** descriptor: sirf given options me se value accept kare, aur `options` ko
   read-only property se expose kare.
2. **`ReadOnlyAfterSet`** descriptor: pehli dafa set ho jaye, uske baad koi change nahi
   (write-once field).
3. **`Alias`** non-data descriptor: `full = Alias("name")` → `obj.full` = `obj.name`.
4. **`CallCounter`** descriptor: method par lagao, ye count kare method kitni dafa chali (per
   instance).
5. **`ValidatedDict`**: `__getattr__` + `__setattr__` se dict jise attribute ki tarah use karein,
   magar sirf allowed keys.
"""),
    code('''
# --- Solutions ---

# 1) ChoiceField
class ChoiceField:
    def __init__(self, *options):
        if not options:
            raise ValueError("kam az kam ek option do")
        self._options = tuple(options)

    @property
    def options(self):                # read-only
        return self._options

    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_choice_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.storage, self._options[0])   # pehla = default

    def __set__(self, obj, value):
        if value not in self._options:
            raise ValueError(f"{self.name}: {value!r} allowed nahi; options: {self._options}")
        obj.__dict__[self.storage] = value


# 2) ReadOnlyAfterSet
class ReadOnlyAfterSet:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_ro_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.storage not in obj.__dict__:
            raise AttributeError(f"{self.name} abhi set nahi hua")
        return obj.__dict__[self.storage]

    def __set__(self, obj, value):
        if self.storage in obj.__dict__:
            raise AttributeError(f"{self.name} write-once hai; ab {self.name} badal nahi sakta")
        obj.__dict__[self.storage] = value


# 3) Alias (non-data: sirf __get__)
class Alias:
    def __init__(self, target):
        self.target = target

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.target)


# 4) CallCounter (non-data descriptor jo bound wrapper deta hai)
import functools

class CallCounter:
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __set_name__(self, owner, name):
        self.name = name
        self.counter_attr = f"_calls_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        @functools.wraps(self.func)
        def wrapper(*a, **kw):
            obj.__dict__[self.counter_attr] = obj.__dict__.get(self.counter_attr, 0) + 1
            return self.func(obj, *a, **kw)

        wrapper.call_count = obj.__dict__.get(self.counter_attr, 0)
        return wrapper

    @staticmethod
    def count_for(obj, method_name):
        return obj.__dict__.get(f"_calls_{method_name}", 0)


# 5) ValidatedDict
class ValidatedDict:
    ALLOWED = {"host", "port", "user"}

    def __init__(self, **kw):
        object.__setattr__(self, "_data", {})
        for k, v in kw.items():
            setattr(self, k, v)

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"{name!r} set nahi hai") from None

    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
            return
        if name not in self.ALLOWED:
            raise AttributeError(f"{name!r} allowed nahi; {sorted(self.ALLOWED)}")
        self._data[name] = value

    def __delattr__(self, name):
        self._data.pop(name, None)

    def __dir__(self):
        return sorted(set(list(super().__dir__()) + list(self._data)))

    def __repr__(self):
        return f"ValidatedDict({self._data})"


# ---- Tests ----
class Order:
    status = ChoiceField("pending", "shipped", "delivered", "cancelled")
    order_id = ReadOnlyAfterSet()
    name = "Widget Order"
    label = Alias("name")

    def __init__(self, order_id):
        self.order_id = order_id

    @CallCounter
    def ship(self):
        self.status = "shipped"
        return "shipped!"


o = Order("ORD-1")
print("1) default status ->", o.status)
o.status = "shipped"
print("   set ke baad    ->", o.status, "| options:", Order.status.options)
try:
    o.status = "teleported"
except ValueError as e:
    print("   [ok]", e)

print("\\n2) order_id ->", o.order_id)
try:
    o.order_id = "ORD-2"
except AttributeError as e:
    print("   [ok]", e)

print("\\n3) alias label ->", o.label, "(name se aaya)")

print("\\n4) call counts:")
for _ in range(3):
    o.ship()
print("   ship() chali ->", CallCounter.count_for(o, "ship"), "dafa")
o2 = Order("ORD-9")
o2.ship()
print("   naye object par ->", CallCounter.count_for(o2, "ship"), "(per-instance)")

vd = ValidatedDict(host="localhost", port=8080)
print("\\n5)", vd, "| vd.host ->", vd.host)
try:
    vd.hostt = "typo"
except AttributeError as e:
    print("   [ok]", e)
try:
    vd.user
except AttributeError as e:
    print("   [ok]", e)

assert o.status == "shipped" and Order.status.options[0] == "pending"
assert CallCounter.count_for(o, "ship") == 3 and CallCounter.count_for(o2, "ship") == 1
assert o.label == "Widget Order" and vd.port == 8080
print("\\n[pass] saare exercises")
'''),
    md("""
## 19. Interview Q&A (quick)

**Q1. `obj.x` ka lookup order?**
Metaclass path chhor kar: `type(obj).__mro__` me **data descriptor** → `obj.__dict__` →
class attr / **non-data descriptor** → `__getattr__` → `AttributeError`.

**Q2. Data vs non-data descriptor?**
Data = `__set__`/`__delete__` mojood → instance dict se **oopar**. Non-data = sirf `__get__` →
instance dict se **neeche**. `property` data hai, `cached_property`/functions non-data.

**Q3. `cached_property` kaise kaam karti hai?**
Non-data descriptor: pehli dafa compute kar ke result `obj.__dict__[name]` me daal deti hai. Agli
dafa instance dict jeet jata hai → descriptor bilkul chalta hi nahi → zero overhead. Invalidate
karne ke liye dict se key delete karo.

**Q4. Method ko `self` kaun deta hai?**
Function ek non-data descriptor hai. `obj.m` → `function.__get__(obj, type(obj))` → bound method,
jo `obj` ko pehla argument bana deta hai.

**Q5. `__getattr__` vs `__getattribute__`?**
`__getattribute__` har access par (default me poora algorithm); `__getattr__` sirf naakami ke baad.
Override karne ke liye `__getattr__` safe aur sasta.

**Q6. `__set_name__` kyun aaya?**
Ke descriptor ko apna attribute naam automatic mil jaye (pehle manually dena parta tha). Class body
ke bahar attach karne par khud nahi chalta.

**Q7. Descriptor par per-instance data kyun nahi rakh sakte?**
Descriptor object poori class ke liye **ek** hi hai. `obj.__dict__` ya `WeakKeyDictionary` use karo.

**Q8. `property` kab, descriptor class kab?**
Ek attribute ka logic → `property`. Wahi logic **kai** attributes/classes me reuse karna ho
(validation, typed fields, ORM) → descriptor class.

**Q9. `__slots__` descriptors ke sath?**
`__slots__` khud slot descriptors banata hai. Same naam par conflict hota hai → descriptor ke liye
alag storage naam (`_x`) rakho ya weak dict.

**Q10. `__getattr__` me `AttributeError` na raise karein to?**
`hasattr` hamesha `True`, aur `copy`/`pickle` jo `__deepcopy__`/`__reduce__`/`__getstate__` dhoondte
hain, wo galat objects pa kar bizarre errors dete hain.
"""),
    md("""
## 20. Summary & Cheat-sheet

### Lookup order (yaad karo)

```
obj.x:
  1. type(obj).__mro__ me data descriptor?     -> desc.__get__(obj, type(obj))
  2. obj.__dict__["x"]?                        -> wahi value
  3. class attr / non-data descriptor?         -> value ya desc.__get__(...)
  4. type(obj).__getattr__(obj, "x")           -> aakhri mauqa
  5. AttributeError
```

### Descriptor skeleton (copy-paste)

```python
class MyField:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = f"_{name}"
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self                      # class se access
        return obj.__dict__[self.storage]
    def __set__(self, obj, value):
        # validate...
        obj.__dict__[self.storage] = value   # PER-INSTANCE
    def __delete__(self, obj):
        obj.__dict__.pop(self.storage, None)
```

### Faisla table

| Chahiye | Istemal karo |
|---|---|
| Ek computed/validated attribute | `property` |
| Wahi logic kai fields/classes me | descriptor class |
| Mehngi value ek dafa compute | `functools.cached_property` |
| Dynamic/unknown attribute names | `__getattr__` |
| Har assignment intercept | `__setattr__` |
| Binding rokna | `staticmethod` |
| Alternative constructor | `classmethod` |
| Memory + speed, fixed fields | `__slots__` |
| Field collect karna class banne par | `__init_subclass__` (NB2) |

### Dunder cheat-sheet

| Dunder | Trigger |
|---|---|
| `__getattribute__` | har `obj.x` |
| `__getattr__` | `obj.x` fail hone par |
| `__setattr__` | `obj.x = v` |
| `__delattr__` | `del obj.x` |
| `__dir__` | `dir(obj)` |
| `__get__/__set__/__delete__` | descriptor access |
| `__set_name__` | class creation (ek dafa) |

### Aage kya

**NB2 — Metaclasses & Dynamic OOP:** `__init_subclass__` (jo hum ne ORM me use kiya) ki poori
kahani, `type()` se runtime class banana, class creation ka lifecycle, plugin registry, aur "kab
metaclass warranted hai" (mostly nahi).

---

**Is notebook ke topics cover hue:** attribute lookup algorithm ✓ · `__getattribute__` +
recursion trap ✓ · `__getattr__` vs `__getattribute__` ✓ · `__setattr__`/`__delattr__`/`__dir__` ✓ ·
descriptor protocol ✓ · data vs non-data proof ✓ · function→method binding ✓ · `property` scratch se ✓ ·
`classmethod`/`staticmethod` scratch se ✓ · TypedField/RangeField/Positive/NonEmpty/UnitField/
AuditedField/LazyProperty/cached_property ✓ · slots + dataclass interplay ✓ · ORM Model ✓ ·
pitfalls ✓ · performance ✓ · LeetCode 146/155/706/380 ✓
"""),
]

save(PATH, cells)
