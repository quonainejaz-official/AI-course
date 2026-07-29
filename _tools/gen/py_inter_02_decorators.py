# Generator script: Python/Intermediate/02_Closures_Decorators_aur_Functional_Python.ipynb
import sys

sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save  # noqa: E402

PATH = r"Python/Intermediate/02_Closures_Decorators_aur_Functional_Python.ipynb"

cells = []

cells += [
md("""
# 02 — Closures, Decorators aur Functional Python

**Level:** Intermediate  ·  **Language:** Python 3.14  ·  **Series:** Python/Intermediate

Python me functions **objects** hain. Isi ek baat se closures, decorators, aur poora functional
programming style nikalta hai. Django/Flask/FastAPI/pytest — sab decorators par khade hain.

## Is notebook me kya seekhenge

- **First-class functions** — function ko variable, argument, return value ki tarah use karna
- **Higher-order functions** — function jo function le ya de
- **Nested functions** aur **LEGB** scope rule, `nonlocal` / `global`
- **Closures** — `__closure__`, `cell_contents`, `co_freevars` se andar dekhna
- **Late binding trap** loops me (aur uske 3 hal)
- **Decorator scratch se** — manual wrapping se `@` tak
- `*args`/`**kwargs` wala **generic** decorator
- `functools.wraps` kyun **lazmi** hai
- **Decorator with arguments** (3-level nesting)
- **Stacked decorators** ka order (bottom-up — sabit karenge)
- **Class-based decorator** (`__call__`) aur **method decorator**
- Asli kaam ke decorators: **timer, retry, memoize, logging, validate-types, rate-limit**
- `functools.lru_cache` / `cache` — `cache_info()`, hits/misses
- `functools`: `partial`, `partialmethod`, `reduce`, `singledispatch`, `total_ordering`, `cached_property`
- `operator` module — `itemgetter`, `attrgetter`, `methodcaller`
- `map`/`filter`/`reduce` **vs** comprehension — readability + **speed measurement**
- Gotchas, Real-world problems, **LeetCode (146, 509, 70, 1137)**, Interview Q&A, Practice, Cheat-sheet

## Prerequisites

- Functions, `*args`/`**kwargs` ka basic idea
- Classes ka thora taaruf (`__init__`, `self`)
- NB 01 (generators) — zaroori nahi magar madadgar

> **Tip:** Cells upar se neeche chalao — baad ke cells pehle wale decorators use karte hain.
"""),
]

cells += [
md("""
---
## 1. First-class functions — bunyad

Python me function bhi ek **object** hai (jaise `int`, `list`). Iska matlab:

1. Function ko **variable** me rakh sakte ho
2. Function ko dusre function ka **argument** bana sakte ho
3. Function se function **return** kar sakte ho
4. Function ko **list/dict** me store kar sakte ho
5. Function ke apne **attributes** hote hain (`__name__`, `__doc__`, `__module__`...)

Yehi "first-class" hona kehlata hai. Isi ki wajah se decorators mumkin hain.
"""),
code("""
# ---- Function ek object hai: iske attributes dekho ----

def greet(name):
    '''Kisi ko salam karta hai.'''       # ye docstring hai
    return f"Assalam-o-Alaikum, {name}!"

print("type       :", type(greet))
print("__name__   :", greet.__name__)          # function ka naam (string)
print("__doc__    :", greet.__doc__)           # docstring
print("__module__ :", greet.__module__)
print("id (address):", type(greet.__code__).__name__, "object mojood hai")

# Function par apna attribute bhi laga sakte ho (decorators isse use karte hain)
greet.call_count = 0
print("custom attr:", greet.call_count)
"""),
code("""
# ---- 1) Variable me rakhna: naam sirf ek "label" hai, function object alag ----
say_hi = greet                 # koi () nahi -- yani CALL nahi kiya, sirf reference copy kiya
print("say_hi('Ali')  ->", say_hi("Ali"))
print("dono same object?", say_hi is greet)     # True
print("say_hi ka __name__:", say_hi.__name__)   # 'greet' -- asal naam wahi raha!

print("-" * 50)
# GOTCHA: bracket lagate hi function CALL ho jata hai
x = greet          # reference
y = greet("Sara")  # CALL ka NATIJA (string)
print("x ka type:", type(x).__name__, "| y ka type:", type(y).__name__)
"""),
code("""
# ---- 2) & 4) List/dict me functions: ye "dispatch table" pattern hai ----

def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): return "undefined" if b == 0 else a / b

# Dict of functions -- long if/elif chain ki jagah (bohat Pythonic)
OPS = {"+": add, "-": sub, "*": mul, "/": div}

def calculate(a, op, b):
    fn = OPS.get(op)                    # function dhoondo
    if fn is None:
        return f"unknown operator: {op}"
    return fn(a, b)                     # phir call karo

for op in ["+", "-", "*", "/", "%"]:
    print(f"  10 {op} 3 =", calculate(10, op, 3))
print("  10 / 0 =", calculate(10, "/", 0))     # edge case handle
"""),
md("""
**Interview tip:** `OPS` dict wala pattern **dispatch table** kehlata hai. Jab bhi 5+ `elif` dikhein,
sochna chahiye: *"kya main isko dict of functions bana sakta hoon?"* Faida: `O(1)` lookup, naye operator
add karna aasan, aur test karna aasan.
"""),
]

cells += [
md("""
---
## 2. Higher-order functions

**Definition:** Jo function (a) function ko **argument** le, ya (b) function **return** kare — wo
higher-order function hai.

Built-in misalein: `map`, `filter`, `sorted(key=)`, `min/max(key=)`, `functools.reduce`.
"""),
code("""
# ---- (a) Function ko ARGUMENT lena ----

def apply_twice(fn, value):
    # fn ko do baar lagao: fn(fn(value))
    return fn(fn(value))

print("apply_twice(str.upper, 'ab'):", apply_twice(str.upper, "ab"))
print("apply_twice(lambda x: x*3, 2):", apply_twice(lambda x: x * 3, 2))    # 2*3=6, 6*3=18

print("-" * 50)
# Built-in higher-order functions
words = ["Pakistan", "fig", "Bangladesh", "kiwi", "Sri Lanka"]
print("sorted by len :", sorted(words, key=len))                  # key= ek FUNCTION hai
print("sorted by last:", sorted(words, key=lambda w: w[-1]))
print("max by len    :", max(words, key=len))
print("map upper     :", list(map(str.upper, ["ali", "sara"])))
print("filter long   :", list(filter(lambda w: len(w) > 4, words)))
"""),
code("""
# ---- (b) Function RETURN karna: ye "function factory" hai ----

def make_multiplier(factor):
    # Andar wala function BANATA hai aur return karta hai (call nahi karta)
    def multiplier(x):
        return x * factor              # `factor` bahar wale scope se aa raha hai
    return multiplier                  # bracket NAHI -- function object return

double = make_multiplier(2)            # factor=2 wala function
triple = make_multiplier(3)            # factor=3 wala function

print("double(5) :", double(5))
print("triple(5) :", triple(5))
print("dono alag objects?", double is not triple)
print("double ka type:", type(double).__name__)

# Ye do functions ek hi code share karte hain, magar unka `factor` ALAG hai
print("double.__code__ is triple.__code__ ->", double.__code__ is triple.__code__)
"""),
md("""
### Output ka matlab (bohat ahem)

`double` aur `triple` ka **code same** hai (`__code__` same object hai!) magar unka **data (`factor`) alag**
hai. Ye "code + captured data" ka jodha hi **closure** kehlata hai — agla section.
"""),
]

cells += [
md("""
---
## 3. Nested functions aur LEGB scope rule

Jab Python koi naam (variable) dhoondta hai, wo **LEGB** order me dekhta hai:

```
L  ->  Local        (current function ke andar)
E  ->  Enclosing    (bahar wale function ke andar) <- nested functions ke liye
G  ->  Global       (module level)
B  ->  Built-in     (print, len, ...)
```

Pehla jahan mil jaye, wahin ruk jata hai.

### Likhne ke rules

| Keyword | Kaam |
|---|---|
| (kuch nahi) | Assignment se **local** variable banta hai |
| `nonlocal x` | **Enclosing** function ka `x` badlo |
| `global x` | **Module-level** `x` badlo |
"""),
code("""
# ---- LEGB ko action me dekho ----

value = "GLOBAL"                       # G

def outer():
    value = "ENCLOSING"                # E (outer ka local)

    def inner():
        value = "LOCAL"                # L (inner ka local)
        print("   inner me value  :", value)      # L jeeta

    inner()
    print("   outer me value  :", value)          # inner ne outer ko nahi badla

outer()
print("global me value :", value)                 # global bilkul safe raha

print("-" * 50)
# B (built-in) ki misaal -- aur ek khatarnaak gotcha
print("built-in len   :", len([1, 2, 3]))
len_backup = len
len = "OOPS, built-in shadow ho gaya"    # GALTI: built-in ko chhupa diya
try:
    print(len([1, 2, 3]))
except TypeError as e:
    print("shadowing ->", type(e).__name__, ":", e)
len = len_backup                          # theek karo
print("wapis theek   :", len([1, 2, 3]))
"""),
code("""
# ---- `nonlocal`: enclosing scope ko BADALNA ----

def counter_broken():
    count = 0
    def increment():
        # count = count + 1   <- ye UnboundLocalError deta, kyunki assignment
        #                        se `count` LOCAL ban jata hai (bahar wala nahi)
        return count + 1       # sirf parh rahe hain -> theek hai
    increment()
    return count               # 0 hi rahega

def counter_working():
    count = 0
    def increment():
        nonlocal count         # "count bahar wale function ka hai, naya local na banao"
        count += 1
        return count
    increment(); increment(); increment()
    return count

print("broken  :", counter_broken(), " <- badla nahi")
print("working :", counter_working(), " <- nonlocal se badal gaya")

print("-" * 50)
# UnboundLocalError ka live demo (safe try/except me)
def bad():
    n = 5
    def inner():
        n += 1                 # assignment -> n local, magar abhi value nahi -> error
        return n
    return inner()

try:
    bad()
except UnboundLocalError as e:
    print("Gotcha ->", type(e).__name__, ":", e)
    print("HAL: `nonlocal n` likho (ya mutable container use karo)")
"""),
code("""
# ---- `global` aur mutable-container trick ----

hits = 0                       # module-level

def record_hit_global():
    global hits                # module-level `hits` badlo
    hits += 1

record_hit_global(); record_hit_global()
print("global se hits:", hits)

print("-" * 50)
# Purana tareeqa (Python 2 me nonlocal nahi tha): mutable container
def make_counter_dict():
    state = {"n": 0}           # dict MUTATE karna hai, rebind nahi -> nonlocal ki zaroorat nahi
    def inc():
        state["n"] += 1        # ye ek METHOD call hai (mutation), assignment nahi
        return state["n"]
    return inc

c = make_counter_dict()
print("dict trick:", c(), c(), c())
print("(aaj ke Python me `nonlocal` behtar hai -- magar ye trick classes/lists me bhi kaam aata hai)")
"""),
]

cells += [
md("""
---
## 4. Closures — andar se kholte hain

**Definition:** Closure ek **nested function** hai jo apne **enclosing scope ke variables ko yaad rakhta
hai**, chahe bahar wala function khatam ho chuka ho.

### Closure banne ki 3 sharten
1. Ek nested (andar wala) function ho
2. Wo bahar wale scope ka koi variable **use** kare (free variable)
3. Bahar wala function usko **return** kare

### Kahan use hota hai?
- Decorators (poora concept isi par khada hai)
- Function factories (`make_multiplier`)
- Callbacks jinme configuration "baked in" ho
- Data hiding — chhota state bina poori class banane ke

Python ye state kahan rakhta hai? `function.__closure__` me — **cell** objects ka tuple.
"""),
code("""
# ---- Closure ke andar jhaank kar dekhte hain ----

def make_greeter(greeting, punctuation="!"):
    def greeter(name):
        # `greeting` aur `punctuation` FREE variables hain (yahan define nahi hue)
        return f"{greeting}, {name}{punctuation}"
    return greeter

salam = make_greeter("Assalam-o-Alaikum")
hello = make_greeter("Hello", punctuation="...")

print(salam("Ali"))
print(hello("Sara"))

print("-" * 55)
# 1) Kaun se variables capture hue? -> __code__.co_freevars
print("co_freevars    :", salam.__code__.co_freevars)

# 2) Un variables ki VALUES kahan hain? -> __closure__ (cell objects)
print("__closure__    :", salam.__closure__)
print("cell values    :", [cell.cell_contents for cell in salam.__closure__])
print("hello ki values:", [cell.cell_contents for cell in hello.__closure__])

# 3) Normal function (jo kuch capture na kare) ka __closure__ None hota hai
def plain(x): return x * 2
print("plain.__closure__:", plain.__closure__, " <- closure nahi hai")
"""),
code("""
# ---- Closure ka state ZINDA rehta hai (bahar wala function khatam hone ke baad bhi) ----

def make_account(balance=0):
    # Ye chhoti "class jaisi" cheez hai -- bina class ke
    history = []

    def deposit(amount):
        nonlocal balance                 # balance rebind karna hai -> nonlocal
        balance += amount
        history.append(("deposit", amount))    # list MUTATE -> nonlocal ki zaroorat nahi
        return balance

    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            return f"insufficient funds (balance {balance})"
        balance -= amount
        history.append(("withdraw", amount))
        return balance

    def statement():
        return {"balance": balance, "transactions": len(history), "history": list(history)}

    # Teen closures return karte hain -- teeno WAHI balance/history share karte hain
    return deposit, withdraw, statement

dep, wd, stmt = make_account(1000)
print("deposit 500  ->", dep(500))
print("withdraw 200 ->", wd(200))
print("withdraw 9999->", wd(9999))          # reject
print("deposit 100  ->", dep(100))
print("statement    ->", stmt())

# `balance` bahar se access NAHI ho sakta -- ye encapsulation hai
print()
print("teeno same cell share karte hain?",
      dep.__closure__[0] is wd.__closure__[0])
"""),
md("""
### Output ka matlab

`dep`, `wd`, `stmt` teeno **ek hi** `balance` cell share karte hain (`is` check `True` aaya). Yani closure
sirf value ki copy nahi — **shared mutable state** hai. `make_account` kab ka khatam ho chuka hai, magar
uska local `balance` zinda hai kyunki teen closures usko reference kar rahe hain.

**Interview tip:** *"Closure aur class me kya farq?"* → *"Class zyada explicit aur extensible hai (methods,
inheritance, `__repr__`). Closure halka hai — 1-2 pieces of state ke liye. Agar 3+ state ya methods chahiye,
class use karo."*
"""),
code("""
# ---- Closure vs class: same kaam, do tareeqe ----

# Closure version
def counter_closure():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc

# Class version
class CounterClass:
    def __init__(self):
        self.n = 0
    def __call__(self):          # __call__ se object "function jaisa" ban jata hai
        self.n += 1
        return self.n

c1 = counter_closure()
c2 = CounterClass()
print("closure:", c1(), c1(), c1())
print("class  :", c2(), c2(), c2())
print("class ka faida: state bahar se dikhta hai ->", c2.n)
print("closure ka state chupa hua hai (sirf __closure__ se) ->", c1.__closure__[0].cell_contents)
"""),
]

cells += [
md("""
---
## 5. Late Binding Trap — loops me closures

Ye Python ka **sab se mashhoor gotcha** hai aur interview me bohat poocha jata hai.

**Masla:** Closure variable ki **value** capture nahi karta, wo **variable (cell)** capture karta hai.
Value tab parhi jati hai jab function **call** hota hai — na ke jab define hota hai. Isko
**late binding** kehte hain.

Loop me sab closures **ek hi** loop variable ko share karte hain, aur loop khatam hone par us variable ki
value **aakhri** hoti hai.
"""),
code("""
# ---- MASLA: sab functions same (aakhri) value dete hain ----

def build_funcs():
    # NOTE: loop ko function ke ANDAR rakha hai taake `i` ek closure cell bane.
    # (Module level par `i` global hota hai -> __closure__ None aata hai, cell nahi.)
    out = []
    for i in range(5):
        out.append(lambda: i)      # `i` capture hua -- magar VALUE nahi, CELL
    return out

funcs = build_funcs()
print("Tawaqqu :", [0, 1, 2, 3, 4])
print("Haqeeqat:", [f() for f in funcs], "  <- sab 4! (loop ka aakhri i)")

# Kyun? Kyunki sab lambdas EK HI cell share karte hain:
print()
print("co_freevars               :", funcs[0].__code__.co_freevars)
print("sab ka closure cell same? :",
      all(f.__closure__[0] is funcs[0].__closure__[0] for f in funcs))
print("us cell ki value ab       :", funcs[0].__closure__[0].cell_contents)
"""),
code("""
# ================= 3 HAL =================

# HAL 1: Default argument -- value DEFINE time par freeze ho jati hai
def build_default_arg():
    out = []
    for i in range(5):
        out.append(lambda i=i: i)     # `i=i` -> default value ABHI evaluate hui
    return out
funcs1 = build_default_arg()
print("HAL 1 (default arg)  :", [f() for f in funcs1])

# HAL 2: Factory function -- har call apna naya scope banata hai
def make_returner(value):
    return lambda: value              # har call ka apna `value` cell
funcs2 = [make_returner(i) for i in range(5)]
print("HAL 2 (factory)      :", [f() for f in funcs2])

# HAL 3: functools.partial -- argument abhi bind ho gaya
from functools import partial
def identity(x): return x
funcs3 = [partial(identity, i) for i in range(5)]
print("HAL 3 (partial)      :", [f() for f in funcs3])

assert [f() for f in funcs1] == [f() for f in funcs2] == [f() for f in funcs3] == [0, 1, 2, 3, 4]
print()
print("Teeno hal ka natija same:", [f() for f in funcs1])
"""),
code("""
# ---- Asli duniya me ye trap kahan pakadta hai? Event handlers / callbacks ----

# GALAT: sab buttons "Save" ka message dikhayenge
buttons_bad = []
for label in ["New", "Open", "Save"]:
    buttons_bad.append(lambda: f"clicked: {label}")
print("GALAT:", [b() for b in buttons_bad])

# SAHI: default arg se bind karo
buttons_good = []
for label in ["New", "Open", "Save"]:
    buttons_good.append(lambda label=label: f"clicked: {label}")
print("SAHI :", [b() for b in buttons_good])

print("-" * 55)
# GOTCHA ka ulta ru: agar tum JAAN BOOJH KAR shared state chahte ho, late binding FAIDA hai
config = {"mode": "dev"}
def get_mode():
    return config["mode"]              # hamesha TAAZA value parhega
print("mode ab       :", get_mode())
config["mode"] = "prod"                # runtime par badal diya
print("badalne ke baad:", get_mode(), " <- late binding ki wajah se update mila")
"""),
md("""
### Interview tip (ye exact jawab yaad karlo)

*"Loop me lambda banaya to sab same value de rahe hain — kyun?"*

> *"Closure variable ko capture karta hai, value ko nahi (late binding). Loop khatam hone par us variable ki
> value aakhri hoti hai, is liye saare closures wahi parhte hain. Hal: `lambda i=i: ...` se default argument
> me value freeze karo, ya factory function / `functools.partial` se har closure ko apna scope do."*

**Yaad rakho:** `for` loop Python me **naya scope nahi banata** (JavaScript ke `let` ki tarah nahi).
Sirf functions, classes, aur comprehensions naya scope banate hain.
"""),
]

cells += [
md("""
---
## 6. Decorator — scratch se banate hain

**Decorator kya hai?** Ek function jo **doosra function leta hai**, usko wrap karta hai, aur ek **naya
function return** karta hai — original ka code chhue baghair uska behaviour badal deta hai.

**Kyun?** Cross-cutting concerns: logging, timing, caching, auth, retry, validation. Ye "kaam" har function
me copy-paste karne ke bajaye ek jagah likho aur `@` se laga do (DRY principle).

### Bunyadi shakal
```python
def decorator(func):            # 1. function leta hai
    def wrapper(*a, **kw):      # 2. wrapper banata hai
        # pehle kuch karo
        result = func(*a, **kw) # 3. asal function call
        # baad me kuch karo
        return result
    return wrapper              # 4. wrapper return
```

### `@` ka matlab
```python
@decorator              # bilkul barabar hai:
def f(): ...            # def f(): ...
                        # f = decorator(f)
```
Bas itna — `@` sirf **syntactic sugar** hai.
"""),
code("""
# ---- Step 1: BINA `@` ke, manually wrap karte hain ----

def shout(text):
    return text

def make_loud(func):
    # func ko lapet kar naya function banao
    def wrapper(text):
        result = func(text)              # asal function
        return result.upper() + "!!!"    # natija badal diya
    return wrapper

# Manual application -- yehi `@` andar karta hai
shout = make_loud(shout)                 # naam ko wrapper se rebind kiya
print("shout('salam ho') ->", shout("salam ho"))
print("shout ka __name__ ->", shout.__name__, " <- 'wrapper'! (masla, aage hal karenge)")
"""),
code("""
# ---- Step 2: wahi cheez `@` ke sath ----

def make_loud(func):
    def wrapper(text):
        return func(text).upper() + "!!!"
    return wrapper

@make_loud                     # == whisper = make_loud(whisper)
def whisper(text):
    return text

print("@ ke sath ->", whisper("dheere bolo"))

# Sabit karte hain ke @ aur manual barabar hain
def plain(text): return text
manual = make_loud(plain)
print("manual    ->", manual("dheere bolo"))
assert whisper("x") == manual("x")
"""),
code("""
# ---- Step 3: MASLA -- ye decorator sirf 1-argument functions par chalta hai ----

@make_loud
def join_words(a, b):          # do arguments
    return a + " " + b

try:
    join_words("assalam", "alaikum")
except TypeError as e:
    print("Masla ->", type(e).__name__, ":", e)
    print("Kyun? wrapper(text) sirf EK argument leta hai.")
    print("HAL:  wrapper(*args, **kwargs) -- agla section.")
"""),
]

cells += [
md("""
---
## 7. Generic decorator — `*args` / `**kwargs`

Har decorator ka wrapper **`*args, **kwargs`** lena chahiye taake wo **kisi bhi** signature ke function par
lag sake. Ye default template hai:

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        ...                                  # before
        result = func(*args, **kwargs)       # sab arguments pass-through
        ...                                  # after
        return result                        # return value bhool na jao!
    return wrapper
```

**Do sab se aam ghaltiyan:**
1. `*args, **kwargs` na lena → sirf ek signature par chalega
2. `return result` bhool jana → decorated function hamesha `None` dega
"""),
code("""
# ---- Generic version: kisi bhi signature par chalta hai ----

def loud(func):
    def wrapper(*args, **kwargs):            # SAB arguments accept
        result = func(*args, **kwargs)       # SAB arguments forward
        return str(result).upper() + "!!!"   # return LAZMI
    return wrapper

@loud
def one(a): return a

@loud
def two(a, b): return a + " " + b

@loud
def kw(name, greeting="hello"): return f"{greeting} {name}"

@loud
def no_args(): return "khali"

print("one     :", one("ek"))
print("two     :", two("do", "teen"))
print("kwargs  :", kw("ali", greeting="salam"))
print("no args :", no_args())
"""),
code("""
# ---- Ghalti #2 ka demo: `return` bhool jana ----

def broken_decorator(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)        # call kiya... magar RETURN nahi kiya!
    return wrapper

@broken_decorator
def add_nums(a, b):
    return a + b

print("broken:", add_nums(2, 3), " <- None! (return bhool gaye)")

def fixed_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)   # <- yehi ek lafz farq hai
    return wrapper

@fixed_decorator
def add_nums2(a, b):
    return a + b

print("fixed :", add_nums2(2, 3))
assert add_nums2(2, 3) == 5
"""),
]

cells += [
md("""
---
## 8. `functools.wraps` — kyun **lazmi** hai

Decorator lagane ke baad naam badal jata hai (`wrapper`), docstring gayab ho jati hai, signature
introspection tootti hai. Ye sirf "cosmetic" masla nahi:

- Debugging / traceback me ghalat naam
- `help()` bekaar
- Sphinx docs kharab
- **Framework tootna** — Flask routes, pytest fixtures, `functools.singledispatch` sab
  `__name__`/`__wrapped__` par depend karte hain
- Do decorated functions ka `__name__` same (`wrapper`) → Flask "duplicate endpoint" error deta hai

**Hal:** `@functools.wraps(func)` — ye `__name__`, `__doc__`, `__module__`, `__qualname__`,
`__annotations__`, `__dict__` copy karta hai aur `__wrapped__` set karta hai.
"""),
code("""
import functools
import inspect

# ---- BINA wraps ----
def no_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# ---- WRAPS ke SATH ----
def with_wraps(func):
    @functools.wraps(func)              # <- ek line, bara farq
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@no_wraps
def compute_tax(amount: float, rate: float = 0.17) -> float:
    '''Amount par tax nikalta hai (default 17% GST).'''
    return amount * rate

@with_wraps
def compute_tax2(amount: float, rate: float = 0.17) -> float:
    '''Amount par tax nikalta hai (default 17% GST).'''
    return amount * rate


print("BINA wraps:")
print("   __name__   :", compute_tax.__name__)
print("   __doc__    :", compute_tax.__doc__)
print("   signature  :", inspect.signature(compute_tax))
print("   annotations:", compute_tax.__annotations__)

print()
print("WRAPS ke sath:")
print("   __name__   :", compute_tax2.__name__)
print("   __doc__    :", compute_tax2.__doc__)
print("   signature  :", inspect.signature(compute_tax2))
print("   annotations:", compute_tax2.__annotations__)
print("   __wrapped__:", compute_tax2.__wrapped__.__name__, " <- asal function yahan mil jata hai")
"""),
md("""
### Output ka matlab

- Bina `wraps`: naam `wrapper`, docstring `None`, signature `(*args, **kwargs)` — sab maloomat gayab.
- `wraps` ke sath: sab kuch original jaisa, aur bonus `__wrapped__` se asal function bhi mil jata hai.

**Interview tip:** *"`functools.wraps` kya karta hai?"* → *"Wrapper par original function ki metadata
(`__name__`, `__doc__`, `__qualname__`, `__annotations__`, `__dict__`) copy karta hai aur `__wrapped__` set
karta hai — taake introspection, debugging, docs aur frameworks na tootein."*

**Rule:** Har decorator me `@functools.wraps(func)` likho. Koi exception nahi.
"""),
code("""
# ---- Real nuksan: bina wraps do functions ka naam same ho jata hai ----

@no_wraps
def route_home(): return "home"

@no_wraps
def route_about(): return "about"

print("bina wraps -> dono ka naam:", route_home.__name__, "aur", route_about.__name__)
print("Flask/Django is naam se endpoint register karte hain -> 'duplicate endpoint' error!")

@with_wraps
def route_home2(): return "home"

@with_wraps
def route_about2(): return "about"
print()
print("wraps ke sath -> ", route_home2.__name__, "aur", route_about2.__name__, " <- theek")
assert route_home2.__name__ != route_about2.__name__
"""),
]

cells += [
md("""
---
## 9. Decorator with arguments — 3 level nesting

Jab decorator ko khud configuration chahiye (`@repeat(3)`, `@retry(attempts=5)`), to ek **extra layer**
lagti hai:

```python
def repeat(times):                  # LEVEL 1: decorator ke arguments
    def decorator(func):            # LEVEL 2: asal decorator (function leta hai)
        @functools.wraps(func)
        def wrapper(*a, **kw):      # LEVEL 3: call ke arguments
            ...
        return wrapper
    return decorator
```

**Yaad rakhne ka tareeqa:** `@repeat(3)` me pehle `repeat(3)` **call** hota hai — wo ek **decorator**
return karta hai — phir wo decorator function par lagta hai. Yani:

```python
@repeat(3)
def f(): ...          # ==  f = repeat(3)(f)
```

Do brackets → do calls → teen levels.
"""),
code("""
# ---- Level-by-level: @repeat(times) ----

def repeat(times):
    # LEVEL 1: config (`times`) yahan capture hui
    def decorator(func):
        # LEVEL 2: asal function mila
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # LEVEL 3: har call par chalta hai
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

tick = {"n": 0}          # deterministic "random" (test pass hone ke liye)

@repeat(3)
def roll_dice(sides=6):
    tick["n"] += 1
    return tick["n"] % sides + 1

print("roll_dice():", roll_dice())          # 3 baar chala -> 3 results ki list
print("__name__  :", roll_dice.__name__, " <- wraps ki wajah se sahi")
assert len(roll_dice()) == 3

# Manual equivalent -- sabit karte hain
def greet_plain(name): return f"hi {name}"
greet3 = repeat(3)(greet_plain)              # do calls, exactly jaise @ karta hai
print("manual    :", greet3("Ali"))
assert greet3("Ali") == ["hi Ali", "hi Ali", "hi Ali"]
"""),
code("""
# ---- Bohat aam pattern: decorator jo arguments KE SATH aur BINA dono chale ----
# (jaise @cache aur @cache(maxsize=100) dono kaam karte hain)

def tag(func=None, *, name=None, upper=False):
    # Trick: `func` None hai to iska matlab arguments ke sath call hua hai
    def decorator(f):
        label = name or f.__name__
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            text = f"[{label}] {result}"
            return text.upper() if upper else text
        return wrapper

    if func is None:
        return decorator          # @tag(name="x") ki soorat
    return decorator(func)        # @tag (bina bracket) ki soorat

@tag                               # bina bracket
def a(): return "alpha"

@tag()                             # khali bracket
def b(): return "beta"

@tag(name="CUSTOM", upper=True)    # arguments ke sath
def c(): return "gamma"

print("@tag            :", a())
print("@tag()          :", b())
print("@tag(name=,upper=):", c())
assert a() == "[a] alpha" and b() == "[b] beta" and c() == "[CUSTOM] GAMMA"
"""),
md("""
### Gotcha: bracket bhool jana

```python
@repeat            # ❌ times = function ban gaya! (galat)
def f(): ...

@repeat(3)         # ✅
def f(): ...
```

Pehli soorat me `repeat` ko `func` mil gaya `times` ki jagah, aur `decorator` return hua — yani `f` ab
ek **decorator** ban gaya, function nahi. Error bohat confusing aata hai. Isi liye upar wala
`func=None, *, ...` pattern (dono soorat support karna) popular hai.
"""),
code("""
# ---- Bracket bhoolne ka live demo ----

@repeat                    # GALTI: bracket nahi (times = roll_twice function ban gaya)
def roll_twice():
    return 7

print("type(roll_twice):", type(roll_twice).__name__, " <- function hai magar...")
try:
    roll_twice()           # ye ab `decorator` hai, jisko `func` chahiye
except TypeError as e:
    print("call karne par ->", type(e).__name__, ":", e)
    print("HAL: @repeat(2) likho.")
"""),
]

cells += [
md("""
---
## 10. Stacked decorators — order kya hota hai?

```python
@A
@B
@C
def f(): ...
```

**Application (lagne) ka order: NEECHE se UPAR (bottom-up)**
```
f = A(B(C(f)))
```
Yani `C` sab se pehle lagta hai (function ke sab se qareeb), `A` sab se aakhir (sab se bahar).

**Execution (chalne) ka order: BAHAR se ANDAR**
Call par: `A` ka wrapper → `B` ka wrapper → `C` ka wrapper → asal function → phir wapis
`C` → `B` → `A`.

Yani **onion (pyaz) model**: `A` sab se bahar ki layer hai.
"""),
code("""
# ---- Order ko print se sabit karte hain ----

def deco_A(func):
    print("   [apply] A lag raha hai")
    @functools.wraps(func)
    def wrapper(*a, **kw):
        print("      [enter] A")
        r = func(*a, **kw)
        print("      [exit ] A")
        return r
    return wrapper

def deco_B(func):
    print("   [apply] B lag raha hai")
    @functools.wraps(func)
    def wrapper(*a, **kw):
        print("      [enter] B")
        r = func(*a, **kw)
        print("      [exit ] B")
        return r
    return wrapper

def deco_C(func):
    print("   [apply] C lag raha hai")
    @functools.wraps(func)
    def wrapper(*a, **kw):
        print("      [enter] C")
        r = func(*a, **kw)
        print("      [exit ] C")
        return r
    return wrapper

print("DEFINE karte waqt (apply order -- NEECHE se UPAR):")
@deco_A
@deco_B
@deco_C
def target():
    print("      [BODY ] asal function")
    return "done"

print()
print("CALL karte waqt (execution -- BAHAR se ANDAR aur wapis):")
result = target()
print("result:", result)
"""),
md("""
### Output ka matlab

```
apply    : C, B, A          (neeche se upar)
execution: A -> B -> C -> BODY -> C -> B -> A   (pyaz ki layers)
```

### Order kab **matter** karta hai? (interview me poocha jata hai)

```python
@app.route("/admin")     # 1. routing sab se bahar
@login_required          # 2. phir auth check
@cache(60)               # 3. phir cache
def admin_panel(): ...
```
Yahan order **bilkul** matter karta hai:
- Agar `@cache` `@login_required` ke **upar** hota, to cached response **auth check se pehle** mil jata →
  **security hole**! Unauthorized user ko dusre ka cached data mil sakta hai.
- `@timer` `@retry` ke upar → poore retry ka total time. Neeche → har attempt ka time.

**Rule of thumb:** Jo cheez **hamesha** chalni chahiye (auth, logging) usko **bahar** (upar) rakho.
Jo cheez **skip** kar sakti hai (cache) usko **andar** (neeche).
"""),
code("""
# ---- Order ka farq: @timer + @retry ----
import time

def timer_simple(func):
    @functools.wraps(func)
    def wrapper(*a, **kw):
        t0 = time.perf_counter()
        r = func(*a, **kw)
        print(f"      [timer] {func.__name__} ne {(time.perf_counter()-t0)*1000:.1f} ms liye")
        return r
    return wrapper

def retry_simple(attempts=3, delay=0.005):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*a, **kw):
            for n in range(1, attempts + 1):
                try:
                    return func(*a, **kw)
                except ValueError:
                    if n == attempts:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

state = {"n": 0}
def flaky():
    state["n"] += 1
    time.sleep(0.005)
    if state["n"] < 3:
        raise ValueError("fail")
    return "ok"

print("timer BAHAR (@timer upar) -> POORE retry ka total time:")
state["n"] = 0
f1 = timer_simple(retry_simple()(flaky))
print("   result:", f1())

print()
print("timer ANDAR (@timer neeche) -> HAR attempt ka alag time:")
state["n"] = 0
f2 = retry_simple()(timer_simple(flaky))
print("   result:", f2())
"""),
]

cells += [
md("""
---
## 11. Class-based decorators aur method decorators

### Class-based decorator
Agar decorator ko **state** rakhni ho (call count, cache, rate-limit window) to class zyada saaf hai:
`__init__` me function lo, `__call__` me wrapper ka kaam karo.

```python
class MyDeco:
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)   # `wraps` ka class version
    def __call__(self, *a, **kw):
        return self.func(*a, **kw)
```

**Faida:** state explicit (`self.count`), inspect karna aasan, methods add kar sakte ho (`reset()`).
**Nuksan:** methods par lagane me masla aata hai (descriptor protocol chahiye) — neeche dekhenge.
"""),
code("""
# ---- Class-based decorator: call counting with state ----

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)    # <- `functools.wraps` ka class version
        self.func = func
        self.count = 0                           # state EXPLICIT hai

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"   call #{self.count} -> {self.func.__name__}")
        return self.func(*args, **kwargs)

    def reset(self):
        # Class hone ka faida: extra methods de sakte ho
        old, self.count = self.count, 0
        return old

@CountCalls
def fetch_data(key):
    return f"data[{key}]"

print(fetch_data("a"))
print(fetch_data("b"))
print(fetch_data("c"))
print("total calls:", fetch_data.count)
print("reset()    :", fetch_data.reset(), "-> ab", fetch_data.count)
print("__name__   :", fetch_data.__name__, " (update_wrapper ki wajah se)")
assert fetch_data.count == 0
"""),
code("""
# ---- Class-based decorator ka MASLA: methods par lagane par ----

class SimpleDeco:
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)
    def __call__(self, *a, **kw):
        return self.func(*a, **kw)

class Service:
    @SimpleDeco
    def ping(self):        # `self` kaun dega?
        return "pong"

try:
    Service().ping()
except TypeError as e:
    print("Masla ->", type(e).__name__, ":", e)
    print("Kyun? SimpleDeco ek plain object hai, descriptor nahi -> `self` bind nahi hota.")
"""),
code("""
# ---- HAL 1: __get__ add karo (descriptor protocol) ----

class BoundDeco:
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __call__(self, *a, **kw):
        return self.func(*a, **kw)

    def __get__(self, obj, objtype=None):
        # Jab attribute class/instance se access ho, ye chalta hai.
        # partial se `obj` (yani self) ko bind kar dete hain.
        if obj is None:
            return self
        return functools.partial(self.__call__, obj)

class Service2:
    @BoundDeco
    def ping(self):
        return "pong"

print("HAL 1 (descriptor):", Service2().ping())

# ---- HAL 2 (aasan aur behtar): function-based decorator use karo ----
def log_call(func):
    @functools.wraps(func)
    def wrapper(self, *a, **kw):        # `self` bas ek normal argument hai
        print(f"   [log] {type(self).__name__}.{func.__name__} chala")
        return func(self, *a, **kw)
    return wrapper

class Service3:
    def __init__(self, name):
        self.name = name

    @log_call
    def ping(self):
        return f"pong from {self.name}"

    @log_call
    def echo(self, msg, times=1):
        return (msg + " ") * times

s = Service3("api-1")
print("HAL 2 (function deco):", s.ping())
print("                     ", s.echo("hi", times=3).strip())
print()
print("SEEKH: methods ke liye function-based decorator hi use karo -- `self` khud handle ho jata hai.")
"""),
md("""
### Method decorator ka order gotcha: `@staticmethod` / `@classmethod` / `@property`

Ye "special" decorators **sab se bahar (upar)** hone chahiye:

```python
class C:
    @staticmethod          # ✅ upar
    @my_decorator
    def f(): ...

    @property              # ✅ upar
    @my_decorator
    def value(self): ...
```

Kyun? Kyunki `staticmethod`/`classmethod`/`property` **descriptor** objects return karte hain, plain
function nahi. Agar wo neeche hon to tumhara decorator ek descriptor object ko wrap karega — jo callable
nahi hota (Python 3.10+ me `staticmethod` callable ban gaya hai, magar `classmethod`/`property` phir bhi
nahi).
"""),
code("""
# ---- staticmethod / property ke sath sahi order ----

def announce(func):
    # getattr fallback: agar `func` plain function na ho (property/classmethod object)
    # to bhi crash na ho -- ye defensive habit decorators me kaam aati hai
    label = getattr(func, "__name__", type(func).__name__)

    @functools.wraps(func)
    def wrapper(*a, **kw):
        r = func(*a, **kw)
        print(f"   [announce] {label} -> {r}")
        return r
    return wrapper

class Config:
    def __init__(self, raw):
        self._raw = raw

    @staticmethod             # SAHI: staticmethod sab se upar
    @announce
    def version():
        return "1.4.2"

    @property                 # SAHI: property sab se upar
    @announce
    def size(self):
        return len(self._raw)

    @classmethod              # SAHI: classmethod sab se upar
    @announce
    def default(cls):
        return cls("abc")

print("staticmethod:", Config.version())
c = Config("hello world")
print("property    :", c.size)
print("classmethod :", Config.default()._raw)

print()
# GALAT order ka demo: announce ne `property` OBJECT ko wrap kar liya
class Bad:
    @announce                 # GALAT: ye upar nahi hona chahiye
    @property
    def size(self):
        return 42

b = Bad()
print("Bad().size ka type:", type(b.size).__name__, " <- property nahi, bound method ban gaya!")
try:
    b.size()                  # wrapper chalega -> andar property object ko call karega
except TypeError as e:
    print("galat order ->", type(e).__name__, ":", e)
    print("HAL: @property ko SAB SE UPAR rakho.")
"""),
]

# ---- CHUNK MARKER ----

save(PATH, cells)


