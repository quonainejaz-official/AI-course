import sys
sys.path.insert(0, r"c:\Users\Quonain\MyFiles\Artificial-Intelligence\_tools")
from nbgen import md, code, save

cells = []

# ============================================================
# 1. TITLE + ROADMAP + PREREQUISITES
# ============================================================
cells.append(md("""
# 01 — Python Introduction and Setup

**Level:** Beginner (Starting from zero)
**Series:** Python Basics

## What will you learn in this notebook (roadmap)

1. What is Python, why was it created, and where is it used today
2. Interpreter vs Compiler — what Python actually does internally (bytecode, `.pyc`, `__pycache__`)
3. CPython vs PyPy vs Jython vs IronPython vs MicroPython
4. `.py` script vs `.ipynb` notebook — when to use which
5. Jupyter cell types and important keyboard shortcuts
6. `print()` function and all its parameters (`sep`, `end`, `file`, `flush`)
7. Comments vs Docstrings
8. Indentation rules and `IndentationError`
9. PEP 8 essentials (naming, line length, imports, blank lines)
10. Keywords and identifier rules
11. Dynamic typing
12. `type()` and `id()` — object identity
13. `help()` and `dir()`
14. pip basics (install/uninstall/venv/requirements.txt) — conceptual level
15. Python 2 vs Python 3 differences

Then: **Common Mistakes**, **Real-World Problems**, **LeetCode (Easy x2)**,
**Interview Q&A**, **Practice Exercises**, and a **Cheat-sheet**.

## Prerequisites

- No programming background required — starting from zero is fine.
- Python 3.x should be installed on your computer (this notebook targets Python 3.14;
  modern features like `match/case` are available).
- Jupyter (VS Code or JupyterLab) should be running so you can execute cells.

> **Golden rule:** Run this notebook from top to bottom (in order). Each cell may depend on
> previous cells (variables, imports, etc.), just like in a real script.
"""))

# ============================================================
# 2. PYTHON KYA HAI AUR KYUN
# ============================================================
cells.append(md("""
## 1. Python Kya Hai Aur Kyun

**Kya hai:** Python ek **high-level, general-purpose, interpreted** programming language hai.
Isay **Guido van Rossum** ne 1989 me design karna shuru kiya aur pehli release **1991** me aayi
(Python 0.9.0). Naam "Monty Python's Flying Circus" (British comedy show) se liya gaya hai —
snake se koi lena dena nahi tha originally, lekin logo ka snake logo bohat mashhoor ho gaya.

Aaj Python ko **Python Software Foundation (PSF)** — ek non-profit organization — maintain karti
hai. Language ka development process **PEPs (Python Enhancement Proposals)** ke through hota hai.

**Kyun / kahan use hota hai:**
- **Web development** — Django, Flask, FastAPI
- **Data Science / Machine Learning / AI** — pandas, numpy, PyTorch, TensorFlow
- **Automation / Scripting** — system admin scripts, file processing
- **Backend APIs, DevOps tooling, testing frameworks**
- **Education** — beginner-friendly syntax hone ki wajah se universities me first language
  ke taur par bohat use hoti hai

**Kyun itni popular hai:**
- Syntax English jaisi readable hai (semicolons, curly braces ki zaroorat nahi)
- Bohat bara standard library ("batteries included" philosophy)
- Huge community aur third-party packages (PyPI par 500,000+ packages)
- "Glue language" — C/C++/Java/Rust jaisi languages ke sath easily integrate hoti hai

**Interview tip:** Agar poocha jaye "Python interpreted hai ya compiled?" — seedha jawab yeh hai ke
Python pehle source code ko **bytecode** me compile karta hai, phir woh bytecode ek **virtual
machine (PVM)** interpret karti hai. Yeh agla section detail me samjhata hai.
"""))

cells.append(code("""
# Chhota "environment teaser" — aage detail me aayega, abhi bas dekh lete hain
import sys
import platform

print("Python version (full string):", sys.version)
print("Version info tuple         :", sys.version_info)
print("Sirf major.minor           :", f"{sys.version_info.major}.{sys.version_info.minor}")
print("Implementation (CPython?)  :", platform.python_implementation())

# sys.getsizeof() batata hai ke object memory me kitni jagah (bytes) le raha hai
print()
print("sys.getsizeof(10)      ->", sys.getsizeof(10), "bytes")
print("sys.getsizeof('hello') ->", sys.getsizeof("hello"), "bytes")
print("sys.getsizeof([1,2,3]) ->", sys.getsizeof([1, 2, 3]), "bytes")
"""))

# ============================================================
# 3. INTERPRETER VS COMPILER
# ============================================================
cells.append(md("""
## 2. Interpreter vs Compiler — Python "Andar Se" Kya Karta Hai

**Kya hai:**
- **Compiler:** poora source code ek hi baar machine code me convert karta hai, phir woh binary
  chalta hai (C, C++, Rust jaisi languages).
- **Interpreter:** code ko line-by-line (ya chunk-by-chunk) padh kar turant execute karta hai.

**Python dono thora sa hai** — isay "compiled + interpreted" kehna zyada sahi hai:

1. Jab tum `python script.py` chalate ho, Python pehle source (`.py`) ko **bytecode** (`.pyc`)
   me compile karta hai — yeh low-level instructions hoti hain (machine code nahi, CPU-specific
   nahi).
2. Yeh bytecode phir **Python Virtual Machine (PVM)** ke andar interpret hoti hai.
3. Agar file ko **module** ke taur par import kiya jaye, Python is bytecode ko `__pycache__`
   folder me cache kar leta hai (`.pyc` files) taake agli baar dobara compile na karna pare
   (jab tak source file change na ho).

**Kyun important hai:** Isi wajah se Python thora slow hoti hai C/C++ ke muqable (extra VM layer),
lekin development speed aur readability me fayda deti hai.

**Interview tip:** "Python compiled hai ya interpreted?" — dono! Source → bytecode (compile step,
automatic aur invisible) → PVM interpret karti hai bytecode ko.
"""))

cells.append(code("""
# Demo: Python source ko bytecode (.pyc) me compile karke __pycache__ dekhte hain
import tempfile
import os
import py_compile

# Ek temporary folder banate hain (koi real project folder ganda nahi hoga)
tmp_dir = tempfile.mkdtemp(prefix="py_bytecode_demo_")

source_path = os.path.join(tmp_dir, "sample_module.py")
with open(source_path, "w", encoding="utf-8") as f:
    f.write("def greet(name):\\n    return 'Hello, ' + name\\n")

# py_compile.compile() source file ko .pyc bytecode me convert karta hai
compiled_path = py_compile.compile(source_path, doraise=True)

pycache_dir = os.path.join(tmp_dir, "__pycache__")
print("Source (.py) file   :", source_path)
print("Compiled (.pyc) file:", compiled_path)
print("__pycache__ folder ban gaya?:", os.path.isdir(pycache_dir))
print("__pycache__ ke andar files  :", os.listdir(pycache_dir))
"""))

cells.append(code("""
# Demo: dis module se dekhte hain ke Python function ke andar kaisi bytecode instructions hoti hain
import dis


def add_numbers(a, b):
    # Yeh simple function — iski bytecode dekhenge
    return a + b


print("add_numbers() ki bytecode instructions:")
dis.dis(add_numbers)
# Har line ek "instruction" hai jo PVM (Python Virtual Machine) execute karti hai
# LOAD_FAST = variable load karo, BINARY_OP = jama karo, RETURN_VALUE = wapas bhejo (roughly)
"""))

# ============================================================
# 4. CPYTHON VS PYPY VS JYTHON VS IRONPYTHON VS MICROPYTHON
# ============================================================
cells.append(md("""
## 3. CPython vs PyPy vs Jython vs IronPython vs MicroPython

"Python" ek **language specification** hai — usay implement karne ke multiple tareeqe (interpreters)
hain:

| Implementation | Likha kis me gaya | Khaas baat |
|---|---|---|
| **CPython** | C | **Default / official** implementation — jo tum normally `python.exe` chalate ho, yehi hai |
| **PyPy** | RPython (Python subset) | **JIT compiler** ki wajah se kaafi hot loops me tez hota hai |
| **Jython** | Java | Java Virtual Machine (JVM) par chalta hai, Java libraries ke sath direct interop |
| **IronPython** | C# | .NET / CLR par chalta hai, C# libraries ke sath interop |
| **MicroPython** | C (minimal) | Microcontrollers / embedded devices (Raspberry Pi Pico waghera) ke liye chhota version |

**Kyun important hai:** `platform.python_implementation()` se pata chalta hai tum konsa
implementation use kar rahe ho — yeh production debugging aur performance tuning me kaam aata hai
(masalan PyPy JIT ki wajah se kabhi kabhi 5-10x faster hota hai loops par).

**Interview tip:** Agar poocha jaye "CPython aur Python me farq?" — Python language hai (spec),
CPython uska sabse common **interpreter/implementation** hai (C me likha gaya).
"""))

cells.append(code("""
# Har implementation ka ek chhota static "fact sheet" — reference ke taur par
implementations = {
    "CPython": "Official/default, C me likha, sab jagah standard",
    "PyPy": "JIT-compiled, tez hota hai (CPU-heavy loops me)",
    "Jython": "JVM par chalta hai, Java libs ke sath interop",
    "IronPython": ".NET/CLR par chalta hai, C# libs ke sath interop",
    "MicroPython": "Microcontrollers ke liye chhota/lightweight version",
}

for name, note in implementations.items():
    print(f"{name:12} -> {note}")

print()
print("Yeh machine chala rahi hai:", __import__("platform").python_implementation())
"""))

# ============================================================
# 5. .py VS .ipynb
# ============================================================
cells.append(md("""
## 4. `.py` vs `.ipynb` — Kab Konsa Use Karein

| | `.py` (plain script) | `.ipynb` (Jupyter Notebook) |
|---|---|---|
| Format | Plain text Python code | JSON file (cells ka structure) |
| Execution | Poori file ek sath chalti hai (top to bottom) | Cell-by-cell, interactive, order tumhare control me |
| State | Har run par fresh | Cells ke beech variables/state persist hoti hai (jab tak kernel restart na ho) |
| Best for | Production code, scripts, packages, automation, `.py` files jo import honge | Exploration, data analysis, teaching, prototyping, visualization |
| Version control | Git diff clean hota hai | JSON hone ki wajah se diff messy ho sakta hai (outputs bhi save hote hain) |
| Deployment | Seedha production me chal sakta hai | Normally production me directly nahi chalate (convert karte hain `.py` me) |

**Kab `.py` use karein:** jab code ko reuse karna ho, tests likhne hon, ya production deploy karna ho.

**Kab `.ipynb` use karein:** jab data explore karna ho, results turant dekhne hon, ya teaching/demo
ka context ho (jaisa yeh notebook khud hai!).

**Common mistake:** Notebook me cells ko out-of-order chalana (masalan cell 5 phir cell 2) —
isse "it worked on my machine but fails top-to-bottom" wala bug aata hai. Hamesha **Restart &
Run All** karke check karo.
"""))

# ============================================================
# 6. JUPYTER CELL TYPES + SHORTCUTS
# ============================================================
cells.append(md("""
## 5. Jupyter Cell Types aur Keyboard Shortcuts

**Cell types:**

| Cell Type | Kaam |
|---|---|
| **Code** | Python code likhte ho, `Shift+Enter` se run hota hai, output neeche aata hai |
| **Markdown** | Text/documentation — headings, bullets, tables, LaTeX formulas (jaisi yeh cell hai) |
| **Raw** | Bilkul plain text — kisi bhi format me convert nahi hota (rare use, nbconvert ke liye) |

**Zaroori keyboard shortcuts (Command mode — cell select ho lekin edit na ho rahi ho):**

| Shortcut | Kaam |
|---|---|
| `Enter` | Edit mode me jao (cell ke andar type karne ke liye) |
| `Esc` | Command mode me wapas aao |
| `Shift + Enter` | Cell run karo, agli cell select ho jaye (ya nayi ban jaye) |
| `Ctrl + Enter` | Cell run karo, wahi cell selected rahe |
| `Alt + Enter` | Cell run karo aur neeche nayi cell insert ho jaye |
| `A` | Upar (Above) nayi cell insert karo |
| `B` | Neeche (Below) nayi cell insert karo |
| `D, D` (do baar D) | Selected cell delete karo |
| `M` | Cell ko Markdown bana do |
| `Y` | Cell ko Code bana do |
| `Z` | Undo cell operation |
| `Ctrl + Shift + -` | Edit mode me cursor position par cell ko split karo |

**Interview tip:** Yeh purely tooling knowledge hai — interviews me kam poocha jata hai, lekin
day-to-day productivity ke liye bohat zaroori hai. Muscle memory bana lo.
"""))

# ============================================================
# 7. print() — SAB PARAMETERS
# ============================================================
cells.append(md("""
## 6. `print()` Function — Sab Parameters

**Kya hai:** `print()` built-in function hai jo values ko standard output (ya kisi bhi file-like
object) par likhta hai.

**Syntax:**
```python
print(*objects, sep=' ', end='\\n', file=sys.stdout, flush=False)
```

- `*objects` — jitni marzi values, comma se separate karke
- `sep` — objects ke beech separator (default: single space `' '`)
- `end` — line ke aakhir me kya lagana hai (default: newline `'\\n'`)
- `file` — kahan likhna hai (default: `sys.stdout`; `sys.stderr` ya koi file-like object bhi de sakte ho)
- `flush` — buffer ko turant flush karna hai ya nahi (default: `False`)

**Interview tip:** `print()` Python 3 me hamesha ek **function** hai (call karte waqt parentheses
lazmi). Python 2 me yeh ek **statement** tha — `print "hello"` — is farq par baad me alag section hai.
"""))

cells.append(code("""
# 1) Multiple objects + custom sep
print("Ali", "Sara", "Bilal")                 # default sep = space
print("Ali", "Sara", "Bilal", sep=", ")        # comma-space separator
print("2026", "07", "29", sep="-")             # date jaisa format bana sakte ho
print(1, 2, 3, 4, sep=" | ")
"""))

cells.append(code("""
# 2) end parameter — line ke aakhir me kya print ho
print("Loading", end="")
print(".", end="")
print(".", end="")
print(".", end="\\n")   # ab newline lagayenge
print("Done!")

print()
# end use karke ek hi line me loop ka output print karna (bina extra newlines ke)
for i in range(5):
    print(i, end=" -> " if i < 4 else "\\n")
"""))

cells.append(code("""
# 3) file parameter — output kahan bhejna hai
import sys
import io

# (a) sys.stderr par likhna (error/log messages ke liye common pattern)
print("Yeh ek warning jaisi cheez hai", file=sys.stderr)

# (b) io.StringIO() ek "in-memory file" hai — bilkul real file jaisa behave karta hai
#     lekin disk par kuch nahi likhta. Yahan hum REAL file path use NAHI kar rahe.
memory_file = io.StringIO()
print("Line 1: server started", file=memory_file)
print("Line 2: request processed", file=memory_file)

captured_text = memory_file.getvalue()
print("io.StringIO() me capture hua text:")
print(captured_text)
"""))

cells.append(code("""
# 4) flush parameter — output buffer ko turant "push" karna
# Normally Python output buffer karta hai (especially jab terminal ki bajaye pipe/file ho).
# flush=True ka matlab: "abhi ke abhi likh do, buffer me mat roko".
print("Processing step 1...", flush=True)
print("Processing step 2...", flush=True)
print("Done.", flush=True)

# Kahan kaam aata hai: long-running scripts me progress dikhane ke liye,
# ya jab output ko dusre process (pipe) me turant bhejna ho.
print()
print("Gotcha: flush=True sirf timing (kab dikhta hai) affect karta hai, VALUE nahi.")
"""))

# ============================================================
# 8. COMMENTS VS DOCSTRINGS
# ============================================================
cells.append(md("""
## 7. Comments vs Docstrings

**Kya hai:**
- **Comment (`#`)** — code ke andar note jo Python bilkul ignore kar deta hai (runtime par
  koi wajood nahi). Sirf humans ke liye.
- **Docstring** (triple-quoted string) — function/class/module ke **pehle statement** ke taur
  par likha gaya triple-quoted string. Yeh runtime par `__doc__` attribute me store hota hai
  aur `help()` isay dikhata hai.

**Syntax:**
```python
# single-line comment

# Python me "block comment" ka koi alag syntax nahi hai —
# log consecutive # lines use karte hain (jaisa yeh 3 lines hain)

def kaam(x):
    \"\"\"Yeh function ka docstring hai — help(kaam) isay dikhayega.\"\"\"
    return x
```

**Interview tip:** Docstring aur comment ka bunyadi farq — docstring **runtime object** hai
(`func.__doc__` se access ho sakta hai, documentation tools isay parse karte hain), comment
sirf source code me hota hai, compile hote hi ghayab.
"""))

cells.append(code("""
# Yeh ek single-line comment hai — Python isay ignore karta hai
x = 5  # inline comment: x ko 5 assign kar rahe hain

# Yeh
# "block style"
# comments hain (bas consecutive # lines)


def calculate_area(length, width):
    \"\"\"Rectangle ka area calculate karta hai.

    Parameters:
        length (float): Rectangle ki lambai
        width (float): Rectangle ki chorai

    Returns:
        float: length * width
    \"\"\"
    return length * width


class BankAccount:
    \"\"\"Simple bank account ko represent karne wali class.\"\"\"

    def deposit(self, amount):
        \"\"\"Account me paisay deposit karta hai.\"\"\"
        return amount


# Docstring runtime par __doc__ attribute me store hota hai
print("Function docstring:", calculate_area.__doc__.strip().split("\\n")[0])
print("Class docstring   :", BankAccount.__doc__)
print("Method docstring  :", BankAccount.deposit.__doc__)

print()
print(calculate_area(4, 5))  # function normally use bhi ho sakta hai
"""))

# ============================================================
# 9. INDENTATION RULES
# ============================================================
cells.append(md("""
## 8. Indentation Rules

**Kya hai:** Python me curly braces `{}` ki bajaye **indentation** (whitespace) se code blocks
define hote hain. Yeh language ka core design decision hai (readability ke liye).

**Rules:**
- Standard convention: **4 spaces** per indentation level (PEP 8 recommend karta hai).
- Ek hi block ke andar **consistent** indentation honi chahiye (sab lines same level par).
- **Tabs aur spaces mix karna** dangerous hai — Python 3 me yeh error deta hai agar ambiguous ho.
- Colon (`:`) ke baad agli line indented honi chahiye (if/for/while/def/class waghera ke baad).

**Common mistakes:**
- Colon ke baad indent bhool jana → `IndentationError`
- Tabs aur spaces mix karna → `TabError`
- Editor settings alag hona (kuch editors tab ko 4 spaces dikhate hain, kuch 8) — isliye
  hamesha ek hi style (spaces) use karo, poori file me.

**Interview tip:** "Python whitespace-sensitive kyun hai?" — readability enforce karne ke liye;
Guido van Rossum ka design philosophy tha ke code ka visual structure hi uska logical structure
ho, taake alag developers ka code consistent dikhe.
"""))

cells.append(code("""
# Sahi (correct) indentation ka example
def check_number(n):
    if n > 0:
        result = "positive"
    elif n < 0:
        result = "negative"
    else:
        result = "zero"
    return result


for value in [5, -3, 0]:
    print(value, "->", check_number(value))
"""))

cells.append(code("""
# IndentationError demo — jaan boojh kar bad code, isliye try/except + compile() use kar rahe hain
# compile() source string ko bytecode me compile karne ki koshish karta hai (bina chalaye)
bad_code = "def broken():\\nprint('galat indent, colon ke baad indent nahi hai')\\n"

try:
    compile(bad_code, "<bad_snippet>", "exec")
except IndentationError as e:
    print("IndentationError pakad liya:", e)

print()

# TabError demo — tab aur spaces mix karne se ambiguous indentation
mixed_tabs_and_spaces = "if True:\\n\\tx = 1\\n        y = 2\\n"

try:
    compile(mixed_tabs_and_spaces, "<mixed_tabs>", "exec")
except TabError as e:
    print("TabError pakad liya:", e)
except IndentationError as e:
    print("IndentationError pakad liya:", e)
"""))

# ============================================================
# 10. PEP 8 ESSENTIALS
# ============================================================
cells.append(md("""
## 9. PEP 8 Essentials — Python Ka Official Style Guide

**Kya hai:** PEP 8 Python code likhne ka **official style guide** hai — taake sab ka code ek
jaisa consistent dikhe.

**Zaroori rules:**

| Cheez | Convention | Example |
|---|---|---|
| Variables/functions | `snake_case` | `total_amount`, `calculate_tax()` |
| Constants | `UPPER_CASE` | `MAX_RETRIES = 5` |
| Classes | `PascalCase` (CapWords) | `class BankAccount:` |
| "Private" (convention) | leading underscore | `_internal_value` |
| Line length | Max **79 chars** (kai teams 99-100 tak relax karte hain) | — |
| Imports | Top of file, order: stdlib → third-party → local, ek line par ek import (recommended) | `import os` phir `import numpy` phir `from myapp import utils` |
| Blank lines | Functions/classes ke beech 2 blank lines (top-level par), methods ke beech 1 | — |
| Indentation | 4 spaces, tabs nahi | — |

**Good vs Bad example:**
```python
# Good (PEP 8)
MAX_RETRIES = 3

def calculate_total(price, quantity):
    return price * quantity


# Bad (PEP 8 violations)
maxretries=3
def CalculateTotal(Price,Quantity):
        return Price*Quantity   # inconsistent indent + no spaces + wrong naming
```

**Interview tip:** PEP 8 rules "enforced" nahi hoti Python interpreter se (code chal jayega),
lekin linters (`flake8`, `pylint`) aur formatters (`black`) isay check karte hain — professional
teams me CI pipeline me yeh checks lazmi hote hain.
"""))

cells.append(code("""
# PEP 8-compliant naming demo (yeh sab chalti hai, bas style ka farq hai)

MAX_RETRIES = 3          # constant -> UPPER_CASE
default_timeout = 30      # variable -> snake_case
_cache = {}                # "private" convention -> leading underscore


class OrderProcessor:      # class -> PascalCase
    \"\"\"Order processing ka simple example (naming convention demo).\"\"\"

    def process_order(self, order_id):   # method -> snake_case
        return f"Processing order #{order_id}"


processor = OrderProcessor()
print(processor.process_order(101))
print("MAX_RETRIES:", MAX_RETRIES)
print("default_timeout:", default_timeout)

# Non-PEP8 (bad) style — yeh bhi chalta hai, Python isay reject nahi karta,
# lekin professional codebase me review me reject ho jayega
BadStyleVariable = "yeh chalega lekin convention ke khilaf hai"
print(BadStyleVariable)
"""))

# ============================================================
# 11. KEYWORDS AUR IDENTIFIERS
# ============================================================
cells.append(md("""
## 10. Keywords Aur Identifiers Ke Rules

**Kya hai:**
- **Keywords** — Python ke reserved words jinka special meaning hai (`if`, `for`, `class`,
  `return` waghera) — inhe variable/function name ke taur par use nahi kar sakte.
- **Soft keywords** — context-dependent keywords (`match`, `case`, `type`, `_`) — kuch jagah
  keyword hain, baaki jagah normal identifier ban sakte hain.
- **Identifier** — variable, function, class waghera ka **naam**.

**Identifier rules:**
1. Letters (a-z, A-Z), digits (0-9), aur underscore (`_`) allowed hain.
2. **Number se shuru nahi ho sakta** (`2fast` invalid).
3. Keywords use nahi kar sakte (`class`, `for` waghera invalid as names).
4. Case-sensitive hai (`Name` aur `name` alag identifiers hain).
5. Special characters (`-`, `@`, space) allowed nahi.

**Interview tip:** `str.isidentifier()` sirf **syntax** check karta hai (valid naam ban sakta hai
ya nahi) — yeh keyword hai ya nahi woh nahi batata. Iske liye `keyword.iskeyword()` chahiye. Dono
saath use karo real validation ke liye.
"""))

cells.append(code("""
import keyword

print("Total hard keywords:", len(keyword.kwlist))
print(keyword.kwlist)
print()
print("Soft keywords (context-dependent):", keyword.softkwlist)
"""))

cells.append(code("""
import keyword

candidates = ["my_var", "2fast", "class", "_private", "my-var", "myVar2", "for", "match", "total_amount"]

print(f"{'name':15} {'isidentifier':13} {'iskeyword':10} usable_as_name")
for name in candidates:
    valid_syntax = name.isidentifier()
    is_kw = keyword.iskeyword(name)
    usable = valid_syntax and not is_kw
    print(f"{name!r:15} {str(valid_syntax):13} {str(is_kw):10} {usable}")
"""))

# ============================================================
# 12. DYNAMIC TYPING
# ============================================================
cells.append(md("""
## 11. Dynamic Typing

**Kya hai:** Python **dynamically typed** language hai — matlab variable ki type runtime par
decide hoti hai, aur ek hi variable ko baar baar **rebind** kiya ja sakta hai different types se.

Yeh mindset zaroori hai: variable ek **label/name** hai jo kisi object ki taraf point karta hai —
variable khud ka koi "type" nahi hota, **object** ka type hota hai.

**Kyun important hai:** C/Java jaisi statically-typed languages me variable declare karte waqt
type fix karni parti hai (`int x = 5;`) aur badalna mushkil hai. Python me flexibility hai lekin
isi wajah se bugs bhi ho sakte hain agar careless ho.

**Interview tip:** "Python statically typed hai ya dynamically?" — **dynamically typed**
(runtime par type check hoti hai), lekin **strongly typed** bhi hai (implicit unsafe conversions
nahi hoti, jaise `"5" + 5` seedha error dega, JavaScript ki tarah silently concat nahi karega).
"""))

cells.append(code("""
x = 10
print("x =", x, "| type:", type(x))

x = "ab yeh string ban gaya"     # same variable, naya type — bilkul valid hai
print("x =", x, "| type:", type(x))

x = [1, 2, 3]                     # ab list ban gaya
print("x =", x, "| type:", type(x))

x = {"key": "value"}               # ab dictionary
print("x =", x, "| type:", type(x))

print()
# Strongly typed hone ka demo — implicit unsafe conversion nahi hoti
try:
    result = "5" + 5   # str + int -> TypeError
except TypeError as e:
    print("TypeError pakad liya:", e)
"""))

# ============================================================
# 13. type() AUR id()
# ============================================================
cells.append(md("""
## 12. `type()` Aur `id()` — Object Identity

**Kya hai:**
- `type(obj)` — object ki **class/type** batata hai.
- `id(obj)` — object ki **unique memory identity** (CPython me yeh actual memory address hota
  hai, lekin isay implementation detail samjho, guarantee nahi).

**Syntax:** `type(x)`, `id(x)`

**`is` vs `==`:**
- `==` — **value equality** check karta hai (kya values barabar hain).
- `is` — **identity equality** check karta hai (kya dono same object hain memory me).

**Common gotcha:** CPython chhote integers (`-5` se `256` tak) aur kuch strings ko **cache/intern**
karta hai performance ke liye — is wajah se `a is b` kabhi kabhi `True` dikhta hai chhote numbers
ke liye, lekin yeh **guaranteed behavior nahi hai** (implementation detail hai, Python version se
depend kar sakta hai). Value compare karne ke liye hamesha `==` use karo, `is` sirf `None`, `True`,
`False` ke liye use karo.

**Interview tip:** "`is` aur `==` me farq?" — `==` value compare karta hai (`__eq__` call hota
hai), `is` identity compare karta hai (same object in memory). `None` ke sath hamesha `is None`
use karo, `== None` nahi (best practice, PEP 8 recommend karta hai).
"""))

cells.append(code("""
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print("a == b :", a == b)   # values same hain -> True
print("a is b :", a is b)   # alag objects hain memory me -> False
print("a is c :", a is c)   # c, a ka hi reference hai -> True

print()
print("type(a):", type(a))
print("id(a)  :", id(a))
print("id(c)  :", id(c), "(a jaisa hi, kyunke c = a)")

print()
# Small integer caching (CPython implementation detail — guarantee mat karo)
small1 = 100
small2 = 100
print("100 is 100 (small int cache):", small1 is small2)
print("Best practice: values compare karne ke liye '==' use karo, 'is' nahi (except None/True/False)")
"""))

# ============================================================
# 14. help() AUR dir()
# ============================================================
cells.append(md("""
## 13. `help()` Aur `dir()`

**Kya hai:**
- `help(obj)` — obj ki documentation (docstring) interactive tareeqe se dikhata hai.
- `dir(obj)` — obj ke saare attributes/methods ke naam **list** ke taur par deta hai.

**Kyun important hai:** Yeh dono Python ke **introspection tools** hain — jab kisi naye object
(library, class) ke sath kaam kar rahe ho aur documentation online na dekhni ho, `help()` aur
`dir()` se seedha terminal/notebook me pata chal jata hai woh kya support karta hai.

**Interview tip:** `dir()` bina arguments ke current scope ke names dikhata hai; kisi object par
`dir(obj)` uski class hierarchy se saare inherited attributes bhi dikhata hai (dunder methods
samet).
"""))

cells.append(code("""
# help() ka output short rakhne ke liye ek chhota, specific method choose kiya hai
help(str.upper)
"""))

cells.append(code("""
# dir() ka output bohat lamba hota hai (100+ items) — isliye filter/slice kar ke dekhte hain
all_names = dir(str)
public_names = [name for name in all_names if not name.startswith("_")]

print("Total dir(str) names        :", len(all_names))
print("Public (non-dunder) methods :", len(public_names))
print("Pehle 15 public methods      :", public_names[:15])

print()
# Kisi bhi custom object par bhi dir() chalta hai
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
own_attrs = [name for name in dir(p) if not name.startswith("_")]
print("Point object ke apne attributes:", own_attrs)
"""))

# ============================================================
# 15. PIP BASICS (markdown only, no execution)
# ============================================================
cells.append(md("""
## 14. pip Basics — Package Management

**pip** Python ka default **package manager** hai — PyPI (Python Package Index) se libraries
install karne ke liye.

> **Note:** Yeh commands **terminal me chalti hain**, notebook cell me nahi. Neeche sirf
> reference ke liye likhi hain — hum inhe execute nahi kar rahe (koi network access nahi).

**Zaroori commands:**

```bash
# Package install karna
pip install requests

# Specific version install karna
pip install requests==2.31.0

# Package uninstall karna
pip uninstall requests

# Installed packages ki list dekhna
pip list

# Current environment ke packages ko file me freeze karna (dependency tracking)
pip freeze > requirements.txt

# requirements.txt se sab packages install karna (naya machine setup karte waqt)
pip install -r requirements.txt

# python -m pip use karna behtar hai (yeh confirm karta hai ke sahi Python environment
# ke pip se install ho raha hai — especially jab multiple Python versions installed hon)
python -m pip install requests

# --user flag: system-wide ki bajaye sirf current user ke liye install karna
pip install --user requests
```

**Virtual environments (venv):** Har project ke apne isolated dependencies hone chahiye, taake
ek project ke packages dusre project se clash na karein.

```bash
python -m venv myenv          # naya virtual environment banao
myenv\\Scripts\\activate         # Windows par activate karo
source myenv/bin/activate     # Linux/Mac par activate karo
```

**Wheels (`.whl`) vs sdist (`.tar.gz`):**
- **Wheel (`.whl`)** — pre-built binary package format, install fast hoti hai (koi compile step
  nahi).
- **sdist (source distribution, `.tar.gz`)** — raw source code, install ke waqt compile/build ho
  sakta hai (dheema, lekin har platform ke liye kaam karta hai agar wheel available na ho).

**Interview tip:** "requirements.txt kya hota hai?" — ek text file jisme project ke saare
dependencies aur unke exact versions listed hote hain, taake team ke sab members (aur production
server) exact same environment reproduce kar saken.
"""))

cells.append(code("""
# Yeh optional/safe demo hai — importlib.metadata se installed package ka version pata karte hain.
# Har package ke liye try/except use kar rahe hain kyunke yeh environment-dependent hai
# (ho sakta hai kisi machine par install na ho) — is wajah se yeh code fail nahi karega.
import importlib.metadata as im

candidate_packages = ["pip", "setuptools", "wheel"]

for pkg_name in candidate_packages:
    try:
        version = im.version(pkg_name)
        print(f"{pkg_name:12} -> version {version}")
    except im.PackageNotFoundError:
        print(f"{pkg_name:12} -> installed nahi mila (theek hai, yeh sirf demo hai)")
"""))

# ============================================================
# 16. PYTHON 2 VS PYTHON 3
# ============================================================
cells.append(md("""
## 15. Python 2 Vs Python 3 Ke Farq

Python 2 ka **End of Life (EOL)** **January 1, 2020** ko official ho gaya tha — ab sirf Python 3
maintained hai. Lekin interviews me yeh farq abhi bhi poocha jata hai (legacy code samajhne ke liye).

| Feature | Python 2 | Python 3 |
|---|---|---|
| `print` | **Statement**: `print "hello"` | **Function**: `print("hello")` |
| Integer division | `5 / 2` -> `2` (floor division by default) | `5 / 2` -> `2.5` (true division); `5 // 2` -> `2` (floor) |
| Strings | `str` = bytes by default, `unicode` alag type tha | `str` = Unicode by default, `bytes` alag type hai |
| Range | `range()` list return karta tha, `xrange()` lazy tha | Sirf `range()` hai — lazy `range` object return karta hai |
| Input | `raw_input()` string leta tha, `input()` eval karta tha | Sirf `input()` hai — hamesha string return karta hai |
| Dict iteration | `d.iteritems()`, `d.iterkeys()`, `d.itervalues()` | Sirf `d.items()`, `d.keys()`, `d.values()` (yeh khud lazy/view hote hain) |
| Future imports | `from __future__ import ...` se Py3 features "borrow" karte the | Zaroorat nahi — features already default hain |
| EOL | **January 1, 2020** ko end-of-life | Actively maintained |

**Interview tip:** Sabse common poocha jane wala farq: **integer division** (`5/2`) aur
**`print` function vs statement**. Dono confidently explain kar sako.
"""))

cells.append(code("""
# Python 3 ka actual behavior demo (safe, koi Python 2 code nahi chala rahe)

print("True division  5 / 2  ->", 5 / 2)    # Python 3: hamesha float
print("Floor division 5 // 2 ->", 5 // 2)   # explicit floor division chahiye ho to yeh use karo

r = range(5)
print("range(5) ka type ->", type(r), "| value:", r, "| list bana kar dekho:", list(r))

d = {"a": 1, "b": 2}
print("dict.items() ->", list(d.items()))   # Python 2 me .iteritems() hota tha, ab bas .items()

text = "hello"
raw_bytes = text.encode("utf-8")
print("str  ->", type(text), text)
print("bytes->", type(raw_bytes), raw_bytes)

print()
# __future__ module Python 3 me bhi exist karta hai (backward compatibility ke liye)
import __future__
print("__future__.division ka feature object:", __future__.division)
print("__future__.print_function feature object:", __future__.print_function)
"""))

cells.append(code("""
# Python 2 style print statement — Python 3 me yeh SyntaxError hai
py2_style_code = 'print "Hello from Python 2 style"'

try:
    compile(py2_style_code, "<py2_snippet>", "exec")
except SyntaxError as e:
    print("Python 3 me yeh SyntaxError deta hai:", e)
"""))

# ============================================================
# COMMON MISTAKES / GOTCHAS
# ============================================================
cells.append(md("""
## Common Mistakes / Gotchas (is topic ke)

- **Colon bhool jana** — `if x > 0` ke baad `:` lagana zaroori hai, warna `SyntaxError`.
- **Indentation inconsistent hona** — ek block ke andar kuch lines 4 spaces, kuch 2 spaces —
  `IndentationError`.
- **Tabs aur spaces mix karna** — kabhi kabhi editor me dikhta nahi lekin Python `TabError` deta
  hai.
- **Case-sensitivity bhool jana** — `Name` aur `name` do alag variables hain, Python case-sensitive
  hai.
- **Keyword ko variable name banane ki koshish** — `class = 5`, `for = 10` waghera — `SyntaxError`.
- **`print` ko Python 2 ki tarah statement samajhna** — `print "text"` Python 3 me chalega nahi.
- **`is` ko value comparison ke liye use karna** — hamesha `==` use karo values ke liye, `is`
  sirf identity/`None` check ke liye.
- **`help()` ka bohat bara output notebook me dump karna** — specific method/function par `help()`
  call karo (`help(str.upper)`), poori class par nahi (jab tak zaroorat na ho).
"""))

cells.append(code("""
# Gotcha 1: case sensitivity
name = "Ali"
Name = "Sara"   # yeh EK ALAG variable hai (capital N)
print("name:", name)
print("Name:", Name)
print("Kya yeh same hain?", name == Name)
"""))

cells.append(code("""
# Gotcha 2: keyword ko identifier banane ki koshish -> SyntaxError
bad_snippet = "class = 5"

try:
    compile(bad_snippet, "<bad_identifier>", "exec")
except SyntaxError as e:
    print("SyntaxError pakad liya (keyword ko variable name banane ki koshish):", e)
"""))

# ============================================================
# REAL-WORLD PROBLEMS
# ============================================================
cells.append(md("""
## Real-World Problems

Ab tak seekhi cheezein (print parameters, docstrings, dir/type, keywords waghera) chhote
practical problems solve karne ke liye use karte hain.
"""))

cells.append(md("""
### Problem 1: Formatted Receipt Printer

Ek chhoti dukan (cafe) ka receipt print karna hai, columns aligned hon (`sep`, `end`, f-strings
alignment use karke).
"""))

cells.append(code("""
items = [("Coffee", 2, 350), ("Sandwich", 1, 650), ("Water Bottle", 3, 100)]

print("=" * 32)
print("BIZEE CAFE - RECEIPT")
print("=" * 32)

total = 0
for name, qty, price in items:
    line_total = qty * price
    total += line_total
    # f-string alignment: <15 (left align, 15 chars), >6 (right align, 6 chars)
    print(f"{name:<15}", f"x{qty}", f"Rs.{line_total:>6}", sep="  ")

print("-" * 32)
print("TOTAL:", f"Rs.{total}", sep=" ")
print("=" * 32)
"""))

cells.append(md("""
### Problem 2: "Capture Print Output" Logger

Kai baar hum print statements ko file me capture karna chahte hain (testing, logging) — `file=`
parameter aur `io.StringIO` se yeh asaan hai (koi real disk file ki zaroorat nahi).
"""))

cells.append(code("""
import io


def log_event(buffer, message, level="INFO"):
    \"\"\"Log message ko given buffer (file-like object) me likhta hai.\"\"\"
    print(f"[{level}] {message}", file=buffer)


log_buffer = io.StringIO()
log_event(log_buffer, "Server started")
log_event(log_buffer, "User login failed", level="WARN")
log_event(log_buffer, "Disk almost full", level="ERROR")

captured_logs = log_buffer.getvalue()
print("Captured logs:")
print(captured_logs)

log_lines = captured_logs.strip().split("\\n")
print("Total log lines:", len(log_lines))
print("ERROR wale lines:", [line for line in log_lines if "ERROR" in line])
"""))

cells.append(md("""
### Problem 3: Docstring-Driven Mini Help System

Chhota "help system" banate hain jo kisi bhi class/object ka docstring aur public methods
show kare — bilkul `help()` ke jaisa, apna version.
"""))

cells.append(code("""
class InventoryManager:
    \"\"\"Inventory manage karne wali simple class.

    Methods:
        add_item(name, qty): stock me item add/increase karta hai.
        remove_item(name, qty): stock se item remove/decrease karta hai.
    \"\"\"

    def add_item(self, name, qty):
        \"\"\"Item ko stock me add/increase karta hai.\"\"\"
        pass

    def remove_item(self, name, qty):
        \"\"\"Item ko stock se remove/decrease karta hai.\"\"\"
        pass


def mini_help(obj):
    \"\"\"Kisi bhi object/class ka docstring aur public methods print karta hai.\"\"\"
    print("Docstring:")
    print(obj.__doc__.strip())
    print("\\nPublic methods:")
    for attr in dir(obj):
        if not attr.startswith("_"):
            print(" -", attr)


mini_help(InventoryManager)
"""))

cells.append(md("""
### Problem 4: Environment / Diagnostic Report

Production support ke liye ek chhota "environment report" banate hain — Python version,
implementation, keywords count waghera — jo bug report ke sath attach kiya ja sake.
"""))

cells.append(code("""
import sys
import platform
import keyword


def environment_report():
    \"\"\"Machine ki Python environment ke baare me chhota diagnostic report deta hai.\"\"\"
    report = {
        "python_version": sys.version.split()[0],
        "version_info": tuple(sys.version_info[:3]),
        "implementation": platform.python_implementation(),
        "os_platform": platform.system(),
        "total_keywords": len(keyword.kwlist),
        "total_soft_keywords": len(keyword.softkwlist),
    }
    return report


report = environment_report()
for key, value in report.items():
    print(f"{key:20}: {value}")
"""))

cells.append(md("""
### Problem 5: PEP8-Style Identifier Validator

Ek chhota validator banate hain jo batata hai ke koi diya gaya naam **valid Python identifier**
ban sakta hai ya nahi — `str.isidentifier()` aur `keyword.iskeyword()`/`issoftkeyword()` combine
karke.
"""))

cells.append(code("""
import keyword


def is_valid_identifier_name(name):
    \"\"\"Batata hai ke 'name' ek valid, use-karne-laayak Python identifier hai ya nahi.\"\"\"
    if not isinstance(name, str) or not name:
        return False, "empty ya non-string value"
    if not name.isidentifier():
        return False, "invalid identifier syntax"
    if keyword.iskeyword(name):
        return False, "yeh ek Python (hard) keyword hai"
    if keyword.issoftkeyword(name):
        return True, "valid hai, lekin soft keyword hai (context me ehtiyat se use karo)"
    return True, "valid identifier"


test_names = ["total_amount", "class", "match", "1value", "user-name", "_hidden", "TotalAmount"]

for candidate in test_names:
    ok, reason = is_valid_identifier_name(candidate)
    print(f"{candidate!r:15} -> valid={str(ok):5} ({reason})")
"""))

# ============================================================
# LEETCODE
# ============================================================
cells.append(md("""
## LeetCode Problems (Easy)

Do **Easy** problems solve karte hain jo is notebook ke concepts (print formatting, `round()`,
`type()`, integer vs float) se directly connect hote hain.
"""))

cells.append(md("""
### LC 2469. Convert the Temperature — Easy
https://leetcode.com/problems/convert-the-temperature/

**Problem (Roman Urdu):** Ek `celsius` (float) diya gaya hai. Isay **Kelvin** aur **Fahrenheit**
me convert kar ke `[kelvin, fahrenheit]` list return karo. Answer me `10^-5` tak ki error
acceptable hai.

**Formulas:**
- `Kelvin = Celsius + 273.15`
- `Fahrenheit = Celsius * 1.80 + 32.00`

**Approach / Intuition:**
1. Seedha formula apply karo — koi loop ya condition ki zaroorat nahi.
2. `round(value, 5)` use karo taake floating-point precision consistent rahe (LeetCode `10^-5`
   precision expect karta hai).
3. Yeh notebook ke `type()` concept se connect hota hai — input `float` hai, output bhi dono
   `float` values ki list honi chahiye.

**Time Complexity:** O(1) — sirf 2 arithmetic operations.
**Space Complexity:** O(1) — sirf ek chhoti list return ho rahi hai.
"""))

cells.append(code("""
def convert_temperature(celsius: float) -> list[float]:
    \"\"\"Celsius ko Kelvin aur Fahrenheit me convert karta hai (LC 2469).\"\"\"
    kelvin = round(celsius + 273.15, 5)
    fahrenheit = round(celsius * 1.80 + 32.00, 5)
    return [kelvin, fahrenheit]


# LeetCode ke official examples se test cases
assert convert_temperature(36.50) == [309.65000, 97.70000]
assert convert_temperature(122.11) == [395.26000, 251.79800]

# Extra edge case: 0 Celsius (freezing point of water)
assert convert_temperature(0.0) == [273.15, 32.0]

print("convert_temperature(36.50) ->", convert_temperature(36.50))
print("convert_temperature(0.0)   ->", convert_temperature(0.0))
print("type of result elements   ->", type(convert_temperature(0.0)[0]))
print("Sab asserts pass ho gaye - LC 2469 solved")
"""))

cells.append(md("""
### LC 1281. Subtract the Product and Sum of Digits of an Integer — Easy
https://leetcode.com/problems/subtract-the-product-and-sum-of-digits-of-an-integer/

**Problem (Roman Urdu):** Ek integer `n` diya gaya hai. Uske digits ka **product** (guna) nikalo
aur digits ka **sum** (jama) nikalo, phir `product - sum` return karo.

Example: `n = 234` -> digits `[2, 3, 4]` -> product = `24`, sum = `9` -> answer = `15`.

**Approach 1 — String-based:**
1. `n` ko string me convert karo (`str(n)`), har character ko wapas `int()` karo.
2. Loop chala kar product aur sum nikal lo.

**Approach 2 — Math-based (`%` aur `//`):**
1. `n % 10` se aakhri digit milta hai, `n // 10` se woh digit hata do (integer/floor division).
2. Loop tab tak chalao jab tak `n > 0`.
3. Yeh approach **string conversion avoid karta hai** — thora zyada "number-crunching" wala,
   interviews me zyada pasand kiya jata hai.

**Time & Space Complexity (dono approaches):**
- **Time:** O(d) jahan `d` = digits ki count (roughly `log10(n)`).
- **Space:** O(d) string approach me (digits list banti hai), O(1) math approach me (sirf counters).
"""))

cells.append(code("""
def subtract_product_and_sum_string(n: int) -> int:
    \"\"\"String-based approach: n ko string bana kar digits nikalte hain.\"\"\"
    digits = [int(ch) for ch in str(n)]   # har character ko wapas int banaya

    product = 1
    for d in digits:
        product *= d

    total = sum(digits)
    return product - total


# LeetCode ke official examples
assert subtract_product_and_sum_string(234) == 15
assert subtract_product_and_sum_string(4421) == 21
assert subtract_product_and_sum_string(1) == 0   # single digit: product=1, sum=1 -> 1-1=0

print("subtract_product_and_sum_string(234) ->", subtract_product_and_sum_string(234))
print("subtract_product_and_sum_string(4421) ->", subtract_product_and_sum_string(4421))
"""))

cells.append(code("""
def subtract_product_and_sum_math(n: int) -> int:
    \"\"\"Math-based approach: % (mod) se digit nikalo, // (floor division) se hatao.\"\"\"
    product = 1
    total = 0
    while n > 0:
        digit = n % 10       # aakhri digit
        product *= digit
        total += digit
        n //= 10             # aakhri digit hata do (floor division)
    return product - total


assert subtract_product_and_sum_math(234) == 15
assert subtract_product_and_sum_math(4421) == 21

print("subtract_product_and_sum_math(234) ->", subtract_product_and_sum_math(234))
print("subtract_product_and_sum_math(4421) ->", subtract_product_and_sum_math(4421))
print()
print("Note: '//' floor division int deta hai, '/' true division float deti — yahan '//' zaroori hai")
"""))

cells.append(code("""
# Dono approaches ko random test cases par compare karte hain (consistency check)
import random

random.seed(42)   # reproducible test cases ke liye seed fix ki
test_values = [random.randint(1, 999_999) for _ in range(20)]

all_match = all(
    subtract_product_and_sum_string(v) == subtract_product_and_sum_math(v)
    for v in test_values
)

print("20 random test cases par dono approaches match karte hain?", all_match)
assert all_match

print()
print("Comparison:")
print("- String approach: readable hai, lekin str(n) conversion ka thora overhead")
print("- Math approach  : koi string conversion nahi, thora zyada 'raw' aur interview-friendly")
"""))

# ============================================================
# INTERVIEW Q&A
# ============================================================
cells.append(md("""
## Interview Questions & Answers

**Q1. Python interpreted hai ya compiled?**
Dono — source code pehle bytecode me compile hota hai (automatic, `.pyc`), phir Python Virtual
Machine (PVM) us bytecode ko interpret karti hai.

**Q2. CPython kya hai?**
Python language ka official, default implementation — C programming language me likha gaya hai.
Jab tum normally `python` command chalate ho, yehi implementation chal raha hota hai.

**Q3. `.pyc` file kya hoti hai aur `__pycache__` folder ka kaam?**
`.pyc` compiled bytecode hoti hai. Jab koi module import hota hai, Python uski bytecode
`__pycache__` folder me cache kar leta hai taake agli baar dobara compile karne ki zaroorat na
pare (jab tak source `.py` change na ho).

**Q4. `.py` script aur `.ipynb` notebook me farq?**
`.py` plain text Python file hai jo top-to-bottom ek sath chalti hai — production/scripts ke
liye behtar. `.ipynb` JSON-based notebook hai jisme cells alag-alag, interactively chalte hain,
aur state persist hoti hai — exploration/teaching ke liye behtar.

**Q5. `print()` ke zaroori parameters kya hain?**
`sep` (objects ke beech separator, default space), `end` (line ke aakhir, default newline),
`file` (output kahan jaye, default `sys.stdout`), `flush` (buffer turant flush karna hai ya nahi).

**Q6. Comment aur docstring me farq?**
Comment (`#`) sirf source code me hota hai, runtime par ghayab ho jata hai. Docstring
(triple-quoted string, function/class/module ke pehle statement ke taur par) runtime object hai
— `__doc__` attribute me store hota hai, `help()` isay use karta hai.

**Q7. Python me indentation kyun zaroori hai?**
Python curly braces `{}` ki bajaye indentation se code blocks define karta hai — yeh readability
enforce karta hai. Inconsistent indentation `IndentationError`/`TabError` deta hai.

**Q8. PEP 8 kya hai?**
Python ka official style guide — naming conventions (`snake_case` variables, `PascalCase`
classes, `UPPER_CASE` constants), line length, import order, blank lines waghera define karta hai.

**Q9. Keyword aur identifier me farq?**
Keyword Python ka reserved word hai (`if`, `for`, `class`) jo special meaning rakhta hai —
variable name ke taur par use nahi ho sakta. Identifier kisi bhi variable/function/class ka
naam hai jo developer choose karta hai (kuch rules ke sath).

**Q10. Soft keyword kya hota hai?**
Context-dependent keyword — jaise `match`, `case`, `type`, `_` — sirf specific syntax context
me special meaning rakhte hain, baaki jagah normal identifier ban sakte hain (unlike hard
keywords jo hamesha reserved hain).

**Q11. Python dynamically typed hai matlab kya?**
Variable ki type runtime par decide hoti hai object ke basis par — ek hi variable ko different
types se rebind kiya ja sakta hai. Lekin Python **strongly typed** bhi hai — implicit unsafe
type conversions nahi hoti.

**Q12. `is` aur `==` me farq?**
`==` value equality check karta hai (`__eq__` call hota hai). `is` identity equality check
karta hai — kya dono variables **same object** hain memory me. `None` ke sath hamesha `is`
use karo.

**Q13. `type()` aur `id()` ka kaam?**
`type(obj)` object ki class batata hai. `id(obj)` object ki unique memory identity (CPython me
memory address) deta hai — do objects ka `id()` same ho to woh same object hain.

**Q14. `help()` aur `dir()` me farq?**
`help(obj)` obj ki documentation (docstring) dikhata hai — readable format me. `dir(obj)` obj ke
saare available attributes/methods ke naam ki list deta hai (documentation nahi, sirf names).

**Q15. `requirements.txt` kis liye use hoti hai?**
Project ke saare dependencies aur unke exact versions record karne ke liye — `pip freeze >
requirements.txt` se banti hai, `pip install -r requirements.txt` se restore hoti hai — taake team
ke sab members same environment reproduce kar saken.

**Q16. Virtual environment (venv) kyun zaroori hai?**
Har project ke dependencies ko isolate karne ke liye — taake ek project ke package versions
dusre project ke sath clash na karein. `python -m venv myenv` se banta hai.

**Q17. Python 2 aur Python 3 ka sabse bara farq?**
`print` statement (Py2) vs function (Py3), aur integer division (`5/2` Py2 me `2`, Py3 me `2.5`).
Python 2 ka EOL January 1, 2020 tha.

**Q18. Wheel (`.whl`) aur sdist me farq?**
Wheel pre-built binary package hai (fast install, koi compile nahi), sdist (source distribution,
`.tar.gz`) raw source code hai jo install ke waqt compile ho sakta hai.

**Q19. `flush=True` kab use karte hain `print()` me?**
Jab output ko turant dikhana ho — buffering skip kar ke — masalan long-running scripts me
progress bars, ya jab output kisi pipe/file me redirect ho raha ho aur real-time dikhna zaroori ho.

**Q20. `str.isidentifier()` kya check karta hai, aur kya miss kar sakta hai?**
Sirf yeh check karta hai ke string valid Python identifier **syntax** follow karti hai (letters/
digits/underscore, number se start nahi). Yeh **keyword check nahi karta** — `"class".isidentifier()`
`True` deta hai, lekin `class` ek keyword hai isliye variable name ke taur par use nahi ho sakta.
Iske liye `keyword.iskeyword()` alag se check karna parta hai.
"""))

# ============================================================
# PRACTICE EXERCISES
# ============================================================
cells.append(md("""
## Practice Exercises (Khud Karo)

1. **Print formatting practice:** Ek list of tuples `[("Item", price), ...]` ko `print()` ke
   `sep`/`end` parameters use karke ek formatted table ki tarah print karo (bina f-string
   alignment ke, sirf `sep`/`end` se).
   *Hint:* Har row ke liye ek `print(...)` call, `sep="\\t"` try karo.

2. **Docstring writer:** Ek function `calculate_discount(price, percent)` likho jisme proper
   docstring ho (parameters aur return value describe kare), phir `.__doc__` print kar ke verify
   karo.
   *Hint:* Function ka **pehla statement** hi docstring hona chahiye (triple-quoted string).

3. **IndentationError hunter:** Teen alag bad code strings banao (har ek me alag indentation
   mistake) aur `compile()` + `try/except` se unke exact error messages print karo.
   *Hint:* `compile(code_string, "<test>", "exec")` use karo, `IndentationError`/`TabError`/
   `SyntaxError` catch karo.

4. **Identifier checker (upgrade):** Practice-5 (real-world problem) ke `is_valid_identifier_name`
   function ko upgrade karo taake yeh batae ke agar naam invalid hai to **kyun specifically**
   (starts with digit? has space? has hyphen?) — generic message ki bajaye specific reason do.
   *Hint:* `name[0].isdigit()`, `" " in name`, `"-" in name` jaisi checks add karo.

5. **Environment fingerprint:** `environment_report()` function (real-world problem 4) ko extend
   karo taake yeh `sys.getsizeof()` bhi report kare kisi sample list/dict/string ka.
   *Hint:* Dictionary me nayi keys add karo jaise `"list_size_bytes"`.

6. **Bytecode explorer:** Do chhote functions banao — ek `for` loop use kare, ek list comprehension
   use kare — dono ka same kaam ho (masalan squares nikalna 1 se 5 tak). `dis.dis()` se dono ki
   bytecode dekho aur compare karo instructions count.
   *Hint:* `dis.dis(func)` ka output ek string ki tarah treat nahi hota seedha — `dis.get_instructions()`
   use kar ke `list()` bana kar `len()` nikal sakte ho.

7. **LeetCode variant:** LC 1281 ka apna variant likho — `subtract_sum_and_product` (order
   ulta — pehle sum minus product) — aur 3-4 test cases ke sath verify karo.
   *Hint:* Bas `return total - product` kar do (product aur total ki jagah badal do).
"""))

# ============================================================
# SUMMARY / CHEAT-SHEET
# ============================================================
cells.append(md("""
## Summary / Cheat-Sheet

| Topic | Ek-line Yaad Rakhne Wali Baat |
|---|---|
| Python kya hai | High-level, interpreted, PSF-maintained; Guido van Rossum, 1991 |
| Interpreter vs Compiler | Source -> bytecode (compile) -> PVM interpret karti hai |
| CPython vs others | CPython = default (C); PyPy = JIT/fast; Jython = JVM; IronPython = .NET; MicroPython = embedded |
| `.py` vs `.ipynb` | `.py` = production/scripts; `.ipynb` = exploration/teaching |
| Jupyter shortcuts | `Shift+Enter` run, `A`/`B` insert cell, `M`/`Y` markdown/code, `D,D` delete |
| `print()` params | `sep`, `end`, `file`, `flush` |
| Comments vs docstrings | `#` = ignored by Python; docstring = runtime `__doc__` object |
| Indentation | 4 spaces standard; tabs/spaces mix -> `TabError` |
| PEP 8 | `snake_case` vars, `PascalCase` classes, `UPPER_CASE` constants |
| Keywords | `keyword.kwlist` (hard), `keyword.softkwlist` (context-dependent) |
| Identifiers | `str.isidentifier()` (syntax) + `keyword.iskeyword()` (reserved check) |
| Dynamic typing | Variable = label; object ka type hota hai, variable ka nahi |
| `type()`/`id()` | `type()` = class; `id()` = memory identity; `==` values, `is` identity |
| `help()`/`dir()` | `help()` = docs; `dir()` = attribute names list |
| pip | `pip install/uninstall/list/freeze`; `venv` = isolated environment |
| Python 2 vs 3 | `print` statement -> function; `5/2` int -> float; EOL Jan 2020 |

**Agla kadam:** Notebook 02 me variables, data types, aur operators deep-dive honge.
"""))

save(r"Python/Basics/01_Python_Introduction_and_Setup.ipynb", cells)
