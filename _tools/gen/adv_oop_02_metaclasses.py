"""Generator: OOP in Python/Advance/02_Metaclasses_ClassCreation_aur_Dynamic_OOP.ipynb"""
import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

PATH = r"OOP in Python/Advance/02_Metaclasses_ClassCreation_aur_Dynamic_OOP.ipynb"

cells = []

cells += [
    md("""
# 02 — Metaclasses, Class Creation aur Dynamic OOP

**Level:** Advanced OOP · **Series:** OOP in Python → Advance

Python me **class bhi ek object hai**. Aur har object ki koi class hoti hai — to class ki class
kaun hai? Jawab: **metaclass** (default `type`).

Ye notebook do hisson me hai:
1. **Class creation ka poora lifecycle** — metaclass resolve se `__init_subclass__` tak, aur us par
   control kaise lein (metaclass, `__init_subclass__`, class decorator — teen tools, teen levels).
2. **Dynamic OOP toolkit** — runtime par classes banana, inspect karna, patch karna, mixins inject
   karna, plugin + serialization frameworks banana.

## Is notebook me kya seekhenge

- Class = object; `type` ka dohra role (type-checker aur class-factory)
- `type(name, bases, namespace)` se **runtime par class** banana
- Class body kaise chalti hai (execution order + namespace)
- Metaclass ke `__prepare__`, `__new__`, `__init__`, `__call__`
- **Poora lifecycle**: metaclass resolve → `__prepare__` → body exec → `__new__` → `__init__` → `__set_name__` → `__init_subclass__`
- Metaclass use-cases: auto-registry/plugins, interface enforcement, attribute injection, auto `__repr__`, singleton, sealed/final class, naming conventions, abstract enforcement
- **Metaclass conflicts** aur `ABCMeta`
- `__init_subclass__` — aksar metaclass ka behtar aur saada alternative
- **Class decorators** — wahi kaam, aur bhi saada
- Teenon ka comparison table + "kab metaclass warranted hai" (jawab: aksar nahi)
- `__class_getitem__` (generics), `__mro_entries__` ka zikr
- Dynamic toolkit: `getattr`/`setattr`/`hasattr`/`delattr`, `inspect` (signature, isclass, getmembers, getsource), `functools.wraps` on methods
- **Monkey patching** — safe patterns + `unittest.mock.patch`
- Runtime **mixin injection**, `abc.register` se **virtual subclass**
- Mini **plugin framework** + mini **serialization framework** (end-to-end)
- `__reduce__` / `pickle` custom classes ke liye
- `eval`/`exec`/`compile` se class generate karna (aur kyun ye aakhri option hai)
- **LeetCode**: 150, 227, 1396, 933 — registry/dispatch nazariye se

## Prerequisites

- NB1 (descriptors, `__set_name__`) — hum us par build karenge
- Inheritance, MRO, `super()`, ABC ki basic samajh
- Decorators ka concept

> **Warning (pyaar se):** metaclass ek power tool hai. 95% cases me `__init_subclass__` ya class
> decorator kaafi hai. Notebook me hum dono seekhenge **aur** ye faisla karna bhi seekhenge.
"""),
    md("""
## 1. Class bhi ek object hai

**Kya hai:** Python me `class` statement ek **object** banata hai jo memory me rehta hai, jise tum
variable me daal sakte ho, function me pass kar sakte ho, list me rakh sakte ho.

**Kyun ahem hai:** jab class object hai to uska bhi ek type hai (`type`), aur us type ko badla ja
sakta hai (metaclass). Yehi poore notebook ki bunyad hai.
"""),
    code('''
class Dog:
    def speak(self):
        return "Woof"


d = Dog()

print("type(d)      ->", type(d))          # instance ka type = uski class
print("type(Dog)    ->", type(Dog))        # class ka type = type  <-- metaclass
print("type(type)   ->", type(type))       # type khud ka type bhi type hai (loop yahan rukta hai)

# Class ke sath object ki tarah salook karo
Alias = Dog                                 # variable me daal do
print("\\nAlias()      ->", Alias().speak())

classes = [Dog, int, str]                   # list me
print("list me       ->", [c.__name__ for c in classes])

def make(cls):                              # function ko pass
    return cls()
print("function se   ->", type(make(Dog)).__name__)

print("\\nid(Dog)      ->", type(id(Dog)).__name__, "(memory me object hai)")
print("Dog.__name__  ->", Dog.__name__)
print("Dog.__bases__ ->", Dog.__bases__)
print("Dog.__dict__ ke keys ->", [k for k in Dog.__dict__ if not k.startswith("__")])
assert type(Dog) is type and isinstance(Dog, object)
'''),
    md("""
**Output ka matlab:** `type(Dog)` ne `type` diya — yani `Dog` **`type` ka instance** hai. Isi liye
kaha jata hai "classes are instances of their metaclass".

**Interview tip:** `type` ke **do** kaam hain:
1. **1 argument** → us object ka type batao: `type(5)` → `int`
2. **3 arguments** → nayi class **banao**: `type(name, bases, namespace)`

Yehi dohra role log ko confuse karta hai.
"""),
    md("""
## 2. `type(name, bases, ns)` — runtime par class banana

**Syntax:**

```python
NewClass = type(
    "NewClass",              # __name__
    (Base1, Base2),          # __bases__  (tuple; khali tuple => object)
    {"attr": 1, "method": fn},  # namespace (class __dict__)
)
```

**Kahan use hota hai:** ORMs (table se class), API clients (schema se model), test factories,
plugin loaders, `collections.namedtuple` jaisi factories.
"""),
    code('''
# Normal class statement...
class Cat:
    sound = "Meow"

    def speak(self):
        return f"{type(self).__name__} kehta hai {self.sound}"


# ...bilkul isi ka barabar type() se:
def speak(self):
    return f"{type(self).__name__} kehta hai {self.sound}"


CatDynamic = type("CatDynamic", (), {"sound": "Meow", "speak": speak})

print("class statement ->", Cat().speak())
print("type() se       ->", CatDynamic().speak())
print("\\ndono ka type   ->", type(Cat), type(CatDynamic))
print("bases           ->", Cat.__bases__, CatDynamic.__bases__)
assert Cat().speak().replace("Cat", "X") == CatDynamic().speak().replace("CatDynamic", "X")

# Inheritance bhi de sakte hain
Puppy = type("Puppy", (Cat,), {"sound": "Yip"})
print("\\nPuppy MRO ->", [c.__name__ for c in Puppy.__mro__])
print("Puppy      ->", Puppy().speak())
assert issubclass(Puppy, Cat)
'''),
    code('''
# Asli faida: schema (data) se classes generate karna — boilerplate khatam.
SCHEMAS = {
    "User": {"fields": ["id", "email", "name"], "table": "users"},
    "Order": {"fields": ["id", "user_id", "total"], "table": "orders"},
    "Product": {"fields": ["id", "title", "price"], "table": "products"},
}


def make_model(class_name, spec):
    """Ek spec dict se poori class banao — __init__, __repr__, __eq__, sql sab."""
    field_names = spec["fields"]

    def __init__(self, **kw):
        missing = set(field_names) - set(kw)
        if missing:
            raise TypeError(f"{class_name}: ye fields chahiye: {sorted(missing)}")
        extra = set(kw) - set(field_names)
        if extra:
            raise TypeError(f"{class_name}: unknown fields: {sorted(extra)}")
        for k, v in kw.items():
            setattr(self, k, v)

    def __repr__(self):
        inner = ", ".join(f"{f}={getattr(self, f)!r}" for f in field_names)
        return f"{class_name}({inner})"

    def __eq__(self, other):
        return type(self) is type(other) and all(
            getattr(self, f) == getattr(other, f) for f in field_names
        )

    def to_dict(self):
        return {f: getattr(self, f) for f in field_names}

    @classmethod
    def select_sql(cls):
        return f"SELECT {', '.join(field_names)} FROM {spec['table']};"

    namespace = {
        "__init__": __init__,
        "__repr__": __repr__,
        "__eq__": __eq__,
        "__doc__": f"Auto-generated model for table {spec['table']!r}.",
        "__slots__": tuple(field_names),        # memory bhi bachao
        "_fields": tuple(field_names),
        "_table": spec["table"],
        "to_dict": to_dict,
        "select_sql": select_sql,
    }
    return type(class_name, (), namespace)


# Sab classes ek loop me ban gayi
models = {name: make_model(name, spec) for name, spec in SCHEMAS.items()}
globals().update(models)                     # module namespace me daal do

u = models["User"](id=1, email="a@b.c", name="Ali")
o = models["Order"](id=7, user_id=1, total=999)
print(u)
print(o)
print("\\nSQL:", models["User"].select_sql())
print("     ", models["Product"].select_sql())
print("\\nto_dict ->", u.to_dict())
print("equality ->", u == models["User"](id=1, email="a@b.c", name="Ali"))
print("docstring ->", models["Order"].__doc__)
print("__slots__ ka faida: __dict__ hai? ->", hasattr(u, "__dict__"))

try:
    models["User"](id=2)
except TypeError as e:
    print("\\nmissing fields ->", e)
try:
    models["User"](id=2, email="x", name="y", nickname="z")
except TypeError as e:
    print("unknown field  ->", e)
assert u == models["User"](id=1, email="a@b.c", name="Ali")
'''),
    md("""
## 3. Class body kaise chalti hai?

**Kya hota hai:** `class` statement chalte waqt Python:
1. Body ko ek **naye namespace** (dict jaisa) me **normal code ki tarah** chalata hai (top se
   neeche).
2. Us namespace ko metaclass ko de deta hai class banane ke liye.

Yani class body **ek block of code hai jo foran chalta hai** — koi "declaration only" cheez nahi.
Isi liye us me `print`, `if`, loops, sab chal sakta hai.

**Gotcha:** class body ka scope **function scope nahi** hai — comprehensions ke andar class-level
naam nazar nahi aate (mashhoor `NameError`).
"""),
    code('''
print("class body chalne se PEHLE")

class Demo:
    print("  1. body shuru")
    x = 10
    print("  2. x set hua:", x)

    if x > 5:                          # normal control flow chalta hai
        y = "bara"
    else:
        y = "chhota"
    print("  3. y =", y)

    for i in range(2):                 # loop bhi
        print(f"  4. loop i={i}")

    def method(self):                  # function def bhi ek assignment hai
        return "method chali"
    print("  5. method define hui:", method)

    # locals() = zer-e-tameer namespace
    print("  6. ab tak namespace:", [k for k in locals() if not k.startswith("__")])

print("class body ke BAAD — ab class object mojood hai:", Demo)
print("Demo.__dict__ me ->", [k for k in Demo.__dict__ if not k.startswith("__")])
print("i bhi class attribute ban gaya! ->", Demo.i, "(loop variable leak)")
assert Demo.x == 10 and Demo.y == "bara" and Demo.i == 1
'''),
    code('''
# Gotcha: class body ka scope comprehension ke andar visible nahi hota.
try:
    class Broken:
        size = 3
        # comprehension apna naya function-scope banata hai -> class scope skip
        values = [size * i for i in range(3)]
except NameError as e:
    print("NameError ->", e)
    print("Wajah: comprehension ka implicit function class-scope ko dekh nahi sakta.")

# Hal 1: default argument / closure se value andar bhejo
class Fixed1:
    size = 3
    values = [s * i for s in (size,) for i in range(3)]   # size ko iterable me pehle evaluate kiya

# Hal 2: module-level constant ya staticmethod
SIZE = 3
class Fixed2:
    size = SIZE
    values = [SIZE * i for i in range(3)]

# Hal 3: sab se saaf — __init__ me karo
class Fixed3:
    size = 3
    def __init__(self):
        self.values = [self.size * i for i in range(3)]

print("\\nFixed1.values ->", Fixed1.values)
print("Fixed2.values ->", Fixed2.values)
print("Fixed3().values ->", Fixed3().values)
assert Fixed1.values == Fixed2.values == Fixed3().values == [0, 3, 6]

# Note: comprehension ka FIRST iterable class scope me evaluate hota hai (isi liye Hal 1 chala)
'''),
]

cells += [
    md("""
## 4. Metaclass ke hooks: `__prepare__`, `__new__`, `__init__`, `__call__`

**Kya hai:** metaclass wo class hai jiska **instance** ek class hoti hai. `type` se inherit karo:

```python
class Meta(type):
    @classmethod
    def __prepare__(mcls, name, bases, **kw):   # namespace object do (body isi me chalega)
        return {}
    def __new__(mcls, name, bases, ns, **kw):   # CLASS banao (yahan namespace badla ja sakta hai)
        return super().__new__(mcls, name, bases, ns)
    def __init__(cls, name, bases, ns, **kw):   # bani hui CLASS ko configure karo
        super().__init__(name, bases, ns)
    def __call__(cls, *a, **kw):                # jab class ko BULAYA jaye (instance banana)
        return super().__call__(*a, **kw)

class MyClass(metaclass=Meta):
    ...
```

**Yaad rakho:**
- `__new__`/`__init__` **class banate waqt ek dafa** chalte hain.
- `__call__` **har instance** banate waqt chalta hai (`MyClass()`).
- `mcls` = metaclass, `cls` = bani hui class.
"""),
    code('''
class VerboseMeta(type):
    """Har hook par print karta hai — lifecycle dekhne ke liye."""

    @classmethod
    def __prepare__(mcls, name, bases, **kwargs):
        print(f"  [1] __prepare__  name={name} bases={[b.__name__ for b in bases]} kwargs={kwargs}")
        return {}                              # yahi dict class body ka namespace banega

    def __new__(mcls, name, bases, ns, **kwargs):
        print(f"  [3] __new__      namespace keys={[k for k in ns if not k.startswith('__')]}")
        cls = super().__new__(mcls, name, bases, ns)   # asli class yahan banti hai
        print(f"      class ban gayi: {cls}")
        return cls

    def __init__(cls, name, bases, ns, **kwargs):
        print(f"  [4] __init__     cls={cls.__name__} (configure karne ka mauqa)")
        super().__init__(name, bases, ns)

    def __call__(cls, *args, **kwargs):
        print(f"  [5] __call__     {cls.__name__}{args} -> instance banega")
        instance = super().__call__(*args, **kwargs)    # cls.__new__ + cls.__init__
        print(f"      instance tayyar: {instance}")
        return instance


print("=== class define ho rahi hai ===")

class Service(metaclass=VerboseMeta, region="asia"):     # extra kwargs metaclass ko jate hain
    print("  [2] class body chal rahi hai")
    version = 1

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Service({self.name!r})"


print("\\n=== ab instance banate hain ===")
s = Service("auth")
print("\\n=== doosra instance ===")
s2 = Service("billing")
print("\\nfinal:", s, s2, "| type(Service) ->", type(Service).__name__)
assert type(Service) is VerboseMeta and isinstance(s, Service)
'''),
    md("""
**Output ka matlab (tarteeb ghor se dekho):**

```
1. __prepare__  -> namespace mila
2. class body   -> usi namespace me chali
3. __new__      -> namespace se class bani
4. __init__     -> class configure hui
--- (class ready) ---
5. __call__     -> har instance par
```

**Interview tip:** "`Meta.__new__` aur `Meta.__init__` me farq?" → `__new__` ke paas abhi **namespace
dict** hai, yani tum class ke members **badal/add/reject** kar sakte ho **class banne se pehle**.
`__init__` ke paas **ban chuki class** hai — sirf uske attributes set kar sakte ho. Namespace
manipulate karna ho → `__new__`; registration/side-effects → `__init__`.
"""),
    code('''
# __prepare__ ka asal faida: ordered/custom namespace. Duplicate names pakro.
class NoDuplicatesDict(dict):
    """Class body me same naam do dafa? foran error."""

    def __setitem__(self, key, value):
        if key in self and not key.startswith("__"):
            raise TypeError(f"'{key}' class body me do dafa define hua — shayad copy-paste bug hai")
        super().__setitem__(key, value)


class StrictMeta(type):
    @classmethod
    def __prepare__(mcls, name, bases, **kw):
        return NoDuplicatesDict()             # normal dict ki jagah apna dict

    def __new__(mcls, name, bases, ns, **kw):
        return super().__new__(mcls, name, bases, dict(ns))   # type() ko asli dict do


# Theek class
class Ok(metaclass=StrictMeta):
    def alpha(self): return 1
    def beta(self): return 2

print("Ok class bani ->", Ok().alpha(), Ok().beta())

# Duplicate method (asli bug jo chup chaap pehli definition kha jata hai)
src = (
    "class Oops(metaclass=StrictMeta):\\n"
    "    def handler(self): return 'pehla'\\n"
    "    def handler(self): return 'doosra'\\n"
)
try:
    exec(src)
except TypeError as e:
    print("duplicate pakra gaya ->", e)

# Normal Python me ye chup chaap chalta hai (khatarnaak)
class Silent:
    def handler(self): return "pehla"
    def handler(self): return "doosra"      # noqa: F811 — pehla gayab ho gaya
print("\\nnormal class me   ->", Silent().handler(), "(pehla chup chaap chala gaya)")
'''),
    code('''
# __prepare__ #2: definition order yaad rakho (fields ki tarteeb ahem ho, jaise forms/serializers)
class OrderTrackingMeta(type):
    @classmethod
    def __prepare__(mcls, name, bases, **kw):
        return {}                              # Python 3.7+ dict already ordered hai

    def __new__(mcls, name, bases, ns, **kw):
        cls = super().__new__(mcls, name, bases, ns)
        # definition order me public names save karo
        cls._definition_order = tuple(
            k for k in ns if not k.startswith("_")
        )
        return cls


class Form(metaclass=OrderTrackingMeta):
    email = "email input"
    password = "password input"
    remember_me = "checkbox"

    def render(self):
        return " | ".join(f"<{name}>" for name in self._definition_order if name != "render")


f = Form()
print("definition order ->", Form._definition_order)
print("rendered form    ->", f.render())
assert Form._definition_order[:3] == ("email", "password", "remember_me")
print("\\nFaida: alphabetical nahi, LIKHNE ki tarteeb mili — forms/serializers ke liye zaroori.")
'''),
    md("""
## 5. Class creation ka poora lifecycle (ek nazar me)

```
class C(Base, metaclass=Meta, **kwds):
    <body>

STEP 1  metaclass resolve:
        explicit `metaclass=` diya? warna bases ke metaclasses me se sab se DERIVED chuno
        (agar aapas me incompatible hon -> TypeError: metaclass conflict)
STEP 2  ns = Meta.__prepare__(name, bases, **kwds)          # custom namespace
STEP 3  class body ko `ns` me execute karo (top se neeche)
STEP 4  cls = Meta.__new__(Meta, name, bases, ns, **kwds)   # class object bana
STEP 5      andar type.__new__ ye karta hai:
              - __set_name__(owner, name) har descriptor par        <- NB1 ka hook
              - __init_subclass__(cls=naya) parent par bulao        <- implicit classmethod
STEP 6  Meta.__init__(cls, name, bases, ns, **kwds)         # class configure
STEP 7  class decorators (@deco) neeche se oopar apply hote hain
        naam `C` bind hota hai
--- class tayyar ---
LATER   C(...)  ->  Meta.__call__(C, ...)  ->  C.__new__  ->  C.__init__
```

Chalo isay **print kar kar** saabit karein.
"""),
    code('''
# Poora lifecycle ek hi example me — har step apna naam print karega.
events = []

class TraceDescriptor:
    def __set_name__(self, owner, name):
        events.append(f"5a. __set_name__({owner.__name__}.{name})")
    def __get__(self, obj, objtype=None):
        return "desc-value"


class LifecycleMeta(type):
    @classmethod
    def __prepare__(mcls, name, bases, **kw):
        events.append("2. Meta.__prepare__")
        return {}

    def __new__(mcls, name, bases, ns, **kw):
        events.append("4. Meta.__new__ (namespace mojood, class abhi nahi)")
        cls = super().__new__(mcls, name, bases, ns)
        events.append("5c. type.__new__ mukammal (set_name + init_subclass ho gaye)")
        return cls

    def __init__(cls, name, bases, ns, **kw):
        events.append("6. Meta.__init__ (class tayyar, configure kar sakte hain)")
        super().__init__(name, bases, ns)


class Base(metaclass=LifecycleMeta):
    def __init_subclass__(cls, **kw):
        events.append(f"5b. Base.__init_subclass__(cls={cls.__name__})")
        super().__init_subclass__(**kw)


def class_decorator(cls):
    events.append("7. class decorator")
    return cls


events.clear()
events.append("1. metaclass resolve (bases se LifecycleMeta mila)")

@class_decorator
class Child(Base):
    events.append("3. class body execute")
    marker = TraceDescriptor()


creation = list(events)
print("--- CLASS CREATION ---")
for e in creation:
    print("  ", e)

child = Child()
print("\\n--- INSTANCE CREATION ---")
print("   Meta.__call__ -> Child.__new__ -> Child.__init__")
print("   marker ->", child.marker)

# Tarteeb verify karo: prepare < body < new < set_name < init_subclass < init
def idx(prefix):
    return next(i for i, e in enumerate(creation) if e.startswith(prefix))

assert idx("2.") < idx("3.") < idx("4.") < idx("5a.") < idx("5b.") < idx("6.")
print("\\nTarteeb verified:", " -> ".join(e.split(" ")[0] for e in creation))
print("\\nAhem: __set_name__ aur __init_subclass__ dono type.__new__ ke ANDAR chalte hain,")
print("      yani Meta.__new__ ke super() call ke doran — Meta.__init__ se PEHLE.")
'''),
    code('''
# Sab se ahem lifecycle sabaq: __init_subclass__ ko PARENT par likho, chalega SUBCLASS ke liye.
class Plugin:
    registry = {}

    def __init_subclass__(cls, key=None, **kw):
        # ye implicitly classmethod hai — @classmethod likhne ki zaroorat nahi
        super().__init_subclass__(**kw)
        name = key or cls.__name__.lower()
        if name in Plugin.registry:
            raise ValueError(f"plugin key {name!r} pehle se mojood hai")
        Plugin.registry[name] = cls
        cls.key = name

    def run(self, data):
        raise NotImplementedError


class CsvPlugin(Plugin):                      # key=None -> "csvplugin"
    def run(self, data):
        return ",".join(map(str, data))


class JsonPlugin(Plugin, key="json"):         # class kwargs -> __init_subclass__ ko
    def run(self, data):
        import json
        return json.dumps(data)


class UpperPlugin(Plugin, key="upper"):
    def run(self, data):
        return [str(x).upper() for x in data]


print("registry ->", {k: v.__name__ for k, v in Plugin.registry.items()})
data = ["ali", "sara", "bilal"]
for key, cls in Plugin.registry.items():
    print(f"  {key:12} -> {cls().run(data)}")

# Duplicate key par error
try:
    class Dup(Plugin, key="json"):
        pass
except ValueError as e:
    print("\\nduplicate key ->", e)

assert set(Plugin.registry) == {"csvplugin", "json", "upper"}
assert Plugin.registry["json"] is JsonPlugin and JsonPlugin.key == "json"
print("\\nNote: yehi registry hum metaclass se bhi bana sakte the — magar __init_subclass__ saada hai.")
'''),
]

cells += [
    md("""
## 6. Metaclass use-cases (8 asli patterns)

Ab ek ek pattern dekhte hain. Har ek ke sath hum ye bhi likhenge ke **kya isay `__init_subclass__`
ya decorator se karna behtar tha?**

| # | Pattern | Metaclass zaroori? |
|---|---|---|
| 1 | Auto-registry / plugins | Nahi — `__init_subclass__` behtar |
| 2 | Interface enforcement | Nahi — `__init_subclass__` ya ABC |
| 3 | Attribute injection | Nahi — decorator behtar |
| 4 | Auto `__repr__` | Nahi — decorator/dataclass |
| 5 | Singleton | **Haan** — `__call__` intercept sirf metaclass kar sakta hai |
| 6 | Sealed / final class | Nahi — `__init_subclass__` se ho jata hai |
| 7 | Naming conventions | Nahi — `__init_subclass__` |
| 8 | Abstract enforcement | `ABCMeta` (jo khud ek metaclass hai) |

Yani asli faisla-kun cheez: **kya tumhein class-creation ke namespace ya class ke `__call__` par
control chahiye?** Agar nahi, to metaclass mat likho.
"""),
    code('''
# Pattern 1 & 2: registry + interface enforcement (metaclass version)
class HandlerMeta(type):
    """Sab handlers ko register karo aur required methods force karo."""

    REQUIRED = {"handle", "can_handle"}
    registry = {}

    def __new__(mcls, name, bases, ns, **kw):
        cls = super().__new__(mcls, name, bases, ns, **kw)
        if bases:                                       # base class khud ko chhor do
            missing = mcls.REQUIRED - set(dir(cls))
            if missing:
                raise TypeError(
                    f"{name} me ye methods lazmi hain: {sorted(missing)}"
                )
            # signature bhi check karo (interface = naam + shape)
            import inspect
            sig = inspect.signature(cls.handle)
            if list(sig.parameters) != ["self", "request"]:
                raise TypeError(
                    f"{name}.handle(self, request) hona chahiye, mila {sig}"
                )
            mcls.registry[name] = cls
        return cls


class BaseHandler(metaclass=HandlerMeta):
    pass


class AuthHandler(BaseHandler):
    def can_handle(self, request):
        return request.get("path", "").startswith("/auth")

    def handle(self, request):
        return {"status": 200, "body": "authenticated"}


class ApiHandler(BaseHandler):
    def can_handle(self, request):
        return request.get("path", "").startswith("/api")

    def handle(self, request):
        return {"status": 200, "body": "api data"}


print("registry ->", list(HandlerMeta.registry))

# Router jo registry use karta hai (koi if-else chain nahi)
def route(request):
    for cls in HandlerMeta.registry.values():
        handler = cls()
        if handler.can_handle(request):
            return handler.handle(request)
    return {"status": 404, "body": "not found"}


for path in ["/auth/login", "/api/users", "/unknown"]:
    print(f"  {path:14} ->", route({"path": path}))

# Interface violations
print("\\n--- enforcement tests ---")
bad_defs = [
    ("method missing", "class NoHandle(BaseHandler):\\n    def can_handle(self, r): return True\\n"),
    ("galat signature", "class BadSig(BaseHandler):\\n"
                        "    def can_handle(self, r): return True\\n"
                        "    def handle(self, r, extra): return {}\\n"),
]
for why, src in bad_defs:
    try:
        exec(src, globals())
        print(f"[FAIL] {why} pass ho gaya")
    except TypeError as e:
        print(f"[ok] {why:16} -> {e}")

assert set(HandlerMeta.registry) == {"AuthHandler", "ApiHandler"}
assert route({"path": "/api/x"})["body"] == "api data"
'''),
    code('''
# Pattern 3 & 4: attribute injection + auto __repr__ (metaclass version)
class AutoMeta(type):
    """Har class me created_at, __repr__, aur field list inject karo."""

    def __new__(mcls, name, bases, ns, **kw):
        # 1) Auto __repr__ agar user ne khud nahi diya
        if "__repr__" not in ns:
            def __repr__(self):
                items = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
                return f"{type(self).__name__}({items})"
            ns["__repr__"] = __repr__

        # 2) Metadata inject karo
        ns["_created_by"] = "AutoMeta"
        ns["_annotated_fields"] = tuple(ns.get("__annotations__", {}))

        # 3) Auto __eq__
        if "__eq__" not in ns:
            def __eq__(self, other):
                return type(self) is type(other) and vars(self) == vars(other)
            ns["__eq__"] = __eq__
            ns["__hash__"] = None            # eq define karo to hash explicit karo

        return super().__new__(mcls, name, bases, ns, **kw)


class Book(metaclass=AutoMeta):
    title: str
    pages: int

    def __init__(self, title, pages):
        self.title, self.pages = title, pages


class Magazine(metaclass=AutoMeta):
    def __init__(self, name):
        self.name = name

    def __repr__(self):                      # apna repr -> inject nahi hoga
        return f"<Magazine {self.name}>"


b = Book("Clean Code", 464)
print("auto repr    ->", b)
print("apna repr    ->", Magazine("Wired"))
print("injected     ->", Book._created_by, "| fields:", Book._annotated_fields)
print("auto eq      ->", b == Book("Clean Code", 464), "|", b == Book("Other", 1))
assert repr(b) == "Book(title='Clean Code', pages=464)"
assert Book._annotated_fields == ("title", "pages")
print("\\nSach: ye dataclass/decorator se bhi hota — metaclass zaroori nahi tha.")
'''),
    code('''
# Pattern 5: SINGLETON — yahan metaclass ASAL me faida deta hai (__call__ intercept)
import threading

class SingletonMeta(type):
    """Class ko bulane par hamesha wahi ek instance — thread-safe."""

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # double-checked locking: fast path bina lock
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:            # dobara check (race condition)
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def reset(cls):
        """Testing ke liye — singleton ko bhula do."""
        with cls._lock:
            cls._instances.pop(cls, None)


class Database(metaclass=SingletonMeta):
    def __init__(self, dsn="postgres://localhost/app"):
        print(f"  (mehngi connection ban rahi hai: {dsn})")
        self.dsn = dsn
        self.queries = 0

    def query(self, sql):
        self.queries += 1
        return f"result of {sql!r}"


class Cache(metaclass=SingletonMeta):
    def __init__(self):
        self.store = {}


print("pehli dafa:")
db1 = Database()
print("doosri dafa (koi print nahi hona chahiye):")
db2 = Database("ye-dsn-ignore-hoga")
print("\\ndb1 is db2 ->", db1 is db2)
print("dsn        ->", db2.dsn, "(pehla hi rehta hai)")

db1.query("SELECT 1")
db2.query("SELECT 2")
print("shared state -> queries:", db1.queries)

# Har class ka apna singleton
c1, c2 = Cache(), Cache()
print("\\nCache singleton ->", c1 is c2, "| Database se alag ->", c1 is not db1)

# Threads me bhi ek hi instance
Database.reset()
found = []
def worker():
    found.append(Database("threaded"))

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
print("\\n10 threads ne banaye:", len(set(map(id, found))), "unique instance(s)")
assert len(set(map(id, found))) == 1
assert db1 is db2 and c1 is c2
print("\\nYAHAN metaclass warranted hai: __call__ ko koi decorator itni safai se intercept nahi karta.")
'''),
    code('''
# Pattern 5b: Singleton ke aur tareeqe (trade-offs samajh lo)
# (a) module-level instance — Python ka sab se idiomatic "singleton"
class _Settings:
    def __init__(self):
        self.theme = "dark"

settings = _Settings()          # module import ek dafa hota hai => ek instance

# (b) __new__ override — saada magar __init__ dobara chalta hai (gotcha!)
class NewSingleton:
    _self = None
    def __new__(cls, *a, **kw):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self
    def __init__(self, value=0):
        print(f"  __init__ phir chala! value={value}")
        self.value = value

print("(b) __new__ tareeqa:")
n1 = NewSingleton(1)
n2 = NewSingleton(2)
print("  same object?", n1 is n2, "| value:", n1.value, "<- overwrite ho gayi (BUG)")

# (c) decorator se singleton — saada, magar class 'function' ban jati hai
def singleton(cls):
    instances = {}
    def get(*a, **kw):
        if cls not in instances:
            instances[cls] = cls(*a, **kw)
        return instances[cls]
    return get

@singleton
class Logger:
    def __init__(self):
        self.lines = []

print("\\n(c) decorator tareeqa:")
l1, l2 = Logger(), Logger()
print("  same object?", l1 is l2)
print("  magar isinstance check tootta hai ->", type(Logger).__name__, "(class nahi, function hai)")

print("\\nFaisla: config ke liye (a) module-level; asli singleton semantics chahiye to metaclass.")
assert n1 is n2 and l1 is l2
'''),
    code('''
# Pattern 6 & 7: final/sealed class + naming conventions
class FinalMeta(type):
    """final=True wali class se inherit karna mana."""

    def __new__(mcls, name, bases, ns, final=False, **kw):
        for base in bases:
            if getattr(base, "_is_final", False):
                raise TypeError(f"{base.__name__} final hai; {name} isay extend nahi kar sakti")
        cls = super().__new__(mcls, name, bases, ns, **kw)
        cls._is_final = final
        return cls


class Money(metaclass=FinalMeta, final=True):
    def __init__(self, amount):
        self.amount = amount


class Currency(metaclass=FinalMeta):          # final nahi -> extend ho sakti hai
    symbol = "?"


class Rupee(Currency):
    symbol = "Rs"


print("Money final? ->", Money._is_final, "| Currency final? ->", Currency._is_final)
print("Rupee bani   ->", Rupee.symbol)
try:
    class Dollar(Money):
        pass
except TypeError as e:
    print("final violation ->", e)


# Naming conventions enforce karo
class NamingMeta(type):
    def __new__(mcls, name, bases, ns, **kw):
        if not name[0].isupper():
            raise TypeError(f"class ka naam PascalCase ho: {name!r}")
        problems = []
        for attr, val in ns.items():
            if attr.startswith("__"):
                continue
            if callable(val) and attr != attr.lower():
                problems.append(f"method {attr!r} snake_case ho")
            if not callable(val) and not isinstance(val, (staticmethod, classmethod, property)):
                if attr.isupper() is False and attr != attr.lower():
                    problems.append(f"attribute {attr!r} snake_case ya UPPER_CASE ho")
        if problems:
            raise TypeError(f"{name}: " + "; ".join(problems))
        return super().__new__(mcls, name, bases, ns, **kw)


class GoodStyle(metaclass=NamingMeta):
    MAX_SIZE = 100
    default_name = "x"
    def do_work(self): return "ok"

print("\\nGoodStyle ->", GoodStyle().do_work())
for why, src in [
    ("lowercase class", "class badName(metaclass=NamingMeta): pass"),
    ("camelCase method", "class Styled(metaclass=NamingMeta):\\n    def doWork(self): return 1\\n"),
]:
    try:
        exec(src, globals())
    except TypeError as e:
        print(f"[ok] {why:17} -> {e}")

assert Money._is_final and Rupee.symbol == "Rs"
'''),
    md("""
## 7. Metaclass conflicts aur `ABCMeta`

**Masla:** ek class ke do bases ke **do mukhtalif** metaclasses hon, aur wo aapas me
parent-child na hon → `TypeError: metaclass conflict`.

**Niyam:** chuni gayi metaclass ko **sab** bases ki metaclasses ka **subclass** hona chahiye.

**Sab se aam scenario:** tum `ABC` (metaclass `ABCMeta`) aur apna metaclass mila rahe ho.
**Hal:** apni metaclass ko `ABCMeta` se inherit karao:

```python
class MyMeta(ABCMeta):   # <- type ki jagah ABCMeta
    ...
```
"""),
    code('''
from abc import ABC, ABCMeta, abstractmethod

class MetaA(type):
    pass

class MetaB(type):
    pass

class A(metaclass=MetaA):
    pass

class B(metaclass=MetaB):
    pass

# Conflict: MetaA aur MetaB me koi rishta nahi
try:
    class AB(A, B):
        pass
except TypeError as e:
    print("conflict ->", e)

# Hal: ek combined metaclass jo dono se inherit kare
class MetaAB(MetaA, MetaB):
    pass

class AB(A, B, metaclass=MetaAB):
    pass

print("hal ke baad ->", AB, "| type:", type(AB).__name__)
print("MRO         ->", [c.__name__ for c in AB.__mro__])
assert issubclass(type(AB), MetaA) and issubclass(type(AB), MetaB)
'''),
    code('''
# ABC + custom metaclass ka asli scenario
class RegistryMeta(type):
    registry = {}
    def __new__(mcls, name, bases, ns, **kw):
        cls = super().__new__(mcls, name, bases, ns, **kw)
        if bases:
            mcls.registry[name] = cls
        return cls


# Koshish: ABC ke sath mila do -> conflict
try:
    class Shape(ABC, metaclass=RegistryMeta):
        @abstractmethod
        def area(self): ...
except TypeError as e:
    print("ABC + custom meta ->", e)

# HAL: metaclass ko ABCMeta se inherit karao
class RegistryABCMeta(ABCMeta):
    registry = {}
    def __new__(mcls, name, bases, ns, **kw):
        cls = super().__new__(mcls, name, bases, ns, **kw)
        # sirf concrete (non-abstract) classes register karo
        if bases and not getattr(cls, "__abstractmethods__", None):
            mcls.registry[cls.__name__.lower()] = cls
        return cls


class Shape(metaclass=RegistryABCMeta):
    @abstractmethod
    def area(self): ...

    def describe(self):
        return f"{type(self).__name__} ka area {self.area():.2f} hai"


class Square(Shape):
    def __init__(self, side): self.side = side
    def area(self): return self.side ** 2


class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159 * self.r ** 2


class Incomplete(Shape):          # area implement nahi kiya -> abstract raha
    pass


print("\\nregistry (sirf concrete) ->", list(RegistryABCMeta.registry))
for name, cls in RegistryABCMeta.registry.items():
    print("  ", cls(3).describe())

try:
    Incomplete()
except TypeError as e:
    print("\\nabstract instantiate ->", e)

print("Incomplete ke abstract methods ->", Incomplete.__abstractmethods__)
assert set(RegistryABCMeta.registry) == {"square", "circle"}
assert "area" in Incomplete.__abstractmethods__
'''),
    code('''
# Pattern 8: abstract enforcement — ABCMeta ke baghair (khud ka version) vs ABC
# (a) Khud ka: __init_subclass__ se check
class Interface:
    _required = ()

    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        missing = [m for m in cls._required if not callable(getattr(cls, m, None))]
        if missing and not getattr(cls, "_abstract", False):
            raise TypeError(f"{cls.__name__} me ye implement karo: {missing}")


class Repository(Interface):
    _required = ("save", "find")
    _abstract = True                       # ye khud base hai


class SqlRepository(Repository):
    def save(self, obj): return f"saved {obj} to SQL"
    def find(self, id_): return f"found {id_} in SQL"


print("(a) khud ka enforcement ->", SqlRepository().save("user"))
try:
    class BrokenRepo(Repository):
        def save(self, obj): return "x"
except TypeError as e:
    print("    [ok]", e)

# (b) ABC tareeqa (standard, aur tooling/IDE ise samajhti hai)
class RepositoryABC(ABC):
    @abstractmethod
    def save(self, obj): ...
    @abstractmethod
    def find(self, id_): ...
    def save_many(self, objs):             # concrete helper abstract class me bhi de sakte ho
        return [self.save(o) for o in objs]


class MemoryRepo(RepositoryABC):
    def __init__(self): self._data = {}
    def save(self, obj):
        self._data[obj["id"]] = obj
        return obj["id"]
    def find(self, id_): return self._data.get(id_)


r = MemoryRepo()
print("\\n(b) ABC tareeqa ->", r.save_many([{"id": 1}, {"id": 2}]))
print("    find(1) ->", r.find(1))
assert r.find(2) == {"id": 2}
print("\\nFarq: khud ka check CLASS banate waqt fail hota hai (fail-fast),")
print("      ABC INSTANTIATE karte waqt (aur typing tools ise samajhti hain).")
'''),
]

cells += [
    md("""
## 8. `__init_subclass__` — aksar metaclass ka behtar alternative (PEP 487)

**Kya hai:** parent class par define karo; **har subclass** banne par khud chal jata hai. Ye
**implicitly `classmethod`** hai (decorator likhne ki zaroorat nahi, magar likhna galat bhi nahi).

**Kyun behtar:**
- Metaclass conflicts ka masla **khatam** (koi nayi metaclass nahi)
- Parhne me aasan; naye developers samajh jate hain
- Class keyword arguments support karta hai: `class C(Base, key="x")`

**Kya nahi kar sakta:**
- Namespace ko **banne se pehle** nahi badal sakta (`__prepare__` nahi)
- Instance creation (`Class()`) intercept nahi kar sakta (`__call__` nahi)
- Class ka `__name__`/`bases` badal nahi sakta

**Syntax:**

```python
class Base:
    def __init_subclass__(cls, /, my_option=None, **kwargs):
        super().__init_subclass__(**kwargs)     # LAZMI: chain ko na toro
        ...
```
"""),
    code('''
# Poora feature-set: options, validation, injection, registry — sab __init_subclass__ se
class Component:
    """Base jo subclasses ko configure, validate aur register karta hai."""

    _registry = {}
    _required_methods = ("render",)

    def __init_subclass__(cls, /, name=None, tag="div", cache=False, abstract=False, **kwargs):
        super().__init_subclass__(**kwargs)     # cooperative — chain na toro

        cls._abstract = abstract
        if abstract:
            return                              # abstract base par validation/registration nahi

        # 1) Validation
        missing = [m for m in cls._required_methods if not callable(getattr(cls, m, None))]
        if missing:
            raise TypeError(f"{cls.__name__} me ye methods chahiye: {missing}")

        # 2) Attribute injection (class kwargs se)
        cls.component_name = name or cls.__name__.lower()
        cls.tag = tag
        cls.cache_enabled = cache

        # 3) Registry
        Component._registry[cls.component_name] = cls

    @classmethod
    def registry(cls):
        return dict(cls._registry)

    def html(self):
        return f"<{self.tag}>{self.render()}</{self.tag}>"


class Layout(Component, abstract=True):         # abstract base — register nahi hoga
    pass


class Button(Component, tag="button", cache=True):
    def render(self):
        return "Click me"


class Card(Layout, name="card-widget", tag="section"):
    def render(self):
        return "Card content"


class Header(Layout):
    def render(self):
        return "Site header"


print("registry ->", {k: v.__name__ for k, v in Component.registry().items()})
for key, cls in Component.registry().items():
    inst = cls()
    print(f"  {key:14} cache={str(cls.cache_enabled):5} -> {inst.html()}")

try:
    class Broken(Component):
        pass                                     # render nahi hai
except TypeError as e:
    print("\\nvalidation ->", e)

print("\\nkoi metaclass define nahi ki ->", type(Button).__name__)
assert type(Button) is type
assert set(Component.registry()) == {"button", "card-widget", "header"}
assert Card.tag == "section" and Header.tag == "div"
'''),
    code('''
# Gotcha 1: super().__init_subclass__(**kwargs) na bulane se chain toot jati hai.
class MixinA:
    def __init_subclass__(cls, **kw):
        cls.from_a = True
        super().__init_subclass__(**kw)          # sahi: chain aage bhejo


class MixinB:
    def __init_subclass__(cls, **kw):
        cls.from_b = True
        # GALAT: super() call gayab -> MixinA ka hook kabhi nahi chalega


class GoodChild(MixinA, MixinB):                 # MRO: GoodChild -> MixinA -> MixinB
    pass

class BadChild(MixinB, MixinA):                  # MixinB pehle -> chain wahin ruk gayi
    pass

print("GoodChild -> from_a:", getattr(GoodChild, "from_a", False),
      "| from_b:", getattr(GoodChild, "from_b", False))
print("BadChild  -> from_a:", getattr(BadChild, "from_a", False),
      "| from_b:", getattr(BadChild, "from_b", False), " <- MixinA skip ho gaya")
assert getattr(BadChild, "from_a", False) is False
print("\\nSabaq: __init_subclass__ me HAMESHA super().__init_subclass__(**kwargs) bulao.")


# Gotcha 2: base class KHUD ke liye hook nahi chalta (sirf subclasses ke liye)
calls = []
class Root:
    def __init_subclass__(cls, **kw):
        calls.append(cls.__name__)
        super().__init_subclass__(**kw)

class Level1(Root): pass
class Level2(Level1): pass                        # ye bhi trigger karta hai (Root ka hook)

print("\\nhook kin classes par chala ->", calls)
assert calls == ["Level1", "Level2"] and "Root" not in calls
'''),
    md("""
## 9. Class decorators — wahi kaam, aur bhi saada

**Kya hai:** ek function jo **class** leta hai aur class (ya kuch aur) wapis karta hai.

```python
def deco(cls):
    cls.extra = 1
    return cls

@deco
class C: ...
```

**Faide:**
- Sab se saada mental model — bas ek function
- **Compose** ho jate hain: kai decorators ek class par
- Inheritance ko affect nahi karte (subclasses ko **automatically nahi** milte — ye faida bhi hai
  aur nuqsan bhi)

**Nuqsan:**
- Class body chal chuki hoti hai (namespace pre-processing nahi)
- Har class par **manually** lagana parta hai (bhool sakte ho)
- `__set_name__`/`__init_subclass__` pehle ho chuke hote hain
"""),
    code('''
import functools

# Decorator #1: auto __repr__ / __eq__ (dataclass ka chhota version)
def auto_dunder(cls=None, *, eq=True, order=False):
    def wrap(klass):
        fields = tuple(getattr(klass, "__annotations__", {}))

        if "__repr__" not in klass.__dict__:
            def __repr__(self):
                inner = ", ".join(f"{f}={getattr(self, f)!r}" for f in fields)
                return f"{type(self).__name__}({inner})"
            klass.__repr__ = __repr__

        if eq and "__eq__" not in klass.__dict__:
            def __eq__(self, other):
                if type(self) is not type(other):
                    return NotImplemented
                return all(getattr(self, f) == getattr(other, f) for f in fields)
            klass.__eq__ = __eq__
            klass.__hash__ = lambda self: hash(tuple(getattr(self, f) for f in fields))

        if order:
            def __lt__(self, other):
                return tuple(getattr(self, f) for f in fields) < \\
                       tuple(getattr(other, f) for f in fields)
            klass.__lt__ = __lt__
            klass = functools.total_ordering(klass)

        klass._fields = fields
        return klass

    return wrap if cls is None else wrap(cls)


# Decorator #2: har public method ko log karo
def log_methods(prefix="CALL"):
    def deco(cls):
        for name, attr in list(vars(cls).items()):
            if name.startswith("_") or not callable(attr):
                continue

            def make(fn):
                @functools.wraps(fn)             # __name__/__doc__ mehfooz
                def wrapper(self, *a, **kw):
                    cls._log.append(f"{prefix} {fn.__name__}{a}")
                    return fn(self, *a, **kw)
                return wrapper

            setattr(cls, name, make(attr))
        cls._log = []
        return cls
    return deco


# Decorator #3: attribute freeze
def frozen(cls):
    original_setattr = cls.__setattr__

    def __setattr__(self, name, value):
        if getattr(self, "_locked", False):
            raise AttributeError(f"{type(self).__name__} frozen hai")
        original_setattr(self, name, value)

    def lock(self):
        original_setattr(self, "_locked", True)

    cls.__setattr__ = __setattr__
    cls.lock = lock
    return cls


@frozen
@log_methods(prefix="->")
@auto_dunder(order=True)
class Point:
    x: int
    y: int

    def __init__(self, x, y):
        self.x, self.y = x, y

    def translate(self, dx, dy):
        return Point(self.x + dx, self.y + dy)

    def norm2(self):
        return self.x ** 2 + self.y ** 2


p = Point(1, 2)
print("auto repr ->", p)
print("auto eq   ->", p == Point(1, 2), "| hash ok ->", isinstance(hash(p), int))
print("ordering  ->", sorted([Point(3, 1), Point(1, 5), Point(1, 2)]))
print("fields    ->", Point._fields)
print("\\nmethods:", p.translate(1, 1), "| norm2:", p.norm2())
print("call log  ->", Point._log)
print("wraps ne naam bachaya ->", Point.translate.__name__)

p.lock()
try:
    p.x = 100
except AttributeError as e:
    print("\\nfrozen ->", e)

assert p == Point(1, 2) and Point._fields == ("x", "y")
assert Point.translate.__name__ == "translate"
print("\\nTeen decorators compose ho gaye — metaclass se kahin saada.")
'''),
    code('''
# Decorator ka nuqsan: subclasses ko automatic nahi milta (jab ke __init_subclass__ deta hai)
registry_deco = {}

def register(cls):
    registry_deco[cls.__name__.lower()] = cls
    return cls


@register
class BaseJob:
    pass

class ChildJob(BaseJob):        # decorator lagana BHOOL gaye -> register nahi hui
    pass

print("decorator registry ->", list(registry_deco), " <- ChildJob gayab")


class BaseJob2:
    registry = {}
    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        cls.registry[cls.__name__.lower()] = cls

class ChildJob2(BaseJob2): pass
class GrandChildJob2(ChildJob2): pass

print("__init_subclass__  ->", list(BaseJob2.registry), " <- sab automatic")
assert "childjob" not in registry_deco
assert set(BaseJob2.registry) == {"childjob2", "grandchildjob2"}
print("\\nFaisla: 'opt-in per class' chahiye -> decorator. 'sab subclasses par lazmi' -> __init_subclass__.")
'''),
    md("""
## 10. Comparison: metaclass vs `__init_subclass__` vs class decorator

| Feature | Class decorator | `__init_subclass__` | Metaclass |
|---|---|---|---|
| Seekhna/parhna | 🟢 sab se aasan | 🟢 aasan | 🔴 mushkil |
| Subclasses par automatic | ❌ nahi | ✅ haan | ✅ haan |
| Namespace body chalne se pehle badalna (`__prepare__`) | ❌ | ❌ | ✅ |
| Namespace body ke baad, class banne se pehle badalna | ❌ | ❌ | ✅ (`__new__`) |
| Class attributes add/modify | ✅ | ✅ | ✅ |
| Class ka naam / bases badalna | 🟡 (nayi class bana kar) | ❌ | ✅ |
| Instance creation intercept (`Class()`) | 🟡 (`__new__` patch kar ke) | ❌ | ✅ (`__call__`) |
| Class-level `__getattr__` (`Class.x` fallback) | ❌ | ❌ | ✅ |
| Duplicate-name detection in body | ❌ | ❌ | ✅ |
| Conflicts ka khatra | 🟢 koi nahi | 🟢 koi nahi | 🔴 metaclass conflict |
| Compose karna | 🟢 aasan (stack) | 🟡 MRO + super() | 🔴 mushkil |
| `isinstance(Class, X)` custom | ❌ | ❌ | ✅ (`__instancecheck__`) |
| Typing/IDE support | 🟢 acha | 🟢 acha | 🟡 kamzor |

### Faisla ka flowchart (yaad karo)

```
Kya class BANNE ke waqt kuch karna hai?
├── Nahi -> normal inheritance / mixin / composition
└── Haan
    ├── Sirf kuch chuni hui classes par?      -> CLASS DECORATOR
    ├── Har subclass par automatic?
    │   ├── Sirf class attributes chhedne hain? -> __init_subclass__
    │   └── Namespace/bases/__call__ chahiye?   -> METACLASS
    └── isinstance/issubclass custom?           -> METACLASS (__instancecheck__) ya ABC.register
```

### "Kab metaclass warranted hai?" (sach sach)

✅ **Haan:**
- Instance creation control (singleton, instance caching/interning, pooling)
- `__prepare__` chahiye (duplicate detection, custom namespace, ordered magic)
- Virtual `isinstance`/`issubclass` (`__instancecheck__`, `__subclasscheck__`)
- Class-level `__getattr__` ya class par `property` jaisa behaviour
- Tum ek **framework** likh rahe ho jise hazaron log use karenge (Django/SQLAlchemy/Pydantic level)

❌ **Nahi (ye sab aasan tareeqon se ho jata hai):**
- Registry/plugins → `__init_subclass__`
- Validation/interface → `__init_subclass__` ya ABC ya Protocol
- Attribute injection / auto dunders → decorator ya `dataclass`
- Field collection → `__set_name__` + `__init_subclass__` (NB1 ka ORM yaad karo)

> **Tim Peters ka mashhoor jumla:** *"Metaclasses are deeper magic than 99% of users should ever
> worry about. If you wonder whether you need them, you don't."*
"""),
    code('''
# Same feature (registry + validation) teen tareeqon se — code ka size khud dekh lo
import inspect, textwrap

# ---- (1) METACLASS ----
class MetaWay(type):
    reg = {}
    def __new__(mcls, name, bases, ns, **kw):
        cls = super().__new__(mcls, name, bases, ns, **kw)
        if bases:
            if not callable(ns.get("run")):
                raise TypeError(f"{name}: run() chahiye")
            mcls.reg[name] = cls
        return cls

class MetaBase(metaclass=MetaWay): pass
class MetaTask(MetaBase):
    def run(self): return "meta-task"

# ---- (2) __init_subclass__ ----
class SubBase:
    reg = {}
    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        if not callable(getattr(cls, "run", None)):
            raise TypeError(f"{cls.__name__}: run() chahiye")
        SubBase.reg[cls.__name__] = cls

class SubTask(SubBase):
    def run(self): return "sub-task"

# ---- (3) DECORATOR ----
deco_reg = {}
def task(cls):
    if not callable(getattr(cls, "run", None)):
        raise TypeError(f"{cls.__name__}: run() chahiye")
    deco_reg[cls.__name__] = cls
    return cls

@task
class DecoTask:
    def run(self): return "deco-task"


for label, reg, sample in [
    ("metaclass", MetaWay.reg, MetaTask),
    ("__init_subclass__", SubBase.reg, SubTask),
    ("decorator", deco_reg, DecoTask),
]:
    print(f"{label:20} registry={list(reg)}  output={sample().run()}")

# Lines of "machinery" code ginte hain
sizes = {
    "metaclass": len(inspect.getsource(MetaWay).strip().splitlines()),
    "__init_subclass__": 6,
    "decorator": len(inspect.getsource(task).strip().splitlines()),
}
print("\\nmachinery lines ->", sizes)
print("Teenon ka natija same — magar parhne/debug karne me farq bohat bara hai.")
assert MetaTask().run() == "meta-task" and SubTask().run() == "sub-task"
'''),
    md("""
## 11. `__class_getitem__` aur `__mro_entries__`

### `__class_getitem__` — `MyClass[int]` ko kaam karwana

**Kya hai:** jab tum `SomeClass[...]` likho (subscript **class** par, instance par nahi), Python
`SomeClass.__class_getitem__(item)` bulata hai. Ye implicitly `classmethod` hai.

**Kahan use hota hai:** generics (`list[int]`, `dict[str, int]`), typed containers, DSLs.

### `__mro_entries__` — jab base class **class hi na ho** (PEP 560)

`class C(Generic[T])` me `Generic[T]` ek class **nahi**, ek `_GenericAlias` object hai. Python
uske `__mro_entries__(bases)` ko bula kar asli bases nikalta hai. Ye mechanism `typing` ko fast
banata hai. Rozana code me tum ise likhoge nahi — magar interview me iska naam lena impress karta
hai. Neeche ek chhota demo hai.
"""),
    code('''
from typing import TypeVar, Generic, get_args, get_origin

# (a) Apna __class_getitem__ — runtime type info ke sath typed container
class TypedList:
    """TypedList[int] -> ek nayi class jo sirf int accept karti hai."""

    item_type = object
    _cache = {}

    def __class_getitem__(cls, item):
        # implicit classmethod; hum har type ke liye ek subclass bana kar cache karte hain
        if item not in cls._cache:
            cls._cache[item] = type(
                f"{cls.__name__}[{getattr(item, '__name__', item)}]",
                (cls,),
                {"item_type": item},
            )
        return cls._cache[item]

    def __init__(self, items=()):
        self._items = []
        for it in items:
            self.append(it)

    def append(self, item):
        if not isinstance(item, self.item_type):
            raise TypeError(
                f"{type(self).__name__} sirf {self.item_type.__name__} leta hai, "
                f"mila {type(item).__name__}"
            )
        self._items.append(item)

    def __repr__(self):
        return f"{type(self).__name__}({self._items})"

    def __len__(self): return len(self._items)
    def __iter__(self): return iter(self._items)


IntList = TypedList[int]
StrList = TypedList[str]
print("IntList         ->", IntList.__name__, "| item_type:", IntList.item_type.__name__)
nums = IntList([1, 2, 3])
print("nums            ->", nums, "| len:", len(nums))
try:
    nums.append("chaar")
except TypeError as e:
    print("type check      ->", e)

print("StrList         ->", StrList(["a", "b"]))
print("caching kaam kar raha? ->", TypedList[int] is IntList)
assert TypedList[int] is IntList and len(nums) == 3

# (b) typing.Generic ke sath — standard tareeqa
T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self): self._items: list[T] = []
    def push(self, item: T) -> None: self._items.append(item)
    def pop(self) -> T: return self._items.pop()
    def __len__(self): return len(self._items)


s: Stack[int] = Stack()
s.push(1); s.push(2)
print("\\nGeneric Stack ->", s.pop(), "| len:", len(s))
alias = Stack[int]
print("Stack[int] ka type ->", type(alias).__name__)
print("get_origin ->", get_origin(alias).__name__, "| get_args ->", get_args(alias))
assert get_origin(Stack[int]) is Stack and get_args(Stack[int]) == (int,)
'''),
    code('''
# (c) __mro_entries__ ka demo: base "class" jo class hi nahi hai
class Injector:
    """Ye class nahi — magar base ki jagah likha ja sakta hai (PEP 560)."""

    def __init__(self, *extra_bases):
        self.extra_bases = extra_bases

    def __mro_entries__(self, bases):
        # Python yahan se ASLI bases mangta hai
        print(f"  __mro_entries__ bula liya gaya; bases={[getattr(b, '__name__', b) for b in bases]}")
        return self.extra_bases


class LoggerMixin:
    def log(self, msg): return f"[LOG] {msg}"


class TimerMixin:
    def elapsed(self): return 0.5


print("class define ho rahi hai:")
class Service(Injector(LoggerMixin, TimerMixin)):     # base ek Injector INSTANCE hai!
    def work(self): return "kaam ho gaya"


svc = Service()
print("\\nMRO       ->", [c.__name__ for c in Service.__mro__])
print("log       ->", svc.log("hello"))
print("elapsed   ->", svc.elapsed())
print("__orig_bases__ ->", type(Service.__orig_bases__[0]).__name__, "(asli likha hua base yaad hai)")
assert isinstance(svc, LoggerMixin) and isinstance(svc, TimerMixin)
print("\\nYehi mechanism typing.Generic[T] ko base banne deta hai.")
'''),
]

cells += [
    md("""
## 12. Dynamic OOP toolkit — `getattr` / `setattr` / `hasattr` / `delattr`

**Kya hai:** attribute ka naam **runtime par string** ki soorat me ho to ye 4 builtins use karo.

| Builtin | Barabar | Note |
|---|---|---|
| `getattr(o, "x")` | `o.x` | 3rd arg = default (no exception) |
| `setattr(o, "x", v)` | `o.x = v` | |
| `hasattr(o, "x")` | try/except AttributeError | andar `getattr` hi chalta hai |
| `delattr(o, "x")` | `del o.x` | |

**Kahan use hota hai:** config loaders, serializers, CLI/HTTP dispatch, ORMs, test factories.

**Gotcha:** `hasattr` **poora getattr chalata hai** — agar property ke andar mehnga kaam ya
side-effect ho to wo bhi chalega. Aur Python 3 me `hasattr` sirf `AttributeError` ko pakarta hai
(baqi exceptions upar aa jate hain).
"""),
    code('''
class Settings:
    def __init__(self):
        self.host = "localhost"
        self.port = 8080

    @property
    def expensive(self):
        print("   (mehnga computation chala!)")
        return 42

    @property
    def broken(self):
        raise ValueError("ye property toot gayi")


s = Settings()

# String naam se access
for name in ["host", "port", "missing"]:
    print(f"getattr({name!r}) ->", getattr(s, name, "<default>"))

# Dict se object bharna (config loader ka core)
config = {"host": "0.0.0.0", "port": 9090, "debug": True}
for k, v in config.items():
    setattr(s, k, v)
print("\\nload ke baad ->", vars(s))

# hasattr side-effect chalata hai
print("\\nhasattr(s, 'expensive'):")
print("  natija ->", hasattr(s, "expensive"))

# hasattr sirf AttributeError pakarta hai
try:
    hasattr(s, "broken")
except ValueError as e:
    print("\\nhasattr ne ValueError nahi chhupaya ->", e)

delattr(s, "debug")
print("\\ndelattr ke baad ->", vars(s))
assert not hasattr(s, "debug") and s.port == 9090
'''),
    code('''
# Practical: string-based dispatch (if-else chain ki jagah) — HTTP-style router
class Controller:
    """Method naam se dispatch: GET /users -> get_users()"""

    def get_users(self, **params):
        return {"users": ["ali", "sara"], "params": params}

    def get_user(self, user_id, **params):
        return {"user": f"user-{user_id}"}

    def post_users(self, **params):
        return {"created": params}

    def dispatch(self, method, resource, **params):
        handler_name = f"{method.lower()}_{resource}"
        handler = getattr(self, handler_name, None)
        if handler is None or not callable(handler):
            # available routes bata do (introspection se)
            available = sorted(
                n for n in dir(self)
                if not n.startswith("_") and n != "dispatch" and callable(getattr(self, n))
            )
            return {"error": f"404 {method} /{resource}", "available": available}
        return handler(**params)


c = Controller()
print(c.dispatch("GET", "users", page=1))
print(c.dispatch("GET", "user", user_id=7))
print(c.dispatch("POST", "users", name="bilal"))
print(c.dispatch("DELETE", "users"))
assert c.dispatch("GET", "users")["users"] == ["ali", "sara"]
assert "error" in c.dispatch("PATCH", "nope")
print("\\nFaida: naya endpoint add karne ke liye sirf naya method likho — dispatch code na chhero.")
'''),
    md("""
## 13. `inspect` — runtime introspection

| Function | Kaam |
|---|---|
| `inspect.signature(fn)` | parameters, defaults, annotations |
| `inspect.isclass/isfunction/ismethod` | qism check |
| `inspect.getmembers(obj, predicate)` | sab members filter ke sath |
| `inspect.getsource(obj)` | source code (agar file se load hua) |
| `inspect.getmro(cls)` | MRO |
| `inspect.isabstract(cls)` | abstract hai? |
| `inspect.getdoc(obj)` | cleaned docstring |
| `inspect.stack()` / `currentframe()` | call stack (debugging) |

**Kahan use hota hai:** dependency injection, auto CLI/API generation, validation frameworks,
test collection (pytest), documentation tools.
"""),
    code('''
import inspect

class Repository:
    """Data access layer."""

    table = "items"

    def __init__(self, connection: str, timeout: float = 5.0, *, retries: int = 3):
        self.connection, self.timeout, self.retries = connection, timeout, retries

    def find(self, id_: int) -> dict:
        """Ek record dhoondo."""
        return {"id": id_}

    @classmethod
    def from_url(cls, url: str) -> "Repository":
        return cls(url)

    @staticmethod
    def ping() -> bool:
        return True

    @property
    def dsn(self) -> str:
        return f"db://{self.connection}"


# 1) signature — parameters ki poori tafseel
sig = inspect.signature(Repository.__init__)
print("signature ->", sig)
for name, param in sig.parameters.items():
    if name == "self":
        continue
    default = "<required>" if param.default is inspect.Parameter.empty else repr(param.default)
    ann = "<none>" if param.annotation is inspect.Parameter.empty else getattr(
        param.annotation, "__name__", str(param.annotation))
    print(f"  {name:12} kind={param.kind.name:20} default={default:8} type={ann}")

# 2) members ko qism ke hisab se chhanto
print("\\n--- members by kind ---")
kinds = {}
for name, member in inspect.getmembers(Repository):
    if name.startswith("_"):
        continue
    raw = Repository.__dict__.get(name)
    if isinstance(raw, staticmethod):
        kind = "staticmethod"
    elif isinstance(raw, classmethod):
        kind = "classmethod"
    elif isinstance(raw, property):
        kind = "property"
    elif inspect.isfunction(member):
        kind = "method"
    else:
        kind = "attribute"
    kinds.setdefault(kind, []).append(name)
for kind, names in sorted(kinds.items()):
    print(f"  {kind:14} -> {names}")

print("\\nisclass ->", inspect.isclass(Repository), "| isabstract ->", inspect.isabstract(Repository))
print("getdoc  ->", inspect.getdoc(Repository))
print("MRO     ->", [c.__name__ for c in inspect.getmro(Repository)])
assert kinds["property"] == ["dsn"] and "find" in kinds["method"]
'''),
    code('''
# inspect ka killer use-case: signature se automatic dependency injection
import inspect

class Container:
    """Chhota DI container — constructor annotations dekh kar dependencies khud banata hai."""

    def __init__(self):
        self._providers = {}
        self._singletons = {}

    def register(self, cls, singleton=False):
        self._providers[cls] = singleton
        return cls

    def resolve(self, cls):
        if self._providers.get(cls) and cls in self._singletons:
            return self._singletons[cls]

        sig = inspect.signature(cls.__init__)
        kwargs = {}
        for name, param in sig.parameters.items():
            if name == "self":
                continue
            ann = param.annotation
            if inspect.isclass(ann) and ann in self._providers:
                kwargs[name] = self.resolve(ann)          # recursive resolve
            elif param.default is not inspect.Parameter.empty:
                kwargs[name] = param.default
            else:
                raise TypeError(f"{cls.__name__}.{name}: kaise banaun? register karo ya default do")

        instance = cls(**kwargs)
        if self._providers.get(cls):
            self._singletons[cls] = instance
        return instance


class Config:
    def __init__(self, env: str = "dev"):
        self.env = env

class Connection:
    def __init__(self, config: Config):
        self.config = config
        self.id = id(self) % 1000

class UserRepo:
    def __init__(self, conn: Connection):
        self.conn = conn

class UserService:
    def __init__(self, repo: UserRepo, conn: Connection):
        self.repo, self.conn = repo, conn
    def describe(self):
        return f"UserService(env={self.repo.conn.config.env}, conn={self.conn.id})"


container = Container()
for c in (Config, UserRepo, UserService):
    container.register(c)
container.register(Connection, singleton=True)       # connection shared hona chahiye

svc = container.resolve(UserService)
print("resolve ->", svc.describe())
print("connection shared? ->", svc.conn is svc.repo.conn)
assert svc.conn is svc.repo.conn                     # singleton kaam kar raha
assert svc.repo.conn.config.env == "dev"

class Unregistered:
    def __init__(self, mystery: "SomethingElse"): ...   # noqa: F821
try:
    container.resolve(Unregistered)
except TypeError as e:
    print("\\nun-resolvable ->", e)
print("\\nYehi asool FastAPI/pytest fixtures/Spring jaisi cheezon ke peeche hai.")
'''),
    md("""
## 14. Monkey patching — safe patterns

**Kya hai:** runtime par mojood class/module ka behaviour badal dena.

**Kab jaiz hai:**
- **Tests** me (network/time/random ko fake karna) — sab se acha use
- Third-party library ke bug ka **temporary** hotfix
- Instrumentation/profiling (metrics wrap karna)

**Kab bura hai:** production business logic me. Kyun? "Action at a distance" — koi doosri file
padh kar samajh hi nahi sakta ke behaviour kyun badla.

**Safe patterns:**
1. **Original ko save** karo aur **restore** karo (context manager)
2. `functools.wraps` use karo (naam/doc/signature mehfooz)
3. Tests me `unittest.mock.patch` (khud restore karta hai)
4. Patch ko ek **jaga** rakho aur comment me "kyun" likho
"""),
    code('''
import functools
from contextlib import contextmanager

# Wo class jise hum "third-party" maan rahe hain
class PaymentGateway:
    def charge(self, amount):
        # asli zindagi me: network call
        return {"status": "charged", "amount": amount, "network": True}

    def refund(self, txn_id):
        return {"status": "refunded", "txn": txn_id}


# --- Pattern 1: context manager wala safe patch ---
@contextmanager
def patched(target_cls, name, new_func):
    """Attribute ko temporarily replace karo, phir hamesha wapis kar do."""
    sentinel = object()
    original = target_cls.__dict__.get(name, sentinel)
    setattr(target_cls, name, new_func)
    try:
        yield
    finally:
        if original is sentinel:
            delattr(target_cls, name)                 # jo nahi tha use hata do
        else:
            setattr(target_cls, name, original)       # jo tha use wapis


gw = PaymentGateway()
print("asli       ->", gw.charge(100))

def fake_charge(self, amount):
    return {"status": "charged", "amount": amount, "network": False}

with patched(PaymentGateway, "charge", fake_charge):
    print("patch ke andar ->", gw.charge(100))

print("bahar (restore) ->", gw.charge(100))
assert gw.charge(1)["network"] is True


# --- Pattern 2: behaviour ADD karo (wrap), replace na karo ---
def add_logging(cls, method_name, log_list):
    original = getattr(cls, method_name)

    @functools.wraps(original)                        # naam/doc mehfooz
    def wrapper(self, *a, **kw):
        log_list.append((method_name, a, kw))
        result = original(self, *a, **kw)             # asli kaam wahi
        log_list.append((method_name, "returned", result["status"]))
        return result

    wrapper._original = original                      # undo ke liye rakh lo
    setattr(cls, method_name, wrapper)
    return wrapper


audit = []
add_logging(PaymentGateway, "refund", audit)
print("\\nwrapped refund ->", gw.refund("txn-1"))
print("audit log      ->", audit)
print("naam mehfooz   ->", PaymentGateway.refund.__name__)

# Undo
PaymentGateway.refund = PaymentGateway.refund._original
print("undo ke baad audit nahi barhega ->", gw.refund("txn-2"), "| log size:", len(audit))
assert len(audit) == 2 and PaymentGateway.refund.__name__ == "refund"
'''),
    code('''
# Tests me sahi tareeqa: unittest.mock.patch (khud restore karta hai + call assertions)
from unittest.mock import patch, MagicMock
import unittest

class OrderService:
    def __init__(self, gateway):
        self.gateway = gateway

    def checkout(self, amount):
        if amount <= 0:
            raise ValueError("amount > 0 hona chahiye")
        result = self.gateway.charge(amount)
        return f"order ok: {result['status']} {result['amount']}"


class TestOrderService(unittest.TestCase):
    def test_checkout_with_mock_object(self):
        # (a) Dependency injection + MagicMock — sab se saaf tareeqa
        fake_gw = MagicMock()
        fake_gw.charge.return_value = {"status": "charged", "amount": 500}
        svc = OrderService(fake_gw)
        self.assertEqual(svc.checkout(500), "order ok: charged 500")
        fake_gw.charge.assert_called_once_with(500)     # interaction verify

    def test_checkout_with_patch(self):
        # (b) patch.object — class ki method ko temporarily badlo
        with patch.object(PaymentGateway, "charge",
                          return_value={"status": "test", "amount": 1}) as mocked:
            svc = OrderService(PaymentGateway())
            self.assertEqual(svc.checkout(1), "order ok: test 1")
            self.assertTrue(mocked.called)
        # bahar aate hi asli method wapis
        self.assertTrue(PaymentGateway().charge(5)["network"])

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            OrderService(MagicMock()).checkout(0)


suite = unittest.TestLoader().loadTestsFromTestCase(TestOrderService)
import io
result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
print(f"tests run: {result.testsRun} | failures: {len(result.failures)} | errors: {len(result.errors)}")
for t, tb in result.failures + result.errors:
    print(t, tb)
assert result.wasSuccessful()
print("[pass] mock/patch tests")
print("\\nSabaq: manual monkey patch se behtar hai dependency INJECT karna (testable design).")
'''),
    code('''
# Runtime mixin injection — chalti hui class me nayi capabilities daalna
class Serializable:
    def to_json(self):
        import json
        return json.dumps({k: v for k, v in vars(self).items() if not k.startswith("_")},
                          sort_keys=True)


class Comparable:
    def __eq__(self, other):
        return type(self) is type(other) and vars(self) == vars(other)
    def __hash__(self):
        return hash(tuple(sorted(vars(self).items())))


class Plain:
    def __init__(self, a, b):
        self.a, self.b = a, b


p = Plain(1, 2)
print("pehle to_json hai? ->", hasattr(p, "to_json"))

# Tareeqa 1: __bases__ ko badlo (chalta hai magar naazuk)
Plain.__bases__ = (Serializable, Comparable)
print("bases badalne ke baad ->", p.to_json())
print("equality              ->", p == Plain(1, 2))
print("MRO                   ->", [c.__name__ for c in Plain.__mro__])
assert p.to_json() == '{"a": 1, "b": 2}'

# Tareeqa 2 (BEHTAR): nayi class banao purani + mixins se
class Plain2:
    def __init__(self, a):
        self.a = a

Enhanced = type("Enhanced", (Serializable, Plain2), {})
e = Enhanced(5)
print("\\nnayi class se ->", e.to_json(), "| isinstance(Plain2) ->", isinstance(e, Plain2))

# Tareeqa 3: sirf methods copy karo (sab se kam invasive)
for name, fn in vars(Serializable).items():
    if not name.startswith("__"):
        setattr(Plain2, name, fn)
print("methods copy ->", Plain2(9).to_json())
assert Plain2(9).to_json() == '{"a": 9}'
print("\\nWarning: __bases__ badalna layout-conflict par TypeError de sakta hai (e.g. __slots__).")
'''),
    code('''
# abc.register — "virtual subclass" (inheritance ke baghair isinstance sach)
from abc import ABC, abstractmethod

class JsonSerializable(ABC):
    @abstractmethod
    def to_json(self): ...


# Ek third-party class jise hum badal nahi sakte
class ThirdPartyPoint:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def to_json(self):
        return f'{{"x": {self.x}, "y": {self.y}}}'


print("pehle isinstance ->", isinstance(ThirdPartyPoint(1, 2), JsonSerializable))

JsonSerializable.register(ThirdPartyPoint)            # virtual subclass bana do

pt = ThirdPartyPoint(1, 2)
print("register ke baad ->", isinstance(pt, JsonSerializable))
print("issubclass       ->", issubclass(ThirdPartyPoint, JsonSerializable))
print("MRO me hai?      ->", JsonSerializable in ThirdPartyPoint.__mro__, "<- NAHI (virtual hai)")
print("to_json          ->", pt.to_json())

# Decorator ki tarah bhi
@JsonSerializable.register
class MyPoint:
    def to_json(self): return "{}"

print("decorator se     ->", issubclass(MyPoint, JsonSerializable))
assert isinstance(pt, JsonSerializable) and JsonSerializable not in ThirdPartyPoint.__mro__

# GOTCHA: register abstract methods CHECK nahi karta
@JsonSerializable.register
class Liar:
    pass                                              # to_json nahi hai!

print("\\nLiar isinstance ->", isinstance(Liar(), JsonSerializable), "<- True, magar...")
try:
    Liar().to_json()
except AttributeError as e:
    print("...call par crash ->", type(e).__name__, "-", e)
print("Isi liye structural checks ke liye typing.Protocol behtar hai (NB4 me).")
'''),
]

save(PATH, cells)
